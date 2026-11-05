# table4/VERDICT.md -- erratum (2026-11-05, repair 5; codex pass 5 R1, upheld by ../../adj_p5_20261105/ADJ_MYTHOS_local.md section 4)

STRIKES "EQUIVALENT" from B2t in lines 16-17 ("EQUIVALENT by rule D2-F (iv), texturedline's integer ends: B1t, B2t, B13t, B14t").
B2t (`int x = x1 + 0.5` in texturedline) was green on all 140 rows, as measured, but it is not equivalent: the start truncates toward
zero, so at a negative int start it begins one column late with every attribute one step behind -- a floor breach, rowed by repair 5
(`texnegx n start` and its Z-off twin).  B1t, B13t and B14t stay EQUIVALENT (int operands in every texturedline compare).  Nothing
else in VERDICT.md changes; VERDICT.md itself is not rewritten.
