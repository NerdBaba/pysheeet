#!/usr/bin/env bash
set -euo pipefail

# Phase 1: Bulk pandoc convert docs/notes/*.rst -> vitepress/**/*.md
SRC="${1:-docs/notes}"
DST="${2:-vitepress}"

if [[ ! -d "$SRC" ]]; then
    echo "Source directory not found: $SRC" >&2
    exit 1
fi

# Mirror category folders; convert .rst -> .md
find "$SRC" -name "*.rst" -type f | while read -r f; do
    rel="${f#${SRC}/}"
    out="${DST}/${rel%.rst}.md"
    mkdir -p "$(dirname "$out")"
    pandoc "$f" \
        -f rst \
        -t gfm-raw_html \
        --wrap=none \
        -o "$out"
    echo "  converted: $rel"
done

echo "Phase 1 complete: $(find "$DST" -name "*.md" -type f | wc -l | tr -d ' ') files written"
