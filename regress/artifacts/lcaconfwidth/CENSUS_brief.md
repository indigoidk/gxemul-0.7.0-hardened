# CENSUS — `lcaconfwidth`: a 64-bit guarded value printed through `(int)`, so a kill message can name a value that would NOT have killed

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Two hours ago I stated a premise as *settled* and
three of six seats confirmed it; **one seat opened the file and refuted it**, correctly, and it
reversed the round's blocking question. **This brief's central number is almost certainly wrong in one
direction or the other — find out which.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE:** `GXEMUL-SEC/src/devices/*.c`.

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE EXEMPLAR, verified by reading `dev_lca.c`.**

```c
:205        " IOC_CONF: 0x%x\n", (int)idata);
:206   if (idata & ~1) { ... exit(1); }        /* the guard, on the FULL 64-bit value */
```

`idata` is the 64-bit value parameter of `DEVICE_ACCESS`. A write of `0x100000000` sets a bit above
31, so `idata & ~1` is true and the process dies — but `(int)idata` is **0**, and `0` is precisely the
value this guard **accepts**. *The kill message names an acceptable value while killing on an
unacceptable one.*

**S2 — WHY IT IS NOT COSMETIC, and this is why the row exists.** A sibling HIGH row, `lcabadval`,
plans a rung-3 witness whose rows must match the **`fatal()` TEXT** rather than the exit status —
because `lca_interrupt_assert`/`_deassert` are bare `fatal()`+`exit(1)` with the ISA PIC chain wired
to them, so *any* interrupt ends the host with the same status. **If the text can print the wrong
value, the text-matching oracle is unsound at that arm.** So this row may be a PREREQUISITE of
`lcabadval` rather than its sibling.

**S3 — MY CENSUS, AND I BELIEVE THE HEADLINE IS A CORRELATE, NOT THE CLASS.** Derived, not quoted:

```
grep -rn '(int)idata' src/devices/*.c            ->  226 sites, ~68 files
   (uint32_t)idata 4 · (long)idata 1 · (int32_t)/(unsigned int) 0
sites within 3 lines of an exit(1)               ->   15
```

**226 is certainly far too many** — most are ordinary debug prints of an 8-bit register write, where
narrowing loses nothing. **15 is proximity, which is also a correlate**: being near an `exit(1)` is not
the same as being the *subject* of the guard that kills.

**S4 — WHAT I THINK ACTUALLY DEFINES A MEMBER**, offered as a hypothesis to attack: *the diagnostic
prints a value that is also the subject of a guard, narrowed on the way out, where the guard can be
tripped by bits the print discards.* On that reading, a guard testing only bits 0–31 is **not** a
member however it prints, because no distinguishing value exists.

---

## The questions

**Q1 — WHAT IS THE REAL MEMBERSHIP?** Take the 15 proximate sites (derive them yourself; the command
is in S3) and for each, **read the guard** and say whether a 64-bit value exists that trips the guard
and prints as something the guard would accept. **Give the discriminating value where one exists.**
That, not proximity, is the census.

**Q2 — IS S4's DEFINITION RIGHT?** Attack it. Two shapes I suspect it mishandles: a guard on
`relative_addr` rather than `idata`; and a print that is *misleading* without being *wrong* — e.g. it
narrows but every reachable value fits in 32 bits, so the defect is latent rather than live. **Should
those be members?**

**Q3 — IS `dev_lca.c:313` A SECOND MEMBER IN THE SAME FILE?** It is `fatal(": 0x%x", (int)idata)`.
`dev_mvme187.c:88` looks like the same shape. **Check both** — and if they are members, say whether
the fix is per-site or one idiom change.

**Q4 — WHAT IS THE FIX, AND WHAT IS ITS BLAST RADIUS?** The obvious form is
`%" PRIx64 "` with the cast dropped. **Is `PRIx64` already used in this tree** (check, do not assume),
and does any gate, hygiene grep or probe match on the CURRENT text of any member? A diagnostic's text
is an oracle here — several probes match on it — so changing one can turn a green row red by
succeeding.

**Q5 — ORDERING.** Given S2: is this a **prerequisite** of `lcabadval`, or can that row's witness be
built with a text oracle that avoids the affected arm? **Say which, and why.**

## What I am not asking

Do not write a patch, and do not run builds, gates or probes. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
