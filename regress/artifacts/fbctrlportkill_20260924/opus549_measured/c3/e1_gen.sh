#!/bin/bash
set -u
CL=/tmp/gxo549c3
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/c3
T5=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/table5
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd "$CL" || exit 2
rm -rf var/v var/t5
python3 "$C/gen_c3.py" var/fix.c var/v || exit 3
( for f in var/v/*.c; do echo "=== $(basename "$f")"; diff var/fix.c "$f"; done ) > "$C/c3_variants.diff"
# regenerate table 5's 212 edits with ITS OWN generator, compare file contents
cp "$SP/dev_fbctrl_HEAD.c" var/dev_fbctrl_HEAD.c
python3 "$T5/mutants549_t5.py.txt" var/fix.c var/dev_fbctrl_HEAD.c \
    "$T5/../table4/mutants549.py.txt" "$T5/../table4/mutants549_t3.py.txt" "$T5/../table4/mutants549_t4.py.txt" var/t5 \
    > var/t5_gen.log 2>&1 || { echo "T5 GEN FAILED"; tail -3 var/t5_gen.log; exit 4; }
tail -1 var/t5_gen.log
python3 - var/t5 var/v <<'PY'
import io, os, sys
t5, v = sys.argv[1:3]
rd = lambda d, f: io.open(os.path.join(d, f), encoding="utf-8", newline="").read()
t5src = {rd(t5, f): f for f in os.listdir(t5) if f.endswith(".c")}
mine = sorted(f for f in os.listdir(v) if f.endswith(".c"))
dup = [(f, t5src[rd(v, f)]) for f in mine if rd(v, f) in t5src]
print("table-5 edits regenerated: %d ; my edits: %d ; identical to a table-5 edit: %s" % (len(t5src), len(mine), dup or "NONE"))
PY
