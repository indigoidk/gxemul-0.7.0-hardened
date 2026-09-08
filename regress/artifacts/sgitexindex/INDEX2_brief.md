# sgitexindex -- the one-character fix that would have added an OUT-OF-BOUNDS WRITE

**PLEASE DO NOT RATIFY.**  I proposed a one-character fix here with three independent derivations
agreeing, and a reviewing seat showed it would introduce a memory-safety defect.  **The premises
below are that seat's, re-verified by me** -- check them too: a correction carries more authority
than the error it replaces, which makes it exactly the thing to re-test.

**Tree under review: `GXEMUL-SEC/src/`.**  Other `src/` copies under the project root are pristine
2021 upstream.

---

## 1.  THE TWO ARMS

TEX, which indexes with `>> 3`:

```c
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
```

Its sibling TLB_A, structurally identical, indexing with `>> 1`:

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
```

`_B` and `_C` match TLB_A.  **TEX is the only arm shifting by 3.**

## 2.  SETTLED PREMISES -- each MEASURED or read on this machine

* **S1.  The reachable-cell counts.**  `re_tex` is `uint16_t[112]`; the window `[CRIME_RE_TEX,
  +0xe0)` is 224 bytes = exactly 112 halfwords.  Enumerated over the 28 aligned stores, each
  writing FOUR consecutive cells:

        >> 3 (today)   starting indices 0..27, cells 0..30 touched  ->  31 reachable, 81 NOT
        >> 1           starting indices 0..111, cells 0..111        ->  all 112, no overlap

  With `>> 3` consecutive stores OVERLAP BY THREE (`+0` writes [0..3], `+8` writes [1..4]).
* **S2.  `>> 3` IS NOT ARBITRARY -- it matches the hardware's REGISTER numbering.**  The SGI CRIME
  specification lists `TLB.tex[28]` as **28 separate 64-bit registers**, followed by the clip-ID
  registers.  For byte offset `o` the register is `o/8`; its first cell in a FLAT `uint16_t[112]` is
  `4*(o/8)` = `o/2`.  **So the defect is a MISSING FACTOR OF FOUR between register number and
  backing-cell number** -- `>> 3` would be right for `uint64_t[28]` or `uint16_t[28][4]`, and is
  wrong for a flat array incremented once per halfword.
* **S3.  *** THE ISOLATED SHIFT REPLACEMENT INTRODUCES AN OOB WRITE.  MEASURED. ***  An 8-byte
  LENGTH does not establish 8-byte ALIGNMENT.  Enumerated over EVERY offset in the window, not just
  the aligned ones:

        >> 3 (today)   worst cell index  30   IN BOUNDS
        >> 1           worst cell index 114   *** OOB on uint16_t[112] ***

  Offset `0xdf` starts at 111 and writes 111..114.  **And `& 0xff` cannot help: 111 is already
  inside the mask.**
* **S4.  The unaligned access is REACHABLE.**  The device callback does not enforce alignment; the
  arm relies on CPU-side mechanisms, and the DEBUGGER bypasses them -- `debugger_cmds.c:1549` prints
  *"WARNING: address isn't aligned"* and **continues**.  (`pcc2widthkills` measured that same
  operator path for `put h`.)
* **S5.  `re_tex` has NO FUNCTIONAL CONSUMER** -- declaration, this store, a `debug()` print.  So
  correcting the shift changes NOTHING observable to a guest today, and the read path is a separate
  row's `fatal()+exit(1)`.  *The 81 cells are unreachable through TEX WRITES; they are NOT
  uninitialised -- the constructor zeroes the array.*

## 3.  THE PROPOSED FIX -- `>> 1` PLUS A BOUNDS POLICY, not `>> 1` alone

The detector proposed is a HOST-SIDE DIFFERENTIAL: execute the production handler against a fixture
and inspect the private state, the pattern `regress/diff_rtc_range.c` already uses.  It would write
distinct halfwords into neighbouring aligned registers and require both groups to survive; exercise
all 28 registers against an independently specified expected sequence; and **fail with the original
shift restored AND with writes suppressed** (floor clauses (b) and (a)).

## 4.  QUESTIONS

**Q1 (THE ONE THAT DECIDES THE ROUND).  What is the right BOUNDS POLICY?**  Candidates: clamp the
index; reject a misaligned `relative_addr` with a latched announce (the house idiom); mask the index
to `112 - 4`; or compute the count from the remaining space.  **Each has a different failure mode
for a legitimate aligned store at the window's top** -- say which and why, and note the option-set
rule: if the fork already has an idiom for this, it beats invention.

**Q2.  Is the host-side differential the right detector, given S5?**  It establishes backing-store
mapping coverage and NOT guest behaviour, so the witness stays `none` and the ladder's `detector:`
term applies.  **Is that honest, or is it a fix shipping with a detector that cannot observe the
thing the fix is for?**

**Q3.  PREMISE AUDIT.**  Which of S1-S5 is wrong?  **S2 is the one I would attack** -- it rests on a
specification I have not opened myself, cited by one seat.

**Verdict line first** -- FIX-WITH-BOUNDS-POLICY / FIX-DOCUMENTED-ONLY / LEAVE-ALONE -- then the
body.  **A verdict that merely agrees is the least useful reply.**
