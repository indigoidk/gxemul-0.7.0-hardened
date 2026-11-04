# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 17:43:06Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpmpur2/55b2bcf2-4a93-49e6-b868-a88c73b8f5e3.jsonl`
* session: `https://claude.ai/code/session_015fEQzGEpahnN3cqmL8Z1Gj`   trigger: `trig_013iRuJLiLoL1z87DMkzT5yg`   packet: `_scratchpad/cloud_fable_20261103/prompt_mipsprimundec_FINAL_COMPACT.md`
* the answer's message: timestamp 2026-11-04T17:12:38.141Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDFINAL_MPU_20261104`: present; 25527 characters; PART markers N = 32, present 32, MISSING none; `END OF PARTS`: YES
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINAL mipsprimundec: 12 RULINGS 4 CHANGES 28 ROWS VERDICT:GO-WITH-CHANGES

---
PART 1/32
CLOUDFINAL_MPU_20261104
model: claude-fable-5-1 (configured id; the serving model may differ)
Evidence basis: the compact packet only -- the roster verdict lines (A), the rung-3 witness (C), the Opus 5.5 manual-reading excerpt, v3 MEASURED, the v3 review with the measured v3b, the v3 diff against HEAD, the v3b diff against v3, and grok 4.7's consolidation. No repository, no manuals, no pass-1 briefs, no Opus pass-1 readings, no share-findings answers. PROVISIONAL on: the scope of the IDT sentence (U1), the pmax coproc[3] behaviour (D2), whether the tree has any MIPS16 decode path (U6), whether -C R5900 builds (U5).
VERDICT: GO-WITH-CHANGES. Ship v3b (v3 plus the D1 alternative) with four amendments, all to comments. 12 rulings, 4 changes, 28 owed rows.

PART 2/32
Grading of claims. Measurements in C, v3 MEASURED and v3b MEASURED are CHECKED-IN-PACKET: I take the reported tables as fact. Source line citations (HEAD 5527-5530, 5565-5568, 5712-5724; HI6_COP3 at 5136-5154; machine_pmax.c:81/:170; "coproc[2] is never assigned") are REASONED: two or more seats cite them concordantly, none measured them, I cannot open the tree. Manual citations are REASONED from the reading seat's quotes, except the ones the main loop re-checked against the local text (mips-iv.txt :1366/:1372/:1380/:1388/:1447; mips_r4000.txt :5823/:5834), which I grade CHECKED-IN-PACKET because the quoted cells are reproduced verbatim.

PART 3/32
Omitted text I depend on: none of the twelve rulings needs the Opus pass-1 readings or the four share-findings answers beyond what grok's consolidation quotes. The packet says both Opus readings named exactly the four cells (LDC2/SDC2 on ISA I, LWC3/SWC3 on ISA III) and the 0x1e stop; every one of those five is now fixed and measured, so nothing in them can change a ruling. If the User00 session finds the consolidation misquoted a seat, only section 5 (who said what) changes, not the design. Facts I lean on hardest: v3 80/80 with exactly five cells changed from the draft; v3b changing exactly two further cells (R4400 lwc3/swc3 CpU/11/ce=3 -> RI/10/ce=0) and nothing else on R3000, 5KE, 24KEc; R5000 under v3b: jalx RI, mdmx RI, cp2 words CpU CE=2, lwc3 PREF, swc3 RI.

PART 4/32
2. RULINGS (ExcCode 10 = Reserved Instruction, RI; ExcCode 11 = Coprocessor Unusable, CpU, with Cause.CE).
R1 0x1d JALX, every ISA level, every CPU this tree builds: RI, CE 0. Warrant: the MIPS I-IV maps mark 0x1d reserved (mips-iv.txt :1372/:1380/:1388/:1396; R4000 :5823 asterisk = RI); MIPS32/64 define it only through MIPS16e/microMIPS (mips32_volII.txt:690; mips64_volII.txt:2046), which this translator does not implement. Measured RI on R4400, R3000, 5KE, 24KEc under v3. CHECKED-IN-PACKET. Condition: if a MIPS16 decode path exists for a CPU type flagged mips16, that CPU is outside this ruling (U6).
R2 0x1e on every non-R5900 CPU, every level: RI. Warrant: reserved at MIPS I-IV (mips-iv.txt :1372..1404); MIPS32 RI unless MSA (:1782); MIPS64 RI unless MDMX; neither ASE is implemented. Measured RI on all four CPUs under v3 (the draft left it stopping: 72/80). CHECKED-IN-PACKET.

PART 5/32
R3 0x1e on the R5900, where the encoding is LQ (load quadword): this fix does not touch that branch. Warrant: LQ is a defined instruction; the manual prescribes a 128-bit load, not an exception, so raising RI would hand the guest a false architectural result and hide a missing instruction behind a plausible one. The honest state until LQ (and SQ under HI6_SQ_SPECIAL3) are implemented is the existing TODO stop, which is an "unimplemented instruction" marker, not a reserved-encoding bug. FILE separately: "R5900 LQ/SQ not implemented", whose first measurement is whether -C R5900 constructs on testmips at all. REASONED; the mandate "never stop the machine" is read as applying to encodings the architecture says to trap, which LQ on R5900 is not.

PART 6/32
R4 0x32 LWC2 and 0x3a SWC2, every level: CpU with CE = 2, hard-coded, whatever Status.CU2 holds, not gated by ISA (both exist from MIPS I). Warrant: no coprocessor 2 is ever attached (coproc[2] never assigned: REASONED from grok's source reading; the implementer greps before commit); with CU2 clear CpU CE=2 is the architectural result at every level (the reading seat: agrees). With CU2 set and no coprocessor, MIPS I-IV leave it undefined and MIPS32/64 Volume II say RI; the fix keeps CpU there to match HEAD's HI6_COP2 (#236 idiom) and the comment says so (U2 stays open as a refinement for the COP2 arm and these two together). Measured CpU/11/ce=2 on all four CPUs. CHECKED-IN-PACKET.

PART 7/32
R5 0x36 LDC2 and 0x3e SDC2 at ISA I (R3000; the pmax R2000/R3000): RI. Warrant: the MIPS I map leaves both cells reserved, MIPS II added them (mips-iv.txt :1372, :1415); LDC1/SDC1 already gate on isa_level < 2 at HEAD 5527-5530; opcodes_mips.h marks both MIPS II. All four share-findings seats, GLM's pass-1 condition and the reading seat concur. Measured RI/10/ce=0 on R3000 under v3. CHECKED-IN-PACKET.
R6 LDC2/SDC2 at ISA >= 2: CpU CE=2, same CU2 note as R4. The gate is written `< 2`, not `<= 2` or `< 3`: a native MIPS II CPU has LDC2, and the fork has no MIPS II-only mode bit for the kappa case. Measured CpU/11/ce=2 on R4400, R5000, 24KEc, 5KE. The ISA II cell itself is unobservable (R6000 and Allegrex fail config0 init); disclosed, not owed.

PART 8/32
R7 0x33 LWC3 at ISA I and II: CpU CE=3. Warrant: the MIPS I and II maps list LWC3 as a coprocessor operation (pi) (mips-iv.txt :1372/:1380; idt_r30xx.txt:17148). Measured CpU/11/ce=3 on R3000. CHECKED-IN-PACKET for the text; ISA II unobservable.
R8 0x33 LWC3 at ISA III (R4400, R4000, any isa_level 3 part except the R5900, see R3): RI. This is D1, ruled for v3b. Warrant: two primary sources quoted in the packet: R4000 User's Manual Figure A-2 prints `LWC1 LWC2 *` and :5834 defines the asterisk as "reserved instruction exceptions in all current implementations"; MIPS IV rev 3.2 Table A-39 leaves the MIPS III cell empty and :1366 says the coprocessor-3 loads/stores "were removed or changed to another use starting in MIPSIII". Measured RI/10/ce=0 on R4400 under v3b. CHECKED-IN-PACKET.

PART 9/32
R9 0x33 at ISA >= 4, MIPS32 and MIPS64: PREF, unchanged (nop, PC + 4, no exception). The witness named this as the thing a fix must not break. Measured on R5000, 24KEc, 5KE under v3 and v3b. CHECKED-IN-PACKET.
R10 0x3b SWC3 at ISA I and II: CpU CE=3. Warrant: the MIPS IV manual's MIPS I and II maps give pi for 0x3b exactly as for 0x33, and HEAD's HI6_COP3 arm already raises CpU CE=3 on the R3000 when coproc[3] is NULL, so the fork models the architectural R3000, not an IDT R30xx derivative. The IDT sentence (idt_r30xx.txt:18335-18336: a coprocessor-3 reference "causes a reserved instruction exception, not a coprocessor unusable exception") describes parts that omit CP3; modelling that deviation must change COP3, LWC3 and SWC3 together, keyed on CPU type, and is a separate bug (U1). REASONED. Measured CpU/11/ce=3 on R3000.

PART 10/32
R11 0x3b SWC3 at ISA III and above, MIPS32 and MIPS64 included: RI. Warrant at ISA III: the same two sources as R8 (`SWC1 SWC2 *` in Figure A-2; `SC SWC1 SWC2 [empty]` in Table A-39). At ISA IV: the MIPS IV map, already v3's behaviour. MIPS32 before Release 6: MIPS64 Rev 2.50 marks the cell reserved and the fork models no release bit, so U3 resolves to RI at the level the tree can express. Measured RI on R4400 (v3b), R5000, 24KEc, 5KE. CHECKED-IN-PACKET.
R12 D2 (pmax, where coproc[3] is an R2020/R3220 object): LWC3/SWC3 at ISA I raise CpU CE=3 there too, whatever coproc[3] or Status.CU3 holds. Warrant: no coprocessor-3 load or store is implemented anywhere (every seat agrees); a trappable exception beats a stopped CPU; nobody on file can state what the R2020/R3220 does on such a load, so nothing truer can be coded. The v3 sentence "no COP3 is modelled" is false as written (machine_pmax.c:81/:170, REASONED) and is replaced by v3b's wording. pmax and arc rows disclosed unobservable; FILE the device question.

PART 11/32
3. THE FIX. Apply apply_v3.py, then apply_v3b.py, then the four amendments below (C1 is v3b itself over v3; C2-C4 are comment rewrites). Control flow after the amendments is identical to measured v3b, so the v3b tables stand as the fix's measurement. Every `#NNN` is replaced by the issue number at commit. The arms as they must read:

```
	case HI6_LWC2:
	case HI6_SWC2:
		/*  #NNN: coprocessor-2 word load and store.  Nothing in this
		    tree assigns coproc[2] and no coprocessor-2 load or store
		    is implemented, so the arm raises Coprocessor Unusable with
		    Cause.CE = 2 whatever Status.CU2 holds, as HI6_COP2 does
		    (the #236 idiom).  With CU2 clear that is the architectural
		    result at every ISA level; with CU2 set and no coprocessor
		    MIPS I-IV leave it undefined and MIPS32/64 Vol. II say
		    Reserved Instruction, a state not modelled here.  Before
		    this the words fell to default: goto bad and stopped the
		    emulated CPU.  */
		ic->f = instr(cpu);
		ic->arg[0] = 2;
		break;
```
(C3: replaces v3's comment, whose "architectural result" claim held only with CU2 clear.)

PART 12/32
```
	case HI6_LDC2:
	case HI6_SDC2:
		/*  #NNN: the doubleword forms are MIPS II; below that the
		    encoding is reserved, as LDC1/SDC1 already are (above).
		    From MIPS II on: Coprocessor Unusable, CE = 2, with the
		    Status.CU2 note under HI6_LWC2 applying.  */
		if (cpu->cd.mips.cpu_type.isa_level < 2) {
			ic->f = instr(reserved);
		} else {
			ic->f = instr(cpu);
			ic->arg[0] = 2;
		}
		break;
```
(v3's V3-1 arm; one sentence added to the comment so the CU2 caveat is not silently omitted. x64 stays 0: these are MIPS II, not 64-bit-only, and the MODE32 tail would otherwise rewrite them to RI on the 24KEc.)

PART 13/32
```
	case HI6_SWC3:
		/*  #NNN: through MIPS II, SWC3 is a coprocessor-3 store; no
		    coprocessor-3 load or store is implemented, so it raises
		    Coprocessor Unusable with CE = 3 whatever Status.CU3 holds
		    and whether or not a coprocessor-3 object (pmax's R2020 or
		    R3220) is attached.  MIPS III removed the coprocessor-3
		    loads and stores and later levels keep the encoding
		    reserved, so from ISA III on it is a Reserved Instruction
		    (MIPS IV Instruction Set rev 3.2, Table A-39; R4000 User's
		    Manual, Figure A-2).  Neither stops the CPU.  */
		if (cpu->cd.mips.cpu_type.isa_level >= 3) {
			ic->f = instr(reserved);
		} else {
			ic->f = instr(cpu);
			ic->arg[0] = 3;
		}
		break;
```
(C1: v3b's gate `>= 3` replaces v3's `>= 4`; the pmax clause is added so D2 is stated, not hidden.)

PART 14/32
```
	case 0x1d:
		/*  #NNN: JALX.  The MIPS I-IV opcode maps mark 0x1d reserved,
		    and MIPS32/64 define it only through the MIPS16e and
		    microMIPS ASEs.  This translator implements neither ASE's
		    JALX, so the encoding raises Reserved Instruction (#309's
		    REGIMM precedent) instead of stopping the CPU.  */
		ic->f = instr(reserved);
		break;
```
(C2: v3's "exists only with MIPS16e, which this tree does not model" is replaced. Astra's objection stands on the quoted MIPS32 text, which names microMIPS as well; and the sentence is now about this arm, which is checkable, rather than about the whole tree, which U6 leaves open.)

PART 15/32
```
	case HI6_LWC3:
		/*  PREF (prefetch) on ISA IV and MIPS32/64:  */
		if (cpu->cd.mips.cpu_type.isa_level >= 4) {
			/*  Treat as nop for now:  */
			ic->f = instr(nop);
		} else if (cpu->cd.mips.cpu_type.isa_level == 3) {
			/*  #NNN: MIPS III removed the coprocessor-3 loads; the
			    encoding is a Reserved Instruction there (MIPS IV
			    Instruction Set rev 3.2, Table A-39; R4000 User's
			    Manual, Figure A-2).  */
			ic->f = instr(reserved);
		} else {
			/*  #NNN: through MIPS II, LWC3 is a coprocessor-3 load.  No
			    coprocessor-3 load or store is implemented, so it raises
			    Coprocessor Unusable with Cause.CE = 3 (the #236 idiom)
			    whatever Status.CU3 holds and whether or not a
			    coprocessor-3 object is attached, instead of stopping
			    the CPU.  */
			ic->f = instr(cpu);
			ic->arg[0] = 3;
		}
		break;
```
(C1, v3b as measured, plus the same pmax clause as SWC3.)

PART 16/32
In case HI6_LQ_MDMX the R5900 branch (HEAD 5565-5568) is left exactly as it is (R3). The non-R5900 tail becomes:

```
		/*  #NNN: MDMX, and on MIPS32/64 Release 5 and later MSA, share
		    this opcode; neither ASE is implemented, so the encoding
		    decodes as a Reserved Instruction, as on a CPU without the
		    ASE, instead of stopping the CPU.  The R5900 branch above
		    (LQ) is a defined instruction that is still unimplemented
		    and is not changed here.  */
		ic->f = instr(reserved);
		break;
```
(C4: v3's comment named only MDMX; MIPS32 Rev 6.04 (:1782) makes the cell RI "unless MSA implemented", so the comment must name both or it is incomplete about what the arm forgoes.) The draft's blank-line hunk stays dropped, as v3 already did.

PART 17/32
Fix conditions, owed at commit, each a one-line check the implementer records in the commit message:
(a) `grep -n 'coproc\[2\]' src/cpus/*.c src/machines/*.c` shows no assignment; if it does, strip "Nothing in this tree assigns coproc[2]" from the LWC2/SWC2 comment (the code is unchanged either way).
(b) `grep -rn mips16 src/cpus/cpu_mips*.c src/include/mips_cpu_types.h`: if a reachable MIPS16 decode path exists for a flagged CPU type, report it under U6 before commit; the 0x1d arm still ships.
(c) After both apply scripts and the comment edits, the per-word table must equal table_v3b cell for cell (the amendments touch no code).
(d) make: rc 0, 0 warnings, as both measured builds gave.
(e) A diff of the committed hunk against v3b.diff shows only comment lines changed.

PART 18/32
4. THE ROWS (28). Session = `-E testmips -C <cpu>`, probe regress/mips_primundec_probe.py extended to assert exact ExcCode and CE per cell (the witness's "10 or 11" acceptance is withdrawn: it cannot see V3-1 or D1). Every exception row also wants: CPU not stopped, EPC = the planted PC, PC = the general vector (0x80000080 on the R3000, 0xffffffff80000180 on 64-bit CPUs, 0x80000180 on the 24KEc), as the 64 witness rows already assert. Words: jalx 74000000, mdmx 78000000, lwc2 c8000000, lwc3 cc000000, ldc2 d8000000, swc2 e8000000, swc3 ec000000, sdc2 f8000000. Want shorthand: RI = 10/ce0; CpU2 = 11/ce2; CpU3 = 11/ce3; PREF = PC+4, no exception.
Rows 1-8, R3000 (ISA I, MODE32 translator): jalx RI; mdmx RI; lwc2 CpU2; swc2 CpU2; ldc2 RI; sdc2 RI; lwc3 CpU3; swc3 CpU3.

PART 19/32
What rows 1-8 catch: ldc2/sdc2 RI (5, 6) catch the V3-1 gate omitted or rejoined to the word case (the draft's CpU/11/ce=2, which the witness scored green); lwc2/swc2 CpU2 (3, 4) catch the ISA gate copied onto the word forms and a CE written 3 or 0; lwc3/swc3 CpU3 (7, 8) catch the D1 boundary over-extended downward (`<= 3`, `>= 1`) and a CE written 2; jalx/mdmx RI (1, 2) catch an arm missing from the MODE32 build. Two rows per opcode pair because each label is a separate edit.
Rows 9-16, R4400 (ISA III, 64-bit translator): jalx RI; mdmx RI; lwc2 CpU2; swc2 CpU2; ldc2 CpU2; sdc2 CpU2; lwc3 RI; swc3 RI.
Catch: ldc2/sdc2 CpU2 (13, 14) catch the V3-1 gate inverted or written `< 4`; lwc3/swc3 RI (15, 16) are D1 (v3's `>= 4` kept; the LWC3 `== 3` arm missing); mdmx RI (10) catches the RI placed inside the R5900 branch; jalx (9), lwc2/swc2 (11, 12) catch the arm missing or CE wrong on the 64-bit build.

PART 20/32
Rows 17-22, 24KEc (MIPS32, MODE32 translator, isa_level >= 4): lwc2 CpU2; swc2 CpU2; ldc2 CpU2; sdc2 CpU2; lwc3 PREF; swc3 RI.
Catch: the MODE32 tail (HEAD 5712-5724) rewrites any arm that set x64 to RI, so 17-21 catch x64 set on any coprocessor-2 arm or on LWC3 (as RI where CpU2 or PREF is wanted); 22 catches a SWC3 gate written `== 3 || == 4` or `<= 4`, which would miss isa_level 32. 24KEc jalx and mdmx are not owed: on a MODE32 build they want RI either way and add nothing to rows 1-2 (recorded as corroborating).
Rows 23-24, R5000 (ISA IV): lwc3 PREF; swc3 RI. Catch: a SWC3 gate written `> 4` (the review named this one); an LWC3 ISA III arm written `>= 3` or `<= 4` that swallows PREF.

PART 21/32
Rows 25-26, 5KE (MIPS64, the default testmips CPU): lwc3 PREF; swc3 RI. Catch: the witness's own stated invariant, "a fix must leave 0x33 alone there", and an LWC3/SWC3 gate that excludes isa_level 64; it is also the free control row (HEAD already gives PREF).
Rows 27-28, R4400, the word in a branch delay slot (the measured v3 variant): jalx -> RI with Cause.BD set and EPC = the branch; lwc2 -> CpU2 with BD set and EPC = the branch. Catch: an arm that raises through its own helper instead of X(reserved)/X(cpu) and so skips the pc synchronisation that mips_cpu_exception (cpu_mips.c:2138-2144) relies on for EPC = pc - 4 and CAUSE_BD. One CPU suffices: the exception path is shared by both translators; one row per idiom because X(reserved) and X(cpu) are separate functions.
Bound check: 28 rows, each tied above to a named wrong edit; no row asserts a cell that no enumerated edit can flip.

PART 22/32
Disclosed as UNOBSERVABLE on this tree (no row owed, must be named in the detector's output and the test-variant table):
- the ISA II cell of every gate: `< 2` vs `<= 2`/`< 3` on LDC2/SDC2 and `< 3` vs `< 2` on LWC3/SWC3 cannot be told apart, because R6000 and Allegrex fail `No initialization code for config0`;
- every R5900 cell, including the edit-slip that would make LQ raise RI (no -C R5900 session; constructibility unknown);
- Status.CU2 = 1 and CU3 = 1 states (U2): no probe variant sets them;
- user mode: the arms do not branch on mode, and the probe runs in kernel mode;
- the pmax and arc rig machines (D2): coproc[3] non-NULL on pmax is unreached by testmips;
- the IDT R30xx reading of 0x3b at MIPS I (U1): -C R3000 is the only ISA I part the probe runs.

PART 23/32
5. DISAGREEMENTS SETTLED.
S1 D1, LWC3/SWC3 on ISA III. Grok and the manual reading: RI on a removed slot. GLM and Argon: architecturally RI, but keep CpU CE=3 "at this step" on process grounds. Settled for RI (v3b) by the two primary sources quoted verbatim in the packet (Figure A-2's asterisk defined at :5834; Table A-39's empty cell with :1366), and by the fact that the two dissenters conceded the architecture; a process objection is not a design argument, and this ruling is on the design. Measured: v3b flips exactly the two cells and nothing else.
S2 D2, "no COP3 is modelled". Astra: false, pmax allocates coproc[3]. Grok: testmips leaves it NULL and nothing reaches pmax. Both right about different things; settled by rewriting the sentence to the true one (no coprocessor-3 load or store is implemented) and keeping hard-coded CpU, with the pmax device question filed. Source line outranks the convenience of the sentence.

PART 24/32
S3 LDC2/SDC2 on ISA I. The draft: CpU CE=2 everywhere. GLM's pass-1 condition, all four share-findings seats, the reading: reserved below MIPS II. Settled for RI by the MIPS I map plus the in-tree LDC1/SDC1 precedent, and measured (five-cell delta, v3). Astra's point that "the witness itself does not rank RI ahead of CpU" is why rows 5-6 now assert the exact ExcCode.
S4 The 0x1e stop. The draft kept `goto bad`; three seats and the reading: RI. Settled by measurement: draft 72/80, v3 80/80, and the manual's reserved cell at MIPS I-IV.
S5 The JALX comment. Astra alone asked to drop "exists only with MIPS16e". Settled for Astra on the quoted MIPS32 text naming microMIPS; one seat, but it is a text, not a vote. The arm is unchanged.

PART 25/32
S6 U1, SWC3 at MIPS I. IDT: RI for a coprocessor-3 reference. MIPS IV manual's MIPS I map: pi, CpU. All four seats and the draft: CpU CE=3. Settled for the fix as CpU CE=3 by symmetry with HEAD's HI6_COP3 on the same CPU; the IDT reading stays open as U1 because adopting it means a CPU-type-keyed change to three arms, not a different constant in this one.
S7 The pass-1 NO-GOs (Astra on the bug, Grok and Astra on the fix draft, Argon's DRAFTABLE:NO with 2 BROKEN). Their stated grounds, as the packet reports them, were the four wrong cells and the 0x1e stop; all five are fixed and measured in v3 and v3b. The NO-GOs are therefore moot on this packet. PROVISIONAL: the briefs are omitted; if any NO-GO rested on a sixth ground, the User00 session supplies it and section 2 is reopened on that point only.

PART 26/32
S8 Astra's blank-line hunk: dropped; v3 already did, nobody objected.
S9 U3, SWC3 on MIPS32 before Release 6. The Rev 6.04 map shows only the Release 6 class; MIPS64 Rev 2.50 marks the cell reserved. Settled for RI at the level the fork can express (isa_level 32, no release bit): a reserved cell in the only pre-R6 map on file, and no seat produced a map defining 0x3b there. Measured RI on the 24KEc.
S10 The count of labels. Grok: after six new labels no primary value reaches `default: goto bad` at 5708. Accepted as REASONED and made a fix condition in spirit: rows 1-16 execute every one of the eight words on two translators, so a label left out shows as a stop.

PART 27/32
6. UNSETTLED.
U1 (0x3b, and by the same IDT sentence 0x33 and COP3, on an IDT R30xx): settles by reading idt_r30xx.txt around :18335 for whether the sentence describes the R3000 architecture or the R30xx family, and by whether the tree's R3000 entry in mips_cpu_types.h is meant as an IDT part. If both: FILE "IDT R30xx: coprocessor-3 references are RI" covering HI6_COP3, LWC3, SWC3 together. The fix as ruled is unaffected until then.
U2 (CU2 = 1 or CU3 = 1 with no coprocessor, MIPS32/64 say RI; MIPS I-IV undefined): settles by a probe variant that executes MTC0 to set Status.CU2 before the word on the 24KEc and 5KE, plus an X(cpu) variant that tests the CU bit. HEAD's HI6_COP2/COP3 share the deviation, so FILE one refinement for all four arms rather than special-casing the loads.

PART 28/32
U3: ruled RI (S9). What overturns it: a MIPS32 Volume II of Release 2 to 5 whose opcode map defines 0x3b. None of the seats found one.
U4 (LWC3/SWC3 and LDC2/SDC2 at a native ISA II CPU): unobservable until R6000 or Allegrex construct on testmips. Settles by fixing their config0 initialisation. FILE "R6000/Allegrex not constructible on testmips"; until then the test-variant table carries the ISA II cell as DISCLOSED.
U5 (R5900): the 0x36/0x3e stop becomes CpU CE=2 under V3-1 (R5900 isa_level 3) and the 0x1e LQ stop stays. Settles by a -C R5900 session; if it builds, measure the eight words there and add the rows. FILE "R5900 LQ/SQ" (R3).

PART 29/32
U6 (new): whether any reachable MIPS16 decode path exists for a mips16-flagged CPU type. Settles by the grep in fix condition (b). If yes, JALX on that CPU needs its own ruling (mode switch, not RI) and R1 is narrowed to unflagged CPUs.
U7 (new): "coproc[2] is never assigned" is one seat's reading. Settles by fix condition (a); affects one comment clause, no code.
D2 (pmax): what an R2020/R3220 does on LWC3/SWC3 with CU3 set, and whether Ultrix or the DEC PROM ever issue one. Settles by a pmax session planting the words with CU3 set, plus a DECstation 3100 hardware reference. FILE "pmax coprocessor-3 load/store semantics".
User mode: settles by a probe variant entering user mode; no arm branches on mode, so it is a shared-path check, not a design question.

PART 30/32
TO FILE SEPARATELY (none blocks this fix):
F1 R5900 LQ/SQ unimplemented (the remaining stop in HI6_LQ_MDMX and HI6_SQ_SPECIAL3), with -C R5900 constructibility as step one.
F2 IDT R30xx coprocessor-3 = RI deviation, if U1 resolves that way; three arms together.
F3 CU2/CU3-set with no coprocessor on MIPS32/64 should be RI; covers HI6_COP2, HI6_COP3 and the six load/store arms.
F4 R6000 and Allegrex fail config0 initialisation on testmips.
F5 pmax R2020/R3220 LWC3/SWC3 semantics.
F6 Any other reachable `goto bad` (secondary-opcode reserved slots, SPECIAL2/SPECIAL3 holes): outside this bug's six labels and two TODO arms; the probe's method transfers directly.

PART 31/32
7. WEAKEST RULING. R10 (SWC3 at ISA I = CpU CE=3) is the weakest: it rests on one map cell (pi) and on symmetry with HEAD's HI6_COP3, against a primary-source sentence from IDT that says RI, whose scope I could not read. It would be overturned by the IDT context showing the sentence describes the R3000 architecture itself, or by the tree's R3000 entry being documented as an IDT R30xx part; then rows 7 and 8 flip to RI/10/ce0 and the change is a CPU-type test around the `else` branches of LWC3 and SWC3 plus the same in HI6_COP3, a small edit with no structural effect. Second weakest: R3 (leaving the R5900 LQ stop). It would be overturned by a reading of the mandate that unimplemented defined instructions must also trap; even then the honest remedy is implementing LQ/SQ, not RI, so the fix text would not change, only the filing's priority.

PART 32/32
Recap for a reader of this part only: v3b is the design, with the LDC2/SDC2 ISA I split, the 0x1e RI, the coprocessor-2 words at CpU CE=2, JALX at RI, and LWC3/SWC3 at CpU CE=3 through MIPS II and RI from MIPS III (PREF unchanged from ISA IV). Four comment amendments make every product comment true as written. 28 exact-ExcCode rows are owed on R3000, R4400, 24KEc, R5000, 5KE and two delay-slot cases; the ISA II, R5900, CU-set, user-mode, pmax/arc and IDT cells are disclosed as unobservable. Six items are filed separately; nothing filed blocks the fix.
CLOUDFINAL mipsprimundec: 12 RULINGS 4 CHANGES 28 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS
