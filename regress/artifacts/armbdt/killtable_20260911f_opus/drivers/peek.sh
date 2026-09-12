#!/usr/bin/env bash
echo "--- clone sentinel:"; ls -la /tmp/gxopus524c/.MUTANT 2>&1 | head -1
echo "--- SCORES so far:"; cat /tmp/opus524_out/SCORES.txt 2>&1
echo "--- raws:"; ls -la /tmp/opus524_out/ 2>&1 | tail -20
echo "--- live processes (PPID + start, name-grep is blind on MSYS but fine in WSL):"
ps -eo pid,ppid,etime,comm,args 2>/dev/null | grep -E '[t]able_opus|[c]c1|[g]xemul|[m]ake' | head -10
