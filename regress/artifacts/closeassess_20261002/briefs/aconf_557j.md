#557 -- the two wording repairs of your aconf_557i: right?

Open with the token `ASTRA557J_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` at HEAD `1329d894`; files
under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA:** `draft\REPAIRS_since_aconf557i.diff` and `draft\prep557.py.txt` (lines ~329, ~528, ~562).
1. Item 2: "because committing" -> "because staging" in the changelog and its template, and the step-3b comment.  Any
   copy left that describes the failed attempt as a commit (a quotation of the defect itself does not count)?
2. Item 3: the message now names BOTH of `aconf_557h`'s findings (the block check; staged, not committed).  Right?
3. The chain now carries `aconf_557i` (2 things wrong, named) and `aconf_557j` = this check as the placeholder.  Accurate?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of <total> hunks read`.
