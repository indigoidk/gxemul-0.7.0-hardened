# `#567` F2 -- the adjudication pass's answers, and what they changed (2026-10-19)

**Roster.**  GPT-6 Astra (`codex_fbcmdf2.txt`, 05:58; token `ASTRA_FBCMD_F2_20261019`), Grok 4.7 xhigh (`grok_f2.txt`,
06:11; `GROK_FBCMD_F2_20261019`), GLM 5.3 (`glm_f2.txt`, 06:04, packet-fed; `GLM_FBCMD_F2_20261019`).  Each answer
carries its token and a verdict line and was read in full.  **All three: SHIP WITH CHANGES.**  Fable 5.1: walled, HTTP 429
(`fable5_f2_WALL.txt`) -- a SEAT FAILURE, held with a question under the owner's 2026-10-17 directive, never agreement.
Opus 5.5, agy, kimi, deepseek and minimax DELIBERATELY NOT FIRED (the owner's 2026-10-17 roster).  Rulings: Astra, Grok and
GLM, by the owner's directive; where the three converge the main loop records the ruling, and where they split it says so.

## Where the three converge

**G1 -- F2 WAS NOT REPAIRED BY v2: WIDTH x BOUND EDGE.**  Astra (FLAG 1; Q3 `M_sd_no_dispatch`, `M_sd_bound0`), Grok
(FLAG 1; Q3 "`sd` bound up by one" and its `sh` twin).  v2's only accepted `sd` was a NOP -- an empty case body -- and only
`sb` and `sw` held both edges of the bound (accept 2, refuse 3; `sw` by the seeds and `R:3`).  **Kill table 3a (`killtable3a_20261019/`, run before any repair)
MEASURED the class's seven open cells ESCAPING v2, 99/99 each:** E15 sd dispatch skipped (= Astra's `M_sd_no_dispatch`),
E16 sd bound 0 (= `M_sd_bound0`), E17 sh bound 1, E18 sd bound 3 (= Grok's), E19 sh bound 3 (= Grok's twin), E20 the
latch cleared by an accept, E21 the latch cleared by a read.  **Disposition: L1 (pre-ship construction -- nothing is
committed), and clause (d) in shape (the fix's own bound relaxed at one width).**  Two consecutive passes (pass 2's E13,
F2's E15-E19) breached ONE class, so by the class-closure amendment the repair owes the CLASS: v3 held accept 2 and refuse 3
at every width with an observable dispatch (`A:edges`, `R:edges`); then **reading the arm for the rest of the class found
seven more open cells at the bound's edges alone -- width x LATCH, where a bound relaxed in one (width, latch) cell
restores the host kill -- so v4 closes the whole class in one diff** (`killtable4_20261019/PRETABLE_ADDENDUM_t4.out` holds
the enumeration, written before v4 ran).

**G2 -- LATCH PERSISTENCE.**  Astra (FLAG 2; Q4), Grok (FLAG 3; Q4): no session refused after an accept or a read; E20/E21
escaped v2 (table 3a).  **Disposition: L1; the contract's "announced once per device" had no row at that cell (CLAIM ->
ROW).**  v3's T2 refuses 3, accepts a NOP, reads COMMAND, refuses 5, refuses `sd 0x100000005`: one announce.

**G3 -- NOT CLAIMED (6)'s MECHANISM SENTENCE WAS FALSE.**  Astra, Grok; GLM's F19 concurs.  The callback RECEIVES all 16
bytes (`memory_rw` hands the device the caller's buffer and `len`; a 16-byte store at DATA fits the window);
`memory_readmax64()` drops the prefix while building `idata`, before the compare.  "The device never sees the rest" put the
loss in the wrong place.  **L4 in the probe's contract -- corrected in v4's.**  And the packet's `machine_test.c:337` is
testmips's OWN install; testppc's comes through `default_test()` at `:154` (Astra, Grok) -- **L4 in my packet; the records
cite `:154`.**  Grok adds the consequence: a 128-bit value whose low half is 1 still runs SET_RESOLUTION -- "this round's
width bug one step further out", which is how the filing names it.

**G4 -- THE GATE BLOCK HAS NEVER RUN IN SITU.**  Astra (FLAG 3), GLM (FLAG 1; Q2), Grok (F18 REFINE).  The replay sourced
the block's lines with a stub `check()` and an injected `fcrc`: the launch line, the real `check()`, the exit propagation
and gate 16's two device probes side by side never executed together.  **Disposition: OWED BEFORE COMMIT** -- one real
`gate_mips_folds.sh` run on the fix's binary (expect green) and one on HEAD's (expect nonzero, naming the block's rows),
`LOGDIR` in scratch, preserved under `wiring_20261019/`.  My F18 "no change" answered only the trailer half.

**G5 -- RECORDS OWED.**  Astra (FLAG 3), Grok (F15, D5), GLM (F15): `fbctrlvec128` as its own ledger row;
`gatedevicesplit`'s row AND `OUTSTANDING_BUGS.md` carry the gate-16 stop -- in GLM's form, *a third device probe lands only
with the split or with a pin on the launch count* (the stop is procedural, not mechanical, and the records say so).
**Owed in commit B.**

## Single-seat findings

* **S1 (GLM FLAG 2) -- census blast radius.**  `tools/precommit_check.sh`'s manifest comment says *"pinned UNQUOTED in
  gate_mips_folds.sh at 95 rows"* -- stale since v2 (99) and again at v3/v4.  **L4 in my working tree: corrected to the
  final count; the records are grepped for stale 95/99/106 row counts before commit.**
* **S2 (GLM FLAG 3) -- E8's name.**  E8 SETS THE LATCH ON AN ACCEPT (`d->warned_cmd = 1;` after the store), not a pre-set:
  a pre-set would silence every first refusal.  The probe's mutant list already says "set by an accept"; my F2 packet said
  "pre-set".  **L4 in the packet; the CHANGELOG says "set by an accept".**
* **S3 (GLM FLAG 4, Q4.4) -- two scope lines.**  "A read stores nothing" was pinned at COMMAND and X1 only (Y1 is read once
  in every session); the `noset` channel is live only in STEPPED sessions (F free-runs).  **Accepted: both go into v4's
  contract** (v4's M3 also reads COMMAND at four widths).
* **S4 (Astra, Grok F20) -- "two stores into `port[]`" was wrong.**  GET_RESOLUTION makes four X1/Y1 assignments, plus the
  dynamic DATA store; `DEVINIT` `memset`s the struct.  **L4 in my packet; the conclusion -- no other writer of COMMAND --
  stands.**
* **S5 (Grok F2 REFINE; Astra Q2) -- "stored and runs at every width" overclaimed** the `sd` NOP.  **v3/v4: GET runs (X1
  zeroed) at every width; the contract says which value is seen to run at which width, and a NOP is stored, not claimed to
  run.**
* **S6 (Astra D2 REFINE) -- describe E14's closure without implying every latch x wide behaviour is covered.**  **Accepted:
  NOT CLAIMED (0) stays and says so.**
* **S7 (GLM F17) -- the unlisted-value class closes only by reshaping the product's compare into an enumeration of accepted
  values.**  **Recorded in NOT CLAIMED (2) as one clause; no reshape here (no measured delta licenses it).**
* **S8 (Astra F14, GLM F14, Grok F14) -- the census split is a plan, not done.**  Correct: commit A is still owed.

## Q2 -- "which of my accepted dispositions is wrong?"

Astra: **F2** (its completeness).  Grok: **F2**, **F1's mechanism sentence**, and **F18's** "no change" (half right).  GLM:
**F18** (the launch line unowned) and **F14** (accepted as a plan, not done).  Every one is taken above (G1, G3, G4, S8).
Upheld by all three: F3, F4, F5, F6, F7, F9, F10, F11, F12, F13, F16, F17 and D3.  GLM withdrew its own F8/D2 wording
("exploitable", "needs a row more than a mutant") -- a seat being harder on its own finding, as asked.

## Q3 -- clean sweeps of the shipped composite (v2)

Astra: `M_sd_no_dispatch`, `M_sd_bound0` (= E15, E16).  Grok: E18 and its `sh` twin E19.  GLM: the three disclosed
families -- value carve-out (2), latch x wide alias (0), 16-byte (6).  **E15-E19 MEASURED escaping v2 (table 3a);** GLM's
three are disclosed by the contract, and the seats agree disclosure is the honest disposition for each.

## What the repair is now, and what it owes

**v3** (106 rows, 24 sessions) = v2 + `A:edges` + `R:edges` + T2's NOP and read between refusals.  Legs: fix 106/106,
HEAD 42/106.  **Kill table 3** (`killtable3_20261019/`) re-ran all 32 mutants and both null media on v3.

**v4** (123 rows, 27 sessions) = v3 + `W:latch` (sd 3 with the latch clear; sb, sh, sw 3 with it set; GET by sb, sh, sd
with it set) + `W:sb` (the latch set by a byte refusal) + `M3` (width at a non-COMMAND port and on the read path).  v3's
rows unchanged.  **Kill table 4** (`killtable4_20261019/`, predictions written first): both legs, all 44 mutants on v4,
the 12 new ones also on v3.

**The repair chain:** v3/v4 are repairs made in response to F2, so they owe their OWN pass -- effort scoped to the v3+v4
diff, the floor question asked of the shipped composite, and, by the class-closure amendment, **the closing pass VERIFIES
THE ENUMERATION** (`PRETABLE_ADDENDUM_t4.out`) rather than hunting cells.  Then Astra confirms before commit.

**Fable's held question:** *"F2 converged three ways on WIDTH x BOUND EDGE and latch persistence (G1, G2); v4 closes the
whole width class in one diff from an explicit enumeration.  Is that enumeration complete for the DATA arm -- does any
partition the arm's code distinguishes, crossed with width, lack a row or a disclosure?"*
