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
    check "fbctrl probe exit status" "$fbrc" "0"
    fbres=$(sed -n 's/^FBCTRLP_RESULT=//p' "$FBCLOG")
    #  Pinned UNQUOTED under a one-token stem, so check_score_claims.py sees the pin.
    check "fbctrl_port rows run" "${fbres#*/}" 41
    check "fbctrl_port rows correct" "${fbres%/*}" "41"
    check "fbctrl_port rows failed" "$(grep -c '^  FAIL ' "$FBCLOG")" "0"
    check "fbctrl_port rows emitted" "$(grep -cE '^  (ok|FAIL) ' "$FBCLOG")" "${fbres#*/}"
fi
