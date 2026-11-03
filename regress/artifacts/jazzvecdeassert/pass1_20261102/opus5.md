OPUS_SEAT_ALIVE_20261102_578P1

First line of the brief, verbatim:
> # PANEL PASS 1 -- `jazzvecdeassert` (#578): every access to the Jazz interrupt-source register deasserts the CPU's IRQ3 unconditionally, dropping a level interrupt that is still pending (OB-22, the oldest open bug in the file)

VERDICT: PROCEED WITH CHANGES (6)

Opus 5.5 seat (claude-opus-5-5), pass 1, read-only.  Everything below was read from
`git -C GXEMUL-SEC show HEAD:<path>` at 3cb8bdc1 unless I say otherwise.  Nothing was built or run.
For each claim I say whether I CHECKED it (grep or line read) or am JUDGING it.  My line numbers match
the brief's for dev_jazz.c (`:141/:151` int_asserted writers, `:154/:467/:697` the three IRQ3 deasserts,
`:459` the only int_enable_mask writer, `:780-782` pica_jazzio registration).

## The six changes, in short

1. **Ship the DELETION (option 2), not the conditional.**  They are equivalent on every path, by an
   invariant whose writers I enumerated (Q3).  Also, the conditional hunk **does not compile in est/**:
   est's dev_jazz.c has no `R4030_EXT_IP3` and still uses the pre-#69 predicate (Q5).  So the deletion is
   the only form that is correct in both twins and keeps the identical function identical.
2. **The offset-2 premise is wrong in what it implies.**  Offset 2 of the jazzio page is `PICA_SYS_LB_IE`,
   the guest's per-line LOCAL-BUS INTERRUPT ENABLE (`pica.h:117`).  It is not a timer register; the model
   merely stores it in `jazz_timer_value`.  The "needed by Windows NT" deassert most plausibly stands in
   for **an LB_IE write that masks lines while one is pending**.  That is exactly the case the fix changes.
   So the record must say "NT behaviour CHANGED for the pending case, not measurable here", not "preserved".
3. **Detector floor gap (clause (d), the fix-adds-no-predicate branch):** every row's jazzio access is an
   offset-0 READ.  The mutant `if (relative_addr != 0) INTERRUPT_DEASSERT(d->mips_irq_3);` puts the removed
   behaviour back under a different predicate, and I predict it scores 13/13.  Rows are owed for offset-0
   write, offset-2 read and write, and a default-offset access, each with a line pending (Q2/Q3).  They cost
   no new session.
4. **Correct the "nothing re-asserts it" premise and the severity.**  For UART lines HEAD heals ITSELF
   within one ns16550 tick (16384 cycles), because `DEVICE_TICK(ns16550)` re-asserts on every tick while
   pending.  The red rows therefore depend on single-step with a step budget below one tick period, and the
   probe header must say so.  The lasting loss is for the edge-asserting devices (asc, pckbc).  The only
   guest this project boots (OpenBSD 2.2) loops on the vector until it reads 0, so it is insensitive
   (Q1, "found else").
5. **`jz ip nt` cannot red under any mutant of this fix** (the invariant already clears IRQ3 there).  It is a
   no-regression row, not an NT control, and its label and the brief's "control" wording should say so.
6. **Durability of the witness artifact:** `witness_head.out` cites
   `log=/mnt/c/.../_scratchpad/w578/witness_20261102/transcript_head.log`, and the witness imports
   `_scratchpad/gxprobe.py`.  Copy both transcripts into `regress/artifacts/jazzvecdeassert/witness_20261102/`
   before any record cites them (volatile-path rule).  The committed probe must be self-contained, as the
   brief already plans.

---

## Q1, premise audit

**(a) Can a pica device hold a Jazz local-bus line with no deassert path?**  CHECKED by reading each device's
assert/deassert logic, not by counting macros.  A per-file macro count is a correlate of "has a deassert path".
It cannot see a STATE in which the device holds its line while the deassert branch is unreachable.

Lines on pica (machine_arc.c, read): pckbc jazz.6 (kbd) and jazz.7 (mouse); ns16550 jazz.8 and jazz.9; sn
jazz.4; asc jazz.5; fdc jazz.1; ne2000 on jazz.isa.9 (IP4 path); mc146818 on CPU line 2 directly; the
interval timer on jazz.15 (bit 15, excluded by `& 0x7fff` and by the vector loop's `i<15`).  I checked that
nothing else in machine_arc.c connects to CPU line 3: the only `INTERRUPT_CONNECT(... ".3")` is
dev_jazz.c:754.

* **sn, fdc, vga:** zero INTERRUPT_ASSERT sites (checked).  They never hold a line.
* **asc** (`dev_asc.c:173-179`): the tick asserts on a RISING edge of `NCRSTAT_INT`.  `NCRSTAT_INT` is
  cleared only in the NCR_INTR read (`:1513-1523`, which deasserts) and in `dev_asc_reset` (`:226-228`,
  which deasserts, #266).  Every other `reg_ro[NCR_STAT] =` write (`:872, :954, :1042, :1297, :1316`) has the
  form `(stat & ~7) | phase` and keeps the INT bit.  It has a deassert path.
* **pckbc** (`pckbc_reassert_interrupts`, `:610-640`): edge-tracked by `currently_asserted`.  It deasserts
  when the queue empties or `rx_int_enable` clears.  It has a path.
* **ns16550** (`:92-104`): **ONE held-line state exists.**  If the guest clears `MCR.IENABLE` (OUT2) while
  the IER/IIR condition still holds, the first branch is taken.  That branch neither asserts nor deasserts,
  `d->int_asserted` stays 1, and the Jazz bit stays set.  The line stays high until IER is cleared, or until
  IIR_TXRDY/RXRDY drops (IIR read, or input drained).  So "drop OUT2 to silence the port" does not drop the
  line in this model.  Under HEAD the next jazzio access would hide that.  Under the fix (or deletion), IRQ3
  stays high while IP3 is enabled.
  - Reachability by OpenBSD 2.2, CHECKED in `_guest-src-openbsd22`: `arch/arc/dev/com_lbus.c:160-161`
    writes `com_ier, 0` and THEN `com_mcr, 0`, so IER goes first and the line drops through the normal
    branch.  I did not trace `dev/ic/com.c`'s close/open order completely; that is UNSETTLED but low risk,
    and gate 4 measures it.
  - This is a device-model wart (OUT2 should gate the output).  It is not a reason to keep the blanket
    deassert.  It is the one precise answer to "could IRQ3 be left high": **yes, by a guest that masks a UART
    with OUT2 alone, or one that masks lines with LB_IE alone (change 2).**
* **Storm risk on the gate-4 boot:** OpenBSD 2.2's handler is `pica_iointr` (`arch/arc/pica/picabus.c:291-300`,
  CHECKED):

  ```c
  while((vector = inb(PVIS) >> 2) != 0) {
          (*int_table[vector].int_hand)(int_table[vector].param);
  }
  ```

  It loops until the vector reads 0, and an unhandled slot goes to `pica_intrnull`, which PANICS (`:281-285`).
  Consequences:
  - An unserviced pending line already panics HEAD's boot inside this loop.  Since gate 4 boots, no such
    line occurs there.
  - On loop exit nothing is pending, so HEAD and fix leave IRQ3 in the same state.
  - **For this guest the defect is benign and the fix should be invisible.**  Both are still worth
    measuring by gate 4, not asserting.

**(b) Cause 0x800 and `print cause`.**  CHECKED: `cpu_mips.c:245-257` registers lines i=2..7 as
`templ.line = 1 << (STATUS_IM_SHIFT + i)`, so i=3 gives bit 11 = 0x800.  `mips_cpu_interrupt_assert`/`_deassert`
(`:1884-1892`) are a bare OR / AND-NOT with no reference count, and `INTERRUPT_ASSERT` is a bare call.  A
guest `mtc0` to Cause affects only `0x3 << STATUS_IM_SHIFT` (`cpu_mips_coproc.c:949-953`, CHECKED), so the
guest cannot forge IP3.  I did not read the debugger's `print cause` implementation.  The witness's
`jz ip one` = 0x800 serves as its liveness evidence.

**(c) Synchronous ns16550 assert.**  CHECKED.
- The IER write arm (`:186-201`) sets IIR_TXRDY on an ETXRDY rising edge and calls `dev_ns16550_tick`
  inline.
- The tick asserts only if `MCR & MCR_IENABLE`.  The witness writes MCR=0x08 first, and the MCR write arm
  (`:282-291`) also sets TXRDY and calls the tick, harmlessly, since IER is still 0.
- Synchronous: yes.

**But the brief misses one property of the same tick:** it calls `INTERRUPT_ASSERT` on EVERY tick while the
condition holds; there is no edge test, unlike asc and pckbc.  It is registered at TICK_SHIFT 14
(`:50`, `:357`).  `machine.c:355` sets the reset value to `1 << 14`, and `:727-728` decrements it by 1 per
single-step and by N_SAFE_DYNTRANS_LIMIT when free-running.  So:
- **Free-running:** a UART line dropped by HEAD's tail is re-asserted within about 16K cycles.
- **Under single-step:** that happens only every 16384 steps.
The witness's red rows are deterministic only because its whole run is a few hundred steps, far below one
period.  That is a property the committed probe must state.  An added row or a longer stub could cross a tick
boundary and turn a HEAD red green.  It would not be load-sensitive, but it would be step-budget-sensitive.

**(d) Encodings.**  CHECKED arithmetic against `:666-676`: line 8 gives v=9, 9<<2 = 0x24; line 9 gives
v=10, 10<<2 = 0x28; IP3 = 0x02 at `dev_jazz.c:79` (R4030_EXT_IP3).  All correct.
- Guest-side cross-check (CHECKED): OpenBSD 2.2's `PICA_SYS_LB_IE_COM1 0x0100` / `COM2 0x0200`
  (`arch/arc/pica/pica.h:112-113`) show LB_IE bit i corresponds to Jazz line i.  So com0 = line 8 agrees
  with the guest's own numbering.
- `inb(PVIS) >> 2` indexes `int_table[i+1]`, consistent.
- The witness reads the vector with `lw` (guest_load32) at relative 0.  OpenBSD uses `inb`.  Both reach
  `case 0`.  A byte read at `+1` would go to `default:`.

**(e) "The two deassert lines are the 0.7.0 import's."**  CHECKED that
`git log -L 694,698:src/devices/dev_jazz.c` returns exactly one commit, `39748e3c` (the import).  Two
qualifications:
- The project's own memory records that 39748e3c is NOT a pristine upstream commit.
- No pristine 2021 copy is present under the project root today: there is no `./src/`, and I did not find
  `GXEMUL_upstream_2021`.
So "upstream's" is established only as "unchanged since the import", not against pristine upstream.  est's
copy carries the same two lines (est `:661-662`, CHECKED), which supports, but does not prove, upstream
origin.

**Premise false in section 1, "offset 2 reads or writes jazz_timer_value".**  That is code-true but
semantically misleading (change 2).
- `pica.h:116-117`: `PICA_SYS_LB_IS (PVIS+0)` "Local bus int source", `PICA_SYS_LB_IE (PVIS+2)` "Local bus
  int enables".
- OpenBSD 2.2 writes it: `machdep.c:1270` (`out16(PICA_SYS_LB_IE,0x000)` in `initcpu`, "Disable all
  interrupts"), and `picabus.c:254` (`out16(PICA_SYS_LB_IE, local_int_mask)` on every intr_establish).
- In the model that write sets `jazz_timer_value`, which separately arms the "Linux?" branch of
  `DEVICE_TICK(jazz)` (`:299-310`).  That is a separate conflation; I am naming it, not asking to fix it here.
- **The blanket tail deassert is the model's only crude approximation of "LB_IE write masks lines".**  The
  brief's own NT question ("does it depend on the deassert firing WHILE A LINE IS PENDING?") gets a reasoned
  answer of **probably yes**: a mask write is the event that should drop the CPU line with lines still
  pending.  That is unmeasurable here, as the brief says, but the claim "the fix preserves the case the old
  comment describes" should be withdrawn.

## Q2, the partition

The body-tested partition of the tail predicate P = `(int_asserted & 0x7fff) && (int_enable_mask & IP3)`
gives {pending: 0, >=1} x {mask IP3: off, on}.  I add "two pending" as the brief asks.  I also add the axis
the brief omits: **the access label {offset 0, offset 2, default} x {read, write}**.  The tail is reached from
all six cells.  The body tests `writeflag` in case 2 and in `default`, and it tests `relative_addr` in the
switch.

**INVARIANT I** (CHECKED by enumerating every writer):

> CPU IRQ3 is high  =>  P is true.

* `int_asserted` is written only at `:141` (assert handler) and `:151` (deassert handler).
* `int_enable_mask` is written only at `:459` (mask arm).
* `mips_irq_3` is asserted only at `:144` (under P) and `:469` (under new P).
* It is deasserted at `:154` (under !P), at `:467` (old P and !new P), and at the tail.
* Init is memset 0 (`:712`), so P is false and IRQ3 is clear.
* The guest cannot set IP3 via mtc0 (Q1b), and nothing else connects to CPU line 3 on pica or magnum.

The same writers recompute P on every change of its operands, so the converse also holds outside the tail:
P true implies IRQ3 high, except where HEAD's tail has dropped it.

| cell | HEAD | fix / deletion | rows |
|---|---|---|---|
| 0 pending, mask on | IRQ3 already clear; tail is a no-op | same | `jz ip none`, `jz vec none`, `jz ip nt` |
| 0 pending, mask off | no-op | same | none (equivalent, nothing to pin) |
| 1 pending, mask on | **drops IRQ3** | keeps it | `jz ip com1` (see note) |
| 2 pending, mask on | **drops IRQ3** | keeps it | `jz ip after` |
| >=1 pending, mask off | IRQ3 already clear by I; tail is a no-op | same | none |

**The fix changes exactly the cells where P is true, and only those.**

**On "(pending, mask disabled) is unobservable through the tail's predicate": I CANNOT refute it.  It is TRUE
for the Cause channel**, and here is the derivation.
- By I, IRQ3 is already clear in that cell under every build, so whether the tail deasserts makes no
  difference.
- The cell IS reachable (write EXT_IMASK 0 with a UART pending), and it has other channels:
  - The vector read still returns 0x24 there (case 0 ignores the mask).
  - A subsequent EXT_IMASK write of 0x2 must re-assert IRQ3 via the `!old && new` arm.
- Neither channel separates HEAD from the fix.  But a row "mask off, vector read, mask on, IP3 set" kills a
  different and tempting wrong fix: **clear the line's `int_asserted` bit on the vector read**.  The OB-22
  table row's own phrase, "without clearing int_asserted", invites that fix.  `jz vec again` already kills it
  for the mask-on case, so this extra row is optional, under clause (e).

**Notes on the existing rows (CHECKED by reading the witness script):**
* `jz ip com1` on HEAD reads 0 for two reasons stacked:
  - IRQ3 was already dropped at `jz vec`;
  - the `jz vec com1` read itself is a jazzio access that would drop it again.
  So the row does not isolate "a one-line-pending vector read drops IP3".  A cleaner cell: after `jz ip reheal`
  (IRQ3 freshly high with com0 and com1 pending), do one vector read and read IP3.  Even better, use a
  one-pending reheal: re-raise with only com1 pending, by toggling com1's IER 0 then 2.
* `jz ip nt` is the cell (0 pending, mask on).  By I it reads 0 on HEAD, the fix, deletion and every mutant
  that only deasserts.  **It cannot red under any mutant of this fix** (change 5).

**The access-label axis has one rowed cell of six: (offset 0, read).**  Owed rows, each with com0 and com1
pending and IRQ3 high, then `print cause`:
- `jz ip vecw`: a store to offset 0.
- `jz ip lbie`: a halfword or word read at offset 2.
- `jz ip lbiew`: a write at offset 2.  Write 0, the value OpenBSD's initcpu writes, so the "Linux?" tick
  branch is not armed (jazz_timer_value stays 0).
- `jz ip dflt`: a byte read at 0xf0000001 (the `default:` arm; it prints one unlatched `fatal()`).
They fit in the existing session after `jz ip reheal`, re-raising before each if needed.  This is the
pre-table SIBLING PARITY / joint-label point turned on the tail: all three case labels flow into the edited
tail.

## Q3, weakenings and the equivalence

Let the fix deassert when !P'.  It is equivalent to the fix iff (!P' implies IRQ3 already clear), and by I
that is iff (P implies P').  So **every WEAKENING of P (P' implied by P) is EQUIVALENT, and only
STRENGTHENINGS are detectable**, and only at inputs where P holds and P' fails.  The table below is predicted
from the source; nothing was built.

| mutant | equivalent? | first differing input | rows that red |
|---|---|---|---|
| `M_b` (blanket reinstated) | NO | first jazzio access with >=1 line pending and IP3 enabled | `jz ip after`, `jz ip com1` (11/13) |
| `M_del` | **YES, by I (proof, not measurement)** | none | none (13/13).  13 green rows are CONSISTENT with equivalence; they do not prove it.  The proof is the writer enumeration above. |
| `M_nomask` (drop mask term) | YES (a weakening) | none | none |
| `M_lowbits` `& 0x00ff` | NO, but only for lines 8-14 | an access with only lines in 8..14 pending | both IP rows (11/13).  It is EQUIVALENT when a line in 0..7 is pending, so a mutant `& 0x0300` (lines 8/9 only) is the mirror escape: it passes all 13 rows and re-opens the defect for asc (5) and pckbc (6/7) |
| `M_ip6` | NO | access with pending and mask having IP3 but not IP6 (the rows' 0x2) | both IP rows (11/13).  Equivalent when the mask is 0x12 |
| `M_timer` `& 0x8000` | NO | access with a local line pending and the timer line not pending | both IP rows (11/13).  Masked whenever the timer line is pending |
| `M_inv` | NO | the same input as `M_b` | `jz ip after` AND `jz ip com1` (11/13).  The brief named only the first; at `jz vec com1`, P is true (bit 9), so M_inv deasserts there too.  `jz ip nt` stays green as the brief says |

**Ship the deletion.**  Reasons:
1. The conditional is a guard that by I can never fire with an effect.  Shipping it adds a FOURTH copy of P
   whose weak side no detector can ever pin, since every weakening is equivalent.  That is a guard the
   addition licence would call "cannot hurt".
2. It cannot be byte-identical in est (Q5).
3. It matches the house idiom (Q6).

**The honest record:** "conditional form considered and measured/derived EQUIVALENT to deletion via invariant
I; deletion shipped because the tail has no effect once the predicate holds the line, and the handlers already
maintain it."  A one-line comment at the old site (`/* #578: no deassert here -- the CPU line follows
jazz_interrupt_(de)assert() and EXT_IMASK; see OB-22 */`) is enough.

**With deletion the fix ADDS no predicate**, so clause (d)'s "pure deletion" branch applies: put the removed
behaviour back under a DIFFERENT predicate.  The enumerated set, bounded to the enclosing function's own
tests:

| mutant | predicted score |
|---|---|
| `if (relative_addr == 0) DEASSERT` | 11/13, reds |
| **`if (relative_addr != 0) DEASSERT`** | **13/13, ESCAPES today** |
| `if (writeflag == MEM_READ) DEASSERT` | reds |
| **`if (writeflag == MEM_WRITE) DEASSERT`** | **13/13, ESCAPES today** (no row writes jazzio) |
| `if (relative_addr == 2) DEASSERT` | **ESCAPES** |
| `if (v == 0) ...` (DEASSERT when the vector is 0) | equivalent by I |
| `if (v != 0) ...` | reds |

Three escapes means the 13-row detector is BELOW the floor for the deletion.  The four owed rows in Q2 close
all of them.  Kept as mutants for the conditional form: `M_b`, `M_inv`, and the mirror strengthening
`& 0x0300`.  The last is a clause-(e) disclosure unless a line-5/6 row is added.  pckbc can assert line 6
synchronously: enable the keyboard interrupt in the command byte, then issue a command that queues a response
byte.  I have not traced that sequence; UNSETTLED.

## Q4, the vehicle

Gate 4 is the right home: it is the only gate holding `$ARC_RIG/gxsec-gxemul`, and it boots the guest whose
behaviour the deletion must not change.  A ~40 s cold probe is acceptable.  Load sensitivity:
- There is no free-running oracle.
- The pty driver's read timeouts are wall-clock, but a timeout yields None and therefore FAIL.  That is a
  loud failure, not a false pass.
- The one real sensitivity is the STEP BUDGET versus the 16384-step tick period of ns16550 and jazz
  (Q1c), and that is deterministic.
Pin the row count by equality, as planned (13 + the owed rows).  Write the probe header's clause-(e) contract
to cover: lines 8/9 only; mask 0x2 only; the label cells rowed; lines 0-7/10-14 and the timer line
disclosed.

## Q5, the twins

CHECKED:
- est's `jazz_jazzio` (47 lines) is byte-identical to SEC's.
- `cmp build/src/devices/dev_jazz.c est/...` is clean, and `cmp build-asan/... GXEMUL-SEC/...` is clean.
- **But est's predicate is the pre-#69 form:** est `:120` is `d->int_asserted & d->int_enable_mask & 0x7fff`,
  and `R4030_EXT_IP3` does not occur in est's file at all.

So:
- **The conditional hunk, copied into est (and from there into build/, which compiles dev_jazz.c into the
  pmax binary), would FAIL TO COMPILE.**  A version using est's own predicate would make the two
  "identical" functions diverge.
- Invariant I holds in est too, by the same writer shape with est's predicate.  So the DELETION is correct in
  both and keeps the function byte-identical.

**Land the deletion in both.**  Owed at landing:
- SEC to `/tmp/gxsec-build` and `build-asan/` (two-part clearance against SEC).
- est to `build/`.  Per the divergence rule, `build/` is compared against est for this path, never against
  SEC, and part 2 is a rebuild of build/'s binary because dev_jazz.c is linked into it.
- est: source tree, part 2 N/A.

## Q6, option-set completeness

Members the brief did not name:
* **7. MODEL LB_IE (implement).**  Store offset 2 as `lb_ie` and use
  `(int_asserted & lb_ie & 0x7fff) && (mask & IP3)` at the three predicate sites.  Recompute IRQ3 on an
  LB_IE write, as the EXT_IMASK arm does.  Then delete the tail.
  - That is `jazzlbmask` and OB-22 together.  It gives NT's plausible "mask then expect quiet" behaviour
    honestly instead of by a blanket drop.
  - The bit mapping is settled by the guest's own header (`PICA_SYS_LB_IE_*`, bit i = line i).
  - Round-scope rule: it is the same device and the same semantic class (CPU line follows pending&enabled),
    but it needs new oracles.  So I recommend it as the NEXT round, filed with this dependency, not merged.
  - Caveat it must carry: OpenBSD writes LB_IE before EXT_IMASK in `initcpu`.  Separating it from
    `jazz_timer_value` changes the "Linux?" tick branch's arming, so it has its own blast radius.
* **8. Clear-on-read (ACK semantics):** clear the reported line's `int_asserted` bit on the vector read.
  Rejected: it breaks the level model the rest of the file implements, and the device would still hold its
  output.  `jz vec again` pins against it.

**Grepped idiom (CHECKED by grep, partial reads):**
- `dev_footbridge.c:572`: the IRQStatus read returns `irq_status & irq_enable` and touches no CPU line.  The
  line is recomputed at assert and deassert from `(status & enable)` (`:394, :409`).
- `dev_gc.c` recomputes on enable writes (`:123-183`).
- `dev_8259.c` changes the line only on EOI (a write that edits ISR, `:145-174`).  ISR/IRR reads at `:194`
  have no line side effect.
- No controller in the tree drops its CPU line as a side effect of a status or vector read.

**The house idiom is "a read has no side effect; the line follows pending & enable".**  That supports the
deletion for #578 and member 7 for the follow-up.

## Something else found

* `DEVICE_TICK(jazz)`'s "Linux?" branch (`:299-310`) is armed by ANY nonzero write to offset 2, i.e. by
  OpenBSD's own `pica_intr_establish` LB_IE writes.  It then asserts `jazz_timer_irq` whenever
  `pending_timer_interrupts > 0`, independent of `interval_start`.  It is a pre-existing conflation of LB_IE
  with a timer; file it under `jazzlbmask`.  Do not touch it here.
* The OB-22 row's text ("without clearing int_asserted") describes the wrong remedy (member 8).  The round
  record should say the defect is the CPU-line drop, not a failure to clear.

## Premises I could not settle

- Windows NT's actual LB_IE/jazzio access pattern (no image, no source).
- Pristine-upstream origin of the two lines (no pristine copy found).
- dev/ic/com.c's full IER/MCR ordering on close.
- Whether a pckbc line-6 synchronous assert sequence exists for a row.
- The debugger's `print cause` implementation (taken from the witness's liveness row).

VERDICT: PROCEED WITH CHANGES (6)
