#!/bin/bash
# opus5 seat: run the FROZEN kt.py instrument against BASE and every mutant binary, in parallel.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE" || exit 9
STAMP=$(date +%Y%m%d_%H%M%S)
FROZEN="kt.run-$STAMP.py"
cp kt.py "$FROZEN"
md5sum kt.py "$FROZEN"
BINS=/tmp/gxopusmmuv_bins
mkdir -p kt_out
for b in "$BINS"/*; do
  n=$(basename "$b")
  ( python3 -u "$FROZEN" "$b" "$n" > "kt_out/KT_$n.out" 2>&1 ) &
done
wait
for b in "$BINS"/*; do
  n=$(basename "$b")
  printf '%-12s %s   last=%s\n' "$n" "$(grep -h '^KT_BRIEF' "kt_out/KT_$n.out")" "$(tail -1 "kt_out/KT_$n.out")"
done
echo RUN_KT_ALL_DONE
