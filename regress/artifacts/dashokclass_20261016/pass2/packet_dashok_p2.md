# PASS 2 -- `dashokclass`: the dashboard's LEGACY class for an explicit `d` outside its four glyphs, and the forward domain check (precommit Q2)

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a records tool (the generator of the project's
review dashboard) and a pre-commit check.  READ-ONLY: write nothing to any project tree.  The tree under review is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the proposed files are STAGED, not yet in the tree, under
`regress/artifacts/dashokclass_20261016/staged/` (they mirror `tools/...`), and everything a packet-fed seat needs is
inlined below.  Ignore the pristine upstream copy at `C:/DocumentNoSnc/cc/GXEMUL/src/`.

**Please do not simply ratify -- check the premises, not just the derivations.**

Open with your seat token -- `FABLE_DASHOK_20261016` / `ASTRA_DASHOK_20261016` / `GROK_DASHOK_20261016` /
`GLM_DASHOK_20261016` -- then ONE line: `VERDICT: SHIP / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`.

## 1. What the three-seat adjudication ruled (RULINGS_C_records.md, F2 -- Fable 5.1, GPT-6 Astra, Grok 4.7)

* Every mechanical sweep of the existing entries stays WITHDRAWN (3/3): no batch rewrite of any `"d": "OK"`; an OK becomes
  ✓ or anything else only when a reader rewrites that one entry.
* The legacy class is keyed on the DOMAIN, not the spelling: every explicit `d` outside the four glyphs (✓ ✕ ⏸ …)
  renders as ONE residue class, labelled "legacy -- verdict unclassified" (Astra's wording), text kept, notes and
  hold/record precedence preserved, counted as a FIFTH strip number so the strip sums to the entry total.  Keyed on
  `OK` alone it would leave 958 of 1,397 off-domain entries in the false `pend` (seat-failure) class (Fable's census).
* The forward domain check keeps Astra's four completeness conditions -- (1) a missing `d` = the existing `…` default;
  (2) annotation/hold/record entries pass whatever their `d`; (3) an inclusive cutoff tested before, on and after;
  (4) a positive control for a valid post-cutoff glyph beside the negatives and a cutoff-removed mutant -- and, because a
  date-only cutoff cannot stop a back-dated or undated new entry, it defines grandfathering against the EXISTING ENTRIES
  and the missing-date case.
* Its rendering control must show `OK` NOT rendered as approval, canonical approvals still ✓, and semantic holds/records
  unchanged.  Denominator: 439 stored `OK` entries, 365 displayed `OK` cells (Astra).

## 2. Settled premises (measured 2026-10-16 on HEAD; challenge any of them)

* 5,167 ledger entries; 1,397 carry an explicit `d` outside the four glyphs, of which 1,356 are ANSWERS
  (`stage_tokens.is_answer`) in 1,136 distinct (row, phase, seat, date, d) tuples, multiplicity at most 6.  Top `d`
  values among the answers: OK 439, N/A 248, y 89, 2026-09-09 63, 2026-09-10 56, blank 23, NOT-FIRED 22, NOT FIRED 14,
  HELD 10.  The LATEST off-domain answer is dated 2026-09-19; none is undated; none is dated on or after 2026-10-17.
* The working tree's ledger (it carries a peer session's uncommitted rows) holds NO off-domain answer that HEAD lacks.
* Before vs after on HEAD's ledger (control R2): cell classes ok 1413, hold 52, bad 17, tok 374, none 29401 unchanged;
  pend 1503 -> 833; legacy 670.  So 670 displayed cells moved, and nothing else.
* `gen_dashboard.py`'s answer cell is reached only AFTER the hold and record branches (`live_holds`, `is_answer`), so
  the class change touches answer cells only.

## 3. Dispositions to check -- each is mine, not the ruling's

* **The grandfathering key** is the multiset of (row, phase, seat, date, d) over off-domain ANSWERS, frozen in
  `tools/pipeline/entry_domain_baseline.json` by a ONE-TIME writer kept in the artifacts dir (the checker only reads it).
  Notes are deliberately NOT in the key: editing a grandfathered entry's note (a correction, a defanged marker) must not
  re-arm it; changing its `d`, row, phase, seat or date makes it a new tuple and it then needs a glyph.
* **The cutoff** is 2026-10-17, inclusive -- an off-domain answer dated on/after it fails even if its tuple were in the
  baseline (C12 shows the date test is load-bearing on a fixture that contains such a tuple; no real one exists).
* **Display**: an explicit blank `d` shows `?` (the tooltip says `d = ''`); every `d` is now HTML-escaped (the old cell
  wrote it raw).  The tooltip of a legacy cell opens with "legacy -- verdict unclassified: d = 'OK' is none of ✓ ✕ ⏸ …
  (not approval, not a seat failure)".
* **The strip** reads `1687✓ 17✕ 34⏸ 2032… 1397 legacy · 5167 in all` -- it counts ALL entries by raw `d`, records and holds
  included, as it always did; the fifth number is every explicit off-domain `d`, so the five sum to the total.
* **Q2 is HARD** (it can only fail on an entry added after it lands).

## 4. The renderer -- `git diff` of `tools/pipeline/gen_dashboard.py` (HEAD) against the staged copy (7 hunks)

```diff
diff --git a/tools/pipeline/gen_dashboard.py b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/gen_dashboard.py
index 5e683827..4d55eedc 100644
--- a/tools/pipeline/gen_dashboard.py
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/pipeline/gen_dashboard.py
@@ -72,6 +72,14 @@ if _orphans:
     sys.exit(2)
 
 D_CLASS = {"✓": "ok", "⏸": "hold", "✕": "bad", "…": "pend"}
+#  *** AN EXPLICIT `d` OUTSIDE THOSE FOUR IS NEITHER APPROVAL NOR A SEAT FAILURE, AND UNTIL 2026-10-16 IT RENDERED AS THE
+#  SECOND.  (ledger `dashokclass`; ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, adj_20261016/RULINGS_C_records.md F2.) ***
+#  The fallback was `pend`, so 1,397 entries whose `d` is "OK", "N/A", a date, "y", "HELD", blank ... -- 439 of them "OK",
+#  365 displayed cells -- all read as "no answer / seat failure".  Mapping "OK" to `ok` was REJECTED (it canonises one
+#  off-domain spelling as approval); every mechanical sweep of the entries was withdrawn.  So an explicit `d` the map does
+#  not know renders as ONE residue class, LEGACY, keeping its text, with the reason first in its tooltip; a MISSING `d` is
+#  still `…`.  check_entry_domain.py (precommit Q2) stops new off-domain answers, so this class can only shrink.
+LEGACY = "legacy"
 e = lambda t: html.escape(str(t), quote=True)
 
 BADGE_TIP = {"A": "the author did this review (shown, not hidden)",
@@ -158,12 +166,14 @@ def cell(row, phase, seat):
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
+        tip.insert(0, "legacy -- verdict unclassified: d = %r is none of ✓ ✕ ⏸ … (not approval, not a seat failure)" % d)
     #  #534 F2 pass (codex): both of these lived only in the no-answer branch, so an ANSWER cell hid
     #  them -- a refused RE_READ rendered calm, and a record filed after the seat's answer vanished.
     if st.exempts_stage(ent):
@@ -175,7 +185,7 @@ def cell(row, phase, seat):
     t = e(" — ".join(tip))
     b = f'<sup class="b b-{badge}">{badge}</sup>' if badge else ""
     return (f'<td class="c {cls}"><span class="wrap" tabindex="0">'
-            f'<span class="g">{d}</span>{b}<span class="tip">{t}</span></span></td>')
+            f'<span class="g">{e(d) if str(d).strip() else "?"}</span>{b}<span class="tip">{t}</span></span></td>')
 
 
 def fix_section(row):
@@ -255,10 +265,13 @@ sections = ("".join(fix_section(r) for r in open_rows)
 
 
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
 
 
@@ -369,6 +382,8 @@ tr.ph.st-closed td.c.ok {{ background:color-mix(in srgb, var(--okbg) 55%, var(--
 .c.bad .g {{ color:var(--bad); font-weight:700; }} .c.pend .g {{ color:var(--pend); }}
 .c.none .g {{ color:var(--line); }}
 .c.tok .g {{ color:var(--muted); }}
+td.c.legacy {{ outline:1px dashed var(--line); outline-offset:-3px; }}
+.c.legacy .g {{ color:var(--muted); font-style:italic; font-size:11px; }}
 .b {{ font-size:9.5px; font-weight:700; margin-left:1px; color:var(--accent);
   border:1px solid var(--accent); border-radius:2px; padding:0 2px; vertical-align:6px; }}
 .b-s {{ color:var(--hold); border-color:var(--hold); }}
@@ -404,7 +419,7 @@ footer code {{ color:var(--ink); }}
     <span>{e(bat["when"])} @ {e(bat["head"])}</span></span>
   <span class="chip"><span class="k">flagship</span><b>{e(sid[L["flagship"]]["name"])} ({e(sid[L["flagship"]]["ver"])})</b></span>
   <span class="chip"><span class="k">bugs</span><b>{len(open_rows)} in work · {len(closed_rows)} closed · {len(dropped_rows)} dropped</b></span>
-  <span class="chip"><span class="k">entries</span><b>{n["✓"]}✓ {n["✕"]}✕ {n["⏸"]}⏸ {n["…"]}…</b></span>
+  <span class="chip"><span class="k">entries</span><b>{n["✓"]}✓ {n["✕"]}✕ {n["⏸"]}⏸ {n["…"]}… {n[LEGACY]} legacy · {n["total"]} in all</b></span>
   <span class="chip"><span class="k">updated</span><b>{e(L["updated"])}</b></span>
 </div>
 <div class="matrix-scroll"><table>
@@ -416,6 +431,7 @@ footer code {{ color:var(--ink); }}
   <span><span class="g" style="color:var(--hold)">⏸</span> held / in work</span>
   <span><span class="g" style="color:var(--bad)">✕</span> objection</span>
   <span><span class="g" style="color:var(--pend)">…</span> no answer / seat failure (not agreement)</span>
+  <span><span class="g" style="color:var(--muted);font-style:italic">OK</span> legacy -- an older entry's verdict text outside ✓ ✕ ⏸ … (unclassified: not approval, not a seat failure; hover for it)</span>
   <span><span class="g" style="color:var(--muted)">∅</span> a record, not an answer (exemption or main-loop note; hover for why)</span>
   <span><span class="g" style="color:var(--line)">·</span> no input — input is possible</span>
   <span><sup class="b">A</sup> the author did this review (shown)</span>
```

## 5. The checker -- `tools/pipeline/check_entry_domain.py` (new), whole

```python
#!/usr/bin/env python3
"""A NEW LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR NONE.  2026-10-16, ledger `dashokclass`.

THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer --
or no `d` at all (the renderer's default is …).  MEASURED when this landed: 1,397 ledger entries carried an explicit
`d` OUTSIDE the four -- OK 439, other 399, N/A 253, dates 128, y 89, HELD 31, blank 29, NOT-FIRED 22, WALL 7 (Fable
5.1, regress/artifacts/adj_20261016/fable5/meas_C/okdomain_census.txt) -- and until the same commit every one of them
that reached a cell rendered in the SEAT-FAILURE class, because the renderer's fallback was `pend`.  The renderer now
shows them as one residue class, "legacy -- verdict unclassified" (an explicit `d` it cannot classify is neither
approval nor a seat failure); this check stops that population GROWING.  Ruled by Fable 5.1, GPT-6 Astra and Grok 4.7
(regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old entries is withdrawn --
an OK becomes ✓ or anything else only when a reader rewrites that one entry.

ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt), each held here:
  1. a MISSING `d` passes -- it renders as … ;
  2. an entry that is not an ANSWER passes whatever its `d` -- holds, annotations, records (stage_tokens.is_answer);
  3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
  4. the controls carry a POSITIVE row (a valid glyph after the cutoff passes) beside the negatives and a mutant with
     the baseline removed.

GRANDFATHERING IS AGAINST THE EXISTING ENTRIES, NOT AGAINST A DATE (the ruling's amendment: a date-only cutoff cannot
stop a back-dated or an undated new entry).  An off-domain answer passes only if it is dated BEFORE `CUTOFF` AND its
(row, phase, seat, date, d) tuple is within the count frozen in `entry_domain_baseline.json` -- the off-domain answers
present when this check landed, written once by regress/artifacts/dashokclass_20261016/write_baseline.py and never by
this file.  So a back-dated or undated addition exceeds its tuple's frozen count and fails, and so does any off-domain
answer dated on or after CUTOFF.  Rewriting a grandfathered entry's `d` to a glyph only shrinks the population.

Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
Exit: 0 clean; 1 a new off-domain answer (each named); 2 apparatus failure (baseline or ledger unreadable)."""
import collections, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stage_tokens as st  # noqa: E402

LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
BASELINE = os.environ.get("GXDOMAIN_BASELINE") or os.path.join(HERE, "entry_domain_baseline.json")
DOMAIN = ("✓", "✕", "⏸", "…")      # gen_dashboard.py's D_CLASS keys; the two must agree
CUTOFF = "2026-10-17"               # inclusive: an off-domain answer dated on or after it always fails


def off_domain_answers(ledger):
    """(row, phase, seat, date, d) for every ANSWER entry carrying an explicit `d` outside DOMAIN."""
    out = []
    for r in ledger.get("rows", []):
        for x in r.get("entries", []):
            if "d" not in x or x["d"] in DOMAIN or not st.is_answer(x):
                continue
            out.append((r.get("id"), x.get("phase") or "", x.get("seat") or "", x.get("date") or "", str(x["d"])))
    return out


def main():
    try:
        ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    except Exception as ex:
        print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2
    try:
        base = collections.Counter({tuple(k[:5]): k[5] for k in json.load(io.open(BASELINE, encoding="utf-8"))})
    except Exception as ex:
        print("APPARATUS FAIL: baseline unreadable: %s (%s)" % (BASELINE, ex)); return 2
    cur = off_domain_answers(ledger)
    seen = collections.Counter()
    bad = []
    for t in cur:
        seen[t] += 1
        if t[3] >= CUTOFF:
            bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
        elif seen[t] > base[t]:
            bad.append((t, "not among the %d grandfathered entries of this tuple" % base[t]))
    print("entry domain: %d off-domain answer entries; %d grandfathered (baseline %d); cutoff %s inclusive"
          % (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))
    for (row, phase, seat, date, d), why in bad:
        print("  NEW OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r -- %s"
              % (row, phase, seat, date or "(none)", d, why))
    if bad:
        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"
              % " ".join(DOMAIN))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 6. The precommit wiring -- `git diff` of `tools/precommit_check.sh` (HEAD) against the staged copy

```diff
diff --git a/tools/precommit_check.sh b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/precommit_check.sh
index 4569fd39..48a09557 100644
--- a/tools/precommit_check.sh
+++ b/C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/dashokclass_20261016/staged/tools/precommit_check.sh
@@ -492,6 +492,30 @@ else
 	rm -f "$_mx"
 fi
 
+#  ---- Q2 --------------------------------------------------------------------------
+#  A NEW LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR NONE.  2026-10-16, ledger `dashokclass`
+#  (ruled by Fable 5.1, GPT-6 Astra and Grok 4.7, regress/artifacts/adj_20261016/RULINGS_C_records.md F2).
+#  gen_dashboard.py maps four glyphs; 1,397 entries carried a `d` outside them ("OK" 439 of them) and all that reached a
+#  cell rendered as SEAT FAILURES.  The renderer now shows them as one LEGACY class; this section keeps that class from
+#  growing.  Grandfathering is against the EXISTING ENTRIES (a frozen baseline), not a date, because a date-only
+#  cutoff cannot stop a back-dated or undated addition -- check_entry_domain.py's docstring says how.  HARD: it is
+#  forward-only by construction, so it cannot retro-fail anything that was already there.
+say ""; say "Q2. a new ledger answer carries a d the dashboard classifies"
+CED=$_HERE/pipeline/check_entry_domain.py
+if [ ! -f "$CED" ]; then
+	bad "check_entry_domain.py MISSING -- the entry-domain check proved nothing"
+else
+	_ced=$(python "$CED" 2>&1); _cedrc=$?
+	if [ $_cedrc -eq 0 ]; then
+		good "$(printf '%s\n' "$_ced" | head -1)"
+	elif [ $_cedrc -eq 1 ]; then
+		bad "a NEW ledger answer carries a d outside the four glyphs:"
+		printf '%s\n' "$_ced" | sed 's/^/          /'
+	else
+		bad "check_entry_domain.py could not run (rc $_cedrc): $(printf '%s\n' "$_ced" | head -1)"
+	fi
+fi
+
 #  ---- R ---------------------------------------------------------------------------
 #  A COMMITTED DETECTOR THAT NO GATE RUNS DEFENDS NOTHING BETWEEN BATTERIES.
 #
```

## 7. The controls -- `regress/artifacts/dashokclass_20261016/run_controls.py`, run in a staging copy of the tree (RECEIPT_staged.txt verbatim)

The baseline writer is `write_baseline.py` beside it (one-time; the checker never runs it); the first lines of the baseline:

```
[
["alphactxfail", "assess", "codex", "2026-09-08", "y", 1],
["alphapteprot", "assess", "codex", "2026-09-08", "y", 1],
["alphaswpctxreg", "design", "codex", "2026-09-08", "y", 2],
... (1138 lines)
```

```
# dashokclass controls -- repo C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\f2dash\stage
C1   shipped ledger, shipped baseline                                       ok  rc 0: entry domain: 1356 off-domain answer entries; 1356 grandfathered (baseline 1356); cutoff 2026-10-17 inclusive
C2   on the cutoff, a valid glyph (positive)                                ok  rc 0 (want 0)
C3   on the cutoff, d OK (inclusive)                                        ok  rc 1 (want 1)
C4   after the cutoff, d OK                                                 ok  rc 1 (want 1)
C5   before the cutoff, d OK, a new tuple (back-dated)                      ok  rc 1 (want 1)
C6   undated, d N/A                                                         ok  rc 1 (want 1)
C7   after the cutoff, no d                                                 ok  rc 0 (want 0)
C8   a HELD marker after the cutoff, d HELD                                 ok  rc 0 (want 0)
C9   a second copy of grandfathered (alphactxfail assess codex 2026-09-08 'y') ok  rc 1
C10  grandfathered entries rewritten to a glyph                             ok  rc 0
C11  MUTANT baseline removed: the shipped ledger fails                      ok  rc 1, 1356 entries named
C12  MUTANT cutoff removed: real fails, mutant passes                       ok  real rc 1, mutant rc 0
C13  an unreadable baseline                                                 ok  rc 2
R1   fixture row: class and glyph per seat (AFTER renderer)                 ok  9 cells; mismatches []
R2   shipped ledger BEFORE vs AFTER: only pend -> legacy moves; strip sums  ok  before {'bad': 17, 'hold': 52, 'none': 29401, 'ok': 1413, 'pend': 1503, 'tok': 374} | after {'bad': 17, 'hold': 52, 'legacy': 670, 'none': 29401, 'ok': 1413, 'pend': 833, 'tok': 374} | strip '1687✓ 17✕ 34⏸ 2032… 1397 legacy · 5167 in all'
R3   MUTANT fallback -> ok: R1 must fail                                    ok  9 cells; mismatches [('opus5', ('ok', 'OK'), ('legacy', 'OK')), ('agy', ('ok', '?'), ('legacy', '?')), ('minimax', ('ok', 'N/A'), ('legacy', 'N/A'))]
R3   MUTANT fallback -> pend: R1 must fail                                  ok  9 cells; mismatches [('opus5', ('pend', 'OK'), ('legacy', 'OK')), ('agy', ('pend', '?'), ('legacy', '?')), ('minimax', ('pend', 'N/A'), ('legacy', 'N/A'))]
W1   Q2 on the shipped ledger                                               ok  GOOD entry domain: 1356 off-domain answer entries; 1356 grandfathered (baseline 1356); cutoff 2026-10-17 inclusive
W2   Q2 with a new off-domain answer                                        ok  BAD a NEW ledger answer carries a d outside the four glyphs:
DASHOKCLASS CONTROLS: 19/19 as expected
DASHOKCLASS_CONTROLS_DONE
```

## 8. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **The ruling.**  Does the renderer implement the ruled class exactly -- every explicit `d` outside ✓ ✕ ⏸ … in ONE
   residue class, text kept, a missing `d` still `…`, holds and records untouched -- and does the strip now sum to the
   entry total?  Is "legacy -- verdict unclassified" faithful to Astra's wording, and is anything in the legend or
   tooltip a claim the data does not support?
2. **The grandfathering key.**  Is the (row, phase, seat, date, d) multiset the right key?  Name an edit that adds a NEW
   off-domain answer and still passes Q2 (for example by reusing an existing tuple), and one that blocks a legitimate
   edit.  Is leaving the NOTE out of the key right?  Is the baseline writer's placement (artifacts dir, never run by the
   checker) a sufficient guard against re-baselining to launder an entry?
3. **The cutoff.**  Inclusive 2026-10-17.  Given that the baseline already refuses back-dated and undated additions, does
   the date test add anything real (C12 says it refuses a post-cutoff tuple that is somehow in the baseline), or is it a
   rule kept only because the ruling named it?  What does it do to an entry whose date is malformed (not ISO)?
4. **The controls (section 7).**  Are C1-C13, R1-R3 and W1-W2 each able to fail for the reason they name?  **What is the
   smallest edit to the staged checker, renderer or precommit block that passes all 19 controls and breaks a ruled
   property?**  (A sketch is fine; do not build anything.)
5. **Display.**  `?` for an explicit blank `d`, and HTML-escaping every `d` -- right?  Does the escape change any existing
   cell's rendering (an `&` or `<` in some `d`)?
6. **Which of my dispositions is wrong?**  Name the count you checked.
