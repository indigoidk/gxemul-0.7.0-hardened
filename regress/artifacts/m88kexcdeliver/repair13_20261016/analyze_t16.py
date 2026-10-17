"""analyze_t16.py -- TABLE 16's true red set per log (the driver's own `red:' column listed every non-DELIVER row,
including the eight rows whose CORRECT answer is HALT).  Expectations are taken from the frozen v20 probe itself."""
import glob, io, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, "m88k_exc_probe_v20.FROZEN.py"), encoding="utf-8").read()
m = re.search(r"^EXPECT_RESULT = (\{[^\n]*\})", src, re.M)
EXPECT_RESULT = eval(m.group(1))
CONTROLS = {"live", "attrib"}
pred = {"BASE": "63/63", "M_DSNOT_MISALIGNED_ACCESS": "62/63 dslotmisalign", "M_DSNOT_UNIMPLEMENTED_OPCODE": "62/63 dslotunimpl",
        "M_DSNOT_PRIVILEGE_VIOLATION": "62/63 dslotpriv", "M_DSNOT_INTEGER_OVERFLOW": "62/63 dslotovf",
        "M_DSNOT_ILLEGAL_INTEGER_DIVIDE": "62/63 dslot", "M_DSNOT_BOUNDS_CHECK_VIOLATION": "63/63 (disclosed escape)",
        "M_DSNOT_ERROR": "63/63 (disclosed escape)", "M_DS_MISALIGNED_ACCESS": "55/63", "M_DS_UNIMPLEMENTED_OPCODE": "58/63",
        "M_DS_PRIVILEGE_VIOLATION": "57/63", "M_DS_INTEGER_OVERFLOW": "54/63"}
pred.update({"16b:BASE": "63/63 (committed form)", "16b:M_RRTRAPJOINT": "62/63 trapfrozensfd1"})
order = ["BASE"] + [k for k in pred if k != "BASE" and not k.startswith("16b:")] + ["16b:BASE", "16b:M_RRTRAPJOINT"]
print("%-32s %-8s %-26s %s" % ("log", "score", "PREDICTED (PRETABLE.out)", "true red set (row/RESULT where RESULT != expected)"))
for tag in order:
    f = os.path.join(D, ("t16b_%s.out" % tag[4:]) if tag.startswith("16b:") else ("t16_%s.out" % tag))
    if not os.path.exists(f):
        print("%-32s MISSING" % tag); continue
    t = io.open(f, encoding="utf-8", errors="replace").read()
    sc = re.search(r"M88KEXC_RESULT=(\d+/\d+)", t)
    done = "M88KEXC_DONE" in t
    red = []
    for line in t.splitlines():
        mm = re.match(r"M88KEXC_ROW=(\S+)\s+RESULT=(\S+)", line)
        if not mm: continue
        name, res = mm.groups()
        want = "DONE" if name in CONTROLS else EXPECT_RESULT.get(name, "DELIVER")
        if res != want:
            red.append("%s/%s" % (name, res))
    print("%-32s %-8s %-26s %s%s" % (tag, sc.group(1) if sc else "??", pred[tag], " ".join(red) or "(none)",
                                     "" if done else "   *** NO COMPLETION SENTINEL"))
print("ANALYZE_T16_DONE")
