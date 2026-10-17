#!/bin/bash
#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`; RULINGS_C_records.md F1).
#  Every row runs the launcher against a FAKE codex (CX_CODEX_BIN) that replays a fixture -- nothing here calls the
#  network -- once on the BEFORE launcher (cxlaunch_before.sh = the production copy the farm ran, md5 3c51a757...) and
#  once on the AFTER launcher (tools/cxlaunch.sh), and compares each exit status with the expected one.
#
#    P1 P2 N1-N4      the six Option-C fixtures (adj_20261016/cxctl_optionC/RECEIPT.txt)
#    Q1-Q3            Fable 5.1's boundary fixtures (adj_20261016/fable5/meas_C/cxctl_fable/)
#    A1               an ANSI-coloured REFUSAL (Q3's colouring on P2's text) -- the ANSI strip, refusal side
#    M1               N1's real run (header `model: gpt-6-astra`) asked as another model -- the identity check
#    M2               N2 (an answer, no stderr at all) -- no header: reported UNVERIFIED, not failed
#    D1               P2 refused on Astra, then a Daybreak answer -- the fallback branch answers
#    D2               as D1, but the Daybreak run's header names gpt-6-astra -- the identity check after a fallback
#
#  Usage: bash run_controls.sh   (from anywhere; writes nothing outside a scratch dir it creates and removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
BEFORE="$HERE/cxlaunch_before.sh"
AFTER="$REPO/tools/cxlaunch.sh"
N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
for f in "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout"; do
    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
done
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
ESC=$(printf '\033')

mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr text from stdin)
    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
}
mkfx P1 1 "" "$HERE/fx/P1.stderr"
mkfx P2 1 "" "$HERE/fx/P2.stderr"
mkfx N1 0 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx N2 0 "$HERE/fx/N2.stdout" ""
mkfx N3 0 "" ""
mkfx N4 1 "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err"
mkfx Q1 1 "" "$QD/Q1.stderr"
mkfx Q2 0 "" "$QD/Q2.stderr"
mkfx Q3 1 "" "$QD/Q3.stderr"
sed "s/^ERROR:/${ESC}[1m${ESC}[31mERROR:${ESC}[0m${ESC}[0m/" "$HERE/fx/P2.stderr" | mkfx A1 1 "" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-daybreak-blue-latest\nreasoning effort: ultra\n--------\n' | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" -

#  the fake codex: replays $FX; when the requested model (-m) equals $FX2_MODEL it replays $FX2 instead
cat > "$T/fakecodex.sh" <<'EOF'
#!/bin/bash
D="$FX"; prev=""
for a in "$@"; do
    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
    prev="$a"
done
cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
EOF
chmod +x "$T/fakecodex.sh"
printf 'control brief\n' > "$T/brief.md"

pass=0; total=0
run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit, then env assignments
    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
    local out="$T/out_${row}_${lab}"
    ( export CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL=; for kv in "$@"; do export "$kv"; done
      bash "$sh" "$T/brief.md" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1
    local got=$?
    total=$((total + 1))
    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
    printf '%-3s %-6s exit=%-2s want=%-2s %s\n' "$row" "$lab" "$got" "$want" "$ok"
    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
}
both() {    # $1 row, $2 want-before, $3 want-after, then env
    local row="$1" wb="$2" wa="$3"; shift 3
    run "$row" before "$BEFORE" "$wb" "$@"
    run "$row" after "$AFTER" "$wa" "$@"
}

echo "# cxlaunch landing controls, $(date '+%Y-%m-%d %H:%M:%S')"
echo "# before: $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
echo "# after:  $(md5sum < "$AFTER" | cut -c1-32)  tools/cxlaunch.sh"
both P1 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
both P2 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
both N1 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
both N2 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
both N3 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
both N4 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
both Q1 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
both Q2 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
both Q3 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
both A1 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
both M1 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
both M2 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
both D1 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
both D2 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
#  the M2 note and the D1 keep-the-refused-run behaviour are content, not exit status: check them on the AFTER logs
total=$((total + 1)); if grep -q 'answering model is UNVERIFIED' "$T/log_M2_after.txt"; then pass=$((pass + 1)); echo "M2  after  UNVERIFIED note printed  ok"; else echo "M2  after  UNVERIFIED note MISSING  NO"; fi
total=$((total + 1)); if [ -s "$T/out_D1_after/codex_D1.refused.err" ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; then pass=$((pass + 1)); echo "D1  after  refused run kept, Daybreak credited  ok"; else echo "D1  after  refused-run/credit check  NO"; fi
echo "CONTROLS: $pass/$total as expected"
echo "CXLAND_CONTROLS_DONE"
