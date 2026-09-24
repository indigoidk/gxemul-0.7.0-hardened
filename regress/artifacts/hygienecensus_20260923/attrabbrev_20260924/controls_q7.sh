#!/bin/bash
# attrabbrev Q7-Q9 (PREDICTIONS_q7.txt): the six-character reopened control, and the {6,40} extractor mutant run
# IN MEMORY against it and against Q0's input.  usage: ATTR_A=<this dir> SP=<scratch> controls_q7.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir for the injected ledger}
python - "$SEC/tools/pipeline/ledger.json" "$SP/ledger_six.json" <<'PYEOF'
import io, json, sys
src, out = sys.argv[1:3]
L = json.load(io.open(src, encoding="utf-8"))
n = 0
for r in L["rows"]:
    if r["id"] == "pcc2widthkills":
        r["reopened"] = "b78bb0 -- closure superseded (six-character control)"
        n += 1
assert n == 1, n
io.open(out, "w", encoding="utf-8").write(json.dumps(L, indent=1, ensure_ascii=False))
PYEOF
# mutant <out>: the checker with the SHA extractor's {7,40} -> {6,40}, exec'd in memory from its real path
mutant() {
	python - "$CHK" > "$A/$1" 2>&1 <<'PYEOF'
import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
old = 'SHA = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")'
assert src.count(old) == 1, "mutant site not found"
src = src.replace(old, old.replace("{7,40}", "{6,40}"))
ns = {"__name__": "attrabbrev_mutant", "__file__": p}
exec(compile(src, p, "exec"), ns)
sys.exit(ns["main"]([]))
PYEOF
	echo "$1 rc=$?"
}
GXATTR_DEPTH=130 GXLEDGER="$SP/ledger_six.json" python "$CHK" > "$A/post_Q7.out" 2>&1; echo "post_Q7.out rc=$?"
GXATTR_DEPTH=130 GXLEDGER="$SP/ledger_six.json" mutant mut_Q8.out
GXATTR_DEPTH=60 GXLEDGER= mutant mut_Q9.out
