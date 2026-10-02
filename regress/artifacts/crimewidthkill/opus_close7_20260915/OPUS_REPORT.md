# OPUS REPORT -- #529 `crimewidthkill`, CLOSING PASS 7, measuring seat (the FINISHING instance)

**VERDICT: GAP.**  `} else if (len == 4) {` -> `} else if (len == 4 && !(writeflag == MEM_WRITE && relative_addr ==
CRIME_INTMASK && (d->warned & CRIME_W_LEN))) {` in `src/devices/dev_sgi_ip32.c` scores **157/157** on the shipped test
and loses an accepted guest store (`K1`, `logs/lane_A.out`, `logs/disc_K1_w_imask4w.out`).  Two siblings do the same at
other cells (`K2` REV 4-byte, `K3` CONTROL 8R).  It is a FLOOR breach, L2: the class is the shipped fix's OWN latch
used as an accept-guard conjunct, and it is inside the clause-(d) DEPENDS-ON closure, not outside it.  I also settle
the panel's three disputed silent cells by measurement, and the enumeration is WRONG at one of them (TIME 4W/4R).

`CRIME_CLOSE7_OPUS_20260916`

> `# CHECKPOINT -- 2026-09-15 ~07:xx   HEAD 9c91999 (records)   two rounds in flight, both UNCOMMITTED`

*(first line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`, verbatim)*

---

## 0.  WHAT THIS SEAT DID, AND WHAT IT INHERITED

The pass-7 measuring seat built twelve mutants, ran nine probe legs and two discriminator scripts, wrote `PREDICT.md`
**before** its builds, and was then terminated by an account-side weekly limit before writing a verdict.  Its
measurements survive.  I verified them against the logs, built and ran three further instruments of my own
(`scripts2/post7.py`, `post7b.py`, `post7c.py`, sixteen legs), and wrote `PREDICT2.md` before each run -- its mtime and
the two addenda are the order proof, and **two of my own predictions were wrong and are recorded as such below.**

I applied no mutant, dropped no sentinel, and wrote to no tree.  The clone `/tmp/gxopuscrimec7` and the thirteen
binaries in `/tmp/gxopuscrimec7_bins` are **left in place** (`logs2/final.out`: no `.MUTANT`; all four device/CPU
sources `cmp`-CLEAN against `GXEMUL-SEC`; `gxemul` newer than its source; the shipped probe's md5
`127a7a7e02c316db514b86afbf6800ee` identical at 11:16 and 11:36).  `build/`, `est/`, `build-asan/`, `/tmp/gxsec-build`,
`/tmp/gxopuscrime`, `/tmp/gxlca530` and `/tmp/gxopus530c5` were not touched.  `git status` shows
`M src/devices/dev_sgi_ip32.c` and `?? regress/crime_width_probe.py`: both are the ROUND's own uncommitted work
(`CHECKPOINT.md` records the fix as UNCOMMITTED), not mine -- the fix's md5 is `8c1d1545eeddd12fd49f52ccede60262`,
the same value `PREDICT.md` recorded as the baseline on 2026-09-15.

---

## 1.  THE HARVEST, VERIFIED -- and three corrections to it

Every score in `MAINLOOP_HARVEST.md` is confirmed against `logs/lane_[ABCDE].out`; every cited log ends `CRIMEP_DONE`
or `DISC7_DONE`.  The binaries are verified BEHAVIOURALLY, not by name: `logs/disc_K*.out` gives each K mutant a
distinct one-cell POST signature matching its own `mutants/*.diff`, `disc7b` does the same for E1/E2/E3b/F1/F1b/F3, and
my `post7`/`post7c` runs reproduce each signature independently on the same binaries.  F4a/F4b are identified by their
full-probe red sets, which match their diffs uniquely.

| harvest claim | verdict |
|---|---|
| base 157/157; E1 157/157; E3 156/157 {free rev said}; E3b 157/157; F1 157/157; F1b 157/157; F3 157/157; F4a 155/157 {imask ctl, gate line}; F4b 156/157 {istat ctl}; K1/K2/K3 157/157 | **all confirmed** |
| E2 157/157 with a measured guest difference (base 0xc6/0x108 6/6, E2 0x0 6/6) and item 6's TIME equivalence FALSE | **confirmed, and strengthened** -- four independent channels now measure it (below) |
| F1/F1b differ only in a HOST-LOG line (text count 2 -> 1; `CTL after ld` 0x100 on both) | **confirmed** |
| F3 differs only in the stepped default-arm WRITE line (`EQV dflt write 0x4` 1 -> 0; `EQV +4 sw->lw` 0x11 on both) | **confirmed** |
| K1-K3 are an accept guard keyed on the LATCH at one cell, declining SILENTLY once any refusal has happened | **confirmed, and the mechanism traced**: with the latch set, the grown `else if` drops the cell into the width arm, whose `if (!(d->warned & CRIME_W_LEN))` is now FALSE -- *the fix's own latch suppresses the announce of the mutant that abuses it*.  With the latch clear the mutant is INERT, which is why every latch-clear row stays green. |

### CORRECTION 1 -- *"Every value row in the 157-row probe sits in a refusal-free session"* is **FALSE**, and the
### round's own table 10 refutes it.

Derived, not asserted: `scripts2/session_map2.py` replays the shipped probe with `session()` and `row()` intercepted
and decodes each session's command list back into `(op, offset, pc)` triples.  It does not run the emulator.  Output:
**45 sessions, 72 accepted CRIME accesses issued AFTER the session's first refusal**, in eleven sessions, and **ten of
those carry a VALUE or EFFECT oracle**:

```
#18 imask   POST lw+0x18 ld+0x18   rows: imask ctl (IP2), imask keeps (value)
#19 istat   POST lw+0x10 ld+0x18   rows: istat ctl (IP2)
#21-24 time POST ld+0x38 x2 each   rows: time lb/sb/lh/sh ctl (TIME moved)
#25 keeps   POST ld+0x30 x2, sd+0x40, ld+0x40   rows: sb keeps, sh keeps, lo keeps
#26 rearm   POST all 46 ACCEPTS    rows: rearm once, rearm surv  -- NOTICE COUNT ONLY
#27 top     POST ld/lw+0x278, lw/sw+0x27c, sw+0x278, ld+0x278   rows: top8 st+ld, top4 rhi/rlo/w
#28 hi      POST ld+0x278          rows: hi keeps
#29 mid     POST ld+0x1f8, sd+0x1f8  rows: mid keeps
#30 dog     POST sd+0x38           (seed only -- no oracle in the useful direction)
#40 latch x5  firstRefusal at index 46: its 46 ACCEPTS run BEFORE the lh, POST = 0
```

**The round's own kill table 10 is the measurement that settles it**: `W_8r` -- the same `d->warned`-keyed shrink at
the WIDTH level -- scored **145/157 and reddened twelve rows**, all of them post-latch value rows
(`killtable10_20260915/PRETABLE.out`, `POSTTABLE.out`).  That is impossible if every value row were refusal-free.

**Why the correction changes the repair rather than only the record:** the closure is **not** 46 cells.  Eight of the
46 are already pinned post-latch (INTSTAT 4R, INTMASK 4R and 8R, TIME 8R, DOG 8R, default 8W and 8R at +0x40, default
8R at +0x278).  The open set is smaller and nameable -- see S4.

### CORRECTION 2 -- attribution of the TIME finding.

The harvest credits codex and says *"grok and kimi-k3 called it equivalent"*.  Both halves check out
(`grok.txt:42` tabulates TIME 4W/4R as **equivalent**; `ollama_kimi.txt:11` reasons from G3's 156 that it is
equivalent).  **It omits minimax, which also called the equivalence wrong** -- in its verdict line, independently.
Its *conclusion* is right and its *mechanism* is wrong: it argues from a "low lane" at +0x38, but at +0x38
`relative_addr & 4` is 0, so a 4-byte access there is the HIGH lane; the low lane is +0x3c, which is not a case label
and not in `ACCEPTS`.  Count the arguments, not the seats: **one seat gave the right reason (codex), one reached the
right verdict by a wrong route (minimax), two ratified the wrong claim (grok, kimi-k3).**

### CORRECTION 3 -- F4b's attribution, and two refuted seat claims.

F4b refutes **deepseek**, not "kimi-k3's query": deepseek's floor-gap claim was
`if (len == 4 && relative_addr == CRIME_INTMASK && writeflag == MEM_READ) goto crime_declined;` (its `ollama_deepseek.txt`
item 3) -- that is F4a verbatim, **measured 155/157, CAUGHT** -- and its companion guess that INTSTAT 4R is *"likely
equivalent"* is refuted by F4b at 156/157 {istat ctl}: the channel is the REASSERT, not the value.  kimi-k3 named
INTSTAT 4R too and got it RIGHT (*"in fact pinned by an incidental row, but the mapping never says so"*); crediting the
kill to it inverts who was corrected.  Minor in the harvest, load-bearing in a ledger entry.

---

## 2.  THE FIND, PINNED

### (a) HOW GENERAL THE CLASS IS -- derived from the handler, cell by cell

A silent decline at an accepted cell removes exactly three things: the `d->reg[]` update (writes), the `odata` it would
have answered (reads), and the switch arm's side effect.  Working those against the function
(`dev_sgi_ip32.c:229-231` prelude, `:275-320` width arms, `:322-409` switch, `:411-420` tail) gives, over the 46
`ACCEPTS` entries:

* **EQUIVALENT -- nothing observable at all (10 entries):** REV 8W / 4W-hi / 4R-hi out of the window (the prelude
  rewrites `reg[0]`, its high half is 0); CONTROL 4R-hi (high half of 0x100 is 0); CONTROL 4W and 8W at `0`, `0x0200`
  and `0x0100` (DOG is a local, ENDIANESS is cleared unconditionally, the leftover is 0 so nothing prints).
* **HOST-DIAGNOSTIC ONLY -- the guest cannot tell (5 entries):** CONTROL 4W and 8W at `0x0201` and `0x0001` (the
  leftover-nonzero `fatal()` line), and the default-arm 4W at `+0x04` (its `debug()` write line; the store itself lands
  in REV's low lane, which the prelude rewrites).
* **GUEST-VISIBLE (31 entries):** everything else.  The channels are the PROM-window redirect (`pc = ra`, the four
  window kinds), a nonzero register answer (REV 0x11, CONTROL 0x100, INTSTAT, INTMASK, DOG, TIME, the far and middle
  blocks), a durable store read back later (INTMASK, DOG, TIME, every default-arm slot), `crime_interrupt_reassert()`
  raising or lowering `cause.IP2` (INTSTAT and INTMASK, all four kinds each), and the skipped
  `crime_update_crime_time()` (TIME, all four kinds).

**Every one of the 31 is reachable in the K form**, because the mutant's condition is just `(d->warned & CRIME_W_LEN)`
and any session that has refused once satisfies it.  So the class is not three cells; it is thirty-one.

### (b) WHY NO SHIPPED ROW SEES IT -- and exactly which eight it does see

From S1's session map: of the 31 guest-visible cells, **eight are exercised post-latch with an oracle** and
**twenty-three are not**.  `rearm once` (#26) runs all 46 post-latch and is the reason the mutant is *reachable* in the
shipped probe -- and it counts notices only, so it is blind by construction.  `latch x5` (#40) runs its 46 BEFORE its
first refusal, so the K mutant is inert there and `latch said` stays green.

That is why K1/K2/K3 score 157/157 while a PRE/POST discriminator shows a guest difference at each
(`logs/disc_K*.out`): INTMASK 4W lost (`0x0` vs `0x1000000000000000`), the REV window redirect lost (pc `0xbfc05184`
vs ra), CONTROL 8R answering `0x0` vs `0x100` -- with the notice count 1 in every case.

> **The one sentence that generalises it:** the shipped detector measures the **latch-CLEAR** half of
> {latch} x {len} x {direction} x {label} at every cell and the **latch-SET** half at eight cells.  Table 10 closed two
> more cells of that product (`W_8r`, `W_8w`) at the WIDTH level, with no label conditioning.  **Adding the label
> conditioning is what escapes**, and the dispatch label is a floor axis here by the 2026-09-09 `sgimtedepth4dead`
> ruling, because `relative_addr` flows into `d->reg[relative_addr / 8]`, an lvalue the guarded body both reads and
> writes.

**Why this is FLOOR and not clause-(e) debt** -- the ruling's RA3 says the `d->warned`-keyed shrink is *"clause (e) by
the DEPENDS-ON bound (`d->warned` is not a field the accept bodies read)"*.  I hold that reading is wrong, and I state
the counter-argument because it is the only thing standing between GAP and DEBT:

* the clause-(d) operand-swap form draws swaps from *"fields the guarded BODY reads"*, and the guarded body of the
  width dispatch is the whole `if (len == 8) / else if (len == 4) / else` chain.  **Its `else` arm reads `d->warned`**
  (`:314`) -- a read this very fix ADDED.  The narrow reading in RA3 scopes "body" to the two ACCEPT arms only.
* the 2026-09-04 JOINT-CELLS wording enumerates joint cells *"exactly when the guarded body's own code distinguishes
  them"*; `if (!(d->warned & CRIME_W_LEN))` is literally that test, so `{clear, set}` is a body-tested partition.
* the round's own practice already agrees: RA3 **ordered the mutant BUILT** rather than disclosed, and table 10 built
  and scored it.  A class that owes a measured mutant is not being treated as prose.

Honest limit: RA3's narrow reading is defensible on its own terms, and if the adjudicator upholds it the disposition is
clause-(e) debt with three MEASURED escapes named -- not silence.  **Either way the record must stop saying the silent
form is "CAUGHT" at these cells, because it is measurably not.**

### (c) THE CHEAPEST CLOSURE -- prototyped in a COPY and MEASURED

`scripts2/post7.py` is a standalone prototype; the shipped probe was not edited (md5 identical before and after).  It
repeats the existing value checks ONCE with the latch set -- the whole structural change is one refused `lb +0x07` at
the head of the session.  Frozen before the comparison (`logs2/freeze.out`), every log ends `POST7_DONE`.

| binary | predicted (`PREDICT2.md`, written first) | **measured** | rows red |
|---|---|---|---|
| base | 23/23 | **29/29** | -- |
| K1_w_imask4w | 22/23 {p acc imask sw} | **28/29** | `p acc imask sw` 0x0 |
| K2_w_rev4 | 21/23 {p revP sw pc, p revP lw pc} | **27/29** | `p revP sw pc`, `p revP lw pc` = 0xbfc05184 |
| K3_w_ctl8r | 22/23 {p acc ctl ld} | **28/29** | `p acc ctl ld` 0x0 |
| E2_byp_time4 | 21/23 {p time 4w upd, p time 4r upd} | **29/29 -- MY PREDICTION FAILED** | none |
| E1 / E3b / F1 / F3 (negative controls) | 23/23 each | **29/29 each** | none |

*(The denominator is 29, not the 23 I predicted: I under-counted my own control rows.  Recorded as a miss.)*

**The three K escapes close, each on its own cell, with no new channel invented and no control disturbed.**  The four
negative controls stay green, so the rows measure the mutant and not the POST prefix.

#### The TIME 4W/4R cell does NOT close with this template, and finding that out took three shapes

My `p time 4w/4r upd` rows were **VACUOUS**, which is the CHANNEL-line failure this project's pre-table block exists
to catch, arriving inside my own repair prototype.  Measured, then repaired, then repaired again:

| shape | base | E2 | control | disposition |
|---|---|---|---|---|
| `post7`: POST prefix, then `ld; 4-byte; ld`, magnitude threshold | 0x10d49672 | 0x86c913c | -- | **VACUOUS** -- a factor of 2, both far above the threshold |
| `post7b` FREE: one run of `[lb, ld, 4-byte, ld]` | 0x84, 0x42 | **0x0, 0x0** | K1 0xc6, **0x0** | **FLAKY** -- a FALSE RED on a control |
| `post7b` STEP: one `step 4` of the same | 0xfba, 0x1188 | 0x8c4, 0xa92 | K1 0xce4, 0xca2 | **NON-DISCRIMINATING** |
| **`post7c` GAP: `step 2 [lb, ld]` then `step 1 [4-byte]` then `step 1 [ld]`** | **0x13414f8, 0x1348fb0** (2 runs) | **0x5ee, 0x5ac** | K1 0x13562d6/0x135de96, K3 0x1355f7c/0x135c6de | **WORKS** -- ~13,000x separation, no false red |

**Cause, established rather than guessed:** the POST prefix's own `step` runs the CPU, so `dev_crime_tick` fires and
sets `d->last_microseconds`.  After that every accepted TIME access only CATCHES UP, so skipping one HALVES the total
instead of zeroing it.  The gapped shape fuses the refusal and the first TIME read into the session's first `step`, so
TIME is still exactly 0 after it (`first ld 0x0` on all four legs) and the 4-byte access is the only thing that can
move it before the final read.

*Log-hygiene note: `laneR.sh` ran `base` twice into the same filename, so `logs2/post7c_base.out` holds run 2; both
scores are preserved in `logs2/laneR.out` and the run-1 raw values are not.  My defect, recorded.*

### The cells the closure leaves, and the cheapest way to take them

Of the 46 `ACCEPTS` entries, the prototype (4 value sessions + 2 TIME sessions, 30 rows) plus the 8 already covered
would pin **32** post-latch.  The 14 left are the 10 EQUIVALENTs (no row owed) and four others:

| left open | why | cost to take it |
|---|---|---|
| DOG 4W-high (`sw +0x30`) | my P6 writes `+0x34` but not `+0x30` | one access + one read-back row in P6 |
| CONTROL 4W `0x0001` | P2 writes the 8W form only (`acc ctl sd`) | one `sw +0x08, 0x01` + a text count in P2 |
| CONTROL 4W/8W `0x0201` | glm's and codex's cell -- HOST-DIAGNOSTIC only | one write of each + a text count, or DISCLOSE by name with F1/F1b's measurement |
| default 4W `+0x04` | kimi CLI's and codex's cell -- HOST-DIAGNOSTIC only | one `dflt(t, clean, 0x4, True)` count beside the existing read count, or DISCLOSE with F3's measurement |

Taking all four costs **~4 accesses and ~4 rows in sessions the repair already adds**, so the full post-latch closure
of every guest-visible cell is **~34 rows across 6 new sessions** -- about +2 minutes on a 15-minute probe.

**Form: SEPARATE POST sessions, not a refusal inserted into the existing ones.**  Three reasons, and the third is
decisive: (i) prepending a refusal to the existing sessions would trade the latch-SET blind half for a latch-CLEAR
blind half, since a bypass conditioned on `!(d->warned & CRIME_W_LEN)` would then escape; (ii) a second in-session copy
read positionally with `nth()` is feasible but changes the CONTROL text counts and the register economy; (iii) **new
sessions leave every existing command list untouched, so the targeting rule selects nothing and table 11 owes only its
own new mutants** -- exactly the property that kept table 10 to 40 legs.

---

## 3.  THE PANEL'S THREE DISPUTED SILENT CELLS -- settled by measurement

| cell | dispute | settled |
|---|---|---|
| **CONTROL 0x0201, 4W and 8W** | glm `ENUMERATION WRONG`, codex `U: CONTROL diagnostic`; grok/agy CLOSES | **codex and glm are RIGHT that it escapes.**  `F1`/`F1b` are their mutants (the built form adds `writeflag == MEM_WRITE`, which is behaviourally identical since `idata` is only set under `MEM_WRITE`): **157/157 each**.  The delta is HOST-LOG ONLY: the `CRIME_CONTROL: unimplemented` count drops 2 -> 1, `CTL after ld` is 0x100 on both.  **Disposition: clause-(e) DEBT, not floor** -- the guard is a MULTI-AXIS `idata` joint (DOG set AND leftover nonzero), which the 2026-09-04 pass-11 amendment puts in debt; the single-axis marginals are either equivalent (DOG alone: nothing prints) or already rowed (leftover alone: reds `acc ctl sd` / `sw08 msg ctl`).  Item 6's *"CONTROL ... 8W (acc ctl sd)"* is true at the `0x01` value only. |
| **TIME 4W and 4R** | codex `ENUMERATION WRONG`, minimax agrees (wrong reason); grok and kimi-k3 say EQUIVALENT; item 6 says EQUIVALENT | **codex is RIGHT and item 6 is MEASURED FALSE.**  `E2` is codex's mutant verbatim: **157/157**, with the difference measured on four channels -- `ld;sw;ld` free-running base 0xc6/0x108 6/6 vs E2 0x0 6/6 (`disc_*`); `P4W`/`P4R` base nonzero 6/6 vs E2 0x0 6/6 (`disc7b_*`); the `STEP time sw/lw acc` rows base LARGE vs E2 SMALL; and my gapped rows base 0x13414f8 vs E2 0x5ee.  Mechanism confirmed: a read takes `odata` BEFORE its own `crime_update_crime_time()`, so an update skipped at the 4-byte access arrives one access late.  **Disposition: guest-visible, unrowed -- and it is a SINGLE-AXIS cell, so it is floor, not debt.** |
| **default 4W at +0x04** | kimi CLI `EQUIVALENT`; codex `U: write diagnostic; guest value equivalent` | **BOTH are right about the guest and codex is right about the label.**  `F3` is their mutant verbatim: **157/157**; `EQV +4 sw->lw` reads 0x11 on base and on F3 (the prelude rewrites `reg[0]`), while the stepped default-arm WRITE line goes 1 -> 0.  So it is NOT "EQUIVALENT" simpliciter -- a channel this detector rows elsewhere does vary -- and it is not guest-visible either.  **Disposition: guest-equivalent with an unrowed host-diagnostic delta.**  `dflt ctl` counts READS at +0x04; nothing counts writes there. |

**And a fourth, which the panel raised and nobody settled: minimax's `latch said` text-collision hole does not exist.**
It asked whether any `ACCEPTS` entry is a 2-byte access at +0x06, which would make a stolen announce indistinguishable
from the lh's own.  **`ACCEPTS` contains no 1- or 2-byte access at all** -- all 46 are `sd`/`ld`/`sw`/`lw` (plus the
four `P` window kinds, which are the same four opcodes) -- so a grown guard at any `ACCEPTS` cell announces `len=4` or
`len=8` and can never satisfy `said(t, 2, 0x6, ...)`.  The generality argument holds by construction.  (codex reached
the same answer by reconstructing the command list; it is one line of the `ACCEPTS` tuple.)

---

## 4.  VERDICT ON CLOSING PASS 7, AND WHAT REPAIR 13 OWES

**GAP.**  The exact edit, and the two siblings:

```c
/* K1 -- 157/157 */  } else if (len == 4 && !(writeflag == MEM_WRITE &&
                                relative_addr == CRIME_INTMASK && (d->warned & CRIME_W_LEN))) {
/* K2 -- 157/157 */  } else if (len == 4 && !(relative_addr == CRIME_REV && (d->warned & CRIME_W_LEN))) {
/* K3 -- 157/157 */  if (len == 8 && !(writeflag == MEM_READ &&
                                relative_addr == CRIME_CONTROL && (d->warned & CRIME_W_LEN))) {
```

Each keeps the width guard and nulls its repair at one cell once the guard has fired -- clause (d)'s own shape, using
the latch the fix introduced.  The row I expected to catch each is the value row that already exists for that cell
(`acc imask sw`, `revP sw pc`, `acc ctl ld`); each is green because it is measured only with the latch clear.

**And the enumeration is WRONG at TIME 4W/4R** (item 6 and the ruling's RA1 both name it EQUIVALENT; `E2` measures it
guest-visible on four channels).  So the verdict is GAP **and** ENUMERATION WRONG; I lead with GAP because the floor
grade is what governs the disposition.

### Repair 13 owes

1. **Six POST sessions, ~34 rows** (S2c): the four `post7.py` sessions as written, the TIME pair in the **gapped**
   shape of `post7c.py` -- NOT the POST-prefix or one-run shapes, both measured unusable -- and the four extra
   accesses for DOG 4W-high, CONTROL 4W `0x0001`, CONTROL 4W/8W `0x0201` and the `+0x04` write line.  Every row's
   CHANNEL line must name its mutant AND be shown to vary under it: **mine did not, for TIME, and the prototype caught
   it only because I ran the mutant.**
2. **Table 11**, targeted: K1/K2/K3 verbatim, E2 verbatim, plus the four-axis product the new rows claim -- and, per
   the class-closure amendment, *enumerate the whole {latch} x {len} x {direction} x {label} space in ONE diff* rather
   than repairing cell by cell.  Three consecutive passes have now found one class three times (pass 6 the announced
   accept-guard growth, table 10 the width-level latch shrink, pass 7 the per-cell latch shrink); the next repair owes
   the closure, not the next cell.
3. **Four record corrections** (S5), including the ruling's own RA1 sentence.
4. **A `PRETABLE.out` for table 11 whose CHANNEL line is checked, not merely written** -- the TIME row is this pass's
   evidence that a channel can be named correctly and still not vary in the shape you row it in.

*Everything above is FILED-or-FIXED per the existing grades: (1) and (2) are L2 floor work; (3) is L4; the CONTROL
`0x0201` pair and the `+0x04` write line are clause-(e) debt and may be disclosed instead of rowed, with their
measurements cited.*

---

## 5.  WRONG STATEMENTS

**In the probe header (`regress/crime_width_probe.py`):**

1. **Item 6: *"it is EQUIVALENT at ... TIME 4W/4R (the high half is 0; updates accumulate)"*** -- **MEASURED FALSE**
   (`E2`, four channels).  The parenthetical reason is also wrong: updates do not "accumulate" back to the same value,
   because a read samples `odata` before its own update.
2. **Item 6: *"it is CAUGHT where a bypassed cell is guest-visible, by the value rows derived per cell"*** -- true of
   an UNCONDITIONAL bypass, **false of a latch-conditioned one** (K1/K2/K3, 157/157).  The sentence needs the
   qualifier, or the rows need to exist in both latch states.
3. **Item 6: *"The remaining ACCEPTS cells' accept side is pinned by the rows below"*** -- false at `sw +0x04` (F3),
   at CONTROL `0x0201` both widths (F1/F1b), and at the eight cells whose pin is an *incidental* row in another
   session that the enumeration never names (kimi-k3 and minimax both raised this; my session map lists them).

**In `killtable10_20260915/POSTTABLE.out`:**

4. ***"the silent form ... CAUGHT at the twelve guest-visible cells"*** -- the guest-visible set has **31** members, not
   twelve; the twelve are the cells the ruling ENUMERATED.  codex's independent 46-entry audit reaches the same
   conclusion from the other side.  Say "the twelve cells the ruling enumerated".

**In the brief and the ruling it quotes (`FABLE_C4_RULING_20260915.md` part A):**

5. **RA1: *"the cells where it is EQUIVALENT at the guest (REV 8W/4W/4R out of the window, CONTROL 4R, TIME 4W/4R)"***
   -- TIME 4W/4R is measured guest-visible.  The ruling is the origin of item 6's wrong sentence; correcting one
   without the other leaves the record inconsistent.
6. **RA3: *"It is clause (e) by the DEPENDS-ON bound (`d->warned` is not a field the accept bodies read)"*** --
   disputed, with the argument in S2b: the width dispatch's own `else` arm reads `d->warned`, and that read is part of
   the fix's diff.  I ask the adjudicator to rule; the measured escapes stand either way.
7. codex's finding, confirmed: the brief's *"THE MUTANTS OF TABLE 10, verbatim"* section is truncated at `.split("` and
   omits the `S_*` and `W_*` definitions -- a brief defect, not a shipped record.

**In `MAINLOOP_HARVEST.md`:** the three corrections in S1 -- the refusal-free-session over-generalisation (the
important one, because it sizes the repair), minimax's missing attribution on TIME, and F4b's inverted credit.
Also *"both killed, by the `keeps' rows"* undercounts `W_8r`: four of its twelve red rows are `time * ctl`, not keeps
rows.

**In my own work:** `p time 4w upd` / `p time 4r upd` were vacuous; my predicted denominator of 23 was 29; and
`laneR.sh` overwrote one base log.  All three are recorded above and in `PREDICT2.md`'s two addenda.

---

## 6.  ARTIFACTS

```
PREDICT.md            the walled seat's predictions, written before its builds
PREDICT2.md           mine, written before each of my runs (+2 addenda, each before the run it predicts)
MAINLOOP_HARVEST.md   the main loop's reading -- corrected in S1
logs/                 the walled seat's 9 probe legs, 13 discriminator runs, 5 lane logs
mutants/ scripts/     its 12 diffs and its frozen probe, disc7, disc7b, builders
scripts2/session_map.py, session_map2.py   the static session map (no emulator; derives S1 and S2b)
scripts2/post7.py     the repair-13 row prototype (29 rows, 6 sessions)
scripts2/post7b.py    the first TIME repair -- both shapes measured unusable
scripts2/post7c.py    the GAPPED TIME shape -- works, ~13,000x separation
scripts2/laneP.sh laneQ.sh mkfreeze.sh   frozen-copy runners
logs2/                freeze.out, 16 prototype legs (all end their sentinel), laneP_A/B, laneQ_Q, laneR, final.out
```

Clone and binaries LEFT IN PLACE, verified clean (`logs2/final.out`).
