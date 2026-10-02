FILING TABLE CHECK -- part 08 (closing): the outcome of the HIGH-row dispute as applied, and the records text

Open with the token `ASTRAFILE_08_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 32 overlay lines wrong; <r> records sentences wrong` -- and, if both are 0, the single word `CLOSES` on
the next line.

**Context.**  Your part-07 answer
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_07\codex_afile_07.txt`) conceded 11
of the 22 HIGH rows the grok seat disputed, held 11, accepted five conditions and re-worded the sixth.  That outcome is
now applied, as 32 further overlay lines -- lines 88 to 119 of
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING_OVERLAY.tsv` (the block that wrote
them is `fix_overlay_high.py.txt`, beside it) -- and the records that the commit will carry are drafted in
`...\astrafiling_20261002\draft\`: `changelog554.draft.md` (the CHANGELOG block), `section554.draft.md` (the section of
`OUTSTANDING_BUGS.md`, head and all 506 rows), `msg554.draft.txt` (the commit message).  In those drafts the two
strings `DRY-ASTRA` and `DRY-GROK` stand where this answer's verdict and the dispute's one-line summary will go; ignore
them.  The third seat's fact table is `...\astrafiling_20261002\agy\agy_highfacts.txt` and the grok re-read is
`...\astrafiling_20261002\grok\grok_filehigh.txt`.

**Please do not simply ratify.**  The main loop wrote every title and every note in those 32 lines, and the three
records texts, from your answer and grok's; a paraphrase can change a meaning.  Read committed source with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`; read the artifacts from disk.  Write nothing, build
nothing, run nothing that changes a file.

**A. The 32 overlay lines.**  One line per failure: `<id> | overlay says <X> | should be <Y> | the line (file:line) | confidence`.
1. Each of your 11 concessions is applied as MED, with a reason that is yours and is true.
2. Each of your 11 holds stays HIGH and carries a note that states BOTH positions fairly -- yours and grok's -- and does
   not present the dispute as settled.  Is the note's one-sentence statement of your rule a fair statement of your
   sentences (ii) and (iii)?
3. `vgadirtyarm`: the new title is true of `src/devices/dev_vga.c:732-743` and of what you withdrew and what you hold;
   it claims nothing measured.
4. The five conditional titles (`ne2krxbudget`, `taprxquota`, `gdromdmareentr`, `ascwidecount`, and `m88kbcndnest` in
   your wording) are true and carry the condition you accepted, no wider and no narrower.
5. `optpinanyfno` consolidated into `optpinor`: the merged title is true of `tools/pipeline/check_optpin.py:52, :93-98`.

**B. The records text.**  One line per false or unsupported sentence: `<file>:<line> | says <X> | should say <Y> | why`.
Check especially every NUMBER (each is meant to be derived: the row counts, the HIGH count and how many are disputed,
the re-grades, the seats' verdict figures, the file counts), the account of who ruled what, the list of what the
section does NOT file, and the sentence about the carrier's vacuity floor.  Say also whether `section554.draft.md`
files any row that the three seats' answers leave OPEN, and whether any id appears twice in it.

End with `DENOMINATOR: checked <a> of 32 overlay lines; read <b> of the three records drafts in full`.
