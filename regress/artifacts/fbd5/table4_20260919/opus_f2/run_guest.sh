#!/bin/bash
# Opus f2: GUEST half -- the shipped footbridge_sites_probe.py (frozen) vs FIX + f2 mutants, in /tmp/gxopusf2 (cp -a of build/).
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL; SEC=$R/GXEMUL-SEC; D=$R/_scratchpad/fbd5/opus_f2_20260919; OUT=$D/guest
mkdir -p "$OUT"; : > "$D/GUEST.log"
log() { echo "$*" | tee -a "$D/GUEST.log"; }
C=/tmp/gxopusf2
rm -rf "$C"; cp -a "$R/build" "$C" || { log "CLONE FAILED"; exit 2; }
mkdir -p "$C/frozen" "$C/out"
cp "$SEC/regress/footbridge_sites_probe.py" "$D/mkmut_f2.py" "$C/frozen/"
cp "$SEC/src/devices/dev_footbridge.c" "$C/out/FIX.c"
echo "opus f2 guest -- restore dev_footbridge.c from SEC, rebuild" > "$C/.MUTANT"
cp "$C/out/FIX.c" "$C/src/devices/dev_footbridge.c"
printf '\0\0\0\0' > "$C/out/stub.bin"
log "GUEST_START $(date '+%F %T') SEC md5 $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8) probe md5 $(md5sum $C/frozen/footbridge_sites_probe.py | cut -c1-8)"
cd "$C" || exit 2
build() { rm -f src/devices/dev_footbridge.o gxemul; make -j4 > "$C/out/build_$1.log" 2>&1; rc=$?
          if [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ]; then log "BUILD_$1 rc=$rc FRESH $(md5sum gxemul | cut -c1-8)"; cp gxemul "$C/out/gxemul_$1"; return 0; fi
          log "BUILD_$1 NOT FRESH -- STOP"; exit 4; }
for M in FIX "$@"; do
    cp "$C/out/FIX.c" src/devices/dev_footbridge.c
    if [ $M != FIX ]; then python3 "$C/frozen/mkmut_f2.py" "$C" "$M" > /dev/null || { log "$M DID NOT APPLY"; continue; }
        diff "$C/out/FIX.c" src/devices/dev_footbridge.c > "$OUT/mut_$M.diff"; log "MUT $M diff lines: $(grep -c '^[<>]' "$OUT/mut_$M.diff")"; fi
    build "$M"
    python3 -u "$C/frozen/footbridge_sites_probe.py" "$C/out/gxemul_$M" "$C/out/stub.bin" > "$OUT/sites_$M.log" 2>&1
    log "$(printf 'SITES %-4s %s  red: %s' "$M" "$(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)' "$OUT/sites_$M.log" | tr '\n' ' ')" "$(grep -E ' FAIL$' "$OUT/sites_$M.log" | awk '{print $1}' | tr '\n' ',')")"
done
cp "$SEC/src/devices/dev_footbridge.c" src/devices/dev_footbridge.c
build RESTORED
cmp -s src/devices/dev_footbridge.c "$SEC/src/devices/dev_footbridge.c" && [ gxemul -nt src/devices/dev_footbridge.c ] && rm -f "$C/.MUTANT" && log "GUEST RESTORED (cmp == SEC, binary fresh), sentinel cleared"
log "GUEST_DONE $(date '+%F %T')"
