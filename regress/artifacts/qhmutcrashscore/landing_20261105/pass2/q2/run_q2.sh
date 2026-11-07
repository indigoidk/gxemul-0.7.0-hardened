#!/bin/bash
#  run_q2.sh -- the pass-2 Q2 measurement, in WSL Gentoo, scratch only:
#     MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc/landing/q2/run_q2.sh
#  Runs each gate from q2/gates/ (mk_q2.py) through the research's own W2 control driver -- a frozen copy of
#  wkdc/witness/w2_gate3.sh whose ONLY change is its output directory (q2/driver_vs_input.diff says so) -- on the three
#  stub sets: allcrash (every mutant raises SIGFPE before any output), mixed (two genuine kills, one genuine survivor,
#  two SIGFPE endings, an exit(1), an empty log) and allkill (every mutant a genuine kill).  Each leg is gate 3 run whole
#  in a fake ROOT with the stub in place of diff_ieee_store.c; nothing outside q2/ is written.  Then compare_q2.py.
set -u
if [ -z "${GXKIT_FROZEN:-}" ]; then
	_fz="$(cd "$(dirname "$0")" && pwd)/run_q2.run-$(date +%Y%m%d_%H%M%S)-$$.sh"
	cp "$0" "$_fz" && GXKIT_FROZEN=1 exec bash "$_fz" "$@"
	echo "could not freeze $0"; exit 9
fi
Q=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc/landing/q2
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
exec > "$Q/RUN_Q2.log" 2>&1
echo "run_q2 start $(date '+%F %T')"
sed "s#^X=\$W/witness/g3\$#X=$Q/g3#" "$W/witness/w2_gate3.sh" > "$Q/w2_gate3_q2.sh"
diff "$W/witness/w2_gate3.sh" "$Q/w2_gate3_q2.sh" > "$Q/driver_vs_input.diff"
echo "driver: w2_gate3.sh md5 $(md5sum < "$W/witness/w2_gate3.sh" | cut -c1-32) -> w2_gate3_q2.sh md5 $(md5sum < "$Q/w2_gate3_q2.sh" | cut -c1-32); the only difference:"
sed 's/^/    /' "$Q/driver_vs_input.diff"
[ "$(grep -c '^[<>]' "$Q/driver_vs_input.diff")" = 2 ] || { echo "the driver copy differs in more than its output line -- refusing"; echo RUN_Q2_DONE; exit 2; }
mkdir -p "$Q/g3"
for g in STAGED M_q2a M_q2b; do
	for st in allcrash mixed allkill; do
		bash "$Q/w2_gate3_q2.sh" "$Q/gates/$g.sh" "$g" "$st"
		echo "leg $g $st: driver rc=$?  $(grep -a 'selftest-float-emul-can-fail:' "$Q/g3/W2_$g.$st.log" | tail -1)  sentinel: $(tail -1 "$Q/g3/W2_$g.$st.log")"
	done
done
echo "RUN_Q2_DONE $(date '+%F %T')"
