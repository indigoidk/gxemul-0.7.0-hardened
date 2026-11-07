# Reading task: closedraft_15 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBCLOSE15-2b1d` on a line of its own.

# GXemul hardened fork -- DRAFT THE CLOSURE RECORDS for 2 filed issues proposed for closing (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork keeps a
ledger of every filed issue.  An earlier triage pass proposed closing each row below.  Closing must be HONEST: a row closed
as documented says what was assessed and not changed; a dropped row says why it is not a defect worth a round; a row closed
as OVERTAKEN (someone else's fix removed the defect) is only closable on three conditions -- (1) a discriminating control,
measured at HEAD: neutralise the overtaking fix and this row's own symptom comes back; (2) the rows that now carry the
coverage named; (3) that control preserved at a durable path.  You cannot read files; work from the text.  Ledger at HEAD 8d9df658.

## The rows

### ROW `wdcperopcode` -- state `open`, severity `-`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** wdcperopcode  wdc_command()'s unimplemented-command latch is per-DEVICE, so a guest cycling opcodes gets ONE line and 255 silent aborts -- a SPEC choice, filed not fixed

**state_note (head):** *** FILED 2026-08-26 BECAUSE THE SHIPPED DETECTOR'S CONTRACT CLAIMED A FILING THAT DID NOT EXIST. *** `wdc_flood_probe.py`'s header says *"deepseek argued for a per-opcode set; FILED, not shipped"* -- and no row carried it; the only trace was prose inside `wdcflood`'s state_note, which is not something a reader can find. **A contract line asserting a disposition is a WRONG RECORD until the disposition exists as a row.** Caught by the readiness adjudication before the round shipped. THE PROPOSAL, from the deepseek seat on the `wdcflood` pass-1 panel: `:583`'s diagnostic VALUE [dev_wdc.c; at 987cb596 the latch and its message are :1156-1161] is the opcode, so a single per-device flag suppresses every later unimplemented command and hides distinct guest actions. A 256-bit set (`uint32_t warned_unimpl_cmd[8]`) is cheap and preserves them. WHY IT WAS NOT SHIPPED, and the reason is not that it is wrong: the scalar is exactly what stops a guest cycling 0x00..0xff for 256 lines, which is the flood the round exists to bound. Per-opcode-versus-per-device is a SPEC choice between two acceptable behaviours, and the adjudication ruled that clause (d) tests the CHOSEN spec's repair rather than adjudicating between specs -- deepseek's framing ("the scalar IS the (d) mutant") is circular, since it assumes per-opcode is the baseline and then calls the alternative a weakening. *** THE SHIPPED SPEC IS PINNED, WHICH IS WHAT MAKES THIS SAFE TO DEFER: *** the `unimpl 2op` row fires TWO DIFFERENT opcodes and demands ONE line, so a later change to per-opcode is a VISIBLE spec change that reddens a row, not a silent drift. The same row kills a "last-warned-opcode" latch (measured: `M3`, 21/22, that row alone), under which an alternating guest floods forever. IF IT IS EVER WORKED, the option set is THREE-membered and the third member is the one the dispute never named: scalar (shipped), per-opcode set (deepseek), and the in-tree COUNT-BOUND idiom (`n_trunc_msgs`, `src/cpus/memory_rw.c:495-523`). Note also that #337's other latched messages at `:816`/`:855` [dev_wdc.c; at 987cb596 the `warned_badlen` latches :1604-1609 and :1638-1643] carry NO value payload, so "three latches in this file" is weaker precedent for discarding value-resolution than it looks -- `:583` [dev_wdc.c; at 987cb596: :1156-1161] is the only site whose message names an opcode.

**hold_question:** (none)

**the triage pass's reason:** the scalar spec choice is pinned by unimpl 2op and safe to defer

### ROW `offlinescope` -- state `open`, severity `low`; PROPOSED: **DOCUMENT-AND-CLOSE**

**title:** offlinescope  The machine embargo was over-scoped: 11 of 14 offline differentials build and run in 10 seconds total, and six of the top eight ranked defects sit in files they already pull in [corrected 2026-11-02: seven of the top eight, not six -- the row's own list in its state_note names ranks 1-6 and 8, and only sh4sqwrite (7th) has no differential]

**state_note (head):** *** REFINEMENT 2026-08-27, and it corrects my own overstatement. 'Six of the top eight are workable offline' conflated TWO different claims, and the gap between them is the real cost of each next round. ***

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
  5 wdcnoirq      diff_wdc_identify      <- devices/dev_wdc.c
  6 n6            diff_footbridge        <- devices/dev_footbridge.c
  8 mrwstore2     diff_memory_rw         <- cpus/memory_rw.c
```
**Only `sh4sqwrite` (7th) has none** -- its site is `cpus/memory_sh.c`, and no differential covers that file. *(`diff_m8820x` / `diff_m8invread` also cover the [[m8sarrows]] spec.)*

*** THE HONEST LIMIT, AND IT IS NOT A TECHNICALITY: RUNG 1 IS A DETECTOR, NEVER A WITNESS. *** The ladder is explicit -- *if it still compiles and still fails after the machine description and CPU/device dispatch are removed, leaving only a direct call, it was never a reproduction*. So this unblocks **measuring and detecting**, not witnessing. A rung-3 witness for any of these still needs a real emulator run.

*** THE APPARATUS LESSON, WHICH COST FOUR WRONG ANSWERS BEFORE IT WAS LEARNED: THERE IS NO UNIFORM FLAG SET. Each differential has its OWN gate invocation. ***
  * my first sweep used one flag set and reported **7 of 14 'COMPILE FAILED'**. Adding `-I$SEC/src` and `-lm` -- which the gate uses for some -- took it to 11. `diff_footbridge.c` does `#include "include/misc.h"`, which resolves ONLY with that path.
  * **`diff_diskimage_sync` then read as a REAL PRE-EXISTING RED** -- 11 rows, 5 failed, and identical under two different flag sets, which is exactly the evidence pattern that says *not your apparatus*. **It was still my apparatus.** The gate links it with `-Wl,--wrap=fsync -Wl,--wrap=fflush` (`gate_offline.sh:1479`), a line my grep window dropped. Without the wrappers `trace_add` never runs, so every row expecting a flush/sync SEQUENCE got `(none)` -- and the CHECK-CONDITION row failed too, because the harness ARMS its injected failure through the same interception. **With the wrap flags: `run rc=0`.**

> **I nearly reported a shipped differential as red at HEAD.** What stopped it was asking *what would make this fail for a reason other than the one under test* -- and the tell was that every failing row wanted a CALL SEQUENCE while every value row passed. **A failure whose rows share one shape is an apparatus failure until proven otherwise.**

**THREE STILL DO NOT COMPILE under any flag set I tried** -- `diff_diskimage_geom`, `diff_fbpending_bound`, `diff_ieee_store`. Each needs its own gate line read; two are link errors and one is a missing include. **Not investigated, and NOT to be read as broken** -- the pattern above says the flags are mine to fix.

**WHAT THIS CHANGES: the queue is workable now, not when the machine frees.** The remaining embargo covers rigs, the battery, boots and any wall-clock oracle -- which is what the owner actually asked for.

**SEVERITY SET LOW, 2026-09-07, by the MAIN LOOP** (not a flagship adjudication -- opus5/fable5 are reserved for the 09-09 adjudication, and a rating is exactly the kind of judgment call that seat exists for; overturn it freely).  REASON: the embargo is over-scoped, so the cost is work not done rather than a wrong result.

**hold_question:** (none)

**the triage pass's reason:** The true cost/scope is per-function fixture availability, not just file inclusion.

## For EACH row return (a numbered block per row, its id first)

1. `AGREE` or `DISAGREE` with the proposed closure, and why in one line -- DISAGREE when the row's own text describes a live,
   reachable defect, or names work still owed.
2. If AGREE: the closure RECORD text, two to four lines, in that honest form (for OVERTAKEN: the control that would
   discriminate and the rows that would carry it, stated as OWED, never as done).
3. The ONE fact that would make closing wrong -- what someone must check before closing it.
Do not invent commits, measurements or file contents the text does not give.

End with one line: `CLOSEDRAFT_15: <a> AGREE, <d> DISAGREE`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBCLOSE15: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
