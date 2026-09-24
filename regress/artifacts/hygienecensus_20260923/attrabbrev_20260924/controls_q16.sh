#!/bin/bash
# attrabbrev Q16-Q18 + the Opus seat's SF2 variants C1, K4, Lg5 (PREDICTIONS_q16.txt), re-measured.  Variants IN MEMORY
# (one line of the checker's source replaced, exec'd with __file__ = the real path); no tree file changes.
# usage: ATTR_A=<this dir> SP=<scratch> controls_q16.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir for the injected ledgers}
setrow() {   # setrow <name> <row id> <field> <value>
	python - "$SEC/tools/pipeline/ledger.json" "$SP/ledger_$1.json" "$2" "$3" "$4" <<'PYEOF'
import io, json, sys
src, out, rid, field, val = sys.argv[1:6]
L = json.load(io.open(src, encoding="utf-8"))
n = 0
for r in L["rows"]:
    if r["id"] == rid:
        r[field] = val
        n += 1
assert n == 1, n
io.open(out, "w", encoding="utf-8").write(json.dumps(L, indent=1, ensure_ascii=False))
PYEOF
}
variant() {   # variant <out> <which>
	python - "$CHK" "$2" > "$A/$1" 2>&1 <<'PYEOF'
import sys
p, which = sys.argv[1:3]
BS = chr(92)
src = open(p, encoding="utf-8").read()
join = '    subjects = " ' + BS + 'n".join(sub for _full, _h, sub in log)'
EDITS = {
    "C1":  ('                if names(row.get("reopened"), full):',
            '                if names(row.get("reopened"), h):'),
    "K4":  ('            if CLOSURE.search(subj) and state != "closed":',
            '            if CLOSURE.search(subj) and state not in ("closed", "held"):'),
    "Lg5": (join, join.replace("join(sub for", "join(_h for")),
    "pipecode": ('        or p.startswith("tools/pipeline/")',
                 '        or (p.startswith("tools/pipeline/") and not p.endswith((".py", ".sh")))'),
}
old, new = EDITS[which]
assert src.count(old) == 1, "variant site not found: " + which
src = src.replace(old, new)
ns = {"__name__": "attrabbrev_variant", "__file__": p}
exec(compile(src, p, "exec"), ns)
sys.exit(ns["main"]([]))
PYEOF
	echo "$1 rc=$?"
}
setrow full pcc2widthkills reopened "b78bb0f6b2ab7b7bb58323ad2a12a205116100b6 -- the closure its later passes superseded (Q16)"
setrow held fbdeclinefive state held
setrow open fbdeclinefive state open
setrow inwork fbdeclinefive state "in work"
export GXATTR_DEPTH=130
GXLEDGER="$SP/ledger_full.json" python "$CHK" > "$A/post_Q16.out" 2>&1; echo "post_Q16.out rc=$?"
GXLEDGER="$SP/ledger_full.json" variant var_C1_Q16.out C1
GXLEDGER= variant var_C1_Q2.out C1
export GXATTR_DEPTH=60
GXLEDGER="$SP/ledger_held.json" python "$CHK" > "$A/post_Q17a.out" 2>&1; echo "post_Q17a.out rc=$?"
GXLEDGER="$SP/ledger_open.json" python "$CHK" > "$A/post_Q17b.out" 2>&1; echo "post_Q17b.out rc=$?"
GXLEDGER="$SP/ledger_held.json" variant var_K4_Q17a.out K4
GXLEDGER="$SP/ledger_inwork.json" variant var_K4_Q15.out K4
GXLEDGER= variant var_Lg5_Q0.out Lg5
export GXATTR_DEPTH=800
GXLEDGER= variant var_Q18.out pipecode
# the population claim: of the 60 scanned commits, how many touch tools/pipeline/*.py|*.sh
python - "$CHK" > "$A/pipeline_code_census.out" 2>&1 <<'PYEOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("cca", sys.argv[1]); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
log = [l.split("\t", 2) for l in m.git("log", "--format=%H\t%h\t%s", "-60").splitlines() if l.count("\t") >= 2]
touch = exempt = 0
for full, h, subj in log:
    paths = [x for x in m.git("show", "--name-only", "--format=", full).splitlines() if x.strip()]
    if any(x.startswith("tools/pipeline/") and x.endswith((".py", ".sh")) for x in paths):
        touch += 1
        if m.records_only(full):
            exempt += 1
            print("  records-only by the exemption:", h, subj[:70])
print("scanned %d; touch pipeline code %d; graded records-only among them %d" % (len(log), touch, exempt))
PYEOF
echo "pipeline_code_census.out rc=$?"
