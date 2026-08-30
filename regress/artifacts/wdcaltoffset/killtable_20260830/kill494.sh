#!/bin/bash
#
#  #494 KILL TABLE -- four mutants against the shipped detector pair.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/kill494.sh
#
#  A FILE, and run from a FROZEN COPY of itself is unnecessary here only because it
#  is not edited while running -- but the probes ARE frozen per leg, because python
#  re-reads a script between runs and an edit lands in the very output being diffed.
#
#  SCRATCH CLONE BY DEFAULT.  Every tree is `git archive HEAD` + a patch into /tmp,
#  so no project build tree is mutated and NO .MUTANT SENTINEL IS OWED.  The baseline
#  is NAMED: HEAD plus the round's own working diff, cmp'd before mutant 1.
#
#  THE MUTANTS, each prescribed before the table ran (PRETABLE.out):
#    m1  over-reach     `!= 0` -> `!= 2`   declines BOTH offsets; must redden ACCEPT
#    m2  nulled decode  `!= 0` -> `>  1`   never true; must redden the DEFECT rows
#    m3  partial guard  guard only the helper call, leave cur_command clobbered.
#                       *** ESCAPED the 15-row witness 15/15.  The SIGNATURE probe
#                       is the only instrument that sees it. ***
#    m4  value guard    `!= 0` -> `!= 0 && idata == 0x06`   keeps the witness's own
#                       value working and re-opens 0x04/0x0c/0x0e.  The PHASE 4 rows
#                       exist for exactly this one.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
O=${OUT:-/tmp/gxk494}
SRC=${SRCTREE:-/tmp/gx494}
ART="$SEC/regress/artifacts/wdcaltoffset/killtable_20260830"
J=${J:-8}
OUTF="$O/TABLE.txt"

rm -rf "$O"; mkdir -p "$O"
say () { echo "$@" | tee -a "$OUTF"; }

say "===================================================================================="
say "#494 wdcaltoffset -- KILL TABLE"
say "===================================================================================="
say "date      $(date '+%Y-%m-%d %H:%M:%S')"
cd "$SEC" || exit 9
say "baseline  HEAD $(git rev-parse --short HEAD) + the round's working diff on dev_wdc.c"
say ""

for leg in base fix; do
	[ -x "$SRC/$leg/gxemul" ] || { say "*** $SRC/$leg/gxemul missing"; exit 8; }
done

IMG="$SRC/altoff-scratch.img"
CD="$SRC/altoff-cd.img"
[ -f "$IMG" ] || dd if=/dev/zero of="$IMG" bs=1M count=8 status=none
[ -f "$CD" ]  || dd if=/dev/zero of="$CD"  bs=1M count=8 status=none

#  ONE frozen instrument pair for the whole table.
FR="$O/frozen"; mkdir -p "$FR"
cp "$SEC/regress/wdc_altoffset_probe.py"     "$FR/"
cp "$SEC/regress/wdc_altoffset_sig_probe.py" "$FR/"
say "instruments frozen in $FR"
say ""

#  ---------------------------------------------------------------- mutant text
mut_apply () {   # $1 = tree
	local T="$1" F="$1/src/devices/dev_wdc.c"
	case "$MUT" in
	m1) sed -i 's/else if (relative_addr != 0) {/else if (relative_addr != 2) {/' "$F" ;;
	m2) sed -i 's/else if (relative_addr != 0) {/else if (relative_addr > 1) {/' "$F" ;;
	m4) sed -i 's/else if (relative_addr != 0) {/else if (relative_addr != 0 \&\& idata == 0x06) {/' "$F" ;;
	m3) python3 - "$F" <<'PY'
import io, sys
#  m3: revert the decode, then guard ONLY the helper call -- cur_command stays
#  clobbered.  Two edits, and the second is the point: this is the shape that
#  escaped the witness, because no row observed cur_command.
p = sys.argv[1]
t = io.open(p, encoding="utf-8", newline="").read()
a = "\telse if (relative_addr != 0) {"
i = t.index(a)
j = t.index("\t} else {", i)
t = t[:i] + "\telse {" + t[j + len("\t} else {"):]
b = ("\t\tif (idata & WDCTL_RST) {\n"
     "\t\t\td->cur_command = COMMAND_RESET;\n"
     "\t\t\twdc_new_command_reset(d);\n")
c = ("\t\tif (idata & WDCTL_RST) {\n"
     "\t\t\td->cur_command = COMMAND_RESET;\n"
     "\t\t\tif (relative_addr == 0)\n"
     "\t\t\t\twdc_new_command_reset(d);\n")
assert t.count(b) == 1, "m3 anchor B count %d" % t.count(b)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(b, c, 1))
PY
	   ;;
	esac
}

for MUT in m1 m2 m3 m4; do
	say "------------------------------------------------------------------ $MUT"
	T="$O/$MUT"; mkdir -p "$T"
	( cd "$SEC" && git archive HEAD ) | tar -x -C "$T"
	( cd "$T" && patch -p1 --batch --forward < "$SRC/shipped.diff" ) > /dev/null 2>&1 \
	    || { say "  *** base patch failed"; exit 8; }
	#  cmp against the round's own fix leg BEFORE mutating: the clone must start
	#  from the named baseline, not from whatever /tmp held.
	cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c" \
	    || { say "  *** clone is not the baseline"; exit 8; }

	mut_apply "$T"
	if cmp -s "$T/src/devices/dev_wdc.c" "$SEC/src/devices/dev_wdc.c"; then
		say "  *** MUTANT TEXT NOT APPLIED -- a no-op mutant scores as a kill"
		say "  *** and that is the vacuity this table exists to refuse."
		exit 8
	fi

	( cd "$T" && ./configure > "$T/conf.log" 2>&1 && rm -f src/cpus/*.o \
	    && make -j"$J" > "$T/make.log" 2>&1 )
	if [ ! -x "$T/gxemul" ] || [ ! "$T/gxemul" -nt "$T/src/devices/dev_wdc.c" ]; then
		say "  *** no fresh binary; last make lines:"; tail -8 "$T/make.log" | tee -a "$OUTF"
		exit 8
	fi

	R="$O/run_$MUT"; mkdir -p "$R"; cp "$FR"/*.py "$R/"
	( cd "$R" && python3 -u "$R/wdc_altoffset_probe.py" \
	    "$SRC/base/gxemul" "$T/gxemul" "$IMG" "$R" > "$R/main.out" 2>&1 )
	( cd "$R" && python3 -u "$R/wdc_altoffset_sig_probe.py" "$R" "$CD" \
	    "base=$SRC/base/gxemul" "mut=$T/gxemul" > "$R/sig.out" 2>&1 )

	#  *** THIS COUNTER HAS BEEN WRONG TWICE, IN TWO DIFFERENT WAYS. ***
	#
	#  (1) `grep -c` PRINTS 0 and EXITS 1 when nothing matches, so a trailing
	#      `|| echo 0` appended a SECOND line and the variable held two lines.
	#      `[ "$X" -gt 0 ]` on that is an ERROR, not a comparison.
	#  (2) `grep -c ' FAIL '` MATCHED THE PROBE'S OWN VERDICT LINE -- *** SOMETHING
	#      DID NOT HOLD -- read the FAIL line *** -- so every nonzero count came
	#      back inflated by one.  The only count that was RIGHT was the zero, which
	#      is why the defect hid: with nothing failing there is no verdict line to
	#      miscount, so the anomalous-looking row was the correct one.
	#
	#  Repaired by not counting prose at all.  The probe emits `N of M row
	#  predictions` itself; that number is self-describing and cannot match a
	#  sentence.  RED = M - N.
	PRED=$(grep -oE '[0-9]+ of [0-9]+ row predictions' "$R/main.out" 2>/dev/null | head -1)
	if [ -n "$PRED" ]; then
		MAINRED=$(( $(echo "$PRED" | awk '{print $3}') - $(echo "$PRED" | awk '{print $1}') ))
	else
		say "  *** the probe printed no prediction count -- cannot score this mutant"
		exit 8
	fi
	#  the sig probe reports per leg; a mutant that re-opens the signature shows
	#  "DEFECT PRESENT" on its own leg.
	SIGRED=$(awk '/^  mut /{f=1} f&&/DEFECT PRESENT/{print "1"; exit}' "$R/sig.out" | head -1)
	SIGRED=${SIGRED:-0}
	say "  main detector FAIL rows : $MAINRED"
	say "  signature defect on mut : $SIGRED   (1 = the mutant re-opened it)"
	if [ "$MAINRED" -gt 0 ] || [ "$SIGRED" = "1" ]; then
		say "  ==> KILLED"
	else
		say "  ==> *** ESCAPED ***"
	fi
	say ""
done

say "KILL494_DONE"
cp "$OUTF" "$ART/TABLE.txt"

#  *** PRESERVE PER MUTANT.  The first version of this block was
#  `cp -r "$O"/run_*/main.out "$ART/"` -- FOUR files copied to ONE name, so three
#  runs were destroyed and the survivor identified no mutant.  A record citing
#  `main.out` would have pointed at whichever ran last.
#
#  This is the immutable-artifact rule broken inside the script whose whole job is
#  producing citable evidence, and it was found only because a live seat noticed a
#  DIFFERENT citation of mine disagreed with its own log.
for MUT in m1 m2 m3 m4; do
	for kind in main sig; do
		src="$O/run_$MUT/$kind.out"
		[ -f "$src" ] && cp "$src" "$ART/${kind}_${MUT}.out"
	done
done
echo "preserved: killtable_20260830/TABLE.txt + main_<mutant>.out + sig_<mutant>.out"
