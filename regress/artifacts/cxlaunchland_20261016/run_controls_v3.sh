#!/bin/bash
#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
#  F1), v3 after the four-seat pass 2 and the adjudication pass.  Every row runs a launcher against a FAKE codex that replays a
#  fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the expected one:
#
#    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
#             landing REPLACES -- driven through $HOME, since it names its codex binary under $HOME and has no override
#    before   cxlaunch_before.sh   = the untracked production copy the farm ran (md5 3c51a757...)
#    after    tools/cxlaunch.sh    = the landed file (or $CXL_AFTER, which the mutant table uses)
#
#  The tracked column is the PRE-FIX state (Fable 5.1's pass-2 C1, via its Opus 4.8 fallback): N1 and N2 are the
#  `cxlaunchquotation' false wall (exit 8 there, 0 after), D1 the missing Daybreak fallback (7 there, 0 after).
#
#    P1 P2 N1-N4   the six Option-C fixtures          Q1-Q3  Fable 5.1's boundary fixtures
#    A1  an ANSI-coloured refusal                     M1  N1's real run asked as another model    M2  an answer, no stderr
#    D1  a refusal, then a Daybreak answer            D2  the same, the Daybreak header naming gpt-6-astra
#    X1  rc 1, empty stdout, ONLY a prefixed quotation of a refusal line (pins the `^ERROR:' anchor)
#    X2  rc 0, an answer with NO verdict line, column-0 wall lines on stderr (pins the empty-STDOUT half of the gate)
#    X5  N1's run asked as gpt-5-astra (pins the WHOLE model name: a suffix-only compare passes it)
#    X6  rc 0, an answer, NO codex header block but a quoted `model: gpt-6-other' line (pins header-block parsing)
#    X8  rc 1, empty, a NUL byte in stderr BEFORE the column-0 wall lines (pins `grep -a': the real 2026-09-19 wall
#        that was recorded exit 6, _scratchpad/cxfarm3_20260919/out/codex_l1_batterypreflight.err -- Grok 4.7, pass 2)
#    X9  rc 0, an answer, NO opening header but a complete QUOTED header block naming gpt-6-astra after line 12 -- it must
#        NOT verify (v2 matched the banner anywhere: N1's own stderr quotes four such blocks, from line 5528; GPT-6 Astra)
#    X10 the same, the quoted block naming gpt-6-other -- it must NOT exit 5
#    E0  every run of every column reached the FAKE: its argument log exists (a launcher that ignores the override would
#        run the REAL CLI -- the tracked file names its binary under $HOME, and a pass-2 seat ran it unmodified once)
#    E1/E2  the EXACT arguments the fake codex received, one per line: exec, --sandbox read-only, --skip-git-repo-check,
#        -m <model>, -c model_reasoning_effort=ultra and the brief -- once for N1, twice (Astra, then Daybreak) for D1
#        (v2 matched a substring, so `ultrax' passed, and it never read the sandbox flag or the brief; Astra, GLM 5.3)
#  NOT pinned, by Fable 5.1's ruling on pass 2 (filed in `cxlaunchunpinned'): `-ne 0' -> `-eq 1' in the classify gate is
#  observable only at an rc outside {0, 1} WITH an answer -- a sibling of the N4 residual (N4 itself is rc 1, where the two
#  forms agree; GLM 5.3), with 0 instances on record; the strip narrowed to SGR (`[0-9;]*m') and wall-before-refusal
#  precedence each need a stderr shape with 0 instances on record (no non-SGR CSI or OSC in 2,372 .err files; no
#  refusal+wall co-occurrence).
#
#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
#  Usage: bash run_controls_v3.sh     ($CXL_AFTER overrides the after launcher; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
TRACKED="$HERE/cxlaunch_tracked.sh"
BEFORE="$HERE/cxlaunch_before.sh"
AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout"; do
    [ -s "$f" ] || { echo "APPARATUS FAIL: missing $f"; exit 9; }
done
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
ESC=$(printf '\033')

mkfx() {    # $1 name, $2 rc, $3 stdout source or "", $4 stderr source or "" (or "-" to read stderr from stdin)
    mkdir -p "$T/fx/$1"; echo "$2" > "$T/fx/$1/rc"
    if [ -n "$3" ]; then cp "$3" "$T/fx/$1/stdout"; else : > "$T/fx/$1/stdout"; fi
    if [ "$4" = "-" ]; then cat > "$T/fx/$1/stderr"; elif [ -n "$4" ]; then cp "$4" "$T/fx/$1/stderr"; else : > "$T/fx/$1/stderr"; fi
}
printf 'A complete review answer.\nVERDICT: SHIP\n' > "$T/ans_verdict.txt"
#  NOT the word "verdict" in any case: the launcher counts it case-insensitively, and a first draft of this fixture said
#  "no verdict line" -- so it HAD one, and the kill table measured X2 blind to the mutant it exists for.
printf 'A complete review answer that ends without its summary line.\n' > "$T/ans_noverdict.txt"
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
sed 's/^/regress\/artifacts\/old_panel\/codex.txt:17:/' "$HERE/fx/P2.stderr" | mkfx X1 1 "" -
mkfx X2 0 "$T/ans_noverdict.txt" "$HERE/fx/P1.stderr"
printf 'streamed source, quoted while the review read a file:\nmodel: gpt-6-other\nreasoning effort: low\n' | mkfx X6 0 "$T/ans_verdict.txt" -
{ printf 'streamed binary from a file the review read: \000\001\002 end\n'; cat "$HERE/fx/P1.stderr"; } | mkfx X8 1 "" -
#  X9/X10: twenty lines of streamed text, then a complete codex header block QUOTED from a file the review read (the shape
#  N1's stderr carries from line 5528) -- and no opening header at all
latehdr() {    # $1 the quoted block's model
    i=1; while [ $i -le 20 ]; do printf 'streamed line %d of a file the review read\n' $i; i=$((i + 1)); done
    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$1"
    printf 'reasoning effort: ultra\n--------\nuser\nthe quoted session brief\n'
}
latehdr gpt-6-astra | mkfx X9 0 "$T/ans_verdict.txt" -
latehdr gpt-6-other | mkfx X10 0 "$T/ans_verdict.txt" -

#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL) and logs its arguments to $FX_ARGS
cat > "$T/fakecodex.sh" <<'EOF'
#!/bin/bash
D="$FX"; prev=""
for a in "$@"; do
    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
    prev="$a"
done
[ -n "${FX_ARGS:-}" ] && { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
EOF
chmod +x "$T/fakecodex.sh"
#  the tracked launcher names $HOME/AppData/Local/Programs/OpenAI/Codex/bin/codex and reads no override, so give it a HOME
mkdir -p "$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
cp "$T/fakecodex.sh" "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
chmod +x "$T/home/AppData/Local/Programs/OpenAI/Codex/bin/codex"
printf 'control brief\n' > "$T/brief.md"

pass=0; total=0
run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit, then env assignments
    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
    local out="$T/out_${row}_${lab}"
    ( export CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
      [ "$lab" = tracked ] && export HOME="$T/home"
      for kv in "$@"; do export "$kv"; done
      bash "$sh" "$T/brief.md" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1
    local got=$?
    total=$((total + 1))
    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
    printf '%-3s %-7s exit=%-2s want=%-2s %s\n' "$row" "$lab" "$got" "$want" "$ok"
    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
}
three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
    run "$row" tracked "$TRACKED" "$wt" "$@"
    run "$row" before "$BEFORE" "$wb" "$@"
    run "$row" after "$AFTER" "$wa" "$@"
}
check() {    # $1 label, $2 0/1 result
    total=$((total + 1))
    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
}

echo "# cxlaunch landing controls (v3), $(date '+%Y-%m-%d %H:%M:%S')"
echo "# tracked: $(md5sum < "$TRACKED" | cut -c1-32)  cxlaunch_tracked.sh"
echo "# before:  $(md5sum < "$BEFORE" | cut -c1-32)  cxlaunch_before.sh"
echo "# after:   $(md5sum < "$AFTER" | cut -c1-32)  $AFTER"
three P1 8 8 8 FX="$T/fx/P1" CX_AUP_MODEL=
three P2 7 7 7 FX="$T/fx/P2" CX_AUP_MODEL=
three N1 8 0 0 FX="$T/fx/N1" CX_AUP_MODEL=
three N2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three N3 6 6 6 FX="$T/fx/N3" CX_AUP_MODEL=
three N4 8 8 8 FX="$T/fx/N4" CX_AUP_MODEL=
three Q1 7 7 7 FX="$T/fx/Q1" CX_AUP_MODEL=
three Q2 8 8 8 FX="$T/fx/Q2" CX_AUP_MODEL=
three Q3 6 6 8 FX="$T/fx/Q3" CX_AUP_MODEL=
three A1 6 6 7 FX="$T/fx/A1" CX_AUP_MODEL=
three M1 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three M2 8 0 0 FX="$T/fx/N2" CX_AUP_MODEL=
three D1 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three D2 7 0 5 FX="$T/fx/P2" FX2="$T/fx/DB_WRONG" FX2_MODEL=gpt-daybreak-blue-latest
three X1 6 6 6 FX="$T/fx/X1" CX_AUP_MODEL=
three X2 8 0 0 FX="$T/fx/X2" CX_AUP_MODEL=
three X5 8 0 5 FX="$T/fx/N1" CX_AUP_MODEL= CX_MODEL=gpt-5-astra
three X6 0 0 0 FX="$T/fx/X6" CX_AUP_MODEL=
three X8 6 6 8 FX="$T/fx/X8" CX_AUP_MODEL=
three X9 0 0 0 FX="$T/fx/X9" CX_AUP_MODEL=
three X10 0 0 0 FX="$T/fx/X10" CX_AUP_MODEL=
#  E0: the fake ran for every row of every column; the run count is pinned, so a deleted row is visible
nruns=$(ls "$T"/log_* 2>/dev/null | wc -l); nargs=$(ls "$T"/args_* 2>/dev/null | wc -l)
miss=""; for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}; [ -s "$T/args_$b" ] || miss="$miss $b"; done
[ "$nruns" = 63 ] && [ "$nargs" = "$nruns" ]; check "E0  all  the fake codex logged $nargs of $nruns runs (21 rows x 3, pinned)${miss:+ -- NOT reached:$miss}" $?
#  content, not exit status -- on the AFTER logs
grep -q 'model UNVERIFIED' "$T/log_M2_after.txt" && ! grep -q 'answered by:' "$T/log_M2_after.txt"; check "M2  after  says model UNVERIFIED and names no model" $?
grep -q 'model UNVERIFIED' "$T/log_X6_after.txt" && ! grep -q 'answered by:' "$T/log_X6_after.txt"; check "X6  after  a quoted model: line is NOT read as the header" $?
[ -s "$T/out_D1_after/codex_D1.refused.err" ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1  after  refused run kept, Daybreak credited" $?
grep -q 'model UNVERIFIED' "$T/log_X9_after.txt" && ! grep -q 'answered by:' "$T/log_X9_after.txt"; check "X9  after  a late QUOTED header block is NOT read as the header" $?
#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
callseq() {    # $1 model -- the sequence one call must receive
    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
}
callseq gpt-6-astra > "$T/want_E1"
{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
echo "CONTROLS: $pass/$total as expected"
echo "CXLAND_CONTROLS_DONE"
[ "$pass" = "$total" ]
