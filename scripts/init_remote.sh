#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-Krishlo-Chen/hsi-paper-watch}"
VISIBILITY="${2:---private}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is required: https://cli.github.com/" >&2
  exit 1
fi

if [ ! -d .git ]; then
  git init
fi

git add .
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "init: HSI paper watch repository"
fi

gh repo create "$REPO" "$VISIBILITY" --source=. --remote=origin --push
