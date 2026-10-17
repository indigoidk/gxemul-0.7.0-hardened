# RULINGS -- packet A (#563 wdc473floor: REPAIR3's pass-2 findings and the drafted REPAIR4), 2026-10-16

Consolidated by the main loop (Opus 5.5, 087a90) from three independent adjudications of `packet_A_563.md`:

| seat | answer | verdict |
|---|---|---|
| GPT-6 Astra (ultra) | `astra/A_563/codex_adjA.txt` | UPHOLD WITH CHANGES (10 changed) |
| Grok 4.7 (xhigh; `git show` blocked, read the working tree, which is clean for dev_wdc.c) | `grok/A_563/grok_adjA.txt` | UPHOLD WITH CHANGES (2 changed) |
| Fable 5.1 seat -- **FALLBACK, a SEAT FAILURE** (agent_models.py: claude-fable-5-1 for 65 turns, REFUSAL 17:03:15Z, thinking_drop -> claude-opus-4-8, which wrote the answer AND `meas_A/f4_run.txt`) | `fable5/FALLBACK_opus48_adj_A_563.md` (called **FB-A** below: an Opus 4.8 reading plus a real measurement, NOT a Fable ruling); Fable resumed 12:3x for `fable5/fable5_adj_A_563_v2.md` | FB-A: UPHOLD WITH CHANGES (2 changed) |

**Roster: 3 of 3 after a resume.**  The first Fable run FAILED by fallback (FB-A, above; this file first credited FB-A and its measurement to Fable -- corrected 12:3x).  Resumed with a neutral follow-up, Fable 5.1 wrote its OWN ruling, `fable5/fable5_adj_A_563_v2.md` (agent_models.py: written 17:30:57Z by claude-fable-5-1): **UPHOLD WITH CHANGES (2) -- F4/D7 FLOOR with row N5; every other ruling stands, D3 by reading (iii).**  It read FB-A as a colleague's notes, so it is not independent of FB-A on F4; it cites `meas_A/f4_run.txt` as the measurement.  Its argument that widths 3/5/6/7 cannot reach the data register lists every WDC base except macppc's (0xf3020000), the one Astra's route uses -- the factual half of D3 stays contested.  The chain does NOT close: REPAIR4 as I disposed it was insufficient (Fable, Astra), and the corrected
REPAIR4 is below.

## Rulings

- **F1, F2, F3 -- FLOOR (3/3).**  `D2_st`, `D2_or_st`, and the (flag 0, `atapi_len` > 0) cell.  Rows N1, N2.
- **F4 / D7 -- OVERTURNED: FLOOR, row N5 (Astra REASONED, MEASURED in FB-A's run by claude-opus-4-8; Grok's "disclose" rested on the premise
  Astra and FB-A refuted).**  A CMDOUT ring CAN sit on a 512-byte boundary before any dispatch: the dispatch fires only
  at `inbuf_len == 12` exactly (`dev_wdc.c:1717`), and one 2-byte store then 4-byte stores step 2, 6, 10, 14, ...,
  past 12, then on to 514.  MEASURED (`fable5/meas_A/f4_run.txt`, the real `dev_wdc_access`, `dispatched=no`, `st=NULL`):
  HEAD `int_assert=0 sink=0 warned_null_xfer=1`; `D2_and_st` and `D2_st` `int_assert=1 sink=1`; `D2_or_st` and
  `D2_phase` as HEAD.  The discriminator, which my packet applied to the latches and failed to apply here (FB-A): the
  swapped operand `atapi_st` IS a repair-path lvalue (:1424, :1461), so (flag x `atapi_st`) is in pass 11's floor --
  the latches are not, which is why the latch class stays (e).
- **F5, F6, F7 -- EQUIVALENT (3/3).**
- **F8 / D5 (`D0_nocmd`) -- (e) (3/3)**, the disabled-STATUS delta (0 vs 0x50) written into the contract.
- **F9 (`D6_head`) -- (e) (3/3)**, the `tail != 0` state named; Astra's input avoids an intermediate head-12 dispatch:
  push six, read two, push four, push four.
- **F10, F11, F18, F19 / D2 (the latch operands) -- (e) (3/3)**, recorded as GUEST-VISIBLE (e) debt with each delta,
  disclosed as a family without implying the found members exhaust it (Astra); the bound is pass 11's repair-path
  lvalues (FB-A, Grok).  FR's sentence "the reject arm reads no field" is removed (:1766 reads it); the grade does not
  move.
- **F15 (VD1) -- FLOOR (Astra, FB-A; my ruling), Grok dissenting ((e) by the derived-input ruling).**  FB-A's answer
  to Grok: the 2026-10-09 ruling grades the derived LOCAL `consumed` by the tests on it; it does not demote the body's
  direct tests on the INPUT `len` (`len >= 2 ? 2 : 1` makes width 1 its own case).  VD1 is the downward bound move
  `len >= 1`, and the only width-1 row's channel (occupancy, constant fill) cannot vary under it.  Row N4: a count read
  (CYL_LO/CYL_HI, not occupancy) after the first 1-byte DATA read of the 1-byte walk, want 32767 (Astra).
- **F12, F13 (`bepop_ge4`, `lepop_ge4`, `cons_eq2`) / D3 -- (e) by Grok and FB-A, FLOOR by Astra.  RULING: (e), and
  ROW THEM ANYWAY as L1 (the cheapest way to make the closing pass verify instead of argue).**  Astra's reading (i): D1
  says a relational compare's generating set is "its three regions, below / at / past", so the past region of
  `len >= 2` (widths 3, 5-8) is owed.  FB-A's (iii): the body's cases are {1}, {2,3,5-8}, {4}; width 8 sits in width 2's
  case, the far region's branch is discharged by the width-2 rows, and D2 does not bind a non-dominating ternary.
  Grok's (ii): all width cells are (e).  REPAIR4 adds Astra's width-8 fixture (N6, below), which kills `cons_eq2`, both
  pops, `n_C6` and `n_E_cons_ge4` at once (FB-A: "cheap coverage, not floor-owed").  **The grading rule goes to the
  OWNER as rule question 4** (below); REPAIR4 does not depend on its answer.
- **Width reachability (D3's factual half) -- CONTESTED, not decision-critical.**  Width 8: reachable (MIPS64
  `lld`/`ld`/`sd`; all three).  Widths 3/5/6/7: FB-A and Grok "unreachable" (power-of-two issuers; an access starting
  at `wd_data` does not straddle); Astra "reachable" by a different route -- an 8-byte translated PowerPC `lfd` starting
  `8-w` bytes before a granule boundary into a mapping of the macppc WDC base.  The main loop READ `memory_rw.c:183-226`:
  translated accesses ARE split at 1 KB granules (`MRW_SPLIT_MASK 0x3ff`), so the tail chunk reaches the next granule as a
  `w`-byte access at offset 0; FB-A's argument covered accesses starting AT `wd_data` and listed bases (0x1f0, 0x170,
  0x14000000, 0x900001f0) without macppc's.  Astra's route is unmeasured.  No grade depends on it (under every reading the
  past region's reachable member width 8 decides); the contract states it as REASONED-contested.
- **F14 (`cmdlen_ms10`) -- OUT OF CONTRACT (3/3).**
- **F16 -- (e) stands; the REASON is rewritten (Grok, Astra).**  Deletion of the wrap loop drops a wrapped DISPATCH
  (262655 one-byte store/read pairs in one CMDOUT, then 12 bytes: HEAD normalises to 12 and dispatches); `<= 0` differs
  only in the host drain-announce latch (`write_count` 2 is an example, not a universal condition -- 3 divides 513);
  `< -1` is equivalent at the current consumers (Astra).  The glm/kimi phantom-drain breach stays REFUTED
  (`wdc_new_command_reset` clears `write_in_progress`, :919).
- **F17 -- records accepted (3/3)**, with R14 checking BOTH count bytes and R15 sampling the interrupt-count INCREMENT
  across the disabled DATA read (Astra); S4's R1-R5 are rewritten to this adjudication -- their EXHAUSTED, equivalence and
  width-grade sentences cannot be adopted unchanged (Astra).
- **F20 -- FLOOR CELL (3/3), row N3**, built valid (Astra): a 40000-byte transfer with cursor 32768, `atapi_len` 0, the
  starting interrupt acknowledged, two bytes preloaded; HEAD leaves occupancy 0 / IRQ 0, the mutant refills 7232 bytes and
  asserts.  N3 gains a WRITE counterpart (Astra's G2 member, below).
- **F21-F23 -- UPHOLD (3/3).  F24 -- REFINE (Astra):** enumerate Argon's second-pop variants at :1201/:1208
  (`len >= 2` -> `len == 2 || len == 4`) in the width enumeration.  FB-A: Argon was RIGHT on F4 where I was wrong.
- **F25 -- UPHOLD, extended:** the REPAIR4 PRETABLE measures every new row (N1-N6 and the G0/G2 candidates) on HEAD and on
  its named mutants BEFORE table 1.
- **D1 FLOOR, D4 (D2 does not bind the ternary), D6 (S4's new rows over a one-line edit of the shipped PIO row) --
  UPHOLD (3/3).**

## What the packet missed

1. **N5 (FB-A, measured; Astra).**  The (flag 1, `atapi_st` NULL) half of the (flag x `atapi_st`) floor joint.  The
   joint has four cells: (0, NULL) HEAD-equal; (0, non-NULL) N1/N2; (1, NULL) N5; (1, non-NULL) the existing re-arm rows.
   Write all four into the contract.
2. **Three guard cells (Astra, REASONED; PRETABLE measures them):** G0 `!io_enabled && atapi_cmd_in_progress` (flag 0,
   two bytes queued, disable I/O, read DATA: HEAD returns 0 and keeps occupancy 2, the mutant pops); G0
   `!io_enabled && !(atapi_st != NULL && atapi_len == 0)` (complete a DATA-IN, acknowledge STATUS, disable I/O, read DATA:
   HEAD returns 0 without a tick, the mutant runs the completion and asserts INTRQ); G2 READ guard additionally accepting
   F20's cell, then WRITE two bytes (HEAD pushes 2, the mutant takes the read arm).  PCI configuration can disable the WDC
   without resetting the ATAPI fields (`bus_pci.c:775-790`).  Grade each by FB-A's discriminator -- floor iff the
   qualifying operand is a repair-path lvalue (`atapi_st`, `atapi_len`, `atapi_received`, `data_in_len`); the flag-only
   member is graded in the ledger with its delta.
3. **One more (e) cell (Grok):** `flag || (atapi_len != 0 && atapi_received != 0)` -- arm 1000, one width-2 read, a later
   command, the PIO walk; (e) because once `atapi_len > 0` the body (:1318 false) does not test `atapi_received`.  Grok
   also names S4's line 51 ("row 2 holds every (flag 0, received < data_in_len)") as the sentence that hid F20.
4. **The enumeration's FORM (Astra, FB-A, Grok):** replace HELD/EXHAUSTED with a per-guard LEDGER -- each (guard, cell)
   -> detecting row + channel + named mutant, or EQUIVALENT/UNREACHABLE with its writer derivation, or (e) with its delta.
   The class is "dominating-guard operand substitutions and their bounded, body-tested joint cells" (Astra) -- conjuncts,
   disjuncts and cell exemptions, not only pure swaps.
5. **The 14 `prescreen_563.md` LIVE items -- all UPHELD as records or (e) sentences (FB-A ruled each)**: R3:837's 68930
   (68928), R3:1230-1231, R3:1449, R3:1996-1998 and R3:2172-2173, R3:2778/2818-2819 brackets, R3:7462-7463's uncommitted
   citation, the `case 3:` CMDOUT write mutant ((e) sentence or a measured mutant), the uncited owner "write-target
   exclusion", the unfiled BE case-4 lane shift, "eight one-token variants", and four items outside #563 (the
   `seat_verdicts.py` "bytes" column, the `wdcrearmwalk` ranking and arithmetic, `doc/misc.html`'s `t4:`).

## REPAIR4 as adjudicated (for the builder, Opus 5.5; PRETABLE first, its mtime before table 1)

New rows (fixtures synthesised as the shipped PIO row does; every existing row byte-identical):
- **N1** `PIO: stale xfer, no early irq` (S4 Row 1; allocate the declared 36-byte buffer).
- **N2** `stale count, PIO boundary irq` (S4 Row 2; allocate the declared 1000-byte buffer).
- **N3** the F20 joint cell (valid 40000-byte transfer, cursor 32768, ack, two bytes preloaded) + its WRITE counterpart.
- **N4** VD1: a count read after the first 1-byte DATA read of the 1-byte walk, want 32767.
- **N5** `CMDOUT boundary read, no transfer`: ATAPI_PKT_CMD; stores stepping past 12 to 514; one width-2 DATA read;
  oracle `rep_asserts == 0 && warned_null_xfer == 1` (FB-A).
- **N6** width 8: arm three distinguishable bytes (e.g. `12 34 56`), one 8-byte DATA read, check returned bytes, count,
  phase, occupancy and the over-read latch, two endian legs (Astra: HEAD count 1, occ 1, DATAIN, latch clear;
  `cons_eq2` count 2; `n_E_cons_ge4` 0 / COMPLETED; the applicable `pop_ge4` occ 0 and latch set; `n_C6` count 3 and
  zeros).  A two-byte transfer would miss `n_E_cons_ge4` (#475 clamps it back).
- **G0/G2 rows** for each of Astra's three candidates that the PRETABLE measures as distinguishing.
Oracle additions: R14 (DATA-OUT both count bytes), R15 (interrupt-count increment across the disabled DATA read).
Contract: the per-guard ledger (item 4), the (flag x `atapi_st`) four cells, the latch family (e), `D0_nocmd`, `D6_head`,
Grok's (len>0, received>0) cell, `cmd_len` OUT, the width reachability statement, the corrected F16 reason, S4 R1-R17
rewritten.  Then its own pass; then Astra confirms; then the commit unit.

## Rule question 4 for the OWNER (new; REPAIR4 does not wait on it)

Does a guarded body's relational compare on the ACCESS WIDTH `len` (here `len >= 2` inside `consumed`'s ternary) take
D1's three-region generating set (Astra: the past region is owed), the body's case partition (FB-A: width 8 sits in width
2's case; (e)), or the 2026-10-09 derived-input ruling (Grok: every width cell (e))?  The three answers grade `cons_eq2`
and the pops FLOOR, (e), (e), and VD1 FLOOR, FLOOR, (e).
