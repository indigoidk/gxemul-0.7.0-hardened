# DESIGN BRIEF pass 1 — `sgirergbroundtrip`: the RGB PUT and GET arms disagree about which byte holds which channel

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**A brief of mine yesterday stated a false premise — an index variable's declared TYPE — and I built
four paragraphs of consequences on it, filed the result HIGH, and committed it, before a seat read
the declaration. Please read the declarations. If a premise below is wrong, that is the most
valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork; their line numbers differ by hundreds.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## SETTLED PREMISES — measured, with their evidence, so you need not re-derive them

**S1. The two arms, quoted verbatim from `src/devices/dev_sgi_re.c`:**

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

**That is the complete tail of the function.** The whole enclosing function is `horrible_getputpixel`
in that file — please open it; a brief that shows only a fragment has produced four identical wrong
answers here before.

**S2. Byte-position table, enumerated rather than reasoned:**

| mode | PUT writes | GET reads | round-trips? |
|---|---|---|---|
| CI | `buf[0]` | `buf[0]` | yes |
| **RGB** | **`buf[0],[1],[2]`, and `buf[3]=0`** | **`buf[1],[2],[3]`** | **NO** |
| RGBA | `buf[0],[1],[2],[3]` | `buf[0],[1],[2],[3]` | yes |
| ABGR | `buf[0],[1],[2],[3]` | `buf[3],[2],[1],[0]` | yes |

**RGB is the only mode that fails its own round trip.** RGBA and ABGR both round-trip while using
*opposite* byte orders, which is why I claim this is an internal inconsistency rather than an
endianness question — but **that is exactly the kind of claim I want challenged.**

**S3. The constants** (`src/include/thirdparty/crmfbreg.h`): `DE_MODE_TYPE_CI 0x00`,
`RGB 0x10`, `RGBA 0x20`, `ABGR 0x30`, `YCRCB 0xf0`, `MASK 0xf0`.

**S4. MEASURED on the committed build (`a264a34`), rung-3, unmodified `-E sgi -e ip32`:** a copy
whose source mode selects RGB and whose destination mode selects RGBA turns `0xaabbccdd` into
`0xbbccdd00` — the source shifted one byte left with a zero fill, which is what the GET reading
`buf[1..3]` predicts exactly. The same probe's controls pass in the same run: a RAM store/load
returns its value, `CRIME_DE_STATUS` reads `0x1e000000` where RAM would read 0, and **an RGBA source
copies correctly through the same code path**, so the engine is being driven properly and only the
RGB arm misbehaves.

## The questions

**Q1 — WHICH ARM IS WRONG?** I believe it is the GET, on two grounds: PUT's `buf[3] = 0` is an
explicit pad write, so byte 3 is the pad and a GET that reads it is reading the pad; and RGBA — the
neighbour that shares PUT's byte order exactly — puts R at `buf[0]`. **Argue the other side.** Is
there a reading on which PUT is the wrong arm and GET is right?

**Q2 — WHAT DOES THE HARDWARE ACTUALLY DO?** This is the question I cannot answer from the source.
If you know, or can find in the tree, anything about how the CRIME/RE drawing engine lays out a
32-bit RGB pixel in memory — a driver, a comment, a framebuffer consumer that reads these bytes back
— say so and cite it. **If you do not know, say you do not know**; I would rather have an honest
gap than a plausible reconstruction.

**Q3 — DOES ANYTHING DEPEND ON THE CURRENT BEHAVIOUR?** This project has twice found a bug that
another part of the emulator was silently relying on. Is there any consumer of a pixel written or
read in RGB mode — the framebuffer path, a later copy, a `debug()` — that would change behaviour if
the GET were corrected? **Name what you checked, not just your conclusion.**

**Q4 — IS RGB MODE REACHABLE BY A REAL GUEST, or only by a probe like mine?** I have not
established this. `dev_sgi_re.c` also constructs modes internally in the MTE path
(`src_mode |= DE_MODE_TYPE_RGBA` and the `dst_mode` beside it). Does any in-tree path, or any
plausible driver, select `DE_MODE_TYPE_RGB`? This decides whether the round is a correctness fix or
a robustness one, and I would rather know before writing the record than after.

**Q5 — THE MUTANT ENUMERATION.** If the fix is one line in the GET arm, what is the smallest edit
that reintroduces the defect or nulls the repair while still *reading* like the corrected code?
I am looking for the clause-(d) set: predicates or expressions the fix depends on, weakened to the
least-restrictive form that still looks right. A shift count changed by 8, a byte index changed by
one, a `+` become an `|`. **Which of those would my three rows fail to catch?**

## What I am not asking

Do not write the fix as a patch, and do not run anything. I want the design settled first: which arm
is wrong, on what evidence, and what a detector must cover.

**If, while verifying a claim, you found something ELSE — say so.**
