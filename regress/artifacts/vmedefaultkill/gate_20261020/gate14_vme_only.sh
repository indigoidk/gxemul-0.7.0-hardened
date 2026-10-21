#!/bin/bash
#  gate14_vme_only.sh -- gate 14's #568 block alone (test-first at gate level).  PMAX and LOGDIR from the env.
set -u
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
. ./lib.sh
gate_begin "gate 14 (#568 vme block only)"
PMAX=${PMAX:?}
need_exec "$PMAX"
note "binary : $PMAX"
#  ------------------------------------------------------------ vmedefaultkill (#568)
#  dev_vme.c's default: ended the emulator (exit(1), announced only by debug() -- silent while
#  free-running) on any VME2 offset the switch did not name.  Now: the 26 header-named registers
#  the model does not implement DECLINE (reads served the preloaded word, writes dropped, one
#  latched fatal() per register); every other unmatched offset returns 0, and memory_rw raises the
#  m88k data-access exception.  The rung-3 witness (regress/artifacts/vmedefaultkill/
#  witness_20261020/, 7 of 7 guest sites rc 1 on 5dbc000e) is NOT run here; this is its detector.
#  Needs only the binary: mvme88k/mvme187 constructs from the PROM, like the mk48/pcc2 blocks above.
VMEDLOG=$LOGDIR/vme_default.log
python3 -u vme_default_probe.py "$PMAX" gate > "$VMEDLOG" 2>&1 || true
if ! grep -q "VME_DEFAULT_PROBE_DONE" "$VMEDLOG"; then
    check "vme default probe completed" "no" "yes"
else
    check "vme default probe completed" "yes" "yes"
    check "vme default controls" "$(grep -c '^VME_DEFAULT_CONTROL=OK$' "$VMEDLOG")" "1"
    for v in "neg apparatus" "session" "live" "vbr reset" "t1cmp rt" "cased census" "free ctl" "free quiet" "free neg ctl" "tctl rt" "vbr rt" "t1count inc" "cased wr" "p2 rd census" "p2 wr census" "p2 ld widths" "p2 st widths" "p2 ann rd" "p2 ann rd 2" "p2 ann wr" "p2 ann wr 2" "p2 nw rd" "p2 nw wr" "p1 fault lo" "p1 fault hi" "p1 fault mid" "p1 fault wr" "p1 p2 edge" "p3 interim" "p2 int byte" "p2 int half" "p1 census" "p1 widths" "unasm"; do
        check "vme default row: $v" "$(count "$VMEDLOG" "^$v  .*ok$")" "1"
    done
    check "vme default rows emitted" "$(( $(count "$VMEDLOG" " ok$") + $(count "$VMEDLOG" " FAIL$") ))" "34"
    check "vme default rows green"   "$(count "$VMEDLOG" " ok$")"   "34"
    check "vme default rows red"     "$(count "$VMEDLOG" " FAIL$")" "0"
fi

gate_end
