#!/usr/bin/env python3
"""#545 r3e table -- write PREDICTIONS.tsv/.txt BEFORE any variant is scored.
Carried (the r3d table's 739): r3e only ADDS conjuncts -- X14's kept fields after each access, X6/X9/X10's bytes above
the width -- so a variant red on r3d is predicted red on r3e with every r3d failing row still failing, and a variant
green on r3d is predicted green (none of the 146 changes a field inside an X14 sequence and restores it, or touches a
byte past len).  The new R3E_ shapes are predicted per instrument: r3d (6c92d7e5) and r3e."""
import glob, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
ART = ROOT + "/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923"
R3D = ART + "/r3d_20260923"
OUT = ART + "/r3e_20260923"


def verdict(r):
    if r["build"] != "ok":
        return "BUILD-FAIL"
    if r["rc"] == "TIMEOUT":
        return "HUNG"
    if r["rows"] is None:
        return "DIED" if r["rc"] != 0 else "NO-ROWS"
    if r["rc"] not in (0, 1):
        return "DIED"
    return "RED" if r["fails"] else "GREEN"


setof = {}
for ln in io.open(R3D + "/PREDICTIONS.tsv", encoding="utf-8").read().splitlines()[1:]:
    setof[ln.split("\t")[0]] = ln.split("\t")[1]
rows = []
got = {}
for f in sorted(glob.glob(R3D + "/results_r3d_w*.jsonl")):
    for ln in io.open(f, encoding="utf-8"):
        r = json.loads(ln)
        got[r["vid"]] = r
assert len(got) == 739, len(got)
for vid in sorted(got):
    r = got[vid]
    v = verdict(r)
    assert v in ("RED", "GREEN", "DIED"), (vid, v)
    rows.append((vid, setof.get(vid, "?"), "6c92", v, v, "-", "carried from r3d: %s" % v, r.get("failing", [])))
NEW = [  # vid, on r3d (before), on r3e, n on r3e, why
    ("R3E_CXT1", "GREEN", "RED", "3", "a toggle on each +0x180 decline (codex): r3e's per-decline check reds the two "
     "DEVINIT declines rows (0 -> 1) and the re-arm row (1 -> 0 after its first batch)"),
    ("R3E_WB4", "GREEN", "RED", "96", "a read writes back 4 bytes at len 1/2: X6's declined read (2 widths x 4 states "
     "x first/repeat = 16), X9 and X10's reads at len 1/2 (5 registers x 2 x 4 = 40 each)"),
    ("R3E_WB8", "ANY", "ANY", "ANY", "an 8-byte write-back also overflows the harness's own buf[4] in the timer rows: "
     "outcome not predicted on either instrument -- recorded"),
    ("R3E_GLM1", "RED", "RED", ">=16", "glm: X12/X13 read the FIQ fields after an asserting Clear (their 16 wide/ones "
     "narrow rows at least; X9/X10's asserting Clears too if they read them) -- the SAME n on both instruments"),
    ("R3E_GLM2", "RED", "RED", ">=48", "glm: X6 reads the four fields after a +0x180 decline (48 rows at least) -- "
     "the SAME n on both instruments"),
    ("R3E_BO1", "GREEN", "GREEN", "-", "the caller class, disclosed: a calloc'd cpu's byte order"),
    ("R3E_PC1", "GREEN", "GREEN", "-", "the caller class, disclosed: pc 0"),
    ("R3E_CXD1", "GREEN", "GREEN", "-", "the destination class, disclosed: keyed on fiq_enable bit 0"),
    ("R3E_CXS2", "RED/2", "RED", "2", "codex's dedicated job: the raw status zeroed at the asserted Clears only while "
     "their latch is clear -- E3's two rows, and not the re-arm row"),
]
for vid, before, pd, nd, why in NEW:
    rows.append((vid, "r3enew", "6c92", before, pd, nd, why, []))
os.makedirs(OUT, exist_ok=True)
with io.open(OUT + "/PREDICTIONS.tsv", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("vid\tset\tinstr_before\tbefore\tpred_r3e\tn_r3e\twhy\tfailing_before\n")
    for t in rows:
        fh.write("\t".join(t[:7]) + "\t" + "|".join(t[7]) + "\n")
cnt = {}
for t in rows:
    cnt[(t[1], t[4])] = cnt.get((t[1], t[4]), 0) + 1
with io.open(OUT + "/PREDICTIONS.txt", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("#545 repair 3e (864 rows, no row added) -- PREDICTIONS, written before the table.\n"
             "FIX on r3e: 864 rows, 0 failures, 0 warnings; every ok-line of the r3d FIX run printed again (no rename).\n"
             "RULE: red on r3d -> RED on r3e with every r3d failing row still failing; green on r3d -> GREEN; DIED stays\n"
             "DIED.  A crash after the rows printed now scores DIED, not GREEN (the r3d results have none: every green\n"
             "exited 0, every red 1).\n")
    for k in sorted(cnt):
        fh.write("  %-8s %-6s %d\n" % (k[0], k[1], cnt[k]))
    fh.write("NEW shapes, each on BOTH instruments (r3d = 6c92d7e5, r3e):\n")
    for vid, before, pd, nd, why in NEW:
        fh.write("  %-9s r3d %-6s r3e %-6s n=%-5s %s\n" % (vid, before, pd, nd, why))
print("PREDICTIONS: %d rows -> %s" % (len(rows), OUT))
