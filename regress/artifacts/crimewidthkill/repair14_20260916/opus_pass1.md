OPUS_R14_ALIVE_20260916

> `# CHECKPOINT -- 2026-09-16 ~22:2x   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED, ONE MEASURING`

(first line of `_scratchpad/CHECKPOINT.md`, verbatim)

---

# VERDICT

**DO NOT SHIP REPAIR 14 AS PROPOSED.  P2 IS FALSE AND P3 IS FALSE, AND I MEASURED BOTH.**

> ### *** THE HEADLINE, MEASURED: a TWO-LINE edit scores **188/188** — a TOTAL ESCAPE of the
> ### shipped detector — on an axis repair 14 as proposed does not touch, while its one-line
> ### form (the same edit minus the latch conjunct) is killed four times over at **184/188**. ***
>
> Six mutants, two tables, every log ending `CRIMEP_DONE`, **predictions matched 6 of 6**:
>
>     base            188/188  OK      harness validated
>     PC_imk4r        187/188  gate line            POSITIVE CONTROL: reproduces close-8 exactly
>     M1_gotolatch    178/188  10 rows              decline-side latch, UNRESTRICTED -- KILLED
>     M2_ld278clr     188/188  --                   *** ESCAPE -- a FIFTH one, unnamed in the brief
>     M4_timeplain    184/188  time lb/sb/lh/sh     DISCRIMINATING CONTROL -- exactly the 4 predicted
>     M3_timelatch    188/188  --                   *** TOTAL ESCAPE -- the Q2 answer

* **P2 is the ACCEPT HALF of a 112-cell space.**  The 56-cell product describes only accesses
  that are SERVICED.  The DECLINE arm — the thing #529 actually added — has its own product,
  `{len 1,2} x {R,W} x {7 labels} x {latch}`, and the enumeration contains **none** of it.
  Part A (a pre-latch mirror of accept cells) and Part B (HARD_RESET at CONTROL) are both on
  the accept side, so **neither can reach it**.  I built two decline-side mutants; the results
  are in §1.
* **P3's stated behaviour belongs to a different mutant than P3's stated code.**  The K-form
  (`&& !(cell && latch)`) with the latch CLEAR is **LOUD, not silent** — it falls into the
  decline arm, sets the latch and prints.  It escapes because the announce is **STOLEN**, not
  because it is absent.  Reasoning from "it is silent" points a repair at the wrong channel.
* **A FIFTH ESCAPE, MEASURED: `M2_ld278clr` scored 188/188** on the shipped instrument.  The
  brief names four escapes.  ACCEPTS entry 46 (`ld +0x278`, DFL 8R) is one of the eight
  PRE-BLIND entries and the only one with **no equivalence derivation on record and no
  measurement** — and it is guest-visible.
* **Part A's denominator is 8, not 23** — derived, not argued (`mirror14.py`,
  `N_ENTRIES_WITH_NO_PRELATCH_OBSERVER=8 of 46`).  23 is the count of cells repair 13 rowed
  POST-latch; it is not the count lacking a pre-latch observer, which is what Part A buys.
  A mirror of all 23 is ~3x the work for the same closure.
* **Q3 is UNANSWERABLE as posed, and the probe's own header says so.**  2 of the 5
  HOST-DIAGNOSTIC and 6 of the 10 EQUIVALENT cells **have no listed members**
  (`crime_width_probe.py:242-257`: *"a bucket whose members cannot be listed cannot be
  audited"*).  The brief inlines those counts as a SETTLED PREMISE while its own source flags
  them unlistable.  **8 of 46 cannot be checked by anyone.**

**Repair 14 should close the DECLINE-side latch axis in the same diff**, or state in the
contract that it is deliberately out of scope — otherwise the class-closure amendment is
satisfied on one half of the space and the next pass finds the other half, which is exactly
the cell-by-cell chain the amendment exists to end.

**I enumerated that half rather than naming one cell (§2a): SEVEN cells, FOUR covered, ONE
empty by construction (DOG's arm is `break;`), and TWO OPEN — `CRIME_TIME` and `CRIME_REV`.**
Both are open for the same structural reason, which is readable without running anything: their
widths are driven in SEPARATE sessions, so every row observing them sees only the latch-CLEAR
state, whereas INTSTAT/INTMASK/CONTROL/default are driven several times in ONE session.  **Two
rows in one diff close the axis; the cell-by-cell route would have found TIME this pass and REV
the next.**  And the asymmetry is already written down in the probe — `crime_width_probe.py:
1077-1079` states it in as many words, for a different mutant, and nobody turned it around.

---

# 1.  WHAT I MEASURED

Scratch clone `/tmp/gxopus_r14` (`cp -a` of `/tmp/gxopusc8`).  **Two-part clearance run, not
asserted:** source `cmp`s CLEAN against `GXEMUL-SEC/src/devices/dev_sgi_ip32.c`, binary `-nt`
source (`22:46:52` vs `22:46:51`).  Instrument: the SHIPPED 188-row probe, frozen once to
`/tmp/crime_width_probe.r14.py`.  Clone-local `.MUTANT` sentinel dropped before mutant 1 and
cleared only after `cmp`-clean + rebuild.  **Predictions written before any build**
(`opus_pass1_work/PREDICT.md` 23:58:36, `PREDICT2.md` 00:04:17; first build log 00:00:0x /
00:18:4x).  Every log ends in `CRIMEP_DONE` — checked with `tail -1`, not by existence.

## TABLE 1 — `logs/table14.out`

| mutant | score | failing rows | reading |
|---|---|---|---|
| `base` | **188/188** `CONTROL=OK` | — | harness validated |
| `PC_imk4r` | **187/188** | `gate line` | **POSITIVE CONTROL.**  close-8's own `G_clr_imk4r` binary re-run under my driver: same score, same row.  My harness reproduces P5. |
| `M1_gotolatch` | **178/188** | `sb08 msg`, `sh08b run`, `imask sb/lh/sh`, `istat sb/lh/sh`, `gate run`, `mid nodflt` | **KILLED — and this is a useful negative.** |
| `M2_ld278clr` | **188/188** `CONTROL=OK` | — | ***ESCAPE.  A FIFTH ONE.*** |

**Predictions matched 4 of 4 on direction.**  One was *incomplete* rather than wrong and I
record it as such: I predicted `sh08b run` as M1's reddening row; it reds, **plus nine others I
did not predict.**

### `M1_gotolatch` — the smallest decline-side edit, and it is well covered

The edit is **one line moved up one line** — `goto crime_declined;` moved INSIDE the latch
block.  The session's first refusal declines correctly; every later one falls through into the
register switch, *silently*, because the latch it just set suppresses the announce.

It dies ten ways, and the mechanisms are worth recording because they show the coverage is
**structural, not lucky**:

```
sb08 msg    1 vs 0            sb 0xff at CONTROL (2nd refusal) reaches the arm; leftover
                              0xff != 0 -> the unimplemented-control text prints
sh08b run   0xdeadbeef        sh 0x0900 (2nd refusal) carries HARD_RESET 0x800 -> every CPU
            vs 0x12345678     stops -> the RAM round trip never runs
imask sb/lh/sh    set vs clear    2nd+ refusals at +0x18 reach crime_interrupt_reassert()
istat sb/lh/sh    set vs clear    ditto at +0x10 -> cause.IP2 raised
gate run    0xdeadbeef        the gate session's refused sh 0x800 at CONTROL is not its
            vs 0x12345678     first refusal -> HARD_RESET -> CPUs stop
mid nodflt  4 vs 0            2nd+ refusals at +0x1ff/+0x1fe/+0x1fc reach the default arm
```

**So the DECLINE x LATCH-SET cell is occupied at six independent sessions.**  That is a real
result and it narrows the gap: an *unrestricted* decline-side latch narrowing is caught.  What
is NOT caught is the narrowing conjoined with a LABEL whose only observing rows drive their
refusal first — which is `M3_timelatch`, §2.

### `M2_ld278clr` — the fifth escape, 188/188

```c
	if (relative_addr == 0x278 && len == 8 && writeflag == MEM_READ
	    && !(d->warned & CRIME_W_LEN))
		goto crime_declined;
```

A silent G-form bypass at **ACCEPTS entry 46**, latch CLEAR.

* **Warrant, derived before the build:** `buckets8.py` (close-8's own script, re-run by me,
  `BUCKETS8_DONE`) reports `N_PRE_BLIND=8`, and entry 46's only latch-CLEAR driver is session
  40 (`latch x5`), whose three rows are an announce count, a RAM round trip and an announce
  text — all blind to a silent decline.
* **Guest-visible:** `reg[0x278/8] = reg[79]` is NOT rewritten by the prelude (`:229-273`
  touches `reg[0]`, `reg[1]`, `reg[2]` and `reg[65..72]` only), so a seeded value persists and
  a declined 8R answers 0 instead of it.
* **The brief's P5 names four escapes and this is not among them.**

## TABLE 2 — `logs/table14b.out`

| mutant | score | failing rows | reading |
|---|---|---|---|
| `M4_timeplain` | **184/188** `CONTROL=OK` | `time lb`, `time sb`, `time lh`, `time sh` | **DISCRIMINATING CONTROL — and it reds EXACTLY the four rows I named, nothing else.** |
| `M3_timelatch` | **188/188** `CONTROL=OK` | — | ***TOTAL ESCAPE.  This is the Q2 answer.*** |

**PREDICTIONS MATCHED 6 OF 6 ACROSS BOTH TABLES.**  See §2 for the mechanism and the raw
values; both logs end `CRIMEP_DONE`.

---

# 2.  Q2 — THE SMALLEST EDIT THAT BREAKS THE FIX AND STILL PASSES REPAIR 14

> **`M3_timelatch`: two lines, on an axis repair 14 as proposed does not touch.**

```c
 		if (!(d->warned & CRIME_W_LEN)) {
 			d->warned |= CRIME_W_LEN;
 			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
 			    "  (once) ]\n", (int) len, (int) relative_addr);
+			goto crime_declined;
 		}
-		goto crime_declined;
+		if (relative_addr != CRIME_TIME)
+			goto crime_declined;
```

**Effect:** a narrow access at `CRIME_TIME` that is **not its session's first refusal** falls
into the switch and reaches `crime_update_crime_time()`, advancing the guest's clock.  The
fix's own comment names this as one of the four defects the `goto` exists to prevent —
*"one at CRIME_TIME advance the clock -- all measured"*.

**THE ROW I EXPECT TO STAY GREEN, and why it is structural rather than lucky:** `time lb`,
`time sb`, `time lh`, `time sh` (`crime_width_probe.py:773-793`) are the ONLY rows that observe
a TIME advance — they sample `mag(s1)` and want `"small"`.  In all four sessions the refused
access at `+0x38` is preceded only by an **accepted** `ld`, so it is the session's FIRST
refusal, the latch is CLEAR, and under `M3` it declines correctly.  The only sessions that
refuse at `+0x38` with the latch already SET are:

* **session 40 (`latch x5`)** — tail `lb +0x00`, `lb +0x38` after five refusals; its three rows
  are a count, a RAM trip and an announce text.  None reads TIME.
* **session 30 (dog-first)** — `time sd lb v0` / `time sd lh v0` are **ANSWER** rows, and the
  answer is still 0 because the decline arm never assigns `odata`.

**Why it is outside repair 14:** Part A adds *pre-latch* rows for *accept* cells.  A pre-latch
session by construction contains no refusal before the cell under test, so **it cannot test
anything about the decline arm at all.**  Part B is accepted CONTROL writes.  Neither reaches
this.

**`M4_timeplain` is the discriminating control** — the same narrowing with **no latch
conjunct** (one line).  It must RED `time lb/sb/lh/sh`.  Without it an M3 escape would prove
only that the TIME channel is unobservable, not that it is unobserved in one state.

> ### *** MEASURED, AND THE PAIR SETTLES IT. ***
>
> **The four `time` rows, read directly out of `logs/probe_M4_timeplain.raw` and
> `logs/probe_M3_timelatch.raw`:**
>
> | row | `M4_timeplain` (no latch conjunct) | `M3_timelatch` (with it) |
> |---|---|---|
> | `time lb` | **large, raw 143,380,182 — FAIL** | small, raw **66** — ok |
> | `time sb` | **large, raw 143,250,030 — FAIL** | small, raw **66** — ok |
> | `time lh` | **large, raw 143,134,332 — FAIL** | small, raw **66** — ok |
> | `time sh` | **large, raw 143,545,578 — FAIL** | small, raw **66** — ok |
> | `time lb/sb/lh/sh ctl` *(liveness)* | large — ok | large — ok |
>
> **`M4` reds all four; `M3` reds none — and the liveness control is `large` in BOTH runs**, so
> the channel is live in both and the difference is the mutant, not a dead instrument.  The
> discrimination is about **2.2 million to one** (143 M vs 66, one tick), and `M3` hides it
> completely.  *One token — the latch conjunct — is the whole difference between a mutant this
> detector kills four times over and one it cannot see at all.*
>
> Totals and any other reddened rows are in `logs/table14b.out` / `lane4.out` / `lane5.out`;
> both logs were checked for `CRIMEP_DONE` with `tail -1`.  Predictions and their full
> derivation are in `PREDICT2.md`, written 00:04:17, before the 00:18:4x builds.

**This is the accept-side K-class, mirrored one arm over**: a two-axis narrowing where ONE
axis (the label) is already rowed and the OTHER (the latch) is not — on the decline side,
where the enumeration has no cells at all.

## 2a.  THE WHOLE DECLINE x LATCH-SET AXIS, DERIVED — SEVEN CELLS, **TWO OPEN**

Do not take `M3` as one more cell to row.  The class-closure amendment says *enumerate the
full space from the function's own inputs and close every cell in ONE diff*, so here is that
enumeration for the half P2 omits.  **The discriminator is a SESSION-SHAPE fact, readable
without running anything:** does any session refuse at this label **more than once**?  If yes,
refusals 2+ are measured with the latch SET; if no, the label is measured only latch-CLEAR.

| label | arm's observable effect | sessions refusing there | latch-SET cell |
|---|---|---|---|
| **REV** `+0x00` | `pc = ra`, but **only from the PROM window** (`:344`) | `:637-641` (lb, lh) and `:650-653` (sb, sh) are **FOUR SEPARATE SESSIONS**, each with its REV refusal FIRST and from `PROBE_PC`.  `latch x5`'s tail `lb +0x00` (`:1080`) is from **CODE**, so the window branch is not taken. | ***OPEN*** |
| **CONTROL** `+0x08` | HARD_RESET halt; the leftover text | `sb08` (2 refusals), `sh08b` (4), `gate` | **covered** — M1 reds `sb08 msg`, `sh08b run`, `gate run` |
| **INTSTAT** `+0x10` | `crime_interrupt_reassert()` -> IP2 | `:684-706` puts **all four widths in ONE session** | **covered** — M1 reds `istat sb/lh/sh` |
| **INTMASK** `+0x18` | same | same block, one session | **covered** — M1 reds `imask sb/lh/sh` |
| **DOG** `+0x30` | `case CRIME_DOG: // No warning. break;` — **no body at all** | session 30 refuses there twice | **EQUIVALENT BY CONSTRUCTION** — there is nothing to observe |
| **TIME** `+0x38` | `crime_update_crime_time()` -> the clock advances | `:773-785` calls `session()` **inside** the `for op` loop — **FOUR SEPARATE SESSIONS**, refusal first in each | ***OPEN*** — this is `M3` |
| **default** | a `debug()` line | `mid` (multiple) | **covered** — M1 reds `mid nodflt` |

**Two open cells, one empty, four covered — and the two open ones are open for the SAME
structural reason: their widths are driven in separate sessions, so every row that observes
them sees only the latch-CLEAR state.**  That is the PRE-TABLE CHECK's **SIBLING PARITY** row
doing its job on the decline arm: INTSTAT/INTMASK and TIME/REV are siblings with opposite
session shapes, and the asymmetry is visible by reading, before any table runs.

> ### *** AND THE PROBE ALREADY KNEW.  `crime_width_probe.py:1077-1079`, in `latch x5`'s own
> ### comment: ***
>
> > *"refusals at CRIME_REV and CRIME_TIME AFTER the latch is set (the Opus third-closing
> > seat, measured: a latch TEST that lets one label through -- `|| relative_addr ==
> > CRIME_REV' -- passed, **because REV and TIME were each refused only once per session,
> > first**; every other label is refused again after the latch is set somewhere)"*
>
> **The exact asymmetry that makes `M3` escape is written in the probe, one screen above the
> session it describes.**  It was derived for a different mutant (a latch *test* that lets one
> label through), the two refusals in `latch x5`'s tail were added to close *that*, and nobody
> turned the sentence around to ask what it implies for the **`goto`**.  Those two tail
> refusals run from CODE, so they close the latch-TEST question and leave the latch-GOTO one
> wide open.
>
> *This is the carrier's own finding recurring: knowledge present, unconsulted at row-writing
> time.  It is also why the fix here is an ENUMERATION, not a row — the cell-by-cell route
> would have found TIME this pass and REV the next.*

**WHAT REPAIR 14 SHOULD DO WITH THIS:** two rows, one diff.  For **TIME**, a session that
refuses somewhere else FIRST and then at `+0x38`, with the `time`-row oracle (`mag(s1)`).  For
**REV**, a session that refuses elsewhere first and then at `+0x00` **from `PROBE_PC`**, with
the `rev pc` oracle.  Both are existing oracles in a new session shape — no new channel is
needed.  Then say in the contract that DOG is equivalent by construction and that the other
four are carried by multi-refusal sessions, **naming them**, so a future row-list rewrite
cannot silently drop the property the way `#490`'s did.

---

# 3.  Q1 — THE PREMISE AUDIT

| premise | verdict |
|---|---|
| **P1** the enclosing function | **TRUE**, byte-accurate.  Checked line by line against `GXEMUL-SEC/src/devices/dev_sgi_ip32.c:296-320, 411-423`.  All four fork trees carry md5 `8c1d1545`; the pristine-2021 copies (`_scratchpad/panel_20260830_214609/...`, `_scratchpad/seat500_p9/tree/...`) are `4088baa8` / 871 lines and I did not read them. |
| **P2** 56 cells / floor 23 | **FALSE twice.**  It is the ACCEPT half of a 112-cell space (§1), and the bucket counts are inlined as settled while 8 of 46 members are unlistable (§4). |
| **P3** the mutant shape | **FALSE as stated.**  The code shown is the K-form; the behaviour described is the G-form.  See below. |
| **P4** repair 13 is all post-latch | **TRUE** for the `p *` sessions (all six open with `POST(A)`).  *"the latch-CLEAR state is driven by session 40 ALONE"* is **too strong** — 38 of the 46 entries have another pre-latch driver; **eight** do not. |
| **P5** the kill table | **TRUE.**  I re-ran `G_clr_imk4r` as `PC_imk4r` and got 187/188 reddening `gate line`, matching exactly. |
| **P6** the generating set at CONTROL | **TRUE, and I verified the Part-B warrant by enumeration.**  The only accepted 0x800 write in the probe is `:549` (`sw08 halts`, pre-latch); the `ACCEPTS` CONTROL values (`:864-865, :872`) are `0x0201/0x0001/0/0x0200/0x0100` and P2's post-latch writes are `0x01/0x0001/0x0201` — **no 0x800 anywhere post-latch.**  Two riders below. |
| **P7** the three owed probes | **TRUE.**  Re-read the logs: `ctl4r` 9/9, 9/9, 8/9 (`CTL4R_DONE`); `ctlreset` 6/6, 5/6, 5/6 (`CTLRESET_DONE`).  Scores match the brief exactly. |

## P3 in detail — the two forms are not the same mutant

* **K-form**, `if (len == 4 && !(cell && ...))` — falls into the **decline arm**.  With the
  latch SET it is silent.  **With the latch CLEAR it takes `if (!(d->warned & CRIME_W_LEN))`,
  SETS THE LATCH AND PRINTS.**  It is loud.
* **G-form**, a bypass `goto crime_declined` inserted before the width test — silent in both
  states.  **This is the form close-8 actually built** (`G_clr_ist4r`, `G_glm_tim4clear`), and
  it is the form I built for `M2`.

**Why it matters:** the loud K-form escapes because its announce is **ABSORBED** — in `latch
x5`'s prologue it steals the session's one announce and the count stays 1 (the probe header
records exactly this at `:98-101`, G1–G5 at 141/141).  A repair reasoned from *"it declines
silently"* will look for a missing-message channel when the real channel is a **stolen** one.

## ARE THERE OTHER AXES?  Yes — four, and all four COLLAPSE, with warrants

Read off the whole function (`:211-423`).  Beyond the lane (`:282`, `:291`) and the PC window
(`:344`) that pass 8 measured:

| axis | where | disposition |
|---|---|---|
| **`cpu->is_32bit`** | `:346`, inside the REV window branch | **DEAD CODE on ip32**, not merely equivalent.  `-e ip32` is subtype 32 -> falls through `machine_sgi.c:690-706` to the default `R4400`; `mips_cpu_types.h:84` gives R4400 `isa_level 3`; `cpu_mips.c:116-118` sets `is_32bit` only for `isa_level <= 2 \|\| == 32`.  So it is always 0.  A conjunct on it is either vacuous or identical to the unconditional mutant.  **The distinction matters: if an SGI 32-bit subtype is ever added, this becomes a live axis.** |
| **`cpu->machine->ncpus`** | `:369`, the HARD_RESET loop | 1 on ip32; collapses identically. |
| **`d->use_fb`** | `:229` | constant per run; already disclosed at the probe header `:179-180` as an always-0 *answer source*, but **not as a branch**. |
| **`cpu->machine->physical_ram_in_mb`** | `:244`, `:250`, `:255`, `:266` | machine-config, not guest-drivable.  But see §5 — it carries **two surviving `exit(1)` sites inside the de-fatalised function**. |

**`writeflag` is binary and complete** — I checked rather than assumed: `MEM_DOWNGRADE` (128)
exists in `memory.h:119` but every use is in `cpu_dyntrans.c`'s translation-table path
(`:1695, :1710, :1729`), never as a `memory_rw` writeflag reaching a device.  So the direction
axis is exactly `{MEM_READ, MEM_WRITE}`.

**The callees are correctly outside the DEPENDS-ON bound** (*never into callees*), but each
owes one disclosure line: `crime_interrupt_reassert` tests `asserted && !d->prev_asserted`;
`crime_update_crime_time` tests `d->last_microseconds == 0`, `delta < 0` and `to_add >= 1`.

## THE DOMAIN — and it has a DEPENDENCY nobody has stated

The brief says *"ENUMERATE THE RIGHT DOMAIN — ask what the PRODUCER can actually emit."*  I
audited the `len` producer, and the answer bounds the decline-side product I am claiming is
missing:

> **From a real MIPS guest instruction, `len` in `{1, 2, 4, 8}` EXACTLY.**
> `lwl/lwr/swl/swr/ldl/ldr/sdl/sdr` do **not** emit 3/5/6/7:
> `cpu_mips_instr_unaligned.c:52` computes `aligned_addr = addr & ~(wlen-1)` and `:92`/`:131`/
> `:139` call `memory_rw` with `wlen` (4 or 8) at that aligned address; the byte selection
> happens in a local `aligned_word[8]`.  *(A store is a read-modify-write — a 4-byte MEM_READ
> at `:92` then a 4-byte MEM_WRITE at `:131`.)*

**So the decline arm's reachable `len` is exactly `{1, 2}`** — which is what the probe drives,
and which makes the decline-side product a bounded 2 x 2 x 7 x 2 = 56, not an open set.

> ***BUT THERE IS A SECOND `len` PRODUCER, AND ITS INERTNESS HERE DEPENDS ON A CONSTANT.***
> `memory_rw.c:495-523` **clamps** `len` at the end of a device: `len = mem->devices[i].length
> - paddr`, which can emit any value 1..7.  It cannot fire inside CRIME **only because
> `DEV_CRIME_LENGTH` is `0x280`, a multiple of 8**, so no naturally aligned MIPS access can
> overhang it.  **Change that constant and lengths 3, 5, 6, 7 become reachable.**  That belongs
> in the contract; it is currently stated nowhere.

---

# 4.  Q3 — THE FLOOR AND ITS BUCKETS

**The question cannot be answered against the bucket table, and the probe's own header says
why** (`crime_width_probe.py:242-257`):

> *"THE REMAINING TWO ARE UNNAMED IN THIS RECORD AND THAT IS THE DEFECT, not a rounding: a
> bucket whose members cannot be listed cannot be audited, and minimax independently reported
> it could not check them from the packet (**"4 are named; 6 are not"** of the EQUIVALENT
> bucket, the same shape of hole)."*

So **2 of the 5 HOST-DIAGNOSTIC and 6 of the 10 EQUIVALENT — 8 of 46 — have no listed
members.**  P2 inlines those counts as a SETTLED PREMISE.  A brief may not promote to settled
a number its own source records as unlistable.

**What I *can* check, I did.**  The four NAMED equivalent cells all hold:

* REV 8W / 4W-high / 4R-high outside the window — the prelude at `:229` rewrites
  `d->reg[CRIME_REV/8]` on **every** access, and a read-back needs a second access.  **Correct.**
* CONTROL 4R (high lane) — prelude sets `reg[1] = 0x100`, so the high half is 0 either way.
  **Correct, and measured** (`ctl4r.py` 9/9 with a liveness control at 8/9).

**AND A TWO-EIGHTS COLLISION A READER WILL WALK INTO.**  The brief's *"8 ALREADY PINNED"* is a
**POST**-latch set (from `session_map2.py`).  `buckets8.py` reports `N_PRE_BLIND=8` — a **PRE**-latch
set, a *different* eight.  They are not the same cells and the coincidence of the number is
pure bad luck.  (`buckets8.py` also reports `N_POST_BLIND=4`: entries 1, 3, 4, 8 — all in the
prelude-rewritten equivalent class, so consistent.)

**A specific mis-labelling, minor but it would propagate:** `p rev lw4`
(`crime_width_probe.py:1334`) is noted *"accepted lw +0x04 answers REV low lane"*.  The REGISTER
is `reg[0]` = CRIME_REV, but `switch (0x04)` matches **no case** (labels are 0x00/0x08/0x10/
0x18/0x30/0x38) — the access reaches **`default:`**.  `buckets8.py` files entry 41 as `DFL`,
correctly.  An enumeration built by reading the row notes would put the cell in the wrong
column.

---

# 5.  Q4 — HOW WIDE MUST THE MIRROR BE?  **EIGHT ENTRIES, NOT 23**

Derived, not argued: `opus_pass1_work/mirror14.py` (sentinel `MIRROR14_DONE`) prints, per
ACCEPTS entry, every latch-CLEAR driving session other than `latch x5` **with that session's
row names**.  `N_ENTRIES_WITH_NO_PRELATCH_OBSERVER=8 of 46`:

| entry | cell | disposition |
|---|---|---|
| 1 | `sd +0x00` REV 8W | **collapses** — prelude rewrites `reg[0]`.  *Derivation only; owes the `ctl4r.py` treatment.* |
| 3 | `sw +0x00` REV 4W | **collapses**, same warrant, same caveat. |
| 8 | `lw +0x08` CTL 4R | **collapses — MEASURED** (`ctl4r.py` 9/9, liveness 8/9).  The template. |
| 21 | `lw +0x10` IST 4R | **OPEN.**  `G_clr_ist4r` — escapes the 188-row probe *and* `t4clear.py` (5/5).  **Nothing catches it.** |
| 32 | `sw +0x38` TIM 4W | **OPEN**, covered by `t4clear.py` (3/5). |
| 33 | `lw +0x38` TIM 4R | **OPEN**, same. |
| 40 | `sw +0x04` DFL 4W | guest-equivalent, measured (F3, 157/157). |
| 46 | `ld +0x278` DFL 8R | ***OPEN, AND UNNAMED ANYWHERE.***  My `M2` — 188/188. |

**So Part A needs at most FOUR new pre-latch rows** (21, 46, and 32/33 which `t4clear.py`
already provides), and **each of the four collapse claims owes the `C_ctl4r` treatment** —
which is the brief's own standard, stated in Q4 and met so far by exactly one cell.

## TWO RIDERS ON PART B, both structural

1. **An accepted HARD_RESET write TERMINATES its session, so it can only ever be the session's
   LAST access.**  Part B as worded — *"at every rowed CONTROL cell, write HARD_RESET 0x800
   both clear and set"* — reads as *append two writes to the existing value sessions*, which
   yields a truncated session, not a row.  `ctlreset.py` already has the right shape
   (`halt_session()`: refused `lb +0x07`, then the 0x800 write, then a RAM trip whose
   **absence** is the oracle).  **Part B therefore costs one NEW SESSION per rowed CONTROL
   cell.**  Write that into the design or it will be re-discovered by a red table.
2. **P6 names three tested idata bits and Part B closes one.**  The DOG test at `:361` is
   **observably inert** — `if (idata & DOG) { idata &= ~DOG; }` is exactly `idata &= ~DOG;`,
   so the `if` cannot change any output; DOG is visible only through the leftover at `:377`,
   which `p acc ctl msg` counts.  The **leftover-ZERO** cell (`0x0100` / `0x0000`) is driven
   POST-latch by nothing — but it is guest-equivalent (prelude rewrites `reg[1]`; the arm
   prints nothing), so it is **disclosure, not floor**.  Say so rather than leaving the reader
   to notice P6 lists three and Part B does one.

---

# 6.  THINGS I FOUND WHILE VERIFYING SOMETHING ELSE

### (a) A STALE CITATION THAT **#529'S OWN DIFF** CREATED — arithmetic-verified

`OUTSTANDING_BUGS.md:5574` cites **`dev_sgi_ip32.c:698`** as a register-width device handler.

```
git show HEAD:src/devices/dev_sgi_ip32.c | grep -n "len != 4"   ->  698
grep -n "len != 4" src/devices/dev_sgi_ip32.c                   ->  728
```

**#529's diff adds exactly 30 lines above it** (`@@ -84,0 +85,4 @@` +4, `@@ -86,0 +91,2 @@` +2,
`@@ -291,2 +297,23 @@` +21, `@@ -383,0 +411,3 @@` +3), and 698 + 30 = 728.  This is the
carrier's own rule unexecuted by this round — *"A LINE NUMBER IN A COMMENT IS INVALIDATED BY
YOUR OWN EDITS TO THAT FILE.  Re-grep every same-file citation AFTER the last edit."*  The
remedy is the citation-form rule: a verified-unique grep anchor.  *(The two sibling citations
in the same sentence, `dev_sgi_gbe.c:726` and `dev_kn01.c:89`, are in other files and
unaffected — it is a one-number fix.)*

### (b) TWO `exit(1)` SITES SURVIVE INSIDE THE DE-FATALISED FUNCTION

`DEVICE_ACCESS(crime)` still contains `exit(1)` at **`:246`** and **`:259`** (the RAM-size
prologue), and they run on **every** CRIME access, before the width test.  They are **not
guest-drivable** — `physical_ram_in_mb` is fixed at machine construction — so they are
correctly out of #529's scope.  **But the contract should say so**, because the obvious review
check on a de-fatalised device is `grep -n 'exit(' <file>` and it returns two hits a reader
must then re-derive.

### (c) AN UNLATCHED GUEST-DRIVABLE `fatal()` IN THE SAME FUNCTION, WITH A DETECTOR INTERACTION

`:378` — `fatal("[ CRIME_CONTROL: unimplemented control 0x%016llx ]")` — is **unlatched and
guest-drivable** (any nonzero unmodelled CONTROL write, in a loop).  It is a `floodclass`
member, not a host kill.  **The interaction worth recording: three shipped rows COUNT it**
(`sb08 msg`, `sh08b msg`, `p acc ctl msg`), so a future round adding the house `(once)` latch
there **owes all three rows' re-derivation**.  Siblings in the same file:
`DEVICE_ACCESS(mace):636-640` and `DEVICE_ACCESS(macepci):729`.

**`macepci:728-729` is the SAME WIDTH CLASS one device over** — `if (len != 4) fatal(...)` with
**no decline and no latch**: it warns and then falls through into its own register switch,
which is the very shape #529's `goto` exists to prevent.  Not a host kill, so it is a filing,
not this round's business — but `grep -c dev_sgi_ip32 OUTSTANDING_BUGS.md` returns **2** and
neither is about it.

### (d) A ROW-TO-SESSION OFF-BY-ONE IN MY OWN DERIVER, FOUND AND FIXED BEFORE IT SHIPPED

`_rec()` snapshots `PEND` at the START of a session, so `PEND` then holds the **previous**
session's rows: `S[i] = [accesses_i, rows_{i-1}]`.  My first `mirror14.py` printed `S[s][1]`
and its row column was shifted by one.  **Verified empirically rather than reasoned**: session
40 has 55 accesses (it is `latch x5`) and the names `latch x5, latch surv, latch said` sit at
index **41**.  **`buckets8.py` is UNAFFECTED** — its BLIND test keys on the ACCESS index, not
on rows — so `N_PRE_BLIND=8` stands.  Recorded because the shifted table looked entirely
plausible.

### (e) TWO APPARATUS FAILURES OF MINE, BOTH THE CARRIER'S OWN DOCUMENTED CLASSES

* **The backslash trap, twice.**  `\\n` written through Bash -> heredoc -> Python collapsed to
  `\n`, so my first mutant anchor matched **0 occurrences** and the applier failed loudly (it
  treats MUTANT-TEXT-NOT-FOUND as fatal, which is what made it loud).  A second attempt, one
  layer further out, put real tabs and newlines inside a Python string literal and produced a
  `SyntaxError`.  Fixed by re-anchoring with single-backslash escapes only and by editing the
  file directly instead of rewriting it through a heredoc.
* ***A FAILURE LAUNDERED INTO A CLEAN COMPLETION — and it exited 0.***  I patched `kill14b.sh`
  with Windows Python, which wrote **CRLF**.  Under `bash`: `set -u\r` -> *"invalid option"*,
  then `cd '/tmp/gxopus_r14\r'` -> *No such file or directory* — **and the script exited 0**
  after ~2 seconds, reporting success while building nothing and running nothing.  It was
  caught only because the runtime was impossible (2 s for two 17-minute probes).  No damage:
  the `cd` failed **before** the sentinel was dropped, so the clone was never entered — I
  verified `cmp`-clean, `binary -nt source`, no `.MUTANT`, table-1 bins intact, before
  re-running.  **A shell script written by a Windows tool is CRLF unless something says
  otherwise, and CRLF fails with exit 0.**

---

# 7.  FOOTPRINT

No project source tree was written.  All four fork copies of `dev_sgi_ip32.c` carry md5
`8c1d1545eeddd12fd49f52ccede60262` — `GXEMUL-SEC/`, `build/`, `est/`, `build-asan/` — unchanged
from when I started.  `git status --porcelain` shows the same fourteen pre-existing modified
files and no new one; my only addition is the untracked
`regress/artifacts/crimewidthkill/repair14_20260916/`, which is where I was asked to write.
All mutation happened in `/tmp/gxopus_r14`, which ends `cmp`-clean against SEC with its
sentinel cleared and `restored` byte-identical to `base`.

**Final clearance, run not asserted:** clone sentinel **CLEARED**, clone source `cmp`s **CLEAN**
against SEC, clone binary **`-nt`** source, `restored` **byte-identical to `base`**.  The four
fork copies of `dev_sgi_ip32.c` all still carry md5 `8c1d1545eeddd12fd49f52ccede60262`.

**Artifacts** (all under `GXEMUL-SEC/regress/artifacts/crimewidthkill/repair14_20260916/opus_pass1_work/`):
`PREDICT.md`, `PREDICT2.md`, `mutants14.py`, `mirror14.py`, `kill14.sh` + its frozen run copy,
`kill14b.sh` + its frozen run copy, `mutants/*.diff`, `builds/*.log`, `logs/table14.out`,
`logs/table14b.out`, `logs/lane0..5.out`, `logs/probe_*.raw`, `logs/INSTRUMENT.md5`.

---

# 8.  THE ONE THING I WOULD DO NEXT, IF THE ROUND WANTS ONE MORE MEASUREMENT

**Build `M_revlatch`** — the same two-line edit with `CRIME_REV` in place of `CRIME_TIME`.  §2a
derives that cell as OPEN for the same structural reason, and the derivation is checkable
without running anything: the four REV refusal sessions (`:637-641`, `:650-653`) each refuse
FIRST and from `PROBE_PC`, while the only latch-SET refusal at `+0x00` is `latch x5`'s tail
(`:1080`), which runs from **CODE** — so the `pc = ra` branch at `:344` is never taken there.
**I predict 188/188.**  I did not build it; I am flagging it as DERIVED, NOT MEASURED, because
this project's own rule is that the two must not render the same.  If the round closes the
axis as an enumeration (two rows, one diff) rather than cell by cell, it never needs building.
