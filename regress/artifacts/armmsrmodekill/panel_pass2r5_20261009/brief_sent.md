# armmsrmodekill (#562) -- FINAL PASS, ON REPAIR 5 (owner ruling 2026-10-08: one review pass, then commit)

Open with `VERDICT: SHIP / SHIP-WITH-CHANGES / DO-NOT-SHIP | <n> floor breaches` (VERDICT LINE FIRST).  Read-only;
write nothing, build nothing.  Tree: `GXEMUL-SEC/src/` working tree (HEAD `ef577140`); the detector is
`GXEMUL-SEC/regress/arm_msrmode_probe.py` (47 rows) -- file-reading seats should read it.  Ignore other `src/` copies
under the project root and the peer session's unrelated uncommitted files (cpu_alpha_palcode.c, dev_lca.c,
dev_pcc2.c, dev_sh4.c, mvme_pcctworeg.h).  **Please do not simply ratify; check premises.**

Seats: GPT-6 Astra (codex), grok, agy, glm, deepseek, minimax, kimi, Opus 5.5.  Fable 5.1 DELIBERATELY NOT FIRED.

## Shared findings from the last pass, and their disposition

Last pass (repair 4, 43 rows): codex + grok DO-NOT-SHIP; the Opus 5.5 seat MEASURED 15 of 18 mutants at 43/43, in four
classes -- the helper NARROWED (`mode & 0x17` admits 0x18-0x1a), the msr decline's width varying by label, a restore
decline FORCING a bit or OR-ing old bits in, T while latched -- plus two already disclosed.  agy voted SHIP; minimax,
glm, deepseek and kimi-k3 SHIP-WITH-CHANGES.  ALL ADOPTED.  Owner ruling 2026-10-08: **repair 5 GENERATES the
restore/MSR coverage** (G1-G4 below) instead of adding rows by hand.

## Measured on repair 5 (`regress/artifacts/armmsrmodekill/killtable5_20261008/`)

Product code UNCHANGED (fix5.diff byte-identical to fix4.diff).  fixed 47/47 (43 sessions); HEAD 18/47, 29 named reds.
Two tables in 8 lanes, every lane 47/47 before and after: **110 runs, 104 distinct mutants (the earlier set plus Opus's
18), 103 red, ONE at 47/47: `M_msr_argmask`** -- the msr decline ALSO writes `ic->arg[1] &= ~ARM_FLAG_MODE` (the cached
translation).

**And a records error in repair 5's probe, found while reading that escape, corrected before this pass (comment-only,
AST-identical to the measured probe):** its NOT CLAIMED said the grid's re-executions of `msr cpsr_fsxc,r1` "pin the
register form".  They cannot.  Every re-execution in the probe follows a debugger INTERACTION (to set r1, or to dump),
and `debugger()` clears every dyntrans translation when it interacts -- `src/debugger/debugger.c`, the loop under
"Clear all dyntrans translations" -- returning BEFORE that clear only while a `step N` count is still running.  So each
execution is re-translated and an `ic->arg[]` write never reaches the next one.  A guest loop re-executing ONE
translated MSR inside a single `step N`, changing the register between passes, would pin it; NOT built.

## Gate 14 wiring (NEW in this round -- review it): the section appended to `regress/gate_arm.sh`

```sh

#  #562 armmsrmodekill.  A privileged guest MSR naming a mode this model does not bank (MSR CPSR_c,#0x14 =
#  0xE321F014), or an SPSR restore (MOVS pc,lr; LDM {..pc}^) whose SPSR names one -- including an SPSR never written,
#  which is zero -- reached arm_load_register_bank()'s default: and ended the emulator.  msr_imm and both restores now
#  decline the MODE FIELD only, announced once per site per CPU, and Save/Load's default: arms are latched backstops.
#  The probe's CONTRACT, its generated grid and its NOT CLAIMED list are in its header; the kill tables and the
#  review chain's measurements are in regress/artifacts/armmsrmodekill/.  Rows do not end in their status token
#  (a note follows it), so failed rows are read from ARMMSRMODE_REDS, never grepped.
MSRLOG=$LOGDIR/gate_arm_msrmode.log
mrc=0
python3 -u arm_msrmode_probe.py "$PMAX" gate > "$MSRLOG" 2>&1 || mrc=$?

#  PARSE BEFORE SCORE: exactly one valid record of each kind.
if [ "$(grep -c '^ARMMSRMODE_RESULT=' "$MSRLOG")" != "1" ] ||
   ! grep -Eq '^ARMMSRMODE_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$MSRLOG" ||
   [ "$(grep -c '^ARMMSRMODE_CONTROL=' "$MSRLOG")" != "1" ] ||
   ! grep -Eq '^ARMMSRMODE_CONTROL=(OK|DEAD)$' "$MSRLOG" ||
   [ "$(grep -c '^ARMMSRMODE_REDS=' "$MSRLOG")" != "1" ] ||
   [ "$(grep -cx 'ARMMSRMODE_DONE' "$MSRLOG")" != "1" ]; then
    note "msrmode probe produced no unique, valid completion record; last lines follow"
    tail -5 "$MSRLOG" | sed 's/^/       /'
    check "msrmode probe output parses" "no" "yes"
else
    check "msrmode probe output parses" "yes" "yes"
    grep -E ' want=' "$MSRLOG" | grep -E ' FAIL ' | sed 's/^/       /'
    check "msrmode controls" "$(sed -n 's/^ARMMSRMODE_CONTROL=//p' "$MSRLOG")" "OK"
    check "msrmode probe exit status" "$mrc" "0"
    mres=$(sed -n 's/^ARMMSRMODE_RESULT=//p' "$MSRLOG")
    #  Pinned by hand to a LITERAL, UNQUOTED, under the ONE-TOKEN stem arm_msrmode (check_score_claims.py's PIN regex
    #  takes one whitespace-free token before `rows run'; the stem also puts the probe's docstring under that scan).
    #  MEASURED: <OWED the committed probe's base leg, named, run BEFORE this pin was written>.
    check "arm_msrmode rows run"     "${mres#*/}" 47
    check "arm_msrmode rows correct" "${mres%/*}" "47"
    check "arm_msrmode rows emitted" "$(grep -cE '^  [^ ].* got=.* want=' "$MSRLOG")" "47"
    check "arm_msrmode reds"         "$(sed -n 's/^ARMMSRMODE_REDS=//p' "$MSRLOG")" "none"
fi

```

## Probe header: the generated grid, CONTRACT, NOT CLAIMED, tally (verbatim, as corrected)

```
THE GENERATED GRID (repair 5; owner ruling 2026-10-08).  The restore/MSR coverage is GENERATED
from tables (grid_obs(): labels, MODELLED, UNMODELLED, complementary value pairs), not written row
by row: `grid msr', `grid dpi', `grid pop' run every generated observation and compare the WHOLE
CPSR word; `grid cov' re-derives the coverage table from the same generator and reds on any gap.
  G1 every (path, outcome, bit 0..31, polarity) cell has an observation whose result bit must
     equal the SPSR / operand value while the OLD CPSR's bit differs (complementary pairs:
     OLD 0 / NEW all-ones-with-T, and OLD all-ones / NEW 0), so keep-old, force-0 and force-1 all
     change the word.  This is a UNION across observations, not a property of every decline.
     Named equivalents: bit 4 polarity 0 and bit 4 on accept (every modelled mode and label
     has bit 4 set, so keep-old / force-1 equal the right answer there), and T
     polarity 0 against OLD T = 1 (the guest runs ARM code, so OLD T is always 0; keep-old T is
     caught at polarity 1).  The latch is SET for every decline after a session's first.
  G2 every msr_imm label (FIQ IRQ SVC ABT UND SYS) declines label ^ 0x1f, which differs in all
     five mode bits; the restore labels decline the same value as the SPSR.
  G3 all 25 unmodelled values are declined and all 7 modelled modes accepted on EACH path.
  G4 arm_pop's enclosing cells {S, non-S} x {PC, no PC}, all four, in grid pop.
  The hand-written rows below remain (G5): label x latch x outcome (src), tbit (T with the latch
  clear, by `print cpsr'), encl / encl2 (the DPI enclosing cells), msr wide, msr lbl.  Sessions:
  the probe prints ARMMSRMODE_SESSIONS.

CONTRACT (floor clause (e)) -- the edits this detector is DESIGNED to catch:
  * exit(1) reinstated at Save's default: (dbg save, dbg both, latch rpt) or Load's (dbg both,
    latch rpt);
  * the helper answering 1 always (kill 14/15/1e), wrong on ANY of the 32 mode values on ANY path
    -- narrowed (e.g. `& 0x17' admits 0x18-0x1a), widened by any bit 31:5, or dropped (grid *:
    G3 drives all 25 unmodelled and all 7 modelled values through each path; src rows, tbit,
    msr wide);
  * the guard dropped at msr_imm (kill rows), arm_pop (rst ldm, src pop x FIQ IRQ ABT UND SVC) or
    DPI (rst movs, zero spsr, src dpi x FIQ IRQ ABT UND SVC), or restricted to ONE label, or to
    one unmodelled value such as 0x14 (src rows decline 0x0f), or compiled into the MOV instance
    only (encl2: `subs pc,lr');
  * the msr_imm guard skipped at one current-mode label (msr lbl: a decline from each of FIQ IRQ
    ABT UND SYS; latch rpt: SVC with the latch set);
  * the msr_imm decline clearing fewer than all five mode bits at ANY label (grid msr: G2
    declines label ^ 0x1f at all six labels; kill 03, encl2), or clearing MORE (`& ~0x3f', T lost:
    tbit, grid msr); the restore keep-mode mask letting any SPSR mode bit through (grid dpi/pop:
    G2; src rows);
  * a restore guard made unconditional, or unconditional for one label, or skipped / forced for one
    label x latch-state cell (src rows: all 40 cells; acc movs, acc ldm);
  * a WHOLE-OPERATION decline in msr_imm instead of field-only (the `if=' pin on kill rows; msr
    wide);
  * a decline OR accept taking ANY bit 31:5 from the old CPSR, or forcing it to 0 or to 1,
    with the latch clear or set (grid *: G1 complementary pairs; src R2/R3; tbit; msr wide) --
    this replaces the repair-3 sentence "the declined SPSR has N Z I F SET while the CPSR it
    replaces has them CLEAR" (FALSE for N and Z) and repair 4's "at EVERY decline, every restored
    bit differs" (FALSE for T at src R2/R3 and msr wide: it held only as a UNION);
  * any two of the five latch sites sharing a bit (latch rpt: all five in one process; also
    dbg both, latch ind);
  * a latch that never SUPPRESSES (`|=' -> `&=', or the `|=' line deleted), or a repair applied
    only while its latch is clear (latch rpt: every site visited TWICE; src rows per label);
  * the enclosing predicates widened in ANY of their cells: arm_pop's `if (return_flag)' (grid
    pop: all four {S, non-S} x {PC, no PC}; also encl, encl2), the DPI template's
    `rd == PC' compare (encl: non-S `add r0,pc'; encl2: S `adds r0,pc'), and the restore's
    `#ifdef A__S' (encl: non-S `add pc,r6,#0' -- NOT `mov pc,lr', which the decoder turns into
    `ret' and so never reaches the DPI template).
NOT CLAIMED, disclosed: DPI opcode instances other than MOV and SUB (graded (e): the opcode
flows into nothing the repair reads).  The msr_imm comment's "only the LOCAL mask changes:
ic->arg[] is a cached translation" is NOT pinned, in either form.  Every re-execution in this
probe follows a debugger INTERACTION (to set r1, or to dump), and debugger() clears every dyntrans
translation when it interacts (src/debugger/debugger.c, "Clear all dyntrans translations"; it
returns before that clear only while a `step N' count is still running), so each execution is
re-translated from the instruction word and a write to ic->arg[] never reaches the next one.
MEASURED: M_msr_argmask -- the decline also writes `ic->arg[1] &= ~ARM_FLAG_MODE' -- scores 47/47
(artifacts/armmsrmodekill/killtable5_20261008/kt1b/).  Repair 5's text said the grid's
re-executions of `msr cpsr_fsxc,r1' pinned the register form: FALSE, for that reason (corrected
2026-10-09).  A guest LOOP that re-executes ONE translated MSR inside a single `step N', changing
the register between passes, would pin it; not built.  Per-CPU latch isolation (one CPU only); exception entry as a
Save-backstop route (no row); T-bit / execution-state coherence after a T-set restore beyond the
CPSR word itself; the USR/SYS `LDM {pc}^' and `MSR SPSR' paths that stop the CPU (filed
separately).  The grid, tbit and `print cpsr' readbacks are rung-3 debugger observations.  The
`msr wide' accept 0xffffffd1 sets operand bits 31:6, 4 and 0 only (bits 3:1 are clear: the grid's
accepts and c_17 / c_1b / c_1f carry them) -- repair 4's header said "bits 31:6, 4:0".

NAMED-RED tally: HEAD = 18/47, RED exactly the 29 rows kill 14, kill 15, save 2s, kill 1e,
kill 03, rst movs, rst ldm, zero spsr, dbg save, dbg both, latch ind, latch rpt, the ten src *
rows, msr lbl, tbit, encl2, msr wide, grid msr, grid dpi, grid pop, CONTROL=OK.  `encl' drives no
unmodelled mode and `grid cov' is static, so both are GREEN on HEAD.  `save 2s' on HEAD is the
SAME Load death as `kill 14' (EOF on the first MSR) -- it is not an independent HEAD reproduction
of Save; nor is `dbg both' a HEAD reproduction of Load (HEAD dies in Save first).  47/47 on HEAD
is a broken vehicle, not success.

```

## PRETABLE5 (verbatim, written before the table)

```
PRETABLE5 -- #562 repair 5 (GENERATED FULL GRID), written BEFORE kill table 5 (mtime precedes every
LANE output).  Baseline: HEAD ef577140 export + CURRENT GXEMUL-SEC working-tree 4 src files
(= msr5/src_v5, cmp-verified) = msr6/src_v6, UNCHANGED (no product edit: no real defect found).
Probe: the installed 43-row probe + the generated grid (grid msr / grid dpi / grid pop / grid cov)
+ records = 47 rows, 43 sessions (ARMMSRMODE_SESSIONS; the grid adds 3).  Fixed 47/47, HEAD 18/47
with exactly the 29 named reds; each grid row dies on HEAD in Load at mode 14 (= 0x0e, the first
generated decline, FIQ ^ 0x1f) -- the reason under test.

0. THE GENERATOR (grid_obs, in the probe; tables MODELLED, UNMODELLED, RESTORE_LABELS, MSR_LABELS)
   per path: label ^ 0x1f declines x 2 polarities; all 25 unmodelled values declined (labels and
   polarities cycling); accepts of a mode != label x 2 polarities per label; all 7 modelled modes
   accepted; pop adds {ldmia r6,{pc} / {r0}^ / {r0}} x 2 polarities.
   observations: msr 56, dpi 52, pop 58 (= 166).  Every result is the WHOLE CPSR word by
   `print cpsr', compared exactly; announce count per site == 1; no backstop text.
   Complementary pairs: p1 OLD = label, NEW = 0xffffffe0|m; p2 OLD = 0xffffffc0|label, NEW = m.

1. COVERAGE TABLE (grid cov, re-derived from the generator, run offline before the table):
   msr 0 uncovered, dpi 0, pop 0, over (accept, decline) x bits 0..31 x polarity {0,1} = 128 cells
   per path, minus the NAMED EQUIVALENTS:
     bit 4 polarity 0 (no modelled mode or label has bit 4 clear);
     bit 4 on ACCEPT at polarity 1 (OLD's bit 4 is always 1: keep-old / force-1 = right answer);
     bit 5 polarity 0 vs OLD (OLD T is always 0 -- the guest runs ARM; keep-old T caught at p1).
   G2 msr label x mode-bit: 6 labels x 5 bits = 30/30 (label ^ 0x1f differs in all five); restore
   labels 5 x 5 = 25/25 per path.  (codex counted 20/30 on the 43-row probe.)
   G3 helper boundary: 25/25 unmodelled and 7/7 modelled values on EACH path.
   G4 pop enclosing: 4/4 cells, both polarities.

2. CLAIM -> ROW: every CONTRACT bullet in the probe header names its rows; the three records
   (`c00000df' inline comment, "at EVERY decline" = a UNION, 0xffffffd1 bits 3:1) corrected in the
   header; NOT CLAIMED shrinks to: DPI opcodes other than MOV/SUB; the IMMEDIATE msr form's
   re-execution (the register form is re-executed 56x by grid msr); one CPU; exception entry;
   T-state coherence beyond the CPSR word; the USR/SYS CPU-stop paths.

3. GUARD FIELD vs BODY FIELD: unchanged from PRETABLE4; the grid adds the forced-constant
   alternative (force-0 / force-1) per bit, which the old/new-differ rule could not see.

4. PER ROW -- kills: <mutant> via <channel>
   grid msr  H_narrow_17 (0x18-0x1a accepted), M_msr_clr0f_iaus / M_msr_clr0f_irq (label^0x1f
             at IRQ etc.), W_msr_keepflags, M_wholeop_msr, H_proj_*, M_drop_msr, N_cond_msr,
             N_latch_and_msr (n=), E_msr_notfiq, X_msr_latchsvc  -- via the CPSR word, n=
   grid dpi  H_narrow_17, N_dpi_forceN (p2 wants N=0), R_dpi_clr*, N_dpi_keep*/grok, F_dpi_iclr,
             E_dpi_*, L_dpi_latchlabel, N_dpi_svc_only, N_dpi_keep_irq -- via the CPSR word, n=.
             (O_dpi_movonly is NOT a grid dpi kill: the grid restores through MOVS only;
             encl2's `subs pc,lr' carries it.)
   grid pop  H_narrow_17, N_pop_Tlatch (p1 T-set declines with the latch set), N_pop_forceN,
             C_pop_nonS_nopc / C_pop_retflag1 / C_pop_retflagS (G4), R_pop_clr*, B_pop_only14,
             K_pop_ionly, N_pop_keep*/F_pop_iclr, E_pop_*, L_pop_latchlabel  -- via the word, n=
   grid cov  static; reds only if the generator loses a cell (no mutant targets it).
   earlier rows: as PRETABLE2-4.

5. THE TABLE: 92 DISTINCT mutants = the 85 distinct of tables 1-4 (mutr 10, mutr2 13, mutate2 36,
   mutate3 6, mutr3b 18 new, mutate5 2) + mutate6.py 7 (the four pass-2r4 escapes H_narrow_17,
   M_msr_clr0f_iaus, N_pop_Tlatch, N_dpi_forceN rebuilt from their descriptions, plus
   M_msr_clr0f_irq, N_pop_forceN, C_pop_nonS_nopc for codex's named cells).  Opus's own
   pass-2r4 file (regress/artifacts/armmsrmodekill/opus_pass2r4_20261008/) was NOT published
   when this table started; it runs as a second table when it appears.  4 lanes, own clone each,
   BASE before/after per lane.  Predicted equivalent: NONE.
END PRETABLE5

ADDENDUM (written BEFORE table 5b) -- Opus mutr4.py, 18 mutants, run as the SECOND table on the
same frozen 47-row probe.  Six share a NAME with mutate6.py (H_narrow_17, M_msr_clr0f_iaus,
M_msr_clr0f_irq, N_pop_Tlatch, N_dpi_forceN, N_pop_forceN) but are Opus's own texts; the other
twelve are new.  Predicted kills on the grid probe:
   A  H_narrow_17, H_case_18          grid msr/dpi/pop (0x18 declined on every path)
   B  M_msr_clr0f_iaus/irq, M_msr_clr03_abt, M_msr_clr17_fiq   grid msr (label ^ 0x1f per label)
   C  N_dpi_forceN, N_pop_forceN, N_dpi_orold, N_pop_orold     grid dpi/pop p2 declines (OLD
      upper bits all ones, SPSR upper bits zero)
   D  N_pop_Tlatch, N_dpi_Tlatch, N_msr_Tlatch                 grid p1 declines (T set, latch set)
      E_pop_Tacc                                               grid pop p1 accepts (T set, latch set)
   M_msr_argmask  grid msr: every observation re-executes the SAME translated register-form
      `msr cpsr_fsxc,r1'; once a decline strips arg[1]'s mode bits, every later ACCEPT through it
      stays in the old mode.  Predicted KILLED -- if so the NOT CLAIMED cached-translation item
      shrinks to the IMMEDIATE form only (already worded so).
   controls H_narrow_1b, N_dpi_flagslatch, M_msr_forceN       killed (as Opus measured).
   Predicted equivalent: NONE.

```

## The fix vs HEAD (verbatim, 9 hunks)

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
@@ -556,9 +582,22 @@
 		cpu->cd.arm.und_r13_r14[0] = cpu->cd.arm.r[13];
 		cpu->cd.arm.und_r13_r14[1] = cpu->cd.arm.r[14];
 		break;
-	default:fatal("arm_save_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: reached only once an unmodelled mode is ALREADY in
+		    CPSR, which only a debugger `cpsr=' assignment can now put
+		    there (msr_imm and both SPSR restores decline it).  After
+		    such a plant, Save runs on it from a guest MSR to a modelled
+		    mode, a DPI S-to-PC return, or exception/IRQ entry; an
+		    LDM {..pc}^ return does not get here -- arm_pop's own
+		    selector default: stops the CPU first (pre-existing).
+		    Backstop: announce once per CPU and return -- no exit(1),
+		    no rollback; r8-r14 are not saved.  */
+		if (!(cpu->cd.arm.mode_warned & ARM_MODEWARN_SAVE)) {
+			cpu->cd.arm.mode_warned |= ARM_MODEWARN_SAVE;
+			fatal("arm_save_register_bank: unimplemented mode %i;"
+			    " registers not saved (once)\n",
+			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
+		}
+		return;
 	}
 }
 
@@ -603,9 +642,20 @@
 		cpu->cd.arm.r[13] = cpu->cd.arm.und_r13_r14[0];
 		cpu->cd.arm.r[14] = cpu->cd.arm.und_r13_r14[1];
 		break;
-	default:fatal("arm_load_register_bank: unimplemented mode %i\n",
-		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
-		exit(1);
+	default:/*  #562: backstop, as in arm_save_register_bank().  After a
+		    debugger `cpsr=' plant of an unmodelled mode, the only
+		    caller that gets here is a DPI S-to-PC executed in that
+		    mode: it has no SPSR to copy, so Load runs on the plant.  A
+		    guest MSR, an exception or an IRQ calls Load on the MODELLED
+		    mode it switches to.  Announce once per CPU and return;
+		    r8-r14 keep their current values.  */
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

## Questions -- `<n> | <answer>`
1. FLOOR on the SHIPPED COMPOSITE: is there a smallest edit to the FIX that keeps all 47 rows green?  Give the
   DENOMINATOR (which cells and shapes you swept).  Test the generated grid's own claim (`grid cov`: every
   path x outcome x bit x polarity cell observed, G2 at every label, G3 all 25 unmodelled values per path, G4).
2. `M_msr_argmask`: is DISCLOSURE (clause (e)) the right grade, or is the loop row OWED (a floor cell of the repair)?
   Argue from the repair's own DEPENDS-ON (its comment says "only the LOCAL mask changes: ic->arg[] is a cached
   translation").
3. Records: is any contract / NOT CLAIMED / PRETABLE5 / tally line false?  Including the corrected ic->arg[] sentence
   and its account of when debugger() clears translations.
4. The gate 14 section: does it parse, score and pin correctly (it is tested against repair 5's fixed and HEAD logs:
   fixed -> 47 emitted, 0 FAIL, 47/47, REDS none; HEAD -> 47 emitted, 29 FAIL, 18/47)?  Anything it lets through?
**If, while verifying, you found something ELSE -- say so.**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
