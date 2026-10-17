"""analyze_t20.py -- TABLE 20: each log's true red set (RESULT != the v24 probe's own expectation) beside the predictions
written in PRETABLE_20.out before the run."""
import io, os, re

D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, "m88k_exc_probe_v24.FROZEN.py"), encoding="utf-8").read()
EXPECT_RESULT = eval(re.search(r"^EXPECT_RESULT = (\{[^\n]*\})", src, re.M).group(1))

L5 = {"MISALIGNED_ACCESS": ("dslotmisalign", "errdslotmisalign", "dslotmisaligntb", "trapfrozen4dslot"),
      "UNIMPLEMENTED_OPCODE": ("dslotunimpl", "errdslotunimpl", "dslotunimpltb", "trapfrozen5dslot"),
      "PRIVILEGE_VIOLATION": ("dslotpriv", "errdslotpriv", "dslotprivtb", "trapfrozen6dslot"),
      "ILLEGAL_INTEGER_DIVIDE": ("dslot", "errdslotdiv0", "dslotdiv0tb", "trapfrozen8dslot"),
      "INTEGER_OVERFLOW": ("dslotovf", "errdslotovf", "dslotovftb", "trapfrozen9dslot")}
T2 = {"BOUNDS_CHECK_VIOLATION": ("dslotbounds", "trapfrozen7dslot"), "ERROR": ("dsloterror", "trapfrozen10dslot")}
P = [("BASE", "84/84", [])]
for L, (uf, ff, ut, ft) in L5.items():
    P.append(("M_RRDS_" + L, "83/84", [ft]))
    P.append(("M_ARMTSU_" + L, "83/84", [ut]))
for L in ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "BOUNDS_CHECK_VIOLATION",
          "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW", "ERROR"):
    if L in L5:
        uf, ff, ut, ft = L5[L]
        P.append(("M_ARMTS_" + L, "82/84", [ut, ft]))
        P.append(("M_DSNOT_" + L, "80/84", [uf, ff, ut, ft]))
        P.append(("M_DSFRZ_" + L, "82/84", [ff, ft]))
    else:
        u, f = T2[L]
        P.append(("M_ARMTS_" + L, "82/84", [u, f]))
        P.append(("M_DSNOT_" + L, "82/84", [u, f]))
        P.append(("M_DSFRZ_" + L, "83/84", [f]))
FROZEN12 = [v[1] for v in L5.values()] + [v[3] for v in L5.values()] + ["trapfrozen7dslot", "trapfrozen10dslot"]
P += [("M_DS865", "72/84", FROZEN12),
      ("M_RRTDS", "77/84", [v[3] for v in L5.values()] + ["trapfrozen7dslot", "trapfrozen10dslot"]),
      ("M_RRNTDS", "79/84", [v[1] for v in L5.values()]),
      ("M_FBDS", "82/84", ["usfu1dslot", "sfu1hdslot"]),
      ("M_FBFRZDS", "83/84", ["sfu1hdslot"]),
      ("M_RRUT", "84/84", []),
      ("M_DS840UT", "84/84", [])]

allok = True
for tag, ps, pr in P:
    f = os.path.join(D, "t20_%s.out" % tag)
    if not os.path.exists(f):
        print("%-34s MISSING" % tag); allok = False; continue
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
    print("%-34s %-6s predicted %-6s %s  red: %s" % (tag, sc, ps, "AS PREDICTED" if ok else "*** DIFFERS ***",
                                                      " ".join(red) or "(none)"))
print("TABLE 20: %s" % ("ALL AS PREDICTED" if allok else "SOME DIFFER"))
