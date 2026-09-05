#!/bin/bash
R=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress
rm -rf /tmp/gxinst501p4; mkdir -p /tmp/gxinst501p4
cp "$R/pcc2_default_probe.py" "$R/pcc2_width_probe.py" /tmp/gxinst501p4/
md5sum /tmp/gxinst501p4/*.py
