#!/usr/bin/env python3
"""The row the 101-row detector does not have: a SECOND wide write to one block,
   followed by a readback of that block.  Same session shape as `latch same', plus
   the LD_BU that `latch same' omits."""
import os, sys, pty, select, time, re
BIN = sys.argv[1]; LABEL = sys.argv[2]
DUMMY = "/tmp/pcc2_dummy.bin"; open(DUMMY, "wb").write(b"\x00\x00\x00\x00")
CODE, SCRATCH, PCC2 = 0x00010000, 0x00020000, 0xfff42000
GENCTL, MASK = 0x02, 0x3f
def enc(op, rd, rs1, imm): return (op << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def ST_B(rs, off):  return enc(0x0b, rs, 2, off)
def ST_H(rs, off):  return enc(0x0a, rs, 2, off)
I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    w = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4*i, x) for i, x in enumerate(w)] + \
           ["pc=0x%x" % at, "step %d" % len(insns)]
def setup(r5="0x5a5a5a5a", r6="0x0"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r6=%s" % r6, "r4=0xdeadbeef"]
def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64",
                       "0x10000:" + DUMMY]); os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r: continue
            try:
                d = os.read(fd, 65536)
                if not d: return False
                buf += d.decode("latin-1", "replace")
            except OSError: return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try: os.write(fd, (c + "\n").encode("latin-1"))
        except OSError: alive = False; break
        if not rd(spin if i == len(cmds)-1 else 0.25): alive = False; break
    try: os.write(fd, b"quit\n"); rd(0.4)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    try: os.waitpid(pid, 0)
    except OSError: pass
    return buf.replace("\r", ""), alive
def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"
DECL = "-- declined.  (once) ]"
print("== discriminator, binary=%s label=%s" % (BIN, LABEL))
#  D1: GUEST.  st.b 0x82 GENCTL; st.h 0xaabb GENCTL; st.h 0xaabb GENCTL; ld.bu GENCTL
t, alive = session(setup(r5="0x82", r6="0xaabb")
                   + program([ST_B(5, GENCTL), ST_H(6, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)])
                   + ["print r4"])
print("D1  rb genctl twice : GENCTL=%-8s declines=%d   (fix: 0x82 / 1)"
      % (printed(t, "r4") if alive else "died", t.count("write to PCCTWO_GENCTL " + DECL)))
#  D2: OPERATOR.  put h MASK twice, read back through a guest program
t, alive = session(setup(r5="0x12") + program([ST_B(5, MASK)])
                   + ["put h 0x%x, 0xaabb" % (PCC2 + MASK)] * 2
                   + program([LD_BU(4, MASK)], at=CODE + 0x100) + ["print r4"])
print("D2  rb mask twice   : MASK  =%-8s declines=%d   (fix: 0x12 / 1)"
      % (printed(t, "r4") if alive else "died", t.count("write to PCCTWO_MASK " + DECL)))
#  D3: the CONTROL -- one wide write only, which is what every shipped row does
t, alive = session(setup(r5="0x82", r6="0xaabb")
                   + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
print("D3  rb genctl once  : GENCTL=%-8s declines=%d   (fix: 0x82 / 1)  [the shipped row's shape]"
      % (printed(t, "r4") if alive else "died", t.count("write to PCCTWO_GENCTL " + DECL)))
print("DISCRIM_DONE")
