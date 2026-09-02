#!/bin/bash
#  NEGATIVE CONTROL for n25 rectset, take 2.  The first attempt had a backtick
#  inside a double-quoted echo and died at the reporting step -- and the run it
#  did complete came back 39/39, which means the mutant either did not apply or
#  does not do what the seat predicted.  BOTH are results and this script says
#  WHICH, by diffing the mutated probe against the original before running it.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/negctl_rectset2
rm -rf "$W"; mkdir -p "$W"
cp "$SEC/regress/sgi_de_primop_probe.py" "$W/probe.py"
cp "$SEC/regress/sgi_de_primop_probe.py" "$W/orig.py"
cp "$SEC/regress/dummy_kernel.bin" "$W/" 2>/dev/null

python3 - "$W/probe.py" <<'PYEOF'
import io, sys
P = sys.argv[1]
s = io.open(P, encoding='utf-8').read()
a = "session(store(A, DE + DRAWMODE, val=XFER_EN)"
n = s.count(a)
print("  drawmode-store sites found: %d" % n)
assert n == 2, "expected 2"
i = s.index(a)
s = s[:i] + 'session(store(A, DE + DRAWMODE, val="0x03000000")' + s[i + len(a):]
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print("  swap applied to the FIRST (rectangle) site only")
PYEOF

echo "  --- proof the mutant is really in the file ---"
diff "$W/orig.py" "$W/probe.py" | sed 's/^/    /'
echo "  --- (a blank diff here means the mutator silently did nothing) ---"

cd "$W" || exit 9
timeout 900 python3 -u probe.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul negctl > "$W/out.txt" 2>&1
echo
echo "  --- the n25 rows under the swap ---"
grep -E '^n25' "$W/out.txt"
grep -a OPUS500_RESULT "$W/out.txt"
echo
echo "  --- what the rectangle session emitted ---"
grep -c 'STARTING DRAWING COMMAND' "$W/out.txt"
