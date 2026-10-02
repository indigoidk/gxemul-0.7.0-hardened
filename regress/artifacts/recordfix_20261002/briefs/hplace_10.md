RECORD CORRECTIONS IN THE REGRESSION HARNESS, part 10 -- the notes that changed since your parts 01-09

Open with the token `ASTRAHPLACE_10_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- every changed note is placed right and reads true, and nothing else changed`
`VERDICT: <w> of 48 notes wrong`

This is a RECORDS check: comments and docstrings of test scripts against the committed code they describe.  Write
nothing, build nothing, run no emulator.  Please do not simply ratify, and be harder on the sentences grok adopted
from your own proposals than on the rest: a proposal of yours that grok took is the one you are least likely to test.

**Where things are.**  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is `c29a5fd3`).  Everything else is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\recordfix_20261002\`.

**What changed since parts 01-09, and why.**  Your 42 findings: 20 placement errors -- each note now
follows the line you named (`HREC_PLACE_OVERLAY.tsv`); 34 objections to the ruled sentence -- grok ruled each
first-hand (`grok\grok_hrectext.txt`) and the sentence that stands is cut from its line (`HREC_TEXT_OVERLAY.tsv`,
26 sentences changed).  Besides those: four non-verbatim quotes from the agy locator were matched by their
fragments inside the lines it gave, so four notes you did not see are new (`apply_hrec.py.txt`, `loose_last`); the
typographic characters in the notes (ellipsis, curly quotes) became ASCII, because every target file is ASCII; and
one sentence that arrived with a `#` of its own lost it.  Two notes are no longer placed (their files carry
unreviewed working deltas and are not committed), and those are owed, not lost.

**THE DELTA, whole:** `draft\hrec_repairs.diff` -- the diff from the stage your parts read to the stage as it
stands, five lines of context, 53 hunks.  `draft\PLAN.tsv` lists every note with its key and the HEAD line
it follows.  A hunk that none of the above explains is a finding.

**For each changed note** -- the keys: `hbundle_regress18:F16`, `hbundle_regress26:F11`, `hbundle_regress26:F8`, `hbundle_regress27:F12`, `hbundle_regress27:F6`, `hbundle_regress28:F10`, `hbundle_regress28:F11`, `hbundle_regress30:F9`, `hbundle_regress31:F11`, `hbundle_regress33:F15`, `hbundle_regress5:F7`, `hbundle_tools1:F5`, `hbundle_tools1:F6`, `hdiffdiskimageio:F11`, `hdiffdiskimageio:F5`, `hdiffdiskimageio:F6`, `hdiffdiskimageio:F9`, `hdiffm8invread:F4`, `hdiffwdcidentify:F12`, `hdiffwdcidentify:F14`, `hdiffwdcidentify:F16`, `hgatearm:F7`, `hgatehygiene:F12`, `hgatehygiene:F13`, `hgatehygiene:F14`, `hgateoffline:F10`, `hgateoffline:F11`, `hgateoffline:F7`, `hgateshrounding:F15`, `hgdromcondprobe:F9`, `hgdromdefaultprobe:F9`, `hhpcmipsctorprobe:F5`, `hlcaisalaneprobe:F3`, `hm88kroundingprobe:F6`, `hm88kroundingprobe:F7`, `hm88kroundingprobe:F8`, `hpcc2widthprobe:F3`, `hpcc2widthprobe:F4`, `hpcc2widthprobe:F5`, `hsgideprimopprobe:F5`, `hsgirecolourdefaultprobe:F4`, `hsh4valprobe:F3`, `hwdcaddtoinbufprobe:F3`, `hwdcaddtoinbufprobe:F5`, `hwdcaddtoinbufprobe:F6`, `regress22:F10`, `regress22:F6`, `regress24:F10` -- the same four questions as before: PLACE (does it follow the
paragraph that makes the false statement?), TRUE (is the sentence true of the code at HEAD?), READS (is it clear which
statement it corrects?), TOOL (would a tool that reads the file as text pick it up?).  Report only the ones with
something wrong: `<key> | PLACE / TRUE / READS / TOOL: <what, path:line> | <where it should go, or what it should say>`.

End with `DENOMINATOR: <a> of 48 notes read in the diff and in the code they describe; <h> of 53 hunks read`.
