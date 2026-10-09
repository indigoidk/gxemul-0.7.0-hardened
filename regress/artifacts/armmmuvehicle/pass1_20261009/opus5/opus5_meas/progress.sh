#!/bin/bash
# progress of the parallel mutant builds: compile lines so far vs the base build's count
echo "base build cc lines (cpus only): $(grep '^cc ' /tmp/gxopusmmuv_build2.log | grep -c 'cpus\|^cc .*-c -o [a-z_0-9]*\.o [a-z_0-9]*\.c$')"
for m in M_dom0 M_farpage M_ttbstale M_l2idx11 M_domPS M_ckR M_pgdom0 M_permPS M_dabtret M_c8nop M_c2mask; do
  n=$(grep -c '^cc ' /tmp/gxopusmmuv_$m.build.log 2>/dev/null)
  last=$(tail -1 /tmp/gxopusmmuv_$m.build.log 2>/dev/null | cut -c1-50)
  echo "$m: $n cc lines; last: $last"
done
ls /tmp/gxopusmmuv_bins
