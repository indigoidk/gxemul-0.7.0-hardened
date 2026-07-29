#!/bin/bash
# GATE 9 -- every machine type constructed under AddressSanitizer, three-way.
#
# This is the BREADTH gate. Everything else in this harness executes four machines; the
# fork changed 117 source files, 27 of them specific to architectures (alpha, ARM, i960,
# PowerPC, SGI) that no rig touches at all. This gate builds every machine type, attaches
# its devices, and lets ASan watch.
#
# It revives an instrument the project already used -- the CHANGELOG records a "run every
# machine under ASan sweep (23 machine types)" that found the macppc heap OOB (#23) -- but
# as a STANDING GATE rather than a one-off, and comparatively rather than absolutely.
#
# THE ASSERTION IS DIRECTIONAL, and that matters. The fork exists partly to FIX memory
# errors, so upstream being dirty where HEAD is clean is success, not failure. Only the
# reverse is a regression:
#
#     clean under pristine, dirty under HEAD   -> REGRESSION (this gate fails)
#     dirty under pristine, clean under HEAD   -> the fork doing its job
#     dirty under both                         -> pre-existing, reported not failed
#
# A MACHINE MUST BE HANDED A FILE OR IT NEVER CONSTRUCTS. Measured: `-E testmips` with no
# file prints usage and aborts before any device is attached -- a sweep built that way
# would exercise nothing and pass vacuously. With a dummy image the machine reports
# `model:`, `cpu:`, `memory:` and attaches devices. Machines with subtypes additionally
# need `-e <subtype>`; without it 13 of 37 types never construct.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

ASAN_HEAD=/tmp/gx-asan-head/gxemul
ASAN_PRI=/tmp/gx-asan-pristine/gxemul
DUMMY=$LOGDIR/dummy.elf

gate_begin "asan-machine-sweep"

[ -x "$ASAN_HEAD" ] || gate_skip "no ASan build -- see regress/README.md (build_asan)"

# Leak reporting off: the emulator is killed mid-run, so exit-time leaks are expected and
# say nothing about correctness. ASan's memory-error detection is unaffected.
export ASAN_OPTIONS=detect_leaks=0:abort_on_error=0:print_summary=1
export UBSAN_OPTIONS=print_stacktrace=0

# Minimal file so machine construction proceeds past the loader.
printf '\x7fELF\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x08\x00\x00\x00\x01' > "$DUMMY"
head -c 512 /dev/zero >> "$DUMMY"

# Build "type[:subtype]" list: every top-level machine type, with its first subtype when
# the type needs one to construct.
"$ASAN_HEAD" -H 2>&1 > "$LOGDIR/help.txt"
awk '
  /^        [A-Za-z].*\("/ { if (match($0, /\("[a-z0-9_.-]+"/)) {
        t=substr($0, RSTART+2, RLENGTH-3); type=t; print "T " t; next } }
  /^            - .*\("/   { if (match($0, /\("[a-z0-9_.-]+"/)) {
        s=substr($0, RSTART+2, RLENGTH-3); print "S " type " " s } }
' "$LOGDIR/help.txt" > "$LOGDIR/mtypes.txt"

run_machine() {   # binary, type, subtype(optional), outfile
    local bin=$1 t=$2 s=$3 out=$4
    if [ -n "$s" ]; then
        timeout 25 "$bin" -V -E "$t" -e "$s" "$DUMMY" </dev/null > "$out" 2>&1
    else
        timeout 25 "$bin" -V -E "$t" "$DUMMY" </dev/null > "$out" 2>&1
    fi
}

# constructed? -- did devices actually attach
constructed() { grep -qa "cpu:" "$1" && grep -qa "memory:" "$1" && echo yes || echo no; }
# sanitizer hit? -- ASan or UBSan diagnostic present
sanhit() { grep -acE "AddressSanitizer|runtime error:|SEGV|heap-buffer-overflow|stack-buffer|use-after-free" "$1"; }

types=$(grep '^T ' "$LOGDIR/mtypes.txt" | awk '{print $2}')
n_total=0; n_built=0; n_regress=0; n_fixed=0; n_both=0
: > "$LOGDIR/asan_findings.txt"

printf "  %-14s %-10s %-9s %-9s %s\n" "machine" "subtype" "built" "pristine" "HEAD"
for t in $types; do
    # bare first; if it does not construct, retry with its first subtype
    sub=""
    run_machine "$ASAN_HEAD" "$t" "" "$LOGDIR/asan_head.txt"
    if [ "$(constructed "$LOGDIR/asan_head.txt")" = no ]; then
        sub=$(awk -v t="$t" '$1=="S" && $2==t {print $3; exit}' "$LOGDIR/mtypes.txt")
        [ -n "$sub" ] && run_machine "$ASAN_HEAD" "$t" "$sub" "$LOGDIR/asan_head.txt"
    fi
    built=$(constructed "$LOGDIR/asan_head.txt")
    h=$(sanhit "$LOGDIR/asan_head.txt")

    p="-"
    if [ -x "$ASAN_PRI" ]; then
        run_machine "$ASAN_PRI" "$t" "$sub" "$LOGDIR/asan_pri.txt"
        p=$(sanhit "$LOGDIR/asan_pri.txt")
    fi

    n_total=$((n_total+1))
    [ "$built" = yes ] && n_built=$((n_built+1))
    printf "  %-14s %-10s %-9s %-9s %s\n" "$t" "${sub:--}" "$built" "$p" "$h"

    if [ "$p" != "-" ]; then
        if [ "$p" = 0 ] && [ "$h" != 0 ]; then
            n_regress=$((n_regress+1))
            echo "REGRESSION $t ${sub:-} -- clean upstream, $h hit(s) on HEAD" >> "$LOGDIR/asan_findings.txt"
            grep -aE "AddressSanitizer|runtime error:" "$LOGDIR/asan_head.txt" | head -3 \
                | sed 's/^/       /'
        elif [ "$p" != 0 ] && [ "$h" = 0 ]; then
            n_fixed=$((n_fixed+1))
        elif [ "$p" != 0 ] && [ "$h" != 0 ]; then
            n_both=$((n_both+1))
        fi
    fi
done

echo
note "machine types swept       : $n_total"
note "of which constructed      : $n_built"
[ -x "$ASAN_PRI" ] && {
    note "fixed by the fork         : $n_fixed  (dirty upstream, clean on HEAD)"
    note "pre-existing, still dirty : $n_both   (reported, not failed)"
}

# A FLOOR, so a broken enumeration cannot pass by sweeping nothing.
check_min "machine types enumerated"      "$n_total" 20
check_min "machine types constructed"     "$n_built" 20
if [ -x "$ASAN_PRI" ]; then
    check "machines clean upstream but dirty on HEAD" "$n_regress" "0"
else
    degrade "no ASan pristine build -- HEAD swept, but no three-way comparison"
fi

gate_end
exit $?
