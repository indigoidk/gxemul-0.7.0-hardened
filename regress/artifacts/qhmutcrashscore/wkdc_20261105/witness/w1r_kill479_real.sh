#!/bin/bash
#  CONTROL (valid long run): the kill479.sh driver with its BASELINE = HEAD's REAL diff_wdc_identify.c
#  compiled against HEAD's REAL dev_wdc.c (wkdc/headsrc_src, from `git archive HEAD`), and two stub
#  mutants (a genuine kill and a genuine survivor).  The fixed driver must NOT refuse the real
#  128-row run -- a tightening that rejects valid runs is worse than none.
#  usage: bash w1r_kill479_real.sh [DRIVER] [TAG]
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
DRV=${1:-$W/headsrc/regress/artifacts/wdccmdreset/killtable_20260827/kill479.sh}
TAG=${2:-HEAD}
SRCTREE=${3:-$W/headsrc_src}   # headsrc_src = git archive HEAD; r479src = git archive 23430365 (#479)
X=$W/witness/k479real/$(basename "$SRCTREE")
mkdir -p "$X"
rm -rf "$X/$TAG"; mkdir -p "$X/$TAG"
exec > "$X/W1R_$TAG.log" 2>&1
S=$SRCTREE M=$X/$TAG/M O=$X/$TAG/O
mkdir -p "$M" "$O"
for m in Mk_kill Ms_survive; do
	mkdir -p "$M/$m/regress"
	python3 "$W/witness/mkstub_wdc.py" "$m" > "$M/$m/regress/diff_wdc_identify.c"
done
sed -e "2s#.*#S=$S#" -e "3s#.*#M=$M#" -e "4s#.*#O=$O; mkdir -p \"\$O\"#" "$DRV" > "$X/$TAG/driver.sh"
echo "driver under test: $DRV  md5 $(md5sum < "$DRV" | cut -c1-32)"
echo "baseline tree: $SRCTREE"
echo "baseline detector: regress/diff_wdc_identify.c md5 $(md5sum < "$S/regress/diff_wdc_identify.c" | cut -c1-32)"
echo "                   src/devices/dev_wdc.c          md5 $(md5sum < "$S/src/devices/dev_wdc.c" | cut -c1-32)"
echo "=================== the driver's own output ==================="
bash "$X/$TAG/driver.sh" > "$X/$TAG/driver.out" 2>&1
echo "driver exit: $?"
cat "$X/$TAG/driver.out"
echo "baseline log: $(wc -l < "$O/base.out") lines, last line: $(tail -n 1 "$O/base.out")"
echo "W1R_DONE $TAG"
