#!/bin/bash
#  §F2: the coordinator's NEW pin, measured with the EXACT string, extracted from the current
#  gate_offline.sh (never transcribed).  Writes ONLY under /tmp/gxopus536f2 and opus5/out/f2pin.
#    base (want OK)  |  R3 blinded (want FAIL)  |  R3 blinded + R1 tightened (want FAIL)
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
OPUS=$ROOT/_scratchpad/p2_536_537/opus5
OUT=$OPUS/out/f2pin
W=/tmp/gxopus536f2
B=$W/base/GXEMUL-SEC
rm -rf "$OUT"; mkdir -p "$OUT"
S=$OUT/SUMMARY.txt
say() { echo "$*" | tee -a "$S"; }
[ -f "$B/regress/diff_fbpending_bound.c" ] || { say "ABORT: base copy missing"; exit 3; }
cmp -s "$B/regress/diff_fbpending_bound.c" "$SEC/regress/diff_fbpending_bound.c" && say "base harness == working-tree harness"
cmp -s "$B/regress/selfmutant.py" "$SEC/regress/selfmutant.py" || { cp "$SEC/regress/selfmutant.py" "$B/regress/selfmutant.py"; say "helper refreshed from the working tree (comment-only change)"; }

#  The rowid, taken from the gate's own call line: the 4th double-quoted argument.
RID=$(python3 - "$SEC/regress/gate_offline.sh" <<'PYEOF'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
m = [l for l in src.splitlines() if l.startswith("selfmutant_one diff_fbpending_bound.c ")]
assert len(m) == 1, len(m)
q = re.findall(r'"([^"]*)"', m[0])
print(q[0])
PYEOF
)
say "rowid from gate_offline.sh = [$RID] (length ${#RID})"

OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
XF_REL="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"
lane() {  # tag sec-root rowid
    local tag=$1 sc=$2 rid=$3 rc
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$XF_REL" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "$rid" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    say "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1)  gate-row=$(grep -c SELFMUTANT_OK "$OUT/$tag.txt")"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | cut -c1-170 | tee -a "$S"
}
for v in v_n1 v_g; do cp "$B/regress/selfmutant.py" "$W/$v/GXEMUL-SEC/regress/selfmutant.py"; done
lane NEWPIN_base "$B" "$RID"
lane NEWPIN_n1_r3blind "$W/v_n1/GXEMUL-SEC" "$RID"
lane NEWPIN_g_r3blind_r1tight "$W/v_g/GXEMUL-SEC" "$RID"
#  Padding sensitivity, stated as a measurement: the same rowid with ONE space fewer.
lane NEWPIN_base_onespace_short "$B" "$(printf '%s' "$RID" | sed 's/interrupt        cats/interrupt       cats/')"
say "F2PIN_DONE"
