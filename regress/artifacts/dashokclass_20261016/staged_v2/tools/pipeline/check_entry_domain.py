#!/usr/bin/env python3
"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS ONE OF THE ENTRIES FROZEN WHEN THIS CHECK LANDED.
2026-10-16, ledger `dashokclass`; precommit section Q2.

THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer -- or no
`d` at all (the renderer's default is …).  MEASURED when this landed (HEAD 8bf8b5a1): 5,177 entries, 1,397 with an explicit
`d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
them as one residue class, "legacy -- verdict unclassified", and this check keeps NEW ones from appearing.  Ruled by Fable
5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md, F2): every mechanical sweep of the old
entries is withdrawn -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.

ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt):
  1. a MISSING `d` passes -- it renders as … (an explicit blank does NOT: it is an off-domain value);
  2. an entry that is not an ANSWER passes whatever its `d` -- holds, annotations, records (stage_tokens.is_answer);
  3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
  4. the controls carry POSITIVE rows (a valid glyph on and after the cutoff passes) beside the negatives.

GRANDFATHERING IS BY ENTRY IDENTITY, NOT BY DATE AND NOT BY COUNT.  An off-domain answer passes only if it is IDENTICAL --
row, phase, seat, date, `d` and NOTE (by its sha1) -- to one frozen in `entry_domain_baseline.json` when this check landed,
and is not dated on or after CUTOFF.  So a new entry fails, a back-dated or undated one fails, a duplicate fails, and an old
one EDITED in any of those fields fails: editing such an entry means giving it a glyph, which is the ruling's way out.
(Pass 2 of this check, 2026-10-16: a per-(row, phase, seat, date, d) COUNT let a converted entry's allowance be refilled by
a new answer, and let a note edit turn a record into an un-normalised answer -- GPT-6 Astra and GLM 5.3; the note is in the
key for that reason.)  The grandfathered population can only shrink.  That is NOT a claim about the dashboard's legacy
count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that reappears when a
newer answer in its cell is removed.

THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`): re-freezing it is a reviewed decision, made by changing that constant in
the same commit with the reason, never by re-running the one-time writer
(regress/artifacts/dashokclass_20261016/write_baseline.py).  A GXDOMAIN_BASELINE override skips the pin, for the controls.
Dates are compared as ISO `YYYY-MM-DD` prefixes; a date in any other form is never "on or after the cutoff", so a malformed
date passes only on an identical frozen entry (none exists).

Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
Exit: 0 clean; 1 an off-domain answer that is not a frozen entry (each named); 2 apparatus failure (baseline or ledger
unreadable or misshapen, or the baseline's md5 is not the pinned one)."""
import collections, hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stage_tokens as st  # noqa: E402

LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
DEFAULT_BASELINE = os.path.join(HERE, "entry_domain_baseline.json")
BASELINE = os.environ.get("GXDOMAIN_BASELINE") or DEFAULT_BASELINE
BASELINE_MD5 = "06a3ffc6929be628c8254fe4e818ee99"      # the md5 of entry_domain_baseline.json as frozen; change only by a reviewed re-freeze
DOMAIN = ("✓", "✕", "⏸", "…")      # gen_dashboard.py's D_CLASS keys; the two must agree
CUTOFF = "2026-10-17"               # inclusive: an off-domain answer dated on or after it always fails
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")


def note_sha(x):
    return hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]


def date_str(x):
    v = x.get("date")
    return v if isinstance(v, str) else ("" if v is None else repr(v))


def off_domain_answers(ledger):
    """(row, phase, seat, date, d, note_sha) for every ANSWER entry carrying an explicit `d` outside DOMAIN."""
    out = []
    for r in ledger.get("rows", []):
        for x in r.get("entries", []):
            if "d" not in x or x["d"] in DOMAIN or not st.is_answer(x):
                continue
            out.append((str(r.get("id")), str(x.get("phase") or ""), str(x.get("seat") or ""), date_str(x), str(x["d"]),
                        note_sha(x)))
    return out


def main():
    #  precommit runs this with stdout on a PIPE, which Windows python opens as cp1252: a glyph or a non-ASCII `d` in the
    #  failure lines raised UnicodeEncodeError and buried the instruction under a traceback (Fable 5.1, pass 2, measured)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    try:
        ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    except Exception as ex:
        print("APPARATUS FAIL: ledger unreadable: %s (%s)" % (LEDGER, ex)); return 2
    try:
        raw = open(BASELINE, "rb").read()
        if BASELINE == DEFAULT_BASELINE and hashlib.md5(raw).hexdigest() != BASELINE_MD5:
            print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
                  "in the same commit, with its reason" % (BASELINE, hashlib.md5(raw).hexdigest(), BASELINE_MD5)); return 2
        base = collections.Counter()
        for k in json.loads(raw.decode("utf-8")):
            if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
                    and k[6] > 0):
                raise ValueError("baseline row %r is not [row, phase, seat, date, d, note_sha, count]" % (k,))
            base[tuple(k[:6])] += k[6]
    except Exception as ex:
        print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
    cur = off_domain_answers(ledger)
    seen = collections.Counter()
    bad = []
    for t in cur:
        seen[t] += 1
        if ISO.match(t[3]) and t[3][:10] >= CUTOFF:
            bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
        elif seen[t] > base[t]:
            why = "not identical to a frozen entry -- a new one, a duplicate, or an old one edited (give it a glyph)"
            if t[3] and not ISO.match(t[3]):
                why += "; its date is not ISO YYYY-MM-DD"
            bad.append((t, why))
    print("entry domain: %d off-domain answer entries; %d frozen (baseline %d); cutoff %s inclusive"
          % (len(cur), len(cur) - len(bad), sum(base.values()), CUTOFF))
    for (row, phase, seat, date, d, ns), why in bad:
        print("  OFF-DOMAIN ANSWER  row %s  phase %s  seat %s  date %s  d %r  note %s -- %s"
              % (row, phase, seat, date or "(none)", d, ns, why))
    if bad:
        print("  -> give each a `d` from %s (or omit `d`, which renders as …); a non-answer record is exempt"
              % " ".join(DOMAIN))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
