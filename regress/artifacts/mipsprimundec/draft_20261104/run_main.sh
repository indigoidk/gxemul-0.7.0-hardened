#!/bin/bash
#  run_main.sh -- the mipsprimundec per-word table on (1) build/gxemul (HEAD's MIPS path) and (2) the DRAFT, applied from the m_mpu
#  seat's saved draft.diff in the main loop's own clone /tmp/gxmain_mpu (removed afterwards); plus the witness probe on the draft.
set -u
M=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/opus_20261104/m_mpu
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; C=/tmp/gxmain_mpu; F=src/cpus/cpu_mips_instr.c
cd "$M" || exit 2
python3 -u main_table.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul head "$M/main_sessions" > "$M/table_head.out" 2>&1; tail -1 "$M/table_head.out"
rm -rf "$C"; cp -a /mnt/c/DocumentNoSnc/cc/GXEMUL/build "$C" || exit 2
cmp -s "$C/$F" "$SEC/$F" || { echo "clone $F differs from SEC -- stop"; exit 2; }
echo "$F = the mipsprimundec DRAFT (main loop, from m_mpu/draft.diff)" > "$C/.MUTANT"
( cd "$C" && patch -s "$F" < "$M/draft.diff" ) || { echo "patch FAILED"; exit 3; }
diff -u "$SEC/$F" "$C/$F" | grep -c '^[-+][^-+]' | sed 's/^/draft changed lines: /'
( cd "$C" && rm -f src/cpus/cpu_mips*.o && make -j4 > "$M/build_main_draft.log" 2>&1 ); echo "make rc=$?"
[ "$C/gxemul" -nt "$C/$F" ] && echo "binary FRESH" || { echo "binary STALE -- stop"; exit 4; }
python3 -u main_table.py "$C/gxemul" draft "$M/main_sessions" > "$M/table_draft.out" 2>&1; tail -1 "$M/table_draft.out"
python3 -u "$SEC/regress/mips_primundec_probe.py" "$C/gxemul" draft "$M/probe_draft_sessions" > "$M/probe_draft.out" 2>&1
grep -E '^MIPS_PRIMUNDEC_(RESULT|CONTROL|SYMPTOM|RED)' "$M/probe_draft.out"
rm -rf "$C" && echo "clone removed"
echo RUN_MAIN_DONE
