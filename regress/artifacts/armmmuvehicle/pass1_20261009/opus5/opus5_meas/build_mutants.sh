#!/bin/bash
# opus5 seat: build every mutant in its OWN copy of the base scratch clone, in parallel.
# Reads /tmp/gxopusmmuv (the cmp-verified base clone); writes /tmp/gxopusmmuv_<M> and /tmp/gxopusmmuv_bins.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE=/tmp/gxopusmmuv
BINS=/tmp/gxopusmmuv_bins
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
mkdir -p "$BINS"
# (1) the baseline: source identity with the working tree, and a fresh binary
for f in src/cpus/memory_arm.c src/cpus/cpu_arm.c src/cpus/cpu_arm_coproc.c; do
  if cmp -s "$BASE/$f" "$SEC/$f"; then echo "BASE_CMP_OK $f"; else echo "BASE_CMP_DIFF $f"; exit 4; fi
  if [ "$BASE/gxemul" -nt "$BASE/$f" ]; then echo "BASE_FRESH $f"; else echo "BASE_STALE $f"; exit 4; fi
done
cp -p "$BASE/gxemul" "$BINS/BASE"
MUTS="M_dom0 M_farpage M_ttbstale M_l2idx11 M_domPS M_ckR M_pgdom0 M_permPS M_dabtret M_c8nop M_c2mask"
for m in $MUTS; do
  (
    D=/tmp/gxopusmmuv_$m
    rm -rf "$D"; cp -a "$BASE" "$D"
    python3 "$HERE/mutants.py" "$D" "$m" > "$D.apply.log" 2>&1 || { echo "APPLY_FAILED $m"; cat "$D.apply.log"; exit 1; }
    cd "$D" && rm -f src/cpus/*.o gxemul && make -j2 > "$D.build.log" 2>&1
    f=$(cut -d' ' -f1 "$D/.MUTANT")
    if [ -x "$D/gxemul" ] && [ "$D/gxemul" -nt "$D/$f" ]; then
      cp -p "$D/gxemul" "$BINS/$m"; echo "BUILT $m ($(md5sum < "$D/gxemul" | cut -c1-8)) $(grep -c "$m" "$D/$f") marker-line(s) in $f"
    else
      echo "BUILD_FAILED $m"; tail -5 "$D.build.log"
    fi
  ) &
done
wait
ls -la "$BINS"
md5sum "$BINS"/* | cut -c1-8,34-
echo BUILD_MUTANTS_DONE
