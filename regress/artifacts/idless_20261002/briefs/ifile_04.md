ID-LESS TABLE CHECK -- part 04, the CLOSING check: is the table as finally assembled, and the text that files it, right?

Open with the token `ASTRAIFILE_04_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- nothing wrong in parts A to E`
`VERDICT: <n> things wrong (A: <a>, B: <b>, C: <c>, D: <d>, E: <e>)`

Please do not simply ratify.  I assembled this, so the mistakes that are left are the ones I cannot see: a ruling
applied to the wrong row, a sentence placed under the wrong entry, a number in the text that the tables do not give.
**Which of my dispositions is wrong?**  I applied 62 of grok's concessions, your five concessions of part 03, three
changes from grok's ruling of the agy seat's flags, and ONE resolution of my own (part C).  Check the premises, not
only the arithmetic.

**Where things are.**  The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; ignore any other `src/` under
the project root.  The working tree carries another session's uncommitted edits (`src/devices/dev_sh4.c`,
`dev_lca.c`, `dev_pcc2.c`, `src/cpus/cpu_alpha_palcode.c`, `src/include/thirdparty/mvme_pcctworeg.h`), so read
committed source with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is `1202d342`, the `#554`
commit; no `src/` file has changed since `7440e129`) and the queue as the scan saw it with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`.  Write nothing, build nothing, run
no emulator.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\`.

**What happened since your part 03.**
* `grok\grok_irule_a.txt` and `grok\grok_irule_b.txt` ruled your 68 findings (62 conceded, 6 held); you answered the
  six in `ifile_03\codex_ifile_03.txt` (5 conceded, F12 held).
* The agy seat audited rows against the source; four audits answered (`icite_01`, `icite_02a`, `icite_02b`,
  `icite_03`) before its quota wall, and grok ruled the eight claims in them that no seat had made
  (`grok\grok_irule_c.txt`: 1 conceded, 5 held, 2 conceded in part).  grok read the WORKING tree for that ruling, so
  its `dev_sh4.c` line numbers in item 1 are shifted by the other session's edits (687, 2788, 2799-2802, 2815-2824
  there are 581, 2662, 2673-2676, 2689-2698 at HEAD).
* `mk_itable2.py.txt` applies the RESULT field of every grok line and wrote `IDLESS_TABLE2.tsv` (128 NEW rows),
  `IDLESS_SENTENCES.tsv` (42 sentences to add in place), `IDLESS_CARRIED.tsv` (passages pointed at an id; the five
  UNSETTLED entries), `IDLESS_TITLEFIX.tsv`, `IDLESS_RETIRED.tsv`.
* `draft\` holds what the commit would file: `section555.draft.md` (the section appended to `OUTSTANDING_BUGS.md`),
  `inplace555.draft.diff` (every other change to that file: the 42 sentences as PLACED, and one corrected heading),
  `changelog555.draft.md`, `msg555.draft.txt`, `ledger555.draft.txt`.  The line `<OWED: GPT-6 Astra's closing verdict>`
  in them is where your verdict line goes.

**Part A -- the table.**  `IDLESS_TABLE2.tsv` against the rulings.
1. For each of your 68 findings: does the table now hold what grok's RESULT says?  Report only the ones that do not:
   `<item> | <what the RESULT says> | <what the table holds>`.
2. The three changes from `grok_irule_c.txt`, each against the source at HEAD:
   (1) `qhscifssr` lost the clause ", and the console-overrun sites named beside this are X11-only" from its title, and
   its passage 1980-1982 is also pointed at `qhx11fifo` for that clause;
   (5) the passage 3042-3063 of `qhshsqat` is also pointed at `sh4sqexpevt` (the PREF exception kind) and `sh4sqwrite`
   (the missing write-side translation), and the row's title is unchanged;
   (3) `qhembargotext` is NOT filed: `wdcringambig` is closed (ledger, commit `cf300c0`), so instead of an id under a
   closed row the correction is made in place -- the sentence at queue line 1160 in `inplace555.draft.diff`.  Is that
   sentence true, and is making the correction the right reading of grok's "a records correction on `wdcringambig`"?
3. Is any row of the 128 a duplicate of another row of the 128, or of a ledger row at HEAD, that the earlier parts
   did not catch?  (grok held against five of agy's duplicate claims; say if you think any of those five holds is
   wrong, with the lines.)

**Part B -- the 42 sentences AS PLACED** (`draft\inplace555.draft.diff`).  For each added line: is the sentence true of
the source at HEAD, and does it sit directly after the passage it speaks about -- not inside another entry, not
splitting a sentence or a list item?  You checked 40 closing sentences in part 02; six were replaced by grok's
rulings (S items of `grok_irule_b.txt`), one comes from an UNSETTLED entry grok settled, one is the line-1160 sentence
above.  Report only the wrong ones: `<queue line> | <what is wrong> | <path:line>`.

**Part C -- F12, the item you still hold, and my resolution.**  You held that `#554`'s row `m88kidleslotsem` does not
cover the accumulating, MMIO and order-sensitive slots of queue lines 4676-4682, because its title states only the
slot that writes the polled word; you asked for `NEW MED m88kidleslotfreq`.  grok holds that the id is the whole
entry's.  My resolution is neither: the id was proposed for the whole entry and the TITLE stated half of it, so the
title is corrected to the entry's own sentence (`IDLESS_TITLEFIX.tsv`; the heading change is in
`inplace555.draft.diff`, the ledger change in `ledger555.draft.txt`) and no second row is opened.
Be harder on your own hold than on my fix, and on my fix than on grok's ruling: does the corrected title state
everything your `m88kidleslotfreq` would have stated, against `src/cpus/cpu_m88k_instr.c:2692-2765` at HEAD and queue
lines 4675-4682?  Is there anything ONE row cannot do here that two can (a different grade, a different fix, a
different witness)?  Answer `C | RESOLVED` or `C | STILL HELD: <the reason one row is not enough>`.

**Part D -- the passages pointed at an id** (the list at the end of `section555.draft.md`, 105 passages).
1. Twelve are carried ONLY by rows whose ledger state is closed or dropped: 5500-5503 (`census`), 5563-5573
   (`capgap`), 5575-5580 (`capN`), 5582-5585 (`cflood`), 5587-5605 (`sigunsafe`), 5686-5691 (`mrwgrind`), 6082-6086
   (`m8latch`), 6095-6096 (`m8snprintf`, `m8latch`), 6097-6099 (`gcsections`), 6101-6140 (`ns16550`), 8144
   (`sh4prio0`), 10412-10418 (`gdrompionull`).  For each: does the passage record anything still OPEN that the closed
   or dropped row does not settle?  `<lines> | NOTHING OPEN / OPEN: <what>, <path:line>`.
2. Any passage in the list whose id does not cover it, that part 02 did not already raise.

**Part E -- the texts** (`changelog555.draft.md`, the prose head of `section555.draft.md`, `msg555.draft.txt`).
Report any sentence that is false, and any number that the tables do not give (`MANIFEST.txt` has the derived
numbers).  Two things to check in particular:
1. the note under the UNSETTLED list says the PowerPC and SH manuals three entries call unopened or absent are on this
   machine in `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\` -- list that directory and say whether the note is true;
2. the paragraph "Seats, by name" -- is anything said of your own work there that is not so?

End with `DENOMINATOR: A <findings checked> of 68, <rows read> of 128; B <sentences read> of 42; D <passages read> of
12; E <texts read> of 3`.
