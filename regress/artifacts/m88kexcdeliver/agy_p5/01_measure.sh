#!/bin/bash
set -e

S=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/m88kexc/agy_p5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxagy502

echo "=== STARTING MEASUREMENT SUITE ==="
echo "TABLE pass5 m88kexcdeliver $(date +%F' '%T)" > "$C/.MUTANT"
echo "src/cpus/cpu_m88k.c -- restore: cp $SEC/src/cpus/cpu_m88k.c ; cmp ; rebuild" >> "$C/.MUTANT"

MUTANTS=(
  "M_FALLBACK127"
  "M_FALLBACK_NO_BOUND"
  "M_SFRZ_EPSR_SWAP"
  "M_TAIL_ERROR_DROP"
  "M_TAIL_BOUNDS_DROP"
  "M_SFRZ_TRAP_UPDATE"
)

for M in "${MUTANTS[@]}"; do
  echo "=================================================="
  echo ">>> MEASURING $M  $(date +%T)"
  echo "=================================================="
  
  # 1. Apply mutant
  echo "$M active" > "$C/.MUTANT"
  python3 "$S/mutate.py" "$M" > "$S/mut_$M.log" 2>&1
  if ! grep -q "MUTATE_OK" "$S/mut_$M.log"; then
    echo "MUTATE_FAIL for $M! Log:"
    cat "$S/mut_$M.log"
    exit 1
  fi
  cat "$S/mut_$M.log"
  
  # 2. Rebuild
  bash "$S/rebuild.sh" > "$S/build_$M.log" 2>&1
  if ! grep -q "REBUILD_DONE" "$S/build_$M.log"; then
    echo "BUILD_FAIL for $M! Log:"
    tail -20 "$S/build_$M.log"
    exit 1
  fi
  
  # 3. Run probe
  python3 -u "$C/probe.frozen.py" "$C/gxemul" > "$S/$M.out" 2>&1 || true
  
  # 4. Check probe results
  echo "Probe output summary for $M:"
  grep -E 'M88KEXC_RESULT|M88KEXC_DONE|M88KEXC_SELFTEST' "$S/$M.out" || echo "NO_RESULT_LINE"
  grep -E 'RESULT=(BADREGS|STOP|TAILHALT|NOSTART|NOBOOT)|bad=' "$S/$M.out" | sed 's/^/   RED: /' || true
  grep -E 'M88KEXC_ROW=(resid50|sfu1h)' "$S/$M.out" | sed 's/^/   NEG: /' || true
  
  if ! grep -q "M88KEXC_DONE" "$S/$M.out"; then
    echo "WARNING: $M did not print M88KEXC_DONE!"
  fi

  # 5. Restore from GXEMUL-SEC
  cp "$SEC/src/cpus/cpu_m88k.c" "$C/src/cpus/cpu_m88k.c"
  if cmp "$C/src/cpus/cpu_m88k.c" "$SEC/src/cpus/cpu_m88k.c"; then
    echo "RESTORE_CMP_CLEAN $M"
  else
    echo "RESTORE_CMP_FAILED $M!"
    exit 1
  fi
  
  # 6. Rebuild restored tree
  bash "$S/rebuild.sh" > "$S/restore_$M.log" 2>&1
  if ! grep -q "REBUILD_DONE" "$S/restore_$M.log"; then
    echo "RESTORE_BUILD_FAIL for $M!"
    exit 1
  fi
done

echo "=================================================="
echo ">>> RUNNING FINAL BASELINE PROBE  $(date +%T)"
echo "=================================================="
python3 -u "$C/probe.frozen.py" "$C/gxemul" > "$S/BASE_final.out" 2>&1

grep -E 'M88KEXC_RESULT|M88KEXC_DONE|M88KEXC_SELFTEST' "$S/BASE_final.out"

if grep -q "M88KEXC_RESULT=29/29" "$S/BASE_final.out" && grep -q "M88KEXC_DONE" "$S/BASE_final.out"; then
  rm -f "$C/.MUTANT"
  echo "SENTINEL_CLEARED_CLEAN_BASE_29_OF_29"
else
  echo "SENTINEL_KEPT_BASE_NOT_29_OF_29!"
  exit 1
fi

echo "=== ALL MEASUREMENTS COMPLETE ==="
