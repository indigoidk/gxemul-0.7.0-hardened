import io, json, re, collections
O = "/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus"
def fam(n):
    if n.startswith("IDENTITY"): return "ID"
    if re.match(r"^P\d", n): return "P"
    m = re.match(r"^X(\d+) ", n)
    return "X" + m.group(1) if m else "T"
recs = [json.loads(l) for l in io.open(O + "/results_t2.jsonl", encoding="utf-8")]
print("records", len(recs), "gated_same all:", all(r.get("gated_same") for r in recs), "built all:", all(r.get("build") == "ok" for r in recs))
for r in sorted(recs, key=lambda r: r["vid"]):
    green = r["rows"] == 707 and r["fails"] == 0
    fl = [x for x in r["failing"] if not x.startswith("IDENTITY")]
    fs = sorted(set(fam(x) for x in fl))
    sole_gates = [g for g in ("X6W", "X6R", "X6P", "X7W", "X7R", "X9R", "X9W", "X10R", "X10W", "X12", "ONES", "WIDE", "SEEDED", "ZERO") if r["gates"][g]["n"] == 0 and not green]
    print("%-8s pred=%-10s %-5s n_fail=%-3d holders=%-20s green-if-disabled=%s  %s" % (r["vid"], r["pred"], "GREEN" if green else "RED", len(fl), ",".join(fs), ",".join(sole_gates), (fl[0] if fl else "")))
