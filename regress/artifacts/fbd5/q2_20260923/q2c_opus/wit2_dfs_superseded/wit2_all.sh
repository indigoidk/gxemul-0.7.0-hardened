#!/bin/bash
# The differential on every GREEN variant of the table (58 new + 57 of the 434), plus the BASE negative control,
# in four independent directories.
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus
GREENS=$(python3 -c "
import json
for l in open('$O/results_all.jsonl'):
    r = json.loads(l)
    if r.get('build') == 'ok' and r.get('rows') == 707 and r.get('fails') == 0:
        print(r['vid'])
")
echo "greens: $(echo $GREENS | wc -w)" > "$O/wit2_all.out"
i=0
for k in 0 1 2 3; do : > /tmp/opusq2c_witlist$k; done
for v in $GREENS; do echo "$v" >> /tmp/opusq2c_witlist$((i % 4)); i=$((i + 1)); done
for k in 0 1 2 3; do
	MAXL=3 NRAND=2000000 W=/tmp/opusq2c_wit$k bash "$O/wit2_run.sh" $(cat /tmp/opusq2c_witlist$k) > "$O/wit2_all_$k.out" 2>&1 &
done
wait
cat "$O"/wit2_all_[0-3].out >> "$O/wit2_all.out"
echo "WIT2_ALL_DONE" >> "$O/wit2_all.out"
