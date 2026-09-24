#!/usr/bin/env python3
"""Collect all 50 shapes into one list.  gen_shapes_b and gen_q2 each clear gen_shapes.V on import, so snapshot
(deepcopy) each generator's variants IMMEDIATELY after importing it.  pred3e overrides pred for the 3e instrument."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def all_shapes():
    import gen_shapes
    A = copy.deepcopy(gen_shapes.variants())          # 37
    import gen_shapes_b
    B = copy.deepcopy(gen_shapes_b.variants())        # 2  (CX09, CX10)
    import gen_q2
    C = copy.deepcopy(gen_q2.variants())              # 11
    out = []
    for v in A + B:
        v["src"] = "q2g"
        v["pred3d"] = v["pred"]
        v["pred3e"] = "RED" if v["vid"] == "IAS01" else v["pred"]
        out.append(v)
    for v in C:
        v["src"] = "q2h"
        v["pred3d"] = None
        v["pred3e"] = v["pred"]
        out.append(v)
    ids = [v["vid"] for v in out]
    assert len(ids) == len(set(ids)), "dup ids: %s" % [x for x in ids if ids.count(x) > 1]
    return out


if __name__ == "__main__":
    s = all_shapes()
    print("total shapes:", len(s))
    fz = open("/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2h/frozen/dev_footbridge.c",
              encoding="utf-8", newline="").read()
    bad = [(v["vid"], fz.count(v["old"])) for v in s if fz.count(v["old"]) != 1 or v["old"] == v["new"]]
    print("anchor errors:", bad)
