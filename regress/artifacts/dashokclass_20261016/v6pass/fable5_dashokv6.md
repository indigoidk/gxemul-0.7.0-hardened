FABLE_DASHOKV6_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES (8)

Fable 5.1 (claude-fable-5-1), v6 pass, measuring in a mirror.  Provenance, MEASURED: my frozen controls copy md5s
`e9b811eeaf9e221b29e1c932b4a7014c` and is byte-identical (`cmp`) to the repo's `run_controls_v6.py`; the four staged
inputs md5 `a6ff64d8` / `516df040` / `769f261f` / `06a3ffc6` -- the receipt's header exactly.  BASE 116/116 (question 3
says "115 controls"; the controls' own tally prints 116).  The receipt's 157-mutant table I READ line by line (157/157 as
recorded).  My instrument: 28 one-edit mutants of the staged files, each through all 116 controls at 2 jobs
(`v6out/SWEEP_fable.txt`, per-mutant outputs beside it), plus three small probes -- the C27 walk alone against each
glyph-set mutant with each file's EFFECTIVE set then read by import; the shipped checker and four of my mutants against six
hand-built ledgers; the staged Q2 block against a stub checker exiting 256, 257, 258, 512 and -1.

Three apparatus findings from the sweep, first because they qualify what follows:

* **A non-literal binding crashes the walk.**  `d_domnonliteral` (DOMAIN bound by one Assign whose right side is a tuple
  EXPRESSION, not a literal) aborts `run_controls_v6.py` at C13: `walk_name` (:592) calls `ast.literal_eval` on the store
  and the `ValueError` is uncaught, so no walk row runs and no sentinel prints -- the driver scores it INCOMPLETE.  MEASURED
  (the traceback is in `mut_sweep/d_domnonliteral.txt`).  This is V19's class -- a crash before the tally -- at C27.  The
  walk should REFUSE a non-literal store (`DOMAIN = FOUR + EXTRA` is a plausible edit); the import read then shows the
  effective set.
* **R3's presence pin scored as a kill.**  `x_dclassliteral5` (the renderer's cell use site inlined with a fifth key) came
  back 114/116, and both reds are R3's nested fixture-mutations reporting MUTANT TEXT NOT FOUND: my outer edit removed the
  text R3 rewrites.  Every behavioural renderer row (R1, R1b-R1w, R2, R2b, R3's noescape leg) passes and the effective
  D_CLASS read by import is the four, so it is an escape in substance and my driver's line is a misattributed kill.  The
  shape does not occur in the receipt: 0 of 157 mutants is killed by R3 alone, and each of the 11 whose killers include R3
  lists another row (READ).  The packet already names this pin (V7, V20: "R3's presence pin its only red"); what is new is
  that R3's find-text happens to pin the renderer's cell use site TEXTUALLY, which is why that one site resists the
  inlined-literal form while the checker's predicate and `summary()` do not.
* **One of my mutants pins nothing.**  `w_sed9`'s find-text `sed 's/^/          /'` occurs ten times in the staged
  precommit and the driver requires exactly one (`src.count(f) != 1`, :101), so it was never applied.  Mine; re-specified
  with its enclosing line it targets Q2's indent (W2).

## 1. My own findings (V1, V4, V5, V7, V10, V13, V18-V24)

Row identity READ off the receipt for every mutant those dispositions name: 32 of 32 are killed with the bracketed row among
the killers (`d_dompadr` C28b; the six ISO mutants C12w; `d_hinttext`/`tail` C11, `d_hintalways` C1; the three strip mutants
R1h, with R1g; `r_tippend`/`notok` R1p; `r_sumcrash` C27 R2 and every R row; `r_wsset4` R1w; `d_strnone` C17n; `r_tipempty`
R1q; `w_q2paren`, `w_named` W2; `d_phasenone`/`seatnone` C29; the C27 four C27).  The REASON is MEASURED where my sweep
exercised the row: ten positive controls die on their named rows for the named reason -- `d_domliteralok` (the plausible "OK"
inlined at the use site) 96/116, C1's summary moving 1356 to 917 as the 439 OK answers enter the domain; `d_dombuiltins`
114/116 by C27 through the IMPORT read (the walk alone passes it; the effective DOMAIN shows the fifth spelling);
`d_baselatin1` and `d_sha15` 88/116 across 21 rows; `d_datenonerepr` 115/116 by C6; `r_dclassliteralok` 108/116;
`r_sumblank` by R2 R2b; `r_equote`, `r_legacyname`, `w_python3` by W1-W9.

Harder on my own.  **V18 is incomplete, and it is my complement axis turned on my own pin.**  R1p closes "ONLY a legacy cell
carries the class line" at cells holding a date and a note and nothing else.  The predicate `cls == LEGACY` sits in a
tooltip builder that READS and TESTS grade, badge and ev (that is why V6's position mutants needed R1o).  The 2x2 {legacy,
non-legacy} x {optional fields absent, present} is rowed at three cells -- R1g, R1o, R1p -- and open at the fourth:
`x_tipbadge` (`cls == LEGACY or ent.get("badge")`) and `x_tipev` (`... or ent.get("ev")`) pass 116/116, MEASURED.  Graded in
section 3.  **V1 overclaims by a word and is open at the renderer**: "a call to ... setattr" is refused by Name only;
`builtins.setattr(...)` is an Attribute call and passes the walk, as does a subscript store into `f_globals` keyed by a Name
-- each changes the renderer's effective D_CLASS (read by import: the four plus ZXQ) and passes 116/116, MEASURED.  The
checker half is closed by construction, its effective DOMAIN being read -- exactly the class closure the renderer half
lacks.  V19's fix is right for R2; its class recurs at C27 (above).  V20: `str.strip()` with no argument removes the code
points `str.isspace()` reports -- one predicate in CPython -- so R1w's 29 is the whole set, REASONED.  V4, V5, V7, V13, V21,
V22: right, their rows red on their mutants (READ).  V23: the comment reads as corrected; the PATH prepend I did not
re-measure (READ).  V10, V24: records, consistent with the previews.

## 2. The enumeration, by the CONTRACT's own decisions

Checked, MEASURED unless marked.  **Ledger shape**: the type partition {dict, not dict} is rowed at both levels (C21b an
int, C21e a str); the one-token widening `(dict, list)` escapes both -- a list ROW then raises uncaught (rc 1, a traceback,
which Q2 reports as "beyond the ceiling") and a list ENTRY walks as a non-entry and the ledger is GREEN (rc 0): the
contract's "rc 2 ... never silently green" is false for that shape.  **Baseline shape, md5 pin**: a latin-1 decode and a
15-char sha each die on 21 rows; the CRLF fold narrowed to "strip every CR" is equivalent but for a lone CR.  **The
selection**: every glyph, both pads, null, list, blank, hold and record rowed; a fifth spelling admitted at the use site by
an inlined literal or a disjunct passes -- the shipped checker refuses a ZXQ answer rc 1, both mutants return rc 0 on it.
**The key**: six positions at both ends rowed; the ABSENT case is rowed at phase, seat, date, d and note and open at the
row id (`r.get("id") or ""` keys a missing id as "" where the shipped code keys "None"; no fixture or shipped row lacks
one).  **The cutoff**: widths and separators rowed; the digit CLASS is not -- `\d` without `re.ASCII` admits fullwidth
digits, equivalent on every ASCII date.  **Output**: C1 and C11 whole, confirmed by the positive controls.  **The glyph
sets**: every Name binding form rowed; a non-literal store crashes the walk; at the renderer two runtime rebindings pass; a
use site REPLACED outright (no Load remains) passes at all three sites, R3's text pin aside.  Renderer **class, glyph,
strip, CSS**: rowed; a glyph-hiding rule not naming `legacy` is disclosed; `summary()`'s "accidental closure worth keeping
deliberately" has no row -- `n` given a fifth key passes 116/116 (`x_sumliteral5`).  **The class line on every legacy cell /
ONLY a legacy cell**: the open cell above.  **Q2**: the status partition is exhausted over `$?`'s range; a child exiting 256
or 512 reads GOOD (the status folds to 0 -- MEASURED on a stub), unreachable from the staged checker's three exits; the
`-eq 0` rewrite is equivalent.

## 3. The kill table and the floor

Misattributed kills: none in the receipt (0 of 157 rest on R3 alone, READ); one in my sweep (`x_dclassliteral5`, above).
One-edit mutants not in the table that pass all 116, graded:

**Floor breach, clause (d) -- one cell, two mutants, one row closes it.**  `x_tipbadge`, `x_tipev`.  The guard
`cls == LEGACY` crossed with body-read, body-tested, jointly reachable lvalues (grade, badge, ev -- the builder tests each;
R1o's fixture models real answers, and V6's own count has 642 of 670 legacy cells carrying evidence) gives four cells; three
are rowed and the symmetric fourth is not.  That is the #499 shape the repair-chain rule names: the cell repaired at the
address the mutant used, its mirror left open.  L2 -- row a NON-legacy cell with a grade, a badge and evidence, its WHOLE
tooltip with no class line.  I did not count HEAD's non-legacy cells carrying those fields; that census is owed with the row.

**Clause (e), fourteen**, each disclosed or disclosable at bounded cost.  `x_domliteral5`, `x_dclassliteral5`,
`x_sumliteral5`: the use site inlined with a fifth spelling -- the body tests no single spelling as a case, and the
contract's disjunct disclosure reasons the same way; name the inlined form beside it, or add one walk condition (the
selection site's right operand IS the Name).  `x_domdisjunct`: disclosed verbatim.  `x_builtinsetattr`, `x_frameglobals`:
the disclosed "mechanism C27 does not name" class -- but two consecutive passes have now found this class at the renderer,
so the CLASS CLOSURE is owed: read the renderer's effective D_CLASS by import, set-equal to the four, as the checker's is.
`x_rowlist`, `x_entrylist`: not a body-tested cell, but the D2 lesson applies -- a row at `str` does not pin a type tuple
against `list`; two fixture rows close it.  `x_rowidnone`.  `x_isoascii`.  `x_md5cr`, `x_reprstr`, `x_w_ceq`: equivalent
(`repr` already disclosed).  `x_cssglobalhide`: disclosed.  Unscored: `d_domnonliteral`.  Unapplied: `w_sed9`.

Shapes swept, as the denominator for the zero elsewhere: at the checker, the shape check at both levels, the baseline decode
and hash, the CR fold, the date repr, the row-id key, the ISO digit class, DOMAIN's binding (builtins, non-literal) and its
use (literal, disjunct); at the renderer, D_CLASS's runtime rebinding by two routes, its three use sites, the strip, the
escape, the class name, the class line against badge and ev, the CSS; at Q2, the interpreter name, the indent, the `-eq 0`
branch, statuses past 255.

## 4. The records (section 5)

The 5b entries and the 5d draft are true of the v5 pass and leave the v6 sentence to this pass; nothing there is false.  Two
sentences elsewhere are: the CONTRACT's "rows each member, or discloses it with its reason" (the open cell is neither) and
its "a call to globals / ... / setattr" (by Name).  Question 3's "115 controls" against a tally of 116.  A v6 sentence
written as "zero floor breaches" is false by one cell until change 1 lands.

## 5. Dispositions

Thirty checked.  Two need correction, neither reversed: V18 (R1p pins the complement at one cell of the optional-field
partition) and V1 (Name-only, and no effective-set read at the renderer).  V19 right, its class recurring at C27.

## 6. Closure

No.  One floor breach survives my own adjudication -- one cell, `x_tipbadge`/`x_tipev`: 2 of 28 one-edit mutants through 116
controls (10 positive controls killed as named; 16 substantive escapes, 2 floor and 14 clause (e); 1 unscored; 1 unapplied).
The repair is one fixture cell and owes its own pass on that diff.

## The eight changes

1. R1 sibling: a non-legacy cell with a grade, a badge and evidence -- whole tooltip, no class line (L2; kills `x_tipbadge`,
   `x_tipev`).
2. C27: read the renderer's effective D_CLASS by import, set-equal to the four (class closure; kills `x_builtinsetattr`,
   `x_frameglobals` and any rebinding syntax not enumerated).
3. C27: a non-literal store is a refusal, not a crash (`walk_name`'s `literal_eval` guarded; V19's class).
4. C27, or the disclosure: require the Name at the three use sites, or name the inlined-literal form beside the disjunct.
5. C21b/C21e siblings: a list row and a list entry, each wanting rc 2 (a list entry is silently green one token away).
6. Records: "a call BY NAME to ..."; the enumeration sentence qualified until (1); question 3's 115 to 116.
7. The driver: a NOT-FOUND inside a control's nested fixture is UNSCORED, never a kill; `w_sed9` re-specified.
8. Disclose: `$?` folds a child status of 256k to 0 (unreachable from the checker's 0/1/2); the ISO digit class; the absent
   row id (or row it); a lone CR in the baseline.

Not checked: HEAD's census of non-legacy cells with optional fields; V23's PATH prepend; the 157-table's per-row reasons
beyond the row identities and my own ten positive controls.
