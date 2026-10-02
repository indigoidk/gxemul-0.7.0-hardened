#!/bin/bash
# waitn.sh N -- block until N RESULT lines exist across both lanes, then print lanes + aug-only rows of every aug log
N="$1"
until [ "$(cat /tmp/gxopuscrimec6_work/lane_A.out /tmp/gxopuscrimec6_work/lane_B.out | grep -c RESULT)" -ge "$N" ]; do sleep 10; done
cat /tmp/gxopuscrimec6_work/lane_*.out
cd /tmp/gxopuscrimec6_work/logs
for f in aug_*.raw; do
    tail -1 "$f" | grep -q CRIMEP_DONE || continue
    echo "== $f"; grep -E "^(latch said|free revP|dg )" "$f" | grep -v ' ok$'
    grep -E '^FAILING:' "$f"
done
