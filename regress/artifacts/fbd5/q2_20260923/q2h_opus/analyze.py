#!/usr/bin/env python3
"""Score results_all.jsonl against pred3d/pred3e.  Flag: mispredictions, and shapes that FLIP 3d->3e."""
import io, json, os
D = os.path.dirname(os.path.abspath(__file__))
res = [json.loads(l) for l in io.open(D + "/results_all.jsonl", encoding="utf-8") if l.strip()]
order = {v: i for i, v in enumerate(
    "AS01 AS02 AS03 AS04 AS04b AS05 AS06 AS07 AS08 AS09 SR01 SR02 SR03 SR04 SR05 SR06 SR07 SR08 SR09 SR10 SR11 "
    "CX01 CX02 CX03 CX04 CX05 CX06 CX07 CX08 CX09 CX10 RS01 RS02 IAS01 IAS02 FMT01 FW01 FW02 FW03 "
    "QWBIE8 QWBST8 QWBVEND QWBTMRV QTAIL0 QCLRFS QCLRIS QZKTR QIASRD QLATCHX QIASRAW".split())}
res.sort(key=lambda r: order.get(r["vid"], 999))


def state(r):
    if not r:
        return "N/A"
    if r.get("build") != "ok":
        return r.get("build", "?")
    return "RED%d" % r["fails"] if r.get("fails") else "GREEN"


def cls(pred):
    return "RED" if pred == "RED" else "GREEN"  # GREEN-DISC/GREEN-REAL/EQ all -> measured GREEN


mm = flips = 0
print("%-8s %-4s | 3d: pred/got      | 3e: pred/got      | flip  match" % ("vid", "src"))
print("-" * 84)
for r in res:
    p3d, p3e = r.get("pred3d"), r.get("pred3e")
    g3d, g3e = state(r.get("r3d")), state(r.get("r3e"))
    ok3d = p3d is None or (cls(p3d) == "RED") == g3d.startswith("RED")
    ok3e = (cls(p3e) == "RED") == g3e.startswith("RED")
    flip = (g3d != "N/A") and (g3d.startswith("RED") != g3e.startswith("RED"))
    mm += (not ok3d) + (not ok3e)
    flips += flip
    print("%-8s %-4s | %-10s %-6s | %-10s %-6s | %-5s %s" % (
        r["vid"], r.get("src"), str(p3d), g3d, str(p3e), g3e,
        "FLIP" if flip else "", "" if (ok3d and ok3e) else "*** MISPREDICT ***"))
print("-" * 84)
print("shapes %d  mispredictions %d  flips(3d->3e) %d" % (len(res), mm, flips))
# 3e greens still under a NOT COVERED disposition?
g3e_greens = [r for r in res if state(r.get("r3e")) == "GREEN"]
print("\n3e GREENS (%d): each must be GREEN-DISC/GREEN-REAL(disclosed)/EQ per pred3e:" % len(g3e_greens))
for r in g3e_greens:
    print("  %-8s pred3e=%-10s  %s" % (r["vid"], r["pred3e"], r["note"][:76]))
print("\nFLIP detail:")
for r in res:
    if (state(r.get("r3d")) != "N/A" and state(r.get("r3d")).startswith("RED") != state(r.get("r3e")).startswith("RED")):
        print("  %-8s 3d=%s -> 3e=%s   %s" % (r["vid"], state(r["r3d"]), state(r["r3e"]), r["note"][:70]))
        for f in (r["r3e"].get("failing") or [])[:6]:
            print("        3e FAIL: " + f)
