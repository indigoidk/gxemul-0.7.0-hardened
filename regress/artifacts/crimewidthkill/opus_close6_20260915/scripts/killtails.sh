#!/bin/bash
pkill -f 'gxopuscrimec6_work/lane_' ; sleep 1
ps -eo pid,args | grep -E '[g]xopuscrimec6' || echo "no processes reference the clone"
