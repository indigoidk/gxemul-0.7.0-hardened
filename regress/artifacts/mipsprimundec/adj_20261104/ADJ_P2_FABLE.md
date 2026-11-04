# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 19:05:15Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpadjmpu/e77cf084-1634-40a1-8fcf-6aac8dd43e08.jsonl`
* session: `https://claude.ai/code/session_015fEQzJUj3esYSvzRaqgVuc`   trigger: `trig_01QA4yV7tqEVZCT5mDiMHoqB`   packet: `_scratchpad/cloud_fable_20261103/RECON_pvrrenderexit.md`
* the answer's message: timestamp 2026-11-04T19:03:05.350Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDADJP2MPU`: present; 7527 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDADJP2MPU: 23 RULINGS 16 TEXT-CHANGES 2 FILED VERDICT:APPLY-WITH-CHANGES

---
CLOUDADJP2MPU
model: claude-fable-5-1 (configured identifier; the serving model may differ)
VERDICT: APPLY-WITH-CHANGES. Wrong as proposed: P1 (drops the privilege-level clause and names a "state" instead of a distinction), P4 (its tail still says "from ISA III on" without the Release 6 carve-out), P6 (adopts a text never placed before the adjudicator), P12 (the replacement still does not say why the stop rows stay green), P19 (no sequencing against the other docstring edits). All other proposals are upheld, several with the exact text they lacked.

**P1. REFINE, L4.** The CU2 finding stands. The proposed text loses "from any privilege level", which is the hardening point of the whole fix, and "a state not modelled here" is imprecise, since the emulator does model CU2 being set. Final text:

```
/*  #NNN: coprocessor-2 word load and store.  Nothing in this
    tree creates a coprocessor-2 object and no coprocessor-2
    load or store is implemented, so the arm raises Coprocessor
    Unusable with Cause.CE = 2 whatever Status.CU2 holds, as the
    HI6_COP2 arm does.  With CU2 clear that is the architectural
    result at every ISA level; with CU2 set and no coprocessor,
    MIPS I-IV leave it undefined and MIPS32/64 Vol. II say
    Reserved Instruction, a distinction this arm does not make.
    Before this the words fell to default: goto bad, which
    stopped the emulated CPU from any privilege level.  */
```

**P2. UPHOLD, L4.** Both "#236" attributions are false on the checked record. The LWC2/SWC2 drop is absorbed by the P1 text. LWC3 ISA <= II arm, final sentence: "through MIPS II, LWC3 is a coprocessor-3 load. No coprocessor-3 load or store is implemented, so it raises Coprocessor Unusable with Cause.CE = 3, as the HI6_COP3 arm does when no coprocessor 3 is attached, whatever Status.CU3 holds, instead of stopping the CPU."

**P3. UPHOLD, L4.** JALX shipped with the original MIPS16 ASE on MIPS III parts, and Release 6 reassigns 0x1d to DAUI. The proposed text is true as written and is adopted verbatim.

**P4. REFINE, L4.** The Release 5 bound is right, but the sentence still concludes "from ISA III on it is a Reserved Instruction", which Release 6 contradicts. Final sentence: "MIPS III removed the coprocessor-3 loads and stores and later levels through Release 5 keep the encoding reserved (Release 6 reassigns it to PCREL; no Release 6 CPU is modelled), so from ISA III on it is a Reserved Instruction here (MIPS IV Instruction Set rev 3.2, Table A-39; R4000 User's Manual, Figure A-2)." The block-wide "pre-Release 6" note stays unadopted.

**P5. UPHOLD, L4.** Adopt the added sentence verbatim: "From MIPS II on: Coprocessor Unusable, CE = 2, with the Status.CU2 note under HI6_LWC2 applying."

**P6. REFINE, L4.** The MSA co-tenant should be recorded, but r2's C4 text is not quoted in the record and I will not adopt a product comment unseen. Append this sentence to the shipped MDMX comment and adopt nothing else from C4: "The same opcode (0x1e) carries MSA from Release 5 on; MSA is not implemented either, and on a CPU without it the encoding is likewise a Reserved Instruction."

**P7. UPHOLD, INFO.** Not adopted. "No coprocessor-3 load or store is implemented" is true whether or not a coprocessor-3 object is attached, and the pmax object was not checked this round.

**P8. UPHOLD, L4.** Strike SWC3 `>= 2` from the catches. D11 is that edit and is disclosed as undetected.

**P9. UPHOLD, L4.** Final clause: "LWC3: the PREF gate is `>= 4`. Widening it to `>= 3` (D15) makes the ISA III session decode lwc3 as PREF and reds the 64 lwc3 rows. The ISA III test sits in an `else if` behind that gate, so `== 3` -> `>= 3` is an equivalent edit, not a catch."

**P10. UPHOLD, L4.** Final citation: "Catches: table 1 plus the supplement, 28 of 34 variants red. D30 and D31 are green as predicted: no constructible ISA II or R5900 session on testmips."

**P11. UPHOLD, L4.** The two cells are inside the contract and disclosed. The ISA II clause must cite D30 (LWC3 `== 3` -> `>= 2`, 121/121) and the R5900 clause must cite D31 (the MDMX R5900 test made false, 121/121), each with "no constructible session on testmips: R6000 and Allegrex exit 1 before the prompt".

**P12. REFINE, L4.** "Sixteen `stop` absence rows" does not tell a reader why they survive. Final comment: "an ABSENT binary is a dead-binary run: every row fails except the sixteen `stop` rows, which assert that no stop was printed and so pass vacuously on empty output".

**P13. UPHOLD, L4.** "raised without the PC sync that instr(reserved) and X(cpu) perform".

**P14. UPHOLD, L4, docstring only.** Final text: "SYMPTOM counts stops in the sixteen main witness sessions only. A stop in the R5000, 24KEc, 5KE or delay-slot sessions is not counted here; it reds that session's exc/epc/pc rows instead."

**P15. UPHOLD, L4.** No removal. Labels: "named rows == 121 compares a static literal: it cannot fail on a run and is an edit tripwire for the name table." and "the yes/yes twin in the else branch is the green twin of the parse check: it cannot fail and records that the output parsed."

**P16. UPHOLD, L1.** This is instrument work, not product code, so it does not conflict with the four seats' text-only verdict. Add the four synthetic cases (truncated log, doubled sentinel, output after the sentinel, nonzero probe exit) to the replay and record the result. Each must red. If any stays green, the parser has a defect and that is fixed before APPLY, because a gate that cannot see a truncated log guards nothing.

**P17. UPHOLD, L4.** Final comment: "This gate launches \"$PMAX\", the generic gxemul build, not a per-CPU binary. The probe has no outer timeout; the worst case is about 37 sessions x 60 s, so a hung probe shows as a roughly 37-minute run, not as a failure."

**P18. UPHOLD, INFO.** The TABLE.md record of the D02, D17/D27, D20 and D21 gaps is sufficient.

**P19. REFINE, INFO.** Record the syntax-tree identity (docstrings stripped) of the shipped probe against the frozen copy beside MD5.txt, as #579 did. Sequencing is the missing part: make the record only after the P12, P14 and P15 edits have landed, and record the stripped-tree hash of both copies, so the record covers the probe that actually ships.

**P20. UPHOLD, L4.** Annotate r1 row 9 and r2 rows 27-28: "Superseded by measurement (D22, 121/121): the delay-slot rows do not catch a handler without the PC sync. They remain the only readers of Cause.BD and of EPC = the branch; B1, B4 and D07 red them." D22 stays DISCLOSE.

**P21. UPHOLD, FILE.** The mkdtemp leak is a code change to the measured probe. Not this round.

**P22. UPHOLD, INFO.** Superseded by the P1 text. The TABLE.md note stands.

**D. FILE Fable's shape as the helpers' own row; Opus's shape is not filed.** The breakpoint-at-the-vector shape reuses the exact EPC reader the existing exc/epc/pc rows use and adds no guest code. Opus's shape installs a guest handler, a second EPC reader and its own stop mechanism, which tests the guest as much as the emulator. Admission test, written as a prediction before the run: the eight nops and the planted word sit in one page with no sync-bearing instruction between them; the shipped build reads EPC = PLANT+32; the D22 variant reads the stale value at the last sync point and reds the row; none of the existing 121 rows changes colour. A row that fails any of those four is not admitted. No seat owes this row to the present fix.

CLOUDADJP2MPU: 23 RULINGS 16 TEXT-CHANGES 2 FILED VERDICT:APPLY-WITH-CHANGES
