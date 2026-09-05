#!/bin/bash
#  Opus 5 seat, pcc2widthkills pass 7.  Scratch clone only; never writes any project tree.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxopus_p7
L=/tmp/p7logs
SRC=$T/src/devices/dev_pcc2.c
GUARD='if (len != 1 && writeflag == MEM_WRITE) {'

log() { echo "[$(date +%T)] $*" | tee -a $L/driver.log; }

restore_verify() {
  cp $SEC/src/devices/dev_pcc2.c $SRC
  if cmp -s $SRC $SEC/src/devices/dev_pcc2.c; then log "RESTORE cmp-clean vs SEC"; else log "RESTORE CMP FAILED"; return 1; fi
  ( cd $T && rm -f src/devices/dev_pcc2.o gxemul && make > $L/build_restore.log 2>&1 )
  log "restore MAKE_RC=$?"
  if [ -x $T/gxemul ] && [ $T/gxemul -nt $SRC ]; then log "restore binary FRESH"; rm -f $T/.MUTANT; log "SENTINEL CLEARED"; else log "restore binary STALE/MISSING -- SENTINEL KEPT"; return 1; fi
  return 0
}

run_mutant() {
  NAME=$1
  ADD=$2
  log "=== $NAME : appending [$ADD] to all twelve guards ==="
  echo "$NAME <- $ADD" > $T/.MUTANT
  log "SENTINEL DROPPED"
  python3 - "$SRC" "$ADD" <<'PY'
import sys
p, add = sys.argv[1], sys.argv[2]
s = open(p).read()
old = "if (len != 1 && writeflag == MEM_WRITE) {"
new = "if (len != 1 && writeflag == MEM_WRITE && " + add + ") {"
n = s.count(old)
print("OCCURRENCES_FOUND=%d" % n)
assert n == 12, "expected 12 guards, found %d" % n
open(p, "w").write(s.replace(old, new))
print("MUTATION_WRITTEN")
PY
  log "mutant text in source: $(grep -c "$ADD" $SRC) occurrences (want 12)"
  ( cd $T && rm -f src/devices/dev_pcc2.o gxemul && make > $L/build_$NAME.log 2>&1 )
  log "$NAME MAKE_RC=$?"
  if [ -x $T/gxemul ] && [ $T/gxemul -nt $SRC ]; then log "$NAME binary FRESH"; else log "$NAME BUILD FAILED -- ABORT"; restore_verify; return 1; fi
  #  proof the mutation is in the BINARY: the guard now loads the qualifying field
  log "PROOF grep in .o: $(objdump -d $T/src/devices/dev_pcc2.o 2>/dev/null | wc -l) insn lines"
  python3 -u $L/frozen_probe.py $T/gxemul $NAME > $L/$NAME.out 2>&1
  log "$NAME PROBE_RC=$?"
  log "$NAME $(grep -E 'PCC2W_RESULT' $L/$NAME.out)"
  log "$NAME $(grep -E 'PCC2W_RED' $L/$NAME.out)"
  log "$NAME sentinel: $(tail -1 $L/$NAME.out)"
  restore_verify
}

log "DRIVER START (frozen copy).  probe md5 $(md5sum $L/frozen_probe.py | cut -c1-8)"
run_mutant M1_PENDT2_ALL12 "d->pending_timer2_interrupts == 0"
run_mutant M2_IPLZERO_ALL12 "d->pcctwo_reg[PCCTWO_IPL] == 0"
log "DRIVER DONE"
cp $L/driver.log $L/*.out /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p7_opus/ 2>/dev/null
echo P7_DRIVER_DONE
