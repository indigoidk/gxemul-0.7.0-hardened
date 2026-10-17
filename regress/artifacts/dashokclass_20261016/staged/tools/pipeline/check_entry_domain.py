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
