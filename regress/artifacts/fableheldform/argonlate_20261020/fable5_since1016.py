"""READ-ONLY, KEYWORD-FREE: every fable5 entry dated >= 2026-10-16 that is_answer() counts, listed to be READ."""
import io, json, sys
sys.path.insert(0, sys.argv[2])
import stage_tokens as st
H = json.load(io.open(sys.argv[1], encoding="utf-8"))["rows"]
o = io.open(sys.argv[3], "w", encoding="utf-8")
n = tot = 0
for r in H:
    for i, e in enumerate(r.get("entries", [])):
        if e.get("seat") == "fable5" and (e.get("date") or "") >= "2026-10-16":
            tot += 1
            if st.is_answer(e):
                n += 1
                o.write("%-18s [%2d] %s %-8s d=%r | %s\n" % (r["id"], i, e.get("date"), e.get("phase"), e.get("d"),
                                                          (e.get("note") or "")[:230].replace("\n", " ")))
o.write("fable5 entries dated >= 2026-10-16: %d ; counted as answers: %d (all listed, read by hand)\n" % (tot, n))
o.close()
