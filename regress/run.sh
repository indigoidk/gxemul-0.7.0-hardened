#!/bin/bash
# Run the regression gates. `./run.sh` runs all of them; `./run.sh 2 4` runs a subset.
#
# Order matters: the build gate produces the binaries the rest test, and the hygiene gate
# reads the logs the MIPS gate produces.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

GATES=(gate_build gate_offline selftest_mutation gate_mips gate_crossfamily gate_hygiene gate_ab gate_upstream gate_asan_sweep gate_sh_rounding gate_m88k_rounding gate_mips_rounding gate_ppc gate_arm gate_ppc_halt gate_mips_folds)

#  How many gates this battery is supposed to have.  Every round ends with a claim of
#  the form "the battery is green", and until now NOTHING checked how many gates that
#  covered -- so a gate silently dropped from the array above would have looked exactly
#  like a battery that was always this size.  The count was also wrong in three places
#  at once: this README said "all six", the top-level README stopped at 13, and the
#  working notes had said both 15 and 17.  A number nobody checks is not a fact.
#
#  Adding a gate means editing BOTH lines, deliberately.  That is the point.
GATE_MANIFEST=16
if [ "${#GATES[@]}" -ne "$GATE_MANIFEST" ]; then
    echo "GATE MANIFEST MISMATCH: array has ${#GATES[@]}, manifest says $GATE_MANIFEST"
    echo "  a gate was added or removed without updating GATE_MANIFEST -- refusing to run,"
    echo "  because 'the battery is green' means nothing if the battery changed size."
    exit 2
fi

#  #399: AND EACH SCRIPT MUST AGREE WITH ITS OWN POSITION. The count above proves the
#  battery did not change SIZE; it says nothing about whether the scripts know which
#  gate they are. Four of them did not: selftest_mutation was inserted at position 3 and
#  gate_mips, gate_crossfamily, gate_hygiene and gate_ab were never renumbered, so each
#  self-labelled one low while gate_upstream onward stayed correct.
#
#  That is not cosmetic. A shipped commit message cited "gate 5" for gate_hygiene because
#  it read the number out of a comment, and the comment was wrong -- the project's rule is
#  READ THE LINE BEFORE CITING IT, and the line itself lied. A self-label with nothing
#  behind it is a fact-shaped string.
#
#  NAMED MUTANT, and it is why this compares the NUMBER rather than looking for a header:
#  a check that merely greps for the EXISTENCE of a "GATE n" line passes on all four of
#  the wrong files. A missing header is also a failure, not a pass -- selftest_mutation
#  gained one in #399 rather than being exempted, because an exemption is a hole.
_i=0
for _g in "${GATES[@]}"; do
    _i=$((_i+1))
    _lbl=$(sed -n 's/^# GATE \([0-9][0-9]*\).*/\1/p' "$HERE/$_g.sh" | head -1)
    if [ -z "$_lbl" ]; then
        echo "GATE LABEL MISSING: $_g.sh has no '# GATE n' header (expected $_i)"
        echo "  every gate must declare which gate it is, so a citation taken from its"
        echo "  own comments is checkable. Refusing to run."
        exit 2
    fi
    if [ "$_lbl" != "$_i" ]; then
        echo "GATE LABEL MISMATCH: $_g.sh calls itself GATE $_lbl but is position $_i"
        echo "  the array is the authority. A stale self-label has already put a wrong"
        echo "  gate number into a shipped record. Refusing to run."
        exit 2
    fi
done

# Validate selectors up front. Without this, `./run.sh 99` matched nothing, ran zero
# gates, and printed REGRESS_PASS -- one mistyped digit produced a green push.
for i in "$@"; do
    case "$i" in
        ''|*[!0-9]*) echo "bad gate selector '$i' (want 1..${#GATES[@]})"; exit 2 ;;
    esac
    if [ "$i" -lt 1 ] || [ "$i" -gt ${#GATES[@]} ]; then
        echo "gate selector '$i' out of range (want 1..${#GATES[@]})"; exit 2
    fi
done

want=("$@")
run_this() {
    [ ${#want[@]} -eq 0 ] && return 0
    local i
    for i in "${want[@]}"; do [ "$i" = "$1" ] && return 0; done
    return 1
}

declare -a RESULTS
n=0
for g in "${GATES[@]}"; do
    n=$((n+1))
    run_this "$n" || continue
    bash "$HERE/$g.sh"
    rc=$?
    # Only the explicit skip code counts as SKIP. bash exits 2 on a SYNTAX ERROR, so
    # mapping 2 to SKIP turned a broken gate script into a "coverage gap" and still
    # exited 0 overall.
    case $rc in
        0)            RESULTS+=("$n $g PASS") ;;
        "$EXIT_SKIP") RESULTS+=("$n $g SKIP") ;;
        *)            RESULTS+=("$n $g FAIL") ;;
    esac
    echo
done

echo "############################################################"
echo "## SUMMARY"
echo "############################################################"
pass=0; fail=0; skip=0
for r in "${RESULTS[@]}"; do
    set -- $r
    case "$3" in
        PASS) printf "  ${C_OK}%-4s${C_OFF} %s. %s\n" PASS "$1" "$2"; pass=$((pass+1)) ;;
        SKIP) printf "  ${C_SKIP}%-4s${C_OFF} %s. %s\n" SKIP "$1" "$2"; skip=$((skip+1)) ;;
        *)    printf "  ${C_BAD}%-4s${C_OFF} %s. %s\n" FAIL "$1" "$2"; fail=$((fail+1)) ;;
    esac
done
echo
echo "  passed $pass   failed $fail   skipped $skip"
#  Say what was actually covered.  A bare "passed N" invites the reader to assume N is
#  the whole battery; when a subset was selected it is not, and that distinction is
#  exactly what an auditor of a green push needs.
if [ ${#want[@]} -eq 0 ]; then
    echo "  GATE_COVERAGE=$((pass+fail+skip))/$GATE_MANIFEST (full battery)"
else
    echo "  GATE_COVERAGE=$((pass+fail+skip))/$GATE_MANIFEST (SUBSET: ${want[*]})"
fi
echo
# A skip is NEVER a pass. It means a gate could not run, which is a gap in coverage, not
# evidence of correctness -- so the overall verdict says so out loud.
if [ $((pass+fail+skip)) -eq 0 ]; then
    echo "${C_BAD}REGRESS_NOTHING_RAN${C_OFF}"; exit 1
elif [ "$fail" -gt 0 ]; then
    echo "${C_BAD}REGRESS_FAIL${C_OFF}"; exit 1
elif [ "$skip" -gt 0 ]; then
    # EXIT 3, NOT 0. Automation reads the exit status, not the colour: exiting 0 here made
    # a run where every gate skipped indistinguishable from a run where every gate passed,
    # which contradicts this harness's own rule that a skip is never a pass.
    echo "${C_SKIP}REGRESS_PASS_WITH_GAPS${C_OFF} ($skip gate(s) could not run; exit 3)"
    exit 3
else
    echo "${C_OK}REGRESS_PASS${C_OFF}"; exit 0
fi
