HARNESS RECORD CORRECTIONS, part 04 -- find the text each correction replaces

FIRST line of your answer: `VERDICT: <s> of 18 still say it, <c> already corrected, <m> not found, <w> replacement does not fit`.
SECOND line: the token `AGY_HREC_04_ALIVE_1002`.  THIRD line: quote verbatim the first line of
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
1. hbundle_regress33:F14 | hbundle_regress33:F14 | RECORD | RIGHT | RECORD "Ten encodings still halt, on purpose, and the gate asserts that they DO ... fcmpo/fmadds/fmsubs have no technical blocker at all (fnmadd/fnmsub were fixed in #344)." | regress/gate_ppc_halt.sh:30-38,82-85; regress/ppc_halt_probe.py:55-60,271-275
2. hbundle_regress33:F15 | hbundle_regress33:F15 | draft said RECORD “A semantically-equivalent rewrite that changes the statement text reddens it…” | should be RECORD “C1 fails when the extracted, normalized statement multiset differs from CANON. Compiler miscompilation is invisible because this probe reads source text.” | `regress/arcbios_shift_probe.py:71–79,95–99` strips comments, normalizes whitespace and sorts before comparison. Changing raw statement text need not change that multiset. Codex’s canonical-statement wording is better supported than agy’s unqualified wording. | HIGH confidence
3. hbundle_regress4:F5 | hbundle_regress4:F5 | RECORD | RIGHT | RECORD "With one overlay, break and return 0 produce identical traces (F(d0) S(d0)) because there is no next iteration; deleting continue falls through to bitmap sync (F(d0) S(d0) F(b0) S(b0)), caught by single-overlay but letting break/return pass." | regress/diff_diskimage_sync.c:60-67,162-167; src/disk/diskimage.c:2400-2415
4. hbundle_regress4:F6 | hbundle_regress4:F6 | RECORD | RIGHT | RECORD "Zero cannot be used here: W_BASE0's guard is one of the three arms that accepts it (along with CONF and TB_ENA)." | regress/lca_badval_probe.py:20-27,48-52
5. hbundle_regress5:F6 | hbundle_regress5:F6 | RECORD | RIGHT | RECORD "'print t2' produces a value from register t2 regardless of whether [I] executed (and 'no-checkpoint' only catches a missing print response);" | regress/lca_confbus_probe.py:195-200,490-505,525-535
6. hbundle_regress5:F7 | hbundle_regress5:F7 | draft said RECORD “…never branches on ‘len’, ‘func’ or the bus VALUE” | should be RECORD “This handler tests writeflag, reg == 0 and bus == 0; it never branches on len or func.” Consolidate with the existing retro record correction. | `src/devices/dev_lca.c:259–268` explicitly tests `bus == 0`; `regress/artifacts/astraretro_20260926/DISPOSITIONS.md:741` already directs this correction under `devlca:F5`. Codex’s narrower statement about not distinguishing bus values above 1 is source-supported; agy’s categorical statement is false. | HIGH confidence
7. hbundle_regress5:F8 | hbundle_regress5:F8 | RECORD | RIGHT | RECORD "P: previous selector 5, then nine refusals with read-backs (the FIRST is 8), two EXTRA refusals (16 by sb/sh with read-backs), and the twelfth after PORT=7." | regress/fbctrl_port_probe.py:444-464,630-635
8. hbundle_regress5:F9 | hbundle_regress5:F9 | RECORD | RIGHT | RECORD "V: X1 across a refusal made while COMMAND still holds GET_RESOLUTION, then every cell across five refusals (six total)." | regress/fbctrl_port_probe.py:487,499-501,656-659
9. hbundle_tools1:F5 | hbundle_tools1:F5 | draft said RECORD “…verifies each actually answered…” | should be RECORD “Launches the configured scriptable transports concurrently, waits, and heuristically checks their output. Launch Opus and Fable separately through the Agent tool.” | `tools/panel.sh:438-439` explicitly calls the check heuristic; `:708-709` credits size alone; `:633-639` identifies the external seats. | high
10. hbundle_tools1:F6 | hbundle_tools1:F6 | draft said RECORD “A backgrounded launch loses the waiter…” | should be RECORD “The documented double-backgrounded launch lost panel.sh, the waiter; the seats completed unattended without completion reporting.” | `OUTSTANDING_BUGS.md:6430-6433` describes that particular launch; ordinary backgrounding does not establish inevitable waiter loss. | medium-high
11. hbundle_tools1:F18 | hbundle_tools1:F18 | RECORD | RIGHT | RECORD "Exit status, verdict token, tally and coverage presence checked. No single one has ever been trustworthy here:" | tools/nightly_check.sh:87-106
12. hbundle_tools2:F6 | hbundle_tools2:F6 | draft said RECORD “PRECOMMIT SECTION B CHECKS ALL FOUR…” | should be RECORD “PRECOMMIT COVERS EST IN SECTION A AND THE OTHER THREE TREES IN SECTION B, INCLUDING THE ACCESSIBLE WSL TREE VIA UNC.” | `tools/precommit_check.sh:1010-1025` compares est before section B begins at `:1027`; B checks build, build-asan and WSL at `:1032-1120`. | high
13. hbundle_tools2:F10 | hbundle_tools2:F10 | RECORD | RIGHT | RECORD "CONTAMINATED. gate_ab uses an instruction-progress budget (12B instructions, 120s stall, 1800s backstop) via run_emu_progress." | tools/nightly_battery.sh:11-14, regress/gate_ab.sh:105-120
14. hcheckprobewiring:F10 | hcheckprobewiring:F10 | draft said RECORD “352 rows on unmodified -E alphabook1…” | should be RECORD “lcaisalane (#530): 352 rows on unmodified -E alpha -e alphabook1, expanded from table 1’s 37-row instrument; passing result LCAISALANE_RESULT=352/352.” | `regress/lca_isalane_probe.py:288,382-383` supplies the actual arguments; `src/machines/machine_alpha.c:240-243` distinguishes machine and subtype. | high
15. hcheckprobewiring:F11 | hcheckprobewiring:F11 | RECORD | RIGHT | RECORD "the PowerPC gates historically drove 32-bit parts before gate_ppc.sh wired 64-bit ppc_rldimi_probe.py." | tools/pipeline/check_probe_wiring.py:1288-1293, regress/gate_ppc.sh:130-135, regress/ppc_rldimi_probe.py:54-56,237
16. hcheckprobewiring:F12 | hcheckprobewiring:F12 | STATUS: RIGHT | DISPOSITION: RECORD "alphatbinegsel (#520) table 3: the CLOSING 15-row instrument, matching the oracle logic of shipped regress/alpha_tbi_probe.py" | SUPPORTED: agy | db8b1a33 tools/pipeline/check_probe_wiring.py:1382-1383; blob sizes 28008 (frozen) and 29269 (regress/alpha_tbi_probe.py); diff hunks are contract notes and two row-note strings, oracle expectations unchanged
17. hcheckprobewiring:F13 | hcheckprobewiring:F13 | RECORD | RIGHT | RECORD "m88kexcdeliver detector (#502): the m88k exception-delivery path, 59 fault rows + 2 controls, run by gate_m88k_rounding.sh" | tools/pipeline/check_probe_wiring.py:1548-1549, regress/m88k_exc_probe.py:307-446
18. hcheckprobewiring:F14 | hcheckprobewiring:F14 | RECORD | RIGHT | RECORD "lunaabsentcpu detector (#503): dev_luna88k.c reassert_interrupts(), 37 rows including liveness and device-signature controls, run by gate_m88k_rounding.sh. Also the round's rung-3 WITNESS." | tools/pipeline/check_probe_wiring.py:1553-1554, regress/luna_absentcpu_probe.py:168,356,362,768-769
