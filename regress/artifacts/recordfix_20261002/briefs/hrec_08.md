HARNESS RECORD CORRECTIONS, part 08 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_08_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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
1. hgdromcondprobe:F7 | hgdromcondprobe:F7 | RECORD | RIGHT | RECORD "converts 'the rig was alive when we started' into 'the rig was still alive at the end (though intermediate sessions can still fail)'" | [regress/gdrom_cond_probe.py:990-1016](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L990-L1016), [OUTSTANDING_BUGS.md:13820-13830](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/OUTSTANDING_BUGS.md#L13820-L13830)
2. hgdromcondprobe:F8 | hgdromcondprobe:F8 | RECORD | RIGHT | RECORD "Clause (e) includes 'forging readiness so a later DATA READ finds data (R12)'; this consequence lands in the WRITE path." | [regress/gdrom_cond_probe.py:53-68](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L53-L68), [regress/gdrom_cond_probe.py:885-895](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L885-L895)
3. hgdromcondprobe:F9 | hgdromcondprobe:F9 | RECORD | RIGHT | RECORD "which is why an earlier version of R12 remained a member of the class until line 772 added the COND decline announcement." | [regress/gdrom_cond_probe.py:760-775](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L760-L775), [regress/gdrom_cond_probe.py:925-935](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L925-L935)
4. hgdromcondprobe:F10 | hgdromcondprobe:F10 | RECORD | RIGHT | RECORD "Kills a mutant that reinstates exit(1) (detected via how != exit0) and one that declines SILENTLY." | [regress/gdrom_cond_probe.py:390-405](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L390-L405)
5. hgdromcondprobe:F11 | hgdromcondprobe:F11 | RECORD | RIGHT | RECORD "the 0x%02x -> 0x%02d fidelity mutant (0xaa formats as 170, leaving m absent)." | [regress/gdrom_cond_probe.py:164](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L164), [regress/gdrom_cond_probe.py:412-423](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_cond_probe.py#L412-L423)
6. hgdromdefaultprobe:F5 | hgdromdefaultprobe:F5 | RECORD | RIGHT | RECORD "0x6313 is MOV R1,R3 (low nibble 0011); MOV.L @R1+,R3 is 0x6316 (low nibble 0110)." | [regress/gdrom_default_probe.py:228-232](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L228-L232), [_scratchpad/sh4_programming.txt:13660-13695](file:///C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/sh4_programming.txt#L13660-L13695)
7. hgdromdefaultprobe:F6 | hgdromdefaultprobe:F6 | RECORD | RIGHT | RECORD "which a declined default read (returning 0) cannot satisfy, distinguishing implemented from default." | [regress/gdrom_default_probe.py:405-415](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L405-L415)
8. hgdromdefaultprobe:F7 | hgdromdefaultprobe:F7 | RECORD | RIGHT | RECORD "scores full marks on the default-trigger rows above (though impl ok would catch CNTHI deletion)." | [regress/gdrom_default_probe.py:410-415](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L410-L415), [regress/gdrom_default_probe.py:515-525](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L515-L525)
9. hgdromdefaultprobe:F8 | hgdromdefaultprobe:F8 | RECORD | RIGHT | RECORD "The scan hardcodes 64 words and 56 declines; accept8 iterates IMPLEMENTED_WORDS." | [regress/gdrom_default_probe.py:207](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L207), [regress/gdrom_default_probe.py:570-585](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L570-L585), [regress/gdrom_default_probe.py:610-620](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L610-L620)
10. hgdromdefaultprobe:F9 | hgdromdefaultprobe:F9 | RECORD | RIGHT | RECORD "at L=14 it leaves ONE space, so the gate's ^$v  anchor matches 0 lines and the gate fails." | [regress/gdrom_default_probe.py:280-288](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L280-L288), [regress/gdrom_default_probe.py:885-895](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L885-L895), [regress/gate_sh_rounding.sh:580-590](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_sh_rounding.sh#L580-L590)
11. hgdromdefaultprobe:F10 | hgdromdefaultprobe:F10 | RECORD | RIGHT | RECORD "Transfering formerly printed before the d->data == NULL check; #462 moved it below the check." | [regress/gdrom_default_probe.py:1375-1380](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L1375-L1380), [src/devices/dev_dreamcast_gdrom.c:1395](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c#L1395), [src/devices/dev_dreamcast_gdrom.c:1475-1500](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_gdrom.c#L1475-L1500)
12. hgdromdefaultprobe:F11 | hgdromdefaultprobe:F11 | RECORD | RIGHT | RECORD "Latent today (all 60 rows always run) and" | [regress/gdrom_default_probe.py:418-425](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py#L418-L425), [regress/gate_sh_rounding.sh:522-526](file:///C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/gate_sh_rounding.sh#L522-L526)
13. hhpcmipsctorprobe:F5 | hhpcmipsctorprobe:F5 | RECORD | RIGHT | RECORD "* machine->path replaced by a hardcoded \"machine[0]\"  -> C5, S4" | regress/hpcmips_ctor_probe.py:72,351-359,579-583,681-686; src/machines/machine_hpcmips.c:288-292
14. hlcaisalaneprobe:F3 | hlcaisalaneprobe:F3 | RECORD | RIGHT | RECORD "#  A doubled store delivers 0xAA twice, so TWO replies queue and DIB is STILL 1 after the single pop.  A phantom read on 0x64 is inert and does not pop the reply (see :989); this session detects duplicate stores." | regress/lca_isalane_probe.py:962-971,987-995; src/devices/dev_pckbc.c:1015-1025
15. hlunaabsentcpuprobe:F4 | hlunaabsentcpuprobe:F4 | RECORD | RIGHT | RECORD "EVERY PLANTED PROGRAM SLOT IS DISASSEMBLED AND ITS TEXT CHECKED BEFORE IT IS STEPPED (PARK AND VBR+8 BRANCHES UNCHECKED)." | regress/luna_absentcpu_probe.py:19-20,262-266,313
16. hlunaabsentcpuprobe:F5 | hlunaabsentcpuprobe:F5 | RECORD | RIGHT | RECORD "On the pre-fix binary the witness reads PRE_FIX_SYMPTOM at row soft1 (session A) and at siofirst (session A2); on HEAD it reads PASS." | regress/luna_absentcpu_probe.py:91-95,776; src/devices/dev_luna88k.c:178,1072
17. hlunaabsentcpuprobe:F6 | hlunaabsentcpuprobe:F6 | RECORD | RIGHT | RECORD "ONE cold-debugger session per SESSION below (except B3, which boots a second session for noreenter/redeliver)" | regress/luna_absentcpu_probe.py:17,504,518,520
18. hm88kroundingprobe:F5 | hm88kroundingprobe:F5 | RECORD | RIGHT | RECORD "A decode without the 2<->3 swap inverts the directed rounding modes, failing both positive directed rows (toward+Inf rounds down and toward-Inf rounds up) as well as the negative rows." | regress/m88k_rounding_probe.py:20-25,68-75,153-155
