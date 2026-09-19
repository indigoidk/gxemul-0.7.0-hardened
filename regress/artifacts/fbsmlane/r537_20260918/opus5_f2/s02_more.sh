#!/bin/bash
#  #537 pass-2 measurements, part 2.  Reuses /tmp/gxopus536p2/base from s01 (verified below).
#  Writes ONLY under /tmp/gxopus536p2 and _scratchpad/p2_536_537/opus5/out.
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
FROZ=$ROOT/_scratchpad/p2_536_537/frozen
OPUS=$ROOT/_scratchpad/p2_536_537/opus5
OUT=$OPUS/out/more
W=/tmp/gxopus536p2
B=$W/base/GXEMUL-SEC
rm -rf "$OUT"; mkdir -p "$OUT"
S=$OUT/SUMMARY.txt
say() { echo "$*" | tee -a "$S"; }
cmp -s "$B/regress/diff_fbpending_bound.c" "$FROZ/diff_fbpending_bound.c" && say "base harness == frozen" || { say "ABORT: base copy missing or changed"; exit 3; }
cmp -s "$B/src/devices/dev_footbridge.c" "$SEC/src/devices/dev_footbridge.c" && say "base dev_footbridge.c == SEC"

rm -rf "$W/variants"
python3 "$OPUS/scripts/mkvariants.py" "$B/regress/diff_fbpending_bound.c" "$W/variants" 2>&1 | tee -a "$S"

OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
XF_REL="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"

mkvariant() {
    local d=$W/v2_$1/GXEMUL-SEC
    rm -rf "$W/v2_$1"
    mkdir -p "$d/regress/selfmutants"
    ln -s "$B/src" "$d/src"
    cp "$B/config.h" "$d/config.h"
    cp "$B/regress/selfmutant.py" "$d/regress/"
    cp "$B/regress/selfmutants/fbpending_bound.old" "$B/regress/selfmutants/fbpending_bound.new" "$d/regress/selfmutants/"
    cp "$2" "$d/regress/diff_fbpending_bound.c"
    echo "$d"
}
lane() {
    local tag=$1 sc=$2 xf=$3 rc t0 t1
    t0=$(date +%s.%N)
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$xf" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "R4 every case bounded" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    t1=$(date +%s.%N)
    say "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1) wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')s  gate-row=$(grep -c 'SELFMUTANT_OK' "$OUT/$tag.txt")"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | tee -a "$S"
}

say "=== N1 (re-run with a valid variant): R3 blinded ==="
lane N1_r3blind "$(mkvariant n1 "$W/variants/harness.n1_r3blind.c")" "$XF_REL"
say "=== G: R3 blinded AND R1 tightened to trough >= 1 ==="
lane G_r3blind_r1tight "$(mkvariant g "$W/variants/harness.g_r3blind_r1tight.c")" "$XF_REL"
say "=== G0: R1 tightened alone (control) ==="
lane G0_r1tight "$(mkvariant g0 "$W/variants/harness.g0_r1tight.c")" "$XF_REL"

say "=== P2: both arms, full stdout, exactly as the helper builds and runs them ==="
( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$XF_REL" python3 "$OPUS/scripts/armdump.py" "$B" "$OUT/armdump" "$W/armtree" ) 2>&1 | tee -a "$S"

say "=== P1: which dev_footbridge.c gcc opened (-H include trace, the lane's own flags, in the mirror) ==="
#  armdump leaves the mirror at $W/armtree with the MUTANT text written last.
( cd "$W/armtree/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I../src -I../src/include \
    -I../src/include/thirdparty -ffunction-sections -fdata-sections -std=gnu99 -I../src/include \
    -I../src/include/thirdparty -I../src/devices -E -H diff_fbpending_bound.c -o /dev/null ) 2> "$OUT/P1_H.txt"
say "  first-level includes (depth 1):"; grep -E '^\. ' "$OUT/P1_H.txt" | sed 's/^/    /' | tee -a "$S"
say "  config.h reached as:"; grep -E 'config\.h' "$OUT/P1_H.txt" | head -2 | sed 's/^/    /' | tee -a "$S"
say "  mirror subject: $(ls -l "$W/armtree/src/devices/dev_footbridge.c" | cut -c1-10) (a real file) ; mirror src/include: $(ls -ld "$W/armtree/src/include" | cut -c1-10)"
say "  the mirror copy carries the MUTANT line? $(grep -c 'pending_timer_interrupts\[nr\] = 0;' "$W/armtree/src/devices/dev_footbridge.c") ; SEC copy? $(grep -c 'pending_timer_interrupts\[nr\] = 0;' "$SEC/src/devices/dev_footbridge.c")"

say "=== P1: standalone -- does gcc search the directory of a SYMLINK's TARGET for a quote include? ==="
T=$W/symtest; rm -rf "$T"; mkdir -p "$T/A" "$T/B" "$T/C"
printf '#include "x.h"\nint v = X;\n' > "$T/B/h.c"
printf '#define X 222  /* B: the symlink TARGET directory */\n' > "$T/B/x.h"
printf '#define X 333  /* C: the -I directory */\n' > "$T/C/x.h"
ln -s "$T/B/h.c" "$T/A/h.c"
( cd "$T/A" && gcc -I../C -E -P h.c ) 2>&1 | grep 'int v' | sed 's/^/    one-level symlink, -I..\/C : /' | tee -a "$S"
ln -s "$T/A/h.c" "$T/A/h2.c"
( cd "$T/A" && gcc -I../C -E -P h2.c ) 2>&1 | grep 'int v' | sed 's/^/    two-level symlink chain   : /' | tee -a "$S"
( cd "$T/B" && gcc -I../C -E -P h.c ) 2>&1 | grep 'int v' | sed 's/^/    control, compiled in B    : /' | tee -a "$S"

say "=== P3: the lane's compile vs gate 2's #442 compile, same pristine source ==="
#  Gate-2 style, exactly gate_offline.sh:1279 but pointed at the base copy.
( cd "$B/regress" && gcc -O2 -std=gnu99 -I"$B/src/include" -I"$B/src/include/thirdparty" -I"$B/src/devices" \
    -o "$W/fb_gate2" "$B/regress/diff_fbpending_bound.c" $OBJS -lm -L/usr/X11R6/lib -lX11 ) > "$OUT/P3_gate2_build.txt" 2>&1
say "  gate-2 style build rc=$?"
#  Lane style, in a PRISTINE mirror (armtree currently holds the mutant; rewrite it pristine first).
cp "$B/src/devices/dev_footbridge.c" "$W/armtree/src/devices/dev_footbridge.c.tmp" && mv -f "$W/armtree/src/devices/dev_footbridge.c.tmp" "$W/armtree/src/devices/dev_footbridge.c"
cmp -s "$W/armtree/src/devices/dev_footbridge.c" "$B/src/devices/dev_footbridge.c" && say "  mirror restored to pristine (cmp clean vs base)"
( cd "$W/armtree/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I../src -I../src/include -I../src/include/thirdparty \
    -ffunction-sections -fdata-sections -Wl,--gc-sections $XF_REL -o "$W/fb_lane" diff_fbpending_bound.c -lm ) > "$OUT/P3_lane_build.txt" 2>&1
say "  lane style build rc=$?"
#  Preprocessed text, line markers stripped (-P), both from their own cwd/-I sets.
( cd "$B/regress" && gcc -O2 -std=gnu99 -I"$B/src/include" -I"$B/src/include/thirdparty" -I"$B/src/devices" -E -P "$B/regress/diff_fbpending_bound.c" ) > "$OUT/P3_gate2.i" 2>/dev/null
( cd "$W/armtree/regress" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -I../src -I../src/include -I../src/include/thirdparty \
    -ffunction-sections -fdata-sections -std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices -E -P diff_fbpending_bound.c ) > "$OUT/P3_lane.i" 2>/dev/null
say "  preprocessed: gate2 $(wc -l < "$OUT/P3_gate2.i") lines, lane $(wc -l < "$OUT/P3_lane.i") lines; diff lines: $(diff "$OUT/P3_gate2.i" "$OUT/P3_lane.i" | grep -c '^[<>]')"
diff "$OUT/P3_gate2.i" "$OUT/P3_lane.i" | head -20 | sed 's/^/    /' | tee -a "$S"
#  Predefined macros that differ between the two flag sets
( cd "$B/regress" && gcc -O2 -std=gnu99 -dM -E - < /dev/null ) | sort > "$OUT/P3_gate2.dM"
gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -std=gnu99 -dM -E - < /dev/null | sort > "$OUT/P3_lane.dM"
say "  predefined-macro differences (lane vs gate2): $(diff "$OUT/P3_gate2.dM" "$OUT/P3_lane.dM" | grep -c '^[<>]')"
diff "$OUT/P3_gate2.dM" "$OUT/P3_lane.dM" | sed 's/^/    /' | tee -a "$S"
#  Behaviour: both binaries, no argument (the lane's run) and the deep argument (gate 2's run).
"$W/fb_gate2" > "$OUT/P3_gate2_shallow.txt" 2>&1; r1=$?
"$W/fb_lane"  > "$OUT/P3_lane_shallow.txt"  2>&1; r2=$?
say "  shallow: gate2 rc=$r1 lane rc=$r2 ; stdout identical? $(cmp -s "$OUT/P3_gate2_shallow.txt" "$OUT/P3_lane_shallow.txt" && echo YES || echo NO)"
t0=$(date +%s.%N); "$W/fb_gate2" 2147487744 > "$OUT/P3_gate2_deep.txt" 2>&1; r1=$?; t1=$(date +%s.%N)
"$W/fb_lane"  2147487744 > "$OUT/P3_lane_deep.txt"  2>&1; r2=$?; t2=$(date +%s.%N)
say "  deep:    gate2 rc=$r1 ($(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')s) lane rc=$r2 ($(awk -v a="$t1" -v b="$t2" 'BEGIN{printf "%.1f", b-a}')s) ; stdout identical? $(cmp -s "$OUT/P3_gate2_deep.txt" "$OUT/P3_lane_deep.txt" && echo YES || echo NO)"
say "  binary sizes: gate2 $(stat -c %s "$W/fb_gate2") lane $(stat -c %s "$W/fb_lane")"

say "=== Q2(b): gate 2's #442 verdict row, ^FBBOUND_PASS\$ vs FBBOUND_, on a PASS log and on a FAIL log ==="
#  A FAIL log: the gate-2-style build of the MUTANT subject (reset-to-0), run deep, as the main lane runs.
MT=$W/mutsubject; rm -rf "$MT"; mkdir -p "$MT"
python3 - "$B/src/devices/dev_footbridge.c" "$B/regress/selfmutants/fbpending_bound.old" "$B/regress/selfmutants/fbpending_bound.new" "$MT/dev_footbridge.c" <<'PYEOF'
import sys
body = open(sys.argv[1], encoding="utf-8").read()
old = open(sys.argv[2], encoding="utf-8").read(); new = open(sys.argv[3], encoding="utf-8").read()
assert body.count(old) == 1
open(sys.argv[4], "w", encoding="utf-8", newline="\n").write(body.replace(old, new, 1))
PYEOF
( cd "$B/regress" && gcc -O2 -std=gnu99 -I"$B/src/include" -I"$B/src/include/thirdparty" -I"$MT" -I"$B/src/devices" \
    -o "$W/fb_gate2_mut" "$B/regress/diff_fbpending_bound.c" $OBJS -lm -L/usr/X11R6/lib -lX11 ) > "$OUT/Qb_mut_build.txt" 2>&1
say "  mutant-subject gate-2 build rc=$?"
"$W/fb_gate2_mut" 2147487744 > "$OUT/Qb_fail_deep.log" 2>&1; say "  mutant deep run rc=$?"
for L in "$OUT/P3_gate2_deep.txt" "$OUT/Qb_fail_deep.log"; do
    say "  $(basename "$L"): '^FBBOUND_PASS\$'=$(grep -c '^FBBOUND_PASS$' "$L")  'FBBOUND_'=$(grep -c 'FBBOUND_' "$L")  R2-ran=$(grep -c 'R2 no signed overflow.*direct ticks' "$L")  rows=$(grep -cE '^  (ok|FAIL) ' "$L")  FAIL-rows=$(grep -cE '^  FAIL ' "$L")"
done

say "=== Q2(a) on gate 2's MAIN lane: the unconditional-PASS harness, pristine subject, deep ==="
( cd "$B/regress" && gcc -O2 -std=gnu99 -I"$B/src/include" -I"$B/src/include/thirdparty" -I"$B/src/devices" \
    -o "$W/fb_gate2_a" "$W/variants/harness.a_uncond_pass.c" $OBJS -lm -L/usr/X11R6/lib -lX11 ) > "$OUT/Qa_main_build.txt" 2>&1
"$W/fb_gate2_a" 2147487744 > "$OUT/Qa_main_deep.log" 2>&1
say "  pristine subject: '^FBBOUND_PASS\$'=$(grep -c '^FBBOUND_PASS$' "$OUT/Qa_main_deep.log")  R2-ran=$(grep -c 'R2 no signed overflow.*direct ticks' "$OUT/Qa_main_deep.log")  rows=$(grep -cE '^  (ok|FAIL) ' "$OUT/Qa_main_deep.log")"
( cd "$B/regress" && gcc -O2 -std=gnu99 -I"$B/src/include" -I"$B/src/include/thirdparty" -I"$MT" -I"$B/src/devices" \
    -o "$W/fb_gate2_a_mut" "$W/variants/harness.a_uncond_pass.c" $OBJS -lm -L/usr/X11R6/lib -lX11 ) > "$OUT/Qa_main_mut_build.txt" 2>&1
"$W/fb_gate2_a_mut" 2147487744 > "$OUT/Qa_main_mut_deep.log" 2>&1
say "  MUTANT subject:   '^FBBOUND_PASS\$'=$(grep -c '^FBBOUND_PASS$' "$OUT/Qa_main_mut_deep.log")  R2-ran=$(grep -c 'R2 no signed overflow.*direct ticks' "$OUT/Qa_main_mut_deep.log")  rows=$(grep -cE '^  (ok|FAIL) ' "$OUT/Qa_main_mut_deep.log")  FAIL-rows=$(grep -cE '^  FAIL ' "$OUT/Qa_main_mut_deep.log")"
say "MORE_DONE"
