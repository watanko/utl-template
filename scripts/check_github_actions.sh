#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
workflow_files=(.github/workflows/*.yml .github/workflows/*.yaml)

if [ "${#workflow_files[@]}" -eq 0 ]; then
  echo "GitHub Actions workflows are disabled; skipping actionlint."
  exit 0
fi

actionlint "${workflow_files[@]}"
