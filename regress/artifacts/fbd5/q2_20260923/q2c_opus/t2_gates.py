import io, json, collections
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus"
G = ["P", "X1", "X2", "X3", "X4", "X5", "X6", "X6R", "X6W", "X6P", "X7", "X7W", "X7R", "X8", "X9", "X9R", "X9W", "X10",
     "X10R", "X10W", "X11", "X12", "SEEDED", "ZERO", "WIDE", "ONES", "X9,X12", "X7,X10", "P,X1,X2,X3,X4,X5",
     "X6,X7,X9,X10,X11,X12"]
recs = [json.loads(l) for l in io.open(O + "/results_t2.jsonl", encoding="utf-8")]
reds = [r for r in recs if not (r["rows"] == 707 and r["fails"] == 0)]
print("table 2: %d variants, %d red on the full 707" % (len(recs), len(reds)))
for g in G:
    m = sorted(r["vid"] for r in reds if r["gates"][g]["n"] == 0 and r["gates"][g]["done"])
    print("  %-22s turned green %d  %s" % (g, len(m), " ".join(m)))
