#!/usr/bin/env python3
"""mutants529d.py NAME SRC DST -- #529 kill table 4: the closing pass's undetected changes of the 85-row test.

Imports table 3's mutator (so every earlier mutant stays available by name) and the Opus closing seat's mutator
VERBATIM (mutants_close_opus.py, copied from the seat's scratch as run -- its definitions are executed up to its own
command-line handling, so the edits are exactly the ones it measured).  Every find-text must occur EXACTLY ONCE.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "killtable3_20260913"))
sys.path.insert(0, os.path.join(HERE, "..", "killtable2_20260913"))
import mutants529c as C                                    # noqa: E402

GOTO, g = C.GOTO, C.g

_opus = io.open(os.path.join(HERE, "mutants_close_opus.py"), encoding="utf-8").read()
_ns = {}
exec(_opus.split("name, path = sys.argv")[0], _ns)
OPUS = {k: v for k, v in _ns["M"].items() if k != "base"}

M = dict(C.M)
M.update({"o_" + k: v for k, v in OPUS.items()})
M.update({
    # grok: the NEAR end of the 8-byte accept window
    "near8":     [(C.ARM8, C.ARM8.replace("len == 8", "len == 8 && relative_addr != 0", 1))],
    # glm: the latch keyed on CRIME_CONTROL; kimi-k3:cloud: the notice condition keyed on a range; deepseek: parity
    "lt_ctl":    [(C.B.LATCH_SET, "\t\t\td->warned |= (relative_addr != CRIME_CONTROL);\n")],
    "lt_rng":    [(C.B.LATCH_TEST, "\t\tif (!(d->warned & CRIME_W_LEN) || relative_addr >= 0x40) {")],
    "lt_par":    [(C.B.LATCH_SET, "\t\t\td->warned |= (relative_addr & 1) ? 0 : CRIME_W_LEN;\n")],
    # glm: CONTROL's third tested bit; kimi CLI: an untested data bit
    "c_endian":  [(GOTO, g("if (relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_ENDIANESS)) goto crime_declined;"))],
    "c_bit1":    [(GOTO, g("if (relative_addr != CRIME_CONTROL || !(idata & 0x0002)) goto crime_declined;"))],
    # codex: a nonzero answer at a named label
    "rev_od1":   [(GOTO, g("if (relative_addr == CRIME_REV) odata = 1; goto crime_declined;"))],
    "istat_od1": [(GOTO, g("if (relative_addr == CRIME_INTSTAT) odata = 1; goto crime_declined;"))],
    "time_od1":  [(GOTO, g("if (relative_addr == CRIME_TIME) odata = 1; goto crime_declined;"))],
    # kimi-k3:cloud: a refused store landing only at TIME -- PREDICTED SURVIVOR, disclosed
    "time_land": [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr == CRIME_TIME) "
                           "d->reg[CRIME_TIME / sizeof(uint64_t)] = idata; goto crime_declined;"))],
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
