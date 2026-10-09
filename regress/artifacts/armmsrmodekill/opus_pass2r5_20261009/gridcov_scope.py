#!/usr/bin/env python3
"""gridcov_scope.py <probe> -- OFFLINE: what does the `grid cov' row actually certify?
Executes the probe's own MODELLED / UNMODELLED / *_LABELS / HI* / grid_obs / grid_cov text verbatim,
then perturbs the GENERATOR (not the checker) and reports grid_cov()'s verdict.  No emulator."""
import io
import re
import sys

src = io.open(sys.argv[1], newline="").read()
a = src.index("MODELLED = (0x10, 0x11, 0x12, 0x13, 0x17, 0x1B, 0x1F)")
b = src.index('GRID_SITE = {"msr": "msr_imm"')
block = src[a:b]
# drop the WORDS/GRID_CHECK/GBAD lines (they need the probe's WORDS dict) -- keep tables + functions
keep = []
skip = False
for ln in block.split("\n"):
    if ln.startswith("WORDS[") or ln.startswith("GRID_CHECK") or ln.startswith("GBAD") or \
            ln.startswith("for k in (\"ldm_r6_pc_s\",)"):
        skip = True
    if skip and (ln.startswith("HI1") or ln.startswith("def ")):
        skip = False
    if not skip:
        keep.append(ln)
ns = {}
exec("\n".join(keep), ns)


def report(tag):
    tot = sum(len(ns["grid_cov"](p)) for p in ("msr", "dpi", "pop"))
    n = [len(ns["grid_obs"](p)) for p in ("msr", "dpi", "pop")]
    print("%-58s obs msr/dpi/pop=%s  grid_cov uncovered=%d" % (tag, n, tot))


report("SHIPPED generator")
U0 = ns["UNMODELLED"]
ns["UNMODELLED"] = tuple(m for m in U0 if m != 0x18)
report("G3 loses 0x18 (the repair-4 `& 0x17' cell)")
ns["UNMODELLED"] = tuple(m for m in U0 if m not in (0x18, 0x19, 0x1A))
report("G3 loses 0x18-0x1a")
ns["UNMODELLED"] = U0
M0 = ns["MODELLED"]
# G3 accept side: the per-label accepts already cycle modelled modes; drop the
# `every modelled mode' loop's 0x1F target by shrinking MODELLED's tail loop is not possible
# without editing grid_obs, so instead drop one LABEL from MSR_LABELS (loses G2 at SYS):
L0 = ns["MSR_LABELS"]
ns["MSR_LABELS"] = tuple(l for l in L0 if l != 0x1F)
report("msr G2 loses label SYS (no SYS decline / accept at all)")
ns["MSR_LABELS"] = L0
R0 = ns["RESTORE_LABELS"]
ns["RESTORE_LABELS"] = tuple(l for l in R0 if l != 0x17)
report("restore G2 loses label ABT")
ns["RESTORE_LABELS"] = R0
print("GRIDCOV_SCOPE_DONE")
