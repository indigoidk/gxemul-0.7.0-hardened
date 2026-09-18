#!/bin/bash
IMG=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/wdc-scratch-64m.img
P=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918/iq_devlist.py
for T in base fix; do
  echo "== $T  evbarm/iq80321"; python3 $P /tmp/gxopus_lax_$T/gxemul -E evbarm -e iq80321 -d iR:$IMG
  echo "== $T  hpcmips/mobilepro770"; python3 $P /tmp/gxopus_lax_$T/gxemul -E hpcmips -e mobilepro770 -d iR:$IMG
done
