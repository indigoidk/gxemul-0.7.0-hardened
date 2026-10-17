#!/bin/bash
#  Controls for the tools/cxlaunch.sh landing of 2026-10-16 (ledger `cxlaunchquotation`, `cxlaunchdaybreak`; RULINGS_C_records.md
#  F1), v5 after the four-seat pass 2, the adjudication pass, the v3 pass and the v4 pass.  Every row runs a launcher against a FAKE
#  codex that replays a fixture -- nothing here calls the network -- on THREE launchers, and compares each exit status with the
#  expected one:
#
#    tracked  cxlaunch_tracked.sh  = `git show HEAD:tools/cxlaunch.sh` before the landing (md5 cb180d9d...), the file the
#             landing REPLACES -- it names its codex binary under $HOME and has no override
#    before   cxlaunch_before.sh   = the untracked production copy the farm ran (md5 3c51a757...)
#    after    tools/cxlaunch.sh    = the landed file (or $CXL_AFTER, which the mutant table uses)
#
#  The tracked column is the PRE-FIX state (Fable 5.1's pass-2 C1, via its Opus 4.8 fallback): N1 and N2 are the
#  `cxlaunchquotation' false wall (exit 8 there, 0 after), D1 the missing Daybreak fallback (7 there, 0 after).  The tracked and
#  before expectations RECORD what the two old files do; only the after column is a claim.  Those of the rows v5 added were
#  recorded from a calibration run of this file (RECEIPT_v5_calibration.txt); every after expectation was written before it.
#
#  v5 -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3) measured one-edit mutants passing all 116 v4 controls at
#  decisions the v4 CONTRACT did not list -- codex's own rc passed through, the fallback's second and third conjuncts, the
#  header's ANSI strip, the stdin redirect, the output names, the pattern alternatives, the two `-eq 0` body tests, the default
#  codex path.  The v4 CONTRACT was derived from the three passes' FINDINGS, not from the file (Fable 5.1).  v5's is derived from
#  the file: every predicate, conjunct, pattern alternative, redirection, constant, exit-cascade order and caller-read log
#  phrase, each asked "which row goes red if this changes".  Every launcher run is under `timeout 120' (a looping mutant exits
#  124 and reds; an honest run takes about 0.6 s -- Fable 5.1, v4 pass) and is fed a MARKER file on stdin; HOME is a scratch
#  dir holding a second fake at the launcher's default codex path, which marks the runs that reach it.
#
#  THE CONTRACT -- each decision of the landed launcher (by construct), the rows that pin its edges, and what is not pinned:
#  configuration
#    CX_CODEX_BIN honoured, its `:-'      E0b (no after run but DP's and EO's reaches the default-path fake); EO (set EMPTY)
#    the default codex path               DP (CX_CODEX_BIN unset: the run reaches $HOME/AppData/Local/Programs/.../codex)
#    CX_MODEL, CX_EFFORT, CX_AUP_EFFORT, their `:-' and defaults
#                                         E1, E2 (the whole argument sequence); EO (each set EMPTY -> its default)
#    CX_AUP_MODEL, its default and `-' (EMPTY disables the fallback)
#                                         E2; FD (every row that sets it empty makes exactly one call)
#    the output names and the stdout/stderr redirections, `mkdir -p "$OUT"'
#                                         N1F (codex_N1.txt and .err byte-for-byte the fixture's, nothing else written)
#    `< /dev/null' on codex's stdin       SI (no after run's codex reads the marker the launcher is fed)
#    `cd "$PROJ"'                         CWD (every after run's codex starts in the project root)
#    the argv cap `sz -gt 30000', exit 9  X14 (30,000 accepted) / X15 (30,001: exit 9, codex never called)
#  the call
#    the argument sequence                E1 (one call), E2 and EO (Astra, then Daybreak), DP -- each compared whole
#  the opening header
#    ANSI strip on the header             CH (the real coloured header of fx/R2.stderr, asked as gpt-6-other -> 5)
#    the window `NR > 12 && h < 2'        W12 / W13 (first rule at line 12 read, at 13 not); X13 (the real banner-at-4 header);
#                                         X9, X10 (no opening block, a quoted one at line 21)
#    the banner: `h == 0 &&', `/^OpenAI Codex/'
#                                         HB (a banner-shaped line inside the block does not restart it); BA (a banner with a
#                                         prefix, above the real one, is not a banner); every header row (the text)
#    the first rule: `h == 1 &&', 8 dashes, `next'
#                                         BA (a rule before any banner is not the first rule); R7A (seven dashes are not a
#                                         rule; nine find no block anywhere); every header row (`next')
#    the closing rule: `h == 2 &&', 8 dashes, `exit'
#                                         BA (a rule before any banner closes nothing); R7B (seven dashes do not close the
#                                         block); NM (no model line in the block: a model line after the close is not read)
#    the body: `h == 2', the cap `++n > 30'
#                                         R7A (the lines between banner and first rule are not body); K30 / K31 (a model at
#                                         body line 30 read, at 31 not)
#    the first `model:' line, anchored    TM (two model lines: the first is read); MA (`fallback model:' is not a model line);
#                                         M1, X5
#    the model line's two trims           WS (`model:<TAB><SP><SP>gpt-6-astra<SP><CR>' verifies)
#  classification
#    the gate `rc -ne 0 || body -eq 0'    N1, N2, X2, N4; RC2W (rc 2 with an answer IS classified); B1G (a 1-byte rc-0
#                                         answer is NOT)
#    `^ERROR:', `grep -a'                 X1; X8
#    ANSI strip on the ERROR lines        A1, Q3, R2X (SGR, one code per escape); CSI (a non-SGR CSI and a `;'-joined SGR)
#    the refusal alternatives, `-i'       P2, Q1, A1 (`flagged for possible cybersecurity'); RF1 (`cannot help with');
#                                         RF2 (`can't help with'); RF3 (`I won't help'); RFC (the first, upper case)
#    the wall alternatives, `-i'          P1, Q2, Q3, X8 (`usage limit'); WL1 (`quota'); WL2 (`rate limit');
#                                         WL3 (`not authenticated'); WLC (the first, upper case)
#    refusal count `refus -gt 0', at BOTH guards
#                                         P2, Q1, A1, D1 (count 1); R2X (2, the final guard); D3 (2, the fallback)
#    wall count `wall -gt 0'              W1L (count 1); P1, Q2, Q3, X8 (2); N4 (6)
#  the fallback
#    trigger `refus -gt 0 && -n AUP_MODEL && AUP_MODEL != MODEL'
#                                         D1, D2, D3 fire; FB1, FB2 do not (an answer, a wall; the fallback on); FD (empty:
#                                         never); D5 (asked ON Daybreak and refused: no second run)
#    once                                 D4 (refused, then refused on Daybreak: exactly two calls)
#    the refused run's files kept         D1R (codex_D1.refused.txt and .refused.err byte-for-byte the first run's; codex_D1.txt
#                                         and .err the Daybreak run's)
#    the answer credited to the fallback  D1, D3 (Daybreak credited); D2 (Daybreak compared -> 5)
#  the exit cascade: refused 7, walled 8, empty 6, a different model 5, codex's own rc
#    each status                          P2 (7); P1 (8); N3, X1 (6); M1 (5); RC1A (1); RC3A (3: the RAW rc, not a 1)
#    the order, each adjacent pair        RW (refusal + wall -> 7); P2 (refusal + empty + rc 1 -> 7); RI (refusal + another
#                                         model's header -> 7); P1 (wall + empty -> 8); WI (wall + another header -> 8);
#                                         EM (empty + another header -> 6); X1 (empty + rc 1 -> 6); IR (rc 1, an answer,
#                                         another header -> 5)
#    the empty test `body -eq 0'          N3, X1 (0 bytes -> 6); B1E (1 byte -> 0)
#    identity `-n RAN && RAN != ANSWERED_BY'
#                                         M1, D2, X5, W12, K30, X13, CH, IR, BA -> 5; M2, X6, X9, W13, K31, NM, HB -> UNVERIFIED, 0
#  the log phrases a caller reads (_scratchpad/codexpack_20260928/run_pack_body.sh: done_job and reap)
#    `seat answered' iff exit 0; `The answer is LOST' iff exit 7; `answered by: <model>' iff an exit 0 whose model verified
#                                         PK (every after run); N1V, WMT (which model); M2, X6, X9, W13, K31, NM, HB (none)
#    the `codex rc=N   stdout=N b   stderr=N b   asked: M / E' line, which the launch-log censuses this file cites parse
#                                         LOG (N1)
#  NOT PINNED, each with its reason:
#    `|| exit 9' after `cd'               needs a missing project dir -- untestable without editing the file
#    `set -u'                             reached only by a missing positional argument (a usage error, exit 1); every caller
#                                         passes three, and a row without them would write outside the scratch dir under a
#                                         mutant that drops it
#    the banner rule's `next'             equivalent: the banner line matches no later rule
#    RELATIVE paths                       the brief's size and `mkdir' resolve in the caller's directory, codex's files after
#                                         `cd "$PROJ"', so a relative brief or out path breaks (measured 2026-10-17: a relative
#                                         pointer read 787 bytes, codex got no brief, exit 1 -- NOT a clean run, nothing
#                                         laundered).  Disclosed in the usage line; every caller on record, and every row here,
#                                         passes absolute paths
#    display only -- printed, read by no decision and no caller: `brief bytes'; the `ran:' line (the header's effort is
#                                         printed, never compared); `verdict-in-stdout' (verd exists for that line alone); the
#                                         IGNORED note; the refusal excerpts (`-m1'/`-m2', `cut -c1-160'); the REPHRASE line;
#                                         the wording of the 5, 6, 8 and rc messages beyond the phrases above
#  SYNTHETIC SHAPES, pinned because a constant's edges are what an edge row is for: RF1-RF3, RFC, WL1-WL3, WLC, RW, BA, HB,
#  R7A, R7B, NM, TM, MA, WS, K30, K31 and W12/W13 have 0 instances on record, and so does CSI's non-SGR half (CENSUS_v5.txt,
#  which names each count).  CSI's other half is NOT synthetic: a `;'-joined SGR sits in 44 of the 2,425 codex .err files on
#  record, so the strip's `;' is load-bearing.
#
#  Exit 0 only if every expectation holds (v1 ended on an echo and exited 0 whatever the tally -- GPT-6 Astra, pass 2).
#  Usage: bash run_controls_v5.sh   ($CXL_AFTER overrides the after launcher; CXL_AFTER_ONLY=1 runs only the after column, which
#  the mutant table uses; writes only to a scratch dir it removes)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
TRACKED="$HERE/cxlaunch_tracked.sh"
BEFORE="$HERE/cxlaunch_before.sh"
AFTER="${CXL_AFTER:-$REPO/tools/cxlaunch.sh}"
ONLY="${CXL_AFTER_ONLY:-}"
N1D="$REPO/regress/artifacts/exemptredate_20260925/final550"
QD="$REPO/regress/artifacts/adj_20261016/fable5/meas_C/cxctl_fable"
NROWS=65
NFD=56
for f in "$TRACKED" "$BEFORE" "$AFTER" "$N1D/codex_astra550.txt" "$N1D/codex_astra550.err" "$QD/Q1.stderr" "$QD/Q2.stderr" \
         "$QD/Q3.stderr" "$HERE/fx/P1.stderr" "$HERE/fx/P2.stderr" "$HERE/fx/N2.stdout" "$HERE/fx/R2.stderr"; do
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
printf 'x' > "$T/ans_1byte.txt"
hdr() {    # $1 the model -- a minimal closed opening header block
    printf 'OpenAI Codex v0.153.4\n--------\nmodel: %s\nreasoning effort: ultra\n--------\n' "$1"
}
hdr gpt-6-astra > "$T/hdr_astra.txt"
hdr gpt-6-other > "$T/hdr_other.txt"
grep -m1 '^ERROR:' "$HERE/fx/P2.stderr" > "$T/refusal_line.txt"
grep -m1 '^ERROR:' "$HERE/fx/P1.stderr" > "$T/wall_line.txt"
[ -s "$T/refusal_line.txt" ] && [ -s "$T/wall_line.txt" ] || { echo "APPARATUS FAIL: no column-0 ERROR line in P1 or P2"; exit 9; }
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
hdr gpt-daybreak-blue-latest | mkfx DB_OK 0 "$HERE/fx/N2.stdout" -
mkfx DB_WRONG 0 "$HERE/fx/N2.stdout" "$T/hdr_astra.txt"
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
#  v4 (the v3 pass): the window's and the cap's EDGES, the real warning-prefixed header, a real doubled refusal, one wall line
hdrat() {    # $1 lines before the banner, $2 the block's model -- a CLOSED opening block whose banner is line $1+1
    i=1; while [ $i -le "$1" ]; do printf 'startup line %d\n' $i; i=$((i + 1)); done
    printf 'OpenAI Codex v0.153.4\n--------\nworkdir: C:\\DocumentNoSnc\\CC\\GXEMUL\nmodel: %s\nprovider: openai\n' "$2"
    printf 'reasoning effort: ultra\n--------\nuser\nthe session brief\n'
}
hdrat 10 gpt-6-other | mkfx W12 0 "$T/ans_verdict.txt" -      # banner line 11, first rule line 12: inside the window
hdrat 11 gpt-6-other | mkfx W13 0 "$T/ans_verdict.txt" -      # banner line 12, first rule line 13: outside it
head -14 "$REPO/regress/artifacts/ppcrldimimask/codex_book1check_20260910.err" | mkfx X13 0 "$T/ans_verdict.txt" -
capat() {    # $1 body lines before the block's `model:' line -- an UNTERMINATED opening block
    printf 'OpenAI Codex v0.153.4\n--------\n'
    i=1; while [ $i -le "$1" ]; do printf 'body line %d\n' $i; i=$((i + 1)); done
    printf 'model: gpt-6-other\nreasoning effort: ultra\n'
    i=1; while [ $i -le 20 ]; do printf 'streamed line %d\n' $i; i=$((i + 1)); done
}
capat 29 | mkfx K30 0 "$T/ans_verdict.txt" -                  # the model is body line 30: read
capat 30 | mkfx K31 0 "$T/ans_verdict.txt" -                  # the model is body line 31: not read
mkfx R2 1 "" "$HERE/fx/R2.stderr"
mkfx W1L 1 "" "$T/wall_line.txt"
mkfx ANS 0 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
#  v5 (the v4 pass): the rc pass-through, the gate's and the empty test's 1-byte edge, the real coloured header, each pattern
#  alternative and the case fold, a non-SGR strip, each adjacent pair of the exit cascade, and every awk guard and constant
mkfx RC1A 1 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
mkfx RC3A 3 "$T/ans_verdict.txt" "$T/hdr_astra.txt"
mkfx RC2W 2 "$T/ans_verdict.txt" "$HERE/fx/P1.stderr"
mkfx B1G 0 "$T/ans_1byte.txt" "$HERE/fx/P1.stderr"
mkfx B1E 0 "$T/ans_1byte.txt" "$T/hdr_astra.txt"
head -12 "$HERE/fx/R2.stderr" | mkfx CH 0 "$T/ans_verdict.txt" -      # its opening block only: `ESC[1mmodel:ESC[0m gpt-6-astra'
printf 'ERROR: I cannot help with that request.\n' | mkfx RF1 1 "" -
printf "ERROR: I can't help with that request.\n" | mkfx RF2 1 "" -
printf "ERROR: I won't help with that request.\n" | mkfx RF3 1 "" -
printf 'ERROR: THIS CONTENT WAS FLAGGED FOR POSSIBLE CYBERSECURITY RISK.\n' | mkfx RFC 1 "" -
printf 'ERROR: quota exceeded for this workspace.\n' | mkfx WL1 1 "" -
printf 'ERROR: rate limit reached; retry in 60s.\n' | mkfx WL2 1 "" -
printf 'ERROR: not authenticated -- run codex login.\n' | mkfx WL3 1 "" -
printf "ERROR: You've hit your USAGE LIMIT.\n" | mkfx WLC 1 "" -
printf '%s\n' "${ESC}[2K${ESC}[1;31mERROR:${ESC}[0m This content was flagged for possible cybersecurity risk." | mkfx CSI 1 "" -
cat "$T/refusal_line.txt" "$T/wall_line.txt" | mkfx RW 1 "" -
cat "$T/hdr_other.txt" "$T/refusal_line.txt" | mkfx RI 1 "" -
cat "$T/hdr_other.txt" "$T/wall_line.txt" | mkfx WI 1 "" -
mkfx EM 0 "" "$T/hdr_other.txt"
mkfx IR 1 "$T/ans_verdict.txt" "$T/hdr_other.txt"
printf 'OpenAI Codex v0.153.4\n--------\nmodel:\t  gpt-6-astra \r\nreasoning effort: ultra\n--------\n' | mkfx WS 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nfallback model: gpt-6-other\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx MA 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nmodel: gpt-6-other\nreasoning effort: ultra\n--------\n' \
    | mkfx TM 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nworkdir: x\nreasoning effort: ultra\n--------\nuser\nmodel: gpt-6-other\n' \
    | mkfx NM 0 "$T/ans_verdict.txt" -
printf '> OpenAI Codex v0.1 (a quoted transcript)\n--------\nmodel: gpt-6-other\n--------\n' > "$T/ba_pre.txt"
cat "$T/ba_pre.txt" "$T/hdr_astra.txt" | mkfx BA 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\nOpenAI Codex v0.1 (quoted)\n--------\nmodel: gpt-6-other\n--------\n' \
    | mkfx HB 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n-------\nmodel: gpt-6-other\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx R7A 0 "$T/ans_verdict.txt" -
printf 'OpenAI Codex v0.153.4\n--------\n-------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' \
    | mkfx R7B 0 "$T/ans_verdict.txt" -

#  the fake codex: replays $FX (or $FX2 when the requested -m equals $FX2_MODEL); logs its arguments to $FX_ARGS, its working
#  directory to $FX_ARGS.cwd and the first 60 bytes of its stdin to $FX_ARGS.stdin
cat > "$T/fakecodex.sh" <<'EOF'
#!/bin/bash
D="$FX"; prev=""
for a in "$@"; do
    if [ "$prev" = "-m" ] && [ -n "${FX2_MODEL:-}" ] && [ "$a" = "$FX2_MODEL" ]; then D="$FX2"; fi
    prev="$a"
done
if [ -n "${FX_ARGS:-}" ]; then
    { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"
    pwd >> "$FX_ARGS.cwd"
    head -c 60 >> "$FX_ARGS.stdin"
fi
cat "$D/stdout"; cat "$D/stderr" 1>&2; exit "$(cat "$D/rc")"
EOF
chmod +x "$T/fakecodex.sh"
#  the default-path fake under the scratch HOME: it marks the run, then is the same fake (the tracked launcher names only this
#  path; the after launcher reaches it only when CX_CODEX_BIN is unset or empty)
DEFBIN="$T/home/AppData/Local/Programs/OpenAI/Codex/bin"
mkdir -p "$DEFBIN"
printf '#!/bin/bash\n[ -n "${FX_ARGS:-}" ] && echo DEFAULT >> "$FX_ARGS.default"\nexec bash "%s" "$@"\n' "$T/fakecodex.sh" > "$DEFBIN/codex"
chmod +x "$DEFBIN/codex"
printf 'control brief\n' > "$T/brief.md"
printf '%30000s' '' | tr ' ' b > "$T/brief30000.md"
printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"
printf 'STDIN MARKER -- codex must never read this\n' > "$T/stdin_marker"

pass=0; total=0
run() {    # $1 row, $2 launcher label, $3 launcher, $4 expected exit (? = record only, counted as a failure), then env
    local row="$1" lab="$2" sh="$3" want="$4"; shift 4
    local out="$T/out_${row}_${lab}"
    case " $* " in *" CX_AUP_MODEL= "*) : > "$T/disabled_${row}_${lab}" ;; esac
    ( export HOME="$T/home" CX_CODEX_BIN="$T/fakecodex.sh" FX2= FX2_MODEL= FX_ARGS="$T/args_${row}_${lab}"
      for kv in "$@"; do export "$kv"; done
      [ "${UNSET_CODEX_BIN:-}" = 1 ] && unset CX_CODEX_BIN
      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" < "$T/stdin_marker" ) > "$T/log_${row}_${lab}.txt" 2>&1
    local got=$?
    echo "$got" > "$T/exit_${row}_${lab}"
    total=$((total + 1))
    local ok="NO"; [ "$got" = "$want" ] && { ok="ok"; pass=$((pass + 1)); }
    printf '%-4s %-7s exit=%-3s want=%-3s %s\n' "$row" "$lab" "$got" "$want" "$ok"
    sed 's/^/      /' "$T/log_${row}_${lab}.txt" | grep -v '^      brief bytes' | cut -c1-170
}
three() {    # $1 row, $2 want-tracked, $3 want-before, $4 want-after, then env
    local row="$1" wt="$2" wb="$3" wa="$4"; shift 4
    if [ "$ONLY" != 1 ]; then
        run "$row" tracked "$TRACKED" "$wt" "$@"
        run "$row" before "$BEFORE" "$wb" "$@"
    fi
    run "$row" after "$AFTER" "$wa" "$@"
}
check() {    # $1 label, $2 0/1 result
    total=$((total + 1))
    if [ "$2" = 0 ]; then pass=$((pass + 1)); echo "$1  ok"; else echo "$1  NO"; fi
}

echo "# cxlaunch landing controls (v5), $(date '+%Y-%m-%d %H:%M:%S')${ONLY:+ -- AFTER COLUMN ONLY}"
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
three W12 0 0 5 FX="$T/fx/W12" CX_AUP_MODEL=
three W13 0 0 0 FX="$T/fx/W13" CX_AUP_MODEL=
three X13 0 0 5 FX="$T/fx/X13" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three K30 0 0 5 FX="$T/fx/K30" CX_AUP_MODEL=
three K31 0 0 0 FX="$T/fx/K31" CX_AUP_MODEL=
three R2X 6 6 7 FX="$T/fx/R2" CX_AUP_MODEL=
three D3 6 6 0 FX="$T/fx/R2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest
three D4 7 7 7 FX="$T/fx/P2" FX2="$T/fx/P2" FX2_MODEL=gpt-daybreak-blue-latest
three W1L 8 8 8 FX="$T/fx/W1L" CX_AUP_MODEL=
#  CX_AUP_MODEL is left UNSET -- the fallback on, as production runs it -- by FB1 and FB2 (no refusal), by D1-D5 and EO
#  (refusals), and set EMPTY by every other row.  (v4 said "every other row disables it" beside FB1/FB2, which D1-D4 refuted;
#  GLM 5.3, v4 pass.)
three FB1 8 0 0 FX="$T/fx/N1"
three FB2 8 8 8 FX="$T/fx/P1"
three X14 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30000.md"
three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"
#  v5 rows
three RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=
three RC3A 3 3 3 FX="$T/fx/RC3A" CX_AUP_MODEL=
three RC2W 8 8 8 FX="$T/fx/RC2W" CX_AUP_MODEL=
three B1G 8 0 0 FX="$T/fx/B1G" CX_AUP_MODEL=
three B1E 0 0 0 FX="$T/fx/B1E" CX_AUP_MODEL=
three D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest
three CH 0 0 5 FX="$T/fx/CH" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three DP 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= UNSET_CODEX_BIN=1
three EO 7 0 0 FX="$T/fx/P2" FX2="$T/fx/DB_OK" FX2_MODEL=gpt-daybreak-blue-latest CX_CODEX_BIN= CX_MODEL= CX_EFFORT= CX_AUP_EFFORT=
three RF1 7 7 7 FX="$T/fx/RF1" CX_AUP_MODEL=
three RF2 7 7 7 FX="$T/fx/RF2" CX_AUP_MODEL=
three RF3 7 7 7 FX="$T/fx/RF3" CX_AUP_MODEL=
three RFC 7 7 7 FX="$T/fx/RFC" CX_AUP_MODEL=
three WL1 8 8 8 FX="$T/fx/WL1" CX_AUP_MODEL=
three WL2 8 8 8 FX="$T/fx/WL2" CX_AUP_MODEL=
three WL3 8 8 8 FX="$T/fx/WL3" CX_AUP_MODEL=
three WLC 8 8 8 FX="$T/fx/WLC" CX_AUP_MODEL=
three CSI 6 6 7 FX="$T/fx/CSI" CX_AUP_MODEL=
three RW 7 7 7 FX="$T/fx/RW" CX_AUP_MODEL=
three RI 7 7 7 FX="$T/fx/RI" CX_AUP_MODEL=
three WI 8 8 8 FX="$T/fx/WI" CX_AUP_MODEL=
three EM 6 6 6 FX="$T/fx/EM" CX_AUP_MODEL=
three IR 1 1 5 FX="$T/fx/IR" CX_AUP_MODEL=
three WS 0 0 0 FX="$T/fx/WS" CX_AUP_MODEL=
three MA 0 0 0 FX="$T/fx/MA" CX_AUP_MODEL=
three TM 0 0 0 FX="$T/fx/TM" CX_AUP_MODEL=
three NM 0 0 0 FX="$T/fx/NM" CX_AUP_MODEL=
three BA 0 0 5 FX="$T/fx/BA" CX_AUP_MODEL= CX_MODEL=gpt-6-other
three HB 0 0 0 FX="$T/fx/HB" CX_AUP_MODEL=
three R7A 0 0 0 FX="$T/fx/R7A" CX_AUP_MODEL=
three R7B 0 0 5 FX="$T/fx/R7B" CX_AUP_MODEL= CX_MODEL=gpt-6-other

#  E0: the fake ran for every row of every column but X15's, and never for X15's (it must exit 9 BEFORE codex); the run count is
#  pinned, so a deleted row is visible.  The other aggregate checks read the AFTER runs; each pins its own denominator.
cols=3; [ "$ONLY" = 1 ] && cols=1
nruns=$(ls "$T"/log_* 2>/dev/null | wc -l)
miss=""; extra=""
for f in "$T"/log_*; do b=${f##*/log_}; b=${b%.txt}
    case "$b" in X15_*) [ -e "$T/args_$b" ] && extra="$extra $b" ;; *) [ -s "$T/args_$b" ] || miss="$miss $b" ;; esac
done
[ "$nruns" = $((NROWS * cols)) ] && [ -z "$miss" ] && [ -z "$extra" ]; check "E0  all  the fake codex was reached by every run but X15's, and by none of X15's ($NROWS rows x $cols = $nruns of $((NROWS * cols)), pinned)${miss:+ -- NOT reached:$miss}${extra:+ -- X15 REACHED it:$extra}" $?
nafter=0; dbad=""; sbad=""; ns=0; cbad=""; nc=0; pbad=""; fbad=""; nfd=0
for f in "$T"/exit_*_after; do r=${f##*/exit_}; r=${r%_after}; nafter=$((nafter + 1))
    case "$r" in
        DP|EO) [ -e "$T/args_${r}_after.default" ] || dbad="$dbad $r(not reached)" ;;
        *) [ -e "$T/args_${r}_after.default" ] && dbad="$dbad $r" ;;
    esac
    if [ -e "$T/args_${r}_after.stdin" ]; then ns=$((ns + 1)); [ -s "$T/args_${r}_after.stdin" ] && sbad="$sbad $r"; fi
    if [ -e "$T/args_${r}_after.cwd" ]; then nc=$((nc + 1))
        while IFS= read -r d; do [ "$(printf '%s' "$d" | tr 'A-Z' 'a-z')" = /c/documentnosnc/cc/gxemul ] || cbad="$cbad $r"; done < "$T/args_${r}_after.cwd"
    fi
    e=$(cat "$f"); L="$T/log_${r}_after.txt"
    a=$(grep -c 'seat answered' "$L"); l=$(grep -c 'The answer is LOST' "$L"); b=$(grep -c 'answered by: ' "$L"); u=$(grep -c 'model UNVERIFIED' "$L")
    case "$e" in
        0) { [ "$a" -ge 1 ] && [ "$l" = 0 ] && [ $((b + u)) = 1 ]; } || pbad="$pbad $r" ;;
        7) { [ "$l" -ge 1 ] && [ "$a" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
        *) { [ "$a" = 0 ] && [ "$l" = 0 ] && [ "$b" = 0 ]; } || pbad="$pbad $r" ;;
    esac
    if [ -e "$T/disabled_${r}_after" ] && [ "$r" != X15 ]; then nfd=$((nfd + 1))
        [ "$(grep -c '^CALL$' "$T/args_${r}_after" 2>/dev/null)" = 1 ] || fbad="$fbad $r"
    fi
done
[ "$nafter" = "$NROWS" ] && [ -z "$dbad" ]; check "E0b after  the default-path fake was reached by DP's and EO's after runs and by no other (of $nafter)${dbad:+ -- wrong:$dbad}" $?
[ "$ns" = $((NROWS - 1)) ] && [ -z "$sbad" ]; check "SI  after  no after run's codex read the stdin the launcher was fed ($ns runs that reached codex, of $((NROWS - 1)))${sbad:+ -- READ IT:$sbad}" $?
[ "$nc" = $((NROWS - 1)) ] && [ -z "$cbad" ]; check "CWD after  every after run's codex started in the project root ($nc of $((NROWS - 1)))${cbad:+ -- elsewhere:$cbad}" $?
[ "$nfd" = "$NFD" ] && [ -z "$fbad" ]; check "FD  after  every row that sets CX_AUP_MODEL empty made exactly one call ($nfd rows, $NFD pinned)${fbad:+ -- more:$fbad}" $?
[ "$nafter" = "$NROWS" ] && [ -z "$pbad" ]; check "PK  after  'seat answered' iff exit 0, 'The answer is LOST' iff exit 7, 'answered by:' iff a verified exit 0 ($nafter runs)${pbad:+ -- wrong:$pbad}" $?
grep -qE '^codex rc=0   stdout=[0-9]+ b   stderr=[0-9]+ b   asked: gpt-6-astra / ultra$' "$T/log_N1_after.txt"; check "LOG after  N1's 'codex rc=0   stdout=N b   stderr=N b   asked: gpt-6-astra / ultra' line, as the launch-log censuses parse it" $?
[ "$(ls "$T/out_N1_after" | wc -l)" = 2 ] && cmp -s "$T/out_N1_after/codex_N1.txt" "$T/fx/N1/stdout" && cmp -s "$T/out_N1_after/codex_N1.err" "$T/fx/N1/stderr"; check "N1F after  out dir holds exactly codex_N1.txt and codex_N1.err, byte-for-byte the fixture's stdout and stderr" $?
grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_N1_after.txt"; check "N1V after  N1 is credited to gpt-6-astra" $?
grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_WS_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_MA_after.txt" && grep -qF 'seat answered. (answered by: gpt-6-astra)' "$T/log_TM_after.txt"; check "WMT after  WS, MA and TM verify gpt-6-astra (not UNVERIFIED)" $?
#  content, not exit status -- on the AFTER logs
for r in M2 X6 X9 W13 K31 NM HB; do
    grep -q 'model UNVERIFIED' "$T/log_${r}_after.txt" && ! grep -q 'answered by:' "$T/log_${r}_after.txt"; check "$r  after  says model UNVERIFIED and names no model" $?
done
cmp -s "$T/out_D1_after/codex_D1.refused.txt" "$T/fx/P2/stdout" && cmp -s "$T/out_D1_after/codex_D1.refused.err" "$T/fx/P2/stderr" \
    && cmp -s "$T/out_D1_after/codex_D1.txt" "$T/fx/DB_OK/stdout" && cmp -s "$T/out_D1_after/codex_D1.err" "$T/fx/DB_OK/stderr" \
    && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D1_after.txt"; check "D1R after  refused run kept byte-for-byte as .refused.txt/.err, Daybreak's run as .txt/.err, Daybreak credited" $?
[ "$(grep -c '^CALL$' "$T/args_FB1_after" 2>/dev/null)" = 1 ] && ! ls "$T/out_FB1_after"/*.refused.* >/dev/null 2>&1; check "FB1 after  the fallback on, an answer: ONE call, nothing renamed .refused" $?
[ "$(grep -c '^CALL$' "$T/args_FB2_after" 2>/dev/null)" = 1 ]; check "FB2 after  the fallback on, a wall: ONE call" $?
[ "$(grep -c '^CALL$' "$T/args_D4_after" 2>/dev/null)" = 2 ]; check "D4  after  refused, then refused on Daybreak: EXACTLY two calls" $?
[ "$(grep -c '^CALL$' "$T/args_D3_after" 2>/dev/null)" = 2 ] && grep -q 'answered by: gpt-daybreak-blue-latest' "$T/log_D3_after.txt"; check "D3  after  a doubled refusal re-runs on Daybreak: two calls, Daybreak credited" $?
[ "$(grep -c '^CALL$' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked ON Daybreak and refused: ONE call, no re-run on the same model" $?
[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?
grep -qF "codex's header says gpt-6-astra" "$T/log_CH_after.txt"; check "CH  after  the coloured header is read: the log names gpt-6-astra as the model that ran" $?
#  E1/E2: the exact argument sequence of each call, one argument per line, compared whole
callseq() {    # $1 model -- the sequence one call must receive
    printf 'CALL\nARG exec\nARG --sandbox\nARG read-only\nARG --skip-git-repo-check\nARG -m\nARG %s\nARG -c\n' "$1"
    printf 'ARG model_reasoning_effort=ultra\nARG control brief\n'
}
callseq gpt-6-astra > "$T/want_E1"
{ callseq gpt-6-astra; callseq gpt-daybreak-blue-latest; } > "$T/want_E2"
cmp -s "$T/want_E1" "$T/args_N1_after"; check "E1  after  N1: exactly one call, exactly exec --sandbox read-only ... -m gpt-6-astra, effort ultra, the brief" $?
cmp -s "$T/want_E2" "$T/args_D1_after"; check "E2  after  D1: exactly two calls, Astra then Daybreak, the same exact arguments each" $?
cmp -s "$T/want_E2" "$T/args_EO_after"; check "EO  after  CX_CODEX_BIN, CX_MODEL, CX_EFFORT, CX_AUP_EFFORT set EMPTY: the defaults, both calls exactly as E2" $?
cmp -s "$T/want_E1" "$T/args_DP_after"; check "DP  after  CX_CODEX_BIN unset: the default-path codex, called exactly as E1" $?
echo "CONTROLS: $pass/$total as expected"
echo "CXLAND_CONTROLS_DONE"
[ "$pass" = "$total" ]
