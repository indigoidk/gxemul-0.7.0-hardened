ROWS FILED BY #555, part 2 -- do the title and the queue passage of each row agree with the committed source?

FIRST line of your answer: `VERDICT: <f> of 20 rows flagged, <n> not checked`.  SECOND line: the token `AGY_ICITE2_2_ALIVE_1002`.
THIRD line: quote verbatim the first line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

READ-ONLY, always: write no file, run nothing that changes a file, build nothing, and stay in the foreground.  The
tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `c29a5fd3`; read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show c29a5fd3:<path>`), and ignore any other `src/` under the project root -- the working
tree also carries another session's uncommitted edits.  Queue line numbers below are commit `db8b1a33`'s: read that
text with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`.

**Context.**  This project's bug queue, `OUTSTANDING_BUGS.md`, names most rows by a short backticked id; some entries
recorded open work in prose only.  Commit `c29a5fd3` (`#555`) gave those entries ids: its section is at the end of the
queue file at that commit, and its tables are in `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002` (`IDLESS_TABLE2.tsv`, `IDLESS_CARRIED.tsv`).  Each row was
ruled by one seat and confirmed by another.  YOUR AGREEMENT IS NOT WHAT IS WANTED.  What is wanted is a FLAG: a line
that the committed source or the queue text does not support.  A line you cannot check is `NOT CHECKED: <why>`, never
a pass.

**For each row below, ONE line:**
`<id> | TITLE: TRUE / WIDER than the source shows: <what> / NARROWER: <what it leaves out> / NOT TRUE: <what the source shows> | PASSAGE: says this / says something else: <what> | <the lines you read>`
* Read the queue passage (the line range) and the source it names.  A title is checked against the SOURCE at
  `c29a5fd3`, not against the wording of the ruling.
* Where the title names a CONDITION (a CPU model, a mode bit, "latent", an owed measurement), check that the condition
  is real and is stated.
* A row that describes work already done at `c29a5fd3` is `NOT TRUE: done -- <path:line>`.

Then: **(a)** two rows of this part that are one piece of work (name both ids); **(b)** a row whose work the queue
ALREADY files under another backticked id (name the id and the queue line);
**(c)** `DENOMINATOR: <s> of 20 rows read in the source`.

**The rows** (id | grade | queue lines at db8b1a33 | title | the line that governs it, cut at 420 characters):
1. `gdrommaskclaim` | LOW | 13274-13279 | Owed correction of the GDROM comment that still promises a new warn site cannot reuse another site's bit, a promise the following sentences retract. | 13274–13279 | grok said FILED gdromlatchreuse | should be NEW LOW gdrommaskclaim | `OUTSTANDING_BUGS.md:13264–13272,13286–13288` defines the existing defect and its closure as missing cross-site latch coverage. Adding that coverage does not correct the separate false promise at `src/devices/dev_dreamcast_gdrom.c:191–193`, contradicted by `:207–213`. Grok incorrectly changed the scan here: the coverage gap and the ...
2. `pcc2rxiackwrite` | MED | 15038-15040; 15525-15530 | Both queue passages record one defect: a guest write of SCCRXIACK acknowledges the RX interrupt without a direction check, and TX or modem acknowledge work leaves that write unchanged | 15038–15040; repeated 15525–15530 | grok said FILED pcc2iackmodel | should be NEW MED pcc2rxiackwrite, merging the repeated occurrence | At `db8b1a33`, `OUTSTANDING_BUGS.md:15034–15037` scopes `pcc2iackmodel` to missing TX/modem acknowledgment semantics. The RX warning at `:15038–15039`, also copied into `tools/pipeline/ledger.json:35672`, says “do not copy that”; implementing TX/modem semantics leaves RX writes u...
3. `seatcopywait` | LOW | 18376-18405 | copy preserved seat logs after the panel wait | 18376–18405 | ID-LESS: yes | OPEN: YES: the owed change, copy the preserved logs after the launcher `wait`, is absent from `tools/panel.sh`; that script already `wait`s at `tools/panel.sh:435` and writes `PANEL_COMPLETE` at `tools/panel.sh:794` (both from 2026-08-17, before this 2026-09-08 note), and no other `tools/*.sh` copies seat logs after that wait | DISPOSITION: NEW LOW seatcopywait "copy preserved seat log...
4. `armcpabsent` | MED | 18709-18713 | MRC or MCR to an uninstalled ARM coprocessor fatals and falls through, with Undefined Instruction delivery still commented out; CDP already delivers Undefined Instruction | 18709–18713 | grok said FILED `xscaleinten` | should be NEW MED `armcpabsent` | `OUTSTANDING_BUGS.md:18674–18683` defines `xscaleinten` as the installed CP6 inten-read exit, repaired at `src/cpus/cpu_arm_coproc.c:310–314`. The separate missing-coprocessor branch still omits Undefined Instruction delivery at `src/cpus/cpu_arm.c:2656–2662`. Placement beneath the heading does not give this different defect that ID. |...
5. `panelechocheck` | LOW | 19498-19502 | ECHO-ONLY requires both the distinctive brief line in the answer and answer-minus-brief under 800; the owed work is a harness change plus two negative controls | 19498–19502 | grok said FILED `xscaleinten` | should be NEW LOW `panelechocheck` | `tools/panel.sh:487–493` retains the false ECHO-ONLY heuristic; `OUTSTANDING_BUGS.md:19501–19502` explicitly owes a harness change and two controls. Disk `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md:641` identifies this exact defect as **FILED-BY-PROSE**, without an ID. It is unrelated to the shipped inten ...
6. `shfaultclause` | LOW | 19540-19542 | Owed record correction, deferred to carrier review and still owed: the member-5 clause omits that a failed SH load leaves its destination unchanged. | 19540–19542 | grok said KEEP-AS-IS, correction “not owed by this row” | should be NEW LOW `shfaultclause` | `regress/artifacts/mapledmaaddr/fable_pass1_20260912.md:11` explicitly says the carrier “now owes” the SH qualification. `OUTSTANDING_BUGS.md:19540–19542` defers its delivery to the carrier-review round; it does not withdraw it. `tools/CLAUDE.md:1904–1908` still lacks the correction, and `src/cpus/cpu_sh_ins...
7. `qhppcdecode` | HIGH | 1705-1716 | Ten PowerPC floating-point encodings still stop emulation: fctid, fctidz, fcfid, fcmpo, fmadds, fmsubs, fsqrt, fsqrts, fres and frsqrte | (ruled later: grok/grok_icompound.txt (a compound disposition: the table's derivation had dropped this row) -- read that file under the directory named above)
8. `qhm88kstops` | HIGH | 2616 | An MB89352 data-register read with no transfer object stops the emulated CPU | (ruled later: grok/grok_icompound.txt (a compound disposition: the table's derivation had dropped this row) -- read that file under the directory named above)
9. `qhmipstlbwarn` | LOW | 2597-2599 | The optional write-time MIPS TLB-overlap debug warning remains compiled out and was left unimplemented; it is tooling, not a fidelity defect | (ruled later: grok/grok_irule_a.txt B1 (conceding Astra's ifile_01 finding) -- read that file under the directory named above)
10. `armcpsrprint` | LOW | 16972-16975 | A direct debugger print of cpsr can show stale NZCV because the settings read does not fold the separate execution-flags field back into CPSR | (ruled later: grok/grok_irule_a.txt B2 (conceding Astra's ifile_01 finding) -- read that file under the directory named above)
11. `heartirqdelivery` | MED | 20873-20878 | IP30 HEART timer and ISR interrupts are not delivered and the Octane machine wiring is still the unimplemented interrupt TODO, separate from the repaired host-abort fix | (ruled later: grok/grok_irule_a.txt B3 (conceding Astra's ifile_01 finding) -- read that file under the directory named above)
12. `pcc2lineexit` | LOW | 13932-13934 | pcctwo_interrupt_common's default still calls exit on an unsupported interrupt line, and guest reachability is unestablished | (ruled later: grok/grok_irule_b.txt S5 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
13. `ppcenabldeliv` | MED | 1685-1697 | FPSCR enable bits set FEX and never deliver a program exception | (ruled later: grok/grok_irule_b.txt F2 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
14. `armv6cachefmt` | MED | 2097-2109; 1977-1979 | ARMv6 cache-type register format is not the v4/v5 layout hardcoded for every CPU | (ruled later: grok/grok_irule_b.txt F7 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
15. `qharmvsixunal` | MED | 3617-3618 | ARMv6 U=1 word loads still mask and rotate; ARM_CONTROL_U is undefined | (ruled later: grok/grok_irule_b.txt F10 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
16. `armsa1110areset` | MED | 4139-4145 | ARM reset ORs ARM_CONTROL_ALIGN, contradicting the SA-1110 reset state | (ruled later: grok/grok_irule_b.txt F11 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
17. `qhshelltimeout` | LOW | 5262-5266 | gate scripts still bound emulator runs with the timeout command | (ruled later: grok/grok_irule_b.txt F14 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
18. `qhguestasan` | LOW | 7326-7338 | the asan sweep constructs machines under -V and never executes a guest instruction | (ruled later: grok/grok_irule_b.txt F15 (a remainder Astra's ifile_02 found unfiled) -- read that file under the directory named above)
19. `gdromtailcov` | LOW | 10412-10418 | ship cnt-post tail-reach rows for both GD-ROM rejection arms | (ruled later: grok/grok_grok_irule_d.txt 4 (conceding; Astra's ifile_04 raised it) -- read that file under the directory named above)
20. `closeassessrows` | MED | 6082-6086; 6097-6099; 6101-6140; 5607-5615 | the 2026-08-27 sweep closed CLOSE (assess) rows that still name undone work, and each member needs a re-open decision | (ruled later: grok/grok_grok_irule_d.txt 5 (conceding in part; Astra's ifile_04 raised it) -- read that file under the directory named above)
