#!/bin/bash
# kill529_13a.sh -- #529 TABLE 13a: a BASE leg on the current probe bytes (a0af7c92) and the two decline label swaps the
# flagship's first-hand re-ruling requires MEASURED (M7_intmasklatch, M8_ctllatch).  PRETABLE13a.out and check13a.py
# beside this file were both written FIRST; their mtimes prove it.
#
#   *** LAUNCH FROM A FROZEN COPY (cp kill529_13a.sh kill529_13a.run-<stamp>.sh) AND WITH run_in_background. ***
#   *** NOT WHILE ANOTHER CPU-HEAVY JOB RUNS: the probe's `c t4w/c t4r gap' rows are wall-clock oracles. ***
#   SCRATCH CLONE /tmp/gxopus_r14 ONLY.  No project tree is written except this artifacts directory.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/table13a_20260925
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus_r14
B=/tmp/gxopus_13a_bins
F=src/devices/dev_sgi_ip32.c
PROBE=$A/crime_width_probe.table13a.py
MUT=$A/mutants_13a.py
LIST="base M7_intmasklatch M8_ctllatch"

mkdir -p "$B" "$A/logs" "$A/builds" "$A/mutants"
echo "KILL529_13A_START $(date '+%F %T')"

#  ---- freeze the instrument; pin the bytes PRETABLE13a names ----
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
md5sum "$PROBE" "$MUT" "$SEC/$F" | tee "$A/logs/INSTRUMENT.md5"
cmp -s "$PROBE" "$SEC/regress/crime_width_probe.py" && echo "PROBE frozen == working" || { echo "PROBE mismatch -- abort"; exit 1; }
[ "$(md5sum < "$PROBE" | cut -c1-8)" = a0af7c92 ] || { echo "PROBE is not a0af7c92, the bytes PRETABLE13a names -- abort"; exit 1; }
[ "$(md5sum < "$SEC/$F" | cut -c1-8)" = 8c1d1545 ] || { echo "dev_sgi_ip32.c is not 8c1d1545 -- abort"; exit 1; }

cd "$C" || { echo "clone $C missing -- abort"; exit 1; }
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; fi
echo "$F  #529 table 13a -- restore dev_sgi_ip32.c from GXEMUL-SEC, then REBUILD (the synced files ARE the new baseline)" > .MUTANT

#  ---- sync the clone to the NAMED BASELINE: every tracked src .c/.h outside tools/est_divergence.txt ----
DIV=" $(grep -vE '^[[:space:]]*(#|$)' "$SEC/tools/est_divergence.txt" | tr '\n' ' ') "
nsync=0; ntrk=0
for f in $(cd "$SEC" && git -c safe.directory='*' ls-files src | grep -E '\.(c|h)$'); do
	case "$DIV" in *" $f "*) continue;; esac
	ntrk=$((ntrk+1))
	if ! cmp -s "$f" "$SEC/$f" 2>/dev/null; then cp "$SEC/$f" "$f"; echo "SYNCED $f"; nsync=$((nsync+1)); fi
done
echo "synced $nsync of $ntrk tracked shared src files"
nleft=0
for f in $(cd "$SEC" && git -c safe.directory='*' ls-files src | grep -E '\.(c|h)$'); do
	case "$DIV" in *" $f "*) continue;; esac
	cmp -s "$f" "$SEC/$f" 2>/dev/null || { echo "STILL DIFFERS $f"; nleft=$((nleft+1)); }
done
[ "$nleft" = 0 ] && echo "BASELINE_SYNC CLEAN ($ntrk shared files)" || { echo "sync incomplete -- abort"; exit 1; }
rm -f src/cpus/*.o

build() {
	rm -f src/devices/dev_sgi_ip32.o
	nice -n 19 make -j2 > "$A/builds/build_$1.log" 2>&1
	rc=$?
	if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
		cp gxemul "$B/$1"; echo "BUILD_OK $1 $(md5sum < gxemul | cut -c1-8)"
	else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$A/builds/build_$1.log"; return 1; fi
}
restore() {
	cp "$SEC/$F" "$F"
	build restored || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
	if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
		rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
	else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}

OK=""
for m in $LIST; do
	python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; continue; }
	diff -u "$SEC/$F" "$F" > "$A/mutants/$m.diff"
	if [ "$m" = base ]; then
		cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN after applying base" || { echo "base is not a no-op -- abort"; restore; exit 1; }
	fi
	if build "$m"; then OK="$OK $m"; else echo "NOTE $m DID NOT BUILD -- recorded as a RESULT, not retried"; fi
done
restore || exit 1
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "NOTE restored differs from base"
for m in $OK; do
	[ "$m" = base ] && continue
	cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"
done
echo "BUILDS DONE ($OK) $(date '+%F %T')"

#  ---- the edits, shown: each must be repair 14's latch_label() shape with only the label changed ----
for m in $OK; do [ "$m" = base ] && continue; echo "--- $m"; grep '^[+-][^+-]' "$A/mutants/$m.diff"; done

#  ---- probe: one lane per leg ----
leg() {
	m=$1
	case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; return;; esac
	log="$A/logs/probe_$m.raw"
	python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1
	echo "$m $(grep '^CRIMEP_RESULT=' "$log") $(grep '^CRIMEP_CONTROL=' "$log") done=$(grep -c '^CRIMEP_DONE' "$log") FAILING:$(grep '^FAILING:' "$log" | cut -c9-)"
}
i=0
for m in $LIST; do leg "$m" > "$A/logs/lane$i.out" 2>&1 & i=$((i + 1)); done
wait
echo "==== TABLE 13a RESULTS $(date '+%F %T') ===="
cat "$A"/logs/lane*.out
echo "--- mechanical scoring against PRETABLE13a (sharpened addendum) ---"
python3 "$A/check13a.py" 2>&1 | tee "$A/check13a.out"
echo "KILL529_13A_DONE $(date '+%F %T')"
