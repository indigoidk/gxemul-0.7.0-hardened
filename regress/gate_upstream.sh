#!/bin/bash
# GATE 8 -- run upstream GXemul's own tests, on all three builds.
#
# Why this gate is worth having when seven others already exist: everything else in this
# harness was authored by the same process that made the ~290 corrections. These tests
# were written by upstream, before the fork existed, so they encode UPSTREAM's definition
# of correct rather than ours. That independence is the point.
#
# WHAT IT ADDS THAT WE DID NOT ALREADY HAVE. The rigs do load kernels, so loader coverage
# was not zero -- but it was narrow. Measured:
#
#   our rigs load : a.out (bsd.pmax), ELF32 LSB MIPS (arc), ELF32 MSB PPC (macppc),
#                   gzip (landisk .rd)
#   this adds     : ELF64 (RISC-V LSB and SH5 MSB -- a separate code path from ELF32),
#                   b.out i960, MIPS16, and a NEGATIVE case (FileLoader_NonsenseFile),
#                   which is exactly the malformed-input handling the fork hardened
#
# The fork changed SEVEN files under src/file/. Even with this gate, ECOFF, Mach-O, SREC
# and Android still have no corpus here.
#
# TWO MISTAKES THIS GATE MADE ON ITS FIRST RUN, both fixed and both worth recording:
#
#  1. It used `-e testmips`. That is the SUBTYPE flag; the machine type flag is `-E`.
#     Every invocation therefore produced `Sorry, emulation "" (subtype "testmips") is
#     unknown.` -- and the gate compared that identical error across three builds and
#     reported 22 checks passing. Upstream's own configure comment still shows `-e`,
#     which is where the wrong flag came from; it predates the flag change.
#  2. Its only guard was a 100-byte floor on output, which an error message clears
#     easily. A floor proves VOLUME, not VALIDITY. Every case now asserts a
#     format-specific marker that only the real loader path can print -- "ELF64 LSB",
#     "b.out", "a.out" and so on -- so an error, a usage message or an empty run all fail.
#
# DELIBERATELY NOT INCLUDED: test/floatingpoint/fptest.c. It needs a cross-compiler to
# build a program that runs inside the emulator, and gate 2 already proves MORE about the
# one function fix #287 changed: it checks 20 million inputs and shows the difference from
# upstream is exactly what was intended, with nothing extra changed and nothing missed,
# and it has its own self-test proving it can fail. fptest would add the floating-point
# path end to end inside a guest -- worth having, but the most setup for the least new
# information. See README.md.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

SEC=$ROOT/GXEMUL-SEC
T=$SEC/test
PRISTINE=/tmp/gx-pristine/gxemul
PREBATCH=/tmp/gx-prebatch/gxemul
HEAD=$ROOT/build/gxemul

gate_begin "upstream-test-suite"
need_file "$T"
need_exec "$HEAD"

# --- upstream's static hygiene check ---------------------------------
# Every file calling `delete` must appear in its exceptions list. Costs milliseconds.
if [ -f "$T/check_delete_calls.sh" ]; then
    ( cd "$SEC" && sh test/check_delete_calls.sh ) > "$LOGDIR/check_delete.out" 2>&1
    check "upstream check_delete_calls.sh" "$?" "0"
    [ -s "$LOGDIR/check_delete.out" ] && head -6 "$LOGDIR/check_delete.out" | sed 's/^/       /'
else
    degrade "check_delete_calls.sh absent"
fi
echo

# --- upstream's loader corpus, three-way ------------------------------
if [ ! -x "$PRISTINE" ] || [ ! -x "$PREBATCH" ]; then
    degrade "baseline builds absent -- run gate_ab.sh --build for the three-way"
    gate_end; exit $?
fi

# Normalise the two things that legitimately differ between builds and between runs: the
# version string baked in by configure, and gxemul's random temp filename.
run_case() {   # machine, testfile, binary, outfile
    timeout 20 stdbuf -o0 "$3" -V -E "$1" "$T/$2" </dev/null 2>&1 \
        | sed -e 's|/tmp/gxemul\.[A-Za-z0-9]*|<TMP>|g' \
              -e 's/^GXemul [^ ]*/GXemul <VER>/' > "$4"
}

# THE LIST OF DIFFERENCES WE MEANT TO MAKE.
#
# This fork changed about 290 things on purpose, so "upstream and current differ" is not
# by itself a problem -- just counting differences is useless when hundreds are deliberate.
# What makes the comparison workable is sorting each difference into one of three boxes:
#
#     the same                          -> fine
#     differs, and it is fix #N         -> fine, and #N is named below
#     differs, and nobody knows why     -> REGRESSION
#
# Each entry below cancels out exactly one intended change, so anything still left over is
# unexplained by definition. Adding an entry is a deliberate act: it says "we changed this
# on purpose, under this fix number".
#
#   #260 -- net diagnostics were routed through debugmsg(SUBSYS_NET, ...), which prefixes
#           them with "net: ". Upstream printed them bare.
intended_norm() {
    sed -e 's/^\(  *\)net: /\1/'
}

note "upstream loader corpus across pristine / pre-batch / HEAD"
note "'raw' = differences vs upstream; 'unexpl' = what remains after known-intended ones"
printf "  %-26s %-11s %-10s %-11s %s\n" "case" "loader-ran" "raw-diff" "unexplained" "pre=HEAD"

# machine : file : marker only the real loader path can print
for spec in "testmips:FileLoader_ELF_MIPS:ELF32 MSB" \
            "testmips:FileLoader_ELF_MIPS16:ELF32 MSB" \
            "testriscv:FileLoader_ELF_RISCV64:ELF64 LSB" \
            "testsh:FileLoader_ELF_SH5:ELF64 MSB" \
            "testm88k:FileLoader_A.OUT_M88K:a.out" \
            "barei960:FileLoader_B.OUT_i960:b.out" \
            "testmips:FileLoader_NonsenseFile:symbol"; do
    m=${spec%%:*}; rest=${spec#*:}; f=${rest%%:*}; marker=${rest#*:}
    if [ ! -f "$T/$f" ]; then degrade "$f absent"; continue; fi

    run_case "$m" "$f" "$PRISTINE" "$LOGDIR/up_pri.txt"
    run_case "$m" "$f" "$PREBATCH" "$LOGDIR/up_pre.txt"
    run_case "$m" "$f" "$HEAD"     "$LOGDIR/up_head.txt"

    ran=$(grep -ac -- "$marker" "$LOGDIR/up_head.txt")

    # raw differences, before adjudication
    raw=$(diff "$LOGDIR/up_pri.txt" "$LOGDIR/up_head.txt" | grep -c '^[<>]')

    # after erasing every KNOWN-INTENDED change, nothing may remain
    intended_norm < "$LOGDIR/up_pri.txt"  > "$LOGDIR/up_pri_n.txt"
    intended_norm < "$LOGDIR/up_pre.txt"  > "$LOGDIR/up_pre_n.txt"
    intended_norm < "$LOGDIR/up_head.txt" > "$LOGDIR/up_head_n.txt"
    unexplained=$(diff "$LOGDIR/up_pri_n.txt" "$LOGDIR/up_head_n.txt" | grep -c '^[<>]')
    b=$(cmp -s "$LOGDIR/up_pre_n.txt" "$LOGDIR/up_head_n.txt" && echo same || echo DIFF)

    printf "  %-26s %-11s %-10s %-11s %s\n" "$f" \
        "$([ "$ran" != 0 ] && echo yes || echo NO)" "$raw" "$unexplained" "$b"

    # POSITIVE ASSERTION FIRST. Without it, three builds agreeing on an error message
    # counts as agreement -- which is exactly what this gate did on its first run.
    check_min "$f: loader ran ('$marker')"          "$ran"         1
    check     "$f: unexplained diffs vs upstream"   "$unexplained" "0"
    check     "$f: pre-batch == HEAD"               "$b"           "same"
    if [ "$unexplained" != 0 ] || [ "$b" = DIFF ]; then
        diff "$LOGDIR/up_pri_n.txt" "$LOGDIR/up_head_n.txt" | head -8 | sed 's/^/       /'
    fi
done

gate_end
exit $?
