#!/bin/bash
#  $1 = label ; runs the LIVE (unedited) 36-row detector against the clone binary
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress || exit 9
python3 -u pcc2_default_probe.py /tmp/gxopus501p3/gxemul "$1" 2>&1
