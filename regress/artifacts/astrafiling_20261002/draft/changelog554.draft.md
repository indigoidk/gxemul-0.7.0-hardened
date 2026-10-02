# `#554` (astrafile): the Astra review campaign is FILED -- 510 open rows from GPT-6 Astra's retro review of the source and its review of the regression harness, each ruled by a seat of another family and confirmed; none of them is fixed here

**Why.**  The owner asked on 2026-09-26 for GPT-6 Astra to review the old patches as well ("If astra hasn't reviewed old
patches; please do that as well" / "keep pushing astra").  Two read-only reviews followed: the emulator SOURCE (wave 1:
403 findings in 15 batches, `regress/artifacts/astraretro_20260926/`) and the REGRESSION HARNESS (wave 2: 722
findings in 18 verification groups, `regress/artifacts/astraretro_harness_20260926/`).  A finding is one reviewer's
reading; this unit is what makes the reviews usable -- every finding ruled, the rulings confirmed, and the open ones
given queue rows.  **No compiled code changes.  None of the 510 filed rows is fixed here; one further harness
finding, the round reminder's stale roster (`nineseatreminder`), is fixed by this commit and filed closed.**

**How each finding was ruled.**  Wave 1: twelve batches ruled first-hand by the flagship seat (claude-fable-5-1 by its
transcripts) and three -- 3f, 3g, 3h -- by the grok seat (grok-4.7 xhigh) after the owner's instruction of 2026-10-02
that the working seats are GPT-6 Astra, agy and grok; every batch then CONFIRMED by GPT-6 Astra, which overturns and
amends the ruling it names.  Astra RAISED three of its own findings over grok's ruling; a raise by the author family is
not adopted on its say-so, so those went back to grok with Astra's reasons verbatim and grok conceded all three after
re-reading the source (`adjudication/grok_20261002/grok_dispute3fh.txt`) -- `ne2krxbudget`, `taprxquota` and
`dyncacheoffset32` are HIGH, each on a stated condition.  Wave 2: every finding verified against the committed tree by
an independent seat (grok for eight groups, agy for ten) with a draft disposition, the drafts confirmed by Astra
(`hconfirm_NN/`: 39 overturned, 104 amended; it lowered 34 grades and raised 27), and the 21 rows where the agy and
codex verifications differed ruled first-hand by grok.  Three findings on which that tie-break and Astra's confirmation
gave different KINDS went back to grok (`adjudication/grok_20261002/grok_hopen3.txt`): it conceded two (one is the
filed class `ptywaitstatus`, one is a RECORD correction) and held the third, filed here as `gdromcondhow` after the
main loop read the probe lines it rests on; GPT-6 Astra conceded that kind when asked again (`afile_09`).  The two
results are `DISPOSITIONS.md` (15 batches, the batch headers sum
to 403) and `HARNESS_DISPOSITIONS.md` (governing kinds: DROP 10, FILED 171, FILED-BY-PROSE 19, MERGED into an existing row 5, NEW HIGH 29, NEW LOW 242, NEW MED 65, RECORD 181).

**What is filed, and how the table was checked.**  `regress/artifacts/astrafiling_20261002/FILING.tsv` is derived
mechanically from the two dispositions files (`mk_filing.py.txt`).  GPT-6 Astra then checked the table against the
dispositions in four parts (`afile_01..04`): the harness rows were nearly clean, the rows derived from the seven
hand-written retro batches were not -- 43 wrong rows, 21 missing, eight duplicate pairs -- and those corrections are
applied as an explicit overlay (`FILING_OVERLAY.tsv`, 123 lines by the end, each naming who said so and where; the
table itself is never edited, and it was derived while four harness findings were still listed as open between two
seats: what became of them is carried by the overlay lines `hygieneartifactlive` and `gdromcondhow`, not by a second
derivation).  The overlay's titles were written by the main loop, so Astra checked the overlay, the
re-grades and the section as filed (`afile_05`): 6 of the 86 lines then in it wrong -- three line citations that had
moved since the reviewed commit, two titles that had dropped a condition and one that had omitted the opposite half of
its defect -- and one re-grade missing (`ptywaitstatus`).  All seven were repaired, and its check of the repairs
(`afile_06`): 1 of 7 repairs wrong -- the `ptywaitstatus` re-grade, which the brief had described as applied when it exists only in the staged files; the staging step now refuses unless every re-grade is in the staged ledger and in every heading that prints a grade.

**The HIGH rows were re-read first-hand, and that changed eleven grades.**  A row graded HIGH gets a correction round,
so the grok seat re-read the 57 rows graded HIGH at that point against the committed source (`grok/grok_filehigh.txt`):
29 true as titled, 6 true only under a condition the title omitted, 22 not HIGH or not true -- 21 of those in the
harness wave, where 16 of the HIGH grades were Astra's own raises.  The 22 went back to Astra with grok's reasons
verbatim (`afile_07`): it CONCEDED 11 (now MED: the check still fails on a real emulator death, or the severe
consequence was unproved) and HOLDS 11 -- ten harness rows and `vgadirtyarm`.  The agy seat, asked for the facts alone
(`agy/agy_highfacts.txt`), found a real emulator death still fails the check in 9 rows and the protected path no longer
process-ending in 19.  That corroborates the facts its table states -- it does not establish Astra's separate
bounds-regression premise for `sgilwreadzero` -- and leaves a dispute about the RULE -- is a check that would accept the
re-introduction of a defect fixed today HIGH? -- beside two points Astra marks UNSETTLED
until measured (the VGA endpoint conversion and redraw time; whether the MIPS probe accepts an RI followed by a process
exit).  The ten held harness rows are filed HIGH with both positions stated in each.  `vgadirtyarm` is held on a
different ground: the ruling's "-1.7e9 dirty-row origin ... for hours" is WITHDRAWN (`dev_vga.c:732` declares `int r`,
so the start row is a small negative), and the row is re-stated on the unsigned END-row arithmetic at `:743`,
unmeasured.  Five of the six conditions went into the titles and the sixth was re-worded by Astra; `optpinanyfno` is
consolidated into `optpinor`.  Astra's check of that outcome as applied, and of this text (`afile_08`), found no wrong
grade or kind and wording to correct: the note on the ten disputed rows had broadened its rule and credited agy with
more than it showed, one title was unqualified, and 24 sentences of the drafts were inaccurate -- all corrected.  The
seven HIGH rows the table check had added were outside grok's 57 and were read separately (`grok/grok_filehigh2.txt`):
7 of 7 true as titled (read from the working tree: `git show` was refused to the seat, and none of the files these rows name carries an uncommitted edit).  Two HIGH grades had been outside every re-read -- the new row `gdromcondhow` and the MED-to-HIGH re-grade
of the existing class row `ptywaitstatus`, GPT-6 Astra's own raise -- and grok, asked to apply its own test to them
(`grok/grok_filehigh3.txt`), called both HIGH only on the re-introduction rule; both are filed HIGH and disputed like
the ten.  Astra's check of all of that (`afile_09`) conceded `gdromcondhow`'s kind, held HIGH on `ptywaitstatus`, and
found wording to correct again: one shared note mis-described what agy's table shows on nine of the ten disputed rows
(each row now carries its own clause, in Astra's wording, with agy's line), five other sentences of the drafts were
inaccurate, the staging check of the re-graded headings could be satisfied by one heading while a sibling stayed stale
(it now tests every heading), and the rebuilt harness index had two errors of assembly.  All corrected, and its check
of the corrections (`afile_10`) closed that chain: 0 of 10 overlay lines, 0 records sentences and 0 harness-index
statements wrong.  agy, the AUTHOR of the fact table, was asked the same question about the ten clauses
(`agy/agy_highfacts2.txt`) and flagged four as one-sided -- each left out the half of its line that points the other
way -- so every disputed row now also carries agy's own three verdicts, cut verbatim from its line.

**Three rows the table had missed, found by a mechanical check.**  The dispositions of the next unit (the queue's
id-less entries) name three ids as already filed that existed nowhere: `ramspaninval`, `tcpdebugopts`, `jazzlbmask`.
The retro rulings had written `CONFIRMED-FILED <id>` for each -- the defect IS in the queue's prose, and the id was the
ruling's proposal -- and the table read that as nothing to file.  A check that every id a disposition calls filed
exists somewhere (`chk_filed_exist.py.txt`) found exactly these three.  They are added as ids for prose entries, after
the grok seat read each first-hand again (`grok/grok_file3ids.txt`): 1 of 3 true as titled and rightly graded, 2 needed a change -- `ramspaninval` is conditional on the paths that skip the 1 KB split, and the first title of `jazzlbmask` was not true (the LB_IE address is handled, as the timer value; it is the enable bits that are unused); both titles now carry grok's reading and the three grades stand (read from the working tree).  GPT-6 Astra's closing check of the three
additions and of agy's verdict lines (`afile_11`): 0 of 14 overlay lines wrong; 0 records sentences wrong; 0 further rows of the same shape missing -- CLOSES (both dispositions files read in full for the missing-row question, and the existence check reproduced: 268 mentions, none missing).  One clause was added after that check -- the
zero-byte files left out of the commit, under "The files" below -- and Astra checked it together with the list of
files this commit adds (`afile_12`): 0 files wrongly in the list; 0 files wrongly left out; 1 sentence wrong -- "The files" did not name `CHANGELOG.md` itself, and the bullet it asked for is added in its words (1,096 listed paths checked against the rule, the seven directories walked, 332 launch logs read, no never-commit path and no credential pattern found).
**Result: 510 rows -- 456 NEW, 26 test-coverage rows and 28 ids for entries `OUTSTANDING_BUGS.md` already
carried in prose; 54 HIGH, 12 of them disputed.**  The re-grade of `ptywaitstatus` is disputed as well.

**The files.**
* `CHANGELOG.md` -- this `#554` block, prepended to the existing changelog.
* `OUTSTANDING_BUGS.md` -- the 2026-10-02 `#554` section: every HIGH and MED row (and `shoddprfield`, filed with both grades) under its own heading, the LOW rows of
  each wave written out by id under one class row; and 11 existing headings corrected IN PLACE for the 13
  existing rows the campaign re-graded (12 by the retro, 1 by the harness review).  What the section does NOT
  file is listed in it.
* `tools/pipeline/ledger.json`, `matrix.html` -- 224 rows added (221 individual open rows, the two class rows
  `astraretrolow` with 52 members and `astraharnesslow` with 237, and `nineseatreminder`, filed closed), 13 rows
  re-graded, and `crimewidthkill`'s commit recorded (`#529`, 7440e129).
* `tools/hooks/round_reminder.sh` -- the harness finding `nineseatreminder`, fixed and filed closed: the SessionStart
  text named "Codex 5.6-SOL" and "Grok 4.6" (both stale) and the TaskCompleted text said `./panel.sh for six`.  The
  reminder now names no model -- it points at `panel.sh`'s own variables and at the owner's rulings -- states that agy
  fires only when `PANEL_FIRE_AGY` is set, and names the launch as `bash GXEMUL-SEC/tools/panel.sh <ABSOLUTE brief
  path>` (the script path relative to the project root, the brief's absolute).  Both modes emit valid JSON before and
  after (`astrafiling_20261002/hookfix/`).
* `regress/pass2_ledger.tsv` -- `#529`'s pass-2 receipt (7440e129), which the commit after it owes.
* `regress/artifacts/` -- the campaign's 1101 files: the reviews, the briefs, the rulings, the confirmations, the
  agy and grok job sets, the two dispositions files and the filing table with its checks.  **The seats' stderr streams
  are NOT committed**: 376 `*.err` files, 226 MB, stay on disk beside the answers they belong to; no record cites one.
  37 zero-byte files -- answer files of jobs that produced no output -- are left out as well: the committer
  refuses an empty file.

**Seats, by name.**  GPT-6 Astra (codex, effort `ultra`): the two reviews, every confirmation, the six checks of the
filing table (`afile_01` to `afile_06`), its answer to the HIGH dispute (`afile_07`) and five closing checks
(`afile_08` to `afile_12`) -- none walled or refused on 2026-10-02.  grok (grok-4.7 xhigh): three batch rulings, the
severity dispute, the harness tie-break and its three returned rows, eight harness verification groups, the two HIGH
re-reads, its ruling on two further grades and its read of the three rows added last.  agy (gemini-3.8-flash-high): ten harness verification groups, the draft checks, the fact table under the
disputed rows and its own check of the clauses that describe that table; its agreement is given no weight, its flags
and facts are.  The flagship seat: twelve batch rulings
before 2026-10-02, then DELIBERATELY NOT FIRED by owner instruction, as was the Opus seat (its two answers of
2026-10-01 on the HIGH panel were opus-4-8 fallbacks and are labelled so).  The kimi CLI was down (subscription); the
Ollama seats were not fired (owner 2026-09-30).  No seat is counted as agreeing by its absence.

**Not done, and where it goes.**  The L4 / RECORD corrections (false comments and records) are owed in place, by file
family; 12 HIGH grades and one re-grade are filed as disputed and the three rule questions are unsettled; the
flagship sign-off on
the grok-ruled batches and the harness wave is batched; the id-less entries of `OUTSTANDING_BUGS.md` are a separate
unit; the two rows of the peer session that the retro re-grades are left to it.  The next commit owes this one no
pass-2 receipt: it touches no `src/`.

