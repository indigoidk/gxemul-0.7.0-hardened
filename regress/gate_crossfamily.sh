#!/bin/bash
# GATE 4 -- non-MIPS CPU cores actually execute guest code.
#
# float_emul.c is shared by the alpha, m88k, mips, ppc and sh cores, but until this gate
# existed only MIPS had ever executed it under test. Round 51 instrumented the old
# 20-machine smoke and measured that it performed ZERO floating-point stores.
#
# WHAT THIS GATE DOES AND DOES NOT PROVE. It proves the m88k and SH4 cores execute a full
# guest to a shell and return CHECKED ANSWERS -- "the guest kept running" is not a result,
# because a wrong float_emul.c arm keeps the guest running perfectly.
#
# It does NOT prove #287. The luna88k check computes 1.5/3.0 and sqrt(2), and gate 2's own
# closed form says old and new can only differ at |x| >= 2^128 or |x| < 2^-126. Both of
# those values are far inside the region where the two implementations agree, so reverting
# #287 would leave this gate green. That was claimed as #287 coverage in an earlier draft
# and it was wrong. #287 is covered by gate 2, which links the real float_emul.c; this gate
# covers the cores that CALL it. The S-format overflow arm has no in-guest coverage on any
# rig -- see images.md.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

GX=${GX:-$ROOT/build/gxemul}

gate_begin "cross-family-execution"
need_exec "$GX"
command -v python3 >/dev/null 2>&1 || gate_skip "python3 not on PATH"

# run_rig <rig> <image> <expected answer> <note>
# The expected answer is a LITERAL here, not a value read back out of the driver's own
# output. Comparing the driver's VALUES against the driver's VALUES_WANT meant that when
# the driver produced neither, the check compared "" with "" and printed ok.
run_rig() {
    local rig=$1 img=$2 want=$3 note_txt=$4
    if [ ! -f "$img" ]; then
        degrade "$rig: image absent, rig did not run (see images.md)"
        return
    fi

    note "$rig -- $note_txt"
    local out=$LOGDIR/rig_$rig.out
    python3 -u "$HERE/drive_guest.py" "$rig" "$GX" > "$out" 2>&1
    sed 's/^/       /' "$out"

    v() { grep -E "^$1=" "$out" | head -1 | cut -d= -f2-; }
    check "$rig: reached boot milestone" "$(v BOOT_REACHED)" "1"
    check "$rig: computed answer"        "$(v VALUES)"       "$want"
    check "$rig: verdict"                "$(v VERDICT)"      "PASS"
    echo
}

# m88k stores IEEE_FMT_S from a non-MIPS caller and has awk on the media, so it can check
# a real floating-point answer: 1.5/3.0 and sqrt(2).
run_rig luna88k "$IMAGES/liveimage-luna88k-raw-20250518.img" "0.500000,1.414214" \
    "m88k M88100, OpenBSD 7.7, in-guest FP with a checked result"

# SuperH proves the SH4 core executes a full kernel boot through device attachment. It
# sends NO guest input: the emulated SuperH console loses writes non-deterministically
# (measured), so any interactive check is intermittent, and an intermittent gate gets
# ignored and then disabled. The checked answer is the chip identity the guest's own PCI
# probe prints. See drive_guest.py and OUTSTANDING_BUGS.md.
run_rig landisk "$IMAGES/openbsd76-landisk-bsd.rd" "SH7751R" \
    "SuperH SH4, OpenBSD 7.6, full kernel boot with a checked probe result"

gate_end
exit $?
