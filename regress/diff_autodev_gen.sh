#!/bin/sh
#
#  #406: does makeautodev.sh build the device table from the DECLARATIONS, and
#  from nothing else?
#
#  WHY THIS EXISTS.  A prose mention of "DEVINIT" in a comment used to reach the
#  generated C.  dev_rs5c313.c:144 is such a line, and it produced 319
#  declarations instead of 77 -- 358 compiler errors, no binary, gate 1 red, and
#  eleven downstream gates skipped for want of a published binary.
#
#  *** THAT COMMENT IS STILL IN THE TREE, DELIBERATELY.  It was not reworded. ***
#  Rewording it would have made the hardening deletable in silence: revert the
#  generator and everything stays green.  Left in place, the live tree IS the
#  hostile input, so the mutant lane below genuinely fails when the anchor goes.
#  The planted cases exist so this detector does not DEPEND on that one comment
#  surviving a future edit.
#
#  THE ASSERTION IS THE EXACT NAME LIST, NOT "no bad characters", and that is the
#  design.  The corruption had TWO sources: 229 names containing a `.`
#  (Makefile.skel, bus_isa.o, even the generator's own in-flight temp file),
#  which are syntax errors -- and 14 names that are perfectly valid C
#  identifiers (Makefile, README, fonts, plus the comment's own words: gmtime,
#  being, the, right, choice ...), which fail at LINK time instead.  A row
#  asserting "no identifier contains a dot" PASSES a generator that still emits
#  those 14.  Mutant 2 below is exactly that half-fix, carried as a named case.
#
#  Offline: no compiler, no guest, no build tree.  Wired into gate 2.
set -u

HERE=$(cd "$(dirname "$0")" && pwd)
SEC=$(cd "$HERE/.." && pwd)
DEV="$SEC/src/devices"
GEN="$DEV/makeautodev.sh"

WORK=${TMPDIR:-/tmp}/gxsec-autodevgen.$$
trap 'rm -rf "$WORK"' 0 1 2 3 15
rm -rf "$WORK"; mkdir -p "$WORK"

rows=0
failures=0
ok()   { rows=$((rows + 1)); printf '  ok   %-48s %s\n' "$1" "$2"; }
bad()  { rows=$((rows + 1)); failures=$((failures + 1))
         printf '  FAIL %-48s %s\n' "$1" "$2"; }
note() { printf '  --   %s\n' "$1"; }

#  A pristine copy of everything the generator reads.  NEVER run it in the repo:
#  it writes autodev.c and .index, and both are TRACKED.
mkdir -p "$WORK/t"
cp "$DEV"/*.c "$WORK/t/"

#  What the generator SHOULD emit, derived from the declarations themselves.
#  Deliberately not taken from the committed autodev.c -- a tracked generated
#  file is not evidence about its own generator.  `grep dev_*.c` walks the files
#  in the same glob order the generator's `for a in dev_*.c` uses, so this is an
#  ORDERED expectation, not just a set.
( cd "$WORK/t" && grep -h '^DEVINIT(' dev_*.c |
    sed 's/^DEVINIT(\([^)]*\)).*/\1/' ) > "$WORK/want_dev"
( cd "$WORK/t" && grep -h '^PCIINIT(' bus_pci.c |
    sed 's/^PCIINIT(\([^)]*\)).*/\1/' ) > "$WORK/want_pci"
n_dev=$(grep -c . "$WORK/want_dev")
n_pci=$(grep -c . "$WORK/want_pci")

names_of()    { sed -n 's/^int devinit_\(.*\)(struct devinit \*);$/\1/p' "$1"; }
pcinames_of() { sed -n 's/^void pciinit_\([^(]*\)(struct machine \*.*$/\1/p' "$1"; }

#  Run a generator variant over a source tree.  $1=script $2=srcdir $3=tag.
#  Returns 0 and leaves autodev.c in $WORK/run_$3; returns 2 if it produced
#  nothing at all, which is a FAULT and must never be scored as a detection.
run_gen() {
    rm -rf "$WORK/run_$3"
    cp -r "$2" "$WORK/run_$3"
    cp "$1" "$WORK/run_$3/makeautodev.sh"
    chmod +x "$WORK/run_$3/makeautodev.sh"
    ( cd "$WORK/run_$3" && ./makeautodev.sh ) > "$WORK/gen_$3.log" 2>&1
    [ -f "$WORK/run_$3/autodev.c" ] || return 2
    return 0
}

# ------------------------------------------------------------ the committed tree
if ! run_gen "$GEN" "$WORK/t" base; then
    bad "generator runs on the committed tree" "no autodev.c -- see gen_base.log"
    printf '\n%d rows, %d failures\nAUTODEV_GEN_FAIL\n' "$rows" "$failures"
    exit 1
fi
ok "generator runs on the committed tree" "autodev.c produced"
BASE="$WORK/run_base/autodev.c"

names_of    "$BASE" > "$WORK/got_dev"
pcinames_of "$BASE" > "$WORK/got_pci"

#  THE LOAD-BEARING ROW.  Exact list, in order.  Order is not pedantry:
#  device_register() order is the order devices are offered to a machine, so a
#  reordering is a behavioural change even when the set is unchanged.
if cmp -s "$WORK/want_dev" "$WORK/got_dev"; then
    ok "devinit names == the ^DEVINIT( declarations, in order" "$n_dev names"
else
    bad "devinit names == the ^DEVINIT( declarations, in order" "differs:"
    diff "$WORK/want_dev" "$WORK/got_dev" | head -12 | sed 's/^/         /'
fi

if cmp -s "$WORK/want_pci" "$WORK/got_pci"; then
    ok "pciinit names == the ^PCIINIT( declarations, in order" "$n_pci names"
else
    bad "pciinit names == the ^PCIINIT( declarations, in order" "differs:"
    diff "$WORK/want_pci" "$WORK/got_pci" | head -12 | sed 's/^/         /'
fi

#  A fast legible tripwire, kept only as that.  The list comparison above is what
#  actually guards the table -- see mutant 2, which this row does NOT catch.
#  Digits are legal: dev_8253.c and dev_8259.c name devices starting with one.
junk=$(grep -c '^int devinit_[A-Za-z0-9_]*[^A-Za-z0-9_(]' "$BASE" || true)
if [ "$junk" = 0 ]; then
    ok "no emitted identifier holds a stray character" "0"
else
    bad "no emitted identifier holds a stray character" "$junk line(s)"
fi

#  The live off-anchor mention is what keeps the mutant lane honest.  If somebody
#  rewords it, say so out loud rather than letting the lane become unfalsifiable.
live=$(grep -c 'DEVINIT' "$WORK/t/dev_rs5c313.c" || true)
anch=$(grep -c '^DEVINIT(' "$WORK/t/dev_rs5c313.c" || true)
if [ "$live" -gt "$anch" ]; then
    ok "a live off-anchor DEVINIT mention still exists" "dev_rs5c313.c"
else
    bad "a live off-anchor DEVINIT mention still exists" \
        "GONE -- mutant 1/2 no longer prove anything; plant one or fix this row"
fi

# ------------------------------------------------------- planted hostile inputs
#  Do not rely on one comment surviving.  Plant a worse pair: prose DEVINIT and
#  prose PCIINIT, each on a line that BEGINS with the glob character that did the
#  damage.  A correct generator must be byte-for-byte unmoved by both.
cp -r "$WORK/t" "$WORK/t2"
cat >> "$WORK/t2/dev_cons.c" <<'PLANT'
/*
 *  #406 planted input.  A DEVINIT mention in prose, on a line starting with a
 *  glob character, is exactly the shape that expanded to the whole directory.
 */
PLANT
cat >> "$WORK/t2/bus_pci.c" <<'PLANT'
/*
 *  #406 planted input: a PCIINIT mention in prose, same shape.
 */
PLANT

if run_gen "$GEN" "$WORK/t2" plant; then
    if cmp -s "$BASE" "$WORK/run_plant/autodev.c"; then
        ok "planted DEVINIT + PCIINIT prose changes nothing" "byte-identical"
    else
        bad "planted DEVINIT + PCIINIT prose changes nothing" "output differs:"
        diff "$BASE" "$WORK/run_plant/autodev.c" | head -10 | sed 's/^/         /'
    fi
else
    bad "planted DEVINIT + PCIINIT prose changes nothing" "generator produced nothing"
fi

# --------------------------------------------------------------- the mutant lane
#  Every mutant runs against the PLANTED tree, so a surviving mutant means the
#  rows above are blind to it.  A mutant that produces no output is a FAULT and
#  is reported as one; that is not a kill (#55).
mutant() {   # $1 = label, $2 = sed program, $3 = which row is supposed to catch it
    sed "$2" "$GEN" > "$WORK/mut.sh"
    if cmp -s "$GEN" "$WORK/mut.sh"; then
        bad "MUTANT: $1" "sed matched nothing -- the mutant never existed"
        return
    fi
    if ! run_gen "$WORK/mut.sh" "$WORK/t2" mut; then
        bad "MUTANT: $1" "produced no output -- FAULT, not a detection"
        return
    fi
    names_of "$WORK/run_mut/autodev.c" > "$WORK/mut_dev"
    got=$(grep -c . "$WORK/mut_dev" || true)
    #  Report the extras, and how many of them are VALID C IDENTIFIERS.  That
    #  second number is the point: a dotless extra is invisible to the character
    #  row and shows up only as an undefined symbol at link time, so it is the
    #  ordered-list row that catches it BY CONSTRUCTION rather than by luck.
    sort "$WORK/want_dev" > "$WORK/w.s"; sort "$WORK/mut_dev" > "$WORK/m.s"
    comm -13 "$WORK/w.s" "$WORK/m.s" > "$WORK/extras"
    x_all=$(grep -c . "$WORK/extras" || true)
    x_clean=$(grep -vc '\.' "$WORK/extras" || true)
    if cmp -s "$WORK/want_dev" "$WORK/mut_dev"; then
        bad "MUTANT: $1" "SURVIVES -- $3 is blind to it"
    else
        ok "MUTANT killed: $1" \
           "$got names (want $n_dev); $x_all extra, $x_clean of them dotless"
    fi
}

#  1. THE FULL REVERT -- unanchored grep, no noglob.  The defect as it shipped.
mutant "full revert (unanchored + globbing)" \
  "s|grep '\^DEVINIT(' |grep DEVINIT |g; s|grep '\^PCIINIT(' |grep PCIINIT |g; /^[[:space:]]*set -f\$/d; /^[[:space:]]*set +f\$/d" \
  "the ordered-list row"

#  2. *** THE HALF-FIX, and the reason the character row is not enough. ***
#     Keeps `set -f`, so no `.` can ever appear and the tripwire row stays green,
#     but drops the anchor -- so the comment's own words still become device
#     declarations and the link fails instead of the parse.
mutant "noglob only, anchor dropped (the half-fix)" \
  "s|grep '\^DEVINIT(' |grep DEVINIT |g; s|grep '\^PCIINIT(' |grep PCIINIT |g" \
  "the ordered-list row (the character row is NOT)"

#  3. Anchor kept, noglob dropped.  Recorded, NOT asserted: a valid C declaration
#     cannot contain a glob character, so this is expected to be harmless today.
#     Asserting either outcome would be a row that passes both ways.
sed "/^[[:space:]]*set -f\$/d; /^[[:space:]]*set +f\$/d" "$GEN" > "$WORK/mut3.sh"
if run_gen "$WORK/mut3.sh" "$WORK/t2" m3; then
    if cmp -s "$BASE" "$WORK/run_m3/autodev.c"; then
        note "measured: with the anchor in place, dropping noglob changes nothing"
        note "           -- noglob is belt, not braces.  Both are kept anyway."
    else
        note "measured: dropping noglob DOES change the output -- stronger than expected"
    fi
else
    note "measured: the noglob-dropped variant produced nothing (fault, not a kill)"
fi

printf '\n%d rows, %d failures\n' "$rows" "$failures"
if [ "$failures" = 0 ]; then
    printf 'AUTODEV_GEN_PASS\n'; exit 0
else
    printf 'AUTODEV_GEN_FAIL\n'; exit 1
fi
