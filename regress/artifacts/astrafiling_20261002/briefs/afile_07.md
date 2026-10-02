THE HIGH ROWS -- the grok seat's first-hand re-read disputes 22 of them: concede or hold, row by row

Open with the token `ASTRAFILE_07_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <c> conceded, <h> held, of 22 disputed HIGH rows; <t> of 6 conditions accepted into the title`

**Context.**  The filing table of the Astra review campaign carries 57 rows graded HIGH
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING.tsv` with
`FILING_OVERLAY.tsv`).  A row graded HIGH gets a correction round, so the grok seat -- a different model family -- was
asked to re-read all 57 against the COMMITTED SOURCE at `7440e129`, first-hand
(`...\astrafiling_20261002\grok\grok_filehigh.txt`): "29 of 57 HIGH rows true as titled, 6 true only under a condition the title omits, 22 not HIGH or not true.".  21 of its 22 disputed rows are in the HARNESS wave, and
16 of the harness HIGH grades are ones YOU raised in your confirmations.  A raise by the family that wrote the finding
is not adopted over an independent seat's first-hand reading on its say-so -- and a reading in your own favour is the
one you are least likely to test -- so each disputed row comes back to you with grok's reason verbatim.  Nothing is
filed HIGH on a disputed row until this is answered.

**The rule in dispute, stated so that you can apply it uniformly.**  A harness defect is graded by WHAT THE CHECK WOULD
MISS: HIGH if the defect the check was shipped to catch ends the emulator process or makes a memory access leave a
buffer's bounds.  grok's reasons fall into three shapes; say, in ONE sentence each, whether the shape leaves the row
HIGH, and then apply those three sentences to every row:
 (i)   the check's blind spot is a HARNESS-side failure (fork or waitpid failing, a status of a helper run), while a
       real emulator death -- a signal, exit(1) -- STILL fails the row;
 (ii)  the protected defect is FIXED at `7440e129` (the path now declines, latches a message or raises a guest
       exception), so nothing live ends the process, and the check would miss only a re-introduction;
 (iii) the blind spot has no live instance in the battery (no command line, heredoc or call argument of the shape the
       check mis-parses exists today).

**The 22 disputed rows, grok's lines verbatim:**
vgadirtyarm | NOT TRUE: the untracked charcells path leaves a small negative dirty-row origin, and the graphics redraw is clipped on the dyntrans path; the pixel reads stay in range | src/devices/dev_vga.c:413, src/devices/dev_vga.c:429, src/devices/dev_vga.c:555, src/devices/dev_vga.c:599, src/devices/dev_vga.c:741
asanemptyalias | NOT HIGH: a zero-alias help line is neither parsed nor unparsed, and no alias-less machine on this path exits; vocore registers an alias | regress/gate_asan_sweep.sh:245-261, src/machines/machine.c:909-912, src/machines/machine_vocore.c:89-93
sgilwreadzero | NOT HIGH: the narrow read declines before the linear index; an 8-byte-aligned [tlbi+1] stays inside the [32] arrays | regress/sgi_re_width_probe.py:338-341, src/devices/dev_sgi_re.c:179-180, src/devices/dev_sgi_re.c:731-733, src/devices/dev_sgi_re.c:810-812
hpchenumrc | NOT HIGH: -H's return code is unread, but the default symptom row still requires a measured construction abort, and a completed -H still lists those subtypes | regress/hpcabort_witness.py:197-214, regress/hpcabort_witness.py:558-568
mipsrihang | NOT HIGH: the classifier does return RI before a missing PC, and the #309 guest path now raises a reserved-instruction exception with the CPU left running | regress/mips_subnorm_probe.py:227-234, src/cpus/cpu_mips_instr.c:5398-5410, src/core/emul.c:1052-1059, src/core/main.c:807-821
swpctxnoop | NOT HIGH: a handler that never saves leaves the planted PTBR and the ptbr row passes, and the live clobber writes the flags word and fails that row | regress/alpha_harness_probe.py:322-330, OUTSTANDING_BUGS.md:16090-16097
palgateabsent | NOT HIGH: an empty transcript is scored gated-absent, and the user-mode PALcode rejection prints "user mode" before it clears cpu->running | regress/alpha_harness_probe.py:215-218, src/cpus/cpu_alpha_palcode.c:183-190
diagdivunaryop | NOT HIGH: the divisor regex drops a unary or a dereference, and no dropped CALLS-argument guest-zero division still raises SIGFPE | regress/diag_div_sweep.py:76, regress/diag_div_sweep.py:89
diagdivchained | NOT HIGH: a chained division whose first divisor is constant is classed constant, and that miss is not a live guest-zero SIGFPE in a CALLS argument | regress/diag_div_sweep.py:104-113
diagdivtruncarg | NOT HIGH: the argument is cut to 150 characters before classification, and no guest-zero SIGFPE sits past that cut in a CALLS argument | regress/diag_div_sweep.py:99, regress/diag_div_sweep.py:112-113
sh4c7fetch | NOT HIGH: C7 plants a P1 instruction with a P4 data address and user SR, and the translator returns before any P4 device access; W1 still scores the privileged exit | regress/sh4pcic_witness.py:429-470, src/cpus/memory_sh.c:359-370, src/devices/dev_sh4.c:964
sh4hangoracle | NOT HIGH: killed() treats a needle plus an unanswered dump as the kill, and a process that actually exits with that needle still matches | regress/sh4pcic_witness.py:239-244, regress/sh4pcic_witness.py:306-314
shhaltsilent | NOT HIGH: the survival rows accept only "alive", and the odd-register FNEG/FABS paths now raise a guest exception and return | regress/sh_halt_probe.py:318-322, regress/sh_halt_probe.py:629-639, src/cpus/cpu_sh_instr.c:3201-3213, src/cpus/cpu_sh_instr.c:3229-3238
sgiat1count | NOT HIGH: wr lat1 and rd lat1 compare a message count and ignore liveness, and the live unmapped arms latch a fatal() that does not exit and then return | regress/sgi_re_unmapped_probe.py:591-598, src/devices/dev_sgi_re.c:816-836, src/core/debugmsg.c:384-391
probewiringinterpopt | NOT HIGH: only the first token after the interpreter is tested for -c, so an option before -c can credit a later .py argument, and arm_flags_probe.py is really invoked as a script | tools/pipeline/check_probe_wiring.py:3200-3205, regress/gate_arm.sh:97, src/cpus/cpu_dyntrans.c:2014
probewiringvarmap | NOT HIGH: the map keeps only assignments whose right-hand side contains .py and is built before any use, and the BSC probe's assignment is a .py path that the gate really runs | tools/pipeline/check_probe_wiring.py:3165-3171, tools/pipeline/check_probe_wiring.py:3208-3210, regress/gate_sh_rounding.sh:1326-1331
probewiringheredocstrip | NOT HIGH: strip() ends a heredoc on a space-indented terminator word, and no live heredoc in the battery carries an interpreter plus a probe in its body | tools/pipeline/check_probe_wiring.py:3176-3195
fbforkstatus | NOT HIGH: fork failure and an unchecked waitpid leave st at 0 and score survived, and a reaped signal or exit(1) fails the survived check | regress/diff_footbridge.c:389-406, regress/diff_footbridge.c:418-434
m88forkprobe | NOT HIGH: fork failure and an unchecked waitpid return 0, and a reaped exit(1) returns 1 and a signal returns 2, both of which fail a row | regress/diff_m8820x.c:267-282, regress/diff_m8820x.c:470-481
wdcnullstatus | NOT HIGH: a nonsignalled nonzero exit and a failed waitpid print ok, and the NULL atapi_st read is now a latched fatal() that does not exit; a signal still fails the row | regress/diff_wdc_identify.c:1590-1600, src/devices/dev_wdc.c:1312-1317, src/core/debugmsg.c:384-391
hpcenumstatus | NOT HIGH: enumerate_subtypes discards the -H status, and a successful -H still lists the aborting subtypes, which A3 then fails | regress/hpcmips_ctor_probe.py:213-227, regress/hpcmips_ctor_probe.py:448-454, regress/hpcmips_ctor_probe.py:480-482
sgideprimbitslive | NOT HIGH: the dec b26-b31 and n25 line rows compare message counts and drop alive and how; those decline paths are latched messages, and fatal() does not exit | regress/sgi_de_primop_probe.py:280-298, regress/sgi_de_primop_probe.py:345-354, regress/sgi_de_primop_probe.py:916-932, regress/sgi_de_primop_probe.py:1379-1384, src/core/debugmsg.c:384-391

**The 6 rows grok calls TRUE ONLY UNDER A CONDITION the title omits (its lines verbatim).**  For each: is the condition
right, and should the title carry it?
ne2krxbudget | CONDITIONAL: reception stays enabled, the ring stays invalid so OVW is never set, and ingress keeps arriving; a finite burst drains | src/devices/dev_ne2000.c:333-341, src/devices/dev_ne2000.c:450-452, src/net/net.c:302-330
taprxquota | CONDITIONAL: the TAP read() keeps returning a nonnegative count | src/net/net_tap.c:104-120, src/net/net.c:293-295
dyncacheoffset32 | CONDITIONAL: a 64-bit host and a configured cache large enough that translation_cache_cur_ofs crosses 2^32 before the uint32_t physpage_ofs store | src/cpus/cpu_dyntrans.c:630, src/cpus/cpu_dyntrans.c:797-798, src/cpus/cpu_dyntrans.c:803-804, src/cpus/cpu_dyntrans.c:830-833, src/include/cpu.h:472
gdromdmareentr | CONDITIONAL: the staged DMA word is nonzero, with count and enable already 1, d->data non-NULL, and the destination aimed at the window's +0x18 | src/devices/dev_dreamcast_gdrom.c:1373, src/devices/dev_dreamcast_gdrom.c:1389-1391, src/devices/dev_dreamcast_gdrom.c:1501-1503, src/core/memory.c:65-75
ascwidecount | CONDITIONAL: data_out_offset and dma_off are each at least the magnitude of the negative len2, so both size_t guards wrap; a large-magnitude negative such as INT_MIN is still clamped | src/devices/dev_asc.c:577-578, src/devices/dev_asc.c:610-621, src/devices/dev_asc.c:662-665, src/include/diskimage.h:188-189, src/include/thirdparty/ncr53c9xreg.h:39
m88kbcndnest | CONDITIONAL: the dispatch-pointer walk off ics[] is the untaken path and only from an entry already near the end of that page's ic array; the nested delay-slot call through ic[1].f is unbounded | src/cpus/tmp_m88k_bcnd.c:320, src/cpus/tmp_m88k_bcnd.c:328, src/include/cpu.h:81

**Two further points from the same answer:**
(a) optpinor and optpinanyfno are one defect: the pin in tools/pipeline/check_optpin.py no longer keeps the memory_rw recursive split from exhausting the host stack (regress/diff_memory_rw.c:93-98). The lane-OR at check_optpin.py:93 and the any-`-fno-` match at :52 are the two accepts.
(b) wdcnullstatus — the NULL-transfer host kill is already `wdcnullxfer` at OUTSTANDING_BUGS.md:11864. The live arm declines at src/devices/dev_wdc.c:1312-1317, and the row still fails a signal at regress/diff_wdc_identify.c:1594-1597.

**One the main loop checked itself** -- `vgadirtyarm` (retro batch 2d; you confirmed it with a wording amendment).  The
ruling says an untracked charcells write below the CRTC start "leaves a ~-1.7e9 dirty-row origin unclipped and the
graphics redraw walks it for hours".  `src/devices/dev_vga.c:732` declares `int x, y, x2, y2, r, base;` and `:740` is
`r = relative_addr - base;` with `base` at most 0xffff * 2, so `r` is a SMALL negative and `y = r / (d->max_x * 2)` is
at least about -820, not -1.7e9; `:555-558` clips only inside the dyntrans-access branch.  Is the stated consequence
wrong, what defect (if any) remains with a row index of that size in `vga_update_graphics()` (`:346-380`) and
`vga_update_text()` (`:409-431`), and what is its grade?

**Answer format.**  For each of the 22: `<id> | CONCEDE <MED or LOW> | HOLD HIGH` then one line of evidence
(`path:line` at `7440e129`: `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`) and which of your three
sentences decided it.  For each of the 6: `<id> | ACCEPT the condition | REJECT: <why>`.  For the two further points
and `vgadirtyarm`: one line each.  Mark what a reading cannot settle as UNSETTLED and name the measurement.
End with `DENOMINATOR: opened the source for <n> of 22 disputed rows and <m> of 6 conditional rows`.
Read-only: write nothing, build nothing, run nothing that changes a file.
