FABLE_SEAT_ALIVE_20261102_577F2
# ADJUDICATION PASS (F2) -- `shblreset` (#577): the panel shares its pass-2 findings; adjudicate them
F2 VERDICT: RATIFY WITH CHANGES (4)

Fable 5.1, ADJUDICATING seat (the owner's 09-25 rule: codex walled, Fable adjudicates, Astra confirms later).  READ-ONLY: nothing
built, nothing run against any project tree, nothing written but this file.  Disclosed self-review: P1, P3-P7, P9-P12 and P14 are my
pass-2 findings; every one was re-derived below from the artifacts or the tree, and the question asked of each was whether the
disposition that ADOPTED it is right, not whether the finding was.

**Evidence basis, stated on its face: 3 of 5 rostered seats answered this F2** (this seat; Grok 4.7 `f2_20261102/grok.txt`
19:41:49; Argon `f2_20261102/argon/gemini_web.out` 19:29:49).  **GPT-6 Astra is WALLED (weekly) and owed; glm-5.3 is DOWN
(Ollama 403/1010).**  Both are seat failures, not agreement.  This ruling is therefore PROVISIONAL per the carrier's rule, and the
commit holds for Astra by owner ruling.  Nothing below should be read as lifting that hold.

**HEAD at adjudication time is `3cb8bdc1`, not the packet's `20bfde13`.**  `git log`: 3cb8bdc1 (19:20:16, ledger.json + matrix.html
only) landed EIGHT MINUTES BEFORE the packet was written (brief_shblreset_f2.md mtime 19:28:11), so the packet's HEAD line was stale
when written.  Harmless to every number in it: `git diff --stat 987cb596 HEAD -- src/ regress/ OUTSTANDING_BUGS.md CHANGELOG.md`
shows OUTSTANDING_BUGS.md +347 (20bfde13) and nothing else -- `src/` and `regress/` are unchanged since 987cb596, and
OUTSTANDING_BUGS.md `:8238` and `:24063` are the same text at 987cb596, 20bfde13 and 3cb8bdc1 (the 347 lines landed after both).
The round block and the ledger close must name 3cb8bdc1 (or whatever HEAD is at landing) with that proof.

## 0. What was CHECKED (under two minutes each; measured, not judged)

1. **Scores, every raw opened.**  base_head 7/10 (bl trapa / bl mhit / bl ldmis each 0x00000000); fixed 10/10; M_b 7/10; M_c 8/10
   (0x160, 0x0e0); M_noex 9/10 (mhit 0x020); M_wrongex 8/10 (trapa 0x160, mhit 0x020); M_lt100 8/10 (mhit 0x020, ldmis 0x0e0);
   M_trapaonly 9/10 (ldmis 0x0e0); M_power 8/10 (trapa, ldmis 0x000); **M_guard 9/10, `tlbm trapa` 0x00000020 want 0x00000160**;
   **M_resinst 10/10.**  Every header: `binary newer than cpu_sh.c: yes`; every mutant leg carries its sentinel, base_head none.
   base_head md5 b76a7799a3ea == M_b md5 (P11 holds); fixed md5 b7b0d0b5f5ae == witness_fixed md5 (P7 holds); M_guard 8e53c40288fa,
   M_resinst 2fc3306dd0b2, each distinct from fixed.
2. **mtimes, `ls --time-style=full-iso`, both copies.**  PRETABLE.out 18:10:13.379 < run_killtable577.run-181013.sh 18:10:13.517
   (the frozen driver) < BUILD_FIXED.log 18:11:05.717 < base_head.raw 18:14:06.577 -- **the table's order proof holds on mtimes
   alone.**  (The packet's "KILLTABLE.log 18:11:05" is that log's CONTENT; its mtime is 18:39:34, the last write.  Cite the chain
   above.)  **PRETABLE_CORRECTION.out is 19:28:05.560 in BOTH copies -- AFTER M_guard.raw 19:14:12.868 and M_resinst.raw
   19:24:09.193.**  pass2_20261102: argon/gemini_web.out 18:43:04.80, grok.txt 18:53:22.23, fable5.md 19:01:50.85.  run_mguard577.sh
   19:10:42; mutate577.py 19:20:21; run_mutleg577.sh 19:20:45; sh_tlbmulti_probe.NEW.py 19:20:48; ASRUN_NOTE.txt 19:20:52.
3. **cmp across the two dirs: all 17 table files SAME** (PRETABLE.out, PRETABLE_CORRECTION.out, 3 logs, 11 raws, BUILD_FIXED.log),
   mtimes preserved; mutate577.py, apply_fix577.py, product.diff and NEW.py SAME.  P10's repair is real.
4. **AST, by my own script (`python -I`, `ast.dump`):** ASRUN.py and NEW.py are identical **with docstrings KEPT** (18555 chars each),
   not merely with docstrings dropped -- all three post-table edits are `#` comments inside the #577 block (the unified diff shows
   exactly those three passages).  Same ten `row()` names.  ASRUN md5 d41edccdee1c matches both post-table raw headers.
5. **The as-run identity of the SEVEN TABLE legs** (whose raws do not stamp an instrument md5): HEAD's probe vs ASRUN.py gives the
   four hunks `-52,9 +52,10 / -88,11 +89,13 / -122,14 +125,18 / -191,4 +198,33`, the pass-2 brief's section-3 diff exactly
   (header dated 18:08:36); run_probe_leg577.sh ran `$W/sh_tlbmulti_probe.NEW.py` 18:11-18:39; NEW.py's first edit is 18:54.  Sound.
6. **Source at HEAD, read not recalled:** `:910` guard; `:941-942` spc/ssr written; `:945-950` the intevt/expevt store; **`:952`
   `sh_update_sr(cpu, sr | SH_SR_MD | SH_SR_RB | SH_SR_BL)`**; `:1015-1021` ONE arm for RESET_POWER / RESET_MANUAL /
   RESET_TLB_MULTI_HIT (so H'020 has an arm; the fix opens no path to `default: ... exit(1)` at `:1083-1085`); no arm for
   EXPEVT_BREAK or EXPEVT_FPU; `:129` `CPU_SETTINGS_ADD_REGISTER32("sr", cpu->cd.sh.sr)`; `:846-860` `sh_update_sr()` is the only
   bank swap.  cpu_dyntrans.c:247 gates interrupts on `!BL`; cpu_sh_instr.c:209-220 (align checks), :242-246 (RES_INST), :252-263
   (SLEEP refuses under BL), :2852-2858 (TRAPA sets TRA then raises).  Caller census by `git grep sh_exception(` at HEAD: RES_INST,
   FPU_SLOT_DISABLE, FPU_DISABLE, ADDR_ERR_LD/ST, SLOT_INST, TRAPA, memory_sh.c TLB codes, dev_sh4.c:1178 multi-hit, the dyntrans
   interrupt -- **no raiser passes H'000, H'020, H'120 or H'1E0.**  The codes live at `src/include/thirdparty/sh4_exception.h:57-75`
   (not `src/include/`); there is **no macro `EXPEVT_TLB_MISS`** -- the members are `EXPEVT_TLB_MISS_LD` 0x040 / `_ST` 0x060 (Grok F2).
7. **Manual, every section-3b line printed by awk and matched verbatim**; also `:675-685` (the revision table with its page-number
   column interleaved -- P2 is right), `:12372-12389` (5.6.1 (2), `:12376` the source line, `:12383-12384` the EXPEVT sentence),
   `:12455-12465` / `:12495-12503` (both multiple-hit sentences H'140), `:13162-13171`, `:41448-41452`, and **`:40308-40317` ICR.NMIB**
   (NMIB=1: "NMI interrupt requests detected while SR.BL bit is set to 1").
8. **Gate hunks vs HEAD:** #577 `@@ -251,9`; #576 (`_scratchpad/w576/gate_sh_rounding.NEW.sh`) `@@ -56,14` and `@@ -77,7`; the working
   tree's unrelated three at 527/587/819; **the index now holds CHANGELOG.md +77/-75** (a different batch from the one pass 2 saw).
   The two held rounds' hunks are DISJOINT -- the reconciliation at landing is a clean merge.
9. **Trees:** `est/regress` is ABSENT, so the "byte-identical in est" obligation is `cpu_sh.c` only; `cpu_sh.c` md5 d323d495... is
   identical in SEC, est, build, build-asan and HEAD; build and build-asan binaries are newer than their `cpu_sh.c` today.
10. **Ledger row `shblreset` at HEAD:** state open, witness "", commits "", ONE entry (the 10-02 filing); zero pass-1 / pass-2 / F2 seat
    entries; its `state_note` cites the prose carrier as "lines 8145 at db8b1a33" -- it is `:8238` at HEAD.
11. `mutate577.py` parses (`ast.parse`); its M_guard branch is one C line; MGUARD.log and MUTLEG_M_resinst.log each carry the one-line
    mutant diff against the fixed clone.

## 1. P1..P18 and D1..D2

| # | ruling | reason (checked) |
|---|---|---|
| P1 | **UPHOLD the measurement; REFINE the order clause** | M_guard.raw 9/10, `tlbm trapa` 0x020, read.  `BL|MD` is the least-restrictive widening that fires under the probe's state; a widening that fires only under a state no row holds (FD, RB, IMASK) is (e), disclosed in PRETABLE ("Partition on sr beyond BL: none tested").  **But "the prediction was written FIRST into PRETABLE_CORRECTION.out (mtime 19:08:32)" is not observable: the file is 19:28:05 in both copies.**  The prediction IS pre-leg -- by `pass2_20261102/fable5.md` 19:01:50.85 < M_guard.raw 19:14:12.87, which carries "9/10, `tlbm trapa` reads 0x00000020" verbatim.  Cite that. |
| P2 | **UPHOLD** | `:678-681` is the revision table (page column interleaved); NEW.py `:204-205` now cites 5.6.1 (2) `:12376` / `:12383-12384`.  Edit is comment-only (AST identical). |
| P3 | **UPHOLD as done for its own claim; REFINE (change 2)** | Both directions of the CODE axis are now named, correctly.  Grok's F2 shows the sentence still names only code moves: a guard qualified on an sr bit no row varies (`&& !(sr & SH_SR_RB)`) moves no code and escapes all ten rows.  See section 3. |
| P4 | **UPHOLD** | mutate577.py `M_c` replaces the two fixed lines with `;`; guard and `fatal()` stay.  "REWRITE deleted" is what M_c.raw measured (8/10). |
| P5 | **UPHOLD** | `:8238` (prose row, stale `cpu_sh.c:653` cite) and `:24063` (id entry) verified identical at 987cb596, 20bfde13, 3cb8bdc1 and the working tree.  Mark both by content, not line. |
| P6 | **UPHOLD, strengthened** | My own AST compare: identical with docstrings KEPT.  Rows, wants and oracles are one instrument; **no table re-run on the shipped text is owed.** |
| P7 | **UPHOLD** | Both product.diff copies read: identical code lines; the witness copy carries the pre-F4 comment (":678-681", "Interrupts do not reach this path"); md5s as stated.  Kill-table copy is the shipping text. |
| P8 | **UPHOLD the measurement and the (e) grading; REFINE the record** | M_resinst.raw 10/10 as predicted.  Grading: the conjunct tests `expevt` at a value no body test distinguishes; by the 09-04 joint-cells and 10-09 7n-5 rulings ("a value the body never tests as a case ... is clause (e)") it is debt, not floor -- and note the 08-28 `#488` sentence ("`if (X)` -> `if (X && Y)` on the dominating predicate is canonical (d)") reads the other way; the later, narrower rulings govern, and the same edit can be written on either predicate, so the grading must rest on the body-tested partition, which it does.  Records: the order clause "mtime 19:20:29 precedes the raw's" is false on disk (see P17); the predictions are pre-leg by gemini_web.out 18:43:04 / grok.txt 18:53:22 / fable5.md 19:01:50 < 19:24:09.  And Argon's member `EXPEVT_TLB_MISS` is not a macro: write `_LD`/`_ST`. |
| P9 | **UPHOLD** | `:129` registers the raw field; `sh_update_sr()` `:846-860` is the only bank swap; the debugger's `sr=` writes without a swap.  The shipped sentence is the mechanism. |
| P10 | **UPHOLD** (Argon's OVERTURN rejected) | 17 files cmp SAME, originals untouched, source mtimes preserved on the copies.  Restoring the ORIGINAL's mtime on a byte-identical copy is preservation, not tampering; the untouched w577 originals remain the primary witness.  Precision: the pure-mtime chain is PRETABLE.out < frozen driver < BUILD_FIXED.log < base_head.raw (section 0.2). |
| P11 | **UPHOLD** | b76a7799a3ea in base_head.raw and M_b.raw; it is the strongest proof that the fixed clone is HEAD + this block and nothing else. |
| P12 | **UPHOLD, with two measured additions** | Hunks disjoint (#576 @@-56/-77, #577 @@-251, tree 527/587/819); the index has changed AGAIN since pass 2 (now CHANGELOG.md +77/-75) -- stage by path from HEAD-based copies, as the packet says. |
| P13 | **UPHOLD** | `:12499` read; same H'140; `:12461` is a true cite. |
| P14 | **UPHOLD the rejection** | `:945-950` read: intevt path stores INTEVT, `expevt = -1`, EXPEVT never written.  Sentence true; no post-pass-2 product-comment edit for style.  (D2) |
| P15 | **UPHOLD** | `:13165-13166` "undefined"; HEAD `:941-942` writes them; any value complies. |
| P16 | **UPHOLD; REFINE (change 3)** | cpu_sh_instr.c:260-263 and cpu_dyntrans.c:247 refuse under BL; `:13171` accepts in sleep.  The filing should also carry the NMIB clause (section 3). |
| P17 | **OVERTURN as a record (L4, correct in place)** | The addendum-2 MEASURED paragraph says "(this file's mtime 19:20:29 precedes the raw's 19:24:09)" -- a hand-written, SELF-REFERENTIAL mtime, false from the moment it was saved (the write that added it set the mtime past 19:24:09), and the file is now 19:28:05.  "No hand-written time" is refuted by the file's own text.  The measurements are unaffected; the record is wrong.  Grok's UPHOLD here is a reading ("mtimes were not re-stated this turn"); this is the measurement. |
| P18 | **UPHOLD; one clause CANNOT SETTLE** | The file parses; the M_guard branch is one line.  "The seven table branches are byte-unchanged" has no preserved pre-19:20 copy to check against; the indirect evidence (branches read as the brief described, nine scores reconcile with those texts) is accepted and the clause is recorded as inferred, not measured. |
| D1 | **UPHOLD (disclose AND file); REFINE the row** | The carrier: an above-floor MEASURED escape is filed with its escape list, below live defects.  Argon's "noise / contradiction" misreads a disclosure as a waiver: the contract says the instrument does not see it; the row says it is measured debt.  Refinements: members = the TEN raisable undriven codes (H'040, H'060, H'080, H'0A0, H'0C0, H'100, H'180, H'1A0, H'800, H'820); H'120 and H'1E0 have neither raiser nor switch arm, so an exemption at either is EQUIVALENT (not an escape); correct macro names; EXHAUSTED/SAMPLED vocabulary (body-tested partition {H'140, other} EXHAUSTED; the raw code domain within "other" SAMPLED at 2 of 12 raisable general codes); the cheapest closing row; **plus Grok's second member family -- the guard qualified on an sr bit other than BL (section 3).** |
| D2 | **UPHOLD** | Leave the product comment.  The no-raiser fact (H'000, H'020) goes in the round block, with Grok's sharpening: a later H'000 raiser through this block would be stored as H'020 and needs its own exemption. |

## 2. Which accepted disposition is most likely WRONG

**P17, and with it the order-proof clauses of P1 and P8.**  It is not likely wrong; it is measured wrong.  The packet rests both
post-table legs' "predicted first" status on PRETABLE_CORRECTION.out mtimes (19:08:32, 19:20:29) that no longer exist -- the file was
rewritten at 19:28:05 to add addendum 2's MEASURED paragraph, and that paragraph itself carries a hand-written mtime of the file it is
in.  This is the #576 lesson applied to its own remedy: PRETABLE.out was kept mtime-frozen by sending corrections to a SIBLING file,
and the sibling then took FIVE writes (correction, prediction 1, measured 1, prediction 2, measured 2), so its mtime proves only that
the last write came after both legs.  **The predictions survive on other artifacts** -- the three pass-2 answer files (18:43:04,
18:53:22, 19:01:50), run_mguard577.sh 19:10:42 and mutate577.py 19:20:21, all before their legs -- so the measurements stay
predicted-first; only the citation is wrong.  Runner-up by contestability (not by evidence): D1's (e) grading of the conjunct class,
because the carrier carries a 2026-08-28 sentence that grades `if (X && Y)` as canonical (d); I have written the resolution into P8 so
a future reader does not re-litigate it from that sentence alone.

## 3. What all of us missed

1. **The order proof decayed into the file built to protect it** (above).  Structural fix, not prose: ONE file per pre-leg prediction
   (`PREDICTION_<leg>.out`), never written again; the measured paragraph goes to the leg's `.log`, which the driver already writes.
2. **The guard's sr axis beyond BL -- Grok F2, verified here.**  Every BL row presets `sr = 0x500000f0` (MD=1, RB=0, IMASK=0xf, FD=0).
   The state a real BL-set exception most often occurs in is the one `:952` produces on every exception entry -- RB=1 -- and a kernel
   critical section (`ldc` setting BL alone) gives RB=0; both are reachable.  A guard qualified `&& !(cpu->cd.sh.sr & SH_SR_RB)` (or on
   IMASK, which `:952` leaves untouched, or on MD) keeps all ten rows green and skips the manual reset on the other state.  By the
   body-tested-partition rule it is clause (e) -- the guard tests BL only -- and the PRETABLE disclosed it in one clause ("Partition on
   sr beyond BL: none tested by the body"); **the probe CONTRACT, which is what a future editor reads, names only code moves.**  Not a
   floor breach, not a row owed (a filter may reject or repair, never demand); it is a disclosure gap in the shipped text and a second
   member family for `shblundriven`, with the cheapest row named: `sr=0x700000f0`, `trapa #1`, want 0x00000020.  NOT measured; no score.
3. **The NMI half of the deleted TODO.**  The diff deletes "or on NMI interrupts if a special flag is set?" -- that flag is ICR.NMIB
   (`:40308-40317`; NMIB=1 means an NMI is detected while BL=1), and 5.5.3 `:12307-12308` / 5.7.2.b `:13169-13170` say so.  The tree
   refuses every interrupt under BL (cpu_dyntrans.c:247) and `dev_sh4.c` at HEAD has no NMI model at all (no "NMI" in the file).  The
   new comment's "cpu_dyntrans.c delivers none while BL is set" is TRUE of the tree, but the deleted line was the only in-code record of
   the unmodelled hardware case.  It is the SAME class as the SLEEP-under-BL filing (an interrupt the manual accepts under BL that the
   tree refuses, in the same manual sentence); one clause in that filing carries it.  Documented-only; no code (no raiser, no model).
4. **HEAD moved during the pass** (section header) -- records-only, proven harmless, but the F2 record and round block must name it.
5. **The seven table raws carry no instrument md5**; only the post-table raws do.  The identity was re-derived here (section 0.5) and
   holds; one `md5sum` line in the leg script makes the next table self-certifying.
6. **Three small record precisions:** `EXPEVT_TLB_MISS` is not a macro (Grok); H'120 is in the contract's undriven list but has no
   raiser and no switch arm, so it is unraisable rather than undriven; `est/` has no `regress/`, so the landing's byte-identical
   obligation is `cpu_sh.c` only.  And the floor record should write "(f): N/A -- no address decode under test" and "edge rule D2:
   N/A -- an equality compare, pinned by `tlbm bl mhit` (M_wrongex 8/10)" rather than leave either blank.
7. **Argon's "missed user-break exemption" is REFUTED, and the refutation is worth keeping:** EXPEVT_BREAK has no raiser (census, 0.6),
   the UBC suppresses the break under BL before any exception starts (`:41452`), and the switch has no H'1E0 arm, so any user break
   raised today would `exit(1)` at `:1085` regardless of BL -- a future raiser owes an arm and its UBC gating at the raiser, not an
   exemption here.  Packet-fed, Argon could not see the census; recorded as a reading limit, not adopted.

## 4. The four changes (all records or comment-only; the product diff and every detector ROW are unchanged; no re-run owed)

1. **L4 -- the order proof.**  Correct PRETABLE_CORRECTION.out in place, quoting the sentence it refutes ("this file's mtime 19:20:29
   precedes the raw's 19:24:09"), and state the real proof: fable5.md 19:01:50.85 < M_guard.raw 19:14:12.87; gemini_web.out 18:43:04 /
   grok.txt 18:53:22 / fable5.md 19:01:50 < M_resinst.raw 19:24:09.19; this file's mtime is its last write.  Re-copy with `cp -p`.  The
   round block says the same in one sentence and drops "mtime 19:08:32".
2. **Post-table comment edit 4 (comment-only, logged in ASRUN_NOTE.txt, AST re-checked identical):** the contract's clause-(e)
   sentence gains the sr axis: "rows hold MD=1, RB=0, IMASK=0xf, FD=0; a guard qualified on any sr bit other than BL -- RB first, the
   state every exception entry leaves at cpu_sh.c `sh_update_sr(... | SH_SR_RB | SH_SR_BL)` -- is clause-(e) disclosure; cheapest row
   `sr=0x700000f0`, `trapa #1`, want H'020."  The same clause goes into `shblundriven` as its second member family.
3. **The SLEEP-under-BL filing gains the NMIB clause** (manual `:12307-12308`, `:13169-13171`, `:40308-40317`; dev_sh4.c has no NMI
   model; the deleted TODO was the only record).
4. **Records bundle for the round block / ledger / bug file:** HEAD 3cb8bdc1 with the unchanged-tree proof; `shblundriven` as refined
   in D1 (ten raisable members, H'120/H'1E0 unraisable, correct macro names, EXHAUSTED/SAMPLED, M_resinst.raw as evidence, both member
   families); (f) and D2 recorded N/A with reasons; the `est/` scope; the ledger close cites the prose carrier by anchor (its
   `state_note` says "8145 at db8b1a33"; it is `:8238` at HEAD) and records ALL THREE stages' seats with their `w577/pass1_20261102`,
   `pass2_20261102`, `f2_20261102` dirs, with Astra WALLED and glm DOWN by name in each -- the row carries zero seat entries today.

## 5. The other F2 seats, counted by argument

* **Grok (RATIFY WITH CHANGES (1))**: its one change -- the sr-axis gap in the clause-(e) sentence -- is ADOPTED (change 2); its
  `EXPEVT_TLB_MISS` catch and its user-break refutation are adopted into the records.  Its P10/P17 UPHOLDs are readings by its own
  statement ("mtimes were not re-stated"); on P17 the measurement here overturns the record.  Its Q2 answer (P3) and mine (P17) are
  different findings and both stand; mine is the one that is false on disk today.
* **Argon (20 ATTACKS, 2 BROKEN)**: both overturns (P10, D1) REJECTED on measurement and on the carrier's own rule; its user-break
  finding REFUTED by the raiser census and the switch.  Its eighteen UPHOLDs agree with the packet on inlined facts, which is worth
  nothing by itself (a stated premise is load-bearing for a packet-fed seat).  Not a seat failure: a complete, honest reading from a
  packet that could not show it the callers.

## 6. Owed and not changed by this ruling

The owner's hold for Astra stands; Astra's pass 2 and its confirmation of this adjudication are owed.  At landing, unchanged from the
packet's section 5: SEC + est byte-identical `cpu_sh.c`; build / build-asan / `/tmp/gxsec-build` propagated AND rebuilt with the
two-part clearance per tree (`est/`: source tree, part 2 N/A); `gate_sh_rounding.sh` end to end on the applied tree (pin 6 -> 10,
expect 10/10) from the HEAD-based copy, reconciled with #576's disjoint hunks; the bug file's two carriers; the CHANGELOG round block;
the ledger close with `probe:regress/artifacts/shblreset/witness_20261102/sh_blreset_witness.py` (rung 3: red 2/4 on HEAD, green 4/4
on the fix, same script; liveness `bl trapa pc` and control `nobl trapa expevt` present; unmodified in-tree landisk).  The fix is
right, the floor is closed on all four cells and now measured on the guard axis too, the nine scores plus two legs reconcile with
their raws, and nothing here touches product code or a detector row.

F2 VERDICT: RATIFY WITH CHANGES (4)
