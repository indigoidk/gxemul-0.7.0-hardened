#!/usr/bin/env python3
"""mut_launcher_v7.py <launcher.sh> <out dir> -- write one-edit mutants of tools/cxlaunch.sh (2026-10-17 landing, v7) for the
controls' kill table (run_mutants_v7.sh).  Each mutant names the controls expected to catch it; v5 pins every decision its
CONTRACT lists, so no mutant is UNPINNED (v4's three -- m_eq1, m_sgr, m_prec -- are pinned by RC2W, CSI and RW).  The v4 list is
kept whole; v5 adds one mutant per decision the v4 pass found unpinned and per decision the v5 enumeration reads off the file
(run_controls_v5.sh's CONTRACT); v6 appends one per escape the v5 pass MEASURED (GLM 5.3, GPT-6 Astra, Grok 4.7, Fable 5.1)
and per edge v6 rows; v7 one per escape the v6 pass named (GPT-6 Astra's nine), per edge v7 rows and for the
fallback's re-classification (Grok 4.7).  m_twice inserts a line and the m_ord_* mutants MOVE one block of the exit cascade: each is
still one edit.  A find-text that is absent, or present more than once, is an apparatus failure, never a silent skip."""
import io, os, sys

src, out = sys.argv[1], sys.argv[2]
t = io.open(src, encoding="utf-8", newline="").read()
#  the opening-header awk, as v3/v4 read it, so the find-text cannot drift
AWK = ('HDR=$(strip_ansi "$ERR" | awk \'NR > 12 && h < 2 { exit }\n        h == 0 && /^OpenAI Codex/ { h = 1; next }\n'
       '        h == 1 && /^--------/ { h = 2; next }\n        h == 2 && /^--------/ { exit }\n'
       '        h == 2 { if (++n > 30) exit; print }\')')
STRIP = 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*[A-Za-z]//g" "$1" 2>/dev/null; }'
REF = r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with\|I won.t help'"
WAL = r"grep -ic 'usage limit\|quota\|rate limit\|not authenticated'"
GATE = 'if [ "$rc" -ne 0 ] || [ "$body" -eq 0 ]; then'
TRIG = 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ] && [ "$AUP_MODEL" != "$MODEL" ]; then'

#  the exit cascade, cut from the launcher itself into its five blocks: refusal 7, wall 8, empty 6, identity 5, codex's rc
R0 = 'if [ "$refus" -gt 0 ]; then\n    echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.'
W0 = 'if [ "$wall" -gt 0 ]; then echo "  *** SEAT WALLED'
E0 = 'if [ "$body" -eq 0 ]; then echo "  *** EMPTY STDOUT'
I0 = 'if [ -n "$RAN" ] && [ "$RAN" != "$ANSWERED_BY" ]; then'
C0 = 'if [ "$rc" -ne 0 ];  then echo "  *** codex exited $rc'
C1 = 'exit "$rc"; fi\n'
starts = [t.find(x) for x in (R0, W0, E0, I0, C0)]
cend = t.find(C1, starts[4]) + len(C1) if starts[4] >= 0 else -1
if min(starts) < 0 or cend < 0 or starts != sorted(starts) or any(t.count(x) != 1 for x in (R0, W0, E0, I0, C0)):
    print("CASCADE_NOT_FOUND (starts %s)" % starts); sys.exit(1)
B = dict(zip("RWEIC", [t[starts[i]:(starts[i + 1] if i < 4 else cend)] for i in range(5)]))
CASCADE = "".join(B[k] for k in "RWEIC")

def order(seq):
    return (CASCADE, "".join(B[k] for k in seq))

MUTANTS = [
    #  v4's table, unchanged
    ("m_anchor", "X1", "grep -a '^ERROR:'", "grep -a 'ERROR:'"),
    ("m_bodyverd", "X2", GATE, 'if [ "$rc" -ne 0 ] || [ "$verd" -eq 0 ]; then'),
    ("m_suffix", "X5", '[ "$RAN" != "$ANSWERED_BY" ]', '[ "${RAN##*-}" != "${ANSWERED_BY##*-}" ]'),
    ("m_effort", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$1"'),
    ("m_head40", "X6", AWK, 'HDR=$(strip_ansi "$ERR" | head -n 40)'),
    ("m_v2awk", "X9 X10", AWK,
     """HDR=$(strip_ansi "$ERR" | awk '/^OpenAI Codex/ { h = 1; next } h == 1 && /^--------/ { h = 2; next } h == 2 && /^--------/ { exit } h == 2')"""),
    ("m_effortx", "E1 E2", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$2x"'),
    ("m_sandbox", "E1 E2", "--sandbox read-only", "--sandbox workspace-write"),
    ("m_brief", "E1 E2", '"$(cat "$BRIEF")"', '"$BRIEF"'),
    ("m_noa", "X8", "grep -a '^ERROR:'", "grep '^ERROR:'"),
    ("m_nostrip", "Q3 A1 CH", STRIP, 'strip_ansi() { cat "$1" 2>/dev/null; }'),
    ("m_noident", "M1 D2 X5", I0, "if false; then"),
    ("m_nofallback", "D1 D2 E2", 'AUP_MODEL="${CX_AUP_MODEL-gpt-daybreak-blue-latest}"', 'AUP_MODEL=""'),
    ("m_nogate", "N1 X2", GATE, "if true; then"),
    ("m_claimmodel", "M2 X6", 'echo "  seat answered -- model UNVERIFIED: no model line in an opening codex header block (requested: $ANSWERED_BY)"',
     'echo "  seat answered. (answered by: $ANSWERED_BY)"'),
    ("m_eq1", "RC2W", GATE, 'if [ "$rc" -eq 1 ] || [ "$body" -eq 0 ]; then'),
    ("m_sgr", "CSI", STRIP, 'strip_ansi() { sed "s/${ESC}\\[[0-9;]*m//g" "$1" 2>/dev/null; }'),
    ("m_prec", "RW", "        wall=$(printf '%s' \"$CXERR\" | " + WAL + ")",
     "        wall=$(printf '%s' \"$CXERR\" | " + WAL + "); [ \"$wall\" -gt 0 ] && refus=0"),
    ("m_win11", "W12", "NR > 12 && h < 2", "NR > 11 && h < 2"),
    ("m_win13", "W13", "NR > 12 && h < 2", "NR > 13 && h < 2"),
    ("m_win3", "W12 X13", "NR > 12 && h < 2", "NR > 3 && h < 2"),
    ("m_cap29", "K30", "if (++n > 30) exit", "if (++n > 29) exit"),
    ("m_cap31", "K31", "if (++n > 30) exit", "if (++n > 31) exit"),
    ("m_nocap", "K31", "h == 2 { if (++n > 30) exit; print }", "h == 2 { print }"),
    ("m_fbeq1", "D3", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -eq 1 ] && [ -n "$AUP_MODEL" ]'),
    ("m_refeq1", "R2X", 'if [ "$refus" -gt 0 ]; then\n    echo', 'if [ "$refus" -eq 1 ]; then\n    echo'),
    ("m_wallgt1", "W1L", 'if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 1 ]; then'),
    ("m_fbge0", "FB1", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]', 'if [ "$refus" -ge 0 ] && [ -n "$AUP_MODEL" ]'),
    ("m_fbwall", "FB2", 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]',
     'if { [ "$refus" -gt 0 ] || [ "$wall" -gt 0 ]; } && [ -n "$AUP_MODEL" ]'),
    ("m_twice", "D4 E2", '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n',
     '    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n    run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify\n'),
    ("m_argv1", "X15", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 30001 ]'),
    ("m_argv2", "X14", '[ "$sz" -gt 30000 ]', '[ "$sz" -gt 29999 ]'),
    #  v5 -- configuration
    ("m_defpath", "DP", 'Codex/bin/codex}"', 'Codex/bin/codex2}"'),
    ("m_binignore", "E0b", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BINX:-'),
    ("m_bincolon", "EO", '"${CX_CODEX_BIN:-', '"${CX_CODEX_BIN-'),
    ("m_modelcolon", "EO", '"${CX_MODEL:-', '"${CX_MODEL-'),
    ("m_effortcolon", "EO", '"${CX_EFFORT:-', '"${CX_EFFORT-'),
    ("m_aupeffcolon", "EO", '"${CX_AUP_EFFORT:-', '"${CX_AUP_EFFORT-'),
    ("m_aupcolon", "FD", '"${CX_AUP_MODEL-', '"${CX_AUP_MODEL:-'),
    ("m_nomkdir", "N1", 'mkdir -p "$OUT"', ': mkdir -p "$OUT"'),
    ("m_txtname", "N1F", 'TXT="$OUT/codex_${TAG}.txt"', 'TXT="$OUT/codex_${TAG}.out"'),
    ("m_errname", "N1F", 'ERR="$OUT/codex_${TAG}.err"', 'ERR="$OUT/codex_${TAG}.log"'),
    ("m_swapio", "N1F", '> "$TXT" 2> "$ERR" < /dev/null', '> "$ERR" 2> "$TXT" < /dev/null'),
    ("m_nostdin", "SI", '2> "$ERR" < /dev/null', '2> "$ERR"'),
    ("m_cd", "CWD", 'cd "$PROJ" || exit 9', 'cd "$HOME" || exit 9'),
    ("m_noskip", "E1", ' --skip-git-repo-check', ''),
    #  v5 -- the opening header
    ("m_hdrnostrip", "CH", 'HDR=$(strip_ansi "$ERR" | awk', 'HDR=$(cat "$ERR" | awk'),
    ("m_hlt1", "W13", "NR > 12 && h < 2", "NR > 12 && h < 1"),
    ("m_hlt3", "K30 W12", "NR > 12 && h < 2", "NR > 12 && h < 3"),
    ("m_bannerun", "BA", "h == 0 && /^OpenAI Codex/", "h == 0 && /OpenAI Codex/"),
    ("m_bannerh", "HB", "h == 0 && /^OpenAI Codex/", "/^OpenAI Codex/"),
    ("m_rule1h", "BA", "h == 1 && /^--------/ { h = 2; next }", "/^--------/ { h = 2; next }"),
    ("m_rule7a", "R7A", "h == 1 && /^--------/", "h == 1 && /^-------/"),
    ("m_rule1next", "M1", "{ h = 2; next }", "{ h = 2 }"),
    ("m_close2h", "BA", "h == 2 && /^--------/ { exit }", "/^--------/ { exit }"),
    ("m_rule7b", "R7B", "h == 2 && /^--------/ { exit }", "h == 2 && /^-------/ { exit }"),
    ("m_exitnext", "NM", "h == 2 && /^--------/ { exit }", "h == 2 && /^--------/ { next }"),
    ("m_bodyh1", "R7A", "h == 2 { if (++n > 30) exit; print }", "h >= 1 { if (++n > 30) exit; print }"),
    ("m_capn", "K31", "if (++n > 30) exit", "if (n++ > 30) exit"),
    ("m_m2", "TM", "grep -m1 '^model:'", "grep -m2 '^model:'"),
    ("m_modelanchor", "MA", "grep -m1 '^model:'", "grep -m1 'model:'"),
    ("m_trailws", "WS", "s/^model:[[:space:]]*//; s/[[:space:]]*$//'", "s/^model:[[:space:]]*//'"),
    ("m_leadws", "WS", "s/^model:[[:space:]]*//", "s/^model: //"),
    ("m_nomodelsed", "N1", "sed 's/^model:[[:space:]]*//; s/", "sed 's/"),
    #  v5 -- classification
    ("m_strip_nog", "A1 CSI", '[A-Za-z]//g" "$1"', '[A-Za-z]//" "$1"'),
    ("m_strip_nosemi", "CSI", '\\[[0-9;]*[A-Za-z]', '\\[[0-9]*[A-Za-z]'),
    ("m_noinit", "N1", "refus=0; wall=0", ":"),
    ("m_gateand", "N4 RC2W", GATE, 'if [ "$rc" -ne 0 ] && [ "$body" -eq 0 ]; then'),
    ("m_gatele1", "B1G", GATE, 'if [ "$rc" -ne 0 ] || [ "$body" -le 1 ]; then'),
    ("m_ref1", "P2", REF, r"grep -ic 'cannot help with\|can.t help with\|I won.t help'"),
    ("m_ref2", "RF1", REF, r"grep -ic 'flagged for possible cybersecurity\|can.t help with\|I won.t help'"),
    ("m_ref3", "RF2", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|I won.t help'"),
    ("m_ref4", "RF3", REF, r"grep -ic 'flagged for possible cybersecurity\|cannot help with\|can.t help with'"),
    ("m_refcase", "RFC", REF, REF.replace("grep -ic", "grep -c")),
    ("m_wall1", "P1", WAL, r"grep -ic 'quota\|rate limit\|not authenticated'"),
    ("m_wall2", "WL1", WAL, r"grep -ic 'usage limit\|rate limit\|not authenticated'"),
    ("m_wall3", "WL2", WAL, r"grep -ic 'usage limit\|quota\|not authenticated'"),
    ("m_wall4", "WL3", WAL, r"grep -ic 'usage limit\|quota\|rate limit'"),
    ("m_wallcase", "WLC", WAL, WAL.replace("grep -ic", "grep -c")),
    #  v5 -- the fallback
    ("m_samemodel", "D5", TRIG, 'if [ "$refus" -gt 0 ] && [ -n "$AUP_MODEL" ]; then'),
    ("m_noempty", "FD", TRIG, 'if [ "$refus" -gt 0 ] && [ "$AUP_MODEL" != "$MODEL" ]; then'),
    ("m_norefusedtxt", "D1R", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"; ', ''),
    ("m_norefusederr", "D1R", '; mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"', ''),
    ("m_ansby", "D1 D2", '    ANSWERED_BY="$AUP_MODEL"', '    ANSWERED_BY="$MODEL"'),
    #  v5 -- the exit cascade
    ("m_emptyle1", "B1E", E0, 'if [ "$body" -le 1 ]; then echo "  *** EMPTY STDOUT'),
    ("m_noransep", "M2", I0, 'if [ "$RAN" != "$ANSWERED_BY" ]; then'),
    ("m_zflip", "M2 N1V", 'if [ -z "$RAN" ]; then', 'if [ -n "$RAN" ]; then'),
    ("m_rcpass", "RC1A RC3A", 'if [ "$rc" -ne 0 ];  then', 'if false;  then'),
    ("m_rcgt1", "RC1A", 'if [ "$rc" -ne 0 ];  then', 'if [ "$rc" -gt 1 ];  then'),
    ("m_rcone", "RC3A", C1, 'exit 1; fi\n'),
    ("m_ord_wr", "RW",) + order("WREIC"),
    ("m_ord_re", "P2",) + order("ERWIC"),
    ("m_ord_ri", "RI",) + order("IRWEC"),
    ("m_ord_rc", "P2",) + order("CRWEI"),
    ("m_ord_we", "P1",) + order("REWIC"),
    ("m_ord_wi", "WI",) + order("RIWEC"),
    ("m_ord_wc", "P1",) + order("RCWEI"),
    ("m_ord_ei", "EM",) + order("RWIEC"),
    ("m_ord_ec", "X1",) + order("RWCEI"),
    ("m_ord_ic", "IR",) + order("RWECI"),
    #  v5 -- the log phrases a caller reads
    ("m_msganswered", "PK", 'echo "  seat answered. (answered by:', 'echo "  seat replied. (answered by:'),
    ("m_msganswered2", "PK", 'echo "  seat answered -- model UNVERIFIED', 'echo "  seat replied -- model UNVERIFIED'),
    ("m_msglost", "PK", "The answer is LOST, whatever", "The answer is gone, whatever"),
    ("m_msgby", "PK N1V", "(answered by: $ANSWERED_BY)", "(by: $ANSWERED_BY)"),
    ("m_rcline", "LOG", 'echo "codex rc=$rc   stdout=', 'echo "codex rc=$rc stdout='),
    #  v6 -- each override's VALUE (GLM 5.3, GPT-6 Astra, Fable 5.1: each escaped 94/94, measured)
    ("m_effortfix", "OVA", '\nEFFORT="${CX_EFFORT:-ultra}"', '\nEFFORT=ultra'),
    ("m_aupeffortfix", "OVA", 'AUP_EFFORT="${CX_AUP_EFFORT:-ultra}"', 'AUP_EFFORT=ultra'),
    ("m_aupcalleff", "OVA", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex "$AUP_MODEL" "$EFFORT"; classify'),
    ("m_mainmodelfix", "OVA", 'run_codex "$MODEL" "$EFFORT"; classify', 'run_codex gpt-6-astra "$EFFORT"; classify'),
    ("m_aupmodelfix", "OV OVA", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex gpt-daybreak-blue-latest "$AUP_EFFORT"; classify'),
    #  v6 -- the fallback's own rc (GPT-6 Astra)
    ("m_fbrc", "FR", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; rc=$?; classify'),
    #  v6 -- a used out dir, a missing parent, a non-empty refused stdout (all four seats; GLM 5.3; GPT-6 Astra)
    ("m_append", "RSF", '"$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null', '"$(cat "$BRIEF")" >> "$TXT" 2> "$ERR" < /dev/null'),
    ("m_appenderr", "RS RSF", '"$(cat "$BRIEF")" > "$TXT" 2> "$ERR" < /dev/null', '"$(cat "$BRIEF")" > "$TXT" 2>> "$ERR" < /dev/null'),
    ("m_mkdirnop", "MP MPF", 'mkdir -p "$OUT"', 'mkdir "$OUT"'),
    ("m_refusedempty", "RNF", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt";', ': > "$OUT/codex_${TAG}.refused.txt";'),
    #  v6 -- the opening header: the rules' anchors at both ends, the banner's text, the trims' `*' (GPT-6 Astra, GLM 5.3, Grok 4.7)
    ("m_rule1unanch", "SP1", "h == 1 && /^--------/ { h = 2; next }", "h == 1 && /--------/ { h = 2; next }"),
    ("m_rule2unanch", "SP2", "h == 2 && /^--------/ { exit }", "h == 2 && /--------/ { exit }"),
    ("m_rule1end", "R9A", "h == 1 && /^--------/ { h = 2; next }", "h == 1 && /^--------$/ { h = 2; next }"),
    ("m_rule2end", "R9B", "h == 2 && /^--------/ { exit }", "h == 2 && /^--------$/ { exit }"),
    ("m_bannercodex", "BN WMT", "h == 0 && /^OpenAI Codex/", "h == 0 && /^OpenAI/"),
    ("m_ws1", "WZ WMT", "s/^model:[[:space:]]*//", "s/^model:[[:space:]][[:space:]]*//"),
    #  v6 -- a parameterless CSI (GPT-6 Astra)
    ("m_csi1", "CZ", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-9;][0-9;]*[A-Za-z]")),
    #  v6 -- the phrases and numbers a caller reads (GPT-6 Astra: status.sh reads SEAT WALLED; LOG read the format only)
    ("m_wallmsg", "PK", '*** SEAT WALLED ($ANSWERED_BY).', '*** SEAT BLOCKED ($ANSWERED_BY).'),
    ("m_stdoutcnt", "LOG", 'stdout=$(wc -c < "$TXT") b', 'stdout=$(wc -c < "$ERR") b'),
    ("m_stderrcnt", "LOG", 'stderr=$(wc -c < "$ERR") b', 'stderr=$(wc -c < "$TXT") b'),
    ("m_logrc", "LOG", 'echo "codex rc=$rc   stdout=', 'echo "codex rc=0   stdout='),
    ("m_lost7", "R7XL", R0, R0.replace('if [ "$refus" -gt 0 ]; then', 'if [ "$refus" -gt 0 ] || [ "$rc" -eq 7 ]; then')),
    #  v6 -- Fable 5.1's v5-pass escapes in the forms the list above lacked (each measured 94/94 on the v5 controls)
    ("m_effortignore", "OVA", '"${CX_EFFORT:-ultra}"', '"${CX_EFFORTX:-ultra}"'),
    ("m_aupeffignore", "OVA", '"${CX_AUP_EFFORT:-ultra}"', '"${CX_AUP_EFFORTX:-ultra}"'),
    ("m_effortglobal", "OVA", '-c model_reasoning_effort="$2"', '-c model_reasoning_effort="$EFFORT"'),
    ("m_ansbyhard", "OV OVA", '    ANSWERED_BY="$AUP_MODEL"', '    ANSWERED_BY=gpt-daybreak-blue-latest'),
    ("m_askedglobal", "LOG", 'asked: $1 / $2"', 'asked: $MODEL / $EFFORT"'),
    ("m_stripplus", "CZ", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-9;]\\{1,\\}[A-Za-z]")),
    #  v7 -- GPT-6 Astra's nine v6-pass escapes, A-I, each reasoned 269/269 on the v6 controls
    ("m_lostecho7", "PK", 'echo "  *** SEAT REFUSED (content filter) on $ANSWERED_BY.  The answer is LOST, whatever the token count says."',
     'echo "  *** codex exited 7 -- NOT a clean run."'),
    ("m_askedultra", "LOG", 'asked: $1 / $2"', 'asked: $1 / ultra"'),
    ("m_rcmsg7", "RXM R8XL", 'echo "  *** codex exited $rc -- NOT a clean run."', 'echo "  *** codex exited 7 -- NOT a clean run."'),
    ("m_briefhead", "MBA", '"$(cat "$BRIEF")"', '"$(head -n 1 "$BRIEF")"'),
    ("m_mvntxt", "RN2F", 'mv -f "$TXT" "$OUT/codex_${TAG}.refused.txt"', 'mv -n "$TXT" "$OUT/codex_${TAG}.refused.txt"'),
    ("m_mvnerr", "RN2F", 'mv -f "$ERR" "$OUT/codex_${TAG}.refused.err"', 'mv -n "$ERR" "$OUT/codex_${TAG}.refused.err"'),
    ("m_tagupper", "TGF", 'TAG="$3"', 'TAG="${3^^}"'),
    ("m_strip8", "CSX", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-8;]*[A-Za-z]")),
    ("m_stripazm", "CSX", STRIP, STRIP.replace("[0-9;]*[A-Za-z]", "[0-9;]*[A-Zm]")),
    #  v7 -- m_lost7's twin at the wall exit: codex's own rc 8 printed as a wall (R8X; GPT-6 Astra, v6 pass: "SEAT WALLED iff
    #  exit 8" is false of it)
    ("m_rc8wall", "R8XL PK", W0, W0.replace('if [ "$wall" -gt 0 ]; then', 'if [ "$wall" -gt 0 ] || [ "$rc" -eq 8 ]; then')),
    #  v7 -- the fallback run's re-classification (Grok 4.7, v6 pass: the row that pins it is not D4)
    ("m_noreclassify", "D1 D2", 'run_codex "$AUP_MODEL" "$AUP_EFFORT"; classify', 'run_codex "$AUP_MODEL" "$AUP_EFFORT"'),
]
os.makedirs(out, exist_ok=True)
bad = 0
names = set()
with io.open(os.path.join(out, "MUTANTS.list"), "w", encoding="utf-8", newline="\n") as lst:
    for name, catches, find, repl in MUTANTS:
        n = t.count(find)
        if n != 1 or name in names or find == repl:
            print("MUTANT_TEXT_NOT_FOUND %s (found %d)" % (name, n)); bad += 1; continue
        names.add(name)
        io.open(os.path.join(out, name + ".sh"), "w", encoding="utf-8", newline="").write(t.replace(find, repl))
        lst.write("%s\t%s\n" % (name, catches))
print("mutants written: %d of %d" % (len(MUTANTS) - bad, len(MUTANTS)))
sys.exit(1 if bad else 0)
