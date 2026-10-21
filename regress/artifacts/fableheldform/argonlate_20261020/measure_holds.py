"""READ-ONLY measurement over a COPY of the ledger (argv[1]); writes argv[2].
Uses the HEAD copy of stage_tokens.py placed in ./st/ (argv[3])."""
import io, json, re, sys
sys.path.insert(0, sys.argv[3])
import stage_tokens as st
led, outp = sys.argv[1], sys.argv[2]
rows = json.load(io.open(led, encoding="utf-8"))["rows"]
KW = re.compile(r"NOT FIRED|SEAT FAILURE|\bwalled\b|STALLED|not tried|NOT TRIED|HTTP 429|HTTP 529|usage limit|DID NOT ANSWER|no answer", re.I)
TEN = ["wiringcliff","sgirekills","sgirandomcolour","mapledmaaddr","xscaleinten","ppcrldimimask",
       "ppcrlwimiwidth","ppcgateimageskip","cxlaunchquotation","dashokclass","fableheldform","ip30abortkill"]
o = io.open(outp, "w", encoding="utf-8")
o.write("ledger=%s rows=%d\n" % (led, len(rows)))

# (1) live holds per stage on the rows of interest
o.write("\n## (1) live_holds per (row, phase) on the fableheldform rows\n")
by = {r["id"]: r for r in rows}
for rid in TEN:
    r = by[rid]
    ph = {}
    for i, e in enumerate(r.get("entries", [])):
        ph.setdefault(e.get("phase"), []).append((i, e))
    for p, lst in ph.items():
        ents = [e for _, e in lst]
        held = [(i, e.get("date"), e.get("seat")) for i, e in lst if st.is_held(e)]
        if not held:
            continue
        o.write("  %-18s %-9s state=%-7s live=%s  held_entries=%s\n" % (rid, p, r.get("state"), st.live_holds(ents), held))

# (2) same-day answered holds anywhere: a HELD entry naming S at date D, and an is_answer entry by S
#     in the same (row, phase) dated == D at a HIGHER index, with NO strictly-later answer by S
o.write("\n## (2) holds a same-day LATER-INDEX answer by the named seat would discharge under an index rule, but the strictly-later rule leaves live\n")
n2 = 0
for r in rows:
    ph = {}
    for i, e in enumerate(r.get("entries", [])):
        ph.setdefault(e.get("phase"), []).append((i, e))
    for p, lst in ph.items():
        ents = [e for _, e in lst]
        live = st.live_holds(ents)
        for i, h in lst:
            if not st.is_held(h):
                continue
            hd = h.get("date") or ""
            for s in st.held_seats(h):
                if s not in live:
                    continue
                same = [(j, (e.get("note") or "")[:140]) for j, e in lst
                        if j > i and (e.get("seat") or "").lower() == s and st.is_answer(e) and (e.get("date") or "") == hd]
                if same:
                    n2 += 1
                    o.write("  %-18s %-9s state=%-7s hold[%d] %s %s ; same-day later answers: %s\n" % (r["id"], p, r.get("state"), i, hd, s, same))
o.write("  TOTAL %d\n" % n2)

# (3) holds DISCHARGED (not live) where every discharging entry (named seat, is_answer, strictly later)
#     reads like a non-answer by the keyword correlate -- the discharge direction of untokenedanswers
o.write("\n## (3) holds discharged ONLY by entries whose first 400 chars match the non-answer keyword correlate\n")
n3 = 0
for r in rows:
    ph = {}
    for i, e in enumerate(r.get("entries", [])):
        ph.setdefault(e.get("phase"), []).append((i, e))
    for p, lst in ph.items():
        ents = [e for _, e in lst]
        live = st.live_holds(ents)
        for i, h in lst:
            if not st.is_held(h):
                continue
            hd = h.get("date") or ""
            for s in st.held_seats(h):
                if s in live:
                    continue
                dis = [(j, e) for j, e in lst if (e.get("seat") or "").lower() == s and st.is_answer(e)
                       and (e.get("date") or "") > hd]
                if dis and all(KW.search((e.get("note") or "")[:400]) for _, e in dis):
                    n3 += 1
                    o.write("  %-18s %-9s state=%-7s hold[%d] %s %s ; discharged only by: %s\n" % (
                        r["id"], p, r.get("state"), i, hd, s,
                        [(j, e.get("date"), (e.get("note") or "")[:160]) for j, e in dis]))
o.write("  TOTAL %d\n" % n3)
o.close()
