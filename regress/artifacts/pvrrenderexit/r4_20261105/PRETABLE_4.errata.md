# PRETABLE_4.out -- erratum (2026-11-05, repair 5; codex pass 5 R1 and the pass-5 ruling's R3, ../adj_p5_20261105/ADJ_MYTHOS_local.md section 4)

STRIKES "EQUIVALENT" from B2t, at two places: line 14 ("the four textured fractional moves, EQUIVALENT by rule D2-F (iv) (B1t, B2t,
B13t, B14t)") and line 200 (`B2t_start_half  exactly: none -- GREEN (EQUIVALENT (rule D2-F (iv)): x1 is an int, so (int)(x1 + 0.5) is
x1)`).
The prediction stands -- green on 140 rows, and table 4 measured it so -- but the reason is false: `int x = x1 + 0.5` truncates toward
zero, so for a NEGATIVE int x1 it starts at x1 + 1, and the attributes, which advance on clipped iterations too, then arrive one step
behind.  B2t is a floor breach that no 140-row span showed (no shipped textured span has a negative start with varying u or v); repair
5 rows it (`texnegx n start`, `ztnegx n start`).  The same truncation reaches simpleline's start, so the start family is not SAMPLED
below half a pixel (R3) [2026-11-05, repair 6: except below the start's double resolution -- c = 2^-54 is SAMPLED, the pass-6
ruling's R3; ../r6_20261105/RECORDS6_NOTE.md].  B1t, B13t and B14t stay EQUIVALENT: in texturedline both operands of every position compare are ints, for
negative ends as well.  PRETABLE_4.out itself is not rewritten.
