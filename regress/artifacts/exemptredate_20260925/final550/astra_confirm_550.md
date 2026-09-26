You are the second ADJUDICATOR (with the flagship seat) for a test-infrastructure change in a C hardware emulator
(GXemul, change #550: re-dating ten dated exemptions in a test-wiring checker, one by one, and one in the offline
test gate).  Read-only; no file may be changed.  The flagship seat ruled SHIP; nothing is committed until you confirm.

Read, in this order:
1. The three diffs against the committed tree, exactly what would be committed:
   `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\exemptredate_20260925\final550\diff550_final_check_probe_wiring.diff`,
   `diff550_final_gate_offline.diff` and `diff550_final_precommit_check.diff` beside it.
2. The flagship rulings: `..\fable5_f2_550_551.md` and
   `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\wdcidselfcheck_20260925\fable_f2b\fable5_f2b_550_551.md`
   (its "#550" parts).
3. The measurements: `..\measured\schedule_v3final.out` (the checker run at each date) and
   `..\measured\selftest_550v3final.out`.
4. The draft round record: `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\records\changelog550.md`
   and its queue filings in `bugs550.md` beside it (angle-bracket placeholders are owed, not claims).

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Check every factual sentence the diffs
ADD against the file it names -- a count, a path, a grep that is said to match or not match -- by opening the file or
running the grep read-only.

FIRST LINE: `VERDICT: <CONFIRM | CONFIRM WITH CHANGES | DO NOT CONFIRM>`.  Then: (1) any ruling of the flagship seat
you would overturn, with the reason; (2) every sentence in the diffs or the draft record that is false, with the file
evidence; (3) anything the dates or the schedule get wrong.  Say what is a reading and what is a measurement.
