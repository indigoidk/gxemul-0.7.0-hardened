# Reading task: closedraft_05 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE05-9fca` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 6 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `gdrompiooddlen` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** gdrompiooddlen  the GDROM PIO read guards ONE byte and then reads TWO -- LATENT, because no path can produce an odd length today

**state_note (head):** *** FOUND 2026-08-25 WHILE VERIFYING A PREMISE IN THE `gdrompionull` PASS-1 BRIEF, NOT WHILE LOOKING FOR IT. *** The brief's Q4 asked, almost as an afterthought, whether `d->cur_data_offset` is reset anywhere -- because the round had reasoned about `data_len` throughout and barely looked at the guard's OTHER operand. It is reset (`:327`, beside the NULL). But reading the guard to check that showed something else. *** THE GUARD CHECKS ONE BYTE AND THE BODY READS TWO. *** Verified by reading, three lines:   (1) `dev_dreamcast_gdrom.c:611` -- `if (d->cur_data_offset < d->data_len) {`   (2) `:612-613` -- `odata = d->data[d->cur_data_offset ++];` then `odata |= (d->data[d->cur_data_offset ++] << 8);` -- **two increments, one bounds test**   (3) `alloc_data` `:309` -- `malloc(d->data_len)`, **exactly `data_len` bytes, no padding, no rounding**. So at `cur_data_offset == data_len - 1` the guard PASSES, the first read is the last valid byte, and **the second read is `d->data[data_len]` -- one byte past the allocation**. *** REACHABILITY, STATED AS WHAT IS READ AND WHAT IS OWED. *** READ: `data_len = d->cnt` (`:307`), and `d->cnt` is GUEST-WRITABLE A BYTE AT A TIME -- `:704` sets the low byte from a CNTLO store and `:712` the high byte from CNTHI, so an ODD count is expressible. The two subsequent adjustments do not remove oddness: `:409-410` only replaces `cnt` when it is ZERO, and `:4 [... 4745 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** the row's own evidence confirms the defect is a latent structural hazard with no reachable route.

### ROW `wdcperopcode` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** wdcperopcode  wdc_command()'s unimplemented-command latch is per-DEVICE, so a guest cycling opcodes gets ONE line and 255 silent aborts -- a SPEC choice, filed not fixed

**state_note (head):** *** FILED 2026-08-26 BECAUSE THE SHIPPED DETECTOR'S CONTRACT CLAIMED A FILING THAT DID NOT EXIST. *** `wdc_flood_probe.py`'s header says *"deepseek argued for a per-opcode set; FILED, not shipped"* -- and no row carried it; the only trace was prose inside `wdcflood`'s state_note, which is not something a reader can find. **A contract line asserting a disposition is a WRONG RECORD until the disposition exists as a row.** Caught by the readiness adjudication before the round shipped. THE PROPOSAL, from the deepseek seat on the `wdcflood` pass-1 panel: `:583`'s diagnostic VALUE [dev_wdc.c; at 987cb596 the latch and its message are :1156-1161] is the opcode, so a single per-device flag suppresses every later unimplemented command and hides distinct guest actions. A 256-bit set (`uint32_t warned_unimpl_cmd[8]`) is cheap and preserves them. WHY IT WAS NOT SHIPPED, and the reason is not that it is wrong: the scalar is exactly what stops a guest cycling 0x00..0xff for 256 lines, which is the flood the round exists to bound. Per-opcode-versus-per-device is a SPEC choice between two acceptable behaviours, and the adjudication ruled that clause (d) tests the CHOSEN spec's repair rather than adjudicating between specs -- deepseek's framing ("the scalar IS the (d) mutant") is circular, since it assumes per-opcode is the baseline and then calls the alternative a weakening. *** THE SHIPPED SP [... 962 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** the scalar spec choice is pinned by unimpl 2op and safe to defer

### ROW `fbclearidempotent` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** fbclearidempotent  the DC21285 says a timer clear has no effect if the interrupt was already clear, but the write arm reloads a periodic timer unconditionally

**state_note (head):** PRE-EXISTING, not introduced by `#474`.  Named by the pass-2 codex seat, which said
explicitly that it *"deserves a separate filing, not an untested expansion of #474"* -- and
that is the disposition taken.

Datasheet, section 7.3.42: *"The write has no effect if the associated interrupt was
already clear."*  The model reloads the counter whenever the periodic bit is set,
regardless of whether anything was pending.  Needs a row of its own and a reading of what
the reload is actually for.

**hold_question:** Is `reload_timer_value()` at TIMER_x_CLEAR a MODELLING SHORTCUT standing in for the hardware's automatic reload-at-zero, or is it modelling the Clear write itself?  The fix differs: if a shortcut, guarding it on `pending > 0` is right but for a different reason than the datasheet gives; if not, the guard changes when periodic timers reload.

**the triage pass's reason:** Claim verified by datasheet text, brief-ready.

### ROW `gdromdefaultstatusless` -- state `open`, severity `-`; PROPOSED: **CLOSE-OVERTAKEN**

**title:** gdromdefaultstatusless  gdrom_default_probe.py's session() calls waitpid and DISCARDS the status, so NO row in 52 can tell a clean exit from a signal from a decline

**state_note (head):** *** MATERIALLY ADVANCED BY #490 AND THIS RECORD DID NOT KNOW.  Added 2026-08-29 after a
pass-2 seat found the gap -- the gap-closes-itself shape. ***

`#490` added TWO rows to `regress/gdrom_default_probe.py` that bear directly on this row:
**`stale quiet`** (the two anchored decline regexes must BOTH read zero on a session that
sends a well-formed packet) and **`stale how`** (the session must end `exit0`, read from the
exit status rather than from `alive`).

`stale how` closes something this tree had left inert: **`how` had been threaded through 37
call sites and NO ROW READ IT.**  `alive` is False only when a read fails inside a budget
window, so it is true of a hung emulator, a frozen one, and -- measured -- one already killed
after the last budget check.  The exit status cannot be fooled that way.

**HONEST LIMIT: neither new row has a MEASURED RED on disk yet.**  The preserved blinding
artifacts predate them (58-row era).  One rot-packet run of the 60-row probe reds
`stale quiet` and discharges both under this project's own bar that a row is discharged by a
measured kill, not by existing.  Owed before #490 closes.

*(`stale how`'s kills-annotation was also FALSE as first written -- it claimed floor clause
(b), but that session sends a CORRECT packet reaching neither de-fatalised site, so a
reinstated exit(1) leaves it exiting 0 and the row green.  Corrected in-round.)*

FI [... 2331 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** Defect superseded by #490's stale quiet/how rows.

### ROW `offlinescope` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** offlinescope  The machine embargo was over-scoped: 11 of 14 offline differentials build and run in 10 seconds total, and six of the top eight ranked defects sit in files they already pull in [corrected 2026-11-02: seven of the top eight, not six -- the row's own list in its state_note names ranks 1-6 and 8, and only sh4sqwrite (7th) has no differential]

**state_note (head):** *** REFINEMENT 2026-08-27, and it corrects my own overstatement. 'Six of the top eight are workable offline' conflated TWO different claims, and the gap between them is the real cost of each next round. ***

**THE TWO CLAIMS, which are not the same:**
  1. **the SOURCE compiles offline** -- a differential `#include`s the file the defect lives in, so the shipping code is present and callable. True for seven [corrected 2026-11-02, records: said six] of eight.
  2. **a FIXTURE exists that reaches the defect** -- the harness already builds the structs and stubs that particular code path needs. **This is per-FUNCTION, not per-FILE**, and it is what actually determines the cost.

**Measured on the next queue item, [[wdcringambig]]:** `diff_wdc_identify.c` `#include`s `dev_wdc.c` (claim 1 holds) but has **ZERO references to the ring buffer** -- it is a focused differential on the ATA IDENTIFY capacity packing. So claim 2 does NOT follow from claim 1.

*** BUT THE FIXTURE IS THERE ANYWAY, WHICH IS THE USEFUL FINDING: *** that file (766 lines) already builds `struct wdc_data` accessors, a `stub_machine` / `stub_cpu` pair with `fake_cpu()`, and ~65 stub lines. **So a ring-buffer section is the same order of work as the overlay section `#472` added** -- write the section, reuse the fixture, add rows.

**Why `b115` was the cheapest possible start, in hindsight:** `diff_diskimage_io.c` alre [... 4559 more characters not shown]

**hold_question:** (none)

**the triage pass's reason:** The true cost/scope is per-function fixture availability, not just file inclusion.

### ROW `wdcnullxfer` -- state `held`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** wdcnullxfer  #475's clamp WOKE a NULL dereference that the broken counter had been hiding -- two guest register accesses SIGSEGV the host.  FIXED in-round as #476

**state_note (head):** *** DID `#476` CLOSE THE CLASS OR ONE INSTANCE?  ENUMERATED 2026-08-27, and the answer is
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

*Worth noting for anyone reasoning about the free: `scsi_transfer_alloc [... 2284 more characters not shown]

**hold_question:** RUNG-3 ATTEMPT DISCHARGED 2026-09-13: WITNESSED (regress/artifacts/wdcnullxfer/rung3_20260913/).  QUESTION for the batched flagship close pass: does the rung-3 witness plus the shipped detector close this row, or is anything still owed (e.g. promoting the witness probe into regress/)?  [previous: OWNER DECIDED 2026-09-13: a host SIGSEGV reached by two guest register accesses REQUIRES a rung-3 witness BEFORE its fix -- it is about as rung-3-able as a defect gets, and the rung-1 exemption question [... 320 more characters not shown]

**the triage pass's reason:** State notes and recent entries confirm the fix and overlapping guards, with no other reachable dereferences.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_05: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE05: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
