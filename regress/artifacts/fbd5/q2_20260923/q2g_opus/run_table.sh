#!/bin/bash
# Opus seat, q2g: six worker trees (copies of /tmp/opusr3d), the driver and generator FROZEN into a run directory,
# six drivers in parallel (foreground wait), then a check that every worker restored its tree.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/frozen
NW=6
RUN=/tmp/opusr3d_run_$(date +%H%M%S)
mkdir -p "$RUN"
cp "$O/driver_q2g.py" "$O/gen_r3d_opus.py" "$RUN/"
md5sum "$RUN/driver_q2g.py" "$RUN/gen_r3d_opus.py"
cmp /tmp/opusr3d/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || { echo "base tree device != frozen"; exit 9; }
cmp /tmp/opusr3d/regress/diff_footbridge.c "$F/diff_footbridge.c" || { echo "base tree harness != frozen"; exit 9; }
[ -e /tmp/opusr3d/.MUTANT ] && { echo "base tree carries a sentinel"; exit 9; }
for k in $(seq 0 $((NW - 1))); do
	rm -rf /tmp/opusr3d_w$k
	cp -a /tmp/opusr3d /tmp/opusr3d_w$k
	rm -f /tmp/opusr3d_w$k/regress/d
done
for k in $(seq 0 $((NW - 1))); do
	python3 -u "$RUN/driver_q2g.py" $k $NW > "$O/driver_w$k.out" 2>&1 &
done
wait
for k in $(seq 0 $((NW - 1))); do
	tail -3 "$O/driver_w$k.out"
	cmp /tmp/opusr3d_w$k/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "w$k device == frozen"
	[ -e /tmp/opusr3d_w$k/.MUTANT ] && echo "w$k SENTINEL PRESENT" || echo "w$k no sentinel"
done
cat "$O"/results_w*.jsonl > "$O/results_all.jsonl"
wc -l "$O/results_all.jsonl"
tar czf "$O/variant_logs_and_diffs.tar.gz" -C /tmp $(for k in $(seq 0 $((NW - 1))); do echo opusr3d_w$k/logs opusr3d_w$k/diffs; done)
ls -la "$O/variant_logs_and_diffs.tar.gz"
echo RUN_TABLE_DONE
