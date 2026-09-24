import io, json, re
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus"
recs = [json.loads(l) for l in io.open(O + "/results_all.jsonl", encoding="utf-8")]
order = {v: i for i, v in enumerate(l.split()[0] for l in io.open(O + "/PREDICTIONS_q2e.txt", encoding="utf-8")
                                     if re.match(r"^(B_|IA|TD|PR|J0|W0)", l))}
recs.sort(key=lambda r: order.get(r["vid"], 999))
def fam(n):
    if n.startswith("IDENTITY"): return "ID"
    if re.match(r"^P\d", n): return "P"
    m = re.match(r"^X(\d+) ", n)
    return "X" + m.group(1) if m else "T"
out = io.open(O + "/analysis.txt", "w", encoding="utf-8")
def P(s):
    print(s); out.write(s + "\n")
miss = 0
for r in recs:
    ok = r.get("build") == "ok" and r.get("rows") == 862
    green = ok and r["fails"] == 0
    fl = [x for x in r.get("failing", []) if not x.startswith("IDENTITY")]
    meas = "GREEN" if green else ("RED" if ok else r.get("build"))
    hit = (meas == "RED") == (r["pred"] == "RED")
    miss += not hit
    fs = ",".join(sorted(set(fam(x) for x in fl)))
    P("%-5s %-4s pred=%-10s got=%-5s %s %s" % (r["vid"], r["arm"], r["pred"], meas, "" if hit else "<-- PREDICTION MISSED", r["text"]))
    if fl:
        P("        %d rows [%s]: %s" % (len(fl), fs, " | ".join(fl[:4]) + (" | ..." if len(fl) > 4 else "")))
        if r.get("target"):
            P("        target: %s" % r["target"])
P("variants %d; built %d; warnings %d; red/green prediction misses: %d" % (len(recs), sum(r.get("build") == "ok" for r in recs),
  sum(r.get("warn", 0) for r in recs), miss))
P("GREEN: " + " ".join(r["vid"] for r in recs if r.get("fails") == 0 and r.get("rows") == 862))
P("ANALYSIS_DONE")
