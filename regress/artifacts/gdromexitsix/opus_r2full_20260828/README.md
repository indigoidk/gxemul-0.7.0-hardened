# Round 2 pass 1, the MEASURING seat — three escapes, and two of them I had already specified

Built in `/tmp/gxor2f`, a `cp -a` of `build/`: `cmp` clean vs SEC before mutant 1, baseline
rebuilt in-clone with `[ binary -nt source ]` checked, a `.MUTANT` sentinel on every mutation
cleared only after `cmp`-vs-SEC **and** a rebuild. Eight binaries, **eight distinct md5s**.
`git -C GXEMUL-SEC status --porcelain` empty afterwards; `est/`, `build/`, `build-asan/` all
`cmp`-identical to SEC.

*The seat's own first md5 attempt silently produced eight empty-string hashes through a
quoting path, and it re-ran from a script file. Worth recording: that is the third time today
a shell-quoting chain produced a confident wrong answer, and the second time the remedy was
"write it as a real file".*

## SENTINEL AUDIT — run before citing any number here

| log | sentinel | complete? |
|---|---|---|
| `gxor2f_out_{fixed,M_retA,Ma_toclen,Mb_toclen,M_braceA,M_growA}.txt` | `TPROBE3_DONE` | **YES** |
| `gxor2f_pio_{fixed,M_growA,M_growB}.txt` | `GDROMPIO_VECTOR=` | **YES** |
| `finish_braceA_crossbit_pio.log` | `FINISH_DONE` | **YES** |
| `gxor2f_out_base.txt` | none — ends mid-row at `S1 mount` | **NO — truncated at source** (619 b, verified against the seat's own scratchpad) |

The truncated one is the PRE-FIX baseline and its load-bearing rows landed before the cut:
`S1 unkcmd` and `S1 badfmt` both read **`exit1`**, so both sites reproduce on the committed
build. Nothing below depends on the rows that were lost.

## THE VERDICT

**The product fix is correct, and `break` is right at both sites — measured, not argued.**
On `fixed`, `S1 badfmt` reads `CNT=0x0` after the guest staged `CNTLO/CNTHI = 408`. Since
`GDROM_CNTLO` returns `d->cnt & 0xff`, that `0x0` can only have come from the common tail's
`else` branch. Host alive, event set, diagnostic exactly once.

**The 13-row detector committed at `eae8c8c` is NOT ready.** Three mutants leave it green.

| mutant (one edit over the fix) | measured | status |
|---|---|---|
| `M_retA` Site A `break;`→`return;` | `S1 badfmt` **CNT 0x0→0x98** | **caught** by `fmt cnt` |
| **`Ma_toclen`** Site A latch bit → `GDROM_W_TOCLEN` | `S5 toc+fmt` **`fmtD` 1→0, `fmtB` 1→0** | **ESCAPES** |
| **`Mb_toclen`** Site B latch bit → `GDROM_W_TOCLEN` | `S6 toc+unk` **`unk` 1→0** | **ESCAPES** |
| **`M_braceA`** Site A `break` inside the latch `if` | `S2 fmt x2` **`fmtD`=1, same as fixed**; only `rej` 0→1 | **ESCAPES** |
| `M_growA` `!= 0x20` → `!= 0x21` | `S4 acceptA` **`huh` 1→0** | caught — `acceptA` is FAILABLE |

## *** THE FINDING THAT IS ABOUT PROCESS, NOT CODE ***

**Both escaping mutants were named in this round's own `PRETABLE.out` at 16:05, as `M5` and
`M4`, with the rows `crossbit` and `latch cond` prescribed for them. Both rows were DROPPED
when the 18:45 addition list was written.**

Nothing was forgotten in the sense of never known. The knowledge was in the round's own
artifact, three hours old, and it did not survive the rewrite of a list in a different
artifact. That is the carrier's *"knowledge living where nobody consults it at row-writing
time"* — except here it was living in the file that exists precisely to be consulted at
row-writing time.

> **A ROW LIST REWRITTEN FROM A PANEL'S FINDINGS MUST BE DIFFED AGAINST THE PRE-TABLE BLOCK'S
> OWN PRESCRIBED ROWS, NOT ONLY EXTENDED WITH THE NEW ONES.** The 18:45 list correctly added
> everything four seats had just found and silently lost two rows the same document already
> owed.

## THE CROSS-BIT ESCAPE IS THE WORST, AND THE SURFACE IS BIGGER THAN THE ROUND TESTS

After a short TOC sets `GDROM_W_TOCLEN`, the Site-A decline prints **nothing at all** — the
bounded-announce guarantee gone, a silent refusal. Invisible to any session that does not
first decline a TOC, and no row in any of the four gdrom probes builds that state.

**`d->warned` has seven live writers today; the fix makes nine sites sharing one field, and
the round tests exactly one pair (A×B, via `M3shared`).** Six of the seven existing bits are
set from ordinary register reads — `GDROM_W_OVERREAD` is set by the benign
TOC-then-Mount-then-read sequence `gdrompio`'s own `staged quiet` row exercises. **A collision
with that bit would be silenced by completely normal guest traffic.**

> **AND THIS IS WHY THE GUARD-FIELD PRE-TABLE CHECK FOUND NOTHING.** That check asks where the
> guard field and the body field *differ*. Here they are the **same** field. For a shared
> bitfield the right question is *"who else writes this field, and can they set my bit?"* —
> one `grep -c 'd->warned |='`, and it is the check that would have caught this.

## ROWS OWED — two sessions, both bounded

* **`crossbit`** — short TOC (cnt 407) → bad format → unknown command, asserting all three
  declines fire. Covers both new bits at once. Extend it to touch `GDROM_W_OVERREAD` and
  `GDROM_W_NODATA` first and one session covers the whole collision surface instead of N².
* **`latch cond`** at Site A — in the `fmt x2` session, read a decline channel *after the
  second command*. Measured discriminator: `rej == 0`.

**A staging constraint on `fmt cnt` that would have made it vacuous:** `M_retA`'s `S3 both`
measured **`CNT=0x0` — it escapes**, because the unknown command ran first and its tail had
already zeroed `cnt`. **The CNT channel discriminates only when `d->cnt` is non-zero on entry
to the declined command**, so `fmt cnt` must not live in the `both sites` session. Write
`CNTLO/CNTHI` directly, then the bad-format packet — one command then carries both `fmt cnt`
and `fmt event`, and the single-command form is also what `fmt event` needs, since
`pending_irq` is sticky and a staging TOC would pre-set the bit.

## THE ACCEPT SIDE, MEASURED RATHER THAN COUNTED

| predicate | covered? |
|---|---|
| `cmd[0]==0x14` | **YES**, strongly |
| `cmd[0]==0x70` | **YES — measured**: `gdrompio vs M_growB` = 12/13, red on `staged quiet` |
| `cmd[1]==0x20` | **NO — measured**: `gdrompio vs M_growA` = 13/13, fully blind |
| `cmd[0]==0x30` *completing* | **NO** |
| `cmd[1]==0x24` | **NO** |

`gdrompio vs fixed` = **13/13** — the fix does not regress the existing gated detector.

**`acceptA` does not discharge `0x30`'s accept side**: its oracle is `Huh?`, a diagnostic on
the *reject* path one guard later, so it proves the arm was ENTERED, never that it COMPLETES.
The completing packet already exists — `gdrompio`'s `CMD_READ`, `sector_count=1`, `cnt=0`.

## CORRECTIONS TO MY OWN CLAIMS

* **`gdromonce` does NOT close for free.** I wrote that putting `(once)` in the new regexes
  discharges it. It does not: that row names one specific regex in a *different* file
  (`gdrom_toclen_probe.py`'s `DECLINE`). The marker gets pinned at the new sites and the filed
  row stays open.
* **The decline regexes must be ANCHORED, and the reason is measured.** On `fixed`, `S7 fmt24`
  reads `fmtB=1, fmtD=0, f24=1`: the bare `unimplemented data format` matches BOTH the P5
  `0x24` warn-and-continue line and the new decline, because the fix's message contains that
  substring. Anchor on `-- declined`.
* **The death-mode obligation is still owed.** `how` now returns from 37 call sites and **no
  row asserts on it** — the only `exit0` in the whole file is inside a comment. The plumbing
  landed; the oracle did not.

## A SEAT DISAGREEMENT, SETTLED BY MEASUREMENT RATHER THAN RANK

This seat states the row-name limit is **≤12**; the codex seat states it is **not** 12. The
format string decides:

    12 chars -> 3 trailing spaces   `^name  ` MATCHES
    13 chars -> 2 trailing spaces   MATCHES

**13 is the limit.** `%-14s` plus the literal space in the format leaves exactly the two
spaces the gate needs. *Seat rank does not settle fact — the measurement does, and it took
four lines.*

## SCOPE NOTES

* New rows should go in a **new probe with its own gate section and denominator**, per
  `#489`'s precedent — that sidesteps the 58→71 coupling entirely. Only `stale quiet` and the
  death-mode rows must land in `gdrom_default_probe.py`.
* Four `fatal()`s in `case 0x30` stay unlatched and guest-drivable after this fix (the `0x24`
  warn, `rejecting sector_count`, `Huh?`, `diskimage_access failed`) — the `floodclass`
  family. Two of them are used as oracles by `fmt cont` and `acceptA`, so a future latching
  round will interact with these rows. Worth one contract line.
* `dev_dreamcast_gdrom.c` is not on `tools/est_divergence.txt` and is byte-identical today, so
  the fix must land in **both** `GXEMUL-SEC/` and `est/`.
