#!/usr/bin/env python3
"""apply_r7_records.py -- repair 6's TEXT-ONLY edits to regress/mvme187_memc_probe.py's docstring (records findings 1, 2, 5, 8, 9 of
regress_20261105/REG_MYTHOS_local.md section 5, and R18 in the contract).  Every edit is an exact string replacement asserted once;
no code line changes (proved afterwards by r6_20261105/textonly_check.py against table6/probe213_frozen.py).  Counts come from
table 6's measured SCORES.txt, read here, never typed: the script refuses unless table 6 is complete (TABLE6_MEMC_DONE).
Usage: python -I apply_r7_records.py <probe>
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T6 = os.path.join(HERE, "table6")
LEGS = ["base", "HEAD", "null_true", "null_absent", "null_false", "B1_cnf_exit", "B2_def_exit", "B3_idx_read"]
EIGHT = ["L_MB_M_xori_any", "L_ME_M_xori_any", "L_DB_D_xori_any", "L_DA_D_xori_any", "L_MT_M_xori_M", "L_MW_M_xori_M",
         "L_DT_D_xori_D", "L_DT_D_idat_W.D"]

log = io.open(os.path.join(HERE, "table6_run.log"), encoding="utf-8").read()
assert "TABLE6_MEMC_DONE" in log, "table 6 is not complete"
sc = {}
order = []
for line in io.open(os.path.join(T6, "SCORES.txt"), encoding="utf-8"):
    p = line.split()
    m = re.search(r" RED=(\S+) PRED=(\S+)$", line.strip())
    sc[p[0]] = (p[3], m.group(1), m.group(2))
    order.append(p[0])
assert order[:8] == LEGS and order[8:16] == EIGHT and len(order) == 673, (order[:16], len(order))
assert all(sc[n][1] == "R18_lines" for n in EIGHT)
variants = order[8:]
red = [n for n in variants if sc[n][0] != "213/213"]
green = [n for n in variants if sc[n][0] == "213/213"]
miss = [n for n in order if sc[n][2] == "MISS"]
assert miss == ["B3_idx_read"], miss            # the one miss, reported in table6/VERDICT.md before this edit
k5 = {}
for line in io.open(os.path.join(os.path.dirname(HERE), "r5_20261105", "PRETABLE_5.out"), encoding="utf-8"):
    if "exact: none -- " in line:
        k5[line.split()[0]] = line.rsplit("-- ", 1)[1].strip()
red_nochange = [n for n in red if k5.get(n) == "NOCHANGE"]
NR, NG, NRN = len(red), len(green), len(red_nochange)
B3 = sc["B3_idx_read"][1].replace("_", " ").replace(",", ", ")
print("table 6: %d variants red, %d green; %d of the red are NOCHANGE; B3 red: %s" % (NR, NG, NRN, B3))
nt, na, nf, nh = (sc[n][0] for n in ("null_true", "null_absent", "null_false", "HEAD"))
assert (nt, na, nf) == ("28/213", "4/213", "5/213") and nh == "29/213", (nt, na, nf, nh)

path = sys.argv[1]
s = io.open(path, encoding="latin-1", newline="").read()
assert "\r" not in s


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


rep("The multi-access sessions are fifteen:\nR3 to R17.", "The multi-access sessions are sixteen:\nR3 to R18.")
rep("no chipid or chiprev readback follows R16's phase-11 tail (adj_p5_20261105/ADJ_MYTHOS_local.md, R1).\n",
    "no chipid or chiprev readback follows R16's phase-11 tail (adj_p5_20261105/ADJ_MYTHOS_local.md, R1).\n"
    "\n"
    "REPAIR 6 (regress_20261105/REG_MYTHOS_local.md section 2(d); 206 -> 213 rows).  R18: three default stores to +0x18 (0x01, 0x01,\n"
    "0x00) and the load back, then three memconf stores (0x01, 0x01, 0x00) and the memconf load; one announce per category, both\n"
    "naming 0x1.  It rows the eight own-latch cells table 5 left green -- L_MB_M_xori_any, L_ME_M_xori_any, L_DB_D_xori_any,\n"
    "L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D and L_DT_D_idat_W.D: 206/206 each in table 5 (r5_20261105/table5/\n"
    "SCORES.txt:2916-2919, :2931, :2936-2937, :2990) and again before R18 (r7_20261105/step1/SCORES.txt:2-9); in table 6 each is red\n"
    "on R18 lines alone (r7_20261105/table6/SCORES.txt:9-16).  Table 6 measured %d more of table 5's green representatives red\n"
    "(PRETABLE_6.out lists all %d).\n" % (NR - 8, NR))
rep("tightened where the summary contradicted it: r6_20261105/RECORDS6_NOTE.md).",
    "tightened where the summary contradicted it: r6_20261105/RECORDS6_NOTE.md; repair 6: r7_20261105/).")
rep("Table 5 (clause (e) below) leaves NO surviving cell in the floor.  COVERED (red in table 5, except the cells disclosed below): any",
    "Table 5 left eight of those cells green, the own-latch cells REPAIR 6 names (regress_20261105/REG_MYTHOS_local.md section\n"
    "2(d)); R18 rows them.  COVERED (red in table 5 or table 6, except the cells disclosed below): any")
rep("DISCLOSED, NOT CLAIMED --\nthe five debt families (665 variants green in table 5, every one predicted; filed in r6_20261105/FILING_memccoverdebt.md with the\n"
    "rows that would close each; a future green variant inside one of them is OUTSIDE this contract, one inside the floor is a breach):",
    "DISCLOSED, NOT CLAIMED --\nsix families (table 5 left 665 variants green, every one predicted; table 6 re-ran them on these 213 rows: %d red, %d green,\n"
    "every one as PRETABLE_6 predicted; (1)-(5) are filed in r6_20261105/FILING_memccoverdebt.md with the rows that would close each; a\n"
    "future green variant inside one of them is OUTSIDE this contract, one inside the floor is a breach):" % (NR, NG))
rep(", or which lands on a set latch\n(1 ^ v is truthy for every store value the rows use: 0x05, 0x07, 0x5a, 0xff, 0xffffffff), or whose only odd driver",
    ", or which lands on a set latch,\nor whose only odd driver")
rep("every nonvacuous single-literal widening is red.  Remedy: family (1)'s two store pairs.  Also disclosed",
    "every nonvacuous single-literal widening is red.  Remedy: family (1)'s two store pairs.  (6) NOCHANGE -- every cell PRETABLE_5\n"
    "classes NOCHANGE (fired on the 206 rows, state unchanged; 148 representatives, its `exact: none -- NOCHANGE` lines, :7789 to\n"
    ":8574, NB4's two among them), except the representatives table 6 measured red (%d, the eight own-latch cells among them).  Also\n"
    "disclosed" % NRN)
rep("and the next default access re-announces; the ungated\n`M ^= idata` at the memconf arm's end was BUILT (L_ME_M_xori_any, classed NOCHANGE, 206/206: PRETABLE_5.out:7792, SCORES.txt:2917)\n"
    "and escapes the same way (M goes 1 -> 2 -> 0 over memconf stores of 0x03 then 0x02).  Neither is a semantic no-op (FILING item 6).",
    "and the next default access re-announces; it is not a\nsemantic no-op (FILING item 6).")
rep("CLAUSE (e) -- catches.  TABLE 5, the record (artifacts/mvme187memcoob/r5_20261105/table5/SCORES.txt; PRETABLE_5.out written before\n"
    "it): 3,575 variants on these 206 rows",
    "CLAUSE (e) -- catches.  TABLE 6, the record for repair 6 (artifacts/mvme187memcoob/r7_20261105/table6/SCORES.txt; PRETABLE_6.out\n"
    "written before it): on these 213 rows the legs and table 5's 665 green variants -- %d variants red, %d green, every variant as\n"
    "predicted; one leg missed its prediction: B3 reddened R17 f3 r2 as well as the four below (r7_20261105/table6/VERDICT.md).\n"
    "TABLE 5 (artifacts/mvme187memcoob/r5_20261105/table5/SCORES.txt; PRETABLE_5.out written before it): 3,575 variants on the then\n"
    "206 rows" % (NR, NG))
assert sc["K_MB_memconf_and_D"][1] == "R18_08_r4" and sc["K_MB_chiprev_and_D"][0] == "213/213", (sc["K_MB_memconf_and_D"],
                                                                                                 sc["K_MB_chiprev_and_D"])
rep("which every controller-0 first store\nof 0x07, 0xff or 0xffffffff leaves unchanged on chiprev (0x01) and memconf (0x03): probe-relative only",
    "which every controller-0 first store\nof 0x07, 0xff or 0xffffffff leaves unchanged on chiprev (0x01) and memconf (0x03), and R18's first store of 0x01 on chiprev\n"
    "(K_MB_memconf_and_D, the memconf form, is red in table 6): probe-relative only")
assert sc["L_ME_M_idat_W.nC"][0] == "213/213", sc["L_ME_M_idat_W.nC"]
rep("the 0x00 controller-0 stores of R3, R7\nand R9 -- are each the last memconf store",
    "the 0x00 controller-0 stores of R3, R7,\nR9 and R18 -- are each the last memconf store")
rep("non-first stores at 0x05, 0xff and 0xffffffff (R3, R5, R9);",
    "non-first stores at 0x05, 0xff and 0xffffffff (R3, R5, R9); R18 adds a first store of 0x01 and non-first stores of 0x01 and\n"
    "0x00 in both categories;")
rep("and the gate's source check (no `memcreg)[` and no `[relative_addr]` in\ndev_mvme187.c) covers latches moved before it;",
    "and the gate's source check (no `memcreg)[` and no `[relative_addr]` in\ndev_mvme187.c) covers latches moved before it, for the read in its old spelling;")
rep("for B3 are R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4 (table 4; the same four in table 5, SCORES.txt:8).",
    "for B3 are R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4 (table 4; the same four in table 5, SCORES.txt:8; table 6 adds R17 f3 r2).")
rep("On\nthese 206 rows the pre-fix build scores 29 of 206 with the symptom PRESENT (33 of the then 148-row probe, 31 of the 118), and the\n"
    "three null media -- /bin/true 27/206, an absent binary 4/206, /bin/false 5/206 -- each CONTROL=FAIL (r5_20261105/table5/\n"
    "SCORES.txt:1-5; on the 148 rows 25, 4 and 5, r4_20261105/table4/SCORES.txt).",
    "On\nthese 213 rows the pre-fix build scores 29 of 213 with the symptom PRESENT (29 of the then 206-row probe, 33 of the 148, 31 of the\n"
    "118), and the three null media -- /bin/true 28/213, an absent binary 4/213, /bin/false 5/213 -- each CONTROL=FAIL (r7_20261105/\n"
    "table6/SCORES.txt:2-5; on the 206 rows 27, 4 and 5, r5_20261105/table5/SCORES.txt:1-5; on the 148 rows 25, 4 and 5,\n"
    "r4_20261105/table4/SCORES.txt).  Clause (c): measured at r7_20261105/table6/SCORES.txt:3-5 (binary media: /bin/true, an absent\n"
    "binary, /bin/false); a build without the device was not run.")
io.open(path, "w", encoding="latin-1", newline="").write(s)
print("APPLIED to %s" % path)
