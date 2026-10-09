#!/usr/bin/env python3
"""loop_standalone.py <frozen probe> <loop_row.py> <gxemul> <label> -- run ONLY the prototype
`msr loop' row, with the frozen probe's own helpers (its text up to the `enc ok' section is
executed verbatim, so session()/prog_session()/arming() are the shipped ones)."""
import io
import sys

probe, looprow, binary, label = sys.argv[1:5]
src = io.open(probe, newline="").read()
CUT = "# ---------------------------------------------------------------- enc ok"
if src.count(CUT) != 1:
    print("CUT-NOT-UNIQUE")
    sys.exit(3)
ns = {"__name__": "probe_prefix", "__file__": probe}
sys.argv = [probe, binary, label]
exec(compile(src.split(CUT)[0], probe, "exec"), ns)
ns["MODELLED"] = (0x10, 0x11, 0x12, 0x13, 0x17, 0x1B, 0x1F)     # as in the probe's grid section
exec(compile(io.open(looprow, newline="").read(), looprow, "exec"), ns)
print("loop_standalone -- binary=%s label=%s sessions=%d" % (binary, label, ns["NSESS"][0]))
for nm, got, want, note in ns["rows"]:
    print("  %-9s %s\n     got =%s\n     want=%s" % (nm, "ok" if got == want else "FAIL", got, want))
for d in ns["diagnosis"]:
    print("  diag  %s" % d)
print("LOOPSTANDALONE_DONE")
