# VERDICT: GAP -- read arm, after its forward: `if (len != 1) cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr, &byte, 1, MEM_READ, CACHE_NONE);` (R2w). It scores **111/111** (`logs/probe_R2w.raw`) and changes what the guest sees: an **LDL** of IIR 0x3fa with TXRDY armed delivers lane-2 IIR & 3 = **0x1 instead of 0x2** (`logs/disc2_R2w.out`). That is the contract-named RD2 edit, gated on exactly the one width its single row uses. Four more edits of the same forward-count class also score 111/111 and are guest-visible, all MEASURED: **WT6/WTsplit** (the split-TAIL write cells), **RD2L0** (lane-0 reads) and **L3gate** (lane-3 direct, whose header warrant is false again). The next repair owes the whole-class closure tabled in Q1.

Liveness `LCA530_C4_OPUS_20260914`.  `_scratchpad/CHECKPOINT.md` line 1, verbatim, read at the end of this pass:

    # CHECKPOINT -- 2026-09-15 ~07:xx   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED

(At the start of the pass, 2026-09-14, it read `# CHECKPOINT -- 2026-09-14 ~05:0x   HEAD 9c91999 (records)   #529 TABLE 8 PROBES RUNNING; #530 CLOSING PASS 2 FIRED`.)

**Seat:** Opus 5, Agent tool, MEASURING.  **Tree:** `GXEMUL-SEC/` only.  **Writes:** the only project directory I wrote into is this one (`opus_c4_20260914/`: this file, `logs/`, `instrument/`).  **Resumed twice:** the first session exited at about 12:55 with nothing measured, and the clone was re-verified before any use.  My first reading, in `logs/PREDICT.out`, leaned CLOSES; that was before the panel cells were measured, and the measurements overturned it.

---

## HOW IT WAS MEASURED

### Clone

* `/tmp/gxopus530c4` was made with `cp -a build/`, then given GXEMUL-SEC's working-tree `src/devices/dev_lca.c` (md5 `8084ff07`, the fixed handler).
  * `BASELINE_CMP CLEAN`.
* Every build did `rm src/cpus/*.o src/devices/dev_lca.o`, then checked `[ gxemul -nt dev_lca.c ] && [ dev_lca.o -nt dev_lca.c ]`.
* A clone-local `.MUTANT` sentinel was held while mutants were applied.
* Both drivers restored the clone.  Both report `restored == base (byte-identical)`, and no mutant binary is identical to base.
* `logs/cleanup.out` is the final clearance, run before deletion:
  * no `.MUTANT`;
  * `dev_lca.c` cmp-clean against SEC;
  * `gxemul -nt dev_lca.c`;
  * clone binary == base.
* Then **CLONE AND BINS DELETED**.  GXEMUL-SEC `dev_lca.c` is still `8084ff07`.

### Instrument

* The shipped `regress/lca_isalane_probe.py`, frozen as `lca_isalane_probe.c4.frozen.py`, md5 **`b36b1de1`**.
  * It is byte-identical to table 5's `lca_isalane_probe.table5.py`.
* **The shipped file was edited at 00:19, mid-run, by the coordinator** (header corrections, md5 `7ba1fd57`).
  * I checked it: it is **AST-identical** to the frozen copy (comments only).
  * So both tables ran ONE instrument.  Driver B's guard was switched from byte identity to AST identity for that reason.
  * Its first launch aborted at the byte guard, before touching the clone: `logs/driverB_abort1.out`.
  * Both md5s are recorded in `logs/INSTRUMENT2.md5`.

### Discriminator

* `instrument/disc530c4.frozen.py`.  This is NOT a detector.
  * Its encoders, session and build helpers are copied verbatim from the probe.
  * It runs on unmodified `alphabook1`, and every access in it is a guest instruction.
  * It has 17 channels, each in its own session.
* It ran on all 11 binaries, and every log ends `DISC530C4_DONE`.
* **Each mutant moves only its own channels** (`logs/DISC_SUMMARY.out`), which doubles as the cross-control.

### Predictions

* `logs/PREDICT.out` covers table 1 and `logs/PREDICT2.out` covers table 2.  Each was written before its table's first log.
* **11 of 11 scores matched their predictions.**
* Every red set is exact.  Wpure and dataB each red exactly table 5's 8 x_wfallthru rows: `iir stb/stl/stw/stq` and `kbcq b/w/l/q dib`.

### Load

* At most two probe lanes of mine at once, beside #529's four.
* `LCAISALANE_RETRIED=none` on all 11 legs, and every probe log ends `LCAISALANE_DONE`.

### Drivers

* Table 1: `instrument/drive530c4.sh`.  It ran directly and was not edited while running.
* Table 2: `instrument/drive530c4b.run-003612.sh`, frozen.
* Second discriminator lane: `instrument/disclaneR.sh`.
* Driver B was stopped by PID after its L3gate discriminator, because the rest of its list duplicated lane R's `disc2_*`.
  * So `DRIVE530C4B_DONE` is absent by design.
  * `logs/disc_WT6.PARTIAL_duplicate_stopped.out` is the stopped duplicate and is not cited.

---

## THE DENOMINATOR -- 10 mutants of the FIXED handler plus base, on the 111-row instrument

Every mutant's exact source diff is in `logs/<id>.diff`, and its probe log is in `logs/probe_<id>.raw`.

| id | edit (after the forward unless noted) | 111-row | discriminator, base -> mutant | disposition |
|---|---|---|---|---|
| base | -- | **111/111** | (all 17 channels at their base value) | |
| Wpure | write: `return` removed | 103/111 (the 8 fallthrough rows) | A, C x4, E-store x4 lanes, F, G | caught; cross-control |
| dataB | write: `if (byte != 0) return 1;` (fallthrough only on a ZERO store) | 103/111 (the same 8) | C x4, E-store x4 | caught; the rows store 0 |
| **dataA** | write: `if (byte == 0) return 1;` (fallthrough only on a NONZERO store) | **111/111** | A: STB 0x06 / STL 0x60000 -> FCR, IIR & 3 **0x2 -> 0x1**; F; G | escape, data axis (Q2 reading) |
| **L1gate** | write: `if ((relative_addr & 3) != 1) return 1;` | **111/111** | E tog61 store flip **0x0 -> 0x10**; F pit41 **0x34/0x00 -> 0x00/0x34**; G REG C **0x40 -> 0x00** | escape; lane 1 is DISCLOSED, and its warrant is now correct |
| **L3gate** | write: `if ((relative_addr & 3) != 3) return 1;` (lane-3 direct AND every head) | **111/111** | E tog63 store flip **0x0 -> 0x10** | escape; **the lane-3 warrant is FALSE** (Q3.3) |
| **WT6** (panel) | write: `if (len != 6) return 1;` | **111/111** | C: 2-byte head at 0x5f and 6-byte TAIL at 0x60, DIB **1 -> 0** | escape; **tail cells unclassified** |
| **WTsplit** | write: `if (len != 3 && len != 5 && len != 6 && len != 7) return 1;` | **111/111** | C: tails 6, 5, 3 and 7, each DIB **1 -> 0** | escape; tail cells unclassified |
| **R2w** (panel) | read: `if (len != 1)` + a second forward | **111/111** | B: LDWU / LDL / LDQ SP(0x3fa), lane & 3 **0x2 -> 0x1**; D at (8,0) and tail 6; E-load at all 4 lanes | **THE GAP**, the contract's RD2 gated on width |
| **R2w2** (panel) | read: `if (len == 2)` + a second forward | **111/111** | B: LDWU **0x2 -> 0x1** (only) | escape, same class |
| **RD2L0** | read: `if ((relative_addr & 3) == 0)` + a second forward | **111/111** | D: two replies queued, then LDBU (1,0), LDQ (8,0) or LDQ tail 6, DIB after **1 -> 0**; E tog68 load flip | escape; lane-0 reads unclassified |

**Shapes swept:**

* write-arm fallthrough, gated on {none, data == 0, data != 0, lane 1, lane 3, len 6, len in {3,5,6,7}};
* read-arm duplicated forward, gated on {len != 1, len == 2, lane 0}.

**Discriminator: 11 binaries x 17 channels** (`logs/DISC_SUMMARY.out`).

**Not built** (measured by construction through a channel measured on another mutant):

* RD2 gated to lane 1 or lane 3 alone.  R2w's E-load flip at 0x61 and 0x63 is the same mechanism.
* The 8253 counter 0 at 0x40 as a tail channel.

Tables 1-5 were not re-run.  Repair 4 changed no existing session, and my base is 111/111 on the same instrument.

**Why each escape escapes, read against the rows:**

* **R2w, R2w2.**
  * The only RD2 row is `iir lca rd`, an LDBU (len 1).
  * Every other lca read at lane 2 is MSR 0x3fe (`r22`, `r82`, `r42`, `ofs2 wide`), whose read is inert.
* **RD2L0.**
  * Every lca read of 0x60 in the probe (`live`, `tailr ctl`, `tailr t*`) has ONE reply queued.
  * The duplicated read then hits the empty-queue arm of `dev_pckbc.c`'s data port, which returns `d->last_scancode`.  That is the byte just popped, so the delivered value is unchanged.
* **WT6, WTsplit.**
  * `tailw`'s tails at 0x60 find an EMPTY queue, because that session never queues a reply.  Its 0x60 and 0x20 commands only change the 8042's state.  The phantom read changes nothing there.
  * Their heads land on 0x5f (unmapped) or 0x3ff (SCR, inert).
* **L1gate.**  No lane-1 row stores to a port whose access has a side effect.  The lane-1 stores all go to IER.
* **L3gate.**
  * Lane-3 stores go to SCR.
  * wdc 0x1f7 does not exist on this machine (Q1).
* **dataA.**  Every fallthrough row stores ZERO: `iir stb/stl`, `iirw`, and `kbcq`.

---

## Q1 -- THE ENUMERATION, checked against alphabook1's ISA devices

### What is on the bus

This is from `bus_isa_init` with `BUS_ISA_IDE0 | BUS_ISA_IDE1` (`dev_lca.c`) and the device lengths.

| device | ports |
|---|---|
| 8259 | 0x20-0x21 and 0xa0-0xa1 |
| 8253 | 0x40-0x43 |
| 8042 (`pckbc`, `DEV_PCKBC_LENGTH` 0x10) | **0x60-0x6f** |
| pccmos | 0x70-0x71 |
| ns16550 | 0x3f8-0x3ff and 0x2f8-0x2ff |
| lpt | 0x378-0x37a |

* No FDC is present (flag not set), and no VGA without X11.
* **wdc0 and wdc1 are added ONLY `if (diskimage_exist(machine, n, DISKIMAGE_IDE))` (`bus_isa.c`).**  The probe loads `0x20000000:alpha_dummy.bin`, which is not a disk.  So **0x1f0-0x1f7 and 0x170-0x177 are UNMAPPED on the probe's machine.**  grok is right.

### Read (access) side effects, by lane

Each is read from the source; "MEASURED" means a discriminator channel shows it.

| lane | port(s) with an access side effect | status |
|---|---|---|
| 0 | 8042 data 0x60 (the pop; with TWO replies queued, a second read pops the second: **D, MEASURED**); **8042 PC-style stub 0x68/0x6c** (below); 8253 counter 0 at 0x40 (16-bit flip-flop); RBR 0x3f8/0x2f8 (`console_readchar`) | observable |
| 1 | **stub 0x61/0x65/0x69/0x6d (E, MEASURED)**; **8253 counter 1 at 0x41 after a LSB+MSB control word (F, MEASURED)**; **CMOS 0x71 with REG C selected, where a read clears it and a store sets it (G, MEASURED)** | observable, no arming needed at 0x61 |
| 2 | IIR 0x3fa/0x2fa (clears TXRDY: A/B, MEASURED); stub 0x62/0x66/0x6a/0x6e (E, MEASURED); 8253 counter 2 at 0x42 | observable |
| 3 direct | **stub 0x63/0x67/0x6b/0x6f (E, MEASURED)**.  wdc 0x1f7 only with an IDE image | observable, no arming needed |
| 3 split heads (P = 0x1f mod 0x20) | mapped head ports are **0x3ff and 0x2ff only**, both ns16550 SCR (the `default:` arm, inert).  0x1f..0x3df, 0x5f, 0x7f and so on are unmapped; the stub's 0x60-0x6f holds no 0x1f-mod-0x20 port | **EQUIVALENT**.  Still true with IDE images: wdc and altstatus add no 0x1f-mod-0x20 port |
| 0 split tails (P = 0 mod 0x20) | 0x20 and 0xa0 (8259: its read arm only reads irr/isr, inert); **0x40** (8253 counter 0); **0x60** (8042: C and D, MEASURED); 0x300 and 0x400 unmapped | observable at 0x40 and 0x60 |

**The stub.**

* `DEVICE_ACCESS(pckbc)`, PC-style branch, reads `if (relative_addr != 0 && relative_addr != 4) { /* TODO (port 0x61) */ odata = 0x21; { static int x = 0; x++; if (x&1) odata ^= 0x10; } ... return 1; }`.
* That is **a function-static counter bumped on EVERY access to 0x61-0x63 and 0x65-0x6f, read or write**, and bit 0x10 of the answer is its parity.
* So on base, a flat read, then ONE lca access, then a flat read leaves bit 4 unchanged.  One extra access flips it.
* The control channel (two plain reads flip 0x10) is live on every binary: `ctl=0x10` in all 11 discriminator logs.

### Answers to the Q1 sub-questions

**Heads EQUIVALENT: correct.**

**Lane-1 DISCLOSED: the classification is right, and the ORIGINAL warrant was false.**

* The original header said "no port with an armable read side effect".
* 0x61 needs no arming, and 0x41 and 0x71 need one store each.
* The coordinator's 00:19 correction states this accurately, and I measured all three.

**Lane-3 direct: the classification is DISCLOSED, and the CORRECTED warrant is FALSE.**

* The 00:19 header now says "LANE-3 DIRECT (no read-side-effect port is present on this probe's machine ...)".
* That is measured false.  L3gate flips E tog63.
* See Q3.3.

**The rows' channels vary under their named mutants.**

* `kbcq * pre` = 0x1 on base: one reply is queued, and Wpure pops it.
* `iirw ctl` / `iir ctl` = 0x2: TXRDY is armed, and Wpure clears it.
* No vacuous row was found.

### The complete (arm x width-kind x lane) enumeration of the forward-count class

"Observable" means observable on alphabook1 as the probe configures it.  "Rowed" means rowed in the 111-row instrument.

| arm | width-kind | lane | observable? | rowed? | cheapest channel (measured where noted) |
|---|---|---|---|---|---|
| write (phantom read after store) | direct 1/2/4/8 | 0 | yes | **yes** (`kbcq b/w/l/q`), ZERO data only | also stub 0x68 (E) |
| write | direct | 1 | **yes** | no, disclosed | stub 0x61 (E); 8253 0x41 (F); REG C (G) |
| write | direct | 2 | yes | **yes** (`iir`/`iirw` x4), ZERO data only | also stub 0x62 (E) |
| write | direct | 3 | **yes** | no, disclosed with a false warrant | stub 0x63 (E) |
| write | head 1..7 | 3 | no | -- | **EQUIVALENT** (0x3ff/0x2ff SCR) |
| write | **tail 3/5/6/7** (tails 1/2/4 are the direct lane-0 cells) | 0 | **yes** | **no -- UNCLASSIFIED** (not caught, not equivalent, not disclosed) | 8042 with one reply queued, then 0xd1, then a split store (C) |
| read (duplicated forward) | direct | 0 | **yes** | **no -- UNCLASSIFIED** | 8042 with TWO replies queued (D); stub 0x68 (E-load) |
| read | direct | 1 | **yes** | no, unclassified | stub 0x61 (E-load, via R2w) |
| read | direct | 2 | yes | **len 1 only** (`iir lca rd`); **2/4/8 NOT** | IIR (B); stub 0x62 |
| read | direct | 3 | **yes** | no, unclassified | stub 0x63 (E-load, via R2w) |
| read | head 1..7 | 3 | no | -- | **EQUIVALENT** (SCR) |
| read | **tail 3/5/6/7** | 0 | **yes** | **no -- UNCLASSIFIED** | 8042 with two replies (D, measured at tail 6) |

**Cheapest whole-class closure: one diff, new sessions only, so no earlier kill moves.**

* **Direct cells, 4 lanes x 4 widths x 2 arms = 32 cells.**
  * Use the stub at 0x68 / 0x61 / 0x62 / 0x63.
  * Each row is: flat read, then ONE lca access, then flat read; want `(a ^ b) & 0x10 == 0`.
  * Add one liveness row per session: two plain flat reads, want a flip of 0x10.
  * It needs no arming, does not care about the data value, and needs no queue.  About four sessions.
* **Tail cells, 4 widths x 2 arms = 8 cells.**
  * These are the C and D channels: 8042 queue plus a split access at SP(0x5f) + 0x1f / 0x1e / 0x1d / 0x1b.
  * Tails start at 0x60, the data port, not in the stub's range.  0x40 (8253) is the alternative.
* **Heads.**  Disclose EQUIVALENT with the mapped-port list: 0x3ff and 0x2ff SCR, and 0x60-0x6f contains no 0x1f-mod-0x20 port.
* **Store a NONZERO byte in the stub rows.**  The stub ignores store data.  The existing zero-store `iir`/`kbcq` rows then keep dataB red, and the nonzero stub stores red dataA.  So the data axis is closed for free.
* **Caution, and it is why the liveness row is mandatory.**
  * The stub is an emulator TODO.  If port 0x61 is ever implemented properly, every stub row goes vacuous silently, because `a == b` whatever the access count.
  * The liveness row reds when that happens.
  * The 8253 route (lanes 0-2) is architectural and survives such a change, but it cannot reach lane 3.  On this machine only the stub reaches lane 3.

---

## Q2 -- FLOOR GAP

**The GAP is R2w.  This is my reading of where it sits.**

**The contract names it.**

* Since repair 4 the header's CONTRACT paragraph ("the detector is DESIGNED to catch ...") ends with "And the read arm's forward DUPLICATED (RD2 ... rowed since repair 4 at IIR, 4j `iirr')", with **no width or lane scope**.
* POSTTABLE 5's FLOOR line states it as "the read-arm mirror RD2 at lane 2".
* R2w is at lane 2, and it escapes at widths 2, 4 and 8.

**This is the exact shape the flagship ruled on in closing pass 3.**

* FABLE_C3_RULING part B: *"A detector that catches a contract-named edit only at the widths its rows happen to use has not caught the edit"*.
* W4 then; R2w now.
* That makes it a wrong record (L4) at minimum, fixed in-round, and L2-in-spirit if the claim stays unscoped.

**It is the most realistic escape on the record.**

* The fix's own comment names "the 21066's own len 4/8 accesses".
* The 21066 is an EV4-core part.  BWX arrived later, with EV56, so its own OS drivers read ISA bytes through sparse space with LDL.
* R2w's LDL is exactly that access.  The single RD2 row uses LDBU, an instruction the modelled CPU does not have.

**This is the third consecutive pass to breach the forward-count class.**

* Closing pass 2: the write fallthrough, unconditioned.
* Closing pass 3: the write fallthrough gated on width or lane, plus RD2.
* Closing pass 4: the read side gated on width or lane, the tail write cells, and lane-3 direct.
* Each repair rowed the cells that had been measured, and the next pass found the cells beside them.
* The repair-chain amendment applies with full force: **the next repair owes the CLASS closure** (the Q1 table) in one diff.
* The 32 + 8 cell space above is finite, derived from the handler's arms and `len`/lane, so the next closing pass can verify it rather than hunt it.

**dataA: my reading is that it is NOT floor, and it costs nothing to close anyway.**

* The write body tests no bit of the written value.  It forwards `data[ofs]`.
* By the pass-11 rule ("the bits of the single value being written are single-operand MARGINALS, not floor") and the generating-set amendment ("every idata bit the guarded body TESTS"), the value axis of this arm is clause-(e) debt.
* It is guest-visible and realistic: a com driver writes FCR nonzero (for example 0x07) at open, and under dataA a pending TX interrupt is lost (A: IIR & 3 0x2 -> 0x1).
* The header's data-class disclosure names *mis-decode* keyed on data.  **It should also name the fallthrough keyed on data**, or the class-closure repair should close it for free with nonzero stub stores (above).
* I recommend the free closure.

---

## PANEL MUTANTS (as the coordinator asked)

| panel cell | seats | built as | 111-row | guest-visible discriminator |
|---|---|---|---|---|
| R2w | kimi-k3, grok, codex, kimi CLI | `if (len != 1)` + second forward | **111/111** | arm TXRDY, then LDWU / LDL / LDQ SP(0x3fa): lane & 3 **0x2 -> 0x1** at all three widths (raw 0x2 -> 0x1, 0x20000 -> 0x10000, 0x20000 -> 0x10000) |
| R2w (`len == 2` form) | same | R2w2 | **111/111** | LDWU **0x2 -> 0x1**; LDL and LDQ unchanged |
| WT6 | glm, kimi-k3, codex, kimi CLI | `if (len != 6) return 1;` | **111/111** | flat self-test (0x55 queued), then 0xd1, then an unaligned STQ at SP(0x5f) + 0x1e (2-byte head at 0x5f, 6-byte tail at 0x60): flat status DIB **1 -> 0** |
| WT 3/5/7 | same | WTsplit (3, 5, 6, 7 together) | **111/111** | the same, at offsets 0x1b / 0x1d / 0x1f (tails 3 / 5 / 7): each DIB **1 -> 0** |

**Is RD2 at LANE 0 observable?**

* **Yes**, with two replies queued: a duplicated 0x60 read pops both.
* Measured on RD2L0 at (1,0), at (8,0), and at the split-TAIL READ cell (LDQ tail 6): DIB after, **1 -> 0**, value unchanged.
* So the `tailr` read cells are observable too.
* The stub at 0x68 also shows it (E-load flip).

---

## Q3 -- WRONG STATEMENTS

1. **POSTTABLE 5, FLOOR line.**  "the read-arm mirror RD2 at lane 2" is false at len 2, 4 and 8.  R2w and R2w2 each score 111/111.
2. **Header CONTRACT, the RD2 sentence.**  It is unscoped, while its only row is (1,2).  This is the L4 above.
3. **Header, lane-3-direct warrant AS CORRECTED at 00:19.**
   * The corrected text reads "no read-side-effect port is present on this probe's machine".
   * That is false: 0x63, 0x67, 0x6b and 0x6f (the 8042 stub's access counter) are present.
   * Measured: L3gate, E tog63 store flip 0x10.
   * The correction fixed the wdc half correctly (wdc needs an IDE image), then made a new universal claim that is also false.
4. **Header, scoped x_wfallthru entry.**
   * It classifies direct widths and heads, and **says nothing about the tail cells 3, 5, 6 and 7**.
   * Those cells are in the header's own CELL SPACE, and they are neither caught, equivalent nor disclosed.
   * WT6 and WTsplit each score 111/111 and are guest-visible.
   * The same holds for RD2 at lanes 0, 1 and 3, and at tails: named nowhere.
5. **The coordinator's lane-1 correction** (0x61 / 0x41 / 0x71) is **verified**: L1gate moves E tog61, F and G exactly.
6. **Heads EQUIVALENT is verified**: the mapped-port derivation above.  **The `kbcq` and `iir` channel premises are verified** (Q1).

I found no error in the fix itself or in its comment.  Every seat since pass 2 has found the fix right, and nothing I built touches the fix's own predicates.

**Not checked:**

* 8253 counter 0 as a tail channel.
* RD2 gated to lane 1 or lane 3 alone.  It is covered by construction through R2w's E-load flips.
* The lpt read arm.
* Behaviour with IDE disk images attached.

---

## CLONE

* `/tmp/gxopus530c4` was verified restored (`logs/cleanup.out`):
  * no `.MUTANT`;
  * `dev_lca.c` cmp-clean against GXEMUL-SEC;
  * `gxemul -nt dev_lca.c`;
  * binary == base.
* It was then **DELETED**, together with `/tmp/gxopus530c4_bins`.
* GXEMUL-SEC `src/devices/dev_lca.c` is unchanged: md5 `8084ff07` before and after.
* No process of mine is running.  Driver B was stopped by PID, and checked with `ps` afterwards.
* I did not touch `/tmp/gxopuscrime`, `/tmp/gxcrime529i_bins` or `/tmp/gxlca530`.
