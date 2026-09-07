# FULL PANEL — `pcc2c040kill`: a one-byte guest write ends the emulator. Design + witness, consolidated.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. **Seven briefs of mine this week stated premises that were false or too broad**, and every one
was caught by a seat reading the code rather than my description of it. Two were in *this* row and are
marked below as CORRECTED — **so this packet has already been wrong twice about its own subject.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**Where this packet states a COUNT or a REACHABILITY claim, ENUMERATE it.** Both of this row's
corrections were counts restated as reachability.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, with their evidence

**S1 — THE SITE.** `dev_pcc2.c`, `reassert_interrupts()`:

```c
	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		fatal("pcc2: C040 interrupt assertions... TODO\n");
		exit(1);
	}
```

**S2 — ARMING IS TERMINATION, IN ONE ACCESS.** The GENCTL write arm stores and calls the helper:

```c
	case PCCTWO_GENCTL:
		if (len != 1 && writeflag == MEM_WRITE) { ...decline...; break; }
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;   /* UNMASKED */
			reassert_interrupts(d);                 /* terminates */
		}
		break;
```

`PCCTWO_GENCTL = 0x0002`, `PCC2_C040 = 0x04`, the array is `uint8_t`, the header permits byte access,
and there is no read-only treatment. **One legal byte write of `0x04` to offset `0x02` ends the
process.**

**S3 — CORRECTED: "TEN CALL SITES" IS TRUE AND WAS MISLEADING.** Ten sites call the helper (383, 400,
459, 551, 574, 588, 602, 609, 622, 662) and all reach one shared branch — that part stands. **But
GENCTL is written in exactly ONE place, and that place calls the helper in the same access.** Every
other reference to `pcctwo_reg[PCCTWO_GENCTL]` is a read (`:271` the C040 test, `:341` the MIEN test),
and a wide write is declined *before* the store. **So the process always dies on the arming write, and
the other nine sites are unreachable as a first hit. The defect has ONE reachable entry.**

**S4 — CORRECTED: THE TICK CLAIM IS VACUOUS.** I wrote that a guest which arms C040 and then does
nothing is terminated at the next tick. `DEVICE_TICK(pcc2)` does call the helper unconditionally — but
**there is no interval in which C040 is set and the process is alive**, so that state cannot be
reached. A row waiting for a tick would wait forever.

**S5 — DISPOSITION, from a pass-1 audit:** DECLINE + LATCHED ANNOUNCE, with its own latch bit.
*"Survival is a nonvacuous oracle here, but cannot establish interrupt correctness."*

**S6 — THE WITNESS DESIGN WAS NOT RATIFIED.** A reviewer: *"A guest `st.b` of `0x04` at GENCTL is a
sound CORE… Survival-only, with no same-decode preset and no site-attribution, is not."* Required:
`how == "exit1"` rather than `not alive`; the transcript must carry `C040 interrupt assertions`, or it
is *failed for some other reason*; controls that must survive (RAM round-trip, CHIPID `ld.bu` → `0x20`,
and a **C040-clear GENCTL round-trip of `0x82`** as the same-decode preset); **and all of them must run
BEFORE the killing store, because nothing runs after it.**

---

## The questions

**Q1 — IS THE DISPOSITION RIGHT?** The option set is DELETE · DECLINE (silent) ·
DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT · IMPLEMENT. **Argue against
DECLINE + LATCHED ANNOUNCE.** Note that FAULT is not universally available — it needs the CPU family's
exception delivery, which exists for MIPS and M88K; this is M88K, so check rather than assume.
**Grep the fork for the existing idiom before answering.**

**Q2 — WHAT SHOULD THE HELPER DO AFTER DECLINING?** Fall through to the normal interrupt-level
recalculation, or return having asserted nothing? **They differ in what the guest observes**, and the
source may not settle it. Say which, or say plainly that it does not.

**Q3 — DOES S3's CORRECTION HOLD?** I now claim the defect has exactly one reachable entry. **Attack
that.** Is there any path — reset, init, a partially-declined access, a different register aliasing
into offset 2, `%=`-folded addressing — that sets C040 without calling the helper in the same access?
If there is, the tick row becomes live again and S4 is wrong too.

**Q4 — IS THE REQUIRED ATTRIBUTION SUFFICIENT?** Given S6's list, **what still goes green while
measuring nothing?** This project has had three witness designs refuted this week, all the same class:
the observation and the thing observed cannot coexist.

**Q5 — THE SMALLEST EDIT that breaks the fix and still passes. Name the row you expect to stay green.**
I am after the clause-(d) family — a repair conditioned on a field the guarded body reads. A
neighbouring round was swept clean three times by that shape, at a transfer width, an addressing mode,
and finally the joint cell of the two.

## What I am not asking

Do not write a patch or a probe, and do not run anything. **Nothing ships until the flagship
adjudication**, so this packet exists to be complete, not to authorise work.

**If, while verifying a claim, you found something ELSE — say so.**
