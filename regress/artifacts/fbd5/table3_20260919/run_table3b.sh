#!/bin/bash
# #545 TABLE 3 -- the repaired detector (after pass 2) against EVERY mutant built so far, in scratch trees only.
#   A offline: the SHIPPED regress/diff_footbridge.c (149 rows) vs FIX + 34 mutants  (/tmp/fbd5x, a copy of SEC src)
#   B guest:   the SHIPPED footbridge_sites_probe.py (37 rows) + the two pending probes, in a clone of build/
#              (/tmp/gxfbd5c): FIX, Z9 (text swap, guest-only), M1b-M1e (exit reinstated per site)
# Frozen instruments, a sentinel per scratch tree, restore + cmp against GXEMUL-SEC, every build freshness-checked.
set -u
R=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$R/GXEMUL-SEC
I=$R/_scratchpad/fbd5/impl
OUT=$I/table3
mkdir -p "$OUT"
log() { echo "$*" | tee -a "$OUT/TABLE3.log"; }
log "TABLE3B_START (guest half, re-run after the 12:53 stop) $(date '+%F %T')  SEC dev_footbridge.c md5 $(md5sum $SEC/src/devices/dev_footbridge.c | cut -c1-8)"

# ---------------------------------------------------------------- B guest
C=/tmp/gxfbd5c
rm -rf "$C"; cp -a "$R/build" "$C" || { log "CLONE FAILED"; exit 2; }
mkdir -p "$C/frozen" "$C/out"
cp "$SEC/regress/footbridge_sites_probe.py" "$SEC/regress/fbpending_drain_probe.py" "$SEC/regress/fbpending_witness.py" "$C/frozen/"
cp "$SEC/src/devices/dev_footbridge.c" "$C/src/devices/dev_footbridge.c"; cp "$C/src/devices/dev_footbridge.c" "$C/out/FIX.c"
printf '\0\0\0\0' > "$C/out/stub.bin"
echo "#545 table3 B -- restore dev_footbridge.c from SEC, rebuild" > "$C/.MUTANT"
cd "$C" || exit 2
build() { rm -f src/devices/dev_footbridge.o gxemul; make -j4 > "$C/out/build_$1.log" 2>&1; rc=$?
          if [ -x gxemul ] && [ gxemul -nt src/devices/dev_footbridge.c ]; then log "BUILD_$1 rc=$rc FRESH $(md5sum gxemul | cut -c1-8)"; cp gxemul "$C/out/gxemul_$1"; return 0; fi
          log "BUILD_$1 NOT FRESH -- STOP"; exit 4; }
sites() { python3 -u "$C/frozen/footbridge_sites_probe.py" "$C/out/gxemul_$1" "$C/out/stub.bin" > "$OUT/sites_$1.log" 2>&1
          log "$(printf 'SITES %-4s %s  red: %s' "$1" "$(grep -E '^ROWS=|^FOOTBRIDGE_SITES_(PASS|FAIL)' "$OUT/sites_$1.log" | tr '\n' ' ')" "$(grep -E ' FAIL$' "$OUT/sites_$1.log" | awk '{print $1}' | tr '\n' ',')")"; }
build FIX
sites FIX
python3 -u "$C/frozen/fbpending_witness.py" "$C/out/gxemul_FIX" "$C/out/stub.bin" > "$OUT/witness_FIX.log" 2>&1
log "WITNESS FIX rc=$? $(grep -E '^  (ok|FAIL) +(H1|H2|R0)' "$OUT/witness_FIX.log" | awk '{print $1":"$2}' | tr '\n' ' ') $(grep -E 'VERDICT' "$OUT/witness_FIX.log" | tail -1)"
python3 -u "$C/frozen/fbpending_drain_probe.py" "$C/out/gxemul_FIX" "$C/out/stub.bin" > "$OUT/drain_FIX.log" 2>&1
log "DRAIN FIX rc=$? $(grep -E '^  (ok|FAIL) +(H1|H2|R0)' "$OUT/drain_FIX.log" | awk '{print $1":"$2}' | tr '\n' ' ') $(grep -E 'FBDRAIN_VERDICT' "$OUT/drain_FIX.log" | tail -1)"
for M in Z9 M1b M1c M1d M1e; do
    cp "$C/out/FIX.c" src/devices/dev_footbridge.c
    python3 "$I/mkmut_p2b.py" "$C" "$M" > /dev/null || { log "$M DID NOT APPLY (guest)"; continue; }
    build "$M"; sites "$M"
done
cp "$SEC/src/devices/dev_footbridge.c" src/devices/dev_footbridge.c
build RESTORED
cmp -s src/devices/dev_footbridge.c "$SEC/src/devices/dev_footbridge.c" && [ gxemul -nt src/devices/dev_footbridge.c ] && rm -f "$C/.MUTANT" && log "B RESTORED (cmp == SEC, binary fresh), sentinel cleared"
log "TABLE3B_DONE $(date '+%F %T')"
