# CODE REVIEW (read-only) — `regress/alpha_harness_probe.py`, before its first run

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Five briefs of mine this week stated premises that
were false or too broad**, each caught by a seat reading the code rather than my description of it.
**If a premise below is wrong, that is the most valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**VERDICT LINE FIRST.**

---

## What this is

`regress/alpha_harness_probe.py` is a new file and **has never been run**. There has never been an
Alpha probe in this tree. It exists because three open rows need one, and it is deliberately written
controls-first: five control rows and three defect rows, with nothing asserted about the defect until
the controls are green.

**I am asking you to read it as CODE, not to assess the design.** The design was reviewed separately
and one earlier version of it was refuted — the first design put both process control blocks in
ordinary RAM, and a seat pointed out that the defect under test (`apcb_ptbr` taking the flags value)
**destroys the address translation the witness needs to observe it**, because `alpha_translate_v2p`
identity-maps only while `base == 0`. Everything now lives in K0SEG, which is checked before `base`
is read.

## Facts it was built on, each read out of `src/` rather than assumed

* `call_pal` is opcode 0 with the PAL number in bits 25..0, dispatched to `alpha_palcode()`.
* **`alpha_palcode()` gates its own switch on `ps & ALPHA_PSL_USERMODE`, and `0x30` is not on the
  unprivileged whitelist** — in user mode it sets `cpu->running = 0` and returns. `ps` has no
  initialiser, so it is zero (kernel mode); the `palgate` row measures that rather than trusting it.
* Memory-format encoding is `opcode<<26 | ra<<21 | rb<<16 | disp16`; LDA `0x08`, LDAH `0x09`,
  LDQ `0x29`, STQ `0x2d`.
* Register numbers and debugger names come from `ALPHA_REG_NAMES`: r0 `v0`, r1 `t0`, r2 `t1`,
  r3 `t2`, r4 `t3`, r16 `a0`, r31 `zero`.
* `ALPHA_K0SEG_BASE = 0xfffffc0000000000`.
* PCB field offsets from the handler's own save block: `+0` ksp, `+8` usp, `+16` ptbr, `+24` cpc,
  `+28` asn, `+32` unique, `+40` flags, `+48`/`+56` decrsv.

## The questions

**Q1 — WILL THE BOOTSTRAP WORK?** `lda`/`ldah` build 32-bit constants and a K0SEG address needs bit
63..42. The file writes the 64-bit pointers into identity-mapped scratch with the debugger's `put d`
and has the guest load them with one `ldq` **while `ptbr` is still zero**, after which every address
is a K0SEG value in a register. **Is that sequence actually valid**, and does anything between the
`put d` writes and the first `call_pal` disturb `ptbr`?

**Q2 — ARE THE INSTRUCTION ENCODINGS RIGHT?** This project has been bitten four times by
hand-assembled encodings, most recently in this very file: two control rows loaded into register 3
and printed `t1` (register 2), which would have read a register the test never wrote. **Check every
encoder and every register number against the decoder in `src/cpus/cpu_alpha_instr.c`.**

**Q3 — WILL THE ORACLE DISCRIMINATE?** `PCB_A` is written with `ptbr = 0` and `flags = MARKER`. Two
`swpctx` calls later, `PCB_A+16` should hold the saved `apcb_ptbr` — `0` if the handler is correct,
`MARKER` if the defect is present. **Walk the handler and say whether that is what lands there**, and
in particular whether the second call's SAVE writes to the OLD context (A) or the new one.

**Q4 — IS `put d` THE RIGHT DEBUGGER COMMAND?** The file uses `put d` for 64-bit writes on the
grounds that `put q` is 128-bit in this debugger. **Confirm from `src/debugger/`.**

**Q5 — WHAT WILL FAIL SILENTLY?** This is the question I most want answered. **Which of these rows
could go GREEN while measuring something other than what it claims?** The harness's own recent
history is that its sibling probe read a plausible value twice while the access was being declined —
so a green row is not self-evidently a correct one.

## What I am not asking

Do not run it, do not fix it, and do not write the defect rows differently. I want to know what is
wrong with the code before it runs, because its first run is also its first evidence.

**If, while verifying a claim, you found something ELSE — say so.**
