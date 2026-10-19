#!/bin/bash
#  legs41.sh -- #567 probe v4.1 (the working tree's regress/fbctrl_cmd_probe.py, 125 rows): plain regression runs on the
#  fixed build (/tmp/gx567), the original build (/tmp/gx566, HEAD's dev_fbctrl.c) and two null media.  Mutates nothing.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/fbcmd
OUT=$S/legs41
mkdir -p "$OUT"
P=$OUT/probe.v41.frozen.py
cp "$R/regress/fbctrl_cmd_probe.py" "$P"
F=src/devices/dev_fbctrl.c
{
echo "LEGS41 start $(date '+%F %T'); probe md5 $(md5sum < "$P" | cut -c1-32)"
echo "/tmp/gx567: $(cmp -s "$S/dev_fbctrl.fix567.c" /tmp/gx567/$F && echo 'the fix' || echo 'NOT the fix'), $([ /tmp/gx567/gxemul -nt /tmp/gx567/$F ] && echo 'binary fresh' || echo 'binary STALE'), sentinel $([ -e /tmp/gx567/.MUTANT ] && echo PRESENT || echo none)"
echo "/tmp/gx566: $(cmp -s "$S/dev_fbctrl.head.c" /tmp/gx566/$F && echo 'HEAD source' || echo 'NOT HEAD'), $([ /tmp/gx566/gxemul -nt /tmp/gx566/$F ] && echo 'binary fresh' || echo 'binary STALE')"
} | tee "$OUT/LEGS41.txt"
for leg in FIX:/tmp/gx567/gxemul HEAD:/tmp/gx566/gxemul C_absent:/nonexistent/gxemul C_bintrue:/bin/true; do
    name=${leg%%:*}; bin=${leg#*:}
    python3 -u "$P" "$bin" > "$OUT/$name.raw" 2>&1
    rc=$?
    printf '%-10s rc=%s %s %s last=%s\n' "$name" "$rc" "$(grep -a '^FBCMD_RESULT' "$OUT/$name.raw")" \
        "$(grep -a '^FBCMD_CONTROL' "$OUT/$name.raw")" "$(tail -n 1 "$OUT/$name.raw")" | tee -a "$OUT/LEGS41.txt"
    grep -aE '^  (edge x1|edge y1) ' "$OUT/$name.raw" | sed 's/^/      /' | tee -a "$OUT/LEGS41.txt"
done
echo "LEGS41 end $(date '+%F %T')" | tee -a "$OUT/LEGS41.txt"
echo LEGS41_DONE | tee -a "$OUT/LEGS41.txt"
