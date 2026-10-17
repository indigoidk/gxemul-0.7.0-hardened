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

**Liveness:** open your answer with the token `GROK_DASHOKV6_20261017` on its own line, then your verdict line.

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

## 4. The repair: the controls, v5 -> v6

### 4a. `run_controls_v5.py` -> `run_controls_v6.py` (459 changed lines)

```diff
--- run_controls_v5.py
+++ run_controls_v6.py
@@ -1,66 +1,134 @@
 #!/usr/bin/env python3
-"""Controls for `dashokclass` (2026-10-17, v5 after the v4 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
+"""Controls for `dashokclass` (2026-10-17, v6 after the v5 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
 ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
 ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
-the three files under test (run_mutants_v5.py and the staged runs use them); the defaults are the tree's.
+the three files under test (run_mutants_v6.py and the staged runs use them); the defaults are the tree's.
 
-  THE CONTRACT (v5) -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7; GLM 5.3 read the packet) measured 21 one-edit mutants
-  passing all 72 v4 controls, 15 of them at decisions v4 listed as pinned.  They share one shape (Fable 5.1): each pin tested
-  ONE edge of its decision -- the trailing end of a key field, the first literal line, a number but not its label, a substring
-  but not the whole tooltip, one branch of three.  So v5 rows the DUAL edge of every pin: for each decision below, the edit its
-  v4 pin would not see.  The decisions are the checker's, the renderer's and Q2's, read from the three files.
-    checker  ledger shape: an object, `rows' PRESENT and a list, row objects, entries   C21a-f, C21i (rows absent: {} and
-             lists, entry objects                                                       {"seats": []}); C23 (not JSON)
+  THE CONTRACT (v6) -- the v4 pass found pins that tested ONE edge of a decision, and v5 rowed the dual edge.  The v5 pass
+  (GPT-6 Astra and Fable 5.1 measured, GLM 5.3 reasoned, Grok 4.7 traced) found the next layer on two axes.  A v5 pin covered
+  PART of its decision's GENERATING SET -- the leading pad but not the trailing one, two of the baseline row's six string
+  positions, the ISO shape's anchor but not its widths or separators, the glyph sets' Name stores while `globals()' and a dict
+  mutation changed them, the hint's prefix, a tooltip whose fixture held no optional field, a CSS rule's presence but not the
+  absence of an overriding one, the apparatus branch's first line on one-line output, four whitespace code points of 29, the
+  newline and NBSP cells' class but not their tooltips, Q2's `else' at three of its 254 statuses, the named entry by a prefix
+  of W2's output.  And a pin
+  asserting a property of the SELECTED set said nothing about its COMPLEMENT (Fable 5.1) -- every legacy cell has the class
+  line but not ONLY legacy cells, the padded cell's class but not its text, the set where it is DEFINED but not where it is
+  USED.  So v6 enumerates each decision's generating set -- every operand position, both ends, every width and separator,
+  every binding form and use, every optional field, every whitespace code point -- with its complement, and rows each
+  member, or discloses it with its reason.
+    checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
+             `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
+                                                                                        entries key: rc 0); C23 (not JSON)
              baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
-             fields, each of the six a str, the count an int and not a bool, > 0        key sums), C17c-i (eight fields, a true
-                                                                                        count, -1, 0, 1.0, a numeric first field,
-                                                                                        a numeric note sha), C21g (an object)
+             fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
+                                                                                        of true, -1, 0, 1.0), C17h-m (each of the
+                                                                                        six positions numeric in turn), C17n (a
+                                                                                        None field), C21g (an object)
              md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
-             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C28
-                                                                                        (a padded ✓), C2/C2b/C2c/C2d (each glyph,
-                                                                                        C2c/C2d isolated), C8 (hold), C24 (a
-                                                                                        record, isolated)
+             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C26b
+                                                                                        (a list), C28 / C28b (a ✓ padded at its
+                                                                                        start / its end), C2/C2b/C2c/C2d (each
+                                                                                        glyph, C2c/C2d isolated), C8 (hold), C24
+                                                                                        (a record, isolated)
              the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
-             ends; str() of d                                                           move), C25l-r (the leading end; a row id
-                                                                                        with a trailing or a leading space);
-                                                                                        C15/C16 (the note); C26b (a list d)
+             ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
+             over its UTF-8 text, after str()                                          with a trailing or a leading space);
+                                                                                        C15/C16 (the note); C26b; C29 (no phase,
+                                                                                        no seat: its line exact); C20b (a
+                                                                                        non-ASCII note: its line exact); C21k (a
+                                                                                        list note holding no token: refused)
              the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
-             the cutoff: inclusive; a date counts only when the ISO shape OPENS it     C3, C4, C12 (isolated: before / on /
-                                                                                        after / far, and C12s a MATCHED identity
-                                                                                        dated 2026-10-17T12:00:00), C19a/b
-             output: cp1252-safe; the summary line WHOLE (its baseline number is the   C20; C1, C11, C12 (the summary exact --
-             frozen total, not the within-count); each refusal line WHOLE --           at C12-on the two numbers differ);
-             identifiers in order, its reason; the hint                                C3, C6, C9, C19a (the refusal line
-                                                                                        exact); C11 (the hint)
-             the glyph set: ONE binding of DOMAIN and of D_CLASS, each the four         C27 (an ast walk of both files: every
-                                                                                        store of the name, its value)
-    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (padded), R1n (null),
-             the answer a cell shows                                                    R3
-             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip      R1 (OK), R1g (every simple legacy d,
-                                                                                        null included), R1e (a record beside it),
-                                                                                        R1f (a refused exemption first)
-             the glyph: escaped; `?` for a blank or whitespace-only d (any whitespace)  R1b, R1d (space, tab, newline, NBSP)
+             the cutoff: inclusive; a date counts only when the ISO shape -- four      C3, C4, C12 (isolated: before / on /
+             digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
+                                                                                        dated 2026-10-17T12:00:00), C12w (MATCHED
+                                                                                        identities breaking the shape in one
+                                                                                        place -- year, month or day width, either
+                                                                                        separator: rc 0), C19a/b
+             output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
+             ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
+             refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
+                                                                                        C6, C9, C19a, C20, C20b, C29, C21k (the
+                                                                                        refusal line exact; C20's d escaped)
+             the glyph sets: ONE binding of DOMAIN and of D_CLASS, each the four,       C27 (an ast walk of both files: every
+             and no other way to change either                                         binding form of the name -- a store, a
+                                                                                        delete, a global, an import alias, a def
+                                                                                        or class, an except or match name, a
+                                                                                        parameter, an attribute or subscript store
+                                                                                        keyed by it; a call to globals / vars /
+                                                                                        locals / setattr / delattr / exec / eval /
+                                                                                        compile / __import__; __dict__ or
+                                                                                        __globals__ -- and every USE whitelisted:
+                                                                                        DOMAIN in `in' and as `" ".join's
+                                                                                        argument, D_CLASS in `.get(' and `in'; the
+                                                                                        checker's EFFECTIVE DOMAIN read by
+                                                                                        importing it)
+    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
+             the answer a cell shows                                                    end), R1n (null), R3
+             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
+             whatever optional fields the answer carries                                null, both pads, the newline and NBSP
+                                                                                        cells included), R1w (all 29 whitespace
+                                                                                        cells, whole), R1e (a
+                                                                                        record beside it), R1f (a refused
+                                                                                        exemption first), R1o (a grade, a badge
+                                                                                        and evidence all present), R1q (neither
+                                                                                        date nor note)
+             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells)
+             the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
+             or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
+                                                                                        str.isspace() code points)
              the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
              its labels                                                                 string), R2b (the fixture ledger, whose
-                                                                                        padded ✓ counts legacy)
-             the legend line; the two CSS rules the class adds                          R4; R5
-    Q2       the branches: rc 0 GOOD, rc 1 BAD with the refusal named, ANY other       W1, W2, W3 (rc 2), W7 (rc 7, its message
-             status BAD "could not run" with the checker's first line, stderr included  on stderr), W8 (python absent: rc 127)
+                                                                                        pads and null count legacy)
+             the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
+             the style block naming the class                                          rules naming `legacy')
+    Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
+             refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
+                                                                                        output whole, the entry named), W3 (rc 2),
+             FIRST line, stderr included                                                W7 (rc 7, a two-line message on stderr:
+                                                                                        the output whole), W8 (python absent: rc
+                                                                                        127), W9 (EVERY status 2-255: the else
+                                                                                        partition exhausted)
              the checker absent -> BAD                                                  W6
              an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
     DISCLOSED, each with its reason:
       a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
         arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
         (GPT-6 Astra, v4 pass: the two figures are different searches);
-      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^';
+      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^'; the `[:10]' slice before the compare:
+        equivalent, a string sharing the cutoff's first ten characters is never smaller than it; `repr' of a non-string date:
+        equivalent to `str' for every JSON value;
+      a missing or null NOTE hashed as "" (`d_notenone'): 0 of the 1,356 frozen answers has one, and 0 entries anywhere carry
+        a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
       case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
+      the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
+        wording: display only (their rc 2 is pinned; an emptied reason passes every row -- `x_apparatusmsg', Fable 5.1, v5
+        pass, measured);
+      the page's CSS outside the two rules this landing adds (a rule hiding every glyph would be HEAD's CSS, not this diff);
+      a change to the glyph sets by a mechanism C27 does not name (a helper module rebinding them after import, a C
+        extension) is outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
+        `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
+        first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
+      the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
+        x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
+        set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
+        v5 pass, measured: `+ ("OK",)' at the use site 80/96);
+      a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
+        sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
+        apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
       the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
         precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
-      the Q2 section header: `say' is stubbed in the W block, and it is display only.
+      the Q2 section header: `say' is stubbed in the W block, and it is display only;
+      the note-type scope of condition 2: "is it an answer" is `stage_tokens.is_answer', which tests membership on the untyped
+        note -- a list or dict note holding a token as an element or a key is a NON-answer and is skipped, as the renderer
+        also shows it (GPT-6 Astra, v5 pass, measured; K19's "nothing is skipped" was false); a list note holding no token is
+        an answer and is refused (C21k); a bool note: True rc 2, False rc 1 (Astra, measured).
     A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
     note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
     frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
-    two-edit design mutant d_dfold2, killed by C25d.
+    two-edit design mutant d_dfold2, killed by C25d.  Two kills the shipped ledger already supplies are ALSO rowed in isolation,
+    so no pin rests on the ledger's composition alone: the `entries' default (98 of 912 shipped rows carry no `entries' key;
+    C21j) and a latin-1 note encoding (34 frozen notes are non-ASCII, one beyond latin-1; C20b).
 
   CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
   v4 passes' findings):
@@ -85,16 +153,21 @@
     C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
     C17  a misshapen baseline (override; counts as strings)                                         -> 2
     C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
-    C17c-i  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0; a numeric
-         first field; a numeric note sha                                                            -> 2 each
+    C17c-g  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0  -> 2 each
+    C17h-m  the same, each of the six string positions numeric in turn: row, note sha, phase, seat, date, d     -> 2 each
+    C17n the same, a None date (`isinstance(v, (str, type(None)))' would pass it)                    -> 2
     C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
     C18b the same baseline with CRLF line endings passes the pin                                    -> 0
     C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
          the date NAMED as not ISO                                                                  -> 1 / 1
-    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback   -> 1
+    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback, its line EXACT
+         with the d backslash-escaped                                                               -> 1
+    C20b a new answer whose NOTE is non-ASCII ("café — ✓") -- rc 1, its line EXACT (the note's UTF-8 sha)  -> 1
     C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
          that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
          note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
+    C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
+    C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
     C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
     C23  a ledger that is not JSON                                                                  -> 2
     C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
@@ -104,8 +177,13 @@
          note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
     C26  a new answer with an explicit "d": null                                                     -> 1
     C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
-    C27  DOMAIN and D_CLASS: ONE binding each (an ast walk -- a second assignment is the effective one), each exactly ✓ ✕ ⏸ …
-    C28  a new answer BEFORE the cutoff with a PADDED glyph " ✓" (outside the four, as the renderer says) -> 1
+    C27  DOMAIN and D_CLASS: ONE binding each and NO other way to change them -- an ast walk of every binding form and
+         every use (whitelisted), and the checker's EFFECTIVE DOMAIN read by importing it -- each exactly ✓ ✕ ⏸ …
+    C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
+    C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
+    C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
+         one-digit day, a `/' for the first separator, for the second -- each in its fixture baseline, so only the shape
+         decides                                                                                    -> 0 each
   RENDERER:
     R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
     R1b  an escapable `d` ("<b>&") renders escaped
@@ -114,8 +192,13 @@
     R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
     R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
     R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
-         null), the date, the note
-    R1h  a padded glyph " ✓" renders legacy, not ok
+         "\n", "\xa0", null), the date, the note
+    R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
+    R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
+    R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
+    R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
+    R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
+         whitespace set exhausted
     R1n  an explicit "d": null renders legacy with the glyph "None", not …
     R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
          own count by exact membership, and its labels
@@ -123,17 +206,21 @@
     R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
          a kill
     R4   the legend carries the legacy line EXACTLY
-    R5   the page carries the two CSS rules the class adds, EXACTLY (the legacy outline; the glyph's muted italic 11px)
+    R5   the page carries the two CSS rules the class adds, EXACTLY, and NO other rule in its style block names `legacy'
   WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
   carry its BRANCH's own words):
-    W1   the shipped ledger                    -> GOOD, failures 0
-    W2   a new off-domain answer               -> BAD "beyond the frozen legacy ceiling", the entry named, failures >= 1
+    W1   the shipped ledger                    -> exactly "GOOD <the summary line>" and "FAILURES 0"
+    W2   a new off-domain answer               -> BAD, its WHOLE output: the first line, every line of the checker's
+         output indented, the counter
     W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
     W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
     W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
     W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
-    W7   a checker that exits 7 with its message on STDERR -> BAD "could not run (rc 7): <that message>", failures >= 1
+    W7   a checker that exits 7 with a TWO-line message on STDERR -> exactly "BAD ... could not run (rc 7): <its FIRST line>"
+         and "FAILURES 1"
     W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
+    W9   EVERY status 2-255, a stub exiting each in turn (254 runs)    -> each exactly "BAD ... could not run (rc N): <its
+         first line>" and the counter 1 -- the `else' partition EXHAUSTED
 """
 import collections, copy, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile
 
@@ -240,6 +327,11 @@
         row, e.get("phase") or "", e.get("seat") or "", dt or "(none)", str(e["d"]), sha16(e.get("note")), why)
 
 
+def cp(s):
+    """what the checker's cp1252 stdout, reconfigured errors="backslashreplace", carries for s -- as run_checker decodes it"""
+    return s.encode("cp1252", "backslashreplace").decode("cp1252")
+
+
 def summary_line(n_cur, n_within, n_base):
     return ("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff 2026-10-17 inclusive"
             % (n_cur, n_within, n_base))
@@ -250,7 +342,7 @@
             str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]
 
 
-print("# dashokclass controls (v5) -- checker %s | renderer %s | precommit %s | baseline %s"
+print("# dashokclass controls (v6) -- checker %s | renderer %s | precommit %s | baseline %s"
       % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
          hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
 # ------------------------------------------------------------------ the checker
@@ -259,8 +351,9 @@
 #  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
 #  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
 #  v5: the WHOLE line -- "inclusive" dropped from it passed all 72 v4 controls (Fable 5.1, v4 pass)
-say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY", rc == 0 and first == summary_line(N_OFF, N_OFF, N_OFF),
-    "rc %d: %s" % (rc, first))
+#  v6: and ALONE -- the hint printed on a clean run passed all 96 v5 controls
+say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY, and the only line",
+    rc == 0 and out == [summary_line(N_OFF, N_OFF, N_OFF)], "rc %d: %d lines; %s" % (rc, len(out), first))
 for lab, ent, want in [
     ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
     ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
@@ -281,6 +374,16 @@
     #  v5: a PADDED glyph is outside the four for the checker as for the renderer (R1h) -- `str(d).strip() in DOMAIN` passed
     #  all 72 v4 controls (Fable 5.1, Grok 4.7, v4 pass)
     ("C28 a new answer BEFORE the cutoff with a padded glyph ' ✓'", ans("2026-10-10", d=" ✓"), 1),
+    #  v6: the OTHER end -- `str(x["d"]).rstrip() in DOMAIN' passed all 96 v5 controls (GPT-6 Astra, v5 pass)
+    ("C28b a new answer BEFORE the cutoff with a glyph padded at its END '✓ '", ans("2026-10-10", d="✓ "), 1),
+    #  v6: a NON-ASCII note -- its sha is over the note's UTF-8; a latin-1 encode raises (or rehashes) on it (GLM 5.3, v5 pass)
+    ("C20b a new answer whose note is non-ASCII", ans("2026-10-10", d="OK", note="café — ✓"), 1),
+    #  v6: no phase, no seat -- each keys and prints as "" ; dropping the `or ""' printed "None" and passed all 96 v5 controls
+    #  (GLM 5.3, v5 pass, measured)
+    ("C29 a new answer with no phase and no seat", {"date": "2026-10-10", "d": "OK", "note": "no phase or seat"}, 1),
+    #  v6: a LIST note holding no token is an ANSWER (is_answer finds no token in it) and is refused, never skipped; a
+    #  mutant dropping the str() before the hash raised on it instead (Fable 5.1 measured rc 1 on the v4 pass)
+    ("C21k a new answer whose note is a list holding no token", ans("2026-10-10", d="OK", note=["a list note"]), 1),
 ]:
     rc, out = run_checker(with_entries([(ROW0, ent)]))
     tb = any("Traceback" in l for l in out)
@@ -289,9 +392,12 @@
     why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
     #  v5: the WHOLE refusal line for C3 (the cutoff reason), C6 (an undated entry: "(none)", no ISO clause) and C19a (the
     #  ISO clause) -- v4 read only rc and the line count (Fable 5.1, GPT-6 Astra, v4 pass)
-    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO}.get(lab.split()[0])
+    #  v6: also C20 (its d backslash-escaped by the cp1252 reconfigure -- "replace" printed `?' and passed all 96 v5
+    #  controls), C20b, C29 and C21k
+    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO, "C20": WHY_CUT, "C20b": WHY_CEIL, "C29": WHY_CEIL,
+                 "C21k": WHY_CEIL}.get(lab.split()[0])
     offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
-    exact = exact_why is None or offl == [offline(ROW0, ent, exact_why)]
+    exact = exact_why is None or offl == [cp(offline(ROW0, ent, exact_why))]
     say(lab, rc == want and not tb and why and exact, "rc %d (want %d)%s%s%s" % (
         rc, want, " TRACEBACK" if tb else "", "" if why else " REASON NOT NAMED",
         "" if exact else " LINE NOT EXACT: %r" % (offl[:1],)))
@@ -393,10 +499,13 @@
 #  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
 s11 = summary_line(N_OFF, 0, 0)
 f11 = out[0] if out else ""
-hint = any("give each a `d` from" in l for l in out)      # the instruction line (Fable 5.1, v3 pass: no control asserted it)
-say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint printed",
-    rc == 1 and nb == N_OFF and f11 == s11 and hint, "rc %d, %d of %d named; summary %s; hint %s"
-    % (rc, nb, N_OFF, "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else "MISSING"))
+#  v6: the hint WHOLE -- a false "all records need classification" passed the v5 prefix test (GPT-6 Astra, v5 pass) -- and the
+#  output exactly the summary, one line per refusal, the hint
+HINT = cp("  -> give each a `d` from ✓ ✕ ⏸ … (or omit `d`, which renders as …); a non-answer record is exempt").strip()
+hint = bool(out) and out[-1].strip() == HINT
+say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint WHOLE",
+    rc == 1 and nb == N_OFF and f11 == s11 and hint and len(out) == N_OFF + 2, "rc %d, %d of %d named, %d lines; summary %s; hint %s"
+    % (rc, nb, N_OFF, len(out), "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else repr(out[-1][:90] if out else "")))
 # C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
 #  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
 for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
@@ -417,29 +526,104 @@
 fb = wjson("b_cut_suffixed.json", base + [ident(ROW0, e) + [1]])
 rc, out = run_checker(with_entries([(ROW0, e)]), fb)
 say("C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00", rc == 1, "rc %d (want 1)" % rc)
+#  C12w (v6): the ISO SHAPE's widths and separators -- `\d{1,2}' for the month passed all 96 v5 controls, reading
+#  "2026-9-1" as a date after the cutoff (GPT-6 Astra, v5 pass).  Each identity is FROZEN and breaks the shape in one place,
+#  each chosen to compare at or after the cutoff if the shape were loosened there, so only the shape decides: rc 0
+#  (a one-edit mutant loosens ONE separator, so each has its own row: one date breaking both would miss either alone)
+for tag, dt in (("year", "99999-10-18"), ("month", "2026-9-17"), ("day", "2026-10-9"), ("sep1", "2026/10-18"),
+                ("sep2", "2026-10/18")):
+    e = ans(dt, d="OK", seat="kimi", note="iso shape " + tag)
+    fb = wjson("b_cut_w_%s.json" % tag, base + [ident(ROW0, e) + [1]])
+    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
+    say("C12w the ISO shape's %s: a FROZEN identity dated %s is not read as a date" % (tag, dt), rc == 0, "rc %d (want 0)" % rc)
 rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
 say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
 #  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
 #  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
 #  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
 import ast  # noqa: E402
-#  v5: by the BINDINGS, not the first line -- a second `DOMAIN = (..., "ZXQ")' further down is the one that takes effect, and
-#  the v4 reader of the first line passed it (Fable 5.1, v4 pass).  Every store of the name anywhere in the file is counted
-#  (an assignment, an augmented one, a loop target ...), and a `global' naming it is refused: exactly one binding, at module
-#  level, whose value is a literal.
-def literal(path, name):
+#  v5 counted the Name stores of each name; v6 walks EVERY binding form and EVERY use.  `globals()["DOMAIN"] = ...' and
+#  `D_CLASS.update(ZXQ="ok")' each passed all 96 v5 controls -- the first is no Name store, the second mutates the dict
+#  without rebinding it (GLM 5.3, GPT-6 Astra, v5 pass, measured).  So: exactly one binding, a module-level assignment of a
+#  literal; no other binding form of the name (a store or delete, a global or nonlocal, an import alias, a def or class, an
+#  except or match name, a parameter, an attribute or subscript store keyed by it); no call to the builtins that rebind by
+#  name or by string (globals, vars, locals, setattr, delattr, exec, eval, compile, __import__) and no __dict__ / __globals__;
+#  and every USE of the name on a whitelist -- DOMAIN only in `in' / `not in' and as `" ".join(...)''s argument, D_CLASS only
+#  as `D_CLASS.get(...)' and in `in' / `not in'.  The checker is import-safe, so its EFFECTIVE DOMAIN is also read by importing
+#  it; the renderer renders on import, so it is read by the walk alone.
+BANNED = {"globals", "vars", "locals", "setattr", "delattr", "exec", "eval", "compile", "__import__"}
+
+
+def walk_name(path, name, use_ok):
     tree = ast.parse(io.open(path, encoding="utf-8").read())
+    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
+    probs = []
     stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
-    globs = [n for n in ast.walk(tree) if isinstance(n, ast.Global) and name in n.names]
-    top = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(g, ast.Name) and g.id == name for g in n.targets)]
-    if len(stores) != 1 or globs or len(top) != 1:
-        return "%d bindings, %d top-level assignments, %d global statements" % (len(stores), len(top), len(globs))
-    return ast.literal_eval(top[0].value)
-dom, dcls = literal(CHECKER, "DOMAIN"), literal(RENDER, "D_CLASS")
+    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
+           and n.targets[0].id == name]
+    if len(stores) != 1 or len(top) != 1:
+        probs.append("%d stores, %d module-level assignments" % (len(stores), len(top)))
+    for n in ast.walk(tree):
+        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Del):
+            probs.append("del")
+        elif isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
+            probs.append("global/nonlocal")
+        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split(".")[0]) == name for a in n.names):
+            probs.append("import alias")
+        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
+            probs.append("def/class")
+        elif isinstance(n, ast.ExceptHandler) and n.name == name:
+            probs.append("except name")
+        elif isinstance(n, ast.arg) and n.arg == name:
+            probs.append("parameter")
+        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == name:
+            probs.append("match name")
+        elif isinstance(n, ast.Attribute) and n.attr == name and not isinstance(n.ctx, ast.Load):
+            probs.append("attribute store")
+        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load) and isinstance(n.slice, ast.Constant)
+              and n.slice.value == name):
+            probs.append("subscript store keyed by the name")
+        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
+            probs.append("call to " + n.func.id)
+        elif isinstance(n, ast.Attribute) and n.attr in ("__dict__", "__globals__"):
+            probs.append(n.attr)
+        elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
+            probs.append("a use at line %d" % n.lineno)
+    return (ast.literal_eval(top[0].value) if len(top) == 1 else None), probs
+
+
+def in_compare(n, parent):
+    p = parent.get(n)
+    return (isinstance(p, ast.Compare) and n in p.comparators
+            and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))
+
+
+def dom_use(n, parent):
+    p = parent.get(n)
+    return in_compare(n, parent) or (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
+                                     and p.func.attr == "join" and isinstance(p.func.value, ast.Constant))
+
+
+def dcls_use(n, parent):
+    p = parent.get(n)
+    return in_compare(n, parent) or (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
+                                     and parent.get(p).func is p)
+
+
+dom, dprobs = walk_name(CHECKER, "DOMAIN", dom_use)
+dcls, cprobs = walk_name(RENDER, "D_CLASS", dcls_use)
+r_imp = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import check_entry_domain as c; "
+                        "print(ascii(c.DOMAIN))", os.path.dirname(DEFAULT_CHECKER)], capture_output=True, text=True)
+try:
+    eff = ast.literal_eval(r_imp.stdout.strip()) if r_imp.returncode == 0 else None
+except (ValueError, SyntaxError):
+    eff = None
 four = ("✓", "✕", "⏸", "…")
-say("C27 ONE binding each: the checker's DOMAIN and the renderer's D_CLASS keys are exactly ✓ ✕ ⏸ …",
-    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four),
-    "DOMAIN %r | D_CLASS keys %r" % (dom, sorted(dcls) if isinstance(dcls, dict) else dcls))
+say("C27 ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ …",
+    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four)
+    and not dprobs and not cprobs and isinstance(eff, tuple) and sorted(eff) == sorted(four),
+    "DOMAIN %r %s | effective %r | D_CLASS keys %r %s" % (dom, dprobs or "", eff, sorted(dcls) if isinstance(dcls, dict) else dcls,
+                                                          cprobs or ""))
 rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
 say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
 #  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
@@ -455,7 +639,13 @@
 for tag, row_, how in (("c", kx[:6] + [1, "extra"], "eight fields"), ("d", kx[:6] + [True], "a count of true"),
                        ("e", kx[:6] + [-1], "a count of -1"), ("f", kx[:6] + [0], "a count of 0"),
                        ("g", kx[:6] + [1.0], "a count of 1.0"), ("h", [5] + kx[1:6] + [1], "a numeric first field"),
-                       ("i", kx[:5] + [5, 1], "a numeric note sha")):
+                       ("i", kx[:5] + [5, 1], "a numeric note sha"),
+                       #  v6: the MIDDLE positions -- `for v in k[::5]' checked only the first and the sixth and passed all
+                       #  96 v5 controls (GPT-6 Astra, v5 pass)
+                       ("j", kx[:1] + [5] + kx[2:6] + [1], "a numeric phase"), ("k", kx[:2] + [5] + kx[3:6] + [1], "a numeric seat"),
+                       ("l", kx[:3] + [5] + kx[4:6] + [1], "a numeric date"), ("m", kx[:4] + [5] + kx[5:6] + [1], "a numeric d"),
+                       #  v6: a None field -- `isinstance(v, (str, type(None)))' passed all 96 v5 controls (Fable 5.1, v5 pass)
+                       ("n", kx[:3] + [None] + kx[4:6] + [1], "a None date")):
     rc, out = run_checker(LEDGER, wjson("b_row_%s.json" % tag, base + [row_]))
     tb = any("Traceback" in l for l in out)
     say("C17%s a misshapen baseline row: %s (override)" % (tag, how), rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
@@ -485,6 +675,11 @@
     say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
 rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
 say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
+#  C21j (v6): a row with NO entries key is an empty row, not a misshapen one -- `r.get("entries")' at either site turns it
+#  into rc 2; the shipped ledger kills that today (98 of 912 rows carry no `entries'), so it is rowed in isolation (GLM 5.3,
+#  v5 pass)
+rc, out = run_checker(wjson("l_noentries.json", {"rows": [{"id": "ctlnoent"}, {"id": "ctlent", "entries": [ans("2026-10-18", d="✓")]}]}))
+say("C21j a row with no entries key beside a valid one", rc == 0, "rc %d" % rc)
 #  C21h: the shape check passes it, then is_answer raises on a NON-STRING note -- the one input that still reaches the walk's
 #  except-arm, so that arm stays a measured rc 2 rather than dead code
 rc, out = run_checker(wjson("l_shape_note.json", {"rows": [{"id": "x", "entries": [
@@ -553,9 +748,29 @@
               #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
               #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
               {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
-               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"}]},
+               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"},
+                           #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
+                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
+              #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
+              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while 649 and 642 of the 670
+              #  shipped legacy cells lost the class line (GPT-6 Astra, v5 pass)
+              #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
+              #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
+              {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
+               "entries": [{"phase": "assess", "seat": "fable5", "d": "BARE"}]},
+              {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
+               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
+                            "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
               {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
                "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
+#  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
+#  `str.strip()' removes, and `.strip(" \t\n\xa0")' passed all 96 v5 controls but R3's presence pin (Fable 5.1, v5 pass)
+WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
+for i in range(0, len(WS), len(SEATS)):
+    FX["rows"].append({"id": "ctlws%02d" % (i // len(SEATS)), "title": "whitespace set control row", "sev": "LOW", "state": "open",
+                       "commits": "", "entries": [{"phase": "assess", "seat": SEATS[j], "date": "2026-10-16", "d": ch,
+                                                   "note": "ws control U+%04X" % ord(ch)}
+                                                  for j, ch in enumerate(WS[i:i + len(SEATS)])]})
 fx_path = wjson("fx_render.json", FX)
 
 
@@ -572,7 +787,8 @@
 
 
 CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
-             "padded glyph control", "tab control", "newline control", "nbsp control", "null control")
+             "padded glyph control", "tab control", "newline control", "nbsp control", "null control", "padded trailing control",
+             "optional fields control", "BARE", "ws control U+")
 
 
 def cells(html_text):
@@ -628,8 +844,11 @@
     #  LEGACY and d == "OK"` and `... and str(d).strip()` passed all 46 v3 controls (Fable 5.1, v3 pass, measured)
     want = [(note, d, html.escape(" — ".join([legacy_line(d), "2026-10-16", note]), quote=True))
             for note, d in (("a renderer control", "OK"), ("a renderer control", ""), ("a renderer control", "N/A"),
-                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"),
-                            ("tab control", "\t"), ("null control", None))]
+                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"), ("padded trailing control", "✓ "),
+                            ("tab control", "\t"), ("null control", None),
+                            #  v6: the newline and NBSP cells -- R1d checked their class and glyph only, so `if cls == LEGACY
+                            #  and d not in ("\n", "\xa0")' passed all 96 v5 controls (Grok 4.7, v5 pass)
+                            ("newline control", "\n"), ("nbsp control", "\xa0"))]
     legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
     missing = [(note, d) for note, d, whole in want if whole not in legacy]
     return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])
@@ -662,9 +881,37 @@
 ha_fx = render(RENDER, fx_path, "after")
 ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
 ok, det = r1g(ha_fx); say("R1g every simple legacy cell's WHOLE tooltip, the class line for ITS d", ok, det)
+#  v6: both ends, and the glyph TEXT -- `html.escape(str(t).strip())' showed " ✓" as "✓" and passed all 96 v5 controls,
+#  which read only the class (GPT-6 Astra, v5 pass)
 pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
-say("R1h a padded glyph ' ✓' renders legacy, not ok", len(pad) == 1 and pad[0][0] == "legacy",
-    "cell %r" % (pad[0][:2],) if pad else "render FAILED or no cell")
+padt = [c for c in cells(ha_fx or "") if "padded trailing control" in c[2]]
+say("R1h a ✓ padded at either end renders legacy, its glyph text exactly as written",
+    len(pad) == 1 and pad[0][:2] == ("legacy", " ✓") and len(padt) == 1 and padt[0][:2] == ("legacy", "✓ "),
+    "cells %r %r" % (pad[0][:2] if pad else None, padt[0][:2] if padt else None))
+opt = [c for c in cells(ha_fx or "") if "optional fields control" in c[2]]
+want_o = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "MANUAL", "the author did this review (shown, not hidden)",
+                                  "optional fields control", "evidence: regress/artifacts/x/ctl.txt"]), quote=True)
+say("R1o a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first",
+    len(opt) == 1 and opt[0][0] == "legacy" and opt[0][2] == want_o,
+    "cell %r; tooltip %s" % (opt[0][:2] if opt else None, "exact" if opt and opt[0][2] == want_o else "WRONG: %r" % (opt[0][2][:140] if opt else "")))
+#  R1p (v6): the class line ONLY on a legacy cell -- `if cls in (LEGACY, "pend")' and `if cls != "ok"' each passed all 96 v5
+#  controls, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend cell, 833 on HEAD's ledger (Fable 5.1, v5 pass)
+plain = html.escape("2026-10-16 — a renderer control", quote=True)
+ctl = [c for c in cells(ha_fx or "") if not any(k in c[2] for k in CTL_OTHER)][:len(SEATS)]
+tips = dict(zip(SEATS, [c[2] for c in ctl])) if len(ctl) == len(SEATS) else {}
+bad_p = [s for s in ("fable5", "codex", "glm", "deepseek") if tips.get(s) != plain]
+say("R1p the NON-legacy answer cells -- ok, pend, bad, hold -- carry no class line: the date and the note alone",
+    bool(tips) and not bad_p, "wrong: %r" % ([(s, (tips.get(s) or "")[:70]) for s in bad_p],))
+bare = [c for c in cells(ha_fx or "") if "BARE" in c[2]]
+want_b = html.escape(legacy_line("BARE"), quote=True)
+say("R1q a legacy answer with neither date nor note: its tooltip is the class line alone",
+    len(bare) == 1 and bare[0][0] == "legacy" and bare[0][2] == want_b, "cells %d: %r" % (len(bare), [c[2][:80] for c in bare]))
+wsc = [c for c in cells(ha_fx or "") if "ws control U+" in c[2]]
+wsw = {html.escape(" — ".join([legacy_line(ch), "2026-10-16", "ws control U+%04X" % ord(ch)]), quote=True) for ch in WS}
+wsbad = [c[2][-14:] for c in wsc if c[0] != "legacy" or c[1] != "?" or c[2] not in wsw]
+say("R1w every str.isspace() code point alone as d (%d) shows ? and renders legacy, each with its WHOLE tooltip" % len(WS),
+    len(wsc) == len(WS) == 29 and not wsbad and len({c[2] for c in wsc}) == 29,
+    "%d cells of %d; wrong: %r" % (len(wsc), len(WS), wsbad[:5]))
 ok, det = r1e(ha_fx); say("R1e an answer with a record beside it: its WHOLE tooltip", ok, det)
 nul = [c for c in cells(ha_fx or "") if "null control" in c[2]]
 say("R1n an explicit null d renders legacy with the glyph None", len(nul) == 1 and nul[0][:2] == ("legacy", "None"),
@@ -683,8 +930,13 @@
 #  (GPT-6 Astra, Fable 5.1, v4 pass)
 CSS = ("td.c.legacy { outline:1px dashed var(--line); outline-offset:-3px; }",
        ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
-say("R5 the page carries the legacy class's two CSS rules EXACTLY", ha_fx is not None and all(c in ha_fx for c in CSS),
-    "missing %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")],))
+#  v6: and they are the ONLY rules in the style block naming `legacy' -- a later `.c.legacy .g { font-size:0; }' left both
+#  present and hid every legacy glyph (GPT-6 Astra, v5 pass)
+sty = re.search(r"<style>(.*?)</style>", ha_fx or "", re.S)
+leg_rules = [" ".join(m.group(0).split()) for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", sty.group(1) if sty else "")]
+say("R5 the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it",
+    ha_fx is not None and all(c in ha_fx for c in CSS) and sorted(leg_rules) == sorted(CSS),
+    "missing %r; legacy rules %d %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")], len(leg_rules), [r[:40] for r in leg_rules]))
 
 
 def census(html_text):
@@ -694,8 +946,10 @@
 
 
 hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
-cb, sb = census(hb)
-ca, sa = census(ha)
+#  v6: guarded -- a renderer that crashes on the shipped ledger made census() raise, so the controls died with no tally and no
+#  sentinel and the mutant driver scored a KILL as INCOMPLETE (Fable 5.1, v5 pass); now R2 says NO and the run completes
+cb, sb = census(hb) if hb else (collections.Counter(), "")
+ca, sa = census(ha) if ha else (collections.Counter(), "")
 same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
 moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
 nums = [int(x) for x in re.findall(r"(\d+)", sa)]
@@ -797,10 +1051,12 @@
             ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING"),
             #  v5: ANY status other than 0 and 1 is "could not run" -- `else' narrowed to `elif [ $_cedrc -eq 2 ]' passed all 72
             #  v4 controls, leaving rc 7 or 127 silently green (GPT-6 Astra, Fable 5.1, v4 pass).  W7's message is on STDERR,
-            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given
+            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given -- and
+            #  the git-bash wrapper PREPENDS /mingw64/bin, /usr/bin and ~/bin to that PATH; none holds a python on this
+            #  machine, and if one did W8 would fail LOUDLY (GOOD instead of BAD), never pass falsely (Fable 5.1, v5 pass)
             ("W7 Q2 with a checker that exits 7, its message on stderr",
-             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB CHECKER ON STDERR\\n")\nsys.exit(7)\n'), {},
-             "BAD", 1, "could not run (rc 7): STUB CHECKER ON STDERR"),
+             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB FIRST LINE\\nSTUB SECOND LINE\\n")\nsys.exit(7)\n'), {},
+             "BAD", 1, "could not run (rc 7): STUB FIRST LINE"),
             ("W8 Q2 with python absent from PATH (rc 127)", w_tools("8", LEDGER),
              {"PATH": os.path.join(os.path.dirname(os.path.dirname(BASH)), "usr", "bin")}, "BAD", 1, "could not run (rc 127)")):
         env = dict(os.environ)
@@ -815,8 +1071,45 @@
         #  W2's refusal must also NAME the entry to the committer: deleting Q2's `printf | sed` passed every v3 control, which
         #  read only the first line and the counter (Grok 4.7, v3 pass)
         named = (not lab.startswith("W2 ")) or any(l.strip().startswith("OFF-DOMAIN ANSWER  row") for l in outl)
+        #  v6: W1 and W7 read the WHOLE output -- the apparatus branch's `head -1' -> `tail -1' passed all 96 v5 controls on
+        #  one-line messages (GPT-6 Astra, v5 pass)
+        whole = {"W1": ["GOOD " + summary_line(N_OFF, N_OFF, N_OFF), "FAILURES 0"],
+                 "W7": ["BAD check_entry_domain.py could not run (rc 7): STUB FIRST LINE", "FAILURES 1"]}.get(lab.split()[0])
+        #  v6: W2's WHOLE output -- its first line, then EVERY line of the checker's own output, indented, then the counter:
+        #  Q2's `printf | sed' replaced by a constant "OFF-DOMAIN ANSWER  row ..." line passed all 96 v5 controls, which read a
+        #  prefix (Grok 4.7, v5 pass).  The checker's lines come from running the checker in W2's own tools dir as Q2 does.
+        if lab.split()[0] == "W2":
+            e2 = subprocess.run([sys.executable, os.path.join(tools, "pipeline", "check_entry_domain.py")],
+                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
+            whole = (["BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one "
+                      "edited):"] + ["          " + l for l in e2.stdout.decode("cp1252", "replace").splitlines()] + ["FAILURES 1"])
+        named = named and (whole is None or outl == whole)
+        #  v6: W2's first line EXACT -- its parenthetical dropped passed all 96 v5 controls (Fable 5.1, v5 pass)
+        named = named and (lab.split()[0] != "W2" or firstl == "BAD an off-domain ledger answer is beyond the frozen legacy ceiling "
+                                                           "(a new one, a copy, or an old one edited):")
         ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
         say(lab, ok, "%s | failures %d" % (firstl[:90], nf))
+    #  W9 (v6): EVERY status but 0 and 1 is "could not run".  The else partition is {2..255}, EXHAUSTED in ONE bash loop over
+    #  a stub that exits $W9RC: `else' -> `elif [ $_cedrc -ne 3 ]' passed all 96 v5 controls, whose W3, W7 and W8 are three
+    #  statuses of 254 (Grok 4.7, v5 pass)
+    w9 = w_tools("9", LEDGER, stub='import os, sys\nsys.stderr.write("STUB rc %s\\n" % os.environ["W9RC"])\n'
+                                   'sys.exit(int(os.environ["W9RC"]))\n')
+    loop = os.path.join(T, "q2_loop.sh")
+    io.open(loop, "w", encoding="utf-8", newline="\n").write(
+        'say () { :; }\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n_HERE="$1"\n'
+        'for W9RC in $(seq 2 255); do export W9RC; fails=0; echo "RC $W9RC"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\ndone\n')
+    env = dict(os.environ)
+    for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
+        env.pop(k, None)
+    r = subprocess.run([BASH, loop.replace("\\", "/"), w9.replace("\\", "/")], capture_output=True, env=env)
+    got9 = r.stdout.decode("cp1252", "replace").splitlines()
+    want9 = []
+    for n_ in range(2, 256):
+        want9 += ["RC %d" % n_, "BAD check_entry_domain.py could not run (rc %d): STUB rc %d" % (n_, n_), "FAILURES 1"]
+    bad9 = ([n_ for n_ in range(2, 256) if got9[3 * (n_ - 2):3 * (n_ - 1)] != want9[3 * (n_ - 2):3 * (n_ - 1)]]
+            if len(got9) == len(want9) else ["%d lines of %d" % (len(got9), len(want9))])
+    say("W9 Q2 with EVERY status 2-255 (254 runs of one stub): each exactly BAD 'could not run (rc N)' with its first line, "
+        "the counter 1", got9 == want9, "wrong at: %r" % (bad9[:8],))
 
 shutil.rmtree(T, ignore_errors=True)
 print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
```

### 4b. `run_controls_v6.py`, WHOLE (its docstring is the CONTRACT and the row list)

```python
     1	#!/usr/bin/env python3
     2	"""Controls for `dashokclass` (2026-10-17, v6 after the v5 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
     3	ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
     4	ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
     5	the three files under test (run_mutants_v6.py and the staged runs use them); the defaults are the tree's.
     6	
     7	  THE CONTRACT (v6) -- the v4 pass found pins that tested ONE edge of a decision, and v5 rowed the dual edge.  The v5 pass
     8	  (GPT-6 Astra and Fable 5.1 measured, GLM 5.3 reasoned, Grok 4.7 traced) found the next layer on two axes.  A v5 pin covered
     9	  PART of its decision's GENERATING SET -- the leading pad but not the trailing one, two of the baseline row's six string
    10	  positions, the ISO shape's anchor but not its widths or separators, the glyph sets' Name stores while `globals()' and a dict
    11	  mutation changed them, the hint's prefix, a tooltip whose fixture held no optional field, a CSS rule's presence but not the
    12	  absence of an overriding one, the apparatus branch's first line on one-line output, four whitespace code points of 29, the
    13	  newline and NBSP cells' class but not their tooltips, Q2's `else' at three of its 254 statuses, the named entry by a prefix
    14	  of W2's output.  And a pin
    15	  asserting a property of the SELECTED set said nothing about its COMPLEMENT (Fable 5.1) -- every legacy cell has the class
    16	  line but not ONLY legacy cells, the padded cell's class but not its text, the set where it is DEFINED but not where it is
    17	  USED.  So v6 enumerates each decision's generating set -- every operand position, both ends, every width and separator,
    18	  every binding form and use, every optional field, every whitespace code point -- with its complement, and rows each
    19	  member, or discloses it with its reason.
    20	    checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
    21	             `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
    22	                                                                                        entries key: rc 0); C23 (not JSON)
    23	             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
    24	             fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
    25	                                                                                        of true, -1, 0, 1.0), C17h-m (each of the
    26	                                                                                        six positions numeric in turn), C17n (a
    27	                                                                                        None field), C21g (an object)
    28	             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
    29	             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C26b
    30	                                                                                        (a list), C28 / C28b (a ✓ padded at its
    31	                                                                                        start / its end), C2/C2b/C2c/C2d (each
    32	                                                                                        glyph, C2c/C2d isolated), C8 (hold), C24
    33	                                                                                        (a record, isolated)
    34	             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
    35	             ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
    36	             over its UTF-8 text, after str()                                          with a trailing or a leading space);
    37	                                                                                        C15/C16 (the note); C26b; C29 (no phase,
    38	                                                                                        no seat: its line exact); C20b (a
    39	                                                                                        non-ASCII note: its line exact); C21k (a
    40	                                                                                        list note holding no token: refused)
    41	             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
    42	             the cutoff: inclusive; a date counts only when the ISO shape -- four      C3, C4, C12 (isolated: before / on /
    43	             digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
    44	                                                                                        dated 2026-10-17T12:00:00), C12w (MATCHED
    45	                                                                                        identities breaking the shape in one
    46	                                                                                        place -- year, month or day width, either
    47	                                                                                        separator: rc 0), C19a/b
    48	             output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
    49	             ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
    50	             refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
    51	                                                                                        C6, C9, C19a, C20, C20b, C29, C21k (the
    52	                                                                                        refusal line exact; C20's d escaped)
    53	             the glyph sets: ONE binding of DOMAIN and of D_CLASS, each the four,       C27 (an ast walk of both files: every
    54	             and no other way to change either                                         binding form of the name -- a store, a
    55	                                                                                        delete, a global, an import alias, a def
    56	                                                                                        or class, an except or match name, a
    57	                                                                                        parameter, an attribute or subscript store
    58	                                                                                        keyed by it; a call to globals / vars /
    59	                                                                                        locals / setattr / delattr / exec / eval /
    60	                                                                                        compile / __import__; __dict__ or
    61	                                                                                        __globals__ -- and every USE whitelisted:
    62	                                                                                        DOMAIN in `in' and as `" ".join's
    63	                                                                                        argument, D_CLASS in `.get(' and `in'; the
    64	                                                                                        checker's EFFECTIVE DOMAIN read by
    65	                                                                                        importing it)
    66	    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
    67	             the answer a cell shows                                                    end), R1n (null), R3
    68	             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
    69	             whatever optional fields the answer carries                                null, both pads, the newline and NBSP
    70	                                                                                        cells included), R1w (all 29 whitespace
    71	                                                                                        cells, whole), R1e (a
    72	                                                                                        record beside it), R1f (a refused
    73	                                                                                        exemption first), R1o (a grade, a badge
    74	                                                                                        and evidence all present), R1q (neither
    75	                                                                                        date nor note)
    76	             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells)
    77	             the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
    78	             or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
    79	                                                                                        str.isspace() code points)
    80	             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
    81	             its labels                                                                 string), R2b (the fixture ledger, whose
    82	                                                                                        pads and null count legacy)
    83	             the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
    84	             the style block naming the class                                          rules naming `legacy')
    85	    Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
    86	             refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
    87	                                                                                        output whole, the entry named), W3 (rc 2),
    88	             FIRST line, stderr included                                                W7 (rc 7, a two-line message on stderr:
    89	                                                                                        the output whole), W8 (python absent: rc
    90	                                                                                        127), W9 (EVERY status 2-255: the else
    91	                                                                                        partition exhausted)
    92	             the checker absent -> BAD                                                  W6
    93	             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
    94	    DISCLOSED, each with its reason:
    95	      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
    96	        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
    97	        (GPT-6 Astra, v4 pass: the two figures are different searches);
    98	      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^'; the `[:10]' slice before the compare:
    99	        equivalent, a string sharing the cutoff's first ten characters is never smaller than it; `repr' of a non-string date:
   100	        equivalent to `str' for every JSON value;
   101	      a missing or null NOTE hashed as "" (`d_notenone'): 0 of the 1,356 frozen answers has one, and 0 entries anywhere carry
   102	        a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
   103	      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
   104	      the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
   105	        wording: display only (their rc 2 is pinned; an emptied reason passes every row -- `x_apparatusmsg', Fable 5.1, v5
   106	        pass, measured);
   107	      the page's CSS outside the two rules this landing adds (a rule hiding every glyph would be HEAD's CSS, not this diff);
   108	      a change to the glyph sets by a mechanism C27 does not name (a helper module rebinding them after import, a C
   109	        extension) is outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
   110	        `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
   111	        first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
   112	      the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
   113	        x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
   114	        set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
   115	        v5 pass, measured: `+ ("OK",)' at the use site 80/96);
   116	      a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
   117	        sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
   118	        apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
   119	      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
   120	        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
   121	      the Q2 section header: `say' is stubbed in the W block, and it is display only;
   122	      the note-type scope of condition 2: "is it an answer" is `stage_tokens.is_answer', which tests membership on the untyped
   123	        note -- a list or dict note holding a token as an element or a key is a NON-answer and is skipped, as the renderer
   124	        also shows it (GPT-6 Astra, v5 pass, measured; K19's "nothing is skipped" was false); a list note holding no token is
   125	        an answer and is refused (C21k); a bool note: True rc 2, False rc 1 (Astra, measured).
   126	    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
   127	    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
   128	    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
   129	    two-edit design mutant d_dfold2, killed by C25d.  Two kills the shipped ledger already supplies are ALSO rowed in isolation,
   130	    so no pin rests on the ledger's composition alone: the `entries' default (98 of 912 shipped rows carry no `entries' key;
   131	    C21j) and a latin-1 note encoding (34 frozen notes are non-ASCII, one beyond latin-1; C20b).
   132	
   133	  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
   134	  v4 passes' findings):
   135	    C1   shipped ledger, shipped baseline (md5 pin live): rc 0 and the summary line EXACTLY
   136	    C2 / C2b  an answer ON / AFTER the cutoff with a valid glyph (positive)                       -> 0 / 0
   137	    C2c / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
   138	    C3   an answer ON the cutoff with "OK" (inclusive) -- its refusal line EXACTLY                  -> 1
   139	    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
   140	    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
   141	    C6   an UNDATED answer with "N/A" -- its refusal line EXACTLY (date "(none)", no ISO clause)    -> 1
   142	    C7   an answer after the cutoff with NO `d`                                                     -> 0
   143	    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
   144	    C9   an identical copy of a frozen entry -- its refusal line EXACTLY                            -> 1
   145	    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
   146	    C11  the baseline emptied (override): every shipped off-domain answer named, the summary EXACTLY, the hint -> 1
   147	    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after / far   -> 0 / 1 / 1 / 1,
   148	         each with its summary line EXACTLY (on/after/far: within = baseline - 1)
   149	    C12s a MATCHED identity dated "2026-10-17T12:00:00" (the ISO shape opens it)                    -> 1
   150	    C13  an unreadable baseline (override)                                                          -> 2
   151	    C14  a new answer with an explicit BLANK d                                                      -> 1
   152	    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat, date, d) -> 1
   153	    C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
   154	    C17  a misshapen baseline (override; counts as strings)                                         -> 2
   155	    C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
   156	    C17c-g  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0  -> 2 each
   157	    C17h-m  the same, each of the six string positions numeric in turn: row, note sha, phase, seat, date, d     -> 2 each
   158	    C17n the same, a None date (`isinstance(v, (str, type(None)))' would pass it)                    -> 2
   159	    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
   160	    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
   161	    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
   162	         the date NAMED as not ISO                                                                  -> 1 / 1
   163	    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback, its line EXACT
   164	         with the d backslash-escaped                                                               -> 1
   165	    C20b a new answer whose NOTE is non-ASCII ("café — ✓") -- rc 1, its line EXACT (the note's UTF-8 sha)  -> 1
   166	    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
   167	         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
   168	         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
   169	    C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
   170	    C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
   171	    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
   172	    C23  a ledger that is not JSON                                                                  -> 2
   173	    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
   174	    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
   175	         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
   176	         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
   177	         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
   178	    C26  a new answer with an explicit "d": null                                                     -> 1
   179	    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
   180	    C27  DOMAIN and D_CLASS: ONE binding each and NO other way to change them -- an ast walk of every binding form and
   181	         every use (whitelisted), and the checker's EFFECTIVE DOMAIN read by importing it -- each exactly ✓ ✕ ⏸ …
   182	    C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
   183	    C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
   184	    C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
   185	         one-digit day, a `/' for the first separator, for the second -- each in its fixture baseline, so only the shape
   186	         decides                                                                                    -> 0 each
   187	  RENDERER:
   188	    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
   189	    R1b  an escapable `d` ("<b>&") renders escaped
   190	    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
   191	    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
   192	    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
   193	    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
   194	    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
   195	         "\n", "\xa0", null), the date, the note
   196	    R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
   197	    R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
   198	    R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
   199	    R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
   200	    R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
   201	         whitespace set exhausted
   202	    R1n  an explicit "d": null renders legacy with the glyph "None", not …
   203	    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
   204	         own count by exact membership, and its labels
   205	    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
   206	    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
   207	         a kill
   208	    R4   the legend carries the legacy line EXACTLY
   209	    R5   the page carries the two CSS rules the class adds, EXACTLY, and NO other rule in its style block names `legacy'
   210	  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
   211	  carry its BRANCH's own words):
   212	    W1   the shipped ledger                    -> exactly "GOOD <the summary line>" and "FAILURES 0"
   213	    W2   a new off-domain answer               -> BAD, its WHOLE output: the first line, every line of the checker's
   214	         output indented, the counter
   215	    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
   216	    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
   217	    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
   218	    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
   219	    W7   a checker that exits 7 with a TWO-line message on STDERR -> exactly "BAD ... could not run (rc 7): <its FIRST line>"
   220	         and "FAILURES 1"
   221	    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
   222	    W9   EVERY status 2-255, a stub exiting each in turn (254 runs)    -> each exactly "BAD ... could not run (rc N): <its
   223	         first line>" and the counter 1 -- the `else' partition EXHAUSTED
   224	"""
   225	import collections, copy, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile
   226	
   227	if hasattr(sys.stdout, "reconfigure"):          # this file prints glyphs (R2's strip); run it anywhere, piped or not
   228	    sys.stdout.reconfigure(encoding="utf-8")
   229	
   230	HERE = os.path.dirname(os.path.abspath(__file__))
   231	REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
   232	PIPE = os.path.join(REPO, "tools", "pipeline")
   233	CHECKER = os.environ.get("CTL_CHECKER") or os.path.join(PIPE, "check_entry_domain.py")
   234	RENDER = os.environ.get("CTL_RENDER") or os.path.join(PIPE, "gen_dashboard.py")
   235	PRE = os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")
   236	BEFORE = os.path.join(HERE, "gen_dashboard_before.py")      # HEAD's renderer at the landing, preserved
   237	#  the baseline travels WITH the checker under test: staged runs keep it beside the staged checker, and on the tree the two
   238	#  directories are the same
   239	BASELINE = os.path.join(os.path.dirname(os.path.abspath(CHECKER)), "entry_domain_baseline.json")
   240	if not os.path.exists(BASELINE):
   241	    BASELINE = os.path.join(PIPE, "entry_domain_baseline.json")
   242	LEDGER = os.path.join(PIPE, "ledger.json")
   243	sys.path.insert(0, PIPE)
   244	import stage_tokens as st  # noqa: E402
   245	
   246	T = tempfile.mkdtemp()
   247	res = []
   248	
   249	
   250	def say(label, ok, detail=""):
   251	    res.append(ok)
   252	    tag, rest = label.split(" ", 1)
   253	    print("%-4s %-76s %s  %s" % (tag, rest, "ok" if ok else "NO", detail))
   254	
   255	
   256	def wjson(name, obj):
   257	    p = os.path.join(T, name)
   258	    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
   259	    return p
   260	
   261	
   262	def pipe_copy(tag, baseline_text=None):
   263	    """a temp copy of the pipeline dir holding the checker under test, stage_tokens.py and a baseline (default: shipped)"""
   264	    d = os.path.join(T, "pipe_" + tag)
   265	    os.makedirs(d, exist_ok=True)
   266	    shutil.copy(CHECKER, os.path.join(d, "check_entry_domain.py"))
   267	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   268	    b = os.path.join(d, "entry_domain_baseline.json")
   269	    if baseline_text is None:
   270	        shutil.copy(BASELINE, b)
   271	    else:
   272	        io.open(b, "w", encoding="utf-8", newline="").write(baseline_text)
   273	    return os.path.join(d, "check_entry_domain.py")
   274	
   275	
   276	def run_checker(ledger_path, baseline_path=None, checker=None):
   277	    #  NO PYTHONIOENCODING: the precommit sets none, so the checker must survive a cp1252 pipe (Fable 5.1, pass 2)
   278	    env = dict(os.environ, GXLEDGER=ledger_path)
   279	    for k in ("GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
   280	        env.pop(k, None)
   281	    if baseline_path is not None:
   282	        env["GXDOMAIN_BASELINE"] = baseline_path
   283	    r = subprocess.run([sys.executable, checker or DEFAULT_CHECKER], capture_output=True, env=env)
   284	    out = (r.stdout + r.stderr).decode("cp1252", "replace")
   285	    return r.returncode, out.strip().splitlines()
   286	
   287	
   288	DEFAULT_CHECKER = pipe_copy("default")          # the checker under test, beside the SHIPPED baseline (md5 pin live)
   289	L0 = json.load(io.open(LEDGER, encoding="utf-8"))
   290	ROW0 = L0["rows"][0]["id"]
   291	N_OFF = sum(1 for r in L0["rows"] for x in r.get("entries", [])
   292	            if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…") and st.is_answer(x))
   293	
   294	
   295	def with_entries(entries, ledger=None):
   296	    L = copy.deepcopy(ledger or L0)
   297	    for row, e in entries:
   298	        for r in L["rows"]:
   299	            if r["id"] == row:
   300	                r.setdefault("entries", []).append(e)
   301	    return wjson("l_%d.json" % len(res), L)
   302	
   303	
   304	def ans(date, **kw):
   305	    e = {"phase": "review", "seat": "grok", "note": "a control entry"}
   306	    if date is not None:
   307	        e["date"] = date
   308	    e.update(kw)
   309	    return e
   310	
   311	
   312	def sha16(note):
   313	    return hashlib.sha1(str(note or "").encode("utf-8")).hexdigest()[:16]
   314	
   315	
   316	WHY_CUT = "dated on or after the cutoff 2026-10-17"
   317	WHY_CEIL = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
   318	WHY_ISO = "; its date is not ISO YYYY-MM-DD"
   319	
   320	
   321	def offline(row, e, why):
   322	    """the WHOLE refusal line the checker must print for entry e of row -- identifiers in their order, then the reason
   323	    (v4 read only the count of lines, so a reason replaced or row and phase swapped passed -- Fable 5.1, GPT-6 Astra, v4 pass)"""
   324	    dt = e.get("date")
   325	    dt = dt if isinstance(dt, str) else ("" if dt is None else repr(dt))
   326	    return "OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s" % (
   327	        row, e.get("phase") or "", e.get("seat") or "", dt or "(none)", str(e["d"]), sha16(e.get("note")), why)
   328	
   329	
   330	def cp(s):
   331	    """what the checker's cp1252 stdout, reconfigured errors="backslashreplace", carries for s -- as run_checker decodes it"""
   332	    return s.encode("cp1252", "backslashreplace").decode("cp1252")
   333	
   334	
   335	def summary_line(n_cur, n_within, n_base):
   336	    return ("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff 2026-10-17 inclusive"
   337	            % (n_cur, n_within, n_base))
   338	
   339	
   340	def ident(row, e):
   341	    return [row, e.get("phase") or "", e.get("seat") or "", e.get("date") if isinstance(e.get("date"), str) else "",
   342	            str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]
   343	
   344	
   345	print("# dashokclass controls (v6) -- checker %s | renderer %s | precommit %s | baseline %s"
   346	      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
   347	         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
   348	# ------------------------------------------------------------------ the checker
   349	rc, out = run_checker(LEDGER)
   350	first = out[0] if out else ""
   351	#  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
   352	#  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
   353	#  v5: the WHOLE line -- "inclusive" dropped from it passed all 72 v4 controls (Fable 5.1, v4 pass)
   354	#  v6: and ALONE -- the hint printed on a clean run passed all 96 v5 controls
   355	say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY, and the only line",
   356	    rc == 0 and out == [summary_line(N_OFF, N_OFF, N_OFF)], "rc %d: %d lines; %s" % (rc, len(out), first))
   357	for lab, ent, want in [
   358	    ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
   359	    ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
   360	    ("C3 ON the cutoff, d OK (inclusive)", ans("2026-10-17", d="OK"), 1),
   361	    ("C4 AFTER the cutoff, d OK", ans("2026-10-18", d="OK"), 1),
   362	    ("C5 a new answer BEFORE the cutoff, d OK (back-dated)", ans("2026-09-01", d="OK", seat="minimax"), 1),
   363	    ("C6 undated, d N/A", ans(None, d="N/A"), 1),
   364	    ("C7 after the cutoff, NO d", ans("2026-10-18"), 0),
   365	    ("C8 a HELD marker after the cutoff, d HELD", ans("2026-10-18", d="HELD", note=st.HELD + " grok] waiting"), 0),
   366	    ("C14 a new answer with an explicit BLANK d", ans("2026-10-10", d=""), 1),
   367	    ('C19a a new answer dated "10/18/2026", d OK', ans("10/18/2026", d="OK"), 1),
   368	    ("C19b a new answer with a NUMERIC date, d OK", ans(20261018, d="OK"), 1),
   369	    ("C20 a new answer with a non-ASCII d (cp1252 stdout, no traceback)", ans("2026-10-18", d="✗"), 1),
   370	    #  an explicit "d": null is PRESENT and off-domain -- `if x.get("d") is None` would treat it as missing (Fable 5.1, v3 pass)
   371	    ("C26 a new answer with an explicit null d", ans("2026-10-10", d=None), 1),
   372	    #  v5: a LIST d -- the key takes str() of d; without it the Counter raises on an unhashable key (Fable 5.1, v4 pass)
   373	    ("C26b a new answer whose d is a LIST", ans("2026-10-10", d=["OK"]), 1),
   374	    #  v5: a PADDED glyph is outside the four for the checker as for the renderer (R1h) -- `str(d).strip() in DOMAIN` passed
   375	    #  all 72 v4 controls (Fable 5.1, Grok 4.7, v4 pass)
   376	    ("C28 a new answer BEFORE the cutoff with a padded glyph ' ✓'", ans("2026-10-10", d=" ✓"), 1),
   377	    #  v6: the OTHER end -- `str(x["d"]).rstrip() in DOMAIN' passed all 96 v5 controls (GPT-6 Astra, v5 pass)
   378	    ("C28b a new answer BEFORE the cutoff with a glyph padded at its END '✓ '", ans("2026-10-10", d="✓ "), 1),
   379	    #  v6: a NON-ASCII note -- its sha is over the note's UTF-8; a latin-1 encode raises (or rehashes) on it (GLM 5.3, v5 pass)
   380	    ("C20b a new answer whose note is non-ASCII", ans("2026-10-10", d="OK", note="café — ✓"), 1),
   381	    #  v6: no phase, no seat -- each keys and prints as "" ; dropping the `or ""' printed "None" and passed all 96 v5 controls
   382	    #  (GLM 5.3, v5 pass, measured)
   383	    ("C29 a new answer with no phase and no seat", {"date": "2026-10-10", "d": "OK", "note": "no phase or seat"}, 1),
   384	    #  v6: a LIST note holding no token is an ANSWER (is_answer finds no token in it) and is refused, never skipped; a
   385	    #  mutant dropping the str() before the hash raised on it instead (Fable 5.1 measured rc 1 on the v4 pass)
   386	    ("C21k a new answer whose note is a list holding no token", ans("2026-10-10", d="OK", note=["a list note"]), 1),
   387	]:
   388	    rc, out = run_checker(with_entries([(ROW0, ent)]))
   389	    tb = any("Traceback" in l for l in out)
   390	    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
   391	    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
   392	    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
   393	    #  v5: the WHOLE refusal line for C3 (the cutoff reason), C6 (an undated entry: "(none)", no ISO clause) and C19a (the
   394	    #  ISO clause) -- v4 read only rc and the line count (Fable 5.1, GPT-6 Astra, v4 pass)
   395	    #  v6: also C20 (its d backslash-escaped by the cp1252 reconfigure -- "replace" printed `?' and passed all 96 v5
   396	    #  controls), C20b, C29 and C21k
   397	    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO, "C20": WHY_CUT, "C20b": WHY_CEIL, "C29": WHY_CEIL,
   398	                 "C21k": WHY_CEIL}.get(lab.split()[0])
   399	    offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   400	    exact = exact_why is None or offl == [cp(offline(ROW0, ent, exact_why))]
   401	    say(lab, rc == want and not tb and why and exact, "rc %d (want %d)%s%s%s" % (
   402	        rc, want, " TRACEBACK" if tb else "", "" if why else " REASON NOT NAMED",
   403	        "" if exact else " LINE NOT EXACT: %r" % (offl[:1],)))
   404	#  C2c/C2d ISOLATED (GPT-6 Astra, v3 pass): the shipped ledger already carries 21 ⏸ and 35 … answers, so dropping either glyph
   405	#  from DOMAIN reddened the v3 rows without their own entry; a ledger holding ONLY the fixture entry makes each its own witness
   406	for lab, ent in (("C2c AFTER the cutoff, d ⏸, in a ledger holding only it (positive)", ans("2026-10-18", d="⏸")),
   407	                 ("C2d AFTER the cutoff, d …, in a ledger holding only it (positive)", ans("2026-10-18", d="…"))):
   408	    rc, out = run_checker(wjson("l_iso_%d.json" % len(res), {"rows": [{"id": "ctliso", "entries": [ent]}]}))
   409	    say(lab, rc == 0, "rc %d" % rc)
   410	#  C24 ISOLATED (GPT-6 Astra, v4 pass): the shipped ledger carries five off-domain NOTSEAT records, so `st.is_held(x)` for
   411	#  `not st.is_answer(x)` reddened C24 for the LEDGER's reason; a ledger holding only the record makes it its own witness
   412	rc, out = run_checker(wjson("l_iso_c24.json", {"rows": [{"id": "ctliso", "entries": [
   413	    ans("2026-10-18", d="OK", note=st.NOTSEAT + " a main-loop record")]}]}))
   414	say("C24 a non-answer RECORD (NOTSEAT) after the cutoff, d OK, in a ledger holding only it", rc == 0, "rc %d" % rc)
   415	# a frozen entry, found from the shipped baseline: copied (C9), rewritten (C10), refilled (C15), note-edited (C16), ev-edited (C22)
   416	base = [json.loads(l.rstrip(",\n")) for l in io.open(BASELINE, encoding="utf-8") if l.startswith("[\"")]
   417	k0 = base[0]
   418	
   419	
   420	def find_frozen(L):
   421	    for r in L["rows"]:
   422	        if r["id"] != k0[0]:
   423	            continue
   424	        for x in r["entries"]:
   425	            if "d" in x and ident(r["id"], x) == k0[:6]:
   426	                return x
   427	    raise SystemExit("APPARATUS FAIL: the first baseline identity is not in the shipped ledger")
   428	
   429	
   430	src = find_frozen(L0)
   431	rc, out = run_checker(with_entries([(k0[0], dict(src))]))
   432	offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   433	say("C9 an identical copy of a frozen entry (%s %s %s %s %r): its refusal line EXACTLY" % tuple(k0[:5]),
   434	    rc == 1 and offl == [offline(k0[0], src, WHY_CEIL)], "rc %d; %r" % (rc, offl[:1]))
   435	L = copy.deepcopy(L0); find_frozen(L)["d"] = "✓"
   436	rc, out = run_checker(wjson("l_rewrite.json", L))
   437	say("C10 a frozen entry rewritten to a glyph", rc == 0, "rc %d" % rc)
   438	refill = dict(src); refill["note"] = "a different answer reusing the converted entry's slot"
   439	rc, out = run_checker(with_entries([(k0[0], refill)], ledger=L))
   440	say("C15 REFILL: the converted entry's (row, phase, seat, date, d) reused", rc == 1, "rc %d" % rc)
   441	L2 = copy.deepcopy(L0); f = find_frozen(L2); f["note"] = (f.get("note") or "") + " (a later correction)"
   442	rc, out = run_checker(wjson("l_noteedit.json", L2))
   443	say("C16 a frozen entry's note edited, d left off-domain", rc == 1, "rc %d" % rc)
   444	L3 = copy.deepcopy(L0); f = find_frozen(L3); f["ev"] = (f.get("ev") or "") + " (a corrected path)"
   445	rc, out = run_checker(wjson("l_evedit.json", L3))
   446	say("C22 a frozen entry's ev edited, outside the six fields (positive)", rc == 0, "rc %d" % rc)
   447	#  C25: each key field of the FROZEN entry edited by its least visible change.  A mutant normalising one field on the ledger's
   448	#  side -- `v[:10]` on the date, `.strip()`, `.lower()` -- passed every v3 control (GPT-6 Astra, v3 pass: the date suffix)
   449	OTHER_ROW = next(r["id"] for r in L0["rows"] if r["id"] != k0[0])
   450	for tag, field, how, fn in (("a", "date", "suffixed T12:00:00", lambda v: v + "T12:00:00"),
   451	                            ("b", "date", "a trailing space", lambda v: v + " "),
   452	                            ("c", "d", "a trailing space", lambda v: v + " "),
   453	                            ("d", "d", "its case swapped", lambda v: v.swapcase()),
   454	                            ("e", "note", "a trailing space", lambda v: v + " "),
   455	                            ("f", "note", "its case swapped", lambda v: v.swapcase()),
   456	                            ("g", "seat", "a trailing space", lambda v: v + " "),
   457	                            ("h", "seat", "upper-cased", lambda v: v.upper()),
   458	                            ("i", "phase", "a trailing space", lambda v: v + " "),
   459	                            ("j", "phase", "upper-cased", lambda v: v.upper())):
   460	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   461	    assert fn(fe[field]) != fe[field], (tag, field)
   462	    fe[field] = fn(fe[field])
   463	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   464	    say("C25%s a frozen entry's %s, %s" % (tag, field, how), rc == 1, "rc %d" % rc)
   465	Le = copy.deepcopy(L0); fe = find_frozen(Le)
   466	for r in Le["rows"]:
   467	    if r["id"] == k0[0]:
   468	        r["entries"] = [x for x in r["entries"] if x is not fe]
   469	    if r["id"] == OTHER_ROW:
   470	        r.setdefault("entries", []).append(fe)
   471	rc, out = run_checker(wjson("l_key_k.json", Le))
   472	say("C25k a frozen entry moved to another row (%s)" % OTHER_ROW, rc == 1, "rc %d" % rc)
   473	#  v5: the LEADING end of every field, and the row id at both ends -- `.lstrip()` on the date, d, seat, phase or note, and
   474	#  `str(r.get("id")).strip()`, each passed all 72 v4 controls, which edited only the trailing end (Fable 5.1, Grok 4.7, GPT-6
   475	#  Astra, v4 pass)
   476	
   477	
   478	def moved_to(new_id):
   479	    Lm = copy.deepcopy(L0); fm = find_frozen(Lm)
   480	    for r in Lm["rows"]:
   481	        if r["id"] == k0[0]:
   482	            r["entries"] = [x for x in r["entries"] if x is not fm]
   483	    Lm["rows"].append({"id": new_id, "title": "row id control", "sev": "LOW", "state": "open", "commits": "", "entries": [fm]})
   484	    return Lm
   485	
   486	
   487	rc, out = run_checker(wjson("l_key_l.json", moved_to(k0[0] + " ")))
   488	say("C25l a frozen entry moved to a row whose id has a TRAILING space", rc == 1, "rc %d" % rc)
   489	for tag, field in (("m", "date"), ("n", "d"), ("o", "note"), ("p", "seat"), ("q", "phase")):
   490	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   491	    fe[field] = " " + fe[field]
   492	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   493	    say("C25%s a frozen entry's %s with a LEADING space" % (tag, field), rc == 1, "rc %d" % rc)
   494	rc, out = run_checker(wjson("l_key_r.json", moved_to(" " + k0[0])))
   495	say("C25r a frozen entry moved to a row whose id has a LEADING space", rc == 1, "rc %d" % rc)
   496	rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
   497	nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
   498	#  and the SUMMARY line on this dirty ledger: it was pinned only on the clean one, where "passes" and "entries" agree, so
   499	#  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
   500	s11 = summary_line(N_OFF, 0, 0)
   501	f11 = out[0] if out else ""
   502	#  v6: the hint WHOLE -- a false "all records need classification" passed the v5 prefix test (GPT-6 Astra, v5 pass) -- and the
   503	#  output exactly the summary, one line per refusal, the hint
   504	HINT = cp("  -> give each a `d` from ✓ ✕ ⏸ … (or omit `d`, which renders as …); a non-answer record is exempt").strip()
   505	hint = bool(out) and out[-1].strip() == HINT
   506	say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint WHOLE",
   507	    rc == 1 and nb == N_OFF and f11 == s11 and hint and len(out) == N_OFF + 2, "rc %d, %d of %d named, %d lines; summary %s; hint %s"
   508	    % (rc, nb, N_OFF, len(out), "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else repr(out[-1][:90] if out else "")))
   509	# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
   510	#  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
   511	for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
   512	                      ("far", "2027-01-01", 1)):
   513	    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
   514	    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
   515	    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   516	    #  v5: the summary EXACTLY -- here the fixture baseline holds N_OFF + 1 and a refused entry leaves N_OFF within, so the
   517	    #  baseline number differs from the within-count; C1 and C11 cannot tell them apart (1356/1356, 0/0), and printing the
   518	    #  within-count there passed all 72 v4 controls (Fable 5.1, v4 pass)
   519	    s12 = summary_line(N_OFF + 1, N_OFF + 1 if want == 0 else N_OFF, N_OFF + 1)
   520	    f12 = out[0] if out else ""
   521	    say("C12 cutoff isolated: a FROZEN identity dated %s (%s), the summary EXACTLY" % (dt, tag), rc == want and f12 == s12,
   522	        "rc %d (want %d); summary %s" % (rc, want, "ok" if f12 == s12 else repr(f12[:100])))
   523	#  C12s: a MATCHED identity whose date the ISO shape OPENS -- `^...$' on the shape refused nothing and passed all 72 v4
   524	#  controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass); the checker reads the first ten characters
   525	e = ans("2026-10-17T12:00:00", d="OK", seat="kimi", note="cutoff isolation suffixed")
   526	fb = wjson("b_cut_suffixed.json", base + [ident(ROW0, e) + [1]])
   527	rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   528	say("C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00", rc == 1, "rc %d (want 1)" % rc)
   529	#  C12w (v6): the ISO SHAPE's widths and separators -- `\d{1,2}' for the month passed all 96 v5 controls, reading
   530	#  "2026-9-1" as a date after the cutoff (GPT-6 Astra, v5 pass).  Each identity is FROZEN and breaks the shape in one place,
   531	#  each chosen to compare at or after the cutoff if the shape were loosened there, so only the shape decides: rc 0
   532	#  (a one-edit mutant loosens ONE separator, so each has its own row: one date breaking both would miss either alone)
   533	for tag, dt in (("year", "99999-10-18"), ("month", "2026-9-17"), ("day", "2026-10-9"), ("sep1", "2026/10-18"),
   534	                ("sep2", "2026-10/18")):
   535	    e = ans(dt, d="OK", seat="kimi", note="iso shape " + tag)
   536	    fb = wjson("b_cut_w_%s.json" % tag, base + [ident(ROW0, e) + [1]])
   537	    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   538	    say("C12w the ISO shape's %s: a FROZEN identity dated %s is not read as a date" % (tag, dt), rc == 0, "rc %d (want 0)" % rc)
   539	rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
   540	say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
   541	#  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
   542	#  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
   543	#  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
   544	import ast  # noqa: E402
   545	#  v5 counted the Name stores of each name; v6 walks EVERY binding form and EVERY use.  `globals()["DOMAIN"] = ...' and
   546	#  `D_CLASS.update(ZXQ="ok")' each passed all 96 v5 controls -- the first is no Name store, the second mutates the dict
   547	#  without rebinding it (GLM 5.3, GPT-6 Astra, v5 pass, measured).  So: exactly one binding, a module-level assignment of a
   548	#  literal; no other binding form of the name (a store or delete, a global or nonlocal, an import alias, a def or class, an
   549	#  except or match name, a parameter, an attribute or subscript store keyed by it); no call to the builtins that rebind by
   550	#  name or by string (globals, vars, locals, setattr, delattr, exec, eval, compile, __import__) and no __dict__ / __globals__;
   551	#  and every USE of the name on a whitelist -- DOMAIN only in `in' / `not in' and as `" ".join(...)''s argument, D_CLASS only
   552	#  as `D_CLASS.get(...)' and in `in' / `not in'.  The checker is import-safe, so its EFFECTIVE DOMAIN is also read by importing
   553	#  it; the renderer renders on import, so it is read by the walk alone.
   554	BANNED = {"globals", "vars", "locals", "setattr", "delattr", "exec", "eval", "compile", "__import__"}
   555	
   556	
   557	def walk_name(path, name, use_ok):
   558	    tree = ast.parse(io.open(path, encoding="utf-8").read())
   559	    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
   560	    probs = []
   561	    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
   562	    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
   563	           and n.targets[0].id == name]
   564	    if len(stores) != 1 or len(top) != 1:
   565	        probs.append("%d stores, %d module-level assignments" % (len(stores), len(top)))
   566	    for n in ast.walk(tree):
   567	        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Del):
   568	            probs.append("del")
   569	        elif isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
   570	            probs.append("global/nonlocal")
   571	        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split(".")[0]) == name for a in n.names):
   572	            probs.append("import alias")
   573	        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
   574	            probs.append("def/class")
   575	        elif isinstance(n, ast.ExceptHandler) and n.name == name:
   576	            probs.append("except name")
   577	        elif isinstance(n, ast.arg) and n.arg == name:
   578	            probs.append("parameter")
   579	        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == name:
   580	            probs.append("match name")
   581	        elif isinstance(n, ast.Attribute) and n.attr == name and not isinstance(n.ctx, ast.Load):
   582	            probs.append("attribute store")
   583	        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load) and isinstance(n.slice, ast.Constant)
   584	              and n.slice.value == name):
   585	            probs.append("subscript store keyed by the name")
   586	        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
   587	            probs.append("call to " + n.func.id)
   588	        elif isinstance(n, ast.Attribute) and n.attr in ("__dict__", "__globals__"):
   589	            probs.append(n.attr)
   590	        elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
   591	            probs.append("a use at line %d" % n.lineno)
   592	    return (ast.literal_eval(top[0].value) if len(top) == 1 else None), probs
   593	
   594	
   595	def in_compare(n, parent):
   596	    p = parent.get(n)
   597	    return (isinstance(p, ast.Compare) and n in p.comparators
   598	            and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))
   599	
   600	
   601	def dom_use(n, parent):
   602	    p = parent.get(n)
   603	    return in_compare(n, parent) or (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
   604	                                     and p.func.attr == "join" and isinstance(p.func.value, ast.Constant))
   605	
   606	
   607	def dcls_use(n, parent):
   608	    p = parent.get(n)
   609	    return in_compare(n, parent) or (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
   610	                                     and parent.get(p).func is p)
   611	
   612	
   613	dom, dprobs = walk_name(CHECKER, "DOMAIN", dom_use)
   614	dcls, cprobs = walk_name(RENDER, "D_CLASS", dcls_use)
   615	r_imp = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import check_entry_domain as c; "
   616	                        "print(ascii(c.DOMAIN))", os.path.dirname(DEFAULT_CHECKER)], capture_output=True, text=True)
   617	try:
   618	    eff = ast.literal_eval(r_imp.stdout.strip()) if r_imp.returncode == 0 else None
   619	except (ValueError, SyntaxError):
   620	    eff = None
   621	four = ("✓", "✕", "⏸", "…")
   622	say("C27 ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ …",
   623	    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four)
   624	    and not dprobs and not cprobs and isinstance(eff, tuple) and sorted(eff) == sorted(four),
   625	    "DOMAIN %r %s | effective %r | D_CLASS keys %r %s" % (dom, dprobs or "", eff, sorted(dcls) if isinstance(dcls, dict) else dcls,
   626	                                                          cprobs or ""))
   627	rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
   628	say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
   629	#  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
   630	#  nothing pinned the sum -- GPT-6 Astra and GLM 5.3)
   631	k2 = next(k for k in base if k[6] >= 2)
   632	split = [k for k in base if k is not k2] + [k2[:6] + [1], k2[:6] + [k2[6] - 1]]
   633	rc, out = run_checker(LEDGER, wjson("b_split.json", split))
   634	say("C17b a key split across two baseline rows sums (%s %s %s %s %r x%d)" % (tuple(k2[:5]) + (k2[6],)), rc == 0, "rc %d" % rc)
   635	#  v5: each clause of the baseline row test at its own edge, one misshapen row appended to the shipped baseline -- `len(k) >=
   636	#  7', `isinstance(k[6], int)' (a bool is an int), `k[6] != 0', and the string test narrowed to five fields each passed all 72
   637	#  v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   638	kx = base[0]
   639	for tag, row_, how in (("c", kx[:6] + [1, "extra"], "eight fields"), ("d", kx[:6] + [True], "a count of true"),
   640	                       ("e", kx[:6] + [-1], "a count of -1"), ("f", kx[:6] + [0], "a count of 0"),
   641	                       ("g", kx[:6] + [1.0], "a count of 1.0"), ("h", [5] + kx[1:6] + [1], "a numeric first field"),
   642	                       ("i", kx[:5] + [5, 1], "a numeric note sha"),
   643	                       #  v6: the MIDDLE positions -- `for v in k[::5]' checked only the first and the sixth and passed all
   644	                       #  96 v5 controls (GPT-6 Astra, v5 pass)
   645	                       ("j", kx[:1] + [5] + kx[2:6] + [1], "a numeric phase"), ("k", kx[:2] + [5] + kx[3:6] + [1], "a numeric seat"),
   646	                       ("l", kx[:3] + [5] + kx[4:6] + [1], "a numeric date"), ("m", kx[:4] + [5] + kx[5:6] + [1], "a numeric d"),
   647	                       #  v6: a None field -- `isinstance(v, (str, type(None)))' passed all 96 v5 controls (Fable 5.1, v5 pass)
   648	                       ("n", kx[:3] + [None] + kx[4:6] + [1], "a None date")):
   649	    rc, out = run_checker(LEDGER, wjson("b_row_%s.json" % tag, base + [row_]))
   650	    tb = any("Traceback" in l for l in out)
   651	    say("C17%s a misshapen baseline row: %s (override)" % (tag, how), rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   652	txt = io.open(BASELINE, encoding="utf-8").read()
   653	lines = txt.split("\n")
   654	lines[1] = lines[1].replace('"y"', '"Y"', 1) if '"y"' in lines[1] else lines[1].replace(", 1]", ", 2]", 1)
   655	rc_mod, out_mod = run_checker(LEDGER, checker=pipe_copy("md5mod", "\n".join(lines)))
   656	rc_same, _ = run_checker(LEDGER, checker=pipe_copy("md5same", txt))
   657	say("C18 md5 pin: one baseline line changed -> 2, unchanged -> 0", rc_mod == 2 and rc_same == 0,
   658	    "changed rc %d, unchanged rc %d" % (rc_mod, rc_same))
   659	#  C18b: the same bytes checked out with CRLF -- what a fresh clone under core.autocrlf=true writes (measured 06a3ffc6 ->
   660	#  89d1d370 raw at the adjudication pass) -- must pass the pin, which folds line endings
   661	rc_crlf, _ = run_checker(LEDGER, checker=pipe_copy("md5crlf", txt.replace("\n", "\r\n")))
   662	say("C18b md5 pin: the baseline checked out with CRLF line endings -> 0", rc_crlf == 0, "rc %d" % rc_crlf)
   663	for lab, obj in (('C21a a misshapen ledger: {"rows": null}', {"rows": None}),
   664	                 ("C21b a misshapen ledger: a row that is not an object", {"rows": [42]}),
   665	                 ("C21c a misshapen ledger: a list, not an object", []),
   666	                 #  each of these walked as EMPTY and passed v3, rc 0 (GPT-6 Astra, v3 pass)
   667	                 ('C21d a misshapen ledger: {"rows": {}}', {"rows": {}}),
   668	                 ("C21e a misshapen ledger: an entry that is a string", {"rows": [{"id": "x", "entries": ["bogus"]}]}),
   669	                 ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]}),
   670	                 #  v5: `rows' ABSENT -- `ledger.get("rows", [])' would walk it as empty (Grok 4.7, GLM 5.3, v4 pass)
   671	                 ("C21i a misshapen ledger: no rows key -- {}", {}),
   672	                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []})):
   673	    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
   674	    tb = any("Traceback" in l for l in out)
   675	    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   676	rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
   677	say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
   678	#  C21j (v6): a row with NO entries key is an empty row, not a misshapen one -- `r.get("entries")' at either site turns it
   679	#  into rc 2; the shipped ledger kills that today (98 of 912 rows carry no `entries'), so it is rowed in isolation (GLM 5.3,
   680	#  v5 pass)
   681	rc, out = run_checker(wjson("l_noentries.json", {"rows": [{"id": "ctlnoent"}, {"id": "ctlent", "entries": [ans("2026-10-18", d="✓")]}]}))
   682	say("C21j a row with no entries key beside a valid one", rc == 0, "rc %d" % rc)
   683	#  C21h: the shape check passes it, then is_answer raises on a NON-STRING note -- the one input that still reaches the walk's
   684	#  except-arm, so that arm stays a measured rc 2 rather than dead code
   685	rc, out = run_checker(wjson("l_shape_note.json", {"rows": [{"id": "x", "entries": [
   686	    {"phase": "review", "seat": "grok", "date": "2026-10-18", "d": "OK", "note": 5}]}]}))
   687	tb = any("Traceback" in l for l in out)
   688	say("C21h an entry whose note is a number (it raises inside is_answer)", rc == 2 and not tb,
   689	    "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   690	pj = os.path.join(T, "l_notjson.json")
   691	io.open(pj, "w", encoding="utf-8").write("{ this is not json")
   692	rc, out = run_checker(pj)
   693	tb = any("Traceback" in l for l in out)
   694	say("C23 an unreadable ledger (not JSON)", rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   695	
   696	# ------------------------------------------------------------------ the renderer
   697	SEATS = [s["id"] for s in L0["seats"]]
   698	EXPECT = {   # seat -> (entry fields, class, glyph)
   699	    "fable5": ({"d": "✓"}, "ok", "✓"),
   700	    "opus5": ({"d": "OK"}, "legacy", "OK"),
   701	    "codex": ({}, "pend", "…"),
   702	    "agy": ({"d": ""}, "legacy", "?"),
   703	    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
   704	    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", "∅"),
   705	    "glm": ({"d": "✕"}, "bad", "✕"),
   706	    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
   707	    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
   708	}
   709	assert set(EXPECT) == set(SEATS), SEATS
   710	#  the legacy cell's WHOLE tooltip: the class line, the date, the note -- joined and escaped exactly as cell() does.  A prefix
   711	#  check let "(not approval, not a seat failure)" return after the checked words (GPT-6 Astra and GLM 5.3, adjudication pass)
   712	LEGACY_TIP = html.escape("legacy -- verdict unclassified: d = 'OK' is outside ✓ ✕ ⏸ …; read the note for the outcome"
   713	                         " — 2026-10-16 — a renderer control", quote=True)
   714	LEGEND_LINE = ('<span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside '
   715	               '✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = '
   716	               'an explicit blank)</span>')
   717	REC_NOTE = st.NOTSEAT + " a record beside the answer"
   718	REF_A = {"phase": "research", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": st.RE_READ + " refused re-read control"}
   719	FX = copy.deepcopy(L0)
   720	ents = []
   721	for s in SEATS:
   722	    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
   723	    e.update(EXPECT[s][0])
   724	    ents.append(e)
   725	FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents},
   726	              {"id": "ctlesc", "title": "escape control row", "sev": "LOW", "state": "open", "commits": "",
   727	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "<b>&", "note": "escape control"}]},
   728	              #  a whitespace-only `d` must show `?`, never an invisible glyph (0 such values in the ledger; Fable 5.1,
   729	              #  adjudication pass, measured `{e(d) if d else "?"}` passing every v2 control)
   730	              {"id": "ctlws", "title": "whitespace control row", "sev": "LOW", "state": "open", "commits": "",
   731	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"},
   732	                           #  a TAB-only d: `.strip(" ")` would keep it invisible (Grok 4.7, v3 pass)
   733	                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"},
   734	                           #  v5: a newline and an NBSP -- `.strip(" \t")' kept both invisible and passed all 72 v4
   735	                           #  controls (Fable 5.1, Grok 4.7, v4 pass)
   736	                           {"phase": "assess", "seat": "opus5", "date": "2026-10-16", "d": "\n", "note": "newline control"},
   737	                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "\xa0", "note": "nbsp control"}]},
   738	              #  v5: an explicit null d renders legacy with the glyph None -- a renderer that treats null as missing (…) or
   739	              #  skips its class line passed all 72 v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   740	              {"id": "ctlnull", "title": "null control row", "sev": "LOW", "state": "open", "commits": "",
   741	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": None, "note": "null control"}]},
   742	              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
   743	              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
   744	              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
   745	               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
   746	                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
   747	              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
   748	              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
   749	              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
   750	              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
   751	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"},
   752	                           #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
   753	                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
   754	              #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
   755	              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while 649 and 642 of the 670
   756	              #  shipped legacy cells lost the class line (GPT-6 Astra, v5 pass)
   757	              #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
   758	              #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
   759	              {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
   760	               "entries": [{"phase": "assess", "seat": "fable5", "d": "BARE"}]},
   761	              {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
   762	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
   763	                            "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
   764	              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
   765	               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
   766	#  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
   767	#  `str.strip()' removes, and `.strip(" \t\n\xa0")' passed all 96 v5 controls but R3's presence pin (Fable 5.1, v5 pass)
   768	WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
   769	for i in range(0, len(WS), len(SEATS)):
   770	    FX["rows"].append({"id": "ctlws%02d" % (i // len(SEATS)), "title": "whitespace set control row", "sev": "LOW", "state": "open",
   771	                       "commits": "", "entries": [{"phase": "assess", "seat": SEATS[j], "date": "2026-10-16", "d": ch,
   772	                                                   "note": "ws control U+%04X" % ord(ch)}
   773	                                                  for j, ch in enumerate(WS[i:i + len(SEATS)])]})
   774	fx_path = wjson("fx_render.json", FX)
   775	
   776	
   777	def render(gen, ledger_path, tag):
   778	    d = os.path.join(T, "r_" + tag)
   779	    os.makedirs(d, exist_ok=True)
   780	    shutil.copy(gen, os.path.join(d, "gen_dashboard.py"))
   781	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   782	    out = os.path.join(d, "out.html")
   783	    env = dict(os.environ, GXLEDGER=ledger_path, PYTHONIOENCODING="utf-8")
   784	    r = subprocess.run([sys.executable, os.path.join(d, "gen_dashboard.py"), "--out", out], capture_output=True, text=True,
   785	                       encoding="utf-8", env=env)
   786	    return io.open(out, encoding="utf-8").read() if r.returncode == 0 and os.path.exists(out) else None
   787	
   788	
   789	CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
   790	             "padded glyph control", "tab control", "newline control", "nbsp control", "null control", "padded trailing control",
   791	             "optional fields control", "BARE", "ws control U+")
   792	
   793	
   794	def cells(html_text):
   795	    got = []
   796	    for m in re.finditer(r'<td class="c ([a-z]+)">(.*?)</td>', html_text, re.S):
   797	        if m.group(1) == "none":
   798	            continue
   799	        g = re.search(r'<span class="g">(.*?)</span>', m.group(2))
   800	        tip = re.search(r'<span class="tip">(.*?)</span>', m.group(2), re.S)
   801	        got.append((m.group(1), g.group(1) if g else None, tip.group(1) if tip else ""))
   802	    return got
   803	
   804	
   805	def r1(html_text):
   806	    if html_text is None:
   807	        return False, "render FAILED (a crash is not a kill)"
   808	    got = [c for c in cells(html_text) if not any(k in c[2] for k in CTL_OTHER)]   # the control row's nine, in seat order
   809	    want = [(EXPECT[s][1], EXPECT[s][2]) for s in SEATS]
   810	    head = got[:len(want)]
   811	    bad = [(s, g[:2], w) for s, g, w in zip(SEATS, head, want) if (g[0], g[1]) != w]
   812	    legacy_tip = head[SEATS.index("opus5")][2] if len(head) == len(want) else ""
   813	    tip_ok = legacy_tip == LEGACY_TIP
   814	    return (len(head) == len(want) and not bad and tip_ok), ("%d cells; mismatches %s; legacy tip %s" % (
   815	        len(head), bad[:3], "exact" if tip_ok else "WRONG: %r" % legacy_tip[:120]))
   816	
   817	
   818	def r1b(html_text):
   819	    if html_text is None:
   820	        return False, "render FAILED (a crash is not a kill)"
   821	    got = [c for c in cells(html_text) if "escape control" in c[2]]
   822	    esc = got[0] if got else ("", "", "")
   823	    return (esc[0] == "legacy" and esc[1] == "&lt;b&gt;&amp;"), "escape cell %r" % (esc[:2],)
   824	
   825	
   826	def r1d(html_text):
   827	    if html_text is None:
   828	        return False, "render FAILED (a crash is not a kill)"
   829	    got = [c for c in cells(html_text) if any(k in c[2] for k in ("whitespace control", "tab control", "newline control",
   830	                                                                    "nbsp control"))]
   831	    return (len(got) == 4 and all(c[0] == "legacy" and c[1] == "?" for c in got)), "whitespace cells %r" % ([c[:2] for c in got],)
   832	
   833	
   834	def legacy_line(d):
   835	    return "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d
   836	
   837	
   838	def r1g(html_text):
   839	    #  EVERY legacy cell, not only the "OK" one: `if cls == LEGACY` -> `if d == "OK"` passed every v3 control and drops the
   840	    #  explanation from 305 displayed cells (GPT-6 Astra, v3 pass)
   841	    if html_text is None:
   842	        return False, "render FAILED (a crash is not a kill)"
   843	    #  the WHOLE tooltip of each simple legacy cell -- class line, date, note -- not a prefix and not one cell: `if cls ==
   844	    #  LEGACY and d == "OK"` and `... and str(d).strip()` passed all 46 v3 controls (Fable 5.1, v3 pass, measured)
   845	    want = [(note, d, html.escape(" — ".join([legacy_line(d), "2026-10-16", note]), quote=True))
   846	            for note, d in (("a renderer control", "OK"), ("a renderer control", ""), ("a renderer control", "N/A"),
   847	                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"), ("padded trailing control", "✓ "),
   848	                            ("tab control", "\t"), ("null control", None),
   849	                            #  v6: the newline and NBSP cells -- R1d checked their class and glyph only, so `if cls == LEGACY
   850	                            #  and d not in ("\n", "\xa0")' passed all 96 v5 controls (Grok 4.7, v5 pass)
   851	                            ("newline control", "\n"), ("nbsp control", "\xa0"))]
   852	    legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
   853	    missing = [(note, d) for note, d, whole in want if whole not in legacy]
   854	    return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])
   855	
   856	
   857	def r1e(html_text):
   858	    if html_text is None:
   859	        return False, "render FAILED (a crash is not a kill)"
   860	    got = [c for c in cells(html_text) if "record control answer" in c[2]]
   861	    #  v5: the WHOLE tooltip -- class line, date, note, the record line.  v4 asserted the record substring, so a class line
   862	    #  dropped from every cell with a record beside it passed all 72 v4 controls (Fable 5.1, GPT-6 Astra, v4 pass)
   863	    want = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "record control answer", "record: 2026-10-16 — " + REC_NOTE]),
   864	                       quote=True)
   865	    return (len(got) == 1 and got[0][0] == "legacy" and got[0][2] == want), "cells %d; tooltip %s" % (
   866	        len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:140] if got else ""))
   867	
   868	
   869	def r1f(html_text):
   870	    if html_text is None:
   871	        return False, "render FAILED (a crash is not a kill)"
   872	    stage = [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]
   873	    probs = st.stage_token_problems(stage)
   874	    want = html.escape(" — ".join(["EXEMPTION REFUSED BY SECTION H: " + "; ".join(probs), legacy_line("OK"), "2026-10-16",
   875	                                   REF_A["note"]]), quote=True)
   876	    got = [c for c in cells(html_text) if "refused re-read control" in c[2]]
   877	    return (bool(probs) and len(got) == 1 and got[0][2] == want), "refusals %d; cells %d; tooltip %s" % (
   878	        len(probs), len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:120] if got else ""))
   879	
   880	
   881	ha_fx = render(RENDER, fx_path, "after")
   882	ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
   883	ok, det = r1g(ha_fx); say("R1g every simple legacy cell's WHOLE tooltip, the class line for ITS d", ok, det)
   884	#  v6: both ends, and the glyph TEXT -- `html.escape(str(t).strip())' showed " ✓" as "✓" and passed all 96 v5 controls,
   885	#  which read only the class (GPT-6 Astra, v5 pass)
   886	pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
   887	padt = [c for c in cells(ha_fx or "") if "padded trailing control" in c[2]]
   888	say("R1h a ✓ padded at either end renders legacy, its glyph text exactly as written",
   889	    len(pad) == 1 and pad[0][:2] == ("legacy", " ✓") and len(padt) == 1 and padt[0][:2] == ("legacy", "✓ "),
   890	    "cells %r %r" % (pad[0][:2] if pad else None, padt[0][:2] if padt else None))
   891	opt = [c for c in cells(ha_fx or "") if "optional fields control" in c[2]]
   892	want_o = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "MANUAL", "the author did this review (shown, not hidden)",
   893	                                  "optional fields control", "evidence: regress/artifacts/x/ctl.txt"]), quote=True)
   894	say("R1o a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first",
   895	    len(opt) == 1 and opt[0][0] == "legacy" and opt[0][2] == want_o,
   896	    "cell %r; tooltip %s" % (opt[0][:2] if opt else None, "exact" if opt and opt[0][2] == want_o else "WRONG: %r" % (opt[0][2][:140] if opt else "")))
   897	#  R1p (v6): the class line ONLY on a legacy cell -- `if cls in (LEGACY, "pend")' and `if cls != "ok"' each passed all 96 v5
   898	#  controls, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend cell, 833 on HEAD's ledger (Fable 5.1, v5 pass)
   899	plain = html.escape("2026-10-16 — a renderer control", quote=True)
   900	ctl = [c for c in cells(ha_fx or "") if not any(k in c[2] for k in CTL_OTHER)][:len(SEATS)]
   901	tips = dict(zip(SEATS, [c[2] for c in ctl])) if len(ctl) == len(SEATS) else {}
   902	bad_p = [s for s in ("fable5", "codex", "glm", "deepseek") if tips.get(s) != plain]
   903	say("R1p the NON-legacy answer cells -- ok, pend, bad, hold -- carry no class line: the date and the note alone",
   904	    bool(tips) and not bad_p, "wrong: %r" % ([(s, (tips.get(s) or "")[:70]) for s in bad_p],))
   905	bare = [c for c in cells(ha_fx or "") if "BARE" in c[2]]
   906	want_b = html.escape(legacy_line("BARE"), quote=True)
   907	say("R1q a legacy answer with neither date nor note: its tooltip is the class line alone",
   908	    len(bare) == 1 and bare[0][0] == "legacy" and bare[0][2] == want_b, "cells %d: %r" % (len(bare), [c[2][:80] for c in bare]))
   909	wsc = [c for c in cells(ha_fx or "") if "ws control U+" in c[2]]
   910	wsw = {html.escape(" — ".join([legacy_line(ch), "2026-10-16", "ws control U+%04X" % ord(ch)]), quote=True) for ch in WS}
   911	wsbad = [c[2][-14:] for c in wsc if c[0] != "legacy" or c[1] != "?" or c[2] not in wsw]
   912	say("R1w every str.isspace() code point alone as d (%d) shows ? and renders legacy, each with its WHOLE tooltip" % len(WS),
   913	    len(wsc) == len(WS) == 29 and not wsbad and len({c[2] for c in wsc}) == 29,
   914	    "%d cells of %d; wrong: %r" % (len(wsc), len(WS), wsbad[:5]))
   915	ok, det = r1e(ha_fx); say("R1e an answer with a record beside it: its WHOLE tooltip", ok, det)
   916	nul = [c for c in cells(ha_fx or "") if "null control" in c[2]]
   917	say("R1n an explicit null d renders legacy with the glyph None", len(nul) == 1 and nul[0][:2] == ("legacy", "None"),
   918	    "cell %r" % (nul[0][:2],) if nul else "render FAILED or no cell")
   919	ok, det = r1f(ha_fx); say("R1f a refused exemption's line first, then the class line, exactly", ok, det)
   920	ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
   921	ok, det = r1d(ha_fx); say("R1d a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?", ok, det)
   922	low = (ha_fx or "").lower()
   923	hits = [p for p in ("not approval", "not a seat failure") if p in low]
   924	say("R1c the fixture page says neither 'not approval' nor 'not a seat failure'", ha_fx is not None and not hits,
   925	    "render %s; found %s" % ("ok" if ha_fx is not None else "FAILED", hits or "none"))
   926	leg = re.search(r'<div class="legend">(.*?)</div>', ha_fx or "", re.S)
   927	say("R4 the legend carries the legacy line EXACTLY", bool(leg) and LEGEND_LINE in leg.group(1),
   928	    "legend %s" % ("found" if leg else "MISSING"))
   929	#  R5 (v5): the two CSS rules the class adds -- `font-size:0' made every legacy glyph invisible and passed all 72 v4 controls
   930	#  (GPT-6 Astra, Fable 5.1, v4 pass)
   931	CSS = ("td.c.legacy { outline:1px dashed var(--line); outline-offset:-3px; }",
   932	       ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
   933	#  v6: and they are the ONLY rules in the style block naming `legacy' -- a later `.c.legacy .g { font-size:0; }' left both
   934	#  present and hid every legacy glyph (GPT-6 Astra, v5 pass)
   935	sty = re.search(r"<style>(.*?)</style>", ha_fx or "", re.S)
   936	leg_rules = [" ".join(m.group(0).split()) for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", sty.group(1) if sty else "")]
   937	say("R5 the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it",
   938	    ha_fx is not None and all(c in ha_fx for c in CSS) and sorted(leg_rules) == sorted(CSS),
   939	    "missing %r; legacy rules %d %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")], len(leg_rules), [r[:40] for r in leg_rules]))
   940	
   941	
   942	def census(html_text):
   943	    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html_text))
   944	    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html_text).group(1)
   945	    return c, s
   946	
   947	
   948	hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
   949	#  v6: guarded -- a renderer that crashes on the shipped ledger made census() raise, so the controls died with no tally and no
   950	#  sentinel and the mutant driver scored a KILL as INCOMPLETE (Fable 5.1, v5 pass); now R2 says NO and the run completes
   951	cb, sb = census(hb) if hb else (collections.Counter(), "")
   952	ca, sa = census(ha) if ha else (collections.Counter(), "")
   953	same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
   954	moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
   955	nums = [int(x) for x in re.findall(r"(\d+)", sa)]
   956	n_entries = sum(len(r.get("entries", [])) for r in L0["rows"])
   957	n_legacy = sum(1 for r in L0["rows"] for x in r.get("entries", []) if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…"))
   958	#  the strip's FIFTH number is checked against the ledger itself: a renderer that folded legacy into … still summed (the
   959	#  kill table measured R2 blind to that on its first run)
   960	cnt = collections.Counter()
   961	for r_ in L0["rows"]:
   962	    for x in r_.get("entries", []):
   963	        d_ = x.get("d", "…")
   964	        cnt[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
   965	#  EACH number against the ledger's own count: the v3 form checked only the total and the legacy number, so folding every
   966	#  canonical glyph into ✓ passed (GPT-6 Astra, v3 pass)
   967	sums = nums == [cnt["✓"], cnt["✕"], cnt["⏸"], cnt["…"], cnt["legacy"], n_entries] and nums[4] == n_legacy
   968	#  v5: the WHOLE strip string -- its labels too: "1397 approved" passed all 72 v4 controls (GPT-6 Astra, v4 pass)
   969	def strip_text(c, total):
   970	    return "%d✓ %d✕ %d⏸ %d… %d legacy · %d in all" % (c["✓"], c["✕"], c["⏸"], c["…"], c["legacy"], total)
   971	
   972	
   973	label_ok = sa == strip_text(cnt, n_entries)
   974	say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label)",
   975	    same and moved and sums and label_ok,
   976	    "before %s | after %s | strip '%s' | ledger %d entries, %d off-domain" % (dict(sorted(cb.items())), dict(sorted(ca.items())),
   977	                                                                          sa, n_entries, n_legacy))
   978	#  R2b (v5): the FIXTURE page's strip against the fixture's own counts, by exact membership -- its padded " ✓" and its null
   979	#  count legacy.  R2 recomputes on the shipped ledger, which holds no padded glyph, so counting " ✓" as ✓ passed all 72 v4
   980	#  controls (Fable 5.1, Grok 4.7, v4 pass)
   981	cfx = collections.Counter()
   982	for r_ in FX["rows"]:
   983	    for x in r_.get("entries", []):
   984	        d_ = x.get("d", "…")
   985	        cfx[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
   986	_, sfx = census(ha_fx) if ha_fx else (None, "")
   987	want_fx = strip_text(cfx, sum(len(r_.get("entries", [])) for r_ in FX["rows"]))
   988	say("R2b the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy)", sfx == want_fx,
   989	    "strip %r, want %r" % (sfx, want_fx))
   990	src_r = io.open(RENDER, encoding="utf-8").read()
   991	for tag, find, repl, check in (
   992	        ("ok", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")', r1),
   993	        ("pend", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")', r1),
   994	        ("noescape", '{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}', r1b)):
   995	    if src_r.count(find) != 1:
   996	        say("R3 MUTANT %s: find-text present" % tag, False, "MUTANT TEXT NOT FOUND"); continue
   997	    m = os.path.join(T, "gen_mut_%s.py" % tag)
   998	    io.open(m, "w", encoding="utf-8").write(src_r.replace(find, repl))
   999	    h = render(m, fx_path, "mut_" + tag)
  1000	    ok, det = check(h)
  1001	    say("R3 MUTANT %s renders and fails its check" % tag, h is not None and not ok, det)
  1002	
  1003	# ------------------------------------------------------------------ the wiring: precommit section Q2, failures counted
  1004	BASH = os.environ.get("BASH_EXE") or r"C:\Program Files\Git\bin\bash.exe"
  1005	txt_pre = io.open(PRE, encoding="utf-8").read()
  1006	a, b = txt_pre.find('say ""; say "Q2.'), txt_pre.find("#  ---- R ----")
  1007	if a < 0 or b < a or not os.path.exists(BASH):
  1008	    say("W0 precommit Q2 block extracted and a git-bash found", False, "a=%d b=%d bash=%s" % (a, b, BASH))
  1009	else:
  1010	    blk = os.path.join(T, "q2_block.sh")
  1011	    io.open(blk, "w", encoding="utf-8", newline="\n").write(
  1012	        'say () { :; }\nfails=0\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n'
  1013	        '_HERE="$1"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\n')
  1014	    def w_tools(tag, ledger_path, baseline_text=None, nochecker=False, stub=None):
  1015	        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
  1016	        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
  1017	        d = os.path.join(T, "w_" + tag)
  1018	        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
  1019	        if stub is not None:
  1020	            io.open(os.path.join(d, "pipeline", "check_entry_domain.py"), "w", encoding="utf-8").write(stub)
  1021	        elif not nochecker:
  1022	            shutil.copy(CHECKER, os.path.join(d, "pipeline", "check_entry_domain.py"))
  1023	        shutil.copy(os.path.join(PIPE, "stage_tokens.py"), os.path.join(d, "pipeline"))
  1024	        shutil.copy(ledger_path, os.path.join(d, "pipeline", "ledger.json"))
  1025	        if baseline_text is None:
  1026	            shutil.copy(BASELINE, os.path.join(d, "pipeline", "entry_domain_baseline.json"))
  1027	        elif baseline_text != "<absent>":
  1028	            io.open(os.path.join(d, "pipeline", "entry_domain_baseline.json"), "w", encoding="utf-8").write(baseline_text)
  1029	        return d
  1030	    #  dated BEFORE the cutoff, so only the BASELINE decides W4: a post-cutoff entry is refused by the date rule whichever
  1031	    #  baseline is read, and the kill table measured W4 blind to the un-stripped override on its first run for that reason
  1032	    new_led = with_entries([(ROW0, ans("2026-10-10", d="OK", seat="deepseek", note="W new off-domain"))])
  1033	    permissive = wjson("b_permissive.json", base + [ident(ROW0, ans("2026-10-10", d="OK", seat="deepseek",
  1034	                                                                      note="W new off-domain")) + [1]])
  1035	    #  the FIRST LINE names which branch fired: W2 the rc-1 refusal, W3 the rc-2 apparatus line -- `-eq 1` -> `-eq 7` and a
  1036	    #  rewritten message each passed every v2 control, which tested only the BAD prefix and the counter (Fable 5.1,
  1037	    #  adjudication pass)
  1038	    for lab, tools, envx, want, wantf, msg in (
  1039	            ("W1 Q2 on the shipped ledger", w_tools("1", LEDGER), {}, "GOOD", 0, "within the frozen ceiling"),
  1040	            ("W2 Q2 with a new off-domain answer", w_tools("2", new_led), {}, "BAD", 1, "beyond the frozen legacy ceiling"),
  1041	            ("W3 Q2 with the baseline absent (rc 2 path)", w_tools("3", LEDGER, "<absent>"), {}, "BAD", 1,
  1042	             "could not run (rc 2)"),
  1043	            ("W4 Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry", w_tools("4", new_led),
  1044	             {"GXDOMAIN_BASELINE": permissive}, "BAD", 1, "beyond the frozen legacy ceiling"),
  1045	            #  the bad ledger is the block's DEFAULT; the exported GXLEDGER names the clean shipped one, so only the strip
  1046	            #  decides W5 (deleting `-u GXLEDGER` passed all 35 v2 controls -- GPT-6 Astra, adjudication pass)
  1047	            ("W5 Q2 ignores an exported GXLEDGER naming a clean ledger", w_tools("5", new_led), {"GXLEDGER": LEDGER},
  1048	             "BAD", 1, "beyond the frozen legacy ceiling"),
  1049	            #  the checker ABSENT: the missing-file branch was exercised by no v3 row, so `bad` -> `good` there passed
  1050	            #  (GPT-6 Astra, v3 pass)
  1051	            ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING"),
  1052	            #  v5: ANY status other than 0 and 1 is "could not run" -- `else' narrowed to `elif [ $_cedrc -eq 2 ]' passed all 72
  1053	            #  v4 controls, leaving rc 7 or 127 silently green (GPT-6 Astra, Fable 5.1, v4 pass).  W7's message is on STDERR,
  1054	            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given -- and
  1055	            #  the git-bash wrapper PREPENDS /mingw64/bin, /usr/bin and ~/bin to that PATH; none holds a python on this
  1056	            #  machine, and if one did W8 would fail LOUDLY (GOOD instead of BAD), never pass falsely (Fable 5.1, v5 pass)
  1057	            ("W7 Q2 with a checker that exits 7, its message on stderr",
  1058	             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB FIRST LINE\\nSTUB SECOND LINE\\n")\nsys.exit(7)\n'), {},
  1059	             "BAD", 1, "could not run (rc 7): STUB FIRST LINE"),
  1060	            ("W8 Q2 with python absent from PATH (rc 127)", w_tools("8", LEDGER),
  1061	             {"PATH": os.path.join(os.path.dirname(os.path.dirname(BASH)), "usr", "bin")}, "BAD", 1, "could not run (rc 127)")):
  1062	        env = dict(os.environ)
  1063	        for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
  1064	            env.pop(k, None)
  1065	        env.update(envx)
  1066	        r = subprocess.run([BASH, blk.replace("\\", "/"), tools.replace("\\", "/")], capture_output=True, env=env)
  1067	        outl = r.stdout.decode("cp1252", "replace").strip().splitlines()
  1068	        firstl = outl[0] if outl else ""
  1069	        fl = [l for l in outl if l.startswith("FAILURES ")]
  1070	        nf = int(fl[-1].split()[1]) if fl else -1
  1071	        #  W2's refusal must also NAME the entry to the committer: deleting Q2's `printf | sed` passed every v3 control, which
  1072	        #  read only the first line and the counter (Grok 4.7, v3 pass)
  1073	        named = (not lab.startswith("W2 ")) or any(l.strip().startswith("OFF-DOMAIN ANSWER  row") for l in outl)
  1074	        #  v6: W1 and W7 read the WHOLE output -- the apparatus branch's `head -1' -> `tail -1' passed all 96 v5 controls on
  1075	        #  one-line messages (GPT-6 Astra, v5 pass)
  1076	        whole = {"W1": ["GOOD " + summary_line(N_OFF, N_OFF, N_OFF), "FAILURES 0"],
  1077	                 "W7": ["BAD check_entry_domain.py could not run (rc 7): STUB FIRST LINE", "FAILURES 1"]}.get(lab.split()[0])
  1078	        #  v6: W2's WHOLE output -- its first line, then EVERY line of the checker's own output, indented, then the counter:
  1079	        #  Q2's `printf | sed' replaced by a constant "OFF-DOMAIN ANSWER  row ..." line passed all 96 v5 controls, which read a
  1080	        #  prefix (Grok 4.7, v5 pass).  The checker's lines come from running the checker in W2's own tools dir as Q2 does.
  1081	        if lab.split()[0] == "W2":
  1082	            e2 = subprocess.run([sys.executable, os.path.join(tools, "pipeline", "check_entry_domain.py")],
  1083	                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
  1084	            whole = (["BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one "
  1085	                      "edited):"] + ["          " + l for l in e2.stdout.decode("cp1252", "replace").splitlines()] + ["FAILURES 1"])
  1086	        named = named and (whole is None or outl == whole)
  1087	        #  v6: W2's first line EXACT -- its parenthetical dropped passed all 96 v5 controls (Fable 5.1, v5 pass)
  1088	        named = named and (lab.split()[0] != "W2" or firstl == "BAD an off-domain ledger answer is beyond the frozen legacy ceiling "
  1089	                                                           "(a new one, a copy, or an old one edited):")
  1090	        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
  1091	        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))
  1092	    #  W9 (v6): EVERY status but 0 and 1 is "could not run".  The else partition is {2..255}, EXHAUSTED in ONE bash loop over
  1093	    #  a stub that exits $W9RC: `else' -> `elif [ $_cedrc -ne 3 ]' passed all 96 v5 controls, whose W3, W7 and W8 are three
  1094	    #  statuses of 254 (Grok 4.7, v5 pass)
  1095	    w9 = w_tools("9", LEDGER, stub='import os, sys\nsys.stderr.write("STUB rc %s\\n" % os.environ["W9RC"])\n'
  1096	                                   'sys.exit(int(os.environ["W9RC"]))\n')
  1097	    loop = os.path.join(T, "q2_loop.sh")
  1098	    io.open(loop, "w", encoding="utf-8", newline="\n").write(
  1099	        'say () { :; }\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n_HERE="$1"\n'
  1100	        'for W9RC in $(seq 2 255); do export W9RC; fails=0; echo "RC $W9RC"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\ndone\n')
  1101	    env = dict(os.environ)
  1102	    for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
  1103	        env.pop(k, None)
  1104	    r = subprocess.run([BASH, loop.replace("\\", "/"), w9.replace("\\", "/")], capture_output=True, env=env)
  1105	    got9 = r.stdout.decode("cp1252", "replace").splitlines()
  1106	    want9 = []
  1107	    for n_ in range(2, 256):
  1108	        want9 += ["RC %d" % n_, "BAD check_entry_domain.py could not run (rc %d): STUB rc %d" % (n_, n_), "FAILURES 1"]
  1109	    bad9 = ([n_ for n_ in range(2, 256) if got9[3 * (n_ - 2):3 * (n_ - 1)] != want9[3 * (n_ - 2):3 * (n_ - 1)]]
  1110	            if len(got9) == len(want9) else ["%d lines of %d" % (len(got9), len(want9))])
  1111	    say("W9 Q2 with EVERY status 2-255 (254 runs of one stub): each exactly BAD 'could not run (rc N)' with its first line, "
  1112	        "the counter 1", got9 == want9, "wrong at: %r" % (bad9[:8],))
  1113	
  1114	shutil.rmtree(T, ignore_errors=True)
  1115	print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
  1116	print("DASHOKCLASS_CONTROLS_DONE")
  1117	sys.exit(0 if all(res) else 1)
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

## 5. The records this landing writes AT COMMIT (previews against HEAD 8bf8b5a1)

### 5a. OUTSTANDING_BUGS.md

```diff
--- OUTSTANDING_BUGS.md@HEAD
+++ OUTSTANDING_BUGS.md@preview
@@ -24719,6 +24719,12 @@
 * **`dashokclass` (LOW, open)** -- `tools/pipeline/gen_dashboard.py`: `D_CLASS` maps only the four glyphs, so the 439
   ledger entries whose `d` is "OK" (365 matrix cells) render in the seat-failure class.  One line or a ledger sweep;
   either owes the controls a `DASH` row with `d` "OK".  Display only.
+  **CLOSED 2026-10-17 by the `dashokclass` landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F2:
+  no `OK` -> approval mapping and no sweep): every explicit `d` outside the four glyphs, on the ANSWER a cell shows,
+  renders as ONE class, "legacy -- verdict unclassified" (a live hold and a non-answer record keep their own rendering),
+  its text kept -- 670 displayed cells at HEAD 8bf8b5a1, 1,397 entries, not the 365 `OK` cells
+  named above -- and precommit Q2 (`tools/pipeline/check_entry_domain.py`) holds the off-domain ANSWERS to a ceiling frozen
+  at landing.  Controls `regress/artifacts/dashokclass_20261016/RECEIPT_v6_on_staged_v5.txt`; kill table `regress/artifacts/dashokclass_20261016/KILLTABLE_v6_staged.txt`.
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
@@ -24761,3 +24767,25 @@
   supervisor trap in a slot naming a residual vector (11..113, 116..127) or 114/115 -- is unrowed.  `&& !(cpu->delay_slot
   && is_trap)` at :799 is a PREDICTED 84/84 escape, not measured (Fable 5.1, pass 16, `pass16/fable5_m88kp16.md` section
   4).  Pin if ever rowed: `residtbdslot` = `[BR_N_PLUS16, TB1_0_R3_50]`, r3 = 1, expected HALT naming 0x032.
+
+### 2026-10-17 -- the dashboard's legacy class and the entry-domain check landed (`dashokclass` closed); one row filed
+
+* **`dashmissingd` (LOW, open)** -- `tools/pipeline/gen_dashboard.py` renders an ANSWER that carries no `d` with the
+  seat-failure glyph (`d = ent.get("d", "…")`), and precommit Q2 lets a new one in (Astra's completeness condition 1: a
+  MISSING `d` passes).  MEASURED at HEAD 8bf8b5a1 (`regress/artifacts/dashokclass_20261016/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`, its deriver beside it): 1,561 of
+  5,177 entries are answers with no `d` (2026-08 174, 2026-09 1,244, 2026-10 143; the latest dated 2026-10-16 -- this
+  project still writes them, the main loop's own `m88kexcdeliver` entries of 2026-10-16 among them), and 814 of the 2,953
+  displayed answer cells show `…` because their latest answer has no `d` -- 682 of them by a keyword screen of the note
+  (an approximation) record a real answer.  Larger than `dashokclass`'s 670 cells.  A RULE question, not a sweep: either
+  Q2 refuses a NEW answer without `d` (reversing condition 1 forward of a cutoff) or the renderer gives a `d`-less answer
+  its own class; the old entries stay as they are under RULINGS_C F2 either way.  **The question is entangled with section
+  H, and the ruling must take both**: the same census's NOT-FIRED screen (`/not[ -]fired|roster/i`) finds 222 entries
+  recording a seat not fired or naming the roster, 200 of them untokened -- ANSWERS by `stage_tokens.is_answer` -- and 87
+  of those with no `d`, while `check_stage_panels.py` counts an untokened entry as a recorded seat and skips a NOTSEAT one.
+  So the project's standing way to meet H's nine seats under a reduced roster IS part of this population: a Q2 refusing a
+  new `d`-less answer would refuse the next landing's not-fired entries, and tokening them NOTSEAT turns H red (9/9
+  untokened, 4/9 tokened, measured by GPT-6 Astra, v4 pass).  A mechanism for the owner to weigh (Fable 5.1, v4 pass): an
+  entry-scoped "not fired by owner roster" token that `is_answer` treats as a non-answer, the renderer as a record and
+  section H as roster-excused.  Nine recorded seats are not nine reviews.  (The v3 pass cited "158 / 127 / 71" from a
+  screen whose regex was never written down; three seats could not reproduce it.)  Found by the main loop while landing
+  `dashokclass`.
```

### 5b. the ledger rows

```
# ledger changes the dashokclass landing makes, against HEAD (a preview; applied at commit)

== dashmissingd (NEW ROW)
  commits: ""
  id: "dashmissingd"
  sev: "LOW"
  state: "open"
  state_note: "filed 2026-10-17 at the dashokclass landing, by the main loop: regress/artifacts/dashokclass_20261016/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt (its deriver dashmissingd_census.py beside it) counts 1,561 of 5,177 entries as answers with no d -- 2026-08 174, 2026-09 1,244, 2026-10 143, the latest dated 2026-10-16 -- and 814 displayed cells whose latest answer has none.  gen_dashboard.py's `d = ent.get(\"d\", \"…\")` shows each as no answer / seat failure.  A rule question for the adjudicators, not a sweep: either Q2 refuses a NEW answer without d (reversing Astra's condition 1 forward of a cutoff) or the renderer gives a d-less answer its own class; RULINGS_C F2 keeps the old entries as they are either way.  ENTANGLED WITH SECTION H (the same census's NOT-FIRED screen, /not[ -]fired|roster/i, at HEAD): 222 entries record a seat not fired or name the roster, 200 untokened (answers by is_answer), 87 of them with no d, and check_stage_panels.py counts an untokened entry as a recorded seat while skipping a NOTSEAT one -- so refusing a new d-less answer would refuse the next landing's not-fired entries, and tokening them NOTSEAT turns H red (9/9 untokened, 4/9 tokened -- GPT-6 Astra, v4 pass); the ruling must take both.  A mechanism for the owner to weigh (Fable 5.1, v4 pass): an entry-scoped 'not fired by owner roster' token that is_answer treats as a non-answer, the renderer as a record and section H as roster-excused.  (The v3 pass's '158 / 127 / 71' came from an unrecorded screen and could not be reproduced.)"
  title: "tools/pipeline/gen_dashboard.py renders an ANSWER with no `d` as the seat-failure glyph and precommit Q2 lets new ones in: 814 of 2,953 displayed answer cells at HEAD 8bf8b5a1 (682 of them, by a keyword screen, real answers)"
  witness: null

== dashokclass 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the dashokclass landing (RULINGS_C F2): every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class, 'legacy -- verdict unclassified', its text kept and its reason in the tooltip; precommit Q2 (check_entry_domain.py) holds the off-domain answers to a ceiling frozen at landing -- per (row, phase, seat, date, d, note sha1), no more answers than the md5-pinned baseline holds.  The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities cannot exceed their landing baseline.  Witness: R2, 670 cells moved from the seat-failure class to legacy with nothing else changing.  The controls' CONTRACT rows, for each decision of the checker, the renderer change and Q2, its GENERATING SET and its COMPLEMENT -- every operand position, both ends, every width, every binding form and use, every optional field -- or discloses a member with its reason.  Six passes on the staged files -- pass 2, the adjudication pass and the v3, v4, v5 and v6 passes, the owner's four-seat roster each time (Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- GPT-6 Astra: a per-(row, phase, seat, date, d) count let a converted entry's allowance be refilled by a new answer (measured rc 0); the tooltip's 'not approval, not a seat failure' is contradicted by legacy answers whose notes record real failures; the baseline writer's placement is no guard.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/codex_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2 (v1): SHIP WITH CHANGES (4) -- GLM 5.3: the rc-2 path through the gate untested, no escapable-d fixture, no refill control, no legend line for an explicit blank.  All added in v2 (W3, R1b, C15, the legend line).", "ev": "regress/artifacts/dashokclass_20261016/pass2/glm_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured; CUTOFF moved to 2026-10-18 passed all 19 v1 controls; the precommit's cp1252 pipe raised UnicodeEncodeError on the failure lines; legacy answers whose notes name a non-answer; control gaps in C1, C11, R1-R3, W1-W2.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/fable5_dashok.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- Grok 4.7: an exported GXDOMAIN_BASELINE was honoured inside the hook; the loader kept the LAST count for a repeated key; the tooltip's denial and the unpinned inclusive cutoff.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/grok_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the 'identity' key is a CEILING over selected content (a byte-identical revert and a same-note replacement pass; 1,342 keys cover 1,356 answers) -- state the narrower guarantee or build provenance; three one-edit survivors (the tooltip clause restored after the checked prefix, `-u GXLEDGER` deleted, the loader's += made =); the v2 runner named the v1 controls; four claims to correct.  All applied in v3, the narrower guarantee stated in its words.", "ev": "regress/artifacts/dashokclass_20261016/f2/codex_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3: d_nonote dies on the baseline mismatch, not on the note (add the coherent two-edit form); the loader's summation pinned by nothing; R1 and R4 pinned prefixes only.  All applied in v3 (d_nonote2 killed by C15 and C16 -- among others, the v5 table showing nine; C17b; whole-string R1 and R4).", "ev": "regress/artifacts/dashokclass_20261016/f2/glm_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v2 receipts reproduce only with v2 under v1's name; six one-edit mutants pass all 35 (the tooltip tail, the malformed-date reason, which Q2 branch fired); three sentences overclaim; and its own pass-2 'note out of the key' was wrong.  All applied in v3.", "ev": "regress/artifacts/dashokclass_20261016/f2/fable5_dashokf2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: the note-only toll is this check's, not the ruling's; the Q2 comment's growth claim and 'can only shrink' survived; the raw-byte md5 pin reds a default Git-for-Windows checkout (the main loop measured it the same hour: a fresh clone gives 89d1d370 for 06a3ffc6; Fable 5.1 reproduced it on the v3 pass).  All applied in v3 (the pin folds CRLF; C18b).", "ev": "regress/artifacts/dashokclass_20261016/f2/grok_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v6 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v6 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v6 pass, NOT FIRED: the kimi seat sat outside the roster."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v6 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v6 pass, NOT FIRED: minimax-m3 was given no packet; the roster, not a wall."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: five one-edit survivors of the 46 (a date suffix, the record line, the class line on non-OK cells, the per-glyph strip, the missing-checker branch); {\"rows\": {}} and a string entry walked as empty and passed; C2c/C2d red without their own entries; four record sentences.  All addressed in v4 (the class closure: ledger_shape, C21d-h, C25, R1e-g, R2 per glyph, W6, isolated C2c/C2d).  Its NOTSEAT advice on not-fired entries is carried as a disagreement (section H counts seats by is_answer).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/codex_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GLM 5.3: the checker-absent and ledger-unreadable edges unpinned; the summary line pinned only on a clean ledger; two stale sentences (RULINGS_C's '5,150 at HEAD', Q2's 'or is a frozen legacy entry' header).  All addressed in v4 (W6, C23, C11's dirty summary, the Q2 header), the RULINGS count dated in v5 (5,150 at e483d931).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/glm_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v3 receipts and the table reproduce; `if cls == LEGACY and d == \"OK\"` and its non-blank sibling pass all 46 (R1 pinned ONE cell's tooltip); the MISSING-checker branch; three records sentences; the dashmissingd question omits the section-H collision.  All addressed in v4 (R1g whole tooltips, W6, C24, C26, R1h, the hint, the filing).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/fable5_dashokv3.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Grok 4.7: the glyph set open at the top (a fifth DOMAIN member or D_CLASS key passes); the cutoff pinned on two days; the summary's baseline number and Q2's named-entry lines unread; a tab-only d.  All addressed in v4 (C27, C12 far, C1 baseline, W2 names, R1d tab).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/grok_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V4 PASS: SHIP WITH CHANGES (18) -- Fable 5.1 (claude-fable-5-1 throughout), measuring in a mirror (its receipts copied to v4pass/fable5_meas/): 72/72 and the 66-mutant table reproduce byte for byte; 21 one-edit mutants pass all 72, 15 at decisions v4 listed as pinned, all one shape -- each pin tested ONE edge of its decision (the trailing end of a key field, the first literal line, a number but not its label, a substring, one branch of three); six records sentences false.  All addressed in v5, which rows each pin's dual edge.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/fable5_dashokv4.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V4 PASS: SHIP WITH CHANGES (4) -- GPT-6 Astra: ten more one-edit survivors run in memory (a row-id strip, a bool or -1 baseline count, a numeric key field, a suffixed matched date, swapped refusal identifiers, the record-adjoining and null tooltips, the strip labels, an invisible legacy glyph) and Q2's else narrowed to rc 2; C24 confounded by the ledger's own NOTSEAT records; J15's 'whole population' false; it WITHDREW its NOTSEAT advice after measuring section H (9/9 untokened, 4/9 tokened).  All addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/codex_dashokv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V4 PASS: SHIP WITH CHANGES (6) -- Grok 4.7: six survivors traced against every control -- a null cell rendered pend, membership by a stripped d in both files, the leading end of the key (the CONTRACT's 'C25 edits the ends' false), the whitespace glyph's character set, the ISO $ anchor, the baseline scalars; ruled the not-fired entries stay untokened on this landing.  All addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/grok_dashokv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V4 PASS: SHIP WITH CHANGES (4) -- GLM 5.3 (glm-5.3:cloud, packet-fed): 5d's 'killed by exactly C15/C16' stale (v4 kills d_nonote2 by C15, C16, C25e, C25f); four decisions it could not settle from the packet -- the note's type (a list, None or dict note without a token is refused -- Fable 5.1 measured; one holding a non-answer token as an element or key is SKIPPED, and True is rc 2 but False rc 1 -- GPT-6 Astra, v5 pass), rows absent (pinned in v5, C21i), a renderer null (pinned, R1n), hold/record precedence over an off-domain d (answered by the fixture); J15 overstated.  Addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/glm_dashokv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V5 PASS: SHIP WITH CHANGES (10) -- Fable 5.1 (claude-fable-5-1 throughout), measuring in a mirror: 96/96 and the 105-mutant table reproduce byte for byte; 25 one-edit mutants of its own through the 96, 16 escapes on a second axis -- a pin asserting a property of the SELECTED set says nothing about its COMPLEMENT (only legacy cells carry the class line; the glyph set where USED; the padded cell's text; the hint's tail; 4 whitespace code points of 29); a renderer crash on the shipped ledger scored INCOMPLETE, not killed; zero floor breaches.  All addressed in v6.", "ev": "regress/artifacts/dashokclass_20261016/v5pass/fable5_dashokv5.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V5 PASS: SHIP WITH CHANGES (10) -- GPT-6 Astra: ten survivors measured in memory, each at a decision v5 listed as pinned -- a pin covered PART of its decision's generating set (the trailing pad, baseline positions 1-4, the ISO widths, globals() and a dict mutation past C27, the hint's tail, a tooltip with optional fields, an overriding CSS rule, the apparatus line's first-line selection); K2 and K19 wrong as stated (a list or dict note holding a token is skipped).  All addressed in v6.", "ev": "regress/artifacts/dashokclass_20261016/v5pass/codex_dashokv5.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V5 PASS: SHIP WITH CHANGES (12) -- Grok 4.7 (its shell denied; every survivor traced against each assertion, the ledger and baseline searched): eleven one-edit survivors of the 96 -- the trailing pad, baseline positions 1-4, a truncated ISO pattern, dynamic rebinding past C27, the hint's join, the class line on every cell or off the newline and NBSP cells, an overriding CSS rule, Q2's else narrowed to skip one status, the apparatus line's tail, the named entry replaced by a constant -- and K19 wrong.  All rowed in v6 (W9 exhausts Q2's 254 other statuses).", "ev": "regress/artifacts/dashokclass_20261016/v5pass/grok_dashokv5.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V5 PASS: SHIP WITH CHANGES (3) -- GLM 5.3 (glm-5.3:cloud, packet-fed), reasoned: `entries` absent unrowed (the K16 twin); C27 blind to dynamic rebinding; the note's UTF-8 and the phase/seat None defaults pinned on neither edge.  Rowed in v6 (C21j, the C27 walk, C20b, C29).", "ev": "regress/artifacts/dashokclass_20261016/v5pass/glm_dashokv5.txt", "d": "✓"}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] dashokclass closed by its landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v6_on_staged_v5.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 115/115 -- in particular R2 (only pend -> legacy, 670 cells, the strip string exact), R2b (the fixture strip by exact membership), C15/C16 (the note in the key), C25a-r (each key field byte for byte, at both ends), C17b-n (the baseline row's every clause and every string position), C18/C18b (the md5 pin, CRLF folded), C21a-k (a misshapen ledger or baseline is rc 2; a row without entries is empty), C27 (one binding of each glyph set, no other way to change it, the effective DOMAIN), C28/C28b (a glyph padded at either end), C29 (no phase or seat), C20/C20b (non-ASCII d and note), C3/C6/C9/C19a (each refusal line whole), C11 (the hint whole), C12, C12s and C12w (the cutoff and the ISO shape's widths and separators, the summary exact), R1e/R1g/R1n/R1o (whole tooltips, null and optional fields included), R1p/R1q (no class line outside legacy; a bare legacy cell), R1h/R1w (the glyph text exact; every whitespace code point), R5 (the CSS, no overriding rule) and W4-W8 (exported overrides stripped; the checker absent, an unexpected status -- its FIRST line -- and a missing python are BAD) -- and does regress/artifacts/dashokclass_20261016/KILLTABLE_v6_staged.txt's runner still kill every pinned mutant?  Is the record (the checker's docstring, the Q2 comment, the CHANGELOG block, the bug-file closure) true of what shipped, and is the narrower guarantee -- a ceiling over selected content, not an entry identity -- stated where a reader will meet it?"
  state: "closed"
  state_note: "filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, \"pend\")`; HEAD's ledger carries 439 entries with d \"OK\" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS (\"OK\": \"ok\") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d \"OK\".  LOW, display only.\n\n[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line \"OK\": \"ok\", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class (a live hold and a non-answer record keep their own rendering), its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at landing.  The 365 above counts OK cells only; the legacy class is 670 displayed cells (1,397 entries) at HEAD 8bf8b5a1."
  witness: "harness:regress/artifacts/dashokclass_20261016/RECEIPT_v6_on_staged_v5.txt -- R2: HEAD's renderer (gen_dashboard_before.py) shows 1,503 displayed cells in the seat-failure class and the staged one 833, the 670 moved now LEGACY with nothing else changing; C1-C29 and W1-W8 pin the entry-domain check and Q2; regress/artifacts/dashokclass_20261016/KILLTABLE_v6_staged.txt kills every pinned mutant (157/157 as recorded, two escapes recorded as equivalent)"
```

### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md

```diff
--- RULINGS_C_records.md@HEAD
+++ RULINGS_C_records.md@preview
@@ -41,8 +41,12 @@
 **F2 / D2 `dashokclass` -- UPHELD with the class re-keyed (Grok and Fable independently; Astra agrees on the semantics).**
 - Every mechanical sweep stays withdrawn (3/3).
 - The legacy class is keyed on the DOMAIN, not the spelling: every explicit `d` outside the four glyphs renders as one
-  residue class, labelled "legacy -- verdict unclassified" (Astra's wording), text kept, notes and hold/record precedence
-  preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at HEAD).  Keyed on `OK` alone
+  residue class, labelled "legacy -- verdict unclassified" (adapted from Astra's "legacy OK — verdict unclassified";
+  this said "Astra's wording" until the 2026-10-17 dashokclass landing -- Fable 5.1 and GPT-6 Astra, adjudication pass),
+  text kept, notes and hold/record precedence
+  preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at e483d931, where it was
+  measured -- 5,167 at c64445fa, which committed this file, Fable 5.1, v4 pass; 5,177 at the landing's HEAD, 8bf8b5a1).
+  Keyed on `OK` alone
   it would leave 958 of 1,397 off-domain entries in the false `pend` class (Fable, `meas_C/okdomain_census.txt`: OK 439,
   other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7).
 - The forward domain check keeps Astra's four completeness conditions; a date-only cutoff cannot stop a back-dated or
```

### 5d. the CHANGELOG block (a DRAFT: its v6-pass sentence is written from this pass's answers)

# `dashokclass` (2026-10-17): the dashboard's LEGACY class and the entry-domain check -- every explicit `d` outside ✓ ✕ ⏸ … on the answer a cell shows renders as one class, "legacy -- verdict unclassified", instead of a seat failure (670 displayed cells at HEAD 8bf8b5a1), and precommit section Q2 holds the off-domain answers to a ceiling frozen at landing

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F2, upholding `packet_C_records.md` F2): no `OK` -> approval mapping, every mechanical sweep withdrawn, the class keyed on
the DOMAIN of `d` rather than on one spelling, and Astra's four completeness conditions for the forward check.

* `tools/pipeline/gen_dashboard.py`: an explicit `d` the four-glyph map does not know, on the ANSWER a cell shows, renders as
  class `legacy` (a live hold and a non-answer record keep their own rendering) -- its text kept, `?` for an explicit blank
  or a whitespace-only `d`, and a tooltip that opens (after a refused exemption's line, if any) with "legacy -- verdict
  unclassified: d = ... is outside ✓ ✕ ⏸ …; read the note for the outcome", because some legacy notes record real seat
  failures; the strip counts the class as a fifth number, so it sums to the entry total; the legend says what the class is.
  A MISSING `d` is unchanged -- it still renders `…` (filed as `dashmissingd`).
* `tools/pipeline/check_entry_domain.py` and `entry_domain_baseline.json`, precommit section **Q2** (HARD): an ANSWER whose
  explicit `d` is outside the four passes only while, for its (row, phase, seat, date, `d`, sha1 of its note), the ledger
  holds no more such answers than the baseline froze at landing (1,342 keys, 1,356 answers), and only if it is dated
  before 2026-10-17.  **The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities
  cannot exceed their landing baseline** -- unmatched content or an excess occurrence fails; a byte-identical revert, a
  replacement differing only outside the six fields, and an edit outside them (`ev`, `grade`, `b`) pass.  Editing a frozen
  entry's note means classifying it; that toll is this check's, not the ruling's.  Every container level of the ledger and
  the baseline is type-checked before it is walked; the baseline is md5-pinned with CRLF folded (this machine's system git
  sets `core.autocrlf=true`; a fresh clone measured 89d1d370 for the committed 06a3ffc6); Q2 strips exported
  `GXDOMAIN_BASELINE` and `GXLEDGER`, and reds on ANY status but 0 and 1; a misshapen or unreadable ledger or baseline is rc
  2, never green.
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v6.py`, 116 rows, its docstring the CONTRACT: each decision
  of the checker, the renderer change and Q2 with its GENERATING SET -- every operand position, both ends of each field,
  every width and separator of the ISO shape, every binding form and use of the glyph sets, every optional tooltip field,
  every `str.isspace()` code point -- and its COMPLEMENT (only legacy cells carry the class line; the set where it is used),
  each member rowed or disclosed with its reason.  C27 walks both files' ast: one module-level binding of DOMAIN and of
  D_CLASS, every other binding form, dynamic namespace write and dict mutation refused, every use whitelisted, and the
  checker's EFFECTIVE DOMAIN read by import.  116/116 on the staged files, installed byte for byte
  (`RECEIPT_v6_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v6.py`: 157/157 as recorded
  (`KILLTABLE_v6_staged.txt`) -- 155 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356 off-domain
  answers has an empty note, and no note anywhere is the string "None") and `d_isosearch` (the pattern is `^`-anchored)
  equivalent escapes; `d_nonote2` and `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms), killed by
  C15/C16 and by C25d.  The note-type scope is disclosed: a list or dict note holding a non-answer token as an element or a
  key is a non-answer and is skipped, as the renderer shows it (GPT-6 Astra, v5 pass, measured).  A fold of `d`, or a
  fold or strip of the note, is one-sided on this ledger and dies on C1: some frozen keys stop matching (the d fold changes
  1,100 of the 1,356 frozen answers' keys, the note strip 2, the note fold 1,352 -- Fable 5.1, v4 pass).  The v1-v4 runners
  and receipts are kept; `run_mutants.py` names `run_controls_v2.py` (it named the v1 suite, which crashes on the 7-field
  baseline, so its 14/14 had reproduced only in a staging copy -- Fable 5.1, GPT-6 Astra).
* Records: `dashokclass` closed (witness `harness:`, its REGRESS review HELD for the flagship); `dashmissingd` (LOW) filed --
  814 of 2,953 displayed answer cells show `…` because their latest answer has no `d` (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`),
  its rule question entangled with section H's seat count: the census's NOT-FIRED screen (`/not[ -]fired|roster/i`) finds
  222 entries, 200 untokened, 87 with no `d` (the v3 pass's "158 / 127 / 71" came from an unrecorded screen and could not be
  reproduced); RULINGS_C's "Astra's wording" corrected to "adapted from", and its "5,150 at HEAD" dated to e483d931.

**Pass 2** (`pass2/`, on v1): Astra SWC 3, GLM SWC 4, Fable SWC 7, Grok SWC 3 -- the count key's refill, the tooltip's
denial, the baseline guard, the unpinned cutoff, the cp1252 traceback, the honoured override.  **Adjudication pass** (`f2/`,
on v2, every finding shared with every seat): all four SWC 3 -- the "identity" is a ceiling (Astra), one-edit survivors
(Astra, GLM, Fable, Grok), v2's runner naming the wrong controls (Fable, Astra), the CRLF pin (Grok; measured), the
note-only toll credited to the ruling (Grok); Fable 5.1 withdrew its own pass-2 "note out of the key".  **V3 pass**
(`v3pass/`): all four SWC 3 -- every seat found one-edit survivors of the 46, so v4 was the class closure.  **V4 pass**
(`v4pass/`): Fable SWC 18, Astra SWC 4, Grok SWC 6, GLM SWC 4 -- 21 one-edit mutants passed all 72 v4 controls, 15 at
decisions v4 listed as pinned, one shape: each pin tested ONE edge of its decision (Fable 5.1); the not-fired entries stay
untokened on this landing, all four agreeing (Astra withdrew its NOTSEAT advice after measuring section H: 9/9 untokened,
4/9 tokened), the rule question carried by `dashmissingd`.  **V5 pass** (`v5pass/`): Fable SWC 10, Astra SWC 10, GLM SWC 3,
Grok SWC 12 -- no floor breach and no misattributed kill (Fable 5.1, measuring in a mirror, both v5 receipts reproduced
byte for byte), and the next layer on two axes: a pin covered PART of its decision's generating set (Astra: ten survivors
measured, among them `globals()` and a dict mutation changing the glyph sets past C27; Grok: eleven traced, three of them
past every v6 row then drafted -- the newline and NBSP cells' tooltips, Q2's `else` at 251 of its 254 statuses, the named
entry by a prefix) and a pin on the SELECTED set said nothing about its complement (Fable: sixteen escapes, among them the
class line on 833 pend cells); GLM named the `entries` default, the note's UTF-8 and the None phase/seat; Astra and Grok
both found K19's "nothing is skipped" false; a renderer crashing on the shipped ledger was scored INCOMPLETE, not killed,
until R2's census was guarded.  All rowed or disclosed in v6 -- W9 EXHAUSTS Q2's else partition (254 statuses), R1w the
whitespace set (29 code points).  **V6 pass** (`v6pass/`): [to be
written from its answers].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.


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
