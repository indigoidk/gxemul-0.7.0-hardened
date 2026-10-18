
# ---- ppcrldiclzero (#522): X(rldicl) wrote ZERO on every execution -- its 24-row detector -----
# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated twice by owner ruling (2026-09-24 with the
# other nine, then 04f3e7c0 on 2026-10-09) because no block here scored it; this block discharges
# that exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc
# -M 64` needs no image, so a red row is recorded first.  A stalled guest cannot hang the gate: the
# probe's own subprocess backstops (90 s; 60 s for the bogus-machine and 32-bit sessions) turn it
# into failing rows.
# The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores mk48's: its
# completion sentinel, then EVERY row by name, then the emitted/green/red counts and its own SCORE
# line, each pinned to a literal so a shrunk or renamed table cannot pass.  30 checks when green.  Names sit in a %-18s
# column and none is longer than 15, so `^name  ' cannot match a neighbour (the padded-column trap).
RLCLOG=$LOGDIR/ppc_rldicl.log
python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
    note "rldicl: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$RLCLOG" | sed 's/^/       /'
    check "rldicl probe completed" "no" "yes"
else
    check "rldicl probe completed" "yes" "yes"
    for v in "session" "live" "seed holds" "src intact" "disasm xcheck" "zx32 rldicl" "zx32 rldicr" "rot8 rldicl" "rot8 rldicr" "naive fix wrong" "neg apparatus" "bits32 live" "bits32 rld bad" "vacuous cell" "vac neighbour" "census run" "census wrong" "census zero" "disasm total" "cand session" "cr parsed" "sh63 rldicl" "sh32 rldicl" "rc cr0"; do
        check "rldicl row: $v" "$(count "$RLCLOG" "^$v  .*ok$")" "1"
    done
    check "rldicl rows emitted" "$(( $(count "$RLCLOG" " ok$") + $(count "$RLCLOG" " FAIL$") ))" "24"
    check "rldicl rows green"   "$(count "$RLCLOG" " ok$")"   "24"
    check "rldicl rows red"     "$(count "$RLCLOG" " FAIL$")" "0"
    #  EVERY SCORE line is counted, then the one is read: counting only `SCORE 24/24' lines let an
    #  appended contradictory `SCORE 0/24' pass (GPT-6 Astra, pass 1).
    check "rldicl score lines"  "$(grep -c '^SCORE ' "$RLCLOG")" "1"
    check "rldicl score 24/24"  "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
fi
