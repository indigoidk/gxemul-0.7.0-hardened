#!/bin/bash
#  #501 pass-3 Opus escape hunt.  Runs in a SCRATCH CLONE only.  Sentinel first.
T=/tmp/gxopus501p3
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/panel_501p3_agents/opus
cd "$T" || exit 9
F=src/devices/dev_pcc2.c

mut () {   #  $1 name  $2 python-edit-file
  echo "$F  $1" > "$T/.MUTANT"
  cp /tmp/pcc2.baseline.c "$F"
  python3 "$2" "$F" || { echo "$1 EDIT_FAILED"; return 1; }
  n=$(diff /tmp/pcc2.baseline.c "$F" | grep -c '^[<>]')
  echo "=== $1 : difflines=$n"
  diff /tmp/pcc2.baseline.c "$F"
  rm -f src/devices/dev_pcc2.o gxemul
  make -j4 > /tmp/mut_build.log 2>&1
  rc=$?
  if [ $rc -ne 0 ] || [ ! -x gxemul ]; then echo "$1 BUILD_FAILED rc=$rc"; tail -5 /tmp/mut_build.log; return 1; fi
  if [ ! gxemul -nt "$F" ]; then echo "$1 BINARY_STALE"; return 1; fi
  ( cd "$SEC/regress" && python3 -u pcc2_default_probe.py "$T/gxemul" "$1" ) > "$OUT/probe_$1.out" 2>&1
  grep -E "PCC2D_RESULT|PCC2D_RED|PCC2D_PROBE_DONE" "$OUT/probe_$1.out"
}

for m in "$@"; do
  mut "$m" "$OUT/edit_$m.py"
done

#  RESTORE + REBUILD, verified against SEC (never against the script's own backup path alone)
cp /tmp/pcc2.baseline.c "$F"
if cmp -s "$F" "$SEC/src/devices/dev_pcc2.c"; then echo "RESTORE_CMP_CLEAN_VS_SEC"; else echo "RESTORE_DIFFERS -- SENTINEL KEPT"; exit 7; fi
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/restore_build.log 2>&1
echo "RESTORE_MAKE_RC=$?"
if [ gxemul -nt "$F" ]; then rm -f "$T/.MUTANT"; echo "SENTINEL_CLEARED (two-part clearance: cmp clean AND binary newer)"; else echo "REBUILD_STALE -- SENTINEL KEPT"; fi
