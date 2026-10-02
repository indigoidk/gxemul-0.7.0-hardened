RECORD CORRECTIONS IN THE REGRESSION HARNESS, part 11 -- the three repairs of your part 10

Open with the token `ASTRAHPLACE_11_ALIVE` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the three repairs are right and nothing else changed`
`VERDICT: <w> of 3 repairs wrong`

This is a RECORDS check: comments and docstrings of test scripts against the committed code they describe.  Write
nothing, build nothing, run no emulator.  Please do not simply ratify: two of the three sentences are your own
wording, adopted after the main loop read the code, and those are the ones you are least likely to test.

**Where things are.**  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (HEAD is `c29a5fd3`).  Everything else is under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\recordfix_20261002\`.

**THE DELTA, whole:** `draft\hrec_repairs_11.diff` -- from the stage your part 10 read to the stage as it stands, four
hunks in three files.  Anything there that is not one of the three repairs below is a finding.

1. `hdiffdiskimageio:F5` -- now TWO notes in `regress/diff_diskimage_io.c`: the buffer correction after HEAD:13
   ("Early sections assert return values; later sections assert buffer contents.") and the proof-status correction
   after HEAD:26 ("[PROOF] rows pass on the corrected tree."), as you asked.  Is each under the statement it corrects?
2. `hbundle_regress27:F6` -- grok had HELD the ruled sentence ("...for ceil.w and floor.w, non-zero FCSR.RM ensures
   directed modes differ from inherited modes"); you said non-zero RM does not ensure it.  The main loop read the
   probe's ROWS table (`regress/mips_fixedmode_probe.py:125-128`: `c21rm` and `cn225rm` set RM for ceil.w, `f29rp` and
   `fn225rp` set RP for floor.w) and adopted your sentence: "Only round.w necessarily matches inherited RM=0.  These
   ceil.w rows choose RM=3 and floor.w rows RM=2, with operands chosen to distinguish inherited from forced rounding."
   Is every clause of it true of the probe at HEAD -- including "with operands chosen to distinguish"?
3. `hwdcaddtoinbufprobe:F6` -- grok's sentence stands and gains your qualification at its end: "Writes refused by the
   preceding phase guard (src/devices/dev_wdc.c:1576-1577) reach no width switch and set neither badlen_this nor
   warned_badlen."  The main loop read `dev_wdc.c:1576-1611`.  Is the whole note true and clear?

For each: `<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <a> of 3 repairs read; <h> of 4 hunks read`.
