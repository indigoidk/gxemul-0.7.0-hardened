# PASS 1 DESIGN BRIEF — `sgimtedepth4dead`
## A comparison in `do_mte_transfer()` tests a bit-count against a byte-count, so its branch never runs

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable values — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

### If you can read files
Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`** — they are bulk
historical records, they are not evidence for this question, and reading them wastes the run.

---

## 0. HAS THIS ROUND ALREADY SHIPPED?  No.

`grep -n '#509' src/devices/dev_sgi_re.c` returns nothing.  The most recent correction tags
in this file are `#505` (an RGB read that took the wrong buffer bytes) and `#499`.  The
comparison discussed below is unmodified upstream text.

---

## 1. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled by the design work of 2026-09-07 and by a probe that has now been RUN.  Warrants
given inline; every one is a file reading or a measurement, not an argument.

* **`depth` in `do_mte_transfer()` is a count of BITS, and its only possible values are
  8, 16, 32 and 64.**  Warrant: `int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);`
  with `MTE_MODE_DEPTH_MASK 0x00000300` and `MTE_DEPTH_SHIFT 8` — a two-bit field, so the
  shift amount is 0..3 and `depth` is `8<<0 .. 8<<3`.
* **The header defines only three depth encodings.**  `MTE_DEPTH_8 0`, `MTE_DEPTH_16 1`,
  `MTE_DEPTH_32 2` in `src/include/thirdparty/crmfbreg.h`.  **There is no `MTE_DEPTH_64`** —
  field value 3 is undefined by the header while the code still computes 64 for it.
* **The author knew `depth` was in bits two lines earlier.**  `x1 /= (depth / 8);` and
  `src_x1 /= (depth / 8);` convert a bit count to a byte count in the same block.
* **`horrible_getputpixel()`'s colour-format arm is selected by `mode & DE_MODE_TYPE_MASK`,
  and `DE_MODE_TYPE_CI` is 0.**  So a `mode` word with no type bits set selects CI.
* **The two format arms differ in WHICH BYTE of the colour lands at the lowest address:**
  CI writes `buf[0] = *color` (the low byte); RGBA writes `buf[0] = *color >> 24` (the high
  byte).  Both are inlined verbatim in §3 below.
* **The transfer moves `bufdepth = 1 << ((mode >> 8) & 3)` bytes** via one `memory_rw` call,
  and `buf` is declared `uint8_t buf[8];` with no initialiser.
* **MEASURED, this session, on the committed build:** a rung-3 probe drives a real guest
  store sequence through real CRIME decode on an unmodified `-E sgi -e ip32` and reads the
  destination back.  Result `5/6`: five controls green, and the row asserting the correct
  destination byte FAILS with `got=0x44 want=0x11`.  The full row list is in §4.

---

## 2. THE CLAIM, STATED AS A QUESTION

I believe `if (depth == 4)` at the marked line below is **unreachable**, because `depth` is a
bit count that can only be 8/16/32/64.  **Is that true?**  Enumerate the four values rather
than agreeing with me.

If it is true, three things follow, and I would like each checked rather than accepted:

1. The two `|= DE_MODE_TYPE_RGBA` assignments never execute, so `src_mode` and `dst_mode`
   always carry type `CI` for tiled MTE operations.
2. At `MTE_DEPTH_32` the CI arm assigns exactly one byte of an eight-byte automatic array and
   the transfer then copies **four**, so three bytes of whatever the stack held are written
   into guest memory.
3. The comment immediately above the comparison states the intended condition in plain
   words: *"this makes sure that we copy 32 bits when doing 32-bit transfers."*

---

## 3. THE FULL ENCLOSING FUNCTION, AND THE HELPER IT CALLS

**`do_mte_transfer()`, `src/devices/dev_sgi_re.c` — head through the end of the tiled arm.**
The line under discussion is marked `<<<< THE LINE`.

```c
void do_mte_transfer(struct cpu* cpu, struct sgi_re_data *d)
{
	uint32_t mode = d->mte_reg[(CRIME_MTE_MODE - 0x3000) / sizeof(uint32_t)];
	uint32_t src0 = d->mte_reg[(CRIME_MTE_SRC0 - 0x3000) / sizeof(uint32_t)];
	uint32_t src1 = d->mte_reg[(CRIME_MTE_SRC1 - 0x3000) / sizeof(uint32_t)];
	uint32_t dst0 = d->mte_reg[(CRIME_MTE_DST0 - 0x3000) / sizeof(uint32_t)];
	uint32_t dst1 = d->mte_reg[(CRIME_MTE_DST1 - 0x3000) / sizeof(uint32_t)];
	int32_t src_y_step = d->mte_reg[(CRIME_MTE_SRC_Y_STEP - 0x3000) / sizeof(uint32_t)];
	int32_t dst_y_step = d->mte_reg[(CRIME_MTE_DST_Y_STEP - 0x3000) / sizeof(uint32_t)];
	uint32_t dstlen = dst1 - dst0 + 1, fill_addr;
	unsigned char zerobuf[4096];
	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
	int src = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
	uint32_t bytemask = d->mte_reg[(CRIME_MTE_BYTEMASK - 0x3000) / sizeof(uint32_t)];
	uint32_t bg = d->mte_reg[(CRIME_MTE_BG - 0x3000) / sizeof(uint32_t)];

	debug("[ sgi_mte: STARTING: mode=0x%08x src0=0x%08x src1=0x%08x src_y_step=%i dst0=0x%08x,"
	    " dst1=0x%08x dst_y_step=%i bg=0x%x bytemask=0x%x ]\n",
	    mode, src0, src1, src_y_step, dst0, dst1, dst_y_step, bg, bytemask);

	if (dst_y_step != 0 && dst_y_step != 1 && dst_y_step != -1) {
		fatal("[ sgi_mte: TODO! unimplemented dst_y_step %i ]", dst_y_step);
		// exit(1);
	}

	if (mode & MTE_MODE_STIPPLE) {
		fatal("[ sgi_mte: unimplemented MTE_MODE_STIPPLE ]");
		exit(1);
	}

	int src_tlb = (mode & MTE_MODE_SRC_BUF_MASK) >> MTE_SRC_TLB_SHIFT;
	int dst_tlb = (mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT;

	if (src > MTE_TLB_C) {
		fatal("[ sgi_mte: unimplemented SRC ]");
		exit(1);
	}

	switch (dst_tlb) {
	case MTE_TLB_A:
	case MTE_TLB_B:
	case MTE_TLB_C:
		// Used by NetBSD's crmfb_fill_rect. It puts graphical
		// coordinates in dst0 and dst1.
		{
			int x1 = (dst0 >> 16) & 0xfff;
			int y1 = dst0 & 0xfff;
			int x2 = (dst1 >> 16) & 0xfff;
			int y2 = dst1 & 0xfff;
			x1 /= (depth / 8);
			x2 /= (depth / 8);

			int src_x1 = (src0 >> 16) & 0xfff;
			int src_y1 = src0 & 0xfff;
			// int src_x2 = (src1 >> 16) & 0xfff;
			// int src_y2 = src1 & 0xfff;
			src_x1 /= (depth / 8);
			// src_x2 /= (depth / 8);

			int dx = x1 > x2 ? -1 : 1;
			int dy = y1 > y2 ? -1 : 1;

			uint32_t src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
			uint32_t dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);

			// Hack. The MTE perhaps doesn't deal with colors per se,
			// but this makes sure that we copy 32 bits when doing 32-bit
			// transfers.
			if (depth == 4) {                          /*  <<<< THE LINE  */
				src_mode |= DE_MODE_TYPE_RGBA;
				dst_mode |= DE_MODE_TYPE_RGBA;
			}

			int src_y = src_y1;
			for (int y = y1; y != y2+dy; y += dy) {
				int src_x = src_x1;

				for  (int x = x1; x != x2+dx; x += dx) {
					if (mode & MTE_MODE_COPY) {
						horrible_getputpixel(0, cpu, d,
							src_x, src_y, &bg, src_mode);
						src_x += dx;
					}

					horrible_getputpixel(1, cpu, d, x, y, &bg, dst_mode);
				}

				src_y += dy;
			}
		}
		break;
	case MTE_TLB_LIN_A:
	case MTE_TLB_LIN_B:
		/*  ... a separate linear arm, NOT touched by this round.  It rejects
		    MTE_MODE_COPY and rejects any depth other than 8, both with a
		    terminating call, before doing a page-walked memset.  ...  */
```

**The helper's two relevant arms, `horrible_getputpixel()` in the same file.**  `put` is 1
for a write, 0 for a read; `color_mode` is `mode & DE_MODE_TYPE_MASK`.

```c
	uint8_t buf[8];		/* #100: bufdepth can be 8 = 1<<((mode>>8)&3) */
	if (put) {
		switch (color_mode) {
		case DE_MODE_TYPE_CI:
			buf[0] = *color;
			break;
		case DE_MODE_TYPE_RGB:
			buf[0] = *color >> 24;
			buf[1] = *color >> 16;
			buf[2] = *color >> 8;
			buf[3] = 0;
			break;
		case DE_MODE_TYPE_RGBA:
			buf[0] = *color >> 24;
			buf[1] = *color >> 16;
			buf[2] = *color >> 8;
			buf[3] = *color;
			break;
		...
		}
		cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
		    buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
	} else {
		cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
		    buf, bufdepth, MEM_READ, NO_EXCEPTIONS | PHYSICAL);
		switch (color_mode) {
		case DE_MODE_TYPE_CI:
			*color = buf[0];
			break;
		...   /*  RGBA reads back all four bytes, high byte first  */
		}
	}
```

and near the top of the same helper:

```c
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;
	int bufdepth = 1 << ((mode >> 8) & 3);
	uint32_t tlb_mode = (mode >> 10) & 0x7;
	int linear = tlb_mode > 3;
	int tilewidth_in_pixels = 512 / bufdepth;
	int xofs = (x % tilewidth_in_pixels) * bufdepth;
	int ofs = 512 * y + xofs;
```

The relevant header constants, verbatim:

```
#define MTE_MODE_DST_BUF_MASK	0x0000001c      MTE_TLB_A 0  MTE_TLB_B 1  MTE_TLB_C 2
#define MTE_DST_TLB_SHIFT 2                     MTE_TLB_LIN_A 4  MTE_TLB_LIN_B 5
#define MTE_MODE_SRC_BUF_MASK	0x000000e0      MTE_SRC_TLB_SHIFT 5
#define MTE_MODE_DEPTH_MASK	0x00000300      MTE_DEPTH_8 0  MTE_DEPTH_16 1  MTE_DEPTH_32 2
#define MTE_DEPTH_SHIFT 8                       (no MTE_DEPTH_64 is defined)
#define MTE_MODE_STIPPLE	0x00000400
#define MTE_MODE_COPY		0x00000800	/* 1 - copy, 0 - clear dst */
#define DE_MODE_TYPE_CI		0x00000000
#define DE_MODE_TYPE_RGB	0x00000010
#define DE_MODE_TYPE_RGBA	0x00000020
#define DE_MODE_TYPE_MASK	0x000000f0
```

---

## 4. THE WITNESS THAT HAS ALREADY BEEN RUN

`regress/sgi_mte_fill_probe.py`, on the committed build, machine `sgi/ip32`.  The guest is a
short instruction sequence written into RAM with the cold debugger and single-stepped: it
programs one tile-table entry, writes the MTE mode/background/destination registers, and the
final write carries the transfer-start address bit.  A later load reads the destination back.

```
row          got            want             note
live         0x5a5a5a5a     0x5a5a5a5a       LIVENESS: guest store then load, through RAM         ok
devsig       0x1e000000     0x1e000000       DEVSIG: CRIME_DE_STATUS reads 0x1e000000; RAM reads 0 ok
paint ok     0x99           0x99             CONTROL: the paint really lands AT the oracle address ok
fill alive   alive          alive            CONTROL: the host survives a tiled 32-bit fill       ok
fill ran     yes            yes              CONTROL: dest[0] is 0x44 (CI) or 0x11 (RGBA)         ok
fill top     0x44           0x11             dest[0] must be bg>>24 (RGBA), not (uint8_t)bg       FAIL

MTEFILL_RESULT=5/6
```

The background register holds `0x11223344`, four distinct bytes, so the destination's first
byte names which arm ran: `0x44` is the CI arm's low byte, `0x11` would be the RGBA arm's
high byte.  Only the first byte is asserted — the other three are the uninitialised ones and
**must not** be an oracle.

**Two channels were considered and rejected before this one; please check the reasoning:**
* A **pre-painted tail** does not work.  CI does not replicate or preserve — it writes one
  byte and the copy overwrites the rest with stack contents, so "the tail is still painted"
  is false both before and after any fix.
* A **copy** cannot show the difference at all.  With both arms CI the destination's first
  byte is the source's first byte; with both arms RGBA it is *also* the source's first byte.
  The first byte is the one CI already gets right.

---

## 5. THE PROPOSED CHANGE, AND THE OPTION SET I CAN SEE

**F1 (proposed): `if (depth == 4)` becomes `if (depth == 32)`.**  One token.  It is what the
comment says, and `depth == 32` is exactly the encoding whose `bufdepth` is 4.

Alternatives I considered and did not choose — **please tell me if there is a member I have
not named, and grep the fork for an existing idiom before answering:**

* **F2 `depth >= 32`** — would also catch the undefined field value 3 (`depth == 64`).  But at
  64 the copy length is 8 while the RGBA arm assigns only four bytes, so this converts a
  four-byte problem into a four-byte problem at a different offset.  Rejected for want of a
  warrant, not because it is obviously wrong.
* **F3** map depth to a colour type generally (a small switch).  More invasive than the
  evidence supports.
* **F4** give `buf` an initialiser in `horrible_getputpixel()`.  This removes the
  uninitialised bytes at *every* depth but does **not** change which byte of the colour lands
  first, so the measured row stays red.  It is a different defect and I intend to file it.
* **F5** change what CI does for multi-byte pixels.  That would alter every caller of the
  helper, not just this one.

**Known and deliberately out of scope, to be filed as siblings rather than folded in:** at
`MTE_DEPTH_16` the copy length is 2 and CI still assigns one byte, so one uninitialised byte
is written; at field value 3 the copy length is 8 and seven are.  F1 fixes the 32 case only.
**Is confining the round to one cell right here, or does the panel read the three cells as one
defect that must close together?**

---

## 6. THE DETECTOR, AND THE ENUMERATION I MOST WANT CHECKED

The six rows above are the witness.  A change that survives has to be defended against edits
that would re-open it, so I intend to add rows.  **Here is my enumeration of the state space;
I think it is complete and that is exactly the kind of claim this project has got wrong
before.**

The edited comparison is dominated by: the three-way `switch (dst_tlb)` label group
(A / B / C share one block), the stipple rejection, and the source-buffer range test.  The
block the comparison guards writes two variables, `src_mode` and `dst_mode`.  The body then
reads **`src_mode` only when `mode & MTE_MODE_COPY` is set**, and `dst_mode` always.

So the cells I can see are `{A, B, C} x {copy off, copy on} x {depth 32, depth not 32}`.

**Proposed additional rows:**

| row | shape | what it pins |
|---|---|---|
| `copy top` | TLB_A, depth 32, copy ON, source pixel holds `aa bb cc dd` | that the two `|=` assignments move TOGETHER |
| `fill b top` | TLB_B, depth 32, fill | the label axis |
| `depth8 top` | TLB_A, depth 8, fill, expect `0x44` | that the change did not over-reach |

**The `copy top` row is the one I am least sure of, and here is my reasoning — please check
the arithmetic by walking the bytes rather than agreeing.**  Source pixel `aa bb cc dd`:

```
  both arms CI    (today)          read gives 0xaa;          write puts 0xaa first  -> 0xaa
  both arms RGBA  (after F1)       read gives 0xaabbccdd;    write puts 0xaa first  -> 0xaa
  source RGBA only                 read gives 0xaabbccdd;    write puts 0xdd first  -> 0xdd
  dest   RGBA only                 read gives 0xaa;          write puts 0x00 first  -> 0x00
```

If that is right, a row wanting `0xaa` is green today AND green after the change — it
distinguishes neither — but it goes red under either one-sided edit.  **That is the point of
it, and I want to know whether it is a legitimate row or a self-satisfying one.**

Four edits I have already designed, which I would like CHECKED rather than replaced:

```
  E1  depth == 32   ->  depth == 4          (the original text restored)
  E2  delete  dst_mode |= DE_MODE_TYPE_RGBA;
  E3  delete  src_mode |= DE_MODE_TYPE_RGBA;
  E4  depth == 32   ->  depth == 32 && (mode & MTE_MODE_COPY)
```

I predict E1, E2 and E4 turn `fill top` red, and that **E3 is invisible to every row in the
six-row witness**, because a fill never reads `src_mode`.  E3 is why `copy top` exists.
**Is that prediction right, and is E3 the only edit of its kind?**

---

## 7. QUESTIONS

1. **The premise audit.**  Is `depth` really confined to `{8, 16, 32, 64}`?  Is the branch
   really unreachable?  Is the comment's stated intent really `32`?  Is my claim that
   `depth == 32` and `bufdepth == 4` are the same condition correct?  **Say which of my
   premises you could not settle from this packet.**
2. **The smallest change that re-opens this and still passes the six rows.**  Name the row
   you expect to stay green.  *(Codex seat: skip this one — answer 1, 3 and 4 instead, and
   CHECK my E1–E4 above rather than proposing new ones.)*
3. **Option-set completeness on the change itself.**  Is there a disposition F1–F5 does not
   contain?  Grep the fork for how it handles a bit-count/byte-count confusion elsewhere.
4. **Scope.**  Three depth cells are broken and F1 fixes one.  Is one round per cell right,
   or is that three passes of the same class — which this project has been bitten by?

If, while verifying a claim, you found something ELSE — say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
