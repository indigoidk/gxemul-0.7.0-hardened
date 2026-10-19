**The weekly battery, run on this working tree** (`_scratchpad/nightly/verdict_20261018_231924.txt` and
`battery_20261018_231924.log`; re-triggered by hand after the scheduled 18:00 run died in Modern Standby during gate 3):
`HEAD=6c2840d7`, `TREE_DIRTY=YES` (this round's diff plus other uncommitted work), START 2026-10-18 23:22:00, END
2026-10-19 03:51:19, `RUN_SH_EXIT=0`, **`REGRESS_PASS`, `GATE_COVERAGE=16/16`, passed 16, failed 0, skipped 0.**  Gate 1
rebuilt `build/` from `est/` and `/tmp/gxsec-build` from SEC with the fix in both (18 checks, including the est/SEC
divergence check); gate 6 passed on the re-derived census pins; gate 16 ran this round's block on `build/gxemul`
(CONDENSED from the log, lines 6489-6542: verbatim, except that the 30 fold-probe lines between `fold probe completed`
and the gate's PASS line are omitted):

```
## GATE: gate 16: MIPS fold witness (#388)
  ok   fbctrl probe output parses                           yes
  ok   fbctrl probe controls                                OK
  ok   fbctrl probe exit 0 (nonzero: a crash or a red row)  0
  ok   fbctrl_port rows run                                 117
  ok   fbctrl_port rows correct                             117
  ok   fbctrl_port rows failed                              0
  ok   fbctrl_port rows emitted match the trailer total     117
  ok   fbctrl_port ok rows match the trailer count          117
  ok   fbctrl_port row names are unique                     0
  ok   fbctrl command probe output parses                   yes
  ok   fbctrl command probe controls                        OK
  ok   fbctrl command probe exit 0 (nonzero: a crash or a red row) 0
  ok   fbctrl_cmd rows run                                  95
  ok   fbctrl_cmd rows correct                              95
  ok   fbctrl_cmd rows failed                               0
  ok   fbctrl_cmd rows emitted match the trailer total      95
  ok   fbctrl_cmd ok rows match the trailer count           95
  ok   fbctrl_cmd row names are unique                      0
  ok   fold probe completed (result line present)           yes
gate 16: MIPS fold witness (#388): PASS (35 checks)
```
