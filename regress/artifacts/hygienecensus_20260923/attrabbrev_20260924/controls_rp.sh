#!/bin/bash
# attrabbrev R' controls (PREDICTIONS_rp.txt).  Every case runs twice: HEAD = the committed checker, exec'd in memory from
# the real path; RP = the working checker.  Outputs rp_<case>_{head,rp}.out.  Q21 runs in a --shared scratch clone.
# usage: ATTR_A=<this dir> SP=<scratch> controls_rp.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir}
git -C "$SEC" show HEAD:tools/pipeline/check_commit_attribution.py > "$SP/cca_head_src.py"
LED=$SEC/tools/pipeline/ledger.json
setrow() {   # setrow <name> <row id> <field> <value>
	python - "$LED" "$SP/rp_ledger_$1.json" "$2" "$3" "$4" <<'PYEOF'
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
# both <case> <depth> <ledger-or-empty> [abbrev]: run HEAD and RP on one input
both() {
	local c=$1 d=$2 led=$3 ab=${4:-}
	for which in head rp; do
		if [ -n "$ab" ]; then export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=$ab
		else unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0; fi
		if [ "$which" = head ]; then
			GXATTR_DEPTH=$d GXLEDGER=$led python - "$CHK" "$SP/cca_head_src.py" > "$A/rp_${c}_head.out" 2>&1 <<'PYEOF'
import sys
p, srcf = sys.argv[1:3]
ns = {"__name__": "cca_head", "__file__": p}
exec(compile(open(srcf, encoding="utf-8").read(), p, "exec"), ns)
sys.exit(ns["main"]([]))
PYEOF
		else
			GXATTR_DEPTH=$d GXLEDGER=$led python "$CHK" > "$A/rp_${c}_rp.out" 2>&1
		fi
		echo "rp_${c}_${which}.out rc=$?"
	done
	unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0
}
setrow q3 fbsmlane commits 4264ee2
setrow q4 fbsmlane commits cdbe7d76
setrow q5 fbsmlane commits cdbe7d75735ae3836635d91d70819a09f564fd1a
setrow q7 pcc2widthkills reopened "b78bb0 -- closure superseded (six-character control)"
setrow q11 fbsmlane commits dbe7d757
setrow q12 fbsmlane commits "4264ee2 cdbe7d7"
setrow q15 fbdeclinefive state "in work"
setrow q16 pcc2widthkills reopened "b78bb0f6b2ab7b7bb58323ad2a12a205116100b6 -- the closure its later passes superseded (Q16)"
setrow q17a fbdeclinefive state held
setrow q17b fbdeclinefive state open
setrow q19a fbsmlane commits "outside the repo (ops); compared against (cdbe7d75)"
setrow q19b fbsmlane commits "outside the repo (ops); compared against (4264ee20)"
setrow q19c fbsmlane commits "cdbe7d7 outside the repo (ops)"
both Q0 60 ""
both Q1 60 "" 7
both Q2 130 ""
both Q3 60 "$SP/rp_ledger_q3.json"
both Q4 60 "$SP/rp_ledger_q4.json"
both Q5 60 "$SP/rp_ledger_q5.json"
both Q7 130 "$SP/rp_ledger_q7.json"
both Q10a 60 "" 12
both Q10b 60 "" 40
both Q11 60 "$SP/rp_ledger_q11.json"
both Q12 60 "$SP/rp_ledger_q12.json"
both Q13a7 800 "" 7
both Q13a8 800 ""
both Q15 60 "$SP/rp_ledger_q15.json"
both Q16 130 "$SP/rp_ledger_q16.json"
both Q17a 60 "$SP/rp_ledger_q17a.json"
both Q17b 60 "$SP/rp_ledger_q17b.json"
both Q19a 60 "$SP/rp_ledger_q19a.json"
both Q19b 60 "$SP/rp_ledger_q19b.json"
both Q19c 60 "$SP/rp_ledger_q19c.json"
GIT_DIR=/nonexistent both Q20 60 ""
# ---- Q21: a ref named like an abbreviation, in a --shared scratch clone --------------------------------------------
CL="$SP/clone21"
rm -rf "$CL" && git clone -q --shared "$SEC" "$CL" || { echo "CLONE FAILED"; exit 9; }
cp "$SP/cca_head_src.py" "$CL/tools/pipeline/cca_head.py"
cp "$CHK" "$CL/tools/pipeline/cca_rp.py"
python - "$CL/tools/pipeline/cca_rp.py" "$LED" > "$A/rp_Q21_pick.out" 2>&1 <<'PYEOF'
import importlib.util, io, json, os, sys
p, led = sys.argv[1:3]
os.environ["GXLEDGER"] = led
spec = importlib.util.spec_from_file_location("cca_rp", p); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L = json.load(io.open(led, encoding="utf-8"))
rows = {r["id"]: r for r in L["rows"] if len(r["id"]) >= m.MIN_ID}
import re
log = [l.split("\t", 2) for l in m.git("log", "--format=%H\t%h\t%s", "-60").splitlines() if l.count("\t") >= 2]
code = m.git("rev-parse", "fd150657").strip()
assert not m.records_only(code), "the tag target must be a CODE commit"
for full, h, subj in log:
    for rid, row in rows.items():
        pat = (r"[`\"']%s[`\"']" % re.escape(rid)) if rid in m.SUBJECT_STOPWORDS else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(rid))
        if not re.search(pat, subj) or m.CLOSURE.search(subj):
            continue
        if row.get("state") == "closed" and (row.get("commits") or "").strip() and not m.lists(row.get("commits"), full) and m.records_only(full):
            print("PICK", full, h, rid, "| tag target", code)
            sys.exit(0)
print("NO CANDIDATE")
sys.exit(3)
PYEOF
pick=$?
cat "$A/rp_Q21_pick.out"
if [ "$pick" = 0 ]; then
	read -r _ C H R _ _ _ T < <(grep '^PICK' "$A/rp_Q21_pick.out")
	git -C "$CL" tag "$H" "$T" && echo "tagged $H -> $T"
	for which in head rp; do
		GXATTR_DEPTH=60 GXLEDGER=$LED python "$CL/tools/pipeline/cca_$which.py" > "$A/rp_Q21_$which.out" 2>&1
		echo "rp_Q21_$which.out rc=$?"
	done
fi
rm -rf "$CL"
