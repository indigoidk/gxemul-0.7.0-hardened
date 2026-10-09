
#  #562 armmsrmodekill.  A privileged guest MSR naming a mode this model does not bank (MSR CPSR_c,#0x14 =
#  0xE321F014), or an SPSR restore (MOVS pc,lr; LDM {..pc}^) whose SPSR names one -- including an SPSR never written,
#  which is zero -- reached arm_load_register_bank()'s default: and ended the emulator.  msr_imm and both restores now
#  decline the MODE FIELD only, announced once per site per CPU, and Save/Load's default: arms are latched backstops.
#  The probe's CONTRACT, its generated grid and its NOT CLAIMED list are in its header; the kill tables and the
#  review chain's measurements are in regress/artifacts/armmsrmodekill/.  Rows do not end in their status token
#  (a note follows it), so failed rows are read from ARMMSRMODE_REDS, never grepped.
MSRLOG=$LOGDIR/gate_arm_msrmode.log
mrc=0
python3 -u arm_msrmode_probe.py "$PMAX" gate > "$MSRLOG" 2>&1 || mrc=$?

#  PARSE BEFORE SCORE: exactly one valid record of each kind.
if [ "$(grep -c '^ARMMSRMODE_RESULT=' "$MSRLOG")" != "1" ] ||
   ! grep -Eq '^ARMMSRMODE_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$MSRLOG" ||
   [ "$(grep -c '^ARMMSRMODE_CONTROL=' "$MSRLOG")" != "1" ] ||
   ! grep -Eq '^ARMMSRMODE_CONTROL=(OK|DEAD)$' "$MSRLOG" ||
   [ "$(grep -c '^ARMMSRMODE_REDS=' "$MSRLOG")" != "1" ] ||
   [ "$(grep -cx 'ARMMSRMODE_DONE' "$MSRLOG")" != "1" ]; then
    note "msrmode probe produced no unique, valid completion record; last lines follow"
    tail -5 "$MSRLOG" | sed 's/^/       /'
    check "msrmode probe output parses" "no" "yes"
else
    check "msrmode probe output parses" "yes" "yes"
    grep -E ' want=' "$MSRLOG" | grep -E ' FAIL ' | sed 's/^/       /'
    check "msrmode controls" "$(sed -n 's/^ARMMSRMODE_CONTROL=//p' "$MSRLOG")" "OK"
    check "msrmode probe exit status" "$mrc" "0"
    mres=$(sed -n 's/^ARMMSRMODE_RESULT=//p' "$MSRLOG")
    #  Pinned by hand to a LITERAL, UNQUOTED, under the ONE-TOKEN stem arm_msrmode (check_score_claims.py's PIN regex
    #  takes one whitespace-free token before `rows run'; the stem also puts the probe's docstring under that scan).
    #  MEASURED: <OWED the committed probe's base leg, named, run BEFORE this pin was written>.
    check "arm_msrmode rows run"     "${mres#*/}" 47
    check "arm_msrmode rows correct" "${mres%/*}" "47"
    check "arm_msrmode rows emitted" "$(grep -cE '^  [^ ].* got=.* want=' "$MSRLOG")" "47"
    check "arm_msrmode reds"         "$(sed -n 's/^ARMMSRMODE_REDS=//p' "$MSRLOG")" "none"
fi

