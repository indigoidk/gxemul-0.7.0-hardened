#557 -- the repair of your aconf_557c: right?

Open with the token `ASTRA557D_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repair is right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf557c.diff` -- the four draft texts from what `aconf_557c` read to now
(4 hunks).  Anything there that is not the repair below, or the consequential count and chain lines, is a finding.

**The repair.**  Your `aconf_557c` found the class row's note still saying "one left empty on purpose".  Rather than
change the word, the note now DERIVES its counts from the two census artifacts each time it is generated
(`draft\prep557.py.txt`, function `census()`, called from `edit_ledger`): grok's per-row verdict words in
`grok\grok_closedcensus.txt` (20 SHIPPED, 14 NOTHING, 3 WORK, of 37) and your verdict line in
`aconf_census\codex_aconf_census.txt` (34 confirmed, 3 wrong, of 37); the script REFUSES unless the verdicts partition
the 37, unless grok's shipped set equals the 17 census fills + the 2 empty-on-purpose + `boilerplateprefix`, and unless
the overlap of that shipped set with the five alive rows is exactly `boilerplateprefix` and `smhang`.  The regenerated
note (`draft\ledger557.draft.txt`, the `closeassessrows` line) says: 20 shipped / 14 nothing owed / 3 alive from grok;
your 34 / 3 with the two rows that moved from shipped to alive and `gdromcontractresidual` re-scoped; 17 fills from the
twenty (smhang's among them, for the part that shipped) plus `xfamscope`'s = 18; **2 left empty on purpose
(asanunbuildable, wiringshghost)**; 14 nothing owed; 5 alive (4 members + `boilerplateprefix`, landed); and that
`boilerplateprefix` and `smhang` sit in both the twenty and the five, "which is why those three counts sum past 37".
The commit message gained the same overlap clause (smhang in both counts; boilerplateprefix the fifth alive row).

Three questions:
1. Is every number in the regenerated note what the two artifacts give?  In particular: is smhang in grok's SHIPPED
   twenty AND in your three overturns (so the count "17 fills from the twenty" is right to include it), and is the
   overlap statement -- the only two rows in both the shipped twenty and the alive five are `boilerplateprefix` and
   `smhang` -- true?
2. Does the message's new clause say the same thing as the note, and is it true of the ledger diff?
3. The changelog's chain paragraph now carries your `aconf_557c` verdict (`1 things wrong`) with a one-line account
   of what it found and what was done, and `aconf_557d` is the placeholder (`<OWED: aconf_557d>`, filled at staging).
   Is the account of `aconf_557c` accurate?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of 4 hunks read`.
