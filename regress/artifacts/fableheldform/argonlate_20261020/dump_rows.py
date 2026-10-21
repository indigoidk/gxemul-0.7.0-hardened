import io, json, sys
led = sys.argv[1]
ids = sys.argv[2].split(",")
outp = sys.argv[3]
full = len(sys.argv) > 4 and sys.argv[4] == "full"
rows = json.load(io.open(led, encoding="utf-8"))["rows"]
by = {r["id"]: r for r in rows}
with io.open(outp, "w", encoding="utf-8") as f:
    f.write("ledger=%s rows=%d\n" % (led, len(rows)))
    for i in ids:
        r = by.get(i)
        if r is None:
            f.write("== %s: ABSENT\n" % i); continue
        f.write("\n== %s\n" % i)
        for k, v in r.items():
            if k == "entries":
                continue
            s = json.dumps(v, ensure_ascii=False)
            if not full and len(s) > 1500:
                s = s[:1500] + "...<%d chars>" % len(s)
            f.write("  %s: %s\n" % (k, s))
        for n, e in enumerate(r.get("entries", [])):
            note = e.get("note") or ""
            keys = sorted(k for k in e.keys() if k != "note")
            extra = {k: e[k] for k in keys if k not in ("date", "phase", "seat")}
            ex = json.dumps(extra, ensure_ascii=False)
            if not full and len(ex) > 300: ex = ex[:300] + "..."
            nn = note if full else (note[:600] + ("...<%d>" % len(note) if len(note) > 600 else ""))
            f.write("  [%d] %s %s %s | %s\n      extra=%s\n" % (n, e.get("date"), e.get("phase"), e.get("seat"), nn, ex))
