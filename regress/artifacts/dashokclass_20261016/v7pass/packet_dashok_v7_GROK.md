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

**Liveness:** open your answer with the token `GROK_DASHOKV7_20261017` on its own line, then your verdict line.

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

## 4. The repair: the controls, v6 -> v7

### 4a. `run_controls_v6.py` -> `run_controls_v7.py` (298 changed lines)

```diff
--- run_controls_v6.py
+++ run_controls_v7.py
@@ -1,8 +1,8 @@
 #!/usr/bin/env python3
-"""Controls for `dashokclass` (2026-10-17, v6 after the v5 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
+"""Controls for `dashokclass` (2026-10-17, v7 after the v6 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
 ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
 ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
-the three files under test (run_mutants_v6.py and the staged runs use them); the defaults are the tree's.
+the three files under test (run_mutants_v7.py and the staged runs use them); the defaults are the tree's.
 
   THE CONTRACT (v6) -- the v4 pass found pins that tested ONE edge of a decision, and v5 rowed the dual edge.  The v5 pass
   (GPT-6 Astra and Fable 5.1 measured, GLM 5.3 reasoned, Grok 4.7 traced) found the next layer on two axes.  A v5 pin covered
@@ -14,12 +14,24 @@
   of W2's output.  And a pin
   asserting a property of the SELECTED set said nothing about its COMPLEMENT (Fable 5.1) -- every legacy cell has the class
   line but not ONLY legacy cells, the padded cell's class but not its text, the set where it is DEFINED but not where it is
-  USED.  So v6 enumerates each decision's generating set -- every operand position, both ends, every width and separator,
-  every binding form and use, every optional field, every whitespace code point -- with its complement, and rows each
-  member, or discloses it with its reason.
+  USED.  So v6 enumerated each decision's generating set -- every operand position, both ends, every width and separator,
+  the binding forms and uses C27 named, every optional field, every whitespace code point -- with its complement, and rowed
+  each member it named, or disclosed it with its reason.
+
+  v7 -- the v6 pass (GPT-6 Astra in memory, Fable 5.1 in a mirror, Grok 4.7 and GLM 5.3 reading) found no defect in the
+  staged files.  It found C27's universal false -- a banned callable reached by an attribute path or an alias, a
+  mapping-pattern rest capture, a store into a frame's globals, a rebinding inside the `__main__' block the import read
+  never runs (all four seats) -- and a NON-LITERAL binding crashing the walk before the tally (V19's class: Grok 4.7, GLM
+  5.3, Fable 5.1); and members still open in the generating sets: list rows and entries, the ISO widths' other directions,
+  a NON-legacy cell carrying optional fields (graded clause (d) by Fable 5.1, (e) by GPT-6 Astra -- rowed either way), single
+  optional fields on a legacy cell, every style block, the counter keys as spellings, a numeric or bool d, a row with no id.
+  So v7 reads BOTH files' glyph sets by EXECUTING each as `__main__' on a fixture and taking its globals after the run -- the
+  effect, not the syntax, which closes the runtime-rebinding class at once -- refuses a non-literal binding instead of
+  crashing on it, pins each set's use COUNT, and rows each open member.
     checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
              `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
-                                                                                        entries key: rc 0); C23 (not JSON)
+                                                                                        entries key: rc 0); C21l / C21m (a row,
+                                                                                        an entry that is a LIST); C23 (not JSON)
              baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
              fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
                                                                                         of true, -1, 0, 1.0), C17h-m (each of the
@@ -35,7 +47,8 @@
              ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
              over its UTF-8 text, after str()                                          with a trailing or a leading space);
                                                                                         C15/C16 (the note); C26b; C29 (no phase,
-                                                                                        no seat: its line exact); C20b (a
+                                                                                        no seat: its line exact); C29b (a row with
+                                                                                        no id keys as "None"); C20b (a
                                                                                         non-ASCII note: its line exact); C21k (a
                                                                                         list note holding no token: refused)
              the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
@@ -43,26 +56,34 @@
              digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
                                                                                         dated 2026-10-17T12:00:00), C12w (MATCHED
                                                                                         identities breaking the shape in one
-                                                                                        place -- year, month or day width, either
-                                                                                        separator: rc 0), C19a/b
+                                                                                        place -- a year of 5 or 3 digits, a month
+                                                                                        of 1 or 3, a day of 1, either separator:
+                                                                                        rc 0, which C12w reads; C12s reads rc
+                                                                                        too), C19a/b
              output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
              ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
              refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
                                                                                         C6, C9, C19a, C20, C20b, C29, C21k (the
                                                                                         refusal line exact; C20's d escaped)
-             the glyph sets: ONE binding of DOMAIN and of D_CLASS, each the four,       C27 (an ast walk of both files: every
-             and no other way to change either                                         binding form of the name -- a store, a
-                                                                                        delete, a global, an import alias, a def
-                                                                                        or class, an except or match name, a
-                                                                                        parameter, an attribute or subscript store
-                                                                                        keyed by it; a call to globals / vars /
-                                                                                        locals / setattr / delattr / exec / eval /
-                                                                                        compile / __import__; __dict__ or
-                                                                                        __globals__ -- and every USE whitelisted:
-                                                                                        DOMAIN in `in' and as `" ".join's
-                                                                                        argument, D_CLASS in `.get(' and `in'; the
-                                                                                        checker's EFFECTIVE DOMAIN read by
-                                                                                        importing it)
+             the glyph sets: ONE literal binding of DOMAIN and of D_CLASS, each the    C27 -- the EFFECT: BOTH files run as
+             four, used where they are used and nowhere else                            __main__ on a fixture, each glyph set read
+                                                                                        from the globals AFTER the run (any
+                                                                                        rebinding the run executes, whatever its
+                                                                                        syntax).  The SYNTAX, for what the run
+                                                                                        does not execute: one module-level LITERAL
+                                                                                        store of the name (a non-literal one is
+                                                                                        refused, never crashed on); a delete, a
+                                                                                        global, an import alias, a def or class,
+                                                                                        an except, match or mapping-rest name, a
+                                                                                        parameter, an attribute store of the name,
+                                                                                        a subscript store keyed by it or into a
+                                                                                        call; a banned builtin called by name OR
+                                                                                        attribute, or referenced uncalled;
+                                                                                        __dict__, __globals__, f_globals,
+                                                                                        f_locals; and each use COUNTED -- DOMAIN
+                                                                                        once in `in' and once as `" ".join's
+                                                                                        argument, D_CLASS once in `.get(' and once
+                                                                                        in `in' 
     renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
              the answer a cell shows                                                    end), R1n (null), R3
              the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
@@ -71,17 +92,25 @@
                                                                                         cells, whole), R1e (a
                                                                                         record beside it), R1f (a refused
                                                                                         exemption first), R1o (a grade, a badge
-                                                                                        and evidence all present), R1q (neither
-                                                                                        date nor note)
-             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells)
+                                                                                        and evidence all present), R1o2 (a grade,
+                                                                                        evidence, a badge `s', each ALONE), R1q
+                                                                                        (neither date nor note); R1g also a
+                                                                                        number and a bool d
+             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells);
+                                                                                        R1p2 (ok, bad and hold cells carrying a
+                                                                                        grade, a badge and evidence); a tok, a
+                                                                                        live hold and an empty cell return before
+                                                                                        the class is computed (read)
              the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
              or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
                                                                                         str.isspace() code points)
              the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
              its labels                                                                 string), R2b (the fixture ledger, whose
-                                                                                        pads and null count legacy)
+                                                                                        pads, null and the counter-key spellings
+                                                                                        `total' and `legacy' count legacy)
              the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
-             the style block naming the class                                          rules naming `legacy')
+             any style block naming the class                                          rules naming `legacy' in ANY style block,
+                                                                                        CSS escapes decoded)
     Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
              refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
                                                                                         output whole, the entry named), W3 (rc 2),
@@ -102,17 +131,30 @@
         a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
       case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
       the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
-        wording: display only (their rc 2 is pinned; an emptied reason passes every row -- `x_apparatusmsg', Fable 5.1, v5
-        pass, measured);
-      the page's CSS outside the two rules this landing adds (a rule hiding every glyph would be HEAD's CSS, not this diff);
-      a change to the glyph sets by a mechanism C27 does not name (a helper module rebinding them after import, a C
-        extension) is outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
+        wording: DELIBERATELY unpinned display wording (C13 could carry it; their rc 2 is pinned; an emptied reason passes
+        every row -- `x_apparatusmsg', Fable 5.1, v5 pass, measured);
+      a CSS rule hiding glyphs WITHOUT naming the class (an attribute selector, a rule on every `.g'): R5 reads the rules
+        naming `legacy', in every style block, escapes decoded; HEAD's CSS is not this diff;
+      a change to the glyph sets C27's two reads cannot see -- a rebinding in a code path the fixture run does not execute
+        AND whose syntax the walk does not name (a runtime-built attribute name, a helper module), a C extension -- is
+        outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
         `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
         first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
       the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
         x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
         set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
         v5 pass, measured: `+ ("OK",)' at the use site 80/96);
+      the use site INLINED: a literal standing for a glyph set at its use is now a removed use, which C27's COUNT sees; a
+        literal ADDED beside the Name (a disjunct) is the novel-spelling class above, and so is `summary()''s `n' given a
+        fifth key (the strip then fails to sum only for an entry spelling it -- Fable 5.1, v6 pass, measured);
+      a LIST d crashes the renderer at `D_CLASS.get' (unhashable) -- unreachable through a committed ledger: Q2 refuses a
+        new answer with a list d (C26b), no frozen answer carries one, and a hold or record returns before the class is
+        computed (GLM 5.3's member, read);
+      Q2's `$?' folds a child status of 256k to 0 -- unreachable from the checker's exits 0, 1 and 2 (Fable 5.1, v6 pass,
+        measured on a stub); the ISO digit class: `\\d' admits non-ASCII digits (a fullwidth `２'), equivalent on every
+        ASCII date; a lone CR in the baseline is not folded by the md5 pin -- no checkout writes one;
+      R3 is a PRESENCE pin as well as a mutant-render check: a mutant editing R3's find-text reds it by absence, which is
+        not a behavioural kill -- no mutant in the kill table rests on R3 alone (Fable 5.1, v6 pass, read);
       a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
         sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
         apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
@@ -126,9 +168,10 @@
     A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
     note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
     frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
-    two-edit design mutant d_dfold2, killed by C25d.  Two kills the shipped ledger already supplies are ALSO rowed in isolation,
-    so no pin rests on the ledger's composition alone: the `entries' default (98 of 912 shipped rows carry no `entries' key;
-    C21j) and a latin-1 note encoding (34 frozen notes are non-ASCII, one beyond latin-1; C20b).
+    two-edit design mutant d_dfold2, killed by C25d.  The `entries' default is ALSO rowed in isolation (98 of 912 shipped rows
+    carry no `entries' key; C21j's ledger holds only its two rows).  C20b is NOT isolated: its answer joins the shipped
+    ledger, whose 34 non-ASCII frozen notes already fail a latin-1 encode -- it is a named witness of that kill, not the sole
+    carrier (GPT-6 Astra and Grok 4.7, v6 pass; the v6 text called it isolated).
 
   CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
   v4 passes' findings):
@@ -168,6 +211,9 @@
          note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
     C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
     C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
+    C21l / C21m  a misshapen ledger: a row that is a LIST / an entry that is a LIST -- `(dict, list)' at either shape test
+         walked them (a list ENTRY as a non-entry, GREEN; Fable 5.1, v6 pass, measured)       -> 2 / 2
+    C29b an off-domain answer in a row with NO id -- keyed and printed as "None", its line EXACT    -> 1
     C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
     C23  a ledger that is not JSON                                                                  -> 2
     C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
@@ -177,8 +223,8 @@
          note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
     C26  a new answer with an explicit "d": null                                                     -> 1
     C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
-    C27  DOMAIN and D_CLASS: ONE binding each and NO other way to change them -- an ast walk of every binding form and
-         every use (whitelisted), and the checker's EFFECTIVE DOMAIN read by importing it -- each exactly ✓ ✕ ⏸ …
+    C27  DOMAIN and D_CLASS: one LITERAL binding each, every named binding form refused, each use COUNTED, and BOTH
+         files' EFFECTIVE set -- read after running each as __main__ on a fixture -- exactly ✓ ✕ ⏸ … (D_CLASS's classes too)
     C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
     C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
     C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
@@ -195,6 +241,8 @@
          "\n", "\xa0", null), the date, the note
     R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
     R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
+    R1o2 legacy answers carrying a grade ALONE, evidence ALONE, the badge `s' ALONE: each WHOLE tooltip, the line first
+    R1p2 ok, bad and hold answers carrying a grade, a badge and evidence: each WHOLE tooltip, NO class line
     R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
     R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
     R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
@@ -530,8 +578,11 @@
 #  "2026-9-1" as a date after the cutoff (GPT-6 Astra, v5 pass).  Each identity is FROZEN and breaks the shape in one place,
 #  each chosen to compare at or after the cutoff if the shape were loosened there, so only the shape decides: rc 0
 #  (a one-edit mutant loosens ONE separator, so each has its own row: one date breaking both would miss either alone)
+#  v7: the other DIRECTION of each width -- `\d{3,4}' read a frozen 999-10-17 as a date after the cutoff, `\d{2,3}' a frozen
+#  2026-100-17, and both passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass); a day of three digits is equivalent
+#  (the pattern has no end anchor, so `\d{2}' already reads 2026-10-178's first two)
 for tag, dt in (("year", "99999-10-18"), ("month", "2026-9-17"), ("day", "2026-10-9"), ("sep1", "2026/10-18"),
-                ("sep2", "2026-10/18")):
+                ("sep2", "2026-10/18"), ("year3", "999-10-17"), ("month3", "2026-100-17")):
     e = ans(dt, d="OK", seat="kimi", note="iso shape " + tag)
     fb = wjson("b_cut_w_%s.json" % tag, base + [ident(ROW0, e) + [1]])
     rc, out = run_checker(with_entries([(ROW0, e)]), fb)
@@ -585,11 +636,38 @@
             probs.append("subscript store keyed by the name")
         elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
             probs.append("call to " + n.func.id)
-        elif isinstance(n, ast.Attribute) and n.attr in ("__dict__", "__globals__"):
+        #  v7: by ATTRIBUTE (`builtins.exec', `builtins.setattr', `object.__setattr__'), by an uncalled REFERENCE (`_e =
+        #  exec'), a mapping-pattern REST capture, a subscript store into a CALL or a frame's globals -- each changed the
+        #  renderer's effective D_CLASS past the v6 walk (GPT-6 Astra, GLM 5.3, Grok 4.7, Fable 5.1, v6 pass)
+        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in BANNED_ATTR:
+            probs.append("call to ." + n.func.attr)
+        elif (isinstance(n, ast.Name) and n.id in BANNED and isinstance(n.ctx, ast.Load)
+              and not (isinstance(parent.get(n), ast.Call) and parent.get(n).func is n)):
+            probs.append("a reference to " + n.id)
+        elif isinstance(n, ast.MatchMapping) and n.rest == name:
+            probs.append("match rest")
+        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load)
+              and (isinstance(n.value, ast.Call) or (isinstance(n.value, ast.Attribute) and n.value.attr in DUNDER))):
+            probs.append("a subscript store into a call or a namespace")
+        elif isinstance(n, ast.Attribute) and n.attr in DUNDER:
             probs.append(n.attr)
         elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
             probs.append("a use at line %d" % n.lineno)
-    return (ast.literal_eval(top[0].value) if len(top) == 1 else None), probs
+    #  v7: a NON-LITERAL store is refused, never crashed on -- `ast.literal_eval' raised on `tuple((...))' and the run died
+    #  before its tally, the driver scoring the kill INCOMPLETE (V19's class; Grok 4.7, GLM 5.3, Fable 5.1, v6 pass)
+    lit = None
+    if len(top) == 1:
+        try:
+            lit = ast.literal_eval(top[0].value)
+        except (ValueError, SyntaxError, TypeError):
+            probs.append("a non-literal binding")
+    uses = collections.Counter(use_ok(n, parent) for n in ast.walk(tree)
+                               if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and use_ok(n, parent))
+    return lit, probs, uses
+
+
+BANNED_ATTR = ("exec", "eval", "globals", "vars", "locals", "setattr", "delattr", "__import__", "__setattr__", "__delattr__")
+DUNDER = ("__dict__", "__globals__", "f_globals", "f_locals")
 
 
 def in_compare(n, parent):
@@ -598,32 +676,67 @@
             and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))
 
 
+#  each use returns its KIND (v7: the kinds are COUNTED -- a use site inlined with a literal is a removed use)
 def dom_use(n, parent):
     p = parent.get(n)
-    return in_compare(n, parent) or (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
-                                     and p.func.attr == "join" and isinstance(p.func.value, ast.Constant))
+    if in_compare(n, parent):
+        return "in"
+    return "join" if (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
+                      and p.func.attr == "join" and isinstance(p.func.value, ast.Constant)) else None
 
 
 def dcls_use(n, parent):
     p = parent.get(n)
-    return in_compare(n, parent) or (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
-                                     and parent.get(p).func is p)
-
-
-dom, dprobs = walk_name(CHECKER, "DOMAIN", dom_use)
-dcls, cprobs = walk_name(RENDER, "D_CLASS", dcls_use)
-r_imp = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); import check_entry_domain as c; "
-                        "print(ascii(c.DOMAIN))", os.path.dirname(DEFAULT_CHECKER)], capture_output=True, text=True)
-try:
-    eff = ast.literal_eval(r_imp.stdout.strip()) if r_imp.returncode == 0 else None
-except (ValueError, SyntaxError):
-    eff = None
+    if in_compare(n, parent):
+        return "in"
+    return "get" if (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
+                     and parent.get(p).func is p) else None
+
+
+dom, dprobs, duses = walk_name(CHECKER, "DOMAIN", dom_use)
+dcls, cprobs, cuses = walk_name(RENDER, "D_CLASS", dcls_use)
+#  v7: the EFFECTIVE sets, read by EXECUTING each file as __main__ on a fixture and taking its globals after the run -- any
+#  rebinding the run executes, in the module body or the main block, whatever its syntax.  v6 imported the checker, so a
+#  rebinding under `if __name__ == "__main__"' was invisible to it (GLM 5.3), and read nothing of the renderer, so
+#  `builtins.setattr' and a frame-globals store passed (Fable 5.1, v6 pass, measured).
+#  the run is a real MODULE registered as sys.modules["__main__"], as a script's is -- a bare namespace dict let
+#  `setattr(sys.modules[__name__], ...)' land on the wrapper instead of the run
+RUN_MAIN = ("import io, sys, types\npath, name = sys.argv[1], sys.argv[2]\nsys.argv = [path] + sys.argv[3:]\n"
+            "sys.path.insert(0, __import__('os').path.dirname(path))\n"
+            "mod = types.ModuleType('__main__')\nmod.__file__ = path\nsys.modules['__main__'] = mod\n"
+            "try:\n    exec(compile(io.open(path, encoding='utf-8').read(), path, 'exec'), mod.__dict__)\nexcept SystemExit:\n    pass\n"
+            "print('EFFECTIVE ' + ascii(mod.__dict__.get(name)))\n")
+
+
+def effective(path, name, ledger, *args):
+    env = dict(os.environ, GXLEDGER=ledger, PYTHONIOENCODING="utf-8")
+    env.pop("GXDOMAIN_BASELINE", None)
+    r = subprocess.run([sys.executable, "-c", RUN_MAIN, path, name] + list(args), capture_output=True, text=True,
+                       encoding="utf-8", errors="replace", env=env)
+    last = [l for l in r.stdout.splitlines() if l.startswith("EFFECTIVE ")]
+    try:
+        return ast.literal_eval(last[-1][len("EFFECTIVE "):]) if last else None
+    except (ValueError, SyntaxError):
+        return None
+
+
+eff = effective(DEFAULT_CHECKER, "DOMAIN", LEDGER)
+effd = os.path.join(T, "eff_render")
+os.makedirs(effd, exist_ok=True)
+shutil.copy(RENDER, os.path.join(effd, "gen_dashboard.py"))
+shutil.copy(os.path.join(PIPE, "stage_tokens.py"), effd)
+effc = effective(os.path.join(effd, "gen_dashboard.py"), "D_CLASS", LEDGER, "--out", os.path.join(effd, "out.html"))
 four = ("✓", "✕", "⏸", "…")
-say("C27 ONE binding each and no other way to change it: DOMAIN (and its EFFECTIVE value) and D_CLASS's keys are ✓ ✕ ⏸ …",
-    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four)
-    and not dprobs and not cprobs and isinstance(eff, tuple) and sorted(eff) == sorted(four),
-    "DOMAIN %r %s | effective %r | D_CLASS keys %r %s" % (dom, dprobs or "", eff, sorted(dcls) if isinstance(dcls, dict) else dcls,
-                                                          cprobs or ""))
+DCLS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
+say("C27 the glyph sets: one literal binding each, no named way to change it, each use counted, and BOTH files' EFFECTIVE "
+    "set -- read after running each as __main__ -- the four",
+    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and dcls == DCLS
+    and not dprobs and not cprobs and duses == collections.Counter({"in": 1, "join": 1})
+    and cuses == collections.Counter({"in": 1, "get": 1})
+    and isinstance(eff, tuple) and sorted(eff) == sorted(four) and effc == DCLS,
+    "DOMAIN %r %s uses %s | effective %r | D_CLASS %r %s uses %s | effective %r" % (
+        dom, dprobs or "", dict(duses), eff, sorted(dcls) if isinstance(dcls, dict) else dcls, cprobs or "", dict(cuses),
+        sorted(effc) if isinstance(effc, dict) else effc))
 rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
 say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
 #  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
@@ -669,12 +782,25 @@
                  ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]}),
                  #  v5: `rows' ABSENT -- `ledger.get("rows", [])' would walk it as empty (Grok 4.7, GLM 5.3, v4 pass)
                  ("C21i a misshapen ledger: no rows key -- {}", {}),
-                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []})):
+                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []}),
+                 #  v7: a LIST row and a LIST entry -- `isinstance(r, (dict, list))' raised on the row and walked the entry
+                 #  as a non-entry, GREEN, each passing all 116 v6 controls (Fable 5.1, v6 pass, measured)
+                 ("C21l a misshapen ledger: a row that is a list", {"rows": [[1]]}),
+                 ("C21m a misshapen ledger: an entry that is a list", {"rows": [{"id": "x", "entries": [["bogus"]]}]})):
     rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
     tb = any("Traceback" in l for l in out)
     say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
 rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
 say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
+#  C29b (v7): a row with NO id -- the key's row field is str() of it, "None"; `r.get("id") or ""' keyed it "" and passed all
+#  116 v6 controls (Fable 5.1, v6 pass, measured)
+e29 = ans("2026-10-10", d="OK", seat="deepseek", note="no row id")
+l29 = copy.deepcopy(L0)
+l29["rows"].append({"title": "a row with no id", "entries": [e29]})
+rc, out = run_checker(wjson("l_noid.json", l29))
+off29 = [l.strip() for l in out if l.strip().startswith("OFF-DOMAIN ANSWER")]
+say("C29b an off-domain answer in a row with no id: refused, keyed and printed as row None",
+    rc == 1 and off29 == [offline("None", e29, WHY_CEIL)], "rc %d; %r" % (rc, off29[:1]))
 #  C21j (v6): a row with NO entries key is an empty row, not a misshapen one -- `r.get("entries")' at either site turns it
 #  into rc 2; the shipped ledger kills that today (98 of 912 rows carry no `entries'), so it is rowed in isolation (GLM 5.3,
 #  v5 pass)
@@ -752,8 +878,9 @@
                            #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
                            {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
               #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
-              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while 649 and 642 of the 670
-              #  shipped legacy cells lost the class line (GPT-6 Astra, v5 pass)
+              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while the first MOVED the
+              #  class line off the front of 649 of the 670 shipped legacy cells and the second REMOVED it from 642 (GPT-6
+              #  Astra, v5 pass; "lost" corrected to moved/removed on the v6 pass)
               #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
               #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
               {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
@@ -761,6 +888,33 @@
               {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
                "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
                             "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
+              #  v7 (R1o2): ONE optional field each on a legacy answer -- `and (not ent.get("ev") or ent.get("grade"))' and
+              #  its twin, and `and badge != "s"', each passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass)
+              {"id": "ctlopt1", "title": "single optional field control row", "sev": "LOW", "state": "open", "commits": "",
+               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL",
+                            "note": "single grade control"},
+                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "OK",
+                            "ev": "regress/artifacts/x/ev1.txt", "note": "single ev control"},
+                           {"phase": "assess", "seat": "glm", "date": "2026-10-16", "d": "OK", "b": "s",
+                            "note": "single badge control"}]},
+              #  v7 (R1p2): NON-legacy answers carrying a grade, a badge and evidence get NO class line -- `if cls == LEGACY
+              #  or badge' and `... or ent.get("ev")' passed all 116 v6 controls (Fable 5.1, v6 pass, measured; the fourth
+              #  cell of {legacy, non-legacy} x {optional fields absent, present})
+              {"id": "ctlnlopt", "title": "non-legacy optional fields control row", "sev": "LOW", "state": "open",
+               "commits": "",
+               "entries": [{"phase": "assess", "seat": s_, "date": "2026-10-16", "d": g_, "grade": "MANUAL", "b": "A",
+                            "ev": "regress/artifacts/x/ev2.txt", "note": "nonlegacy optional control"}
+                           for s_, g_ in (("fable5", "✓"), ("codex", "✕"), ("glm", "⏸"))]},
+              #  v7 (R1g): a NUMBER and a BOOL d render legacy with their whole tooltip (GLM 5.3, v6 pass: the member was
+              #  unrowed); v7 (R2b): the counter keys `total' and `legacy' spelled as d count legacy -- `n[d if d in n else
+              #  LEGACY]' counted them as themselves and passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass)
+              {"id": "ctlscalar", "title": "scalar and counter-key control row", "sev": "LOW", "state": "open",
+               "commits": "",
+               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": 5, "note": "scalar control int"},
+                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": True, "note": "scalar control bool"},
+                           {"phase": "assess", "seat": "glm", "date": "2026-10-16", "d": "total", "note": "counter key total"},
+                           {"phase": "assess", "seat": "deepseek", "date": "2026-10-16", "d": "legacy",
+                            "note": "counter key legacy"}]},
               {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
                "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
 #  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
@@ -788,7 +942,8 @@
 
 CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
              "padded glyph control", "tab control", "newline control", "nbsp control", "null control", "padded trailing control",
-             "optional fields control", "BARE", "ws control U+")
+             "optional fields control", "BARE", "ws control U+", "single grade control", "single ev control",
+             "single badge control", "nonlegacy optional control", "scalar control", "counter key")
 
 
 def cells(html_text):
@@ -848,7 +1003,10 @@
                             ("tab control", "\t"), ("null control", None),
                             #  v6: the newline and NBSP cells -- R1d checked their class and glyph only, so `if cls == LEGACY
                             #  and d not in ("\n", "\xa0")' passed all 96 v5 controls (Grok 4.7, v5 pass)
-                            ("newline control", "\n"), ("nbsp control", "\xa0"))]
+                            ("newline control", "\n"), ("nbsp control", "\xa0"),
+                            #  v7: a number, a bool, and the counter keys as spellings
+                            ("scalar control int", 5), ("scalar control bool", True), ("counter key total", "total"),
+                            ("counter key legacy", "legacy"))]
     legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
     missing = [(note, d) for note, d, whole in want if whole not in legacy]
     return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])
@@ -894,6 +1052,20 @@
 say("R1o a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first",
     len(opt) == 1 and opt[0][0] == "legacy" and opt[0][2] == want_o,
     "cell %r; tooltip %s" % (opt[0][:2] if opt else None, "exact" if opt and opt[0][2] == want_o else "WRONG: %r" % (opt[0][2][:140] if opt else "")))
+BT = {"A": "the author did this review (shown, not hidden)", "s": "a review by the same model family"}
+o1 = {c[2] for c in cells(ha_fx or "") if c[0] == "legacy" and "single " in c[2] and " control" in c[2]}
+want_o1 = {html.escape(" — ".join(p), quote=True) for p in (
+    [legacy_line("OK"), "2026-10-16", "MANUAL", "single grade control"],
+    [legacy_line("OK"), "2026-10-16", "single ev control", "evidence: regress/artifacts/x/ev1.txt"],
+    [legacy_line("OK"), "2026-10-16", BT["s"], "single badge control"])}
+say("R1o2 legacy answers carrying a grade, evidence or the badge s ALONE: each WHOLE tooltip, the class line first",
+    o1 == want_o1, "got %r" % sorted(x[:70] for x in o1 - want_o1))
+p2 = [c for c in cells(ha_fx or "") if "nonlegacy optional control" in c[2]]
+want_p2 = html.escape(" — ".join(["2026-10-16", "MANUAL", BT["A"], "nonlegacy optional control",
+                                   "evidence: regress/artifacts/x/ev2.txt"]), quote=True)
+say("R1p2 ok, bad and hold answers carrying a grade, a badge and evidence: each WHOLE tooltip, NO class line",
+    sorted(c[0] for c in p2) == ["bad", "hold", "ok"] and all(c[2] == want_p2 for c in p2),
+    "%d cells %r; tips %r" % (len(p2), [c[0] for c in p2], [c[2][:60] for c in p2 if c[2] != want_p2][:2]))
 #  R1p (v6): the class line ONLY on a legacy cell -- `if cls in (LEGACY, "pend")' and `if cls != "ok"' each passed all 96 v5
 #  controls, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend cell, 833 on HEAD's ledger (Fable 5.1, v5 pass)
 plain = html.escape("2026-10-16 — a renderer control", quote=True)
@@ -932,8 +1104,15 @@
        ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
 #  v6: and they are the ONLY rules in the style block naming `legacy' -- a later `.c.legacy .g { font-size:0; }' left both
 #  present and hid every legacy glyph (GPT-6 Astra, v5 pass)
-sty = re.search(r"<style>(.*?)</style>", ha_fx or "", re.S)
-leg_rules = [" ".join(m.group(0).split()) for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", sty.group(1) if sty else "")]
+#  v7: EVERY style block, CSS escapes decoded -- a second <style> block and `.c.lega\\63 y' each hid the glyph past the v6
+#  form, which read the first block's literal `legacy' (GPT-6 Astra, Grok 4.7, v6 pass)
+def css_unescape(s):
+    return re.sub(r"\\([0-9a-fA-F]{1,6})\s?", lambda m: chr(int(m.group(1), 16)), s)
+
+
+blocks = re.findall(r"<style[^>]*>(.*?)</style>", ha_fx or "", re.S)
+leg_rules = [" ".join(m.group(0).split()) for b_ in blocks
+             for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", css_unescape(b_))]
 say("R5 the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it",
     ha_fx is not None and all(c in ha_fx for c in CSS) and sorted(leg_rules) == sorted(CSS),
     "missing %r; legacy rules %d %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")], len(leg_rules), [r[:40] for r in leg_rules]))
```

### 4b. `run_controls_v7.py`, WHOLE (its docstring is the CONTRACT and the row list)

```python
     1	#!/usr/bin/env python3
     2	"""Controls for `dashokclass` (2026-10-17, v7 after the v6 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
     3	ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
     4	ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
     5	the three files under test (run_mutants_v7.py and the staged runs use them); the defaults are the tree's.
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
    17	  USED.  So v6 enumerated each decision's generating set -- every operand position, both ends, every width and separator,
    18	  the binding forms and uses C27 named, every optional field, every whitespace code point -- with its complement, and rowed
    19	  each member it named, or disclosed it with its reason.
    20	
    21	  v7 -- the v6 pass (GPT-6 Astra in memory, Fable 5.1 in a mirror, Grok 4.7 and GLM 5.3 reading) found no defect in the
    22	  staged files.  It found C27's universal false -- a banned callable reached by an attribute path or an alias, a
    23	  mapping-pattern rest capture, a store into a frame's globals, a rebinding inside the `__main__' block the import read
    24	  never runs (all four seats) -- and a NON-LITERAL binding crashing the walk before the tally (V19's class: Grok 4.7, GLM
    25	  5.3, Fable 5.1); and members still open in the generating sets: list rows and entries, the ISO widths' other directions,
    26	  a NON-legacy cell carrying optional fields (graded clause (d) by Fable 5.1, (e) by GPT-6 Astra -- rowed either way), single
    27	  optional fields on a legacy cell, every style block, the counter keys as spellings, a numeric or bool d, a row with no id.
    28	  So v7 reads BOTH files' glyph sets by EXECUTING each as `__main__' on a fixture and taking its globals after the run -- the
    29	  effect, not the syntax, which closes the runtime-rebinding class at once -- refuses a non-literal binding instead of
    30	  crashing on it, pins each set's use COUNT, and rows each open member.
    31	    checker  ledger shape: an object; `rows' present and a list; row objects;           C21a-f, C21i (rows absent: {} and
    32	             `entries' absent = an empty row, else a list; entry objects                {"seats": []}), C21j (a row with no
    33	                                                                                        entries key: rc 0); C21l / C21m (a row,
    34	                                                                                        an entry that is a LIST); C23 (not JSON)
    35	             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
    36	             fields, EACH of the six a str, the count an int and not a bool, > 0       key sums), C17c-g (eight fields; a count
    37	                                                                                        of true, -1, 0, 1.0), C17h-m (each of the
    38	                                                                                        six positions numeric in turn), C17n (a
    39	                                                                                        None field), C21g (an object)
    40	             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
    41	             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C26b
    42	                                                                                        (a list), C28 / C28b (a ✓ padded at its
    43	                                                                                        start / its end), C2/C2b/C2c/C2d (each
    44	                                                                                        glyph, C2c/C2d isolated), C8 (hold), C24
    45	                                                                                        (a record, isolated)
    46	             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
    47	             ends; str() of d; a missing phase or seat keys as ""; the note's sha1     move), C25l-r (the leading end; a row id
    48	             over its UTF-8 text, after str()                                          with a trailing or a leading space);
    49	                                                                                        C15/C16 (the note); C26b; C29 (no phase,
    50	                                                                                        no seat: its line exact); C29b (a row with
    51	                                                                                        no id keys as "None"); C20b (a
    52	                                                                                        non-ASCII note: its line exact); C21k (a
    53	                                                                                        list note holding no token: refused)
    54	             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
    55	             the cutoff: inclusive; a date counts only when the ISO shape -- four      C3, C4, C12 (isolated: before / on /
    56	             digits, `-', two, `-', two -- OPENS it                                    after / far), C12s (a MATCHED identity
    57	                                                                                        dated 2026-10-17T12:00:00), C12w (MATCHED
    58	                                                                                        identities breaking the shape in one
    59	                                                                                        place -- a year of 5 or 3 digits, a month
    60	                                                                                        of 1 or 3, a day of 1, either separator:
    61	                                                                                        rc 0, which C12w reads; C12s reads rc
    62	                                                                                        too), C19a/b
    63	             output: cp1252-safe with backslash escapes; the summary line WHOLE, and   C1 (the only line), C11 (the line count,
    64	             ALONE on a clean run (its baseline number is the frozen total); each     the hint whole), C12 (the summary exact --
    65	             refusal line WHOLE -- identifiers in order, its reason; the hint WHOLE    at C12-on the two numbers differ); C3,
    66	                                                                                        C6, C9, C19a, C20, C20b, C29, C21k (the
    67	                                                                                        refusal line exact; C20's d escaped)
    68	             the glyph sets: ONE literal binding of DOMAIN and of D_CLASS, each the    C27 -- the EFFECT: BOTH files run as
    69	             four, used where they are used and nowhere else                            __main__ on a fixture, each glyph set read
    70	                                                                                        from the globals AFTER the run (any
    71	                                                                                        rebinding the run executes, whatever its
    72	                                                                                        syntax).  The SYNTAX, for what the run
    73	                                                                                        does not execute: one module-level LITERAL
    74	                                                                                        store of the name (a non-literal one is
    75	                                                                                        refused, never crashed on); a delete, a
    76	                                                                                        global, an import alias, a def or class,
    77	                                                                                        an except, match or mapping-rest name, a
    78	                                                                                        parameter, an attribute store of the name,
    79	                                                                                        a subscript store keyed by it or into a
    80	                                                                                        call; a banned builtin called by name OR
    81	                                                                                        attribute, or referenced uncalled;
    82	                                                                                        __dict__, __globals__, f_globals,
    83	                                                                                        f_locals; and each use COUNTED -- DOMAIN
    84	                                                                                        once in `in' and once as `" ".join's
    85	                                                                                        argument, D_CLASS once in `.get(' and once
    86	                                                                                        in `in' 
    87	    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (a ✓ padded at each
    88	             the answer a cell shows                                                    end), R1n (null), R3
    89	             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip,     R1 (OK), R1g (every simple legacy d,
    90	             whatever optional fields the answer carries                                null, both pads, the newline and NBSP
    91	                                                                                        cells included), R1w (all 29 whitespace
    92	                                                                                        cells, whole), R1e (a
    93	                                                                                        record beside it), R1f (a refused
    94	                                                                                        exemption first), R1o (a grade, a badge
    95	                                                                                        and evidence all present), R1o2 (a grade,
    96	                                                                                        evidence, a badge `s', each ALONE), R1q
    97	                                                                                        (neither date nor note); R1g also a
    98	                                                                                        number and a bool d
    99	             ONLY a legacy cell carries the class line                                  R1p (the ok, pend, bad and hold cells);
   100	                                                                                        R1p2 (ok, bad and hold cells carrying a
   101	                                                                                        grade, a badge and evidence); a tok, a
   102	                                                                                        live hold and an empty cell return before
   103	                                                                                        the class is computed (read)
   104	             the glyph: escaped and otherwise UNCHANGED (a pad kept); `?` for a blank  R1b, R1h (the glyph text exact), R1d
   105	             or whitespace-only d (any whitespace)                                     (space, tab, newline, NBSP); R1w (all 29
   106	                                                                                        str.isspace() code points)
   107	             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
   108	             its labels                                                                 string), R2b (the fixture ledger, whose
   109	                                                                                        pads, null and the counter-key spellings
   110	                                                                                        `total' and `legacy' count legacy)
   111	             the legend line; the two CSS rules the class adds, and no other rule in   R4; R5 (the two rules exact, and the ONLY
   112	             any style block naming the class                                          rules naming `legacy' in ANY style block,
   113	                                                                                        CSS escapes decoded)
   114	    Q2       the branches: rc 0 GOOD with the checker's first line; rc 1 BAD with the  W1 (the output whole: GOOD and the
   115	             refusal named; ANY other status BAD "could not run" with the checker's     summary, then the counter), W2 (the
   116	                                                                                        output whole, the entry named), W3 (rc 2),
   117	             FIRST line, stderr included                                                W7 (rc 7, a two-line message on stderr:
   118	                                                                                        the output whole), W8 (python absent: rc
   119	                                                                                        127), W9 (EVERY status 2-255: the else
   120	                                                                                        partition exhausted)
   121	             the checker absent -> BAD                                                  W6
   122	             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
   123	    DISCLOSED, each with its reason:
   124	      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
   125	        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
   126	        (GPT-6 Astra, v4 pass: the two figures are different searches);
   127	      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^'; the `[:10]' slice before the compare:
   128	        equivalent, a string sharing the cutoff's first ten characters is never smaller than it; `repr' of a non-string date:
   129	        equivalent to `str' for every JSON value;
   130	      a missing or null NOTE hashed as "" (`d_notenone'): 0 of the 1,356 frozen answers has one, and 0 entries anywhere carry
   131	        a note that is the literal string "None", which the mutant would hash a missing note as (GLM 5.3, v5 pass; measured);
   132	      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
   133	      the GOOD branch's `head -1': equivalent, the checker prints exactly one line on rc 0 (C1); the APPARATUS FAIL messages'
   134	        wording: DELIBERATELY unpinned display wording (C13 could carry it; their rc 2 is pinned; an emptied reason passes
   135	        every row -- `x_apparatusmsg', Fable 5.1, v5 pass, measured);
   136	      a CSS rule hiding glyphs WITHOUT naming the class (an attribute selector, a rule on every `.g'): R5 reads the rules
   137	        naming `legacy', in every style block, escapes decoded; HEAD's CSS is not this diff;
   138	      a change to the glyph sets C27's two reads cannot see -- a rebinding in a code path the fixture run does not execute
   139	        AND whose syntax the walk does not name (a runtime-built attribute name, a helper module), a C extension -- is
   140	        outside the contract -- and the renderer has a second, ACCIDENTAL closure worth keeping deliberately:
   141	        `summary()''s `n' is keyed by the four literal glyphs, so a fifth D_CLASS key CRASHES the generator (KeyError) on the
   142	        first entry that spells it -- loud, never a silent misclassification (Fable 5.1, v5 pass, measured);
   143	      the selection predicate widened by a DISJUNCT naming a spelling no fixture or ledger entry carries (`x["d"] in DOMAIN or
   144	        x["d"] == "ZXQ"'): C27 pins DOMAIN's definition and every use of it, not the predicate around it, and no finite row
   145	        set pins every novel spelling -- the plausible widenings, the ledger's own off-domain spellings, die on C1 (Fable 5.1,
   146	        v5 pass, measured: `+ ("OK",)' at the use site 80/96);
   147	      the use site INLINED: a literal standing for a glyph set at its use is now a removed use, which C27's COUNT sees; a
   148	        literal ADDED beside the Name (a disjunct) is the novel-spelling class above, and so is `summary()''s `n' given a
   149	        fifth key (the strip then fails to sum only for an entry spelling it -- Fable 5.1, v6 pass, measured);
   150	      a LIST d crashes the renderer at `D_CLASS.get' (unhashable) -- unreachable through a committed ledger: Q2 refuses a
   151	        new answer with a list d (C26b), no frozen answer carries one, and a hold or record returns before the class is
   152	        computed (GLM 5.3's member, read);
   153	      Q2's `$?' folds a child status of 256k to 0 -- unreachable from the checker's exits 0, 1 and 2 (Fable 5.1, v6 pass,
   154	        measured on a stub); the ISO digit class: `\\d' admits non-ASCII digits (a fullwidth `２'), equivalent on every
   155	        ASCII date; a lone CR in the baseline is not folded by the md5 pin -- no checkout writes one;
   156	      R3 is a PRESENCE pin as well as a mutant-render check: a mutant editing R3's find-text reds it by absence, which is
   157	        not a behavioural kill -- no mutant in the kill table rests on R3 alone (Fable 5.1, v6 pass, read);
   158	      a renderer that CRASHES on the shipped ledger is a kill: R2's census is guarded, so the run completes with its tally and
   159	        sentinel instead of dying INCOMPLETE (v5's controls crashed there, and the mutant driver scored a real kill as an
   160	        apparatus failure -- Fable 5.1, v5 pass, measured on a comment-only renderer);
   161	      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
   162	        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
   163	      the Q2 section header: `say' is stubbed in the W block, and it is display only;
   164	      the note-type scope of condition 2: "is it an answer" is `stage_tokens.is_answer', which tests membership on the untyped
   165	        note -- a list or dict note holding a token as an element or a key is a NON-answer and is skipped, as the renderer
   166	        also shows it (GPT-6 Astra, v5 pass, measured; K19's "nothing is skipped" was false); a list note holding no token is
   167	        an answer and is refused (C21k); a bool note: True rc 2, False rc 1 (Astra, measured).
   168	    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
   169	    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
   170	    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
   171	    two-edit design mutant d_dfold2, killed by C25d.  The `entries' default is ALSO rowed in isolation (98 of 912 shipped rows
   172	    carry no `entries' key; C21j's ledger holds only its two rows).  C20b is NOT isolated: its answer joins the shipped
   173	    ledger, whose 34 non-ASCII frozen notes already fail a latin-1 encode -- it is a named witness of that kill, not the sole
   174	    carrier (GPT-6 Astra and Grok 4.7, v6 pass; the v6 text called it isolated).
   175	
   176	  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
   177	  v4 passes' findings):
   178	    C1   shipped ledger, shipped baseline (md5 pin live): rc 0 and the summary line EXACTLY
   179	    C2 / C2b  an answer ON / AFTER the cutoff with a valid glyph (positive)                       -> 0 / 0
   180	    C2c / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
   181	    C3   an answer ON the cutoff with "OK" (inclusive) -- its refusal line EXACTLY                  -> 1
   182	    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
   183	    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
   184	    C6   an UNDATED answer with "N/A" -- its refusal line EXACTLY (date "(none)", no ISO clause)    -> 1
   185	    C7   an answer after the cutoff with NO `d`                                                     -> 0
   186	    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
   187	    C9   an identical copy of a frozen entry -- its refusal line EXACTLY                            -> 1
   188	    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
   189	    C11  the baseline emptied (override): every shipped off-domain answer named, the summary EXACTLY, the hint -> 1
   190	    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after / far   -> 0 / 1 / 1 / 1,
   191	         each with its summary line EXACTLY (on/after/far: within = baseline - 1)
   192	    C12s a MATCHED identity dated "2026-10-17T12:00:00" (the ISO shape opens it)                    -> 1
   193	    C13  an unreadable baseline (override)                                                          -> 2
   194	    C14  a new answer with an explicit BLANK d                                                      -> 1
   195	    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat, date, d) -> 1
   196	    C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
   197	    C17  a misshapen baseline (override; counts as strings)                                         -> 2
   198	    C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
   199	    C17c-g  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0  -> 2 each
   200	    C17h-m  the same, each of the six string positions numeric in turn: row, note sha, phase, seat, date, d     -> 2 each
   201	    C17n the same, a None date (`isinstance(v, (str, type(None)))' would pass it)                    -> 2
   202	    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
   203	    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
   204	    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
   205	         the date NAMED as not ISO                                                                  -> 1 / 1
   206	    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback, its line EXACT
   207	         with the d backslash-escaped                                                               -> 1
   208	    C20b a new answer whose NOTE is non-ASCII ("café — ✓") -- rc 1, its line EXACT (the note's UTF-8 sha)  -> 1
   209	    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
   210	         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
   211	         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
   212	    C21j a ledger whose row carries NO entries key (an empty row), beside a valid one               -> 0
   213	    C21k a new answer whose note is a LIST holding no token -- an answer, refused, its line EXACT  -> 1
   214	    C21l / C21m  a misshapen ledger: a row that is a LIST / an entry that is a LIST -- `(dict, list)' at either shape test
   215	         walked them (a list ENTRY as a non-entry, GREEN; Fable 5.1, v6 pass, measured)       -> 2 / 2
   216	    C29b an off-domain answer in a row with NO id -- keyed and printed as "None", its line EXACT    -> 1
   217	    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
   218	    C23  a ledger that is not JSON                                                                  -> 2
   219	    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
   220	    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
   221	         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
   222	         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
   223	         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
   224	    C26  a new answer with an explicit "d": null                                                     -> 1
   225	    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
   226	    C27  DOMAIN and D_CLASS: one LITERAL binding each, every named binding form refused, each use COUNTED, and BOTH
   227	         files' EFFECTIVE set -- read after running each as __main__ on a fixture -- exactly ✓ ✕ ⏸ … (D_CLASS's classes too)
   228	    C28 / C28b  a new answer BEFORE the cutoff with a glyph padded at its START (" ✓") / its END ("✓ ")  -> 1 / 1
   229	    C29  a new answer with NO phase and NO seat -- refused, its line EXACT (both identifiers empty)   -> 1
   230	    C12w MATCHED identities whose date breaks the ISO shape in ONE place -- a five-digit year, a one-digit month, a
   231	         one-digit day, a `/' for the first separator, for the second -- each in its fixture baseline, so only the shape
   232	         decides                                                                                    -> 0 each
   233	  RENDERER:
   234	    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
   235	    R1b  an escapable `d` ("<b>&") renders escaped
   236	    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
   237	    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
   238	    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
   239	    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
   240	    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
   241	         "\n", "\xa0", null), the date, the note
   242	    R1h  a ✓ padded at its start (" ✓") and at its end ("✓ ") each renders legacy, its glyph text EXACTLY as written
   243	    R1o  a legacy answer carrying a grade, a badge and evidence: its WHOLE tooltip, the class line first
   244	    R1o2 legacy answers carrying a grade ALONE, evidence ALONE, the badge `s' ALONE: each WHOLE tooltip, the line first
   245	    R1p2 ok, bad and hold answers carrying a grade, a badge and evidence: each WHOLE tooltip, NO class line
   246	    R1p  the NON-legacy answer cells -- ok, pend, bad, hold -- carry NO class line: each tooltip is the date and note alone
   247	    R1q  a legacy answer with NO date and NO note (d "BARE"): its tooltip is the class line alone
   248	    R1w  EVERY str.isspace() code point alone as d (29 in this python) shows `?' and carries its WHOLE tooltip -- the
   249	         whitespace set exhausted
   250	    R1n  an explicit "d": null renders legacy with the glyph "None", not …
   251	    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
   252	         own count by exact membership, and its labels
   253	    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
   254	    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
   255	         a kill
   256	    R4   the legend carries the legacy line EXACTLY
   257	    R5   the page carries the two CSS rules the class adds, EXACTLY, and NO other rule in its style block names `legacy'
   258	  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
   259	  carry its BRANCH's own words):
   260	    W1   the shipped ledger                    -> exactly "GOOD <the summary line>" and "FAILURES 0"
   261	    W2   a new off-domain answer               -> BAD, its WHOLE output: the first line, every line of the checker's
   262	         output indented, the counter
   263	    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
   264	    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
   265	    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
   266	    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
   267	    W7   a checker that exits 7 with a TWO-line message on STDERR -> exactly "BAD ... could not run (rc 7): <its FIRST line>"
   268	         and "FAILURES 1"
   269	    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
   270	    W9   EVERY status 2-255, a stub exiting each in turn (254 runs)    -> each exactly "BAD ... could not run (rc N): <its
   271	         first line>" and the counter 1 -- the `else' partition EXHAUSTED
   272	"""
   273	import collections, copy, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile
   274	
   275	if hasattr(sys.stdout, "reconfigure"):          # this file prints glyphs (R2's strip); run it anywhere, piped or not
   276	    sys.stdout.reconfigure(encoding="utf-8")
   277	
   278	HERE = os.path.dirname(os.path.abspath(__file__))
   279	REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
   280	PIPE = os.path.join(REPO, "tools", "pipeline")
   281	CHECKER = os.environ.get("CTL_CHECKER") or os.path.join(PIPE, "check_entry_domain.py")
   282	RENDER = os.environ.get("CTL_RENDER") or os.path.join(PIPE, "gen_dashboard.py")
   283	PRE = os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")
   284	BEFORE = os.path.join(HERE, "gen_dashboard_before.py")      # HEAD's renderer at the landing, preserved
   285	#  the baseline travels WITH the checker under test: staged runs keep it beside the staged checker, and on the tree the two
   286	#  directories are the same
   287	BASELINE = os.path.join(os.path.dirname(os.path.abspath(CHECKER)), "entry_domain_baseline.json")
   288	if not os.path.exists(BASELINE):
   289	    BASELINE = os.path.join(PIPE, "entry_domain_baseline.json")
   290	LEDGER = os.path.join(PIPE, "ledger.json")
   291	sys.path.insert(0, PIPE)
   292	import stage_tokens as st  # noqa: E402
   293	
   294	T = tempfile.mkdtemp()
   295	res = []
   296	
   297	
   298	def say(label, ok, detail=""):
   299	    res.append(ok)
   300	    tag, rest = label.split(" ", 1)
   301	    print("%-4s %-76s %s  %s" % (tag, rest, "ok" if ok else "NO", detail))
   302	
   303	
   304	def wjson(name, obj):
   305	    p = os.path.join(T, name)
   306	    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
   307	    return p
   308	
   309	
   310	def pipe_copy(tag, baseline_text=None):
   311	    """a temp copy of the pipeline dir holding the checker under test, stage_tokens.py and a baseline (default: shipped)"""
   312	    d = os.path.join(T, "pipe_" + tag)
   313	    os.makedirs(d, exist_ok=True)
   314	    shutil.copy(CHECKER, os.path.join(d, "check_entry_domain.py"))
   315	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   316	    b = os.path.join(d, "entry_domain_baseline.json")
   317	    if baseline_text is None:
   318	        shutil.copy(BASELINE, b)
   319	    else:
   320	        io.open(b, "w", encoding="utf-8", newline="").write(baseline_text)
   321	    return os.path.join(d, "check_entry_domain.py")
   322	
   323	
   324	def run_checker(ledger_path, baseline_path=None, checker=None):
   325	    #  NO PYTHONIOENCODING: the precommit sets none, so the checker must survive a cp1252 pipe (Fable 5.1, pass 2)
   326	    env = dict(os.environ, GXLEDGER=ledger_path)
   327	    for k in ("GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
   328	        env.pop(k, None)
   329	    if baseline_path is not None:
   330	        env["GXDOMAIN_BASELINE"] = baseline_path
   331	    r = subprocess.run([sys.executable, checker or DEFAULT_CHECKER], capture_output=True, env=env)
   332	    out = (r.stdout + r.stderr).decode("cp1252", "replace")
   333	    return r.returncode, out.strip().splitlines()
   334	
   335	
   336	DEFAULT_CHECKER = pipe_copy("default")          # the checker under test, beside the SHIPPED baseline (md5 pin live)
   337	L0 = json.load(io.open(LEDGER, encoding="utf-8"))
   338	ROW0 = L0["rows"][0]["id"]
   339	N_OFF = sum(1 for r in L0["rows"] for x in r.get("entries", [])
   340	            if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…") and st.is_answer(x))
   341	
   342	
   343	def with_entries(entries, ledger=None):
   344	    L = copy.deepcopy(ledger or L0)
   345	    for row, e in entries:
   346	        for r in L["rows"]:
   347	            if r["id"] == row:
   348	                r.setdefault("entries", []).append(e)
   349	    return wjson("l_%d.json" % len(res), L)
   350	
   351	
   352	def ans(date, **kw):
   353	    e = {"phase": "review", "seat": "grok", "note": "a control entry"}
   354	    if date is not None:
   355	        e["date"] = date
   356	    e.update(kw)
   357	    return e
   358	
   359	
   360	def sha16(note):
   361	    return hashlib.sha1(str(note or "").encode("utf-8")).hexdigest()[:16]
   362	
   363	
   364	WHY_CUT = "dated on or after the cutoff 2026-10-17"
   365	WHY_CEIL = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
   366	WHY_ISO = "; its date is not ISO YYYY-MM-DD"
   367	
   368	
   369	def offline(row, e, why):
   370	    """the WHOLE refusal line the checker must print for entry e of row -- identifiers in their order, then the reason
   371	    (v4 read only the count of lines, so a reason replaced or row and phase swapped passed -- Fable 5.1, GPT-6 Astra, v4 pass)"""
   372	    dt = e.get("date")
   373	    dt = dt if isinstance(dt, str) else ("" if dt is None else repr(dt))
   374	    return "OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s" % (
   375	        row, e.get("phase") or "", e.get("seat") or "", dt or "(none)", str(e["d"]), sha16(e.get("note")), why)
   376	
   377	
   378	def cp(s):
   379	    """what the checker's cp1252 stdout, reconfigured errors="backslashreplace", carries for s -- as run_checker decodes it"""
   380	    return s.encode("cp1252", "backslashreplace").decode("cp1252")
   381	
   382	
   383	def summary_line(n_cur, n_within, n_base):
   384	    return ("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff 2026-10-17 inclusive"
   385	            % (n_cur, n_within, n_base))
   386	
   387	
   388	def ident(row, e):
   389	    return [row, e.get("phase") or "", e.get("seat") or "", e.get("date") if isinstance(e.get("date"), str) else "",
   390	            str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]
   391	
   392	
   393	print("# dashokclass controls (v6) -- checker %s | renderer %s | precommit %s | baseline %s"
   394	      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
   395	         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
   396	# ------------------------------------------------------------------ the checker
   397	rc, out = run_checker(LEDGER)
   398	first = out[0] if out else ""
   399	#  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
   400	#  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
   401	#  v5: the WHOLE line -- "inclusive" dropped from it passed all 72 v4 controls (Fable 5.1, v4 pass)
   402	#  v6: and ALONE -- the hint printed on a clean run passed all 96 v5 controls
   403	say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY, and the only line",
   404	    rc == 0 and out == [summary_line(N_OFF, N_OFF, N_OFF)], "rc %d: %d lines; %s" % (rc, len(out), first))
   405	for lab, ent, want in [
   406	    ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
   407	    ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
   408	    ("C3 ON the cutoff, d OK (inclusive)", ans("2026-10-17", d="OK"), 1),
   409	    ("C4 AFTER the cutoff, d OK", ans("2026-10-18", d="OK"), 1),
   410	    ("C5 a new answer BEFORE the cutoff, d OK (back-dated)", ans("2026-09-01", d="OK", seat="minimax"), 1),
   411	    ("C6 undated, d N/A", ans(None, d="N/A"), 1),
   412	    ("C7 after the cutoff, NO d", ans("2026-10-18"), 0),
   413	    ("C8 a HELD marker after the cutoff, d HELD", ans("2026-10-18", d="HELD", note=st.HELD + " grok] waiting"), 0),
   414	    ("C14 a new answer with an explicit BLANK d", ans("2026-10-10", d=""), 1),
   415	    ('C19a a new answer dated "10/18/2026", d OK', ans("10/18/2026", d="OK"), 1),
   416	    ("C19b a new answer with a NUMERIC date, d OK", ans(20261018, d="OK"), 1),
   417	    ("C20 a new answer with a non-ASCII d (cp1252 stdout, no traceback)", ans("2026-10-18", d="✗"), 1),
   418	    #  an explicit "d": null is PRESENT and off-domain -- `if x.get("d") is None` would treat it as missing (Fable 5.1, v3 pass)
   419	    ("C26 a new answer with an explicit null d", ans("2026-10-10", d=None), 1),
   420	    #  v5: a LIST d -- the key takes str() of d; without it the Counter raises on an unhashable key (Fable 5.1, v4 pass)
   421	    ("C26b a new answer whose d is a LIST", ans("2026-10-10", d=["OK"]), 1),
   422	    #  v5: a PADDED glyph is outside the four for the checker as for the renderer (R1h) -- `str(d).strip() in DOMAIN` passed
   423	    #  all 72 v4 controls (Fable 5.1, Grok 4.7, v4 pass)
   424	    ("C28 a new answer BEFORE the cutoff with a padded glyph ' ✓'", ans("2026-10-10", d=" ✓"), 1),
   425	    #  v6: the OTHER end -- `str(x["d"]).rstrip() in DOMAIN' passed all 96 v5 controls (GPT-6 Astra, v5 pass)
   426	    ("C28b a new answer BEFORE the cutoff with a glyph padded at its END '✓ '", ans("2026-10-10", d="✓ "), 1),
   427	    #  v6: a NON-ASCII note -- its sha is over the note's UTF-8; a latin-1 encode raises (or rehashes) on it (GLM 5.3, v5 pass)
   428	    ("C20b a new answer whose note is non-ASCII", ans("2026-10-10", d="OK", note="café — ✓"), 1),
   429	    #  v6: no phase, no seat -- each keys and prints as "" ; dropping the `or ""' printed "None" and passed all 96 v5 controls
   430	    #  (GLM 5.3, v5 pass, measured)
   431	    ("C29 a new answer with no phase and no seat", {"date": "2026-10-10", "d": "OK", "note": "no phase or seat"}, 1),
   432	    #  v6: a LIST note holding no token is an ANSWER (is_answer finds no token in it) and is refused, never skipped; a
   433	    #  mutant dropping the str() before the hash raised on it instead (Fable 5.1 measured rc 1 on the v4 pass)
   434	    ("C21k a new answer whose note is a list holding no token", ans("2026-10-10", d="OK", note=["a list note"]), 1),
   435	]:
   436	    rc, out = run_checker(with_entries([(ROW0, ent)]))
   437	    tb = any("Traceback" in l for l in out)
   438	    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
   439	    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
   440	    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
   441	    #  v5: the WHOLE refusal line for C3 (the cutoff reason), C6 (an undated entry: "(none)", no ISO clause) and C19a (the
   442	    #  ISO clause) -- v4 read only rc and the line count (Fable 5.1, GPT-6 Astra, v4 pass)
   443	    #  v6: also C20 (its d backslash-escaped by the cp1252 reconfigure -- "replace" printed `?' and passed all 96 v5
   444	    #  controls), C20b, C29 and C21k
   445	    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO, "C20": WHY_CUT, "C20b": WHY_CEIL, "C29": WHY_CEIL,
   446	                 "C21k": WHY_CEIL}.get(lab.split()[0])
   447	    offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   448	    exact = exact_why is None or offl == [cp(offline(ROW0, ent, exact_why))]
   449	    say(lab, rc == want and not tb and why and exact, "rc %d (want %d)%s%s%s" % (
   450	        rc, want, " TRACEBACK" if tb else "", "" if why else " REASON NOT NAMED",
   451	        "" if exact else " LINE NOT EXACT: %r" % (offl[:1],)))
   452	#  C2c/C2d ISOLATED (GPT-6 Astra, v3 pass): the shipped ledger already carries 21 ⏸ and 35 … answers, so dropping either glyph
   453	#  from DOMAIN reddened the v3 rows without their own entry; a ledger holding ONLY the fixture entry makes each its own witness
   454	for lab, ent in (("C2c AFTER the cutoff, d ⏸, in a ledger holding only it (positive)", ans("2026-10-18", d="⏸")),
   455	                 ("C2d AFTER the cutoff, d …, in a ledger holding only it (positive)", ans("2026-10-18", d="…"))):
   456	    rc, out = run_checker(wjson("l_iso_%d.json" % len(res), {"rows": [{"id": "ctliso", "entries": [ent]}]}))
   457	    say(lab, rc == 0, "rc %d" % rc)
   458	#  C24 ISOLATED (GPT-6 Astra, v4 pass): the shipped ledger carries five off-domain NOTSEAT records, so `st.is_held(x)` for
   459	#  `not st.is_answer(x)` reddened C24 for the LEDGER's reason; a ledger holding only the record makes it its own witness
   460	rc, out = run_checker(wjson("l_iso_c24.json", {"rows": [{"id": "ctliso", "entries": [
   461	    ans("2026-10-18", d="OK", note=st.NOTSEAT + " a main-loop record")]}]}))
   462	say("C24 a non-answer RECORD (NOTSEAT) after the cutoff, d OK, in a ledger holding only it", rc == 0, "rc %d" % rc)
   463	# a frozen entry, found from the shipped baseline: copied (C9), rewritten (C10), refilled (C15), note-edited (C16), ev-edited (C22)
   464	base = [json.loads(l.rstrip(",\n")) for l in io.open(BASELINE, encoding="utf-8") if l.startswith("[\"")]
   465	k0 = base[0]
   466	
   467	
   468	def find_frozen(L):
   469	    for r in L["rows"]:
   470	        if r["id"] != k0[0]:
   471	            continue
   472	        for x in r["entries"]:
   473	            if "d" in x and ident(r["id"], x) == k0[:6]:
   474	                return x
   475	    raise SystemExit("APPARATUS FAIL: the first baseline identity is not in the shipped ledger")
   476	
   477	
   478	src = find_frozen(L0)
   479	rc, out = run_checker(with_entries([(k0[0], dict(src))]))
   480	offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   481	say("C9 an identical copy of a frozen entry (%s %s %s %s %r): its refusal line EXACTLY" % tuple(k0[:5]),
   482	    rc == 1 and offl == [offline(k0[0], src, WHY_CEIL)], "rc %d; %r" % (rc, offl[:1]))
   483	L = copy.deepcopy(L0); find_frozen(L)["d"] = "✓"
   484	rc, out = run_checker(wjson("l_rewrite.json", L))
   485	say("C10 a frozen entry rewritten to a glyph", rc == 0, "rc %d" % rc)
   486	refill = dict(src); refill["note"] = "a different answer reusing the converted entry's slot"
   487	rc, out = run_checker(with_entries([(k0[0], refill)], ledger=L))
   488	say("C15 REFILL: the converted entry's (row, phase, seat, date, d) reused", rc == 1, "rc %d" % rc)
   489	L2 = copy.deepcopy(L0); f = find_frozen(L2); f["note"] = (f.get("note") or "") + " (a later correction)"
   490	rc, out = run_checker(wjson("l_noteedit.json", L2))
   491	say("C16 a frozen entry's note edited, d left off-domain", rc == 1, "rc %d" % rc)
   492	L3 = copy.deepcopy(L0); f = find_frozen(L3); f["ev"] = (f.get("ev") or "") + " (a corrected path)"
   493	rc, out = run_checker(wjson("l_evedit.json", L3))
   494	say("C22 a frozen entry's ev edited, outside the six fields (positive)", rc == 0, "rc %d" % rc)
   495	#  C25: each key field of the FROZEN entry edited by its least visible change.  A mutant normalising one field on the ledger's
   496	#  side -- `v[:10]` on the date, `.strip()`, `.lower()` -- passed every v3 control (GPT-6 Astra, v3 pass: the date suffix)
   497	OTHER_ROW = next(r["id"] for r in L0["rows"] if r["id"] != k0[0])
   498	for tag, field, how, fn in (("a", "date", "suffixed T12:00:00", lambda v: v + "T12:00:00"),
   499	                            ("b", "date", "a trailing space", lambda v: v + " "),
   500	                            ("c", "d", "a trailing space", lambda v: v + " "),
   501	                            ("d", "d", "its case swapped", lambda v: v.swapcase()),
   502	                            ("e", "note", "a trailing space", lambda v: v + " "),
   503	                            ("f", "note", "its case swapped", lambda v: v.swapcase()),
   504	                            ("g", "seat", "a trailing space", lambda v: v + " "),
   505	                            ("h", "seat", "upper-cased", lambda v: v.upper()),
   506	                            ("i", "phase", "a trailing space", lambda v: v + " "),
   507	                            ("j", "phase", "upper-cased", lambda v: v.upper())):
   508	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   509	    assert fn(fe[field]) != fe[field], (tag, field)
   510	    fe[field] = fn(fe[field])
   511	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   512	    say("C25%s a frozen entry's %s, %s" % (tag, field, how), rc == 1, "rc %d" % rc)
   513	Le = copy.deepcopy(L0); fe = find_frozen(Le)
   514	for r in Le["rows"]:
   515	    if r["id"] == k0[0]:
   516	        r["entries"] = [x for x in r["entries"] if x is not fe]
   517	    if r["id"] == OTHER_ROW:
   518	        r.setdefault("entries", []).append(fe)
   519	rc, out = run_checker(wjson("l_key_k.json", Le))
   520	say("C25k a frozen entry moved to another row (%s)" % OTHER_ROW, rc == 1, "rc %d" % rc)
   521	#  v5: the LEADING end of every field, and the row id at both ends -- `.lstrip()` on the date, d, seat, phase or note, and
   522	#  `str(r.get("id")).strip()`, each passed all 72 v4 controls, which edited only the trailing end (Fable 5.1, Grok 4.7, GPT-6
   523	#  Astra, v4 pass)
   524	
   525	
   526	def moved_to(new_id):
   527	    Lm = copy.deepcopy(L0); fm = find_frozen(Lm)
   528	    for r in Lm["rows"]:
   529	        if r["id"] == k0[0]:
   530	            r["entries"] = [x for x in r["entries"] if x is not fm]
   531	    Lm["rows"].append({"id": new_id, "title": "row id control", "sev": "LOW", "state": "open", "commits": "", "entries": [fm]})
   532	    return Lm
   533	
   534	
   535	rc, out = run_checker(wjson("l_key_l.json", moved_to(k0[0] + " ")))
   536	say("C25l a frozen entry moved to a row whose id has a TRAILING space", rc == 1, "rc %d" % rc)
   537	for tag, field in (("m", "date"), ("n", "d"), ("o", "note"), ("p", "seat"), ("q", "phase")):
   538	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   539	    fe[field] = " " + fe[field]
   540	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   541	    say("C25%s a frozen entry's %s with a LEADING space" % (tag, field), rc == 1, "rc %d" % rc)
   542	rc, out = run_checker(wjson("l_key_r.json", moved_to(" " + k0[0])))
   543	say("C25r a frozen entry moved to a row whose id has a LEADING space", rc == 1, "rc %d" % rc)
   544	rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
   545	nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
   546	#  and the SUMMARY line on this dirty ledger: it was pinned only on the clean one, where "passes" and "entries" agree, so
   547	#  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
   548	s11 = summary_line(N_OFF, 0, 0)
   549	f11 = out[0] if out else ""
   550	#  v6: the hint WHOLE -- a false "all records need classification" passed the v5 prefix test (GPT-6 Astra, v5 pass) -- and the
   551	#  output exactly the summary, one line per refusal, the hint
   552	HINT = cp("  -> give each a `d` from ✓ ✕ ⏸ … (or omit `d`, which renders as …); a non-answer record is exempt").strip()
   553	hint = bool(out) and out[-1].strip() == HINT
   554	say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint WHOLE",
   555	    rc == 1 and nb == N_OFF and f11 == s11 and hint and len(out) == N_OFF + 2, "rc %d, %d of %d named, %d lines; summary %s; hint %s"
   556	    % (rc, nb, N_OFF, len(out), "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else repr(out[-1][:90] if out else "")))
   557	# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
   558	#  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
   559	for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
   560	                      ("far", "2027-01-01", 1)):
   561	    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
   562	    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
   563	    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   564	    #  v5: the summary EXACTLY -- here the fixture baseline holds N_OFF + 1 and a refused entry leaves N_OFF within, so the
   565	    #  baseline number differs from the within-count; C1 and C11 cannot tell them apart (1356/1356, 0/0), and printing the
   566	    #  within-count there passed all 72 v4 controls (Fable 5.1, v4 pass)
   567	    s12 = summary_line(N_OFF + 1, N_OFF + 1 if want == 0 else N_OFF, N_OFF + 1)
   568	    f12 = out[0] if out else ""
   569	    say("C12 cutoff isolated: a FROZEN identity dated %s (%s), the summary EXACTLY" % (dt, tag), rc == want and f12 == s12,
   570	        "rc %d (want %d); summary %s" % (rc, want, "ok" if f12 == s12 else repr(f12[:100])))
   571	#  C12s: a MATCHED identity whose date the ISO shape OPENS -- `^...$' on the shape refused nothing and passed all 72 v4
   572	#  controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass); the checker reads the first ten characters
   573	e = ans("2026-10-17T12:00:00", d="OK", seat="kimi", note="cutoff isolation suffixed")
   574	fb = wjson("b_cut_suffixed.json", base + [ident(ROW0, e) + [1]])
   575	rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   576	say("C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00", rc == 1, "rc %d (want 1)" % rc)
   577	#  C12w (v6): the ISO SHAPE's widths and separators -- `\d{1,2}' for the month passed all 96 v5 controls, reading
   578	#  "2026-9-1" as a date after the cutoff (GPT-6 Astra, v5 pass).  Each identity is FROZEN and breaks the shape in one place,
   579	#  each chosen to compare at or after the cutoff if the shape were loosened there, so only the shape decides: rc 0
   580	#  (a one-edit mutant loosens ONE separator, so each has its own row: one date breaking both would miss either alone)
   581	#  v7: the other DIRECTION of each width -- `\d{3,4}' read a frozen 999-10-17 as a date after the cutoff, `\d{2,3}' a frozen
   582	#  2026-100-17, and both passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass); a day of three digits is equivalent
   583	#  (the pattern has no end anchor, so `\d{2}' already reads 2026-10-178's first two)
   584	for tag, dt in (("year", "99999-10-18"), ("month", "2026-9-17"), ("day", "2026-10-9"), ("sep1", "2026/10-18"),
   585	                ("sep2", "2026-10/18"), ("year3", "999-10-17"), ("month3", "2026-100-17")):
   586	    e = ans(dt, d="OK", seat="kimi", note="iso shape " + tag)
   587	    fb = wjson("b_cut_w_%s.json" % tag, base + [ident(ROW0, e) + [1]])
   588	    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   589	    say("C12w the ISO shape's %s: a FROZEN identity dated %s is not read as a date" % (tag, dt), rc == 0, "rc %d (want 0)" % rc)
   590	rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
   591	say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
   592	#  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
   593	#  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
   594	#  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
   595	import ast  # noqa: E402
   596	#  v5 counted the Name stores of each name; v6 walks EVERY binding form and EVERY use.  `globals()["DOMAIN"] = ...' and
   597	#  `D_CLASS.update(ZXQ="ok")' each passed all 96 v5 controls -- the first is no Name store, the second mutates the dict
   598	#  without rebinding it (GLM 5.3, GPT-6 Astra, v5 pass, measured).  So: exactly one binding, a module-level assignment of a
   599	#  literal; no other binding form of the name (a store or delete, a global or nonlocal, an import alias, a def or class, an
   600	#  except or match name, a parameter, an attribute or subscript store keyed by it); no call to the builtins that rebind by
   601	#  name or by string (globals, vars, locals, setattr, delattr, exec, eval, compile, __import__) and no __dict__ / __globals__;
   602	#  and every USE of the name on a whitelist -- DOMAIN only in `in' / `not in' and as `" ".join(...)''s argument, D_CLASS only
   603	#  as `D_CLASS.get(...)' and in `in' / `not in'.  The checker is import-safe, so its EFFECTIVE DOMAIN is also read by importing
   604	#  it; the renderer renders on import, so it is read by the walk alone.
   605	BANNED = {"globals", "vars", "locals", "setattr", "delattr", "exec", "eval", "compile", "__import__"}
   606	
   607	
   608	def walk_name(path, name, use_ok):
   609	    tree = ast.parse(io.open(path, encoding="utf-8").read())
   610	    parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
   611	    probs = []
   612	    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
   613	    top = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
   614	           and n.targets[0].id == name]
   615	    if len(stores) != 1 or len(top) != 1:
   616	        probs.append("%d stores, %d module-level assignments" % (len(stores), len(top)))
   617	    for n in ast.walk(tree):
   618	        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Del):
   619	            probs.append("del")
   620	        elif isinstance(n, (ast.Global, ast.Nonlocal)) and name in n.names:
   621	            probs.append("global/nonlocal")
   622	        elif isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split(".")[0]) == name for a in n.names):
   623	            probs.append("import alias")
   624	        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name:
   625	            probs.append("def/class")
   626	        elif isinstance(n, ast.ExceptHandler) and n.name == name:
   627	            probs.append("except name")
   628	        elif isinstance(n, ast.arg) and n.arg == name:
   629	            probs.append("parameter")
   630	        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == name:
   631	            probs.append("match name")
   632	        elif isinstance(n, ast.Attribute) and n.attr == name and not isinstance(n.ctx, ast.Load):
   633	            probs.append("attribute store")
   634	        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load) and isinstance(n.slice, ast.Constant)
   635	              and n.slice.value == name):
   636	            probs.append("subscript store keyed by the name")
   637	        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in BANNED:
   638	            probs.append("call to " + n.func.id)
   639	        #  v7: by ATTRIBUTE (`builtins.exec', `builtins.setattr', `object.__setattr__'), by an uncalled REFERENCE (`_e =
   640	        #  exec'), a mapping-pattern REST capture, a subscript store into a CALL or a frame's globals -- each changed the
   641	        #  renderer's effective D_CLASS past the v6 walk (GPT-6 Astra, GLM 5.3, Grok 4.7, Fable 5.1, v6 pass)
   642	        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in BANNED_ATTR:
   643	            probs.append("call to ." + n.func.attr)
   644	        elif (isinstance(n, ast.Name) and n.id in BANNED and isinstance(n.ctx, ast.Load)
   645	              and not (isinstance(parent.get(n), ast.Call) and parent.get(n).func is n)):
   646	            probs.append("a reference to " + n.id)
   647	        elif isinstance(n, ast.MatchMapping) and n.rest == name:
   648	            probs.append("match rest")
   649	        elif (isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load)
   650	              and (isinstance(n.value, ast.Call) or (isinstance(n.value, ast.Attribute) and n.value.attr in DUNDER))):
   651	            probs.append("a subscript store into a call or a namespace")
   652	        elif isinstance(n, ast.Attribute) and n.attr in DUNDER:
   653	            probs.append(n.attr)
   654	        elif isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and not use_ok(n, parent):
   655	            probs.append("a use at line %d" % n.lineno)
   656	    #  v7: a NON-LITERAL store is refused, never crashed on -- `ast.literal_eval' raised on `tuple((...))' and the run died
   657	    #  before its tally, the driver scoring the kill INCOMPLETE (V19's class; Grok 4.7, GLM 5.3, Fable 5.1, v6 pass)
   658	    lit = None
   659	    if len(top) == 1:
   660	        try:
   661	            lit = ast.literal_eval(top[0].value)
   662	        except (ValueError, SyntaxError, TypeError):
   663	            probs.append("a non-literal binding")
   664	    uses = collections.Counter(use_ok(n, parent) for n in ast.walk(tree)
   665	                               if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and use_ok(n, parent))
   666	    return lit, probs, uses
   667	
   668	
   669	BANNED_ATTR = ("exec", "eval", "globals", "vars", "locals", "setattr", "delattr", "__import__", "__setattr__", "__delattr__")
   670	DUNDER = ("__dict__", "__globals__", "f_globals", "f_locals")
   671	
   672	
   673	def in_compare(n, parent):
   674	    p = parent.get(n)
   675	    return (isinstance(p, ast.Compare) and n in p.comparators
   676	            and isinstance(p.ops[p.comparators.index(n)], (ast.In, ast.NotIn)))
   677	
   678	
   679	#  each use returns its KIND (v7: the kinds are COUNTED -- a use site inlined with a literal is a removed use)
   680	def dom_use(n, parent):
   681	    p = parent.get(n)
   682	    if in_compare(n, parent):
   683	        return "in"
   684	    return "join" if (isinstance(p, ast.Call) and p.args == [n] and isinstance(p.func, ast.Attribute)
   685	                      and p.func.attr == "join" and isinstance(p.func.value, ast.Constant)) else None
   686	
   687	
   688	def dcls_use(n, parent):
   689	    p = parent.get(n)
   690	    if in_compare(n, parent):
   691	        return "in"
   692	    return "get" if (isinstance(p, ast.Attribute) and p.attr == "get" and isinstance(parent.get(p), ast.Call)
   693	                     and parent.get(p).func is p) else None
   694	
   695	
   696	dom, dprobs, duses = walk_name(CHECKER, "DOMAIN", dom_use)
   697	dcls, cprobs, cuses = walk_name(RENDER, "D_CLASS", dcls_use)
   698	#  v7: the EFFECTIVE sets, read by EXECUTING each file as __main__ on a fixture and taking its globals after the run -- any
   699	#  rebinding the run executes, in the module body or the main block, whatever its syntax.  v6 imported the checker, so a
   700	#  rebinding under `if __name__ == "__main__"' was invisible to it (GLM 5.3), and read nothing of the renderer, so
   701	#  `builtins.setattr' and a frame-globals store passed (Fable 5.1, v6 pass, measured).
   702	#  the run is a real MODULE registered as sys.modules["__main__"], as a script's is -- a bare namespace dict let
   703	#  `setattr(sys.modules[__name__], ...)' land on the wrapper instead of the run
   704	RUN_MAIN = ("import io, sys, types\npath, name = sys.argv[1], sys.argv[2]\nsys.argv = [path] + sys.argv[3:]\n"
   705	            "sys.path.insert(0, __import__('os').path.dirname(path))\n"
   706	            "mod = types.ModuleType('__main__')\nmod.__file__ = path\nsys.modules['__main__'] = mod\n"
   707	            "try:\n    exec(compile(io.open(path, encoding='utf-8').read(), path, 'exec'), mod.__dict__)\nexcept SystemExit:\n    pass\n"
   708	            "print('EFFECTIVE ' + ascii(mod.__dict__.get(name)))\n")
   709	
   710	
   711	def effective(path, name, ledger, *args):
   712	    env = dict(os.environ, GXLEDGER=ledger, PYTHONIOENCODING="utf-8")
   713	    env.pop("GXDOMAIN_BASELINE", None)
   714	    r = subprocess.run([sys.executable, "-c", RUN_MAIN, path, name] + list(args), capture_output=True, text=True,
   715	                       encoding="utf-8", errors="replace", env=env)
   716	    last = [l for l in r.stdout.splitlines() if l.startswith("EFFECTIVE ")]
   717	    try:
   718	        return ast.literal_eval(last[-1][len("EFFECTIVE "):]) if last else None
   719	    except (ValueError, SyntaxError):
   720	        return None
   721	
   722	
   723	eff = effective(DEFAULT_CHECKER, "DOMAIN", LEDGER)
   724	effd = os.path.join(T, "eff_render")
   725	os.makedirs(effd, exist_ok=True)
   726	shutil.copy(RENDER, os.path.join(effd, "gen_dashboard.py"))
   727	shutil.copy(os.path.join(PIPE, "stage_tokens.py"), effd)
   728	effc = effective(os.path.join(effd, "gen_dashboard.py"), "D_CLASS", LEDGER, "--out", os.path.join(effd, "out.html"))
   729	four = ("✓", "✕", "⏸", "…")
   730	DCLS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
   731	say("C27 the glyph sets: one literal binding each, no named way to change it, each use counted, and BOTH files' EFFECTIVE "
   732	    "set -- read after running each as __main__ -- the four",
   733	    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and dcls == DCLS
   734	    and not dprobs and not cprobs and duses == collections.Counter({"in": 1, "join": 1})
   735	    and cuses == collections.Counter({"in": 1, "get": 1})
   736	    and isinstance(eff, tuple) and sorted(eff) == sorted(four) and effc == DCLS,
   737	    "DOMAIN %r %s uses %s | effective %r | D_CLASS %r %s uses %s | effective %r" % (
   738	        dom, dprobs or "", dict(duses), eff, sorted(dcls) if isinstance(dcls, dict) else dcls, cprobs or "", dict(cuses),
   739	        sorted(effc) if isinstance(effc, dict) else effc))
   740	rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
   741	say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
   742	#  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
   743	#  nothing pinned the sum -- GPT-6 Astra and GLM 5.3)
   744	k2 = next(k for k in base if k[6] >= 2)
   745	split = [k for k in base if k is not k2] + [k2[:6] + [1], k2[:6] + [k2[6] - 1]]
   746	rc, out = run_checker(LEDGER, wjson("b_split.json", split))
   747	say("C17b a key split across two baseline rows sums (%s %s %s %s %r x%d)" % (tuple(k2[:5]) + (k2[6],)), rc == 0, "rc %d" % rc)
   748	#  v5: each clause of the baseline row test at its own edge, one misshapen row appended to the shipped baseline -- `len(k) >=
   749	#  7', `isinstance(k[6], int)' (a bool is an int), `k[6] != 0', and the string test narrowed to five fields each passed all 72
   750	#  v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   751	kx = base[0]
   752	for tag, row_, how in (("c", kx[:6] + [1, "extra"], "eight fields"), ("d", kx[:6] + [True], "a count of true"),
   753	                       ("e", kx[:6] + [-1], "a count of -1"), ("f", kx[:6] + [0], "a count of 0"),
   754	                       ("g", kx[:6] + [1.0], "a count of 1.0"), ("h", [5] + kx[1:6] + [1], "a numeric first field"),
   755	                       ("i", kx[:5] + [5, 1], "a numeric note sha"),
   756	                       #  v6: the MIDDLE positions -- `for v in k[::5]' checked only the first and the sixth and passed all
   757	                       #  96 v5 controls (GPT-6 Astra, v5 pass)
   758	                       ("j", kx[:1] + [5] + kx[2:6] + [1], "a numeric phase"), ("k", kx[:2] + [5] + kx[3:6] + [1], "a numeric seat"),
   759	                       ("l", kx[:3] + [5] + kx[4:6] + [1], "a numeric date"), ("m", kx[:4] + [5] + kx[5:6] + [1], "a numeric d"),
   760	                       #  v6: a None field -- `isinstance(v, (str, type(None)))' passed all 96 v5 controls (Fable 5.1, v5 pass)
   761	                       ("n", kx[:3] + [None] + kx[4:6] + [1], "a None date")):
   762	    rc, out = run_checker(LEDGER, wjson("b_row_%s.json" % tag, base + [row_]))
   763	    tb = any("Traceback" in l for l in out)
   764	    say("C17%s a misshapen baseline row: %s (override)" % (tag, how), rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   765	txt = io.open(BASELINE, encoding="utf-8").read()
   766	lines = txt.split("\n")
   767	lines[1] = lines[1].replace('"y"', '"Y"', 1) if '"y"' in lines[1] else lines[1].replace(", 1]", ", 2]", 1)
   768	rc_mod, out_mod = run_checker(LEDGER, checker=pipe_copy("md5mod", "\n".join(lines)))
   769	rc_same, _ = run_checker(LEDGER, checker=pipe_copy("md5same", txt))
   770	say("C18 md5 pin: one baseline line changed -> 2, unchanged -> 0", rc_mod == 2 and rc_same == 0,
   771	    "changed rc %d, unchanged rc %d" % (rc_mod, rc_same))
   772	#  C18b: the same bytes checked out with CRLF -- what a fresh clone under core.autocrlf=true writes (measured 06a3ffc6 ->
   773	#  89d1d370 raw at the adjudication pass) -- must pass the pin, which folds line endings
   774	rc_crlf, _ = run_checker(LEDGER, checker=pipe_copy("md5crlf", txt.replace("\n", "\r\n")))
   775	say("C18b md5 pin: the baseline checked out with CRLF line endings -> 0", rc_crlf == 0, "rc %d" % rc_crlf)
   776	for lab, obj in (('C21a a misshapen ledger: {"rows": null}', {"rows": None}),
   777	                 ("C21b a misshapen ledger: a row that is not an object", {"rows": [42]}),
   778	                 ("C21c a misshapen ledger: a list, not an object", []),
   779	                 #  each of these walked as EMPTY and passed v3, rc 0 (GPT-6 Astra, v3 pass)
   780	                 ('C21d a misshapen ledger: {"rows": {}}', {"rows": {}}),
   781	                 ("C21e a misshapen ledger: an entry that is a string", {"rows": [{"id": "x", "entries": ["bogus"]}]}),
   782	                 ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]}),
   783	                 #  v5: `rows' ABSENT -- `ledger.get("rows", [])' would walk it as empty (Grok 4.7, GLM 5.3, v4 pass)
   784	                 ("C21i a misshapen ledger: no rows key -- {}", {}),
   785	                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []}),
   786	                 #  v7: a LIST row and a LIST entry -- `isinstance(r, (dict, list))' raised on the row and walked the entry
   787	                 #  as a non-entry, GREEN, each passing all 116 v6 controls (Fable 5.1, v6 pass, measured)
   788	                 ("C21l a misshapen ledger: a row that is a list", {"rows": [[1]]}),
   789	                 ("C21m a misshapen ledger: an entry that is a list", {"rows": [{"id": "x", "entries": [["bogus"]]}]})):
   790	    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
   791	    tb = any("Traceback" in l for l in out)
   792	    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   793	rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
   794	say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
   795	#  C29b (v7): a row with NO id -- the key's row field is str() of it, "None"; `r.get("id") or ""' keyed it "" and passed all
   796	#  116 v6 controls (Fable 5.1, v6 pass, measured)
   797	e29 = ans("2026-10-10", d="OK", seat="deepseek", note="no row id")
   798	l29 = copy.deepcopy(L0)
   799	l29["rows"].append({"title": "a row with no id", "entries": [e29]})
   800	rc, out = run_checker(wjson("l_noid.json", l29))
   801	off29 = [l.strip() for l in out if l.strip().startswith("OFF-DOMAIN ANSWER")]
   802	say("C29b an off-domain answer in a row with no id: refused, keyed and printed as row None",
   803	    rc == 1 and off29 == [offline("None", e29, WHY_CEIL)], "rc %d; %r" % (rc, off29[:1]))
   804	#  C21j (v6): a row with NO entries key is an empty row, not a misshapen one -- `r.get("entries")' at either site turns it
   805	#  into rc 2; the shipped ledger kills that today (98 of 912 rows carry no `entries'), so it is rowed in isolation (GLM 5.3,
   806	#  v5 pass)
   807	rc, out = run_checker(wjson("l_noentries.json", {"rows": [{"id": "ctlnoent"}, {"id": "ctlent", "entries": [ans("2026-10-18", d="✓")]}]}))
   808	say("C21j a row with no entries key beside a valid one", rc == 0, "rc %d" % rc)
   809	#  C21h: the shape check passes it, then is_answer raises on a NON-STRING note -- the one input that still reaches the walk's
   810	#  except-arm, so that arm stays a measured rc 2 rather than dead code
   811	rc, out = run_checker(wjson("l_shape_note.json", {"rows": [{"id": "x", "entries": [
   812	    {"phase": "review", "seat": "grok", "date": "2026-10-18", "d": "OK", "note": 5}]}]}))
   813	tb = any("Traceback" in l for l in out)
   814	say("C21h an entry whose note is a number (it raises inside is_answer)", rc == 2 and not tb,
   815	    "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   816	pj = os.path.join(T, "l_notjson.json")
   817	io.open(pj, "w", encoding="utf-8").write("{ this is not json")
   818	rc, out = run_checker(pj)
   819	tb = any("Traceback" in l for l in out)
   820	say("C23 an unreadable ledger (not JSON)", rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   821	
   822	# ------------------------------------------------------------------ the renderer
   823	SEATS = [s["id"] for s in L0["seats"]]
   824	EXPECT = {   # seat -> (entry fields, class, glyph)
   825	    "fable5": ({"d": "✓"}, "ok", "✓"),
   826	    "opus5": ({"d": "OK"}, "legacy", "OK"),
   827	    "codex": ({}, "pend", "…"),
   828	    "agy": ({"d": ""}, "legacy", "?"),
   829	    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
   830	    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", "∅"),
   831	    "glm": ({"d": "✕"}, "bad", "✕"),
   832	    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
   833	    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
   834	}
   835	assert set(EXPECT) == set(SEATS), SEATS
   836	#  the legacy cell's WHOLE tooltip: the class line, the date, the note -- joined and escaped exactly as cell() does.  A prefix
   837	#  check let "(not approval, not a seat failure)" return after the checked words (GPT-6 Astra and GLM 5.3, adjudication pass)
   838	LEGACY_TIP = html.escape("legacy -- verdict unclassified: d = 'OK' is outside ✓ ✕ ⏸ …; read the note for the outcome"
   839	                         " — 2026-10-16 — a renderer control", quote=True)
   840	LEGEND_LINE = ('<span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside '
   841	               '✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = '
   842	               'an explicit blank)</span>')
   843	REC_NOTE = st.NOTSEAT + " a record beside the answer"
   844	REF_A = {"phase": "research", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": st.RE_READ + " refused re-read control"}
   845	FX = copy.deepcopy(L0)
   846	ents = []
   847	for s in SEATS:
   848	    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
   849	    e.update(EXPECT[s][0])
   850	    ents.append(e)
   851	FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents},
   852	              {"id": "ctlesc", "title": "escape control row", "sev": "LOW", "state": "open", "commits": "",
   853	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "<b>&", "note": "escape control"}]},
   854	              #  a whitespace-only `d` must show `?`, never an invisible glyph (0 such values in the ledger; Fable 5.1,
   855	              #  adjudication pass, measured `{e(d) if d else "?"}` passing every v2 control)
   856	              {"id": "ctlws", "title": "whitespace control row", "sev": "LOW", "state": "open", "commits": "",
   857	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"},
   858	                           #  a TAB-only d: `.strip(" ")` would keep it invisible (Grok 4.7, v3 pass)
   859	                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"},
   860	                           #  v5: a newline and an NBSP -- `.strip(" \t")' kept both invisible and passed all 72 v4
   861	                           #  controls (Fable 5.1, Grok 4.7, v4 pass)
   862	                           {"phase": "assess", "seat": "opus5", "date": "2026-10-16", "d": "\n", "note": "newline control"},
   863	                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "\xa0", "note": "nbsp control"}]},
   864	              #  v5: an explicit null d renders legacy with the glyph None -- a renderer that treats null as missing (…) or
   865	              #  skips its class line passed all 72 v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   866	              {"id": "ctlnull", "title": "null control row", "sev": "LOW", "state": "open", "commits": "",
   867	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": None, "note": "null control"}]},
   868	              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
   869	              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
   870	              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
   871	               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
   872	                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
   873	              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
   874	              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
   875	              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
   876	              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
   877	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"},
   878	                           #  v6: the other end -- a renderer reading `str(d).rstrip()' would class it ok (GPT-6 Astra)
   879	                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "✓ ", "note": "padded trailing control"}]},
   880	              #  v6 (R1o): a legacy answer carrying a grade, a badge and evidence -- with only a date and a note, `tip.insert(-2,
   881	              #  ...)' and `if cls == LEGACY and not ent.get("ev")' each passed all 96 v5 controls, while the first MOVED the
   882	              #  class line off the front of 649 of the 670 shipped legacy cells and the second REMOVED it from 642 (GPT-6
   883	              #  Astra, v5 pass; "lost" corrected to moved/removed on the v6 pass)
   884	              #  v6 (R1q): a legacy answer with NO date and NO note -- its tooltip is the class line alone; `if cls == LEGACY
   885	              #  and tip:' would leave it empty (Fable 5.1, v5 pass: equivalent on the ledger, every off-domain answer has a note)
   886	              {"id": "ctlbare", "title": "bare legacy control row", "sev": "LOW", "state": "open", "commits": "",
   887	               "entries": [{"phase": "assess", "seat": "fable5", "d": "BARE"}]},
   888	              {"id": "ctlopt", "title": "optional fields control row", "sev": "LOW", "state": "open", "commits": "",
   889	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL", "b": "A",
   890	                            "ev": "regress/artifacts/x/ctl.txt", "note": "optional fields control"}]},
   891	              #  v7 (R1o2): ONE optional field each on a legacy answer -- `and (not ent.get("ev") or ent.get("grade"))' and
   892	              #  its twin, and `and badge != "s"', each passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass)
   893	              {"id": "ctlopt1", "title": "single optional field control row", "sev": "LOW", "state": "open", "commits": "",
   894	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "OK", "grade": "MANUAL",
   895	                            "note": "single grade control"},
   896	                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "OK",
   897	                            "ev": "regress/artifacts/x/ev1.txt", "note": "single ev control"},
   898	                           {"phase": "assess", "seat": "glm", "date": "2026-10-16", "d": "OK", "b": "s",
   899	                            "note": "single badge control"}]},
   900	              #  v7 (R1p2): NON-legacy answers carrying a grade, a badge and evidence get NO class line -- `if cls == LEGACY
   901	              #  or badge' and `... or ent.get("ev")' passed all 116 v6 controls (Fable 5.1, v6 pass, measured; the fourth
   902	              #  cell of {legacy, non-legacy} x {optional fields absent, present})
   903	              {"id": "ctlnlopt", "title": "non-legacy optional fields control row", "sev": "LOW", "state": "open",
   904	               "commits": "",
   905	               "entries": [{"phase": "assess", "seat": s_, "date": "2026-10-16", "d": g_, "grade": "MANUAL", "b": "A",
   906	                            "ev": "regress/artifacts/x/ev2.txt", "note": "nonlegacy optional control"}
   907	                           for s_, g_ in (("fable5", "✓"), ("codex", "✕"), ("glm", "⏸"))]},
   908	              #  v7 (R1g): a NUMBER and a BOOL d render legacy with their whole tooltip (GLM 5.3, v6 pass: the member was
   909	              #  unrowed); v7 (R2b): the counter keys `total' and `legacy' spelled as d count legacy -- `n[d if d in n else
   910	              #  LEGACY]' counted them as themselves and passed all 116 v6 controls (GPT-6 Astra, Grok 4.7, v6 pass)
   911	              {"id": "ctlscalar", "title": "scalar and counter-key control row", "sev": "LOW", "state": "open",
   912	               "commits": "",
   913	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": 5, "note": "scalar control int"},
   914	                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": True, "note": "scalar control bool"},
   915	                           {"phase": "assess", "seat": "glm", "date": "2026-10-16", "d": "total", "note": "counter key total"},
   916	                           {"phase": "assess", "seat": "deepseek", "date": "2026-10-16", "d": "legacy",
   917	                            "note": "counter key legacy"}]},
   918	              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
   919	               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
   920	#  v6 (R1w): EVERY whitespace code point alone as d, nine per row (one cell per seat) -- R1d's four were a SAMPLE of the set
   921	#  `str.strip()' removes, and `.strip(" \t\n\xa0")' passed all 96 v5 controls but R3's presence pin (Fable 5.1, v5 pass)
   922	WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
   923	for i in range(0, len(WS), len(SEATS)):
   924	    FX["rows"].append({"id": "ctlws%02d" % (i // len(SEATS)), "title": "whitespace set control row", "sev": "LOW", "state": "open",
   925	                       "commits": "", "entries": [{"phase": "assess", "seat": SEATS[j], "date": "2026-10-16", "d": ch,
   926	                                                   "note": "ws control U+%04X" % ord(ch)}
   927	                                                  for j, ch in enumerate(WS[i:i + len(SEATS)])]})
   928	fx_path = wjson("fx_render.json", FX)
   929	
   930	
   931	def render(gen, ledger_path, tag):
   932	    d = os.path.join(T, "r_" + tag)
   933	    os.makedirs(d, exist_ok=True)
   934	    shutil.copy(gen, os.path.join(d, "gen_dashboard.py"))
   935	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   936	    out = os.path.join(d, "out.html")
   937	    env = dict(os.environ, GXLEDGER=ledger_path, PYTHONIOENCODING="utf-8")
   938	    r = subprocess.run([sys.executable, os.path.join(d, "gen_dashboard.py"), "--out", out], capture_output=True, text=True,
   939	                       encoding="utf-8", env=env)
   940	    return io.open(out, encoding="utf-8").read() if r.returncode == 0 and os.path.exists(out) else None
   941	
   942	
   943	CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
   944	             "padded glyph control", "tab control", "newline control", "nbsp control", "null control", "padded trailing control",
   945	             "optional fields control", "BARE", "ws control U+", "single grade control", "single ev control",
   946	             "single badge control", "nonlegacy optional control", "scalar control", "counter key")
   947	
   948	
   949	def cells(html_text):
   950	    got = []
   951	    for m in re.finditer(r'<td class="c ([a-z]+)">(.*?)</td>', html_text, re.S):
   952	        if m.group(1) == "none":
   953	            continue
   954	        g = re.search(r'<span class="g">(.*?)</span>', m.group(2))
   955	        tip = re.search(r'<span class="tip">(.*?)</span>', m.group(2), re.S)
   956	        got.append((m.group(1), g.group(1) if g else None, tip.group(1) if tip else ""))
   957	    return got
   958	
   959	
   960	def r1(html_text):
   961	    if html_text is None:
   962	        return False, "render FAILED (a crash is not a kill)"
   963	    got = [c for c in cells(html_text) if not any(k in c[2] for k in CTL_OTHER)]   # the control row's nine, in seat order
   964	    want = [(EXPECT[s][1], EXPECT[s][2]) for s in SEATS]
   965	    head = got[:len(want)]
   966	    bad = [(s, g[:2], w) for s, g, w in zip(SEATS, head, want) if (g[0], g[1]) != w]
   967	    legacy_tip = head[SEATS.index("opus5")][2] if len(head) == len(want) else ""
   968	    tip_ok = legacy_tip == LEGACY_TIP
   969	    return (len(head) == len(want) and not bad and tip_ok), ("%d cells; mismatches %s; legacy tip %s" % (
   970	        len(head), bad[:3], "exact" if tip_ok else "WRONG: %r" % legacy_tip[:120]))
   971	
   972	
   973	def r1b(html_text):
   974	    if html_text is None:
   975	        return False, "render FAILED (a crash is not a kill)"
   976	    got = [c for c in cells(html_text) if "escape control" in c[2]]
   977	    esc = got[0] if got else ("", "", "")
   978	    return (esc[0] == "legacy" and esc[1] == "&lt;b&gt;&amp;"), "escape cell %r" % (esc[:2],)
   979	
   980	
   981	def r1d(html_text):
   982	    if html_text is None:
   983	        return False, "render FAILED (a crash is not a kill)"
   984	    got = [c for c in cells(html_text) if any(k in c[2] for k in ("whitespace control", "tab control", "newline control",
   985	                                                                    "nbsp control"))]
   986	    return (len(got) == 4 and all(c[0] == "legacy" and c[1] == "?" for c in got)), "whitespace cells %r" % ([c[:2] for c in got],)
   987	
   988	
   989	def legacy_line(d):
   990	    return "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d
   991	
   992	
   993	def r1g(html_text):
   994	    #  EVERY legacy cell, not only the "OK" one: `if cls == LEGACY` -> `if d == "OK"` passed every v3 control and drops the
   995	    #  explanation from 305 displayed cells (GPT-6 Astra, v3 pass)
   996	    if html_text is None:
   997	        return False, "render FAILED (a crash is not a kill)"
   998	    #  the WHOLE tooltip of each simple legacy cell -- class line, date, note -- not a prefix and not one cell: `if cls ==
   999	    #  LEGACY and d == "OK"` and `... and str(d).strip()` passed all 46 v3 controls (Fable 5.1, v3 pass, measured)
  1000	    want = [(note, d, html.escape(" — ".join([legacy_line(d), "2026-10-16", note]), quote=True))
  1001	            for note, d in (("a renderer control", "OK"), ("a renderer control", ""), ("a renderer control", "N/A"),
  1002	                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"), ("padded trailing control", "✓ "),
  1003	                            ("tab control", "\t"), ("null control", None),
  1004	                            #  v6: the newline and NBSP cells -- R1d checked their class and glyph only, so `if cls == LEGACY
  1005	                            #  and d not in ("\n", "\xa0")' passed all 96 v5 controls (Grok 4.7, v5 pass)
  1006	                            ("newline control", "\n"), ("nbsp control", "\xa0"),
  1007	                            #  v7: a number, a bool, and the counter keys as spellings
  1008	                            ("scalar control int", 5), ("scalar control bool", True), ("counter key total", "total"),
  1009	                            ("counter key legacy", "legacy"))]
  1010	    legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
  1011	    missing = [(note, d) for note, d, whole in want if whole not in legacy]
  1012	    return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])
  1013	
  1014	
  1015	def r1e(html_text):
  1016	    if html_text is None:
  1017	        return False, "render FAILED (a crash is not a kill)"
  1018	    got = [c for c in cells(html_text) if "record control answer" in c[2]]
  1019	    #  v5: the WHOLE tooltip -- class line, date, note, the record line.  v4 asserted the record substring, so a class line
  1020	    #  dropped from every cell with a record beside it passed all 72 v4 controls (Fable 5.1, GPT-6 Astra, v4 pass)
  1021	    want = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "record control answer", "record: 2026-10-16 — " + REC_NOTE]),
  1022	                       quote=True)
  1023	    return (len(got) == 1 and got[0][0] == "legacy" and got[0][2] == want), "cells %d; tooltip %s" % (
  1024	        len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:140] if got else ""))
  1025	
  1026	
  1027	def r1f(html_text):
  1028	    if html_text is None:
  1029	        return False, "render FAILED (a crash is not a kill)"
  1030	    stage = [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]
  1031	    probs = st.stage_token_problems(stage)
  1032	    want = html.escape(" — ".join(["EXEMPTION REFUSED BY SECTION H: " + "; ".join(probs), legacy_line("OK"), "2026-10-16",
  1033	                                   REF_A["note"]]), quote=True)
  1034	    got = [c for c in cells(html_text) if "refused re-read control" in c[2]]
  1035	    return (bool(probs) and len(got) == 1 and got[0][2] == want), "refusals %d; cells %d; tooltip %s" % (
  1036	        len(probs), len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:120] if got else ""))
  1037	
  1038	
  1039	ha_fx = render(RENDER, fx_path, "after")
  1040	ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
  1041	ok, det = r1g(ha_fx); say("R1g every simple legacy cell's WHOLE tooltip, the class line for ITS d", ok, det)
  1042	#  v6: both ends, and the glyph TEXT -- `html.escape(str(t).strip())' showed " ✓" as "✓" and passed all 96 v5 controls,
  1043	#  which read only the class (GPT-6 Astra, v5 pass)
  1044	pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
  1045	padt = [c for c in cells(ha_fx or "") if "padded trailing control" in c[2]]
  1046	say("R1h a ✓ padded at either end renders legacy, its glyph text exactly as written",
  1047	    len(pad) == 1 and pad[0][:2] == ("legacy", " ✓") and len(padt) == 1 and padt[0][:2] == ("legacy", "✓ "),
  1048	    "cells %r %r" % (pad[0][:2] if pad else None, padt[0][:2] if padt else None))
  1049	opt = [c for c in cells(ha_fx or "") if "optional fields control" in c[2]]
  1050	want_o = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "MANUAL", "the author did this review (shown, not hidden)",
  1051	                                  "optional fields control", "evidence: regress/artifacts/x/ctl.txt"]), quote=True)
  1052	say("R1o a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first",
  1053	    len(opt) == 1 and opt[0][0] == "legacy" and opt[0][2] == want_o,
  1054	    "cell %r; tooltip %s" % (opt[0][:2] if opt else None, "exact" if opt and opt[0][2] == want_o else "WRONG: %r" % (opt[0][2][:140] if opt else "")))
  1055	BT = {"A": "the author did this review (shown, not hidden)", "s": "a review by the same model family"}
  1056	o1 = {c[2] for c in cells(ha_fx or "") if c[0] == "legacy" and "single " in c[2] and " control" in c[2]}
  1057	want_o1 = {html.escape(" — ".join(p), quote=True) for p in (
  1058	    [legacy_line("OK"), "2026-10-16", "MANUAL", "single grade control"],
  1059	    [legacy_line("OK"), "2026-10-16", "single ev control", "evidence: regress/artifacts/x/ev1.txt"],
  1060	    [legacy_line("OK"), "2026-10-16", BT["s"], "single badge control"])}
  1061	say("R1o2 legacy answers carrying a grade, evidence or the badge s ALONE: each WHOLE tooltip, the class line first",
  1062	    o1 == want_o1, "got %r" % sorted(x[:70] for x in o1 - want_o1))
  1063	p2 = [c for c in cells(ha_fx or "") if "nonlegacy optional control" in c[2]]
  1064	want_p2 = html.escape(" — ".join(["2026-10-16", "MANUAL", BT["A"], "nonlegacy optional control",
  1065	                                   "evidence: regress/artifacts/x/ev2.txt"]), quote=True)
  1066	say("R1p2 ok, bad and hold answers carrying a grade, a badge and evidence: each WHOLE tooltip, NO class line",
  1067	    sorted(c[0] for c in p2) == ["bad", "hold", "ok"] and all(c[2] == want_p2 for c in p2),
  1068	    "%d cells %r; tips %r" % (len(p2), [c[0] for c in p2], [c[2][:60] for c in p2 if c[2] != want_p2][:2]))
  1069	#  R1p (v6): the class line ONLY on a legacy cell -- `if cls in (LEGACY, "pend")' and `if cls != "ok"' each passed all 96 v5
  1070	#  controls, putting the FALSE line "d = '…' is outside ✓ ✕ ⏸ …" on every pend cell, 833 on HEAD's ledger (Fable 5.1, v5 pass)
  1071	plain = html.escape("2026-10-16 — a renderer control", quote=True)
  1072	ctl = [c for c in cells(ha_fx or "") if not any(k in c[2] for k in CTL_OTHER)][:len(SEATS)]
  1073	tips = dict(zip(SEATS, [c[2] for c in ctl])) if len(ctl) == len(SEATS) else {}
  1074	bad_p = [s for s in ("fable5", "codex", "glm", "deepseek") if tips.get(s) != plain]
  1075	say("R1p the NON-legacy answer cells -- ok, pend, bad, hold -- carry no class line: the date and the note alone",
  1076	    bool(tips) and not bad_p, "wrong: %r" % ([(s, (tips.get(s) or "")[:70]) for s in bad_p],))
  1077	bare = [c for c in cells(ha_fx or "") if "BARE" in c[2]]
  1078	want_b = html.escape(legacy_line("BARE"), quote=True)
  1079	say("R1q a legacy answer with neither date nor note: its tooltip is the class line alone",
  1080	    len(bare) == 1 and bare[0][0] == "legacy" and bare[0][2] == want_b, "cells %d: %r" % (len(bare), [c[2][:80] for c in bare]))
  1081	wsc = [c for c in cells(ha_fx or "") if "ws control U+" in c[2]]
  1082	wsw = {html.escape(" — ".join([legacy_line(ch), "2026-10-16", "ws control U+%04X" % ord(ch)]), quote=True) for ch in WS}
  1083	wsbad = [c[2][-14:] for c in wsc if c[0] != "legacy" or c[1] != "?" or c[2] not in wsw]
  1084	say("R1w every str.isspace() code point alone as d (%d) shows ? and renders legacy, each with its WHOLE tooltip" % len(WS),
  1085	    len(wsc) == len(WS) == 29 and not wsbad and len({c[2] for c in wsc}) == 29,
  1086	    "%d cells of %d; wrong: %r" % (len(wsc), len(WS), wsbad[:5]))
  1087	ok, det = r1e(ha_fx); say("R1e an answer with a record beside it: its WHOLE tooltip", ok, det)
  1088	nul = [c for c in cells(ha_fx or "") if "null control" in c[2]]
  1089	say("R1n an explicit null d renders legacy with the glyph None", len(nul) == 1 and nul[0][:2] == ("legacy", "None"),
  1090	    "cell %r" % (nul[0][:2],) if nul else "render FAILED or no cell")
  1091	ok, det = r1f(ha_fx); say("R1f a refused exemption's line first, then the class line, exactly", ok, det)
  1092	ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
  1093	ok, det = r1d(ha_fx); say("R1d a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?", ok, det)
  1094	low = (ha_fx or "").lower()
  1095	hits = [p for p in ("not approval", "not a seat failure") if p in low]
  1096	say("R1c the fixture page says neither 'not approval' nor 'not a seat failure'", ha_fx is not None and not hits,
  1097	    "render %s; found %s" % ("ok" if ha_fx is not None else "FAILED", hits or "none"))
  1098	leg = re.search(r'<div class="legend">(.*?)</div>', ha_fx or "", re.S)
  1099	say("R4 the legend carries the legacy line EXACTLY", bool(leg) and LEGEND_LINE in leg.group(1),
  1100	    "legend %s" % ("found" if leg else "MISSING"))
  1101	#  R5 (v5): the two CSS rules the class adds -- `font-size:0' made every legacy glyph invisible and passed all 72 v4 controls
  1102	#  (GPT-6 Astra, Fable 5.1, v4 pass)
  1103	CSS = ("td.c.legacy { outline:1px dashed var(--line); outline-offset:-3px; }",
  1104	       ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
  1105	#  v6: and they are the ONLY rules in the style block naming `legacy' -- a later `.c.legacy .g { font-size:0; }' left both
  1106	#  present and hid every legacy glyph (GPT-6 Astra, v5 pass)
  1107	#  v7: EVERY style block, CSS escapes decoded -- a second <style> block and `.c.lega\\63 y' each hid the glyph past the v6
  1108	#  form, which read the first block's literal `legacy' (GPT-6 Astra, Grok 4.7, v6 pass)
  1109	def css_unescape(s):
  1110	    return re.sub(r"\\([0-9a-fA-F]{1,6})\s?", lambda m: chr(int(m.group(1), 16)), s)
  1111	
  1112	
  1113	blocks = re.findall(r"<style[^>]*>(.*?)</style>", ha_fx or "", re.S)
  1114	leg_rules = [" ".join(m.group(0).split()) for b_ in blocks
  1115	             for m in re.finditer(r"[^{}]*legacy[^{}]*\{[^{}]*\}", css_unescape(b_))]
  1116	say("R5 the page carries the legacy class's two CSS rules EXACTLY, and no other rule names it",
  1117	    ha_fx is not None and all(c in ha_fx for c in CSS) and sorted(leg_rules) == sorted(CSS),
  1118	    "missing %r; legacy rules %d %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")], len(leg_rules), [r[:40] for r in leg_rules]))
  1119	
  1120	
  1121	def census(html_text):
  1122	    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html_text))
  1123	    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html_text).group(1)
  1124	    return c, s
  1125	
  1126	
  1127	hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
  1128	#  v6: guarded -- a renderer that crashes on the shipped ledger made census() raise, so the controls died with no tally and no
  1129	#  sentinel and the mutant driver scored a KILL as INCOMPLETE (Fable 5.1, v5 pass); now R2 says NO and the run completes
  1130	cb, sb = census(hb) if hb else (collections.Counter(), "")
  1131	ca, sa = census(ha) if ha else (collections.Counter(), "")
  1132	same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
  1133	moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
  1134	nums = [int(x) for x in re.findall(r"(\d+)", sa)]
  1135	n_entries = sum(len(r.get("entries", [])) for r in L0["rows"])
  1136	n_legacy = sum(1 for r in L0["rows"] for x in r.get("entries", []) if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…"))
  1137	#  the strip's FIFTH number is checked against the ledger itself: a renderer that folded legacy into … still summed (the
  1138	#  kill table measured R2 blind to that on its first run)
  1139	cnt = collections.Counter()
  1140	for r_ in L0["rows"]:
  1141	    for x in r_.get("entries", []):
  1142	        d_ = x.get("d", "…")
  1143	        cnt[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
  1144	#  EACH number against the ledger's own count: the v3 form checked only the total and the legacy number, so folding every
  1145	#  canonical glyph into ✓ passed (GPT-6 Astra, v3 pass)
  1146	sums = nums == [cnt["✓"], cnt["✕"], cnt["⏸"], cnt["…"], cnt["legacy"], n_entries] and nums[4] == n_legacy
  1147	#  v5: the WHOLE strip string -- its labels too: "1397 approved" passed all 72 v4 controls (GPT-6 Astra, v4 pass)
  1148	def strip_text(c, total):
  1149	    return "%d✓ %d✕ %d⏸ %d… %d legacy · %d in all" % (c["✓"], c["✕"], c["⏸"], c["…"], c["legacy"], total)
  1150	
  1151	
  1152	label_ok = sa == strip_text(cnt, n_entries)
  1153	say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label)",
  1154	    same and moved and sums and label_ok,
  1155	    "before %s | after %s | strip '%s' | ledger %d entries, %d off-domain" % (dict(sorted(cb.items())), dict(sorted(ca.items())),
  1156	                                                                          sa, n_entries, n_legacy))
  1157	#  R2b (v5): the FIXTURE page's strip against the fixture's own counts, by exact membership -- its padded " ✓" and its null
  1158	#  count legacy.  R2 recomputes on the shipped ledger, which holds no padded glyph, so counting " ✓" as ✓ passed all 72 v4
  1159	#  controls (Fable 5.1, Grok 4.7, v4 pass)
  1160	cfx = collections.Counter()
  1161	for r_ in FX["rows"]:
  1162	    for x in r_.get("entries", []):
  1163	        d_ = x.get("d", "…")
  1164	        cfx[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
  1165	_, sfx = census(ha_fx) if ha_fx else (None, "")
  1166	want_fx = strip_text(cfx, sum(len(r_.get("entries", [])) for r_ in FX["rows"]))
  1167	say("R2b the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy)", sfx == want_fx,
  1168	    "strip %r, want %r" % (sfx, want_fx))
  1169	src_r = io.open(RENDER, encoding="utf-8").read()
  1170	for tag, find, repl, check in (
  1171	        ("ok", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")', r1),
  1172	        ("pend", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")', r1),
  1173	        ("noescape", '{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}', r1b)):
  1174	    if src_r.count(find) != 1:
  1175	        say("R3 MUTANT %s: find-text present" % tag, False, "MUTANT TEXT NOT FOUND"); continue
  1176	    m = os.path.join(T, "gen_mut_%s.py" % tag)
  1177	    io.open(m, "w", encoding="utf-8").write(src_r.replace(find, repl))
  1178	    h = render(m, fx_path, "mut_" + tag)
  1179	    ok, det = check(h)
  1180	    say("R3 MUTANT %s renders and fails its check" % tag, h is not None and not ok, det)
  1181	
  1182	# ------------------------------------------------------------------ the wiring: precommit section Q2, failures counted
  1183	BASH = os.environ.get("BASH_EXE") or r"C:\Program Files\Git\bin\bash.exe"
  1184	txt_pre = io.open(PRE, encoding="utf-8").read()
  1185	a, b = txt_pre.find('say ""; say "Q2.'), txt_pre.find("#  ---- R ----")
  1186	if a < 0 or b < a or not os.path.exists(BASH):
  1187	    say("W0 precommit Q2 block extracted and a git-bash found", False, "a=%d b=%d bash=%s" % (a, b, BASH))
  1188	else:
  1189	    blk = os.path.join(T, "q2_block.sh")
  1190	    io.open(blk, "w", encoding="utf-8", newline="\n").write(
  1191	        'say () { :; }\nfails=0\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n'
  1192	        '_HERE="$1"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\n')
  1193	    def w_tools(tag, ledger_path, baseline_text=None, nochecker=False, stub=None):
  1194	        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
  1195	        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
  1196	        d = os.path.join(T, "w_" + tag)
  1197	        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
  1198	        if stub is not None:
  1199	            io.open(os.path.join(d, "pipeline", "check_entry_domain.py"), "w", encoding="utf-8").write(stub)
  1200	        elif not nochecker:
  1201	            shutil.copy(CHECKER, os.path.join(d, "pipeline", "check_entry_domain.py"))
  1202	        shutil.copy(os.path.join(PIPE, "stage_tokens.py"), os.path.join(d, "pipeline"))
  1203	        shutil.copy(ledger_path, os.path.join(d, "pipeline", "ledger.json"))
  1204	        if baseline_text is None:
  1205	            shutil.copy(BASELINE, os.path.join(d, "pipeline", "entry_domain_baseline.json"))
  1206	        elif baseline_text != "<absent>":
  1207	            io.open(os.path.join(d, "pipeline", "entry_domain_baseline.json"), "w", encoding="utf-8").write(baseline_text)
  1208	        return d
  1209	    #  dated BEFORE the cutoff, so only the BASELINE decides W4: a post-cutoff entry is refused by the date rule whichever
  1210	    #  baseline is read, and the kill table measured W4 blind to the un-stripped override on its first run for that reason
  1211	    new_led = with_entries([(ROW0, ans("2026-10-10", d="OK", seat="deepseek", note="W new off-domain"))])
  1212	    permissive = wjson("b_permissive.json", base + [ident(ROW0, ans("2026-10-10", d="OK", seat="deepseek",
  1213	                                                                      note="W new off-domain")) + [1]])
  1214	    #  the FIRST LINE names which branch fired: W2 the rc-1 refusal, W3 the rc-2 apparatus line -- `-eq 1` -> `-eq 7` and a
  1215	    #  rewritten message each passed every v2 control, which tested only the BAD prefix and the counter (Fable 5.1,
  1216	    #  adjudication pass)
  1217	    for lab, tools, envx, want, wantf, msg in (
  1218	            ("W1 Q2 on the shipped ledger", w_tools("1", LEDGER), {}, "GOOD", 0, "within the frozen ceiling"),
  1219	            ("W2 Q2 with a new off-domain answer", w_tools("2", new_led), {}, "BAD", 1, "beyond the frozen legacy ceiling"),
  1220	            ("W3 Q2 with the baseline absent (rc 2 path)", w_tools("3", LEDGER, "<absent>"), {}, "BAD", 1,
  1221	             "could not run (rc 2)"),
  1222	            ("W4 Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry", w_tools("4", new_led),
  1223	             {"GXDOMAIN_BASELINE": permissive}, "BAD", 1, "beyond the frozen legacy ceiling"),
  1224	            #  the bad ledger is the block's DEFAULT; the exported GXLEDGER names the clean shipped one, so only the strip
  1225	            #  decides W5 (deleting `-u GXLEDGER` passed all 35 v2 controls -- GPT-6 Astra, adjudication pass)
  1226	            ("W5 Q2 ignores an exported GXLEDGER naming a clean ledger", w_tools("5", new_led), {"GXLEDGER": LEDGER},
  1227	             "BAD", 1, "beyond the frozen legacy ceiling"),
  1228	            #  the checker ABSENT: the missing-file branch was exercised by no v3 row, so `bad` -> `good` there passed
  1229	            #  (GPT-6 Astra, v3 pass)
  1230	            ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING"),
  1231	            #  v5: ANY status other than 0 and 1 is "could not run" -- `else' narrowed to `elif [ $_cedrc -eq 2 ]' passed all 72
  1232	            #  v4 controls, leaving rc 7 or 127 silently green (GPT-6 Astra, Fable 5.1, v4 pass).  W7's message is on STDERR,
  1233	            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given -- and
  1234	            #  the git-bash wrapper PREPENDS /mingw64/bin, /usr/bin and ~/bin to that PATH; none holds a python on this
  1235	            #  machine, and if one did W8 would fail LOUDLY (GOOD instead of BAD), never pass falsely (Fable 5.1, v5 pass)
  1236	            ("W7 Q2 with a checker that exits 7, its message on stderr",
  1237	             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB FIRST LINE\\nSTUB SECOND LINE\\n")\nsys.exit(7)\n'), {},
  1238	             "BAD", 1, "could not run (rc 7): STUB FIRST LINE"),
  1239	            ("W8 Q2 with python absent from PATH (rc 127)", w_tools("8", LEDGER),
  1240	             {"PATH": os.path.join(os.path.dirname(os.path.dirname(BASH)), "usr", "bin")}, "BAD", 1, "could not run (rc 127)")):
  1241	        env = dict(os.environ)
  1242	        for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
  1243	            env.pop(k, None)
  1244	        env.update(envx)
  1245	        r = subprocess.run([BASH, blk.replace("\\", "/"), tools.replace("\\", "/")], capture_output=True, env=env)
  1246	        outl = r.stdout.decode("cp1252", "replace").strip().splitlines()
  1247	        firstl = outl[0] if outl else ""
  1248	        fl = [l for l in outl if l.startswith("FAILURES ")]
  1249	        nf = int(fl[-1].split()[1]) if fl else -1
  1250	        #  W2's refusal must also NAME the entry to the committer: deleting Q2's `printf | sed` passed every v3 control, which
  1251	        #  read only the first line and the counter (Grok 4.7, v3 pass)
  1252	        named = (not lab.startswith("W2 ")) or any(l.strip().startswith("OFF-DOMAIN ANSWER  row") for l in outl)
  1253	        #  v6: W1 and W7 read the WHOLE output -- the apparatus branch's `head -1' -> `tail -1' passed all 96 v5 controls on
  1254	        #  one-line messages (GPT-6 Astra, v5 pass)
  1255	        whole = {"W1": ["GOOD " + summary_line(N_OFF, N_OFF, N_OFF), "FAILURES 0"],
  1256	                 "W7": ["BAD check_entry_domain.py could not run (rc 7): STUB FIRST LINE", "FAILURES 1"]}.get(lab.split()[0])
  1257	        #  v6: W2's WHOLE output -- its first line, then EVERY line of the checker's own output, indented, then the counter:
  1258	        #  Q2's `printf | sed' replaced by a constant "OFF-DOMAIN ANSWER  row ..." line passed all 96 v5 controls, which read a
  1259	        #  prefix (Grok 4.7, v5 pass).  The checker's lines come from running the checker in W2's own tools dir as Q2 does.
  1260	        if lab.split()[0] == "W2":
  1261	            e2 = subprocess.run([sys.executable, os.path.join(tools, "pipeline", "check_entry_domain.py")],
  1262	                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
  1263	            whole = (["BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one "
  1264	                      "edited):"] + ["          " + l for l in e2.stdout.decode("cp1252", "replace").splitlines()] + ["FAILURES 1"])
  1265	        named = named and (whole is None or outl == whole)
  1266	        #  v6: W2's first line EXACT -- its parenthetical dropped passed all 96 v5 controls (Fable 5.1, v5 pass)
  1267	        named = named and (lab.split()[0] != "W2" or firstl == "BAD an off-domain ledger answer is beyond the frozen legacy ceiling "
  1268	                                                           "(a new one, a copy, or an old one edited):")
  1269	        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
  1270	        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))
  1271	    #  W9 (v6): EVERY status but 0 and 1 is "could not run".  The else partition is {2..255}, EXHAUSTED in ONE bash loop over
  1272	    #  a stub that exits $W9RC: `else' -> `elif [ $_cedrc -ne 3 ]' passed all 96 v5 controls, whose W3, W7 and W8 are three
  1273	    #  statuses of 254 (Grok 4.7, v5 pass)
  1274	    w9 = w_tools("9", LEDGER, stub='import os, sys\nsys.stderr.write("STUB rc %s\\n" % os.environ["W9RC"])\n'
  1275	                                   'sys.exit(int(os.environ["W9RC"]))\n')
  1276	    loop = os.path.join(T, "q2_loop.sh")
  1277	    io.open(loop, "w", encoding="utf-8", newline="\n").write(
  1278	        'say () { :; }\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n_HERE="$1"\n'
  1279	        'for W9RC in $(seq 2 255); do export W9RC; fails=0; echo "RC $W9RC"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\ndone\n')
  1280	    env = dict(os.environ)
  1281	    for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
  1282	        env.pop(k, None)
  1283	    r = subprocess.run([BASH, loop.replace("\\", "/"), w9.replace("\\", "/")], capture_output=True, env=env)
  1284	    got9 = r.stdout.decode("cp1252", "replace").splitlines()
  1285	    want9 = []
  1286	    for n_ in range(2, 256):
  1287	        want9 += ["RC %d" % n_, "BAD check_entry_domain.py could not run (rc %d): STUB rc %d" % (n_, n_), "FAILURES 1"]
  1288	    bad9 = ([n_ for n_ in range(2, 256) if got9[3 * (n_ - 2):3 * (n_ - 1)] != want9[3 * (n_ - 2):3 * (n_ - 1)]]
  1289	            if len(got9) == len(want9) else ["%d lines of %d" % (len(got9), len(want9))])
  1290	    say("W9 Q2 with EVERY status 2-255 (254 runs of one stub): each exactly BAD 'could not run (rc N)' with its first line, "
  1291	        "the counter 1", got9 == want9, "wrong at: %r" % (bad9[:8],))
  1292	
  1293	shutil.rmtree(T, ignore_errors=True)
  1294	print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
  1295	print("DASHOKCLASS_CONTROLS_DONE")
  1296	sys.exit(0 if all(res) else 1)
```

### 4c. `RECEIPT_v7_on_staged_v5.txt`, whole

```
# controls md5 836927f03474c85de42bd5f247cdfcc5
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
C12w the ISO shape's year3: a FROZEN identity dated 999-10-17 is not read as a date ok  rc 0 (want 0)
C12w the ISO shape's month3: a FROZEN identity dated 2026-100-17 is not read as a date ok  rc 0 (want 0)
C13  an unreadable baseline                                                       ok  rc 2
C27  the glyph sets: one literal binding each, no named way to change it, each use counted, and BOTH files' EFFECTIVE set -- read after running each as __main__ -- the four ok  DOMAIN ('✓', '✕', '⏸', '…')  uses {'in': 1, 'join': 1} | effective ('✓', '✕', '⏸', '…') | D_CLASS ['…', '⏸', '✓', '✕']  uses {'get': 1, 'in': 1} | effective ['…', '⏸', '✓', '✕']
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
C21l a misshapen ledger: a row that is a list                                     ok  rc 2
C21m a misshapen ledger: an entry that is a list                                  ok  rc 2
C21g a misshapen baseline: an object, not a list (override)                       ok  rc 2
C29b an off-domain answer in a row with no id: refused, keyed and printed as row None ok  rc 1; ["OFF-DOMAIN ANSWER  row None  phase review  seat deepseek  date 2026-10-10  d 'OK'  note f22fae7211f9c8be -- beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"]
C21j a row with no entries key beside a valid one                                 ok  rc 0
C21h an entry whose note is a number (it raises inside is_answer)                 ok  rc 2
C23  an unreadable ledger (not JSON)                                              ok  rc 2
R1   fixture row: class, glyph and the legacy tooltip EXACTLY, per seat           ok  9 cells; mismatches []; legacy tip exact
R1g  every simple legacy cell's WHOLE tooltip, the class line for ITS d           ok  51 legacy cells; no exact tooltip for: []
R1h  a ✓ padded at either end renders legacy, its glyph text exactly as written   ok  cells ('legacy', ' ✓') ('legacy', '✓ ')
R1o  a legacy answer with a grade, a badge and evidence: its WHOLE tooltip, the class line first ok  cell ('legacy', 'OK'); tooltip exact
R1o2 legacy answers carrying a grade, evidence or the badge s ALONE: each WHOLE tooltip, the class line first ok  got []
R1p2 ok, bad and hold answers carrying a grade, a badge and evidence: each WHOLE tooltip, NO class line ok  3 cells ['ok', 'bad', 'hold']; tips []
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
R2b  the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy) ok  strip '3✓ 2✕ 2⏸ 2… 53 legacy · 62 in all', want '3✓ 2✕ 2⏸ 2… 53 legacy · 62 in all'
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
DASHOKCLASS CONTROLS: 123/123 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4d. `KILLTABLE_v7_staged.txt` (the mutants are `run_mutants_v7.py`'s MUTANTS; the v7 additions follow)

```
# controls md5 836927f03474c85de42bd5f247cdfcc5
# driver md5 68d819c958abc6d46b9938ecde306902
# dashokclass kill table (v7) -- controls run_controls_v7.run-073901.py, 2 at a time
BASE          123/123
d_cutoff18      113/123 killed by: C1 C11 C12 C12s C20 C3 W1                               [C12]
d_cutgt         120/123 killed by: C12 C12s C3                                             [C12]
d_nodate        117/123 killed by: C12 C12s C20 C3                                         [C12]
d_lexdate       115/123 killed by: C12w C19b                                               [C19b]
d_noreason      121/123 killed by: C19a C19b                                               [C19a C19b]
d_blank         114/123 killed by: C1 C11 C12 C14 C26 W1                                   [C14]
d_domnohold     89/123  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C27 C29 C29b C2b C2c C3 C6 C7 C8 C9 W1 [C2c]
d_domnopend     89/123  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C27 C29 C29b C2b C2d C3 C6 C7 C8 C9 W1 [C2d]
d_dupplus1      85/123  killed by: C11 C14 C15 C16 C19a C19b C20b C21k C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C29b C5 C6 C9 W2 W4 W5 [C5 C9]
d_nonote        92/123  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C29b C2b C3 C6 C7 C8 C9 W1 [C1]
d_nonote2       109/123 killed by: C15 C16 C19a C20 C20b C21k C25e C25f C25o C29 C29b C3 C6 C9 [C15 C16]
d_lastwins      122/123 killed by: C17b                                                    [C17b]
d_ledger1       122/123 killed by: C21h                                                    [C21h]
d_nomd5         122/123 killed by: C18                                                     [C18]
d_pinoverride   108/123 killed by: C11 C12 C12s C12w C17b C18                              [C18]
d_crlfpin       122/123 killed by: C18b                                                    [C18b]
d_noreconf      107/123 killed by: C11 C14 C19a C19b C20 C20b C21k C26 C26b C28 C28b C29 C3 C4 C5 C6 [C20]
d_notenone      123/123 escapes (as recorded)                                              [UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note]
r_nolegend      122/123 killed by: R4                                                      [R4]
r_tipclause     114/123 killed by: R1 R1c R1e R1f R1g R1o R1o2 R1q R1w                     [R1 R1c]
r_tiptail       115/123 killed by: R1 R1e R1f R1g R1o R1o2 R1q R1w                         [R1]
r_ok            108/123 killed by: R1 R1b R1d R1e R1f R1g R1h R1n R1o R1o2 R1q R1w R2 R3   [R1]
r_pend          108/123 killed by: R1 R1b R1d R1e R1f R1g R1h R1n R1o R1o2 R1q R1w R2 R3   [R1]
r_noescape      121/123 killed by: R1b R3                                                  [R1b]
r_wsblank       119/123 killed by: R1d R1n R1w R3                                          [R1d]
r_strip         121/123 killed by: R2 R2b                                                  [R2]
w_envkeep       121/123 killed by: W4 W5                                                   [W4 W5]
w_ledgerkeep    122/123 killed by: W5                                                      [W5]
w_collapse      119/123 killed by: W3 W7 W8 W9                                             [W3]
w_rc7           118/123 killed by: W2 W4 W5 W7 W9                                          [W2]
w_msg           120/123 killed by: W2 W4 W5                                                [W2]
w_subshell      120/123 killed by: W2 W4 W5                                                [W2]
d_date10        119/123 killed by: C12w C25a C25b                                          [C25a C25b]
d_dstrip        121/123 killed by: C25c C25n                                               [C25c]
d_dfold         92/123  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C29b C2b C3 C6 C7 C8 C9 W1 [C1]
d_dfold2        115/123 killed by: C19a C20b C21k C25d C29 C29b C3 C6                      [C25d]
d_notestrip     92/123  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C29b C2b C3 C6 C7 C8 C9 W1 [C1]
d_notefold      92/123  killed by: C1 C10 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C29 C29b C2b C3 C6 C7 C8 C9 W1 [C1]
d_seatstrip     121/123 killed by: C25g C25p                                               [C25g]
d_seatfold      122/123 killed by: C25h                                                    [C25h]
d_phasestrip    121/123 killed by: C25i C25q                                               [C25i]
d_phasefold     122/123 killed by: C25j                                                    [C25j]
d_shaperows     122/123 killed by: C21d                                                    [C21d]
d_shapeents     122/123 killed by: C21f                                                    [C21f]
d_shapeentry    121/123 killed by: C21e C21m                                               [C21e]
d_noshape       117/123 killed by: C21d C21e C21f C21i C21m                                [C21d C21e C21f]
d_basedict      122/123 killed by: C21g                                                    [C21g]
r_norecord      122/123 killed by: R1e                                                     [R1e]
r_okonly        120/123 killed by: R1g R1q R1w                                             [R1g]
r_stripok       121/123 killed by: R2 R2b                                                  [R2]
r_refusallast   122/123 killed by: R1f                                                     [R1f]
w_nochecker     122/123 killed by: W6                                                      [W6]
d_unread0       122/123 killed by: C23                                                     [C23]
d_summary       119/123 killed by: C11 C12                                                 [C11]
r_tipokonly     120/123 killed by: R1g R1q R1w                                             [R1g]
r_tipnonblank   121/123 killed by: R1g R1w                                                 [R1g]
r_clsstrip      119/123 killed by: R1g R1h R3                                              [R1h]
d_isheld        90/123  killed by: C1 C10 C11 C12 C12w C17b C18 C18b C19a C2 C20 C20b C21k C22 C24 C29 C29b C2b C3 C6 C7 C8 C9 W1 [C24]
d_nulld         122/123 killed by: C26                                                     [C26]
d_nohint        122/123 killed by: C11                                                     [C11]
d_domzxq        121/123 killed by: C11 C27                                                 [C27]
r_dclasszxq     122/123 killed by: C27                                                     [C27]
d_cut2days      122/123 killed by: C12                                                     [C12]
d_baselen       117/123 killed by: C1 C12 W1                                               [C1]
w_nosed         122/123 killed by: W2                                                      [W2]
r_wsspace       120/123 killed by: R1d R1w R3                                              [R1d]
d_domredef      121/123 killed by: C11 C27                                                 [C27]
r_dclassredef   122/123 killed by: C27                                                     [C27]
d_dompad        121/123 killed by: C28 C28b                                                [C28]
d_rowstrip      121/123 killed by: C25l C25r                                               [C25l C25r]
d_rowrstrip     122/123 killed by: C25l                                                    [C25l]
d_rowlstrip     122/123 killed by: C25r                                                    [C25r]
d_datelstrip    122/123 killed by: C25m                                                    [C25m]
d_dlstrip       122/123 killed by: C25n                                                    [C25n]
d_notelstrip    122/123 killed by: C25o                                                    [C25o]
d_seatlstrip    122/123 killed by: C25p                                                    [C25p]
d_phaselstrip   122/123 killed by: C25q                                                    [C25q]
d_cutreason     121/123 killed by: C20 C3                                                  [C3]
d_ceilreason    116/123 killed by: C19a C20b C21k C29 C29b C6 C9                           [C6 C9]
d_rowphaseswap  114/123 killed by: C19a C20 C20b C21k C29 C29b C3 C6 C9                    [C9]
d_basewithin    120/123 killed by: C12                                                     [C12]
d_isodollar     122/123 killed by: C12s                                                    [C12s]
d_len7ge        122/123 killed by: C17c                                                    [C17c]
d_boolcount     122/123 killed by: C17d                                                    [C17d]
d_negcount      122/123 killed by: C17e                                                    [C17e]
d_zerocount     122/123 killed by: C17f                                                    [C17f]
d_floatcount    122/123 killed by: C17g                                                    [C17g]
d_str1          122/123 killed by: C17h                                                    [C17h]
d_str5          122/123 killed by: C17i                                                    [C17i]
d_isosearch     123/123 escapes (as recorded)                                              [UNPINNED: equivalent -- the ISO pattern is anchored with ^, so search and match agree on every string]
d_nostr         122/123 killed by: C26b                                                    [C26b]
d_hintundated   122/123 killed by: C6                                                      [C6]
d_datenone      122/123 killed by: C6                                                      [C6]
d_cutoffmsg     116/123 killed by: C1 C11 C12 W1                                           [C1 C11 C12]
d_rowsabsent    121/123 killed by: C21i                                                    [C21i]
r_sumstrip      122/123 killed by: R2b                                                     [R2b]
r_tipnorecord   122/123 killed by: R1e                                                     [R1e]
r_tipnotnull    122/123 killed by: R1g                                                     [R1g]
r_nullpend      121/123 killed by: R1g R1n                                                 [R1n R1g]
r_striplabel    121/123 killed by: R2 R2b                                                  [R2]
r_wsset         120/123 killed by: R1d R1w R3                                              [R1d]
r_css0          122/123 killed by: R5                                                      [R5]
r_cssoutline    122/123 killed by: R5                                                      [R5]
w_elif2         120/123 killed by: W7 W8 W9                                                [W7 W8]
w_no2to1        121/123 killed by: W7 W9                                                   [W7]
d_domglobals    121/123 killed by: C11 C27                                                 [C27]
d_domglobalsaug 121/123 killed by: C11 C27                                                 [C27]
d_domexec       121/123 killed by: C11 C27                                                 [C27]
d_domsetattr    121/123 killed by: C11 C27                                                 [C27]
d_domarg        122/123 killed by: C27                                                     [C27]
r_dclassglobals 122/123 killed by: C27                                                     [C27]
r_dclassupdate  122/123 killed by: C27                                                     [C27]
r_dclasssetitem 122/123 killed by: C27                                                     [C27]
d_dompadr       122/123 killed by: C28b                                                    [C28b]
r_clsrstrip     119/123 killed by: R1g R1h R3                                              [R1h]
d_strskip1      122/123 killed by: C17j                                                    [C17j]
d_strskip2      122/123 killed by: C17k                                                    [C17k]
d_strskip3      121/123 killed by: C17l C17n                                               [C17l]
d_strskip4      122/123 killed by: C17m                                                    [C17m]
d_isowidthy     122/123 killed by: C12w                                                    [C12w]
d_isowidthm     122/123 killed by: C12w                                                    [C12w]
d_isowidthd     122/123 killed by: C12w                                                    [C12w]
d_isosep1       122/123 killed by: C12w                                                    [C12w]
d_isosep2       122/123 killed by: C12w                                                    [C12w]
d_hinttext      122/123 killed by: C11                                                     [C11]
d_hintalways    122/123 killed by: C1                                                      [C1]
d_reconfreplace 121/123 killed by: C11 C20                                                 [C20]
d_notelatin1    59/123  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C29b C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C20b]
d_notenostr     122/123 killed by: C21k                                                    [C21k]
d_entriesdef1   58/123  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21j C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C29b C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C21j]
d_entriesdef2   58/123  killed by: C1 C10 C11 C12 C12s C12w C14 C15 C16 C17b C18 C18b C19a C19b C2 C20 C20b C21j C21k C22 C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C28b C29 C29b C2b C3 C4 C5 C6 C7 C8 C9 W1 W2 W4 W5 [C21j]
d_phasenone     122/123 killed by: C29                                                     [C29]
d_seatnone      122/123 killed by: C29                                                     [C29]
r_tipinsertm2   121/123 killed by: R1o R1o2                                                [R1o]
r_tipnoev       121/123 killed by: R1o R1o2                                                [R1o]
r_escstrip      122/123 killed by: R1h                                                     [R1h]
r_cssoverride   122/123 killed by: R5                                                      [R5]
w_tail1         122/123 killed by: W7                                                      [W7]
r_tippend       122/123 killed by: R1p                                                     [R1p]
r_tipnotok      121/123 killed by: R1p R1p2                                                [R1p]
r_tipempty      122/123 killed by: R1q                                                     [R1q]
r_glyphstrip    121/123 killed by: R1h R3                                                  [R1h]
r_wsset4        121/123 killed by: R1w R3                                                  [R1w]
r_sumcrash      100/123 killed by: C27 R1 R1b R1c R1d R1e R1f R1g R1h R1n R1o R1o2 R1p R1p2 R1q R1w R2 R2b R3 R4 R5 [C27 R2]
d_domusesite    122/123 killed by: C27                                                     [C27]
d_strnone       122/123 killed by: C17n                                                    [C17n]
d_hinttail      122/123 killed by: C11                                                     [C11]
d_isodigits     121/123 killed by: C12w                                                    [C12w]
w_q2paren       122/123 killed by: W2                                                      [W2]
r_tipnows       121/123 killed by: R1g R1w                                                 [R1g]
r_tipnows2      122/123 killed by: R1w                                                     [R1w]
r_tipall        121/123 killed by: R1p R1p2                                                [R1p]
d_hintjoin      121/123 killed by: C11 C27                                                 [C11]
d_domsysmod     121/123 killed by: C11 C27                                                 [C27]
d_isotrunc      122/123 killed by: C12w                                                    [C12w]
w_elifne3       122/123 killed by: W9                                                      [W9]
w_named         122/123 killed by: W2                                                      [W2]
d_domnonliteral 122/123 killed by: C27                                                     [C27]
d_domattrexec   121/123 killed by: C11 C27                                                 [C27]
d_dommain       121/123 killed by: C11 C27                                                 [C27]
d_domuseinline  122/123 killed by: C27                                                     [C27]
r_dclassmatchrest 122/123 killed by: C27                                                     [C27]
r_dclassalias   122/123 killed by: C27                                                     [C27]
r_dclassbuiltins 122/123 killed by: C27                                                     [C27]
r_dclasssetattr 122/123 killed by: C27                                                     [C27]
r_dclassfglobals 122/123 killed by: C27                                                     [C27]
r_dclassuseinline 120/123 killed by: C27 R3                                                  [C27]
r_sumuseinline  122/123 killed by: C27                                                     [C27]
d_rowlist       122/123 killed by: C21l                                                    [C21l]
d_entrylist     122/123 killed by: C21m                                                    [C21m]
d_rowidnone     122/123 killed by: C29b                                                    [C29b]
d_isoyear3      122/123 killed by: C12w                                                    [C12w]
d_isomonth3     122/123 killed by: C12w                                                    [C12w]
r_tipbadge      122/123 killed by: R1p2                                                    [R1p2]
r_tipev         122/123 killed by: R1p2                                                    [R1p2]
r_tipgradeonly  122/123 killed by: R1o2                                                    [R1o2]
r_tipevonly     122/123 killed by: R1o2                                                    [R1o2]
r_tipbadges     122/123 killed by: R1o2                                                    [R1o2]
r_css2block     122/123 killed by: R5                                                      [R5]
r_cssescape     122/123 killed by: R5                                                      [R5]
r_sumcounterkey 121/123 killed by: C27 R2b                                                 [R2b]
KILL TABLE: 181/181 as recorded
DASHOKCLASS_MUTANTS_DONE
```

```python
    #  v7 -- the v6 pass's survivors (four seats), each rebuilt here verbatim, and the generating-set members v7 rows
    ("d_domnonliteral", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = tuple(("✓", "✕", "⏸", "…"))')], ["C27"]),
    ("d_domattrexec", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                   'import builtins\nbuiltins.exec(\'DOMAIN = DOMAIN + ("ZXQ",)\')\nCUTOFF = "2026-10-17"               # inclusive')],
     ["C27"]),
    ("d_dommain", "checker", [('if __name__ == "__main__":\n',
                               'if __name__ == "__main__":\n    import builtins\n    builtins.globals()["DOM" + "AIN"] = ("✓", "✕", "⏸", "…", "ZXQ")\n')],
     ["C27"]),
    ("d_domuseinline", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'x["d"] in ("✓", "✕", "⏸", "…", "ZXQ") or not st.is_answer(x):')],
     ["C27"]),
    ("r_dclassmatchrest", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                      'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n'
                                      'match {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}:\n'
                                      '    case {**D_CLASS}:\n        pass')], ["C27"]),
    ("r_dclassalias", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n_e = exec\n_e(\'D_CLASS["ZXQ"] = "ok"\')')],
     ["C27"]),
    ("r_dclassbuiltins", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                     'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport builtins\n'
                                     'builtins.exec(\'D_CLASS["ZXQ"] = "ok"\')')], ["C27"]),
    ("r_dclasssetattr", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                    'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport builtins as _b, sys as _s\n'
                                    '_b.setattr(_s.modules[__name__], "D_CLASS", {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"})')],
     ["C27"]),
    ("r_dclassfglobals", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                     'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\nimport sys as _s2\n'
                                     '_s2._getframe().f_globals["D_CLASS"] = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')],
     ["C27"]),
    ("r_dclassuseinline", "render", [("cls = D_CLASS.get(d, LEGACY)",
                                      'cls = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}.get(d, LEGACY)')], ["C27"]),
    ("r_sumuseinline", "render", [("n[d if d in D_CLASS else LEGACY] += 1", 'n[d if d in ("✓", "⏸", "✕", "…", "ZXQ") else LEGACY] += 1')],
     ["C27"]),
    ("d_rowlist", "checker", [("        if not isinstance(r, dict):", "        if not isinstance(r, (dict, list)):")], ["C21l"]),
    ("d_entrylist", "checker", [("            if not isinstance(x, dict):", "            if not isinstance(x, (dict, list)):")], ["C21m"]),
    ("d_rowidnone", "checker", [('str(r.get("id"))', 'str(r.get("id") or "")')], ["C29b"]),
    ("d_isoyear3", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{3,4}-\\d{2}-\\d{2}")')], ["C12w"]),
    ("d_isomonth3", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2,3}-\\d{2}")')], ["C12w"]),
    ("r_tipbadge", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY or badge:\n")], ["R1p2"]),
    ("r_tipev", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY or ent.get("ev"):\n')], ["R1p2"]),
    ("r_tipgradeonly", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and (not ent.get("ev") or ent.get("grade")):\n')], ["R1o2"]),
    ("r_tipevonly", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and (not ent.get("grade") or ent.get("ev")):\n')], ["R1o2"]),
    ("r_tipbadges", "render", [("    if cls == LEGACY:\n", '    if cls == LEGACY and badge != "s":\n')], ["R1o2"]),
    ("r_css2block", "render", [("</style>", "</style><style>.c.legacy .g {{ font-size:0; }}</style>")], ["R5"]),
    ("r_cssescape", "render", [(".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}",
                                ".c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}\n.c.lega\\\\63 y .g {{ font-size:0; }}")],
     ["R5"]),
    ("r_sumcounterkey", "render", [("n[d if d in D_CLASS else LEGACY] += 1", "n[d if d in n else LEGACY] += 1")], ["R2b"]),
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
+  at landing.  Controls `regress/artifacts/dashokclass_20261016/RECEIPT_v7_on_staged_v5.txt`; kill table `regress/artifacts/dashokclass_20261016/KILLTABLE_v7_staged.txt`.
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
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the dashokclass landing (RULINGS_C F2): every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class, 'legacy -- verdict unclassified', its text kept and its reason in the tooltip; precommit Q2 (check_entry_domain.py) holds the off-domain answers to a ceiling frozen at landing -- per (row, phase, seat, date, d, note sha1), no more answers than the md5-pinned baseline holds.  The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities cannot exceed their landing baseline.  Witness: R2, 670 cells moved from the seat-failure class to legacy with nothing else changing.  The controls' CONTRACT rows, for each decision of the checker, the renderer change and Q2, its GENERATING SET and its COMPLEMENT -- every operand position, both ends, both directions of every width, every optional field alone and together, on legacy and non-legacy cells -- and the glyph sets by their EFFECT, read after running both files, with each named binding form refused and each use counted; what it does not row it discloses with its reason.  Seven passes on the staged files -- pass 2, the adjudication pass and the v3, v4, v5, v6 and v7 passes, the owner's four-seat roster each time (Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- GPT-6 Astra: a per-(row, phase, seat, date, d) count let a converted entry's allowance be refilled by a new answer (measured rc 0); the tooltip's 'not approval, not a seat failure' is contradicted by legacy answers whose notes record real failures; the baseline writer's placement is no guard.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/codex_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2 (v1): SHIP WITH CHANGES (4) -- GLM 5.3: the rc-2 path through the gate untested, no escapable-d fixture, no refill control, no legend line for an explicit blank.  All added in v2 (W3, R1b, C15, the legend line).", "ev": "regress/artifacts/dashokclass_20261016/pass2/glm_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured; CUTOFF moved to 2026-10-18 passed all 19 v1 controls; the precommit's cp1252 pipe raised UnicodeEncodeError on the failure lines; legacy answers whose notes name a non-answer; control gaps in C1, C11, R1-R3, W1-W2.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/fable5_dashok.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- Grok 4.7: an exported GXDOMAIN_BASELINE was honoured inside the hook; the loader kept the LAST count for a repeated key; the tooltip's denial and the unpinned inclusive cutoff.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/grok_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the 'identity' key is a CEILING over selected content (a byte-identical revert and a same-note replacement pass; 1,342 keys cover 1,356 answers) -- state the narrower guarantee or build provenance; three one-edit survivors (the tooltip clause restored after the checked prefix, `-u GXLEDGER` deleted, the loader's += made =); the v2 runner named the v1 controls; four claims to correct.  All applied in v3, the narrower guarantee stated in its words.", "ev": "regress/artifacts/dashokclass_20261016/f2/codex_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3: d_nonote dies on the baseline mismatch, not on the note (add the coherent two-edit form); the loader's summation pinned by nothing; R1 and R4 pinned prefixes only.  All applied in v3 (d_nonote2 killed by C15 and C16 -- among others, the v5 table showing nine; C17b; whole-string R1 and R4).", "ev": "regress/artifacts/dashokclass_20261016/f2/glm_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v2 receipts reproduce only with v2 under v1's name; six one-edit mutants pass all 35 (the tooltip tail, the malformed-date reason, which Q2 branch fired); three sentences overclaim; and its own pass-2 'note out of the key' was wrong.  All applied in v3.", "ev": "regress/artifacts/dashokclass_20261016/f2/fable5_dashokf2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: the note-only toll is this check's, not the ruling's; the Q2 comment's growth claim and 'can only shrink' survived; the raw-byte md5 pin reds a default Git-for-Windows checkout (the main loop measured it the same hour: a fresh clone gives 89d1d370 for 06a3ffc6; Fable 5.1 reproduced it on the v3 pass).  All applied in v3 (the pin folds CRLF; C18b).", "ev": "regress/artifacts/dashokclass_20261016/f2/grok_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v7 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v7 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v7 pass, NOT FIRED: the kimi seat sat outside the roster."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v7 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v7 pass, NOT FIRED: minimax-m3 was given no packet; the roster, not a wall."}
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
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V6 PASS: SHIP WITH CHANGES (8) -- Fable 5.1 (claude-fable-5-1 wrote the answer; the seat refused twice mid-run and claude-opus-4-8 ran 12 turns of its mutant sweep, re-run after a disk-full cleanup -- disclosed by agent_models.py; resumed, Fable 5.1 wrote the file), measuring in a mirror: 28 one-edit mutants through the 116 -- the class line on a NON-legacy cell carrying a badge or evidence (graded clause (d), the open fourth cell of a two-by-two), builtins.setattr and a frame-globals store past C27, a non-literal binding crashing the walk, list rows and entries, a row with no id.  All rowed in v7.", "ev": "regress/artifacts/dashokclass_20261016/v6pass/fable5_dashokv6.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V6 PASS: SHIP WITH CHANGES (6) -- GPT-6 Astra, measuring in memory: zero floor breaches on an enumerated (a)-(d) denominator; clause-(e) survivors -- C27's mapping-rest, aliased and attribute-path exec; the ISO widths' other directions; optional-field combinations; a second style block and an escaped selector; the counter keys as spellings -- and six records sentences (115 for 116, C12w's summary, C20b's isolation, the moved-not-removed class line).  All rowed or corrected in v7.", "ev": "regress/artifacts/dashokclass_20261016/v6pass/codex_dashokv6.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V6 PASS: SHIP WITH CHANGES (7) -- Grok 4.7 (shell denied; every item traced): the unguarded literal_eval in C27 (graded clause (c); adjudicated V19's apparatus class -- the null medium still scores), C27's binding and call forms, the ISO width directions, R1o's single fields, R5's other blocks and escapes, the strip's counter keys, eight records sentences.  All addressed in v7.", "ev": "regress/artifacts/dashokclass_20261016/v6pass/grok_dashokv6.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V6 PASS: SHIP WITH CHANGES (4) -- GLM 5.3 (glm-5.3:cloud, packet-fed), reasoned: C27's banned-call check name-path-only (builtins.globals() in the module body or the __main__ block), a numeric or list d unrowed at the renderer, the tok and empty cells' tooltips, 115 for 116.  Rowed or disclosed in v7 (a list d crashes the renderer -- unreachable through Q2 -- disclosed).", "ev": "regress/artifacts/dashokclass_20261016/v6pass/glm_dashokv6.txt", "d": "✓"}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] dashokclass closed by its landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v7_on_staged_v5.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 123/123 -- in particular R2 (only pend -> legacy, 670 cells, the strip string exact), R2b (the fixture strip by exact membership), C15/C16 (the note in the key), C25a-r (each key field byte for byte, at both ends), C17b-n (the baseline row's every clause and every string position), C18/C18b (the md5 pin, CRLF folded), C21a-m (a misshapen ledger or baseline is rc 2, a list row or entry included; a row without entries is empty), C27 (one literal binding of each glyph set, every named binding form refused, each use counted, and BOTH files' effective sets read by running them), C28/C28b (a glyph padded at either end), C29 and C29b (no phase or seat; no row id), C20/C20b (non-ASCII d and note), C3/C6/C9/C19a (each refusal line whole), C11 (the hint whole), C12 (the cutoff, the summary exact), C12s and C12w (the ISO shape's anchor, both directions of each width and both separators, by rc), R1e/R1g/R1n/R1o/R1o2 (whole tooltips -- null, a number, a bool, each optional field alone and all together), R1p/R1p2/R1q (no class line outside legacy, optional fields or not; a bare legacy cell), R1h/R1w (the glyph text exact; every whitespace code point), R5 (the CSS, and no other rule naming the class in any style block, escapes decoded) and W4-W9 (exported overrides stripped; the checker absent, an unexpected status -- its FIRST line, every status 2-255 -- and a missing python are BAD) -- and does regress/artifacts/dashokclass_20261016/KILLTABLE_v7_staged.txt's runner still kill every pinned mutant?  Is the record (the checker's docstring, the Q2 comment, the CHANGELOG block, the bug-file closure) true of what shipped, and is the narrower guarantee -- a ceiling over selected content, not an entry identity -- stated where a reader will meet it?"
  state: "closed"
  state_note: "filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, \"pend\")`; HEAD's ledger carries 439 entries with d \"OK\" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS (\"OK\": \"ok\") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d \"OK\".  LOW, display only.\n\n[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line \"OK\": \"ok\", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class (a live hold and a non-answer record keep their own rendering), its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at landing.  The 365 above counts OK cells only; the legacy class is 670 displayed cells (1,397 entries) at HEAD 8bf8b5a1."
  witness: "harness:regress/artifacts/dashokclass_20261016/RECEIPT_v7_on_staged_v5.txt -- R2: HEAD's renderer (gen_dashboard_before.py) shows 1,503 displayed cells in the seat-failure class and the staged one 833, the 670 moved now LEGACY with nothing else changing; C1-C29b and W1-W9 pin the entry-domain check and Q2; regress/artifacts/dashokclass_20261016/KILLTABLE_v7_staged.txt kills every pinned mutant (181/181 as recorded, two escapes recorded as equivalent)"
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

### 5d. the CHANGELOG block (a DRAFT: its v7-pass sentence is written from this pass's answers)

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
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v7.py`, 123 rows, its docstring the CONTRACT: each decision
  of the checker, the renderer change and Q2 with its GENERATING SET -- every operand position, both ends of each field,
  both directions of every width and both separators of the ISO shape, every optional tooltip field alone and together on
  legacy and non-legacy cells, every `str.isspace()` code point, a list row and a list entry, a row with no id -- and its
  COMPLEMENT (only legacy cells carry the class line; the set where it is used), each member rowed or disclosed with its
  reason.  C27 reads the glyph sets by their EFFECT: both files run as `__main__` on a fixture and their sets are read from
  the globals after the run, which closes runtime rebinding whatever its syntax; the ast walk refuses each named binding
  form (a banned builtin by name, by attribute or by reference; a mapping-pattern rest; a store into a frame's globals), a
  non-literal binding rather than crashing on it, and counts each use.  123/123 on the staged files, installed byte for byte
  (`RECEIPT_v7_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v7.py`: 181/181 as recorded
  (`KILLTABLE_v7_staged.txt`) -- 179 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356 off-domain
  answers has an empty note, and no note anywhere is the string "None") and `d_isosearch` (the pattern is `^`-anchored)
  equivalent escapes; `d_nonote2` and `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms) -- `d_nonote2`
  killed by C15 and C16 among others, `d_dfold2` by C25d (Grok 4.7, v6 pass: the v6 text read as if both died on all three).  The note-type scope is disclosed: a list or dict note holding a non-answer token as an element or a
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
whitespace set (29 code points).  **V6 pass** (`v6pass/`): Fable SWC 8 (its seat refused twice and claude-opus-4-8
ran 12 turns of its sweep; resumed, Fable 5.1 wrote the answer), Astra SWC 6, Grok SWC 7, GLM SWC 4 -- C27's universal
false at the renderer and in the main block (all four), a non-literal binding crashing the walk (three), and members
still open: list rows and entries, the widths' other directions, single optional fields, the non-legacy optional-field
cell (graded clause (d) by Fable 5.1, (e) by GPT-6 Astra; rowed either way), every style block, the counter keys, a
numeric d, a row with no id; eight records sentences.  All rowed in v7, which reads the glyph sets by their effect.
**V7 pass** (`v7pass/`): [to be written from its answers].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.


## 2c. The disagreements, both sides in their own words

**D1 -- W2's grade.**  Grok 4.7: *"One floor breach: clause (c), the unguarded `literal_eval`. ... The exception then skips
`DASHOKCLASS_CONTROLS_DONE`. `one()` records INCOMPLETE and drops the reds. That is the lost-kill form measured on
`D_CLASS["OK"] = "ok"` in the v5 pass, now on the new detector. A comment-only file does not take this path."*  The main
loop: clause (c) is the NULL MEDIUM -- a product carrying none of the behaviour under test -- and Grok's own trace shows the
comment-only medium still scores; a non-literal binding is a mutant, and its crash is fail-safe (INCOMPLETE fails the table,
never passes it).  It is V19's apparatus class, repaired in v7 as L1 either way.  **Grok: rule first.**

**D2 -- W7's grade.**  Fable 5.1: *"Floor breach, clause (d) -- one cell, two mutants, one row closes it. ... The guard
`cls == LEGACY` crossed with body-read, body-tested, jointly reachable lvalues (grade, badge, ev -- the builder tests each ...)
gives four cells; three are rowed and the symmetric fourth is not.  That is the #499 shape."*  GPT-6 Astra (on the same
family): *"These are clause-(e) cases: the class-line guarded body reads `tip` and `d`, not these optional-field
combinations."*  The main loop: rowed either way (R1p2); the grade decides only whether the v6 pass could have closed.
**Fable and Astra: rule first.**

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **The disagreements you are a party to** (2c): rule on them, harder on the side that is yours.
2. **Your own findings** (the W-rows naming you): is my disposition right, AND is the fix right -- does the named row go red
   under the named mutant for the reason named?
3. **The effective read and the use count** (W1, W3; 2b): sound, complete, and not a new failure mode of its own?
4. **The floor.**  Is there a one-edit mutant of the staged files, NOT in the table, that passes all 123 controls and breaks a
   ruled property or a line of the CONTRACT?  **Grade each: a floor breach (clauses a-d) or clause-(e) debt, and why.**  A
   zero needs its denominator.
5. **The records** (sections 4b, 5): name any sentence that is false.
6. **Which of my 20 dispositions is WRONG?**  Name the count you checked.
7. **Does the chain close here?**  One line, with the denominator.

Label each claim MEASURED (you ran it), READ (you opened the file) or REASONED.  Write nothing to any project tree.
