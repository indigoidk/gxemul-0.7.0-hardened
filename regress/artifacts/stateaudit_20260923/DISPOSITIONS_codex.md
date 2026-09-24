# Main-loop dispositions of the Codex GPT-6 Astra review (seats/codex_verify.txt, 18,544 b, rc 0, 0 refusal / 0 wall lines)

Codex (gpt-6-astra, max, read-only sandbox; it ran read-only git and in-memory Python) returned
`VERDICT: INVENTORY HAS 8 ERRORS`.  It agrees with Grok on every point both raised; its additions are marked NEW.
Each was CHECKED here before disposition.

| # | Codex finding | check run here | disposition |
|---|---|---|---|
| E1 | "NO FILE WAS LOST" is scoped to the snapshot's population. | = Grok G1; `cited_paths.py` run (DISPOSITIONS_grok.md G1). | ACCEPTED (re-worded to its measured scope). |
| E2 NEW | A4's "every measurement since 09-17 is of the working tree" is not proven by present equality; `fbd5/killtable_20260919/TABLE2.log:2` names a SEC-HEAD baseline. | The sentence infers history from today's equality. | ACCEPTED -- sentence struck. |
| E3 NEW | A5's "recorded ONLY in the transcript" is false: the v8 result is `alphavmkill/killtable7_20260921/logs/TABLE7c.out:1` and the codex refusal is `_scratchpad/panel_20260921_191126/codex.txt:132`. | Both lines read: `M_freshfetchcode_v8 rc=1 KILLED 34/36 red=[fe exec4, fetch pc4]`; `ERROR: This content was flagged for possible cybersecurity risk ...` | ACCEPTED.  What is missing is the SYNTHESIS (ledger entry, changelog pass, checkpoint), not the evidence. |
| E4 NEW | The "10 untracked outside artifacts" silently excludes 267 files under the shadow `GXEMUL-SEC/_scratchpad/`. | My list was scoped to `regress src tools`. | ACCEPTED -- the exclusion is now stated. |
| E5 | 37 artifact roots lack a unit (Codex maps three more: lcaisaphys->U8, ppcwitnessmaskoracle->U10, armmsrmodekill->U11). | = Grok G3 (Grok counted 35; the difference is those three inferred mappings). | ACCEPTED -> U16 (18 zero-tracked dirs cited by committed records; list in `untracked_cited_dirs.txt`). |
| E6 NEW | U5 omits `gdromcontractresidual` (the M3a/M3b split at `gdrom_default_probe.py:59`, the qualified escape claim at `:255`) and the evidence dir `gdromdmadefault/acceptdma_20260917/`. | Dir exists; the M3a/M3b block is in the U5 hunk. | ACCEPTED. |
| E7 | Five manifest additions belong to four other rounds (b115, fbclearread, wdcnullxfer x2 incl. `mkvariants_wdc.py`, wdcrearmzero). | = Grok G4. | ACCEPTED. |
| E8 | U2's blockers: the two ungrandfathered promptless probes are ARM MSR and LCA ISA; tracking a file does not remove it from filesystem-based counts. | = Grok G5; deriver report confirms. | ACCEPTED. |
| U5 NEW | **A recorded correction that is NOT in the file**: `gdromdmadefault` entry [11] (09-17) says "FOUR APPLIED", one of them the comment listing `dma alias` as an ARMING-arm byte store (it is a `default:`-arm store at +0x05); `regress/gdrom_default_probe.py:1187` still reads "`dma alias' (+0x05) and `arm bytetrig' (+0x18), and BOTH are on the ARMING arm". | Read :1180-1192; the same sentence is in ff7ab93 (09-21) and 60b28f6 (today). | **ACCEPTED, and THE WORDING WAS WRONG -- reversed by the Fable 5.1 adjudication (W1), verified here: the correction WAS applied at `gdrom_default_probe.py:160-166` and `:1608-1610` (both working-tree only; HEAD has neither); `:1187` is a MISSED THIRD SIBLING, and `:1186`'s "the sentence was true when written" is false too.  A sibling miss, not a phantom application.  My round-2 brief then stated "never applied" as the calibration answer and BOTH seats ratified it -- the wrong-fact-in-a-brief class, on my own premise.** |
| U7 NEW | Stale prose in #529's uncommitted hunks: `check_probe_wiring.py:553` (141), `precommit_check.sh:340` (188), `gate_arm.sh:1774` ("four kill tables" beside a section discussing table 12). | First two = Grok G7. | ACCEPTED. |
| U4 NEW | `dev_sh4.c:292` says "WHAT SHIPPED INSTEAD" of X4c/X4d, which are uncommitted. | Prose that becomes true only on commit. | ACCEPTED -- becomes true when U4 ships; must not ship without it. |
| U1 NEW | `cl545_draft.md:23` "Nothing a guest can now do to this device ends the process" contradicts the draft's own :19-20: the SDRAM read pair still ends it (`dev_footbridge.c:732-735`, `:757-760`). | Read both. | **ACCEPTED -- a wrong record in MY draft; repair R6.** |
| U1 NEW | "49 detected" combines successive instrument versions; the gate totals describe the combined working tree (incl. U7), not an isolated #545 candidate. | M9 now re-measured on the final probe (R3, below). | ACCEPTED -- the draft names which instrument each survivor-of-offline was measured on. |
| Q4 NEW | Coupling: U7 also needs U12's score-regex fix (`entries-4/8` in the crime probe reads as a stale score otherwise); ledger + matrix must travel together (precommit section Q re-renders); #529's artifact dir holds 111 untracked .py of which the manifest classifies 72 -> committing the dir wholesale adds 39 UNCLASSIFIED files. | 111 / 72 counted here. | ACCEPTED -- recorded as commit-recipe constraints. |
| Q6 | 09-27: gate 6's seven checks fail on the current files; gate 8 is already fixed in the tree the battery runs; `nightly_check.sh:110` separately rejects a dirty tree.  09-28: gate_offline SC_EXEMPT (2) + precommit section R (11, the eleventh being `artifacts/ip30abortkill/ip30_abort_probe.py`).  Deleting an exemption entry does not discharge it.  #537's "do not re-date" concerned the SM obligation; SC's source records a separate owner-authorised re-date. | Consistent with Grok's Q6 and the deriver. | ACCEPTED, including the correction to my attribution of #537. |
| D2 | Historical -- the checkpoint header was fixed after the saved checker output. | -- | noted, not counted. |

## R3 DONE (my #545 draft's M9 claim) -- measured 2026-09-23 10:27, artifacts `_scratchpad/fbd5/impl/r3_m9_20260923/`

Prediction written into `R3.log` above the result (same file, 13 s apart -- the ORDER within the file is the only witness; there is no mtime discriminator): FIX 37/37; M9 33/37 red N1 N2 N0 NO.  Measured on a fresh clone of
`build/` (baseline `dev_footbridge.c` == SEC, md5 783c0c7f; probe md5 9e9961de, frozen copy): **FIX 37/37 (binary
9fa0c1f9); M9 33/37 red N1, N2, N0, NO (binary fb0a051a); restored, cmp == SEC, binary 9fa0c1f9, sentinel cleared.**
The predicted ROWS matched exactly; my parenthetical N0 value (4) was wrong -- the row reports `distinct-once=3`
(texts that occur exactly once), consistent with its definition.  So "all 49 detected by the combined detector" is
now MEASURED for M9 on the FINAL instrument.
