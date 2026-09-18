# VERDICT: GAP -- (1) `ofs = (relative_addr & 3) % len;` followed by the inserted line `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;` scores 77/77 and moves the byte at the four split-TAIL cells (3,0) (5,0) (6,0) (7,0), both arms, at a MAPPED port. (2) x_wfallthru (delete the write arm's `return`) scores 77/77 and loses the ns16550's IIR_TXRDY on a store to port 0x3fa. BOTH MEASURED, each with a guest-visible discriminator run on base and mutant.

Liveness `LCA530_C2_OPUS_20260914`.  `_scratchpad/CHECKPOINT.md` line 1, verbatim, read at 05:1x:

    # CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED

(At the start of this seat, ~04:5x, line 1 read `# CHECKPOINT -- 2026-09-13 ~23:2x   HEAD 9c91999 (records)   crimewidthkill #529: TABLE 7 PROBES RUNNING; rung-3 seat out`. The file was overwritten while this seat ran.)

Seat: Opus 5, the Agent tool, MEASURING.  Tree: `GXEMUL-SEC/` only.  I wrote nothing into GXEMUL-SEC except this directory.

---

## HOW IT WAS MEASURED

* Clone `/tmp/gxopus530c2` = `cp -a build/`, plus GXEMUL-SEC's working-tree `src/devices/dev_lca.c` (md5 `dc49ebdd...`,
  the same before and after this seat).  `BASELINE_CMP CLEAN`.  `rm src/cpus/*.o` before the first build; every build
  checked with `[ gxemul -nt dev_lca.c ] && [ dev_lca.o -nt dev_lca.c ]`.  I dropped a clone-local `.MUTANT` sentinel,
  and both drivers restored the clone (`cmp` clean against SEC, the binary newer than the source, `restored == base
  (byte-identical)`).  No mutant binary was identical to base.
* Instrument: `regress/lca_isalane_probe.py` frozen as a scratch copy, **md5 `299645d6...`, identical to the shipped
  probe and to table 3's `lca_isalane_probe.table3.py`** (`logs/INSTRUMENT.md5`).
* Discriminators (NOT detectors): `instrument/opus_c2_demo.py` (16 rows) and `instrument/opus_c2_demo2.py` (6 rows).
  Both are the probe's own helpers, lines 157-337 and 467-494 copied verbatim, plus new sessions.  They run on
  unmodified `alphabook1`, and every access in them is a guest instruction.
* Drivers `instrument/opus530c2.run-050257.sh` and `opus530c2b.run-050845.sh` (frozen copies).  Two probe lanes each.
  **Every log below ends with its completion sentinel** (`LCAISALANE_DONE` / `OPUSC2_DONE`).  `RETRIED=none` on every
  leg.
* Durable logs: `logs/` (my sweep) and `logs_panel/` (the panel mutants relayed mid-run).

---

## Q1 -- DOES "THE CELL SPACE" ENUMERATE THE SPACE CORRECTLY?

**The axes are right.**  The handler reads `relative_addr` only through `(relative_addr >> 5)`:

* as the forwarded port P, which is the same on both arms, and
* through `P & 3` in `ofs`.

It reads `len` only through `len == 0`, `% len` and the fill-loop bound.  So (len, lane = P & 3, direction) is the
handler's own partition.

**The reachable len values are enumerated right: direct 1, 2, 4, 8 at any lane, plus split pieces.  The split pieces
are where the enumeration goes wrong.**  MRW_SPLIT_MASK is 0x3ff on the VIRTUAL address, which is 32 ports per 1 KB.
Every split therefore produces:

* a HEAD of length h = 1..7 at a port that is 0x1f mod 0x20 (lane 3), and
* a TAIL of length 8-h (LDQ/STQ) or 4-h (LDL/STL) at a port that is 0 mod 0x20 (lane 0).

**The header states both facts as if the probe's one boundary were every boundary:**

* "a head always ends at port 0x3ff" -- it ends at 0x1f, 0x3f, ... 0x3ff, ...  The lane (3) is the invariant, the
  port is not.  This does no harm by itself: a head cell is still (h, 3).
* **"split TAILS start at port 0x400 (lane 0), where nothing is mapped, so a tail cell shows only as a whole-access
  failure"**.  This one is false, and it is load-bearing.  Tails start at 0x20, 0x40, 0x60, 0xa0 ..., and bus_isa
  puts the 8259 at +0x20 and +0xa0, the 8253 at +0x40, and the 8042 at +0x60.

**OMITTED CELLS (should be rowed): (3,0), (5,0), (6,0), (7,0), for both R and W -- eight cells.**

* The tails of length 1, 2 and 4 are handler-identical to the direct lane-0 cells.  Those are rowed at 0x3fc, 0x60
  and 0x300.
* Tails of length 3, 5, 6 and 7 exist only as tails.
* At the probe's only tail port, 0x400, the position channel **cannot vary**:
  * a tail READ forwards to non-existent memory, and memory_rw zero-fills it (`memory_rw.c`, the physical_max arm:
    `memset(data, 0, len)`), so the tail contributes a zero at whichever position;
  * a tail WRITE goes nowhere.
* So the rows the header leans on (`h1/h2/h3 ldq`, `h3 ldl`, `h1/h2/h3 stq`, whose tails are (7,0) (6,0) (5,0) (1,0))
  see a tail **decline** (whole-access failure, e.g. table 3's x_len6 via `h2 ldq`) and never a tail **mis-placement**.
* This is the probe's own principle 2, *"zero readback alone proves nothing"*, applied to its own tails.

**MEASURED at port 0x60 (8042 data).**  An unaligned LDQ/STQ at `SP(0x5f) + 0x1f/0x1e/0x1d/0x1b` gives head 1/2/3/5
at port 0x5f (unmapped) and tail 7/6/5/3 at port 0x60.  `logs/demo_base.raw` is 16/16:

| row | cell | base | t_tails |
|---|---|---|---|
| tailr t7 | (7,0) R | 0x5500 | 0x550000 |
| tailr t6 | (6,0) R | 0x550000 | 0x55000000 |
| tailr t5 | (5,0) R | 0x55000000 | 0x5500000000 |
| tailr t3 | (3,0) R | 0x550000000000 | 0x55000000000000 |
| tailw t7/t6/t5/t3 | (7,0)..(3,0) W: 8042 command byte, flat readback | 0x44 | 0x21 |

**CELLS LISTED AS ROWED THAT NO ROW EXERCISES: NONE.  Verified in one run rather than argued:** `x_rot` =
`ofs = ((relative_addr & 3) + 1) % len;` rotates the position at every cell with len >= 2 and leaves every len-1 cell
alone.

* **Measured 38/77** (`logs/probe_x_rot.raw`).  Its 39 red rows match my written prediction **exactly**, with zero
  extra and zero missing.
* The prediction was every row of every len >= 2 cell: all 24 direct cells (len 2/4/8 x lane x R/W) and the 10
  head-only cells (len 2, 3, 5, 6, 7 at lane 3 x R/W; head len 4 is the direct (4,3) cell), across 39 rows.  No len-1 row reddened.
* So every len >= 2 cell the header lists as rowed has a row whose channel varies with the position there.
* The len-1 cells have only one position.  Their mis-decode (byte dropped) is HEAD's own shape, measured red on
  `r11/r12/r13/w12/w13` by table 1 and HEAD_r3.
* By construction, every store row's value carries a nonzero correct byte and different bytes at the other positions,
  and every read row compares the FULL register against a nonzero device byte.  So alternatives other than the
  rotation are also visible.  (That last point is argued, not measured.)

---

## Q2 -- FLOOR GAPS IN THE 77-ROW DETECTOR

### GAP 1 -- the split-tail cells (the SAME CLASS the class closure closed)

* **Edit:** insert after `ofs = (relative_addr & 3) % len;`
  `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;`
* **Score:** 77/77 (`logs/probe_t_tails.raw`).  Discriminator: 8/16 (`logs/demo_t_tails.raw`), the eight tail rows
  above.
* **Rows expected to catch it, and why they cannot:** `h1 ldq`, `h2 ldq`, `h3 ldq`, `h3 ldl`, `h1 stq`, `h2 stq`,
  `h3 stq` all put a (7,0), (6,0), (5,0) or (1,0) tail through the handler.  But the tail lands on port 0x400.  There
  the forwarded byte is a zero-fill (read) or a write into nothing, so moving it changes nothing observable.
* **Guest-visible difference:** a guest LDQ that straddles a 1 KB sparse line onto the 8042 data port sees the device
  byte one register byte too high.  A STQ there hands the 8042 the next byte of the value instead of the right one.
  The command byte reads back 0x21 instead of 0x44.
* **Why it is in scope rather than disclosable:**
  * The header ENUMERATES these cells and declines to row them on a stated premise that is measured false.
  * The edit is a (len, lane) conjunct of the position rule.  That is exactly the shape of `c1_w1w`
    (`ofs == 1 && len > 2`), which the previous pass accepted as a gap and rowed.
  * `% len` distinguishes every len in the body, and the header's own axis is len 1..7.
  * My grading: the class the round claims closed, one sub-space over.  **L2 if the contract's "at every cell of that
    space" stands; at minimum an L4 wrong record** in THE CELL SPACE paragraph.
* **Cheapest closure:** two sessions (`tailr`, `tailw` in `instrument/opus_c2_demo.py`).  That is 8 value rows plus
  controls against the 8042 at 0x60, with no new port and no timer.
* Note for a detector: the (1,3) and (2,3) heads at 0x5f end the host on HEAD.  That is the expected HEAD-red, the same
  as `h1/h2` today.

### GAP 2 -- x_wfallthru (kimi-k3's shape; I re-measured it and dispute the "DISCLOSED")

* **Edit:** in the write arm, `return cpu->memory_rw(...)` becomes `cpu->memory_rw(...)`.  The store then falls into
  the read arm: a phantom 1-byte READ of the same port, a fill of the (store) buffer, then `return 1`.
* **Score:** 77/77 (`logs/probe_x_wfallthru.raw`; table 3 measured the same).  Discriminator: 14/16
  (`logs/demo_x_wfallthru.raw`):

| row | base | x_wfallthru |
|---|---|---|
| iir stb: (1,2) STB 0 to SP(0x3fa), then flat IIR & 3 | 0x2 (TXRDY) | 0x1 (NOPEND) |
| iir stl: (4,2) STL 0 to SP(0x3fa), same readback | 0x2 | 0x1 |

* **Why no row catches it:** every port the probe stores to (SCR, MCR, IER, MSR, the 8042 command port, the unmapped
  0x5f and 0x400) reads back without a side effect.
* **What it breaks in a guest:**
  * dev_ns16550.c's `com_iir` READ arm clears IIR_TXRDY, so an FCR store loses a pending transmit-ready interrupt.
  * The `com_data` READ arm calls `console_readchar`, so **every THR store (every console output byte) consumes one
    pending input character**.
  * The 8042 data READ pops the output buffer.
* **The "DISCLOSED" is wrong twice:**
  * The contract text (the probe header's clause (e) list) does not mention it.  `grep -i "fallthru\|phantom"` over
    `regress/lca_isalane_probe.py` returns nothing.  The disclosure lives only in table 3's PRETABLE and POSTTABLE,
    and PRETABLE itself names the ports that would see it ("RBR, IIR").
  * Its warrant, "no port it stores to has a read side effect", is a fact about the probe's port choice.  It is not a
    reason the edit is outside the contract.
* **Floor classification (for adjudication):** `if (writeflag == MEM_WRITE)` dominates the fix's edited line
  `byte = data[ofs]`.  Deleting the guarded body's `return` keeps the guard and nulls its routing, which is clause (d)'s
  "keep the guard, remove its effect".  I read it as floor-shaped.  At minimum the header must disclose it by name.
* **Cost to row it:** one session, 3 rows (`iir` in the demo).

### THE DENOMINATOR -- every shape built and swept (12 mutants: 6 of mine + the 6 relayed panel mutants; base measured twice)

| mutant | edit to the FIXED handler | 77-row | red rows | discriminator | disposition |
|---|---|---|---|---|---|
| base | -- | **77/77** (x2: `logs/`, `logs_panel/`) | -- | 16/16, 6/6 | |
| **t_tails** | insert `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;` | **77/77** | none | **8/16** | **GAP 1** |
| **x_wfallthru** | delete the write arm's `return` | **77/77** | none | **14/16** | **GAP 2** |
| x_rot | `ofs = ((relative_addr & 3) + 1) % len;` | 38/77 | exactly the 39 predicted (every len >= 2 cell) | 7/16 | the channel check for the whole cross |
| swapmod | `ofs = (relative_addr % len) & 3;` | 75/77 | h7 ldq (0x5a00), h7 stq (0x96) | 12/16 (tailr/tailw t7, t5) | killed -- but see the caution below |
| r_fwdret | read arm: `if (!cpu->memory_rw(...)) return 0;` | 77/77 | none | 16/16 | EQUIVALENT on alphabook1 (below) |
| w_ret1 | write arm: `return 1 \| cpu->memory_rw(...)` | 77/77 | none | 16/16 | EQUIVALENT on alphabook1 (below) |
| G1..K2b | see PANEL MUTANTS | | | | |

**CAUTION on swapmod.  It is killed by two rows, and only because of a coincidence in the port.**  0x3ff = 1023, and
1023 is 0 mod 3, 3 mod 5 and 3 mod 6.  So at the probe's single head boundary, `(P % len) & 3` equals `(P & 3) % len`
for heads 3, 5 and 6.  Only h7 (1023 mod 7 = 1) sees it.  At any other boundary (port 0x1f: 31 mod 3/5/6 = 1) the h3,
h5 and h6 rows would also see it.  This is clause (f)'s layout caution in another coat: the head rows' kills of a
modulus edit depend on WHICH boundary was chosen.  The GAP-1 tail rows at 0x60 add kills for it too (0x60 mod 5 = 1,
0x60 mod 7 = 1, measured red).

**r_fwdret / w_ret1 are equivalent.  The reasoning, checked against the code:**

* No ISA device on alphabook1 fails an access.  I scanned `DEVICE_ACCESS` in dev_8259/8253/pccmos/lpt/wdc/fdc/pckbc/
  ns16550 for `return 0;`, and the only hit is ns16550's out-of-range arm, which the flat mapping cannot reach.
* An unmapped forward returns OK with a zero fill (`memory_warn_about_unimplemented_addr` returns false).  The
  exception is `halt_on_nonexistant_memaccess`, and there `cpu->running = 0` makes the OUTER memory_rw fail whatever
  the handler returns.
* So the forward's return value never differs.  Guest visibility would need a failing forward (a STx_C success flag, or
  a split store whose head fails before its tail), and nothing produces one.  Recommend: disclose as EQUIVALENT by
  name.

**Thought about, not built:**

* `i < len` -> `i <= len` in the fill loop: a 1-byte host write past the caller's `data[]` on direct reads.  ASAN-
  visible and host-only.  For split heads the tail overwrites it, so it is not guest-visible.
* `byte = data[ofs] ? data[ofs] : data[0]`: the generalisation of C1 below, a value-keyed forward.  It escapes by the
  same argument as C1.
* Mutants keyed on port bits other than `& 3` (address-decode, the p_port10 class).  Disclosed, and consistent with the
  joint-cell rule: the body never tests those bits.

---

## PANEL MUTANTS (relayed by the main loop mid-run; built in the same clone, `logs_panel/`)

| id | edit | 77-row | red rows (got vs want) | discriminator (base -> mutant) | note |
|---|---|---|---|---|---|
| G1 (grok) | write `byte = data[(len == 5 && ofs == 3) ? 0 : ofs];` | **76/77** | `h5 stq` 0x7e vs 0xc3 | -- | **grok's premise is false; the main loop's reading is right.**  C4e slot 4 is `k0(SP(UART_SCR) + 0x1b)`, a real 5-byte head |
| G2 (grok) | `if (len == 0 \|\| (len == 5 && writeflag == MEM_WRITE)) return 0;` | **76/77** | `h5 stq` 0x5a (SCR's prior value kept) vs 0xc3 | -- | `h3 stq` stays green: its head lands before its 5-byte tail is declined |
| K1 (kimi-k3) | after `relative_addr >>= 5;`: `if (relative_addr == 0x400 && len == 4) return 0;` | **77/77** | none | `demo2`: LDQ SP(SCR)+0x1c 0x5a000000 -> sentinel 0x0bad1d8a (whole load abandoned); LDL SP(0x400) 0x0 -> sentinel | guest-visible (a load's register kept); see below |
| C1 (codex) | write `byte = data[ofs == 2 && !data[2] ? 0 : ofs];` | **77/77** | none | `demo2`: STQ 0x04 via SP(MSR), flat MSR 0xb0 -> **0xb4**; STL 0x04 the same, 0xb0 -> 0xb4 | codex's discriminator is confirmed exactly |
| K2a (kimi CLI) | write `byte = data[(ofs == 3 && len == 4) ? 0 : ofs];` | **76/77** | `st4 lane3` 0x0 vs 0x7e | -- | confirmed |
| K2b (kimi CLI) | write `byte = data[(ofs == 3 && len == 8) ? 0 : ofs];` | **75/77** | `st8 lane3` 0x0 vs 0x6d; `ld8 lane3` 0x0 vs 0x6d000000 | -- | confirmed.  The read row reddens too, because it reads back the SCR value the bad store left |

**K1: disclose, but not under the tail paragraph's warrant.**

* The cell (4,0) is rowed (`st4 lane0`, `ld4 lane0` at 0x3fc).  K1 adds an exact-ADDRESS conjunct inside it.  The body
  never tests `relative_addr` against a constant, so under the joint-cell rule this is a clause-(e) value/address
  disclosure, the p_port10 class.  I agree with disclosing it.
* But the header's "a tail cell shows only as a whole-access failure -- seen by the split rows" is **not** why it is
  safe.  No row produces a len-4 tail.  The tail lengths the probe produces are 7 (h1), 6 (h2), 5 (h3 ldq/stq), 3 (h5),
  2 (h6), and 1 (h7 and h3 ldl).  It is also not a floor cell: a (4,0) decline keyed on len and lane, not address, is
  caught by the direct rows.

**C1: disclose by class, as intended.**  It is a value conjunct the body never tests.  Every store row carries a
NONZERO correct byte, so "the correct byte is 0" is an unrowed value class at every store cell.  Name the class in the
disclosure (with `data[ofs] ? data[ofs] : data[0]` as its general form), not only C1.

---

## Q3 -- WRONG STATEMENTS

1. **Probe header, THE CELL SPACE (and the brief's SETTLED bullet 4):**
   * "split TAILS start at port 0x400 (lane 0), where nothing is mapped, so a tail cell shows only as a whole-access
     failure".
   * False: tails start at every port that is 0 mod 0x20, including 0x20/0xa0 (8259), 0x40 (8253) and 0x60 (8042).
   * At 0x60 a tail's byte and its position are guest-visible (measured, GAP 1).
   * "not rowed per length" therefore leaves eight live cells unrowed on a false premise.
2. **Probe header and the session-4e comment:** "a head always ends at port 0x3ff" / "A split head always ends at port
   0x3ff (lane 3)".  A head ends at every port that is 0x1f mod 0x20.  Lane 3 is the invariant, 0x3ff is the probe's
   choice.  It is harmless for the cell, but it hides the swapmod coincidence above.
3. **POSTTABLE 3 (and PRETABLE 3):** "x_wfallthru 77 (PREDICTED EQUIVALENT on this probe ...) -- DISCLOSED".
   * "Equivalent on this probe" is accurate.
   * "DISCLOSED" is false: the probe header's contract has no such entry.
   * The edit is not equivalent for a guest (measured, GAP 2).  PRETABLE's own text names the ports that would catch it.
4. **Fix comment in dev_lca.c:** "or the 1- or 2-byte head of an unaligned LDL/LDQ that memory_rw splits at 1 KB".
   * It omits STL/STQ.  `fix530_20260914/HEAD_r3.out` records `h1 stq alive` and `h2 stq alive` = `dead` on HEAD.
   * The store heads ended the host too, and the probe's own row notes say so ("(1,3) STQ head ... was a host death on
     HEAD").
5. **Probe header CONTRACT, "at every cell of that space"**: this is false for the eight tail cells of item 1 while
   they stay unrowed.  It is true (x_rot, measured) for every direct and head cell.

POSTTABLE 3's per-mutant counts, re-derived from the diffs: c1_w2 75, c1_w1w 75, c1_r4 75, x_len6 74 (with the
`h2 stq` stays-green explanation), x_len8lane0 76, x_lane2clamp 72, x_w1drop 75.  I agree with all of them.  The base
77/77 and the head 49/77 = 20 + 8 are consistent with HEAD_r3.out.  I found nothing else wrong in it.

---

## CLONE

`/tmp/gxopus530c2` was restored by both drivers.  I re-checked it by hand before deleting: no `.MUTANT`,
`dev_lca.c` cmp-clean against GXEMUL-SEC, `gxemul -nt dev_lca.c`.  Then I **DELETED** it, together with
`/tmp/gxopus530c2_bins` and `/tmp/gxopus530c2_bins2`.  GXEMUL-SEC's `dev_lca.c` is unchanged: md5 `dc49ebdd...`
before and after.  The only project path written is `regress/artifacts/lcaisalane/opus_c2_20260914/`.
