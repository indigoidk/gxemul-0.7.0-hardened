#!/bin/bash
G=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$G/GXEMUL-SEC; F=src/devices/dev_pcc2.c; T=/tmp/gxfable501r; OUT=/tmp/f501r
A=$SEC/regress/artifacts/pcc2defaultkill/killtable4_20260905
echo "=== clone end state ==="
cmp "$T/$F" "$SEC/$F" && echo "clone $F cmp CLEAN vs SEC"
[ -e "$T/.MUTANT" ] && echo "SENTINEL STILL PRESENT" || echo "no .MUTANT sentinel in clone"
[ "$T/gxemul" -nt "$T/$F" ] && echo "clone binary NEWER than source (restore rebuild landed)" || echo "clone binary OLDER than source"
grep -c 'exit(1)' "$T/$F" "$SEC/$F"
echo "=== project trees untouched? (mtimes must predate 13:12) ==="
ls -la --time-style=+%H:%M:%S $G/build/gxemul $G/build/$F $G/est/$F $G/build-asan/$F $G/build-asan/gxemul 2>&1 | awk '{print $6, $7}'
ls $G/build/.MUTANT $G/build-asan/.MUTANT 2>&1 | grep -v 'No such' || echo "no sentinels in build/ or build-asan/"
echo "=== red lists: my FABLE_MEXIT vs archived M_EXIT ==="
grep -m1 PCC2D_RED "$OUT/FABLE_MEXIT.out" > /tmp/f501r/my_red.txt
grep -m1 PCC2D_RED "$A/M_EXIT.out" > /tmp/f501r/arch_red.txt
cmp /tmp/f501r/my_red.txt /tmp/f501r/arch_red.txt && echo "RED LIST IDENTICAL to archived M_EXIT (39 rows)"
echo "my red count: $(tr ',' '\n' < /tmp/f501r/my_red.txt | wc -l)"
echo "=== row-by-row got columns: mine vs archived (BASE and M_EXIT), ignoring the binary-path header ==="
diff <(grep -vE '^pcc2defaultkill DETECTOR' "$OUT/FABLE_BASE.out") <(grep -vE '^pcc2defaultkill DETECTOR' "$A/BASE.out") && echo "BASE rows byte-identical to archived BASE.out"
diff <(grep -vE '^pcc2defaultkill DETECTOR' "$OUT/FABLE_MEXIT.out") <(grep -vE '^pcc2defaultkill DETECTOR' "$A/M_EXIT.out") && echo "M_EXIT rows byte-identical to archived M_EXIT.out"
echo "=== gate-anchor replay on MY logs: the gate's own count pattern per name ==="
cnt(){ grep -ac -- "$2" "$1"; }
for f in FABLE_BASE FABLE_MEXIT; do ok=0; red=0; n=0; while read v; do c=$(cnt "$OUT/$f.out" "^$v  .*ok$"); n=$((n+1)); [ "$c" = 1 ] && ok=$((ok+1)) || red=$((red+1)); done < /tmp/probe_names.txt; echo "$f: per-row checks green=$ok red=$red of $n;  emitted=$(( $(cnt $OUT/$f.out ' ok$') + $(cnt $OUT/$f.out ' FAIL$') )) green=$(cnt $OUT/$f.out ' ok$') redlines=$(cnt $OUT/$f.out ' FAIL$')"; done
echo "=== copy my outputs beside FINDINGS (durable) ==="
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/regress_501_fable
cp "$OUT/FABLE_BASE.out" "$OUT/FABLE_MEXIT.out" "$OUT/build_BASE.log" "$OUT/build_M_EXIT.log" "$OUT/build_restore.log" "$D/" && ls -la "$D"
tail -2 "$OUT/build_M_EXIT.log"
