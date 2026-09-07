# DESIGN BRIEF pass 1 — `pcc2c040kill`: one guest-writable bit turns ten ordinary code paths into `exit(1)`

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** A seat that re-derives a premise from something
this brief did NOT give it is worth more than one that agrees. **Five briefs of mine this week stated
premises that were false or too broad** — a variable's declared type, which of two arms is
authoritative, what a sibling probe's oracle asserts, the scope of "every MTE transfer", and a
zero-fill site count. Each was caught by a seat reading the code rather than my description of it.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**Where this brief states a COUNT, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE SITE**, quoted verbatim from `src/devices/dev_pcc2.c`:

```c
static void reassert_interrupts(struct pcc2_data *d)
{
	int assert = 0;

	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		/*  The M68000 interrupt mechanism involves outputting
		    interrupt level on pins EIPL<2..0>. Not implemented
		    yet.  */
		fatal("pcc2: C040 interrupt assertions... TODO\n");
		exit(1);
	}

	/*
	 *  Recalculate current interrupt level:
	 */
	...
```

**S2 — THE CONSTANTS.** `PCCTWO_GENCTL = 0x0002` and `PCC2_C040 = 0x04`
(`src/include/thirdparty/mvme_pcctworeg.h`). So the arming write is a **single byte of value 0x04 to
register offset 0x02** — a legal, in-range, correctly-sized register write.

**S3 — TEN CALL SITES.** `reassert_interrupts()` is called at `dev_pcc2.c` lines 383, 400, 459, 551,
574, 588, 602, 609, 622 and 662. **Once the bit is set, every one of those paths terminates the
emulator process.** Please check that enumeration — I derived it from a grep, and a grep that matches
a comment or a declaration would inflate it.

**S4 — THE ENTRY IS ROUTINE GUEST TRAFFIC; ONLY THE ARMING IS RARE.** The `SCCRXIACK` arm (offset
0x27) has **no `writeflag` test**, so a guest *load* of that offset runs `reassert_interrupts()`. This
was established by a design seat on a neighbouring row and verified by reading. OpenBSD's console
driver `cl.c` reads that offset on SCC receive interrupts. **So the question is not whether the path
is travelled — it is — but whether a guest sets `C040` first.**

**S5 — WHAT THE NEIGHBOURING ROUND DID AND DID NOT DO.** A previous round removed ten *width* kills
in this same file. This is not one of them; it is the sibling that round **exposed rather than
removed**, and its detector deliberately chose GENCTL lane values (`0xd9`/`0x40`, C040 clear) to stay
off this path — with an authoring-time assertion, `c040ok()`, keeping them there. So "ten kills
removed" reads as the file being safe while a one-byte write still terminates the process.

---

## The questions

**Q1 — WHICH DISPOSITION?** The project's option set is DELETE · DECLINE (silent) ·
DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT · IMPLEMENT. **Argue for one and against
the others**, and **grep the fork for the existing idiom before answering** — this project has twice
found an option-set member by looking rather than by reasoning, and once found that a member it had
chosen was unavailable on the target CPU.

**Q2 — WHAT IS THE CORRECT BEHAVIOUR, not merely the safe one?** If `C040` selects an interrupt
delivery mechanism the model does not implement, then after this returns without terminating:
**should it fall through to the normal level recalculation, or return having asserted nothing?**
Those differ in what the guest observes. **Say which the hardware would do**, or say plainly that the
source does not settle it.

**Q3 — IS THE BIT REACHABLE, and by what?** I claim a legal byte write to GENCTL sets it. **Check the
write path**: is there a width guard, a mask, or a read-only treatment that prevents it? And is there
any in-tree guest — a PROM, an OS driver — that writes `C040` deliberately? I would rather know the
arming is purely hypothetical than assume it is not.

**Q4 — THE ORACLE.** A detector must fail on the pre-fix build. Pre-fix, the process **terminates**,
so the row's channel is process survival plus whatever the guest observes afterwards. **Is a
survival-only row vacuous here?** This project has measured that survival oracles at refusal-effect
sites are vacuous by construction — guarded and unguarded code both survive — but here the pre-fix
build genuinely does not survive, which is the opposite case. **Say which it is.**

**Q5 — THE SMALLEST EDIT.** Once fixed, what is the smallest edit that breaks it and still passes?
Name the row you expect to stay green. I am after the clause-(d) family: a repair conditioned on a
field the guarded body reads. A neighbouring round's detector was swept clean twice by exactly that
shape — once at a transfer width no row drove, once at an addressing mode no row used.

## What I am not asking

Do not write a patch and do not run anything. I want the disposition argued and the oracle settled.

**If, while verifying a claim, you found something ELSE — say so.**
