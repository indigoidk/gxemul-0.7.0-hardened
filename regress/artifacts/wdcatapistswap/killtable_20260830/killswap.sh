#!/bin/bash
#
#  `wdcatapistswap` -- the kill table for the ACCEPT arms (M and N).
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcatapistswap/killtable_20260830/killswap.sh
#
#  Run runswap.sh FIRST: this reuses its base/fix binaries and its CD image.
#
#  *** LEG 0 IS THE RE-MEASUREMENT, AND IT IS THE REASON THIS SCRIPT EXISTS IN TWO
#  HALVES. ***  The E2 escape figure this round is built on came from a pass-2 seat's
#  scratch run whose cited artifact (`opus495/wave2/run_q3.out`) NO LONGER EXISTS, and
#  the ledger row disagrees with itself about it -- witness field "20/20", note "all 22
#  rows".  A number that disagrees with itself and whose evidence is gone is not a
#  measurement, it is a transcription.  So leg 0 runs E2 against the COMMITTED
#  (pre-extension) probe from `git show HEAD:`, and the escape becomes a result of THIS
#  round.  Both halves of the harness proof are then measured rather than asserted:
#      the COMMITTED probe CANNOT see E2      (leg 0, expect ESCAPED)
#      the EXTENDED probe KILLS it            (E2 below, expect 4 red)
#
#  *** AND THE APPARATUS GATE IS FIXED HERE, NOT COPIED. ***  kill495.sh computes
#  WORDS_OK and then references it NOWHERE, while printing "its encodings agree -- the
#  run is scoreable".  That is a check that cannot fail, inside the scorer, and it was
#  found by a panel seat one day after the checkpoint documented the class.  Here the
#  word count is DERIVED from the probe's own CONTROL 0 line and actually gates.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
SRC=${SRC:-/tmp/gxswap}
O=${OUT:-/tmp/gxkswap}
ART="$SEC/regress/artifacts/wdcatapistswap/killtable_20260830"
J=${J:-8}
MUTANTS=${MUTANTS:-"M1 M2 M3 M4 M5 M6 M7 E2 E3 E4 E5"}
#  *** THE TABLE FILENAME IS A PARAMETER, AND IT HAS TO BE. ***  This script ends
#  by copying its table over $ART/TABLE.txt.  Re-running it for ONE extra mutant
#  would therefore DESTROY the preserved twelve-leg table -- the immutable-artifact
#  defect this very round already had to repair once, with a git blob recovery.
#  A follow-up run passes TABLETAG so its output lands beside the original.
TABLETAG=${TABLETAG:-}

[ -x "$SRC/base/gxemul" ] || { echo "*** $SRC/base/gxemul missing -- run runswap.sh first"; exit 8; }
[ -x "$SRC/fix/gxemul" ]  || { echo "*** $SRC/fix/gxemul missing -- run runswap.sh first"; exit 8; }
[ -f "$SRC/cd.iso" ]      || { echo "*** $SRC/cd.iso missing -- run runswap.sh first"; exit 8; }

rm -rf "$O"; mkdir -p "$O"
OUTF="$O/TABLE.txt"
: > "$OUTF"
say () { echo "$@" | tee -a "$OUTF"; }

say "===================================================================================="
say "wdcatapistswap -- KILL TABLE for the M and N accept arms"
say "===================================================================================="
say "date      $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "baseline  HEAD $(git rev-parse --short HEAD), UNMODIFIED -- #495 is committed, so"
say "          this round patches nothing into the product before mutating."
say ""

#  TWO frozen instruments.  A comparison run owes ONE instrument, and python re-reads
#  its source between invocations -- so both are frozen, and they are DIFFERENT files
#  on purpose: leg 0 needs the probe as COMMITTED, the rest need the extended one.
FR="$O/frozen_extended.py"
FRC="$O/frozen_committed.py"
cp "$SEC/regress/wdc_addtoinbuf_probe.py" "$FR"
#  *** THE PRE-EXTENSION PROBE IS PINNED BY SHA, AND THIS IS THE SECOND TIME TODAY
#  A RELATIVE REF IN THIS DIRECTORY WENT STALE THE MOMENT A COMMIT LANDED. ***  It
#  read `git show HEAD:`, which was right WHILE the round was in flight -- HEAD held
#  the 11-row probe and the working tree held 15.  The round then SHIPPED, HEAD
#  became the 15-row probe, and the guard below correctly refused a run in which
#  there was no longer any extension to measure.
#
#  The guard was right; the reference was wrong.  LEG 0 wants the probe as it stood
#  BEFORE this round extended it, which is a fixed revision, not a moving one.
#  `runswap.sh` learned the identical lesson about FIXREV this morning.
PROBEREV=${PROBEREV:-e61ccd8^}      # the parent of the round that added the arms
git show "$PROBEREV:regress/wdc_addtoinbuf_probe.py" > "$FRC" || exit 9

EXT_ROWS=$(awk '/^ROWS = \[/,/^\]/' "$FR"  | grep -c '^    (')
CMT_ROWS=$(awk '/^ROWS = \[/,/^\]/' "$FRC" | grep -c '^    (')
say "instruments frozen:"
say "  extended (working tree)  $EXT_ROWS rows -> $((EXT_ROWS * 2)) predictions"
say "  pre-extension ($PROBEREV) $CMT_ROWS rows -> $((CMT_ROWS * 2)) predictions"
if [ "$EXT_ROWS" -le "$CMT_ROWS" ]; then
	say "*** THE EXTENDED PROBE IS NOT LARGER THAN THE COMMITTED ONE.  There is no"
	say "*** extension to measure.  Refusing."
	exit 8
fi
say ""

#  ---------------------------------------------------------------- the mutant applier
apply_mutant () {   #  $1 = tree, $2 = mutant name
	MUT="$2" python3 - "$1/src/devices/dev_wdc.c" <<'PY'
import io, os, sys
NL = chr(10)
p = sys.argv[1]
t = io.open(p, encoding="utf-8", newline="").read()
TAB = chr(9) * 3
PRED = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
        TAB + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
BODY = TAB + chr(9) + "/*  out of protocol: refuse the push  */" + NL
CLOSE = TAB + "} else if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {" + NL
m = os.environ["MUT"]
if t.count(PRED) != 1:
    sys.exit("PRED anchor %d -- refusing" % t.count(PRED))
if m == "M1":
    new = TAB + "if (d->atapi_phase != PHASE_CMDOUT) {" + NL
elif m == "M2":
    new = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
           TAB + "    d->atapi_phase == PHASE_COMPLETED) {" + NL)
elif m == "M3":
    new = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT && len == 1) {" + NL)
elif m == "M5":
    new = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
           TAB + "    d->atapi_phase == PHASE_DATAIN) {" + NL)
elif m == "M6":
    new = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT && len == 2) {" + NL)
elif m == "E2":
    #  the operand swap this round exists to catch
    new = (TAB + "if (d->atapi_st != NULL &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
elif m == "E4":
    #  *** THE FLOOR BREACH. ***  An INEQUALITY width qualifier.  It refuses both the
    #  1-byte and the 2-byte injection, so before the 4-byte store was added it swept
    #  every row while re-opening the defect byte-for-byte.  MUST now be KILLED.
    new = (TAB + "if (d->atapi_cmd_in_progress &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT && len != 4) {" + NL)
elif m == "E6":
    #  *** THE ONLY MUTANT IN THIS ROUND DRAWN FROM FIELDS THE GUARDED BODY READS,
    #  so unlike E2 and E5 it is INSIDE clause (d)'s DEPENDS-ON enumeration. ***
    #  Refuse a push unless the ring is EMPTY.  It should pass the FIRST accept row of
    #  each arm (ring empty, push lands) and fail only the SECOND (ring now holds one
    #  byte, push refused, the read over-reads and returns ff).  That asymmetry is the
    #  whole warrant for the second row of each pair, and until this leg ran it was a
    #  PREDICTION rather than a measurement.
    new = (TAB + "if (d->inbuf_head != d->inbuf_tail &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
elif m == "E5":
    #  A SECOND operand replacement in E2's family.  The N arm does NOT defeat it:
    #  after both RECAL and SOFT_RESET cur_command != 0xa0, so the guard is false and
    #  both accept arms stay green.  EXPECTED TO ESCAPE -- filed as `wdcflagswap2`,
    #  and it is in the table so the escape is a measurement rather than a claim.
    new = (TAB + "if (d->cur_command == ATAPI_PKT_CMD &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT) {" + NL)
elif m == "E3":
    #  E2 plus a ONE-CONJUNCT exemption of the M arm's own opcode.  The N arm exists
    #  so that this cannot sweep: after ATAPI_SOFT_RESET the exemption does not apply.
    new = (TAB + "if (d->atapi_st != NULL &&" + NL +
           TAB + "    d->atapi_phase != PHASE_CMDOUT &&" + NL +
           TAB + "    d->cur_command != WDCC_RECAL) {" + NL)
elif m == "X4":
    #  `wdcringresetblind`: delete the RING RESET from wdc_new_command_reset(), leaving
    #  the flag/phase clears intact.  Two seats predicted opposite results -- one said
    #  29/30 (reasoning from the base leg), the other a clean escape (reasoning that the
    #  mutant lands only on the FIX tree, where the intact guard keeps the ring empty so
    #  the reset is dead code).  Measured rather than argued.
    RING = chr(9) + "d->inbuf_head = d->inbuf_tail = 0;" + NL
    if t.count(RING) != 1:
        sys.exit("ring-reset anchor %d -- refusing" % t.count(RING))
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace(RING, "", 1))
    sys.exit(0)
elif m == "M4":
    #  clause (b): remove the guard ENTIRELY, restoring the pre-fix control flow.
    if t.count(PRED + BODY + CLOSE) != 1:
        sys.exit("M4 block anchor %d -- refusing" % t.count(PRED + BODY + CLOSE))
    t = t.replace(PRED + BODY + CLOSE,
                  TAB + "if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {" + NL, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    sys.exit(0)
elif m == "M7":
    #  the refusal RETURNS instead of falling through to the handler's common tail.
    if t.count(PRED + BODY) != 1:
        sys.exit("M7 body anchor %d -- refusing" % t.count(PRED + BODY))
    t = t.replace(PRED + BODY, PRED + TAB + chr(9) + "return 0;" + NL, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    sys.exit(0)
else:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(PRED, new, 1))
PY
}

#  ------------------------------------------------------- the apparatus gate + scorer
#
#  Returns 0 and prints the verdict, or exits 8 if the run measured nothing.
score () {   #  $1 = run dir, $2 = label
	R="$1"
	#  *** THE WORD COUNT NOW ACTUALLY GATES.  Derived from the probe's own CONTROL 0
	#  line rather than matched against a hardcoded 46/54 -- this round's program is
	#  longer than either, so a literal would have silently stopped matching. ***
	BASE_W=$(sed -n '/LEG 1/,/LEG 2/p' "$R/out.txt" \
	    | grep -oE 'words [0-9]+ of [0-9]+' | head -1)
	BASE_PC=$(sed -n '/LEG 1/,/LEG 2/p' "$R/out.txt" | grep -c 'pc at entry')
	BASE_BP=$(sed -n '/LEG 1/,/LEG 2/p' "$R/out.txt" | grep -c 'breakpoint reached: True')
	WG=$(echo "$BASE_W" | awk '{print $2}')
	WT=$(echo "$BASE_W" | awk '{print $4}')

	#  THE DISCRIMINATOR IS THE BASE LEG, NOT A THRESHOLD.  The base binary is
	#  known-good and runs in the SAME invocation, so a control failure THERE is
	#  environmental; one confined to the MUTANT leg is a result -- M7 legitimately
	#  kills the guest, and a threshold would reject it wrongly.
	if [ "$BASE_PC" -lt 1 ] || [ "$BASE_BP" -lt 1 ]; then
		say "  *** THE BASE LEG'S APPARATUS CONTROLS FAILED -- this run measured"
		say "  *** nothing and its verdict would be environmental, not a result."
		say "  *** base: pc-at-entry=$BASE_PC  breakpoint-reached-True=$BASE_BP"
		say "  *** Re-run alone.  Do NOT score it."
		exit 8
	fi
	if [ -z "$WG" ] || [ -z "$WT" ] || [ "$WG" != "$WT" ]; then
		say "  *** THE BASE LEG'S ENCODINGS DO NOT AGREE WITH THE DISASSEMBLER"
		say "  *** (CONTROL 0 base leg: '${BASE_W:-<no line found>}')."
		say "  *** A hand-assembled word is wrong, or the probe never got that far."
		exit 8
	fi
	say "  apparatus: base leg parked, and $WG of $WT encodings agree -- scoreable"

	#  *** THE RUN MUST HAVE FINISHED, NOT MERELY GOT FAR ENOUGH TO PRINT A COUNT.
	#  Filed as `killdrivercrash`: a kill driver that reads neither the run exit
	#  status nor the completion sentinel scores a CRASHED mutant purely by HOW FAR
	#  IT GOT -- a partial run reads as KILLED, a very partial one as ESCAPED. ***
	#
	#  This driver was PARTLY protected already: a missing prediction count refuses
	#  below.  But the probe prints that count BEFORE its differential section and
	#  its sentinel, so a crash in between scored normally.  Narrower window, same
	#  class, and the census behind that row found SEVEN drivers with no sentinel
	#  check at all.
	#
	#  NOT hypothetical for this device: `write_in_progress` and `write_count` are
	#  set together and CLEARED AT DIFFERENT SITES, and the drain guard divides by
	#  `512 * d->write_count`.  An operand swap leaving the flag set while the count
	#  is zero is a MODULO BY ZERO -- exactly the clause-(d) shape this table builds.
	if ! grep -q ADDTOINBUF_RUNG3_DONE "$R/out.txt"; then
		say "  *** THE PROBE DID NOT REACH ITS COMPLETION SENTINEL.  It may have"
		say "  *** crashed after printing a score.  Refusing to score a partial run;"
		say "  *** a mutant that dies is a RESULT, but not this one."
		tail -4 "$R/out.txt" | sed 's/^/          /' | tee -a "$OUTF"
		exit 8
	fi

	#  Score from the probe's OWN prediction count, never by grepping prose -- a
	#  `grep -c ' FAIL '` matched a probe's own verdict line last round and inflated
	#  every nonzero figure by one.
	PRED_N=$(grep -oE '[0-9]+ of [0-9]+ predictions correct' "$R/out.txt" | head -1)
	if [ -z "$PRED_N" ]; then
		say "  *** the probe printed no prediction count -- cannot score this"
		tail -6 "$R/out.txt" | tee -a "$OUTF"
		exit 8
	fi
	GOT=$(echo "$PRED_N" | awk '{print $1}')
	TOT=$(echo "$PRED_N" | awk '{print $3}')
	say "  $PRED_N"
	if [ "$GOT" -lt "$TOT" ]; then say "  ==> KILLED  ($((TOT - GOT)) red)"
	else say "  ==> *** ESCAPED ***"; fi
}

#  ------------------------------------------------------------------------- build one
build_mutant () {   #  $1 = mutant name -> echoes tree path
	T="$O/$1"; mkdir -p "$T"
	( cd "$SEC" && git archive HEAD ) | tar -x -C "$T"
	#  The clone must START from the named baseline.  A clone inherits whatever it was
	#  made from, and this is the one check that says which that was.
	cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
	    || { say "  *** clone is NOT the named baseline (HEAD)"; exit 8; }
	apply_mutant "$T" "$1" || { say "  *** mutant text not applied"; exit 8; }
	if cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c"; then
		say "  *** MUTANT IS A NO-OP -- it would score as a kill, which is the"
		say "  *** vacuity this table exists to refuse."
		exit 8
	fi
	( cd "$T" && ./configure > "$T/conf.log" 2>&1 && rm -f src/cpus/*.o \
	    && make -j"$J" > "$T/make.log" 2>&1 )
	if [ ! -x "$T/gxemul" ] || [ ! "$T/gxemul" -nt "$T/src/devices/dev_wdc.c" ]; then
		say "  *** no fresh binary.  last make lines:"; tail -8 "$T/make.log" | tee -a "$OUTF"
		exit 8
	fi
}

#  ==================================================================== LEG 0
say "------------------------------------------------------------------ LEG 0"
say "  E2 against the COMMITTED probe ($CMT_ROWS rows).  EXPECT: ESCAPED."
say "  This re-measures the escape whose original artifact no longer exists."
build_mutant E2
R="$O/run_L0"; mkdir -p "$R"
( cd "$R" && python3 -u "$FRC" "$SRC/base/gxemul" "$O/E2/gxemul" "$SRC/cd.iso" "$R" \
    > "$R/out.txt" 2>&1 )
score "$R" "LEG0"
say ""

#  ==================================================================== the table
for MUT in $MUTANTS; do
	say "------------------------------------------------------------------ $MUT"
	if [ ! -d "$O/$MUT" ]; then build_mutant "$MUT"; else say "  (tree already built)"; fi
	R="$O/run_$MUT"; mkdir -p "$R"
	( cd "$R" && python3 -u "$FR" "$SRC/base/gxemul" "$O/$MUT/gxemul" "$SRC/cd.iso" "$R" \
	    > "$R/out.txt" 2>&1 )
	score "$R" "$MUT"
	say ""
done

say "KILLSWAP_DONE"
#  *** REFUSE THE COPY-BACK ON A PARTIAL RUN THAT DID NOT NAME ITSELF. ***  The
#  MUTANTS knob invites a one-mutant re-run, and an unconditional copy-back would
#  then replace a full table with a two-leg one -- destroying the artifact every
#  score in the round cites.  TABLETAG prevents that, but only if the caller
#  REMEMBERS it, and this round exists partly because a cited artifact vanished.
#  So remembering is not the mechanism: a subset run without a tag is REFUSED.
#  Named by a measuring seat that watched a partial run start and thought it was
#  about to lose the table.  It was not -- the tag was set -- but the knob is a
#  trap whether or not it springs.
if [ "$MUTANTS" != "M1 M2 M3 M4 M5 M6 M7 E2 E3 E4 E5" ] && [ -z "$TABLETAG" ]; then
	say "*** PARTIAL RUN (MUTANTS=$MUTANTS) WITH NO TABLETAG -- refusing to copy"
	say "*** this table over $ART/TABLE.txt.  Re-run with TABLETAG=_<something>."
	say "*** The run itself is complete and its logs are under $O."
	exit 8
fi
cp "$OUTF" "$ART/TABLE${TABLETAG}.txt"
#  *** THE KILL LOGS ARE TAGGED TOO, AND THIS WAS THE ROUND'S OWN LESSON APPLIED
#  TO ONLY HALF ITS OWN MECHANISM. ***  The TABLE was tagged; the per-mutant logs
#  and LEG 0 were not.  So the follow-up E6 run overwrote the twelve-leg table's
#  `kill_L0_committed_probe.out`, and the X4 run overwrote it AGAIN -- **twice, and
#  a regress-review seat's report about it went stale within the hour.**  The
#  original survived only because it had been COMMITTED and could be recovered from
#  the git blob, exactly as `shipped.diff` was earlier in this same round.
#
#  This is the immutability discipline applied to its own newest mechanism and
#  stopping halfway.  A tagged run now writes tagged logs, and LEG 0 -- which runs
#  unconditionally -- writes a tagged name so a follow-up cannot claim the main
#  table's slot.
cp "$O/run_L0/out.txt" "$ART/kill_L0${TABLETAG}_committed_probe.out" 2>/dev/null
for MUT in $MUTANTS; do
	[ -f "$O/run_$MUT/out.txt" ] && cp "$O/run_$MUT/out.txt" "$ART/kill${TABLETAG}_$MUT.out"
done
echo "preserved: wdcatapistswap/killtable_20260830/TABLE.txt + kill_<mutant>.out"
