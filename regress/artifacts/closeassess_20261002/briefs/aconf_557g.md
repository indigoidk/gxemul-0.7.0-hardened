#557 -- the one repair of your aconf_557f: right?

Open with the token `ASTRA557G_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CLOSES -- the repair is right and nothing else changed`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`
at HEAD `1329d894`.  Everything below is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**THE DELTA, whole:** `draft\REPAIRS_since_aconf557f.diff` (6 hunks over the four draft texts).  Anything there beyond
the repair below and its consequential lines is a finding.

1. Your `aconf_557f` item 4: `section557.draft.md` still said a closed-with-no-commit row "owes nothing on paper".  It now
   says "owes nothing under those two rules" (K's witness rule and I's missing-regress rule).  The same phrase also sat
   in the eight regress `hold_question` texts; they now read "section I's rule 3 never demanded this review" (see any of
   the eight rows in `draft\ledger557.draft.txt`, e.g. `smhang`).  Are both wordings true of `tools\pipeline\
   check_witness.py` and `check_fable_queue.py` as written, and is any other copy of the overstated clause left in the
   four drafts or `draft\prep557.py.txt`?
2. The chain paragraph (changelog) and the message now carry `aconf_557f` (1 thing wrong, named) and `aconf_557g` = this
   check as the placeholder (`<OWED: aconf_557g>`, filled at staging); the artifact count moved 54 -> 62 (derived at
   staging time).  Accurate?

`<n> | RIGHT / WRONG: <why, path:line>`.  End with `DENOMINATOR: <h> of 6 hunks read`.
