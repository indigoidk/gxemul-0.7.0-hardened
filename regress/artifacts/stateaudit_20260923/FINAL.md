# FINAL -- GXEMUL state audit after the 2026-09-22 reboot (2026-09-23, session GXEMUL [087a90])

Owner's request: *"verify where we are with the progress of GXEMUL, some progress might have been lost; review all
patch previous diff, any discrepancy review with Codex Astra, Fable 5.1, and Grok 4.7"*.

Seats: **Codex GPT-6 Astra** (max, read-only; rounds 1 and 2), **Grok 4.7** (xhigh, plan mode; rounds 1 and 2), **Fable
5.1** (Agent tool, LAST, after both; identity VERIFIED from its subagent transcript -- 107 turns on `claude-fable-5-1`,
final text by `claude-fable-5-1`; ONE turn recorded as a refusal at 16:01Z, recovered on the same model, no fallback).
Every finding a seat made was checked by a command here before it was accepted; the checks are in the three
`DISPOSITIONS_*.md` files.  Fable's answer, verbatim: `seats/fable_adjudication.md`.

## 1. Was progress lost?  The answer the evidence supports (Fable's wording, re-checked)

**No path in GXEMUL-SEC's non-ignored tree (tracked or untracked) was deleted** between the 2026-09-21 15:36 snapshot and
2026-09-23 (name-status: 0 deleted / 3 modified / 389 added -- all additions and modifications are the peer's later
work).  Fable additionally checked that every file either session wrote with Write/Edit since 2026-09-19 still exists
(peer 194 targets, this session 132, **0 missing**, 148 of them outside the repo where no snapshot reaches), and that
the peer's out-of-repo carriers are present (`/tmp/gx541`, `/tmp/gx542`, the `_scratchpad/{w541,waifk}` generators, its
transcript).  **Every records-vs-tree disagreement found pre-dates the reboot** (each is present in the 09-21 snapshot).

**What the reboot cost is SYNTHESIS, not evidence:** the peer session's last four hours (09-21 15:0x-19:35) --
#541's pass 6 (4-2 does not close; a codex seat refused on the brief's wording), its v8 instrument (34/36, predicted),
#542's pass 4 (zero floor breaches) -- exist as files (`TABLE7c.out`, `panel_20260921_191126/`, the changelog drafts)
but in no ledger entry and no checkpoint.  The reconstruction is now in `_scratchpad/CHECKPOINT.md`, attribution-marked.

**Not yet run, and it could still falsify the claim:** the peer made 97 Bash calls after the snapshot and writes files
through python heredocs (`io.open(...,'w')`), which no scan here enumerated; and there is no pre-09-21 baseline of
untracked files at all.  The 81-claim reconciliation is a FLOOR (ledger-only, verb-keyed).

## 2. Where the records and the tree disagree (all pre-reboot)

| # | discrepancy | owner | disposition |
|---|---|---|---|
| D1 | `gdromdmadefault` [11] "FOUR APPLIED": the `dma alias` correction was applied at `gdrom_default_probe.py:160-166` and `:1608-1610` and MISSED at a third sibling, `:1186-1187` | U5's round (uncommitted, 09-17) | R7: fix `:1186-1187` with U5 -- not this session's file |
| D2 | `stagetokens` [18] "ALL REPAIRED" -- the dashboard half of the malformed-hold finding is not repaired (`gen_dashboard.py:143-146`, `:173`, both written by `09ded75`) | #534 (committed, closed) | L4 ledger correction + FILE the dashboard defect (R8) |
| D3 | `HEAD:CHANGELOG.md` #539 block: "the gate's distinct-id check now counts ids over the GREEN lines" -- never shipped | mine (#539) | **CORRECTED IN PLACE today** (uncommitted); the hunk ships with #545 |
| D4 | `CHANGELOG.md` #517 heading "a different register's bits" -- false (same register), flagged 09-18, corrected nowhere | #517's round | **CORRECTED IN PLACE today** (uncommitted), per Fable's Q3(a) |
| D5 | my #545 draft: "nothing a guest can do ... ends the process" (the SDRAM pair still does); M9's guest detection on an older instrument | mine | **CORRECTED** in `cl545_draft.md`; **M9 RE-MEASURED today on the final 37-row probe: 33/37, red N1 N2 N0 NO** (`regress/artifacts/fbd5/r3_m9_20260923/`) |
| D6 | two durable copies cited and never made: `n6/p1_20260919/fable5_p1_20260919.md`, `ip30abortkill/PROBEATTACK_grok_20260917.txt` | mine / #531's | **COPIED today** from their surviving scratch sources (cmp-verified) |
| D7 | 18 artifact directories cited by COMMITTED records hold no tracked file (largest `seataudit_20260917`, 38 files) | each round | protected by the snapshot refs; staging is each round's (owner) |
| D8 | stale numbers in #529's uncommitted comments (`precommit_check.sh:340` 188, `check_probe_wiring.py:553` 141, `gate_arm.sh:1774` "four kill tables") | #529 (orphan since 09-13) | R4 -- #529's owner |
| D9 | older evidence gaps (Fable, 08-01 onward): 21 `ollama_` name mismatches in 08-27 citations; `alphatbinegsel` cites a file that lives under `ppcrldiclzero/`; `armbdt/passD/fable_floor_20260911.md` never made and no source found; `regress/fable5_2026-08-15.md` nowhere; ~8 scratch evidence paths gone | various | FILE; none reboot-timed |
| D10 | **gate 6 is RED AT HEAD**, measured today on a pure HEAD export: pty 70/46, promptless 40/20, anchor 24/23, echo 24/23, whole-buffer 3/2 -- not only a dirty-tree problem | census (owner) | see section 4 |

## 3. Done today (protective, records, measurement)

* Snapshot `refs/snapshots/tree_including_untracked_087a90_20260923` (60b28f6) -- HEAD/index/tree untouched; re-taken
  after today's copies (see the checkpoint for the newest ref).
* **The peer's #540/#541/#542/#544 work that NO snapshot held** -- the `/tmp/gx541`, `/tmp/gx542` clones' differing
  sources and the `_scratchpad/{w541,w540,waifk}` generators (+ `w544` top level) -- COPIED, never edited, to
  `regress/artifacts/stateaudit_20260923/peer_carriers/` with a MANIFEST: **1170 copies, verified by cmp and md5, 0
  mismatches**.  (The first verification pass reported "0 files" -- a parse that selected nothing -- and was redone.)
* Build trees: two-part clearance RUN on all four (build/, build-asan/, /tmp/gxsec-build CLEAN + FRESH; est/ CLEAN).
* Checkpoint consolidated (27.7 KB -> 11.8 KB), peer section untouched, `check_checkpoint` now OK.
* D3, D4 corrected in place in `CHANGELOG.md`; D5, D6 done; this audit's evidence, seat answers and DERIVERS copied to
  `regress/artifacts/stateaudit_20260923/` (Fable: the derivers lived only in a volatile temp dir).

## 4. Decisions that belong to the owner

1. **The weekly battery, Sunday 2026-09-27 18:00** -- gate 6 fails today at HEAD and on the tree.  Fable's minimal set
   (codex's ordering, grok's specifics corrected): (i) are the three untracked probes (`crime_width`, `arm_msrmode`,
   `lca_isaphys`) part of the census; (ii) grandfather or convert the two promptless ones; (iii)
   `arm_bdt_probe.py:76` -- convert, or allowlist BY NAME at pin 3; (iv) the `crime_width_probe.py:956` spelling (#529);
   (v) accept ONE bulk re-derivation of the pins for the 24 committed probes, then `derive_hygiene_pins.sh --write`.
   Writing the pins to whatever the last run printed (grok's step 3) would fit the check to the tree.  And
   `nightly_check.sh` reports FAIL on Sunday regardless, until the tree is clean.
2. **Thirteen dated exemptions lapse on 2026-09-28** (2 `SC_EXEMPT`, 11 probe-wiring incl. my `fbpending_drain_probe.py`):
   each is a wiring decision for its round; deleting an entry does not discharge it.
3. **The #545 commit** (held since 09-19; complete and green, draft records now corrected) and **the Fable hold** for
   its adjudication.
4. **Commits of other sessions' verified work** (U4 sh4dmacie repair, U5 gdrom repairs, U6 comment corrections, U12
   checker fixes -- all since 09-17; #529 needs an owner assigned; the peer's #540-#544).
5. **The never-commit list vs section J**: HEAD's `tools/CLAUDE.md` is +133/-12 behind the live carrier.
6. The dashboard: the session is now signed in to the account that owns the dashboard artifact; it was regenerated
   LOCALLY only, per the standing instruction.
