#!/bin/bash
#  Forced-site differential: FORCE_SITE=k makes site k's condition true in BOTH arms (the same
#  mechanical instrumentation applied to ORIG and to each transform), so every one of the 95
#  FAIL arms is executed once and the two arms' full output is compared.
set -u
W=/tmp/opus551p1
d=$W/dev/pristine/regress
out=$W/force; rm -rf $out; mkdir -p $out
for k in $(seq 0 95); do
    for h in ORIGF AF AhardF TdropF TdoubleF; do
        FORCE_SITE=$k timeout 120 $d/$h.O2 > $out/$h.$k.log 2>&1; echo $? > $out/$h.$k.rc
    done
done
python3 - "$out" <<'PYEOF'
import io, re, sys
out = sys.argv[1]
def rd(h, k):
    t = io.open("%s/%s.%d.log" % (out, h, k), encoding="utf-8", errors="replace").read()
    rc = io.open("%s/%s.%d.rc" % (out, h, k)).read().strip()
    return "\n".join(l for l in t.split("\n") if "SELFCHECK" not in l), rc, t
res = {h: [] for h in ("AF", "AhardF", "TdropF", "TdoubleF")}
live = 0
nf_by_k = {}
for k in range(0, 96):
    o, orc, raw = rd("ORIGF", k)
    m = re.search(r"^(\d+) rows, (\d+) failures", raw, re.M)
    nf_by_k[k] = int(m.group(2)) if m else None
    if k > 0 and nf_by_k[k] and "WDC_IDENTIFY_FAIL" in raw:
        live += 1
    for h in res:
        t, trc, _ = rd(h, k)
        if t != o or trc != orc:
            res[h].append(k)
print("forced sites that produced a FAIL verdict in ORIG (liveness of the forcing): %d of 95" % live)
print("k=0 (nothing forced) failures:", nf_by_k[0])
print("per-k ORIG failure counts (k>0), distinct values:", sorted(set(v for k, v in nf_by_k.items() if k)))
for h, bad in res.items():
    print("%-9s differs from ORIG at %d of 96 runs: %s" % (h, len(bad), bad))
PYEOF
echo FORCE_DONE
