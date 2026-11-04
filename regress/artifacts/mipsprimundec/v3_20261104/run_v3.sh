#!/bin/bash
#  run_v3.sh -- mipsprimundec v3 (main loop, 2026-11-04 04:4x).  Builds the v3 (apply_v3.py: the measured draft plus grok's two
#  consensus edits, without the draft's stray blank-line hunk) in the main loop's own clone /tmp/gxmain_mpu3, which is removed afterwards,
#  and measures it with FROZEN copies: the per-word table (main_table_frozen.py), the same table with two more CPUs (main_table_cpus.py:
#  R6000 = ISA II, 24KEc = MIPS32/MODE32), and the witness probe (probe_frozen.py; the repo copy differs from the witness's frozen copy
#  only in its docstring).  The two-CPU table also runs on build/gxemul (HEAD's MIPS path) for the baseline.  No project tree is written.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/mipsprimundec/v3_20261104
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build; C=/tmp/gxmain_mpu3; F=src/cpus/cpu_mips_instr.c
cd "$A" || exit 2
echo "== baseline: build/gxemul"
cmp -s "$B/$F" "$SEC/$F" && echo "build/ $F == SEC (part 1 CLEAN)" || echo "build/ $F DIFFERS from SEC"
[ "$B/gxemul" -nt "$B/$F" ] && echo "build/gxemul newer than its $F (part 2 FRESH)" || echo "build/gxemul NOT newer than its $F"
python3 -u main_table_cpus.py "$B/gxemul" head "$A/table_cpus_head_sessions" > "$A/table_head_cpus.out" 2>&1; tail -n 1 "$A/table_head_cpus.out"
echo "== v3 clone"
rm -rf "$C"; cp -a "$B" "$C" || exit 2
cmp -s "$C/$F" "$SEC/$F" || { echo "clone $F differs from SEC -- stop"; rm -rf "$C"; exit 2; }
echo "$F = the mipsprimundec v3 (main loop, apply_v3.py)" > "$C/.MUTANT"
python3 "$A/apply_v3.py" "$SEC/$F" "$C/$F" || { echo "apply FAILED"; rm -rf "$C"; exit 3; }
diff -u "$SEC/$F" "$C/$F" > "$A/v3.diff"; echo "v3 changed lines: $(grep -c '^[-+][^-+]' "$A/v3.diff")"
( cd "$C" && rm -f src/cpus/cpu_mips*.o && make -j4 > "$A/build_v3.log" 2>&1 ); echo "make rc=$?"
[ "$C/gxemul" -nt "$C/$F" ] && echo "binary FRESH" || { echo "binary STALE -- stop"; rm -rf "$C"; exit 4; }
grep -c -i 'warning' "$A/build_v3.log" | sed 's/^/build warnings: /'
python3 -u main_table_frozen.py "$C/gxemul" v3 "$A/table_v3_sessions" > "$A/table_v3.out" 2>&1; tail -n 1 "$A/table_v3.out"
python3 -u main_table_cpus.py "$C/gxemul" v3 "$A/table_cpus_v3_sessions" > "$A/table_v3_cpus.out" 2>&1; tail -n 1 "$A/table_v3_cpus.out"
python3 -u probe_frozen.py "$C/gxemul" v3 "$A/probe_v3_sessions" > "$A/probe_v3.out" 2>&1; tail -n 1 "$A/probe_v3.out"
grep -E '^MIPS_PRIMUNDEC_(RESULT|CONTROL|SYMPTOM|RED)' "$A/probe_v3.out"
rm -rf "$C"; [ ! -e "$C" ] && echo "clone removed"
echo RUN_V3_DONE
