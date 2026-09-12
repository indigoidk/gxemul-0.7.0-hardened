# ADJUDICATION PASS (§F2) — `xscaleinten` and `ppcrlwimiwidth`/`ppcrldimimask`: the whole panel's findings, shared

VERDICT LINE FIRST, then the liveness token `ADJUD_XP_20260912`.

You answered one of two pass-2 briefs blind to the other seats.  Below is **every seat's finding from both
panels**, numbered, with **my disposition** and **what I changed**, and then the **measured result** of the
changes.  The questions are at the end.  **Please do not ratify** — I have accepted most findings, and that is
a suspicious number; agreement with me is not evidence.

Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` (ignore any other `src/` under the project root).  Both fixes are
uncommitted; the diffs and enclosing functions are in the two pass-2 briefs, re-inlined here only where a
finding needs them.

## SETTLED PREMISES (re-inlined for packet-fed seats)

* xscale fix: in `arm_coproc_i80321_6`, the `crm 0 / crn 0 / l_bit` arm did `r[rd] = i80321_inten;
  fatal("TODO: XScale read from inten?"); exit(1);` — the fix deletes the last two lines (ACCEPT).  The body
  reads `rd` (as an index) and `i80321_inten`; it TESTS neither.  The sibling `crn 4` read is quiet.
* PPC fixes: rlwimi narrows `tmp` to 32 bits and, BEFORE the insertion loop, `if (mb > me) ra = (ra &
  0xffffffff) | ((uint64_t)tmp << 32)`; rldimi rotates a COPY `n = sh` (the old loop consumed `sh`), and
  its mask loop wraps: `m = (m + 1) & 63; } while (m != ((64 - sh) & 63))`.  rldimi snapshots `s = gpr[rs]`
  before rotating it, then `gpr[ra] &= ~tmp; gpr[ra] |= (tmp & s);`.
* Clause (d) DEPENDS-ON enumerates the predicates dominating the edited lines (to the function boundary) and
  operand swaps drawn from fields the guarded body reads; for a PURE DELETION the (d) mutant re-introduces the
  removed behaviour under a DIFFERENT predicate.  A value the body never tests as a case (`idata == k`) is
  clause-(e) DISCLOSURE, not a floor cell.  An UNSHIPPED detector's rows are L1 construction — adding a row
  needs no floor warrant.

## FINDINGS — xscaleinten (panel_20260912_095235_xscalepass2 + the Opus measuring seat)

* **F1** `if (rd == 0) { fatal; exit(1); }` after the load survives all 29 rows.  **Opus MEASURED 29/29** and
  showed it is a live kill (MRC into r0 dies, into r9 survives); codex, grok, glm, deepseek, kimi predicted it.
  Inten reads landed only in r3-r7, r9, r10, r15.  **ACCEPTED.**
* **F2** an exit keyed on an inten bit no row sets survives: the rows drive inten = 0, S1 = 0xA500005A,
  S2 = 0x5AA5F00D, bit 28 (union 0xFFA5F05F; never set: 0x005A0FA0).  minimax, glm, deepseek, kimi, codex, grok;
  **Opus MEASURED bit 22 at 29/29**, live kill.  **ACCEPTED.**
* **CHANGE for F1+F2:** one row, `RD0_ALLONES` — fresh session, r0 poisoned 0xdeadbe00, inten <- 0xffffffff,
  `mrc p6,0,r0,c0,c0,0`, want r0 == 0xffffffff.  One read fires both.  Detector 29 -> 30 rows, gate pin 30.
* **F3** the CONTRACT said "the read loading another register (M5: isteer)"; the measured M5 redirects BOTH
  directions of the crn-0 arm to isteer (`mut_xscale_t2.py`).  codex, grok, kimi, glm.  **ACCEPTED**, header
  corrected; it now also says a read-only redirect was never built (it would red D_S1 by construction).
* **F4** glm: "M5's 27/29 has no consistent mechanism"; deepseek: "INTEN_WRITE_PRESERVES_ISTEER is vacuous under
  M5".  **REJECTED** — both assumed a read-only M5.  Under the two-way M5 the inten write lands in isteer, so the
  row reading isteer gets S1 (`probe_M5.raw`: got 0xa500005a want 0), and inten is never written, so the IRQ
  never enables (ANCHOR_EXC got 0x8024 spin, want 0x18).
* **F5** `if (isteer != 0)` exit survives.  All seats; Opus: EQUIVALENT on this instrument — isteer can only become
  non-zero through a write that itself exits.  **ACCEPTED as disclosure** (NOT COVERED).
* **F6** ACCEPT is the right disposition — codex, grok, kimi, glm, deepseek, minimax.  Qualification (codex, grok):
  the DC21285 precedent my brief cited is a DISPOSITION precedent, not quiet source — `dev_footbridge.c` still has
  its `fatal`+`exit` there.  **ACCEPTED**; my brief overstated it.
* **F7** kimi: D_RESET/D_ZERO cannot vary under a wrong-source mutant whose substitute is also 0; ANCHOR_CONTRAST
  kills M1 by host death, not by its named "spins" channel.  **ACCEPTED as record**, no change (the kills are real;
  the names overstate the discriminator).
* **F8** kimi: NOT COVERED omitted the read-count ceiling (no session makes more than five inten reads) and that
  the ANCHOR rows raise only irq 28.  **ACCEPTED**, two clauses added.

## FINDINGS — ppcrlwimiwidth / ppcrldimimask (panel_20260912_095238_ppcpass2 + Opus)

* **F9** codex: `while (n-- != 0)` -> `while (n-- != 0 && mb != ((64 - sh) & 63))` skips the rotate exactly when
  the mask is full width; every full-width row and census cell used the ALL-ONES source, which no rotate changes.
  **ACCEPTED.** Row `full rot`: SH=24, MB=40 from 0xDEADBEEFCAFEF00D into 0x5A5A.., want 0xefcafef00ddeadbe.
* **F10** glm: rldimi had no rA == rS row (rlwimi has three).  **ACCEPTED as a sibling-parity gap** — but glm's
  literal mutant, `gpr[ra] |= (tmp & cpu->cd.ppc.gpr[rs])`, reads the UNROTATED source and is wrong for every
  SH != 0 whatever the aliasing; I built glm's own "equivalently" form (re-read rS after the clear AND rotate it),
  which differs from the fix only when rA == rS.  Row `alias rs=ra`: r8 = RS_VAL, SH=8, MB=16.
* **F11** Opus: the `census run`/`disasm total` literal pins DO carry a measured kill — its end-test-without-`&63`
  mutant read `census run 0 / 495`, `disasm total 8/16`.  My table-2 note said they had none.  **ACCEPTED**; corrected.
* **F12** grok, kimi, Opus: rotate amount was evidenced only at SH 8 and 40 (all-ones census is rotate-blind).
  **ACCEPTED**: `full rot` adds SH 24; CONTRACT now says an edit keyed on another single SH is not pinned.
* **F13** codex: the rlwimi `wrap fullword` note said 31 low bits; it replaces all 32.  **ACCEPTED**, fixed.
* **F14** codex: both `cr0 record form` rows check CR presence only; deleting `update_cr0` survives.  **ACCEPTED as
  disclosure** — already stated for rldimi; NOT YET stated in the rlwimi header (owed).
* **F15** kimi, minimax, grok: deleting rlwimi's `sh ?` guard is equivalent on this host (`tmp >> 32` at sh=0 is UB
  but evaluates as `>> 0` on x86-64); the line predates the fix.  **ACCEPTED as not-a-gap**, no change.
* **F16** deepseek: a mutant misrotating only at SH 1 or 2 survives.  **ACCEPTED as clause (e)** (an `idata == k`
  shape on SH), now disclosed.

## DISAGREEMENTS

* **D1 — are F1/F2 floor cells or clause-(e) disclosure?**  *Floor:* glm ("the body reads rd and inten"), deepseek,
  minimax, kimi ("one added row closes the two floor-cell classes"), codex for `rd == 0` ("a bounded operand swap:
  an existing equality-to-zero predicate with the body-read index substituted").  *Disclosure:* grok ("the body
  never tests rd; `rd == 0` is the `idata == k` shape"), codex for the inten bit.  **My provisional ruling:** the
  row was added either way (L1, unshipped), so D1 decides only the GRADE in the CHANGELOG and what the rule says
  for the next pure deletion whose body tests nothing.  I lean **disclosure for arbitrary `rd == k` / bit
  predicates, floor for `rd == 0` and "any inten bit" only because one cheap row pins each partition** — and I
  distrust that lean, because it grades by what was cheap.  **Parties: adjudicate your own dispute.**
* **D2 — M5 consistency** (glm, deepseek vs codex, grok, kimi): settled by the mutator text (F4).
* **D3 — literal pins: floor gap (deepseek) or disclosure (grok, kimi, codex)?**  Settled for "carries a kill" by
  Opus's measurement (F11); the floor-vs-disclosure label is still open.

## MEASURED AFTER THE CHANGES — kill table 3, both rounds, predictions written BEFORE each ran

**xscaleinten** (`regress/artifacts/xscaleinten/killtable3_20260912/`): 12 legs, **12 on prediction**.  BASE 30/30
CONTROL=OK; HEAD 12/30; M1 27; M5 28; M_OPCODE2 27; M_RD15 29; M_NREAD 27; M_OP1 29; M_ISTEER_WR 29; M_CRM 29;
**M_RD0 29/30 and M_MAGICBIT 29/30, each failing RD0_ALLONES ALONE.**

**PPC joint** (`regress/artifacts/ppcrlwimiwidth/killtable3_20260912/`, one build per leg, both probes): 17 legs,
**15 on prediction**, cross-check held on every leg.  rldimi BASE 29/29 (`disasm total` 513/513 measured);
**D_SKIP_FULL_ROT 28/29 failing `full rot` ALONE; D_ALIAS_REREAD 28/29 failing `alias rs=ra` ALONE.**  Two misses,
recorded in POSTTABLE.out: D_NO_MERGE predicted 26, measured 25 (my arithmetic — the row-level prediction was
right); D_NOCIRC predicted 21, measured 22 — `full rot` PASSED under that undefined-shift mutant (measured; the
likely mechanism is x86 shift-count masking making the unmasked loop circular, NOT measured).

## WHERE I MIGHT BE FOOLING MYSELF

* I accepted 14 of 16 findings.  Two I rejected (F4) rest on a mutator text I read, not on a new measurement.
* The one row for F1+F2 closes `rd == 0` and "any inten bit"; it does not close `rd == 8` or `inten == S1 ^ 1`.  I
  have written those as disclosure.  If D1 comes out "floor", is the right closure a row per undriven rd, or is
  the enumeration unbounded and therefore disclosure by construction?
* F10's row catches the aliasing form I BUILT.  Is there an aliasing mutant it does not catch?

## QUESTIONS

1. Adjudicate **F1..F16 and D1..D3** — UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted fourteen; that is a suspicious count.
3. **WHAT DID ALL OF US MISS?**  You now have both panels' output and the measured tables.
4. Is either round **ready to commit** once its gate is green, or is something owed first?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
