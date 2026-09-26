OPUS_SEAT_ALIVE_20260925_f2v6

`# CHECKPOINT -- 2026-09-25 ~20:35 (087a90 sections rewritten; the peer's sections below are untouched)` (when I first opened it at the start of the task it read `~20:25`; this is the current first line)

VERDICT: SHIP WITH CHANGES

The fix is right. What is owed is new rows in the probe. D1 is a floor breach, now measured rather than reasoned, so v6 does not close the repair chain. The rows that close D1 also close most of D2 if they use the right anchor.

1. **How I measured.**
   - I worked in the WSL clone `/tmp/opusf2v6`, a `cp -a` of `build/`. Its `dev_fbctrl.c` and the frozen probe both `cmp` clean against GXEMUL-SEC (fix md5 129694b8, probe a9a2be3d).
   - I rebuilt the baseline in the clone after `rm src/cpus/*.o`. It is fresh, and its md5 is b5b99e6d, the same as `build/gxemul` and table 6's base.
   - Five of table 6's own edit texts (MKB_05, MKB_31, MKB_40, MKB_63, DSC_ann_hibits) rebuilt byte-identical to table 6's binaries. MB_pc4 rebuilt identical to the fallback's (8fa9af7e).
   - I wrote 22 edits with their predictions before building them. Every prediction held on v6.
   - The clone carried its own `.MUTANT` sentinel, and the restore was verified twice (cmp, freshness, md5).
   - I wrote nothing under `C:\DocumentNoSnc`. The md5s of `build/` and SEC are unchanged afterwards.

2. **D2 (N21) is real. Measured on the unmodified v6 probe:**
   - The one-liner `if (idata == 32) d->current_port = 5;` at the top of the refusal arm scores **117/117** (CONTROL=OK, rc 0).
   - These also score 117/117: `(uint32_t) idata == 0 → 5`, `== 2^40 → 5`, `== 2^32 → 5`.
   - Two values no seat named also score 117/117: `== 0xffffffff → 5` (P's all-ones by `sw`) and `== 0x100000005 → 3` (X3's value).
   - The same edits writing the other constant go red exactly where predicted:
     - `32 → 7`: 113/117 (B's four width rows read 0x7).
     - `2^40 → 7` and `2^32 → 7`: 116/117 (B's `sd` row).
     - `lo32==0 → 7`: 114/117 (P's 0x200000000, W's 2^63, B's `sd` row).
   - I walked the probe's own programs statically (`SIM_ANCHORS.out`). **60 refused values are observed at only one previous selector:**
     - 58 single bits (bits 5-7 and 9-63), all at selector 5;
     - 0xffffffff at 5;
     - 0x100000005 at 3.
   - Each of the 60 admits a refusal-time write of its one observed selector (its anchor).

3. **D2's one-second-anchor remedy moves the hole instead of closing it.** I scored a probe copy whose B `sd` group selects 7; the fix scores 117/117 on it.
   - The `→ 5` forms (32, 2^32, 2^40, `lo32==0`) all go red, at 116/117.
   - `2^40 → 7` and `2^32 → 7` now score **117/117**.
   - `0xffffffff → 5` and `0x100000005 → 3` are untouched.
   - It loses none of B's existing kills (MKB_05/31/40/63 stay red).
   - This is the `#499` shape: the gap is repaired at the address the mutant used, and the mirror cell opens.

4. **D1 (N1) is real, and nobody had built the form grok named.** The fallback built the value form (`idata == 0x10 && !warned_port`), not the mask.
   - `(d->warned_port ? idata : (idata & ~(1ULL << 4))) >= NPORTS` scores **117/117**. The same at bit 40 scores **117/117**, on both v6 and the `sd`-at-7 copy.
   - Witnesses on fresh devices:
     - **Bit-4 form:** a first `sw 16`, then a DATA read, ends the process in the DATA-arm check.
     - **Bit-40 form:** a first `sd 2^40` is accepted silently as selector 0. PORT reads 0 and there is no announce. The guest's next DATA write of 0x2a (meant for COLOR_R) runs as command 42, and the process ends through `fbctrl_command`'s default ("Unimplemented command 42"), not through the kept tripwire.
   - The static walk agrees: there are 14 latch-clear refusals, and the tested bits held alone at latch-clear are exactly {3, 8, 32}. **58 of 61 are open.**

5. **One repair closes D1 and most of D2, and it is cheap.** I measured a prototype (`u_sessions.py`, not a probe edit): one fresh device per single-bit value. Each does `PORT=7`, stores 2^k (`sw` below bit 32, `sd` above), and reads PORT; the checks are keep, announce once, and name.
   - On the fix: 61/61 green in **9.7 s**. That would take gate 16 from about 17 s to about 27 s.
   - It kills N1_mask4 (U04 reads 0x10), N1_mask40 (U40 reads 0x0) and MKB_40.
   - It kills `32→5`, `2^40→5` and `lo32==0→5` (U32..U63). It kills `2^32→5` only if bit 32 is included; grok's 58 leave it out.
   - The `→7` forms stay green under U, but v6's B at selector 5 already kills them. **So B at 5 plus U at 7 gives every single-bit value two anchors.**
   - Residue, green under v6, the `sd`-at-7 copy and U: `0xffffffff→5` and `0x100000005→3`.
   - **The anchor must be neither 5 (that is D2) nor 0.** For k ≥ 32 a leaked 2^k is stored as int 0, which would read as "kept 0".
   - With announce/name checks, U also turns DSC_ann_hibits red (U09..U63 are silent under it). Adopting those rows means re-predicting that edit and CF2_KM_not16/CF2_DM_ge16 (predicted by reading, not built), and narrowing (3).

6. **Adjudication.**
   - **D1 = N1: UPHOLD FLOOR (L2). A v7 is owed.** Reasons:
     - The refusal body reads `warned_port`, so {clear, set} is a floor axis under the joint-cell rule.
     - The generating-set amendment applies at each floor cell, and v6's own session B defines "set" for this compare as "set alone".
     - The edit is DEPENDS-ON clause (2)'s operand swap, drawn from a field the body reads.
     - It measured 117/117.
     - The repair terminates: the latch has only two reachable states, the product is 58 cells, one width each suffices, and width at latch-clear stays a (0) joint.
     - This is the same class as the verifying pass's breach, found on two consecutive passes, so the class-closure rule applies. Write the floor into the contract as the cross-product {latch} × {each tested bit alone}, not as marginals.
   - **D2 = N21: REFINE.** It is real and outside the literal (0)-(8). It is not a floor breach: it is keyed on `idata == k` or on a value class, which the 2026-09-04 joint-cell ruling puts under clause (e). What is owed is an L4 wording fix:
     - (3)'s "one value no row writes" implies coverage the rows don't have;
     - B's "never 5" covers a store only;
     - refusal-time writes of the selector need their own disclosure.
     Closing it for single bits costs nothing if the D1 rows use anchor 7.
   - **N2 REFINE.** The open low-3 classes are 2, 4 and 6 (agy found this). Measured: `!=2` scores 117/117; the control `!=5` scores 114/117. The consequence is not always the exit: a first `sd 0x100000006` is accepted silently as selector 6.
   - **N3 REFINE.** "Re-arm periods > 108" is off by one. "Every mask red" holds only while the latch is set.
   - **N4: OVERTURN the consequence clause; UPHOLD widening (3) to value classes.** MB_pc4 accepts a first `sd 0x700000001` silently as selector 1, with no announce and no exit.
   - **N5 OVERTURN** (see D1).
   - **N6 UPHOLD.**
   - **N7 UPHOLD** (verified in `table6/TABLE.out`).
   - **N8 UPHOLD.**
   - **N9 UPHOLD, measured:** period 107 scores 116/117 (count 2); period 108 scores 117/117.
   - **N10 UPHOLD, with an option.** Printing t1..t4 after session B costs no extra steps. Measured on the fix: 0x100, 0x10000, 0x100000000, 0 (`B_REGS.out`). That pins every doubling, and t3 = 2^32 pins a 64-bit `dsll`.
   - **N11 UPHOLD.**
   - **N12 UPHOLD.**
   - **N13 UPHOLD.** Minimax's (5) premise ("fatal() exits") is false here; record it as refuted rather than dropping it.
   - **N14 OVERTURN.**
   - **N15 UPHOLD.**
   - **N16 REFINE.** Bit 31 is named too: MKB_31 prints 0xffffffff80000000. Only bits 32-63 read 0.
   - **N17 UPHOLD (8), settled by reading R.** R's only post-refusal DATA read (`lw s2,16`) follows its own write to port 5 and is never printed; R prints only s1.
   - **N18 UPHOLD.** **N19 UPHOLD.**
   - **N20 UPHOLD.** K and R, which hold only the value 9, are the only DATA accesses behind any "the tripwire bounds it" argument.
   - **N22 UPHOLD.** **N24 UPHOLD.**
   - **N23 UPHOLD the four channel corrections; OVERTURN its parenthetical** ("more than 108 holds"). It contradicts N9, which you also accepted, and period 108 escapes.

7. **Six of your accepted dispositions are wrong**, the first two materially:
   - N4's consequence clause;
   - N23's parenthetical, accepted alongside N9 on the same boundary — the measurement sides with N9;
   - N16's "up to 30";
   - N3's "> 108";
   - N2's scope (only 6) and its "the exit returns";
   - N13, which dropped a refuted premise instead of recording it.

8. **What all of us missed.**
   - (a) **The "bounded by the tripwire" argument is false for wide values.** A let-through whose low 32 bits are 0-7 becomes a legal selector silently. If the process dies at all, it is through the filed command default (`fbctrlcmdkill`), not the kept check. This is the pre-#549 truncation defect coming back. It defeats the (0)-side's argument on N1 (bits 33-63, 31 of the 58), on N4, and on N2.
   - (b) D1 and D2 share one repair, and the anchor choice decides whether that repair closes D2 or reopens it.
   - (c) The two 58s are different sets. N1's is bits 4-7, 9-31 and 33-63; N21's is bits 5-7 and 9-63. Taking grok's 58 leaves 2^32 open for D2.
   - (d) PRETABLE_ADDENDUM_t6 carried its GUARD-vs-BODY section over "unchanged" in the same table that introduced B's generating set. Re-run against B, it would have asked at which latch state each bit is held — which is N1.
   - (e) Apparatus trap: `wsl -d Gentoo -- sed -i 's/\r$//'` run from git-bash deletes a trailing letter `r`, not a CR. It corrupted one of my scripts; a NameError caught it. The dollar guard can't see this because there is no `-c`.

9. **Artifacts.** Logs are in WSL `/tmp/opusf2v6/seat/logs/`, and copied to `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\opusf2v6_seat\logs\` (outside the project).
   - `TABLE_f2v6.out` — every score, on v6 and on the `sd`-at-7 copy
   - `MANIFEST.out` — the 22 predictions, written before building
   - `BUILD.out` — md5s and the restore record
   - `TABLE_U.out` and `U_*.out` — the U prototype runs
   - `WITNESS.out`, `SIM_ANCHORS.out`, `B_REGS.out`, `v6_sd7.diff`
   - 46 raw probe logs, each ending `FBCTRLP_DONE`
   - Scripts: `/tmp/opusf2v6_scripts/`. Binaries: `/tmp/opusf2v6/seat/bins/`.

---
*Recorded by the main loop: agent a0e1c60f2041a0a33, final text by claude-opus-5-5 (last block 2026-09-26T01:46:56.500Z), extracted verbatim from the agent transcript; agent_models.py: clean (claude-opus-5-5, 143 runs, no refusal).  Its logs and scripts are copied to regress/artifacts/fbctrlportkill_20260924/opus549_measured/f2v6/.  Badge s.*
