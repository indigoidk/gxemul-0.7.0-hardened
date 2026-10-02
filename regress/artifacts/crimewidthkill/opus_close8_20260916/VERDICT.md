# CLOSING PASS 8 — VERDICT: **GAP**.  #529 is NOT closed and owes REPAIR 14.

**VERDICT LINE FIRST.**  The shipped 188-row detector is escaped at **188/188 by FIVE mutants**
of the fix, out of the 23 open guest-visible cells in the 56-cell product
`{latch CLEAR, SET} × {len 4, 8} × {read, write} × {7 labels}`.  Every escape was PREDICTED
CLEAN before its own build (`scripts/check_pred8.py`: **PREDICTIONS MATCHED 13, WRONG 0** -- see the correction in section 8; this line first said 12, a count taken before the last leg landed), and
the class carries both a positive and a negative control, so the sweeps mean *no row looked*
rather than *nothing to see*.

This pass is a VALID pass in the repair-chain sense: the instrument was the shipped one, every
leg ends `CRIMEP_DONE`, the driver ends `KILL8_DONE` / `KILL8B_DONE`, and the zero that would
have closed the chain is carried **with its denominator** rather than bare.

---

## 1. THE SIX 188/188 LEGS, AND WHY ONLY FIVE ARE ESCAPES

| leg | 188-row | disposition |
|---|---|---|
| `G_glm_tim4clear` | 188/188 | **ESCAPE** — TIME, latch-CLEAR (glm's cell) |
| `G_clr_ist4r` | 188/188 | **ESCAPE** — INTSTAT 4R, latch-CLEAR |
| `G_lane_ctl` | 188/188 | **ESCAPE** — the lane decode at CONTROL |
| `K_ctl4w_reset_post` | 188/188 | **ESCAPE** — CONTROL 4W, HARD_RESET `0x800` SET (codex's generating-set cell) |
| `K_ctl8w_reset_post` | 188/188 | **ESCAPE** — the 8-byte mirror |
| `G_clr_ctl4r` | 188/188 | **NOT an escape — EQUIVALENT.  See the honesty note below.** |

### THE TWO CONTROLS, and they are what make the table mean anything

* **POSITIVE — `G_clr_imk4r` 187/188, reddening `gate line`.**  A latch-CLEAR mutant at
  INTMASK 4R that IS caught, because the GATE-RUN session drives that cell with a value oracle BEFORE its own first refusal (`crime_width_probe.py:735`, ahead of the refused `lb` at `:741`; that session calls `POST()` nowhere).  *This verdict first said "session 20", an ordinal I had not verified -- see the correction in section 7.*  So the
  latch-CLEAR state is **observable when a row exists**; the escapes above are unobserved, not
  unobservable.  *Without this line, five clean sweeps would have proved nothing at all.*
* **NEGATIVE — `G_clr_ctl4r`,** below.

### *** THE HONESTY NOTE ON `G_clr_ctl4r`, because the measurement does not quite cover it ***

CONTROL 4R is EQUIVALENT: the prelude writes `0x100` at `:231`, so the high lane is 0 either
way, and that derivation is **latch-independent** — it turns on the lane, not on `d->warned`.
`ctl4r.py` now measures that equivalence properly, with a liveness control:

    base        9/9
    C_ctl4r     9/9    <- equivalent
    G_lane_ctl  8/9    <- reds `post ctl4r' -- THE LIVENESS CONTROL

> **But the leg measured was `C_ctl4r`, the latch-SET sibling — NOT `G_clr_ctl4r` itself.**  So
> `G_clr_ctl4r`'s equivalence is DERIVED-and-inherited, not directly measured.  It is recorded
> that way rather than folded into the measured column, because a prediction written in a
> measured column is a class this project has paid for twice.

---

## 2. WHAT THE THREE OWED ROWS CATCH — and the one thing NOTHING catches

All three purpose-built probes ran; every log ends in its own sentinel.

| probe | base | catches | misses |
|---|---|---|---|
| `t4clear.py` (5 rows) | 5/5 | `G_glm_tim4clear` **3/5** (`c t4w gap`, `c t4r gap`) | **`G_clr_ist4r` 5/5** |
| `ctl4r.py` (9 rows) | 9/9 | `G_lane_ctl` **8/9** (`post ctl4r`) | — |
| `ctlreset.py` (6 rows) | 6/6 | `K_ctl4w_reset_post` **5/6**, `K_ctl8w_reset_post` **5/6** | — |

Each carries an OFF-CELL NEGATIVE CONTROL that is correctly green (`C_ctl4r` 5/5 on
`t4clear.py`; `G_glm_tim4clear` 6/6 on `ctlreset.py`), so none of them is a blunt instrument.

> ### *** SO FOUR OF THE FIVE ESCAPES HAVE A MEASURED CARRIER ALREADY BUILT, AND **INTSTAT 4R
> ### LATCH-CLEAR IS CAUGHT BY NOTHING THAT EXISTS**. ***
>
> That is the single most useful sentence this pass produced, and it is a measurement rather
> than a reading: `t4clear.py` IS the narrow repair — one purpose-built row for the cell glm
> named — and it scores `G_clr_ist4r` at **5/5**.  **A repair 14 that folds in the three owed
> rows as-built would close four cells and ship believing it had closed the class.**

---

## 3. WHAT TABLE A SETTLED (14 of 14, `KILL8_DONE`)

The four legs that were TRUNCATED at the owner's 2026-09-16 pause were **re-run, not read** —
the sentinel rule catching exactly the case it exists for — and all four now carry
`CRIMEP_DONE`:

    W_rev4r_out   188/188   the fourth PC-window leg: EQUIVALENT
    G_lane_ist    188/188   the lane bit is UNSATISFIABLE at an 8-aligned label
    G_lane_tim    188/188   likewise
    G_lane_all    185/188   KILLED at the default arm, where the lane IS satisfiable

Plus the two legs that had never started: `D1_landpost` **183/188** and `D2_remappost`
**180/188**, both killed.

**TWO AXES THE ENUMERATION NEVER NAMED ARE THEREFORE MEASURED CLOSED** — `relative_addr & 4`
(the lane, tested at `:291`) and `cpu->pc` (the PROM window at `:344`).  Both are RECORDS
defects, not floor gaps.  `W_rev8r_out` 187/188 reddening `p rev ld` ONLY is the positive
control that makes the three 188/188 window legs mean EQUIVALENCE.

---

## 4. *** A RECORDS TRAP THIS RESUME CREATED, written down before it can mislead ***

`scripts/check_pred8.py` reads the **lane files**, and the resume run overwrote
`logs/lane0..3.out`.  It therefore now reports the EIGHT pass-1 legs as **NOT RUN**.

**They ran, they are valid, and their tallies are preserved at `logs/pass1_preserved/`**
(`lane0..3.out`, `table8.out`, `INSTRUMENT.md5`), copied BEFORE the re-run could clobber them.
*NOT RUN and NOT IN THIS FILE must not render the same* — this project's oldest rule about
blanks, met by a tool that is working exactly as designed on an input that moved underneath it.

## 5. AN APPARATUS NOTE, because it nearly cost a wrong reading

Mid-run, `ps -ef | grep -E 'gxemul|kill8b'` returned **nothing** while `G_lane_ctl` was very
much alive (pid 20924).  On this machine git-bash `ps -ef` prints the executable path and no
arguments, so a pattern naming a SCRIPT can never match and the check answers "dead" always.
**The real signal was the redirect target**: `probe188_G_lane_ctl.raw` growing, and carrying no
`CRIMEP_DONE`.  Mid-probe, not dead.

## 6. WHAT REPAIR 14 OWES

Closing pass 7 found the latch-SET half of this class; closing pass 8 found the latch-CLEAR
half **and** the generating-set cell.  **Two consecutive passes, one class** — so the
repair-chain amendment applies and repair 14 owes **CLASS CLOSURE IN ONE DIFF**, not five rows
for five cells.  The design brief is `../repair14_20260916/PASS1_brief.md`; its panel pass 1 is
running.  Fable is deliberately held until every other seat has answered.

---

## 7. *** CORRECTION, 2026-09-17, FROM REPAIR 14's PANEL PASS 1.  A PREMISE THIS VERDICT INHERITED
## IS FALSE, AND TWO SEATS FOUND IT INDEPENDENTLY FROM THE PACKET ALONE. ***

The close-8 record — and the repair-14 brief built from it — carried this claim:

> *"The latch-CLEAR state is driven by session 40 (`latch x5`) ALONE, and that session's only three
> rows are two announce COUNTS and a RAM round-trip, all blind to a silent decline."*

**IT IS FALSE.**  `ollama_glm` and `ollama_kimi` each derived the contradiction without repo access:
a latch-SET row cannot red a latch-CLEAR mutant, because the conjunct is inert once
`d->warned & CRIME_W_LEN` is set — so `G_clr_imk4r` being KILLED at 187/188 via `gate line` is
impossible if session 40 is the only latch-CLEAR driver.

**SETTLED BY READING THE PROBE, not by choosing between the two claims.**  The gate-run session
contains **no `POST(` call at all**, and its INTMASK 4-byte read precedes its first refused access:

    733| x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
    735| x, _ = ld(A, "lw", CRIME + 0x18, "a0"); c += x     <-- INTMASK 4R, LATCH STILL CLEAR
    741| x, _ = ld(A, "lb", CRIME + 0x08, "t1"); c += x     <-- the FIRST refusal in this session

**WHAT SURVIVES UNCHANGED: every measurement in sections 1–5.**  The five escapes, the two controls,
the three owed rows and the INTSTAT-4R-caught-by-nothing finding are all measured and none of them
depends on the refuted premise.

**WHAT CHANGES IS THE EXPLANATION, and it gets better rather than worse.**  "The latch-CLEAR half is
unobserved" was too strong.  The true criterion is sharper, derivable by reading, and it explains
all three outcomes at once instead of two:

> **A latch-CLEAR cell is COVERED exactly when some session drives it BEFORE that session's first
> refused access, with an oracle that observes it.**

`G_clr_imk4r` is killed because INTMASK 4R is driven pre-refusal at `:735`.  `G_clr_ist4r` and
`G_glm_tim4clear` escape because nothing drives those cells pre-refusal with an oracle.  **So repair
14 is priced PER CELL rather than by mirroring every session**, which is a materially cheaper and
better-warranted repair than the one the brief proposed.

*Recorded here rather than left to the brief, because this verdict is what a future round will read
first, and a wrong premise gets reused.  Full disposition: `../repair14_20260916/FINDINGS_pass1.md`.*

---

## 8. *** SECOND CORRECTION, FROM THE kimi SEAT: THE `MATCHED N, WRONG 0` CLAIM IS WEAKER THAN I
## WROTE IT, AND THE N WAS STALE. ***

**(a) THE COUNT.**  This verdict said **12**.  Re-running the checker now that every leg has landed
gives **13**.  My 12 was taken while `G_lane_ctl` was still in flight -- I said so at the time, and
the number still went into a durable record where a later reader would reuse it.  *That is the
frozen-number class: a count written before the thing it counts has finished.*

**(b) THE CLAIM, and this is the substantive half.**  kimi:

> *"`MATCHED N, WRONG 0` certifies OUTCOME CLASSES, not the named-row content of predictions."*

**CONFIRMED by running the checker and reading what it prints.**  Three legs carry row-name misses
as NOTES *inside* a `MATCH` verdict:

    D2_remappost  180/188  MATCH  ROWS I NAMED THAT DID NOT RED: p rev ld, p acc ctl ld.  ALSO RED: ...
    G_lane_all    185/188  MATCH  ROWS I NAMED THAT DID NOT RED: p rev lw4.
    G_clr_imk4r   187/188  MATCH  ROWS I NAMED THAT DID NOT RED: gate run.

So `13, WRONG 0` means **thirteen legs landed in the predicted KILL/CLEAN class**.  It does NOT mean
thirteen per-row predictions were exact -- three were not, and the checker said so in a column I read
past.  **The predict-then-measure discipline still holds and the escapes are unaffected**, because an
escape is an outcome-class claim.  What is corrected is the STRENGTH of the certificate.

*The checker was right, printed the truth, and I quoted its headline instead of its body -- which is
this project's own "read the body of any seat whose verdict merely agrees", turned on a tool.*
