#!/usr/bin/env python3
"""mut_launcher_v4.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-17 landing, v4) for the
controls' kill table (run_mutants_v4.sh).  Each mutant names the control expected to catch it, or UNPINNED with the reason it
is deliberately not pinned (a sibling of the recorded N4 residual, or a shape with 0 instances on record -- CENSUS_v4.txt and
the v4 controls' CONTRACT).  One mutant, m_twice, inserts a line (the fallback run twice): still one edit.
A find-text that is absent is an apparatus failure, never a silent skip."""
import io, os, sys

src, out = sys.argv[1], sys.argv[2]
t = io.open(src, encoding="utf-8", newline="").read()
#  the v3 launcher's opening-header awk, read from the launcher itself so the find-text cannot drift
V3AWK = 'HDR=$(strip_ansi "$ERR" | awk \'NR > 12 && h < 2 { exit }\n        h == 0 && /^OpenAI Codex/ { h = 1; next }\n        h == 1 && /^--------/ { h = 2; next }\n        h == 2 && /^--------/ { exit }\n        h == 2 { if (++n > 30) exit; print }\')'
MUTANTS = [
    ("m_anchor", "X1", "grep -a '^ERROR:'", "grep -a 'ERROR:'"),
    ("m_bodyverd", "X2", 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', 'if [ "$rc" -ne 0 ] || [ "$verd" -eq 0 ]; then'),
    ("m_suffix", "X5", '[ "$RAN" != "$ANSWERED_BY" ]', '[ "${RAN##*-}" != "${ANSWERED_BY##*-}" ]'),
    ("m_effort", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$1"'),
    ("m_head40", "X6", V3AWK, 'HDR=$(strip_ansi "$ERR" | head -n 40)'),
    ("m_v2awk", "X9 X10", V3AWK,
     """HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')"""),
    ("m_effortx", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$2x"'),
    ("m_sandbox", "E1 E2", "--sandbox read-only", "--sandbox workspace-write"),
    ("m_brief", "E1 E2", '"$(cat "$BRIEF")"', '"$BRIEF"'),
    ("m_noa", "X8", "grep -a '^ERROR:'", "grep '^ERROR:'"),
    ("m_nostrip", "Q3 A1", 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }', 'strip_ansi() { cat "$1" 2>/dev/null; }'),
    ("m_noident", "M1 D2 X5", 'if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then', "if false; then"),
    ("m_nofallback", "D1 D2 E2", 'AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"', 'AUP_MODEL=""'),
    ("m_nogate", "N1 X2", 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', "if true; then"),
    ("m_claimmodel", "M2 X6", 'echo "  seat answered -- model UNVERIFIED: no codex header block in stderr (requested: $ANSWERED_BY)"',
     'echo "  seat answered. (answered by: $ANSWERED_BY)"'),
    ("m_eq1", "UNPINNED (only an rc outside {0,1} WITH an answer -- a sibling of N4, 0 on record)",
     'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then', 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
    ("m_sgr", "UNPINNED (non-SGR CSI: 0 of 2,372 .err files on record)",
     'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }', 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
    ("m_prec", "UNPINNED (a refusal and a wall line in one stderr on a run that ENTERS classification: 0 of 410 in CENSUS_v4.txt)",
     r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated')""",
     r"""        wall=$(printf '%s' "$CXERR" | grep -ic 'usage limit\|quota\|rate limit\|not authenticated'); [ "$wall" -gt 0 ] && refus=0"""),
    #  v4 -- the v3 pass's floor breaches (GPT-6 Astra, Grok 4.7, GLM 5.3) and their edges
    ("m_win11", "W12", "NR > 12 && h < 2", "NR > 11 && h < 2"),
    ("m_win13", "W13", "NR > 12 && h < 2", "NR > 13 && h < 2"),
    ("m_win3", "W12 X13", "NR > 12 && h < 2", "NR > 3 && h < 2"),
    ("m_cap29", "K30", "if (++n > 30) exit", "if (++n > 29) exit"),
    ("m_cap31", "K31", "if (++n > 30) exit", "if (++n > 31) exit"),
    ("m_nocap", "K31", "h == 2 { if (++n > 30) exit; print }", "h == 2 { print }"),
    ("m_fbeq1", "D3", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -eq 1 ] && [ -n "$AUP_MODEL" ]'),
    ("m_refeq1", "R2X", 'if [ "$refus" -gt 0 ]; then', 'if [ "$refus" -eq 1 ]; then'),
    ("m_wallgt1", "W1L", 'if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 1 ]; then'),
    ("m_fbge0", "FB1", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -ge 0 ] && [ -n "$AUP_MODEL" ]'),
    ("m_fbwall", "FB2", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]',
     'if { [ "$refus" -gt 0 ] || [ "$wall" -gt 0 ]; } && [ -n "$AUP_MODEL" ]'),
    ("m_twice", "D4 E2", '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n',
     '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n'),
    ("m_argv1", "X15", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 30001 ]'),
    ("m_argv2", "X14", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 29999 ]'),
]
os.makedirs(out, exist_ok=True)
bad = 0
with io.open(os.path.join(out, "MUTANTS.list"), "w", encoding="utf-8", newline="\n") as lst:
    for name, catches, find, repl in MUTANTS:
        n = t.count(find)
        if n != 1:
            print("MUTANT_TEXT_NOT_FOUND %s (found %d)" % (name, n)); bad += 1; continue
        io.open(os.path.join(out, name + ".sh"), "w", encoding="utf-8", newline="").write(t.replace(find, repl))
        lst.write("%s\t%s\n" % (name, catches))
print("mutants written: %d of %d" % (len(MUTANTS) - bad, len(MUTANTS)))
sys.exit(1 if bad else 0)
