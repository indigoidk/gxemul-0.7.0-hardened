# V7 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v7 = THE GLYPH SETS BY THEIR EFFECT, AND THE v6 PASS'S FINDINGS SHARED

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the files under test are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v5/` (**unchanged since v5** -- no pass has found a defect in them); the
controls are `run_controls_v7.py` and `run_mutants_v7.py` beside it; the v6-pass answers are in `v6pass/`.  Everything a
packet-fed seat needs is inlined below.

**This is the closing pass, in the shared-findings shape.**  Every seat answered the v6 pass blind to the other three.  Here
every finding from all four is in ONE numbered list with my disposition (section 2), and the two places where seats
DISAGREED are set out with both sides in their own words (section 2c).  **Rule on the disagreements you are a party to
first, and be HARDER on a disposition that adopts your own position than on one that rejects it.**

**What v7 changed (controls only).**  The v6 pass found no defect in the staged files and no misattributed kill, and it
found C27's universal false: a banned callable reached by an attribute path or an alias, a mapping-pattern rest capture, a
store into a frame's globals, and a rebinding inside the `__main__` block all changed a glyph set past the static walk (all
four seats).  Rather than enumerate a fifth batch of syntax, **v7 reads both glyph sets by their EFFECT**: each file runs as
`__main__` on a fixture, inside a real module registered as `sys.modules["__main__"]`, and its set is read from the globals
after the run -- any rebinding the run executes, whatever its syntax.  The walk stays for what the run does not execute:
the named binding forms (now by attribute and by reference too), a non-literal binding refused instead of crashing the
run, and each use COUNTED.  v7 also rows every open generating-set member the seats named.  Controls 116 -> 123, kill
table 157 -> 181.

**The chain closes on this pass if it finds zero floor breaches that survive adjudication.**  Check the premises in 2b; do
not ratify them.

<TOKEN_LINE>

## 1. The v6-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (8)** (`v6pass/fable5_dashokv6.md`).  The seat refused twice mid-run and claude-opus-4-8
  ran 12 turns of its mutant sweep (re-run after a disk-full cleanup); resumed, Fable 5.1 wrote the answer (agent_models.py).
  28 one-edit mutants through the 116; ONE floor breach graded (W7, clause (d)).
* **GPT-6 Astra -- SHIP WITH CHANGES (6)** (`v6pass/codex_dashokv6.txt`).  Zero floor breaches on an enumerated (a)-(d)
  denominator; supports closing with the rest as clause-(e) debt.
* **Grok 4.7 -- SHIP WITH CHANGES (7)** (`v6pass/grok_dashokv6.txt`).  Shell denied, every item traced; ONE floor breach
  graded (W2, clause (c)).
* **GLM 5.3 -- SHIP WITH CHANGES (4)** (`v6pass/glm_dashokv6.txt`).  Zero floor breaches; "fix change 1 and close".

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| W1 | all four | C27's universal false: `builtins.exec`, `builtins.setattr`, `object.__setattr__`, an aliased `exec`, `case {**D_CLASS}`, a store into `sys._getframe().f_globals`, a rebinding under `if __name__ == "__main__"` -- each changed an effective glyph set and passed the walk (the checker's import read never runs the main block) | **CLASS CLOSED**: C27 reads BOTH effective sets after running each file as `__main__` (a real module registered as `sys.modules["__main__"]`, so `setattr(sys.modules[__name__], ...)` lands where a script's would); the walk also refuses a banned builtin by attribute or uncalled reference, a mapping-pattern rest, a subscript store into a call or a frame's globals, `f_globals`/`f_locals`.  Mutants `d_domattrexec`, `d_dommain`, `r_dclassmatchrest`, `r_dclassalias`, `r_dclassbuiltins`, `r_dclasssetattr`, `r_dclassfglobals` |
| W2 | Grok, GLM, Fable | `walk_name`'s `ast.literal_eval` is unguarded: `DOMAIN = tuple((...))` aborts the controls before the tally, scored INCOMPLETE | **FIXED**: a non-literal store is refused ("a non-literal binding"), never crashed on.  Mutant `d_domnonliteral`.  **Grade disputed -- 2c, D1** |
| W3 | Fable, Astra | a use site INLINED with a literal (`x["d"] in ("✓", ..., "ZXQ")`, a dict literal's `.get`, the summary's membership) passes: no Load of the name remains to check | **PINNED**: each set's use COUNT -- DOMAIN once in `in` and once as `" ".join`'s argument, D_CLASS once in `.get(` and once in `in`.  Mutants `d_domuseinline`, `r_dclassuseinline`, `r_sumuseinline` |
| W4 | Fable | `isinstance(r, (dict, list))` / `(x, ...)` passes: a list row raises (a traceback Q2 reports as beyond the ceiling) and a list ENTRY walks as a non-entry -- GREEN | **PINNED**: C21l, C21m (each rc 2).  Mutants `d_rowlist`, `d_entrylist` |
| W5 | Fable | a row with NO id: `r.get("id") or ""` keys it "" where the shipped code keys "None" | **PINNED**: C29b (refused, its line exact with row None).  Mutant `d_rowidnone` |
| W6 | Astra, Grok | the ISO widths' other directions: `\d{3,4}` year and `\d{2,3}` month pass (C12w rowed one direction each); a day of three digits is equivalent (no end anchor) | **PINNED**: C12w's frozen `999-10-17` and `2026-100-17`.  Mutants `d_isoyear3`, `d_isomonth3`.  The day: noted equivalent |
| W7 | Fable (Astra and Grok: the optional-field family) | a NON-legacy cell carrying a grade, a badge and evidence: `if cls == LEGACY or badge` and `... or ent.get("ev")` put the class line on it and pass 116/116 -- the open fourth cell of {legacy, non-legacy} x {optional fields absent, present} | **PINNED**: R1p2 (ok, bad and hold cells carrying all three: whole tooltip, no class line).  Mutants `r_tipbadge`, `r_tipev`.  **Grade disputed -- 2c, D2** |
| W8 | Astra, Grok | single optional fields on a legacy cell: `and (not ev or grade)`, its twin, and `and badge != "s"` pass (R1o carried all three together) | **PINNED**: R1o2 (a grade, evidence, the badge `s`, each alone: whole tooltip, the class line first).  Mutants `r_tipgradeonly`, `r_tipevonly`, `r_tipbadges` |
| W9 | Astra, Grok | R5 read the first style block's literal `legacy`: a second `<style>` block, or `.c.lega\63 y`, hides the glyph | **PINNED**: R5 reads EVERY style block, CSS escapes decoded.  Mutants `r_css2block`, `r_cssescape` |
| W10 | Astra, Grok | the strip's membership: `n[d if d in n else LEGACY]` counts a d spelled `total` or `legacy` as itself | **PINNED**: the fixture's d `total` and `legacy`; R2b counts them legacy.  Mutant `r_sumcounterkey` |
| W11 | GLM | a d that is neither string nor null is unrowed at the renderer | **PINNED** a number and a bool (R1g, whole tooltips).  **DISCLOSED**: a LIST d crashes the renderer at `D_CLASS.get` (unhashable) -- unreachable through a committed ledger: Q2 refuses a new answer with a list d (C26b), no frozen answer carries one, and a hold or record returns before the class is computed |
| W12 | GLM, Grok | the tok and empty cells' tooltips | **READ, no row**: `cell()` returns for a tok record, a live hold and an empty cell BEFORE `cls` is computed (Grok read it: `gen_dashboard.py` 154-172), so a disjunct at the insert is dead there |
| W13 | Fable | `summary()`'s `n` given a fifth key passes 116/116 | **DISCLOSED**: the novel-spelling class -- the strip fails to sum only for an entry spelling the fifth key |
| W14 | Fable | R3's presence pin can score a mutant that removes its find-text | **DISCLOSED**: no kill in the table rests on R3 alone (Fable read all 157); a presence red can only ADD a name |
| W15 | Fable | Q2's `$?` folds a child status of 256k to 0 | **DISCLOSED**: unreachable from the checker's exits 0/1/2 |
| W16 | Fable, Astra | the ISO digit class (`\d` admits fullwidth digits); a lone CR in the baseline | **DISCLOSED**: equivalent on every ASCII date; no checkout writes a lone CR |
| W17 | all four | records: "115" for 116 (the v6 brief and the hold question); C12w's "summary exact" (it reads rc); C20b "isolated" (its ledger is the shipped one); the class line "lost" where `insert(-2)` moved it; "displayed only" for the apparatus wording (it is deliberately unpinned); the CSS disclosure; "every binding form and use"; `d_nonote2`/`d_dfold2`'s killers; the witness's W1-W8 | **CORRECTED** in the CONTRACT, the hold question, the witness and the CHANGELOG draft (sections 4b, 5) |
| W18 | Fable | the driver should score a NOT-FOUND inside a control's nested fixture as UNSCORED | **NO DRIVER CHANGE**: W14's disclosure; the table requires every NAMED killer red, so a presence red cannot stand in for a behavioural one |
| W19 | Fable (its own) | `w_sed9`'s find-text occurs ten times | the seat's own sweep mutant, not in the table -- no action |
| W20 | main loop (reading the v7 receipt) | the v7 controls still PRINT `# dashokclass controls (v6)` as the receipt's second line, and the docstring's CONTRACT heading still reads `THE CONTRACT (v6)` -- labels the v7 builder did not bump | **TO CORRECT BEFORE COMMIT**: both read (v7), and the receipt and the kill table are re-run on that file so their md5 stamps name it.  No check, driver or assembler reads either label -- the assembler keys on the `# controls md5` stamp line |

## 2b. Premises to CHECK (stated as questions)

* **The effective read** (W1).  Is running each file as `__main__` on a fixture a faithful read of the set the shipped file
  uses?  What rebinding does it still miss -- one in a path the fixture run does not execute, and is the walk then enough?
* **The use count** (W3).  Is "DOMAIN once in `in`, once in `.join`; D_CLASS once in `.get(`, once in `in`" the shipped
  files' exact use set, and does a count close the inlined-literal form?
* **R1p2 / R1o2** (W7, W8).  Do the four cells of {legacy, non-legacy} x {fields absent, present} and the three single-field
  cells now cover the class line's guard and its complement?
* **Anything else** in the checker, the renderer change or Q2 whose generating set has an unrowed, undisclosed member?
