#!/bin/bash
# QUIET SLOT (no panel, no seat, no other gate): gates 1 2 4 6 in ONE run -- #545 (3f) targeted gate 2 at 864 rows and the
# census's (#546) gate 6 on its F6e files, graded on the pty logs gate 4 produces in THIS run -- then gate 14 on #545's COMMIT
# BLOB of gate_arm.sh (HEAD + #545's two hunks; #529's section excluded), from a /tmp copy of regress/.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
O2=$SEC/regress/artifacts/fbd5/q2_20260923/r3f_20260923/gates_final
O6=$SEC/regress/artifacts/hygienecensus_20260923/gate6_f6e
O14=$SEC/regress/artifacts/fbd5/q2_20260923/r3f_20260923/gate_arm
mkdir -p "$O2" "$O6" "$O14"
L=/tmp/gxregress_final; rm -rf "$L"; mkdir -p "$L"
{
  echo "RUN1246_START $(date '+%F %T')  HEAD $(git -C $SEC rev-parse --short HEAD)"
  (cd "$SEC" && md5sum regress/gate_offline.sh regress/diff_footbridge.c src/devices/dev_footbridge.c \
      regress/gate_hygiene.sh regress/census_tokens.py tools/derive_hygiene_pins.sh regress/crime_width_probe.py \
      regress/luna_absentcpu_probe.py | cut -c1-8,33-)
  echo "dirty tracked files: $(git -C $SEC status --porcelain --untracked-files=no | wc -l)"
} > "$O2/RUN_TIMES.txt"
( cd "$SEC/regress" && LOGDIR="$L" bash run.sh 1 2 4 6 ) > "$O2/run_1246.log" 2>&1
rc=$?
echo "RUN1246_DONE $(date '+%F %T') rc=$rc" >> "$O2/RUN_TIMES.txt"
for f in "$L"/*.log "$L"/*.ptylog "$L"/arc.screen; do [ -f "$f" ] && cp "$f" "$O2/"; done
ls -la "$L" > "$O2/LOGDIR_LISTING.txt" 2>&1
cp "$O2/RUN_TIMES.txt" "$O6/RUN_TIMES.txt"; cp "$O2/run_1246.log" "$O6/run_1246.log"
for f in "$L"/*hygiene*; do [ -f "$f" ] && cp "$f" "$O6/"; done
echo "RUN1246_COPIED" >> "$O2/RUN_TIMES.txt"

X=/tmp/gxarm545f; L14=/tmp/gxarm545f_logs; rm -rf "$X" "$L14"; mkdir -p "$X/regress" "$L14"
(cd "$SEC/regress" && find . -maxdepth 1 -type f -exec cp -p {} "$X/regress/" \;)
cp "$R/_scratchpad/t545/ga_stage.sh" "$X/regress/gate_arm.sh"
{
  echo "GATE14_START $(date '+%F %T')  HEAD $(git -C $SEC rev-parse --short HEAD)"
  echo "gate_arm.sh = the #545 commit blob: $(md5sum $X/regress/gate_arm.sh | cut -c1-8) (HEAD $(git -C $SEC show HEAD:regress/gate_arm.sh | md5sum | cut -c1-8), working $(md5sum $SEC/regress/gate_arm.sh | cut -c1-8))"
  (cd "$X/regress" && md5sum footbridge_sites_probe.py fbpending_drain_probe.py fbpending_witness.py | cut -c1-8,33-)
  echo "PMAX build/gxemul $(stat -c %y $R/build/gxemul | cut -c1-19); build/ dev_footbridge.c $(cmp -s $R/build/src/devices/dev_footbridge.c $SEC/src/devices/dev_footbridge.c && echo CLEAN || echo DIFFERS)"
} > "$O14/TIMES.txt"
( cd "$X/regress" && LOGDIR="$L14" bash gate_arm.sh ) > "$O14/gate_arm_545.log" 2>&1
rc=$?
echo "GATE14_DONE $(date '+%F %T') rc=$rc" >> "$O14/TIMES.txt"
cp -p "$L14"/*.log "$O14/" 2>/dev/null
ls -la "$L14" > "$O14/LOGDIR_LISTING.txt"
echo "QUIET_FINAL_DONE $(date '+%F %T')" >> "$O14/TIMES.txt"
tail -30 "$O2/run_1246.log" | sed 's/\x1b\[[0-9;]*m//g'; tail -3 "$O14/gate_arm_545.log" | sed 's/\x1b\[[0-9;]*m//g'
cat "$O2/RUN_TIMES.txt" "$O14/TIMES.txt"
