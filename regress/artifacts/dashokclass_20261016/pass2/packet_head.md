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
