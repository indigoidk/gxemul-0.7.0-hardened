#!/bin/bash
set -e
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_p2
CL=/tmp/gxopus_p2
OX="$SEC/regress/artifacts/xscaleinten/opus_pass2_20260912"
STUB="$SEC/regress/artifacts/xscaleinten/base_20260912/xscale_stub.bin"
F=src/cpus/cpu_arm_coproc.c
T=$'\t'

OLD="cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;"
printf '%s' "$OLD" > "$SD/x_old.txt"

apply () {  # $1 = label, $2 = mutant C body (single stmt)
  local L="$1"; local BODY="$2"
  cp "$SEC/src/cpus/cpu_arm_coproc.c" "$CL/$F"
  printf 'cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;\n%s%s%s%s%s\n' "$T" "$T" "$T" "$T" "$BODY" > "$SD/x_new.txt"
  python3 "$SD/patch.py" "$CL/$F" "$SD/x_old.txt" "$SD/x_new.txt"
  cp "$SD/x_new.txt" "$OX/mutant_${L}.txt"
  touch "$CL/.MUTANT"
  echo "$F XSCALE $L" > "$CL/.MUTANT"
  cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
  if ! [ gxemul -nt "$CL/$F" ]; then echo "$L BUILD STALE/FAIL"; tail -3 /tmp/ob.log; return; fi
  python3 -u "$SD/xscale_inten_probe.frozen.py" "$CL/gxemul" "$L" "$STUB" > "$OX/xscale_${L}.log" 2>&1 || true
  echo -n "$L : "; grep -E 'XSCALE_RESULT|XSCALE_CONTROL' "$OX/xscale_${L}.log" | tr '\n' ' '
  echo -n " FAILING="; grep '^FAILING' "$OX/xscale_${L}.log"
}

apply XM_RD0     'if (rd == 0) { fatal("TODO: XScale read from inten?\n"); exit(1); }'
apply XM_ISTEER  'if (cpu->cd.arm.i80321_isteer != 0) { fatal("TODO: XScale read from inten?\n"); exit(1); }'
apply XM_MAGICBIT 'if (cpu->cd.arm.i80321_inten & 0x00400000) { fatal("TODO: XScale read from inten?\n"); exit(1); }'

echo "=== restore + rebuild ==="
cp "$SEC/src/cpus/cpu_arm_coproc.c" "$CL/$F"
cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
cmp -s "$CL/$F" "$SEC/src/cpus/cpu_arm_coproc.c" && [ gxemul -nt "$CL/$F" ] && { rm -f "$CL/.MUTANT"; echo "RESTORE CLEAN, sentinel cleared"; } || echo "RESTORE PROBLEM"
echo MUT_XSCALE_DONE
