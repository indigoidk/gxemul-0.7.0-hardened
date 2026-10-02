OPUS_CRIME_P1_20260913 — the Opus 5 measuring seat's PASS-1 report on `crimewidthkill`, verbatim, saved because an Agent
seat leaves no file in a panel dir.  Brief: _scratchpad/brief_crime_pass1_20260913.md (scriptable seats in
_scratchpad/panel_20260913_000135/).  Every artifact it cites is in this directory.  (The harness rendered `&` and `>`
as HTML entities in the returned text; restored here, nothing else changed.)

---

OPUS_CRIME_P1_20260913

First line of `_scratchpad/CHECKPOINT.md`, verbatim: `# CHECKPOINT -- 2026-09-13 ~00:0x   HEAD 9c91999 (records)   no round in flight`

**VERDICT: member 3, DECLINE + LATCHED ANNOUNCE, with the refused access skipping the `switch` and reaching the common tail.**
- **Measured:** it is the only candidate I built that does all four of these: the host survives, the guest keeps running, no switch side effect fires, and the host prints a diagnostic even when free-running.
- **Reading:** FAULT (member 5) has no transferable warrant. `dev_unreadable` models absent hardware, but CRIME is present. No document establishes that real CRIME bus-errors narrow accesses. And the same machine's CRIME-RE precedent (#497/#499/#513) chose member 3.

The evidence is saved in `GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_pass1_20260913/` (README, 9 witness logs, 9 row logs, diffs, scripts, build logs). Every log ends in its completion sentinel.

---

## What I built and ran (scratch clone only)
- **Clone:** `/tmp/gxopuscrime`, a `cp -a` of `build/`.
  - Its `dev_sgi_ip32.c` compares **clean** against SEC, and so do `memory_rw.c`, `cpu_mips*.c`, `machine_sgi.c`, `crimereg.h` and `dev_unreadable.c`.
  - The baseline was rebuilt in the clone and the binary is newer than the source. The committed witness gives **3/15, CONTROL=OK**, matching `witness_committed.out`.
- **Binaries:**
  - `base` (committed code).
  - `fault`: `return 0;` in place of the kill.
  - `decline`: `warned_len` latch with `(once)` text, then `goto crime_common_tail`.
  - `delete`: member 1, the else-arm removed.
  - Five mutants of `decline`:
    - `return1`: the goto replaced by `return 1`.
    - `fallsw`: the latch kept, the goto deleted.
    - `nolatch`: the latch is never set.
    - `len1only`: the decline conditioned on `else if (len == 1)`.
    - `readonly`: the decline conditioned on `else if (writeflag == MEM_READ)`.
- **Build results:** all built with rc=0 and a fresh binary; every variant differs from base.
- **Clean-up:** the clone was restored from SEC and rebuilt. The restored binary is byte-identical to base, the source compares clean, and the sentinel is cleared.
- **Untouched:** `build/`, `est/` and `build-asan/`. No `build/.MUTANT`; `build/gxemul` still carries its 09-12 12:50 timestamp.
- **Instruments:** each binary ran the committed witness plus my observational probe (`crime_opus_rows.FROZEN.py`, frozen by copy for the whole run).

## Results (MEASURED)

| cell | base | fault | decline | delete |
|---|---|---|---|---|
| committed witness | 3/15 | 15/15 | 15/15 | 15/15 |
| lb/lbu +7, lh/lhu +6; destination seeded 0xdeadbeef | exit 1 | **0xdeadbeef**; pc=0xffffffff80000180, ExcCode 7, EPC = the load | 0x0, pc+4 | 0x0, pc+4 |
| sb +0x37 / sh +0x36 after an accepted `sw 0x0badcafe` | exit 1 | data bus error; word unchanged | word unchanged | word unchanged |
| `sh 0x0800 → +0x08` | exit 1 | data bus error | runs | **"emul: All machines stopped."** |
| `sh 0x0800 → +0x0e` (the lane bit 11 is in) | exit 1 | data bus error | runs | runs; nothing happens |
| `sb 0x01 → +0x08` | exit 1 | data bus error | silent | **`[ CRIME_CONTROL: unimplemented control 0x..01 ]`** (not latched) |
| lb/lh at +0 from pc 0xbfc05180, ra=0x80004000 | exit 1 | data bus error | pc=0xbfc05184 | **pc=0x80004000** (the PROM-probe hack fired) |
| 5 refused accesses in one session | exit 1 | 5 `...failed ]` debug lines | **1 `(once)`** | 5 default-arm debug lines |
| **free-running** (breakpoint + continue), lb +7 | exit 1 | **host prints NOTHING**; guest at vector 0x80000180, ExcCode 7, status 0x34000002 | `(once)` printed; host alive | nothing printed |
| accept cells: sd/ld, lw hi/lo, sw then ld, lw/ld REV | identical in all builds | | | |

- The committed witness gives **15/15 on all eight non-base binaries**. It is survival-only, so it cannot tell any candidate or mutant apart.
- FAULT's only host-side trace is a `debug()` line. It appears while single-stepping and is **suppressed when free-running** (measured). So a bare `return 0` removes the host diagnostic entirely in normal runs.

## Q1: does anything in the tree issue a narrow CRIME access?
**No (READING).**
- No code outside `dev_sgi_ip32.c` references CRIME's address. `machine_sgi.c` only calls `dev_crime_init`, and the ARCBIOS emulation never touches CRIME.
- `-e ip32` runs with PROM emulation. There is no PROM image in the tree, so the CRIME_REV hack matters only for an external real PROM.
- DMA and debugger accesses cannot reach the guard. CRIME is registered `DM_DEFAULT`, and `memory_rw` calls such a device only `if (!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS))`.
- `lwl/lwr/swl/swr` use aligned full-width accesses (`memory_rw(..., aligned_addr, ..., wlen, ...)` in `cpu_mips_instr_unaligned.c`).
- The end-of-device truncation cannot produce a narrow length, because `0x280` is 8-aligned.
- So the refused set is exactly `len ∈ {1,2}`, and it is reached only by guest `lb/lbu/lh/lhu/sb/sh`.
- Guest OS drivers are not in the tree, so what NetBSD, OpenBSD or Linux do is not established here.
- Sibling handlers in the same file: MACE serves any width by byte lane (`memcpy` plus `switch (relative_addr & ~7)`); macepci announces without a latch and proceeds; sgi_ust treats any width as the whole register. None of them faults.

## Q2: which lines run, at HEAD 9c91999 (READING, confirmed by the measurements above)
**Every candidate** runs the prelude first: `dev_sgi_ip32.c:205-267`.
- Writes compute `idata = memory_readmax64(data, len)` at `:211`.
- The REV, CONTROL and INTSTAT registers are refreshed at `:223-229`.
- The RAM-size checks run at `:238-254`, then the bank loop at `:256-267`.

**Decline (my recommendation):**
- The width chain at `:269-274` misses.
- The else-arm runs the latch test; `fatal()` prints only the first time.
- The goto skips the switch at `:295-382` entirely and lands on the tail at `:384-387`. The `HARDINT` restore and the `INTSTAT` recompute are both no-ops, because nothing changed either register.
- A read then runs `:389-390`: `memory_writemax64(data, len, 0)` and `return 1`, and the guest gets 0.
- A write skips `:390`, so its `idata` is computed and never used.

**Fault:**
- The same prelude, then `return 0` skips both the switch and the tail.
- In `memory_rw`, `res 0→-1`, a `debug()` "failed" line, `mips_cpu_exception(DBE)` and `MEMORY_ACCESS_FAILED`. The load returns before `reg(ic->arg[0]) = x`, so the destination is untouched.

**Delete / fallsw:** the switch runs on the exact `relative_addr`:
- `0x000` (REV): on a read, the PC is redirected when pc is in 0xbfc051xx (measured). The case has no writeflag test, so a write should redirect too (READING, not measured).
- `0x008` (CONTROL), writes only:
  - A halfword can hold `0x0800`, so it stops every CPU (measured).
  - A byte cannot reach 0x800, 0x200 or 0x100, so any nonzero byte prints the unlatched fatal (measured).
  - Note that this is the wrong lane: in the 4-byte arm's own big-endian convention, bit 11 lives at `+0x0e`, which goes to the default arm.
- `0x010`/`0x018`: `crime_interrupt_reassert` runs (reading; idempotent).
- `0x038`: the CRIME_TIME update runs (reading).
- The default arm prints `debug()` lines.

## Q3: the smallest edit that breaks the decline and still passes

| edit | committed witness | caught only by |
|---|---|---|
| `fallsw`: delete the goto line | 15/15 (measured) | **switch side-effect rows** |
| `len1only` | 15/15 (measured) | the other width's own-session announce row, `sh CTL+08`, `revhack lh` |
| `readonly` | 15/15 (measured) | the write cells' own-session announce rows, `sh CTL+08`, `sb CTL+08` |
| `return1` | 15/15 | nothing: **EQUIVALENT on every channel** (measured, 0 differing lines) |
| `nolatch` | 15/15 | the latch-count row |

- `fallsw`, `len1only` and `readonly` also leave **every value row identical** to the decline.
- `return1` is equivalent because the `#95` pre-zero in `memory_rw` (`memset(data, 0, len)` just above `paddr -= mem->devices[i].baseaddr;`) already zeroes the read buffer. Disclose it; don't row it.

Rows I would ship:
1. **Survival and kill-text rows:** the committed 15.
2. **Value rows for 1R and 2R:** the sentinel-seeded destination reads 0 and pc moves to pc+4. These kill the `return 0` shape and any lane-serving shape.
3. **Value rows for 1W and 2W:** a pre-written CRIME_DOG word reads back unchanged.
4. **Switch side-effect rows, one per width × direction cell:**
   - 2W: `sh 0x0800 → +0x08`, then a RAM round trip.
   - 1W: `sb 0x01 → +0x08`, with the CONTROL text absent.
   - 1R and 2R: `lb` and `lh` at +0 from 0xbfc05180, with the pc not redirected.
   - Plus the live-channel control `revhack lw ctl`, which does redirect (measured).
5. **Announce rows:** each cell in its **own session**, since the latch hides the second access, checking that `(once)` appears carrying `len=N`. Plus a 5-access session that must count exactly one announcement.
6. **Accept rows (de-escalation):** 8R/8W/4R/4W at +0x00, +0x04, +0x30 and +0x34.
7. **Disclosed rather than rowed:** the `return1` equivalence, the INTSTAT/INTMASK reassert and TIME cells (not observable from a refused access), and the REV write direction.

## Q4: premise audit
- **Premise 1:** correct.
- **Premise 2:** true but incomplete.
  - The exception is raised only when `!no_exceptions`, and DMA or debugger accesses never call a `DM_DEFAULT` device at all.
  - The excerpt omits `if (running_before_device_access && !cpu->running) return MEMORY_ACCESS_FAILED;`, which governs the HARD_RESET cells.
  - The "failed" `debug()` line is invisible when free-running (measured).
  - In this setup the vector is 0x80000180, because BEV is 0 (measured).
- **Premise 3:** RE's rejection of `return 0` is a policy preference, not a hardware fact. That is correctly flagged as a question.
- **Premise 4:** correct, but the brief misses the MACE sibling in the same file, which is a byte-lane (member 7) precedent.
- **Premise 5:** correct.
- **Premise 6:** holds; `ls _scratchpad/*.pdf` shows no CRIME document.
- **Premise 7:** incomplete in two ways.
  - The device's `> 1024` check is dead code, because `machine_sgi.c` exits with that check first at construction (READING).
  - The divisibility check is live and fires at the guest's **first CRIME access of any width**. Measured: `-M 48`, then `lw +4`, gives exit 1 in all builds. The value comes from the launch, but the timing comes from the guest. I agree it is not this round's subject; it should be filed.
- **Brief switch note:** CRIME_REV fires on writes as well as reads.

## Something else (MEASURED unless marked)
1. **The existing 4-byte arm puts CRIME_CONTROL on the wrong lane.** `sw 0x800 → +0x08`, the high half, **stops the machine in every build**. `sw 0x800 → +0x0c`, the low half where bit 11 actually lives (the file's own TODO says NetBSD writes there), does nothing. Worth filing separately; member 7 would inherit this.
2. **`[ CRIME_CONTROL: unimplemented control ... ]` is an unlatched `fatal()` a guest can drive.** It can flood the log. Measured via `delete`; for 8- and 4-byte writes this is a reading.
3. **The `-M 48` kill is lazy**, as described under premise 7.
4. **Is there an eighth member?** I found only compositions: FAULT with a latched announce, and IMPLEMENT for reads with DECLINE for writes. Neither has a warrant here.

## Implementation note (READING)
- A per-instance latch field. Either `warned_len`, or a `warned` bitfield so the CONTROL fatal can be latched later.
- Use the `(once)` text and place the decline at the guard site.
- Use a `goto` to the tail; there are 21 `goto`s across 11 device files, including `dev_sgi_re.c`, so it is house style.
- **Do not fall through to the switch.** Doing so halts the machine on `sh 0x0800 → +0x08` (measured).
