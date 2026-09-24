#!/bin/bash
set -u
X=/tmp/gxr3fv
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
Q=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h
rm -rf "$X"; mkdir -p "$X/regress"; cp -a "$SEC/src" "$X/src"; cp "$SEC/config.h" "$X/"
cp "$SEC/regress/diff_footbridge.c" "$X/regress/r3e.c"; cp "$Q/diff_footbridge.r3f.c" "$X/regress/r3f.c"
cd "$X/regress"
for v in r3e r3f; do gcc -fpreprocessed -dD -E -P "$v.c" 2>/dev/null | tr -s ' \t\n' ' ' > "$v.stripped"; done
cmp -s r3e.stripped r3f.stripped && echo "STRIPPED: identical ($(wc -c < r3e.stripped) bytes)" || echo "STRIPPED: DIFFER"
for v in r3e r3f; do
  gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I"$X/src" -I"$X/src/include" -I"$X/src/include/thirdparty" \
      -ffunction-sections -fdata-sections -Wl,--gc-sections -o "$v" "$v.c" -lm 2> "$v.build" || echo "$v BUILD FAILED"
  ./"$v" > "$v.out" 2>&1; echo "$v rc=$? $(grep -oE '^[0-9]+ rows[^.]*' $v.out) $(tail -n 1 $v.out)"
done
cmp -s r3e.out r3f.out && echo "OUTPUT: identical" || { echo "OUTPUT: DIFFER"; diff r3e.out r3f.out | head; }
echo "r3f md5 $(md5sum r3f.c | cut -c1-8)"; rm -rf "$X"; echo VERIFY_R3F_DONE
