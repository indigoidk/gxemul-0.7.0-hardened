"""analyze_t19.py -- TABLES 19 and 19b: the true red set of each log (RESULT != the probe's own expectation), beside the
predictions written in PRETABLE_19.out / PRETABLE_19b.out before the runs."""
import io, os, re

D = os.path.dirname(os.path.abspath(__file__))


def expect(probe):
    src = io.open(os.path.join(D, probe), encoding="utf-8").read()
    return eval(re.search(r"^EXPECT_RESULT = (\{[^\n]*\})", src, re.M).group(1))


FR = ["errdslotmisalign", "errdslotovf", "errdslotdiv0", "errdslotpriv", "errdslotunimpl", "trapfrozen7dslot", "trapfrozen10dslot"]
T19 = [("BASE", "73/73", [])]
for L, uf, fr in [("MISALIGNED_ACCESS", "dslotmisalign", "errdslotmisalign"), ("UNIMPLEMENTED_OPCODE", "dslotunimpl", "errdslotunimpl"),
                  ("PRIVILEGE_VIOLATION", "dslotpriv", "errdslotpriv"), ("BOUNDS_CHECK_VIOLATION", "dslotbounds", "trapfrozen7dslot"),
                  ("ILLEGAL_INTEGER_DIVIDE", "dslot", "errdslotdiv0"), ("INTEGER_OVERFLOW", "dslotovf", "errdslotovf"),
                  ("ERROR", "dsloterror", "trapfrozen10dslot")]:
    T19.append(("M_DSNOT_" + L, "71/73", [uf, fr]))
    T19.append(("M_DSFRZ_" + L, "72/73", [fr]))
T19 += [("M_DS865", "66/73", FR), ("M_RRTDS", "71/73", ["trapfrozen7dslot", "trapfrozen10dslot"]),
        ("M_RRNTDS", "68/73", FR[:5])]
for L in ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW"):
    T19.append(("M_RRDS_" + L, "73/73", []))
T19.append(("M_FBDS", "72/73", ["usfu1dslot"]))
T19B = [("BASE", "63/63", [])] + [("M_DSFRZ_" + L, "63/63", []) for L in
        ("MISALIGNED_ACCESS", "UNIMPLEMENTED_OPCODE", "PRIVILEGE_VIOLATION", "BOUNDS_CHECK_VIOLATION",
         "ILLEGAL_INTEGER_DIVIDE", "INTEGER_OVERFLOW", "ERROR")] + [("M_DS865", "63/63", [])]


def table(title, prefix, probe, preds):
    exp = expect(probe)
    print("== %s (instrument %s)" % (title, probe))
    allok = True
    for tag, ps, pr in preds:
        f = os.path.join(D, "%s_%s.out" % (prefix, tag))
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
                want = "DONE" if name in ("live", "attrib") else exp.get(name, "DELIVER")
                if res != want:
                    red.append("%s/%s" % (name, res))
        names = sorted(r.split("/")[0] for r in red)
        ok = (sc == ps and names == sorted(pr) and "M88KEXC_DONE" in t)
        allok &= ok
        print("%-34s %-6s predicted %-6s %s  red: %s" % (tag, sc, ps, "AS PREDICTED" if ok else "*** DIFFERS ***",
                                                          " ".join(red) or "(none)"))
    print("%s: %s" % (title, "ALL AS PREDICTED" if allok else "SOME DIFFER"))
    return allok


a = table("TABLE 19", "t19", "m88k_exc_probe_v23.FROZEN.py", T19)
b = table("TABLE 19b", "t19b", "m88k_exc_probe_v20final.FROZEN.py", T19B) if os.path.exists(os.path.join(D, "t19b_BASE.out")) else None
print("ANALYZE_T19_DONE %s" % ("ALL AS PREDICTED" if a and b is not False else "SEE ABOVE"))
