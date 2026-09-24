#!/bin/bash
# Compare the CURRENT working tree (tracked + untracked, .gitignore honoured) against the
# 2026-09-21 snapshots WITHOUT touching the real index, HEAD or the tree.
set -u
cd /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC || exit 9
SP=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
IDX="$SP/tmpidx_$$"
echo "control BEFORE: staged=$(git diff --cached --name-only | wc -l) porcelain=$(git status --porcelain | wc -l) HEAD=$(git rev-parse --short HEAD)"
GIT_INDEX_FILE="$IDX" git read-tree HEAD || exit 8
GIT_INDEX_FILE="$IDX" git add -A . 2>"$SP/tmpidx_add.err" || { echo "add failed"; tail -5 "$SP/tmpidx_add.err"; }
NOW=$(GIT_INDEX_FILE="$IDX" git write-tree)
rm -f "$IDX"
echo "current full tree = $NOW"
echo "control AFTER:  staged=$(git diff --cached --name-only | wc -l) porcelain=$(git status --porcelain | wc -l) HEAD=$(git rev-parse --short HEAD)"
echo
echo "=== NOW vs ff7ab93 (peer temp-index snapshot 09-21 15:36): name-status summary ==="
git diff --no-renames --name-status ff7ab93 "$NOW" > "$SP/vs_ff7ab93.txt"
awk '{print $1}' "$SP/vs_ff7ab93.txt" | sort | uniq -c
echo "--- DELETED since the snapshot (D) ---"
grep -P '^D\t' "$SP/vs_ff7ab93.txt" | head -60
echo "--- MODIFIED since the snapshot (M), outside regress/artifacts ---"
grep -P '^M\t' "$SP/vs_ff7ab93.txt" | grep -v 'regress/artifacts/' | head -60
echo "--- MODIFIED inside regress/artifacts (count) ---"
grep -P '^M\t' "$SP/vs_ff7ab93.txt" | grep -c 'regress/artifacts/'
echo "--- ADDED since the snapshot (A), by top dirs ---"
grep -P '^A\t' "$SP/vs_ff7ab93.txt" | cut -f2 | awk -F/ '{ if ($1=="regress" && $2=="artifacts") print $1"/"$2"/"$3"/"$4; else print $1"/"$2 }' | sort | uniq -c | sort -rn | head -30
echo
echo "=== tracked-only: NOW vs 4b8fe17 (my stash-create snapshot 09-21 15:34) ==="
git diff --no-renames --stat 4b8fe17 "$NOW" -- $(git ls-tree -r --name-only HEAD | tr '\n' ' ' | head -c 0) . ':(exclude)regress/artifacts' ':(exclude)_scratchpad' 2>/dev/null | tail -40
echo "NOW=$NOW" > "$SP/now_tree.txt"
