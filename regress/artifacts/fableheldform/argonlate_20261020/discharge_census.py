import io, json, re, sys
sys.path.insert(0, sys.argv[3])
import stage_tokens as st
rows = json.load(io.open(sys.argv[1], encoding="utf-8"))["rows"]
BROAD = re.compile(r"NOT FIRED|never answered|did not answer|DID NOT ANSWER|no answer|SEAT FAILURE|\bwalled\b|STALLED|not tried|NOT TRIED|HTTP 4\d\d|HTTP 5\d\d|usage limit|quota|outside the owner'?s roster|roster exclu|deliberately not|DELIBERATELY NOT|skipped|SKIPPED|not fired|refused|REFUSED", re.I)
o = io.open(sys.argv[2], "w", encoding="utf-8")
pairs = susp = 0
for r in rows:
    ph = {}
    for i, e in enumerate(r.get("entries", [])):
        ph.setdefault(e.get("phase"), []).append((i, e))
    for p, lst in ph.items():
        for i, h in lst:
            if not st.is_held(h):
                continue
            hd = h.get("date") or ""
            for s in st.held_seats(h):
                dis = [(j, e) for j, e in lst if (e.get("seat") or "").lower() == s and st.is_answer(e) and (e.get("date") or "") > hd]
                if not dis:
                    continue
                pairs += 1
                # suspect if EVERY discharging entry's first 400 chars hit the broad net
                if all(BROAD.search((e.get("note") or "")[:400]) for _, e in dis):
                    susp += 1
                    o.write("%-18s %-9s state=%-7s hold[%d] %s seat=%s discharged by %s\n" % (
                        r["id"], p, r.get("state"), i, hd, s,
                        [(j, e.get("date"), (e.get("note") or "")[:150]) for j, e in dis]))
o.write("\nDISCHARGED (hold, seat) pairs: %d ; every discharging entry hits the broad non-answer net: %d\n" % (pairs, susp))
o.close()
