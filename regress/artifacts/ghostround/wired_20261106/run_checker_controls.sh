#!/usr/bin/env bash
# run_checker_controls.sh CHECKER SEC WORK HOOK -- the controls of check_ghost_rounds.py AS INSTALLED (ledger row
# `ghostround`), and of section P2 itself.
#
#   CHECKER  the installed checker (tools/pipeline/check_ghost_rounds.py as committed, or a staged copy of it)
#   SEC      a GXEMUL-SEC clone, read ONLY through `git show` / `git blame` by the --at legs (GXSEC)
#   WORK     a scratch directory for outputs and the index-mode repos (created, never inside SEC)
#   HOOK     the precommit_check.sh carrying section P2 (as committed, or staged); leg 9 cuts P2's block out of it
#
# Legs 1-7 are the census's 35 controls (regress/artifacts/ghostround/census_20261106/controls/run_controls.out), the
# same fixtures (synth/, beside this script) and the same expectations, run on the installed copy.  Legs 8 are new:
# the installed checker reads CHANGELOG.md and the ledger from the INDEX, and each leg shows which copy it read --
# a staged block fails, a working-tree-only block does not (unless --worktree), and a write-back counts only when
# it is staged.  Every control greps the verdict TOKEN, never the exit code alone (a crash is not a FAIL).
#
# The legs marked REVIEW were added after the pass-2 review (Fable 5.1's ruling, PASS2_RULING.md): each pins a predicate
# the rule depends on that a one-line mutant could break, traced past the controls BY READING -- M1, M2 and M5 passed
# every earlier leg and the full GREEN/RED runs; M3 and M6 were already red on the census count legs c5, which the
# mutant table measured (this said "while every earlier leg and the full GREEN/RED runs stayed green").  Beside each is the mutant it was built for and that mutant's MEASURED score (MUTANTS.out, run_mutants.sh).
# The script EXITS NONZERO on any BAD leg (it ended in `echo` before the review).
#
# The legs marked REVIEW 2 are the CLASS CLOSURE the repair's own pass 2 owed (Fable 5.1's ruling of 2026-11-07,
# REPAIR_RULING.md, s.4): two passes found one class -- a degraded read, dating or verdict silently taking a weaker
# source -- so every cell of the space (the checker's mode x what git returns; the hook's verdict x environment x
# effect) has a leg or a disclosure, and the checker's docstring names which (THE CONTRACT).  c4d (an --at blame git
# cannot do), c8j and c8k (a blame that exits 0 dating none of the lines: a SHA-256 repository), c9d (the hook keeps
# GIT_INDEX_FILE), c9e (the hook hard-fails VOID); leg 9's harness now COUNTS `fail` as the hook does (HOOK-fail=N) and
# runs under `set -u` as the hook does, and every hook leg that wants a FAIL wants HOOK-fail=1.
#
# The legs marked REVIEW 3 are the closing pass's (Fable 5.1, CLOSE_RULING.md): the index guard tests its two reads
# separately, so "show fails" is a {ok,fail} x {ok,fail} product -- c8l (the ledger absent from the index) and c8m
# (CHANGELOG.md absent) hold the two mixed cells, which c8h's both-fail cell cannot see.
C=$1; SEC=$2; WORK=$3; HOOK=$4
C0=$C
S=$(cd "$(dirname "$0")" && (pwd -W 2>/dev/null || pwd))/synth    # -W: the C:/ form python prints back
[ -f "$C" ] && [ -d "$SEC" ] && [ -n "$WORK" ] && [ -f "$HOOK" ] || { echo "usage: $0 CHECKER SEC WORK HOOK"; exit 9; }
WORK=$(mkdir -p "$WORK" && cd "$WORK" && pwd)      # absolute: legs 8-9 run from inside the repos they build
C=$(cd "$(dirname "$C")" && pwd)/$(basename "$C"); C0=$C
HOOK=$(cd "$(dirname "$HOOK")" && pwd)/$(basename "$HOOK")
O=$WORK/out; mkdir -p "$O"
pass=0; bad=0

ctl () {   # name want_rc want_token [must-contain ...]; env from CTL_ENV, args from CTL_ARGS
	local name=$1 want_rc=$2 want_tok=$3; shift 3
	env $CTL_ENV python -W ignore "$C" $CTL_ARGS > "$O/$name.out" 2>&1
	local rc=$? ok=1
	[ "$rc" = "$want_rc" ] || ok=0
	grep -q "^$want_tok" "$O/$name.out" || ok=0
	for need in "$@"; do grep -q -- "$need" "$O/$name.out" || { ok=0; echo "    missing: $need"; }; done
	if [ $ok = 1 ]; then pass=$((pass+1)); printf 'ok    %-34s rc=%s %s\n' "$name" "$rc" "$want_tok"
	else bad=$((bad+1)); printf 'BAD   %-34s rc=%s (want %s %s)\n' "$name" "$rc" "$want_rc" "$want_tok"; fi
}
absent () {
	if grep -q -- "$2" "$O/$1.out"; then bad=$((bad+1)); printf 'BAD   %-34s contains %s\n' "$1" "$2"
	else pass=$((pass+1)); printf 'ok    %-34s has no %s\n' "$1" "$2"; fi
}
cm () { git -c user.name=ctl -c user.email=ctl@scratch -c core.autocrlf=false "$@"; }

L="GXLEDGER=$S/synth_ledger.json GXGHOST_CUTOFF=2026-11-05 GXGHOST_TODAY=2026-11-06"
echo "checker $C ($(md5sum < "$C" | cut -c1-12)); --at legs read $SEC"

echo "== 1. a synthetic round block naming an OPEN row with no write-back must FAIL"
CTL_ENV="$L GXCHANGELOG=$S/c1a_open.md" CTL_ARGS="" ctl c1a_open_mention 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen" "read: $S/c1a_open.md"
CTL_ENV="$L GXCHANGELOG=$S/c1a_open.md" CTL_ARGS="--rule=date" ctl c1a_open_date 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen"
CTL_ENV="$L GXCHANGELOG=$S/c1b_sameday.md" CTL_ARGS="" ctl c1b_sameday_mention 1 GHOST_ROUNDS_FAIL "GHOST    ghostsameday"
CTL_ENV="$L GXCHANGELOG=$S/c1b_sameday.md" CTL_ARGS="--rule=date" ctl c1b_sameday_date_BLIND 0 GHOST_ROUNDS_PASS
CTL_ENV="$L GXCHANGELOG=$S/c1c_claimed.md" CTL_ARGS="" ctl c1c_claimed_mention 1 GHOST_ROUNDS_FAIL "GHOST    ghostclaimed" "named in the body of #902"
CTL_ENV="$L GXCHANGELOG=$S/c1c_claimed.md" CTL_ARGS="--rule=date" ctl c1c_claimed_date_BLIND 0 GHOST_ROUNDS_PASS
#  REVIEW (M6): a HELD row named in the header with no write-back must FAIL -- `held` is not terminal.
#    mutant M6: TERMINAL = ("closed", "dropped", "held")                                   measured: KILLED; 3 of 69 checks BAD: c1d_held_header_FAIL c5_HEAD_all c5_HEAD_date_all
CTL_ENV="$L GXCHANGELOG=$S/c1d_held.md" CTL_ARGS="" ctl c1d_held_header_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostheld"
#  REVIEW (M3): a row whose only #901 is in an entry dated BEFORE the round must FAIL -- an entry counts from the round on.
#    mutant M3: entries count whatever their date (`(e.get("date") or "") >= date and` deleted)   measured: KILLED; 3 of 69 checks BAD: c1e_prior_entry_FAIL c5_HEAD_all c5_HEAD_subject
CTL_ENV="$L GXCHANGELOG=$S/c1e_prior.md" CTL_ARGS="" ctl c1e_prior_entry_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostprior"

echo "== 2. a properly CLOSED row named the same way must PASS"
CTL_ENV="$L GXCHANGELOG=$S/c2a_closed.md" CTL_ARGS="" ctl c2a_closed_mention 0 GHOST_ROUNDS_PASS "0 without a write-back"
CTL_ENV="$L GXCHANGELOG=$S/c2a_closed.md" CTL_ARGS="--rule=date" ctl c2a_closed_date 0 GHOST_ROUNDS_PASS
CTL_ENV="$L GXCHANGELOG=$S/c2b_recorded.md" CTL_ARGS="" ctl c2b_recorded_mention 0 GHOST_ROUNDS_PASS
CTL_ENV="$L GXCHANGELOG=$S/c2b_recorded.md" CTL_ARGS="--rule=date" ctl c2b_recorded_date_FP 1 GHOST_ROUNDS_FAIL "GHOST    ghostrecorded"
CTL_ENV="$L GXCHANGELOG=$S/c2c_reference.md" CTL_ARGS="" ctl c2c_reference_subject 0 GHOST_ROUNDS_PASS
CTL_ENV="$L GXCHANGELOG=$S/c2c_reference.md" CTL_ARGS="--scope=all" ctl c2c_reference_all 1 GHOST_ROUNDS_FAIL "GHOST    ghostref"

echo "== 3. NULL controls: nothing parsed must be VOID (exit 2), never a clean pass"
CTL_ENV="$L GXCHANGELOG=$S/c3a_empty.md" CTL_ARGS="" ctl c3a_empty_changelog 2 GHOST_ROUNDS_VOID "0 blocks parsed, 0 ROUND"
absent c3a_empty_changelog GHOST_ROUNDS_PASS
CTL_ENV="GXLEDGER=$S/synth_ledger_norows.json GXCHANGELOG=$S/c1a_open.md" CTL_ARGS="" ctl c3b_empty_ledger 2 GHOST_ROUNDS_VOID "no ledger row"
CTL_ENV="$L GXCHANGELOG=$S/c3c_records_only.md" CTL_ARGS="" ctl c3c_records_only 2 GHOST_ROUNDS_VOID "no ROUND block"

echo "== 4. the MOTIVATING CASE, replayed read-only from git: d9efd339, the commit before the write-back"
CTL_ENV="GXSEC=$SEC GXGHOST_CUTOFF=2026-08-26" CTL_ARGS="--at=d9efd339" ctl c4a_d9efd339_mention 1 GHOST_ROUNDS_FAIL "GHOST    wdcwipclear" "GHOST    wdcringnoflush" "GHOST    wdcstalephase"
CTL_ENV="GXSEC=$SEC GXGHOST_CUTOFF=2026-08-26" CTL_ARGS="--at=d9efd339 --rule=date" ctl c4b_d9efd339_date_BLIND 1 GHOST_ROUNDS_FAIL
absent c4b_d9efd339_date_BLIND "GHOST    wdcwipclear"
absent c4b_d9efd339_date_BLIND "GHOST    wdcringnoflush"
absent c4b_d9efd339_date_BLIND "GHOST    wdcstalephase"
CTL_ENV="GXSEC=$SEC GXGHOST_CUTOFF=2026-08-26" CTL_ARGS="--at=4cc3952a" ctl c4c_4cc3952a_mention 1 GHOST_ROUNDS_FAIL
absent c4c_4cc3952a_mention "GHOST    wdcwipclear"
absent c4c_4cc3952a_mention "GHOST    wdcringnoflush"
absent c4c_4cc3952a_mention "GHOST    wdcstalephase"
#  REVIEW 2 (A9, clause (b) at blame_rev's fixed site): a blame git cannot do in --at mode is VOID.  `git show
#  HEAD^{tree}:<path>` reads the files while `git blame HEAD^{tree}` fails ("Non commit HEAD^{tree}?", rc 128 --
#  measured on GXEMUL-SEC by the ruling).  The message is the FAILURE's: with complete() in the same diff, a blame_rev
#  that returned {} would still be VOID, as "dated 0 of N lines" -- so the leg tells the two apart by what it says.
#    mutant M9: blame_rev's `else None` -> `else {}`                                       measured: KILLED; 1 of 69 checks BAD: c4d_at_tree_blame_VOID
CTL_ENV="GXSEC=$SEC" CTL_ARGS="--at=HEAD^{tree}" ctl c4d_at_tree_blame_VOID 2 GHOST_ROUNDS_VOID "git blame HEAD^{tree} -- CHANGELOG.md failed in"
absent c4d_at_tree_blame_VOID GHOST_ROUNDS_PASS
absent c4d_at_tree_blame_VOID GHOST_ROUNDS_FAIL

echo "== 5. the census HEAD (2632277f), the cutoff: everything already in the file is archived, nothing fails"
CTL_ENV="GXSEC=$SEC" CTL_ARGS="--at=2632277f --list" ctl c5_HEAD_subject 0 GHOST_ROUNDS_PASS "13 archived"
CTL_ENV="GXSEC=$SEC" CTL_ARGS="--at=2632277f --list --scope=all" ctl c5_HEAD_all 0 GHOST_ROUNDS_PASS "184 archived"
CTL_ENV="GXSEC=$SEC" CTL_ARGS="--at=2632277f --list --rule=date --scope=all" ctl c5_HEAD_date_all 0 GHOST_ROUNDS_PASS "268 archived"

echo "== 6. a round block not yet committed lands TODAY (file mode, a scratch git repo)"
G=$WORK/gitrepo6; rm -rf "$G"; mkdir -p "$G"
( cd "$G" && git init -q . &&
  printf '# `#900` (2026-11-01) -- `ghostclosed`: an old round, already committed\n\nText.\n' > CHANGELOG.md &&
  cm add CHANGELOG.md && cm commit -q -m old &&
  { printf '# `#903` (ghostopen): a round being committed right now, with no date in its header\n\nThe fix landed.\n\n'; cat CHANGELOG.md; } > CHANGELOG.new && mv CHANGELOG.new CHANGELOG.md )
python - "$S/synth_ledger.json" "$G/ledger_wb.json" <<'PYEOF'
import io, json, sys
d = json.load(io.open(sys.argv[1], encoding="utf-8"))
for r in d["rows"]:
    if r["id"] == "ghostopen":
        r["state_note"] = "[#903, today: the fix landed; the row stays open for the regress review.]"
io.open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1))
PYEOF
CTL_ENV="GXLEDGER=$S/synth_ledger.json GXCHANGELOG=$G/CHANGELOG.md GXGHOST_CUTOFF=2026-11-04" CTL_ARGS="" ctl c6a_uncommitted_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen" "dated by blame"
CTL_ENV="GXLEDGER=$G/ledger_wb.json GXCHANGELOG=$G/CHANGELOG.md GXGHOST_CUTOFF=2026-11-04" CTL_ARGS="" ctl c6b_uncommitted_writeback_PASS 0 GHOST_ROUNDS_PASS

echo "== 7. a sha in \`commits\` is not a write-back: 2951694f, the last ledger commit before the 2026-10-18 repair"
CTL_ENV="GXSEC=$SEC GXGHOST_CUTOFF=2026-09-11" CTL_ARGS="--at=2951694f" ctl c7a_2951694f_default 1 GHOST_ROUNDS_FAIL "GHOST    mapledmaaddr           in work  named in the header of #528" "GHOST    xscaleinten            in work  named in the header of #526" "GHOST    ppcrlwimiwidth         in work  named in the header of #527" "GHOST    ppcrldimimask          in work  named in the header of #527"
CTL_ENV="GXSEC=$SEC GXGHOST_CUTOFF=2026-09-11" CTL_ARGS="--at=2951694f --accept-commits" ctl c7b_2951694f_accept_commits 1 GHOST_ROUNDS_FAIL
absent c7b_2951694f_accept_commits "named in the header of #528"
absent c7b_2951694f_accept_commits "named in the header of #527"
absent c7b_2951694f_accept_commits "named in the header of #526"

echo "== 8. NEW: the installed checker reads the INDEX -- a repo laid out like GXEMUL-SEC, the checker at tools/pipeline/"
R=$WORK/indexrepo; rm -rf "$R"; mkdir -p "$R/tools/pipeline"
cp "$C" "$R/tools/pipeline/check_ghost_rounds.py"
cp "$S/synth_ledger.json" "$R/tools/pipeline/ledger.json"
( cd "$R" && git init -q . &&
  printf '# `#900` (2026-11-01) -- `ghostclosed`: an old round, already committed\n\nText.\n' > CHANGELOG.md &&
  cm add -A && cm commit -q -m base )
NEWB='# `#904` (ghostopen): a round being committed, its row not written back\n\nThe fix landed.\n\n'
X="GXGHOST_CUTOFF=2026-11-04"
C=$R/tools/pipeline/check_ghost_rounds.py        # the copy INSIDE the repo: its own location makes $R the repo it reads
#  8a: the new block STAGED, the ledger untouched -> FAIL, and the run says it read the index
( cd "$R" && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md && cm add CHANGELOG.md )
CTL_ENV="$X" CTL_ARGS="" ctl c8a_staged_block_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen" "read: the index of"
#  8b: the block only in the WORKING TREE (unstaged) -> the index has no new block: PASS; --worktree sees it: FAIL
( cd "$R" && cm reset -q && git diff --cached --quiet )
CTL_ENV="$X" CTL_ARGS="" ctl c8b_worktree_only_PASS 0 GHOST_ROUNDS_PASS "read: the index of"
CTL_ENV="$X" CTL_ARGS="--worktree" ctl c8c_worktree_flag_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen"
#  8d: block AND the write-back both staged -> PASS
python - "$R/tools/pipeline/ledger.json" <<'PYEOF'
import io, json, sys
d = json.load(io.open(sys.argv[1], encoding="utf-8"))
for r in d["rows"]:
    if r["id"] == "ghostopen":
        r["state_note"] = "[#904, today: landed; the row stays open for the regress review.]"
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1))
PYEOF
( cd "$R" && cm add CHANGELOG.md tools/pipeline/ledger.json )
CTL_ENV="$X" CTL_ARGS="" ctl c8d_staged_writeback_PASS 0 GHOST_ROUNDS_PASS
#  8e: block staged, the write-back ONLY in the working-tree ledger -> the index ledger lacks it: FAIL
( cd "$R" && cm reset -q -- tools/pipeline/ledger.json )
CTL_ENV="$X" CTL_ARGS="" ctl c8e_writeback_unstaged_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen"
#  back to HEAD in the index and the working tree, for the review's legs
( cd "$R" && cm reset -q && git checkout -q -- . && git diff --quiet && git diff --cached --quiet )
RW=$(cd "$R" && (pwd -W 2>/dev/null || pwd))
#  REVIEW (M2): a STAGED block whose header carries a date BEFORE the cutoff lands TODAY (blame: the all-zero sha), so it
#  FAILs -- the header date never decides when a block landed while blame can.
#    mutant M2: landed = date if src == "header" else (bdate or UNDATED)                  measured: KILLED; 1 of 69 checks BAD: c8f_staged_dated_FAIL
( cd "$R" && { printf '# `#905` (2026-11-01) -- `ghostopen`: a round dated before the cutoff in its header, committed now\n\nText.\n\n'; git show HEAD:CHANGELOG.md; } > CHANGELOG.md && cm add CHANGELOG.md )
CTL_ENV="$X GXGHOST_TODAY=2026-11-06" CTL_ARGS="" ctl c8f_staged_dated_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen" "landed 2026-11-06"
( cd "$R" && cm reset -q && git checkout -q -- . )
#  REVIEW (M5): `git commit -a` and partial commits hand the hook a TEMPORARY index (GIT_INDEX_FILE); a block staged only
#  there must FAIL under it, and the real index (no block) must PASS.  This MEASURES QP1, which three seats ratified.
#    mutant M5: git() runs with GIT_INDEX_FILE removed from its environment               measured: KILLED; 5 of 69 checks BAD: c8g_tempindex_FAIL c8h_index_unreadable_VOID c9d_hook_tempindex_FAIL c9e_hook_void_FAIL
( cd "$R" && cp .git/index .git/index.ghost && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md &&
  GIT_INDEX_FILE="$RW/.git/index.ghost" cm add CHANGELOG.md && git diff --cached --quiet )
CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.ghost $X" CTL_ARGS="" ctl c8g_tempindex_FAIL 1 GHOST_ROUNDS_FAIL "GHOST    ghostopen" "read: the index of"
CTL_ENV="$X" CTL_ARGS="" ctl c8g2_realindex_PASS 0 GHOST_ROUNDS_PASS "read: the index of"
( cd "$R" && git checkout -q -- . && rm -f .git/index.ghost )
#  REVIEW (the repair): an index git cannot read is VOID -- never the working copies (which here hold a block that would
#  FAIL), and never a PASS.
#    the code before the repair (a `note:`, then the working copies)                    measured: KILLED; 15 of 69 checks BAD: c4d_at_tree_blame_VOID c8h_index_unreadable_VOID c8i_blame_unreadable_VOID c8j_blame_incomplete_VOID c8k_at_blame_incomplete_VOID c8l_ledger_unstaged_VOID c8m_changelog_unstaged_VOID c9e_hook_void_FAIL
( cd "$R" && printf 'not an index\n' > .git/index.bogus && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md )
CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.bogus $X" CTL_ARGS="" ctl c8h_index_unreadable_VOID 2 GHOST_ROUNDS_VOID "cannot be read"
absent c8h_index_unreadable_VOID GHOST_ROUNDS_PASS
absent c8h_index_unreadable_VOID GHOST_ROUNDS_FAIL
( cd "$R" && git checkout -q -- . && rm -f .git/index.bogus )
#  REVIEW 3 (the closing pass, CLOSE_RULING.md s.1): the index guard tests its TWO reads separately (`lb is None or cb is
#  None`), so "show fails" is a {ok,fail} x {ok,fail} product; c8h holds only the both-fail cell, from which a ONE-SIDED
#  working-copy fallback cannot be seen (measured: 63/63 for each side).  Real git writes each mixed cell with one `git rm --cached`.
#    mutant M15: `lb = lb if lb is not None else open(LEDGER, "rb").read()` after the index git_show line    measured: KILLED; 2 of 69 checks BAD: c8l_ledger_unstaged_VOID
#    mutant M16: `cb = cb if cb is not None else open(CHANGELOG, "rb").read()` after the same line           measured: KILLED; 2 of 69 checks BAD: c8m_changelog_unstaged_VOID
( cd "$R" && cm rm -q --cached tools/pipeline/ledger.json && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md && cm add CHANGELOG.md )
python - "$S/synth_ledger.json" "$R/tools/pipeline/ledger.json" <<'PYEOF'
import io, json, sys
d = json.load(io.open(sys.argv[1], encoding="utf-8"))
for r in d["rows"]:
    if r["id"] == "ghostopen":
        r["state_note"] = "[#904, today: landed.]"      # the WORKING copy records the round; the index has no ledger at all
io.open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1))
PYEOF
CTL_ENV="$X" CTL_ARGS="" ctl c8l_ledger_unstaged_VOID 2 GHOST_ROUNDS_VOID "cannot be read"
absent c8l_ledger_unstaged_VOID GHOST_ROUNDS_PASS
absent c8l_ledger_unstaged_VOID GHOST_ROUNDS_FAIL
( cd "$R" && cm reset -q && git checkout -q -- . )
( cd "$R" && cm rm -q --cached CHANGELOG.md && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md )
CTL_ENV="$X" CTL_ARGS="" ctl c8m_changelog_unstaged_VOID 2 GHOST_ROUNDS_VOID "cannot be read"
absent c8m_changelog_unstaged_VOID GHOST_ROUNDS_PASS
absent c8m_changelog_unstaged_VOID GHOST_ROUNDS_FAIL
( cd "$R" && cm reset -q && git checkout -q -- . )
#  REVIEW (the repair): a blame git cannot do is VOID -- never the header dates.  This repo has NO COMMIT yet, so
#  `git blame` fails ("no such ref: HEAD") while `git show :<path>` reads the staged files; the staged block's header
#  says 2026-11-01, which header dating would ARCHIVE.  (A HEAD lacking only CHANGELOG.md does not do it: blame
#  --contents then succeeds and dates every line TODAY -- measured while building this leg.)
#    the code before the repair (blame -> {}, the header date trusted)                   measured: KILLED; 15 of 69 checks BAD: c4d_at_tree_blame_VOID c8h_index_unreadable_VOID c8i_blame_unreadable_VOID c8j_blame_incomplete_VOID c8k_at_blame_incomplete_VOID c8l_ledger_unstaged_VOID c8m_changelog_unstaged_VOID c9e_hook_void_FAIL
#  REVIEW 2: the message is the FAILURE's ("failed in"), so blame_contents returning {} -- VOID too since complete(),
#  as "dated 0 of N lines" -- is told apart (this leg wanted only "blame" before, which that edit would have passed).
#    mutant M14: blame_contents' `else None` -> `else {}`                                  measured: KILLED; 1 of 69 checks BAD: c8i_blame_unreadable_VOID
R2=$WORK/noblamerepo; rm -rf "$R2"; mkdir -p "$R2/tools/pipeline"
cp "$C0" "$R2/tools/pipeline/check_ghost_rounds.py"
cp "$S/synth_ledger.json" "$R2/tools/pipeline/ledger.json"
( cd "$R2" && git init -q . &&
  printf '# `#907` (2026-11-01) -- `ghostopen`: the first CHANGELOG.md, staged, its header dated before the cutoff\n\nText.\n' > CHANGELOG.md &&
  cm add -A && git show :CHANGELOG.md > /dev/null )
C=$R2/tools/pipeline/check_ghost_rounds.py
CTL_ENV="$X" CTL_ARGS="" ctl c8i_blame_unreadable_VOID 2 GHOST_ROUNDS_VOID "git blame --contents" "failed in"
absent c8i_blame_unreadable_VOID GHOST_ROUNDS_PASS
#  REVIEW 2 (A1, the class cell): a blame that EXITS 0 and dates fewer lines than the file holds is VOID -- never the
#  header dates.  The real-git writer of that cell: a repository whose object format is SHA-256, whose porcelain lines
#  carry 64-hex shas the parser (40-hex) does not read, so the map comes back EMPTY with rc 0.  The staged block's
#  header says 2026-11-01, which header dating would ARCHIVE (a PASS before complete()).  c8j: index mode; c8k: --at.
#    mutant M10: complete()'s `if len(bl) != nlines(cb):` -> `if False:`                   measured: KILLED; 4 of 69 checks BAD: c8j_blame_incomplete_VOID c8k_at_blame_incomplete_VOID
R3=$WORK/sha256repo; rm -rf "$R3"; mkdir -p "$R3/tools/pipeline"
cp "$C0" "$R3/tools/pipeline/check_ghost_rounds.py"
cp "$S/synth_ledger.json" "$R3/tools/pipeline/ledger.json"
( cd "$R3" && git init -q --object-format=sha256 . &&
  printf '# `#900` (2026-11-01) -- `ghostclosed`: an old round, already committed\n\nText.\n' > CHANGELOG.md &&
  cm add -A && cm commit -q -m base && [ "$(git rev-parse HEAD | wc -c)" = 65 ] &&
  { printf '# `#908` (2026-11-01) -- `ghostopen`: a round dated before the cutoff in its header, committed now\n\nText.\n\n'; git show HEAD:CHANGELOG.md; } > CHANGELOG.md &&
  cm add CHANGELOG.md )
R3W=$(cd "$R3" && (pwd -W 2>/dev/null || pwd))
C=$R3/tools/pipeline/check_ghost_rounds.py
CTL_ENV="$X" CTL_ARGS="" ctl c8j_blame_incomplete_VOID 2 GHOST_ROUNDS_VOID "dated 0 of"
absent c8j_blame_incomplete_VOID GHOST_ROUNDS_PASS
CTL_ENV="GXSEC=$R3W $X" CTL_ARGS="--at=HEAD" ctl c8k_at_blame_incomplete_VOID 2 GHOST_ROUNDS_VOID "dated 0 of"
absent c8k_at_blame_incomplete_VOID GHOST_ROUNDS_PASS
C=$R/tools/pipeline/check_ghost_rounds.py

echo "== 9. REVIEW: section P2 ITSELF -- its block cut from HOOK and run as the hook runs it, in the index repo"
P2=$WORK/p2_block.sh
awk '/^say ""; say "P2\. /{f=1} f{print} f && /^fi$/{exit}' "$HOOK" > "$P2"
if grep -q GHOSTCHK "$P2" && [ "$(tail -1 "$P2")" = "fi" ]; then
	pass=$((pass+1)); printf 'ok    %-34s %s lines cut from %s\n' p2_block_cut "$(wc -l < "$P2")" "$(basename "$HOOK")"
else
	bad=$((bad+1)); printf 'BAD   %-34s no section P2 block in %s\n' p2_block_cut "$HOOK"
fi
#  REVIEW 2 (A6, A8): the harness COUNTS as the hook does -- `bad` increments `fail` (the hook's own `bad` at its
#  helpers) and the count is printed after the block -- and runs under `set -u`, as the hook does.  A `bad` that
#  printed and did not count would let a sole P2 failure end PRECOMMIT_PASS while every leg read HOOK-FAIL.
#    mutant M13: P2's `bad "A ROUND BLOCK'S ROWS ..."` run in a subshell                   measured: KILLED; 3 of 69 checks BAD: c9a_hook_mention_rule c9b_hook_env_cleared c9d_hook_tempindex_FAIL
{
	echo 'set -u'
	echo 'fail=0'
	echo 'say () { printf "%s\n" "$*"; }'
	echo 'good () { printf "HOOK-ok    %s\n" "$*"; }'
	echo 'bad () { fail=$((fail+1)); printf "HOOK-FAIL  %s\n" "$*"; }'
	echo 'warn () { printf "HOOK-WARN  %s\n" "$*"; }'
	echo 'missing () { printf "HOOK-MISSING  %s\n" "$*"; }'
	echo 'cd "$1" || exit 9'
	echo '_HERE=$1/tools'
	echo '. "$2"'
	echo 'printf "HOOK-fail=%s\n" "$fail"'
} > "$WORK/p2_harness.sh"
hookctl () {   # name want(ok|FAIL) [must-contain ...]; env from CTL_ENV
	local name=$1 want=$2; shift 2
	env $CTL_ENV bash "$WORK/p2_harness.sh" "$R" "$P2" > "$O/$name.out" 2>&1
	local ok=1
	grep -q "^HOOK-$want " "$O/$name.out" || ok=0
	for need in "$@"; do grep -q -- "$need" "$O/$name.out" || { ok=0; echo "    missing: $need"; }; done
	if [ $ok = 1 ]; then pass=$((pass+1)); printf 'ok    %-34s HOOK-%s\n' "$name" "$want"
	else bad=$((bad+1)); printf 'BAD   %-34s (want HOOK-%s) %s\n' "$name" "$want" "$(grep -m1 '^HOOK-' "$O/$name.out")"; fi
}
SAMEDAY='# `#906` (2026-11-06) -- `ghostsameday`: shipped; its row carries only an entry dated this day, and no #906\n\nThe fix landed.\n\n'
( cd "$R" && { printf "$SAMEDAY"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md && cm add CHANGELOG.md )
#  REVIEW (M1): the hook's own rule.  The row's only entry is dated the block's day, so ONLY the mention rule fails it.
#    mutant M1: P2's python line gains --rule=date                                        measured: KILLED; 2 of 69 checks BAD: c9a_hook_mention_rule c9b_hook_env_cleared
CTL_ENV="" hookctl c9a_hook_mention_rule FAIL "GHOST    ghostsameday" "^HOOK-fail=1$"
#  REVIEW (D2): an exported override must not reach the checker.  GXLEDGER names a ledger that DOES record #906; read,
#  it would make the run read files other than the index, and PASS.
#    mutant M7: P2's line without its `env -u GX...` prefix                               measured: KILLED; 1 of 69 checks BAD: c9b_hook_env_cleared
python -c "
import io, json, sys
d = json.load(io.open(sys.argv[1], encoding='utf-8'))
for r in d['rows']:
    if r['id'] == 'ghostsameday':
        r['state_note'] = '[#906: landed.]'
io.open(sys.argv[2], 'w', encoding='utf-8', newline='').write(json.dumps(d, indent=1))
" "$S/synth_ledger.json" "$WORK/ledger_906.json"
WW=$(cd "$WORK" && (pwd -W 2>/dev/null || pwd))
CTL_ENV="GXLEDGER=$WW/ledger_906.json" hookctl c9b_hook_env_cleared FAIL "GHOST    ghostsameday" "^HOOK-fail=1$"
#  REVIEW (the token): a checker that exits 0 WITHOUT the PASS token is not a pass.
#    mutant M8: P2's line without `&& ... grep -q '^GHOST_ROUNDS_PASS'`                    measured: KILLED; 1 of 69 checks BAD: c9c_hook_rc0_no_token
cp "$R/tools/pipeline/check_ghost_rounds.py" "$WORK/checker.keep"
echo 'print("a checker that exits 0 and says nothing")' > "$R/tools/pipeline/check_ghost_rounds.py"
CTL_ENV="" hookctl c9c_hook_rc0_no_token FAIL "reached no verdict" "^HOOK-fail=1$"
cp "$WORK/checker.keep" "$R/tools/pipeline/check_ghost_rounds.py"
( cd "$R" && cm reset -q && git checkout -q -- . )
#  REVIEW 2 (G6, the de-escalation ACCEPT ROW for P2's `env -u`): the names NOT cleared must still reach the checker,
#  and GIT_INDEX_FILE is the load-bearing one -- `git commit -a` and a partial commit hand the hook a TEMPORARY index,
#  and a block staged only there must FAIL at the hook as it does at the checker (c8g).
#    mutant M11: P2's line clears GIT_INDEX_FILE too                                       measured: KILLED; 2 of 69 checks BAD: c9d_hook_tempindex_FAIL c9e_hook_void_FAIL
( cd "$R" && cp .git/index .git/index.ghost && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md &&
  GIT_INDEX_FILE="$RW/.git/index.ghost" cm add CHANGELOG.md && git diff --cached --quiet )
CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.ghost" hookctl c9d_hook_tempindex_FAIL FAIL "GHOST    ghostopen" "^HOOK-fail=1$"
( cd "$R" && git checkout -q -- . && rm -f .git/index.ghost )
#  REVIEW 2 (G7, CLAIM -> ROW for "it is VOID -- a hard FAIL below" in P2's comment): a VOID verdict is a hard FAIL at
#  the hook -- an index git cannot read, c8h's setup, the working tree holding a block that would FAIL.
#    mutant M12: an `elif ... '^GHOST_ROUNDS_VOID' ... good` before P2's FAIL branch        measured: KILLED; 1 of 69 checks BAD: c9e_hook_void_FAIL
( cd "$R" && printf 'not an index\n' > .git/index.bogus && { printf "$NEWB"; git show HEAD:CHANGELOG.md; } > CHANGELOG.md )
CTL_ENV="GIT_INDEX_FILE=$RW/.git/index.bogus" hookctl c9e_hook_void_FAIL FAIL "reached no verdict" "GHOST_ROUNDS_VOID" "^HOOK-fail=1$"
( cd "$R" && git checkout -q -- . && rm -f .git/index.bogus )

echo
echo "CONTROLS: $pass ok, $bad BAD"
echo "CONTROLS_DONE"
exit $(( bad > 0 ))
