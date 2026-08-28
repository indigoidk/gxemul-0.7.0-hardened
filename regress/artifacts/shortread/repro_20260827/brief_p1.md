# PASS 1 DESIGN BRIEF — `shortread`: a short read in a NON-FINAL iteration corrupts twice

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel here had **seven of nine seats confirm a premise the brief stated
wrongly** (a census that was wrong by 4x). **Check the premises, not just the
derivations.** Where I state something as fact below, ask whether it is true; where
I ask a question, it is a real one. A seat that re-derives a premise from something
this brief did NOT give it is worth more than a seat that agrees with all of them.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Ignore any other `src/` you find —
there are **three pristine-2021-upstream copies** under the project root
(`./src/`, and two under `_archive/audit-results-*/builds/`) and they are NOT this
fork. If your line numbers disagree with mine by hundreds, you are reading one of
them; say so rather than reconciling.

**If you cannot read files, that is expected** — every fact you need is inlined
below. Name any premise you cannot settle from this packet rather than guessing.

---

## 1. THE CODE, INLINED IN FULL

`src/disk/diskimage.c`, `fread_helper()` — **the entire function**, verbatim:

```c
static size_t fread_helper(off_t offset, unsigned char *buf,
	size_t len, struct diskimage *d)
{
	off_t curofs;
	size_t totallenread = 0;

	/*  Fast return-path for the case when no overlays are used:  */
	if (d->nr_of_overlays == 0) {
		int res = my_fseek(d->f, offset, SEEK_SET);
		if (res != 0) {
			fatal("[ diskimage__internal_access(): fseek() failed"
			    " on disk id %i \n", d->id);
			return 0;
		}

		return fread(buf, 1, len, d->f);
	}

	/*  Split the read into OVERLAY_BLOCK_SIZE reads:  */
	for (curofs=offset; len != 0;
	    curofs = (curofs | (OVERLAY_BLOCK_SIZE-1)) + 1) {
		/*  Find the overlay, if any, that has this block:  */
		off_t lenread, lentoread, inblock, remain;
		int overlay_nr;
		for (overlay_nr = d->nr_of_overlays-1;
		    overlay_nr >= 0; overlay_nr --) {
			if (overlay_has_block(d, overlay_nr, curofs))
				break;
		}

		/*  #472: clamp to what REMAINS in the CURRENT block, not to the
		    block size.  [...comment elided, 10 lines...]  */
		inblock = curofs & (OVERLAY_BLOCK_SIZE - 1);
		remain = OVERLAY_BLOCK_SIZE - inblock;
		lentoread = len > remain? remain : len;

		if (overlay_nr >= 0) {
			/*  Read from overlay:  */
			int res = my_fseek(d->overlays[overlay_nr].f_data,
			    curofs, SEEK_SET);
			if (res != 0) {
				fatal("[ diskimage__internal_access(): fseek()"
				    " failed on disk id %i \n", d->id);
				return 0;
			}
			lenread = fread(buf, 1, lentoread,
			    d->overlays[overlay_nr].f_data);
		} else {
			/*  Read from the base disk image:  */
			int res = my_fseek(d->f, curofs, SEEK_SET);
			if (res != 0) {
				fatal("[ diskimage__internal_access(): fseek()"
				    " failed on disk id %i \n", d->id);
				return 0;
			}
			lenread = fread(buf, 1, lentoread, d->f);
		}

		if (lenread != lentoread) {
			fatal("[ INCOMPLETE READ from disk id %i, offset"
			    " %lli ]\n", d->id, (long long)curofs);
		}

		len -= lentoread;
		totallenread += lenread;
		/*  #472: advance by what was CONSUMED.  [...comment elided...]  */
		buf += lentoread;
	}

	return totallenread;
}
```

**`OVERLAY_BLOCK_SIZE` is 512.**

Its **only** caller, `diskimage__internal_access()`, again verbatim — note the
common tail, because a proposed edit that returns early skips it:

```c
	if (writeflag) {
		if (!d->writable)
			return 0;

		lendone = fwrite_helper(offset, buf, len, d);
	} else {
		if (d->nr_of_tracks > 0)
			lendone = diskimage_access__cue(d, offset, buf, len);
		else if (d->is_a_cdrom)
			lendone = diskimage_access__cdrom(d, offset, buf, len);
		else
			lendone = fread_helper(offset, buf, len, d);

		if (lendone >= 0 && lendone < (ssize_t)len)
			memset(buf + lendone, 0, len - lendone);
	}

	/*  [...a 22-line comment saying READS may legitimately come up short and
	    still succeed -- the advertised capacity is rounded up to whole
	    cylinders, so the last 480..992 blocks of every image in this project
	    are addressable but not backed by file.  Those reads are zero-filled
	    above and stay GOOD.  WRITES may not...]  */
	if (writeflag && lendone < (ssize_t)len) {
		debugmsg(SUBSYS_DISK, "", VERBOSITY_WARNING,
		    "disk_id %i: short write at offset %lli: %i of %i bytes",
		    d->id, (long long)offset, (int)lendone, (int)len);
		return 0;
	}

	return 1;
}
```

## 2. THE DEFECT

Three lines of accounting disagree about which length they use:

```c
		len          -= lentoread;      /*  REQUESTED  */
		totallenread += lenread;        /*  ACTUAL     */
		buf          += lentoread;      /*  REQUESTED  */
```

On a short read the buffer pointer still advances by the **requested** length, so
the shortfall becomes a **HOLE at the position where it happened** and every later
iteration lands at its correct final offset. The caller then zero-fills the
**TAIL**.

**That tail zero-fill is correct only if the shortfall was at the END.** For a
short read in a non-final iteration it is wrong twice over.

## 3. HOW THE SHORT READ IS PRODUCED — a construction, not an injected failure

`diskimage_add_overlay()` opens the overlay data file and its `.map` bitmap and
**does not compare the data file's length against the image**. The bitmap alone
decides which blocks are live. So an overlay whose `.map` claims block 0 while its
data file is 200 bytes long is accepted silently.

*(A host that ran out of space while writing an overlay leaves exactly this state.
So does a user-supplied or truncated overlay. **This is NOT guest-reachable** — a
guest cannot truncate a host file — and I am not claiming it is.)*

## 4. THE MEASUREMENT — taken on the committed build BEFORE any edit

Offline differential that `#include`s the shipping `src/disk/diskimage.c` (so the
code that runs IS the code that ships). Base image 4096 bytes of `B`; overlay data
**truncated to 200 bytes of `V`**; bitmap `0x01` = block 0 only; caller buffer
pre-filled with the sentinel `X`; then one 1536-byte read at offset 0, crossing
three blocks.

```
  ok    [LIVE] truncated overlay supplies its 200 real bytes       = 200
  ok    [LIVE] a FINAL-iteration shortfall is zero-filled correctly = 0
  ok    [LIVE] bitmap discriminates: block 1 is all base           = 512
  FAIL  short read: caller bytes the read never wrote              = 312, want 0
  FAIL  short read: base bytes surviving the tail zero-fill        = 712, want 1024
  ok    short read: overlay bytes are the 200 that exist           = 200
  ok    short read: NUL fill covers exactly the unbacked hole      = 312
  ok    short read: reports success either way [CONTROL]           = 1
  ok    [ANCHOR] byte 199 is the last real overlay byte            = 86
  FAIL  [ANCHOR] byte 200 is the first unbacked byte               = 88, want 0
  ok    [ANCHOR] byte 512 is the first base byte                   = 66
  FAIL  [ANCHOR] byte 1535 is still a base byte                    = 0, want 66
66 rows, 5 failures, 0 faults
```

So: **312 stale caller bytes left in the middle, AND 312 valid base bytes destroyed
at the tail**, and the access returns 1.

**One row is worth your attention:** `NUL fill covers exactly the unbacked hole =
312` is **GREEN on the broken code**. The population of NULs is right; only their
POSITION is wrong. It is a vacuous row standing alone, and it is only the ANCHOR
rows that make the section absolute. *Is that the right reading, or should that row
be deleted rather than kept beside the anchors?*

## 5. THE OPTION SET — four members, and I want the set audited before the choice

I am deliberately listing four because a two-membered framing recently cost this
project two rounds of argument about an option nobody had named. **If there is a
fifth, name it.** In particular: **is there an existing idiom in this fork for
validating a companion file's length at open time?** I have not grepped for one.

**A — STOP THE LOOP.** `buf += lenread; len -= lenread;` and `break` on a short
read. The caller's tail memset then becomes correct by construction.
*Cost, and I think it is disqualifying: blocks after the short one are never read
at all.* On the measurement above that turns 1024 bytes of perfectly readable base
data into zeroes. It trades a wrong-position hole for a much larger data loss.

**B — ZERO-FILL THE HOLE AT ITS OWN POSITION, AND COUNT IT AS DONE.**

```c
		if (lenread != lentoread) {
			fatal("[ INCOMPLETE READ from disk id %i, offset"
			    " %lli ]\n", d->id, (long long)curofs);
			memset(buf + lenread, 0, lentoread - lenread);
		}

		len -= lentoread;
		totallenread += lentoread;     /*  was: += lenread  */
		buf += lentoread;
```

Two lines. It does at the RIGHT position exactly what the caller was already trying
to do at the wrong one. Result on the measurement: 200 `V`, 312 NUL, 1024 `B`.

*The consequence I want challenged:* `fread_helper()` would then always return
`len` on the overlay path, so the caller's `lendone < len` memset becomes dead
**for that path** (it stays live for the no-overlay fast path, which still returns
a short `fread`). **Is making a caller's guard unreachable-on-one-path acceptable,
or does it want the guard deleted / an assertion instead?**

**C — REFUSE THE WHOLE READ.** `return 0` on any short read; the caller zero-fills
everything. Fail-stop, and it discards data the disk really does have.

**D — VALIDATE AT OPEN TIME.** Make `diskimage_add_overlay()` compare the data
file's length against the image and refuse or warn. *This does not fix the
accounting* — a genuine I/O error mid-read still produces the same corruption — so
I read it as a complement, not an alternative. **Is that right?**

I lean **B**. Tell me if that is wrong.

## 6. WHAT I AM ASKING YOU FOR

1. **AUDIT THE PREMISES ABOVE**, especially: that the hole is at the position I say
   it is; that `totallenread` is read by nothing but that one caller; that no other
   consumer depends on `fread_helper` returning a short count; and that option A
   really does lose the later blocks.
2. **IS THE OPTION SET COMPLETE?** Name a fifth member if there is one.
3. **THE SMALLEST EDIT THAT BREAKS FIX B AND STILL PASSES THE ROWS IN §4.** This is
   the highest-value question in the brief. Consider in particular:
   - the dominating predicate `if (lenread != lentoread)` weakened;
   - the memset's operands swapped for other in-scope lengths (`len`, `remain`,
     `inblock`, `totallenread`);
   - `totallenread += lentoread` reverted to `+= lenread` **while keeping** the
     memset (this is a null-repair: the guard stays, its effect goes).
4. **A RUNG-3 WITNESS.** The offline differential is rung 1 and is a DETECTOR, never
   a reproduction. **Can a real guest on an unmodified in-tree machine description
   reach this?** It needs an overlay attached (`-d` with an overlay) whose data file
   is short, and one guest read crossing the boundary. If you think it cannot be
   built, say so plainly — "tried and could not" is a real answer and the round
   proceeds as documented-only.
5. **SEVERITY.** I rank this as a real correctness defect that is NOT guest-driven.
   Is that ranking right, or am I under- or over-stating it?

**VERDICT LINE FIRST**, please, so it survives truncation.
