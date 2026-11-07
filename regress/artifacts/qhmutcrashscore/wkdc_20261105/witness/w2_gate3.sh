#!/bin/bash
#  WITNESS 2 (harness:) -- gate 3, regress/selftest_mutation.sh, run as a WHOLE GATE in a fake ROOT.
#  The gate script and lib.sh are HEAD's bytes (md5 printed); only the DETECTOR is swapped:
#     STUB=mixed|allkill  -> witness/stub_diff_ieee_store.c (no float_emul.c behaviour is tested)
#     STUB=real           -> HEAD's real regress/diff_ieee_store.c (the valid-run control)
#  float_emul.c, src/include and diff_ieee_store.c come from `git archive HEAD` (wkdc/headsrc_src);
#  config.h is a copy of build/config.h (wkdc/fake/config.h).  Nothing outside wkdc/ is written.
#  usage: bash w2_gate3.sh [DRIVER] [TAG] [STUB]
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
X=$W/witness/g3
DRV=${1:-$W/headsrc/regress/selftest_mutation.sh}
TAG=${2:-HEAD}
STUB=${3:-mixed}
R=$X/$TAG.$STUB
rm -rf "$R"; mkdir -p "$R"
exec > "$X/W2_$TAG.$STUB.log" 2>&1
mkdir -p "$R/ROOT/build/src/core" "$R/ROOT/build/src/include" "$R/regress" "$R/logdir"
cp "$W/fake/config.h" "$R/ROOT/build/config.h"
cp -r "$W/headsrc_src/src/include/." "$R/ROOT/build/src/include/"
cp "$W/headsrc_src/src/core/float_emul.c" "$R/ROOT/build/src/core/float_emul.c"
cp "$DRV" "$R/regress/selftest_mutation.sh"
cp "$W/headsrc/regress/lib.sh" "$R/regress/lib.sh"
if [ "$STUB" = real ]; then
	cp "$W/headsrc_src/regress/diff_ieee_store.c" "$R/regress/diff_ieee_store.c"
else
	cp "$W/witness/stub_diff_ieee_store.c" "$R/regress/diff_ieee_store.c"
fi
echo "gate script: $DRV  md5 $(md5sum < "$DRV" | cut -c1-32)"
echo "lib.sh md5 $(md5sum < "$R/regress/lib.sh" | cut -c1-32)   detector: $STUB  md5 $(md5sum < "$R/regress/diff_ieee_store.c" | cut -c1-32)"
echo "float_emul.c md5 $(md5sum < "$R/ROOT/build/src/core/float_emul.c" | cut -c1-32)"
echo "=================== the gate's own output ==================="
STUBSET=$STUB ROOT=$R/ROOT LOGDIR=$R/logdir bash "$R/regress/selftest_mutation.sh"
echo "gate exit: $?"
echo "=================== ground truth, from each run's own log ==================="
printf "  %-22s %-9s %s\n" BINARY RUN-EXIT "LAST LINE OF ITS LOG"
for b in real mut_revert287 mut_tiesaway mut_modeignored mut_wlegacyrounds mut_revert303 mut_maskcarry mut_flushband; do
	f=$R/logdir/mutation/$b
	if [ -x "$f" ]; then
		( cd "$R/logdir/mutation" && STUBSET=$STUB "./$b" > /dev/null 2>&1 ); rc=$?
		printf "  %-22s %-9s %s\n" "$b" "$rc" "$(tail -n 1 "$f.out" 2>/dev/null | cut -c1-60)"
	else
		printf "  %-22s %-9s %s\n" "$b" "no binary" "-"
	fi
done
echo "W2_GATE3_DONE $TAG $STUB"
