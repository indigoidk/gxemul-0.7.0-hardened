# REPAIR 14 — PANEL PASS 1 FINDINGS, with my disposition on each

**Status: 6 of 9 seats landed at the time of writing.**  `grok` was MID-ANSWER (streaming, 846 b —
verified by content, not size).  `codex` **REFUSED** on its provider's content filter and has been
RE-FIRED with a scoped variant (see S1).  The `opus5` Agent seat is running.  `fable5` is
DELIBERATELY HELD until every other seat has answered — standing owner directive.

**Panel dir: `_scratchpad/panel_20260916_234606/`.**

Seat verdicts as landed: `agy` GO-WITH-CHANGES · `ollama_glm` "direction survives, brief is not
clean" · `ollama_deepseek` REJECT REPAIR AS SCOPED · `ollama_minimax` BRIEF HAS REAL DEFECTS ·
`ollama_kimi` DO NOT RATIFY AS WRITTEN · `kimi` (CLI) answered, no verdict line.

> **Every one of the findings below is against MY BRIEF, not against the fix or the detector.**  That
> is what pass 1 is for, and the premise-audit opener is why they were found.

---

## F1 — **THE 46-vs-56 GAP.  THREE SEATS INDEPENDENTLY.  UPHELD.**
*(glm F2, minimax, ollama_kimi — each derived it separately from the packet alone.)*

The brief states the product is **56 cells** and then dispositions **23 rowed / 8 already-pinned /
10 equivalent / 5 host-diagnostic = 46**.  `56 − 46 = 10 cells in no category.`

**MY DISPOSITION: UPHELD, and the cause is a UNIT CONFLATION that is mine.**  46 is a count of
**ACCEPTS ENTRIES** — the probe's accept-path drive list.  56 is a count of **PRODUCT CELLS**.  They
are different populations, and my brief presented the 46-split as though it dispositioned the 56.
*Stages and rows are different units, and a count that names neither cannot be checked* — this
project's own rule, and I broke it in a packet.

**OWED:** a per-cell disposition table over the 56, or an explicit statement that the 46 is a
different population with the mapping given.  Not a re-argument — a table.

## F2 — **P4 IS FALSE: THE LATCH-CLEAR STATE IS *NOT* DRIVEN BY SESSION 40 ALONE.**
*(glm F1 and ollama_kimi Finding 1, independently.  **SETTLED BY MEASUREMENT, NOT BY JUDGEMENT.**)*

Both seats spotted that P4 and P5 cannot both be true: P4 says the latch-CLEAR state is driven by
session 40 (`latch x5`) **ALONE**, whose three rows are announce counts and a RAM round-trip; P5 says
`G_clr_imk4r` — a latch-CLEAR conjunct, silent by P3's own shape — is **killed 187/188** via
`gate line`.  **A latch-SET row cannot red a latch-CLEAR mutant**: the conjunct is inert once
`d->warned & CRIME_W_LEN` is set.

glm named the settling fact ("the log line showing which session/row reds under `G_clr_imk4r`").  I
checked the probe instead, which settles it more directly:

```
 733| x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
 734| x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
 735| x, _ = ld(A, "lw", CRIME + 0x18, "a0"); c += x     <-- INTMASK 4-BYTE READ
 ...
 741| x, _ = ld(A, "lb", CRIME + 0x08, "t1"); c += x     <-- the FIRST refusal in this session
 743| x, _ = st(A, "sh", CRIME + 0x08, 0x0800); c += x
```

**`grep -c "POST(" ` over that session block returns 0**, and the `lw` at `:735` precedes the first
refused access at `:741`.  **So the gate-run session drives INTMASK 4R with the latch CLEAR and with
a value oracle**, which is exactly why that one member of the class is caught.

> ### *** THIS IS THE MOST USEFUL THING THE PANEL PRODUCED, BECAUSE IT REPLACES A GUESS WITH A
> ### CRITERION. ***
>
> The brief framed repair 14 as *"mirror the post-latch sessions"*, which is a shape chosen by
> analogy.  The real criterion is now derivable by reading:
>
> > **A latch-CLEAR cell is COVERED exactly when some session drives it BEFORE that session's first
> > refused access, with an oracle that observes it.**
>
> That explains all three measured outcomes at once — `G_clr_imk4r` killed (INTMASK 4R driven
> pre-refusal at `:735`), `G_clr_ist4r` and `G_glm_tim4clear` escaped (not driven pre-refusal with an
> oracle anywhere) — and it prices the repair per cell instead of doubling every session.

**AND IT CUTS BOTH WAYS, which glm said and I am recording rather than softening:** the covered set
may be LARGER than P4 admits, so the mirror may be narrower than proposed — but *"the CLEAR half is
wholly unobserved"* was also overstated in my own VERDICT.md, and that sentence needs correcting
there too.

## F3 — **P1's early-return claim is FALSE, and the probe's own header refutes it.**  UPHELD.
*(agy, citing `crime_width_probe.py:269-272`.)*

My brief said an early `return` "skips the interrupt recomputation AND `memory_writemax64`, which is
a defect the shipped code does not have."  The probe's DISCLOSED block says the opposite and gives
the warrant:

```
 269|   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
 270|     (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);' ...
 271|     ... on a declined access nothing between the entry and the tail writes
 272|     HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 ... in kill table 1.
```

**MY DISPOSITION: UPHELD.**  The statements are mechanically skipped; the SKIPPING IS UNOBSERVABLE,
because the tail's operations are identities on a declined access and the read buffer is zeroed
upstream.  The consequence I attached is what is false.  *I imported a correct general caution — the
four-readers-and-a-common-tail lesson — into a site where it had been measured not to apply, without
reading the probe header that says so.*

## F4 — **IS `CRIME_HARDINT` ITS OWN CASE?  CHECKED: NO.  THE BRIEF SURVIVES.**
*(minimax, Q1.)*

minimax noticed the inlined switch jumps `384| case CRIME_INTMASK` → `388| case CRIME_DOG` and asked
whether `CRIME_HARDINT` (0x020) has an elided case, which would make "six named + default" wrong and
the product 64 rather than 56.  **A fair premise-audit question against an ELIDED region — exactly
the right instinct.**  Checked:

```
 383| 	case CRIME_INTSTAT:	/*  0x010, Current interrupt status  */
 384| 	case CRIME_INTMASK:	/*  0x018, Current interrupt mask  */
 385| 		crime_interrupt_reassert(d);
 386| 		break;
 388| 	case CRIME_DOG:		/*  0x030  */
```

`385-387` is the shared body of the INTSTAT/INTMASK fall-through pair.  **There is no
`case CRIME_HARDINT`**, so HARDINT falls to `default:` and the seven-label count stands.

## F5 — **"the leftover" is unspecified and the CONTROL arm body was never inlined.**  UPHELD.
*(minimax, finding 1.)*

P6 says the CONTROL arm tests DOG `0x200`, HARD_RESET `0x800` "and the leftover", while P1 inlines
only the `case` labels — thirty lines of CONTROL body unaccounted for.  If that body tests a bit
other than those two, Part B does not close it.  **UPHELD: inline `353-382` before pass 2.**  This is
§C4 again (a total whose members are not shown), reached from a different direction than F1.

## F6 — deepseek: **the enumeration is internally contradicted by the brief's own two extra axes.**
UPHELD, and it is F1's sibling.

The brief states the domain as a four-factor product and then names two further factors of the same
handler (`relative_addr & 4`, `cpu->pc`) as "measured closed".  **If they partition the handler they
are FACTORS, so the domain is at least 2×56 and more with the PC window.**  Calling them closed while
excluding them from the product is not a disclosure, it is an omission with a note attached.

**MY DISPOSITION: UPHELD.**  The honest form states the domain as the SIX-factor product and records
the lane and PC factors as **measured closed with their evidence** (the four lane-split legs at
185/185/186/185, and `W_rev8r_out` 187/188 as the PC positive control), rather than leaving them out
of the arithmetic.  *A packet-fed seat caught this from the packet alone, which is the strongest kind
of catch — it needed no repo access to see that the brief contradicted itself.*

---

## S1 — SEAT RECORD (operational, never agreement)

* **`codex` REFUSED** — `ERROR: This content was flagged for possible cybersecurity risk`, after
  158 KB of file-reading trace.  **Not a wall and not an answer.**  The cause is my brief, not the
  seat: it broke all three of the documented codex rules at once — flagged vocabulary (*host kill*,
  *breaks the fix*), unrestricted reading scope, and a Q2 that asked for **the smallest edit that
  re-opens the defect**, which is the exact construction the four-run controlled experiment recorded
  as reliably refused.  **RE-FIRED** with `PASS1_brief_codex.md`: ordinary engineering language,
  reading scoped to `src/` + `regress/*.py`, and the edit-construction question dropped.
* **`grok` MID-ANSWER** at sampling time, not walled — verified by reading its content (progress
  narration), not its size.
* **`opus5`** running.  **`fable5` HELD** until all others have answered.

---

## F7 — **grok LANDED, AND IT IS THE STRONGEST ANSWER: IT CONVERGES ON F1 AND THEN EXPLAINS THE
## ESCAPE NOTHING CATCHES.**  VERDICT: NOT RATIFIED as written.

**It reached F1 independently and diagnosed the MECHANISM, which no other seat did:**

> *"23 is not the floor.  It is a count of ACCEPTS ENTRIES rowed post-latch by repair 13, not of
> guest-visible product cells, and not of both latch states.  23+8+10+5=46 partitions ENTRIES —
> CONTROL writes of `0x0201` / `0x0001` / `0` / `0x0200` / `0x0100` are five entries of ONE cell."*

So the two populations do not merely differ in size: **many entries map to one cell**, which is why
no re-count could reconcile 46 with 56.  *That is the unit conflation of F1 with its cause supplied.*

**AND IT DERIVES THE CONSEQUENCE, which is the answer to "why does INTSTAT 4R escape everything":**

> *"Using 23 as the class-closure denominator is how IST 4R falls through: it is not in the 23 —
> SET-side it is already pinned by `istat ctl` — and it is still open on CLEAR."*

**THE MISSING FLOOR CELL, NAMED PRECISELY AND WITH ITS ORACLE REQUIREMENT:**

> **INTSTAT 4R, latch-CLEAR, with `SOFTINT|HARDINT` SEEDED NONZERO.**
> *"`t4clear.py` is the TIME shape, not the class."*

That is a sharper statement than mine: it is not enough to drive INTSTAT 4R pre-refusal — the
interrupt state must be seeded so the reassert has something OBSERVABLE to do.  My F2 criterion
("driven pre-refusal with an oracle") is right and underspecified; grok supplies what the oracle has
to contain.

**AND A DESIGN CONSTRAINT I HAD NOT STATED, which is a genuine addition:**

> *"`G_clr_imk4r` 187/188 reddening `gate line` is the positive control and MUST STAY in the 188-row
> instrument, so the next closing pass still has a CLEAR-half control that is not TIME."*

A repair that incidentally changes what `gate line` observes would cost the class its only
non-TIME positive control.  **Repair 14 owes a check that it does not.**

### F8 — **P1 WAS NOT THE FULL ENCLOSING FUNCTION, AND THE OMISSION WAS LOAD-BEARING.**  UPHELD.

grok: the inlined block starts at the `else` at `:296`.  Omitted and load-bearing:

* **the prelude at `229-235`** — `CONTROL = ENDIANESS` `0x100` on every access.  ***The CONTROL-4R
  equivalence IS that line***, so the packet asserted the equivalence while omitting its warrant;
* the `len == 4` lane tests at `:282` and `:291`;
* the RAM-size exits at `244-260` (filed, not this detector).

**MY DISPOSITION: UPHELD, and it is a §D violation of mine** — the rule is that a brief which
solicits or evaluates edits inlines the FULL enclosing function, every exit path and the common tail.
I inlined from the decline onward and the case labels without their bodies.  **Pass 2 inlines
`229-423` entire**, which also discharges F5 (minimax's unspecified "leftover" in the CONTROL body).

> ### THE PANEL HAS CONVERGED, AND THE CONVERGENCE IS THE RESULT
>
> Six seats, reached independently: the floor denominator is the wrong population (grok, glm,
> minimax, kimi-k3); P4 is false (glm, kimi-k3, and grok from the other direction); the brief
> omitted load-bearing context (grok, minimax); and the repair's SHAPE — a mirror of the post-latch
> sessions — aims at the wrong set.  **Not one seat defended Part A as written.**
>
> **What survives unanimously: the MANDATE.** Class-close in one diff, and folding in `t4clear.py`
> alone is measured insufficient.  That was the brief's central claim and no seat disputed it.

---

## F9 — **codex ANSWERED ON THE RE-FIRE (zero flags, 7,826 b), AND IT REFRAMES THE DOMAIN.**
## VERDICT: *"Repair 14 needs a revised coverage model."*

**THE §C5 REMEDY IS VALIDATED A SECOND TIME.**  Same seat, same questions, same tree — the only
changes were neutral vocabulary, reading scoped to `src/` + `regress/*.py`, and dropping the
edit-construction question.  First firing: flagged after 158 KB.  Second: **353 KB of streamed
reasoning, no flag, a full verdict.**

**F9a — THE DOMAIN IS NOT 56, AND IT IS NOT THE 224 THE NAIVE FIX WOULD GIVE EITHER.**  This is the
deepest finding of the panel and it comes straight from the opener's *"enumerate the right DOMAIN —
ask what the PRODUCER can emit"* instruction:

> *"Adding lane and PROM-window state mechanically gives 224 nominal tuples, but that still
> misrepresents reachability.  The MIPS producer checks natural alignment... The CRIME switch matches
> the EXACT offset, so every named label has lane bit clear.  A four-byte access to a register's low
> lane reaches `default`."*

So the lane is **not a free factor**: at width 4 with the lane bit SET, the only reachable arm is
`default`.  **The corrected enumeration is REACHABILITY-CONSTRAINED, not a cross-product** — which
means F6's remedy ("state it as the six-factor product") would itself have been wrong, just wrong in
the opposite direction.  *Two seats pushed the enumeration in opposite directions and the truth is
neither; that is what a panel is for.*

**F9b — A RECORDS FINDING NO OTHER SEAT REACHED:**

> *"The shipped probe does NOT contain a direct value assertion for accepted CONTROL `lw +0x08`.
> That access occurs through `ACCEPTS`, where its destination is subsequently overwritten.
> `devsig hi` checks REV, and `acc ctl ld` checks EIGHT-byte CONTROL.  The CONTROL equivalence
> derivation is sound, but the claimed direct supporting row is missing."*

**UPHELD, and it is consistent with everything measured** — it is precisely why `ctl4r.py` had to be
built at all, and it independently confirms the close-8 reading that table 11's `C_ctl4r` leg was
vacuous *for want of an oracle rather than for want of an access*.

**F9c — four arms whose effects the common tail does NOT reproduce**, against any argument that a
declined access is harmless everywhere: DOG's register read/write effects; INTSTAT's interrupt-LINE
update (the tail recomputes the register, not the line); TIME's update effect; REV's PC effect
inside the PROM window.

**It also independently enumerated the instrument: 51 sessions, 188 uniquely named rows** — a free
cross-check on the denominator every score in this campaign is quoted against.

---

## SEAT TALLY — 8 of 9 answered; opus running; fable HELD

| seat | transport | verdict |
|---|---|---|
| codex | CLI (file-reading) | revised coverage model needed — **after a re-fire** |
| agy | CLI (file-reading) | GO-WITH-CHANGES |
| grok | CLI (file-reading) | NOT RATIFIED as written |
| kimi | CLI (file-reading) | answered, no verdict line |
| glm | packet-fed | not clean |
| deepseek | packet-fed | REJECT AS SCOPED |
| minimax | packet-fed | real defects |
| kimi-k3 | packet-fed | do not ratify as written |
| **opus5** | Agent | **running** |
| **fable5** | Agent | **HELD BY DIRECTIVE — not a seat failure** |

**Not one seat ratified Part A.  Every seat that engaged with the mandate upheld it.**

---

## F10 — **kimi (CLI, 225 KB, 100% novel) — THREE FINDINGS, AND THE FIRST IS A HOLE IN MY OWN
## PROPOSED REPAIR.**  All three CHECKED, not judged.

**K1 — THE BRIEF DROPPED AN ESCAPE, AND PARTS A/B/C DO NOT CLOSE IT.**  UPHELD, and it is the
sharpest finding against the proposal itself.

> *"The brief says four escape types; pass 8 measured five.  The dropped one (`G_lane_ctl`) is not
> cosmetic -- it is the only evidence about the lane axis at CONTROL, and Parts A/B/C as written
> never say 'fold in `ctl4r.py`', so a repair 14 implemented literally from the brief re-opens it."*

**CHECKED:** `G_lane_ctl` appears exactly ONCE in the brief (line 171), and only as `ctl4r.py`'s
LIVENESS CONTROL -- never in the escapes table.  `grep -cE "ctl4r|lane"` over Parts A/B/C returns
**0**.  *(Cause: I wrote the brief while that leg was still in flight.  The brief was never revised
when it landed, and the verdict written afterwards has five.)*

> **SO A REPAIR 14 BUILT LITERALLY FROM MY BRIEF WOULD CLOSE TIME AND THE TWO HARD_RESET CELLS AND
> LEAVE THE LANE-AT-CONTROL CELL OPEN — which is the exact shape of the defect this entire round
> exists to fix.**  The proposal reproduced the failure it was written to end.

**K2 — THE BUCKETS ARE STALE IN TWO DIRECTIONS AND MUST BE RE-DERIVED, NOT INHERITED.**  UPHELD.
`p acc ctl msg` already counts the `0x0201` cells post-latch, so the header's "5 host-diagnostic" is
wrong in both directions at once.  **Part C must re-derive the buckets from scratch with
`scripts/buckets8.py`** -- which kimi noted exists and runs STATICALLY (confirmed: 4,665 b, present).
*A bucket count inherited across a repair is the transcribed-count class; the deriver is sitting
right there.*

**K3 — `MATCHED N, WRONG 0` CERTIFIES OUTCOME CLASSES, NOT ROW CONTENT.**  UPHELD, and it corrects a
claim of mine in the close-8 verdict, the ledger and my own reporting.  Three legs carry
`ROWS I NAMED THAT DID NOT RED` as notes inside a `MATCH`.  Corrected in place in `VERDICT.md`
section 8, together with the stale count (12 -> 13).

*kimi read the VERDICT.md that the brief was derived from and diffed the two — which is why it found
what six seats reading only the packet could not.*
