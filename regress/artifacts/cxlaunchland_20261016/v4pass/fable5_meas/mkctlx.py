import io, sys
src, dst = sys.argv[1], sys.argv[2]
t = io.open(src, encoding="utf-8", newline="").read()
R = [
 ('      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" ) > "$T/log_${row}_${lab}.txt" 2>&1',
  '      timeout 120 bash "$sh" "${BRIEF_OVERRIDE:-$T/brief.md}" "$out" "$row" < "${STDIN_OVERRIDE:-/dev/null}" ) > "$T/log_${row}_${lab}.txt" 2>&1'),
 ('''[ -n "${FX_ARGS:-}" ] && { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"\n''',
  '''[ -n "${FX_ARGS:-}" ] && { printf 'CALL\n'; for a in "$@"; do printf 'ARG %s\n' "$a"; done; } >> "$FX_ARGS"\n[ -n "${FX_ARGS:-}" ] && head -c 60 > "$FX_ARGS.stdin"\n'''),
 ('''printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx ANS 0 "$T/ans_verdict.txt" -\n''',
  '''printf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx ANS 0 "$T/ans_verdict.txt" -\nprintf 'OpenAI Codex v0.153.4\n--------\nmodel: gpt-6-astra\nreasoning effort: ultra\n--------\n' | mkfx RC1A 1 "$T/ans_verdict.txt" -\n'''),
 ('''printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"\n''',
  '''printf '%30001s' '' | tr ' ' b > "$T/brief30001.md"\nprintf 'STDIN_LEAK: the launcher left its own stdin open to codex\n' > "$T/stdin_marker.txt"\n'''),
 ('''three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"\n''',
  '''three X15 9 9 9 FX="$T/fx/ANS" CX_AUP_MODEL= BRIEF_OVERRIDE="$T/brief30001.md"\n#  fable5 v4-pass PROPOSED rows (scratch copy, not in the tree)\nthree RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=\nthree D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest\nthree SI 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= STDIN_OVERRIDE="$T/stdin_marker.txt"\n'''),
 ('[ "$nruns" = 102 ]', '[ "$nruns" = 111 ]'),
 ('(34 rows x 3 = $nruns of 102, pinned)', '(37 rows x 3 = $nruns of 111, pinned)'),
 ('''[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?\n''',
  '''[ ! -e "$T/args_X15_after" ]; check "X15 after  a 30,001-byte brief never reaches codex" $?\n[ "$(grep -c '^CALL$' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked on Daybreak and refused: no re-run on the SAME model, ONE call" $?\n[ "$(grep -c '^CALL$' "$T/args_P2_after" 2>/dev/null)" = 1 ]; check "P2  after  the fallback DISABLED (CX_AUP_MODEL empty): ONE call" $?\n[ -e "$T/args_SI_after.stdin" ] && ! grep -q STDIN_LEAK "$T/args_SI_after.stdin"; check "SI  after  codex's stdin is /dev/null: the launcher's own stdin does not reach it" $?\n[ -s "$T/out_N1_after/codex_N1.txt" ] && [ -s "$T/out_N1_after/codex_N1.err" ]; check "N1  after  the answer and stderr land in codex_<tag>.txt / .err" $?\n'''),
 ('echo "# cxlaunch landing controls (v4), $(date', 'echo "# cxlaunch landing controls (v4 + fable5 PROPOSED rows, scratch), $(date'),
]
for a, b in R:
    n = t.count(a)
    if n != 1:
        print("EDIT_TEXT_NOT_FOUND (found %d): %s" % (n, a[:70])); sys.exit(1)
    t = t.replace(a, b)
io.open(dst, "w", encoding="utf-8", newline="").write(t)
print("wrote", dst)
