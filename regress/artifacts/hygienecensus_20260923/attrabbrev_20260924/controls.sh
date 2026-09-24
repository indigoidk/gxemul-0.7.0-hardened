#!/bin/bash
# attrabbrev controls (PREDICTIONS.txt beside this file).  usage: controls.sh pre|post
# Runs the check in THIS tree (it resolves the repo and ledger from its own location); writes <mode>_<case>.out here.
set -u
MODE=$1
# ATTR_A: this artifact dir -- REQUIRED when running a frozen copy from elsewhere, since the repo is found from it
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir for the injected ledgers}
run() {   # run <case> <abbrev7:0|1> <depth> [ledger]
	local c=$1 a7=$2 d=$3 led=${4:-}
	if [ "$a7" = 1 ]; then
		GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=7 GXATTR_DEPTH=$d GXLEDGER=$led \
			python "$CHK" > "$A/${MODE}_$c.out" 2>&1
	else
		GXATTR_DEPTH=$d GXLEDGER=$led python "$CHK" > "$A/${MODE}_$c.out" 2>&1
	fi
	echo "$c rc=$? $(grep -cE '^  HARD ' "$A/${MODE}_$c.out") HARD  $(tail -1 "$A/${MODE}_$c.out")"
}
if [ "$MODE" = pre ]; then
	run P0 0 60; run P1 1 60; run P2 0 130; run P3 1 130
	exit 0
fi
# injected ledgers: fbsmlane.commits replaced, everything else the working ledger
inj() {   # inj <name> <commits value>
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
inj other 4264ee2
inj near cdbe7d76
inj full cdbe7d75735ae3836635d91d70819a09f564fd1a
git -C "$SEC" show :tools/pipeline/ledger.json > "$SP/ledger_index.json"
run Q0 0 60; run Q1 1 60; run Q2 0 130
run Q3 0 60 "$SP/ledger_other.json"; run Q4 0 60 "$SP/ledger_near.json"; run Q5 0 60 "$SP/ledger_full.json"
run Q6 0 60 "$SP/ledger_index.json"
