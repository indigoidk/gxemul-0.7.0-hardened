#!/bin/bash
# #545 repair R3 (2026-09-23): M9 on the FINAL instrument.  Grok 4.7's records audit (verify_20260923) found that
# cl545_draft.md's "every one of the 49 is detected" rests, for M9, on TABLE2's 36-row probe (33/36, red N1,N2,N0);
# the probe gained the NO row and header corrections after that, and M9 was never re-run (F2_FINDINGS G27).
# This measures M9 against the SHIPPED 37-row footbridge_sites_probe.py (frozen copy), FIX first as the control.
# PREDICTION, written before the run: FIX 37/37; M9 33/37 red N1 (2 lines), N2 (0), N0 (4 distinct), NO (order).
# Scratch clone only; sentinel; restore from GXEMUL-SEC; cmp + freshness before the sentinel is cleared.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
I=$R/_scratchpad/fbd5/impl
OUT=$I/r3_m9_20260923
mkdir -p "$OUT"
log() { echo "$*" | tee -a "$OUT/R3.log"; }
log "R3_START $(date '+%F %T')  SEC dev_footbridge.c md5 $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)  probe md5 $(md5sum $SEC/regress/footbridge_sites_probe.py | cut -c1-8)"
log "PREDICTION: FIX 37/37; M9 33/37 red N1 N2 N0 NO"
C=/tmp/gxfbd5m9
rm -rf "$C"; cp -a "$R/build" "$C" || { log "CLONE FAILED"; exit 2; }
mkdir -p "$C/frozen" "$C/out"
cp "$SEC/regress/footbridge_sites_probe.py" "$C/frozen/"
cmp -s "$C/src/devices/dev_footbridge.c" "$SEC/src/devices/dev_footbridge.c" && log "BASELINE clone dev_footbridge.c == SEC" || { log "BASELINE MISMATCH -- STOP"; exit 3; }
cp "$C/src/devices/dev_footbridge.c" "$C/out/FIX.c"
printf '\0\0\0\0' > "$C/out/stub.bin"
echo "#545 R3 M9 -- restore dev_footbridge.c from GXEMUL-SEC, rebuild" > "$C/.MUTANT"
cd "$C" || exit 2
build() { rm -f src/devices/dev_footbridge.o gxemul; make -j4 > "$C/out/build_$1.log" 2>&1; rc=$?
          if [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ]; then log "BUILD_$1 rc=$rc FRESH $(md5sum gxemul | cut -c1-8)"; cp gxemul "$C/out/gxemul_$1"; return 0; fi
          log "BUILD_$1 NOT FRESH -- STOP"; exit 4; }
sites() { python3 -u "$C/frozen/footbridge_sites_probe.py" "$C/out/gxemul_$1" "$C/out/stub.bin" > "$OUT/sites_$1.log" 2>&1
          log "$(printf 'SITES %-4s %s  red: %s' "$1" "$(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)' "$OUT/sites_$1.log" | tr '\n' ' ')" "$(grep -E ' FAIL$' "$OUT/sites_$1.log" | awk '{print $1}' | tr '\n' ',')")"; }
build FIX
sites FIX
cp "$C/out/FIX.c" src/devices/dev_footbridge.c
python3 "$I/mkmut_fbd5.py" "$C" M9 > "$C/out/mkmut_M9.log" 2>&1 || { log "M9 DID NOT APPLY"; cat "$C/out/mkmut_M9.log" >> "$OUT/R3.log"; exit 5; }
diff "$C/out/FIX.c" src/devices/dev_footbridge.c > "$OUT/M9.diff"
log "M9 applied: $(grep -c '^[<>]' "$OUT/M9.diff") changed lines"
build M9
sites M9
cp "$SEC/src/devices/dev_footbridge.c" src/devices/dev_footbridge.c
build RESTORED
if cmp -s src/devices/dev_footbridge.c "$SEC/src/devices/dev_footbridge.c" && [ gxemul -nt src/devices/dev_footbridge.c ]; then
    rm -f "$C/.MUTANT"; log "RESTORED: cmp == SEC, binary fresh ($(md5sum gxemul | cut -c1-8)), sentinel cleared"
else
    log "RESTORE NOT VERIFIED -- sentinel LEFT IN PLACE"
fi
log "R3_DONE $(date '+%F %T')"
