#!/bin/bash
# GATE 6 -- no distress markers in the boot logs.
#
# Cheap, and it has caught real regressions: round 40 found that #265's own diagnostic
# flooded the log on a healthy boot, and that #261 was listing a subsystem it had not
# actually armed. Neither changed a pass/fail count -- both showed up only as marker counts.
#
# READS THE RAW PTY LOGS ON PURPOSE. fatal() and debugmsg() output is not guest console
# output; it goes straight to stdout and interleaves into the pty stream, and the arc
# screen reconstruction that gate 4 needs for GUEST tokens actively garbles it. Measured:
# '{ asc: data in' reads 0 from the arc screen rebuild and 5 from the raw log.
#
# TWO WAYS THIS GATE USED TO PASS WITHOUT PROVING ANYTHING, both now closed:
#
#  * EMPTY LOGS. It checked only that the files existed. `: > /tmp/pD.log` made 20 checks
#    go green -- two empty files certifying a clean boot. There is now a POSITIVE CONTROL:
#    each log must be substantial AND contain the guest's own uid=0(root), so absence of
#    distress is only counted when presence of a real boot is proved.
#  * STALE LOGS. Everything lives in /tmp and survives until reboot, so running this gate
#    alone -- or after gate 4 skipped -- graded yesterday's logs, produced by a binary that
#    no longer exists. Gate 4 now deletes them first and copies them into $LOGDIR when it
#    finishes; this gate reads THOSE copies, which only exist if gate 4 actually ran.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

gate_begin "log-hygiene"

# ---- static wiring: the readiness-predicate ratchet ---------------------
#
#  DELIBERATELY BEFORE the log check below, so a missing log can never SKIP
#  it.  This gate had no source assertions at all until now -- it graded logs
#  and nothing else -- which is why the defect it guards could spread unseen.
#
#  THE DEFECT IT FREEZES: a readiness predicate matching a BARE ">" is
#  satisfied by the guest's own register dump, whose FIRST line is the
#  symbol line "  <...>" -- and that line ends in ">".  Line-buffered on a
#  pty, each line is its own flush, so a reader waking between line 1 and
#  line 2 returns SATISFIED WITH THE REGISTERS UNREAD.  Healthy host,
#  microseconds wide, and armed on every CPU family whose dump starts that
#  way (MIPS, PPC, SH, m88k all do).
#
#  THE CONVERSION HAS LANDED (#392), so EXPECT_BARE is now 0 and this is a
#  RATCHET AGAINST REGRESSION rather than against spread.  All 15 sites now take
#  a fresh mark before the write, require the FULL prompt in that slice, and
#  require the command's own echo first.
#
#  The converted predicate deliberately keeps the LITERAL endswith("GXemul>")
#  spelling, which is the idiom the ARM probes already use (arm_idle_probe.py:194).
#  A reviewer proposed a shared helper holding the prompt in a constant or a
#  regex; either would have broken this gate, though -- as a pass-2 seat pointed
#  out -- NOT by the same route, and the first draft of this comment conflated
#  them:
#      endswith(PROMPT)  -> counted, unrecognised -> fails the `unknown` check;
#      re.search(...)    -> not an endswith at all, so `unknown` never moves --
#                           it fails the anchored-site COUNT below instead.
#  Matching the house idiom kept the ratchet working with no redesign, which is
#  worth remembering the next time a "cleaner" abstraction is proposed for
#  something a static check is watching.
#
#  Exact equality, not a ceiling, and on purpose: a "<=" check would let the
#  number fall silently, and a silent fall is how you lose track of whether
#  the conversion actually happened.  Any movement in either direction must
#  be a deliberate edit here.
#  COUNTING IT PROPERLY, after a review pass named three ways to walk around a
#  naive grep: the single-quoted spelling, a variable or helper holding the
#  prompt, and probes living in a subdirectory the flat glob never visits.
#  A ratchet you can step around is worse than no ratchet, because it reads as
#  protection.  So:
#    - find RECURSIVELY, not "$HERE"/*.py;
#    - accept either quote style;
#    - and make the check CLOSED-WORLD: every .endswith() in the tree must use
#      one of the two KNOWN literals.  A third spelling -- endswith(PROMPT),
#      say -- is unknown, and unknown fails.  A helper module under regress/
#      is scanned like a probe: an endswith( line there with a known literal
#      is not "unknown" (the bare one still fails the bare row), and one with
#      an unrecognised argument fails "unknown".  What no count here
#      sees is WHICH probe a helper's test serves: a probe whose ONLY test
#      moved into a helper is listed promptless and the names row reds
#      (fail-closed), while a probe that keeps one call of its own can move
#      the rest into a helper with every row green (hygienecensusholes n3k,
#      n3k2; this said a helper's line was unknown until the census F3 pass,
#      codex and grok).  That converts "I grepped for the bad thing" into "I
#      enumerated everything and recognised all of it" -- for the spellings
#      these counts can SEE.
#      (*** 2026-09-23: this said it was "the only form that cannot be evaded
#      by inventing a new way to write it".  FALSE: every TEXTUAL count here
#      (bare, allends, full, unknown -- the token classifier is not one of
#      them) is LINE-based and keys on `endswith(`, so a space before the paren
#      (`endswith (">")`) or a backslash continuation between the name and
#      the paren removes a call from all of them (both measured on copies,
#      controls_f2 e_e9 and controls_c5 t_bsl).  Filed as hygienecensusholes
#      e9, ranked first; the census F3 pass widened it from one spelling to
#      this LINE-based class (glm, agy, the kimi substitute).  And the
#      comment filter drops every PHYSICAL line that begins with `#`: code on
#      such a line (after a closing triple quote, or in an f-string field) and
#      a whole file saved with CR-only line endings (grep then sees one line,
#      beginning `#!`) escape too -- measured, the census F4 pass (the Opus
#      seat: hash_line, cr_only), filed with e10.  The census is closed-world
#      over the literal spellings on the physical lines it keeps, not over
#      the method. ***)
EXPECT_BARE=0
EXPECT_UNKNOWN=0
#  CODE ONLY.  The first version of this check counted a line of PROSE -- a
#  comment in arm_flags_probe.py that discusses endswith() -- and reported an
#  unrecognised spelling that does not exist.  A check that fires on its own
#  documentation trains the reader to ignore it, so full-line comments are
#  stripped before anything is counted.  (Known limit, stated rather than
#  hidden: an endswith() sitting after code on the same line as a trailing
#  comment is still counted as code, which is the safe direction.)
#  readiness_predicate_test.py is EXCLUDED here and pinned separately below.
#  It is the offline truth table for #392, so it necessarily CONTAINS the two
#  broken spellings -- demonstrating them is its whole job. Counting them with
#  the live sites would make the ratchet permanently red.
#
#  This is a FAIL-CLOSED exception, not a hole: the file is named exactly, and
#  its own contents are asserted below, so it cannot quietly stop testing what it
#  claims to test. A loose `grep -v test` would have been the wrong shape -- it
#  would silently exempt any future file with "test" in its name.
#  *** SCOPE, MEASURED 2026-08-29: `regress/artifacts/` IS PRESERVED EVIDENCE, NOT LIVE
#  HARNESS CODE, and leaving it in scope was a defect in BOTH directions. ***
#
#  *** THE NUMBERS THAT WERE HERE WENT STALE INSIDE THIS VERY DIFF, so they are
#  replaced by their DERIVERS.  An earlier draft froze 138 / 59 / 59; this round then
#  added wdc_latch_census.py and the true values became 139 / 60 / 60 -- a frozen count
#  in a comment ABOUT counting, wrong before the commit that wrote it had landed.
#  Caught by the codex seat. ***
#
#      find . -name "*.py" | wc -l                             the OLD recursive scope
#      find . -name "*.py" -not -path "*/artifacts/*" | wc -l  the NEW one
#      ls *.py | wc -l                                         the flat glob
#      grep -l "pty.fork" artifacts/*/*.py artifacts/*/*/*.py  the invisible copies
#
#  THE LOAD-BEARING FACT IS THE EQUALITY, NOT THE VALUES: recursive-minus-artifacts
#  equals the flat glob, which is what makes this the right exclusion -- it ALIGNS the
#  censuses instead of moving any of them.  Re-derive rather than quote; if the two
#  ever differ, that difference is the finding.
#
#  Two censuses recursed while a third used a flat glob -- which is evasion route #3
#  that this file condemns ninety lines above.  TEN pty-forking promptless probes sat
#  under artifacts/, invisible to the denominator, to the promptless pin and to the
#  comm -13 offender-naming: invisible to the entire mechanism built to find them.
#
#  AND THE HAZARD WAS SCHEDULED IN THE OTHER DIRECTION.  CLAUDE.md MANDATES frozen
#  probe copies for a comparison run; copying one converted probe into artifacts/
#  takes conv_anchor 23 -> 24 and reds this gate -- so the next round to freeze a
#  probe would have gone red FOR OBEYING THE CARRIER.
#
#  RECURSION IS KEPT so a genuinely new subdirectory is still scanned; only the
#  evidence archive is excluded.  Measured a NO-OP on every pinned count today.
py_code() { find "$HERE" -name '*.py' -type f ! -path "$HERE/artifacts/*" \
                 ! -name 'readiness_predicate_test.py' -print0 2>/dev/null | \
            xargs -0 grep -h "endswith(" 2>/dev/null | grep -v '^[[:space:]]*#'; }
#  -o, so these count OCCURRENCES and not LINES.  With -c a single line holding
#  two different spellings counts once in each of the three totals and drives
#  `unknown` NEGATIVE -- a subtraction is only meaningful if all three terms
#  count the same kind of thing.
bare=$(py_code | grep -o "endswith([\"']>[\"'])" | wc -l)
#  Every endswith( in code, minus the two we recognise: the bare prompt above
#  and the correct full prompt.  Anything left is a spelling nobody reviewed --
#  including endswith(PROMPT), wherever it sits under regress/ (a helper module included).
allends=$(py_code | grep -o "endswith(" | wc -l)
full=$(py_code | grep -o "endswith([\"']GXemul>[\"'])" | wc -l)
unknown=$((allends - bare - full))
check "readiness: bare-prompt sites frozen (#37)" "$bare" "$EXPECT_BARE"
check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN"

#  ---------------------------------------------------------------------------
#  *** THE THREE COUNTS ABOVE ARE CLOSED-WORLD AND STRUCTURALLY CANNOT SEE A
#  PROBE WITH NO PROMPT DETECTION AT ALL. ***  py_code() concatenates every
#  `endswith(` line across the tree, so a file containing ZERO of them
#  contributes to no counter and passes invisibly.  A ratchet built to catch
#  probes with BAD prompt detection is blind to probes with NONE -- which is
#  the larger set: SEVEN of the 33 pty-forking probes have no prompt
#  detection whatever.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Some current PTY probes are
#  classified as promptless. The ratchet pins their grandfathered set by count and name.  (hgatehygiene:F12:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#
#  The fix is the one this project applies to every phantom-zero: ENUMERATE THE
#  DENOMINATOR FIRST.  Count the pty-forking probes, then the promptless subset,
#  and compare that subset against an explicit list.
#
#  *** IT IS A RATCHET, NOT A REJECT, AND THAT IS NOT A COMPROMISE. ***  EVERY
#  current probe is promptless, so "reject any file lacking a predicate" would
#  redden the whole battery PERMANENTLY -- a red no edit can clear, which this
#  project has already paid for once and which destroys the credibility of every
#  other row in the run.  The grandfathered set is named exactly, so it cannot
#  quietly grow; a NEW promptless probe fails, and converting one is a
#  ratchet-down that must edit this list.
#
#  Provenance: a codex seat named the enumerate-first shape on the
#  probetimebased panel; the ratchet-not-reject refinement is the adjudication's,
#  after it checked what a reject-all would do to the current set.
#  *** BOTH PINS BELOW WERE RED AT HEAD UNTIL 2026-08-27, FOR THE SAME CAUSE, AND NOBODY
#  HAD SEEN IT. ***  Derived with this gate's own commands, not estimated:
#
#      EXPECT_PTY_PROBES   pinned 33   actual 35
#      grandfathered set   pinned  7   actual  9
#
#  The two extra files are `asic_badaddr_probe.py` (#463) and `wdc_flood_probe.py` (#464).
#  Both were added AFTER the pins were last set and neither pin was bumped.  The weekly
#  battery runs Sundays, so the red had not surfaced -- and when it did it would have been
#  mis-attributed to whatever change triggered that run.  That is the same class #486 closed
#  for `overrun x2` on the same day: a scored row red for an unrelated, already-diagnosed
#  reason.  Found by a panel seat re-deriving the pin rather than reading it.
#
#  *** ADDING THEM TO THE GRANDFATHERED SET IS NOT A BYPASS, AND THE DISTINCTION IS THE
#  WHOLE POINT OF THE ROW. ***  This list is not `probes we forgive`; it is `promptless
#  probes we KNOW about`, and the check's job is to NAME any that appear unnoticed (the
#  `comm -13` below).  Both new entries are promptless for exactly the reason the five
#  already listed are -- they free-run to a breakpoint, and only a breakpoint hit returns a
#  prompt, as `sh_intprio_probe.py` records in its own comment.  So they belong in the set,
#  with the reason written down rather than the count quietly raised.
#
#  *** THAT STATED REASON WAS WRONG ABOUT ITS OWN SET, AND IT SENT A READER TO THE WRONG
#  ONE OF THE TWO DISPOSITIONS THIS ROW OFFERS.  Censused member by member 2026-08-29,
#  independently by three seats (codex, opus5, and the main loop), all agreeing: ***
#
#  *** THESE CATEGORIES OVERLAP.  THEY ARE NOT A PARTITION, AND AN EARLIER DRAFT OF
#  THIS BLOCK PRINTED THEM AS ONE -- 3 + 8 + 1 = 12 over a NINE-member set.  Caught on
#  pass 2 by the glm and agy seats, on the arithmetic. ***
#
#      wall-clock BUDGET-DRAIN readiness .... 11 of 11   a `while ... time.time() ...` loop
#        of which ALSO free-run to a breakpoint  3       sh_intprio, sh_iprbcd, wdc_flood
#      NEITHER ............................... 0
#
#  *** THIS CENSUS HAS NOW BEEN WRONG THREE TIMES AND EACH ERROR WAS A DIFFERENT
#  SHAPE.  Recorded because the third one is the instructive one. ***
#    (1) the ORIGINAL claimed a single universal reason ("they free-run to a
#        breakpoint") that was true of 3 members.
#    (2) MY FIRST CORRECTION printed 3 + 8 + 1 = 12 against a NINE-member set --
#        it read as a PARTITION when the categories overlap.  Caught on the
#        arithmetic by the glm and agy seats.
#    (3) MY SECOND CORRECTION said drive_guest.py is NEITHER.  It is not: it
#        budget-drains at `expect()` and its sibling, spelled
#        `while time.time() - t < timeout:`.  I had grepped for the literal
#        `time.time() < end`, which is ONE SPELLING of the mechanism, and
#        measured the spelling instead of the thing.  Caught by opus5.
#
#  *** THAT IS THIS ROUND'S OWN DEFECT, COMMITTED IN THE COMMENT DESCRIBING IT:
#  counting a TEXTUAL FORM where a PROPERTY was meant. ***  It is why the row-5
#  replacement counts set/read BALANCE rather than occurrences of a spelling.
#
#  drive_guest.py IS in the promptless list, and for a reason that is about the
#  CENSUS rather than about readiness: its `boot_progress()` matches with
#  `re.search`, which `grep -L "endswith("` cannot see.  That is why it is
#  LISTED -- not how it waits.  The two axes were conflated by (3).
#
#  Measured per member over the CURRENT eleven: breakpoint is a strict SUBSET of
#  budget-drain, so the set is covered by budget-drain alone and "neither" is empty.
#
#  So the mechanism ALL ELEVEN share is BUDGET-DRAIN --
#  readiness by elapsed time rather than by prompt -- and the two probes added below share
#  it BYTE-FOR-BYTE with the already-listed gdrom_default_probe.py.
#
#  *** drive_guest.py IS BUDGET-BEARING TOO; what is distinct about it is why it is
#  LISTED, not how it waits. ***  It is
#  classified promptless only because `grep -L "endswith("` cannot see REGEX readiness:
#  its boot_progress() uses `re.search(pat, buf)`.  This gate's own comment already
#  anticipates that -- "re.search(...) -> not an endswith at all, so `unknown` never
#  moves" -- so the honest correction states the CENSUS rather than swapping one
#  universal claim for another.  A per-member reason, not a dominant one.
#
#  The grandfather-with-a-reason discipline is UNCHANGED; only the reason is repaired.
#  *** BOTH PINS RAISED 37->41 AND 11->15 ON 2026-08-31, AFTER RE-DERIVING THEM WITH THIS
#  GATE'S OWN COMPUTATION RATHER THAN APPROXIMATING IT.  Four pty-forking probes had been
#  added since the pins were set, all four promptless, so both pins were short by exactly
#  the same four -- which is the arithmetic that makes this one event and not two. ***
#
#  Left alone, the next weekly battery reds TWO rows in this gate, and a failed gate is a
#  failed battery.  This project has already had a battery go RED AND UNREAD FOR FIVE DAYS.
#
#  *** PER-MEMBER REASONS, NOT A DOMINANT ONE -- the discipline this block already demands
#  of itself, and the four do NOT share a reason.  They fall into two groups: ***
#
#  BREAKPOINT-DRIVEN, i.e. promptless for exactly the reason the existing members are --
#  they free-run and only a breakpoint hit returns a prompt:
#    wdc_addtoinbuf_probe.py   its own comment states it: "The probe therefore breakpoints
#                              and continues."
#    wdc_altoffset_probe.py    sends `breakpoint add 0x%x` at HALT_ADDR and continues.
#
#  TIME-BASED DRAIN, which is a WEAKER reason and is recorded as such rather than folded
#  in with the others -- these wait `while time.time() < end` around select() with no
#  prompt predicate at all:
#    gdrom_cond_probe.py
#    sgi_re_width_probe.py     *** ADDED BY #497 ON 2026-08-30, i.e. BY THE SESSION THAT
#                              RAISED THIS PIN.  Disclosed rather than absorbed. ***
#
#  The second group is the live defect tracked by the `probetimebased` queue row.  Listing
#  them here does not forgive them: this set is `promptless probes we KNOW about`, and the
#  `comm -13` below exists to NAME any that appear unnoticed.  A probe in this list with a
#  weak reason is tracked; the same probe absent from it is invisible.
#
#  PROVENANCE, DERIVED FROM git RATHER THAN ASSUMED -- because "both pins are short by the
#  same four" is an assumption until the sets are compared.  Against d9efd33, the commit that
#  last set EXPECT_PTY_PROBES=37 (VERIFIED: `git show d9efd33:regress/gate_hygiene.sh'):
#
#  *** THIS NUMBER READ 38 UNTIL #500 pass 11, AND THE #500 CHAIN IS WHAT BROKE IT.
#  It was 37, which was CORRECT, and a comment edit in this chain changed a right
#  number into a wrong one.  That is the carrier's "a correction is not safer than
#  the thing it corrects" class, in its worst direction: not a stale number left
#  standing, but a CORRECT one overwritten. ***
#
#    non-artifact .py under regress/ :  60 -> 66   (SIX new files, not four)
#    of the six, pty.fork            :  FOUR       gdrom_cond, sgi_re_width,
#                                                  wdc_addtoinbuf, wdc_altoffset
#    of those four, endswith(        :  ZERO       so all four are promptless
#    not in the denominator          :  wdc_altoffset_4bit_probe.py,
#                                       wdc_altoffset_sig_probe.py -- they fork no pty
#
#  So both pins move by the SAME four files, +4 each, and the two extra new probes are
#  correctly outside the denominator.  Had one of the six been a pty probe WITH readiness,
#  the two deltas would have differed and this raise would have been wrong.
#
#  NEGATIVE CONTROLS RUN BEFORE COMMITTING (recorded, not asserted): with the four added
#  both rows go green; removing any ONE of the four reds the promptless row again with
#  got=15 want=14, so the check still fires rather than having been switched off.
#  *** RAISED 41 -> 42 ON 2026-08-31, AND IT IS THE SECOND TIME IN ONE SESSION THAT A ROUND
#  OF MINE ADDED A PROBE AND LEFT THIS PIN SHORT. ***  The 42nd is
#  `sgi_de_width_probe.py', shipped by #498 hours after the same session raised this pin
#  37 -> 41 for exactly this reason.  The weekly battery of 2026-08-30 18:00 had ALREADY
#  red on the earlier instance (got=40 want=37, got=14 want=11) and that verdict sat unread
#  for ten hours; this one was caught by running the dead-man switch rather than by waiting
#  for Sunday.
#
#  *** THE LESSON IS NOT `BE MORE CAREFUL'.  A ROUND THAT ADDS A pty-FORKING PROBE MUST
#  RAISE THIS PIN IN THE SAME COMMIT ***, because the gate cannot fire until the weekly
#  battery runs -- so the feedback arrives up to seven days after the mistake, by which time
#  the round that made it is closed.  Re-derive, never transcribe:
#    find regress -name '*.py' ! -path '*/artifacts/*' | xargs grep -l pty.fork | wc -l
#
#  *** BOTH HALVES WERE STALE, NOT ONE.  An earlier draft of this very comment asserted that
#  the promptless half `needed no change' because #498 had added the probe to the list below.
#  IT HAD NOT.  Checked before committing: the list held 15 members and the measured
#  promptless set held 16, the extra being sgi_de_width_probe.py -- so that check would have
#  red too, at got=16 want=15. ***
#
#  The retraction is kept because the near-miss is the point: I wrote a confident claim about
#  a list, in a comment, WITHOUT OPENING THE LIST -- one line after correcting a stale pin
#  caused by the same habit.  The check that caught it cost one `grep -c`.
#  *** RAISED 42 -> 43 BY #499, IN THE SAME COMMIT THAT ADDS THE PROBE. ***  The 43rd is
#  `sgi_re_unmapped_probe.py'.  This is the THIRD raise in one session and the FIRST that
#  did not arrive as a surprise: the two before it were found by the weekly battery and by
#  a re-derivation hours after the fact, because this check cannot fire until the battery
#  runs, so the feedback lands up to seven days late -- after the round that caused it has
#  closed.  The obligation was written into
#  regress/artifacts/sgireunmapped/killtable_20260831/port/WIRING_OBLIGATIONS.md at wiring
#  time and predicted BOTH pins correctly.
#  *** RAISED 43 -> 44 BY #500 pass 11, AND THE RAISE IS THE FINDING: #500 ADDED A
#  pty.fork PROBE, EDITED THIS COMMENT TO NAME IT, AND NEVER TOUCHED THE PIN.  So
#  `readiness: pty-probe denominator' HAS BEEN FAILING SINCE 840f3d0. ***
#
#  The 44th is `sgi_de_primop_probe.py'.  Measured before the edit, with the gate's
#  OWN enumerator rather than a flat glob:  _ptyn = 44, pin = 43, check FAILS.
#
#  *** WHY NOBODY SAW IT, and this is the part worth carrying: THIS CHECK ONLY RUNS
#  IN THE FULL WEEKLY BATTERY, AND THE WEEKLY BATTERY IS DISABLED BY OWNER CHOICE.
#  A disabled battery produces NO RED ROW ANYWHERE -- nothing can observe its own
#  absence.  The checkpoint has carried that hazard as a standing warning for days;
#  this is its first MEASURED instance, and it cost a red gate that shipped in nine
#  consecutive commits without a single signal. ***
#
#  DERIVE IT, never transcribe it -- a count in a durable record names its deriver:
#
#      find regress -name '*.py' -type f ! -path 'regress/artifacts/*' \
#          | xargs grep -l 'pty.fork' | wc -l
#
#  (The `! -path artifacts' exclusion is load-bearing: the artifacts tree holds
#  FROZEN probe copies, which are evidence rather than gate material.)
#  *** RAISED 44 -> 46 BY pcc2widthkills, IN THE SAME COMMIT THAT ADDS THE TWO FILES --
#  pcc2_width_witness.py and pcc2_width_probe.py, both pty.fork, both promptless (fixed
#  timeouts, no endswith( predicate).  Written into the checkpoint at the moment the
#  witness was created, because #500 added a probe and moved NEITHER census, and it took
#  two passes and three seats to find. ***
#  *** 46 -> 73 ON 2026-09-23 BY ONE BULK RE-DERIVATION, BY OWNER RULING (hygienecensus; ledger row
#  stateaudit0923).  The pin had sat at 46 since b78bb0f (2026-09-03) while committed pty probes grew to
#  70, so this gate was RED AT HEAD -- measured on a pure export of HEAD's regress/, not inferred.  73 =
#  those 70 plus THREE UNTRACKED probes that lie in the tree and are counted as they sit, because the
#  census counts files, not commits: crime_width_probe.py (#529), arm_msrmode_probe.py (armmsrmodekill)
#  and lca_isaphys_probe.py (#540).  The owner chose to count all three in this denominator (2026-09-23,
#  "count all"); grandfathering crime_width_probe.py as PROMPTLESS is the part the ruling did not name -- it was
#  reported to the owner as a third name, not assumed authorised.  Consequence, stated so nobody
#  meets it cold: until all three are committed, a FRESH CLONE counts FEWER than 73 (70 with none of them)
#  and reds THREE rows -- this one, the promptless count and the promptless-names row -- because all three are
#  grandfathered names that exist only in the working tree (measured on a copy with them removed: 70/73, 40/43,
#  names gone=the three).  Written by `tools/derive_hygiene_pins.sh --write`, never by hand. ***
EXPECT_PTY_PROBES=81
#  *** AND THE SAME PROBE BROKE A SECOND CENSUS IN THIS FILE, WHICH pass 11's OWN
#  REPAIR DID NOT FIX.  Found by the codex seat reviewing that repair. ***
#
#  `#500' added `sgi_de_primop_probe.py', and it broke BOTH pty censuses here:
#
#      readiness: pty-probe denominator            44 vs 43   <- pass 11 fixed this
#      readiness: promptless probes, grandfathered 18 vs 17   <- AND MISSED THIS
#
#  *** THAT IS THIS ROUND'S OWN HEADLINE FAILURE, COMMITTED INSIDE THE REPAIR FOR
#  IT.  Pass 11 diagnosed "I close one side of a symmetry and leave the mirror
#  open", raised the pin, and left the sibling census in the SAME FILE untouched --
#  a second red that shipped in the same nine commits and survived the pass that
#  was sweeping for exactly this. ***
#
#  Grandfathered DELIBERATELY, which is one of the two dispositions this gate's own
#  message offers ("add prompt detection, or grandfather deliberately").  The
#  statement is TRUE rather than convenient: the probe's `session()' drives the
#  guest on fixed `settle'/`spin' timeouts and has no prompt predicate at all --
#  `grep -c "endswith(" sgi_de_primop_probe.py' is 0.  So it belongs on this list
#  exactly as the other seventeen do.
#
#  ADDING REAL READINESS IS FILED, NOT DONE, and the reason is scope rather than
#  difficulty: changing how that probe decides a command finished perturbs all 47
#  rows and owes a full re-measured kill table.  That is a round, not a records fix,
#  and doing it inside a records pass is how a green detector becomes unverified.
GRANDFATHERED_PROMPTLESS="pcc2_width_witness.py pcc2_width_probe.py sgi_de_primop_probe.py drive_guest.py gdrom_data_probe.py gdrom_default_probe.py
sh_intprio_probe.py sh_iprbcd_probe.py sh_pclock_probe.py sh_tlbmulti_probe.py
asic_badaddr_probe.py wdc_flood_probe.py gdrom_decline_probe.py
gdrom_toclen_probe.py wdc_addtoinbuf_probe.py wdc_altoffset_probe.py
gdrom_cond_probe.py sgi_re_width_probe.py
sgi_de_width_probe.py sgi_re_unmapped_probe.py
alpha_harness_probe.py alpha_pfnoffset_probe.py alpha_swpctx_v0_probe.py alpha_tbi_probe.py arm_bfx_width_probe.py landisk_aux_probe.py lca_badval_probe.py lca_confbus_probe.py lca_confwidth_probe.py lca_irqstub_probe.py lca_irqstub_uart_probe.py lca_isalane_probe.py lca_widewrite_probe.py maple_dmaaddr_probe.py pcc2_c040_probe.py sgi_mte_fill_probe.py sgi_re_colourdefault_probe.py sgi_re_randompixel_probe.py sgi_re_rgb_probe.py wdc_altdigin_probe.py
arm_msrmode_probe.py lca_isaphys_probe.py
crime_width_probe.py
sgi_mte_decline_probe.py
vme_default_probe.py
wdc_lba_probe.py
le_csrmask_probe.py
i8259_eoi_probe.py"
#  hygienecensus: tools/derive_hygiene_pins.sh --grandfather appended FIVE blocks to the list above; they are
#  named here by their FIRST NAME, never by position, because the next --grandfather appends another.
#  The block beginning `alpha_harness_probe.py` (derived 2026-09-19): 20 PROMPTLESS pty probes committed
#  between 2026-09-05 and 2026-09-18 that moved NO PIN -- they moved the promptless census (20 -> 40) and the
#  denominator (46 -> 66); four prompt-detecting probes committed in the same weeks (luna_absentcpu, m88k_exc,
#  arm_bdt, xscale_inten) took it to 70, while EXPECT_PTY_PROBES sat at b78bb0f's 46.  None makes a CODE-level
#  call of the ends-with method, which is this census's key: most use fixed waits or drain-to-EOF, and
#  alpha_tbi_probe.py has a real readiness wait the census cannot see (`"gxemul>" in buf[...].lower()`).
#  GRANDFATHERED, not converted:
#  converting a probe's readiness is its own round.  The block beginning `arm_msrmode_probe.py`
#  (2026-09-23, OWNER RULING): arm_msrmode_probe.py (armmsrmodekill) and lca_isaphys_probe.py (#540).  The
#  block beginning `crime_width_probe.py` (2026-09-23, pass 2 of this round, under the same ruling's
#  principle): crime_width_probe.py (#529), hidden from this census by a comment until pass 2 stopped the
#  classifier reading full-line comments (it reads tokens since the F2 repair).  All three were UNTRACKED and lying
#  in the tree, named so the census passes on
#  the tree the weekly battery runs.  (2026-10-18: crime_width_probe.py was committed by 7440e129 and
#  arm_msrmode_probe.py by 4f908ad5; lca_isaphys_probe.py still lies untracked.)  The block beginning
#  `sgi_mte_decline_probe.py` (2026-10-18, #567): #564 (e7fc97e6) committed that promptless probe -- fixed
#  waits, no readiness read -- and moved neither census, so this gate would have reddened at the next battery;
#  #567, adding its own pty probe, could not re-derive its pins while it stood, because --write refuses a
#  promptless probe that is neither grandfathered nor prompt-detecting.  Grandfathered on the 2026-09-19
#  precedent; converting its readiness is its own round.  The block beginning `vme_default_probe.py`
#  (2026-10-21, #568): its pty driver DOES wait for the prompt -- `PROMPT in buf[0]' and
#  `buf[0].find(PROMPT, start)' -- a real readiness wait this census cannot see, as with alpha_tbi_probe.py,
#  because the key is a CODE-level call of the ends-with method.  Grandfathered by name, not converted; the same
#  --write moved EXPECT_PTY_PROBES 76 -> 77 (75 committed + this probe + lca_isaphys_probe.py, still untracked).
#  Re-derive, never hand-edit: `bash tools/derive_hygiene_pins.sh` (report),
#  `--grandfather NAME...` / `--release NAME...`, then `--write`.

#  *** THIS WAS THE THIRD POPULATION AND THE F2 EDIT MISSED IT.  Found by the agy seat
#  on pass 2. ***  py_code and probe_code were converted to recursive-minus-artifacts
#  while this line kept a FLAT GLOB -- so two censuses were aligned and a third was not,
#  which is the exact defect F2 exists to end.
#
#  It AGREES today (recursive-minus-artifacts == flat == 59) and that agreement is a
#  COINCIDENCE, not a property: a .py added in any NEW non-artifacts subdirectory would
#  be scanned by two censuses and missed by this one.  Equal counts are not an aligned
#  population, and reading the equality as safety is how the flat glob survived the
#  first repair.
#  hygienecensus F2: paths RELATIVE TO regress/, not basenames -- a probe in a subdirectory was classified by a
#  same-named top-level file (measured: a promptless copy at newsub/ read as prompt-detecting), and a bare xargs
#  split a filename holding a space.  NUL-safe as far as grep: `grep -l` prints one name per LINE, so a file name
#  holding a newline is not supported (and a name holding a space cannot be grandfathered -- the list is
#  space-separated; the deriver refuses it by name).  For every file in regress/ itself the relative path IS the basename, so the
#  grandfathered names are unchanged.
_ptylist=$(find "$HERE" -name "*.py" -type f ! -path "$HERE/artifacts/*" -print0 2>/dev/null \
           | xargs -0 grep -l "pty.fork" 2>/dev/null | sed "s|^$HERE/||" | LC_ALL=C sort)
_ptyn=$(printf '%s' "$_ptylist" | grep -c . )
#  hygienecensus (2026-09-23): THE CLASSIFIER READS PYTHON TOKENS -- regress/census_tokens.py, where a COMMENT, a
#  STRING or a DOCSTRING is not code.  It was a raw `grep -L "endswith("`, so text naming the method hid a
#  promptless probe: crime_width_probe.py's only such text was a comment this very round added (pass 2).  The
#  first repair stripped only FULL-LINE comments and said it "reads code" -- the F2 pass measured seven edits, on
#  five probe files, where a TRAILING comment, a string or a docstring changed the answer (the Opus seat's n1a-n1d,
#  n2a, n2b, n9).  A comment, a string or a docstring is never a "." NAME "(" sequence of tokens, so none of
#  those can hide a probe now; and the classifier keeps STATEMENT boundaries, so a method reference on one line
#  and a parenthesised string on the next is not a call (the closing pass, codex -- controls_c2/t_nljoin).  A file that cannot be read or tokenized is listed promptless (it cannot
#  be read, so it is not trusted).  The spelling counts above deliberately stay textual, so a comment or a string
#  that spells the method is counted -- the safe direction.  They see only the LITERAL `endswith(`: a space before
#  the paren passes every one of them (hygienecensusholes e9).  `printf '%s\n'`, not `'%s'`: $(...) strips the list's last
#  newline, and a line-reader then drops the last file -- measured by this round's own controls.
_promptless=$(printf '%s\n' "$_ptylist" | python3 "$HERE/census_tokens.py" promptless "$HERE" | LC_ALL=C sort)
_want=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '
' | grep -c . )
_got=$(printf '%s' "$_promptless" | grep -c . )

check "readiness: pty-probe denominator (enumerate FIRST)" "$_ptyn" "$EXPECT_PTY_PROBES"
check "readiness: promptless probes, grandfathered set only" "$_got" "$_want"

#  Name the offender rather than only the count -- a bare number tells nobody
#  WHICH file, and the whole point of the denominator is attribution.
#  hygienecensus pass 2: AND GRADE THE NAMES, not only the count.  The count row alone read 42 == 42 after one
#  grandfathered probe was swapped for a new promptless one (measured); the owner's ruling is "grandfather BY NAME",
#  so the set is what is graded.  LC_ALL=C on both sides: comm needs one collation.
_gfs=$(printf '%s' "$GRANDFATHERED_PROMPTLESS" | tr ' ' '\n' | grep . | LC_ALL=C sort)
_new=$(LC_ALL=C comm -13 <(printf '%s\n' "$_gfs") <(printf '%s\n' "$_promptless" | grep .) 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
_gone=$(LC_ALL=C comm -23 <(printf '%s\n' "$_gfs") <(printf '%s\n' "$_promptless" | grep .) 2>/dev/null | tr '\n' ' ' | sed 's/ $//')
check "readiness: promptless names == grandfathered names" "new=${_new:-none} gone=${_gone:-none}" "new=none gone=none"
if [ -n "$_new" ]; then
        echo "  NEW PROMPTLESS PTY PROBE(S) -- add prompt detection, or grandfather it"
        echo "  deliberately: tools/derive_hygiene_pins.sh --grandfather <name> (never by hand):"
        ( set -f; printf '    %s
' $_new )   # set -f: a tree file named with a glob character prints as itself (census F5 pass)
fi

#  THE POSITIVE HALF OF THE #392 CHECK, and it is the half that binds the offline
#  truth table in gate_offline.sh to the code that actually ships.  Counting only
#  the ABSENCE of the bad spelling is not enough: a site could be deleted, or
#  reverted to something that is neither the old form nor the new one, and the two
#  checks above would both stay green.  So count the three constructs the
#  conversion introduced and require all fifteen of each.
#
#  Exact equality again, and for the same reason as EXPECT_BARE: a ">=" would let
#  a site quietly disappear.  If a probe legitimately gains or loses a wait site,
#  this number is edited deliberately, in the same commit, by someone who looked.
#
#  14 -> 15 on 2026-08-16: m8820x_sites_probe.py.  It shipped in 9494c6a with the
#  anchored form and the echo guard but NOT the pinned call form -- so two of the
#  three counts went to 15 and this gate went red, correctly, on a commit that had
#  never been run past it.  The probe is converted rather than exempted, and the
#  conversion was not free: reordering wait()'s parameters turned an existing
#  positional wait(120) into mark=120, which is a real behaviour change and is
#  fixed in the same commit.  That is the argument for the exact-equality pin.
#  15 -> 16 on 2026-08-19: footbridge_sites_probe.py, the first reachability witness this tree
#  has ever had for a footbridge machine.  MEASURED with this gate's own probe_code() census on
#  a staged copy: conv_anchor, conv_echo and conv_mark all move 15 -> 16 while bare, unknown and
#  whole_full do not move at all.  The probe ships WITH the pinned #392 call form rather than
#  being converted afterwards -- which is the lesson of the m8820x entry above, where a probe
#  landed in 9494c6a carrying two of the three constructs and turned this gate red on a commit
#  that had never been run past it.
#  16 -> 17 on 2026-08-19: luna_intmask_probe.py, #438's witness.  *** AND THIS ENTRY IS THE
#  THIRD TIME THIS GATE HAS GONE RED FOR THE SAME REASON, ONE COMMIT AFTER THE SECOND. ***
#  cf4b083 added the probe carrying all three pinned constructs and did NOT move this number.
#  The commit ran gate 2 and the float selftest; GATE 6 NEVER FIRED, so the red was never seen
#  and shipped latent -- it would have failed the Aug 22 weekly battery as a hygiene regression
#  with a bookkeeping cause, which is the phantom-regression class this project already names.
#  Found by the flagship seat recomputing this gate's own probe_code() census read-only.
#
#  The m8820x entry above records this shape, the footbridge entry directly above records it
#  again, AND THE FOOTBRIDGE ENTRY WAS WRITTEN THE SAME DAY -- by the same operator, who was
#  warned about the coupling for THAT probe, handled it correctly, and then repeated it for a
#  different probe one commit later.  Reading a lesson is not the same as having it.
#
#  The structural fix, since three annotations have not been enough: a probe that ships in the
#  same commit as its gate wiring cannot skip this pin, because the wiring forces a gate run.
#  cf4b083 shipped the probe UNWIRED, so nothing made gate 6 fire.  See the luna88k block in
#  gate_arm.sh, added with this bump.
#  17 -> 18 on 2026-08-20: pit8253_latch_probe.py, #439's witness for pitlatch/pitclobber.
#  MEASURED read-only with this gate's OWN probe_code()/py_code() definitions, run before and
#  after staging the file: conv_anchor, conv_echo and conv_mark all move 17 -> 18 while bare,
#  unknown and whole_full do not move at all (0 / 0 / 2 both times) -- the same signature the
#  footbridge entry above records.  Bumped in the SAME edit that added the probe, which is the
#  coupling the three entries above went red for.
#  The probe ships UNWIRED.  Per the structural note directly above, that means nothing forces
#  gate 6 to fire, and an unwired probe is exactly what shipped latent in cf4b083 -- so this pin
#  is doing the whole job here and was verified by recomputation rather than by a gate run.
#  Wiring it into gate_arm.sh alongside footbridge_sites_probe.py is the follow-up, and it wants
#  an operator who can run that gate.
#  18 -> 19 on 2026-08-20: sh4_bsc_width_probe.py, #441's detector for sh4bcr.  MEASURED the
#  same way -- this gate's own probe_code()/py_code(), run before and after staging: all three of
#  conv_anchor, conv_echo and conv_mark move 18 -> 19 while bare, unknown and whole_full do not
#  move (0/0/2).  The same signature every entry above records.
#
#  IT DID NOT START THAT WAY, and the near-miss is the part worth keeping.  The probe first named
#  its local `mark` rather than `_mark`, so the fresh-mark guard was PRESENT but invisible to
#  conv_mark, which keys on `return wait(mark=_mark, ...)`.  Two counts went green and the third
#  went red -- and the first draft of THIS comment argued that was correct and blamed the census,
#  on the reasoning that renaming a local to satisfy a grep is the tail wagging the dog.  Wrong:
#  `_mark` is the idiom in every other pty probe in the tree, so the new file was the outlier.
#  Teaching the census a second spelling would have made it count substrings of the first.
#  19 -> 20 on 2026-08-20: fbpending_drain_probe.py, #442's rung-3 reproduction.  All three
#  counts move together after two corrections made in the same edit: the probe was renamed
#  `mark` -> `_mark` (the sh4markspell shape, one round old), and conv_mark's pattern was
#  extended to see the METHOD form, because this is the first class-based pty probe in the
#  tree and its guard was invisible to a pattern written for closures.
#  20 -> 21 on 2026-08-21: fbpending_witness.py, #442's rung-3 reproduction, COMMITTED as part
#  of that round's pass 2.  It had lived in _scratchpad/, so a clone could not re-run the
#  reproduction that licensed the fix -- the mrwstore2 shape, whose probe left no artefact at all.
#  All three counts move together (21/21/21): it uses the closure form and the `_mark` spelling,
#  so neither of the two corrections the previous entry needed applies here.
#  21 -> 22 on 2026-08-21: sh4_pcic_probe.py, #443's detector.  All three counts move together
#  (22/22/22) and bare/unknown/whole_full do not move (0/0/2) -- the signature every prior entry
#  records.
#
#  *** THIS PIN WAS LATENTLY RED AT HEAD BETWEEN 3f9ff56 AND THIS COMMIT, AND THE CAUSE WAS A
#  CONCURRENCY SLIP RATHER THAN AN OVERSIGHT ABOUT THE COUPLING. ***  A `git add -A regress/`
#  during the #442 pass-2 commit swept in a probe a background agent was still creating, so the
#  file landed WITHOUT its pin and WITHOUT this annotation.  That is the FOURTH recurrence of the
#  coupling these comments already document (m8820x, footbridge, luna_intmask, sh4_bsc_width) --
#  and the first caused by staging rather than by forgetting.
#
#  The structural note above says a probe shipping in the same commit as its gate wiring cannot
#  skip the pin, because the wiring forces a gate run.  `git add -A` defeats that by adding files
#  the author did not choose.  STAGE BY EXPLICIT PATH when a background agent may be writing into
#  the same directory.
#  22 -> 23 in the SAME commit: sh4pcic_witness.py, #443's rung-3 reproduction, committed
#  alongside its detector.  It is a SEPARATE artefact from sh4_pcic_probe.py and both belong in
#  the tree: the witness asserts the PRE-FIX symptom (so it correctly reads 15/30 now) and the
#  detector asserts the FIXED behaviour.  Grading one by the other's clauses is a category error.
#
#  Committing it is the mrwstore2 lesson: that round's rung-3 probe left NO ARTEFACT, so its
#  witness became a remembered grep and a later row had to re-cost the work.  #442's witness had
#  the same problem and was committed one commit ago for the same reason.
#  *** 23 -> 24 ON 2026-09-23, the same owner-ruled re-derivation.  luna_absentcpu_probe.py (committed
#  79cd12e, 2026-09-06) is anchored and echo-guarded, so those two censuses counted it (24) -- but its
#  send() spelled the fresh mark `mark=mark`, which the fresh-mark census does not read, so that one said
#  23 and the three #392 counts DISAGREED at HEAD.  The probe's rename to `_mark` (same change) makes the
#  three agree; the deriver refuses to write while they disagree, which is why the rename precedes the pin. ***
EXPECT_CONVERTED=26
#  One helper for all three, so they agree on WHAT they look at.  The first draft
#  used py_code() for the anchored count and a raw grep for the other two, which
#  meant a comment mentioning the echo guard would have inflated one count and not
#  the others -- a spurious mismatch with no defect behind it.  A seat caught it
#  while it was still latent.
#  Same scope as py_code above -- the two must agree, and a past defect came from
#  their populations diverging.
probe_code() { find "$HERE" -name '*.py' -type f ! -path "$HERE/artifacts/*" \
                    ! -name 'readiness_predicate_test.py' -print0 2>/dev/null | \
               xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
conv_anchor=$(probe_code 'resp.rstrip().endswith("GXemul>")' | grep -c .)
conv_echo=$(probe_code 'echo is not None and echo not in resp' | grep -c .)
#  ANCHOR THROUGH THE ECHO ARGUMENT.  The first version stopped at
#  'return wait(mark=_mark' -- a PREFIX -- so deleting ", echo=s if s else None"
#  from all fourteen sites left this count at 14 and every other counter
#  unchanged. A pass-2 seat MEASURED that mutant passing gate_hygiene,
#  gate_offline, gate_mips_rounding and gate_sh_rounding simultaneously: a
#  shipped fix with no detector, which is this project's worst vacuity class.
#  The comma is what makes the assertion an assertion.
#  ANCHOR THROUGH THE WHOLE EXPRESSION, not just as far as "echo=". A pass-2b
#  seat pointed out that the previous form still admitted
#      return wait(mark=_mark, echo=None)
#  which passes the argument and disables the guard in ONE WORD. This is the
#  THIRD tightening of this same count -- first it stopped at "_mark", then at
#  "echo=", now at the full conditional. Each time the surviving prefix was a
#  real substring of both the fixed and the broken code, which is exactly the
#  property a detector must not have.
#  *** EXTENDED 2026-08-20 FOR THE METHOD FORM, and narrowly on purpose given the history
#  in the paragraph above. ***  Every probe until now wrote `send()` as a closure over a local
#  `buf`, so the guard read `return wait(mark=_mark, ...)`.  fbpending_drain_probe.py is the
#  first CLASS-BASED probe in the tree: its guard is `return self.wait(mark=_mark, ..., 
#  timeout=timeout)`, which is not a spelling variation but a different construct, and the
#  pattern could not see it AT ALL -- the guard was present, correct, and uncounted.
#
#  That is a wider blind spot than the `mark`/`_mark` one filed as sh4markspell: a whole probe
#  STYLE was invisible.  The two additions here are `\(self\.\)\?` and an optional trailing
#  argument.  Both are anchored -- `mark=_mark` and the full `echo=` conditional still have to
#  be present and in order -- so neither re-opens the hole the three earlier tightenings closed:
#  a site that passes the argument, or drops the conditional, still fails to match.
conv_mark=$(probe_code 'return \(self\.\)\?wait(mark=_mark, echo=[a-z][a-z]* if [a-z][a-z]* else None[,)]' | grep -c .)

#  THE HOLE A PASS-2 SEAT FOUND, and it is the sharpest finding of the review:
#  the checks above catch a REVERT but not an ADDITION of the OTHER broken form.
#  A brand-new site spelled
#        if buf.rstrip().endswith("GXemul>"):
#  passes everything -- bare is still 0, the spelling is RECOGNISED so `unknown`
#  stays 0, and it is not the anchored form so conv_anchor stays 14.  Yet #392
#  MEASURED that exact configuration (full prompt, whole buffer) failing just as
#  completely as the bare one: arm B scored 0/80, byte-identical to arm A.
#
#  So count it explicitly.  The two that exist are arm_flags_probe.py:144 and
#  :645 -- known, filed, and deliberately out of #392's scope.  Pinning the count
#  at 2 turns that scope decision into a FAIL-CLOSED ALLOWLIST: those two are
#  tolerated, a third is not, and when they are finally converted this number
#  goes to 0 in the same commit.
#  *** 2 -> 3 ON 2026-09-23 BY OWNER RULING, AGAINST THIS BLOCK'S OWN DEFAULT -- recorded as an EXCEPTION,
#  not a precedent.  The third site is arm_bdt_probe.py:76 (committed 4dfc716, #524, 2026-09-12): its
#  `self.buf.rstrip().endswith("GXemul>")' raised the count to 3 in a commit that did not move this pin,
#  so this row was red at HEAD.  The block below says a new hit is never answered by raising the pin; the
#  owner chose to allowlist it BY NAME rather than convert it inside the census round.  Converting its
#  readiness to #392's anchored form is FILED (`armbdtreadiness`).  A count alone would let a site MOVE
#  between files unseen, so a second row pins each FILE WITH ITS OWN COUNT (WHOLE_FULL_FILES, `name:count`,
#  sorted under LC_ALL=C).  Pass 2 of this round MEASURED two holes in the first form of these rows (a set of
#  names let a site move between the two files; the pattern matched only the double-quoted spelling), and the
#  F2 pass two more in the repair (the rows counted LINES, so two sites on one line read as one, and a site kept
#  as a trailing comment after its conversion still counted).  Both rows now come from census_tokens.py: code
#  tokens only, either quote, any spacing, every OCCURRENCE.  Other spellings of the same test -- another
#  receiver name, `strip()`, a slice compare -- are the filed `hygienecensusholes`, not closed here. ***
WHOLE_FULL_FILES="arm_bdt_probe.py:1 arm_flags_probe.py:2"
EXPECT_WHOLE_FULL=3
#  *** ROW 3: SCOPED TO FILES THAT CAN DRIVE A REAL GUEST, rather than exempting a
#  filename.  Adjudicated 2026-08-29; the name-exclusion form was WITHDRAWN. ***
#
#  The allowlist below is FAIL-CLOSED over a pattern #392 MEASURED at 0/80, so the
#  disposition for a new hit is never to raise the pin.  The two that appeared are
#  `selftest_inactivity.py:87` -- a deliberately preserved negative control whose own
#  docstring says DO NOT FIX IT -- and `:102`, #467's correct shape.  NEITHER DRIVES A
#  GUEST: both read a Stub that pops a python list, so #392's failure mode (a real
#  guest's own output racing the predicate) cannot arise.  That file is also LIVE
#  APPARATUS -- gate_offline.sh runs it every battery -- so it must not be edited.
#
#  A filename exemption was the wrong shape and this file says so at :92-95 and
#  :347-348: an exemption must travel WITH a content pin on the excluded file.  Scoping
#  the POPULATION needs neither an exemption nor a companion pin, and it subsumes the
#  readiness_predicate_test.py case automatically.
#
#  THE POPULATION TERM IS FOUR ALTERNATIVES -- pty.fork, forkpty, pty.spawn, importing drive_guest (it said
#  "TWO" until 2026-09-23) -- and the drive_guest one is not hypothetical:
#  `selftest_absorb.py`, `selftest_budget.py` and `selftest_logdir.py` import
#  drive_guest and contain NO pty.fork literal -- measured -- so a pty.fork-only term
#  would let a guest-driving file out of the census.  None holds a whole-full site
#  today; the term is widened so that it cannot.
#
#  *** THE CLAIM IS SCOPED, NOT GENERAL, AND TWO SEATS SPLIT ON IT. ***  codex named
#  three files that drive the emulator with NEITHER spelling -- hpcabort_witness.py,
#  hpcmips_ctor_probe.py and sgi_eaddr_probe.py, through subprocess.run or GDB --args.
#  So this is NOT a general guest-driving census and must not be read as one.  grok
#  argued against widening to cover them and that is the disposition taken: they
#  cannot carry the #392 failure, which is a PTY READINESS RACE, and all three hold
#  zero `endswith(` in any case (measured).  Widening to processes that cannot exhibit
#  the defect would make this pin answer a question it is not asking.
#
#  DISCLOSED RESIDUALS, all real, none live today: `from pty import fork` with a bare
#  fork(); `import pty as p`; a statement-local import; `import regress.drive_guest`.  Censused at 0
#  apiece.  (`os.forkpty` was listed here too until 2026-09-23 -- the pattern MATCHES it.)  THE
#  PRESENT VALUE (3, pinned above) IS CORRECT; THAT DOES NOT ESTABLISH POPULATION COMPLETENESS.
#
#  `-print0 | xargs -0` matches both neighbours: a bare xargs finds ZERO files when a
#  path contains a space (measured).  No space in $HERE today; the neighbours' own
#  comment says the three must agree, so it agrees.
#
#  NO FILENAME EXEMPTION HERE.  readiness_predicate_test.py matches neither alternative
#  and holds zero whole-full sites, so scoping subsumes it -- an earlier draft carried
#  the exemption anyway, inert and un-companioned by a content pin, which is the shape
#  :92-95 condemns.  opus5 found it dead and it is gone.
pty_driving() { find "$HERE" -name '*.py' -type f ! -path "$HERE/artifacts/*" \
                     -print0 2>/dev/null \
                | xargs -0 grep -lE 'pty\.fork|forkpty|pty\.spawn|^[[:space:]]*(import|from) drive_guest' 2>/dev/null; }
pty_code() { pty_driving | tr '\n' '\0' \
             | xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
#  hygienecensus 2026-09-23: the allowlist BY NAME, WITH EACH FILE'S OWN COUNT -- `path:count` for every file
#  holding a CODE-token whole-buffer site (census_tokens.py; per occurrence), over the same pty-driving
#  population, paths relative to regress/, sorted under LC_ALL=C and space-joined.  The count is their sum.
whole_files=$(pty_driving | sed "s|^$HERE/||" | python3 "$HERE/census_tokens.py" whole "$HERE" | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')
whole_full=$(printf '%s\n' $whole_files | awk -F: 'NF > 1 {s += $NF} END {print s + 0}')
check "readiness: whole-buffer full-prompt sites (allowlist)" "$whole_full" "$EXPECT_WHOLE_FULL"
check "readiness: whole-buffer sites, per allowlisted file" "$whole_files" "$WHOLE_FULL_FILES"
check "readiness: anchored full-prompt sites (#392)" "$conv_anchor" "$EXPECT_CONVERTED"
check "readiness: echo guard present (#392)"         "$conv_echo"   "$EXPECT_CONVERTED"
check "readiness: send takes a fresh mark (#392)"    "$conv_mark"   "$EXPECT_CONVERTED"

#  PIN THE EXEMPTED FILE'S OWN CONTENTS.  readiness_predicate_test.py is excluded
#  from the census above because it deliberately contains the broken spellings;
#  that exemption is only safe while the file still HOLDS them.  If its two
#  negative arms were deleted the offline truth table would go green by testing
#  nothing, and the exclusion above would hide it.  So the exemption and this
#  assertion travel together -- an allowlist entry that checks what it exempts.
#  -o again, not -c: OCCURRENCES, not lines.  Same reason as above, and the
#  expected numbers are asymmetric for a real reason -- 2 bad arms, but 3 good
#  occurrences, because besides the two `full-*` arms the test also prints the
#  LEFTOVER demonstration line, which re-matches the prompt on purpose to show
#  that rstrip() erases the trailing space.  The first draft of this check
#  expected 2 and failed; the file was right and the expectation was wrong.
#  CODE ONLY here too.  The first version grepped the file RAW, so a seat
#  gutted both negative arms, dropped the two spellings into a single COMMENT
#  line, and the pin still read 2 and 3. The filter that this file already
#  applies sixty lines above was missing from the one check whose whole job is
#  to keep an exemption honest.
rpt="$HERE/readiness_predicate_test.py"
rpt_code() { [ -f "$rpt" ] && grep -v '^[[:space:]]*#' "$rpt"; }
check "readiness: truth table keeps its 2 bad arms" \
      "$( [ -f "$rpt" ] && rpt_code | grep -o 'endswith(">")' | wc -l || echo missing)" "2"
#  FIVE, not three: the two original full-* arms, the two late-prompt arms that
#  give the ECHO conjunct its behavioural coverage, and the leftover demo.
check "readiness: truth table keeps its good arms + leftover demo" \
      "$( [ -f "$rpt" ] && rpt_code | grep -o 'endswith("GXemul>")' | wc -l || echo missing)" "5"

#  ---------------------------------------------------------------------------
#  A CLASS RATCHET, not a bug fix.  Task from the R6 pass-2 kimi seat, whose
#  answer had gone unread for a day: "sweep for other divisions in
#  debug()/fatal() argument position with guest-writable operands -- ns16550 is
#  unlikely to be the only instance of that shape."
#
#  The shape is worth a ratchet because C evaluates an argument whether or not
#  the callee prints it, so a division there runs at EVERY verbosity.  A grep
#  cannot find it: the operator has to be in argument position with literals and
#  comments already stripped, and the call may span lines.  diag_div_sweep.py
#  balances the parens and does that; it also splits constant divisors (which
#  cannot be zero, so are not the shape) from drivable ones.
#
#  MEASURED 2026-08-16: 24 sites, 22 constant, 2 non-constant -- so kimi's
#  hypothesis is REFUTED, and the ratchet is what keeps the refutation true.
#    * dev_ns16550.c, anchor `115200 / d->divisor` -- the live one, filed `ns16550`.
#      The other 115200 in that file is `115200 / 9600`, a CONSTANT divisor and not
#      the shape, so anchor on the `d->divisor` form rather than on the number.
#    * diskimage.c, anchor `(int) (bytes_left % ct->sector_size)` -- NOT drivable:
#      every unsupported TRACK mode reaches a `goto fail` immediately following the
#      diagnostic anchored at `unsupported TRACK mode`, and `nr_of_pt ++` runs only
#      after that, so a counted track always carries 2048/2336/2352.  The plain
#      division -- anchor `nr_sectors = bytes_left / ct->sector_size` -- would fault
#      first regardless.
#
#  *** THESE WERE LINE NUMBERS UNTIL 2026-08-30 AND THREE OF THE FIVE HAD DRIFTED. ***
#  `dev_ns16550.c:79` had become a comment line (the division is at :181);
#  `diskimage.c:543` was wrong by 440 lines (:983); and `:819` named the LAST ARGUMENT
#  LINE of the diagnostic rather than the `goto fail` below it -- the
#  read-the-line-before-citing-it trap, inside a citation whose only job is to be
#  re-checked.  `:823` and `:974` were still correct, so this is drift and not a bad
#  transcription.  Every anchor above was verified to match EXACTLY ONCE when written;
#  the bare form `bytes_left % ct->sector_size` matches TWICE and is deliberately not
#  used.  An anchor that stops matching is LOUD; a drifted number is silent.
#  A THIRD site means someone added a new instance of the class: read it before
#  raising this number.
DIVSWEEP=$HERE/diag_div_sweep.py
if [ -f "$DIVSWEEP" ] && command -v python3 > /dev/null 2>&1; then
    dsout=$(python3 "$DIVSWEEP" 2>/dev/null)
    check "class ratchet: drivable divisions in diagnostic argument position" \
          "$(printf '%s\n' "$dsout" | grep -oE 'DIAG_DIV_NONCONST=[0-9]+' | cut -d= -f2)" "2"
    #  The denominator too: if the sweep silently stopped finding ANYTHING the
    #  count above would still read 2 only by luck, and a zero total is the
    #  classic vacuous green.
    #  *** 24 -> 21 ON 2026-08-29, AND IT IS A CONSOLIDATION, NOT THREE REMOVALS. ***
    #  NOT ONE INSTANCE OF THE CLASS LEFT THE CODE.  `7c9dd9e` (#462) merged FOUR
    #  one-division fatal() calls -- grep anchor `dma_reg[4 / sizeof(uint32_t)]` --
    #  into ONE fatal() carrying the SAME FOUR DIVISIONS as its arguments.
    #  DIAG_DIV_TOTAL counts CALLS carrying at least one division, so merging four
    #  into one moves the total while the division census is unchanged.  A round
    #  acting on the first reading would have hunted three removals that never were.
    #
    #  Attribution settled BY MEASUREMENT, because two seats disagreed (#490 vs #462):
    #      git show 7c9dd9e --format= -- <file> | grep -cE '^[+-].*dma_reg'  ->  9
    #      (the BARE `| grep -c dma_reg` form yields 11 -- it counts context
    #      lines too.  9 is the CHANGED-LINES count and is the right figure;
    #      the command printed here was the wrong one.  Caught by fable5.)
    #      git show fb0cc78 --format= -- <file> | grep -cE '^[+-].*dma_reg'  ->  0
    #
    #  *** CITED BY COMMIT AND ANCHOR, NOT BY LINE NUMBER, AND DELIBERATELY. ***  This
    #  sweep computes its printed line numbers from STRIPPED-text offsets indexed
    #  against the RAW file, so they run systematically small -- it reports the gdrom
    #  sites 400+ lines early, landing inside a comment block.  Its COUNTS do not
    #  depend on that and are sound.  Filed as `divsweeplines`; the remedy (a
    #  length-preserving strip) is measured to move the citations to their true
    #  call-start lines with the counts unchanged.  Do not paste its line numbers.
    #  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] The sweep derives
    #  call-start line numbers from newline-preserving stripped text; divsweeplines is resolved.  (hgatehygiene:F13:
    #  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
    #
    #  THE DOWN DIRECTION NEEDED ITS OWN INSTRUCTION AND NOW HAS ONE.  The rule above
    #  ("A THIRD site means someone added a new instance") is written for GROWTH.  A
    #  DECREASE is ambiguous: it can mean the code improved, or that the sweep quietly
    #  stopped finding things -- the vacuous-green shape this denominator exists to
    #  catch.  THE DISCRIMINATOR IS THE NUMERATOR: if DIAG_DIV_NONCONST still reads 2
    #  and names the same two sites, the sweep works and a lower total is real.  If
    #  the numerator moves too, suspect the TOOL before the code.  Then diff the site
    #  list against the last green tree AT FILE GRANULARITY, the lines being wrong.
    #
    #  FILED, NOT TAKEN HERE: a seat argued this should become a FLOOR, since an
    #  equality breaks on every legitimate de-fatalisation and de-fatalisation is this
    #  fork's whole queue.  The argument is good.  Converting it changes what the
    #  check PROVES, so it is not folded into a re-pin.
    check "class ratchet: the sweep still sees the whole call set" \
          "$(printf '%s\n' "$dsout" | grep -oE 'DIAG_DIV_TOTAL=[0-9]+' | cut -d= -f2)" "21"
else
    note "diag_div_sweep.py or python3 missing -- class ratchet NOT run"
fi

PLOG=$LOGDIR/pmax.ptylog
ALOG=$LOGDIR/arc.ptylog
[ -f "$PLOG" ] && [ -f "$ALOG" ] || \
    gate_skip "no logs from this run -- gate 4 must run first (it publishes them here)"

# ---- positive control --------------------------------------------------
# Without this the gate cannot tell "nothing went wrong" from "nothing happened".
# The floor is MEASURED, not guessed. A healthy run produces about 4,600 bytes on pmax
# (a plain serial console) and about 1,195,000 on arc (a VGA text console that repaints
# differentially, so it re-emits the screen constantly). An earlier draft used a single
# 20,000-byte floor for both and failed pmax on a perfectly good boot -- a false red, which
# is how gates get switched off. 2,000 is comfortably below the smaller rig and still far
# above the "empty or truncated file" case this control exists to catch.
for pair in "pmax:$PLOG" "arc:$ALOG"; do
    lab=${pair%%:*}; f=${pair##*:}
    check_min "$lab: log is substantial"   "$(wc -c < "$f")" 2000
done
# pmax sets the 8th bit on every console character; arc repaints differentially. Strip the
# high bit for pmax and accept either the raw arc log or gate 4's screen rebuild.
check "pmax: log proves a real boot (uid=0)" \
      "$(tr '\200-\377' '\000-\177' < "$PLOG" | grep -qa 'uid=0(root)' && echo yes || echo no)" "yes"
check "arc: log proves a real boot (uid=0)" \
      "$( { grep -qa 'uid=0(root)' "$ALOG" || grep -qa 'uid=0(root)' "$LOGDIR/arc.screen" 2>/dev/null; } && echo yes || echo no)" "yes"
echo

# ---- markers that must be ZERO -----------------------------------------
# Every pattern below was verified to exist as an emittable string in src/. Three did NOT
# survive that check and were removed rather than left in place looking like coverage:
#   'FIFO underrun'        -- 0 sites. The real string is 'FIFO overrun' (4 sites).
#   [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] 'FIFO underrun' -- 0 sites.
#   The real string is 'FIFO overrun' (2 emitting fatal sites in dev_asc.c).  (hgatehygiene:F14:
#   regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#   'INSTR: unimplemented' -- 0 sites. The token 'INSTR:' is in no format string at all;
#                             the real dyntrans marker is 'could not find physical'.
#   '{ asc: data in'       -- exists, but is NOT distress. See the bounded list below.
PATTERNS='panic
FATAL
zero-length
FIFO overrun
short DATA_IN DMA
short DATA_OUT DMA
unimplemented format
could not find physical'

printf "  %-28s %8s %8s\n" "marker" "pmax" "arc"
while IFS= read -r pat; do
    [ -n "$pat" ] || continue
    p=$(count "$PLOG" "$pat")
    a=$(count "$ALOG" "$pat")
    printf "  %-28s %8s %8s\n" "$pat" "$p" "$a"
    check "pmax clean: $pat" "$p" "0"
    check "arc  clean: $pat" "$a" "0"
done <<EOF
$PATTERNS
EOF
echo

# ---- the OTHER rigs' logs ----------------------------------------------
# This gate used to read only the two MIPS pty logs, so a panic in the m88k or SuperH
# guest left it green while the README claimed "any boot log". Gate 5's logs are scanned
# here too when they exist -- they are the newer, less-exercised rigs, which is exactly
# where a distress marker is most likely to be informative.
for rig in luna88k landisk; do
    rlog=$LOGDIR/drive_$rig.log
    [ -f "$rlog" ] || { note "$rig: no log from this run (gate 5 did not run it)"; continue; }
    while IFS= read -r pat; do
        [ -n "$pat" ] || continue
        c=$(count "$rlog" "$pat")
        [ "$c" != 0 ] && printf "  %-20s %-28s %s\n" "$rig" "$pat" "$c"
        check "$rig clean: $pat" "$c" "0"
    done <<EOF
$PATTERNS
EOF
done
echo

# ---- markers with a KNOWN NON-ZERO baseline ----------------------------
# '{ asc: data in, lenIn=.. lenIn2=.. }' (dev_asc.c:417) fires whenever a SCSI target has
# fewer bytes ready than the guest asked for. That is an ordinary occurrence -- measured
# at 1 on pmax and 5 on arc across a healthy OpenBSD 2.2 boot -- so demanding zero was
# simply wrong, and this gate failed on it the first time it ran.
#
# It is still worth watching, because the failure mode that matters is a FLOOD: round 40
# found #265's own diagnostic firing on every healthy boot, and that showed up only as a
# marker count. So the assertion is a CEILING rather than an equality -- generous enough
# that ordinary boot-to-boot variation cannot trip it, tight enough that a per-transfer
# flood will.
printf "  %-28s %8s %8s   %s\n" "bounded marker" "pmax" "arc" "ceiling"
BOUNDED_CEILING=50
for pat in '{ asc: data in'; do
    p=$(count "$PLOG" "$pat")
    a=$(count "$ALOG" "$pat")
    printf "  %-28s %8s %8s   %s\n" "$pat" "$p" "$a" "$BOUNDED_CEILING"
    check "pmax not flooding: $pat" "$([ "$p" -le "$BOUNDED_CEILING" ] && echo ok || echo FLOOD)" "ok"
    check "arc  not flooding: $pat" "$([ "$a" -le "$BOUNDED_CEILING" ] && echo ok || echo FLOOD)" "ok"
done

gate_end
exit $?
