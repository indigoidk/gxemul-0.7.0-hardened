#!/bin/bash
# usage: run.sh <script.py> <outfile> [args...]   -- runs inside WSL, from this directory
cd "$(dirname "$0")" || exit 9
S="$1"; shift
O="$1"; shift
python3 -u "$S" "$@" > "$O" 2>&1
echo "RC=$?"
