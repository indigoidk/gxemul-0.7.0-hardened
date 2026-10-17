FABLE_DASHOKV5_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP WITH CHANGES (10) -- the staged CODE is unchanged and correct on every input I built; the 96 controls and the
105-mutant table both reproduce BYTE-IDENTICALLY in a mirror; every v5 dual-edge row stands and its mutant dies on it; ZERO
floor breaches (clauses a-d each measured, denominator in section 3).  The ten changes are controls rows, disclosures and two
records sentences, all L1 (nothing has shipped): the v5 class -- "each pin tested ONE edge of its decision" -- is closed on its
own axis, and my sweep found the residue on a DIFFERENT axis, one shape again: a pin that asserts a property of the SELECTED
set says nothing about its COMPLEMENT (every legacy cell has the line vs ONLY legacy cells; the set where DEFINED vs where
USED; the padded cell's CLASS vs its TEXT; the hint's opening vs its tail).  If adjudication grades those as clause-(e)
contract debt, as I do, the chain closes on this pass with the rows landing beside their kill receipts; no further floor pass
is owed.

Fable 5.1 review seat (claude-fable-5-1; `agent_models.py` is the main loop's to run).  Everything measured ran in a MIRROR under
my session scratchpad (`scratchpad/v5mirror/`, the repo's relative layout: `tools/pipeline/{ledger.json,stage_tokens.py,
gen_dashboard.py}`, `tools/precommit_check.sh`, `regress/artifacts/dashokclass_20261016/{run_controls_v5.py,run_mutants_v5.py,
gen_dashboard_before.py,dashmissingd_census.py,staged_v5/}`), every copy `cmp`-SAME against GXEMUL-SEC before anything ran, the
controls and the mutant driver run from FROZEN copies, every long run in the background with its completion sentinel checked.
Nothing was written into any project tree except this file.  MEASURED = run here; READ = the file opened; REASONED = derived.
Every number names its deriver.  Scratch receipts (volatile, named not copied): `scratchpad/v5mirror/regress/artifacts/
dashokclass_20261016/{ctl_v5_mirror.txt, killtable_v5_mirror.txt, extra_mutants_v5.py, extra_mutants_v5.out,
extra_mutants_v5b.py, extra_mutants_v5b.out, compare_tables.py, dbg/, dbg2/, nullmedium/{checker,render}.{out,err}}` and
`scratchpad/v5mirror/ledgers/ledger_{e483d931,c64445fa,8bf8b5a1}.json`.

## 0. Banked facts

* MEASURED: the staged v5 md5s are the receipt header's -- a6ff64d8 / 516df040 / 769f261f / 06a3ffc6 (`md5sum`).  The packet's
  inlined checker (3a) and controls (4a) are BYTE-IDENTICAL to the staged files (a python compare after stripping the line
  prefixes).  `gen_dashboard_before.py` is HEAD's renderer and the working tree's (93dcb7ea, all three).  staged_v4 -> v5 differs
  by exactly the two title lines (`diff -r`).  The checker and the baseline are untracked at HEAD (new files).  The working-tree
  `precommit_check.sh` equals HEAD's in content; staged v5 differs from HEAD by the 32-line Q2 block.
* MEASURED: `run_controls_v5.py` (a frozen copy) on the staged v5 files in the mirror: 96/96, `DASHOKCLASS_CONTROLS_DONE`, rc 0,
  BYTE-IDENTICAL to `RECEIPT_v5_on_staged_v5.txt` after a trailing-space strip (`diff`: none).  (A `grep " NO "` of it hits ONE
  line -- C7's label "NO d" -- a pattern match, not a NO status; noted so nobody reads it as a red row.)
* MEASURED: `run_mutants_v5.py` (frozen) in the mirror, 3 jobs, 03:33:00 -> 03:53:57 under my own batches' contention:
  `BASE 96/96`, `KILL TABLE: 105/105 as recorded`, `DASHOKCLASS_MUTANTS_DONE`, rc 0 -- the 105 mutant lines BYTE-IDENTICAL to
  `KILLTABLE_v5_staged.txt` (`compare_tables.py`: 105 vs 105, 0 differences in tally, kill list or named rows; `diff` of the
  non-header lines: none).  That corroborates K23's "the comment edit after the table ran changed no behaviour" (the pre-edit
  file is not preserved, so corroborated, not proved).
* MEASURED: K24's three counts from `git show <sha>:tools/pipeline/ledger.json` -- 5,150 at e483d931 (903 rows), 5,167 at
  c64445fa (910), 5,177 at 8bf8b5a1 (912); the working-tree ledger is also 5,177 / 912 (it differs from HEAD by 29+/29- lines
  of state notes; no entry-count change).
* MEASURED: `dashmissingd_census.py` on HEAD's ledger (GXLEDGER = `git show 8bf8b5a1:...`) reproduces
  `DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt` line for line: 5177 / 1561 (174, 1244, 143; latest 2026-10-16) / 300 / 2953 / 814 / 682;
  the NOT-FIRED screen `/not[ -]fired|roster/i`: 222 / 200 / 87.
* MEASURED (W8's premise, 2b): the PATH the control sets holds `env.exe` and no python; `env python` on it is rc 127 with
  `env: 'python': No such file or directory`.  BUT the git-bash WRAPPER (`Git/bin/bash.exe`) hands the block
  `PATH=/mingw64/bin:/usr/bin:/c/Users/User00/bin:/usr/bin` -- it PREPENDS three directories -- and `command -v python` inside
  it is still "not found" (`find Git -maxdepth 3 -iname 'python*'`: nothing).  So W8 is a faithful launch failure HERE (the same
  `env` exec path a missing python takes, rc 127), and the packet's "python is not on the PATH it is given" is imprecise: the
  wrapper adds directories; none holds a python on this machine.  Machine-sensitive in the LOUD direction only -- a python in
  `~/bin` or `mingw64/bin` would make W8 FAIL (GOOD instead of BAD), never pass falsely.
* MEASURED (ledger shapes my sweep depends on): 98 of the 912 working-tree rows have NO `entries` key (101 have `[]`), so a
  checker requiring `entries` is killed by C1 (44/96 -- `x_entriesreq`): a row without entries is pinned as well-formed already,
  and the `dashmissingd` row the landing adds (5b: no `entries` field) is the 99th; 0 of the 1,356 off-domain answers lacks a
  phase, seat, date or note (1 entry in the whole ledger lacks a phase; not an off-domain answer).
* MEASURED: `ISO.match` == `ISO.search` on `'2026-10-17'`, `'x2026-10-17'`, `'\n2026-10-17'`, `'2026-10-17T12'`, `''`,
  `'10/18/2026'`, `' 2026-10-17'` -- the tabled `d_isosearch` equivalence holds at the edges (`^` without re.M matches at 0 only).
  `str.strip()` with no argument removes 29 code points (`isspace()` over the whole code space; `\xa0` is one of them).
* READ: section 5b's seat sentences against the v4 answer files -- grok's six headings are the six the entry names (null cell,
  membership by a stripped d in both files, the leading edge, the whitespace set, the ISO `$` anchor, the baseline scalars) and
  its "this landing does not choose it" (line 56) is the "stay untokened" ruling; codex's "ten ... in memory", its withdrawal and
  9/9 -> 4/9 (lines 27, 68, 70); GLM's "exactly C15/C16" (line 47); `run_mutants.py` names `run_controls_v2.py` (its line 3).
  Astra's 9/9 and 4/9 are ITS measurement; I did not re-run section H on a fixture this pass (my v4 reading of H stands).

## 1. My own findings (K1-K11, K13, K14, K17, K22-K25, K27) -- disposition AND fix, harder on mine

Each verified by READING the row's code in 4a against the mutant's edit in `run_mutants_v5.py`, and by the kill line now
reproduced in the mirror.  "Red for the reason named" = the row's assertion is the observable the edit changes, not a side
effect.

* **K1** (`d_dompad` -> C28): right.  C28 is a NEW answer dated 2026-10-10 with d `" ✓"`, want rc 1; the mutant's `.strip()` puts
  it in DOMAIN, rc 0.  Red for its own reason; 95/96.
* **K2** (C27 by ast; `d_domredef`, `r_dclassredef`): the disposition is right and **MY v4 FIX WAS INCOMPLETE AS A PIN** -- I asked
  for "exactly ONE module-level assignment ... an ast walk", and that is what landed.  It counts BINDINGS.  A dict is MUTABLE:
  an added line `D_CLASS["ZXQ"] = "ok"` (a Subscript store -- the Name's ctx is Load) or `D_CLASS.update({"ZXQ": "ok"})` is not
  a binding, leaves one top-level assignment whose literal is the four, and reaches no fixture or ledger spelling: BOTH PASS
  96/96 (MEASURED, `x_dclassmut`, `x_dclassupdate`).  **But the harm is bounded by the PRODUCT, by accident, and I measured
  that before grading it**: `summary()`'s `n` is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator
  on the first entry that spells it -- `n[d if d in D_CLASS else LEGACY] += 1` -> `KeyError: 'ZXQ'` on a one-row ledger with
  d "ZXQ" (MEASURED, `dbg2/`), and `D_CLASS["OK"] = "ok"` -- the forbidden one-liner itself -- crashes on the SHIPPED ledger
  the same way (MEASURED, every R row "render FAILED").  So an in-place mutation is EQUIVALENT on any ledger without that
  spelling and LOUD on any with it, never a silent misclassification.  The checker's DOMAIN is a tuple (no in-place form), but
  its USE SITE can widen: `x["d"] in DOMAIN + ("ZXQ",)` passes 96/96 (MEASURED, `x_usesite`) and nothing crashes -- a new
  answer with that spelling is admitted by Q2 and rendered legacy -- while the plausible `+ ("OK",)` dies 80/96 on C1 C11 C12
  C12s C19a C19b C21h C3 C4 C5 W2 W4 W5 (MEASURED, `x_usesiteOK`).  **That use-site widening with a novel spelling is the one
  real residual on the glyph-set axis**, the v3 definition finding one level down.  The 2b premise question, answered: the walk
  misses (i) in-place mutation (equivalent-or-loud, above), (ii) `globals()[...]`/`vars()`/`setattr`/`exec` (MEASURED 96/96 for
  `globals()["DOMAIN"] = (..., "ZXQ")`, `x_domglobals`; adversarial, not a plausible edit), (iii) `from m import DOMAIN` /
  `import m as DOMAIN` (alias nodes, no Name store; a second file; not a one-edit mutant of these files), (iv) a `def`/`class`
  named DOMAIN (rc 2 on C1 by behaviour).  Fix (change 6): C27 also refuses a Subscript/Attribute store or delete whose value
  is the Name and any Call on `<name>.update/setdefault/pop/popitem/clear`, so the pin says what it means; the checker's use
  site pinned by ast (every Load of `DOMAIN` is the direct right operand of an `in`, or the join's argument) or DISCLOSED; and
  the accidental closure in `summary()` written down where the next editor of D_CLASS will meet it.
* **K3** (`r_sumstrip` -> R2b): right; the fixture holds `" ✓"` and a null, R2b recomputes by exact membership; 95/96, R2b only,
  as predicted (R2's ledger has no padded glyph).
* **K4** (C25l-r; eight lstrip/row mutants): right, each 95/96 on its own row, `d_rowstrip` 94/96 on C25l C25r.  C25l/r REMOVE
  the frozen entry from its row and add it to a new row id with the space, so the shipped code refuses the excess key (rc 1)
  and the strip mutant matches it (rc 0) -- the row's own reason.  "C25 edits the ends" is now true.
* **K5** (whole refusal lines at C3/C6/C9/C19a): right.  `offline()` rebuilds the line from the entry and `offl == [line]`
  demands exactly ONE refusal, exact.  `d_cutreason` C3 only; `d_ceilreason` C6 C9 (+C19a, whose want is WHY_CEIL+WHY_ISO);
  `d_rowphaseswap` all four exact-line rows; `d_hintundated` and `d_datenone` C6.  Each red is the line itself.
* **K6** (summary exact; `d_basewithin` -> C12): right -- C12-on/after/far have within N and baseline N+1 (3 red, 93/96; C12-before
  has N+1 = N+1 and stays green, as the arithmetic says).  `d_cutoffmsg` C1 C11 C12.
* **K7** (C12s -> `d_isodollar`): right; a MATCHED identity dated `2026-10-17T12:00:00` is refused by date under `^` and admitted
  under `^...$` (seen 1 > base 1 is false).  95/96 C12s only.
* **K8** (C17c-i; seven baseline-row mutants): right, each 95/96 on its own row.  The short side (`len(k) <= 7`, a six-field row)
  is covered by behaviour, not by a row: `k[6]` raises IndexError inside the try -> rc 2 either way (REASONED).  Third edge,
  MEASURED: `isinstance(v, (str, type(None)))` passes 96/96 (`x_strnone`) -- a None key field in an override baseline is
  accepted; it matches nothing (`date_str` never yields None) and inflates "baseline N" by its count.  Override path only; the
  md5 pin bounds the default path.  Change 8.
* **K9** (R1e whole tooltip; `r_tipnorecord`): right, 95/96 R1e only (R1g's want list excludes the record cell, by design).
* **K10** (R1n, R1g null): right; `r_nullpend` R1n R1g, `r_tipnotnull` R1g.
* **K11** (R2 whole strip; `r_striplabel`): right, R2 R2b.
* **K13** (C24 isolated): right; `d_isheld` now carries C24 in its kill list beside the ledger-reason reds.
* **K14** (R1d newline/NBSP; `r_wsset`): right as far as it goes, and it is a SAMPLE: `str.strip()` removes 29 code points
  (MEASURED); R1d drives 4.  A mutant naming exactly those four, `.strip(" \t\n\xa0")`, keeps a CR-only (U+2028, U+3000 ...)
  `d` invisible and is "killed" by R3 ONLY -- the presence pin, its find-text gone (MEASURED, `x_wsset4` 95/96) -- so
  behaviourally it escapes.  The CONTRACT's "(any whitespace)" should read SAMPLED 4 of 29, or the partition exhausted: one
  fixture entry per `isspace()` code point is 29 cells in one row.  Change 7.
* **K17** (C26b list d; `d_nostr`): right; the shipped `str()` keys `"['OK']"`, rc 1, no traceback; the mutant's Counter raises
  on the unhashable tuple OUTSIDE the try -> traceback.
* **K22** (two title lines): right -- `diff -r staged_v4 staged_v5` is exactly those two lines (MEASURED).
* **K23** (records corrected): right -- the CONTRACT (4a :60-63), the runner comment and 5d carry 1,100 / 2 / 1,352 (my v4
  numbers); "exactly" is gone; the post-table comment edit is disclosed and the reproduced table corroborates it (section 0).
* **K24**: right, all three counts MEASURED (section 0).
* **K25**: right -- the deriver carries the screen and its output reproduces line for line on HEAD's ledger (section 0).
* **K27**: right (my v4 census: 21 ⏸ and 35 … answers; the mechanism of the un-isolated reds).

## 2. The enumeration -- every decision of the CONTRACT, checked at both edges, with the THIRD edge where one exists

The v5 class ("each pin tested ONE edge") is CLOSED on its own axis -- the field end, the first literal line, the number vs
label, the substring vs whole, the two branches of three -- every dual-edge row stands and its mutant dies on it (section 3).
**What remains is a different axis, and it is one shape too: a pin asserting a property of the SELECTED set says nothing about
its COMPLEMENT** -- every legacy cell has the line (pinned) vs ONLY legacy cells have it (open); the set is the four where
DEFINED (pinned) vs where USED (open); the padded cell's CLASS (pinned) vs its TEXT (open); the hint's OPENING (pinned) vs its
tail (open); the ISO shape's two ANCHORS (pinned) vs its digit widths (open).  Astra's condition 4 ("positive rows beside the
negatives") is this rule for the checker's selection; it was not applied to the renderer's tooltip or to the glyph-set pin.
Eighteen decisions checked, by the CONTRACT's own lines (READ against the staged files; the pin tested by the table's mutant or
mine, every "MEASURED" below a run of the frozen 96 controls in the mirror):

**checker (9)**
| decision | v4 pin | v5 dual row | third edge |
|---|---|---|---|
| ledger shape: object, rows PRESENT and a list, row objects, entries lists, entry objects | C21a-f, C23 | C21i (rows absent) | the POSITIVE edge is pinned by C1 itself: 98 rows without `entries`, 101 with `[]` (`x_entriesreq` 44/96, MEASURED).  HOLDS |
| baseline shape: list of [6 str, int not bool, > 0], exactly 7 | C13, C17, C21g | C17c-i | a None field accepted (`x_strnone` 96/96, MEASURED; override only) -- change 8 |
| md5 pin on the default path, CRLF folded; overrides skip | C18, C18b; C11/C12/C17 | -- | HOLDS (`d_pinoverride` reds every override row) |
| the selection: explicit d, EXACT membership, an ANSWER | C7, C14, C26, C2*, C8, C24 | C28, C26b, C24 isolated | the USE SITE widened with a novel spelling, `in DOMAIN + ("ZXQ",)`: 96/96 (MEASURED); the plausible `("OK",)` dies 80/96 -- change 6 |
| the key, byte for byte, both ends; str() of d | C25a-k, C15/C16 | C25l-r, C26b | `str(x.get("phase"))` without `or ""`: 96/96 (MEASURED, `x_phasenone`) -- EQUIVALENT on this ledger (0 off-domain answers lack a phase/seat); disclose (change 9) |
| the ceiling: a copy fails, no refill | C9, C10, C15 | -- | `>=` dies 77/96 on C1 ... W1 (positive control, MEASURED).  HOLDS |
| the cutoff: inclusive; ISO OPENS the date | C3, C4, C12 x4, C19a/b | C12s | digit widths `^\d{4}-\d{1,2}-\d{1,2}`: 96/96 (MEASURED, `x_isodigits`) -- a new answer dated "2026-9-17" is then refused "on or after the cutoff" (September) instead of "not ISO"; `[:11]` for `[:10]`: 96/96, EQUIVALENT for ISO-opened strings (REASONED, MEASURED `x_isocutle`) -- change 4 |
| output: cp1252; summary WHOLE; refusal lines WHOLE; the hint | C20; C1/C11/C12; C3/C6/C9/C19a; C11 | (v5 made these whole) | the hint's tail dropped: 96/96 (MEASURED, `x_hinttail`; C11 reads "give each a `d` from"); the APPARATUS lines' content: 96/96 (MEASURED, `x_apparatusmsg` empties the ledger-misshapen line; C21 reads rc only, W3 reads the baseline path) -- K5's shape at two more lines; changes 3, 9 |
| the glyph set: ONE binding of DOMAIN / D_CLASS, each the four | C27 (first line) | C27 (ast, every store) | in-place MUTATION of D_CLASS 96/96 but equivalent-or-loud (K2); `globals()[...]` 96/96, adversarial -- change 6 |

**renderer (6)**
| decision | v4 pin | v5 dual row | third edge |
|---|---|---|---|
| the class: EXACT membership -> class, else legacy, on the answer a cell shows | R1, R1h, R3 | R1n | `D_CLASS["ZXQ"] = "ok"` / `.update`: 96/96 and KeyError on the first entry that spells it (K2) |
| the class line opens EVERY legacy cell's tooltip, WHOLE | R1, R1g, R1f | R1e whole, R1g null | `if cls in (LEGACY, "pend")` and `if cls != "ok"`: 96/96 each (MEASURED, `x_tippend`, `x_tipnotok`) -- the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend (and hold/bad) cell, 833 displayed … cells on HEAD's ledger, and no row asserts a NON-legacy cell's tooltip -- change 1.  `if cls == LEGACY and tip:` 96/96, EQUIVALENT on this ledger (every off-domain answer has a note) -- disclose (change 9) |
| the glyph: escaped; `?` for blank / whitespace-only (any whitespace) | R1b, R1d | R1d newline, NBSP | `e(str(d).strip())`: 95/96, R3 ONLY = the presence pin (MEASURED, `x_glyphstrip`); behaviourally unpinned -- a legacy `" ✓"` would show `✓` in muted italics; "its text kept" is the ruled property -- change 2.  R1d SAMPLED 4/29 (`x_wsset4`, R3 only) -- change 7 |
| the strip: each number by EXACT membership, and its labels | R2 | R2b, R2 whole | HOLDS (`r_strip`, `r_stripok`, `r_sumstrip`, `r_striplabel`; `x.get("d") or "…"` in `summary()` would red R2 on the 23 blank-d entries -- REASONED) |
| the legend; the two CSS rules | R4 | R5 | HOLDS (whole strings) |
| hold / record precedence over an off-domain d | R1 fixture (HELD d "HELD"; NOTSEAT d "OK") | -- | HOLDS (READ: `_held_cell` and the `tok` branch return before `D_CLASS` is consulted, `cell()` :147-196) |

**Q2 (3)**
| decision | v4 pin | v5 dual row | third edge |
|---|---|---|---|
| rc 0 GOOD / rc 1 BAD named / ANY other BAD "could not run" + first line, stderr included | W1, W2, W3 | W7, W8 | `-eq 1` -> `-ge 1`: dies W3 W7 W8 (MEASURED, positive); the "could not run" line without its echoed first line: dies W7 only (MEASURED, `x_w_nomsg`: W3/W8 assert the rc, not the echo); `head -2` on the good branch: 96/96, EQUIVALENT on the clean path (one line when clean); the rc-1 line's parenthetical dropped: 96/96, display (`x_q2paren`) -- change 9 |
| the checker absent -> BAD | W6 | -- | HOLDS |
| exported GXDOMAIN_BASELINE / GXLEDGER stripped | W4, W5 | -- | HOLDS |

**Missing decisions?**  None of the staged checker's, the renderer diff's or the Q2 block's that the CONTRACT does not list,
after reading all three whole: the `stage_tokens` import (uncaught if the module is absent: rc 1 with a traceback, which Q2
reports under the rc-1 words -- RED, wrong first line; shared with every pipeline check, outside this diff); `_HERE` and `say`
(the block's own, stubbed); `summary()`'s `"total"`; the `tok`/held branches (HEAD's code).  The renderer's `D_CLASS.get(d,
...)` on an UNHASHABLE d (a list) crashes the render -- HEAD's code crashed the same way, the ledger holds no such d (my v4
census: all 1,397 strings), and C26b refuses new ones; outside the diff, noted.  One thing the CONTRACT does not say and
should: `summary()`'s literal keys are what closes D_CLASS at four for every entry that exists -- loud by accident (change 6).

## 3. The kill table and the floor

* **Reproduction**: 105/105 as recorded, BYTE-IDENTICAL mutant lines (section 0).  `d_notenone` and `d_isosearch` escape as
  recorded, and both equivalences are MEASURED today (0 empty notes among the 1,356; `match` == `search` at the edges).
* **Is any mutant killed for a reason other than the one its line names?**  No -- MEASURED on the recorded table and on the
  mirror's (identical): every named row is in its mutant's red list, and 41 mutants are killed MORE WIDELY than their line
  names; each wider list is the ledger-level consequence of a one-sided edit and the named row is the isolated witness:
  `d_domnohold`/`d_domnopend` (the shipped 21 ⏸ / 35 … answers turn off-domain -> 19 rows), `d_dupplus1` (every single-excess
  refusal passes -> 32 rows), `d_nonote`/`d_dfold`/`d_notestrip`/`d_notefold`/`d_isheld` (bulk key mismatch -> 16-18 rows),
  `d_pinoverride` (pins the override path instead -> the four override rows), `d_noreconf` (the hint line's glyphs under cp1252
  -> every rc-1 row), `d_cutoff18` (the literal is in the summary line -> C1 C11; the on-cutoff entry falls to the ceiling
  with the wrong reason -> C3), `w_rc7`/`w_collapse` (a branch swallows another's status -> W4 W5 W7 / W7 W8),
  `d_baselen`/`d_summary` (C12's exact summary).  Two cautions worth keeping: **R3 is a PRESENCE pin** -- it reds whenever a
  mutant touches one of its three find-texts (`r_wsset`, `r_wsspace`, `r_noescape`, `r_clsstrip` in the table; `x_glyphstrip`
  and `x_wsset4` in mine), so "R3" alone in a kill list is evidence the TEXT changed, never that behaviour did; and the three
  one-sided folds die on C1 exactly as the corrected comment says (1,100 / 2 / 1,352 keys move, not "everywhere").
* **The floor, each clause measured on the staged controls as the detector** -- (a) red on the pre-fix build: R2's own
  before-census (HEAD's renderer: 1,503 pend, 0 legacy) and W6 (no checker at HEAD); (b) verbatim reinstatement: `r_pend`
  (the `"pend"` fallback) 85/96, `w_nochecker` 95/96, `d_blank`'s v1 selection 88/96 -- all killed; (c) NULL MEDIUM, measured
  at `nullmedium/`: a COMMENT-ONLY checker is RED on 66 of 96 (30/96, rc 1, sentinel intact -- C1's exact summary reds on the
  empty output, every rc-1 row reds); a COMMENT-ONLY renderer reds all 11 R rows ("render FAILED (a crash is not a kill)") --
  AND THEN THE CONTROLS THEMSELVES CRASH: `render()` returns None and `census(ha)` at :691 calls `re.finditer` on it
  (`TypeError: expected string ... got 'NoneType'`), so the run has NO tally, NO sentinel, and W1-W8 never run.  The mutant
  driver scores that INCOMPLETE (apparatus), not KILLED -- measured a second time on `D_CLASS["OK"] = "ok"` (84 stdout lines,
  no sentinel).  A kill in substance, lost in form: change 5; (d) null repair: `r_okonly`/`r_tipokonly`/`r_tipnonblank` (the
  guard kept, its effect narrowed) R1g; `d_nodate` (`if False:`) C12; `d_nomd5` C18 -- killed.  **Zero floor breaches.**
* **My sweep, the denominator**: 25 one-edit mutants of the staged v5 files not in the table, each through the frozen 96 in
  the mirror (`extra_mutants_v5.py`, `extra_mutants_v5b.py`), 6 of them positive controls that reddened as predicted (`x_usesiteOK`
  80/96, `x_seenge` 77/96, `x_entriesreq` 44/96, `x_hintlen` 57/96, `x_tipins1` 92/96 R1 R1e R1f R1g, `x_w_ge1` 93/96 W3 W7 W8)
  and `x_w_nomsg` 95/96 W7 -- the driver detects kills.  **ESCAPES (96/96, or R3-only): 16** -- break a listed decision's
  complement edge: `x_tippend`, `x_tipnotok`, `x_glyphstrip` (R3 only), `x_hinttail`, `x_isodigits`, `x_usesite`, `x_strnone`,
  `x_wsset4` (R3 only), `x_apparatusmsg`; equivalent-or-loud: `x_dclassmut`, `x_dclassupdate`; equivalent on this ledger or on
  every input: `x_phasenone`, `x_tipempty`, `x_isocutle`, `x_w_head2`, `x_q2paren`; adversarial: `x_domglobals`.  (That is 17
  names; `x_dclassmutOK` is the 25th, INCOMPLETE as described under clause (c) -- a kill the apparatus cannot score.)
* **Shapes swept by reading, not built** (REASONED): the cutoff compare without the slice (equivalent, same argument as
  `[:11]`); `repr` vs `str` of a non-string date (equivalent for int/list); the summary's three numbers against `len(seen)`,
  `len(cur) +/- len(bad)`, `len(base)` (C1/C11/C12 cover each); the two tests' ORDER in the walk (C3 pins it: a ceiling-first
  order prints the wrong reason for an on-cutoff new answer); `%s` for `%r` in the refusal line and the class line (C9, R1 whole
  strings); `insert(0)` -> `append`/`insert(1)` (R1); `n["total"]` outside the loop and `x.get("d") or "…"` in `summary()`
  (R2/R2b); the class attribute's spelling (R1, the `cells()` regex); `[ ! -f ]` -> `[ -f ]` and another `$CED` path (W1/W6);
  `-eq 0` -> `-le 0`, `else` -> `elif -ge 2` (equivalent for a non-negative rc); `python` -> `python3` (machine-dependent, not a
  decision); a six-field baseline row (IndexError -> rc 2); `BASELINE == DEFAULT_BASELINE` -> a basename test (a benign
  WIDENING of the pin; equivalent on every row); `e(d)[:20]` (unpinned, implausible; no fixture d exceeds 20 characters).  Not
  swept: two-condition edits beyond the two design mutants; `stage_tokens.py`; the controls' own code as a target.

## 4. The records (section 5) -- true of what ships, with these exceptions

Every number re-derived (section 0) and every sentence read:
1. **W8's comment** ("python is not on the PATH it is given", 4a :800, and the packet's 2b): imprecise -- the git-bash wrapper
   prepends `/mingw64/bin`, `/usr/bin` and `~/bin` to that PATH (MEASURED); none holds a python here.  Say so, and that W8 fails
   LOUDLY on a machine where one does (change 10).
2. **"(any whitespace)"** (the CONTRACT :42): SAMPLED, 4 of 29 code points; `x_wsset4` escapes behaviourally (change 7).
3. **The closure's and 5d's "rows the DUAL edge of every pin ... the edit an earlier pin would not see -- or discloses it with its
   reason"**: true on the axis v5 closed; on the complement axis (section 2) the edits are neither rowed nor disclosed today.
   True once changes 1-9 land; no separate edit then.
4. **5d "103 mutants killed by the rows their lines name"**: 105 - 2 = 103, and the mirror table says so (MEASURED).
Everything else checks: 5a's 670 / 1,397 / 365 and the two artifact paths (exist); 5b's `dashmissingd` row (its census
reproduced; its title's 814 / 2,953 / 682), the closure note ("five passes", the roster, the witness's 1,503 -> 833 = 670,
"105/105 ... two escapes recorded as equivalent"), the hold_question's row names (all exist in 4a), every seat entry (section 0,
READ against the v4 answers); 5c's three counts (MEASURED); 5d's 96 rows, the two equivalent escapes, the 1,100 / 2 / 1,352,
"d_nonote2 and d_dfold2 ... killed by C15/C16 and by C25d" (among their killers; "exactly" is gone), `run_mutants.py` ->
`run_controls_v2.py` (READ), "the v1-v4 runners and receipts are kept" (`ls`).  Not checkable before the commit: "installed byte
for byte" (the md5s in the receipt header are the staged files' today).

## 5. Which of the 28 dispositions is wrong?  28 of 28 checked

None is wrong as a DISPOSITION.  Two are INCOMPLETE on the fix -- the verb right, the pin with an open edge on the complement
axis, both MINE: **K2** (one binding is pinned; the checker's use site and the dict's mutation are not -- the mutation
equivalent-or-loud by the product, the use site a real novel-spelling escape), **K14** (four whitespace code points of 29).  One
is IMPRECISE in its record: **K12**'s W8 premise (the wrapper's PATH).  The other 25 hold as written and as fixed.

## 6. The ten changes (controls and records; no code)

1. **R1** also asserts a NON-legacy cell's WHOLE tooltip -- the fixture's fable5 ✓ and codex … cells are exactly
   `2026-10-16 — a renderer control` (escaped as `cell()` does).  Kills `x_tippend` and `x_tipnotok`: the "only legacy" edge.
2. **R1h** asserts the glyph `' ✓'` exactly beside the class (its detail already prints it).  Kills `x_glyphstrip` behaviourally;
   today R3's presence pin is the only red.
3. **C11** asserts the hint line WHOLE (`-> give each a `d` from ✓ ✕ ⏸ … (or omit `d`, which renders as …); a non-answer record is
   exempt`).  Kills `x_hinttail`.
4. **C19c**: a new answer dated `2026-9-17` with d OK -> rc 1 and its refusal line EXACTLY (WHY_CEIL + WHY_ISO).  Kills
   `x_isodigits`, which would refuse September as "dated on or after the cutoff".
5. **R2's `census()` guarded for a failed render**: R2 (and R2b) say NO "render FAILED (a crash is not a kill)" and the run
   COMPLETES with its tally and sentinel, so a renderer that crashes on the shipped ledger is scored a KILL, not INCOMPLETE.
   Measured twice: `D_CLASS["OK"] = "ok"` and the comment-only null medium.
6. **C27's other two faces**: refuse a Subscript/Attribute store or delete whose value is `D_CLASS`/`DOMAIN` and any Call on
   `<name>.update/setdefault/pop/popitem/clear` (kills `x_dclassmut`, `x_dclassupdate`); pin the checker's USE SITE by ast --
   every Load of `DOMAIN` is the direct right operand of an `in` Compare, or the argument of the hint's join -- or DISCLOSE
   `x_usesite` as the novel-spelling escape it is (the plausible spelling dies on C1); and write beside the disclosure that
   `summary()`'s literal keys make a fifth D_CLASS key crash the generator on the first entry that spells it (KeyError,
   measured) -- loud by accident, to be kept deliberately.  Disclose `globals()[...]`/import aliases as outside the pin.
7. **R1d**: EXHAUST the body-tested partition -- one fixture entry per `str.isspace()` code point (29) in the whitespace row --
   or re-word the CONTRACT's "(any whitespace)" to SAMPLED 4 of 29 and disclose `x_wsset4`.
8. **C17j**: a baseline row with a None field -> rc 2 (kills `x_strnone`), or disclose it beside C17h/i as override-only,
   md5-bound.
9. **The DISCLOSED list grows**, each with its reason: `x_apparatusmsg` (the apparatus lines' TEXT is unpinned -- rc is; or the
   C21 rows assert their reason text, K5's shape); `x_phasenone` and `x_tipempty` (equivalent on this ledger: 0 off-domain
   answers without a phase, seat or note); `x_isocutle` (`[:11]` == `[:10]` for ISO-opened strings); `x_w_head2` (one line when
   clean); `x_q2paren` (display); `x_domglobals` (dynamic namespace writes; adversarial).
10. **Records**: W8's comment (section 4, item 1); and the closure/5d "dual edge" sentence stands once 1-9 land.

Chain status, in the stop condition's terms: this pass's floor count is ZERO with its denominator named (18 decisions, 105 +
25 mutants, four clauses); the sixteen escapes are clause-(e) contract debt on a named axis and are L1 because nothing has
shipped.  If that grading survives adjudication the chain closes here: the rows land in the commit beside their own kill
receipts (each owes a measured red on the mutant named above), and the pass that verifies them is the commit's receipt, not
another panel.  What I could not check: `agent_models.py` for this seat; the other three seats' answers (deliberately unread --
a parallel pass); the kills of the rows I ask for (I measured the ESCAPES; each row's observable is the one its mutant
changes, so the kill is predicted, not measured); "installed byte for byte" at commit.
