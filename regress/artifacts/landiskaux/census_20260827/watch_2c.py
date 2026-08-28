#!/usr/bin/env python3
"""watch_2c.py -- capture the VALUES written to landisk paddr 0x1400002c on the
PRISTINE (unmodified) build, using the tree's own committed write-watchpoint
(#250, memory_rw.c / debugger_cmds.c).  No source modification of any kind.

WHY A WATCHPOINT AND NOT A GREP: the "non-existant paddr=..." warning prints
direction, length and pc but NOT the value.  The watchpoint fatal() prints the
value bytes.  It is checked BEFORE the device/RAM dispatch, so it sees mapped
and unmapped addresses alike.

The watchpoint enters the debugger after the offending instruction, so this
driver must `continue` once per hit.  Address is given as 0xb400002c -- the P2
(uncached) alias -- so the debugger's v2p succeeds and yields paddr 0x1400002c
without the "couldn't translate" fallback.

PTY PLUMBING IS gxprobe.Emu's, per the standing rule.  install_stubs() is
overridden away because it installs MIPS instruction stubs into a MIPS scratch
address; this rig is SH4 and needs none of that layer.
"""
import os, re, sys, time

sys.path.insert(0, "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad")
import gxprobe

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxcensusA/gxemul"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/census_A_watch.log"
WATCH = sys.argv[3] if len(sys.argv) > 3 else "0xb400002c"
IMG = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"


class SH4Emu(gxprobe.Emu):
    def install_stubs(self):
        pass                      # MIPS-only layer; this rig is SH4


argv = ["-V", "-E", "landisk", "-M", "64",
        "-d", "iR:%s/wdc-scratch-64m.img" % IMG,
        "%s/openbsd76-landisk-bsd.rd" % IMG]

e = SH4Emu(BIN, argv, boot_wait=6.0)
e.send("watchpoint add %s, 1" % WATCH, wait=1.0)
e.send("watchpoint show", wait=1.0)

#  Drive to the installer prompt, `continue`ing past each watchpoint stop.
#  The loop is bounded in BOTH directions: at most MAXC continues and at most
#  DEADLINE seconds, so a rig that stops hitting the watchpoint still ends.
MAXC, DEADLINE = 60, 300.0
t0 = time.time()
seen = 0
for i in range(MAXC):
    if time.time() - t0 > DEADLINE:
        print("DEADLINE reached after %d continues" % i)
        break
    e.send("continue", wait=6.0)
    txt = e.raw_text
    n = txt.count("WATCHPOINT:")
    if "(I)nstall" in txt:
        print("installer prompt reached after %d continues (%d hits)" % (i + 1, n))
        break
    if n == seen:
        #  no new hit in this window -- give it one longer drain before giving up
        e.drain(10.0)
        txt = e.raw_text
        if txt.count("WATCHPOINT:") == seen and "(I)nstall" not in txt:
            print("no new hit after continue %d; stopping" % (i + 1))
            break
    seen = txt.count("WATCHPOINT:")

txt = e.raw_text
open(OUT, "w").write(txt)
e.close()

pat = re.compile(r"WATCHPOINT: write of (\d+) byte\(s\) to vaddr 0x([0-9a-f]+) "
                 r"\(paddr 0x([0-9a-f]+)\) = ([0-9a-f ]+?), pc = 0x([0-9a-f]+)")
hits = pat.findall(txt)
print()
print("DENOMINATORS: transcript bytes=%d, 'WATCHPOINT:' occurrences=%d, regex hits=%d"
      % (len(txt), txt.count("WATCHPOINT:"), len(hits)))
print()
print("#   len  vaddr       paddr       value  pc")
import collections
vals = collections.Counter()
for i, (ln, va, pa, val, pc) in enumerate(hits, 1):
    print("%-3d %-4s 0x%-9s 0x%-9s 0x%-4s 0x%s" % (i, ln, va, pa, val.strip(), pc))
    vals[val.strip()] += 1
print()
print("VALUE HISTOGRAM at %s:" % WATCH)
for v in sorted(vals):
    print("   0x%s  x%d" % (v, vals[v]))
print("WATCH_TOTAL=%d" % len(hits))
