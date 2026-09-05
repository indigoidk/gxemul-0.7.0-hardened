#!/bin/bash
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxfable_p6
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p6_fable
PROBE=$SEC/regress/pcc2_width_probe.py
log(){ echo "[$(date +%H:%M:%S)] $*"; }

log "clone build/ -> $CL"
rm -rf "$CL"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CL" || { echo CLONE_FAIL; exit 9; }

log "sync SEC dev_pcc2.c + headers into clone (tree under review)"
cp "$SEC/src/devices/dev_pcc2.c" "$CL/src/devices/dev_pcc2.c"
cp "$SEC/src/include/thirdparty/mvme_pcctworeg.h" "$CL/src/include/thirdparty/mvme_pcctworeg.h" 2>/dev/null
cp "$SEC/src/include/thirdparty/mvme187.h" "$CL/src/include/thirdparty/mvme187.h" 2>/dev/null
cmp -s "$CL/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c" && log "clone dev_pcc2.c == SEC (BASE source verified)" || { echo BASE_SRC_MISMATCH; exit 9; }

cd "$CL" || exit 9
log "build BASE"
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > "$OUT/build_base.log" 2>&1
if [ ! -x gxemul ]; then echo BASE_BUILD_FAIL; tail -30 "$OUT/build_base.log"; exit 9; fi
[ gxemul -nt src/devices/dev_pcc2.c ] && log "BASE binary FRESH" || { echo BASE_STALE; exit 9; }

log "run probe on BASE"
python3 "$PROBE" "$CL/gxemul" > "$OUT/probe_base.out" 2>&1
BE=$(grep -cE '  ok$' "$OUT/probe_base.out"); BF=$(grep -cE '  FAIL$' "$OUT/probe_base.out")
log "BASE ok=$BE FAIL=$BF"

log "MUTANT: TxICR guard += '&& !d->pending_timer2_interrupts'"
echo "dev_pcc2.c TxICR-guard pending_timer2 qualifier" > "$CL/.MUTANT"
python3 - "$CL/src/devices/dev_pcc2.c" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old='if (len != 1 && writeflag == MEM_WRITE) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN'
new='if (len != 1 && writeflag == MEM_WRITE && !d->pending_timer2_interrupts) {\n\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN'
assert s.count(old)==1, "anchor count=%d"%s.count(old)
open(p,'w').write(s.replace(old,new))
print("MUTATED_OK")
PY
grep -n 'pending_timer2_interrupts) {' "$CL/src/devices/dev_pcc2.c" || { echo MUT_APPLY_FAIL; exit 9; }
log "build MUTANT"
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > "$OUT/build_mut.log" 2>&1
if [ ! -x gxemul ]; then echo MUT_BUILD_FAIL; tail -30 "$OUT/build_mut.log"; exit 9; fi
[ gxemul -nt src/devices/dev_pcc2.c ] && log "MUT binary FRESH" || { echo MUT_STALE; exit 9; }

log "run probe on MUTANT"
python3 "$PROBE" "$CL/gxemul" > "$OUT/probe_mut.out" 2>&1
ME=$(grep -cE '  ok$' "$OUT/probe_mut.out"); MF=$(grep -cE '  FAIL$' "$OUT/probe_mut.out")
log "MUT ok=$ME FAIL=$MF"

log "restore clone dev_pcc2.c from SEC + cmp"
cp "$SEC/src/devices/dev_pcc2.c" "$CL/src/devices/dev_pcc2.c"
cmp -s "$CL/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c" && { rm -f "$CL/.MUTANT"; log "restored, sentinel cleared"; } || echo RESTORE_FAIL
echo "SUMMARY BASE ok=$BE FAIL=$BF | MUT ok=$ME FAIL=$MF"
if [ "$MF" = "0" ] && [ "$BF" = "0" ] && [ "$BE" = "$ME" ]; then echo "VERDICT: MUTANT ESCAPES (both $BE/$BE green)"; else echo "VERDICT: differ (base $BE ok/$BF fail, mut $ME ok/$MF fail)"; fi
echo "MEASURE_DONE"
