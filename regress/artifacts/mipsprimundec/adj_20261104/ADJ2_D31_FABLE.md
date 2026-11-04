# Cloud routine answer, banked VERBATIM by extract_teleport.py at 2026-11-04 19:29:01Z

* source: the local transcript of `claude --teleport` -- `C:/Users/User00/.claude/projects/C--Users-User00-AppData-Local-Temp-claude-d0d925bc6bb158fc-ccd8e376-b626-4ae7-b60a-ecf2767f320e-scratchpad-tpd31mpu/9c25a884-eda0-42d5-8671-657367ac408e.jsonl`
* session: `https://claude.ai/code/session_015fEQzGigdDMnrCPcxcs1xZ`   trigger: `trig_0176ni5eXYYemtjdxvAa4hvM`   packet: `_scratchpad/cloud_fable_20261103/D31_FOLLOWUP_mipsprimundec.md`
* the answer's message: timestamp 2026-11-04T19:20:01.472Z, model field `claude-fable-5-1` (all assistant models in the transcript: ['claude-fable-5-1', 'claude-haiku-5-5'])
* delivery token `CLOUDADJ2MPU`: present; 3810 characters; PART markers N = 0, present 0, MISSING none; `END OF PARTS`: NO
* safety-classifier notices in the transcript: none
* the run's final line: CLOUDADJ2MPU: D31:ROW-OWED 4 TEXT-CHANGES VERDICT:HOLD

---
CLOUDADJ2MPU
model: claude-fable-5-1 (configured identifier; the serving model may differ)
Verdict: D31 is OWED a row, in a form that does not pin the stop; the P10/P11 texts and the contract clause change; HOLD the apply until the main loop measures the new row.

**(1) D31: ROW-OWED, not disclosed.** My pass-2 reasoning rejected a row because the only form considered was "want the stop text present", which would pin R3's untouched UNIMPLEMENTED stop as behaviour. That objection stands, but it does not cover the other form: `-E testmips -C R5900`, step 0x1e, require exit 0 and the prompt reached, and want the Reserved Instruction marker ABSENT (the same marker the other 0x1e rows want present). That row goes red under D31 (the R5900 would take RI), stays green under the fix, and stays green if LQ is ever implemented, because "0x1e is not a Reserved Instruction on the R5900" is the architectural fact the fix's R5900 test exists to preserve. It pins nothing about the stop. A reachable mutation of fix code left undetected by choice is a weaker position than detecting it with a durable assertion, so the row is owed. Fallback: if the main loop measures the absence row and it does NOT go red under D31 (the RI marker not emitted on that path), D31 reverts to DISCLOSE with the true reason "reachable on testmips but deliberately not asserted: the only observable is the pre-fix UNIMPLEMENTED stop, which R3 leaves untouched and the fix does not claim." Never again the reason "no constructible session".

**(2) Exact texts, each true as written once the row is measured.**

P10: "Catches: table 1 plus the supplement plus the D31 row, 29 of 34 variants red. D30 is green as predicted: no constructible ISA II session on testmips (R6000 and Allegrex exit 1 before the prompt: 'No initialization code for config0'). D31 is red via the R5900 row (`-C R5900`, 0x1e, exit 0, prompt reached, Reserved Instruction marker absent), which asserts only that the R5900 does not take RI on 0x1e, not the UNIMPLEMENTED stop."

P11: "... the ISA II clause must cite D01, D11 and D30 with 'no constructible session on testmips: R6000 and Allegrex exit 1 before the prompt'. D31 is no longer a disclosure; it is covered by the R5900 row, and the R5900 clause must say so."

Contract R5900 clause: "discloses, not claimed: every R5900 behaviour except one, namely that 0x1e is not a Reserved Instruction on the R5900 (asserted by the D31 row, which wants the RI marker absent and says nothing about what happens instead); the R5900's 0x1e UNIMPLEMENTED stop itself and its 0x33 [remainder of the existing clause carried over verbatim] remain disclosed, not claimed. The R5900 constructs on testmips; these behaviours are unclaimed by policy, not because they are unreachable."

If the fallback triggers, P10 keeps "28 of 34" and reads "D31 is green by choice: the cell is reachable (`-C R5900`, 0x1e) but its only observable is the untouched UNIMPLEMENTED stop, which the fix does not claim", and the contract clause drops the exception sentence but keeps the final "unclaimed by policy, not because they are unreachable" sentence.

**(3) Other text resting on the false premise.** Section A's sentence that D30 and D31 share one reason must be split; D30 keeps the ISA II reason, D31 gets the row (or the policy reason). Any statement in the packet that the R5900 disclosures (0x1e stop, 0x33) are "untestable" or "cannot be exercised on testmips" is false and must read "testable but not claimed". The "28 of 34" count changes to 29 wherever it appears, if the row measures red. The pass-2 remark that a D31 row "would pin R3's untouched stop" is true only of the presence form and should be qualified. Nothing in the ISA II rulings (D01, D11, D30) changes.

CLOUDADJ2MPU: D31:ROW-OWED 4 TEXT-CHANGES VERDICT:HOLD
