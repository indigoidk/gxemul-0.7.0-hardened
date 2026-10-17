FABLE_DASHOKV3_20261017
# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)
VERDICT: SHIP WITH CHANGES (3) -- both v3 receipts and the kill table reproduce line for line from the staged files and HEAD's ledger (46/46, 37/46 with the same nine reds, 32/32 with the same red sets); H6 reproduces exactly (a fresh clone on this machine checks the LF baseline out as 89d1d370, v3 rc 0 on it with the pin live, v2 rc 2); v3 refuses nothing v2 passed and passes nothing misshapen v2 refused. But the floor question does not come back empty: `if cls == LEGACY:` -> `if cls == LEGACY and d == "OK":` in the renderer passes all 46 (R1 asserts the legacy tooltip of the OK cell only), which keys the ruled LABEL on one spelling -- the clause-(d) shape, caught before commit (L1); a `good` on Q2's MISSING-checker branch also passes all 46 (no null-medium leg for the wiring); and three record sentences overclaim. The chain therefore does not close on this pass by its own stop condition; the repair is two control rows and two kill-table lines, no product line.

Seat: Fable 5.1, file-reading and measuring.  Mirror: `scratchpad/dashokv3/mirror` -- the repo's `stage_tokens.py`,
`git show 8bf8b5a1:tools/pipeline/ledger.json`, `staged_v2/`, `staged_v3/`, `run_controls_v3.py`, `run_mutants_v3.py`,
`gen_dashboard_before.py` (MEASURED identical to HEAD's renderer), `dashmissingd_census.py`.  Nothing under the project was
written but this file.  The receipt header's four md5 prefixes (0266971b | 483af869 | 74358345 | 06a3ffc6) are the staged_v3
checker, renderer, precommit and baseline exactly (MEASURED), so section 4b is of the files in section 3.  The staged precommit
is HEAD's plus 32 added lines and 0 removed (the Q2 block only); the staged renderer is HEAD's plus the legacy class, the
tooltip line, the escape, the strip's fifth number and total, two CSS lines and the legend line -- nothing else (MEASURED by
diff).  Timing: the 46 controls run in 10 s here, the kill table in about six minutes.

## 1. My own findings (H2, H3, H4, H6, H8, H10, H13): disposition and fix, each

| # | disposition right? | fix right? | how |
|---|---|---|---|
| H2 (my part: the tooltip tail, the lexical date / deleted reason, which Q2 branch fired, ⏸/… incidental, whitespace `d`) | yes | **yes, and each has its mutant**: `r_tiptail` reds R1 alone; `d_lexdate` reds C19b alone and `d_noreason` C19a+C19b alone (the output must NAME "its date is not ISO"); `w_rc7`/`w_msg`/`w_subshell` red W2 (+W4/W5, the same branch); `d_domnohold`/`d_domnopend` have their direct rows C2c/C2d; `r_wsblank` reds R1d.  **But R1's whole-tip assertion is of ONE cell** -- see section 3 | MEASURED (the table reproduced; `LEGACY_TIP` compared whole at `r1()`, `legacy_tip = head[SEATS.index("opus5")][2]`) |
| H3 | yes | yes: `d_nonote` reds C1 and thirteen more, all the rc-0 fixtures that hold off-domain answers (the one-sided key mismatch), and the line says so; `d_nonote2` reds **exactly C15 and C16** | MEASURED |
| H4 | yes | yes: `run_mutants.py` names `run_controls_v2.py` (grep), `run_mutants_v3.py` names `run_controls_v3.py` and takes CTL_*; the v3 receipts are of the staged files by md5 | MEASURED |
| H6 (I named the exposure, the main loop measured it) | yes | **yes** -- reproduced end to end: a temp repo with `core.autocrlf=false`, the LF baseline committed (blob md5 06a3ffc6), `git clone` on this machine (the clone's `.git/config` has no autocrlf, so the system `true` applies), the checkout is 89d1d370 with CRLF; the staged v3 checker on that copy with the pin live: rc 0, 1356/1356; the staged v2 checker: rc 2 "has md5 89d1d370, not the pinned 06a3ffc6".  C18b and `d_crlfpin` pin it | MEASURED |
| H8 | yes | yes: docstring lines 23-25 and the Q2 comment name the three exits | READ |
| H10 | yes | yes: "(after a refused exemption's line, if any)" at the renderer comment; `cell()` inserts the legacy line first and the refusal line on top of it | READ |
| H13 | yes | yes: disclosed in the controls' docstring; the production wiring IS correct by inspection -- `bad () { fail=$((fail+1)); ... }`, `set -u` only, `exit 1` when `fail -gt 0` at the tail, `_HERE` defined at line 27 | READ |

## 2. The repair as material: no path where v3 does wrong what v2 did right

The v2 -> v3 CODE changes are exactly four (READ, section 3 = the staged source I read whole): the md5 fold, the ledger-walk
wrap, and two message strings; everything else is comment.  The population, date and ceiling logic is byte-identical.

* **Nothing harmless newly refused.**  The pre-repair column proves it: the nine reds of v3's suite on v2 (reproduced, same
  rows) are five reworded-output assertions (C1, W1, W2, W4, W5), three rc-2 shape rows (C21a-c) and the CRLF pin (C18b) --
  every one a v3-NEW assertion, none an input v2 passed and v3 refuses.
* **One new acceptance, by design**: a CRLF checkout of the baseline.  The fold cannot make a misshapen file pass -- the JSON
  parse and the row-shape test still run on the folded bytes -- and a file committed WITH CRLF (which git does not convert on
  checkout) hashes the same as its LF form, which is the intent.
* **Misshapen inputs, side by side** (MEASURED, HEAD's ledger plus one shape each): an int note, a string entry, a list entry
  and `"entries": null` -> v2 rc 1 with a traceback, v3 rc 2 `APPARATUS FAIL: ledger misshapen (TypeError: ...)`; a list note,
  an explicit `d: null` (refused as `'None'`), a padded `" ✓"` and a list date are refused identically by both.  The wrap guards
  only the population walk, so it cannot turn a refusal into a pass; it turns crashes into a named rc 2 -- including a
  `stage_tokens` exception on a non-string note, which is honest.
* **Q2 is green at landing whichever ledger ships**: the working-tree ledger (29 lines changed since HEAD) holds 1,356
  off-domain answers with 0 keys over the ceiling (MEASURED), and the landing's own thirteen entries carry ✓, no `d`, or a
  HELD marker -- none off-domain.

## 3. The kill table and the floor

**Reproduced line for line** (MEASURED): BASE 46/46, 32/32 as recorded, the same red set on every line.  **Every named kill is
for the named reason**, and the extra reds are explained, not incidental to the pin: `d_blank` also reds C1/C11 because the 23
blank-`d` answers leave the population; `d_domnohold`/`d_domnopend` red fifteen rows because every explicit ⏸/… answer in the
ledger turns off-domain and unfrozen, while C2c/C2d are the direct, isolated pins; `d_dupplus1` reds every "exactly one beyond"
row; `d_pinoverride` reds the override-path rows (fixture baselines now meet the pin); `d_noreconf` reds the nine rc-1 rows that
print the glyph hint; `r_ok`/`r_pend` red R1b/R1d (class), R2 (the census) and R3 -- R3 only as a PRESENCE pin, the find-text
being gone; `w_rc7`/`w_msg`/`w_subshell` share W2's branch with W4/W5.  `d_lexdate` C19b alone, `d_noreason` C19a+C19b alone,
`d_nonote` C1 as its comment says, `d_nonote2` C15+C16 exactly.  The only entries counted twice-over are the two the packet
already names (`d_nonote`, `r_*`'s R3).

**One-edit mutants NOT in the table, 23 built, run through the 46** (MEASURED; `extra_mutants.py` / `extra2.py` in the mirror):

```
x_tipOKonly        46/46  ESCAPES   render:   "    if cls == LEGACY:\n" -> "    if cls == LEGACY and d == \"OK\":\n"
x_tipnonblank      46/46  ESCAPES   render:   ... -> "    if cls == LEGACY and str(d).strip():\n"
x_missinggood      46/46  ESCAPES   precommit: the MISSING branch's `bad "check_entry_domain.py MISSING ..."` -> `good ...`
x_nulld            46/46  ESCAPES   checker:  'if "d" not in x or' -> 'if x.get("d") is None or'   (a null d treated as missing)
x_clsstrip         44/46  R3 ONLY   render:   D_CLASS.get(d, LEGACY) -> D_CLASS.get(str(d).strip(), LEGACY)   (a presence pin)
x_cssgone          46/46  ESCAPES   render:   the two td.c.legacy CSS lines deleted            (presentation)
x_hintgone         46/46  ESCAPES   checker:  the "-> give each a `d` from ..." line deleted    (no control asserts it)
x_nostderr, x_head2, x_prefix, x_count0, x_len7, x_md5cr, x_notseat_pass   46/46   equivalent or cosmetic, as predicted
x_isheld           31/46  C1 ...    checker:  `not st.is_answer(x)` -> `st.is_held(x)`  (the five NOTSEAT off-domain records enter)
x_seenge           32/46  C1 ...    checker:  `seen[t] > base[t]` -> `>=`
x_cutoff16         45/46  C12       checker:  CUTOFF -> 2026-10-16   (C12 pins the cutoff in BOTH directions)
x_nobaseoverride   42/46  C11 ...   checker:  GXDOMAIN_BASELINE ignored
x_noledgeroverride 19/46  C1 ...    checker:  GXLEDGER ignored
x_tipappend        45/46  R1        render:   tip.insert(0, legacy line) -> tip.append(...)
x_rcge             45/46  W3        precommit: `-eq 1` -> `-ge 1`
```

**(A) One escape breaks a RULED property.**  `x_tipOKonly`: the fix's own guard `if cls == LEGACY:` qualified with a second
predicate -- the canonical clause-(d) form, `if (X)` -> `if (X && Y)` -- and the 46 stay green, because R1 compares the whole
tooltip of the opus5 (`OK`) cell only; the agy (blank -> `?`) and minimax (`N/A`) legacy cells are asserted for class and glyph,
not tip (`bad` compares `(g[0], g[1])`).  Under the mutant the LABEL "legacy -- verdict unclassified" is keyed on one spelling,
which is the "keyed on `OK` alone" defect F2 rejected for the class ("every explicit `d` outside the four glyphs renders as one
residue class, labelled ... keyed on the DOMAIN, not the spelling"), relocated to the label.  Caught before commit, so **L1**,
not a reopening -- but it is the shape the floor exists for, and it is the SAME CLASS the adjudication pass found (R1 pinned a
PREFIX of the tip; now R1 pins ONE CELL of the tip): two consecutive passes, one class.  Per the repair-chain amendment the
repair owes the class closure, not the cell: assert the whole tooltip of EVERY legacy cell in the fixture, and say in the
controls' docstring which cells are rowed.  `x_tipnonblank` is the sibling (the blank cell's label).

**(B) One escape breaks a CLAIMED property of the record.**  `x_missinggood`: the Q2 block says "HARD ... never silently
green", and its MISSING-checker branch is the one guard no W row exercises -- a `good` there is 46/46 green with no checker on
disk.  This is the wiring's NULL MEDIUM in the carrier's clause-(c) sense ("an ABSENT binary"), and it has no leg: one W6 row
(`w_tools` with the checker absent -> BAD "MISSING") plus a kill-table line.

**(C) Disclosed, no row owed.**  `x_nulld`: an explicit `"d": null` is a third member of the d-present partition no row holds
(0 in the ledger); as shipped the checker refuses a new one as `'None'` and the renderer shows legacy `None`, which is
consistent.  `x_clsstrip`: a padded glyph would take its stripped class while the checker refuses it (0 such values; behaviourally
unpinned, R3 caught it only because its find-text vanished).  `x_cssgone`, `x_hintgone`: presentation and the instruction line.
Optional and direct rather than incidental: `x_isheld` is killed by C1 only because five NOTSEAT records with an off-domain `d`
sit in the shipped ledger -- the same incidental shape the adjudication pass repaired for ⏸/…; a C8b row ("a NOTSEAT record after
the cutoff with `d` OK -> 0") would pin condition 2's second token directly.

**Shapes swept (the DEPENDS-ON enumeration, each cell named to its row):** the checker's four guards -- population (`d` present
x in-domain x `is_answer`: C7, C8, C14, C2-C2d, `x_nulld`, `x_isheld`, `x_notseat_pass`), date (ISO shape x `>=` cutoff: C12
in both directions, C19a/b, `d_lexdate`, `x_prefix`), ceiling (`>` / `>=` / `+1`: C1, C9, C15, C16, `d_dupplus1`, `x_seenge`),
pin (default x override x md5 x line endings: C18, C18b, C13, `d_pinoverride`, `x_nobaseoverride`, `x_md5cr`), plus the two
path overrides and the ledger walk (C21a-c, the eight shapes of section 2); the renderer's guard `cls == LEGACY` x the fixture's
three legacy spellings -- the CLASS rowed at all three, the TIP at one (the escape); the strip (R2) and the legend (R4) whole;
Q2's three rc branches rowed (W1-W3), the override strips rowed (W4, W5), the MISSING guard not rowed (the escape).  Not swept:
`_latest`, holds and record precedence -- unchanged from HEAD and outside the diff.

## 4. The records (section 5): sentences that are false or overclaim

1. **CHANGELOG draft: "46/46 on the landed files (`RECEIPT_v3_on_staged_v3.txt`)".**  The receipt is of the STAGED files --
   its own header says so by md5.  "Landed" is a prediction written in the measured column unless the controls are re-run after
   install.  Write "on the staged files, installed byte for byte (md5 0266971b | 483af869 | 74358345)", or re-run on the tree
   and cite that receipt.  And after the two rows of section 3 land the suite is 48, so **every "46/46" in section 5** (the
   CHANGELOG, the closure note, the witness field, the hold_question) must be re-derived from the re-run, never edited by hand.
2. **Ledger, grok's adjudication-pass entry: "(measured the same hour: a fresh clone gives 89d1d370 for 06a3ffc6)"** reads as
   grok's measurement; grok's answer says "I did not re-run ... did not recompute BASELINE_MD5".  H6's row has it right ("main
   loop (measured)"); the entry should say "(the main loop measured it the same hour)".
3. **Checker docstring lines 10-12: "Ruled by ... (RULINGS_C_records.md, F2): every mechanical sweep ... is withdrawn -- an OK
   becomes ✓ or anything else only when a reader rewrites that one entry."**  RULINGS_C F2 says "Every mechanical sweep stays
   withdrawn (3/3)" and "UPHELD with the class re-keyed"; the second sentence is `packet_C_records.md` F2 clause (d) -- the main
   loop's own new disposition -- which F2 upheld without restating.  True by UPHELD, invisible to a reader who greps RULINGS_C.
   Cite "packet_C_records.md F2 (d), upheld by RULINGS_C F2".  (The Q2 comment cites F2 without quoting (d); fine.)

True as written, re-derived: the docstring's census (5,177 / 1,397 / 1,356; OK 439, N/A 248, y 89, blank 23; the latest
2026-09-19; 0 empty notes; 0 non-ISO dates in 1,342 keys), the six multiplicity-> 1 keys, `baseline_write.out`'s 1,356 in
1,342, R2's 1,503 -> 833 + 670, the strip `1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177`, the dashmissingd census (1,561 / 300 /
2,953 / 814 / 682 -- reproduced exactly), `d_notenone`'s equivalence (0 empty notes), `d_nonote2` by exactly C15/C16,
`run_mutants.py` naming v2, the OB preview's 670 / 1,397, 5c's "adapted from", and the hold entry's live marker in the regress
phase with its `hold_question`.  The `dashmissingd` row is a true record; its question is incomplete (section 5, item 3).

## 5. Section 2b, each

1. **H1 -- ship the ceiling, stated as the ceiling (which v3 does).**  REASONED on measured facts.  (i) F2's clause (d) governs
   WHEN a classification may change -- only when a reader rewrites that one entry; it forbids sweeps, it does not ask the check
   to detect a revert.  A reader who restores a converted entry byte for byte HAS rewritten that one entry; (d) licenses it.
   (ii) The `ev`-only replacement adds no verdict text a reader sees -- same `d`, same note -- and the ceiling admits it only in
   place of the converted one, never beside it.  (iii) The alternatives are worse or not this round's: a comparison against
   HEAD's ledger has the measured hole from my adjudication-pass answer (convert X, add Y with X's tuple leaves the per-tuple
   count unchanged) unless it compares whole entries -- and then it either refuses the `ev`/`grade`/`b` edits the ruling allows
   or excludes them, at which point it IS the six-field ceiling computed against HEAD, with no blob at the first landing and an
   exception owed at every re-freeze; persistent ids are a schema change over 5,177 entries and an owner decision.  So: the
   ceiling, with the three passing cases named where a reader meets them (done), and the stronger mechanism filed if anyone wants
   it -- not built here.
2. **H6 -- the fold is the right repair, and it is the testable half.**  MEASURED (section 1).  A `.gitattributes` line
   (`tools/pipeline/entry_domain_baseline.json text eol=lf`, or `-text`) acts at CHECKOUT, which no control can observe, and the
   repo has no `.gitattributes` at all -- `ledger.json` is committed CRLF, the sources LF -- so adding one is a repo-wide
   line-ending policy, an owner decision with its own blast radius (`* text=auto` would renormalise on the next touch).  The fold
   lives in the checker, is pinned by C18b and `d_crlfpin`, and is the whole defence a reader of the checker needs.  Belt and
   braces is fine; the braces are the owner's.
3. **H14 -- filing is right; LOW is right; the filed question is INCOMPLETE.**  F2 as upheld says in clause (c) "missing `d` =
   the existing `…` default", so reversing condition 1 changes a ruled disposition -- adjudication, not a rider; and the
   renderer alternative moves 814 displayed cells.  LOW matches `dashokclass` (display only, no gate reads `d`); 814 > 670 does
   not change the harm class.  **What the row must add** (MEASURED at HEAD): 158 entries whose note says NOT FIRED or names the
   roster, 127 of them untokened -- i.e. ANSWERS by `is_answer`, 71 with no `d` -- and `check_stage_panels.py` COUNTS an untokened
   entry as a recorded seat (`if not st.is_answer(ent): continue`, then `seats.add`) while a NOTSEAT one is skipped.  So the
   project's standing way to satisfy section H's nine-seat count under a reduced roster is exactly the population dashmissingd
   counts, and a Q2 that refused a new `d`-less answer would refuse the next landing's five "not fired" entries, while tokening
   them NOTSEAT turns H red at 4/9.  The rule question is entangled with H; name it in the row so the adjudicators rule on both.
4. **The landing's own entries -- yes, as the least-wrong practice today, with two conditions.**  `d` ✓ for an answered seat
   whose SWC changes were applied: the ledger's precedent is split (179 SHIP WITH CHANGES entries at HEAD: 147 no `d`, 32 ✓),
   ✓ reads "approved" in the legend, and the seat approved v2-with-changes, not v3 -- so the v3-pass entries must carry each
   seat's OWN v3 verdict, and the ✓ on an adjudication-pass SWC is the author's reading (the closure's `A` badge covers it).  No
   `d` for a seat deliberately not fired: the ledger's convention (above) and the only form section H accepts; keep it for this
   landing, with the H collision filed under `dashmissingd`.  The carrier's distinction -- not fired is not a seat failure -- is
   carried by the note today and by nothing the dashboard renders; that is dashmissingd's subject, not this landing's.

## 6. Which accepted dispositions are wrong -- 14 of 14 checked (H1-H14)

Wrong outright: **none**.  To sharpen, two: **H14** (the filed question omits the section-H / NOTSEAT collision, section 5
item 3); **H6** (the disposition is right; grok's ledger entry in section 5 attributes the measurement to the wrong seat).
Holding, twelve: H1 (the narrower guarantee is the right one to ship, section 5 item 1), H2 (all named instances pinned -- the
CLASS stays open, section 3), H3, H4, H5 (the wrap names the exception type; eight shapes measured), H7, H8, H9, H10, H11,
H12, H13.

## The three changes

1. **(L1, the floor shape)** R1 asserts the WHOLE tooltip of every legacy cell in the fixture -- opus5 `OK`, agy blank, minimax
   `N/A` -- and the controls' docstring says so; kill-table line `r_tipokonly` (`"    if cls == LEGACY:\n"` -> `... and d ==
   "OK":\n`) must red R1.  That closes the class R1's coverage has now missed twice, not the cell.
2. **(L1/L3, the wiring's null medium)** W6: `w_tools` with the checker ABSENT -> BAD "check_entry_domain.py MISSING";
   kill-table line `w_missinggood` -> W6.  Optional beside it: C8b, a NOTSEAT record after the cutoff with `d` OK -> 0.
3. **(L4)** the three sentences of section 4; then re-run both receipts and the kill table from the staged names and re-derive
   every count section 5 quotes (the suite becomes 48).

By the packet's own stop condition the chain does not close on this pass: one clause-(d) escape of the detector shipped with the
fix is measured, and both repairs are detector-only (two rows, two kill-table lines, no product change).  Whether that two-line
repair takes a short v4 pass or rides the regress hold already filed for the flagship is the adjudicator's call; the rule's
letter says a pass, its amendment says the pass verifies the ENUMERATION (which cells are rowed) rather than hunting cells.

## What I could not check

* The other seats' v3 answers: `codex_dashokv3.txt` (10 KB) landed while I was measuring and I did not read it;
  `grok_dashokv3.txt` was 191 bytes mid-answer.  The `agent_models.py` claims about my own earlier answers.
* The landing's section Q (`matrix.html` regeneration) -- not simulated; only the staged renderer on HEAD's ledger.
* The production `precommit_check.sh` end to end -- only the extracted Q2 block, as the controls run it.
* `write_baseline.py --force` not re-run; the staged baseline's raw md5 equals the pin and its 1,356-in-1,342 matches my count.

Durable artifacts: none in the project (one file allowed).  Every number above re-derives in under ten minutes from the mirror
recipe in the preamble; the extra mutants are the find/replace pairs quoted in section 3, each run through `run_controls_v3.py`
with the matching `CTL_*` override (the driver is `run_mutants_v3.py` with its list swapped).
