import io, sys
src, dst = sys.argv[1], sys.argv[2]
lines = io.open(src, encoding="utf-8", newline="").read().split("\n")
def one(pred, what):
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if len(idx) != 1:
        print("ANCHOR %s matched %d lines" % (what, len(idx))); sys.exit(1)
    return idx[0]
i = one(lambda l: 'timeout 120 bash "$sh"' in l, "run line")
assert lines[i].count('"$row" )') == 1
lines[i] = lines[i].replace('"$row" )', '"$row" < "${STDIN_OVERRIDE:-/dev/null}" )')
i = one(lambda l: ">> \"$FX_ARGS\"" in l, "fake args log")
lines.insert(i + 1, '[ -n "${FX_ARGS:-}" ] && head -c 60 > "$FX_ARGS.stdin"')
i = one(lambda l: '| mkfx ANS 0' in l, "ANS fixture")
lines.insert(i + 1, 'mkfx RC1A 1 "$T/ans_verdict.txt" "$T/fx/ANS/stderr"     # fable5 PROPOSED: rc 1 WITH an answer and a clean header')
i = one(lambda l: l.startswith("printf") and 'brief30001.md"' in l, "brief30001")
lines.insert(i + 1, "echo 'STDIN_LEAK: the launcher left its own stdin open to codex' > \"$T/stdin_marker.txt\"")
i = one(lambda l: l.startswith("three X15 "), "X15 row")
lines[i + 1:i + 1] = ['#  fable5 v4-pass PROPOSED rows (scratch copy, not in the tree)',
                      'three RC1A 1 1 1 FX="$T/fx/RC1A" CX_AUP_MODEL=',
                      'three D5 7 7 7 FX="$T/fx/P2" CX_MODEL=gpt-daybreak-blue-latest',
                      'three SI 0 0 0 FX="$T/fx/ANS" CX_AUP_MODEL= STDIN_OVERRIDE="$T/stdin_marker.txt"']
i = one(lambda l: '[ "$nruns" = 102 ]' in l, "E0")
lines[i] = lines[i].replace('[ "$nruns" = 102 ]', '[ "$nruns" = 111 ]').replace('34 rows x 3 = $nruns of 102', '37 rows x 3 = $nruns of 111')
i = one(lambda l: 'args_X15_after" ]; check' in l, "X15 check")
lines[i + 1:i + 1] = ['[ "$(grep -c \'^CALL$\' "$T/args_D5_after" 2>/dev/null)" = 1 ]; check "D5  after  asked on Daybreak and refused: no re-run on the SAME model, ONE call" $?',
                      '[ "$(grep -c \'^CALL$\' "$T/args_P2_after" 2>/dev/null)" = 1 ]; check "P2  after  the fallback DISABLED (CX_AUP_MODEL empty): ONE call" $?',
                      '[ -e "$T/args_SI_after.stdin" ] && ! grep -q STDIN_LEAK "$T/args_SI_after.stdin"; check "SI  after  codex stdin is /dev/null: the launcher own stdin does not reach it" $?',
                      '[ -s "$T/out_N1_after/codex_N1.txt" ] && [ -s "$T/out_N1_after/codex_N1.err" ]; check "N1  after  the answer and stderr land in codex_<tag>.txt / .err" $?']
i = one(lambda l: 'echo "# cxlaunch landing controls (v4),' in l, "title")
lines[i] = lines[i].replace('(v4),', '(v4 + fable5 PROPOSED rows, scratch),')
io.open(dst, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("wrote", dst)
