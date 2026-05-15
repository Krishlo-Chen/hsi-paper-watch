# HSI Paper Watch

Daily repository for newly discovered Human-Scene Interaction (HSI) papers and code.

This repo is designed for a daily discovery workflow:

1. Search recent HSI-related papers, currently focused on arXiv and public GitHub signals.
2. Remove duplicates already listed in Awesome-Human-Motion.
3. Remove explicit exclusions, including `EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents`.
4. Store structured metadata, a daily report, and paper-specific notes for any remaining new findings.

## Current seed

As of 2026-05-15 JST, the non-duplicate item seeded from today's review is:

- **FunHSI** — `Open-Vocabulary Functional 3D Human-Scene Interaction Generation`
  - arXiv: https://arxiv.org/abs/2601.20835
  - code status: not confirmed in this initial seed; the daily workflow will keep checking public GitHub candidates.

`EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents` is intentionally excluded.

## Repository layout

```text
.
├── .github/workflows/daily_hsi_discovery.yml  # daily scheduled task
├── data/
│   ├── config.json                            # search queries and source settings
│   ├── discovered_papers.json                 # cumulative structured paper index
│   └── exclusions.json                        # explicit exclusions and duplicate sources
├── papers/YYYY-MM-DD/<paper-slug>/            # per-paper metadata and notes
├── reports/YYYY-MM-DD.md                      # daily discovery report
└── scripts/
    ├── discover_hsi.py                        # daily discovery script
    └── init_remote.sh                         # helper for first push to GitHub
```

## Daily schedule

The workflow runs at `00:35 UTC` every day, which is `09:35 JST`. It can also be run manually from the GitHub Actions tab.

The workflow commits changes only when the discovery script creates or updates files.

## First-time GitHub setup

From inside this folder, run:

```bash
git init
git add .
git commit -m "init: HSI paper watch repository"
gh repo create Krishlo-Chen/hsi-paper-watch --private --source=. --remote=origin --push
```

To make the repository public instead, replace `--private` with `--public`.

## Local run

```bash
python3 scripts/discover_hsi.py --days-back 14
```

Useful environment variables:

- `GITHUB_TOKEN` or `GH_TOKEN`: optional, improves GitHub repository search rate limits.
- `HSI_DAYS_BACK`: optional default lookback window for daily search.
