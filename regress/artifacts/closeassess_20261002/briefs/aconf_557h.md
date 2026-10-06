#557 -- a precheck failure after your aconf_557g CLOSES, and its repair: right?

Open with the token `ASTRA557H_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repair is right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**What happened.**  After `aconf_557g` the unit was staged and the pre-commit hook run (`draft\precheck_20261006_1147_FAIL.out`).
ONE hard section failed -- I, on TEN rows #557 does not touch (n6, wdcaltctrlbit, diskimagesign, sgirergbroundtrip,
lcashiftub, alphapfnoffset, alphaswpctxptbr, stagetokens, heldmasked, pcc2c040mienannounce): "closed ... with NO regress
entry and not queued".  The cause: #557 committed `tools\pipeline\fable_queue.md` as HEAD's bytes plus a regenerated
generated block (your `aconf_557e` item 3), and those ten rows are named only in the WORKING copy's uncommitted prose
(`git diff HEAD -- tools/pipeline/fable_queue.md` shows +187 lines).

**The repair** (`draft\prep557.py.txt` step 3b and the file list; `draft\post557.py.txt`): `fable_queue.md` is no longer
committed; the post step regenerates the WORKING copy's generated block in place.  The claim that makes this safe:
#557's eight regress holds need NO queue entry, because `tools\pipeline\check_fable_queue.py` skips the regress phase for
rule 2 (holds must be queued) and rule 3 (a closed row with commits owes a regress review) is satisfied by any regress
entry.  Measured: `check_fable_queue.py` with `GXLEDGER` pointed at the staged ledger and the working queue untouched
prints `0 closed rows owing a regress review ... FABLE_QUEUE_PASS`.

**THE DELTA:** `draft\REPAIRS_since_aconf557g.diff` (5 hunks).  Questions:
1. Is the "needs no queue entry" claim true of `check_fable_queue.py` as written (quote the lines)?  Does reversing your
   aconf_557e item 3 lose anything that item was protecting -- e.g. a check that compares the generated block to the
   ledger (`gen_codex_wall.py --check`) that the hook runs?  Search `tools\precommit_check.sh` for it.
2. Are the new sentences in the section, changelog and message true, and is the chain paragraph accurate (aconf_557g
   CLOSES, the second precheck, aconf_557h = this, `<OWED: aconf_557h>` filled at staging)?
3. Anything else in the 5 hunks.

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of 5 hunks read`.
