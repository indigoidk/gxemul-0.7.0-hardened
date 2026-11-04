# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 18:39:34Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpmpup2o/9e564efc-0c05-407b-a0ed-1f883da43de6.jsonl`
* session: `https://claude.ai/code/session_015fEQzJLJnxwFmPwDDyoAuA`   trigger: `trig_01N1ZoWpRd57bAcQ4qRpj4Hc`   packet: `_scratchpad/w_mpu/P2_MPU_cloud.md`
* the answer's message: timestamp 2026-11-04T18:30:19.565Z, model field `claude-opus-5-5` (all assistant models in the transcript: ['claude-haiku-5-5', 'claude-opus-5-5'])
* delivery token `CLOUDP2MPU`: present; 8806 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDP2MPU: 171 CHECKED 4 FALSE 4 FLOOR-GAPS D22:DISCLOSE VERDICT:REPAIR-NEEDED

---
CLOUDP2MPU
model: claude-opus-5-5 (configured model; the model serving this turn may differ)
VERDICT: REPAIR-NEEDED. The code can ship as it stands. Two shipped fix comments and two probe docstring sentences are false as written. The repair touches text only and changes no control flow.

**1. The fix compared with the rulings**

**Code.** The code matches v3 with v3b applied, arm for arm:
- LWC2/SWC2 raise Coprocessor Unusable with CE 2.
- LDC2/SDC2 are Reserved Instruction below ISA II and Coprocessor Unusable with CE 2 from ISA II on.
- SWC3 is Reserved Instruction from ISA III on (`>= 3`, v3b's gate) and Coprocessor Unusable with CE 3 below.
- 0x1d is Reserved Instruction.
- LWC3 is PREF from ISA IV, Reserved Instruction at ISA III (`== 3`) and Coprocessor Unusable with CE 3 below.
- The non-R5900 MDMX tail is Reserved Instruction, and the R5900 branch is untouched.

It is also token for token the code in r2's section 3, so r2's condition (c) holds by inspection.

**Comments.** Every comment except 0x1d's is v3's text unchanged. I cannot check the 0x1d first sentence against r1's exact C2 wording because the packet does not contain it. Separately, r2 counts the pmax "coprocessor-3 object attached" clause on SWC3 and LWC3 as part of C1, and the shipped text lacks it. The shipped sentence "no coprocessor-3 load or store is implemented" is true without that clause, so the clause is optional wording either way.

**C3 is owed.** This shipped sentence is false as written:
> "No COP2 is modelled on any emulated MIPS, so the architectural result is Coprocessor Unusable (Cause.CE = 2)"

With Status.CU2 = 1 and no coprocessor 2 present, MIPS32/64 Vol. II give Reserved Instruction, and MIPS I–IV leave the result undefined. The arm raises Coprocessor Unusable whatever CU2 holds, so the comment calls a result architectural that is only architectural when CU2 is clear. The minimal repair is to insert "with Status.CU2 clear". The same sentence has two parts I cannot settle from this packet:
- "No COP2 is modelled on any emulated MIPS" is a claim about the whole tree; r2's condition (a) grep settles it.
- "as X(cpu) already raises for COP1 (#236)": both r2 and the probe describe #236 as the HI6_COP2 arm, not COP1. Check this before landing.

The LDC2/SDC2 sentence that r2 adds is optional. The shipped LDC2 text is true and only omits the CU2 caveat. If you apply C3, the cross-reference is cheap to add.

**C4 is optional.** "MDMX is not implemented, so the encoding decodes as a Reserved Instruction (as on a CPU without the MDMX ASE)" is true as written. Leaving out MSA makes it incomplete, not false.

**The shipped 0x1d first sentence is also false as written:**
> "JALX is defined only together with MIPS16e or microMIPS, neither of which this tree models"

JALX was introduced with the original MIPS16 ASE (not "e"), which shipped on MIPS III parts such as the NEC VR41xx. Release 6 also reassigns 0x1d to DAUI, though no Release 6 CPU is in the tree. r2's wording, "MIPS32/64 define it only through the MIPS16e and microMIPS ASEs; this translator implements neither ASE's JALX", is scoped so that it is true. "Neither of which this tree models" is UNSETTLED until r2's condition (b) grep for mips16 runs. GXemul's hpcmips VR41xx CPU types make that grep matter.

**2. The detector**

**Contract sentences that are false as written:**
- **The SWC3 `>= 2` claim.** CLAUSE (e) lists SWC3 `>= 2` among the edits the probe catches. The same docstring then discloses it as not caught (D11, 121/121). Remove `>= 2` from the catches list.
- **The LWC3 `>= 3` claim.** CLAUSE (e) says LWC3's ISA III arm "written `>= 3` so that it eats PREF (R5000, 24KEc, 5KE rows)". In the shipped structure that arm is an `else if` after the `>= 4` PREF test, so `== 3` → `>= 3` is an equivalent edit. It eats nothing and no row reds. The sentence describes a reordered arm that does not exist. Delete it, or restate it as "the PREF gate `>= 3`" (D15), whose catching rows are 64 lwc3, not R5000/24KEc/5KE.

**Claimed in CLAUSE (e) but not measured:** LWC3 `>= 1` and SWC3 `== 4`. Both should red: 32 lwc3 exc for the first, and 64/24k/5ke swc3 exc for the second. Either add them to the table or mark them predicted.

**Rows whose observable cannot vary under their variant:** among 121 rows, only `64 ds epc/bd` and `64 dsc epc/bd` against the no-PC-sync class (D22, item 3).

The arithmetic checks out:
- 121 rows: 1 + 38 + 41 + 33 + 8.
- Pre-fix 28/121: 16 controls, 3 extra `live pc` rows and 9 PREF rows.
- Null-binary 16/121: the 16 stop rows.
- 25 of 29 variants red.

**Floor gaps:** 4 in all, 2 of them absent from the table:
- D01 (LDC2/SDC2 `< 2` → `<= 2`): in the table, disclosed.
- D11 (SWC3 `>= 3` → `>= 2`): in the table, disclosed.
- **Absent: `else if (isa_level == 3)` → `else if (isa_level >= 2)` on LWC3.** This changes only the ISA II cell, which moves from Coprocessor Unusable CE 3 to Reserved Instruction. I expect no row to red. The docstring's ISA II disclosure covers it in general terms, but PRETABLE section 3 tests the edges of `== 3` only at 3 and 4.
- **Absent: the MDMX arm's `rev == MIPS_R5900` test weakened to false.** The R5900 would then take Reserved Instruction instead of stopping, and I expect no row to red. It is covered by the "every R5900 behaviour" disclosure.

Both absent gaps should go into the table as measured D rows.

**Denominator:** 171 items checked:
- 12 shipped comment sentences
- 22 docstring contract sentences
- 121 rows
- 8 gate check kinds
- 8 predicates the edited lines depend on (6 edited plus the R5900 test and the MODE32 tail)

**3. D22: DISCLOSE**

A handler that raises without the PC sync is a replaced body. It is not a reinstated defect, a weakened predicate or a swapped operand, so it lies outside the floor bound. The fix also edits neither X(reserved) nor X(cpu). Both are pre-existing shared handlers that the existing LDC1 and COP2 arms already use.

What is owed instead:
- Amend the ruling's text that says the delay-slot rows catch this class; it was measured false.
- Fix the disclosure sentence's grammar. It should read "raised without the PC sync that instr(reserved) and X(cpu) perform".

If a free-running row is ever wanted, it would look like this:
- Plant `nop; nop; <word>` at PLANT.
- Place a handler at the general vector: `mfc0 k0, EPC; move v0, k0`, then a testmips console-halt store.
- Run with `continue` and no breakpoint, then assert `v0 == PLANT+8`.

Two parts of that are UNSETTLED from this packet:
- Whether GXemul's dyntrans forces one-instruction-at-a-time execution, and so keeps the PC synced, when any breakpoint is set. If it does, a breakpoint-based row is also blind to this class.
- Whether `reg ,0` is still readable after a guest halt in a `-x` stdin session.

**4. The gate block**

Two checks cannot fail:
- `check "... output parses" "yes" "yes"` in the `else` branch is a tautology. The real test is the `if` condition, which is acceptable.
- `check "... named rows" "${#MPUNAMES[@]}" 121` counts a static literal array, so it is a self-check of the script edit, not of the run.

The per-row regex is sound. Names are at most 16 characters inside an 18-character field, which guarantees at least two padding spaces. No name is a prefix of another followed by two spaces. Duplicate names are asserted against in the probe.

**The replay is not enough.** All 34 logs are complete records, so the replay never exercises three failure paths:
- the no-unique-record branch, for a truncated or doubled sentinel
- the sentinel-not-last check
- the `mpurc != 0` check, since a replayed log has no exit status

Add three synthetic logs: one truncated (simulating a timeout kill), one with the sentinel twice, and one with trailing stderr after the sentinel. Then run the block once against a probe that exits 1.

**5. Anything else, by severity**
1. **(Medium)** The TABLE has no D02, D17, D20 or D21. Record why each number was dropped.
2. **(Medium)** `symptom_hits` counts only the 16 main witness sessions. A stop in the r5k, 24k, 5ke or delay-slot sessions is caught only through the exc, epc and pc rows, not through SYMPTOM. Either pass `count_symptom=True` on those sessions or say so in the docstring.
3. **(Low)** The gate launches with `"$PMAX"`. Confirm it is the fixed generic gxemul build. The probe also allows up to about 37 sessions × 60 s ≈ 37 minutes with no outer timeout.
4. **(Low)** PRETABLE's claim-to-row map has no entries for "as X(cpu) already raises for COP1 (#236)" or "No COP2 is modelled on any emulated MIPS".
5. **(Low)** PRETABLE's B1 prediction named two `24k … stop` rows that do not exist (the 24KEc sessions have no stop rows); TABLE.md already notes this.

CLOUDP2MPU: 171 CHECKED 4 FALSE 4 FLOOR-GAPS D22:DISCLOSE VERDICT:REPAIR-NEEDED
