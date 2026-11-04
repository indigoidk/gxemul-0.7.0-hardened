#!/bin/bash
# false_leg.sh -- the shipped regress/mips_primundec_probe.py against /bin/false (the regress review's extra null medium)
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
D=$R/artifacts/mipsprimundec/landing_20261104
cp $R/mips_primundec_probe.py $D/probe_shipped_frozen.py
md5sum $R/mips_primundec_probe.py $D/probe_shipped_frozen.py > $D/MD5_false.txt
python3 -u $D/probe_shipped_frozen.py /bin/false falseleg > $D/false.out 2>&1
echo "probe rc=$?"
grep -E '^MIPS_PRIMUNDEC_(RESULT|CONTROL|SYMPTOM)=' $D/false.out
grep -E '  ok$' $D/false.out | sed 's/  .*//' | tr '\n' ',' ; echo
tail -n 1 $D/false.out
