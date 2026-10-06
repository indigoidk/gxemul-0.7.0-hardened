#557 -- the two repairs of your aconf_557b: right?

Open with the token `ASTRA557C_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf557b.diff` -- the four draft texts from what `aconf_557b` read to now
(9 hunks).  Anything there that is not one of the two repairs, or the consequential counts, is a finding.

1. `wiringshghost` -- its commits field is now left EMPTY; the row's note names `686d179c` as provenance (it recorded
   the resolution; the three `.sh` keys were never committed) and the attribution rule's distinction.  The fills are
   therefore 18 (17 from the census, plus `xfamscope`), and the section and changelog say so, with two fields left
   empty on purpose.  Do the ledger diff (`draft\ledger557.draft.txt`), the section and the changelog agree?
2. The changelog and the message now name the chain of your three checks on this unit (`aconf_557`: 6 things wrong;
   `aconf_557b`: 2 things wrong; `aconf_557c`: this one) instead of a single "closing check"; the placeholder for your
   verdict is `<OWED: aconf_557c>` and is filled when the unit is staged.  Is the account of your two earlier answers
   accurate?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of 9 hunks read`.
