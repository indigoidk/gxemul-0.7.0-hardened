#!/bin/bash
# Two mutants ON TOP OF the proposed fix, in the scratch clone only.
# Me = the fixed file (already in place from s_fix.sh).
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
F=$T/src/devices/dev_footbridge.c
cd "$T" || exit 9
cp "$F" "$T/out/fb_fixed.c"

mut () {   # $1 = tag ; $2 = python edit script path
  cp "$T/out/fb_fixed.c" "$F"
  python3 - "$F" < "$2" || { echo "PATCH FAILED $1"; return 9; }
  rm -f src/devices/dev_footbridge.o
  make -j4 > "out/build_$1.log" 2>&1
  echo "  MAKE_RC=$? ; fresh=$( [ gxemul -nt "$F" ] && echo yes || echo NO )"
  python3 -u "$D/opus_e.py" "$T/gxemul" "$T/out/arm_stub.bin" "MUTANT $1" \
          > "out/e_$1.raw" 2>&1
  cp "out/e_$1.raw" "$D/e_$1.raw"
  grep -E "^(A1|E[0-6]) |status=|diagnostics" "out/e_$1.raw"
}

cat > "$T/out/mut_e.py" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
old = ("\t\t\t/*  #539: IRQEnable is a DOCUMENTED read-only\n"
       "\t\t\t    register (DC21285 Table 7-10, offset 188h).  */\n"
       "\t\t\todata = d->irq_enable;\n")
new = ("\t\t\todata = d->irq_enable;\n"
       "\t\t\tfatal(\"[ WARNING: footbridge read from \"\n"
       "\t\t\t    \"ENABLE SET? ]\\n\");\n")
assert s.count(old) == 1, s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("  mutant (e): fatal() kept, exit(1) gone")
PYEOF

cat > "$T/out/mut_j.py" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
old = ("\tcase IRQ_ENABLE_SET:\n"
       "\t\tif (writeflag == MEM_WRITE) {\n"
       "\t\t\td->irq_enable |= idata;\n"
       "\t\t\tif (d->irq_status & d->irq_enable)\n")
new = ("\tcase IRQ_ENABLE_SET:\n"
       "\t\tif (writeflag == MEM_WRITE) {\n"
       "\t\t\td->irq_enable |= idata;\n"
       "\t\t\tif (d->irq_status | d->irq_enable)\n")
assert s.count(old) == 1, s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("  mutant (j): assert condition & -> |")
PYEOF

echo "########## MUTANT (e): keep fatal(), delete only exit(1) ##########"
mut e "$T/out/mut_e.py"
echo "  --- and the existing sites probe (I1 reads 'not L[fatals]') ---"
python3 -u "$T/out/footbridge_sites_probe.frozen.py" "$T/gxemul" "$T/out/arm_stub.bin" \
        > "out/sites_e.raw" 2>&1
cp "out/sites_e.raw" "$D/sites_e.raw"
grep -E "^(I1|K1|ROWS|FOOTBRIDGE)" "out/sites_e.raw"

echo
echo "########## MUTANT (j): assert on irq_status | irq_enable ##########"
mut j "$T/out/mut_j.py"

echo
echo "########## RESTORE ##########"
cp "$T/out/fb_fixed.c" "$F"    # back to fixed, then to HEAD
git -C /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC show HEAD:src/devices/dev_footbridge.c > "$F"
if cmp -s "$F" "$T/out/fb_head.c"; then
  echo "  SOURCE RESTORED: cmp clean vs GXEMUL-SEC HEAD:src/devices/dev_footbridge.c"
else
  echo "  *** RESTORE FAILED ***"; exit 9
fi
rm -f src/devices/dev_footbridge.o
make -j4 > out/build_restore.log 2>&1
echo "  MAKE_RC=$?"
if [ gxemul -nt "$F" ]; then echo "  BINARY REBUILT AND FRESH -- two-part clearance complete"; rm -f "$T/.MUTANT"; echo "  sentinel cleared"; else echo "  *** STALE -- SENTINEL KEPT ***"; exit 9; fi
echo "  confirm baseline behaviour is back:"
python3 -u "$T/out/footbridge_sites_probe.frozen.py" "$T/gxemul" "$T/out/arm_stub.bin" \
        > "out/sites_restored.raw" 2>&1
cp "out/sites_restored.raw" "$D/sites_restored.raw"
grep -E "^(K1|ROWS|FOOTBRIDGE)" "out/sites_restored.raw"
