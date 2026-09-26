#!/bin/bash
cd /tmp/gxo549f2m/probe || exit 2
F2=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2
timeout 120 python3 -u "$F2/drive_cfg.py" /tmp/gxo549f2m/bins/gx_fix 2 - "emul" "machine" "print serial_nr" "focus 0,1" "print serial_nr" "machine" "focus 0,0" "print serial_nr" "print pc"
