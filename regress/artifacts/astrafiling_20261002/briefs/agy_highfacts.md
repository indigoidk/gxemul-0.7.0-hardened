THE FACTS UNDER 22 DISPUTED ROWS -- a read-only check by the agy seat

Open your answer with the token AGY_HIGHFACTS_ALIVE_1002 on its own line.  SECOND line, exactly in this form:
VERDICT: <a> rows where the check still fails on a real emulator death, <b> where the protected path no longer ends the process, <c> not settled by reading, of 22 rows

You are one seat of a review panel for a C emulator fork (GXemul, hardened).  READ-ONLY, always: write no file, run
nothing, build nothing, change nothing anywhere.  Your only output is the text you print.

CONTEXT.  A review of this project's REGRESSION HARNESS (its gate scripts, probes and checkers) produced a table of
test-coverage defects.  22 of its rows are graded HIGH and two seats disagree about that grade.  The grade turns on
FACTS about the committed source, and those facts are what you are asked for -- NOT a grade.  Your agreement with either
seat carries no weight; a fact you cite with a file and line does.

THE TREE.  C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC (git).  Read the COMMITTED files at 7440e129 only
(git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show 7440e129:<path>, with grep -n or awk for line numbers).  Never read
C:\DocumentNoSnc\cc\GXEMUL\src, est, build, build-asan or _archive: they are other copies and their line numbers
differ by hundreds.  Never run git status or git diff.  The table is
C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING.tsv (tab-separated; column 6 is
the row id, column 8 the governing text, which names the files and lines of each finding).

FOR EACH OF THE 22 ROWS BELOW answer three questions from the committed source, each with path:line:
 Q1  THE CHECK: when the emulator child process really dies (killed by a signal, or exit status 1) at the point this
     row is about, does the row / check FAIL, or can it still PASS?  Say which lines decide it.
 Q2  THE PROTECTED PATH: the defect this check was written to catch -- does that path in src/ STILL end the emulator
     process today (exit(), abort, cpu->running = 0 with the process stopping), or does it now decline, latch a
     message, or raise a guest exception and carry on?  Name the lines in src/.
 Q3  THE SHAPE: for rows about a parser or a census (a check that mis-reads some command line, heredoc or argument
     shape), does ANY live instance of the mis-read shape exist in the committed gate scripts today?  Name it, or say
     none was found and what you searched.
One block per row:
<row id> | Q1: FAILS / CAN PASS -- <lines> | Q2: STILL ENDS THE PROCESS / NO LONGER -- <lines> | Q3: LIVE INSTANCE <where> / NONE FOUND <what was searched> / N/A
If a question cannot be settled by reading, write UNSETTLED and name what would settle it.  Do not guess.

THE 22 ROWS (the title, then the grok seat's reason for calling the row not HIGH -- check its facts, do not adopt them):
vgadirtyarm  [retro, batch 2d -]
    the row's title: VGA: an untracked charcells write below the CRTC start leaves a ~-1.7e9 dirty-row origin unclipped, and the graphics redraw walks it
    grok: NOT TRUE: the untracked charcells path leaves a small negative dirty-row origin, and the graphics redraw is clipped on the dyntrans path; the pixel reads stay in range | src/devices/dev_vga.c:413, src/devices/dev_vga.c:429, src/devices/dev_vga.c:555, src/devices/dev_vga.c:599, src/devices/dev_vga.c:741
asanemptyalias  [harness, group 03 hbundle_regress10:F3]
    the row's title: alias-less help line is neither parsed nor unparsed
    grok: NOT HIGH: a zero-alias help line is neither parsed nor unparsed, and no alias-less machine on this path exits; vocore registers an alias | regress/gate_asan_sweep.sh:245-261, src/machines/machine.c:909-912, src/machines/machine_vocore.c:89-93
sgilwreadzero  [harness, group 03 hbundle_regress11:F1]
    the row's title: narrow read of a zeroed window looks like the width decline
    grok: NOT HIGH: the narrow read declines before the linear index; an 8-byte-aligned [tlbi+1] stays inside the [32] arrays | regress/sgi_re_width_probe.py:338-341, src/devices/dev_sgi_re.c:179-180, src/devices/dev_sgi_re.c:731-733, src/devices/dev_sgi_re.c:810-812
hpchenumrc  [harness, group 03 hbundle_regress13:F4]
    the row's title: subtype census ignores a failing -H status
    grok: NOT HIGH: -H's return code is unread, but the default symptom row still requires a measured construction abort, and a completed -H still lists those subtypes | regress/hpcabort_witness.py:197-214, regress/hpcabort_witness.py:558-568
mipsrihang  [harness, group 06 regress21:F3]
    the row's title: RI classification returns before a missing PC
    grok: NOT HIGH: the classifier does return RI before a missing PC, and the #309 guest path now raises a reserved-instruction exception with the CPU left running | regress/mips_subnorm_probe.py:227-234, src/cpus/cpu_mips_instr.c:5398-5410, src/core/emul.c:1052-1059, src/core/main.c:807-821
swpctxnoop  [harness, group 06 regress23:F2]
    the row's title: swpctx rows pass when the handler never saves
    grok: NOT HIGH: a handler that never saves leaves the planted PTBR and the ptbr row passes, and the live clobber writes the flags word and fails that row | regress/alpha_harness_probe.py:322-330, OUTSTANDING_BUGS.md:16090-16097
palgateabsent  [harness, group 06 regress23:F3]
    the row's title: palgate passes when the transcript has no user-mode text
    grok: NOT HIGH: an empty transcript is scored gated-absent, and the user-mode PALcode rejection prints "user mode" before it clears cpu->running | regress/alpha_harness_probe.py:215-218, src/cpus/cpu_alpha_palcode.c:183-190
diagdivunaryop  [harness, group 09 hbundle_regress33:F8]
    the row's title: diag_div_sweep divisor regex rejects unary operators and pointer dereference
    grok: NOT HIGH: the divisor regex drops a unary or a dereference, and no dropped CALLS-argument guest-zero division still raises SIGFPE | regress/diag_div_sweep.py:76, regress/diag_div_sweep.py:89
diagdivchained  [harness, group 09 hbundle_regress33:F9]
    the row's title: diag_div_sweep nonconst classifies chained division with leading constant divisor as constant
    grok: NOT HIGH: a chained division whose first divisor is constant is classed constant, and that miss is not a live guest-zero SIGFPE in a CALLS argument | regress/diag_div_sweep.py:104-113
diagdivtruncarg  [harness, group 09 hbundle_regress33:F10]
    the row's title: diag_div_sweep truncates arguments to 150 characters before nonconst classification
    grok: NOT HIGH: the argument is cut to 150 characters before classification, and no guest-zero SIGFPE sits past that cut in a CALLS argument | regress/diag_div_sweep.py:99, regress/diag_div_sweep.py:112-113
sh4c7fetch  [harness, group 10 hbundle_regress7:F1]
    the row's title: C7's user-mode P1 fetch never issues the P4 access it claims to bound
    grok: NOT HIGH: C7 plants a P1 instruction with a P4 data address and user SR, and the translator returns before any P4 device access; W1 still scores the privileged exit | regress/sh4pcic_witness.py:429-470, src/cpus/memory_sh.c:359-370, src/devices/dev_sh4.c:964
sh4hangoracle  [harness, group 10 hbundle_regress7:F2]
    the row's title: sh4pcic killed() scores a hang that printed the diagnostic as the guest exit
    grok: NOT HIGH: killed() treats a needle plus an unanswered dump as the kill, and a process that actually exits with that needle still matches | regress/sh4pcic_witness.py:239-244, regress/sh4pcic_witness.py:306-314
shhaltsilent  [harness, group 10 hbundle_regress8:F3]
    the row's title: five sh_halt survival rows accept an open pty that never dumps
    grok: NOT HIGH: the survival rows accept only "alive", and the odd-register FNEG/FABS paths now raise a guest exception and return | regress/sh_halt_probe.py:318-322, regress/sh_halt_probe.py:629-639, src/cpus/cpu_sh_instr.c:3201-3213, src/cpus/cpu_sh_instr.c:3229-3238
sgiat1count  [harness, group 10 hbundle_regress9:F1]
    the row's title: sgi wr lat1 and rd lat1 pass when the second access exits
    grok: NOT HIGH: wr lat1 and rd lat1 compare a message count and ignore liveness, and the live unmapped arms latch a fatal() that does not exit and then return | regress/sgi_re_unmapped_probe.py:591-598, src/devices/dev_sgi_re.c:816-836, src/core/debugmsg.c:384-391
probewiringinterpopt  [harness, group 11 hcheckprobewiring:F2]
    the row's title: check_probe_wiring.py ignores interpreter options preceding -c false-wiring probes passed as arguments
    grok: NOT HIGH: only the first token after the interpreter is tested for -c, so an option before -c can credit a later .py argument, and arm_flags_probe.py is really invoked as a script | tools/pipeline/check_probe_wiring.py:3200-3205, regress/gate_arm.sh:97, src/cpus/cpu_dyntrans.c:2014
probewiringvarmap  [harness, group 11 hcheckprobewiring:F3]
    the row's title: check_probe_wiring.py variable map ignores non-py assignments and ignores assignment order
    grok: NOT HIGH: the map keeps only assignments whose right-hand side contains .py and is built before any use, and the BSC probe's assignment is a .py path that the gate really runs | tools/pipeline/check_probe_wiring.py:3165-3171, tools/pipeline/check_probe_wiring.py:3208-3210, regress/gate_sh_rounding.sh:1326-1331
probewiringheredocstrip  [harness, group 11 hcheckprobewiring:F4]
    the row's title: check_probe_wiring.py heredoc strip treats indented terminator as end of heredoc false-wiring body lines
    grok: NOT HIGH: strip() ends a heredoc on a space-indented terminator word, and no live heredoc in the battery carries an interpreter plus a probe in its body | tools/pipeline/check_probe_wiring.py:3176-3195
fbforkstatus  [harness, group 12 hdifffootbridge:F1]
    the row's title: diff_footbridge F1/G1 ignore fork/waitpid failure, laundering st=0 into survived
    grok: NOT HIGH: fork failure and an unchecked waitpid leave st at 0 and score survived, and a reaped signal or exit(1) fails the survived check | regress/diff_footbridge.c:389-406, regress/diff_footbridge.c:418-434
m88forkprobe  [harness, group 12 hdiffm8820x:F2]
    the row's title: diff_m8820x probe ignores fork/waitpid errors, laundering failure to survived
    grok: NOT HIGH: fork failure and an unchecked waitpid return 0, and a reaped exit(1) returns 1 and a signal returns 2, both of which fail a row | regress/diff_m8820x.c:267-282, regress/diff_m8820x.c:470-481
wdcnullstatus  [harness, group 13 hdiffwdcidentify:F1]
    the row's title: row_null_atapi_st ignores non-zero child exit status and waitpid failure
    grok: NOT HIGH: a nonsignalled nonzero exit and a failed waitpid print ok, and the NULL atapi_st read is now a latched fatal() that does not exit; a signal still fails the row | regress/diff_wdc_identify.c:1590-1600, src/devices/dev_wdc.c:1312-1317, src/core/debugmsg.c:384-391
hpcenumstatus  [harness, group 15 hhpcmipsctorprobe:F2]
    the row's title: enumerate_subtypes discards _run exit status allowing partial -H output
    grok: NOT HIGH: enumerate_subtypes discards the -H status, and a successful -H still lists the aborting subtypes, which A3 then fails | regress/hpcmips_ctor_probe.py:213-227, regress/hpcmips_ctor_probe.py:448-454, regress/hpcmips_ctor_probe.py:480-482
sgideprimbitslive  [harness, group 17 hsgideprimopprobe:F2]
    the row's title: dec b26-b31 and n25 line ignore liveness and exit status
    grok: NOT HIGH: the dec b26-b31 and n25 line rows compare message counts and drop alive and how; those decline paths are latched messages, and fatal() does not exit | regress/sgi_de_primop_probe.py:280-298, regress/sgi_de_primop_probe.py:345-354, regress/sgi_de_primop_probe.py:916-932, regress/sgi_de_primop_probe.py:1379-1384, src/core/debugmsg.c:384-391

LAST LINE: DENOMINATOR: opened the source for <n> of 22 rows; <m> questions answered UNSETTLED
