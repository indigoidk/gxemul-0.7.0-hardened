# Reading task: oldrec473 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC473-c1ec` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #473 wdcrearmzero (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 21471-21600 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
21471| ## Round 473 (#473) -- the ATAPI DATAIN chunking pushed a whole transfer into a ring that cannot hold it, and then reported zero bytes left
21472| 
21473| Two defects in one piece of machinery, closed by one diff.  The adjudication took them as ONE
21474| round with TWO row ids: the arm and the re-arm are the two halves of a single chunking protocol,
21475| and bounding the push WITHOUT repairing the re-arm would have injected new corruption into the
21476| (32K, 64K] band that works today.
21477| 
21478|   `wdcringambig`  the initial arm pushed every byte of the transfer into a 513-block ring
21479|   `wdcrearmzero`  the re-arm reported ZERO bytes remaining and the command never completed
21480| 
21481| ### What was wrong
21482| 
21483| `WDC_INBUF_SIZE` is `512 * (WDC_MAX_SECTORS + 1)` -- exactly 513 blocks, 262656 bytes.  The
21484| initial arm did `atapi_len = data_in_len`, pushed every byte, and clamped to 32768 **afterwards**.
21485| The clamp was not missing; it was on the wrong side of the loop.
21486| 
21487| At the re-arm, `if (atapi_len > 32768) atapi_len = 0;` -- where the initial arm clamps to 32768
21488| under the identical condition.  With more than 32768 bytes left the guest is told zero remain
21489| while `received < data_in_len`, and there is no recovery: the next read decrements from 0, steps
21490| PAST zero, and `== 0` never fires again.  That is the `#341` class, reintroduced by the re-arm.
21491| 
21492| **MEASURED on the committed build, before any edit**, by the same script that later ran green:
21493| 
21494|     FAIL arm: pushes one chunk, not the whole   occupancy = 512, want 32768
21495|     FAIL arm: block 0 survives the push         first byte = 0xc3, want 0x5a
21496|     FAIL re-arm: >32768 left is not zeroed      atapi_len = 0, want 32768
21497|     ok   re-arm: the branch was actually taken  1
21498|     FAIL re-arm: the chunk is REFILLED          occupancy = 0, want 32768
21499|     FAIL re-arm: refill starts at received      first byte = 0x00, want 0x3c
21500|     22 rows, 5 failures  WDC_IDENTIFY_FAIL
21501| 
21502| 263168 bytes pushed into a 262656-byte ring reports **512** -- the ring cannot even say how much
21503| it lost -- and block 0's marker byte is gone, overwritten by block 514.  That second row is the
21504| corruption oracle: it shows data destroyed, not merely miscounted.
21505| 
21506| ### The fix -- three edits, all in the DATAIN chunking
21507| 
21508| 1. **initial arm:** move the existing 32768 clamp BEFORE the push loop, so one DRQ chunk is
21509|    pushed, which is what the re-arm already assumed.
21510| 2. **re-arm:** clamp to 32768 instead of assigning 0.
21511| 3. **re-arm:** refill the next chunk from `data_in[atapi_received + j]`.
21512| 
21513| The refill is what makes the bounded push correct.  It is safe at that point because `atapi_len`
21514| is 0 -- the guest has drained the previous chunk and the ring is empty -- and `data_in` is still
21515| live, the transfer struct being freed only when the next command arrives.
21516| 
21517| ### The reproduction took three attempts, and the first two were red for the WRONG REASON
21518| 
21519| Attempts 1 and 2 reddened on `atapi_len = 2`, the value the fixture itself had set, and both were
21520| REMOVED rather than shipped.  The cause was found with gdb: a NULL function pointer, because
21521| `dev_wdc_tick()` runs unconditionally after every access and calls `INTERRUPT_ASSERT(d->irq)`.
21522| DEVINIT wires that with `INTERRUPT_CONNECT` -- a **macro**, invisible to a scan for field
21523| assignments, which is why reading DEVINIT for field sets missed it twice.
21524| 
21525| ### *** A DETECTOR AIMED ONE LEVEL BELOW THE FIX, and it went red for a reason the fix does not address ***
21526| 
21527| The first ring row called `wdc_addtoinbuf()` DIRECTLY, 514 blocks' worth.  It was red on the
21528| committed build, which made it look like a reproduction.  It is not: that primitive is unbounded
21529| and **the fix did not bound it** -- the repair is in the CALLER.  So the row pinned a property
21530| still true afterwards and could never go green.
21531| 
21532| > **A detector aimed at a primitive cannot verify a fix made in its caller.**  Right defect,
21533| > wrong instrument -- the red-for-the-wrong-reason failure moved one level up, where it is harder
21534| > to see because the row is red on the correct build for a real reason.
21535| 
21536| Replaced by a row that drives the ARM: `atapi_cmd_in_progress` plus ten queued bytes, then a
21537| 2-byte `wd_data` write completes the 12-byte packet and calls `diskimage_scsicommand()`.  The
21538| SCSI stub was made **controllable rather than productive** -- a file-static byte count, zero by
21539| default -- because that file's own header correctly warns that a stub returning a fabricated
21540| transfer would overwrite the re-arm row's placed state.
21541| 
21542| *The packet fires on `inbuf_len == 12` AFTER the access pushes its own bytes.  Queueing twelve
21543| gives 14 and the command silently never fires; the first version of the row measured exactly
21544| that, reporting occupancy 14.*
21545| 
21546| ### The kill table -- 8 of 8, and TWO clause-(d) escapes closed in-round
21547| 
21548|     Mb_arm       KILLED  2/6   (b) clamp back after the push loop
21549|     Mb_rearm     KILLED  3/6   (b) = 0, no refill
21550|     Mb_both      KILLED  5/6   (b) both sites -- the full pre-fix code
21551|     Mc_null      KILLED        (c) null medium: comment-only source, caught at compile
21552|     Md_widenarm  KILLED  1/6   (d) arm clamp widened to the ring size
21553|     Md_armzero   KILLED  2/6   (d) arm clamp inverted to 0
21554|     Md_norefill  KILLED  2/6   (d) clamp kept, REFILL LOOP DELETED
21555|     Md_wrongoff  KILLED  1/6   (d) refill re-based to data_in[j]
21556| 
21557| `regress/artifacts/wdcchunking/killtable_20260827/TABLE.txt`, one file per mutant run, the
21558| pre-fix source, and `regress/artifacts/wdcchunking/killtable_20260827/PREFIX_RUN.txt`.  Baseline 22 rows, 0 failures, `WDC_IDENTIFY_PASS`. [2026-11-02, records: that archive was not produced from the final detector -- this round's pass-2 block ("The archive contradicted itself, and a seat caught it") records that every archived run said 22 rows while the committed source had 23, and re-derived the set; at 987cb596 `killtable_20260827/TABLE.txt` reads `26 rows, 0 failures`, last written by d894e35d; the same 22 stands in OUTSTANDING_BUGS.md's 2026-08-27 #473 entry]
21559| 
21560| *Five of the six rows red pre-fix; the sixth is the liveness control, which is green in BOTH
21561| builds by design -- it proves the fixture reached the re-arm branch rather than that the branch
21562| computed the right value.  The logs live at a durable path because a citation into a reused
21563| scratch buffer becomes CONTRADICTED BY ITS OWN EVIDENCE on the next run.*
21564| 
21565| **The last two ESCAPED the first table**, and they are the dangerous pair: `Md_norefill` tells the
21566| guest 32768 bytes are ready while the ring is EMPTY, and `Md_wrongoff` returns chunk 0's bytes for
21567| every chunk -- silent data corruption.  Both kept the guard and nulled its repair, and the length
21568| check alone passes both.
21569| 
21570| The arm row already carried a corruption oracle; the re-arm row carried only a length check.
21571| **The sibling-parity check exists precisely to catch that asymmetry and would have found it before
21572| the table ran.**  Closed under L1 -- pre-ship construction, the rows being part of a deliverable
21573| still being built -- though the same finding against shipped material would have been an L2 floor
21574| breach.
21575| 
21576| ### A padded-column near-miss
21577| 
21578| FOUR of the six new labels were AT or OVER the `%-38s` column width (39, 38, 38, 39), which is
21579| the trap that has previously made a gate check unsatisfiable so a row silently stops being
21580| tested.  All four shortened below the boundary and re-measured.
21581| 
21582| ### Honest scope
21583| 
21584| `wdc_addtoinbuf()` **remains unbounded** -- the fix bounds its caller, and no row here constrains
21585| the primitive.  Only the FIRST re-arm is pinned; a transfer crossing several re-arms is not walked
21586| end to end.  The fixture drives one packet command; interleaved commands, aborts and resets are
21587| outside the contract.  All three are written into the differential's clause-(e) contract block
21588| rather than left to be discovered.
21589| 
21590| Rung-1 direct-call harness = DETECTOR, never a witness.  **`wdcrearmzero` still owes a rung-3/4
21591| witness**; that obligation is unchanged by this round and is recorded, not discharged.
21592| 
21593| *Both ledger rows are `held`, NOT closed, and their witness field carries the reason rather than
21594| the bare word `none`.  A draft of this block said `none` was the honest value; it is not.
21595| `state_semantics` defines `none` as DOCUMENTED-ONLY, and this round shipped a fix -- so the bare
21596| value asserts that no code changed.  `b115` (#472) set the precedent deliberately: no ladder term
21597| fits "fix shipped on rung-1 evidence", and that absence is the signal a round needs an owner
21598| exemption or a rung-3 probe.  THREE rounds now sit here, so it is filed as a standing question.*
21599| 
21600| `est/`, `build/` and `build-asan/` carry `dev_wdc.c` byte-identically with GXEMUL-SEC.
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_473: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC473: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
