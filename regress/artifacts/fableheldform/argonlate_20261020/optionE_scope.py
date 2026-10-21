"""READ-ONLY: rows whose LIVE holds in section H's STAGES are ALL fable5 -- the set a seat-keyed option E would
let close.  argv[1] ledger copy, argv[2] dir holding the HEAD copy of stage_tokens.py, argv[3] output."""
import io, json, sys
sys.path.insert(0, sys.argv[2])
import stage_tokens as st
rows = json.load(io.open(sys.argv[1], encoding="utf-8"))["rows"]
o = io.open(sys.argv[3], "w", encoding="utf-8")
n = 0
for r in rows:
    live, dates = {}, {}
    for p in ("assess", "research", "review"):
        ents = [e for e in r.get("entries", []) if e.get("phase") == p]
        lh = st.live_holds(ents)
        if lh:
            live[p] = lh
            hd = [e.get("date") for e in ents if st.is_held(e) and "fable5" in st.held_seats(e)]
            dates[p] = (min(hd), max(hd)) if hd else None
    if live and all(v == ["fable5"] for v in live.values()):
        n += 1
        o.write("%-18s state=%-8s live=%s hold dates(min,max)=%s\n" % (r["id"], r.get("state"), live, dates))
o.write("TOTAL %d\n" % n)
o.close()
