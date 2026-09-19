#!/bin/bash
#  #537 F2 repair measurement: the lane's pin moved from R4 (verdict-equivalent) to R3's
#  "cats, slowest legal" row.  WSL Gentoo.  Writes ONLY /tmp/sm537b and _scratchpad/t537/out_b.
#    P0  the gate's exact lane call, new pin, real tree              want SELFMUTANT_OK via R3
#    P1  composite (R3 blinded + R1 tightened), NEW pin              want SELFMUTANT_FAIL (not via the named row)
#    P2  the same composite, OLD R4 pin                              want SELFMUTANT_OK -- the escape the move closes
#    P3  R3 blinded alone, new pin                                   want SELFMUTANT_FAIL
#    P4  R1 tightened alone, new pin (green on the fix?)             want SELFMUTANT_OK  -- the composite's second edit
#                                                                    is inert alone (the carrier's licence for a composite)
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
OUT=$ROOT/_scratchpad/t537/out_b2
S=/tmp/sm537b
rm -rf "$S" "$OUT"; mkdir -p "$S" "$OUT"
OBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort | tr '\n' ' ')
echo "build/ objects linked: $(printf '%s' "$OBJS" | wc -w)" | tee "$OUT/SUMMARY.txt"
XF="-std=gnu99 -I../src/include -I../src/include/thirdparty -I../src/devices $OBJS -L/usr/X11R6/lib -lX11"
NEWPIN="R3 the reset still owes one interrupt        cats, slowest legal"
OLDPIN="R4 every case bounded"
grep -c "$NEWPIN" "$SEC/regress/gate_offline.sh" | sed 's/^/new pin present in gate_offline.sh: /' | tee -a "$OUT/SUMMARY.txt"

mkcopy() {  # dir harness-file
    local d=$1/GXEMUL-SEC
    mkdir -p "$d/regress/selfmutants"
    cp -a "$SEC/src" "$d/src"
    cp "$SEC/config.h" "$d/config.h"
    cp "$SEC/regress/selfmutant.py" "$d/regress/"
    cp "$SEC/regress/selfmutants/fbpending_bound.old" "$SEC/regress/selfmutants/fbpending_bound.new" "$d/regress/selfmutants/"
    cp "$2" "$d/regress/diff_fbpending_bound.c"
}
lane() {  # tag sec-root pin
    local tag=$1 sc=$2 pin=$3 rc
    ( cd /tmp && SELFMUTANT_EXTRA_FLAGS="$XF" python3 "$sc/regress/selfmutant.py" \
        diff_fbpending_bound.c src/devices/dev_footbridge.c \
        "$sc/regress/selfmutants/fbpending_bound.old" "$sc/regress/selfmutants/fbpending_bound.new" \
        "$pin" ) > "$OUT/$tag.txt" 2>&1
    rc=$?
    echo "$tag rc=$rc token=$(grep -oE 'SELFMUTANT_(OK|FAIL|SETUP)' "$OUT/$tag.txt" | tail -1)" | tee -a "$OUT/SUMMARY.txt"
    grep -E '^       ' "$OUT/$tag.txt" | sed 's/^/    /' | tee -a "$OUT/SUMMARY.txt"
}
#  Variants by sed, count-checked: the harness is CRLF and sed keeps each line ending.  R3 is the only
#  line holding "worst_trough >= 1,"; R1 is the only one holding "worst_peak <= ceiling && worst_trough >= 0,".
variant() {  # src dst kind
    local src=$1 dst=$2 kind=$3
    cp "$src" "$dst"
    if [ "$kind" = blindR3 ] || [ "$kind" = composite ]; then
        [ "$(grep -c "worst_trough >= 1," "$dst")" = 1 ] || { echo "R3 anchor not unique"; exit 5; }
        sed -i "s/worst_trough >= 1,/worst_trough >= 0,/" "$dst"
    fi
    if [ "$kind" = tightenR1 ] || [ "$kind" = composite ]; then
        [ "$(grep -c "worst_peak <= ceiling && worst_trough >= 0," "$dst")" = 1 ] || { echo "R1 anchor not unique"; exit 5; }
        sed -i "s/worst_peak <= ceiling \&\& worst_trough >= 0,/worst_peak <= ceiling \&\& worst_trough >= 1,/" "$dst"
    fi
    echo "$kind written: $(diff "$src" "$dst" | grep -c '^>') line(s) changed, CR kept: $(grep -c $'' "$dst")"
}
lane P0_newpin "$SEC" "$NEWPIN"
variant "$SEC/regress/diff_fbpending_bound.c" "$S/composite.c" composite | tee -a "$OUT/SUMMARY.txt"
mkcopy "$S/comp" "$S/composite.c"
lane P1_composite_newpin "$S/comp/GXEMUL-SEC" "$NEWPIN"
lane P2_composite_oldpin "$S/comp/GXEMUL-SEC" "$OLDPIN"
variant "$SEC/regress/diff_fbpending_bound.c" "$S/blind.c" blindR3 | tee -a "$OUT/SUMMARY.txt"
mkcopy "$S/blind" "$S/blind.c"
lane P3_blindR3_newpin "$S/blind/GXEMUL-SEC" "$NEWPIN"
variant "$SEC/regress/diff_fbpending_bound.c" "$S/tight.c" tightenR1 | tee -a "$OUT/SUMMARY.txt"
mkcopy "$S/tight" "$S/tight.c"
lane P4_tightenR1_newpin "$S/tight/GXEMUL-SEC" "$NEWPIN"
rm -rf "$S"
echo "RUN537B_DONE" | tee -a "$OUT/SUMMARY.txt"
