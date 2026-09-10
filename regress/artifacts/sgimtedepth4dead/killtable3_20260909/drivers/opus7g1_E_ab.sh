#!/bin/bash
# Stage E: preserve the M_tlbA binary; build+measure M_tlbAB.  Sentinel stays in place throughout.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1
F=src/devices/dev_sgi_re.c
OUT=$CL/logs
echo "=== STAGE E  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "-- sentinel still present? --"; cat "$CL/.MUTANT" | head -c 120; echo

echo "-- preserve the M_tlbA binary before rebuilding over it --"
cp "$CL/gxemul" "$CL/bin_M_tlbA" && echo "bin_M_tlbA md5 $(md5sum $CL/bin_M_tlbA | cut -c1-32)"

echo "-- restore from SEC, then apply M_tlbAB --"
cp "$SEC/$F" "$CL/$F" || exit 9
cmp -s "$CL/$F" "$SEC/$F" && echo "restored to SEC baseline OK" || { echo "E-FAIL restore"; exit 9; }
echo "/tmp/gxopus7g1/.MUTANT: src/devices/dev_sgi_re.c  M_tlbAB: 'if (depth == 32)' -> 'if (depth == 32 && dst_tlb != MTE_TLB_C)' at :1519.  RESTORE FROM $SEC/$F." > "$CL/.MUTANT"

python3 - "$CL/$F" <<'PYEOF'
import sys
p = sys.argv[1]
old = "if (depth == 32) {"
new = "if (depth == 32 && dst_tlb != MTE_TLB_C) {"
lines = open(p).read().split("\n")
hits = [i for i, l in enumerate(lines) if old in l]
print("OCCURRENCES: %d at %s" % (len(hits), [i+1 for i in hits]))
if len(hits) != 1: print("E-FAIL"); sys.exit(9)
lines[hits[0]] = lines[hits[0]].replace(old, new)
open(p, "w").write("\n".join(lines))
print("NEW LINE %d: %s" % (hits[0]+1, lines[hits[0]]))
PYEOF
[ $? -ne 0 ] && { echo "E-FAIL mutate"; exit 9; }

diff "$SEC/$F" "$CL/$F" > /tmp/gxopus7g1_M_tlbAB.diff 2>&1
cat /tmp/gxopus7g1_M_tlbAB.diff
NCH=$(grep -cE '^[<>]' /tmp/gxopus7g1_M_tlbAB.diff)
[ "$NCH" != "2" ] && { echo "E-FAIL: not a one-line edit ($NCH)"; exit 9; }
echo "ONE_LINE_EDIT=confirmed"

cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/gxopus7g1_buildE.log 2>&1; echo "MAKE_RC=$?"
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then echo "FRESHNESS=OK"; else echo "E-FAIL freshness"; exit 9; fi
cp "$CL/gxemul" "$CL/bin_M_tlbAB"
echo "bin_M_tlbAB md5 $(md5sum $CL/bin_M_tlbAB | cut -c1-32)"

cd "$CL/probe" || exit 9
python3 -u ./sgi_mte_fill_probe.py "$CL/gxemul" M_tlbAB > "$OUT/M_tlbAB.raw" 2>&1
echo "PROBE_RC=$?"
tail -1 "$OUT/M_tlbAB.raw"; grep -E '^MTEFILL_RESULT=' "$OUT/M_tlbAB.raw"
echo "RED ROWS: $(grep -c 'FAIL$' $OUT/M_tlbAB.raw)"; grep 'FAIL$' "$OUT/M_tlbAB.raw"
echo "-- row diff vs BASE --"; diff <(tail -n +2 "$OUT/BASE.raw") <(tail -n +2 "$OUT/M_tlbAB.raw") && echo "IDENTICAL_TO_BASE (rows)"
echo "STAGE_E_DONE"
