# Reading task: nextstep_03 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBNEXT03-178f` on a line of its own.

# GXemul hardened fork -- THE NEXT STEP for 6 filed issues that must NOT be closed yet (a defensive project's queue work)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier pass found that each row below still names work owed, so it stays open.  You cannot
read files; work from the text.  Ledger at HEAD 8d9df658.  Proposals only.

## The rows

### ROW `offlinescope` -- state `open`, severity `low`

**title:** offlinescope  The machine embargo was over-scoped: 11 of 14 offline differentials build and run in 10 seconds total, and six of the top eight ranked defects sit in files they already pull in [corrected 2026-11-02: seven of the top eight, not six -- the row's own list in its state_note names ranks 1-6 and 8, and only sh4sqwrite (7th) has no differential]

**state_note:** *** REFINEMENT 2026-08-27, and it corrects my own overstatement. 'Six of the top eight are workable offline' conflated TWO different claims, and the gap between them is the real cost of each next round. ***

**THE TWO CLAIMS, which are not the same:**
  1. **the SOURCE compiles offline** -- a differential `#include`s the file the defect lives in, so the shipping code is present and callable. True for seven [corrected 2026-11-02, records: said six] of eight.
  2. **a FIXTURE exists that reaches the defect** -- the harness already builds the structs and stubs that particular code path needs. **This is per-FUNCTION, not per-FILE**, and it is what actually determines the cost.

**Measured on the next queue item, [[wdcringambig]]:** `diff_wdc_identify.c` `#include`s `dev_wdc.c` (claim 1 holds) but has **ZERO references to the ring buffer** -- it is a focused differential on the ATA IDENTIFY capacity packing. So claim 2 does NOT follow from claim 1.

*** BUT THE FIXTURE IS THERE ANYWAY, WHICH IS THE USEFUL FINDING: *** that file (766 lines) already builds `struct wdc_data` accessors, a `stub_machine` / `stub_cpu` pair with `fake_cpu()`, and ~65 stub lines. **So a ring-buffer section is the same order of work as the overlay section `#472` added** -- write the section, reuse the fixture, add rows.

**Why `b115` was the cheapest possible start, in hindsight:** `diff_diskimage_io.c` already had `mkdisk()` AND called `diskimage__internal_access()` directly, so the defect was reachable with no new fixture at all. That is not typical, and the ranking happened to put it first for unrelated (harm) reasons.

> **THE HONEST RULE FOR ESTIMATING THE NEXT ONE: check whether the differential already REFERENCES the code path, not just whether it includes the file.** One grep. `diff_wdc_identify` includes `dev_wdc.c` and mentions the ring zero times.

*** MEASURED 2026-08-27. The embargo blocks far less than a whole session assumed -- MY assumption, not the owner's, who embargoed *bugs that require idle computer for timing issues*. An offline differential has no timing content at all. ***

**THE MEASUREMENT** (deriver: compile each `regress/diff_*.c` with the gate's flags, run it, time it):

```
  compiled and ran   11 of 14
  wall, per harness  0 s
  wall, ALL of them  10 s
  a full battery     ~45 min, and needs the machine to itself
```

Each is ONE `.c` compiled by ONE `cc`, `#include`ing the REAL shipping source. **No gxemul build, no build tree touched, no rig, no wall-clock oracle.**

*** SEVEN [corrected 2026-11-02, records: said SIX] OF THE TOP EIGHT RANKED DEFECTS SIT IN SOURCE AN EXISTING DIFFERENTIAL ALREADY PULLS IN: ***
```
  1 b115          diff_diskimage_io      <- disk/diskimage.c          REPRODUCED TODAY
  2 wdcringambig  diff_wdc_identify      <- devices/dev_wdc.c
  3 b120          diff_diskimage_io/sync <- disk/diskimage_scsicmd.c
  4 fbclearread   diff_footbridge        <- devices/dev_footbridge.c
  5 wdcnoirq      diff_wdc_identify      <- device

**hold_question:** (none)

### ROW `wdcnullxfer` -- state `held`, severity `-`

**title:** wdcnullxfer  #475's clamp WOKE a NULL dereference that the broken counter had been hiding -- two guest register accesses SIGSEGV the host.  FIXED in-round as #476

**state_note:** *** DID `#476` CLOSE THE CLASS OR ONE INSTANCE?  ENUMERATED 2026-08-27, and the answer is
THE CLASS -- but the enumeration is the point, not the answer. ***

`#475` taught that repairing a counter can WAKE DEAD CODE, so fixing one dereference proves
nothing about the others.  All nine derefs of `atapi_st` in the file, with their protection:

```
  :812  atapi_received < atapi_st->data_in_len   <- the #476 site, NOW GUARDED
  :877  atapi_len = atapi_st->data_in_len - ..   <- nested inside :812's true arm
  :884  wdc_addtoinbuf(.. atapi_st->data_in[..]) <- same block
  :1033 atapi_st->cmd = scsi_cmd                 <- immediately after the alloc
  :1034 atapi_st->cmd_len = 12                       at :1023
  :1039 atapi_st->cmd_len = 10
  :1072 if (atapi_st->data_in != NULL)
  :1082 atapi_len = atapi_st->data_in_len
  :1087 wdc_addtoinbuf(.. atapi_st->data_in[j])
```

**The first three are the reachable family and all three are inside the arm `#476` guards**
-- `:812` runs only when `atapi_len == 0 && atapi_st != NULL`, and `:877`/`:884` are nested
within its true branch.

**The remaining six sit after `scsi_transfer_alloc()`, WHICH CANNOT RETURN NULL** -- verified
by opening it: on malloc failure it prints and `exit(1)`s.  (That exit is a separate,
pre-existing, OOM-only concern and is not guest-reachable.)

*Worth noting for anyone reasoning about the free: `scsi_transfer_alloc` runs a FREELIST, so
a fresh alloc typically REUSES the just-freed chunk.  That is why a pointer-identity oracle
reads a false negative on a plain build and only separates under a sanitiser's quarantine --
a seat measured exactly that.*

**So no second host kill of this family is in the tree.**  Recorded as an enumeration a
reader can re-derive rather than as an assurance.

*** A REGRESSION I SHIPPED, FOUND BY THE MEASURING SEAT ONE COMMIT LATER, FIXED THE SAME
HOUR.  2026-08-27. ***

```
  d894e35 (before #475)   a DATA read with no transfer survives   exit 0
  d64a1fc (with #475)     a DATA read with no transfer survives   host killed, signal 11
```

**THE MECHANISM IS ENTIRELY #475's.**  Before it, a data-port read with `atapi_len` already
0 drove the counter NEGATIVE, so `if (atapi_len == 0)` never fired again and the
`d->atapi_st->data_in_len` deref on the next line was **dead code**.  The clamp makes
`atapi_len` STAY 0.  The test fires.  `atapi_st` is NULL.

> **A FIX THAT STOPS A COUNTER GOING NEGATIVE CAN MAKE A PREVIOUSLY-UNREACHABLE BRANCH
> REACHABLE.**  The clamp was right; the branch it woke was never NULL-safe.  *Repairing a
> counter can enable code that was only ever protected by the broken value* -- and nothing
> in `#475`'s own kill table could see it, because every mutant there attacked the clamp
> rather than what the clamp let through.

MEASURED `SIGSEGV at address 0x48` = `offsetof(struct scsi_transfer, data_in_len)`.  Two
guest register accesses from a fresh device: write ATAPI_PKT_CMD to COMMAND, then read
DATA.  The seat's control -- the same comma

**hold_question:** RUNG-3 ATTEMPT DISCHARGED 2026-09-13: WITNESSED (regress/artifacts/wdcnullxfer/rung3_20260913/).  QUESTION for the batched flagship close pass: does the rung-3 witness plus the shipped detector close this row, or is anything still owed (e.g. promoting the witness probe into regress/)?  [previous: OWNER DECIDED 2026-09-13: a host SIGSEGV reached by two guest register accesses REQUIRES a rung-3 witness BEFORE its fix -- it is about as rung-3-able as a defect gets, and the rung-1 exemption question is answered no for the whole class.  [previous question: Same rung-1 question as `rung1exempt`, but sharper here: this defect is a HOST SIGSEGV reached by two guest register accesses, which is about 

### ROW `exitcensus` -- state `open`, severity `med`

**title:** exit_census.py's BY-ENCLOSING-CONSTRUCT split attributed every call in a plain non-static function to the preceding DEVICE_ACCESS -- inflating the bucket used to rank reachability

**state_note:** 

**hold_question:** (none)

### ROW `exit0oracle` -- state `open`, severity `med`

**title:** shipped rows pin survival as an `exit0` want, so a mutant that announces and then exit(0)s satisfies them -- count DERIVED, never restated: grep -h 'row(.*"exit0"' regress/*.py | wc -l

**state_note:** 

*** THE CLASS IS NOT A PREDICTION -- IT HAS A MEASURED TOTAL ESCAPE, AND THE PROBE THAT MEASURED IT
ALSO SHIPS THE REPAIR.  Read out of the source 2026-09-08, not reasoned. ***

`regress/sgi_re_unmapped_probe.py` records it in its own comments:

    E0   exit(0) after the whole catch-all, BOTH directions   47/48
    E0W  exit(0) in the WRITE arm only                        48/48  *** TOTAL ESCAPE ***

and gives the reason, which is the class in one sentence: *"a `surv' row wants "exit0", and a clean
`exit(0)' IS exit status 0, so the oracle is SATISFIED by the very thing it should catch; a `decl'
row counts the message, which was already printed before the exit.  The two together therefore
pass."*  **E0 was caught by exactly one row and only INCIDENTALLY** -- that row makes two accesses,
so it notices the second one never happening.

*** THE IN-TREE REPAIR IDIOM, which answers the "is there a probe that does this well" question:
A POST-STORE POSITIVE OBSERVABLE. ***  Seed RAM, perform the declined device access, then read the
seed back -- *"if the host quit at the write, the load never runs and `printed()' returns "absent",
which is not the datum."*  `#499` added two such rows, deliberately covering BOTH components,
because a write-side `exit(0)` conditioned on one component is the asymmetry that round *"has now
been bitten by three times"*.

*** THE OPEN QUESTION IS WHETHER THAT REPAIR GENERALISED, AND A SCREEN SAYS PROBABLY NOT.  IT IS A
SCREEN AND IS RECORDED AS ONE. ***

The population, derived with this row's own command (`grep -h 'row(.*"exit0"' regress/*.py | wc -l`)
= **43 rows across 9 files**:

    sgi_re_unmapped_probe.py   11 exit0   seed-idiom  9   <- where E0W was measured and repaired
    pcc2_width_probe.py        11 exit0   seed-idiom  0   <- largest population, no seed idiom
    sgi_de_width_probe.py       5 exit0   seed-idiom  3
    gdrom_toclen_probe.py       5 exit0   seed-idiom  0
    pcc2_width_witness.py       4 exit0   seed-idiom  0
    sgi_de_primop_probe.py      3 exit0   seed-idiom  0
    gdrom_decline_probe.py      2 exit0   seed-idiom  0
    gdrom_default_probe.py      1 exit0   seed-idiom  1
    sgi_re_width_probe.py       1 exit0   seed-idiom  4

**On its face the repair stayed inside the `sgi_re`/`sgi_de` family and did not reach the `pcc2` or
`gdrom` probes -- 22 `exit0` rows across four files with no seed idiom at all.**  That would be the
`#499` shape at the HARNESS level: repaired at the address the mutant used, symmetric cells left
open.

> *** BUT THE SCREEN KEYS ON A CORRELATE AND I WILL NOT REPORT IT AS A FINDING. ***  It counts rows
> whose LABEL contains "live"/"surv"/"runs on" and files mentioning a seed variable.  **A probe can
> achieve the same discrimination without either -- by reading any value back after the access under
> any row name.**  That is precisely the deriver failure this project has recorded twice, and which
> I committed twice more today (a by-NAME census of switch labels that are a

**hold_question:** (none)

### ROW `gxprobepccache` -- state `open`, severity `med`

**title:** gxprobe cached the pc across `step`, so a driver that stepped without _exec_at() had its next pc assignment silently skipped -- a detector row that could not fail

**state_note:** 

**hold_question:** (none)

### ROW `pcc2pscaleflood` -- state `open`, severity `med`

**title:** pcc2pscaleflood  dev_pcc2.c: PSCALEADJ's write-side fatal() is unlatched and guest-drivable -- one of nine such prints (see pcc2huhflood)

**state_note:** Filed by the Opus seat on pass 3 while verifying something else.  floodclass member.  Filed in OUTSTANDING_BUGS.md (dated tail, `### pcc2pscaleflood`, line 14668 as of 2026-09-04); this row added 2026-09-04 so the dashboard shows it -- the bug file had it, the ledger did not.  FOLD (2026-09-04 fix review, both seats): into ONE floodclass round with pcc2huhflood (+ pcc2assertflood as the lowest); keep provenance, close as duplicate when the nine-site latch lands.

**hold_question:** (none)

## For EACH row (a numbered block, its id first)

1. The ONE concrete next step that would resolve it, as exactly one of: FIX-ROUND (a code change, with its site),
   MEASUREMENT (what to run and what result settles it), READING (a question a careful reading of named code or a manual
   answers), RECORD (a correction or closure note), OWNER-DECISION (the question, phrased so it can be answered).
2. If it is a READING or a RECORD that the text above already settles, DRAFT it now (two to six lines).  Otherwise say
   what the step needs that is not in the text.
3. Whether it can be COMBINED with another row in this packet (same device, same next step).
Do not invent measurements, commits or file contents.

End with one line: `NEXTSTEP_03: <f> FIX-ROUND, <m> MEASUREMENT, <r> READING, <c> RECORD, <o> OWNER-DECISION`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBNEXT03: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
