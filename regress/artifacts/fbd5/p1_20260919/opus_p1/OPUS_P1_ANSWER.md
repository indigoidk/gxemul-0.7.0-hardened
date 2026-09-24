OPUS_SEAT_ALIVE_20260919_FBD5P1

`# CHECKPOINT -- 2026-09-19 06:2x   HEAD: 9c28ca5 #539 receipt (7836071 = #539 n6, the footbridge IRQEnable read ACCEPTED)`

---

## VERDICT

**PROCEED with the five-site decline, but the ROW SET AS PROPOSED IS BELOW THE VACUITY FLOOR:
I built the brief's own Q2(c) weakening and it swept the proposed A1-A5/D1-D5 detector CLEAN, and
so did two more (Q2 f, and the FIQ read-expression mutant). Three measured total escapes.**

* The fix itself measures correct. All five sites witnessed dying at rung 3 on the committed build
  (exit 1, five distinct complaint texts); after member 3 all five survive, announce exactly once
  across two accesses, leave every register untouched, and the shipped sites probe goes
  **18 of 19 with K1 the only red** — exactly the bridge retiring and nothing else moving.
* **`m_sharebit` (Q2 c) scored 20/20 on the D rows and 9/9 on the A rows, and `m_onebit` — all
  five sites on ONE bit, the "aggregate boolean" the brief itself warns about — ALSO scored 20/20.**
  Cause: every proposed D row touches ONE site in ITS OWN PROCESS, so a shared latch bit is
  unobservable by construction. **One extra arm fixes it and costs one cold launch (0.4 s):** all
  five sites in ONE process, announce count 5. Measured: 5 on the fix, 4 under `m_sharebit`,
  1 under `m_onebit`.
* **A4/A5 are vacuous for the read EXPRESSION, because `d->fiq_status` has NO WRITER ANYWHERE IN
  THE TREE.** `grep -rn 'fiq_status' src/` returns the struct declaration and the two read arms and
  nothing else. So `fiq_status & fiq_enable`, `fiq_status`, and constant `0` are the same observable,
  measured: `m_fiqraw` (drop the `&` at +0x280) escaped 29/29. A4 does catch `odata = d->fiq_enable`
  (measured red at 0xc0), so it is not wholly vacuous — but the brief's instruction "verify the FIQ
  enable through its effect on +0x280/+0x284" is **not satisfiable: I set fiq_enable to 0xc0 and all
  three of +0x280, +0x284, +0x288 read 0.**
* **`m_swallow` (Q2 f) escaped 29/29 too**, for the same reason one level over: `irq_status` cannot
  be made nonzero by any single-stepped guest (measured — I armed timer 1 and spun 24 steps;
  +0x184 still read 0), so A1's `0` is the same `0` a constant-0 arm returns.
* **Both harness legs measure GREEN through all three launchers, with negative controls** — and
  BOTH of K2's non-obvious clauses are load-bearing: a child that died BEFORE the prologue finished
  produces `next-send fails` and `dead` **identically**, and is separated only by `exit == 0` and by
  the fresh-`reg` prologue verification. **A K2 without those two clauses goes green exactly when
  the fix has failed.**
* **Q2(h) settled by measurement: FIVE different startup refusals all exit 1** — so neither
  "nonzero" nor "== 1" discriminates. Only the diagnostic text naming the input does.
* **Four brief premises are wrong or unsupported** (details in Q1): the exit census is **9, not ten**
  (the project's own `tools/pipeline/exit_census.py` says 9, and the brief's own list names nine
  lines); HEAD is **f685d75**, not 9c28ca5 (records-only; the two files under review are
  byte-identical, so nothing measured is affected); "five `int` latches in the file's existing
  style" — **the file has no latch of any kind, zero `static int`, zero `warned` field**; and the
  0-on-a-declined-read warrant is quoted from a sentence about a **nonexistent** CSR, while 18Ch is
  an existing write-only one.
* **A sibling-parity finding the brief does not contain: 28Ch (FIQEnableClear) — the exact FIQ twin
  of 18Ch — ALREADY declines silently and returns 0 today, and 190h/290h announce on EVERY access
  through `default:`.** Measured. So the interrupt controller carries three different dispositions
  for write-only-register reads, and this round adds a fourth at 18Ch while leaving its twin alone.

Everything below is measured in `/tmp/gxopusfbd5`, a `cp -a` of `build/`. No project tree was
written. No gate was run. The clone is restored, `cmp`-clean and REBUILT.

---

## 0. TREE UNDER REVIEW — checked before measuring

```
git -C GXEMUL-SEC log --oneline -1   ->  f685d75 records: five "fable5" rulings ...
git diff --stat 9c28ca5 f685d75 -- src/devices/dev_footbridge.c regress/footbridge_sites_probe.py
                                     ->  (empty: byte-identical)
git status --porcelain -- src        ->  6 files dirty, none of them dev_footbridge.c
wc -l src/devices/dev_footbridge.c   ->  899            (brief says 899 -- agrees)
wc -l regress/footbridge_sites_probe.py -> 445
```

Every line of the brief's section-3 inlined function matches the file byte for byte at the line
numbers given (498-760), and section 5's four citations match (sites 161/347/402/408/411,
drain 231, witness 200). **I found no line-number drift of any size.**

One thing to carry: `regress/gate_arm.sh` is **uncommitted-dirty in the working tree (+67 lines
against HEAD)**, and this round plans to edit its footbridge section. That section will be edited
on top of deltas nobody has reviewed.

---

## 1. THE WITNESS (rung 3, committed HEAD) — `s2_witness_HEAD.out`

Shape: `regress/footbridge_sites_probe.py`'s — cold `-E cats -M 32` debugger, MMU-off prologue,
words planted with `put w`, stepped ONE AT A TIME, each stepped word compared against the
disassembly the emulator prints. Registers read at a checkpoint BEFORE the site access, so a dying
arm still carries its controls.

Controls, identical in all five arms: `r3 = 0x00001136` (CP15 c1 bit 0 CLEAR, MMU really off),
`r5 = 0x11223344` (RAM liveness), `r6 = 0x00001011` (VENDOR_ID — the device signature; RAM would
not answer that).

| arm | the one guest access | disassembled as | status | exit | the exact complaint text |
|---|---|---|---|---|---|
| W1 | `str r8,[r0,#384]`  +0x180 | `str r8,[r0,#384]` | HOST-DIED | **1** | `[ WARNING: footbridge write to irq status? ]` |
| W2 | `str r8,[r0,#388]`  +0x184 | `str r8,[r0,#388]` | HOST-DIED | **1** | `[ footbridge write to irq_raw_status ]` |
| W3 | `str r8,[r0,#640]`  +0x280 | `str r8,[r0,#640]` | HOST-DIED | **1** | `[ WARNING: footbridge write to fiq status? ]` |
| W4 | `str r8,[r0,#644]`  +0x284 | `str r8,[r0,#644]` | HOST-DIED | **1** | `[ footbridge write to fiq_raw_status ]` |
| W5 | `ldr r1,[r0,#396]`  +0x18c | `ldr r1,[r0,#396]` | HOST-DIED | **1** | `[ WARNING: footbridge read from ENABLE CLEAR? ]` |

`signal=None` in all five: an ordinary `exit(1)`, not a signal death. Zero disassembly mismatches.
**This is the round's pre-fix red, and it is five for five.** Wall: 1.5 s for five cold launches.

All five texts are DISTINCT — the brief's "0/5 share an exact message" is confirmed by enumeration,
and it is what makes the count channel per-site.

---

## 2. THE ACCEPT SIDE ON HEAD — `s3_accept_HEAD.out`

Both arms SURVIVED, `exit=0`, **zero footbridge diagnostics**.

| what | measured |
|---|---|
| `+0x188 <- 0x30` then read `+0x180` | **0x00000000**  (`irq_status & irq_enable`, and irq_status is 0) |
| read `+0x184` | **0x00000000** |
| `+0x18c <- 0x10` with enable 0x30, read `+0x188` | **0x00000020**  — the brief's claim, confirmed |
| then `+0x18c <- 0`, read `+0x188` | **0x00000020**  — a zero write preserves it |
| `+0x288 <- 0xc0` then read `+0x280` | **0x00000000** |
| read `+0x284` | **0x00000000** |
| read `+0x288` | **0x00000000**  — `fiqenableread` confirmed: the FIQ enable is unreadable |
| `+0x28c <- 0x40` then read `+0x288` | **0x00000000** |

**The legal directions already work, and the FIQ enable is unobservable from the guest by any
route.** I set it, and all three of the registers that could show it read 0. The brief's
"verify the FIQ enable through its effect on +0x280/+0x284" cannot be done, and the reason is in
the source: `d->fiq_status` is assigned **nowhere in the tree** —

```
grep -rn 'fiq_status\|fiq_enable' src/     ->   dev_footbridge.c:83  uint32_t fiq_status;
                                                dev_footbridge.c:84  uint32_t fiq_enable;
                                                dev_footbridge.c:612 odata = d->fiq_status & d->fiq_enable;
                                                dev_footbridge.c:621 odata = d->fiq_status;
                                                dev_footbridge.c:630 d->fiq_enable |= idata;
                                                dev_footbridge.c:635 d->fiq_enable &= ~idata;
```

so line 612 is `0 & fiq_enable` for the life of the process, and `fiq_enable`'s only read is that
one AND. **`fiq_enable` is write-only state with no observable consequence anywhere.**

**And `irq_status` is equally pinned for a stepped probe.** Its only writer is
`footbridge_interrupt_assert()` (`:378`), reached from `DEVICE_TICK` (`:365`) only when
`pending_timer_interrupts[i] > 0`, which is produced by a `timer_add`/SIGALRM callback — and
`debugger.c` stops the host timers for the whole of a `step`. I measured it rather than inferring:
arm timer 1 (`+0x300 <- 1`, `+0x308 <- 0xc0`), enable 0x34 so IRQ_TIMER_1 (bit 2) would show, spin
24 steps, read back — **`+0x180 = 0`, `+0x184 = 0`, `+0x188 = 0x34`** (`s7_cross.out`, set `seed`).

---

## 3. THE PROPOSED FIX, MEASURED

### 3.0 What I applied, and the latch-storage choice

**K4's `uint32_t warned_access` bit-field, one bit per site**, because the brief's alternative
("five `int` latches in the file's existing style") has no referent: **`dev_footbridge.c` contains
no latch at all.** `grep -n -e 'static int' -e 'warn' -e 'once' src/devices/dev_footbridge.c`
returns **nothing**. So there is no in-file idiom to match, only the house idiom (per-instance
field + `fatal()` carrying an explicit suppression marker), and both candidate storages satisfy it.

Zeroing: `DEVINIT` does `memset(d, 0, sizeof(struct footbridge_data))` at `:771` — **and there is a
SECOND zeroing path the brief does not mention**: `regress/diff_footbridge.c:151` and
`regress/diff_fbpending_bound.c:143` `#include` the device's `.c` and build their own instance with
`calloc(1, sizeof(struct footbridge_data))`. Both zero the new field, so neither differential
breaks; I name it because "cleared by DEVINIT's memset" is one of two paths, not the only one.

The diff applied (`s4_fix_apply.out`, full text there): the struct gains `warned_access` plus five
`FB_W_*` defines; each of the five arms replaces `fatal(...); exit(1);` with
`if (!(d->warned_access & BIT)) { d->warned_access |= BIT; fatal("... (once) ]\n"); }`; the +0x18c
arm additionally **drops `odata = d->irq_enable;`**. Build clean, `MAKE_RC=0`, no warnings,
`[ gxemul -nt src/devices/dev_footbridge.c ]` true.

### 3.1 (a) The five witness arms again, on the fixed build — `s5_postfix.out`

| arm | status | exit | complaints over the arm | text |
|---|---|---|---|---|
| W1 +0x180 | **SURVIVED** | **0** | 1 | `[ WARNING: footbridge write to irq status? (once) ]` |
| W2 +0x184 | **SURVIVED** | **0** | 1 | `[ footbridge write to irq_raw_status (once) ]` |
| W3 +0x280 | **SURVIVED** | **0** | 1 | `[ WARNING: footbridge write to fiq status? (once) ]` |
| W4 +0x284 | **SURVIVED** | **0** | 1 | `[ footbridge write to fiq_raw_status (once) ]` |
| W5 +0x18c | **SURVIVED** | **0** | 1 | `[ WARNING: footbridge read from ENABLE CLEAR? (once) ]` |

The D arms (two accesses at the site, then the state read back), all SURVIVED / exit 0 /
**one announcement across two accesses**:

| arm | two accesses at | +0x180 or +0x280 | +0x184 or +0x284 | enable reg | announces |
|---|---|---|---|---|---|
| D1 | +0x180 `<- 0x10` ×2 | 0x00000000 | 0x00000000 | +0x188 = **0x30** | **1** |
| D2 | +0x184 `<- 0x10` ×2 | 0x00000000 | 0x00000000 | +0x188 = **0x30** | **1** |
| D3 | +0x18c read ×2 | (r1 = **0**) | (r7 = **0**) | +0x188 = **0x30** | **1** |
| D4 | +0x280 `<- 0x40` ×2 | 0x00000000 | 0x00000000 | +0x288 = 0 | **1** |
| D5 | +0x284 `<- 0x40` ×2 | 0x00000000 | 0x00000000 | +0x288 = 0 | **1** |

D3's two reads return 0 and 0 — the enable leak is gone — and the enables are unchanged, so there
is no clear-on-read. **Rows A1-A5 and D1-D5 are all satisfied by the fix as the brief expects.**

*One row-design note measured rather than argued:* the brief's D4/D5 write value is `0x10` while
fiq_enable is `0xc0`, and `0x10 & 0xc0 == 0`, so a store-into-`fiq_status` mutant would move +0x284
and **not** +0x280. I used **0x40** (inside 0xc0) so both channels move. Cost: none. Keep 0x10 for
D1/D2, where 0x10 is inside 0x30 already.

### 3.2 (b) The shipped sites probe, unchanged — `s5_postfix.out`, tail

```
  arm L  live      (MMU off)               SURVIVED  exit=0     signal=None
  arm T  trap ctrl (MMU LEFT ON)           SURVIVED  exit=0     signal=None
  arm K  kill      (MMU off,+18c)          SURVIVED  exit=0     signal=None
  arm E  enable    (MMU off,#539)          SURVIVED  exit=0     signal=None

C1   liveness: guest ran, plain RAM readback  got=0x11223344   want=0x11223344   ok
C2   MMU really OFF in arm L (CP15 c1 bit 0)  got=0x00000000   want=0x00000000   ok
C3   MMU really ON in arm T (the arms differ) got=0x00000001   want=0x00000001   ok
C4   MMU-on arm CANNOT see the device         got=0x00000000   want=!= 0x1011    ok
A1   VENDOR_ID through a real guest ldr       got=0x00001011   want=0x00001011   ok
A2   TIMER_1_LOAD masked to 24 bits (MAX_VAL) got=0x00345678   want=0x00345678   ok
A2b  the value the guest actually stored      got=0x12345678   want=0x12345678   ok
I1   isolation arm SURVIVES untouched         status=SURVIVED exit=0         ok
K1   kill arm dies at 0x18c, exit 1           exit=0                         FAIL
      kill arm said: [ WARNING: footbridge read from ENABLE CLEAR? (once) ]
EC1  arm E liveness: plain RAM readback       got=0x11223344   want=0x11223344   ok
EA1  arm E reaches the device: VENDOR_ID      got=0x00001011   want=0x00001011   ok
E0   IRQEnable reads 0 before any write       got=0x00000000   want=0x00000000   ok
E1   Set <- P, read back                      got=0x00002002   want=0x00002002   ok
E2   Set <- Q, read back (|=)                 got=0x60002002   want=0x60002002   ok
E3   byte read: low byte                      got=0x00000002   want=0x00000002   ok
E6   halfword read: low two bytes             got=0x00002002   want=0x00002002   ok
E5   Clear <- P, read Set back                got=0x60000000   want=0x60000000   ok
E4   arm E: no footbridge diagnostic, exit 0  status=SURVIVED exit=0 fatals=0 ok
D1   every planted word disassembled as meant 0 mismatches                   ok

ROWS=18 of 19
FOOTBRIDGE_SITES_CONTROL=OK
FOOTBRIDGE_SITES_FAIL
```

**Exactly K1 goes red, everything else stays green, and the control block stays OK.** Note K1's
own printed line already shows the new text — the probe's `saw ENABLE CLEAR` half still matches,
and it is the `K["exit"] == 1` half that reds. The same is true of the other two probes: both score
`status == "HOST-DIED" AND saw AND exit == 1` (`fbpending_drain_probe.py:712-713`,
`fbpending_witness.py:634-635`), so all three go red on the status and exit clauses while their text
clause stays satisfied. **One row per probe to replace, and none of the three can be "fixed" by
touching the text.**

And on the restored HEAD build at the end of the session the same probe reads
`ROWS=19 of 19 / FOOTBRIDGE_SITES_PASS` (`s11_restore.out`) — so 18/19 is the fix, not the harness.

### 3.3 THE WEAKENING TABLE — `s6_table.out`, `s7_cross.out`, `s8_all5.out`

Eleven variants built and scored, each from HEAD source + one patch, each a fresh
`rm src/devices/dev_footbridge.o gxemul; make -j6` with the freshness check. Scored against the
brief's own rows: `accept` = A1..A6 + two silence rows (9), `decline` = D1..D5 × {two state
readbacks, the enable readback, the announce-count-and-survival row} (20), plus the shipped sites
probe (19).

| # | mutant (Q2 label) | accept 9 | decline 20 | sites | which row reds first |
|---|---|---|---|---|---|
| — | **the fix** | 9/9 | 20/20 | 18/19 (K1) | — |
| a | `m_keepexit` keep `exit(1)` at +0x284 only | 9/9 | **16/20** | 18/19 | D5s,D5r,D5e,D5n (the arm dies) |
| b | `m_unlatch` announce every access | 9/9 | **15/20** | 18/19 | D1n,D2n,D3n,D4n,D5n (n=2) |
| c | `m_sharebit` +0x180 and +0x184 share a bit | 9/9 | **20/20** | 18/19 | **NOTHING — TOTAL ESCAPE** |
| c' | `m_onebit` ALL FIVE share one bit | 9/9 | **20/20** | 18/19 | **NOTHING — TOTAL ESCAPE** |
| d | `m_leak18c` +0x18c keeps `odata = irq_enable` | 9/9 | **18/20** | 18/19 | D3s,D3r (0x30 instead of 0) |
| e | `m_store180` the decline stores into irq_status | 9/9 | **18/20** | 18/19 | D1s,D1r (0x10 instead of 0) |
| f | `m_swallow` IRQ_STATUS READ returns 0 always | 9/9 | **20/20** | 18/19 | **NOTHING — TOTAL ESCAPE** |
| g | `m_misname` +0x184 text says "irq status" | 9/9 | **19/20** | 18/19 | D2n (text clause) |
| j | `m_latchrd` the +0x18c latch cleared by its read | 9/9 | **19/20** | 18/19 | D3n (n=2) |
| + | `m_fiqleak` +0x280 READ returns `fiq_enable` | **8/9** | **18/20** | 18/19 | A4 (0xc0), D4s, D5s |
| + | `m_fiqraw` +0x280 READ drops the `&` | 9/9 | **20/20** | 18/19 | **NOTHING — TOTAL ESCAPE** |

**Three distinct total escapes, one of them the brief's own Q2(c), and one of them the exact
"aggregate boolean" hazard the brief names and then ships a row set blind to.**

### 3.4 THE REPAIR FOR THE SHARED-LATCH CLASS, MEASURED — one extra arm, 0.4 s

The D rows cannot see a shared latch because **each one runs in its own process**, so the latch
state never crosses sites. Touch all five sites in ONE process and count:

| build | announcements over the five sites in one process |
|---|---|
| the fix | **5** (all five texts, distinct) |
| `m_sharebit` | **4** — RED |
| `m_onebit` | **1** — RED |

Register state in that arm is unchanged in every build (+0x180, +0x184, +0x280, +0x284 all 0,
+0x188 still 0x30), so the arm adds a count channel and no value risk. A two-arm form (IRQ pair,
FIQ pair) also works and was measured — `X1n` reds at n=1 under `m_sharebit` — but the single
five-site arm is one launch instead of two and catches `m_onebit` as well.

**This is the row I would require before the fix ships.** By the project's own floor it is a
clause-(d) breach: `warned_access` is a predicate the fix DEPENDS ON, a shared bit is the
least-restrictive form that still reads like the same check, and it sweeps the table.

### 3.5 WHAT I WOULD NOT TRY TO FIX IN THIS ROUND, and why

`m_swallow` and `m_fiqraw` escape because their channels are **constant by construction**, not
because a row is missing: `irq_status` is unreachable from a stepped guest and `fiq_status` has no
writer at all. Making A1 and A4 non-vacuous for the read EXPRESSION needs either a free-running arm
with a delivered timer interrupt (a load-sensitive wall-clock oracle, which the sites probe's own
header refuses on purpose) or an offline differential that drives `footbridge_interrupt_assert()`
directly — rung 1, a detector not a witness. **The honest disposition is clause (e): say in the
probe header that A1/A2/A4/A5 pin the value 0 and catch a WIDENING (`&`→`|`, `odata = enable`), and
do NOT claim they pin the expression, because `irq_status`/`fiq_status` are 0 on every path this
probe can reach.** That sentence costs two lines and converts three escapes into stated
non-coverage.

---

## 4. THE HARNESS LEGS' PREMISE — `s9_legs.out`, `s10_legmut.out`

Three launchers, replicated verbatim from the three files (the only change is that the emulation
name is a parameter, which is what a K1 leg needs):
`footbridge_sites_probe.py`'s nested closure inside `run_arm` (`:182-235`), `fbpending_drain_probe.py`'s
`class Session` (`:286-351`), `fbpending_witness.py`'s `class Session` (`:210-278`). The only
difference between the families that matters here is the wait deadline: the sites closure is
TOTAL-time, the two Sessions are INACTIVITY (`if len(self.buf) != seen: seen = ...; t = time.time()`).

### LEG K1 — launch with an unused `-E` name

| launcher | `wait()` | elapsed | reaped | everything the child wrote |
|---|---|---|---|---|
| S (sites) | **False** | 0.00 s | **exited, code 1** | `Sorry, emulation "nosuchmachine" is unknown.` / `Use the -H command line option to get a list of available types and subtypes.` |
| D (drain) | **False** | 0.00 s | **exited, code 1** | identical, 125 bytes |
| W (witness) | **False** | 0.00 s | **exited, code 1** | identical, 125 bytes |

Negative control, same leg, `-E cats`: `wait() -> True`, prompt reached, the diagnostic absent,
`K1 PASS-SHAPE=False`. (In that control my simplified `reap()` closes the master without draining,
so it reports `signal=1` — that is MY harness's SIGHUP, not a product death; the real probes'
`close()` drains to EOF first and labels it `HARNESS-CLOSE(1)`.)

**All three launchers deliver the leg, the diagnostic names the offending input, and the status is
`WIFEXITED && WEXITSTATUS == 1`.** The stream is the pty, so the diagnostic arrives on the same fd
as stdout — no separate stderr handling is needed, and none of the three probes has any.

### LEG K2 — a verified prologue, then `quit`, then the next ordinary interaction

| launcher | prologue verified by a FRESH `reg` | `send("quit")` | the NEXT `send("reg")` | reaped |
|---|---|---|---|---|
| S | **True** — r3=0x1136 (MMU bit 0 = 0), r5=0x11223344, r6=0x1011 | False in 0.01 s, `dead=True` | **False in 0.00 s, `dead=True`** | **exited, code 0** |
| D | **True** — same three values | False in 0.01 s, `dead=True` | **False in 0.00 s, `dead=True`** | **exited, code 0** |
| W | **True** — same three values | False in 0.01 s, `dead=True` | **False in 0.00 s, `dead=True`** | **exited, code 0** |

**Yes, it is observable through `send()`/`wait()` exactly as written, and it is instant** — no
timeout is consumed. The path, quoting the helper I checked (`footbridge_sites_probe.py:225-235`,
and the two Sessions are the same shape):

```python
def send(x, timeout=60):
    b = (x + "\n").encode("latin1")
    _mark = len(buf)
    n = 0
    try:
        while n < len(b):
            n += os.write(fd, b[n:])
    except OSError:
        dead[0] = True
        return False
    return wait(mark=_mark, echo=x if x else None)
```

The write to the master still succeeds after the child is gone; it is the next `rd()` inside
`wait()` that takes `OSError` (EIO) or a zero-length read, sets `dead[0] = True` and returns False,
so `wait()` returns False and `send()` returns False. **`dead` is set BEFORE any cleanup**, which is
what the leg needs.

### The leg mutants (Q2 h, i) — measured, and both matter

**Q2(h) — "K1 passing on ANY nonzero exit".** I ran five different startup refusals through the
launcher:

| refusal | prompt | exit | first line |
|---|---|---|---|
| `-E nosuchmachine` | False | **1** | `Sorry, emulation "nosuchmachine" is unknown.` |
| no file argument | False | **1** | the normal banner (the refusal comes later) |
| `0x8000:/no/such/file.bin` | False | **1** | the normal banner |
| `--no-such-option` | False | **1** | `./gxemul: invalid option -- '-'` |
| `-M notanumber` | False | **1** | `Bad -M argument 'notanumber': must be an integer between 1 and 1048576` |

**All five are `no prompt` + `exit 1`.** So Q2(h) is right that "any nonzero exit" proves nothing —
and so does "exit == 1", and so does "no prompt". **The ONLY discriminator is the diagnostic text
plus the offending name**, and note two of the five print the ordinary banner first, so the leg must
search the whole buffer, not the first line. Codex M1's spec (no prompt AND the unknown-emulation
diagnostic naming that input AND `WIFEXITED && == 1`) is exactly right, and the text clause is the
one doing all the work.

**Q2(i) — "K2 passing when the child died BEFORE the prologue completed".** Driven on the kept
pre-fix binary with a terminating `+0x18c` read inside the prologue:

| build | prologue completed | fresh `reg` | next-send fails | `dead` | exit |
|---|---|---|---|---|---|
| PRE-FIX (dies at +0x18c) | **False** | **False** | **True** | **True** | **1** |
| FIXED (survives) | True | True | True | True | **0** |

**The two clauses a naive K2 would assert — "the next interaction fails" and "`dead` is set" — are
IDENTICAL in both rows.** Only `exit == 0` and the fresh-`reg` prologue verification separate them.
A K2 missing either is satisfied by a child that died at the first device access — i.e. **it goes
green precisely when the round's fix has failed**, which is the worst available direction.

---

## 5. RESTORE — `s11_restore.out`, `s13_final.out`

```
restored from  git -C GXEMUL-SEC show HEAD:src/devices/dev_footbridge.c   (the repo, never a local backup)
PART 1 OK: source cmps clean against HEAD
  and all six other restored src/ files still cmp clean against HEAD
PART 2 OK: binary newer than source        (rm objects; make -j6; MAKE_RC=0)
  binary 2026-09-19 07:18:14   source 2026-09-19 07:18:11
md5 gxemul == md5 out/gxemul_HEAD  ->  7f3293e48f924cf09822bbdd3e20c016  (identical, both ways)
shipped sites probe on the restored build: ROWS=19 of 19  FOOTBRIDGE_SITES_PASS
.MUTANT cleared only after both parts verified -> absent
```

---

## Q1 — PREMISE AUDIT

### (a) The datasheet direction, per site; and is member 3 right for each?

**Verified against `_scratchpad/dc21285.txt` rather than taken from the brief, and calibrated**, per
the carrier's rule that a single calibration point is only valid for a uniform stagger. Table 7-10
(`:6821-6833`) is NOT staggered — `188h  IRQEnable  IRQEnableSet` pairs correctly, confirmed
independently by the prose at `:6804` (*"Enable and EnableSet share the same address for reads and
writes respectively"*) and by the shipped, working `case IRQ_ENABLE_SET`. `288h` gives a second
calibration point below the FIQ rows. So I have calibration points straddling every row I cite.

**And there is a single PROSE sentence covering all five at once, which the brief does not quote —
`:6803`:**

> *"The Status and RawStatus are read-only, and EnableClear and Soft are write-only."*

| site | direction under test | datasheet | member 3 right? |
|---|---|---|---|
| 180h IRQStatus | WRITE | read-only — `:6803`; 7.3.29 `:6886-6888` *"This read-only register is a bit-wise AND of RawStatus and IRQEnable"*; Table 7-10 write column `--` | yes |
| 184h IRQRawStatus | WRITE | read-only — `:6803`; `:6903` *"The IRQRawStatus and FIQRawStatus read-only registers"*; Table 7-10 `--` | yes |
| 18Ch IRQEnableClear | READ | write-only — `:6803`; 7.3.33 `:6937-6947` *"This write-only register is used to clear bits in the IRQEnable/FIQEnable register"*; Table 7-10 read column `--` | yes, **but see the sibling finding** |
| 280h FIQStatus | WRITE | same 7.3.29, same table row | yes |
| 284h FIQRawStatus | WRITE | same `:6903`, same table row | yes |

**Member 4 (ACCEPT) is not available at any of the five.** Four are writes with nothing computed;
the fifth computes `d->irq_enable`, but that is 188h's documented answer, and handing it out at 18Ch
is the leak `m_leak18c` models — the brief and codex M2 are right to delete the assignment.

**Member 5 (FAULT) is NOT AVAILABLE ON ARM AT ALL.** `src/cpus/memory_rw.c:603-625` dispatches an
architectural exception on a failed device access under `#ifdef MEM_MIPS` and `#ifdef MEM_M88K`
**and nothing else** — there is no `MEM_ARM` arm, so `return 0` from an ARM device yields
`MEMORY_ACCESS_FAILED` with no abort delivered to the guest. `dev_unreadable.c` (whose whole access
function is `return 0;`) is installed ten times by `machine_sgi.c` and zero times by any ARM
machine. This is the carrier's Alpha finding recurring on a second architecture: **check the member
is available on this CPU before choosing it.**

**Member 2 (silent) has a live in-file precedent for one of the five, and it is the twin of 18Ch.**
See the sibling finding under "Other things found" — `case FIQ_ENABLE_CLEAR` (28Ch) has no `else`,
so a READ of the FIQ EnableClear register **already declines silently and returns 0 today**,
measured. Member 3 at 18Ch and member 2 at 28Ch is a new asymmetry in a register pair the datasheet
calls identical (`:6801` *"The control registers for the nFIQ and nIRQ control are identical"*).
I do not think that sinks member 3 — a diagnostic on the first undefined-direction access is worth
having — but **the round owes a sentence saying which way it went and why**, and the cheapest
resolution is to give 28Ch the same latched announce in the same commit (one more arm, one more
bit; it is the same class and the same file).

**The value 0 for a declined READ is an INFERENCE, not a quotation.** `:1651-1653` is about a
**nonexistent** CSR (*"If a nonexistent CSR is selected within the CSR address range, zeros are
read"*), and 18Ch is an EXISTING write-only CSR. I searched for a sentence that covers reading a
write-only register and the nearest is `:6836`, which is about **reserved BITS** (*"Unused bit
positions are reserved for future use and read as 0 for read-only registers, and must be 0 for
write-only registers"*) — it does not reach the case. 0 is the right engineering answer (Figure 7-2
at `:6814` shows only RawStatus driving the CSR read path, so nothing drives D[31:0] for 18Ch) and
it matches what the model already does for 28Ch/190h/290h, but **the round should state it as the
fork's own convention with the nonexistent-CSR sentence as the analogy, not as the datasheet's
requirement.**

### (b) One `warned_access` bit-field vs five `int` latches

**The brief's framing ("the file's existing style") has no referent — the file has no latch of any
kind.** Measured: `grep -n -e 'static int' -e 'warn' -e 'once' src/devices/dev_footbridge.c`
returns nothing at all.

Recommend the **bit-field**, and the collision hazard is measured rather than assumed. The carrier's
version of this question is *"who else writes this field, and can they set my bit?"* — the check
that the guard-field/body-field grep cannot do. Answer, in the shipped fix:
`grep -c 'warned_access |=' -> 5`, all five inside `DEVICE_ACCESS(footbridge)`, each with a distinct
constant, and **no read of the field outside its own `if`**. That is materially safer than the
`#490` case the carrier records (8 `|=` sites, 6 of them set by ordinary guest register reads):
here no benign traffic can set any bit, because the only writers ARE the five declines.

The real hazard is the opposite one, and it is what my table measured: a **duplicate or shared
constant** is invisible to the proposed rows. The structural defence the carrier already prescribes
for exactly this (`#447`'s `SH4_VAL_*` conversion) applies — make the five an `enum` ending in a
`_NBITS` so a duplicate is impossible by construction — **and the five-site arm catches it
empirically if it is not.** I would take both; the arm costs 0.4 s and the enum costs nothing.

### (c) Do the K1/K2 legs establish what the old kill arm established, in each of the three launchers?

**Yes for both, in all three, measured — and "observable through `send()`/`wait()` as written" is
confirmed with the helper quoted above (`footbridge_sites_probe.py:225-235`).**

What the old arm established was two things: *the harness can DETECT a host death* and *it can
detect one that happens AFTER guest steps*. K1 covers the first — a child that exits before the
prompt is detected as no-prompt-with-status-1-and-a-naming-diagnostic. K2 covers the second, and
covers it better than the old arm did in one respect: the old arm's death came from the product, so
it could only ever prove the harness noticed a death it did not cause; K2's `quit` proves the same
detection path **with a known-good child**, and the fresh `reg` proves the guest really executed
first. The two together also pin something the old arm never did — that a surviving arm reaps
**exit 0** rather than merely "not 1".

One caution, from the S launcher specifically: its initial `wait` is a **TOTAL-time** deadline, so
`False` after 120 s is also what a HUNG child returns. K1 must therefore never rest on
`wait() == False` alone; with the text and status clauses it does not.

### (d) After this round, is "no footbridge access these probes make ends the process" TRUE?

**Enumerated, not reasoned.** `grep -n 'exit(' src/devices/dev_footbridge.c` at HEAD gives thirteen
hits, of which **four are inside comments** (`:244`, `:449`, `:590`, `:665` — each one a
de-fatalisation quoting the call it removed). The live sites are **NINE**:

| line | site | reached by a guest access? | after this round |
|---|---|---|---|
| 565 | IRQ_STATUS write | yes, +0x180 W | **gone** |
| 574 | IRQ_RAW_STATUS write | yes, +0x184 W | **gone** |
| 606 | IRQ_ENABLE_CLEAR read | yes, +0x18c R | **gone** |
| 615 | FIQ_STATUS write | yes, +0x280 W | **gone** |
| 624 | FIQ_RAW_STATUS write | yes, +0x284 W | **gone** |
| 714 | SDRAM_BA_MASK read | yes, +0x100 R | **stays** (`fbsdrampair`) |
| 739 | SDRAM_BA_OFFSET read | yes, +0x104 R | **stays** (`fbsdrampair`) |
| 843 | DEVINIT | no — construction time | stays |
| 879 | DEVINIT | no — construction time | stays |

**So the statement is TRUE for the three probes as written, and only because none of them touches
+0x100/+0x104.** It is a fact about the probes' current programs, not about the device: one added
`ldr rN,[r0,#256]` would end the process again. The precise form for the record is *"no footbridge
access ANY of the three probes makes ends the process; two guest-reachable terminating reads remain
at +0x100/+0x104 and are `fbsdrampair`'s."*

**The brief says TEN and it is NINE.** Its own list names nine line numbers (565, 574, 606, 615,
624, 714, 739, 843, 879) under the word "ten", and the project's own deriver agrees with the list:
`python tools/pipeline/exit_census.py` prints `dev_footbridge.c   9`. A count that will be quoted
into a CHANGELOG should be re-derived rather than carried.

### (e) Does anything read the five complaint texts, or `ENABLE CLEAR`?

Measured by grep across the tree (excluding `.git`, `artifacts`, objects):

| text | consumers outside `dev_footbridge.c` |
|---|---|
| `ENABLE CLEAR` | `footbridge_sites_probe.py:402`, `fbpending_drain_probe.py:612`, `fbpending_witness.py:489` — plus CHANGELOG/ledger/matrix (records only) |
| `irq_raw_status` | **none** |
| `fiq_raw_status` | **none** |
| `write to irq status` | **none** |
| `write to fiq status` | **none** |

Plus **`gate_arm.sh:1104-1105`**, which pins the count of green K1 rows:

```
check "footbridge: the one-instruction kill arm still dies" \
      "$(grep -cE '^K1 .*ok$' "$FBLOG")" "1"
```

That is the gate check the round replaces. Nothing else in the tree depends on any of the five
texts, so **adding ` (once)` to all five breaks nothing** — the three probes' `in s.buf` /
`in f for f in K["fatals"]` substring tests all still match the new text (measured: the sites
probe's K1 line printed the `(once)` form while reddening on exit status).

`gate_hygiene.sh` is NOT coupled: its flood ceiling grades the **pmax and arc** pty logs
(`:827-828`), and neither machine constructs a footbridge. Its probe-code census counts probe
FILES, not diagnostics.

---

## Q2 — THE CANDIDATE WEAKENINGS: which row reds first, or escapes

Every row in this table was built and run (§3.3). "first" = the row with the lowest id among those
that redden; all reds within a variant are listed.

| | weakening | result |
|---|---|---|
| **a** | `exit(1)` kept at ONE of the five (+0x284) | **D5s reds first**, then D5r/D5e/D5n — the whole arm goes HOST-DIED, so all four of its rows fail together. Robust. |
| **b** | the announce unlatched | **D1n reds first**, and all five count rows red (n=2 where 1 is wanted). Robust, and the only channel that sees it. |
| **c** | one latch bit shared by two sites | **NOTHING REDS. 29/29 — TOTAL ESCAPE.** The D rows run one site per process. Repair measured: the five-site arm, `Z1n` = 4 instead of 5. |
| **c'** | one bit shared by ALL FIVE (the "aggregate boolean") | **NOTHING REDS. 29/29 — TOTAL ESCAPE.** `Z1n` = 1 instead of 5. |
| **d** | +0x18c decline keeps `odata = d->irq_enable` | **D3s reds first** (0x30 instead of 0), D3r too. Robust — and this is the row that justifies deleting the assignment. |
| **e** | a WRITE decline stores the value into irq_status | **D1s reds first** (0x10 instead of 0), D1r too. Works because 0x10 is inside the 0x30 enable; **with the brief's 0x10 against fiq_enable 0xc0 the FIQ equivalent would move only D4r/D5r, not the `& enable` channel.** Use 0x40 for the FIQ arms. |
| **f** | the decline swallows the legal direction (+0x180 READ returns 0 always) | **NOTHING REDS. 29/29 — TOTAL ESCAPE.** A1 wants 0 and gets 0, because `irq_status` is 0 on every path a stepped probe can reach (measured with an armed timer). A1 still catches a WIDENING (`&`→`|`) and `odata = irq_enable`; it cannot catch a NARROWING to a constant. Clause (e) disclosure, not a new row. |
| **g** | the announce text misnames the register | **D2n reds** — the count row's text clause. It is the only thing that looks at the text, so the row must assert the text and not just the count. |
| **h** | K1 passing on ANY nonzero exit | **Measured non-discriminating: five different startup refusals all exit 1 with no prompt.** So does `== 1`. Only the diagnostic text + the offending name discriminates; and the search must cover the whole buffer, since two of the five print the banner first. |
| **i** | K2 passing when the child died before the prologue | **Measured: `next-send fails` and `dead` are IDENTICAL in both rows.** Separated only by `exit == 0` and the fresh-`reg` verification. Both clauses load-bearing; without them the leg greens exactly when the fix failed. |
| **j** | the latch cleared by the read it announces | **D3n reds** (n=2). Robust. |
| **k** | the legs implemented in one launcher only | Not a row in the detector at all — nothing in the 29 rows looks at the other two probes. Caught only by the GATE pinning a leg row per probe. See Q4. |

**Summary: 8 of 11 weakenings are caught by the proposed rows; 3 escape completely, and one of the
three is the brief's own (c).**

---

## Q4 — THE HARNESS CHANGE'S OWN RISK

**The smallest edit to the LEGS that leaves them green while proving nothing** — measured, not
guessed:

> **Delete the fresh-`reg` prologue verification from K2 and score it on
> `next-send fails AND dead`.** That is a two-line deletion. It stays green on a correct build, AND
> it stays green on the PRE-FIX binary whose child died at the first device access — I measured both
> rows and the two clauses are bit-identical. **It is green when the round succeeded and green when
> the round failed.**

Runner-up, one token smaller: **score K1 on `exit != 0`** (or on `exit == 1`). Measured green under
five unrelated startup refusals, including a typo'd command-line option and a bad `-M` value. A
future edit that breaks the probe's invocation entirely would leave K1 green.

Third, and the one a reviewer is least likely to see: **implement both legs in the sites probe only
and leave the drain's and witness's K rows deleted rather than replaced** (Q2 k). Nothing in the
sites probe's 19 rows and nothing in the other two probes' own row sets observes that. The gate is
the only thing that could, and only if it pins a leg row **per probe**.

**The row I expect to stay green under every one of these is `I1` — "isolation arm SURVIVES
untouched"** — together with the whole value block `C1 C2 C3 C4 A1 A2 A2b EC1 EA1 E0 E1 E2 E3 E6 E5
E4 D1`. Measured: those eighteen rows were green in all eleven kill-table variants, including the
three total escapes. **The value rows cannot see a harness defect, and after K1 retires there is no
row left in that probe that observes the harness's own failability at all** — which is precisely why
the legs have to be pinned by the gate, with a check per probe, and why the gate check must key on
the leg's DISCRIMINATING clause (the naming diagnostic; the exit-0 reap) rather than on the row
existing.

Concretely, replacing `gate_arm.sh:1104-1105`'s one check with two that would each have caught one
of the above:

```
check "footbridge: K1 startup leg names the rejected -E input"  <count of the K1 row green>  "1"
check "footbridge: K2 quit leg reaps exit 0 after a VERIFIED prologue"  <count of the K2 row green>  "1"
```

and the same pair in each of the three probes' gate sections, so Q2(k) cannot pass.

---

## Q3 (not asked of me, but I found something) — OPTION-SET COMPLETENESS

**Grepping the fork for the sibling handlers' dispositions, as the option-set rule says to do,
turned up a member already shipping in the same switch for the same register class.**

Measured on the committed HEAD build (`s12_sibling.out`), reading each of the interrupt
controller's other write-only registers TWICE:

| offset | register | direction under test | what HEAD does | announces over two accesses |
|---|---|---|---|---|
| 18Ch | IRQEnableClear | READ | `fatal()` + **`exit(1)`** | 1, then the process ends |
| **28Ch** | **FIQEnableClear** | **READ** | **silent decline, returns 0** | **0** |
| 190h | IRQSoft | READ | `default:` — `[ footbridge: read from 0x190 ]`, returns 0 | **2 (unlatched)** |
| 290h | FIQSoft | READ | `default:` — `[ footbridge: read from 0x290 ]`, returns 0 | **2 (unlatched)** |

`case FIQ_ENABLE_CLEAR:` is `if (writeflag == MEM_WRITE) d->fiq_enable &= ~idata;` with no `else`,
so a read falls through to the common tail with `odata` still 0 — **member 2, already in the file,
at the exact FIQ twin of the site this round is fixing.** The brief names the `default:` arm as a
thing not to copy by accident and does not mention 28Ch at all.

That gives the interrupt controller **four different dispositions for the same question** once this
round lands (terminate → latched announce at 18Ch; silent at 28Ch; unlatched per-access at
190h/290h). The SIBLING PARITY row of the pre-table check is what this is for, and I would put the
finding in the round's `PRETABLE.out` with a decision: either give 28Ch the same latched announce in
this commit (one bit, one arm, same file, same class — it satisfies the reopening rule's "same
device, same semantic class, same detector, one fix design") or write down why the twin stays
silent.

**A second, separate defect surfaced by the same arm, filed not fixed:** a **LEGAL** write to 190h
(IRQSoft — the datasheet's documented write direction, `:6952-6960`) prints
`[ footbridge: write to 0x190: 0x10 ]` on **every access**, unlatched, and does nothing. That is a
documented register announced as unknown — member 7 (IMPLEMENT) territory, and a guest-drivable
unlatched log flood in its own right. Same for 290h. Not this round.

---

## OTHER THINGS FOUND WHILE VERIFYING

1. **`d->fiq_status` has no writer anywhere in the tree**, and `d->fiq_enable`'s only read is the
   AND against it. So the entire FIQ side of this device is state with no observable consequence,
   and `m_fiqraw` proves it: dropping the `&` at +0x280 is undetectable. Worth a filed row of its
   own (the FIQ path is unimplemented, not merely unrowed).
2. **HEAD is `f685d75`, not `9c28ca5`** — a records-only commit landed on top. `dev_footbridge.c`
   and `footbridge_sites_probe.py` are byte-identical between the two (`git diff --stat` empty), so
   nothing I measured changes; but the brief's stated HEAD is one commit stale and a pass-2 brief
   citing it will be two behind.
3. **`regress/gate_arm.sh` carries +67 uncommitted lines** against HEAD in the working tree. The
   round plans to edit its footbridge section.
4. **The two offline differentials build their own device instance with `calloc`**, not through
   DEVINIT (`diff_footbridge.c:151`, `diff_fbpending_bound.c:143`). Both zero the new field, so both
   are safe — but "cleared by DEVINIT's memset" names one of two zeroing paths.
5. **The brief's D4/D5 write value (0x10) does not intersect its own FIQ enable mask (0xc0)**, so
   the `& enable` channel at +0x280 cannot move under a store-into-`fiq_status` mutant. 0x40 fixes
   it at no cost. (The IRQ pair is fine: 0x10 is inside 0x30.)
6. All five complaint texts are distinct, and **adding ` (once)` breaks no consumer** — the three
   probes use substring tests that still match, and they redden on the status and exit clauses
   instead, which is the intended behaviour.

---

## SEAT RECORD

**Model.** Claude Opus 5 (1M context), the measuring seat, pass 1 of `fbdeclinefive`.

**What I read.** `_scratchpad/fbd5/brief_fbd5_design_BUILT.md`; `_scratchpad/CHECKPOINT.md` (first
line); `GXEMUL-SEC/src/devices/dev_footbridge.c` (whole file, at HEAD);
`src/include/thirdparty/dc21285reg.h`; `src/cpus/memory_rw.c:596-632`;
`src/machines/machine_cats.c` (device list); `regress/footbridge_sites_probe.py` (whole file);
`regress/fbpending_drain_probe.py` and `regress/fbpending_witness.py` (the `Session` classes and
the `run_kill`/`row` blocks); `regress/diff_footbridge.c` and `regress/diff_fbpending_bound.c`
(include and allocation only); `regress/gate_arm.sh` and `regress/gate_hygiene.sh` (footbridge
sections); `tools/pipeline/exit_census.py` (header, then ran it);
`_scratchpad/dc21285.txt:1645-1660, 6795-6960`; my own previous seat's
`regress/artifacts/n6/opus_p1_20260919/opus_e.py` and `s_build.sh` as the starting shape.
**I did not open** `regress/artifacts/` beyond that one directory, `tools/pipeline/ledger.json`,
`CHANGELOG.md`, `OUTSTANDING_BUGS.md`, or `_scratchpad/r6pass2_fb/`.

**What I ran.** Everything in the foreground, everything in `/tmp/gxopusfbd5` (a `cp -a` of
`build/`), invoked as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/<script>` with script files
under `_scratchpad/fbd5/opus_p1_20260919/`. 15 emulator builds (1 baseline, 13 variants, 1 restore),
~40 cold-debugger launches, ~0 seconds of background work.

| script | log | what |
|---|---|---|
| `s1_clone_build.sh` | `s1_clone_build.out` | clone, restore 6 dirty src files to HEAD, `rm *.o gxemul`, `make -j6`, freshness, stub |
| `s2_witness.sh` | `s2_witness_HEAD.out` | the five witness arms, pre-fix |
| `s3_accept.sh` | `s3_accept_HEAD.out` | the accept side, pre-fix |
| `s4_fix.sh` | `s4_fix_apply.out` | sentinel, restore, apply member 3, full diff, rebuild |
| `s5_run.sh` | `s5_postfix.out` | witness + accept + decline + the shipped sites probe, post-fix |
| `s6_table.sh` | `s6_table.out` | the 11-variant weakening table (frozen copies of probe and patcher) |
| `s7_cross.sh` | `s7_cross.out` | the cross-site arms and the timer-seed arm |
| `s8_all5.sh` | `s8_all5.out` | the five-sites-in-one-process arm vs `m_sharebit` and `m_onebit` |
| `s9_legs.sh` | `s9_legs.out` | legs K1 and K2 through all three launchers + the K1 negative control |
| `s10_legmut.sh` | `s10_legmut.out` | Q2(h) five startup refusals; Q2(i) the dead-before-prologue row |
| `s11_restore.sh` | `s11_restore.out` | restore from SEC, two-part clearance, rebuild, sites probe 19/19, sentinel cleared |
| `s12_sibling.sh` | `s12_sibling.out` | 190h / 28Ch / 290h sibling parity on HEAD |
| `s13_final.sh` | `s13_final.out` | final clone state |

Harnesses written: `opus_w.py` (the arm driver and row scorer), `mkfix.py` (the fix and 11 mutants,
each replacement refusing unless it matches exactly once), `legs.py`, `legmut.py`. Frozen copies
were used for every table run, so the originals stayed editable while jobs ran.

**The clone's final state.** `/tmp/gxopusfbd5`: `src/devices/dev_footbridge.c` **cmps clean against
`GXEMUL-SEC` HEAD**; the other six restored files cmp clean; `gxemul` rebuilt after the restore,
newer than its source, and **md5-identical to the HEAD binary kept aside before the mutants**
(`7f3293e48f924cf09822bbdd3e20c016`); `.MUTANT` absent, cleared only after both parts verified; the
shipped sites probe reads `19 of 19 / FOOTBRIDGE_SITES_PASS` on it. **`GXEMUL-SEC/`, `est/`,
`build/`, `build-asan/` and `/tmp/gxsec-build` were not written. No `regress/gate_*.sh` was run.**
