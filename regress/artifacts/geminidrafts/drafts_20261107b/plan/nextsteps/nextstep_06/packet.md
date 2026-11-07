# Reading task: nextstep_06 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT06-db5d` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `m88kwtbit` -- state `open`, severity `MED`

**title:** cpus/cpu_m88k_instr.c ld/st register form -- the .wt bit (bit 7) halts ("wt bit not yet implemented") -- CPU-STOP

**state_note:** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T127 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A7-31).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/cpu_m88k_instr.c:3606-3614.  Portable fix: UNVERIFIED -- port ajfa mvme187 4a01173 patch 01 (treating .wt as a cache hint is the recipe's claim, not the manual's).  Filing check (TRIAGE.md): 0 hits.  Port confidence UNVERIFIED (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): legal MC88100 `.wt` semantics are not established and the recipe is not an authority; do not port `.wt`-as-a-hint (F).  witness: none -- research finding, not yet reproduced here.  [2026-11-02, records] The title's 'ld/st register form' is narrower than the guard: the wt test at cpu_m88k_instr.c:3611-3614 runs before the ld/st (:3620), lda (:3639) and xmem (:3653) arms of the register form, so the same halt reaches lda and xmem (987cb596, unchanged since de8c7547).

**hold_question:** (none)

### ROW `mipspagemaskdead` -- state `open`, severity `LOW`

**title:** src/cpus/memory_mips_v2p.c:293: `case 0x00007ff:` in the R4100 page-mask switch is unreachable -- a nonzero stored mask under PAGEMASK_MASK_R4100 (0x7f800) cannot OR back down to 0x7ff; the live 1 KB path is the `pmask == 0` arm at :282-289

**state_note:** filed 2026-10-22 from Grok 4.7's critical-items design adjudication (regress/artifacts/research_20261022/crit_20261022/grok_crit.txt, Q5): dead code, no behaviour change; hygiene.  Goes with the VR41xx 1 KB-page round (the T11 row of the research filing), which edits that function and should delete or justify the arm rather than leave a case that reads as the 1 KB path.

**hold_question:** (none)

### ROW `i8259ocw3revert` -- state `open`, severity `LOW`

**title:** devices/dev_8259.c -- the one-shot poll read (#574) reverts current_command to the IRR (0x0a); the chip remembers the LAST RR/RIS selection and the datasheet qualifies that memory for polling -- DOCUMENTED (approximation)

**state_note:** Filed 2026-10-25 by #574 (GLM, F2b; Astra: the datasheet paragraph at _scratchpad/i8259/8259A.txt:649 qualifies polling).  No documented guest observes it: NetBSD re-selects 0x0c before every poll and its last selection is the IRR; Linux/malta never writes 0x0c and its spurious path restores 0x0a itself.  A remembered byte (last_rr) is a product addition the addition licence refuses on 'cannot hurt'.  F2d (D8): the IRR-selected-prior case is pinned by `poll once2`; the ISR-selected-prior case (OCW3 0x0b, a poll, a bare read: the model answers IRR, a remembered-selection implementation ISR) is the row owed with any implementation, in the probe's port-I/O shape.

**hold_question:** (none)

### ROW `i8259smm` -- state `open`, severity `LOW`

**title:** devices/dev_8259.c -- OCW3 0x68 (set special mask mode) is an empty TODO arm; NetBSD/malta writes 0x68 at attach and never clears it, and #574's acknowledge selects from irr & ~ier regardless -- DOCUMENTED

**state_note:** Filed 2026-10-25 by #574 (GLM, F2b Q3.3).  Special mask mode concerns service-based priority inhibition, which this model does not have (i8259priority); with no ISR inhibition the set of delivered lines is unchanged by SMM, so NetBSD's delivered set is the same with or without it.  Impact otherwise NOT CHECKED (the 0x68 arm and the datasheet's SMM semantics).

**hold_question:** (none)

### ROW `lecsr3inert` -- state `open`, severity `LOW`

**title:** devices/dev_le.c -- the three implemented CSR3 bits (BSWP, ACON, BCON) are stored and never consulted by the model -- DOCUMENTED

**state_note:** Filed 2026-10-25 by #573 (GLM, F2 pass): `grep -n 'reg\[3\]' src/devices/dev_le.c` matches nothing; BSWP governs DMA byte lanes the model does not emulate (is_bigendian drives its SRAM byte order instead).  #573 pins the read-back only.

**hold_question:** (none)

### ROW `pit8253pendingptr` -- state `open`, severity `MED`

**title:** devices/bus_isa.c + devices/dev_v3.c -- the 8253's pending-event count pointer is snapshotted before DEVINIT(8253) publishes it, so the IRQ-0 decrement in isa_interrupt_deassert() is dead code on every machine; dev_8253.c itself never deasserts and never resets the count -- WRONG-RESULT (the rate; #574 retires the event at the acknowledge instead)

**state_note:** Filed 2026-10-25 by #574 (found by Astra and Grok on pass 1, CHECKED): bus_isa.c copies machine->isa_pic_data.pending_timer_interrupts right after the 8259's device_add and before the 8253's; dev_8253.c's DEVINIT stores the pointer afterwards; machine_new zero-fills.  #574's acknowledge reads the machine field at call time, so no live code depends on the stale copy; the dead decrement is left in place and recorded here.  Also: the count is a plain int incremented from the SIGALRM callback and decremented in mainline (the house idiom, mc146818/gt/jazz do the same; mc146818's is volatile).

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_06: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT06: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
