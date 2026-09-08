# sgitexindex -- a shift that makes 81 of 112 backing cells unreachable

**PLEASE DO NOT RATIFY.**  The arithmetic below is mine and I would rather have it refuted than
agreed with.  **Check the premises, not just the derivations**, and say plainly if the packet cannot
settle something.

**Tree under review: `GXEMUL-SEC/src/`.**

---

## 1.  THE TWO ARMS, side by side

The TEX arm, which uses `>> 3`:

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

Its sibling TLB_A, structurally identical, which uses `>> 1`:

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

The other two TLB arms (`_B`, `_C`) match TLB_A.  **TEX is the only one shifting by 3.**

## 2.  MY DERIVATION -- attack this

* `re_tex` is declared `uint16_t re_tex[112]`.
* The TEX window is `[CRIME_RE_TEX, CRIME_RE_TEX + 0xe0)` -- **224 bytes, which is EXACTLY 112
  halfwords.**  So the array size and the window size agree under a `>> 1` index and under nothing
  else.
* With `>> 3`: offsets `0..0xdf` give starting indices `0..27`, and each 8-byte store writes FOUR
  consecutive cells (`tlbi++` in the loop).  So a store at `+0` writes `[0..3]`, one at `+8` writes
  `[1..4]`, one at `+0x10` writes `[2..5]` -- **consecutive aligned stores OVERLAP BY THREE**, and
  the highest cell ever written is `27 + 3 = 30`.  **31 cells touched, 81 unreachable.**
* With `>> 1`: offsets `0..0xdf` give `0..111`, a store at `+0` writes `[0..3]`, one at `+8` writes
  `[4..7]` -- **contiguous, no overlap, full coverage** -- which is precisely what the three TLB
  arms do.

## 3.  THE COMPLICATION, and it is why this row is rated LOW

**`re_tex` has NO FUNCTIONAL CONSUMER.**  Searching the tree finds the declaration, this store, and
a `debug()` print -- nothing reads it to produce emulated behaviour.  The read path is currently a
`fatal()` + `exit(1)` (a separate row).

**So correcting the shift changes NO OBSERVABLE GUEST BEHAVIOUR TODAY.**

## 4.  QUESTIONS

**Q1.  Is `>> 1` right?**  I am reasoning from the sibling arms and from `0xe0 == 112 * 2`.  **Is
there a reading under which `>> 3` is correct** -- e.g. a texture format where one 8-byte store is
meant to fill one logical entry, making 28 entries of 4 halfwords each the intended structure and
`[112]` the coincidence?  If so my whole framing is wrong.

**Q2 (THE HARD ONE).  What DETECTOR can a fix ship with, given zero consumers?**  A round-trip row
needs a read path, and the read path currently terminates the host.  The options I see are all
unattractive: (a) fix the read arm first, which is a different row's work; (b) score the `debug()`
print, which is a diagnostic and not a behaviour; (c) ship documented-only with no detector.
**Which is right, and is there an option I have not named?**  Note this project's rule that a fix
shipping with a vacuous detector is worse than one shipping with none, because the record then
claims coverage it does not have.

**Q3.  PREMISE AUDIT.**  Which claim in section 2 is wrong?  The overlap-by-three figure and the
31/81 split are the ones I would attack first -- they depend on my reading of the `tlbi++` loop.

**Verdict line first** -- FIX-WITH-DETECTOR / FIX-DOCUMENTED-ONLY / LEAVE-ALONE, and if you say
LEAVE-ALONE say what would change your mind.  **A verdict that merely agrees is the least useful
reply.**
