#!/bin/bash
# attrabbrev Q15 + the Opus seat's variants C4, N7, N10, N11 (PREDICTIONS_q15.txt), re-measured.  Variants IN MEMORY
# (one line of the checker's source replaced, exec'd with __file__ = the real path); no tree file changes.
# usage: ATTR_A=<this dir> SP=<scratch> controls_q15.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir for the injected ledger}
python - "$SEC/tools/pipeline/ledger.json" "$SP/ledger_inwork.json" <<'PYEOF'
import io, json, sys
src, out = sys.argv[1:3]
L = json.load(io.open(src, encoding="utf-8"))
n = 0
for r in L["rows"]:
    if r["id"] == "fbdeclinefive":
        assert r["state"] == "closed" and not r.get("reopened"), (r["state"], r.get("reopened"))
        r["state"] = "in work"
        n += 1
assert n == 1, n
io.open(out, "w", encoding="utf-8").write(json.dumps(L, indent=1, ensure_ascii=False))
PYEOF
variant() {   # variant <out> <which>
	python - "$CHK" "$2" > "$A/$1" 2>&1 <<'PYEOF'
import sys
p, which = sys.argv[1:3]
src = open(p, encoding="utf-8").read()
ret = '    return any(full.startswith(t) for t in SHA.findall(field or ""))'
EDITS = {
    "C4":  ('                if names(row.get("reopened"), full):',
            '                if names(row.get("reopened") or row.get("commits"), full):'),
    "N7":  (ret, '    return any(full.startswith(t) for t in SHA.findall(field or full))'),
    "N11": (ret, '    return any(full.startswith(t) for t in SHA.findall(field or "")[:2])'),
    "N10": (ret, '    return any(full.startswith(t) for t in SHA.findall((field or "")[:40]))'),
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
export GXATTR_DEPTH=60
GXLEDGER="$SP/ledger_inwork.json" python "$CHK" > "$A/post_Q15.out" 2>&1; echo "post_Q15.out rc=$?"
GXLEDGER="$SP/ledger_inwork.json" variant var_C4_Q15.out C4
GXLEDGER="$SP/ledger_inwork.json" variant var_N7_Q15.out N7
GXLEDGER= variant var_N11_d60.out N11
GXLEDGER= variant var_N10_d60.out N10
export GXATTR_DEPTH=800
GXLEDGER= variant var_N11_d800.out N11
GXLEDGER= variant var_N10_d800.out N10
