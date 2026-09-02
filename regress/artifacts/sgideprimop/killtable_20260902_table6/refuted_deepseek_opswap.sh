#!/bin/bash
#  Is deepseek's pass-7 mutant real?  It proposes swapping the n25-LINE session's
#  op store from LINE to RECT and claims a clean sweep, reasoning that the
#  XFER_EN guard "fires for any op when drawmode is set".
#
#  READING SAYS OTHERWISE: that guard is INSIDE `case DE_PRIM_LINE:', so a RECT op
#  never reaches it and `n25 line' should red at 0 instead of 1.  glm's mutant was
#  the SAME SHAPE on the drawmode-CLEAR session, where no diagnostic fires either
#  way -- and that one really did escape.
#
#  Same shape, different session, opposite prediction.  MEASURE IT: I have twice
#  tonight had a confident reading overturned, and once nearly dismissed a correct
#  seat finding on a broken mutator.
#
#  PREDICTION, written before the run: `n25 line' reds (0 want 1), 40/41.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/ds_mutant
rm -rf "$W"; mkdir -p "$W"
cp "$SEC/regress/sgi_de_primop_probe.py" "$W/probe.py"
cp "$SEC/regress/sgi_de_primop_probe.py" "$W/orig.py"
cp "$SEC/regress/dummy_kernel.bin" "$W/" 2>/dev/null

python3 - "$W/probe.py" <<'PYEOF'
import io, sys
P = sys.argv[1]
s = io.open(P, encoding='utf-8').read()
#  the n25-LINE session: drawmode store, THEN a 0x01000000 primitive store.
a = 'store(A, DE + PRIM_START, val="0x01000000")'
n = s.count(a)
print("  LINE-op store sites: %d" % n)
assert n == 1, "expected exactly one"
s = s.replace(a, 'store(A, DE + PRIM_START, val="0x03000000")')
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print("  swapped the n25-LINE session's op LINE -> RECT")
PYEOF

echo "  --- proof the mutant is in the file (blank = mutator did nothing) ---"
diff "$W/orig.py" "$W/probe.py" | sed 's/^/    /'

cd "$W" || exit 9
timeout 900 python3 -u probe.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul dsmut > "$W/out.txt" 2>&1
echo
echo "  --- the n25 rows under deepseek's mutant ---"
grep -E '^n25' "$W/out.txt"
grep -a OPUS500_RESULT "$W/out.txt"
echo
echo "  --- every RED ---"
grep -a ' FAIL$' "$W/out.txt" | cut -c1-16 | sed 's/^/    /'
