# AUDIT (read-only) — what does `PAL_OSF1_swpctx` assign, and what reads those fields?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**Two briefs of mine this week stated premises that were simply false** — one was a variable's
declared *type*, the other was which of two code paths is authoritative — and I built conclusions on
both before a seat read the code. **If a premise below is wrong, that is the most valuable thing you
can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/`.** Do not read `GXEMUL-SEC/regress/artifacts/` or
`GXEMUL-SEC/tools/pipeline/ledger.json`.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## Context

`src/cpus/cpu_alpha_palcode.c` implements the OSF/1 PALcode calls for the Alpha CPU model. Case
`0x30` is `PAL_OSF1_swpctx`, which saves the current process control block to memory and loads a new
one. I am auditing that one handler for internal consistency, and I want each question answered from
the source rather than from what the code appears to intend.

**These are independent reading questions. Please answer them separately — I am not asking you to
assemble them into anything.**

## The questions

**Q1 — FIELD-BY-FIELD ASSIGNMENT AUDIT.** In case `0x30`, the handler reads nine values from memory
into locals and then assigns them into `cpu->cd.alpha.pcb`. **List every assignment in that block, in
order, as a table of `destination field <- source local`.** Then answer two things from your own
table: **is any destination field assigned more than once, and is any local never used as a source?**
Do not assume the intent; read the nine lines.

**Q2 — THE SAVE SIDE'S OFFSETS.** The same handler writes the *current* pcb out to memory before
loading. **List the offsets it writes and the field each one carries.** Are the save offsets and the
load offsets the same map?

**Q3 — WHO ELSE READS THESE FIELDS?** For `cpu->cd.alpha.pcb.apcb_ptbr` and
`cpu->cd.alpha.pcb.apcb_flags` separately: **which files and functions in `src/` read each one, and
what is each read used for?** I want the consumers named, not summarised.

**Q4 — THE COMMENT AT THE RETURN.** Immediately before the load block there is a line under a comment
reading *"Return old context in v0."* **Which register does the line actually assign?** Check
`ALPHA_REG_NAMES` in `src/include/cpu_alpha.h` for the numbering, and say whether the comment and the
code agree. If they disagree, say which one matches the calling convention the rest of this file uses
for PAL return values — cite two or three other cases in the same `switch` as evidence.

**Q5 — ORDERING.** Does the save block execute before or after the statement that updates
`cpu->cd.alpha.ctx`? Quote the two lines that settle it.

**Q6 — IS `call_pal` DISPATCH GATED?** In `src/cpus/cpu_alpha_instr.c`, what conditions must hold for
opcode 0 to reach `alpha_palcode()`? **Is there any privilege check, mode check, or enable bit** on
that path, or is the dispatch unconditional? I have read this and believe it is unconditional, and I
would like that either confirmed from the source or corrected.

**Q7 — IF ANYTHING IN Q1 LOOKS WRONG, HOW BIG IS THE CORRECTION?** Is it a one-token change, or does
correcting it require touching more than one line? Say what the corrected line should read.

## What I am not asking

Do not write a patch, do not write a test, and do not run anything. **Do not describe how software
would exercise this handler** — I want the code read and the questions above answered directly.

**If, while verifying a claim, you found something ELSE — say so.**
