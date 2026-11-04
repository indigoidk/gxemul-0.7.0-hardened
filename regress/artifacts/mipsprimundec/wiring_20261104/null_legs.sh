#!/bin/bash
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
W=$G/GXEMUL-SEC/regress/artifacts/mipsprimundec/wiring_20261104
P=$G/GXEMUL-SEC/regress/artifacts/mipsprimundec/killtable_20261104/probe_frozen.py
python3 -u $P /bin/true null > $W/null_true.out 2>&1; echo "true rc=$?"
python3 -u $P /nonexistent/gxemul null > $W/null_absent.out 2>&1; echo "absent rc=$?"
grep -h "^MIPS_PRIMUNDEC_\(RESULT\|CONTROL\|SYMPTOM\)" $W/null_true.out $W/null_absent.out
