#!/usr/bin/env bash
echo "--- control console:"; cat /tmp/opus524_control_console.txt 2>/dev/null | tail -25
echo "--- ldmdb outs:"; ls /tmp/opus524_out/ldmdb_* 2>/dev/null
echo "--- live:"; ps -eo pid,etime,comm,args | grep -E '[c]ontrol_run|[l]dmdb_control|[c]c1 ' | head -4
