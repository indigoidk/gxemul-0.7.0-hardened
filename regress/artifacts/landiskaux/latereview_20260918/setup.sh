#!/bin/bash
#  setup.sh -- build a PRE-FIX and a POST-FIX gxemul in /tmp, never touching
#  GXEMUL-SEC/ or build/.  Both clones come from build/ (relocatable: its
#  Makefiles carry only relative paths -- checked before this was written).
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
BLD=/mnt/c/DocumentNoSnc/CC/GXEMUL/build
B=/tmp/gxopus_lax_base
F=/tmp/gxopus_lax_fix
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918

rm -rf "$B" "$F"
cp -a "$BLD" "$B" || { echo "CP_FAILED"; exit 2; }

#  (1) NAME THE BASELINE: every shared .c/.h in SEC/src must be byte-identical
#  in the clone.  The six est_divergence paths are SKIPPED, not compared --
#  build/ matches est/ there by record, and they are not on the landisk path.
DIV=$(grep -vE '^\s*(#|$)' "$SEC/tools/est_divergence.txt")
same=0; diff=0; miss=0; skip=0
cd "$SEC"
while IFS= read -r f; do
    if printf '%s\n' "$DIV" | grep -qxF "$f"; then skip=$((skip+1)); continue; fi
    if [ ! -e "$B/$f" ]; then miss=$((miss+1)); echo "MISSING_IN_CLONE $f"; continue; fi
    if cmp -s "$f" "$B/$f"; then same=$((same+1)); else diff=$((diff+1)); echo "DIFFERS $f"; fi
done < <(find src -name '*.c' -o -name '*.h' | grep -v '/tmp_' | sort)
echo "BASELINE_CMP same=$same differ=$diff missing=$miss skipped_divergence=$skip"

build() {
    local T="$1"
    cd "$T" || return 9
    rm -f src/devices/dev_wdc.o
    make > "$T.build.log" 2>&1
    local rc=$?
    echo "MAKE_RC[$T]=$rc"
    if [ "$T/gxemul" -nt "$T/src/devices/dev_wdc.c" ] && [ -e "$T/src/devices/dev_wdc.o" ]; then
        echo "FRESH_OK[$T] $(ls -la --time-style=full-iso "$T/gxemul" | awk '{print $6, $7}')"
    else
        echo "***STALE_OR_FAILED[$T]***"; tail -20 "$T.build.log"
    fi
}

#  (2) rebuild the baseline IN THE CLONE, so its freshness is proven here.
build "$B"

#  (3) the post-fix clone: the brief's one `case`, inserted after IQ80321's
#  break (so it is the LAST arm and its own break is not load-bearing today).
cp -a "$B" "$F"
python3 - "$F/src/devices/dev_wdc.c" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
anchor = ("\tcase MACHINE_IQ80321:\n"
          "\t\talt_status_addr = devinit->addr + 0x402;\n"
          "\t\tbreak;\n")
assert s.count(anchor) == 1, "anchor count %d" % s.count(anchor)
fix = ("\tcase MACHINE_LANDISK:\n"
       "\t\talt_status_addr = devinit->addr + 0x16 * devinit->addr_mult;\n"
       "\t\tbreak;\n")
s = s.replace(anchor, anchor + fix)
open(p, "w").write(s)
print("FIX_APPLIED")
PYEOF
diff -u "$SEC/src/devices/dev_wdc.c" "$F/src/devices/dev_wdc.c" > "$OUT/fix.diff"
echo "FIX_DIFF_LINES=$(grep -c '^[+-][^+-]' "$OUT/fix.diff")"
cat "$OUT/fix.diff"
build "$F"
cmp -s "$SEC/src/devices/dev_wdc.c" "$B/src/devices/dev_wdc.c" && echo "BASE_WDC_IS_SEC"
echo SETUP_DONE
