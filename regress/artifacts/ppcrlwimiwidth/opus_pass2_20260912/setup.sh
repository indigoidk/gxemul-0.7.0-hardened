#!/bin/bash
set -e
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_p2
CL=/tmp/gxopus_p2

echo "=== fresh clone ==="
rm -rf "$CL"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL"
rm -f "$CL/.MUTANT"

echo "=== copy SEC sources (the fix) into clone baseline ==="
cp "$SEC/src/cpus/cpu_arm_coproc.c" "$SEC/src/cpus/cpu_ppc_instr.c" "$CL/src/cpus/"

echo "=== freeze probes ==="
cp "$SEC/regress/xscale_inten_probe.py" "$SD/xscale_inten_probe.frozen.py"
cp "$SEC/regress/ppc_rlwimi_probe.py" "$SD/ppc_rlwimi_probe.frozen.py"
cp "$SEC/regress/ppc_rldimi_probe.py" "$SD/ppc_rldimi_probe.frozen.py"

echo "=== artifact dirs ==="
mkdir -p "$SEC/regress/artifacts/xscaleinten/opus_pass2_20260912"
mkdir -p "$SEC/regress/artifacts/ppcrlwimiwidth/opus_pass2_20260912"

echo "=== baseline build (the fix) ==="
cd "$CL"
rm -f src/cpus/*.o
make -j4 >/tmp/opus_build.log 2>&1
tail -2 /tmp/opus_build.log
if [ gxemul -nt src/cpus/cpu_ppc_instr.c ] && [ gxemul -nt src/cpus/cpu_arm_coproc.c ]; then
  echo "BINARY FRESH OK"
else
  echo "BINARY STALE -- FAIL"; exit 1
fi
ls -la gxemul
echo SETUP_DONE
