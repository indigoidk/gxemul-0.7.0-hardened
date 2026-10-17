#!/usr/bin/env python3
"""nul_blocks.py -- how many codex opening header blocks on record carry a NUL byte, over census_v5.py's own scope and by
the landed rule (banner by line 12, first rule, block read for at most 30 lines, closed by the second rule), the ANSI strip
applied first as the launcher does.  Also counts the codex .err files carrying a NUL anywhere."""
import os, re

PROJ = r"C:\DocumentNoSnc\cc\GXEMUL"
roots = [os.path.join(PROJ, "GXEMUL-SEC"), os.path.join(PROJ, "_scratchpad")]
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
codex = []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            fl = f.lower()
            if fl.endswith(".err") and "codex" in fl:
                codex.append(os.path.join(dp, f))
nread = blocks = nulblocks = nulfiles = 0
for p in codex:
    try:
        raw = open(p, "rb").read().decode("utf-8", "replace")
    except OSError:
        continue
    nread += 1
    nulfiles += "\x00" in raw
    lines = ANSI.sub("", raw).split("\n")
    h = n = 0; body = []
    for i, l in enumerate(lines, 1):
        if i > 12 and h < 2:
            break
        if h == 0 and l.startswith("OpenAI Codex"):
            h = 1; continue
        if h == 1 and l.startswith("--------"):
            h = 2; continue
        if h == 2 and l.startswith("--------"):
            break
        if h == 2:
            n += 1
            if n > 30:
                break
            body.append(l)
    if h == 2:
        blocks += 1
        if any("\x00" in l for l in body):
            nulblocks += 1; print("NUL IN BLOCK:", p)
print("SUMMARY: %d codex .err files read | %d carry a NUL anywhere | %d opening blocks | %d of them carry a NUL"
      % (nread, nulfiles, blocks, nulblocks))
