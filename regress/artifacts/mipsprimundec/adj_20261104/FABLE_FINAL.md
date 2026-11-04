# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 16:48:38Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-teleport-mpu/aa05fc8a-6788-40de-b057-e936cb367655.jsonl`
* session: `https://claude.ai/code/session_015fEQzKhfhWqhRmE7tixQpV`   trigger: `trig_013iRuJLiLoL1z87DMkzT5yg`   packet: `_scratchpad/cloud_fable_20261103/prompt_mipsprimundec_FINAL_COMPACT.md`
* the answer's message: timestamp 2026-11-04T16:35:32.842Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDFINAL_MPU_20261104`: present; 22618 characters; PART markers N = 34, present 34, MISSING none; `END OF PARTS`: YES
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDFINAL mipsprimundec: 11 RULINGS 2 CHANGES 24 ROWS VERDICT:GO-WITH-CHANGES

---
PART 1/34
CLOUDFINAL_MPU_20261104
model: claude-fable-5-1 (configured id; the serving model may differ)
Evidence basis: the compact packet only. Measured: the rung-3 witness on HEAD, v3 MEASURED, the v3b measurement in REVIEW_V3R, the 24KEc/R5000/delay-slot tables. Read: the Opus manual-reading excerpt (quoted file:line), grok's consolidation with its source quotations, both diffs. Omitted: pass-1 briefs, both Opus pass-1 readings, the four share-findings answers. No repository, no manual text beyond the quoted lines. No ruling below depends on omitted text; rulings that rest on a reading rather than a measurement are marked REASONED or UNSETTLED.
VERDICT: GO-WITH-CHANGES. Adopt v3 plus v3b (D1 = Reserved Instruction on ISA III) plus one comment amendment on 0x1d.

PART 2/34
1. EVIDENCE BASIS, detail and rank.
Rank 1, measurements (CHECKED-IN-PACKET): HEAD stops the CPU on all 8 words on R4400 and R3000 (16/80, controls OK). v3 scores 80/80 and changes exactly five cells (mdmx x3 to RI; R3000 ldc2/sdc2 to RI). v3b changes exactly two more (R4400 lwc3/swc3 CpU CE=3 to RI). 24KEc, R5000 and 5KE tables; JALX in a delay slot gives BD with EPC = the branch.
Rank 2, quoted primary sources: mips-iv.txt :1366 :1372 :1380 :1388 :1415 :1447; mips_r4000.txt :5823 :5834; mips32_volII.txt :690 :1782; mips64_volII.txt :2046; idt_r30xx.txt :17148 :18335-18336; machine_pmax.c :81 :170.
Rank 3, seat readings (grok): coproc[2] never assigned; HI6_COP3 raises CpU only when coproc[3] is NULL; the outer switch lacks exactly 0x1d 0x32 0x36 0x3a 0x3b 0x3e.

PART 3/34
1. EVIDENCE BASIS, limits.
The witness exc rows accept ExcCode 10 OR 11, so the witness alone cannot see V3-1 or D1; only the per-word tables can. The ISA II cell is unobservable (R6000 and Allegrex fail to construct). No session selected -C R5900. No row sets Status.CU2 or CU3, runs user mode, or boots pmax/arc.
PROVISIONAL points (packet cannot settle): the subject of the sentence at idt_r30xx.txt:18335 (U1); every R5900 claim (U5); whether mips_cpu_types.h holds any Release 6 CPU (U6 below). Everything else is ruled on what the packet shows.

PART 4/34
2. RULINGS. Format: opcode, level, result, warrant, mark.
R1. 0x1d JALX, every ISA level: Reserved Instruction (RI, ExcCode 10). Warrant: reserved on MIPS I-IV (mips-iv.txt:1372-1396; mips_r4000.txt:5823 asterisk, :5834 "cause reserved instruction exceptions in all current implementations"); on MIPS32/64 JALX exists only with MIPS16e or microMIPS, neither in the tree (mips32_volII.txt:690; mips64_volII.txt:2046). Measured under v3: RI on R4400, R3000, 24KEc, R5000; in a delay slot RI with BD set and EPC = the branch. CHECKED-IN-PACKET. Code: v3 arm stands; comment amended (change C2, below).

PART 5/34
R2. 0x1e, non-R5900 CPUs, every level: RI. Warrant: reserved on MIPS I-IV (mips-iv.txt:1372-1404); MIPS32 RI unless MSA is implemented (mips32_volII.txt:1782); MIPS64 marks the MDMX cell as an extension that is RI when not implemented (epsilon, mips64_volII.txt legend as read). Measured: v3 turns the three STOP cells (R4400, R3000, 5KE) into RI/10 with EPC = the planted PC and PC = the general vector; 24KEc and R5000 also RI. CHECKED-IN-PACKET. Code: V3-2 verbatim.

PART 6/34
R3. 0x1e on the R5900 (the LQ half, HEAD 5565-5568): NOT changed by this fix; the arm keeps its TODO and goto bad. Warrant: LQ is a real EE instruction, so neither RI nor CpU is "the exception the manual prescribes"; a 128-bit load is a feature, and no R5900 manual is on file. The stop remains a defect of the same class and is FILED separately ("R5900 LQ/SQ unimplemented: stops the CPU", together with HI6_SQ_SPECIAL3). REASONED; disclosed as unobservable (no session has selected -C R5900). This is a scoping ruling, not an endorsement of the stop.

PART 7/34
R4. 0x32 LWC2 and 0x3a SWC2, every ISA level: Coprocessor Unusable (CpU, ExcCode 11) with Cause.CE = 2. Warrant: coprocessor-2 word loads and stores are defined from MIPS I on; the tree never assigns coproc[2] (grok source reading), so the result that HI6_COP2's NULL test and the #236 COP1 idiom already give is CpU CE=2; the witness control COP2 word measured CE=2 with the right EPC and vector on both CPUs. Measured under v3 on every built CPU. CHECKED-IN-PACKET for the measured states; the CU2 = 1 state is U2 (MIPS32/64 Vol II says RI there; MIPS I-IV undefined), disclosed as unobservable. Code: v3 arm verbatim.

PART 8/34
R5. 0x36 LDC2 and 0x3e SDC2 on ISA I: RI. Warrant: the doubleword coprocessor loads/stores appear in the MIPS II map, not the MIPS I map (mips-iv.txt:1372 vs :1415); the tree already gates LDC1/SDC1 the same way (HEAD 5527-5530); opcodes_mips.h marks both MIPS II; consensus 1 of all four share-findings seats. Measured: R3000 ldc2/sdc2 go from CPU/11/ce=2 (draft) to RI/10/ce=0 (v3). CHECKED-IN-PACKET.
R6. 0x36/0x3e on ISA II and up: CpU CE=2. Measured on R4400, 5KE, 24KEc, R5000. The ISA II cell itself is unobservable: a gate written `<= 2` is indistinguishable from `< 2` on every CPU the tree can build; the detector discloses that cell. Code: V3-1 verbatim, gate `isa_level < 2`.

PART 9/34
R7. 0x33 LWC3 on ISA I and II: CpU CE=3. Warrant: the MIPS I and MIPS II maps list LWC3 as a coprocessor operation (pi) (mips-iv.txt:1372, :1380); idt_r30xx.txt:17148 gives CpU for LWC3 on the R30xx. Measured: R3000 CPU/11/ce=3 under v3 and v3b. CHECKED-IN-PACKET. The ISA II cell is unobservable; U4 (MIPS II-only mode on a MIPS III/IV part gives RI) does not apply: the fork has no such mode bit and no native ISA II CPU constructs.
R8. 0x33 on ISA III: RI (D1, v3b). Warrant: mips-iv.txt:1366 (coprocessor-3 instructions "were removed or changed to another use starting in MIPS III"); :1388 Table A-39 leaves the cell empty; mips_r4000.txt:5823 Figure A-2 asterisk and :5834. Measured under v3b: R4400 lwc3 RI/10/ce=0, EPC and vector right. CHECKED-IN-PACKET.

PART 10/34
R9. 0x33 on ISA IV, MIPS32, MIPS64: PREF, executed as a nop (PC + 4, no exception). Unchanged from HEAD; measured on 5KE (HEAD and v3), R5000 and 24KEc. The fix must and does leave this arm first. CHECKED-IN-PACKET. Release 6 note: on Release 6 the 0x33 cell is no longer PREF; whether the tree models any Release 6 CPU is U6 (I cannot read mips_cpu_types.h); if none, nothing changes.

PART 11/34
R10. 0x3b SWC3 on ISA I and II: CpU CE=3 (this rules U1). Both sides: the MIPS IV manual's MIPS I map gives pi (CpU) for the cell pair (mips-iv.txt:1372); IDT at idt_r30xx.txt:18335-18336 says "the instruction referencing coprocessor 3 causes a reserved instruction exception, not a coprocessor unusable exception". Why CpU: (a) the IDT sentence is quoted without its subject, so the packet cannot show it is about SWC3 rather than, say, the R3041/R3081 CU3 handling; (b) IDT itself gives CpU for LWC3 at :17148, and no architecture distinguishes the load from the store; (c) for an isa_level 1 arm the architecture map is the rank-1 source, the implementation manual rank 2. Measured: R3000 swc3 CPU/11/ce=3 under v3 and v3b. UNSETTLED at source level; ruled on the arguments as they stand; the R3000 swc3 row is pinned to this ruling and flagged as such.

PART 12/34
R11. 0x3b SWC3 on ISA III and up: RI (D1 for ISA III, v3b). Warrant: ISA III as in R8 (Table A-39 empty; R4000 Figure A-2 asterisk); ISA IV map reserved (mips-iv.txt:1396 as read); MIPS64 Rev 2.50 asterisk; MIPS32 Rev 6.04 marks the cell 6R. U3 (MIPS32 before Release 6): the Rev 6.04 cell shows only the Release 6 class, but MIPS64 Rev 2.50, the same era, marks it reserved, and there is no source that defines 0x3b on any MIPS32 part, so RI stands. Measured: R4400 swc3 RI under v3b; R5000, 24KEc and 5KE swc3 RI under v3 and v3b. CHECKED-IN-PACKET for the measured cells; REASONED for pre-R6 MIPS32.

PART 13/34
D1, decided: v3b (RI on ISA III for both 0x33 and 0x3b). Grok and the manual reading say RI on a removed slot; GLM and Argon say the cells are "architecturally incorrect" under v3 but should stay CE=3 "at this step". A process reason is not a design argument: counting arguments, two primary sources and zero contrary sources say RI, and the measurement shows the change is exactly two cells with no side effect on R3000, 5KE, 24KEc or R5000. v3b's gate (`isa_level >= 3` on SWC3; an `== 3` arm on LWC3 after the PREF test) satisfies the MIPS I 0x33 row and the MIPS III rows at once, which a single `< 4` arm cannot. CHECKED-IN-PACKET.

PART 14/34
D2, decided in two halves. (i) Wording: the draft/v3 sentence "no COP3 is modelled" is false as written, since machine_pmax.c:81 and :170 allocate coproc[3] (R2020/R3220 write-back unit); v3b's wording "no coprocessor-3 load or store is implemented" is true as written because no LWC3/SWC3 handler exists for that object. Adopted. (ii) Behaviour: what LWC3/SWC3 should do on pmax with Status.CU3 set and a live coproc[3] is not stated by any seat or source in the packet; the fix raises CpU CE=3 there, which is the same result HI6_COP3 gives for a NULL pointer and strictly better than a stopped CPU. FILED separately; disclosed as unobservable (no pmax session). REASONED.

PART 15/34
3. THE FIX. The exact code is v3.diff with v3b applied on top, with one further comment amendment. Everything not quoted in PARTS 16-21 is v3/v3b verbatim. The two changes against v3 are:
C1. D1: the v3b hunks for HI6_SWC3 and HI6_LWC3 exactly as in the packet (SWC3 gate `>= 3`; LWC3 gains the `== 3` RI arm between the PREF arm and the CpU arm; comments as v3b writes them).
C2. The 0x1d comment: replace "exists only with MIPS16e" with the true sentence quoted in PART 19.
The build and warnings status of v3 and v3b are measured (make rc 0, 0 warnings, each in its own clone); C2 touches a comment only. Fill every #NNN with the issue number before commit.

PART 16/34
Arm 1 of 6, LWC2/SWC2 (v3 verbatim; each comment sentence checked true against the packet: coproc[2] never assigned; X(cpu) is the #236 idiom; HEAD fell to default goto bad):
```
	case HI6_LWC2:
	case HI6_SWC2:
		/*  #NNN: coprocessor-2 word loads and stores.  No COP2 is
		    modelled on any emulated MIPS, so the architectural result is
		    Coprocessor Unusable (Cause.CE = 2), as X(cpu) already raises
		    for COP1 (#236).  Before this they fell to default: goto bad,
		    which stopped the emulated CPU from any privilege level.  */
		ic->f = instr(cpu);
		ic->arg[0] = 2;
		break;
```

PART 17/34
Arm 2 of 6, LDC2/SDC2 (v3 verbatim):
```
	case HI6_LDC2:
	case HI6_SDC2:
		/*  #NNN: the doubleword forms are MIPS II; below that the
		    encoding is reserved, as LDC1/SDC1 already are (above).  */
		if (cpu->cd.mips.cpu_type.isa_level < 2) {
			ic->f = instr(reserved);
		} else {
			ic->f = instr(cpu);
			ic->arg[0] = 2;
		}
		break;
```
x64 stays 0 on both arms, so the MODE32 tail (HEAD 5712-5724) does not rewrite them; the 24KEc ldc2/sdc2 rows guard that.

PART 18/34
Arm 3 of 6, SWC3 (v3b verbatim):
```
	case HI6_SWC3:
		/*  #NNN: through MIPS II, SWC3 is a coprocessor-3 store; no
		    coprocessor-3 load or store is implemented, so it raises
		    Coprocessor Unusable with CE = 3 whatever Status.CU3 holds.
		    MIPS III removed the coprocessor-3 loads and stores and later
		    levels keep the encoding reserved, so from ISA III on it is a
		    Reserved Instruction (MIPS IV Instruction Set rev 3.2, Table
		    A-39; R4000 User's Manual, Figure A-2).  Neither stops the
		    CPU.  */
		if (cpu->cd.mips.cpu_type.isa_level >= 3) {
			ic->f = instr(reserved);
		} else {
			ic->f = instr(cpu);
			ic->arg[0] = 3;
		}
		break;
```

PART 19/34
Arm 4 of 6, 0x1d (v3 with amendment C2; the only sentence changed is the first):
```
	case 0x1d:
		/*  #NNN: JALX is defined only together with MIPS16e or
		    microMIPS, neither of which this tree models, and on MIPS
		    I-IV the encoding is reserved: it is a Reserved Instruction
		    here (#309's REGIMM precedent), not a stopped CPU.  */
		ic->f = instr(reserved);
		break;
```
Warrant for the wording: mips32_volII.txt:690 and mips64_volII.txt:2046 name both ASEs (Astra's change 5); the manual reading records the tree has neither.

PART 20/34
Arm 5 of 6, LWC3 (v3b verbatim; the PREF arm is HEAD's and stays first):
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
			    whatever Status.CU3 holds, instead of stopping the CPU.  */
			ic->f = instr(cpu);
			ic->arg[0] = 3;
		}
		break;
```

PART 21/34
Arm 6 of 6, the non-R5900 half of HI6_LQ_MDMX (v3 verbatim; the R5900 half at HEAD 5565-5568 is untouched, per R3):
```
		/*  #NNN: MDMX is not implemented, so the encoding decodes as a
		    Reserved Instruction (as on a CPU without the MDMX ASE)
		    instead of stopping the CPU.  */
		ic->f = instr(reserved);
		break;
```
This replaces HEAD's `fatal("TODO: MDMX\n"); goto bad; /* break */`. After these six arms no primary opcode value reaches `default: goto bad` at HEAD 5708 on a non-R5900 CPU (grok's enumeration of the missing labels; REASONED, confirmed by the 80/80 witness).

PART 22/34
4. ROWS OWED. Conventions: every row wants the EXACT ExcCode and CE (the witness's 10-or-11 acceptance must be tightened, or rows 7, 8, 10, 11 cannot see D1 and V3-1), EPC = the planted PC, PC = the general vector (0xffffffff80000180 on 64-bit CPUs, 0x80000080 on the R3000, 0x80000180 on 24KEc), BD clear unless stated. Words: jalx 0x74000000, mdmx 0x78000000, lwc2 0xc8000000, lwc3 0xcc000000, ldc2 0xd8000000, swc2 0xe8000000, swc3 0xec000000, sdc2 0xf8000000. Sessions: -E testmips with -C as named. Each row names the wrong edit it catches; no row without one.

PART 23/34
Session A, -C R4400 (ISA III, 64-bit translator):
1. jalx: RI 10. Catches the 0x1d label dropped (STOP returns).
2. mdmx: RI 10. Catches V3-2 reverted, or the R5900 test inverted.
3. lwc2: CpU 11 CE=2. Catches the 0x32 label dropped; arg[0] not 2.
4. swc2: CpU 11 CE=2. Same for 0x3a.
5. ldc2: CpU 11 CE=2. Catches the LDC2 gate inverted (`>= 2`) or widened (`< 4`).
6. sdc2: CpU 11 CE=2. Same for 0x3e.
7. lwc3: RI 10. Catches D1 reverted to CpU CE=3 (v3), or the `== 3` arm dropped.
8. swc3: RI 10. Catches the SWC3 gate written `>= 4` (v3).
9. jalx in the delay slot of a taken branch: RI 10, Cause.BD set, EPC = the branch. Catches a hand-written handler that skips the pc sync that instr(reserved) does (measured in packet).

PART 24/34
Session B, -C R3000 (ISA I, MODE32 translator):
10. ldc2: RI 10. Catches V3-1 dropped (CpU CE=2 returns).
11. sdc2: RI 10. Same.
12. lwc2: CpU 11 CE=2. Catches the ISA gate applied to the combined LWC2/SWC2 case, and x64 set on that arm (the MODE32 tail would rewrite it to RI).
13. swc2: CpU 11 CE=2. Same.
14. lwc3: CpU 11 CE=3. Catches the ISA III arm written `<= 3` or `>= 1`; arg[0] not 3.
15. swc3: CpU 11 CE=3. Catches the SWC3 gate written `>= 1` or `>= 2`. PINNED to the U1 ruling; flips to RI if U1 settles for IDT.
16. jalx: RI 10. 17. mdmx: RI 10. Catch a STOP regression in the MODE32 build (both translators compile the arms; the 64-bit rows cannot see the MODE32 one).

PART 25/34
Session C, -C R5000 (ISA IV, 64-bit translator):
18. lwc3: PREF, no exception, PC = planted + 4. Catches the LWC3 ISA III arm written `>= 3`, which would eat PREF.
19. swc3: RI 10. Catches the SWC3 gate written `> 4` or `== 3`.
Session D, -C 24KEc (MIPS32, MODE32 translator):
20. ldc2: CpU 11 CE=2. 21. sdc2: CpU 11 CE=2. Catch x64 set on the LDC2/SDC2 arm (the MODE32 tail rewrites it to RI; the R3000 rows want RI there and cannot see it).
22. lwc3: PREF, PC + 4. Catches `>= 3` on the MODE32 path (isa_level 32).
Session E, default CPU (MIPS64 5KE):
23. lwc3: PREF, PC + 4. Preserves the HEAD baseline the witness measured; catches any reordering that puts a reserved arm before the PREF test.
24. swc3: RI 10. Catches a gate written `== 3` or `== 4`.

PART 26/34
Controls, kept but not counted as rows: COP2 0x48000000 gives CpU CE=2 on R4400 and R3000; LDC1 0xd4000000 gives RI on the R3000; /bin/true and a missing path must read CONTROL FAIL. Bound check: 24 rows against 17 enumerated wrong edits (several edits need one row per translator, since the 64-bit and MODE32 builds compile the arm separately).
Disclosed as UNOBSERVABLE in this tree, and to be stated in the test-variant table: the ISA II cell of V3-1 (`<= 2` versus `< 2`), every R5900 row including the 0x1e stop, Status.CU2 = 1 and CU3 = 1 states, user mode, the pmax and arc rig machines (D2), and any Release 6 behaviour (U6).

PART 27/34
5. DISAGREEMENTS SETTLED.
S1. D1, LWC3/SWC3 on ISA III: Grok and the manual reading, RI; GLM and Argon, CE=3 on process grounds while conceding the architecture. Settled by two primary sources (Table A-39, Figure A-2) and the v3b measurement showing exactly two cells move. Ruling: v3b.
S2. V3-1, LDC2/SDC2 on ISA I: all four seats RI; Astra noted the witness cannot rank RI over CpU. Settled by the MIPS I versus MIPS II maps and the R3000 per-word table (the witness is not the instrument; the table is).
S3. V3-2, MDMX: three seats RI, GLM indifferent. Settled by the draft's 72/80 measurement: the three mdmx cells stopped the CPU; v3 removes the stop.

PART 28/34
S4. Pass-1 NO-GO (Grok, Astra) and Gemini's DRAFTABLE:NO on the fix draft versus GLM's GO: settled by measurement. The draft was indeed wrong on five cells (mdmx x3, R3000 ldc2/sdc2); v3 fixes all five and nothing else moves. Both Opus readings' "four cells plus 0x1e" (omitted text, as summarised in the packet) match the manual reading in the packet, so the ruling does not depend on them.
S5. Change 4, the "no COP3 is modelled" sentence: Astra, false; Grok, testmips only. Settled by the source quotation (machine_pmax.c:81, :170): false as written, and a comment must be true on every machine, not only the measured one. v3b's wording adopted; pmax behaviour filed (D2).
S6. Change 5, the 0x1d comment: one seat, no dispute; adopted as C2. Change 6, the blank-line hunk: already dropped in v3.

PART 29/34
6. UNSETTLED.
U1. 0x3b on ISA I: ruled CpU CE=3 on the rank of sources (PART 11). Settled by: the User00 session reads idt_r30xx.txt around :18335 and reports which instruction or which part (R3041/R3081 CU3 handling?) the sentence describes, and whether :17148 (LWC3) says the same. If it is the general R30xx SWC3 rule, rows 14 and 15 flip to RI and the SWC3/LWC3 ISA I arms need an R30xx-specific test that the packet cannot define.
U2. Coprocessor-2 loads/stores with CU2 set and no coprocessor 2: MIPS32/64 Vol II says RI, MIPS I-IV undefined; the arms hard-code CpU like HI6_COP2. Settled by a probe that sets Status.CU2 before the word; until then disclosed.

PART 30/34
U3. 0x3b on MIPS32 before Release 6: ruled RI on MIPS64 Rev 2.50's asterisk; settled by a pre-R6 MIPS32 Vol II (Rev 2.x) opcode map if the User00 session has one.
U4. 0x33/0x3b on a native ISA II CPU versus MIPS II-only mode: moot while R6000 and Allegrex cannot be constructed; settled by fixing their config0 initialisation (a separate bug to FILE: "ISA II CPUs fail to construct on testmips").
U5. R5900: the 0x1e LQ stop stays (R3); V3-1 turns the 0x36/0x3e stop into CpU CE=2 on an isa_level 3 part. Settled by an EE Core manual and a -C R5900 session. REASONED, not in packet: I recall the EE core defines opcode 0x33 as PREF, which would make v3b's RI on R5900 lwc3 wrong (though still not a stop); the User00 session should check that before the R5900 test variant is written.

PART 31/34
U6. Release 6: on Release 6 the 0x33 cell is no longer PREF and the COP2 loads/stores moved to the COP2 opcode; if mips_cpu_types.h holds any Release 6 CPU, R9's nop arm and R4/R6's CpU arms are wrong for it. Settled by one grep of mips_cpu_types.h; if none, nothing changes.
U7. Whether X(cpu) consults Status.CU bits at all (it raises CpU for a NULL coprocessor regardless): matters only for U2 and D2; settled by reading X(cpu) at HEAD 148-157 with mips_cpu_exception.
To FILE separately: (a) R5900 LQ/SQ unimplemented stops the CPU; (b) pmax/arc coprocessor-3 load/store semantics with a live R2020/R3220 object; (c) ISA II CPUs fail to construct; (d) the witness's loose exc rows (10 or 11) as a tooling defect, to be tightened before the rows in PART 23-25 are banked.

PART 32/34
7. WEAKEST RULING.
R10 (U1): 0x3b on ISA I as CpU CE=3. It rests on ranking the architecture map above an implementation manual whose quoted sentence I cannot see in context, and on a symmetry argument (load and store should behave alike). It is overturned if the paragraph at idt_r30xx.txt:18335 is the R30xx-family rule for SWC3 (or for all CP3 references) and :17148 is reconciled with it; then the ISA I arms for 0x33 and 0x3b become RI on R30xx parts and rows 14-15 flip. The code change would be small (an isa_level 1 branch to instr(reserved)); the design point would still hold, since neither reading stops the CPU.

PART 33/34
Second weakest: R3, leaving the R5900 0x1e stop in place. It is overturned if the User00 session shows an existing LQ/SQ implementation elsewhere in the tree (then the arm should route to it) or rules that the robustness principle outranks architectural fidelity for an unmodelled real instruction (then RI would be the interim result, as for MDMX). Third: U3, RI for 0x3b on pre-R6 MIPS32, overturned only by a pre-R6 Vol II map that defines the cell, which I consider unlikely.
Counts: 11 rulings (R1-R11; D1 and D2 are decided inside R8, R10, R11 and the comments), 2 changes against v3 (C1 = v3b, C2 = the 0x1d comment), 24 rows.

PART 34/34
Summary for the bank: adopt v3 + v3b + C2. Every non-R5900 primary opcode now delivers RI or CpU with EPC, Cause and the vector set, measured on R4400, R3000, R5000, 24KEc and 5KE; no process exit and no machine stop remains on those CPUs. The R5900 LQ stop, pmax COP3 semantics, the ISA II construction failure and the loose witness rows are filed separately. The detector owes the 24 exact-code rows in PARTS 23-25, with the unobservable cells of PART 26 disclosed in the test-variant table.
CLOUDFINAL mipsprimundec: 11 RULINGS 2 CHANGES 24 ROWS VERDICT:GO-WITH-CHANGES
END OF PARTS
