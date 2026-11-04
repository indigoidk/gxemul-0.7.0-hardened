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

#  ---------------------------------------------------------------------------------------
#  #567 fbctrlcmdkill: the same device's COMMAND port.  Before #567 a DATA write at COMMAND of any
#  command but NOP (0), SET_RESOLUTION (1) and GET_RESOLUTION (2) -- FILL and COPY among them --
#  reached fbctrl_command()'s default: and ended the emulator, and a wide value was stored into the
#  int cell as its low word, so 0x100000001 ran SET_RESOLUTION.  #567 refuses every other 64-bit
#  value before the store (COMMAND keeps its value, nothing runs) and announces once per device.
#  regress/fbctrl_cmd_probe.py drives real guest sb/sh/sw/sd and lb/lh/lw/ld on an unmodified
#  testmips, like the #549 probe above, so it too runs before the pmax-kernel check.  THE CONTRACT is
#  its header: it holds the bound's edges and the latch at every access WIDTH (the class two review
#  passes found open), and its NOT CLAIMED (7) names the width x latch cells pass 3 found reached but
#  not observed (filed as `fbctrlobsgrid`).  Kill table 4 (regress/artifacts/fbctrlcmdkill/
#  killtable4_20261019/) re-ran all 44 mutants built for this round on v4's 123 rows -- every one
#  red, the twelve built last having escaped the 106-row v3.  Pass 3 added two rows (`edge x1',
#  `edge y1'); the 125 rows score 125 on the fix, 51 on HEAD's build, and 17 on a binary that runs
#  nothing -- absence rows read green there and the record still parses, so this block requires CONTROL=OK, pins the
#  score by EQUALITY, and checks EVERY row by name (pass 2: a row swapped for an unrelated unique
#  green one keeps every count).
#  `gatedevicesplit` (#498) grows by this second device probe in a CPU gate.  That is debt, not a
#  fit: pass 2 asked that it not be called fine (Grok 4.7), and the STOP is recorded on that row --
#  a third device probe lands here only with the split or with a pin on this gate's launch count
#  (GLM 5.3).  Like #549's, the launch below has no timeout: a wedged probe hangs the gate, which is
#  visible and not a false pass (filed for both blocks as `gate16fence`).
#  The probe prints a row's status AFTER got/want, unlike the #549 probe, so every row count below
#  uses one anchored pattern, FCROW.  The v4 block (123 names), replayed on kill table 4's 48 logs,
#  was green only on the fix (wiring_20261019/GATE16_REPLAY_v4.out); this one adds the two names and
#  moves the pins, and was run in situ on both builds (wiring_20261019/INSITU.md).
FCLOG=$LOGDIR/fbctrl_cmd_probe.log
FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
FCNAMES=("live" "devsig" "ref 3 alive" "ref 3 cmd" "ref 3 x1" "ref 3 y1" "ref 3 once" "ref 3 noset"
         "ref 4 alive" "ref 4 cmd" "ref 4 x1" "ref 4 y1" "ref 4 once" "ref 4 noset" "ref sb3 alive"
         "ref sb3 cmd" "ref sb3 x1" "ref sb3 y1" "ref sb3 once" "ref sb3 noset" "ref sh4 alive" "ref sh4 cmd"
         "ref sh4 x1" "ref sh4 y1" "ref sh4 once" "ref sh4 noset" "ref 5 alive" "ref 5 cmd" "ref 5 x1"
         "ref 5 y1" "ref 5 once" "ref 5 noset" "ref m1w alive" "ref m1w cmd" "ref m1w x1" "ref m1w y1"
         "ref m1w once" "ref m1w noset" "ref w3 alive" "ref w3 cmd" "ref w3 x1" "ref w3 y1" "ref w3 once"
         "ref w3 noset" "ref w0 alive" "ref w0 cmd" "ref w0 x1" "ref w0 y1" "ref w0 once" "ref w0 noset"
         "ref w1 alive" "ref w1 cmd" "ref w1 x1" "ref w1 y1" "ref w1 once" "ref w1 noset" "ref w2 alive"
         "ref w2 cmd" "ref w2 x1" "ref w2 y1" "ref w2 once" "ref w2 noset" "ref m1d alive" "ref m1d cmd"
         "ref m1d x1" "ref m1d y1" "ref m1d once" "ref m1d noset" "edge alive" "edge cmd" "edge once"
         "edge x1" "edge y1" "acc nop cmd" "acc nop x1" "acc nop quiet" "acc set cmd" "acc set ran"
         "acc set res" "acc set quiet" "acc get cmd" "acc get x1" "acc get y1" "acc get quiet" "acc sd get x1"
         "acc sh get x1" "acc edges cmd" "acc edges quiet" "latch get x1" "latch nop cmd" "latch set cmd"
         "latch set ran" "latch once" "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three"
         "x2 quiet" "x2 sb" "x2 sh" "x2 sd" "m3 quiet" "rdw lb" "rdw lh" "rdw ld" "rdw lw" "rdw x1" "two once"
         "two cmd" "wl alive" "wl once" "wl sb get x1" "wl sh get x1" "wl sd get x1" "wl cmd" "wb once"
         "wb cmd" "p1 port" "p1 cmd" "p2 cmd" "p2 port" "free alive" "free once" "sessions clean")
fcrc=0
python3 -u fbctrl_cmd_probe.py "$PMAX" > "$FCLOG" 2>&1 || fcrc=$?
if [ "$(grep -cx 'FBCMD_DONE' "$FCLOG")" != "1" ] ||
   [ "$(grep -c '^FBCMD_RESULT=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$FCLOG" ||
   [ "$(grep -c '^FBCMD_CONTROL=' "$FCLOG")" != "1" ] ||
   ! grep -Eq '^FBCMD_CONTROL=(OK|FAILED)$' "$FCLOG"; then
    note "fbctrl command probe produced no unique, complete record; last lines follow"
    tail -5 "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe output parses" "no" "yes"
else
    check "fbctrl command probe output parses" "yes" "yes"
    grep -E "${FCROW}FAIL  " "$FCLOG" | sed 's/^/       /'
    check "fbctrl command probe controls" "$(sed -n 's/^FBCMD_CONTROL=//p' "$FCLOG")" "OK"
    #  As for #549: the probe exits nonzero on a crash OR a red row, a second catcher of a red score.
    check "fbctrl command probe exit 0 (nonzero: a crash or a red row)" "$fcrc" "0"
    fcres=$(sed -n 's/^FBCMD_RESULT=//p' "$FCLOG")
    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin (as #549's).
    check "fbctrl_cmd rows run" "${fcres#*/}" 125
    check "fbctrl_cmd rows correct" "${fcres%/*}" "125"
    check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
    #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
    check "fbctrl_cmd rows emitted match the trailer total" \
          "$(grep -cE "${FCROW}(ok|FAIL)  " "$FCLOG")" "${fcres#*/}"
    check "fbctrl_cmd ok rows match the trailer count" \
          "$(grep -cE "${FCROW}ok  " "$FCLOG")" "${fcres%/*}"
    check "fbctrl_cmd row names are unique" \
          "$(grep -E "${FCROW}(ok|FAIL)  " "$FCLOG" | sed -E 's/^  (.*[^ ]) +got=.*/\1/' |
             sort | uniq -d | wc -l)" "0"
    #  And EVERY expected row by NAME, green exactly once: counts and uniqueness cannot tell an expected
    #  row from an unrelated unique one put in its place (pass 2, GPT-6 Astra).
    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 125
    for v in "${FCNAMES[@]}"; do
        check "  fbctrl_cmd row: $v" "$(grep -cE "^  ${v} +got=[^ ]* +want=[^ ]* +ok  " "$FCLOG")" "1"
    done
fi

#  #580 mipsprimundec: the MIPS translator's unassigned primary opcodes (0x1d JALX, 0x1e MDMX, LWC2/SWC2, LDC2/SDC2,
#  LWC3/SWC3) stopped the emulated CPU ("UNIMPLEMENTED instruction") before #580.  regress/mips_primundec_probe.py places
#  each word with real guest execution on an unmodified -E testmips (R4400, R3000, R5000, 24KEc, 5KE) and asserts the EXACT
#  ExcCode/CE, EPC and PC per CPU and word, plus a jalx and an lwc2 in a branch delay slot, and one R5900 row (0x1e not
#  a Reserved Instruction; cloud Fable's D31 ruling).  The 121-row probe: pre-fix 28/121, fix 121/121
#  (artifacts/mipsprimundec/detector_20261104/).  The 122-row probe: pre-fix 29/122, fix 122/122
#  (artifacts/mipsprimundec/killtable_20261104/d31_20261104/), the test-variant table beside it.
#  This is a CPU-translator probe, the subject of this gate -- not a third device probe in the sense of `gatedevicesplit`.
#  As in the blocks above: CONTROL=OK and SYMPTOM=ABSENT required, the score pinned by EQUALITY, EVERY row checked by name
#  (the names are literals copied from the fixed build's run).  The probe's exit status is 0 unless it crashes; red rows
#  show in RESULT and the rows.  This gate launches "$PMAX", the generic gxemul build, not a per-CPU binary.  The
#  probe has no outer timeout; the worst case is about 38 sessions x 60 s, so a hung probe shows as a roughly
#  38-minute run, not as a failure.  Two checks below cannot fail on a run, on purpose: `named rows == 122` compares a
#  static literal (an edit tripwire for the name table), and the yes/yes twin in the else branch is the green twin of
#  the parse check (it records that the output parsed).
MPULOG=$LOGDIR/mips_primundec_probe.log
MPUNAMES=("neg apparatus" "64 live v0" "64 live pc" "64 live epc" "64 cpu2 exc" "64 cpu2 epc" "64 cpu2 pc"
          "64 jalx stop" "64 jalx exc" "64 jalx epc" "64 jalx pc" "64 mdmx stop" "64 mdmx exc" "64 mdmx epc"
          "64 mdmx pc" "64 lwc2 stop" "64 lwc2 exc" "64 lwc2 epc" "64 lwc2 pc" "64 lwc3 stop" "64 lwc3 exc"
          "64 lwc3 epc" "64 lwc3 pc" "64 ldc2 stop" "64 ldc2 exc" "64 ldc2 epc" "64 ldc2 pc" "64 swc2 stop"
          "64 swc2 exc" "64 swc2 epc" "64 swc2 pc" "64 swc3 stop" "64 swc3 exc" "64 swc3 epc" "64 swc3 pc"
          "64 sdc2 stop" "64 sdc2 exc" "64 sdc2 epc" "64 sdc2 pc" "32 live v0" "32 live pc" "32 live epc"
          "32 cpu2 exc" "32 cpu2 epc" "32 cpu2 pc" "32 ri exc" "32 ri epc" "32 ri pc" "32 jalx stop" "32 jalx exc"
          "32 jalx epc" "32 jalx pc" "32 mdmx stop" "32 mdmx exc" "32 mdmx epc" "32 mdmx pc" "32 lwc2 stop"
          "32 lwc2 exc" "32 lwc2 epc" "32 lwc2 pc" "32 lwc3 stop" "32 lwc3 exc" "32 lwc3 epc" "32 lwc3 pc"
          "32 ldc2 stop" "32 ldc2 exc" "32 ldc2 epc" "32 ldc2 pc" "32 swc2 stop" "32 swc2 exc" "32 swc2 epc"
          "32 swc2 pc" "32 swc3 stop" "32 swc3 exc" "32 swc3 epc" "32 swc3 pc" "32 sdc2 stop" "32 sdc2 exc"
          "32 sdc2 epc" "32 sdc2 pc" "r5k live pc" "r5k lwc3 exc" "r5k lwc3 epc" "r5k lwc3 pc" "r5k swc3 exc"
          "r5k swc3 epc" "r5k swc3 pc" "24k live pc" "24k lwc2 exc" "24k lwc2 epc" "24k lwc2 pc" "24k swc2 exc"
          "24k swc2 epc" "24k swc2 pc" "24k ldc2 exc" "24k ldc2 epc" "24k ldc2 pc" "24k sdc2 exc" "24k sdc2 epc"
          "24k sdc2 pc" "24k lwc3 exc" "24k lwc3 epc" "24k lwc3 pc" "24k swc3 exc" "24k swc3 epc" "24k swc3 pc"
          "5ke live pc" "5ke lwc3 exc" "5ke lwc3 epc" "5ke lwc3 pc" "5ke swc3 exc" "5ke swc3 epc" "5ke swc3 pc"
          "r59 mdmx notRI"
          "64 ds exc" "64 ds bd" "64 ds epc" "64 ds pc" "64 dsc exc" "64 dsc bd" "64 dsc epc" "64 dsc pc")
mpurc=0
python3 -u mips_primundec_probe.py "$PMAX" gate "$LOGDIR/mips_primundec" > "$MPULOG" 2>&1 || mpurc=$?
if [ "$(grep -cx 'MIPS_PRIMUNDEC_PROBE_DONE' "$MPULOG")" != "1" ] ||
   [ "$(grep -c '^MIPS_PRIMUNDEC_RESULT=' "$MPULOG")" != "1" ]; then
    note "mips_primundec probe produced no unique, complete record; last lines follow"
    tail -5 "$MPULOG" | sed 's/^/       /'
    check "mips_primundec probe output parses" "no" "yes"
else
    check "mips_primundec probe output parses" "yes" "yes"
    check "mips_primundec sentinel is the last line" "$(tail -n 1 "$MPULOG")" "MIPS_PRIMUNDEC_PROBE_DONE"
    check "mips_primundec probe exit 0 (nonzero: a crash)" "$mpurc" "0"
    check "mips_primundec controls" "$(sed -n 's/^MIPS_PRIMUNDEC_CONTROL=//p' "$MPULOG")" "OK"
    check "mips_primundec symptom absent" "$(sed -n 's/^MIPS_PRIMUNDEC_SYMPTOM=//p' "$MPULOG")" "ABSENT"
    check "mips_primundec rows correct" "$(sed -n 's/^MIPS_PRIMUNDEC_RESULT=//p' "$MPULOG")" "122/122"
    check "mips_primundec named rows" "${#MPUNAMES[@]}" 122
    for v in "${MPUNAMES[@]}"; do
        check "  mips_primundec row: $v" "$(grep -cE "^${v}  +[^ ]+ +[^ ]+ .* ok$" "$MPULOG")" "1"
    done
    #  the denominator, pinned UNQUOTED in the form check_score_claims reads (`<stem> rows run`), as #578 and #579 do
    mpuok=$(grep -c " ok$" "$MPULOG"); mpubad=$(grep -c " FAIL$" "$MPULOG"); mpurun=$((mpuok + mpubad))
    check "mips_primundec rows run"   "$mpurun" 122
    check "mips_primundec rows green" "$mpuok" 122
    check "mips_primundec rows red"   "$mpubad" 0
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
