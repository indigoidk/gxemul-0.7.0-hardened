# #530 `lcaisalane` CLOSING PASS 5 -- the Opus MEASURING seat (SECOND instance, finishing the walled seat's work)

**VERDICT: `ENUMERATION WRONG` -- the forward-count class is EIGHT cells ({write arm, read arm} x {DROP, SWAP,
DUPLICATE, ADD-OTHER}); the contract enumerates TWO of them, and the repair-5 design additionally picked ONE-SHOT
LATCHES as the lane-1/lane-2 channels, which cannot carry a COUNT class by construction. FIVE mutants score 185/185
and THREE more are carried by the emulator-TODO stub ALONE at lanes 0-2, in direct breach of the ruling's RB1.
Repair 6 owes the eight-cell closure in one diff. The FIX is correct and untouched.**

```
LCA530_C5_OPUS_20260915
# CHECKPOINT -- 2026-09-15 ~07:xx   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED
```

Evidence basis: my predecessor's 11 probe legs + 14 discriminator legs (re-verified here), plus **21 new legs I ran
this session** (16 prototype-row legs, 5 shipped-185-row legs, 6 new binaries). Every log ends its completion
sentinel. Predictions were written before every run; `logs2/PREDICT3.out` (11:13), `PREDICT4.out` (12:43),
`PREDICT5.out` (12:44) and `PREDICT6.out` (14:14) all predate the builds and runs they govern. **13 of 13 numeric
predictions EXACT, on score AND on red set**, plus every family prediction and PREDICT6's row-level discriminator;
the remaining legs were predicted by FAMILY only, deliberately, because two of them leave `byte` uninitialised and a
number there would have been a guess in a measured column.

---

## 1. VERIFICATION OF `MAINLOOP_HARVEST.md` -- four corrections, one of them material

I checked every row against the raw logs rather than taking the harvest on trust.

**All eleven scores are correct** and every log ends `LCAISALANE_DONE`: base 185, WWtail 185, WW6 185, WWall 169,
RD2post 161, RD2z 185, cdxZL3 185, dNZtail 185, RWtail 183, W23 184, nox 181. The mutant diffs in `logs/*.diff`
match the harvest's descriptions of them exactly. `check_pred_batch1.out` records `exact=8 differs=0`.

### C1 -- the WWall row UNDERSTATES the breach, and the seat's own PREDICT.out says so

The harvest reads *"WWall 169/185 -- the UNGATED store duplicate: caught, by the stub rows (16 of them)."* True, and
materially incomplete: **the 16 stub rows are the ONLY reds.** Not one architectural row moves -- `kbcq * dib`,
`iir st*`, `cmos w*`, `tailq w t*` are all green. So for the store-duplicate form the stub is the SOLE CARRIER at
lanes 0, 1 AND 2 -- **twelve cells**, a strictly wider RB1 breach than the RD2post one the harvest does flag.

The seat had already found this. `logs/PREDICT.out`, written 07:44 before any build, predicts
*"stub0-3 w1/w2/w4/w8 (16) ONLY -- the stub counter is direction-blind; kbcq (ACK queued, DIB stays 1), iir (FCR
twice), cmos w (REG C set twice) cannot see a doubled store."* **The finding was made and the harvest dropped it.**

### C2 -- "after building and running every leg below" is not right, and the error is the interesting kind

The seat walled at ~09:2x. Batch 1's driver finished at **09:22:59**; batch B's probe legs landed at **09:42 and
10:02**, and **all nine `discB_*.out` legs between 10:07 and 10:28** -- the driver was backgrounded and ran on
unattended. So the seat *launched* every leg and *read* eight of the eleven probe legs. **It never saw WW6,
RD2post or cdxZL3, and it never saw ANY of the 8253 measurement.**

That matters because **the 8253 channel -- the open question I was sent to measure -- was already designed,
predicted and RUN by my predecessor**, and its output has been sitting unread on disk for a day. `PREDICT2.out`
contains the full design and a correct prediction of every leg. This is the UNREAD REVIEW class inside a seat's own
artifacts, and it cost this round a day.

### C3 -- the harvest's closing paragraph is right and short by one

*"The forward-count class as enumerated by repair 5 has only two arms ...; the STORE's own duplicate is a third."*
Correct as far as it goes. The space is **eight** cells (section 3), and the harvest's "third" is one of the six
unnamed.

### C4 -- two small omissions, stated so the record is complete

`Wpure` was built and has **no probe leg** -- `PREDICT2.out` says so explicitly ("disc-only subject for the 8253
channel; no probe leg") and table 6 already scored that mutant at 153/185. Not a gap. The harvest's table also
omits the `restored`/`restoredB` control binaries, which are byte-identical to `base` as their drivers recorded.

**Everything else in the harvest I could check is accurate**, including the RD2post reading: its 24 reds are
`rdq r1-r8` (4) + `stub0-3 r1-r8` (16) + `tailq r t7/t6/t5/t3` (4), with **no `cmos r*` and no `iirr`/`iirr2`**,
so the stub is indeed the sole carrier at lanes 1 and 2 for that form -- exactly codex's prediction.

---

## 2. THE OPEN QUESTION, MEASURED: the 8253 counters as the forward-count channel

I verified the mechanism in source first (`src/devices/dev_8253.c`, read, not taken from the brief):

* `:143-147` ports 0x40/0x41/0x42 are `relative_addr` 0/1/2 = **lanes 0/1/2**; `:289` port 0x43 =
  `I8253_TIMER_MODE` = **lane 3**.
* `:280-285` the flip-flop advance sits INSIDE the counter case and fires on **every** counter access, read and
  write -- but **only while `(mode_byte & 0x30) == I8253_TIMER_16BIT`**. `wr_msb` toggles on writes, `rd_msb` on
  reads: **separate per direction**. That separation is load-bearing (see the RWall result).
* `:320-321` a control word **rewinds both flip-flops for that counter**, which is what lets every phase be
  self-starting.
* `:289-348` lane 3: a READ of the mode port returns `mode_byte` with **no side effect and no flip-flop advance**;
  a repeated identical control-word WRITE is idempotent.

I then built a **prototype 150-row session** (`instrument2/pitrows530c5.py`, a COPY -- the shipped probe was never
touched and `cmp`s clean against it throughout) with four phase shapes: `live` (the control), `PS X` (store
parity), `PL L` (load parity) and `PW` (a load followed by a store, which is the only shape that sees an added
WRITE). Counters 0/1/2 at widths 1/2/4/8, tails 7/6/5/3 at port 0x40, each at data 0x00 and 0x5a.

### The measured table -- 15 legs, one instrument, frozen before the comparison

| leg | class cell | shipped 185-row probe | **8253 prototype** | predicted | pit red families |
|---|---|---|---|---|---|
| base | -- | 185/185 | **150/150** | 150 ✓ | none |
| nox (`dev_pckbc` stub killed) | control | 181/185 | **150/150** | 150 ✓ | none -- **independent of the stub** |
| noff (`dev_8253` flip-flop frozen) | control | -- | **77/150** | 77 ✓ | `live1` x4 first, then 69 more |
| Wpure | write x ADD | 153/185 (table 6) | **86/150** | 86 ✓ | all 64 PS |
| WWall | write x DUP | **169/185, STUB-ONLY** | **86/150** | 86 ✓ | all 64 PS -- set IDENTICAL to Wpure |
| WWtail | write x DUP (tails) | **185/185 ESCAPE** | **134/150** | 134 ✓ | 16 tail PS |
| WW6 | write x DUP (len 6) | **185/185 ESCAPE** | **146/150** | 146 ✓ | 4, tail 6 only |
| dNZtail | write x ADD, data-gated | **185/185 ESCAPE** | **142/150** | 142 ✓ | 8 -- X=0x5a RED, X=0x00 green, same cell |
| RD2post | read x DUP, after the loop | **161/185, lanes 1-2 STUB-ONLY** | **108/150** | 108 ✓ | 32 `pl_r1` + 10 `pw` |
| RD2z | read x DUP, data-gated | **185/185 ESCAPE** | **118/150** | 118 ✓ | 32 at L=0x00 (`dlv` AND `r1`) |
| RWall | read x ADD | **167/185, STUB-ONLY** | **140/150** | 140 ✓ | 10 `pw` ONLY |
| RWtail | read x ADD (tails) | 183/185 (2 of 4 tails) | **146/150** | 146 ✓ | 4 `pw` at tails |
| cdxZL3 | write x ADD, lane 3 x zero | **185/185 ESCAPE** | **150/150** | 150 ✓ | **none -- THE LIMIT** |
| WXR | write x SWAP | 140/185 | **118/150** | family ✓ | 32 `ps_r1` |
| RXW | read x SWAP | 143/185 | **97/150** | family ✓ | 48 `pl` + 5 `pw` (`r1` halves only) |
| Wdrop | write x DROP | 136/185 | -- | family ✓ | -- |
| Rdrop | read x DROP | 127/185 | **92/150** | family ✓ | 48 `pl` + **10 `pw` (BOTH halves)** |

Logs: `logs2/pit_*.out`, `logs2/probe185_*.raw` (every one ends `PITROWS_DONE` / `LCAISALANE_DONE`).
Predictions: `logs2/PREDICT3.out`, `PREDICT4.out`, `PREDICT5.out`, `PREDICT6.out`, all written before their runs.

### Answering the question exactly as asked

**Does an 8253 row RED on each named escape while staying green on base? YES on five of six, NO on the sixth --
and the NO is structural, not fixable.**

| named mutant | 8253 row that reds | cell it carries |
|---|---|---|
| **WWtail** | `pitT ps{5a,00} t{7,6,5,3}` | tails x both data, store side |
| **WW6** | `pitT ps{5a,00} t6` | one tail cell -- the row is width-exact |
| **RD2post** | `pit{0,1,2} pl*_r1` and `pitT pl*_r1`, plus every `pw` | **lanes 1 and 2**, the cells the stub alone held |
| **RD2z** | `pit{0,1,2} pl00_*` and `pitT pl00_*`, **including `dlv`** | the zero-delivered-byte data cell, all lanes |
| **dNZtail** | `pitT ps5a t*` only; `ps00` stays green | the tail x NONZERO data cell, per cell |
| **cdxZL3** | **NONE. 150/150.** | **lane 3 is unreachable on this channel** |

**Cells the 8253 CAN carry:** lanes 0, 1 and 2 at all four direct widths, and the split tails 3/5/6/7 at lane 0,
on BOTH arms, at BOTH data values, for **all four** mutation shapes (drop, swap, duplicate, add-other).

**Cells it CANNOT carry, and why:**

1. **LANE 3 -- in either direction, permanently.** Port 0x43 is the mode register: a read returns `mode_byte` with
   no side effect and does not advance any flip-flop (the advance is inside the counter case); a repeated control
   word is idempotent. Measured, not reasoned: `cdxZL3` -- whose entire edit is at lane 3 -- scores **150/150**,
   and `W23` (x_wfallthru at (2,3)) is likewise invisible to it. **`stub3` remains lane 3's sole carrier, which is
   what RB1 already licenses.**
2. **Split HEADS.** A head lands at a port 0x1f mod 0x20, which is lane 3 and is not an 8253 port. Unchanged --
   the contract's EQUIVALENT derivation still governs.
3. **It cannot distinguish a doubled STORE from a phantom READ.** `WWall` and `Wpure` produce **byte-identical red
   sets** (verified by `diff`, not by score). Both are in the class so detection is unaffected, but the contract
   must not claim the rows identify which form occurred.
4. **A read-parity row is BLIND to an added WRITE.** `rd_msb` and `wr_msb` are separate, and a write-back rewrites
   the same half with the same value. Measured: `RWall` reds **zero** `pl` rows and exactly the 10 `pw` rows. Any
   row for the read x ADD cell must force a LATER STORE, which is what the `PW` shape does.

### The mandatory control/liveness row -- and it is stronger than the stub's

The `live` pair: after a control word, a flat LSB store of `0x34` and a flat MSB store of `0x12` must read back
**`0x34` then `0x12`**. One row per session (four sessions), and it is three controls in one:

* **LIVENESS** -- the port answers at all (an unmapped port returns 0 twice);
* **DEVICE SIGNATURE** -- two DIFFERENT bytes in a FIXED order from ONE address. RAM returns the same byte twice;
  the ns16550 scratch register returns what was written. **Only a 16-bit read/write flip-flop alternates halves.**
  This is a genuine device signature, where the stub's is a fabricated constant (`odata = 0x21`) with a parity bit;
* **ORACLE LIVENESS** -- if the mechanism goes away the row REDS.

I built that negative control rather than predicting it. **`noff`** (`dev_8253.c:282/:284`, `^= 1` -> `^= 0`, the
flip-flops frozen, `dev_lca.c` untouched) scores **77/150**, and `live1` is red in **all four** sessions and is
the FIRST row of each.

> **And the DIRECTION of that failure is the argument for this channel over the stub.** `nox` -- the stub's TODO
> "implemented" -- leaves every stub access row GREEN and reds only the four liveness rows: the oracle vanishes
> **silently** and the liveness row is the only thing standing between that and a vacuous detector. `noff` makes
> **73 of 150 rows RED**. The 8253 flip-flop is modelled architecture with a cited source in the file itself
> (i8254 Figure 7, `dev_8253.c:314-319`, round `#440`); there is no "implemented later" state that greens its rows.
> **The stub needs its liveness row to avoid going quietly vacuous; the 8253 cannot go quietly vacuous.**

Two further constructional requirements, both measured or read:

* **Every phase must open with a control word** (`:320-321` rewinds the pair), or phases leak parity into each other.
* **COST, measured not predicted** (the prototype counts it and prints it): a 16-bit MSB write to counters 1 and 2
  emits an UNLATCHED `fatal()` -- `dev_8253.c:198` `TODO: DMA refresh?` and `:200` `TODO: 8253 tone generation?`.
  **18 of each per session, 36 per run.** It does not affect any row (the probe parses `print` output) but it is
  real log noise on a guest-drivable path, and it is a `floodclass` instance worth filing separately.
* An MSB write to counter **0** instead calls `timer_add`/`timer_update_frequency` (`:191-196`) with
  `hz = 1193182/counter`. Keep the programmed counter large -- the prototype's values give ~250 Hz. A row that
  programs a small counter would install a high-frequency host timer.

### WHY the architectural rows failed, which is the finding under the finding

This is not bad luck in choosing channels. I read the two devices repair 5 picked for lanes 1 and 2:

* **CMOS REG C (lane 1, port 0x71)** -- `dev_mc146818.c:565`, the read does `d->reg[MC_REGC*4] = 0x00;`. A second
  read finds it already zero. The write path (`:468-469`) is a plain assignment: writing the same byte twice is
  idempotent.
* **ns16550 IIR (lane 2, port 0x3fa)** -- `dev_ns16550.c:211-213`, the read clears `IIR_TXRDY` once. The write path
  (`:206-209`) is `d->fcr = idata;`, a plain assignment.

> **Both are ONE-SHOT LATCHES. A latch distinguishes ZERO accesses from AT LEAST ONE. It can never distinguish ONE
> from TWO -- which is exactly and only what a forward-COUNT class asks.** Every count mutant that leaves the first
> access intact and adds a second is invisible to them *by construction*, and that is the mechanical cause of all
> three measured RB1 breaches. The stub was carrying those cells alone because the stub is an ALTERNATOR and the
> channels beside it were latches.

That also shows the shape a replacement must have, and it is checkable by reading: **a forward-COUNT row needs a
COUNTER or an ALTERNATOR, never a LATCH.** On this machine those are the 8253 flip-flops (lanes 0/1/2 + tails), the
8042 reply queue (lane 0 only, ports 0x60/0x64), and the pckbc stub (all lanes, but an emulator TODO).

**There is a second, independent carrier for lane 0 and the tails that needs no new device, and my predecessor
measured it**: `logs/disc_*.out`'s `kbcmd` phase issues an 8042 command that generates one ACK, pops one reply, and
asserts the queue is then EMPTY. Base gives `DIB=1, pop=0xfa, DIB=0`; **WWall and WWtail give `DIB=1` after the pop**
(two ACKs queued) and **dNZtail gives `DIB=0` before it** (the phantom read popped it). That is the same 8042 the
`tailq_w` rows already use -- **with a different oracle.** `tailq_w`'s oracle is *"the queued reply SURVIVES the
store"*, which a doubled store cannot move; `kbcmd`'s is *"the command produced exactly one reply"*, which it can.

---

## 3. THE CLASS: eight cells, not two, three or six

Derived from the handler, which makes **exactly one** 1-byte bus forward per access -- `writeflag` on the write arm,
`MEM_READ` on the read arm. One-edit perturbations of that one-element sequence are DROP (length 0), SWAP (length 1,
direction flipped), DUPLICATE (length 2, same direction), ADD-OTHER (length 2, mixed), over two arms.

| # | arm | shape | one-edit form | named as | shipped-probe score |
|---|---|---|---|---|---|
| 1 | write | DROP | `return 1;` | `Wdrop` | 136/185 caught |
| 2 | write | SWAP | `writeflag` -> `MEM_READ` (one token) | `WXR` | 140/185 caught |
| 3 | write | DUP | a second store forward | `WWall`/`WWtail`/`WW6` | **169 stub-only / 185 / 185** |
| 4 | write | ADD | drop the `return` (x_wfallthru) | `Wpure`/`W23`/`cdxZL3`/`dNZtail` | 153 / 184 / **185** / **185** |
| 5 | read | DROP | delete the read forward | `Rdrop` | 127/185 caught |
| 6 | read | SWAP | `MEM_READ` -> `MEM_WRITE` (one token) | `RXW` | 143/185 caught |
| 7 | read | DUP | a second read forward | `RD2`/`R2w`/`RD2post`/`RD2z` | 153 / 160 / **161 stub-only** / **185** |
| 8 | read | ADD | an added `MEM_WRITE` of the fetched byte | `RWall`/`RWtail` | **167 stub-only** / 183 |

**The contract names cells 4 and 7 only.** Cells 1, 2, 5, 6 were never built by anyone until this session; cell 3
was found by the c5 panel (glm, kimi-k3, kimi CLI) and cell 8 by me.

### What the four newly-built cells settle -- and neither of the DROP/SWAP pairs escapes

The coordinator asked me not to take the converse on trust either. Measured:

* **`Wdrop` 136/185 and `Rdrop` 127/185 -- NOT escapes.** The guess that the DROP pair is already discharged is
  correct. (`Rdrop` also *builds*: the compiler accepts the uninitialised `byte`, so the cell is reachable by a
  one-edit mutant.)
* **`WXR` 140/185 and `RXW` 143/185 -- NOT escapes.**
* **`WXR` and `Wdrop` are distinguished by 28 rows moving in OPPOSITE directions**, exactly as PREDICT5 said:

  | family | `Wdrop` (no forward) | `WXR` (one READ forward) |
  |---|---|---|
  | `stub<l> w<n>` | **16 RED** -- the port is never touched | **0** -- one access still happens |
  | `kbcq * dib` | 0 -- the reply survives | **4 RED** -- the read pops it |
  | `tailq w t*` | 0 | **4 RED** |
  | `iir st*` | 0 -- "TXRDY survives" is true of a lost store too | **4 RED** -- the read clears TXRDY |
  | `cmos w*` / `tailw t*` | 4 / 4 RED | 4 / 4 RED |

  So the coordinator's claim is confirmed by measurement: **a row that only checks "the store landed" cannot
  separate DROP from SWAP; the side-effect rows can, and they separate it in both directions.**

### The read arm is ASYMMETRIC, and today's coverage of its SWAP cell is subsumption -- measured, then discharged

On the shipped detector **`RXW`'s red ROW SET is a STRICT SUBSET of `Rdrop`'s**: 42 reds against 58, the difference
being exactly the sixteen `stub<l> r<n>` rows. (I first compared including the GOT value and got one spurious
"RXW-unique" entry -- the `live` row, red in both, differing only in stack residue, 0xff vs 0x00. Corrected by
keying on the row name.) The mechanism is the stub's direction-blindness: under `RXW` the read arm still makes ONE
forward, so the counter still advances and the stub rows stay green; under `Rdrop` nothing happens at all.

> **So on TODAY'S rows the read-arm SWAP is covered only BY SUBSUMPTION under the read-arm DROP, and a future
> repair that closed the drop cell and reasoned "the swap is covered" would be making exactly the inference this
> pass exists to refuse.** A contract sentence for today's row set must say *subsumption* and name the fact.

**That caveat is dischargeable, and I measured it rather than leaving it standing.** `PREDICT6.out` (14:14) derived
one row as the discriminator, before the run: the `PW` pair's second half, RED under `Rdrop` and GREEN under `RXW`,
because `Rdrop` moves NEITHER flip-flop while `RXW` moves the WRITE one, so the later flat store of `0x77` lands in
a different half.

| row | `RXW` | `Rdrop` |
|---|---|---|
| `pit0/1/2 pw r2`, `pitT pw t6B`, `pitT pw t3B` | **green** (0x77) | **RED** (0x12) |

Five rows, all five as predicted; totals `RXW` 97/150 against `Rdrop` 92/150. **Once repair 6 ships the 8253 rows
the two read-arm cells are INDEPENDENTLY PINNED and the contract may say so. It may not say so about the row set
that exists today.**

* **The `RXW` result is the one worth carrying, and it is not the score.** All 42 of its reds are read-VALUE rows
  (`live`, `ofs* zero/wide`, `r* byte/lane`, `ld4`/`ld8`, `h* ldq`, `tailr`, `iir lca rd*`, `cmos r*`).
  **Zero stub rows red** -- the access COUNT is still one. So the detector catches `RXW` for the **missing read**,
  and **nothing whatever observes the acquired WRITE.** The proof is independent and already in the table: put the
  read back and keep the write (`RWall`) and the detector falls to **167/185, stub and two `tailr` rows only.**
  The header's sentence *"a DIRECTION swap ... is a different class, caught by the value rows"* is therefore true
  about detection and false about what is detected.

---

## 4. VERDICT AND WHAT REPAIR 6 OWES

**`ENUMERATION WRONG`.** Pass 5 does not close. This is the FOURTH consecutive pass in which the forward-count class
escapes, and by the repair-chain amendment the next repair owes the CLASS CLOSURE in ONE diff, enumerated from the
function's own inputs, with the contract naming which cells are covered and which are deliberately not.

**GRADE.** Following the flagship ruling's own correction at B1-B3: these are ROUTING edits and weaken no predicate
the fix depends on, so they are **not clause-(d) floor by the letter**. They are **L4** (the contract claims a cell
space "rowed WHOLE" and "closed by enumeration" that is open in six of eight cells and in three data joints) **plus
the class-closure obligation**. In-round either way.

### 4a. The class definition -- yes, it grows, and by five not one

`{write arm, read arm} x {DROP, SWAP, DUPLICATE, ADD-OTHER}` = eight cells, derived above from the single forward
each arm emits. Write it into the contract as the *derivation*, not as a list, so a future pass re-derives it.

### 4b. The cells

The existing (arm x width-kind x lane) table, crossed with **two axes the contract does not have**:

* **SHAPE** -- the four perturbations above. Four of the eight cells are currently unrowed as such.
* **DATA {zero, nonzero}, PER CELL.** The contract's *"the zero/nonzero partition is rowed on both sides"* is a
  MARGINAL over all cells, and three joints are empty and measured: lane 3 x zero store (`cdxZL3` 185/185),
  tail x nonzero store (`dNZtail` 185/185), any lane x zero DELIVERED byte (`RD2z` 185/185). Per the carrier's
  JOINT CELLS clause this is the cross-product of partitions the body distinguishes; per RB4 the handler tests no
  bit of the value, so the data axis is clause-(e) debt and NOT floor -- **but the contract CLAIMS it closed, and
  that claim is the L4.** Row it or correct the sentence; do not leave both.
* Heads stay EQUIVALENT (unchanged, and re-verified: no 8253 port is 0x1f mod 0x20).

### 4c. The channels -- and the rule that chooses them

> **A forward-COUNT row needs a COUNTER or an ALTERNATOR. A one-shot LATCH cannot carry this class.**

| lane / kind | carrier repair 6 should use | status |
|---|---|---|
| 0 direct | 8253 counter 0 at 0x40 **and** the 8042 `kbcmd` oracle at 0x60 | both MEASURED |
| 1 direct | **8253 counter 1 at 0x41** -- the only architectural alternator at lane 1 | MEASURED |
| 2 direct | **8253 counter 2 at 0x42** -- ditto | MEASURED |
| 3 direct | `stub3` + its liveness row, unchanged (RB1 already licenses it) | unchanged |
| tails 3/5/6/7 | 8253 counter 0 at 0x40 (a tail port, 0 mod 0x20) **and** `kbcmd` | both MEASURED |
| heads 1-7 | EQUIVALENT | unchanged |

Keep `cmos` and `iirr`/`iirr2` -- they are good VALUE rows and they carry the position rule. They are simply not
count rows, and the contract should say which is which.

### 4d. The rows

1. **Four new sessions** (`pit0`, `pit1`, `pit2`, `pitT`), the prototype re-typed into the shipped probe. Per
   session: `alive`; the `live1`/`live2` pair (the mandatory control, liveness + device signature + oracle
   liveness); `PS` at 4 widths x 2 data values (store side -- cells 3 and 4, and `WXR` too); `PL` at 4 widths x 2
   data values with **both** a delivered row and an **after-the-access readback** row (read side -- cell 7 in both
   positions, and `RD2z`); **`PW`, and KEEP BOTH HALVES OF THE PAIR** -- `r1` is the only shape that sees an added
   write (cell 8), and `r2` is what separates cell 5 from cell 6 (measured above; a single-row `PW` would leave the
   read-arm swap on subsumption). The tail session repeats it at tails 7/6/5/3. That is **150 rows measured green
   on base and red on every escape above.**
2. **One `stub3` store phase that stores ZERO** -- closes the lane-3 x zero-data joint (`cdxZL3`) for one row.
3. **A `kbcmd`-shaped oracle** on the existing 8042 sessions (command -> one ACK -> pop -> assert empty). Cheap,
   needs no new device, and gives lane 0 and the tails a hardware-contract channel beside the timer's flip-flop.
4. **Contract rewrites**: the eight-cell derivation; the per-cell data statement; that the store-side row is
   direction-blind (`WWall` == `Wpure` row for row); that a read-parity row is blind to an added write; that the
   8253 cannot reach lane 3 in either direction, **measured**, with `cdxZL3` 150/150 cited; and the 36-`fatal()`
   cost with its two source lines.

**A general rule this pass earned, worth putting in the contract because it is checkable by reading:** *a row that
inspects only the value an access DELIVERED cannot see a second access; a row must read the channel AFTER the access
as well.* Every row that caught `RD2post` (`rdq`, `tailq r`, the stub, my `pl_r1`) reads the port again afterwards;
every row that missed it (`cmos r*`, `iirr2`) inspects only the delivered register.

**RE-TYPED ROWS ARE MEASURED, NOT ASSUMED** (the ruling's RA2). My 150 rows ran in a prototype; repair 6 must re-run
them in the shipped probe as kill table 7, on base plus the thirteen mutants above.

### 4e. What I did not reach

* `W23` was dropped from the prototype run to keep to two lanes; `cdxZL3` already measures the lane-3 limit and
  `W23`'s shipped score (184/185, `stub3 w2`) was already known. I did not re-measure it on the 8253 rows.
* **I did not run `Wdrop` through the prototype rows.** `Rdrop` I did run, because the read-arm subsumption
  question turned on it. The write-arm analogue -- whether the 8253 rows separate `Wdrop` from `WXR` independently
  -- is therefore UNMEASURED, and I will not infer it from the write-arm result on the shipped rows. It is one
  13-minute leg and repair 6 should take it.
* I did not build the 8042 `kbcmd` rows as ROWS; I am relying on my predecessor's discriminator measurement of that
  channel, which is a measurement of the channel and not of a row with a want.

---

## 5. WRONG STATEMENTS

Citations are verified-unique grep anchors in `GXEMUL-SEC/regress/lca_isalane_probe.py`, with line numbers as of
this reading.

1. **`in either form, unconditioned or gated on the width, the lane or the data`** (`:101`) and
   **`CLOSED BY ENUMERATION SINCE REPAIR 5`** (`:100`) -- **FALSE.** "Either form" names two of eight cells.
   Measured: `WWtail` and `WW6` (write x DUP) both 185/185.
2. **`never as the sole carrier`** -- **MEASURED FALSE, THREE TIMES, and it occurs at TWO SITES** (`:106` and
   `:864`; the grep-for-siblings rule applies). `WWall` 169/185 is 16 stub rows and nothing else (lanes 0,1,2,3);
   `RWall` 167/185 is 16 stub + 2 `tailr` (every direct lane); `RD2post` 161/185 has no architectural carrier at
   lanes 1 or 2. This is a direct breach of the ruling's RB1, which the row set was built to satisfy.
3. **`every one rowed`** (`:102`, "DIRECT cells, 4 lanes x widths 1/2/4/8 x both arms") -- **FALSE** for cells 3
   and 8: at lanes 0/1/2 those direct cells are rowed by the stub alone, which the same header forbids.
4. **`the zero/nonzero partition is rowed on both sides`** (`:112`) -- **FALSE as a per-cell claim**; it is a
   marginal. Three joints measured empty: `cdxZL3`, `dNZtail`, `RD2z`, all 185/185.
5. **`a DIRECTION swap`** (`:117`) *"...is a different class, caught by the value rows"* -- **half true, and the
   half that is false is the one that matters.** The value rows catch the MISSING READ (`RXW` 143/185, all 42 reds
   are value rows, zero stub rows). They do not catch the ACQUIRED WRITE: restore the read and keep the write
   (`RWall`) and the detector falls to the stub. Also, SWAP and ADD are different shapes and the sentence conflates
   them.
6. **`table6/POSTTABLE.out`, the FLOOR line** -- *"the forward-count class CLOSED BY ENUMERATION ... every one
   rowed ... lanes 0-2 on architectural channels ... the data axis's zero/nonzero partition rowed on both sides"*
   inherits items 1, 2, 3 and 4. It is the record a future reader will trust.
7. **`MAINLOOP_HARVEST.md`** -- corrections C1-C4 in section 1. C1 (the WWall row understating a twelve-cell RB1
   breach that the seat's own `PREDICT.out` had named) is the material one.
8. **`PREDICT_r6.out` -- I checked it and found NO error.** It predicts `HEAD_r6` 112/185 with 30 named new reds;
   `HEAD_r6.out` has exactly 73 FAIL rows, and the 30 in the new sessions are exactly the named set (`cmos r1`,
   `iir lca rd2`, `stub3` x9, `stub2` x9, `tailq w` x5, `tailq r` x5). `FIX_r6` is 185/185. Recorded as checked
   rather than left blank -- an unrun check and a clean one must not render the same.

**Not wrong, and worth stating because six passes have now agreed:** the FIX itself (`dev_lca.c`, disposition B) is
correct and untouched by any of this. Every finding here is against the DETECTOR and its record.

---

## 6. HOUSEKEEPING

* **Clone `/tmp/gxopus530c5` RESTORED and verified**: no `.MUTANT`; `dev_lca.c`, `dev_pckbc.c` AND `dev_8253.c` all
  `cmp`-clean against `GXEMUL-SEC`; `gxemul` newer than all three; `restoredC` and `restoredD` byte-identical to
  `base`; no orphan process. Both drivers dropped a clone-local sentinel naming all three files and cleared it only
  after a rebuild-and-`cmp`.
* **Nothing outside `regress/artifacts/lcaisalane/opus_c5_20260915/` was written.** The shipped probe was `cmp`'d
  against the frozen copy at the start of every batch and never edited.
* **LEFT IN PLACE, as instructed**: the clone and all 22 binaries at `/tmp/gxopus530c5_bins` (`base`, `nox`,
  `noff`, `Wpure`, `WWall`, `WWtail`, `WW6`, `W23`, `dNZtail`, `cdxZL3`, `RD2post`, `RD2z`, `RWall`, `RWtail`,
  `WXR`, `RXW`, `Wdrop`, `Rdrop`, plus four `restored*` controls). **/tmp is volatile** -- every log and every
  prediction a durable record could cite is already copied into `logs2/`, and the instruments into `instrument2/`.
* New artifacts: `instrument2/` (`pitrows530c5.py` + its frozen copy, `mut530c5c.py`, `mut530c5d.py`, both
  drivers and their frozen run-copies) and `logs2/` (4 prediction files, 21 measurement logs, 6 mutant diffs,
  build logs, `INSTRUMENT_C/D/E.md5`).
* **One instrument across the whole comparison.** `pitrows530c5.frozen.py` md5 `7919c9e5` was frozen by driver C at
  11:31 and every one of the 16 prototype legs -- including `pit_Rdrop.out`, run three hours later -- used that
  same frozen copy, re-checked by `INSTRUMENT_E.md5`. The shipped 185-row probe (`fb47c89c`) was `cmp`'d against
  `regress/lca_isalane_probe.py` at the start of both batches and never edited.
* The `smoke_base.out` in `logs2/` is a PRE-FREEZE validation run of the prototype against `base` (150/150). It is
  kept for provenance and is **not** part of the comparison; the comparison's baseline is `pit_base.out`.
