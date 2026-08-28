#!/bin/bash
#  Table 5: ONLY the three mutants that failed to apply in table 4 (M8/M9/M10).
#  The probe is UNCHANGED at 19 rows, so table 4's other cells carry over -- the
#  adjudicator measured that legacy cells are identical across row-set changes when
#  the probe itself does not change, and here it does not change at all.
#  Mutants are applied by mut_common.py, a REAL FILE -- no shell->heredoc->python
#  escaping chain, which is what broke table 4's M8/M9/M10.
R=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$R/GXEMUL-SEC
B=$R/build
F=src/devices/dev_dreamcast_gdrom.c
MUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/40fd4ccc-4c3b-4ad6-91dc-122d039ab5a2/scratchpad/mut_common.py
PROBE=$SEC/regress/gdrom_toclen_probe.py
KERNEL=$R/_images/openbsd76-landisk-bsd.rd
OUT=$SEC/regress/artifacts/gdromexitsix/killtable4_20260828
mkdir -p $OUT

echo "gdromexitsix #489 table 5 -- $F  $(date)" > $B/.MUTANT
echo "kill489e.sh is mutating this tree.  Restore from GXEMUL-SEC and REBUILD." >> $B/.MUTANT

score () {   # $1 = label
    ( cd $B && make -j4 >/tmp/mk5.log 2>&1 )
    if [ ! "$B/gxemul" -nt "$B/$F" ]; then
        echo "$1  *** BUILD PRODUCED NO FRESH BINARY -- SCORE VOID (a BUILD failure) ***"
        tail -4 /tmp/mk5.log | sed 's/^/      /'
        return 9
    fi
    python3 -u "$PROBE" "$B/gxemul" "$KERNEL" > $OUT/$1.raw 2>&1
    local res ctl fails
    res=$(grep -o "TOCLEN_RESULT=[0-9]*/[0-9]*" $OUT/$1.raw | tail -1 | cut -d= -f2)
    ctl=$(grep -o "TOCLEN_CONTROL=[A-Z]*" $OUT/$1.raw | tail -1 | cut -d= -f2)
    fails=$(grep " FAIL$" $OUT/$1.raw | cut -c1-14 | sed 's/ *$//' | tr '\n' ',')
    printf '%-16s %-10s controls=%-5s  reds: %s\n' "$1" "${res:-NORESULT}" "${ctl:-?}" "${fails:-none}"
}

for m in M8 M9 M10; do
    case $m in
      M8)  label=M8_exemptzero ;;
      M9)  label=M9_lowerbound ;;
      M10) label=M10_latchstate ;;
    esac
    echo "=================== $label ==================="
    cp "$SEC/$F" "$B/$F"
    if python3 "$MUT" $m "$B/$F"; then
        score "$label"
    else
        echo "$label  *** MUTANT DID NOT APPLY -- anchor problem, NOT a build failure ***"
    fi
done

echo "=================== RESTORE ==================="
cp "$SEC/$F" "$B/$F"
if cmp -s "$B/$F" "$SEC/$F"; then
    ( cd $B && make -j4 >/tmp/mk5.log 2>&1 )
    if [ "$B/gxemul" -nt "$B/$F" ]; then
        rm -f $B/.MUTANT
        echo "RESTORE VERIFIED: source cmp-clean AND binary rebuilt.  Sentinel cleared."
    else
        echo "*** RESTORE INCOMPLETE: binary not fresh.  SENTINEL KEPT. ***"
    fi
else
    echo "*** RESTORE FAILED: source differs from SEC.  SENTINEL KEPT. ***"
fi
echo KILL489E_DONE
