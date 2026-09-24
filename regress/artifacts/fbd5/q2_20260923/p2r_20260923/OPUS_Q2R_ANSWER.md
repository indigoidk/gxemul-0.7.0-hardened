<!-- Extracted VERBATIM from agent-a10a242a9e44f63dd.jsonl (session 8e474f41), the LAST assistant text block; timestamp 2026-09-23T20:05:15.716Z; model claude-opus-5-5; models seen: ['claude-opus-5-5']. -->

OPUS_SEAT_ALIVE_20260923_Q2R
# CHECKPOINT -- 2026-09-23 15:0x (087a90 sections rewritten; the peer's sections below are untouched)

(That is the first line as it reads now. The file was rewritten while I worked. At the start of the seat the first line was `# CHECKPOINT -- 2026-09-23 10:4x (rewritten by 087a90 after the 09-22 Windows-Update reboot; the peer's section below is untouched)`.)

VERDICT: GAP -- IRQ_RAW_STATUS `if (writeflag == MEM_READ && !d->warned_irq_raw_w)` scores 491/491 green, and the guest can see the difference. After one declined write to +0x184, every later +0x184 read returns 0. Twenty more edits in the bound also stay green: the other four latches in the same conjunct, the five FIQ_STATUS mirrors, and the flag test conjoined with a later site's latch (10). So do the legal narrow write at +0x18c (3) and a case label added from outside (5).

**Baseline and controls.** The baseline is 491 rows, 0 failures, DIFF_FOOTBRIDGE_PASS. The driver reproduces the brief's Q1..Q5 result exactly: 3, 3, 3, 3 and 2 red rows, all X9 all-zero.

**Scope.** I built 434 one-line variants: 425 inside the five arms, plus 4 on the two function-head predicates and 5 extra case labels. 281 are red and 153 are green.

## Variant table (every variant is in `results.tsv`, `results_dom.tsv` and `results_case.tsv`)

Notation:
- F is one of irq_status, irq_enable, fiq_status, fiq_enable.
- L is one of the five warned_* latches. "Later" means later in the fixed order every multi-site sequence uses: A0 IRQ_STATUS, A1 IRQ_RAW, A2 IRQ_EN_CLR, A3 FIQ_STATUS, A4 FIQ_RAW.
- "dir" is the direction test and "flag" is `!d->warned_own`.

| variant text | A0 IRQ_STATUS | A1 IRQ_RAW | A2 IRQ_EN_CLR | A3 FIQ_STATUS | A4 FIQ_RAW | first failing row |
|---|---|---|---|---|---|---|
| (a+) `dir && d->F` (includes Q1..Q5) | 4 red | 4 red | 4 red | 4 red | 4 red | X9 legal len 1 read of <reg> (all-zero, latches clear); at A2, X9 IRQ Clear write 0 (all-zero, ...) |
| (a) `dir && !d->F` | 4 red | 4 red | 4 red | 4 red | 4 red | P0 <reg> read = ...; at A2, P8 legal EnableClear write |
| `dir && d->L`, all 5 latches | 5 red | 5 red | 5 red | 5 red | 5 red | P0; at A2, X5 |
| (b) `dir && !d->L`, all 5 latches | 5 red, 1 row each | **5 GREEN** | 5 red, 1 row each | **5 GREEN** | 5 red, 1 row each | only P7 at A0/A4; only P8 at A2 |
| (c) `dir && len==4`, `len!=1`, `len!=2` | 3 red | 3 red | **3 GREEN** | 3 red | 3 red | X2 legal len 1/2 read = low lanes |
| `flag && len==4`, `len!=1` | 2 red | 2 red | 2 red | 2 red | 2 red | P9 / X1 len 1 as the FIRST access |
| (d) `flag && d->F` | 4 red | 4 red | 4 red | 4 red | 4 red | X6 ... all-zero first / P9 / X4 |
| (d) `flag && !d->F` | 4 red | 4 red | 4 red | 4 red | 4 red | P1..P5 announced exactly once |
| (b') `flag && d->L(other)` | 4 red | 4 red | 4 red | 4 red | 4 red | P1..P5 / X1 |
| (b') `flag && !d->L(other)` | **4 GREEN** | **3 G**, 1 red | **2 G**, 2 red | **1 G**, 3 red | 4 red | green exactly for the later latches; red on "P<n> announced exactly once" |
| (e) `dir && d->F != 0x10` | **4 G** | **4 G** | **4 G** | **4 G** | **4 G** | — |
| (e) `flag && d->F != 0x10` | **4 G** | **4 G** | **4 G** | **4 G** | **4 G** | — |
| seed-valued controls (`ie != 0x30`, `is != 0x18`) | 2 red | | 1 red | | | P0 / P1 / P8 |
| `dir && !(d->F & 0xff00)` | **4 G** | **4 G** | **4 G** | **4 G** | **4 G** | — |
| `dir && !(d->F & 0xff000000)` | ie/fe **G**, is/fs red | same | same | same | same | X8 wide read; at A2, X9 Clear write (wide) |
| `flag && !(d->F & 0xff00)` | **4 G** | **4 G** | **4 G** | **4 G** | **4 G** | — |
| `dir \|\| d->L` | **5 G** | **4 G**, 1 red | **2 G**, 3 red | **2 G**, 3 red | **1 G**, 4 red | green for the own latch and the later latches |
| `dir \|\| d->F`, `dir \|\| !d->F` | 8 red | 8 red | 8 red | 8 red | 8 red | P1..P5 / X6 / X4 / P9 |
| flag reads another latch | 4 red | 4 red | 4 red | 4 red | 4 red | "#2 announced nothing more (latched)" |
| decline body sets another latch | 4 red | 4 red | 4 red | 4 red | 4 red | same |
| `writeflag != MEM_WRITE` (A2: `!= MEM_READ`) | **G** | **G** | **G** | **G** | **G** | equivalent |
| `!idata` (A2: `idata`) | red | red | red | red | red | X4 / X5 |
| byte-lane masks in reads or decline bodies (outside the bound) | **10 GREEN** across the arms | | | | | — |
| A2 `dir && idata != 0x20`, `dir && !(idata>>8)` | | | **2 G** | | | — |
| head predicates missing from the §C.2 list: idata-load `&& len==4` / `&& len!=1`; timer fold `>= IRQ_STATUS` / `>= 0x100` | **4 GREEN** | | | | | — |
| `case 0x1a0: case IRQ_STATUS:` and likewise at 0x1a4, 0x1ac, 0x2a0, 0x2a4 | **G** | **G** | **G** | **G** | **G** | — |

## Equivalence notes

I classified each green with an in-process differential. The frozen device and the variant are linked into one binary. From reset it runs every sequence of up to 3 steps (8,040,200) and 2,000,000 random sequences of 4 to 6 steps. The operations cover the 8 registers, widths 1/2/4, 7 data values and device lines 4, 10, 11 and 18. It compares the return value, the read buffer, the CPU irq line level, the announce count and the call counts. As a control, the frozen device against itself shows 0 divergences.

- **Equivalent in every reachable state (35).**
  - 20 variants keyed on fiq_status. Nothing in the product ever writes it, so it is always 0.
  - 5 `writeflag !=` forms.
  - 4 `dir || own latch` forms. At A1 and A4 gcc emits a byte-identical binary.
  - `dir && !warned_fiq_status_w` at A3, and three FIQ read-lane masks. FIQ reads are always 0.
  - The IRQ_STATUS byte-3 read mask. No device drives irq_status bits 24-31.
  - The fiq_enable byte-3 store in the decline body. fiq_enable cannot be observed.
- **Guest-visible real changes (46).** Shortest sequences from reset:
  - `dir && !L` at A1 (5): `W180/1=0 ; line4+ ; R184/1` returns 0 instead of 0x10. The own-latch form is `W184/1=0 ; line4+ ; R184/1`.
  - Narrow Clear write at A2 (3): `W188/1=0x10 ; W18c/1=0x10 ; R188/1` returns 0x10 instead of 0. The byte write is announced as a bad read.
  - Value and bit conditions on irq fields or fiq_enable at A0/A1/A2 (24). For example, `W188/2=0x400 ; line10+ ; R180/2` returns 0 instead of 0x400. Bit 10 is the cats ISA cascade.
  - The rest: 5 lane masks, 2 idata forms, 4 head-predicate forms, and the case labels at A0/A1/A2. For example, R1a0 returns IRQ_STATUS, and W1ac clears IRQEnable and drops the line.
- **Visible only on the announce channel (72).**
  - Flag test with a later latch (10), and `dir || later latch` (10): `W184/1=0 ; W180/1=0` leaves the second bad write unannounced.
  - `dir && !other latch` at A3 (4): `W180/1=0 ; R280/1` announces the legal read as a bad write and uses up that site's latch.
  - Value and bit conditions whose read value cannot differ (46).
  - Case labels at A3/A4 (2).
- **The brief's Q1 shape is also host-only.** I measured Q1: 298,788 announce divergences and 0 guest-visible ones. A guest row can only catch that shape by scoring the host log.

## Other findings

- **Q1(a).** The §C.2 list leaves out two predicates that dominate every decline. One is the head `if (writeflag == MEM_WRITE) idata = ...`; the other is the timer-fold range test. One-token edits to either stay green. The contract's LATCH axis covers only the site's own latch; other sites' latches are only ever exercised in the one fixed order. And X7's "legal x latch set" cell checks only the announce count. After latching, the read value is checked only by P7 (A0 and A4) and P8 (A2), one seeded cell each, and at A1 and A3 by nothing.
- **Q1(b).** The handler agrees with X9's expectations in all 24 cells, and with my hand derivation (`x9check.out`). In the wide state, IRQ Clear 0x70 leaves 0x10000 and asserts.
- **Q1(c).** The masked products are 0x10 and 0x40 (seeded) and 0x00010010 and 0x00020040 (wide). No state sets any bit 8-15, any bit 18-29, or bits 24-31 of irq_enable or fiq_enable. So the gate comment "bits 8-31 of a field are exercised" is false, and the X8 rows named "(all 32 bits)" overclaim.
- **Q1(d).** All 333 pre-repair row names reappear green. The repair adds exactly X6 54, X7 35 and X9 69.
- **Q4.** The X9 header says "every legal access", but every legal write in the file is len 4.
- **Scratch closure measurement (not a patch).** I added 74 rows to a scratch copy: 20 cross-latch pairs, 48 legal accesses with every latch set, and 6 narrow Clear writes. On the frozen device that gives 565/0. It turns red every in-bound green except the value/bit-specific and case-label families. What stays green is those (clause (e) and the address axis), the byte-lane and idata extras, the fold edits and the 9 equivalent forms. (The case-label variants were not re-scored.)
- **Unrelated model defect.** The CPU irq line can stick high: `line10+` while disabled, then `W188=0x400`, then `line10-` leaves the line at 1 while IRQ_STATUS reads 0. The enable arms assert without setting `irq_asserted`.

## Seat record

- **Model:** Claude Opus 5.5 (claude-opus-5-5[1m]).
- **Read:** the brief; the frozen dev_footbridge.c and diff_footbridge.c in full; the pre-repair diff; the footbridge section of gate_offline.sh; the register offsets in dc21285reg.h; the interrupt routing in bus_pci.c. I also saw the first 30 lines of another seat's task prompt (`codex_ded_q2r.md`) while listing the directory. I read no seat's answer.
- **Ran, all in `/tmp/opusq2r*`:**
  - the baseline build;
  - 434 variants, mutated in place behind a `.MUTANT` sentinel, then restored, checked with cmp against the frozen copy, rebuilt to 491/0, and the sentinel cleared;
  - the differential on 144 greens plus 2 controls, and targeted sequences for 10 more;
  - the X9 check, the pre-repair name comparison and the 74-row scratch experiment.
- **Not touched:** GXEMUL-SEC, est, build and build-asan. The three relevant GXEMUL-SEC files still have their starting md5s. I ran no gate script.

Everything is in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2r\opus\`. Start with `SUMMARY.txt`; the per-variant rows are in `results*.tsv`, the classifications in `classify.txt`, the differential output in `wit/`, `dom_witness.txt` and `dom_witness_case.txt`, and the raw logs and diffs in `variant_logs_and_diffs.tar.gz`.
