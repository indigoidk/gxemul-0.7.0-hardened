#!/bin/bash
#  legs566.sh -- #566's measurement legs for the ip30_abort gate block, run in a SCRATCH CLONE of build/
#  (/tmp/gx566), never in build/ itself (the 2026-08-28 kill-table default).
#
#  BASELINE: SEC HEAD.  build/ carries five uncommitted files of another session (alpha/lca/pcc2/sh4 and
#  mvme_pcctworeg.h); the clone has those five set back to HEAD before anything is built, and the clone's
#  dev_sgi_ip30.c is checked byte-identical to HEAD's.
#
#  [ANNOTATED 2026-10-18 after the run, on #566's pass 2 (Grok 4.7) and F2 (GPT-6 Astra): the `prefix' leg below is
#  clause (a) ONLY.  A whole-file restore removes the rest of #531's fix along with the four abort() calls; clause (b)
#  is abort() re-inserted at each fixed site of the FIXED file, and no table holds it.  The text below is as it ran.]
#  LEGS (each scored by the block's own scoring text, extracted from the working tree's gate_arm.sh):
#    base    HEAD, rebuilt in the clone                         -> must be GREEN (all checks)
#    prefix  HEAD with dev_sgi_ip30.c set to 686d179c^ (= the     -> must RED   (clause (a); it is also the
#            upstream import, the only other version) -- the        verbatim reinstatement of every fixed
#            four abort() calls back                                site, clause (b), since #531 touched no
#                                                                    other source file)
#    absent  /nonexistent/gxemul                                -> must RED   (clause (c), null medium)
#    nonemu  /bin/true                                          -> must RED   (clause (c), null medium)
set -u
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build
W=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/w566
C=/tmp/gx566
OUT=$SEC/regress/artifacts/ip30abortkill/gatewire_20261018/legs
mkdir -p "$OUT"
echo "LEGS566 start $(date '+%F %T')"
echo "probe md5 $(md5sum < "$SEC/regress/artifacts/ip30abortkill/ip30_abort_probe.py" | cut -c1-32)  gate_arm.sh md5 $(md5sum < "$SEC/regress/gate_arm.sh" | cut -c1-32)"

rm -rf "$C"
cp -a "$B" "$C" || { echo "CLONE FAILED"; exit 9; }
echo "SCRATCH CLONE of build/ (#566): five shared sources set to HEAD; dev_sgi_ip30.c is mutated by the prefix leg" > "$C/.MUTANT"
for f in src/cpus/cpu_alpha_palcode.c src/devices/dev_lca.c src/devices/dev_pcc2.c src/devices/dev_sh4.c src/include/thirdparty/mvme_pcctworeg.h; do
    cp "$W/headsrc/$f" "$C/$f" || { echo "COPY FAILED $f"; exit 9; }
    echo "set to HEAD: $f"
done
rm -f "$C/src/devices/dev_lca.o" "$C/src/devices/dev_pcc2.o" "$C/src/devices/dev_sh4.o" \
      "$C/src/devices/dev_clmpcc.o" "$C/src/machines/machine_mvme88k.o"
cmp -s "$W/head_dev_sgi_ip30.c" "$C/src/devices/dev_sgi_ip30.c" && echo "clone dev_sgi_ip30.c == HEAD" \
    || { echo "clone dev_sgi_ip30.c is NOT HEAD -- stop"; exit 9; }

build() {
    (cd "$C" && rm -f src/cpus/*.o src/devices/dev_sgi_ip30.o && make -j4 > "$OUT/build_$1.log" 2>&1)
    echo "make rc=$? ($1)"
    for f in src/devices/dev_sgi_ip30.c src/devices/dev_lca.c src/devices/dev_pcc2.c src/devices/dev_sh4.c \
             src/cpus/cpu_alpha_palcode.c src/include/thirdparty/mvme_pcctworeg.h; do
        [ "$C/gxemul" -nt "$C/$f" ] || { echo "BINARY NOT NEWER THAN $f ($1) -- stop"; exit 9; }
    done
    echo "binary fresh ($1): $(ls -la --time-style=+%T "$C/gxemul" | awk '{print $6, $5}')"
}
run() {
    t0=$(date +%s)
    (cd "$SEC/regress" && timeout 1500 python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "$2" gate > "$OUT/probe_$1.log" 2>&1)
    prc=$?
    echo "$prc" > "$OUT/probe_$1.rc"
    echo "probe $1: rc=$prc $(( $(date +%s) - t0 ))s  $(grep -a '^IP30ABORT_RESULT=' "$OUT/probe_$1.log" | tr '\n' ' ') last=[$(tail -1 "$OUT/probe_$1.log")]"
}

build base
run base "$C/gxemul"
cp "$W/upstream_dev_sgi_ip30.c" "$C/src/devices/dev_sgi_ip30.c"
echo "clone dev_sgi_ip30.c := 686d179c^ (the upstream import): $(grep -c 'abort()' "$C/src/devices/dev_sgi_ip30.c") abort() calls"
build prefix
run prefix "$C/gxemul"
run absent /nonexistent/gxemul
run nonemu /bin/true

#  Score each log with the scoring text that ships -- extracted from gate_arm.sh, from the line after the probe
#  invocation through the block's closing `fi'.
T=$(mktemp -d)
awk '/python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' \
    "$SEC/regress/gate_arm.sh" > "$T/score.sh"
grep -q '^fi$' "$T/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
echo "scoring text: $(wc -l < "$T/score.sh") lines, md5 $(md5sum < "$T/score.sh" | cut -c1-32)"
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
for leg in base prefix absent nonemu; do
    IP30LOG=$OUT/probe_$leg.log; ip30rc=$(cat "$OUT/probe_$leg.rc"); _checks=0; _fails=0; _red=""
    . "$T/score.sh" > /dev/null 2>&1
    want=$([ "$leg" = base ] && echo GREEN || echo RED)
    got=$([ "$_fails" -gt 0 ] && echo RED || echo GREEN)
    printf 'LEG %-7s gate checks=%-3s fails=%-3s %-5s %s\n' "$leg" "$_checks" "$_fails" "$got" \
        "$([ "$got" = "$want" ] && echo "as required" || echo "*** NOT AS REQUIRED ***")"
    [ "$leg" = base ] || echo "      red:$(echo "$_red" | cut -c1-400)"
done
rm -rf "$T"
echo "clone left at $C with its .MUTANT sentinel (scratch; build/ untouched)"
echo "LEGS566 end $(date '+%F %T')"
echo LEGS566_DONE
