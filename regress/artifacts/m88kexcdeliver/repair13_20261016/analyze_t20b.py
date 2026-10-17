"""analyze_t20b.py -- TABLE 20b (the corrected v24): each log's true red set beside PRETABLE_20b.out's predictions."""
import io, os, re
D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, "m88k_exc_probe_v24b.FROZEN.py"), encoding="utf-8").read()
EXPECT_RESULT = eval(re.search(r"^EXPECT_RESULT = (\{[^\n]*\})", src, re.M).group(1))
FZ = ["errdslotmisalign", "errdslotovf", "errdslotdiv0", "errdslotpriv", "errdslotunimpl", "trapfrozen7dslot",
      "trapfrozen10dslot", "trapfrozen4dslot", "trapfrozen5dslot", "trapfrozen6dslot", "trapfrozen8dslot", "trapfrozen9dslot"]
P = [("BASE", "84/84", []), ("M_DS865", "72/84", FZ), ("M_RRDS_INTEGER_OVERFLOW", "83/84", ["trapfrozen9dslot"]),
     ("M_ARMTS_INTEGER_OVERFLOW", "82/84", ["dslotovftb", "trapfrozen9dslot"]),
     ("M_DSNOT_INTEGER_OVERFLOW", "80/84", ["dslotovf", "errdslotovf", "dslotovftb", "trapfrozen9dslot"]),
     ("M_DSFRZ_INTEGER_OVERFLOW", "82/84", ["errdslotovf", "trapfrozen9dslot"]),
     ("M_RRTDS", "77/84", ["trapfrozen4dslot", "trapfrozen5dslot", "trapfrozen6dslot", "trapfrozen8dslot",
                           "trapfrozen9dslot", "trapfrozen7dslot", "trapfrozen10dslot"])]
allok = True
for tag, ps, pr in P:
    f = os.path.join(D, "t20b_%s.out" % tag)
    if not os.path.exists(f):
        print("%-30s MISSING" % tag); allok = False; continue
    t = io.open(f, encoding="utf-8", errors="replace").read()
    m = re.search(r"M88KEXC_RESULT=(\d+/\d+)", t)
    sc = m.group(1) if m else "??"
    red = []
    for line in t.splitlines():
        mm = re.match(r"M88KEXC_ROW=(\S+)\s+RESULT=(\S+)", line)
        if mm:
            name, res = mm.groups()
            want = "DONE" if name in ("live", "attrib") else EXPECT_RESULT.get(name, "DELIVER")
            if res != want:
                red.append("%s/%s" % (name, res))
    names = sorted(r.split("/")[0] for r in red)
    ok = sc == ps and names == sorted(pr) and "M88KEXC_DONE" in t
    allok &= ok
    print("%-30s %-6s predicted %-6s %s  red: %s" % (tag, sc, ps, "AS PREDICTED" if ok else "*** DIFFERS ***", " ".join(red) or "(none)"))
print("TABLE 20b: %s" % ("ALL AS PREDICTED" if allok else "SOME DIFFER"))
