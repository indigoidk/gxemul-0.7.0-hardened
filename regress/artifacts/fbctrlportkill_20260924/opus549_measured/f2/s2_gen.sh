#!/bin/bash
# Generate every variant into the clone and verify the p2 variants are the ones p2 measured.
set -u
CL=/tmp/gxo549f2m
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
ART=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd "$CL" || exit 2
cp "$SP/dev_fbctrl_HEAD.c" var/dev_fbctrl_HEAD.c
md5sum var/fix.c var/dev_fbctrl_HEAD.c
cmp var/fix.c /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_fbctrl.c && echo "fix.c CMP SEC: CLEAN"
rm -rf var/v
python3 "$F2/gen_variants_f2.py" var/fix.c var/dev_fbctrl_HEAD.c "$ART/table2/mutants549.py.txt" /tmp/gxopus549p2_var var/v || exit 3
( for f in var/v/N_*.c; do echo "=== $(basename "$f")"; diff var/fix.c "$f"; done ) > var/variants_regen.diff
if cmp var/variants_regen.diff "$ART/opus549_measured/p2/variants.diff"; then echo "P2 VARIANTS: regenerated diff == p2/variants.diff (byte-identical)"; else echo "P2 VARIANTS DIFFER"; fi
# the M_ set must also match table 2's own recorded mutants: compare each to its make-log-free source by diff count
for f in var/v/*.c; do n=$(diff var/fix.c "$f" | grep -c '^[<>]'); echo "$(basename "$f" .c) changed_lines=$n"; done
ls var/v | wc -l
