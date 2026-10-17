# V6 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v6 = EACH DECISION'S GENERATING SET AND ITS COMPLEMENT

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the files under test are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v5/` (mirroring `tools/`; **v6 changes no staged file** -- the v5 pass found
no defect in the code); the controls are `run_controls_v6.py` and `run_mutants_v6.py` beside it, run with CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT naming the staged files; the v5-pass answers are in `v5pass/`.  Everything a packet-fed seat needs
is inlined below.

**Why v6.**  The v5 pass found no floor breach in the staged code and no misattributed kill, and it found the next layer of
the controls on two axes.  GPT-6 Astra measured nine one-edit mutants passing the v5 controls, each at a decision v5 listed
as pinned: **a v5 pin covered PART of its decision's GENERATING SET** -- the leading pad but not the trailing one, two of the
baseline row's six string positions, the ISO shape's anchor but not its widths, the glyph sets' Name stores while `globals()`
and a dict mutation changed them, the hint's opening, a tooltip whose fixture held no optional field, a CSS rule's presence
but not an overriding rule, the apparatus branch's first line on one-line output.  Fable 5.1 measured sixteen more and named
the second axis: **a pin asserting a property of the SELECTED set said nothing about its COMPLEMENT** -- every legacy cell has
the class line, but not ONLY legacy cells; the padded cell's class, not its text; the set where DEFINED, not where USED.  GLM
5.3 named three data-dependent edges, and Grok 4.7 traced eleven survivors, three of them past every v6 row then drafted
(the whitespace cells' tooltips, Q2's `else` at 251 of its 254 statuses, the named entry by a prefix).  So v6 enumerates
each decision's generating set with its complement and rows each member, or discloses it with its reason: the controls grew
from 96 to 116 and the kill table from 105 to 157 mutants.

**Fable 5.1 graded the v5 pass ZERO floor breaches** (clauses a-d measured, its denominator named) and proposed that the chain
close there, the v6 rows landing beside their own kill receipts.  **This pass is run anyway, and the reason is the material:**
v6 is not only rows -- C27 is new detector LOGIC (an ast walk of every binding form and every use of the glyph sets, plus the
checker's effective DOMAIN read by import), and under the repair-chain rule a repair's obligation follows what it adds.  **If
this pass finds zero floor breaches that survive adjudication, the chain closes here.**  Check the premises in 2b; do not
ratify them.

<TOKEN_LINE>

## 1. The v5-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (10)** (`v5pass/fable5_dashokv5.md`).  Measured in a mirror: 96/96 and the 105-mutant
  table reproduce byte for byte; 25 one-edit mutants of its own through the 96 -- 6 positive controls, 16 escapes, 2 equivalent,
  1 a kill the apparatus could not score.  ZERO floor breaches.
* **GPT-6 Astra -- SHIP WITH CHANGES (10)** (`v5pass/codex_dashokv5.txt`).  Ten survivors measured in memory (five checker,
  five renderer); K2 and K19 wrong as stated.
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`v5pass/glm_dashokv5.txt`).  REASONED; 28 of 28 dispositions checked.
* **Grok 4.7 -- SHIP WITH CHANGES (12)** (`v5pass/grok_dashokv5.txt`).  Its shell was denied: eleven survivors TRACED
  from the staged sources against every assertion, the baseline and ledger searches measured; K19 wrong.

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| V1 | Astra (F1), GLM (2), Fable (K2) | C27 counted Name stores: `globals()["DOMAIN"] += ("ZXQ",)`, `D_CLASS.update(ZXQ="ok")`, `D_CLASS["ZXQ"] = "ok"` and the USE SITE `x["d"] in DOMAIN + ("ZXQ",)` each pass all 96, the effective set gaining ZXQ | **PINNED**: C27 v6 walks each file's ast -- exactly one store of the name, a module-level Assign; it REFUSES a `del`, `global`/`nonlocal`, an import alias, a `def`/`class`, an `except` name, a parameter, a `match` capture, an attribute store of that name, a subscript store keyed by it, a call to `globals`/`vars`/`locals`/`setattr`/`delattr`/`exec`/`eval`/`compile`/`__import__`, any `__dict__`/`__globals__`, and any LOAD of the name outside its whitelisted uses (checker: the direct right operand of `in`/`not in`, or the argument of a constant's `.join`; renderer: the right operand of `in`/`not in`, or the object of a called `.get`) -- so a dict mutation through the Name (`D_CLASS.update`, `D_CLASS[...] = `) is a non-whitelisted Load and is refused.  It also reads the checker's EFFECTIVE DOMAIN by importing the file under test (`DEFAULT_CHECKER` is `pipe_copy("default")`: a temp copy of the checker under test beside `stage_tokens.py`).  Mutants `d_domglobals`, `d_domglobalsaug`, `d_domexec`, `d_domsetattr`, `d_domarg`, `d_domusesite`, `r_dclassglobals`, `r_dclassupdate`, `r_dclasssetitem`, `r_sumcrash`.  DISCLOSED: a helper module rebinding the sets after import, a C extension, and a selection predicate widened by a DISJUNCT naming a novel spelling (`... or x["d"] == "ZXQ"`) -- no finite row set pins every novel spelling; the plausible widenings die on C1 |
| V2 | Astra (F2) | the trailing pad: `str(x["d"]).rstrip() in DOMAIN` passes (C28 padded the start only) | **PINNED**: C28b (a new answer before the cutoff with d `"✓ "` -> rc 1).  Mutant `d_dompadr` |
| V3 | Astra (F3) | baseline string positions 1-4: `for v in k[::5]` passes (C17h/i made positions 0 and 5 numeric) | **PINNED**: C17j-m (positions 1-4 numeric, each in turn; with C17h/i every position).  Mutants `d_strskip1`-`4` |
| V4 | Astra (F4), Fable (change 4) | the ISO widths: `^\d{4}-\d{1,2}-\d{1,2}` passes, refusing a matched `2026-9-17` as "on or after the cutoff" | **PINNED**: C12w (MATCHED identities whose date breaks the shape in ONE place: `99999-10-18`, `2026-9-17`, `2026-10-9`, `2026/10-18`, `2026-10/18` -> rc 0, each its summary exact).  Mutants `d_isowidthy`/`m`/`d`, `d_isosep1`/`2`, `d_isodigits` (Fable's two-width form) |
| V5 | Astra (F5), Fable (change 3) | the hint: replacing or dropping its tail passes (C11 read its opening) | **PINNED**: C11 asserts the hint line WHOLE and the line count.  Mutants `d_hinttext`, `d_hinttail`, `d_hintalways` (the hint printed on rc 0 -> C1, whose output is now exactly one line) |
| V6 | Astra (F6) | the class line's POSITION: `tip.insert(-2, ...)` and `if cls == LEGACY and not ent.get("ev")` pass (the fixture held only a date and a note), while 649 / 642 of the 670 shipped legacy cells lose the line | **PINNED**: R1o (a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first).  Mutants `r_tipinsertm2`, `r_tipnoev` |
| V7 | Astra (F7), Fable (change 2) | the glyph TEXT: `html.escape(str(t).strip())` and `e(str(d).strip())` pass (R1h checked the class only; R3's presence pin was the only red) | **PINNED**: R1h asserts each padded glyph's text exactly (`" ✓"`, and a new `"✓ "` cell).  Mutants `r_escstrip`, `r_glyphstrip`, `r_clsrstrip` |
| V8 | Astra (F8) | the CSS: a later `.c.legacy .g {{ font-size:0; }}` passes (R5 found its two rules present) | **PINNED**: R5 asserts the two rules exactly AND no other rule in the style block naming `legacy`.  Mutant `r_cssoverride` |
| V9 | Astra (F9) | Q2's apparatus line: `head -1` -> `tail -1` passes (every exercised apparatus output was one line) | **PINNED**: W7's stub prints TWO lines on stderr and W7 asserts the output whole.  Mutant `w_tail1` |
| V10 | Astra (F10), Fable | records: 5b's closure and 5d's "both edges" are false at their scope; K19's "nothing is skipped" (a list or dict note holding a token AS AN ELEMENT OR KEY is skipped, measured); "a bool rc 2" (True rc 2, False rc 1); the GLM V3 entry's "all addressed in v4" (the RULINGS count arrived in v5) | **CORRECTED**: the CONTRACT discloses the note-type scope and the two bools; the previews (section 5) carry v6's sentences and the qualified GLM V3 entry |
| V11 | GLM (1) | `entries` ABSENT has no row: `r.get("entries")` passes | **PINNED**: C21j (a ledger whose row has no `entries` key, beside a valid one -> rc 0; 98 of 912 shipped rows carry none).  Mutants `d_entriesdef1`, `d_entriesdef2` |
| V12 | GLM (3a) | the note's UTF-8: a latin-1 encode passes on ASCII notes | **PINNED**: C20b (a new answer whose note is `"café — ✓"` -> rc 1, its line exact; 34 frozen notes are non-ASCII).  Mutant `d_notelatin1` |
| V13 | GLM (3b), Fable | `x.get("phase") or ""` / `seat or ""`: dropping the `or ""` printed "None" and passed | **PINNED**: C29 (a new answer with no phase and no seat -> rc 1, both identifiers empty in its exact line).  Mutants `d_phasenone`, `d_seatnone` |
| V14 | GLM | K6's "C1 and C11 exact too" reads as if those rows killed `d_basewithin`; they cannot (1356/1356 and 0/0 coincide under it) | **AGREED, NO RECORD CHANGE**: the clause lived only in the v5 brief's K6 cell; no record repeats it, the controls' own C12 comment says "C1 and C11 cannot tell them apart", and the kill table names C12 alone |
| V15 | GLM | K20 (the fixture's HELD and NOTSEAT cells) not checkable from the packet | **FIXED in the packet**: GLM's body now carries the renderer fixture (the EXPECT table and FX rows) beside the CONTRACT |
| V16 | GLM | `d_notenone`'s reason did not cover a missing note hashing as the literal "None" | **CORRECTED** in the CONTRACT: 0 entries anywhere carry a note that is the string "None" (measured) |
| V17 | GLM | the renderer comment's "365 displayed cells" against R2's 670 legacy cells | **NO CHANGE**: 365 is the displayed cells whose d is "OK" ("439 of them OK, 365 displayed cells"); 670 is every displayed legacy cell |
| V18 | Fable (change 1) | the ONLY-legacy edge: `if cls in (LEGACY, "pend")` and `if cls != "ok"` pass, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on 833 pend cells of HEAD's ledger | **PINNED**: R1p (the fixture's ok, pend, bad and hold cells: each tooltip exactly `2026-10-16 — a renderer control`).  Mutants `r_tippend`, `r_tipnotok` |
| V19 | Fable (change 5) | a renderer CRASHING on the shipped ledger (`D_CLASS["OK"] = "ok"`, and the comment-only null medium) killed the controls before their tally -- the driver scored a kill INCOMPLETE | **FIXED**: R2's census is guarded; the run completes and R2 says NO.  Mutant `r_sumcrash` (C27 and R2) |
| V20 | Fable (change 7) | the whitespace set was SAMPLED: `.strip(" \t\n\xa0")` passes behaviourally (R3's presence pin its only red) | **PINNED, the partition exhausted**: R1w (every `str.isspace()` code point alone as d -- 29 -- shows `?` and renders legacy).  Mutant `r_wsset4` |
| V21 | Fable (change 8) | `isinstance(v, (str, type(None)))` passes: a None key field in an override baseline is accepted | **PINNED**: C17n (a None date -> rc 2).  Mutant `d_strnone` |
| V22 | Fable (change 9) | equivalent or display-only escapes, to be disclosed | **ROWED where a row exists, DISCLOSED where none can**: `x_phasenone` -> C29; `x_tipempty` -> R1q (a legacy answer with no date and no note: its tooltip is the class line alone; mutant `r_tipempty`); `x_q2paren` -> W2's first line EXACT (mutant `w_q2paren`); `x_domglobals` -> C27.  DISCLOSED with their reasons: `x_apparatusmsg` (the apparatus lines' wording; their rc 2 is pinned), `x_isocutle` (the `[:10]` slice), `x_w_head2` (the GOOD branch prints one line) |
| V23 | Fable (change 10), Astra (READ) | W8's comment: "python is not on the PATH it is given" -- the git-bash wrapper PREPENDS `/mingw64/bin`, `/usr/bin`, `~/bin` | **CORRECTED**: the comment says so, and that W8 fails LOUDLY (GOOD instead of BAD), never falsely, on a machine where one holds a python |
| V24 | Fable | K2 and K14 incomplete on the fix (the verb right, the pin with an open complement edge) | covered by V1 and V20 |
| V25 | Grok (1-5, 7, 8, 10) | the trailing pad; baseline positions 1-4; the ISO pattern TRUNCATED (`^\d{4}-\d{2}-`); `globals()`, a subscript store, `sys.modules[__name__].DOMAIN = ...`, `exec`; the hint's join argument; the class line on EVERY cell (`if cls`); a later overriding CSS rule; `head -1` -> `tail -1` | **PINNED by the rows above**: V2 (C28b), V3 (C17j-m), V4 (C12w -- its one-digit-day member is ISO under the truncated pattern and then sorts after the cutoff), V1 (C27: an attribute store named DOMAIN is refused), V5 (C11 whole), V18 (R1p), V8 (R5), V9 (W7).  Mutants `d_isotrunc`, `d_domsysmod`, `d_hintjoin`, `r_tipall` added, so each is measured, not argued |
| V26 | Grok (6) | the newline and NBSP cells' class line: `if cls == LEGACY and d not in ("\n", "\xa0")` passes (R1d read class and glyph; R1g's list held neither) | **PINNED**: R1g takes both R1d cells, and R1w asserts each of the 29 whitespace cells' WHOLE tooltip.  Mutants `r_tipnows`, `r_tipnows2` (sparing `\x0b` alone) |
| V27 | Grok (9) | `else` -> `elif [ $_cedrc -ne 3 ]`: rc 3 runs no branch and the section is silent -- W3, W7 and W8 are three statuses of 254 | **PINNED, the partition EXHAUSTED**: W9 drives Q2 with EVERY status 2-255 through one stub, 254 runs in one bash loop, each exactly "BAD ... could not run (rc N): <first line>" with the counter 1.  Mutant `w_elifne3` |
| V28 | Grok (11) | W2 named the entry by a PREFIX: Q2's `printf \| sed` replaced by a constant "OFF-DOMAIN ANSWER  row redacted" passes | **PINNED**: W2 reads its WHOLE output -- the first line, every line of the checker's own output (from running the checker in W2's tools dir exactly as Q2 does) indented, the counter.  Mutant `w_named` |
| V29 | Grok, Astra | K19 wrong: a list or dict note holding a token as an element or a key is SKIPPED (rc 0); True rc 2, False rc 1 | **CORRECTED** (with V10): the CONTRACT discloses the note-type scope; the GLM V4 seat entry's "refused, never skipped" is corrected in the records preview |
| V30 | Grok, Astra | records: "rows both edges of every decision" (closure, CHANGELOG); the GLM adjudication-pass entry's "d_nonote2 killed by exactly C15 and C16"; the GLM V3 entry's "both sentences" | **CORRECTED**: the closure and the CHANGELOG say the generating set and its complement; "killed by C15 and C16 -- among others, the v5 table showing nine"; the V3 entry dates the RULINGS count to v5 |

## 2b. Premises to CHECK (stated as questions)

* **The generating sets.**  For each decision in the CONTRACT (section 4a's docstring), is the set v6 rows the WHOLE
  generating set -- every operand position, both ends, every width, every binding form and use -- with its complement?  Or is
  there a member, or a complement edge, that neither a row nor a disclosure names?
* **C27 v6.**  Is the whitelist sound and complete: is there a one-edit change to `check_entry_domain.py` or `gen_dashboard.py`
  that changes the EFFECTIVE glyph set (or the set a USE reads) and passes the walk?  Is any whitelisted use itself a way to
  widen the set?  Does reading the effective DOMAIN by import add a failure mode of its own?
* **R1w's 29.**  Is `str.isspace()` the set the renderer's `str(d).strip()` removes -- or do the two differ (Python's `strip()`
  with no argument strips the whitespace `isspace()` reports)?
* **The disclosures.**  Is each disclosure's reason true, and is any disclosed edit in fact rowable at bounded cost?
