# V5 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v5 = EACH PIN'S DUAL EDGE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v5 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v5/` (mirroring `tools/`; v5 changes only two title lines of v4's); the
controls are `run_controls_v5.py` and `run_mutants_v5.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming
the staged files; the v4-pass answers are in `v4pass/` (Fable's mirror measurements in `v4pass/fable5_meas/`).  Everything a
packet-fed seat needs is inlined below.

**Why v5.**  The v4 pass found 21 one-edit mutants passing all 72 v4 controls, 15 of them at decisions v4 listed as pinned,
and Fable 5.1 named their one shape: **each pin tested ONE edge of its decision** -- the trailing end of a key field but not
the leading one, the first literal line but not the binding that takes effect, a number but not its label, a substring but
not the whole tooltip, two branches of Q2's three.  So v5 rows the DUAL edge of every pin: for each decision, the edit its v4
pin would not see.  The staged CODE is unchanged (the seats found no defect in it); the controls grew from 72 to 96 and the
kill table from 66 to 105 mutants.  **This pass's job is to VERIFY that every pin now holds at both edges**, and that no
decision of the checker, the renderer change or the Q2 block is missing.  The chain closes on the first pass whose zero floor
breaches survive adjudication; if you find none, NAME THE DECISIONS YOU CHECKED.  Check the premises in 2b; do not ratify them.

**Liveness:** open your answer with the token `GLM_DASHOKV5_20261017` on its own line, then your verdict line.

## 1. The v4-pass verdicts

* **Fable 5.1 -- SHIP WITH CHANGES (18)** (`v4pass/fable5_dashokv4.md`; claude-fable-5-1 throughout).  Measured in a mirror:
  72/72 and the 66-mutant table reproduce byte for byte; 29 mutants of its own through the 72.
* **GPT-6 Astra -- SHIP WITH CHANGES (4)** (`v4pass/codex_dashokv4.txt`).  Ten survivors run in memory.
* **Grok 4.7 -- SHIP WITH CHANGES (6)** (`v4pass/grok_dashokv4.txt`).  Six survivors traced.
* **GLM 5.3 -- SHIP WITH CHANGES (4)** (`v4pass/glm_dashokv4.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| K1 | Fable, Grok, Astra | the checker-side padded glyph: `str(x["d"]).strip() in DOMAIN` passes all 72 (only the renderer's R1h held a padded ✓), so Q2 would admit an answer the dashboard shows as legacy | **PINNED**: C28 (a new answer before the cutoff with d " ✓" -> rc 1).  Mutant `d_dompad` |
| K2 | Fable | C27 read the FIRST `DOMAIN = ` / `D_CLASS = ` line; a second assignment further down is the one that takes effect, and passes | **PINNED**: C27 walks each file's ast -- exactly ONE binding of the name anywhere (every store, any `global` refused), at module level, its literal the four.  Mutants `d_domredef`, `r_dclassredef` |
| K3 | Fable, Grok | `summary()` counting by a stripped d passes: R2 recomputes on the shipped ledger, which holds no padded glyph | **PINNED**: R2b (the FIXTURE page's strip, exactly, against the fixture's own counts -- its padded ✓ and its null count legacy).  Mutant `r_sumstrip` |
| K4 | Fable, Grok, Astra | the key's LEADING end: `.lstrip()` on the date, d, seat, phase or note, and a row-id strip, pass (C25 edited only the trailing end; the CONTRACT's "C25 edits the ends" was false) | **PINNED**: C25l (a row id with a trailing space), C25m-q (date, d, note, seat, phase each with a LEADING space), C25r (a row id with a leading space).  Mutants `d_rowstrip`, `d_rowrstrip`, `d_rowlstrip`, `d_datelstrip`, `d_dlstrip`, `d_notelstrip`, `d_seatlstrip`, `d_phaselstrip` |
| K5 | Fable, Astra | each refusal line's content: the cutoff reason replaced, the ceiling reason emptied, row and phase swapped -- C11 counted lines, W2 checked a prefix | **PINNED**: the WHOLE refusal line at C3 (the cutoff reason), C6 (an undated entry: `date (none)`, no ISO clause), C9 (a frozen copy: the ceiling reason, every identifier in order) and C19a (the ISO clause).  Mutants `d_cutreason`, `d_ceilreason`, `d_rowphaseswap`, `d_hintundated`, `d_datenone` |
| K6 | Fable | the summary's baseline number equals the within-count wherever a row reads it (1356/1356, 0/0), so printing the within-count passes | **PINNED**: every C12 row's summary EXACTLY -- the fixture baseline holds N+1 and a refused entry leaves N within, so the two differ; C1 and C11 exact too (which also pins "inclusive").  Mutants `d_basewithin`, `d_cutoffmsg` |
| K7 | Fable, Grok, Astra | the ISO shape anchored at its end (`^...$`) refuses a matched `2026-10-17T12:00:00` by nothing | **PINNED**: C12s (a FROZEN identity dated `2026-10-17T12:00:00` -> rc 1).  Mutant `d_isodollar` |
| K8 | Fable, Grok, Astra | the baseline row test at its clauses: `len(k) >= 7`, `isinstance(k[6], int)` (a bool is an int), `k[6] != 0`, the string test narrowed -- each passes; the CONTRACT's `> 0` -> `>= 0` "equivalent" holds for the ceiling's arithmetic, not for the promised malformed-baseline exit | **PINNED**: C17c-i, the shipped baseline plus ONE misshapen row each (eight fields; a count of true; -1; 0; 1.0; a numeric first field; a numeric note sha) -> rc 2.  Mutants `d_len7ge`, `d_boolcount`, `d_negcount`, `d_zerocount`, `d_floatcount`, `d_str1`, `d_str5`.  The "equivalent" disclosure is dropped |
| K9 | Fable, Astra | R1e asserted the record line as a SUBSTRING, so dropping the class line from every cell with a record beside it passes | **PINNED**: R1e asserts the WHOLE tooltip (class line, date, note, record line).  Mutant `r_tipnorecord` |
| K10 | Fable, Grok, Astra | an explicit `"d": null` on the RENDERER is unrowed (C26 pins only the checker): rendering it pend, or skipping its class line, passes | **PINNED**: a fixture null entry -- R1n (legacy, the glyph `None`) and R1g (its whole tooltip).  Mutants `r_nullpend`, `r_tipnotnull` |
| K11 | Fable, Astra | the strip's LABELS: "1397 approved" passes (R2 read the numbers) | **PINNED**: R2 asserts the whole strip string.  Mutant `r_striplabel` |
| K12 | Astra, Fable | Q2's `else` narrowed to `elif [ $_cedrc -eq 2 ]` passes, leaving rc 7 or 127 silently green; dropping `2>&1` is unread | **PINNED**: W7 (a stub checker exiting 7 with its message on STDERR -> BAD "could not run (rc 7): <that message>"), W8 (python ABSENT from the PATH -- a real launch failure, rc 127 -> BAD).  Mutants `w_elif2`, `w_no2to1` |
| K13 | Astra, Fable | C24 is confounded: the shipped ledger carries five off-domain NOTSEAT records, so `d_isheld` reddened C24 for the LEDGER's reason | **FIXED**: C24 runs in a ledger holding only its own entry |
| K14 | Grok, Fable | the whitespace glyph's character set: `.strip(" \t")` passes (R1d held a space and a tab; R3's presence pin was the only thing that saw it) | **PINNED**: R1d adds a newline-only and an NBSP-only d.  Mutant `r_wsset` |
| K15 | Astra, Fable | the two CSS rules the class adds are read by nothing: `font-size:0` makes every legacy glyph invisible and passes | **PINNED**: R5 (both rules, exactly, on the page).  Mutants `r_css0`, `r_cssoutline` |
| K16 | Grok, GLM | a ledger with NO `rows` key is unrowed (`.get("rows", [])` would walk it as empty) | **PINNED**: C21i (`{}` and `{"seats": []}` -> rc 2).  Mutant `d_rowsabsent` |
| K17 | Fable | `str()` of d in the key: dropping it is equivalent on the baseline, but a list d raises in the Counter -- rc 1 WITH a traceback | **PINNED**: C26b (a new answer whose d is a LIST -> rc 1, no traceback).  Mutant `d_nostr` |
| K18 | Fable | equivalent or out-of-scope edits | **DISCLOSED / recorded**: `ISO.match` -> `ISO.search` (the pattern is `^`-anchored: tabled UNPINNED, measured to escape); `r_recheld` is HEAD's own record loop, outside this landing's diff; the Q2 section header is display only (`say` is stubbed in the W block) |
| K19 | GLM | a mis-typed note (list, None, dict) might be SKIPPED as a non-answer, rc 0 | **NO CHANGE, measured** (Fable 5.1, v4 pass): a list, None or dict note is refused rc 1, a bool rc 2; nothing is skipped.  C21h keeps the except-arm a measured rc 2 |
| K20 | GLM | a hold or record cell carrying an explicit off-domain d is unrowed | **NO CHANGE**: R1's fixture already holds both -- grok's HELD marker with d "HELD" (renders hold) and kimi's NOTSEAT record with d "OK" (renders a record, ∅) |
| K21 | GLM | the 72-row enumeration was not checkable from the packet | **FIXED in the packet**: section 4a inlines the controls whole |
| K22 | Fable, Astra | two TITLE lines kept the retired identity wording: the checker's docstring ("OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED") and the Q2 banner ("OR IS A FROZEN LEGACY ENTRY") | **FIXED** in `staged_v5` (section 3): "within the (frozen) legacy ceiling" |
| K23 | GLM, Fable, Astra | records: 5d's "killed by exactly C15/C16" (v4 kills `d_nonote2` by C15 C16 C25e C25f); "miss the baseline everywhere" (on HEAD's ledger the d fold changes 1,100 of 1,356 frozen keys, the note strip 2, the note fold 1,352); "68/72 on v3 (the four structure rows)" folds in C21g, a baseline object | **CORRECTED** in the CONTRACT, the CHANGELOG draft and `run_mutants_v5.py`'s comment on the one-sided folds -- that comment was corrected AFTER the kill table ran (the diff is comment lines only; the table's behaviour is unchanged) |
| K24 | Fable | RULINGS_C's "5,150 at the ruling's HEAD": 5,150 is the count at e483d931; at c64445fa, which committed the file, 5,167 | **CORRECTED** (section 5c) |
| K25 | Fable, Astra, Grok | `dashmissingd`'s "158 / 127 / 71" came from a screen whose regex was never written down; nobody could reproduce it | **REPLACED by a deriver**: `dashmissingd_census.py` now carries the screen, `/not[ -]fired|roster/i`, and prints 222 entries / 200 untokened / 87 with no d at HEAD 8bf8b5a1 -- the record cites that output |
| K26 | Astra | the sha1-16 disclosure gave one figure for two searches | **CORRECTED**: a note passing as a FROZEN entry's is a fixed-target second preimage (~2^64); an arbitrary collision between two new notes (~2^32, birthday) passes nothing |
| K27 | GLM | J3's red MECHANISM ("the v3 rows reddened for the ledger's reason") was asserted, not derivable from the packet | **KEPT, with its measurement named**: Fable 5.1 measured the shipped ledger's 21 ⏸ and 35 … answers (v4 pass, census) -- the reason the un-isolated rows went red |
| K28 | all four | NOTSEAT on the five not-fired entries | **UPHELD unanimously** (Astra withdrew its advice after measuring H: 9/9 untokened, 4/9 tokened): they stay untokened on this landing; `dashmissingd` carries the RULE question and Fable's mechanism (an entry-scoped "not fired by owner roster" token that `is_answer` treats as a non-answer, the renderer as a record, section H as roster-excused -- an owner decision).  Nine recorded seats are not nine reviews, and the prose says so |

## 2b. Premises to CHECK (stated as questions)

* **Every pin at both edges.**  For each decision in the CONTRACT (section 4a's docstring), does the row named on the OTHER
  edge actually go red under the edit its v4 pin missed?  The kill table (section 4c) claims so for 103 of 105 mutants.
* **Is "the dual edge of each pin" the whole class**, or does some decision have a THIRD edge -- an edit neither the v4 pin nor
  the v5 row sees (a middle-of-field strip is disclosed; what else)?
* **The ast walk (K2).**  Does counting every `Name` store of DOMAIN / D_CLASS, plus `global`s, catch every way a second
  binding can take effect -- or is there one it misses (`globals()[...]`, an import, a function attribute)?
* **W8's PATH.**  Is "python absent from the PATH" a faithful launch failure, and does the git-bash wrapper add any directory
  holding a python?  (The receipt shows `env: 'python': No such file or directory`, rc 127.)

## 3. The repair, staged v4 -> v5 (4 changed lines: two title lines; no code)

```diff
--- staged_v4
+++ staged_v5
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED.
+"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS WITHIN THE LEGACY CEILING FROZEN WHEN THIS CHECK LANDED.
 2026-10-16, ledger `dashokclass`; precommit section Q2.
 
 THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer -- or no
--- staged_v4/precommit_check.sh
+++ staged_v5/precommit_check.sh
@@ -493,7 +493,7 @@
 fi
 
 #  ---- Q2 --------------------------------------------------------------------------
-#  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS A FROZEN LEGACY ENTRY.  2026-10-16, ledger `dashokclass`
+#  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS WITHIN THE FROZEN LEGACY CEILING.  2026-10-16, ledger `dashokclass`
 #  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
 #  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
 #  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section holds the off-domain
```

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

### 3b. the renderer change, `gen_dashboard.py` HEAD -> staged v5 (32 changed lines)

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

## 4. The controls and their receipts

### 4a. the CONTRACT and the 96 rows -- the docstring of `run_controls_v5.py` (the whole file is in the tree)

```
"""Controls for `dashokclass` (2026-10-17, v5 after the v4 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
the three files under test (run_mutants_v5.py and the staged runs use them); the defaults are the tree's.

  THE CONTRACT (v5) -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7; GLM 5.3 read the packet) measured 21 one-edit mutants
  passing all 72 v4 controls, 15 of them at decisions v4 listed as pinned.  They share one shape (Fable 5.1): each pin tested
  ONE edge of its decision -- the trailing end of a key field, the first literal line, a number but not its label, a substring
  but not the whole tooltip, one branch of three.  So v5 rows the DUAL edge of every pin: for each decision below, the edit its
  v4 pin would not see.  The decisions are the checker's, the renderer's and Q2's, read from the three files.
    checker  ledger shape: an object, `rows' PRESENT and a list, row objects, entries   C21a-f, C21i (rows absent: {} and
             lists, entry objects                                                       {"seats": []}); C23 (not JSON)
             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
             fields, each of the six a str, the count an int and not a bool, > 0        key sums), C17c-i (eight fields, a true
                                                                                        count, -1, 0, 1.0, a numeric first field,
                                                                                        a numeric note sha), C21g (an object)
             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C28
                                                                                        (a padded ✓), C2/C2b/C2c/C2d (each glyph,
                                                                                        C2c/C2d isolated), C8 (hold), C24 (a
                                                                                        record, isolated)
             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
             ends; str() of d                                                           move), C25l-r (the leading end; a row id
                                                                                        with a trailing or a leading space);
                                                                                        C15/C16 (the note); C26b (a list d)
             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
             the cutoff: inclusive; a date counts only when the ISO shape OPENS it     C3, C4, C12 (isolated: before / on /
                                                                                        after / far, and C12s a MATCHED identity
                                                                                        dated 2026-10-17T12:00:00), C19a/b
             output: cp1252-safe; the summary line WHOLE (its baseline number is the   C20; C1, C11, C12 (the summary exact --
             frozen total, not the within-count); each refusal line WHOLE --           at C12-on the two numbers differ);
             identifiers in order, its reason; the hint                                C3, C6, C9, C19a (the refusal line
                                                                                        exact); C11 (the hint)
             the glyph set: ONE binding of DOMAIN and of D_CLASS, each the four         C27 (an ast walk of both files: every
                                                                                        store of the name, its value)
    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (padded), R1n (null),
             the answer a cell shows                                                    R3
             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip      R1 (OK), R1g (every simple legacy d,
                                                                                        null included), R1e (a record beside it),
                                                                                        R1f (a refused exemption first)
             the glyph: escaped; `?` for a blank or whitespace-only d (any whitespace)  R1b, R1d (space, tab, newline, NBSP)
             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
             its labels                                                                 string), R2b (the fixture ledger, whose
                                                                                        padded ✓ counts legacy)
             the legend line; the two CSS rules the class adds                          R4; R5
    Q2       the branches: rc 0 GOOD, rc 1 BAD with the refusal named, ANY other       W1, W2, W3 (rc 2), W7 (rc 7, its message
             status BAD "could not run" with the checker's first line, stderr included  on stderr), W8 (python absent: rc 127)
             the checker absent -> BAD                                                  W6
             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
    DISCLOSED, each with its reason:
      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
        (GPT-6 Astra, v4 pass: the two figures are different searches);
      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^';
      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
      the Q2 section header: `say' is stubbed in the W block, and it is display only.
    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
    two-edit design mutant d_dfold2, killed by C25d.

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
    C17c-i  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0; a numeric
         first field; a numeric note sha                                                            -> 2 each
    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
         the date NAMED as not ISO                                                                  -> 1 / 1
    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback   -> 1
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
    C23  a ledger that is not JSON                                                                  -> 2
    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
    C26  a new answer with an explicit "d": null                                                     -> 1
    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
    C27  DOMAIN and D_CLASS: ONE binding each (an ast walk -- a second assignment is the effective one), each exactly ✓ ✕ ⏸ …
    C28  a new answer BEFORE the cutoff with a PADDED glyph " ✓" (outside the four, as the renderer says) -> 1
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
         null), the date, the note
    R1h  a padded glyph " ✓" renders legacy, not ok
    R1n  an explicit "d": null renders legacy with the glyph "None", not …
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
         own count by exact membership, and its labels
    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
         a kill
    R4   the legend carries the legacy line EXACTLY
    R5   the page carries the two CSS rules the class adds, EXACTLY (the legacy outline; the glyph's muted italic 11px)
  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
  carry its BRANCH's own words):
    W1   the shipped ledger                    -> GOOD, failures 0
    W2   a new off-domain answer               -> BAD "beyond the frozen legacy ceiling", the entry named, failures >= 1
    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
    W7   a checker that exits 7 with its message on STDERR -> BAD "could not run (rc 7): <that message>", failures >= 1
    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
"""
```

### 4b. `RECEIPT_v5_on_staged_v5.txt`, whole

```
# dashokclass controls (v5) -- checker a6ff64d8 | renderer 516df040 | precommit 769f261f | baseline 06a3ffc6
C1   shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY     ok  rc 0: entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
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
C11  baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint printed ok  rc 1, 1356 of 1356 named; summary ok; hint ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-16 (before), the summary EXACTLY ok  rc 0 (want 0); summary ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-17 (on), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-18 (after), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12  cutoff isolated: a FROZEN identity dated 2027-01-01 (far), the summary EXACTLY ok  rc 1 (want 1); summary ok
C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00                 ok  rc 1 (want 1)
C13  an unreadable baseline                                                       ok  rc 2
C27  ONE binding each: the checker's DOMAIN and the renderer's D_CLASS keys are exactly ✓ ✕ ⏸ … ok  DOMAIN ('✓', '✕', '⏸', '…') | D_CLASS keys ['…', '⏸', '✓', '✕']
C17  a misshapen baseline (counts as strings)                                     ok  rc 2
C17b a key split across two baseline rows sums (alphaswpctxreg review grok 2026-09-08 'y' x2) ok  rc 0
C17c a misshapen baseline row: eight fields (override)                            ok  rc 2
C17d a misshapen baseline row: a count of true (override)                         ok  rc 2
C17e a misshapen baseline row: a count of -1 (override)                           ok  rc 2
C17f a misshapen baseline row: a count of 0 (override)                            ok  rc 2
C17g a misshapen baseline row: a count of 1.0 (override)                          ok  rc 2
C17h a misshapen baseline row: a numeric first field (override)                   ok  rc 2
C17i a misshapen baseline row: a numeric note sha (override)                      ok  rc 2
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
C21h an entry whose note is a number (it raises inside is_answer)                 ok  rc 2
C23  an unreadable ledger (not JSON)                                              ok  rc 2
R1   fixture row: class, glyph and the legacy tooltip EXACTLY, per seat           ok  9 cells; mismatches []; legacy tip exact
R1g  every simple legacy cell's WHOLE tooltip, the class line for ITS d           ok  12 legacy cells; no exact tooltip for: []
R1h  a padded glyph ' ✓' renders legacy, not ok                                   ok  cell ('legacy', ' ✓')
R1e  an answer with a record beside it: its WHOLE tooltip                         ok  cells 1; tooltip exact
R1n  an explicit null d renders legacy with the glyph None                        ok  cell ('legacy', 'None')
R1f  a refused exemption's line first, then the class line, exactly               ok  refusals 1; cells 1; tooltip exact
R1b  an escapable d renders escaped                                               ok  escape cell ('legacy', '&lt;b&gt;&amp;')
R1d  a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?         ok  whitespace cells [('legacy', '?'), ('legacy', '?'), ('legacy', '?'), ('legacy', '?')]
R1c  the fixture page says neither 'not approval' nor 'not a seat failure'        ok  render ok; found none
R4   the legend carries the legacy line EXACTLY                                   ok  legend found
R5   the page carries the legacy class's two CSS rules EXACTLY                    ok  missing []
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label) ok  before {'bad': 17, 'hold': 53, 'none': 29472, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 53, 'legacy': 670, 'none': 29472, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all' | ledger 5177 entries, 1397 off-domain
R2b  the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy) ok  strip '2✓ 1✕ 1⏸ 2… 14 legacy · 20 in all', want '2✓ 1✕ 1⏸ 2… 14 legacy · 20 in all'
R3   MUTANT ok renders and fails its check                                        ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT pend renders and fails its check                                      ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT noescape renders and fails its check                                  ok  escape cell ('legacy', '<b>&')
W1   Q2 on the shipped ledger                                                     ok  GOOD entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baselin | failures 0
W2   Q2 with a new off-domain answer                                              ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W3   Q2 with the baseline absent (rc 2 path)                                      ok  BAD check_entry_domain.py could not run (rc 2): APPARATUS FAIL: baseline unreadable or mis | failures 1
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W5   Q2 ignores an exported GXLEDGER naming a clean ledger                        ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W6   Q2 with the checker absent                                                   ok  BAD check_entry_domain.py MISSING -- the entry-domain check proved nothing | failures 1
W7   Q2 with a checker that exits 7, its message on stderr                        ok  BAD check_entry_domain.py could not run (rc 7): STUB CHECKER ON STDERR | failures 1
W8   Q2 with python absent from PATH (rc 127)                                     ok  BAD check_entry_domain.py could not run (rc 127): env: 'python': No such file or directory | failures 1
DASHOKCLASS CONTROLS: 96/96 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4c. `KILLTABLE_v5_staged.txt` (the mutants are `run_mutants_v5.py`'s MUTANTS; the v5 additions follow)

```
# dashokclass kill table (v5) -- controls run_controls_v5.run-030841.py, 3 at a time
BASE          96/96
d_cutoff18      88/96   killed by: C1 C11 C12 C12s C3                                      [C12]
d_cutgt         93/96   killed by: C12 C12s C3                                             [C12]
d_nodate        91/96   killed by: C12 C12s C3                                             [C12]
d_lexdate       95/96   killed by: C19b                                                    [C19b]
d_noreason      94/96   killed by: C19a C19b                                               [C19a C19b]
d_blank         88/96   killed by: C1 C11 C12 C14 C26                                      [C14]
d_domnohold     74/96   killed by: C1 C10 C11 C12 C17b C18 C18b C19a C2 C22 C27 C2b C2c C3 C6 C7 C8 C9 W1 [C2c]
d_domnopend     74/96   killed by: C1 C10 C11 C12 C17b C18 C18b C19a C2 C22 C27 C2b C2d C3 C6 C7 C8 C9 W1 [C2d]
d_dupplus1      63/96   killed by: C11 C14 C15 C16 C19a C19b C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C25l C25m C25n C25o C25p C25q C25r C26 C26b C28 C5 C6 C9 W2 W4 W5 [C5 C9]
d_nonote        77/96   killed by: C1 C10 C12 C17b C18 C18b C19a C2 C22 C2b C3 C6 C7 C8 C9 W1 [C1]
d_nonote2       87/96   killed by: C15 C16 C19a C25e C25f C25o C3 C6 C9                    [C15 C16]
d_lastwins      95/96   killed by: C17b                                                    [C17b]
d_ledger1       95/96   killed by: C21h                                                    [C21h]
d_nomd5         95/96   killed by: C18                                                     [C18]
d_pinoverride   88/96   killed by: C11 C12 C12s C17b C18                                   [C18]
d_crlfpin       95/96   killed by: C18b                                                    [C18b]
d_noreconf      84/96   killed by: C11 C14 C19a C19b C20 C26 C26b C28 C3 C4 C5 C6          [C20]
d_notenone      96/96   escapes (as recorded)                                              [UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note]
r_nolegend      95/96   killed by: R4                                                      [R4]
r_tipclause     91/96   killed by: R1 R1c R1e R1f R1g                                      [R1 R1c]
r_tiptail       92/96   killed by: R1 R1e R1f R1g                                          [R1]
r_ok            85/96   killed by: R1 R1b R1d R1e R1f R1g R1h R1n R2 R3                    [R1]
r_pend          85/96   killed by: R1 R1b R1d R1e R1f R1g R1h R1n R2 R3                    [R1]
r_noescape      94/96   killed by: R1b R3                                                  [R1b]
r_wsblank       93/96   killed by: R1d R1n R3                                              [R1d]
r_strip         94/96   killed by: R2 R2b                                                  [R2]
w_envkeep       94/96   killed by: W4 W5                                                   [W4 W5]
w_ledgerkeep    95/96   killed by: W5                                                      [W5]
w_collapse      93/96   killed by: W3 W7 W8                                                [W3]
w_rc7           92/96   killed by: W2 W4 W5 W7                                             [W2]
w_msg           93/96   killed by: W2 W4 W5                                                [W2]
w_subshell      93/96   killed by: W2 W4 W5                                                [W2]
d_date10        94/96   killed by: C25a C25b                                               [C25a C25b]
d_dstrip        94/96   killed by: C25c C25n                                               [C25c]
d_dfold         77/96   killed by: C1 C10 C12 C17b C18 C18b C19a C2 C22 C2b C3 C6 C7 C8 C9 W1 [C1]
d_dfold2        92/96   killed by: C19a C25d C3 C6                                         [C25d]
d_notestrip     77/96   killed by: C1 C10 C12 C17b C18 C18b C19a C2 C22 C2b C3 C6 C7 C8 C9 W1 [C1]
d_notefold      77/96   killed by: C1 C10 C12 C17b C18 C18b C19a C2 C22 C2b C3 C6 C7 C8 C9 W1 [C1]
d_seatstrip     94/96   killed by: C25g C25p                                               [C25g]
d_seatfold      95/96   killed by: C25h                                                    [C25h]
d_phasestrip    94/96   killed by: C25i C25q                                               [C25i]
d_phasefold     95/96   killed by: C25j                                                    [C25j]
d_shaperows     95/96   killed by: C21d                                                    [C21d]
d_shapeents     95/96   killed by: C21f                                                    [C21f]
d_shapeentry    95/96   killed by: C21e                                                    [C21e]
d_noshape       91/96   killed by: C21d C21e C21f C21i                                     [C21d C21e C21f]
d_basedict      95/96   killed by: C21g                                                    [C21g]
r_norecord      95/96   killed by: R1e                                                     [R1e]
r_okonly        95/96   killed by: R1g                                                     [R1g]
r_stripok       94/96   killed by: R2 R2b                                                  [R2]
r_refusallast   95/96   killed by: R1f                                                     [R1f]
w_nochecker     95/96   killed by: W6                                                      [W6]
d_unread0       95/96   killed by: C23                                                     [C23]
d_summary       92/96   killed by: C11 C12                                                 [C11]
r_tipokonly     95/96   killed by: R1g                                                     [R1g]
r_tipnonblank   95/96   killed by: R1g                                                     [R1g]
r_clsstrip      92/96   killed by: R1g R1h R3                                              [R1h]
d_isheld        75/96   killed by: C1 C10 C11 C12 C17b C18 C18b C19a C2 C22 C24 C2b C3 C6 C7 C8 C9 W1 [C24]
d_nulld         95/96   killed by: C26                                                     [C26]
d_nohint        95/96   killed by: C11                                                     [C11]
d_domzxq        95/96   killed by: C27                                                     [C27]
r_dclasszxq     95/96   killed by: C27                                                     [C27]
d_cut2days      95/96   killed by: C12                                                     [C12]
d_baselen       91/96   killed by: C1 C12                                                  [C1]
w_nosed         95/96   killed by: W2                                                      [W2]
r_wsspace       94/96   killed by: R1d R3                                                  [R1d]
d_domredef      95/96   killed by: C27                                                     [C27]
r_dclassredef   95/96   killed by: C27                                                     [C27]
d_dompad        95/96   killed by: C28                                                     [C28]
d_rowstrip      94/96   killed by: C25l C25r                                               [C25l C25r]
d_rowrstrip     95/96   killed by: C25l                                                    [C25l]
d_rowlstrip     95/96   killed by: C25r                                                    [C25r]
d_datelstrip    95/96   killed by: C25m                                                    [C25m]
d_dlstrip       95/96   killed by: C25n                                                    [C25n]
d_notelstrip    95/96   killed by: C25o                                                    [C25o]
d_seatlstrip    95/96   killed by: C25p                                                    [C25p]
d_phaselstrip   95/96   killed by: C25q                                                    [C25q]
d_cutreason     95/96   killed by: C3                                                      [C3]
d_ceilreason    93/96   killed by: C19a C6 C9                                              [C6 C9]
d_rowphaseswap  92/96   killed by: C19a C3 C6 C9                                           [C9]
d_basewithin    93/96   killed by: C12                                                     [C12]
d_isodollar     95/96   killed by: C12s                                                    [C12s]
d_len7ge        95/96   killed by: C17c                                                    [C17c]
d_boolcount     95/96   killed by: C17d                                                    [C17d]
d_negcount      95/96   killed by: C17e                                                    [C17e]
d_zerocount     95/96   killed by: C17f                                                    [C17f]
d_floatcount    95/96   killed by: C17g                                                    [C17g]
d_str1          95/96   killed by: C17h                                                    [C17h]
d_str5          95/96   killed by: C17i                                                    [C17i]
d_isosearch     96/96   escapes (as recorded)                                              [UNPINNED: equivalent -- the ISO pattern is anchored with ^, so search and match agree on every string]
d_nostr         95/96   killed by: C26b                                                    [C26b]
d_hintundated   95/96   killed by: C6                                                      [C6]
d_datenone      95/96   killed by: C6                                                      [C6]
d_cutoffmsg     90/96   killed by: C1 C11 C12                                              [C1 C11 C12]
d_rowsabsent    94/96   killed by: C21i                                                    [C21i]
r_sumstrip      95/96   killed by: R2b                                                     [R2b]
r_tipnorecord   95/96   killed by: R1e                                                     [R1e]
r_tipnotnull    95/96   killed by: R1g                                                     [R1g]
r_nullpend      94/96   killed by: R1g R1n                                                 [R1n R1g]
r_striplabel    94/96   killed by: R2 R2b                                                  [R2]
r_wsset         94/96   killed by: R1d R3                                                  [R1d]
r_css0          95/96   killed by: R5                                                      [R5]
r_cssoutline    95/96   killed by: R5                                                      [R5]
w_elif2         94/96   killed by: W7 W8                                                   [W7 W8]
w_no2to1        95/96   killed by: W7                                                      [W7]
KILL TABLE: 105/105 as recorded
DASHOKCLASS_MUTANTS_DONE
```

```python
    #  v5 -- the v4 pass's survivors (Fable 5.1 measured 21, GPT-6 Astra 10 more in memory, Grok 4.7 traced 6) and each pin's dual edge
    ("d_domredef", "checker", [('CUTOFF = "2026-10-17"               # inclusive',
                                'DOMAIN = ("✓", "✕", "⏸", "…", "ZXQ")\nCUTOFF = "2026-10-17"               # inclusive')], ["C27"]),
    ("r_dclassredef", "render", [('D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}',
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}\n'
                                  'D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend", "ZXQ": "ok"}')], ["C27"]),
    ("d_dompad", "checker", [('x["d"] in DOMAIN or not st.is_answer(x):', 'str(x["d"]).strip() in DOMAIN or not st.is_answer(x):')],
     ["C28"]),
    ("d_rowstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).strip(),')], ["C25l", "C25r"]),
    ("d_rowrstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).rstrip(),')], ["C25l"]),
    ("d_rowlstrip", "checker", [('out.append((str(r.get("id")),', 'out.append((str(r.get("id")).lstrip(),')], ["C25r"]),
    ("d_datelstrip", "checker", [('return v if isinstance(v, str) else', 'return v.lstrip() if isinstance(v, str) else')], ["C25m"]),
    ("d_dlstrip", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), str(x["d"]).lstrip(),')], ["C25n"]),
    ("d_notelstrip", "checker", [(SHA, SHA.replace('str(x.get("note") or "")', 'str(x.get("note") or "").lstrip()'))], ["C25o"]),
    ("d_seatlstrip", "checker", [('str(x.get("seat") or "")', 'str(x.get("seat") or "").lstrip()')], ["C25p"]),
    ("d_phaselstrip", "checker", [('str(x.get("phase") or "")', 'str(x.get("phase") or "").lstrip()')], ["C25q"]),
    ("d_cutreason", "checker", [('bad.append((t, "dated on or after the cutoff %s" % CUTOFF))', 'bad.append((t, "refused"))')], ["C3"]),
    ("d_ceilreason", "checker", [('why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"',
                                  'why = ""')], ["C6", "C9"]),
    ("d_rowphaseswap", "checker", [('% (row, phase, seat, date or "(none)", d, ns, why))',
                                    '% (phase, row, seat, date or "(none)", d, ns, why))')], ["C9"]),
    ("d_basewithin", "checker", [("% (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))",
                                  "% (len(cur), len(cur) - len(bad), len(cur) - len(bad), CUTOFF))")], ["C12"]),
    ("d_isodollar", "checker", [('ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}")', 'ISO = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")')], ["C12s"]),
    ("d_len7ge", "checker", [("len(k) == 7", "len(k) >= 7")], ["C17c"]),
    ("d_boolcount", "checker", [("type(k[6]) is int", "isinstance(k[6], int)")], ["C17d"]),
    ("d_negcount", "checker", [("and k[6] > 0):", "and k[6] != 0):")], ["C17e"]),
    ("d_zerocount", "checker", [("and k[6] > 0):", "and k[6] >= 0):")], ["C17f"]),
    ("d_floatcount", "checker", [("type(k[6]) is int", "type(k[6]) in (int, float)")], ["C17g"]),
    ("d_str1", "checker", [("for v in k[:6])", "for v in k[1:6])")], ["C17h"]),
    ("d_str5", "checker", [("for v in k[:6])", "for v in k[:5])")], ["C17i"]),
    ("d_isosearch", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if ISO.search(t[3]) and t[3][:10] >= CUTOFF:")],
     "UNPINNED: equivalent -- the ISO pattern is anchored with ^, so search and match agree on every string"),
    ("d_nostr", "checker", [('date_str(x), str(x["d"]),', 'date_str(x), x["d"],')], ["C26b"]),
    ("d_hintundated", "checker", [("if t[3] and not ISO.match(t[3]):", "if not ISO.match(t[3]):")], ["C6"]),
    ("d_datenone", "checker", [('date or "(none)", d, ns, why))', 'date, d, ns, why))')], ["C6"]),
    ("d_cutoffmsg", "checker", [('cutoff %s inclusive"', 'cutoff %s"')], ["C1", "C11", "C12"]),
    ("d_rowsabsent", "checker", [('rows = ledger.get("rows")', 'rows = ledger.get("rows", [])')], ["C21i"]),
    ("r_sumstrip", "render", [("n[d if d in D_CLASS else LEGACY] += 1",
                               "n[str(d).strip() if str(d).strip() in D_CLASS else LEGACY] += 1")], ["R2b"]),
    ("r_tipnorecord", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and all(st.is_answer(x) for x in mine):\n")], ["R1e"]),
    ("r_tipnotnull", "render", [("    if cls == LEGACY:\n", "    if cls == LEGACY and d is not None:\n")], ["R1g"]),
    ("r_nullpend", "render", [('    d = ent.get("d", "…")', '    d = ent.get("d") if ent.get("d") is not None else "…"')], ["R1n", "R1g"]),
    ("r_striplabel", "render", [("{n[LEGACY]} legacy · ", "{n[LEGACY]} approved · ")], ["R2"]),
    ("r_wsset", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if str(d).strip(" \\t") else "?"}')], ["R1d"]),
    ("r_css0", "render", [("font-size:11px; }}", "font-size:0; }}")], ["R5"]),
    ("r_cssoutline", "render", [("td.c.legacy {{ outline:1px dashed var(--line); outline-offset:-3px; }}", "td.c.legacy {{ outline:0; }}")],
     ["R5"]),
    ("w_elif2", "precommit", [('\telse\n\t\tbad "check_entry_domain.py could not run',
                               '\telif [ $_cedrc -eq 2 ]; then\n\t\tbad "check_entry_domain.py could not run')], ["W7", "W8"]),
    ("w_no2to1", "precommit", [('python "$CED" 2>&1); _cedrc=$?', 'python "$CED"); _cedrc=$?')], ["W7"]),
]
```

### 4d. `DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt` (`dashmissingd_census.py` on HEAD's ledger; v5 adds the NOT-FIRED screen)

```
entries: 5177 | answers with no d: 1561 (by month: 2026-08 174, 2026-09 1244, 2026-10 143; the latest dated 2026-10-16) | of those, the note names a non-answer: 300
displayed answer cells: 2953 | whose latest answer has no d (rendered as the seat-failure glyph): 814 | of those, the note names no non-answer (an answer shown as a failure, by the keyword screen): 682
NOT-FIRED screen /not[ -]fired|roster/i over every entry's note: 222 entries | untokened (ANSWERS by stage_tokens.is_answer, so section H counts each as a recorded seat): 200 | of those with no d (each renders the seat-failure glyph): 87
DASHMISSINGD_CENSUS_DONE
```

## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A.

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2 (K1-K28): is my disposition right, AND is the fix right --
   does the named row go red under the named mutant for the reason named?  Be harder on the ones you raised.
2. **The enumeration.**  For each decision in the CONTRACT, does a row now stand on BOTH edges?  Is any decision of the staged
   checker, the renderer change or the Q2 block missing?  Name every decision you checked.
3. **The kill table and the floor.**  Is any mutant killed for a reason OTHER than the one its line names?  Is there a
   one-edit mutant of the staged v5 files, NOT in the table, that passes all 96 controls and breaks a ruled property or a line
   of the CONTRACT?  If you find none, name the shapes you swept (a zero needs its denominator).
4. **The records (section 5).**  Is that text true of what ships?  Name any sentence that is false.
5. **Which of my 28 dispositions is wrong?**  Name the count you checked.

Label each claim MEASURED (you ran it), READ (you opened the file) or REASONED.  Write nothing to any project tree.
