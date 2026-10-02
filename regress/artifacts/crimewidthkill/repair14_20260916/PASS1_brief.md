# #529 `crimewidthkill` — REPAIR 14 design brief (panel pass 1)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. WHAT IS BEING REPAIRED — and it is the DETECTOR, not the product code

`#529` de-fatalised a guest-drivable host kill in `src/devices/dev_sgi_ip32.c`: any narrow
(`lb/lbu/lh/lhu/sb/sh`) access anywhere in CRIME used to end the process.  **That fix shipped
and is NOT under review here.**  What is under review is the DETECTOR that defends it —
`regress/crime_width_probe.py`, currently **188 rows**, and whether it can see the fix
being re-broken.

Repair 13 grew it 157 → 188 rows.  **Closing pass 8 has now measured that repair 13 closed
exactly one half of the space and left the mirror open.**  This brief proposes repair 14.

---

## 2. SETTLED PREMISES — re-inlined so nobody spends an answer re-deriving them

Each is a RECORDED resolution with its warrant.  Challenge any of them; do not assume them.

**P1 — THE FULL ENCLOSING FUNCTION.**  `DEVICE_ACCESS(crime)` in
`GXEMUL-SEC/src/devices/dev_sgi_ip32.c`.  The width decline and the common tail, verbatim:

```c
 296| 	} else {
 297| 		/*
 298| 		 *  #529: THIS USED TO END THE PROCESS.  One guest lb, lbu, lh,
 299| 		 *  lhu, sb or sh anywhere in CRIME did it (witnessed at rung 3
 300| 		 *  on an unmodified -E sgi -e ip32, 6/6).  The width is now
 301| 		 *  DECLINED and announced once, the #498 sgi_de shape: a read
 302| 		 *  is answered 0 through the common tail, a write is dropped.
 303| 		 *  [ ... 10 further comment lines ... ]
 313| 		 */
 314| 		if (!(d->warned & CRIME_W_LEN)) {
 315| 			d->warned |= CRIME_W_LEN;
 316| 			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
 317| 			    "  (once) ]\n", (int) len, (int) relative_addr);
 318| 		}
 319| 		goto crime_declined;
 320| 	}
 321|
 322| 	switch (relative_addr) {
 324| 	case CRIME_REV:		/*  0x000  */
 353| 	case CRIME_CONTROL:	/*  0x008  */
 383| 	case CRIME_INTSTAT:	/*  0x010  */
 384| 	case CRIME_INTMASK:	/*  0x018  */
 388| 	case CRIME_DOG:		/*  0x030  */
 392| 	case CRIME_TIME:	/*  0x038  */
 396| 	default:
 409| 	}
 410|
 411|  crime_declined:
 412| 	/*  #529: a declined access jumps here, skipping the register switch,
 413| 	    and is still answered.  */
 414| 	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
 415| 	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
 416| 		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
 417| 		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);
 418|
 419| 	if (writeflag == MEM_READ)
 420| 		memory_writemax64(cpu, data, len, odata);
 421|
 422| 	return 1;
 423| }
```

**Note the tail is COMMON and `crime_declined` is reached by `goto`, not by `return`.**  An
edit that returns early here skips the interrupt recomputation AND `memory_writemax64`, which
is a defect the shipped code does not have.  *(Four independent readers once proposed exactly
that shape on a different device, none having read nine lines down.)*

**P2 — THE ENUMERATION IS 56 CELLS, and here are the members rather than the total.**
`{latch CLEAR, latch SET} × {len 4, len 8} × {read, write} × {REV, CONTROL, INTSTAT, INTMASK,
DOG, TIME, default}` = 2 × 2 × 2 × 7 = **56**.  The seven labels are exactly the `case` arms
inlined in P1 — six named plus `default:`.

**The FLOOR is not 56 and not 28.**  It is the **23 open guest-visible cells** — the
INTERSECTION of the mutants that can be built with the rows that could observe them.  The full
disposition of the 46 ACCEPTS entries is: **23 rowed / 8 already-pinned / 10 equivalent /
5 host-diagnostic**.  *Is 23 the right floor?  That is question Q3 below.*

**P3 — THE MUTANT SHAPE.**  Every escape in this family is the accept guard grown with a
conjunct on the fix's OWN latch:

```c
    && !(<cell> && (d->warned & CRIME_W_LEN))       /* the latch-SET half — repair 13 closed this */
    && !(<cell> && !(d->warned & CRIME_W_LEN))      /* the latch-CLEAR half — STILL OPEN */
```

It declines **silently**: no message, no latch write, host alive.  **A row that only checks
"the host survived" cannot see it, by construction.**

**P4 — REPAIR 13'S DISPOSITION, and why it left a mirror.**  Repair 13 added six POST sessions
(`P1`–`P6`), each opening with `POST(A)` — a *refused* `lb` at `+0x07` whose only job is to set
`d->warned & CRIME_W_LEN` before anything else in the session:

```python
def POST(A):
    """A refused lb at +0x07 sets d->warned & CRIME_W_LEN before anything else in the session."""
    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
    return x
```

So **every row repair 13 added runs with the latch SET**.  The latch-CLEAR state is driven by
session 40 (`latch x5`) ALONE, and that session's only three rows are two announce COUNTS and
a RAM round-trip — all blind to a silent decline.

**P5 — THE MEASURED RESULT OF CLOSING PASS 8.**  Kill table, shipped 188-row instrument, every
leg ending `CRIMEP_DONE`, scored mechanically by `check_pred8.py` against predictions whose
mtimes predate the first build log: **PREDICTIONS MATCHED 12, WRONG 0.**

| leg | score | reading |
|---|---|---|
| `G_glm_tim4clear` | **188/188** | **ESCAPE** — TIME, latch-CLEAR |
| `G_clr_ist4r` | **188/188** | **ESCAPE** — INTSTAT 4R, latch-CLEAR |
| `K_ctl4w_reset_post` | **188/188** | **ESCAPE** — CONTROL 4W with HARD_RESET 0x800 SET |
| `K_ctl8w_reset_post` | **188/188** | **ESCAPE** — the 8-byte mirror |
| `G_clr_imk4r` | 187/188 | **POSITIVE CONTROL** — killed, reds `gate line` |
| `G_clr_ctl4r` | 188/188 | **NEGATIVE CONTROL** — CONTROL 4R is derived-EQUIVALENT |

**The two controls are what make the four escapes mean "no row looked" rather than "nothing to
see".**  `G_clr_imk4r` proves the latch-CLEAR state IS observable when a row exists (session 20
drives INTMASK 4R with a value oracle).  `G_clr_ctl4r` is the class's own boundary: the prelude
writes `0x100` at `:231` so the high lane is 0 either way.  *A clean sweep with neither control
would have proved nothing at all.*

**P6 — THE GENERATING-SET CLAUSE this breaches.**  *"At each floor cell, every idata bit the
guarded body TESTS is written both clear and set."*  The CONTROL arm tests DOG `0x200`,
HARD_RESET `0x800` and the leftover.  **Every post-latch CONTROL write in the 188-row probe
carries HARD_RESET CLEAR** — `0x01`, `0x0001`, `0x0201`, and session 26's ACCEPTS values — and
**the only `0x800` write in the whole probe (`sw08 halts`, session #2) is PRE-latch.**  So the
(HARD_RESET set × post-latch) cell is driven by nothing.

**P7 -- THE THREE OWED ROWS ARE ALREADY BUILT AND MEASURED, AND ONE OF THEM ARGUES AGAINST
THE NARROW REPAIR.**  Closing pass 8 ran three purpose-built probes beside the 188-row
instrument.  All logs end in their own sentinel (`CTL4R_DONE`, `T4CLEAR_DONE`, `CTLRESET_DONE`).

`ctl4r.py`, 9 rows -- **settles the CONTROL-4R equivalence claim by MEASUREMENT rather than by
derivation**, which is what POSTTABLE 11 recorded as owed:

    base        9/9
    C_ctl4r     9/9    <- the cell is EQUIVALENT
    G_lane_ctl  8/9    <- reds `post ctl4r' -- THE LIVENESS CONTROL

*Without that third line the 9/9 would be the same vacuity table 11 shipped.  With it, the
equivalence is a measurement.*

`t4clear.py`, 5 rows -- the latch-CLEAR owed row (the gapped TIME shape MINUS the opening
refusal):

    base              5/5
    G_glm_tim4clear   3/5    <- reds `c t4w gap', `c t4r gap' -- THE TIME CELL IS CAUGHT
    C_ctl4r           5/5    <- off-cell negative control, correctly green
    G_clr_ist4r       5/5    <- *** STILL ESCAPES ***
    G_clr_ctl4r       5/5    <- expected (equivalent cell)
    G_clr_imk4r       5/5    <- expected (already caught by the 188-row probe)

**THIS IS THE LOAD-BEARING MEASUREMENT OF THE WHOLE BRIEF, AND IT CUTS AGAINST THE CHEAP
OPTION.**  `t4clear.py` IS the narrow repair -- one purpose-built row for the cell glm named.
It kills that cell and **leaves INTSTAT 4R open**.  So a repair 14 that adds the owed rows
as-built would close one of the two open latch-CLEAR members and ship believing it had closed
the class.

`ctlreset.py`, 6 rows -- the generating-set row for codex's cell:

    base                  6/6
    K_ctl4w_reset_post    5/6    <- reds `post rst 4w'
    K_ctl8w_reset_post    5/6    <- reds `post rst 8w'
    G_glm_tim4clear       6/6    <- off-cell negative control, correctly green

**Both generating-set mutants are killed, with a negative control proving the row is not a
blunt instrument.**  Part B below is therefore measured-complete rather than proposed.

---

---

## 3. WHAT THE REPAIR-CHAIN RULE DEMANDS OF REPAIR 14

Closing pass 7 found the latch-SET half of this class.  Closing pass 8 found the latch-CLEAR
half **and** the generating-set cell.  **Two consecutive passes, one class** — which triggers:

> *"WHEN TWO CONSECUTIVE PASSES FIND BREACHES OF ONE CLASS, THE NEXT REPAIR OWES THE CLASS
> CLOSURE: enumerate the full space from the function's own inputs, close every cell in ONE
> diff, and write into the CONTRACT which cells are covered and which are deliberately not.
> The closing pass then VERIFIES THE ENUMERATION rather than hunting cells."*

**So repair 14 may not add three rows for the three escaped cells.**  That is the cell-by-cell
chain the amendment exists to end, and it converges linearly while each pass costs a table.

---

## 4. THE PROPOSED REPAIR — state it as a target, not as a decision

**PART A — a PRE-LATCH MIRROR of the post-latch sessions.**  For every open guest-visible
cell, drive it in a session that does **NOT** open with `POST(A)`, carrying that cell's own
value oracle rather than an announce count.  That closes `{latch CLEAR} × {the rowed cells}`
in one diff instead of one cell at a time.

**PART B — the generating set at CONTROL.**  At every rowed CONTROL cell, write HARD_RESET
`0x800` **both clear and set**, post-latch as well as pre-latch, so any conjunct keyed on that
bit lands a write and reds a readback.

**PART C — the contract.**  Write into the probe header which of the 56 cells are ROWED, which
are EQUIVALENT with the derivation, and which are DISCLOSED — so a later escape is "outside the
contract, as stated" rather than a fourth breach.

**THE OBVIOUS OBJECTION, and I want it pressed rather than waved past:** a pre-latch session
cannot contain any refused access at all, or it sets the latch and becomes a post-latch session
from that point on.  **Does that make some cell unreachable pre-latch?**  I believe not — the
accesses under test are all *legal widths*, so they refuse nothing — but that is a premise, and
it is the one this repair rests on.

---

## 5. QUESTIONS

**Q1 — THE PREMISE AUDIT.**  Six premises above (P1–P6) are load-bearing, stated as claims.
Which is false?  In particular: *is the 56-cell product the right enumeration, or does the
handler partition on an axis it does not name?*  Two such axes were found and measured closed
in pass 8 — `relative_addr & 4` (the lane, tested at `:291`) and `cpu->pc` (the PROM window at
`:344`).  **Are there others?**

**Q2 — WHAT IS THE SMALLEST EDIT that breaks the fix and still passes repair 14 as proposed?**
Name the row you expect to stay green.  This question has the highest recorded per-invocation
yield in this project; it is the reason to answer it concretely rather than generally.

**Q3 — OPTION-SET COMPLETENESS ON THE FLOOR ITSELF.**  I claim the floor is the 23 open
guest-visible cells, with 8 already-pinned / 10 equivalent / 5 host-diagnostic.  **Is a cell
mis-filed?**  An "equivalent" cell that is actually observable is a floor breach wearing a
disclosure's clothes, and the `C_ctl4r` leg in table 11 was exactly that — it scored 188/188
not because the cell was equivalent but because the one session driving it had no oracle.

**Q4 -- round-specific, and P7 has already moved it.**  Part A proposes a pre-latch MIRROR.
The cheap alternative -- fold in the three owed rows as built -- is now MEASURED INSUFFICIENT:
`t4clear.py` kills TIME and leaves INTSTAT 4R at 5/5.  So the question is no longer *mirror or
narrow row*; it is **how wide the mirror must be**.  Does it need every rowed cell, or do some
cells' two latch states collapse provably?  If some collapse, say WHICH and give the warrant --
and note that `C_ctl4r` is the one cell where collapse is now measured rather than argued
(`ctl4r.py`, 9/9 with a liveness control at 8/9), so it is the template for what a collapse
claim has to look like.

---

If, while verifying a claim, you found something ELSE — say so.
