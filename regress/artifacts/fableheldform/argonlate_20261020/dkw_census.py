"""READ-ONLY: entries counted as answers since 2026-10-01, cross-tabbed by `d' presence and a 12-phrase
non-answer keyword net over the first 400 characters (a CORRELATE, stated as such)."""
import io, json, re, sys
sys.path.insert(0, sys.argv[3])
import stage_tokens as st
H = json.load(io.open(sys.argv[1], encoding="utf-8"))["rows"]
KW = re.compile(r"NOT FIRED|SEAT FAILURE|\bwalled\b|STALLED|not tried|NOT TRIED|HTTP 429|HTTP 529|usage limit|DID NOT ANSWER|no answer|never answered", re.I)
o = io.open(sys.argv[2], "w", encoding="utf-8")
c = {}
for r in H:
    for i, e in enumerate(r.get("entries", [])):
        if st.is_answer(e) and (e.get("date") or "") >= "2026-10-01":
            k = ("d" if e.get("d") else "no-d", "kw" if KW.search((e.get("note") or "")[:400]) else "no-kw")
            c[k] = c.get(k, 0) + 1
            if k == ("d", "kw"):
                m = KW.search((e.get("note") or "")[:400])
                o.write("d+kw  %-18s [%2d] %s %-7s %-6s match=%r | %s\n" % (r["id"], i, e.get("date"), e.get("phase"), e.get("seat"), m.group(0), (e.get("note") or "")[:200]))
o.write("counts: %s ; total counted answers since 2026-10-01: %d\n" % (c, sum(c.values())))
o.close()
