OPUS_HIGH_ARM_ALIVE_1001

First line of _scratchpad/CHECKPOINT.md (verbatim):
# CHECKPOINT -- 2026-10-01 10:16 RUNNING: #529 precheck (working files swapped until it ends), Astra confirm 3a, Fable retro 3b/3c/3d; loop cron fb3a48fa live (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: 3 of 3 findings hold as stated -- all three are guest-reachable paths that end the emulator process (H4 exit(1), H5 host stack overflow, H6 cpu->running=0 on a single-CPU machine); none is misgraded on reachability or severity. Zero DISPOSITIONS are wrong on those two axes; the only imprecision is a label (H4 "new" is really "documented-but-unqueued", H5's PPC/SH/M88K note is unverified here). And the standing license fires loudly: H4's reachability is BROADER than the brief says (no CP15 privilege gate -> user-mode reaches it), and memory_arm.c carries TWO more guest-reachable exit(1)s of H5's own class that the brief does not list.

All line numbers are read from `git show db8b1a33:<path>` on GXEMUL-SEC, not the working tree and not the 2021 copies. My exit census of cpu_arm_coproc.c matches the brief exactly (13 lines, 7 active: 62,177,264,322,331,417,528). Settled premises S1/S2/S3 all check out against db8b1a33 (fatal() at debugmsg.c:384-391 has no exit; machine.c:701-747 machine_run returns false when no CPU runs; emul.c:1052-1059 breaks the loop unless debugger_enter_at_end_of_run, which -K/-V/any configured breakpoint sets; main.c:821 returns 0).

====================================================================
Q1. PREMISE AUDIT -- reachable as described? the one load-bearing premise, and could I check it?
====================================================================

H4 -- REACHABLE (and wider than stated).
  The load-bearing premise: "a guest can, during execution, write CP15 c1/op2=0 with the byte-order (B) bit differing from cpu->byte_order, and line 177 exit(1) runs." If anything gated or overrode that write, H4 would be false.
  Checked -- YES, and it HOLDS:
   * arm_mcr_mrc (cpu_arm.c:2643-2655) dispatches to coproc[15] with NO processor-mode check. The mcr_mrc instruction wrapper (cpu_arm_instr.c:948-954) has none either. On real ARM a CP15 MCR from User mode is UNDEFINED; this model lets user code reach arm_coproc_15 directly. So H4 is reachable from UNPRIVILEGED code, not only privileged.
   * The write path: l_bit=0 so the read block (c1:91-104) is skipped; op2=0 so both 107 and 124 are skipped; line 135 stores r[rd] into cpu->cd.arm.control UNCONDITIONALLY; 157-159 derive old_control's B from cpu->byte_order (default LITTLE, cpu_arm.c:123); 161 compares. Guest writes control with bit 0x80 (ARM_CONTROL_BIG) set -> mismatch -> fatal()+exit(1). Nothing forces the bit or declines the write.
  Verifiable statically from the committed tree; done. (A rung-3 witness -- one mcr p15,0,Rd,c1,c0,0 with Rd=0x80 on evbarm -- is cheap if the round wants one, but the control flow is local and unambiguous.)

H5 -- REACHABLE.
  The load-bearing premise: "the fault-delivery path re-enters the pc-to-pointers routine for the exception vector with NO depth bound, and the vector page can be unmapped while translate_v2p can fail." If a double-fault guard existed, H5 would be false.
  Checked -- YES, and it HOLDS. The cycle, all on db8b1a33:
     cpu_dyntrans.c:679 translate_v2p(..., FLAG_INSTR)  [FLAG_INSTR only; no FLAG_NOEXCEPTIONS, so it WILL raise]
       -> memory_arm.c:268-269 arm_exception(PREF_ABT)
         -> cpu_arm.c:733 quick_pc_to_pointers(cpu)
           -> quick_pc_to_pointers.h:9-16 vector page not cached (phys_page==NULL) -> generic pc_to_pointers
             -> cpu_dyntrans.c:679 again, for the vector -> faults -> arm_exception -> ... (grows one C frame per turn)
  There is no re-entry counter anywhere in that loop. Host stack exhausts -> SIGSEGV -> process ends. Note the exit(1) at cpu_dyntrans.c:729-733 ("could not find physical address of the exception handler") is NEVER reached on ARM: translate_v2p at :679 never returns in the faulting case (it recurses inside arm_exception before returning), so control never reaches :720-733. That dead-for-ARM exit exists for an arch whose translate_v2p returns 0 WITHOUT raising; ARM's always raises. The brief's reading is correct on both points.
  Trigger: MMU enabled (so translate_v2p == arm_translate_v2p_mmu, which can fail; with MMU off translate_v2p == arm_translate_v2p and always succeeds) AND the vector page (0x0 or, with ARM_CONTROL_V, 0xffff0000) not mapped, then any exception. Only a faulty/under-construction kernel is ever that -- a correct OS maps its vectors before enabling the MMU. Reachable from privileged guest code only. Verified statically.

H6 -- REACHABLE (unprivileged; the broadest surface of the three).
  The load-bearing premise: "for a USR32/SYS32 LDM with S-bit and r15 in the list, return_flag becomes set, and the mode switch has no USR/SYS case so it halts." If line 1616 sat outside the s_bit block, or the switch had a USR/SYS arm, H6 would be false.
  Checked -- YES, and it HOLDS:
   * USR32: cpu_arm_instr.c:1612 true -> fatal()+s_bit=0 (:1614). Then :1616 `if (iw & 0x8000)` is still INSIDE the outer `if (s_bit)` entered while s_bit was set, so with r15 in the list it sets return_flag=1 (:1618). So return_flag IS set for a user-mode LDM that lists r15.
   * SYS32: :1612 false (mode 0x1f != USR 0x10), so s_bit stays 1 through the load; :1616 then sets s_bit=0, return_flag=1 when r15 is listed. Same outcome.
   * Return path :1784 switches on mode with cases FIQ/ABT/UND/IRQ/SVC only; USR32 (0x10) and SYS32 (0x1f) fall to default (:1795) -> fatal()+cpu->running=0+next_ic=nothing_call. Halts for BOTH.
   * No mode or privilege gate at decode: main_opcode 0x8/0x9 -> bdt_load (cpu_arm_instr.c:4787-4788) -> arm_pop with s_bit=(iw&0x00400000). The fast-path generator REJECTS S-bit opcodes at build time (generate_arm_multi.c:86-89 exit if s), so every LDM^ reaches the generic arm_pop -- the halt is not bypassed by the fast path. (The Thumb `pop` caller, cpu_arm.c:1677, passes s_bit=0, so only the ARM LDM^ form reaches this.)
  One ordinary user instruction (LDM with bit22 S and bit15 r15 set) stops the emulated machine. Verified statically; a rung-3 witness is trivial if wanted.

====================================================================
Q2. WHICH OF THE THREE DISPOSITIONS IS WRONG? -- count
====================================================================

ZERO are wrong on the two axes that define the grade. All three are genuinely guest-reachable and all three end the process, so HIGH is correct for each, and raising H5 MED->HIGH is correct (stack overflow ends the process).

I checked each of the three ways a disposition can be wrong and did not simply ratify:
 * Reachability: holds for all three (H4 even wider than claimed; H6 unprivileged; H5 privileged-but-real).
 * Severity: HIGH holds for all three (process ends in every case on a single-CPU machine, which is the normal ARM config here).
 * Duplicate: none is a duplicate. H6 is a DIFFERENT defect from #524/armbdt even though both live in arm_pop -- #524 is the unaligned-address splice in the LOAD path (the :1653 comment); H6 is the s-bit RETURN path. H5 is distinct from the dead exit(1) it sits near. H4 is distinct from everything.

The only imprecisions worth recording, neither of which flips a grade:
 * H4 is labelled "new". It is not strictly new: round #378 already DOCUMENTED this exit as deliberate and load-bearing, with the alternative's cost analysed in-comment (:163-174). "Documented-but-never-queued-as-a-defect" is the honest state. It is still a correct HIGH to act on.
 * H5's "same shape on PowerPC and possibly SH and M88K" is UNVERIFIED in this packet. The recursion is in the arch-generic cpu_dyntrans.c pc-to-pointers routine, so the shape is plausible on any arch whose translate_v2p raises by calling <arch>_exception which calls quick_pc_to_pointers -- but I did not confirm PPC/SH/M88K here and would not ratify that clause.

====================================================================
Q3. CORRECTION ROUND -- chosen disposition per finding; is the machinery on THIS CPU? and a member the list does not name
====================================================================

The list: (1) delete the terminating call; (2) decline silently; (3) decline + announce once per device/CPU; (4) accept (value already computed); (5) fault (deliver the architecture's exception); (6) accept into invented store; (7) implement.

H4 -> member 3 (decline the B-bit change, keep the old byte order, announce once per CPU), with member 7 filed.
  Why not 1: the #378 comment is right -- deleting the exit alone leaves cpu->cd.arm.control's B bit disagreeing with the byte order the already-translated code was built for. So the fix must also NOT let the mismatching bit persist in the stored register.
  The read-back question the brief asks: today line 135 stores r[rd] wholesale, so a subsequent read of c1 (line 95) returns the B bit the guest tried to set -- which, if we only suppressed the exit, would be a lie. The sound member-3 fix forces the stored control's B bit back to match cpu->byte_order after announcing, so the guest reads back the UNCHANGED (actual) endianness. That is the architecturally honest answer: the write of an unsupported bit is ignored and reads as the old value.
  Machinery on THIS CPU: YES. Member 3 needs only debugmsg + a per-CPU latch (the tree's house idiom). Member 7 (really switch) needs invalidate_translation_caches(cpu,0,INVALIDATE_ALL) -- which EXISTS and is already called from cp15 c8 (cpu_arm_coproc.c:238) -- plus re-translation and a revisit of the LDM/STM install gate (#378). So 7 is available in principle but is its own round; 3 is the right in-round disposition.

H5 -> member 5 is already the INTENT (deliver PREF_ABT/DATA_ABT), and option 5's machinery EXISTS on ARM (arm_exception delivers both). The defect is not an unserviceable access at all -- it is UNBOUNDED RE-ENTRY in the fault-delivery machinery. So the needed change is a double-fault / re-entry bound: detect that a translation fault is being raised while already delivering an exception-vector fetch, and stop that CPU cleanly with one diagnostic (member-3-style) instead of recursing. Real ARM has no architectural "give up" here (hardware would just keep taking aborts -- a livelock, not a stack overflow), so a bounded, announced halt of that CPU is the faithful emulator behaviour.
  => THIS IS THE MEMBER THE LIST DOES NOT NAME: a re-entry/recursion bound (double-fault detection) on the fault path. The seven options are all dispositions for an ACCESS the model cannot service; H5 is a control-flow depth bug in the exception machinery, orthogonal to them. Call it member 8: "bound the re-entry."

H6 -> member 1 (ignore the S/return in USR/SYS and just load the listed registers as a plain LDM) is the least-surprising, with member 5 (raise UND) as a defensible alternative. The architecture calls it UNPREDICTABLE (ddi0100i A4.1.22), so either is conformant; the ONE thing the model must not do is halt the machine on an unprivileged instruction.
  Concretely: in USR32/SYS32 do not set return_flag (treat as an ordinary LDM, loading r15 as a plain value, no CPSR restore). Machinery: trivial. Member 5 (arm_exception(ARM_EXCEPTION_UND)) also exists and is already used by arm_cdp (cpu_arm.c:2677), so UND delivery is available on this CPU too. I would choose member 1 (closest to what most real cores do and it preserves forward progress); member 5 is acceptable.

====================================================================
Q4. RANK by what an OS in ordinary operation would actually meet (most likely first), and on what basis
====================================================================

1. H6 (most likely to be met).  Basis: PRIVILEGE and SURFACE. It is an UNPRIVILEGED single instruction; the attack/accident surface is the entire userland, and no special machine configuration or kernel state is required. A correct user program will not emit the UNPREDICTABLE USR/SYS form, but any hand-written, miscompiled, or fuzzed user binary -- or a port's early test program -- can, and it halts the whole machine. No kernel cooperation needed.

2. H5 (middle).  Basis: it needs a KERNEL in a specific broken state -- MMU enabled with the vector page unmapped -- then any exception. That is precisely the classic early-boot / new-port bug (enable the MMU, then something faults before the vector mapping is in place), so a kernel under development meets it readily; a shipping, correct kernel never does. Privileged-only, but a real and recurring contact point during OS bring-up (which is a lot of what this emulator is used for).

3. H4 (least likely).  Basis: it requires a deliberate RUNTIME attempt to flip the CP15 byte-order bit. No supported ARM OS switches endianness after boot; byte order is fixed at reset. So in ordinary operation essentially nothing reaches it -- it is reachable, and HIGH, but the trigger is an action real guests do not take. (It becomes more reachable than its rank suggests ONLY because the missing CP15 privilege gate lets user code attempt the write -- see the standing-license note -- but a correct guest still never flips the bit.)

Ranking basis in one line: privilege required to reach it, and whether correct software ever emits the trigger -- H6 (unprivileged, whole userland) > H5 (privileged, a classic bring-up bug) > H4 (privileged, an action no real guest performs).

====================================================================
STANDING LICENSE -- things I found while verifying the three
====================================================================

SL1. No CP15 privilege check (widens H4, and is its own defect).
  arm_mcr_mrc (cpu_arm.c:2643-2655) and the mcr_mrc wrapper (cpu_arm_instr.c:948-954) perform NO processor-mode check before dispatching to coproc[15]. On real ARM, CP15 MCR/MRC executed in User mode is UNDEFINED and traps to the undefined handler. Here a user-mode `mcr p15,...` reaches arm_coproc_15 directly. Consequences: H4 (line 177), the `rd==ARM_PC` exit (line 62) and the FCSE `pid!=0` exit (line 264) are all reachable from UNPRIVILEGED code on EVERY ARM machine. That is both a correctness gap (missing UNDEF trap) and a denial-of-service surface. Worth its own row.

SL2. Answering the brief's wider question -- which of the seven active exits a guest can reach:
   * 62  (cp15, rd==r15): ANY ARM machine; reachable even from user mode (SL1). Guest-reachable.
   * 177 (cp15, endianness switch = H4): ANY ARM machine; user-reachable (SL1).
   * 264 (cp15, pid!=0 / FCSE): ANY ARM machine; user-reachable (SL1). A guest write of nonzero to c13 ends the process.
   * 322 (cp6, i80321 interrupt steering != 0): only machines that install coproc[6] -- machine_iq80321.c:57 and machine_iyonix.c:64. Guest-reachable there.
   * 331 (cp6, i80321 "int ack"): same machines; fires on ANY write to that register. Guest-reachable there.
   * 417 (cp6, unknown reg): same machines; reachable with an unhandled crn/crm.
   * 528 (cp14, xscale PMU unknown reg): only XScale CPUs (coproc[14] installed at cpu_arm.c:178-179 under ARM_XSCALE). Reachable there.
  So 3 of 7 (62,177,264) are guest-reachable on every ARM machine (and from user mode); the other 4 are guest-reachable on the specific machines/CPUs that install cp6/cp14. Six of the seven are guest-reachable given the right target; only the top-of-handler ones are config-limited. Several of these (notably 62 and 264) are the same HIGH class as H4 and are arguably higher-priority than H4 because the trigger (any nonzero PID, or naming r15) is closer to something software might actually do than a runtime endian flip.

SL3. Two MORE guest-reachable exit(1)s in memory_arm.c, NOT in the brief, same class as H5's siblings (direct host exit on guest-controlled MMU state):
   * memory_arm.c:78-79  arm_check_access() dav==2 -> fatal()+exit(1). dav = (dacr >> (domain*2)) & 3, and dacr is fully guest-controlled via CP15 c3 (cpu_arm_coproc.c:203, an unconditional store, and user-reachable per SL1). A guest that sets any domain's DAC field to 0b10 (a value real hardware treats as reserved, NOT a crash) and then accesses a page in that domain ends the process. HIGH.
   * memory_arm.c:252-254  first-level descriptor type 3 -> default -> fatal()+exit(1). The switch on (d&3) handles 0/1/2 and sends 3 to default. The first-level descriptor is read from the guest's own translation table, so a guest page table carrying a type-0b11 (fine page table / reserved) entry ends the process. HIGH.
  Both are distinct from H5 (H5 is unbounded recursion; these are direct exits), both are guest-reachable, both HIGH, and neither is in the packet. If H5 becomes a round, these two belong in the same sweep of memory_arm.c.

SL4. Minor, for the record: arm_save_register_bank / arm_load_register_bank (cpu_arm.c:559-562, 606-609) also exit(1) on an unimplemented mode. They are reachable only if cpsr's mode field is already an unhandled value; H6's halt happens in arm_pop before those would be hit for the USR/SYS case, so they are not the H6 mechanism, but they are another exit-on-guest-mode-state site in the same area.
