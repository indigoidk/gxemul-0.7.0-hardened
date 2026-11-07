# Reading task: closedraft_12 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE12-d42a` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `i8259priority` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_8259.c -- the in-service register does not inhibit equal- or lower-priority requests (the CPU line is irr & ~ier, never & ~isr); no nested-priority logic -- DOCUMENTED

**state_note (head):** Filed 2026-10-25 by #574 (Astra, F2 Q3.4): once ISR is live (after #574) a second request can be delivered while a lower-numbered line is in service; neither documented guest depends on the inhibition (both mask in the handler).  Priority rotation (OCW2 R bit) is likewise unimplemented (i8259ocw2nonspec).

**hold_question:** (none)

**the triage pass's reason:** Missing priority inhibition does not impact known guests as they mask in handlers.

### ROW `i8259smm` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_8259.c -- OCW3 0x68 (set special mask mode) is an empty TODO arm; NetBSD/malta writes 0x68 at attach and never clears it, and #574's acknowledge selects from irr & ~ier regardless -- DOCUMENTED

**state_note (head):** Filed 2026-10-25 by #574 (GLM, F2b Q3.3).  Special mask mode concerns service-based priority inhibition, which this model does not have (i8259priority); with no ISR inhibition the set of delivered lines is unchanged by SMM, so NetBSD's delivered set is the same with or without it.  Impact otherwise NOT CHECKED (the 0x68 arm and the datasheet's SMM semantics).

**hold_question:** (none)

**the triage pass's reason:** SMM absence is functionally benign since ISR inhibition is already absent.

### ROW `lecsr12readback` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_le.c:le_register_write -- CSR1 bit 0 and CSR2 bits 15:8 are stored as written; their read-back is unspecified by the Am7990 manual, read-as-zero on the C-LANCE for CSR2 only -- DOCUMENTED (a per-chip model flag is the port if a C-LANCE instance is ever added)

**state_note (head):** Filed 2026-10-25 by #573 (the narrowing of `lecsrmask`): TM1986.txt 1749 'Must be zero.' / 1695 'Reserved.' (no read-back statement); am79c90_bitsavers.txt 1161-1163 (CSR2 read as zeroes) / 1138-1142 (CSR1 bit 0 'Must be zero.' only); MAME am79c90.cpp stores CSR1 whole on both chips and CSR2 whole on the Am7990 ('MIPS RS2030 diagnostic requires these bits to be writable'); rpajarola e108b54 masks all three for a 3MIN port this fork lacks.  The chip of the KN230, PMAD-AA and luna88k instances is unverified (the KN01 is the Am7990).  #573's contract rows pin the stored-whole behaviour; a per-chip change re-pins them under the oracle-correction order.

**hold_question:** (none)

**the triage pass's reason:** The read-back behavior is pinned by contract rows and documented.

### ROW `lecsr3inert` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/dev_le.c -- the three implemented CSR3 bits (BSWP, ACON, BCON) are stored and never consulted by the model -- DOCUMENTED

**state_note (head):** Filed 2026-10-25 by #573 (GLM, F2 pass): `grep -n 'reg\[3\]' src/devices/dev_le.c` matches nothing; BSWP governs DMA byte lanes the model does not emulate (is_bigendian drives its SRAM byte order instead).  #573 pins the read-back only.

**hold_question:** (none)

**the triage pass's reason:** Stored CSR3 bits are unconsulted because the model does not emulate DMA byte lanes.

### ROW `pit8253pendingptr` -- state `open`, severity `MED`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** devices/bus_isa.c + devices/dev_v3.c -- the 8253's pending-event count pointer is snapshotted before DEVINIT(8253) publishes it, so the IRQ-0 decrement in isa_interrupt_deassert() is dead code on every machine; dev_8253.c itself never deasserts and never resets the count -- WRONG-RESULT (the rate; #574 retires the event at the acknowledge instead)

**state_note (head):** Filed 2026-10-25 by #574 (found by Astra and Grok on pass 1, CHECKED): bus_isa.c copies machine->isa_pic_data.pending_timer_interrupts right after the 8259's device_add and before the 8253's; dev_8253.c's DEVINIT stores the pointer afterwards; machine_new zero-fills.  #574's acknowledge reads the machine field at call time, so no live code depends on the stale copy; the dead decrement is left in place and recorded here.  Also: the count is a plain int incremented from the SIGALRM callback and decremented in mainline (the house idiom, mc146818/gt/jazz do the same; mc146818's is volatile).

**hold_question:** (none)

**the triage pass's reason:** no live code depends on the stale copy

### ROW `lancetxtempty` -- state `open`, severity `LOW`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** _scratchpad/lance -- Am7990_ds.txt (3,015 bytes, one scanner watermark line per page) and am7990_ardent.txt (58 bytes, form feeds only) carry no datasheet text, so a grep of either reports nothing for everything and an Am7990 datasheet absence cannot be claimed from them -- RECORD (the primary-sources caution, not product code)

**state_note (head):** 

**hold_question:** (none)

**the triage pass's reason:** explicitly recognized as a documentation/carrier note rather than a bug in product code.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_12: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE12: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
