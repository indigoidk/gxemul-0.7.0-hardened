# #529 crimewidthkill -- CLOSING PASS 3, Opus compile-and-measure seat (2026-09-13)

Liveness: `OPUS_CLOSE3_ALIVE_20260913`.  First line of `_scratchpad/CHECKPOINT.md`:
`# CHECKPOINT -- 2026-09-13 ~18:5x   HEAD 9c91999 (records)   crimewidthkill #529: TABLES 5 + 6 RUNNING (repairs 6, 7)`

**VERDICT: `GAP: in DEVICE_ACCESS(crime), make the first statement of case CRIME_CONTROL`
`if (writeflag == MEM_READ) d->warned = 0;`** -- the latch is re-armed by an accepted read of CRIME_CONTROL.  It scores
**121/121** (`logs/probe_rearm_ctlrd.raw`), and it is NOT equivalent: refused lb +7, accepted lw +8, refused lb +6 gives
**1 notice on base and 2 on the mutant** (`logs/disc_c3.out`).  Contract item 8 claims re-arm "closed over every place an
accepted access can go ... each switch arm AND EACH BRANCH", and the CONTROL arm's own body tests `writeflag`.

It is one of **TWELVE** survivors.  **All twelve scored 121/121, all twelve were predicted to** (`PRETABLE.out`, 20:44:08,
before the first build at 20:45:51 -- `logs/ORDER.txt`), and a guest-only session showed **all twelve NON-equivalent**.
They fall in **four of the five classes the brief says are closed** (re-arm, pre-set, latch keying, address-bit landing),
plus the label-answer class.  The enumerations were built from the members earlier passes found, not from the cells the
body's own tests distinguish, so each class stayed open one cell over.

## Apparatus

* Scratch clone `/tmp/gxopus529c3` = `cp -a build/`.  Its `dev_sgi_ip32.c` `cmp`-clean vs SEC (md5 `8c1d1545`).
  Baseline rebuilt in the clone, gxemul `-nt` source (base md5 `f06efcf6`).
* Sentinel held across the 12 mutant builds.  Every mutant binary is distinct from base (`logs/BINARIES.md5`); diffs are
  in `logs/<m>.diff`.
* Restore: source from SEC, rebuilt; `cmp` clean, gxemul `-nt`, and the binary byte-identical to the baseline.
  The sentinel was then removed and the clone deleted (`logs/build_c3.out`, `logs/probe_c3.out`).
* Instrument: the shipped 121-row `regress/crime_width_probe.py`, md5 `c083168c` (== `killtable6_20260913/
  crime_width_probe.table6.py`), frozen once to `/tmp/cwp_close3.py` (`logs/INSTRUMENT.md5`).
* Four probe lanes ran concurrently (nothing else running on the host).  **13 of 13 logs end `CRIMEP_DONE`**, all with
  `CRIMEP_CONTROL=OK`.  The discriminators (`disc_c3.py`) ran serially afterwards; every session was `clean=True`.
* Nothing was written to GXEMUL-SEC except this directory.  `build/` still `cmp`s clean for `dev_sgi_ip32.c`, and has
  no `.MUTANT`.
* **The shipped probe changed underneath this run**: md5 `444de77c`, mtime 21:05:39 -- repair 8 / killtable7, in
  progress.  Every number here is against the 121-row instrument the brief names.  Repair 8 is assessed by READING only,
  at the end.

## Mutant table (instrument md5 c083168c; each score from its `logs/probe_<m>.raw`, summary `table_c3.out`)

| # | mutant | exact edit to dev_sgi_ip32.c | class | predicted | measured | red rows | equivalent? discriminator, base -> mutant (`logs/disc_c3.out`) |
|---|---|---|---|---|---|---|---|
| - | base | none | | 121/121 | **121/121** | none | -- |
| M1 | rearm_ctlrd | first stmt of `case CRIME_CONTROL:` `if (writeflag == MEM_READ) d->warned = 0;` | re-arm | 121 | **121/121** | none | **NOT**: lb+7, lw+8, lb+6 -> notices 1 -> **2** |
| M2 | rearm_dogclr | `if (idata & DOG_ENABLE) {...}` gains `else d->warned = 0;` | re-arm | 121 | **121/121** | none | **NOT**: lb+7, sw+8 0x01, lb+6 -> 1 -> **2** |
| M3 | rearm_ctl0 | `if (idata != 0) fatal(...)` gains `else d->warned = 0;` | re-arm | 121 | **121/121** | none | **NOT**: lb+7, sw+8 0x0, lb+6 -> 1 -> **2** |
| M4 | pre_istat | `d->warned \|= CRIME_W_LEN;` between `case CRIME_INTSTAT:` and `case CRIME_INTMASK:` | pre-set | 121 | **121/121** | none | **NOT**: lw+0x10, lb+7 -> 1 -> **0** |
| M5 | pre_revbr | `d->warned \|= CRIME_W_LEN;` after `cpu->pc = ...gpr[MIPS_GPR_RA];` | pre-set | 121 | **121/121** | none | **NOT**: lw+0 from 0xbfc05180 (pc->ra both), lb+7 -> 1 -> **0** |
| M6 | pre_dogbr | `d->warned \|= CRIME_W_LEN;` inside the DOG_ENABLE branch | pre-set | 121 | **121/121** | none | **NOT**: sw+8 0x200, lb+7 -> 1 -> **0** |
| M12 | pre_ctlrd | first stmt of `case CRIME_CONTROL:` `if (writeflag == MEM_READ) d->warned \|= CRIME_W_LEN;` | pre-set | 121 | **121/121** | none | **NOT**: lw+8, lb+7 -> 1 -> **0** |
| M7 | byp_rev | latch test -> `if (!(d->warned & CRIME_W_LEN) \|\| relative_addr == CRIME_REV) {` | latch keyed on a label (TEST side) | 121 | **121/121** | none | **NOT**: lb+7, lb+0, lh+0 -> 1 -> **3** |
| M8 | byp_time | the same, `== CRIME_TIME` | latch, test side | 121 | **121/121** | none | **NOT**: lb+7, lb+0x38, lh+0x38 -> 1 -> **3** |
| M9 | ans_hi32_b5 | before the goto: `if (!(relative_addr & 0x20)) odata = d->reg[relative_addr / 8] >> 32;` | answer at label + one address bit | 121 | **121/121** | none | **NOT**: with the probe's BIT seed lb/lh+0x10 read 0x0/0x0 on BOTH (the blindness); with SOFTINT=0x0000ffff00000000, lb/lh+0x10 read 0x0/0x0 -> **0xffffffffffffffff/0xffffffffffffffff**; with INTMASK=0x00005aa5.., lh+0x18 reads 0x0 -> **0x5aa5** |
| M10 | land_b4clr | before the goto: `if (writeflag == MEM_WRITE && !(relative_addr & 0x10)) d->reg[relative_addr / 8] = idata;` | landing keyed on one address bit | 121 | **121/121** | none | **NOT**: refused sb 0xff at +0x47, then ld +0x40: 0x0 -> **0xff**; refused sh 0xabcd at +0x4c, then ld +0x48: 0x0 -> **0xabcd** |
| M11 | ans_ctl_lb | before the goto: `if (len == 1 && relative_addr == CRIME_CONTROL) odata = 1;` | answer at CONTROL, 1 byte | 121 | **121/121** | none | **NOT**: lb+8 0x0 -> **0x1** (lh+8 0x0 on both, so `ctl v0` is structurally blind to it) |

Channel line: every survivor varies one of the channels the contract already names (the notice count, the answer value,
or a landing read back by an accepted ld).  **Each is a missing CELL, never a missing channel**: the probe's own
machinery sees each one the moment the cell is driven.

## Q1 -- per class: is the enumeration complete and true?

The method: derive each class's cells from the partitions the body's OWN tests induce, then check each cell against the
rows.  That is the carrier's JOINT CELLS rule.

**A. The answer at every named label.  NOT TRUE, two ways.**
* **CONTROL is rowed at 2 bytes only.**  `ctl v0` is an lh; no refused lb at +0x08 exists anywhere in the probe.
  POSTTABLE 5's DENOMINATOR ("at both widths") is therefore false for CONTROL; M11 escapes.
  * For the REGISTER form this cell is equivalent: CONTROL's low byte is 0.
  * For any other value it is not, and every other label has both an lb and an lh row.  That is a sibling-parity
    asymmetry.
  * Repair 8's text now discloses it as a label x width joint.  I accept that as a disclosure, but it was a wrong record
    in the 121-row header.
* **The IRQ seed `0x0101000010000001` is zero in bytes 2-3 and 5-6.**  So "a decline that answers the register shows"
  holds only for the two forms tested: the whole-register form (low bytes) and the lane form (top bytes).
  * The 4-byte read path's own half, `reg >> 32`, hands a narrow read `0x01010000`, whose low byte and halfword are 0.
    So M9 escapes at INTSTAT and INTMASK.
  * **Repair 8's `0x0101010111010101`, nonzero in every byte, closes this.**  Predicted; I did not run it.
* DOG (`0x0123456789abcdef`) is sound against any byte selection.  REV, CONTROL and TIME above bit 31 are held at 0
  by the model, so their disclosure is right.

**B. The latch keyed on any single axis.  INCOMPLETE: the enumeration models only the SET side.**
* The set side: contract 4's rule is "every axis value is a FIRST refusal followed by another".  I checked every value
  of width, direction, label and address bits 0-9 (set-first and clear-first) against the sessions' first refusals.
  **It holds.**
* The TEST side is missing.  A latch that does not SUPPRESS at axis value v needs v as a NON-FIRST refusal (after the
  latch is set) in a counted session.
  * That holds for widths, directions, address bits, CONTROL (sh08b; the dog session's lh +8), INTSTAT, INTMASK and DOG.
  * **It fails for REV and TIME**: every refusal at +0x00 or +0x38 is its session's only refusal, or its first
    (M7, M8).
  * This is a single-axis (label) key, and not in the disclosed list, which names only JOINT and unnamed-offset latches.

**C. Pre-set and re-arm in every arm and branch.  NOT TRUE; seven cells open.**
The body-tested partitions of the switch are:
* REV: {window, not}.
* CONTROL: {R, W}, and within W: DOG bit {0, 1} x RESET {0, 1} x the text test's residual {0, nonzero}.
* INTSTAT and INTMASK as separate labels of one arm.
* DOG, TIME, and the default arm {R, W}.

*Re-arm* (an accepted access between two refusals).  Rowed: REV both halves, INTSTAT, INTMASK, DOG, TIME, default R/W,
every accept-path branch, and CONTROL W as DOG=1 / RESET=0 / residual nonzero (0x0201 only).  Open:
* **CONTROL R** (M1).
* **CONTROL DOG=0** (M2).
* **CONTROL residual 0** (M3).
* RESET=1 is disclosed and unrowable.

*Pre-set* (an accepted access before a counted session's first refusal).  Rowed: CONTROL W with DOG=0 and residual
nonzero (latch x5's 0x01), REV normal, INTMASK, DOG, TIME, the default arm, 8W, 8R, and 4-byte in both lanes.  Open:
* **INTSTAT alone** (M4).
* **the REV redirect branch** (M5).
* **the DOG_ENABLE branch** (M6).
* **CONTROL R** (M12).
* the CONTROL residual-0 path (reasoned, not built: no accepted zero-control write precedes any first refusal).

Contract 4's own wording, "in EVERY switch arm an accepted access reaches first in some counted session", is circular:
it names exactly the arms that happen to be reached.  DISCLOSED names only HARD_RESET as unrowed, which implies the
other branches are rowed.  They are not.

**D. Effects keyed on a single address bit.  NOT TRUE for landings.**
* **Every refused store the test reads back has address bit 4 SET**: 0x37, 0x30, 0x18, 0x27f, 0x27c, 0x1ff and 0x1fc.
* The only bit-4-clear refused stores are at +0x00 and +0x08, which the prelude rewrites on the next access.
* So "every bit 0-9 is carried both ways by a refused access of each kind" is false for the LANDING kind at bit 4
  CLEAR, at both widths.  M10 escapes.
* Its bit-4-clear slots include SOFTINT and HARDINT (+0x20..+0x2f).  A landing at SOFTINT feeds the next reassert, which
  is an interrupt a guest never raised.
* Also measured-by-reading: no 2-byte read-back store has bit 1 set.  A single-axis bit-1 landing is still caught by
  `sb keeps` (+0x37), so only the width x bit joint escapes, which is clause (e).
* The answer, notice, fall-through, re-arm and pre-set kinds all hold at every bit, both values.

**E. Refused stores that land.**  At DOG, INTMASK, the far block and the middle block the rows are sound, and the
all-ones data catches every OR/replace form.  **The open cell is the address-keyed one in D (M10)**, which the disclosure
says is NOT in the single-unnamed-offset class and is rowed.

## Q2 -- floor gaps in the 121-row test, most severe first

1. **Re-arm of the latch by an accepted CONTROL access** (M1 read, M2 DOG-clear write, M3 zero-residual write).
   * Contract 8 claims this whole class, which is its third instance (codex F2, codex pass 1, codex pass 2).
   * These are cells the CONTROL body's own tests distinguish, so they are floor under the joint-cells rule.
   * Cheapest repair (predicted, not measured): add `("lw", 0x08)`, `("sw", 0x08)` with 0x01, and `("sw", 0x08)` with
     0x0 to `KINDS`.  Each of those writes is ACCEPTED and none stops the CPUs.
2. **Latch test-side keyed on REV or TIME** (M7, M8).
   * A guest hammering narrow reads at CRIME_TIME, or the PROM probe loop at CRIME_REV, floods the log, which is
     exactly what the latch exists to stop.
   * Cheapest repair: two refusals appended to latch x5 after its first, one at +0x00 (a normal pc) and one at +0x38.
     Refusals do not enter the switch, so nothing else in that session moves.
3. **A landing keyed on one address bit, bit 4 clear** (M10).
   * It contradicts an explicit DISCLOSED sentence.
   * Cheapest repair: seed an unnamed bit-4-clear slot, e.g. sd +0x40, then refused sb +0x47 and sh +0x44, then ld +0x40
     wanting the seed.
4. **Pre-set in a branch or label** (M4, M5, M6, M12, and residual-0 by reading).
   * Repair 8's prologue now reaches M4, M5 and M6 (see below); M12 and residual-0 stay open.
5. **Answer forms** (M9, M11).
   * Closed by repair 8's seed and disclosure respectively, both by reading.

## Repair 8 (probe md5 444de77c, in flight) -- read, not measured

* **Closes by construction:**
  * M4, M5, M6: the prologue now carries sw 0x0201, a REV read from the PROM window, and lw +0x10.
  * M9: the seed is `0x0101010111010101`.
  * M11: disclosed.
* **Still open (unchanged rows):**
  * M1, M2, M3: `KINDS` is unchanged.
  * M12: there is no accepted +0x08 read anywhere.
  * the residual-0 pre-set.
  * M7, M8: the new `rev said` / `time said` rows count the FIRST refusal's text, not a second one at the label.
  * M10: there is no new bit-4-clear read-back.
* **NEW, and it is the #499 shape (predicted, not built):**
  * The prologue swapped CONTROL `0x01` for `0x0201`.  The 0x01 write was the ONLY accepted DOG-CLEAR CONTROL write
    before a first refusal in any counted session.
  * So `} else d->warned |= CRIME_W_LEN;` on the DOG test was caught by `latch x5` on the 121-row test, but has no row
    on repair 8.
  * Repair: the prologue should write both 0x0201 and 0x01, plus 0x0 and a lw +0x08.

## Q3 -- wrong statements

1. **Contract 8**, "closed over every place an accepted access can go ... each switch arm AND EACH BRANCH": false.
   CONTROL R, DOG-clear and residual-0 were measured open (M1-M3).  POSTTABLE 5's DENOMINATOR, "re-arm in CONTROL's DOG
   and text branches", is true as far as it goes, but it is not the class.
2. **Contract 4 and the brief's Q1**, "pre-set ... in EVERY switch arm / every arm and branch", with DISCLOSED excepting
   only HARD_RESET: false.  M4, M5, M6 and M12 were measured open.
3. **Contract 4**, "the class closed on its single axes": false.  The enumeration covers the set side only (M7, M8).
4. **DISCLOSED**, "every bit 0-9 is carried both ways by a refused access of each kind": false for the landing kind,
   bit 4 clear (M10).  Repair 8 amends the bit-0 case for 2-byte accesses but not this one.
5. **POSTTABLE 5 DENOMINATOR**, "the answer at every named label ... at both widths": false at CONTROL (M11).
   **Contract 9**, "lh sees every value lb sees": true of values, but it does not make the 2-byte row stand in for the
   1-byte cell against a width-keyed edit.
6. **Contract 9 and the brief**, "INTSTAT/INTMASK 0x0101000010000001 ... so a decline that answers the register shows":
   true for the whole-register and lane forms only (M9).
7. **Contract 9**, "TIME 66-990 (low bytes)": false as a universal.
   * TIME at the refused read is always a multiple of 66, since `to_add = delta * 66`.
   * It is **0** in 42 of 800 time small-cells across every log under `artifacts/crimewidthkill/`, and in 2 of 32
     base-build cells.  For example, `killtable4_20260913/logs/probe_base.raw` and `opus_close2_20260913/logs/
     probe_base.raw` give `time lb ... (raw 0)`.
   * In those runs `time lb v0` cannot see a register answer; `time lh v0` in its own session usually still can.
   * **Repair 8's replacement sentence is also wrong in its mechanism.**  It reads "TIME's low byte is 0 for about 0.3%
     of runs (66-990 includes 256, 512, 768)".  But 256, 512 and 768 are not multiples of 66, so they never occur.
     The real blind case is TIME == 0, at about 5%.
8. **Checked and TRUE:**
   * The SETTLED counts: `killtable5 check_pred.out` reads `CHECKPRED exact=59 differs=1 of 60`, and killtable6's reads
     `exact=27 differs=0 of 27`.
   * `table5.out` has 48 `NEW` rows and `table6.out` has 24.
   * The table-6 instrument md5 equals the shipped 121-row probe's.

## What I could not measure

* **None of the twelve against repair 8's instrument**, which was mid-edit.  Repair 8's closures and its new DOG-clear
  pre-set hole are reasoned.
* **The residual-0 pre-set** (not built).
* **The kill power of any repair suggested above.**
* **Multi-machine (function-static latch) behaviour**, which is disclosed.
* **Host-load sensitivity**: four emulators ran at once, and every control row stayed green.
