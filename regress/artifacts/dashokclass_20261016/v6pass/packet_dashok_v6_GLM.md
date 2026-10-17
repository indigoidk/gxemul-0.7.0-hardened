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

**Liveness:** open your answer with the token `GLM_DASHOKV6_20261017` on its own line, then your verdict line.

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

## 3. The files under test (UNCHANGED since v5: md5s in the receipt header)

### 3a. the staged checker, `staged_v5/tools/pipeline/check_entry_domain.py`, WHOLE

```python
     1	#!/usr/bin/env python3
     2	"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS WITHIN THE LEGACY CEILING FROZEN WHEN THIS CHECK LANDED.
     3	2026-10-16, ledger `dashokclass`; precommit section Q2.
     4	
     5	THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer -- or no
     6	`d` at all (the renderer's default is …).  MEASURED when this landed (HEAD 8bf8b5a1): 5,177 entries, 1,397 with an explicit
     7	`d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
     8	2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
     9	them as one residue class, "legacy -- verdict unclassified", and this check keeps answers with NEW content from appearing.
    10	Ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md F2, which upheld
    11	packet_C_records.md's F2): every mechanical sweep of the old entries is withdrawn, and -- that packet's clause (d), upheld
    12	there without restatement -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.
    13	
    14	ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt):
    15	  1. a MISSING `d` passes -- it renders as … (an explicit blank does NOT: it is an off-domain value);
    16	  2. an entry that is not an ANSWER passes whatever its `d` -- holds, annotations, records (stage_tokens.is_answer);
    17	  3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
    18	  4. the controls carry POSITIVE rows (a valid glyph on and after the cutoff passes) beside the negatives.
    19	
    20	GRANDFATHERING IS A CEILING OVER SELECTED CONTENT -- NOT A DATE, AND NOT AN ENTRY IDENTITY.  An off-domain answer passes
    21	only while the ledger holds no more answers with its (row, phase, seat, date, `d`, sha1 of its NOTE) than
    22	`entry_domain_baseline.json` froze when this check landed, and only if it is not dated on or after CUTOFF.  So UNMATCHED
    23	selected content fails and so does an EXCESS occurrence -- a new answer, a back-dated or undated one, a copy, an old one
    24	EDITED in any of those six fields -- while an admitted replacement, identical in all six, can be new (GPT-6 Astra, v3 pass).
    25	Editing such an entry means classifying it -- a glyph, or no `d` at all (it renders as …), or a non-answer record token if it is not an
    26	answer.  For a NOTE-only correction that is this check's toll, not the ruling's: the ruling withdraws every mechanical sweep
    27	and classifies an entry when a reader rewrites it, and says nothing of note edits (Grok 4.7, adjudication pass).  (Pass 2,
    28	2026-10-16: a per-(row, phase, seat, date, d)
    29	count let a converted entry's allowance be refilled by a new answer with another note, measured by GPT-6 Astra and Fable
    30	5.1; the note is in the key for that reason.)
    31	
    32	THE GUARANTEE IS THE NARROWER ONE, in GPT-6 Astra's words at the adjudication pass: CURRENT SELECTED-CONTENT MULTIPLICITIES
    33	CANNOT EXCEED THEIR LANDING BASELINE.  The six fields are not an identity -- 1,342 distinct keys cover the 1,356 frozen
    34	answers -- and the check reads no earlier revision, so three things pass: an entry converted to a glyph and later restored
    35	byte for byte (a revert); a replacement that matches a frozen entry in all six fields and differs only outside them; and an
    36	edit outside them (`ev`, `grade`, `b`; stage_tokens.is_answer reads only the note, so such an edit cannot turn a record into
    37	an answer).  So the count within the ceiling never exceeds 1,356 -- until a reviewed re-freeze changes the pin -- and can
    38	climb back to it after shrinking.  It is not the
    39	dashboard's legacy count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that
    40	reappears when a newer answer in its cell is removed.
    41	
    42	THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`), which makes a re-freeze VISIBLE: it has to change that constant in the
    43	same commit, with its reason, where a reviewer sees both -- never a silent re-run of the one-time writer
    44	(regress/artifacts/dashokclass_20261016/write_baseline.py, which refuses to overwrite without --force).  That the change was
    45	REVIEWED is a practice the pin cannot enforce (GPT-6 Astra and Fable 5.1, adjudication pass).  The md5 is taken with CRLF
    46	folded to LF: this machine's system git sets core.autocrlf=true, and a fresh clone checked the file out as 89d1d370 for
    47	06a3ffc6 (measured at the adjudication pass), which a raw pin would red on every commit.  A GXDOMAIN_BASELINE override skips
    48	the pin, for the controls; precommit Q2 strips it.
    49	
    50	The cutoff reads a date only when it OPENS with the ISO shape `YYYY-MM-DD` -- a shape test, not a calendar check: a
    51	"2026-13-45" counts as on or after it and fails; a "2026-02-30" counts as before it and must match a frozen entry.  A date in
    52	any other form, or none, is never "on or after the cutoff", so it passes only by matching a frozen entry -- and the baseline
    53	holds none: 0 of its 1,342 keys carries an empty or non-ISO date (measured at landing).
    54	
    55	Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
    56	Exit: 0 clean; 1 an off-domain answer beyond the frozen ceiling (each named); 2 apparatus failure (baseline or ledger
    57	unreadable or misshapen -- every container level is type-checked before it is walked -- or the baseline's md5 is not the
    58	pinned one)."""
    59	import collections, hashlib, io, json, os, re, sys
    60	
    61	HERE = os.path.dirname(os.path.abspath(__file__))
    62	sys.path.insert(0, HERE)
    63	import stage_tokens as st  # noqa: E402
    64	
    65	LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
    66	DEFAULT_BASELINE = os.path.join(HERE, "entry_domain_baseline.json")
    67	BASELINE = os.environ.get("GXDOMAIN_BASELINE") or DEFAULT_BASELINE
    68	BASELINE_MD5 = "06a3ffc6929be628c8254fe4e818ee99"      # the md5 of entry_domain_baseline.json as frozen; change only by a reviewed re-freeze
    69	DOMAIN = ("✓", "✕", "⏸", "…")      # gen_dashboard.py's D_CLASS keys; the two must agree
    70	CUTOFF = "2026-10-17"               # inclusive: an off-domain answer dated on or after it always fails
    71	ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")
    72	
    73	
    74	def note_sha(x):
    75	    return hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]
    76	
    77	
    78	def date_str(x):
    79	    v = x.get("date")
    80	    return v if isinstance(v, str) else ("" if v is None else repr(v))
    81	
    82	
    83	def off_domain_answers(ledger):
    84	    """(row, phase, seat, date, d, note_sha) for every ANSWER entry carrying an explicit `d` outside DOMAIN."""
    85	    out = []
    86	    for r in ledger.get("rows", []):
    87	        for x in r.get("entries", []):
    88	            if "d" not in x or x["d"] in DOMAIN or not st.is_answer(x):
    89	                continue
    90	            out.append((str(r.get("id")), str(x.get("phase") or ""), str(x.get("seat") or ""), date_str(x), str(x["d"]),
    91	                        note_sha(x)))
    92	    return out
    93	
    94	
    95	def ledger_shape(ledger):
    96	    #  the first structural problem, or None.  A container of the wrong type WALKS AS EMPTY and passes -- {"rows": {}} and a
    97	    #  string entry were rc 0 (GPT-6 Astra, v3 pass) -- so every level is checked before anything is walked
    98	    if not isinstance(ledger, dict):
    99	        return "the ledger is not an object"
   100	    rows = ledger.get("rows")
   101	    if not isinstance(rows, list):
   102	        return "rows is not a list"
   103	    for i, r in enumerate(rows):
   104	        if not isinstance(r, dict):
   105	            return "row %d is not an object" % i
   106	        ents = r.get("entries", [])
   107	        if not isinstance(ents, list):
   108	            return "row %r: entries is not a list" % (r.get("id"),)
   109	        for x in ents:
   110	            if not isinstance(x, dict):
   111	                return "row %r: an entry is not an object" % (r.get("id"),)
   112	    return None
   113	
   114	
   115	def main():
   116	    #  precommit runs this with stdout on a PIPE, which Windows python opens as cp1252: a glyph or a non-ASCII `d` in the
   117	    #  failure lines raised UnicodeEncodeError and buried the instruction under a traceback (Fable 5.1, pass 2, measured)
   118	    if hasattr(sys.stdout, "reconfigure"):
   119	        sys.stdout.reconfigure(errors="backslashreplace")
   120	    try:
   121	        ledger = json.load(io.open(LEDGER, encoding="utf-8"))
   122	    except Exception as ex:
   123	        print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2
   124	    try:
   125	        raw = open(BASELINE, "rb").read()
   126	        md = hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()      # line endings folded: see the docstring
   127	        if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:
   128	            print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
   129	                  "in the same commit, with its reason" % (BASELINE, md, BASELINE_MD5)); return 2
   130	        base = collections.Counter()
   131	        rows_b = json.loads(raw.decode("utf-8"))
   132	        if not isinstance(rows_b, list):
   133	            raise ValueError("the baseline is not a list")
   134	        for k in rows_b:
   135	            if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
   136	                    and k[6] > 0):
   137	                raise ValueError("baseline row %r is not [row, phase, seat, date, d, note_sha, count]" % (k,))
   138	            base[tuple(k[:6])] += k[6]
   139	    except Exception as ex:
   140	        print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
   141	    shape = ledger_shape(ledger)
   142	    if shape:
   143	        print("APPARATUS FAIL: ledger misshapen: %s (%s)" % (LEDGER, shape)); return 2
   144	    try:
   145	        cur = off_domain_answers(ledger)
   146	    except Exception as ex:      # {"rows": null}, a row that is not an object ... (GPT-6 Astra, adjudication pass)
   147	        print("APPARATUS FAIL: ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2
   148	    seen = collections.Counter()
   149	    bad = []
   150	    for t in cur:
   151	        seen[t] += 1
   152	        if ISO.match(t[3]) and t[3][:10] >= CUTOFF:
   153	            bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
   154	        elif seen[t] > base[t]:
   155	            why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
   156	            if t[3] and not ISO.match(t[3]):
   157	                why += "; its date is not ISO YYYY-MM-DD"
   158	            bad.append((t, why))
   159	    print("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff %s inclusive"
   160	          % (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))
   161	    for (row, phase, seat, date, d, ns), why in bad:
   162	        print("  OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s"
   163	              % (row, phase, seat, date or "(none)", d, ns, why))
   164	    if bad:
   165	        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"
   166	              % " ".join(DOMAIN))
   167	        return 1
   168	    return 0
   169	
   170	
   171	if __name__ == "__main__":
   172	    sys.exit(main())
```

### 3b. the renderer change, `gen_dashboard.py` HEAD -> staged (32 changed lines)

```diff
--- gen_dashboard.py@HEAD
+++ gen_dashboard.py@staged_v5
@@ -72,6 +72,20 @@
     sys.exit(2)
 
 D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
+#  *** AN EXPLICIT `d` OUTSIDE THOSE FOUR IS NO VERDICT THIS PAGE CAN CLASSIFY, AND UNTIL 2026-10-16 IT RENDERED AS A SEAT
+#  FAILURE.  (ledger `dashokclass`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, adj_20261016/RULINGS_C_records.md F2.  This
+#  heading said "NEITHER APPROVAL NOR A SEAT FAILURE" until the adjudication pass; some of them are a seat failure.) ***
+#  The fallback was `pend`, so 1,397 entries whose `d` is "OK", "N/A", a date, "y", "HELD", blank ... -- 439 of them "OK",
+#  365 displayed cells -- all read as "no answer / seat failure".  Mapping "OK" to `ok` was REJECTED (it canonises one
+#  off-domain spelling as approval); every mechanical sweep of the entries was withdrawn.  So an explicit `d` the map does
+#  not know, on the ANSWER a cell shows, renders as ONE residue class, LEGACY (a live hold and a non-answer record keep their
+#  own rendering whatever their `d` -- GPT-6 Astra, v3 pass), keeping its text, with the reason first in its tooltip (after a refused
+#  exemption's line, if any -- Fable 5.1, adjudication pass); a MISSING `d` is
+#  still `…`, an explicit blank shows `?`.  The class says only that the `d` is unclassified -- three legacy cells (`WALL`)
+#  record real seat failures in their notes, so the tooltip sends the reader to the note rather than denying either reading
+#  (GPT-6 Astra, pass 2).  check_entry_domain.py (precommit Q2) holds the off-domain ANSWERS to the ceiling frozen when it
+#  landed.
+LEGACY = "legacy"
 e = lambda t: html.escape(str(t), quote=True)
 
 BADGE_TIP = {"A": "the author did this review (shown, not hidden)",
@@ -158,12 +172,14 @@
                 f'<span class="g">{TOKEN_GLYPH}</span><span class="tip">{t}</span></span></td>')
     ent = _latest(ents)
     d = ent.get("d", "…")
-    cls = D_CLASS.get(d, "pend")
+    cls = D_CLASS.get(d, LEGACY)
     badge = ent.get("b", "")
     tip = [p for p in (ent.get("date"), ent.get("grade"),
                        BADGE_TIP.get(badge), ent.get("note")) if p]
     if ent.get("ev"):
         tip.append("evidence: " + ent["ev"])
+    if cls == LEGACY:
+        tip.insert(0, "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d)
     #  #534 F2 pass (codex): both of these lived only in the no-answer branch, so an ANSWER cell hid
     #  them -- a refused RE_READ rendered calm, and a record filed after the seat's answer vanished.
     if st.exempts_stage(ent):
@@ -175,7 +191,7 @@
     t = e(" — ".join(tip))
     b = f'<sup class="b b-{badge}">{badge}</sup>' if badge else ""
     return (f'<td class="c {cls}"><span class="wrap" tabindex="0">'
-            f'<span class="g">{d}</span>{b}<span class="tip">{t}</span></span></td>')
+            f'<span class="g">{e(d) if str(d).strip() else "?"}</span>{b}<span class="tip">{t}</span></span></td>')
 
 
 def fix_section(row):
@@ -255,10 +271,13 @@
 
 
 def summary():
-    n = {"✓": 0, "⏸": 0, "✕": 0, "…": 0}
+    #  the strip SUMS TO THE ENTRY TOTAL: every explicit `d` outside the four glyphs is counted once, as legacy
+    n = {"✓": 0, "⏸": 0, "✕": 0, "…": 0, LEGACY: 0, "total": 0}
     for r in L["rows"]:
         for x in r.get("entries", []):
-            n[x.get("d", "…")] = n.get(x.get("d", "…"), 0) + 1
+            d = x.get("d", "…")
+            n[d if d in D_CLASS else LEGACY] += 1
+            n["total"] += 1
     return n
 
 
@@ -369,6 +388,8 @@
 .c.bad .g {{ color:var(--bad); font-weight:700; }} .c.pend .g {{ color:var(--pend); }}
 .c.none .g {{ color:var(--line); }}
 .c.tok .g {{ color:var(--muted); }}
+td.c.legacy {{ outline:1px dashed var(--line); outline-offset:-3px; }}
+.c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}
 .b {{ font-size:9.5px; font-weight:700; margin-left:1px; color:var(--accent);
   border:1px solid var(--accent); border-radius:2px; padding:0 2px; vertical-align:6px; }}
 .b-s {{ color:var(--hold); border-color:var(--hold); }}
@@ -404,7 +425,7 @@
     <span>{e(bat["when"])} @ {e(bat["head"])}</span></span>
   <span class="chip"><span class="k">flagship</span><b>{e(sid[L["flagship"]]["name"])} ({e(sid[L["flagship"]]["ver"])})</b></span>
   <span class="chip"><span class="k">bugs</span><b>{len(open_rows)} in work · {len(closed_rows)} closed · {len(dropped_rows)} dropped</b></span>
-  <span class="chip"><span class="k">entries</span><b>{n["✓"]}✓ {n["✕"]}✕ {n["⏸"]}⏸ {n["…"]}…</b></span>
+  <span class="chip"><span class="k">entries</span><b>{n["✓"]}✓ {n["✕"]}✕ {n["⏸"]}⏸ {n["…"]}… {n[LEGACY]} legacy · {n["total"]} in all</b></span>
   <span class="chip"><span class="k">updated</span><b>{e(L["updated"])}</b></span>
 </div>
 <div class="matrix-scroll"><table>
@@ -416,6 +437,7 @@
   <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
   <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
   <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
+  <span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = an explicit blank)</span>
   <span><span class="g" style="color:var(--muted)">∅</span> a record, not an answer (exemption or main-loop note; hover for why)</span>
   <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
   <span><sup class="b">A</sup> the author did this review (shown)</span>
```

### 3c. precommit section Q2, as staged

```bash
#  ---- Q2 --------------------------------------------------------------------------
#  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS WITHIN THE FROZEN LEGACY CEILING.  2026-10-16, ledger `dashokclass`
#  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
#  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
#  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section holds the off-domain
#  ANSWERS to a CEILING frozen at landing: for each row, phase, seat, date, d and note, no more answers than the md5-pinned
#  baseline holds.  Not a date (a date-only cutoff cannot stop a back-dated or undated addition), not a count without the
#  note (a converted entry's allowance could be refilled; pass 2), and NOT an entry identity: a byte-identical revert of a
#  normalised entry passes, and the dashboard's legacy count can still rise through exempt records and re-exposed older
#  answers (adjudication pass, GPT-6 Astra).  HARD.  It fails on UNMATCHED content and on an EXCESS occurrence -- a NEW
#  off-domain answer, or an OLD one edited in any of those fields (an admitted replacement can be new; v3 pass): editing such an entry means classifying it -- a glyph, no `d`, or a non-answer record token (Fable
#  5.1); for a note-only correction that toll is this check's, not the ruling's (Grok 4.7).  It reds (rc 2) when the ledger
#  or the baseline is unreadable or misshapen or the baseline's md5 is not the pinned one, never silently green.
say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is within the frozen legacy ceiling"
CED=$_HERE/pipeline/check_entry_domain.py
if [ ! -f "$CED" ]; then
	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
else
	#  the overrides are for the controls, never for a commit: an exported GXDOMAIN_BASELINE would swap in another baseline
	#  and skip the md5 pin (Grok 4.7, pass 2), and an exported GXLEDGER would check another ledger (adjudication pass), so
	#  the section checks the real ledger against the pinned baseline
	_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1); _cedrc=$?
	if [ $_cedrc -eq 0 ]; then
		good "$(printf '%s\n' "$_ced" | head -1)"
	elif [ $_cedrc -eq 1 ]; then
		bad "an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one edited):"
		printf '%s\n' "$_ced" | sed 's/^/          /'
	else
		bad "check_entry_domain.py could not run (rc $_cedrc): $(printf '%s\n' "$_ced" | head -1)"
	fi
fi

#  ---- R ---------------------------------------------------------------------------
```

## 4. The repair: the controls, v5 -> v6 (the whole file and its diff are in the tree; this seat gets the parts below)

### 4a. the CONTRACT and the 115 rows -- the docstring of `run_controls_v6.py`

```
"""Controls for `dashokclass` (2026-10-17, v6 after the v5 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
the three files under test (run_mutants_v6.py and the staged runs use them); the defaults are the tree's.

  THE CONTRACT (v6) -- the v4 pass found pins that tested ONE edge of a decision, and v5 rowed the dual edge.  The v5 pass
  (GPT-6 Astra and Fable 5.1 measured, GLM 5.3 reasoned, Grok 4.7 traced) found the next layer on two axes.  A v5 pin covered
  PART of its decision's GENERATING SET -- the leading pad but not the trailing one, two of the baseline row's six string
  positions, the ISO shape's anchor but not its widths or separators, the glyph sets' Name stores while `globals()' and a dict
  mutation changed them, the hint's prefix, a tooltip whose fixture held no optional field, a CSS rule's presence but not the
  absence of an overriding one, the apparatus branch's first line on one-line output, four whitespace code points of 29, the
  newline and NBSP cells' class but not their tooltips, Q2's `else' at three of its 254 statuses, the named entry by a prefix
  of W2's output.  And a pin
  asserting a property of the SELECTED set said nothing about its COMPLEMENT (Fable 5.1) -- every legacy cell has the class
  line but not ONLY legacy cells, the padded cell's class but not its text, the set where it is DEFINED but not where it is
  USED.  So v6 enumerates each decision's generating set -- every operand position, both ends, every width and separator,
  every binding form and use, every optional field, every whitespace code point -- with its complement, and rows each
  member, or discloses it with its reason.
    checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
             `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
                                                                                        entries key: rc 0); C23 (not JSON)
             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
             fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
                                                                                        of true, -1, 0, 1.0), C17h-m (each of the
                                                                                        six positions numeric in turn), C17n (a
                                                                                        None field), C21g (an object)
             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C26b
                                                                                        (a list), C28 / C28b (a ✓ padded at its
                                                                                        start / its end), C2/C2b/C2c/C2d (each
                                                                                        glyph, C2c/C2d isolated), C8 (hold), C24
                                                                                        (a record, isolated)
             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
             ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
             over its UTF-8 text, after str()                                          with a trailing or a leading space);
                                                                                        C15/C16 (the note); C26b; C29 (no phase,
                                                                                        no seat: its line exact); C20b (a
                                                                                        non-ASCII note: its line exact); C21k (a
                                                                                        list note holding no token: refused)
             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
             the cutoff: inclusive; a date counts only when the ISO shape -- four      C3, C4, C12 (isolated: before / on /
             digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
                                                                                        dated 2026-10-17T12:00:00), C12w (MATCHED
                                                                                        identities breaking the shape in one
                                                                                        place -- year, month or day width, either
                                                                                        separator: rc 0), C19a/b
             output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
             ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
             refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
                                                                                        C6, C9, C19a, C20, C20b, C29, C21k (the
                                                                                        refusal line exact; C20's d escaped)
             the glyph sets: ONE binding of DOMAIN and of D_CLASS, each the four,       C27 (an ast walk of both files: every
             and no other way to change either                                         binding form of the name -- a store, a
                                                                                        delete, a global, an import alias, a def
                                                                                        or class, an except or match name, a
                                                                                        parameter, an attribute or subscript store
                                                                                        keyed by it; a call to globals / vars /
                                                                                        locals / setattr / delattr / exec / eval /
                                                                                        compile / __import__; __dict__ or
                                                                                        __globals__ -- and every USE whitelisted:
                                                                                        DOMAIN in `in' and as `" ".join's
                                                                                        argument, D_CLASS in `.get(' and `in'; the
                                                                                        checker's EFFECTIVE DOMAIN read by
                                                                                        importing it)
    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
             the answer a cell shows                                                    end), R1n (null), R3
             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
             whatever optional fields the answer carries                                null, both pads, the newline and NBSP
                                                                                        cells included), R1w (all 29 whitespace
                                                                                        cells, whole), R1e (a
                                                                                        record beside it), R1f (a refused
                                                                                        exemption first), R1o (a grade, a badge
                                                                                        and evidence all present), R1q (neither
                                                                                        date nor note)
             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells)
             the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
             or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
                                                                                        str.isspace() code points)
             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
             its labels                                                                 string), R2b (the fixture ledger, whose
                                                                                        pads and null count legacy)
             the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
             the style block naming the class                                          rules naming `legacy')
    Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
             refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
                                                                                        output whole, the entry named), W3 (rc 2),
             FIRST line, stderr included                                                W7 (rc 7, a two-line message on stderr:
                                                                                        the output whole), W8 (python absent: rc
                                                                                        127), W9 (EVERY status 2-255: the else
                                                                                        partition exhausted)
             the checker absent -> BAD                                                  W6
             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
    DISCLOSED, each with its reason:
      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
        (GPT-6 Astra, v4 pass: the two figures are different searches);
      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^'; the `[:10]' slice before the compare:
        equivalent, a string sharing the cutoff's first ten characters is never smaller than it; `repr' of a non-string date:
        equivalent to `str' for every JSON value;
      a missing or null NOTE hashed as "" (`d_notenone'): 0 of the 1,356 frozen answers has one, and 0 entries anywhere carry
        a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
      the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
        wording: display only (their rc 2 is pinned; an emptied reason passes every row -- `x_apparatusmsg', Fable 5.1, v5
        pass, measured);
      the page's CSS outside the two rules this landing adds (a rule hiding every glyph would be HEAD's CSS, not this diff);
      a change to the glyph sets by a mechanism C27 does not name (a helper module rebinding them after import, a C
        extension) is outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
        `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
        first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
      the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
        x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
        set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
        v5 pass, measured: `+ ("OK",)' at the use site 80/96);
      a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
        sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
        apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
      the Q2 section header: `say' is stubbed in the W block, and it is display only;
      the note-type scope of condition 2: "is it an answer" is `stage_tokens.is_answer', which tests membership on the untyped
        note -- a list or dict note holding a token as an element or a key is a NON-answer and is skipped, as the renderer
        also shows it (GPT-6 Astra, v5 pass, measured; K19's "nothing is skipped" was false); a list note holding no token is
        an answer and is refused (C21k); a bool note: True rc 2, False rc 1 (Astra, measured).
    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
    two-edit design mutant d_dfold2, killed by C25d.  Two kills the shipped ledger already supplies are ALSO rowed in isolation,
    so no pin rests on the ledger's composition alone: the `entries' default (98 of 912 shipped rows carry no `entries' key;
    C21j) and a latin-1 note encoding (34 frozen notes are non-ASCII, one beyond latin-1; C20b).

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
  v4 passes' findings):
    C1   shipped ledger, shipped baseline (md5 pin live): rc 0 and the summary line EXACTLY
    C2 / C2b  an answer ON / AFTER the cutoff with a valid glyph (positive)                       -> 0 / 0
    C2c / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
    C3   an answer ON the cutoff with "OK" (inclusive) -- its refusal line EXACTLY                  -> 1
    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
    C6   an UNDATED answer with "N/A" -- its refusal line EXACTLY (date "(none)", no ISO clause)    -> 1
    C7   an answer after the cutoff with NO `d`                                                     -> 0
    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
    C9   an identical copy of a frozen entry -- its refusal line EXACTLY                            -> 1
    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
    C11  the baseline emptied (override): every shipped off-domain answer named, the summary EXACTLY, the hint -> 1
    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after / far   -> 0 / 1 / 1 / 1,
         each with its summary line EXACTLY (on/after/far: within = baseline - 1)
    C12s a MATCHED identity dated "2026-10-17T12:00:00" (the ISO shape opens it)                    -> 1
    C13  an unreadable baseline (override)                                                          -> 2
    C14  a new answer with an explicit BLANK d                                                      -> 1
    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat, date, d) -> 1
    C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
    C17  a misshapen baseline (override; counts as strings)                                         -> 2
    C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
    C17c-g  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0  -> 2 each
    C17h-m  the same, each of the six string positions numeric in turn: row, note sha, phase, seat, date, d     -> 2 each
    C17n the same, a None date (`isinstance(v, (str, type(None)))' would pass it)                    -> 2
    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
         the date NAMED as not ISO                                                                  -> 1 / 1
    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback, its line EXACT
         with the d backslash-escaped                                                               -> 1
    C20b a new answer whose NOTE is non-ASCII ("café — ✓") -- rc 1, its line EXACT (the note's UTF-8 sha)  -> 1
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
    C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
    C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
    C23  a ledger that is not JSON                                                                  -> 2
    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
    C26  a new answer with an explicit "d": null                                                     -> 1
    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
    C27  DOMAIN and D_CLASS: ONE binding each and NO other way to change them -- an ast walk of every binding form and
         every use (whitelisted), and the checker's EFFECTIVE DOMAIN read by importing it -- each exactly ✓ ✕ ⏸ …
    C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
    C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
    C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
         one-digit day, a `/' for the first separator, for the second -- each in its fixture baseline, so only the shape
         decides                                                                                    -> 0 each
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
         "\n", "\xa0", null), the date, the note
    R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
    R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
    R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
    R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
    R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
         whitespace set exhausted
    R1n  an explicit "d": null renders legacy with the glyph "None", not …
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
         own count by exact membership, and its labels
    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
         a kill
    R4   the legend carries the legacy line EXACTLY
    R5   the page carries the two CSS rules the class adds, EXACTLY, and NO other rule in its style block names `legacy'
  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
  carry its BRANCH's own words):
    W1   the shipped ledger                    -> exactly "GOOD <the summary line>" and "FAILURES 0"
    W2   a new off-domain answer               -> BAD, its WHOLE output: the first line, every line of the checker's
         output indented, the counter
    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
    W7   a checker that exits 7 with a TWO-line message on STDERR -> exactly "BAD ... could not run (rc 7): <its FIRST line>"
         and "FAILURES 1"
    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
    W9   EVERY status 2-255, a stub exiting each in turn (254 runs)    -> each exactly "BAD ... could not run (rc N): <its
         first line>" and the counter 1 -- the `else' partition EXHAUSTED
"""
```

### 4b. the renderer FIXTURE -- the EXPECT table and the FX rows, verbatim

```python
SEATS = [s["id"] for s in L0["seats"]]
EXPECT = {   # seat -> (entry fields, class, glyph)
    "fable5": ({"d": "✓"}, "ok", "✓"),
    "opus5": ({"d": "OK"}, "legacy", "OK"),
    "codex": ({}, "pend", "…"),
    "agy": ({"d": ""}, "legacy", "?"),
    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", "∅"),
    "glm": ({"d": "✕"}, "bad", "✕"),
    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
}
assert set(EXPECT) == set(SEATS), SEATS
#  the legacy cell's WHOLE tooltip: the class line, the date, the note -- joined and escaped exactly as cell() does.  A prefix
#  check let "(not approval, not a seat failure)" return after the checked words (GPT-6 Astra and GLM 5.3, adjudication pass)
LEGACY_TIP = html.escape("legacy -- verdict unclassified: d = 'OK' is outside ✓ ✕ ⏸ …; read the note for the outcome"
                         " — 2026-10-16 — a renderer control", quote=True)
LEGEND_LINE = ('<span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside '
               '✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = '
               'an explicit blank)</span>')
REC_NOTE = st.NOTSEAT + " a record beside the answer"
REF_A = {"phase": "research", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": st.RE_READ + " refused re-read control"}
FX = copy.deepcopy(L0)
ents = []
for s in SEATS:
    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
    e.update(EXPECT[s][0])
    ents.append(e)
FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents},
              {"id": "ctlesc", "title": "escape control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "<b>&", "note": "escape control"}]},
              #  a whitespace-only `d` must show `?`, never an invisible glyph (0 such values in the ledger; Fable 5.1,
              #  adjudication pass, measured `{e(d) if d else "?"}` passing every v2 control)
              {"id": "ctlws", "title": "whitespace control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"},
                           #  a TAB-only d: `.strip(" ")` would keep it invisible (Grok 4.7, v3 pass)
                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"},
                           #  v5: a newline and an NBSP -- `.strip(" \t")' kept both invisible and passed all 72 v4
                           #  controls (Fable 5.1, Grok 4.7, v4 pass)
                           {"phase": "assess", "seat": "opus5", "date": "2026-10-16", "d": "\n", "note": "newline control"},
                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "\xa0", "note": "nbsp control"}]},
              #  v5: an explicit null d renders legacy with the glyph None -- a renderer that treats null as missing (…) or
              #  skips its class line passed all 72 v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
              {"id": "ctlnull", "title": "null control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": None, "note": "null control"}]},
              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"},
                           #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
              #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while 649 and 642 of the 670
              #  shipped legacy cells lost the class line (GPT-6 Astra, v5 pass)
              #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
              #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
              {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "d": "BARE"}]},
              {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
                            "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
#  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
#  `str.strip()' removes, and `.strip(" \t\n\xa0")' passed all 96 v5 controls but R3's presence pin (Fable 5.1, v5 pass)
WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
for i in range(0, len(WS), len(SEATS)):
    FX["rows"].append({"id": "ctlws%02d" % (i // len(SEATS)), "title": "whitespace set control row", "sev": "LOW", "state": "open",
                       "commits": "", "entries": [{"phase": "assess", "seat": SEATS[j], "date": "2026-10-16", "d": ch,
                                                   "note": "ws control U+%04X" % ord(ch)}
                                                  for j, ch in enumerate(WS[i:i + len(SEATS)])]})
fx_path = wjson("fx_render.json", FX)
```

### 4b2. C27 -- the ast walk and its use whitelists, verbatim (new in v6)

```python
def walk_name(path, name, use_ok):
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    probs = []
    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
           and n.targets[0].id == name]
    if len(stores) != 1 or len(top) != 1:
        probs.append("%d stores, %d module-level assignments" % (len(stores), len(top)))
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Del):
            probs.append("del")
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
            probs.append("global/nonlocal")
        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split(".")[0]) == name for a in n.names):
            probs.append("import alias")
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
            probs.append("def/class")
        elif isinstance(n, ast.ExceptHandler) and n.name == name:
            probs.append("except name")
        elif isinstance(n, ast.arg) and n.arg == name:
            probs.append("parameter")
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == name:
            probs.append("match name")
        elif isinstance(n, ast.Attribute) and n.attr == name and not isinstance(n.ctx, ast.Load):
            probs.append("attribute store")
        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load) and isinstance(n.slice, ast.Constant)
              and n.slice.value == name):
            probs.append("subscript store keyed by the name")
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
            probs.append("call to " + n.func.id)
        elif isinstance(n, ast.Attribute) and n.attr in ("__dict__", "__globals__"):
            probs.append(n.attr)
        elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
            probs.append("a use at line %d" % n.lineno)
    return (ast.literal_eval(top[0].value) if len(top) == 1 else None), probs


def in_compare(n, parent):
    p = parent.get(n)
    return (isinstance(p, ast.Compare) and n in p.comparators
            and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))


def dom_use(n, parent):
    p = parent.get(n)
    return in_compare(n, parent) or (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
                                     and p.func.attr == "join" and isinstance(p.func.value, ast.Constant))


def dcls_use(n, parent):
    p = parent.get(n)
    return in_compare(n, parent) or (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
                                     and parent.get(p).func is p)


dom, dprobs = walk_name(CHECKER, "DOMAIN", dom_use)
dcls, cprobs = walk_name(RENDER, "D_CLASS", dcls_use)
r_imp = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import check_entry_domain as c; "
                        "print(ascii(c.DOMAIN))", os.path.dirname(DEFAULT_CHECKER)], capture_output=True, text=True)
try:
    eff = ast.literal_eval(r_imp.stdout.strip()) if r_imp.returncode == 0 else None
except (ValueError, SyntaxError):
    eff = None
four = ("✓", "✕", "⏸", "…")
say("C27 ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ …",
```

### 4c. `RECEIPT_v6_on_staged_v5.txt`, whole

```
# controls md5 e9b811eeaf9e221b29e1c932b4a7014c
# dashokclass controls (v6) -- checker a6ff64d8 | renderer 516df040 | precommit 769f261f | baseline 06a3ffc6
C1   shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY, and the only line ok  rc 0: 1 lines; entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
C2   ON the cutoff, a valid glyph (positive)                                      ok  rc 0 (want 0)
C2b  AFTER the cutoff, a valid glyph (positive)                                   ok  rc 0 (want 0)
C3   ON the cutoff, d OK (inclusive)                                              ok  rc 1 (want 1)
C4   AFTER the cutoff, d OK                                                       ok  rc 1 (want 1)
C5   a new answer BEFORE the cutoff, d OK (back-dated)                            ok  rc 1 (want 1)
C6   undated, d N/A                                                               ok  rc 1 (want 1)
C7   after the cutoff, NO d                                                       ok  rc 0 (want 0)
C8   a HELD marker after the cutoff, d HELD                                       ok  rc 0 (want 0)
C14  a new answer with an explicit BLANK d                                        ok  rc 1 (want 1)
C19a a new answer dated "10/18/2026", d OK                                        ok  rc 1 (want 1)
C19b a new answer with a NUMERIC date, d OK                                       ok  rc 1 (want 1)
C20  a new answer with a non-ASCII d (cp1252 stdout, no traceback)                ok  rc 1 (want 1)
C26  a new answer with an explicit null d                                         ok  rc 1 (want 1)
C26b a new answer whose d is a LIST                                               ok  rc 1 (want 1)
C28  a new answer BEFORE the cutoff with a padded glyph ' ✓'                      ok  rc 1 (want 1)
C28b a new answer BEFORE the cutoff with a glyph padded at its END '✓ '           ok  rc 1 (want 1)
C20b a new answer whose note is non-ASCII                                         ok  rc 1 (want 1)
C29  a new answer with no phase and no seat                                       ok  rc 1 (want 1)
C21k a new answer whose note is a list holding no token                           ok  rc 1 (want 1)
C2c  AFTER the cutoff, d ⏸, in a ledger holding only it (positive)                ok  rc 0
C2d  AFTER the cutoff, d …, in a ledger holding only it (positive)                ok  rc 0
C24  a non-answer RECORD (NOTSEAT) after the cutoff, d OK, in a ledger holding only it ok  rc 0
C9   an identical copy of a frozen entry (alphactxfail assess codex 2026-09-08 'y'): its refusal line EXACTLY ok  rc 1; ["OFF-DOMAIN ANSWER  row alphactxfail  phase assess  seat codex  date 2026-09-08  d 'y'  note 366d4c0c34110db4 -- beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"]
C10  a frozen entry rewritten to a glyph                                          ok  rc 0
C15  REFILL: the converted entry's (row, phase, seat, date, d) reused             ok  rc 1
C16  a frozen entry's note edited, d left off-domain                              ok  rc 1
C22  a frozen entry's ev edited, outside the six fields (positive)                ok  rc 0
C25a a frozen entry's date, suffixed T12:00:00                                    ok  rc 1
C25b a frozen entry's date, a trailing space                                      ok  rc 1
C25c a frozen entry's d, a trailing space                                         ok  rc 1
C25d a frozen entry's d, its case swapped                                         ok  rc 1
C25e a frozen entry's note, a trailing space                                      ok  rc 1
C25f a frozen entry's note, its case swapped                                      ok  rc 1
C25g a frozen entry's seat, a trailing space                                      ok  rc 1
C25h a frozen entry's seat, upper-cased                                           ok  rc 1
C25i a frozen entry's phase, a trailing space                                     ok  rc 1
C25j a frozen entry's phase, upper-cased                                          ok  rc 1
C25k a frozen entry moved to another row (d1)                                     ok  rc 1
C25l a frozen entry moved to a row whose id has a TRAILING space                  ok  rc 1
C25m a frozen entry's date with a LEADING space                                   ok  rc 1
C25n a frozen entry's d with a LEADING space                                      ok  rc 1
C25o a frozen entry's note with a LEADING space                                   ok  rc 1
C25p a frozen entry's seat with a LEADING space                                   ok  rc 1
C25q a frozen entry's phase with a LEADING space                                  ok  rc 1
C25r a frozen entry moved to a row whose id has a LEADING space                   ok  rc 1
C11  baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint WHOLE ok  rc 1, 1356 of 1356 named, 1358 lines; summary ok; hint ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-16 (before), the summary EXACTLY ok  rc 0 (want 0); summary ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-17 (on), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-18 (after), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12  cutoff isolated: a FROZEN identity dated 2027-01-01 (far), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00                 ok  rc 1 (want 1)
C12w the ISO shape's year: a FROZEN identity dated 99999-10-18 is not read as a date ok  rc 0 (want 0)
C12w the ISO shape's month: a FROZEN identity dated 2026-9-17 is not read as a date ok  rc 0 (want 0)
C12w the ISO shape's day: a FROZEN identity dated 2026-10-9 is not read as a date ok  rc 0 (want 0)
C12w the ISO shape's sep1: a FROZEN identity dated 2026/10-18 is not read as a date ok  rc 0 (want 0)
C12w the ISO shape's sep2: a FROZEN identity dated 2026-10/18 is not read as a date ok  rc 0 (want 0)
C13  an unreadable baseline                                                       ok  rc 2
C27  ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ … ok  DOMAIN ('✓', '✕', '⏸', '…')  | effective ('✓', '✕', '⏸', '…') | D_CLASS keys ['…', '⏸', '✓', '✕'] 
C17  a misshapen baseline (counts as strings)                                     ok  rc 2
C17b a key split across two baseline rows sums (alphaswpctxreg review grok 2026-09-08 'y' x2) ok  rc 0
C17c a misshapen baseline row: eight fields (override)                            ok  rc 2
C17d a misshapen baseline row: a count of true (override)                         ok  rc 2
C17e a misshapen baseline row: a count of -1 (override)                           ok  rc 2
C17f a misshapen baseline row: a count of 0 (override)                            ok  rc 2
C17g a misshapen baseline row: a count of 1.0 (override)                          ok  rc 2
C17h a misshapen baseline row: a numeric first field (override)                   ok  rc 2
C17i a misshapen baseline row: a numeric note sha (override)                      ok  rc 2
C17j a misshapen baseline row: a numeric phase (override)                         ok  rc 2
C17k a misshapen baseline row: a numeric seat (override)                          ok  rc 2
C17l a misshapen baseline row: a numeric date (override)                          ok  rc 2
C17m a misshapen baseline row: a numeric d (override)                             ok  rc 2
C17n a misshapen baseline row: a None date (override)                             ok  rc 2
C18  md5 pin: one baseline line changed -> 2, unchanged -> 0                      ok  changed rc 2, unchanged rc 0
C18b md5 pin: the baseline checked out with CRLF line endings -> 0                ok  rc 0
C21a a misshapen ledger: {"rows": null}                                           ok  rc 2
C21b a misshapen ledger: a row that is not an object                              ok  rc 2
C21c a misshapen ledger: a list, not an object                                    ok  rc 2
C21d a misshapen ledger: {"rows": {}}                                             ok  rc 2
C21e a misshapen ledger: an entry that is a string                                ok  rc 2
C21f a misshapen ledger: entries that are an object                               ok  rc 2
C21i a misshapen ledger: no rows key -- {}                                        ok  rc 2
C21i a misshapen ledger: no rows key -- {"seats": []}                             ok  rc 2
C21g a misshapen baseline: an object, not a list (override)                       ok  rc 2
C21j a row with no entries key beside a valid one                                 ok  rc 0
C21h an entry whose note is a number (it raises inside is_answer)                 ok  rc 2
C23  an unreadable ledger (not JSON)                                              ok  rc 2
R1   fixture row: class, glyph and the legacy tooltip EXACTLY, per seat           ok  9 cells; mismatches []; legacy tip exact
R1g  every simple legacy cell's WHOLE tooltip, the class line for ITS d           ok  44 legacy cells; no exact tooltip for: []
R1h  a ✓ padded at either end renders legacy, its glyph text exactly as written   ok  cells ('legacy', ' ✓') ('legacy', '✓ ')
R1o  a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first ok  cell ('legacy', 'OK'); tooltip exact
R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry no class line: the date and the note alone ok  wrong: []
R1q  a legacy answer with neither date nor note: its tooltip is the class line alone ok  cells 1: ['legacy -- verdict unclassified: d = &#x27;BARE&#x27; is outside ✓ ✕ ⏸ …; read th']
R1w  every str.isspace() code point alone as d (29) shows ? and renders legacy, each with its WHOLE tooltip ok  29 cells of 29; wrong: []
R1e  an answer with a record beside it: its WHOLE tooltip                         ok  cells 1; tooltip exact
R1n  an explicit null d renders legacy with the glyph None                        ok  cell ('legacy', 'None')
R1f  a refused exemption's line first, then the class line, exactly               ok  refusals 1; cells 1; tooltip exact
R1b  an escapable d renders escaped                                               ok  escape cell ('legacy', '&lt;b&gt;&amp;')
R1d  a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?         ok  whitespace cells [('legacy', '?'), ('legacy', '?'), ('legacy', '?'), ('legacy', '?')]
R1c  the fixture page says neither 'not approval' nor 'not a seat failure'        ok  render ok; found none
R4   the legend carries the legacy line EXACTLY                                   ok  legend found
R5   the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it ok  missing []; legacy rules 2 ['td.c.legacy { outline:1px dashed var(--l', '.c.legacy .g { color:var(--muted); font-']
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label) ok  before {'bad': 17, 'hold': 53, 'none': 29472, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 53, 'legacy': 670, 'none': 29472, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all' | ledger 5177 entries, 1397 off-domain
R2b  the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy) ok  strip '2✓ 1✕ 1⏸ 2… 46 legacy · 52 in all', want '2✓ 1✕ 1⏸ 2… 46 legacy · 52 in all'
R3   MUTANT ok renders and fails its check                                        ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT pend renders and fails its check                                      ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT noescape renders and fails its check                                  ok  escape cell ('legacy', '<b>&')
W1   Q2 on the shipped ledger                                                     ok  GOOD entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baselin | failures 0
W2   Q2 with a new off-domain answer                                              ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W3   Q2 with the baseline absent (rc 2 path)                                      ok  BAD check_entry_domain.py could not run (rc 2): APPARATUS FAIL: baseline unreadable or mis | failures 1
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W5   Q2 ignores an exported GXLEDGER naming a clean ledger                        ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W6   Q2 with the checker absent                                                   ok  BAD check_entry_domain.py MISSING -- the entry-domain check proved nothing | failures 1
W7   Q2 with a checker that exits 7, its message on stderr                        ok  BAD check_entry_domain.py could not run (rc 7): STUB FIRST LINE | failures 1
W8   Q2 with python absent from PATH (rc 127)                                     ok  BAD check_entry_domain.py could not run (rc 127): env: 'python': No such file or directory | failures 1
W9   Q2 with EVERY status 2-255 (254 runs of one stub): each exactly BAD 'could not run (rc N)' with its first line, the counter 1 ok  wrong at: []
DASHOKCLASS CONTROLS: 116/116 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4d. `KILLTABLE_v6_staged.txt` (the mutants are `run_mutants_v6.py`'s MUTANTS; the v6 additions follow)

```
# controls md5 e9b811eeaf9e221b29e1c932b4a7014c
# driver md5 05d1a98bb54f70b4eb7f9abdb475ca80
# dashokclass kill table (v6) -- controls run_controls_v6.run-045605.py, 2 at a time
BASE          116/116
d_cutoff18      106/116 killed by: C1 C11 C12 C12s C20 C3 W1                               [C12]
d_cutgt         113/116 killed by: C12 C12s C3                                             [C12]
d_nodate        110/116 killed by: C12 C12s C20 C3                                         [C12]
d_lexdate       110/116 killed by: C12w C19b                                               [C19b]
d_noreason      114/116 killed by: C19a C19b                                               [C19a C19b]
d_blank         107/116 killed by: C1 C11 C12 C14 C26 W1                                   [C14]
d_domnohold     85/116  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C27 C29 C2b C2c C3 C6 C7 C8 C9 W1 [C2c]
d_domnopend     85/116  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C27 C29 C2b C2d C3 C6 C7 C8 C9 W1 [C2d]
d_dupplus1      79/116  killed by: C11 C14 C15 C16 C19a C19b C20b C21k C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C5 C6 C9 W2 W4 W5 [C5 C9]
d_nonote        88/116  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C2b C3 C6 C7 C8 C9 W1 [C1]
d_nonote2       103/116 killed by: C15 C16 C19a C20 C20b C21k C25e C25f C25o C29 C3 C6 C9  [C15 C16]
d_lastwins      115/116 killed by: C17b                                                    [C17b]
d_ledger1       115/116 killed by: C21h                                                    [C21h]
d_nomd5         115/116 killed by: C18                                                     [C18]
d_pinoverride   103/116 killed by: C11 C12 C12s C12w C17b C18                              [C18]
d_crlfpin       115/116 killed by: C18b                                                    [C18b]
d_noreconf      100/116 killed by: C11 C14 C19a C19b C20 C20b C21k C26 C26b C28 C28b C29 C3 C4 C5 C6 [C20]
d_notenone      116/116 escapes (as recorded)                                              [UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note]
r_nolegend      115/116 killed by: R4                                                      [R4]
r_tipclause     108/116 killed by: R1 R1c R1e R1f R1g R1o R1q R1w                          [R1 R1c]
r_tiptail       109/116 killed by: R1 R1e R1f R1g R1o R1q R1w                              [R1]
r_ok            102/116 killed by: R1 R1b R1d R1e R1f R1g R1h R1n R1o R1q R1w R2 R3        [R1]
r_pend          102/116 killed by: R1 R1b R1d R1e R1f R1g R1h R1n R1o R1q R1w R2 R3        [R1]
r_noescape      114/116 killed by: R1b R3                                                  [R1b]
r_wsblank       112/116 killed by: R1d R1n R1w R3                                          [R1d]
r_strip         114/116 killed by: R2 R2b                                                  [R2]
w_envkeep       114/116 killed by: W4 W5                                                   [W4 W5]
w_ledgerkeep    115/116 killed by: W5                                                      [W5]
w_collapse      112/116 killed by: W3 W7 W8 W9                                             [W3]
w_rc7           111/116 killed by: W2 W4 W5 W7 W9                                          [W2]
w_msg           113/116 killed by: W2 W4 W5                                                [W2]
w_subshell      113/116 killed by: W2 W4 W5                                                [W2]
d_date10        113/116 killed by: C12w C25a C25b                                          [C25a C25b]
d_dstrip        114/116 killed by: C25c C25n                                               [C25c]
d_dfold         88/116  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C2b C3 C6 C7 C8 C9 W1 [C1]
d_dfold2        109/116 killed by: C19a C20b C21k C25d C29 C3 C6                           [C25d]
d_notestrip     88/116  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C2b C3 C6 C7 C8 C9 W1 [C1]
d_notefold      88/116  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C2b C3 C6 C7 C8 C9 W1 [C1]
d_seatstrip     114/116 killed by: C25g C25p                                               [C25g]
d_seatfold      115/116 killed by: C25h                                                    [C25h]
d_phasestrip    114/116 killed by: C25i C25q                                               [C25i]
d_phasefold     115/116 killed by: C25j                                                    [C25j]
d_shaperows     115/116 killed by: C21d                                                    [C21d]
d_shapeents     115/116 killed by: C21f                                                    [C21f]
d_shapeentry    115/116 killed by: C21e                                                    [C21e]
d_noshape       111/116 killed by: C21d C21e C21f C21i                                     [C21d C21e C21f]
d_basedict      115/116 killed by: C21g                                                    [C21g]
r_norecord      115/116 killed by: R1e                                                     [R1e]
r_okonly        113/116 killed by: R1g R1q R1w                                             [R1g]
r_stripok       114/116 killed by: R2 R2b                                                  [R2]
r_refusallast   115/116 killed by: R1f                                                     [R1f]
w_nochecker     115/116 killed by: W6                                                      [W6]
d_unread0       115/116 killed by: C23                                                     [C23]
d_summary       112/116 killed by: C11 C12                                                 [C11]
r_tipokonly     113/116 killed by: R1g R1q R1w                                             [R1g]
r_tipnonblank   114/116 killed by: R1g R1w                                                 [R1g]
r_clsstrip      112/116 killed by: R1g R1h R3                                              [R1h]
d_isheld        86/116  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C24 C29 C2b C3 C6 C7 C8 C9 W1 [C24]
d_nulld         115/116 killed by: C26                                                     [C26]
d_nohint        115/116 killed by: C11                                                     [C11]
d_domzxq        114/116 killed by: C11 C27                                                 [C27]
r_dclasszxq     115/116 killed by: C27                                                     [C27]
d_cut2days      115/116 killed by: C12                                                     [C12]
d_baselen       110/116 killed by: C1 C12 W1                                               [C1]
w_nosed         115/116 killed by: W2                                                      [W2]
r_wsspace       113/116 killed by: R1d R1w R3                                              [R1d]
d_domredef      114/116 killed by: C11 C27                                                 [C27]
r_dclassredef   115/116 killed by: C27                                                     [C27]
d_dompad        114/116 killed by: C28 C28b                                                [C28]
d_rowstrip      114/116 killed by: C25l C25r                                               [C25l C25r]
d_rowrstrip     115/116 killed by: C25l                                                    [C25l]
d_rowlstrip     115/116 killed by: C25r                                                    [C25r]
d_datelstrip    115/116 killed by: C25m                                                    [C25m]
d_dlstrip       115/116 killed by: C25n                                                    [C25n]
d_notelstrip    115/116 killed by: C25o                                                    [C25o]
d_seatlstrip    115/116 killed by: C25p                                                    [C25p]
d_phaselstrip   115/116 killed by: C25q                                                    [C25q]
d_cutreason     114/116 killed by: C20 C3                                                  [C3]
d_ceilreason    110/116 killed by: C19a C20b C21k C29 C6 C9                                [C6 C9]
d_rowphaseswap  108/116 killed by: C19a C20 C20b C21k C29 C3 C6 C9                         [C9]
d_basewithin    113/116 killed by: C12                                                     [C12]
d_isodollar     115/116 killed by: C12s                                                    [C12s]
d_len7ge        115/116 killed by: C17c                                                    [C17c]
d_boolcount     115/116 killed by: C17d                                                    [C17d]
d_negcount      115/116 killed by: C17e                                                    [C17e]
d_zerocount     115/116 killed by: C17f                                                    [C17f]
d_floatcount    115/116 killed by: C17g                                                    [C17g]
d_str1          115/116 killed by: C17h                                                    [C17h]
d_str5          115/116 killed by: C17i                                                    [C17i]
d_isosearch     116/116 escapes (as recorded)                                              [UNPINNED: equivalent -- the ISO pattern is anchored with ^, so search and match agree on every string]
d_nostr         115/116 killed by: C26b                                                    [C26b]
d_hintundated   115/116 killed by: C6                                                      [C6]
d_datenone      115/116 killed by: C6                                                      [C6]
d_cutoffmsg     109/116 killed by: C1 C11 C12 W1                                           [C1 C11 C12]
d_rowsabsent    114/116 killed by: C21i                                                    [C21i]
r_sumstrip      115/116 killed by: R2b                                                     [R2b]
r_tipnorecord   115/116 killed by: R1e                                                     [R1e]
r_tipnotnull    115/116 killed by: R1g                                                     [R1g]
r_nullpend      114/116 killed by: R1g R1n                                                 [R1n R1g]
r_striplabel    114/116 killed by: R2 R2b                                                  [R2]
r_wsset         113/116 killed by: R1d R1w R3                                              [R1d]
r_css0          115/116 killed by: R5                                                      [R5]
r_cssoutline    115/116 killed by: R5                                                      [R5]
w_elif2         113/116 killed by: W7 W8 W9                                                [W7 W8]
w_no2to1        114/116 killed by: W7 W9                                                   [W7]
d_domglobals    114/116 killed by: C11 C27                                                 [C27]
d_domglobalsaug 114/116 killed by: C11 C27                                                 [C27]
d_domexec       114/116 killed by: C11 C27                                                 [C27]
d_domsetattr    114/116 killed by: C11 C27                                                 [C27]
d_domarg        115/116 killed by: C27                                                     [C27]
r_dclassglobals 115/116 killed by: C27                                                     [C27]
r_dclassupdate  115/116 killed by: C27                                                     [C27]
r_dclasssetitem 115/116 killed by: C27                                                     [C27]
d_dompadr       115/116 killed by: C28b                                                    [C28b]
r_clsrstrip     112/116 killed by: R1g R1h R3                                              [R1h]
d_strskip1      115/116 killed by: C17j                                                    [C17j]
d_strskip2      115/116 killed by: C17k                                                    [C17k]
d_strskip3      114/116 killed by: C17l C17n                                               [C17l]
d_strskip4      115/116 killed by: C17m                                                    [C17m]
d_isowidthy     115/116 killed by: C12w                                                    [C12w]
d_isowidthm     115/116 killed by: C12w                                                    [C12w]
d_isowidthd     115/116 killed by: C12w                                                    [C12w]
d_isosep1       115/116 killed by: C12w                                                    [C12w]
d_isosep2       115/116 killed by: C12w                                                    [C12w]
d_hinttext      115/116 killed by: C11                                                     [C11]
d_hintalways    115/116 killed by: C1                                                      [C1]
d_reconfreplace 114/116 killed by: C11 C20                                                 [C20]
d_notelatin1    55/116  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C20b]
d_notenostr     115/116 killed by: C21k                                                    [C21k]
d_entriesdef1   54/116  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21j C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C21j]
d_entriesdef2   54/116  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21j C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C21j]
d_phasenone     115/116 killed by: C29                                                     [C29]
d_seatnone      115/116 killed by: C29                                                     [C29]
r_tipinsertm2   115/116 killed by: R1o                                                     [R1o]
r_tipnoev       115/116 killed by: R1o                                                     [R1o]
r_escstrip      115/116 killed by: R1h                                                     [R1h]
r_cssoverride   115/116 killed by: R5                                                      [R5]
w_tail1         115/116 killed by: W7                                                      [W7]
r_tippend       115/116 killed by: R1p                                                     [R1p]
r_tipnotok      115/116 killed by: R1p                                                     [R1p]
r_tipempty      115/116 killed by: R1q                                                     [R1q]
r_glyphstrip    114/116 killed by: R1h R3                                                  [R1h]
r_wsset4        114/116 killed by: R1w R3                                                  [R1w]
r_sumcrash      95/116  killed by: C27 R1 R1b R1c R1d R1e R1f R1g R1h R1n R1o R1p R1q R1w R2 R2b R3 R4 R5 [C27 R2]
d_domusesite    115/116 killed by: C27                                                     [C27]
d_strnone       115/116 killed by: C17n                                                    [C17n]
d_hinttail      115/116 killed by: C11                                                     [C11]
d_isodigits     114/116 killed by: C12w                                                    [C12w]
w_q2paren       115/116 killed by: W2                                                      [W2]
r_tipnows       114/116 killed by: R1g R1w                                                 [R1g]
r_tipnows2      115/116 killed by: R1w                                                     [R1w]
r_tipall        115/116 killed by: R1p                                                     [R1p]
d_hintjoin      115/116 killed by: C11                                                     [C11]
d_domsysmod     114/116 killed by: C11 C27                                                 [C27]
d_isotrunc      115/116 killed by: C12w                                                    [C12w]
w_elifne3       115/116 killed by: W9                                                      [W9]
w_named         115/116 killed by: W2                                                      [W2]
KILL TABLE: 157/157 as recorded
DASHOKCLASS_MUTANTS_DONE
```

```python
    #  v6 -- the v5 pass's survivors (GLM 5.3 and GPT-6 Astra measured) and each decision's GENERATING SET
    ("d_domglobals", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                  'globals()["DOMAIN"] = DOMAIN + ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domglobalsaug", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                     'globals()["DOMAIN"] += ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domexec", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                               'exec(\'DOMAIN = DOMAIN + ("ZXQ",)\')\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("d_domsetattr", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                  'setattr(sys.modules[__name__], "DOMAIN", DOMAIN + ("ZXQ",))\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_domarg", "checker", [("def off_domain_answers(ledger):", 'def off_domain_answers(ledger, DOMAIN=DOMAIN + ("ZXQ",)):')], ["C27"]),
    ("r_dclassglobals", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nglobals()["D_CLASS"] = dict(D_CLASS, ZXQ="ok")')],
     ["C27"]),
    ("r_dclassupdate", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                   'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS.update(ZXQ="ok")')], ["C27"]),
    ("r_dclasssetitem", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS["ZXQ"] = "ok"')], ["C27"]),
    ("d_dompadr", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'str(x["d"]).rstrip() in DOMAIN or not st.is_answer(x):')],
     ["C28b"]),
    ("r_clsrstrip", "render", [("cls = D_CLASS.get(d, LEGACY)", "cls = D_CLASS.get(str(d).rstrip(), LEGACY)")], ["R1h"]),
    ("d_strskip1", "checker", [("for v in k[:6])", "for v in k[:1] + k[2:6])")], ["C17j"]),
    ("d_strskip2", "checker", [("for v in k[:6])", "for v in k[:2] + k[3:6])")], ["C17k"]),
    ("d_strskip3", "checker", [("for v in k[:6])", "for v in k[:3] + k[4:6])")], ["C17l"]),
    ("d_strskip4", "checker", [("for v in k[:6])", "for v in k[:4] + k[5:6])")], ["C17m"]),
    ("d_isowidthy", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4,5}-\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isowidthm", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{1,2}-\\d{2}")')], ["C12w"]),
    ("d_isowidthd", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{1,2}")')], ["C12w"]),
    ("d_isosep1", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}.\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isosep2", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}.\\d{2}")')], ["C12w"]),
    ("d_hinttext", "checker", [("; a non-answer record is exempt", "; all records need classification")], ["C11"]),
    ("d_hintalways", "checker", [('    if bad:\n        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"\n'
                                  '              % " ".join(DOMAIN))\n        return 1\n',
                                  '    print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"\n'
                                  '          % " ".join(DOMAIN))\n    if bad:\n        return 1\n')], ["C1"]),
    ("d_reconfreplace", "checker", [('reconfigure(errors="backslashreplace")', 'reconfigure(errors="replace")')], ["C20"]),
    ("d_notelatin1", "checker", [('str(x.get("note") or "").encode("utf-8")', 'str(x.get("note") or "").encode("latin-1")')], ["C20b"]),
    ("d_notenostr", "checker", [('str(x.get("note") or "").encode("utf-8")', '(x.get("note") or "").encode("utf-8")')], ["C21k"]),
    ("d_entriesdef1", "checker", [('        ents = r.get("entries", [])', '        ents = r.get("entries")')], ["C21j"]),
    ("d_entriesdef2", "checker", [('        for x in r.get("entries", []):', '        for x in r.get("entries"):')], ["C21j"]),
    ("d_phasenone", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase"))')], ["C29"]),
    ("d_seatnone", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat"))')], ["C29"]),
    ("r_tipinsertm2", "render", [('tip.insert(0, "legacy -- verdict unclassified:', 'tip.insert(-2, "legacy -- verdict unclassified:')],
     ["R1o"]),
    ("r_tipnoev", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and not ent.get("ev"):\n')], ["R1o"]),
    ("r_escstrip", "render", [("e = lambda t: html.escape(str(t), quote=True)", "e = lambda t: html.escape(str(t).strip(), quote=True)")],
     ["R1h"]),
    ("r_cssoverride", "render", [(".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}",
                                  ".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}\n.c.legacy .g {{ font-size:0; }}")],
     ["R5"]),
    ("w_tail1", "precommit", [("could not run (rc $_cedrc): $(printf '%s\\n' \"$_ced\" | head -1)\"",
                               "could not run (rc $_cedrc): $(printf '%s\\n' \"$_ced\" | tail -1)\"")], ["W7"]),
    #  v6 -- Fable 5.1's v5-pass sweep (`extra_mutants_v5*.py'), each escape rebuilt here verbatim
    ("r_tippend", "render", [("    if cls == LEGACY:\n", '    if cls in (LEGACY, "pend"):\n')], ["R1p"]),
    ("r_tipnotok", "render", [("    if cls == LEGACY:\n", '    if cls != "ok":\n')], ["R1p"]),
    ("r_tipempty", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and tip:\n")], ["R1q"]),
    ("r_glyphstrip", "render", [('{e(d) if str(d).strip() else "?"}', '{e(str(d).strip()) if str(d).strip() else "?"}')], ["R1h"]),
    ("r_wsset4", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" " + chr(9) + chr(10) + chr(160)) else "?"}')],
     ["R1w"]),
    ("r_sumcrash", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                               'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nD_CLASS["OK"] = "ok"')], ["C27", "R2"]),
    ("d_domusesite", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'x["d"] in DOMAIN + ("ZXQ",) or not st.is_answer(x):')],
     ["C27"]),
    ("d_strnone", "checker", [("all(isinstance(v, str) for v in k[:6])", "all(isinstance(v, (str, type(None))) for v in k[:6])")],
     ["C17n"]),
    ("d_hinttail", "checker", [(' (or omit `d`, which renders as …); a non-answer record is exempt"', '"')], ["C11"]),
    ("d_isodigits", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{1,2}-\\d{1,2}")')], ["C12w"]),
    ("w_q2paren", "precommit", [('ceiling (a new one, a copy, or an old one edited):"', 'ceiling:"')], ["W2"]),
    #  v6 -- Grok 4.7's v5-pass survivors, each rebuilt here verbatim
    ("r_tipnows", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and d not in ("\\n", "\\xa0"):\n')], ["R1g"]),
    ("r_tipnows2", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and d != "\\x0b":\n')], ["R1w"]),
    ("r_tipall", "render", [("    if cls == LEGACY:\n", "    if cls:\n")], ["R1p"]),
    ("d_hintjoin", "checker", [('% " ".join(DOMAIN))', '% "ZZZ")')], ["C11"]),
    ("d_domsysmod", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                 'sys.modules[__name__].DOMAIN = DOMAIN + ("ZXQ",)\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_isotrunc", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-")')], ["C12w"]),
    ("w_elifne3", "precommit", [('\telse\n\t\tbad "check_entry_domain.py could not run',
                                 '\telif [ $_cedrc -ne 3 ]; then\n\t\tbad "check_entry_domain.py could not run')], ["W9"]),
    ("w_named", "precommit", [("\t\tprintf '%s\\n' \"$_ced\" | sed 's/^/          /'\n",
                               "\t\tprintf '%s\\n' \"OFF-DOMAIN ANSWER  row redacted\"\n")], ["W2"]),
]
```

### 4e. `DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt` (`dashmissingd_census.py` on HEAD's ledger)

```
entries: 5177 | answers with no d: 1561 (by month: 2026-08 174, 2026-09 1244, 2026-10 143; the latest dated 2026-10-16) | of those, the note names a non-answer: 300
displayed answer cells: 2953 | whose latest answer has no d (rendered as the seat-failure glyph): 814 | of those, the note names no non-answer (an answer shown as a failure, by the keyword screen): 682
NOT-FIRED screen /not[ -]fired|roster/i over every entry's note: 222 entries | untokened (ANSWERS by stage_tokens.is_answer, so section H counts each as a recorded seat): 200 | of those with no d (each renders the seat-failure glyph): 87
DASHMISSINGD_CENSUS_DONE
```

## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A.

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2 (V1-V30): is my disposition right, AND is the fix
   right -- does the named row go red under the named mutant for the reason named?  Be harder on the ones you raised.
2. **The enumeration.**  For each decision in the CONTRACT, does a row now stand on every member of its generating set and on
   its complement?  Is any decision of the staged checker, the renderer change or the Q2 block missing?  Name every decision
   you checked.
3. **The kill table and the floor.**  Is any mutant killed for a reason OTHER than the one its line names?  Is there a
   one-edit mutant of the staged files, NOT in the table, that passes all 115 controls and breaks a ruled property or a line
   of the CONTRACT?  **Grade each you find: a floor breach (clauses a-d) or clause-(e) contract debt, and say why.**  If you
   find none, name the shapes you swept (a zero needs its denominator).
4. **The records (section 5).**  Is that text true of what ships?  Name any sentence that is false.
5. **Which of my dispositions is wrong?**  Name the count you checked.
6. **Does the chain close here?**  If your answer to 3 is zero floor breaches, say so in one line with its denominator.

Label each claim MEASURED (you ran it), READ (you opened the file) or REASONED.  Write nothing to any project tree.
