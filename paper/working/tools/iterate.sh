#!/bin/sh
# Rebuild, diff against the previous reader-facing Markdown, run checks. Run from package root.
# Usage: tools/iterate.sh [PREV_READER.md]
set -e
PREV=${1:-/home/claude/_prev_reader.md}; NAME=MANUSCRIPT_V1R12_2026-10-26
rm -rf build; python3 BUILD.py | tail -1
echo "--- changed reader lines vs previous:"; diff "$PREV" $NAME.md | grep '^[<>]' | cut -c1-200 || true
python3 CHECK_CANDIDATE.py 2>&1 | grep -E 'screen|links_checked|Assertion|Error' || true
echo "--- $(sha256sum $NAME.md | cut -d' ' -f1)  $(wc -c < $NAME.md) bytes; $(pdfinfo $NAME.pdf | grep Pages)"
