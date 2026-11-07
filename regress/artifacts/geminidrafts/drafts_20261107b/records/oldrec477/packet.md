# Reading task: oldrec477 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC477-fa7d` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #477 wdccdbmidxfer (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 20767-20944 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
20767| ## Round 477 (#477) -- a guest data-port WRITE could free the ATAPI transfer the device was still delivering
20768| 
20769| `atapi_cmd_in_progress` is set when a packet command arrives and cleared only when the NEXT
20770| command does, so it stays 1 through the whole of DATAIN and past `PHASE_COMPLETED`. The CDB
20771| dispatch keyed on that flag plus ring occupancy alone. A guest write during DATAIN that
20772| brought occupancy to exactly 12 therefore re-entered the dispatch, **freed the live
20773| transfer**, and issued a SCSI command assembled from the guest's own returned DATA-IN
20774| payload. MEASURED on the committed build: `freed 1 live transfer(s)`.
20775| 
20776| THE FIX is option B, a phase guard: the dispatch additionally requires
20777| `atapi_phase == PHASE_CMDOUT`. The flag conflates two roles -- *a packet command is active*
20778| (read at four register sites through completion, so it must stay set) and *I am collecting a
20779| CDB* (what the test actually wants). The phase distinguishes them; clearing the flag would
20780| have broken the completion handshake.
20781| 
20782| Option A -- guarding the data-port pushes -- was **MEASURED WORSE THAN NO FIX**: with
20783| occupancy already 12 a suppressed push leaves it at 12, so the guard CREATES a free on an
20784| input the unfixed code survives.
20785| 
20786| ### *** THE PHASE GUARD ALONE WAS A REGRESSION, AND A SEAT MEASURED IT ***
20787| 
20788| I answered the brief's own question 5 -- *does this make anything worse?* -- by reading the
20789| WRITE path, confirming nothing there moves `atapi_phase` between the packet command and the
20790| twelfth byte, and concluding #477 could not block a legal CDB. **That was wrong, and the
20791| Fable seat measured it wrong.** A data-port READ moves the phase:
20792| 
20793| | sequence | HEAD | phase guard alone |
20794| |---|---|---|
20795| | completed, PKT, CDB | DISPATCHED | DISPATCHED |
20796| | completed, PKT, **stray read**, CDB | DISPATCHED | **NO DISPATCH**, permanently |
20797| 
20798| `ATAPI_PKT_CMD` assigns only the flag and the phase, so after a prior completed command a new
20799| packet starts with `atapi_len == 0`, `atapi_received == data_in_len`, and `atapi_st` **stale
20800| non-NULL** -- it is freed at the next dispatch and never NULLed. A read then falls into the
20801| `atapi_len == 0` arm, finds `received < data_in_len` false, and sets `PHASE_COMPLETED`.
20802| Recovery is unavailable: the twelve-byte residue means occupancy can never EQUAL 12 again.
20803| 
20804| **That is worse than the unfixed code on an input the unfixed code survives -- the exact
20805| standard that rejected option A.** L1 (pre-ship), so it was repaired in-round rather than
20806| filed: the read arm now declines to derive completion state while a CDB is being collected
20807| (`atapi_len == 0 && atapi_phase != PHASE_CMDOUT`). In CMDOUT that pair describes the
20808| PREVIOUS transfer -- the same statement #477's own comment makes about the flag, applied one
20809| arm over.
20810| 
20811| ### The detector: 44 rows, and the accept side did not exist
20812| 
20813| Two seats found independently that **no row proved a legal CDB actually dispatches.**
20814| `row_cdb_already12` asserts nothing is FREED -- a reject assertion -- so a fix that
20815| suppressed every dispatch would have passed the entire table. Added `pkt_cdb_case` with a
20816| control (no stray read, must dispatch) and the regression row, so a red is attributable to
20817| the read rather than to the fixture.
20818| 
20819| Kill table `regress/artifacts/wdccdbmidxfer/killtable2_20260827/`, baseline **45 rows**
20820| 0 failures (`killtable2_20260827/base.out`): **six killed, one escape.**
20821| 
20822| *This sentence read "baseline 44 rows ... five killed, two escapes" until the same day.
20823| Both numbers were the state BEFORE the `occupancy above 12` row landed and killed
20824| `M7_ge12`; the verdict table and `killtable2_20260827/TABLE.txt` were corrected and this
20825| line was not.
20826| **The grep-for-siblings rule failing inside the session that applies it** -- and the
20827| bare filename-only citation went ambiguous the moment a second kill-table directory
20828| existed, which is the names-its-log rule needing a PATH and not just a filename.*
20829| 
20830| `Mr_readarm` (revert only the read-arm repair) is killed by the new row ALONE -- the (a)
20831| clause for it. `M7_zerolen`, the seventh mutant **four seats proposed independently**
20832| (`|| atapi_len == 0`), is killed by the COMPLETED row alone.
20833| 
20834| ### *** TWO FIXTURE DEFECTS OF MINE, AND FIXING THE SECOND TURNED A KILL INTO A FINDING ***
20835| 
20836| **(a) The COMPLETED fixture set `atapi_len = 10`, which the device cannot produce.** Every
20837| real transition to `PHASE_COMPLETED` leaves the count at zero. So `M7_zerolen` passed that
20838| row for the FIXTURE's reason and swept the table, while a real completed command plus twelve
20839| guest writes still re-entered dispatch. `alen` is now decoupled from the ring prefill: ten
20840| bytes still sit in the ring so the dispatch is genuinely attempted; only the COUNT is zero.
20841| Found by the codex seat.
20842| 
20843| **(b) No fixture set `cur_command`,** though the device assigns it with the flag and the
20844| phase in one arm. `M2_curcmd` was therefore scored KILLED **by `row_arm_overrun`, because
20845| legal dispatch vanished in an unreachable `cur_command == 0` state** -- a false-path kill. A
20846| table entry that proves nothing while reading as coverage.
20847| 
20848| With the fixtures corrected it ESCAPES -- and the comfortable reading, *redundant conjunct,
20849| provably equivalent*, is **wrong**. The discriminating state is reachable, and chasing it
20850| produced two live defects, both FILED (neither is a measured false pass nor a wrong record,
20851| so the stopping rule keeps them out of this round):
20852| 
20853| * **`wdcaltctrlbit`** -- the ALT-CTRL arm tests `WDCTL_4BIT` (`0x08`, *use four head bits
20854|   (wd1003)*) where the reset bit is `WDCTL_RST` (`0x04`). Selecting 4-bit head mode is
20855|   treated as a controller reset; a real soft reset is ignored.
20856| * **`wdcsrstnoabort`** -- the same arm leaves `atapi_cmd_in_progress` set, so an in-flight
20857|   packet command survives what the device itself calls a reset.
20858| 
20859| **An escape chased is worth more than an escape classified.** Filing this one as an
20860| equivalence would have buried both.
20861| 
20862| ### *** AND THE NINTH SEAT KILLED THE ROUND'S OWN CLASSIFICATION. `M7_ge12` IS A HEAP
20863| ### OVERFLOW, NOT AN IMPROVEMENT. ***
20864| 
20865| This round closed its research stage at **eight of nine** and recorded the ruling as
20866| PROVISIONAL on its face. The Opus seat then landed with **DO NOT CLOSE**, and it was right
20867| on a measurable -- which is the provisional-adjudication rule earning its keep for the
20868| second time.
20869| 
20870| An earlier draft of this block, and of the kill table, classified `M7_ge12`
20871| (`inbuf_len == 12` relaxed to `>= 12`) as *an improvement, not a re-opening* -- reasoning
20872| that under the phase guard it differs only in CMDOUT, where dispatching on an overshoot
20873| beats never dispatching. **That reasoning never looked nine lines down:**
20874| 
20875| ```c
20876| CHECK_ALLOCATION(scsi_cmd = (unsigned char *) malloc(12));
20877| while (inbuf_len > 0) { scsi_cmd[x++] = wdc_get_inbuf(d); inbuf_len--; }
20878| ```
20879| 
20880| `x` is unbounded. **`inbuf_len == 12` is not only selecting the dispatch -- it is the ONLY
20881| thing bounding that copy into a 12-byte allocation.** MEASURED under ASAN: `>= 12` gives a
20882| `heap-buffer-overflow` WRITE at `dev_wdc.c:1048`, **while the detector stays 44 rows
20883| 0 failures on both sides.** The rows could not see it at all.
20884| 
20885| **This is the carrier's SKETCH RULE recurring verbatim** -- *four readers, nine lines,
20886| nobody looked*. agy, kimi, Fable and I all reasoned about `>= 12` as a dispatch-selection
20887| predicate; a grep for `malloc(12)` and `scsi_cmd[x` across the whole artifact directory and
20888| the detector returns **zero hits**, so the bound was never in anyone's field of view. The
20889| brief showed the guard and never the tail it protects, and *when every reader makes the same
20890| mistake, suspect the brief.*
20891| 
20892| L4, corrected in place in both records. The row **`occupancy above 12 does not dispatch`**
20893| now kills it ALONE. It reaches occupancy 14 by preloading thirteen bytes and writing one --
20894| a fixture writing two at a time would dispatch at 12 and never reach the overshoot -- and
20895| its oracle is the dispatch count, so it reds on an ordinary build with no sanitiser.
20896| 
20897| The overshoot objection that motivated the wrong classification is real, and it is answered
20898| at the right layer: **flush the ring**, never widen a bound that guards a `malloc(12)`.
20899| 
20900| *`inbuf_len == 12` sits on the diff's own edited line, so clause (d)'s "predicates
20901| dominating the edited lines" enumeration had already caught it. The enumeration was run;
20902| the consequence of weakening it was assessed BY READING and got the wrong answer. **A
20903| predicate can be correctly enumerated and still misjudged, and only a measurement separates
20904| the two.***
20905| 
20906| ### `wdcringnoflush` -- a measured live defect, and the other entrance to this round's wedge
20907| 
20908| `ATAPI_PKT_CMD` **never flushes the input ring**, and neither reset path does either.
20909| MEASURED: under-drain a DATA-IN and occupancy climbs `32 -> 44 -> 56 -> 68`, so every later
20910| CDB is dropped forever; `ATAPI_SOFT_RESET` leaves it at 32 and the ALT-CTRL reset at 44.
20911| Pre-existing on `d894e35`, `1cec2da` and the live tree.
20912| 
20913| **#477's own comment stated the residue as a property of the REGRESSION.** It is a property
20914| of the DEVICE -- reachable with no stray read at all. Corrected in place, because a wrong
20915| reason gets reused. `dev_asc.c`'s `dev_asc_fifo_flush()` is the in-tree idiom, so the fix
20916| is a transferred warrant rather than a design; filed, not shipped.
20917| 
20918| It also upgrades `wdcsrstnoabort` from READ-and-unmeasured to MEASURED.
20919| 
20920| ### Three defects of my own in this diff, all found by seats, all fixed
20921| 
20922| * **I silently dropped a tab.** My read-arm anchor was `T*3 + "} else if ..."`, and a run of
20923|   tabs is a SUFFIX of any longer run -- so it matched inside the real 4-tab line, consumed
20924|   three and emitted three. The `count == 1` assert passed and was still wrong, leaving the
20925|   brace misaligned with its own `if`. `git show 1cec2da:` settled the original depth.
20926|   **Anchors built from repeated whitespace now carry a leading newline.**
20927| * The `#477` comment block sat physically INSIDE the `#476` latch arm, so it read as
20928|   commentary on the latch. Rehoused into the arm it documents.
20929| * It cited `(:620-626)` -- a bare same-file line citation, the exact form the carrier's
20930|   citation-form rule prohibits. Replaced with the construct name.
20931| 
20932| *A fourth was apparatus rather than product, and two of us hit it independently in the same
20933| session: **`wsl -d Gentoo -- bash -c '...'` from the Bash tool strips shell variables**, so
20934| `X=hello; echo "[$X]"` prints `[]`. It cost the Opus seat two wrong measurements that both
20935| looked like results, and it cost me a `0 of 0` that read as a missing log. Run scripts from
20936| files. Sibling of the documented backslash-mangling and plain-`&` teardown traps.*
20937| 
20938| ### Records
20939| 
20940| The `#476` round block below was **owed and missing** -- `1cec2da` shipped without touching
20941| this file, against the standing rule of a round block per correction. Written now rather
20942| than backdated, and this sentence is the record of the gap.
20943| 
20944| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_477: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC477: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
