#!/bin/bash
set -u
CL=/tmp/gxo549close
C=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/close
T3=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/table3
cd "$CL" || exit 2
rm -rf var/v
python3 "$C/gen_close.py" var/fix.c var/v || exit 3
( for f in var/v/*.c; do echo "=== $(basename "$f")"; diff var/fix.c "$f"; done ) > "$C/close_variants.diff"
# none of these may be one of table 3's 62: compare each to every table-3 mutant source the t3 generator would write
python3 - "$T3/mutants549_t3.py.txt" "$T3/mutants549.py.txt" var/fix.c var/v <<'PY'
import io, os, sys, types
t3, t2, fix, vdir = sys.argv[1:5]
ns = {"__name__": "x"}
src = io.open(t3, encoding="utf-8").read().replace('if __name__ == "__main__":', "if False:")
exec(src, ns)
ns2 = {"__name__": "mutants549"}
exec(io.open(t2, encoding="utf-8").read(), ns2)
base = io.open(fix, encoding="utf-8", newline="").read()
t3src = {}
for name, cls, edits in list(ns2["MUTANTS"]) + ns["TARGETS"] + ns["PASS2"]:
    if edits is None:
        continue
    s = base
    ok = True
    for old, new in edits:
        if s.count(old) != 1:
            ok = False
            break
        s = s.replace(old, new)
    if ok:
        t3src[s] = name
mine = sorted(f for f in os.listdir(vdir) if f.endswith(".c"))
dup = [f for f in mine if io.open(os.path.join(vdir, f), encoding="utf-8", newline="").read() in t3src]
print("table-3 edits regenerated against the final source: %d; closing edits: %d; identical to a table-3 edit: %s"
      % (len(t3src), len(mine), dup or "NONE"))
PY
