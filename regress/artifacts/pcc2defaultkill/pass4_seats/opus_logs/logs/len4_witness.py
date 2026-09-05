#!/usr/bin/env python3
"""#501 pass-4 Opus seat -- is the len-4 default READ's announced VALUE rowable at all?

The 46-row instrument pins the read announce's value at 0x05 (len 1) and 0x06 (len 2) only.
Its one len-4 read row (`wide rd srvd') reads PRTICR, whose four array bytes are 0 and which
no cased arm can write -- so its VALUE channel cannot vary, which is why M_LASTBYTE swept the
36-row instrument.  All TEN word-aligned uncased offsets (0x14 0x18 0x20 0x24 0x28 0x2c 0x30
0x34 0x38 0x3c) are outside every cased arm's byte range, and m88k alignment is enforced
before memory_rw -- so a guest cannot start a len-4 read anywhere else.

EXCEPT: the counter arm memcpys `len' bytes with no width check (the filed `pcc2counter8'),
so an 8-byte st.d at T2COUNT (0x10) writes pcctwo_reg[0x10..0x17] -- filling 0x14, which IS
word-aligned and uncased.  A following ld.w at 0x14 is then a len-4 default read whose FIRST
served byte is guest-chosen and NONZERO.  This probe measures whether that route works.
"""
import io, os, pty, re, select, sys, time
BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/pcc2_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 4096)
HERE = os.path.dirname(os.path.abspath(__file__))
_w = io.open(os.path.join(HERE, "pcc2_width_probe.py"), encoding="utf-8").read()
exec(_w[_w.index("def session("):_w.index("\ndef printed")])

CODE, PCC2, SCRATCH, SENTINEL = 0x00010000, 0xfff42000, 0x00020000, 0xdeadbeef
def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_D(rs, off): return enc(0x08, rs, 2, off)
I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4 * k, w) for k, w in enumerate(words)] + \
           ["pc=0x%x" % at, "step %d" % len(insns)]
def printed(t, reg="r4"):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"

print("len4 witness -- binary=%s label=%s" % (BIN, LABEL))
cmds = ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH,
        "r4=0x11223344", "r5=0x99887766", "r6=0x%x" % SENTINEL]
cmds += program([ST_D(4, 0x10), LD_W(6, 0x14)]) + ["print r6"]
t, alive, how = session(cmds)
print("ALIVE=%s HOW=%s" % (alive, how))
print("r6(ld.w at 0x14)=%s   want 0x99887766 if the st.d filled 0x14..0x17" % printed(t, "r6"))
for line in t.splitlines():
    if "pcc2:" in line:
        print("MSG: " + line.strip())
print("LEN4WIT_DONE")
