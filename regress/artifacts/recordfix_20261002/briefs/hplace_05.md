RECORD CORRECTIONS IN THE REGRESSION HARNESS, part 05 -- is each note under the statement it corrects, and is it true there?

Open with the token `ASTRAHPLACE_05_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- all 20 notes are placed right and read true`
`VERDICT: <w> of 20 notes wrong`

This is a RECORDS check: comments and docstrings of test scripts against the committed code they describe.  Write
nothing, build nothing, run no emulator.  Please do not simply ratify: the notes were placed by a script, and a script
cannot tell which paragraph of a comment makes the false statement.

**Where things are.**  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is `c29a5fd3`); ignore any other `src/` under the project root.
Everything else below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\recordfix_20261002\`.

**Context.**  Your review of the regression harness found comments and docstrings that state something the code does
not do.  Each such finding was ruled RECORD, with the sentence that is true (`HRECORD.tsv`; the final dispositions are
`..\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md`), and a locator seat quoted the false text verbatim
(`HREC_VERIFIED.tsv`).  The corrections are now PLACED: one note after the paragraph that holds the quoted text, the old
text kept as it was written.  `draft\hrec_05.diff` is the diff against HEAD for this part's 6 files;
`draft\PLAN.tsv` lists every note with its key.  A script has already shown that every change is inside a comment or
a docstring, so no program token changes.  Nothing is committed yet.

**For each added note** (a line that begins `[#556, 2026-10-02 -- a records correction; ...]` and ends with its key):
* PLACE -- does it follow the paragraph that makes the false statement, and not another paragraph of the same comment,
  the end of an unrelated block, or the middle of a list or table?
* TRUE -- is its sentence true of the committed code at HEAD?  Read the code the comment describes.
* READS -- read straight after the old text, is it clear WHICH statement it corrects?
* TOOL -- would its text be picked up by a tool that reads these files as text: a gate that greps a probe for a row
  name or a token, a score such as `13/13` that a checker compares with a gate's pin, a marker a script keys on?
Report only the notes with something wrong, one line each:
`<key> | PLACE / TRUE / READS / TOOL: <what is wrong, path:line> | <where it should go, or what it should say>`

The keys of this part: `hgdromcondprobe:F10`, `hgdromcondprobe:F11`, `hgdromcondprobe:F2`, `hgdromcondprobe:F5`, `hgdromcondprobe:F7`, `hgdromcondprobe:F8`, `hgdromcondprobe:F9`, `hgdromdefaultprobe:F10`, `hgdromdefaultprobe:F11`, `hgdromdefaultprobe:F5`, `hgdromdefaultprobe:F6`, `hgdromdefaultprobe:F7`, `hgdromdefaultprobe:F8`, `hgdromdefaultprobe:F9`, `hhpcmipsctorprobe:F5`, `hbundle_regress4:F6`, `hbundle_regress5:F6`, `hbundle_regress5:F7`, `hbundle_regress27:F10`, `hbundle_regress27:F9`.

End with `DENOMINATOR: <a> of 20 notes read in the diff and in the code they describe`.
