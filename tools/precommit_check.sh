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
#  `warn` is called at the four "checker MISSING" branches and was DEFINED NOWHERE -- so a
#  missing pipeline checker printed `warn: command not found` on stderr and its gate was
#  silently disabled, which is the exact failure those branches exist to announce.  Measured
#  by renaming check_stage_panels.py and check_seats_read.py away: both gates vanished and the
#  run still said PRECOMMIT_PASS.
warn () { soft "$@"; }

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
#  ---- I2 --------------------------------------------------------------------------
#  I proves every HELD marker is NAMED IN THE QUEUE.  It cannot prove the queue's own summary
#  of those markers is CURRENT -- and that summary was maintained BY HAND until it drifted:
#  the entry said "nineteen held stages" when the ledger held THIRTY-FOUR.  Caught the moment
#  the section was mechanised, which is the whole argument for mechanising it.
#
#  gen_codex_wall.py DERIVES the row list and the count from the ledger's markers; the prose
#  stays human, because a generator that wrote the reasoning too is a generator nobody reads.
say ""; say "I2. the queue's held-stage summary matches the ledger"
WALLCHK=$_HERE/pipeline/gen_codex_wall.py
if [ ! -f "$WALLCHK" ]; then
	warn "gen_codex_wall.py MISSING -- the queue summary is NOT verified"
elif out=$(python "$WALLCHK" --check 2>&1); then
	good "$(printf '%s' "$out" | tr '\n' ' ')"
else
	bad "THE QUEUE'S HELD-STAGE SUMMARY IS STALE:"
	printf '%s\n' "$out" | sed 's/^/          /'
	say "          fix: python tools/pipeline/gen_codex_wall.py"
fi

#  ---- M (soft) ---------------------------------------------------------------------
#  CHECKPOINT.md carries its OWN staleness rule -- "if this HEAD disagrees with git log,
#  re-derive and rewrite this file; it has no other authority" -- and that rule was enforced
#  by NOTHING.  It drifted TWICE in one session: once by six commits, then again an hour after
#  being rewritten.  The second time was caught by a REVIEW SEAT, which opened the file against
#  its brief's own "do not read files" instruction and reported it before answering anything.
#
#  SOFT on purpose, and not out of timidity: the file is UNTRACKED and lives OUTSIDE the git
#  root, so a hard failure would block a fresh clone that has none, and block the legitimate
#  window between committing and rewriting it.  What it must not do is stay SILENT -- a stale
#  checkpoint is indistinguishable from a current one to the next session, which is how it once
#  cost 26 rounds.
say ""; say "M. the checkpoint names the actual HEAD"
CKPTCHK=$_HERE/pipeline/check_checkpoint.py
if [ ! -f "$CKPTCHK" ]; then
	warn "check_checkpoint.py MISSING -- checkpoint staleness NOT verified"
elif out=$(python "$CKPTCHK" 2>&1); then
	good "$(printf '%s' "$out" | head -1)"
else
	soft "$(printf '%s' "$out" | head -1)"
	printf '%s\n' "$out" | tail -n +2 | sed 's/^/          /'
fi

#  ---- N ---------------------------------------------------------------------------
#  A row that MEASURES A RESOURCE is only as good as the optimisation it pins.
#  diff_memory_rw.c asserts "the split is a loop, not recursion" by measuring stack growth --
#  and gcc 15.2.1 eliminates the tail call at -O2, so the recursion mutant measured 96 bytes
#  and THE ROW PASSED UNDER THE EXACT DEFECT IT EXISTED TO CATCH.  One flag makes it real:
#  loop 0 bytes, recursion 1,572,768.
#
#  Where `constblind` is a row following the CONSTANT, this is a row following the COMPILER.
#  The ledger asked for an AUDIT of every other resource-measuring row; the audit was done and
#  its answer is "memory_rw is the only one" -- but there were SEVEN differentials at the last
#  such audit and there are THIRTEEN now, and a five-seat panel voted to drop a row this week
#  on the strength of a stale audit sentence.  An audit is a claim with a shelf life.
#
#  HARD, because the baseline is clean: exactly one differential measures stack and it is
#  pinned.  The check reports its own blindness on every run -- it knows the stack-watermark
#  idiom ONLY, not "measures a resource" in general.
say ""; say "N. resource-measuring differentials pin their optimisation"
OPTCHK=$_HERE/pipeline/check_optpin.py
if [ ! -f "$OPTCHK" ]; then
	warn "check_optpin.py MISSING -- optimisation pinning NOT verified"
elif out=$(python "$OPTCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'OPTPIN_PASS' | tr '\n' ' ')"
	printf '%s\n' "$out" | grep -E '^  BLINDNESS' | sed 's/^/          /'
else
	bad "A RESOURCE-MEASURING ROW FOLLOWS THE COMPILER:"
	printf '%s\n' "$out" | grep -E 'OPTPIN_FAIL|pin: \*\*\*' | sed 's/^/          /'
fi

#  ---- O ---------------------------------------------------------------------------
#  THE LEDGER CAN MANUFACTURE AGREEMENT, AND FOR 52 ROWS IT DID.
#
#  Found 2026-08-20 by a reviewing seat: on `wdcnoirq`, five seat cells differed ONLY in the
#  leading seat name -- 378/379/379/383/382 bytes of the same paragraph.  THREE of those seats
#  had argued in their own files that the round was too narrow, and one had not mentioned the
#  opcode at issue at all.  The record showed five seats concurring.
#
#  Under the PIPELINE doctrine the ledger is the single source of truth, so this is not lost
#  detail -- it converts "six seats ANSWERED" into "six seats AGREED", which is precisely the
#  claim a panel exists to earn.  It is the seat-count analogue of the padded-column grep trap.
#
#  Complements G and H rather than duplicating them, and the three-way split is the point:
#  H asks whether the seat was FIRED, G whether an answer was RECORDED, O whether the recorded
#  answer is that seat's OWN.  A cell can pass both G and H while saying nothing the seat said.
#
#  FORWARD-ONLY BY DATE, not by allowlist: running it returned 57 clusters across 52 rows, so
#  a per-row exemption list would be the check switched off with extra steps.
say ""; say "O. each seat cell is that seat's own answer, not a stamped summary"
BOILCHK=$_HERE/pipeline/check_boilerplate.py
if [ ! -f "$BOILCHK" ]; then
	warn "check_boilerplate.py MISSING -- seat-cell independence NOT verified"
elif out=$(python "$BOILCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'BOILERPLATE_PASS' | tr '
' ' ')"
else
	bad "A POST-CUTOFF HARVEST STAMPED ONE NOTE ACROSS SEVERAL SEATS:"
	printf '%s
' "$out" | grep -E 'BOILERPLATE_FAIL|^  SHARED' | sed 's/^/          /'
fi

#  ---- P ---------------------------------------------------------------------------
#  A ROW THAT EXISTS ONLY IN THE LEDGER IS WORK A FRESH SESSION WILL NOT SEE.
#
#  This gap was hand-fixed one round ago -- f7eac43 is titled, in full, "OUTSTANDING_BUGS:
#  the R4-detector round's residuals, which went to the ledger and not here" -- and it
#  recurred IMMEDIATELY, at twenty-one open rows in a single day.  A catch-up commit is not
#  a fix for that; it is the same fix twice.  A check a human has to remember is a check
#  that eventually does not happen.
#
#  It complements the es438 direction rather than duplicating it, and this project has been
#  bitten from BOTH: es438 was a round with no LEDGER row, invisible to section H and the
#  dashboard; fixing it produced `lunafuse`, filed in OUTSTANDING_BUGS with no ledger row --
#  the defect reproduced one layer in.  P closes the other direction.
#
#  Only OPEN rows are required.  The bug file's own charter says resolved items are REMOVED,
#  not annotated, so demanding an entry for a closed row would push it toward the
#  accumulating-index failure that #270 exists to prevent.
say ""; say "P. every OPEN ledger row is findable in OUTSTANDING_BUGS.md"
BUGSYNC=$_HERE/pipeline/check_bugfile_sync.py
if [ ! -f "$BUGSYNC" ]; then
	warn "check_bugfile_sync.py MISSING -- ledger/bugfile sync NOT verified"
elif out=$(python "$BUGSYNC" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'BUGFILE_SYNC_PASS' | tr '
' ' ')"
else
	bad "AN OPEN ROW EXISTS ONLY IN THE LEDGER:"
	printf '%s
' "$out" | grep -E 'BUGFILE_SYNC_FAIL|^  MISSING' | sed 's/^/          /'
fi

#  ---- Q ---------------------------------------------------------------------------
#  THE MATRIX IS A GENERATED FILE AND NOTHING CHECKED THAT IT WAS REGENERATED.
#
#  matrix.html is rendered from ledger.json and is ALSO the source of the published
#  artifact, so a ledger edit committed without a regenerate ships a stale rendering AND
#  a stale artifact -- and the artifact is what the owner actually reads.  Every other
#  generated-file relationship in this harness is checked (J for the carrier copies, I2
#  for the queue summary); this one was not, purely because nobody had been bitten yet.
#
#  Deterministic and cheap: render to a temp path with --out and cmp.  It catches the
#  half that lives in the repo.  It CANNOT catch the other half -- whether the artifact
#  was republished -- because that lives outside git; that step stays manual, and this
#  comment is the reminder that it exists.
#  ONE spelling of the cutoff, passed into the heredoc rather than repeated in it.
#  A seat caught it spelled twice -- shell and Python -- which is the same drift the
#  TCR_UNIMPLEMENTED mask exists to prevent, one file over.
GRADING_CUTOFF_NOTE=2026-08-23
say ""; say "U. score claims match their gate pin"
#  Built after FOUR stale-score incidents in one session (#458 #459 #460 #461), all
#  the same shape: a round measures a detector at N rows, writes x/N into a gate
#  comment and a docstring, then GROWS the detector.  The pin gets updated because
#  the gate fails without it; the prose does not, because nothing reads it.
#
#  The fourth was caught by a seat that hit its usage limit MID-ANSWER and got one
#  sentence out.  That is the argument for mechanising it -- the catch depended on a
#  seat surviving long enough to say so.
#
#  HARD, and negative-controlled in both directions on the day it was written: the
#  #461 claim reintroduced makes it name the line and both stale numbers; restored,
#  it passes, with the file byte-identical.
SCORECHK=$_HERE/pipeline/check_score_claims.py
if [ ! -f "$SCORECHK" ]; then
	warn "check_score_claims.py MISSING -- stale score claims NOT verified"
elif out=$(python "$SCORECHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'SCORE_CLAIMS_PASS|check_score_claims:' | tr '
' ' ')"
	printf '%s\n' "$out" | grep -E '^  note ' | sed 's/^/        /'
	#  *** THE PROBE COUNT WAS A DISPLAY, NOT AN ASSERTION, SO NOTHING FAILED
	#  WHEN IT DROPPED. ***  A measuring seat showed the whole check can be
	#  disarmed for a probe with NO behaviour change at all: quote the pin
	#  literal (`"32"` instead of `32`) and regress/lib.sh:82 compares it as a
	#  string exactly as before, while this file silently stops governing that
	#  probe.  A two-word label or a hoisted variable does the same.
	#
	#  *** THIS WAS A RATCHET WITH A FLOOR OF 16 AND THE MEASURED VALUE WAS 18.
	#  A HAND-MAINTAINED RATCHET IS ITSELF AN UNRATCHETED NUMBER. ***
	#
	#  The old comment said "raise the floor when it rises, never lower it".  That
	#  instruction was silently missed TWICE -- the count went 16 -> 17 -> 18 while
	#  the floor stayed at 16 -- so two whole gate blocks carrying score-claim pins
	#  could have been deleted with this check still printing `good`.  Measured
	#  2026-08-26 by the seat answering `gateflr`.
	#
	#  So it is now an EQUALITY PIN, which is the idiom this harness already uses
	#  one level up: run.sh's GATE_MANIFEST, whose comment reads "Adding a gate
	#  means editing BOTH lines.  That is the point."  Equality fails in BOTH
	#  directions -- shrinking means a pin was lost; growing means a new probe
	#  arrived and the number becomes a deliberate edit rather than silent drift.
	#
	#  Cost, stated: one extra line to edit per new gated probe.  That trade has
	#  already been accepted twice here (GATE_MANIFEST, and SM_COVERED in
	#  gate_offline.sh), both times for exactly this reason.
	#
	#  A pin stops being SEEN when its literal is quoted (`"32"` for 32), when its
	#  label gains a word before the stem, or when the count moves to a variable --
	#  all of which leave the gate behaving identically.  That is why the count is
	#  asserted at all.
	#  19 -> 20 on 2026-08-28: `#489` wired gdrom_toclen_probe.py into gate_sh_rounding.sh
	#  with a literal denominator pin (`check "gdromtoclen rows run" ... 15`).  Raised
	#  DELIBERATELY, which is what the growth arm below asks for -- the count is the
	#  point, so it may not be nudged to silence a red.
	#  22 -> 23 on 2026-08-30: `sh4_bsc_width_probe.py` wired into gate_sh_rounding.sh with a
	#  literal denominator pin (`check "sh4bscwidth rows run" ... 13`), discharging the SECOND
	#  exemption of the day.  Raised DELIBERATELY -- and worth noting that discharging the
	#  FIRST one broke the wiring checker's own selftest, which had hardcoded the probe it was
	#  driving toward.  Progress is not supposed to red the harness; that was repaired in the
	#  same session and its mutant count is now pinned here too.
	#  21 -> 22 on 2026-08-30: `#496` wired gdrom_cond_probe.py into gate_sh_rounding.sh
	#  with a literal denominator pin (`check "gdromcond rows run" ... 20`).  Same
	#  deliberate raise, and the growth arm named this file and this line when it fired --
	#  which is the property that makes the check worth its noise.
	#  RAISED 23 -> 25 ON 2026-09-12, DELIBERATELY.  Two newly gated probes:
	#  wdc_altdigin_probe.py (#525, pinned in gate_sh_rounding.sh at 22 rows)
	#  and arm_bdt_probe.py (#524, pinned in gate_arm.sh at 43).  (This said 19
	#  and 39 -- both pins grew under their class closures after it was written.)
	#  The checker reads the WORKING TREE, so #524's pin counts here one commit
	#  before gate_arm.sh lands; #524 is the next commit.  Growth is a
	#  hard FAIL on purpose -- a floor that only catches SHRINKAGE goes slack
	#  every time the count rises, which is how this check once sat at 16
	#  against a real 18.
	#  RAISED 25 -> 28 ON 2026-09-12, DELIBERATELY.  Three newly SEEN pins: ppc_rlwimi_probe.py
	#  and ppc_rldimi_probe.py (#527, gate_ppc.sh, 28 and 29 rows), and xscale_inten_probe.py
	#  (#526, gate_arm.sh, 30) -- whose pin #526 shipped QUOTED ("30"), which this check's PIN
	#  regex cannot see, so for one commit the score-claims check guarded nothing there.  The
	#  gate behaved identically either way (a string compare); the literal is unquoted in #527.
	#  RAISED 28 -> 29 ON 2026-09-12, DELIBERATELY.  One newly gated probe: maple_dmaaddr_probe.py
	#  (#528, pinned UNQUOTED in gate_sh_rounding.sh at 37 rows).
	#  RAISED 29 -> 30 ON 2026-09-18, DELIBERATELY.  One newly gated probe: landisk_aux_probe.py
	#  (#533, pinned UNQUOTED in gate_sh_rounding.sh at 6 rows).
	#  RAISED 30 -> 31 ON 2026-09-24, DELIBERATELY.  One newly gated probe: fbctrl_port_probe.py
	#  (#549, pinned UNQUOTED in gate_mips_folds.sh at 117 rows).
	#  RAISED 31 -> 32 ON 2026-10-02, DELIBERATELY.  One newly gated probe: crime_width_probe.py
	#  (#529, pinned UNQUOTED in gate_arm.sh at 226 rows; the working tree had carried its bump since
	#  2026-09-13, re-telling this history with #529 in the 29 -> 30 slot).
	#  RAISED 32 -> 33 ON 2026-10-09, DELIBERATELY.  One newly gated probe: arm_msrmode_probe.py
	#  (#562, pinned UNQUOTED in gate_arm.sh at 47 rows).
	#  RAISED 33 -> 34 ON 2026-10-18, DELIBERATELY.  One newly gated probe: ppc_rldicl_probe.py
	#  (#565, pinned UNQUOTED in gate_ppc.sh at 24 rows).
	SCORE_CLAIMS_MANIFEST=34
	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
	if [ -z "$_spinned" ]; then
		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
	elif [ "$_spinned" -lt "$SCORE_CLAIMS_MANIFEST" ]; then
		bad "SCORE-CLAIM COVERAGE DROPPED: $_spinned probes pinned, manifest says $SCORE_CLAIMS_MANIFEST."
		bad "  A pin stops being seen when its literal is quoted, its label gains a"
		bad "  word before the stem, or the count moves to a variable -- all of which"
		bad "  leave the gate behaving identically.  Restore it; do not lower the manifest."
	elif [ "$_spinned" -gt "$SCORE_CLAIMS_MANIFEST" ]; then
		bad "SCORE-CLAIM COVERAGE GREW: $_spinned probes pinned, manifest says $SCORE_CLAIMS_MANIFEST."
		bad "  This is not a failure -- it means a new gated probe arrived.  Raise"
		bad "  SCORE_CLAIMS_MANIFEST to $_spinned in tools/precommit_check.sh, deliberately."
		bad "  Growth is caught on purpose: a floor that only catches shrinkage goes"
		bad "  slack every time the count rises, which is how this check sat at 16"
		bad "  against a real 18."
	else
		good "coverage pinned: $_spinned probes (manifest $SCORE_CLAIMS_MANIFEST, equality)"
	fi
else
	bad "STALE SCORE CLAIMS -- prose disagrees with the gate pin:"
	printf '%s
' "$out" | sed 's/^/          /'
	bad "  the pin is authoritative; fix the prose, or re-measure and fix both"
fi

say ""; say "T. seat outcomes: a CLOSED row's panel entries should be graded"
#  SOFT ON PURPOSE, and the reason matters.  A hard gate here would force a grade at
#  commit time, and a forced grade is a guessed grade -- which is precisely the recall
#  bias seat_scorecard.py exists to replace.  What this does is make coverage VISIBLE
#  every commit, so a seat's accuracy stops being something anyone has to remember.
#  Introduced 2026-08-22 after the ledger, with 1525 entries across nine seats, could
#  not answer "which seat is most accurate" -- it recorded participation and nothing
#  else.
#
#  *** OWNER DECISION 2026-08-22: STAYS SOFT, AND THE REVIEW IS SCHEDULED. ***
#  The pass-2 panel argued HARD, and the argument is good: a soft check ignored for six
#  months yields 1.3% coverage forever, which is indistinguishable from not having the
#  tool at all.  The counter is that a hard gate forces a grade at commit time, and a
#  forced grade is a guessed grade -- the exact bias this tool replaces.
#
#  Neither side is measured, so it is settled BY MEASUREMENT rather than by argument:
#  leave it soft and RE-CHECK COVERAGE AFTER ROUGHLY TEN MORE ROUNDS.  If it has not
#  moved off the floor, the panel was right and this goes hard -- preferably in the
#  closed-rows-only form, since closing a row is the moment its outcome is actually
#  known.  Write the coverage number down when you check, so the next reader sees a
#  trend instead of re-arguing it.
#
#  BASELINE AT THE DECISION: 1558 entries, 20 graded, 1.3%.
SCARD=$_HERE/pipeline/seat_scorecard.py
if [ ! -f "$SCARD" ]; then
	warn "seat_scorecard.py MISSING -- seat accuracy NOT tracked"
else
	#  Grep the WHOLE output, not a tail window.  The first version took `tail -n 8`
	#  and broke the same day: adding the self-graded disclosure banner pushed the
	#  summary line out of the window, so the check reported "produced no summary"
	#  about a tool that was working perfectly.  A positional grep over another
	#  program's output is a brittle check, and this one proved it within hours.
	_sc=$(python "$SCARD" 2>&1 | grep -E "entries, [0-9]+ graded")
	if [ -n "$_sc" ]; then
		good "seat scorecard: $_sc"
	else
		warn "seat_scorecard.py produced no summary -- check it by hand"
	fi
	#  The row that JUST closed is the one whose outcome is actually known, so name
	#  closed rows whose panel entries are still ungraded.  That is the moment to grade.
	_ug=$(GRADING_CUTOFF_NOTE="$GRADING_CUTOFF_NOTE" python - "$_HERE/pipeline/ledger.json" <<'PYEOF'
import json, io, os, sys
GRADING_CUTOFF = os.environ.get("GRADING_CUTOFF_NOTE", "2026-08-23")
                                # seat_scorecard.py shipped MID-DAY on 2026-08-22 (8185920),
                                # so rows closed ON that day are a boundary this cannot
                                # resolve from dates alone -- grandfather the whole day
                                # rather than guess intra-day ordering.  From 08-23 the
                                # check is live and every closure carries its outcomes.
d = json.load(io.open(sys.argv[1], encoding="utf-8"))
bad, old = [], []
for r in d.get("rows", []):
    if r.get("state") != "closed":
        continue
    ents = [e for e in r.get("entries", []) if e.get("phase") in ("assess", "review")]
    if len(ents) <= 1:
        continue                      # filed, never panelled -- nothing to grade
    #  *** UNVERIFIED IS NOT A GRADE, AND COUNTING IT AS ONE MADE THIS CHECK
    #  VACUOUS. ***  A review seat found it by reading the predicate rather than
    #  the docstring: `any(e.get("outcome"))` is true of the string the design
    #  defines as NOT a grade, so writing UNVERIFIED everywhere would green the
    #  check.  Latent rather than live -- zero rows trip it today -- but a check
    #  that CAN be satisfied without doing the thing is the shape this project
    #  calls vacuous, and it was in the tool built to refuse exactly that.
    if any(e.get("outcome") not in (None, "UNVERIFIED") for e in ents):
        continue
    #  *** FORWARD-ONLY FROM THE DAY THE SCORECARD SHIPPED (8185920, 2026-08-22). ***
    #
    #  This check asked for something seat_scorecard.py's own banner FORBIDS: "Grade an
    #  entry when its claim is CHECKED -- reconstructing grades later reproduces exactly
    #  the recall bias this tool replaced."  Eight rows closed between 08-14 and 08-20,
    #  before the tool existed, and every commit since has printed them as an ungraded
    #  warning that CANNOT BE HONESTLY CLEARED -- only by the reconstruction the tool was
    #  built to refuse.  A warning nobody can clear is a warning everybody learns to skip,
    #  which is worse than not having it.
    #
    #  So they are GRANDFATHERED and COUNTED, in the idiom check_stage_panels.py already
    #  uses -- named as a number rather than a to-do list, so the gap stays visible without
    #  masquerading as an action item.  A row closed on or after the cutoff is still named
    #  individually, because that IS the moment its outcome is known.
    if max([e.get("date", "") for e in ents] or [""]) < GRADING_CUTOFF:
        old.append(r["id"])
        continue
    bad.append(r["id"])
#  Report the TOTAL, not just the first eight.  The original printed bad[:8]
#  with no count, so 37 ungraded rows read as 8 -- a silent cap, which is the
#  shape this project already refuses elsewhere ("silent truncation reads as
#  covered-everything when it did not").
print("%s|%d|%d" % (" ".join(bad[:8]), len(old), len(bad)))
PYEOF
)
	_ugnames=$(printf '%s' "$_ug" | cut -d'|' -f1)
	_ugold=$(printf '%s' "$_ug" | cut -d'|' -f2)
	_ugtot=$(printf '%s' "$_ug" | cut -d'|' -f3)
	if [ -n "$_ugnames" ]; then
		warn "closed rows with panel entries but NO seat outcomes: $_ugtot total, first 8: $_ugnames"
		warn "  grade them with an outcome + outcome_note; see seat_scorecard.py"
		warn "  ($_ugold more are GRANDFATHERED pre-$GRADING_CUTOFF_NOTE and not counted above)"
	elif [ "${_ugold:-0}" != "0" ]; then
		good "every post-cutoff closed row carries seat outcomes ($_ugold grandfathered
          -- closed before seat_scorecard.py existed; grading them now would be the
          reconstruction its own banner forbids)"
	else
		good "every closed-and-panelled row carries seat outcomes"
	fi
fi

say ""; say "Q. matrix.html is current with ledger.json"
GEND=$_HERE/pipeline/gen_dashboard.py
if [ ! -f "$GEND" ]; then
	warn "gen_dashboard.py MISSING -- matrix freshness NOT verified"
else
	_mx=$(mktemp)
	if python "$GEND" --out "$_mx" >/dev/null 2>&1 && cmp -s "$_mx" "$_HERE/pipeline/matrix.html"; then
		good "matrix.html matches a fresh render of ledger.json"
	else
		bad "matrix.html IS STALE -- run: python tools/pipeline/gen_dashboard.py"
		bad "  (and REPUBLISH the artifact; this check cannot see that half)"
	fi
	rm -f "$_mx"
fi

#  ---- Q2 --------------------------------------------------------------------------
#  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS WITHIN THE FROZEN LEGACY CEILING.  2026-10-16, ledger `dashokclass`
#  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
#  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
#  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section holds the off-domain
#  ANSWERS to a CEILING frozen at landing: for each row, phase, seat, date, d and note, no more answers than the md5-pinned
#  baseline holds.  Not a date (a date-only cutoff cannot stop a back-dated or undated addition), not a count without the
#  note (a converted entry's allowance could be refilled; pass 2), and NOT an entry identity: a byte-identical revert of a
#  normalised entry passes, and the dashboard's legacy count can still rise through exempt records and re-exposed older
#  answers (adjudication pass, GPT-6 Astra).  HARD.  It fails on UNMATCHED content and on an EXCESS occurrence -- a NEW
#  off-domain answer, or an OLD one edited in any of those fields (an admitted replacement can be new; v3 pass): editing such an entry means classifying it -- a glyph, no `d`, or a non-answer record token (Fable
#  5.1); for a note-only correction that toll is this check's, not the ruling's (Grok 4.7).  It reds (rc 2) when the ledger
#  or the baseline is unreadable or misshapen or the baseline's md5 is not the pinned one, never silently green.
say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is within the frozen legacy ceiling"
CED=$_HERE/pipeline/check_entry_domain.py
if [ ! -f "$CED" ]; then
	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
else
	#  the overrides are for the controls, never for a commit: an exported GXDOMAIN_BASELINE would swap in another baseline
	#  and skip the md5 pin (Grok 4.7, pass 2), and an exported GXLEDGER would check another ledger (adjudication pass), so
	#  the section checks the real ledger against the pinned baseline
	_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1); _cedrc=$?
	if [ $_cedrc -eq 0 ]; then
		good "$(printf '%s\n' "$_ced" | head -1)"
	elif [ $_cedrc -eq 1 ]; then
		bad "an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one edited):"
		printf '%s\n' "$_ced" | sed 's/^/          /'
	else
		bad "check_entry_domain.py could not run (rc $_cedrc): $(printf '%s\n' "$_ced" | head -1)"
	fi
fi

#  ---- R ---------------------------------------------------------------------------
#  A COMMITTED DETECTOR THAT NO GATE RUNS DEFENDS NOTHING BETWEEN BATTERIES.
#
#  Detector escapes in this project come in three shapes and TWO already had mechanical
#  guards: gate_offline's SM/SC manifests catch a differential with no self-mutant control,
#  and gate_hygiene's EXPECT_CONVERTED pin catches a probe that does not carry the #392 pty
#  constructs.  The third had none -- NOBODY RUNS IT -- and it was the largest.  MEASURED at
#  3d752b4: FOUR committed detectors totalling SIXTY-SIX rows executed in no gate at all.
#    #439/#440 pit8253_latch_probe.py      18 rows         #441 sh4_bsc_width_probe.py  13
#    #442      fbpending_drain_probe.py    11, report-only  #444 hpcmips_ctor_probe.py   24
#  The finding that named the gap put it at 24 rows across two rounds; it is four rounds and
#  66, because #444's detector landed after the census and nothing existed to notice.
#
#  THE MEASURE IS NAMED BECAUSE THE FIRST ONE WAS WRONG: `row()` call sites with a literal
#  label, counted through python's `ast`.  A first pass grepped for 'row("R' and reported 56,
#  having silently dropped every control row that is not R-prefixed.  The padded-column grep
#  trap in another costume -- a number that looks right and counts the wrong set.
#
#  GATE 6's CENSUS PIN IS NOT THIS CHECK IN DIFFERENT CLOTHES, and the distinction is the
#  same one this file already draws between G and H: the PIN asks whether the probe's SOURCE
#  carries the right constructs, R asks whether anything EXECUTES it.  All four files above
#  satisfy the pin today.  Neither catches the other's failure.
#
#  A MENTION IS NOT WIRING, and that is the whole difficulty.  gate_sh_rounding.sh:185
#  mentions sh4_bsc_width_probe.py in a comment COMPLAINING that it is unwired; gate_hygiene
#  mentions all four in its census annotations; and gate_hygiene.sh:331 carries a probe
#  basename and the token `python3` on ONE non-comment line whose message is that the probe
#  did NOT run.  A grep-for-the-name check scores every one of those as wired and prints
#  green over the entire defect.  check_probe_wiring.py decides by COMMAND POSITION, derives
#  the battery from run.sh's own GATES array, and PRINTS the file:line it found -- so the
#  derivation is auditable rather than trusted.  It is the check_fable_queue substring bug
#  from earlier the same day, refused in advance.
#
#  HARD, and retroactive rather than forward-only-by-date: the domain was 36 files in one
#  flat directory when this was written (#471 has since made the scan recursive), and a date
#  cutoff would have grandfathered exactly the four files it existed for.
#  Existing gaps are carried as DATED exemptions that EXPIRE, never as silent grandfathering; the
#  dates live in check_probe_wiring.py's EXEMPT table, not here.  (They were 2026-09-20, chosen to
#  fall due with gate_offline's fbpending_bound; #537 discharged that debt and #536 moved the
#  block to 2026-09-27 by owner ruling; #550 dispersed it to ten individual dates, 2026-10-08
#  to 2026-12-03, by owner ruling 2026-09-24.)
#
#  THE SELFTEST RUNS ONLY WHEN THE CHECKER ITSELF CHANGES.  --selftest applies its mutants (22, pinned below) to
#  temp copies and asserts each exit status, which takes ~14 s -- too slow for every commit,
#  and pointless when the checker did not move.  Firing it on the one commit that could break
#  it is the section-E idea: a check nobody has to remember.
say ""; say "R. every committed detector is run by a gate (or dated-exempt)"
PWCHK=$_HERE/pipeline/check_probe_wiring.py
if [ ! -f "$PWCHK" ]; then
	warn "check_probe_wiring.py MISSING -- probe wiring is NOT verified"
else
	if out=$(python "$PWCHK" 2>&1); then
		good "$(printf '%s' "$out" | grep -E 'PROBEWIRING_PASS')"
		printf '%s\n' "$out" | grep -E '^  note ' | sed 's/^/        /'
	else
		bad "A COMMITTED DETECTOR IS RUN BY NO GATE (or an exemption expired):"
		printf '%s\n' "$out" | grep -E 'PROBEWIRING_FAIL|^  FAIL ' | sed 's/^/          /'
		bad "  wire it into a gate, or add a DATED line to EXEMPT naming the gate that owes it"
	fi
	#  UNTRACKED COUNTS AS TOUCHED.  The first version asked only `git diff` and
	#  `git diff --cached`, and reported "checker unchanged" on the very commit that
	#  INTRODUCED the checker -- it was untracked, so neither diff could see it, and the
	#  one commit that most needed the selftest was the one that skipped it.  Measured on
	#  this file's own first run.
	_pwtouched=$( { git diff --cached --name-only; git diff --name-only;
	                git ls-files --others --exclude-standard; } \
	              | grep -c 'tools/pipeline/check_probe_wiring\.py' )
	if [ "$_pwtouched" -gt 0 ]; then
		if stout=$(python "$PWCHK" --selftest 2>&1); then
			good "$(printf '%s' "$stout" | grep -E 'PROBEWIRING_SELFTEST_PASS')"
			#  *** THE EXIT CODE IS NOT ENOUGH, AND A SEAT NAMED THE GAP:
			#  "precommit checks the exit code, not the mutant census -- the
			#  suite goes green with MALFORMED-EXEMPTION coverage gone." ***
			#
			#  Every mutant that REMAINS can behave correctly while mutants
			#  that were DELETED say nothing at all.  The selftest itself now
			#  holds its denominator when a case cannot run (it appends a
			#  failure rather than skipping), but that only covers the SKIP
			#  path -- an edit that removes a case outright still exits 0.
			#
			#  So the count is pinned to a LITERAL here, which is the same
			#  discipline every gate row in this tree already uses for its own
			#  denominator: a suite that loses cases cannot pass by shrinking.
			#  Raise it DELIBERATELY when mutants are added, and never nudge it
			#  down to silence a red -- the count is the point.
			_stden=$(printf '%s' "$stout" \
			         | sed -n 's/.*PROBEWIRING_SELFTEST_PASS *[0-9]*\/\([0-9]*\).*/\1/p' \
			         | tail -1)
			if [ "${_stden:-0}" -eq 22 ] 2>/dev/null; then
				good "selftest mutant count is 22, the pinned value"
			else
				bad "THE PROBE-WIRING SELFTEST HAS LOST MUTANTS: ${_stden:-unparseable}, pinned 22."
				bad "  Every REMAINING mutant can behave correctly while DELETED ones say"
				bad "  nothing at all.  Raise the pin DELIBERATELY when mutants are added;"
				bad "  never nudge it down to silence a red -- the count is the point."
			fi
		else
			bad "THE PROBE-WIRING CHECKER CAN NO LONGER BE SHOWN TO FAIL:"
			printf '%s\n' "$stout" | grep -E 'SELFTEST_FAIL|^  FAIL ' | sed 's/^/          /'
		fi
	else
		good "checker unchanged -- selftest not re-run (fires when it is edited)"
	fi
fi

#  ---- V ---------------------------------------------------------------------------
#  THE VERDICT EXTRACTOR DECIDES WHETHER A PANEL WAS SPLIT OR UNANIMOUS, AND IT WAS
#  WRONG ABOUT THAT FOR ITS WHOLE LIFE WITH NOTHING EXECUTING IT.
#
#  Two defects, both found by a seat READING the regex rather than running it: markdown
#  emphasis made a LIVE seat's correct verdict read as a format miss, and a single-word
#  capture collapsed SHIP against SHIP WITH CHANGES and every OPTION A/B/C into one
#  token -- so every split panel this project ran was reported as unanimous.
#
#  Same shape as section R's selftest and wired the same way: it fires only when the
#  extractor itself is touched, and UNTRACKED COUNTS AS TOUCHED, which is the lesson R
#  paid for -- the first version reported "unchanged" on the very commit that
#  introduced the file.
say ""; say "V. the verdict extractor can still be shown to fail"
SVCHK=$_HERE/pipeline/seat_verdicts.py
if [ ! -f "$SVCHK" ]; then
	warn "seat_verdicts.py MISSING -- panel verdicts are NOT extracted"
else
	_svtouched=$( { git diff --cached --name-only; git diff --name-only;
	                git ls-files --others --exclude-standard; } \
	              | grep -c 'tools/pipeline/seat_verdicts\.py' )
	if [ "$_svtouched" -gt 0 ]; then
		if svout=$(python "$SVCHK" --selftest 2>&1); then
			good "$(printf '%s' "$svout" | grep -E 'SEAT_VERDICTS_SELFTEST_PASS')"
		else
			bad "THE VERDICT EXTRACTOR CAN NO LONGER BE SHOWN TO FAIL:"
			printf '%s
' "$svout" | grep -E 'SELFTEST_FAIL|^  FAIL ' | sed 's/^/          /'
		fi
	else
		good "extractor unchanged -- selftest not re-run (fires when it is edited)"
	fi
fi

#  ---- W ---------------------------------------------------------------------------
#  A ROUND WAS NEARLY REDONE FROM SCRATCH BECAUSE A LEDGER ROW SAID `open` ON WORK
#  THAT HAD SHIPPED HOURS EARLIER.
#
#  `sqreadtype` carried a witness field saying its warrant measurement was PENDING;
#  the measurement is in its own CHANGELOG block and the round shipped as 3ff2138.
#  It was caught by accident -- the row was picked as the next round and the source
#  comment already said the fix was in.  The carrier names this class (a
#  state-vs-substance mismatch) and nothing checked it.
#
#  *** THE FIRST DESIGN WAS VACUOUS AND ITS POSITIVE CONTROL SAID SO. ***  It looked
#  for the row id in a commit SUBJECT; subjects here carry ROUND NUMBERS and name no
#  row, so reinstating the defect did not flag it.  The association that works is the
#  `witness` field, which exists for exactly this purpose: an open row naming a
#  COMMITTED probe is claiming to be unstarted while its detector is in the tree.
#  Negative-controlled both ways; opt out with a `state_note` that says what is left.
#  W ALSO CHECKS THE QUEUE FILE NOW.  Section P checks ledger -> file; nothing
#  checked file -> ledger, and SEVEN headings in OUTSTANDING_BUGS.md said `open` on
#  work the ledger recorded as closed.  That is the EXPENSIVE direction: the
#  carrier's first-stop procedure names that file as the live queue, so each stale
#  heading offers shipped work to a fresh session, which has no reason to doubt it.
#  Deliberately preserved originals are exempt, and the sweep measured exactly one
#  of those against six genuine cases.
say ""; say "W. a row's state agrees with what shipped"
RSCHK=$_HERE/pipeline/check_row_states.py
if [ ! -f "$RSCHK" ]; then
	bad "check_row_states.py MISSING -- stale row states are NOT verified"
elif rsout=$(python "$RSCHK" 2>&1); then
	good "$(printf '%s' "$rsout" | grep -E 'ROW_STATES_PASS')"
else
	bad "A LEDGER ROW SAYS open ON WORK THAT SHIPPED:"
	printf '%s\n' "$rsout" | grep -E 'STALE|ROW_STATES_FAIL|^ ' | sed 's/^/          /'
fi

#  ---- X ---------------------------------------------------------------------------
#  A CITED MEASUREMENT MUST EXIST.  The rule "a score claim names its artifact" was
#  already in force and already being followed when it failed TWICE in one day:
#
#    * `#462` cited `probe_base.raw` for 52/52; a later 57-row table REUSED that name,
#      so the claim became CONTRADICTED BY ITS OWN EVIDENCE, not merely unverifiable.
#    * `#461`'s lethal mutant `m_dmarevert` (22/31) has NO per-row artifact at all --
#      0 candidate lines across every `.out` in both scratchpads.  A retrospective audit
#      of that detector was ATTEMPTED on 2026-08-24 and could not run.
#
#  EXISTENCE ONLY, and the scope cut is the safety argument.  It does not parse the log
#  or re-derive the score: section U already checks DENOMINATORS against the gate pin,
#  nothing mechanical can tell a measured numerator from a carried one, and a checker
#  that tried would grow without bound -- the #392 shape.  A gate that stats cited paths
#  cannot creep into policing scratch directories.
#
#  Specified by the fable5 adjudication of #462, Decision 4c, which set both the altitude
#  ("checks committed records, never scratchpad state") and the scope cut.  Forward-only
#  from round 462; earlier blocks predate the rule, and a red that no edit can clear is
#  its own hazard.  NEGATIVE-CONTROLLED ON ITS FIRST RUN: it reported two missing
#  artifacts, both real, and went green only after they were archived to a durable path.
say ""; say "X. every measurement cited in a round block still exists"
CACHK=$_HERE/pipeline/check_cited_artifacts.py
if [ ! -f "$CACHK" ]; then
	bad "check_cited_artifacts.py MISSING -- cited measurements are NOT verified"
elif caout=$(python "$CACHK" 2>&1); then
	good "$(printf '%s' "$caout" | grep -E 'CITED_ARTIFACTS_PASS')"
else
	bad "A ROUND BLOCK CITES A MEASUREMENT THAT DOES NOT EXIST:"
	printf '%s\n' "$caout" | grep -E 'CITED_ARTIFACTS_FAIL|^    #' | sed 's/^/          /'
	bad "  restore the artifact, or correct the claim to say the log was not preserved"
fi

#  THE SELFTEST FIRES ONLY WHEN THE CHECKER ITSELF CHANGES -- the section-R idiom, and
#  wired the same way.  A completeness check found that this gate shipped WITHOUT one
#  while both its siblings have them: the gate enforcing "every score names verifiable
#  evidence" had no evidence of its own correctness, and the three false-green fixes it
#  went through had nothing pinning them.  ***  IT FAILED ON ITS FIRST RUN AND FOUND A
#  REAL BUG: *** `LOOSE` had been compiled with a literal BACKSPACE byte where `\\b`
#  belonged, so the unenforced-mentions denominator matched NOTHING and had been printing
#  a PHANTOM ZERO all evening -- in the counter added specifically to make phantom zeros
#  visible.  UNTRACKED COUNTS AS TOUCHED, per section R's own scar.
#  DETECT THE TOUCH INLINE, exactly as section R does -- `$CHANGED` is not defined
#  until much later in this file, so the first version of this block never fired.
#  UNTRACKED COUNTS AS TOUCHED: section R's own scar is that a checker was untracked
#  on the very commit that introduced it, so neither diff could see it and the one
#  commit that most needed the selftest was the one that skipped it.
_catouched=$( { git diff --cached --name-only; git diff --name-only; git ls-files --others --exclude-standard; } | grep -c 'tools/pipeline/check_cited_artifacts\.py' )
if [ "$_catouched" -gt 0 ]; then
	if stout=$(python "$CACHK" --selftest 2>&1); then
		good "$(printf '%s' "$stout" | grep -E 'SELFTEST_PASS')"
	else
		bad "check_cited_artifacts.py SELFTEST FAILED -- the gate is not trustworthy:"
		printf '%s\n' "$stout" | grep -E 'SELFTEST_FAIL|^    ' | sed 's/^/          /'
	fi
else
	good "checker unchanged -- selftest not re-run (fires when it is edited)"
fi

#  ---- J ---------------------------------------------------------------------------
#  THE CARRIER IS TRACKED BY COPY, AND A COPY THAT NOTHING CHECKS GOES STALE.
#
#  Owner decision, 2026-08-17, asked as a question: track `CLAUDE.md` and `PIPELINE.md`
#  rather than leave the files that direct every session outside version control.
#
#  The literal answer was "track them at the project root" -- and that is not possible,
#  because the git root is GXEMUL-SEC/, one level BELOW the project root where the carrier
#  must sit to be auto-loaded.  (The question's own diagram drew GXEMUL/ as the repo.  It
#  was wrong.)  So the tracked form is a COPY under tools/, and the copy reintroduces
#  exactly the divergence risk the owner rejected when rejecting the dated snapshot.
#
#  This check is what makes the copy safe: byte-identity, HARD, using check A's own `cmp`
#  idiom.  A carrier edit that never reaches the repo is then a red commit rather than a
#  copy that silently describes last week's process.
#
#  tools/ and not GXEMUL-SEC/ deliberately: Claude Code auto-loads CLAUDE.md from the cwd
#  upward, and the session cwd DRIFTS -- it has sat in GXEMUL-SEC/regress for whole rounds.
#  A copy at GXEMUL-SEC/CLAUDE.md would then load ALONGSIDE the root original, putting two
#  copies of a 38 KB carrier in one context.  tools/ is never a cwd ancestor in practice.
#
#  An ABSENT original is not a failure: on a fresh clone the repo copy is the only one
#  there is, and demanding a file that version control cannot deliver would make the check
#  fail hardest in the one situation it exists to serve.
say ""; say "J. tracked carrier copies match the originals"
for _c in CLAUDE.md PIPELINE.md; do
	if [ ! -f "$SEC/tools/$_c" ]; then
		bad "$_c has no tracked copy at tools/$_c -- the carrier is untracked again"
	elif [ ! -f "$ROOT/$_c" ]; then
		good "tools/$_c tracked; no project-root original (fresh clone -- repo copy is it)"
	elif cmp -s "$ROOT/$_c" "$SEC/tools/$_c"; then
		good "tools/$_c is byte-identical to the project-root original"
	else
		bad "tools/$_c HAS DRIFTED from $ROOT/$_c -- the tracked carrier is stale."
		bad "     cp \"$ROOT/$_c\" \"$SEC/tools/$_c\"   (the root file is the live one)"
	fi
done

#  ---- K ---------------------------------------------------------------------------
#  A ROW THAT CLOSES WITH COMMITS MUST NAME ITS WITNESS.
#
#  Specified by the flagship seat that adjudicated the WITNESS LADDER, and needed for a
#  measured reason: asked whether the tightened rule would retroactively invalidate any
#  shipped round, a measure seat could only answer by READING ROUND PROSE, because nothing
#  in the schema names the witnessing artefact.  A rule that cannot be audited backwards or
#  enforced forwards is a rule kept by memory.
#
#  It enforces the SHAPE, never the truth -- it cannot tell whether `probe:foo.py` really
#  preserves routing, and a script that claimed to would be the false comfort the ladder was
#  written against.  Its first run found a gap in the ladder itself: none of the four rungs
#  fit a HARNESS round, which ships commits with no guest path to witness.
say ""; say "K. a row that closed with commits names its witness"
WITCHK=$_HERE/pipeline/check_witness.py
if [ ! -f "$WITCHK" ]; then
	warn "check_witness.py MISSING -- witness naming NOT verified"
elif out=$(python "$WITCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'WITNESS_PASS|check_witness:' | tr '
' ' ')"
else
	bad "A ROW CLOSED WITH COMMITS AND NO ADMISSIBLE WITNESS:"
	printf '%s
' "$out" | sed 's/^/          /'
fi

#  ---- L ---------------------------------------------------------------------------
#  DOES THE LEDGER KNOW ABOUT THE WORK THAT SHIPPED?
#
#  G, H, I and K all ask whether a row's PROCESS was carried out -- seats fired, seats
#  recorded, owed work queued, witness named.  None of them asks the blunter question:
#  did the row notice that the code landed?  Measured on this check's first run: of the 40
#  most recent commits 33 were named by no row at all, and two of those were sharp --
#  6014b7e's subject reads "selfmutant6 CLOSED" against a row that read held with empty
#  commits, and gate3scope's `commits` named 2a5bc48, the R9/#435 m8820x DEVICE round, which
#  touches zero selfmutant lines.  The board renders from the ledger, so that drift shows
#  finished work as open queue -- the direction that matters, because it is invisible.
#
#  It reports TWO blindnesses every run rather than hiding them: 13 row ids are too short to
#  match safely, and 13 rows carry commits that no scanned subject ever names.  Both are
#  printed on GREEN runs too.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] It reports two blindnesses
#  every run: 13 row ids are too short to match safely, and 117 rows carry commits that no scanned subject names.
#  (hprecommitcheck:F15: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
say ""; say "L. the ledger names the work that shipped"
ATTRCHK=$_HERE/pipeline/check_commit_attribution.py
if [ ! -f "$ATTRCHK" ]; then
	warn "check_commit_attribution.py MISSING -- ledger attribution NOT verified"
elif out=$(python "$ATTRCHK" 2>&1); then
	good "$(printf '%s' "$out" | grep -E 'ATTRIBUTION_PASS' | tr '\n' ' ')"
	#  The blindnesses are part of the result, not a footnote -- echo them on green.
	printf '%s\n' "$out" | grep -E 'NOT MATCHABLE|NEVER NAMED' | sed 's/^/          /'
else
	bad "THE LEDGER DISAGREES WITH WHAT SHIPPED:"
	printf '%s\n' "$out" | grep -E '^  HARD' | sed 's/^/          /'
fi

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

#  H2 (#534, fable5 R5): four tools read ledger stage tokens and each once carried its own copy;
#  every mis-classification this project measured came from one copy not mirroring another.  The
#  literals and the classifier now live in stage_tokens.py, and this refuses a token spelled as a
#  CODE string anywhere else in tools/pipeline/ (docstrings and comments exempt -- they describe).
say ""; say "H2. stage tokens are spelled in one place"
TOKCHK=$_HERE/pipeline/stage_tokens.py
if [ ! -f "$TOKCHK" ]; then
	bad "stage_tokens.py MISSING -- H, I and the dashboard import it"
elif out=$(python "$TOKCHK" --selfcheck 2>&1); then
	good "$(printf '%s' "$out" | tail -1)"
else
	bad "A STAGE TOKEN IS SPELLED OUTSIDE stage_tokens.py:"
	printf '%s\n' "$out" | sed 's/^/          /'
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

#  -z + strip the status columns, and take the RIGHT-hand side of a rename.  The old form
#  was `awk '{print $2}'`, which is not a path extractor: `R  old -> new` yields the OLD
#  path so the new file is never checked, and a quoted path containing a space is truncated
#  at the space, silently skipping checks A, B and E for it.
#  *** SCOPED TO WHAT IS ACTUALLY BEING COMMITTED, NOT THE WHOLE WORKING TREE. ***
#
#  This was `git status --porcelain`, i.e. staged AND unstaged together.  That is correct for a
#  single-writer session and WRONG the moment two rounds run in parallel: on 2026-08-21 a
#  records-only commit (tools/ and OUTSTANDING_BUGS only) was blocked by sections A and B firing
#  on `src/machines/machine_hpcmips.c` -- a file a CONCURRENT agent was editing and had not yet
#  propagated, and which the commit did not touch.
#
#  Nothing is weakened by the narrowing.  The un-propagated file is still caught -- at the moment
#  it is committed, because then it IS staged.  What changes is that it no longer blocks an
#  unrelated commit, which is the difference between a gate and an obstacle.
#
#  The fallback matters: with nothing staged (an interactive run, or `git commit -a`), fall back
#  to the full working tree, so a bare invocation still audits everything.  A check that silently
#  audited nothing when run the ordinary way would be worse than the problem being fixed.
CHANGED=$(git diff --cached --name-only)
if [ -z "$CHANGED" ]; then
	CHANGED=$(git status --porcelain -z | tr '\0' '\n' | sed -e 's/^...//' -e 's/.* -> //')
fi

#  ANNOUNCE what the narrowing means for this run, so a divergent file that is merely OUT OF
#  SCOPE is never mistaken for one that was checked and passed.
_unstaged_src=$(git diff --name-only -- 'src/*' | tr '\n' ' ')
if [ -n "$_unstaged_src" ]; then
	warn "With nothing staged, A/B select modified source paths through the working-tree fallback.  When anything is staged, they select staged paths but inspect working-tree contents, including unstaged hunks in those paths; exclusively unstaged paths are omitted.  UNSTAGED src/: $_unstaged_src"  # (#560)
fi
say ""; say "Z. no tracked script invokes wsl -c with a bare dollar"
#
#  WSL DOLLAR RATCHET.  A wsl -c invocation does not deliver shell variables to the
#  inner shell, EVEN INSIDE SINGLE QUOTES -- measured 2026-08-29 with controls in
#  regress/artifacts/makercfalse/wsl_dollar_20260829.out.  A mutant never applied
#  then scores the BASE binary and reports a clean kill table.
#
#  *** ITS RECALL ON THE RECORDED HISTORY IS ZERO, STATED HERE RATHER THAN
#  DISCOVERED LATER. ***  The class bit FIVE times and every occurrence was an
#  INTERACTIVE, ad-hoc command; the committed tree holds the form four times and all
#  four are QUOTATIONS of the defect in prose.  This check would have caught NONE of
#  them, and it is NOT the primary defence.
#
#  The primary defence is the PreToolUse hook at .claude/hooks/wsl_dollar_guard.py,
#  which fires where all five happened -- at the keyboard.  THIS does the one thing
#  the hook cannot: stop the form being COMMITTED into a script, to run unattended.
#
#  ZERO-POPULATION RATCHET: 229 tracked .sh/.py at introduction, NONE carrying the
#  form, so it grandfathers nothing and needs no dated cutoff.  Controlled both ways
#  on the day it landed: 9/9 line cases, a clean tree passing with its denominator,
#  and an injected violation failing with file:line.
#
#  ABOVE THE EMPTY-CHANGED EXIT ON PURPOSE, for the reason recorded just below about
#  F/G/H/I/J/K: it scans TRACKED files, so a clean tree is exactly when it matters.
if [ -f "$SEC/tools/pipeline/check_wsl_dollar.py" ]; then
	if wslout=$(python "$SEC/tools/pipeline/check_wsl_dollar.py" "$SEC" 2>&1); then
		good "$(printf "%s" "$wslout" | sed -e "s/^ *//" | head -1)"
	else
		printf "%s\n" "$wslout" | while IFS= read -r l; do bad "$l"; done
		fail=$((fail+1))
	fi
else
	bad "check_wsl_dollar.py MISSING -- section Z proved nothing"
	fail=$((fail+1))
fi

if [ -z "$CHANGED" ]; then
	say "nothing staged or modified -- no per-file checks."
	#  *** DO NOT exit 0 HERE.  *** Sections F/G/H/I/J/K have already run above and may have
	#  set `fail`.  The old form discarded them: measured on a clean tree with a stale carrier
	#  and a missing pass-2 receipt, it printed SIX `FAIL` lines, no verdict line at all, and
	#  exited 0.  A clean tree is precisely the state in which those checks are meaningful --
	#  F was deliberately moved above this exit for that reason, and then the exit threw its
	#  answer away.
	if [ $fail -gt 0 ]; then
		say ""
		say "=========================================================="
		say "PRECOMMIT_FAIL   $fail hard, $warn soft"
		exit 1
	fi
	say "PRECOMMIT_PASS   0 hard, $warn soft"
	exit 0
fi

say "=== #418-era PRE-COMMIT REWORK CHECK ==="
say "files in play:"; printf '    %s\n' $CHANGED

# ---------------------------------------------------------------- A
#  TWIN-TREE PROPAGATION.  est/ and GXEMUL-SEC differ by exactly five named
#  files plus SEC-only dev_ne2000.c; ANY OTHER src/ file must land byte-
#  identical in both.  #415 is a whole commit that exists because this was
#  skipped once -- and the gate that should have caught it named two files when
#  the truth was three, because an allowlist entry had gone stale.
say ""; say "A. twin-tree propagation (the #415 class -- FULLY mechanical)"
#  DERIVED, NOT PINNED -- because a pinned list has now gone stale TWICE, by one file and
#  then by five.  Measured 2026-08-19: the tree has SEVEN divergent paths (.index,
#  Makefile.skel, autodev.c, dev_jazz.c, machine_arc.c, arcbios.c, and SEC-only
#  dev_ne2000.c) while this list named TWO.  The consequence was not a missed check but an
#  ACTIVELY HARMFUL one: touching any unlisted ARC/Jazz file hard-failed and instructed the
#  operator to overwrite the SEC-only ARC layer with est/'s version.  And `misc.h` was listed
#  while NOT being divergent, so it false-passed a genuine unpropagated edit.
#
#  The tracked file is the declaration; this recomputes reality and compares.  A drift in
#  either direction is then a red row naming the path, instead of a silent wrong instruction.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] tools/est_divergence.txt is
#  an exemption allowlist whose members are unconditionally skipped rather than recomputed and verified.
#  (hprecommitcheck:F14: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
DIVERGENCE_FILE=$SEC/tools/est_divergence.txt
DIVERGENT_OK=$(grep -vE '^\s*(#|$)' "$DIVERGENCE_FILE" 2>/dev/null | tr '\n' ' ')
if [ -z "$DIVERGENT_OK" ]; then
	warn "tools/est_divergence.txt missing or empty -- twin-tree allowlist NOT derived"
fi
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

#  *** build-asan/ JOINED THE PROPAGATION SET BY OWNER RULING, 2026-08-27. ***
#
#  It was measured FOUR ROUNDS STALE on 2 of 4 sampled files, and it is the tree
#  that catches heap overflows.  Two findings in one session turned on an ASAN
#  build: a heap-buffer-overflow mutant that the ordinary detector scored 52/52
#  GREEN, and a NULL dereference.  A stale ASAN tree is a detector that has
#  silently stopped detecting -- worse than no detector, because it reassures.
#
#  ABSENCE IS NOT A FAILURE.  On a machine that never built the tree the rows are
#  skipped, exactly as section A treats a missing est/.  A gate that hard-fails on
#  a tree someone chose not to build is a gate that gets switched off.
ASAN=$ROOT/build-asan
if [ -d "$ASAN/src" ]; then
	if [ -f "$ASAN/.MUTANT" ]; then
		bad ".MUTANT sentinel present in build-asan/ -- restore from SEC and REBUILD:"
		sed 's/^/          /' "$ASAN/.MUTANT"
	else
		good "no .MUTANT sentinel in build-asan/"
	fi
	for f in $CHANGED; do
		case "$f" in src/*) ;; *) continue ;; esac
		[ -f "$ASAN/$f" ] || continue
		if cmp -s "$SEC/$f" "$ASAN/$f"; then good "$f == build-asan/"
		else bad "$f DIFFERS from build-asan/ -- the sanitiser tree is not this source"; fi
	done
else
	say "      --    build-asan/ absent -- rows skipped, not failed"
fi

#  *** THE FOURTH TREE.  As of 2026-08-30 the no-VPATH rule names FOUR build trees --
#  est/, build/, build-asan/ and WSL /tmp/gxsec-build -- and this gate enforced THREE.
#  Filed as `novpadfourth` and left open on the assumption that a WSL tree is
#  unreachable from the Windows side. ***
#
#  *** THIS COMMENT SAID "HAS ALWAYS NAMED FOUR", AND THAT WAS BOTH UNDATED AND FALSE.
#  A panel seat caught it on the diff, under the standing license. ***  `build-asan/`
#  joined the propagation set BY OWNER RULING ON 2026-08-27 -- the section thirty lines
#  above says so in its own first line -- so the set has been four for three days, not
#  always.  An empirical claim about a RULE'S HISTORY, sitting undated in a tool
#  comment, is the same defect this round repaired in a probe's header: a sentence that
#  is wrong on the day it is committed and that nothing re-reads.
#
#  THE HYGIENE RULE GENERALISES, and the seat stated it better than this comment can:
#  **claims about prior state either cite the rule's text and date, or are DATED.**
#  That applies to TOOL comments exactly as it does to probe comments.
#
#  MEASURED 2026-08-30, and the assumption is false: `//wsl.localhost/<distro>/tmp/...`
#  is readable from git-bash, and a `cmp` across that boundary completes in 83 ms.  The
#  obstacle was never technical; the check simply was never written.
#
#  THE HAZARD IT CLOSES IS THE SAME ONE build-asan/ CLOSES, and this tree is the one
#  the arc rig actually runs: a stale source here means a measurement attributed to a
#  commit that the binary never contained.
#
#  ABSENCE IS NOT A FAILURE, for two reasons rather than one: the tree may never have
#  been built, AND the WSL distro may simply not be running, in which case the UNC path
#  is unreadable and nothing is wrong.  Both skip.  A gate that hard-fails because a VM
#  is asleep is a gate that gets switched off.
WSLT=${GXWSLTREE:-//wsl.localhost/Gentoo/tmp/gxsec-build}
if [ -d "$WSLT/src" ]; then
	if [ -f "$WSLT/.MUTANT" ]; then
		bad ".MUTANT sentinel present in the WSL tree -- restore from SEC and REBUILD:"
		sed 's/^/          /' "$WSLT/.MUTANT"
	else
		good "no .MUTANT sentinel in the WSL tree"
	fi
	for f in $CHANGED; do
		case "$f" in src/*) ;; *) continue ;; esac
		[ -f "$WSLT/$f" ] || continue
		if cmp -s "$SEC/$f" "$WSLT/$f"; then good "$f == WSL /tmp/gxsec-build"
		else bad "$f DIFFERS from the WSL tree -- the arc rig's source is not this source"; fi
	done
else
	say "      --    WSL /tmp/gxsec-build unreachable (tree absent, or the distro is"
	say "            not running) -- rows skipped, not failed"
fi

#  *** THE PreToolUse HOOK'S 18 CONTROLS ARE NOW RUN BY SOMETHING.  Until 2026-08-30
#  they were run by nothing -- filed as `hookctlgate`. ***
#
#  THE CASE IS MEASURED, NOT HYPOTHETICAL: that hook shipped on 2026-08-29 with FOUR
#  defects and nobody noticed for hours -- two false negatives (including the multi-line
#  `bash -c` shape that actually bites) and two false positives that line-scoping was
#  adopted to fix and did not.  A guard that fires on every Bash call had no regression
#  test that anything executed.
#
#  CONDITIONAL ON PURPOSE.  The suite takes ~28 s, which is too slow for every commit
#  and is exactly how a gate earns being switched off.  It runs only when the hook, its
#  shim, or the suite itself is in the changed set -- which is when it can regress.
#
#  NOT a regress gate: it tests a Claude-Code hook, not the emulator, so no battery gate
#  can host it.  This is the harness gate, which is where harness properties belong.
HOOKCTL="$SEC/regress/artifacts/makercfalse/hook_controls_20260829/hookctl.py"
hookctl_wanted=no
for f in $CHANGED; do
	case "$f" in
	tools/hooks/wsl_dollar_guard.py|regress/artifacts/makercfalse/hook_controls_20260829/hookctl.py)
		hookctl_wanted=yes ;;
	esac
done
if [ "$hookctl_wanted" = yes ] && [ -f "$HOOKCTL" ] && command -v python > /dev/null 2>&1; then
	#  *** PASS AN EXPLICIT OUTPUT PATH.  The suite defaults to `hookctl.out` in the
	#  CURRENT DIRECTORY, so the first run of this section dropped a stray file in
	#  the repo root -- caught by `git status` one minute after the commit that
	#  introduced the section.  A gate that litters the tree it guards is a gate
	#  people delete. ***
	hctmp=$(mktemp 2>/dev/null || echo "${TMPDIR:-/tmp}/hookctl.$$.out")
	hcout=$(python "$HOOKCTL" "$hctmp" 2>&1)
	rm -f "$hctmp"
	if printf '%s' "$hcout" | grep -q HOOKCTL_DONE; then
		hcn=$(printf '%s' "$hcout" | grep -oE '[0-9]+ of [0-9]+ controls pass' | head -1)
		hcw=$(printf '%s' "$hcout" | grep -oE '[0-9]+ wrong' | head -1)
		case "$hcw" in
		"0 wrong") good "wsl-dollar hook controls: $hcn" ;;
		*)         bad  "wsl-dollar hook controls: $hcn, $hcw -- the guard regressed" ;;
		esac
	else
		#  No sentinel is NOT a pass.  The suite refuses outright if the hook is
		#  missing, and that refusal must read as a failure rather than a skip.
		bad "wsl-dollar hook controls did not reach HOOKCTL_DONE:"
		printf '%s\n' "$hcout" | tail -3 | sed 's/^/          /'
	fi
elif [ "$hookctl_wanted" = yes ]; then
	soft "the hook changed but its control suite could not be run -- NOT passed"
fi

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

say ""; say "Y. no tracked TEXT file has gained a NUL byte"
#
#  WHY THIS EXISTS.  A shell heredoc once wrote three literal NUL bytes into two
#  tracked text files (row `nulheredoc`).  The damage is not the bytes -- it is that
#  grep then treats the file as BINARY and silently stops reporting matches.  Almost
#  every gate here is grep-based, so one NUL can hollow out a whole gate while every
#  row still reads green.
#
#  *** THIS CHECK WAS WRITTEN WRONG TWICE ON 2026-08-27 AND BOTH FAILURES ARE THE
#  REASON IT LOOKS LIKE THIS. ***
#
#  (1) The first version used `LC_ALL=C grep -qm1 -P "\\x00"`.  **grep REFUSES to
#      run -P under LC_ALL=C** -- "supports only unibyte and UTF-8 locales" -- and with
#      -q plus 2>/dev/null that refusal is invisible.  Every file reported clean.  A
#      check that cannot fail, built inside a checker.  The same mistake made an
#      earlier 1161-file census inert: it reported 0 hits because grep never ran.
#
#  (2) Writing that pattern through a heredoc turned `\\x00` into an actual NUL
#      byte in this script -- reproducing `nulheredoc`s exact mechanism inside the
#      check meant to catch it.  Ordinary grep then called precommit_check.sh binary.
#
#  So: `tr -cd` and not grep.  No regex engine, no -P, no locale dependency, and no
#  backslash to survive a quoting layer.  If you edit this line, re-run the negative
#  control below; do not assume a pattern-based rewrite is equivalent.
#
#  Scoped to text extensions on purpose: a future tracked .pdf or .png carries NULs
#  legitimately, and widening this to every tracked file would make it a check that
#  has to be switched off, which is worse than no check.
nulhits=0
nulscanned=0
for f in $(git -C "$SEC" ls-files -- "*.c" "*.h" "*.py" "*.sh" "*.md" "*.json" "*.txt" "*.tsv" 2>/dev/null); do
	[ -f "$SEC/$f" ] || continue
	nulscanned=$((nulscanned+1))
	if [ "$(tr -cd "\000" < "$SEC/$f" | wc -c)" -gt 0 ]; then
		bad "$f contains a NUL byte -- grep will treat it as BINARY and go quiet"
		nulhits=$((nulhits+1))
	fi
done
if [ "$nulscanned" -eq 0 ]; then
	bad "NUL check scanned ZERO files -- the ls-files pattern selected nothing, so it"
	bad "proved nothing.  A pattern that matches nothing reports 0 for everything."
elif [ "$nulhits" -eq 0 ]; then
	good "no NUL bytes in $nulscanned tracked text files"
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
