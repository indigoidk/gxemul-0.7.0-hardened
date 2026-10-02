
### THE RETRO -- 185 rows (wave 1, the emulator source)

#### `ppcbatppkill` (HIGH) -- PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches fatal()+exit(1) instead of a DSI/ISI
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ppcfmasingle` (HIGH) -- PPC opcode-59 fnmadds/fnmsubs (and their Rc forms) are undecoded and stop the emulator (cpu_ppc_instr.c:5197-5218); fmadds/fmsubs are ALREADY FILED in prose (OUTSTANDING_BUGS.md:1705, :1712) -- cross-reference, do not double-file
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:24-27]

#### `gdromdmareentr` (HIGH) -- A guest-aimed GD-ROM DMA into its own +0x18 trigger recurses unboundedly and exhausts the host stack -- CONDITIONAL: a nonzero staged word, count and enable armed, data loaded, and the destination inside the trigger window
batch 1a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: grok's re-read: true only under a condition the title omitted; Astra ACCEPTS the condition (afile_07)]

#### `armendianexit` (HIGH, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:18721-18722 at db8b1a33 -- the CP15-endian member of the seven sibling exits of cpu_arm_coproc.c: a CP15 c1 write that toggles the B bit reaches fatal() + exit(1) (:157-178)
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [kind corrected: Astra afile_01: NOT NEW -- recorded in prose at OUTSTANDING_BUGS.md:18721-18722; D:281-284, ratified D:341; title corrected: Astra afile_01, D:281-284]

#### `ppcllscrcexit` (HIGH) -- lwarx/ldarx with Rc=1 or stwcx/stdcx with Rc=0 reach fatal()+exit(1) in X(llsc); the decoder keys on xo alone
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `i960disasmspan` (HIGH) -- i960: disassembling a long (two-word MEMB) instruction reads ib[4..7] of a four-byte buffer, on the to_be_translated `bad:` path and on the trace/single-step path
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `xscalecp6exits` (HIGH, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:18721-18722 at db8b1a33 -- the three XScale CP6 exits of cpu_arm_coproc.c (:322, :331, :417) end the process; the entry's other three siblings are `armcp15cp14exits`
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:335-336]

#### `mboutcapacity` (HIGH) -- MB89352: the WRITE path re-sizes data_out_len without reallocating, and DREG writes bound on that length
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `vgadirtyarm` (HIGH) -- VGA: an untracked charcells write below the CRTC start computes the dirty rectangle's END row in UNSIGNED arithmetic (dev_vga.c:743: `r + len - 1` with a negative int `r` and a size_t `len`), and outside the dyntrans branch the accumulated bounds can reach the redraw without that clamp unless a palette path resets them (:562-578).  The redraw's size and duration are UNMEASURED; the START row is a small negative (the ruling's `-1.7e9 origin` and `hours` are withdrawn)
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_07 (withdraws its earlier figures, holds HIGH on this basis); HIGH IS DISPUTED AND UNMEASURED -- grok's re-read: NOT TRUE (the origin is a small negative and the pixel reads stay in range); Astra holds HIGH for excessive redraw work and marks the endpoint conversion and the redraw time UNSETTLED; agy: UNSETTLED.  The round that takes this row measures first]

#### `dectxzero` (HIGH) -- DEC21143: an empty continuation of an empty first segment calls realloc(p, 0), which glibc answers with NULL, and CHECK_ALLOCATION ends the process
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `symdemanglebound` (HIGH) -- The C++ demangler copies a length-prefixed name component without testing source termination, over-reading a NUL-terminated loader string by up to MAXLEN bytes
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ecoffoffsetspan` (HIGH) -- ECOFF table-offset guards admit a sign-extended negative offset, then seek unchecked and exit(1) on the resulting short read
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ascwidecount` (HIGH) -- A 32-bit ASC transfer-count write during a continued DATA_OUT DMA yields a negative len2 that both span guards pass, and the DEC memcpy takes it as size_t -- CONDITIONAL: both existing offsets cover the negative count's magnitude (the guards do not admit every negative value)
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: grok's re-read: true only under a condition the title omitted; Astra ACCEPTS the condition (afile_07)]

#### `m88kconvodd` (HIGH) -- int.sd/nint.sd/trnc.sd reject an odd source register, and flt.ds an odd destination, by stopping the CPU
batch 3a, `cpum88kinstr:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88kfpr0stop` (HIGH) -- every FP arithmetic/convert decode with rD = r0 stops the CPU instead of raising the FP unimplemented-opcode exception
batch 3a, `cpum88kinstr:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88kbcndnest` (HIGH) -- m88k: a delayed branch entered as another delayed branch's delay slot recurses on the host without bound; separately, on the untaken nested unwind the shared dispatch pointer overruns its array once the cumulative increments exceed the entries that remain
batch 3a, `generatem88kbcnd:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: grok's re-read asked for a condition; Astra REJECTS grok's wording as too narrow and gives this one (afile_07)]

#### `mipscop0tail` (HIGH) -- Five COP0 decoder arms still `goto bad` (CPU stops) on guest-executable encodings: EI/DI off-R5900, MFMCz non-ei/di, BC0x, unknown rs
batch 3b, `cpumipsinstr:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipsresetalias` (HIGH) -- The reboot sentinel is gated on the VIRTUAL address's low 29 bits, so `break 0x30378` at any VA with low bits 0x1fc00000 stops the emulator (or raises CpU instead of BP)
batch 3b, `cpumipsinstr:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shifetchkill` (HIGH) -- SH: a privileged instruction fetch from 0xe4000000-0xffffffff ends the process at memory_sh.c:379-381 -- reached through the guest's own VBR (+0x100 / +0x600) on the...
batch 3d, `cpush:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `pvrdirtyregion` (HIGH) -- PVR pvr_extend_update_region(): with zero display width it divides by zero (SIGFPE) on any multi-byte VRAM write whose span straddles DIWADDRL; with ordinary geometry...
batch 3d, `devpvr:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `x11alloc32` (HIGH) -- X11 resize allocation wraps when size_t is 32 bits, inside the 16384 cap
batch 3g, `bundle_console:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `emulgzipfail` (HIGH) -- A gzip load that fails to decompress terminates the process
batch 3g, `emul:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2krxbudget` (HIGH) -- NE2000: enabled reception with an invalid ring has no per-tick packet budget -- CONDITIONAL: reception enabled, the ring persistently invalid with OVW clear, and ingress keeping packets available; a finite burst drains
batch 3f, `devne2000:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: grok's re-read: true only under a condition the title omitted; Astra ACCEPTS the condition (afile_07)]

#### `taprxquota` (HIGH) -- The TAP receive poll never increments its packet budget (unconditional); CONDITIONAL consequence: the poll does not return to emulation while read() keeps returning a nonnegative count
batch 3f, `bundle_net:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: grok's re-read: true only under a condition the title omitted; Astra ACCEPTS the condition (afile_07)]

#### `arccursorbound` (HIGH) -- Unbounded ARC cursor column makes erase-line walk 2^31 cells
batch 3h, `arcbios:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `arczeroalloc` (HIGH) -- Zero-length ARC disk I/O calls malloc(0) and CHECK_ALLOCATION exits if that returns NULL
batch 3h, `arcbios:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `arcsgiprivate` (HIGH) -- `src/promemul/arcbios.c:1271` dispatches to the SGI handler whose default stops the CPU at `:1226`
batch 3h, `arcbios:F6` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `dyncacheoffset32` (HIGH) -- CONDITIONAL: with `-k` at least 4097 on a 64-bit host, once the translation-cache cursor crosses 2^32 a truncated 32-bit page offset is published and the dispatch loop calls through it (cpu_dyntrans.c:797-833)
batch 3h, `bundle_core:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:962, :966]

#### `ofopenexit` (HIGH) -- OpenFirmware open exits the host on any nonempty pathname
batch 3h, `bundle_promemul:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `armcp15cp14exits` (HIGH, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:18721-18722 at db8b1a33 -- the three remaining sibling exits of cpu_arm_coproc.c: :62 CP15 Rd==PC, :264 CP15 PID, :528 CP14 unknown (the id is assigned HERE: the ruling left one id owed)
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:335-336 and D:284; id chosen by the main loop]

#### `m88kpsrbokill` (HIGH) -- m88k: a supervisor stcr or rte that writes PSR with the BO bit flipped against the machine's byte order stops the CPU (cpu_m88k.c:522-532; cpu_m88k_instr.c:843-847)
batch 3a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:557-563 (the ruler's own addition)]

#### `osiopselectzero` (HIGH, an id for an entry this file already carries in prose) -- a SITE of the existing class row `exitunowned76` (dev_osiop.c), id reserved by the ruling for the round that takes it
batch 3e, `devosiop:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:681]

#### `osiopregexit` (HIGH, an id for an entry this file already carries in prose) -- a SITE of the existing class row `exitunowned76` (dev_osiop.c), id reserved by the ruling for the round that takes it
batch 3e, `devosiop:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:683]

#### `osiopdnadexit` (HIGH, an id for an entry this file already carries in prose) -- a SITE of the existing class row `exitunowned76`: dev_osiop.c:942, :946 whitelist OSIOP_DNAD (0x28) and OSIOP_ADDER (0x3c) for 32-bit width, the register switch has no case for either, and one aligned access reaches exit(1) at :1152
batch 3e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:700 (the ruler's own addition)]

#### `pvrrenderexit` (HIGH, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2721-2723 at db8b1a33 -- dev_pvr.c's render and texture loops still call exit(1) (the entry graded it `med DoS`; the ruling grades it HIGH)
batch 3d, `devpvr:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:726]

#### `ofpeerexit` (HIGH) -- OpenFirmware peer(): of.c:394 calls exit(1) when the handle is not the root and the lookup misses
batch 3h -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:956 (the ruler's own addition)]

#### `tcpdebugopts` (HIGH, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2731 at db8b1a33 -- the TCP options dump in net_ip.c (:420-447) runs while i < data_offset with no test against the frame length, so on a short frame it reads past a transmit buffer allocated at exactly the transmitted length (dev_dec21143.c:788-809, dev_le.c:410-439; dev_ne2000.c:278 is a 2048-byte buffer and is not affected) -- CONDITIONAL: the dump runs only while NET debug verbosity is on
batch 3f, `netip:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [missing from the table until chk_filed_exist.py.txt (the id existed nowhere); the grok ruling grok_rule3f.txt:37-38 (HIGH by the severity rule's letter while NET debug verbosity is on), D:870; grok's first-hand read (grok/grok_file3ids.txt): TRUE, HIGH while SUBSYS_NET verbosity is DEBUG (the default is INFO)]

#### `shoddprfield` (LOW/HIGH (disputed)) -- SH4 PR=1 arithmetic and compare handlers accept an odd register field and read or write fr[n+1] -- field 15 lands on xf[0]; FCNVSD/FCNVDS are NOT affected.  SEVERITY DISPUTED, LOW or HIGH: a rule question (is an out-of-array access inside the containing struct HIGH?)
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:223-230]

#### `ppcbatstale` (MED) -- PPC: mtspr to a BAT (or to HID0[HIGH_BAT_EN]) never invalidates the dyntrans translation cache and isync is a nop, so a remapped block keeps its old physical page
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `divbyinfnan` (MED) -- ieee_div_round_rm()/ieee_div_round_to_odd(): a finite dividend over an infinite divisor yields a NaN or +/-2^-1074 where the ISA owes a signed zero
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88ksddovf` (MED) -- m88k single-destination arms with a double source lose the exponent range in their double intermediate: an exact result from 2^1024 - 2^970 up stores +/-Inf where MC88100 Table 2-6 owes the largest finite value under RZ, positive RM and negative RP; a nonzero product with |exact| <= 2^-1075 stores 0 where positive RP and negative RM owe the minimum subnormal (batch 2b's `sddexprange`, consolidated here)
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01; corrected by Astra afile_05: D:238-241, fable_batch1b.md:27-28, fable_batch2b.md:52-60]

#### `scsicapnosense` (MED) -- SCSI READ/WRITE refused by the #163 transfer-size cap return CHECK CONDITION with the sense latch CLEARED, so the guest's REQUEST SENSE answers NO SENSE
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `timerupdrow` (MED, test coverage) -- diff_timer.c never reaches timer_update_frequency()'s store on a CHANGE (both calls re-send the already-normalised rate)
batch 1b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01 and afile_02: the harness consolidation grades it MED, H:316]

#### `sh4tmupending` (MED) -- unacknowledged SH4 timer underflows accumulate without bound in signed timer_interrupts_pending[]
batch 1a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `wdcnien` (MED) -- wdc models no nIEN: completion IRQs are asserted even when the guest set nIEN
batch 1a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `M2_gdromnodatawidth` (MED) -- L2 OBLIGATION (CHANGELOG.md:3124-3143 at 7440e129), never discharged: the committed gdrom_default_probe.py has no `nodata byte` / `accept byte` row and its no-data session uses word stores only
batch 1a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01: the missed behaviour is the guest-visible DMA busy state not clearing (CHANGELOG.md:3124-3143; dev_dreamcast_gdrom.c:1406-1417, :1471); title corrected: Astra afile_01; corrected by Astra afile_05: the dispositions' :2896-2909 is that block's place at the reviewed commit]

#### `armmemcpyoverlap` (MED) -- netbsd_memcpy fold: forward-overlapping copy publishes pre-store source words and calls memcpy on overlapping ranges
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `armcachecleanload` (MED) -- netbsd_cacheclean fold never performs the ldr: r2 stays stale and a walk over an unmapped page cannot fault
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ppcllscsrr0` (MED) -- X(llsc) never synchronizes cpu->pc before memory_rw, so a DSI raised in lwarx/stwcx records a stale SRR0
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ppcnanpayload` (MED) -- PPC add, subtract, multiply, divide and the fused handlers lose a NaN operand's payload through ieee_interpret/ieee_store (fnmadd/fnmsub also flip its sign); fsel preserves it
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:151-153]

#### `ppcfpstatus` (MED) -- PPC arithmetic and conversion handlers do not derive numerical rounding status (FR, FI, XX, OX, UX); explicit FPSCR writes can still set those bits
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:154-155]

#### `armalignexc` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1256-1264 at db8b1a33 -- `armbdt`'s residual: with alignment checking enabled, an unaligned access does not raise the alignment exception it owes
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:168-169, :778]

#### `ppcfmarn` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1620-1622 at db8b1a33 -- the PPC fused multiply-add forms ignore FPSCR[RN] and round as the host does
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:170]

#### `ppcsinglealias` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1671-1675 at db8b1a33 -- fadds/fsubs/fmuls/fdivs keep double precision instead of narrowing to single
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:171]

#### `ppcfprfclass` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1685-1687 at db8b1a33 -- result classification never updates FPRF's C bit (explicit FPSCR writes can)
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:172-173]

#### `ppcveinhibit` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1685-1687 at db8b1a33 -- frsp overwrites FRT and FPRF, and fctiw/fctiwz overwrite FRT, despite an enabled VE
batch 2a -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:172-173]

#### `optinyband` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1971-1973 at db8b1a33 -- below the OPTINY cutoff div, sqrt and mul keep the NEAREST result where a directed rounding was requested (fadd excluded: its helper has no cutoff)
batch 2a, `- + batch 2b` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:174-176, :246; MED confirmed from float_emul.c:895-896, :1027-1028, :1045-1046]

#### `oddoptinyband` (MED) -- the OPTINY guard copied into ieee_div_round_to_odd() suppresses the odd-force for normal operands below 2^-969 and breaks NEAREST single rounding on m88k fdiv.sdd
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `addovftie` (MED) -- ieee_add_round_rm() returns the nearest sum when 2Sum's intermediate overflows: RZ at the overflow tie stores 0xffeffffffffffffe where 0xffeffffffffffffd is owed...
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shnestedbranch` (MED) -- a delayed branch in another branch's delay slot is silently re-run as a plain branch; the manual makes it a Slot Illegal Instruction exception (EXPEVT H'1A0)
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shslotres` (MED) -- X(reserved) raises EXPEVT_RES_INST (H'180) in a delay slot; the manual requires the Slot Illegal code H'1A0 for the designated undefined instruction H'FFFD there --...
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipscmpdenorm` (MED) -- the #246 denormal-operand E trap fires for C.cond.fmt on R4000; the manual exempts Compare
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipstinyenable` (MED) -- the #246 tiny-result guard tests FS alone; the R4000 raises E for a tiny result whenever Underflow OR Inexact is ENABLED, FS notwithstanding
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipstinyhostzero` (MED) -- a D result the host already rounded to +-0 is classified FP_ZERO and escapes the #246 tiny trap; exact 2^-2044 from mul.d(2^-1022, 2^-1022) stores +0 where FS=0 owes E
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shdnoperand` (MED) -- (Fable's own) -- with FPSCR.DN=1, the reset default, a denormalized OPERAND is treated as zero on silicon (sh4_programming.txt:999); the fork decodes it to its true...
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipstinyprerm` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1650-1655 at db8b1a33 -- The #246 trap predicate is pre-rounding. `fabs(nf) < FLT_MIN` at
batch 2b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ppctblcarry` (MED) -- PPC: an mftb polled at TBL == 0xffffffff pushes the 64-bit TBL cell to 2^32; the #141 batch update then truncates it and the carry into TBU is lost
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `armmrcr15flags` (MED) -- i80321 CP6: an MRC with Rd=R15 stores into r[15] and leaves NZCV untouched; the ARM ARM routes bits 31:28 to the flags and does not write the register
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipssuperseg` (MED) -- MIPS R4000+: in Supervisor mode with EXL=ERL=0, translation refuses sseg with SX=0 and xsseg/csseg with SX=1 (AdEL/AdES); addresses inside the selected user-space limit still reach the TLB
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:317-320]

#### `mipssamepcstore` (MED) -- swl/swr/sdl/sdr: the #227 load-to-store ExcCode conversion is gated on `cpu->pc != oldpc`, which is false when the faulting store sits at the very vector its own...
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `sh4utlbmultihit` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1946-1947 at db8b1a33 -- the SH4 first-match UTLB walker never detects a multiple hit, on any translated access (not only the SQ PREF)
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:331-333]

#### `alphatinyzero` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1645-1649 at db8b1a33 -- a negative tiny Alpha result keeps -0 where unqualified T operations owe an exact +0 (21066_66a_hrm.txt:1889-1891); the entry's `no Alpha rig` premise is stale since #505-#508
batch 2c -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:333-334]

#### `mbcdbincomplete` (MED) -- MB89352 dispatches a CDB whose uncollected bytes are uninitialised heap
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `rtcpendovf` (MED) -- dev_rtc: pending_interrupts increments without saturation and wraps negative under an unacknowledged high-rate timer
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `gssiglblid` (MED) -- ps2_gs: N_GS_REGS excludes the file's own highest register, so SIGLBLID (0x1080) is refused -- writes dropped, reads 0
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mpstartupsp` (MED) -- dev_mp STARTUPCPU sets the startup stack pointer only for MIPS and PPC; every other test machine starts the CPU with its old SP against the documented contract
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mk48aliasrow` (MED, test coverage) -- mk48_nvram_probe.py's nine round-trip rows each run one offset per session, so the DISTINCT bytes cannot see a mutant folding offsets onto one cell; the kill table...
batch 2d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01 and afile_02: the harness consolidation grades it MED, H:391]

#### `ascoutresid` (MED) -- A DATA_OUT DMA clamped to the target's remaining length still reports residual 0 with Terminal Count set
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `asccmddma` (MED) -- COMMAND-phase DMA reads the CDB from the private DEC buffer even when an external DMA controller is configured (PICA)
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ascpiozero` (MED) -- PIO DATA_IN pushes zeros from the never-populated incoming_data instead of xferp->data_in
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `writeflusherr` (MED) -- Under -f, a guest WRITE reports GOOD after fflush()/fsync() fail -- overlay data, flat file and bitmap all discard the results
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `drecalccap` (MED) -- READ CAPACITY (and the two other recalc callers) re-run diskimage_recalc_size() on a d:-retyped floppy image and replace its exact geometry with 16/63
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `stalelbsbound` (MED) -- MODE SELECT changes logical_block_size without refreshing nr_of_logical_blocks, so the read bound shrinks until a capacity command recalculates
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `cuebomparse` (MED) -- The CUE sniffer skips a UTF-8 BOM that the parser keeps in its first keyword, so a BOM-prefixed FILE line is dropped and the image falls back to flat
batch 2e -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88kdivcontext` (MED) -- m88k: a delivered INTEGER-DIVIDE exception writes no fcr2/fcr4/fcr5 and clears the destination scoreboard bit (precise FP delivery is `m88kexcsfu1`'s)
batch 3a, `cpum88k:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:549]

#### `m88kextcross` (MED) -- ext with offset+width > 32 no longer sign-extends from bit 31
batch 3a, `cpum88kinstr:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88knegdiv` (MED) -- div completes negative-operand divisions that the MC88100 traps on; the #195 comment states a false premise
batch 3a, `cpum88kinstr:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88kpairpadding` (MED) -- Double-result FP handlers can write r[32], and double-source FP handlers read it back. Doubleword loads and stores starting at r31 are currently rejected by the decoder
batch 3a, `cpum88kinstr:F7` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipsbadvpnscale` (MED) -- R4000 Context/XContext BadVPN2 is scaled by the matched (or last-scanned) TLB entry's page size instead of fixed VA bits 31:13 / 39:13
batch 3b, `cpumips:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipssubmin` (MED) -- SUB/DSUB test overflow on the NEGATED subtrahend: MIN-MIN traps, 0-MIN does not
batch 3b, `cpumipsinstr:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipscachepriv` (MED) -- The R3000 cache-invalidate fold mutates the loop register and skips to the final MTC0 before any COP0 availability check runs
batch 3b, `cpumipsinstr:F6` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipspsfault` (MED) -- PS-format COP1 on an R3000/R4000-class FPU raises RI; the R4000 owes an FPU Unimplemented-Operation exception (Cause.E, FPE), and CpU when CU1 is clear
batch 3b, `cpumipsinstr:F9` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `mipssynci` (MED) -- SYNCI has no REGIMM decoder case, so modelled Release-2 CPUs (4KEc, 24KEc, 5KE) raise RI on a defined instruction
batch 3b, `cpumipsinstr:F10` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m8dirtyfast` (MED) -- m88k: a READ of a writable page installs a writable fast-path mapping, so the first store through it never sets the page descriptor's M bit
batch 3e, `devm8820x:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m8supersegrow` (MED, test coverage) -- diff_m8820x.c's survivor check passes on EQUALITY, so SUPER_SEGMENT narrowed to SUPER_PAGE -- or deleted -- still passes, and no other row drives SUPER_SEGMENT (also the harness review's `m88supersegflush`)
batch 3e, `devm8820x:F9` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01: the harness consolidation grades it MED, D:674 and H:771; title corrected: Astra afile_01, D:674, H:771 and fable_batch3e.md]

#### `pcc2timerlanes` (MED) -- PCC2: byte and halfword writes that START inside one of the four 32-bit counter/compare words are declined
batch 3e, `devpcc2:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `osiopzeroram` (MED) -- OSIOP: a SCRIPTS or DMA read from RAM whose 1 MB memblock was never written stops the script engine instead of reading zeros
batch 3e, `devosiop:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `lebufsize` (MED) -- LANCE: the 12..1900 byte-count window rejects legal buffers -- RX buffers above 1900 bytes and TX continuation fragments under 12
batch 3e, `devle:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `letxrestart` (MED) -- LANCE: STOP then STRT does not restore TXON after a transmit abort or MERR -- only INIT does
batch 3e, `devle:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `letxshortage` (MED) -- LANCE: a host-owned TX continuation (OWN clear) that is not yet available leaves the partial frame pending with no BUFF, no TINT and TXON still set
batch 3e, `devle:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:687, :695]

#### `lerxstaleenp` (MED) -- LANCE: RMD1 status is OR-ed into the host-written word, so a stale ENP (and stale ERR/FRAM/OFLO/CRC/BUFF/STP) survives into the status the chip returns
batch 3e, `devle:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shresetinit` (MED) -- SH reset arm (power-on, manual, TLB multiple-hit) sets PC, VBR and SR only; FPSCR, MMUCR and the on-chip module registers keep their pre-reset values
batch 3d, `cpush:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `shinttieorder` (MED) -- SH INTC: equal-priority requests are ordered by arrival (assert path) or by lowest INTEVT code (rescan), not by Table 19.5 -- SCIF RXI loses to an earlier TXI
batch 3d, `cpush:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `alphatbilowerwidth` (MED, test coverage) -- alpha_tbi_probe.py cannot see the LOWER-bound selector cast narrowed to 32 bits alone (cpu_alpha_palcode.c:430): every value it drives gives the same answer
batch 3d, `cpualphapalcode:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01 and afile_02: the harness consolidation grades it MED, D:734 and H:206; title corrected: Astra afile_01, D:734 and fable_batch3d.md]

#### `thumbrorstale` (MED, test coverage) -- arm_flags_probe.py's two `T RORS clears Z / N` rows preset N=0 Z=0, so #329's clear-before-re-deriving repair (cpu_arm.c:1454-1455) can be removed and both still pass (also the harness review's `rorsstalevacuous`)
batch 3c, `cpuarm:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [sev corrected: Astra afile_01: the harness consolidation grades it MED, D:774 and H:839; title corrected: Astra afile_01, D:774, H:34, :839; also covers the harness review's group 01 harmflagsprobe:F1 (the id `rorsstalevacuous`, consolidated here)]

#### `armabortdest` (MED) -- A faulting word load zero-fills its destination after Data Abort entry (LE hosts)
batch 3c, `cpuarminstrloadstore:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `armliteralrot` (MED) -- Same-page PC-relative LDR shortcut assembles the unaligned bytes and skips the U=0 rotation
batch 3c, `cpuarminstrloadstore:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `fbpcibus255zero` (MED) -- A PCI-config read decoding to bus 255 returns 0, not the no-device answer
batch 3c, `devfootbridge:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `fbexternalclock` (MED) -- TIMER_EXTERNAL runs the timer from the internal clock; hardware counts irq_in_l edges
batch 3c, `devfootbridge:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `subpagecache` (MED) -- A 1 KB guest page is cached as a full host page
batch 3g, `memoryrw:F1` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ramnulltail` (MED) -- A read that starts in an unallocated memblock zeroes the whole request, including a later allocated memblock, and returns success
batch 3g, `memoryrw:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2ktsrstale` (MED) -- A rejected transmit leaves the previous TSR value
batch 3f, `devne2000:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2kdmacmd` (MED) -- Remote DMA follows the CPU access, not the CR command
batch 3f, `devne2000:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2kzerordc` (MED) -- Reissuing exhausted remote DMA alongside a transmit command fails to assert RDC immediately
batch 3f, `devne2000:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2kparsync` (MED) -- NE2000: a page-1 PAR write does not update the address the TAP backend filters UNICAST on, with promiscuous mode clear (dev_ne2000.c:607; net_tap.c:89)
batch 3f, `devne2000:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [title corrected: Astra afile_01, D:888]

#### `ne2krxfilter` (MED) -- RCR accept-broadcast and accept-multicast are stored and never applied
batch 3f, `devne2000:F6` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2krxfcs` (MED) -- Receive reserves four FCS bytes and never writes them
batch 3f, `devne2000:F7` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2kloopback` (MED) -- TCR and DCR loopback bits are stored and transmit still leaves the card
batch 3f, `devne2000:F8` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2krxphy` (MED) -- Every stored receive status is PRX with PHY clear
batch 3f, `devne2000:F9` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `ne2kmontally` (MED) -- Monitor mode frees frames and the missed-packet tally reads as zero
batch 3f, `devne2000:F10` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `jazzpendingovf` (MED) -- Interval-timer backlog is a signed counter with no saturation
batch 3f, `devjazz:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `fbresizeoverlap` (MED) -- Framebuffer growth overlaps its controller mapping
batch 3h, `bundle_core:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`

#### `m88kconvdelivery` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:1549-1558 at db8b1a33 -- m88k float-to-int conversions complete in the emulator where the MC88100 raises a conversion-overflow or reserved-operand exception and writes nothing (cpu_m88k_instr.c:2063-2101)
batch 3a, `cpum88kinstr:F6` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:532; MED by the severity rule -- the dispositions line states no grade]

#### `m88kidleslotsem` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:4675-4682 at db8b1a33 -- the m88k idle fold decides to idle from the polled word's PRE-slot value, so a slot that writes it can still request a premature idle (cpu_m88k_instr.c:2726-2765)
batch 3a, `cpum88kinstr:F15` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:541, :551]

#### `mipsreadpriv` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2636-2638 at db8b1a33 -- the mfc0/dmfc0 READ-side availability check is missing on the fast paths, and the `rt == $zero -> nop` fold also drops CFC0 (cpu_mips_instr.c:4950-4951)
batch 3b, `cpumipsinstr:F7` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:596, :639-640]

#### `mipsr3kpcpriv` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2636-2638 at db8b1a33 -- the EXC3K user-mode-from-PC heuristic (contrived to reach; the in-code comment says forcing KUc `crashes Linux`)
batch 3b, `cpumipsinstr:F8` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:597]

#### `mipstrapgate` (MED) -- MIPS trap instructions are gated the wrong way round: the REGIMM forms TGEI/TGEIU/TLTI/TLTIU/TEQI/TNEI become `reserved` when isa_level < 32 (cpu_mips_instr.c:5358-5369), so R4000/R4400/R5000/R10000 raise RI on instructions they implement, while the SPECIAL forms TGE/TGEU/TLT/TLTU/TEQ/TNE have NO ISA gate (:4535-4540), so an R3000 executes them where RI is owed
batch 3b -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01; corrected by Astra afile_05: D:627-635 (the ruler's own addition: one row, both halves)]

#### `pvrpal8888trunc` (MED) -- PVR: dev_pvr.c:838 loads a 32-bit palette entry into `uint16_t c32`, so in ARGB8888 palette mode alpha and red are always 0 and every such texel renders nothing
batch 3d -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:756 (raised by the check, verified by the ruler)]

#### `armcachegeom` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2097-2109 at db8b1a33 -- ARM1136JSR1's cache-type word describes a 512-byte, 32-way D-cache with a negative NSETS exponent (arm_cpu_types.h:78; cpu_arm.c:158-172)
batch 3c, `cpuarm:F2` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:771]

#### `armdwordalign` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:5140-5144 at db8b1a33 -- (task #74) LDRD/STRD mask the address with ~7 where ARMv6 with U=1 permits word alignment and accesses address and address+4
batch 3c, `cpuarminstrloadstore:F5` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:779]

#### `armoddpair` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:5142-5143 at db8b1a33 -- (task #76) LDRD/STRD with an odd Rd reach the pair transfer where the ARM ARM makes the instruction UNDEFINED
batch 3c, `cpuarminstrloadstore:F6` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [Astra afile_01, D:780]

#### `ramspaninval` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2727-2728 at db8b1a33 -- a bulk RAM write invalidates translated code once per memblock fragment, at the fragment's first page (memory_rw.c:760; the split and recursion at :762-775), so translated code in the later pages it writes can go stale -- CONDITIONAL: only an access that skips the 1 KB split (a PHYSICAL access, or a CPU with no translate_v2p: memory_rw.c:186) reaches that single invalidate with a length past its first page, e.g. GD-ROM DMA on the Dreamcast; a translated store is cut to at most 1024 bytes and each chunk invalidates its own page.  The queue's prose says `only the endpoint pages`
batch 3g, `memoryrw:F3` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [missing from the table until chk_filed_exist.py.txt (the id existed nowhere); the grok ruling grok_rule3g.txt:13-14 (proposes the id; independent grade MED), Astra codex_astraconfirm_3g.txt:8 (the id does not exist; the prose files the defect), D:824; the CONDITION is grok's first-hand read (grok/grok_file3ids.txt), and the main loop read memory_rw.c:186 and :757-775 at 7440e129]

#### `jazzlbmask` (MED, an id for an entry this file already carries in prose) -- OUTSTANDING_BUGS.md:2730 at db8b1a33 -- the Jazz local-bus interrupt enable BITS are unused: the access at the LB_IE address (pica.h:117; dev_jazz.c:677-684, relative 2) stores and returns jazz_timer_value, and jazz_interrupt_assert (dev_jazz.c:138-147) forwards every pending local line when EXT_IP3 is enabled, so a local interrupt the guest would mask is still delivered (the `dual-pending-IRQ loss` half of the queue's sentence is the existing entry OB-22)
batch 3f, `devjazz:F4` -- `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`  [missing from the table until chk_filed_exist.py.txt (the id existed nowhere); the grok ruling grok_rule3f.txt:70-71 (no grade stated), D:881; grok's first-hand read (grok/grok_file3ids.txt) found the first title NOT TRUE -- the LB_IE address IS handled, as the timer value -- and gives this reading and the grade MED; the main loop read dev_jazz.c:138-147 and :677-684 at 7440e129]

#### `astraretrolow` (LOW, a CLASS row) -- the 52 LOW rows of wave 1, the emulator source, one line each; a row is promoted to its own ledger row when a round takes it up
`regress/artifacts/astraretro_20260926/DISPOSITIONS.md`; the table with each row's governing text: `regress/artifacts/astrafiling_20261002/FILING.tsv`.

* `M1_sh4latchleak` -- L2 OBLIGATION (CHANGELOG.md:3124-3133 at 7440e129), never discharged: sh4_chcr_probe.py stores once per tested channel (only channel 0 repeats), so the (1,set) and (7,set) latch cells have no row (batch 1a)  [sev corrected: Astra afile_01: the missed behaviour is a repeated diagnostic (dev_sh4.c:785-792); title corrected: Astra afile_01; corrected by Astra afile_05: the dispositions' :2896-2903 is that block's place at the reviewed commit]
* `sh4chcrdualdiag` (test coverage) -- sh4_chcr_probe.py R7/L0 count only VAL_RE, so a mutant turning an RS-switch `return` into `break` (illegal RS + IE set -> decline PLUS a spurious IE_RE) would escape... (batch 1a)  [also covers the harness review's group 14 hgateshrounding:F1 (the id `sh4chcrrsfall`, consolidated here)]
* `armuserpageshift` -- copyin/copyout evaluate signed `1 << (index & 31)` before their decline guards (batch 2a)
* `ppccrlogicshift` -- seven CR logical handlers evaluate signed `1 << (31-bt)`; bt=0 gives 1<<31 (batch 2a)
* `badfmtlatchrow` (test coverage) -- #279's two one-shot latches have no committed row that fires them (batch 2b)
* `ftrvfourstores` (test coverage) -- only the fr0 store of `ftrv`'s four is observed (sh_rounding_probe.py:94-98) (batch 2b)
* `mipscvtsdlive` (test coverage) -- AMENDED (Astra): the gap is the `cvt.s.d` RN/RZ CONTRAST specifically; the nearest-mode single-store wiring IS observed live (mips_rounding_probe.py:63, the `cvt.s.l`... (batch 2b)
* `testmipshighramrow` (test coverage) -- nothing at HEAD observes testmips's >256 MB mirror/high mapping (#120's "regression-gated" has no carrier; every `-M` under regress/ is 32 or 64) (batch 2c)
* `gberesizezero` -- GBE keeps a rejected VCMAP/HCMAP dimension in xres/yres and reads it back through negative shifts (batch 2d)
* `vgacursoronly` -- VGA headless console: the OB-16 guard returns before the cursor-only tick can reposition the terminal cursor (batch 2d)
* `pxdmatail` -- PX COPYSPANS decodes span records past the bytes the bounded SRAM copy filled (batch 2d)
* `gifputcharovf` -- ps2_gif putchar: (24 + y*xsize)*4 overflows int before #108's bound; residual of the RESOLVED OB-28 (batch 2d)
* `pxfilladd` -- PX fill: int32_t lw + 1 overflows at INT32_MAX before the row loop (batch 2d)
* `lunaintshift` -- luna88k: signed 1 << 31 in the INT_ST_MASK read loop and the line-6 assert/deassert, and highestCurrentStatus << 29 for levels 4-6 (batch 2d)
* `kn02banameshift` -- kn02ba: 1 << i for i == 31 in the interrupt-name snprintf, the sibling #24 cast at :192 did not (batch 2d)
* `macesignedshift` -- MACE assert/deassert compute 1 << line in int; line 31 is registered and undefined (batch 2d)
* `autodevregorder` (test coverage) -- diff_autodev_gen.sh's ordered rows compare PROTOTYPE lines; the registration loops are a separate scrape no row observes (batch 2d)
* `lunad3diag` (test coverage) -- no row observes luna_intmask_probe.py's D3 diagnostic (its "kills a narrowed guard" sentence is ambiguous, not false) (batch 2d)
* `fdcdiagrows` (test coverage) -- CHANGELOG #20522's "asserted rather than assumed" fdc measurement has no committed carrier (batch 2d)
* `fileloaderrows` (test coverage) -- (no ECOFF/Mach-O/SREC/Android corpus row; gate_upstream.sh says so itself) (batch 2e)
* `ascaccountrows` (test coverage) -- (no committed row asserts NCR_TCL/NCR_TCM/NCRSTAT_TC) (batch 2e)
* `cuemapgap` (test coverage) -- (#127's "each regression-gated" CUE claims have no carrier; diff_diskimage_io.c routes reads away from the CUE path) (batch 2e)
* `modeselectrow` (test coverage) -- (no diff_diskimage_*.c row issues opcode 0x15) (batch 2e)
* `scsicaprow` (test coverage) -- (diff_diskimage_parse.c asserts the PARSER's count, never READ CAPACITY -- which is how `drecalccap` shipped past "advertised blocks exact"; discharged by... (batch 2e)
* `m88ktrapmask` -- tb0/tb1 build their bit mask with a signed 1 << d (undefined at d = 31); m88k_rot's (1 << n) - 1 is the same class (batch 3a, cpum88kinstr:F2)
* `mipslowrefrow` (test coverage) -- no committed row observes #278's `LOW reference` diagnostic (cpu_mips.c:2003, :2029-2037); the CHANGELOG's `Probe, 36/36 checks` names two test-first probe rigs that are not in the tree (batch 3b, cpumips:F2)  [title corrected: Astra afile_01, D:589 and fable_batch3b.md]
* `mipsaddiuub` -- ADDIU and seven addition sites across six fused handlers add two int32_t in signed arithmetic (UB on the wrap ADDIU is defined to perform) (batch 3b, cpumipsinstr:F3)  [title corrected: Astra afile_01, D:592, :617]
* `mipsjregionub` -- MODE32 J/JAL/JAL_trace: `page_base + (int32_t)arg[1]` overflows `int32_t` for a jump in the last two slots of page 0x7ffff000 (batch 3b, cpumipsinstr:F4)
* `leregrows` (test coverage) -- the LANCE observations the CHANGELOG cites (CHANGELOG.md:20714 at 7440e129: la_extra_reject, the #274 and #275 probes -- MISS, rmd1, tmd1, tmd3, CSR0) have no committed carrier: no regress file names the device (batch 3e, devle:F6)  [title corrected: Astra afile_01; corrected by Astra afile_05: the ruling's :20484 is that line's place at 8ea26abb]
* `pvrofssignedovf` -- PVR fb tick: `int vram_ofs` (DIWADDRL + y1*bytes_per_line, then per line) can overflow signed int BEFORE the unsigned % VRAM_SIZE -- undefined behaviour; the index is still masked, no out-of-bounds access shown (batch 3d, devpvr:F2)  [title corrected: Astra afile_01, D:724]
* `pvrrgbuninit` -- PVR TA: `wf_r/g/b[4]` are not zero-initialised (#12 covered x/y/z/u/v only); a textured strip's slide at :1407/:1411 copies indeterminate values (batch 3d, devpvr:F3)
* `pvrpaletteend` -- PVR texture sampler: the #55 clamp `addr > VRAM_SIZE-2` is sized for two-byte texels; it redirects the one legal one-byte sample at VRAM_SIZE-1 (8-bit palette, format... (batch 3d, devpvr:F5)
* `ppcmixedfx` (test coverage) -- no row raises a NEW FPSCR cause while a different one is already set, so the per-bit FX latch (cpu_ppc.c:1933-1946) is checked only for one cause repeated (batch 3d, cpuppc:F2)  [title corrected: Astra afile_01, D:731 and fable_batch3d.md]
* `pitonebytelatch` (test coverage) -- no PIT latch row programs a single-byte access format, so the one-read latch release (dev_8253.c:259-261) is unobserved (batch 3c, dev8253:F7)  [title corrected: Astra afile_01, D:788]
* `dbgexprambig` -- Breakpoint and watchpoint adds treat PARSE_MULTIPLE as success and then read the output (batch 3g, debuggercmds:F1)
* `findaddrwrap` -- Debugger memory search can wrap its scan address into low addresses (batch 3g, debuggercmds:F2)
* `findcountovf` -- Debugger search counts matches and unreadable chunks in unbounded signed ints (batch 3g, debuggercmds:F3)
* `dbgignorow` (test coverage) -- No committed row observes breakpoint ignore-count stops (batch 3g, debuggercmds:F5)
* `mipsbpnormrow` (test coverage) -- No committed row observes MIPS breakpoint sign-extension of an unextended address (batch 3g, debuggercmds:F6)
* `subsysbprow` (test coverage) -- No committed row arms a subsystem breakpoint and observes debugger entry (batch 3g, debugmsg:F2)
* `dbglisterow` (test coverage) -- No committed row observes the global break-on-ERROR listing after one subsystem is cleared (batch 3g, debugmsg:F3)
* `stepcallfocus` -- Changing machine focus leaves step-call running cached untraced handlers (batch 3g, bundle_debugger:F1)
* `netipurgptr` -- TCP reply checksum covers an urgent pointer the reply never stores (batch 3f, netip:F2)
* `netipseqarith` -- TCP sequence difference is a signed subtraction before the mismatch reject (batch 3f, netip:F3)
* `netipbcastmask` -- Broadcast mask shifts a signed 1 by an accepted prefix (batch 3f, netip:F4)
* `arcseekshift` -- ARC Seek retains a signed byte-decoding shift (batch 3h, arcbios:F2)
* `arcstdinlimit` -- ARC stdin Read overflows its signed loop counter at length 2147483647 (batch 3h, arcbios:F3)
* `irqcmaskshift` -- IRQ mask and unmask writes still use a signed 1 shifted by the guest selector (batch 3h, bundle_devices6:F1)
* `isopathptr` -- ISO path-table checks form pointers beyond one-past (batch 3h, bundle_disk:F1)
* `shdmteupper` -- OUTSTANDING_BUGS.md:8691-8694 at db8b1a33 -- the SH DMAC interrupt loop stops at DMAE (0x6c0) and omits DMTE4-7 (H'780-H'7E0), which exist on SH7750R/SH7751R (cpu_sh.c:447-448).  LOW today because nothing in the tree asserts any DMTE; it becomes MED when `sh4dmacintr` lands, and the loop is to be extended in that round (batch 3d, cpush:F5)  [Astra afile_01; corrected by Astra afile_05: D:719, fable_batch3d.md:62]
* `emulmkstempexit` -- emul.c:600-603 calls exit(1) when mkstemp fails -- a host temporary-directory failure ends the process (batch 3g)  [Astra afile_01, D:850 (the ruler's own addition)]
* `arcpartlba` -- OUTSTANDING_BUGS.md:2730-2731 at db8b1a33 -- the ARC partition LBA is multiplied by 512 in signed int and overflows (arcbios.c:1010-1017; it defeats the #168 bound) (batch 3h, arcbios:F1)  [Astra afile_01, D:952]


### THE HARNESS REVIEW -- 325 rows (wave 2, the regression harness)

#### `optpinor` (HIGH) -- check_optpin.py's optimisation pin can be satisfied without the property holding, two ways: either compile lane satisfies it (:93-98) and any `-fno-` flag matches (:52) -- so the memory_rw recursive split's stack growth stops being measurable
group 02, `hbundle_pipeline4:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [title corrected: grok's re-read (a) and Astra afile_07 (a); also covers group 02 hbundle_pipeline4:F2 (the id `optpinanyfno`, consolidated here: one check, two accepts)]

#### `asanexit1subtype` (HIGH) -- exit-1 subtype hidden by a constructing sibling
group 03, `hbundle_regress10:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `sgilwreadzero` (HIGH) -- narrow read of a zeroed window looks like the width decline
group 03, `hbundle_regress11:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt) establishes what the check does on a real emulator death and that the protected path declines today; it does not test Astra's regression argument. agy's own verdicts on that line (agy/agy_highfacts.txt:6), verbatim: "Q1: FAILS | Q2: NO LONGER | Q3: N/A" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `sgialiaspace` (HIGH) -- alias extractor misses aliases that contain a space
group 06, `regress24:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `countunreadable` (HIGH) -- count turns an unreadable log into zero matches
group 06, `regress24:F7` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `gateupstreamstatus` (HIGH) -- gate_upstream.sh run_case pipe to sed hides loader exit status
group 09, `hbundle_regress33:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `diagdivunaryop` (HIGH) -- diag_div_sweep divisor regex rejects unary operators and pointer dereference
group 09, `hbundle_regress33:F8` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:11): agy found no current missed guest-zero diagnostic division or offending unary/dereference divisor shape. agy's own verdicts on that line (agy/agy_highfacts.txt:11), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `diagdivchained` (HIGH) -- diag_div_sweep nonconst classifies chained division with leading constant divisor as constant
group 09, `hbundle_regress33:F9` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:12): agy found no current missed guest-zero chained diagnostic division. agy's own verdicts on that line (agy/agy_highfacts.txt:12), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `diagdivtruncarg` (HIGH) -- diag_div_sweep truncates arguments to 150 characters before nonconst classification
group 09, `hbundle_regress33:F10` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:13): agy found no current guest-zero diagnostic division beyond the classification cutoff. agy's own verdicts on that line (agy/agy_highfacts.txt:13), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `sgiat1count` (HIGH) -- sgi wr lat1 and rd lat1 pass when the second access exits
group 10, `hbundle_regress9:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:17): agy corroborates acceptance of process death and the current safe decline, without adjudicating the HIGH rule. agy's own verdicts on that line (agy/agy_highfacts.txt:17), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: N/A" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `probewiringinterpopt` (HIGH) -- check_probe_wiring.py ignores interpreter options preceding -c false-wiring probes passed as arguments
group 11, `hcheckprobewiring:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:18): agy establishes the false-wiring mechanism and found no current offending invocation shape. agy's own verdicts on that line (agy/agy_highfacts.txt:18), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `wirereassign` (HIGH) -- check_probe_wiring.py variable map ignores non-py assignments and ignores assignment order
group 11, `hcheckprobewiring:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [id corrected: Astra afile_03: the tie-break assigns this id, H:734; HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:19): agy establishes the stale-map mechanism, current BSC probe execution, and absence of the offending reassignment shape. agy's own verdicts on that line (agy/agy_highfacts.txt:19), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `probewiringheredocstrip` (HIGH) -- check_probe_wiring.py heredoc strip treats indented terminator as end of heredoc false-wiring body lines
group 11, `hcheckprobewiring:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:20): agy establishes the parsing mechanism and found no current probe-looking heredoc body. agy's own verdicts on that line (agy/agy_highfacts.txt:20), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `wdcchildstatus` (HIGH) -- row_null_atapi_st ignores non-zero child exit status and waitpid failure
group 13, `hdiffwdcidentify:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [id corrected: Astra afile_04: the tie-break assigns this id, H:853; HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:23): agy corroborates acceptance of nonsignalled process termination and the current safe decline, without adjudicating HIGH. agy's own verdicts on that line (agy/agy_highfacts.txt:23), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: N/A" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship; the NULL-transfer kill it guards is the existing row `wdcnullxfer`; accepting a nonsignalled process death is this row's own defect]

#### `hygienesweepmissing` (HIGH) -- With Python present, a missing diagnostic-division sweep is only noted and does not degrade the gate
group 13, `hgatehygiene:F7` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [id corrected: Astra afile_04: the tie-break assigns this id, H:856]

#### `sgideprimbitslive` (HIGH) -- dec b26-b31 and n25 line ignore liveness and exit status
group 17, `hsgideprimopprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [HIGH IS DISPUTED -- the grok seat's first-hand re-read says NOT HIGH (grok/grok_filehigh.txt: nothing live ends the process today); GPT-6 Astra HOLDS HIGH (afile_07): a fixed defect leaves the harness row HIGH if its faulty check would ACCEPT the protected process-ending or out-of-bounds regression, and no live instance is required where a preventive check DEMONSTRABLY misses the severe class it was shipped to catch -- an unrelated hypothetical severe consequence does not qualify.  agy's fact table (agy/agy_highfacts.txt:25): agy corroborates the discarded liveness/status predicate and current safe decline, without adjudicating HIGH. agy's own verdicts on that line (agy/agy_highfacts.txt:25), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: N/A" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  A RULE QUESTION for the flagship]

#### `gdromcondhow` (HIGH) -- gdrom_cond_probe.py's R1b and R2b rows pass on the announced byte alone (:419, :499) and never assert that the session survived, though the wait status is collected (:224-233) and asserted by their siblings R1 and R2 (:410-411, :493)
group 14, `hgdromcondprobe:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [the grok tie-break, HELD against Astra's FILED `ptywaitstatus` (grok_hopen3.txt: putting the status into the liveness verdict would leave :419 and :499 green, so it is the rows' own oracle, not the class); the lines read by the main loop at 7440e129; HIGH IS DISPUTED; THE KIND IS SETTLED -- GPT-6 Astra's confirmation had filed this finding under the existing class `ptywaitstatus` (hconfirm_14) and the grok seat held it as its own row (grok_hopen3.txt); asked again, Astra CONCEDED the kind (afile_09: :419 and :499 compare only the captured byte and consume neither `alive` nor `how`, so folding the status into the liveness verdict leaves them unchanged).  On the grade, grok under its own re-read test (grok/grok_filehigh3.txt): HIGH ONLY ON THE RE-INTRODUCTION RULE -- nothing on the live decline path ends the process; what the rows miss is the removed exit(1) being put back after the diagnostic prints -- which is the rule question of the ten disputed harness rows (GPT-6 Astra's rule, afile_07, grades such a check HIGH).  agy's facts for these two rows (agy/agy_highfacts2.txt:16), verbatim: "Q1: CAN PASS | Q2: NO LONGER | Q3: NONE FOUND" -- Q1 the check on a real emulator death, Q2 the protected path today, Q3 a live instance of the shape.  Filed HIGH with both positions; a RULE QUESTION for the flagship]

#### `cachecleanrdmask` (MED) -- cacheclean wrongregs fails #346's Rd check, so removing #345 still looks intact
group 01, `harmflagsprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [also covers group 13 hgatearm:F2 (the id `armcachecleanwrongregs`, consolidated here: one defect, two findings)]

#### `rotcsentinelc` (MED) -- rotated-immediate halt leaves the sentinel, whose carry bit is the expected 0
group 01, `harmflagsprobe:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `sentinelrawswap` (MED) -- three flag-probe sentinels compare the raw dump token deadbeef
group 01, `harmflagsprobe:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `geomparsercheck` (MED) -- the parser self-check never reaches the accepted-tuple compare
group 02, `hbundle_regress1:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `geomtypewitness` (MED) -- s: and i: rows do not witness the autodetection type guard
group 02, `hbundle_regress1:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `asanemptyalias` (MED) -- alias-less help line is neither parsed nor unparsed
group 03, `hbundle_regress10:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): no omitted selectable process-ending target is established]

#### `fbs3early` (MED) -- S3 samples IRQEnable before the FIQ decline pairs
group 03, `hbundle_regress10:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `guestrelbin` (MED) -- execvp leaves a relative binary path to resolve after chdir
group 03, `hbundle_regress11:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `pcc2ctlhang` (MED) -- genctl ctl scores a hung store as alive
group 03, `hbundle_regress12:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `hpchenumrc` (MED) -- subtype census ignores a failing -H status
group 03, `hbundle_regress13:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): the default witness still requires the measured construction aborts]

#### `sh4tmuirqidx` (MED) -- row_interrupt stays green if the pending increment is hardcoded to timer 0
group 04, `hbundle_regress14:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `rldiclvacrow` (MED) -- vacuous rldicl cell scores 0 for both the always-zero handler and the fix
group 04, `hbundle_regress15:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ppcdatahow` (MED) -- rlwimi and rldimi data sessions ignore a nonzero emulator exit
group 04, `hbundle_regress16:F2 + hbundle_regress17:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `timerhundredexpands` (MED) -- 100 Hz row stays green at a 1 kHz floor
group 05, `hbundle_regress18:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `fbslicehide` (MED) -- three 50-second slices hide the 42.95-second freeze
group 05, `hbundle_regress2:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `fbsignalcoverage` (MED) -- wall-time coverage does not establish callback progress
group 05, `hbundle_regress2:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `armcolddump` (MED) -- empty tlbdump satisfies the four cold PATH rows
group 05, `hbundle_regress2:F6` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `armwarmflags` (MED) -- warm PATH rows ignore host_load and host_store
group 05, `hbundle_regress2:F7` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `sgilosent2` (MED) -- halfword read of a zero register matches a decline
group 05, `hbundle_regress20:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `bgezfallstore` (MED) -- BGEZ rows score branched when both stores run
group 06, `regress21:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [also covers group 09 hbundle_regress32:F1 (the id `mipsbgezcontrol`, consolidated here: one defect, two findings)]

#### `mipsrihang` (MED) -- RI classification returns before a missing PC
group 06, `regress21:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): a progress-observation gap, not an established escape of the halt]

#### `bscd3clear` (MED) -- D3 accepts a cleared BCR2
group 06, `regress21:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `swpctxnoop` (MED) -- swpctx rows pass when the handler never saves
group 06, `regress23:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): the flags-to-PTBR clobber still fails the comparison]

#### `palgateabsent` (MED) -- palgate passes when the transcript has no user-mode text
group 06, `regress23:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): the privilege rejection prints the searched text before it stops the CPU]

#### `mk48howdrop` (MED) -- clock and signature rows ignore session how
group 06, `regress24:F6` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `sh4rptincompleterun` (MED) -- sh4_tlbda2_probe RPT/RPTu and sh4_sci_probe RPT/RPT1 discard guest execution got/completion
group 07, `hbundle_regress26:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `pcc2byterdovw` (MED) -- legal-width byte row scores the RAM word that overwrites r4
group 08, `hbundle_regress29:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `armfoldp1hide` (MED) -- pass 1 values conceal missing pass-2 register loads
group 08, `hbundle_regress3:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `armfastrotxor` (MED) -- fast-path rotation loss is overwritten before the XOR
group 08, `hbundle_regress3:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `armxchgname` (MED) -- unset _xchg_pos NameError becomes a clean-slate SKIP
group 08, `hbundle_regress3:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `mipsrp54host` (MED) -- 2^54+7 RP and negative RM match host nearest
group 08, `hbundle_regress30:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [also covers group 09 hbundle_regress32:F2 (the id `cvtroundingrprm`, consolidated here: one defect, two findings)]

#### `m88kdumptail` (MED) -- address tail regex accepts any hex prefix before 20000
group 08, `hbundle_regress30:F8` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `m8invreadrc` (MED) -- repro_m8invread returns 0 after a failed read-back control
group 08, `hbundle_regress31:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `upstreambinarydiff` (MED) -- gate_upstream.sh diff grep parser returns 0 on binary diff
group 09, `hbundle_regress33:F6` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `sh4c7fetch` (MED) -- C7's user-mode P1 fetch never issues the P4 access it claims to bound
group 10, `hbundle_regress7:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): W1 separately observes the device-death symptom]

#### `sh4hangoracle` (MED) -- sh4pcic killed() scores a hang that printed the diagnostic as the guest exit
group 10, `hbundle_regress7:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): a genuine diagnostic-bearing death still satisfies the witness]

#### `shfmovalign` (MED) -- fmovd r0idx addresses are 8-aligned, so mask 3 and mask 7 are the same check
group 10, `hbundle_regress8:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `pittickabsent` (MED) -- pit R3 treats missing F r6/r7 as divisor 65535, and empty T passes
group 10, `hbundle_regress8:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `shhaltsilent` (MED) -- five sh_halt survival rows accept an open pty that never dumps
group 10, `hbundle_regress8:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): an observed EOF or error becomes HOSTEXIT and fails the survival rows]

#### `pitcounteraxis` (MED) -- pit C1/C2/A1/E/A2 never run on MMU-off arms W and X
group 10, `hbundle_regress8:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `diskwritefullstore` (MED) -- SCSI write onto full store aims past capacity and cannot test backing store write failure
group 11, `hdiffdiskimageio:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `fbforkstatus` (MED) -- diff_footbridge F1/G1 ignore fork/waitpid failure, laundering st=0 into survived
group 12, `hdifffootbridge:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): an observed signal or nonzero exit still fails the survival predicate]

#### `ieeesliverinf` (MED) -- diff_ieee_store sliver below 2^128 tests exactly 2^128, passing pre-#292 truncation
group 12, `hdiffieeestore:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ieeeinfrnvac` (MED) -- diff_ieee_store inf +Inf+1.0 RN passes with isfinite guard removed due to RN overflow
group 12, `hdiffieeestore:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ieeequantumband` (MED) -- diff_ieee_store quantum band rows pass under old 2^-1018 guard due to host fma underflow
group 12, `hdiffieeestore:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ieeesignmustdiffer` (MED) -- diff_ieee_store must_differ lower bound omits negative doubles below 2^-149
group 12, `hdiffieeestore:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ieeedsubsweep` (MED) -- diff_ieee_store D sweep only counts differences, missing D subnormal bit-forcing mutants
group 12, `hdiffieeestore:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `m88forkprobe` (MED) -- diff_m8820x probe ignores fork/waitpid errors, laundering failure to survived
group 12, `hdiffm8820x:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): collected nonzero exits and signals still fail rows]

#### `m8inve9astorevac` (MED) -- diff_m8invread E9a cannot fail on store deletion because fresh() zeroes register
group 12, `hdiffm8invread:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `m8invcpuoneowner` (MED) -- diff_m8invread does not verify CPU 1 target on CPU 1 owner writes, allowing hardcoded CPU 0
group 12, `hdiffm8invread:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdcopcodealloc` (MED) -- row_every_opcode_resets skips failed allocations without tracking executed count
group 13, `hdiffwdcidentify:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdcphasefixture` (MED) -- mid-transfer rows stage 10 bytes and push is refused so dispatch equality 12 never reached
group 13, `hdiffwdcidentify:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [id corrected: Astra afile_04: the tie-break assigns this id, H:854]

#### `wdcstalephasepkt` (MED) -- row_stale_phase_write resets phase to 0 so dispatch packet-flag removal passes
group 13, `hdiffwdcidentify:F4` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdcsoftresetflush` (MED) -- soft reset flushes ring check runs after packet command already emptied occupancy to zero
group 13, `hdiffwdcidentify:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdcblock0survive` (MED) -- block 0 survival check tests tail byte which drop-newest producer guard never overwrites
group 13, `hdiffwdcidentify:F6` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `fbdrainl2stale` (MED) -- row L2 accepts accrual-era O_VEND and probe terminates on phase 3 before post-drain read
group 13, `hfbpendingdrainprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `fbdrainloadpass` (MED) -- accrual deliver under 763 callbacks yields backlog under 763 passing expect-cap on unbounded timer
group 13, `hfbpendingdrainprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `hygieneasczero` (MED) -- zero-length pattern matches no emittable string in src/ as dev_asc.c:599 emits data_out_len == 0
group 13, `hgatehygiene:F9` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `hygienepmaxrawpanic` (MED) -- pmax console sets bit 7 on characters so raw grep for panic matches nothing in PLOG
group 13, `hgatehygiene:F10` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdcslavegeomgrep` (MED) -- gate_offline slave geometry grep matches capacity-only string
group 14, `hgateoffline:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `gdroma88zeroinit` (MED) -- gdrom_cond_probe R10b tests cond preservation from zero pre-state, missing cond clearance
group 14, `hgdromcondprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `gdromacceptseed` (MED) -- Unseeded DMA destination can satisfy accept data without a copy
group 14, `hgdromdefaultprobe:F3` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `siuparenarith` (MED) -- S1 accepts parenthesized arithmetic in VRIP_INTR_SIU
group 15, `hhpcmipsctorprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `hpcenumstatus` (MED) -- enumerate_subtypes discards _run exit status allowing partial -H output
group 15, `hhpcmipsctorprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [sev corrected: grok's first-hand re-read (grok/grok_filehigh.txt) said NOT HIGH; Astra CONCEDED MED (afile_07); agy's facts agree (agy/agy_highfacts.txt): enumerated construction aborts still fail A3-A5]

#### `lcaabsentpass` (MED) -- Differential rows and ofs1 zero pass when both readings are absent
group 15, `hlcaisalaneprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `lunabreaktmo` (MED) -- cont_until_breakpoint ignores cleanup prompt wait and launders timeouts into non-delivery
group 15, `hlunaabsentcpuprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `lunaothersidle` (MED) -- others idle23 accepts None as evidence of inactive CPUs
group 15, `hlunaabsentcpuprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `ppclfsupreload` (MED) -- PowerPC lfsu/lfdu value rows preload f1 with expected result
group 16, `hppcroundingprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdctimeoutscore` (MED) -- breakpoint timeout scored as measured failures and emits done sentinel
group 18, `hwdcaddtoinbufprobe:F1` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `wdccontrol0discard` (MED) -- control 0 disassembly check failures are printed but discarded without affecting probe outcome
group 18, `hwdcaddtoinbufprobe:F2` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`

#### `hygieneartifactlive` (MED) -- gate_hygiene's blanket `! -path artifacts/*` hides the live promptless pty probe gdrom_pio_null_probe.py from its census
group 13, `hgatehygiene:F5` -- `regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`  [Astra afile_04: both seats make it NEW, so the tie-break's grade governs and the derived index was wrong to call it OPEN, H:852]

#### `astraharnesslow` (LOW, a CLASS row) -- the 237 LOW rows of wave 2, the regression harness, one line each; a row is promoted to its own ledger row when a round takes it up
`regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md`; the table with each row's governing text: `regress/artifacts/astrafiling_20261002/FILING.tsv`.

* `flagspinmajority` -- arm_flags header says the table is mostly pins and that two subtracts were already right (group 01, harmflagsprobe:F8)
* `mvnsrot0disc` -- two MVNS rows are labeled DISC but both builds produce the same result (group 01, harmflagsprobe:F9)
* `asanrecovercomment` -- build_asan comment says recovery is on; the flags never enable it (group 01, hbuildasan:F2)
* `asanchmodcomment` -- build_asan says configure is untracked-mode and fails 126 without chmod (group 01, hbuildasan:F3)
* `dashccluster` -- dollar guard misses bash -cl and bash -e -lc (group 01, hbundle_hooks:F1)
* `heredocopener` -- dollar guard strips a heredoc opener's trailing command and the body bash runs (group 01, hbundle_hooks:F2)
* `quoteconcat` -- dollar guard stops at the first quote of an adjacent-quote concatenation (group 01, hbundle_hooks:F3)
* `dollarpastsemi` -- unquoted wsl -c reader consumes commands after the semicolon (group 01, hbundle_hooks:F4)
* `dollarbslashnl` -- dollar guard splits backslash-newline continuations before matching wsl -c (group 01, hbundle_hooks:F5)
* `dollarprose` -- dollar guard flags documentation and inline comments as wsl invocations (group 01, hbundle_hooks:F6)
* `wakeupstampshare` -- wakeup stamp has no session id and the tmp fallback is cross-project (group 01, hbundle_hooks:F8)
* `wakeupstampsticky` -- consumed wakeup stamp still suppresses the re-arm reminder for 900s (group 01, hbundle_hooks:F9)
* `citeprefixblind` -- citation gate ignores the changelog prefix and every ## Round #N heading (group 01, hbundle_pipeline1:F1)
* `blocksgarbagevacuous` -- zero-heading selftest checks the parser, not the fail branch it was added to guard (group 01, hbundle_pipeline1:F2)
* `trackedsubstring` -- cited-artifact tracked() keys off the literal directory name GXEMUL-SEC (group 01, hbundle_pipeline1:F3)
* `citeclassifycomment` -- cited-artifact header still says untracked hits are classified and greened (group 01, hbundle_pipeline1:F4)
* `refusalafteranswer` -- dashboard omits a refused exemption once that seat has an ordinary answer (group 01, hbundle_pipeline1:F7)
* `hlinetipclip` -- header tooltip is positioned below an overflow-hidden hline (group 01, hbundle_pipeline1:F8)
* `wallcountsasanswer` -- untokened WALL counts as a stage answer (group 02, hbundle_pipeline2:F1)
* `holdqblank` -- hold-only stage stores a blank date and skips the question failure (group 02, hbundle_pipeline2:F2)
* `censusline` -- exit census counts lines, and zero sites pass (group 02, hbundle_pipeline2:F3)
* `censusbucket` -- exit attribution can bind a helper to the previous function (group 02, hbundle_pipeline2:F4)
* `rowgitstatus` -- row-state git status is discarded (group 02, hbundle_pipeline2:F5)
* `rowqueueos` -- unreadable queue becomes an empty pass (group 02, hbundle_pipeline2:F6)
* `rowheadingsev` -- severity parenthetical hides a queue heading (group 02, hbundle_pipeline2:F7)
* `wallmarkerdrop` -- trailing-comma hold is omitted and the wall stays green (group 02, hbundle_pipeline2:F8)
* `wallrowcount` -- The committed ledger derives 26 held rows containing 28 phases. The printed ‘held stages’ count counts rows. The stale stored wall separately contains 25 rows and 34... (group 02, hbundle_pipeline2:F9)
* `scoreerasub` -- era skip treats 8-row as present inside 18-row (group 02, hbundle_pipeline2:F11)
* `scorepincomment` -- a commented gate pin still counts as coverage (group 02, hbundle_pipeline2:F12)
* `emptywitnessgf` -- a row with no entries is grandfathered before the witness shape check (group 02, hbundle_pipeline3:F1)
* `witnessext` -- witness existence ignores .out and directories (group 02, hbundle_pipeline3:F2)
* `seatsreaddirskip` -- a missing or ambiguous panel directory still passes (group 02, hbundle_pipeline3:F3)
* `seatsreadsubstr` -- answer filenames match as substrings (group 02, hbundle_pipeline3:F4)
* `seatsreadcross` -- one ledger blob credits every filename in every panel it names (group 02, hbundle_pipeline3:F5)
* `hookstderrfire` -- stderr alone satisfies a must-fire hook control (group 02, hbundle_pipeline3:F9)
* `hookctlcopy` -- precommit runs the artifact hook suite, not this file (group 02, hbundle_pipeline3:F10)
* `exitcensusline` -- two calls on one line count as one live call (group 02, hbundle_pipeline3:F11)
* `exitcensusstr` -- a string containing exit(1) counts as a live call (group 02, hbundle_pipeline3:F12)
* `seatcovstem` -- suffixed panel directories miss the citation key (group 02, hbundle_pipeline3:F14)
* `seatcovkimi` -- ollama_kimi.txt does not count as the kimi seat (group 02, hbundle_pipeline3:F15)
* `seatcovperseat` -- coverage is credited once per seat, not per file (group 02, hbundle_pipeline3:F16)
* `codexrefusaltail` -- a refusal string in the tail is counted even when a verdict follows (group 02, hbundle_pipeline4:F3)
* `codexcrop` -- cropped answer blocks are printed without a truncation notice (group 02, hbundle_pipeline4:F4)
* `floodcheckdead` -- census_floods --check always returns success (group 02, hbundle_pipeline4:F5)
* `floodlatchgroup` -- latch census collapses every warned_* name to one (group 02, hbundle_pipeline4:F6)
* `floodstaleprint` -- flood census still says the WDC command diagnostic is unlatched (group 02, hbundle_pipeline4:F7)
* `wsldollarline` -- a continued wsl -c dollar is invisible (group 02, hbundle_pipeline4:F8)
* `wsldollaros` -- an unreadable tracked file counts as scanned and passes (group 02, hbundle_pipeline4:F9)
* `boilernotes80` -- identical post-cutoff notes under 80 characters are skipped (group 02, hbundle_pipeline4:F11)
* `boilerheader` -- boilerplate header says it is outside the hard gate (group 02, hbundle_pipeline4:F12)
* `geomtmpshare` -- geometry self-mutants share /tmp/geom_N.img (group 02, hbundle_regress1:F3)
* `wdcprobering` -- flood-probe header still says the ring never compares pointers (group 02, hbundle_regress1:F7)
* `geomonlyround` -- rounding comments call two rows the only discriminators (group 02, hbundle_regress1:F8)
* `geomonly80` -- the 160-cylinder row is not the only non-80 floppy expectation (group 02, hbundle_regress1:F9)
* `wdcprobecountonly` -- flood-probe contract calls value-checked sites count-only (group 02, hbundle_regress1:F10)
* `geomstubfive` -- the geometry differential's stub comment says five (group 02, hbundle_regress1:F11)
* `asanpri127` -- pristine status 127 scored as a clean baseline when HEAD is clean (group 03, hbundle_regress10:F2)
* `fbd1empty` -- D1 scores zero mismatches when no arm reached a prompt (group 03, hbundle_regress10:F4)
* `asanbaddate` -- ab_expired accepts an impossible date that sorts after today (group 03, hbundle_regress10:F7)
* `arcshiftcomment` -- gate comment still says a quoting comment reddens the shift census (group 03, hbundle_regress10:F9)
* `guestshglue` -- luna88k answer does not exercise the #287 arms (group 03, hbundle_regress11:F5)
* `sgiretailclaim` -- early return 1 still completes the load as zero (group 03, hbundle_regress11:F6)
* `sgirexbit12` -- tex xbit does not prime SGIRE_W_BADCOLOR (group 03, hbundle_regress11:F7)
* `sgipadbound` -- a 17-character row name still matches the two-space gate pattern (group 03, hbundle_regress11:F8)
* `sh4stepfatal` -- stepped rows cannot tell fatal() from debug() (group 03, hbundle_regress12:F2)
* `sh4l1fresh` -- L1's two words share DM latch bit 8 (group 03, hbundle_regress12:F6)
* `sh4x4channel0` -- X4 says every other row drives channel 0 (group 03, hbundle_regress12:F7)
* `pcc2contractstale` -- the PCC2 c040 probe's header still says it is not a detector of the repair (group 03, hbundle_regress12:F8)  [title corrected: Astra afile_02, H:187, :204]
* `pcc2diffsite` -- parenthetical says the return-mutant comment names a different site (group 03, hbundle_regress12:F9)
* `hpcgitstatus` -- P3 treats empty git-status stdout as a clean tree (group 03, hbundle_regress13:F3)
* `hpcirqcomment` -- comment irq= tokens are scored as bad construction arms (group 03, hbundle_regress13:F5)
* `hpcfixedunsat` -- expect-fixed cannot be true while S2 and C7 hold (group 03, hbundle_regress13:F6)
* `alphacastrow` -- tbia/tbiap obs do not detect dropping the signed casts (group 03, hbundle_regress13:F8)
* `alphapagezero` -- header still says HEAD TBIA/TBIAP flushes only page zero (group 03, hbundle_regress13:F10)
* `sgiheadrgba` -- sgi fill-top comment still says the RGBA row fails on HEAD (group 04, hbundle_regress14:F4)
* `sgicopycount` -- copy-4th comment counts twelve preceding rows; the file has fifteen (group 04, hbundle_regress14:F5)
* `sh4tmuself18` -- selfcheck still says 12 of 18 after the row count became 19 (group 04, hbundle_regress14:F6)
* `sh4tmuuniecause` -- selfcheck credits the UNIE guard with an UNF change the guard does not make (group 04, hbundle_regress14:F7)
* `sh4tmuunder0` -- three-timer comment calls the underflow case no underflow (group 04, hbundle_regress14:F8)
* `gdromiprdhalf` -- gdrom comment still says SH4_IPRD ignores a halfword (group 04, hbundle_regress15:F8)
* `gdromexitcount` -- gdrom comment still counts three live exit(1) sites in the access function (group 04, hbundle_regress15:F9)
* `gdromwarnednine` -- gdrom comment still says nine warned writers, six of them reads (group 04, hbundle_regress15:F10)
* `ppcmsrsfheader` -- rlwimi and rldimi headers say MSR[SF]=1; startup leaves MSR zero (group 04, hbundle_regress16:F3 + hbundle_regress17:F5)
* `memrwsh1kflag` -- memory differential says SH 1KB pages return MEMORY_NOT_FULL_PAGE (group 04, hbundle_regress16:F4)
* `memrwnumclaim` -- memory differential still says every real row compares numbers (group 04, hbundle_regress16:F5)
* `memrwpage4096` -- F1 comment predicts 4096 host lookups; the granule yields 16384 (group 04, hbundle_regress16:F6)
* `mfolddevstall` -- mlw2_dev_tm64 scores (1,0) on a timed-out first pass (group 04, hbundle_regress17:F2)
* `rldimisrcnote` -- rldimi comment says rS is always r3; the alias word uses r8 (group 04, hbundle_regress17:F6)
* `asicgroupzero` -- group-zero predicate described as the other fifteen groups (group 05, hbundle_regress18:F5)
* `asiccaselabel` -- duplicate case label described as an invisible misroute (group 05, hbundle_regress18:F7)
* `asicguesttrig` -- guest event path described as unreachable (group 05, hbundle_regress18:F8)
* `asicirq13drop` -- adjacent latch described as dropping IRQ13 (group 05, hbundle_regress18:F9)
* `rgbsetupsig` -- setup() described as hardcoding destination mode (group 05, hbundle_regress18:F10)
* `rgblowbyte` -- correct RGB GET predicted as 0xaabbccdd (group 05, hbundle_regress18:F11)
* `rgbtlbindex` -- TLBA_TILE<<32 described as index 2 (group 05, hbundle_regress18:F13)
* `rgbimplies` -- chan and not-corrupt described as independent (group 05, hbundle_regress18:F14)
* `rgbsamemode` -- same-mode row described as proving padding discard (group 05, hbundle_regress18:F15)
* `timerinitfreq` -- timer_freq init attributed to timer_start (group 05, hbundle_regress18:F17)
* `timerstopzero` -- double-stop row described as passing an always-report timer (group 05, hbundle_regress18:F19)
* `wdcbpecho` -- breakpoint-hit flag matches the breakpoint add command (group 05, hbundle_regress19:F2)
* `wdctrl0print` -- control-0 disassembly count is only printed (group 05, hbundle_regress19:F3)
* `fbarmdirect` -- arm() described as using the register handler (group 05, hbundle_regress19:F7)
* `shprioscore` -- prio<=1 mutant described as passing all six rows (group 05, hbundle_regress19:F8)
* `fbfiveglobals` -- four globals, five definitions (group 05, hbundle_regress19:F9)
* `fbbadisprint` -- arm A disassembly mismatches are only printed (group 05, hbundle_regress2:F3)
* `armresidue3` -- four load legs described as residue 2 (group 05, hbundle_regress2:F11)
* `armlivenostm` -- liveness control described as an LDM/STM round-trip (group 05, hbundle_regress2:F12)
* `sgidelenword` -- decline rows require wording the contract says is free (group 05, hbundle_regress20:F5)
* `sgiderowcount` -- 25-row kill table described as every current row (group 05, hbundle_regress20:F6)
* `sgidebitspan` -- six primed bits described as the whole warning enum (group 05, hbundle_regress20:F8)
* `gdromfreshfour` -- overread described as a one-instruction fresh-machine site (group 05, hbundle_regress20:F9)
* `gdromfirsttouch` -- first DATA touch described as illegal in every state (group 05, hbundle_regress20:F10)
* `gdromexitassign` -- remaining host exits assigned to two removed rows (group 05, hbundle_regress20:F11)
* `bscbeconf` -- BE config path is shared and unlinked (group 06, regress21:F5)
* `alphaldcsign` -- load_const self-test duplicates its own formula (group 06, regress23:F1)
* `idlequietempty` -- A idle quiet passes on an empty failed session (group 06, regress23:F4)
* `buildverdsnap` -- stale-verdict snapshot absorbs a check placed before it (group 06, regress24:F2)
* `armmultitxt` -- build sync inventory skips cpu_arm_multi.txt (group 06, regress24:F4)
* `buildpubstat` -- a failed publication copy still exits 0 (group 06, regress24:F5)
* `lunabackhard` -- both-backstop luna run still fails the 1:1:1 check (group 06, regress24:F12)
* `mk48midnight` -- one gmtime sample is reused across the midnight boundary (group 06, regress24:F13)
* `logdirrel` -- relative LOGDIR splits the progress log across the image chdir (group 06, regress24:F14)
* `ftrcneghalf` -- ftrcD-neghalf boundary row in sh_rounding_probe cannot detect invalid arm or pre-fix cast (group 07, hbundle_regress25:F1)
* `r418parsetmp` -- diff_diskimage_parse hardcodes shared temporary directory /tmp/r418parse causing collisions (group 07, hbundle_regress25:F5)
* `armbfxencok` -- BFX encoding check shares the encoder’s opcode-base constants and cannot independently validate their identity (group 07, hbundle_regress26:F3)
* `alphawalkfound` -- alpha_pfnoffset_probe walk found reports ok on empty session text (group 07, hbundle_regress27:F1)
* `lunasteptimeout` -- luna_intmask_probe attributes send timeout to pre-fix process death without checking dead status (group 07, hbundle_regress27:F5)
* `absorbgreedykeep` -- selftest_absorb greedy check uses multiline fixture that dot cannot span (group 07, hbundle_regress28:F4)
* `rtcsrsentinel` -- RTCSR interrupt rows accept a dump after SIGINT with no sentinel (group 08, hbundle_regress29:F2)
* `autodevrunst` -- run_gen returns success whenever autodev.c already exists (group 08, hbundle_regress29:F4)
* `rtcsra1cmf` -- A1 0x39 intersects neither the current guard nor a CMF-widened guard (group 08, hbundle_regress29:F5)
* `lcaconf2of6` -- IOC_CONF idata-and-3 makes the kill rows fail on corrected HEAD (group 08, hbundle_regress29:F7)
* `autodevnoglob` -- the noglob mutant still trips the character regex, via `*` and `input.` (group 08, hbundle_regress29:F8)  [title corrected: Astra afile_03, H:475]
* `autodevsort` -- registration order is sorted before lookup and dumplist (group 08, hbundle_regress29:F9)
* `armwbplus5` -- post-index +5 walks by 4 and is not a livelock (group 08, hbundle_regress3:F7)
* `armwbbyte` -- the byte PIN row is not a word form (group 08, hbundle_regress3:F8)
* `armwbname32` -- two literal spaces keep a full 32-column name satisfiable (group 08, hbundle_regress3:F9)
* `armgateskip` -- comment says gate_skip swallows failures that #371 made exit 1 (group 08, hbundle_regress3:F10)
* `armfoldret` -- session() docstring names a return value it does not return (group 08, hbundle_regress3:F11)
* `sgieaddrto` -- V8 scores a peek timeout as the abort control's non-arrival (group 08, hbundle_regress30:F1)
* `wdclatchanysite` -- latch census stays balanced when one of two guard pairs is removed (group 08, hbundle_regress30:F3)  [also covers group 14 hgateshrounding:F3 (the id `wdclatchpairdrop`, consolidated here: one defect, two findings)]
* `absorbmclean` -- cleanup deletes the entire work/m tree, including caller files (group 08, hbundle_regress30:F6)
* `chcrxor7` -- S5 is seven bits from S4 and one bit from C2 (group 08, hbundle_regress30:F10)
* `sciprime` -- SCI comment requires a prime the first low store already provides (group 08, hbundle_regress30:F11)
* `scic2eighth` -- C2 comment still says the protocol where the file tests the eighth pulse (group 08, hbundle_regress30:F12)
* `scithreek` -- section header says two kills and the loop has three (group 08, hbundle_regress30:F13)
* `rtcsc2same` -- C2's CMF write is discarded, so it matches C1's zero (group 08, hbundle_regress31:F7)
* `flushbandmiss` -- flushband anchor removes only the FP_SUBNORMAL encode call (group 08, hbundle_regress31:F8)
* `revert287finite` -- revert287 else-branch stores the largest finite value, not the old NaN (group 08, hbundle_regress31:F9)
* `diffelevenstale` -- self-test still says one of eleven differentials (group 08, hbundle_regress31:F10)
* `inactivityresethole` -- selftest_inactivity leg 3 accepts production files with clock reset assignment deleted (group 09, hbundle_regress32:F3)
* `sh4storeattribution` -- SH4 STORE witness cannot identify which access ended the session (group 09, hbundle_regress32:F4)  [id corrected: Astra afile_03: the tie-break assigns this id, H:589]
* `selftestbudgetstatus` -- selftest_budget discards wrapper subprocess exit status (group 09, hbundle_regress32:F6)
* `inactivityloadflake` -- selftest_inactivity slow-but-progressing leg has 120ms host-load deadline (group 09, hbundle_regress32:F7)
* `selftestbudgetskip` -- gate_offline.sh fails when selftest_budget skips on missing images (group 09, hbundle_regress32:F8)
* `m8820xtimeoutdrop` -- m8820x_sites_probe send() drops timeout argument when calling wait() (group 09, hbundle_regress32:F9)
* `logdirinheritenv` -- selftest_logdir child shell preserves caller exported LOGDIR on bare assignment (group 09, hbundle_regress33:F1)  [also covers group 14 hgateoffline:F2 (the id `logdirinhexfail`, consolidated here: one defect, two findings)]
* `selftestlogdirstatus` -- gate_offline.sh discards selftest_logdir exit status and ignores driver_ran (group 09, hbundle_regress33:F2)  [also covers group 14 hgateoffline:F1 (the id `logdirlaunder`, consolidated here: one defect, two findings)]
* `logdirreturncode` -- selftest_logdir ignores subprocess returncode when wrapper killed (group 09, hbundle_regress33:F3)
* `runshselectorpad` -- run.sh string match skips zero-padded gate selector that passed validation (group 09, hbundle_regress33:F4)
* `mipslogpublishstale` -- gate_mips.sh skip or preflight death leaves stale published pty logs for gate 6 (group 09, hbundle_regress33:F13)
* `disksyncforkspin` -- diff_diskimage_sync spins infinitely in waitpid loop if fork fails (group 09, hbundle_regress4:F4)
* `fbctrldisasmnosteps` -- fbctrl_port_probe disassembly check passes vacuously on NO-PROMPT sessions (group 09, hbundle_regress5:F3)
* `ldrddocblind` -- ldrd_pc_prog docstring still says the aligned pair distinguishes a +4 base (group 10, hbundle_regress6:F4)
* `wdcphasecount` -- altoffset header counts two differential rows; s4 s5 t5 t6 are four (group 10, hbundle_regress6:F5)
* `wdczerooracle` -- emit()'s comment falsely says a zero register value would pass; all 36 expected values are nonzero (group 10, hbundle_regress6:F6)  [title corrected: Astra afile_03, H:602, :629]
* `wdcpadwidth` -- altoffset %-56s comment says the width truncates; Python minimum width does not (group 10, hbundle_regress6:F7)
* `wdcexemptdate` -- altoffset header still says the wiring exemption ends 2026-09-20 (group 10, hbundle_regress6:F8)
* `sh4sixguard` -- sh4pcic comment says six value guards; the loop has seven (group 10, hbundle_regress7:F4)
* `sh4nopexec` -- sh4pcic says the NOP 0x0009 is executed; write_arm steps only the store (group 10, hbundle_regress7:F5)
* `m88kfrz10eq` -- trapfrozen10 blurb still calls the re-route equivalent (group 10, hbundle_regress7:F6)
* `m88ktailtext` -- TAILHALT glossary requires a stop; the classifier tests the text only (group 10, hbundle_regress7:F7)
* `pitlsbiff` -- pit rewind comment swaps which byte is the LSB (group 10, hbundle_regress8:F7)
* `shxdseed` -- sh_halt XD comment says both rows seed both banks; only the store does (group 10, hbundle_regress8:F8)
* `pitsendto` -- pit send() drops the timeout its step and reg calls pass (group 10, hbundle_regress8:F9)
* `xscaldiedor` -- xscale exit-1 controls pass on exit 0 or a signal when the text is present (group 10, hbundle_regress9:F3)
* `sgixwin7doc` -- sgi contract says window-bit collisions are uncaught; xwin7 pre fails on one (group 10, hbundle_regress9:F4)
* `sgiverblen` -- sgi mutant W comment says the removed catch-all tested len != 8 (group 10, hbundle_regress9:F5)
* `panelchildstatus` -- Child exit status discarded by wait allows mid-review child crash to pass as answered (group 11, hbundle_tools1:F2)
* `ollamathinkburn` -- panel_ollama.py wrapper surfaces unverified thinking text as answer when both attempts return empty response (group 11, hbundle_tools1:F7)
* `ollamaretrybody` -- HTTPError response body dropped on retry in panel_ollama.py discarding usage limit explanation (group 11, hbundle_tools1:F8)
* `hygieneuntrackedhelper` -- Untracked Python helper without pty.fork affects census counts while bypassed by untracked check (group 11, hbundle_tools1:F9)
* `nightlycheckagearg` -- Non-numeric MAX_AGE_H causes test syntax error and falls through to ok verdict (group 11, hbundle_tools1:F15)
* `nightlycheckheadunknown` -- nightly_check.sh accepts HEAD=UNKNOWN as valid attributable commit SHA (group 11, hbundle_tools1:F16)
* `adjudcontentcheck` -- adjudicate.sh size-only check counts long OLLAMA_SEAT_ERROR or recovered thinking as answered (group 11, hbundle_tools2:F2)
* `adjudzeroexit` -- adjudicate.sh exits zero when all adjudicators fail and can read stale output files (group 11, hbundle_tools2:F3)
* `propagateskipall` -- propagate_all_trees.sh skips all trees on new file absent from targets and exits zero (group 11, hbundle_tools2:F4)
* `propagateunbuilt` -- propagate_all_trees.sh classifies build tree lacking binary as source twin and skips build (group 11, hbundle_tools2:F5)
* `batteryrootexport` -- nightly_battery.sh unexported ROOT allows child run.sh and lib.sh to fall back to hardcoded default (group 11, hbundle_tools2:F7)
* `gitstatuslaunder` -- Empty output on failed git status reported as clean working tree in nightly_battery.sh and FIRST-RUN-CHECK.sh (group 11, hbundle_tools2:F8)
* `firstrunexitcode` -- FIRST-RUN-CHECK.sh prints FAIL count but final echo causes zero exit status (group 11, hbundle_tools2:F11)
* `firstruncheckempty` -- FIRST-RUN-CHECK.sh divergence check selects nothing on empty source tree and reports pass (group 11, hbundle_tools2:F12)
* `firstrundiffsallow` -- FIRST-RUN-CHECK.sh divergence check accepts arbitrary mismatched C files and excludes Makefile.skel (group 11, hbundle_tools2:F13)
* `hookspathoverride` -- install_hooks.sh hardcodes .git/hooks path ignoring git core.hooksPath configuration (group 11, hbundle_tools2:F15)
* `hookswritefailure` -- install_hooks.sh ignores write and chmod failures and reports success (group 11, hbundle_tools2:F16)
* `hookscommentclobber` -- install_hooks.sh ownership check matches precommit_check.sh in comment clobbering foreign hooks (group 11, hbundle_tools2:F17)
* `inlinediffhunkregex` -- inline_diff.sh hunk regex fails to match markdown list items or blank line diffs (group 11, hbundle_tools2:F21)
* `probewiringdupquotes` -- check_probe_wiring.py duplicate key check regex matches double quotes only missing single-quoted duplicate dict keys (group 11, hcheckprobewiring:F5)
* `probewiringspacefile` -- check_probe_wiring.py git ls-files whitespace split drops filenames containing spaces from domain (group 11, hcheckprobewiring:F6)
* `diffdiskfflushfsize` -- Unflushed image streams can blunt redundant file-size assertions (group 11, hdiffdiskimageio:F3)
* `diffdisksharedworkdir` -- Hardcoded shared /tmp/r411c1/work directory has no creation logic and risks concurrent fixture collision (group 11, hdiffdiskimageio:F4)
* `wdcannouncelax` -- announcement assertions check first < 1 and other < 1 accepting multiple emissions (group 13, hdiffwdcidentify:F10)
* `wdcaltctlmemleak` -- row_orphan_altctl reinitializes third fixture without freeing second buffer leaking 262656 bytes (group 13, hdiffwdcidentify:F11)
* `fbdrainfastcollapse` -- Fast-mode freeze retains control 0x80, runs at 2.98 Hz, and a subsequent callback can collapse remaining debt to 1 (group 13, hfbpendingdrainprobe:F3)
* `hygienemarkassign` -- conv_mark checks call to wait(mark=_mark) but never checks that _mark was assigned fresh len(buf) (group 13, hgatehygiene:F1)
* `hygienettinert` -- rpt_code filters hash comments only so inert endswith string preserves 2 bad arms pin without arms (group 13, hgatehygiene:F2)
* `hygienenestedtest` -- Basename exclusion also exempts nested readiness helpers (group 13, hgatehygiene:F3)
* `hygieneclonepins` -- gate 6 expects 74 PTY probes and 43 promptless probes which includes 3 untracked working-tree files (group 13, hgatehygiene:F6)  [id corrected: Astra afile_04: the tie-break assigns this id, H:855]
* `offexemptparse` -- Offline exemptions accept impossible dates and extra components (group 14, hgateoffline:F5)
* `shroundemptyparse` -- SuperH result parsing accepts empty score fields in individual checks (group 14, hgateshrounding:F6)
* `hpcc1timeout` -- C1 accepts TIMEOUT or signal kill as clean rejection (group 15, hhpcmipsctorprobe:F3)
* `lunawaitpidzero` -- host_status decodes waitpid (0,0) on live child as exit 0 (group 15, hlunaabsentcpuprobe:F3)
* `m88kptyleak` -- m88k_rounding_probe leaks 81 master PTY descriptors across sessions (group 15, hm88kroundingprobe:F2)
* `pcc2iplrdvacuity` -- IPL wide-read check cannot fail against pre-fix code (group 16, hpcc2widthprobe:F1)
* `ppcptyfdleak` -- ppc_rounding_probe session() leaks master pty file descriptor (group 16, hppcroundingprobe:F3)
* `precommitungraded` -- precommit check T treats arbitrary non-grade outcome strings as graded (group 16, hprecommitcheck:F4)
* `precommitugstatus` -- precommit check T launders python failure in grading check as success (group 16, hprecommitcheck:F5)
* `precommitpass2sub` -- precommit check F unanchored regex matches 'bypass 2' as pass-2 commit (group 16, hprecommitcheck:F6)
* `receiptprefixlen` -- precommit check F allows arbitrarily short 1-char prefix in receipt SHA (group 16, hprecommitcheck:F7)
* `identguardgrep` -- precommit check E identity guard check matches comment word instead of assertion (group 16, hprecommitcheck:F10)
* `hookctlzeropass` -- precommit check B hook controls accept 0 of 0 controls as pass (group 16, hprecommitcheck:F11)
* `precommitchangedspace` -- precommit_check.sh unquoted $CHANGED splits paths containing whitespace (group 16, hprecommitcheck:F12)
* `precommitcleanskip` -- clean-tree early exit skips section B .MUTANT and section Y NUL checks (group 16, hprecommitcheck:F13)
* `seatverdictsm9` -- seat_verdicts selftest M9 mutant does not test the one-character guard (group 16, hseatverdicts:F1)
* `verdictssplitvacuity` -- seat_verdicts selftest does not assert verdicts_of split extraction (group 16, hseatverdicts:F2)
* `mutantbuildlaunder` -- seat_verdicts selftest scores uncompilable mutant as detected (group 16, hseatverdicts:F3)
* `brieflineslenfilter` -- brief_lines >20 threshold drops short brief lines like wrapped menu options (group 16, hseatverdicts:F4)
* `grepwindrivepath` -- GREP_OUTPUT_LINE pattern misses Windows drive-letter paths (group 16, hseatverdicts:F5)
* `ollamarecoverynote` -- seat_verdicts does not recognize panel_ollama empty-retry recovery envelopes (group 16, hseatverdicts:F9)
* `recoveredverdictsplit` -- seat_verdicts uses verdict_of rather than verdicts_of on recovered text (group 16, hseatverdicts:F11)
* `recoveredwritelaunder` -- seat_verdicts swallows write failure while advertising RECOVERED.md file (group 16, hseatverdicts:F12)
* `shortverdictechoonly` -- seat_verdicts short <=20char verdict classified as ECHO ONLY (group 16, hseatverdicts:F13)
* `sgiredetabsent` -- determinism row reports identical when both reads absent (group 17, hsgirecolourdefaultprobe:F1)
* `pcicp17noisy` -- P17 omits noisy check from pass predicate (group 17, hsh4pcicprobe:F1)
* `pcicp1dempty` -- P1d passes write-suppression check on empty transcript (group 17, hsh4pcicprobe:F4)
* `sh4pcicfdleak` -- session() leaks pty master fd on all return paths (group 17, hsh4pcicprobe:F5)
* `rldicldisasmgap` -- the rldicl probe's header says every placed word is disassembled; four session calls discard the returned disassembly (group 04, hbundle_regress15:F7)  [Astra afile_02, H:232, :253]
