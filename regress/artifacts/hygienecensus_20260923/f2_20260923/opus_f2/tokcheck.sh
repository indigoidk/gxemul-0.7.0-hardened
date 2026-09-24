#!/bin/bash
# run tokcheck.py over the run-2 copies (all under /tmp; read-only)
W=/tmp/opus_censusf2b
T=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/census0923/opus_f2/tokcheck.py
python3 "$T" "$W/snap/GXEMUL-SEC/regress" $(for c in n1a n1b n1c n1d n2a n2b n9 n3j n3m n5a; do echo "$W/c/$c/GXEMUL-SEC/regress"; done)
