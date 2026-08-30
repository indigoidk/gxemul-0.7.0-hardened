#!/bin/bash
#
#  #494 -- run the SIGNATURE detector, the only row that sees the m3 escape.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/runsig494.sh
#
#  *** THIS FILE EXISTS BECAUSE THE INLINE FORM SILENTLY MEASURED NOTHING. ***  The
#  first attempt was `wsl -d Gentoo -- bash -lc '... $O ...'`.  `wsl ... -c '<string>'`
#  strips $VARS even inside single quotes, so $O emptied: the probe was handed
#  /base/gxemul and /fix/gxemul, the emulator never loaded the program, and the table
#  printed `??` in every cell under a VERDICT line reading "declined" for BOTH legs.
#  A false PASS.  The project's own guard did not fire because its pattern wanted a
#  BARE -c and this was `-lc`, a combined short-flag cluster -- fixed, and controlled
#  in both directions, in regress/artifacts/makercfalse/hook_controls_20260830/.
#
#  The rule the incident restates: RUN SCRIPTS AS FILES.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gx494}
R="$O/sig"
ART="$SEC/regress/artifacts/wdcaltoffset/killtable_20260830"
CD="$O/altoff-cd.img"

for leg in base fix; do
	if [ ! -x "$O/$leg/gxemul" ]; then
		echo "*** $O/$leg/gxemul missing -- run build494.sh first"
		exit 8
	fi
done

rm -rf "$R"
mkdir -p "$R"
[ -f "$CD" ] || dd if=/dev/zero of="$CD" bs=1M count=8 status=none

#  Frozen copies: one instrument for both legs.  The sig probe IMPORTS the main
#  detector, so BOTH must be frozen together or the import could change mid-run.
cp "$SEC/regress/wdc_altoffset_probe.py"     "$R/"
cp "$SEC/regress/wdc_altoffset_sig_probe.py" "$R/"

cd "$R" || exit 9
python3 -u "$R/wdc_altoffset_sig_probe.py" "$R" "$CD" \
    "base=$O/base/gxemul" "fix=$O/fix/gxemul" > "$R/SIG.out" 2>&1
RC=$?
echo "python rc = $RC"

#  A preserved log is verified by its COMPLETION SENTINEL, not by its existence --
#  and here the sentinel is NOT sufficient on its own, because the failed run above
#  printed one.  The CONTROLS are what say the run measured something, so they are
#  checked here rather than left to a reader.
tail -40 "$R/SIG.out"

if ! grep -q ALTOFF_SIG_DONE "$R/SIG.out"; then
	echo "*** NO ALTOFF_SIG_DONE -- not preserving a truncation"
	exit 8
fi
if grep -q '??' "$R/SIG.out"; then
	echo "*** THE TABLE CONTAINS ?? -- registers were not read.  The run did not"
	echo "*** measure anything, whatever the verdict line says.  NOT preserving."
	exit 8
fi
if ! grep -q 'calls the image a CD-ROM: True' "$R/SIG.out"; then
	echo "*** THE IMAGE WAS NOT RECOGNISED AS A CD-ROM -- the signature channel is"
	echo "*** DEAD, so every leg would read 'declined' whatever the code does."
	exit 8
fi

cp "$R/SIG.out" "$ART/RESULTS_signature.txt"
echo "preserved: killtable_20260830/RESULTS_signature.txt"
echo "RUNSIG494_DONE"
