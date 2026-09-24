#!/usr/bin/env python3
"""Q4 records checks against the main loop's own r3d results (results_r3d_w*.jsonl) and the variant catalogue."""
import glob, io, json, re, os
A = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/fbd5/q2_20260923/r3d_20260923"
r3d = {}
for p in glob.glob(A + "/results_r3d_w*.jsonl"):
    for l in io.open(p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); r3d[r["vid"]] = r
cat, cur = {}, None
for l in io.open("existing_edits.txt", encoding="utf-8"):
    if l.startswith("=== "):
        cur = l[4:].strip(); cat[cur] = []
    elif cur:
        cat[cur].append(l.rstrip("\n"))
def st(v):
    r = r3d[v]
    return "GREEN" if r.get("fails") == 0 else ("RED(%d)" % r["fails"] if r.get("fails") else "DIED")
# the `!= 0x10` (and != 0x18 / 0x30 / 0x20) exact-value forms: site from the removed line
site_of = {"odata = d->irq_status & d->irq_enable;": "+0x180", "odata = d->irq_status;": "+0x184",
           "d->irq_enable &= ~idata;": "+0x18c", "odata = d->fiq_status & d->fiq_enable;": "+0x280",
           "odata = d->fiq_status;": "+0x284"}
print("== exact-value forms (a `!= <const>` conjunct), by test and site ==")
for v, lines in sorted(cat.items()):
    add = [x for x in lines if x.startswith("+")]
    if len(add) == 1 and re.search(r"!= 0x(10|18|20|30|55)\)?", add[0]) and v in r3d:
        rem = [x[1:].strip() for x in lines if x.startswith("-")]
        kind = "dir" if "writeflag" in add[0] else ("latch" if "warned" in add[0] else "other")
        print("  %-24s %-6s %-9s %s" % (v, kind, st(v), add[0][1:].strip()))
print("== N_SB16 on r3d ==")
print("  ", st("N_SB16"), r3d["N_SB16"]["failing"])
print("== the W0x instance shapes ==")
for v in ("W02", "W03", "W04", "W05", "W06"):
    print("  %-4s %-6s %s" % (v, st(v), [x for x in cat[v] if x.startswith("+")]))
print("== PR09 / PR04 on r3d ==")
for v in ("PR04", "PR09"):
    print("  %-4s %s %s" % (v, st(v) if v in r3d else "NOT IN TABLE", cat.get(v)))
