HARNESS RECORD CORRECTIONS, part 09 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_09_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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

End with `DENOMINATOR: <a> of 18 dispositions looked up in the committed file`.

**The dispositions** (key | the governing line, cut at 640 characters; where a replacement sentence is quoted in it,
that is the sentence that should stand):
1. hm88kroundingprobe:F6 | hm88kroundingprobe:F6 | STATUS: RIGHT | DISPOSITION: RECORD "This tree implemented four to six of each (fdiv 4, fadd 5, fmul 5, fsub 6), with #306 adding the twelve missing forms." | SUPPORTED: agy | db8b1a33 regress/m88k_rounding_probe.py:184-190; src/cpus/cpu_m88k_instr.c:1473-1480,3209-3217,3253-3261,3278-3286,3364-3372 (untagged 4/5/5/6, twelve `#306` cases)
2. hm88kroundingprobe:F7 | hm88kroundingprobe:F7 | RECORD | RIGHT | RECORD "# fadd.sdd / fsub.sdd: both sources double; fsub.ssd: single source 1, double source 2; all three single destination." | regress/m88k_rounding_probe.py:219-224; _scratchpad/mc88100.txt:6703-6740
3. hm88kroundingprobe:F8 | hm88kroundingprobe:F8 | RECORD | RIGHT | RECORD "Same-format compares cannot discriminate single subnormals (order preserved), but double subnormals collide under the old rounding (e.g. m=3 and m=4) so same-format double compares can discriminate." | regress/m88k_rounding_probe.py:280-284; src/core/float_emul.c:192-208
4. hpcc2widthprobe:F3 | hpcc2widthprobe:F3 | RECORD | RIGHT | RECORD "A translation of the bit index ('1u << bit' -> '1u << (bit + 1)') maps MASK onto bit 12 (PCC2_W_C040), which reassert_interrupts() reads and writes; bit translation is no longer equivalent." | regress/pcc2_width_probe.py:154-159, src/devices/dev_pcc2.c:141-156,391-398
5. hpcc2widthprobe:F4 | hpcc2widthprobe:F4 | RECORD | RIGHT | RECORD "pcc2c040kill -- FIXED by #512: a legal byte write of 0x04 to GENCTL announces once and suppresses interrupt assertion; every GENCTL lane here keeps that bit clear" | regress/pcc2_width_probe.py:400-402,1365-1366, src/devices/dev_pcc2.c:391-398
6. hpcc2widthprobe:F5 | hpcc2widthprobe:F5 | RECORD | RIGHT | RECORD "The TEST line's operand swap ('&' -> '==') is not caught by 'latch all' (which announces 12 either way); 'latch aba' supplies the distinguishing observation" | regress/pcc2_width_probe.py:142-146
7. hpcc2widthprobe:F6 | hpcc2widthprobe:F6 | RECORD | RIGHT | RECORD "HUH?-CLEAR wide writes land HUH?-clear values; 'latch all zero' writes 0 to every block, so a guard '&& (idata & ~mask)' already fails existing latch-announcement rows" | regress/pcc2_width_probe.py:299-308,823-828,1123-1126
8. hpcc2widthprobe:F7 | hpcc2widthprobe:F7 | RECORD | RIGHT | RECORD "two 4-byte writes to MASK announce ONCE -- deduplication within width 4, not establishing cross-width latch behavior" | regress/pcc2_width_probe.py:862-863
9. hpcc2widthprobe:F9 | hpcc2widthprobe:F9 | RECORD | RIGHT | RECORD "Removing ten exit(1)s and two warn-once latches destroys the tripwire that announced guard growth." | regress/pcc2_width_probe.py:5-7,1224-1227, src/devices/dev_pcc2.c:681-710
10. hppcroundingprobe:F5 | hppcroundingprobe:F5 | RECORD | RIGHT | RECORD "All seven clean cause rows are control rows (expected values unchanged by #330); classifying them as DISC inflates the discriminator count" | regress/ppc_rounding_probe.py:47-50,371-380,1232-1234
11. hppcroundingprobe:F6 | hppcroundingprobe:F6 | RECORD | RIGHT | RECORD "FPSCR is set by DEBUGGER WRITE, with mode verification handled once in verify_mode_writes(); individual mode rows receive None for readback" | regress/ppc_rounding_probe.py:20-22,107-111
12. hppcroundingprobe:F7 | hppcroundingprobe:F7 | RECORD | RIGHT | RECORD "SUMMARY_ROWS defines seven rows (#327 derivation, including FX latch); ad0e67da updated four mtfsf expectations and added seven summary rows" | regress/ppc_rounding_probe.py:54-58,297-337,1220-1223
13. hppcroundingprobe:F8 | hppcroundingprobe:F8 | RECORD | RIGHT | RECORD "mtfsf rows test FM decoding and summary derivation; mtfsf clears preloads 0xffffffff with source 0x0fffffff to test mask clearing" | regress/ppc_rounding_probe.py:761-778,791-803
14. hppcroundingprobe:F9 | hppcroundingprobe:F9 | RECORD | RIGHT | RECORD "Publishing to memory is the probe's readback path (though cpu_register_dump in cpu_ppc.c implements GPR and FPR printing)" | regress/ppc_rounding_probe.py:830-834, src/cpus/cpu_ppc.c:401-422,457-473
15. hppcroundingprobe:F10 | hppcroundingprobe:F10 | RECORD | RIGHT | RECORD "Table expectations are post-fix values; COMMITTED_BEFORE records pre-#304/#305 baseline values where NaN payloads and signs were destroyed" | regress/ppc_rounding_probe.py:873-878,941,958,1117-1126
16. hppcroundingprobe:F11 | hppcroundingprobe:F11 | RECORD | RIGHT | RECORD "fctiwz 1.0 control verifies operand register reading; NaN and out-of-range rows expect nonzero sentinels (0x80000000 or 0x7fffffff)" | regress/ppc_rounding_probe.py:986-990,1010-1016
17. hppcroundingprobe:F12 | hppcroundingprobe:F12 | RECORD | RIGHT | RECORD "The operand 0x3ff0000018000000 is 1 + 3*2^-25 (3/4 single ULP, not 3/2 ULP); half-ULP ties are mode-dependent under directed modes" | regress/ppc_rounding_probe.py:888-896
18. hprecommitcheck:F14 | hprecommitcheck:F14 | RECORD | RIGHT | RECORD "tools/est_divergence.txt is an exemption allowlist whose members are unconditionally skipped rather than recomputed and verified" | tools/precommit_check.sh:1004-1018
