#!/usr/bin/env python3
"""#545 r3e table, variant generation (WSL).  /tmp/fbd5r3e_var gets the r3d table's 739 variant files and its FIX.c
(copied from /tmp/fbd5r3d_var; FIX.c must be SEC's device), plus R3E_<id>.c -- the shapes of 3d's pass that r3e's
checks are for, the premise-settling shapes the pass asked for, and the disclosed shapes as controls.
Every anchor must occur exactly once in the device; a shape whose text does not change the file is refused."""
import hashlib, io, os, shutil

R = "/mnt/c/DocumentNoSnc/CC/GXEMUL"
SEC = R + "/GXEMUL-SEC"
OLD = "/tmp/fbd5r3d_var"
V = "/tmp/fbd5r3e_var"
DEV = SEC + "/src/devices/dev_footbridge.c"
T, NL = "\t", "\n"


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


base = io.open(DEV, encoding="utf-8", newline="").read()
assert md5(DEV).startswith("783c0c7f"), "SEC device md5"
shutil.rmtree(V, ignore_errors=True)
os.makedirs(V)
n_old = 0
for f in sorted(os.listdir(OLD)):
    if f.endswith(".c"):
        shutil.copy(OLD + "/" + f, V + "/" + f)
        n_old += 1
assert md5(V + "/FIX.c") == md5(DEV), "FIX.c is not SEC's device"
print("CARRIED %d files from %s (FIX.c == SEC device)" % (n_old, OLD))


def put(vid, old, new):
    c = base.count(old)
    if c != 1 or old == new:
        print("ANCHOR-ERROR %s count=%d" % (vid, c))
        return
    io.open(V + "/" + vid + ".c", "w", encoding="utf-8", newline="").write(base.replace(old, new))
    print("ok %s" % vid)


A0_FLAG = T * 2 + "else if (!d->warned_irq_status_w) {"
A0_BODY = T * 3 + "d->warned_irq_status_w = 1;" + NL
A0_DIR = T * 2 + "if (writeflag == MEM_READ)" + NL + T * 3 + "odata = d->irq_status & d->irq_enable;"
CLR3 = T * 3 + "d->irq_enable &= ~idata;" + NL + T * 3 + "if (d->irq_status & d->irq_enable)" + NL \
    + T * 4 + "INTERRUPT_ASSERT(d->irq);"
CLR_END = T * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL + T * 2 + "} else if (!d->warned_irq_clear_r) {"
TAIL = T * 2 + "}" + NL + T + "}" + NL + NL + T + "if (writeflag == MEM_READ)" + NL \
    + T * 2 + "memory_writemax64(cpu, data, len, odata);"

#  3d's pass: the endpoint-only KEPT check (codex): each +0x180 decline toggles irq_asserted
put("R3E_CXT1", A0_FLAG, T * 2 + "else if ((d->irq_asserted ^= 1, !d->warned_irq_status_w)) {")
#  3d's pass: the read write-back past len (kimi-k3:cloud).  WB4 is deterministic (the timer rows read 4 bytes
#  through buf[4]); WB8 also overflows the harness's own 4-byte buffers there -- recorded, not predicted.
put("R3E_WB4", TAIL, TAIL.replace("memory_writemax64(cpu, data, len, odata);",
                                  "memory_writemax64(cpu, data, len < 4 ? 4 : len, odata);"))
put("R3E_WB8", TAIL, TAIL.replace("memory_writemax64(cpu, data, len, odata);",
                                  "memory_writemax64(cpu, data, 8, odata);"))
#  glm's two premise-settling shapes: do X12/X13 read the FIQ fields, and X6 the four fields?
put("R3E_GLM1", CLR3, T * 3 + "d->irq_enable &= ~idata;" + NL + T * 3 + "if (d->irq_status & d->irq_enable) {" + NL
    + T * 4 + "d->fiq_status = 0; INTERRUPT_ASSERT(d->irq); }")
put("R3E_GLM2", A0_BODY, A0_BODY + T * 3 + "d->irq_enable = 0;" + NL)
#  the widened disclosures, as controls (green expected on both)
put("R3E_BO1", A0_DIR, T * 2 + "if (writeflag == MEM_READ && cpu->byte_order != EMUL_LITTLE_ENDIAN)" + NL
    + T * 3 + "odata = d->irq_status & d->irq_enable;")
put("R3E_PC1", A0_DIR, T * 2 + "if (writeflag == MEM_READ && !cpu->pc)" + NL + T * 3 + "odata = d->irq_status & d->irq_enable;")
put("R3E_CXD1", CLR3, T * 3 + "d->irq_enable &= ~idata;" + NL + T * 3 + "if (d->irq_status & d->irq_enable)" + NL
    + T * 4 + "{ if (d->fiq_enable & 1) INTERRUPT_ASSERT(d->timer_irq[0]); else INTERRUPT_ASSERT(d->irq); }")
#  codex's dedicated job, 3d: the raw status at the asserted Clears, keyed so the re-arm row cannot see it (E3 only)
put("R3E_CXS2", CLR_END, T * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL
    + T * 3 + "if (d->irq_asserted && !d->warned_irq_clear_r) d->irq_status = 0;" + NL
    + T * 2 + "} else if (!d->warned_irq_clear_r) {")
print("VARIANT FILES %d" % len([f for f in os.listdir(V) if f.endswith(".c") and f != "FIX.c"]))
