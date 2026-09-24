#!/bin/bash
# attrabbrev Q22c-Q25 (PREDICTIONS_q23.txt).  Variants and the git shim run IN MEMORY (the checker's source exec'd with
# __file__ = the real path); no tree file changes.  usage: ATTR_A=<this dir> SP=<scratch> controls_q23.sh
set -u
A=${ATTR_A:-$(cd "$(dirname "$0")" && pwd)}
SEC=$(cd "$A/../../../.." && pwd)
CHK=$SEC/tools/pipeline/check_commit_attribution.py
[ -f "$CHK" ] || { echo "NO CHECK AT $CHK -- wrong ATTR_A?"; exit 9; }
SP=${SP:?set SP to a scratch dir}
LED=$SEC/tools/pipeline/ledger.json
setrow() {   # setrow <name> <row id> <field> <value>
	python - "$LED" "$SP/q23_ledger_$1.json" "$2" "$3" "$4" <<'PYEOF'
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
# run <out> <variant|none> <shim:0|1>: the working checker, optionally with one line replaced and/or git log shimmed
run() {
	python - "$CHK" "$2" "$3" > "$A/$1" 2>&1 <<'PYEOF'
import subprocess, sys
p, which, shim = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
src = open(p, encoding="utf-8").read()
EDITS = {
    "token6":  ('TOKEN = re.compile(r"[0-9a-f]{7,40}")', 'TOKEN = re.compile(r"[0-9a-f]{6,40}")'),
    "stdout":  ("    if r.returncode != 0:", "    if r.returncode != 0 and not r.stdout:"),
    "depth0":  ('DEPTH = int(os.environ.get("GXATTR_DEPTH", "60"))', 'DEPTH = int(os.environ.get("GXATTR_DEPTH", "0"))'),
    "depth130": ('DEPTH = int(os.environ.get("GXATTR_DEPTH", "60"))', 'DEPTH = int(os.environ.get("GXATTR_DEPTH", "130"))'),
    "e1":      ("              % (len(hard), len(soft), len(ph)))\n        return 1",
                "              % (len(hard), len(soft), len(ph)))\n        return 0"),
}
if which != "none":
    old, new = EDITS[which]
    assert src.count(old) == 1, "variant site not found: " + which
    src = src.replace(old, new)
ns = {"__name__": "cca_q23", "__file__": p}
exec(compile(src, p, "exec"), ns)
if shim:
    real = subprocess.run
    class Shim:
        def __getattr__(self, k):
            return getattr(subprocess, k)
        @staticmethod
        def run(cmd, *a, **k):
            r = real(cmd, *a, **k)
            if "log" in cmd:
                return subprocess.CompletedProcess(r.args, 1, r.stdout, "simulated: nonzero exit after a complete log")
            return r
    ns["subprocess"] = Shim()
sys.exit(ns["main"]([]))
PYEOF
	echo "$1 rc=$?" | tee -a "$A/q23_rc_table.out"
}
: > "$A/q23_rc_table.out"
setrow six fbsmlane commits "cdbe7d outside the repo (ops)"
setrow q19a fbsmlane commits "outside the repo (ops); compared against (cdbe7d75)"
setrow q15 fbdeclinefive state "in work"
setrow q3 fbsmlane commits 4264ee2
# Q22c: the TOKEN floor
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=6
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_six.json" run q23_Q22c_token6.out token6 0
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_six.json" run q23_Q22c_rp.out none 0
unset GIT_CONFIG_COUNT GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0
# Q23: git log exits nonzero with its real stdout
GXATTR_DEPTH=60 GXLEDGER= run q23_Q23_rp.out none 1
GXATTR_DEPTH=60 GXLEDGER= run q23_Q23_stdout.out stdout 1
# Q24: exactly as section L runs it -- no environment
env -u GXATTR_DEPTH -u GXLEDGER python "$CHK" > "$A/q23_Q24_rp_noenv.out" 2>&1; echo "q23_Q24_rp_noenv.out rc=$?" | tee -a "$A/q23_rc_table.out"
( unset GXATTR_DEPTH GXLEDGER; run q23_Q24_depth0.out depth0 0 )
( unset GXATTR_DEPTH GXLEDGER; run q23_Q24_depth130.out depth130 0 )
# Q25: exit status
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_q19a.json" run q23_Q25_q19a_rp.out none 0
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_q15.json"  run q23_Q25_q15_rp.out none 0
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_q3.json"   run q23_Q25_q3_rp.out none 0
GXATTR_DEPTH=60 GXLEDGER=                          run q23_Q25_q0_rp.out none 0
GXATTR_DEPTH=60 GXLEDGER="$SP/q23_ledger_q19a.json" run q23_Q25_q19a_e1.out e1 0
