#!/bin/bash
#  chain.sh -- wait for table A to finish, THEN run table B.  The two must not overlap: both carry wall-clock
#  oracles (`p t4w/t4r gap', `time * ctl', and table B's own `c t4w/c t4r gap'), and the carrier's rule is to
#  serialize anything CPU-heavy against a run with a load-sensitive oracle.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
until grep -q KILL8_DONE "$A/logs/table8.out" 2>/dev/null; do sleep 30; done
echo "TABLE A COMPLETE at $(date +%H:%M:%S) -- starting table B"
bash "$A/scripts/kill8b.run-202251.sh"
echo "CHAIN_DONE"
