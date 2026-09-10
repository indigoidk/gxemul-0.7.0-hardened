**PASS 2 ON THE REAL DIFF** (`regress/artifacts/lcabadval/pass2_20260910/`, brief 32.8 KB with the diff,
the detector block and the pre-table check inlined; codex and kimi pointer-fed above the argv cap). SIX of
SEVEN scriptable transports answered -- the kimi CLI on its weekly 403 wall and COVERED by `kimi-k3:cloud`;
agy DELIBERATELY NOT FIRED (measurement reserve); the Opus seat holding the tables; the main loop as Fable
adjudicating. In the seats' own words: codex **NO-GO**; grok **NOT RATIFY the detector as floor-complete**;
deepseek **NOT RATIFY**; glm "the fix itself verifies from the packet ... but the mutant floor is NOT
complete"; minimax "PASS WITH ONE UNCAUGHT CELL"; the kimi substitute "the detector has one LIVE defect".
**Every finding was pre-ship (L1) or a wrong record (L4), and all were repaired in round, in four rounds:**

* **A live detector defect** (kimi substitute, from the packet alone): `def read0` scored the STALE `t3`
  printed after a store-only phase -- index 0 where the load was in phase 1. Index 1 now. Its `M20_def_echo`
  sweep could not have measured this (that edit returns zero either way and is equivalent to the fixed
  code); the repaired row's discriminator is measured by `M29_def_allones`, 57/58.
* **The enumeration was wrong, not merely incomplete.** My DEPENDS-ON grid had {kept, narrowed, dropped}
  per mask; four packet-fed seats named the missing **widened** cell (minimax: `& 0x3` -> `& 0x7` stores
  reserved bit 2; W_MASK `& 0xfff00000` -> `& 0xfffff000`; glm: `f = idata >> 20` declines a legal value
  carrying bit 32) and the missing **latch-removed** cells at MASK1 (one unsupported write) and at the
  default read (one read). Codex added the **assignment-vs-accumulation** latch cell, a field-rule
  weakening that admits encoding 2 (`== 0` -> `<= 2`; rejecting 5 and 9 does not exclude it), and that my
  full-width diagnostic check used `0x5a5a5a5a`, which fits in 32 bits. Grok added the **per-label WEN
  announce** (the shared latch bit is the 7g-1 join reached by another door: `wen once` pinned only "at
  least one of two in a BASE0-first session") and the CONF announce operand. Round one scored 52/53 because
  **my own test constant** `0x100f0000` was bit 28 (declined) rather than `0x100000` plus low bits; the row
  refused the wrong constant, and it is recorded rather than silently fixed.
* **Two corrections of the loop by codex, both accepted:** the SG-drop cell three packet-fed seats named
  was never a hole at BASE0 (`wbase0 live`'s accepted `0x300800000` carries SG) -- it was one at BASE1,
  rowed in round four; and my accept-row growth candidate (the old whitelist re-added) was inconsistent --
  that whitelist accepts `0x300800000` and zero, so it reddens neither `wbase0 live` nor `wbase0 zero`.
  `conf live` and `tbena live` get real growth mutants (`& 0x2`, `& 0`) instead.
* **L4s in the diff:** grok, from `lca_pci_conf`: my CONF comment and announce called bit 1 the type-1
  select; `type1 = d->ioc_conf & 1` (`#515`) says bit 0. Reworded in the arm; the audit then found the
  `LCA_W_IOC_CONF_CFG1` define comment still said it, reworded in round four. The default-arm comment called
  every non-switch offset "unlisted" -- four are documented registers (see the fix paragraph).
* **Round three came from the tables themselves.** Both Opus seats were walled mid-table by the Agent
  tool's session limit (HTTP 429, "resets 3am America/Chicago"; the two task notifications are quoted in
  the ledger's seat entries -- no artifact on disk records them), and what they had measured stood: every
  log of the completed runs carries its sentinel, EXCLUDING the first table-1 attempt, quarantined under
  `pre_repair_aborted/` because the fix changed under it (README). Table 1's own additions -- SIX
  non-equivalent 58/58 sweepers, M26/M27/M32/M33/M35/M37 -- exposed two VACUOUS rows (`wmask0 hif`'s prior
  value equalled its wanted value, so a decline read like a store; the TB_ENA rows drove only reserved bit 0)
  and two ABSENT ones (no session wrote W_BASE without WEN, or CONF without bit 1, and asserted silence).
  Round three: `tbena b1`, a distinct prior at `wmask0 hif`, one silence session and one announcing session
  (the first draft put the announcing value in the silence session; `conf silent` read 1 on the correct
  build, 63/64, re-measured with its own log). The main loop ran TABLE 3 itself in the seats' clones against
  their frozen baselines (both `cmp`-identical to SEC at start). Because the 64-row instrument CHANGED a
  session (D6's last phase, `wmask0 hif`), "added rows only add reds" is not the argument for the earlier
  kills; the argument is per row -- every 58-row kill was carried by a row whose session is byte-identical
  between the two frozen instruments, and `wmask0 hif` never reddened on any 58-row mutant.
* **Round four came from a records audit of THIS BLOCK's draft** (codex, `codex_audit_20260910.err`, NO-GO,
  27 items, every one disposed in PRETABLE §9): the 63/64 score had no preserved log; `def width` matched
  the wide value in the debugger's own echoed `put d` command -- a check that cannot fail, inside the
  repair for one -- re-keyed on the announce's form; two rows codex's saved answer had named were still
  absent (legal ZERO at W_MASK, SG at BASE1) and a third was owed by the "no state change" sentence
  (`def state`: a named register survives a default-arm write); and a dozen sentences of the draft were
  wrong in the ways the block above now avoids -- the roster, the seats' verdicts, the scope, the citation
  lines, the mtime claim, "untestable" for "untested", the `-q` claim's ownership, the two witness logs.
* **Recorded, not rowed** (clause (e), in the probe's contract): the registers are WO on hardware with
  UNPREDICTABLE readback (HRM `:980-988`), so every read-back row tests the model's echo POLICY (grok);
  once-per-instance latching is untested (one LCA exists); the W_T_BASE arms store raw; the reserved bits
  above 33 of W_BASE are one row per mask, not per bit; the `-q` clause is source-supported only.

**THE TABLES** (`regress/artifacts/lcabadval/killtable_20260910/`; scratch clones, frozen baselines and
instruments, every score read from a log ending `LCABADVAL_DONE`):
* Table 1 (Opus, 58-row instrument, `SCORES.txt` / `SCORES_B.txt`, 36 distinct mutants): every planned
  mutant killed except the equivalent `M20_def_echo` and the six sweepers that became round three; null
  medium (the pre-fix file) 16/58.
* Table 2 (Opus, 58-row instrument, `t2/`, M1..M24): BASE 58/58; all killed except the equivalent M20;
  `M24_base_nosg` 56/58. Its `PREDICTIONS.txt` predates every log and two predictions missed (M7 47 vs 48,
  M22 15 vs 16) -- predictions, never scores.
* Table 3 (main loop, 64-row instrument, `t3/SCORES3.txt`): *** OWED: the scores, every clean sweep
  disposed. ***
* Table 4 (67-row instrument): *** OWED: BASE, M43..M47, M48_wen_perreg (PRETABLE §4's own prescribed
  two-bit mutant, which neither seat's mutator had implemented), M49_def_narrow. ***

**The repair chain:** four repairs, each owing its pass; *** OWED: the closing pass on the final diff and
instrument with its denominator. ***

Propagated to `est/` and all three build trees twice with the two-part clearance RUN each time
(`propagate518.out` at 00:24 after round two; `propagate518b.out` at 04:11 after round four's comment-only
edits: `build/`, `build-asan/` and `/tmp/gxsec-build` rebuilt, CLEAN/FRESH; `est/` CLEAN, part 2 N/A). Witness:
`probe:regress/lca_badval_probe.py` (rung 3, 14/20 -> 20/20 -> 67/67 with the detector).
