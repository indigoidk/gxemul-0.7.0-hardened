# V4 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v4 = the CLASS CLOSURE

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v4 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v4/` (mirroring `tools/`); the controls are `run_controls_v4.py` and
`run_mutants_v4.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming the staged files; the v3-pass
answers are in `v3pass/`.  Everything a packet-fed seat needs is inlined below.

**Why v4 is a class closure.**  Pass 2, the adjudication pass and the v3 pass each found one-edit mutants that passed every
control of the version before -- the same class: a behaviour of the checker, the renderer change or the Q2 block that no
row pinned.  By the repair-chain rule the next repair owes the class: v4 enumerates every decision those three make, pins
each at its edges, and writes the rest into a CONTRACT in `run_controls_v4.py`'s docstring (inlined in section 4a).
**This pass's job is to VERIFY THE ENUMERATION** -- is any decision missing from the CONTRACT, or listed as pinned while a
one-edit mutant of it still passes all 72 controls?  The chain closes on the first pass whose zero floor breaches survive
adjudication; if you find none, name the decisions you checked.  Check the premises in 2b; do not ratify them.

**Liveness:** open your answer with the token `ASTRA_DASHOKV4_20261017` on its own line, then your verdict line.

## 1. The v3-pass verdicts -- all four SHIP WITH CHANGES (3)

GPT-6 Astra (`v3pass/codex_dashokv3.txt`), GLM 5.3 (`v3pass/glm_dashokv3.txt`), Fable 5.1 (`v3pass/fable5_dashokv3.md`;
agent_models.py: clean claude-fable-5-1, measuring in a mirror), Grok 4.7 (`v3pass/grok_dashokv3.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| J1 | Astra | five one-edit survivors of the 46: the date's `v` -> `v[:10]`; the answer cell's `record:` line deleted (32 displayed cells lose it); `if cls == LEGACY` -> `if d == "OK"` (305 cells lose the class line); the strip folding the canonical glyphs into ✓; Q2's missing-checker `bad` -> `good` | **PINNED**: C25a/b (a frozen entry's date suffixed / given a trailing space), R1e (an answer with a record beside it keeps the record's note), R1g (every simple legacy cell's WHOLE tooltip), R2 (each strip number is the ledger's own count), W6 (the checker absent: BAD "MISSING") -- mutants `d_date10`, `r_norecord`, `r_okonly`, `r_stripok`, `w_nochecker` |
| J2 | Astra | `{"rows": {}}` and a string entry walk as EMPTY and pass (rc 0): the rc-2 promise is false in general | **FIXED in the checker**: `ledger_shape()` type-checks every container level (ledger object, rows list, row objects, entries lists, entry objects) before anything is walked, and the baseline must be a list; C21d-g.  The walk's except-arm stays for the one input that still reaches it -- a non-string note raises inside `stage_tokens.is_answer` (C21h) |
| J3 | Astra | C2c/C2d were red without their own entries (the shipped ledger carries 21 ⏸ and 35 … answers) | **FIXED**: each runs on a ledger holding ONLY its entry |
| J4 | Astra | records: "on the landed files"; "every explicit d renders as one class" (holds and records keep their rendering); "a new answer fails" (an admitted replacement can be new) | **CORRECTED** (sections 5a-5d) |
| J5 | GLM | the checker-absent and ledger-unreadable edges are unpinned | **PINNED**: W6, C23 (a ledger that is not JSON: rc 2) -- `w_nochecker`, `d_unread0` |
| J6 | GLM | the summary line is pinned only on a clean ledger, where "passes" and "entries" agree | **PINNED**: C11 asserts the dirty summary ("0 within the frozen ceiling (baseline 0)") -- `d_summary` |
| J7 | GLM | RULINGS_C's "5,150 at HEAD" and Q2's header "or is a frozen legacy entry" are stale | **CORRECTED** (5c; Q2's header now "or is within the frozen legacy ceiling") |
| J8 | Fable | `if cls == LEGACY and d == "OK"` and `... and str(d).strip()` pass all 46: R1 compared ONE cell's tooltip | **PINNED**: R1g compares the WHOLE tooltip of every simple legacy cell -- `OK`, blank, `N/A`, `<b>&`, a space, a tab, a padded ` ✓` -- `r_tipokonly`, `r_tipnonblank` |
| J9 | Fable | an explicit `"d": null`; a padded glyph `" ✓"`; condition 2's NOTSEAT half pinned only incidentally; the hint line asserted by nothing | **PINNED**: C26 (a new answer with d null: rc 1), R1h (the padded glyph renders legacy), C24 (a NOTSEAT record after the cutoff: rc 0), C11 asserts the hint -- `d_nulld`, `r_clsstrip`, `d_isheld`, `d_nohint` |
| J10 | Fable | records: the checker docstring quotes a clause RULINGS_C upheld but did not restate; grok's adjudication entry credited it with the CRLF measurement; dashmissingd's question omits section H | **CORRECTED** (the docstring cites packet_C_records.md F2 (d) as upheld by RULINGS_C F2; the entry says the main loop measured it; the filing names the H collision with Fable's measured counts) |
| J11 | Grok | the glyph SET is open at the top: a fifth member of DOMAIN, or a fifth key of D_CLASS, passes all 46 | **PINNED**: C27 reads both files' literals and requires exactly ✓ ✕ ⏸ … -- `d_domzxq`, `r_dclasszxq` |
| J12 | Grok | the cutoff was pinned on two days (`in ("2026-10-17", "2026-10-18")` passes) | **PINNED**: C12 adds a FAR-after frozen identity (2027-01-01) -- `d_cut2days` |
| J13 | Grok | the summary's baseline number and Q2's named-entry lines are never read | **PINNED**: C1 asserts "(baseline 1356)"; W2 asserts the OFF-DOMAIN ANSWER lines reach the committer -- `d_baselen`, `w_nosed` |
| J14 | Grok | a tab-only `d` would render invisible under `.strip(" ")` | **PINNED**: R1d adds a tab -- `r_wsspace` |
| J15 | main loop | the first v4 table: `d_dfold`, `d_notestrip`, `d_notefold` were killed by C1, not by C25d-f | **RE-NAMED**: they are ONE-SIDED here -- the baseline holds raw values and only the note's sha -- so the whole frozen population misses and C1 kills them; the COHERENT fold of d is the two-edit design mutant `d_dfold2`, killed by exactly C25d; no coherent note fold or strip can exist |
| J16 | main loop | the seat entries | answered seats carry `d` ✓ (their changes applied, entry by entry); seat failures and seats not fired carry none |

### The one DISAGREEMENT, both sides

* **GPT-6 Astra (v3 pass):** *"all five proposed NOT FIRED entries classify as answers under `stage_tokens.is_answer`.  Their
  prose and missing `d` do not make them non-answer records.  Adding the entry-scoped `NOTSEAT` token makes all five classify
  correctly."*
* **Mine, on Fable 5.1's measurement:** they stay plain entries.  `check_stage_panels.py` (precommit section H) tallies a
  stage's seats by `is_answer` -- an untokened entry counts as a recorded seat, a NOTSEAT one is skipped -- and the owner's
  standing directive records a seat not fired as DELIBERATELY NOT FIRED so the stage still shows nine recorded seats.
  Tokening them NOTSEAT turns H red at 4/9 on this landing.  Fable measured 158 such entries at HEAD (127 untokened); the
  collision is now part of `dashmissingd`'s rule question rather than settled here.  **Rule on it.**

## 2b. Premises to CHECK (stated as questions)

* **The CONTRACT's completeness** (section 4a).  Read the staged checker, the renderer's changed lines and the Q2 block for
  every `if`, comparison, literal, container walk, exit and printed line a caller reads.  Is any decision missing, or listed
  as pinned by a row that cannot see its mutant?
* **The NOTSEAT disagreement** above.
* **J2's shape check.**  Is there a misshapen ledger or baseline the v4 checker still walks as empty and passes?

## 3. The repair, staged v3 -> v4 (51 changed lines; the checker's shape check is the only code change)

```diff
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v3/tools/pipeline/check_entry_domain.py
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v4/tools/pipeline/check_entry_domain.py
@@ -7,9 +7,9 @@
 `d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
 2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
 them as one residue class, "legacy -- verdict unclassified", and this check keeps answers with NEW content from appearing.
-Ruled by Fable
-5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old
-entries is withdrawn -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.
+Ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md F2, which upheld
+packet_C_records.md's F2): every mechanical sweep of the old entries is withdrawn, and -- that packet's clause (d), upheld
+there without restatement -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.
 
 ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt):
   1. a MISSING `d` passes -- it renders as … (an explicit blank does NOT: it is an off-domain value);
@@ -19,9 +19,10 @@
 
 GRANDFATHERING IS A CEILING OVER SELECTED CONTENT -- NOT A DATE, AND NOT AN ENTRY IDENTITY.  An off-domain answer passes
 only while the ledger holds no more answers with its (row, phase, seat, date, `d`, sha1 of its NOTE) than
-`entry_domain_baseline.json` froze when this check landed, and only if it is not dated on or after CUTOFF.  So a new answer
-fails, a back-dated or undated one fails, a copy fails, and an old one EDITED in any of those six fields fails: editing such
-an entry means classifying it -- a glyph, or no `d` at all (it renders as …), or a non-answer record token if it is not an
+`entry_domain_baseline.json` froze when this check landed, and only if it is not dated on or after CUTOFF.  So UNMATCHED
+selected content fails and so does an EXCESS occurrence -- a new answer, a back-dated or undated one, a copy, an old one
+EDITED in any of those six fields -- while an admitted replacement, identical in all six, can be new (GPT-6 Astra, v3 pass).
+Editing such an entry means classifying it -- a glyph, or no `d` at all (it renders as …), or a non-answer record token if it is not an
 answer.  For a NOTE-only correction that is this check's toll, not the ruling's: the ruling withdraws every mechanical sweep
 and classifies an entry when a reader rewrites it, and says nothing of note edits (Grok 4.7, adjudication pass).  (Pass 2,
 2026-10-16: a per-(row, phase, seat, date, d)
@@ -53,7 +54,8 @@
 
 Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
 Exit: 0 clean; 1 an off-domain answer beyond the frozen ceiling (each named); 2 apparatus failure (baseline or ledger
-unreadable or misshapen, or the baseline's md5 is not the pinned one)."""
+unreadable or misshapen -- every container level is type-checked before it is walked -- or the baseline's md5 is not the
+pinned one)."""
 import collections, hashlib, io, json, os, re, sys
 
 HERE = os.path.dirname(os.path.abspath(__file__))
@@ -90,6 +92,26 @@
     return out
 
 
+def ledger_shape(ledger):
+    #  the first structural problem, or None.  A container of the wrong type WALKS AS EMPTY and passes -- {"rows": {}} and a
+    #  string entry were rc 0 (GPT-6 Astra, v3 pass) -- so every level is checked before anything is walked
+    if not isinstance(ledger, dict):
+        return "the ledger is not an object"
+    rows = ledger.get("rows")
+    if not isinstance(rows, list):
+        return "rows is not a list"
+    for i, r in enumerate(rows):
+        if not isinstance(r, dict):
+            return "row %d is not an object" % i
+        ents = r.get("entries", [])
+        if not isinstance(ents, list):
+            return "row %r: entries is not a list" % (r.get("id"),)
+        for x in ents:
+            if not isinstance(x, dict):
+                return "row %r: an entry is not an object" % (r.get("id"),)
+    return None
+
+
 def main():
     #  precommit runs this with stdout on a PIPE, which Windows python opens as cp1252: a glyph or a non-ASCII `d` in the
     #  failure lines raised UnicodeEncodeError and buried the instruction under a traceback (Fable 5.1, pass 2, measured)
@@ -106,13 +128,19 @@
             print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
                   "in the same commit, with its reason" % (BASELINE, md, BASELINE_MD5)); return 2
         base = collections.Counter()
-        for k in json.loads(raw.decode("utf-8")):
+        rows_b = json.loads(raw.decode("utf-8"))
+        if not isinstance(rows_b, list):
+            raise ValueError("the baseline is not a list")
+        for k in rows_b:
             if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
                     and k[6] > 0):
                 raise ValueError("baseline row %r is not [row, phase, seat, date, d, note_sha, count]" % (k,))
             base[tuple(k[:6])] += k[6]
     except Exception as ex:
         print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
+    shape = ledger_shape(ledger)
+    if shape:
+        print("APPARATUS FAIL: ledger misshapen: %s (%s)" % (LEDGER, shape)); return 2
     try:
         cur = off_domain_answers(ledger)
     except Exception as ex:      # {"rows": null}, a row that is not an object ... (GPT-6 Astra, adjudication pass)
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v3/tools/pipeline/gen_dashboard.py
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v4/tools/pipeline/gen_dashboard.py
@@ -78,7 +78,8 @@
 #  The fallback was `pend`, so 1,397 entries whose `d` is "OK", "N/A", a date, "y", "HELD", blank ... -- 439 of them "OK",
 #  365 displayed cells -- all read as "no answer / seat failure".  Mapping "OK" to `ok` was REJECTED (it canonises one
 #  off-domain spelling as approval); every mechanical sweep of the entries was withdrawn.  So an explicit `d` the map does
-#  not know renders as ONE residue class, LEGACY, keeping its text, with the reason first in its tooltip (after a refused
+#  not know, on the ANSWER a cell shows, renders as ONE residue class, LEGACY (a live hold and a non-answer record keep their
+#  own rendering whatever their `d` -- GPT-6 Astra, v3 pass), keeping its text, with the reason first in its tooltip (after a refused
 #  exemption's line, if any -- Fable 5.1, adjudication pass); a MISSING `d` is
 #  still `…`, an explicit blank shows `?`.  The class says only that the `d` is unclassified -- three legacy cells (`WALL`)
 #  record real seat failures in their notes, so the tooltip sends the reader to the note rather than denying either reading
--- /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v3/tools/precommit_check.sh
+++ /c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v4/tools/precommit_check.sh
@@ -501,11 +501,11 @@
 #  baseline holds.  Not a date (a date-only cutoff cannot stop a back-dated or undated addition), not a count without the
 #  note (a converted entry's allowance could be refilled; pass 2), and NOT an entry identity: a byte-identical revert of a
 #  normalised entry passes, and the dashboard's legacy count can still rise through exempt records and re-exposed older
-#  answers (adjudication pass, GPT-6 Astra).  HARD.  It fails on a NEW off-domain answer and on an OLD one edited in any
-#  of those fields: editing such an entry means classifying it -- a glyph, no `d`, or a non-answer record token (Fable
+#  answers (adjudication pass, GPT-6 Astra).  HARD.  It fails on UNMATCHED content and on an EXCESS occurrence -- a NEW
+#  off-domain answer, or an OLD one edited in any of those fields (an admitted replacement can be new; v3 pass): editing such an entry means classifying it -- a glyph, no `d`, or a non-answer record token (Fable
 #  5.1); for a note-only correction that toll is this check's, not the ruling's (Grok 4.7).  It reds (rc 2) when the ledger
 #  or the baseline is unreadable or misshapen or the baseline's md5 is not the pinned one, never silently green.
-say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is a frozen legacy entry"
+say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is within the frozen legacy ceiling"
 CED=$_HERE/pipeline/check_entry_domain.py
 if [ ! -f "$CED" ]; then
 	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
```

## 4. The controls and their receipts

### 4a. the CONTRACT and the 72 controls -- the docstring of `run_controls_v4.py`

```
"""Controls for `dashokclass` (2026-10-17, v4 after the v3 pass -- the CLASS CLOSURE): gen_dashboard.py's LEGACY class,
check_entry_domain.py (a ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on
temp copies and fixture ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT override the three files under test (run_mutants_v3.py and the staged runs use them); the defaults
are the tree's.

  THE CONTRACT (v4) -- the v3 pass (GPT-6 Astra) found five more one-edit survivors of the 46 v3 controls, the same class as the
  adjudication pass's, so v4 closes the class: each decision below is pinned at its edges, or DISCLOSED with its reason.
    checker  ledger shape (object, rows list, row objects, entries lists, entry objects)   C21a-f      (and C23: not JSON)
             baseline shape (a list of [6 strings, positive int])                         C13, C17, C21g; C17b sums a split key
             md5 pin on the default path, CRLF folded; overrides skip it                   C18, C18b; C11, C12, C17 (override)
             the selection: explicit d, outside the four, an ANSWER                        C7 (no d), C14 (blank), C2/C2b/C2c/C2d
                                                                                          (each glyph, C2c/C2d in a ledger holding
                                                                                          only their entry), C8 (hold), C24 (record)
             the key -- each of row, phase, seat, date, d, note -- byte for byte          C25a-k: a suffix, a trailing space, a case
                                                                                          change, a row move; C15/C16 (the note)
             the ceiling: a copy fails, a converted entry's allowance cannot be refilled  C9, C10, C15; d_nonote2 (design mutant)
             the cutoff: inclusive, ISO-shaped dates only                                  C3, C4, C12 (isolated), C19a/b
             output: cp1252-safe, the reason named, every refusal named                    C20, C19, C11
    renderer the class: explicit d outside the four -> legacy, on the answer a cell shows  R1 (per seat), R3
             the class line opens EVERY legacy cell's tooltip, exactly                    R1 (whole tooltip, OK), R1g (every legacy
                                                                                          d), R1c (no denial anywhere)
             a refused exemption's line comes first; a record's note is kept              R1f, R1e
             the glyph: escaped; `?` for a blank or whitespace d                          R1b, R1d
             the strip: each of the five numbers is the ledger's own count                R2
             the legend line                                                              R4
    Q2       the branches: rc 0 GOOD, rc 1 BAD with the refusal, else BAD "could not run"  W1, W2, W3 (first-line words)
             the checker absent -> BAD                                                     W6
             exported GXDOMAIN_BASELINE / GXLEDGER stripped                                W4, W5
    DISCLOSED: a sha1-16 collision of two notes (2^64 work); `k[6] > 0` -> `>= 0` (a zero count adds nothing: equivalent);
    case-folding or whitespace-stripping INSIDE a field rather than at its ends (C25 edits the ends); the production good/bad
    reporters and final exit (the W rows use counting stand-ins; correct by inspection).  A fold of d or a fold or strip of the
    NOTE is one-sided on this ledger -- the baseline holds raw values and only the note's sha -- so it dies on C1 (measured,
    the first v4 table); the coherent fold of d is the two-edit design mutant d_dfold2, killed by C25d.

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's and the adjudication pass's findings):
    C1   shipped ledger, shipped baseline (the md5 pin is checked on the default path)             -> 0, all within the ceiling
    C2   an answer ON the cutoff with a valid glyph (positive)                                      -> 0
    C2b  an answer AFTER the cutoff with a valid glyph (positive)                                   -> 0
    C2c  / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
    C3   an answer ON the cutoff with "OK" (inclusive)                                              -> 1
    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
    C6   an UNDATED answer with "N/A"                                                               -> 1
    C7   an answer after the cutoff with NO `d`                                                     -> 0
    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
    C9   an identical copy of a frozen entry                                                        -> 1
    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
    C11  the baseline emptied (override): every one of the shipped off-domain answers is named      -> 1
    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after it   -> 0 / 1 / 1
    C13  an unreadable baseline (override)                                                          -> 2
    C14  a new answer with an explicit BLANK d (blank is off-domain; only a MISSING d is …)         -> 1
    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat,
         date, d) with another note -- the per-tuple count let this through on pass 2                -> 1
    C16  a frozen entry's NOTE edited, its d left off-domain (editing means normalising)            -> 1
    C17  a misshapen baseline (override; counts as strings)                                         -> 2
    C17b a key SPLIT across two baseline rows (override) must sum -- the loader once kept the last  -> 0
    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    C18b the same baseline with CRLF line endings (a fresh clone under core.autocrlf=true) passes the pin -> 0
    C19  malformed dates on new answers: "10/18/2026" and a number -- rc 1, never a traceback, and the
         output NAMES the date as not ISO                                                         -> 1 / 1
    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback   -> 1
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
         that are an object -- rc 2, no traceback; C21g a baseline that is an object (override); C21h a note that is
         a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)            -> 2 each
    C23  a ledger that is not JSON                                                              -> 2
    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK" (condition 2's other half)  -> 0
    C26  a new answer with an explicit "d": null (present, off-domain -- not "missing")         -> 1
    C25  a frozen entry with ONE key field edited by its least visible change -- date suffixed / trailing space,
         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
         the entry moved to another row                                                         -> 1 each
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell (the record cell's glyph included), and the
         legacy cell's tooltip EXACTLY (the whole string, not a prefix)
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` (" ") shows `?`
    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓"), the date,
         the note
    R1h  a padded glyph " ✓" renders legacy, not ok
    C27  the glyph SET, read from both files' literals: DOMAIN and D_CLASS's keys are exactly ✓ ✕ ⏸ …
    R1e  an answer cell with a non-answer record beside it keeps the record's note in its tooltip
    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; EACH of the strip's five numbers is the ledger's own
         count of that class (the v3 form checked the total and the legacy number, so folding every glyph into ✓ passed)
    R4   the legend carries the legacy line EXACTLY
    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash
         is not a kill
  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures -- stand-ins for the
  production good/bad and its final exit, which are correct by inspection and not executed here; each first line must also
  carry its BRANCH's own words):
    W1   the shipped ledger                    -> GOOD, failures 0
    W2   a new off-domain answer               -> BAD "beyond the frozen legacy ceiling", failures >= 1
    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
"""
```

### 4b. `RECEIPT_v4_on_staged_v4.txt`, whole

```
# dashokclass controls (v4) -- checker 79e2497e | renderer 516df040 | precommit ee874ba0 | baseline 06a3ffc6
C1   shipped ledger, shipped baseline, md5 pin live                               ok  rc 0: entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
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
C24  a non-answer RECORD (NOTSEAT) after the cutoff, d OK                         ok  rc 0 (want 0)
C26  a new answer with an explicit null d                                         ok  rc 1 (want 1)
C2c  AFTER the cutoff, d ⏸, in a ledger holding only it (positive)                ok  rc 0
C2d  AFTER the cutoff, d …, in a ledger holding only it (positive)                ok  rc 0
C9   an identical copy of a frozen entry (alphactxfail assess codex 2026-09-08 'y') ok  rc 1
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
C11  baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint printed ok  rc 1, 1356 of 1356 named; summary ok; hint ok
C12  cutoff isolated: a FROZEN identity dated 2026-10-16 (before)                 ok  rc 0 (want 0)
C12  cutoff isolated: a FROZEN identity dated 2026-10-17 (on)                     ok  rc 1 (want 1)
C12  cutoff isolated: a FROZEN identity dated 2026-10-18 (after)                  ok  rc 1 (want 1)
C12  cutoff isolated: a FROZEN identity dated 2027-01-01 (far)                    ok  rc 1 (want 1)
C13  an unreadable baseline                                                       ok  rc 2
C27  the checker's DOMAIN and the renderer's D_CLASS keys are exactly ✓ ✕ ⏸ …     ok  DOMAIN ('✓', '✕', '⏸', '…') | D_CLASS keys ['…', '⏸', '✓', '✕']
C17  a misshapen baseline (counts as strings)                                     ok  rc 2
C17b a key split across two baseline rows sums (alphaswpctxreg review grok 2026-09-08 'y' x2) ok  rc 0
C18  md5 pin: one baseline line changed -> 2, unchanged -> 0                      ok  changed rc 2, unchanged rc 0
C18b md5 pin: the baseline checked out with CRLF line endings -> 0                ok  rc 0
C21a a misshapen ledger: {"rows": null}                                           ok  rc 2
C21b a misshapen ledger: a row that is not an object                              ok  rc 2
C21c a misshapen ledger: a list, not an object                                    ok  rc 2
C21d a misshapen ledger: {"rows": {}}                                             ok  rc 2
C21e a misshapen ledger: an entry that is a string                                ok  rc 2
C21f a misshapen ledger: entries that are an object                               ok  rc 2
C21g a misshapen baseline: an object, not a list (override)                       ok  rc 2
C21h an entry whose note is a number (it raises inside is_answer)                 ok  rc 2
C23  an unreadable ledger (not JSON)                                              ok  rc 2
R1   fixture row: class, glyph and the legacy tooltip EXACTLY, per seat           ok  9 cells; mismatches []; legacy tip exact
R1g  every simple legacy cell's WHOLE tooltip, the class line for ITS d           ok  9 legacy cells; no exact tooltip for: []
R1h  a padded glyph ' ✓' renders legacy, not ok                                   ok  cell ('legacy', ' ✓')
R1e  an answer with a record beside it keeps the record's note                    ok  cells 1; record kept True
R1f  a refused exemption's line first, then the class line, exactly               ok  refusals 1; cells 1; tooltip exact
R1b  an escapable d renders escaped                                               ok  escape cell ('legacy', '&lt;b&gt;&amp;')
R1d  a whitespace-only d -- a space, a tab -- shows ?                             ok  whitespace cells [('legacy', '?'), ('legacy', '?')]
R1c  the fixture page says neither 'not approval' nor 'not a seat failure'        ok  render ok; found none
R4   the legend carries the legacy line EXACTLY                                   ok  legend found
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy; EACH strip number is the ledger's own count ok  before {'bad': 17, 'hold': 53, 'none': 29472, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 53, 'legacy': 670, 'none': 29472, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all' | ledger 5177 entries, 1397 off-domain
R3   MUTANT ok renders and fails its check                                        ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT pend renders and fails its check                                      ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT noescape renders and fails its check                                  ok  escape cell ('legacy', '<b>&')
W1   Q2 on the shipped ledger                                                     ok  GOOD entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baselin | failures 0
W2   Q2 with a new off-domain answer                                              ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W3   Q2 with the baseline absent (rc 2 path)                                      ok  BAD check_entry_domain.py could not run (rc 2): APPARATUS FAIL: baseline unreadable or mis | failures 1
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W5   Q2 ignores an exported GXLEDGER naming a clean ledger                        ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W6   Q2 with the checker absent                                                   ok  BAD check_entry_domain.py MISSING -- the entry-domain check proved nothing | failures 1
DASHOKCLASS CONTROLS: 72/72 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4c. `RECEIPT_v4_on_staged_v3.txt` (the v3 files, the pre-repair column) -- the tally and the red rows

```
# dashokclass controls (v4) -- checker 0266971b | renderer 483af869 | precommit 74358345 | baseline 06a3ffc6
C21d a misshapen ledger: {"rows": {}}                                             NO  rc 0
C21e a misshapen ledger: an entry that is a string                                NO  rc 0
C21f a misshapen ledger: entries that are an object                               NO  rc 0
C21g a misshapen baseline: an object, not a list (override)                       NO  rc 1
DASHOKCLASS CONTROLS: 68/72 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4d. `KILLTABLE_v4_staged.txt` (the mutant list is `run_mutants_v4.py`'s MUTANTS)

```
# dashokclass kill table (v4) -- controls run_controls_v4.py
BASE          72/72
d_cutoff18    71/72   killed by: C12                                                     [C12]
d_cutgt       71/72   killed by: C12                                                     [C12]
d_nodate      69/72   killed by: C12                                                     [C12]
d_lexdate     71/72   killed by: C19b                                                    [C19b]
d_noreason    70/72   killed by: C19a C19b                                               [C19a C19b]
d_blank       68/72   killed by: C1 C11 C14 C26                                          [C14]
d_domnohold   56/72   killed by: C1 C10 C11 C12 C17b C18 C18b C2 C22 C24 C27 C2b C2c C7 C8 W1 [C2c]
d_domnopend   56/72   killed by: C1 C10 C11 C12 C17b C18 C18b C2 C22 C24 C27 C2b C2d C7 C8 W1 [C2d]
d_dupplus1    48/72   killed by: C11 C14 C15 C16 C19a C19b C25a C25b C25c C25d C25e C25f C25g C25h C25i C25j C25k C26 C5 C6 C9 W2 W4 W5 [C5 C9]
d_nonote      59/72   killed by: C1 C10 C12 C17b C18 C18b C2 C22 C24 C2b C7 C8 W1        [C1]
d_nonote2     68/72   killed by: C15 C16 C25e C25f                                       [C15 C16]
d_lastwins    71/72   killed by: C17b                                                    [C17b]
d_ledger1     71/72   killed by: C21h                                                    [C21h]
d_nomd5       71/72   killed by: C18                                                     [C18]
d_pinoverride 65/72   killed by: C11 C12 C17b C18                                        [C18]
d_crlfpin     71/72   killed by: C18b                                                    [C18b]
d_noreconf    62/72   killed by: C11 C14 C19a C19b C20 C26 C3 C4 C5 C6                   [C20]
d_notenone    72/72   escapes (as recorded)                                              [UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note]
r_nolegend    71/72   killed by: R4                                                      [R4]
r_tipclause   68/72   killed by: R1 R1c R1f R1g                                          [R1 R1c]
r_tiptail     69/72   killed by: R1 R1f R1g                                              [R1]
r_ok          62/72   killed by: R1 R1b R1d R1e R1f R1g R1h R2 R3                        [R1]
r_pend        62/72   killed by: R1 R1b R1d R1e R1f R1g R1h R2 R3                        [R1]
r_noescape    70/72   killed by: R1b R3                                                  [R1b]
r_wsblank     70/72   killed by: R1d R3                                                  [R1d]
r_strip       71/72   killed by: R2                                                      [R2]
w_envkeep     70/72   killed by: W4 W5                                                   [W4 W5]
w_ledgerkeep  71/72   killed by: W5                                                      [W5]
w_collapse    71/72   killed by: W3                                                      [W3]
w_rc7         69/72   killed by: W2 W4 W5                                                [W2]
w_msg         69/72   killed by: W2 W4 W5                                                [W2]
w_subshell    69/72   killed by: W2 W4 W5                                                [W2]
d_date10      70/72   killed by: C25a C25b                                               [C25a C25b]
d_dstrip      71/72   killed by: C25c                                                    [C25c]
d_dfold       59/72   killed by: C1 C10 C12 C17b C18 C18b C2 C22 C24 C2b C7 C8 W1        [C1]
d_dfold2      71/72   killed by: C25d                                                    [C25d]
d_notestrip   59/72   killed by: C1 C10 C12 C17b C18 C18b C2 C22 C24 C2b C7 C8 W1        [C1]
d_notefold    59/72   killed by: C1 C10 C12 C17b C18 C18b C2 C22 C24 C2b C7 C8 W1        [C1]
d_seatstrip   71/72   killed by: C25g                                                    [C25g]
d_seatfold    71/72   killed by: C25h                                                    [C25h]
d_phasestrip  71/72   killed by: C25i                                                    [C25i]
d_phasefold   71/72   killed by: C25j                                                    [C25j]
d_shaperows   71/72   killed by: C21d                                                    [C21d]
d_shapeents   71/72   killed by: C21f                                                    [C21f]
d_shapeentry  71/72   killed by: C21e                                                    [C21e]
d_noshape     69/72   killed by: C21d C21e C21f                                          [C21d C21e C21f]
d_basedict    71/72   killed by: C21g                                                    [C21g]
r_norecord    71/72   killed by: R1e                                                     [R1e]
r_okonly      71/72   killed by: R1g                                                     [R1g]
r_stripok     71/72   killed by: R2                                                      [R2]
r_refusallast 71/72   killed by: R1f                                                     [R1f]
w_nochecker   71/72   killed by: W6                                                      [W6]
d_unread0     71/72   killed by: C23                                                     [C23]
d_summary     71/72   killed by: C11                                                     [C11]
r_tipokonly   71/72   killed by: R1g                                                     [R1g]
r_tipnonblank 71/72   killed by: R1g                                                     [R1g]
r_clsstrip    68/72   killed by: R1g R1h R3                                              [R1h]
d_isheld      58/72   killed by: C1 C10 C11 C12 C17b C18 C18b C2 C22 C24 C2b C7 C8 W1    [C24]
d_nulld       71/72   killed by: C26                                                     [C26]
d_nohint      71/72   killed by: C11                                                     [C11]
d_domzxq      71/72   killed by: C27                                                     [C27]
r_dclasszxq   71/72   killed by: C27                                                     [C27]
d_cut2days    71/72   killed by: C12                                                     [C12]
d_baselen     71/72   killed by: C1                                                      [C1]
w_nosed       71/72   killed by: W2                                                      [W2]
r_wsspace     70/72   killed by: R1d R3                                                  [R1d]
KILL TABLE: 66/66 as recorded
DASHOKCLASS_MUTANTS_DONE
```

## 5. The records this landing writes AT COMMIT (previews against HEAD 8bf8b5a1)

### 5a. OUTSTANDING_BUGS.md

```diff
--- ../cxland/ob_head.md
+++ ob_dash_preview.md
@@ -24719,6 +24719,12 @@
 * **`dashokclass` (LOW, open)** -- `tools/pipeline/gen_dashboard.py`: `D_CLASS` maps only the four glyphs, so the 439
   ledger entries whose `d` is "OK" (365 matrix cells) render in the seat-failure class.  One line or a ledger sweep;
   either owes the controls a `DASH` row with `d` "OK".  Display only.
+  **CLOSED 2026-10-17 by the `dashokclass` landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F2:
+  no `OK` -> approval mapping and no sweep): every explicit `d` outside the four glyphs, on the ANSWER a cell shows,
+  renders as ONE class, "legacy -- verdict unclassified" (a live hold and a non-answer record keep their own rendering),
+  its text kept -- 670 displayed cells at HEAD 8bf8b5a1, 1,397 entries, not the 365 `OK` cells
+  named above -- and precommit Q2 (`tools/pipeline/check_entry_domain.py`) holds the off-domain ANSWERS to a ceiling frozen
+  at landing.  Controls `regress/artifacts/dashokclass_20261016/RECEIPT_v4_on_staged_v4.txt`; kill table `regress/artifacts/dashokclass_20261016/KILLTABLE_v4_staged.txt`.
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
@@ -24761,3 +24767,20 @@
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
+  H, and the ruling must take both** (Fable 5.1, v3 pass, measured at HEAD): 158 entries' notes say NOT FIRED or name the
+  roster, 127 of them carry no token -- ANSWERS by `stage_tokens.is_answer`, 71 with no `d` -- and `check_stage_panels.py`
+  counts an untokened entry as a recorded seat while skipping a NOTSEAT one.  So the project's standing way to meet H's
+  nine seats under a reduced roster IS part of this population: a Q2 refusing a new `d`-less answer would refuse the next
+  landing's not-fired entries, and tokening them NOTSEAT turns H red.  Found by the main loop while landing `dashokclass`.
```

### 5b. the ledger rows

```
# ledger changes the dashokclass landing makes, against HEAD (a preview; applied at commit)

== dashmissingd (NEW ROW)
  commits: ""
  id: "dashmissingd"
  sev: "LOW"
  state: "open"
  state_note: "filed 2026-10-17 at the dashokclass landing, by the main loop: regress/artifacts/dashokclass_20261016/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt (its deriver dashmissingd_census.py beside it) counts 1,561 of 5,177 entries as answers with no d -- 2026-08 174, 2026-09 1,244, 2026-10 143, the latest dated 2026-10-16 -- and 814 displayed cells whose latest answer has none.  gen_dashboard.py's `d = ent.get(\"d\", \"…\")` shows each as no answer / seat failure.  A rule question for the adjudicators, not a sweep: either Q2 refuses a NEW answer without d (reversing Astra's condition 1 forward of a cutoff) or the renderer gives a d-less answer its own class; RULINGS_C F2 keeps the old entries as they are either way.  ENTANGLED WITH SECTION H (Fable 5.1, v3 pass, measured at HEAD): 158 entries' notes say NOT FIRED or name the roster, 127 untokened (answers by is_answer), 71 of them with no d, and check_stage_panels.py counts an untokened entry as a recorded seat while skipping a NOTSEAT one -- so refusing a new d-less answer would refuse the next landing's not-fired entries, and tokening them NOTSEAT turns H red; the ruling must take both."
  title: "tools/pipeline/gen_dashboard.py renders an ANSWER with no `d` as the seat-failure glyph and precommit Q2 lets new ones in: 814 of 2,953 displayed answer cells at HEAD 8bf8b5a1 (682 of them, by a keyword screen, real answers)"
  witness: null

== dashokclass 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the dashokclass landing (RULINGS_C F2): every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class, 'legacy -- verdict unclassified', its text kept and its reason in the tooltip; precommit Q2 (check_entry_domain.py) holds the off-domain answers to a ceiling frozen at landing -- per (row, phase, seat, date, d, note sha1), no more answers than the md5-pinned baseline holds.  The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities cannot exceed their landing baseline.  Witness: R2, 670 cells moved from the seat-failure class to legacy with nothing else changing.  The controls' CONTRACT names each decision's pinned edges and what is disclosed.  Four passes on the staged files -- pass 2, the adjudication pass, the v3 pass and the v4 pass, the owner's four-seat roster each time (Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- GPT-6 Astra: a per-(row, phase, seat, date, d) count let a converted entry's allowance be refilled by a new answer (measured rc 0); the tooltip's 'not approval, not a seat failure' is contradicted by legacy answers whose notes record real failures; the baseline writer's placement is no guard.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/codex_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2 (v1): SHIP WITH CHANGES (4) -- GLM 5.3: the rc-2 path through the gate untested, no escapable-d fixture, no refill control, no legend line for an explicit blank.  All added in v2 (W3, R1b, C15, the legend line).", "ev": "regress/artifacts/dashokclass_20261016/pass2/glm_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured; CUTOFF moved to 2026-10-18 passed all 19 v1 controls; the precommit's cp1252 pipe raised UnicodeEncodeError on the failure lines; legacy answers whose notes name a non-answer; control gaps in C1, C11, R1-R3, W1-W2.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/fable5_dashok.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- Grok 4.7: an exported GXDOMAIN_BASELINE was honoured inside the hook; the loader kept the LAST count for a repeated key; the tooltip's denial and the unpinned inclusive cutoff.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/grok_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the 'identity' key is a CEILING over selected content (a byte-identical revert and a same-note replacement pass; 1,342 keys cover 1,356 answers) -- state the narrower guarantee or build provenance; three one-edit survivors (the tooltip clause restored after the checked prefix, `-u GXLEDGER` deleted, the loader's += made =); the v2 runner named the v1 controls; four claims to correct.  All applied in v3, the narrower guarantee stated in its words.", "ev": "regress/artifacts/dashokclass_20261016/f2/codex_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3: d_nonote dies on the baseline mismatch, not on the note (add the coherent two-edit form); the loader's summation pinned by nothing; R1 and R4 pinned prefixes only.  All applied in v3 (d_nonote2 killed by exactly C15 and C16; C17b; whole-string R1 and R4).", "ev": "regress/artifacts/dashokclass_20261016/f2/glm_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v2 receipts reproduce only with v2 under v1's name; six one-edit mutants pass all 35 (the tooltip tail, the malformed-date reason, which Q2 branch fired); three sentences overclaim; and its own pass-2 'note out of the key' was wrong.  All applied in v3.", "ev": "regress/artifacts/dashokclass_20261016/f2/fable5_dashokf2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: the note-only toll is this check's, not the ruling's; the Q2 comment's growth claim and 'can only shrink' survived; the raw-byte md5 pin reds a default Git-for-Windows checkout (the main loop measured it the same hour: a fresh clone gives 89d1d370 for 06a3ffc6; Fable 5.1 reproduced it on the v3 pass).  All applied in v3 (the pin folds CRLF; C18b).", "ev": "regress/artifacts/dashokclass_20261016/f2/grok_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v4 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v4 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v4 pass, NOT FIRED: the kimi seat sat outside the roster."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v4 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v4 pass, NOT FIRED: minimax-m3 was given no packet; the roster, not a wall."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: five one-edit survivors of the 46 (a date suffix, the record line, the class line on non-OK cells, the per-glyph strip, the missing-checker branch); {\"rows\": {}} and a string entry walked as empty and passed; C2c/C2d red without their own entries; four record sentences.  All addressed in v4 (the class closure: ledger_shape, C21d-h, C25, R1e-g, R2 per glyph, W6, isolated C2c/C2d).  Its NOTSEAT advice on not-fired entries is carried as a disagreement (section H counts seats by is_answer).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/codex_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GLM 5.3: the checker-absent and ledger-unreadable edges unpinned; the summary line pinned only on a clean ledger; two stale sentences (RULINGS_C's '5,150 at HEAD', Q2's 'or is a frozen legacy entry' header).  All addressed in v4 (W6, C23, C11's dirty summary, both sentences).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/glm_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v3 receipts and the table reproduce; `if cls == LEGACY and d == \"OK\"` and its non-blank sibling pass all 46 (R1 pinned ONE cell's tooltip); the MISSING-checker branch; three records sentences; the dashmissingd question omits the section-H collision.  All addressed in v4 (R1g whole tooltips, W6, C24, C26, R1h, the hint, the filing).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/fable5_dashokv3.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Grok 4.7: the glyph set open at the top (a fifth DOMAIN member or D_CLASS key passes); the cutoff pinned on two days; the summary's baseline number and Q2's named-entry lines unread; a tab-only d.  All addressed in v4 (C27, C12 far, C1 baseline, W2 names, R1d tab).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/grok_dashokv3.txt", "d": "✓"}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] dashokclass closed by its landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v4_on_staged_v4.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 72/72 -- in particular R2 (only pend -> legacy, 670 cells, each strip number the ledger's own), C15/C16 (the note in the key), C25 (each key field byte for byte), C17b (a split baseline key sums), C18/C18b (the md5 pin, CRLF folded), C21a-h (a misshapen ledger or baseline is rc 2), C27 (the glyph set), R1g (every legacy cell's whole tooltip) and W4-W6 (exported overrides stripped; the checker absent is BAD) -- and does regress/artifacts/dashokclass_20261016/KILLTABLE_v4_staged.txt's runner still kill every pinned mutant?  Is the record (the checker's docstring, the Q2 comment, the CHANGELOG block, the bug-file closure) true of what shipped, and is the narrower guarantee -- a ceiling over selected content, not an entry identity -- stated where a reader will meet it?"
  state: "closed"
  state_note: "filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, \"pend\")`; HEAD's ledger carries 439 entries with d \"OK\" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS (\"OK\": \"ok\") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d \"OK\".  LOW, display only.\n\n[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line \"OK\": \"ok\", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class (a live hold and a non-answer record keep their own rendering), its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at landing.  The 365 above counts OK cells only; the legacy class is 670 displayed cells (1,397 entries) at HEAD 8bf8b5a1."
  witness: "harness:regress/artifacts/dashokclass_20261016/RECEIPT_v4_on_staged_v4.txt -- R2: HEAD's renderer (gen_dashboard_before.py) shows 1,503 displayed cells in the seat-failure class and the staged one 833, the 670 moved now LEGACY with nothing else changing; C1-C27 and W1-W6 pin the entry-domain check; regress/artifacts/dashokclass_20261016/KILLTABLE_v4_staged.txt kills every pinned mutant (66/66 as recorded, one escape recorded as equivalent)"
```

### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md

```diff
--- ../cxland/rulingsC_head.md
+++ rulingsC_dash_preview.md
@@ -41,8 +41,11 @@
 **F2 / D2 `dashokclass` -- UPHELD with the class re-keyed (Grok and Fable independently; Astra agrees on the semantics).**
 - Every mechanical sweep stays withdrawn (3/3).
 - The legacy class is keyed on the DOMAIN, not the spelling: every explicit `d` outside the four glyphs renders as one
-  residue class, labelled "legacy -- verdict unclassified" (Astra's wording), text kept, notes and hold/record precedence
-  preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at HEAD).  Keyed on `OK` alone
+  residue class, labelled "legacy -- verdict unclassified" (adapted from Astra's "legacy OK — verdict unclassified";
+  this said "Astra's wording" until the 2026-10-17 dashokclass landing -- Fable 5.1 and GPT-6 Astra, adjudication pass),
+  text kept, notes and hold/record precedence
+  preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at the ruling's HEAD; 5,177 at
+  the landing's, 8bf8b5a1).  Keyed on `OK` alone
   it would leave 958 of 1,397 off-domain entries in the false `pend` class (Fable, `meas_C/okdomain_census.txt`: OK 439,
   other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7).
 - The forward domain check keeps Astra's four completeness conditions; a date-only cutoff cannot stop a back-dated or
```

### 5d. the CHANGELOG block (a DRAFT: its v4-pass sentence is written from this pass's answers)

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
  `GXDOMAIN_BASELINE` and `GXLEDGER`; a misshapen or unreadable ledger or baseline is rc 2, never green.
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v4.py`, 72 rows, its docstring the CONTRACT (each decision
  of the checker, the renderer change and Q2, with the rows that pin its edges and what is disclosed): 72/72 on the staged
  files, installed byte for byte (`RECEIPT_v4_on_staged_v4.txt`; the md5s are in its header), 68/72 on v3 (the four
  structure rows).  Kill table `run_mutants_v4.py`: 66/66 as recorded (`KILLTABLE_v4_staged.txt`) -- 65 mutants killed by
  the rows their lines name, `d_notenone` an equivalent escape (0 of 1,356 off-domain answers has an empty note);
  `d_nonote2` and `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms), killed by exactly C15/C16 and C25d.
  The v1-v3 runners and receipts are kept; `run_mutants.py` names `run_controls_v2.py` (it named the v1 suite, which
  crashes on the 7-field baseline, so its 14/14 had reproduced only in a staging copy -- Fable 5.1, GPT-6 Astra).
* Records: `dashokclass` closed (witness `harness:`, its REGRESS review HELD for the flagship); `dashmissingd` (LOW) filed --
  814 of 2,953 displayed answer cells show `…` because their latest answer has no `d` (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`),
  its rule question entangled with section H's seat count (Fable 5.1); RULINGS_C's "Astra's wording" corrected to "adapted
  from", and its "5,150 at HEAD" dated.

**Pass 2** (`pass2/`, on v1): Astra SWC 3, GLM SWC 4, Fable SWC 7, Grok SWC 3 -- the count key's refill, the tooltip's
denial, the baseline guard, the unpinned cutoff, the cp1252 traceback, the honoured override.  **Adjudication pass** (`f2/`,
on v2, every finding shared with every seat): all four SWC 3 -- the "identity" is a ceiling (Astra), one-edit survivors
(Astra, GLM, Fable, Grok), v2's runner naming the wrong controls (Fable, Astra), the CRLF pin (Grok; measured), the
note-only toll credited to the ruling (Grok); Fable 5.1 withdrew its own pass-2 "note out of the key".  **V3 pass**
(`v3pass/`): all four SWC 3 -- every seat found one-edit survivors of the 46 (the same class as the adjudication pass's), so
v4 is the CLASS CLOSURE: the shape check, each key field byte for byte, every legacy cell's whole tooltip, the strip per
glyph, the glyph set from both files, the missing checker.  **V4 pass** (`v4pass/`): [to be written from its answers].
Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2 (J1-J16): is my disposition right, and is the FIX right
   -- not only the finding?
2. **The enumeration.**  Is the CONTRACT complete (section 2b)?  Name every decision you checked.
3. **The kill table and the floor.**  Is any mutant killed for a reason OTHER than the one its line names?  Is there a
   one-edit mutant of the staged v4 checker, renderer or Q2 block, NOT in the table, that passes all 72 controls and breaks
   a ruled property?  If you find none, name the shapes you swept.
4. **The records (section 5).**  Is that text true of what ships?  Name any sentence that is false.
5. **The NOTSEAT disagreement** (section 2): rule on it.
6. **Which of my accepted dispositions is wrong?**  There are 16 in section 2; name the count you checked.
