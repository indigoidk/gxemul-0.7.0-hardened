VERDICT: GAP: `if (len == 8) {` -> `if (len == 8 && relative_addr != CRIME_CONTROL) {` -- scores **141/141** on the shipped 141-row test, and it is guest-visible: an accepted `ld` of CRIME_CONTROL answers 0 instead of 0x100, and an accepted `sd` to CONTROL no longer reaches the CONTROL arm. The same one-conjunct growth of an ACCEPT guard escapes at CONTROL 4R (codex's C1), INTSTAT 8W/8R, TIME 4W/4R, INTMASK 4W and REV 4W (the PROM-window redirect). All six measured 141/141. Codex's one-row repair kills all six and moves no row on base (149/149).
CRIME_CLOSE6_OPUS_20260915

CHECKPOINT.md line 1, verbatim:
`# CHECKPOINT -- 2026-09-15 ~00:0x   HEAD 9c91999 (records)   RECOVERED from a Claude Code exit at ~12:55 on 09-14`

# #529 CLOSING PASS 6 -- Opus 5 seat (Agent tool, MEASURING)

## Apparatus (every number below is from a log in `logs/`)

* **Clone.** `/tmp/gxopuscrimec6` is a `cp -r` of `build/`. GXEMUL-SEC's working-tree `src/devices/dev_sgi_ip32.c`
  (md5 `8c1d1545...`, the same as build/ and est/) was copied in, and `cmp` came back CLEAN. I then ran
  `rm src/cpus/*.o src/devices/dev_sgi_ip32.o gxemul` and rebuilt. `cpu_mips.o` was recompiled at 01:33:59, and
  `[ gxemul -nt dev_sgi_ip32.c ]` was checked. All 12 mutant binaries were built serially from that baseline, under a
  clone-local `.MUTANT` sentinel, and copied to `/tmp/gxopuscrimec6_bins`. Each one was checked to differ from base,
  and each was checked with `-nt`. The restore was built last: `CLONE RESTORED cmp=clean binary-nt-source=yes`, and
  `restored binary == base (byte-identical)` (`scripts/build6.out`). Mutant diffs are in `mutants/*.diff`.
* **Instruments.** `scripts/crime_width_probe.frozen.py` is a copy of the shipped probe, `cmp`-identical at launch
  and again at the end (md5 `88428f4c...`). `scripts/crime_width_probe.aug6.py` is the frozen probe with rows
  APPENDED (`augprobe6.py`), and no shipped session's command list changed. There are three appended groups:
  `latch said` is **codex's repair**, a new row that reads latch x5's existing transcript. `free revP said` is one
  new free-running session. The six `dg *` DIAGNOSTIC rows (two new sessions) are guest-visible discriminators.
  The augmented probe has 149 rows. Its first 141 rows are the shipped rows, computed from unchanged commands.
* **Runs.** 22 legs ran in two lanes, 01:34-04:12, about 14 minutes each. The other Opus seat was measuring
  concurrently in its own clone. Every log ends `CRIMEP_DONE`, and every leg is `CRIMEP_CONTROL=OK`.
  **Base: shipped 141/141, augmented 149/149.**

## RESULTS

| id | source edit (exact diff in `mutants/`) | shipped 141 | augmented 149 (red rows) | guest- or transcript-visible discriminator |
|---|---|---|---|---|
| base | -- | **141/141** | **149/149** | -- |
| **C1** (codex) | `} else if (len == 4 && (relative_addr != CRIME_CONTROL \|\| writeflag != MEM_READ)) {` | **141/141** | 147: `latch said`, `dg first said` | TRANSCRIPT ONLY. The 4R answers 0 either way (`dg lw ctl` 0x0 on both). It emits a spurious `len=4 at 0x8` notice and silences the first genuine refusal's notice. |
| **C2** (glm) | `(((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100 ? debug : fatal)(` | **141/141** | 148: `free revP said` | A free-running refused lb at CRIME_REV **from the PROM window** is silent (the fatal becomes a debug). |
| C3p (kimi-k3) | `if (relative_addr & 0x180) d->warned \|= CRIME_W_LEN;` before the switch | 139/141: `mid said`, `mid once` | -- | killed |
| C3r | the same with `d->warned = 0;` | 139/141: `mid said`, `mid once` | -- | killed |
| C4 (minimax) | `odata = (relative_addr & 7);` before the goto | 131/141: `lb/lh/lbu/lhu v0`, `warm v0`, `top rd v0`, `top rd2 v0`, `mid lb/lh v0`, `free v0` | -- | killed |
| C5 (kimi CLI) | `odata = idata;` before the goto | **141/141** | -- | **EQUIVALENT by construction** (below) |
| **G1** (own) | `if (len == 8 && relative_addr != CRIME_CONTROL) {` | **141/141** | 146: `latch said`, **`dg ld ctl` 0x0 != 0x100**, `dg first said` | GUEST: an 8R of CONTROL answers 0; an 8W skips the CONTROL arm |
| **G2** (own) | `if (len == 8 && relative_addr != CRIME_INTSTAT) {` | **141/141** | 146: `latch said`, **`dg ld istat` 0x0 != SOFTINT**, `dg first said` | GUEST: an 8R of INTSTAT with an interrupt pending answers 0 |
| **G3** (own) | `} else if (len == 4 && relative_addr != CRIME_TIME) {` | **141/141** | 148: `latch said` | TRANSCRIPT ONLY. The 4-byte TIME cells are value-equivalent: the high half is 0, and updates accumulate. |
| **G4** (own) | `} else if (len == 4 && (relative_addr != CRIME_REV \|\| writeflag != MEM_WRITE)) {` | **141/141** | 147: `latch said`, **`dg swP pc` 0xbfc05184 != ra** | GUEST: an accepted sw to REV from the PROM window no longer redirects |
| **G5** (own) | `} else if (len == 4 && (relative_addr != CRIME_INTMASK \|\| writeflag != MEM_WRITE)) {` | **141/141** | 146: `latch said`, **`dg sw imask` 0x0 != 1<<60**, `dg first said` | GUEST: a 4W to INTMASK does not land |
| G6 (own) | `if (len == 8 && relative_addr == CRIME_CONTROL) goto crime_declined;` inserted before the width test | **141/141** | 148: **`dg ld ctl`** only | GUEST: as G1, but SILENT. **`latch said` is GREEN on it**: no notice, so codex's row cannot see it. |

Every red row above is exactly the row I predicted before the run. The only red rows are appended rows: no
shipped row moved in any augmented leg, and base is 149/149.

## Q1 -- VERIFY THE ENUMERATION

**Derivation from the function's own branches.** An accepted access (len 4 or 8) passes two tests in the width arm:
`writeflag`, and for 4-byte accesses `relative_addr & 4`. That gives six kinds: 8W, 8R, 4W-hi, 4W-lo, 4R-hi, 4R-lo.
It then goes through `switch (relative_addr)`. The labels are 8-aligned, so a 4-byte access AT a label is the hi
lane. The lo lane is the default arm. The label bodies test the following:
* REV tests the pc window.
* CONTROL tests `writeflag`, and on writes it tests DOG, HARD_RESET and leftover-nonzero.
* The default arm tests `writeflag`.
* INTSTAT, INTMASK, DOG and TIME have no `if` in this function.

So the latch floor is:

| label | floor cells | count |
|---|---|---|
| REV | {8W,8R,4W,4R} x window {in,out} | 8 |
| CONTROL | reads {8R,4R}, plus writes {8W,4W} x {DOG set/clear} x {leftover 0/nonzero} (HARD_RESET's true side disclosed) | 10 |
| INTSTAT, INTMASK, DOG, TIME | {8W,8R,4W,4R} each | 16 |
| default | 6 kinds | 6 |
| **total** | | **40** |

**`ACCEPTS` (46) = these 40 + the two named ENDIANESS strengthenings + 4 positional repeats of default kinds**
(`sw/lw 0x04` repeat 0x34's lo-lane kinds; `sd/ld 0x278` repeat 0x40's 8-byte kinds). No floor cell is missing for the
PRE-SET/RE-ARM class, and every listed kind is takeable -- `ldP` is correctly routed by `accept()`.

**BUT THE TWO ROWS ACCEPTS FEEDS HAVE A CHANNEL THAT CANNOT VARY UNDER AN ACCEPT-SET SHRINK -- of ANY of its 46
cells.** Both rows count `-- declined.`:
* In `rearm once`, a shrunk cell comes after the first refusal, so its decline is silenced by the latch.
* In `latch x5`, the first shrunk cell in the prologue IS the session's first refusal. It takes the one notice, the
  lh +0x06 after it is silent, and the count is still 1.

So ACCEPTS carries the latch cross and carries **nothing** about whether its cells are still accepted. For a cell whose only
accepted access in the probe is in those two sessions, a shrink is invisible. Per-cell, derived by grepping every
accepted access outside ACCEPTS:

| ACCEPTS cell(s) | accept side pinned elsewhere? | a shrink there would... |
|---|---|---|
| REV 8R (`ld 0`), 4R window (`lwP`) | yes: `acc8 near`, `rev pc ctl` | -- |
| REV 8W/4W/4R out of window (`sd/sw/lw 0`), `sw 0x04` | no | be value-equivalent (the prelude rewrites REV; the hi half is 0) -- notice only |
| **REV window 4W/8W/8R (`swP`,`sdP`,`ldP`)** | **no** | **lose the pc redirect (G4 measured)** |
| CONTROL 4R (`lw 8`) | no | be value-equivalent -- notice only (**C1** measured) |
| **CONTROL 8R, 8W (`ld 8`, `sd 8` x5)** | **no** (every CONTROL write row is a 4-byte `sw`) | **answer 0 not 0x100; skip the arm (G1 measured)** |
| CONTROL 4W (`sw 8` x5) | yes, for an address+direction shrink: `sw08 halts`, `sw08 msg ctl` | (a shrink keyed on the DOG-set value cells is not seen -- clause (e), a value joint) |
| **INTSTAT 8W, 8R, 4W** | **no** | **drop the reassert / answer 0 with an irq pending (G2 measured)** |
| INTSTAT 4R; INTMASK 8W, 8R, 4R | yes: `istat ctl`; `imask said`+`imask ctl`; `imask keeps`; `imask ctl`, `gate line` | -- |
| **INTMASK 4W** | **no** | **not land (G5 measured)** |
| DOG x4, `sw/lw 0x34` | yes: `acc8 st+ld`, `acc4 *` | -- |
| TIME 8R | yes: `time * ctl` | -- |
| **TIME 8W** (`sd 0x38`; the dog session's `sd 0x38` comes after its first refusal, and its refused reads answer 0 either way) | **no** | **lose the seed (reasoned, not built)** |
| TIME 4W, 4R | no | be value-equivalent (hi half 0; updates accumulate) -- notice only (G3 measured) |
| default `sd/ld 0x40`, `sd/ld 0x278` | yes: `lo keeps`, `top *` | -- |
| **default `sw/lw 0x40`** (4-byte hi lane, interior) | **no** | **lose the value** -- the address-keyed form falls under the disclosed "unrowed slot" class |

**THE FLOOR ARGUMENT, so this is graded on the rules and not on the count.** Four points, strongest last.
1. **The de-escalation clause.** C1 and G1-G5 are exactly its shape: a growth of the predicate that used to gate
   death. Pre-fix, the else-arm was `exit(1)`, so `len == 8 && relative_addr != CRIME_CONTROL` would have ended the
   process at the first 64-bit CONTROL access. That is self-announcing. Post-fix, the same edit declines once and
   nothing reds. The clause says those accept rows are the fix's own cost.
2. **The JOIN clause.** The label is a floor axis of that guard. `relative_addr` flows into
   `d->reg[relative_addr / 8]`, which the guarded body reads and writes, and the switch re-tests it after the join.
3. **The contract's own item 6.** It claims "the ACCEPT SET shrunk at any single cell". The DISCLOSED list's
   "unrowed slots" bullet names +0x08, +0x10, +0x18 and +0x38 as ROWED slots.
4. **This exact edit shape was already found once, at one label, and repaired only there.** Grok's closing-pass
   `len == 8 && relative_addr != 0` is why `acc8 near` exists. The identical edit with `CRIME_CONTROL` or
   `CRIME_INTSTAT` passes today. That is the #499 shape: a class repaired at the address the mutant used.

**I grade it L2, a FLOOR breach, and a class that owes CLASS CLOSURE rather than a cell.** C1 on its own is
value-equivalent at the guest, so it shows only on the notice channel. G1, G2, G4 and G5 are guest-visible and
leave no room for an equivalence argument.

## THE REPAIR -- codex's row, MEASURED, and it closes the whole announced class at once

`row("latch said", said(t, 2, 0x6, clean), 1, ...)` goes in latch x5, beside `latch x5`. It can equally be folded
into `latch x5` as count == 1 AND said == 1. It is red on **C1, G1, G2, G3, G4 and G5**, and green on base (149/149,
no other row moved). **Why it is general:** all 46 ACCEPTS cells sit in latch x5's prologue BEFORE the lh +0x06. Any
guard-growth shrink of any of them sends that cell into the announcing decline arm, where it takes the notice the lh
should have had. So one row turns the prologue from a latch-only detector into an ACCEPT-SET detector for every
ACCEPTS cell. No new session is needed and the command list is unchanged.

**What it cannot see: a SILENT bypass (G6, measured 148/149 with `latch said` GREEN).** I grade G6 outside the
de-escalation class. The deleted `exit(1)` would not have announced a new bypass inserted before the width test
either: pre-fix `if (...) return 1;` is equally silent. It is, however, inside item 6's literal "any single cell"
sentence. Two dispositions are open, and the choice is the adjudicator's:
* (i) narrow item 6 to "any single cell, in the guard-growth form" and DISCLOSE the silent bypass by class; or
* (ii) add VALUE rows at the uncovered label cells as a licensed clause-(e) strengthening.

`dg ld ctl` / `dg ld istat` / `dg sw imask` in my diagnostic session are a measured template: one session, green on
base, and each red on its cell. So is `dg swP pc`, in its own one-access session. The same holds, reasoned and not
built, for a shrink keyed on `d->warned`: it is silent once the latch is set, and it is a joint on an lvalue the
accept body does not read, so it is clause (e).

**Side effect the next table must carry.** A pre-set mutant also silences the lh, so every table-9 pre-set kill
(the 17 that red `latch x5`) will also red `latch said`, and its score drops by one more. Re-arm kills are
unchanged, because the lh's own text still appears exactly once. The targeting rule is not triggered, because no
command list changed. Even so, the new row is floor material and needs its own targeted table.

## C2 -- measured 141/141; one free-running window refusal kills it (148/149, no other row moved)

Every free-running refusal in the probe runs from `CODE`, at 0x800010xx. The window refusals (`lb/lh/sb/sh rev`,
`rev once`, `rev said`) are all stepped, and a stepped probe cannot tell `debug` from `fatal`.

**Grade: clause (e) by the DEPENDS-ON bound.** The decline arm does not read `cpu->pc`, and the window predicate does
not dominate it. **Recommend adding `free revP said` anyway, as a licensed strengthening.** The PROM's probe loop is
the one real-world code path that issues CRIME accesses from that window, and item 3 already treats "from the
window" as a refusal cell. With C2, a narrow access from the PROM would be declined in silence in a default,
non-verbose run. The row is measured, cheap (one session), and moved nothing. At minimum the DISCLOSED list owes a
line for it: item 5's "EVERY axis of the refusal" does not name pc, and no disclosure does either.

## C3, C4, C5

* **C3 is killed in both forms**, pre-set and re-arm, at 139/141 (`mid said`, `mid once`). kimi-k3's premise, "no
  ACCEPTS entry sets bits 7/8", is TRUE. The conclusion does not follow from it, because the mid session's accepted
  `sd +0x1f8` has bits 7 and 8 set, and it runs both before the first refusal (pre-set) and between refusals (re-arm).
* **C4 is killed**, 131/141 over ten answer rows. minimax's premise, "item 9 rows the answer at named labels only",
  is FALSE. The default-arm answer rows sit at +0x07, +0x06, +0x27b, +0x27a, +0x1ff and +0x1fe, which are all
  non-8-aligned. (The label rows read `& 7` = 0 and stay green, as expected.)
* **C5 is EQUIVALENT, measured 141/141 and provable by reading.** `idata` is initialised to 0 and assigned only under
  `if (writeflag == MEM_WRITE)`. `odata` is consumed only under `if (writeflag == MEM_READ)`. So on every path the
  consumed `odata` is 0, exactly as in base. The binary differs from base because of codegen, not behaviour. No row
  is owed; one DISCLOSED line would stop it being re-raised.

## MY OWN HUNT -- denominator

**Built and swept on the 141-row probe (13 binaries):**

| class | mutants | result |
|---|---|---|
| accept-guard growth, 8-byte | CONTROL (G1), INTSTAT (G2) | escaped |
| accept-guard growth, 4-byte | CONTROL R (C1), TIME (G3), REV W (G4), INTMASK W (G5) | escaped |
| silent accept bypass | CONTROL 8 (G6) | escaped |
| latch key on address bits 7/8 | pre-set (C3p), re-arm (C3r) | killed |
| notice channel keyed on pc | C2 | escaped |
| answer source | `relative_addr & 7` (C4), `idata` (C5) | C4 killed; C5 equivalent |

**Reasoned from the per-cell table, NOT built:**
* TIME 8W growth.
* REV window 8R/8W growth.
* default `sw/lw 0x40` growth.
* a `d->warned`-keyed shrink.

**Not re-swept (earlier tables, and the disclosed list):**
* host-death reinstatement and FAULT;
* fall-through by label, width and address;
* landing, answer-register and latch-key single axes.

## Q3 -- WRONG STATEMENTS

1. **Probe header, contract item 6: "the ACCEPT SET shrunk at any single cell"** is FALSE. C1, G1, G2, G3, G4 and G5
   each scored 141/141. It holds at REV 8R/4R-window, DOG, CONTROL 4W (address+direction), INTMASK 8W/8R/4R,
   INTSTAT 4R, TIME 8R and the default +0x40/+0x278 8-byte cells. It does not hold at the cells in the table above.
2. **DISCLOSED, "ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18,
   ... +0x38"** implies that a touched slot is pinned. **Touching a cell in ACCEPTS pins its latch behaviour, never its
   acceptance.**
3. **DISCLOSED, "an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: ... no round trip there can observe
   whether the store was accepted (the CONTROL arm's effects are rowed separately as sw08 halts / sw08 msg ctl)"** is
   wrong twice:
   * At +0x00 from the PROM window, an accepted write REDIRECTS THE PC. The REV arm ignores the direction, which is
     item 3's own words, and **G4 measured it: `dg swP pc` read 0xbfc05184 against ra**.
   * The CONTROL arm's effects are rowed for 4-byte writes only. An 8-byte CONTROL write shrink is unrowed (G1).
4. **Brief, "is `ACCEPTS` now exactly the (branch side x kind) floor"**: yes for the latch class (40 + 2 + 4). The
   question as framed cannot see that the rows ACCEPTS feeds are blind to the ACCEPT side of the same 46 cells.
   **"46 kinds" is also slightly loose**: 4 are positional repeats, not kinds.
5. **Item 5's "on EVERY axis of the refusal"** has no line for the issuing pc (C2), although items 3 and 4 treat "from
   the window" as a cell.
6. **POSTTABLE 9's FLOOR line, "(d) the window x kind cross is closed"**, is true for pre-set/re-arm. Read beside
   item 6, it could suggest the accept side of the same cross is closed too, and it is not.

## What I could not check

* I did not re-run tables 1-9 against the augmented probe. The "17 pre-set kills also red `latch said`" prediction
  is reasoned from the mechanism, not measured.
* I did not build the four "reasoned" growths or the `d->warned` shrink.
* I did not check real-O2 behaviour for 64-bit CONTROL or INTSTAT access, or which widths NetBSD and the PROM use.
  The guest-visibility claims above are about the model's own answers.
* Operational note: my `killtails.sh` `pkill -f 'gxopuscrimec6_work/lane_'` also matched ten of my own idle
  wait-loops, which exited 15. Those were waiters, not measurements, and every measured leg had finished before it
  ran.

**Clone status:** `/tmp/gxopuscrimec6`, `/tmp/gxopuscrimec6_bins` and `/tmp/gxopuscrimec6_work` are **RESTORED, then
DELETED**. At deletion the source was CLEAN against SEC, the binary was newer than the source, and there was no
sentinel (`finish6.sh`). I wrote nothing into GXEMUL-SEC except this directory. I did not touch `/tmp/gxopus530c4`,
`/tmp/gxopuscrime` or `/tmp/gxlca530`.
