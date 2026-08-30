#!/bin/bash
#
#  #495 -- M6, the ask-again mutant.  A packet-fed seat named it on pass 2 and said
#  plainly it was NOT CHECKABLE FROM THE PACKET.  It is checkable here.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaddtoinbufbound/killtable_20260830/kill495_M6.sh
#
#  THE MUTANT:  `atapi_phase != PHASE_CMDOUT`  ->  `atapi_phase != PHASE_CMDOUT && len == 2`
#
#  *** THE NINE LINES THAT SAT HERE WERE M5's RATIONALE, COPIED WHOLESALE WHEN THIS
#  SCRIPT WAS CLONED -- a PHASE-narrowing argument inside a WIDTH-narrowing mutant.
#  Byte-identical to kill495_M5.sh lines 11-19, verified by diff. ***
#
#  They argued that PHASE_COMPLETED is reachable while the flag is still 1, which is
#  true and is M5's point, and says nothing whatever about access WIDTH.
#
#  WHAT M6 ACTUALLY TESTS.  The guard gains `&& len == 2`, so it refuses only 2-byte
#  stores.  At the time this ran, BOTH of the probe's injections were 2-byte, so the
#  mutant refused both and every row stayed green -- it ESCAPED at 22/22, and that is
#  why the round made the second injection a SINGLE byte.  The table had measured the
#  inert member of a family and concluded the family was covered.
#
#  *** AND THE FAMILY WAS STILL NOT CLOSED, WHICH THIS SCRIPT COULD NOT HAVE KNOWN.
#  Making the widths {1,2} closes the EQUALITY qualifiers and leaves the INEQUALITY
#  `&& len != 4` open -- a floor breach found and repaired by wdcatapistswap, which
#  injects a third width. ***
#
#  Corrected 2026-08-30.  A seat reported this file AND kill495_M7.sh as carrying M5's
#  header; the first check answered on the `THE MUTANT:` line, found it correct here,
#  and called the report over-broad.  **The check was aimed at the wrong lines.**  The
#  seat was right about both files, and a correction is not safer than the thing it
#  corrects.
#
#  IF IT ESCAPES, IT IS A CLAUSE-(d) FLOOR BREACH -- L2, repaired in-round however late
#  it is found -- because the guard is present and its repair is nulled for a state the
#  shipped predicate covers.  The cap counts ASKS, never findings.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gxm6}
SRC=${SRCTREE:-/tmp/gx495}
ART="$SEC/regress/artifacts/wdcaddtoinbufbound/killtable_20260830"
J=${J:-8}
OUTF="$O/TABLE_M6.txt"

rm -rf "$O"; mkdir -p "$O"
say () { echo "$@" | tee -a "$OUTF"; }

say "===================================================================================="
say "#495 M6 -- the ask-again mutant (width-qualified len==2, the MIRROR of M3)"
say "===================================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "baseline HEAD $(git rev-parse --short HEAD) + this round's working diff"
say ""

[ -x "$SRC/base/gxemul" ] || { say "*** run495.sh must run first"; exit 8; }
[ -f "$SRC/cd.iso" ] || { say "*** $SRC/cd.iso missing"; exit 8; }

T="$O/M6"; mkdir -p "$T"
( cd "$SEC" && git archive HEAD ) | tar -x -C "$T"
( cd "$T" && patch -p1 --batch --forward < "$SRC/shipped.diff" ) > /dev/null 2>&1 \
    || { say "  *** base patch failed"; exit 8; }
cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
    || { say "  *** clone is NOT the named baseline"; exit 8; }

python3 - "$T/src/devices/dev_wdc.c" <<'PY'
import io, sys
NL = chr(10)
TAB = chr(9) * 3
p = sys.argv[1]
t = io.open(p, encoding="utf-8", newline="").read()
OLD = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
       TAB + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
NEW = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
       TAB + "    d->atapi_phase != PHASE_CMDOUT && len == 2) {" + NL)
if t.count(OLD) != 1:
    sys.exit("PRED anchor %d -- refusing" % t.count(OLD))
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(OLD, NEW, 1))
PY
[ $? -eq 0 ] || { say "  *** mutant text not applied"; exit 8; }
cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
    && { say "  *** MUTANT IS A NO-OP -- it would score as a kill"; exit 8; }
say "  mutant applied: != PHASE_CMDOUT  ->  != PHASE_CMDOUT && len == 2"

( cd "$T" && ./configure > "$T/conf.log" 2>&1 && rm -f src/cpus/*.o \
    && make -j"$J" > "$T/make.log" 2>&1 )
if [ ! -x "$T/gxemul" ] || [ ! "$T/gxemul" -nt "$T/src/devices/dev_wdc.c" ]; then
	say "  *** no fresh binary.  last make lines:"; tail -8 "$T/make.log" | tee -a "$OUTF"
	exit 8
fi
say "  binary $(stat -c '%s bytes' "$T/gxemul")"
say ""

R="$O/run"; mkdir -p "$R"
cp "$SEC/regress/wdc_addtoinbuf_probe.py" "$R/frozen.py"
( cd "$R" && python3 -u "$R/frozen.py" "$SRC/base/gxemul" "$T/gxemul" "$SRC/cd.iso" "$R" \
    > "$R/out.txt" 2>&1 )

PRED=$(grep -oE '[0-9]+ of [0-9]+ predictions correct' "$R/out.txt" | head -1)
if [ -z "$PRED" ]; then
	say "  *** no prediction count -- cannot score"; tail -6 "$R/out.txt" | tee -a "$OUTF"; exit 8
fi
GOT=$(echo "$PRED" | awk '{print $1}'); TOT=$(echo "$PRED" | awk '{print $3}')
say "  $PRED"
if [ "$GOT" -lt "$TOT" ]; then
	say "  ==> KILLED  ($((TOT - GOT)) red)  -- the detector sees the narrowing"
else
	say "  ==> *** ESCAPED ***  -- CLAUSE (d) FLOOR BREACH, L2, repair in-round"
fi
say ""
say "KILL495M6_DONE"
cp "$OUTF" "$ART/TABLE_M6.txt"
cp "$R/out.txt" "$ART/kill_M6.out"
echo "preserved: killtable_20260830/TABLE_M6.txt + kill_M6.out"
