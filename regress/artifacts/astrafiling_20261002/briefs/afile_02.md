FILING TABLE CHECK -- part 02: the HARNESS rows of groups 01 to 06 (155 rows)

Open with the token `ASTRAFILE_02_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 155 table rows wrong, <m> rows missing from the table, <d> duplicate or colliding ids`

**The two reviews.**  GPT-6 Astra reviewed this GXemul fork read-only twice: the emulator SOURCE (wave 1, 403 findings)
and the REGRESSION HARNESS (wave 2, 722 findings).  Every finding was then ruled on by an independent seat and the
ruling confirmed or amended; the two results are
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (15 batches; an Astra amendment governs the ruling it names, and each batch's SEVERITY DISPUTE block, where
there is one, governs the grades it lists) and
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md` (18 groups; its header states the precedence, its RESULT section is a derived index).
**The table.**  A records round is about to FILE every new row as a queue row -- a heading in `OUTSTANDING_BUGS.md` and
a row in the ledger.  The rows to file are listed in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING.tsv` (tab-separated: wave, where, key, kind, severity, id, title, governing text), DERIVED MECHANICALLY from the two
dispositions files by the script kept beside it as `mk_filing.py.txt`; its report is `FILING_REPORT.txt`.  Kinds: NEW (a
new queue row), GAP (a test-coverage row), ID (an id assigned to an entry `OUTSTANDING_BUGS.md` already carries in
prose).  The derivation parses prose and CAN BE WRONG -- the hand-written batches 1b to 2e especially.  Nothing is
filed until this check is back.

**Please do not simply ratify, and mind what is being checked.**  You are checking the TABLE against the DISPOSITIONS,
not re-ruling the findings: your own family wrote the findings, so your agreement with a finding is not evidence, but
whether a table row says what its governing disposition says is a plain reading question.  Read committed files only
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`); the two dispositions files and the table are untracked artifacts, read those from
disk.  Write nothing, build nothing, run nothing that changes a file.

**Your part:** the HARNESS rows of groups 01 to 06 -- the 155 rows of the table whose first two columns select them.

**For each row, check four things against its governing disposition:**
1. KIND -- after the amendments, the tie-break and any dispute block, the finding really is a NEW / GAP / ID row, and not
   FILED, L4 / RECORD, DUPLICATE, MERGED, DROP, REFUTED or UNSETTLED.
2. SEVERITY -- the row's grade is the governing grade.
3. ID -- it is the governing id; it exists nowhere in `OUTSTANDING_BUGS.md` at `7440e129` and is no ledger row id
   (`git show 7440e129:tools/pipeline/ledger.json`, the `"id"` fields); and it does not name two different defects in the
   table.
4. TITLE -- one line that states the defect truly; where the governing grade is CONDITIONAL the title or the governing
   text must carry the condition.
**Then:** (a) rows MISSING from the table -- a disposition in your part that makes a finding NEW, GAP or ID while no row
carries it; (b) pairs of rows that are ONE defect under two ids, including one row in each wave.

**For each row you find wrong, one line:** `<id> | table says <X> | should be <Y> | the dispositions line (file:line) | confidence`.
List the rows you checked and found right by id.  End with
`DENOMINATOR: checked <c> of 155 rows against the dispositions`.
