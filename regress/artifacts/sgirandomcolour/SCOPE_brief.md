# CHECK TWO PREMISES about `horrible_getputpixel()` in `dev_sgi_re.c` — scope of a filed defect

**VERDICT LINE FIRST**, then the body.

Scope your reading to **`GXEMUL-SEC/src/`**. Ignore any other `src/` you can reach — there are
three pristine 2021 upstream copies under the project root, and reading one gives line numbers off
by hundreds and different arms. **Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.**

**I am asking you to CHECK TWO CLAIMS I HAVE DERIVED BUT NOT CONFIRMED, and to audit the premises
under them. Do not write a probe, choose register values, or design a test.**

A recent panel here had seven of nine seats confirm a premise the brief stated wrongly — the true
number was four times larger. **So: check the premises, not just the derivations.** A clean "your
claim 2 is wrong because X" is the most useful answer you can give.

## What is already filed

A queue row (`sgirandomcolour`) records that the COLOUR-mode PUT switch has a `default:` arm which
fills a buffer with `random()` and then writes it to guest memory, and that `DE_MODE_TYPE_YCRCB`
— a mode the header documents — is handled nowhere in the file, so a guest selecting it lands
there. That much is established and is not what I am asking about.

## The code, verbatim

```c
	uint32_t color_mode = mode & DE_MODE_TYPE_MASK;
	int bufdepth = 1 << ((mode >> 8) & 3);
	...
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
		...
	}
```

And from `src/include/thirdparty/crmfbreg.h`:

```c
#define DE_MODE_TYPE_CI		0x00000000
#define DE_MODE_TYPE_RGB	0x00000010
#define DE_MODE_TYPE_RGBA	0x00000020
#define DE_MODE_TYPE_ABGR	0x00000030
#define DE_MODE_TYPE_YCRCB	0x000000f0
#define DE_MODE_TYPE_MASK	0x000000f0
```

---

# CLAIM 1 — the reachable set is TWELVE values, not one

The row is written as though YCRCB were the way in. But `color_mode = mode & 0xf0` can take
**sixteen** distinct values (`0x00, 0x10, ... 0xf0`), and the switch implements **four**
(`0x00/0x10/0x20/0x30`). So I believe **twelve** of the sixteen reach the `random()` arm — YCRCB
being merely the one that is also *documented*.

**Is that right?** Specifically:

* Is `mode` guest-writable such that bits 7:4 can hold any of the sixteen values, or is it
  constrained upstream — masked, validated, or only ever set from a small set — before reaching
  this function? **Name the writer(s) of `mode`.**
* Does anything reject a `color_mode` outside the documented five before this switch runs?

I care because a fix or detector built from a **one-value** census covers one sixteenth of the
door, reports full coverage, and is exactly the failure this project has already paid for once.

---

# CLAIM 2 — this may be an UNINITIALISED-STACK disclosure, and on the IMPLEMENTED paths too

This is the one I am least sure of and it is the reason for the brief.

`buf` is `uint8_t buf[8]` with **no initialiser**. The write is
`memory_rw(..., buf, bufdepth, MEM_WRITE, ...)` — i.e. **`bufdepth` bytes**, where
`bufdepth = 1 << ((mode >> 8) & 3)` ∈ {1, 2, 4, 8}. But:

    case CI      writes buf[0]        only  -> bytes 1..bufdepth-1 never assigned
    RGB/RGBA/ABGR writes buf[0..3]          -> bytes 4..7 never assigned when bufdepth == 8
    default:     writes buf[0..3]           -> bytes 4..7 never assigned when bufdepth == 8

If `bufdepth` can exceed the number of bytes an arm assigns, then **uninitialised stack bytes are
copied into guest-visible memory** — which is a different and arguably worse defect than
`random()`, because `random()` at least yields defined values, whereas stack residue can carry
whatever the host last put there.

**Questions, and I want these answered from the source rather than from plausibility:**

1. **Is `bufdepth == 8` actually reachable** at this call site? `#100`'s comment asserts it is —
   that is why `buf` is `[8]` — but a comment is not a measurement. Trace where `mode` comes from
   and whether bits 9:8 can be `3` here.
2. **Can `bufdepth` exceed the assigned byte count on the CI path?** CI assigns exactly one byte.
   If CI is only ever used with `bufdepth == 1`, what enforces that?
3. **Does `memory_rw` with `NO_EXCEPTIONS | PHYSICAL` really copy `bufdepth` bytes from `buf`**, or
   does something clamp/pad it? Check the callee rather than assuming.
4. If the disclosure is real, **is it reachable on a path a guest drives**, or only through a
   register combination nothing writes?

**If claim 2 is wrong, say so plainly and say which step fails.** I would rather withdraw it than
file a second finding on a misreading — this project withdrew one such row recently after the
declaration turned out to be three lines above the code that was quoted.

---

# Also

5. **`fatal()` here does not terminate** (it calls the returning printer `va_debug()`; only an
   explicit `exit(1)` ends the process). So the `default:` arm announces on **every** pixel. Is
   this a guest-drivable log flood — i.e. is this function called per-pixel in a loop? Name the
   caller and the loop if so.

6. If, while checking this, you found something **else** in this function — say so. The `#505`
   comment nearby records that the GET arm's RGB case once disagreed with the PUT arm's byte
   layout, so this function has a history of asymmetry between its two halves.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* **Give the denominator**: how many call sites and how many writers of `mode` you actually examined.
* Prefer "measure X" to "I think X" where a measurement would settle it.
