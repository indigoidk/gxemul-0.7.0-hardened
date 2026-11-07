#!/usr/bin/env bash
# run_mutants.sh CHECKER HOOK SEC WORK [PRE] -- the mutants the pass-2 review traced past the controls BY READING (Fable
# 5.1, PASS2_RULING.md, section B item 3; this table then corrected the reading: M3 and M6 were already red on the census
# count legs c5, M1, M2 and M5 on nothing earlier), and those the repair's pass 2 owed for its class closure (Fable 5.1,
# REPAIR_RULING.md, s.4: M9-M13, and M14, M9's index-mode twin), and the closing pass's (Fable 5.1, CLOSE_RULING.md: M15
# and M16, a one-sided working-copy fallback on each of the index guard's two reads), each MEASURED against
# run_checker_controls.sh rather than predicted.
#
#   CHECKER  the checker as it lands; HOOK  a file carrying section P2 as it lands (the staged precommit_check.sh, or the
#   filled hunk); SEC  a GXEMUL-SEC clone for the --at legs; WORK  scratch; PRE  optional: the checker as it was BEFORE the
#   repair (the first build's), run as one more "mutant" -- the repair's own legs must red on it.
#
# Each mutant is ONE edit, applied by exact text to a copy (an edit whose text is not found exactly once is NOT BUILT --
# counted against the run, which then exits nonzero -- so every find-text also pins that the code still reads that way;
# the destination is removed first, so a stale copy is never scored).  It is killed when the leg built for it reads BAD; the
# score is every leg that went BAD.  The unmutated pair runs first and must be 0 BAD, or nothing after it means anything.
# Ends `MUTANTS: N mutants, K killed by their own leg, E escaped`; exits nonzero unless every mutant was killed.
CH=$1; HK=$2; SEC=$3; WORK=$4; PRE=$5
D=$(cd "$(dirname "$0")" && pwd)
[ -f "$CH" ] && [ -f "$HK" ] && [ -d "$SEC" ] && [ -n "$WORK" ] || { echo "usage: $0 CHECKER HOOK SEC WORK [PRE]"; exit 9; }
mkdir -p "$WORK"; WORK=$(cd "$WORK" && pwd)
CTL=$WORK/run_checker_controls.frozen.sh
cp "$D/run_checker_controls.sh" "$CTL"; cp -r "$D/synth" "$WORK/"      # the controls find synth/ beside themselves
echo "controls: run_checker_controls.sh md5 $(md5sum < "$CTL" | cut -c1-12), frozen for this run"
echo "checker $(md5sum < "$CH" | cut -c1-12); hook $(md5sum < "$HK" | cut -c1-12)"

mutate () {   # src dst find replace -> exact one-occurrence replacement, or a FAIL
	python - "$1" "$2" "$3" "$4" <<'PYEOF'
import io, sys
src, dst, find, rep = sys.argv[1:5]
s = io.open(src, encoding="utf-8", newline="").read()
n = s.count(find)
if n != 1:   # bytes, so Windows' text stdout cannot turn the newline into CRLF: the bank is LF text
    sys.stdout.buffer.write(("MUTANT TEXT FOUND %d TIMES (want 1): %r\n" % (n, find)).encode("utf-8")); sys.exit(3)
io.open(dst, "w", encoding="utf-8", newline="").write(s.replace(find, rep))
PYEOF
}
runctl () {   # tag checker hook -> the BAD legs, one per line, in $WORK/$tag.bad; the total in $WORK/$tag.n
	rm -rf "$WORK/w_$1"
	bash "$CTL" "$2" "$SEC" "$WORK/w_$1" "$3" > "$WORK/$1.out" 2>&1
	grep -E '^BAD ' "$WORK/$1.out" | awk '{print $2}' | sort -u > "$WORK/$1.bad"
	sed -n 's/^CONTROLS: \([0-9]*\) ok, \([0-9]*\) BAD$/\1 \2/p' "$WORK/$1.out" > "$WORK/$1.n"
}
runctl base "$CH" "$HK"
read bok bbad < "$WORK/base.n"
echo "baseline: $bok ok, $bbad BAD"
[ "$bbad" = "0" ] && [ -n "$bok" ] || { echo "BASELINE NOT CLEAN -- no mutant score means anything"; cat "$WORK/base.bad"; echo "MUTANTS: 0 mutants, 0 killed by their own leg, 0 escaped"; exit 4; }

n=0; k=0; e=0
leg () {   # name kind(checker|hook|whole) target-leg(s, comma) find replace
	local name=$1 kind=$2 targets=$3 find=$4 rep=$5 ch=$CH hk=$HK
	#  A stale destination from an earlier run must never be scored: remove it first, and a mutate that fails (its text
	#  not found exactly once) is NOT BUILT -- counted, and the run exits nonzero (REVIEW 2, A2).
	rm -f "$WORK/$name.check_ghost_rounds.py" "$WORK/$name.hook.sh"
	if [ "$kind" = checker ]; then ch=$WORK/$name.check_ghost_rounds.py
		mutate "$CH" "$ch" "$find" "$rep" || { e=$((e+1)); n=$((n+1)); echo "$name  NOT BUILT: mutant text"; return; }
	elif [ "$kind" = hook ]; then hk=$WORK/$name.hook.sh
		mutate "$HK" "$hk" "$find" "$rep" || { e=$((e+1)); n=$((n+1)); echo "$name  NOT BUILT: mutant text"; return; }
	else ch=$find; fi
	[ -f "$ch" ] && [ -f "$hk" ] || { e=$((e+1)); n=$((n+1)); echo "$name  NOT BUILT"; return; }
	runctl "$name" "$ch" "$hk"
	read mok mbad < "$WORK/$name.n"
	local killed=1 t
	for t in ${targets//,/ }; do grep -qx "$t" "$WORK/$name.bad" || killed=0; done
	n=$((n+1)); if [ $killed = 1 ]; then k=$((k+1)); v=KILLED; else e=$((e+1)); v=ESCAPED; fi
	printf '%-5s %-7s %-8s by %-46s score %s of %s legs BAD: %s\n' "$name" "$kind" "$v" "$targets" "$mbad" "$((mok + mbad))" \
		"$(tr '\n' ' ' < "$WORK/$name.bad")"
	printf '      the edit: %s\n' "$( [ "$kind" = whole ] && echo "the whole checker replaced by $(basename "$find") ($(md5sum < "$find" | cut -c1-12))" || printf '%s  ->  %s' "$find" "$rep")"
}
#  The NEGATIVE CONTROL of this driver (REVIEW 2, A2): NEGCTL=1 runs one mutant whose text is in no checker, over a
#  STALE destination as an earlier run would leave it.  It must print NOT BUILT and the run must exit nonzero -- before
#  the fix, mutate's status was dropped and the stale file was scored (MUTANTS_NEGCTL.out).
if [ -n "${NEGCTL:-}" ]; then
	cp "$CH" "$WORK/NEG.check_ghost_rounds.py"
	leg NEG checker c1a_open_mention 'THIS TEXT IS IN NO CHECKER' ''
	echo "MUTANTS: $n mutants, $k killed by their own leg, $e escaped"
	[ "$k" = "$n" ]; exit
fi
leg M1 hook c9a_hook_mention_rule 'python "$GHOSTCHK" 2>&1)' 'python "$GHOSTCHK" --rule=date 2>&1)'
leg M2 checker c8f_staged_dated_FAIL 'landed = bdate or (date if src == "header" else UNDATED)' 'landed = date if src == "header" else (bdate or UNDATED)'
leg M3 checker c1e_prior_entry_FAIL 'return any((e.get("date") or "") >= date and pat.search(as_text(e)) for e in entries(row))' 'return any(pat.search(as_text(e)) for e in entries(row))'
leg M5 checker c8g_tempindex_FAIL 'capture_output=True, timeout=timeout)' 'capture_output=True, timeout=timeout, env={k: v for k, v in os.environ.items() if k != "GIT_INDEX_FILE"})'
leg M6 checker c1d_held_header_FAIL 'TERMINAL = ("closed", "dropped")' 'TERMINAL = ("closed", "dropped", "held")'
leg M7 hook c9b_hook_env_cleared 'env -u GXLEDGER -u GXCHANGELOG -u GXSEC -u GXGHOST_CUTOFF -u GXGHOST_TODAY python' 'python'
leg M8 hook c9c_hook_rc0_no_token " && printf '%s' \"\$out\" | grep -q '^GHOST_ROUNDS_PASS'; then" '; then'
#  REVIEW 2 -- the class closure's mutants (Fable 5.1's ruling of 2026-11-07, REPAIR_RULING.md, s.4), and M14, the
#  index-mode twin of M9: complete() made a blame returning {} VOID too, so c8i was tightened to the failure's message
#  and this measures that it tells the two apart.
leg M9 checker c4d_at_tree_blame_VOID '    rc, out = git(["blame", "--porcelain", rev, "--", CHANGELOG_REL])
    return porcelain_dates(out) if rc == 0 else None' '    rc, out = git(["blame", "--porcelain", rev, "--", CHANGELOG_REL])
    return porcelain_dates(out) if rc == 0 else {}'
leg M10 checker c8j_blame_incomplete_VOID,c8k_at_blame_incomplete_VOID '    if len(bl) != nlines(cb):' '    if False:'
leg M11 hook c9d_hook_tempindex_FAIL 'env -u GXLEDGER -u GXCHANGELOG' 'env -u GIT_INDEX_FILE -u GXLEDGER -u GXCHANGELOG'
M12REP="elif printf '%s' \"\$out\" | grep -q '^GHOST_ROUNDS_VOID'; then
	good \"void\"
elif printf '%s' \"\$out\" | grep -q 'GHOST_ROUNDS_FAIL'; then"
leg M12 hook c9e_hook_void_FAIL "elif printf '%s' \"\$out\" | grep -q 'GHOST_ROUNDS_FAIL'; then" "$M12REP"
leg M13 hook c9a_hook_mention_rule,c9b_hook_env_cleared,c9d_hook_tempindex_FAIL "bad \"A ROUND BLOCK'S ROWS DO NOT RECORD THE ROUND:\"" "(bad \"A ROUND BLOCK'S ROWS DO NOT RECORD THE ROUND:\")"
leg M14 checker c8i_blame_unreadable_VOID '        os.remove(tmp)
    return porcelain_dates(out) if rc == 0 else None' '        os.remove(tmp)
    return porcelain_dates(out) if rc == 0 else {}'
#  REVIEW 3 -- the closing pass's mutants (Fable 5.1, CLOSE_RULING.md, s.4 R2): a one-sided working-copy fallback after
#  the index git_show line, on each of the two reads the guard tests separately.
leg M15 checker c8l_ledger_unstaged_VOID '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)' '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)
        lb = lb if lb is not None else open(LEDGER, "rb").read()'
leg M16 checker c8m_changelog_unstaged_VOID '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)' '        lb, cb = git_show("", LEDGER_REL), git_show("", CHANGELOG_REL)
        cb = cb if cb is not None else open(CHANGELOG, "rb").read()'
[ -n "$PRE" ] && leg PRE whole c8h_index_unreadable_VOID,c8i_blame_unreadable_VOID "$PRE" ""
echo "MUTANTS: $n mutants, $k killed by their own leg, $e escaped"
[ "$k" = "$n" ]
