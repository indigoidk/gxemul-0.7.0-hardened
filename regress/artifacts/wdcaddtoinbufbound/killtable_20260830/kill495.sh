#!/bin/bash
#
#  #495 KILL TABLE -- four mutants against the shipped rung-3 detector.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaddtoinbufbound/killtable_20260830/kill495.sh
#
#  SCRATCH CLONE BY DEFAULT.  Every tree is `git archive HEAD` + the round's working
#  diff into /tmp, so no project build tree is mutated and NO .MUTANT IS OWED.  The
#  baseline is NAMED -- HEAD plus this round's own diff -- and cmp'd before mutant 1.
#
#  THE MUTANTS.  M1..M3 are the pass-1 seat's, re-measured against the SHIPPED code
#  rather than its candidate; M4 is floor clause (b).
#
#    M1  drop the FLAG conjunct        over-refuses -- suppresses CMDOUT pushes too
#    M2  clause (d): null the repair   `!= PHASE_CMDOUT` -> `== PHASE_COMPLETED`
#    M3  clause (d): width-qualify     `&& len == 1`, reads like the same check
#    M4  clause (b): REINSTATE         delete the guard entirely, restoring the defect
#
#  Each mutant is ONE EXPRESSION off the shipped predicate, except M4 which is the
#  verbatim reinstatement clause (b) demands.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gxk495}
SRC=${SRCTREE:-/tmp/gx495}
ART="$SEC/regress/artifacts/wdcaddtoinbufbound/killtable_20260830"
J=${J:-8}
OUTF="$O/TABLE.txt"

rm -rf "$O"; mkdir -p "$O"
say () { echo "$@" | tee -a "$OUTF"; }

say "===================================================================================="
say "#495 wdcaddtoinbufbound -- KILL TABLE"
say "===================================================================================="
say "date      $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "baseline  HEAD $(git rev-parse --short HEAD) + this round's working diff"
say ""

[ -x "$SRC/base/gxemul" ] || { say "*** $SRC/base/gxemul missing -- run run495.sh first"; exit 8; }
[ -f "$SRC/cd.iso" ]      || { say "*** $SRC/cd.iso missing"; exit 8; }
[ -f "$SRC/shipped.diff" ] || { say "*** $SRC/shipped.diff missing"; exit 8; }

#  ONE frozen instrument for the whole table.
FR="$O/frozen.py"
cp "$SEC/regress/wdc_addtoinbuf_probe.py" "$FR"
say "instrument frozen at $FR"
say ""

for MUT in M1 M2 M3 M4; do
	say "------------------------------------------------------------------ $MUT"
	T="$O/$MUT"; mkdir -p "$T"
	( cd "$SEC" && git archive HEAD ) | tar -x -C "$T"
	( cd "$T" && patch -p1 --batch --forward < "$SRC/shipped.diff" ) > /dev/null 2>&1 \
	    || { say "  *** base patch failed"; exit 8; }
	#  The clone must START from the named baseline.  A clone inherits whatever it
	#  was made from, and this is the one check that says which that was.
	cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
	    || { say "  *** clone is NOT the named baseline"; exit 8; }

	MUT="$MUT" python3 - "$T/src/devices/dev_wdc.c" <<'PY'
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
elif m == "M4":
    #  clause (b): remove the guard ENTIRELY, restoring the pre-fix control flow.
    if t.count(PRED + BODY + CLOSE) != 1:
        sys.exit("M4 block anchor %d -- refusing" % t.count(PRED + BODY + CLOSE))
    t = t.replace(PRED + BODY + CLOSE,
                  TAB + "if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {" + NL, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    sys.exit(0)
else:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(PRED, new, 1))
PY
	[ $? -eq 0 ] || { say "  *** mutant text not applied"; exit 8; }

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

	R="$O/run_$MUT"; mkdir -p "$R"
	( cd "$R" && python3 -u "$FR" "$SRC/base/gxemul" "$T/gxemul" "$SRC/cd.iso" "$R" \
	    > "$R/out.txt" 2>&1 )

	#  *** BEFORE SCORING: DID THIS RUN MEASURE ANYTHING? ***
	#
	#  A measuring seat triggered a false KILL three times in one table -- runs with
	#  `words 0 of 46`, pc already at HALT and elapsed 0.00 s were scored `KILLED
	#  (20 red)`.  Re-run quietly, two ESCAPED.  **Every one carried the completion
	#  sentinel**, which proves the probe finished writing and says nothing about
	#  whether it measured.  A FALSE KILL IS WORSE THAN A FALSE ESCAPE: it certifies
	#  coverage that was never taken.
	#
	#  THE DISCRIMINATOR IS THE BASE LEG, NOT A THRESHOLD.  The base binary is
	#  known-good and runs in the SAME invocation, so a control failure THERE is
	#  environmental; one confined to the MUTANT leg is a result -- some mutants
	#  legitimately kill the guest, and a threshold would reject those wrongly.
	WORDS_OK=$(grep -cE 'words ([0-9]+) of \\1$|words 46 of 46|words 54 of 54' "$R/out.txt")
	BASE_PC=$(sed -n '/LEG 1/,/LEG 2/p' "$R/out.txt" | grep -c 'pc at entry')
	BASE_BP=$(sed -n '/LEG 1/,/LEG 2/p' "$R/out.txt" | grep -c 'breakpoint reached: True')
	if [ "$BASE_PC" -lt 1 ] || [ "$BASE_BP" -lt 1 ]; then
		say "  *** THE BASE LEG'S APPARATUS CONTROLS FAILED -- this run measured"
		say "  *** nothing and its verdict would be environmental, not a result."
		say "  *** base: pc-at-entry rows=$BASE_PC  breakpoint-reached-True=$BASE_BP"
		say "  *** Re-run alone.  Do NOT score it."
		exit 8
	fi
	say "  apparatus: base leg parked and its encodings agree -- the run is scoreable"

	#  Score from the probe's OWN prediction count, never by grepping prose -- a
	#  `grep -c ' FAIL '` matched a probe's own verdict line last round and inflated
	#  every nonzero figure by one.
	PRED_N=$(grep -oE '[0-9]+ of [0-9]+ predictions correct' "$R/out.txt" | head -1)
	if [ -z "$PRED_N" ]; then
		say "  *** the probe printed no prediction count -- cannot score this mutant"
		tail -6 "$R/out.txt" | tee -a "$OUTF"
		exit 8
	fi
	GOT=$(echo "$PRED_N" | awk '{print $1}')
	TOT=$(echo "$PRED_N" | awk '{print $3}')
	say "  $PRED_N"
	if [ "$GOT" -lt "$TOT" ]; then say "  ==> KILLED  ($((TOT - GOT)) red)"
	else say "  ==> *** ESCAPED ***"; fi
	say ""
done

say "KILL495_DONE"
cp "$OUTF" "$ART/TABLE.txt"
for MUT in M1 M2 M3 M4; do
	[ -f "$O/run_$MUT/out.txt" ] && cp "$O/run_$MUT/out.txt" "$ART/kill_$MUT.out"
done
echo "preserved: killtable_20260830/TABLE.txt + kill_<mutant>.out"
