#!/bin/bash
# attrabbrev Q21b (PREDICTIONS_rp_addendum.txt): a ref named like an abbreviation, in a --shared scratch clone; HEAD and
# R' each run WITHOUT and WITH the tag.  usage: ATTR_A=<this dir> SP=<scratch> controls_rp_q21b.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir}
LED=$SEC/tools/pipeline/ledger.json
CL="$SP/clone21b"
rm -rf "$CL" && git clone -q --shared "$SEC" "$CL" || { echo "CLONE FAILED"; exit 9; }
git -C "$SEC" show HEAD:tools/pipeline/check_commit_attribution.py > "$CL/tools/pipeline/cca_head.py"
cp "$CHK" "$CL/tools/pipeline/cca_rp.py"
python - "$CL/tools/pipeline/cca_rp.py" "$LED" > "$A/rp_Q21b_pick.out" 2>&1 <<'PYEOF'
import importlib.util, io, json, os, re, sys
p, led = sys.argv[1:3]
os.environ["GXLEDGER"] = led
spec = importlib.util.spec_from_file_location("cca_rp", p); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L = json.load(io.open(led, encoding="utf-8"))
rows = {r["id"]: r for r in L["rows"] if len(r["id"]) >= m.MIN_ID}
log = [l.split("\t", 2) for l in m.git("log", "--format=%H\t%h\t%s", "-60").splitlines() if l.count("\t") >= 2]
code = m.git("rev-parse", "fd150657").strip()
assert not m.records_only(code), "the tag target must be a CODE commit"
cands = {1: None, 2: None}
for full, h, subj in log:
    if m.CLOSURE.search(subj) or not m.records_only(full):
        continue
    for rid, row in rows.items():
        pat = (r"[`\"']%s[`\"']" % re.escape(rid)) if rid in m.SUBJECT_STOPWORDS else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(rid))
        if not re.search(pat, subj) or row.get("state") == "closed" or m.lists(row.get("commits"), full):
            continue
        k = 1 if not (row.get("commits") or "").strip() else 2
        if cands[k] is None:
            cands[k] = (full, h, rid)
k = 1 if cands[1] else (2 if cands[2] else 0)
if not k:
    print("NO CANDIDATE"); sys.exit(3)
full, h, rid = cands[k]
print("PICK", k, full, h, rid, "| tag target", code)
PYEOF
pick=$?
cat "$A/rp_Q21b_pick.out"
[ "$pick" = 0 ] || { rm -rf "$CL"; exit 0; }
read -r _ K C H R _ _ _ T < <(grep '^PICK' "$A/rp_Q21b_pick.out")
for phase in notag tag; do
	[ "$phase" = tag ] && { git -C "$CL" tag "$H" "$T" && echo "tagged $H -> $T"; }
	for which in head rp; do
		GXATTR_DEPTH=60 GXLEDGER=$LED python "$CL/tools/pipeline/cca_$which.py" > "$A/rp_Q21b_${which}_$phase.out" 2>&1
		echo "rp_Q21b_${which}_$phase.out rc=$?  line: $(grep -E "^  (HARD|SOFT) +$H +$R " "$A/rp_Q21b_${which}_$phase.out" | cut -c1-110)"
	done
done
rm -rf "$CL"
