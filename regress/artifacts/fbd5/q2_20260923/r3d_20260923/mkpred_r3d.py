#!/usr/bin/env python3
"""#545 r3d table -- write PREDICTIONS.tsv/.txt BEFORE any variant is scored (run from git-bash or WSL).
Carried sets (the r3c table's 711, the Opus seat's 22 q2f shapes): r3d only ADDS conjuncts to existing checks and
fills X12/X13's buffer above the width, so a variant red on r3c is predicted red on r3d with every r3c failing row
still failing (after the one rename), and a variant green on r3c is predicted green -- except the ones named below.
The new R3D_ shapes are predicted per instrument, on r3c (8309c5b7) and on r3d."""
import glob, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
ART = ROOT + "/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923"
R3C = ART + "/r3c_20260923"
OUT = ART + "/r3d_20260923"
OPUS = ROOT + "/_scratchpad/fbd5/q2f/opus/results_all.jsonl"
RENAME = {
    "X14 line 4 raised by a device: Clear 0x10 clears it, CPU line deasserted once":
        "X14 line 4 raised by a device: Clear 0x10 clears it, the raw status kept, CPU line deasserted once",
    "X14 line 4 raised by a device: Clear 0x400 keeps it, CPU line asserted once":
        "X14 line 4 raised by a device: Clear 0x400 keeps it, the raw status kept, CPU line asserted once"}
KEEPS = "X14 DEVINIT timers%s: Clear 0x20 keeps 0x10 pending and enabled: CPU line asserted once"
STATR = "X14 line 4 raised by a device: IRQ_STATUS reads 0x10"
REARM = "X14 line 4 raised by a device: 5 declines, then the legal reads and a Clear re-arm no latch"


def verdict(r):
    if r["build"] != "ok":
        return "BUILD-FAIL"
    if r["rc"] == "TIMEOUT":
        return "HUNG"
    if r["rows"] is None:
        return "DIED" if r["rc"] != 0 else "NO-ROWS"
    return "RED" if r["fails"] else "GREEN"


rows = []
r3c = {}
for f in sorted(glob.glob(R3C + "/results_w*.jsonl")):
    for ln in io.open(f, encoding="utf-8"):
        r = json.loads(ln)
        r3c[r["vid"]] = r
setof = {}
for ln in io.open(R3C + "/PREDICTIONS.tsv", encoding="utf-8").read().splitlines()[1:]:
    setof[ln.split("\t")[0]] = ln.split("\t")[1]
assert len(r3c) == 711, len(r3c)
for vid in sorted(r3c):
    r = r3c[vid]
    v = verdict(r)
    assert v in ("RED", "GREEN", "DIED"), (vid, v)
    fl = [RENAME.get(x, x) for x in r.get("failing", [])]
    rows.append((vid, setof.get(vid, "?"), "8309", v, "RED" if v == "RED" else ("DIED" if v == "DIED" else "GREEN"),
                 "-", "carried from r3c: %s" % v, fl))
opus = [json.loads(l) for l in io.open(OPUS, encoding="utf-8")]
assert len(opus) == 22
for r in opus:
    vid = "OQ_" + r["vid"]
    v = "RED" if r["verdict"] == "FAIL" else "GREEN"
    fl = [RENAME.get(x, x) for x in r.get("failing", [])]
    if r["vid"] == "FS01":
        rows.append((vid, "opusq2f", "8309", v, "RED", "1", "r3d E3: the raw status at the asserted Clear 0x10 "
                     "(0x10 -> 0) -- " + RENAME["X14 line 4 raised by a device: Clear 0x10 clears it, CPU line "
                     "deasserted once"], []))
    else:
        rows.append((vid, "opusq2f", "8309", v, v, str(r["fails"]) if v == "RED" else "-",
                     "carried from the Opus seat's 864 run: %s" % v, fl))
NEW = [  # vid, pred on r3c (8309), n, pred on r3d, n, why
    ("R3D_CXC1", "GREEN", "-", "RED", "2", "E1: the raw status at the DEVINIT Clear 0x20, both timer states (0x18 -> 0)"),
    ("R3D_CXA1", "RED", "1", "RED", "2", "control for E3 at k=1: the re-arm row already reads the status (r3c: 1); "
     "r3d adds the Clear 0x400 row"),
    ("R3D_GF1", "GREEN", "-", "RED", "2", "E2 + E4: fiq_enable 0 -> 1 after an asserted IRQ_STATUS read -- the "
     "status-read row and the re-arm row"),
    ("R3D_DA1", "GREEN", "-", "RED", "1", "E4: a +0x180 decline clearing irq_asserted -- only the re-arm row "
     "declines while asserted"),
    ("R3D_FW1", "GREEN", "-", "RED", "16", "E5: a 4-byte fetch at len 1/2 -- X12 and X13's four narrow Clears in the "
     "wide and ones states (bits the 0xa5 bytes clear: 16 in wide, all in ones); seeded and all-zero hold none"),
    ("R3D_LH1", "GREEN", "-", "GREEN", "-", "disclosed (a latch's HISTORY): no instance declines one site five "
     "times"),
]
for vid, pc, nc, pd, nd, why in NEW:
    rows.append((vid, "r3dnew", "8309", pc + ("/" + nc if nc != "-" else ""), pd, nd, why, []))
os.makedirs(OUT, exist_ok=True)
with io.open(OUT + "/PREDICTIONS.tsv", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("vid\tset\tinstr_before\tbefore\tpred_r3d\tn_r3d\twhy\tfailing_before_renamed\n")
    for t in rows:
        fh.write("\t".join(t[:7]) + "\t" + "|".join(t[7]) + "\n")
cnt = {}
for t in rows:
    k = (t[1], t[4])
    cnt[k] = cnt.get(k, 0) + 1
with io.open(OUT + "/PREDICTIONS.txt", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("#545 repair 3d (864 rows, no row added) -- PREDICTIONS, written before the table.\n"
             "FIX on r3d: 864 rows, 0 failures; every ok-line of the r3c FIX run is printed again, the two asserted\n"
             "Clear rows under their new names (%s).\n" % " / ".join(sorted(RENAME.values())))
    fh.write("RULE: red on r3c -> RED on r3d with EVERY r3c failing row still failing (renamed where renamed); green\n"
             "on r3c -> GREEN, except OQ_FS01 (RED, 1).  r3d adds conjuncts only, plus X12/X13's 0xa5 above the\n"
             "width, which no carried variant reads (none edits the fetch's width).\n")
    for k in sorted(cnt):
        fh.write("  %-8s %-6s %d\n" % (k[0], k[1], cnt[k]))
    fh.write("NEW shapes, each on BOTH instruments (r3c = 8309c5b7, r3d):\n")
    for vid, pc, nc, pd, nd, why in NEW:
        fh.write("  %-9s r3c %-5s n=%-2s  r3d %-5s n=%-2s  %s\n" % (vid, pc, nc, pd, nd, why))
    fh.write("Named rows for the new reds on r3d:\n  CXC1: %s ; %s\n  GF1: %s ; %s\n  DA1: %s\n"
             "  CXA1: %s ; %s\n" % (KEEPS % "", KEEPS % ", a tick pending", STATR, REARM, REARM, REARM,
                                    RENAME["X14 line 4 raised by a device: Clear 0x400 keeps it, CPU line asserted once"]))
print("PREDICTIONS: %d rows -> %s" % (len(rows), OUT))
