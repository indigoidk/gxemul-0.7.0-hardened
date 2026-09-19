#!/bin/bash
#  §F2 measurements (Opus 5).  Writes ONLY under /tmp/gxopus536f2 and _scratchpad/p2_536_537/opus5/out/f2.
#    PIN   O1 closed with NO harness change?  A rowid naming ONE R3 line (the last case), derived
#          from the pristine output, run on: base (want OK), R3 blinded (want FAIL), R3 blinded +
#          R1 tightened (want FAIL -- this is the composite that escaped the R4 pin).
#    TIME  per-arm build and run times over 5 runs, with the host load recorded, for the
#          selfmutant.py margin line.
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
FROZ=$ROOT/_scratchpad/p2_536_537/frozen
OPUS=$ROOT/_scratchpad/p2_536_537/opus5
OUT=$OPUS/out/f2
W=/tmp/gxopus536f2
rm -rf "$W" "$OUT"; mkdir -p "$W" "$OUT"
S=$OUT/SUMMARY.txt
say() { echo "$*" | tee -a "$S"; }

B=$W/base/GXEMUL-SEC
mkdir -p "$B/regress/selfmutants"
cp -a "$SEC/src" "$B/src"
cp "$SEC/config.h" "$B/config.h"
cp "$SEC/regress/selfmutant.py" "$B/regress/"
cp "$SEC/regress/selfmutants/fbpending_bound.old" "$SEC/regress/selfmutants/fbpending_bound.new" "$B/regress/selfmutants/"
cp "$SEC/regress/diff_fbpending_bound.c" "$B/regress/diff_fbpending_bound.c"
cmp -s "$B/regress/diff_fbpending_bound.c" "$FROZ/diff_fbpending_bound.c" && say "harness unchanged since pass 2 (== frozen)"
say "selfmutant.py vs frozen-era HEAD: $(git -C "$SEC" show HEAD:regress/selfmutant.py 2>/dev/null | diff - "$B/regress/selfmutant.py" | grep -c '^[<>]') changed line(s), all comments? $(git -C "$SEC" show HEAD:regress/selfmutant.py 2>/dev/null | diff - "$B/regress/selfmutant.py" | grep '^[<>]' | grep -vc '^[<>] *#')= non-comment"
python3 "$OPUS/scripts/mkvariants.py" "$B/regress/diff_fbpending_bound.c" "$W/variants" > "$OUT/mkvariants.txt" 2>&1; tail -1 "$OUT/mkvariants.txt" | tee -a "$S"

OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
XF_REL="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"

mkvariant() {
    local d=$W/v_$1/GXEMUL-SEC
    rm -rf "$W/v_$1"; mkdir -p "$d/regress/selfmutants"
    ln -s "$B/src" "$d/src"; cp "$B/config.h" "$d/config.h"
    cp "$B/regress/selfmutant.py" "$d/regress/"
    cp "$B/regress/selfmutants/fbpending_bound.old" "$B/regress/selfmutants/fbpending_bound.new" "$d/regress/selfmutants/"
    cp "$2" "$d/regress/diff_fbpending_bound.c"
    echo "$d"
}
lane() {  # tag sec-root xflags rowid
    local tag=$1 sc=$2 xf=$3 rid=$4 rc
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$xf" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "$rid" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    say "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1)"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | tee -a "$S"
}

say "=== TIME: 5 runs of both arms (armdump = the helper's own functions), load recorded ==="
say "nproc=$(nproc)  loadavg before: $(cat /proc/loadavg)"
for i in 1 2 3 4 5; do
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$XF_REL" python3 "$OPUS/scripts/armdump.py" "$B" "$W/ad$i" "$W/armtree" ) > "$OUT/armdump_$i.txt" 2>&1
    grep -E '^(pristine|mutant) ' "$OUT/armdump_$i.txt" | sed -E 's/ sha=.*//; s/^/  run '"$i"': /' | tee -a "$S"
done
say "loadavg after: $(cat /proc/loadavg)"
python3 - "$OUT" <<'PYEOF' | tee -a "$S"
import re, sys, glob
b, r = [], []
for f in sorted(glob.glob(sys.argv[1] + "/armdump_*.txt")):
    for l in open(f):
        m = re.match(r"^(pristine|mutant)\s+build ([\d.]+)s run ([\d.]+)s", l)
        if m:
            b.append(float(m.group(2))); r.append(float(m.group(3)))
print("  per-arm build: n=%d min %.2f max %.2f   per-arm run: n=%d min %.2f max %.2f" % (len(b), min(b), max(b), len(r), min(r), max(r)))
print("  margins at the max: BUILD 120/%.2f = %.1fx   RUN 60/%.2f = %.1fx" % (max(b), 120 / max(b), max(r), 60 / max(r)))
PYEOF

say "=== PIN: derive a rowid naming ONE R3 line, from the pristine arm's own output ==="
P=$W/ad1/arm_pristine.stdout
RID=$(python3 - "$P" <<'PYEOF'
import re, sys
out = open(sys.argv[1]).read()
lines = [l for l in out.splitlines() if "R3 the reset still owes one interrupt" in l and "slowest legal" in l]
assert len(lines) == 1, lines
l = lines[0]
i = l.index("slowest legal"); j = l.index("lowest value") + len("lowest")
rid = l[i:j]
n = sum(1 for x in out.splitlines() if rid in x and (x.strip().startswith("ok") or x.strip().startswith("FAIL")))
assert n == 1, n
print(rid)
PYEOF
)
say "  rowid = [$RID]  (length ${#RID}; it spans the %-28s padding, so it is padding-dependent)"
say "  lines naming it in the pristine output: $(grep -cF "$RID" "$P")"
lane PIN_base "$B" "$XF_REL" "$RID"
lane PIN_n1_r3blind "$(mkvariant n1 "$W/variants/harness.n1_r3blind.c")" "$XF_REL" "$RID"
lane PIN_g_r3blind_r1tight "$(mkvariant g "$W/variants/harness.g_r3blind_r1tight.c")" "$XF_REL" "$RID"
say "=== reference: the shipped R4 pin on the same composite ==="
lane R4_g_r3blind_r1tight "$W/v_g/GXEMUL-SEC" "$XF_REL" "R4 every case bounded"
say "=== compiler identity (F12) ==="
say "  cc  -> $(readlink -f "$(command -v cc)")   gcc -> $(readlink -f "$(command -v gcc)")"
say "  cc --version: $(cc --version | head -1)"
say "F2_DONE"
