#!/bin/bash
# Write PREDICTIONS.txt (all 50 shapes) BEFORE any 3e mutant build.  My 39 q2g shapes keep their 3d prediction
# EXCEPT IAS01, which I predict FLIPS green(3d)->RED(3e): it sets irq_asserted on a declined IRQ_STATUS write, and
# 3e's ZKEPT after each ZDECLINE access catches it on the DEVINIT declines rows (irq_asserted starts 0 there).
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/opus
cd "$O"
{
  echo "PREDICTIONS q2h (#545 3e pass), written $(date '+%Y-%m-%d %H:%M:%S %Z') BEFORE any 3e-instrument build."
  echo "Columns: vid  pred_on_3d  pred_on_3e  text"
  echo "My 39 q2g shapes (pred_on_3d from PREDICTIONS_q2g.txt/.b, unchanged on 3e EXCEPT IAS01):"
  python3 - <<'PY'
import gen_shapes, gen_shapes_b
def pr(v, p3d, p3e):
    print("  %-8s %-10s %-10s %s" % (v["vid"], p3d, p3e, v["text"]))
for v in gen_shapes.variants():
    p = v["pred"]
    p3e = "RED" if v["vid"] == "IAS01" else p   # IAS01 flips: 3e ZKEPT catches irq_asserted on DEVINIT declines rows
    pr(v, p, p3e)
for v in gen_shapes_b.variants():
    pr(v, v["pred"], v["pred"])
PY
  echo "My 11 NEW q2h edge shapes (aimed at 3e's two closures):"
  python3 - <<'PY'
import gen_q2
for v in gen_q2.variants():
    print("  %-8s %-10s %-10s %s" % (v["vid"], "(new)", v["pred"], v["text"]))
PY
  echo "PRED_DONE"
} > "$O/PREDICTIONS.txt" 2>&1
cat "$O/PREDICTIONS.txt"
