#!/bin/bash
# Enumerate clone divergences vs GXEMUL-SEC working tree
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cd /tmp/gxopus539p1 || exit 9
mkdir -p out
cd src || exit 9
find . \( -name '*.c' -o -name '*.h' \) | sed 's|^\./||' | while read -r f; do
  if [ -f "$SEC/src/$f" ]; then
    cmp -s "$f" "$SEC/src/$f" || echo "DIFF   src/$f"
  else
    echo "ABSENT-IN-SEC src/$f"
  fi
done | sort
