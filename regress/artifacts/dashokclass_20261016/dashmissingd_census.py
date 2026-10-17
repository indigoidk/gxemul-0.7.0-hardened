#!/usr/bin/env python3
"""dashmissingd_census.py [ledger.json] -- how many ledger ANSWERS carry no `d`, and how many displayed cells that puts in the
seat-failure glyph (2026-10-17; filed as `dashmissingd` at the `dashokclass` landing).  gen_dashboard.py renders `d =
ent.get("d", "…")`, so an answer without `d` shows `…` -- "no answer / seat failure" -- and precommit Q2 lets a new one in
(Astra's completeness condition 1).  A cell is what the renderer shows: phases assess/research/review/regress, the declared
seats, the latest answer (`_latest`: date, then later-recorded) outside a live hold.  The NON-ANSWER screen is a keyword test
of the note (not fired, seat failure, stalled, walled, refused, ...) -- a CORRELATE, so approximate in both directions; the
first two numbers are exact.  Default ledger: tools/pipeline/ledger.json beside this repo."""
import collections, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
sys.path.insert(0, os.path.join(REPO, "tools", "pipeline"))
import stage_tokens as st  # noqa: E402

L = json.load(io.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "tools", "pipeline", "ledger.json"),
                      encoding="utf-8"))
PH = ["assess", "research", "review", "regress"]
SEATS = [s["id"] for s in L["seats"]]
NOANS = re.compile(r"not fired|seat failure|seat down|did not answer|no answer|stalled|walled|\bwall\b|refused|"
                   r"deliberately not|not run|skipped", re.I)


def latest(xs):
    return max(enumerate(xs), key=lambda t: ((t[1].get("date") or ""), t[0]))[1]


ents = sum(len(r.get("entries", [])) for r in L["rows"])
nod = [x for r in L["rows"] for x in r.get("entries", []) if "d" not in x and st.is_answer(x)]
bym = collections.Counter((x.get("date") or "")[:7] for x in nod)
print("entries: %d | answers with no d: %d (by month: %s; the latest dated %s) | of those, the note names a non-answer: %d"
      % (ents, len(nod), ", ".join("%s %d" % kv for kv in sorted(bym.items())), max((x.get("date") or "") for x in nod),
         sum(1 for x in nod if NOANS.search(x.get("note") or ""))))
cells = cnod = creal = 0
for r in L["rows"]:
    for ph in PH:
        stage = [x for x in r.get("entries", []) if x.get("phase") == ph]
        holds = st.live_holds(stage)
        for s in SEATS:
            if s in holds:
                continue
            a = [x for x in stage if x["seat"] == s and st.is_answer(x)]
            if not a:
                continue
            cells += 1
            lt = latest(a)
            if "d" not in lt:
                cnod += 1
                creal += not NOANS.search(lt.get("note") or "")
print("displayed answer cells: %d | whose latest answer has no d (rendered as the seat-failure glyph): %d | of those, the "
      "note names no non-answer (an answer shown as a failure, by the keyword screen): %d" % (cells, cnod, creal))
#  the section-H collision (v5, 2026-10-17): entries recording a seat NOT FIRED, or naming the roster.  The v3 pass's
#  "158 / 127 / 71" came from a screen whose regex was never written down, and three seats could not reproduce it (Fable 5.1,
#  GPT-6 Astra, Grok 4.7, v4 pass) -- so the screen is HERE, by its regex, and its output is what a record cites.
NOTFIRED = re.compile(r"not[ -]fired|roster", re.I)
nf = [x for r in L["rows"] for x in r.get("entries", []) if NOTFIRED.search(x.get("note") or "")]
nfa = [x for x in nf if st.is_answer(x)]
print("NOT-FIRED screen /%s/i over every entry's note: %d entries | untokened (ANSWERS by stage_tokens.is_answer, so "
      "section H counts each as a recorded seat): %d | of those with no d (each renders the seat-failure glyph): %d"
      % (NOTFIRED.pattern, len(nf), len(nfa), sum(1 for x in nfa if "d" not in x)))
print("DASHMISSINGD_CENSUS_DONE")
