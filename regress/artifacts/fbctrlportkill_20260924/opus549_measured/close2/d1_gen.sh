#!/bin/bash
set -u
CL=/tmp/gxo549cf2
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close2
T4=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/table4
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
cd "$CL" || exit 2
rm -rf var/v var/t4
python3 "$C/gen_close2.py" var/fix.c var/v || exit 3
( for f in var/v/*.c; do echo "=== $(basename "$f")"; diff var/fix.c "$f"; done ) > "$C/close2_variants.diff"
# regenerate table 4's 101 edits with its OWN generator and compare file contents
cp "$SP/dev_fbctrl_HEAD.c" var/dev_fbctrl_HEAD.c
python3 "$T4/mutants549_t4.py.txt" var/fix.c var/dev_fbctrl_HEAD.c "$T4/mutants549.py.txt" "$T4/mutants549_t3.py.txt" var/t4 || exit 4
python3 - var/t4 var/v <<'PY'
import io, os, sys
t4, v = sys.argv[1:3]
rd = lambda d, f: io.open(os.path.join(d, f), encoding="utf-8", newline="").read()
t4src = {rd(t4, f): f for f in os.listdir(t4) if f.endswith(".c")}
mine = sorted(f for f in os.listdir(v) if f.endswith(".c"))
dup = [(f, t4src[rd(v, f)]) for f in mine if rd(v, f) in t4src]
print("table-4 edits regenerated: %d; closing-F2 edits: %d; identical to a table-4 edit: %s" % (len(t4src), len(mine), dup or "NONE"))
PY
