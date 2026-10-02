FILING TABLE CHECK -- part 10 (closing): the repairs of part 09

Open with the token `ASTRAFILE_10_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 10 overlay lines wrong; <r> records sentences wrong; <h> harness-index statements wrong`
-- and, if all three numbers are 0, the single word `CLOSES` on the next line.

**Context.**  Your part-09 answer
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_09\codex_afile_09.txt`) found 9
overlay lines, 14 records sentences and 2 statements of the rebuilt harness index wrong, conceded `gdromcondhow`'s
kind and held HIGH on `ptywaitstatus`.  No grade and no kind was wrong.  Each finding is repaired; the block that made
the repairs is `fix_afile09.py.txt`.  Everything below is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\` unless a full path is given.

**Please do not simply ratify.**  Two passes in a row found the same class -- a sentence of the main loop's that
described what another seat's table shows -- so this repair does not paraphrase again: each of the nine rows now
carries YOUR OWN wording from part 09, with agy's line number.  Check that I copied it without changing its meaning,
and that I applied it to the right row.  Read committed source with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`; read the artifacts from disk.  The tree under
review is `GXEMUL-SEC`; ignore any other `src/` under the project root.  Write nothing, build nothing, run nothing
that changes a file.

**A. Ten overlay lines changed** (`FILING_OVERLAY.tsv`).  One line per failure:
`<id> | overlay says <X> | should be <Y> | the line (file:line) | confidence`.
1. Lines 100-108, the nine disputed harness rows whose agy clause you faulted.  The first part of each note (grok's
   position, your rules (ii) and (iii)) is byte-identical to what you passed in part 09; the agy clause is now the row's
   own -- your "should say" wording, prefixed with `agy's fact table (agy/agy_highfacts.txt:<line>):`.  Line 99
   (`sgilwreadzero`) is unchanged, as you found it correct.  For each of the nine: is the clause your wording, on the
   right row, with the right line of `agy\agy_highfacts.txt`?
2. Line 121, `gdromcondhow`'s note: the kind is recorded as SETTLED by your part-09 concession, your earlier FILED
   position kept as history, the HIGH dispute kept.  Is that what you conceded, no more and no less?

**B. The records text**, regenerated: `draft\changelog554.draft.md` (106 lines), `draft\section554.draft.md` (1022
lines), `draft\msg554.draft.txt` (30 lines).  The string `DRY-ASTRA10` stands where this answer's verdict will go.
1. Your 14 part-09 records findings -- say for each whether it is REPAIRED; one line per finding that is NOT:
   `<file>:<line> | still says <X> | should say <Y>`.  Where they are now:
   * `changelog554.draft.md:38` and `msg554.draft.txt:14` (the staging check and the headings): the SENTENCE is
     unchanged; the CHECK was changed to make it true -- `draft\prep554.py.txt:155-162` now tests EVERY heading that
     prints a grade for a re-graded id and refuses on any that prints another grade.  Is the sentence true of that code?
   * `changelog554.draft.md:47` (what agy's table corroborates); `:94` (grok's work, by name);
   * `section554.draft.md:15-16` (the 218 individual rows include `shoddprfield`), and the same statement at
     `changelog554.draft.md:72` and `msg554.draft.txt:8`;
   * the nine row notes of `section554.draft.md` (at :538-:565; they print the overlay lines of A.1).
2. The NEW sentences this repair added, one line per false or unsupported one
   (`<file>:<line> | says <X> | should say <Y> | why`): `changelog554.draft.md:23` and `section554.draft.md:32-33`
   (your concession of the kind); `section554.draft.md:51-53` (your HOLD on `ptywaitstatus`, and the kind as a former
   difference); `changelog554.draft.md:62-67` and `msg554.draft.txt:18-19` (the account of part 09 itself: is "nine of
   the ten disputed rows", "five other sentences", "the staging check ... could be satisfied by one heading while a
   sibling stayed stale", "two errors of assembly" a fair account of what you found?); `changelog554.draft.md:91`
   (the checks, by name).
3. The totals have not changed and need no recount unless a line above changes one: 507 open rows; 53 HIGH; 12 disputed
   HIGH rows and one disputed re-grade; 221 ledger rows added; 13 re-grades, 11 headings; 120 overlay lines.

**C. `HARNESS_DISPOSITIONS.md`**
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md`;
`mk_hdisp.py.txt` beside it).  Your two part-09 findings: header line 16 (the word KINDS had been replaced by the list
of draft kinds: the placeholder was that word) and the NEW HIGH index entry for `hgdromcondprobe:F3` (it quoted your
superseded amendment; it now quotes grok's answer on the finding's return, at :1165).  New: your part-09 verdict line
is quoted at :1135-1136.  One line per statement that is still, or newly, wrong.

End with `DENOMINATOR: checked <a> of 10 overlay lines; <b> of 14 part-09 records findings re-checked; <c> of 2
harness-index findings re-checked`.
