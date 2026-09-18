#!/bin/bash
#  Run the F2 probe and the shipped witness against HEAD and variants A/B/C, one instrument
#  (frozen copy) for all four.  READ-ONLY against every tree; mutates nothing.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
ART=$SEC/regress/artifacts/lcaisalane/opus_f2_20260913
R=/tmp/gxlcaf2
P=$ART/lca_f2_probe.frozen.py
W=$ART/lca_isalane_probe.frozen.py
cp "$ART/lca_f2_probe.py" "$P"
cp "$SEC/regress/lca_isalane_probe.py" "$W"
mkdir -p "$ART/logs"

for v in head A B C; do
	B=$R/$v/gxemul
	if [ ! -x "$B" ]; then echo "SKIP $v: no binary"; continue; fi
	echo "===== F2 probe: $v ====="
	mkdir -p "$ART/logs/raw_f2_$v"
	LCAF2_RAW="$ART/logs/raw_f2_$v" python3 -u "$P" "$B" "$v" > "$ART/logs/f2_$v.out" 2>&1
	tail -1 "$ART/logs/f2_$v.out"
	echo "===== witness: $v ====="
	python3 -u "$W" "$B" "$v" > "$ART/logs/witness_$v.out" 2>&1
	tail -1 "$ART/logs/witness_$v.out"
done
echo RUN_PROBE_DONE
