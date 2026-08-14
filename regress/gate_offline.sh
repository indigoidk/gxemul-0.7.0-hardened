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
              "$(grep -oE '^[0-9]+ rows' "$IOLOG" | grep -oE '^[0-9]+')" 31
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

gate_end
exit $?
