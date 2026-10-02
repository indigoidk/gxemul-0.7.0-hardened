HARNESS RECORD CORRECTIONS, part 11 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 1 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_11_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing.  The tree under review is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`), and ignore any other `src/` under the project root.

**Context.**  A review of this project's regression harness (its gate scripts, probes and checkers under `regress/`
and `tools/`) found comments and records that say something false or out of date.  Each such finding was ruled
RECORD: nothing is wrong with the code, the SENTENCE is wrong, and a replacement sentence was written.  The
corrections will be made in place, file by file, in later rounds.  Before a sentence can be replaced, somebody has to
find the text it replaces in the committed file and say whether it is still there.  That is this job.  The line
numbers in the dispositions are an older commit's (`db8b1a33`); the files have moved since, so find the text by what
it SAYS.

**For each disposition below, ONE line:**
`<key> | <path>:<first line>-<last line> at 7440e129 | STILL SAYS IT / ALREADY CORRECTED / NOT FOUND | CURRENT: "<the sentence or comment as it stands now, verbatim, at most 300 characters>" | FITS / DOES NOT FIT: <why>`
* `STILL SAYS IT`: the false or stale statement the disposition describes is present.  Quote it exactly as it stands
  (comment markers and all), so that a script can find it.
* `ALREADY CORRECTED`: the place now says what the replacement says, or the statement is gone.  Quote what stands there.
* `NOT FOUND`: you could not find the statement in the file the disposition names.  Say where you looked.
* `DOES NOT FIT`: the replacement sentence would itself be false at `7440e129`, or it describes another place.  Say
  which, with `path:line`.  Your agreement is not what is wanted: a replacement you cannot check against the source is
  `FITS: NOT CHECKED`, never a plain `FITS`.

End with `DENOMINATOR: <a> of 1 dispositions looked up in the committed file`.

**The dispositions** (key | the governing line, cut at 640 characters; where a replacement sentence is quoted in it,
that is the sentence that should stand):
1. hwdcaddtoinbufprobe:F6 | hverify_18:F6 | draft said **RECORD “width-3 inertness in the device remains derived from code inspection, not measured”** | should be **RECORD “The len != 3 escape exercises only widths 1, 2 and 4; it does not measure width-3 behavior. Source inspection establishes that unsupported-width writes push no bytes, but admitting them through the guard can change the bad-width diagnostic and latch.”** | The defaults set `badlen_this` and `warned_badlen` and emit a diagnostic ([dev_wdc.c:1601](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_wdc.c:1601), `:1635`). Thus **codex’s diagnostic/latch qualification is supported**. Apply...
