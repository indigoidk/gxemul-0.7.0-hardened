#!/bin/bash
# gate16_replay122.sh <log>... -- gate 16's mips_primundec block (122-row form; verbatim from gate_mips_folds.sh but for the
# two lines marked `replay:`) on recorded logs.  P16 of cloud Fable's pass-2 adjudication: the synthetic logs must red.
check() { if [ "$2" = "$3" ]; then P=$((P+1)); else F=$((F+1)); fi; }
note() { :; }
for REPLAY_LOG in "$@"; do P=0; F=0
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
MPULOG="$REPLAY_LOG"   # replay: the log under test
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
mpurc=$(cat "$REPLAY_LOG.rc" 2>/dev/null || echo 0)   # replay: the launch is replaced by the log and its recorded exit
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
printf '%-34s %3d pass %3d fail  %s\n' "$(basename $REPLAY_LOG)" $P $F "$([ $F = 0 ] && echo GREEN || echo RED)"
done
