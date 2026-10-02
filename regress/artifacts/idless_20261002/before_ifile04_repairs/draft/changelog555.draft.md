# `#555` (idless): the queue's id-less entries get ids -- 128 rows, 42 sentences added in place, 105 passages pointed at the id that carries them; none of the rows is fixed here

**Why.**  `OUTSTANDING_BUGS.md` names most rows by a short backticked id, and some entries record an open defect, an
owed measurement or an owed correction in prose only.  A row with no id cannot be claimed, ranked or closed, and the
ledger cannot see it.  GPT-6 Astra scanned the file for such entries at `db8b1a33` (279 claimed entries; the
grok seat found 13 more; 292 dispositions resulted).  This unit files what that review found.  **No
compiled code changes.**

**How each entry was ruled.**  The grok seat (grok-4.7 xhigh) ruled every entry first-hand; GPT-6 Astra confirmed,
overturned or amended each ruling (`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`).  The table derived
mechanically from those lines could not turn an amendment that says "narrowed to ..." into a title, and it reads one
outcome per disposition; grok wrote the titles that needed writing (`grok/grok_ititles.txt`) and settled the
dispositions that name more than one outcome (`grok/grok_icompound.txt`), which restored two HIGH rows the derivation
had dropped.  GPT-6 Astra then checked the table against the dispositions and the source (`ifile_01`: 18 of 127 NEW rows wrong; 3 rows missing; 12 duplicate pairs; qhppcdecode: CONCEDE;
`ifile_02`: 6 of 40 closing sentences wrong; 16 of 84 FILED entries wrong; 18 of 35 KEEP-AS-IS entries owe something; 3 of 6 UNSETTLED wrong).  Nothing in those two answers was adopted on Astra's word, because Astra wrote the scan: grok
ruled every item first-hand (`grok/grok_irule_a.txt`: 25 conceded, 0 held, of 25 items; `grok/grok_irule_b.txt`: 37 conceded, 6 held, of 43 items), each ruling ending in a
RESULT that says what the table should hold, and `mk_itable2.py.txt` applies those RESULT fields and nothing else -- a
title is cut out of grok's line, never retyped.  The six items grok held went back to Astra (`ifile_03`: 5 conceded, 1 held, of 6).

**The one item still disputed after that, and how it is settled.**  GPT-6 Astra holds that `#554`'s row `m88kidleslotsem`
does not cover the accumulating, MMIO and order-sensitive delay slots of the entry it names, because its title states
only the slot that writes the polled word, and asks for a second row (`m88kidleslotfreq`).  grok holds that the id is
the whole entry's.  Both are right about what they read: the id was proposed for the whole entry (queue lines
4675-4682 at `db8b1a33`) and the TITLE stated half of it.  The main loop's resolution, which is neither seat's: the
title is corrected to the entry's own sentence, in the queue heading and in the ledger, and no second row is opened
(`IDLESS_TITLEFIX.tsv`; `mk_itable2.py.txt` checks each clause of the new title against the passage).

**The agy seat's audits.**  agy audited the table's rows against the source.  4 of its 9 audits answered
before its quota wall, and the eight claims in them that no other seat had made were ruled by grok
(`grok/grok_irule_c.txt`: 1 conceded, 5 held, 2 conceded in part, of 8 flags).  What that changed: `qhscifssr` loses the console-overrun clause of its title, which
is `qhx11fifo`'s; the passage of `qhshsqat` is also pointed at `sh4sqexpevt` and `sh4sqwrite` for the two parts those
rows carry; and `qhembargotext` is not filed -- the stale sentence it named sits on the closed row `wdcringambig`, so
the correction is made in place by this commit.  grok read the working tree for that ruling (its `git show` was
refused); `src/devices/dev_sh4.c` there carries another session's uncommitted 126 lines, so the `dev_sh4.c` line
numbers in its first item are the working copy's -- 687, 2788, 2799-2802 and 2815-2824 there are 581, 2662, 2673-2676
and 2689-2698 in the committed file, where the main loop re-read them.

**GPT-6 Astra's closing check of the result and of this text (`ifile_04`):** <OWED: GPT-6 Astra's closing verdict>.

**What is filed.**
* `OUTSTANDING_BUGS.md` -- the `#555` section: 128 rows (7 HIGH, 28 MED, 93 LOW), each an id for an entry
  the file already carries in prose; the 35 HIGH and MED rows under their own headings, the LOW rows by id under the
  class row `idlesslow`; then the 105 passages an id carries, with that id and its ledger state where it is not
  open (12 are carried only by closed or dropped rows), and the 5 entries that stay unsettled, with what is
  unsettled in each and a note that the manuals three of them call unopened or absent are on this machine, outside the
  git tree the seats read.  **42 sentences are added IN PLACE** at the passages the review closed (41) or settled
  (1); `apply555.py.txt` finds each passage by its text -- the scan's line numbers are `db8b1a33`'s -- and
  refuses on a passage that does not occur exactly once.  The heading of `m88kidleslotsem` is corrected in place.
* `tools/pipeline/ledger.json`, `matrix.html` -- 36 rows added (35 individual rows and the class row
  `idlesslow`); the title of `m88kidleslotsem` corrected, with what it read kept in the row's note.
* `CHANGELOG.md` -- this block, prepended.
* `regress/artifacts/` -- 134 files: the id-less review (`idless_20261002/`: the scan's rulings and
  confirmations, the tables and the scripts that made them, the checks and their rulings) and what `#554`'s directory
  gained after that commit was staged.  Seat stderr streams and zero-byte answer files are left on disk, as in `#554`.

**What the checks changed in the table.**  10 ids of the first table (`IDLESS_TABLE.tsv`) do not survive:
9 named work another row already names and were merged into it, and one is the in-place correction above
(`IDLESS_RETIRED.tsv`).  Of the 35 entries first ruled KEEP-AS-IS, 17 turned out to record work an id
carries and are now pointed at it.  The FILED entries whose id is one of the old table's plain-text ids (`OB-22`,
`OB-24`) are pointed at that entry: the existence rule in the main loop's brief was too narrow, grok held against it
and Astra conceded.

**Seats, by name.**  GPT-6 Astra (codex, effort `ultra`): the scan, the confirmations, the checks `ifile_01` to
`ifile_04`; no wall and no refusal on this unit.  grok (grok-4.7 xhigh): every ruling of the scan, the titles, the
compound dispositions, and the three rulings of the checks; two of its ten scan rulings were touched by a runner fault
(two processes writing one file) and the notes are beside those two files.  agy (gemini-3.8-flash-high): it verified
the scan's rows on 2026-10-01 and answered 4 audits of the table; it WALLED at 13:58 on 2026-10-02 (quota,
reset about 18:21), so 5 audits did not run (3 walled at launch, 2 never launched) -- a seat
failure for those, not agreement.  The flagship and Opus agent seats were deliberately not fired (owner instruction,
2026-10-02); the kimi CLI was down (subscription); the Ollama seats were not fired (owner 2026-09-30; they are the
fallback for a content-filter refusal, and none occurred).

**Not done, and where it goes.**  None of the 128 rows is fixed.  The 5 agy audits that did not run.  The
RECORD/L4 corrections of the two Astra reviews (the locator pack `regress/artifacts/recordfix_20261002/` is not part
of this commit).  The flagship sign-off, batched with `#554`'s.  This commit touches no `src/`: the next one owes it
no pass-2 receipt.

