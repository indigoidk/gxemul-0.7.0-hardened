#!/bin/bash
# Apply the PROPOSED fix in the scratch clone ONLY, measure E0-E6, then restore.
# Clone-local sentinel; restore verified by cmp against GXEMUL-SEC HEAD.
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
SECG=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
F=$T/src/devices/dev_footbridge.c
cd "$T" || exit 9

echo "### 0. baseline E-probe (pre-fix): must die at E0"
python3 -u "$D/opus_e.py" "$T/gxemul" "$T/out/arm_stub.bin" "PRE-FIX baseline 408accf" \
        > "$T/out/e_prefix.raw" 2>&1
tail -3 "$T/out/e_prefix.raw"
cp "$T/out/e_prefix.raw" "$D/e_prefix.raw"

echo "### 1. sentinel"
echo "$F : proposed n6 fix (delete fatal+exit in IRQ_ENABLE_SET read branch)" > "$T/.MUTANT"
cat "$T/.MUTANT"

echo "### 2. apply the proposed fix"
python3 - "$F" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
old = ("\t\t} else {\n"
       "\t\t\todata = d->irq_enable;\n"
       "\t\t\tfatal(\"[ WARNING: footbridge read from \"\n"
       "\t\t\t    \"ENABLE SET? ]\\n\");\n"
       "\t\t\texit(1);\n"
       "\t\t}\n")
new = ("\t\t} else {\n"
       "\t\t\t/*  #539: IRQEnable is a DOCUMENTED read-only\n"
       "\t\t\t    register (DC21285 Table 7-10, offset 188h).  */\n"
       "\t\t\todata = d->irq_enable;\n"
       "\t\t}\n")
n = s.count(old)
print("  occurrences of the exact ENABLE SET block: %d" % n)
if n != 1:
    sys.exit(9)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("  applied")
PYEOF
[ $? -eq 0 ] || { echo "PATCH FAILED"; exit 9; }
grep -n "IRQ_ENABLE_SET" -A 14 "$F" | head -20

echo "### 3. rebuild"
rm -f src/devices/dev_footbridge.o
make -j4 > out/build_fix.log 2>&1
echo "MAKE_RC=$?"
if [ gxemul -nt "$F" ]; then echo "  FRESH"; else echo "  *** STALE ***"; exit 9; fi

echo "### 4. post-fix E-probe"
python3 -u "$D/opus_e.py" "$T/gxemul" "$T/out/arm_stub.bin" "POST-FIX (proposed n6 diff)" \
        > "$T/out/e_postfix.raw" 2>&1
cp "$T/out/e_postfix.raw" "$D/e_postfix.raw"
cat "$T/out/e_postfix.raw"

echo "### 5. the existing sites probe on the post-fix build (does K1 red?)"
python3 -u "$T/out/footbridge_sites_probe.frozen.py" "$T/gxemul" "$T/out/arm_stub.bin" \
        > "$T/out/sites_postfix.raw" 2>&1
cp "$T/out/sites_postfix.raw" "$D/sites_postfix.raw"
grep -E "^(I1|K1|ROWS|FOOTBRIDGE)" "$T/out/sites_postfix.raw"
grep "kill arm said" "$T/out/sites_postfix.raw"
