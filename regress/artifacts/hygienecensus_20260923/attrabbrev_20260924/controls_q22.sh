#!/bin/bash
# attrabbrev Q22 (PREDICTIONS_q22.txt): a 6-character whole token inside a non-repo note, run through the pre-R checker
# (as of 4264ee20), HEAD (R, 3e33201d) and R' (working).  pre-R and HEAD are exec'd in memory from the real path.
# usage: ATTR_A=<this dir> SP=<scratch> controls_q22.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir}
git -C "$SEC" show 4264ee20:tools/pipeline/check_commit_attribution.py > "$SP/cca_preR_src.py"
git -C "$SEC" show HEAD:tools/pipeline/check_commit_attribution.py > "$SP/cca_head_src.py"
python - "$SEC/tools/pipeline/ledger.json" "$SP/q22_ledger.json" <<'PYEOF'
import io, json, sys
src, out = sys.argv[1:3]
L = json.load(io.open(src, encoding="utf-8"))
n = 0
for r in L["rows"]:
    if r["id"] == "fbsmlane":
        r["commits"] = "cdbe7d outside the repo (ops)"
        n += 1
assert n == 1, n
io.open(out, "w", encoding="utf-8").write(json.dumps(L, indent=1, ensure_ascii=False))
PYEOF
runmem() {   # runmem <out> <srcfile>
	python - "$CHK" "$2" > "$A/$1" 2>&1 <<'PYEOF'
import sys
p, srcf = sys.argv[1:3]
ns = {"__name__": "cca_mem", "__file__": p}
exec(compile(open(srcf, encoding="utf-8").read(), p, "exec"), ns)
sys.exit(ns["main"]([]))
PYEOF
	echo "$1 rc=$?"
}
export GXATTR_DEPTH=60 GXLEDGER="$SP/q22_ledger.json"
for ab in 6 def; do
	if [ "$ab" = 6 ]; then export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=6; sfx=Q22
	else unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0; sfx=Q22b; fi
	[ "$ab" = 6 ] && echo "git prints: $(git -C "$SEC" log -1 --format=%h cdbe7d75735ae3836635d91d70819a09f564fd1a)"
	runmem "q22_${sfx}_preR.out" "$SP/cca_preR_src.py"
	runmem "q22_${sfx}_head.out" "$SP/cca_head_src.py"
	python "$CHK" > "$A/q22_${sfx}_rp.out" 2>&1; echo "q22_${sfx}_rp.out rc=$?"
done
