FILING TABLE CHECK -- part 05: the OVERLAY that applies your four answers, the re-grades, and the section as it will be filed

Open with the token `ASTRAFILE_05_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 86 overlay lines wrong, <m> of your corrections not applied, <r> of 12 re-grades wrong`

**Context.**  You checked the filing table of the Astra review campaign in four parts
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_01\codex_afile_01.txt` to
`afile_04\codex_afile_04.txt`): 43 wrong rows, 21 missing rows and the duplicate pairs.  The table itself
(`...\astrafiling_20261002\FILING.tsv`) is a mechanical derivation and is NOT edited.  Your corrections are applied as
an explicit overlay:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING_OVERLAY.tsv`
(86 lines: id, field, value, who said so and where; the script that wrote it is beside it as `mk_overlay.py.txt`).
The main loop WROTE THE TITLES in that overlay from the dispositions lines you cited and from the ruling files -- your
answers said what a title should say, not its words -- so those 35 titles and the 21 added rows are new text nobody
has checked.  The result, exactly as it will be filed in `OUTSTANDING_BUGS.md`, is
`...\astrafiling_20261002\draft\bugs554.body.md` (508 rows: every HIGH and MED row under its own heading, the LOW rows
of each wave listed under one class row), and the re-grades of EXISTING queue rows are in
`...\astrafiling_20261002\draft\REGRADES.txt`.

**Please do not simply ratify.**  A correction is not safer than the thing it corrects: this project has a record of
corrections that repeated the error they fixed.  The two dispositions files are
`...\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (D:) and
`...\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md` (H:); read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`, and the artifacts from disk.  Write nothing, build
nothing, run nothing that changes a file.

**Check, and report each failure as one line `<id> | overlay says <X> | should be <Y> | the line (file:line) | confidence`:**
1. Every correction in your four answers is APPLIED -- wrong rows, missing rows, duplicate pairs, the three grades you
   settled -- and none is applied to the wrong row.
2. Every overlay TITLE is true of its dispositions line and of the committed source it names: no claim the line does
   not make, no condition dropped, no line number that is not in the cited text.  Be hardest on the 21 ADD rows.
3. Three choices the main loop made that you did not dictate: the id `armcp15cp14exits` for the three remaining sibling
   exits of `cpu_arm_coproc.c` (D:335-336 left one id owed); MED for `m88kconvdelivery` (D:532 states no grade); and, in
   each duplicate pair whose dispositions "do not choose between these IDs", keeping the FIRST-listed row's id.  Say
   whether each is right; propose the alternative if not.
4. `draft\REGRADES.txt`: each of the 12 re-grades is the grade the retro dispositions give that EXISTING row, the two
   rows left to the peer session are rightly left, and no existing row whose grade the dispositions changed is absent.
5. `draft\bugs554.body.md`: no id appears under two headings or in both a heading and a class list; no id in it exists
   in `OUTSTANDING_BUGS.md` or as a ledger row id at `7440e129`, EXCEPT that an `ID` row's entry already exists in prose
   by design; and the three findings held OPEN between two seats (`hbundle_regress28:F1`, `hdiffdiskimageio:F2`,
   `hgdromcondprobe:F3`) are absent from it.

End with `DENOMINATOR: read <a> of 86 overlay lines against their cited lines; <b> of 12 re-grades; <c> of 508 section rows scanned for id collisions`.
