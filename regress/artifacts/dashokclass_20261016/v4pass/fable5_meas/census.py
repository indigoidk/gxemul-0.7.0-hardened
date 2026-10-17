#!/usr/bin/env python3
"""Re-derive the packet's numbers from a NAMED ledger file (argv[1]) and the staged baseline (argv[2]).  Read-only."""
import collections, hashlib, io, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[3])      # the repo's tools/pipeline (for stage_tokens)
import stage_tokens as st

L = json.load(io.open(sys.argv[1], encoding="utf-8"))
FOUR = ("✓", "✕", "⏸", "…")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}")
ents = [(r, x) for r in L["rows"] for x in r.get("entries", [])]
print("ledger:", sys.argv[1])
print("rows", len(L["rows"]), "entries", len(ents))
off = [(r, x) for r, x in ents if "d" in x and x["d"] not in FOUR]
offa = [(r, x) for r, x in off if st.is_answer(x)]
print("off-domain entries", len(off), "off-domain ANSWERS", len(offa), "off-domain non-answers", len(off) - len(offa))
print("d types among off-domain entries:", collections.Counter(type(x["d"]).__name__ for r, x in off))
print("null d:", sum(1 for r, x in off if x["d"] is None), " blank d answers:", sum(1 for r, x in offa if x["d"] == ""),
      " blank d entries:", sum(1 for r, x in off if x["d"] == ""))
cd = collections.Counter(str(x["d"]) for r, x in offa)
print("answers' d census (top 12):", cd.most_common(12))
dates = [x.get("date") for r, x in offa]
isodates = [d for d in dates if isinstance(d, str) and ISO.match(d)]
print("latest ISO date among off-domain answers:", max(isodates) if isodates else None,
      "| non-ISO/absent:", len(dates) - len(isodates))
print("off-domain answers with empty/missing note:", sum(1 for r, x in offa if not (x.get("note") or "")))
print("answers with ⏸:", sum(1 for r, x in ents if x.get("d") == "⏸" and st.is_answer(x)),
      " answers with …:", sum(1 for r, x in ents if x.get("d") == "…" and st.is_answer(x)))
keys = collections.Counter((str(r.get("id")), str(x.get("phase") or ""), str(x.get("seat") or ""),
                            x.get("date") if isinstance(x.get("date"), str) else ("" if x.get("date") is None else repr(x.get("date"))),
                            str(x["d"]), hashlib.sha1(str(x.get("note") or "").encode("utf-8")).hexdigest()[:16]) for r, x in offa)
print("distinct six-field keys over off-domain answers:", len(keys), " sum", sum(keys.values()))
# answers with NO d at all
nod = [(r, x) for r, x in ents if "d" not in x and st.is_answer(x)]
print("answers with NO d:", len(nod), " by month:", sorted(collections.Counter((x.get("date") or "")[:7] for r, x in nod).items())[-4:])
# NOT FIRED style entries
kw = re.compile(r"NOT FIRED|not fired|roster", re.I)
nf = [(r, x) for r, x in ents if kw.search(str(x.get("note") or ""))]
nfu = [(r, x) for r, x in nf if st.is_answer(x)]
print("entries whose note says NOT FIRED / roster:", len(nf), " untokened (answers):", len(nfu),
      " of those with no d:", sum(1 for r, x in nfu if "d" not in x))
# the baseline
B = json.load(io.open(sys.argv[2], encoding="utf-8"))
print("baseline rows", len(B), " sum", sum(k[6] for k in B), " non-ISO/empty dates", sum(1 for k in B if not ISO.match(k[4-1])),
      " max count", max(k[6] for k in B))
bk = collections.Counter(tuple(k[:6]) for k in B)
print("baseline keys == ledger keys:", bk == keys, " ledger keys not in baseline:", sum(1 for k in keys if k not in bk),
      " baseline keys not in ledger:", sum(1 for k in bk if k not in keys))
