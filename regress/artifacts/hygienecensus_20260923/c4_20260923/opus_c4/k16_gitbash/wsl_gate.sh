#!/bin/bash
W=/mnt/c/Users/User00/AppData/Local/Temp/gxc4_k16gb
( cd "$W/GXEMUL-SEC/regress" && LOGDIR=/tmp/gxc4_k16gb_logs bash ./gate_hygiene.sh ) 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
    | grep -E '^\s*FAIL.*(readiness|whole-buffer)' | sed 's/^\s*/   /'
rm -rf /tmp/gxc4_k16gb_logs; echo "   (end of FAIL rows)"
