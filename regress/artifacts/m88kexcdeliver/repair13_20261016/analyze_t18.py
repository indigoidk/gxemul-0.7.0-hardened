"""analyze_t18.py -- TABLE 18's true red sets (RESULT != the v23-candidate probe's own expectation), beside PRETABLE_18."""
import io, os, re
D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, "m88k_exc_probe_v21cand.FROZEN.py"), encoding="utf-8").read()
EXPECT_RESULT = eval(re.search(r"^EXPECT_RESULT = (\{[^\n]*\})", src, re.M).group(1))
pred = [("BASE", "68/68", ""), ("M_DSNOT_MISALIGNED_ACCESS", "66/68", "dslotmisalign errdslot"),
        ("M_DSNOT_UNIMPLEMENTED_OPCODE", "67/68", "dslotunimpl"), ("M_DSNOT_PRIVILEGE_VIOLATION", "67/68", "dslotpriv"),
        ("M_DSNOT_INTEGER_OVERFLOW", "67/68", "dslotovf"), ("M_DSNOT_ILLEGAL_INTEGER_DIVIDE", "67/68", "dslot"),
        ("M_DSNOT_BOUNDS_CHECK_VIOLATION", "66/68", "dslotbounds trapfrozendslot"), ("M_DSNOT_ERROR", "67/68", "dsloterror"),
        ("M_RRNTDS", "67/68", "errdslot"), ("M_RRTDS", "67/68", "trapfrozendslot"), ("M_FBDS", "67/68", "usfu1dslot")]
ok_all = True
for tag, ps, pr in pred:
    t = io.open(os.path.join(D, "t18_%s.out" % tag), encoding="utf-8", errors="replace").read()
    sc = re.search(r"M88KEXC_RESULT=(\d+/\d+)", t).group(1)
    red = []
    for line in t.splitlines():
        m = re.match(r"M88KEXC_ROW=(\S+)\s+RESULT=(\S+)", line)
        if m:
            name, res = m.groups()
            want = "DONE" if name in ("live", "attrib") else EXPECT_RESULT.get(name, "DELIVER")
            if res != want:
                red.append(name)
    match = (sc == ps and sorted(red) == sorted(pr.split()))
    ok_all &= match
    print("%-32s %-6s predicted %-6s red: %-34s %s" % (tag, sc, ps, " ".join(red) or "(none)", "AS PREDICTED" if match else "*** DIFFERS"))
print("ANALYZE_T18 %s" % ("ALL AS PREDICTED" if ok_all else "SOME DIFFER"))
