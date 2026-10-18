# `#564` sgirekills (MTE half) -- §F2 FOR PASS 3: ONE SCOPE QUESTION, THREE POSITIONS

## READ THIS FIRST

Pass 3 (the repair's own review) split on whether three groups of cells are inside the vacuity floor -- owed a row
AND a measured kill -- or outside it, disclosed under clause (e).  The working seats rule on that by owner ruling
(Fable 5.1 is held, walled at HTTP 429 three times this round).  **The governing rule texts are quoted verbatim in
section 3, so please rule from the text, not from memory.**  Count arguments, not seats.  If you raised a group, be
HARDER on it; if a position is adopted in your favour, test it more, not less.

**THE TREE** is `GXEMUL-SEC/` at HEAD `2951694f` plus this round's uncommitted edits (the 68-row detector, md5
8928a02f; `dev_sgi_re.c` 23fa76aa).  **VERDICT LINE FIRST.**

## 1. The facts every position agrees on

* S1 (`mode & MTE_MODE_STIPPLE`) and S2 (`src > MTE_TLB_C`) are guards BEFORE `switch (dst_tlb)`; their `return` bypasses
  the dispatch.  S3 (`mode & MTE_MODE_COPY`), S4 (`depth != 8`) and S5 (`bytemask != 0xffffffff`) are guards INSIDE
  `case MTE_TLB_LIN_A: case MTE_TLB_LIN_B:`; their `return` bypasses only the linear fill that follows.  Each site's
  repair is `if (!(d->warned & BIT)) { d->warned |= BIT; fatal(...); } return;` -- it reads and writes its own latch
  bit.  The S3-S5 messages print `dst_tlb`; nothing in a decline body compares it.  After S5 the fill selects
  `dst_tlb == MTE_TLB_LIN_A ? d->re_linear_a : d->re_linear_b`.
* Kill table 3 (68-row instrument): 29/29, including all 20 latch-conditioned REFUSE-face label exemptions of S1/S2
  (each red on its own cell's row), five latch aliases, and S1/S2 grown to refuse every transfer to B or to C.
* Held today: every REFUSE-face cell of S1/S2 (20); the ACCEPT face of S1/S2 with the latch CLEAR at all five labels
  (`tile mask`, `fill b ok`, `fill c ok`, `lin fill a`, `lin fill b` -- one ACCEPT session, every latch clear) and with
  the latch SET at A (`after fill`; `src c fill`) and, indirectly, LIN_A (a grown guard refuses the later S3-S5
  transfers of the latch and crossbit sessions before they announce); S3/S4/S5 refuse at LIN_A CLEAR, and at LIN_B
  SET; S4/S5 refuse at LIN_A SET; S3/S4/S5 accept at both labels CLEAR, and S3/S4 accept at LIN_A SET (indirectly).

## 2. The three groups, and the three positions

| group | cells not held today | Astra | GLM | Grok |
|---|---|---|---|---|
| **G1** S1/S2 ACCEPT face x label x latch SET | S1 at B, C, LIN_B; S2 at B, C, LIN_B -- e.g. `if (src > MTE_TLB_C \|\| (dst_tlb == MTE_TLB_B && (d->warned & SGIRE_W_MTE_SRC)))` passes all 68 | definite hole; "cannot certify floor closure from the supplied rule text" | -- | outside: latch-conditioned accept growth is a named clause-(e) limit (PRETABLE3 section 3) |
| **G2** S5 ACCEPT face with its latch SET | one -- `if (bytemask != 0xffffffff \|\| (d->warned & SGIRE_W_MTE_BYTEMASK))` refuses every legal linear fill after the first S5 decline; no session drives one | definite hole | -- | (not discussed) |
| **G3** S3/S4/S5 label x latch | S3 refuse LIN_A SET and LIN_B CLEAR; S4 and S5 refuse LIN_B CLEAR; S3/S4/S5 accept LIN_B SET (and S5 accept LIN_A SET = G2) | -- | inside only if the 09-25 construction transfers to in-arm guards; "the single fact that settles it is the clause's wording" | outside: the 09-25 disjunct is the BYPASS, which in-arm returns do not have; the 09-09 clause bounds labels to `{labels} x the guard operand's partition` |

## 3. THE MAIN LOOP'S PROPOSED DISPOSITION -- please test it

* **G3: OUTSIDE (clause e).**  The 09-25 third disjunct applies only "when the edited guard's repair bypasses that
  dispatch"; an in-arm `return` does not.  The 09-09 clause does reach S3-S5 (each body reads `dst_tlb`), but it fixes
  the product: "{labels} x the guard operand's body-tested partition ... never the labels' cross-product with
  everything" -- {LIN_A, LIN_B} x {COPY / depth / mask: refused, accepted}, all held (`copy lin a/b`, `lin fill a/b`,
  `depth a/b *`, `mask *`, `mask lin b`).  The latch is not the guard operand.  Disclosed in the contract.
* **G1: OUTSIDE (clause e), and this is the one most worth attacking.**  The 09-25 clause crosses the skipped labels
  with "the guard's dominating predicates and the jointly reachable device-state lvalues read by the fix's own repair
  path, as defined by pass 11".  The pass-11 floor is "the cross-product of the guard's DOMINATING predicates with the
  device-STATE lvalues the fix's own repair path reads".  The main loop reads "the guard's dominating predicates" as the
  predicates that dominate the guard -- S1 has none in the function, S2 has S1 -- so the label x latch product lives on
  the face where the repair path RUNS, the refuse face (the 20 cells table 3 measured).  The ACCEPT face of each guard
  is the accept-row failability rule's ground (one growth mutant per predicate: `s1grow`, `s2down`, measured in tables
  1-2) plus the plain label growths `s1gb/s1gc/s2gb/s2gc` (table 3); a growth CONDITIONED on the latch is a combination
  "the body never tests as a case" on that face.  **The counter-reading:** the guard dominates its own repaired body,
  so the guard's own partition {true, false} is in the product, and the accept face x label x latch is floor -- 20
  cells per site, 6 not held.  If that reading is right, the next repair owes 6 rows and their measured kills.
* **G2: the same question as G1 for S5, without labels.**  Under the main loop's reading, S5's accept face with the
  latch SET is outside (clause e); under the counter-reading it is floor and owes one row.

## 4. The rule texts, verbatim from the project carrier (`CLAUDE.md`)

### 4a. The joint-cell rule (2026-09-04)

> > **DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues EXACTLY
> > WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM.**  For each lvalue take the PARTITION the
> > body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives
> > {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary
> > boolean functions of the read-set.  A mutant exempting a single cell whose reachability is
> > MEASURED is a floor breach; close the whole cross-product in ONE diff and write into the
> > contract which cells are rowed.  A value or combination the body never tests as a case
> > (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`)
> > is DISCLOSED under clause (e).

### 4b. The floor, as bounded on pass 11 (2026-09-04)

> #### *** THE LETTER OVER-DEMANDED, AND ITS OWN AUTHOR BOUNDED IT ONE PASS LATER (pass 11, 2026-09-04). ***
>
> Read literally, "the cross-product of the body-tested partitions" demanded ALL 128 cells at the TxICR
> arm -- the body also tests `idata & IEN`, `idata & ICLR`, the register's INT bit and `idata & 0xe0` --
> and it compounds as 2^k in the `if`-count across twelve arms: the `#392` shape wearing the rule's
> clothes.  Three seats said the letter demands the remainder; the flagship seat, asked to be harder on
> its own rule than on anyone, ruled AGAINST the letter:
>
> > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
> > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
> > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
> > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
> > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
> > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
>
> At TxICR the floor is {label} x {p1} x {p2}: one `pcc_timer_tick` callback increments both counts and
> `reassert_interrupts` reads both, so the pair is a joint input of the model.  Eight cells, all rowed.
>
> #### *** THE FLOOR INCLUDES THE SINGLE-AXIS GENERATING SET, AND "DERIVED" STATE IS NOT DISPOSABLE.
> #### Adjudicated 2026-09-04 by the fix review (Fable 5.1 adjudicating; GPT-6 Astra at max dissenting on the
> #### bound and supplying the two findings that made the amendment measurable). ***
>
> > **At each floor cell, every idata bit the guarded body TESTS is written both clear and set.**  The bare
> > state floor above does not catch `M_ICLR` -- an idata-bit x state joint -- and would grade the pass-11
> > escape as debt while the CHANGELOG grades it L2; the generating set is what makes the two consistent.
> > Multi-axis idata joints stay clause-(e) debt.  **The codex seat adopts the Opus strength-t covering
> > array instead** (its `t` = the body's longest conjunction) and is RECORDED, not adopted -- for COST (seven
> > binary axes at TxICR make a strength-4 array tens of pty cells per arm: the 2^k growth by another door) and

### 4c. The label clauses: the join (2026-09-09) and the skipped dispatch (2026-09-25 / 09-30)

> before its table ran (Opus, pass 10).  **AND THE JOIN ITSELF, adjudicated 2026-09-09 on `sgimtedepth4dead` 7g-1 after a MEASURED total escape: a dispatch LABEL is a floor axis of an edited guard when the selector's value FLOWS INTO an lvalue the guarded body reads or writes within the enclosing function (there, `dst_mode = (dst_tlb << 10) + ...` two lines above a repair of `dst_mode |= RGBA`), or when the body re-tests it after the join (TxICR); a label that reaches the edit and touches nothing the body reads is clause (e) (the `mode & COPY` shape).  A detector rowing one label of three was swept 14/14 by `&& dst_tlb == MTE_TLB_A` while a guest-only control showed the closed defect live at the other two (`regress/artifacts/sgimtedepth4dead/killtable3_20260909/`).  The floor it adds is {labels} x the guard operand's body-tested partition -- six cells there, two rows owed -- never the labels' cross-product with everything.**  **AND A GUARD THAT SUPPRESSES A DISPATCH ADDS A THIRD DISJUNCT TO THE 2026-09-09 LABEL CLAUSE, adjudicated 2026-09-25 on `#529` by the flagship's first-hand Q3 re-ruling, with GPT-6 Astra's amendments of 2026-09-26 (`crimewidthkill/rerule_20260925/`); this text is the codex seat's 2026-09-26 rewrite of the clause (`codexfarm_20260926/codex_carrierq3.txt`, "faithful with changes"), adopted with three corrections by the flagship's final ruling of 2026-09-30 (`crimewidthkill/final529r18_20260926/fable5_final.md`, item E): a dispatch LABEL is ALSO a floor axis when the edited guard's repair bypasses that dispatch in the enclosing function.  This is an alternative to selector data flow into the guarded body or re-testing after the join; absence of those two connections does not put a qualifying suppression label in clause (e).  At CRIME the repair is `goto crime_declined`, bypassing the register switch.  The jump omits the dispatch; that omission does not make the whole repair path empty of reads, writes or tests (it reads and writes the latch).  The added axis consists of the skipped dispatch's GUEST-OBSERVABLE labels.  Cross it with the applicable code-tested predicate and state partitions under the existing bounds: the guard's dominating predicates and the jointly reachable device-state lvalues read by the fix's own repair path, as defined by pass 11 above.  This does not make every test or state in the skipped arms a floor axis; the existing partition, reachability and generating-set bounds still apply.  At `#529` the repair path tests the warning latch, so its CLEAR and SET states belong explicitly in the enumeration.  TIME and REV with the latch SET were the demonstrated holes at repair 14 -- `M3_timelatch` and `M5_revlatch` escaped at 204/204 while `M4_timeplain` was detected at 200/204 and `M6_istlatch` at 201/204 (`repair14_20260916/POSTTABLE.out`) -- and were CLOSED by repair 15 (table 14: 214/218 both; table 16: 222/226 both, `table16_20260926/POSTTABLE16.out`).  Those holes were never the whole enumeration, and detection of the plain TIME variant does not discharge the latch-conditioned variants.  The INTMASK and CONTROL-write label-swaps were measured DETECTED: table 13a `M7_intmasklatch` / `M8_ctllatch` 201/204 each, table 16 223/226 each.  An OFFSET within one label is not an axis unless the body distinguishes it: `#529`'s entry 34 (`sd +0x40`, latch CLEAR) is unrowed while its label cell is held at +0x278 -- the unrowed-slot class, clause (e).  Include only labels whose skipped arms have guest-observable effects.  CRIME's DOG arm is a bare `break;` and its `default:` body is host-debug only, so neither contributes a floor label for THIS skipped-dispatch face.  This exclusion does not establish guest equivalence for ACCEPTED accesses at those labels: CRIME's width arm supplies `+0x0c`'s observable value before `default:` prints.  DISCHARGE requires measured DETECTION by the shipped instrument of each enumerated label-swap variant, including the relevant state-conditioned variants.  Existing rows may discharge them; predictions or aggregate detection do not substitute for the individual measurements.  Table 11's K2 PER-ROW prediction error is the recorded caution.  The added label enumeration is bounded to the ONE skipped dispatch in the enclosing function; it does not recurse into further dispatches or dispatches in callees.  MINTED FROM ONE DEVICE: on first reuse, check that the skipped-label enumeration and its bounded predicate/state product fit the new device.**  And the measuring seat's own bound -- the cross-product

