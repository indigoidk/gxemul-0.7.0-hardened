# i8259eoiirr (#574) -- pass-1 rulings of the main loop (2026-10-25 07:2x), BEFORE the F2 adjudication

These are the main loop's dispositions on the eight pass-1 answers, written to be adjudicated (GPT-6 Astra adjudicates
from the F2 packet; Grok, GLM and DeepSeek re-read it; Argon owed; Fable held).  Every "CHECKED" below names what was
opened or run; nothing here is a seat's word taken on trust.

## 0. The roster record (one line per seat; the launcher log is `../../../..` -> see `cxlaunch_t19p1_stdout.txt`, `grok_t19p1.exit`)

| seat | transport | answer | verdict line |
|---|---|---|---|
| GPT-6 Astra | codex pointer, ultra | `codex_t19p1.txt` 14,742 b | NOT READY -- (A) is the preferred PIC correction but needs a defined PIT lifetime/accounting resolution; detector gaps |
| Grok 4.7 | `--prompt-file`, xhigh, plan mode; read NetBSD + Linux sources itself | `grok_t19p1.txt` 16,951 b | NOT READY -- do not ship (A) as written: it removes the only request-consume this model has |
| GLM 5.3 QA (Q1-2) | packet-fed | `ollama_glm_t19p1_QA.txt` 8,894 b | READY WITH CHANGES -- ship (A); resolve the 8253 floor contradiction first; fix the (d) table |
| GLM 5.3 QB (Q3-4) | packet-fed | `..._QB.txt` 6,639 b | READY WITH CHANGES -- ship (A) alone; file (B) separately; names missing member (F) = (A) + an 8253-side fix |
| GLM 5.3 QC (Q5-6) | packet-fed | `..._QC.txt` 6,096 b | READY WITH CHANGES -- (A) core, but (A) alone breaches the brief's own floor; needs a companion or it is NOT READY |
| DeepSeek QA (Q1-2) | packet-fed | `ollama_deepseek_t19p1_QA.txt` 4,225 b | READY WITH CHANGES -- ship (A); do not close until the PIT path is settled |
| DeepSeek QB (Q3-4) | packet-fed | `..._QB.txt` 1,902 b | NOT READY -- (A) alone fails the floor; ship (C) or (A) + an 8253 clear |
| DeepSeek QC (Q5-6) | packet-fed | `..._QC.txt` 1,525 b | NOT READY -- same 8253 reason; NetBSD's EOI form NOT CHECKABLE from the packet |
| agy / Argon (file-reading) | -- | NOT FIRED | quota wall since 04:24 (reset ~2026-10-30); a wall with a stated reset is a scheduled re-fire |
| Argon web route (packet-fed) | -- | OWED | queued behind T18's single sender; job dir `argon_api/` ready |
| Fable 5.1 | -- | HELD | `FABLE_HOLD_QUESTION.md` (owner hold 2026-10-21) |
| kimi, minimax, Opus seat | -- | DELIBERATELY NOT FIRED | roster (owner 2026-10-23/25); `SEATS_NOT_FIRED_20261025.txt` |

No wall text, no echo, no thinking-burn in any of the eight (tails read; `usage limit|quota|429|filter` grep 0 in each).
Count the arguments, not the seats: the eight answers carry ONE argument on each side, and the side that says "(A)
alone" (GLM QA/QB, DeepSeek QA) also says the 8253 must be settled before it ships -- so the whole panel converges on
"(A)'s EOI semantics are right, and (A) alone is not shippable until the 8253's request has a consumer".

## 1. Facts added by the main loop after the brief went out (all CHECKED; artifacts named)

F-1  **The 8253 crux, MEASURED** (`timer_explore_20261025/RUN_IDENTITY.txt`, two runs each): on the unmodified HEAD
     clone, counter 0 programmed (0x34, count 0x1000 -> a 291 Hz host timer, confirmed by the emulator's own
     `[ 8253: counter 0 set to 4096 (291 Hz) ]`), after ~54M guest instructions IRR bit 0 reads 1; the specific EOI
     0x60 reads it back 0 two instructions later; after another ~54M instructions it reads 1 again; ISR 0x00 at every
     point; the poll byte 0x80.  (The short variant, ~5 ms of guest time, read 0 everywhere: the host timer had not
     fired yet -- not a statement about the model.)
F-2  **The pending-count pointer is captured before it is published** (Astra and Grok, independently; CHECKED
     `bus_isa.c:222-225` vs `:241-244`, `dev_8253.c:383-384`, `dev_v3.c:297-298`): `bus_isa_init` copies
     `machine->isa_pic_data.pending_timer_interrupts` right after the 8259's `device_add` and BEFORE the 8253's;
     `DEVINIT(8253)` stores the pointer afterwards; `machine_new` zero-fills, so the bus copy is NULL on every ISA
     machine and the decrement at `bus_isa.c:133-138` (and `dev_v3.c:143-145`) is dead.  `dev_8253.c`'s count has
     exactly one writer (`++`, :112) and no reset on reprogram (:105/:112/:127/:384 are all its sites).  A ratchet.
F-3  **The malta ISA census, CHECKED** (`machine_evbmips.c:72`: `bus_isa_init(machine, tmpstr, 0, ...)`, flags 0;
     `bus_isa.c:220-310`): the 8259 pair, the 8253, pccmos/mc146818 (irq 8), two ns16550 (irq 4, irq 3), lpt (irq 7, no
     assert), and -- UNCONDITIONALLY, `bus_isa.c:306-310` -- a pckbc on irq 1 (keyboard) and irq 12 (mouse); no fdc, no
     ISA wdc (piix4 IDE comes by PCI with a disk image).  *An earlier draft of this line said "no pckbc on malta"; the
     `dev_pckbc_init` call sits outside every flag test.*  The mc146818 re-asserts every tick while PIE and its count
     > 0 and retires one event per register-C read (`dev_mc146818.c:111/118/562-563`; Astra + Grok) -- the brief's
     "one-shot" label for it was WRONG.  So on the witness machine the EOI's IRR clear costs a tick of latency on the
     re-asserting sources and can lose a request on the one-shot pckbc (`dev_pckbc.c:618-637`: a queued byte after the
     clear does not re-assert while `currently_asserted` stays 1 -- until the queue drains and refills).
F-4  **NetBSD/malta, read at source** (WebFetch `sys/arch/evbmips/malta/pci/pcib.c`, `malta_intr.c`, quoted in
     `../../../../_scratchpad/CHECKPOINT.md` and below): ICW1 = `ICW1_SELECT|ICW1_IC4` (0x11, LTIM clear = EDGE); at
     attach it writes OCW3 `OCW3_SELECT|OCW3_SSMM|OCW3_SMM` (0x68 -- the model's empty "Set Special Mask Mode" arm,
     `dev_8259.c:131-133`, harmless) and `OCW3_SELECT|OCW3_RR` (0x0a); dispatch = POLL the master (0x0c), read the poll
     byte, if 2 poll the slave (+8), run the handlers, then SPECIFIC EOI to the slave (`OCW2_SELECT|OCW2_EOI|OCW2_SL|
     OCW2_ILS(irq&7)`) and then to the master (ILS(2) for a slave line); never 0x20; the IRR/ISR-reading branch is
     `#else`'d out.  `malta_intr.c` calibrates CP0 count from the mc146818 by POLLING its status register and uses no
     PIT at all (no 0x40-0x43 anywhere) -> NetBSD never unmasks ISA irq 0; the 8253 question does not touch it.
F-5  **Linux/malta, read at source** (WebFetch `drivers/irqchip/irq-i8259.c`, `arch/mips/mti-malta/malta-int.c`,
     `malta-time.c`, `arch/mips/kernel/i8253.c`, `arch/mips/Kconfig`): ICW1 0x11 (edge) on both PICs;
     `mask_and_ack_8259A` masks FIRST then writes `0x60+irq` (slave: `0x60+(irq&7)` then `0x60+2`); the spurious path
     reads ISR (0x0B) and restores 0x0A; the vector comes from `mips_pcibios_iack()` = a PCI interrupt-acknowledge
     READ through the system controller (`GT_READ(GT_PCI0_IACK_OFS)` on GT64120) installed by
     `i8259_set_poll(mips_pcibios_iack)` -- it NEVER writes OCW3 0x0c.  **The brief's premise "malta obtains the vector
     with OCW3 0x0c" is true of NetBSD and FALSE of current Linux/malta** (Grok found it; CHECKED).  In the model that
     read is `dev_gt.c:154-157`: `odata = cpu->machine->isa_pic_data.last_int; /* TODO: Actually ack the interrupt? */`.
     **And Linux/malta DOES program the PIT and unmask IRQ 0:** `config MIPS_MALTA` carries `select I8253` and
     `select I8259`; `malta-time.c` calls `setup_pit_timer()` under `CONFIG_I8253` ("Only Malta has a PIT.");
     `setup_pit_timer()` calls `clockevent_i8253_init(true)` then `request_irq(0, timer_interrupt, IRQF_NOBALANCING|
     IRQF_TIMER, "timer", NULL)`, and `timer_interrupt` unconditionally calls the clockevent's `event_handler` and
     returns `IRQ_HANDLED` -- so Linux's own spurious-interrupt guard can never disable line 0.
F-6  **The witness's `poll byte` row ran with line 4 MASKED** (GLM QA raised it; CHECKED `i8259_eoi_probe.py`
     `build_other()`: `e_out(PIC1_IMR, 0x10)` precedes `e_ocw3_read(a3, OCW3_POLL)`), and the model's poll scans raw
     `d->irr` with no `& ~d->ier` (`dev_8259.c:150-157`, and the `default` arm too).  The row's 0x84 therefore pins a
     MASK-BLIND poll as its contract value -- the pin-the-bug shape.  Disposition: re-cut the row (poll BEFORE the
     OCW1 write) before the detector ships (L1, pre-ship construction), and file the mask-blind poll as its own row.
F-7  **The OCW2 arms** (Astra + Grok; CHECKED `dev_8259.c:96-141`): the "specific EOI" arm matches 0x21-0x27 (which
     the datasheet makes NON-specific, SL=0), 0x60-0x67 and 0xe0-0xe7 (rotate-on-specific-EOI; the rotate is not done,
     `priority_reg` is never written); 0x68 and 0xc0-0xc7 are empty TODO arms; EVERY other command byte -- 0xa0-0xa7
     (rotate on non-specific EOI) among them -- reaches `fatal(...unimplemented command...)` and `cpu->running = 0`.
     Separate rows (below); not this round's edit.
F-8  **Provenance**: `dev_8259.c` and `bus_isa.c` have ONE commit each (the upstream import `39748e3c`; `git log
     -L118,130:src/devices/dev_8259.c` agrees); `dev_8253.c` was touched by #439/#440 and the early hardening commits,
     none of them at the tick or the count.  No pristine-upstream copy of these files exists under the project root
     any more (the 10-22 archive); provenance is by `git log`.
F-9  **`dev_v3.c` is the Algor P5064's V3, not the Iyonix's** (Astra + Grok): its handlers are the bus_isa trio
     re-done for Algor (dummy line 16; no `pic2 != NULL` test; `secondary_mask1` routing), and `dev_algor.c`'s
     `P5064_LOCINT`/`P5064_ISAINT` READS clear `pic1->irr &= ~0x18` / `pic2->irr &= ~0xc0` (a read-acknowledge
     outside the PIC).  Accepted on two file-reading seats' concurring readings of the files; own row.
F-10 **Three IACK-shaped readers of `isa_pic_data.last_int` exist** (CHECKED `git grep last_int`): `dev_gt.c:155`
     (malta, Linux's path), `dev_prep.c:57`, `dev_footbridge.c:432`.  `last_int` is written at assert time by
     `isa_interrupt_common` (`bus_isa.c:76-87`: the lowest pending unmasked line, skipping 2).
F-11 **The storm, MEASURED with real interrupt delivery** (added 07:4x, after the F2 packet went out -- it reaches the
     seats in pass 2; `rate_explore_20261025/RUN_IDENTITY.txt`): a guest handler at the MIPS general exception vector
     (BEV cleared) that polls, writes the specific EOI 0x60|n and counts, with only ISA line 0 unmasked and 8253
     counter 0 programmed to 0xffff (18 Hz): **7,415 IRQ 0 deliveries in 180M guest instructions** (last poll byte
     0x80, every word of both binaries disassembler-checked, park pc-verified) -- one per 2^14-instruction tick after
     the first host-timer fire, where the programmed rate implies well under 100.  This is the guest-visible form of the
     8253 half of this row, and the detector's RATE row (a band: HEAD >= 5000, FIX 1..1000; separation of two orders of
     magnitude at any host speed).  **And a count-0 finding on the way**: counter 0 programmed with count 0 (65536 on
     hardware) delivered NOTHING in 60M instructions -- `dev_8253.c` maps a zero count to hz 0, clamped by `timer_add`
     to 1e-8 Hz, a timer that never fires.  Filed `pit8253count0`; not this round's edit.

## 2. Premise corrections to the brief (C-numbers; each names its finder and its check)

C1  (Astra, Grok; F-9)  "`dev_v3.c` carries a verbatim copy of bus_isa's handlers (Iyonix)" -> it is Algor's V3 and
    the copy is not verbatim.  Records only; the EOI arms are the same code for both PIC pairs.
C2  (Astra, Grok; F-3)  mc146818 is not one-shot; it is a level-while-count>0 source retired by the register-C read.
C3  (Astra, Grok; F-2)  "the only decrement of the pending count is in `isa_interrupt_deassert`, which the 8253 never
    calls" was TRUE AND UNDERSTATED: that decrement is dead on every machine because its pointer is NULL.
C4  (Grok; F-5)  "malta obtains the vector with OCW3 0x0c" -> NetBSD yes; Linux/malta reads the GT IACK register.
C5  (Astra)  "the ~2e-4 interference probability" of a UART tick landing inside the two-instruction read window is
    UNSUPPORTED: ticks are dispatched at batch boundaries, not uniformly; the eight repetitions need not be
    independent.  The phrase is withdrawn; the row's value is that all eight repetitions AGREED, which is a
    measurement, not a probability.
C6  (Astra, Grok; F-7)  the brief called the arm "specific EOI 0x60-0x67"; it also captures 0x21-0x27 and 0xe0-0xe7.
C7  (Astra, GLM)  Linux's ICW1 0x11 is EDGE mode; "`handle_level_irq`" says nothing about the PIC's trigger mode.
C8  (Grok)  the census missed malta's GT timer on ISA irq 9 (`DEVICE_TICK(gt)` asserts while its count > 0;
    `GT_INTR_CAUSE` read deasserts and decrements), the second ns16550 (irq 3), lpt (irq 7, no assert), and that the
    piix4 wdc exists only with a disk image.
C9  (GLM QA)  the `poll byte` row's state (F-6): the brief presented 0x84 as a plain contract; it was measured masked.
C10 (Grok)  `ier` is MASK polarity (`irr & ~ier` is the output) despite the struct comment "interrupt enable register".
C11 (Grok)  OCW1 0x10 masks line 4; "masked irr4" is therefore the right name but the row never EOIs while masked
    (the masked-EOI row is owed; section 4).
C12 (main loop)  the brief said NetBSD's EOI form was unknown.  It is SPECIFIC, slave-then-master, after a poll (F-4).

## 3. The six questions, ruled

Q1 (premise audit): corrections C1-C12 adopted.  The core premise survives on every seat and on the measurement:
    the EOI arm clears a request bit the device still holds, and nothing in OCW2 touches IRR on the datasheet.
Q2 (smallest edit that still passes): all eight agree the three named (d) variants leave the 19 rows green; the
    rows OWED are (i) EOI-while-masked then IRR read within two instructions (want 1), (ii) an n != 4 held-level EOI
    -- the 8253's line 0 is the natural one and the planned PIC2 line-12 row does NOT discriminate it (slave-local n
    is 4 again; and 0x60|12 = 0x6c would hit the stop path, F-7), (iii) `isr & bit` is EQUIVALENT under any design
    that never sets ISR and must be recorded so, not rowed; (iv) Grok's fourth hole -- reinstating the non-specific
    arm's `irr &= ~isr` alone -- is likewise equivalent while ISR is never set.  Under the acknowledge design below
    (iii) and (iv) become FALSIFIABLE (ISR is set at the acknowledge) and are then rowed.
Q3 (option set): two members were missing and both came from seats that went to the tree.  (F) = (A) plus an
    8253-side consumer (GLM QB); and the one this ruling adopts, from Astra ("the SOURCE owns assertion lifetime and
    pending-event retirement") and Grok ("clear the request at the ACKNOWLEDGE the guest performs; refill from a pin
    shadow only for a level pin; the sites are the poll read, `GT_PCI0_INTR_ACK`, `DEVICE_ACCESS(prep)`, Algor's
    reads").  (B) as sketched is rejected as incomplete (poll selection ignores the mask; no IRR clear at the ack;
    Linux never polls).  (C) collapses into the acknowledge design.  (D) restores the 8253's bit too.  (E) is a pckbc
    change and does not move the symptom rows.
Q4 (scope): `i8259isrnever` is NOT merged as a row, but the acknowledge design sets ISR at the poll/IACK as its own
    mechanism, so the sibling's malta-reachable half (poll and GT IACK set no ISR) is fixed BY CONSTRUCTION and its
    row is NARROWED to the PReP/footbridge IACK readers (F-10), which have no witness machine here.
Q5 (the 8253): measured (F-1) and chained to a documented guest (F-5): **(A) alone would hang Linux/malta** -- the
    kernel programs the PIT (`in_use`), requests IRQ 0, the model's host timer ratchets the count, the EOI no longer
    drops IRR bit 0, `timer_interrupt` always returns IRQ_HANDLED, so after the first unmask the CPU line never falls.
    HEAD's own behaviour is ALSO a defect: one interrupt per 2^14-instruction tick instead of per period, forever
    (F-1: the bit returns before the next read; F-2: the count can only grow).  Both are fixed by retiring one pending
    event at the acknowledge of line 0 and clearing its request bit there.
Q6 (NetBSD's EOI form): SPECIFIC, after a poll acknowledge, slave then master (F-4).  Every seat that said NOT
    CHECKABLE was right to say so from a packet; the fact is now read at source and inlined.

## 4. THE DESIGN THIS RULING TAKES TO F2 -- "(G) acknowledge": EOI touches ISR only; the guest's ACKNOWLEDGE moves the
##    request to service; the 8253's event is retired at that acknowledge

Edits (all in `dev_8259.c` except one line in `dev_gt.c`):
 G1  the two EOI arms: delete `d->irr &= ~d->isr;` (non-specific) and `d->irr &= ~(1 << (idata & 7));` (specific);
     keep the ISR clears; keep the recalc blocks but compute the output as `irr & ~ier` as today (they become dead
     code under G1 alone -- grok/GLM -- and are REMOVED, not kept dead; the acknowledge helper does its own recalc).
 G2  a static helper `pic8259_acknowledge(struct pic8259_data *d, struct machine *m)`: pick the lowest set bit of
     `d->irr & ~d->ier` (none -> return -1 and change nothing); set that ISR bit; CLEAR that IRR bit (both guests
     program LTIM=0; the model's devices re-assert every tick while a condition holds, so a still-pending level source
     re-requests within one tick -- the "refill from the pin" is already the devices' own convention); if `d` is pic1
     and the bit is 0 and `m->isa_pic_data.pending_timer_interrupts` is non-NULL and `> 0`, decrement it (read through
     the MACHINE at call time -- never a pointer captured at init, F-2); recompute pic1's cascade bit 2 from pic2 when
     `d` is pic2 (`pic1->irr |= 4` iff `pic2->irr & ~pic2->ier`, the `bus_isa.c:55-61` fold); then
     `if (d->irr & ~d->ier) INTERRUPT_ASSERT(d->irq) else INTERRUPT_DEASSERT(d->irq)`; return the bit.
 G3  the poll read (`current_command == 0x0c`, and the `default` arm, which emits the same byte today): call G2; return
     `0x80 | n` if it acknowledged a line, else 0x00.  (Selection becomes mask-aware as a by-product; the old
     mask-blind scan is the defect F-6 names.)
 G4  `dev_gt.c:154-157` (`GT_PCI0_INTR_ACK`): call G2 on `isa_pic_data.pic1` (and on pic2 if it returned 2); return the
     acknowledged line (8 + the slave line when the master gave 2) -- or `last_int` unchanged when nothing was pending
     (today's value; the spurious case is NOT re-designed here).  Witnessed on the same machine as the rest: the GT
     is at `0x1be00000` on malta, the register at `+0xc34` (`gtreg.h:114`), reachable by one guest load.
 NOT in this round: `dev_prep.c:57` and `dev_footbridge.c:432` (no witness machine; filed under the narrowed
     `i8259isrnever`); the ELCR; LTIM=1 level mode (the model keeps edge semantics; ICW1 bit 3 still only prints);
     the OCW2 arm census (F-7, own rows); the Algor read-clears (own row); the dead decrement in `bus_isa.c`/`dev_v3.c`
     (left in place: the fix reads the machine field directly, so no live code depends on the stale copy; its own row
     records the dead code).

Why (G) and not the smaller "(A) + line-0 special case at the EOI": the EOI-as-consume keeps every request bit set
until the device's own deassert, and ns16550/wdc/gt/mc146818 all deassert on a TICK or on a register read the handler
makes BEFORE the EOI -- so under "(A) + special case" Linux's unmask after the EOI finds the UART's bit still set until
the UART's next tick and re-enters the handler with nothing pending (spurious entries, up to one tick's worth per
real interrupt).  Under (G) the request bit is cleared at the acknowledge and only a NEW assert re-raises it.  HEAD
has no such churn because its EOI clears the bit; (G) keeps that property by moving the clear to where the
datasheet puts it.  The 8253 is covered by the same move (its event is retired at the acknowledge).

Cost in the floor's terms: clause (b) reinstatements per edited site (the two EOI clears; the poll's raw scan; the GT
read's `last_int` body); clause (d) over the helper's predicates (`irr & ~ier` selection; the pic1/bit-0 count guard;
the cascade fold) and the EOI arms' DEPENDS-ON (ISR only); the accept side: legal OCW2/OCW3 traffic still lands.

## 5. Detector consequences (rows the probe OWES before it is a detector; L1)

 R1  re-cut `poll byte`: poll BEFORE the OCW1 mask write (F-6); add `poll masked` = poll with only line 4 pending and
     line 4 masked, want 0x00 under (G) (HEAD reads 0x84 -- the pinned defect becomes a red row).
 R2  `poll acks`: after the poll, ISR bit 4 set (want 0x10) and IRR bit 4 clear two instructions later (want 0).
 R3  `eoi after ack`: poll, then specific EOI 0x64 -> ISR 0x00; IRR bit 4 re-set only after the UART's tick (sample
     after `e_delay()`: want 1 while the UART condition holds -- the level re-request).
 R4  `eoi irr4` / `eoi x8` unchanged (no poll before the EOI: IRR bit 4 stays 1 under (G)).
 R5  `masked eoi`: OCW1 0x10, EOI 0x64, IRR read within two instructions, want 1 (Q2(i)).
 R6  the 8253 rows (the n != 4 held-level line, Q2(ii)): program counter 0 (0x34/0x1000), wait ~18M instructions
     (F-1's measured sufficient wait), read IRR bit 0 (control: 1); poll -> byte 0x80, and IRR bit 0 read two
     instructions later wants 0 under (G) while HEAD reads 1 (its poll acknowledges nothing) -- a red symptom row;
     then, in a SEPARATE session with no poll, EOI 0x60 and IRR bit 0 two instructions later: want 1 under (G) (the
     EOI no longer clears it; the 8253's tick keeps it) while HEAD reads 0 -- the n != 4 held-level anchor the (d)
     table needs, R4's shape on line 0.  A third session pins the retirement: poll (bit 0 cleared, count retired),
     then IRR bit 0 read after a short wait (a few thousand instructions, under one host-timer period) wants 0 under
     (G) -- the tick re-asserts only while the count is > 0 -- while HEAD reads 1 (its count never falls).
 R7  `gt iack`: with the UART level on, a guest load from `0xbbe00c34` returns 4 (both columns) and under (G) ISR bit 4
     reads 0x10 and IRR bit 4 reads 0 afterwards (HEAD: ISR 0, IRR 1).
 R8  `isr` rows: `quiet isr`, `level isr` keep want 0 in both columns (no acknowledge has happened); `eoi isr` after a
     poll -> 0.
 R9  cascade: PIC2 line 12 via the ns16550?  No ISA source on malta sits on the slave except pccmos (irq 8): program
     the mc146818 periodic interrupt (PIE) for a level on line 8 -> master IRR bit 2 folds; poll master -> 0x82, poll
     slave -> 0x80; EOI slave 0x60 then master 0x62 -> ISR clear both; the fold recomputed.  (Owed only if the
     adjudication keeps the cascade inside the round; otherwise filed with the contract naming it OUTSIDE.)
 Equivalent mutants to RECORD, not row: `if (d->isr & bit)` around a reinstated IRR clear is equivalent under HEAD's
 never-set ISR but NOT under (G) (R2/R3 red it); the non-specific `irr &= ~isr` reinstatement is caught by R3's
 ISR-set state only if a non-specific EOI row exists after a poll -> add `nonspec after ack`.

## 6. Rows to FILE from this pass (one line each; provenance in brackets)

 - `pit8253pendingptr`  MED  `bus_isa.c:224` and `dev_v3.c:297` snapshot `isa_pic_data.pending_timer_interrupts` before
   `DEVINIT(8253)` publishes it (NULL on every machine); the decrement at `bus_isa.c:138`/`dev_v3.c:145` is dead code;
   `dev_8253.c`'s count is increment-only.  [Astra, Grok; CHECKED]  (The (G) fix reads the machine field at call time.)
 - `i8259cmdhalt`  HIGH-class (emulation stop)  any OCW2/OCW3 byte outside {0x0a,0x0b,0x0c,0x20,0x21-0x27,0x60-0x67,
   0x68,0xc0-0xc7,0xe0-0xe7} -- 0xa0-0xa7 (rotate on non-specific EOI), 0x00, 0x40, 0x48, 0x80 among them -- reaches
   `cpu->running = 0` at `dev_8259.c:140`.  [Grok, GLM; CHECKED]  Host-stop class: HELD with the other HIGH rows.
 - `i8259ocw2nonspec`  LOW  0x21-0x27 are treated as specific EOIs (datasheet: SL=0 is non-specific); 0xe0-0xe7's
   rotate is not performed; `priority_reg` is never written.  [Astra, Grok]
 - `i8259pollmask`  MED  the poll (0x0c and the `default` read arm) returns a MASKED line and ignores priority;
   measured 0x84 with line 4 masked (`witness_20261025/RESULTS_base.txt`, row `poll byte`).  [GLM QA, Grok; CHECKED]
   Fixed BY CONSTRUCTION by (G3) if (G) is ruled; otherwise its own round.
 - `algorisaintclear`  LOW  `dev_algor.c` `P5064_LOCINT`/`P5064_ISAINT` READS clear PIC request bits (`irr &= ~0x18`,
   `pic2->irr &= ~0xc0`) -- a read-acknowledge outside the PIC, same class, different producer, no witness machine
   (Algor).  [Astra, Grok]
 - `isaiackreaders`  LOW  `dev_prep.c:57` and `dev_footbridge.c:432` return `last_int` with no acknowledge -- the
   remainder of `i8259isrnever` after (G) covers the poll and the GT read.  [Grok; CHECKED]
 - `i8259ltim`  LOW  ICW1 bit 3 (level-triggered mode) only prints (`dev_8259.c:74-76`); the model is edge-only after
   (G); NetBSD/malta also writes an ELCR nothing models.  [Grok]
 - `pit8253count0`  LOW  a zero count (65536 on the 8253/8254) is mapped to hz 0 (`dev_8253.c`, the `else d->hz[...] = 0;`
   arm of the MSB write), which `timer_add` clamps to TIMER_MIN_FREQUENCY (1e-8 Hz): the timer never fires.  MEASURED
   (`rate_explore_20261025/rate_073805`: 0 deliveries in 60M instructions; 0xffff delivered 7,415).  [main loop]
 - the brief's own records corrections C1-C12 go into the round's CHANGELOG block, not into rows.

## 7. Disputes carried to F2 (both sides in their own words; the adjudicator rules)

 D1  (A) alone -- GLM QA/QB and DeepSeek QA: "ship (A) alone this round; file (B)" / "do not close until the PIT path
     is settled"; Astra, Grok, GLM QC, DeepSeek QB/QC: "(A) alone fails the floor / removes the only request-consume".
     Main loop: REJECT (A) alone on F-1 + F-5 (a documented guest hangs).
 D2  Where the acknowledge lives -- GLM QB: "(B) is a family with an undecided site (poll / selection / IACK)";
     Grok: "the ack sites that are actually in src/: poll, GT IACK, PReP, Algor"; Astra: "A + a separately specified
     PIT lifetime/accounting correction".  Main loop: poll + GT IACK in this round (both witnessed on malta), PReP/
     footbridge filed.  QUESTION for the adjudicator: is the GT read inside the round-scope rule (same semantic class,
     one detector, witnessed on the same machine) or a second round?
 D3  Edge vs level at the acknowledge -- the model clears the request bit at the ack for every line (edge semantics,
     what both guests program) and relies on the devices' per-tick re-assert for a still-pending level source.
     Astra: "INTERRUPT_ASSERT invokes the callback unconditionally; a callback invocation cannot be read as a new
     electrical edge" -- which is exactly why the per-tick re-assert refills the bit.  QUESTION: accept edge-only with
     LTIM filed, or must (G) honour ICW1 bit 3 now?
 D4  The dead recalc blocks -- GLM: "dead code outright; fix the sentence"; main loop: REMOVE them in the EOI arms
     (the helper recalcs), keep the OCW1 arm's.
 D5  Severity of #574 itself -- F-3 shows no lost request on malta (latency only) while F-1/F-5 show the 8253 rate
     defect is live for Linux/malta today.  QUESTION: does the row keep MED WRONG-RESULT with its exposure record
     rewritten (the lost-request half is one-shot machines; the live malta half is the 8253's rate and the mask-blind
     poll), or split?
