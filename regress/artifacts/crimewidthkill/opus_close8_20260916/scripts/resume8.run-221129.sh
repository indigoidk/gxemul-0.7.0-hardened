#!/bin/bash
#  resume8.run-221129.sh -- CLOSING PASS 8 RESUME, 2026-09-16 22:1x.  Frozen at creation; do not edit while running.
#  Runs table A's SIX remaining legs (the four TRUNCATED ones plus the two never started), then table B, SERIALLY
#  -- both carry wall-clock oracles and the carrier's rule is to serialize anything CPU-heavy against them.
#  Pass-1's eight VALID legs are preserved at logs/pass1_preserved/ and are NOT re-run: the targeting rule is that
#  a re-run is owed only where the thing measured changed, and nothing about those eight did.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
echo "RESUME8 START $(date +%Y-%m-%d_%H:%M:%S)"
LIST="W_rev4r_out G_lane_ist G_lane_tim G_lane_all D1_landpost D2_remappost"     bash "$A/scripts/kill8.run-221129.sh" > "$A/logs/table8_resume.out" 2>&1
rcA=$?
echo "TABLE A REMAINDER rc=$rcA  sentinel=$(grep -c KILL8_DONE "$A/logs/table8_resume.out") at $(date +%H:%M:%S)"
tail -12 "$A/logs/table8_resume.out"
if ! grep -q KILL8_DONE "$A/logs/table8_resume.out"; then echo "TABLE A DID NOT FINISH -- NOT starting table B"; exit 1; fi
echo "=== TABLE B START $(date +%H:%M:%S) ==="
bash "$A/scripts/kill8b.run-221129.sh" > "$A/logs2/table8b.out" 2>&1
rcB=$?
echo "TABLE B rc=$rcB  sentinel=$(grep -c KILL8B_DONE "$A/logs2/table8b.out") at $(date +%H:%M:%S)"
tail -30 "$A/logs2/table8b.out"
echo "RESUME8_DONE $(date +%H:%M:%S)"
