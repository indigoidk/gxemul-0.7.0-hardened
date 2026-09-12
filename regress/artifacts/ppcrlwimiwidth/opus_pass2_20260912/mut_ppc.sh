#!/bin/bash
set -e
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_p2
CL=/tmp/gxopus_p2
OP="$SEC/regress/artifacts/ppcrlwimiwidth/opus_pass2_20260912"
F=src/cpus/cpu_ppc_instr.c

mutate () { # label  probe(rlwimi|rldimi)  old  new
  local L="$1" P="$2" OLD="$3" NEW="$4"
  cp "$SEC/src/cpus/cpu_ppc_instr.c" "$CL/$F"
  printf '%s' "$OLD" > "$SD/p_old.txt"; printf '%s' "$NEW" > "$SD/p_new.txt"
  python3 "$SD/patch.py" "$CL/$F" "$SD/p_old.txt" "$SD/p_new.txt"
  printf 'OLD: %s\nNEW: %s\n' "$OLD" "$NEW" > "$OP/mutant_${L}.txt"
  echo "$F PPC $L" > "$CL/.MUTANT"
  cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
  if ! [ gxemul -nt "$CL/$F" ]; then echo "$L BUILD STALE/FAIL"; tail -4 /tmp/ob.log; return; fi
  python3 -u "$SD/ppc_${P}_probe.frozen.py" "$CL/gxemul" "$L" > "$OP/${P}_${L}.log" 2>&1 || true
  echo -n "$L ($P): "; grep -E "PPC_${P^^}_RESULT|PPC_${P^^}_CONTROL" "$OP/${P}_${L}.log" | tr '\n' ' '
  echo -n " FAILING="; grep '^FAILING' "$OP/${P}_${L}.log"
}

mutate RM_GE     rlwimi 'if (mb > me)' 'if (mb >= me)'
mutate RM_UNROT  rlwimi '| ((uint64_t)tmp << 32);' '| ((uint64_t)(uint32_t)reg(ic->arg[0]) << 32);'
mutate DM_ROT1   rldimi 'while (n-- != 0) {' 'while (n-- > 1) {'
mutate DM_NOAND_END rldimi 'while (m != ((64 - sh) & 63));' 'while (m != (64 - sh));'

echo "=== restore + rebuild ==="
cp "$SEC/src/cpus/cpu_ppc_instr.c" "$CL/$F"
cd "$CL"; rm -f src/cpus/*.o; make -j4 >/tmp/ob.log 2>&1
cmp -s "$CL/$F" "$SEC/src/cpus/cpu_ppc_instr.c" && [ gxemul -nt "$CL/$F" ] && { rm -f "$CL/.MUTANT"; echo "RESTORE CLEAN, sentinel cleared"; } || echo "RESTORE PROBLEM"
echo MUT_PPC_DONE
