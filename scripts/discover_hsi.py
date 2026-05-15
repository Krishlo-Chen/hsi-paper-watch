#!/usr/bin/env python3
"""Discover recent HSI-related papers and store non-duplicate metadata.

The script intentionally avoids non-standard dependencies so it can run in
GitHub Actions without a setup step beyond Python.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PAPERS_DIR = ROOT / "papers"
REPORTS_DIR = ROOT / "reports"

ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def now_in_timezone(tz_name: str) -> dt.datetime:
    if ZoneInfo is not None:
        return dt.datetime.now(ZoneInfo(tz_name))
    if tz_name == "Asia/Tokyo":
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    return dt.datetime.now(dt.timezone.utc)


def normalize_title(text: str) -> str:
    text = text.lower()
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_blob(text: str) -> str:
    return normalize_title(text)


def slugify(text: str, max_len: int = 96) -> str:
    slug = normalize_title(text).replace(" ", "-")
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:max_len].strip("-") or "paper"


def http_get(url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None) -> str:
    req_headers = {"User-Agent": "hsi-paper-watch/0.1"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310 - controlled public URLs
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def parse_arxiv_datetime(value: str) -> Optional[dt.datetime]:
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError:
        return None


def arxiv_id_from_url(url: str) -> str:
    m = re.search(r"/abs/([^/?#]+)", url)
    return m.group(1) if m else url.rstrip("/").split("/")[-1]


def query_arxiv(search_query: str, max_results: int) -> List[Dict[str, Any]]:
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    xml_text = http_get(url)
    root = ET.fromstring(xml_text)
    entries: List[Dict[str, Any]] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ARXIV_NS) or "").split())
        paper_url = entry.findtext("atom:id", default="", namespaces=ARXIV_NS) or ""
        authors = [
            (name.text or "").strip()
            for name in entry.findall("atom:author/atom:name", ARXIV_NS)
            if (name.text or "").strip()
        ]
        links = []
        pdf_url = None
        for link in entry.findall("atom:link", ARXIV_NS):
            href = link.attrib.get("href", "")
            rel = link.attrib.get("rel", "")
            title_attr = link.attrib.get("title", "")
            type_attr = link.attrib.get("type", "")
            links.append({"href": href, "rel": rel, "title": title_attr, "type": type_attr})
            if title_attr == "pdf" or type_attr == "application/pdf":
                pdf_url = href
        arxiv_id = arxiv_id_from_url(paper_url)
        entries.append(
            {
                "id": f"arxiv:{arxiv_id}",
                "arxiv_id": arxiv_id,
                "title": title,
                "summary": summary,
                "authors": authors,
                "published": entry.findtext("atom:published", default="", namespaces=ARXIV_NS),
                "updated": entry.findtext("atom:updated", default="", namespaces=ARXIV_NS),
                "paper_url": paper_url,
                "pdf_url": pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
                "links": links,
                "source": "arXiv",
            }
        )
    return entries


def is_recent(entry: Dict[str, Any], cutoff: dt.datetime) -> bool:
    published = parse_arxiv_datetime(entry.get("published", ""))
    updated = parse_arxiv_datetime(entry.get("updated", ""))
    compare = updated or published
    if compare is None:
        return True
    if compare.tzinfo is None:
        compare = compare.replace(tzinfo=dt.timezone.utc)
    return compare >= cutoff.astimezone(dt.timezone.utc)


def is_relevant(entry: Dict[str, Any], keywords: Iterable[str]) -> bool:
    text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
    hits = [kw.lower() for kw in keywords if kw.lower() in text]
    if "human-scene interaction" in hits or "human scene interaction" in hits:
        return True
    return len(hits) >= 2


def load_awesome_text(exclusions: Dict[str, Any]) -> Tuple[str, List[str]]:
    source = exclusions.get("duplicate_sources", {}).get("awesome_human_motion", {})
    urls = list(source.get("raw_readme_candidates", []))
    homepage = source.get("homepage")
    if homepage:
        urls.append(homepage)
    texts = []
    used = []
    for url in urls:
        try:
            texts.append(http_get(url, timeout=20))
            used.append(url)
        except Exception as exc:  # keep going; report later
            print(f"warning: could not fetch duplicate source {url}: {exc}", file=sys.stderr)
    return "\n".join(texts), used


def github_code_candidates(title: str, short_name: Optional[str], top_k: int) -> List[Dict[str, Any]]:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    queries = []
    if short_name:
        queries.append(f'"{short_name}" in:name,description,readme')
    queries.append(f'"{title}" in:name,description,readme')

    seen = set()
    results: List[Dict[str, Any]] = []
    for q in queries:
        params = urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": top_k})
        url = f"https://api.github.com/search/repositories?{params}"
        try:
            payload = json.loads(http_get(url, timeout=20, headers=headers))
        except Exception as exc:
            print(f"warning: GitHub code search failed for {title}: {exc}", file=sys.stderr)
            continue
        for item in payload.get("items", []):
            html_url = item.get("html_url")
            if not html_url or html_url in seen:
                continue
            seen.add(html_url)
            results.append(
                {
                    "full_name": item.get("full_name"),
                    "url": html_url,
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count", 0),
                    "updated_at": item.get("updated_at"),
                }
            )
        if results:
            break
        time.sleep(1)
    return results[:top_k]


def infer_short_name(title: str) -> Optional[str]:
    m = re.search(r"\b([A-Z][A-Za-z0-9]*HSI[A-Za-z0-9]*)\b", title)
    if m:
        return m.group(1)
    return None


def build_paper_record(entry: Dict[str, Any], discovered_on: str, config: Dict[str, Any]) -> Dict[str, Any]:
    short_name = infer_short_name(entry["title"])
    code_candidates: List[Dict[str, Any]] = []
    if config.get("code_search_enabled", True):
        code_candidates = github_code_candidates(entry["title"], short_name, int(config.get("code_search_top_k", 5)))
    code_status = "candidates_found" if code_candidates else "not_confirmed"
    return {
        "id": entry["id"],
        "title": entry["title"],
        "short_name": short_name,
        "authors": entry.get("authors", []),
        "submitted": entry.get("published"),
        "last_revised": entry.get("updated"),
        "discovered_on": discovered_on,
        "source": entry.get("source", "arXiv"),
        "paper_url": entry.get("paper_url"),
        "pdf_url": entry.get("pdf_url"),
        "code": {
            "status": code_status,
            "url": code_candidates[0]["url"] if code_candidates else None,
            "candidates": code_candidates,
        },
        "duplicate_filter": {
            "awesome_human_motion": "not_found",
            "explicit_exclusions": "not_excluded",
        },
        "tags": ["HSI", "human-scene interaction"],
        "summary": entry.get("summary", ""),
    }


def write_paper_folder(record: Dict[str, Any]) -> None:
    date = record["discovered_on"]
    slug_parts = []
    if record.get("short_name"):
        slug_parts.append(record["short_name"])
    slug_parts.append(record["title"])
    slug = slugify(" ".join(slug_parts))
    folder = PAPERS_DIR / date / slug
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "metadata.json", record)
    readme = textwrap.dedent(
        f"""
        # {record.get('short_name') or 'Paper'} — {record['title']}

        - **Paper:** {record.get('paper_url') or ''}
        - **PDF:** {record.get('pdf_url') or ''}
        - **Discovered on:** {date}
        - **Code status:** {record.get('code', {}).get('status')}
        - **Code URL:** {record.get('code', {}).get('url') or 'not confirmed'}

        ## Summary

        {record.get('summary') or 'No summary captured.'}
        """
    ).strip() + "\n"
    (folder / "README.md").write_text(readme, encoding="utf-8")


def write_report(date: str, new_records: List[Dict[str, Any]], skipped: Dict[str, List[str]], duplicate_sources: List[str]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{date}.md"
    lines = [
        f"# HSI daily discovery report — {date} JST",
        "",
        "## Kept new findings",
        "",
    ]
    if new_records:
        for rec in new_records:
            lines.extend(
                [
                    f"### {rec.get('short_name') or rec['title']}",
                    "",
                    f"- **Title:** {rec['title']}",
                    f"- **Paper:** {rec.get('paper_url') or ''}",
                    f"- **PDF:** {rec.get('pdf_url') or ''}",
                    f"- **Code status:** {rec.get('code', {}).get('status')}",
                    f"- **Code URL:** {rec.get('code', {}).get('url') or 'not confirmed'}",
                    "",
                ]
            )
    else:
        lines.append("No new non-duplicate HSI papers found today.")
        lines.append("")

    lines.extend(["## Skipped", ""])
    for reason, titles in skipped.items():
        lines.append(f"### {reason}")
        if titles:
            for title in sorted(set(titles)):
                lines.append(f"- {title}")
        else:
            lines.append("- None")
        lines.append("")

    lines.extend(["## Duplicate sources checked", ""])
    if duplicate_sources:
        for src in duplicate_sources:
            lines.append(f"- {src}")
    else:
        lines.append("- No duplicate sources were reachable during this run.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily HSI paper discovery")
    parser.add_argument("--days-back", type=int, default=None, help="lookback window in days")
    parser.add_argument("--dry-run", action="store_true", help="do not write files")
    args = parser.parse_args()

    config = load_json(DATA_DIR / "config.json", {})
    exclusions = load_json(DATA_DIR / "exclusions.json", {})
    discovered = load_json(DATA_DIR / "discovered_papers.json", [])

    tz_name = config.get("timezone", "Asia/Tokyo")
    today = now_in_timezone(tz_name).date()
    today_s = today.isoformat()
    days_back = args.days_back or int(os.getenv("HSI_DAYS_BACK", config.get("default_days_back", 14)))
    cutoff = dt.datetime.combine(today - dt.timedelta(days=days_back), dt.time.min, tzinfo=dt.timezone.utc)

    awesome_text, duplicate_sources = load_awesome_text(exclusions)
    awesome_blob = normalize_blob(awesome_text)

    known_titles = {normalize_title(item.get("title", "")) for item in discovered if item.get("title")}
    known_ids = {item.get("id") for item in discovered if item.get("id")}
    excluded_titles = {
        normalize_title(title)
        for title in exclusions.get("explicit_title_exclusions", [])
        if title
    }

    candidates_by_id: Dict[str, Dict[str, Any]] = {}
    skipped: Dict[str, List[str]] = {
        "explicit_exclusions": [],
        "already_discovered": [],
        "awesome_human_motion_duplicates": [],
        "not_recent_or_not_relevant": [],
    }

    for query in config.get("arxiv_queries", []):
        try:
            entries = query_arxiv(query, int(config.get("max_results_per_query", 50)))
        except Exception as exc:
            print(f"warning: arXiv query failed [{query}]: {exc}", file=sys.stderr)
            continue
        for entry in entries:
            title_norm = normalize_title(entry.get("title", ""))
            if not title_norm:
                continue
            if title_norm in excluded_titles or any(ex in title_norm for ex in excluded_titles):
                skipped["explicit_exclusions"].append(entry["title"])
                continue
            if entry.get("id") in known_ids or title_norm in known_titles:
                skipped["already_discovered"].append(entry["title"])
                continue
            if title_norm and title_norm in awesome_blob:
                skipped["awesome_human_motion_duplicates"].append(entry["title"])
                continue
            if not is_recent(entry, cutoff) or not is_relevant(entry, config.get("relevance_keywords", [])):
                skipped["not_recent_or_not_relevant"].append(entry["title"])
                continue
            candidates_by_id[entry["id"]] = entry
        time.sleep(1)

    new_records = [build_paper_record(entry, today_s, config) for entry in candidates_by_id.values()]
    new_records.sort(key=lambda rec: rec.get("submitted") or "", reverse=True)

    if not args.dry_run:
        if new_records:
            discovered.extend(new_records)
            discovered.sort(key=lambda rec: (rec.get("discovered_on") or "", rec.get("submitted") or ""), reverse=True)
            write_json(DATA_DIR / "discovered_papers.json", discovered)
            for rec in new_records:
                write_paper_folder(rec)
        write_report(today_s, new_records, skipped, duplicate_sources)

    print(f"date={today_s}")
    print(f"new_records={len(new_records)}")
    for rec in new_records:
        print(f"- {rec['title']} :: {rec.get('paper_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
