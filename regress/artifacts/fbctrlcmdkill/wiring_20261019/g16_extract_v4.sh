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
         "acc nop cmd" "acc nop x1" "acc nop quiet" "acc set cmd" "acc set ran" "acc set res" "acc set quiet"
         "acc get cmd" "acc get x1" "acc get y1" "acc get quiet" "acc sd get x1" "acc sh get x1"
         "acc edges cmd" "acc edges quiet" "latch get x1" "latch nop cmd" "latch set cmd" "latch set ran"
         "latch once" "rdcmd val" "rdcmd again" "rdcmd noexec" "rdx1 again" "x2 three" "x2 quiet" "x2 sb"
         "x2 sh" "x2 sd" "m3 quiet" "rdw lb" "rdw lh" "rdw ld" "rdw lw" "rdw x1" "two once" "two cmd"
         "wl alive" "wl once" "wl sb get x1" "wl sh get x1" "wl sd get x1" "wl cmd" "wb once" "wb cmd"
         "p1 port" "p1 cmd" "p2 cmd" "p2 port" "free alive" "free once" "sessions clean")
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
    check "fbctrl_cmd rows run" "${fcres#*/}" 123
    check "fbctrl_cmd rows correct" "${fcres%/*}" "123"
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
    check "fbctrl_cmd named rows" "${#FCNAMES[@]}" 123
    for v in "${FCNAMES[@]}"; do
        check "  fbctrl_cmd row: $v" "$(grep -cE "^  ${v} +got=[^ ]* +want=[^ ]* +ok  " "$FCLOG")" "1"
    done
fi
