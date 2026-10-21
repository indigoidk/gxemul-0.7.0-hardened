import io, json, sys
a, b, outp = sys.argv[1], sys.argv[2], sys.argv[3]
A = {r["id"]: r for r in json.load(io.open(a, encoding="utf-8"))["rows"]}
B = {r["id"]: r for r in json.load(io.open(b, encoding="utf-8"))["rows"]}
with io.open(outp, "w", encoding="utf-8") as f:
    f.write("A=%s B=%s\n" % (a, b))
    for rid in sorted(set(A) | set(B)):
        ra, rb = A.get(rid), B.get(rid)
        if ra is None:
            f.write("\n== NEW ROW %s state=%s\n" % (rid, rb.get("state"))); continue
        if rb is None:
            f.write("\n== GONE ROW %s\n" % rid); continue
        if ra == rb:
            continue
        f.write("\n== %s\n" % rid)
        for k in sorted(set(ra) | set(rb)):
            if k == "entries":
                continue
            if ra.get(k) != rb.get(k):
                f.write("  FIELD %s:\n    OLD: %s\n    NEW: %s\n" % (k, json.dumps(ra.get(k), ensure_ascii=False), json.dumps(rb.get(k), ensure_ascii=False)))
        ea, eb = ra.get("entries", []), rb.get("entries", [])
        if len(ea) != len(eb):
            f.write("  ENTRIES %d -> %d\n" % (len(ea), len(eb)))
        for i in range(max(len(ea), len(eb))):
            x = ea[i] if i < len(ea) else None
            y = eb[i] if i < len(eb) else None
            if x != y:
                f.write("  [%d]\n" % i)
                if x is None:
                    f.write("    ADDED: %s\n" % json.dumps(y, ensure_ascii=False)); continue
                if y is None:
                    f.write("    REMOVED: %s\n" % json.dumps(x, ensure_ascii=False)); continue
                for k in sorted(set(x) | set(y)):
                    if x.get(k) != y.get(k):
                        f.write("    %s:\n      OLD: %s\n      NEW: %s\n" % (k, json.dumps(x.get(k), ensure_ascii=False), json.dumps(y.get(k), ensure_ascii=False)))
