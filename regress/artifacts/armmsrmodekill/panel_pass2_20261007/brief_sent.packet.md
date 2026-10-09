# armmsrmodekill (#562) -- PASS 2 on the real diff

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`; the change is
UNCOMMITTED in the working tree over HEAD `ef577140`; other uncommitted files there -- dev_pcc2.c, dev_sh4.c, dev_lca.c,
mvme_pcctworeg.h, cpu_alpha_palcode.c -- belong to another session and are NOT part of this review).  Ignore any other src/
under the project root.  Read-only: write nothing, build nothing.  If you cannot read files, everything you need is inlined.
**VERDICT LINE FIRST:** `VERDICT: SHIP | SHIP-WITH-CHANGES | DO-NOT-SHIP -- <one line> | <n> floor breaches`

## What the round does (rulings from pass 1 + the shared adjudication pass, both 8/8 seats + Opus 5.5; Fable on hold)
A reserved/unmodelled ARM mode (anything but 10 11 12 13 17 1b 1f) used to end the PROCESS at `arm_load_register_bank`'s /
`arm_save_register_bank`'s `default: exit(1)`.  Guest paths: `MSR CPSR_c,#0x14`; an SPSR poisoned by `MSR SPSR_c` then
restored by `MOVS pc,lr` (DPI S-to-PC) or `LDM {..pc}^` (arm_pop); and a NEVER-WRITTEN SPSR (cpu_new zero-fills: mode 0x00)
restored the same way -- no MSR needed.  The fix (member 3): decline the MODE FIELD only at those three writers (POLICY for an
UNPREDICTABLE result: DDI 0100I A2.5.7, glossary "must not halt or hang"; ARMv7 also permits UNDEFINED), latched per-CPU
announces with `(once)`, and both `default:` arms become latched backstops that return (reachable only by a debugger
`cpsr=` assignment).

## The detector and its measurement (rung-3, `-E testarm`, debugger-driven; `regress/arm_msrmode_probe.py`, 26 rows)
* FIXED build 26/26; HEAD 16/26 -- reds exactly kill 14, kill 15, save 2s, kill 1e, rst movs, rst ldm, zero spsr, dbg save,
  dbg both, latch ind, every one `dead` (process exit).
* Kill table (each mutant built in a scratch clone, probe frozen; logs end ARMMSRMODE_DONE).  M_shared_msrpop ESCAPED the
  25-row probe; the `latch ind` row was added (L1) and closes it and the two DPI pairings:
```
BASE                   RESULT=25/25             REDS=none                                                    tail=ARMMSRMODE_DONE
M_load_exit            RESULT=24/25             REDS=dbg both                                                tail=ARMMSRMODE_DONE
M_save_exit            RESULT=23/25             REDS=dbg save,dbg both                                       tail=ARMMSRMODE_DONE
M_load_exit_latched    RESULT=24/25             REDS=dbg both                                                tail=ARMMSRMODE_DONE
M_save_exit_latched    RESULT=23/25             REDS=dbg save,dbg both                                       tail=ARMMSRMODE_DONE
M_helper_always1       RESULT=18/25             REDS=kill 14,kill 15,save 2s,kill 1e,rst movs,rst ldm,zero spsr tail=ARMMSRMODE_DONE
M_helper_range         RESULT=24/25             REDS=kill 1e                                                 tail=ARMMSRMODE_DONE
M_drop_msr             RESULT=21/25             REDS=kill 14,kill 15,save 2s,kill 1e                         tail=ARMMSRMODE_DONE
M_drop_pop             RESULT=24/25             REDS=rst ldm                                                 tail=ARMMSRMODE_DONE
M_drop_dpi             RESULT=23/25             REDS=rst movs,zero spsr                                      tail=ARMMSRMODE_DONE
M_uncond_both          RESULT=23/25             REDS=acc movs,acc ldm                                        tail=ARMMSRMODE_DONE
M_uncond_pop           RESULT=24/25             REDS=acc ldm                                                 tail=ARMMSRMODE_DONE
M_uncond_dpi           RESULT=24/25             REDS=acc movs                                                tail=ARMMSRMODE_DONE
M_wholeop_msr          RESULT=22/25             REDS=kill 14,kill 15,kill 1e                                 tail=ARMMSRMODE_DONE
M_shared_latch         RESULT=24/25             REDS=dbg both                                                tail=ARMMSRMODE_DONE
M_shared_saveload      RESULT=24/25             REDS=dbg both                                                tail=ARMMSRMODE_DONE
M_shared_msrpop        RESULT=25/25             REDS=none                                                    tail=ARMMSRMODE_DONE
M_dpi_uncond_call      RESULT=24/25             REDS=dbg both                                                tail=ARMMSRMODE_DONE
M_pop_return           RESULT=24/25             REDS=rst ldm                                                 tail=ARMMSRMODE_DONE
BASE_AFTER             RESULT=25/25             REDS=none                                                    tail=ARMMSRMODE_DONE
FIXED_probe2               RESULT=25/26             REDS=latch ind                                               tail=ARMMSRMODE_DONE
HEAD_probe2                RESULT=16/26             REDS=kill 14,kill 15,save 2s,kill 1e,rst movs,rst ldm,zero spsr,dbg save,dbg both,latch ind tail=ARMMSRMODE_DONE
BASE_probe2                RESULT=25/26             REDS=latch ind                                               tail=ARMMSRMODE_DONE
FIXED_probe2               RESULT=26/26             REDS=none                                                    tail=ARMMSRMODE_DONE
HEAD_probe2                RESULT=16/26             REDS=kill 14,kill 15,save 2s,kill 1e,rst movs,rst ldm,zero spsr,dbg save,dbg both,latch ind tail=ARMMSRMODE_DONE
BASE_probe2                RESULT=26/26             REDS=none                                                    tail=ARMMSRMODE_DONE
M_shared_msrpop_probe2     RESULT=25/26             REDS=latch ind                                               tail=ARMMSRMODE_DONE
M_shared_msrdpi_old        RESULT=25/25             REDS=none                                                    tail=ARMMSRMODE_DONE
M_shared_msrdpi_probe2     RESULT=25/26             REDS=latch ind                                               tail=ARMMSRMODE_DONE
M_shared_popdpi_old        RESULT=25/25             REDS=none                                                    tail=ARMMSRMODE_DONE
M_shared_popdpi_probe2     RESULT=25/26             REDS=latch ind                                               tail=ARMMSRMODE_DONE
M_shared_latch_probe2      RESULT=24/26             REDS=dbg both,latch ind                                      tail=ARMMSRMODE_DONE
BASE_AFTER_probe2          RESULT=26/26             REDS=none                                                    tail=ARMMSRMODE_DONE
```
* DISCLOSED, not rowed (in the probe header): helper errors at values no row drives (0x16, 0x18-0x1a, 0x1c-0x1d, 0x01-0x0f);
  a decline bit shared with a backstop bit; the "only the local mask changes" claim (needs a row re-executing the same
  translated MSR); T-bit/execution-state consistency on restore (filed separately); the USR-mode LDM^/MSR SPSR CPU stop
  (filed separately).

## `git diff --numstat` for the round's files (all INLINED below)
```
48	6	src/cpus/cpu_arm.c
35	0	src/cpus/cpu_arm_instr.c
23	6	src/cpus/cpu_arm_instr_dpi.c
13	0	src/include/cpu_arm.h
regress/arm_msrmode_probe.py  (NEW FILE in the commit; its diff against the 2026-09-17 untracked version is INLINED)
```

## Questions
1. Premise audit: which statement above is wrong?
2. Is each guard right against its caller's real control flow (MSR mask before `switch_register_banks`; arm_pop no early
   return before the PC load; DPI `new_cpsr`/`spsr_copied`, no early return, flags written after CPSR)?  Any path left
   reachable to `exit(1)` or to `running = 0` by a reserved mode?
3. **The smallest edit to the FIX that still passes all 26 rows** -- name it and the row you expect to stay green.
4. Floor check: does the detector fail on the pre-fix build (yes, 16/26), on a verbatim reinstatement of each removed
   `exit(1)` (see table), on a nulled repair (each guard dropped / made unconditional -- see table)?  Is any DEPENDS-ON
   predicate un-mutated?
5. Records: is any added comment claim (in the diff) unsupported by a row or by the measurement above?
**If, while verifying, you found something ELSE — say so.**

## THE FIX (verbatim `git diff` of src/, 4 files)
```diff
--- a/src/include/cpu_arm.h
+++ b/src/include/cpu_arm.h
@@ -113,6 +113,14 @@
 #define	ARM_MODE_UND32	      0x1b
 #define	ARM_MODE_SYS32	      0x1f
 
+/*  #562: arm_cpu.mode_warned bits -- the three guest declines and the two
+    register-bank backstops each announce once per CPU, independently.  */
+#define	ARM_MODEWARN_MSR	0x01
+#define	ARM_MODEWARN_POP	0x02
+#define	ARM_MODEWARN_DPI	0x04
+#define	ARM_MODEWARN_SAVE	0x08
+#define	ARM_MODEWARN_LOAD	0x10
+
 #define ARM_EXCEPTION_TO_MODE	{	\
 	ARM_MODE_SVC32, ARM_MODE_UND32, ARM_MODE_SVC32, ARM_MODE_ABT32, \
 	ARM_MODE_ABT32, 0,              ARM_MODE_IRQ32, ARM_MODE_FIQ32 	}
@@ -194,6 +202,10 @@
 	uint32_t		spsr_irq;
 	uint32_t		spsr_fiq;
 
+	/*  #562: once-latch for the unmodelled-mode announces, one
+	    ARM_MODEWARN_* bit per site (per CPU, zero at cpu_new).  */
+	uint32_t		mode_warned;
+
 
 	/*
 	 *  System Control Coprocessor registers:
@@ -342,6 +354,7 @@
 	unsigned char *host_page, int writeflag, uint64_t paddr_page);
 void arm_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
 void arm_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
+int arm_mode_is_modelled(uint32_t mode);
 void arm_load_register_bank(struct cpu *cpu);
 void arm_save_register_bank(struct cpu *cpu);
 int arm_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
--- a/src/cpus/cpu_arm.c
+++ b/src/cpus/cpu_arm.c
@@ -517,6 +517,32 @@
 
 
 /*
+ *  arm_mode_is_modelled():
+ *
+ *  #562: 1 if M[4:0] of `mode' is one of the seven modes this model banks
+ *  (10 11 12 13 17 1b 1f), else 0.  Its case list MUST stay equal to the
+ *  case lists of arm_save_register_bank() and arm_load_register_bank()
+ *  below: the three switches together define "modelled", and those two
+ *  default: arms are reached only for a mode this returns 0 for.  Extern,
+ *  not static: the DPI template is compiled as its own object.
+ */
+int arm_mode_is_modelled(uint32_t mode)
+{
+	switch (mode & ARM_FLAG_MODE) {
+	case ARM_MODE_USR32:
+	case ARM_MODE_SYS32:
+	case ARM_MODE_FIQ32:
+	case ARM_MODE_IRQ32:
+	case ARM_MODE_SVC32:
+	case ARM_MODE_ABT32:
+	case ARM_MODE_UND32:
+		return 1;
+	default:return 0;
+	}
+}
+
+
+/*
  *  arm_save_register_bank():
  */
 void arm_save_register_bank(struct cpu *cpu)
@@ -556,9 +582,18 @@
 		cpu->cd.arm.und_r13_r14[0] = cpu->cd.arm.r[13];
 		cpu->cd.arm.und_r13_r14[1] = cpu->cd.arm.r[14];
 		break;
-	default:fatal("arm_save_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: a guest instruction no longer gets here (msr_imm
+		    and both SPSR restores decline an unmodelled mode first); a
+		    debugger `cpsr=' assignment still does.  Backstop: announce
+		    once per CPU and return -- no exit(1), no rollback; r8-r14
+		    stay live and are simply not saved.  */
+		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_SAVE)) {
+			cpu->cd.arm.mode_warned |= ARM_MODEWARN_SAVE;
+			fatal("arm_save_register_bank: unimplemented mode %i;"
+			    " registers not saved (once)\n",
+			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
+		}
+		return;
 	}
 }
 
@@ -603,9 +638,16 @@
 		cpu->cd.arm.r[13] = cpu->cd.arm.und_r13_r14[0];
 		cpu->cd.arm.r[14] = cpu->cd.arm.und_r13_r14[1];
 		break;
-	default:fatal("arm_load_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: backstop, as in arm_save_register_bank(): only a
+		    debugger `cpsr=' assignment reaches it.  Announce once per
+		    CPU and return; r8-r14 keep their current values.  */
+		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_LOAD)) {
+			cpu->cd.arm.mode_warned |= ARM_MODEWARN_LOAD;
+			fatal("arm_load_register_bank: unimplemented mode %i;"
+			    " registers not loaded (once)\n",
+			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
+		}
+		return;
 	}
 }
 
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -827,6 +827,25 @@
 		mask &= 0xff000000;
 	}
 
+	/*
+	 *  #562: a mode-field write naming a mode this model does not bank
+	 *  (reserved, or 26-bit) used to reach arm_load_register_bank()'s
+	 *  exit(1).  The architecture makes the result UNPREDICTABLE (DDI
+	 *  0100I A2.5.7; ARMv7 lets it be UNDEFINED) and forbids halting.
+	 *  Declining the MODE FIELD only, with the rest of the write applied,
+	 *  is this emulator's POLICY, not an architectural requirement.  Only
+	 *  the local mask changes: ic->arg[] is a cached translation.
+	 */
+	if ((mask & ARM_FLAG_MODE) && !arm_mode_is_modelled(ic->arg[0])) {
+		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_MSR)) {
+			cpu->cd.arm.mode_warned |= ARM_MODEWARN_MSR;
+			fatal("[ msr_imm: mode 0x%02x is not modelled; mode field"
+			    " not written, other fields are (once) ]\n",
+			    (int)(ic->arg[0] & ARM_FLAG_MODE));
+		}
+		mask &= ~ARM_FLAG_MODE;
+	}
+
 	int switch_register_banks = (mask & ARM_FLAG_MODE) &&
 	    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
 	    (ic->arg[0] & ARM_FLAG_MODE));
@@ -1799,6 +1818,22 @@
 			return;
 		}
 
+		/*  #562: an SPSR naming an unmodelled mode (an MSR SPSR_c of a
+		    reserved value, or an SPSR never written: zero = mode 0)
+		    keeps the CURRENT mode in M[4:0]; every other bit comes from
+		    the SPSR.  Same POLICY as msr_imm.  No return here: the PC
+		    load below must still run.  */
+		if (!arm_mode_is_modelled(new_cpsr)) {
+			if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_POP)) {
+				cpu->cd.arm.mode_warned |= ARM_MODEWARN_POP;
+				fatal("[ arm_pop: SPSR mode 0x%02x is not modelled;"
+				    " mode kept (once) ]\n",
+				    (int)(new_cpsr & ARM_FLAG_MODE));
+			}
+			new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) |
+			    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);
+		}
+
 		switch_register_banks = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
 		    (new_cpsr & ARM_FLAG_MODE);
 
--- a/src/cpus/cpu_arm_instr_dpi.c
+++ b/src/cpus/cpu_arm_instr_dpi.c
@@ -215,19 +215,36 @@
 		cpu->pc = (uint32_t)c64;
 #ifdef A__S
 		/*  Copy the right SPSR into CPSR:  */
+		uint32_t cur_mode = cpu->cd.arm.cpsr & ARM_FLAG_MODE;
+		uint32_t new_cpsr = cpu->cd.arm.cpsr;
+		int spsr_copied = 1;
 		arm_save_register_bank(cpu);
-		switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
+		switch (cur_mode) {
 		case ARM_MODE_FIQ32:
-			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_fiq; break;
+			new_cpsr = cpu->cd.arm.spsr_fiq; break;
 		case ARM_MODE_IRQ32:
-			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_irq; break;
+			new_cpsr = cpu->cd.arm.spsr_irq; break;
 		case ARM_MODE_SVC32:
-			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_svc; break;
+			new_cpsr = cpu->cd.arm.spsr_svc; break;
 		case ARM_MODE_ABT32:
-			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_abt; break;
+			new_cpsr = cpu->cd.arm.spsr_abt; break;
 		case ARM_MODE_UND32:
-			cpu->cd.arm.cpsr = cpu->cd.arm.spsr_und; break;
+			new_cpsr = cpu->cd.arm.spsr_und; break;
+		default:spsr_copied = 0;
 		}
+		/*  #562: an SPSR naming an unmodelled mode keeps the CURRENT mode
+		    in M[4:0], all other bits from the SPSR -- msr_imm's POLICY.
+		    Only when an SPSR was copied; no early return (pc is set).  */
+		if (spsr_copied && !arm_mode_is_modelled(new_cpsr)) {
+			if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_DPI)) {
+				cpu->cd.arm.mode_warned |= ARM_MODEWARN_DPI;
+				fatal("[ dpi S-to-pc: SPSR mode 0x%02x is not "
+				    "modelled; mode kept (once) ]\n",
+				    (int)(new_cpsr & ARM_FLAG_MODE));
+			}
+			new_cpsr = (new_cpsr & ~ARM_FLAG_MODE) | cur_mode;
+		}
+		cpu->cd.arm.cpsr = new_cpsr;
 		cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;
 		arm_load_register_bank(cpu);
 #else

```

## THE PROBE DIFF (against the 2026-09-17 untracked version)
```diff
--- a/regress/arm_msrmode_probe.py
+++ b/regress/arm_msrmode_probe.py
@@ -46,12 +46,42 @@
 *** POLARITY: WANT IS POST-FIX CORRECT.  A PRE FAIL ON A DEFECT ROW *IS* THE REPRODUCTION. ***
 *** ORACLE: EOF ALONE => DEAD.  THE TEXT IS DIAGNOSIS, NEVER HALF THE TRIGGER. ***
 
-NAMED-RED tally (spec): HEAD = 14/17, RED exactly kill 14, kill 15, save 2s, CONTROL=OK.
-`save 2s' on HEAD is the SAME Load death as `kill 14' (EOF on the first MSR) -- it is not an
-independent HEAD reproduction of Save.  17/17 on HEAD is a broken vehicle, not success.
+#562 THE FIX AND WHAT THIS PROBE NOW DETECTS.  Three guest writers can put an unmodelled mode
+(anything but 10 11 12 13 17 1b 1f) into CPSR, and each now DECLINES THE MODE FIELD ONLY, with a
+`(once)' announce naming its site: msr_imm (`MSR CPSR_c'), arm_pop's `LDM {..pc}^' SPSR restore,
+and the DPI `MOVS pc,..' SPSR restore.  The restores keep the CURRENT mode in M[4:0] and take
+every other bit from the SPSR.  The Save/Load `default:' arms are BACKSTOPS (latched announce,
+return, no exit(1)), reachable only by a debugger `cpsr=' assignment.  POST-FIX the guest is in
+SVC32 with the I/F bits the write set -- `#0x14' clears I and F -- NOT in a reserved mode.  Rows
+added by #562: kill 1e, rst movs, rst ldm, zero spsr, acc movs, acc ldm, dbg save, dbg both,
+latch ind,
+and the `if=' (I/F) pin on kill 14 / kill 15.
+
+MODES 0x00-0x0F ARE NOW CLAIMED.  This header used to BAN `MSR CPSR_c, #0' as "the 26-bit hole,
+a different defect".  The helper declines 0x00-0x0F like any other unmodelled value, and
+`zero spsr' drives exactly mode 0x00 (an SPSR never written is zero: cpu_new zero-fills).
+
+CONTRACT (floor clause (e)) -- the edits this detector is DESIGNED to catch:
+  * exit(1) reinstated at Save's default: (dbg save, dbg both) or Load's default: (dbg both);
+  * the helper answering 1 always (kill 14/15/1e), or admitting 0x1c-0x1e (kill 1e);
+  * the guard dropped at msr_imm (kill rows), arm_pop (rst ldm) or DPI (rst movs, zero spsr);
+  * a restore guard made unconditional, always keeping the current mode (acc movs, acc ldm);
+  * a WHOLE-OPERATION decline in msr_imm instead of field-only (the `if=' pin on kill rows);
+  * Save and Load sharing one latch bit (dbg both, which fires both in one instruction);
+  * any two of the three DECLINE sites (msr_imm, arm_pop, DPI) sharing a latch bit (latch ind).
+NOT CLAIMED, disclosed: unmodelled values other than 0x00, 0x14, 0x15, 0x1e (a helper wrong only
+at 0x16, 0x18-0x1a, 0x1c-0x1d or 0x01-0x0f escapes); a DECLINE bit shared with a BACKSTOP bit
+(no row drives a guest decline and a backstop in one process); T-bit / execution-state coherence
+on restore;
+the USR/SYS `LDM {pc}^' and `MSR SPSR' paths that stop the CPU (filed separately).
+
+NAMED-RED tally: HEAD = 16/26, RED exactly kill 14, kill 15, save 2s, kill 1e, rst movs, rst ldm,
+zero spsr, dbg save, dbg both, latch ind, CONTROL=OK.  `save 2s' on HEAD is the SAME Load death as
+`kill 14' (EOF on the first MSR) -- it is not an independent HEAD reproduction of Save; nor is
+`dbg both' a HEAD reproduction of Load (HEAD dies in Save first).  26/26 on HEAD
+is a broken vehicle, not success.
 
-Stay on `step', never `continue' (IRQ dispatch is inside `if (!single_step)').  `MSR CPSR_c,
-#0' is BANNED (26-bit hole, a different defect).
+Stay on `step', never `continue' (IRQ dispatch is inside `if (!single_step)').
 """
 import os
 import pty
@@ -91,9 +121,19 @@
     "str_r0":   0xE5840000,              # str  r0, [r4]
     "b_self":   0xEAFFFFFE,              # b    .
 }
-for m in (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x1B, 0x1F):
+for m in (0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x1B, 0x1E, 0x1F):
     WORDS["c_%02x" % m] = 0xE321F000 | m     # msr cpsr_c, #m
 WORDS["f_14"] = 0xE328F014                   # msr cpsr_f, #0x14
+#  #562: SPSR poisoning and the two restore paths.
+for m in (0x14, 0x1F):
+    WORDS["s_%02x" % m] = 0xE361F000 | m     # msr spsr_c, #m
+WORDS["movs_pc_lr"] = 0xE1B0F00E             # movs pc, lr       (DPI S-to-PC restore)
+WORDS["ldm_r5_pc_s"] = 0xE8D58000            # ldmia r5, {pc}^   (arm_pop restore)
+
+TGT = 0x8100                                 # restore target: lr, and the word at LDMW
+LDMW = 0x9100                                # where `ldm_r5_pc_s' loads pc from
+TGT_OPS = ["mrs_r3", "str_r3_4", "str_sp_8"]
+TGT2 = 0x8140                                # `latch ind': readback after the chained MOVS
 
 rows = []
 diagnosis = []
@@ -248,29 +288,77 @@
 PREFIX = ["mrs_r3", "str_r3"]
 
 
-def msr_cmds(ops, steps_after, late_end=DEST + 12):
+def msr_cmds(ops, steps_after, late_end=DEST + 12, restore=False, regs=(), poke=(),
+             chain=False):
     """Standard MSR session: prefix MRS/STR to DEST, arming dumps (DEST and the whole planted
-    stream), MARK, the stimulus steps, then the result dump."""
+    stream), MARK, the stimulus steps, then the result dump.
+    #562: restore=True also plants TGT_OPS at TGT, sets lr=TGT and the LDMW word to TGT, and
+    arms all three (a fall-through past the restore lands on b_self and reads `nofire').
+    `regs' are debugger assignments made BEFORE the prefix; `poke' ones AFTER the arming dumps
+    (a `cpsr=' poke must follow the prefix, whose MRS arms DEST == 0xd3).
+    chain=True (with restore): TGT holds `movs pc,lr' and the readback TGT_OPS move to TGT2,
+    where lr points -- so one session can run an LDM^ restore and then a MOVS restore."""
     full = PREFIX + ops
-    return (prologue() + plant(full)
-            + ["pc=0x%x" % CODE, "step 2", dumpcmd(DEST),
-               dumpcmd(CODE, CODE + 4 * len(full)), MARK]
-            + ["step %d" % s for s in steps_after]
-            + [dumpcmd(DEST, late_end)]), full
+    cmds = prologue() + plant(full)
+    extra = {}
+    rb = TGT2 if chain else TGT
+    if restore:
+        cmds += plant(TGT_OPS, at=rb) + ["put w 0x%x, 0x%08x" % (LDMW, TGT),
+                                         "lr=0x%x" % rb, "r5=0x%x" % LDMW]
+        for i, k in enumerate(TGT_OPS + ["b_self"]):
+            extra[rb + 4 * i] = WORDS[k]
+        extra[LDMW] = TGT
+        if chain:
+            cmds += plant(["movs_pc_lr"], at=TGT)
+            extra[TGT] = WORDS["movs_pc_lr"]
+            extra[TGT + 4] = WORDS["b_self"]
+    cmds += list(regs) + ["pc=0x%x" % CODE, "step 2", dumpcmd(DEST),
+                          dumpcmd(CODE, CODE + 4 * len(full))]
+    if restore:
+        cmds += [dumpcmd(TGT, TGT + 4 * len(TGT_OPS)), dumpcmd(LDMW)]
+        if chain:
+            cmds += [dumpcmd(TGT2, TGT2 + 4 * len(TGT_OPS))]
+    cmds += [MARK] + list(poke) + ["step %d" % s for s in steps_after] \
+        + [dumpcmd(DEST, late_end)]
+    return cmds, (full, extra)
 
 
 def arming(early, full):
-    """R4: DEST == 0xd3 after the prefix, and every planted word reads back as its WORDS entry."""
+    """R4: DEST == 0xd3 after the prefix, and every planted word reads back as its WORDS entry.
+    #562: `full' may be (ops, {addr: word}) -- the extra plants (restore target, LDM word)."""
+    extra = {}
+    if isinstance(full, tuple):
+        full, extra = full
     if dumped(early, DEST) != BOOT_CPSR:
         return False
     for i, k in enumerate(full):
         if dumped(early, CODE + 4 * i) != WORDS[k]:
             return False
+    for a, w in extra.items():
+        if dumped(early, a) != w:
+            return False
     return True
 
 
-def classify(early, late, alive, marked, full, cpsr_at=DEST + 4, sp_at=None, rt_at=None):
-    """The got string.  EOF ALONE => dead.  Arming is checked first, from the EARLY half."""
+def diag_unimpl(nm, t):
+    """#562: which register-bank `unimplemented mode' text a session printed (HEAD: the
+    function that exit(1)ed -- the reason under test; fixed: the backstop that announced)."""
+    hits = sorted(set(re.findall(r"arm_(save|load)_register_bank: unimplemented mode (\d+)", t)))
+    diagnosis.append("%s: %s" % (nm, ", ".join("%s mode %s" % h for h in hits) if hits
+                                 else "no bank text"))
+
+
+def announced(t, key):
+    """#562: a `(once)' announce from the NAMED site -- the five sites share the token, so a
+    bare `(once)' cannot tell a decline from a backstop, or Save's backstop from Load's."""
+    return any(key in ln and "(once)" in ln for ln in t.splitlines())
+
+
+def classify(early, late, alive, marked, full, cpsr_at=DEST + 4, sp_at=None, rt_at=None,
+             once_key=None, pin_if=False, backstops=False, declines=False):
+    """The got string.  EOF ALONE => dead.  Arming is checked first, from the EARLY half.
+    #562: once_key names the announcing site; pin_if adds the CPSR I/F pair (field-only vs
+    whole-operation decline); backstops adds ` save' / ` load' per Save/Load announce."""
     if not marked or not arming(early, full):
         return "unarmed"
     if not alive:
@@ -279,10 +367,22 @@
     if cpsr is None or cpsr == POISON:
         return "nofire"
     got = "m=%02x" % (cpsr & 0x1F)
+    if pin_if:
+        got += " if=%d" % ((cpsr >> 6) & 3)
     if sp_at is not None and dumped(late, sp_at) == BOOT_SP:
         got += " sp"
-    if "(once)" in early + late:
+    t = early + late
+    if (announced(t, once_key) if once_key else "(once)" in t):
         got += " once"
+    if declines:
+        for key, tag in (("msr_imm", "msr"), ("arm_pop", "pop"), ("dpi S-to-pc", "dpi")):
+            if announced(t, key):
+                got += " " + tag
+    if backstops:
+        if announced(t, "arm_save_register_bank"):
+            got += " save"
+        if announced(t, "arm_load_register_bank"):
+            got += " load"
     if rt_at is not None:
         v = dumped(late, rt_at)
         if v not in (None, POISON) and (v & 0x1F) == 0x13:
@@ -315,6 +415,22 @@
         if ((w >> 16) & 0xF) != 0b1000 or (w & 0xFF) != 0x14 or ((w >> 8) & 0xF) != 0 \
                 or (w & 0x00400000) or (w & 0x0FB0F000) != 0x0320F000:
             bad.append(k)
+    if k.startswith("s_"):
+        #  #562: the SPSR form -- same frame, field nibble 0001, bit 22 (R) SET.
+        if ((w >> 16) & 0xF) != 0b0001 or (w & 0xFF) != int(k[2:], 16) \
+                or ((w >> 8) & 0xF) != 0 or not (w & 0x00400000) \
+                or (w & 0x0FB0F000) != 0x0320F000:
+            bad.append(k)
+    if k == "movs_pc_lr":
+        #  data-processing MOV (opcode 1101), S set, Rd = 15, Rm = 14, no shift
+        if (w >> 21) & 0xF != 0xD or not (w >> 20) & 1 or (w >> 12) & 0xF != 15 \
+                or w & 0xFFF != 14 or (w >> 25) & 7 != 0:
+            bad.append(k)
+    if k == "ldm_r5_pc_s":
+        #  LDM: bits 27:25 = 100, L set, S (bit 22) set, W clear, Rn = 5, list = {pc} only
+        if (w >> 25) & 7 != 0b100 or not (w >> 20) & 1 or not (w >> 22) & 1 \
+                or (w >> 21) & 1 or (w >> 16) & 0xF != 5 or w & 0xFFFF != 0x8000:
+            bad.append(k)
 row("enc ok", "clean" if not bad else ",".join(bad), "clean",
     "CONTROL=DEAD. Decoder match on the PLANTED literals: MSR-imm frame (w & 0x0FB0F000) == "
     "0x0320F000, field nibble (w>>16)&0xF = 0001 c-form / 1000 f-form, rot 0, bit 22 clear, imm8 "
@@ -357,9 +473,12 @@
 for nm, key, dec in (("kill 14", "c_14", 20), ("kill 15", "c_15", 21)):
     cmds, full = msr_cmds([key, "mrs_r3", "str_r3_4", "str_sp_8"], [1, 3])
     early, late, alive, marked = _session_split(cmds)
-    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8), "m=13 sp once",
+    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key="msr_imm",
+                     pin_if=True), "m=13 if=0 sp once",
         "MSR CPSR_c, #0x%02x into a RESERVED mode reaches arm_load_register_bank's default: and "
-        "exit(1)s. PRE is `dead' -- EOF ALONE -- and that FAIL is the reproduction." % int(key[2:], 16))
+        "exit(1)s. PRE is `dead' -- EOF ALONE -- and that FAIL is the reproduction. #562: "
+        "if=0 pins FIELD-ONLY (the write clears I/F; a whole-op decline keeps if=3)."
+        % int(key[2:], 16))
     t = early + late
     diagnosis.append("%s: %s" % (nm, "load mode %d seen" % dec
                                  if ("arm_load_register_bank: unimplemented mode %d" % dec) in t
@@ -421,7 +540,85 @@
     "In USR32 the c-byte is STRIPPED, so the following #0x14 must NOT reach the mode field. "
     "The host lives and the mode stays 0x10.")
 
-row("row count", len(rows) + 1, 17, "identity row (floor clause (c)): the row set is complete.")
+# ---------------------------------------------------------------- #562 rows
+#  kill 1e: pins the helper's DOMAIN past the two driven reserved values -- a range form
+#  admitting 0x1c-0x1e sends 0x1e to Load's backstop and reads m=1e.
+cmds, full = msr_cmds(["c_1e", "mrs_r3", "str_r3_4", "str_sp_8"], [1, 3])
+early, late, alive, marked = _session_split(cmds)
+row("kill 1e", classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key="msr_imm",
+                        pin_if=True), "m=13 if=0 sp once",
+    "MSR CPSR_c, #0x1e: unmodelled, like 0x14/0x15. Kills a helper widened by RANGE to 0x1e.")
+diag_unimpl("kill 1e", early + late)
+
+#  The two SPSR restores.  `MSR SPSR_c, #0x14' poisons spsr_svc (I=F=0, mode 0x14); the restore
+#  must land at TGT (else `nofire') in SVC32 -- current mode kept -- with I/F FROM THE SPSR
+#  (if=0; a restore that skipped the CPSR write keeps the boot if=3) and the SVC SP.
+for nm, op, site in (("rst movs", "movs_pc_lr", "dpi S-to-pc"),
+                     ("rst ldm", "ldm_r5_pc_s", "arm_pop")):
+    cmds, full = msr_cmds(["s_14", op], [6], restore=True)
+    early, late, alive, marked = _session_split(cmds)
+    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, once_key=site,
+                     pin_if=True), "m=13 if=0 sp once",
+        "MSR SPSR_c,#0x14 then %s: the restore reaches Load's default: (HEAD dead). Post-fix: "
+        "at TGT, mode kept, I/F from the SPSR, `%s' announce." % (op, site))
+    diag_unimpl(nm, early + late)
+
+#  zero spsr: NO MSR at all -- spsr_svc is never written on testarm (cpu_new zero-fills), so
+#  `MOVS pc,lr' from boot SVC32 restores mode 0x00.
+cmds, full = msr_cmds(["movs_pc_lr"], [4], restore=True)
+early, late, alive, marked = _session_split(cmds)
+row("zero spsr", classify(early, late, alive, marked, full, sp_at=DEST + 8,
+                          once_key="dpi S-to-pc", pin_if=True), "m=13 if=0 sp once",
+    "MOVS pc,lr from boot SVC32 with spsr_svc never written (mode 0x00). HEAD dead.")
+diag_unimpl("zero spsr", early + late)
+
+#  The restores' ACCEPT side: a modelled SPSR mode must be APPLIED.  A guard made unconditional
+#  (always keep the current mode) reads m=13 here.  SYS32 SP is the usr/sys bank's (0).
+for nm, op in (("acc movs", "movs_pc_lr"), ("acc ldm", "ldm_r5_pc_s")):
+    cmds, full = msr_cmds(["s_1f", op], [6], restore=True)
+    early, late, alive, marked = _session_split(cmds)
+    row(nm, classify(early, late, alive, marked, full, sp_at=DEST + 8, pin_if=True),
+        "m=1f if=0",
+        "MSR SPSR_c,#0x1f then %s: SYS32 restored, SP from the usr/sys bank (0), no announce."
+        % op)
+
+#  The BACKSTOPS: reachable only by the debugger `cpsr=' ASSIGNMENT (no bank switch, no flags
+#  sync).  NOT `put', which writes MEMORY.  The poke follows the arming dumps.  once_key names
+#  a DECLINE site that must NOT announce: a plant is not a guest decline (dbg both: the DPI
+#  guard runs only when an SPSR was copied, and mode 0x14 has none).
+cmds, full = msr_cmds(["c_13", "mrs_r3", "str_r3_4", "str_sp_8"], [4], poke=["cpsr=0xd4"])
+early, late, alive, marked = _session_split(cmds)
+row("dbg save", classify(early, late, alive, marked, full, sp_at=DEST + 8, backstops=True,
+                         once_key="msr_imm"),
+    "m=13 save",
+    "cpsr=0xd4 then MSR CPSR_c,#0x13: Save's default: (HEAD exit(1)) announces and returns; "
+    "Load(SVC) gives the never-saved svc SP (0, so no ` sp').")
+diag_unimpl("dbg save", early + late)
+
+cmds, full = msr_cmds(["movs_pc_lr"], [4], restore=True, poke=["cpsr=0xd4"])
+early, late, alive, marked = _session_split(cmds)
+row("dbg both", classify(early, late, alive, marked, full, sp_at=DEST + 8, backstops=True,
+                         once_key="dpi S-to-pc"),
+    "m=14 sp save load",
+    "cpsr=0xd4 then MOVS pc,lr: no SPSR for 0x14, so BOTH Save's and Load's default: run in ONE "
+    "instruction -- the only carrier of Load's backstop, and of their distinct latch bits.")
+diag_unimpl("dbg both", early + late)
+
+#  latch ind: ALL THREE guest declines in ONE process -- MSR CPSR_c,#0x14, then MSR SPSR_c,#0x14
+#  and LDM {pc}^ (arm_pop) to TGT, whose MOVS pc,lr (DPI) restores the same poisoned spsr_svc to
+#  TGT2.  Each site has its own mode_warned bit, so all three texts must appear; any two sharing a
+#  bit print only the first.  (The other rows are each a fresh process and cannot see sharing.)
+cmds, full = msr_cmds(["c_14", "s_14", "ldm_r5_pc_s"], [8], restore=True, chain=True)
+early, late, alive, marked = _session_split(cmds)
+#  once_key="register_bank": the generic ` once' token would be set by ANY of the three texts and
+#  so carries nothing here; keyed on the backstops it pins their ABSENCE instead (no guest
+#  decline may fall through to Save/Load).  The per-site ` msr pop dpi' tags are the channel.
+row("latch ind", classify(early, late, alive, marked, full, sp_at=DEST + 8, pin_if=True,
+                          once_key="register_bank", declines=True), "m=13 if=0 sp msr pop dpi",
+    "MSR, LDM^ and MOVS declines in ONE session: three distinct latch bits, three texts.")
+diag_unimpl("latch ind", early + late)
+
+row("row count", len(rows) + 1, 26, "identity row (floor clause (c)): the row set is complete.")
 
 # ---------------------------------------------------------------- report
 print("arm_msrmode_probe -- binary=%s label=%s machine=testarm" % (BIN, LABEL))
@@ -438,7 +635,7 @@
 print("ARMMSRMODE_REDS=%s" % (",".join(reds) if reds else "none"))
 for d in diagnosis:
     print("  diag  %s" % d)
-EXPECT = "kill 14,kill 15,save 2s"
+EXPECT = "kill 14,kill 15,save 2s,kill 1e,rst movs,rst ldm,zero spsr,dbg save,dbg both,latch ind"
 print("ARMMSRMODE_EXPECT_HEAD_REDS=%s" % EXPECT)
 print("ARMMSRMODE_TALLY_MATCHES_HEAD_EXPECT=%s" % ("yes" if ",".join(reds) == EXPECT else "no"))
 print("ARMMSRMODE_DONE")

```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
