RULING WANTED: one disputed record correction about the IEEE store differential.  READ-ONLY (plan mode).  Tree under
review: C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC (judge the committed HEAD 96a44fe3 via `git -C ... show HEAD:<path>`;
the working tree has another session's edits).  Ignore any other src/.

Open with GROKF6_ALIVE_1006, then ONE verdict line: `VERDICT: ASTRA RIGHT` or `VERDICT: HELPER RIGHT` or
`VERDICT: BOTH WRONG -- <one line>`.

The key is hdiffieeestore:F6.  A read-only helper wrote a corrected replacement sentence describing which S-format
inputs the store's underflow path changes; its row (verbatim) is in
C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\gweb\adjudicate_rrec\f6_row.txt.

GPT-6 Astra says that replacement is WRONG: "The new S-format equivalence omits negative normal inputs below 2^-149.
For example, -2^-150 changes from 0x00000000 to 0x80000000, although the proposed predicate is false. The underflow
term must be isnormal(x) && 0 < abs(x) < 2^-126 && (signbit(x) || abs(x) >= 2^-149). The D-subnormal correction is
right."  Astra cites regress/diff_ieee_store.c:145-146,275-304 and src/core/float_emul.c:377-388,663-665.

Rule on it from the source: trace -2^-150 and +2^-150 (and one value between 2^-149 and 2^-126, each sign) through the
OLD and NEW store paths the differential compares, give the bit pattern each yields, and say whether Astra's predicate
is exactly right (not merely closer).  Cite path:line for each step.  If the right predicate differs from both, write it.
