#!/bin/bash
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/landisk_census
mkdir -p "$D/logs"
cp /tmp/census_A_default.log  "$D/logs/A1_pristine_boot.log"
cp /tmp/census_A_run2.log     "$D/logs/A2_pristine_boot.log"
cp /tmp/census_A_run3.log     "$D/logs/A3_pristine_boot.log"
cp /tmp/census_A_watch.log    "$D/logs/A4_pristine_watchpoint.log"
cp /tmp/census_devlist.log    "$D/logs/A5_device_list.log"
cp /tmp/census_B_hook.log     "$D/logs/B1_hook_full_window.log"
#  The -v run is 12.6 MB; keep the head, every wdc/ALTSTATUS/non-existant line,
#  and the tail.  The FULL byte count is recorded so the trim is visible.
{
  echo "### TRIMMED EXTRACT of /tmp/census_A_verbose.log"
  echo "### FULL SIZE: $(wc -c < /tmp/census_A_verbose.log) bytes, $(wc -l < /tmp/census_A_verbose.log) lines"
  echo "### kept: first 120 lines, every wdc:/ALTSTATUS/ALT. CTRL/non-existant line, last 60 lines"
  echo "### ---------------- HEAD ----------------"
  head -120 /tmp/census_A_verbose.log
  echo "### ---------------- SELECTED ----------------"
  grep -aE 'wdc:|ALTSTATUS|ALT\. CTRL|non-existant' /tmp/census_A_verbose.log | sort | uniq -c | sort -rn | head -40
  echo "### ---------------- TAIL ----------------"
  tail -60 /tmp/census_A_verbose.log
} > "$D/logs/A6_pristine_verbose_TRIMMED.log"
#  build B is reproducible from this diff alone
diff -u /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/memory_rw.c \
        /tmp/gxcensusB/src/cpus/memory_rw.c > "$D/buildB_census_hook.diff"
cp /tmp/gxcensusA_build.log "$D/logs/buildA.log"
cp /tmp/gxcensusB_build.log "$D/logs/buildB.log"
ls -la "$D/logs"
