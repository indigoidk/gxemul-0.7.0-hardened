#  ---- gate_arm.sh: wiring for #499's detector.  NOT APPLIED -- gate_arm.sh is
#  ---- the coordinator's file.  Modelled on the sgi_re_width_probe block at :1131.
UNMLOG=$LOGDIR/sgi_re_unmapped.log
python3 sgi_re_unmapped_probe.py "$PMAX" gate > "$UNMLOG" 2>&1 || true

#  SENTINEL FIRST.  A preserved log is verified by its completion sentinel, never by its
#  existence: a killed run loses every row and looks exactly like a run that produced none.
if ! grep -q "OPUS499T_DONE" "$UNMLOG"; then
    check "sgi_re unmapped probe completed" "no" "yes"
else
    check "sgi_re unmapped probe completed" "yes" "yes"
    check "sgi_re unmapped controls" "$(count "$UNMLOG" '^OPUS499T_CONTROL=OK$')" "1"
    for v in "live" "devsig" "wr surv" "wr kill" "wr decl" "rd surv" "rd kill" "rd decl" "rd sent" "rd nodbe" "wr lat1" "rd lat1" "wr rd 2msg" "xwin7 pre" "xwin wr" "xwin rd" "tlba acc lo" "tlba acc hi" "tlbb acc lo" "tlbb acc hi" "tlbc acc lo" "tlbc acc hi" "tex acc lo" "tex acc hi" "lina acc lo" "lina acc hi" "linb acc lo" "linb acc hi"; do
        check "sgi_re unmapped row: $v" "$(count "$UNMLOG" "^$v  .*ok$")" "1"
    done

    #  DENOMINATOR, SUMMED ARITHMETICALLY -- two rows, not one: a single "28 ok" check
    #  cannot tell a LOST row from a FAILING one, and those need different responses.
    check "sgi_re unmapped rows emitted" \
          "$(( $(count "$UNMLOG" " ok$") + $(count "$UNMLOG" " FAIL$") ))" "28"
    check "sgi_re unmapped rows green" "$(count "$UNMLOG" " ok$")"   "28"
    check "sgi_re unmapped rows red"   "$(count "$UNMLOG" " FAIL$")" "0"
fi
