# ADJUDICATION PASS (§F2) -- `dashokclass`: the four seats' pass-2 findings, my dispositions, and the repair (v2)

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the dashboard generator) and a
pre-commit check over its JSON ledger.  READ-ONLY: write nothing to any project tree.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v2 files are STAGED under `regress/artifacts/dashokclass_20261016/staged_v2/`
(mirroring `tools/`), with `run_controls_v2.py`, `run_mutants.py`, `write_baseline.py`, `RECEIPT_v2_staged.txt` and
`KILLTABLE_staged.txt` beside them; the pass-2 answers are in `pass2/`.  Everything a packet-fed seat needs is inlined.

**This pass SHARES every seat's findings with every seat.**  Rule on your OWN findings harder than on anyone else's --
including whether the FIX I made is right, not only whether the finding was.  **The load-bearing question is section 6's:
which of my accepted dispositions is wrong?**

Open with your seat token `FABLE_DASHOKF2_20261016`, then ONE line: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`.

## 1. The pass-2 verdicts

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`pass2/codex_dashok.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (4)** (`pass2/glm_dashok.txt`).
* **Fable 5.1 -- SHIP WITH CHANGES (7)** (`pass2/fable5_dashok.md`; `agent_models.py`: clean claude-fable-5-1).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`pass2/grok_dashok.txt`).

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| D1 | Astra, Fable, Grok | the tooltip's "(not approval, not a seat failure)" is contradicted by legacy answers whose notes record real seat failures (`WALL` x3 per Astra/Grok; 73 answers / 20 displayed cells naming a non-answer, per Fable); the legend's "older entry" is not what the code tests | **FIXED**: tooltip "legacy -- verdict unclassified: d = 'X' is outside ✓ ✕ ⏸ …; read the note for the outcome"; legend "legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified (read the note; ? = an explicit blank)"; pinned by R1 (tooltip prefix) and R4 (legend) |
| D2 | all four | a per-(row, phase, seat, date, d) COUNT lets a converted entry's slot be REFILLED by a new answer (measured rc 0 by Astra and Fable) | **FIXED**: the key is now the entry's IDENTITY -- row, phase, seat, date, d and the sha1 of its NOTE; C15 pins the refill (rc 1) |
| D3 | Astra, Fable, Grok | a legitimate correction (a frozen entry's date) fails Q2 | **ACCEPTED as designed**: editing a frozen off-domain answer means giving it a glyph -- the ruling's own way out ("an OK becomes ✓ only when a reader rewrites that one entry").  **Under v2 this now includes a NOTE-only edit** (C16) -- see section 3 |
| D4 | Astra, Grok | a note edit can change `is_answer` (defanging the `ns16550` blank-d HELD record makes it an answer) | **COVERED by D2/D3**: it becomes an off-domain answer that is not frozen, so it fails and is normalised |
| D5 | all four | the baseline writer's placement is not a guard; the checker trusts the file | **FIXED**: the checker pins the baseline's md5 (`BASELINE_MD5 = 06a3ffc6...`) on its default path -- a re-freeze is a reviewed change to that constant in the same commit; the writer refuses to overwrite; C18 pins (one changed line -> rc 2) |
| D6 | Grok | an exported `GXDOMAIN_BASELINE` is honoured inside the hook | **FIXED**: section Q2 runs `env -u GXDOMAIN_BASELINE -u GXLEDGER python check_entry_domain.py`; W4 pins (an override that would admit a new entry is ignored) |
| D7 | Grok | the loader's dict keeps the LAST count for a repeated key | **FIXED**: counts are summed and each row's shape is validated (C17: string counts -> rc 2) |
| D8 | Astra, Fable, Grok | `CUTOFF` -> 2026-10-18 passes all 19 controls: the inclusive boundary was unpinned (C3 red for the baseline reason) | **FIXED**: C12 isolates the date test with FROZEN identities dated before / on / after the cutoff (0 / 1 / 1); the kill table kills `d_cutoff18` there |
| D9 | all four | dates compare lexically; a non-string date raised `TypeError` (rc 1 with a traceback) | **FIXED**: the cutoff applies only to an ISO `YYYY-MM-DD` prefix; non-string dates are compared by `repr`; a malformed date on a non-frozen entry is named in the reason; C19a/C19b pin (rc 1, no traceback) |
| D10 | Astra, Fable, Grok | `"d" not in x` -> `not x.get("d")` lets a new explicit blank pass | **PINNED**: C14 |
| D11 | Astra, Grok, Fable | control gaps: C1 asserted only rc; no strictly-after positive; C11 named "at least one"; R1 skipped the record glyph and the tooltip; R2 did not check the total; R3 counted a crash as a kill; W1/W2 never ran the real failure counter | **ALL FIXED** (C1 "1356 frozen", C2b, C11 all 1,356 named, R1 record glyph + tooltip, R2 total = entry count and legacy = the ledger's off-domain count, R3 requires a successful render, W1-W4 count failures) |
| D12 | Fable | under the precommit's cp1252 stdout the checker's failure lines raise `UnicodeEncodeError` | **FIXED**: `sys.stdout.reconfigure(errors="backslashreplace")`; the controls run the checker WITHOUT `PYTHONIOENCODING`; C20 pins (a non-ASCII `d`, rc 1, no traceback) |
| D13 | GLM | rc 2 through the gate untested; no escapable-`d` fixture; no refill control; no `?` legend line | **FIXED**: W3, R1b, C15, the legend line |
| D14 | Fable | "Astra's wording" is Astra's phrase minus "OK" | **CORRECTED** in the records |
| D15 | Astra, Fable | the packet's 5,167 entries and R2 census were one commit stale | **CORRECTED**: HEAD 8bf8b5a1 has 5,177 entries; v2's receipt is of that ledger |
| D16 | Grok, Fable | the landing must regenerate `matrix.html` with the new renderer (section Q) | **IN THE COMMIT PLAN** |
| D17 | all four | "Q2 can only fail on an entry added after it lands", "cannot retro-fail", "this class can only shrink" are false | **CORRECTED**: the docstring and the Q2 comment say it fails on a new entry AND on an old one edited; the GRANDFATHERED population only shrinks, and the dashboard's legacy count is a different number |
| D18 | GLM | does the tooltip insert reach hold/record cells? | **SETTLED by reading** `cell()`: the hold and record branches return before `tip` is built |
| D19 | Fable | five answers carry `✗` (U+2717), a lookalike of the objection glyph | **NOTED** for a reader's one-at-a-time rewrite; no sweep (ruled) |
| D20 | Fable, Grok | on a refused stage exemption, that line opens the tooltip before the legacy line | **KEPT**: the refusal is the louder fact |

## 3. Disagreements, both sides in their own words

* **The note IN the key.**  All four seats on pass 2: *"Leaving the note out is right for ordinary note corrections"*
  (Astra); *"note-in-key would re-arm every correction/defang ... the refill hole is the price and the smaller evil"* (GLM);
  *"Note out of the key: right"* (Fable); *"Leaving the note out is right for a wording fix"* (Grok).  **I put it in**, to
  close the refill (D2): under a count key the two edits -- "convert X and add Y with X's tuple" and "correct X's note"
  -- are indistinguishable, so one of them must pass or both must fail.  I chose both-fail; the price is that a note-only
  correction of a frozen off-domain answer now needs a glyph (C16).  **Rule on this.**
* **The baseline guard.**  Fable: a `cmp` of the working baseline against `HEAD:` inside Q2 (`bad` on any difference).
  GLM: pin the total (1,356).  Astra: "baseline changes still need a protected, reviewed provenance rule".  **I chose an
  md5 pin in the checker**: it detects every unreviewed change, as the `cmp` would, and still lets a REVIEWED re-freeze
  land in one commit (the constant changes with the file); a `cmp` against HEAD would refuse every re-freeze for ever.

## 4. The repair -- v1 (pass 2) -> v2, `git diff --no-index` of the staged files

### 4a. check_entry_domain.py

```diff
diff --git a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/check_entry_domain.py b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/pipeline/check_entry_domain.py
index 9350583c..8e64c72c 100644
--- a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/check_entry_domain.py
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/pipeline/check_entry_domain.py
@@ -1,78 +1,115 @@
 #!/usr/bin/env python3
-"""A NEW LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR NONE.  2026-10-16, ledger `dashokclass`.
-
-THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer --
-or no `d` at all (the renderer's default is …).  MEASURED when this landed: 1,397 ledger entries carried an explicit
-`d` OUTSIDE the four -- OK 439, other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7 (Fable
-5.1, regress/artifacts/adj_20261016/fable5/meas_C/okdomain_census.txt) -- and until the same commit every one of them
-that reached a cell rendered in the SEAT-FAILURE class, because the renderer's fallback was `pend`.  The renderer now
-shows them as one residue class, "legacy -- verdict unclassified" (an explicit `d` it cannot classify is neither
-approval nor a seat failure); this check stops that population GROWING.  Ruled by Fable 5.1, GPT-6 Astra and Grok 4.7
-(regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old entries is withdrawn --
-an OK becomes ✓ or anything else only when a reader rewrites that one entry.
-
-ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt), each held here:
-  1. a MISSING `d` passes -- it renders as … ;
+"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED.
+2026-10-16, ledger `dashokclass`; precommit section Q2.
+
+THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer -- or no
+`d` at all (the renderer's default is …).  MEASURED when this landed (HEAD 8bf8b5a1): 5,177 entries, 1,397 with an explicit
+`d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
+2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
+them as one residue class, "legacy -- verdict unclassified", and this check keeps NEW ones from appearing.  Ruled by Fable
+5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old
+entries is withdrawn -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.
+
+ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt):
+  1. a MISSING `d` passes -- it renders as … (an explicit blank does NOT: it is an off-domain value);
   2. an entry that is not an ANSWER passes whatever its `d` -- holds, annotations, records (stage_tokens.is_answer);
   3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
-  4. the controls carry a POSITIVE row (a valid glyph after the cutoff passes) beside the negatives and a mutant with
-     the baseline removed.
+  4. the controls carry POSITIVE rows (a valid glyph on and after the cutoff passes) beside the negatives.
 
-GRANDFATHERING IS AGAINST THE EXISTING ENTRIES, NOT AGAINST A DATE (the ruling's amendment: a date-only cutoff cannot
-stop a back-dated or an undated new entry).  An off-domain answer passes only if it is dated BEFORE `CUTOFF` AND its
-(row, phase, seat, date, d) tuple is within the count frozen in `entry_domain_baseline.json` -- the off-domain answers
-present when this check landed, written once by regress/artifacts/dashokclass_20261016/write_baseline.py and never by
-this file.  So a back-dated or undated addition exceeds its tuple's frozen count and fails, and so does any off-domain
-answer dated on or after CUTOFF.  Rewriting a grandfathered entry's `d` to a glyph only shrinks the population.
+GRANDFATHERING IS BY ENTRY IDENTITY, NOT BY DATE AND NOT BY COUNT.  An off-domain answer passes only if it is IDENTICAL --
+row, phase, seat, date, `d` and NOTE (by its sha1) -- to one frozen in `entry_domain_baseline.json` when this check landed,
+and is not dated on or after CUTOFF.  So a new entry fails, a back-dated or undated one fails, a duplicate fails, and an old
+one EDITED in any of those fields fails: editing such an entry means giving it a glyph, which is the ruling's way out.
+(Pass 2 of this check, 2026-10-16: a per-(row, phase, seat, date, d) COUNT let a converted entry's allowance be refilled by
+a new answer, and let a note edit turn a record into an un-normalised answer -- GPT-6 Astra and GLM 5.3; the note is in the
+key for that reason.)  The grandfathered population can only shrink.  That is NOT a claim about the dashboard's legacy
+count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that reappears when a
+newer answer in its cell is removed.
+
+THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`): re-freezing it is a reviewed decision, made by changing that constant in
+the same commit with the reason, never by re-running the one-time writer
+(regress/artifacts/dashokclass_20261016/write_baseline.py).  A GXDOMAIN_BASELINE override skips the pin, for the controls.
+Dates are compared as ISO `YYYY-MM-DD` prefixes; a date in any other form is never "on or after the cutoff", so a malformed
+date passes only on an identical frozen entry (none exists).
 
 Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
-Exit: 0 clean; 1 a new off-domain answer (each named); 2 apparatus failure (baseline or ledger unreadable)."""
-import collections, io, json, os, sys
+Exit: 0 clean; 1 an off-domain answer that is not a frozen entry (each named); 2 apparatus failure (baseline or ledger
+unreadable or misshapen, or the baseline's md5 is not the pinned one)."""
+import collections, hashlib, io, json, os, re, sys
 
 HERE = os.path.dirname(os.path.abspath(__file__))
 sys.path.insert(0, HERE)
 import stage_tokens as st  # noqa: E402
 
 LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
-BASELINE = os.environ.get("GXDOMAIN_BASELINE") or os.path.join(HERE, "entry_domain_baseline.json")
+DEFAULT_BASELINE = os.path.join(HERE, "entry_domain_baseline.json")
+BASELINE = os.environ.get("GXDOMAIN_BASELINE") or DEFAULT_BASELINE
+BASELINE_MD5 = "06a3ffc6929be628c8254fe4e818ee99"      # the md5 of entry_domain_baseline.json as frozen; change only by a reviewed re-freeze
 DOMAIN = ("✓", "✕", "⏸", "…")      # gen_dashboard.py's D_CLASS keys; the two must agree
 CUTOFF = "2026-10-17"               # inclusive: an off-domain answer dated on or after it always fails
+ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")
+
+
+def note_sha(x):
+    return hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]
+
+
+def date_str(x):
+    v = x.get("date")
+    return v if isinstance(v, str) else ("" if v is None else repr(v))
 
 
 def off_domain_answers(ledger):
-    """(row, phase, seat, date, d) for every ANSWER entry carrying an explicit `d` outside DOMAIN."""
+    """(row, phase, seat, date, d, note_sha) for every ANSWER entry carrying an explicit `d` outside DOMAIN."""
     out = []
     for r in ledger.get("rows", []):
         for x in r.get("entries", []):
             if "d" not in x or x["d"] in DOMAIN or not st.is_answer(x):
                 continue
-            out.append((r.get("id"), x.get("phase") or "", x.get("seat") or "", x.get("date") or "", str(x["d"])))
+            out.append((str(r.get("id")), str(x.get("phase") or ""), str(x.get("seat") or ""), date_str(x), str(x["d"]),
+                        note_sha(x)))
     return out
 
 
 def main():
+    #  precommit runs this with stdout on a PIPE, which Windows python opens as cp1252: a glyph or a non-ASCII `d` in the
+    #  failure lines raised UnicodeEncodeError and buried the instruction under a traceback (Fable 5.1, pass 2, measured)
+    if hasattr(sys.stdout, "reconfigure"):
+        sys.stdout.reconfigure(errors="backslashreplace")
     try:
         ledger = json.load(io.open(LEDGER, encoding="utf-8"))
     except Exception as ex:
         print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2
     try:
-        base = collections.Counter({tuple(k[:5]): k[5] for k in json.load(io.open(BASELINE, encoding="utf-8"))})
+        raw = open(BASELINE, "rb").read()
+        if BASELINE == DEFAULT_BASELINE and hashlib.md5(raw).hexdigest() != BASELINE_MD5:
+            print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
+                  "in the same commit, with its reason" % (BASELINE, hashlib.md5(raw).hexdigest(), BASELINE_MD5)); return 2
+        base = collections.Counter()
+        for k in json.loads(raw.decode("utf-8")):
+            if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
+                    and k[6] > 0):
+                raise ValueError("baseline row %r is not [row, phase, seat, date, d, note_sha, count]" % (k,))
+            base[tuple(k[:6])] += k[6]
     except Exception as ex:
-        print("APPARATUS FAIL: baseline unreadable: %s (%s)" % (BASELINE, ex)); return 2
+        print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
     cur = off_domain_answers(ledger)
     seen = collections.Counter()
     bad = []
     for t in cur:
         seen[t] += 1
-        if t[3] >= CUTOFF:
+        if ISO.match(t[3]) and t[3][:10] >= CUTOFF:
             bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
         elif seen[t] > base[t]:
-            bad.append((t, "not among the %d grandfathered entries of this tuple" % base[t]))
-    print("entry domain: %d off-domain answer entries; %d grandfathered (baseline %d); cutoff %s inclusive"
+            why = "not identical to a frozen entry -- a new one, a duplicate, or an old one edited (give it a glyph)"
+            if t[3] and not ISO.match(t[3]):
+                why += "; its date is not ISO YYYY-MM-DD"
+            bad.append((t, why))
+    print("entry domain: %d off-domain answer entries; %d frozen (baseline %d); cutoff %s inclusive"
           % (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))
-    for (row, phase, seat, date, d), why in bad:
-        print("  NEW OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r -- %s"
-              % (row, phase, seat, date or "(none)", d, why))
+    for (row, phase, seat, date, d, ns), why in bad:
+        print("  OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s"
+              % (row, phase, seat, date or "(none)", d, ns, why))
     if bad:
         print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"
               % " ".join(DOMAIN))
```

### 4b. gen_dashboard.py

```diff
diff --git a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/gen_dashboard.py b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/pipeline/gen_dashboard.py
index 4d55eedc..e6732baa 100644
--- a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/gen_dashboard.py
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/pipeline/gen_dashboard.py
@@ -78,7 +78,9 @@ D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
 #  365 displayed cells -- all read as "no answer / seat failure".  Mapping "OK" to `ok` was REJECTED (it canonises one
 #  off-domain spelling as approval); every mechanical sweep of the entries was withdrawn.  So an explicit `d` the map does
 #  not know renders as ONE residue class, LEGACY, keeping its text, with the reason first in its tooltip; a MISSING `d` is
-#  still `…`.  check_entry_domain.py (precommit Q2) stops new off-domain answers, so this class can only shrink.
+#  still `…`, an explicit blank shows `?`.  The class says only that the `d` is unclassified -- three legacy cells (`WALL`)
+#  record real seat failures in their notes, so the tooltip sends the reader to the note rather than denying either reading
+#  (GPT-6 Astra, pass 2).  check_entry_domain.py (precommit Q2) refuses any off-domain ANSWER not frozen when it landed.
 LEGACY = "legacy"
 e = lambda t: html.escape(str(t), quote=True)
 
@@ -173,7 +175,7 @@ def cell(row, phase, seat):
     if ent.get("ev"):
         tip.append("evidence: " + ent["ev"])
     if cls == LEGACY:
-        tip.insert(0, "legacy -- verdict unclassified: d = %r is none of ✓ ✕ ⏸ … (not approval, not a seat failure)" % d)
+        tip.insert(0, "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d)
     #  #534 F2 pass (codex): both of these lived only in the no-answer branch, so an ANSWER cell hid
     #  them -- a refused RE_READ rendered calm, and a record filed after the seat's answer vanished.
     if st.exempts_stage(ent):
@@ -431,7 +433,7 @@ footer code {{ color:var(--ink); }}
   <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
   <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
   <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
-  <span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- an older entry's verdict text outside ✓ ✕ ⏸ … (unclassified: not approval, not a seat failure; hover for it)</span>
+  <span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside ✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = an explicit blank)</span>
   <span><span class="g" style="color:var(--muted)">∅</span> a record, not an answer (exemption or main-loop note; hover for why)</span>
   <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
   <span><sup class="b">A</sup> the author did this review (shown)</span>
```

### 4c. precommit_check.sh, section Q2

```diff
diff --git a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/precommit_check.sh b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/precommit_check.sh
index 48a09557..321af245 100644
--- a/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/precommit_check.sh
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged_v2/tools/precommit_check.sh
@@ -493,23 +493,27 @@ else
 fi
 
 #  ---- Q2 --------------------------------------------------------------------------
-#  A NEW LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR NONE.  2026-10-16, ledger `dashokclass`
+#  A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES, OR IS A FROZEN LEGACY ENTRY.  2026-10-16, ledger `dashokclass`
 #  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
 #  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
 #  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section keeps that class from
-#  growing.  Grandfathering is against the EXISTING ENTRIES (a frozen baseline), not a date, because a date-only
-#  cutoff cannot stop a back-dated or undated addition -- check_entry_domain.py's docstring says how.  HARD: it is
-#  forward-only by construction, so it cannot retro-fail anything that was already there.
-say ""; say "Q2. a new ledger answer carries a d the dashboard classifies"
+#  growing.  Grandfathering is by ENTRY IDENTITY against a frozen, md5-pinned baseline -- row, phase, seat, date, d and
+#  note -- not by a date (a date-only cutoff cannot stop a back-dated or undated addition) and not by a per-tuple count
+#  (a converted entry's allowance could be refilled; pass 2).  HARD.  It fails on a NEW off-domain answer and on an OLD
+#  one edited in any of those fields: editing such an entry means giving it a glyph, the ruling's way out.  It reds
+#  (rc 2) when the baseline is unreadable or its md5 is not the pinned one, never silently green.
+say ""; say "Q2. a ledger answer carries a d the dashboard classifies, or is a frozen legacy entry"
 CED=$_HERE/pipeline/check_entry_domain.py
 if [ ! -f "$CED" ]; then
 	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
 else
-	_ced=$(python "$CED" 2>&1); _cedrc=$?
+	#  the overrides are for the controls, never for a commit: an exported GXDOMAIN_BASELINE would swap in another baseline
+	#  and skip the md5 pin (Grok 4.7, pass 2), so the section checks the real ledger against the pinned baseline
+	_ced=$(env -u GXDOMAIN_BASELINE -u GXLEDGER python "$CED" 2>&1); _cedrc=$?
 	if [ $_cedrc -eq 0 ]; then
 		good "$(printf '%s\n' "$_ced" | head -1)"
 	elif [ $_cedrc -eq 1 ]; then
-		bad "a NEW ledger answer carries a d outside the four glyphs:"
+		bad "an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edited):"
 		printf '%s\n' "$_ced" | sed 's/^/          /'
 	else
 		bad "check_entry_domain.py could not run (rc $_cedrc): $(printf '%s\n' "$_ced" | head -1)"
```

## 5. The receipts -- run in a staging copy of HEAD 8bf8b5a1 with the v2 files in place

### 5a. RECEIPT_v2_staged.txt (run_controls_v2.py), verbatim

```
# dashokclass controls (v2) -- checker 111bcac0 | renderer 2565a4a0 | precommit a96dad35
C1   shipped ledger, shipped baseline, md5 pin live                               ok  rc 0: entry domain: 1356 off-domain answer entries; 1356 frozen (baseline 1356); cutoff 2026-10-17 inclusive
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
C9   an identical copy of a frozen entry (alphactxfail assess codex 2026-09-08 'y') ok  rc 1
C10  a frozen entry rewritten to a glyph                                          ok  rc 0
C15  REFILL: the converted entry's (row, phase, seat, date, d) reused             ok  rc 1
C16  a frozen entry's note edited, d left off-domain                              ok  rc 1
C11  baseline emptied: every shipped off-domain answer named                      ok  rc 1, 1356 of 1356 named
C12  cutoff isolated: a FROZEN identity dated 2026-10-16 (before)                 ok  rc 0 (want 0)
C12  cutoff isolated: a FROZEN identity dated 2026-10-17 (on)                     ok  rc 1 (want 1)
C12  cutoff isolated: a FROZEN identity dated 2026-10-18 (after)                  ok  rc 1 (want 1)
C13  an unreadable baseline                                                       ok  rc 2
C17  a misshapen baseline (counts as strings)                                     ok  rc 2
C18  md5 pin: one baseline line changed -> 2, unchanged -> 0                      ok  changed rc 2, unchanged rc 0
R1   fixture row: class, glyph and legacy tooltip per seat                        ok  9 cells; mismatches []; legacy tip ok
R1b  an escapable d renders escaped                                               ok  escape cell ('legacy', '&lt;b&gt;&amp;')
R4   the legend carries the legacy line                                           ok  legend found
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy; strip sums, legacy = the ledger's count ok  before {'bad': 17, 'hold': 53, 'none': 29472, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 53, 'legacy': 670, 'none': 29472, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2042… 1397 legacy · 5177 in all' | ledger 5177 entries, 1397 off-domain
R3   MUTANT ok renders and fails its check                                        ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG
R3   MUTANT pend renders and fails its check                                      ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]; legacy tip WRONG
R3   MUTANT noescape renders and fails its check                                  ok  escape cell ('legacy', '<b>&')
W1   Q2 on the shipped ledger                                                     ok  GOOD entry domain: 1356 off-domain answer entries; 1356 frozen (baseline 1356); cutoff 202 | failures 0
W2   Q2 with a new off-domain answer                                              ok  BAD an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edi | failures 1
W3   Q2 with the baseline absent (rc 2 path)                                      ok  BAD check_entry_domain.py could not run (rc 2): APPARATUS FAIL: baseline unreadable or mis | failures 1
W4   Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry          ok  BAD an off-domain ledger answer is not a frozen legacy entry (a new one, or an old one edi | failures 1
DASHOKCLASS CONTROLS: 35/35 as expected
DASHOKCLASS_CONTROLS_DONE
```

### 5b. KILLTABLE_staged.txt (run_mutants.py), verbatim

```
# dashokclass kill table
BASE        DASHOKCLASS CONTROLS: 35/35 as expected
d_cutoff18  34/35   killed by: C12                                               [C12]
d_blank     32/35   killed by: C1 C11 C14                                        [C14]
d_nonote    26/35   killed by: C1 C10 C12 C18 C2 C2b C7 C8 W1                    [C1]
d_nomd5     34/35   killed by: C18                                               [C18]
d_nodate    33/35   killed by: C12                                               [C12]
d_noreconf  26/35   killed by: C11 C14 C19a C19b C20 C3 C4 C5 C6                 [C20]
r_nolegend  34/35   killed by: R4                                                [R4]
r_ok        30/35   killed by: R1 R1b R2 R3                                      [R1]
r_pend      30/35   killed by: R1 R1b R2 R3                                      [R1]
r_noescape  33/35   killed by: R1b R3                                            [R1b]
r_strip     34/35   killed by: R2                                                [R2]
w_envkeep   34/35   killed by: W4                                                [W4]
w_collapse  34/35   killed by: W3                                                [W3]
w_subshell  33/35   killed by: W2 W4                                             [W2]
KILL TABLE: 14/14 killed as named
DASHOKCLASS_MUTANTS_DONE
```

## 6. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **Your own findings.**  For each finding of yours in section 2: is my disposition right, and is the FIX right?
2. **The repair as material.**  Read section 4's diffs (v1 -> v2) and section 5's receipts.  Is there a path where v2
   now does something wrong that v1 did right -- for example a ledger edit a reader would call harmless that Q2 now refuses
   (beyond the note-only correction section 3 names), or an entry the identity key cannot tell apart from another?
3. **The kill table.**  Every mutant is killed by the control its line names.  Is any killed for a reason OTHER than the
   one named?  Is there a one-edit mutant of the v2 checker, renderer or Q2 block, NOT in the table, that passes all 35
   controls and breaks a ruled property?
4. **The note in the key** (section 3, first bullet): keep it, or take it out and accept the refill?  If out, what
   closes the refill instead?
5. **The baseline guard** (section 3, second bullet): md5 pin, `cmp` against HEAD, or a pinned total?
6. **Which of my accepted dispositions is wrong?**  Name the count you checked (there are 20 findings above).
