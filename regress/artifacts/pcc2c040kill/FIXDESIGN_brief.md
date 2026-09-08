# pcc2c040kill -- FIX DESIGN (pass 1).  ONE legal guest byte store ends the host.

**PLEASE DO NOT SIMPLY RATIFY.**  A recent panel had seven of nine seats confirm a premise the brief
stated wrongly (a census off by 4x).  **CHECK THE PREMISES, NOT JUST THE DERIVATIONS** -- every
numbered premise below is stated so you can refute it, and I would rather be corrected than agreed
with.  If you cannot settle a premise from this packet, SAY SO by name rather than assuming it.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  Ignore any other `src/` you find: there are FOUR
pristine-2021-upstream copies under the project root, and a seat reading one reports line numbers off
by hundreds and arms that do not exist here.

---

## 1.  THE DEFECT, MEASURED (not argued)

`regress/pcc2_c040_probe.py`, run on the committed build, artifact
`regress/artifacts/pcc2c040kill/witness_HEAD_20260907.raw`:

    genctl ctl     alive        alive        CONTROL: same st.b, same GENCTL, benign 0x10
    genctl ctlq    no           no           CONTROL: the benign write must NOT reach the C040 arm
    c040 kill      died(exit1)  alive        THE DEFECT -- RED, per witness clause (i)
    c040 attrib    yes          yes          ATTRIBUTION: the death carries the arm's unique text
    EVIDENCE: pcc2: C040 interrupt assertions... TODO

**A single guest `st.b` of 0x04 to PCC2 GENCTL (offset 0x02, base 0xfff42000) on an unmodified
`-E mvme88k -e mvme187` terminates the emulator.**  No driver, no second access, no interrupt: the
GENCTL write arm stores `idata` UNMASKED and calls `reassert_interrupts()` in the same access, and
the C040 test is the FIRST thing in that helper.

## 2.  SETTLED PREMISES (inlined because the packet-fed seats cannot read files)

Each was verified on this machine today.  **P2, P3 and P4 come from the OpenBSD 2.2 source tree that
sits at the project root (`_guest-src-openbsd22/`), not from a datasheet.**

* **P1.**  The fork's `PCC2_C040 = 0x04` and `PCC2_MIEN = 0x02`
  (`src/include/thirdparty/mvme_pcctworeg.h`) are **byte-for-byte OpenBSD's
  `sys/arch/mvme88k/dev/pcctworeg.h`**, which reads `PCC2_DR0 0x80 / PCC2_C040 0x04 /
  PCC2_MIEN 0x02 / PCC2_FAST 0x01`.  *A SECOND guest header,
  `mvme88k/include/pcctworeg.h` lines 139-141, gives `FAST 0x01 / IEN 0x02 / C040 0x03` --
  overlapping masks, which looks like a bug in that header.  The fork follows the `dev/` one.*
  **Is the fork constant right?  I believe yes; refute me if 0x03 is the real encoding.**
* **P2.**  **No file in the OpenBSD 2.2 tree writes C040 to GENCTL.**  A recursive grep for C040
  over `sys/` returns only the two defines, an unrelated `MEMC040` memory-controller macro, and
  S-record bootloader bytes.
* **P3.**  A real driver DOES write GENCTL, but on the 68k board and as a **read-modify-write OR**:
  `mvme68k/dev/pcctwo.c` line 167, `sc->sc_pcc2->pcc2_genctl |= PCC2_GENCTL_IEN;`.
* **P4.**  **mvme88k own `pcctwo.c` never writes `genctl` at all** -- its attach reads chip
  id/rev and takes pointers to `pcc2_ipl` / `pcc2_imask`.
* **P5.**  C040 means *the CPU is an MC68040*, so interrupts leave on the EIPL<2..0> pins.  The
  fork own comment says that mechanism is "Not implemented yet".  **On an m88k board no guest
  should set it** -- which is why P2 is unsurprising and why this is a robustness fix, not a
  compatibility one.
* **P6.**  `reassert_interrupts()` is a **void helper called from TEN sites** in this file
  (lines 383, 400, 459, 551, 574, 588, 602, 609, 622, 662).  Its only outputs are register state in
  `d->pcctwo_reg[]` / `d->cur_int_vec[]` and the CPU interrupt line.
* **P7.**  The file already carries the house latch idiom **per device instance**: a
  `uint32_t warned` bitfield in `struct pcc2_data` with a per-block enum and a compile-time width
  assert (`pcc2_w_fits_in_warned`), plus a `uint64_t warned_unimpl` for the `default:` arm.  The
  tree suppression marker is `(once)` -- the overwhelming plurality; re-derive it with a grep
  rather than trusting a number here.

**NOT CLAIMED:** that any shipped guest reaches this.  P2 says the opposite for OpenBSD 2.2, and
that is ONE guest at ONE version -- what a driver does is evidence a real driver does it; what it
does not do is not evidence that no guest does.

## 3.  THE FULL ENCLOSING FUNCTION, VERBATIM

*A proposed edit is a SKETCH until it has been run against the real control flow.  This project once
had four independent readers -- three seats and the adjudicator -- propose an early `return` into a
function with a common tail, and none of them looked nine lines down.  So the whole function is
here, every exit path and the tail included.*

```c
 267| static void reassert_interrupts(struct pcc2_data *d)
 268| {
 269| 	int assert = 0;
 270| 
 271| 	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
 272| 		/*  The M68000 interrupt mechanism involves outputting
 273| 		    interrupt level on pins EIPL<2..0>. Not implemented
 274| 		    yet.  */
 275| 		fatal("pcc2: C040 interrupt assertions... TODO\n");
 276| 		exit(1);
 277| 	}
 278| 
 279| 	/*
 280| 	 *  Recalculate current interrupt level:
 281| 	 */
 282| 	d->pcctwo_reg[PCCTWO_IPL] = 0;
 283| 
 284| 	/*  Timer interrupts?  */
 285| 	if (d->pending_timer1_interrupts > 0 &&
 286| 	    d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
 287| 		d->pcctwo_reg[PCCTWO_T1ICR] |= PCC2_TTIRQ_INT;
 288| 	if (d->pending_timer2_interrupts > 0 &&
 289| 	    d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
 290| 		d->pcctwo_reg[PCCTWO_T2ICR] |= PCC2_TTIRQ_INT;
 291| 
 292| 	if (d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_INT) {
 293| 		int intlevel = d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IL;
 294| 		d->cur_int_vec[intlevel] = PCC2V_TIMER1;
 295| 		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
 296| 			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
 297| 	}
 298| 	if (d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_INT) {
 299| 		int intlevel = d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IL;
 300| 		d->cur_int_vec[intlevel] = PCC2V_TIMER2;
 301| 		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
 302| 			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
 303| 	}
 304| 
 305| 	if (d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IEN &&
 306| 	    d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_INT) {
 307| 		int intlevel = d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IPL;
 308| 		d->cur_int_vec[intlevel] = PCC2V_SCC_TX;
 309| 		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
 310| 			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
 311| 	}
 312| 
 313| 	if (d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IEN &&
 314| 	    d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_INT) {
 315| 		int intlevel = d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IPL;
 316| 		d->cur_int_vec[intlevel] = PCC2V_SCC_RX;
 317| 		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
 318| 			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
 319| 	}
 320| 
 321| 	if (d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IEN &&
 322| 	    d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_INT) {
 323| 		int intlevel = d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IPL;
 324| 		d->cur_int_vec[intlevel] = PCC2V_SCSI;
 325| 		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
 326| 			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
 327| 	}
 328| 
 329| 	/*  TODO: Other interrupt sources.  */
 330| 
 331| 	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
 332| 	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
 333| 	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
 334| 		assert = 1;
 335| 
 336| 	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
 337| 		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
 338| 		assert ? "ASSERT" : "no assert");
 339| 
 340| 	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
 341| 	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
 342| 		assert = 0;
 343| 
 344| 	if (assert)
 345| 		INTERRUPT_ASSERT(d->cpu_irq);
 346| 	else
 347| 		INTERRUPT_DEASSERT(d->cpu_irq);
 348| }
```

## 4.  THE PROPOSED FIX, and the reason it is shaped this way

The adjudicated disposition (codex, assess stage) is **DECLINE + LATCHED ANNOUNCE**.  The option-set
rule says to GREP THE FORK FOR AN EXISTING IDIOM before reasoning from first principles -- **and the
idiom for this exact situation is SEVENTY LINES BELOW THE KILL, IN THE SAME FUNCTION:**

    /*  ... but only allow interrupts if Master Interrupt Enable is on:  */
    if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
            assert = 0;

**That is the other GENCTL interrupt-control bit, and it suppresses assertion by clearing `assert`
and FALLING THROUGH to the common tail -- it does not return early.**  So:

```c
    /*  ... but only allow interrupts if Master Interrupt Enable is on:  */
    if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
            assert = 0;

    /*  #NNN: ... and not in C040 mode, whose EIPL<2..0> pin mechanism is unmodelled.  This
        used to be a fatal()+exit(1) at the TOP of this function, so ONE legal guest byte
        write of 0x04 to GENCTL ended the host (regress/pcc2_c040_probe.py).  Declining to
        ASSERT -- rather than returning -- is the disposition the MIEN test above already
        applies to the other GENCTL interrupt-control bit, and it keeps the IPL
        recalculation and the INTERRUPT_DEASSERT tail that an early return would skip.  */
    if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
            if (!(d->warned & (1u << PCC2_W_C040))) {
                    d->warned |= (1u << PCC2_W_C040);
                    fatal("[ pcc2: C040 (MC68040 EIPL) interrupt mechanism not "
                        "implemented; interrupts suppressed  (once) ]\n");
            }
            assert = 0;
    }
```

**Why NOT the two obvious alternatives:**
* **an early `return` at the existing site** skips `d->pcctwo_reg[PCCTWO_IPL] = 0`, the whole IPL
  recalculation, the `cur_int_vec[]` updates AND the `INTERRUPT_ASSERT`/`INTERRUPT_DEASSERT` tail --
  so the CPU line would keep whatever state it had, and a guest read of IPL would return a stale
  number.  **This is the sketch-rule hazard exactly.**
* **deleting the test** lets the model assert an m88k interrupt while the guest has selected a
  mechanism the model does not have, i.e. it models something the hardware would not do.

## 5.  THE THREE QUESTIONS

**Q1 (STRUCTURE).**  Is joining the MIEN test right, or does C040 mode additionally require
suppressing the IPL *recalculation* (leaving `PCCTWO_IPL` untouched rather than recomputed)?  Argue
from what a real PCC2 does with its IPL register when C040 is set -- **and say plainly if you cannot
settle it from this packet.**

**Q2 (THE DISCRIMINATING ROW -- the hard one).**  The shipped witness own contract says it is
**NOT a detector of the repair**: "host survives" greens for a silent decline, a latched decline and
a real C040 implementation alike.  **What row separates them?**  The announce text and its once-only
property are the obvious channel -- is that enough, and what is the (d)-clause mutant that a
text-matching row would MISS?  Note the latch bit lives in a SHARED `uint32_t warned` whose other
bits are set by ordinary guest register traffic, so a bit collision is a live mutant shape here
(this project measured exactly that in round #490).

**Q3 (PREMISE AUDIT).**  Which of P1-P7 is wrong?  P1 is the one I am least sure of, because two
guest headers disagree; P6 caller count was derived by grep and could be off if a caller is
inside a macro.

**VERDICT LINE FIRST, please** -- one line at the very top saying IMPLEMENT-AS-PROPOSED /
IMPLEMENT-WITH-REVISIONS / REFUSE, so it survives truncation.  Then the body.  **A verdict that
merely agrees is the least useful thing you can send**; if you find nothing wrong, say what you
CHECKED and how.
