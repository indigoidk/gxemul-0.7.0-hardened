# VERDICT: GAP -- write arm: `return cpu->memory_rw(...)` -> the bare call followed by `if (len != 8) return 1;` (W1). Scores 93/93 (`logs/probe_W1.raw`) and changes a guest-visible outcome: an STQ of 0 to SP(0x3fa) leaves flat IIR & 3 at 0x1 instead of 0x2, so the pending TXRDY is lost (`logs/disc_W1.out` vs `logs/disc_base.out`). MEASURED.

The same channel escapes three more ways, all 93/93 and all guest-visible, all measured: W2 (`len != 2`), W3 (a LANE gate, `(relative_addr & 3) != 0`), and W4 (`len == 1 || len == 4`, which exempts exactly the two widths the `iir` rows use). A fifth escape, RD2, is the read-arm mirror: the read arm forwards twice. The x_wfallthru channel is pinned at 2 of the write cells and at no read cell.

Liveness `LCA530_C3_OPUS_20260914`.  `_scratchpad/CHECKPOINT.md` line 1, verbatim:

    # CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED

Seat: Opus 5, Agent tool, MEASURING.  Tree: `GXEMUL-SEC/` only.  The only project directory I wrote into is this one
(`opus_c3_20260914/`: this file, `PREDICT.out`, `logs/`, `instrument/`), following the c2 seat's layout, so every number
below cites a durable path.

---

## HOW IT WAS MEASURED

* **Clone.** `/tmp/gxopus530c3` = `cp -a build/`, plus GXEMUL-SEC's working-tree `src/devices/dev_lca.c` (md5 `8084ff07`,
  the same as table 4's baseline).
  * `BASELINE_CMP CLEAN`.
  * Every build did `rm src/cpus/*.o src/devices/dev_lca.o`, then checked `[ gxemul -nt dev_lca.c ] && [ dev_lca.o -nt dev_lca.c ]`.
  * A clone-local `.MUTANT` sentinel was held while mutants were applied.
  * Both drivers restored the clone and reported `restored == base (byte-identical)`.
  * No mutant binary was identical to base.
* **Instrument.** The shipped `regress/lca_isalane_probe.py`, frozen as a scratch copy, md5 `72e8b25b`.
  * It is byte-identical to the shipped file.
  * It is AST-identical to `fix530_20260914/table4/lca_isalane_probe.table4.py` (checked with `ast.dump`).
  * Its md5s are in `logs/INSTRUMENT.md5` and `logs/INSTRUMENT2.md5`.
* **Discriminator.** `instrument/disc530c3.frozen.py`.  This is NOT a detector.
  * Its encoders, session and build helpers are copied verbatim from the probe.
  * It runs on unmodified `alphabook1`, and every access in it is a guest instruction.
  * It ran on base and on all seven escaping mutants.  Each mutant differs from base ONLY on its own channel, which
    doubles as a cross-control.
* **Predictions before measurement.** `PREDICT.out` (mtime 09:58:42) predates the first completed log
  (`probe_base.raw`, 10:00:06).  **Every one of the 13 mutants scored exactly as predicted, with exactly the red rows
  predicted.**
* **Load.** Two probe lanes, and discriminators only after both lanes had finished.
  * `LCAISALANE_RETRIED=none` on all 13 probe legs.
  * Every probe log ends `LCAISALANE_DONE`, and every discriminator log ends `DISC530C3_DONE`.  Both were checked by
    `tail -1` before copying.
* **Drivers.** Frozen copies: `instrument/drive530c3.run-094641.sh` (table 1) and `drive530c3b.run-095747.sh`
  (table 2 + discriminators).  Their stdout is in `logs/driver1.out` and `logs/driver2.out`.

---

## THE DENOMINATOR -- 13 mutants of the FIXED handler plus base, both tables

| id | edit | 93-row | red rows | discriminator, base -> mutant | disposition |
|---|---|---|---|---|---|
| base | -- | **93/93** | -- | (all channels at their base value) | |
| **W1** | write: bare forward, then `if (len != 8) return 1;` | **93/93** | none | STQ 0 -> SP(0x3fa), flat IIR&3: **0x2 -> 0x1** | **the GAP** |
| **W2** | write: bare forward, then `if (len != 2) return 1;` | **93/93** | none | STW 0 -> SP(0x3fa): **0x2 -> 0x1**; STW -> SP(0x60): 8042 DIB **1 -> 0** | same class |
| **W3** (own) | write: bare forward, then `if ((relative_addr & 3) != 0) return 1;` | **93/93** | none | STB and STW 0 -> SP(0x60) with a queued reply: 8042 DIB **1 -> 0** | same class, lane axis |
| **W4** (own) | write: bare forward, then `if (len == 1 \|\| len == 4) return 1;` | **93/93** | none | STQ and STW at 0x3fa **0x2 -> 0x1**; STW at 0x60 DIB **1 -> 0** | same class; it exempts exactly the `iir` widths |
| **RD2** (own) | read arm: the forward line duplicated | **93/93** | none | LDBU SP(0x3fa) after arming TXRDY, &3: **0x2 -> 0x1** | read-arm mirror (below) |
| D1 (deepseek) | write `byte = data[ofs] ? data[ofs] : data[0];` | **93/93** | none | STL 0x01 -> SP(IER 0x3f9), flat IER: **0x0 -> 0x1** | disclosed data class; its warrant is false (Q3) |
| H1a (kimi-k3, as written) | after `ofs = ...`: `if ((relative_addr & 0x1f) == 0x1c) ofs = 0;` | **93/93** | none | -- | **EQUIVALENT by construction** (below) |
| H1b (pre-shift) | save `lo5 = relative_addr & 0x1f` before `>>= 5`; `if (lo5 == 0x1c) ofs = 0;` | **93/93** | none | LDQ SP(0x3ff)+0x1c: **0x5a000000 -> 0x5a**; STQ 0x7e000000 there, SCR: **0x7e -> 0x0**; direct LDL (4,3) unchanged 0x5a000000 | discarded-address-bit class; disclosure wording too narrow (Q3) |
| r_fwdret (kimi-k3 R1) | read: `if (!cpu->memory_rw(...)) return 0;` | **93/93** | none | -- | **still EQUIVALENT** (below) |
| w_ret0 (kimi CLI Q3.3) | write: bare forward, then `return 0;` | **89/93** | `tailw t7/t6/t5/t3` = 0x4 vs 0x44 | -- | **killed**, so the "escapes 93/93" claim is false on this instrument |
| dd_decl (kimi CLI Q3.1) | write: `if (!data[ofs]) return 0;` before `byte = data[ofs];` | **89/93** | `tailw t7/t6/t5/t3` = 0x4 vs 0x44 | -- | **killed**, so the "escapes 93/93" claim is false on this instrument |

Each mutant's exact source diff is in `logs/<id>.diff`, and its probe log is in `logs/probe_<id>.raw`.

**Why w_ret0 and dd_decl die, checked against the code rather than argued from the scores:**

* `MEMORY_RW`'s split loop (`cpus/memory_rw.c`, `while (len > granule - offset)`) returns `MEMORY_ACCESS_FAILED` as
  soon as a HEAD chunk fails, before the tail is issued.
* The `tailw` heads land at the unmapped port 0x5f:
  * under w_ret0 every head returns 0;
  * under dd_decl every head carries only zero bytes of `tailv(h)`, so it is declined.
* Either way the tail never reaches 0x60, and the 8042 command byte keeps the per-phase reset value 0x04.
* So the per-phase reset that table 4's `d_w6tail` justified is also what kills these two.

**The STx_C route kimi raised for w_ret0 is real but moot here.**  The detector already kills w_ret0.

---

## W1 / W2 -- MEASURED, AND MY READING OF THE FLOOR QUESTION

**Measurement.**  W1 and W2 both score 93/93 with zero red rows.  In the discriminator, W1 flips only the STQ phase
(0x2 -> 0x1) and W2 flips only the STW phase (0x2 -> 0x1).  The control phase, which makes no lca store, stays 0x2 on
all 8 binaries.

**Why no row can catch them.**

* In `dev_ns16550.c`, the only READ arms with side effects are:
  * `com_data` (0x3f8, lane 0), which calls `console_readchar`;
  * `com_iir` (0x3fa, lane 2), which does `&= ~IIR_TXRDY`.
* Every other ns16550 read is inert.
* In `dev_pckbc.c`, a data-port read pops the output queue.  **On an empty queue it returns `last_scancode`**, so the
  pop is unobservable unless a reply is pending.
* The 93 rows store to a read-side-effect port only in session 4h, at 0x3fa, at len 1 and len 4.
* The `tailw` stores to 0x60 find an empty queue: each phase's `kbc_rdcmd` re-arms 0x20 AFTER the store.
* The four len-8 store rows (`st8 lane3`, `w80`, `w81`, `w82`) and the four len-2 store rows all hit inert registers:
  SCR, MCR, IER and MSR.

**Is it a floor cell?  Both readings, with the facts each rests on.**

**AGAINST floor (grok's reading).**

* The write body tests neither `len` nor the lane.
* More decisively, **whether a phantom read is visible is a property of the FORWARDED DEVICE** (does this port have a
  read side effect?).  The handler never reads that property.
* Under the pass-11 floor ("the guard's dominating predicates x the device-state lvalues the repair path reads"),
  nothing obliges a (len, lane) row on this channel.

**The precedent the other seats cite does not say what they cite it for.**

* `c1_w1w` was graded **clause-(e) COVERAGE DEBT, not a floor breach**, by the measuring seat that built it:
  `opus_c1_20260914/OPUS_ANSWER.md`, line 11, "the write body never tests `ofs' against a constant".
* It was rowed anyway, as part of the position-cell class closure.
* So the precedent is *"graded debt, rowed because it sat in the position cell space"*.  It is not *"ruled floor"*.
* The position cell space is not where W1 lives.

**FOR a contract breach (codex, kimi CLI, glm), and this is my reading.**

* The CONTRACT names the edit.  It lists "the write arm's `return' removed, so a store falls into the read arm and
  makes a phantom read of the stored port (x_wfallthru -- the `iir' rows ...)".
* That entry sits in the "DESIGNED to catch" list with **no width or lane scope**.
* W1 is that named edit, with one conjunct.  A detector that catches a named edit only at the widths its rows happen
  to use has not caught the edit.
* **The shape is `#499`'s, measured here directly.**
  * Closing pass 2's mutant was rowed at exactly the widths it was measured at (STB, STL).
  * W4, which exempts exactly those two widths, sweeps the 93-row table clean.
  * Two consecutive passes have now breached the fallthrough channel.  The repair-chain amendment says the next repair
    owes the CLASS closure, not the next cell.

**My disposition.**

* It is not a DEPENDS-ON (d) breach of the fix: the fix did not touch the `return`.
* It IS a breach of the contract as written.
* So, at minimum, L4: the x_wfallthru entry claims more than the rows deliver.
* It is L2 if the round keeps the claim unscoped.
* Either the rows or the claim must change in-round.
* The adjudication between "row the class" and "scope the claim and file" belongs to the flagship.  Both options are
  priced below.

### What rowing the class costs, versus len 2 and 8 at 0x3fa

The observable exists only where a port with a read side effect sits at that lane.  Per lane, on alphabook1:

| lane | read-side-effect port | cells | cost | status |
|---|---|---|---|---|
| 2 | IIR 0x3fa | direct len 1, 2, 4, 8 (1 and 4 rowed) | **+2 phases in session 4h** (STW, STQ): the discriminator's own phases.  They kill W1, W2 and W4 (measured) | measured channel |
| 0 | 8042 data 0x60, with a reply queued (flat self-test, then 0xd1 so that the store lands in `output_byte` and a phantom read pops the 0x55; flat status & DIB) | direct len 1, 2, 4, 8 | **1 new session, 4 phases.**  STB and STW measured; they kill W3 (and W2 and W4 at STW) | measured channel |
| 0 | same, before each split store | tails 3, 5, 6, 7 | 4 phases.  Arming a reply before each `tailw` store would change an existing session's commands and break the table-targeting rule, so it would need a new session | not built |
| 0 | RBR 0x3f8 (`console_readchar`) | -- | needs console input, e.g. MCR loopback | not built; the 8042 is simpler |
| 1 | none established.  ns16550 IER/LSR reads are inert; I did not check 8253 0x41 or CMOS 0x71 | direct | -- | disclose "no side-effect port rowed" |
| 3 direct | wdc0 status 0x1f7.  A read deasserts its IRQ (`dev_wdc.c`, the `wd_command` arm).  BUS_ISA_IDE0 is on for LCA | direct | needs a pending wdc IRQ plus an IRR readback | channel exists in principle; not built |
| 3 heads | none.  Head ports are 0x1f mod 0x20 (0x3ff SCR; 0x1f, 0x3f and 0x5f unmapped) | heads 3, 5, 6, 7 | -- | **EQUIVALENT on alphabook1**, so disclose |

**Recommendation, as a floor on what must happen rather than a ceiling.**

* Add the two 0x3fa phases, plus the lane-0 direct session.
  * That is 6 phases and one new session, and no existing session's commands change.
  * It kills every escape in this table except RD2.
* Add one sentence to the contract.  It should say the fallthrough is caught at lanes 0 and 2 at every direct width,
  EQUIVALENT at the head cells (no such port), and disclosed at lane 1 (no port rowed) and at lane-3 direct (wdc, not
  rowed).
* Adding only the 0x3fa pair leaves W3 escaping.  **The lane axis is the same class one axis over.**

---

## RD2 -- THE READ-ARM MIRROR (own hunt)

**Edit.**  Duplicate the read arm's forward line.  **Score:** 93/93.

**Guest-visible difference.**  An LDBU of IIR through the sparse window, after TXRDY is armed, reads IIR & 3 =
**0x1 instead of 0x2**: the first forward acknowledges TXRDY and the second forward's byte is the one delivered.  This
is the most realistic escape in the table.  An interrupt handler reads IIR and RBR through this window; it does not
STQ to FCR.

**Why it escapes.**

* The only read-side-effect port the probe READS through the handler is 0x60.
* There the 8042 answers a second, empty-queue read with `last_scancode`, which is the same 0x55.
* So `live`, `tailr ctl` and `tailr t*` stay green.  Measured.

**Grading.**  It is an ADDED forward, not a (d) shape of the fix, and the contract does not name it.  So it is
clause-(e) debt outside the contract as written.

**Cost to row.**  One phase: LDBU SP(0x3fa) after `iir_arm()`, want & 3 == 0x2.  That is the cheapest row in this answer.

---

## H1 -- BOTH KEYINGS

**H1a, as kimi-k3 wrote it (post-shift): EQUIVALENT by construction.  Measured 93/93, no reds.**

* After the shift, `relative_addr` is the port.
* `port & 0x1f == 0x1c` implies `port & 3 == 0`, so the port is at lane 0.
* At lane 0, `ofs = 0 % len` is already 0, so forcing it to 0 changes nothing at any port.
* **The premise "should red MCR rows" is false.**  MCR (0x3fc) is exactly such a port, and it is lane 0.

**H1b, keyed on the pre-shift discarded low 5 bits: 93/93, guest-visible.**

* LDQ at SP(0x3ff)+0x1c is a 4-byte head at port 0x3ff.
* Base returns 0x5a000000; H1b returns 0x5a.
* STQ 0x7e000000 at the same address: base leaves SCR = 0x7e, H1b leaves SCR = 0x00.
* The direct LDL at SP(0x3ff), which is the SAME (4,3) cell, is unchanged at 0x5a000000.

**What this shows.**

* The h=4 head cell IS rowed: it is handler-identical to the direct (4,3) cell.
* A mutant can see the difference only through bits the handler discards.
* That is the discarded-address-bit class, as the brief reads it.
* But see Q3.4: the disclosure as worded names only a<4:3>, and 0x1c is a<4:2> = 111.

---

## D1 -- 93/93, DISCLOSED CLASS, DISCRIMINATOR MEASURED

**Discriminator.**  STL 0x00000001 to SP(IER 0x3f9) is lane 1, len 4, ofs 1, with `data[1] = 0` and `data[0] = 1`.
Flat IER reads 0x0 on base and 0x1 under D1.

**Why it escapes.**  Every store row's correct byte is either nonzero, or the whole stored value is zero (`iir stb`,
`iir stl`, the `tailw` heads at 0x5f).  Either way, any substitute position supplies the same byte.

**Why it is not a floor gap, contra deepseek.**  The body never tests the data value.  So the header's by-class
disclosure is the right disposition, and its guest-visibility is already conceded by the disclosure.  The WARRANT
sentence is what is wrong: see Q3.1.

---

## R1 -- r_fwdret IS STILL EQUIVALENT (93/93), AND THE WARRANT IS NOW READ RATHER THAN INFERRED

The new `tailr` heads forward to the unmapped flat port 0x5f (paddr 0x1d000005f).  That is far above `physical_max`, so
the forward reaches `memory_warn_about_unimplemented_addr` (`core/memory.c`).

* That function prints the `non-existant` line when verbosity allows.  The table-4 base log shows those lines for 0x300
  and 0x400.
* It then returns `true` only when `halt_on_nonexistant_memaccess` is set.
* Otherwise it returns `false`, and `memory_rw` zero-fills and takes `do_return_ok`.
* So an unmapped forward returns OK.  r_fwdret's early return never fires, at 0x5f as at 0x400 and 0x300.

**The disclosure stands as written.**

---

## Q1 -- THE CELL SPACE

**The position enumeration is right, and none of my 13 shapes escapes through a position cell.**

* The seven escapes fall into three groups:
  * the fallthrough / forward-count channel (W1-W4, RD2);
  * the disclosed data and discarded-bit classes (D1, H1b);
  * equivalents (H1a, r_fwdret).
* I did not re-run x_rot.  The c2 seat measured it at 38/77, and repair 3 changed no existing session, so its channel
  check stands.  Table 4's `t_tails` (85/93) covers the eight new tail rows.

**What THE CELL SPACE does not enumerate.**  The CONTRACT claims a property on a second axis: the number and direction
of device accesses per guest access.  Its observable is a property of the forwarded PORT, not of (len, lane).  That axis
is where every live escape in this answer sits.

**The DISCLOSED items:**

| item | status |
|---|---|
| address class (exact port value) | right |
| forward-return equivalents | right: R1 re-measured, warrant read |
| data class | right as a class; its warrant sentence is false (Q3.1) |
| lcaisasize | too narrow as worded (Q3.4) |

---

## Q3 -- WRONG STATEMENTS

1. **Header, disclosed-by-class, data.**
   * The header says "every store row carries a NONZERO correct byte, so 'the correct byte is 0' is unrowed at every
     store cell".
   * This is false on the 93-row instrument.
     * `iir stb` and `iir stl` store an all-zero value at (1,2) and (4,2).
     * The `tailw` heads at 0x5f store zero bytes.
     * codex, grok and kimi all found this.
   * The true warrant: *"every store row's correct byte is nonzero OR its whole value is zero, so no row distinguishes a
     substitute position when the correct byte is 0"*.
   * Measured: D1 93/93.
2. **Header CONTRACT, the x_wfallthru entry.**
   * It claims the edit with no width or lane scope.
   * The rows pin it at (1,2) and (4,2) at one port.
   * W1-W4 are measured escapes of the named edit.
   * This is the GAP above.  Its minimum repair is to scope the sentence, and I recommend adding the rows.
3. **kimi-k3's H1 premise.**  It says the post-shift edit "keys PORT bits ... should red MCR rows".  It cannot red any
   row: it is equivalent by construction (lane 0).  Measured 93/93.
4. **Header, lcaisasize disclosure.**
   * The disclosure reads "the size field a<4:3>".
   * H1b keys on a<4:2> (0x1c).
   * The class the handler actually discards is the whole pre-shift low five bits, a<4:0>.
     * The size field a<4:3>.
     * The split head's byte offset a<2:0>.
   * Name the class by a<4:0>, or a bit-2-keyed mutant is outside both the contract and the disclosure.
5. **The panel's "c1_w1w was ruled in-scope" premise** (glm, kimi CLI, codex).  Its measuring seat graded it
   clause-(e) debt (`opus_c1_20260914/OPUS_ANSWER.md`, line 11).  It was rowed as part of the position class closure.
   The precedent is weaker than cited, which is why my Q2 reading rests on the contract text and the repair-chain
   amendment instead.
6. **kimi CLI Q3.1 and Q3.3.**
   * The claim: a data-keyed decline, and a forced-failure return on the write arm, each "escapes 93/93".
   * Both measured **89/93**, killed by the four `tailw` rows through the split's head-failure abort (above).
   * The mechanism kimi named (STx_C) is real, but the detector already sees these edits.

**Verified, no error found:**

* the fix comment (it now says "load or store", pass 2's omission corrected);
* POSTTABLE 4's per-leg scores, as re-read from `table4/logs/lane*.out`;
* the table-targeting rule, since repair 3 only added sessions.

**Not checked:**

* lane-1 read-side-effect ports (8253 0x41, CMOS 0x71);
* the wdc 0x1f7 channel (not built);
* RBR 0x3f8 (not built);
* tables 1-3 (not re-run).

---

## CLONE

Both drivers restored `/tmp/gxopus530c3`.  I then checked it by hand:

* no `.MUTANT`;
* `dev_lca.c` cmp-clean against GXEMUL-SEC;
* `gxemul -nt dev_lca.c`.

**The clone is DELETED**, together with `/tmp/gxopus530c3_bins`.

* GXEMUL-SEC's `src/devices/dev_lca.c` is unchanged: md5 `8084ff07` before and after.
* No process of mine is running.
* No project path outside `regress/artifacts/lcaisalane/opus_c3_20260914/` was written.
