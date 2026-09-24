#!/bin/bash
# Opus pass-2 kill table for #545 -- scratch clone /tmp/gxopusfbd5p2 ONLY.
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
ME=$ROOT/_scratchpad/fbd5/opus_p2_20260919
CLONE=/tmp/gxopusfbd5p2
OUT=$CLONE/out
echo "OPUS_P2_START $(date +%Y%m%d_%H%M%S)"
rm -rf "$CLONE"
cp -a "$ROOT/build" "$CLONE" || { echo CLONE FAILED; exit 2; }
mkdir -p "$OUT" "$CLONE/frozen"
cd "$CLONE" || exit 2
# baseline = HEAD + #545 patch; must equal SEC's working copy
git -C "$SEC" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c
python3 "$ROOT/_scratchpad/fbd5/impl/patch_fbd5.py" "$CLONE" > "$OUT/patch_fix.log" 2>&1 || { echo FIX PATCH FAILED; exit 3; }
if cmp -s src/devices/dev_footbridge.c "$SEC/src/devices/dev_footbridge.c"; then echo "BASELINE HEAD+patch == SEC working dev_footbridge.c"; else echo "BASELINE MISMATCH -- STOP"; exit 3; fi
cp src/devices/dev_footbridge.c "$OUT/dev_footbridge.FIX.c"
for f in footbridge_sites_probe.py fbpending_drain_probe.py fbpending_witness.py diff_footbridge.c; do cp "$SEC/regress/$f" "$CLONE/frozen/$f"; done
md5sum "$CLONE"/frozen/* | sed 's/^/FROZEN /'
printf '\0\0\0\0' > "$OUT/stub.bin"
echo "opus p2 table $(date) -- dev_footbridge.c mutated; restore = HEAD + patch_fbd5.py, rebuild, cmp vs SEC" > "$CLONE/.MUTANT"
build() {
    rm -f src/devices/dev_footbridge.o gxemul
    make -j4 > "$OUT/build_$1.log" 2>&1; rc=$?
    if [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ]; then fresh=FRESH; else fresh=STALE; fi
    cp gxemul "$OUT/gxemul_$1" 2>/dev/null
    echo "BUILD_$1 rc=$rc $fresh $(md5sum gxemul 2>/dev/null | cut -c1-8)"
    [ "$fresh" = FRESH ] || { echo "BUILD $1 NOT FRESH -- STOP"; exit 4; }
}
runsites() {
    python3 -u "${3:-$CLONE/frozen/footbridge_sites_probe.py}" "$2" "$OUT/stub.bin" > "$OUT/sites_$1.log" 2>&1
    echo "SITES_$1 $(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)|^FOOTBRIDGE_SITES_CONTROL' "$OUT/sites_$1.log" | tr '\n' ' ') red: $(grep -E ' FAIL$' "$OUT/sites_$1.log" | awk '{print $1}' | tr '\n' ',') $(tail -1 "$OUT/sites_$1.log")"
}
rundiff() {
    ( cd "$CLONE/frozen" && gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -I"$CLONE/src" -I"$CLONE/src/include" -I"$CLONE/src/include/thirdparty" -I"$CLONE/regress" \
        -o "$OUT/diff_$1" ./diff_footbridge.c -lm > "$OUT/diffc_$1.log" 2>&1 ); crc=$?
    if [ $crc -ne 0 ]; then echo "DIFF_$1 COMPILE rc=$crc"; return; fi
    "$OUT/diff_$1" > "$OUT/diff_$1.log" 2>&1; rrc=$?
    echo "DIFF_$1 rc=$rrc $(grep -E 'rows, |DIFF_FOOTBRIDGE_' "$OUT/diff_$1.log" | tr '\n' ' ') red: $(grep -E '^  FAIL ' "$OUT/diff_$1.log" | cut -c9-70 | tr '\n' '|' | cut -c1-300)"
}
build FIX
runsites FIX "$OUT/gxemul_FIX"
rundiff FIX
for M in A1 A2 A3 B1 B2 B3 C1 C2 D1 D2 G1 G2; do
    cp "$OUT/dev_footbridge.FIX.c" src/devices/dev_footbridge.c
    python3 "$ME/mkmut_p2.py" "$CLONE" $M > "$OUT/mut_$M.log" 2>&1 || { echo "$M DID NOT APPLY"; cat "$OUT/mut_$M.log"; continue; }
    diff "$OUT/dev_footbridge.FIX.c" src/devices/dev_footbridge.c > "$OUT/mut_$M.diff"
    build $M
    runsites $M "$OUT/gxemul_$M"
    rundiff $M
done
# harness mutants on the FIX binary
for H in R0 M13 M13q; do
    python3 "$ME/hmut_p2.py" "$CLONE/frozen/footbridge_sites_probe.py" "$OUT/sites_$H.py" $H > /dev/null
    runsites $H "$OUT/gxemul_FIX" "$OUT/sites_$H.py"
    grep -E '^(H2|I1) |arm Q' "$OUT/sites_$H.log" | sed "s/^/  $H: /"
done
# restore
git -C "$SEC" show HEAD:src/devices/dev_footbridge.c > src/devices/dev_footbridge.c
python3 "$ROOT/_scratchpad/fbd5/impl/patch_fbd5.py" "$CLONE" > "$OUT/patch_restore.log" 2>&1
build RESTORED
if cmp -s src/devices/dev_footbridge.c "$SEC/src/devices/dev_footbridge.c" && [ gxemul -nt src/devices/dev_footbridge.c ]; then
    rm -f "$CLONE/.MUTANT"; echo "RESTORE OK: source == SEC working copy (HEAD+#545), binary fresh $(md5sum gxemul | cut -c1-8), sentinel cleared"
else echo "RESTORE INCOMPLETE -- sentinel LEFT"; fi
echo "OPUS_P2_DONE $(date +%Y%m%d_%H%M%S)"
