#!/bin/bash
#  insitu_gate3.sh -- gate 3 IN SITU for the qhmutcrashscore landing: four legs on the REAL build tree.
#  RUN IT ALONE (no other gate, probe, build, battery or panel on the machine), from git-bash, run_in_background,
#  NO timeout wrapper (~13 minutes per full leg, two full legs, so ~26-30 minutes):
#
#     MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc/landing/insitu_gate3.sh
#
#  Each leg runs gate 3 from its own FROZEN copy of regress/ (build_kit.py writes them under unit/insitu/; the frozen-copy
#  rule: one instrument per comparison) with ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL, so the gate picks build/ exactly as
#  the battery does, and with a PRIVATE LOGDIR, so the shared gate workdir /tmp/gxregress is never touched:
#    H  HEAD's selftest_mutation.sh,   HEAD's real diff_ieee_store.c   the baseline
#    S  the STAGED selftest_mutation.sh, HEAD's real diff_ieee_store.c   must print H's output exactly
#    C  the STAGED gate, the stub differential, STUBSET=allcrash        every mutant NOLOG rc=136, FAIL (7 of 15 checks)
#    K  the STAGED gate, the stub differential, STUBSET=allkill         PASS (15 checks)
#  build/'s inputs (config.h, src/include/float_emul.h, src/core/float_emul.c) are READ ONLY; their md5s are taken
#  before and after.  Writes only $K/insitu_<stamp>/ and $K/INSITU_G3.out, whose verdict line is
#  INSITU_G3_SUMMARY PASS|FAIL and whose last line is INSITU_G3_DONE.  On FAIL: do not land; read the leg logs.
set -u
#  FROZEN-COPY LAUNCH: bash reads a script incrementally, so editing it while it runs corrupts the run (measured on this
#  kit's own pretest_clone.sh, 2026-11-05: an edit during a run left a syntax error in its log).  Re-exec from a copy.
if [ -z "${GXKIT_FROZEN:-}" ]; then
	_fz="$(cd "$(dirname "$0")" && pwd)/pc/$(basename "$0" .sh).run-$(date +%Y%m%d_%H%M%S)-$$.sh"
	mkdir -p "$(dirname "$_fz")" && cp "$0" "$_fz" && GXKIT_FROZEN=1 exec bash "$_fz" "$@"
	echo "could not freeze $0 -- refusing to run from the live file"; exit 9
fi
K=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc/landing
RR=/mnt/c/DocumentNoSnc/CC/GXEMUL
STAMP=$(date +%Y%m%d_%H%M%S)
R=$K/insitu_$STAMP
OUT=$K/INSITU_G3.out
mkdir -p "$R"
exec > "$OUT" 2>&1
echo "insitu_gate3 start $(date '+%F %T')  run dir $R"
echo "script md5 $(md5sum < "$0" | cut -c1-32)"
echo "host: $(uname -srm)  cc: $( (cc --version || gcc --version) 2>/dev/null | head -1)"
echo "load at start: $(cat /proc/loadavg)"
echo "other gxemul/gate processes at start (want none): $(ps -eo pid,args | grep -E '[g]xemul |[g]ate_[a-z_]*\.sh|[r]un\.sh|[s]elftest_mutation' | grep -v insitu_gate3 | wc -l)"
fail=0
bad() { fail=$((fail + 1)); echo "  FAIL  $*"; }
good() { echo "  ok    $*"; }
B=$RR/build
inputs() { md5sum "$B/config.h" "$B/src/include/float_emul.h" "$B/src/core/float_emul.c" | sed "s#$RR/##"; }
[ -f "$B/config.h" ] && [ -f "$B/src/include/float_emul.h" ] || { echo "build/ is not configured -- gate 3 would SKIP"; echo "INSITU_G3_SUMMARY FAIL"; echo INSITU_G3_DONE; exit 2; }
[ -f "$B/.MUTANT" ] && { echo "build/.MUTANT is present -- restore build/ first"; cat "$B/.MUTANT"; echo "INSITU_G3_SUMMARY FAIL"; echo INSITU_G3_DONE; exit 2; }
inputs > "$R/inputs_before.md5"
echo "build/ inputs before:"; sed 's/^/    /' "$R/inputs_before.md5"
U=$K/unit/insitu
echo "frozen copies (unit/insitu/MD5.txt):"; sed 's/^/    /' "$U/MD5.txt"
echo "staged md5 $(md5sum < "$U/STAGED/regress/selftest_mutation.sh" | cut -c1-32)"
for leg in H S C K; do
	mkdir -p "$R/$leg/regress" "$R/$leg/logdir"
	case $leg in H) src=HEAD ;; *) src=STAGED ;; esac
	cp "$U/$src/regress/selftest_mutation.sh" "$U/$src/regress/lib.sh" "$R/$leg/regress/"
	case $leg in
	H|S) cp "$U/$src/regress/diff_ieee_store.c" "$R/$leg/regress/diff_ieee_store.c" ;;
	*)   cp "$U/stub_diff_ieee_store.c" "$R/$leg/regress/diff_ieee_store.c" ;;
	esac
done
run_leg() {   # leg [STUBSET]
	local leg=$1 st=${2:-} t0 t1 rc
	t0=$(date +%s)
	if [ -n "$st" ]; then
		STUBSET=$st ROOT=$RR LOGDIR=$R/$leg/logdir bash "$R/$leg/regress/selftest_mutation.sh" > "$R/$leg/gate.out" 2>&1
	else
		ROOT=$RR LOGDIR=$R/$leg/logdir bash "$R/$leg/regress/selftest_mutation.sh" > "$R/$leg/gate.out" 2>&1
	fi
	rc=$?
	t1=$(date +%s)
	echo "$rc" > "$R/$leg/rc"
	echo "leg $leg${st:+ (STUBSET=$st)}: gate exit $rc, $((t1 - t0)) s, $(grep -a 'selftest-float-emul-can-fail:' "$R/$leg/gate.out" | tail -1)"
}
run_leg H
run_leg S
run_leg C allcrash
run_leg K allkill
echo
echo "== checks"
v() { grep -a 'selftest-float-emul-can-fail:' "$R/$1/gate.out" | tail -1; }
[ "$(cat "$R/H/rc")" = 0 ] && [ "$(v H)" = "selftest-float-emul-can-fail: PASS (15 checks)" ] && good "H: HEAD's gate PASS (15 checks) on the real differential" || bad "H: HEAD's gate did not PASS (15 checks): $(v H)"
[ "$(cat "$R/S/rc")" = 0 ] && [ "$(v S)" = "selftest-float-emul-can-fail: PASS (15 checks)" ] && good "S: the staged gate PASS (15 checks) on the real differential" || bad "S: the staged gate did not PASS (15 checks): $(v S)"
if cmp -s "$R/H/gate.out" "$R/S/gate.out"; then good "S's whole gate output is byte-identical to H's ($(wc -l < "$R/S/gate.out") lines)"
else bad "S's gate output DIFFERS from H's:"; diff "$R/H/gate.out" "$R/S/gate.out" | head -20 | sed 's/^/        /'; fi
M=$R/S/logdir/mutation
lastline() { grep -av '^[[:space:]]*$' "$1" 2>/dev/null | tail -n 1; }   # a run log's last non-blank line
lastline "$M/real.out" | grep -aq '^DIFF_PASS' && good "S ground truth: the control's log ends DIFF_PASS" || bad "S ground truth: the control's log does not end DIFF_PASS"
n=0
for m in revert287 tiesaway modeignored wlegacyrounds revert303 maskcarry flushband; do
	if lastline "$M/mut_$m.out" | grep -aq '^DIFF_FAIL'; then n=$((n + 1)); else bad "S ground truth: mut_$m's log does not end DIFF_FAIL"; fi
done
[ $n = 7 ] && good "S ground truth: all seven mutants' logs end DIFF_FAIL"
[ "$(cat "$R/C/rc")" = 1 ] && [ "$(v C)" = "selftest-float-emul-can-fail: FAIL (7 of 15 checks)" ] && good "C: the staged gate with every mutant crashed FAILs (7 of 15 checks)" || bad "C: expected FAIL (7 of 15 checks), got: $(v C) (exit $(cat "$R/C/rc"))"
nc=$(grep -ac 'is DETECTED (must fail) *got=NOLOG rc=136 want=0' "$R/C/gate.out")
[ "$nc" = 7 ] && good "C: every mutant reads NOLOG rc=136 (7 of 7)" || bad "C: $nc of 7 mutants read NOLOG rc=136"
grep -aq 'ok   unmutated source passes gate 2 *1$' "$R/C/gate.out" && good "C: the control row is ok (1)" || bad "C: the control row is not ok"
[ "$(cat "$R/K/rc")" = 0 ] && [ "$(v K)" = "selftest-float-emul-can-fail: PASS (15 checks)" ] && good "K: the staged gate with every mutant a genuine kill PASS (15 checks)" || bad "K: expected PASS (15 checks), got: $(v K)"
inputs > "$R/inputs_after.md5"
cmp -s "$R/inputs_before.md5" "$R/inputs_after.md5" && good "build/'s inputs unchanged (md5 before == after)" || bad "build/'s inputs CHANGED during the run"
echo "load at end: $(cat /proc/loadavg)"
for leg in H S C K; do echo; echo "---- leg $leg: the gate's own output ----"; cat "$R/$leg/gate.out"; done
echo
if [ $fail = 0 ]; then echo "INSITU_G3_SUMMARY PASS"; else echo "INSITU_G3_SUMMARY FAIL ($fail)"; fi
echo "INSITU_G3_DONE"
