# CHECKPOINT -- 2026-09-19 10:3x   HEAD: f685d75 (peer records) > 9c28ca5 #539 receipt (7836071 = #539 n6, the footbridge IRQEnable read ACCEPTED)

## TWO SESSIONS SHARE THIS TREE AND INDEX.  "GXEMUL (2)" [e8a2bc] owns lcalenzerodrop, #530, every dev_lca.c row,
#540 (lcaisaphys), #541 (alphavmkill), #542 (alphaifetchkill), #544 (cxlaunch harness round).  This session GXEMUL
[087a90] owns the footbridge campaign (#539 shipped; next fbdeclinefive), fbnobuild, and the codex farm.
## INDEX: FREE (087a90 committed 7836071 + 9c28ca5 at 06:1x and released; peer notified).
## MACHINE: FREE from 06:08 (gate_arm done); the peer's #541 table 2 (/tmp/gx541) may start any time -- ask before any
gate/battery.  Weekly battery SUNDAY 2026-09-20 18:00: keep the machine QUIET from 18:00.

## BUILD TREES (two-part clearance RUN at 04:43, propagate539.out, now in regress/artifacts/n6/gate_20260919/):
  build/            e5d18154  part 1 CLEAN (dev_footbridge.c, dev_lca.c) part 2 FRESH   -- gate_arm PASS on it 04:44-06:08
  build-asan/       2b21cbfa  CLEAN / FRESH
  /tmp/gxsec-build  39966e0c  CLEAN / FRESH
  est/              source tree, part 1 CLEAN, part 2 N/A
  NO .MUTANT sentinel anywhere.  Scratch clones: /tmp/gx539 (fixed source == HEAD, restored, no sentinel; may be
  deleted), /tmp/gxagy539 (agy's copy, restored), peer's /tmp/gxkill540b, /tmp/gx541.

## UNCOMMITTED IN THE WORKING TREE (none mine except the never-commit tools):
  peer's / #529's: src/cpus/cpu_alpha_palcode.c, src/devices/dev_lca.c, dev_pcc2.c, dev_sgi_ip32.c, dev_sh4.c,
  src/include/thirdparty/mvme_pcctworeg.h, regress/gate_arm.sh (:1728+ crime_width orphan), gate_sh_rounding.sh,
  gdrom_default_probe.py, sh4_chcr_probe.py, tools/precommit_check.sh (manifest 31), tools/pipeline/check_probe_wiring.py
  (#529 MANIFEST hunks over HEAD's #539 entries), check_score_claims.py, check_boilerplate.py, adjudicate.sh.
  NEVER COMMIT: tools/{BRIEF_TEMPLATE.md,CLAUDE.md,PIPELINE.md,panel.sh}, tools/pipeline/fable_queue.md,
  regress/ppc_rldicl_probe.py, regress/artifacts/gdromdefault_461/, top-level regress/*.bin, run_*/disk.img.
  Commit technique for a file carrying foreign hunks: HEAD-based partial blob swapped in for the hook (commit539.sh).

## SEAT STATE (measured this night)
  * CODEX walled "usage limit ... 6:59 AM" (batch 6 lost mid-answer; RELAUNCH _scratchpad/cxfarm6_20260919/ after 06:59
    with q1 replaced by q1b_declinefive_reading.md; farm3 l1 battery pre-flight rerun; act on it before Sunday 18:00).
  * Anthropic Agent seats: the 03:40 session limit reset; BUT fable/opus agents fall back to opus-4-8 SILENTLY after a
    REFUSAL turn at the synthesis step (a classifier on the answer's vocabulary) -- ALWAYS run
    `python _scratchpad/agent_models.py <session-id>` on the agent before crediting; a REFUSED agent can be RESUMED via
    SendMessage with a short neutral follow-up and then answers on fable-5-1 (peer, measured).  #539's two fable agents
    were clean (71/71, 12/12).
  * kimi CLI: a brief above its 50 KB READ cap stalls it (looped on a 64 KB brief); re-fire with explicit line ranges.
  * agy: backgrounds its own build and exits (killed on exit) unless told "foreground only"; then it measures correctly.

## NEXT (this session): end-of-round triage done (8 rows filed, ledger/bugs/CHANGELOG written).  Next item: the
fbdeclinefive design brief (BRIEF_TEMPLATE, settled premises from #539: bridge retirement + M1 harness legs in the
same commit; five sites; K4 rows minus SDRAM); pass 1 after codex returns (q1b reading first).  Easy-resolvable
alternative queued: fbnobuild (codex L2 repair draft in _scratchpad/cxfarm3_20260919/out/codex_l2_fbnobuild_repair.txt).
Grades: 402 codex outcome grades attached (n1-n4); batch 6 (95 rows) to re-run.

## 10:3x -- #545 (fbdeclinefive) IMPLEMENTED, TABLED, PROPAGATED; gate_arm RUNNING.  OWNER 10:2x: session switched to OPUS 5;
## "hold adjudication" (Fable NOT fired until the owner says so); "stop any cron job; do anything that requires idle states"
## -> cron 25af26f5 DELETED, dynamic loop STOPPED.  No loop is scheduling this session now.
* Kill table 2 (09:03): clean -- every product mutant M1-M11 killed by the composite detector (M7/M8/M11 offline-only,
  M9 guest-only, as predicted); HEAD red 21/36 + differential dies at P1; FIX 36/36 + 111/111.  Table 1 had two
  INSTRUMENT defects (recorded).  Summary: _scratchpad/fbd5/impl/TABLE_SUMMARY.md; logs durable in
  GXEMUL-SEC/regress/artifacts/fbd5/killtable_20260919/ (84 files).  Pass-1 artifacts: .../fbd5/p1_20260919/.
* APPLIED to GXEMUL-SEC (6 files, byte-identical to what the table measured) and est/ (dev_footbridge.c).  Propagated:
  build/ d19184ee (== the table's FIX binary), build-asan/ 0c1fd857, /tmp/gxsec-build c9b4340a -- part 1 CLEAN, part 2
  FRESH, recorded in _scratchpad/fbd5/impl/propagate545.out; est/ part 1 CLEAN, part 2 N/A.  NO sentinel in any project
  tree.  gate_arm.sh in the working tree = HEAD + my footbridge hunk + #529's orphan section (commit via HEAD-based blob).
* gate_arm STARTED ~10:35 ALONE (bg bz2wq6aa0; _scratchpad/gates545/{ARM_TIMES.txt,gate_arm_545.log,rc_arm.txt});
  a read-only codex.exe (10:11, the HP-Mame SESSION, not the peer) was alive at start, recorded.  Peer told to hold wall-clock work until GATE DONE.
* PASS 2 briefs BUILT, NOT FIRED (panel after the gate -- panel seats contend): _scratchpad/fbd5/p2/brief_fbd5_p2.md (45.5 KB,
  file-reading seats; three probe diffs by path) + brief_fbd5_p2.packet.md (60.8 KB, Ollama sibling).  Launch:
  PANEL_KIMI_CLI=1 PANEL_FIRE_AGY=1 bash GXEMUL-SEC/tools/panel.sh C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/p2/brief_fbd5_p2.md
  + a dedicated codex adversarial job + an Opus measuring seat; Fable HELD by owner directive (record as held, not failed).
* Then: §F2, records (ledger_write545.py -- fill R2/OPUS2/FABLE2/CLOSURE/WITNESS; batch-7 grades attach there: 1394 match),
  bugs (bugs_draft545.md: armdesc3kill, armdacr2kill, fbirqsoftunimpl, fiqenableread dissent, hygienecensus), CHANGELOG,
  commit by name.  The COMMIT waits on the Fable hold (provisional-adjudication rule) unless the owner exempts.
* PEER after GATE DONE: #544 sweep, #541 3c, #542 dev runs, then the #542 KILL TABLE -- keep my panel OFF its probe phase (peer messages start/end; its legs have fixed 0.45-0.6 s waits and retry once on a stall).
* hygienecensus (HIGH before Sunday 18:00): pin-DERIVER WRITTEN (syntax only, not yet run -- gate in progress): _scratchpad/fbd5/hyg/derive_hygiene_pins.sh (evaluates the gate's OWN enumerators; report / --write / --grandfather FILE...; refuses on #392 count disagreement and on unnamed new promptless probes); lands as GXEMUL-SEC/tools/ in the census commit after #545; peer's lca_isaphys and
  alpha_vmkill (and maybe alpha_ifetch) to be grandfathered; luna mark=mark mine.  TREE_DIRTY question with the owner.

## 087a90 -- 12:4x STATE (restored: my 12:0x-12:3x notes sat below the peer's section and were lost in its 12:2x rewrite)
* gate_arm PASS 1058 (11:55) on the pre-repair tree; gate_offline PASS 348 (12:11) on the repaired tree (P=78, X=23, rows 134).
  Logs: regress/artifacts/fbd5/gate_20260919/.  Pin-DERIVER: _scratchpad/fbd5/hyg/derive_hygiene_pins.sh (report run OK).
* PASS 2: panel_20260919_115657 (8/8 answered); Opus measuring seat (VERIFIED opus-5): L2 floor breach -> 23 X-rows added,
  re-measured (impl/xtable/XTABLE.log), gate_offline pins them, H2 header sentence corrected.  Dedicated codex: L2 vs the
  134-row tree too (_scratchpad/fbd5/p2/CODEX_DED_TRIAGE.md, R1-R6/W1-W6/D1-D4).  Consolidation of all seats (Opus agent):
  _scratchpad/fbd5/p2/P2_FINDINGS.md (F1-F50, D1-D10; it scored the dedicated codex a failure because it read before the
  answer landed -- the answer EXISTS, 12.7 KB).
* NEXT: ONE repair diff (seeds fiq_status 0x60; X4 zero-data first access + legal zero Clear write; X3 extended to legal
  writes/timer reads; narrow 18c read value; N-order row; distinct-id gate pins; C4 pin; wrong records W1-W6 + F21-F40),
  re-measure offline + the sites probe in a clone, gate_offline again, then the repair's own pass 2.  Fable HELD by the owner;
  the COMMIT waits on the owner's word about the hold.

## 087a90 -- 12:5x: THE PASS-2 REPAIR IS IN THE TREE, table 3 offline half DONE, guest half + gate_arm OWED
* Repair (from P2_FINDINGS.md + CODEX_DED_TRIAGE.md): seeds fiq_status 0x60; X1 narrow 18c value, X3 widened, X4 zero-data first
  access, X5 legal zero Clear write (differential 149 rows); sites probe NO access-order row (37 rows) + 7 header corrections;
  pending probes H1 no-prompt-anywhere + arm-K paragraphs replaced; gate_arm pins: ROWS=37, distinct ids SC/SA, N, S, SF, NO, C4,
  count=1 boundary, display line; gate_offline pins 149/78/38; device comment (latch is set) -- NOT yet re-propagated.
* #539 WRONG RECORD found (F34): its F2 "E0-E6 distinct GREEN ids" gate fix was never committed (HEAD has the old form); the
  working tree has it; #545's commit carries it and the CHANGELOG says so.
* TABLE 3 (impl/table3/TABLE3.log): OFFLINE FIX 149/149; every mutant red except M9/Z9 (text-only, guest-only by design);
  floor (b) M1+M1b-M1e all die.  GUEST: FIX 37/37 PASS, then STOPPED at the peer's request (its probe legs); /tmp/gxfbd5c
  holds a .MUTANT (FIX source only) -- re-run the guest half (witness, drain, Z9, M1b-e) and restore.
* ORDER agreed with the peer: its two panels after PROBES DONE (~12:55-13:30); my guest half + re-propagation during them;
  then gate_arm ALONE (~13:30).  Then the repair's own pass 2 (short, scoped to the repair diff).  Fable HELD.

## 087a90 -- 13:1x: TABLE 3 COMPLETE, trees re-propagated, gate_offline re-PASS; WAITING for the peer's PANELS DONE -> gate_arm
* Table 3 guest half (13:03): FIX 37/37, witness/drain H1/H2 ok, Z9 red on NO, M1b-M1e red (arm S dies); clone restored,
  no sentinel.  Offline (12:5x): FIX 149/149, all mutants red except M9/Z9 (guest-only by design).  Artifacts:
  regress/artifacts/fbd5/table3_20260919/ (88 files).
* Re-propagated (13:04): build/ 9fa0c1f9 (== table 3's FIX binary), build-asan/ 0f0b4489, /tmp/gxsec-build d0c5946f, all
  part 1 CLEAN + part 2 FRESH; est/ CLEAN.  gate_offline PASS 348 (13:1x, pins 149/78/38).
* NEXT: on PANELS DONE -> `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gates545/run_arm_b.sh`
  ALONE (bg); then the repair's own pass 2 (brief scoped to the repair diff); records; commit on the owner's word (Fable HELD).

## 087a90 -- 13:2x: ADJUDICATION + REPAIR PASS 2 FIRED (brief _scratchpad/fbd5/p2r/brief_fbd5_f2.md, 42 KB; repair diff
## p2r/repair.patch 22 hunks md5 da9e8cf1 vs the exact pass-2 state p2r/p2base_frozen/)
* panel bg bjmj3m2xg (launch log p2r/f2_panel_launch.log); Opus measuring seat (answer -> _scratchpad/fbd5/opus_f2_20260919/
  OPUS_F2_ANSWER.md; VERIFY identity).  Fable HELD.  Then gate_arm ALONE (run_arm_b.sh) after BOTH sessions' panels.
* Since table 3: only the sites probe's send() COMMENT changed (F37) and PRETABLE/TABLE_SUMMARY got appended corrections.

## 087a90 -- 13:3x: CLASS CLOSURE X6/X7 SHIPPED IN THE TREE (differential 327 rows), table 4 CLEAN, gate_offline PASS 350
* Opus repair-pass seat (VERIFIED opus-5): 11 of 14 escapes of the 149-row detector -> same class as pass 2 (two consecutive
  passes) -> the class closure: X6 (108 cells, every declined access) + X7 (70, every legal access re-arms nothing).
* TABLE 4 (impl/table4/TABLE4.log; artifacts fbd5/table4_20260919/): FIX 327/327; all 50 mutants red except M9/Z9 (text-only,
  guest rows kill them) and F1 (guard on timer_control -- outside the DEPENDS-ON bound; guest kills it only because timer 1 is
  armed) -> DISCLOSE F1's class in the probe/differential contract.  gate_offline PASS 350 (pins 327/78/216/108/70).
* Adjudication panel (MY dir panel_20260919_131006 -- NOT 130115, which is the peer's): 7 answered + kimi CLI WALLED mid-answer
  (73 KB readable).  They reviewed the 149-row version.  Consolidation agent running -> _scratchpad/fbd5/p2r/F2_FINDINGS.md.
* STILL OWED: F1 disclosure; the consolidation's open items; gate_arm ALONE on the final gate file (after the peer's PANELS
  DONE); records; commit on the owner's word (Fable HELD).

## 087a90 -- 14:0x: gate_arm RUNNING ALONE (bg b88yt83lo, 13:35 -> ~15:00, _scratchpad/gates545/gate_arm_545b.log)
* Adjudication consolidated: _scratchpad/fbd5/p2r/F2_FINDINGS.md (G1-G33; no product defect).  DONE during the gate (offline
  files only -- gate_arm does not read them): G10 gate_offline pins = DISTINCT green row names (fb_distinct); G11 X8 wide seeds
  (differential 333 rows, FIX 333/0); G13 X4 comment + X3 row name.
* AFTER GATE DONE (do not touch gate_arm.sh or footbridge_sites_probe.py while it runs -- bash reads incrementally, and the
  gate runs the probe): G14 sites :106 "P-rows" -> X1/X6 and :259 "ACCESS-LOCAL"; R4 NO proves ORDER not emitter (probe +
  gate_arm comments); X8 truncation mutant (odata = irq_status & 0xff) must red; gate_offline re-run (pins 333/78/222/108/70/6);
  records incl. G15 (#539 CHANGELOG correction), G16 (table 3 = 35 mutants, table 4 = 49), F11 rationale (no gate reads the
  pending probes' verdicts; drain is REPORT-ONLY), F40 wording.  Comment-only probe edits after the gate do not change its
  measurement; say so in the record.

## 087a90 -- 15:0x: #545 COMPLETE AND GREEN, **COMMIT HELD BY OWNER** ("Hold the commit", asked 15:0x after Fable was held)
* gate_arm PASS 1061 (14:51, repaired gate file; later edits comment-only), gate_offline PASS 351 (15:0x, pins 333/78/222/108/70/6),
  X8 truncation mutants T1/T2 red.  Trees: est/build/build-asan source == SEC, build/ binary fresh; /tmp/gxsec-build cleared 13:04.
* #545 working set (uncommitted, DO NOT LOSE): src/devices/dev_footbridge.c, regress/{diff_footbridge.c, footbridge_sites_probe.py,
  fbpending_drain_probe.py, fbpending_witness.py, gate_arm.sh (footbridge block; #529 orphan section NOT ours), gate_offline.sh},
  regress/artifacts/fbd5/ (all tables, panels, gates).  Generators: _scratchpad/fbd5/impl/.  Records NOT yet written.
* NEXT (owner-approved direction: idle/long jobs, low chatter): hygienecensus prepared in the working tree, not committed.

## 087a90 -- 15:1x: hygienecensus PREPARED in the working tree (NOT committed; pins NOT yet written)
* tools/derive_hygiene_pins.sh installed (evaluates the gate's own enumerators; picks a python by RUNNING it -- git-bash's
  python3 is a Windows Store stub).  luna_absentcpu_probe.py send(): mark -> _mark (the three #392 counts now 24/24/24).
  gate_hygiene.sh: 20 committed promptless probes grandfathered by name + a reason comment after the list.
* REMAINING before Sunday 18:00, by whoever commits LAST: grandfather lca_isaphys (peer's #540) / alpha_vmkill (#541) / maybe
  alpha_ifetch (#542) as they land; decide arm_msrmode_probe.py + crime_width_probe.py (UNTRACKED -- owner's TREE_DIRTY
  question, relayed by the peer); then `bash GXEMUL-SEC/tools/derive_hygiene_pins.sh --write` and re-run the report
  (expect every row got == pinned).  Needs its own panel pass (harness round) and a gate_hygiene run.

## 087a90 -- 2026-09-21 13:0x  OWNER DIRECTIVE: "Make sure to use Grok 4.7 extra high" -- APPLIED AND VERIFIED
* `grok models` now lists FOUR (grok-4.7 DEFAULT, grok-4.7-build-fast, grok-4.6, grok-4.5).  panel.sh GROK_MODEL="grok-4.7"
  (never-committed file); carrier CLAUDE.md seat row + roster line updated and mirrored to tools/CLAUDE.md (section J).
  VERIFIED LIVE: -m grok-4.7 --effort xhigh returned the nonce AND CHECKPOINT.md's first line verbatim, rc 0; the bogus-tier
  discriminator still holds on 4.7 (`--effort ultrahigh` lists xhigh/high/medium/low).  Memory: gxemul-grok47-seat.md.
## SUNDAY BATTERY 2026-09-20 18:00 RAN AND **FAILED**: 14 passed, 2 failed, GATE_COVERAGE 16/16, TREE_DIRTY=YES.
* gate 6 gate_hygiene FAIL (7 of 50): exactly the census drift -- unknown 1/0, pty 73/46, promptless 42/40, whole 3/2,
  #392 counts 24/23 x3.  My prepared fix covers all of it; the pins are still NOT written (blocked: two UNTRACKED probes).
* gate 8 gate_upstream FAIL (1 of 22): `check_delete_calls.sh` -- NEW since the 2026-08-30 battery, and OURS: two COMMENTS
  said "delete the kill" (dev_sgi_re.c:510, from #513) and "delete the paragraph" (dev_sh4.c:266).  The upstream check greps
  `delete ` across src/ and the files are not in test/check_delete_calls.exceptions.  FIXED by rewording both to "remove"
  (never by adding the files to the exceptions list -- that would exempt a REAL delete later).  Check now rc 0.
  Propagated (prop_two.out): est CLEAN; build/ 9fa0c1f9, build-asan/ 0f0b4489, /tmp/gxsec-build d0c5946f -- part 1 CLEAN,
  part 2 FRESH, binaries unchanged (comment-only).  Uncommitted, like everything else.
* nightly_check.sh also FAILS on TREE_DIRTY: the verdict describes no commit.  That is the owner's held #545 + the census
  work + the never-commit tools files.

## 087a90 -- 2026-09-21 13:3x  RECORDS DRAFTED (peer holds the machine 13:30-~15:00 for #542/#541 probe phases)
* CHANGELOG block: _scratchpad/fbd5/records/cl545_draft.md (prepend to CHANGELOG.md at records time).
* OUTSTANDING_BUGS: _scratchpad/fbd5/records/bugs_draft545.md -- #545 closure + upstreamdeleteprose + armdesc3kill,
  armdacr2kill, fbirqsoftunimpl, the fiqenableread dissent, hygienecensus.
* LEDGER: _scratchpad/fbd5/records/ledger_write545.py is now COMPLETE (P2/F2 panel dirs, 8 pass-2 + F2 seat entries,
  OPUS2 both runs, FABLE2 = HELD-by-owner (badge A, not a seat failure), closure note, witness, the three new filings and
  the batch-7 grade attachment).  `python ... records` then `... sha <sha>`; announce TAKING THE LEDGER to the peer first.
* NOTHING is committed.  Machine-side work owed after the commit is approved: none for #545 (both gates green on the
  shipped files); hygienecensus still owes --write + its own panel + a gate_hygiene run.

## 087a90 -- 2026-09-21 14:0x  MEASURED: `untrackeddetectors` (peer row, HIGH, open) HAS REGRESSED, and probably by my hand
* MEASURED, not guessed (the peer refused the unverified self-attribution and was right to): STAGING WRITES A BLOB and a
  reset does not remove it, so the OBJECT DB is the witness.  `git fsck --unreachable` holds THIRTEEN unreachable blobs
  whose first line is `crime_width_probe.py BIN [LABEL] -- #529 crimewidthkill DETECTOR`, loose-object mtimes clustered at
  2026-09-19 03:43:06-09; my `git reset -q` ran ~06:1x, just before 7836071 (06:14); the file is UNTRACKED now.  So it was
  STAGED AND LOST, not merely never committed, and the loss is MINE -- with the one caveat that a later reset by anyone
  would look identical and only mine is on record.  arm_msrmode_probe.py has NO matching blob: never staged by either
  session.  SCOPE (peer, measured): the 147 untracked paths are 145 ARTIFACT dirs of rounds in flight + exactly 2 probes.
  REUSABLE DISCRIMINATOR: `git hash-object` + `git fsck --unreachable` says whether a ghost was ever staged; the loose
  object's mtime says when.
* CONSEQUENCE FOR hygienecensus: gate 6 counts what lies in the tree, so crime_width_probe.py (#529 crimewidthkill, in work)
  and arm_msrmode_probe.py (armmsrmodekill, open HIGH) are counted today.  They belong to THEIR rounds' commits, not to the
  census commit; I am not staging them.  Until they are committed or moved aside, `--write` cannot be run honestly.
* No machine work owed by me.  Peer is running CPU-only work (its #542 pass-3 panel, #544 tally sweep).

## 087a90 -- 2026-09-21 14:2x  THE HELD WORK IS NOW RECOVERABLE WITHOUT BEING COMMITTED (refs/snapshots/*)
* The peer's sharper measurement: `git hash-object regress/crime_width_probe.py` (97ab241) matches NO unreachable blob --
  the staged copies are OLDER revisions, so the file's CURRENT content was in no commit and no dangling object.  The same
  was true of every held #545 / census edit: content on disk only.
* CLOSED WITHOUT COMMITTING OR STAGING (HEAD f685d75, index empty, tree untouched -- all three verified after):
    git hash-object -w regress/crime_width_probe.py regress/arm_msrmode_probe.py   -> blobs 97ab241, daea240
    git stash create "..."                                                          -> commit 4b8fe17 (EVERY tracked
      modification in the tree, mine AND the peer's -- a stash snapshot is tree-wide; it does not stash anything)
    git update-ref refs/snapshots/{crime_width_probe,arm_msrmode_probe,held}_20260921   (a ref may point at a BLOB, which
      is what makes this work for an untracked file; anchoring matters because gc prunes dangling objects)
  Plus a filesystem copy in _scratchpad/backup_20260921/ (insurance against `git clean`, which git objects do not survive).
* IT IS A POINT-IN-TIME SNAPSHOT: anything edited after 14:2x needs the two commands re-run.  Delete the refs when the real
  commits land (`git update-ref -d refs/snapshots/...`).
* REUSABLE, and worth keeping: hash-object = what is on disk now; fsck --unreachable + cat-file = what was ever staged;
  loose-object mtime = when.  Together they separate "never staged" / "staged and lost" / "staged, lost, and since edited",
  which neither `git log` nor `git status` can do.

## 087a90 -- 2026-09-21 14:4x  THE SNAPSHOT NET IS COMPLETE (four refs, two sessions) -- verified, not assumed
* MY `git stash create` COVERS TRACKED FILES ONLY (the peer measured it): every untracked path was absent, including all
  145 artifact dirs -- and MY OWN #545 evidence base was in that gap, not just the peer's PRETABLEs.
* The peer closed it with a TEMPORARY-INDEX snapshot (GIT_INDEX_FILE=... read-tree HEAD; add -A; write-tree; commit-tree),
  refs/snapshots/tree_including_untracked_e8a2bc_20260921 -> ff7ab93.  VERIFIED HERE: 601 paths under
  regress/artifacts/fbd5/ are in it (TABLE4.log, killtable PRETABLE.out, gate_arm_545b.log spot-checked), and the content
  is CURRENT -- `git hash-object` on disk == `git rev-parse ff7ab93:<path>` for dev_footbridge.c (e9869dc5) and
  diff_footbridge.c (53f89f22).
* The net now: ff7ab93 (tree-wide, incl. untracked) + my 4b8fe17 (tracked modifications) + two blob refs for the probes +
  _scratchpad/backup_20260921/.  All point-in-time; the cheapest re-take is the peer's temp-index form, which subsumes mine.
  Remove with `git update-ref -d refs/snapshots/...` once the real commits land.  A SNAPSHOT IS NOT A COMMIT: both rows stay
  open, and the owner's three decisions (the #545 commit, the Fable hold, the two untracked probes) are still unanswered.

## 087a90 -- 2026-09-21 15:0x  peer results taken into my records, and my own panels RE-SCORED against them
* PEER (measured today): a REFUSED seat is recoverable by REWORDING -- codex and the Opus agent both answered neutrally
  worded packets (ordinary defect-and-test-coverage language, kill/mutant vocabulary dropped); a WALL NOTICE CAN SPAN
  LINES (grok's 402 wall is pretty-printed JSON whose marker line carries no quota phrase -- the committed tally's
  position test returns FALSE on it); a sweep over LIVE panel dirs is not reproducible.
* I RE-SCANNED my three #545 panels by TAIL rather than by marker line: 24 seat files, the only genuine wall is the kimi
  CLI on the adjudication pass (already recorded, body read).  NOTHING scored "answered" is walled.
* AND THE RE-SCAN FOUND THE INVERSE DEFECT, reported to the peer for its v12: matching BARE NUMBERS (402/429) flags a
  healthy answer that merely CITES a line number ("line 402" = footbridge_sites_probe.py:402 in pass-1 minimax, which ends
  with a full seat record).  A false wall DISCARDS a real answer -- the more dangerous direction.  Require HTTP context.
* If the owner lifts the Fable hold: fire the packet in ordinary defect-and-test-coverage language (peer's measurement).

## GXEMUL (2) [e8a2bc] -- 2026-09-21 15:0x (REPLACED, never appended, by e8a2bc; only up to the next ## header)
* MACHINE: FREE -- I sent PROBE PHASE DONE at ~14:5x and the peer needs nothing.  Nothing of mine touches a tree or
  a rig now; only CPU work (panels) is in flight.  BOTH TABLES LANDED AND BOTH CLONES ARE CLEAN.
* #542 KILL TABLE 2 = regress/artifacts/alphaifetchkill/killtable2_20260921/ -- **24 of 24 AS PREDICTED**, zero
  retries (TABLE2_vs_PRETABLE2.out).  7 new builds in /tmp/gx542 under a sentinel; clone RESTORED cmp-clean,
  binary-nt-source, binary == base, sentinel removed.  The 15 table-1 binaries were REUSED on a checked warrant
  (fix_aifk.py and the baseline file byte-identical to table 1's; every md5 matched).  M6 31/43 with stop msg2 and
  miss count2 RED = the pre-table CHANNEL repair MEASURED.  PASS 3 PANEL RUNNING (brief_542p3_20260921.md) plus an
  Opus seat; Fable HELD.
* #541 KILL TABLE 5 = regress/artifacts/alphavmkill/killtable5_20260921/ -- 34 legs, 30 as predicted, and the THREE
  direction-keyed escapes are CLOSED (M_loadannounce 28/30, M_storedecl 29/30, M_storeredirect8 29/30).  No
  rebuilds; all four binary sets md5-checked.  FOUR legs differed, all toward MORE kills: three share one cause (an
  unlatched announce fires 3x inside a fetch's step -- the fetch translates the same VA three times), and the fourth
  was cmp542 unable to read a red set off the control-red line -- score541.py now prints it, FORWARD-ONLY.
  PASS 5 PANEL RUNNING (brief_541p5_20260921.md).
* #544 v11 = w544/seat_verdicts.FIX.py (v10 kept beside it).  Closes the wall-position class; selftest 62 rows /
  47 mutants all red; sweep over 398 dirs changes ZERO reports vs v10; launcher table unchanged (45 cases, none
  escaped).  brief_544p5_20260921.md is WRITTEN and NOT yet fired -- held only so three panels do not hit the one
  Ollama daemon at once.
* RECORDS: changelog drafts for all three rounds carry their table blocks; rows_542_DRAFT.md has SIX filings;
  ledger state_notes refreshed for alphaifetchkill / alphavmkill / cxseatcheck / lcaisaphys, and
  `untrackeddetectors' CORRECTED (its "resolved in substance" headline was false -- staging did not survive; scope
  is TWO probes, not 147 paths, the rest being round artifacts).  matrix.html regenerated LOCALLY ONLY.
* SNAPSHOT REFS EXIST AND THEY ARE BACKUPS, NOT HISTORY -- a fresh session will find four and should not
  mistake them for branches.  `git for-each-ref refs/snapshots`: two BLOB refs holding each untracked probe's
  current content, a `stash create` commit for TRACKED modifications (peer), and MINE,
  `tree_including_untracked_e8a2bc_20260921` -> ff7ab93, a temp-index snapshot of the whole tree INCLUDING
  untracked paths -- the only one covering the 145 artifact dirs (both PRETABLEs, every kill-table log) and
  the peer's 601 #545 artifact paths.  Taken with HEAD, the index and the working tree untouched (controls
  printed either side: 0 staged, `git status --porcelain` 184 both times).  Each is one `git update-ref -d`
  to remove once the real commits land; each is POINT-IN-TIME, so re-take after further edits -- the cheapest
  re-take is the temp-index one, which subsumes the other three.  The do-not-commit list still governs REAL
  commits; a backup object is not a commit.
* OWNER QUESTIONS OPEN: (1) the two untracked probes (crime_width_probe.py = #529, arm_msrmode_probe.py =
  armmsrmodekill) -- commit, exclude from the hygiene census, or leave counted; NEITHER is mine to stage.  (2) does
  the peer's Fable HOLD apply here?  #540, #541, #542 and #544 are all queued on a Fable adjudication I have not
  fired.  (3) my /loop cron 0f03f0ef still fires every 10 min while the peer's was stopped -- stop mine too?
* NEXT ROUND SCOPED (read-only, no claim): `fbctrlportkill' -- _scratchpad/fbctrl_scoping.md.  FOUR guest-drivable
  exits in one 174-line file, and machine_test.c installs the device, so a rung-3 witness needs no new machine.
