#!/bin/bash
# The differential on every GREEN variant of this pass plus the BASE control, run as a cats caller and as a netwinder
# caller (DEVINIT-faithful reset, guest-reachable 8-byte accesses only), two directories per machine.
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus
GREENS=$(python3 -c "
import json
for l in open('$O/results_all.jsonl'):
    r = json.loads(l)
    if r.get('build') == 'ok' and r.get('rows') == 864 and r.get('fails') == 0:
        print(r['vid'])
")
echo "greens: $(echo $GREENS | wc -w)" > "$O/wit2_all.out"
set -- $GREENS
half=$(( ($# + 1) / 2 ))
A="BASE $(echo $GREENS | cut -d' ' -f1-$half)"
Bl="BASE $(echo $GREENS | cut -d' ' -f$((half + 1))-)"
for m in cats netwinder; do
	WIT2_MACHINE=$m WIT2_ALIGN8=1 MAXL=3 NRAND=2000000 W=/tmp/opusq2f_wit_${m}_a bash "$O/wit2_run_$m.sh" $A > "$O/wit2_all_${m}_a.out" 2>&1 &
	WIT2_MACHINE=$m WIT2_ALIGN8=1 MAXL=3 NRAND=2000000 W=/tmp/opusq2f_wit_${m}_b bash "$O/wit2_run_$m.sh" $Bl > "$O/wit2_all_${m}_b.out" 2>&1 &
done
wait
cat "$O"/wit2_all_*_[ab].out >> "$O/wit2_all.out"
echo "WIT2_ALL_DONE" >> "$O/wit2_all.out"
