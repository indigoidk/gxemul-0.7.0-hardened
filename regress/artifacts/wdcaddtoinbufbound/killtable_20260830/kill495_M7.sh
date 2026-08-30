#!/bin/bash
#
#  #495 -- M7, the ask-again mutant.  A packet-fed seat named it on pass 2 and said
#  plainly it was NOT CHECKABLE FROM THE PACKET.  It is checkable here.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaddtoinbufbound/killtable_20260830/kill495_M7.sh
#
#  THE MUTANT:  the guarded body's comment  ->  `return 0;`
#               (the PREDICATE is untouched; what changes is what the refusal DOES)
#
#  *** THE FIVE LINES THAT USED TO SIT HERE DESCRIBED M5, NOT M7. ***  They read
#  "THE MUTANT: `atapi_phase != PHASE_CMDOUT` -> `atapi_phase == PHASE_DATAIN`",
#  followed by M5's PHASE_COMPLETED rationale -- copied wholesale when this script was
#  cloned from kill495_M5.sh.  This script's OWN Python applies `return 0;`, and its own
#  `say` line reports "the guarded body now does return 0;", so the file contradicted
#  itself twice over.
#
#  Found by the opus5 seat during `wdcatapistswap` pass 1, in a DURABLE ARTIFACT that
#  had already shipped.  Its report said kill495_M6.sh carried the same defect; checked,
#  and it does NOT -- M6's mutant line reads `&& len == 2` and matches both its Python
#  and its `say`.  What M6 does share is M5's RATIONALE paragraph, which is merely
#  ill-fitting rather than false.  **Verified rather than accepted: seat rank does not
#  settle fact, and the correction is narrower than the finding that prompted it.**
#
#  WHAT M7 ACTUALLY TESTS: the refusal stops falling through to the handler's common
#  tail.  An early `return 0;` skips `memory_writemax64()` and the `return 1`, so the
#  guest gets an untouched read buffer and the access reports unhandled.  This is the
#  SKETCH RULE's own worked example -- four readers proposed exactly this line for a
#  different device without noticing the tail nine lines below.
#
#  THAT STATE IS REACHABLE, which is what makes the mutant worth building rather than
#  arguing about: atapi_phase is set to PHASE_COMPLETED at the end of a transfer, and
#  atapi_cmd_in_progress is cleared ONLY by wdc_new_command_reset() at the NEXT
#  command.  So the flag is still 1 while the phase is COMPLETED.
#
#  IF IT ESCAPES, IT IS A CLAUSE-(d) FLOOR BREACH -- L2, repaired in-round however late
#  it is found -- because the guard is present and its repair is nulled for a state the
#  shipped predicate covers.  The cap counts ASKS, never findings.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gxm7}
SRC=${SRCTREE:-/tmp/gx495}
ART="$SEC/regress/artifacts/wdcaddtoinbufbound/killtable_20260830"
J=${J:-8}
OUTF="$O/TABLE_M7.txt"

rm -rf "$O"; mkdir -p "$O"
say () { echo "$@" | tee -a "$OUTF"; }

say "===================================================================================="
say "#495 M7 -- the ask-again mutant (RETURN VALUE -- refuse the ACCESS instead of the push)"
say "===================================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "baseline HEAD $(git rev-parse --short HEAD) + this round's working diff"
say ""

[ -x "$SRC/base/gxemul" ] || { say "*** run495.sh must run first"; exit 8; }
[ -f "$SRC/cd.iso" ] || { say "*** $SRC/cd.iso missing"; exit 8; }

T="$O/M7"; mkdir -p "$T"
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
#  THE BODY, not the predicate.  `PRETABLE.out` prescribed a row or an explicit
#  no-row sentence for the RETURN VALUE and neither was built; this measures it.
#  The guard is kept and its refusal converted from REFUSE-THE-PUSH to
#  REFUSE-THE-ACCESS -- the one thing no row observes.
OLD = (TAB + chr(9) + "/*  out of protocol: refuse the push  */" + NL)
NEW = (TAB + chr(9) + "/*  out of protocol: refuse the push  */" + NL +
       TAB + chr(9) + "return 0;" + NL)
if t.count(OLD) != 1:
    sys.exit("BODY anchor %d -- refusing" % t.count(OLD))
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(OLD, NEW, 1))
PY
[ $? -eq 0 ] || { say "  *** mutant text not applied"; exit 8; }
cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
    && { say "  *** MUTANT IS A NO-OP -- it would score as a kill"; exit 8; }
#  *** NO BACKTICKS IN A DOUBLE-QUOTED say.  bash runs them as command
#  substitution: the first version of this line contained `return 0;` in backticks
#  and bash tried to EXECUTE it, printing `return: can only return from a function`
#  and truncating the message to `the guarded body now does `.  The MEASUREMENT was
#  unaffected -- 11 of 22 proves the mutant applied -- but the log said something
#  other than what ran, which is the class this whole directory is about. ***
say '  mutant applied: the guarded body now does  return 0;'

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
say "KILL495M7_DONE"
cp "$OUTF" "$ART/TABLE_M7.txt"
cp "$R/out.txt" "$ART/kill_M7.out"
echo "preserved: killtable_20260830/TABLE_M7.txt + kill_M7.out"
