FILING TABLE CHECK -- part 06: the SEVEN repairs made from your part-05 answer (a closing check)

Open with the token `ASTRAFILE_06_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 7 repairs wrong` -- and, if w is 0, the single word `CLOSES` on the next line.

**Context.**  Your part-05 answer
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\afile_05\codex_afile_05.txt`) found six
overlay lines wrong and one re-grade missing.  All seven are repaired; a repair is new text, so it gets its own check,
scoped to the repair -- nothing else in the overlay changed (`FILING_OVERLAY.tsv` is regenerated from
`mk_overlay.py.txt`; the six replaced entries are in `fix_overlay_afile05.py.txt`, both beside the overlay).

**The seven, as they now stand** (read them in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING_OVERLAY.tsv` and
`...\astrafiling_20261002\draft\REGRADES.txt`):
1. `m88ksddovf` (title) -- now carries the amended bounds and the mode/sign conditions on both sides.
2. `M2_gdromnodatawidth` (title) -- now cites `CHANGELOG.md:3124-3143 at 7440e129`.
3. `M1_sh4latchleak` (title) -- now cites `CHANGELOG.md:3124-3133 at 7440e129`.
4. `leregrows` (title) -- now cites `CHANGELOG.md:20714 at 7440e129`.
5. `mipstrapgate` (ADD) -- now states BOTH halves: the REGIMM trap forms made `reserved` below isa_level 32, and the
   SPECIAL trap forms with no ISA gate at `src/cpus/cpu_mips_instr.c:4535-4540`.
6. `shdmteupper` (ADD) -- now says why it is LOW today and that it becomes MED when `sh4dmacintr` lands.
7. `ptywaitstatus` -- added to the re-grades, MED -> HIGH, citing `HARNESS_DISPOSITIONS.md:1029-1030`; the row's heading
   in `OUTSTANDING_BUGS.md` is corrected in place and its ledger grade changed.  Two findings on that class's SCOPE
   (`hbundle_regress28:F1`, `hgdromcondprobe:F3`) remain open between two seats and are not filed.

**Please do not simply ratify.**  For each of the seven say whether the text is now TRUE of the line it cites and of
the committed source at `7440e129` (`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`), whether any
condition is still dropped or any new error was introduced by the rewrite, and for 7 whether re-grading the class row
while two findings on its scope stay open is consistent.  One line per wrong repair:
`<id> | repair says <X> | should be <Y> | the line (file:line) | confidence`.

End with `DENOMINATOR: checked <c> of 7 repairs against their cited lines`.
Read-only: write nothing, build nothing, run nothing that changes a file.
