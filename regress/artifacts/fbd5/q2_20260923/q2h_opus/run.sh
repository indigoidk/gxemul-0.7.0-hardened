#!/bin/bash
# Opus seat q2h: six worker trees (copies of /tmp/opusr3e), driver+generators FROZEN into a run dir, six drivers in
# parallel (foreground wait), then verify every worker restored its device.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen
NW=6
RUN=/tmp/opusr3e_run_$(date +%H%M%S)
mkdir -p "$RUN"
cp "$O"/driver.py "$O"/collect.py "$O"/gen_shapes.py "$O"/gen_shapes_b.py "$O"/gen_q2.py "$RUN/"
md5sum "$RUN"/*.py
cmp /tmp/opusr3e/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || { echo "base device != frozen"; exit 9; }
[ -e /tmp/opusr3e/.MUTANT ] && { echo "base tree carries a sentinel"; exit 9; }
rm -f "$O"/results_w*.jsonl
for k in $(seq 0 $((NW - 1))); do
	rm -rf /tmp/opusr3e_w$k
	cp -a /tmp/opusr3e /tmp/opusr3e_w$k
	rm -f /tmp/opusr3e_w$k/regress/b3d /tmp/opusr3e_w$k/regress/b3e /tmp/opusr3e_w$k/regress/d3d /tmp/opusr3e_w$k/regress/d3e
done
for k in $(seq 0 $((NW - 1))); do
	PYTHONDONTWRITEBYTECODE=1 python3 -u "$RUN/driver.py" $k $NW > "$O/driver_w$k.out" 2>&1 &
done
wait
echo "=== per-worker tails ==="
for k in $(seq 0 $((NW - 1))); do
	tail -2 "$O/driver_w$k.out"
	cmp /tmp/opusr3e_w$k/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "w$k device == frozen"
	[ -e /tmp/opusr3e_w$k/.MUTANT ] && echo "w$k SENTINEL PRESENT" || echo "w$k no sentinel"
done
cat "$O"/results_w*.jsonl > "$O/results_all.jsonl"
echo "result lines: $(wc -l < "$O/results_all.jsonl")"
echo RUN_DONE
