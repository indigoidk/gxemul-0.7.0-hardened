# sgirekills -- ROUND DESIGN.  Six RE read arms end the host on a legal 8-byte load.

**PLEASE DO NOT RATIFY.**  A previous brief on this row stated FIVE premises that a reviewing seat
refuted, **including one that would have shipped a detector GREEN ON HEAD.**  Those corrections are
folded in below and marked; **check them too** -- a correction carries more authority than the error
it replaces, which makes it exactly the thing to re-verify.

**The tree under review is `GXEMUL-SEC/src/`.**  Other `src/` copies under the project root are
pristine 2021 upstream and give line numbers off by hundreds.

---

## 1.  THE DEFECT

`dev_sgi_re.c`, `DEVICE_ACCESS(sgi_re)`.  Six address windows each end with:

    } else {
            fatal("TODO: read from CRIME_RE_<window>\n");
            exit(1);
    }

A legal guest **`ld`** (8-byte load) from any of the six ends the emulator.

## 2.  THE FULL ARM CASCADE, VERBATIM

*A proposed edit is a SKETCH until it has been read against the real control flow, so the whole
cascade is here rather than one arm.*

```c
 420| 	if (relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B) {
 421| 		if (len != 8) {
 422| 			if (!(d->warned & SGIRE_W_TLBA_LEN)) {
 423| 				d->warned |= SGIRE_W_TLBA_LEN;
 424| 				fatal("[ sgi_re: unimplemented len=%i for "
 425| 				    "CRIME_RE_TLB_A -- declined.  (once) ]\n",
 426| 				    (int) len);
 427| 			}
 428| 		} else if (writeflag == MEM_WRITE) {
 429| 			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
 430| 			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
 431| 				d->re_tlb_a[tlbi] = data[hwi]*256 + data[hwi+1];
 432| 				debug("d->re_tlb_a[%i] = 0x%04x\n", tlbi, d->re_tlb_a[tlbi]);
 433| 				tlbi++;
 434| 			}
 435| 		} else {
 436| 			fatal("TODO: read from CRIME_RE_TLB_A\n");
 437| 			exit(1);
 438| 		}
 439| 	} else if (relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C) {
 440| 		if (len != 8) {
 441| 			if (!(d->warned & SGIRE_W_TLBB_LEN)) {
 442| 				d->warned |= SGIRE_W_TLBB_LEN;
 443| 				fatal("[ sgi_re: unimplemented len=%i for "
 444| 				    "CRIME_RE_TLB_B -- declined.  (once) ]\n",
 445| 				    (int) len);
 446| 			}
 447| 		} else if (writeflag == MEM_WRITE) {
 448| 			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
 449| 			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
 450| 				d->re_tlb_b[tlbi] = data[hwi]*256 + data[hwi+1];
 451| 				debug("d->re_tlb_b[%i] = 0x%04x\n", tlbi, d->re_tlb_b[tlbi]);
 452| 				tlbi++;
 453| 			}
 454| 		} else {
 455| 			fatal("TODO: read from CRIME_RE_TLB_B\n");
 456| 			exit(1);
 457| 		}
 458| 	} else if (relative_addr >= CRIME_RE_TLB_C && relative_addr < CRIME_RE_TLB_C + 0x200) {
 459| 		if (len != 8) {
 460| 			if (!(d->warned & SGIRE_W_TLBC_LEN)) {
 461| 				d->warned |= SGIRE_W_TLBC_LEN;
 462| 				fatal("[ sgi_re: unimplemented len=%i for "
 463| 				    "CRIME_RE_TLB_C -- declined.  (once) ]\n",
 464| 				    (int) len);
 465| 			}
 466| 		} else if (writeflag == MEM_WRITE) {
 467| 			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
 468| 			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
 469| 				d->re_tlb_c[tlbi] = data[hwi]*256 + data[hwi+1];
 470| 				debug("d->re_tlb_c[%i] = 0x%04x\n", tlbi, d->re_tlb_c[tlbi]);
 471| 				tlbi++;
 472| 			}
 473| 		} else {
 474| 			fatal("TODO: read from CRIME_RE_TLB_C\n");
 475| 			exit(1);
 476| 		}
 477| 	} else if (relative_addr >= CRIME_RE_TEX && relative_addr < CRIME_RE_TEX + 0xe0) {
 478| 		if (len != 8) {
 479| 			if (!(d->warned & SGIRE_W_TEX_LEN)) {
 480| 				d->warned |= SGIRE_W_TEX_LEN;
 481| 				fatal("[ sgi_re: unimplemented len=%i for "
 482| 				    "CRIME_RE_TEX -- declined.  (once) ]\n",
 483| 				    (int) len);
 484| 			}
 485| 		} else if (writeflag == MEM_WRITE) {
 486| 			int tlbi = ((relative_addr & 0xff) >> 3) & 0xff;
 487| 			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
 488| 				d->re_tex[tlbi] = data[hwi]*256 + data[hwi+1];
 489| 				debug("d->re_tex[%i] = 0x%04x\n", tlbi, d->re_tex[tlbi]);
 490| 				tlbi++;
 491| 			}
 492| 		} else {
 493| 			fatal("TODO: read from CRIME_RE_TEX\n");
 494| 			exit(1);
 495| 		}
 496| 	} else if (relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80) {
 497| 		if (len != 8) {
 498| 			/*
 499| 			 *  #497: THIS GUARD IS ALSO THE ONLY BOUNDS CHECK.  Unlike the
 500| 			 *  TLB/TEX arms, the store below is FIXED ARITY -- it ignores len
 501| 			 *  and always writes [tlbi] and [tlbi+1].  tlbi is
 502| 			 *  ((relative_addr & 0x7f) >> 2) & 0x1f, so it reaches 31 and
 503| 			 *  [tlbi+1] indexes 32 of a [32] array.  Only 8-byte ALIGNMENT
 504| 			 *  keeps tlbi even and thus <= 30.  On the GUEST paths that
 505| 			 *  alignment is supplied by two independent mechanisms, and both
 506| 			 *  were checked rather than assumed:
 507| 			 *    - an ordinary ld/sd tests addr & (LS_SIZE-1) and raises
 508| 			 *      ADES/ADEL WITHOUT calling memory_rw at all
 509| 			 *      (cpus/cpu_mips_instr_loadstore.c);
 510| 			 *    - the unaligned ldl/ldr/sdl/sdr helper masks the address
 511| 			 *      itself -- cpus/cpu_mips_instr_unaligned.c computes
 512| 			 *      aligned_addr = addr & ~(wlen-1) and passes THAT to all
 513| 			 *      three of its memory_rw calls, so it cannot deliver an
 514| 			 *      unaligned len == 8 either.
 515| 			 *  Narrower accesses carry len != 8 and are declined above, and
 516| 			 *  dev_sgi_re_init is called only from machines/machine_sgi.c,
 517| 			 *  so no other CPU family reaches this handler.
 518| 			 *
 519| 			 *  ONE EXCEPTION, AND IT IS NOT A GUEST PATH: the host debugger's
 520| 			 *  `put d' prints "WARNING: address isn't aligned" and then
 521| 			 *  PROCEEDS -- the warning is a printf, not a guard -- so it can
 522| 			 *  hand an unaligned len == 8 straight to memory_rw.  That is why
 523| 			 *  the invariant above is stated for GUEST paths only.  It also
 524| 			 *  means `put d' must NOT be used to "witness" the over-run:
 525| 			 *  it bypasses the guest instruction path, so a reproduction
 526| 			 *  built on it would be laundering rather than witnessing.
 527| 			 *  The over-run itself stays filed as sgilinearoob, and it is
 528| 			 *  NOT guest-reachable while this guard stands.
 529| 			 *
 530| 			 *  Measured, not assumed: the over-run stays INSIDE the struct --
 531| 			 *  re_linear_a[32] IS re_linear_b[0] and re_linear_b[32] IS
 532| 			 *  de_reg[0] (offsetof: 1760/1888/2016).  So this is undefined
 533| 			 *  behaviour and a SILENT clobber of the adjacent register array,
 534| 			 *  reaching a DRAWING-engine register from a rendering-engine
 535| 			 *  write -- not a wild write outside the allocation, and not
 536| 			 *  something plain ASAN would flag.  Declining keeps it shut.
 537| 			 */
 538| 			if (!(d->warned & SGIRE_W_LINA_LEN)) {
 539| 				d->warned |= SGIRE_W_LINA_LEN;
 540| 				fatal("[ sgi_re: unimplemented len=%i for "
 541| 				    "CRIME_RE_LINEAR_A -- declined.  (once) ]\n",
 542| 				    (int) len);
 543| 			}
 544| 		} else if (writeflag == MEM_WRITE) {
 545| 			/*
 546| 			 *  Very interesting. NetBSD writes stuff such as:
 547| 			 *
 548| 			 *  CRIME_RE_LINEAR_A IDATA = 8000173080001731
 549| 			 *  CRIME_RE_LINEAR_A IDATA = 8000173280001733
 550| 			 *  CRIME_RE_LINEAR_A IDATA = 8000173480001735
 551| 			 *  ...
 552| 			 *
 553| 			 *  but the PROM writes something which looks like wrongly
 554| 			 *  32-bit sign-extended words:
 555| 			 *
 556| 			 *  CRIME_RE_LINEAR_A IDATA = ffffffff80040001
 557| 			 *  CRIME_RE_LINEAR_A IDATA = ffffffff80040003
 558| 			 *  CRIME_RE_LINEAR_A IDATA = ffffffff80040005
 559| 			 *  ...
 560| 			 *
 561| 			 *  followed by
 562| 			 *  [ sgi_mte: STARTING TRANSFER: mode=0x00000011
 563| 			 *    dst0=0x0000000040000000, dst1=0x0000000040007fff
 564| 			 *    (length 0x8000), dst_y_step=0 bg=0x0, bytemask=0xffffffff ]
 565| 			 *
 566| 			 *  indicating that it really meant to put both 0x80040000
 567| 			 *  and 0x80040001 into the first LINEAR_A entry.
 568| 			 *
 569| 			 *  The first guess would be a bug in the implementation of
 570| 			 *  one or more instructions in the emulator while coming up
 571| 			 *  with those values, but debugging the PROM so far has NOT
 572| 			 *  revealed any such bug. It may even be that the PROM code
 573| 			 *  is buggy (?) and never really set the LINEAR entries
 574| 			 *  correctly. Perhaps the hardware simply ignores the
 575| 			 *  weird values and does not fill it (using the MTE)
 576| 			 *  when asked to.
 577| 			 */
 578| 			// printf("CRIME_RE_LINEAR_A IDATA = %016llx\n", (long long)idata);
 579| 			int tlbi = ((relative_addr & 0x7f) >> 2) & 0x1f;
 580| 			d->re_linear_a[tlbi] = idata >> 32ULL;
 581| 			d->re_linear_a[tlbi+1] = idata;
 582| 			debug("[ d->re_linear_a[%i] = 0x%08x, [%i] = 0x%08x ]\n",
 583| 				tlbi, d->re_linear_a[tlbi], tlbi+1, d->re_linear_a[tlbi+1]);
 584| 		} else {
 585| 			fatal("TODO: read from CRIME_RE_LINEAR_A\n");
 586| 			exit(1);
 587| 		}
 588| 	} else if (relative_addr >= CRIME_RE_LINEAR_B && relative_addr < CRIME_RE_LINEAR_B + 0x80) {
 589| 		if (len != 8) {
 590| 			/*
 591| 			 *  #497: THIS GUARD IS ALSO THE ONLY BOUNDS CHECK.  Unlike the
 592| 			 *  TLB/TEX arms, the store below is FIXED ARITY -- it ignores len
 593| 			 *  and always writes [tlbi] and [tlbi+1].  tlbi is
 594| 			 *  ((relative_addr & 0x7f) >> 2) & 0x1f, so it reaches 31 and
 595| 			 *  [tlbi+1] indexes 32 of a [32] array.  Only 8-byte ALIGNMENT
 596| 			 *  keeps tlbi even and thus <= 30.  On the GUEST paths that
 597| 			 *  alignment is supplied by two independent mechanisms, and both
 598| 			 *  were checked rather than assumed:
 599| 			 *    - an ordinary ld/sd tests addr & (LS_SIZE-1) and raises
 600| 			 *      ADES/ADEL WITHOUT calling memory_rw at all
 601| 			 *      (cpus/cpu_mips_instr_loadstore.c);
 602| 			 *    - the unaligned ldl/ldr/sdl/sdr helper masks the address
 603| 			 *      itself -- cpus/cpu_mips_instr_unaligned.c computes
 604| 			 *      aligned_addr = addr & ~(wlen-1) and passes THAT to all
 605| 			 *      three of its memory_rw calls, so it cannot deliver an
 606| 			 *      unaligned len == 8 either.
 607| 			 *  Narrower accesses carry len != 8 and are declined above, and
 608| 			 *  dev_sgi_re_init is called only from machines/machine_sgi.c,
 609| 			 *  so no other CPU family reaches this handler.
 610| 			 *
 611| 			 *  ONE EXCEPTION, AND IT IS NOT A GUEST PATH: the host debugger's
 612| 			 *  `put d' prints "WARNING: address isn't aligned" and then
 613| 			 *  PROCEEDS -- the warning is a printf, not a guard -- so it can
 614| 			 *  hand an unaligned len == 8 straight to memory_rw.  That is why
 615| 			 *  the invariant above is stated for GUEST paths only.  It also
 616| 			 *  means `put d' must NOT be used to "witness" the over-run:
 617| 			 *  it bypasses the guest instruction path, so a reproduction
 618| 			 *  built on it would be laundering rather than witnessing.
 619| 			 *  The over-run itself stays filed as sgilinearoob, and it is
 620| 			 *  NOT guest-reachable while this guard stands.
 621| 			 *
 622| 			 *  Measured, not assumed: the over-run stays INSIDE the struct --
 623| 			 *  re_linear_a[32] IS re_linear_b[0] and re_linear_b[32] IS
 624| 			 *  de_reg[0] (offsetof: 1760/1888/2016).  So this is undefined
 625| 			 *  behaviour and a SILENT clobber of the adjacent register array,
 626| 			 *  reaching a DRAWING-engine register from a rendering-engine
 627| 			 *  write -- not a wild write outside the allocation, and not
 628| 			 *  something plain ASAN would flag.  Declining keeps it shut.
 629| 			 */
 630| 			if (!(d->warned & SGIRE_W_LINB_LEN)) {
 631| 				d->warned |= SGIRE_W_LINB_LEN;
 632| 				fatal("[ sgi_re: unimplemented len=%i for "
 633| 				    "CRIME_RE_LINEAR_B -- declined.  (once) ]\n",
 634| 				    (int) len);
 635| 			}
 636| 		} else if (writeflag == MEM_WRITE) {
 637| 			int tlbi = ((relative_addr & 0x7f) >> 2) & 0x1f;
 638| 			d->re_linear_b[tlbi] = idata >> 32ULL;
 639| 			d->re_linear_b[tlbi+1] = idata;
 640| 			debug("[ d->re_linear_b[%i] = 0x%08x, [%i] = 0x%08x ]\n",
 641| 				tlbi, d->re_linear_b[tlbi], tlbi+1, d->re_linear_b[tlbi+1]);
 642| 		} else {
 643| 			fatal("TODO: read from CRIME_RE_LINEAR_B\n");
 644| 			exit(1);
 645| 		}
 646| 	} else {
 647| 		if (writeflag == MEM_WRITE) {
 648| 			if (!(d->warned & SGIRE_W_UNMAP_WR)) {
 649| 				d->warned |= SGIRE_W_UNMAP_WR;
 650| 				fatal("[ sgi_re: unimplemented write to "
 651| 				    "address 0x%llx, data=0x%016llx -- "
 652| 				    "declined.  (once) ]\n",
 653| 				    (long long)relative_addr, (long long)idata);
 654| 			}
 655| 		} else {
 656| 			if (!(d->warned & SGIRE_W_UNMAP_RD)) {
 657| 				d->warned |= SGIRE_W_UNMAP_RD;
 658| 				fatal("[ sgi_re: unimplemented read from address"
 659| 				    " 0x%llx -- declined.  (once) ]\n",
 660| 				    (long long)relative_addr);
```

## 3.  SETTLED PREMISES -- including FIVE CORRECTIONS to the previous brief

* **C1 (the important one).  THE KILL IS REACHED BY `ld`, NOT `lw`.**  The previous brief said a
  guest `lw` kills.  It does not: the `if (len != 8)` arm DECLINES first, and the shipped probe's
  `load()` defaults to `lw`.  **Six accept rows written with `lw` would be GREEN ON HEAD** --
  vacuous by construction, vacuity-floor clause (a).
* **C2.  The census is ELEVEN guest-reachable kills, not twelve.**  `grep -cE '^[[:space:]]+exit\(1\);'`
  returns 12 STATEMENTS and is right, but one is provably unreachable: it is the trailing `else` of
  `if (len == 4) ... else if (len != 4) ... else`, an exact negation.  *A text pattern cannot test
  reachability.*  That dead arm already belongs to a different row.
* **C3.  The "the model already stores the right thing" warrant is FALSE for TEX**, and that is
  itself a filed defect: `re_tex` is written with `((relative_addr & 0xff) >> 3) & 0xff`, consecutive
  stores overlap by three, 81 of 112 cells are unreachable, and there are ZERO consumers.
* **C4.  The committed vehicle is `regress/sgi_re_width_probe.py`**, whose six `ld kill` rows ARE the
  witness -- not `sgi_re_rgb_probe.py`, which is uncommitted work that issues no RE register read.
* **C5.  Those six rows must be RE-PINNED FIRST.**  They currently want `exit1+txt`, so a correct fix
  turns them RED.  The oracle-correction rule requires: re-pin, measure the COMMITTED build RED under
  the new expectations, THEN change the code.  Same scripts, opposite colour.

**The store side, from the cascade above:** TLB_A/B/C are `uint16_t[256]` written as FOUR big-endian
halfwords per 8-byte store (`data[hwi]*256 + data[hwi+1]`, `tlbi++`); LINEAR_A/B are `uint32_t[32]`
written as two words.  **A read that returns only `array[i]` keeps 16 of 64 bits** and is a null
repair that a survival-only row cannot see.

**NOT CLAIMED:** that any guest driver performs these reads.  The witness is a probe.

## 4.  THE PROPOSED ROUND (a reviewing seat's design, not yet adjudicated)

**Five ACCEPT + TEX DECLINE; MTE stays OUT.**

* **TLB_A/B/C and LINEAR_A/B -> ACCEPT** (option-set member 4): return what the store recorded,
  packed as the inverse of the store loop.
* **TEX -> DECLINE, latched, falling through to the existing tail** so `odata` stays 0 -- because
  its backing state is wrong until the separate index defect is fixed.  **Do not mirror the `>> 3`
  index:** a mirrored read is identity only for write-one-slot-read-it-back, since a store at `+8`
  writes cells [1..4] and one at `+16` writes [2..5].
* **MTE stays out:** different function, different trigger, different option-set member, different
  detector.

## 5.  QUESTIONS

**Q1.  Is the five-ACCEPT + TEX-DECLINE split right, or should the round wait for the TEX index fix
and do all six as ACCEPT?**  Note the round-scope rule: a second site joins only if it is witnessed,
in the SAME device and SAME semantic class, and covered by the SAME detector with no new oracle.
**Does a TEX decline satisfy "same detector, no new oracle", given its oracle is a decline channel
and the other five are round-trip values?**

**Q2.  What is the exact packing for the read side of each window, and what is the smallest edit to
it that still passes a round-trip row?**  Consider partial packing, index off-by-one, and a window
bound moved so the access falls into the catch-all instead.

**Q3.  PREMISE AUDIT.**  Which of C1-C5 is wrong?  **C2 and C4 are the ones I am least sure of** --
C2 rests on reading an `if/else if/else` chain as an exact negation, and C4 on which probe is
committed.  Also: is there a SEVENTH window or an arm I have miscounted?

**Verdict line first** -- one line naming the round you would run -- then the body.  **A verdict that
merely agrees is the least useful reply**; if you find nothing wrong, say what you CHECKED and how.
