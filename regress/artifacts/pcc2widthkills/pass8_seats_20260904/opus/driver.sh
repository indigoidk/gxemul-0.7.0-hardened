#!/bin/bash
#  pcc2widthkills pass 8 -- Opus seat kill table.  Runs in a SCRATCH CLONE only.
#  BASE first (must be 171/171), then one mutant at a time, each restored FROM SEC.
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
CL=/tmp/gxopus_p8
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p8_opus
OUT=$CL/p8
PROBE=$OUT/frozen_probe.py

say() { echo "[$(date +%H:%M:%S)] $*"; }

rebuild() {
    cd $CL
    rm -f src/devices/dev_pcc2.o gxemul
    make > $OUT/build_$1.log 2>&1
    if [ ! -f gxemul ]; then say "BUILD FAILED for $1"; tail -20 $OUT/build_$1.log; return 1; fi
    if [ gxemul -nt src/devices/dev_pcc2.c ]; then say "$1 build FRESH_OK"; else say "$1 build STALE *** ABORT ***"; return 1; fi
}

runprobe() {
    cd $CL
    python3 -u $PROBE $CL/gxemul "$1" > $OUT/probe_$1.txt 2>&1
    local res sent red
    sent=$(grep -c PCC2W_PROBE_DONE $OUT/probe_$1.txt)
    res=$(grep -o 'PCC2W_RESULT=[0-9]*/[0-9]*' $OUT/probe_$1.txt | tail -1)
    red=$(grep -o 'PCC2W_RED=.*' $OUT/probe_$1.txt | tail -1)
    say "$1: $res   sentinel=$sent"
    say "$1: $red"
    echo "$1|$res|$red|sentinel=$sent" >> $OUT/TABLE.txt
}

restore_verify() {
    cp "$SEC/src/devices/dev_pcc2.c" $CL/src/devices/dev_pcc2.c
    if cmp -s $CL/src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c"; then
        say "restore CMP CLEAN against SEC"
    else
        say "restore CMP FAILED *** SENTINEL STAYS ***"; return 1
    fi
    rebuild restore || return 1
    rm -f $CL/.MUTANT
    say "sentinel cleared (source cmp-clean AND binary rebuilt newer)"
}

say "=== pass 8 Opus table start ==="
cmp -s $CL/src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" || { say "CLONE NOT CLEAN AT START -- ABORT"; exit 1; }
say "clone dev_pcc2.c cmp-clean against SEC (the named baseline)"
md5sum $PROBE "$SEC/regress/pcc2_width_probe.py"
: > $OUT/TABLE.txt

rebuild BASE || exit 1
runprobe BASE

for M in M_IPLR M_WARNX; do
    say "--- $M ---"
    echo "$M: mutating $CL/src/devices/dev_pcc2.c" > $CL/.MUTANT
    python3 $D/mutate.py $M || { say "mutate failed"; exit 1; }
    #  PROOF OF MUTATION: a diff against SEC, counted.  Never a grep for a literal.
    n=$(diff "$SEC/src/devices/dev_pcc2.c" $CL/src/devices/dev_pcc2.c | grep -c '^[<>]')
    say "$M diff-vs-SEC changed lines: $n"
    if [ "$n" -lt 1 ]; then say "$M SOURCE UNCHANGED -- REFUSING"; restore_verify; exit 1; fi
    diff "$SEC/src/devices/dev_pcc2.c" $CL/src/devices/dev_pcc2.c > $OUT/diff_$M.txt
    rebuild $M || { restore_verify; exit 1; }
    runprobe $M
    restore_verify || exit 1
done

say "=== table done ==="
cat $OUT/TABLE.txt
ls -la $CL/.MUTANT 2>/dev/null && say "*** SENTINEL STILL PRESENT ***" || say "no sentinel: clone is clean"
