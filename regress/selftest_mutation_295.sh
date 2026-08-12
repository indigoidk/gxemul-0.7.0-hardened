#!/bin/bash
# selftest_mutation_295.sh -- prove gate 12 section 3 actually detects the #295
# revert class. NOT part of the default battery (a full emulator build per mutant,
# ~15-25 min total): run manually or at round boundaries touching this area.
#
# Why this is not an arm of selftest_mutation.sh: that harness compiles ONLY
# float_emul.c offline, and #295 is decoder WIRING in cpu_mips_coproc.c -- the
# forced IEEE_RM_* constants at the round/ceil/floor fpu_op call sites. An offline
# stub-world for cpu_mips_coproc.c would test a reimplementation, which is the
# vacuity class the self-test exists to kill. So: copy the real build tree to /tmp,
# substitute BY CONSTANT (never deletion), rebuild the real binary, and require the
# committed probe's rows to flip EXACTLY as predicted.
#
# Acceptance is a per-op flip MATRIX, not "the gate went red": for each mutant, its
# op's must-flip rows FAIL with the exact predicted directed-mode value, and every
# other row -- including the trunc/NaN/cvt/cfc1 controls, which CANNOT flip by
# construction -- stays PASS. "Every committed row must flip" was the design's
# original acceptance rule; five review seats independently rejected it as
# self-contradictory (the controls never flip; that is their purpose).
#
# Hardening (each clause traces to a review finding):
#  * the build tree's cpu_mips_coproc.c is cmp'd against the repo BEFORE copying
#    (a crashed earlier run once left a tree mutant, and the next run's own backup
#    captured the mutant);
#  * each anchor must appear EXACTLY once, and after substitution the anchor must
#    be absent and the replacement present (a drifted anchor aborts SETUP_FAIL,
#    never a silent pass);
#  * a crashing / non-completing probe run is SETUP_FAIL, never detection (the
#    sibling harness's must-fail check accepts a crashed mutant; queue item #55);
#  * pmax only: the constants sit in shared C below the rigs' convergence point
#    (cop1_slow -> coproc_function -> fpu_function), so one rig kills the mutant
#    class; the everyday gate still runs both rigs as transport breadth.
#  * only cpu_mips_coproc.o is rebuilt: the file is a standalone TU -- verified
#    `grep -rn '#include "cpu_mips_coproc.c"' src/` is empty -- so the
#    rm-all-cpus-objects rule for #included .c files does not apply here.
#
# Output: M295MUT_PASS | M295MUT_FAIL | M295MUT_SETUP_FAIL (distinguishable).
set -u
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
SEC=$ROOT/GXEMUL-SEC
BUILD=$ROOT/build
PMAX_KERNEL=$ROOT/gxemul_pmax_rig/bsd
T=/tmp/gx295mut.$$
PROBE=$SEC/regress/mips_fixedmode_probe.py

fail_setup() { echo "SETUP: $1"; echo "M295MUT_SETUP_FAIL"; rm -rf "$T"; exit 2; }

[ -x "$BUILD/gxemul" ] || fail_setup "no build tree binary at $BUILD/gxemul"
[ -f "$PMAX_KERNEL" ] || fail_setup "no pmax kernel"
cmp -s "$BUILD/src/cpus/cpu_mips_coproc.c" "$SEC/src/cpus/cpu_mips_coproc.c" \
    || fail_setup "build tree cpu_mips_coproc.c differs from the repo -- dirty baseline"

echo "copying build tree to $T"
rm -rf "$T"; mkdir -p "$T"
cp -a "$BUILD/." "$T/" || fail_setup "copy failed"

LOGS=/tmp/m295.$$                 # PID-unique: parallel runs are forbidden, but a
mkdir -p "$LOGS"                  # stale fixed-name log once confused forensics

run_probe() {  # $1 = binary, $2 = log
    python3 "$PROBE" "$1" "$PMAX_KERNEL" /dev/null pmax > "$2" 2>&1
    grep -q "M295_RESULT=" "$2" || return 1   # crash/empty is NOT detection
    return 0
}

expect() {     # $1 = log, $2 = fixed string that must appear exactly once
    n=$(grep -cF "$2" "$1")
    if [ "$n" != 1 ]; then
        echo "  MISSING: $2"
        return 1
    fi
    return 0
}

# ---- baseline: the relocated, unmutated tree must pass every row ------------
echo "baseline probe on the copied tree"
run_probe "$T/gxemul" "$LOGS/base.log" || fail_setup "baseline probe did not complete"
base_bad=0
for n in r25rp r35rm r27rm rn25rm rbnd c21rm cn225rm f29rp fn225rp \
         cvt27rm cfc1 t35rp tn35rm nan; do
    expect "$LOGS/base.log" "M295_ROW=pmax:$n RESULT=PASS" || base_bad=1
done
[ "$base_bad" = 0 ] || fail_setup "baseline (unmutated copy) does not pass -- nothing below is meaningful"

# ---- the four per-op mutants ---------------------------------------------------
# op | forced constant | its must-flip rows with the PREDICTED mutant value
# The trunc mutant is the panel's pass-2 addition: it converts the trunc control
# rows' discrimination ("they kill a trunc->FROM_FCSR revert, which no other row
# would") from an asserted claim into a measured one. Its anchor is the W-format
# trunc line -- single-line, distinguished from its L sibling by COP1_FMT_W.
MUTANTS="round:IEEE_RM_RN ceil:IEEE_RM_RP floor:IEEE_RM_RM trunc:IEEE_RM_RZ"

flip_rows() {  # rows (name=predicted-mutant-hex) for one op
    case $1 in
    round) echo "r25rp=00000003 r35rm=00000003 r27rm=00000002 rn25rm=fffffffd rbnd=7fffffff" ;;
    ceil)  echo "c21rm=00000002 cn225rm=fffffffd" ;;
    floor) echo "f29rp=00000003 fn225rp=fffffffe" ;;
    trunc) echo "t35rp=00000004 tn35rm=fffffffc" ;;
    esac
}

overall=0
for spec in $MUTANTS; do
    op=${spec%%:*}; const=${spec##*:}
    echo "---- mutant: $op ($const -> FPU_RM_FROM_FCSR) ----"

    # restore a pristine source, then substitute by constant, exactly once
    cp "$SEC/src/cpus/cpu_mips_coproc.c" "$T/src/cpus/cpu_mips_coproc.c" \
        || fail_setup "source restore failed"
    python3 - "$T/src/cpus/cpu_mips_coproc.c" "$const" "$op" <<'PY' || fail_setup "anchor drifted"
import io, sys
p, const, op = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(p, encoding="utf-8", errors="surrogateescape").read()
if op == "trunc":
    #  trunc's call sites are single-line; the W one is unique by COP1_FMT_W
    #  (its L sibling differs only there and gets no mutant -- no arc .l rows
    #  exist to read it; that is queue item #57).
    anchor = ("\t\tfpu_op(cpu, cp, FPU_OP_CVT, fmt, -1, fs, fd, -1, "
              "COP1_FMT_W, %s);" % const)
else:
    anchor = ("\t\tfpu_op(cpu, cp, FPU_OP_CVT, fmt, -1, fs, fd, -1,\n"
              "\t\t    to_w? COP1_FMT_W : COP1_FMT_L, %s);" % const)
n = s.count(anchor)
if n != 1:
    print("SETUP: anchor for %s found %d times, need exactly 1" % (const, n))
    raise SystemExit(1)
repl = anchor.replace(const, "FPU_RM_FROM_FCSR")
s2 = s.replace(anchor, repl, 1)
if anchor in s2 or repl not in s2:
    print("SETUP: post-substitution check failed")
    raise SystemExit(1)
io.open(p, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s2)
print("  substituted %s -> FPU_RM_FROM_FCSR (exactly once, verified)" % const)
PY

    ( cd "$T" && rm -f src/cpus/cpu_mips_coproc.o gxemul \
        && make -j"$(nproc)" > "$LOGS/build_$op.log" 2>&1 )
    [ -x "$T/gxemul" ] || fail_setup "mutant $op did not build (see $LOGS/build_$op.log)"

    run_probe "$T/gxemul" "$LOGS/mut_$op.log" \
        || fail_setup "mutant $op probe did not complete -- a crash is not detection"

    bad=0
    flips=$(flip_rows $op)
    for pair in $flips; do
        n=${pair%%=*}; want=${pair##*=}
        expect "$LOGS/mut_$op.log" \
            "M295_ROW=pmax:$n RESULT=FAIL got=$want" || bad=1
    done
    for n in r25rp r35rm r27rm rn25rm rbnd c21rm cn225rm f29rp fn225rp \
             cvt27rm cfc1 t35rp tn35rm nan; do
        case " $flips " in *" $n="*) continue ;; esac
        expect "$LOGS/mut_$op.log" "M295_ROW=pmax:$n RESULT=PASS" || bad=1
    done
    if [ "$bad" = 0 ]; then
        echo "  mutant $op: exact flip matrix confirmed"
    else
        echo "  mutant $op: MATRIX MISMATCH"
        overall=1
    fi
done

rm -rf "$T"
if [ "$overall" = 0 ]; then
    echo "M295MUT_PASS"
else
    echo "M295MUT_FAIL"
    exit 1
fi
