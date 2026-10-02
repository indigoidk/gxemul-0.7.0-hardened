# THE ADJUDICATION PASS — RESULT.  8 of 8 scriptable seats answered, 0 walled, 0 down.

Panel dir `_scratchpad/panel_20260917_004011/`.  **codex did NOT refuse this pass** (354 KB, 95%
novel) even though the packet quotes mutant code — the adjudication framing (*attack the
dispositions*) is evidently far enough from *"build me an edit that re-opens this"*.

> ### *** THE PASS DID ITS JOB: IT REFUTED THE FINDING I HAD CALLED "THE FINDING OF THE ROUND". ***

---

## J1 — **O1 IS WRONG.  THREE SEATS, INDEPENDENTLY, AND THE PACKET REFUTES IT FROM THE INSIDE.**

I accepted O1 — *the decline arm is a second 56-cell product `{len 1,2} × {R,W} × {7 labels} ×
{latch}`, so the space is 112* — and called it the finding of the round.  **agy, glm and deepseek
each rejected it, on three different grounds that all hold.**

> **agy:** *"The decline arm is NOT a second 56-cell product.  `dev_sgi_ip32.c:296-320` and
> `:411-423` prove the decline arm has **no switch statement** and never branches on
> `relative_addr`."*

> **deepseek:** *"O1's 56 is an analogy contradicted by a DERIVED figure — the packet's own O4
> derives 7 decline × latch-set cells, and O4's discriminator asks only whether a session refuses at
> a label more than once.  It does not mention `len` or `R/W`."*

> **glm:** *"O1 contradicts the A10 you accepted IN THE SAME ROUND — cross-product by analogy, not
> derivation from the decline code, which the packet shows consulting only the latch.  Derived, the
> decline arm is 7 labels × 2 latch states = **14**, of which 12 are covered or equivalent and 2 are
> exactly the rows O4 derived."*

**ALL THREE ARE RIGHT, AND THE SHARPEST IS glm's: I ACCEPTED A10 AND O1 IN THE SAME DOCUMENT AND
THEY ARE THE SAME ERROR WITH OPPOSITE SIGNS.**  A10 (codex) says *the accept side is
reachability-constrained, not a cross-product* — and I accepted it.  O1 then builds the decline side
**as a cross-product by analogy**, and I accepted that too, in the same breath, without noticing.

**AND O1 CONTRADICTS O4 INSIDE ONE ANSWER.**  Verified by opening it: `opus_pass1.md:26-27` asserts
the four-factor product; `:215` is headed *"THE WHOLE DECLINE × LATCH-SET AXIS, DERIVED — SEVEN
CELLS, TWO OPEN"*.  **A derivation and an analogy about the same arm, four screens apart, and I
ratified both.**

### THE RESIDUAL QUESTION, which the seats do NOT settle between them and which I will not paper over

agy's ground is stronger than glm's arithmetic and they are not quite compatible:

* **agy:** the arm *itself* never branches on `relative_addr`, so the label is not a factor of the
  arm's partition **at all**.  The arm's own partition is `{latch clear, set}` — **2 cells**.
* **glm:** the label enters as **7 × 2 = 14**, matching O4's derived 7-at-latch-set.

**Both can be true of different things, and naming which is the whole point:** the label is not a
partition of the ARM, but it IS a partition of the MUTANT SPACE over the arm — a future edit can
condition the `goto` on `relative_addr`, which is exactly what `M3_timelatch` does and why it scores
188/188.  So *"what partitions the decline arm"* and *"what a (d) DEPENDS-ON enumeration over the
decline arm must cover"* are different questions with different answers, and O1 conflated them.

> **DISPOSITION: O1 IS WITHDRAWN AS STATED.**  The decline arm's own partition is `{latch}`; the
> mutant space over it is `{labels} × {latch}` = 14 by O4's derivation, of which **2 are open (REV
> and TIME)**.  **112 is wrong; the real figure is 56 accept-side + 14 decline-side mutant cells.**
> *O4 — the derived half of the same answer — survives intact and is what repair 14 acts on.*

---

## J2 — **minimax: my A2 evidence was INSUFFICIENT, and it was right.**  Conclusion survives, warrant
## replaced.

> **minimax:** *"A2's 'SETTLED BY READING' is overclaimed.  For the evidence to refute P4 ('CLEAR
> driven by session 40 alone'), the gate-run session must be a DIFFERENT session from session 40.
> The brief never states this.  If gate-run = session 40, the evidence shows session 40 IS a CLEAR
> driver — consistent with P4, not evidence against it."*

**CHECKED, AND minimax IS RIGHT ABOUT THE WARRANT.**  My cited evidence — *the gate-run session calls
`POST()` nowhere and drives INTMASK 4R at `:735` before its first refusal at `:741`* — is entirely
consistent with gate-run BEING session 40.  It does not establish what I claimed.

**THE SUFFICIENT EVIDENCE EXISTS AND I HAD NOT CITED IT.**  `BUCKETS8_rerun.out` entry 25:

    25    lw     +0x18    IMK    [20, 40]    <- TWO DISTINCT SESSIONS drive it latch-CLEAR

Session 40 is `latch x5`; session 20 is the gate-run one.  **They are different, so P4's "ALONE" is
false — but on the buckets output, not on the reading I gave.**

> ### *** THAT IS THE THIRD TIME THIS ROUND A SEAT HAS FOUND MY *REASON* WRONG WHILE MY *CONCLUSION*
> ### HELD (F3/agy, O2/opus, now J2/minimax).  THE PATTERN IS WORTH NAMING: I have been reaching
> ### right answers by routes that do not carry them, and a wrong reason gets reused. ***

## J3 — minimax on A13: the packet asserted a correction without showing its arithmetic.  **UPHELD as
## a PACKET defect, not an arithmetic one.**

> *"A delta of +1 against three over-counted legs is not internally consistent: if those three legs'
> rows were removed from MATCH, the count should fall, not rise."*

The count rose 12 → 13 because a **thirteenth leg landed** (`G_lane_ctl`) after I wrote 12 — not
because of the row-note issue, which is independent.  **minimax could not know that: the packet said
"stale (12 → 13)" and never said why.**  A correction whose arithmetic is not shown is not checkable,
which is this project's own rule turned on my own correction.

## J4 — glm: two more of my acceptances are overstated.  **UPHELD, both.**

* *"'O1 supersedes D1 entirely' — O8 itself demotes codex's reachability to CONDITIONAL"* (it holds
  only because `DEV_CRIME_LENGTH` is `0x280`, a multiple of 8), *"and the routing of split widths is
  unsettleable here."*  **So D1 is NOT superseded; it is narrowed and still open.**
* *"'O7 answers the 4b residual doubt' — O7 is a DIFFERENT blindness mechanism and leaves the
  third-session question untouched."*  **Correct:** O7 is about buckets whose members cannot be
  listed; my 4b doubt was about a third session passing the `26-or-40` test while carrying no oracle
  for a channel.  Two different holes, and I collapsed them.

---

## WHAT SURVIVES, AND IT IS THE PART REPAIR 14 IS BUILT ON

* **O3 — the measured two-line total escape at 188/188 (`M3_timelatch`), with its discriminating
  control at 184/188.**  Unchallenged by any seat.
* **O4 — the decline × latch-set axis, 7 cells, REV and TIME open.**  *Strengthened* by J1: it is the
  derived figure that refutes its own answer's analogy.
* **O5/O6 and section 4b — the nine pre-blind entries, confirmed by two independent tools.**
* **The MANDATE** — class closure in one diff — which no seat has disputed across two passes.

**STILL OPEN AND CARRIED FORWARD, not closed:** D1 (narrowed, conditional on `DEV_CRIME_LENGTH`);
the third-session sufficiency question from 4b; and whether the decline-side mutant space is 14 or
something else once `len`/direction are properly dispositioned rather than assumed.
---

## J5 — **grok REVERSES A REVERSAL: O2's REDIRECT IS WRONG, AND MY ORIGINAL AIM WAS RIGHT.**
## *Settled by reading the code, and grok used the measuring seat's own numbers against it.*

O2 (the Opus seat) said P3 was false — *the K-form is LOUD, not silent; it escapes because the
announce is STOLEN* — and concluded that **reasoning from silence points the repair at the wrong
channel.**  I accepted that and re-aimed the design.

> **grok:** *"P3's latch-CLEAR conjunct: on that code, latch CLEAR does fall into the `else`, does
> set the latch, does print.  Stolen-announce is the channel for THAT mutant, and `latch said`
> already implements it — G1–G5 at 141/141, already shipped.  **Close-8's ESCAPING mutants are not
> that form.**  They are the G-form (goto before the width test: `G_clr_ist4r`, `G_glm_tim4clear`,
> `M2_ld278clr`) and the POST-LATCH K-form (`K_ctl*w_reset_post`).  Those print nothing.
> Stolen-announce cannot move.  **Aiming repair 14 at a stolen count closes a form the 188-row
> instrument already kills and leaves the five 188/188 legs untouched.**"*

**CHECKED AGAINST THE CODE, AND IT HOLDS EXACTLY.**  The announce block is gated on the latch being
CLEAR:

```c
 314| 		if (!(d->warned & CRIME_W_LEN)) {
 315| 			d->warned |= CRIME_W_LEN;
 316| 			fatal("[ crime: unimplemented len=%i at 0x%x -- declined.  (once) ]\n", ...);
 317| 		}
 319| 		goto crime_declined;
```

* **post-latch K-form** — the latch is already SET, so the `if` is FALSE: **no print**;
* **G-form** — the `goto` precedes the width test, so the whole `else` is bypassed: **no print**.

**So none of the five escaping mutants prints anything**, and the rows that kill their neighbours
are not counts: `t4clear.py` kills TIME on a VALUE (`c t4w gap`, `c t4r gap`, 3/5) and `gate line`
(`crime_width_probe.py:748`) is `ip2(nth(t, "cause", 0))` — a **reassert observable**.

> ### **DISPOSITION: O2's SPLIT IS KEPT; O2's REDIRECT IS WITHDRAWN.**
>
> P3 was false **as stated** (K-code described with G-behaviour) — that half of O2 stands and is
> worth keeping, because the two forms really are different.  But the brief's **AIM** — value oracles
> for a silent decline — **is the right aim for the mutants that actually escape.**  grok's own
> summary is the disposition: ***keep the split; drop the redirect.***

**WHY THIS MATTERS MORE THAN A TIDY-UP:** I had already re-aimed the repair design at announce
counts on O2's authority.  Had that shipped, repair 14 would have added rows for a form the shipped
188-row instrument **already kills at 141/141**, and all five measured escapes would have survived it
untouched — the round's own failure mode, reached by accepting a correction.

*This is the panel correcting the measuring seat, on the measuring seat's own measurements, and it
is the clearest vindication of the adjudication pass in this campaign: without it I would have
shipped a repair aimed at the wrong channel with nine seats' apparent blessing.*
