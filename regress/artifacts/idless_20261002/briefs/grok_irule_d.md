ID-LESS TABLE -- ruling D: four passages GPT-6 Astra says a CLOSED ledger row cannot carry, the class they point at, and one amendment of your ruling C

Open with the token `GROK_IRULE_D_ALIVE_1002` on its own line and the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` quoted verbatim, then ONE verdict line:
`VERDICT: <c> conceded, <h> held, <p> conceded in part, of 7 items`.

READ-ONLY.  Write nothing, build nothing, run no emulator.  The tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; ignore any other `src/` under the project root.  On disk,
`src/devices/dev_sh4.c`, `dev_lca.c`, `dev_pcc2.c`, `src/cpus/cpu_alpha_palcode.c` and
`src/include/thirdparty/mvme_pcctworeg.h` carry another session's uncommitted edits; every other source file is the
committed one.  `OUTSTANDING_BUGS.md` on disk is the committed queue; its lines below 16292 are numbered as in
`db8b1a33`.  `tools/pipeline/ledger.json` on disk has the committed state of every row named below.

Please do not simply ratify, in either direction.  Items 1-4 are Astra's findings against FILED dispositions that you
ruled and Astra itself confirmed earlier; item 5 is MY reading of what those four have in common, and I may be wrong
about it; item 6 amends your own ruling; item 7 follows from item 5.  Rule each from the source, the queue and the
ledger -- concede or hold.

**What Astra found** (`regress\artifacts\idless_20261002\ifile_04\codex_ifile_04.txt`, part D).  Twelve queue passages
are pointed only at ledger rows whose state is closed or dropped.  For eight Astra says NOTHING OPEN.  For four it says
the passage still records open work that the closed row does not settle:

1. `OUTSTANDING_BUGS.md:6082-6086` -> `m8latch` (closed).  Astra: "OPEN: per-kind diagnostic latching.  The shared
   flag remains; the assessment names a future fix rather than discharging it.  `src/devices/dev_m8820x.c:55-62,90-97`;
   `tools/pipeline/ledger.json:10387`."
2. `OUTSTANDING_BUGS.md:6097-6099` -> `gcsections` (closed).  Astra: "OPEN: linker portability work.  The builds still
   require the flags; the assessment explicitly says to carry the work into the next m8820x round.
   `regress/gate_offline.sh:729-732,820-822`; `tools/pipeline/ledger.json:10636`."
3. `OUTSTANDING_BUGS.md:6101-6140` -> `ns16550` (closed).  Astra: "OPEN: the divisor guard.  The assessment expressly
   keeps it queued; the division remains unguarded.  `src/devices/dev_ns16550.c:179-181`;
   `tools/pipeline/ledger.json:10772`."
4. `OUTSTANDING_BUGS.md:10412-10418` -> `gdrompionull` (closed, with commits).  Astra: "OPEN: installed tail-reach
   coverage for both recorded rejection arms.  Archived measurements do not supply the missing shipped assertions.  The
   live probe explicitly excludes the full table; newer sibling checks observe other outcomes.
   `regress/artifacts/gdrompionull/gdrom_pio_null_probe.py:21-22`; `regress/gdrom_decline_probe.py:507-512`;
   `regress/gdrom_default_probe.py:1163-1198`; `CHANGELOG.md:17160-17163`."
   Astra adds: "These four obligations need live carrying dispositions.  The three assessment-only closures do not
   justify duplicate defect IDs."

**Item 5 -- the class, which is my reading and is the premise to attack.**  The first three rows were closed on
2026-08-27 by one sweep.  Each row's `state_note` says so in the same words: "CLOSED 2026-08-27 -- EXECUTING A RULING
THAT ALREADY EXISTED ... This row carried a `closure.note` of CLOSE (assess), written by `fable5`, the designated
adjudicator ... Closed on the adjudicator's recorded authority.  No independent re-verification of the underlying
defect was performed today."  My claim: `CLOSE (assess)` signs off the ASSESS STAGE of a row; it does not say the
row's work is done.  The evidence I have, all from the ledger:
* Twenty-two rows carry a `closure.note` beginning `CLOSE (assess)`.  Seven of them are NOT closed and their ruling
  text plainly keeps the work alive: `i8253zero` (held: "CLOSE (assess), and PROMOTE as a small round"), `idesync`
  (in work: "Real class gap ... Sequence it AFTER landiskdisk"), `wdcflood` (in work), `landiskdisk` (in work: "CLOSE
  (assess), and RANK IT UP"), `rtcflood` (held: "A code change to a shipped correction gets its own round"),
  `floodclass` (held), `isaorder` (held: "reproduction first").
* Of the rows the sweep CLOSED on that note, these have an EMPTY `commits` field (or, for `ns16550`, a records-only
  commit) and a ruling text that keeps work alive.  The ruling text is the `fable5` assess entry of 2026-08-22 in each
  row's `entries`:
  `gcsections` -- "Real and small ... Ride the next m8820x round."
  `ns16550` -- "Keep the one-line guard QUEUED, not dropped -- what protects the host today is the optimizer"
  `m8latch` -- "Filed-not-widened-mid-round was right, and the fix shape already exists in-tree"
  `m8sarseq` -- "Legitimate coverage debt on a closed round, correctly filed; the two composed-sequence rows ride the
  next m88k round."
  `xfamscope` -- "Nothing owed beyond the two small edits next time gate_crossfamily is touched."
  `pcchalt` -- "when the PPC probe is written, that reinstatement is its first kill row."
  `wdcstandby` -- "Real (every powerdown issues it), small (accept + status + IRQ per protocol); same wdc round"
  `rtcnarrow` -- "keeping only the silent floor is the honest outcome; reproduction-first for the floor."
  `scunbacked` -- "the wrong COMMENT -- a records defect -- is the cheap, urgent half."
  `m437multi` -- "Genuine but low ... Fine as filed."
  `m437rtmp` -- "One-line scope statement; no code."
I have NOT checked, row by row, whether a later round did the work under another id (a `wdc` round may have
implemented STANDBY IMMEDIATE, for instance).  That audit is the work.

What I propose, for you to rule: file ONE new row in this unit as the live carrier -- say
`NEW MED closeassessrows "the 2026-08-27 sweep closed ledger rows on a CLOSE (assess) note, which signs off the
assess stage; eleven of them have no fix commit and a ruling that keeps work alive, and each needs an audit: done
since, or re-open"` -- with its members named, and point passages 1-3 at it.  It does not re-open any row here: three
of the closures executed the adjudicator's note, and whether to re-open is that row's audit.  Passage 4 is a different
kind (a round closed by commits, with coverage rows measured in a kill table and not installed in the shipped probe)
and would get its own coverage row.  If you think each of 1-3 needs its own row now, or that a closed row may carry
the passage after all, say so and why.

**Item 6 -- Astra amends your ruling C, item 5** (`grok\grok_irule_c.txt`).  Your RESULT pointed the passage of
`qhshsqat`, `OUTSTANDING_BUGS.md:3042-3063`, at `sh4sqwrite` for "the missing write-side translation".  Astra: the
passage does not state that; its three defects (`:3060-3063`) are the PREF exception kind, the AT nesting, and the
fill path's missing privilege check; the write-side translation clause is at `:1931-1936`.  "Keep `sh4sqexpevt`;
remove this `sh4sqwrite` assignment or label it related context ... The distinction is explicit at
`src/cpus/memory_sh.c:289-308,352-357`."  I read `:3060-3063` and it names those three and no translation.  Concede
or hold.

**Item 7 -- a sentence this unit adds that points a remainder at one of the closed rows.**  At
`OUTSTANDING_BUGS.md:5607-5615` the sentence to be added in place reads: "#429 has a detector:
`regress/gate_offline.sh:1090` and `:1361-1365` build `diff_rtc_range`.  The timer-core redesign was refiled as
`rtcnarrow` (`OUTSTANDING_BUGS.md:6695`)."  `rtcnarrow` is one of the rows the sweep closed.  Is anything of the
timer-core redesign or of "the silent floor" still open in the source (`src/devices/dev_rtc.c`, `src/core/timer.c`,
`src/include/timer.h`)?  Should the sentence say the row it names is closed, and is the remainder then carried by the
class row of item 5?

**For each item, ONE line:**
`<n> | CONCEDE / HOLD / CONCEDE IN PART: <why, with path:line> | RESULT: <one of the forms below> | <the lines you read>`

RESULT forms (they are applied by a script, so keep to them):
* items 1-4: `NOTHING OPEN.` or `CARRIED BY `<id>`.` (an OPEN row that exists, or the row of item 5) or
  `NEW <HIGH|MED|LOW> `<id>` "<title>".`
* item 5: `NEW <grade> `<id>` "<title>". MEMBERS: `<id>`, `<id>`, ...` (only the rows whose work you found NOT done)
  or `NOTHING OPEN.`  Say for each row I listed whether you checked it: an unchecked member is listed as
  `UNCHECKED: `<id>`, ...`.
* item 6: `3042-3063 is pointed at `sh4sqexpevt` only.` or `3042-3063 stays pointed at `sh4sqexpevt` and `sh4sqwrite`.`
* item 7: `THE SENTENCE STANDS.` or `THE SENTENCE GAINS: "<the clause to add>".`

End with `DENOMINATOR: <a> of 7 items read in the source, the queue and the ledger`.
