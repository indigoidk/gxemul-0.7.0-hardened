#!/bin/bash
#  setup.sh -- closing pass 8 (Opus measuring seat).  Make MY OWN scratch clone from the table-11 clone,
#  after NAMING THE BASELINE and cmp-ing the file-to-be-mutated against it (the carrier's clone recipe,
#  step 1).  No project tree is touched.
set -u
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
A=$SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
F=src/devices/dev_sgi_ip32.c
{
echo "SETUP $(date +%Y-%m-%d\ %H:%M:%S)"
echo "=== BASELINE NAMED: the #529 working set = GXEMUL-SEC/$F (UNCOMMITTED; git status shows it M) ==="
md5sum /tmp/gxopuscrime/$F "$SEC/$F"
cmp -s /tmp/gxopuscrime/$F "$SEC/$F" && echo "table-11 clone SRC == baseline" || echo "table-11 clone SRC DIVERGENT -- ABORT"
cmp -s /tmp/gxopuscrime/$F "$SEC/$F" || exit 1
echo "=== clone ==="
rm -rf /tmp/gxopusc8
cp -a /tmp/gxopuscrime /tmp/gxopusc8
mkdir -p /tmp/gxopusc8_bins
cp /tmp/gxcrime529k_bins/base /tmp/gxopusc8_bins/base
echo "=== MY CLONE STATE ==="
ls -la /tmp/gxopusc8/gxemul /tmp/gxopusc8/$F
cmp -s /tmp/gxopusc8/$F "$SEC/$F" && echo "MYCLONE SRC CLEAN vs SEC" || echo "MYCLONE SRC DIVERGENT"
if [ /tmp/gxopusc8/gxemul -nt /tmp/gxopusc8/$F ]; then echo "MYCLONE binary -nt source: YES"; else echo "MYCLONE binary -nt source: NO"; fi
ls -la /tmp/gxopusc8/.MUTANT 2>&1 | head -1
md5sum /tmp/gxopusc8_bins/base /tmp/gxcrime529k_bins/base /tmp/gxopusc8/gxemul
echo "=== shipped probe (the instrument under test) ==="
md5sum "$SEC/regress/crime_width_probe.py"
echo SETUP_DONE
} > "$A/logs/setup.out" 2>&1
cat "$A/logs/setup.out"
