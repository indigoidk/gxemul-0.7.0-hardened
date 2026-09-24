#!/usr/bin/env python3
"""Opus seat, #545 q2c: the step-3 table, generated from the result files (never transcribed):
results_all.jsonl + results_t2.jsonl (the 707 rows), wit2_classes.tsv (the differential), wit2/REPLAY_* (replays
outside the search alphabet), ext_results.jsonl (the 28 scratch Z rows)."""
import collections, glob, io, json, os, re

O = os.path.dirname(os.path.abspath(__file__))


def fam(n):
    if n.startswith("IDENTITY"):
        return "ID"
    if re.match(r"^P\d", n):
        return "P"
    m = re.match(r"^X(\d+) ", n)
    return "X" + m.group(1) if m else "T"


R = {}
for fn in ("results_all.jsonl", "results_t2.jsonl"):
    for l in io.open(os.path.join(O, fn), encoding="utf-8"):
        r = json.loads(l)
        R[r["vid"]] = r
W = {}
for ln in io.open(os.path.join(O, "wit2_classes.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = ln.split("\t")
    W[c[0]] = c
REP = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(O, "wit2", "REPLAY_*.txt"))):
    t = io.open(f, encoding="utf-8").read()
    vid = t.splitlines()[0].split()[1]
    seq = re.search(r"REPLAY from (\w+): (.*)", t)
    flg = re.search(r"REPLAY flags: guest-visible (\d)", t)
    REP[vid].append((seq.group(2) if seq else "?", flg and flg.group(1) == "1"))
#  the width-8 variants re-run with 8-byte accesses only at 8-aligned offsets (LDRD/STRD align down to 8)
A8 = {}
for f in glob.glob(os.path.join(O, "wit2_align8", "N_*.txt")):
    t = io.open(f, encoding="utf-8").read()
    if t.rstrip().endswith("rc=0") and "WIT2_DONE" in t:
        dev = re.search(r"START devinit.*?guest-visible (\d+), announce (\d+), internal-only (\d+)", t)
        rnd = re.search(r"RANDOM.*?guest-visible (\d+), announce (\d+), internal (\d+)", t)
        A8[os.path.basename(f)[:-4]] = sum(int(x) for x in dev.groups() + rnd.groups()) == 0
EXT = {}
if os.path.exists(os.path.join(O, "ext_results.jsonl")):
    for l in io.open(os.path.join(O, "ext_results.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        EXT[r["vid"]] = r

# how the contract's NOT COVERED list treats each green that is a real change (measured class != NONE)
DISC = {
    "N_D02": "NOT COVERED: wide data on a declined write", "N_D06": "NOT COVERED: wide data on a declined write",
    "N_D03": "NOT COVERED parenthetical (data stays 0/0x70), NOT its heading 'WIDE DATA'",
    "N_D11": "NOT COVERED parenthetical (data stays 0/0x70), NOT its heading 'WIDE DATA'",
    "N_B10": "NOT COVERED parenthetical (data stays 0/0x70), NOT its heading 'WIDE DATA'",
    "N_T07": "NOT COVERED: latch guard on a field neither branch reads",
    "N_T08": "NOT COVERED: latch guard on a field neither branch reads",
    "N_T10": "NOT COVERED: latch guard on a field neither branch reads",
    "N_H01": "NOT COVERED: the address axis (a widened fold)", "N_H05": "NOT COVERED: other registers' semantics",
}
WIRED = {4, 5, 6, 7, 10, 11, 18}

out = io.open(os.path.join(O, "step3_table.txt"), "w", encoding="utf-8")


def P(s=""):
    print(s)
    out.write(s + "\n")


P("STEP 3 -- %d NEW one-line shapes (none in the 434), scored on the frozen 707 rows; greens classified by the"
  % sum(1 for v in R if v.startswith("N_")))
P("differential (exhaustive to length 3 from DEVINIT's reset over 304 ops, to 2 from the harness's calloc instance, 2M")
P("random of length 4-6); a witness is from DEVINIT's reset.  Z = what the 28 scratch closure rows do to it.")
P("")
P("%-7s %-5s %-6s %-9s %s" % ("id", "arm", "707", "class", "exact new line  ||  red: holders and first failing row  /  green: witness, contract, Z"))
counts = collections.Counter()
undisclosed = []
for vid in sorted((v for v in R if v.startswith("N_")), key=lambda s: (s[:3], s)):
    r = R[vid]
    green = r.get("build") == "ok" and r["rows"] == 707 and r["fails"] == 0
    line = r["text"]
    if not green:
        fl = [x for x in r["failing"] if not x.startswith("IDENTITY")]
        hold = ",".join(sorted(set(fam(x) for x in fl)))
        P("%-7s %-5s %-6s %-9s %s  ||  %d rows [%s]: %s" % (vid, r["arm"], "RED", "-", line, len(fl), hold, fl[0]))
        counts["RED"] += 1
        continue
    w = W.get(vid)
    cls = w[1] if w else "NOT-RUN"
    wit = (w[8] or w[9] or w[10]) if w else ""
    for seq, g in REP.get(vid, []):
        if g:
            cls = "GUEST"
            wit = seq + " [devinit, replay]"
    m = re.match(r"N_SB(\d+)$", vid)
    if A8.get(vid):
        cls = "NONE-A8"
        wit = "(unaligned len 8 only: %s)" % (wit or "-")
    if cls == "NONE-A8":
        contract = "equivalent for guests: len 8 reaches only 8-aligned offsets (LDRD/STRD align down), never this one"
    elif cls in ("NONE", "INTERNAL") and not (m and int(m.group(1)) in WIRED):
        contract = "equivalent"
        if m or vid == "N_S08":
            contract = "equivalent on cats/netwinder: no device drives that bit"
        if cls == "INTERNAL":
            contract = "equivalent: only the latch's nonzero VALUE differs, and it is only ever tested for zero"
        if vid == "N_H05":
            contract = DISC[vid] + " (no divergence on this alphabet)"
    else:
        contract = DISC.get(vid, "NOT DISCLOSED")
    z = EXT.get(vid)
    zs = "" if not z else ("Z: red (%s)" % z["z_failing"][0][:60] if z["fails"] else "Z: still green")
    P("%-7s %-5s %-6s %-9s %s  ||  %s  ||  %s  ||  %s" % (vid, r["arm"], "GREEN", cls, line, wit or "-", contract, zs))
    counts["GREEN " + cls + " " + ("undisclosed" if contract == "NOT DISCLOSED" else "disclosed/eq")] += 1
    if contract == "NOT DISCLOSED":
        undisclosed.append((vid, cls))
P("")
for k, n in sorted(counts.items()):
    P("  %-40s %d" % (k, n))
P("  UNDISCLOSED real changes (%d): %s" % (len(undisclosed), " ".join("%s:%s" % u for u in undisclosed)))
P("  of which guest-visible: %d; host-visible (announce) only: %d" % (
    sum(1 for u in undisclosed if u[1] == "GUEST"), sum(1 for u in undisclosed if u[1] == "HOST")))
zc = [v for v, c in undisclosed if EXT.get(v) and EXT[v]["fails"]]
P("  of which the 28 scratch Z rows turn red: %d (%s)" % (len(zc), " ".join(v for v, c in undisclosed if v not in zc) + " not"))
P("FINAL_TABLES_DONE")
out.close()
