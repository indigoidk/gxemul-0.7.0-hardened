# FABLE_ADJ_B2_20260905 -- Fable 5.1 adjudication of retrospective batch 2 (m88k: d12114d #323, ed242c0 #380).
# Preserved VERBATIM by the main loop from the Agent seat's final message (the harness blocks seat file writes).
# Brief: brief_fable_adj_batch2.md; Astra's answer: codex.txt.  Agent run: 53 tool uses, ~25 min, 307,761 tokens.

FABLE_ADJ_B2_20260905

First line of codex.txt, verbatim:
`d12114d (#323): **RECORD** — mask repair is correct; stale legality claims remain, and the detector covers only part of the repaired domain.`

---

## VERDICT LINE (per commit, then batch)

- **d12114d (#323 bcnd): RECORD.** The mask decode is correct at HEAD — I re-enumerated all 32 field values against the manual and the generator and they agree; the detector is above the vacuity floor. One marginal L4 (a generator comment) + one filed coverage-debt row (mask 6). Fix HOLDS; record needs one correction.
- **ed242c0 (#380 idle fold): fix HOLDS; RECORD (three record errors) + the review SURFACES a live, PRE-EXISTING DEFECT.** The slot-dispatch repair is correct and its detector is above the floor. But the round's records carry three wrong statements, and checking #380's fallback exposed a pre-existing exception-core halt that stops every guest CPU.
- **BATCH: DEFECT.** The live defect is the m88k exception-core fallback (`cpu_m88k.c`, anchor `vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented`): six guest-reachable exception classes stop the machine instead of being delivered. It is upstream code neither #323 nor #380 introduced. A measuring seat should build a rung-3 probe (below) and, when fixing, the deliver-through-common-path form.

Astra's three verdicts are essentially right; its SCOPE on the defect is too narrow (Q1) and its XIP_E finding is correct and important (Q2).

---

## Q1 — THE DEFECT (privilege/unimplemented-vector fallback)

**Astra's finding is right and its scope is too narrow.** The fallback at `cpu_m88k.c` anchor `if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented)` prints `unimplemented vector=0x%03x` and does `for (j..ncpus) cpus[j]->running = false; return;` — for EVERY vector < 128 that the switch did not mark `implemented = true`. Only RESET/INTERRUPT/INSTRUCTION_ACCESS/DATA_ACCESS set it true; the other nine switch cases print a `VERBOSITY_ERROR` and `break`. Confirmed by reading, and `git log -L775,784:src/cpus/cpu_m88k.c` returns only `39748e3 Import GXemul 0.7.0 (unmodified upstream baseline)` — **pre-existing upstream; the fork never touched it.** Astra scoped this to the tb1 privilege path; the real class is much broader.

**Reachability per class, read from the raise sites (deriver reproduced: 77 sites):**

| class | vec | sites | reachable by a guest? |
|---|---|---|---|
| ILLEGAL_INTEGER_DIVIDE | 8 | 4 | **YES, trivially** — `divu`/`div` by zero, supervisor OR user (`cpu_m88k_instr.c` anchors `X(divu)`, `X(div)`; guard is `reg(ic->arg[2]) == 0`, mode-independent). Manual 6.8.3 (`mc88100.txt:10302`). |
| INTEGER_OVERFLOW | 9 | 3 | **YES** — signed `add`/`sub` overflow (`X(add)`, `X(sub_imm)`; guard `d != dx`), mode-independent. Manual 6.6 (`:9305`). |
| PRIVILEGE_VIOLATION | 6 | 10 | **YES** — `ldcr`/`stcr`/`xcr`/`rte`/`ld.usr`/`st.usr`/`tb0`/`tb1`/`tcnd` in user mode. Manual 6.5.4 (`:9257-9264`), and tb1 "whether or not the trap condition is met" (`:6195`). |
| SFU1_PRECISE | 114 | 58 | **YES** — any FP/mul/div with SFD1 set (FPU disabled), OR FP divide-by-zero regardless of SFD1 (`X(fdiv_sss)` sets FPECR=FDVZ then raises). Manual 6.8.4 (`:10316`). |
| MISALIGNED_ACCESS | 4 | 1 | **YES** — misaligned load/store (`cpu_m88k_instr_loadstore.c` anchor `M88K_EXCEPTION_MISALIGNED_ACCESS`). Manual 6.5.2 (`:9231`). |
| UNIMPLEMENTED_OPCODE | 5 | 1 | narrow — `prom_call` in user mode (`X(prom_call)`). |
| BOUNDS_CHECK / SFU1_IMPRECISE / ERROR | 7/115/10 | **0 / 0 / 0** | **latent** — no raise site today (tbnd is disassembler-only; ERROR is only an internal reassignment at anchor `SFRZ already set in PSR => ERROR`). |

So the main loop's framing "**nine vectors (77 raise sites)**" is imprecise: the 77 sites belong to **six** reachable classes; the other three switch cases have no raise site. Correct the count to "nine switch cases halt, six reachable via a raise site today (77 sites)."

**Consequence (measurable):** a guest user program executing one `divu rX,rY,r0` stops the whole emulated machine. When all CPUs stop, `emul.c` (anchor `any_machine_still_running`) `break`s the main loop on a normal boot (no breakpoints → `debugger_enter_at_end_of_run` false), so the process exits cleanly ("All machines stopped") rather than aborting — a **graceful guest-drivable machine halt**, not a host memory-safety abort. Real hardware delivers VBR+8·vector (offsets verified: PRIVILEGE→0x30, ILLEGAL_DIVIDE→0x40, OVERFLOW→0x48, MISALIGNED→0x20, all matching Table 6-1 `mc88100.txt:8524-8538`) and OpenBSD turns it into a signal.

**(a) Queue id + severity:** `m88kexcdeliver`, **HIGH**. Guest-drivable termination of the machine from unprivileged code, and an emulation-correctness hole (a legitimate userland fault gets a dead VM instead of a signal). Rank it at the **top of the live-defect tier** of the OPEN LIST — above the records/coverage items (staticlatchscope, exit0oracle, etc.) and alongside the guest-drivable-halt device rows (pcc2widthkills, lcabadval), with the honest nuance that this is a *graceful* stop where those are `exit(1)` aborts, so just below the abort class.

**(b) Witness (rung 3):** a cold-debugger probe on committed `testm88k` or `luna-88k`, exemplars `regress/m88k_idle_probe.py` / `m88k_rounding_probe.py`. Cleanest: a **supervisor-mode divide-by-zero** (no mode switch needed) — plant `divu r2,r3,r0`, point VBR into RAM, breakpoint at VBR+0x40, free-run. Pre-fix HEAD: `unimplemented vector=0x008` and the machine stops. Post-fix: PC == VBR+0x40, SXIP = the faulting instruction | XIP_V, PSR shadow frozen (SFRZ/IND/SFD1/MODE set), machine still running. Add the two controls the ladder requires: a LIVENESS control (a delivered vector that already works, e.g. an INTERRUPT or a returning path) and an ATTRIBUTION control (the same instruction on a non-faulting operand does not vector).

**(c) Option set:** this is NOT a device de-fatalisation (delete/decline/announce/accept/fault) — these are architected CPU exceptions the guest OS has handlers for, so **the only correct disposition is DELIVER**; declining would suppress a real signal. The common path after anchor `Stuff common for all exceptions` already does SFRZ, EPSR save, the shadow SXIP/SNIP/SFIP, supervisor switch, and `cpu->pc = VBR + 8*vector`. Per vector the additional need:
- Trap-like five (PRIVILEGE, ILLEGAL_DIVIDE, INTEGER_OVERFLOW, UNIMPLEMENTED_OPCODE, MISALIGNED): **nothing but `implemented = true`** — flow through the common path. SXIP already points at the faulting instruction; destination register left unchanged (raise precedes the write); MISALIGNED already populates DMT in the load/store template.
- SFU1_PRECISE/IMPRECISE: FPECR is already set at the raise site, but the manual's FP exception registers **FPHS1/FPLS1/FPHS2/FPLS2/FPPT/FPRH/FPRL/FPIT** (Fig 6-1 `mc88100.txt:8486-8514`, §6.8.1) are **never written by the fork** (`grep -c 'FPHS1\|FPLS1\|FPPT' = 0`); faithful SFU1 delivery needs them (though the common FPU-disabled case, §6.8.4.1 `:10324`, uses EPSR.SFD1 and does not need FPECR).

**SPLIT: yes.** The trap-like five share one fix design and one detector shape → one round `m88kexcdeliver` (HIGH). SFU1 needs FP-register modelling and is a different semantic class → separate `m88kexcsfu1` (MEDIUM). This also honours the round-scope rule (one fix design per round). The fork has already made this exact "deliver instead of halt" fix three times at the decoder layer (#302/#314/#323, CHANGELOG anchor `the fix is the one this fork has already made three times`); this is the same class one layer up, in the exception core.

**Do not attribute it to #323 or #380** — the witness/record must say *pre-existing upstream, exposed by the #380 review*.

---

## Q2 — THE RECORD items (each opened and checked)

**(i) generator "These are legal encodings"** — `generate_m88k_bcnd.c` anchor `every other mask value. These are legal encodings`. **RECORD (L4), LOW, but marginal.** The comment covers masks 0,4,6,9,a,b,f (bit-4 clear — genuinely legal encodings without a mnemonic, per manual `:4118` "M5 field may also be indicated explicitly by a literal value") AND 0x10–0x1f (bit-4 set — *tolerated*, not legal: manual `:4156` "bit 25 reserved ... must be zero for future compatibility"). The blanket "legal encodings" is imprecise for the reserved-bit-set half, and the #323 CHANGELOG's own later paragraph (anchor `accepted field values`) already draws the distinction. Correct the generator comment to match. Marginal because it is true of the majority it primarily describes.

**(ii)+(v) XIP_E — Astra is RIGHT, and this is the strongest record finding.** I ran it: `git show -s --format=%B ed242c0 | grep -c XIP_E` = **0** (and `git log -1 --format=%B` = 0). **The #380 commit message contains no XIP_E.** The XIP_E claim lives ONLY in the source comment added by the diff — `cpu_m88k_instr.c` anchor `delay-slot state wrong (delay_slot flag, XIP_E` (`git show --format= ed242c0 | grep XIP_E` returns exactly that one `+` line). Yet #381 says (CHANGELOG anchor `The commit message additionally listed XIP_E`, and ee4b69b message `commit message's XIP_E over-claim ... corrected here since the message is immutable`) that the error was in the *immutable commit message*. So #381 corrected the wrong artifact: it declared a message immutable and "corrected" it in the CHANGELOG, while **the actual false claim sits uncorrected in the mutable source comment at anchor `delay-slot state wrong`**. **RECORD (L4):** (a) fix/remove the XIP_E claim in the source comment (XIP_E filing is unconditional on `delay_slot`, identical old and new); (b) correct the #381 CHANGELOG/message-attribution to point at the source comment, not the commit message.

**(iii) ":2697 test would be dead always"** — source comment anchor `test would be dead always (the #360/#361 fold-shipped-dead shape)`. **RECORD (L4).** #381 softened this in the CHANGELOG (anchor `dead on every first-touch path and unreliable in general`) but the source comment still says "dead always." Correct the source comment to match #381's softened wording.

**(iv) CHANGELOG:21475 "no post-loop witness can see the defect"** — anchor `exactly why no post-loop witness can see the defect`. **RECORD (L4), LOW — weakest of the five; could be DROPPED.** Astra's counter is correct in principle: a matcher-accepted slot that WRITES THE POLLED WORD makes loop-exit itself distinguish buggy from fixed — and the round's own OUTSTANDING residual already says exactly this (anchor `one that WRITES THE POLLED WORD (arm 3 is the first arm whose elided instruction can`). So the absolute is inconsistent with the round's own records. But the sentence is scoped by its next clause to the shipped idempotent `or r2,rX,imm` slot, where it is true. Fix is a one-clause qualifier ("for the shipped idempotent slot"). I lean RECORD-LOW; the main loop may reasonably DROP it as true-in-context.

---

## Q3 — DETECTOR RESIDUALS (vacuity floor)

Both are **coverage debt, FILE LOW — neither is a floor breach.** Both shipped detectors clear the floor: they fail on pre-fix HEAD (clause a), fail on a verbatim reinstatement of the removed defect at the tested sites (clause b — bcnd rows for masks 0/4/f red when the table returns to NULL; the #380 taken row reds when arm 3 reverts to the plain handler), and carry independent-PC rows, not self-round-trips.

- **`|| m5 == 6` survivor** (source-predicted): adding it to the generator's NULL-emission returns mask 6 to `goto bad`; no gate row uses mask 6 ({0,1,2,4,c,f} only, anchor `BCND_ROWS = [`), so all seven stay green. The `bcnd_m06` handler is correct (`tmp_m88k_bcnd.c` anchor `X(bcnd_m06)` = Z|N). This is a missing row, not a nulled repair or reinstated defect → **coverage debt**, id `m88kbcndm6`, LOW.
- **duplicated `ic[3].f(cpu, &ic[3]);`** survivor: `slot_runs++` is not duplicated, so `slot == ntn` still holds and the idempotent witness store is unchanged → escapes. This is the exactly-once property, which no predicate the fix *depends on* encodes (clause d enumerates dominating predicates: `v==0`, `EXCEPTION_IN_DELAY_SLOT`, the fallback, the entry guard — none is this), so **not a clause-(d) breach**. #381 already added `slot == ntn && ntp == 0` (gate anchor `idle counters: arm3 fired, slot==ntn, ntp=0, guard quiet`), which catches the counter-doubling variant; the no-counter-double variant remains uncovered → **coverage debt**, id `m88kidledup`, LOW.

Both rank BELOW all live defects (i.e. below `m88kexcdeliver`/`m88kexcsfu1` and the OPEN-LIST device halts).

---

## Q4 — UNVERIFIED MEASUREMENTS

**Rule: LEAVE all four unaltered and unannotated in the shipped records; record the finding in this adjudication only. DROP the "annotate" proposal.** The score-claim-names-its-artifact rule is FORWARD-ONLY and explicitly "audits NOTHING retroactively"; #323 (2026-08-01) and #380/#381 (2026-08-12) both predate its adoption (2026-08-23). The carrier's measured position is "no stale count has ever changed a decision," and legacy counts stay under the read-side rule (re-derive before leaning; FILE only if *decayed*). None of these is leaned on for a decision, and none is decayed — they are unreproducible-in-a-read-only-workspace, which is different. Blanket annotation IS the retroactive sweep the rule declines. Detail:
- **"1.9 million comparisons" (#323):** artifact gone (no `panel_20260801_*` dir on disk), but its conclusion — old and new bcnd masks agree — I **independently re-derived by full enumeration** (all 32 values; §Q-below). Conclusion holds; number needs nothing.
- **"6,172 entries" / slot_runs (#380):** window-dependent (the committed battery log shows `M380_COUNTERS=...ntn:6551,slot:6551` — a *different* window). The load-bearing claim is the RATIO `slot == ntn` (exactly-once), which the gate pins live. The absolute 6172 is illustrative.
- **"129.7-second boot" (#380):** a one-off gate-saga timing, not a pinned oracle.
- **"eight historical halts" (#323):** no pre-fix binary to re-run, but mechanically sound — the pre-fix table had those masks NULL and the decoder does `if (ic->f == NULL) goto bad` (anchor `ic->f = m88k_bcnd[d + 32 * (op26 & 1)]`).

---

## Q5 — THE BRIEF DEFECT

**Confirmed: a campaign records/brief-authoring defect, and NO batch-2 answer content was distorted.** The batch-2 brief's Q1 parenthetical "(the twenty-four encodings; the FPSCR bit positions; the straddle split)" (`brief_retro_batch2.md` anchor `twenty-four encodings`) is copied verbatim from the **batch-1 PPC** brief (`brief_retro_batch1.md` anchor `twenty-four encodings`, where it is correct — 24 PPC FP encodings, FPSCR, the `mrwstore2` straddling store). It describes neither m88k fix. Astra flagged it explicitly ("does not describe either shipped fix") and enumerated the CORRECT domain instead (the 32 bcnd masks; the idle matcher's 1,021-position / 384-vector domains). The brief's own premise-audit opener ("ENUMERATE THE RIGHT DOMAIN — ask what the PRODUCER can emit") did its job. Record it as a brief defect of the main loop's; no correction to code or CHANGELOG.

*(Enumeration confirming the fix, since Q4 leans on it: generator `print_condition` gives `m5&1`=>0, `m5&2`===0, `m5&4`=<0 excl 0x80000000, `m5&8`===0x80000000, bit 4 ignored. Manual `:4160-4166` assigns field bits 21/22/23/24 to gt0/eq0/lt0/maxneg with bit 25 reserved — the identical mapping — and the "sign bit + zero bit concatenated" model (`:4104-4108`) yields the same four classes. All 32 values match Astra's table and the manual. Fix is correct.)*

---

## Q6 — WHICH PROPOSED DISPOSITIONS ARE WRONG

Two of the four:

1. **"ONE new row `m88kexcunimpl`, class-wide (nine vectors)" is wrong twice.** (a) It should be **SPLIT** — trap-like five (one fix: `implemented = true` through the common path) vs SFU1 (needs FP-register modelling). (b) "**nine vectors**" is imprecise — nine switch cases halt, but only **six** are reachable via a raise site today; BOUNDS_CHECK/SFU1_IMPRECISE/ERROR have zero raise sites. Also add: witness must record it as *pre-existing upstream*, and the disposition is DELIVER (not a device-style decline).
2. **"Q4 numbers → annotated, not altered" is wrong.** The forward-only/no-retro-audit rule says **leave them entirely alone** in shipped records; annotation is a mild retro-audit the rule declines. Record the finding in the adjudication, not in the CHANGELOG.

The other two are right: RECORD (i)-(v) → L4 in one records commit (with (iv) marginal/droppable, (i) minor); Q3 residuals → FILED LOW under two ids.

---

## NUMBERED DISPOSITION LIST (file verbatim)

Provenance for all: **Astra batch-2 (codex.txt) + this Fable 5.1 adjudication, 2026-09-05.**

1. **`m88kexcdeliver`** — DEFECT, **HIGH**. *m88k exception core halts every guest CPU for six reachable classes (ILLEGAL_INTEGER_DIVIDE, INTEGER_OVERFLOW, PRIVILEGE_VIOLATION, MISALIGNED_ACCESS, UNIMPLEMENTED_OPCODE — the trap-like five) instead of delivering VBR+8·vector.* Pre-existing upstream (`cpu_m88k.c` anchor `vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented`; `git log -L` → import commit only). Witness: rung-3 probe, supervisor `divu r2,r3,r0`, VBR into RAM, breakpoint at VBR+0x40 — pre-fix `unimplemented vector=0x008` + machine stops; post-fix PC==VBR+0x40, SXIP set, running. Fix: `implemented = true` for the five, flow through common path. Witness owed at rung 3 before any edit.

2. **`m88kexcsfu1`** — DEFECT, **MEDIUM** (split from 1). *SFU1_PRECISE (vec 114, 58 raise sites) and latent SFU1_IMPRECISE halt instead of delivering VBR+0x390/0x398.* Additionally needs the FP exception registers FPHS1/FPLS1/FPHS2/FPLS2/FPPT/FPRH/FPRL/FPIT (never written today) for faithful delivery; the FPU-disabled case needs only EPSR.SFD1. Witness: rung-3 FP-divide-by-zero or FP-with-SFD1-set probe. Rank below 1.

3. **`m88kbcndm6`** — FILE, **LOW** (coverage debt). *bcnd detector has no row for mask 6; `|| m5 == 6` on the generator's NULL predicate returns a conforming encoding to `goto bad` and passes all seven rows (source-predicted, unmeasured).* Above the floor; not a breach. Rank below all live defects.

4. **`m88kidledup`** — FILE, **LOW** (coverage debt). *#380 idle detector cannot prove exactly-once: duplicating `ic[3].f(cpu, &ic[3])` without duplicating `slot_runs++` keeps `slot==ntn` and the idempotent store, so it escapes.* Above the floor; #381's `slot==ntn && ntp==0` already catches the counter-doubling variant. Rank below all live defects.

5. **`m88krec`** — RECORD, **L4** (one records commit). Correct in place: (ii/v) the XIP_E claim in `cpu_m88k_instr.c` anchor `delay-slot state wrong (delay_slot flag, XIP_E` (false — XIP_E filing is unconditional/identical old-new) AND the #381 misattribution of it to the commit message (message has no XIP_E, verified `grep -c` = 0); (iii) `test would be dead always` → #381's softened wording; (i) generator `These are legal encodings` → distinguish legal (bit-4 clear) from tolerated (bit-4 set); (iv, optional/droppable) qualify CHANGELOG `no post-loop witness can see the defect` to the shipped idempotent slot.

6. **`retrobriefppc`** — RECORD (campaign note), **LOW**. *The batch-2 retrospective brief copied batch 1's PPC parenthetical ("twenty-four encodings / FPSCR / straddle"), which describes neither m88k fix.* No answer content distorted (Astra flagged and ignored it). Brief-authoring correction only.

7. **Q4 legacy numbers** — **NO ACTION.** Leave "1.9M comparisons", "6,172", "129.7 s", "eight halts" unaltered and unannotated (forward-only rule; legacy; no decision consumes them; conclusions re-derived by enumeration or gate-pinned). Finding recorded here, not in the CHANGELOG.
