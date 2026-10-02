#!/usr/bin/env python3
"""mutants529f.py NAME SRC DST -- #529 kill table 6: repair 7 (the IRQ seed nonzero in the TOP lanes).

Imports table 5's mutator (every earlier mutant by name) and exec's the Opus second-closing seat's batch-3 mutator
verbatim (prefix `q_': istat_leak, dog_leak, istat_lane ...).  Adds the byte-lane answer at the other labels.
Every find-text must occur EXACTLY ONCE -- a presence pin.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable5_20260913", "killtable4_20260913", "killtable3_20260913", "killtable2_20260913"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529e as E                                    # noqa: E402

GOTO, g = E.GOTO, E.g
LANE = "odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7))); goto crime_declined;"

M = dict(E.M)
_p = os.path.join(HERE, "mutants_close2_opus_b3.py")
_ns = {}
exec(io.open(_p, encoding="utf-8").read().split("name, path = sys.argv")[0], _ns)
M.update({"q_" + k: v for k, v in _ns["M"].items() if k != "base"})


def lane(label):
    return [(GOTO, g("if (writeflag == MEM_READ && relative_addr == %s) %s" % (label, LANE)))]


M.update({
    # the Opus seat's istat_lane, at the other labels: INTMASK and DOG are seeded and should show;
    # REV, CONTROL and TIME hold 0 in the lanes a label's refused read names -- PREDICTED EQUIVALENT, disclosed
    "l_imask": lane("CRIME_INTMASK"),
    "l_dog":   lane("CRIME_DOG"),
    "l_rev":   lane("CRIME_REV"),
    "l_ctl":   lane("CRIME_CONTROL"),
    "l_time":  lane("CRIME_TIME"),
})

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M))
        sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
