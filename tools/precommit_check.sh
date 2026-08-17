#!/bin/bash
#  PRE-COMMIT REWORK CHECK.  Run from git-bash before every commit:
#      bash /c/DocumentNoSnc/cc/GXEMUL/precommit_check.sh ["commit message file"]
#
#  WHY THIS EXISTS, measured on 2026-08-14: SEVEN OF FIFTEEN COMMITS THAT DAY
#  (47%) FIXED THE COMMIT IMMEDIATELY BEFORE THEM -- #407->#405, #409->#408,
#  #411->#410, #413->#412, #415->#414, #417->#416, #406->#404.  Raw throughput
#  was never the constraint; REWORK was.  Every one of those was caught later by
#  a gate or a seat, i.e. after the commit existed.
#
#  *** WHAT THIS CANNOT DO, said here so a green run is not read as more than it
#  is.  Of the three rework classes, only ONE is fully decidable by a script:
#    1. twin-tree propagation      -- FULLY mechanical (a cmp).  Check A.
#    2. a claim that outruns the diff -- PARTIALLY mechanical.  Whether a file is
#       named in the message but absent from the diff is decidable; whether a
#       SENTENCE IS TRUE is not.  Checks C and D.
#    3. a detector that does not test what it names -- NOT mechanical at all.
#       Only a mutation run settles it, and the mutant is a human choice.
#       Check E can only ask whether one was RECORDED.
#  A green run means the decidable things were checked.  It is not evidence
#  about correctness. ***
set -u
#  ROOT IS DERIVED FROM THIS SCRIPT'S OWN LOCATION, not hardcoded.  This file lives in
#  GXEMUL-SEC/tools/, so the project root is two levels up.  It used to carry an absolute
#  path, which is only half-tracked: a fresh clone anywhere else would have run against
#  whatever happened to be at the old address, or nothing.  $GXROOT overrides for testing.
_HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ROOT="${GXROOT:-$(cd "$_HERE/../.." && pwd)}"
SEC=$ROOT/GXEMUL-SEC
EST=$ROOT/est
BLD=$ROOT/build
MSGFILE=${1:-}
fail=0
warn=0

say  () { printf '%s\n' "$*"; }
bad  () { fail=$((fail+1)); printf '  FAIL  %s\n' "$*"; }
soft () { warn=$((warn+1)); printf '  WARN  %s\n' "$*"; }
good () { printf '  ok    %s\n' "$*"; }

cd "$SEC" || { say "no repo at $SEC"; exit 9; }
# ---------------------------------------------------------------- F
#  THE PASS-2 RECEIPT, AND THIS IS THE SECOND VERSION BECAUSE THE FIRST COULD NOT FIRE.
#
#  R6 shipped without a pass-2 review of its diff.  That was caught externally,
#  recorded, and corrected -- and R7 then did exactly the same thing one round
#  later.  So a mechanical check was written.  A pass-2 seat then MEASURED that
#  the check itself was vacuous: it sat below the "nothing staged" early exit, so
#  on a clean post-commit tree -- the only state in which a missed pass 2 is
#  actually detectable -- the script returned before reaching it.  It also keyed
#  on source mtime, which any checkout or copy moves, and accepted any panel
#  directory as evidence without asking what that panel reviewed.
#
#  A check that cannot fail is worse than no check, because it reassures.  This
#  version fixes all four faults:
#    * it runs BEFORE the early exit, so a clean tree still gets checked;
#    * it asks about the PREVIOUS src-touching COMMIT, not the working tree --
#      you cannot be required to have reviewed the commit you are about to make,
#      but you can be required to have reviewed the last one;
#    * the receipt is keyed to a SHA in a TRACKED file, which is attributable and
#      survives a different machine, where an mtime is neither;
#    * it is HARD, because both misses were invisible rather than argued.
#  It still cannot judge whether a review was any good.  Nothing mechanical can.
#  It guarantees one was RECORDED against the commit it reviewed, which is the
#  enforceable half.
#  ---------------------------------------------------------------------------
#  G. EVERY SEAT THAT ANSWERED IN A CITED PANEL MUST BE RECORDED.
#
#  The dashboard renders three different things as the same blank cell: a seat
#  never fired, a seat that FAILED, and a seat that ANSWERED AND NOBODY RECORDED
#  IT.  The third is the dangerous one -- the round reads as reviewed while a real
#  review sits unread on disk -- and it happened THREE TIMES:
#
#    panel_20260815_202720 / kimi  192 KB.  Reading it found that gate 2 has ZERO
#                                  coverage of dev_rtc.c, so #429's fix can be
#                                  reverted and the gate stays green.
#    panel_20260816_024410 / kimi   99 KB.  Reading it found that diff_m8invread's
#                                  spy counts CALLBACK calls, so a mutant clearing
#                                  the dyntrans arrays directly passes all 21 rows.
#    panel_20260815_020427 / six seats.  Reading them found a docstring in
#                                  drive_guest.py describing behaviour the code
#                                  deliberately does not have, contradicted by the
#                                  docstring thirty lines below it.
#
#  The owner caught the first two BY EYE, from blank cells on the dashboard.  A
#  check a human has to remember is a check that eventually does not happen -- so
#  this is the mechanical version, and it found the third one within a minute of
#  being written.  HARD, because all three were invisible rather than argued.
#
#  Scope is deliberately "panels the ledger has already cited": citing a dir is the
#  act that puts it in scope.  A round that cites no panel at all is caught by F.
#  ---------------------------------------------------------------------------
#  H. EVERY STAGE RUNS THE FULL PANEL BEFORE THE ROUND MOVES ON.
#
#  Owner directive 2026-08-16, and it SUPERSEDES the carrier's older "ONE full panel
#  per ROUND, pass 2 = codex + Opus".  That rule was written when Grok's free tier
#  was dead and Kimi was quota-dead; both are healthy now and all seven scriptable
#  seats answered the last three panels.  The only live constraint is the Ollama
#  seats' ~20-minute 429 window, which real stages already exceed.
#
#  If a seat cannot be run, the round STOPS AND THE OWNER IS ASKED.  Degrading
#  quietly is precisely what this replaces -- and note G alone would not catch it:
#  G verifies that a seat which ANSWERED was recorded, not that the seat was FIRED.
#  ---- I ---------------------------------------------------------------------------
#  Owner directive 2026-08-17: "make sure to gate and queue up any fable work; don't skip it."
#
#  H proves a stage did not proceed short.  It does NOT prove that the work a short stage
#  still owes was ever written down: H reads a HELD marker as "waiting", and waiting is
#  indistinguishable from forgotten once the round scrolls out of view.  On its first run
#  this check found a closed row (`m8online`) whose regression review had never happened
#  and was recorded nowhere -- and, next to it, two rows that looked identical and had
#  merely lost their attribution.  A held job and a dropped job must not look alike.
say ""; say "I. flagship work that is owed is written down"
FQCHK=$_HERE/pipeline/check_fable_queue.py
if [ ! -f "$FQCHK" ]; then
	warn "check_fable_queue.py MISSING -- owed flagship work NOT verified"
elif out=$(python "$FQCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'FABLE_QUEUE_PASS|check_fable_queue:' | tr '
' ' ')"
else
	bad "FLAGSHIP WORK IS OWED AND NOT QUEUED:"
	printf '%s
' "$out" | sed 's/^/          /'
fi

say ""; say "H. every stage ran the full panel"
STAGECHK=$_HERE/pipeline/check_stage_panels.py
if [ ! -f "$STAGECHK" ]; then
	warn "check_stage_panels.py MISSING -- stage completeness NOT verified"
elif out=$(python "$STAGECHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'STAGE_PANELS_PASS|check_stage_panels:' | tr '
' ' ')"
else
	bad "A STAGE MOVED ON WITHOUT THE FULL PANEL:"
	printf '%s
' "$out" | sed 's/^/          /'
fi

say ""; say "G. every seat that answered in a cited panel is recorded"
SEATCHK=$_HERE/pipeline/check_seats_read.py
if [ ! -f "$SEATCHK" ]; then
	warn "check_seats_read.py MISSING -- seat-recording NOT verified"
elif out=$(python "$SEATCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'SEATS_READ_PASS|substantial answers' | tr '
' ' ')"
else
	bad "SEATS THAT ANSWERED ARE RECORDED NOWHERE:"
	printf '%s
' "$out" | sed 's/^/          /'
	bad "Read them and add a ledger entry.  If a seat truly had nothing to say,"
	bad "record THAT explicitly -- a blank cell and a seat failure must not look alike."
fi

say ""; say "F. pass-2 receipt for the previous src-touching commit"
LEDGER=$SEC/regress/pass2_ledger.tsv
PREV=$(git -C "$SEC" log -1 --format=%H -- 'src/**' 2>/dev/null || true)
if [ -z "$PREV" ]; then
	good "no src-touching commit in history"
elif git -C "$SEC" log -1 --format=%s "$PREV" | grep -qiE 'pass 2'; then
	good "$(git -C "$SEC" log -1 --format=%h "$PREV") is itself a pass-2 commit"
elif [ -f "$LEDGER" ] && awk -v p="$PREV" '!/^#/ && $1 != "" { if (index(p, $1) == 1) found=1 } END { exit !found }' "$LEDGER"; then
	#  PREFIX match, not equality: git gives a FULL sha and a human writing the receipt
	#  will naturally paste the SHORT one.  The first version compared them with grep -x
	#  and could therefore NEVER match -- caught by running the positive control instead
	#  of only the negative one.  A check that always fails is a different bug from one
	#  that always passes, and just as useless.
	good "pass-2 receipt found for $(git -C "$SEC" log -1 --format=%h "$PREV")"
	grep "^$PREV" "$LEDGER" | sed 's/^/          /'
else
	bad "NO PASS-2 RECEIPT for $(git -C "$SEC" log -1 --format='%h %s' "$PREV")"
	bad "A round owes a pass 2 on its own diff.  R6 and R7 both shipped without one,"
	bad "the second time one round after the first was caught and written down."
	bad "Run it, then append a line to regress/pass2_ledger.tsv."
fi

CHANGED=$(git status --porcelain | awk '{print $2}')
[ -z "$CHANGED" ] && { say "nothing staged or modified -- nothing to check."; exit 0; }

say "=== #418-era PRE-COMMIT REWORK CHECK ==="
say "files in play:"; printf '    %s\n' $CHANGED

# ---------------------------------------------------------------- A
#  TWIN-TREE PROPAGATION.  est/ and GXEMUL-SEC differ by exactly five named
#  files plus SEC-only dev_ne2000.c; ANY OTHER src/ file must land byte-
#  identical in both.  #415 is a whole commit that exists because this was
#  skipped once -- and the gate that should have caught it named two files when
#  the truth was three, because an allowlist entry had gone stale.
say ""; say "A. twin-tree propagation (the #415 class -- FULLY mechanical)"
DIVERGENT_OK="src/include/misc.h src/devices/dev_ne2000.c"
for f in $CHANGED; do
	case "$f" in
	src/*) ;;
	*) continue ;;
	esac
	skip=0
	for d in $DIVERGENT_OK; do [ "$f" = "$d" ] && skip=1; done
	[ $skip = 1 ] && { good "$f (known-divergent, not compared)"; continue; }
	if [ ! -f "$EST/$f" ]; then
		soft "$f has no counterpart in est/ -- SEC-only?  Confirm deliberately."
	elif cmp -s "$SEC/$f" "$EST/$f"; then
		good "$f == est/"
	else
		bad "$f DIFFERS from est/ -- propagate it, then cmp against THE REPO (never a backup)"
	fi
done

# ---------------------------------------------------------------- B
#  BUILD-TREE STALENESS.  The build trees have NO VPATH, so an unpropagated
#  edit means you measured the wrong binary.  A .MUTANT sentinel means a prior
#  run left a tree mutated and NOTHING measured against it can be trusted.
say ""; say "B. build tree (measuring the wrong binary is worse than not measuring)"
if [ -f "$BLD/.MUTANT" ]; then
	bad ".MUTANT sentinel present in build/ -- restore from SEC and rebuild BEFORE trusting any measurement:"
	sed 's/^/          /' "$BLD/.MUTANT"
else
	good "no .MUTANT sentinel"
fi
for f in $CHANGED; do
	case "$f" in src/*) ;; *) continue ;; esac
	[ -f "$BLD/$f" ] || continue
	if cmp -s "$SEC/$f" "$BLD/$f"; then good "$f == build/"
	else bad "$f DIFFERS from build/ -- the measured binary is not this source"; fi
done

# ---------------------------------------------------------------- C
#  A MESSAGE THAT OUTRUNS ITS DIFF.  A commit message once claimed a citation
#  fix that no hunk made.  Write messages FROM THE DIFF.  Decidable half: a
#  source path named in the message that no hunk touches.
say ""; say "C. commit message vs diff (write messages FROM THE DIFF)"
if [ -n "$MSGFILE" ] && [ -f "$MSGFILE" ]; then
	for p in $(grep -oE '\b(src|regress|man)/[A-Za-z0-9_./-]+\.(c|h|sh|1)\b' "$MSGFILE" | sort -u); do
		if printf '%s\n' $CHANGED | grep -qx "$p"; then good "message cites $p, and the diff touches it"
		else bad "message cites $p but NO HUNK TOUCHES IT -- the claim outruns the diff"; fi
	done
	[ -z "$(grep -oE '\b(src|regress|man)/[A-Za-z0-9_./-]+\.(c|h|sh|1)\b' "$MSGFILE")" ] &&
		good "message cites no source paths (nothing to cross-check)"
else
	soft "no commit-message file passed -- check C skipped, NOT passed"
fi

# ---------------------------------------------------------------- D
#  ADDED CITATIONS AND SELF-INVALIDATING COUNTS.
#  D1: a `file.c:123` citation added by this diff whose line does not exist.
#      #414 invalidated a line-range citation elsewhere in the tree by moving
#      code; prefer naming the CONSTRUCT over the line.
#  D2: #418's rule -- a comment may not state a count of an identifier it also
#      spells.  Saying "occurs in exactly seven places" in a sentence naming
#      the token MADE THE COUNT EIGHT.
say ""; say "D. added citations and self-invalidating counts"
ADDED=$(git diff -U0 | grep '^+' | grep -v '^+++')
CITES=$(printf '%s\n' "$ADDED" | grep -oE '\b[a-z0-9_]+\.(c|h)\b:[0-9]+' | sort -u)
if [ -z "$CITES" ]; then good "no new file:line citations"; else
	for c in $CITES; do
		cf=${c%%:*}; cl=${c##*:}
		p=$(git ls-files "*/$cf" | head -1)
		if [ -z "$p" ]; then soft "cited $c -- file not found in the repo, check by hand"
		elif [ "$(wc -l < "$p")" -lt "$cl" ]; then bad "cited $c but $p has only $(wc -l < "$p") lines"
		else good "cited $c exists (READ THE LINE -- existence is not correctness)"; fi
	done
fi
#  D2 REFINEMENT, found by running this check against the very commit that
#  established its rule: all three hits were the OLD wrong claim QUOTED INSIDE
#  ITS OWN CORRECTION.  The rule is about ASSERTING a count, not MENTIONING
#  one -- a correction must be able to quote what it corrects, and a
#  strikethrough is a quotation by definition.  Assertion-vs-quotation is not
#  reliably decidable by regex, so this does not guess: a count inside quote
#  marks or `~~` becomes a SOFT warning that names the ambiguity, and a bare
#  one stays hard.  A check that cannot decide should hand the call back, which
#  is a different thing from a check that cannot fail.
COUNTS=$(printf '%s\n' "$ADDED" | grep -inE 'exactly (one|two|three|four|five|six|seven|eight|nine|ten|[0-9]+) (places|occurrences|sites)|occurs in [0-9]+ (places|occurrences|sites)|[0-9]+ occurrences of')
if [ -z "$COUNTS" ]; then good "no added occurrence counts"; else
	hard_hits=$(printf '%s\n' "$COUNTS" | grep -v '~~' | grep -v '"' || true)
	quoted=$(printf '%s\n' "$COUNTS" | grep -E '~~|"' || true)
	if [ -n "$hard_hits" ]; then
		bad "an added line ASSERTS an OCCURRENCE COUNT.  A record may not state a count of an identifier it also spells (#418) -- state the structural property instead:"
		printf '%s\n' "$hard_hits" | sed 's/^/          /' | head -5
	fi
	if [ -n "$quoted" ]; then
		soft "a count appears inside quote marks or strikethrough -- reads as a QUOTATION"
		soft "of a corrected claim, which is legitimate.  CONFIRM it is not a fresh assertion:"
		printf '%s\n' "$quoted" | sed 's/^/          /' | head -5
	fi
	[ -z "$hard_hits" ] && good "all count mentions are quoted/struck (see the warnings above)"
fi

# ---------------------------------------------------------------- E
#  DETECTOR HYGIENE.  Not a correctness check and does not pretend to be.
#  E1: a new regress/diff_*.c should carry an identity guard -- two files with
#      the same name once differed only by parent-directory case, and the stale
#      one encoded a REVERSED design decision.
#  E2: ONLY A MUTATION TEST PROVES A ROW REACHES THE CODE IT NAMES.  This can
#      only ask whether one was run; it cannot run it for you.
say ""; say "E. detector hygiene (NOT a correctness check)"
NEWDET=$(printf '%s\n' $CHANGED | grep -E '^regress/diff_.*\.c$' || true)
if [ -z "$NEWDET" ]; then good "no detector added or modified"; else
	for d in $NEWDET; do
		if grep -q 'IDENTITY' "$SEC/$d"; then good "$d carries an identity guard"
		else bad "$d has NO identity guard -- add a row asserting its own row count"; fi
	done
	soft "MUTATION RUN NOT VERIFIABLE HERE.  Confirm by hand: every new row killed at"
	soft "least one mutant, each kill NAMED ITS ROW, and no mutant merely failed to build"
	soft "(a build fault is a FAULT, not a detection)."
fi

say ""
say "=========================================================="
if [ $fail -gt 0 ]; then
	say "PRECOMMIT_FAIL   $fail hard, $warn soft"
	say "A hard failure is a rework class this project has already paid for."
	exit 1
fi
say "PRECOMMIT_PASS   0 hard, $warn soft"
say "Decidable checks passed.  This is NOT evidence about correctness --"
say "the mutation run and the truth of any claim remain yours."
exit 0
