# Reading task: closedraft_11 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE11-cf50` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `dupidcheck` -- state `open`, severity `LOW`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** tools/precommit_check.sh: no section refuses a duplicate ledger row id -- a row filed twice under one id, or a new row given an existing row's id, passes P, W, O, H, K, Q2, I2, I, L and X

**state_note (head):** filed 2026-10-22 from the external-fixes filing's pretest (regress/artifacts/research_20261022/filing_20261022/PRETEST.md, GAPS.md item 2): both duplicate-id controls -- the same new id twice, and a new row carrying an existing id -- left every checker green; only the records drafter's own uniqueness guard refused them.  A duplicate id makes two rows render and resolve as one on the dashboard and in every by-id lookup.  Remedy is a tooling change (an id-uniqueness section, or a check inside check_entry_domain.py / check_row_states.py), which the carrier says ships as its own harness round owing two negative controls: a duplicated id must red, and the 1067 unique ids at HEAD must stay green.

**hold_question:** (none)

**the triage pass's reason:** remedy ships in its own separate harness round with negative controls.

### ROW `m88kwtbit` -- state `open`, severity `MED`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** cpus/cpu_m88k_instr.c ld/st register form -- the .wt bit (bit 7) halts ("wt bit not yet implemented") -- CPU-STOP

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T127 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A7-31).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3606-3614.  Portable fix: UNVERIFIED -- port ajfa mvme187 4a01173 patch 01 (treating .wt as a cache hint is the recipe's claim, not the manual's).  Filing check (TRIAGE.md): 0 hits.  Port confidence UNVERIFIED (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): legal MC88100 `.wt` semantics are not established and the recipe is not an authority; do not port `.wt`-as-a-hint (F).  witness: none -- research finding, not yet reproduced here.  [2026-11-02, records] The title's 'ld/st register form' is narrower than the guard: the wt test at cpu_m88k_instr.c:3611-3614 runs before the ld/st (:3620), lda (:3639) and xmem (:3653) arms of the register form, so the same halt reaches lda and xmem (987cb596, unchanged since de8c7547).

**hold_question:** (none)

**the triage pass's reason:** text explicitly rules 'do not port .wt-as-a-hint'

### ROW `mipspagemaskdead` -- state `open`, severity `LOW`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** src/cpus/memory_mips_v2p.c:293: `case 0x00007ff:` in the R4100 page-mask switch is unreachable -- a nonzero stored mask under PAGEMASK_MASK_R4100 (0x7f800) cannot OR back down to 0x7ff; the live 1 KB path is the `pmask == 0` arm at :282-289

**state_note (head):** filed 2026-10-22 from Grok 4.7's critical-items design adjudication (regress/artifacts/research_20261022/crit_20261022/grok_crit.txt, Q5): dead code, no behaviour change; hygiene.  Goes with the VR41xx 1 KB-page round (the T11 row of the research filing), which edits that function and should delete or justify the arm rather than leave a case that reads as the 1 KB path.

**hold_question:** (none)

**the triage pass's reason:** handle in VR41xx 1 KB-page round (T11)

### ROW `i8259aeoi` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_8259.c -- ICW4's AEOI bit is unsupported while #574's acknowledge always sets the ISR bit: an auto-EOI guest accumulates in-service bits it never clears; the output line never consults ISR, so no interrupt is lost -- DOCUMENTED

**state_note (head):** Filed 2026-10-25 by #574 (Astra, pass 2 Q5; GLM Q34).  Neither documented malta guest programs AEOI (both EOI specifically).  A fix clears the ISR bit at the acknowledge when ICW4 AEOI is set; needs the ICW4 byte kept, which the model does not store.

**hold_question:** (none)

**the triage pass's reason:** The output line doesn't consult ISR so no interrupt is lost.

### ROW `i8259ltim` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_8259.c -- ICW1 bit 3 (LTIM, level-triggered mode) only prints; the model is edge-only after #574 (the acknowledge clears the request bit); NetBSD/malta's ELCR writes (0x4d0/0x4d1) land on nothing -- DOCUMENTED

**state_note (head):** Filed 2026-10-25 by #574 (Grok, F2).  Both documented malta guests program ICW1 0x11 (edge).  A level mode would keep the request bit across the acknowledge while the line is high; the ns16550 and 8253 models re-assert every tick while a condition holds, which approximates it for those sources (the pckbc does not re-assert while already asserted -- F2b, Astra).

**hold_question:** (none)

**the triage pass's reason:** The emulator model is edge-only and documented guests use edge mode.

### ROW `i8259ocw3revert` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_8259.c -- the one-shot poll read (#574) reverts current_command to the IRR (0x0a); the chip remembers the LAST RR/RIS selection and the datasheet qualifies that memory for polling -- DOCUMENTED (approximation)

**state_note (head):** Filed 2026-10-25 by #574 (GLM, F2b; Astra: the datasheet paragraph at _scratchpad/i8259/8259A.txt:649 qualifies polling).  No documented guest observes it: NetBSD re-selects 0x0c before every poll and its last selection is the IRR; Linux/malta never writes 0x0c and its spurious path restores 0x0a itself.  A remembered byte (last_rr) is a product addition the addition licence refuses on 'cannot hurt'.  F2d (D8): the IRR-selected-prior case is pinned by `poll once2`; the ISR-selected-prior case (OCW3 0x0b, a poll, a bare read: the model answers IRR, a remembered-selection implementation ISR) is the row owed with any implementation, in the probe's port-I/O shape.

**hold_question:** (none)

**the triage pass's reason:** The approximation is unobserved by documented guests.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_11: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE11: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
