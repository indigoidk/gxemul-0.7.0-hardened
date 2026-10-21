# Argon `vmerec` (records check of #568's commit unit, 06:51, extended thinking off): dispositions

VERDICT (Argon): RECORDS NEED CHANGES -- 36 claims checked, 5 BROKEN, 22 HOLD, 9 UNSETTLED.  Reply:
_scratchpad/gweb/jobs_20261021_argonpack25/vmerec/gemini_web.reply.raw.  Meter 93.2% -> 62.7% (this send cost 30.6%).

| # | Argon's flag | disposition | how checked |
|---|---|---|---|
| B1 | O:10 lists "addenda 2b/2c" and omits 2d | ACCEPTED -- "addenda 2b, 2c and 2d" | read ob_568.md |
| B2 | L:112 "Opus 5.5 MEASURED (tables 1, 1b, 2, 2b, 2c, ...)" omits 2d; the same list in the ledger's opus5 review note | ACCEPTED -- 2d added in both | KILLTABLE2D.out:1-2 names the measuring seat |
| B3 | L:110 "Its oracle audit of the probe: every row holds" is stronger than vmer1o's CANNOT SETTLE (1 UNSETTLED: the helper code its bundle omitted) | ACCEPTED -- reworded to the scope it had | vmer1o reply line 2 |
| B4 | O:17-18 (and the ledger's vmewarnedbit note): "kill table 2 reds the one-sided index edits it built (M_LATCHONE, M_ONENARROW)" -- both legs edit the test AND the set | ACCEPTED -- the legs are TWO-sided (legs/M_LATCHONE.diff: `1ULL << 0` in both; legs/M_ONENARROW.diff: `1u << ...` in both), killed by collision and overflow; a one-sided index edit was NOT built (derived only) | read both leg diffs |
| B5 | M:21-22 "34 legs: 32 killed, 2 predicted equivalents" hides the M_ONENARROW miss and that M_CAPNARROW's kill is a failed build | ACCEPTED -- the message says both (the CHANGELOG already does) | KILLTABLE2_VS_PRETABLE2.out:44, :54 |
| U1 | probe md5 346c7813 in the block-alone runs (G1/G2) vs c896d079 in the full gate (G3) | ACCEPTED as a disclosure -- the block-alone runs used the probe before the table-2d docstring additions; both copies are AST-identical to the frozen rev 3 (code unchanged); the full gate ran the shipped file | md5 + AST check (mk_r1.py / the 04:34 check) |
| U2-U9 | claims whose files were not in its bundle (the witness, the device source, kill table 1, the object comparison, the rev-2 gate, passes 1/2/F2, the filed rows' sources) | NO CHANGE -- out of the bundle's scope by construction; GPT-6 Astra's file-reading confirmation checks them against the files | -- |

All five BROKEN items are records wording, not measurements: no score, count or grading the commit rests on changes.
