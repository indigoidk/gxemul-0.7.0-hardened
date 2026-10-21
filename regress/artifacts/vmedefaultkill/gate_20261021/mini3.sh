#!/bin/bash
#  mini3.sh <PMAX> <tag> -- gate 14's #568 block ALONE, extracted verbatim from the working gate_arm.sh
#  (from its `vmedefaultkill (#568)' banner to the first `fi' at column 0 after it).
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
O=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/gate3
export PMAX=$1; TAG=$2
export LOGDIR=/tmp/gx568mini_$TAG; rm -rf $LOGDIR; mkdir -p $LOGDIR
awk '/vmedefaultkill \(#568\)$/{p=1} p{print} p&&/^fi$/{exit}' $R/gate_arm.sh > $O/block568_extracted.sh
echo "block lines: $(wc -l < $O/block568_extracted.sh)  probe md5 $(md5sum < $R/vme_default_probe.py | cut -c1-32)  binary $(md5sum < $PMAX | cut -c1-32)"
cd $R
{ . ./lib.sh
  gate_begin "gate 14 (#568 vme block only, rev 3, $TAG)"
  need_exec "$PMAX"
  note "binary : $PMAX"
  . $O/block568_extracted.sh
  gate_end; }
