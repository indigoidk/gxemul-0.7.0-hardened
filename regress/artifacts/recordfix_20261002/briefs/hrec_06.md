HARNESS RECORD CORRECTIONS, part 06 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_06_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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
1. hdiffm8820x:F4 | hdiffm8820x:F4 | RECORD | RIGHT | RECORD "The callback the SAPR/UAPR register-file arm invokes inside MEM_WRITE." | regress/diff_m8820x.c:132-136; src/devices/dev_m8820x.c:420-435
2. hdiffm8820x:F5 | hdiffm8820x:F5 | RECORD | RIGHT | RECORD "because most rows in this file compare numbers (B2, D2, D6 compare strings)." | regress/diff_m8820x.c:412-418, 494, 587, 673
3. hdiffm8820x:F6 | **hdiffm8820x:F6** | draft said **RECORD “B1 48 unhandled reads complain exactly once”** | should be **RECORD “B1 48 reads, including 47 unhandled offsets, complain exactly once”** | [regress/diff_m8820x.c:487–489](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_m8820x.c:487) performs 48 reads, but `src/include/thirdparty/m8820x.h:86` defines CSSP0 at `0x880`, handled without the default complaint at `src/devices/dev_m8820x.c:488–490`. The source supports **codex’s wording**. | confidence **HIGH**
4. hdiffm8820x:F7 | hdiffm8820x:F7 | RECORD | RIGHT | RECORD "Rows below exercise translation via m88k_translate_v2p(), with F10-F13 checking register/shadow/callback state." | regress/diff_m8820x.c:755-765, 934-943, 958-970, 972-985
5. hdiffm8820x:F8 | hdiffm8820x:F8 | RECORD | RIGHT | RECORD "Two physical pages are recognised and everything else (including FAKE_UNMAPPED_PA) is POISON," | regress/diff_m8820x.c:148-170
6. hdiffm8820x:F9 | hdiffm8820x:F9 | RECORD | RIGHT | RECORD "0x083881c0 (or 0x083881e1 with flags), so bit 31 was never set in any word this file ever stored." | regress/diff_m8820x.c:176-178, 186-215
7. hdiffm8820x:F10 | hdiffm8820x:F10 | RECORD | RIGHT | RECORD "Translation reads five fields out of the shadow (V, SO, PROT and the two block numbers)" | regress/diff_m8820x.c:972-979; src/cpus/memory_m88k.c:156-179
8. hdiffm8invread:F4 | **hdiffm8invread:F4** | draft said **RECORD “…redundant same-value writes are not under-invalidation”** | should be **RECORD “F4, added by #435 alongside G6–G9 and the E9 split, pins historical callback behavior for SAPR and UAPR; skipping the unchanged-value purge is not demonstrated under-invalidation in this model.”** | [regress/diff_m8invread.c:69–76](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/diff_m8invread.c:69) limits the rationale to this model and disclaims demonstrated harm; `:565–576` checks callback counts rather than translation correctness. `CHANGELOG.md:25779–25781` carries the same qualification. The source sup...
9. hdiffwdcidentify:F7 | hdiffwdcidentify:F7 | RECORD | RIGHT | RECORD "Measured escapes closed here: the default: arm guarded on seccnt, head, cyl or sector, and BOTH arms guarded on seccnt, precomp or lba. Seven variants, one leg (drive qualifier remains open at drive=0)." | regress/diff_wdc_identify.c:5241-5275
10. hdiffwdcidentify:F8 | hdiffwdcidentify:F8 | RECORD | RIGHT | RECORD "The enumeration covers thirteen common switch arms, omitting WDCC_DIAGNOSE and all six WDCC_SEC_* cases." | regress/diff_wdc_identify.c:3857-3868, src/devices/dev_wdc.c:967-1064
11. hdiffwdcidentify:F9 | hdiffwdcidentify:F9 | RECORD | RIGHT | RECORD "Two bytes is the smallest two-byte write; single-byte stores are also supported by wd_data." | regress/diff_wdc_identify.c:4652-4658, src/devices/dev_wdc.c:1589,1623
12. hdiffwdcidentify:F12 | hdiffwdcidentify:F12 | draft said RECORD “…keeps occupancy at 512” | should be RECORD “The fixture has 512 bytes free and occupancy SIZE−513. The shipped bound refuses the refill. With the multiplier omitted, the bytewise path admits 512 bytes, then refuses the remaining 512, leaving occupancy SIZE−1. The anchor survives; the occupancy assertion detects partial admission.” | `regress/diff_wdc_identify.c:5048–5055`; `src/devices/dev_wdc.c:245–256,514–541`. Occupancy becomes **262655**, not 512, under the weakened bound. | confidence high
13. hdiffwdcidentify:F13 | hdiffwdcidentify:F13 | RECORD | RIGHT | RECORD "a synthetic packet command state: command in progress, PHASE_DATAIN, no transfer yet allocated." | regress/diff_wdc_identify.c:1578-1588, src/devices/dev_wdc.c:1042-1048
14. hdiffwdcidentify:F14 | hdiffwdcidentify:F14 | draft said RECORD “…geometry overrides clamp cylinders, heads and sectors to 255” | should be RECORD “Heads=300 and sectors-per-track=770 are synthetic fixture values: command-line overrides reject heads or sectors outside 1..255. Cylinders are derived from image size and are not capped at 255.” | `src/disk/diskimage.c:1820–1830` rejects oversized H/S values; `290–297` derives cylinders. The draft’s `140–180` citation concerns overlays. | confidence high
15. hdiffwdcidentify:F15 | hdiffwdcidentify:F15 | RECORD | RIGHT | RECORD "Historically on the fork's only SH4 wdc machine, the driver wrote addr+0x2c while GXemul registered alt-status at addr+0x206 (fixed by #533 to +0x2c)." | regress/diff_wdc_identify.c:2726-2736, OUTSTANDING_BUGS.md:7676,21793
16. hdiffwdcidentify:F16 | hdiffwdcidentify:F16 | RECORD | RIGHT | RECORD "#481's abort row sets write_in_progress, atapi_cmd_in_progress and the ring together and asserts all three are cleared (phase is not asserted)." | regress/diff_wdc_identify.c:4140-4151,4353-4365
17. hgatearm:F7 | hgatearm:F7 | RECORD | RIGHT | RECORD "#311 rewrites ONE line that five instructions share, and three of them were already correct. The pins are the point: they assert that SUB, RSB and CMP --" | regress/gate_arm.sh:6-13,56-61
18. hgatearm:F9 | hgatearm:F9 | RECORD | RIGHT | RECORD "The five cold be * rows use -E barearm (BE) and are the DISCriminators; be warm word and the six le * rows are INVARIANCE CONTROLS" | regress/gate_arm.sh:921-933, regress/arm_endian_probe.py:381-389
