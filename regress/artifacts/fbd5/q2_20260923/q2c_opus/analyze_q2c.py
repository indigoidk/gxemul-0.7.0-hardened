#!/usr/bin/env python3
"""Opus seat, #545 q2c: analyse results_all.jsonl.

  1. the 434 re-scored on the frozen 707 rows, per variant, against the main loop's opus_rescore.tsv;
  2. the gated binary byte-identical to the frozen one for every variant (FBSKIP unset);
  3. for each gate: which variants red on the full 707 go GREEN with that family disabled at code level, and the same
     set PREDICTED from the full run's failing row names (a row-name filter) -- the two methods must agree;
  4. for each variant, the set of row families holding it (families with at least one failing row), and the SOLE
     holders;
  5. the new shapes: measured against their written predictions.
Writes analysis_*.txt/tsv next to itself.
"""
import collections, io, json, os, re, sys

O = os.path.dirname(os.path.abspath(__file__))
RESCORE = "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/repair2/opus_rescore.tsv"
GATES = ["P", "X1", "X2", "X3", "X4", "X5", "X6", "X6R", "X6W", "X6P", "X7", "X7W", "X7R", "X8", "X9", "X9R", "X9W",
         "X10", "X10R", "X10W", "X11", "X12", "SEEDED", "ZERO", "WIDE", "ONES", "X9,X12", "X7,X10",
         "P,X1,X2,X3,X4,X5", "X6,X7,X9,X10,X11,X12"]
STATE_TOKEN = {"SEEDED": "seeded", "ZERO": "all-zero", "WIDE": "wide", "ONES": "ones"}

recs = [json.loads(l) for l in io.open(O + "/results_all.jsonl", encoding="utf-8")]
byid = {r["vid"]: r for r in recs}


def fam(name):
    if name.startswith("IDENTITY"):
        return "ID"
    if re.match(r"^P\d", name):
        return "P"
    m = re.match(r"^X(\d+) ", name)
    if m:
        return "X" + m.group(1)
    return "T"


def state(name):
    m = re.search(r"[ (](seeded|all-zero|wide|ones)[ ,)]", name)
    return m.group(1) if m else None


def in_one(name, g):
    f = fam(name)
    if g in STATE_TOKEN:
        return f in ("X6", "X7", "X9", "X10", "X12") and state(name) == STATE_TOKEN[g]
    if g == "X6R":
        return f == "X6" and "read IRQ_ENABLE_CLEAR" in name
    if g == "X6W":
        return f == "X6" and "read IRQ_ENABLE_CLEAR" not in name
    if g == "X6P":
        return f == "X6" and " repeat:" in name
    if g == "X7W":
        return f == "X7" and " write " in name
    if g == "X7R":
        return f == "X7" and "legal len" in name
    if g == "X9R":
        return f == "X9" and "legal len" in name
    if g == "X9W":
        return f == "X9" and " write " in name
    if g == "X10R":
        return f == "X10" and "legal len" in name
    if g == "X10W":
        return f == "X10" and "IRQ Clear write" in name
    return f == g


def in_gate(name, gate):
    return any(in_one(name, g) for g in gate.split(","))


def failing(r):
    return [x for x in r.get("failing", []) if not x.startswith("IDENTITY")]


def is_green(r):
    return r.get("build") == "ok" and r.get("rows") == 707 and r.get("fails") == 0


out = io.open(O + "/analysis_q2c.txt", "w", encoding="utf-8")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.write(s + "\n")


# ---------------------------------------------------------------- 0. integrity
P("=" * 100)
P("0. INTEGRITY")
P("records:", len(recs), " q2r:", sum(1 for r in recs if not r["vid"].startswith("N_")),
  " new:", sum(1 for r in recs if r["vid"].startswith("N_")))
bad_build = [r["vid"] for r in recs if r.get("build") != "ok"]
P("not built / anchor errors:", bad_build)
nosum = [r["vid"] for r in recs if r.get("build") == "ok" and r.get("rows") is None]
P("no summary line (process died):", nosum)
gsame_bad = [r["vid"] for r in recs if r.get("build") == "ok" and not r.get("gated_same")]
P("gated binary NOT byte-identical to the frozen harness with FBSKIP unset:", gsame_bad)
gdone_bad = [(r["vid"], g) for r in recs if r.get("build") == "ok" for g in GATES if not r["gates"][g]["done"]]
P("gated runs with no summary line:", gdone_bad[:20], "... total", len(gdone_bad))
warn = [r["vid"] for r in recs if r.get("build") == "ok" and (r.get("warn_d") or r.get("warn_g"))]
P("variants whose build printed a -Wall warning:", warn)

# ---------------------------------------------------------------- 1. the 434 re-scored
P("=" * 100)
P("1. THE 434 RE-SCORED ON THE FROZEN 707 ROWS, AGAINST THE MAIN LOOP'S opus_rescore.tsv")
ms = {}
if os.path.exists(RESCORE):
    for ln in io.open(RESCORE, encoding="utf-8").read().splitlines()[1:]:
        c = ln.split("\t")
        ms[c[0]] = c
q = [r for r in recs if not r["vid"].startswith("N_")]
agree = dis = 0
for r in q:
    mine = "green" if is_green(r) else "red"
    m = ms.get(r["vid"])
    theirs = None
    if m:
        theirs = "green" if (m[6] == "707" and m[7] == "0") else "red"
    if theirs == mine:
        agree += 1
    else:
        dis += 1
        P("  DISAGREE", r["vid"], "mine", mine, "main loop", theirs, m)
P("per-variant agreement with the main loop's rescore: %d agree, %d disagree" % (agree, dis))
fams = collections.OrderedDict()
for r in q:
    fams.setdefault(r["family"], [0, 0])
    fams[r["family"]][0] += 1
    fams[r["family"]][1] += is_green(r)
P("family       built  green@707")
for f, (b, g) in fams.items():
    P("  %-12s %4d  %4d" % (f, b, g))
P("  TOTAL        %4d  %4d" % (len(q), sum(is_green(r) for r in q)))

# ---------------------------------------------------------------- 2-3. gates
P("=" * 100)
P("2. FAMILY DISABLED AT CODE LEVEL -> which variants red on the full 707 go GREEN (434 set, then the new shapes)")
P("   'pred' = the same set predicted by filtering the full run's failing row names; 'agree' must be yes")
tsv = io.open(O + "/analysis_gates.tsv", "w", encoding="utf-8")
tsv.write("set\tgate\tturned_green\tpredicted\tagree\tby_family\tvariants\n")
for setname, pool in (("434", q), ("new", [r for r in recs if r["vid"].startswith("N_")])):
    reds = [r for r in pool if r.get("build") == "ok" and not is_green(r)]
    P("-- set %s: %d variants, %d red on the full 707" % (setname, len(pool), len(reds)))
    for g in GATES:
        meas = sorted(r["vid"] for r in reds if r["gates"][g]["n"] == 0 and r["gates"][g]["done"])
        pred = sorted(r["vid"] for r in reds if failing(r) and all(in_gate(x, g) for x in failing(r)))
        agreeflag = "yes" if meas == pred else "NO"
        bf = collections.Counter(byid[v]["family"] for v in meas)
        bfs = " ".join("%s:%d" % kv for kv in sorted(bf.items()))
        P("   %-22s turned green %3d  (pred %3d, agree %s)  %s" % (g, len(meas), len(pred), agreeflag, bfs))
        if meas != pred:
            P("      measured-not-predicted:", sorted(set(meas) - set(pred)))
            P("      predicted-not-measured:", sorted(set(pred) - set(meas)))
        tsv.write("%s\t%s\t%d\t%d\t%s\t%s\t%s\n" % (setname, g, len(meas), len(pred), agreeflag, bfs, " ".join(meas)))
tsv.close()

# ---------------------------------------------------------------- 4. holders
P("=" * 100)
P("4. WHICH ROW FAMILIES HOLD EACH RED VARIANT (families with >= 1 failing row); SOLE HOLDERS")
ht = io.open(O + "/analysis_holders.tsv", "w", encoding="utf-8")
ht.write("vid\tfamily\tarm\ttext\tn_failing\tholding_families\tsole\n")
sole = collections.Counter()
solelist = collections.defaultdict(list)
famhold = collections.defaultdict(collections.Counter)
for r in recs:
    if r.get("build") != "ok" or is_green(r):
        continue
    fs = sorted(set(fam(x) for x in failing(r)))
    s = fs[0] if len(fs) == 1 else ""
    if s:
        sole[s] += 1
        solelist[s].append(r["vid"])
    famhold[r["family"]][",".join(fs)] += 1
    ht.write("%s\t%s\t%s\t%s\t%d\t%s\t%s\n" % (r["vid"], r["family"], r["arm"], r["text"], len(failing(r)), ",".join(fs), s))
ht.close()
P("sole-holder counts over ALL red variants (434 + new):", dict(sole))
for s in sorted(solelist):
    P("  held ONLY by %-4s (%d): %s" % (s, len(solelist[s]), " ".join(solelist[s])))
P("holding-family sets, by variant family:")
for f in famhold:
    P("  %-10s %s" % (f, "; ".join("%s x%d" % kv for kv in famhold[f].most_common())))

# ---------------------------------------------------------------- 5. new shapes
P("=" * 100)
P("5. NEW SHAPES: measured against the written prediction")
nt = io.open(O + "/analysis_new.tsv", "w", encoding="utf-8")
nt.write("vid\tfamily\tarm\tline\tprediction\tmeasured\tn_failing\tfirst_failing_row\tholding_families\n")
for r in recs:
    if not r["vid"].startswith("N_"):
        continue
    if r.get("build") != "ok":
        meas = r.get("build")
        nf, first, fs = "", "", ""
    else:
        g = is_green(r)
        meas = "GREEN" if g else "RED"
        nf = len(failing(r))
        first = failing(r)[0] if failing(r) else "-"
        fs = ",".join(sorted(set(fam(x) for x in failing(r))))
    ok = (meas == "RED") == (r["pred"] == "RED")
    P("  %-6s %-5s %-11s %-6s %s %s | %s" % (r["vid"], r["arm"], r["pred"], meas, "" if ok else "<-- PREDICTION MISSED",
                                            r["text"], first if meas == "RED" else ""))
    nt.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r["vid"], r["family"], r["arm"], r["text"], r["pred"], meas, nf,
                                                      first, fs))
nt.close()
P("new shapes: %d built; green %d; red %d" % (
    sum(1 for r in recs if r["vid"].startswith("N_") and r.get("build") == "ok"),
    sum(1 for r in recs if r["vid"].startswith("N_") and is_green(r)),
    sum(1 for r in recs if r["vid"].startswith("N_") and r.get("build") == "ok" and not is_green(r))))
P("GREEN new shapes:", " ".join(r["vid"] for r in recs if r["vid"].startswith("N_") and is_green(r)))
P("ANALYSIS_DONE")
out.close()
