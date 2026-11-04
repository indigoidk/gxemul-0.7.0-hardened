# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 18:39:30Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpmpup2f/fcc30482-d105-413c-9c91-5c89faab84e6.jsonl`
* session: `https://claude.ai/code/session_015fEQzKk8HHJ2A2Jz5DkxPc`   trigger: `trig_01A2N9wmVLCDG7friC3zsCpV`   packet: `_scratchpad/w_mpu/P2_MPU_cloud.md`
* the answer's message: timestamp 2026-11-04T18:27:44.226Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDP2MPU`: present; 8550 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDP2MPU: 95 CHECKED 3 FALSE 4 FLOOR-GAPS D22:DISCLOSE VERDICT:REPAIR-NEEDED

---
CLOUDP2MPU
model: claude-fable-5-1 (configured identifier; the serving model may differ)
VERDICT: REPAIR-NEEDED (text only: one false contract sentence in the probe's docstring, one overbroad shipped comment sentence that C3 was written to fix, one comment sentence false for Release 6; no code, table or gate change; the measured tables stand)

1. THE FIX vs THE RULINGS

Code: the diff's code lines equal r2's arms line for line (LWC2/SWC2 cpu+2; LDC2/SDC2 `< 2` RI else cpu+2; SWC3 `>= 3` RI else cpu+3; 0x1d RI; LWC3 `>= 4` nop, `== 3` RI, else cpu+3; LQ_MDMX non-R5900 tail RI+break, R5900 branch untouched). The 0x1d comment carries r1's C2 (MIPS16e or microMIPS, #309 precedent). So the diff is v3 + v3b + C2 as far as the packet lets me check; I cannot cmp against v3b.diff itself, so condition (e) stays with the implementer.

C3 (LWC2/SWC2): OWED. Shipped sentence false as written: "No COP2 is modelled on any emulated MIPS, so the architectural result is Coprocessor Unusable (Cause.CE = 2)". The code raises CpU whatever Status.CU2 holds. With CU2 set and no coprocessor 2, MIPS I-IV leave the result undefined and MIPS32/64 Vol. II say Reserved Instruction. The 24KEc and 5KE are MIPS32/64 and both sit in the table, so the sentence claims architectural correctness in a state where the arm gives the wrong exception. It needs the CU2-clear qualifier (r2's text, or one clause). Comment-only; control flow unchanged; conditions (c) and (e) survive.

C4 (MDMX): optional. "MDMX is not implemented, so the encoding decodes as a Reserved Instruction (as on a CPU without the MDMX ASE)" is true as written; naming MSA adds completeness, not correctness.

Also noted: the 0x1d sentence "neither of which this tree models" is a whole-tree claim the packet cannot verify (U6); it is true only if condition (b)'s grep is clean, and r2's arm-scoped wording would not depend on that. The r2 pmax clauses on SWC3/LWC3 are optional; the shipped sentences are true without them.

One more shipped sentence is false against the architecture, though not against the code (SWC3 comment): "MIPS III removed the coprocessor-3 loads and stores and later levels keep the encoding reserved". MIPS32/64 Release 6 assigns 0x3b to PCREL (ADDIUPC/AUIPC/ALUIPC/LWPC). The tree models no Release 6 CPU and the probe discloses Release 6, so bound the claim ("through Release 5"). Low severity.

2. THE DETECTOR

Denominator: 21 docstring sentences; 12 shipped comment sentences; all 29 variants' red-row lists recomputed from the code paths (all 29 counts reproduce, so the 121-row arithmetic and the 28/121 pre-fix count reproduce too); the 9 gate check kinds and the row regex; about 28 further in-bound edits enumerated beyond the table (label drops, gate rewrites, helper swaps cpu/reserved, arg[0] dropped, six missing-break fallthroughs, both MDMX guard weakenings).

False contract sentence (1): the CLAUSE (e) "catches" sentence lists the SWC3 gate "written ... `>= 1` or `>= 2`" as caught; D11 is exactly `>= 2` and scored 121/121, and the same docstring discloses it two sentences later. Strike `>= 2` from the catches list. The same sentence also lists edits with no table row (the LWC3 ISA III arm dropped, LWC3 `>= 1`, SWC3 `== 4`); my trace says each reds (64 lwc3 exc; 32 lwc3 exc; 64/24k/5ke swc3 exc) but they are predicted, not measured, and "Measured: 25 of 29" right after implies otherwise. Separate measured from predicted.

Loose, not false: "CONTROL rows prove the apparatus on each CPU: ... cpu2 ... ri" (the R5000/24KEc/5KE have only a live control; the later sentence says so).

Dead observables: none. Every row varies under some tabled variant except "neg apparatus" (a harness control by design). The delay-slot epc/bd rows do vary (B1, B4, D07 red them) but not under the handler the rulings assigned them; see 3.

In-bound variants absent from the table and undetected (2), both in classes the contract already discloses:
- LWC3: `} else if (cpu->cd.mips.cpu_type.isa_level == 3)` written `>= 2`. Rowed CPUs unchanged (1 CpU, 3 RI, 4/32/64 PREF); only the ISA II cell moves (RI instead of CpU CE=3). No row reds. Same class as D11; disclosed under "LWC3/SWC3".
- LQ_MDMX: the R5900 guard made always-false (branch deleted or `&& 0`). The edited RI line then also serves the R5900, whose LQ becomes RI instead of a stop. No R5900 session, so no row reds. Disclosed under "every R5900 behaviour". A row is possible (`-C R5900`, 0x1e, want stop present) but it would pin R3's untouched stop as behaviour; disclosure is the better choice.
Also absent but caught in principle: LWC2 and LDC2 single-label drops (twins of D25/D26), SWC3 `== 4`, PREF `== 4`, every missing-break fallthrough, every cpu/reserved helper swap. Not floor gaps.

Floor gaps total: 4 cells (D01 and D11 tabled; the two above absent), all disclosed, none undisclosed.

3. D22

DISCLOSE is right. The variant adds a new un-synced helper; it is not a reinstated defect, a weakened predicate or a swapped operand, so it is outside the stated bound, and the PC sync is a property of X(reserved) and X(cpu), which the fix calls and does not edit. The rulings' row-9 sentence misattributed the delay-slot rows' purpose; those rows still earn their place as the only readers of Cause.BD and EPC = branch (B1, B4, D07 red them). Annotate r1 row 9 and r2 rows 27-28 as superseded by measurement.

Mechanics, as far as this packet plus the dyntrans structure settle them: single-step keeps the PC synced (the run loop writes cpu->pc from next_ic after every call, which is one instruction when stepping), consistent with 121/121 on D22a/D22b. Also, the first execution of any word goes through to_be_translated, whose head computes and writes the word's address into cpu->pc before the handler runs, so a one-pass "continue" row would be equally blind; the sync becomes visible only on a second execution of an already translated page inside a free-running batch. Breakpoints re-firing on an already translated vector page, and `continue` resuming without single-step: UNSETTLED from this packet.

If a follow-up row is wanted for the helpers' own test (not owed by this fix), the measurable form: R4400; eight nops at PLANT..PLANT+28, the word at PLANT+32; `breakpoint add 0xffffffff80000180`; `pc=PLANT`; `continue`; `pc=PLANT`; `continue`; `reg ,0`. Want: ExcCode 10/0 (jalx) or 11/2 (lwc2), BD clear, EPC = PLANT+32, PC = vector. Under D22a/b the second pass should give EPC = PLANT (the stale batch start). Admit the row only after it reds D22a/D22b in the scratch clone; if it stays 121/121, the breakpoint or batch assumption failed and the class stays disclosed.

4. THE GATE BLOCK

Cannot fail at runtime: "named rows: ${#MPUNAMES[@]} == 121". It tests the gate script's own literal, not the probe. Keep it as an edit tripwire, but label it so. Every other check can fail and the null and HEAD logs show the controls, symptom and equality pins failing. The row regex is sound: a FAIL line ends "FAIL" and cannot match " ok$"; got/want strings carry no spaces; names have no regex metacharacters and the two-space requirement separates "64 ds" from "64 dsc".

Replay: enough for the pin. Green on exactly the six 121/121 logs shows the block is a faithful function of RESULT, CONTROL and SYMPTOM over 34 real outcomes. Not exercised: the parse-failure branch (a truncated log) and a 121/121 log with one row line mangled; both are cheap synthetic logs and neither is a shipping blocker since RESULT equality already carries the catch. Worst-case wall time is 37 sessions x 60 s, about 37 minutes, if every session hangs; acceptable, but say so in the comment. The launch variable is named "$PMAX" for a general gxemul binary; rename or comment it.

5. ANYTHING ELSE, by severity

- Variant numbering gaps D02, D17, D20, D21 are unexplained in PRETABLE and TABLE; record what they were and why dropped (traceability of the bound).
- The Release 6 overreach above also applies in spirit to the LWC2/SWC2, LDC2/SDC2 and 0x1d arms (R6 reassigns 0x32, 0x36, 0x3a, 0x3e to compact branches and 0x1d to DAUI on MIPS64 R6); only the SWC3 comment states a false universal, but a one-line "pre-Release 6" note at the top of the block would cover all six arms.
- The probe leaks its mkdtemp directory every run; add a cleanup.
- PRETABLE B1 predicted two nonexistent 24k stop rows; TABLE already notes it.
- Condition (a)/(b) grep results are not in the packet; the commit message must carry them.

CLOUDP2MPU: 95 CHECKED 3 FALSE 4 FLOOR-GAPS D22:DISCLOSE VERDICT:REPAIR-NEEDED
