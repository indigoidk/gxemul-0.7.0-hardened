#!/usr/bin/env python3
"""A LEDGER ANSWER CARRIES A `d` THE DASHBOARD CLASSIFIES -- OR IS WITHIN THE LEGACY CEILING FROZEN WHEN THIS CHECK LANDED.
2026-10-16, ledger `dashokclass`; precommit section Q2.

THE DOMAIN is the four glyphs gen_dashboard.py's D_CLASS maps -- ✓ approved, ✕ objection, ⏸ held, … no answer -- or no
`d` at all (the renderer's default is …).  MEASURED when this landed (HEAD 8bf8b5a1): 5,177 entries, 1,397 with an explicit
`d` outside the four, 1,356 of them ANSWERS (OK 439, N/A 248, y 89, dates, blank 23, NOT-FIRED ...; the latest dated
2026-09-19).  Until the same commit every such answer that reached a cell rendered as a SEAT FAILURE; the renderer now shows
them as one residue class, "legacy -- verdict unclassified", and this check keeps answers with NEW content from appearing.
Ruled by Fable 5.1, GPT-6 Astra and Grok 4.7 (regress/artifacts/adj_20261016/RULINGS_C_records.md F2, which upheld
packet_C_records.md's F2): every mechanical sweep of the old entries is withdrawn, and -- that packet's clause (d), upheld
there without restatement -- an OK becomes ✓ or anything else only when a reader rewrites that one entry.

ASTRA'S FOUR COMPLETENESS CONDITIONS (adj_20261016/astra/C_records/codex_adjC.txt):
  1. a MISSING `d` passes -- it renders as … (an explicit blank does NOT: it is an off-domain value);
  2. an entry that is not an ANSWER passes whatever its `d` -- holds, annotations, records (stage_tokens.is_answer);
  3. the cutoff is INCLUSIVE, and the controls test entries dated before it, on it and after it;
  4. the controls carry POSITIVE rows (a valid glyph on and after the cutoff passes) beside the negatives.

GRANDFATHERING IS A CEILING OVER SELECTED CONTENT -- NOT A DATE, AND NOT AN ENTRY IDENTITY.  An off-domain answer passes
only while the ledger holds no more answers with its (row, phase, seat, date, `d`, sha1 of its NOTE) than
`entry_domain_baseline.json` froze when this check landed, and only if it is not dated on or after CUTOFF.  So UNMATCHED
selected content fails and so does an EXCESS occurrence -- a new answer, a back-dated or undated one, a copy, an old one
EDITED in any of those six fields -- while an admitted replacement, identical in all six, can be new (GPT-6 Astra, v3 pass).
Editing such an entry means classifying it -- a glyph, or no `d` at all (it renders as …), or a non-answer record token if it is not an
answer.  For a NOTE-only correction that is this check's toll, not the ruling's: the ruling withdraws every mechanical sweep
and classifies an entry when a reader rewrites it, and says nothing of note edits (Grok 4.7, adjudication pass).  (Pass 2,
2026-10-16: a per-(row, phase, seat, date, d)
count let a converted entry's allowance be refilled by a new answer with another note, measured by GPT-6 Astra and Fable
5.1; the note is in the key for that reason.)

THE GUARANTEE IS THE NARROWER ONE, in GPT-6 Astra's words at the adjudication pass: CURRENT SELECTED-CONTENT MULTIPLICITIES
CANNOT EXCEED THEIR LANDING BASELINE.  The six fields are not an identity -- 1,342 distinct keys cover the 1,356 frozen
answers -- and the check reads no earlier revision, so three things pass: an entry converted to a glyph and later restored
byte for byte (a revert); a replacement that matches a frozen entry in all six fields and differs only outside them; and an
edit outside them (`ev`, `grade`, `b`; stage_tokens.is_answer reads only the note, so such an edit cannot turn a record into
an answer).  So the count within the ceiling never exceeds 1,356 -- until a reviewed re-freeze changes the pin -- and can
climb back to it after shrinking.  It is not the
dashboard's legacy count, which also includes off-domain non-answer records (condition 2) and an older legacy answer that
reappears when a newer answer in its cell is removed.

THE BASELINE IS PINNED BY ITS MD5 (`BASELINE_MD5`), which makes a re-freeze VISIBLE: it has to change that constant in the
same commit, with its reason, where a reviewer sees both -- never a silent re-run of the one-time writer
(regress/artifacts/dashokclass_20261016/write_baseline.py, which refuses to overwrite without --force).  That the change was
REVIEWED is a practice the pin cannot enforce (GPT-6 Astra and Fable 5.1, adjudication pass).  The md5 is taken with CRLF
folded to LF: this machine's system git sets core.autocrlf=true, and a fresh clone checked the file out as 89d1d370 for
06a3ffc6 (measured at the adjudication pass), which a raw pin would red on every commit.  A GXDOMAIN_BASELINE override skips
the pin, for the controls; precommit Q2 strips it.

The cutoff reads a date only when it OPENS with the ISO shape `YYYY-MM-DD` -- a shape test, not a calendar check: a
"2026-13-45" counts as on or after it and fails; a "2026-02-30" counts as before it and must match a frozen entry.  A date in
any other form, or none, is never "on or after the cutoff", so it passes only by matching a frozen entry -- and the baseline
holds none: 0 of its 1,342 keys carries an empty or non-ISO date (measured at landing).

Usage: check_entry_domain.py          (GXLEDGER overrides the ledger path; GXDOMAIN_BASELINE the baseline's)
Exit: 0 clean; 1 an off-domain answer beyond the frozen ceiling (each named); 2 apparatus failure (baseline or ledger
unreadable or misshapen -- every container level is type-checked before it is walked -- or the baseline's md5 is not the
pinned one)."""
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


def ledger_shape(ledger):
    #  the first structural problem, or None.  A container of the wrong type WALKS AS EMPTY and passes -- {"rows": {}} and a
    #  string entry were rc 0 (GPT-6 Astra, v3 pass) -- so every level is checked before anything is walked
    if not isinstance(ledger, dict):
        return "the ledger is not an object"
    rows = ledger.get("rows")
    if not isinstance(rows, list):
        return "rows is not a list"
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            return "row %d is not an object" % i
        ents = r.get("entries", [])
        if not isinstance(ents, list):
            return "row %r: entries is not a list" % (r.get("id"),)
        for x in ents:
            if not isinstance(x, dict):
                return "row %r: an entry is not an object" % (r.get("id"),)
    return None


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
        md = hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()      # line endings folded: see the docstring
        if BASELINE == DEFAULT_BASELINE and md != BASELINE_MD5:
            print("APPARATUS FAIL: %s has md5 %s, not the pinned %s -- a re-freeze is a reviewed decision: change BASELINE_MD5 "
                  "in the same commit, with its reason" % (BASELINE, md, BASELINE_MD5)); return 2
        base = collections.Counter()
        rows_b = json.loads(raw.decode("utf-8"))
        if not isinstance(rows_b, list):
            raise ValueError("the baseline is not a list")
        for k in rows_b:
            if not (isinstance(k, list) and len(k) == 7 and all(isinstance(v, str) for v in k[:6]) and type(k[6]) is int
                    and k[6] > 0):
                raise ValueError("baseline row %r is not [row, phase, seat, date, d, note_sha, count]" % (k,))
            base[tuple(k[:6])] += k[6]
    except Exception as ex:
        print("APPARATUS FAIL: baseline unreadable or misshapen: %s (%s)" % (BASELINE, ex)); return 2
    shape = ledger_shape(ledger)
    if shape:
        print("APPARATUS FAIL: ledger misshapen: %s (%s)" % (LEDGER, shape)); return 2
    try:
        cur = off_domain_answers(ledger)
    except Exception as ex:      # {"rows": null}, a row that is not an object ... (GPT-6 Astra, adjudication pass)
        print("APPARATUS FAIL: ledger misshapen: %s (%s: %s)" % (LEDGER, type(ex).__name__, ex)); return 2
    seen = collections.Counter()
    bad = []
    for t in cur:
        seen[t] += 1
        if ISO.match(t[3]) and t[3][:10] >= CUTOFF:
            bad.append((t, "dated on or after the cutoff %s" % CUTOFF))
        elif seen[t] > base[t]:
            why = "beyond the frozen ceiling for its six fields -- a new answer, a copy, or an old one edited (classify it)"
            if t[3] and not ISO.match(t[3]):
                why += "; its date is not ISO YYYY-MM-DD"
            bad.append((t, why))
    print("entry domain: %d off-domain answer entries; %d within the frozen ceiling (baseline %d); cutoff %s inclusive"
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
