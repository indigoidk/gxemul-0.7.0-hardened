

#  ------------------------------------------------------------ mk48nvramkill (#521) + #536
#  Eight of the nine MK48T08 clock-block offsets ended the emulator through default: (#521).  Its
#  57-row detector shipped EXEMPT (21e7560, 2026-09-10) because "no gate drives mvme88k/mvme187" --
#  false when it was written: this file had run pcc2_width_probe.py on mvme187 since b78bb0f
#  (2026-09-03).  #536 (wiringcliff, owner ruling 2026-09-18) wires it.
MK48LOG=$LOGDIR/mk48_nvram.log
python3 -u mk48_nvram_probe.py "$PMAX" gate > "$MK48LOG" 2>&1 || true
if ! grep -q "MK48_WITNESS_DONE" "$MK48LOG"; then
    check "mk48 nvram probe completed" "no" "yes"
else
    check "mk48 nvram probe completed" "yes" "yes"
    for v in "live" "nvram0" "neg apparatus" "devsig yr" "devsig mon" "devsig mday" "devsig wday" "shape" "ok rd 1fef" "ok wr 1fef" "ok rd 1ff8" "ok wr 1ff8" "ok rd 1ff9" "ok wr 1ff9" "csr rise" "rt 1fef" "rt 1ff0" "rt 1ff1" "rt 1ff2" "rt 1ff3" "rt 1ff4" "rt 1ff5" "rt 1ff6" "rt 1ff7" "rd 1ff0" "rd 1ff0 obs" "rd 1ff1" "rd 1ff1 obs" "rd 1ff2" "rd 1ff2 obs" "rd 1ff3" "rd 1ff3 obs" "rd 1ff4" "rd 1ff4 obs" "rd 1ff5" "rd 1ff5 obs" "rd 1ff6" "rd 1ff6 obs" "rd 1ff7" "rd 1ff7 obs" "wr 1ff0" "wr 1ff0 obs" "wr 1ff1" "wr 1ff1 obs" "wr 1ff2" "wr 1ff2 obs" "wr 1ff3" "wr 1ff3 obs" "wr 1ff4" "wr 1ff4 obs" "wr 1ff5" "wr 1ff5 obs" "wr 1ff6" "wr 1ff6 obs" "wr 1ff7" "wr 1ff7 obs" "msg silent"; do
        check "mk48 nvram row: $v" "$(count "$MK48LOG" "^$v  .*ok$")" "1"
    done
    check "mk48 nvram rows emitted" "$(( $(count "$MK48LOG" " ok$") + $(count "$MK48LOG" " FAIL$") ))" "57"
    check "mk48 nvram rows green"   "$(count "$MK48LOG" " ok$")"   "57"
    check "mk48 nvram rows red"     "$(count "$MK48LOG" " FAIL$")" "0"
fi


#  ------------------------------------------------------------ hpcmipsctor (#444) + #536
#  Three of eight advertised hpcmips subtypes SIGABRTed during construction (#444).  Its rung-2
#  detector (~8 s, no rig image) shipped EXEMPT for want of a construction gate; #536 wires it here.
#  It ends by printing HPCMIPS_CTOR_RESULT=<ok>/<rows> and then its verdict, HPCMIPS_CTOR_PASS / _FAIL; the
#  RESULT line is the completion sentinel, so a run killed before its tally reds the first check.
#  C2 gets its unrelated-abort control from a LIVE, UNRELATED defect: mvme1600's construction aborts in
#  bus_pci_add() ("pci_data == NULL!"), and the row checks only the abort CLASS.  A round that fixes that
#  machine turns C2 red and owes its re-derivation -- the probe's own row F3 covers the classifier with a
#  synthetic abort.  Filed as `hpcmipsc2`.
HPCLOG=$LOGDIR/hpcmips_ctor.log
python3 -u hpcmips_ctor_probe.py --binary "$PMAX" > "$HPCLOG" 2>&1 || true
if ! grep -q "^HPCMIPS_CTOR_RESULT=" "$HPCLOG"; then
    check "hpcmips ctor probe completed" "no" "yes"
else
    check "hpcmips ctor probe completed" "yes" "yes"
    for v in P1 P2 P3 F1 F2 F3 F4 F5 E1 A1 A2 A3 A4 A5 B1 C1 C2 C3 C4 C5 S0 S1 S4 S5 S2 S3 R1 I1; do
        check "hpcmips ctor row: $v" "$(grep -c "^  \[ok\] $v " "$HPCLOG")" "1"
    done
    check "hpcmips ctor rows green" "$(grep -c '^  \[ok\] ' "$HPCLOG")"   "28"
    check "hpcmips ctor rows red"   "$(grep -c '^  \[FAIL\] ' "$HPCLOG")" "0"
    check "hpcmips ctor verdict"    "$(grep -c '^HPCMIPS_CTOR_PASS$' "$HPCLOG")" "1"
fi
