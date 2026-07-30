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
check     "D-format: change-set is empty"          "$(val 'D-format diffs')"    "0"
check_min "S-format: overflow class is non-empty"  "$(val '  of which overflow')" 1
check_min "S-format: underflow class is non-empty" "$(val '  of which negative')" 1
check_min "samples swept"                          "$(val 'samples')"       20000000
check     "clamp threshold is 2^129, not 2^128"    "$(val 'clamp-at')"          "2^129"
check     "exponent-255 threshold is 2^128"        "$(val 'exp255-at')"         "2^128"
check     "first shipped-vs-upstream diff at 2^128" "$(val 'first-difference-at')" "2^128"

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

gate_end
exit $?
