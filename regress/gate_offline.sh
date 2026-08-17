#!/bin/bash
# GATE 2 -- offline differential of the REAL ieee_store_float_value().
#
# The strongest gate here, and the cheapest, but only because it links the shipped
# src/core/float_emul.c. The first version of this gate transcribed BOTH sides of the
# differential and compared the copy against itself -- it never compiled or executed
# float_emul.c at all, so deleting #287 from the shipped source left it green. Review
# caught that, not the gate. Two things now prevent a repeat:
#
#   * the real file is compiled and linked into the driver, and
#   * the file compiled is asserted byte-identical to the committed one, so "the test
#     passed" and "the repository is correct" are the same statement.
#
# misc.h includes ../../config.h, which configure generates, so the compile has to happen
# against a CONFIGURED tree. That tree is a copy of the committed source (no VPATH in this
# project), which is exactly why the identity check above is required rather than assumed.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

SEC=$ROOT/GXEMUL-SEC
SRC=core/float_emul.c

gate_begin "offline-differential"

# #375: the mips*_loadstore[32] dispatch-table index is a SILENT CROSS-FILE
# COUPLING. generate_mips_loadstore.c emits the table in the loop order
# `endianness -> store -> size -> signedness`, so an entry's index is
# endianness*16 + store*8 + size*2 + signedness. That arithmetic is then
# hard-coded BY HAND, with no comment and no check, at a dozen sites: the
# multi-transfer fold's bail (`mips32_loadstore[5]` = plain lw), the coproc
# handlers (lwc1->5, swc1->12, ldc1->7, sdc1->14), the canonical decoder, and
# the COMBINE(nop)/strlen/#169 matcher slots. Reorder that one generator loop
# and every hand-coded index silently mis-resolves -- the fold bail dispatches
# the wrong access SIZE, ldc1 becomes lw -- and NOTHING fails to compile. These
# rows turn the coupling into a checked invariant, offline, needing no compiler
# and no rig (only the committed generated table). Found by the #46 MIPS-combiner
# audit; both boot rigs are LE, so the _be entries are dead code on the harness
# but the coupling is real for any future BE MIPS work.
#
# The byte rows are load-bearing in the opposite direction: size==0 has no
# endianness, so the generator makes the byte LE and BE entries the SAME symbol
# ([1]==[17], [8]==[24]). #169's byte-store check and the strlen byte-load check
# rely on that share; the word rows ([5]!=[21]) prove the discrimination the byte
# rows deliberately lack. If a generator change ever split the byte entries, the
# `|| [x+16]` matcher tautologies become live and those checks silently weaken.
MIPSLS=$SEC/src/cpus/tmp_mips_loadstore.c
need_file "$MIPSLS"

#  ls_entry <array-name> <index> -> the function symbol at that index, read from
#  the committed generated table (the [32] arrays, not the [16] generic ones).
ls_entry() {
    awk -v arr="$1" -v idx="$2" '
        $0 ~ ("\\*" arr "\\[32\\]") { f = 1; n = 0; next }
        f && /^};/ { f = 0 }
        f { gsub(/[ \t,};]/, "");
            if ($0 != "") { if (n == idx) { print $0; exit } n++ } }
    ' "$MIPSLS"
}

for arr in mips32_loadstore mips_loadstore; do
    pfx=${arr%_loadstore}
    check "  $arr[5]  = plain word-load LE"  "$(ls_entry $arr 5)"  "${pfx}_instr_l4_le"
    check "  $arr[12] = plain word-store LE" "$(ls_entry $arr 12)" "${pfx}_instr_s4_le"
    check "  $arr[21] = plain word-load BE"  "$(ls_entry $arr 21)" "${pfx}_instr_l4_be"
    check "  $arr byte-load LE/BE share [1]==[17]" \
        "$([ "$(ls_entry $arr 1)" = "$(ls_entry $arr 17)" ] && echo same || echo differ)" "same"
    check "  $arr byte-store LE/BE share [8]==[24]" \
        "$([ "$(ls_entry $arr 8)" = "$(ls_entry $arr 24)" ] && echo same || echo differ)" "same"
    check "  $arr word-load LE != BE [5]!=[21]" \
        "$([ "$(ls_entry $arr 5)" != "$(ls_entry $arr 21)" ] && echo differ || echo same)" "differ"
done

#  b1w: the pty record parser's selftest, and a POSITIVE CONTROL that proves the selftest can
#  still catch something.  Placed BEFORE the compiler check on purpose: it needs only python3,
#  and a machine without cc must not silently lose parser coverage as well as the
#  differentials.  A measured census (absorb_census.py, 22 mutants) is what set the row floor;
#  the shipped selftest before this round killed 17 of those 22 while reporting every row
#  green, because its rows compared body+tail and a mutant that only MOVES text between the
#  halves preserves the sum.
ABLOG=$LOGDIR/selftest_absorb.log
python3 "$HERE/selftest_absorb.py" > "$ABLOG" 2>&1 || true
check     "absorb: no row failed" \
          "$(grep -oE '[0-9]+ failures' "$ABLOG" | grep -oE '^[0-9]+')" "0"
check     "absorb: verdict present" "$(grep -c SELFTEST_ABSORB_PASS "$ABLOG")" "1"
check_min "absorb: rows actually run" \
          "$(grep -oE '^[0-9]+ rows' "$ABLOG" | grep -oE '^[0-9]+')" 52
#  Name the two rows the census showed were load-bearing, so deleting either is a red row
#  rather than a quieter file.  (#410's lesson: a row that can only be counted cannot be
#  missed by name.)
check     "absorb: the hold invariant row is present" \
          "$(grep -c 'tail invariant held at every step' "$ABLOG")" "1"
#  A FLOOR: three today, and adding a fourth guest-text fixture must not red the gate.
check_min "absorb: the body-landing rows are present" \
          "$(grep -c 'lands in BODY' "$ABLOG")" 1

#  #425/#426: the budget the driver PRINTS must be the budget it ENFORCES, and the gate's
#  budget classifier must be exercisable without a rig.  Both are offline.
#
#  The straddle (selftest_budget.py) reads BUDGET=N from the driver's OWN OUTPUT and then
#  runs one leg under N and one over it.  MEASURED against three mutants in copies: a
#  call-site multiply, a multiply at the COMPARISON, and a deleted stop -- all three go red,
#  and the unmutated copy passes.  The comparison mutant is the one NO printing scheme can
#  catch, which is why this row exists at all.
BULOG=$LOGDIR/selftest_budget.log
python3 "$HERE/selftest_budget.py" > "$BULOG" 2>&1 || true
check     "budget: no row failed" \
          "$(grep -oE '[0-9]+ failures' "$BULOG" | grep -oE '^[0-9]+')" "0"
check     "budget: verdict present" "$(grep -c SELFTEST_BUDGET_PASS "$BULOG")" "1"
check_min "budget: rows actually run" \
          "$(grep -oE '^[0-9]+ rows' "$BULOG" | grep -oE '^[0-9]+')" 7
check     "budget: the over-budget leg stops for the budget" \
          "$(grep -c 'ok    a run PAST the printed budget stops' "$BULOG")" "1"
check     "budget: the under-budget leg does not" \
          "$(grep -c 'ok    a run UNDER the printed budget does not stop' "$BULOG")" "1"

#  budget_class lives in lib.sh precisely so this truth table can run here rather than only
#  under a weekly rig boot.  `zeroed` is the case that used to print a GREEN "deliberately
#  absent" for a rig whose budget is 12 G -- measured at 11/11 PASS before this round.
check "budget class: calibrated value"    "$(budget_class luna88k 12000000000)" "calibrated"
check "budget class: ZERO on a calibrated rig is not 'absent'" \
                                          "$(budget_class luna88k 0)"           "zeroed"
check "budget class: out of range"        "$(budget_class luna88k 5)"           "out-of-range"
check "budget class: a deliberate zero stays absent" \
                                          "$(budget_class landisk 0)"           "absent"
check "budget class: missing is never zero" "$(budget_class luna88k '')"        "unreported"

#  THE POSITIVE CONTROL IS THE NAMED SURVIVOR ITSELF, applied to COPIES -- never the repo.
#  An in-process wrong-expectation row would only prove the reporter can print FAIL; this
#  proves THE ROW KILLS THE MUTANT.  Three states stay distinguishable IN AGGREGATE: never
#  ran (empty log -- rows 1, 3 and 4 red; note that row 2 asks only for a nonzero status and
#  a never-run python3 also exits nonzero, so THAT ROW ALONE DOES NOT SEPARATE THEM, which a
#  review seat measured), ran and crashed (nonzero status, NO verdict token), ran and caught
#  (the token plus the killing row's name).  The gate is red in all three failure shapes.
ACDIR=$LOGDIR/absorb_control
rm -rf "$ACDIR"; mkdir -p "$ACDIR"
python3 - "$HERE" "$ACDIR" <<'PYCTL' > "$ACDIR/apply.log" 2>&1
import os, shutil, sys
here, out = sys.argv[1], sys.argv[2]
src = open(os.path.join(here, "drive_guest.py"), encoding="utf-8").read()
old = 'if i != -1 and "\\n" not in rest[i:] and len(rest) - i < HOLD_MAX:'
new = 'if i != -1 and len(rest) - i < HOLD_MAX:'
if src.count(old) != 1:
    print("CONTROL_STALE applies %d times" % src.count(old)); sys.exit(1)
open(os.path.join(out, "drive_guest.py"), "w", encoding="utf-8",
     newline="\n").write(src.replace(old, new))
shutil.copyfile(os.path.join(here, "selftest_absorb.py"),
                os.path.join(out, "selftest_absorb.py"))
print("CONTROL_APPLIED")
PYCTL
check     "absorb control: the mutant still applies to today's parser" \
          "$(grep -c CONTROL_APPLIED "$ACDIR/apply.log")" "1"
python3 "$ACDIR/selftest_absorb.py" > "$ACDIR/run.log" 2>&1; ACRC=$?
check     "absorb control: the mutant is REJECTED (nonzero status)" \
          "$([ "$ACRC" -ne 0 ] && echo rejected || echo "accepted rc=$ACRC")" "rejected"
check     "absorb control: it failed rather than crashed" \
          "$(grep -c SELFTEST_ABSORB_FAIL "$ACDIR/run.log")" "1"
#  A FLOOR, not an exact count.  The mutant strands every bracket-carrying line in the tail,
#  so it fails EVERY "lands in BODY" row -- three today.  Pinning the exact number would turn
#  a legitimately added row into a red gate; what must be true is that the kill comes from
#  THAT NAMED ROW and not from some unrelated collapse.
check_min "absorb control: the kill is by the named row" \
          "$(grep -c 'FAIL  lands in BODY' "$ACDIR/run.log")" 1
#  KEEP THE LOGS WHEN THE CONTROL FAILS.  Removing them unconditionally deleted the only
#  evidence at exactly the moment it was needed.
[ "$ACRC" -ne 0 ] && grep -q SELFTEST_ABSORB_FAIL "$ACDIR/run.log" && rm -rf "$ACDIR"

command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || \
    gate_skip "no C compiler on PATH"
CC=$(command -v cc || command -v gcc)
need_file "$HERE/diff_ieee_store.c" "$SEC/src/$SRC"

# Pick a configured tree: it must have the generated config.h AND the header directory.
TREE=""
for t in "$ROOT/build" /tmp/gxsec-build; do
    [ -f "$t/config.h" ] && [ -f "$t/src/include/float_emul.h" ] && { TREE=$t; break; }
done
[ -n "$TREE" ] || gate_skip "no configured tree (run gate_build.sh first)"
note "compiling against configured tree: $TREE"

# THE HONESTY LINK. Without this the gate tests whatever happens to be in a scratch
# directory, which may lag the repository by any amount.
if cmp -s "$TREE/src/$SRC" "$SEC/src/$SRC"; then
    check "compiled float_emul.c is the committed one" "identical" "identical"
else
    check "compiled float_emul.c is the committed one" "DIFFERS" "identical"
    note "the configured tree is stale -- run gate_build.sh to re-sync"
    gate_end; exit $?
fi

# #299's 2Sum exactness contract is enforced by GLOBAL build facts, not by anything
# local to the helper: it needs strict IEEE doubles, so -ffast-math (or friends) in the
# TREE's configure would break the shipped emulator while this gate -- which compiles
# with its own flags -- stayed green. A panel seat named that exact hole, so the gate
# trips on the flags themselves.
if grep -Eq -- "-ffast-math|-Ofast|-funsafe-math|-fassociative-math|-ffp-contract=fast" \
        "$SEC/configure" "$SEC/Makefile.skel" 2>/dev/null; then
    check "tree build flags preserve IEEE arithmetic (no fast-math)" "found" "absent"
else
    check "tree build flags preserve IEEE arithmetic (no fast-math)" "absent" "absent"
fi

# #303: the grep above reads the SCRIPTS; `CFLAGS=-Ofast ./configure` lands only in the
# GENERATED Makefiles, which the emulator is actually built from, while this gate compiles
# with its own -O2 -- a poisoned tree would misdecode D subnormals in the emulator with
# every offline check green. So grep what the build actually uses, in every configured
# tree present. This grep is the ONLY defence against tree-flag poisoning -- the runtime
# canary below runs in THIS gate's own -O2 binary and can only see HOST-level trouble
# (MXCSR FTZ/DAZ, a wrong rounding mode), a DIFFERENT hole (both were a panel seat's
# findings; a diff-review seat corrected the first version of this comment, which
# claimed the canary covered this one too).
GENBAD=absent
for t in "$ROOT/build" /tmp/gxsec-build; do
    [ -f "$t/Makefile" ] || continue
    if grep -Eq -- "-ffast-math|-Ofast|-funsafe-math|-fassociative-math|-ffp-contract=fast" \
            "$t/Makefile" "$t"/src/Makefile "$t"/src/*/Makefile 2>/dev/null; then
        GENBAD=found
    fi
done
check "generated Makefiles preserve IEEE arithmetic too" "$GENBAD" "absent"

BIN=$LOGDIR/diff_ieee_store
LOG=$LOGDIR/diff_ieee_store.log
if ! $CC -O2 -I"$TREE/src/include" -o "$BIN" \
        "$HERE/diff_ieee_store.c" "$TREE/src/$SRC" -lm > "$LOG" 2>&1; then
    note "compile failed:"; sed 's/^/       /' "$LOG" | head -12
    check "differential compiles and links" "no" "yes"
    gate_end; exit $?
fi
check "differential compiles and links" "yes" "yes"

"$BIN" > "$LOG" 2>&1
sed 's/^/       /' "$LOG"
echo

val() { grep -E "^$1" "$LOG" | head -1 | sed 's/.*: *//' | tr -d ' '; }

# Absolute answers first: a differential alone is relative and passes when both sides are
# wrong the same way.
check     "absolute-answer failures"               "$(val 'absolute-answer failures')" "0"
check_min "absolute-answer cases run"              "$(val 'absolute-answer cases')"    6

# NOTHING EXTRA CHANGED: no difference may appear outside the two expected groups.
check     "S-format: unexplained differences"      "$(val 'UNEXPLAINED')"       "0"
check     "S-format: in-range values moved"        "$(val 'in-range')"          "0"
# NOTHING WAS MISSED: everything inside those groups must actually differ. Without this
# half, the check only proves the differences it happened to see were allowed -- and a
# broken version that fixes overflow for negative numbers but not positive ones would
# sail through.
check     "S-format: inputs that should have moved but did not" "$(val 'MISSED')" "0"
check_min "S-format: how many inputs should have moved" "$(val 'must-differ population')" 1000
# #331: this was "D-format: change-set is empty" == 0, and its flip is the
# headline of that round -- upstream has NO gradual underflow in double
# precision (an empty "FP_SUBNORMAL: TODO" arm), so this tree now differs from
# it for every D subnormal it samples. The floor is what makes the assertion
# mean something: a bare "> 0" would be satisfied by a single surviving diff
# where the class is roughly ten thousand strong, which is the same
# cannot-fail species this gate's header warns about. Measured 9839 over the
# 20M-sample sweep (host-subnormal patterns are about 1 in 2048 of it).
check_min "D-format: subnormal change-set present" "$(val 'D-format diffs')" 9000
check_min "S-format: overflow class is non-empty"  "$(val '  of which overflow')" 1
check_min "S-format: underflow class is non-empty" "$(val '  of which negative')" 1
check_min "samples swept"                          "$(val 'samples')"       20000000
check     "clamp threshold is 2^129, not 2^128"    "$(val 'clamp-at')"          "2^129"
check     "exponent-255 threshold is 2^128"        "$(val 'exp255-at')"         "2^128"
# #331: was 2^128 -- the overflow threshold #287 fixed, which used to be the
# smallest input where the two implementations parted. The subnormal band is
# further down, so it now comes first. The overflow pins either side of it
# (clamp-at, exp255-at) are unchanged, which is what shows this moved because
# a NEW class appeared below it rather than because the old one drifted.
check     "first shipped-vs-upstream diff at 2^-149" "$(val 'first-difference-at')" "2^-149"

# #292: the mode-aware entry point, checked against INDEPENDENT oracles (the host's own
# correctly-rounded float conversion) rather than against upstream. Named vectors carry
# the cases a random sweep cannot hit -- an exact half-way tie occurs about once per 2^29
# random inputs.
check     "rm: nearest matches the host oracle"    "$(val 'rm: RN oracle')"     "0"
check     "rm: toward-zero matches its oracle"     "$(val 'rm: RZ oracle')"     "0"
check_min "rm: the mode actually changes results"  "$(val 'rm: mode-differing')" 1000000
check     "rm: D untouched under every mode"       "$(val 'rm: D mismatches')"  "0"
check     "rm: named-vector failures"              "$(val 'rm: named-vector' | cut -d'(' -f1)" "0"

# #303: the DECODE side. The canary is load-bearing for HOST-level trouble only --
# MXCSR FTZ/DAZ or a non-nearest rounding mode void every D-subnormal expectation, and
# the canary is the only check that can tell. (Tree-flag poisoning is the generated-
# Makefile grep's job above; this binary compiles with its own -O2 and cannot see tree
# flags.) It is computed with volatile operands at runtime -- a constant expression
# would fold at compile time and pass on exactly the build it exists to catch.
check     "interp: FTZ/DAZ+RN canary alive"        "$(val 'interp: FTZ')"       "alive"
check     "interp: S subnormals both signs"        "$(grep 'interp: S subnormals' "$LOG" | grep -oE '[0-9]+ bad' | cut -d' ' -f1)" "0"
check_min "interp: S population is exhaustive x2"  "$(grep 'interp: S subnormals' "$LOG" | grep -oE 'of [0-9]+' | cut -d' ' -f2)" 16777214
check     "interp: D subnormals both signs"        "$(grep 'interp: D subnormals' "$LOG" | grep -oE '[0-9]+ bad' | cut -d' ' -f1)" "0"
check_min "interp: D population not shrunken"      "$(grep 'interp: D subnormals' "$LOG" | grep -oE 'of [0-9]+' | cut -d' ' -f2)" 400000
check     "interp: D m=3/m=4 decode distinct"      "$(val 'interp: D m=3/m=4')"  "yes"
check     "interp: controls untouched"             "$(grep 'interp: controls' "$LOG" | grep -oE '[0-9]+ bad' | cut -d' ' -f1)" "0"
check     "interp: verdict"                        "$(grep -c 'INTERP_RESULT=PASS' "$LOG")" "1"

check     "verdict"                                "$(grep -c 'DIFF_PASS' "$LOG")" "1"

# ---- #392: the readiness predicate, proved offline ----------------------
# Belongs in THIS gate because it needs no emulator, no pty and no host timing --
# it replays the probes' wait() loop over a scripted byte stream. That property is
# the point: a readiness test whose verdict moved with host load would repeat the
# mistake that once false-FAILed a 45-minute battery.
#
# The four rows are a truth table, and the middle two are the interesting ones:
# changing the prompt STRING alone does not fix the defect (full+whole still
# returns after one byte), and anchoring alone does not either. Only both together
# read the reply. If a future change makes 'full-whole' pass, the predicate has
# stopped being tested rather than started working.
#
# NOTE what this does NOT prove: it tests the four FORMS, not the probes, so on
# its own it would stay green if a probe were reverted. The static census in
# gate_hygiene.sh is what binds the shipped code to this result.
#  A PER-RUN NONCE. It RAISES THE BAR AND DOES NOT CLOSE THE DOOR, and the
#  previous version of this comment claimed otherwise -- wrongly.
#
#  What it does stop: a static transcript. The nonce enters the scripted reply,
#  so the reported byte counts shift by exactly its length, and a file of frozen
#  numbers fails (measured: fake reports 53 where 59 is required).
#
#  *** WHAT IT DOES NOT STOP, MEASURED BY A SEAT: the nonce is passed as an
#  ARGUMENT TO THE VERY SCRIPT BEING VALIDATED, so a fake needs only
#  len(sys.argv[1]) to compute the affine counts. A 12-line transcript that runs
#  no loops passed all ten checks here and both pins in gate_hygiene. ***
#  An oracle that asks the prover to KNOW A PUBLIC INPUT is not an oracle that
#  asks it to DO THE WORK. A nonce only binds when it is WITHHELD -- the gate
#  would have to recompute the expected stream itself, or vary something whose
#  effect is not a length the script is handed. That is a design change, filed
#  rather than rushed; see the queue entry on binding this test to real work.
#  Recorded here rather than quietly weakened, because a check that overstates
#  what it proves is worse than one that states its limit.
#  d1: the driver must put BOTH pty logs where $LOGDIR says.  This cannot be a gate-5 row:
#  in the default battery $LOGDIR IS the string the driver used to hardcode, so such a row
#  passes on the unfixed code -- measured.  selftest_logdir.py points LOGDIR somewhere else
#  and runs a stub in place of the emulator, so it needs no rig and no boot.  It sets the
#  variable itself rather than being invoked as `env LOGDIR=... `, which would export from
#  OUTSIDE and stay green with lib.sh's export missing (half the defect).
DLOG=$LOGDIR/selftest_logdir.log
python3 "$HERE/selftest_logdir.py" > "$DLOG" 2>&1 || true
dlv() { grep -m1 -oE "$1=[a-z]+" "$DLOG" | cut -d= -f2; }
check     "driver honours \$LOGDIR for the console log" "$(dlv console_log_in_logdir)" "yes"
check     "driver honours \$LOGDIR for the raw log"     "$(dlv raw_log_in_logdir)"     "yes"

RNONCE="n$$"
RLEN=${#RNONCE}
RLOG=$LOGDIR/readiness_predicate.log
python3 "$HERE/readiness_predicate_test.py" "$RNONCE" > "$RLOG" 2>&1 || true
rbytes() { grep -E "^READINESS_ROW +$1 " "$RLOG" | grep -oE 'bytes=[0-9]+' | cut -d= -f2; }
rrow() { grep -E "^READINESS_ROW +$1 " "$RLOG" | grep -oE 'saw_reply=[a-z]+' | cut -d= -f2; }
check     "readiness: bare+whole returns early"     "$(rrow bare-whole)" "no"
check     "readiness: full+whole ALSO returns early" "$(rrow full-whole)" "no"
check     "readiness: bare+mark returns early"      "$(rrow bare-mark)"  "no"
check     "readiness: full+mark reads the reply"    "$(rrow full-mark)"  "yes"
check     "readiness: rstrip re-matches old prompt" "$(grep -c 'READINESS_LEFTOVER.*keeps_prompt=yes' "$RLOG")" "1"
#  The two LATE-PROMPT rows are the ECHO conjunct's only behavioural coverage.
#  A seat measured that the echo half could be deleted from all fourteen sites
#  with every gate still green, because the four rows above exercise the mark and
#  the prompt string and nothing exercised the echo. These two do: a stale prompt
#  arriving AFTER the mark cannot be distinguished by byte anchoring, only by
#  requiring the new command's own echo first.
check     "readiness: late prompt fools a no-echo wait"  "$(rrow late-noecho)" "no"
check     "readiness: echo guard survives a late prompt" "$(rrow late-echo)"   "yes"
#  THE ANTI-FAKE CHECK. Both counts are affine in the nonce length, so a printed
#  transcript OF FROZEN NUMBERS cannot satisfy them -- but one that reads the
#  nonce from argv can, which is why this is a bar and not a door (see above).
#  53 and 60 are the measured baselines at
#  nonce="" and the arithmetic was verified at lengths 0, 5 and 10.
check     "readiness: full-mark byte count tracks the nonce" "$(rbytes full-mark)" "$((53 + RLEN))"
check     "readiness: late-echo byte count tracks the nonce" "$(rbytes late-echo)" "$((60 + RLEN))"
check     "readiness: offline verdict"              "$(grep -c 'READINESS_RESULT=6/6' "$RLOG")" "1"

# ---- #400: the SH-4 TMU tick arithmetic -----------------------------------------
# Same shape as the float_emul differential above, and for the same reason: the driver
# stubs fatal() and #includes dev_sh4.c, so the sh4_timer_tick() that runs IS the one
# that ships. sh4_timer_tick is static, so there is no way to link it without including
# the file -- which is precisely what makes a transcription impossible here.
#
# The rows are exact values, not "did it move". The defect being guarded pinned TCNT at
# zero permanently on a booting OpenBSD/landisk guest after 515.4 s; the no-freeze row
# reproduces that in milliseconds instead of a 9.5-minute boot.
#
# The three-timer row exists because a measure seat found two wrong variants -- tcor[0]
# for tcor[i], and cnt from tcnt[0] -- that are BIT-IDENTICAL to correct code across all
# 824288 single-timer cases, because every other row starts timer 0 only. They are the
# typo this rewrite newly risks. Measured: that row alone kills both.
#  #427-#429: the timer core's frequency domain and its catch-up bound, driven OFFLINE.
#  The driver #includes the shipped src/core/timer.c (timer_tick is static), stubs only
#  gettimeofday, and never installs a signal handler -- so no host clock enters and these
#  rows are not load-sensitive.  MEASURED against six mutants in copies: no ceiling,
#  clamp-below-the-early-out, unbounded catch-up, both-clamps-written-plainly, and the
#  drop-the-backlog policy all go red; the shipped file passes.
TIMBIN=$LOGDIR/diff_timer
TIMLOG=$LOGDIR/diff_timer.log
#  -D_POSIX_C_SOURCE, because strict c99 hides struct sigaction and SA_RESTART, which the
#  shipped timer.c uses -- the driver never calls that code, but it still has to compile.
if ! $CC -O1 -std=c99 -D_POSIX_C_SOURCE=200809L -I"$SEC/src/include" \
        -o "$TIMBIN" "$HERE/diff_timer.c" -lm > "$TIMLOG" 2>&1; then
    note "timer differential compile failed:"; sed 's/^/       /' "$TIMLOG" | head -12
    check "timer: compiles against the real timer.c" "no" "yes"
else
    check "timer: compiles against the real timer.c" "yes" "yes"
    "$TIMBIN" > "$TIMLOG" 2>&1
    sed 's/^/       /' "$TIMLOG"
    check     "timer: row failures" \
              "$(grep -oE '[0-9]+ failures' "$TIMLOG" | grep -oE '^[0-9]+')" "0"
    #  THE FLOOR MUST EQUAL THE ROW COUNT, and it did not: it stood at 13 while the driver
    #  ran 14, so DELETING THE IDENTITY ROW LEFT THE GATE FULLY GREEN -- the one defect the
    #  identity row exists to prevent.  Two review seats read it independently and a third
    #  measured it.  A floor set one below the count is not a weaker check, it is no check.
    check_min "timer: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$TIMLOG" | grep -oE '^[0-9]+')" 24
    check     "timer: offline verdict" "$(grep -c 'DIFF_TIMER_PASS' "$TIMLOG")" "1"
    #  Name every row that is the SOLE detector of something, so deleting one is a red row
    #  rather than a quieter file.  Each line below names a mutant that survived the first
    #  version of this differential and was killed by adding that row.
    check "timer: the NaN row is present" \
          "$(grep -c 'NaN lands on the FLOOR' "$TIMLOG")" "1"
    check "timer: the idempotence row is present" \
          "$(grep -c 'five identical requests reset the schedule' "$TIMLOG")" "1"
    check "timer: the anti-regression rows are present" \
          "$(grep -c 'still delivers ~' "$TIMLOG")" "2"
    #  The rows that defend the CONSTANTS.  Every other row reads them from the header and
    #  is therefore green for any value; these two are derived from outside it.
    check "timer: the ceiling-is-INT_MAX row is present" \
          "$(grep -c 'the ceiling IS INT_MAX' "$TIMLOG")" "1"
    check "timer: the floor-is-reachable row is present" \
          "$(grep -c "the floor's interval is still a reachable" "$TIMLOG")" "1"
    #  The absolute floor that defends TIMER_MAX_CATCHUP's value: 40 MHz is the pmax rate,
    #  so this is the offline half of a case the weekly battery boots.
    check "timer: the 40 MHz keeps-time row is present" \
          "$(grep -c 'a 40 MHz timer' "$TIMLOG")" "1"
    #  The bound's EXACT count, and the policy it protects.
    check "timer: the exact-bound row is present" \
          "$(grep -c 'delivers exactly the bound' "$TIMLOG")" "1"
    check "timer: the backlog-retained row is present" \
          "$(grep -c 'the retained backlog' "$TIMLOG")" "1"
    #  The instrument's own self-check: without it the stall above can go inert again, as
    #  it silently was when this differential first shipped.
    check "timer: the stall-is-real row is present" \
          "$(grep -c 'arming the resync really moves' "$TIMLOG")" "1"
    #  The reporting path, which had no row at all: deleting the flag assignment from the
    #  signal handler passed everything.
    check "timer: the cap-is-reported row is present" \
          "$(grep -c 'reports it exactly once' "$TIMLOG")" "1"
    check "timer: the complaint-is-made row is present" \
          "$(grep -c 'complains exactly once' "$TIMLOG")" "1"
    check "timer: the interval-is-reciprocal row is present" \
          "$(grep -c 'the interval is exactly 1/freq' "$TIMLOG")" "1"
fi

#  #430-#431: memory_rw() translated the START vaddr once and then copied the whole length
#  from that page's host pointer, so a page-crossing access walked PHYSICALLY contiguous
#  host bytes across a VIRTUALLY contiguous guest span.  Driven OFFLINE, because the defect
#  needs two pages adjacent virtually and NOT adjacent physically and no rig in this tree can
#  be made to produce that on demand -- the map comes from a stub instead.
#  MEASURED against the pre-fix file (git show b9daca1:src/cpus/memory_rw.c): 11 of these
#  rows go red, including the reproduction (a straddling read returning the physically-
#  following page), the straddling WRITE corrupting an unrelated page, the device case, and
#  the missing fault.  -I"$SEC/src" because the driver includes "include/misc.h" the way the
#  cpu files do.
MRWBIN=$LOGDIR/diff_memory_rw
MRWLOG=$LOGDIR/diff_memory_rw.log
#  -fno-optimize-sibling-calls IS LOAD-BEARING, and only for the stack row.  gcc 15.2.1
#  DOES eliminate the tail call at -O2, so a recursion mutant measured a 96-byte span and
#  the "it is a loop" row passed under the very defect it exists to catch -- vacuous.
#  With the flag: loop 0 bytes, recursion 1,572,768.  Measured both ways by a review seat.
if ! $CC -O2 -fno-optimize-sibling-calls -std=c99 -D_POSIX_C_SOURCE=200809L \
        -D_DEFAULT_SOURCE -I"$SEC/src" \
        -o "$MRWBIN" "$HERE/diff_memory_rw.c" -lm > "$MRWLOG" 2>&1; then
    note "memory_rw differential compile failed:"; sed 's/^/       /' "$MRWLOG" | head -12
    check "memory_rw: compiles against the real memory_rw.c" "no" "yes"
else
    check "memory_rw: compiles against the real memory_rw.c" "yes" "yes"
    "$MRWBIN" > "$MRWLOG" 2>&1
    sed 's/^/       /' "$MRWLOG"
    check     "memory_rw: row failures" \
              "$(grep -oE '[0-9]+ failures' "$MRWLOG" | grep -oE '^[0-9]+')" "0"
    #  The floor is the EXACT count, not one below it: a floor set under the count makes the
    #  identity row deletable with the gate still green, which is what #430's sibling round
    #  had to fix in the timer differential.
    #
    #  *** AND THIS PIN HAD DRIFTED SIX BELOW ITS OWN COUNT, UNDER THAT VERY SENTENCE. ***
    #  17 against a harness printing 23.  A reading seat noticed it; a measuring seat then
    #  DEMONSTRATED it rather than arguing it -- deleted six unpinned rows (A1, B2, B3, C1,
    #  C2, D2, none named by any presence check), retuned the identity constant 23 -> 17 as a
    #  legitimate edit would, and ran this gate's own memory_rw block verbatim: 14 OF 14
    #  GREEN with six rows gone, identity row included.  (The first record of this said
    #  "13 of 13"; a pass-2 seat reproduced the experiment and counted 14.  Substance
    #  identical, number off by one, and it appeared in two places.)
    #
    #  Rows were added in later rounds and the pin was not moved with them.  Every other
    #  floor in this gate was then swept the same way.  THERE ARE THIRTEEN, and the first
    #  version of this list named NINE -- a pass-2 seat measured all thirteen and named the
    #  four omitted: absorb 52/52, budget 7/7, autodev generator 8/8 and DISK GEOMETRY 34/34,
    #  the last of which is a diff_*.c and so the omission a reader would notice.  In full:
    #  absorb 52, budget 7, timer 24, memory_rw 23 (this one, after the fix), footbridge 19,
    #  m8820x 25, m8invread 27, TMU 16, wdc 16, autodev 8, io 45, geom 34, parser 37 -- all
    #  exact, so the drift is bounded to this one.  A DOCTRINE STATED IN A COMMENT IS NOT A MECHANISM:
    #  nothing in the battery compares a floor to the count it claims to pin, which is why
    #  this went six rounds unnoticed while the sentence above kept asserting otherwise.
    check_min "memory_rw: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$MRWLOG" | grep -oE '^[0-9]+')" 23
    check     "memory_rw: offline verdict" "$(grep -c 'DIFF_MEMORY_RW_PASS' "$MRWLOG")" "1"
    #  Name each row that is the SOLE detector of something, so deleting one is a red row
    #  rather than a quieter file.
    check "memory_rw: the straddling-read row is present" \
          "$(grep -c 'straddling read takes the VIRT-next page' "$MRWLOG")" "1"
    check "memory_rw: the write-corruption rows are present" \
          "$(grep -c 'the PHYS-next page was NOT corrupted' "$MRWLOG")" "1"
    check "memory_rw: the device-straddle row is present" \
          "$(grep -c 'device head, RAM tail' "$MRWLOG")" "1"
    check "memory_rw: the faulting-tail rows are present" \
          "$(grep -c 'bad tail returns FAILED' "$MRWLOG")" "2"
    #  The two rows that defend the DESIGN rather than the fix: PHYSICAL must not be split,
    #  and the split must not consume stack per page.
    check "memory_rw: the PHYSICAL-not-split row is present" \
          "$(grep -c 'splits per MEMBLOCK, not per page' "$MRWLOG")" "1"
    check "memory_rw: the loop-not-recursion row is present" \
          "$(grep -c 'stack does not grow per page' "$MRWLOG")" "1"
    #  The two rows the pass-2 review forced, each covering a defect IN THE FIX: a 4 KB
    #  split granule silently misses a 1 KB mapping (ARM tiny pages, SH SZ_1K), and the
    #  split broke #244's promise that a failed read leaves the WHOLE buffer zeroed.
    check "memory_rw: the 1 KB-granule row is present" \
          "$(grep -c 'across a 1 KB mapping boundary' "$MRWLOG")" "1"
    check "memory_rw: the first-chunk-fault rows are present" \
          "$(grep -c 'first-chunk fault' "$MRWLOG")" "1"
    check "memory_rw: the one-byte-tail rows are present" \
          "$(grep -c '1-byte tail across' "$MRWLOG")" "2"
    check "memory_rw: the identity row is present" \
          "$(grep -c 'IDENTITY row count' "$MRWLOG")" "1"
fi

#  #432: the footbridge timer divided by a guest-written zero -- a guest-reachable HOST CRASH,
#  reproduced independently by two seats.  Driven OFFLINE because THERE IS NO NETWINDER OR CATS
#  RIG ANYWHERE IN THIS TREE: nothing here boots a machine that has a footbridge, so this is not
#  the cheapest detector, it is the only possible one.  The driver #includes the shipped device,
#  exactly as diff_sh4_tmu.c does.
#  -Wl,--gc-sections is LOAD-BEARING: without it the link needs eleven more symbols.  The
#  trade-off, stated so it is not mistaken for coverage: it drops DEVINIT, so this file cannot
#  test devinit.  -D_DEFAULT_SOURCE is required for random() under -std=c99.
#  MEASURED against seven mutants in copies -- all red, control passes: the zero guard removed
#  (dies BY SIGNAL 8, the crash itself), the prescaler back to a signed shift, the tick site
#  prescaling, TIMER_EXTERNAL falling through as a bare x16, and the three that PASS 2 found
#  surviving the first fifteen rows -- one character deleting the prescaler from the RATE domain,
#  the tick counter replaced by a constant, and normalize-at-write (the design this round
#  REJECTED).  An eighth is EQUIVALENT and deliberately not counted: on a uint64_t, `<<= 4` and
#  `*= 16` are the same operation for every value in range -- it is the TYPE that makes it
#  equivalent, not the magnitude.
#
#  ON THE FORKS, CORRECTED: two rows fork, and the first version of this comment said that made
#  a re-crashing mutant a named-row KILL rather than a census FAULT.  MEASURED FALSE by two seats
#  independently -- D2 is UNFORKED and reaches the divide first, so an unconditional
#  re-introduction of the crash takes the binary down there, before F1's fork.  G1's fork IS
#  load-bearing (the CONTROL-arm exit(1) is reachable nowhere else in-process) and F1's contains
#  a narrower class (a zero-guard conditioned on the prescaler bits survives D2 and dies in F1).
#  Detection is unaffected either way: every grep below fails on a truncated log.
FBBIN=$LOGDIR/diff_footbridge
FBLOG=$LOGDIR/diff_footbridge.log
if ! $CC -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE \
        -I"$SEC/src" -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$FBBIN" "$HERE/diff_footbridge.c" -lm > "$FBLOG" 2>&1; then
    note "footbridge differential compile failed:"; sed 's/^/       /' "$FBLOG" | head -12
    check "footbridge: compiles against the real dev_footbridge.c" "no" "yes"
else
    check "footbridge: compiles against the real dev_footbridge.c" "yes" "yes"
    "$FBBIN" > "$FBLOG" 2>&1
    sed 's/^/       /' "$FBLOG"
    check     "footbridge: row failures" \
              "$(grep -oE '[0-9]+ failures' "$FBLOG" | grep -oE '^[0-9]+')" "0"
    check_min "footbridge: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 19
    check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
    #  Name each row that is the SOLE detector of something.
    check "footbridge: the zero-load row is present" \
          "$(grep -c 'load 0 becomes the full 24-bit span' "$FBLOG")" "1"
    check "footbridge: the prescaler-overflow rows are present" \
          "$(grep -c 'does not overflow\|does not wrap to zero' "$FBLOG")" "2"
    check "footbridge: the TIMER_EXTERNAL row is present" \
          "$(grep -c 'not silently read as x16' "$FBLOG")" "1"
    check "footbridge: the counter-domain row is present" \
          "$(grep -c 'leave the 24-bit counter in range' "$FBLOG")" "1"
    #  The three rows PASS 2 added, each the SOLE detector of a mutant that survived the first
    #  fifteen: the rate consumer really prescaling (one character defeated it), the counter
    #  tracking the guest's OWN load (every earlier tick row used load 0, for which a constant
    #  is the right answer), and the LOAD register reading back unmodified (nothing drove the
    #  access handler at all, so the design this round REJECTED passed).
    check "footbridge: the rate-prescaler row is present" \
          "$(grep -c 'RATE consumer really applies' "$FBLOG")" "1"
    check "footbridge: the counter-tracks-load row is present" \
          "$(grep -c "below the guest's OWN load" "$FBLOG")" "1"
    check "footbridge: the LOAD read-back rows are present" \
          "$(grep -cE 'reads back as 0, not normalised|stays 0 on read-back' "$FBLOG")" "2"
    #  The two forked end-to-end rows: these are the ones that prove the HOST SURVIVES, and
    #  they are forked so a mutant that re-crashes is a named-row KILL rather than a census
    #  FAULT that takes the gate binary with it.
    check "footbridge: the end-to-end survival rows are present" \
          "$(grep -c 'does not kill the host\|does not exit()' "$FBLOG")" "2"
    check "footbridge: the identity row is present" \
          "$(grep -c 'IDENTITY row count' "$FBLOG")" "1"
fi

#  #433: the M8820x CMMU terminated the HOST process on an ordinary guest register access --
#  measured at 1007 of 1024 word offsets on a plain READ, on luna88k, which BOOTS in this tree.
#  Driven offline for BREADTH (1024 offsets x 2 directions x 256 commands is not a pty job);
#  the online cold-debugger probe that proves guest-instruction reachability is filed separately.
#  THE KILL CRITERION IS THE EXIT STATUS, not "the child died": the first reproduction of this
#  defect overcounted by exactly six in each direction because six offsets crashed in the
#  HARNESS (the register-file arm invalidates before the writeflag check, so it fires on reads,
#  and the driver had left that callback NULL).  A signal death is reported as a FAULT here,
#  never counted as a detection.
M8BIN=$LOGDIR/diff_m8820x
M8LOG=$LOGDIR/diff_m8820x.log
if ! $CC -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE \
        -I"$SEC/src" -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$M8BIN" "$HERE/diff_m8820x.c" -lm > "$M8LOG" 2>&1; then
    note "m8820x differential compile failed:"; sed 's/^/       /' "$M8LOG" | head -12
    check "m8820x: compiles against the real dev_m8820x.c" "no" "yes"
else
    check "m8820x: compiles against the real dev_m8820x.c" "yes" "yes"
    "$M8BIN" > "$M8LOG" 2>&1
    sed 's/^/       /' "$M8LOG"
    check     "m8820x: row failures" \
              "$(grep -oE '[0-9]+ failures' "$M8LOG" | grep -oE '^[0-9]+')" "0"
    check_min "m8820x: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$M8LOG" | grep -oE '^[0-9]+')" 25
    check     "m8820x: offline verdict" "$(grep -c 'DIFF_M8820X_PASS' "$M8LOG")" "1"
    #  The whole-window sweep, and the harness-fault rows that keep its number honest.
    check "m8820x: the whole-window sweep rows are present" \
          "$(grep -cE 'kills the host' "$M8LOG")" "2"
    check "m8820x: the harness-fault rows are present" \
          "$(grep -c 'harness faults' "$M8LOG")" "2"
    #  The latches -- plural, and that is the point.  There are TWO independent flags
    #  (reported_offset and reported_command), and for a while only the first had a row:
    #  the command control issues ONE command, and one command complains exactly once
    #  whether the flag is latched or not.  Both must be present, or the gate greens an
    #  unlatched command path -- a guest-drivable stderr flood on a path a real boot
    #  exercises 640,016 times per boot.
    check "m8820x: BOTH latch rows are present (offset and command)" \
          "$(grep -c 'complain exactly once' "$M8LOG")" "2"
    #  THE ROW THAT DEFENDS THE FOLD.  Without the folded PATC flushes, this round's own
    #  complain-and-continue would have turned FLUSH_SUPER_LINE into a silently ignored TLB
    #  flush -- a defect worse than the crash it removed.  Checked white-box, plus its control.
    check "m8820x: the PATC-invalidation row is present" \
          "$(grep -c 'folded PATC flushes invalidate' "$M8LOG")" "1"
    check "m8820x: both fold controls are present" \
          "$(grep -cE 'CONTROL: an undefined command|CONTROL: a CACHE command' "$M8LOG")" "2"
    #  Values, not survival (rounds 79/80).
    check "m8820x: the seeded-IDR value rows are present" \
          "$(grep -c 'seeded 88200 rev-9 id\|does not corrupt it' "$M8LOG")" "2"
    #  The rows PASS 2 forced.  D1 seeds ONE entry at the flushed address, so it can only
    #  show that a MATCHING entry goes away -- eleven of twenty-one mutants survived it,
    #  the cheapest being ONE DELETED CHARACTER (`!all` -> `all`) that turns every
    #  FLUSH_*_ALL into a single-page flush: the exact under-invalidating TLB this round
    #  exists to prevent.  D3-D6 seed a SPREAD and assert which entries SURVIVE.
    check "m8820x: the flush-scope rows are present"           "$(grep -cE 'drops exactly one entry|drops every supervisor entry|leaves every supervisor entry|drops at least what a PAGE flush|drops every user entry' "$M8LOG")" "5"
    #  D7 uses a counter that was already in the file and never asserted on: clearing the
    #  PATC while leaving the emulator's OWN translation cache is the same failure by
    #  another route.
    check "m8820x: the dyntrans-purge row and its control are present"           "$(grep -cE "purges the emulator's own cache|a cache command purges nothing" "$M8LOG")" "2"
    #  D9/D10 are coupled: if a guest could store to SSR it could set the V bit, and then a
    #  dropped PROBE would read back a plausible-looking VALID translation instead of a
    #  deterministic miss -- which is the command arm's own stated argument.
    check "m8820x: the write-is-dropped rows are present"           "$(grep -cE 'dropped, not stored|cannot fake a valid translation' "$M8LOG")" "2"
    check "m8820x: the identity row is present" \
          "$(grep -c 'IDENTITY row count' "$M8LOG")" "1"
fi

#  #434 -- a guest READ of six CMMU registers purged the whole translation cache.
#
#  THE ROWS THAT MATTER HERE ARE THE ARGUMENT ROWS, and that is not a stylistic
#  preference.  A measuring seat built the one-identifier mutant
#  INVALIDATE_ALL -> INVALIDATE_VADDR as a real emulator and BOOTED THE luna88k RIG
#  WITH IT: 1:1:1 to `login:`, no diagnostics.  The purge is gutted to virtual page
#  0 -- under-invalidation, the dangerous direction -- while the CALL COUNT stays
#  bit-identical.  A count-based offline row cannot catch it, and THAT THREE-RUN
#  BOOT-TO-LOGIN TRIAL did not; a different workload or assertion on the same rig
#  might.  The likely masking mechanism is that the guest issues ~603,000 SCR
#  flushes per boot, each doing its own INVALIDATE_ALL -- BELIEVED, since a
#  successful boot alongside a plausible mechanism is not established attribution.
#  ARGUMENT-INSPECTING ROWS are what catch it, F1 AND F2 both, which is why the
#  named checks below pin the ARGUMENT rows and the cpu/cmmu rows and not the
#  totals.
#
#  *** THESE THREE SENTENCES WERE RETRACTED IN diff_m8invread.c AND SURVIVED HERE
#  VERBATIM FOR ONE PASS. ***  A pass-2 seat grepped and found each phrase alive in
#  exactly one file -- this one.  That is the project's own "when correcting a
#  claim, grep for its siblings" rule failing on its first application, in the very
#  round that wrote the corrections.  A retraction that lives in one file is half a
#  retraction.
IVBIN=$LOGDIR/diff_m8invread
IVLOG=$LOGDIR/diff_m8invread.log
#  WHICH FLAGS ARE ACTUALLY LOAD-BEARING, ABLATED ONE AT A TIME RATHER THAN ASSUMED.
#  The first version of this comment said "-I$SEC/src and -lm are BOTH load-bearing";
#  a pass-2 seat compiled all four variants and measured:
#      -I"$SEC/src"          LOAD-BEARING -- without it, `fatal error: include/misc.h`
#      -Wl,--gc-sections     LOAD-BEARING -- without it, `undefined reference to
#                            memory_device_register` from DEVINIT(m8820x).  It was NOT
#                            named, which is the worst case: the one nobody knew about.
#      -lm                   NOT load-bearing -- links and passes 21/21 without it.
#  The command was right and the explanation was wrong, which is the failure mode a
#  comment has that code does not.  Fitting, since this block's whole point is a lesson
#  about copying a neighbouring block: it was copied from the SH-4 TMU block, whose
#  differential includes nothing from src/, and the gate caught THAT loudly -- a compile
#  failure is a FAIL here, never a skip.
if ! $CC -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE         -I"$SEC/src" -I"$SEC/src/include" -I"$SEC/src/include/thirdparty"         -ffunction-sections -fdata-sections -Wl,--gc-sections         -o "$IVBIN" "$HERE/diff_m8invread.c" -lm > "$IVLOG" 2>&1; then
    note "m8invread differential compile failed:"; sed 's/^/       /' "$IVLOG" | head -12
    check "m8invread: compiles against the real dev_m8820x.c" "no" "yes"
else
    check "m8invread: compiles against the real dev_m8820x.c" "yes" "yes"
    "$IVBIN" > "$IVLOG" 2>&1
    sed 's/^/       /' "$IVLOG"
    check     "m8invread: row failures"               "$(grep -oE '[0-9]+ failures' "$IVLOG" | grep -oE '^[0-9]+')" "0"
    check_min "m8invread: rows actually run"               "$(grep -oE '^[0-9]+ rows' "$IVLOG" | grep -oE '^[0-9]+')" 27
    check     "m8invread: offline verdict" "$(grep -c 'DIFF_M8INVREAD_PASS' "$IVLOG")" "1"
    #  The defect row and its per-register twin: an aggregate alone misses a mutant
    #  that moves a purge between registers, which a seat named explicitly.
    check "m8invread: the read-side rows are present"           "$(grep -cE '^  (ok|FAIL) +(E1|E2) ' "$IVLOG")" "2"
    #  THE ARGUMENT ROWS.  See the comment above -- these are the only defence
    #  against a mutant that keeps the count and guts the flags.
    check "m8invread: the purge-ARGUMENT rows are present"           "$(grep -cE '^  (ok|FAIL) +(F1|F2|F3) ' "$IVLOG")" "3"
    #  The two-cpu row.  repro_m8invread.c and diff_m8820x.c are both single-cpu and
    #  are structurally blind to the wrong-receiver mutant; this row is not.
    check "m8invread: the two-cpu receiver rows are present"           "$(grep -cE '^  (ok|FAIL) +(G1|G2) ' "$IVLOG")" "2"
    #  G3/G4/G5 and E10, all four from mutants a pass-2 seat BUILT AND RAN against the
    #  17-row version.  Three survived it: a read purge gated on the register's VALUE
    #  (which restores HALF the removed purges and boots the rig 1:1:1), the same
    #  one-identifier swap applied to the REGS pointer rather than the callback receiver,
    #  and cmmu[d->cmmu_nr] -> cmmu[0].  All three were invisible because the fixture had
    #  ONE cmmu object, cmmu_nr always 0, and a memset-zero register file on every read.
    check "m8invread: the register-file and second-cmmu rows are present"           "$(grep -cE '^  (ok|FAIL) +(G3|G4|G5) ' "$IVLOG")" "3"
    check "m8invread: the nonzero-READ row is present"           "$(grep -cE '^  (ok|FAIL) +(E10) ' "$IVLOG")" "1"
    #  Idempotency: the brace-drop mutant makes a READ zero the register, and only a
    #  SECOND read can see it because odata is snapshotted before the switch.
    check "m8invread: the idempotency and read-back rows are present"           "$(grep -cE '^  (ok|FAIL) +(E7|E8) ' "$IVLOG")" "2"
    #  E9, and it is NOT redundant with E8.  A pass-2 seat appended ONE token to the
    #  production condition -- `&& idata` -- and it survived all sixteen rows: a zero
    #  write then neither purges nor stores, so writing 0 to a previously nonzero SAPR
    #  silently fails to disable that context.  Every other write row used nonzero data,
    #  and E8's single zero goes to a register fresh() had already zeroed, so it was
    #  never a TRANSITION.  A value table that merely CONTAINS zero proves nothing.
    #  *** THE TITLE THIS GREPPED FOR NO LONGER EXISTS, AND THAT IS THE POINT. ***
    #  It was 'nonzero->ZERO write still purges once'.  #435 SPLIT that row, because it
    #  welded two properties together -- "still purges once AND still stores" -- and the
    #  split moved one half and not the other.  A presence check keyed to a title is a
    #  string dependency on a file it does not own, so a legitimate row edit reddens the
    #  gate on a PRESENCE check while the row itself is fine.  This project has hit that
    #  shape before under the name "the padded-column grep trap"; a pass-2 seat named it
    #  again here, in advance, which is the only reason the gate and the row moved in the
    #  same commit.  Both halves are required, so a future edit cannot quietly drop one.
    #  ANCHORED ON THE ROW IDENTIFIERS, not on prose.  The first version of this check
    #  grepped 'purges exactly as much as it owes' and expected 3 -- which worked only
    #  because that phrase ALSO matches E4, so the count was two real rows plus an
    #  accident.  A pass-2 seat pointed out that this is exactly the title-string
    #  dependency the comment above criticises, committed in the same edit that
    #  criticised it.  E9a/E9b are stable identifiers; the prose can now be reworded
    #  without reddening a presence check.
    check "m8invread: BOTH halves of the nonzero->zero row are present"           "$(grep -cE '^  (ok|FAIL) +E9[ab] ' "$IVLOG")" "2"
    #  F4 is #435's one genuinely new row: purge-only-on-change is the likeliest mutant to
    #  be written by accident, because the BATC arm does exactly that thirty lines away.
    #  G6-G9.  #435 created a SECOND store site, and G1-G5 all drive CMMU_SAPR, which the
    #  split left in the OTHER arm -- so the new arm had ZERO owner/cmmu coverage, and every
    #  purge-asserting row ran with both selectors at 0 because fresh() memsets dev.  A
    #  pass-2 measure seat drove FIVE REAL DEFECTS through that gap, the smallest being one
    #  appended `&& d->cmmu_nr == 0`.  MEASURED: the data CMMU takes 51.9% of all SAR writes
    #  per boot, and a witness driving SAR through the handler shows the WRONG PAGE flushed
    #  and a stale supervisor translation kept.
    #
    #  WHEN A ROUND SPLITS AN ARM, EVERY ROW THAT PINNED A PROPERTY OF THE OLD ARM NOW PINS
    #  IT FOR ONLY ONE HALF.  Re-pinning the rows that go RED is the obvious half; the rows
    #  that stay GREEN while quietly covering less are the half that gets missed.
    check "m8invread: the split-arm selector rows are present" \
          "$(grep -cE '^  (ok|FAIL) +(G6|G7|G8|G9) ' "$IVLOG")" "4"
    check "m8invread: the same-value-write row is present"           "$(grep -cE '^  (ok|FAIL) +(F4) ' "$IVLOG")" "1"
    #  The neighbouring arm, ~603,000 purges/boot: nothing above would notice its loss.
    check "m8invread: the SCR-arm control rows are present"           "$(grep -cE '^  (ok|FAIL) +(H1|H2) ' "$IVLOG")" "2"
    check "m8invread: identity row present"           "$(grep -c 'IDENTITY row count' "$IVLOG")" "1"
fi

# ---------------------------------------------------------------------------
#  CAN THESE DETECTORS STILL FAIL?  (#436)
#
#  Gate 3 is the battery's only failability control and it mutates ONE file,
#  src/core/float_emul.c.  Eleven differentials live here; gate 3 names one.  A
#  measuring seat reproduced the consequence: stub check() so it never compares,
#  and 118 rows across five detectors print `ok`, keep their row counts, keep
#  their identity rows, keep their verdict tokens -- and detect NOTHING, with
#  every assertion in this file green.
#
#  The reason was structural, not an oversight in any one row: every assertion in
#  this file grepped the detector's own stdout, and all of that stdout is downstream
#  of the single comparison the stub removes.  They were ONE EQUIVALENCE CLASS, and
#  the stub stepped over all of it at once.
#
#  PAST TENSE ON PURPOSE.  A pass-2 seat pointed out that this sentence was written
#  in the PRESENT tense by the very hunk that falsified it: the five selfmutant_one
#  checks grep the HELPER's output (varied input) and the manifest checks grep the
#  FILESYSTEM, so a handful of this gate's assertions are now outside the class.
#  That is the whole point of adding them, and stating it as a present fact would
#  have made the comment wrong the moment it landed.  Only a check that VARIES THE INPUT and
#  demands the output track it escapes.
#
#  TWO CONTROLS, COVERING DIFFERENT FAILURES, NEITHER SUBSTITUTING FOR THE OTHER:
#    * the in-detector SELFCHECK row (in the .c files) -- feeds check() a
#      mismatch and requires the failure counter to move.  Covers EVERY row in
#      its file against the comparator dying.  Free, no extra compile.
#    * the self-mutants below -- break the code the detector watches and require
#      the NAMED row to catch it.  Covers ONE site against a fixture that has
#      stopped reaching the code.  Measured: the SELFCHECK is blind to a row
#      rewritten to compare the subject against itself; a pinned mutant is not.
#
#  WHAT THIS DOES NOT PROVE, said plainly because the honest scope is the whole
#  point.  A seat stubbed every row EXCEPT the ones each mutant kills and both
#  this gate and the self-mutant stayed green -- 23 of 24 rows inert for timer,
#  25 of 27 for m8invread.  So this is a LIVENESS CONTROL: it proves the detector
#  is not wholly inert and that one named row still fires.  It is not a census
#  and must never be read as "the detector is fine".  Going from 0 to 1 is not
#  false comfort; CALLING 1 "the detector works" is.
selfmutant_one() {   # harness subject stem row-id
    local h="$1" subj="$2" stem="$3" row="$4"
    local o="$HERE/selfmutants/$stem.old" n="$HERE/selfmutants/$stem.new"
    if [ ! -f "$o" ] || [ ! -f "$n" ]; then
        check "selfmutant $stem: fragments present" "no" "yes"; return
    fi
    local out
    out=$(python3 "$HERE/selfmutant.py" "$h" "$subj" "$o" "$n" "$row" 2>&1)
    printf '%s\n' "$out" | grep -E '^       ' | sed 's/^/    /'
    #  ASSERT THE OK TOKEN IS PRESENT, never "FAIL is absent": a setup error emits
    #  neither, so a negative form is satisfied by a control that never ran.
    check "selfmutant $stem: the detector still detects, via its named row" \
          "$(printf '%s' "$out" | grep -c 'SELFMUTANT_OK')" "1"
}
#  *** F1: THE SELFCHECK ROW NEEDED A PRESENCE CHECK, AND NOT HAVING ONE WAS THE WORST
#  DEFECT IN THE FIRST VERSION OF THIS ROUND. ***  A pass-2 seat deleted the whole SELFCHECK
#  block from all five detectors and measured: gate 2 stayed PASS at the SAME check count with
#  ZERO red rows, byte-identical to baseline, and all five self-mutants still OK.
#
#  It is unprotected PRECISELY BECAUSE THE BOOKKEEPING IS CORRECT: the row restores `rows`, so
#  it is invisible to the only mechanism this gate has for noticing a deleted row -- the
#  `rows actually run` floor.  A few hundred lines above, this file already says "Name each row
#  that is the SOLE detector of something, so deleting one is a red row rather than a quieter
#  file."  The SELFCHECK row is the sole detector of comparator death in five files and was
#  named nowhere.  The doctrine was written down and then not applied to the next row added.
sc_missing=""
for _f in diff_timer diff_memory_rw diff_footbridge diff_m8820x diff_m8invread; do
    grep -q 'SELFCHECK the comparator can still fail' "$LOGDIR/$_f.log" 2>/dev/null \
        || sc_missing="$sc_missing $_f"
done
check "SELFCHECK: every one of the five detectors ran its comparator sentinel" \
      "${sc_missing:-none}" "none"

selfmutant_one diff_timer.c      src/core/timer.c            timer      "NaN"
selfmutant_one diff_memory_rw.c  src/cpus/memory_rw.c        memory_rw  "1 KB"
selfmutant_one diff_footbridge.c src/devices/dev_footbridge.c footbridge "zero"
selfmutant_one diff_m8820x.c     src/devices/dev_m8820x.c    m8820x     "D3"
selfmutant_one diff_m8invread.c  src/devices/dev_m8820x.c    m8invread  "F1 "

#  THE MANIFEST -- the part that stops this being a five-instance fix.
#
#  Without it, differential #12 arrives with no control and nobody notices, which
#  is EXACTLY how R4-R9 added five differentials without once touching gate 3.
#  Same idiom as run.sh's GATE_MANIFEST: adding a differential means adding a
#  control or naming it on the exemption list, deliberately.  That is the point.
#
#  The exemptions are DATED and NAMED rather than silent.  They are real debt:
#  each is a differential whose rows could all be inert with this gate green.
#  Filed as `selfmutant6` -- doing them silently in this round would break the
#  stopping rule, and leaving them unnamed after writing the helper would repeat
#  the "grep for its siblings" miss this project keeps making.
SM_COVERED="timer memory_rw footbridge m8820x m8invread"
SM_EXEMPT="ieee_store:2099-01-01 sh4_tmu:2026-10-01 wdc_identify:2026-10-01 diskimage_io:2026-10-01 diskimage_geom:2026-11-01 diskimage_parse:2026-11-01"
sm_missing=""
for f in "$HERE"/diff_*.c; do
    stem=$(basename "$f" .c); stem=${stem#diff_}
    #  Match the STEM, not the whole token: exemptions now carry ":date" suffixes, and a
    #  substring match against the raw string would silently accept a stem that is merely a
    #  prefix of another one.
    _found=no
    for _c in $SM_COVERED; do [ "$_c" = "$stem" ] && _found=yes; done
    for _e in $SM_EXEMPT; do [ "${_e%%:*}" = "$stem" ] && _found=yes; done
    [ "$_found" = yes ] || sm_missing="$sm_missing $stem"
done
check "selfmutant manifest: every differential is covered or dated-exempt" \
      "${sm_missing:-none}" "none"
#  *** F3: THE MANIFEST VERIFIED THE LEDGER, NOT THE WORK. ***  SM_COVERED is a hand-written
#  string and nothing cross-checked it against the selfmutant_one calls, so a pass-2 seat
#  measured BOTH directions green: delete a selfmutant_one call and leave SM_COVERED intact ->
#  GREEN; move a stem from EXEMPT to COVERED, retune the count, write no mutant -> GREEN, with
#  the gate then PRINTING the paper shrink as evidence.
#
#  Same G-vs-H distinction this project already wrote into precommit_check.sh: the manifest was
#  a G with no H.  It verified that a name appeared in a list, never that work stood behind it.
sm_unbacked=""
for _stem in $SM_COVERED; do
    grep -qE "^selfmutant_one +[^ ]+ +[^ ]+ +$_stem +" "$HERE/gate_offline.sh" \
        || sm_unbacked="$sm_unbacked $_stem"
done
check "selfmutant manifest: every COVERED stem has a real selfmutant_one call" \
      "${sm_unbacked:-none}" "none"
#  ieee_store carries a far-future date because GATE 3 covers it -- against TOTAL comparator
#  death only, and by the vacuity-prone `grep -c PASS == 0` form this helper was written to
#  avoid, so it is a weaker exemption than it looks.  The other five are uncovered debt with
#  real deadlines.
#
#  DATED ENTRIES, NOT A COUNT.  The first version asserted `wc -w == 6` under a row named
#  "6, shrinking not growing" -- and a seat measured that SHRINKING IT IS RED (got=5 want=6),
#  so the pin actively obstructed the thing its own name claimed to want, and the name embedded
#  the constant so a legitimate shrink would print "the exemption list is 6 ...   5".  A count
#  pins; a date expires.  Shrinking is now green by construction: there is nothing to retune.
sm_expired=""
_today=$(date +%Y-%m-%d)
for _e in $SM_EXEMPT; do
    case "${_e##*:}" in
        "") ;;
        *) [ "${_e##*:}" \< "$_today" ] && sm_expired="$sm_expired ${_e%%:*}" ;;
    esac
done
check "selfmutant manifest: no exemption is past its dated deadline" \
      "${sm_expired:-none}" "none"

TMUBIN=$LOGDIR/diff_sh4_tmu
TMULOG=$LOGDIR/diff_sh4_tmu.log
if ! $CC -O2 -std=c99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$TMUBIN" "$HERE/diff_sh4_tmu.c" > "$TMULOG" 2>&1; then
    note "SH-4 TMU differential compile failed:"; sed 's/^/       /' "$TMULOG" | head -12
    check "SH-4 TMU: compiles against the real dev_sh4.c" "no" "yes"
else
    check "SH-4 TMU: compiles against the real dev_sh4.c" "yes" "yes"
    "$TMUBIN" > "$TMULOG" 2>&1
    sed 's/^/       /' "$TMULOG"
    #  Assert the verdict AND the row count. The verdict alone would stay green if the
    #  table were emptied; a floor on the rows is what stops that.
    check     "SH-4 TMU: row failures" \
              "$(grep -oE '[0-9]+ failures' "$TMULOG" | grep -oE '^[0-9]+')" "0"
    check_min "SH-4 TMU: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$TMULOG" | grep -oE '^[0-9]+')" 16
    check     "SH-4 TMU: offline verdict" "$(grep -c 'SH4_TMU_PASS' "$TMULOG")" "1"
    #  #401: the multi-period rows are named because they are the ONLY rows that
    #  make the modulo mean anything. Four seats independently found that dropping
    #  `% period` passed all of #400's eleven rows -- none ever reached
    #  remaining >= period, so the correction itself went untested. Deleting these
    #  must be visible rather than silent.
    check     "SH-4 TMU: the multi-period rows are present" \
              "$(grep -c 'multi-period wrap' "$TMULOG")" "2"
    #  Named rows, so that deleting one is visible rather than silent.
    check     "SH-4 TMU: the freeze row is present" \
              "$(grep -c 'no freeze past 515.4 s' "$TMULOG")" "1"
    check     "SH-4 TMU: the three-timer row is present" \
              "$(grep -c 'three timers at once' "$TMULOG")" "1"
    #  #403: a seat found FOURTEEN wrong implementations that passed the earlier
    #  table, because gcov showed timer_interrupts_pending[i]++ was NEVER
    #  EXECUTED -- no row set TCR_UNIE. These three rows are what made deleting
    #  the increment, wiping TCR with `=`, ignoring TSTR, and a signed compare
    #  visible. Name them so removing one is loud.
    check     "SH-4 TMU: the interrupt row is present" \
              "$(grep -c 'underflow raises one interrupt' "$TMULOG")" "1"
    check     "SH-4 TMU: the stopped-timer row is present" \
              "$(grep -c 'stopped timer' "$TMULOG")" "1"
    check     "SH-4 TMU: the reset-default row is present" \
              "$(grep -c 'reset default must not underflow' "$TMULOG")" "1"
fi

# ---- #405: the ATA IDENTIFY capacity bytes --------------------------------------
# Third instance of the same construction (float_emul, dev_sh4, now dev_wdc): the driver
# stubs the diskimage_* externals and #includes dev_wdc.c, so the function that runs is
# the one that ships. wdc_initialize_identify_struct() is static, so there is no way to
# link it without including the file.
#
# *** WHY THE NAMED ROWS BELOW ARE THE WHOLE POINT. `% 255` and `& 255` return the SAME
# byte for every operand below 255, so a table of plausible-looking disk sizes passes on
# the UNFIXED code -- every disk under 33,423,360 bytes agrees. Each named row puts a
# specific byte at or past the divergence point. Measured against the shipped defect:
# the full revert fails 7 rows, and a PARTIAL fix that corrects only the two `>> 8`
# lines still fails 4 -- which is the case a less careful table would have let through.
# ***
WDCBIN=$LOGDIR/diff_wdc_identify
WDCLOG=$LOGDIR/diff_wdc_identify.log
if ! $CC -O2 -std=c99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$WDCBIN" "$HERE/diff_wdc_identify.c" > "$WDCLOG" 2>&1; then
    note "wdc IDENTIFY differential compile failed:"; sed 's/^/       /' "$WDCLOG" | head -12
    check "wdc IDENTIFY: compiles against the real dev_wdc.c" "no" "yes"
else
    check "wdc IDENTIFY: compiles against the real dev_wdc.c" "yes" "yes"
    "$WDCBIN" > "$WDCLOG" 2>&1
    sed 's/^/       /' "$WDCLOG"
    check     "wdc IDENTIFY: row failures" \
              "$(grep -oE '[0-9]+ failures' "$WDCLOG" | grep -oE '^[0-9]+')" "0"
    check_min "wdc IDENTIFY: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$WDCLOG" | grep -oE '^[0-9]+')" 16
    check     "wdc IDENTIFY: offline verdict" \
              "$(grep -c 'WDC_IDENTIFY_PASS' "$WDCLOG")" "1"
    #  The four divergence rows. Deleting any one of them returns the table to the
    #  vacuous state described above, so each is named rather than merely counted.
    check     "wdc IDENTIFY: the >>8 threshold row is present" \
              "$(grep -c 'threshold: >>8 byte reaches 255' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the carry row is present" \
              "$(grep -c 'carry: >>8 wraps into >>16' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the >>16 row is present" \
              "$(grep -c '>>8 accidentally right, >>16 wrong' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the >>24 threshold row is present" \
              "$(grep -c 'threshold: >>24 byte reaches 255' "$WDCLOG")" "1"
    #  The spec-free oracle. There is no ATA document in this tree, so the absolute
    #  encoding cannot be cited -- but diskimage_recalc_size() rounds every image up to
    #  a whole cylinder, so the block must agree with its OWN geometry words. That
    #  needs no specification at all, and it is what makes the fix defensible here.
    check     "wdc IDENTIFY: the self-consistency oracle is present" \
              "$(grep -c 'IDENTIFY agrees with itself' "$WDCLOG")" "1"
    #  Word 53 is 0x0002 -- asymmetric, so a +0/+1 packing swap is visible. Word 47 is
    #  0x8080, a byte-swap palindrome, and would have been useless here.
    check     "wdc IDENTIFY: the packing anchor is present" \
              "$(grep -c 'packing anchor' "$WDCLOG")" "1"
    #  #407: three rows added after a measure seat found three mutants that passed
    #  the original ten. Each is named because each is the ONLY row that kills its
    #  mutant -- verified by asserting the row NAME in the kill, not just that
    #  something failed.
    #    slave      <- 10 chars: drop `d->drive + ` at dev_wdc.c:179
    #    word 49    <- 1 char:   advertise LBA that is #if 0'd out
    #    65535 loop <- 11-bit cylinder truncation, first contradiction at c=2048,
    #                  which the old c<=2000 bound missed by FORTY-EIGHT
    check     "wdc IDENTIFY: the slave-drive row is present" \
              "$(grep -c 'the SLAVE reports its own capacity' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the word-49 capability row is present" \
              "$(grep -c 'no unimplemented capability claimed' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the oracle sweeps the full 16-bit range" \
              "$(grep -c 'of 65535 contradict their geometry' "$WDCLOG")" "1"
    #  #408: two more named rows, each closing a mutant class that survived the
    #  twelve. The slave row previously asserted only CAPACITY, so four mutants
    #  reading drive 0's cylinders/heads/spt went unnoticed; and base_drive -- which
    #  dev_wdc_init sets to 2 for the SECONDARY controller, so it is live, not
    #  hypothetical -- was ungated at all three call sites.
    check     "wdc IDENTIFY: the slave row covers geometry, not just capacity" \
              "$(grep -c 'the SLAVE reports its own' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the base_drive row is present" \
              "$(grep -c 'base_drive reaches the diskimage id' "$WDCLOG")" "1"
    #  #409: two further rows, each closing mutants that survived the thirteen.
    #    identity  <- is_a_cdrom and getname still IGNORED `id`, so four mutants
    #                 lived. The stub now poisons BY INVERSION: every id except
    #                 this drive's is a CD-ROM. Pinning ONE specific id does not
    #                 work -- a wrong id simply misses it and still reads "not a
    #                 CD-ROM", which is how the first attempt at this row failed.
    #    wide      <- no fixture pushed heads or spt past 255, so the `>> 8` half
    #                 of words 3 and 6 was never non-zero and could be replaced by
    #                 a literal 0 undetected.
    #  #410: grep a string the row prints WHETHER IT PASSES OR FAILS. The #409
    #  version matched 'the right id', which appears only in the ok line -- so a
    #  genuinely FAILING row also reported "not present", turning one red row into
    #  two and making a failure indistinguishable from a deletion. That is the
    #  phantom-regression shape this harness's own vacuity taxonomy warns about.
    check     "wdc IDENTIFY: the identity row is present" \
              "$(grep -c 'the right id\|not the CD-ROM next to it' "$WDCLOG")" "1"
    #  #410: the ATAPI branch was DELETABLE with every row green -- #409's
    #  inverted poison made the drive under test the only non-CD-ROM, so the row
    #  could observe nothing but the negative answer. This row takes the other
    #  branch and asserts word 0 == 0x8580.
    check     "wdc IDENTIFY: the ATAPI-flags row is present" \
              "$(grep -c 'announces itself as one' "$WDCLOG")" "1"
    check     "wdc IDENTIFY: the wide-geometry row is present" \
              "$(grep -c 'high byte' "$WDCLOG")" "1"
fi

# ---- #406: the autodev.c generator ----------------------------------------------
# A prose mention of "DEVINIT" in a comment used to reach the generated C. It cost
# 358 compiler errors, no binary, gate 1 red and eleven gates skipped -- from one
# comment line, which is still in the tree DELIBERATELY (rewording it would have
# made the hardening deletable in silence).
#
# The driver runs the REAL generator in a scratch copy, so it cannot drift from
# what ships, and it carries its own mutant lane. The load-bearing row is the
# ORDERED NAME LIST, not a character check: measured, the half-fix that keeps
# noglob but drops the anchor emits 27 extra names of which 26 are DOTLESS --
# valid C identifiers that a "no bad characters" row waves straight through, and
# that fail at link time instead of parse time.
AGLOG=$LOGDIR/diff_autodev_gen.log
if [ ! -x "$HERE/diff_autodev_gen.sh" ]; then
    check "autodev generator: driver is executable" "no" "yes"
else
    "$HERE/diff_autodev_gen.sh" > "$AGLOG" 2>&1
    sed 's/^/       /' "$AGLOG"
    check     "autodev generator: row failures" \
              "$(grep -oE '[0-9]+ failures' "$AGLOG" | grep -oE '^[0-9]+')" "0"
    check_min "autodev generator: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$AGLOG" | grep -oE '^[0-9]+')" 8
    check     "autodev generator: offline verdict" \
              "$(grep -c 'AUTODEV_GEN_PASS' "$AGLOG")" "1"
    #  Named rows. The two mutants are what make the ordered-list assertion
    #  load-bearing rather than decorative, so deleting either must be loud.
    check     "autodev generator: the ordered devinit list is asserted" \
              "$(grep -c 'devinit names == the .DEVINIT( declarations, in order' "$AGLOG")" "1"
    check     "autodev generator: the full-revert mutant is present" \
              "$(grep -c 'MUTANT killed: full revert' "$AGLOG")" "1"
    check     "autodev generator: the HALF-FIX mutant is present" \
              "$(grep -c 'MUTANT killed: noglob only' "$AGLOG")" "1"
    #  If somebody rewords dev_rs5c313.c:144 the mutant lane stops proving
    #  anything, so the driver asserts that live input still exists and this row
    #  makes that assertion visible at gate level too.
    check     "autodev generator: a live off-anchor mention still exists" \
              "$(grep -c 'a live off-anchor DEVINIT mention still exists' "$AGLOG")" "1"
    #  No mutant may SURVIVE. Named separately from the failure count because a
    #  survivor is a statement about the DETECTOR, not about the generator.
    check     "autodev generator: no mutant survives" \
              "$(grep -c 'SURVIVES' "$AGLOG")" "0"
fi

# ---- #412: SCSI READ CAPACITY on a zero-block disk -------------------------------
# `size` is uint64_t and nr_of_logical_blocks is int64_t, so 0 - 1 underflowed and the
# guest was told the disk holds 4,294,967,296 blocks -- 2 TiB -- rather than that it is
# empty. Measured both directions before and after: 0xffffffff -> 0x00000000.
#
# THIS IS NOT A CORNER CASE TODAY. A separate live defect leaves every `-d gH;S` disk with
# zero blocks, and such a disk KEEPS its SCSI/IDE type, so it reaches the handler and is told
# it holds 2 TiB. Measured: a 10 MB image announced as "SCSI DISK id 0, 0 MB (CHS=0,16,63)".
# (#413 narrowed this from "every floppy": DISKIMAGE_FLOPPY is a WRITE-ONLY type -- no device
# ever passes it, so a floppy-typed disk never reaches this handler at all. That is a separate
# filed defect. The row below is unaffected; a 0-byte image IS a reachable zero-block disk.) The "0 KB" on the console is the host-side banner only; the guest is told two
# terabytes. This guard keeps an empty disk reporting empty however it got that way, and
# stays correct after that defect is fixed -- which is why its row uses a 0-BYTE IMAGE
# rather than a floppy. A floppy row would go vacuous the moment the geometry fix lands.
#
# The driver carries four further sections, DISABLED, that assert defects still live
# (short/failed writes reported as success, reads past EOF, and a single WRITE(10) that
# grew a 10 KB image to 512 MB with status GOOD). Build with -DDISKIMAGE_IO_UNFIXED to
# see them fail; the round that fixes them deletes the guard.
IOLOG=$LOGDIR/diff_diskimage_io.log
if ! $CC -O2 -std=gnu99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$LOGDIR/diff_diskimage_io" "$HERE/diff_diskimage_io.c" > "$IOLOG" 2>&1; then
    note "diskimage I/O differential compile failed:"; sed 's/^/       /' "$IOLOG" | head -12
    check "diskimage I/O: compiles against the real diskimage.c" "no" "yes"
else
    check "diskimage I/O: compiles against the real diskimage.c" "yes" "yes"
    "$LOGDIR/diff_diskimage_io" > "$IOLOG" 2>&1
    sed 's/^/       /' "$IOLOG"
    check     "diskimage I/O: row failures" \
              "$(grep -oE '[0-9]+ failures' "$IOLOG" | grep -oE '^[0-9]+')" "0"
    check     "diskimage I/O: faults" \
              "$(grep -oE '[0-9]+ faults' "$IOLOG" | grep -oE '^[0-9]+')" "0"
    #  #416: was `>= 3`, written when only three rows ran by default.  The
    #  guard that hid the other four sections is now gone, so 3 would permit
    #  28 rows to be deleted silently -- a minimum the current value exceeds
    #  tenfold is decoration, not evidence.
    check_min "diskimage I/O: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$IOLOG" | grep -oE '^[0-9]+')" 45
    #  Named so that deleting the zero-block row is visible rather than silent.
    check     "diskimage I/O: the zero-block capacity row is present" \
              "$(grep -c 'zero-block disk does not announce' "$IOLOG")" "1"
    #  #416: the four sections that used to sit behind -DDISKIMAGE_IO_UNFIXED
    #  now run unconditionally.  Named individually so that re-hiding any of
    #  them is visible; the grep text appears whether the row passes or fails,
    #  so a FAILING row cannot read as a MISSING one.
    check     "diskimage I/O: the past-capacity WRITE rows run by default" \
              "$(grep -c 'WRITE(10) past capacity' "$IOLOG")" "3"
    check     "diskimage I/O: the refused-read zero-fill is ASSERTED" \
              "$(grep -c 'refused read leaves NO caller bytes' "$IOLOG")" "1"
    #  SECTION G is the boundary.  Without it three separate mutants survive:
    #  an off-by-one bound, a start-only bound, and a write bounded by
    #  ADVERTISED capacity rather than the backed extent.
    check     "diskimage I/O: the gap-write row is present" \
              "$(grep -c 'WRITE into the advertised gap is refused' "$IOLOG")" "1"
    check     "diskimage I/O: the run-off-the-end row is present" \
              "$(grep -c 'running off the end' "$IOLOG")" "1"
    check     "diskimage I/O: the gap READ still succeeds (the rig images)" \
              "$(grep -c 'READ inside the advertised gap still succeeds' "$IOLOG")" "1"
fi

# ----------------------------------------------------------------------------
# #414: disk GEOMETRY differential -- diskimage_recalc_size() and the -d gH;S
# parser, linked against the real diskimage.c.
#
# It needs a WRITABLE DIRECTORY because recalc_size() calls stat(): every row
# creates a real file of an exact size rather than faking the size field, so
# what is measured is the shipped code path and not a stub of it.  GEOMDIR is
# how the driver is told where to put them.
#
# The row count is asserted, not merely reported.  Two files named
# diff_diskimage_geom.c existed during development in paths differing only by
# the case of a parent directory, and the smaller one encoded a design decision
# that had since been reversed; a run that silently used the wrong one looked
# exactly like a run that used the right one.
GEOMLOG=$LOGDIR/diff_diskimage_geom.log
if ! $CC -O2 -std=gnu99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$LOGDIR/diff_diskimage_geom" "$HERE/diff_diskimage_geom.c" \
        "$SEC/src/disk/diskimage.c" > "$GEOMLOG" 2>&1; then
    note "disk geometry differential compile failed:"; sed 's/^/       /' "$GEOMLOG" | head -12
    check "disk geometry: compiles against the real diskimage.c" "no" "yes"
else
    check "disk geometry: compiles against the real diskimage.c" "yes" "yes"
    GEOMDIR="$LOGDIR" "$LOGDIR/diff_diskimage_geom" > "$GEOMLOG" 2>&1
    sed 's/^/       /' "$GEOMLOG"
    check     "disk geometry: row failures" \
              "$(grep -oE '[0-9]+ failures' "$GEOMLOG" | grep -oE '^[0-9]+')" "0"
    check     "disk geometry: verdict token" \
              "$(grep -c 'DISKIMAGE_GEOM_PASS' "$GEOMLOG")" "1"
    check_min "disk geometry: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$GEOMLOG" | grep -oE '^[0-9]+')" 34
    #  Named individually so that DELETING one is visible rather than silent.
    #  Every one of these closed a mutant that survived all the other rows;
    #  the grep text is chosen to appear whether the row PASSES OR FAILS, so a
    #  failing row cannot read as a missing row.
    check     "disk geometry: the autodetect rows use type UNKNOWN" \
              "$(grep -c 'autodetect 720 KB\|autodetect 1.2 MB\|autodetect 2.88 MB' "$GEOMLOG")" "3"
    check     "disk geometry: the zero-byte row guarding #412 is present" \
              "$(grep -c '0-byte image stays empty' "$GEOMLOG")" "1"
    check     "disk geometry: the fg prefix row is present" \
              "$(grep -c 'fg2;9 is honoured through the parser' "$GEOMLOG")" "1"
    check     "disk geometry: the SPT-position wrap row is present" \
              "$(grep -c 'wrap in the SPT position' "$GEOMLOG")" "1"
    #  These four cover regions no earlier row entered at all.  The s:/i:
    #  pair is the important one: without it the shared cylinder block is
    #  never reached at the type every primary rig actually uses, and a
    #  one-condition mutant reinstates the whole defect for those disks.
    check     "disk geometry: the non-multiple floppy size row is present" \
              "$(grep -c 'NOT a multiple of 81920' "$GEOMLOG")" "1"
    check     "disk geometry: the shared block is reached as SCSI and IDE" \
              "$(grep -c 'reaches the shared cylinder block' "$GEOMLOG")" "2"
    check     "disk geometry: the unsigned-fold row is present" \
              "$(grep -c 'must not fold to 1 in the SPT position' "$GEOMLOG")" "1"
fi

# ---------------------------------------------------------------------------
# #418: the `-d` PREFIX PARSER differential.  Offline, no binary, no guest.
#
# `d:` is documented as the escape hatch out of the size heuristic, but nothing
# acted on it, so a floppy-sized image stayed DISKIMAGE_FLOPPY -- a type NO
# controller ever passes -- and the guest got no disk at all.
#
# WHY THE [SIZE] ROWS BELOW ARE NAMED INDIVIDUALLY.  Measured, six variants
# built and run: a placement in the prefix block ALSO makes `d:` work and is
# killed by NOTHING ELSE IN THE FILE -- only the four exactness rows fail it,
# because that placement runs before diskimage_recalc_size() and rounds the
# advertised capacity up (720K 1440 -> 2016 blocks, +40%).  Delete those four
# rows and the wrong placement ships green.
PARSELOG=$LOGDIR/diff_diskimage_parse.log
if ! $CC -O2 -std=gnu99 -I"$SEC/src/include" -I"$SEC/src/include/thirdparty" \
        -ffunction-sections -fdata-sections -Wl,--gc-sections \
        -o "$LOGDIR/diff_diskimage_parse" "$HERE/diff_diskimage_parse.c" > "$PARSELOG" 2>&1; then
    note "disk parser differential compile failed:"; sed 's/^/       /' "$PARSELOG" | head -12
    check "disk parser: compiles against the real diskimage.c" "no" "yes"
else
    check "disk parser: compiles against the real diskimage.c" "yes" "yes"
    "$LOGDIR/diff_diskimage_parse" > "$PARSELOG" 2>&1
    sed 's/^/       /' "$PARSELOG"
    check     "disk parser: row failures" \
              "$(grep -oE '[0-9]+ failures' "$PARSELOG" | grep -oE '^[0-9]+')" "0"
    #  37 = the 36 the identity row asserts, plus the identity row itself.
    check_min "disk parser: rows actually run" \
              "$(grep -oE '^[0-9]+ rows' "$PARSELOG" | grep -oE '^[0-9]+')" 37
    check     "disk parser: the identity row is present" \
              "$(grep -c 'row count -- guards against a stale copy' "$PARSELOG")" "1"
    #  The grep text appears whether a row PASSES OR FAILS, so a failing row
    #  cannot read as a missing row.  Each of these closed a mutant that
    #  survived every other row in the file.
    check     "disk parser: all four exactness rows are present" \
              "$(grep -c 'advertised blocks exact' "$PARSELOG")" "4"
    check     "disk parser: the IDE-default rows are present" \
              "$(grep -c 'on IDE-default -> IDE\|exists as IDE (dev_wdc)\|NOT visible as SCSI' "$PARSELOG")" "3"
    #  The 'sd:' row is the SEVENTH mutant's ONLY kill: deleting `&& !prefix_s`
    #  survives every other row in the file, because `sd:` on a SCSI-default
    #  machine changes SCSI to SCSI.  It has to run on an IDE-default machine,
    #  and it has to be named here or deleting it is silent.
    check     "disk parser: the explicit-prefix precedence rows are present" \
              "$(grep -c "'fd:' stays FLOPPY\|'id:' stays IDE\|'sd:' stays SCSI" "$PARSELOG")" "3"
    check     "disk parser: the d:*.iso rows are present" \
              "$(grep -c 'd:\*.iso is not a CD-ROM\|d:\*.iso is writable' "$PARSELOG")" "2"
    #  Records, not endorsements: both pin defects this round did NOT fix, so
    #  the round that does fix them cannot land silently.
    check     "disk parser: the bare-floppy unreachability records are present" \
              "$(grep -c 'unreachable by dev_asc' "$PARSELOG")" "4"
    check     "disk parser: the FLOPPY-typed-ISO record is present" \
              "$(grep -c 'is FLOPPY-typed (filed defect)' "$PARSELOG")" "1"
fi

gate_end
exit $?
