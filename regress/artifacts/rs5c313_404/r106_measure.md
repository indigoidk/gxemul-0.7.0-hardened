# #106 — dev_rs5c313.c: measure seat (compile-and-execute)

Everything below was produced by building the **real** `DEVICE_ACCESS(rs5c313)` and
`DEVINIT(rs5c313)` offline and running them. Nothing was transcribed. No file under
`GXEMUL-SEC` or `est` was touched and no gate was run.

**Rig** (`_scratchpad`-external, in the session scratch dir
`…/cc4a27b6-…/scratchpad/r106/`): the `regress/diff_sh4_tmu.c` shape — stub the
collaborators, `#include` the device `.c`, so the function that runs is the function that
ships. Same flags as `regress/gate_offline.sh:283-285`:

    gcc -O2 -std=c99 -I$SEC/src/include -I$SEC/src/include/thirdparty \
        -ffunction-sections -fdata-sections -Wl,--gc-sections

Stubs: `memory_readmax64` / `memory_writemax64` (bodies from `src/core/memory.c:55-78`
and `:88-108`; leaf functions whose only emulator input is `cpu->byte_order`),
`memory_device_register` (captures `extra`), `fatal`, `debug`. `config.h` resolves as
`src/include/../../config.h` → `GXEMUL-SEC/config.h`, which exists, so the real
`-I` path works with no scratch header layout.

**Determinism** — the answer to "any test that samples host time twice can race a second
boundary". `<time.h>` is included and the fakes are defined **first**, then

```c
#define time(x)   rig_time(x)      /* returns a variable I set */
#define gmtime(x) rig_gmtime(x)    /* the REAL gmtime, on a value I control */
#include DEVFILE
```

`dev_rs5c313.c:41`'s own `#include <time.h>` is then a guarded no-op. The host wall clock
is read **zero** times across the whole 62-row table and the 480 000-access differential.
This needs **no production change** — no injectable clock hook has to be added.

---

## TASK 1 — reproduction. Both halves CONFIRMED, one of them more strongly than claimed.

`dev_rs5c313.c:96` calls `rs5c313_update_time(d)` before the dispatch at `:99-105`.

### Half (a): a write clobbers the other twelve — CONFIRMED, 12/12

Freeze the clock at a named instant (1996-12-19 16:39:57 UTC). After `DEVINIT` all
thirteen time registers are 0 (`dev_rs5c313.c:116`), so any non-zero value afterwards came
from `update_time`. One single-byte write of `9` to `SEC1`:

```
before:  all 13 time regs = 0
after:   SEC1=9 SEC10=5 MIN1=9 MIN10=3 HOUR1=6 HOUR10=1 WDAY=4 TINT=0
         DAY1=9 DAY10=1 MON1=2 MON10=1 YEAR1=6 YEAR10=9  CTRL=4 TEST=0
```

All **twelve** non-target time registers went 0 → host digit. The written register does
survive the refresh (it is stored at `:101`, after `:96`). Brief's description is exact.

### Half (b): a read can only ever return host time — CONFIRMED, and it is stronger than "the write is lost later"

With the clock **frozen** — zero elapsed time between the write and the read — a write of
`9` to `SEC1` reads back `7` (the host digit). The write is invisible at the very next
access, not merely eventually.

### Which registers survive at all

Write `0xf` to each of the sixteen, read it back. `R4_survivor_mask = 49280 = 0xC080` —
bits 7, 14, 15, i.e. exactly **`TINT`, `CTRL`, `TEST`**, the three `update_time` never
writes. The other thirteen are all lost.

### "Does a guest that writes all thirteen end with a coherent time, a mixture, or host time?"

**Both, at different moments — and this distinction turns out to be the whole round.**

* *In the register file*, immediately after the 13th write: **an incoherent mixture** —
  12 host digits + the one just written. A time that never existed.
* *As the guest can observe it*, on read-back: **13/13 host time.** The mixture is never
  visible; every read refreshes first.

A trap for whoever writes the oracle: I first asserted "0 read-back registers match the
value written" and it **failed, correctly** — 1 matched by digit coincidence (Dec **19**
and Sep **9** share `DAY1 = 9`). The sound oracle is the positive one, "13/13 equal host
time", not a count of disagreements.

### Access paths that behave differently — none reachable

The guest never touches this device directly. `machine_landisk.c:93-94` registers it at
`SCI_DEVICE_BASE` = `0x110000000ULL` (`sh4_scireg.h:8`), above 4 GB, and the only two
call sites that ever form that address are the SH-4 SCI bit-bang emulation,
`dev_sh4.c:473-474` and `:494-495`. That path fixes the entire access space:

* `dev_sh4.c:466-467` — `d->sci_cur_addr = cmd & 0x0f` → `relative_addr` ∈ 0..15, so no
  register index can leave `reg[16]`;
* `dev_sh4.c:489` — `data_byte = cmd & 0x0f` → every write carries **4 bits**, so the
  mask at `dev_rs5c313.c:101` is never load-bearing in practice;
* both `memory_rw` calls pass **`len = 1`** — multi-byte accesses do not arise.

I did drive `len = 4` anyway: the store at `:101` writes one byte regardless of `len`, so
there is no overflow, and a 4-byte read leaves `buf[4]` untouched (canary `0xee` intact).
ASAN on the shipped file over the whole table: **clean**. I did not exhaustively audit
SH-4 address translation to prove no guest load can reach `0x1_1000_0000`; I checked that
no other code in the tree produces that address.

---

## TASK 2 — the design question. Offset model: RIGHT SHAPE, NOT IMPLEMENTABLE HERE. Verdict: RECORD.

### "Call update_time only on reads" — refuted, and by more than the brief expected

The brief says that repair leaves the write sticking and the next read clobbering it.
Measured, it is worse than that: it is **completely unobservable**.

`M02_readonly` (the refresh moved into the `else` branch) versus the shipped file, driven
with identical random access sequences over exactly the SCI-reachable space
(`len=1`, `addr` 0..15, 4-bit writes), 600 seeds × 800 steps, start instants spread over
1970..2106 so second/minute/hour/day/month/year boundaries are all crossed:

    248581 reads, 231419 writes, 0 mismatches  ->  DIFFERENTIAL_INDISTINGUISHABLE

Analytically that is forced: every read refreshes before returning, so what a guest can
see is a pure function of host time plus writes to `TINT`/`CTRL`/`TEST`, which
`update_time` never touches. **Moving the call cannot change any guest-visible byte.** By
this project's own standard — a fix whose effect cannot be measured gets documented — the
one-liner is *hygiene*, not a fix, and must not be described as fixing the clobber.

### The sharpest measurement of the round

`M21_writes_ignored` — writes to all thirteen time registers made **no-ops** — is
**also indistinguishable** (same 248 581 reads, 0 mismatches).

> To a landisk guest, the shipped device is already identical to one that silently
> discards every write to a clock register.

So the defect's guest-visible symptom is exactly one thing: **the clock is not settable.**
That is a missing feature, not corruption. The incoherent register file is real but
unobservable.

### Is an offset model needed? Yes — and that is settled by elimination

Nothing short of one makes a clock-set take effect: the register file is rewritten from
`time(NULL)` on every read, so any repair that leaves that intact is defeated on the next
read; and any repair that stops the refresh freezes the clock. The brief's reasoning holds.

### Is there a commit/hold protocol this device ignores? YES — and it is in-tree

`src/include/thirdparty/rs5c313reg.h:63-71`, read directly:

```
#define CTRL_BSY    0x01   /* read  */      #define CTRL_ADJ   0x01  /* write */
#define CTRL_XSTP   0x02   /* read  */      #define CTRL_WTEN  0x02  /* write */
#define CTRL_24H    0x04   /* read/write */ #define CTRL_CTFG  0x08  /* read/write */
#define CTRL_BASE   CTRL_24H
```

There is a **write-enable** bit and an **adjust** bit, and the device ignores both.
Measured (`R13`): setting `CTRL_WTEN` changes nothing — `SEC1` written under WTEN still
reads back host time, and the WTEN 1→0 edge commits nothing.

`RS5C313_TINT` (reg 7) and its `TINT_CT0..CT3` (`rs5c313reg.h:57-61`) are likewise
unimplemented: writes stick and do nothing. No periodic interrupt exists.

### ...but the protocol cannot be reconstructed from this source. This is the RECORD.

What the header supplies is **bit names and read/write direction**. It does not say that
`WTEN` gates writes, what the commit event is (a `WTEN` falling edge? each write?),
whether the counter is held while `WTEN` is set, whether `BSY` must be polled, or how
`HOUR10` encodes AM/PM when `CTRL_24H` is clear. Writing a `WTEN`-edge commit means
**inferring a protocol from bit names** — the exact failure mode that produced the
DDI 0100I citations this project had to retract.

Three further obstacles, each independently sufficient:

1. **The guest driver is not in this tree.** `grep -rl rs5c313` over the whole repo
   returns only the emulator's own files plus `rs5c313reg.h`. Whether OpenBSD/landisk
   sets `WTEN`, in what order it writes, and whether it polls `BSY` are all unknown here.
2. **Guessing is not a safe no-op — measured.** `M22_wten_hold` (hold the clock while
   `CTRL_WTEN` is set) is **guest-DISTINGUISHABLE**: 64 687 divergent reads, first at seed
   0 step 28. A guest that sets `WTEN` and does not clear it would see the clock stop.
   So a wrong guess can regress a currently-booting machine.
3. **The conversion back to `time_t` needs code C99 does not have.** `timegm()` is a
   GNU/BSD extension; `mktime()` is local-time based and wrong here. A hand-rolled
   days-from-civil routine would be required — plus a **century pivot**, because the chip
   has only two year digits and the correct pivot is not derivable from anything in this
   tree.

**No offset infrastructure exists anywhere in the emulator** — `grep` for
`rtc_offset|clock_offset|time_offset` over `src/` returns nothing — so this would also be
the first settable clock in the project.

### The house pattern says the same thing

Every RTC in this tree is a read-only host-clock passthrough, and the two that gate their
refresh do so on a bit their own header documents:

* `dev_mk48txx.c:98-106` refreshes **only** on the 0→1 edge of `MK48TXX_CSR_READ`, whose
  header entry `mk48txxreg.h:101` reads `/* want to read (freeze clock) */` — a documented
  latch. Its comment at `:102-105` says the registers become "froozen".
* `dev_mc146818.c:364` gates its refresh on `MC_REGA`/`MC_REGC` accesses.
* `dev_rs5c313.c:96` is the outlier: unconditional refresh on every access to every
  register.

`rs5c313reg.h` carries no equivalent documented latch, which is precisely why mk48txx
could be implemented and this cannot.

### Recommendation

1. **A RECORD** (source comment + `OUTSTANDING_BUGS.md`): the guest cannot set this clock;
   `WTEN`/`ADJ`/`BSY`/`TINT`/`CTRL_24H` are unimplemented; the write protocol cannot be
   implemented from this source; **and** the measured fact that today's behaviour is
   observationally identical to ignoring writes outright.
2. **A regression table** pinning the current contract (below), so a future round that
   changes any of it does so visibly.
3. *Optional, and must be labelled hygiene:* move `dev_rs5c313.c:96` into the read branch.
   Measured guest-equivalent (0/248 581). It buys a coherent register file and nothing
   else. Shipping it while calling it a fix for the clobber would be a false record.
4. **Do not** implement `WTEN` semantics, 12-hour mode, or a `WDAY` base change from this
   source.

---

## TASK 3 — the mutant table. 23 mutants, all measured.

Method: each mutant is a *generated copy* of `dev_rs5c313.c` (the repo file is never
edited), compiled against the same 62-row table. **A row kills a mutant iff its emitted
value differs from base** — measured, not asserted. Faults are scored separately.

Proposed rows: **R1** devinit state · **R2** registered length · **R3** the 13 exact
digits at three named instants (one pre-2000, two post-2000) · **R4** survivor mask ·
**R5** 13-write set sequence read back · **R6** *internal* file coherence after the set
sequence · **R7** digit sweep 1970..2106 (~170 k samples) · **R8** `CTRL_24H` ignored ·
**R9** `len=4` bounds + canary · **R10** `0xff` write read back · **R11** `0xff` write
*in the file* · **R12** non-UTC `TZ` · **R13** the `WTEN` protocol bit.

| mutant | killed by | note |
|---|---|---|
| M01 delete the refresh | R3,R4,R5,R6,R7,R8,R12,R13 (41 rows) | |
| M02 refresh on reads only | **R6 only** | guest-indistinguishable (0/248 581) |
| M03 `YEAR10 = tm_year/10` | R3(post-2000 only),R7 | **see below** |
| M04 `MON1`/`MON10` operators swapped | R3,R5,R6,R7 | |
| M05 `MON1` loses the `+1` | R3,R5,R6,R7 | |
| M06 `WDAY = tm_wday + 1` | R3,R5,R6,R7 | the plausible "fix" of the TODO |
| M07 drop the **write** mask `:101` | **R9,R11 only** | no guest-visible row sees it |
| M08 drop the **read** mask `:103` | **NOTHING** | see below |
| M09 drop both masks | R9,R10,R11 | |
| M10 `DEV_RS5C313_LENGTH` 16→15 | R2 **+ FAULT** | ASAN heap-buffer-overflow |
| M11 `CTRL_24H` → `CTRL_BASE` | nothing | equivalent by `rs5c313reg.h:71` |
| M12 devinit sets `CTRL_XSTP` | R1 | |
| M13 `gmtime` → `localtime` | R3,R5,R6,R8,R12 | needs R12's non-UTC `TZ` |
| M14 refresh only for regs 7..13 | R3,R4,R8,R12,R13 | |
| M15/M17/M18/M19 redundant `%`/index | nothing | **equivalent — must survive** |
| M16 `DAY10 = tm_mday % 10` | R3,R5,R6,R7 | |
| M20 skip refresh for TINT/CTRL/TEST | nothing | equivalent (0/248 581) |
| M21 ignore writes to the 13 clock regs | **R6 only** | guest-indistinguishable |
| M22 hold the clock while `WTEN` set | **R13 only** | guest-**distinguishable** (64 687) |

### The mutant NO row catches: **M08 — dropping `& 0x0f` at `dev_rs5c313.c:103`.**

It survives all 62 rows *and* the 248 581-read differential. It is undetectable because
the **write**-side mask at `:101` already keeps every byte ≤ 0x0f, so the read mask is
dead code. M07 and M08 are a **compensating pair**: each alone is invisible to every
guest-visible row (M07 needs R9/R11, which read `d->reg[]` directly); together (M09) they
are visible. Any table that asserts only what the guest can read is blind to both.

This is the direct instance of the hazard named in the brief. Two consequences:

* R11 exists *only* to see M07, and R11 asserts **internal state** — reachable solely
  because the rig holds the `extra` pointer. A pure guest-visible table cannot have it.
* M08 stays alive regardless. The honest statement is "M08 is undetectable from behaviour
  and is left uncovered", not a claim of full mutation coverage.

### Second blind spot, deliberately closed: **R13.**

`M22_wten_hold` is killed by **R13 alone**. Without a row that exercises `CTRL_WTEN`, any
future partial `WTEN` implementation passes the whole table silently — while being
measurably guest-visible. That is why R13 is in the table even though it only pins
unimplemented behaviour.

### Third: **M03 dies only on the post-2000 instants.**

`(tm_year / 10) % 10` versus `tm_year / 10` are **identical for every year before 2000**
(`tm_year` ≤ 99 → quotient ≤ 9). My first named instant was 1996 and R3 did not fire on
it; R3 kills M03 only via the 2001 and 2026 instants, and R7 via 132 666 sweep samples.
A table whose named instants are all pre-2000 would miss it.

### Faults, scored separately

**M10 is a FAULT, not a clean kill.** It flips R2, but it also shrinks `reg[]` to 15
bytes while `dev_rs5c313.c:101` still stores at `relative_addr` up to 15. ASAN: `ERROR:
AddressSanitizer: heap-buffer-overflow`. Its R-row differences are produced by undefined
behaviour and must not be read as assertions firing. The shipped file under the identical
table is **ASAN-clean** (the only ASAN exit-1 I saw on the base was *LeakSanitizer*
reporting my own rig's un-freed `devinit` allocations — not a device defect; re-run with
`detect_leaks=0` exits 0).

No mutant crashed or failed to compile.

### A vacuity bug this rig hit, worth carrying forward

The differential renames the variant's symbols by macro before `#include`. Left in force,
those macros **also rewrite `main()`**, so both sides called the mutant and the harness
compared it against itself — it reported `INDISTINGUISHABLE` for `M06`, which plainly
changes a read value. It was caught only because M06 is carried as a **positive control:
a mutant that MUST diverge**. The rig now `#undef`s the four macros after the include and
asserts `dev_rs5c313_access != alt_access` at exit.

> A differential without a positive control cannot detect that it has stopped
> differentiating. Every `INDISTINGUISHABLE` verdict above is only worth the control that
> ran beside it (M06 → 17 396 mismatches, M03 → 11 543, M01 → 177 466, M22 → 64 687).

---

## TASK 4 — the rest of the 127 lines

**Checked and fine:**

* **`YEAR10 = (tm_year / 10) % 10`** (`:87`) is **correct**. It equals
  `(tm_year % 100) / 10` for all `tm_year ≥ 0`. Verified over ~170 k samples from 1970 to
  2105: `YEAR10*10 + YEAR1 == tm_year % 100`, zero mismatches. The `% 10` is load-bearing
  from 2000 on — dropping it yields 12 for 2026 (M03).
* **`MON1 = (tm_mon + 1) % 10`, `MON10 = (tm_mon + 1) / 10`** (`:84-85`) are correct:
  months 1..12 → `MON10` ∈ {0,1}, `MON1` ∈ 0..9. Zero mismatches across the sweep.
* **`DAY`, `HOUR`, `MIN`, `SEC` digits** — zero mismatches across the sweep.
* **`gmtime` vs localtime** (`:70`) is **right and consistent**: every RTC in this tree
  uses `gmtime` — `dev_mc146818.c:191`, `dev_mk48txx.c:64`, `dev_luna88k.c:626-650`,
  `machine_playstation2.c:142`. Changing it would be a cross-tree behaviour change. R12
  (a non-UTC `TZ`) makes the swap detectable.
* **`DEVINIT` defaults** (`:119`): `CTRL = CTRL_24H` leaves `XSTP` (oscillator stopped)
  and `BSY` reading 0 — "clock valid, not busy", the right default for an emulator, and
  the reason a guest may never attempt to set the clock at all.
* **Bounds**: no overflow. `relative_addr` < 16 by construction (`dev_sh4.c:466`), the
  store is one byte regardless of `len`, ASAN clean.

**Genuinely wrong or unimplemented, all RECORD-only:**

* **`CTRL_24H` is accepted and never consulted.** Measured at 13:00 UTC: `HOUR10=1`,
  `HOUR1=3` with the bit set **and** with it cleared — identical. A 12-hour encoding
  cannot be implemented, because nothing in this tree says how `HOUR10` carries AM/PM.
* **`WDAY` (`:79-80`, the upstream TODO) — I cannot verify it, and I recommend not
  touching it.** The only in-tree evidence points the *other* way: both sibling devices
  use one-based (`dev_mc146818.c:196` and `dev_mk48txx.c:69`, `tmp->tm_wday + 1`), and
  `mk48txxreg.h:75` documents `/* weekday (1..7) */` — but that is a **different chip**.
  `rs5c313reg.h` says nothing about `WDAY`'s range. Changing it on sibling analogy is
  exactly the guess this project forbids. The TODO should stay, with the divergence noted.
* **`TINT` (reg 7) and `TINT_CT0..CT3`** are unimplemented; writes stick and do nothing.
* **Two-digit year aliasing**: 2105 reads back as `"05"`, indistinguishable from 2005.
  7 443 of my sweep samples are at/after 2100. This is inherent to a 13-digit RTC with no
  century register, not a code defect — but a guest's pivot decides the result and no
  pivot exists here.
* **Pre-1900 host clock produces non-BCD digits.** C99 truncating division makes
  `tm_year % 10` negative. Measured on the shipped file:

      t=-2240000000 (1899)  tm_year=-1   file YEAR1=0xff  -> guest reads YEAR1=15
      t=-3000000000 (1874)  tm_year=-26  file YEAR1=0xfa YEAR10=0xfe -> reads 10 and 14

  The `& 0x0f` masks keep it in range, so it is invalid BCD, not an out-of-bounds. Only
  reachable if the **host** wall clock is set before 1900 — effectively unreachable, and
  the same expression shape exists in the sibling devices. Note, do not fix.
* **`gmtime()`'s return is dereferenced unchecked** (`:70-72`). It can return `NULL`.
  Unreachable from `time(NULL)` on any sane host, and identical in `dev_mc146818.c:191`
  and `dev_mk48txx.c:64` — a house-wide pattern, not an rs5c313 defect.

---

## What I did NOT verify

* No guest was booted. Every statement about OpenBSD/landisk behaviour is an inference
  from `dev_sh4.c:444-497` and `machine_landisk.c:92-95`, not an observation. In
  particular I did **not** confirm that OpenBSD ever writes these registers at all — the
  reachability of the write path is unmeasured.
* The stubbed `memory_readmax64` / `memory_writemax64` are faithful copies of
  `src/core/memory.c`, not the linked originals.
* The differential is randomized (600 seeds × 800 steps), not exhaustive over sequences.
  The analytic argument for M02/M20/M08 is independent of it; M21's equivalence rests on
  the differential plus the same "every read refreshes first" argument.
* I did not audit SH-4 address translation to prove no guest load can reach
  `0x1_1000_0000`; I only checked that no other code in the tree forms that address.
* The appendix question in the brief (#401/#402/#403) was out of scope for this seat and
  is not answered here.
