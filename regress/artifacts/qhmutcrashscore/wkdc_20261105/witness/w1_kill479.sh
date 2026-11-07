#!/bin/bash
#  WITNESS 1 (harness:) -- HEAD's kill479.sh scorer, fed STUB detectors whose endings are chosen.
#  The driver is HEAD's file with ONLY its three path lines (S, M, O) re-pointed into this dir;
#  witness_vs_HEAD.diff below proves that.  Runs in WSL:  bash .../witness/w1_kill479.sh
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
HEADDRV=$W/headsrc/regress/artifacts/wdccmdreset/killtable_20260827/kill479.sh
X=$W/witness/k479
DRV=${1:-$HEADDRV}            # the driver under test (HEAD by default; the fixed copy for the controls)
TAG=${2:-HEAD}
rm -rf "$X/$TAG"; mkdir -p "$X/$TAG"
#  the log is written HERE, not through wsl.exe: relayed stdout and stderr landed at
#  different offsets of one file on the first run and the stderr lines overwrote its head.
exec > "$X/W1_$TAG.log" 2>&1
S=$X/$TAG/S M=$X/$TAG/M O=$X/$TAG/O
mkdir -p "$S/regress" "$S/src/include/thirdparty" "$M" "$O"
python3 "$W/witness/mkstub_wdc.py" base > "$S/regress/diff_wdc_identify.c"
for m in Mk_kill Ms_survive Mc_early Mc_late Mx_exit1 Mcf_nocompile; do
	mkdir -p "$M/$m/regress"
	python3 "$W/witness/mkstub_wdc.py" "$m" > "$M/$m/regress/diff_wdc_identify.c"
done
sed -e "2s#.*#S=$S#" -e "3s#.*#M=$M#" -e "4s#.*#O=$O; mkdir -p \"\$O\"#" "$DRV" > "$X/$TAG/driver.sh"
diff "$DRV" "$X/$TAG/driver.sh" > "$X/$TAG/driver_vs_input.diff"
echo "driver under test: $DRV  md5 $(md5sum < "$DRV" | cut -c1-32)"
echo "lines changed by the re-pointing (must be exactly 2,3,4):"
grep -E '^[0-9]+(,[0-9]+)?c[0-9]+' "$X/$TAG/driver_vs_input.diff" | sed 's/^/  /'
echo
echo "=================== the driver's own output ==================="
bash "$X/$TAG/driver.sh" > "$X/$TAG/driver.out" 2>&1
echo "driver exit: $?"
cat "$X/$TAG/driver.out"
echo
echo "=================== ground truth, measured from each run's own log ==================="
printf "  %-14s %-10s %-22s %s\n" MUTANT RUN-EXIT SENTINEL "FAIL lines in log"
for m in Mk_kill Ms_survive Mc_early Mc_late Mx_exit1 Mcf_nocompile; do
	if [ -x "$O/$m" ]; then
		"$O/$m" > /dev/null 2>&1; rc=$?
		sent=$(tail -n 1 "$O/$m.out" | grep -oE '^WDC_IDENTIFY_(PASS|FAIL)$' || echo "ABSENT")
		printf "  %-14s %-10s %-22s %s\n" "$m" "$rc" "$sent" "$(grep -c '^  FAIL' "$O/$m.out")"
	else
		printf "  %-14s %-10s %-22s %s\n" "$m" "no binary" "-" "-"
	fi
done
echo "W1_KILL479_DONE $TAG"
