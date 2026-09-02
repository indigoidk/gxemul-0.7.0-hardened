#!/bin/bash
#  NEGATIVE CONTROL for the new `xlatch pre' row.
#
#  The row reads 6 on the fixed probe.  A check that cannot fail is worse than no
#  check, so this proves it FAILS on the defect it exists to catch: restore the
#  ORIGINAL (wrong) window offsets and require `xlatch pre' to read 0 and go RED.
#
#  Run against a COPY in /tmp.  The repo probe is never edited by this script.
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
W=/tmp/negctl_pre
rm -rf "$W"; mkdir -p "$W"
cp "$SEC/regress/sgi_de_primop_probe.py" "$W/probe.py"
cp "$SEC/regress/dummy_kernel.bin" "$W/" 2>/dev/null

python3 - "$W/probe.py" <<'PYEOF'
import io, sys
P = sys.argv[1]
s = io.open(P, encoding='utf-8').read()
#  put the WRONG offsets back: the CRIME_RE_* constants used as device offsets
pairs = [("RE + 0x000,", "RE + 0x1000,"), ("RE + 0x200,", "RE + 0x1200,"),
         ("RE + 0x400,", "RE + 0x1400,"), ("RE + 0x600,", "RE + 0x1600,"),
         ("RE + 0x700,", "RE + 0x1700,"), ("RE + 0x780,", "RE + 0x1780,")]
for a, b in pairs:
    assert s.count(a) == 1, (a, s.count(a))
    s = s.replace(a, b)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print("  reverted all six offsets to the WRONG (pre-fix) values")
PYEOF

cd "$W" || exit 9
timeout 900 python3 -u probe.py /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul negctl > "$W/out.txt" 2>&1
echo
echo "  --- the control rows under the REVERTED offsets ---"
grep -E '^xlatch (pre|all)' "$W/out.txt"
grep -a OPUS500_RESULT "$W/out.txt"
echo
if grep -qE '^xlatch pre +0 +6 .*FAIL$' "$W/out.txt"; then
    echo "  *** NEGATIVE CONTROL PASSES: xlatch pre reads 0 and goes RED on the defect. ***"
else
    echo "  *** NEGATIVE CONTROL FAILED -- the row does NOT catch its own defect. ***"
    grep -E '^xlatch pre' "$W/out.txt"
fi
echo "  (the repo probe was not touched by this script)"
