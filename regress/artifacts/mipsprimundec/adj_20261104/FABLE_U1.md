# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 17:26:18Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-teleport-u1/04a8c223-195c-42ca-83c3-f3a32ef52145.jsonl`
* session: `https://claude.ai/code/session_015fEQzHwHSAzryU3dEb4iKh`   trigger: `trig_01A9Wvftyt2pCh2WQFaPZRGf`   packet: `?`
* the answer's message: timestamp 2026-11-04T17:18:17.167Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDU1_MPU_20261104`: present; 6055 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDU1 mipsprimundec: U1:SPLIT R10:STANDS U5:STANDS

---
CLOUDU1_MPU_20261104
model: claude-fable-5-1
VERDICT: U1 SPLIT (the textual half of my contingency fires, the governance half does not); R10 STANDS, ISA I and ISA II arms of HI6_LWC3 and HI6_SWC3 unchanged from v3b, CpU with CE=3; rows 14 and 15 keep their wants; U5 STANDS, disclosed, filed with the R5900 LQ/SQ row.

**1. U1, does the contingency fire?**

(a) The IDT text. My objection (a) in R10 is withdrawn. The sentence at :18335 sits on the SWCz page, its subject is SWCz itself, generic over z, and MFCz at :17411 says the same thing for coprocessor 3. That is the first half of the contingency, met.

Is :17148 reconciled? Not by the text. The LWCz page is silent about coprocessor 3 and its Exceptions list is the generic list for z in {1, 2}. Silence is not a contrary statement. The manual contains two explicit statements, both RI for CP3, and no explicit CpU-for-CP3 statement anywhere (the grep). The best reading is that the LWCz page omitted the CP3 line that the MFCz page remembered to include. So :17148 is reconciled by inference, not by text. I accept that inference: for the IDT R30xx family, CP3 references raise RI, loads included. My old point (b), "no architecture distinguishes the load from the store", still holds and cuts the same way.

(b) Governance. This is decisive and it is the half that does not fire. The contingency presupposed that the IDT manual is the rank-2 implementation manual for the ISA I arms. It is not. The IDT manual documents the R3041/R3051/R3052/R3071/R3081 integrated parts, which dropped the external coprocessor interface. The tree models R2000, R2000A, R3000, R3000A and TX3920. The R2000/R3000 architecture has four coprocessors: Status has CU0 through CU3, Cause.CE is two bits, and the R3000 has a CpCond3 input. For those parts, a CP3 reference with CU3 clear is exactly the case the MIPS I map legend at :1447 describes: processor state does not allow access to the coprocessor, Coprocessor Unusable. The rank-1 source and the R3000's own design agree; the IDT text describes different silicon. The TX3920 has no manual on file and falls to the architecture default.

The :1365/:1369 statements about MIPS II-only mode on MIPS III/IV processors remain U4, not modelled, and do not reach the R6000 arm.

Net: U1 SPLIT. Fires for the IDT R30xx family, which the tree does not model. Does not fire for any arm the tree has. File a note with the ruling: if an R3041/R3051/R3052/R3071/R3081 entry is ever added to mips_cpu_types.h, its CP3 arms (0x33, 0x3b, and the COP3/MFC3-class references) must be RI, with their own rows and tests.

**2. Code for the ISA I and ISA II arms of HI6_LWC3 and HI6_SWC3**

Unchanged from v3b. Behaviour: CpU, CE=3, on isa_level 1 and 2. No new test.

One conditional, comment-only item. I cannot read v3b in this turn (tool use forbidden). If the comment on those arms repeats my R10 reasoning that the IDT sentence "lacks a subject", that reasoning is now false and the comment must not say it. Replace it with this text, every clause of which is true as written:

```
/*  ISA I/II: CP3 is an architected coprocessor (Status.CU3, Cause.CE=3),
 *  so LWC3/SWC3 with CU3 clear take Coprocessor Unusable, CE=3 (MIPS IV
 *  manual, MIPS I map Table A-37 and its "pi" legend).  The IDT R30xx
 *  family manual documents Reserved Instruction for coprocessor-3
 *  references (its SWCz and MFCz pages); no IDT R30xx part is modelled
 *  in mips_cpu_types.h.  If one is added, its CP3 arms must be RI.  */
```

If the existing comment already says nothing false, leave it alone. Either way, no behavioural change and the GO-WITH-CHANGES disposition (v3 + v3b + C2) is unaffected.

**3. Rows 14 and 15**

Row 14, R3000 lwc3 (0x33): want Coprocessor Unusable, ExcCode 11, Cause.CE = 3, EPC at the instruction, stated for Status.CU3 clear as in the witness.
Row 15, R3000 swc3 (0x3b): same want.
Both stay pinned to R10. Reword the pin on row 15 (and copy it to row 14, since the IDT inference now covers the load): "IDT R30xx manual documents RI for CP3 references on SWCz and MFCz; those parts are not modelled; the R3000 has a CU3 bit and a CP3 interface, so the architecture map governs: CpU CE=3." Drop the "quoted without its subject" wording.

**4. U5, the R5900**

STANDS, disclosed. The v3b isa_level == 3 arm gives the R5900 RI for 0x33. There is no EE Core manual on file, no session selects -C R5900, and the R5900 model is already filed as incomplete on the LQ/SQ row. I will not write a CPU-specific exclusion into a hardening change on no on-file source, and without reading v3b I cannot say what an excluded R5900 would fall through to, so the "exact C" cannot be given honestly.

Add to the R5900 LQ/SQ row, marked as unsourced recollection by this ruling and not as fact: the R5900 is believed to implement the MIPS IV subset MOVN, MOVZ and PREF, and PREF occupies 0x33. If that is so, an R5900 session would take RI on a compiler-emitted prefetch. The row gives the trigger and the fix: when an EE Core manual is on file showing PREF at 0x33, exclude the R5900 from the isa_level == 3 RI arm and route it to the PREF handler, one row, one test.

**5. Weakest ruling and what overturns it**

Weakest is U5. It is decided by default, with zero on-file source in either direction, and my own recollection points the other way. It is overturned by an EE Core manual (or any rank-2 R5900 source) showing PREF at opcode 0x33, at which point the R5900 must be excluded from the ISA III RI arm.

Second weakest is U1(b). It rests on the R2000/R3000 having an architected CP3 (CU3, CE=3, CpCond3), which I hold with high confidence, but no R2000/R3000 implementation manual is on file. It is overturned by a rank-2 source for the parts actually modelled (Kane and Heinrich's R2000/R3000 reference, an R3000A datasheet, or the Toshiba TX39 core manual) stating that CP3 references raise Reserved Instruction. Then rows 14 and 15 flip for that part only, and the arm needs a per-part split, not a per-ISA one.

CLOUDU1 mipsprimundec: U1:SPLIT R10:STANDS U5:STANDS
