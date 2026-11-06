#!/bin/sh
# Rebuild the proposed candidate, optionally show its diff, and run finite checks.
# Usage: tools/iterate.sh [PREV_READER.md] (run from the package root)
set -eu
PREV=${1:-}
NAME=MANUSCRIPT_PROPOSED_v1.1_2026-11-06
python3 BUILD.py
if [ -n "$PREV" ]; then
    if [ ! -f "$PREV" ]; then
        printf 'Previous Markdown file not found: %s\n' "$PREV" >&2
        exit 2
    fi
    if diff -u "$PREV" "$NAME.md"; then
        :
    else
        diff_status=$?
        if [ "$diff_status" -ne 1 ]; then
            exit "$diff_status"
        fi
    fi
fi
python3 CHECK_CANDIDATE.py
sha256sum "$NAME.md"
wc -c < "$NAME.md"
