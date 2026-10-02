#!/bin/bash
ls -d /tmp/gx* 2>/dev/null; df -h /tmp | tail -1; nproc; uptime
ps -eo pid,etime,args | grep -E '[g]xemul|[p]ython3|[m]ake' | head -20
