#!/bin/bash
S=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
for C in /tmp/gx541 /tmp/gx542; do
  [ -d "$C" ] || { echo "$C MISSING"; continue; }
  s="none"; [ -f "$C/.MUTANT" ] && s=$(cat "$C/.MUTANT")
  echo "== $C  sentinel=$s  binary=$(stat -c %y $C/gxemul 2>/dev/null | cut -c1-19) md5=$(md5sum $C/gxemul 2>/dev/null | cut -c1-8)"
  for f in $(cd "$C" && find src -type f \( -name '*.c' -o -name '*.h' \) | sort); do
    [ -f "$S/$f" ] || { echo "  ONLY-IN-CLONE $f"; continue; }
    cmp -s "$C/$f" "$S/$f" || echo "  DIFFERS $f  clone_md5=$(md5sum "$C/$f" | cut -c1-8)  mtime=$(stat -c %y "$C/$f" | cut -c1-16)"
  done
done
