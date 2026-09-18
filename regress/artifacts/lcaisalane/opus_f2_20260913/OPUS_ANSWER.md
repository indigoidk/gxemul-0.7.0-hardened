# lcaisalane F2 -- the Opus 5 seat (Agent tool, measuring)

*** TRANSCRIBED BY THE MAIN LOOP: the seat's own REPORT.md write was refused by the subagent file rule, and the Agent
seats leave no file in the panel dir.  Verdict and table VERBATIM from the returned answer; every logged value below was
re-read by the main loop from `logs/f2_{head,A,B,C}.out` and `logs/witness_{head,A,B,C}.out` (each ends in its
completion sentinel) before this file was written. ***

Liveness: `OPUS_SEAT_ALIVE_20260913_LCAISALANE_F2`, and CHECKPOINT.md line 1 quoted verbatim:
`# CHECKPOINT -- 2026-09-13 ~23:2x   HEAD 9c91999 (records)   crimewidthkill #529: TABLE 7 PROBES RUNNING; rung-3 seat out`

## VERDICT: C

Decline only the cells that end the process today (`ofs > len`, latched `(once)`, `return 0` both directions); leave the
equality cells exactly as they behave now; **FILE F2 as its own open row.**  This **reverses my own pass-1 vote for A**,
on a measured fact.

## How it measured
Four scratch clones in WSL Gentoo at `/tmp/gxlcaf2/{head,A,B,C}` (-j2, `rm src/cpus/*.o` per variant, freshness-checked,
the head clone `cmp`-clean vs `git show HEAD:`).  Variants are HEAD's text by unique-match replacement (`variant_{A,B,C}.diff`).
One frozen instrument (`lca_f2_probe.py`) reading FULL register values -- immune to the witness's sentinel/mask alias.
`SENT` = 0x11335577 preserved = the access was DECLINED (the register kept its pre-load value).

## Cells that never end the host under any variant

| cell (len,ofs,dir) | access | HEAD | A | B | C |
|---|---|---|---|---|---|
| R(1,1) | LDBU LSR | `0x0` false-zero | `SENT` decline | `0x60` byte | `0x0` false-zero |
| R(2,1) | LDWU LSR | `0x6000` byte in lane1 | `0x6000` | `0x6000` | `0x6000` |
| R(2,2) | LDWU MSR | `0x0` false-zero | `SENT` decline | `0xb0` byte lane0 | `0x0` false-zero |
| W(1,1) | STB 0x3a->IER | `0x3a` **lands** | `0x0` **DECLINED (regress)** | `0x3a` lands | `0x3a` lands |
| W(2,1) | STW 0x5a00->IER | `0x5a` data[1]=hi byte | `0x5a` | `0x5a` | `0x5a` |
| W(2,2) | STW 0x0040->MSR | `0xf0` **lands** data[0] | `0xb0` **DECLINED (regress)** | `0xf0` lands | `0xf0` lands |

## Cells that END THE HOST on HEAD (one session each; readback via the flat mapping)

| cell (len,ofs,dir) | access | HEAD | A | B | C |
|---|---|---|---|---|---|
| R(1,2) | LDBU MSR | **DEAD** (attrib) | alive, `SENT` | alive, `0xb0` byte | alive, `SENT` |
| R(1,3) | LDBU SCR | **DEAD** | alive, `SENT` | alive, `0x0` (SCR=0) | alive, `SENT` |
| R(2,3) | LDWU SCR | **DEAD** | alive, `SENT` | alive, `0x0` (SCR=0,lane1) | alive, `SENT` |
| W(1,2) | STB 0x40->MSR | **DEAD** | alive, MSR `0xb0` unchg | alive, MSR `0xf0` **lands** | alive, MSR `0xb0` unchg |
| W(1,3) | STB 0x3c->SCR | **DEAD** | alive, SCR `0x0` unchg | alive, SCR `0x3c` **lands** | alive, SCR `0x0` unchg |
| W(2,3) | STW 0x7e00->SCR | **DEAD** | alive, SCR `0x0` unchg | alive, SCR `0x7e` **lands data[1]=HIGH byte** | alive, SCR `0x0` unchg |

Shipped witness (its oracles encode the ACCEPT contract): HEAD 13/16, A 15/16 (`ofs1 answer` red; `ofs1 zero` FALSELY
green via the sentinel alias), **B 16/16**, C 15/16 (`ofs1 zero` red = false-zero unfixed, as C intends).

## Q1 -- C
* **B rejected on the ADDITION LICENCE, and the measurement seals it.**  The read arm does not fold today (it drops the
  byte, `i==ofs`); B invents read folding.  Its only warrant is "the write arm folds", but the write arm's `% len` is
  plausibly a bounds-safety hack -- the read/write ASYMMETRY is the tell -- and transferring it to reads invents a
  guest-visible semantics for an access the 21066 HRM does not define, with no measured delta and no hardware warrant;
  B ships the measured (2,3) wrong-byte incoherence (`w23` -> 0x7e, the high byte landing at port P).
* **A rejected because it REGRESSES working behaviour to fix a non-safety defect** (measured `w11` 0x3a -> 0x0, `w22`
  0xf0 -> 0xb0), silently (S2), to fix a detectable pre-existing defect (F2).
* **C is the minimal de-fatalisation.**  Removes all six host kills (measured), regresses nothing (every served cell
  byte-identical to HEAD), invents no semantics; `ofs > len` = "the lane is strictly beyond the access width" is a
  principled minimise-blast-radius line.
* **Weakest claim on my side:** C ships F2, a measured false success.  Acceptable only because it is the status quo and
  is FILED as its own row.  If a shipped false success is intolerable, take the OTHER below -- not A or B.
* **OTHER considered, not recommended:** a direction-asymmetric guard (reads decline at `ofs >= len`, writes at
  `ofs > len`) fixes F1+F2 with zero regression, but it is exactly the clause-(d) `&& writeflag == MEM_READ` mutant shape.

## Q2
F1 UPHOLD (six cells DEAD on HEAD, reads AND writes).  F2 UPHOLD (measured; remains under C -> file).  F3 UPHOLD (settles
D1 against A).  F4 UPHOLD with caveat (split cells reasoned, not witnessed -- the split fires only on a translated access).
F5 [the witness sentinel] UPHOLD (`0x0bad1dea & 0x60 == 0x60`; measured on witness A).  F6/F7 REFINE/FILE.  F8 UNDEFINED
(no oracle); identical under all variants.

## Q3
None of F1-F4 overturned.  Overturns the FRAMING that the round must pick a contract for the equality cells: the base
handler is memory-safe (read loop bounded by `len`; write uses `data[ofs % len]`), so the only critical defect is the
kill, fixable without touching the equality contract.

## Q4
* The WRITE exit cells also kill -- every seat framed the exit cells as reads.
* A guest-visible discriminator DOES exist (the table) -- it cannot adjudicate correctness: there is no hardware oracle.
* The base handler is memory-safe; OOB fears materialise only if a fix also drops the `% len`.

## Trees
`/tmp/gxlcaf2/{A,B,C}` keep `.MUTANT` sentinels (scratch clones; nothing in GXEMUL-SEC depends on them);
`/tmp/gxlcaf2/head` is clean.

## Could not check
Split cells (len 3/5/6/7, need a translated access); whether any alphabook1 firmware issues narrow ISA accesses; the
`PHYSICAL` failure path; the correctness of any narrow-access behaviour (no hardware oracle).
