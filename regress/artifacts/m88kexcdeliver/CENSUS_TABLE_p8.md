# MEASURED census: the PSR state in which each switch-1 arm is entered, over all 46 rows
Source: `killtable_opus_p8/CENSUS_cells.txt` -- a `fatal("[ M88KCENSUS v=%d psr=0x%08x t=%d ]")` at the top of
`m88k_exception()` in the scratch clone, harvested from the probe's own pty transcripts.  43 distinct
(vector, PSR, is_trap) triples.  The census build scored **46/46 on the shipped instrument**, so the
instrumentation is non-perturbing.  DERIVED FIRST (PRETABLE section 2), THEN MEASURED: identical.

Bits: MODE 0x80000000 | C 0x10000000 | SFD1 0x8 | IND 0x2 | SFRZ 0x1.  A cell is CLOSED when both values occur.

| arm | measured PSRs at entry | MODE | C | SFD1 | IND | SFRZ |
|---|---|---|---|---|---|---|
| 4 MISALIGNED  | 9000000b, 8000000b(t0/t1), 80000009, 80000002(t0/t1), 00000002 | both | **both** | both | **both** | both |
| 5 UNIMPL      | 8000000b, 80000002, 00000003, 00000002                         | both | **0 only** | both | **1 only** | both |
| 6 PRIVILEGE   | 8000000b, 80000002, 00000003, 00000002                         | both | **0 only** | both | **1 only** | both |
| 7 BOUNDS      | 8000000b, 80000002                                             | 1 only (unreachable, disclosed) | **0 only** | both | **1 only** | both |
| 8 DIV0        | 8000000b, 80000003, 80000002(t0 x20 / t1), 00000002             | both | **0 only** | both | **1 only** | both |
| 9 OVERFLOW    | 8000000b(t0/t1), 90000002, 80000002(t0/t1), 80000000, 00000002  | both | **both** | both | **both** | both |
| 10 ERROR      | 8000000b, 80000002                                             | 1 only (unreachable, disclosed) | **0 only** | both | **1 only** | both |

**Denominator: 35 cells (7 arms x 5 stcr-settable 88100 bits).  2 unreachable with a warrant.  33 reachable.
23 closed.  10 OPEN: {UNIMPL, PRIVILEGE, BOUNDS, DIV0, ERROR} x {C, IND}.**

Three consequences the shipped contract states otherwise:
1. **OVERFLOW x {C, IND} is CLOSED** (`ovfc` 0x90000002, `indclr` 0x80000000) -- the probe v15 docstring lists
   OVERFLOW among the arms whose {C, IND} cells are debt.  Measured wrong.
2. **{any arm} x {SFD1} is CLOSED at every one of the seven** -- every arm sees both a 0x...0b entry (a frozen
   second fault, SFD1 SET) and a 0x...02/03 entry (SFD1 CLEAR).  The docstring calls it debt.  Measured wrong.
   At DIV0 this is architecturally forced and worth knowing: `X(divu)` tests SFD1 BEFORE the divisor
   (`cpu_m88k_instr.c`, anchor `X(divu)`), so the instruction route can never reach the DIV0 arm with SFD1 set --
   only the tb1 route can, and `trapfrozen8` is that row.
3. **BOUNDS and ERROR are OPEN and the docstring's list omits both.**  That is the dangerous direction: a reader
   consulting the contract concludes those two arms are covered.

**Provenance check.** The disclosure sentence came from kimi's pass-7 answer, and it contradicts that answer in
both directions: kimi wrote *"`implemented = !(PSR & C)` sweeps on every arm except OVF -- `ovfc` is the only row
in the whole probe presenting C=1 at switch 1"*, which is exactly what the census measures.  The round's
transcription added OVERFLOW and dropped BOUNDS and ERROR.
