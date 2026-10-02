#!/bin/bash
grep -cE 'cpu_[a-z0-9]+\.c|cc .*cpu' /tmp/gxopuscrimec6_work/build_base.log; grep -E 'cpu_mips|dev_sgi_ip32' /tmp/gxopuscrimec6_work/build_base.log | head -5
ls -la --time-style=full-iso /tmp/gxopuscrimec6/src/cpus/cpu_mips.o /tmp/gxopuscrimec6/src/devices/dev_sgi_ip32.o /tmp/gxopuscrimec6/gxemul /tmp/gxopuscrimec6/src/devices/dev_sgi_ip32.c
cd /tmp/gxopuscrimec6_bins; for b in *; do cmp -s base $b && echo "$b == base" || echo "$b differs"; done
ls /tmp/gxopuscrimec6/.MUTANT 2>&1
