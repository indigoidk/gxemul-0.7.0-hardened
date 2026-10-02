FILING TABLE CHECK -- part 09 (closing): the repairs of part 08, two grades and one kind returned to you, and the records text

Open with the token `ASTRAFILE_09_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 13 overlay lines wrong; <r> records sentences wrong; gdromcondhow kind: CONCEDE or HOLD; ptywaitstatus HIGH: CONCEDE or HOLD`
-- and, if both numbers are 0, the single word `CLOSES` on the next line.  (A HOLD does not prevent closing: a held
row is filed with both positions stated, which is what the drafts do.  A CONCEDE that would change what is filed
does prevent it: say exactly what changes.)

**Context.**  Your part-08 answer
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_08\codex_afile_08.txt`) found 11
overlay lines and 24 records sentences wrong -- every one a matter of wording.  They are repaired, and three things
happened since that you have not seen.  Everything below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\` unless a full path is given.

**Please do not simply ratify.**  The main loop wrote every repaired sentence, and a correction is not safer than the
thing it corrects.  Read committed source with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`;
read the artifacts from disk.  The tree under review is `GXEMUL-SEC`; ignore any other `src/` under the project root.
Write nothing, build nothing, run nothing that changes a file.

**A. Thirteen overlay lines changed or added since part 08** (`FILING_OVERLAY.tsv`; the blocks that wrote them are
`fix_overlay_afile08.py.txt` and `fix_filehigh3.py.txt`).  One line per failure:
`<id> | overlay says <X> | should be <Y> | the line (file:line) | confidence`.
1. Lines 99-108, the note on the ten disputed harness rows, restated after your part-08 finding.  Is it now a fair
   statement of your sentences (ii) and (iii) in `afile_07\codex_afile_07.txt` -- no broader, no narrower -- and of the
   grok seat's position?  Does it credit agy's table with exactly what `agy\agy_highfacts.txt` shows?
2. Line 109, `vgadirtyarm`'s title, now qualified by the palette paths you named (`src/devices/dev_vga.c:562-578`).
3. Lines 120-121, `gdromcondhow` -- A ROW RETURNED TO YOU.  Finding `hgdromcondprobe:F3`.  Your confirmation
   (`...\astraretro_harness_20260926\hconfirm_14\codex_hconfirm_14.txt`) made it FILED under the existing class
   `ptywaitstatus`; the grok tie-break had made it NEW HIGH.  It went back to grok with your reasons verbatim
   (`...\astraretro_harness_20260926\adjudication\grok_brief_hopen3.md`), and grok HELD
   (`...\adjudication\grok_20261002\grok_hopen3.txt`).  Its argument, which I believe is the deciding fact -- CHECK IT
   against `regress/gdrom_cond_probe.py` at `7440e129`, do not take it from here: rows R1b (`:419`) and R2b (`:499`)
   compare the announced byte alone and consult neither the liveness verdict nor the collected wait status, so the
   class's repair (folding the wait status into the liveness verdict) would leave both rows green; the defect is
   those rows' own oracle.  The main loop read those lines and filed the row as grok ruled it.
   Say `CONCEDE` (it is its own row) or `HOLD` (it is the class `ptywaitstatus`), with `path:line`.  Either way: is the
   row's title true of the probe, and does its note (line 121) state both positions fairly?

**B. One re-grade returned to you: `ptywaitstatus` MED -> HIGH.**  The raise is yours (your amendments to
`hpcc2widthprobe:F2` and `hppcroundingprobe:F2` in `...\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md:1029-1030`,
and part 05 called the re-grade missing).  A raise by the family that wrote the finding is not adopted on its say-so,
so the grok seat was asked to rule it first-hand under the test it applied to the 57 HIGH rows, together with
`gdromcondhow` (`briefs\grok_filehigh3.md` -> `grok\grok_filehigh3.txt`).  Its answer: 0 of 2 HIGH by that test --
each is "HIGH ONLY ON THE RE-INTRODUCTION RULE (belongs with the disputed rows)": on the paths it read, a process end
after the last observation WOULD pass today, and nothing live ends the process there.
The drafts therefore file both as HIGH AND DISPUTED, exactly like the ten rows you hold: `ptywaitstatus`'s re-grade
note is `draft\REGRADES.txt:15`, the heading it corrects reads "HIGH, the grade disputed between two seats; it said MED
until #554 re-graded it", and `gdromcondhow` carries line 121.
Say `CONCEDE` (the class row stays MED and the re-grade is dropped) or `HOLD` (filed as drafted), with your reason in
one or two sentences.  Is the dispute stated fairly on both sides in `draft\REGRADES.txt:15` and in
`draft\section554.draft.md:45-51`?

**C. The records text**, regenerated: `draft\changelog554.draft.md` (99 lines), `draft\section554.draft.md` (1019
lines: the head, then every row), `draft\msg554.draft.txt` (29 lines).  The string `DRY-ASTRA9` stands where this
answer's verdict will go; ignore it.
1. For each of your 24 part-08 records findings say whether it is REPAIRED; one line per finding that is NOT:
   `<file>:<line> | still says <X> | should say <Y>`.
2. Any NEW false or unsupported sentence, one line each: `<file>:<line> | says <X> | should say <Y> | why`.  Check
   especially:
   * every number, each of which is meant to be derived: 507 open rows = 456 NEW + 26 test coverage + 25 ids; 53 HIGH =
     36 retro + 17 harness; 12 disputed HIGH rows (your ten harness holds, `vgadirtyarm`, `gdromcondhow`) and one
     disputed re-grade; 221 ledger rows added = 218 individual + 2 class rows + `nineseatreminder` closed; 13 re-grades =
     12 by the retro + 1 by the harness review, 11 headings corrected; 120 overlay lines;
   * the account of the three harness findings that were open between two seats (`grok_hopen3.txt`: two conceded, one
     held) and the sentence that the filing table predates their resolution;
   * the account of grok's two later rulings (`grok\grok_filehigh2.txt`: 7 of 7 true as titled, read from the working
     tree; `grok\grok_filehigh3.txt`: above);
   * the list of what the section does NOT file, and the seat paragraph of the CHANGELOG block.
3. The artifact-file count and the stderr-stream count are derived when the commit is staged and they grow with this
   check's own files: do NOT compare them with a number of your own.  Check instead that `draft\prep554.py.txt`
   derives them (the walk over `DIRS`, `*.err` left out, already-tracked files left out).

**D. `HARNESS_DISPOSITIONS.md`'s derived RESULT section was rebuilt**
(`...\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md`, from line 1094; `mk_hdisp.py.txt` beside it; everything
before that line is byte-identical to the file you read, except header lines 16-17).  It now has "ONE KIND, TWO GRADES
(1)", quoting your part-04 sentence, and "OPEN BETWEEN TWO SEATS (0 now; 3 until 2026-10-02)", quoting grok's answers
on their return.  One line per false derived statement: is each statement true of the lines it quotes, is your
part-04 sentence quoted fairly, and is "a HOLD is ... filed as that seat ruled it, with the difference stated in the
row" an accurate description of what the filing does with `gdromcondhow`?

End with `DENOMINATOR: checked <a> of 13 overlay lines; <b> of 24 part-08 records findings re-checked; read <c> of the
three records drafts in full`.
