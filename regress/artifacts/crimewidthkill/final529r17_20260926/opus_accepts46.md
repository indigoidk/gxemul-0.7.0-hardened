OPUS_SEAT_ALIVE_20260926_529acc
# CHECKPOINT -- 2026-09-26 09:35 (087a90 sections rewritten; the peer's sections below are untouched)

**VERDICT: repair 13's 23 / 8 / 10 / 5 is reproduced exactly, and every member now has a name.  The two unnamed
HOST-DIAGNOSTIC members are entries 11 and 15 (CONTROL 0x0001, 4W and 8W).  The six unnamed EQUIVALENT members are
12, 13, 16, 17, 43 and 44 (CONTROL writes of 0, 0x0200 and 0x0100).  The counts no longer describe r17, though.  Now:
31 GUEST-VISIBLE (30 rowed in both latch states; entry 34, `sd +0x40`, rowed only with the latch SET); 4 ROWED on the
CONTROL-text count in both states (10, 11, 14, 15); 1 HOST-DIAGNOSTIC ONLY (40); 10 EQUIVALENT.  All 92 entry x latch
cells were MEASURED, and 92 of 92 matched predictions written before any run.**

## READ versus RAN

* **Instrument:** `final529r17_20260926/crime_width_probe.r17.py`, **md5 `2fe7123b`**, 226 rows in 68 sessions.
  * Its code equals table 16's `crime_width_probe.table16.py` (`5f770991`) except three row NOTES (comment-stripped
    diff).
  * **I did NOT use `regress/crime_width_probe.py` (`a0af7c92`, the 204-row repair-14 probe).**
  * Before the published file existed I froze the scratchpad copy `p529/r17/crime_width_probe.r17.py` (`064aca65`,
    08:25).  It differs from `2fe7123b` only at docstring lines 472-480, below the bucket block, and every
    measurement below ran on `2fe7123b`.
* **Source:** `GXEMUL-SEC/src/devices/dev_sgi_ip32.c`, md5 `8c1d1545` (the working tree, i.e. the #529 fix).
  Citations `:NNN` below are into that file at that md5.
* **READ:**
  * every session and row of the probe;
  * `DEVICE_ACCESS(crime)` and its tick, reassert, time-update and init functions;
  * `killtable11_20260916/PRETABLE.out` (repair 13);
  * `opus_close7_20260915/OPUS_REPORT.md` sections 1-3 and `MAINLOOP_HARVEST.md`;
  * `repair14_20260916/BUCKETS8_rerun.out`, `opus_adj_work/logs/b12.out` and `opus_pass1.md` sections 4-5;
  * table 16's run log;
  * the two 09-25 re-rulings in `rerule_20260925/`.

  A static session map (`smap17.py`, no emulator) gave every ACCEPTS entry's matching accesses by session and latch
  state.
* **RAN, in a WSL scratch clone only.**  The clone is `/tmp/gxopus_acc46`, a `cp -a` of table 16's clone
  `/tmp/gxopus_r14`, which was only read and is still clean.  No project tree was written except this file.
  1. **Build and restore.**
     * `dev_sgi_ip32.c` was cmp-clean against GXEMUL-SEC, and `src/cpus/*.o` was removed before building.
     * The rebuilt base is **`b5b99e6d`, byte-identical to table 16's base binary**, so table 16's 226/226 base leg is
       this binary's.
     * One measurement-only mutant was built as `envmut` (`858bfb4c`).
     * The clone was then restored: rebuilt byte-identical to base, cmp-clean, binary newer than source, `.MUTANT`
       cleared.
  2. **The mutant** (`mut46.py`, `8c87dc3b`).
     * It is a 66-line block inserted immediately before `if (len == 8) {`, the placement of table 16's
       `G_glm_tim4clear`.
     * It sends an access named by `$ACC46` straight to `crime_declined` with **no announce and the latch untouched**,
       and marks each hit on stderr.
     * That makes it a SILENT decline, keyed on the exact access kind and on the latch state at the access.
  3. **Capture.**  The full probe on `envmut` with `ACC46` unset gave **226/226, CRIMEP_CONTROL=OK, 1243 s**.  That run
     is the inertness leg.  Its 68 transcripts (all clean, one init marker each, zero hits) are the replay cache.
  4. **92 replays**, 46 entries x {latch CLEAR, latch SET}.
     * Each replay re-runs every session that holds a matching access in that latch state.  The other sessions are
       served from the capture, on which the mutant is inert by construction.
     * For the 31 guest-visible entries, `rearm *` (S38) and `latch *` (S52) were served from the capture **by
       declaration**, printed as `FROMCACHE` in each log.  The derivation: those sessions' rows are two notice counts,
       a RAM trip and the CONTROL-text count.  None of them can move when an access that prints no CONTROL text is
       declined silently.
     * For the 15 entries whose disposition rests on those two sessions, S38 and S52 were **re-run**.  Those are the
       ten EQUIVALENT entries, entry 40, and the four text-printing CONTROL writes.
     * Every re-run session's observed hit count equals its statically predicted match count.
  5. **Order proof.**  `PREDICT46.out` (08:48:04, md5 `24c95593`) predates `build46.sh` (08:48:10) and every run.
     **Result: 92 of 92 EXACT** (`SUM46.out`, `d1d57a9e`).

## The unit

An entry is (width, direction, CRIME offset).  At +0x00 it also includes the PROM-window flag (the `P` kinds).  For a
CONTROL (+0x08) write it also includes the stored value.

"Declined" means every probe access of that kind, in that latch state, is sent silently to the common tail.

* With the latch SET, that is the K form: a grown accept guard can only be silent there.
* With the latch CLEAR, it is the G6 bypass form.
* The ANNOUNCED latch-CLEAR form (a grown accept guard that announces) is caught at all 46 entries by `latch said`
  (item 6).  It is not this table's subject and was not re-measured here.

`[C]` marks a CONTROL row: its kill also reads `CRIMEP_CONTROL=FAIL`.  Entries 1-4 are issued from ordinary code,
outside the PROM window.  The table is rendered by `mk_table46.py` from `runs/k<NN><C|S>.raw`, not transcribed.

## Q1 -- the 46 ACCEPTS entries, disposition NOW (r17)

| # | access | label, lane | latch CLEAR: rows red under a silent decline | latch SET: rows red | disposition NOW | channel / derivation | repair 13's bucket | replay (C / S) |
|---|---|---|---|---|---|---|---|---|
| 1 | `sd +0x0` | REV | -- | -- | EQUIVALENT | derivation E-REV | 10 EQUIV | 226/226 exact / 226/226 exact |
| 2 | `ld +0x0` | REV | `acc8 near` | `p rev ld` | ROWED -- guest channel, both states | value 0x11 | 23 p-rowed | 225/226 exact / 225/226 exact |
| 3 | `sw +0x0` | REV, high lane | -- | -- | EQUIVALENT | derivation E-REV | 10 EQUIV | 226/226 exact / 226/226 exact |
| 4 | `lw +0x0` | REV, high lane | -- | -- | EQUIVALENT | derivation E-REV | 10 EQUIV | 226/226 exact / 226/226 exact |
| 5 | `lw +0x0` from the PROM window | REV, high lane | `rev pc ctl` [C] | `p revP lw pc` | ROWED -- guest channel, both states | PROM-window redirect (pc = ra) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 6 | `sw +0x0` from the PROM window | REV, high lane | `revP sw pc` | `p revP sw pc` | ROWED -- guest channel, both states | PROM-window redirect | 23 p-rowed | 225/226 exact / 225/226 exact |
| 7 | `sd +0x0` from the PROM window | REV | `revP sd pc` | `p revP sd pc` | ROWED -- guest channel, both states | PROM-window redirect | 23 p-rowed | 225/226 exact / 225/226 exact |
| 8 | `lw +0x8` | CONTROL, high lane | -- | -- | EQUIVALENT | derivation E-CTL4R | 10 EQUIV | 226/226 exact / 226/226 exact |
| 9 | `ld +0x8` | CONTROL | `acc ctl ld` | `p acc ctl ld` | ROWED -- guest channel, both states | value 0x100 | 23 p-rowed | 225/226 exact / 225/226 exact |
| 10 | `sw +0x8 = 0x0201` | CONTROL, high lane | `ctldog sw msg`, `latch ctl msg` | `rearm ctl msg`, `p acc ctl msg` | ROWED -- host-text channel, both states | CONTROL-arm fatal() text, counted | 5 HOST-DIAG | 224/226 exact / 224/226 exact |
| 11 | `sw +0x8 = 0x0001` | CONTROL, high lane | `sw08 msg ctl` [C], `ctlrst sw msg`, `latch ctl msg`, `rst 4w msg` | `rearm ctl msg`, `p acc ctl msg` | ROWED -- host-text channel, both states | CONTROL-arm fatal() text, counted | 5 HOST-DIAG | 222/226 exact / 224/226 exact |
| 12 | `sw +0x8 = 0x0000` | CONTROL, high lane | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 13 | `sw +0x8 = 0x0200` | CONTROL, high lane | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 14 | `sd +0x8 = 0x0201` | CONTROL | `ctldog sd msg`, `latch ctl msg` | `rearm ctl msg`, `p acc ctl msg` | ROWED -- host-text channel, both states | CONTROL-arm fatal() text, counted | 5 HOST-DIAG | 224/226 exact / 224/226 exact |
| 15 | `sd +0x8 = 0x0001` | CONTROL | `ctlrst sd msg`, `latch ctl msg`, `acc ctl sd`, `rst 8w msg` | `rearm ctl msg`, `p acc ctl msg` | ROWED -- host-text channel, both states | CONTROL-arm fatal() text, counted | 5 HOST-DIAG | 222/226 exact / 224/226 exact |
| 16 | `sd +0x8 = 0x0000` | CONTROL | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 17 | `sd +0x8 = 0x0200` | CONTROL | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 18 | `sd +0x10` | INTSTAT | `istw sd` | `p istw sd` | ROWED -- guest channel, both states | reassert raises IP2 | 23 p-rowed | 225/226 exact / 225/226 exact |
| 19 | `ld +0x10` | INTSTAT | `acc istat ld` | `p acc istat ld` | ROWED -- guest channel, both states | value (INTSTAT) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 20 | `sw +0x10` | INTSTAT, high lane | `istw sw` | `p istw sw` | ROWED -- guest channel, both states | reassert raises IP2 | 23 p-rowed | 225/226 exact / 225/226 exact |
| 21 | `lw +0x10` | INTSTAT, high lane | `acc istat lw` | `istat ctl` [C], `p acc istat lw` | ROWED -- guest channel, both states | value (INTSTAT high lane); SET also the reassert (IP2) | 8 incidental | 225/226 exact / 224/226 exact |
| 22 | `sd +0x18` | INTMASK | `imask ctl` [C], `imask keeps`, `istat ctl` [C], `gate line` [C], `istw sd`, `istw sw` | `p istw sd`, `p istw sw`, `p imask st+ld` | ROWED -- guest channel, both states | stored INTMASK: read back, and the IP2 it enables | 23 p-rowed | 220/226 exact / 223/226 exact |
| 23 | `ld +0x18` | INTMASK | `acc imask sw` | `imask keeps`, `p acc imask sw`, `p imask st+ld` | ROWED -- guest channel, both states | value (INTMASK) | 8 incidental | 225/226 exact / 223/226 exact |
| 24 | `sw +0x18` | INTMASK, high lane | `acc imask sw` | `p acc imask sw` | ROWED -- guest channel, both states | stored lane, read back | 23 p-rowed | 225/226 exact / 225/226 exact |
| 25 | `lw +0x18` | INTMASK, high lane | `gate line` [C] | `imask ctl` [C] | ROWED -- guest channel, both states | reassert raises IP2 (CONTROL rows only) | 8 incidental | 225/226 exact / 225/226 exact |
| 26 | `sd +0x30` | DOG | `acc8 st+ld`, `acc4 rhi`, `acc4 rlo`, `acc4 wlo`, `sb keeps`, `sh keeps` | `p dog st+ld`, `p dog rhi`, `p dog rlo`, `p dog wlo` | ROWED -- guest channel, both states | stored DOG, read back | 23 p-rowed | 220/226 exact / 222/226 exact |
| 27 | `ld +0x30` | DOG | `acc8 st+ld`, `acc4 wlo`, `acc4 whi` | `sb keeps`, `sh keeps`, `p dog st+ld`, `p dog wlo`, `p dog whi` | ROWED -- guest channel, both states | value (DOG) | 8 incidental | 223/226 exact / 221/226 exact |
| 28 | `sw +0x30` | DOG, high lane | `acc4 whi` | `p dog whi` | ROWED -- guest channel, both states | stored lane, read back | 23 p-rowed | 225/226 exact / 225/226 exact |
| 29 | `lw +0x30` | DOG, high lane | `acc4 rhi` | `p dog rhi` | ROWED -- guest channel, both states | value (DOG high lane) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 30 | `sd +0x38` | TIME | `acc time sd` | `p acc time sd` | ROWED -- guest channel, both states | stored TIME, parity | 23 p-rowed | 225/226 exact / 225/226 exact |
| 31 | `ld +0x38` | TIME | `acc time sd`, `c t4w gap`, `c t4r gap` | `time lb ctl` [C], `time sb ctl` [C], `time lh ctl` [C], `time sh ctl` [C], `tl lb ctl` [C], `tl sb ctl` [C], `tl lh ctl` [C], `tl sh ctl` [C], `p acc time sd`, `p t4w gap`, `p t4r gap` | ROWED -- guest channel, both states | value / TIME update | 8 incidental | 223/226 exact / 215/226 exact |
| 32 | `sw +0x38` | TIME, high lane | `c t4w gap` | `p t4w gap` | ROWED -- guest channel, both states | TIME update (gapped) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 33 | `lw +0x38` | TIME, high lane | `c t4r gap` | `p t4r gap` | ROWED -- guest channel, both states | TIME update (gapped) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 34 | `sd +0x40` | default | -- | `lo keeps` | ROWED -- guest channel, latch SET ONLY | stored slot, read back -- latch SET only | 8 incidental | 226/226 exact / 225/226 exact |
| 35 | `ld +0x40` | default | `acc 40 sw` | `lo keeps`, `p acc 40 sw` | ROWED -- guest channel, both states | value (+0x40) | 8 incidental | 225/226 exact / 224/226 exact |
| 36 | `sw +0x40` | default, high lane | `acc 40 lw`, `acc 40 sw` | `p acc 40 lw`, `p acc 40 sw` | ROWED -- guest channel, both states | stored lane, read back | 23 p-rowed | 224/226 exact / 224/226 exact |
| 37 | `lw +0x40` | default, high lane | `acc 40 lw` | `p acc 40 lw` | ROWED -- guest channel, both states | value (+0x40 high lane) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 38 | `sw +0x34` | default (DOG's register), low lane | `acc4 wlo`, `acc4 whi` | `p dog wlo`, `p dog whi` | ROWED -- guest channel, both states | stored lane, read back | 23 p-rowed | 224/226 exact / 224/226 exact |
| 39 | `lw +0x34` | default (DOG's register), low lane | `acc4 rlo` | `p dog rlo` | ROWED -- guest channel, both states | value (DOG low lane) | 23 p-rowed | 225/226 exact / 225/226 exact |
| 40 | `sw +0x4` | default (REV's register), low lane | -- | -- | HOST-DIAGNOSTIC ONLY | derivation H-40: an uncounted debug() WRITE line | 5 HOST-DIAG | 226/226 exact / 226/226 exact |
| 41 | `lw +0x4` | default (REV's register), low lane | `devsig` [C], `dflt ctl` [C] | `p rev lw4` | ROWED -- guest channel, both states | value 0x11; the default-arm READ line | 23 p-rowed | 224/226 exact / 225/226 exact |
| 42 | `ld +0x0` from the PROM window | REV | `revP ld pc` | `p revP ld pc` | ROWED -- guest channel, both states | PROM-window redirect | 23 p-rowed | 225/226 exact / 225/226 exact |
| 43 | `sw +0x8 = 0x0100` | CONTROL, high lane | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 44 | `sd +0x8 = 0x0100` | CONTROL | -- | -- | EQUIVALENT | derivation E-CTLW | 10 EQUIV | 226/226 exact / 226/226 exact |
| 45 | `sd +0x278` | default | `top8 st+ld`, `top8 clear`, `top4 rhi`, `top4 rlo`, `hi keeps` | `p top st+ld` | ROWED -- guest channel, both states | stored slot, read back | 23 p-rowed | 221/226 exact / 225/226 exact |
| 46 | `ld +0x278` | default | `top8 clear` | `top8 st+ld`, `top4 w`, `hi keeps`, `p top st+ld` | ROWED -- guest channel, both states | value (+0x278) | 8 incidental | 225/226 exact / 222/226 exact |

| disposition NOW | entries |
|---|---|
| ROWED -- guest channel, both states | 30 |
| EQUIVALENT | 10 |
| ROWED -- host-text channel, both states | 4 |
| ROWED -- guest channel, latch SET ONLY | 1 (entry 34) |
| HOST-DIAGNOSTIC ONLY | 1 (entry 40) |

Every count here is derived from the logs by `analyze46.py` (`ANALYZE46.out`), not tallied by hand.

## Q2 -- repair 13's buckets, member by member, and the counts now

**Repair 13's partition is exactly reconstructible.**  The close-7 report named every member: section 2(a) the ten
EQUIVALENT and five HOST-DIAGNOSTIC by class, and section 1 the eight post-latch pins.  The docstring kept the counts
and dropped most of the names.

* **23 ROWED post-latch by `p *` sessions:** 2 5 6 7 9 18 19 20 22 24 26 28 29 30 32 33 36 37 38 39 41 42 45.
  All 23 still hold a `p *` row with the latch SET (measured).
* **8 ALREADY PINNED post-latch, incidentally:** 21 23 25 27 31 34 35 46.  Each still has its non-`p` latch-SET row
  (measured):
  * 21: `istat ctl`
  * 23: `imask keeps`
  * 25: `imask ctl`
  * 27: `sb keeps`, `sh keeps`
  * 31: the eight `time/tl * ctl` rows
  * 34 and 35: `lo keeps`
  * 46: `top8 st+ld`, `top4 w`, `hi keeps`
* **10 EQUIVALENT:** 1 3 4 8 12 13 16 17 43 44.  **The six unnamed ones are 12, 13, 16, 17, 43, 44.**  Repair 15's
  block names 13 and 17 as equivalent, but never as members of this count.
* **5 HOST-DIAGNOSTIC:** 10 11 14 15 40.  **The two unnamed ones are 11 and 15, CONTROL 0x0001 at 4W and 8W.**

**THE COUNTS NO LONGER DESCRIBE r17.  Per entry and per latch state:**

| now | n | members | against repair 13 |
|---|---|---|---|
| GUEST-VISIBLE, rowed in both latch states | 30 | the 31 below, less 34 | -- |
| GUEST-VISIBLE, rowed latch-SET only | 1 | 34 | see "found on the way" (1) |
| *(guest-visible total)* | *31* | 2 5 6 7 9 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 41 42 45 46 | = repair 13's 23 + 8 |
| ROWED on the host-text channel, both states | 4 | 10 11 14 15 | were 4 of the 5 HOST-DIAGNOSTIC |
| HOST-DIAGNOSTIC ONLY | 1 | 40 | the 5th |
| EQUIVALENT | 10 | 1 3 4 8 12 13 16 17 43 44 | unchanged |

With the latch SET, 29 of the 31 guest-visible entries are held by a `p *` row.  The exceptions are 25 (held only by
`imask ctl`, a CONTROL row) and 34 (held only by `lo keeps`).

## Q3 -- replacement text for the bucket block

**Replace** `crime_width_probe.r17.py` (`2fe7123b`) **lines 236-262 inclusive**: from the line beginning
`is the INTERSECTION.  Over the 46 ACCEPTS entries:` through `    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).`
Replace them with the block below.  It has no triple quote and no backslash, every line is 116 columns or fewer, and
it keeps the file's `` `name' `` quoting.

**Splice-tested (RAN, on this final text):** `splice46.py` applied the block (`replacement_final.txt`, `9fb6a9a8`) to
a scratch copy of `2fe7123b`, producing `r17_spliced.py` (`93af64ba`).  The result parses, its code (the AST minus
the docstring) is identical to `2fe7123b`'s, and the docstring grows from 485 to 521 lines.

**Precondition (the volatile-path rule):** copy my scratchpad directory
`...\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\opus_acc46\` to `final529r17_20260926/opus_acc46/` BEFORE this
text lands.  The text cites that path.

```
is the INTERSECTION.  Over the 46 ACCEPTS entries (numbered 1-46 in ACCEPTS order), AS REPAIR 13 PARTITIONED THEM
(killtable11_20260916/PRETABLE.out, from the close-7 seat's cell-by-cell derivation, opus_close7_20260915/
OPUS_REPORT.md sections 1-2, which named every member -- this record kept the counts and dropped the names):

    23  ROWED HERE, post-latch, by the `p *' sessions below (the REV window, the value session, the INTSTAT reassert
        channel, the TIME pair, and the residual ACCEPT cells).  Every one runs AFTER a refused lb at +0x07, so the
        latch is SET while the row is measured -- which is the whole point.
            2 5 6 7 9 18 19 20 22 24 26 28 29 30 32 33 36 37 38 39 41 42 45
     8  ALREADY PINNED post-latch by an incidental access in an existing session:
            21 `istat ctl'    23 `imask keeps'    25 `imask ctl'    27 `sb keeps', `sh keeps'    31 `time * ctl'
            34 and 35 `lo keeps'    46 `top8 st+ld', `top4 w', `hi keeps'
    10  EQUIVALENT at the guest -- nothing to observe, so no row is owed or possible:
            1 3 4    REV 8W, 4W, 4R from outside the PROM-probe window
            8        CONTROL 4R (the high lane)
            12 16    CONTROL writes of 0          13 17    of 0x0200          43 44    of 0x0100    (4W, 8W)
     5  HOST-DIAGNOSTIC ONLY: clause-(e) debt, "DISCLOSED with its measurements RATHER THAN ROWED":
            10 14    CONTROL 0x0201 (4W, 8W): F1/F1b, 157/157 on the 157-row test -- the `unimplemented' count
                     drops to one, `CTL after ld' is 0x100 either way
            11 15    CONTROL 0x0001 (4W, 8W)
            40       `sw +0x04': F3, 157/157 -- guest-equivalent; `dflt ctl' counts READS at +0x04 and nothing
                     counts writes there
    --
    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).

*** THE 5-ENTRY LINE NAMED ONLY 10, 14 AND 40 AND THE 10-ENTRY LINE NAMED NONE (1, 3, 4, 8 were named elsewhere in
this contract, and since repair 15 so are 13, 17, but never as this count's members) -- grok, closing pass 8, "NAMED
ONLY THREE CELLS AGAINST A COUNT OF FIVE"; minimax, "4 are named; 6 are not".  The block ended "OWED: enumerate both
buckets member by member from session_map2.py's output, or state that the counts are derived and the members
unlisted".  The 09-25 re-rulings split on it -- the flagship: FILE "the eight unlistable bucket members"; GPT-6
Astra: "an L4 enumeration correction and justified dispositions, not blanket filing as coverage debt"
(rerule_20260925/).  THIS IS THAT CORRECTION.  The members were never unlistable: the two unnamed host-diagnostic
members are 11 and 15, the six unnamed equivalent members 12, 13, 16, 17, 43 and 44.  And the OWED line named the
wrong source -- session_map2.py maps SESSIONS and cannot emit a bucket member.  Grok's second point ("rather than
rowed" is STALE) was wider than stated: `p acc ctl msg' counted 10, 11 AND 15 from repair 13, and 14 from
repair 14. ***

*** AND REPAIR 13'S COUNTS NO LONGER DESCRIBE THIS PROBE.  Per entry AND per latch state, as of repair 16, every one
of the 92 cells MEASURED by a SILENT decline of exactly that access, scored against a prediction written before it
ran (92 of 92 exact): final529r17_20260926/opus_accepts46.md (the table), logs in
final529r17_20260926/opus_acc46/. ***
    31  GUEST-VISIBLE.  Latch SET: all 31 ROWED -- 29 by a `p *' row; 25 only by `imask ctl', 34 only by `lo keeps'.
        Latch CLEAR: 30 ROWED -- and ENTRY 34 (`sd +0x40') IS NOT: both of its latch-CLEAR drivers, `latch x5' and
        the latch-CLEAR value session (`acc ctl ld' .. `acc ctl sd'), store 0 into a slot that holds 0, so its
        decline moves no row.  Its LABEL is rowed latch-CLEAR at +0x278 (entry 45: `top8 clear', `top8 st+ld',
        `top4 rhi', `top4 rlo', `hi keeps'); the offset alone is the unrowed-slot class disclosed below -- touching
        a slot is not pinning it.  Four cells are held ONLY by CONTROL rows, so a kill there reads
        CRIMEP_CONTROL=FAIL: 5 latch-CLEAR (`rev pc ctl'), 41 latch-CLEAR (`devsig', `dflt ctl'), and 25 in both
        states (`gate line'; `imask ctl').
     4  ROWED ON THE HOST-TEXT CHANNEL, BOTH LATCH STATES: 10, 11, 14, 15.  A decline changes only the arm's
        `CRIME_CONTROL: unimplemented' fatal() -- the prelude rewrites CONTROL before anything can read the store.
        `latch ctl msg' counts it latch-CLEAR and `rearm ctl msg', `p acc ctl msg' latch-SET, beside per-entry
        latch-CLEAR rows (`ctldog sw/sd msg', `sw08 msg ctl', `acc ctl sd', `ctlrst sw/sd msg', `rst 4w/8w msg').
        So "HOST-DIAGNOSTIC ONLY: clause-(e) debt" is FALSE of all four: post-latch since repair 13 (10, 11, 15) and
        repair 14 (14), and in both latch states since repair 15.
     1  HOST-DIAGNOSTIC ONLY: 40, `sw +0x04' -- the default arm's stepped debug() WRITE line, which no row counts
        (`dflt ctl' counts the READ line); the store lands in REV's low lane, which the prelude rewrites before any
        read.  Clause (e).
    10  EQUIVALENT, the same ten, and NOTHING differs, host text included: REV's arm acts only from the PROM-probe
        window and CONTROL's only on a write; a CONTROL write whose residue after the DOG and ENDIANESS clears is 0
        prints nothing; a 4-byte read at +0x00 or +0x08 takes a high lane that holds 0; and CRIME_REV and
        CRIME_CONTROL are rewritten by the prelude of every access and read by no other function.
    --
    46
```

## The derivations (READ from `DEVICE_ACCESS(crime)`; E-REV, E-CTL4R, E-CTLW and H-40 each also MEASURED, 226/226 in both latch states; T measured as in the table)

Three facts carry every non-rowed disposition.

* **F1 -- the prelude rewrites two registers on every access**, before the width dispatch, whether or not the access
  is declined:
  * `d->reg[CRIME_REV / sizeof(uint64_t)] = d->use_fb? 0xa1 : 0x11;` (:229)
  * `d->reg[CRIME_CONTROL / sizeof(uint64_t)] = CRIME_CONTROL_ENDIANESS;` (:231)

  `struct crime_data` is defined in, and private to, `dev_sgi_ip32.c`: a grep of the tree finds only `dev_crime_init`
  named outside it.  No function but `DEVICE_ACCESS(crime)` reads `reg[0]` or `reg[1]`: `dev_crime_tick`,
  `crime_interrupt_reassert`, `crime_interrupt_assert/deassert` and `crime_update_crime_time` touch only SOFTINT,
  HARDINT, INTMASK, INTSTAT and TIME.  So anything stored into `reg[0]` or `reg[1]` is overwritten before any read.
* **F2 -- the tail is common to both paths.**  `crime_declined:` restores HARDINT to its entry value, recomputes
  INTSTAT, and answers a read with `odata`.  That answer is 0 on a decline; memory_rw pre-zeroes the buffer anyway
  (#95).
* **F3 -- an accepted 4- or 8-byte access can print only two kinds of text:** the CONTROL arm's `fatal()` for a
  nonzero residue (:377-379), and the default arm's `debug()` lines (:397-408).  A silent decline prints nothing.

**E-REV (entries 1, 3, 4).**
* Entry 1 (8W) and entry 3 (4W, high lane) store into `reg[0]`, so F1 applies.
* Entry 4, a 4-byte read at +0x00, takes the HIGH lane: `odata = (int32_t)(odata >> 32)` (:293-294).  That lane is 0
  for 0x11 and for 0xa1, which is the 0 a decline answers (F2).
* The REV arm acts only when `((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100` (:344).  That test is false
  for these three, which are issued from ordinary code, and the arm prints nothing.

**E-CTL4R (entry 8).**
* `lw +0x08` takes CONTROL's high lane, 0x100 >> 32 = 0, which is the decline's answer.
* The CONTROL arm acts only under `if (writeflag == MEM_WRITE)` (:356).
* Also measured before this: table 16's `G_clr_ctl4r` scored 226/226, and repair 14's `ctl4r.py` scored 9/9 with its
  lane-flip liveness control at 8/9.
* `acc ctl4r` and `p acc ctl4r` drive this cell and read 0 either way.  They are the vacuous half of the +0x0c pair,
  as the contract already says.

**E-CTLW (entries 12 and 16 write 0; 13 and 17 write 0x0200; 43 and 44 write 0x0100; each at 4W and 8W).**
* The store goes into `reg[1]`, so F1 applies.
* The arm clears DOG on the LOCAL `idata` (:361-363), finds HARD_RESET clear (:364), clears ENDIANESS (:375), and
  prints only `if (idata != 0)` (:377-379).  For these three values the residue is 0: no text and no halt.
* `ctldog sw/sd msg` DRIVE 13 and 17 with the latch CLEAR but cannot see their decline.  They count the 0x0201 twin's
  text, which is one either way.  They exist for `D_nodogclear`, which is a different edit.

**H-40 (entry 40, `sw +0x04`).**
* The store lands in `reg[0]`'s LOW lane (:283-284), so F1 applies and there is no guest channel.
* `switch (0x04)` matches no case, so the accepted store reaches the default arm.  Its `debug()` prints
  `[ crime: write to 0x4: <the four bytes> (len=4) ]` while the probe single-steps.  A decline prints nothing.
* No row counts `[ crime: write to 0x4:`; `dflt ctl` counts the READ line `[ crime: read from 0x4,`.
* At LABEL grain, the default arm's 4W low lane is guest-visible and rowed at +0x34 (entry 38).  Only the offset
  +0x04 is host-only.

**T (entries 10, 11, 14, 15).**
* 0x0201 and 0x0001 both leave residue 0x1, because the DOG clear takes the 0x0200.  So the arm prints
  `[ CRIME_CONTROL: unimplemented control 0x0000000000000001 ]` (:377-379).
* The store itself is overwritten (F1).  The text is the only difference, so there is no guest channel, and that
  text IS counted in both latch states (see the table).

## Found on the way

1. **Entry 34's latch-CLEAR hole is new, and the earlier derivations could not see it.**
   * `BUCKETS8_rerun.out`, `b12.out` and `mirror14.py` ask whether a session DRIVES the entry.  Entry 34 is driven
     latch-CLEAR by the value session (S55) and by `latch x5` (S52).  Both store 0 over a slot holding 0, so neither
     is an OBSERVER.  This table asks whether a row MOVES, and on that test the entry fails.
   * Measured on S55: `k34C` 226/226, one hit.  S52 was re-run in the other FULL specs but served from the capture
     here, by declaration.
   * My grading is **clause (e), not a floor breach**:
     * The floor enumeration is per LABEL, and the default label's latch-CLEAR 8W cell is rowed at +0x278 (`k45C`,
       five rows).
     * The body tests no offset within the default label.  The width arm tests only `relative_addr & 4`, and only
       for 4-byte accesses.
     * The existing disclosed bullet already says "TOUCHING a slot in ACCEPTS pins its LATCH behaviour, never its
       acceptance".
   * That grading is a reading; the adjudicators decide it.
   * If a row is wanted, the cheapest one I can derive (not built) needs no new session.  Seed a nonzero value in
     S55's and S58's `sd +0x40` (e.g. 0x0123456789abcdef), and re-want `acc 40 sw` / `p acc 40 sw` as
     0x0a0b0c0d89abcdef.  That would also make those rows check that a 4W high-lane store keeps the low lane.
   * Cost: those two sessions' command lists change, so the targeting rule reselects every kill that touches them.
2. **Four cells are held only by CONTROL rows:** 5-C, 41-C, 25-C and 25-S.  A kill there reads
   `CRIMEP_CONTROL=FAIL`, and table 16's scorer already treats that as a detection (`G_clr_imk4r`, "225/226 1 FAIL
   exact").  A scorer that discarded CONTROL=FAIL legs as apparatus failures would score those four cells as escapes.
3. **Entry 25's answer VALUE is read by no row in either state.**  S18 loads it into `v0` and S20 into `a0`, and
   neither is printed.  Only its reassert effect is rowed.  A decline is caught; an edit that corrupts the value but
   keeps the reassert is outside this table's unit.  This is a reading, not measured.
4. Item 6's "CONTROL 8R (acc ctl ld) and 8W (acc ctl sd)" is true of 8W at the 0x0001 value only (entry 15).  At
   0x0201 the 8W cell is `ctldog sd msg` / `latch ctl msg`; at 0, 0x0200 and 0x0100 it is EQUIVALENT.  The close-7
   report said so; the table confirms it.

## Artifacts

All of these are in `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\opus_acc46\`.
Copy that directory to `final529r17_20260926/opus_acc46/` before any record cites it.

* **Predictions:** `PREDICT46.out` / `predict46.py` (written first).
* **Static map:** `smap17.py` / `smap17.out`.
* **Specs and lanes:** `specs46.py` / `specs46.out`, `plan46.out`, `lanes46.py`, `lane_*.sh`, `replay_all46.sh`.
* **Mutant and build:** `mut46.py` / `mut46.diff`, `build46.sh` / `build46.out`, `build_*.log`.
* **Driver:** `replay46.py`.  The replays ran the frozen copy `replay46.frozen.py` (`861ec105`).  The capture ran
  `2d138730`, which has the same capture path.
* **Runners:** `capture46.sh`, `smoke46.sh`.
* **runs/:**
  * `capture.raw`, `capture.md5`, `capture_cache.pkl`
  * `smoke_k32C.raw`
  * `replay.md5`
  * `k01C.raw` .. `k46S.raw`
  * `lane_*.log`
* **Scoring:** `sum46.py` -> `SUM46.out`; `analyze46.py` -> `ANALYZE46.out`; `mk_table46.py` -> `TABLE46.md`.
* **Splice test:** `splice46.py`, `replacement_final.txt`, `r17_spliced.py`.

The binaries stay in WSL `/tmp/gxopus_acc46_bins`: base `b5b99e6d`, envmut `858bfb4c`.  Every log ends in its
sentinel (`CRIMEP_DONE` plus `REPLAY46_DONE`).
