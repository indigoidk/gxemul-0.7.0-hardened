#557 -- the repairs of your closing check (aconf_557): are they right?

Open with the token `ASTRA557B_ALIVE_1002` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repairs are right and nothing else changed`
`VERDICT: <n> things wrong`

This is a RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` at HEAD `1329d894`; committed files with `git -C ... show HEAD:<path>`, history
with `git -C ... log`.  Everything else is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf557.diff` -- the four draft texts from what your `aconf_557` read to
what stands now (12 hunks).  Anything there that is not one of the five repairs below is a finding.

1. `smhang` -- the member note now dates the deferral to the fable5 ruling of 2026-08-19 ("this should be its own
   round"), not 2026-08-30.  Right?
2. `wiringshghost` -- the fill keeps `686d179c` but now says what it is: the commit RECORDS the resolution; the three
   `.sh` manifest keys existed only in a working tree and were never committed (its parent `9c91999a` has none of
   them; `git log -S'scripts2/laneP.sh'` over the file finds only this commit, which adds the comment at
   `check_probe_wiring.py:1157-1176`).  Is that account right, and is `686d179c` the right thing to put in the field
   (if nothing else can be, say so; if the field should stay empty, say why)?
3. `xfamscope` -- filled with `636c0239 a4c86f11`, your two commits; the staging script checked both touch
   `regress/gate_crossfamily.sh`.  Right?
4. The section and the changelog now say 19 fields filled (18 of the twenty the census found shipped, plus
   `xfamscope` from the ten rows read before it), and the sentence about the three left-out rows is corrected.  Do the
   numbers and the sentence match the ledger diff (`draft\ledger557.draft.txt`, 25 changed rows)?
5. The artifact count is derived at staging time and will differ again at the commit; it is not re-asserted here.

For each: `<n> | RIGHT / WRONG: <why, with the commit or line>`.  End with `DENOMINATOR: <h> of 12 hunks read`.
