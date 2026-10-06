#558 -- the repair of your aconf_558g sentence 7: does your enumeration now read ten of ten TRUE?

Open with the token `ASTRA558H_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- all ten sentences true, nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `e1871fa5`.
Your answer: `regress\artifacts\idlessaudit_20261002\aconf_558g\codex_aconf_558g.txt` (ten sentences; sentence 7,
"Any other closure/state contradiction stays HARD.", false).  The repair: that sentence now ends "stays HARD, bar the
one below." -- the whole working diff is `regress\artifacts\idlessaudit_20261002\draft\CLOSEWORD_checker_v4.diff`.

Re-check each of your ten sentences against the working file (`<k> | TRUE / FALSE: path:line`), and say whether the v4
diff differs from v3 by anything other than that phrase.  End with `DENOMINATOR: <n> of 10 sentences re-checked`.
