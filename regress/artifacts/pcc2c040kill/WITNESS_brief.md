# WITNESS DESIGN (read-only) — `pcc2c040kill`: is a one-byte reproduction sound, and what must it control for?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Six briefs of mine this week stated premises that
were false or too broad**, and a seventh proposed a witness design that a reviewer refuted outright —
the defect it was meant to observe destroyed the mechanism the observation depended on. **Assume this
design has the same class of flaw and go looking for it.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES, each read from the source

**S1 — THE SITE.** `dev_pcc2.c`'s `reassert_interrupts()` opens:

```c
	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		fatal("pcc2: C040 interrupt assertions... TODO\n");
		exit(1);
	}
```

**S2 — ARMING IS TERMINATION, in one access.** The GENCTL write arm is:

```c
	case PCCTWO_GENCTL:
		if (len != 1 && writeflag == MEM_WRITE) { ...decline...; break; }
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;   /* stores UNMASKED */
			reassert_interrupts(d);                 /* terminates */
		}
		break;
```

So a **single legal byte write of `0x04` to offset `0x02`** stores the bit and immediately calls the
helper. No second access is needed. `PCCTWO_GENCTL = 0x0002`, `PCC2_C040 = 0x04`, the register array
is `uint8_t`, and the header explicitly permits byte access.

**S3 — TEN CALL SITES reach that one branch**, at `dev_pcc2.c` 383, 400, 459, 551, 574, 588, 602,
609, 622, 662 — including **400, the device tick, called unconditionally**, so a guest that arms the
bit and then does nothing is still terminated at the next tick.

**S4 — AN EXISTING PROBE ALREADY DRIVES THIS REGISTER.** `regress/pcc2_width_probe.py` byte-writes
GENCTL on this machine and carries an authoring-time assertion, `c040ok()`, whose whole purpose is to
keep its lanes (`0xd9`/`0x40`) **off** this path.

---

## The proposed design, which I want attacked

One session added to `pcc2_width_probe.py`: byte-write `0x04` to GENCTL, then observe that the
emulator process is gone. Oracle: **process survival**, which a pass-1 audit called *"a nonvacuous
oracle here"* — unlike a refusal-effect site, the pre-fix build genuinely does not survive.

**Q1 — WHAT ELSE KILLS THE PROCESS?** If the oracle is "the process is gone", **anything** that ends
it satisfies the row. Name what could: a different `exit()` on the way in, an assertion, a machine
that fails to construct, a probe that mis-addresses. **What control distinguishes "died at THIS
site" from "died"?** The `fatal()` text is one candidate — does it reach the pty before the process
goes, or is it lost to buffering?

**Q2 — IS THE PRE-FIX/POST-FIX PAIR WELL FORMED?** After the repair the process survives, so the row
inverts from "died" to "alive". **What then proves the write was DECLINED rather than silently
accepted?** Survival alone cannot tell a latched decline from a repair that simply removed the check.

**Q3 — DOES ADDING THIS SESSION DISTURB THE EXISTING ROWS?** `c040ok()` exists to keep the width
lanes off this path. **Must it be relaxed, and if so does relaxing it weaken what it protects?** I
would rather scope the new session than turn the guard off file-wide.

**Q4 — IS ONE SESSION ENOUGH, given ten call sites?** The pass-1 audit settled that all ten reach one
shared branch. **Does that make one witness sufficient, or does the round owe a second row at the
tick site (400), which needs no guest access at all?**

**Q5 — WHAT WILL SILENTLY GO GREEN?** Two probes today read plausible values while their accesses
were being declined, and a third had every address outside the machine's memory so all reads returned
zero. **Which part of this design could report success while measuring nothing?**

## What I am not asking

Do not write the probe, the fix, or a patch, and do not run anything.

**If, while verifying a claim, you found something ELSE — say so.**
