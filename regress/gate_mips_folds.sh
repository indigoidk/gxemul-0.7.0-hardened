#!/bin/bash
# GATE 16 -- MIPS instruction-combiner ("fold") witness (#388).
#
# What this protects
# -----------------
# The nine MIPS COMBINE sites install 34 fold-handler variants, and before #388
# NOTHING could witness one firing: most folds are architecturally transparent
# by construction, so any result-asserting row passes whether or not the fold
# fires -- the recorded vacuity mode. #388 added pull-only install/fire counters
# (cpu_mips.h) printed by tlbdump as a prefix-bound MFOLD block. This gate runs
# regress/mips_fold_probe.py, whose rows drive real fold loops free-running
# (never step -- combining gates on !single_step) with a breakpoint AFTER each
# sequence on a NON-ARMING instruction, and grades the counters as EQUALITIES
# derived from the read-ahead rule (a breakpoint anywhere disables read-ahead
# machine-wide, so fire == passes-1; the derivations live in the probe's rows).
#
# Non-vacuity: deleting the bne_samepage_nop replacement sub-arm (incl. its
# install++) in a scratch build flips exactly that fold to (0,0) and reddens
# its two rows while every other row stays green -- measured 2026-08-12
# (M388MUT_PASS), the per-variant attribution -J cannot give.
#
# The BE rows are the first big-endian MIPS guest executions in this harness;
# the mlw2v* value rows additionally witness the _be generated body's BE32
# assembly + sign extension, not just its selection.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 16: MIPS fold witness (#388)"

PMAX=${PMAX:-$ROOT/build/gxemul}
PMAX_KERNEL=$ROOT/gxemul_pmax_rig/bsd

if [ ! -x "$PMAX" ]; then gate_skip "no gxemul binary at $PMAX"; fi
if [ ! -f "$PMAX_KERNEL" ]; then gate_skip "no pmax kernel at $PMAX_KERNEL"; fi

FLOG=$LOGDIR/gate_mips_folds.log
python3 mips_fold_probe.py "$PMAX" "$PMAX_KERNEL" > "$FLOG" 2>&1 || true

if ! grep -q "MFOLDPROBE_RESULT=" "$FLOG"; then
    note "fold probe produced no result line; last lines follow"
    tail -5 "$FLOG" | sed 's/^/       /'
    gate_skip "fold probe did not complete"
fi

grep -E " ok$| FAIL$" "$FLOG" | sed 's/^/       /'

#  Every row named individually (the %-24s column keeps two-space anchoring
#  satisfiable; no name is a prefix of another).
for v in "bne_nop_3max" "bne_nop_tm64" "lui_ori_3max" "mlw2_le_3max" \
         "mlw2_be_tm64" "mlw2v0_be_tm64" "mlw2v1_be_tm64" "mlw2_be_tm32" \
         "memset_3max"; do
    n=$(count "$FLOG" "^$v  *.*ok$")
    check "  fold row: $v" "$n" 1
done

fctrl=$(grep -o "MFOLDPROBE_CONTROL=[A-Z]*" "$FLOG" | tail -1 | cut -d= -f2)
check "fold probe control (parse liveness)" "${fctrl:-missing}" "OK"

fres=$(grep -o "MFOLDPROBE_RESULT=[0-9]*/[0-9]*" "$FLOG" | tail -1 | cut -d= -f2)
check "fold rows correct" "${fres:-missing}" "9/9"

gate_end
