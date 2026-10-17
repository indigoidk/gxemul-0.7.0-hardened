
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

### 4a. `run_controls_v5.py`, WHOLE (its docstring is the CONTRACT and the row list)

```python
     1	#!/usr/bin/env python3
     2	"""Controls for `dashokclass` (2026-10-17, v5 after the v4 pass): gen_dashboard.py's LEGACY class, check_entry_domain.py (a
     3	ceiling over selected content, md5-pinned baseline) and its precommit section Q2.  Everything runs on temp copies and fixture
     4	ledgers; nothing in the tree is written.  Exit 0 only if every control holds.  CTL_CHECKER / CTL_RENDER / CTL_PRECOMMIT override
     5	the three files under test (run_mutants_v5.py and the staged runs use them); the defaults are the tree's.
     6	
     7	  THE CONTRACT (v5) -- the v4 pass (Fable 5.1, GPT-6 Astra, Grok 4.7; GLM 5.3 read the packet) measured 21 one-edit mutants
     8	  passing all 72 v4 controls, 15 of them at decisions v4 listed as pinned.  They share one shape (Fable 5.1): each pin tested
     9	  ONE edge of its decision -- the trailing end of a key field, the first literal line, a number but not its label, a substring
    10	  but not the whole tooltip, one branch of three.  So v5 rows the DUAL edge of every pin: for each decision below, the edit its
    11	  v4 pin would not see.  The decisions are the checker's, the renderer's and Q2's, read from the three files.
    12	    checker  ledger shape: an object, `rows' PRESENT and a list, row objects, entries   C21a-f, C21i (rows absent: {} and
    13	             lists, entry objects                                                       {"seats": []}); C23 (not JSON)
    14	             baseline shape: a list of [six strings, a positive int] -- exactly seven   C13, C17 (a string count), C17b (a split
    15	             fields, each of the six a str, the count an int and not a bool, > 0        key sums), C17c-i (eight fields, a true
    16	                                                                                        count, -1, 0, 1.0, a numeric first field,
    17	                                                                                        a numeric note sha), C21g (an object)
    18	             md5 pin on the default path, CRLF folded; overrides skip it                C18, C18b; C11, C12, C17 (override)
    19	             the selection: an explicit d, EXACT membership in the four, an ANSWER     C7 (no d), C14 (blank), C26 (null), C28
    20	                                                                                        (a padded ✓), C2/C2b/C2c/C2d (each glyph,
    21	                                                                                        C2c/C2d isolated), C8 (hold), C24 (a
    22	                                                                                        record, isolated)
    23	             the key -- row, phase, seat, date, d, note -- byte for byte, at BOTH      C25a-k (the trailing end, case, a row
    24	             ends; str() of d                                                           move), C25l-r (the leading end; a row id
    25	                                                                                        with a trailing or a leading space);
    26	                                                                                        C15/C16 (the note); C26b (a list d)
    27	             the ceiling: a copy fails, a converted entry's allowance cannot refill     C9, C10, C15; d_nonote2 (design mutant)
    28	             the cutoff: inclusive; a date counts only when the ISO shape OPENS it     C3, C4, C12 (isolated: before / on /
    29	                                                                                        after / far, and C12s a MATCHED identity
    30	                                                                                        dated 2026-10-17T12:00:00), C19a/b
    31	             output: cp1252-safe; the summary line WHOLE (its baseline number is the   C20; C1, C11, C12 (the summary exact --
    32	             frozen total, not the within-count); each refusal line WHOLE --           at C12-on the two numbers differ);
    33	             identifiers in order, its reason; the hint                                C3, C6, C9, C19a (the refusal line
    34	                                                                                        exact); C11 (the hint)
    35	             the glyph set: ONE binding of DOMAIN and of D_CLASS, each the four         C27 (an ast walk of both files: every
    36	                                                                                        store of the name, its value)
    37	    renderer the class: EXACT membership in the four -> its class, else legacy, on     R1 (per seat), R1h (padded), R1n (null),
    38	             the answer a cell shows                                                    R3
    39	             the class line opens EVERY legacy cell's tooltip -- the WHOLE tooltip      R1 (OK), R1g (every simple legacy d,
    40	                                                                                        null included), R1e (a record beside it),
    41	                                                                                        R1f (a refused exemption first)
    42	             the glyph: escaped; `?` for a blank or whitespace-only d (any whitespace)  R1b, R1d (space, tab, newline, NBSP)
    43	             the strip: each number the ledger's own count by EXACT membership, and     R2 (the shipped ledger: the whole strip
    44	             its labels                                                                 string), R2b (the fixture ledger, whose
    45	                                                                                        padded ✓ counts legacy)
    46	             the legend line; the two CSS rules the class adds                          R4; R5
    47	    Q2       the branches: rc 0 GOOD, rc 1 BAD with the refusal named, ANY other       W1, W2, W3 (rc 2), W7 (rc 7, its message
    48	             status BAD "could not run" with the checker's first line, stderr included  on stderr), W8 (python absent: rc 127)
    49	             the checker absent -> BAD                                                  W6
    50	             an exported GXDOMAIN_BASELINE / GXLEDGER stripped                          W4, W5
    51	    DISCLOSED, each with its reason:
    52	      a sha1-16 collision -- a note passing as a FROZEN entry's note is a fixed-target second preimage, about 2^64 work; an
    53	        arbitrary collision between two new notes (about 2^32, birthday) passes nothing, since neither matches a frozen key
    54	        (GPT-6 Astra, v4 pass: the two figures are different searches);
    55	      `ISO.match' -> `ISO.search': equivalent, the pattern being anchored with `^';
    56	      case-folding or whitespace-stripping INSIDE a field (C25 edits both ends; nothing edits the middle);
    57	      the production good/bad reporters and the section's final exit: the W rows use counting stand-ins (the staged
    58	        precommit's `bad' increments `fail', and both final exits return 1 when it is positive -- read, Fable 5.1, v4 pass);
    59	      the Q2 section header: `say' is stubbed in the W block, and it is display only.
    60	    A fold of d, or a fold or strip of the NOTE, is one-sided on this ledger -- the baseline holds raw values and only the
    61	    note's sha -- so it dies on C1: some frozen keys stop matching (on HEAD's ledger the d fold changes 1,100 of the 1,356
    62	    frozen answers' keys, the note strip 2, the note fold 1,352; measured by Fable 5.1, v4 pass).  The coherent fold of d is the
    63	    two-edit design mutant d_dfold2, killed by C25d.
    64	
    65	  CHECKER (Astra's four conditions, the ruling's grandfathering amendment, pass 2's, the adjudication pass's and the v3 and
    66	  v4 passes' findings):
    67	    C1   shipped ledger, shipped baseline (md5 pin live): rc 0 and the summary line EXACTLY
    68	    C2 / C2b  an answer ON / AFTER the cutoff with a valid glyph (positive)                       -> 0 / 0
    69	    C2c / C2d  an answer after the cutoff with ⏸ / with …, in a ledger holding ONLY that entry (positive) -> 0 / 0
    70	    C3   an answer ON the cutoff with "OK" (inclusive) -- its refusal line EXACTLY                  -> 1
    71	    C4   an answer AFTER the cutoff with "OK"                                                       -> 1
    72	    C5   a new answer dated BEFORE the cutoff with "OK" (back-dated)                                -> 1
    73	    C6   an UNDATED answer with "N/A" -- its refusal line EXACTLY (date "(none)", no ISO clause)    -> 1
    74	    C7   an answer after the cutoff with NO `d`                                                     -> 0
    75	    C8   a HELD marker after the cutoff with d "HELD" (not an answer)                               -> 0
    76	    C9   an identical copy of a frozen entry -- its refusal line EXACTLY                            -> 1
    77	    C10  a frozen entry rewritten to a glyph (the population shrinks)                               -> 0
    78	    C11  the baseline emptied (override): every shipped off-domain answer named, the summary EXACTLY, the hint -> 1
    79	    C12  the cutoff ISOLATED: a fixture baseline holding an identity dated before / on / after / far   -> 0 / 1 / 1 / 1,
    80	         each with its summary line EXACTLY (on/after/far: within = baseline - 1)
    81	    C12s a MATCHED identity dated "2026-10-17T12:00:00" (the ISO shape opens it)                    -> 1
    82	    C13  an unreadable baseline (override)                                                          -> 2
    83	    C14  a new answer with an explicit BLANK d                                                      -> 1
    84	    C15  REFILL: a frozen entry rewritten to a glyph, plus a new answer reusing its (row, phase, seat, date, d) -> 1
    85	    C16  a frozen entry's NOTE edited, its d left off-domain                                        -> 1
    86	    C17  a misshapen baseline (override; counts as strings)                                         -> 2
    87	    C17b a key SPLIT across two baseline rows (override) sums                                       -> 0
    88	    C17c-i  the shipped baseline plus ONE misshapen row (override): eight fields; a count of true; -1; 0; 1.0; a numeric
    89	         first field; a numeric note sha                                                            -> 2 each
    90	    C18  the md5 PIN: a temp copy of the pipeline with one baseline line changed -> 2; unchanged -> 0
    91	    C18b the same baseline with CRLF line endings passes the pin                                    -> 0
    92	    C19  malformed dates on new answers: "10/18/2026" (its refusal line EXACTLY) and a number -- rc 1, no traceback,
    93	         the date NAMED as not ISO                                                                  -> 1 / 1
    94	    C20  a new answer whose d is non-ASCII, under the precommit's cp1252 pipe -- rc 1, no traceback   -> 1
    95	    C21  misshapen LEDGERS -- {"rows": null}, a row that is not an object, a list, {"rows": {}}, a string entry, entries
    96	         that are an object; C21i {} and {"seats": []} (rows absent); C21g a baseline that is an object (override); C21h a
    97	         note that is a number (it raises inside stage_tokens.is_answer -- the walk's except-arm)  -> 2 each, no traceback
    98	    C22  a frozen entry's `ev` edited -- outside the six fields (positive)                          -> 0
    99	    C23  a ledger that is not JSON                                                                  -> 2
   100	    C24  a non-answer RECORD (NOTSEAT) after the cutoff with d "OK", in a ledger holding ONLY it      -> 0
   101	    C25  a frozen entry with ONE key field edited by its least visible change: a-k the date suffixed / a trailing space,
   102	         d trailing space / case, note trailing space / case, seat trailing space / case, phase trailing space / case,
   103	         the entry moved to another row; l-r the entry moved to a row whose id carries a trailing space, the date, d,
   104	         note, seat and phase each with a LEADING space, the entry moved to a row whose id carries a leading space -> 1 each
   105	    C26  a new answer with an explicit "d": null                                                     -> 1
   106	    C26b a new answer whose d is a LIST -- rc 1, no traceback (the key takes str() of d)              -> 1
   107	    C27  DOMAIN and D_CLASS: ONE binding each (an ast walk -- a second assignment is the effective one), each exactly ✓ ✕ ⏸ …
   108	    C28  a new answer BEFORE the cutoff with a PADDED glyph " ✓" (outside the four, as the renderer says) -> 1
   109	  RENDERER:
   110	    R1   a fixture row, one entry per seat: class AND glyph per cell, and the legacy cell's tooltip EXACTLY
   111	    R1b  an escapable `d` ("<b>&") renders escaped
   112	    R1c  the fixture page says neither "not approval" nor "not a seat failure" anywhere
   113	    R1d  a whitespace-only `d` -- a space, a tab, a newline, an NBSP -- shows `?`
   114	    R1e  an answer cell with a non-answer record beside it: its WHOLE tooltip -- class line, date, note, the record line
   115	    R1f  a legacy answer carrying a refused stage exemption: the refusal line first, then the class line, exactly
   116	    R1g  EVERY simple legacy cell's WHOLE tooltip -- the class line for ITS d ("OK", "", "N/A", "<b>&", " ", " ✓", "\t",
   117	         null), the date, the note
   118	    R1h  a padded glyph " ✓" renders legacy, not ok
   119	    R1n  an explicit "d": null renders legacy with the glyph "None", not …
   120	    R2   the shipped ledger, BEFORE vs AFTER: only pend -> legacy moves; the strip string EXACTLY -- each number the ledger's
   121	         own count by exact membership, and its labels
   122	    R2b  the FIXTURE page's strip EXACTLY, against the fixture's own counts (its padded ✓ and null count legacy)
   123	    R3   MUTANT renderers (fallback -> ok, -> pend; the escape dropped) must RENDER and then fail R1 / R1b -- a crash is not
   124	         a kill
   125	    R4   the legend carries the legacy line EXACTLY
   126	    R5   the page carries the two CSS rules the class adds, EXACTLY (the legacy outline; the glyph's muted italic 11px)
   127	  WIRING (section Q2, extracted from precommit_check.sh and run with reporters that COUNT failures; each first line must also
   128	  carry its BRANCH's own words):
   129	    W1   the shipped ledger                    -> GOOD, failures 0
   130	    W2   a new off-domain answer               -> BAD "beyond the frozen legacy ceiling", the entry named, failures >= 1
   131	    W3   the baseline absent (rc 2 path)       -> BAD "could not run (rc 2)", failures >= 1
   132	    W4   an exported GXDOMAIN_BASELINE that would admit a new entry is IGNORED -> BAD, failures >= 1
   133	    W5   an exported GXLEDGER naming a CLEAN ledger is IGNORED; the bad default ledger is read -> BAD, failures >= 1
   134	    W6   the checker ABSENT from the fake tools dir                -> BAD "MISSING", failures >= 1
   135	    W7   a checker that exits 7 with its message on STDERR -> BAD "could not run (rc 7): <that message>", failures >= 1
   136	    W8   python ABSENT from PATH (a launch failure)               -> BAD "could not run (rc 127)", failures >= 1
   137	"""
   138	import collections, copy, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile
   139	
   140	if hasattr(sys.stdout, "reconfigure"):          # this file prints glyphs (R2's strip); run it anywhere, piped or not
   141	    sys.stdout.reconfigure(encoding="utf-8")
   142	
   143	HERE = os.path.dirname(os.path.abspath(__file__))
   144	REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
   145	PIPE = os.path.join(REPO, "tools", "pipeline")
   146	CHECKER = os.environ.get("CTL_CHECKER") or os.path.join(PIPE, "check_entry_domain.py")
   147	RENDER = os.environ.get("CTL_RENDER") or os.path.join(PIPE, "gen_dashboard.py")
   148	PRE = os.environ.get("CTL_PRECOMMIT") or os.path.join(REPO, "tools", "precommit_check.sh")
   149	BEFORE = os.path.join(HERE, "gen_dashboard_before.py")      # HEAD's renderer at the landing, preserved
   150	#  the baseline travels WITH the checker under test: staged runs keep it beside the staged checker, and on the tree the two
   151	#  directories are the same
   152	BASELINE = os.path.join(os.path.dirname(os.path.abspath(CHECKER)), "entry_domain_baseline.json")
   153	if not os.path.exists(BASELINE):
   154	    BASELINE = os.path.join(PIPE, "entry_domain_baseline.json")
   155	LEDGER = os.path.join(PIPE, "ledger.json")
   156	sys.path.insert(0, PIPE)
   157	import stage_tokens as st  # noqa: E402
   158	
   159	T = tempfile.mkdtemp()
   160	res = []
   161	
   162	
   163	def say(label, ok, detail=""):
   164	    res.append(ok)
   165	    tag, rest = label.split(" ", 1)
   166	    print("%-4s %-76s %s  %s" % (tag, rest, "ok" if ok else "NO", detail))
   167	
   168	
   169	def wjson(name, obj):
   170	    p = os.path.join(T, name)
   171	    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False))
   172	    return p
   173	
   174	
   175	def pipe_copy(tag, baseline_text=None):
   176	    """a temp copy of the pipeline dir holding the checker under test, stage_tokens.py and a baseline (default: shipped)"""
   177	    d = os.path.join(T, "pipe_" + tag)
   178	    os.makedirs(d, exist_ok=True)
   179	    shutil.copy(CHECKER, os.path.join(d, "check_entry_domain.py"))
   180	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   181	    b = os.path.join(d, "entry_domain_baseline.json")
   182	    if baseline_text is None:
   183	        shutil.copy(BASELINE, b)
   184	    else:
   185	        io.open(b, "w", encoding="utf-8", newline="").write(baseline_text)
   186	    return os.path.join(d, "check_entry_domain.py")
   187	
   188	
   189	def run_checker(ledger_path, baseline_path=None, checker=None):
   190	    #  NO PYTHONIOENCODING: the precommit sets none, so the checker must survive a cp1252 pipe (Fable 5.1, pass 2)
   191	    env = dict(os.environ, GXLEDGER=ledger_path)
   192	    for k in ("GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
   193	        env.pop(k, None)
   194	    if baseline_path is not None:
   195	        env["GXDOMAIN_BASELINE"] = baseline_path
   196	    r = subprocess.run([sys.executable, checker or DEFAULT_CHECKER], capture_output=True, env=env)
   197	    out = (r.stdout + r.stderr).decode("cp1252", "replace")
   198	    return r.returncode, out.strip().splitlines()
   199	
   200	
   201	DEFAULT_CHECKER = pipe_copy("default")          # the checker under test, beside the SHIPPED baseline (md5 pin live)
   202	L0 = json.load(io.open(LEDGER, encoding="utf-8"))
   203	ROW0 = L0["rows"][0]["id"]
   204	N_OFF = sum(1 for r in L0["rows"] for x in r.get("entries", [])
   205	            if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…") and st.is_answer(x))
   206	
   207	
   208	def with_entries(entries, ledger=None):
   209	    L = copy.deepcopy(ledger or L0)
   210	    for row, e in entries:
   211	        for r in L["rows"]:
   212	            if r["id"] == row:
   213	                r.setdefault("entries", []).append(e)
   214	    return wjson("l_%d.json" % len(res), L)
   215	
   216	
   217	def ans(date, **kw):
   218	    e = {"phase": "review", "seat": "grok", "note": "a control entry"}
   219	    if date is not None:
   220	        e["date"] = date
   221	    e.update(kw)
   222	    return e
   223	
   224	
   225	def sha16(note):
   226	    return hashlib.sha1(str(note or "").encode("utf-8")).hexdigest()[:16]
   227	
   228	
   229	WHY_CUT = "dated on or after the cutoff 2026-10-17"
   230	WHY_CEIL = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
   231	WHY_ISO = "; its date is not ISO YYYY-MM-DD"
   232	
   233	
   234	def offline(row, e, why):
   235	    """the WHOLE refusal line the checker must print for entry e of row -- identifiers in their order, then the reason
   236	    (v4 read only the count of lines, so a reason replaced or row and phase swapped passed -- Fable 5.1, GPT-6 Astra, v4 pass)"""
   237	    dt = e.get("date")
   238	    dt = dt if isinstance(dt, str) else ("" if dt is None else repr(dt))
   239	    return "OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s" % (
   240	        row, e.get("phase") or "", e.get("seat") or "", dt or "(none)", str(e["d"]), sha16(e.get("note")), why)
   241	
   242	
   243	def summary_line(n_cur, n_within, n_base):
   244	    return ("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff 2026-10-17 inclusive"
   245	            % (n_cur, n_within, n_base))
   246	
   247	
   248	def ident(row, e):
   249	    return [row, e.get("phase") or "", e.get("seat") or "", e.get("date") if isinstance(e.get("date"), str) else "",
   250	            str(e["d"]), hashlib.sha1(str(e.get("note") or "").encode("utf-8")).hexdigest()[:16]]
   251	
   252	
   253	print("# dashokclass controls (v5) -- checker %s | renderer %s | precommit %s | baseline %s"
   254	      % (hashlib.md5(open(CHECKER, "rb").read()).hexdigest()[:8], hashlib.md5(open(RENDER, "rb").read()).hexdigest()[:8],
   255	         hashlib.md5(open(PRE, "rb").read()).hexdigest()[:8], hashlib.md5(open(BASELINE, "rb").read()).hexdigest()[:8]))
   256	# ------------------------------------------------------------------ the checker
   257	rc, out = run_checker(LEDGER)
   258	first = out[0] if out else ""
   259	#  the summary's BASELINE number too: `sum(base.values())` -> `len(base)` printed 1,342 and passed every v3 control (Grok 4.7,
   260	#  v3 pass) -- the count of frozen answers is 1,356 over 1,342 keys
   261	#  v5: the WHOLE line -- "inclusive" dropped from it passed all 72 v4 controls (Fable 5.1, v4 pass)
   262	say("C1 shipped ledger, shipped baseline, md5 pin live; the summary line EXACTLY", rc == 0 and first == summary_line(N_OFF, N_OFF, N_OFF),
   263	    "rc %d: %s" % (rc, first))
   264	for lab, ent, want in [
   265	    ("C2 ON the cutoff, a valid glyph (positive)", ans("2026-10-17", d="✓"), 0),
   266	    ("C2b AFTER the cutoff, a valid glyph (positive)", ans("2026-10-18", d="✕"), 0),
   267	    ("C3 ON the cutoff, d OK (inclusive)", ans("2026-10-17", d="OK"), 1),
   268	    ("C4 AFTER the cutoff, d OK", ans("2026-10-18", d="OK"), 1),
   269	    ("C5 a new answer BEFORE the cutoff, d OK (back-dated)", ans("2026-09-01", d="OK", seat="minimax"), 1),
   270	    ("C6 undated, d N/A", ans(None, d="N/A"), 1),
   271	    ("C7 after the cutoff, NO d", ans("2026-10-18"), 0),
   272	    ("C8 a HELD marker after the cutoff, d HELD", ans("2026-10-18", d="HELD", note=st.HELD + " grok] waiting"), 0),
   273	    ("C14 a new answer with an explicit BLANK d", ans("2026-10-10", d=""), 1),
   274	    ('C19a a new answer dated "10/18/2026", d OK', ans("10/18/2026", d="OK"), 1),
   275	    ("C19b a new answer with a NUMERIC date, d OK", ans(20261018, d="OK"), 1),
   276	    ("C20 a new answer with a non-ASCII d (cp1252 stdout, no traceback)", ans("2026-10-18", d="✗"), 1),
   277	    #  an explicit "d": null is PRESENT and off-domain -- `if x.get("d") is None` would treat it as missing (Fable 5.1, v3 pass)
   278	    ("C26 a new answer with an explicit null d", ans("2026-10-10", d=None), 1),
   279	    #  v5: a LIST d -- the key takes str() of d; without it the Counter raises on an unhashable key (Fable 5.1, v4 pass)
   280	    ("C26b a new answer whose d is a LIST", ans("2026-10-10", d=["OK"]), 1),
   281	    #  v5: a PADDED glyph is outside the four for the checker as for the renderer (R1h) -- `str(d).strip() in DOMAIN` passed
   282	    #  all 72 v4 controls (Fable 5.1, Grok 4.7, v4 pass)
   283	    ("C28 a new answer BEFORE the cutoff with a padded glyph ' ✓'", ans("2026-10-10", d=" ✓"), 1),
   284	]:
   285	    rc, out = run_checker(with_entries([(ROW0, ent)]))
   286	    tb = any("Traceback" in l for l in out)
   287	    #  a malformed date must be NAMED in the reason, not only refused: v1's lexical `t[3] >= CUTOFF` and a deleted suffix each
   288	    #  passed every v2 control while calling a numeric date "on or after the cutoff" (Fable 5.1, adjudication pass)
   289	    why = (not lab.startswith("C19")) or any("its date is not ISO" in l for l in out)
   290	    #  v5: the WHOLE refusal line for C3 (the cutoff reason), C6 (an undated entry: "(none)", no ISO clause) and C19a (the
   291	    #  ISO clause) -- v4 read only rc and the line count (Fable 5.1, GPT-6 Astra, v4 pass)
   292	    exact_why = {"C3": WHY_CUT, "C6": WHY_CEIL, "C19a": WHY_CEIL + WHY_ISO}.get(lab.split()[0])
   293	    offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   294	    exact = exact_why is None or offl == [offline(ROW0, ent, exact_why)]
   295	    say(lab, rc == want and not tb and why and exact, "rc %d (want %d)%s%s%s" % (
   296	        rc, want, " TRACEBACK" if tb else "", "" if why else " REASON NOT NAMED",
   297	        "" if exact else " LINE NOT EXACT: %r" % (offl[:1],)))
   298	#  C2c/C2d ISOLATED (GPT-6 Astra, v3 pass): the shipped ledger already carries 21 ⏸ and 35 … answers, so dropping either glyph
   299	#  from DOMAIN reddened the v3 rows without their own entry; a ledger holding ONLY the fixture entry makes each its own witness
   300	for lab, ent in (("C2c AFTER the cutoff, d ⏸, in a ledger holding only it (positive)", ans("2026-10-18", d="⏸")),
   301	                 ("C2d AFTER the cutoff, d …, in a ledger holding only it (positive)", ans("2026-10-18", d="…"))):
   302	    rc, out = run_checker(wjson("l_iso_%d.json" % len(res), {"rows": [{"id": "ctliso", "entries": [ent]}]}))
   303	    say(lab, rc == 0, "rc %d" % rc)
   304	#  C24 ISOLATED (GPT-6 Astra, v4 pass): the shipped ledger carries five off-domain NOTSEAT records, so `st.is_held(x)` for
   305	#  `not st.is_answer(x)` reddened C24 for the LEDGER's reason; a ledger holding only the record makes it its own witness
   306	rc, out = run_checker(wjson("l_iso_c24.json", {"rows": [{"id": "ctliso", "entries": [
   307	    ans("2026-10-18", d="OK", note=st.NOTSEAT + " a main-loop record")]}]}))
   308	say("C24 a non-answer RECORD (NOTSEAT) after the cutoff, d OK, in a ledger holding only it", rc == 0, "rc %d" % rc)
   309	# a frozen entry, found from the shipped baseline: copied (C9), rewritten (C10), refilled (C15), note-edited (C16), ev-edited (C22)
   310	base = [json.loads(l.rstrip(",\n")) for l in io.open(BASELINE, encoding="utf-8") if l.startswith("[\"")]
   311	k0 = base[0]
   312	
   313	
   314	def find_frozen(L):
   315	    for r in L["rows"]:
   316	        if r["id"] != k0[0]:
   317	            continue
   318	        for x in r["entries"]:
   319	            if "d" in x and ident(r["id"], x) == k0[:6]:
   320	                return x
   321	    raise SystemExit("APPARATUS FAIL: the first baseline identity is not in the shipped ledger")
   322	
   323	
   324	src = find_frozen(L0)
   325	rc, out = run_checker(with_entries([(k0[0], dict(src))]))
   326	offl = [l.strip() for l in out if "OFF-DOMAIN ANSWER" in l]
   327	say("C9 an identical copy of a frozen entry (%s %s %s %s %r): its refusal line EXACTLY" % tuple(k0[:5]),
   328	    rc == 1 and offl == [offline(k0[0], src, WHY_CEIL)], "rc %d; %r" % (rc, offl[:1]))
   329	L = copy.deepcopy(L0); find_frozen(L)["d"] = "✓"
   330	rc, out = run_checker(wjson("l_rewrite.json", L))
   331	say("C10 a frozen entry rewritten to a glyph", rc == 0, "rc %d" % rc)
   332	refill = dict(src); refill["note"] = "a different answer reusing the converted entry's slot"
   333	rc, out = run_checker(with_entries([(k0[0], refill)], ledger=L))
   334	say("C15 REFILL: the converted entry's (row, phase, seat, date, d) reused", rc == 1, "rc %d" % rc)
   335	L2 = copy.deepcopy(L0); f = find_frozen(L2); f["note"] = (f.get("note") or "") + " (a later correction)"
   336	rc, out = run_checker(wjson("l_noteedit.json", L2))
   337	say("C16 a frozen entry's note edited, d left off-domain", rc == 1, "rc %d" % rc)
   338	L3 = copy.deepcopy(L0); f = find_frozen(L3); f["ev"] = (f.get("ev") or "") + " (a corrected path)"
   339	rc, out = run_checker(wjson("l_evedit.json", L3))
   340	say("C22 a frozen entry's ev edited, outside the six fields (positive)", rc == 0, "rc %d" % rc)
   341	#  C25: each key field of the FROZEN entry edited by its least visible change.  A mutant normalising one field on the ledger's
   342	#  side -- `v[:10]` on the date, `.strip()`, `.lower()` -- passed every v3 control (GPT-6 Astra, v3 pass: the date suffix)
   343	OTHER_ROW = next(r["id"] for r in L0["rows"] if r["id"] != k0[0])
   344	for tag, field, how, fn in (("a", "date", "suffixed T12:00:00", lambda v: v + "T12:00:00"),
   345	                            ("b", "date", "a trailing space", lambda v: v + " "),
   346	                            ("c", "d", "a trailing space", lambda v: v + " "),
   347	                            ("d", "d", "its case swapped", lambda v: v.swapcase()),
   348	                            ("e", "note", "a trailing space", lambda v: v + " "),
   349	                            ("f", "note", "its case swapped", lambda v: v.swapcase()),
   350	                            ("g", "seat", "a trailing space", lambda v: v + " "),
   351	                            ("h", "seat", "upper-cased", lambda v: v.upper()),
   352	                            ("i", "phase", "a trailing space", lambda v: v + " "),
   353	                            ("j", "phase", "upper-cased", lambda v: v.upper())):
   354	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   355	    assert fn(fe[field]) != fe[field], (tag, field)
   356	    fe[field] = fn(fe[field])
   357	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   358	    say("C25%s a frozen entry's %s, %s" % (tag, field, how), rc == 1, "rc %d" % rc)
   359	Le = copy.deepcopy(L0); fe = find_frozen(Le)
   360	for r in Le["rows"]:
   361	    if r["id"] == k0[0]:
   362	        r["entries"] = [x for x in r["entries"] if x is not fe]
   363	    if r["id"] == OTHER_ROW:
   364	        r.setdefault("entries", []).append(fe)
   365	rc, out = run_checker(wjson("l_key_k.json", Le))
   366	say("C25k a frozen entry moved to another row (%s)" % OTHER_ROW, rc == 1, "rc %d" % rc)
   367	#  v5: the LEADING end of every field, and the row id at both ends -- `.lstrip()` on the date, d, seat, phase or note, and
   368	#  `str(r.get("id")).strip()`, each passed all 72 v4 controls, which edited only the trailing end (Fable 5.1, Grok 4.7, GPT-6
   369	#  Astra, v4 pass)
   370	
   371	
   372	def moved_to(new_id):
   373	    Lm = copy.deepcopy(L0); fm = find_frozen(Lm)
   374	    for r in Lm["rows"]:
   375	        if r["id"] == k0[0]:
   376	            r["entries"] = [x for x in r["entries"] if x is not fm]
   377	    Lm["rows"].append({"id": new_id, "title": "row id control", "sev": "LOW", "state": "open", "commits": "", "entries": [fm]})
   378	    return Lm
   379	
   380	
   381	rc, out = run_checker(wjson("l_key_l.json", moved_to(k0[0] + " ")))
   382	say("C25l a frozen entry moved to a row whose id has a TRAILING space", rc == 1, "rc %d" % rc)
   383	for tag, field in (("m", "date"), ("n", "d"), ("o", "note"), ("p", "seat"), ("q", "phase")):
   384	    Le = copy.deepcopy(L0); fe = find_frozen(Le)
   385	    fe[field] = " " + fe[field]
   386	    rc, out = run_checker(wjson("l_key_%s.json" % tag, Le))
   387	    say("C25%s a frozen entry's %s with a LEADING space" % (tag, field), rc == 1, "rc %d" % rc)
   388	rc, out = run_checker(wjson("l_key_r.json", moved_to(" " + k0[0])))
   389	say("C25r a frozen entry moved to a row whose id has a LEADING space", rc == 1, "rc %d" % rc)
   390	rc, out = run_checker(LEDGER, wjson("b_empty.json", []))
   391	nb = sum(1 for l in out if "OFF-DOMAIN ANSWER" in l)
   392	#  and the SUMMARY line on this dirty ledger: it was pinned only on the clean one, where "passes" and "entries" agree, so
   393	#  printing len(cur) for both passed every v3 control (GLM 5.3, v3 pass)
   394	s11 = summary_line(N_OFF, 0, 0)
   395	f11 = out[0] if out else ""
   396	hint = any("give each a `d` from" in l for l in out)      # the instruction line (Fable 5.1, v3 pass: no control asserted it)
   397	say("C11 baseline emptied: every shipped off-domain answer named, the summary counts 0 within the ceiling, the hint printed",
   398	    rc == 1 and nb == N_OFF and f11 == s11 and hint, "rc %d, %d of %d named; summary %s; hint %s"
   399	    % (rc, nb, N_OFF, "ok" if f11 == s11 else repr(f11[:90]), "ok" if hint else "MISSING"))
   400	# C12: the cutoff test isolated -- each fixture entry IS in its fixture baseline, so only the date can refuse it
   401	#  and FAR after: a two-day membership test (`in ("2026-10-17", "2026-10-18")`) passed before/on/after (Grok 4.7, v3 pass)
   402	for tag, dt, want in (("before", "2026-10-16", 0), ("on", "2026-10-17", 1), ("after", "2026-10-18", 1),
   403	                      ("far", "2027-01-01", 1)):
   404	    e = ans(dt, d="OK", seat="kimi", note="cutoff isolation " + tag)
   405	    fb = wjson("b_cut_%s.json" % tag, base + [ident(ROW0, e) + [1]])
   406	    rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   407	    #  v5: the summary EXACTLY -- here the fixture baseline holds N_OFF + 1 and a refused entry leaves N_OFF within, so the
   408	    #  baseline number differs from the within-count; C1 and C11 cannot tell them apart (1356/1356, 0/0), and printing the
   409	    #  within-count there passed all 72 v4 controls (Fable 5.1, v4 pass)
   410	    s12 = summary_line(N_OFF + 1, N_OFF + 1 if want == 0 else N_OFF, N_OFF + 1)
   411	    f12 = out[0] if out else ""
   412	    say("C12 cutoff isolated: a FROZEN identity dated %s (%s), the summary EXACTLY" % (dt, tag), rc == want and f12 == s12,
   413	        "rc %d (want %d); summary %s" % (rc, want, "ok" if f12 == s12 else repr(f12[:100])))
   414	#  C12s: a MATCHED identity whose date the ISO shape OPENS -- `^...$' on the shape refused nothing and passed all 72 v4
   415	#  controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass); the checker reads the first ten characters
   416	e = ans("2026-10-17T12:00:00", d="OK", seat="kimi", note="cutoff isolation suffixed")
   417	fb = wjson("b_cut_suffixed.json", base + [ident(ROW0, e) + [1]])
   418	rc, out = run_checker(with_entries([(ROW0, e)]), fb)
   419	say("C12s cutoff isolated: a FROZEN identity dated 2026-10-17T12:00:00", rc == 1, "rc %d (want 1)" % rc)
   420	rc, out = run_checker(LEDGER, os.path.join(T, "no_such_baseline.json"))
   421	say("C13 an unreadable baseline", rc == 2, "rc %d" % rc)
   422	#  C27: the glyph SET, read from both files' own literals.  A fifth member (`"ZXQ"`) in the checker's DOMAIN, or a fifth key in
   423	#  the renderer's D_CLASS, was invisible to every v3 control -- no control writes that spelling, and none can write every one
   424	#  (Grok 4.7, v3 pass) -- so the set is pinned where it is defined, and the two files must agree, as the checker says
   425	import ast  # noqa: E402
   426	#  v5: by the BINDINGS, not the first line -- a second `DOMAIN = (..., "ZXQ")' further down is the one that takes effect, and
   427	#  the v4 reader of the first line passed it (Fable 5.1, v4 pass).  Every store of the name anywhere in the file is counted
   428	#  (an assignment, an augmented one, a loop target ...), and a `global' naming it is refused: exactly one binding, at module
   429	#  level, whose value is a literal.
   430	def literal(path, name):
   431	    tree = ast.parse(io.open(path, encoding="utf-8").read())
   432	    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Store)]
   433	    globs = [n for n in ast.walk(tree) if isinstance(n, ast.Global) and name in n.names]
   434	    top = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(g, ast.Name) and g.id == name for g in n.targets)]
   435	    if len(stores) != 1 or globs or len(top) != 1:
   436	        return "%d bindings, %d top-level assignments, %d global statements" % (len(stores), len(top), len(globs))
   437	    return ast.literal_eval(top[0].value)
   438	dom, dcls = literal(CHECKER, "DOMAIN"), literal(RENDER, "D_CLASS")
   439	four = ("✓", "✕", "⏸", "…")
   440	say("C27 ONE binding each: the checker's DOMAIN and the renderer's D_CLASS keys are exactly ✓ ✕ ⏸ …",
   441	    isinstance(dom, tuple) and isinstance(dcls, dict) and sorted(dom) == sorted(four) and sorted(dcls) == sorted(four),
   442	    "DOMAIN %r | D_CLASS keys %r" % (dom, sorted(dcls) if isinstance(dcls, dict) else dcls))
   443	rc, out = run_checker(LEDGER, wjson("b_shape.json", [k[:6] + [str(k[6])] for k in base]))
   444	say("C17 a misshapen baseline (counts as strings)", rc == 2, "rc %d" % rc)
   445	#  C17b: one key of count >= 2 split into two rows; the sum must hold (pass 2 fixed last-wins; the adjudication pass found
   446	#  nothing pinned the sum -- GPT-6 Astra and GLM 5.3)
   447	k2 = next(k for k in base if k[6] >= 2)
   448	split = [k for k in base if k is not k2] + [k2[:6] + [1], k2[:6] + [k2[6] - 1]]
   449	rc, out = run_checker(LEDGER, wjson("b_split.json", split))
   450	say("C17b a key split across two baseline rows sums (%s %s %s %s %r x%d)" % (tuple(k2[:5]) + (k2[6],)), rc == 0, "rc %d" % rc)
   451	#  v5: each clause of the baseline row test at its own edge, one misshapen row appended to the shipped baseline -- `len(k) >=
   452	#  7', `isinstance(k[6], int)' (a bool is an int), `k[6] != 0', and the string test narrowed to five fields each passed all 72
   453	#  v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   454	kx = base[0]
   455	for tag, row_, how in (("c", kx[:6] + [1, "extra"], "eight fields"), ("d", kx[:6] + [True], "a count of true"),
   456	                       ("e", kx[:6] + [-1], "a count of -1"), ("f", kx[:6] + [0], "a count of 0"),
   457	                       ("g", kx[:6] + [1.0], "a count of 1.0"), ("h", [5] + kx[1:6] + [1], "a numeric first field"),
   458	                       ("i", kx[:5] + [5, 1], "a numeric note sha")):
   459	    rc, out = run_checker(LEDGER, wjson("b_row_%s.json" % tag, base + [row_]))
   460	    tb = any("Traceback" in l for l in out)
   461	    say("C17%s a misshapen baseline row: %s (override)" % (tag, how), rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   462	txt = io.open(BASELINE, encoding="utf-8").read()
   463	lines = txt.split("\n")
   464	lines[1] = lines[1].replace('"y"', '"Y"', 1) if '"y"' in lines[1] else lines[1].replace(", 1]", ", 2]", 1)
   465	rc_mod, out_mod = run_checker(LEDGER, checker=pipe_copy("md5mod", "\n".join(lines)))
   466	rc_same, _ = run_checker(LEDGER, checker=pipe_copy("md5same", txt))
   467	say("C18 md5 pin: one baseline line changed -> 2, unchanged -> 0", rc_mod == 2 and rc_same == 0,
   468	    "changed rc %d, unchanged rc %d" % (rc_mod, rc_same))
   469	#  C18b: the same bytes checked out with CRLF -- what a fresh clone under core.autocrlf=true writes (measured 06a3ffc6 ->
   470	#  89d1d370 raw at the adjudication pass) -- must pass the pin, which folds line endings
   471	rc_crlf, _ = run_checker(LEDGER, checker=pipe_copy("md5crlf", txt.replace("\n", "\r\n")))
   472	say("C18b md5 pin: the baseline checked out with CRLF line endings -> 0", rc_crlf == 0, "rc %d" % rc_crlf)
   473	for lab, obj in (('C21a a misshapen ledger: {"rows": null}', {"rows": None}),
   474	                 ("C21b a misshapen ledger: a row that is not an object", {"rows": [42]}),
   475	                 ("C21c a misshapen ledger: a list, not an object", []),
   476	                 #  each of these walked as EMPTY and passed v3, rc 0 (GPT-6 Astra, v3 pass)
   477	                 ('C21d a misshapen ledger: {"rows": {}}', {"rows": {}}),
   478	                 ("C21e a misshapen ledger: an entry that is a string", {"rows": [{"id": "x", "entries": ["bogus"]}]}),
   479	                 ("C21f a misshapen ledger: entries that are an object", {"rows": [{"id": "x", "entries": {}}]}),
   480	                 #  v5: `rows' ABSENT -- `ledger.get("rows", [])' would walk it as empty (Grok 4.7, GLM 5.3, v4 pass)
   481	                 ("C21i a misshapen ledger: no rows key -- {}", {}),
   482	                 ('C21i a misshapen ledger: no rows key -- {"seats": []}', {"seats": []})):
   483	    rc, out = run_checker(wjson("l_shape_%d.json" % len(res), obj))
   484	    tb = any("Traceback" in l for l in out)
   485	    say(lab, rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   486	rc, out = run_checker(LEDGER, wjson("b_dict.json", {}))
   487	say("C21g a misshapen baseline: an object, not a list (override)", rc == 2, "rc %d" % rc)
   488	#  C21h: the shape check passes it, then is_answer raises on a NON-STRING note -- the one input that still reaches the walk's
   489	#  except-arm, so that arm stays a measured rc 2 rather than dead code
   490	rc, out = run_checker(wjson("l_shape_note.json", {"rows": [{"id": "x", "entries": [
   491	    {"phase": "review", "seat": "grok", "date": "2026-10-18", "d": "OK", "note": 5}]}]}))
   492	tb = any("Traceback" in l for l in out)
   493	say("C21h an entry whose note is a number (it raises inside is_answer)", rc == 2 and not tb,
   494	    "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   495	pj = os.path.join(T, "l_notjson.json")
   496	io.open(pj, "w", encoding="utf-8").write("{ this is not json")
   497	rc, out = run_checker(pj)
   498	tb = any("Traceback" in l for l in out)
   499	say("C23 an unreadable ledger (not JSON)", rc == 2 and not tb, "rc %d%s" % (rc, " TRACEBACK" if tb else ""))
   500	
   501	# ------------------------------------------------------------------ the renderer
   502	SEATS = [s["id"] for s in L0["seats"]]
   503	EXPECT = {   # seat -> (entry fields, class, glyph)
   504	    "fable5": ({"d": "✓"}, "ok", "✓"),
   505	    "opus5": ({"d": "OK"}, "legacy", "OK"),
   506	    "codex": ({}, "pend", "…"),
   507	    "agy": ({"d": ""}, "legacy", "?"),
   508	    "grok": ({"d": "HELD", "note": st.HELD + " grok] waiting"}, "hold", "⏸"),
   509	    "kimi": ({"d": "OK", "note": st.NOTSEAT + " a main-loop record"}, "tok", "∅"),
   510	    "glm": ({"d": "✕"}, "bad", "✕"),
   511	    "deepseek": ({"d": "⏸"}, "hold", "⏸"),
   512	    "minimax": ({"d": "N/A"}, "legacy", "N/A"),
   513	}
   514	assert set(EXPECT) == set(SEATS), SEATS
   515	#  the legacy cell's WHOLE tooltip: the class line, the date, the note -- joined and escaped exactly as cell() does.  A prefix
   516	#  check let "(not approval, not a seat failure)" return after the checked words (GPT-6 Astra and GLM 5.3, adjudication pass)
   517	LEGACY_TIP = html.escape("legacy -- verdict unclassified: d = 'OK' is outside ✓ ✕ ⏸ …; read the note for the outcome"
   518	                         " — 2026-10-16 — a renderer control", quote=True)
   519	LEGEND_LINE = ('<span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- verdict text outside '
   520	               '✓ ✕ ⏸ …, unclassified (read the note; <span class="g" style="color:var(--muted);font-style:italic">?</span> = '
   521	               'an explicit blank)</span>')
   522	REC_NOTE = st.NOTSEAT + " a record beside the answer"
   523	REF_A = {"phase": "research", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": st.RE_READ + " refused re-read control"}
   524	FX = copy.deepcopy(L0)
   525	ents = []
   526	for s in SEATS:
   527	    e = {"phase": "review", "seat": s, "date": "2026-10-16", "note": "a renderer control"}
   528	    e.update(EXPECT[s][0])
   529	    ents.append(e)
   530	FX["rows"] = [{"id": "ctlrow", "title": "renderer control row", "sev": "LOW", "state": "open", "commits": "", "entries": ents},
   531	              {"id": "ctlesc", "title": "escape control row", "sev": "LOW", "state": "open", "commits": "",
   532	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": "<b>&", "note": "escape control"}]},
   533	              #  a whitespace-only `d` must show `?`, never an invisible glyph (0 such values in the ledger; Fable 5.1,
   534	              #  adjudication pass, measured `{e(d) if d else "?"}` passing every v2 control)
   535	              {"id": "ctlws", "title": "whitespace control row", "sev": "LOW", "state": "open", "commits": "",
   536	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ", "note": "whitespace control"},
   537	                           #  a TAB-only d: `.strip(" ")` would keep it invisible (Grok 4.7, v3 pass)
   538	                           {"phase": "assess", "seat": "grok", "date": "2026-10-16", "d": "\t", "note": "tab control"},
   539	                           #  v5: a newline and an NBSP -- `.strip(" \t")' kept both invisible and passed all 72 v4
   540	                           #  controls (Fable 5.1, Grok 4.7, v4 pass)
   541	                           {"phase": "assess", "seat": "opus5", "date": "2026-10-16", "d": "\n", "note": "newline control"},
   542	                           {"phase": "assess", "seat": "codex", "date": "2026-10-16", "d": "\xa0", "note": "nbsp control"}]},
   543	              #  v5: an explicit null d renders legacy with the glyph None -- a renderer that treats null as missing (…) or
   544	              #  skips its class line passed all 72 v4 controls (Fable 5.1, Grok 4.7, GPT-6 Astra, v4 pass)
   545	              {"id": "ctlnull", "title": "null control row", "sev": "LOW", "state": "open", "commits": "",
   546	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": None, "note": "null control"}]},
   547	              #  R1e: an ANSWER with a non-answer RECORD beside it in one cell -- deleting the record line passed every v3
   548	              #  control and drops the note from 32 displayed cells (GPT-6 Astra, v3 pass)
   549	              {"id": "ctlrec", "title": "record control row", "sev": "LOW", "state": "open", "commits": "",
   550	               "entries": [{"phase": "review", "seat": "fable5", "date": "2026-10-16", "d": "OK", "note": "record control answer"},
   551	                           {"phase": "review", "seat": "fable5", "date": "2026-10-16", "note": REC_NOTE}]},
   552	              #  R1f: a legacy answer carrying a stage exemption (a re-read), refused by a LATER answer in its stage
   553	              #  R1h: a PADDED glyph " ✓" is outside the domain and renders legacy (the checker refuses it as off-domain);
   554	              #  `D_CLASS.get(str(d).strip(), ...)` would class it ok (Fable 5.1, v3 pass: caught only as a presence pin)
   555	              {"id": "ctlpad", "title": "padded glyph control row", "sev": "LOW", "state": "open", "commits": "",
   556	               "entries": [{"phase": "assess", "seat": "fable5", "date": "2026-10-16", "d": " ✓", "note": "padded glyph control"}]},
   557	              {"id": "ctlref", "title": "refused exemption control row", "sev": "LOW", "state": "open", "commits": "",
   558	               "entries": [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]}]
   559	fx_path = wjson("fx_render.json", FX)
   560	
   561	
   562	def render(gen, ledger_path, tag):
   563	    d = os.path.join(T, "r_" + tag)
   564	    os.makedirs(d, exist_ok=True)
   565	    shutil.copy(gen, os.path.join(d, "gen_dashboard.py"))
   566	    shutil.copy(os.path.join(PIPE, "stage_tokens.py"), d)
   567	    out = os.path.join(d, "out.html")
   568	    env = dict(os.environ, GXLEDGER=ledger_path, PYTHONIOENCODING="utf-8")
   569	    r = subprocess.run([sys.executable, os.path.join(d, "gen_dashboard.py"), "--out", out], capture_output=True, text=True,
   570	                       encoding="utf-8", env=env)
   571	    return io.open(out, encoding="utf-8").read() if r.returncode == 0 and os.path.exists(out) else None
   572	
   573	
   574	CTL_OTHER = ("escape control", "whitespace control", "record control answer", "refused re-read control", "a later answer",
   575	             "padded glyph control", "tab control", "newline control", "nbsp control", "null control")
   576	
   577	
   578	def cells(html_text):
   579	    got = []
   580	    for m in re.finditer(r'<td class="c ([a-z]+)">(.*?)</td>', html_text, re.S):
   581	        if m.group(1) == "none":
   582	            continue
   583	        g = re.search(r'<span class="g">(.*?)</span>', m.group(2))
   584	        tip = re.search(r'<span class="tip">(.*?)</span>', m.group(2), re.S)
   585	        got.append((m.group(1), g.group(1) if g else None, tip.group(1) if tip else ""))
   586	    return got
   587	
   588	
   589	def r1(html_text):
   590	    if html_text is None:
   591	        return False, "render FAILED (a crash is not a kill)"
   592	    got = [c for c in cells(html_text) if not any(k in c[2] for k in CTL_OTHER)]   # the control row's nine, in seat order
   593	    want = [(EXPECT[s][1], EXPECT[s][2]) for s in SEATS]
   594	    head = got[:len(want)]
   595	    bad = [(s, g[:2], w) for s, g, w in zip(SEATS, head, want) if (g[0], g[1]) != w]
   596	    legacy_tip = head[SEATS.index("opus5")][2] if len(head) == len(want) else ""
   597	    tip_ok = legacy_tip == LEGACY_TIP
   598	    return (len(head) == len(want) and not bad and tip_ok), ("%d cells; mismatches %s; legacy tip %s" % (
   599	        len(head), bad[:3], "exact" if tip_ok else "WRONG: %r" % legacy_tip[:120]))
   600	
   601	
   602	def r1b(html_text):
   603	    if html_text is None:
   604	        return False, "render FAILED (a crash is not a kill)"
   605	    got = [c for c in cells(html_text) if "escape control" in c[2]]
   606	    esc = got[0] if got else ("", "", "")
   607	    return (esc[0] == "legacy" and esc[1] == "&lt;b&gt;&amp;"), "escape cell %r" % (esc[:2],)
   608	
   609	
   610	def r1d(html_text):
   611	    if html_text is None:
   612	        return False, "render FAILED (a crash is not a kill)"
   613	    got = [c for c in cells(html_text) if any(k in c[2] for k in ("whitespace control", "tab control", "newline control",
   614	                                                                    "nbsp control"))]
   615	    return (len(got) == 4 and all(c[0] == "legacy" and c[1] == "?" for c in got)), "whitespace cells %r" % ([c[:2] for c in got],)
   616	
   617	
   618	def legacy_line(d):
   619	    return "legacy -- verdict unclassified: d = %r is outside ✓ ✕ ⏸ …; read the note for the outcome" % d
   620	
   621	
   622	def r1g(html_text):
   623	    #  EVERY legacy cell, not only the "OK" one: `if cls == LEGACY` -> `if d == "OK"` passed every v3 control and drops the
   624	    #  explanation from 305 displayed cells (GPT-6 Astra, v3 pass)
   625	    if html_text is None:
   626	        return False, "render FAILED (a crash is not a kill)"
   627	    #  the WHOLE tooltip of each simple legacy cell -- class line, date, note -- not a prefix and not one cell: `if cls ==
   628	    #  LEGACY and d == "OK"` and `... and str(d).strip()` passed all 46 v3 controls (Fable 5.1, v3 pass, measured)
   629	    want = [(note, d, html.escape(" — ".join([legacy_line(d), "2026-10-16", note]), quote=True))
   630	            for note, d in (("a renderer control", "OK"), ("a renderer control", ""), ("a renderer control", "N/A"),
   631	                            ("escape control", "<b>&"), ("whitespace control", " "), ("padded glyph control", " ✓"),
   632	                            ("tab control", "\t"), ("null control", None))]
   633	    legacy = [tip for cls_, g, tip in cells(html_text) if cls_ == "legacy"]
   634	    missing = [(note, d) for note, d, whole in want if whole not in legacy]
   635	    return not missing, "%d legacy cells; no exact tooltip for: %s" % (len(legacy), missing[:3])
   636	
   637	
   638	def r1e(html_text):
   639	    if html_text is None:
   640	        return False, "render FAILED (a crash is not a kill)"
   641	    got = [c for c in cells(html_text) if "record control answer" in c[2]]
   642	    #  v5: the WHOLE tooltip -- class line, date, note, the record line.  v4 asserted the record substring, so a class line
   643	    #  dropped from every cell with a record beside it passed all 72 v4 controls (Fable 5.1, GPT-6 Astra, v4 pass)
   644	    want = html.escape(" — ".join([legacy_line("OK"), "2026-10-16", "record control answer", "record: 2026-10-16 — " + REC_NOTE]),
   645	                       quote=True)
   646	    return (len(got) == 1 and got[0][0] == "legacy" and got[0][2] == want), "cells %d; tooltip %s" % (
   647	        len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:140] if got else ""))
   648	
   649	
   650	def r1f(html_text):
   651	    if html_text is None:
   652	        return False, "render FAILED (a crash is not a kill)"
   653	    stage = [REF_A, {"phase": "research", "seat": "grok", "date": "2026-10-17", "d": "✓", "note": "a later answer"}]
   654	    probs = st.stage_token_problems(stage)
   655	    want = html.escape(" — ".join(["EXEMPTION REFUSED BY SECTION H: " + "; ".join(probs), legacy_line("OK"), "2026-10-16",
   656	                                   REF_A["note"]]), quote=True)
   657	    got = [c for c in cells(html_text) if "refused re-read control" in c[2]]
   658	    return (bool(probs) and len(got) == 1 and got[0][2] == want), "refusals %d; cells %d; tooltip %s" % (
   659	        len(probs), len(got), "exact" if got and got[0][2] == want else "WRONG: %r" % (got[0][2][:120] if got else ""))
   660	
   661	
   662	ha_fx = render(RENDER, fx_path, "after")
   663	ok, det = r1(ha_fx); say("R1 fixture row: class, glyph and the legacy tooltip EXACTLY, per seat", ok, det)
   664	ok, det = r1g(ha_fx); say("R1g every simple legacy cell's WHOLE tooltip, the class line for ITS d", ok, det)
   665	pad = [c for c in cells(ha_fx or "") if "padded glyph control" in c[2]]
   666	say("R1h a padded glyph ' ✓' renders legacy, not ok", len(pad) == 1 and pad[0][0] == "legacy",
   667	    "cell %r" % (pad[0][:2],) if pad else "render FAILED or no cell")
   668	ok, det = r1e(ha_fx); say("R1e an answer with a record beside it: its WHOLE tooltip", ok, det)
   669	nul = [c for c in cells(ha_fx or "") if "null control" in c[2]]
   670	say("R1n an explicit null d renders legacy with the glyph None", len(nul) == 1 and nul[0][:2] == ("legacy", "None"),
   671	    "cell %r" % (nul[0][:2],) if nul else "render FAILED or no cell")
   672	ok, det = r1f(ha_fx); say("R1f a refused exemption's line first, then the class line, exactly", ok, det)
   673	ok, det = r1b(ha_fx); say("R1b an escapable d renders escaped", ok, det)
   674	ok, det = r1d(ha_fx); say("R1d a whitespace-only d -- a space, a tab, a newline, an NBSP -- shows ?", ok, det)
   675	low = (ha_fx or "").lower()
   676	hits = [p for p in ("not approval", "not a seat failure") if p in low]
   677	say("R1c the fixture page says neither 'not approval' nor 'not a seat failure'", ha_fx is not None and not hits,
   678	    "render %s; found %s" % ("ok" if ha_fx is not None else "FAILED", hits or "none"))
   679	leg = re.search(r'<div class="legend">(.*?)</div>', ha_fx or "", re.S)
   680	say("R4 the legend carries the legacy line EXACTLY", bool(leg) and LEGEND_LINE in leg.group(1),
   681	    "legend %s" % ("found" if leg else "MISSING"))
   682	#  R5 (v5): the two CSS rules the class adds -- `font-size:0' made every legacy glyph invisible and passed all 72 v4 controls
   683	#  (GPT-6 Astra, Fable 5.1, v4 pass)
   684	CSS = ("td.c.legacy { outline:1px dashed var(--line); outline-offset:-3px; }",
   685	       ".c.legacy .g { color:var(--muted); font-style:italic; font-size:11px; }")
   686	say("R5 the page carries the legacy class's two CSS rules EXACTLY", ha_fx is not None and all(c in ha_fx for c in CSS),
   687	    "missing %r" % ([c[:30] for c in CSS if c not in (ha_fx or "")],))
   688	
   689	
   690	def census(html_text):
   691	    c = collections.Counter(m.group(1) for m in re.finditer(r'<td class="c ([a-z]+)"', html_text))
   692	    s = re.search(r'<span class="k">entries</span><b>([^<]*)</b>', html_text).group(1)
   693	    return c, s
   694	
   695	
   696	hb, ha = render(BEFORE, LEDGER, "before_real"), render(RENDER, LEDGER, "after_real")
   697	cb, sb = census(hb)
   698	ca, sa = census(ha)
   699	same = all(cb[k] == ca[k] for k in ("ok", "hold", "bad", "tok", "none"))
   700	moved = cb["pend"] - ca["pend"] == ca["legacy"] and ca["legacy"] > 0
   701	nums = [int(x) for x in re.findall(r"(\d+)", sa)]
   702	n_entries = sum(len(r.get("entries", [])) for r in L0["rows"])
   703	n_legacy = sum(1 for r in L0["rows"] for x in r.get("entries", []) if "d" in x and x["d"] not in ("✓", "✕", "⏸", "…"))
   704	#  the strip's FIFTH number is checked against the ledger itself: a renderer that folded legacy into … still summed (the
   705	#  kill table measured R2 blind to that on its first run)
   706	cnt = collections.Counter()
   707	for r_ in L0["rows"]:
   708	    for x in r_.get("entries", []):
   709	        d_ = x.get("d", "…")
   710	        cnt[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
   711	#  EACH number against the ledger's own count: the v3 form checked only the total and the legacy number, so folding every
   712	#  canonical glyph into ✓ passed (GPT-6 Astra, v3 pass)
   713	sums = nums == [cnt["✓"], cnt["✕"], cnt["⏸"], cnt["…"], cnt["legacy"], n_entries] and nums[4] == n_legacy
   714	#  v5: the WHOLE strip string -- its labels too: "1397 approved" passed all 72 v4 controls (GPT-6 Astra, v4 pass)
   715	def strip_text(c, total):
   716	    return "%d✓ %d✕ %d⏸ %d… %d legacy · %d in all" % (c["✓"], c["✕"], c["⏸"], c["…"], c["legacy"], total)
   717	
   718	
   719	label_ok = sa == strip_text(cnt, n_entries)
   720	say("R2 shipped ledger BEFORE vs AFTER: only pend -> legacy; the strip string EXACTLY (each number, its label)",
   721	    same and moved and sums and label_ok,
   722	    "before %s | after %s | strip '%s' | ledger %d entries, %d off-domain" % (dict(sorted(cb.items())), dict(sorted(ca.items())),
   723	                                                                          sa, n_entries, n_legacy))
   724	#  R2b (v5): the FIXTURE page's strip against the fixture's own counts, by exact membership -- its padded " ✓" and its null
   725	#  count legacy.  R2 recomputes on the shipped ledger, which holds no padded glyph, so counting " ✓" as ✓ passed all 72 v4
   726	#  controls (Fable 5.1, Grok 4.7, v4 pass)
   727	cfx = collections.Counter()
   728	for r_ in FX["rows"]:
   729	    for x in r_.get("entries", []):
   730	        d_ = x.get("d", "…")
   731	        cfx[d_ if d_ in ("✓", "✕", "⏸", "…") else "legacy"] += 1
   732	_, sfx = census(ha_fx) if ha_fx else (None, "")
   733	want_fx = strip_text(cfx, sum(len(r_.get("entries", [])) for r_ in FX["rows"]))
   734	say("R2b the FIXTURE page's strip EXACTLY, by exact membership (padded and null count legacy)", sfx == want_fx,
   735	    "strip %r, want %r" % (sfx, want_fx))
   736	src_r = io.open(RENDER, encoding="utf-8").read()
   737	for tag, find, repl, check in (
   738	        ("ok", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "ok")', r1),
   739	        ("pend", "cls = D_CLASS.get(d, LEGACY)", 'cls = D_CLASS.get(d, "pend")', r1),
   740	        ("noescape", '{e(d) if str(d).strip() else "?"}', '{d if str(d).strip() else "?"}', r1b)):
   741	    if src_r.count(find) != 1:
   742	        say("R3 MUTANT %s: find-text present" % tag, False, "MUTANT TEXT NOT FOUND"); continue
   743	    m = os.path.join(T, "gen_mut_%s.py" % tag)
   744	    io.open(m, "w", encoding="utf-8").write(src_r.replace(find, repl))
   745	    h = render(m, fx_path, "mut_" + tag)
   746	    ok, det = check(h)
   747	    say("R3 MUTANT %s renders and fails its check" % tag, h is not None and not ok, det)
   748	
   749	# ------------------------------------------------------------------ the wiring: precommit section Q2, failures counted
   750	BASH = os.environ.get("BASH_EXE") or r"C:\Program Files\Git\bin\bash.exe"
   751	txt_pre = io.open(PRE, encoding="utf-8").read()
   752	a, b = txt_pre.find('say ""; say "Q2.'), txt_pre.find("#  ---- R ----")
   753	if a < 0 or b < a or not os.path.exists(BASH):
   754	    say("W0 precommit Q2 block extracted and a git-bash found", False, "a=%d b=%d bash=%s" % (a, b, BASH))
   755	else:
   756	    blk = os.path.join(T, "q2_block.sh")
   757	    io.open(blk, "w", encoding="utf-8", newline="\n").write(
   758	        'say () { :; }\nfails=0\ngood () { echo "GOOD $*"; }\nbad () { echo "BAD $*"; fails=$((fails + 1)); }\n'
   759	        '_HERE="$1"\n' + txt_pre[a:b] + '\necho "FAILURES $fails"\n')
   760	    def w_tools(tag, ledger_path, baseline_text=None, nochecker=False, stub=None):
   761	        """a fake tools/ dir: the block's own _HERE, holding the checker under test, the FIXTURE ledger as the default ledger
   762	        and a baseline -- the block strips GXLEDGER / GXDOMAIN_BASELINE, so fixtures can only enter this way"""
   763	        d = os.path.join(T, "w_" + tag)
   764	        os.makedirs(os.path.join(d, "pipeline"), exist_ok=True)
   765	        if stub is not None:
   766	            io.open(os.path.join(d, "pipeline", "check_entry_domain.py"), "w", encoding="utf-8").write(stub)
   767	        elif not nochecker:
   768	            shutil.copy(CHECKER, os.path.join(d, "pipeline", "check_entry_domain.py"))
   769	        shutil.copy(os.path.join(PIPE, "stage_tokens.py"), os.path.join(d, "pipeline"))
   770	        shutil.copy(ledger_path, os.path.join(d, "pipeline", "ledger.json"))
   771	        if baseline_text is None:
   772	            shutil.copy(BASELINE, os.path.join(d, "pipeline", "entry_domain_baseline.json"))
   773	        elif baseline_text != "<absent>":
   774	            io.open(os.path.join(d, "pipeline", "entry_domain_baseline.json"), "w", encoding="utf-8").write(baseline_text)
   775	        return d
   776	    #  dated BEFORE the cutoff, so only the BASELINE decides W4: a post-cutoff entry is refused by the date rule whichever
   777	    #  baseline is read, and the kill table measured W4 blind to the un-stripped override on its first run for that reason
   778	    new_led = with_entries([(ROW0, ans("2026-10-10", d="OK", seat="deepseek", note="W new off-domain"))])
   779	    permissive = wjson("b_permissive.json", base + [ident(ROW0, ans("2026-10-10", d="OK", seat="deepseek",
   780	                                                                      note="W new off-domain")) + [1]])
   781	    #  the FIRST LINE names which branch fired: W2 the rc-1 refusal, W3 the rc-2 apparatus line -- `-eq 1` -> `-eq 7` and a
   782	    #  rewritten message each passed every v2 control, which tested only the BAD prefix and the counter (Fable 5.1,
   783	    #  adjudication pass)
   784	    for lab, tools, envx, want, wantf, msg in (
   785	            ("W1 Q2 on the shipped ledger", w_tools("1", LEDGER), {}, "GOOD", 0, "within the frozen ceiling"),
   786	            ("W2 Q2 with a new off-domain answer", w_tools("2", new_led), {}, "BAD", 1, "beyond the frozen legacy ceiling"),
   787	            ("W3 Q2 with the baseline absent (rc 2 path)", w_tools("3", LEDGER, "<absent>"), {}, "BAD", 1,
   788	             "could not run (rc 2)"),
   789	            ("W4 Q2 ignores an exported GXDOMAIN_BASELINE that would admit the entry", w_tools("4", new_led),
   790	             {"GXDOMAIN_BASELINE": permissive}, "BAD", 1, "beyond the frozen legacy ceiling"),
   791	            #  the bad ledger is the block's DEFAULT; the exported GXLEDGER names the clean shipped one, so only the strip
   792	            #  decides W5 (deleting `-u GXLEDGER` passed all 35 v2 controls -- GPT-6 Astra, adjudication pass)
   793	            ("W5 Q2 ignores an exported GXLEDGER naming a clean ledger", w_tools("5", new_led), {"GXLEDGER": LEDGER},
   794	             "BAD", 1, "beyond the frozen legacy ceiling"),
   795	            #  the checker ABSENT: the missing-file branch was exercised by no v3 row, so `bad` -> `good` there passed
   796	            #  (GPT-6 Astra, v3 pass)
   797	            ("W6 Q2 with the checker absent", w_tools("6", LEDGER, nochecker=True), {}, "BAD", 1, "MISSING"),
   798	            #  v5: ANY status other than 0 and 1 is "could not run" -- `else' narrowed to `elif [ $_cedrc -eq 2 ]' passed all 72
   799	            #  v4 controls, leaving rc 7 or 127 silently green (GPT-6 Astra, Fable 5.1, v4 pass).  W7's message is on STDERR,
   800	            #  which the section captures with 2>&1; W8 is a real launch failure: python is not on the PATH it is given
   801	            ("W7 Q2 with a checker that exits 7, its message on stderr",
   802	             w_tools("7", LEDGER, stub='import sys\nsys.stderr.write("STUB CHECKER ON STDERR\\n")\nsys.exit(7)\n'), {},
   803	             "BAD", 1, "could not run (rc 7): STUB CHECKER ON STDERR"),
   804	            ("W8 Q2 with python absent from PATH (rc 127)", w_tools("8", LEDGER),
   805	             {"PATH": os.path.join(os.path.dirname(os.path.dirname(BASH)), "usr", "bin")}, "BAD", 1, "could not run (rc 127)")):
   806	        env = dict(os.environ)
   807	        for k in ("GXLEDGER", "GXDOMAIN_BASELINE", "PYTHONIOENCODING", "PYTHONUTF8"):
   808	            env.pop(k, None)
   809	        env.update(envx)
   810	        r = subprocess.run([BASH, blk.replace("\\", "/"), tools.replace("\\", "/")], capture_output=True, env=env)
   811	        outl = r.stdout.decode("cp1252", "replace").strip().splitlines()
   812	        firstl = outl[0] if outl else ""
   813	        fl = [l for l in outl if l.startswith("FAILURES ")]
   814	        nf = int(fl[-1].split()[1]) if fl else -1
   815	        #  W2's refusal must also NAME the entry to the committer: deleting Q2's `printf | sed` passed every v3 control, which
   816	        #  read only the first line and the counter (Grok 4.7, v3 pass)
   817	        named = (not lab.startswith("W2 ")) or any(l.strip().startswith("OFF-DOMAIN ANSWER  row") for l in outl)
   818	        ok = firstl.startswith(want + " ") and msg in firstl and ((nf == 0) if wantf == 0 else (nf >= 1)) and named
   819	        say(lab, ok, "%s | failures %d" % (firstl[:90], nf))
   820	
   821	shutil.rmtree(T, ignore_errors=True)
   822	print("DASHOKCLASS CONTROLS: %d/%d as expected" % (sum(res), len(res)))
   823	print("DASHOKCLASS_CONTROLS_DONE")
   824	sys.exit(0 if all(res) else 1)
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
+  at landing.  Controls `regress/artifacts/dashokclass_20261016/RECEIPT_v5_on_staged_v5.txt`; kill table `regress/artifacts/dashokclass_20261016/KILLTABLE_v5_staged.txt`.
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
  closure: {"by": "opus5-mainloop", "badge": "A", "note": "CLOSED by the dashokclass landing (RULINGS_C F2): every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class, 'legacy -- verdict unclassified', its text kept and its reason in the tooltip; precommit Q2 (check_entry_domain.py) holds the off-domain answers to a ceiling frozen at landing -- per (row, phase, seat, date, d, note sha1), no more answers than the md5-pinned baseline holds.  The guarantee is the narrower one, in GPT-6 Astra's words: current selected-content multiplicities cannot exceed their landing baseline.  Witness: R2, 670 cells moved from the seat-failure class to legacy with nothing else changing.  The controls' CONTRACT rows the DUAL edge of every pin -- for each decision of the checker, the renderer change and Q2, the edit an earlier pin would not see -- or discloses it with its reason.  Five passes on the staged files -- pass 2, the adjudication pass and the v3, v4 and v5 passes, the owner's four-seat roster each time (Opus, agy, kimi, deepseek and minimax not fired)."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- GPT-6 Astra: a per-(row, phase, seat, date, d) count let a converted entry's allowance be refilled by a new answer (measured rc 0); the tooltip's 'not approval, not a seat failure' is contradicted by legacy answers whose notes record real failures; the baseline writer's placement is no guard.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/codex_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "PASS 2 (v1): SHIP WITH CHANGES (4) -- GLM 5.3: the rc-2 path through the gate untested, no escapable-d fixture, no refill control, no legend line for an explicit blank.  All added in v2 (W3, R1b, C15, the legend line).", "ev": "regress/artifacts/dashokclass_20261016/pass2/glm_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "PASS 2 (v1): SHIP WITH CHANGES (7) -- Fable 5.1 (agent_models.py: clean claude-fable-5-1): the refill measured; CUTOFF moved to 2026-10-18 passed all 19 v1 controls; the precommit's cp1252 pipe raised UnicodeEncodeError on the failure lines; legacy answers whose notes name a non-answer; control gaps in C1, C11, R1-R3, W1-W2.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/fable5_dashok.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "PASS 2 (v1): SHIP WITH CHANGES (3) -- Grok 4.7: an exported GXDOMAIN_BASELINE was honoured inside the hook; the loader kept the LAST count for a repeated key; the tooltip's denial and the unpinned inclusive cutoff.  All addressed in v2.", "ev": "regress/artifacts/dashokclass_20261016/pass2/grok_dashok.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "codex", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GPT-6 Astra: the 'identity' key is a CEILING over selected content (a byte-identical revert and a same-note replacement pass; 1,342 keys cover 1,356 answers) -- state the narrower guarantee or build provenance; three one-edit survivors (the tooltip clause restored after the checked prefix, `-u GXLEDGER` deleted, the loader's += made =); the v2 runner named the v1 controls; four claims to correct.  All applied in v3, the narrower guarantee stated in its words.", "ev": "regress/artifacts/dashokclass_20261016/f2/codex_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "glm", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- GLM 5.3: d_nonote dies on the baseline mismatch, not on the note (add the coherent two-edit form); the loader's summation pinned by nothing; R1 and R4 pinned prefixes only.  All applied in v3 (d_nonote2 killed by exactly C15 and C16; C17b; whole-string R1 and R4).", "ev": "regress/artifacts/dashokclass_20261016/f2/glm_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "fable5", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v2 receipts reproduce only with v2 under v1's name; six one-edit mutants pass all 35 (the tooltip tail, the malformed-date reason, which Q2 branch fired); three sentences overclaim; and its own pass-2 'note out of the key' was wrong.  All applied in v3.", "ev": "regress/artifacts/dashokclass_20261016/f2/fable5_dashokf2.md", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "grok", "note": "ADJUDICATION PASS (v2): SHIP WITH CHANGES (3) -- Grok 4.7: the note-only toll is this check's, not the ruling's; the Q2 comment's growth claim and 'can only shrink' survived; the raw-byte md5 pin reds a default Git-for-Windows checkout (the main loop measured it the same hour: a fresh clone gives 89d1d370 for 06a3ffc6; Fable 5.1 reproduced it on the v3 pass).  All applied in v3 (the pin folds CRLF; C18b).", "ev": "regress/artifacts/dashokclass_20261016/f2/grok_dashokf2.txt", "d": "✓"}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "opus5", "note": "PASS 2 through the v5 pass, NOT FIRED: outside the owner's four-seat roster; the measurements an Opus seat would make were the main loop's control and kill-table runs, each receipted."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "agy", "note": "PASS 2 through the v5 pass, NOT FIRED: agy is not on the owner's roster for this landing."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "kimi", "note": "PASS 2 through the v5 pass, NOT FIRED: the kimi seat sat outside the roster."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "deepseek", "note": "PASS 2 through the v5 pass, NOT FIRED: GLM 5.3 was the one packet-fed seat fired."}
  + entry: {"date": "2026-10-16", "phase": "review", "seat": "minimax", "note": "PASS 2 through the v5 pass, NOT FIRED: minimax-m3 was given no packet; the roster, not a wall."}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GPT-6 Astra: five one-edit survivors of the 46 (a date suffix, the record line, the class line on non-OK cells, the per-glyph strip, the missing-checker branch); {\"rows\": {}} and a string entry walked as empty and passed; C2c/C2d red without their own entries; four record sentences.  All addressed in v4 (the class closure: ledger_shape, C21d-h, C25, R1e-g, R2 per glyph, W6, isolated C2c/C2d).  Its NOTSEAT advice on not-fired entries is carried as a disagreement (section H counts seats by is_answer).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/codex_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V3 PASS: SHIP WITH CHANGES (3) -- GLM 5.3: the checker-absent and ledger-unreadable edges unpinned; the summary line pinned only on a clean ledger; two stale sentences (RULINGS_C's '5,150 at HEAD', Q2's 'or is a frozen legacy entry' header).  All addressed in v4 (W6, C23, C11's dirty summary, both sentences).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/glm_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Fable 5.1 (clean claude-fable-5-1), measuring in a mirror: both v3 receipts and the table reproduce; `if cls == LEGACY and d == \"OK\"` and its non-blank sibling pass all 46 (R1 pinned ONE cell's tooltip); the MISSING-checker branch; three records sentences; the dashmissingd question omits the section-H collision.  All addressed in v4 (R1g whole tooltips, W6, C24, C26, R1h, the hint, the filing).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/fable5_dashokv3.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V3 PASS: SHIP WITH CHANGES (3) -- Grok 4.7: the glyph set open at the top (a fifth DOMAIN member or D_CLASS key passes); the cutoff pinned on two days; the summary's baseline number and Q2's named-entry lines unread; a tab-only d.  All addressed in v4 (C27, C12 far, C1 baseline, W2 names, R1d tab).", "ev": "regress/artifacts/dashokclass_20261016/v3pass/grok_dashokv3.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "fable5", "note": "V4 PASS: SHIP WITH CHANGES (18) -- Fable 5.1 (claude-fable-5-1 throughout), measuring in a mirror (its receipts copied to v4pass/fable5_meas/): 72/72 and the 66-mutant table reproduce byte for byte; 21 one-edit mutants pass all 72, 15 at decisions v4 listed as pinned, all one shape -- each pin tested ONE edge of its decision (the trailing end of a key field, the first literal line, a number but not its label, a substring, one branch of three); six records sentences false.  All addressed in v5, which rows each pin's dual edge.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/fable5_dashokv4.md", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "codex", "note": "V4 PASS: SHIP WITH CHANGES (4) -- GPT-6 Astra: ten more one-edit survivors run in memory (a row-id strip, a bool or -1 baseline count, a numeric key field, a suffixed matched date, swapped refusal identifiers, the record-adjoining and null tooltips, the strip labels, an invisible legacy glyph) and Q2's else narrowed to rc 2; C24 confounded by the ledger's own NOTSEAT records; J15's 'whole population' false; it WITHDREW its NOTSEAT advice after measuring section H (9/9 untokened, 4/9 tokened).  All addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/codex_dashokv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "grok", "note": "V4 PASS: SHIP WITH CHANGES (6) -- Grok 4.7: six survivors traced against every control -- a null cell rendered pend, membership by a stripped d in both files, the leading end of the key (the CONTRACT's 'C25 edits the ends' false), the whitespace glyph's character set, the ISO $ anchor, the baseline scalars; ruled the not-fired entries stay untokened on this landing.  All addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/grok_dashokv4.txt", "d": "✓"}
  + entry: {"date": "2026-10-17", "phase": "review", "seat": "glm", "note": "V4 PASS: SHIP WITH CHANGES (4) -- GLM 5.3 (glm-5.3:cloud, packet-fed): 5d's 'killed by exactly C15/C16' stale (v4 kills d_nonote2 by C15, C16, C25e, C25f); four decisions it could not settle from the packet -- the note's type (measured by Fable: refused, never skipped), rows absent (pinned in v5, C21i), a renderer null (pinned, R1n), hold/record precedence over an off-domain d (answered by the fixture); J15 overstated.  Addressed in v5.", "ev": "regress/artifacts/dashokclass_20261016/v4pass/glm_dashokv4.txt", "d": "✓"}
  + entry: {"phase": "regress", "seat": "fable5", "date": "2026-10-17", "grade": "UNKNOWN", "grader": "", "ev": "not fired", "note": "[HELD AWAITING SEAT: fable5] dashokclass closed by its landing and owes the REGRESS review, a distinct phase under the regress-is-fable-only directive, batched to the Sunday flagship sign-off after the battery.  The question is in the row's hold_question."}
  hold_question: "REGRESS (held 2026-10-17 at the dashokclass landing): does regress/artifacts/dashokclass_20261016/RECEIPT_v5_on_staged_v5.txt's controls script, run on the landed tools/pipeline/check_entry_domain.py, gen_dashboard.py and precommit section Q2, still give 96/96 -- in particular R2 (only pend -> legacy, 670 cells, the strip string exact), R2b (the fixture strip by exact membership), C15/C16 (the note in the key), C25a-r (each key field byte for byte, at both ends), C17b-i (the baseline row's every clause), C18/C18b (the md5 pin, CRLF folded), C21a-i (a misshapen ledger or baseline is rc 2), C27 (one binding of each glyph set), C28 (a padded glyph), C3/C6/C9/C19a (each refusal line whole), C12 and C12s (the cutoff, the summary exact), R1e/R1g/R1n (whole tooltips, null included), R5 (the CSS) and W4-W8 (exported overrides stripped; the checker absent, an unexpected status and a missing python are BAD) -- and does regress/artifacts/dashokclass_20261016/KILLTABLE_v5_staged.txt's runner still kill every pinned mutant?  Is the record (the checker's docstring, the Q2 comment, the CHANGELOG block, the bug-file closure) true of what shipped, and is the narrower guarantee -- a ceiling over selected content, not an entry identity -- stated where a reader will meet it?"
  state: "closed"
  state_note: "filed 2026-10-09 from Fable 5.1's regress review of stagetokens, finding 4 (regress/artifacts/fablequeue8n_20261009/regress_harness/fable5_regress_harness.md): D_CLASS has keys for the four glyphs only and the cell class is `D_CLASS.get(d, \"pend\")`; HEAD's ledger carries 439 entries with d \"OK\" (a 2026-08-27..31 convention -- wdcnoirq, gdromcondlies, gdromexitsix, shortread, sgireunmapped, ... and n6's 2026-08-30 fable5 assess entry, which the n6 ruling of the same day calls an answer) and HEAD's matrix renders 365 OK cells, all class pend, none ok.  #534's F3 count of ok cells covered the checkmark population only.  Sections H and I never read `d`, so no gate is affected; the rendered matrix is.  Fix: one line in D_CLASS (\"OK\": \"ok\") or a ledger sweep of OK to the checkmark; either owes the controls a DASH row with d \"OK\".  LOW, display only.\n\n[2026-10-17] CLOSED by the dashokclass landing -- and the fix this note prescribes (one D_CLASS line \"OK\": \"ok\", or a ledger sweep of OK to the checkmark) was REPLACED by the three-seat ruling (regress/artifacts/adj_20261016/RULINGS_C_records.md F2), not applied: every explicit d outside the four glyphs, on the answer a cell shows, renders as one LEGACY class (a live hold and a non-answer record keep their own rendering), its text kept, and precommit Q2 holds the off-domain answers to a ceiling frozen at landing.  The 365 above counts OK cells only; the legacy class is 670 displayed cells (1,397 entries) at HEAD 8bf8b5a1."
  witness: "harness:regress/artifacts/dashokclass_20261016/RECEIPT_v5_on_staged_v5.txt -- R2: HEAD's renderer (gen_dashboard_before.py) shows 1,503 displayed cells in the seat-failure class and the staged one 833, the 670 moved now LEGACY with nothing else changing; C1-C28 and W1-W8 pin the entry-domain check and Q2; regress/artifacts/dashokclass_20261016/KILLTABLE_v5_staged.txt kills every pinned mutant (105/105 as recorded, two escapes recorded as equivalent)"
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

### 5d. the CHANGELOG block (a DRAFT: its v5-pass sentence is written from this pass's answers)

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
* Controls `regress/artifacts/dashokclass_20261016/run_controls_v5.py`, 96 rows, its docstring the CONTRACT: each decision
  of the checker, the renderer change and Q2, with the rows standing on BOTH edges of it -- v5 rows the dual edge of every
  pin, the edit an earlier pin would not see -- and what is disclosed with its reason.  96/96 on the staged files, installed
  byte for byte (`RECEIPT_v5_on_staged_v5.txt`; the md5s are in its header).  Kill table `run_mutants_v5.py`: 105/105 as
  recorded (`KILLTABLE_v5_staged.txt`) -- 103 mutants killed by the rows their lines name, `d_notenone` (0 of 1,356
  off-domain answers has an empty note) and `d_isosearch` (the pattern is `^`-anchored) equivalent escapes; `d_nonote2` and
  `d_dfold2` are deliberate two-edit DESIGN mutants (the coherent forms), killed by C15/C16 and by C25d.  A fold of `d`, or a
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
4/9 tokened), the rule question carried by `dashmissingd`.  **V5 pass** (`v5pass/`): [to be written from its answers].
Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.

