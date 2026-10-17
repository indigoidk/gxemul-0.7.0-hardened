# V3 PASS -- `dashokclass`: the dashboard's legacy class and the entry-domain check, v3 after the adjudication pass

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator), a
pre-commit check over its JSON ledger, and the controls that pin both.  READ-ONLY: write nothing to any project tree.  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v3 files are STAGED under
`regress/artifacts/dashokclass_20261016/staged_v3/` (mirroring `tools/`); the controls are `run_controls_v3.py` and
`run_mutants_v3.py` beside it, run with CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT naming the staged files; the
adjudication-pass answers are in `f2/`.  Everything a packet-fed seat needs is inlined below.

**This is the repair chain's pass on v3.**  It closes on the first pass whose zero floor breaches survive adjudication --
so if you find none, say which cells and mutant shapes you swept.  Review EFFORT is scoped to the v2 -> v3 diff; the FLOOR
question -- a one-edit mutant of the staged checker, renderer or Q2 block that passes all 46 controls and breaks a ruled
property -- is asked of the whole v3 material.  Check the premises in section 2b; do not ratify them.

**Liveness:** open your answer with the token `ASTRA_DASHOKV3_20261017` on its own line, then your verdict line.

## 1. The adjudication-pass verdicts (on v2), every finding shared with every seat

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`f2/codex_dashokf2.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`f2/glm_dashokf2.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (3)** (`f2/fable5_dashokf2.md`; agent_models.py: clean claude-fable-5-1).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`f2/grok_dashokf2.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| H1 | Astra | the "identity" key is a COUNT CEILING over selected content: normalise an entry then restore it byte for byte, or replace it with one equal in all six fields and different in `ev`, and the check passes; 1,342 keys cover 1,356 frozen answers | **ACCEPTED as the narrower guarantee**, in Astra's words: *current selected-content multiplicities cannot exceed their landing baseline*.  The docstring and the Q2 comment now say "a ceiling ... not an entry identity", name the three cases that pass, and drop "can only shrink" (the count can climb back to 1,356, and a reviewed re-freeze can raise it).  Persistent entry identity with provenance is NOT built -- see 2b |
| H2 | Astra, GLM, Fable, Grok | one-edit survivors of v2's 35 controls: the tooltip's denial restored after the checked prefix (Astra, GLM, Grok); its tail deleted (Fable); `-u GXLEDGER` deleted from Q2 (Astra); the loader's `+=` made `=` (Astra, GLM, Grok); v1's lexical date compare restored, and the "not ISO" reason deleted (Fable); which Q2 branch fired (`-eq 1` -> `-eq 7`, the message rewritten; Fable); ⏸ and … only incidentally positive; a whitespace-only `d` rendered invisible (Fable) | **ALL PINNED**: R1 compares the legacy tooltip WHOLE and R1c refuses the denial anywhere on the page; R4 the whole legend line; W5 (a bad default ledger, a clean exported GXLEDGER: BAD); C17b (one key split across two baseline rows must sum); C19 asserts the reason; W1-W5 assert their branch's own first-line words; C2c/C2d; R1d.  Each has its mutant in the kill table |
| H3 | GLM, Astra, Fable | `d_nonote` is killed by C1's baseline mismatch, not by the note property | **CORRECTED**: its line says so; the COHERENT note-out (v1's key on both sides, a deliberate two-edit DESIGN mutant) `d_nonote2` is killed by exactly C15 and C16 |
| H4 | Fable, Astra | `run_mutants.py` (v2's table) runs `run_controls.py`, which is the v1 suite and crashes on the 7-field baseline: the 14/14 reproduced only in a staging copy | **FIXED**: `run_mutants.py` names `run_controls_v2.py` and takes CTL_*; v3's runner names `run_controls_v3.py`; the v3 receipts are of the staged files by md5 |
| H5 | Astra | the docstring promised rc 2 for a misshapen ledger, but `{"rows": null}` raised an uncaught exception | **FIXED**: the ledger walk is wrapped -- rc 2 "ledger misshapen", no traceback; C21a-c (`{"rows": null}`, a row that is not an object, a list) |
| H6 | Grok, Fable (exposure), main loop (measured) | the md5 pin hashes raw bytes; this machine's system git sets `core.autocrlf=true` (the repo's own config says false) | **FIXED on a measurement**: a fresh clone of an LF baseline here checked it out with md5 89d1d370 for 06a3ffc6, so the raw pin would red Q2 on every commit from a fresh clone.  The pin now folds CRLF to LF before hashing (the constant is unchanged); C18b |
| H7 | Grok | "editing such an entry means giving it a glyph, the ruling's way out" credits a NOTE-only toll to the ruling, which says nothing of note edits | **CORRECTED**: the toll is named as this check's |
| H8 | Fable | the docstring named one exit ("give it a glyph") where the hint names three | **CORRECTED**: "classify it -- a glyph, no `d`, or a non-answer record token" |
| H9 | Astra | the renderer comment's heading "NEITHER APPROVAL NOR A SEAT FAILURE" survives | **CORRECTED** (and it says what it used to say) |
| H10 | Fable | the renderer comment's "the reason first in its tooltip" is false on a refused-exemption cell | **CORRECTED** ("after a refused exemption's line, if any") |
| H11 | GLM | the summary's "%d frozen" counts passes, not the baseline; "(none exists)" is unchecked | **CORRECTED**: "%d within the frozen ceiling (baseline %d)"; the date paragraph gives the count -- 0 of 1,342 keys carry an empty or non-ISO date -- and says the ISO test is a SHAPE test, not a calendar one |
| H12 | Astra | RULINGS_C_records.md:44 calls the label "Astra's wording"; Astra's phrase was "legacy OK — verdict unclassified" | **CORRECTED AT COMMIT** (section 5c) |
| H13 | Astra, Fable | W1-W5 count failures with stand-in reporters, not the production good/bad and final exit | **DISCLOSED** in the controls' docstring; the production wiring is correct by inspection |
| H14 | main loop | a MISSING `d` on an ANSWER renders as the seat-failure glyph, and Q2 admits new ones (condition 1) | **FILED as `dashmissingd`** (LOW, a rule question for its own round) with its census (section 2b) |

## 2b. Premises to CHECK (stated as questions)

* **H1's narrower guarantee.**  Is a ceiling over (row, phase, seat, date, `d`, note sha1) the right thing to ship under
  RULINGS_C F2 ("an OK becomes ✓ only when a reader rewrites that one entry"), given that a revert and an `ev`-only
  replacement pass?  The alternative is entry identity with provenance (a comparison against HEAD's ledger, or persistent
  ids), which this round does not build.  Say which, and why.
* **H6's measurement.**  A temp repo with an LF copy of the baseline, cloned on this machine, gave md5 89d1d370 for the
  committed 06a3ffc6 (`core.autocrlf=true` in the system gitconfig, false in this repo's own config).  Is folding CRLF in
  the checker the right repair, as against a `.gitattributes` line?
* **H14's census** (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`, deriver `dashmissingd_census.py`): at HEAD 8bf8b5a1, 1,561 of
  5,177 entries are answers with no `d`, and 814 of 2,953 displayed answer cells show `…` because of it -- 682 of those,
  by a keyword screen of the note, record a real answer.  Is filing it (a rule question) right, rather than folding it
  into this round?  Is LOW right, beside `dashokclass`'s LOW and 670 cells?
* The seat entries this landing writes carry `d` ✓ for an answered seat whose changes were applied, and no `d` for a seat
  failure or a seat not fired (it renders `…`, which is what it was).  Is that the right practice while `dashmissingd`
  is open?

## 3. The repair, staged v2 -> v3 (94 changed lines across the checker, the renderer and precommit Q2)

```diff
--- staged_v2/tools/pipeline/check_entry_domain.py
+++ staged_v3/tools/pipeline/check_entry_domain.py
@@ -6,7 +6,8 @@
 `d` at all (the renderer's default is …).  MEASURED when this landed (HEAD 8bf8b5a1): 5,177 entries, 1,397 with an explicit
 `d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
 2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
-them as one residue class, "legacy -- verdict unclassified", and this check keeps NEW ones from appearing.  Ruled by Fable
+them as one residue class, "legacy -- verdict unclassified", and this check keeps answers with NEW content from appearing.
+Ruled by Fable
 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old
 entries is withdrawn -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.
 
@@ -16,24 +17,42 @@
   3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
   4. the controls carry POSITIVE rows (a valid glyph on and after the cutoff passes) beside the negatives.
 
-GRANDFATHERING IS BY ENTRY IDENTITY, NOT BY DATE AND NOT BY COUNT.  An off-domain answer passes only if it is IDENTICAL --
-row, phase, seat, date, `d` and NOTE (by its sha1) -- to one frozen in `entry_domain_baseline.json` when this check landed,
-and is not dated on or after CUTOFF.  So a new entry fails, a back-dated or undated one fails, a duplicate fails, and an old
-one EDITED in any of those fields fails: editing such an entry means giving it a glyph, which is the ruling's way out.
-(Pass 2 of this check, 2026-10-16: a per-(row, phase, seat, date, d) COUNT let a converted entry's allowance be refilled by
-a new answer, and let a note edit turn a record into an un-normalised answer -- GPT-6 Astra and GLM 5.3; the note is in the
-key for that reason.)  The grandfathered population can only shrink.  That is NOT a claim about the dashboard's legacy
-count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that reappears when a
-newer answer in its cell is removed.
-
-THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`): re-freezing it is a reviewed decision, made by changing that constant in
-the same commit with the reason, never by re-running the one-time writer
-(regress/artifacts/dashokclass_20261016/write_baseline.py).  A GXDOMAIN_BASELINE override skips the pin, for the controls.
-Dates are compared as ISO `YYYY-MM-DD` prefixes; a date in any other form is never "on or after the cutoff", so a malformed
-date passes only on an identical frozen entry (none exists).
+GRANDFATHERING IS A CEILING OVER SELECTED CONTENT -- NOT A DATE, AND NOT AN ENTRY IDENTITY.  An off-domain answer passes
+only while the ledger holds no more answers with its (row, phase, seat, date, `d`, sha1 of its NOTE) than
+`entry_domain_baseline.json` froze when this check landed, and only if it is not dated on or after CUTOFF.  So a new answer
+fails, a back-dated or undated one fails, a copy fails, and an old one EDITED in any of those six fields fails: editing such
+an entry means classifying it -- a glyph, or no `d` at all (it renders as …), or a non-answer record token if it is not an
+answer.  For a NOTE-only correction that is this check's toll, not the ruling's: the ruling withdraws every mechanical sweep
+and classifies an entry when a reader rewrites it, and says nothing of note edits (Grok 4.7, adjudication pass).  (Pass 2,
+2026-10-16: a per-(row, phase, seat, date, d)
+count let a converted entry's allowance be refilled by a new answer with another note, measured by GPT-6 Astra and Fable
+5.1; the note is in the key for that reason.)
+
+THE GUARANTEE IS THE NARROWER ONE, in GPT-6 Astra's words at the adjudication pass: CURRENT SELECTED-CONTENT MULTIPLICITIES
+CANNOT EXCEED THEIR LANDING BASELINE.  The six fields are not an identity -- 1,342 distinct keys cover the 1,356 frozen
+answers -- and the check reads no earlier revision, so three things pass: an entry converted to a glyph and later restored
+byte for byte (a revert); a replacement that matches a frozen entry in all six fields and differs only outside them; and an
+edit outside them (`ev`, `grade`, `b`; stage_tokens.is_answer reads only the note, so such an edit cannot turn a record into
+an answer).  So the count within the ceiling never exceeds 1,356 -- until a reviewed re-freeze changes the pin -- and can
+climb back to it after shrinking.  It is not the
+dashboard's legacy count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that
+reappears when a newer answer in its cell is removed.
+
+THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`), which makes a re-freeze VISIBLE: it has to change that constant in the
+same commit, with its reason, where a reviewer sees both -- never a silent re-run of the one-time writer
+(regress/artifacts/dashokclass_20261016/write_baseline.py, which refuses to overwrite without --force).  That the change was
+REVIEWED is a practice the pin cannot enforce (GPT-6 Astra and Fable 5.1, adjudication pass).  The md5 is taken with CRLF
+folded to LF: this machine's system git sets core.autocrlf=true, and a fresh clone checked the file out as 89d1d370 for
+06a3ffc6 (measured at the adjudication pass), which a raw pin would red on every commit.  A GXDOMAIN_BASELINE override skips
+the pin, for the controls; precommit Q2 strips it.
+
+The cutoff reads a date only when it OPENS with the ISO shape `YYYY-MM-DD` -- a shape test, not a calendar check: a
+"2026-13-45" counts as on or after it and fails; a "2026-02-30" counts as before it and must match a frozen entry.  A date in
+any other form, or none, is never "on or after the cutoff", so it passes only by matching a frozen entry -- and the baseline
+holds none: 0 of its 1,342 keys carries an empty or non-ISO date (measured at landing).
 
 Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
-Exit: 0 clean; 1 an off-domain answer that is not a frozen entry (each named); 2 apparatus failure (baseline or ledger
+Exit: 0 clean; 1 an off-domain answer beyond the frozen ceiling (each named); 2 apparatus failure (baseline or ledger
 unreadable or misshapen, or the baseline's md5 is not the pinned one)."""
 import collections, hashlib, io, json, os, re, sys
 
@@ -82,9 +101,10 @@
         print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2
     try:
         raw = open(BASELINE, "rb").read()
-        if BASELINE == DEFAULT_BASELINE and hashlib.md5(raw).hexdigest() != BASELINE_MD5:
+        md = hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()      # line endings folded: see the docstring
+        if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:
             print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
-                  "in the same commit, with its reason" % (BASELINE, hashlib.md5(raw).hexdigest(), BASELINE_MD5)); return 2
+                  "in the same commit, with its reason" % (BASELINE, md, BASELINE_MD5)); return 2
         base = collections.Counter()
         for k in json.loads(raw.decode("utf-8")):
             if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
@@ -93,7 +113,10 @@
             base[tuple(k[:6])] += k[6]
     except Exception as ex:
         print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
-    cur = off_domain_answers(ledger)
+    try:
+        cur = off_domain_answers(ledger)
+    except Exception as ex:      # {"rows": null}, a row that is not an object ... (GPT-6 Astra, adjudication pass)
+        print("APPARATUS FAIL: ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2
     seen = collections.Counter()
     bad = []
     for t in cur:
@@ -101,11 +124,11 @@
         if ISO.match(t[3]) and t[3][:10] >= CUTOFF:
             bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
         elif seen[t] > base[t]:
-            why = "not identical to a frozen entry -- a new one, a duplicate, or an old one edited (give it a glyph)"
+            why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
             if t[3] and not ISO.match(t[3]):
                 why += "; its date is not ISO YYYY-MM-DD"
             bad.append((t, why))
-    print("entry domain: %d off-domain answer entries; %d frozen (baseline %d); cutoff %s inclusive"
+    print("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff %s inclusive"
           % (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))
     for (row, phase, seat, date, d, ns), why in bad:
         print("  OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s"
--- staged_v2/tools/pipeline/gen_dashboard.py
+++ staged_v3/tools/pipeline/gen_dashboard.py
@@ -72,15 +72,18 @@
     sys.exit(2)
 
 D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
-#  *** AN EXPLICIT `d` OUTSIDE THOSE FOUR IS NEITHER APPROVAL NOR A SEAT FAILURE, AND UNTIL 2026-10-16 IT RENDERED AS THE
-#  SECOND.  (ledger `dashokclass`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, adj_20261016/RULINGS_C_records.md F2.) ***
+#  *** AN EXPLICIT `d` OUTSIDE THOSE FOUR IS NO VERDICT THIS PAGE CAN CLASSIFY, AND UNTIL 2026-10-16 IT RENDERED AS A SEAT
+#  FAILURE.  (ledger `dashokclass`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, adj_20261016/RULINGS_C_records.md F2.  This
+#  heading said "NEITHER APPROVAL NOR A SEAT FAILURE" until the adjudication pass; some of them are a seat failure.) ***
 #  The fallback was `pend`, so 1,397 entries whose `d` is "OK", "N/A", a date, "y", "HELD", blank ... -- 439 of them "OK",
 #  365 displayed cells -- all read as "no answer / seat failure".  Mapping "OK" to `ok` was REJECTED (it canonises one
 #  off-domain spelling as approval); every mechanical sweep of the entries was withdrawn.  So an explicit `d` the map does
-#  not know renders as ONE residue class, LEGACY, keeping its text, with the reason first in its tooltip; a MISSING `d` is
+#  not know renders as ONE residue class, LEGACY, keeping its text, with the reason first in its tooltip (after a refused
+#  exemption's line, if any -- Fable 5.1, adjudication pass); a MISSING `d` is
 #  still `…`, an explicit blank shows `?`.  The class says only that the `d` is unclassified -- three legacy cells (`WALL`)
 #  record real seat failures in their notes, so the tooltip sends the reader to the note rather than denying either reading
-#  (GPT-6 Astra, pass 2).  check_entry_domain.py (precommit Q2) refuses any off-domain ANSWER not frozen when it landed.
+#  (GPT-6 Astra, pass 2).  check_entry_domain.py (precommit Q2) holds the off-domain ANSWERS to the ceiling frozen when it
+#  landed.
 LEGACY = "legacy"
 e = lambda t: html.escape(str(t), quote=True)
 
--- staged_v2/tools/precommit_check.sh
+++ staged_v3/tools/precommit_check.sh
@@ -496,24 +496,28 @@
 #  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS A FROZEN LEGACY ENTRY.  2026-10-16, ledger `dashokclass`
 #  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
 #  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
-#  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section keeps that class from
-#  growing.  Grandfathering is by ENTRY IDENTITY against a frozen, md5-pinned baseline -- row, phase, seat, date, d and
-#  note -- not by a date (a date-only cutoff cannot stop a back-dated or undated addition) and not by a per-tuple count
-#  (a converted entry's allowance could be refilled; pass 2).  HARD.  It fails on a NEW off-domain answer and on an OLD
-#  one edited in any of those fields: editing such an entry means giving it a glyph, the ruling's way out.  It reds
-#  (rc 2) when the baseline is unreadable or its md5 is not the pinned one, never silently green.
+#  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section holds the off-domain
+#  ANSWERS to a CEILING frozen at landing: for each row, phase, seat, date, d and note, no more answers than the md5-pinned
+#  baseline holds.  Not a date (a date-only cutoff cannot stop a back-dated or undated addition), not a count without the
+#  note (a converted entry's allowance could be refilled; pass 2), and NOT an entry identity: a byte-identical revert of a
+#  normalised entry passes, and the dashboard's legacy count can still rise through exempt records and re-exposed older
+#  answers (adjudication pass, GPT-6 Astra).  HARD.  It fails on a NEW off-domain answer and on an OLD one edited in any
+#  of those fields: editing such an entry means classifying it -- a glyph, no `d`, or a non-answer record token (Fable
+#  5.1); for a note-only correction that toll is this check's, not the ruling's (Grok 4.7).  It reds (rc 2) when the ledger
+#  or the baseline is unreadable or misshapen or the baseline's md5 is not the pinned one, never silently green.
 say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is a frozen legacy entry"
 CED=$_HERE/pipeline/check_entry_domain.py
 if [ ! -f "$CED" ]; then
 	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
 else
 	#  the overrides are for the controls, never for a commit: an exported GXDOMAIN_BASELINE would swap in another baseline
-	#  and skip the md5 pin (Grok 4.7, pass 2), so the section checks the real ledger against the pinned baseline
+	#  and skip the md5 pin (Grok 4.7, pass 2), and an exported GXLEDGER would check another ledger (adjudication pass), so
+	#  the section checks the real ledger against the pinned baseline
 	_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1); _cedrc=$?
 	if [ $_cedrc -eq 0 ]; then
 		good "$(printf '%s\n' "$_ced" | head -1)"
 	elif [ $_cedrc -eq 1 ]; then
-		bad "an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edited):"
+		bad "an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or an old one edited):"
 		printf '%s\n' "$_ced" | sed 's/^/          /'
 	else
 		bad "check_entry_domain.py could not run (rc $_cedrc): $(printf '%s\n' "$_ced" | head -1)"
```

## 4. The controls and their receipts

### 4a. what each of the 46 controls asserts (the docstring of `run_controls_v3.py`)

```
"""Controls for `dashokclass` (2026-10-16, v3 after the four-seat adjudication pass): gen_dashboard.py's LEGACY class,
check_entry_domain.py (a ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on
temp copies and fixture ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER /
CTL_RENDER / CTL_PRECOMMIT override the three files under test (run_mutants_v3.py and the staged runs use them); the defaults
are the tree's.

  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's and the adjudication pass's findings):
    C1   shipped ledger, shipped baseline (the md5 pin is checked on the default path)             -> 0, all within the ceiling
    C2   an answer ON the cutoff with a valid glyph (positive)                                      -> 0
    C2b  an answer AFTER the cutoff with a valid glyph (positive)                                   -> 0
    C2c  / C2d  an answer after the cutoff with ⏸ / with … (positive, one row per glyph)            -> 0 / 0
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
    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list -- rc 2, no traceback -> 2 / 2 / 2
    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
  RENDERER:
    R1   a fixture row, one entry per seat: class AND glyph per cell (the record cell's glyph included), and the
         legacy cell's tooltip EXACTLY (the whole string, not a prefix)
    R1b  an escapable `d` ("<b>&") renders escaped
    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
    R1d  a whitespace-only `d` (" ") shows `?`
    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip's five numbers sum to the ledger's
         actual entry count, and its legacy number is the ledger's own count of explicit off-domain `d`
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
"""
```

### 4b. `RECEIPT_v3_on_staged_v3.txt` (the v3 files), whole

```
# dashokclass controls (v3) -- checker 0266971b | renderer 483af869 | precommit 74358345 | baseline 06a3ffc6
C1   shipped ledger, shipped baseline, md5 pin live                               ok  rc 0: entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baseline 1356); cutoff 2026-10-17 inclusive
C2   ON the cutoff, a valid glyph (positive)                                      ok  rc 0 (want 0)
C2b  AFTER the cutoff, a valid glyph (positive)                                   ok  rc 0 (want 0)
C2c  AFTER the cutoff, d ⏸ (positive)                                             ok  rc 0 (want 0)
C2d  AFTER the cutoff, d … (positive)                                             ok  rc 0 (want 0)
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
C9   an identical copy of a frozen entry (alphactxfail assess codex 2026-09-08 'y') ok  rc 1
C10  a frozen entry rewritten to a glyph                                          ok  rc 0
C15  REFILL: the converted entry's (row, phase, seat, date, d) reused             ok  rc 1
C16  a frozen entry's note edited, d left off-domain                              ok  rc 1
C22  a frozen entry's ev edited, outside the six fields (positive)                ok  rc 0
C11  baseline emptied: every shipped off-domain answer named                      ok  rc 1, 1356 of 1356 named
C12  cutoff isolated: a FROZEN identity dated 2026-10-16 (before)                 ok  rc 0 (want 0)
C12  cutoff isolated: a FROZEN identity dated 2026-10-17 (on)                     ok  rc 1 (want 1)
C12  cutoff isolated: a FROZEN identity dated 2026-10-18 (after)                  ok  rc 1 (want 1)
C13  an unreadable baseline                                                       ok  rc 2
C17  a misshapen baseline (counts as strings)                                     ok  rc 2
C17b a key split across two baseline rows sums (alphaswpctxreg review grok 2026-09-08 'y' x2) ok  rc 0
C18  md5 pin: one baseline line changed -> 2, unchanged -> 0                      ok  changed rc 2, unchanged rc 0
C18b md5 pin: the baseline checked out with CRLF line endings -> 0                ok  rc 0
C21a a misshapen ledger: {"rows": null}                                           ok  rc 2
C21b a misshapen ledger: a row that is not an object                              ok  rc 2
C21c a misshapen ledger: a list, not an object                                    ok  rc 2
R1   fixture row: class, glyph and the legacy tooltip EXACTLY, per seat           ok  9 cells; mismatches []; legacy tip exact
R1b  an escapable d renders escaped                                               ok  escape cell ('legacy', '&lt;b&gt;&amp;')
R1d  a whitespace-only d shows ?                                                  ok  whitespace cell ('legacy', '?')
R1c  the fixture page says neither 'not approval' nor 'not a seat failure'        ok  render ok; found none
R4   the legend carries the legacy line EXACTLY                                   ok  legend found
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy; strip sums, legacy = the ledger's count ok  before {'bad': 17, 'hold': 53, 'none': 29472, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 53, 'legacy': 670, 'none': 29472, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all' | ledger 5177 entries, 1397 off-domain
R3   MUTANT ok renders and fails its check                                        ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT pend renders and fails its check                                      ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG: '2026-10-16 — a renderer control'
R3   MUTANT noescape renders and fails its check                                  ok  escape cell ('legacy', '<b>&')
W1   Q2 on the shipped ledger                                                     ok  GOOD entry domain: 1356 off-domain answer entries; 1356 within the frozen ceiling (baselin | failures 0
W2   Q2 with a new off-domain answer                                              ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W3   Q2 with the baseline absent (rc 2 path)                                      ok  BAD check_entry_domain.py could not run (rc 2): APPARATUS FAIL: baseline unreadable or mis | failures 1
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
W5   Q2 ignores an exported GXLEDGER naming a clean ledger                        ok  BAD an off-domain ledger answer is beyond the frozen legacy ceiling (a new one, a copy, or | failures 1
DASHOKCLASS CONTROLS: 46/46 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4c. `RECEIPT_v3_on_staged_v2.txt` (the v2 files, the pre-repair column) -- the tally and the red rows

```
# dashokclass controls (v3) -- checker 111bcac0 | renderer 2565a4a0 | precommit a96dad35 | baseline 06a3ffc6
C1   shipped ledger, shipped baseline, md5 pin live                               NO  rc 0: entry domain: 1356 off-domain answer entries; 13
C18b md5 pin: the baseline checked out with CRLF line endings -> 0                NO  rc 2
C21a a misshapen ledger: {"rows": null}                                           NO  rc 1 TRACEBACK
C21b a misshapen ledger: a row that is not an object                              NO  rc 1 TRACEBACK
C21c a misshapen ledger: a list, not an object                                    NO  rc 1 TRACEBACK
W1   Q2 on the shipped ledger                                                     NO  GOOD entry domain: 1356 off-domain answer entries; 135
W2   Q2 with a new off-domain answer                                              NO  BAD an off-domain ledger answer is not a frozen legacy
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          NO  BAD an off-domain ledger answer is not a frozen legacy
W5   Q2 ignores an exported GXLEDGER naming a clean ledger                        NO  BAD an off-domain ledger answer is not a frozen legacy
DASHOKCLASS CONTROLS: 37/46 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 4d. the kill table: the mutants (`run_mutants_v3.py`'s list) and `KILLTABLE_v3_staged.txt`

```python
MUTANTS = [   # name, file, [(find, replace), ...], controls that must go red (or "UNPINNED: why")
    ("d_cutoff18", "checker", [('CUTOFF = "2026-10-17"', 'CUTOFF = "2026-10-18"')], ["C12"]),
    ("d_cutgt", "checker", [("t[3][:10] >= CUTOFF", "t[3][:10] > CUTOFF")], ["C12"]),
    ("d_nodate", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if False:")], ["C12"]),
    ("d_lexdate", "checker", [("if ISO.match(t[3]) and t[3][:10] >= CUTOFF:", "if t[3] >= CUTOFF:")], ["C19b"]),
    ("d_noreason", "checker", [('why += "; its date is not ISO YYYY-MM-DD"', "pass")], ["C19a", "C19b"]),
    ("d_blank", "checker", [('if "d" not in x or x["d"] in DOMAIN', 'if not x.get("d") or x["d"] in DOMAIN')], ["C14"]),
    ("d_domnohold", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = ("✓", "✕", "…")')], ["C2c"]),
    ("d_domnopend", "checker", [('DOMAIN = ("✓", "✕", "⏸", "…")', 'DOMAIN = ("✓", "✕", "⏸")')], ["C2d"]),
    ("d_dupplus1", "checker", [("elif seen[t] > base[t]:", "elif seen[t] > base[t] + 1:")], ["C5", "C9"]),
    #  ONE-SIDED: the baseline still carries real note shas, so EVERY frozen answer stops matching -- a real kill by C1, and
    #  NOT evidence for the note property (GLM 5.3, GPT-6 Astra, Fable 5.1); d_nonote2 is
    ("d_nonote", "checker", [(SHA, 'return "0" * 16')], ["C1"]),
    #  the COHERENT note-out -- the pass-2 (v1) key reinstated on BOTH sides.  A deliberate TWO-edit DESIGN mutant: no
    #  one-edit form is coherent, and it exists to show C15 and C16, not C1's mismatch, discriminate the note
    ("d_nonote2", "checker", [(SHA, 'return "0" * 16'), (LOAD, 'base[tuple(k[:5]) + ("0" * 16,)] += k[6]')], ["C15", "C16"]),
    ("d_lastwins", "checker", [(LOAD, "base[tuple(k[:6])] = k[6]")], ["C17b"]),
    ("d_ledger1", "checker", [('ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2',
                               'ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 1')],
     ["C21a", "C21b", "C21c"]),
    ("d_nomd5", "checker", [("if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:", "if False:")], ["C18"]),
    ("d_pinoverride", "checker", [("if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:",
                                   "if BASELINE != DEFAULT_BASELINE and md != BASELINE_MD5:")], ["C18"]),
    ("d_crlfpin", "checker", [('md = hashlib.md5(raw.replace(b"\\r\\n", b"\\n")).hexdigest()', "md = hashlib.md5(raw).hexdigest()")],
     ["C18b"]),
    ("d_noreconf", "checker", [('sys.stdout.reconfigure(errors="backslashreplace")', "pass")], ["C20"]),
    ("d_notenone", "checker", [('str(x.get("note") or "")', 'str(x.get("note"))')],
     "UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note"),
    ("r_nolegend", "render", [("legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified", "unclassified")], ["R4"]),
    ("r_tipclause", "render", [("; read the note for the outcome", " (not approval, not a seat failure)")], ["R1", "R1c"]),
    ("r_tiptail", "render", [("; read the note for the outcome", "")], ["R1"]),
    ("r_ok", "render", [("cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")')], ["R1"]),
    ("r_pend", "render", [("cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")')], ["R1"]),
    ("r_noescape", "render", [('{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}')], ["R1b"]),
    ("r_wsblank", "render", [('{e(d) if str(d).strip() else "?"}', '{e(d) if d else "?"}')], ["R1d"]),
    ("r_strip", "render", [("n[d if d in D_CLASS else LEGACY] += 1", 'n[d if d in D_CLASS else "…"] += 1')], ["R2"]),
    ("w_envkeep", "precommit", [('_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1)', '_ced=$(python "$CED" 2>&1)')],
     ["W4", "W5"]),
    ("w_ledgerkeep", "precommit", [("env -u GXDOMAIN_BASELINE -u GXLEDGER python", "env -u GXDOMAIN_BASELINE python")], ["W5"]),
    ("w_collapse", "precommit", [("\tif [ $_cedrc -eq 0 ]; then\n\t\tgood", "\tif [ $_cedrc -ne 1 ]; then\n\t\tgood")], ["W3"]),
    ("w_rc7", "precommit", [("\telif [ $_cedrc -eq 1 ]; then", "\telif [ $_cedrc -eq 7 ]; then")], ["W2"]),
    ("w_msg", "precommit", [(BADMSG, '\t\tbad "x"')], ["W2"]),
    ("w_subshell", "precommit", [(BADMSG, "\t\t( " + BADMSG.strip() + " )")], ["W2"]),
]
```

```
# dashokclass kill table (v3) -- controls run_controls_v3.py
BASE          46/46
d_cutoff18    45/46   killed by: C12                                                     [C12]
d_cutgt       45/46   killed by: C12                                                     [C12]
d_nodate      44/46   killed by: C12                                                     [C12]
d_lexdate     45/46   killed by: C19b                                                    [C19b]
d_noreason    44/46   killed by: C19a C19b                                               [C19a C19b]
d_blank       43/46   killed by: C1 C11 C14                                              [C14]
d_domnohold   31/46   killed by: C1 C10 C11 C12 C17b C18 C18b C2 C22 C2b C2c C2d C7 C8 W1 [C2c]
d_domnopend   31/46   killed by: C1 C10 C11 C12 C17b C18 C18b C2 C22 C2b C2c C2d C7 C8 W1 [C2d]
d_dupplus1    34/46   killed by: C11 C14 C15 C16 C19a C19b C5 C6 C9 W2 W4 W5             [C5 C9]
d_nonote      32/46   killed by: C1 C10 C12 C17b C18 C18b C2 C22 C2b C2c C2d C7 C8 W1    [C1]
d_nonote2     44/46   killed by: C15 C16                                                 [C15 C16]
d_lastwins    45/46   killed by: C17b                                                    [C17b]
d_ledger1     43/46   killed by: C21a C21b C21c                                          [C21a C21b C21c]
d_nomd5       45/46   killed by: C18                                                     [C18]
d_pinoverride 40/46   killed by: C11 C12 C17b C18                                        [C18]
d_crlfpin     45/46   killed by: C18b                                                    [C18b]
d_noreconf    37/46   killed by: C11 C14 C19a C19b C20 C3 C4 C5 C6                       [C20]
d_notenone    46/46   escapes (as recorded)                                              [UNPINNED: equivalent on the ledger -- 0 of the 1,356 off-domain answers has an empty or missing note]
r_nolegend    45/46   killed by: R4                                                      [R4]
r_tipclause   44/46   killed by: R1 R1c                                                  [R1 R1c]
r_tiptail     45/46   killed by: R1                                                      [R1]
r_ok          40/46   killed by: R1 R1b R1d R2 R3                                        [R1]
r_pend        40/46   killed by: R1 R1b R1d R2 R3                                        [R1]
r_noescape    44/46   killed by: R1b R3                                                  [R1b]
r_wsblank     44/46   killed by: R1d R3                                                  [R1d]
r_strip       45/46   killed by: R2                                                      [R2]
w_envkeep     44/46   killed by: W4 W5                                                   [W4 W5]
w_ledgerkeep  45/46   killed by: W5                                                      [W5]
w_collapse    45/46   killed by: W3                                                      [W3]
w_rc7         43/46   killed by: W2 W4 W5                                                [W2]
w_msg         43/46   killed by: W2 W4 W5                                                [W2]
w_subshell    43/46   killed by: W2 W4 W5                                                [W2]
KILL TABLE: 32/32 as recorded
DASHOKCLASS_MUTANTS_DONE
```

### 4e. `DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt` (H14)

```
entries: 5177 | answers with no d: 1561 (by month: 2026-08 174, 2026-09 1244, 2026-10 143; the latest dated 2026-10-16) | of those, the note names a non-answer: 300
displayed answer cells: 2953 | whose latest answer has no d (rendered as the seat-failure glyph): 814 | of those, the note names no non-answer (an answer shown as a failure, by the keyword screen): 682
DASHMISSINGD_CENSUS_DONE
```

## 5. The records this landing writes AT COMMIT (previews against HEAD 8bf8b5a1)

### 5a. OUTSTANDING_BUGS.md

```diff
--- ../cxland/ob_head.md
+++ ob_dash_preview.md
@@ -24719,6 +24719,11 @@
 * **`dashokclass` (LOW, open)** -- `tools/pipeline/gen_dashboard.py`: `D_CLASS` maps only the four glyphs, so the 439
   ledger entries whose `d` is "OK" (365 matrix cells) render in the seat-failure class.  One line or a ledger sweep;
   either owes the controls a `DASH` row with `d` "OK".  Display only.
+  **CLOSED 2026-10-17 by the `dashokclass` landing, and the fix prescribed above was REPLACED, not applied** (RULINGS_C F2:
+  no `OK` -> approval mapping and no sweep): every explicit `d` outside the four glyphs renders as ONE class, "legacy --
+  verdict unclassified", its text kept -- 670 displayed cells at HEAD 8bf8b5a1, 1,397 entries, not the 365 `OK` cells
+  named above -- and precommit Q2 (`tools/pipeline/check_entry_domain.py`) holds the off-domain ANSWERS to a ceiling frozen
+  at landing.  Controls `regress/artifacts/dashokclass_20261016/RECEIPT_v3_on_staged_v3.txt`; kill table `regress/artifacts/dashokclass_20261016/KILLTABLE_v3_staged.txt`.
 * **`cxlaunchquotation` (LOW, open)** -- `tools/cxlaunch.sh`'s wall check greps the seat's answer for `quota`, so an
   answer containing "quotation" is reported SEAT WALLED (rc 8).  Measured 2026-10-09 on a complete GPT-6 Astra answer.
   Word-anchor it and test stdout only when no verdict line is present; controls both ways.
@@ -24761,3 +24766,16 @@
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
+  its own class; the old entries stay as they are under RULINGS_C F2 either way.  Found by the main loop while landing
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
  state_note: "filed 2026-10-17 at the dashokclass landing, by the main loop: regress/artifacts/dashokclass_20261016/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt (its deriver dashmissingd_census.py beside it) counts 1,561 of 5,177 entries as answers with no d -- 2026-08 174, 2026-09 1,244, 2026-10 143, the latest dated 2026-10-16 -- and 814 displayed cells whose latest answer has none.  gen_dashboard.py's `d = ent.get(\"d\", \"…\")` shows each as no answer / seat failure.  A rule question for the adjudicators, not a sweep: either Q2 refuses a NEW answer without d (reversing Astra's condition 1 forward of a cutoff) or the renderer gives a d-less answer its own class; RULINGS_C F2 keeps the old entries as they are either way."
  title: "tools/pipeline/gen_dashboard.py renders an ANSWER with no `d` as the seat-failure glyph and precommit Q2 lets new ones in: 814 of 2,953 displayed answer cells at HEAD 8bf8b5a1 (682 of them, by a keyword screen, real answers)"
  witness: null

== dashokclass 
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the dashokclass landing (RULINGS_C F2): every explicit d outside the four glyphs renders as one LEGACY class, 'legacy -- verdict unclassified', its text kept and its reason in the tooltip; precommit Q2 (check_entry_domain.py) holds the off-domain answers to a ceiling frozen at landing -- per (row, phase, seat, date, d, note sha1), no more answers than the md5-pinned baseline holds.  The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities cannot exceed their landing baseline.  Witness: R2, 670 cells moved from the seat-failure class to legacy with nothing else changing.  Three passes on the staged files -- pass 2, the adjudication pass and the v3 pass, the owner's four-seat roster each time (Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- GPT-6 Astra: a per-(row, phase, seat, date, d) count let a converted entry's allowance be refilled by a new answer (measured rc 0); the tooltip's 'not approval, not a seat failure' is contradicted by legacy answers whose notes record real failures; the baseline writer's placement is no guard.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/codex_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2 (v1): SHIP WITH CHANGES (4) -- GLM 5.3: the rc-2 path through the gate untested, no escapable-d fixture, no refill control, no legend line for an explicit blank.  All added in v2 (W3, R1b, C15, the legend line).", "ev": "regress/artifacts/dashokclass_20261016/pass2/glm_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured; CUTOFF moved to 2026-10-18 passed all 19 v1 controls; the precommit's cp1252 pipe raised UnicodeEncodeError on the failure lines; legacy answers whose notes name a non-answer; control gaps in C1, C11, R1-R3, W1-W2.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/fable5_dashok.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- Grok 4.7: an exported GXDOMAIN_BASELINE was honoured inside the hook; the loader kept the LAST count for a repeated key; the tooltip's denial and the unpinned inclusive cutoff.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/grok_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the 'identity' key is a CEILING over selected content (a byte-identical revert and a same-note replacement pass; 1,342 keys cover 1,356 answers) -- state the narrower guarantee or build provenance; three one-edit survivors (the tooltip clause restored after the checked prefix, `-u GXLEDGER` deleted, the loader's += made =); the v2 runner named the v1 controls; four claims to correct.  All applied in v3, the narrower guarantee stated in its words.", "ev": "regress/artifacts/dashokclass_20261016/f2/codex_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3: d_nonote dies on the baseline mismatch, not on the note (add the coherent two-edit form); the loader's summation pinned by nothing; R1 and R4 pinned prefixes only.  All applied in v3 (d_nonote2 killed by exactly C15 and C16; C17b; whole-string R1 and R4).", "ev": "regress/artifacts/dashokclass_20261016/f2/glm_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v2 receipts reproduce only with v2 under v1's name; six one-edit mutants pass all 35 (the tooltip tail, the malformed-date reason, which Q2 branch fired); three sentences overclaim; and its own pass-2 'note out of the key' was wrong.  All applied in v3.", "ev": "regress/artifacts/dashokclass_20261016/f2/fable5_dashokf2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: the note-only toll is this check's, not the ruling's; the Q2 comment's growth claim and 'can only shrink' survived; the raw-byte md5 pin reds a default Git-for-Windows checkout (measured the same hour: a fresh clone gives 89d1d370 for 06a3ffc6).  All applied in v3 (the pin folds CRLF; C18b).", "ev": "regress/artifacts/dashokclass_20261016/f2/grok_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2, the adjudication pass and the v3 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2, the adjudication pass and the v3 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2, the adjudication pass and the v3 pass, NOT FIRED: the kimi seat sat outside the roster."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2, the adjudication pass and the v3 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2, the adjudication pass and the v3 pass, NOT FIRED: minimax-m3 was given no packet; the roster, not a wall."}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] dashokclass closed by its landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v3_on_staged_v3.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 46/46 -- in particular R2 (only pend -> legacy, 670 cells), C15/C16 (the note in the key), C17b (a split baseline key sums), C18/C18b (the md5 pin, CRLF folded), C21 (a misshapen ledger is rc 2) and W4/W5 (exported overrides stripped) -- and does regress/artifacts/dashokclass_20261016/KILLTABLE_v3_staged.txt's runner still kill every pinned mutant?  Is the record (the checker's docstring, the Q2 comment, the CHANGELOG block, the bug-file closure) true of what shipped, and is the narrower guarantee -- a ceiling over selected content, not an entry identity -- stated where a reader will meet it?"
  state: "closed"
  state_note: "filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, \"pend\")`; HEAD's ledger carries 439 entries with d \"OK\" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS (\"OK\": \"ok\") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d \"OK\".  LOW, display only.\n\n[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line \"OK\": \"ok\", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs renders as one LEGACY class, its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at landing.  The 365 above counts OK cells only; the legacy class is 670 displayed cells (1,397 entries) at HEAD 8bf8b5a1."
  witness: "harness:regress/artifacts/dashokclass_20261016/RECEIPT_v3_on_staged_v3.txt -- R2: HEAD's renderer (gen_dashboard_before.py) shows 1,503 displayed cells in the seat-failure class and the landed one 833, the 670 moved now LEGACY with nothing else changing; C1-C22 and W1-W5 pin the entry-domain check; regress/artifacts/dashokclass_20261016/KILLTABLE_v3_staged.txt kills every pinned mutant (32/32 as recorded, one escape recorded as equivalent)"
```

### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (H12)

```diff
--- ../cxland/rulingsC_head.md
+++ rulingsC_dash_preview.md
@@ -41,7 +41,9 @@
 **F2 / D2 `dashokclass` -- UPHELD with the class re-keyed (Grok and Fable independently; Astra agrees on the semantics).**
 - Every mechanical sweep stays withdrawn (3/3).
 - The legacy class is keyed on the DOMAIN, not the spelling: every explicit `d` outside the four glyphs renders as one
-  residue class, labelled "legacy -- verdict unclassified" (Astra's wording), text kept, notes and hold/record precedence
+  residue class, labelled "legacy -- verdict unclassified" (adapted from Astra's "legacy OK — verdict unclassified";
+  this said "Astra's wording" until the 2026-10-17 dashokclass landing -- Fable 5.1 and GPT-6 Astra, adjudication pass),
+  text kept, notes and hold/record precedence
   preserved, counted as a FIFTH strip number so the strip sums to the entry total (5,150 at HEAD).  Keyed on `OK` alone
   it would leave 958 of 1,397 off-domain entries in the false `pend` class (Fable, `meas_C/okdomain_census.txt`: OK 439,
   other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7).
```

### 5d. the CHANGELOG block (a DRAFT: its v3-pass sentence is written from this pass's answers)

# `dashokclass` (2026-10-17): the dashboard's LEGACY class and the entry-domain check -- every explicit `d` outside ✓ ✕ ⏸ … renders as one class, "legacy -- verdict unclassified", instead of a seat failure (670 displayed cells at HEAD 8bf8b5a1), and precommit section Q2 holds the off-domain answers to a ceiling frozen at landing

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F2): no `OK` -> approval mapping, every mechanical sweep withdrawn, the class keyed on the DOMAIN of `d` rather than on
one spelling, and Astra's four completeness conditions for the forward check.

* `tools/pipeline/gen_dashboard.py`: an explicit `d` the four-glyph map does not know renders as class `legacy` -- its
  text kept, `?` for an explicit or whitespace-only blank, and a tooltip that opens (after a refused exemption's line, if
  any) with "legacy -- verdict unclassified: d = ... is outside ✓ ✕ ⏸ …; read the note for the outcome", because some
  legacy notes record real seat failures; the strip counts the class as a fifth number, so it sums to the entry total; the
  legend says what the class is.  A MISSING `d` is unchanged -- it still renders `…` (filed as `dashmissingd`).
* `tools/pipeline/check_entry_domain.py` and `entry_domain_baseline.json`, precommit section **Q2** (HARD): an ANSWER whose
  explicit `d` is outside the four passes only while, for its (row, phase, seat, date, `d`, sha1 of its note), the ledger
  holds no more such answers than the baseline froze at landing (1,342 keys, 1,356 answers), and only if it is dated
  before 2026-10-17.  **The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities
  cannot exceed their landing baseline** -- a byte-identical revert, a replacement differing only outside the six fields,
  and an edit outside them (`ev`, `grade`, `b`) all pass.  Editing a frozen entry's note means classifying it; that toll
  is this check's, not the ruling's.  The baseline is md5-pinned with CRLF folded (this machine's system git sets
  `core.autocrlf=true`; a fresh clone measured 89d1d370 for the committed 06a3ffc6); Q2 strips exported
  `GXDOMAIN_BASELINE` and `GXLEDGER`; a misshapen ledger or baseline is rc 2, never green.
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v3.py`, 46 rows: 46/46 on the landed files
  (`RECEIPT_v3_on_staged_v3.txt`), 37/46 on v2 (`RECEIPT_v3_on_staged_v2.txt`: the reworded output, the ledger-shape rc 2,
  the CRLF pin).  Kill table `run_mutants_v3.py`: 32/32 as recorded (`KILLTABLE_v3_staged.txt`); `d_notenone` escapes as
  an equivalent mutant (0 of 1,356 off-domain answers has an empty note), and `d_nonote2` is a deliberate two-edit DESIGN
  mutant (v1's key, coherently) killed by exactly C15 and C16.  v1 and v2's runners and receipts are kept; `run_mutants.py`
  now names `run_controls_v2.py` -- it named the v1 suite, which crashes on the 7-field baseline, so its 14/14 had
  reproduced only in a staging copy (Fable 5.1, GPT-6 Astra).
* Records: `dashokclass` closed (witness `harness:`, its REGRESS review HELD for the flagship); `dashmissingd` (LOW) filed --
  814 of 2,953 displayed answer cells show `…` because their latest answer has no `d`
  (`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt`); RULINGS_C's "Astra's wording" corrected to "adapted from".

**Pass 2** (`pass2/`, on v1): Astra SWC 3, GLM SWC 4, Fable SWC 7, Grok SWC 3 -- the count key's refill, the tooltip's
denial, the baseline guard, the unpinned cutoff, the cp1252 traceback, the honoured override.  **Adjudication pass** (`f2/`,
on v2, every finding shared with every seat): all four SWC 3 -- the "identity" is a ceiling (Astra), the one-edit survivors
(Astra, GLM, Fable, Grok), v2's runner naming the wrong controls (Fable, Astra), the CRLF pin (Grok; measured), the
note-only toll credited to the ruling (Grok); Fable 5.1 withdrew its own pass-2 "note out of the key".  **V3 pass**
(`v3pass/`): [to be written from the v3 pass's answers].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's
roster of 2026-10-16.

## 6. Questions -- verdict line first (`VERDICT: CLOSE` / `SHIP WITH CHANGES (n)` / `DO NOT SHIP`), then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2 (H1-H14): is my disposition right, and is the FIX right
   -- not only the finding?
2. **The repair as material.**  Read section 3's diff.  Is there a path where v3 does wrong what v2 did right -- a ledger
   or baseline a reader would call harmless that v3 now refuses, or a misshapen input it now passes?
3. **The kill table and the floor.**  Every pinned mutant is killed by the control its line names.  Is any killed for a
   reason OTHER than the one named?  Is there a one-edit mutant of the staged v3 checker, renderer or Q2 block, NOT in the
   table, that passes all 46 controls and breaks a ruled property?  If you find none, name the shapes you swept.
4. **The records (section 5).**  Is that text true of what ships?  Name any sentence that is false.
5. **Section 2b's questions**, each answered.
6. **Which of my accepted dispositions is wrong?**  There are 14 in section 2; name the count you checked.
