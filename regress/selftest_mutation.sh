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

# FOUR mutants now, one per guarded property. Each breaks the code a different way and
# the differential must go red for every one of them.
#
#   A  revert #287      overflow keeps its garbage fraction (a NaN encoding) and
#                       underflow loses its sign -- in the #292 structure that is
#                       "to_inf never fires" plus "flush drops the sign bit"
#   B  ties-away        #292's nearest mode rounds every exact tie up instead of to
#                       even. A random sweep cannot catch this (an exact tie occurs
#                       about once per 2^29 inputs); only the named vectors do.
#   C  mode ignored     #292's rm parameter is accepted and discarded. Every
#                       differential ever written passes an ignored parameter; the
#                       mode-is-read vector pair is what catches it.
#   D  W rounds under LEGACY   #294's integer arm rounding when it should truncate
#                       would silently change every pre-existing trunc-style caller;
#                       the legacy W vectors are what catch it.
mutate() {   # name -> writes $T/mutant_<name>.c, echoes ok/FAIL
    local name=$1
    cp "$TREE/src/core/float_emul.c" "$T/mutant_$name.c"
    python3 - "$T/mutant_$name.c" "$name" <<'PY'
import io, sys
p, name = sys.argv[1], sys.argv[2]
s = io.open(p, encoding="utf-8", errors="surrogateescape").read()
def need(frag):
    if frag not in s:
        print("SETUP_FAIL: expected fragment not found for mutant %s" % name)
        sys.exit(1)

if name == "revert287":
    a = "\t\t\t\tif (to_inf)\n\t\t\t\t\tr &= (uint64_t)1 << signofs;"
    b = "\t\t\tif (exponent == 0)\n\t\t\t\tr &= (uint64_t)1 << signofs;"
    need(a); need(b)
    s = s.replace(a, "\t\t\t\tif (0)\n\t\t\t\t\tr &= (uint64_t)1 << signofs;", 1)
    s = s.replace(b, "\t\t\tif (exponent == 0)\n\t\t\t\tr = 0;", 1)
elif name == "tiesaway":
    a = "round_up = nf > 0.5 ||\n\t\t\t\t\t    (nf == 0.5 && (r & 1));"
    need(a)
    s = s.replace(a, "round_up = nf >= 0.5;", 1)
elif name == "modeignored":
    a = "uint64_t ieee_store_float_value_rm(double nf, int fmt, int rm)\n{"
    need(a)
    s = s.replace(a, a + "\n\trm = IEEE_RM_LEGACY;", 1)
elif name == "wlegacyrounds":
    # #294's W/L arm suddenly rounding under LEGACY would change every
    # pre-existing trunc-style caller. The legacy W vectors must catch it.
    #
    # The FIRST version of this mutant only dropped LEGACY from the outer
    # guard -- and the differential rightly stayed green, because LEGACY
    # matches no case in the inner rounding switch and fell through
    # unchanged. A mutant that cannot fail tests nothing (the self-test's
    # own check caught that). This version forces LEGACY to round nearest,
    # which the "W: LEGACY == old truncation" vector must detect.
    a = ("\t\tif (!isnan(nf) &&\n"
         "\t\t    rm != IEEE_RM_LEGACY && rm != IEEE_RM_RZ) {\n"
         "\t\t\tdouble fl = floor(nf);")
    need(a)
    s = s.replace(a,
         "\t\tif (!isnan(nf) &&\n"
         "\t\t    rm != IEEE_RM_RZ) {\n"
         "\t\t\tif (rm == IEEE_RM_LEGACY)\n"
         "\t\t\t\trm = IEEE_RM_RN;\n"
         "\t\t\tdouble fl = floor(nf);", 1)
io.open(p, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)
PY
    [ $? -eq 0 ] && echo ok || echo FAIL
}

build_and_run() {   # label, source file -> prints DIFF_PASS count
    $CC -O2 -I"$TREE/src/include" -o "$T/$1" \
        "$HERE/diff_ieee_store.c" "$2" -lm > "$T/$1.build" 2>&1 || { echo "BUILDFAIL"; return; }
    "$T/$1" > "$T/$1.out" 2>&1
    grep -c 'DIFF_PASS' "$T/$1.out"
}

for m in revert287 tiesaway modeignored wlegacyrounds; do
    check "mutant $m could be applied" "$(mutate $m)" "ok"
done

note "control: differential against the shipped float_emul.c"
real=$(build_and_run real "$TREE/src/core/float_emul.c")
check "unmutated source passes gate 2" "$real" "1"

for m in revert287 tiesaway modeignored wlegacyrounds; do
    note "mutant $m: the differential must go red"
    out=$(build_and_run "mut_$m" "$T/mutant_$m.c")
    check "mutant $m is DETECTED (must fail)" "$out" "0"
done

gate_end
exit $?
