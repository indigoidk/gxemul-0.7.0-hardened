#!/bin/sh
#  Opus pass-10 kill table.  Frozen at launch; NEVER edited while running.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CLONE=/tmp/gxopus_p10
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p10_opus
L=$OUT/DRIVER.log
say() { echo "[$(date '+%H:%M:%S')] $*" | tee -a $L; }

: > $L
say "PASS 10 opus table.  BASE already measured on this clone.  PREDICTIONS.md mtime:"
ls --time-style=full-iso -la $OUT/PREDICTIONS.md >> $L 2>&1
say "probe md5: $(md5sum /tmp/frozen_probe_p10.py | cut -c1-32)"

for M in M_P2T1 M_T1JOINT; do
    say "=== $M: SENTINEL FIRST ==="
    echo "$M src/devices/dev_pcc2.c TxICR guard conjunct (opus pass10)" > $CLONE/.MUTANT
    cp $SEC/src/devices/dev_pcc2.c $CLONE/src/devices/dev_pcc2.c
    cmp -s $CLONE/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && say "  restored-from-SEC cmp CLEAN before mutating"
    python3 $OUT/mutate.py $M >> $L 2>&1 || { say "  MUTATE FAILED -- ABORT"; exit 9; }
    diff $SEC/src/devices/dev_pcc2.c $CLONE/src/devices/dev_pcc2.c > $OUT/$M.diff
    say "  mutant diff vs SEC: $(grep -c '^[<>]' $OUT/$M.diff) lines"
    grep '^>' $OUT/$M.diff | head -3 | sed 's/^/      /' | tee -a $L
    ( cd $CLONE && rm -f src/devices/dev_pcc2.o && make -j4 > $OUT/${M}_build.log 2>&1 )
    say "  MAKE_RC=$?"
    if [ ! $CLONE/gxemul -nt $CLONE/src/devices/dev_pcc2.c ]; then say "  BINARY NOT NEWER -- ABORT"; exit 8; fi
    say "  binary $(date -r $CLONE/gxemul '+%H:%M:%S')  source $(date -r $CLONE/src/devices/dev_pcc2.c '+%H:%M:%S')"
    ( cd $SEC/regress && python3 -u /tmp/frozen_probe_p10.py $CLONE/gxemul $M > $OUT/$M.out 2>&1 )
    say "  $M: $(grep -o 'PCC2W_RESULT=[0-9]*/[0-9]*' $OUT/$M.out)  sentinel=$(grep -c PCC2W_PROBE_DONE $OUT/$M.out)"
    say "  RED: $(grep 'FAIL$' $OUT/$M.out | cut -c1-16 | tr -d ' ' | paste -sd, -)"
done

say "=== RESTORE from SEC, rebuild, cmp, THEN clear the sentinel ==="
cp $SEC/src/devices/dev_pcc2.c $CLONE/src/devices/dev_pcc2.c
( cd $CLONE && rm -f src/devices/dev_pcc2.o && make -j4 > $OUT/restore_build.log 2>&1 )
say "  restore MAKE_RC=$?"
cmp $CLONE/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && say "  cmp vs SEC CLEAN"
if [ $CLONE/gxemul -nt $CLONE/src/devices/dev_pcc2.c ]; then
    rm -f $CLONE/.MUTANT; say "  binary newer than source: SENTINEL CLEARED"
else
    say "  BINARY NOT NEWER -- SENTINEL LEFT IN PLACE"
fi
say "  project trees untouched? git status of SEC:"
( cd $SEC && git status --porcelain | wc -l ) >> $L 2>&1
say "OPUS_P10_TABLE_DONE"
