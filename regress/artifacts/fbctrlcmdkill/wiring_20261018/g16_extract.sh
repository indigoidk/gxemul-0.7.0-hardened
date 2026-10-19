FCROW='^  [^ ].* got=[^ ]* +want=[^ ]* +'
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
    check "fbctrl_cmd rows run" "${fcres#*/}" 95
    check "fbctrl_cmd rows correct" "${fcres%/*}" "95"
    check "fbctrl_cmd rows failed" "$(grep -cE "${FCROW}FAIL  " "$FCLOG")" "0"
    #  Reconcile the rows printed with the trailer, and require each row name once (#549 F2).
    check "fbctrl_cmd rows emitted match the trailer total" \
          "$(grep -cE "${FCROW}(ok|FAIL)  " "$FCLOG")" "${fcres#*/}"
    check "fbctrl_cmd ok rows match the trailer count" \
          "$(grep -cE "${FCROW}ok  " "$FCLOG")" "${fcres%/*}"
    check "fbctrl_cmd row names are unique" \
          "$(grep -E "${FCROW}(ok|FAIL)  " "$FCLOG" | sed -E 's/^  (.*[^ ]) +got=.*/\1/' |
             sort | uniq -d | wc -l)" "0"
fi
