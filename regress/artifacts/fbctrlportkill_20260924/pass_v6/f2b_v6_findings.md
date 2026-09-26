# #549 v6 -- THE ADJUDICATION PASS'S ANSWERS (the panel shared N1..N24), consolidated for the flagship ruling

Pass: `f2_v6_brief.md` (39 KB; the probe header verbatim, session B, table 6's full-score edits, N1..N24 with my
dispositions).  Panel `_scratchpad/panel_20260925_201529/` (durable copy owed beside this file); the dedicated grok
job (`grok_dedicated_f2_v6.txt`); the Opus measuring seat (asked to MEASURE D2).  **Codex (GPT-6 Astra) walled**
(usage limit to 07:01).  **The kimi CLI failed on the subscription-access 403**; `kimi-k3:cloud` covers the seat.

## THE TALLY ON THE TWO DISPUTES (count the arguments, not the seats -- the arguments follow)

| seat | D1 (N1, latch-clear x bit) | D2 (N21, a refusal that writes the anchor) |
|---|---|---|
| agy (file-reading) | (0) -- OVERTURN my FLOOR disposition | DISCLOSED under (3) (a value-class exception) |
| glm (packet-fed) | FLOOR (conditional on the joint-cell rule's verbatim text) | real gap; one re-anchor MOVES it |
| deepseek (packet-fed) | FLOOR | real gap; a second anchor for ALL B values |
| minimax (packet-fed) | FLOOR | FLOOR; re-anchoring sd alone moves it |
| kimi-k3 (packet-fed) | FLOOR -- from clause (e)'s own partition asymmetry | FLOOR; only SAME-VALUE-TWO-ANCHORS closes it |
| grok (panel, file-reading) -- **SELF-REVIEW: it raised N21 last pass** | (0) -- OVERTURN floor | DISCLOSED -- a clause-(e) sentence; OVERTURNS ITS OWN floor claim |
| grok (dedicated, file-reading) -- **SELF-REVIEW: it raised N1** | (0) -- OVERTURNS ITS OWN floor claim | DISCLOSED in (3); no row |
| **Opus 5.5 (MEASURING; clean)** | FLOOR -- MEASURED 117/117, and the tripwire argument measured FALSE for wide values | REFINE: real, measured 117/117, clause (e) -- L4 wording; closed for single bits free if D1's rows anchor at 7 |

**The Opus measuring seat -- `opus5_f2_v6.md` (claude-opus-5-5, 143 runs, clean), evidence in
`opus549_measured/f2v6/` (TABLE_f2v6.out, MANIFEST.out with 22 predictions written before building -- all held, BUILD.out,
WITNESS.out, SIM_ANCHORS.out, TABLE_U.out; 46 probe logs ending FBCTRLP_DONE, the U logs ending U_DONE).**
* **D2 measured:** `idata == 32 -> 5`, `== 2^32 -> 5`, `== 2^40 -> 5`, `lo32 == 0 -> 5` all 117/117 on the unmodified
  v6; so are `== 0xffffffff -> 5` and `== 0x100000005 -> 3`; the `-> 7` forms red exactly where predicted.  A static walk
  of the probe's programs: **60 refused values observed at exactly one previous selector** (58 single bits, 5-7 and
  9-63, at 5; `0xffffffff` at 5; `0x100000005` at 3).  **The sd-at-7 copy MOVES the hole** (`2^32 -> 7`, `2^40 -> 7` go
  117/117; the two named residues untouched) -- the `#499` shape.
* **D1 measured:** grok's own mask form, at bit 4 and at bit 40, **117/117** on v6 and on the sd-at-7 copy.  **Witnesses
  on fresh devices -- and this is the fact the (0) side's tripwire argument did not have:** the bit-4 form ends the
  process in the DATA-arm check after a first `sw 16`; **the bit-40 form ACCEPTS a first `sd 2^40` SILENTLY AS SELECTOR
  0** -- no announce, PORT reads 0 -- and the guest's next DATA write runs as command 42 and dies in `fbctrl_command`'s
  default, not the kept tripwire.  **That is #549's own pre-fix truncation defect coming back** (for bits 33-63, 31 of
  the 58).  The seat also measures the same silent acceptance for N4's `MB_pc4` (a first `sd 0x700000001` -> selector
  1) and N2's `!= 2` (a first `sd 0x100000006` -> selector 6).
* **Its D1 warrant:** the body reads `warned_port`, so {clear, set} is a floor axis; v6's own session B defines "set"
  for this compare as "set alone"; the edit is DEPENDS-ON clause (2)'s operand swap; and **the class is the verifying
  pass's breach found on two consecutive passes -- so the CLASS-CLOSURE rule applies**: write the floor into the
  contract as {latch} x {each tested bit alone}.
* **One repair for both, measured as a prototype (`u_sessions.py`, not a probe edit):** one fresh device per
  single-bit value, `PORT=7`, the store (`sw` below bit 32, `sd` above), a PORT read -- keep, announce once, name:
  **61/61 green on the fix in 9.7 s** (gate 16 ~17 s -> ~27 s); kills N1_mask4, N1_mask40, MKB_40, and the `-> 5` D2
  forms (`2^32 -> 5` only if bit 32 is included -- grok's 58 leave it out).  **B at 5 plus U at 7 gives every
  single-bit value two anchors.**  The anchor must be neither 5 (that is D2) nor 0 (a leaked 2^k >= 2^32 stores int 0).
  Residue under all three: `0xffffffff -> 5` and `0x100000005 -> 3`.  Adopting U reds `DSC_ann_hibits` too, which
  re-predicts that edit and two CF2 edits.
* **Its wrong-acceptance list (six):** N4's consequence clause (not always the exit -- silent acceptance measured), N23's
  parenthetical (contradicts N9, which it measures: period 107 is 116/117, period 108 is 117/117), N16 ("up to 30":
  bit 31 is named), N3 ("> 108" off by one; "every mask red" only while the latch is set), N2 (the open low-3 classes
  are 2, 4 and 6; "the exit returns" is not always so), N13 (minimax's "fatal() exits" premise is REFUTED -- record it).
* **What all of us missed:** the tripwire argument is false for wide values (above); D1 and D2 share one repair and the
  ANCHOR decides whether it closes D2 or reopens it; the two 58s differ; the pre-table addendum carried its
  GUARD-vs-BODY section over "unchanged" in the very table that introduced B's generating set -- re-run against B it
  would have asked at which latch state each bit is held, which is N1.  **An apparatus trap it hit:** `wsl -d Gentoo --
  sed -i 's/\r$//'` run from git-bash deletes a trailing letter `r`, not a CR.

## THE SHAPE OF THE DISAGREEMENT, FOR THE RULING

On D1 the seats agree on EVERY FACT -- the 58-bit gap, its 117/117 score, the repair's `sw` defect -- and split on
ONE RULE QUESTION: does the joint-cell floor's generating set reach the bits of a value tested only by a relational
compare?  The two groks and agy say no (the carrier's own bound: the written value's bits are single-operand
marginals; the relational operator's generating set is below/at/past, held at both latch states).  The Opus seat says
yes (session B already treats "each bit set alone" as the compare's generating set, and the class recurred on two
consecutive passes), and adds a CONSEQUENCE the (0) side's tripwire warrant did not account for: for bits 33-63 the
escape is silent acceptance of selector 0 -- the defect #549 exists to remove -- not the kept exit.  **The flagship
carrier ruled on `#548` that grading is by the generating set, not the consequence; this pass asks whether that ruling
survives when the consequence is the round's own defect.**

**grok (dedicated) -- `grok_dedicated_f2_v6.txt`, 13,692 bytes, VERDICT: SHIP -- the seat that RAISED N1, asked to be
harder on it, reverses it, from the carrier's full text.**  The 2026-09-04 rule has three bounds the floor reading
dropped: the floor is the guard's dominating predicates x the device-STATE lvalues the repair path reads, where
jointly reachable; **"the bits of the value being written are single-operand MARGINALS, not a floor axis"**; and a joint
is owed only where the guarded body's own code distinguishes it.  The generating-set sentence was added for a body
that MASKS a bit (`idata & ICLR` at TxICR); this arm tests `writeflag == MEM_READ`, `idata >= 8` and `!warned_port`, and
has no `idata & (1 << k)`.  The latch-clear floor CELL is held (every session's first refusal but Z's and R's), at all
three regions of the compare; (latch clear, bit k) is the two-axis joint (0) discloses.  Drop the tripwire as the
warrant: NOT CLAIMED (2) keeps it for DATA-arm edits.  On D2 it lists the eleven rows that read PORT after a refusal
at a previous selector other than 5 -- none refuses 32, 64, 128, 0x200 or a low-32-zero value -- and corrects the
claim: bits 3, 4 and 8 are ALREADY dual-anchored (V at 7, X7 at 7); the constant blind spot also covers `0xffffffff`
(P, anchor 5 only) and `0x100000005` (X3, anchor 3 only).  The smallest closing set is ONE ADDED chain at 7 (60 values,
one read) -- and it is not owed: `idata == k` is a case this body never tests, so no finite row set closes "except
value k", which (3) already says.  Owed: one widening sentence in (3).  Its wrong-acceptance list: **N15**
(VERIFIED here: `BR_ge9` in table 6 and `M_gt` in table 5 are ONE binary, md5 9b21ac29 -- "six changers" counts `M_gt`
twice; five new plus one duplicate), **N20** (as grok panel), **N22** option 2.

## *** A BRIEF DEFECT OF MINE, DISCLOSED: the packet quoted the joint-cell rule's generating-set sentence WITHOUT its
## bounds, and every packet-fed FLOOR vote rests on that sentence. ***

My N1 disposition quoted "at each floor cell, every idata bit the guarded body TESTS is written both clear and set" and
not the sentences around it in the same adjudication -- "the bits of the single value being written are single-operand
MARGINALS, not floor" and "the FLOOR ... is the cross-product of the guard's dominating predicates with the device-STATE
lvalues ... jointly reachable".  glm made its FLOOR ruling explicitly CONDITIONAL on the verbatim text; deepseek and
minimax reasoned from the quoted sentence; kimi-k3 argued from clause (e)'s partition asymmetry instead (a separate
argument, which grok (dedicated) answers: the latch partition's floor CELL is held; the (cell, bit) pair is not a
cell).  **This is the carrier's "a wrong fact in a brief comes back confirmed", committed by the author of the
disposition the seats were asked to test.**  The file-reading seats (agy, grok x2) read the full text.  The flagship
ruling should weigh the packet-fed FLOOR votes accordingly -- count the arguments, not the seats.

**grok (panel) -- `grok.txt`, 10,974 bytes, VERDICT: SHIP -- the argument the FLOOR side did not meet.**  The fixed
arm's body tests ONE relational operator, `idata >= 8`; there is no `idata & bit` in it.  The generating set of that
operator is below / at / past the bound -- the flagship's own ruling on `#548`'s P_win -- and it is held with the latch
clear AND set (8 is the first refusal of P, W and B; values past 8 the first refusals of F, V, X, Y and Z; accepts
before any refusal in A and W; later accepts in V and Z; later 8s in W and V).  **Session B is the one-axis MARGINAL
of the 61 bits that the CONTRACT claimed and v5 left empty; crossing it with the latch is the two-axis joint (0)
discloses.**  Every FLOOR seat above reasoned from "every idata bit the guarded body TESTS" -- and on this reading the
body tests no bit.  On D2: rows are owed per ENUMERATED mutant, and the enumerated refusal mutant ("store the
truncated selector") cannot read back as 5 (`MKB_05` 113/117 on B's four rows); a value-keyed constant write is the
`idata == k` shape, a clause-(e) sentence.  **And the two repairs COLLIDE:** 58 latch-clear rows anchored at 5 widen
D2's blind spot; replacing B's sd anchor with 7 MOVES the constant (bits 32 and 34-62 at 7; P's `0xffffffff` stays at
5 only) -- only an ADDED second anchor closes the constant-write class.  Its wrong-acceptance list: **N9** (keep
"more than 108": N=107 announces on the 108th, already red; the escape starts at N=108), **N16** (name k=31: INT_MIN,
measured `0xffffffff80000000`), **N20** (R's unreselected DATA access is the WRITE of 0x2a; its DATA read re-selects
port 5 -- the post-refusal accesses without a fresh selector are K's read, K's write and R's write), **N22** (keep
thirteen in the gate; (4) grows to thirteen).  N17 settled as agy did.

## THE ARGUMENTS

**D1.**  agy: the edit conditions the guard on two operands at once, so it is the joint (0) discloses, and the kept
DATA-arm range check is the tripwire (`opus549_measured/v6/unset_witness.out`: the exit reached on a fresh device);
admitting it "over-concedes to a single seat" and costs 58 processes.  The FLOOR side, three arguments: (i) the
joint-cell rule's generating set, which puts the body-read state lvalue `warned_port` in the floor (glm, deepseek,
minimax -- all from the rule as QUOTED in the packet, and glm makes its ruling conditional on the verbatim text);
(ii) kimi-k3, from the probe's own clause (e): the body tests three things -- direction, value, latch -- and exempts
previous selector / COMMAND / cells BECAUSE the fix makes no partition of them; the fix DOES partition on the latch,
so an edit keyed on one leg of that partition crossed with the compare's operand is floor by the header's own logic;
(iii) the "unbounded growth" warrant of (0) does not reach a 58-cell set (glm: the generating set is the 64 tested
bits, not the value space).  **The tripwire argument is contested by the FLOOR side's own framing:** the tripwire is
what the fix KEEPS as a backstop, and an accepted out-of-range selector reaching it is the defect the fix removed.

**D2.**  agy: a value-keyed constant write is a value-class exception, disclosed by (3), and no finite set of anchors
closes a relative oracle.  The FLOOR side: the write is conditioned on the value alone (one axis), (3) is about
accept/announce-side exceptions (glm: "(3) is accept/announce-side exceptions, (8) is cell-value conditions"), and the
header CLAIMS "a refusal keeps the previous selector" -- an effect the rows cannot tell from "re-written to the
anchor".  **On the repair every FLOOR seat agrees that ONE re-anchor only MOVES the class**, and two sharpen it:
kimi-k3's audit finds **107 values refused at exactly one anchor** (105 of B's single bits, all but 2^3, 2^4, 2^8,
plus P's 0x200000000 and 0xffffffff) and states the stop condition "no refused value held at exactly one anchor"; it
warns that per-width anchors (sb@5, sh@6, ...) do NOT close it either.  glm finds one more: **0x100000005 is refused
only at X3's anchor 3.**

## NEW FINDINGS FROM THIS PASS

* **P1 -- THE N1 REPAIR AS PROPOSED FAILS ON THE FIX ITSELF** (glm, deepseek, kimi-k3, independently).  "One `sw` of
  2^k": a 32-bit store of 2^k for k >= 32 delivers idata 0, which the fix ACCEPTS (selector 0), so the row "PORT must
  still read 5" is red on the correct build and v7 would fail its own gate.  Use `sd` for all 58 (kimi-k3, glm) or the
  minimum carrying width per bit (deepseek).  **ACCEPTED** -- binding on any v7.
* **P2 -- the two 58s are different sets** (glm): N1's open bits (4-7, 9-31, 33-63) and N21's single-anchor values
  coincide in count, not in membership.  **ACCEPTED** -- records.
* **P3 -- N17 SETTLED by reading** (agy): session R's DATA read lands in `s2`, and R's reads list is `["s1"]`, so no row
  reads it; NOT CLAIMED (8)'s exclusivity holds as written.
* **P4 -- N20 was accepted while N17 was open, and they rest on the same fact** (kimi-k3, glm): R's header summary puts
  "a DATA READ of port 5" after "a NOP command (PORT=0, DATA=0)".  If that NOP re-selects port 0, the summary's "of port
  5" is wrong, or N20's invariant is.  **FOR THE ADJUDICATION** -- a file-reading seat settles it from `PROG_R`.
* **P5 -- LIMITS OF A ROW has TWO errors in one sentence** (agy): besides "not which" (N16), "prints the last one's
  stored int" is false when an earlier store leaks and later ones are refused -- it prints the last value that GOT
  THROUGH.  deepseek: N16's "up to 30" is off by one (INT_MIN names bit 31).  **ACCEPTED** -- wording.
* **P6 -- residues mod 8** (agy): every refused value's low three bits are 0, 1, 3, 5 or 7; none is 2, 4 or 6, which is
  why `(idata & 7) != 6` (N2) scores the full count.  **ACCEPTED** -- the (3) sentence can say so.
* **P7 -- `fatal()` on this path prints and returns** (glm): the design rests on it (twelve refusals in P, 108 in B)
  and no settled premise says so.  **ACCEPTED** -- one SETTLED PREMISES sentence.
* **P8 -- the v6 probe is a NEW file** (agy): `git status` shows it untracked; it is staged by name.  **ACCEPTED** --
  commit mechanics (the #549 commit adds it).

## WHAT IS OWED

The flagship ruling on D1 and D2 (FLOOR -> a v7; or disclosed -> wording only), on the arguments above and on the
measurement the Opus seat was asked for (D2's one-line variant against the unmodified v6).  Then Astra, after 07:01.
