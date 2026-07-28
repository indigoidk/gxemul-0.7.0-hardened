#!/bin/bash
# SELF-TEST -- does gate 2 actually fail when the code it guards is broken?
#
# This exists because the honest answer, the first time it was asked, was NO. The original
# gate 2 transcribed both sides of its differential into its own C file and compared the
# copy against itself; it never compiled or linked src/core/float_emul.c, so deleting #287
# from the shipped source left all eight checks green. Review caught that, not the gate.
#
# A gate that cannot fail is worse than no gate, because it reports green. The only way to
# know which kind you have is to break the subject on purpose and require red. This
# mutates float_emul.c back to upstream behaviour, runs the differential against the
# mutant, and requires DIFF_FAIL -- while the unmutated build must still give DIFF_PASS.
# Nothing in the repository is modified: the mutation is applied to a copy in /tmp.
#
# Run it after any change to gate 2 or to float_emul.c's S/D arm.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

SEC=$ROOT/GXEMUL-SEC
T=$LOGDIR/mutation

gate_begin "selftest-can-gate-2-fail"

command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1 || gate_skip "no C compiler"
CC=$(command -v cc || command -v gcc)
command -v python3 >/dev/null 2>&1 || gate_skip "python3 not on PATH"

TREE=""
for t in "$ROOT/build" /tmp/gxsec-build; do
    [ -f "$t/config.h" ] && [ -f "$t/src/include/float_emul.h" ] && { TREE=$t; break; }
done
[ -n "$TREE" ] || gate_skip "no configured tree (run gate_build.sh first)"

rm -rf "$T"; mkdir -p "$T"
cp "$TREE/src/core/float_emul.c" "$T/mutant.c"

# Revert #287 in the COPY: drop the overflow guard, restore the upstream underflow line.
python3 - "$T/mutant.c" <<'PY'
import io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8", errors="surrogateescape").read()
a = "\t\t\tif (exponent == ((int64_t)1 << n_exp) - 1)\n\t\t\t\tr &= (uint64_t)1 << signofs;\n"
b = "\t\t\tif (exponent == 0)\n\t\t\t\tr &= (uint64_t)1 << signofs;\n"
if a not in s or b not in s:
    print("SETUP_FAIL: the #287 guards were not found -- has the arm been rewritten?")
    sys.exit(1)
s = s.replace(a, "", 1).replace(b, "\t\t\tif (exponent == 0)\n\t\t\t\tr = 0;\n", 1)
io.open(p, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)
PY
if [ $? -ne 0 ]; then
    check "mutation could be applied" "no" "yes"
    gate_end; exit $?
fi
check "mutation could be applied" "yes" "yes"

build_and_run() {   # label, source file -> prints DIFF_PASS count
    $CC -O2 -I"$TREE/src/include" -o "$T/$1" \
        "$HERE/diff_ieee_store.c" "$2" -lm > "$T/$1.build" 2>&1 || { echo "BUILDFAIL"; return; }
    "$T/$1" > "$T/$1.out" 2>&1
    grep -c 'DIFF_PASS' "$T/$1.out"
}

note "control: differential against the shipped float_emul.c"
real=$(build_and_run real "$TREE/src/core/float_emul.c")
note "mutant: differential against float_emul.c with #287 reverted"
mut=$(build_and_run mut "$T/mutant.c")

grep -E '^(absolute-answer failures|S-format differences|first-difference-at)' \
    "$T/mut.out" 2>/dev/null | sed 's/^/       mutant: /'

check "unmutated source passes gate 2"        "$real" "1"
check "reverted #287 is DETECTED (must fail)" "$mut"  "0"

gate_end
exit $?
