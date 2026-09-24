#!/bin/bash
# Opus seat, #545 q2c: four worker trees (copies of /tmp/opusq2c), the driver and generator FROZEN into a run
# directory, four drivers in parallel, then a check that every worker restored its tree.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/frozen
NW=4
STAMP=$(date +%H%M%S)
RUN=/tmp/opusq2c_run_$STAMP
mkdir -p "$RUN"
cp "$O/driver_q2c.py" "$O/gen_variants.py" "$RUN/"
md5sum "$RUN/driver_q2c.py" "$RUN/gen_variants.py"
cmp /tmp/opusq2c/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || { echo "base tree device != frozen"; exit 9; }
[ -e /tmp/opusq2c/.MUTANT ] && { echo "base tree carries a sentinel"; exit 9; }
for k in $(seq 0 $((NW - 1))); do
	rm -rf /tmp/opusq2c_w$k
	cp -a /tmp/opusq2c /tmp/opusq2c_w$k
	rm -f /tmp/opusq2c_w$k/regress/d /tmp/opusq2c_w$k/regress/g
done
for k in $(seq 0 $((NW - 1))); do
	python3 -u "$RUN/driver_q2c.py" $k $NW > "$O/driver_w$k.out" 2>&1 &
done
wait
for k in $(seq 0 $((NW - 1))); do
	tail -3 "$O/driver_w$k.out"
	cmp /tmp/opusq2c_w$k/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "w$k device == frozen"
	[ -e /tmp/opusq2c_w$k/.MUTANT ] && echo "w$k SENTINEL PRESENT" || echo "w$k no sentinel"
done
cat "$O"/results_w*.jsonl > "$O/results_all.jsonl"
wc -l "$O/results_all.jsonl"
tar czf "$O/variant_logs_and_diffs.tar.gz" -C /tmp opusq2c_w0/logs opusq2c_w0/diffs opusq2c_w1/logs opusq2c_w1/diffs \
    opusq2c_w2/logs opusq2c_w2/diffs opusq2c_w3/logs opusq2c_w3/diffs
ls -la "$O/variant_logs_and_diffs.tar.gz"
echo RUN_TABLE_DONE
