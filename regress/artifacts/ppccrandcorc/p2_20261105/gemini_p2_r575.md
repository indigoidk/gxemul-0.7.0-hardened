# Gemini 4 Argon (gemini web proxy) -- job `p2_r575`, banked at the #575 landing (kit built 2026-11-05)

* source: _scratchpad/gweb/jobs_20261105_rounds/p2_r575/gemini_web.out (mtime 2026-11-05 01:44:47 local, 1959 bytes, md5 3342e296cd2c2cbd0cec93dbb9745365)
* sender verdict line: GWEBP2RFIVE: 6 ATTACKS 1 BROKEN 4 HOLDS 1 UNSETTLED DRAFTABLE:NO (sender: exit 0)
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---
1. **FLOOR on the composite**
   There are zero floor breaches. Every mutation to the five sites (decode `ba`, decode `bb`, clear, condition, set) is either caught by the 62 rows or falls into the explicitly ruled non-coverage. Weakening the field masks is caught by the `hi` rows and the `t1`/`t2` variants; replacing `ba & !bb` with a functionally equivalent expression (like `ba > bb` for 1-bit values) is not a defect; and dropping the clear is caught because the destination is pre-set to the inverse of the result. Denominator: 5 sites × the standard logic and mask mutations.

2. **THE DIFF**
   - **Product lines against Book I**: Correct. The edits `ba & !bb` and `ba | !bb` exactly match Book I v2.01's `CRBA & ¬CRBB` and `CRBA | ¬CRBB`.
   - **New rows**: Correct. The two `hi` rows seed the masks properly such that their aliases are inverted, and `edge mfcr` / `edge disasm` accurately capture the second channel and disassembler output.
   - **Records**: Correct. Every sentence of clause (e) and the gate comment is fully true against sections 1-5, accurately reporting the 52/62 HEAD score, the null medium behaviors, and the variants. Zero false records.

3. **Missing from the pass-1 ruling**
   - **BROKEN**: R5 explicitly ordered the four Clause 2 bt-substitutions (`bt & !bb`, `ba & !bt`, `bt | !bb`, `ba | !bt`) to be listed in `PRETABLE.out` as predicted, not built. These four are completely missing from the PRETABLE in section 4a.
   - **UNSETTLED**: R9 ordered to "Correct the three §3 premises in the brief", but the brief (the commit message or PR description) is not included in this packet, so this cannot be verified. (File that would settle it: `commit message` or the PR description file).

4. **VERDICT**
   REPAIR (add the four missing bt-substitutions to the PRETABLE manifest as required by R5; verify the brief corrections for R9).

P-GWEBP2RFIVE-fe90
GWEBP2RFIVE: 6 ATTACKS 1 BROKEN 4 HOLDS 1 UNSETTLED DRAFTABLE:NO
