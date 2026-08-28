#!/bin/bash
#  KILL TABLE #2 for gdromexitsix Round 1 (#489), the case 0x14 TOC length decline.
#  15 rows now: `bad cnt` and `bad event` were added after M7's shape was MEASURED to
#  escape the 13-row version 13/13.  Every denominator changes, so the whole table re-runs.
#
#  SENTINEL DISCIPLINE: drops build/.MUTANT FIRST, clears it only after the restore is
#  verified by cmp against GXEMUL-SEC -- never against its own backup -- AND the binary
#  is rebuilt.
#
#  FIXED FROM THE FIRST VERSION: the mutant lines were
#      [ $? -eq 0 ] && build_and_score X || echo "X *** MUTANT TEXT NOT FOUND ***"
#  so a build_and_score that returned non-zero (a build producing no fresh binary) printed
#  "MUTANT TEXT NOT FOUND" -- a WRONG diagnosis of a build failure.  Two distinct failure
#  modes collapsed onto one message.  They are separated here.

R=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$R/GXEMUL-SEC
B=$R/build
F=src/devices/dev_dreamcast_gdrom.c
PROBE=$SEC/regress/gdrom_toclen_probe.py
KERNEL=$R/_images/openbsd76-landisk-bsd.rd
OUT=$SEC/regress/artifacts/gdromexitsix/killtable2_20260828
mkdir -p $OUT

build_and_score () {   # $1 = label
    ( cd $B && make -j4 >/tmp/mk.log 2>&1 )
    if [ ! "$B/gxemul" -nt "$B/$F" ]; then
        echo "$1  *** BUILD PRODUCED NO FRESH BINARY -- SCORE VOID (this is a BUILD failure, not a missing mutant) ***"
        tail -5 /tmp/mk.log | sed 's/^/      /'
        return 9
    fi
    python3 -u "$PROBE" "$B/gxemul" "$KERNEL" > $OUT/$1.raw 2>&1
    local res ctl fails
    res=$(grep -o "TOCLEN_RESULT=[0-9]*/[0-9]*" $OUT/$1.raw | tail -1 | cut -d= -f2)
    ctl=$(grep -o "TOCLEN_CONTROL=[A-Z]*" $OUT/$1.raw | tail -1 | cut -d= -f2)
    fails=$(grep " FAIL$" $OUT/$1.raw | cut -c1-14 | sed 's/ *$//' | tr '\n' ',' )
    printf '%-16s %-10s controls=%-5s  reds: %s\n' "$1" "${res:-NORESULT}" "${ctl:-?}" "${fails:-none}"
    return 0
}

mutate () {   # $1 = label, reads the python edit on stdin
    cp "$SEC/$F" "$B/$F"
    if python3 - "$B/$F"; then
        build_and_score "$1"
    else
        echo "$1  *** MUTANT TEXT NOT FOUND -- anchor missed, treated as FAIL ***"
    fi
}

restore () {
    cp "$SEC/$F" "$B/$F"
    if cmp -s "$B/$F" "$SEC/$F"; then
        ( cd $B && make -j4 >/tmp/mk.log 2>&1 )
        if [ "$B/gxemul" -nt "$B/$F" ]; then
            rm -f $B/.MUTANT
            echo "RESTORE VERIFIED: source cmp-clean AND binary rebuilt.  Sentinel cleared."
        else
            echo "*** RESTORE INCOMPLETE: source clean but binary NOT fresh.  SENTINEL KEPT. ***"
        fi
    else
        echo "*** RESTORE FAILED: source differs from SEC.  SENTINEL KEPT. ***"
    fi
}

echo "gdromexitsix Round 1 table 2 -- $F  $(date)" > $B/.MUTANT
echo "kill489b.sh is mutating this tree.  Restore from GXEMUL-SEC and REBUILD." >> $B/.MUTANT

echo "=================== BASE (shipped fix, 15 rows) ==================="
cp "$SEC/$F" "$B/$F"
build_and_score base

echo "=================== M1  reinstate exit(1)   (floor b) ==================="
mutate M1_reinstate <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="""		if (d->cnt != 408) {
			if (!(d->warned & GDROM_W_TOCLEN)) {
				d->warned |= GDROM_W_TOCLEN;
				fatal("[ dreamcast_gdrom: Read TOC with"
				    " cnt=%i, not 408 -- declined.  (once) ]\\n",
				    (int) d->cnt);
			}
			break;
		}"""
new="""		if (d->cnt != 408) {
			fatal("GDROM Read TOC not 408 bytes?\\n");
			exit(1);
		}"""
assert old in s
open(p,'w').write(s.replace(old,new,1))
PY

echo "=================== M2  != 408 -> > 408     (floor d) ==================="
mutate M2_gt408 <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="\t\tif (d->cnt != 408) {\n\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {"
new="\t\tif (d->cnt > 408) {\n\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {"
assert old in s
open(p,'w').write(s.replace(old,new,1))
PY

echo "=================== M3  unlatched decline ==================="
mutate M3_unlatched <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="""			if (!(d->warned & GDROM_W_TOCLEN)) {
				d->warned |= GDROM_W_TOCLEN;
				fatal("[ dreamcast_gdrom: Read TOC with"
				    " cnt=%i, not 408 -- declined.  (once) ]\\n",
				    (int) d->cnt);
			}
"""
new="""			fatal("[ dreamcast_gdrom: Read TOC with"
			    " cnt=%i, not 408 -- declined.  (once) ]\\n",
			    (int) d->cnt);
"""
assert old in s
open(p,'w').write(s.replace(old,new,1))
PY

echo "=================== M4  silent decline ==================="
mutate M4_silent <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="""			if (!(d->warned & GDROM_W_TOCLEN)) {
				d->warned |= GDROM_W_TOCLEN;
				fatal("[ dreamcast_gdrom: Read TOC with"
				    " cnt=%i, not 408 -- declined.  (once) ]\\n",
				    (int) d->cnt);
			}
			break;"""
new="""			break;"""
assert old in s
open(p,'w').write(s.replace(old,new,1))
PY

echo "=================== M5  guard grows: accepts 407, refuses 408 ==================="
mutate M5_grow <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="\t\tif (d->cnt != 408) {\n\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {"
new="\t\tif (d->cnt != 407) {\n\t\t\tif (!(d->warned & GDROM_W_TOCLEN)) {"
assert old in s
open(p,'w').write(s.replace(old,new,1))
PY

#  *** M7 IS THE REASON THIS TABLE EXISTS.  It escaped the 13-row version 13/13. ***
#  `break` -> `return` skips the common tail entirely: no `d->cnt = 0`, no
#  SYSASIC_TRIGGER_EVENT.  `bad cond` CANNOT see it (0xa0 has bit 3 already clear, so
#  clearing it is a no-op), which is exactly why `bad cnt` and `bad event` were added.
echo "=================== M7  break -> return  (skips the common tail) ==================="
mutate M7_return <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="\t\t\tbreak;\n\t\t}\n\t\talloc_data(d);"
new="\t\t\treturn;\n\t\t}\n\t\talloc_data(d);"
assert s.count(old) == 1, "M7 anchor is not unique"
open(p,'w').write(s.replace(old,new,1))
PY

echo "=================== M6  null medium  (floor c, apparatus control) ==================="
cp "$SEC/$F" "$B/$F"
( cd $B && make -j4 >/tmp/mk.log 2>&1 )
python3 -u "$PROBE" "$B/gxemul" /nonexistent/image.rd > $OUT/M6_nullmedium.raw 2>&1
echo "M6_nullmedium    controls=$(grep -o 'TOCLEN_CONTROL=[A-Z]*' $OUT/M6_nullmedium.raw | tail -1 | cut -d= -f2)  result=$(grep -o 'TOCLEN_RESULT=[0-9]*/[0-9]*' $OUT/M6_nullmedium.raw | tail -1 | cut -d= -f2)"

echo "=================== RESTORE ==================="
restore
echo "KILL489B_DONE"
