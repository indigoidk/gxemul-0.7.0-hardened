# armmsrmodekill (#562) -- PASS 2 ON THE REPAIR (the repair made in response to pass 2 owes its own pass 2)

Open with `VERDICT: SHIP / SHIP-WITH-CHANGES / DO-NOT-SHIP | <n> floor breaches` (VERDICT LINE FIRST).  Read-only;
write nothing, build nothing.  Tree under review: `GXEMUL-SEC/src/` (working tree; HEAD `ef577140`).  Ignore any
other `src/` under the project root -- they are pristine 2021 upstream.  The working tree ALSO carries a peer
session's unrelated uncommitted edits (cpu_alpha_palcode.c, dev_lca.c, dev_pcc2.c, dev_sh4.c,
mvme_pcctworeg.h) -- not part of this round; ignore them.

**Please do not simply ratify.**  Check the premises, not just the derivations.  A count printed here can be
wrong; re-derive what you can.

Seats: GPT-6 Astra (codex), grok, agy, glm, deepseek, minimax, kimi, Opus 5.5.  Fable 5.1 is DELIBERATELY NOT
FIRED (owner, 2026-10-07).

## What pass 2 found (the repair's inputs)

* codex: (A) latch suppression never revisited -- `|=`->`&=` predicted to keep every row green; (B) SPSR source
  labels: the restore rows ran from SVC only, while FIQ/IRQ/ABT/UND SPSRs also feed new_cpsr; probe overclaims
  (an `SP==0` claim with no readback; the cached-translation limit undisclosed).
* Opus 5.5 (MEASURED in its own clone): F1 deleting the `mode_warned |= ...` line at msr/pop/dpi/load each scored
  26/26; F2 `mask &= ~ARM_FLAG_MODE` -> `mask &= ~0x0f` scored 26/26 (every driven MSR value had bit 4 set);
  F3 = codex's (B).
* grok: the backstop comments' "only a debugger `cpsr=` reaches it" is false -- once a bad mode is planted, later
  GUEST instructions reach the backstops.
* records: the pass-2 brief pasted an ABORTED run's 25/26 score lines without marking them (kimi, deepseek).

## The repair

Product code: comments only changed over the pass-2 diff (the two backstop comments; the DPI comment).  The full
fix vs HEAD is inlined below (9 hunks).  The detector grew 26 -> 38 rows:
* `latch rpt` -- one process visits all five latch sites TWICE (msr, pop, dpi, then a debugger `cpsr=0xd4` plant
  and save/load), counts announces per site (exactly one each), reads CPU state back after the second visits;
* `src dpi|pop x fiq irq abt und svc` (10 rows) -- enter the mode by a modelled MSR, set that mode's SPSR to
  N|Z|0x14: restore 1 declined (whole CPSR word read back = `c00000XX`, mode kept); then SPSR_c := 0x1f, restore 2
  accepted (`c000001f`);
* `kill 03` -- `MSR CPSR_c,#0x03`, the only driven value with mode bit 4 clear;
* ` sp0` token requiring an actual zero SP readback on four rows; NOT CLAIMED list extended.

## Measured (logs under `regress/artifacts/armmsrmodekill/killtable2_20261007/`)

* fixed 38/38 (`run_fixed.out`); HEAD 16/38, 22 named reds (`run_head.out`); both end `ARMMSRMODE_DONE`.
* Table 2 (37-row probe; baseline 37/37 before and after): 16 new mutants + the 20 table-1 mutants re-run --
  ALL 36 red.  New: `|=`->`&=` x5 sites 36/37 each (latch rpt); repair-only-while-latch-clear x5 36/37 each;
  DPI guard SVC-only 33/37; pop guard SVC-only 33/37; DPI keep-current for IRQ only 36/37; pop keep-current for
  ABT only 36/37; helper without `& ARM_FLAG_MODE` 27/37; Save bit aliased to MSR bit 36/37.
* Table 3 (38-row probe; baseline 38/38 before and after): `O_mask_nibble` 37/37 on the OLD 37-row probe (escape
  reproduced) and 37/38 on the 38-row probe (`kill 03`); `|=` line deleted at each of the 5 sites: 37/38 each
  (latch rpt).  Zero escapes on the final probe.
* PRETABLE2 main body written 15:44:06, table 2 started 15:44:37; its table-3 addendum appended 16:04, table 3
  started 21:19.

## The probe's contract (verbatim, regress/arm_msrmode_probe.py)

```
CONTRACT (floor clause (e)) -- the edits this detector is DESIGNED to catch:
  * exit(1) reinstated at Save's default: (dbg save, dbg both, latch rpt) or Load's (dbg both,
    latch rpt);
  * the helper answering 1 always (kill 14/15/1e), admitting 0x1c-0x1e (kill 1e), or dropping its
    `& ARM_FLAG_MODE' projection (src * rows: their SPSRs carry N and Z);
  * the guard dropped at msr_imm (kill rows), arm_pop (rst ldm [SVC], src pop x FIQ IRQ ABT UND
    SVC) or DPI (rst movs, zero spsr [SVC], src dpi x FIQ IRQ ABT UND SVC), or restricted to ONE
    current-mode label (the src * rows: those five SPSR-bearing modes x both paths);
  * the msr_imm decline clearing fewer than all five mode bits, e.g. `& ~0x0f' (kill 03: the
    only driven mode value with bit 4 CLEAR);
  * a restore guard made unconditional, or unconditional for one label (acc movs, acc ldm, the
    valid-SPSR half of each src * row);
  * a WHOLE-OPERATION decline in msr_imm instead of field-only (the `if=' pin on kill rows);
  * the restore not taking N/Z/I/F from the SPSR (src * rows read the whole CPSR word);
  * any two of the five latch sites sharing a bit (latch rpt: all five in one process; also
    dbg both, latch ind);
  * a latch that never SUPPRESSES (`|=' -> `&=', or the `|=' line deleted), or a repair applied
    only while its latch is clear (latch rpt: every site visited TWICE, exactly ONE announce each,
    repair still applied).
NOT CLAIMED, disclosed: unmodelled values other than 0x00, 0x14, 0x15, 0x1e (a helper wrong only
at 0x16, 0x18-0x1a, 0x1c-0x1d or 0x01-0x0f escapes); the msr_imm comment's "only the LOCAL mask
changes: ic->arg[] is a cached translation" -- no row re-executes ONE translated MSR, so a guard
that wrote ic->arg[] would go unseen; per-CPU latch isolation (one CPU only); T-bit /
execution-state coherence on restore; the USR/SYS `LDM {pc}^' and `MSR SPSR' paths that stop the
CPU (filed separately).

NAMED-RED tally: HEAD = 16/38, RED exactly kill 14, kill 15, save 2s, kill 1e, kill 03, rst movs,
rst ldm,
zero spsr, dbg save, dbg both, latch ind, latch rpt, and the ten src * rows, CONTROL=OK.  `save
2s' on HEAD is the SAME Load death as `kill 14' (EOF on the first MSR) -- it is not an
independent HEAD reproduction of Save; nor is `dbg both' a HEAD reproduction of Load (HEAD dies
in Save first).  38/38 on HEAD
is a broken vehicle, not success.

```

## PRETABLE2 (verbatim)

```
PRETABLE2 -- #562 pass-2 repair, written BEFORE kill table 2 (mtime precedes KILLTABLE2.out)
Baseline: HEAD ef577140 export + the CURRENT GXEMUL-SEC working-tree cpu_arm.c / cpu_arm_instr.c /
cpu_arm_instr_dpi.c / cpu_arm.h (copied to msr3/sec_baseline/, byte-identical to the msr2 fix) with
the pass-2 COMMENT-ONLY edits (D) applied = msr3/src; installed probe + pass-2 rows = 37 rows.
Fixed 37/37 (run_fixed.out); HEAD 16/37, reds exactly the 21 named (run_head.out), each `dead' in
Load (mode 20 / 21 / 30 / 0) or Save (dbg save, dbg both).

1. SIBLING PARITY after the repair
   Five latch sites, each now visited TWICE in one process (latch rpt), count-checked (==1), with a
   readback after the second visit.  Two restore paths x five SPSR-bearing labels, each with a
   declined and an accepted cell in one session (src dpi/pop x fiq irq abt und svc).  Remaining
   asymmetry: the SPSR source label is crossed with the reserved value 0x14 only, the zero-SPSR
   cell stays SVC/DPI only (disclosed in the header as values-other-than / one CPU).

2. CLAIM -> ROW (comments changed or newly relied on)
   cpu_arm.h "each announce once per CPU, independently": latch rpt (five sites, x2, count==1).
              "per CPU": NOT rowed (testarm has one CPU) -- disclosed.
   Save default (reworded) "reached only once an unmodelled mode is ALREADY in CPSR -- then any
              later bank switch (guest MSR, S-to-PC, exception entry)": dbg save (guest MSR),
              dbg both + latch rpt (guest MOVS).  Exception entry: NOT rowed (single-step
              suppresses IRQ dispatch; no SWI/UND row) -- disclosed by omission, noted here.
   Load default (reworded): dbg both, latch rpt.
   DPI (reworded) "value assigned below takes all other bits from the SPSR": src dpi * (whole-word
              readback c0000011.. / c000001f).  "T forced for an odd destination PC": NOT rowed.
   arm_pop "every other bit comes from the SPSR": src pop * (whole word).
   msr_imm "only the local mask changes: ic->arg[] is a cached translation": NOT rowed -- now in the
              header's NOT CLAIMED list.
   probe acc usr/acc movs/acc ldm/dbg save "SP is 0": ` sp0' requires dumped == 0.

3. GUARD FIELD vs BODY FIELD
   Restore guards read new_cpsr (selected by the CURRENT mode label: spsr_fiq/irq/svc/abt/und);
   the body writes cpsr from new_cpsr and decides the bank switch on it.  The selector (current
   mode) flows into new_cpsr -> per the selector-data-flow rule each label is an axis: rowed x
   {declined, accepted} x {DPI, POP}.  Helper reads `mode & ARM_FLAG_MODE'; the src SPSRs carry
   N|Z in bits 31:30 so the projection's operand has a nonzero high part.
   Latch field: the five `|=' writers; latch rpt reads every bit's suppression and independence.

4. PER MUTANT: predicted killing row and the differing observable
   N_latch_and_{msr,pop,dpi,save,load}   latch rpt: msr2 / pop2 / dpi2 / save2 / load2
   N_cond_msr     latch rpt: 2nd MSR (#0x15) applied -> s_14 in mode 0x15 -> msr_imm_spsr default
                  (running=0) -> a=nofire (or dead)
   N_cond_pop     latch rpt: 2nd LDM^ applies 0x14 -> Load backstop -> a=14/.. + load text
   N_cond_dpi     latch rpt: 2nd MOVS applies 0x14 -> a=14/.., load text
   N_cond_save    latch rpt: 2nd Save visit -> exit(1) -> dead
   N_cond_load    latch rpt: 2nd Load visit -> exit(1) -> dead
   N_dpi_svc_only src dpi {fiq,irq,abt,und}: c1 = c0000014 (applied), Load backstop
   N_pop_svc_only src pop {fiq,irq,abt,und}: same
   N_dpi_keep_irq src dpi irq: c2 = c0000012 not c000001f
   N_pop_keep_abt src pop abt: c2 = c0000017 not c000001f
   N_helper_nomask  every src * row: c2 = c00000XX (valid SPSR declined because N|Z is set);
                  also ` once' count may change
   N_alias_save_msr latch rpt: save0 (Save's text suppressed by the msr decline's bit)
   M_* (table-1 set, re-run on the 37-row probe as regression): same killing rows as table 1,
   plus latch rpt where the edit touches a latch site or a backstop.
   CHANNEL check: every listed observable is a readback word, an exact announce COUNT or alive/
   dead; none is survive-only.
END PRETABLE2

ADDENDUM (written BEFORE table 3 runs) -- Opus 5.5 pass-2 additions
   New row: kill 03 (MSR CPSR_c,#0x03 -- the only driven mode value with bit 4 clear).
   Records: docstring's cpu_arm.c:606-608/:559-561 marked PRE-#562; contract names the modes
   rowed per restore path; mask width now CLAIMED (kill 03); src_v3 rewords both backstop comments
   ("only after a debugger plant, then by any later mode switch, exception or IRQ") -- comments only.
   Predictions:
   O_mask_nibble   kill 03: bit 4 written 0 -> mode 0x03 -> Load backstop -> m=03 (no msr text
                   is still printed, since the guard ran; the readback is the channel).  On the
                   37-row probe2: predicted ESCAPE (all its MSR values have bit 4 set).
   D_del_msr/pop/dpi/save/load   latch rpt: the deleted site's count = 2 (msr2 / pop2 / dpi2 /
                   save2 / load2), everything else unchanged.

```

## The fix vs HEAD (verbatim)

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
@@ -556,9 +582,20 @@
 		cpu->cd.arm.und_r13_r14[0] = cpu->cd.arm.r[13];
 		cpu->cd.arm.und_r13_r14[1] = cpu->cd.arm.r[14];
 		break;
-	default:fatal("arm_save_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: reached only once an unmodelled mode is ALREADY in
+		    CPSR, which only a debugger `cpsr=' assignment can now put
+		    there (msr_imm and both SPSR restores decline it); after
+		    such a plant ANY later mode switch gets here -- a guest MSR
+		    to a modelled mode, an S-to-PC return, an exception or IRQ
+		    entry.  Backstop: announce once per CPU and return
+		    -- no exit(1), no rollback; r8-r14 are not saved.  */
+		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_SAVE)) {
+			cpu->cd.arm.mode_warned |= ARM_MODEWARN_SAVE;
+			fatal("arm_save_register_bank: unimplemented mode %i;"
+			    " registers not saved (once)\n",
+			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
+		}
+		return;
 	}
 }
 
@@ -603,9 +640,18 @@
 		cpu->cd.arm.r[13] = cpu->cd.arm.und_r13_r14[0];
 		cpu->cd.arm.r[14] = cpu->cd.arm.und_r13_r14[1];
 		break;
-	default:fatal("arm_load_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: backstop, as in arm_save_register_bank(): reached
+		    only after a debugger `cpsr=' plant of an unmodelled mode,
+		    then by any later mode switch (guest MSR, S-to-PC return,
+		    exception or IRQ) that leaves it in place.  Announce once
+		    per CPU and return; r8-r14 keep their current values.  */
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
@@ -215,19 +215,38 @@
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
+		    in M[4:0]; the value assigned to CPSR below takes all other
+		    bits from the SPSR (msr_imm's POLICY) -- though T is forced
+		    after Load for an odd destination PC.  Only when an SPSR was
+		    copied; no early return (pc is set).  */
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

## Questions -- answer each `<n> | <answer>`

1. FLOOR, asked of the SHIPPED COMPOSITE (not only the repair hunks): is there a single smallest edit to the fix
   that keeps all 38 rows green?  Enumerate the cells you swept (the denominator) -- "zero found" must say what
   was looked for.  Consider: the guard dominating predicates in msr_imm / arm_pop / DPI, the five latch sites,
   the helper, the `spsr_copied` gate, and each restore path's label axis.
2. The 2026-09-09 label clause: the DPI/pop restore selects new_cpsr by the CURRENT mode label.  Is the rowed
   product {fiq irq abt und svc} x {declined, accepted} x {dpi, pop} the right closure, or is a cell missing
   (e.g. the zero-SPSR cell rowed for SVC/DPI only; latch state x label)?
3. Records: is any comment, contract line or tally above false?  In particular the reworded backstop comments,
   the DPI comment's "T is forced after Load for an odd destination PC", and the NOT CLAIMED list.
4. Is the NOT CLAIMED list honest -- does any disclosed gap hide something a guest reaches on testarm that the
   round claims to have fixed?
**If, while verifying, you found something ELSE -- say so.**
