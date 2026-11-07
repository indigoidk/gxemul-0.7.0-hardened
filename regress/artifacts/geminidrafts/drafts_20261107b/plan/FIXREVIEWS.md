# Gemini second-lens reviews of the compiled fix drafts -- 123 rows, oldest first

Same model as the drafter (badge `s`): POINTERS for the Fable/Mythos adjudication, not verdicts.  Each packet carried the
row, the draft's APPLIED.diff and every edited function in full (mk_fixreview.py).  Tally: DEFECT 34, SOUND 72, UNSETTLED 5, WITHDRAWN DEFECT 12

### `b120` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pit8253lsbnotimer` -- DEFECT, 2 finding(s)

* (no file:line finding line)

### `pit8253flood` -- DEFECT, 4 finding(s)

* src/devices/dev_8253.c:204 DEFECT The check reuses the emulator's functional state and misses `(once)` in the string. Fix: `default: if (!d->warn_write[relative_addr]++) { fatal("[ 8253: huh? writing to counter %i but neither from msb nor lsb? (once) ]\n", (in
* src/devices/dev_8253.c:272 DEFECT The check reuses the emulator's functional state and misses `(once)` in the string. Fix: `default: if (!d->warn_read[relative_addr]++) { fatal("[ 8253: huh? reading from counter %i but neither from msb nor lsb? (once) ]\n", (i
* src/devices/dev_8253.c:346 DEFECT The check reuses the emulator's functional state and misses `(once)` in the string. Fix: `if (!d->warn_bcd[d->counter_select]++) { fatal("[ 8253: BCD not yet implemented (once) ]\n"); }`
* src/devices/dev_8253.c:200 STYLE The newly added comment line exceeds 79 columns. Fix: break the comment into multiple lines.

### `gdromcondavail` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `armdacr2kill` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `armdesc3kill` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `fbsignalcoverage` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/core/timer.c:281`: DEFECT - The diff merely adds a comment stating it enforces a minimum serviced count, but fails to implement any logic to do so and entirely ignores the second site at lines 327-337. Fix: Implement the actual logic to guarantee the mini

### `pvrdirtyregion` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `sgialiaspace` -- DEFECT, 1 finding(s)

* `src/machines/machine.c:212` QUESTION/DEFECT Fix the root cause in `machine_sgi.c` or `gate_ab.sh` as named in the issue.

### `heldrecedits` -- DEFECT, 1 finding(s)

* (no file:line finding line)

### `armmmufaultlog` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `cpunewstores` -- UNSETTLED, 3 finding(s)

* 2. `cpu_alpha.c:101` (and `cpu_arm.c:187`, `cpu_mips.c:303`): STYLE. The comment exceeds the 79-column limit. Fix: wrap the comment to multiple lines.

### `cpurunningtype` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `dc7085cts` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `i8259icw4` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `i8259isrnever` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* (no file:line finding line)

### `ioasic3minscc` -- DEFECT, 5 finding(s)

* `src/devices/dev_dec_ioasic.c:180`, QUESTION, The guest OS runtime behavior (Ultrix 4.5 issue resolution) is UNSETTLED without runtime testing. Fix: run the OS and verify console output.
* `src/devices/dev_dec_ioasic.c:191`, QUESTION, removed an early `break` ensuring control flow correctly reaches RX DMA and common tail. Fix: none needed.
* `src/devices/dev_dec_ioasic.c:420`, QUESTION, function still returns 1 to the caller. Fix: none needed.
* `src/devices/dev_dec_ioasic.c:192`, QUESTION, removes `fatal()` crash, but completely silences the unhandled DMA condition instead of converting it to a `(once)` diagnostic. Fix: add a rate-limited `debug(once)` warning.
* `src/devices/dev_dec_ioasic.c:223`, STYLE, line exceeds 79 columns due to deep indentation. Fix: refactor indentation or wrap line.

### `ioasicesar` -- SOUND, 2 finding(s)

* src/devices/dev_dec_ioasic.c:416 STYLE break the calculation across two lines to stay under 79 columns
* src/devices/dev_dec_ioasic.c:417 STYLE break the array initialization across two lines to stay under 79 columns

### `leloopback` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* src/devices/dev_le.c:74: DEFECT: Site named in the issue is missing from the patch. UNSETTLED: The file `src/devices/dev_le.c` (around line 74) is missing, so a fix cannot be proposed.

### `lermd3fcs` -- SOUND, 1 finding(s)

* src/devices/dev_le.c:574: STYLE: line exceeds 79 columns; break the line after `>=`

### `lesarom` -- DEFECT, 2 finding(s)

* src/devices/dev_le.c:982: STYLE - Guest-triggerable diagnostic lacks a latch. Fix: `if (!d->rom_warn) { d->rom_warn = 1; debugmsg(... "(once) ..."); }`

### `m88kcarryundec` -- DEFECT, 2 finding(s)

* src/cpus/cpu_dyntrans.c:2014: DEFECT, Apply the equivalent opcode cases and mappings to cpu_dyntrans.c.
* src/cpus/cpu_m88k_instr.c:3815: DEFECT, Apply the necessary missing fix for the site at 3815.

### `m88koutsideram` -- DEFECT, 4 finding(s)

* src/core/memory.c:598, DEFECT, Apply the corresponding out-of-bounds RAM fix to src/core/memory.c.
* src/cpus/memory_rw.c:696, DEFECT, Restore the `if` condition around `memory_warn_about_unimplemented_addr()` so its return value is not ignored.
* src/cpus/memory_rw.c:715, DEFECT, Move the `return MEMORY_ACCESS_FAILED;` inside the `#ifdef MEM_M88K` block so other architectures can fall through to the zero-read fallback.
* src/cpus/memory_rw.c:699, STYLE, Wrap the comment to fit within the 79-column limit.

### `m88kpsrreserved` -- DEFECT, 1 finding(s)

* src/cpus/cpu_m88k_instr.c:2249, DEFECT, patch `src/cpus/cpu_m88k_instr.c` to apply the same `0xf000000f` / `0x0ffffff0` mask to EPSR/PSR.

### `m88kzeroword` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mb89352bfint` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mb89352psns` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mb89352scmd` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/devices/dev_mb89352.c:527`: DEFECT: Missed site from the issue report. Fix: UNSETTLED (lines 470-672 are omitted from the text, so the exact required fix cannot be provided).

### `mc146818reg63` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* src/devices/dev_mc146818.c:529 DEFECT The diff misses the third site named in the issue (line 529). Fix: remove the overwriting of register 63 at line 529 as well.

### `mc146818uie` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mipscop0cpu` -- DEFECT, 4 finding(s)

* `src/cpus/cpu_mips_instr.c:4939` DEFECT: Replaces wrong exception with host halt (`goto bad;`) instead of checking CU0.
* `src/cpus/cpu_mips_instr.c:4939` DEFECT: `goto bad;` skips the common tail at `cpu_dyntrans.c`.
* `src/cpus/cpu_mips_instr.c:4932` STYLE: Uses static latch `warned` rather than a device latch, and missing `(once)` in the string.

### `mipscountidle` -- SOUND, 1 finding(s)

* `src/cpus/cpu_dyntrans.c:377` STYLE - Line exceeds 79 columns. Fix: `/* #mipscountidle: do not subtract */` (or split across two lines).

### `mipscountrate` -- DEFECT, 3 finding(s)

* `src/cpus/cpu_dyntrans.c:427`, DEFECT, implement and use a per-machine divisor (e.g., `cpu->machine->count_divisor`) instead of a hardcoded 2.
* `src/cpus/cpu_dyntrans.c:427`, STYLE, wrap the expression to fit within 79 columns.
* `src/cpus/cpu_dyntrans.c:425`, STYLE, replace `#NNN` with `#mipscountrate`.

### `mipscountread` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mipsdivwrap` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mipssubpageram` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mk48clock` -- DEFECT, 1 finding(s)

* src/devices/dev_mk48txx.c:87, STYLE, wrap the line before `& MK48TXX_CSR_READ` to stay within 79 columns.

### `mk48multibyte` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `natconnfail` -- DEFECT, 1 finding(s)

* src/net/net_ip.c:1520 DEFECT The patch fails to address `net_tcp_rx_avail` named in the issue ledger. Fix: Port the missing `connect` failure handling to `net_tcp_rx_avail`.

### `natdhcpreply` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `osiopcalltemp` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `osiopdmainval` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pccmosnmi` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pcicfgaddrlow` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pckbcauxecho` -- UNSETTLED, 1 finding(s)

* `src/devices/dev_pckbc.c:743` QUESTION: UNSETTLED - we need the rest of `dev_pckbc_command` after line 743 to ensure 0xD3 does not erroneously get parsed as a mouse command. Fix: Provide lines 744-800 of `dev_pckbc_command`.

### `pckbcgetid` -- SOUND, 1 finding(s)

* `src/devices/dev_pckbc.c:856` STYLE Break the `pckbc_add_code` arguments onto a new line to stay within 79 columns.

### `pckbcledparam` -- SOUND, 1 finding(s)

* src/devices/dev_pckbc.c:776: STYLE: Replace magic number 1000 with a descriptive constant like STATE_WAITING_FOR_LED_PARAM.

### `pckbcselftest` -- DEFECT, 2 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/devices/dev_pckbc.c:883`: DEFECT: The keyboard 0xFF self-test is missing from the diff; apply flush logic to that site as well.
* `src/devices/dev_pckbc.c:1057`: QUESTION: The 0xA9 case removed the debug statement instead of preserving it; is it intentional to silence it completely?

### `pmax3minslotnr` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pmaxsystype` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/machines/machine_pmax.c:893`, severity DEFECT, Add the missing `systype` variable to the environment block for Ultrix 3.1D.

### `ppccrnandundec` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ppcdcbiundec` -- DEFECT, 3 finding(s)

* src/cpus/cpu_ppc_instr.c:5290: DEFECT, if (user_mode) goto bad; /* missing actual privilege check */
* src/cpus/cpu_ppc_instr.c:5291: DEFECT, ic->f = instr(dcbi); break; /* missing handler assignment */
* src/cpus/cpu_ppc_instr.c:4782: QUESTION, UNSETTLED: missing lines 4782-4791 to verify or port the remainder of the fix.

### `ppcdecwrite` -- DEFECT, 1 finding(s)

* `src/cpus/cpu_dyntrans.c:450` DEFECT: The file and its defect site are completely omitted from the fix. Apply equivalent decrementer MSB logic to the dynamic translation path.

### `ppcexcfatal` -- DEFECT, 2 finding(s)

* src/cpus/cpu_ppc.c:329 DEFECT Diff removes the log entirely instead of porting to INFO level; fix: change to an INFO-level log macro as requested.
* src/cpus/memory_ppc.c:302 DEFECT Diff removes the log entirely instead of porting to INFO level; fix: change to an INFO-level log macro as requested.

### `ppcisisrr1` -- DEFECT, 1 finding(s)

* src/cpus/memory_ppc.c:324, DEFECT, missing fix for `src/cpus/cpu_ppc.c` and sets SRR1 after `ppc_exception` instead of before it.

### `ppclswizero` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ppcpterc` -- DEFECT, 1 finding(s)

* src/cpus/memory_ppc.c:131, severity DEFECT, Fix: implement the missing PTE referenced/changed bit updates for `get_pte_low`/`ppc_vtp32`.

### `ppcsprg2drop` -- DEFECT, 1 finding(s)

* `src/cpus/cpu_ppc_instr.c:2826` DEFECT: Missing privilege check (UNSETTLED how to trigger a PPC program exception from this file). Fix: `if (!cpu->cd.ppc.pr) reg(ic->arg[1]) = reg(ic->arg[0]); else { /* trigger interrupt */ }`

### `ppctlbieseg` -- SOUND, 1 finding(s)

* src/cpus/cpu_ppc_instr.c:3946 severity STYLE, wrap the comment to a new line or shorten it to stay within 79 columns.

### `rarpaddr` -- SOUND, 1 finding(s)

* src/net/net.c:251: STYLE: line exceeds 79 columns; move the comment to the line above.

### `scc3minlines` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/devices/dev_scc.c:445`: DEFECT: The mapping logic remains broken. The fix adds a comment instead of addressing the incorrect channel mapping. Fix: Implement the correct mapping instead of just commenting on it.

### `sccintpend` -- DEFECT, 2 finding(s)

* src/devices/dev_scc.c:201: DEFECT: Missed sites for WR9 and special-condition interrupts (UNSETTLED without full file context).
* src/devices/dev_scc.c:456: STYLE: Line exceeds 79 columns, wrap `d->scc_register_w[SCC_CHANNEL_A * N_SCC_REGS + SCC_WR1] &`.

### `sccloopback` -- DEFECT, 2 finding(s)

* `src/devices/dev_scc.c:128`: DEFECT, Smallest fix: UNSETTLED (Need to apply similar loopback if/else logic to lines 128-134 and 282-285).
* `src/devices/dev_scc.c:444`: STYLE, Smallest fix: `/* #T70: Loopback: */`

### `sccwr0ptr` -- SOUND, 1 finding(s)

* `src/devices/dev_scc.c:403`, STYLE, change to `/* #000: reg ptr, cmds not decoded */` to fix both column width and tag format.

### `scsievpd` -- SOUND, 1 finding(s)

* `src/disk/diskimage_scsicmd.c:364`: STYLE, missing once-latch for guest-triggerable warning. Fix: `if (!d->warned_evpd) { d->warned_evpd = 1; debugmsg(... "(once)..."); }`

### `scsimodeselhdr` -- SOUND, 1 finding(s)

* 5. src/disk/diskimage_scsicmd.c:1308, STYLE: The new comment uses a literal `#NNN` placeholder instead of a specific issue identifier. Fix: `/* #scsimodeselhdr: Relax check to only require block descriptor length 0x08 */`

### `scsimodesensepc` -- DEFECT, 2 finding(s)

* `src/disk/diskimage_scsicmd.c:595`: DEFECT - The added `return 0;` exits the function early, skipping the common tail at AFTER:1389 and AFTER:1391, returning 0 instead of 1. Smallest fix: `break;`
* `src/disk/diskimage_scsicmd.c:593`: STYLE - Guest-triggerable diagnostic lacks a latch and `(once)` string. Smallest fix: `static int l = 0; if (!l) { debug("WARNING: mode sense, cmd[2] = 0x%02x (once)\n", xferp->cmd[2]); l = 1; }`

### `singlestepdecl` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `tcemptyslot` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `tlbwrrandom` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `vr4131siuinuse` -- UNSETTLED, 1 finding(s)

* src/devices/device.c:266: QUESTION: Line 266 is still missing from the provided `device.c` lines 244-260 snippet; UNSETTLED if a change is needed here to fully resolve the issue.

### `x11cursorclip` -- DEFECT, 4 finding(s)

* file:src/devices/dev_fb.c:913, DEFECT, UNSETTLED (missing dev_fb.c lines 913-914 to apply the visible_xsize clamp).
* file:src/devices/dev_turbochannel.c:250, DEFECT, UNSETTLED (missing dev_turbochannel.c lines 250-251 to apply the visible_xsize clamp).
* file:src/console/x11.c:233, DEFECT, clip `fbwin->OLD_cursor_...` bounds against `fbwin->fb_ximage->width` and `height` before calling `XPutImage`.
* file:src/devices/dev_fb.c:250, STYLE, break the ternary expression to stay within 79 columns.

### `armclrexundec` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `armexregstop` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `armldrexbhdspin` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `armldrexprev6` -- DEFECT, 2 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/cpus/cpu_arm_instr.c:4204` DEFECT The required ARMv6 check is missing. Smallest fix in ONE line: add `if (!cpu->cd.arm.is_v6_or_higher) goto bad;` (or the exact equivalent flag test for this codebase) before `ic->f = cond_instr(ldrex);`.
* `src/cpus/cpu_arm_instr.c:4221` DEFECT The required ARMv6 check is missing. Smallest fix in ONE line: add `if (!cpu->cd.arm.is_v6_or_higher) goto bad;` before `ic->f = cond_instr(strex);`.

### `armstrexgranule` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `bootblockzeroaddr` -- DEFECT, 2 finding(s)

* `src/disk/bootblock.c:259` DEFECT: The early return skips the common cleanup tail, specifically bypassing `free(bootblock_buf);`. Fix: replace `return 0;` with `goto ret_ok;`.

### `catsmemwrap` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `dec5800ncpushift` -- SOUND, 1 finding(s)

* `src/devices/dev_dec5800.c:360`: STYLE, line exceeds 79 columns. `odata = cpu->machine->ncpus >= 64 ? ~(uint64_t)0 :` (split over two lines)
* `src/devices/dev_dec5800.c:365`: STYLE, line exceeds 79 columns.

### `devstrnamequote` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `dyntransstatsbuf` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ecoffclampdead` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `fbscaledownoob` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/devices/fb_include.c:232` (approximate, missing from diff), DEFECT, apply the identical bounds-clamping fix to the `fb_include.c` file as requested by the issue ticket.

### `hpcmipsalloc` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `i8259initread` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `i8259pollcomment` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `kn01bytewrite` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `kn230irqwrong` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `m88kaluignored` -- DEFECT, 1 finding(s)

* 1. cpu_m88k_instr.c:3815: DEFECT: the issue explicitly names sites 3660 and 3815, but the diff only modifies logic around 3660 (which covers 3693 and 3736 in post-edit numbering). It misses site 3815 entirely. Fix: address the switch or logic at 3815.
* 2. cpu_m88k_instr.c:3660: QUESTION: No early exits, gotos, breaks, or returns were added that skip the common tail.
* 3. cpu_m88k_instr.c:3660: QUESTION: No paths return anything different.
* 4. cpu_m88k_instr.c:3660: QUESTION: No other state is modified beyond applying the mask for div/mul/cmp.
* 5. cpu_m88k_instr.c:3660: STYLE: All lines remain well under 79 columns and the issue tags `/* #m88kaluignored: ... */` are applied correctly.

### `m88kldcrunimpl` -- DEFECT, 2 finding(s)

* src/cpus/cpu_m88k.c:504, STYLE, replace `static bool warned = false;` with a per-instance latch field like `if (!cpu->warned_ldcr_unimpl) {`.
* src/cpus/cpu_m88k.c:507, STYLE, append `(once)` to the message string: `"ldcr: UNIMPLEMENTED cr = 0x%02x (%s) (once)\n"`.

### `mipsdsbranch` -- DEFECT, 3 finding(s)

* `src/cpus/cpu_mips_instr.c:4837`: DEFECT: The fix misses three of the five sites reported in the issue. Fix: Apply the same `goto bad;` removal to the remaining three sites.
* `src/cpus/cpu_mips_instr.c:5770`: QUESTION: The exact effect on the return value of bypassing `goto bad;` is UNSETTLED. Missing: The `bad:` label and return statements at the bottom of the function.
* `src/cpus/cpu_mips_instr.c:4642`: STYLE: Comment uses text instead of a numeric tag. Fix: Change `/* #mipsdsbranch: ... */` to `/* #NNN: mipsdsbranch, unpredictable, do not halt */` using the appropriate numeric ID.

### `mipseidicu0` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mipsllzero` -- SOUND, 1 finding(s)

* 5. STYLE: `src/cpus/cpu_mips_instr.c:5486`. The new comment `/* Load into the dummy scratch register... */` does not contain a `/* #NNN: ... */` tag. Fix: `/* #mipsllzero: Load into the dummy scratch register, if rt = zero */`.

### `mipsmuldivrd` -- SOUND, 1 finding(s)

* src/cpus/cpu_mips_instr.c:4590: STYLE - The new comment exceeds 79 columns (it is ~96 characters long, plus 4 tabs of indentation).

### `mipspromwordbe` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mipstlbpfnhigh` -- UNSETTLED, 1 finding(s)

* src/cpus/memory_mips_v2p.c:389: QUESTION - UNSETTLED: missing `src/cpus/memory_mips_v2p.c` lines 389-394 to check the arithmetic expression.

### `mk48gmtime` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `mpipimemmove` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `palputslen` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `pcibarsizeflag` -- UNSETTLED, 1 finding(s)

* src/devices/bus_pci.c:126 QUESTION UNSETTLED: need to see `src/devices/bus_pci.c` lines 126-131, 145-150, and 178.

### `ppc4xxcacheundec` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ppcmtmsrlbit` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ps2gmtime` -- SOUND, 1 finding(s)

* src/machines/machine_playstation2.c:156, severity STYLE, wrap line to stay within 79 columns.

### `pxrowloop` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ramallocnull` -- DEFECT, 1 finding(s)

* `src/devices/dev_ram.c:184`, STYLE, Smallest fix: Wrap the macro arguments to stay under 79 columns.

### `shrfcrkey` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `strtoullbase` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `wdcatadocstale` -- DEFECT, 1 finding(s)

* `src/devices/dev_wdc.c:1080`: DEFECT - The diff misses the second site in this file (and the two `regress` sites). The smallest fix is to apply the comment string removal to the other three locations named in the issue.

### `wdcchssector0` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `vgagfxwindowend` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ctorabortclass` -- DEFECT, 1 finding(s)

* UNSETTLED:UNSETTLED DEFECT Remove `irq=0` from `device_add` at `machine_alpha.c:71` and the `ip27` block (omitted in lines 295-654).

### `fbctrlvec128` -- DEFECT, 2 finding(s)

* src/devices/dev_fbctrl.c:119 DEFECT return 1;
* src/devices/dev_fbctrl.c:118 STYLE if (!d->warned_len) { fatal("[ fbctrl: access length > 8 is not supported (once) ]\n"); d->warned_len = 1; }

### `fbfiqsilent` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `fbirqstuck` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `fbpcibus255zero` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `gssiglblid` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `m88kexcsfu1` -- DEFECT, 3 finding(s)

* src/cpus/cpu_m88k.c:759 DEFECT: The exception is delivered without populating the required FPHS1/FPLS1/FPPT registers required by the architecture. Fix: Populate SFU1 exception state before breaking.
* src/cpus/cpu_m88k.c:839 DEFECT: Proceeding to the common tail unconditionally executes `cpu->cd.m88k.cr[M88K_CR_SSBR] = 0;`, destroying the scoreboard needed for FP exception delivery. Fix: Bypass zeroing SSBR for SFU1 exceptions.
* src/cpus/cpu_m88k.c:759 STYLE: The issue tag `/* #380 */` lacks descriptive text. Fix: `/* #380: Deliver SFU1 exception */`.

### `mboutcapacity` -- DEFECT, 3 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `src/devices/dev_mb89352.c:239` DEFECT: Bounding on `len` still allows out-of-bounds writes because `data_out_len` is resized without reallocation. Fix: UNSETTLED (needs the actual allocation size from diskimage_scsicmd or lines 476-495).
* `src/devices/dev_mb89352.c:476` DEFECT: The issue explicitly names lines 476-495 and diskimage_scsicmd, which this diff completely misses. Fix: UNSETTLED.
* `src/devices/dev_mb89352.c:240` STYLE: The diagnostic can be triggered repeatedly by the guest and lacks a latch and `(once)` in the message. Fix: Add latch field check and include `(once)`.

### `ofemulnodata` -- DEFECT, 3 finding(s)

* `of.c:1105` DEFECT: The fix is implemented as an early return in `of_emul` instead of at the decoder sites `cpu_arm_instr.c` and `cpu_ppc_instr.c`, violating the Argon scoping design.
* `of.c:1105` DEFECT: The early return causes the guest to continue execution with unwritten results instead of faulting.
* `of.c:1100` STYLE: The `warned` flag is a global static variable rather than a per-device instance latch.

### `ppcbatppkill` -- SOUND, 0 finding(s)

* (no file:line finding line)

### `ppctblcarry` -- DEFECT, 1 finding(s) -- **DRAFT WITHDRAWN after this review** (redrafted; fixcheck now SKIP)

* `cpu_dyntrans.c:455` DEFECT: The diff completely omits the required fix for `cpu_dyntrans.c` named in the issue ledger. UNSETTLED: missing file `cpu_dyntrans.c` to provide the exact one-line code fix for that site.

### `wdcdiagerr` -- DEFECT, 1 finding(s)

* src/devices/dev_wdc.c:593 DEFECT UNSETTLED exact fix (needs command context from `d`, e.g., `d->error && !(d->error == 0x01 && d->last_cmd_was_diag)`)

