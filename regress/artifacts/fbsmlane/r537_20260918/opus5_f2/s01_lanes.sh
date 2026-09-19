#!/bin/bash
#  #537 pass-2 measurements (Opus 5 measuring seat).  Run under WSL Gentoo:
#     MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/p2_536_537/opus5/scripts/s01_lanes.sh
#  Writes ONLY under /tmp/gxopus536p2 and _scratchpad/p2_536_537/opus5/out.  Never writes
#  GXEMUL-SEC, est/, build/, build-asan/ or /tmp/gxsec-build: every lane runs from a SCRATCH COPY
#  with its own selfmutant.py (the helper derives SEC from its own location).
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
FROZ=$ROOT/_scratchpad/p2_536_537/frozen
OPUS=$ROOT/_scratchpad/p2_536_537/opus5
OUT=$OPUS/out/lanes
W=/tmp/gxopus536p2
rm -rf "$W" "$OUT"; mkdir -p "$W" "$OUT"
S=$OUT/SUMMARY.txt
say() { echo "$*" | tee -a "$S"; }

#  ---- base copy (real src, config.h, helper, fragments, post-fix harness) ----
B=$W/base/GXEMUL-SEC
mkdir -p "$B/regress/selfmutants"
cp -a "$SEC/src" "$B/src"
cp "$SEC/config.h" "$B/config.h"
cp "$SEC/regress/selfmutant.py" "$B/regress/"
cp "$SEC/regress/selfmutants/fbpending_bound.old" "$SEC/regress/selfmutants/fbpending_bound.new" "$B/regress/selfmutants/"
cp "$FROZ/diff_fbpending_bound.c" "$B/regress/diff_fbpending_bound.c"
cmp -s "$FROZ/diff_fbpending_bound.c" "$SEC/regress/diff_fbpending_bound.c" && say "harness copy == working tree == frozen"
python3 "$OPUS/scripts/mkvariants.py" "$B/regress/diff_fbpending_bound.c" "$W/variants" | tee -a "$S"

OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
OBJS_WITHFB=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' 2>/dev/null | sort | tr '\n' ' ')
OBJS_NONE=$(find "/nonexistent-build-dir/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
say "objects: lane=$(printf '%s' "$OBJS" | wc -w)  with-dev_footbridge.o=$(printf '%s' "$OBJS_WITHFB" | wc -w)  none=$(printf '%s' "$OBJS_NONE" | wc -w)"

#  The gate's EXACT flag string (gate_offline.sh:1063), with $SEC/../build as the gate computes it.
XF_REL="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"
XF_WITHFB="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS_WITHFB -L/usr/X11R6/lib -lX11"
XF_NONE="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS_NONE -L/usr/X11R6/lib -lX11"

mkvariant() {  # name harness-file -> a copy whose src is a symlink to the base's real src
    local d=$W/v_$1/GXEMUL-SEC
    mkdir -p "$d/regress/selfmutants"
    ln -s "$B/src" "$d/src"
    cp "$B/config.h" "$d/config.h"
    cp "$B/regress/selfmutant.py" "$d/regress/"
    cp "$B/regress/selfmutants/fbpending_bound.old" "$B/regress/selfmutants/fbpending_bound.new" "$d/regress/selfmutants/"
    cp "$2" "$d/regress/diff_fbpending_bound.c"
    echo "$d"
}

lane() {  # tag sec-root xflags  -- exactly selfmutant_one's call, from cwd /tmp
    local tag=$1 sc=$2 xf=$3 rc t0 t1
    t0=$(date +%s.%N)
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$xf" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "R4 every case bounded" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    t1=$(date +%s.%N)
    say "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1) wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')s  gate-row(grep -c SELFMUTANT_OK)=$(grep -c 'SELFMUTANT_OK' "$OUT/$tag.txt")"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | tee -a "$S"
}

say "=== L0 reproduced in the base copy (the gate's exact flags) ==="
lane L0_base "$B" "$XF_REL"
say "=== Q2(a) harness prints FBBOUND_PASS unconditionally ==="
lane Qa_uncond_pass "$(mkvariant a "$W/variants/harness.a_uncond_pass.c")" "$XF_REL"
say "=== Q2(c) EXTRA keeps dev_footbridge.o in the object list ==="
lane Qc_with_fb_o "$B" "$XF_WITHFB"
say "=== Q2(d) R4 condition failures <= 1 ==="
lane Qd_r4_le1 "$(mkvariant d "$W/variants/harness.d_r4_le1.c")" "$XF_REL"
say "=== N1 reproduced: R3 blinded (>= 0) ==="
lane N1_r3blind "$(mkvariant n1 "$W/variants/harness.n1_r3blind.c")" "$XF_REL"
say "=== extra G: R3 blinded AND R1 tightened to trough >= 1 ==="
lane G_r3blind_r1tight "$(mkvariant g "$W/variants/harness.g_r3blind_r1tight.c")" "$XF_REL"
say "=== extra G0: R1 tightened alone ==="
lane G0_r1tight "$(mkvariant g0 "$W/variants/harness.g0_r1tight.c")" "$XF_REL"
say "=== P4: no build/ objects at all (find on an absent dir, as the gate's 2>/dev/null would give) ==="
lane P4_no_objects "$B" "$XF_NONE"

say "=== P1(symlink): the copy's harness is ITSELF a symlink into a dir holding a DECOY dev_footbridge.c ==="
DEC=$W/decoydir; mkdir -p "$DEC"
cp "$B/regress/diff_fbpending_bound.c" "$DEC/diff_fbpending_bound.c"
printf '#error "DECOY: the quote include resolved in the SYMLINK TARGET directory"\n' > "$DEC/dev_footbridge.c"
VS=$(mkvariant symdecoy "$B/regress/diff_fbpending_bound.c")
rm -f "$VS/regress/diff_fbpending_bound.c"; ln -s "$DEC/diff_fbpending_bound.c" "$VS/regress/diff_fbpending_bound.c"
say "  copy harness: $(ls -l "$VS/regress/diff_fbpending_bound.c" | awk '{print $9,$10,$11}')"
lane P1_symlink_decoy "$VS" "$XF_REL"
say "=== P1(control): the decoy placed IN the copy's regress/ itself (mirrored as a symlink into <mirror>/regress) ==="
VC=$(mkvariant ctrldecoy "$B/regress/diff_fbpending_bound.c")
cp "$DEC/dev_footbridge.c" "$VC/regress/dev_footbridge.c"
lane P1_ctrl_decoy_in_regress "$VC" "$XF_REL"

say "LANES_DONE"
