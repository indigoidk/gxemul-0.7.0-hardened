# Reading task: oldrec513 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC513-d7f5` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #513 sgirekills (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 10789-10859 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
10789| # `#513` sgirekills: five modelled registers ended the host when read back -- and four adversarial passes, three of which found something
10790| 
10791| **THE DEFECT.**  `dev_sgi_re.c` carried SIX read arms of the form
10792| 
10793|     } else {
10794|             fatal("TODO: read from CRIME_RE_TLB_A");
10795|             exit(1);
10796|     }
10797| 
10798| each on the `else` of a `writeflag == MEM_WRITE` test, inside a window whose WRITE path is fully
10799| modelled.  **A guest could store to `CRIME_RE_TLB_A` and reading the same address back ended the
10800| emulator** -- one `ld` on an unmodified `-E sgi -e ip32`.
10801| 
10802| **FIVE BECAME ACCEPT** -- option-set member 4, because the write arm directly above each one already
10803| computes and stores the value, so nothing is unimplemented and a decline would have shipped a wrong
10804| record in product code.  **`CRIME_RE_TEX` became a latched DECLINE** on its own bit: `sgitexindex`
10805| records its write index as a missing factor of four, only 31 of 112 cells are reachable, `re_tex`
10806| has NO consumer in the file, and that row carries a standing do-not-code ruling -- so accepting the
10807| read would publish a mapping the project has already recorded as wrong.
10808| 
10809| **THE FIX HAD TO WRITE `odata`, NOT `data[]`.**  The common tail is
10810| `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata);`, so a read arm filling
10811| `data[]` is overwritten before the guest sees it.  A first draft did exactly that and **would have
10812| returned zeroes while looking correct**; it is now mutant `M2_datafill`.
10813| 
10814| ## THE ORACLE-CORRECTION ORDERING, run rather than asserted
10815| 
10816| Six shipped rows asserted that a len == 8 READ still ends the host.  The fix makes them false *by
10817| succeeding*, so the rows were re-pinned FIRST and the committed build measured RED:
10818| 
10819|     committed build, re-pinned oracles   30/44        PREFIX_RED_20260908.out
10820|     after the fix, SAME script           44/44       POSTFIX_20260908.out
10821|     after the pass-2 repair, on build/   46/46        POSTFIX46_20260908.out
10822| 
10823| Every red row on the pre-fix run was a NEW row; all pre-existing rows and all three controls stayed
10824| green.
10825| 
10826| ## FOUR PASSES.  THE PANEL WAS RIGHT THREE TIMES AND I WAS WRONG THREE TIMES.
10827| 
10828| **PASS 1** refused my six-row design with two floor-shaped holes: an accept row at a window BASE
10829| tests the near bound twice and the far bound never, and a load-only TEX decline row would have been
10830| VACUOUS -- it wants `v0 == 0`, and a later ACCEPT of the zeroed array yields 0 too.  **Both were
10831| then measured**: `M4_readshift` and `M7_farbound` are caught ONLY by the last-slot row, and would
10832| have swept my design clean.
10833| 
10834| **PASS 2** found an L2 floor breach: aliasing the new latch onto `SGIRE_W_UNMAP_RD` escapes, because
10835| no session read TEX and the unmapped address together.  Repaired with two same-instance rows in both
10836| orderings.  **It also found three wrong records in text I had just written**, including the enum
10837| "next free bit is 1 << 11" -- **which this file already records going false the same way for
10838| `SGIRE_W_PRIM_OP`.  I repeated a documented failure while editing the enum that documents it.**
10839| 
10840| **PASS 3** found that repair closed ONE cell of FIVE: bits 6, 7, 9 and 10 are the same one-token
10841| edit on the same line.  **My "#392, unbounded" objection was a strawman** -- the cover is LINEAR,
10842| the edited latch against each other used bit.  Closed with one widened row, not four.
10843| 
10844| *** AND A READING SEAT THEN FOUND A LIVE BUG A GREEN 46/46 RUN HAD ENDORSED. ***  `store()` is
10845| `store(A, addr, op=..., val=...)`; I wrote `store(A, DE_MODE_DST, MODE_LIN_B)`, so the VALUE became
10846| the OPCODE.  Six calls, all wrong the same way -- **the row executed garbage and still scored 46/46,
10847| because its only oracle was the TEX decline count.**  No mutant could have found it: every mutant is
10848| scored against the same broken row.  Repaired twice over -- the calls fixed, AND the row made
10849| SELF-CHECKING (it now wants `1/11`, so a silently-failing setup reds it).
10850| 
10851| **PASS 4** split 3-2 to close, and the surviving objection was kimi's: **only 2 of 11 aliases had a
10852| logged kill against the FINAL row -- the other nine were carried across a row edit, which this
10853| round own doctrine forbids.**  *"Close every cell in ONE diff" deserves "kill every cell on ONE
10854| probe version."*  Hence the sweep below.
10855| 
10856| ## THE MEASUREMENTS
10857| 
10858| ### kill table -- 12 mutants
10859| ```
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_513: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC513: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
