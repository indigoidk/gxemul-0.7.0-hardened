#!/bin/bash
# Opus seat, q2e: four worker trees (copies of /tmp/opusq2e), the driver and generator FROZEN into a run directory,
# four drivers in parallel, then a check that every worker restored its tree.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/frozen
NW=4
RUN=/tmp/opusq2e_run_$(date +%H%M%S)
mkdir -p "$RUN"
cp "$O/driver_q2e.py" "$O/gen_q2e.py" "$RUN/"
md5sum "$RUN/driver_q2e.py" "$RUN/gen_q2e.py"
cmp /tmp/opusq2e/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || { echo "base tree device != frozen"; exit 9; }
[ -e /tmp/opusq2e/.MUTANT ] && { echo "base tree carries a sentinel"; exit 9; }
for k in $(seq 0 $((NW - 1))); do
	rm -rf /tmp/opusq2e_w$k
	cp -a /tmp/opusq2e /tmp/opusq2e_w$k
	rm -f /tmp/opusq2e_w$k/regress/d
done
for k in $(seq 0 $((NW - 1))); do
	python3 -u "$RUN/driver_q2e.py" $k $NW > "$O/driver_w$k.out" 2>&1 &
done
wait
for k in $(seq 0 $((NW - 1))); do
	tail -3 "$O/driver_w$k.out"
	cmp /tmp/opusq2e_w$k/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "w$k device == frozen"
	[ -e /tmp/opusq2e_w$k/.MUTANT ] && echo "w$k SENTINEL PRESENT" || echo "w$k no sentinel"
done
cat "$O"/results_w*.jsonl > "$O/results_all.jsonl"
wc -l "$O/results_all.jsonl"
tar czf "$O/variant_logs_and_diffs.tar.gz" -C /tmp opusq2e_w0/logs opusq2e_w0/diffs opusq2e_w1/logs opusq2e_w1/diffs \
    opusq2e_w2/logs opusq2e_w2/diffs opusq2e_w3/logs opusq2e_w3/diffs
ls -la "$O/variant_logs_and_diffs.tar.gz"
echo RUN_TABLE_DONE
