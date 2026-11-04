#!/bin/bash
#  run_v3b.sh -- the v3b ALTERNATIVE (apply_v3.py then apply_v3b.py: v3 plus LWC3/SWC3 as Reserved Instruction on ISA III, per two
#  local manuals), built in the main loop's own clone /tmp/gxmain_mpu3b (removed afterwards) and measured with frozen copies: the
#  five-CPU table (main_table_v3b.py: R4400, R3000, 5KE, 24KEc, R5000) and the witness probe.  The same five-CPU table also runs on
#  build/gxemul (HEAD) for the R5000 baseline.  Not a ruling: v3 stays the consensus carrier.  No project tree is written.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/mipsprimundec/v3_20261104
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build; C=/tmp/gxmain_mpu3b; F=src/cpus/cpu_mips_instr.c
cd "$A" || exit 2
echo "== baseline: build/gxemul (five CPUs)"
cmp -s "$B/$F" "$SEC/$F" && echo "build/ $F == SEC (part 1 CLEAN)" || echo "build/ $F DIFFERS from SEC"
[ "$B/gxemul" -nt "$B/$F" ] && echo "build/gxemul newer than its $F (part 2 FRESH)" || echo "build/gxemul NOT newer than its $F"
python3 -u main_table_v3b.py "$B/gxemul" head "$A/table_v3b_head_sessions" > "$A/table_head_5cpu.out" 2>&1; tail -n 1 "$A/table_head_5cpu.out"
echo "== v3b clone"
rm -rf "$C"; cp -a "$B" "$C" || exit 2
cmp -s "$C/$F" "$SEC/$F" || { echo "clone $F differs from SEC -- stop"; rm -rf "$C"; exit 2; }
echo "$F = the mipsprimundec v3b alternative (main loop, apply_v3.py + apply_v3b.py)" > "$C/.MUTANT"
python3 "$A/apply_v3.py" "$SEC/$F" "$C/$F.v3" && python3 "$A/apply_v3b.py" "$C/$F.v3" "$C/$F" && rm -f "$C/$F.v3" || { echo "apply FAILED"; rm -rf "$C"; exit 3; }
diff -u "$SEC/$F" "$C/$F" > "$A/v3b.diff"
echo "v3b diff: $(grep -c -E '^\+([^+]|$)' "$A/v3b.diff") added, $(grep -c -E '^-([^-]|$)' "$A/v3b.diff") deleted"
( cd "$C" && rm -f src/cpus/cpu_mips*.o && make -j4 > "$A/build_v3b.log" 2>&1 ); echo "make rc=$?"
[ "$C/gxemul" -nt "$C/$F" ] && echo "binary FRESH" || { echo "binary STALE -- stop"; rm -rf "$C"; exit 4; }
grep -c -i 'warning' "$A/build_v3b.log" | sed 's/^/build warnings: /'
python3 -u main_table_v3b.py "$C/gxemul" v3b "$A/table_v3b_sessions" > "$A/table_v3b.out" 2>&1; tail -n 1 "$A/table_v3b.out"
python3 -u probe_frozen.py "$C/gxemul" v3b "$A/probe_v3b_sessions" > "$A/probe_v3b.out" 2>&1; tail -n 1 "$A/probe_v3b.out"
grep -E '^MIPS_PRIMUNDEC_(RESULT|CONTROL|SYMPTOM|RED)' "$A/probe_v3b.out"
rm -rf "$C"; [ ! -e "$C" ] && echo "clone removed"
echo RUN_V3B_DONE
