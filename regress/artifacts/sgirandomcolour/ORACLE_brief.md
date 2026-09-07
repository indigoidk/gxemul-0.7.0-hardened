# NARROW QUESTION — does a `MEM_WRITE`-count oracle work for "did a write happen", when it fails for "what did it contain"?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Six briefs of mine this week stated premises that
were false or too broad.** This one asks you to check a distinction *I* drew, and I want it attacked
rather than confirmed — I drew it in one sentence while reading someone else's answer, and I have not
tested it.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**VERDICT LINE FIRST.**

---

## The situation

Two neighbouring rounds in `dev_sgi_re.c`'s `horrible_getputpixel()` both need an oracle, and both
concern the same buffer.

**ROUND A — the colour-mode PUT default.** Its arm assigns `buf[0..3]` from `random()` and falls
through — there is no `break` — into
`memory_rw(..., tileptr + ofs, buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL)`. The intended
repair is to decline: **announce once and return without writing.** A seat proposed the oracle
*"observe ZERO `MEM_WRITE` calls from an unsupported PUT, alongside unchanged destination bytes"*,
on the grounds that this **distinguishes "no write" from "same final value"**.

**ROUND B — the buffer is never initialised.** `uint8_t buf[8];` has no initialiser, and the arm that
assigns it and the length that transfers it come from two independent fields of the same guest-written
mode word. The intended repair is to zero-fill at the declaration. A seat ruled: *"No guest-visible
value **or write-count** oracle can reliably prove initialization occurred."*

## The distinction I drew, and want checked

I wrote that the write-count oracle **survives for Round A and does not transfer to Round B**, because
Round A asks *whether a write happens* and Round B asks *what the written bytes contain* — and a
count can answer the first but not the second.

**Q1 — IS THAT DISTINCTION SOUND, or is it a sentence that sounds right?** Specifically: is there a
reading on which the count fails for Round A too?

**Q2 — CAN A GUEST-SIDE PROBE COUNT `MEM_WRITE` CALLS AT ALL?** This is the part I am least sure of.
The probe drives the emulator through its debugger over a pty and reads guest-visible state; it does
not instrument the emulator. **So what would actually be counted, and by what?** If the honest answer
is "nothing guest-visible counts writes, so the proposed oracle needs an instrumented build or a
`harness:` witness", say so plainly — that changes Round A's shape and is better learned now.

**Q3 — WHAT DOES "UNCHANGED DESTINATION BYTES" ACTUALLY PROVE?** The paired half of the proposal.
The destination is pre-painted with a known value. If a declined PUT leaves it unchanged, the row is
green. **But what else leaves it unchanged?** A copy that never ran, a tile pointer that failed its
validity gate, an address outside RAM — this project has just had a probe read a plausible value
twice while the access was silently declined, and another whose addresses were outside the machine's
memory so every read returned zero.

**Q4 — IS THERE A BETTER ORACLE FOR ROUND A?** The arm's output is `random()`, so no value row can
pin it, and a determinism oracle is refuted (stack reuse can make a wrong value repeat). **What is
left?** I would rather know the honest ceiling than build a row that cannot fail.

## What I am not asking

Do not write a patch, a probe, or a fix. This is one question about oracle validity.

**If, while verifying a claim, you found something ELSE — say so.**
