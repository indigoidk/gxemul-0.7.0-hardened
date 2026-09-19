# Fable 5 seat -- #536/#537 final review + adjudication (2026-09-18, after the F2 pass)

FABLE_SEAT_ALIVE_20260918_536_537
claude-fable-5-1
# CHECKPOINT -- 2026-09-18 19:3x   HEAD: 3c41f01 records: 8bd97e4's pass 2 -- DOES NOT CLOSE; the width row covers one of twelve reachable cells, and the rule question goes to the §F2 pass and fable5

VERDICT: SHIP BOTH.  D1 UPHOLD (keep red, file fbnobuild) with two reasons corrected; D3 REFINE (NEW ships; BOTH is
optional, not owed, not tonight).  The post-packet repairs are right in substance -- every measured claim in the final
diff reproduces from its artifact.  What is wrong: (1) owner question 5(b) is FALSE as characterised -- the task is
ENABLED, State Ready, next run 2026-09-20 18:00; the "2 missed runs" is the scheduler's own count of runs it could not
START; (2) regress/artifacts/wiringcliff/r536_20260918/FINAL_BLOBS_MD5.txt (19:56) records a gate_arm.sh blob
(fdffe712...) that no file on disk carries -- the final staged blob (19:57) is 8f20f651...; (3) an agy F2 finding was
never adjudicated: check_probe_wiring.py:2151 says every probe in the block "prints a verdict token and exits nonzero
on failure", false of mk48 (no _PASS/_FAIL token, exit 0 always) and inside this round's own hunk; (4) the draft
CHANGELOG the checkpoint names as the record source carries four sentences this round has since falsified.
5(a) is right in substance, but "has been red since 09-03" is a reading of the code, not an observation -- and the
sharper half is that NO queue row carries those two exemptions.

## Q1 -- disagreements

D1 -- UPHOLD keep-red + FILE fbnobuild, two reasons corrected, scope widened.
  * lib.sh read: note() (:101) touches neither _fails nor _degraded; degrade() (:107) sets _degraded and gate_end
    returns EXIT_SKIP=77 (:115-117); run.sh maps 77 to SKIP and the battery ends REGRESS_PASS_WITH_GAPS exit 3, which
    nightly_check.sh scores bad.  So Opus's measurement is the whole warrant: a note-skip is a PASS rc 0.
  * "unreachable in the battery" is FALSE (codex): run.sh:82-96 runs every gate whatever the previous rc.  Honest form:
    reachable only when gate 1 already failed (battery already RED) or on a standalone bare-host run.
  * "the #442 lane already has a green path through a stale log" is CONDITIONAL: $LOGDIR persists across runs, so with a
    retained diff_fbpending_bound.log a buildless gate 2 was PASS before #537; with a fresh $LOGDIR the SC "ran its
    sentinel" row (gate_offline.sh:2274-2279) reds anyway.  #537's red is a net gain in the stale-log case only.
  * The scope reason ("touches #442's lane") is weak -- this round already edited that lane's verdict grep (:1299).  The
    real warrant: degrade in both lanes + log truncation + SC accounting is a gate-behaviour change owing two negative
    controls (buildless -> SKIP 77 with the SC row consistent; built -> unchanged), and nothing can be measured while the
    gates run tonight.  fbnobuild carries: degrade() both lanes; truncate the log before the main lane; the misattributed
    row name ("the detector still detects" printed for a link failure); SC sentinel accounting; F14's freshness clause
    (the lane trusts build/ blindly, absent or stale -- gate 1 rebuilds it from est/ and asserts 223 objects in the
    battery, standalone runs have no such control); and O7's stray regress/dev_footbridge.c, which is SILENT for the main
    lane (gcc searches the including file's directory first) and unreached by the SM lane (Opus's decoy), so the two
    lanes would silently test different code -- a one-line refuse-if-exists, filed, not noted.
  * kimi/grok/glm: red-on-bare-host is the lesser harm because it is loud and prints its cause; the note path measured
    PASS rc 0.  grok reversed on that evidence; I would too.

D3 -- REFINE.  NEW (22 cases, M5a ON the stamped date) ships.  Opus's matrix (out/f2_matrix.txt) settles it: the only
  mutant NEW loses is `!=`, and only for a checker commit made ON the stamped date, because M0/M2b read the real clock;
  `!=` expires every exemption on every other day, so production reds it on the next commit.  `<=` is the dangerous one
  (quiet every day but one) and NEW catches it deterministically (21/22, selftest_NEG_le_mutant_final.txt).  BOTH's
  cost is not the case, it is that every artifact this round measured (selftest_final 22/22, the two NEG controls, the
  precommit pin at :576) is of the 22-case layout, and re-measuring tonight contends with the running gates.  Not owed:
  no floor clause binds a checker's selftest, and the day-before row's only unique channel is a self-announcing mutant.
  File as optional (`m5dayb`), warrant = Opus's matrix; the shipped comment already discloses the clock-dependence.

Other dispositions, where I differ or sharpen: O1 in-round was right and is MEASURED (P0-P4; f2pin one-space-short ->
SETUP).  O5 refined as Opus refined it.  F14 stays NOTED but its clause goes into fbnobuild.  O7's stray include:
FILE, not NOTE (silent hazard).  Opus's "latent 15-char mk48 name" is wrong by one and there is NO trap: the probe's
`assert len(name) <= 15` with `%-16s ` guarantees >= 2 spaces, exactly what `^$v  ` needs.  codex's DATE_RE point:
FILE (`exemptcal`): `^\d{4}-\d{2}-\d{2}$` accepts 2026-09-99, production compares strings, and the selftest's
fromisoformat would raise on such a minimum -- a loud crash, not a false pass; pre-existing in production, new in the
selftest.

## Q2 -- which dispositions are wrong

1. 5(b) "DISABLED": schtasks and Get-ScheduledTask/Info agree -- Enabled True, State Ready, weekly trigger SUN 18:00
   enabled, NextRunTime 2026-09-20 18:00, LastRunTime 2026-08-30 18:00, LastTaskResult 1, NumberOfMissedRuns 2.
2. FINAL_BLOBS_MD5.txt: written 19:56, one minute before the last gate_arm.sh edit (the "false when it was written"
   mk48 comment, 19:57).  Its gate_arm.sh line names a blob that exists nowhere; the checker line (4ba4b71e) is right.
   L4: regenerate from the blob that is actually staged, at staging time.
3. agy's F2 finding, unadjudicated: check_probe_wiring.py:2151.  mk48_nvram_probe.py prints MK48_RESULT / MK48_LABEL /
   MK48_ELAPSED / MK48_WITNESS_DONE and falls off the end (exit 0 always); hpcmips does print a token and finish()
   returns 1 on fails.  The sentence is a context line of this round's hunk.  L4, one clause: the gate section scores
   mk48 by rows, not by a token.
4. The draft CHANGELOG (_scratchpad/changelog_536_537_DRAFT.md) is stale against the repairs: :18-19 tells the lane's
   story through "R4 every case bounded" (the shipped pin is R3; P0-P4 unmentioned); :41-42 "had EXPIRED" (the gate
   comment now says "false when it was written"); :49-50 "(minus one day / plus one)" (M5a runs ON the date); :51-52
   "both halves of that pairing are gone" (ONE half).  Not shipped yet, but it is the named record source.
5. O6's "md5-matched to the runs" is half true: t536/mk48_nvram.log == mk48_neg.log; t536/hpcmips_ctor.log matches
   neither preserved hpc log, because both preserved logs carry a driver-appended `HPC_RC=0` line the probe never
   prints (5,363 vs 5,356 B).  No check greps it; the record should say the preserved logs are driver-wrapped.

## Q3 -- post-packet repairs, from the final diff

Right in substance, each reproduced: the pin has exactly 8 spaces (37-char name in `%-44s` + one literal; measured
from the file) and Opus's f2pin shows one fewer -> SETUP; P0-P4 read as stated; selfmutant.py's timing cites
opus5_f2/SUMMARY.txt and reproduces it (n=10, 3.22-3.53 s / 1.69-1.87 s, 34.0x / 32.1x) with the old "~88x and ~190x"
past-tensed; exempt_expired is `\<` (:1184) so "RED the day after" is right; "the other five" now names them and dates
6014b7e; "earlier in this selftest" is right (M1-M3 at :2795-2807, M5 at :2815); precommit's "(22, pinned below)"
has its pin (:576); C2's "checks only the abort CLASS" matches hpcmips_ctor_probe.py:522 (`cls == ABORT_OTHER`); "the
probe's own row F3" resolves the dangling cross-reference.  Nits: gate_offline.sh's "Two things kept it out ... (2) it
links build/ objects" -- (2) is a requirement of the lane, not a cause of its absence; the gate comment's "(measured,
Opus seat, #537 F2 pass)" should name the file (opus5_f2/f2pin_SUMMARY.txt), per the score-claims rule.

## Q4 -- what all of us missed

FINAL_BLOBS_MD5.txt (Q2.2); the task is not disabled (Q2.1); the draft record's four stale sentences (Q2.4); SC_EXEMPT
has NO owner row (grep OUTSTANDING_BUGS for SC_EXEMPT / wdc_identify:2026 -> only a generic mention at :7107) -- codex
and grok found the red, nobody said it is untracked; mk48's token/exit-code vs the checker sentence (agy found it,
nobody ruled); and the run in flight: /tmp/gxregress/diff_fbpending_bound.log is being written (20:01:33), so tonight's
gate 2 is the FIRST run that can observe the SC row red -- expect it, and do not attribute it to #537.

## Q5 -- the two owner questions

(a) RIGHT in substance; refine the wording.  The row is "SELFCHECK manifest: no exemption is past its dated deadline OR
    malformed" (gate_offline.sh:2264-2266); exempt_expired compares `[ "$d" \< "$today" ]` (:1184) against
    `date +%Y-%m-%d`; both entries were set 2026-08-19 in 7e3b120 with the fortnight the owner chose for SM.  From
    09-03 the got is " ieee_store wdc_identify" against want "none".  But "has been red since 09-03" is a reading of
    the code: the last battery (08-30, verdict_20260830_180000.txt) had gate 2 PASS and predates the date; no round has
    run gate 2 since (no September block claims a gate-2 result; the last gate_offline.sh commit, 09-05, is a records
    batch), so tonight's run is the first observation.  The half worth putting to the owner: it is the SM cliff's twin,
    18 days later, with the same three dispositions -- discharge (ieee_store is blocked by design, "no comparator to
    feed"; wdc_identify needs the nine-row refactor, "a round, not a line"), re-date with a reason, or delete and take
    a permanent red on the coverage row -- and no queue row owns it.  The SM ruling was "fix, do not re-date".
(b) WRONG as characterised.  Measured: Enabled True, State Ready, trigger enabled, NextRunTime 2026-09-20 18:00,
    LastRunTime 2026-08-30, LastTaskResult 1, NumberOfMissedRuns 2.  The missed Sundays (09-06, 09-13) are runs the
    scheduler could not start -- the carrier's "Interactive only: a sleeping or logged-out machine skips it silently" --
    not a disabled task.  The 08-30 REGRESS_FAIL is gate_hygiene alone (readiness rows: pty-probe denominator got=40
    want=37, promptless grandfathered got=14 want=11), 15/16 PASS, and TREE_DIRTY=YES at 105c15c, so it describes no
    commit.  OUTSTANDING_BUGS:965 records the CLASS (the 08-23 red sat unread five days; LastTaskResult "still 1"); the
    08-30 hygiene red itself is filed nowhere (grep for its row text: nothing).  Owner questions, restated: (i) the
    hygiene denominators need re-pinning; (ii) the next run is Sunday 09-20 18:00 and fires only if the machine is
    awake and logged in; (iii) nightly_check.sh's newest verdict is 19 days old, so it has said NIGHTLY_CHECK_FAIL by
    its own age rule for that long -- is anyone reading it?

Seat record: fable5 (claude-fable-5-1), file-reading plus light measurement (md5, schtasks/Get-ScheduledTask, git
log/show, greps, one WSL `ls`); no gate, probe, build or precommit run; nothing written inside GXEMUL-SEC/, est/, build/,
build-asan/ or /tmp/gxsec-build.
