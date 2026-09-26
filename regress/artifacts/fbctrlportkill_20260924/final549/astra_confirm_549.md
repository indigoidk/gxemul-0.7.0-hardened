You are the second ADJUDICATOR (with the flagship seat) for a bounds correction in a C hardware emulator (GXemul,
change #549: `src/devices/dev_fbctrl.c`'s PORT register used to STORE an out-of-range port selector, after which the
DATA register's range check ended the emulator process; it now refuses any selector >= 8, compared on the full 64-bit
value, keeps the previous valid selector, and prints one message per device).  Read-only; no file may be changed.
The flagship seat ruled SHIP WITH WORDING on the regression test's last pass; nothing is committed until you confirm.

Read, in this order, under `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\`:
1. What would be committed: `final549\diff549_dev_fbctrl.diff` (the fix), `final549\diff549_gate_mips_folds.diff` (gate
   16's new block), and the new test itself, `regress\fbctrl_port_probe.py` in the tree (117 rows, 16 sessions; its
   header is the CONTRACT -- what it catches, NOT CLAIMED (0)-(8), LIMITS).  `final549\FILES.md5` pins all three.
2. The flagship rulings: `pass_v6\fable5_f2_v6.md` (the last pass: D1 and D2 graded disclosures, not floor; no v7) and
   the packet it ruled on, `pass_v6\f2b_v6_findings.md` (every seat's answer, the tally, and a brief defect of the main
   loop's, disclosed there).
3. The measurements: `table6\TABLE.out` + `table6\MANIFEST.out` (297 edits, predictions written first),
   `opus549_measured\f2v6\` (the measuring seat's last pass), `gates_v6b\gate16.out` (the gate on the final text: PASS),
   and `CORRECTIONS.md` (false sentences in dated artifacts, corrected there rather than edited).
4. The draft round record: `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\records\bugs549.md`
   (the queue filings) and `changelog549.md` beside it (the round block; angle-bracket placeholders anywhere are owed,
   not claims).

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; ignore any other `src/`.  Check the fix against the file, each
"measured" claim in the test's header against the file it names, and each count against the table.

FIRST LINE: `VERDICT: <CONFIRM | CONFIRM WITH CHANGES | DO NOT CONFIRM>`.  Then: (1) whether the fix is correct; (2) any
ruling of the flagship seat you would overturn -- in particular whether the latch-crossed-with-one-bit gap (D1) is
rightly a disclosure rather than a floor obligation, given that above bit 32 its measured consequence is the fix's own
defect for one write; (3) every sentence in the test header or the records that is false, with the file evidence.
Say what is a reading and what is a measurement.
