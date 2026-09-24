# #545 fbdeclinefive -- PASS 2 findings, consolidated (read-only records pass, 2026-09-19)

Inputs: `brief_fbd5_p2.md`; panel `_scratchpad/panel_20260919_115657/` (8 transports); dedicated codex job
`fbd5/p2/codex_ded/`; Opus measuring seat `fbd5/opus_p2_20260919/OPUS_P2_ANSWER.md`.

**About "already addressed".** `CHECKPOINT.md` no longer has a section headed 12:1x or later from this session. The peer
session (e8a2bc) overwrote it with its own 12:2x section. So "already addressed" below uses the caller's summary: 23 X-rows,
IDENTITY 134, gate_offline pins, the corrected H2 header sentence, and gate_arm plus gate_offline both PASS. **Each item
was re-verified in the working tree:**
* `regress/diff_footbridge.c:712-777` holds the X1/X2/X3 block and IDENTITY "134".
* `regress/gate_offline.sh:588` pins 134 and `:596` pins the X rows.
* `regress/footbridge_sites_probe.py:69-75` now says the teardown-first reorder keeps H2 GREEN.

Tree for every CHECKED item: `GXEMUL-SEC/` working tree over HEAD f685d75. No other `src/` was read. Nothing was built or run.

## 1. Seat table

| seat (transport) | verdict line (quoted) | kind |
|---|---|---|
| codex (panel, GPT-6 Astra) | `NO-GO` | READING. It ran regex and patch checks on log copies and read-only git; no emulator or compiler. |
| codex (dedicated job, `codex_ded/`) | **no verdict line: NO ANSWER.** `codex_fbd5p2.txt` is 0 bytes. The `.err` ends mid-run (last write 12:33:40) after a `Reconnecting... 2/5` and two interim progress notes. | SEAT FAILURE: an unfinished run. Its interim notes are carried below as F7 and flagged unfinished. They are not a verdict. |
| agy (gemini-3.8-flash-high) | `**VERDICT: GO-WITH-CHANGES**` | READING |
| kimi (CLI, file-reading) | `**VERDICT: GO-WITH-CHANGES** -- the product change is correct and the measured table reproduces against the artifacts, but the frozen packet is already superseded by its own working tree, the shipped probe header carries one refuted claim, and the gate has three unpinned seams.` | READING. It also ran `patch -o` into /tmp to reconstruct files. |
| grok 4.6 | `**VERDICT: PRODUCT FIX SOUND -- do not treat the detector as class-closed.**` | READING |
| glm-5.3:cloud (packet-fed) | `VERDICT: **PASS WITH CONDITIONS -- the product diff is correct as inlined ... I found three one-line product edits that pass everything ... Clause (d) of the floor is breached on these three**` | READING (packet only) |
| deepseek-v4-pro:cloud (packet-fed) | `VERDICT: PASS -- the packet's own inlined diff and kill table are internally consistent, and I find no fatal defect.` | READING (packet only) |
| minimax-m3:cloud (packet-fed) | `VERDICT (READ): DIFF CORRECT UNDER ITS OWN TEST DESIGN; COMPOSITE DETECTOR SOUND FOR THE 11 MUTANTS MEASURED, WITH ONE PARTIAL HOLE FOR A LEN-GUARD MUTANT ON THE 4 SITES NOT COVERED BY P9` | READING (packet only) |
| kimi-k3:cloud (packet-fed substitute) | `VERDICT: CONFIRM the diff and the table as internally coherent ... with ONE real detector hole (width-as-first-access is rowed only for IRQ_STATUS/byte ...)` | READING (packet only). **Its seat record calls itself "Claude (Anthropic)"**; the transport is kimi-k3:cloud. Record the seat by transport. |
| Opus 5 (Agent, measuring) | `**VERDICT: DO NOT SHIP AS-IS. FLOOR BREACH (L2), MEASURED.**` | **MEASUREMENT.** 14 fresh builds, 15 sites runs, 13 differential runs and 11 compile-only runs in the clone `/tmp/gxopusfbd5p2`; the clone was restored and passed cmp. |
| Fable 5 | not fired | HELD by owner directive, recorded as held (neither a failure nor agreement). |

**Unanimous on the product change.** No seat names a defect in `dev_footbridge.c`'s five arms. The common tail runs, the
+0x18c leak is gone, only the latch changes, and member 3 is still the right option.

## 2. Findings

Categories: DEFECT-IN-DIFF / DETECTOR-GAP / WRONG-RECORD / ALREADY-ADDRESSED / DESIGN-DISSENT / OUT-OF-SCOPE-FIND.

### Detector: the width, latch and expression closures

**F1 -- `&& len == 4` on any decline other than IRQ_STATUS escapes; halfword-first is unrowed everywhere.**
* **Raised by:** Opus (MEASURED A1-A4: 36/36 and 111/111), codex, agy, kimi, grok, glm, deepseek, minimax, kimi-sub. Nine independent seats converged.
* **Evidence:** arm S uses word accesses only. The P-loop latches with a word access before its byte and halfword accesses. P9 is byte-first at IRQ_STATUS only.
* **Category:** ALREADY-ADDRESSED by X1: every site x len {1, 2} as the first access. **CHECKED-TRUE** at `diff_footbridge.c:734-742`.

**F2 -- A narrowed dominating predicate escapes.** The mutant is `writeflag == MEM_READ && len == 4` at IRQ_STATUS (G1) and FIQ_RAW_STATUS (G2).
* **Raised by:** Opus only (MEASURED, 36/36 and 111/111).
* **Evidence:** no row does a legal byte or halfword read. Under the mutant a narrow legal read returns 0, announces a phantom write and consumes the latch.
* **Category:** ALREADY-ADDRESSED by X2 (legal narrow reads of the five readable registers). **CHECKED-TRUE** at `:744-753`.

**F3 -- A legal read re-arms a latch.**
* **Raised by:** Opus (MEASURED B1/B2/B3 escape: own-register read, the +0x188 read, a cross read at the FIQ pair), grok and glm (the own-read form), codex (the FIQ_RAW-read-clears-FIQ_STATUS form), kimi-sub (a +0x188 read clearing the IRQ_STATUS latch).
* **Evidence:** arm S's between-reads pair each site with one fixed register. P0 runs before the declines and P7 after them.
* **Category:** ALREADY-ADDRESSED by X3, which reads all five readable registers at widths 1, 2 and 4, then repeats the declines. **CHECKED-TRUE** at `:754-767`.

**F4 -- A latch cleared by an access to a register OUTSIDE the five readables still escapes.** Examples: a legal TIMER_1_VALUE read, VENDOR_ID, the +0x288/+0x28c reads, or any legal WRITE.
* **Raised by:** kimi (TIMER_1_VALUE named).
* **Evidence:** X3's `rd5[]` lists only IRQ_STATUS, IRQ_RAW, FIQ_STATUS, FIQ_RAW and IRQ_ENABLE_SET, all as reads.
* **Category:** DETECTOR-GAP, **open**. **CHECKED-TRUE** by reading `:725-728` and `:759-762`. Not measured.
* **Grade is disputed (see D2):** Opus and grok place latch-writer insertions in sibling cases outside the diff-closed (d) enumeration.

**F5 -- A wrong-field operand swap in the IRQ_STATUS read survives the seeds.**
* **Raised by:** codex, glm. Independent convergence; both call it an L2 (d) breach.
* **The mutants:** `odata = d->fiq_status & d->irq_enable` gives 0x50 & 0x30 = 0x10. `odata = d->irq_status & d->fiq_status` gives 0x18 & 0x50 = 0x10. Both equal the expected 0x10, so P0 and P7 stay green, and the guest reads 0 either way.
* **Evidence:** codex enumerated all operand replacements for the four expressions. Only these two collide; commuting the operands is equivalent. glm's repair is `fiq_status = 0x60` (masked value stays 0x40, so M8 stays killed; the cross value becomes 0x20). It enumerated all twelve two-operand forms clean under {0x18, 0x30, 0x60, 0xc0}.
* **Category:** DETECTOR-GAP, **open**. The X-block reuses the same seeds (`XSEED`, `:732-733`). **CHECKED-TRUE** by arithmetic and reading. Not measured.
* **Refutes:** the "all seeds distinct, any cross-field swap reds" claims of kimi-sub, agy and deepseek.

**F6 -- Declined NARROW reads of +0x18c are not scored for value or return code.**
* **Raised by:** codex.
* **Evidence:** P3's len-1 and len-2 accesses check only the announce delta. X1's read-site rows check only `fatal_calls`. A mutant that leaks `irq_enable` only when `len != 4` stays green.
* **Category:** DETECTOR-GAP, **open**. **CHECKED-TRUE** by reading `:675-681` and `:734-742`.

**F7 -- A latch conjunct on NONZERO write data or a NONZERO irq_enable escapes, e.g. `&& idata`.**
* **Raised by:** the dedicated codex job's interim note only: "a latch can wrongly depend on nonzero write data or a nonzero IRQ enable, because every tested access satisfies those conditions". The job produced no final answer.
* **Evidence:** every declined write in P, X1 and X3 carries 0x70, and arm S writes 0x10/0x40. Every offline instance is seeded with irq_enable 0x30, and arm S sets 0x30 before its declines.
* **Category:** DETECTOR-GAP, **open**. **CHECKED-TRUE** that the tested data are all nonzero (`diff_footbridge.c:663,738,755`; sites header `:83-85`). Not measured.
* **Grade:** unsettled. The decline body reads neither lvalue, so a strict DEPENDS-ON reading may place it under clause (e).

**F8 -- Floor clause (b), reinstatement at EVERY site: only FIQ_RAW_STATUS (M1) was measured.**
* **Raised by:** codex ("four isolated reinstatement measurements remain owed").
* **Counter-view:** agy, kimi, grok, glm, minimax and kimi-sub argue it holds structurally: arm S is one sequential process and any death reds the same 15 rows.
* **Category:** DETECTOR-GAP (a floor measurement owed), open, disputed (D5). NOT CHECKED.

### Detector: gate pins and harness legs

**F9 -- Gate count pins without a distinct-id guard.** `^S[1-5] .*ok$`==5, `^SF[12]`==2 and `^S(C1|A1)`==2 are all satisfied by a duplicated green line.
* **Raised by:** codex (tested on modified FIX-log copies), kimi, kimi-sub, glm (conditional), grok ("harmless").
* **Category:** DETECTOR-GAP, low. **CHECKED:** true that no distinct-id guard exists. But `gate_arm.sh:1086` pins `FOOTBRIDGE_SITES_PASS`, so any row that is RED still reds the gate. Only a row that is both unprinted and unscored escapes.

**F10 -- C4's strengthening has no individual gate pin.**
* **Raised by:** kimi.
* **Category:** DETECTOR-GAP, low. **CHECKED-TRUE:** there is no `^C4` pin; it is covered only through the PASS token.

**F11 -- The drain and witness H1/H2 legs are not gate-pinned.** A broken H2 there fails no gate.
* **Raised by:** grok.
* **Category:** DETECTOR-GAP, open. **CHECKED-TRUE:** `gate_arm.sh` has no `fbpending_*` reference, and `gate_offline.sh:1277` says the drain probe "is NOT run here".

**F12 -- `quit_rc` is recorded and scored nowhere.** The smallest vacuous H2 edit is to reuse `quit_rc` as `next_rc`, which drops the extra `reg`.
* **Raised by:** codex (the edit), kimi and grok (unscored).
* **Category:** DETECTOR-GAP (harness), open. **CHECKED-TRUE:** `h2_ok` at sites `:547` and the drain/witness row predicates omit it. Not measured.

**F13 -- Vacuous H2 edit: drop `dead_before_close` from the conjunction.**
* **Raised by:** kimi.
* **Category:** DETECTOR-GAP (harness). NOT CHECKED (unmeasured).

**F14 -- Vacuous H2 edit: hardcode `dead_before_close = True`.**
* **Raised by:** agy.
* **Category:** DETECTOR-GAP (harness). NOT CHECKED.

**F15 -- Vacuous H2 edit: drop the `prologue_ok` clause or its register values.**
* **Raised by:** deepseek, kimi-sub.
* **Category:** DETECTOR-GAP (harness). NOT CHECKED.

**F16 -- Vacuous H2 edit: `exit == 0` becomes `exit is not None`.** A quit path that exits 1 would then pass.
* **Raised by:** glm. Opus's M13q measurement shows `exit == 0` is load-bearing.
* **Category:** DETECTOR-GAP (harness). NOT CHECKED.

**F17 -- Weaker H1 edit: drop the machine NAME from the text search.**
* **Raised by:** grok, who judges it almost as strong because only an unknown `-E` prints "is unknown".
* **Category:** DETECTOR-GAP (weak). NOT CHECKED.

### Records already corrected after pass 2

**F18 -- The probe header's "teardown-first -> H2 must red" was false.** It was measured GREEN (M13).
* **Raised by:** Opus (MEASURED M13/M13q), kimi, codex.
* **Category:** WRONG-RECORD, ALREADY-ADDRESSED (header rewritten). **CHECKED-TRUE** at sites `:69-75`.

**F19 -- Under teardown-first, only `exit == 0` separates a quit from a closed pty sending SIGHUP (M13q).**
* **Raised by:** Opus (MEASURED), codex.
* **Category:** ALREADY-ADDRESSED; the header now says so.

**F20 -- "Widths ... rowed OFFLINE (P-rows)" and the M11 disposition ("equivalent mutant ... add P9") claimed a closure that covered 1 of 5 sites and 1 of 2 widths.**
* **Raised by:** grok, codex, glm, kimi-sub, minimax, deepseek, agy.
* **Category:** WRONG-RECORD, ALREADY-ADDRESSED in substance by X1.
* **Residue:** sites `:98-101` still attributes the width rows to "P-rows" only. That is true now, but it should name X1.

### Wrong records still open (all were verified in place unless marked)

**F21 -- PRETABLE's CHANNEL table says M13 was "Measured as a probe mutant in the clone"; the table section says it was NOT built.**
* **Raised by:** codex, kimi.
* **Status:** **CHECKED-TRUE** in brief `:686-692` vs `:751-753`. Opus has since measured it, so the round record should cite Opus's M13/M13q.

**F22 -- Both pending-probe headers still describe arm K as a live failability control ("K must kill the host").**
* **Raised by:** codex.
* **Status:** **CHECKED-TRUE** at `fbpending_witness.py:74-81` and `fbpending_drain_probe.py:64-67`.

**F23 -- The sites header says "the FIQ read EXPRESSION is unpinned everywhere".** P0, X2 and M8 contradict it; it should say "not established through reachable guest state".
* **Raised by:** codex, grok.
* **Status:** **CHECKED-TRUE** at `:145-146`.

**F24 -- "S3 (a legal EnableClear write works, a zero write preserves) is E5's row already" misidentifies S3.** S3 is an IRQEnable read expecting 0x30, and no row tests a zero Clear write.
* **Raised by:** codex, grok.
* **Status:** **CHECKED-TRUE** at `:102`.

**F25 -- "arms L/T/K are byte-identical to what they were": arm K is retired.**
* **Raised by:** grok.
* **Status:** **CHECKED-TRUE** at `:104`.

**F26 -- The arm S description says each site has a "LEGAL read of a SIBLING register" between its two declines.** For N4 and N5 the between-read is the SAME register (+0x280 / +0x284).
* **Raised by:** grok.
* **Status:** **CHECKED-TRUE** at `:77-78` vs `:91-92`.

**F27 -- "(c) irq_status and fiq_enable are 0 throughout" is ambiguous.** It is true of arm E's process, which is the clause's context. It is false of arm S, which writes fiq_enable 0xc0.
* **Raised by:** codex.
* **Status:** CHECKED. Minor.

**F28 -- The differential's P-block comment says "this instance's d->irq callbacks are NULL (calloc)".** Counting no-ops are installed before any access.
* **Raised by:** codex, deepseek (partially).
* **Status:** **CHECKED-TRUE** at `:619-620` vs `:637-638`. Minor.

**F29 -- "0x70 ... a value inside BOTH enables" is false.** 0x70 & ~0x30 = 0x40 and 0x70 & ~0xc0 = 0x30, so it only overlaps each enable.
* **Raised by:** codex.
* **Status:** **CHECKED-TRUE** at `:663`.

**F30 -- The device comment's "no state changes" is literally false: the latch is state.** "No device-register state changes" is the accurate form.
* **Raised by:** codex, deepseek, grok ("pedantic").
* **Status:** CHECKED-TRUE. Cosmetic.

**F31 -- Two md5s for "the diff".** PRETABLE `:100` says "regenerated ... md5 14665812"; the brief §3 says 600f9c4b.
* **Raised by:** agy ("stale intermediate"), kimi ("does not reproduce"), glm, kimi-sub.
* **Status:** **CHECKED:** `diff545_6files.patch` has md5 600f9c4b...; 14665812 matches no file present.

**F32 -- PRETABLE says "Rows whose channel cannot vary under any listed mutant: SC1/SA1".** HEAD and M1 redden both.
* **Raised by:** codex, glm.
* **Status:** **CHECKED-TRUE** (TABLE2 rows in the brief).

**F33 -- PRETABLE's M6 channel reads "irq_status preserved 0x70 != 0x10".** The preservation pin is the seed 0x18.
* **Raised by:** kimi.
* **Status:** **CHECKED-TRUE** (`P_STATE_OK`, `:640`).

**F34 -- The brief's "patched files ... byte-identical to what the table measured" is no longer true.** The working tree now differs in `diff_footbridge.c` (X-rows) and `footbridge_sites_probe.py` (header). **`gate_arm.sh` also carries an E0-E6 distinct-id pin change that is NOT in the reviewed `d_gate_arm.sh.patch`.**
* **Raised by:** kimi, codex.
* **Status:** **CHECKED-TRUE** (`git diff HEAD -- regress/gate_arm.sh` shows the `^E[0-6] .*ok$ | cut | sort -u` line; the frozen patch has only the N-row `sort -u`). The X and header parts are the post-pass-2 changes. The E-row change needs its own record.

**F35 -- The brief cites "Figure 7-2 :6814" as datasheet support for a declined read returning 0.** `:6814` is diagram labels; the zero-read sentence is `:1650-1652`.
* **Raised by:** grok.
* **Status:** **CHECKED-TRUE.** The wrong attribution is in the brief/round prose, not in code.

**F36 -- The gate's display grep still names `K1` and does not echo the H, S or N rows.**
* **Raised by:** grok.
* **Status:** **CHECKED-TRUE** at `gate_arm.sh:1074`. Cosmetic.

**F37 -- The sites `send()` comment says hygiene pins a literal form ending `None)`.** `gate_hygiene.sh:553` accepts `[,)]`, so the trailing-argument form is also recognised.
* **Raised by:** codex.
* **Status:** **CHECKED-TRUE** at `:309-313` vs `gate_hygiene.sh:553`. Minor.

**F38 -- The table's "21/36 FAIL" reads as 21 failures.** 21 is the pass count; there are 15 reds.
* **Raised by:** kimi.
* **Status:** Borderline. CHECKED against `sites_FIX.log`'s `ROWS=` format.

**F39 -- M9's red of N1 depends on the misnamed text copying IRQ_STATUS's text verbatim.** The channel table should say so.
* **Raised by:** kimi-sub.
* **Status:** NOT CHECKED. Minor.

**F40 -- PRETABLE was amended after table 1, so its mtime cannot prove that every sentence preceded table 1.**
* **Raised by:** codex.
* **Status:** NOT CHECKED.

### Design dissents

**F41 -- H1/H2 do not reproduce the former control's device-initiated, mid-session exit-1 channel.**
* **Raised by:** codex, kimi-sub.
* **Their argument:** kimi-sub notes that the +0x100/+0x104 SDRAM reads still `exit(1)` and could have carried a product-death control.
* **Counter-view:** glm, grok and agy call the legs adequate; the HEAD and M1 runs already show the death channel fires.
* **Category:** DESIGN-DISSENT.

**F42 -- The `send()` fix makes the existing `send("reg", timeout=30)` actually enforce 30 s.** Before, it used `wait()`'s 60 s default.
* **Raised by:** glm.
* **Risk:** a new flake on a slow host.
* **Category:** DESIGN-DISSENT / risk note. CHECKED: the `wait` default is 60 (`:314`).

**F43 -- The H1 gate text pin counts the probe's own echo line, not the child's bytes.** It fails closed, but it is one step removed from the child.
* **Raised by:** glm, kimi-sub.
* **Category:** DESIGN-DISSENT (note). NOT CHECKED.

### Out-of-scope finds

**F44 -- §7.3.30 says IRQRawStatus and FIQRawStatus "always contain identical data".** The model keeps separate fields, and the 0x18/0x50 seeds violate that invariant. The seeds are legitimate as synthetic inputs but prove no hardware fidelity.
* **Raised by:** codex.
* **Status:** **CHECKED-TRUE** (`dc21285.txt:6903`).

**F45 -- `gate_arm.sh:1123` omits `tr -d ' '` after `wc -l`.**
* **Raised by:** agy.
* **Status:** CHECKED-FALSE as a live defect: GNU `wc -l` on stdin in WSL prints no padding. BSD portability only.

**F46 -- The differential's `@@SELFCHECK@@` lines match `^  FAIL ` on every run.** A driver must exclude them.
* **Raised by:** Opus.
* **Status:** Harmless; the round's driver already excludes them.

**F47 -- Arm S loads into `sp` and `lr`.** That is safe in bare stepped code but fragile.
* **Raised by:** kimi-sub.
* **Status:** NOT CHECKED.

**F48 -- `count=1.*ok$` would prefix-match `count=10`.**
* **Raised by:** glm.
* **Status:** Unreachable here: the maximum is 2.

### Seat concerns refuted by checking

**F49 -- `H["status"] == "NO-PROMPT"`'s assignment is "not visible".**
* **Raised by:** minimax.
* **Status:** CHECKED-FALSE: it is at sites `:344`.

**F50 -- "the DEVINIT memset half of the struct comment is pinned by no row".**
* **Raised by:** minimax.
* **Status:** CHECKED-FALSE: N1-N5 `count=1` on a real DEVINIT'd instance requires zeroed latches.

**Counts:**
* DEFECT-IN-DIFF: 0
* ALREADY-ADDRESSED: 6 (F1, F2, F3, F18, F19, F20)
* DETECTOR-GAP, open: 14 (F4-F17)
* WRONG-RECORD, open: 20 (F21-F40)
* DESIGN-DISSENT: 3 (F41-F43)
* OUT-OF-SCOPE-FIND: 5 (F44-F48)
* Refuted: 2 (F49, F50)

## 3. Disagreements

**D1 -- Was the width/latch family an L2 floor breach?**
* **Opus:** "FLOOR BREACH (L2), MEASURED ... `if (X)` -> `if (X && len == 4)` on the predicate the fix ADDED is the canonical clause-(d) form."
* **codex:** "L2 dependency-closure breach."
* **glm:** "Clause (d) of the floor is breached on these three ... this is L2."
* **minimax:** "(L2-class) Lenguard mutant is closed on IRQ_STATUS only."
* **grok:** "`&& len == 4` is not a floor cell ... No L2 ... It is the #499 shape as construction debt ... L1 ... or clause (e)."
* **kimi-sub:** "No L2 breach ... the closure is complete for every predicate that exists in the diff; the two under-closures are insertion-class."
* **deepseek:** "No L2 breach."
* **agy:** "(d) PASS."
* **kimi:** "(e) breach, L2-grade but already repaired in the tree" (about the header), and treats width as the Q2 hole.

**D2 -- Is a latch re-armed by a legal read inside the (d) enumeration?**
* **Opus:** "Grade: arguable. A new writer in a sibling case is not obviously inside the diff-closed (d) enumeration. B1 is inside the edited case's own read branch, so it is the strongest L2 candidate."
* **grok:** "Same for a legal-path latch clearer (new writer, not a dominating predicate of the diff). No L2."
* **glm:** counts it among the three (d) survivors.

**D3 -- Is a latch re-armed by a sibling read caught at all?**
* **minimax:** "Caught for these specific pairs."
* **deepseek:** "(d) ... No closure gap found."
* **kimi:** "caught in the frozen set ... caught only for the five siblings actually read. A clear keyed on any other legal register ... is green everywhere."
* **Opus (MEASURED):** B1, B2 and B3 are "ESCAPED" 36/36 and 111/111.
* **grok and glm:** the own-register read escapes; the crosswise sibling read is caught.
* **Resolution:** every seat is right about the pairing it walked. Opus measured escapes in the pairings arm S does not schedule.

**D4 -- Do the seeds close operand swaps?**
* **codex:** "**`F&E=10` survives** ... **`I&F=10` survives**."
* **glm:** "survives because the chosen seeds coincide: 0x50 & 0x30 = 0x10 = 0x18 & 0x30."
* **kimi-sub:** "all four seeds distinct ... so any cross-field or cross-family substitution reds P0/P7."
* **agy:** "swap IRQ with FIQ status caught by P0."
* **deepseek:** "P0's seeds ... are chosen so a swap is observable in both halves."
* **Resolution:** CHECKED by arithmetic that codex and glm are right. The others tested only the whole-expression swaps.

**D5 -- Floor clause (b) at every site.**
* **codex:** "supported by control flow, incompletely measured ... four isolated reinstatement measurements remain owed."
* **kimi:** "holds structurally ... the symmetry argument is airtight here."
* **grok:** "the detector fails them by construction even though only one build ran. Not L2."
* **kimi-sub:** "HEAD *is* the five-site reinstatement."

**D6 -- Do H1/H2 replace what arm K established?**
* **codex:** "They do not reproduce the former control's device-triggered, mid-session exit-1 channel."
* **kimi-sub:** "the direct product-death control was retired when it needn't have been."
* **glm:** "No green-build row exercises a device death, but on the fixed build there is none left to exercise. Acceptable."
* **agy:** "H1 and H2 establish this cleanly."
* **grok:** "They replace failability, not the old K1 fact. The header is honest about that."

**D7 -- Duplicate-line gate pins.**
* **codex:** "Accepted by several pins ... a gate-check weakness."
* **kimi:** "real gap."
* **kimi-sub:** "REAL for two pins."
* **grok:** "Harmless while `FOOTBRIDGE_SITES_PASS` exists."
* **minimax:** "Caught" (it considered only the N pins).
* **glm:** "closed iff the gate also pins the probe's aggregate PASS token -- NOT CHECKABLE."
* **Resolution:** CHECKED: the PASS token is pinned at `:1086`.

**D8 -- Which md5 is stale?**
* **agy:** "`14665812` ... is a stale intermediate record from Table 1."
* **glm and kimi-sub:** the inlined diff contains the I1 fix, so it is the regenerated one. "if 600f9c4b is the pre-fix concatenation its label in §3 is stale."
* **Resolution:** CHECKED: 600f9c4b is the current `diff545_6files.patch`, which contains `QL`, so agy's reading is right.

**D9 -- Datasheet support for the zero-read policy.**
* **brief and agy:** `:1652` plus "Figure 7-2 :6814".
* **grok:** "`:6814` is the interrupt-source diagram. Zeros for a nonexistent CSR are `:1652`."
* **Resolution:** CHECKED: grok is right.

**D10 -- Is "no state changes" a wrong record?**
* **codex:** "FALSE literally; TRUE for architectural device state."
* **deepseek:** it "should read 'no register state changes'."
* **grok:** "Pedantic, not false."
* **agy, glm and kimi:** "NONE beyond the latch" / "only its own latch", i.e. not raised as a record defect.
