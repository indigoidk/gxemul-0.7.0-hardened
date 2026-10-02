#!/bin/bash
SP=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad
ART=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_pass2_20260913
L=/tmp/p2logs
cp $SP/crime_p2_text.py /tmp/crime_p2_text.FROZEN.py
for b in base l_addrmask l_noonce; do python3 -u /tmp/crime_p2_text.FROZEN.py /tmp/p2bins/$b $b; done > $L/text_probe.out 2>&1
cat $L/text_probe.out
# completion-sentinel check before preserving
for f in $L/probe_*.raw; do [ "$(tail -1 $f)" = CRIMEP_DONE ] || echo "INCOMPLETE $f"; done
for f in $L/esc_*.raw; do [ "$(tail -1 $f)" = P2ESC_DONE ] || echo "INCOMPLETE $f"; done
tail -1 $L/table.out
mkdir -p $ART/logs $ART/scripts
cp $L/* $ART/logs/
cp /tmp/p2_esc_base.out $ART/logs/esc_base_standalone.raw
cp /tmp/crime_p2.FROZEN.py $ART/scripts/crime_width_probe.pass2frozen.py
cp /tmp/crime_p2_escape.FROZEN.py $ART/scripts/crime_p2_escape.py
cp /tmp/mutants_p2.FROZEN.py $ART/scripts/mutants_p2.py
cp /tmp/crime_p2_text.FROZEN.py $ART/scripts/crime_p2_text.py
cp $SP/p2_setup.sh $SP/p2_table.sh $SP/p2_text_and_save.sh $ART/scripts/
md5sum $ART/scripts/* > $ART/scripts/MD5SUMS
ls -la $ART $ART/logs | head -80
echo SAVE_DONE
