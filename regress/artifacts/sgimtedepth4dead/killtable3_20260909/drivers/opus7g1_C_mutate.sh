#!/bin/bash
# Stage C: sentinel FIRST, then apply M_tlbA, verify exactly one line changed, rebuild.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus7g1
F=src/devices/dev_sgi_re.c
echo "=== STAGE C  $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

echo "-- SENTINEL DROPPED BEFORE ANY MUTATION --"
echo "/tmp/gxopus7g1/.MUTANT: src/devices/dev_sgi_re.c  M_tlbA: 'if (depth == 32)' -> 'if (depth == 32 && dst_tlb == MTE_TLB_A)' at :1519.  RESTORE FROM $SEC/$F (NEVER from a local backup), then rm src/devices/dev_sgi_re.o and rebuild, then cmp vs SEC AND check [ gxemul -nt $F ] before clearing this file." > "$CL/.MUTANT"
cat "$CL/.MUTANT"

echo "-- APPLY M_tlbA --"
python3 - "$CL/$F" <<'PYEOF'
import sys
p = sys.argv[1]
old = "if (depth == 32) {"
new = "if (depth == 32 && dst_tlb == MTE_TLB_A) {"
lines = open(p).read().split("\n")
hits = [i for i, l in enumerate(lines) if old in l]
print("OCCURRENCES of %r: %d at 1-based lines %s" % (old, len(hits), [i+1 for i in hits]))
if len(hits) != 1:
    print("C-FAIL: expected exactly one occurrence"); sys.exit(9)
lines[hits[0]] = lines[hits[0]].replace(old, new)
open(p, "w").write("\n".join(lines))
print("NEW LINE %d: %s" % (hits[0]+1, lines[hits[0]]))
PYEOF
[ $? -ne 0 ] && { echo "C-FAIL: mutation script failed"; exit 9; }

echo "-- VERIFY EXACTLY ONE LINE CHANGED vs SEC --"
diff "$SEC/$F" "$CL/$F" > /tmp/gxopus7g1_M_tlbA.diff 2>&1
echo "DIFF:"; cat /tmp/gxopus7g1_M_tlbA.diff
NCH=$(grep -cE '^[<>]' /tmp/gxopus7g1_M_tlbA.diff)
echo "CHANGED_LINE_MARKERS=$NCH of $(grep -c '' /tmp/gxopus7g1_M_tlbA.diff) diff lines  (want 2: one '<', one '>')"
[ "$NCH" != "2" ] && { echo "C-FAIL: not a one-line edit"; exit 9; }

echo "-- REBUILD --"
cd "$CL" || exit 9
rm -f src/devices/dev_sgi_re.o
make -j4 > /tmp/gxopus7g1_buildC.log 2>&1; MAKE_RC=$?
echo "MAKE_RC=$MAKE_RC   (not trusted alone)"
tail -2 /tmp/gxopus7g1_buildC.log
if [ -x "$CL/gxemul" ] && [ "$CL/gxemul" -nt "$CL/$F" ]; then
  echo "FRESHNESS=OK  binary NEWER than mutated source"
else
  echo "FRESHNESS=FAIL"; ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"; exit 9
fi
echo "MUTANT_BIN_MD5: $(md5sum $CL/gxemul | cut -c1-32)"
ls -la --time-style=full-iso "$CL/gxemul" "$CL/$F"
echo "STAGE_C_DONE"
