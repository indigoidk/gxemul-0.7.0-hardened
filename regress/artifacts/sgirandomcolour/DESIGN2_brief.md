# DESIGN, PASS 2 — `sgirandomcolour`: a decline does NOT leave the destination untouched

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **You wrote the finding this brief is built on**, on
a different row, and I may have over-read it. Today you corrected two of my premises on
`sgimtedepth4dead` and two more on `sgirebufuninit`. **Assume I have over-read this one and say so.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**

**SCOPE:** `GXEMUL-SEC/src/devices/dev_sgi_re.c`, `GXEMUL-SEC/regress/sgi_re_*.py`.

**VERDICT LINE FIRST.**

## §C — SETTLED PREMISES

**S1 — THE ROW.** `horrible_getputpixel()`'s **colour-mode PUT** `default:` arm assigns
`buf[0..3] = random()` and lets the common tail write those bytes out. Twelve of sixteen type-nibble
values reach it, including the documented `DE_MODE_TYPE_YCRCB`.

**S2 — THE DESIGN SETTLED ON PASS 1** (your own answer): **DECLINE + LATCHED ANNOUNCE with a `return`
before the transfer**, an independent latch bit rather than sharing `SGIRE_W_BADMODE`, and NOT
depth-aware arms. `sgirebufuninit` was established to be independent, not a prerequisite: *"a declined
PUT need not leave anything defined in `buf`, provided nothing consumes it — the helper itself owns
the memory write."*

**S3 — THE FINDING THAT REOPENS IT**, from your `sgimtedepth4dead` answer:

> *"A helper return before accessing the buffer leaves the caller's colour unchanged. MTE still
> performs the dependent PUT, and its `bg` persists across iterations — so a declined GET can reuse an
> earlier source value."*

**S4 — VERIFIED IN THE SOURCE.** `bg` is declared at `:1314`, **outside** both nested loops
(`:1377-1391`), and its address is passed to the GET at `:1383` and the PUT at `:1387` in the same
iteration.

## The questions

**Q1 — DOES S3 ACTUALLY BEAR ON THIS ROW, OR HAVE I CONFLATED TWO THINGS?** S3 is about a declined
**GET** leaving `*color` stale. This row is about the **PUT** default arm. **Are they the same
problem?** If a declined PUT returns before writing, the destination keeps its old contents — which
may be entirely correct. Say plainly if I have merged a GET-side observation into a PUT-side row.

**Q2 — IF IT DOES BEAR: what does the destination hold after a declined pixel?** On the MTE path a
declined GET leaves `bg` at the previous pixel's value, and the PUT then writes **that**. So a run of
unsupported pixels is painted with the last good colour rather than with `random()`. **Is that better,
worse, or merely different?** It is deterministic, which the round wanted — but it is also a
plausible-looking wrong answer, and `random()` at least announces itself as garbage.

**Q3 — DOES THE LATCHED ANNOUNCE STILL FIRE ONCE PER RUN?** If the decline is per-pixel and the latch
is per-device, a thousand declined pixels produce one message. **Is that the right granularity**, or
does it hide the extent — the difference between one bad pixel and a whole bad rectangle?

**Q4 — WHICH ARM SHOULD RETURN?** Candidates: return from the PUT default only; return from the GET
default too; or decline the whole `horrible_getputpixel` call before the switch. **They differ in what
the caller's `color` holds and in whether the dependent PUT still runs.** Name the one that leaves the
guest with the most honest state.

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay green.**
The `#505` detector in this same file was swept clean three times by the clause-(d) shape, and its
rows all exercise DE — **so an MTE-side repair may be unobservable to every existing row**, which is a
coverage answer as much as a mutant answer.

## What I am not asking

Do not write a patch or a probe, and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
