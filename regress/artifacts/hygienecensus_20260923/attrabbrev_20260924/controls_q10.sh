#!/bin/bash
# attrabbrev Q10-Q14 (PREDICTIONS_q10.txt): the constructions the nine-seat panel named, measured.  Variants are applied
# IN MEMORY (one line of the checker's source replaced, exec'd with __file__ = the real path); no tree file changes.
# usage: ATTR_A=<this dir> SP=<scratch> controls_q10.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir for the injected ledgers}
inj() {   # inj <name> <fbsmlane.commits value>
	python - "$SEC/tools/pipeline/ledger.json" "$SP/ledger_$1.json" "$2" <<'PYEOF'
import io, json, sys
src, out, val = sys.argv[1:4]
L = json.load(io.open(src, encoding="utf-8"))
n = 0
for r in L["rows"]:
    if r["id"] == "fbsmlane":
        r["commits"] = val
        n += 1
assert n == 1, n
io.open(out, "w", encoding="utf-8").write(json.dumps(L, indent=1, ensure_ascii=False))
PYEOF
}
# variant <out> <which>: the checker with ONE line replaced, exec'd in memory
variant() {
	python - "$CHK" "$2" > "$A/$1" 2>&1 <<'PYEOF'
import sys
p, which = sys.argv[1:3]
src = open(p, encoding="utf-8").read()
ret = '    return any(full.startswith(t) for t in SHA.findall(field or ""))'
EDITS = {
    "width":    ('            elif names(row.get("commits"), full):',
                 '            elif len(h) <= 8 and names(row.get("commits"), full):'),
    "substr":   (ret, '    return any(t in full for t in SHA.findall(field or ""))'),
    "first":    (ret, '    return any(full.startswith(t) for t in SHA.findall(field or "")[:1])'),
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
a7() { GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=$1; export GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0; }
na() { unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0; }
inj sub dbe7d757
inj two "4264ee2 cdbe7d7"
export GXATTR_DEPTH=60 GXLEDGER=
a7 12; python "$CHK" > "$A/post_Q10a.out" 2>&1; echo "post_Q10a.out rc=$?"
        variant mut_M10.out width
a7 40; python "$CHK" > "$A/post_Q10b.out" 2>&1; echo "post_Q10b.out rc=$?"
na
GXLEDGER="$SP/ledger_sub.json" python "$CHK" > "$A/post_Q11.out" 2>&1; echo "post_Q11.out rc=$?"
GXLEDGER="$SP/ledger_sub.json" variant mut_M11.out substr
variant mut_M12.out first
GXLEDGER="$SP/ledger_two.json" python "$CHK" > "$A/post_Q12.out" 2>&1; echo "post_Q12.out rc=$?"
GXLEDGER="$SP/ledger_two.json" variant mut_M12b.out first
variant var_Q14.out pipecode
export GXATTR_DEPTH=800
a7 7; python "$CHK" > "$A/post_Q13_a7.out" 2>&1; echo "post_Q13_a7.out rc=$?"
na;   python "$CHK" > "$A/post_Q13_a8.out" 2>&1; echo "post_Q13_a8.out rc=$?"
