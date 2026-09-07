# PASS 1 DESIGN BRIEF — `sgirebufuninit`: `horrible_getputpixel()` never initialises `buf[8]`, and the guest chooses how many of its bytes are used

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
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. §C0 — HAS THIS ROUND ALREADY SHIPPED?  Commands run, outputs pasted.

    $ git log -1 --format='%h %ad %s' --date=short -- src/devices/dev_sgi_re.c
    840f3d0 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one

    $ grep -c 'sgirebufuninit' CHANGELOG.md
    0

    $ ls regress/ | grep -i sgi_re
    sgi_re_randompixel_probe.py
    sgi_re_unmapped_probe.py
    sgi_re_width_probe.py

**Not shipped.**  Three sibling probes exist and all three run in `gate_arm.sh`; none of them
programs a mismatched depth field, so none of them can see this.

*** BUT TWO PRIOR ROUNDS TOUCHED THIS EXACT CODE, AND THAT IS THE MOST IMPORTANT PREMISE IN
THIS BRIEF — PLEASE ATTACK IT. ***  Verbatim from `CHANGELOG.md`:

    ## #95 — central uninit-leak fix (Phase A) + #96-#100 (Phase B new-surface audit)
    **#95 `cpus/memory_rw.c`** (root-cause): zero the caller's buffer on every device READ before the
    len-clamp/dispatch, so a device handler that fills only part of `data` - or whose access is len-clamped -
    can never return uninitialised host memory to the guest. Closes the whole class (cf. per-device #91/93/94).

    | `devices/dev_sgi_re.c` | #100 | `buf[4]`->`buf[8]` (bufdepth up to 8 stack overflow) + bound `tile_nr < 256` (re_tlb index) |

So: **`#95` claims to close "the whole class" of uninitialised-host-memory leaks, and `#100`,
in the same batch, edited THIS ARRAY.**  My claim is that two live members of that class
survive in the function `#100` edited.  If that is wrong I want to know now, not after a
round.  See Q1.

## 2. SETTLED PREMISES: none carried — first brief of this campaign.

The `sgirandompixel` campaign that just closed is a DIFFERENT arm of the same function and
settled nothing this brief's questions depend on.  One fact from it is inlined below as
context, not as a settled premise: that round changed the `default:` arm of the `tlb_mode`
switch, which is a different switch from the `color_mode` one at issue here.

## 3. THE CLAIM, stated as precisely as I can make it

`horrible_getputpixel()` declares

    uint8_t buf[8];		/* #100: bufdepth can be 8 = 1<<((mode>>8)&3) */

and **never initialises it.**  There is no `memset`, no initialiser, and (verified by grep)
the only `memset` calls in `dev_sgi_re.c` are on the device struct, on `rop_used`, and on
`zerobuf` — none of them on `buf`.

Two fields decide how much of `buf` is used.  They are decoded from the SAME guest-written
mode word and are **independent of each other**:

    uint32_t color_mode = mode & DE_MODE_TYPE_MASK;      /* bits 4-7  */
    int bufdepth = 1 << ((mode >> 8) & 3);               /* bits 8-9 -> 1, 2, 4 or 8 */

From `src/include/thirdparty/crmfbreg.h`, inlined so you need not open it:

    #define DE_MODE_TYPE_CI		0x00000000
    #define DE_MODE_TYPE_RGB	0x00000010
    #define DE_MODE_TYPE_RGBA	0x00000020
    #define DE_MODE_TYPE_ABGR	0x00000030
    #define DE_MODE_TYPE_YCRCB	0x000000f0
    #define DE_MODE_TYPE_MASK	0x000000f0

**The colour arm decides how many bytes are FILLED; `bufdepth` decides how many are
TRANSFERRED.  Nothing makes them agree.**  `grep -rn '>> *8) *& *3' src/devices/` returns only
the decode itself, the `#100` comment, and the two XFER siblings — **no guard anywhere.**

### 3a. THE TWO PATHS.  Members enumerated, per §C4 — I am claiming exactly two.

**PATH A — PUT: uninitialised host stack written INTO guest-visible memory.**

| `color_mode` | bytes the arm assigns | assigned by nothing |
|---|---|---|
| `CI` (0x00)   | `buf[0]`      | `buf[1..7]` |
| `RGB` (0x10)  | `buf[0..3]`   | `buf[4..7]` |
| `RGBA` (0x20) | `buf[0..3]`   | `buf[4..7]` |
| `ABGR` (0x30) | `buf[0..3]`   | `buf[4..7]` |
| default (incl. `YCRCB` 0xf0) | `buf[0..3]` = `random()` | `buf[4..7]` |

then unconditionally:

    cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
        buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);

**With the depth field = 3 (`bufdepth` 8), NO colour arm writes `buf[4..7]` — not one of the
five, including the four correct ones — and all eight bytes are written.**  `CI` leaks at any
depth above 1.

**PATH B — GET: uninitialised host stack into `*color`, which the caller then STORES.**

    cpu->memory_rw(cpu, cpu->mem, tileptr + ofs,
        buf, bufdepth, MEM_READ, NO_EXCEPTIONS | PHYSICAL);
    switch (color_mode) {
    ...
    case DE_MODE_TYPE_RGBA:
        *color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3];

The read fills `bufdepth` bytes; the combine reads four.  **Depth field 0 (`bufdepth` 1) with
`RGBA` reads ONE byte from memory and builds a 32-bit colour out of four.**  `draw_primitive()`
then writes that colour to the destination in the same loop iteration — **the identical
caller-consumes-a-failed-read shape the `sgirandompixel` round just fixed one arm of**, reached
here with every colour mode documented and implemented and no undocumented value anywhere.

### 3b. WHY I BELIEVE `#95` DOES NOT COVER EITHER — please check this hardest

`#95` zeroes the caller's buffer **on every device READ**, for `len` bytes.

* **Path A is a `MEM_WRITE`.**  A read-side pre-zero cannot apply to it at all.
* **Path B is a `MEM_READ` of `bufdepth` bytes**, so `#95` zeroes `buf[0 .. bufdepth-1]`.  The
  bytes the combine then reads *beyond* `bufdepth` are outside `len` and untouched.

**If either of those is wrong the round is dead and I want it dead now.**

### 3c. Severity, stated honestly rather than at its most alarming

In a drawing loop the stale bytes are usually the PREVIOUS pixel's, so the everyday symptom is
**wrong colours / non-deterministic output**, not a dramatic host-secret disclosure.  On the
first call in a frame they are whatever the host stack held.  I am claiming a guest-reachable
uninitialised read whose value becomes guest-visible — **not** that it is a practical
exfiltration channel, and I would rather a seat talked me DOWN than up.  Both mode words are
ordinary device registers reached by ordinary stores, and all seven call sites pass one of them.

## 4. THE FULL ENCLOSING FUNCTION, verbatim (§D)

Frozen at `regress/artifacts/sgirebufuninit/enclosing_function.txt`, which is the version under
review.  Every exit path is present, including the early returns and the common tail.

```c
void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
	int x, int y, uint32_t* color, int mode)
{
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;
	int bufdepth = 1 << ((mode >> 8) & 3); 

	// dst_mode (see NetBSD's crmfbreg.h):
	// #define DE_MODE_TLB_A           0x00000000
	// #define DE_MODE_TLB_B           0x00000400
	// #define DE_MODE_TLB_C           0x00000800
	// #define DE_MODE_LIN_A           0x00001000
	// #define DE_MODE_LIN_B           0x00001400
	uint32_t tlb_mode = (mode >> 10) & 0x7;
	int linear = tlb_mode > 3;

	if (!linear && (x < 0 || y < 0 || x >= 2048 || y >= 2048))
		return;

	int tilewidth_in_pixels = 512 / bufdepth;
	
	int tile_nr_x = x / tilewidth_in_pixels;
	int tile_nr_y = y >> 7;

	unsigned int tile_nr = tile_nr_y * 16 + tile_nr_x;

	y &= 127;
	int xofs = (x % tilewidth_in_pixels) * bufdepth;
	int ofs = 512 * y + xofs;

	uint32_t tileptr = 0;

	/*  #100: cases 0-2 index re_tlb_[abc][256] with a guest-derived
	    tile_nr = (y>>7)*16 + x/tilewidth; bound it (case 4 self-checks).  */
	if (tlb_mode <= 2 && tile_nr >= 256)
		return;

	switch (tlb_mode) {
	case 0:	tileptr = d->re_tlb_a[tile_nr] << 16;
		break;
	case 1:	tileptr = d->re_tlb_b[tile_nr] << 16;
		break;
	case 2:	tileptr = d->re_tlb_c[tile_nr] << 16;
		break;
	case 4:	tile_nr = x >> 12;
		if (tile_nr >= 32)
			return;
		tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12);
		ofs = x & 4095;
		// TODO... probably not correct!
		// printf("tileptr = %08x x = %i y = %i tile_nr = %i ofs = %i\n", tileptr, x, y, tile_nr, ofs);
		break;
	default:/*  sgirandompixel: this arm used to assign `*color = random()' -- with
		    its exit(1) commented out -- so a failed GET handed the CALLER a
		    random value, and draw_primitive() then wrote it to the destination
		    in the same loop iteration, since `color' is shared by the XFER GET
		    and the PUT.  DE_MODE_LIN_B (0x1400) is one of the FIVE modes
		    crmfbreg.h documents and extracts to tlb_mode 5, so this was
		    reachable with a DOCUMENTED mode, not only with a junk one.
		    MEASURED, rung 3: the destination received 0x4b1763a1, 0x2ee4b4df
		    and 0x7433cdc1 on successive runs of
		    regress/sgi_re_randompixel_probe.py.

		    NOW DECLINED: `*color' is left alone, so the caller's own
		    `uint32_t color = fg' stands and what lands is at least
		    DETERMINISTIC.  The announce is latched because this helper is
		    per-pixel.

		    WHAT THIS DOES NOT DO, filed rather than silently omitted: the
		    caller STILL PERFORMS its dependent PUT, so a declined GET still
		    writes fg (row sgirandomskipput -- suppressing it needs a return
		    value and every GET site changed, which is more than one site);
		    LIN_B is still not implemented, and the panel refused to endorse
		    implementing it as LIN_A-with-the-other-array on symmetry alone
		    (row sgirelinb); and the COLOUR-mode switch below carries the same
		    random() shape at its own default (row sgirandomcolour).  */
		if (!(d->warned & SGIRE_W_BADMODE)) {
			d->warned |= SGIRE_W_BADMODE;
			/*  `dst_mode' is kept from the original text although the
			    parameter is also passed as src_mode on a GET: the probe
			    anchors on this literal, and rewording it here would be
			    scope creep AND would move an oracle anchor mid-round,
			    which is the laundering shape whatever the intent.
			    Filed as sgirenamedstmode.  */
			fatal("[ sgi_re: unimplemented dst_mode %i for "
			    "horrible_getputpixel (%s), x=%i y=%i; declined "
			    "(once) ]\n", mode, put ? "put" : "get", x, y);
		}
		return;
	}

	// The highest bit seems to be set for a "valid" tile pointer.
	if (!(tileptr & 0x80000000)) {
		//printf("dst_mode %i, tile_nr = %i,  tileptr = 0x%llx\n", dst_mode, tile_nr, (long long)tileptr);
		//fatal("sgi gbe horrible_getputpixel: unexpected non-set high bit of tileptr?\n");
		//exit(1);
		return;
	}
	
	tileptr &= ~0x80000000;

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
		case DE_MODE_TYPE_ABGR:
			buf[0] = *color;
			buf[1] = *color >> 8;
			buf[2] = *color >> 16;
			buf[3] = *color >> 24;
			break;
		default:buf[0] = random();
			buf[1] = random();
			buf[2] = random();
			buf[3] = random();
			// TODO.
			fatal("[ put: color mode = 0x%x ]\n", color_mode);
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
		case DE_MODE_TYPE_RGB:
			*color = (buf[1] << 24) + (buf[2] << 16) + (buf[3] << 8);
			break;
		case DE_MODE_TYPE_RGBA:
			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3];
			break;
		case DE_MODE_TYPE_ABGR:
			*color = (buf[3] << 24) + (buf[2] << 16) + (buf[1] << 8) + buf[0];
			break;
		default:// Read "raw" 32-bit value:
			*color = (buf[3] << 24) + (buf[2] << 16) + (buf[1] << 8) + buf[0];
			fatal("[ get: color mode = 0x%x ]\n", color_mode);
		}
	}
}
```

## 5. QUESTIONS

### Q1 — THE PREMISE AUDIT.  These are stated as questions on purpose; please settle them, not ratify them.

1. **Is `buf` really uninitialised on every path?**  I claim no `memset`, no initialiser.  Is
   there an assignment I have missed — in the function, or a compiler-visible one?
2. **Is `#95`'s pre-zero really inapplicable?**  It zeroes the caller's buffer on device
   **READ** for `len` bytes.  Does it reach a `MEM_WRITE`?  Does it reach bytes at index
   >= `len`?  If it does either, PATH A or PATH B is dead.
3. **Is `tileptr + ofs` a DEVICE or is it RAM?**  If RAM, `#95` does not run at all and PATH B
   is worse than I said; if a device, the pre-zero covers `bufdepth` bytes only.  I have not
   settled this and I am not guessing.
4. **Are the two mode fields really independent?**  I claim bits 4-7 and bits 8-9 of one
   guest-written word, with no cross-check anywhere.  Is there a guard in a CALLER — in
   `draw_primitive()` or the XFER path — that constrains the pair before the call?
5. **Is depth field = 3 (`bufdepth` 8) actually reachable**, or does something upstream reject
   it?  `#100` grew the array *because* it believed 8 was reachable; that is evidence, not
   proof, and it is the premise PATH A rests on entirely.
6. **Is `DE_MODE_TYPE_YCRCB` (0xf0) genuinely unimplemented here?**  It is in the header's
   documented list and I see no `case` for it.

### Q2 — THE SMALLEST EDIT.  Name the row you expect to stay green.

Assume the fix is chosen and a detector ships with it.  **What is the smallest edit that
re-opens this defect and still passes a detector built the obvious way?**  I am especially
interested in edits that keep a `memset` but make it the wrong SIZE — `sizeof(buf)` vs
`bufdepth` vs a constant — because that is the shape a future refactor produces, and a
detector that only checks "the bytes are not stale" may not distinguish them.

### Q3 — OPTION-SET COMPLETENESS.  Grep the fork for the existing idiom.

The de-fatalisation option set does not obviously apply — nothing here is a refusal, and there
is no `exit()` to remove.  The dispositions I can name are:

1. **`memset(buf, 0, sizeof buf)` at declaration** — total, one line, and it costs a zeroing of
   8 bytes per pixel in a drawing loop.
2. **`memset(buf, 0, bufdepth)`** — covers PATH A exactly and leaves PATH B, since PATH B reads
   *beyond* `bufdepth`.
3. **Make the colour arms fill all `bufdepth` bytes** — i.e. treat the mismatch as the defect
   and pad per-arm.
4. **Decline the mismatched combination** (member 2/3: a mode whose colour type and depth
   disagree is a guest programming error) — with or without a latched announce.
5. **Clamp `bufdepth`** to what the colour mode needs.

**Is there a member I have not named?**  And which does the fork's own idiom favour — is there
an existing in-tree precedent for a device that reconciles two independent guest-chosen mode
fields?  Please grep rather than reason; the tree's precedents are part of the design space and
this project has twice found whole option-set members that way.

**Note the dispositions are NOT equivalent on observable behaviour**, which is the part I most
want checked: (1) and (2) make the guest see ZEROES, (3) makes it see a defined replication of
the colour, (4) makes it see the destination UNCHANGED, (5) makes it see a shorter transfer.
Those are five different guest-visible outcomes and I have no hardware evidence for any of
them.  **If the honest answer is "we do not know what the hardware does, so pick the one that
is not undefined behaviour and say so in the comment", say that** — it is the answer this
project has taken before and it is a legitimate one.

### Q4 — WITNESS SHAPE (the rung-3 attempt is mandatory before this can be documented-only)

`regress/sgi_re_randompixel_probe.py` already programs this exact code path on an unmodified
committed `-E sgi -e ip32`, with both mandated controls green.  Its mode word is
`MODE_LIN_A = 0x1220` = LIN_A (bits 10-12) | depth field 2 (`bufdepth` 4) | RGBA (0x20) — the
MATCHED case, which leaks nothing.

**Is `0x1020` (the same line with depth field 0) sufficient to witness PATH B?**  And what is
the ORACLE?  The difficulty I see: an uninitialised read is not guaranteed to differ from the
correct value — the stale bytes may happen to be what a correct implementation would produce,
and in a loop they are often the previous pixel's.  **A witness whose oracle is "the value is
wrong" can pass by luck.**

I think the answer is to make the stale content KNOWN rather than to hope it differs: paint a
first pixel with a distinctive colour so `buf` holds known bytes, then read a second pixel at a
mismatched depth and assert the result contains bytes from the FIRST pixel that the second
pixel's memory does not hold.  **Is that sound, and is there a simpler oracle I am missing?**

### Q5 — SEVERITY.  Please talk me down if it is warranted.

I have graded this HIGH on the ledger.  Is that right?  The argument for lower: in a drawing
loop the stale bytes are usually the previous pixel's, so the practical symptom is wrong
colours rather than disclosure.  The argument for higher: it is guest-reachable through
documented registers with no undocumented value, and `#95` was a CRITICAL-class fix whose
claim to have closed the class is what this contradicts.

**If, while verifying a claim, you found something ELSE — say so.**

## 6. THE CLASS SCAN — a denominator for "is this systemic or specific?", run before firing this panel

I scanned `src/devices/*.c` for the signature and I am giving you the WHOLE result, not just the
hits that support me.  The scanner is `/tmp/scan_len.py`, reproduced here so you can judge it:

    call = re.compile(r'memory_rw\s*\((.*?)\)\s*;', re.S)
    for each *.c:
        bufs = names declared as `unsigned char|uint8_t NAME[<literal>];`
        for each memory_rw call whose 4th arg is one of those buffers:
            skip if the 5th arg (length) is sizeof(...) or a numeric literal
            report otherwise

**Result — SIX call sites in the whole device tree where the transfer length is not pinned to
the buffer:**

    file                         line buffer       length           dir
    dev_px.c                      151 dma_buf      dma_len          MEM_READ
    dev_px.c                      265 dma_buf      dma_len          MEM_READ
    dev_sgi_gbe.c                 263 buf          len              MEM_READ
    dev_sgi_re.c                  316 buf          bufdepth         MEM_WRITE   <- PATH A
    dev_sgi_re.c                  319 buf          bufdepth         MEM_READ    <- PATH B
    dev_sgi_re.c                 1462 zerobuf      fill_len         MEM_WRITE

**FOUR OF THE SIX ARE BOUNDED, AND I CHECKED EACH RATHER THAN ASSUMING:**

* **`dev_px.c` 151/265** — `dma_buf[32768]`, `dma_len = 4 * (5 + nspans*3)` where `nspans` is
  read out of guest memory.  That looks unbounded and **is not**: `nspans >>= 24` caps it at
  255, so `dma_len <= 3080`.  The span loop advances `ofs` by 12 per span, max 3080.  The
  `DEV_PX_TYPE_PXG` branch was separately bounded by `#207`.  **Safe, by a shift that is easy
  to miss.**
* **`dev_sgi_gbe.c` 263** — `buf[16384]`, `len` clamped by `if (len > 512) len = 512;` (OB-14).
  I also checked the two ways it could go wrong underneath that clamp: `len` cannot be
  NEGATIVE (`partial_pixels` derives from `((idata >> RHS_SHIFT) & 0x1f) * 32 ...`, so it is
  non-negative), and `bytes_per_pixel`, which is used as a DIVISOR at `(len / bytes_per_pixel)`,
  **cannot be zero** because `d->bitdepth = 8 << ((...) & 3)` yields 8/16/32/64.  **Safe.**
* **`dev_sgi_re.c` 1462** — `zerobuf` is `memset` before use.  **Safe.**

**So the answer is SPECIFIC, not systemic: the only unbounded-fill sites in the device tree are
the two this brief is about.**  That cuts both ways and I want it read both ways — it means the
round is small and bounded, and it also means **I have no corroborating instance**, so if my
reading of these two is wrong there is nothing else holding the finding up.

### THE SCANNER'S OWN LIMITS, stated so you can decide what it does NOT rule out

1. It splits arguments on commas, so a call with a nested comma inside an expression argument
   is mis-parsed and **silently skipped**.
2. It only matches buffers declared with a LITERAL size in the same file — not `malloc`ed
   ones, not ones reached through a struct, not VLAs.
3. **It tests the LENGTH, not the FILL.**  A site passing `sizeof(buf)` is excluded by
   construction — yet a `sizeof(buf)` transfer of a partially-filled buffer is the same defect.
   `dev_sgi_re.c:316` would have been MISSED had it been written `sizeof(buf)`.
4. It looks only at `memory_rw`; `memmove`/`memcpy` into guest-visible storage are not covered.

**Limit 3 is the one I would most like a seat to close**, because it is the direction that
would turn a specific finding into a class — and it is the direction my scanner is blind in.
If you can cheaply enumerate the partially-filled-buffer sites, that is worth more than
anything else in this brief.

### 6b. LIMIT 3 CLOSED — the partially-filled direction, scanned too

I said above that limit 3 was the one I most wanted closed, so I closed it rather than leaving
it for you.  Second scanner (`/tmp/scan_fill.py`): every `memory_rw` that **WRITES** a stack
byte-buffer into guest-visible memory, regardless of whether the length is `sizeof`, plus
whether the buffer is ever initialised wholesale.

    file                      line function                   buffer      size len            wholesale init?
    dev_scc.c                  305 dev_scc_dma_func           word           4 sizeof(word)   NO
    dev_sgi_mec.c              200 mec_try_rx                 data          32 sizeof(data)   yes
    dev_sgi_mec.c              370 mec_try_tx                 data          32 sizeof(data)   yes
    dev_sgi_re.c               316 horrible_getputpixel       buf            8 bufdepth       NO
    dev_sgi_re.c              1462 do_mte_transfer            zerobuf     4096 fill_len       yes

**It found one site the length scanner missed BY CONSTRUCTION** — `dev_scc.c:305` passes
`sizeof(word)`, which the first scanner excludes.  That is limit 3 demonstrated on a real site
rather than argued.

**I then opened all four non-`sgi_re` sites, and all four are SAFE — including the one my own
scanner flagged:**

* **`dev_scc.c:305` — FALSE POSITIVE, my scanner's fault.**  The bytes are assigned by a
  CHAINED assignment, `word[0] = word[1] = word[2] = word[3] = rx_nextchar(d, port);`, which my
  `memset`-or-initialiser test does not recognise.  All four bytes are set.  **Safe.**
* **`dev_sgi_mec.c:200` (`mec_try_rx`) —** `memset(data, 0, sizeof(data))` on a `data[8]`, i.e.
  a full clear, before the six assignments.  **Safe.**
* **`dev_sgi_mec.c:370` (`mec_try_tx`) —** this one deserved the look.  It is
  `memset(data, 0, 6)` on a `data[32]` and then writes `sizeof(data)` = **32** bytes, so bytes
  6..31 are NOT cleared.  They are not stale stack either: the function READ the same 32 bytes
  from the same address at the top and checked the result, so this is an intentional
  read-modify-write preserving the descriptor's tail (its comment says so — *"last 2 bytes are
  len"*).  **Safe.**
* **`dev_sgi_re.c:1462` —** `zerobuf` is `memset` before use.  **Safe.**

**A SCANNER DEFECT I FOUND WHILE CHECKING, which did not change any verdict but would have:**
the `size` column reports **32** for `mec_try_rx`, whose buffer is `data[8]`.  My declaration
map is keyed by NAME across the whole FILE, so two functions declaring `data` at different
sizes collapse to whichever was parsed last.  **A size-based conclusion from that column would
have been wrong**, and I am telling you because I nearly drew one.

> **BOTH SCANS AGREE: `dev_sgi_re.c` is the only member of this class in the device tree.**
> Six unpinned-length sites, five write-a-stack-buffer sites, and after opening every one of
> them the only defective site is the one this brief is about.

**Read that as evidence about SCOPE, not as corroboration.**  It means the round is small and
its blast radius is one function — and equally that **nothing else supports the finding**, so
if my reading of `#95` in §3b is wrong, there is no second instance holding it up.  That is why
§3b is the question I most want attacked.

## 7. REACHABILITY, DERIVED FROM THE INLINED FUNCTION — and the witness is one constant

I worked the mode arithmetic rather than asserting reachability.  **Please check the three
numbers**; they are the whole witness design.

`tlb_mode = (mode >> 10) & 0x7`, so the LIN_A case (`tlb_mode == 4`) needs mode bits 10-12 =
`100b` = `0x1000`.  The depth field is bits 8-9; the colour type is bits 4-7.  Therefore:

| mode word | `tlb_mode` | depth field | `bufdepth` | `color_mode` | what it exercises |
|---|---|---|---|---|---|
| `0x1220` | 4 (LIN_A) | 2 | **4** | RGBA | the MATCHED case — what the shipped probe uses; leaks nothing |
| `0x1320` | 4 (LIN_A) | 3 | **8** | RGBA | **PATH A** — arms fill `buf[0..3]`, eight bytes written |
| `0x1020` | 4 (LIN_A) | 0 | **1** | RGBA | **PATH B** — one byte read, four combined |

**LIN_A is the right vehicle and it is not a coincidence — it is the only case that cannot be
refused.**  Cases 0-2 take `tileptr` from `re_tlb_[abc][tile_nr]` and are then subject to

    if (!(tileptr & 0x80000000))
            return;

so the guest must first arrange the valid bit.  **Case 4 FORCES it:**
`tileptr = 0x80000000 | (d->re_linear_a[tile_nr] << 12)`.  So the LIN_A path reaches the
`buf` code unconditionally, which is why `regress/sgi_re_randompixel_probe.py` already gets
there today with both mandated controls green.

**The consequence for cost: the witness is an existing, committed, gate-wired probe with ONE
CONSTANT CHANGED.**  That is why I am proposing this round now rather than filing it — it is
in the "easy resolvable" class, not because the defect is trivial but because the apparatus
already exists and is already trusted.

### The oracle problem is the real question, and I do not think I have solved it

An uninitialised read is not *guaranteed* to differ from a correct value.  In a loop the stale
bytes are usually the previous pixel's, so **an oracle of the form "the result is wrong" can
pass by luck** — which is the vacuity floor's own concern arriving before the fix exists.

My proposal, and I want it attacked rather than approved: **make the stale content KNOWN
instead of hoping it differs.**  Paint pixel 1 with a distinctive colour through the MATCHED
mode `0x1220` so `buf` demonstrably holds those bytes; then read pixel 2 at `0x1020`, where the
device supplies only `buf[0]`; then assert the resulting colour contains bytes from PIXEL 1
that pixel 2's own memory does not hold.  That is a positive identification of the leak rather
than an inequality.

**Two ways I can see it being wrong**, both of which a seat can settle faster than I can:

1. **`buf` may not survive between the two calls.**  It is a fresh stack frame each time.  The
   bytes usually persist because the frame is reused at the same depth, but *"usually"* is not
   an oracle — and a probe resting on it is a probe that passes for a reason it does not state.
   Is there a way to make the carry-over ARCHITECTURAL rather than incidental?
2. **`#95`'s pre-zero may already zero `buf[0..bufdepth-1]`** on each device read, which does
   not touch the bytes I care about — but if the destination is RAM rather than a device, no
   pre-zero runs at all, and the two cases give different stale content.  **Q1.3 above is
   therefore not a side question: it decides what the oracle can assert.**

If the honest answer is that PATH B cannot carry a deterministic oracle and only PATH A can,
say so — a round that witnesses one path and files the other with its reason is a better record
than one that claims both and proves one by luck.

### Q6 — SCOPE: is this ONE round or two?  (Added after the brief was drafted.)

Filed separately as `sgirandomcolour`, **in the same `switch` as PATH A**, is a second defect: that
switch's `default:` does `buf[0..3] = random()` and writes them.  Verified at HEAD — the switch
implements four `DE_MODE_TYPE_` cases, `crmfbreg.h` documents **five**, and
`grep -c YCRCB dev_sgi_re.c` is **0**, so the documented `YCRCB` (`0xf0`) lands there.

**They are different defects at the same lines:** `sgirebufuninit` is bytes *nobody assigns*;
`sgirandomcolour` is bytes assigned *from `random()`*. **Fixing either leaves the other standing** —
a `memset` does not stop the `default:` arm overwriting with `random()`, and removing the `random()`
does not fill `buf[4..7]`.

The reopening rule admits a second site only if it is witnessed, same device, same semantic class
so one fix design covers both, and **covered by the same detector with no new oracle**.
`sgirandomcolour` has **no witness**, so on the letter it cannot join.

**My question is whether the letter is right here.** Both make the guest receive non-deterministic
data from one function, and a single oracle — *the destination is DETERMINISTIC across runs* —
plausibly covers both. If so, one round with one detector is cheaper and leaves no half-fixed
switch. If not, say so and I will take them separately.

**Please do not let the convenience of one round drive the answer**; a shared oracle that is weaker
than two purpose-built ones is the vacuity floor's problem, not a saving.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
