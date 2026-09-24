# GXEMUL state verification, 2026-09-23 -- what the tree holds, what the records say, and where they disagree

> **READ `FINAL.md` FIRST.**  This inventory is the state AS FIRST WRITTEN; two review rounds and the Fable 5.1
> adjudication corrected it (see `DISPOSITIONS_grok.md`, `DISPOSITIONS_codex.md`, `DISPOSITIONS_r2.md`,
> `seats/fable_adjudication.md`).  Known wrong here, kept as written: A4's "every measurement since 09-17 is of the
> working tree" (struck, E2); A5's "recorded ONLY in the transcript" (the evidence exists on disk -- only the synthesis
> is missing, E3); U2's blockers (G5/E8); U7 as a pure-#529 manifest (G4/E7); the 35-37 unmapped artifact roots (G3/E5).


Written by the main loop of session GXEMUL [087a90] on 2026-09-23 ~09:3x-10:3x, after the owner asked whether
progress had been lost.  EVERY LINE BELOW WAS MEASURED TODAY by a command; the command or the artifact is named
beside it.  Items marked OPEN are questions for the review, not conclusions.

The tree under review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (the git repo; `HEAD f685d75`, branch main, 419
commits ahead of origin, LOCAL ONLY by owner directive -- nothing is pushed).  Ignore every other `src/` under the
project root: `./src/` and `_archive/**/builds/*` are pristine 2021 upstream and will mislead you.

## A. WAS ANYTHING LOST?  -- measured answer: NO FILE WAS LOST; ONE SESSION'S NARRATIVE WAS NEVER CHECKPOINTED

A1. **The stop was a planned Windows Update reboot**, not a crash: System log event 1074 at 2026-09-22 21:30:13
    (MoUsoCoreWorker, "Service pack (Planned)") and 21:32:16 (TrustedInstaller, "Upgrade (Planned)"); boot
    21:32:30.  Both working sessions were already idle: the peer session `568ddca5` [e8a2bc] last wrote at
    2026-09-21 19:35:34 (a completed turn, `turn_duration` record, no error); this session last acted ~15:0x on
    09-21.  The two sessions opened 2026-09-23 09:28/09:30 ran only `/model`, `/effort` and `/login` commands.
    No seat or emulator process is alive now (Get-Process: only `ollama`, started 09:21 today).
A2. **Working tree vs the 2026-09-21 15:36 full-tree snapshot** (`refs/snapshots/tree_including_untracked_e8a2bc_20260921`
    -> ff7ab93, which includes untracked files): **0 deleted, 3 modified, 389 added.**  (`vs_ff7ab93.txt` here.)
    The 3 modified are the peer's `tools/pipeline/ledger.json` + `matrix.html` (19:09) and an appended
    `regress/artifacts/alphaifetchkill/killtable2_20260921/TABLE2_instrument_postfreeze.diff`; the 389 added are
    the peer's `alphaifetchkill/killtable3_20260921` (197), `alphavmkill/killtable6_20260921` (96) and
    `killtable7_20260921` (96).  HEAD, the index (0 staged) and `git status` (187 entries) were unchanged by the
    comparison, which used a temporary GIT_INDEX_FILE.
A3. **A fresh snapshot was taken**: `refs/snapshots/tree_including_untracked_087a90_20260923` -> 60b28f6 (tree 216881b,
    identical to the comparison tree).  It is the only snapshot holding the peer's post-15:36 artifacts.  Verified:
    `dev_footbridge.c` hash on disk == in the snapshot (e9869dc5); `killtable7_20260921/logs/TABLE7c.out` present.
A4. **Build trees -- the two-part clearance, RUN today, all shared files (470 `src/*.c|*.h` minus the six
    `tools/est_divergence.txt` paths):**
        build/            part 1 470/470 CLEAN   part 2 FRESH (0 sources newer)   binary md5 9fa0c1f9  09-21 13:06
        build-asan/       part 1 470/470 CLEAN   part 2 FRESH                     binary md5 0f0b4489  09-21 13:06
        /tmp/gxsec-build  part 1 470/470 CLEAN   part 2 FRESH, no sentinel        binary md5 d0c5946f  09-21 13:06
        est/              part 1 470/470 CLEAN   part 2 N/A (source tree, no binary)
    The md5s equal the ones this session's checkpoint recorded on 09-21 13:04.  WSL `/tmp` survived the reboot
    (disk-backed).  Eleven leftover sentinel files (`.MUTANT`, the project's name for a modified-tree marker) sit in OLD scratch clones (`/tmp/gxpcc2b`, `gx514m`, `gxpcc2b5`,
    `gxo496p2_m1/_m2`, `gxcensusB`, `gxfix`, `gxpio_fix`, `gxopus540p3i`, `gxasan_m0`, `gx514pre`) -- none is a project
    tree.  NOTE: the build trees carry the WORKING TREE's uncommitted product edits (they match SEC's working tree,
    not HEAD) -- consistent, and it means every measurement since 09-17 is of the working tree.
A5. **The peer's 09-21 15:0x -> 19:35 work was never checkpointed.**  Reconstructed from its transcript's last turns
    and its files: #541 (alphavmkill) -- grok's fresh-latch fetch variant measured 34/34 (instrument v7 did not
    detect it), instrument v8 (36 rows) detects it at 34/36 on exactly the two rows added for it (`fe exec4`, `fetch pc4`;
    PRETABLE7c.out predicted before the run); the peer's stated next step was "a full table 8 on v8, then pass 7".
    #542 (alphaifetchkill) -- pass 4 (panel_20260921_191038) found ZERO floor breaches, 5 CLOSES / 2 DOES-NOT-CLOSE,
    both dissents records-only; codex's narrowing of the record adopted verbatim into
    `_scratchpad/waifk/changelog_542_DRAFT.md`.  #544 (cxseatcheck) -- "owes its pass 6".  #541 PASS 6
    (panel_20260921_191126) WAS read by the peer at 2026-09-22T00:25Z: "6 answered, 1 genuine wall, and **codex
    refused again** [a content-filter refusal on the brief's wording] ... Verdicts 4 DOES-NOT-CLOSE
    / 2 CLOSES"; grok's named cell became the v8 repair.  **That reading, the codex content-filter refusal (a seat
    failure) and the v8 measurement are recorded ONLY in the transcript** -- the ledger row `alphavmkill` has 13
    entries ending 2026-09-19 and `_scratchpad/w541/changelog_541_DRAFT.md` carries no pass 6 (grep: 0 hits for
    `191126` / `PASS 6`).  A NARRATIVE LOSS, recoverable from `568ddca5-...jsonl` while that file exists.

## B. THE COMMITTED TREE LAGS THE RECORDS -- verified work that is NOT in HEAD

Unit table.  Every one of the 32 modified tracked files and the 10 untracked files outside `regress/artifacts/` is
mapped below.  (`diffs/` here holds `git diff HEAD -- <file>` for each of the 32; `diffs/_STAT.txt` the stat.)

| unit | round / ledger row (state) | files | age | what the records say |
|---|---|---|---|---|
| U1 | #545 `fbdeclinefive` (open) -- this session | src/devices/dev_footbridge.c; regress/{diff_footbridge.c, footbridge_sites_probe.py, fbpending_drain_probe.py, fbpending_witness.py, gate_offline.sh}; regress/gate_arm.sh (footbridge block + #539's E0-E6 hunk); artifacts `regress/artifacts/fbd5/` (untracked) | 09-19 | complete, gate_arm PASS 1061 + gate_offline PASS 351 on these files; **commit HELD by owner**; records only as drafts `_scratchpad/fbd5/records/{cl545_draft.md,bugs_draft545.md,ledger_write545.py}` |
| U2 | `hygienecensus` (NO ledger row) -- this session | regress/gate_hygiene.sh, regress/luna_absentcpu_probe.py, tools/derive_hygiene_pins.sh (untracked) | 09-19 | prepared, pins NOT written; blocked on U7/U11's untracked probes |
| U3 | `upstreamdeleteprose` (NO ledger row) -- this session | src/devices/dev_sgi_re.c (1 line) | 09-21 | fixes gate 8 (`test/check_delete_calls.sh`): **HEAD still FAILS it** -- `HEAD:src/devices/dev_sgi_re.c:510` (a comment containing the word `delete` followed by a space), file not in the exceptions list; the dev_sh4.c instance lived inside U4's uncommitted text |
| U4 | `sh4dmacie` (closed; commits f532bb6 2b40eb7) -- 09-17 seat audit | regress/sh4_chcr_probe.py (X4c/X4d, EXPECT_ROWS 27->29); regress/gate_sh_rounding.sh (sh4_chcr pin 27->29); src/devices/dev_sh4.c (3 comment hunks, +126/-0, NO code); artifacts `regress/artifacts/sh4dmacie/repairA_20260917/` (untracked) | 09-17 | ledger entry [28] (fable5, 09-18): "L2 done in a follow-up ... correctly not amended under #453's number, and **still uncommitted**" -- HEAD's shipped detector is the one the M1 variant passes 27/27 |
| U5 | `gdromdmadefault` (closed; 7c9dd9e) + `gdromacceptdmanum` (in work) -- 09-17 | regress/gdrom_default_probe.py (coverage matrix, rows `nodata byte` / `accept byte`, accept oracle "Transfering 408 bytes"); regress/gate_sh_rounding.sh (gdrom pin 60->62 + two row names); artifacts `regress/artifacts/gdromdmadefault/repairB_20260917/` (untracked) | 09-17 | ledger: repair chain CLOSES (grok pass 3); codex 09-17 batch "row 9's repair is applied and proven in the working tree, but has not shipped in committed HEAD" |
| U6 | L4 comment corrections -- 09-17 | src/devices/dev_pcc2.c (the shipped "return variant passes every row" sentence is false: 14/16); src/include/thirdparty/mvme_pcctworeg.h (MIEN is the vendor name); src/cpus/cpu_alpha_palcode.c (FIVE instances, not four; artifact `regress/artifacts/cpusexitsweep/TRIAGE_palcode_20260917.md`) | 09-17 | rows `pcc2c040returnmutant` (dropped, "the L4 comment correction is what survives"), `pcc2genctlc040alias` (in work), `cpusexitsweep` (open) |
| U7 | #529 `crimewidthkill` (in work) -- owner not named in any checkpoint ("orphan") | src/devices/dev_sgi_ip32.c; regress/crime_width_probe.py (UNTRACKED; staged once and lost 09-19, recoverable via refs/snapshots/crime_width_probe_20260921); regress/gate_arm.sh (:1772+ section, pins 204); tools/pipeline/check_probe_wiring.py (manifest, 73 #529 tags); tools/precommit_check.sh (SCORE_CLAIMS_MANIFEST 31); artifacts `regress/artifacts/crimewidthkill/` (untracked) | 09-13..18 | fable5 09-18: pin 188 vs 204 "would red the gate today" -- SUPERSEDED: the pin now reads 204 and gate_arm 09-19 ran the section green (gate_arm_545b.log:1625-1631) |
| U8 | #540 `lcaisaphys` (in work) -- peer | src/devices/dev_lca.c; regress/lca_isaphys_probe.py (untracked) | 09-21 | in work |
| U9 | #541 `alphavmkill`, #542 `alphaifetchkill`, #544 `cxseatcheck` (in work) -- peer | NO product hunk in SEC: the fixes live in clones /tmp/gx541, /tmp/gx542 and `_scratchpad/{w541,waifk,w544}`; artifacts untracked | 09-21 | see A5 |
| U10 | `ppcwitnessmaskoracle` (in work) | regress/ppc_rldicl_probe.py (+95/-12) | ? | on the owner's DO-NOT-COMMIT list; fable5 09-18 dissents from treating the uncommitted repair as the row's discharge |
| U11 | `armmsrmodekill` (open) | regress/arm_msrmode_probe.py (UNTRACKED, never staged) | 09-17 | open |
| U12 | harness fixes -- 09-17 | tools/pipeline/check_boilerplate.py (row `boilerplateprefix`), tools/pipeline/check_score_claims.py (`scorehyphenfp`), tools/adjudicate.sh (`adjudglmtag`) | 09-17 | uncommitted |
| U13 | never-commit tool files (owner list) | tools/{BRIEF_TEMPLATE.md, CLAUDE.md, PIPELINE.md, panel.sh}, tools/pipeline/fable_queue.md, tools/pipeline/check_fix_seats.py (untracked) | -- | root CLAUDE.md == working-tree tools/CLAUDE.md BYTE-EQUAL (section J passes on the tree); HEAD's copy lags the live carrier by +133/-12 |
| U14 | records | tools/pipeline/ledger.json, tools/pipeline/matrix.html | -- | both sessions write them; last write peer 09-21 19:09 |
| U15 | stray, in no record | tools/pipeline/check_probe_wiring.py.orig, tools/precommit_check.sh.orig (09-18 19:46; equal to neither HEAD nor the tree nor any of the last 12 commits; the lines they hold that the tree lacks are superseded #530/#536 wiring text); regress/{alpha_dummy,arm_bfx_stub,sgi_mte_dummy}.bin (never-commit); 224 git-ignored `*.o` + a `gxemul` binary of 2026-08-13 INSIDE GXEMUL-SEC | -- | a stale 08-13 binary inside the repo is a stale-binary trap for anything that runs `./gxemul` there |

B-extra. **Findings that have NO durable carrier yet** (only uncommitted drafts in `_scratchpad`): `armdesc3kill` and
`armdacr2kill` (two guest-writable values that end the emulator process in `src/cpus/memory_arm.c` -- `:254` an
unimplemented descriptor type 3, `:79` a reserved domain-access value 2), `fbirqsoftunimpl`, `hygienecensus`,
`upstreamdeleteprose` (all in `_scratchpad/fbd5/records/bugs_draft545.md`), and the peer's six #542 filings
(`_scratchpad/waifk/rows_542_DRAFT.md`, per its checkpoint).
B-extra2. **A wrong record that nothing corrects, not even the working tree**: `CHANGELOG.md:4285` (the `#517` heading)
says the second C040 definition "was a different register's bits"; fable5 on 09-18 verified it false (FAST and MIEN
are bits of the SAME General Control Register).  CHANGELOG.md is unmodified in the working tree.
B-extra3. **#539's CHANGELOG block claims the "E0-E6 distinct GREEN row ids" gate fix shipped; HEAD's gate_arm.sh does
not have it** (the hunk is in the working tree; U1's draft carries the L4 correction).

## C. SCHEDULED FAILURES

C1. **2026-09-27 is the last valid day of THIRTEEN dated exemptions** -- two in `SC_EXEMPT="ieee_store:2026-09-27
    wdc_identify:2026-09-27"` (`regress/gate_offline.sh`, strict `<`: "valid ON 2026-09-27 and RED from 2026-09-28",
    owner row `scexempt`) and ELEVEN in `tools/pipeline/check_probe_wiring.py`'s EXEMPT table (count measured: 11
    entries stamped "2026-09-27"; its own comment at :3009 says "comparison is `d < today`, so an exemption is valid
    ON its stamped date") -- fbpending_drain_probe.py (U1's probe), wdc_altoffset_probe.py, wdc_altoffset_sig_probe.py,
    wdc_altoffset_4bit_probe.py, wdc_addtoinbuf_probe.py, ppc_rldicl_probe.py, alpha_tbi_probe.py, lca_badval_probe.py,
    lca_widewrite_probe.py, lca_isalane_probe.py, and the entry at :2423.  From 2026-09-28 every commit's precommit
    section R and gate_offline red unless each is discharged, re-decided or deleted (owner's call -- #537 says "fix it,
    do not re-date").
C2. **Weekly battery: Sunday 2026-09-27 18:00.**  The last one (09-20) FAILED: gate 6 `gate_hygiene` 7 of 50 (census
    drift -- U2), gate 8 `gate_upstream` 1 of 22 (U3); plus `nightly_check.sh` TREE_DIRTY.  Both fixes are
    uncommitted.

## D. THE PROJECT'S OWN RECORD CHECKERS, run today against the working tree (outputs in `checkers/`)

12 of 14 PASS (optpin, boilerplate, bugfile_sync, score_claims, row_states, cited_artifacts, witness,
commit_attribution, fable_queue, stage_panels, seats_read, wsl_dollar).  Two FAIL:
D1. `check_probe_wiring.py` -- 78 problems, ALL of kind GHOST, and ALL from names that exist ONLY in the working
    tree's uncommitted manifest (HEAD's copy names none of them): #529's untracked probe and its measurement-table scripts,
    plus four untracked 2026-09-13 rung-3 attempt probes (`artifacts/{b115,fbclearread,wdcnullxfer,wdcrearmzero}/rung3_20260913/`).
    So the manifest hunk cannot be committed without the files it names.
D2. `check_checkpoint.py` -- CHECKPOINT_NO_HEAD: its regex is `^HEAD:\s*...` (a line that STARTS with `HEAD:`), and
    the shared checkpoint's header carries `HEAD: f685d75` mid-line.  A format defect in the checkpoint, not a
    stale one.
