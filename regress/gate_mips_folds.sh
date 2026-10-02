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
# [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] fire == passes-1 for loop
# folds; memset expects fire=1 and device-bail expects fire=0.  (hbundle_regress32:F14:
# regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
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

#  ---------------------------------------------------------------------------------------
#  #549 fbctrlportkill: dev_fbctrl.c's PORT selector, on -E testmips.  Before #549 the PORT
#  arm STORED the selector as an int with only a warning: 9 made the next DATA access end the
#  emulator in the DATA arm's range check, and a wide value was truncated onto a legal port.
#  #549 refuses any selector >= 8 (the previous one is kept) and announces the refusal once.
#  regress/fbctrl_port_probe.py drives real guest sb/sh/sw/sd/lb/lh/lw/ld on an unmodified
#  testmips -- no kernel, no rig image -- so it runs BEFORE
#  this gate's pmax-kernel check: a missing kernel still skips the fold rows below, and
#  gate_skip reports FAIL, not SKIP, if an fbctrl row failed first.
#
#  THE CONTRACT is the probe's header (its ENUMERATION and NOT CLAIMED).  Variant table 6
#  (regress/artifacts/fbctrlportkill_20260924/table6/TABLE.out) built 297 edits -- table 5's
#  212 (one one-axis edit GENERATED for every cell the header lists, table5/CELLMAP.out), the
#  verifying pass's equivalents and behaviour changers, its three bit-range narrowings of the
#  compare and their control, a one-bit narrowing for EVERY bit 3-63 (60 edits, bit 8's being the
#  control MK_b8_ctl), four one-width
#  narrowings, and three measured disclosures -- each with its prediction written first
#  (table6/MANIFEST.out): the 267 the contract does not disclose are ALL red, HEAD's own arm
#  among them (M_revert, 54/117 here, and sessions K and R ended the process); the 30 it
#  discloses score 117/117 -- a process-global latch, a serial-number condition, three edits of
#  the DATA arm's kept check, two joint cells, one value no row writes, thirteen equivalent
#  edits, two DATA-width edits, three refusal-time cell writes no row reads back, three announce
#  forms keyed to one value, a value range or a value class no first refusal belongs to, and the
#  announce without its trailing newline.  Every RED/GREEN prediction held, as the pre-table
#  addendum named (PRETABLE_ADDENDUM_t6.out): every UNCONDITIONAL one-bit narrowing reddened
#  session B's rows at exactly the widths that carry its bit, and each WIDTH-CONDITIONED
#  narrowing its conditioned width only (MKW_sb05 reds B's byte row alone, though every wider
#  store carries bit 5) -- other sessions' rows red too where their refused value is decisive on
#  that bit alone.  (This said every one-bit AND one-width narrowing reddened exactly the
#  carrying widths -- GPT-6 Astra, confirming #549.)  Two more classes are disclosed after
#  table 6, each measured at the full score: the latch crossed with one bit (NOT CLAIMED (0)) and
#  a refusal that writes a value's only anchor (NOT CLAIMED (3)) --
#  opus549_measured/f2v6/logs/TABLE_f2v6.out.  Session B -- every single-bit value at each width -- is v6's
#  repair of a floor breach the verifying pass MEASURED: the compare narrowed to ignore bits 9-31
#  scored the full 111 rows of v5 and brought back the DATA arm's exit
#  (opus549_measured/c3/TABLE_mask.out).  The device still ends the process through its command
#  and offset defaults, which are filed, not claimed.
#
#  `gatedevicesplit` is OWED (#498): one more device probe in a CPU gate, as #548 added to
#  gate 14.  Recorded, not compounded silently.
FBCLOG=$LOGDIR/fbctrl_port_probe.log
fbrc=0
python3 -u fbctrl_port_probe.py "$PMAX" > "$FBCLOG" 2>&1 || fbrc=$?
if [ "$(grep -cx 'FBCTRLP_DONE' "$FBCLOG")" != "1" ] ||
   [ "$(grep -c '^FBCTRLP_RESULT=' "$FBCLOG")" != "1" ] ||
   ! grep -Eq '^FBCTRLP_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$FBCLOG" ||
   [ "$(grep -c '^FBCTRLP_CONTROL=' "$FBCLOG")" != "1" ] ||
   ! grep -Eq '^FBCTRLP_CONTROL=(OK|FAILED)$' "$FBCLOG"; then
    note "fbctrl probe produced no unique, complete record; last lines follow"
    tail -5 "$FBCLOG" | sed 's/^/       /'
    check "fbctrl probe output parses" "no" "yes"
else
    check "fbctrl probe output parses" "yes" "yes"
    grep -E '^  FAIL ' "$FBCLOG" | sed 's/^/       /'
    check "fbctrl probe controls" "$(sed -n 's/^FBCTRLP_CONTROL=//p' "$FBCLOG")" "OK"
    #  The probe exits nonzero on a crash OR a red row (#549 F2), so this is a second catcher
    #  of a red score, not only of a Python failure.
    check "fbctrl probe exit 0 (nonzero: a crash or a red row)" "$fbrc" "0"
    fbres=$(sed -n 's/^FBCTRLP_RESULT=//p' "$FBCLOG")
    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin.  The
    #  quoted numerator is inert to that tool BY DESIGN -- it reads only the denominator's
    #  line -- and the exit row above and the two reconciliation rows below are what catch a
    #  red or an edited score.
    check "fbctrl_port rows run" "${fbres#*/}" 117
    check "fbctrl_port rows correct" "${fbres%/*}" "117"
    check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
    #  RECONCILE the rows the probe PRINTED with the trailer it printed (#549 F2, measured by
    #  the Opus seat): checking the trailer alone, a log with one row deleted and its
    #  RESULT line intact passed every check above.
    check "fbctrl_port rows emitted match the trailer total" \
          "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"
    check "fbctrl_port ok rows match the trailer count" \
          "$(grep -c '^  ok ' "$FBCLOG")" "${fbres%/*}"
    #  And each row name prints ONCE: a row replaced by a copy of another keeps every count
    #  above intact (the closing pass's grok seat), and only the names can tell.
    check "fbctrl_port row names are unique" \
          "$(grep -E '^  (ok|FAIL) ' "$FBCLOG" | sed -E 's/^  (ok|FAIL) +//; s/ +got=.*//' |
             sort | uniq -d | wc -l)" "0"
fi

if [ ! -f "$PMAX_KERNEL" ]; then gate_skip "no pmax kernel at $PMAX_KERNEL"; fi

FLOG=$LOGDIR/gate_mips_folds.log
python3 mips_fold_probe.py "$PMAX" "$PMAX_KERNEL" > "$FLOG" 2>&1 || true

#  #388 pass-2 (four seats convergent): a probe that STARTED but produced no
#  result line is a failure of the thing under test (crash, dead emulator,
#  unwritable /tmp), not preflight -- it must FAIL, not skip (lib.sh's #371
#  doctrine: skip = could-not-run-at-all; the binary/kernel checks above are
#  the real preflight). A silent skip here would report
#  REGRESS_PASS_WITH_GAPS while removing all fold coverage.
if ! grep -q "MFOLDPROBE_RESULT=" "$FLOG"; then
    note "fold probe produced no result line; last lines follow"
    tail -5 "$FLOG" | sed 's/^/       /'
fi
check "fold probe completed (result line present)" \
      "$(grep -q 'MFOLDPROBE_RESULT=' "$FLOG" && echo yes || echo no)" "yes"

grep -E " ok$| FAIL$" "$FLOG" | sed 's/^/       /'

#  Every row named individually (the %-24s column keeps two-space anchoring
#  satisfiable; no name is a prefix of another).
for v in "bne_nop_3max" "bne_nop_tm64" "lui_ori_3max" \
         "mlw2_le_3max" "mlw2v0_le_3max" "mlw2v1_le_3max" \
         "mlw2_be_tm64" "mlw2v0_be_tm64" "mlw2v1_be_tm64" \
         "mlw2_be_tm32" "mlw2v0_be_tm32" "mlw2v1_be_tm32" \
         "mlw2_dev_tm64" "memset_3max"; do
    n=$(count "$FLOG" "^$v  *.*ok$")
    check "  fold row: $v" "$n" 1
done

fctrl=$(grep -o "MFOLDPROBE_CONTROL=[A-Z]*" "$FLOG" | tail -1 | cut -d= -f2)
check "fold probe control (parse liveness)" "${fctrl:-missing}" "OK"

fres=$(grep -o "MFOLDPROBE_RESULT=[0-9]*/[0-9]*" "$FLOG" | tail -1 | cut -d= -f2)
check "fold rows correct" "${fres:-missing}" "14/14"

gate_end
