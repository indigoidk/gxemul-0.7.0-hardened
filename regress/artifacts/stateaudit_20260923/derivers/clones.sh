#!/bin/bash
for d in /tmp/gxfbd5*; do
  [ -d "$d" ] || continue
  s=none; [ -f "$d/.MUTANT" ] && s=$(cat "$d/.MUTANT")
  echo "$d  sentinel=$s  bin=$(stat -c %y "$d/gxemul" 2>/dev/null | cut -c1-19)  md5=$(md5sum "$d/gxemul" 2>/dev/null | cut -c1-8)"
done
