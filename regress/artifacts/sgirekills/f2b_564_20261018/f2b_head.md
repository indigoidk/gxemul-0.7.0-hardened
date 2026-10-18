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

