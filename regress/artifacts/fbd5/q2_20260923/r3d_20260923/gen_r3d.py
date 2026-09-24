#!/usr/bin/env python3
"""#545 r3d table, variant generation (WSL).  /tmp/fbd5r3d_var gets:
  the r3c table's 711 variant files and its FIX.c, copied from /tmp/fbd5r3c_var (FIX.c must be SEC's device);
  OQ_<id>.c  -- the Opus seat's 22 q2f shapes (its gen_q2f.py, applied to the same device);
  R3D_<id>.c -- the new shapes of 3c's pass that r3d's checks are for, plus two controls.
Every anchor must occur exactly once in the device; a shape whose text does not change the file is refused."""
import hashlib, io, os, shutil, sys

R = "/mnt/c/DocumentNoSnc/CC/GXEMUL"
SEC = R + "/GXEMUL-SEC"
OLD = "/tmp/fbd5r3c_var"
V = "/tmp/fbd5r3d_var"
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


#  the Opus seat's 22 (q2f), from its own generator
sys.path.insert(0, R + "/_scratchpad/fbd5/q2f/opus")
import gen_q2f  # noqa: E402
assert md5(gen_q2f.FROZEN) == md5(DEV), "Opus frozen device != SEC device"
for v in gen_q2f.variants():
    put("OQ_" + v["vid"], v["old"], v["new"])

#  3c's pass: the shapes r3d's strengthened checks are for
CLR_END = T * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL + T * 2 + "} else if (!d->warned_irq_clear_r) {"
put("R3D_CXC1", CLR_END,           # codex (panel + dedicated), glm: zero the status at a DEVINIT asserting Clear
    T * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL
    + T * 3 + "if (d->timer_control[0] && (d->irq_status & d->irq_enable)) d->irq_status = 0;" + NL
    + T * 2 + "} else if (!d->warned_irq_clear_r) {")
put("R3D_CXA1", CLR_END,           # control for the k=1 row's raw-status channel: zero it at an ASSERTED asserting Clear
    T * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL
    + T * 3 + "if (d->irq_asserted && (d->irq_status & d->irq_enable)) d->irq_status = 0;" + NL
    + T * 2 + "} else if (!d->warned_irq_clear_r) {")
put("R3D_GF1",                     # grok: the IRQ_STATUS read sets fiq_enable while irq_asserted
    T * 3 + "odata = d->irq_status & d->irq_enable;" + NL + T * 2 + "else if (!d->warned_irq_status_w) {",
    T * 3 + "odata = d->irq_status & d->irq_enable, d->fiq_enable |= (uint32_t) d->irq_asserted;" + NL
    + T * 2 + "else if (!d->warned_irq_status_w) {")
put("R3D_DA1",                     # a decline (+0x180) clears irq_asserted
    T * 3 + "d->warned_irq_status_w = 1;" + NL,
    T * 3 + "d->warned_irq_status_w = 1;" + NL + T * 3 + "d->irq_asserted = 0;" + NL)
put("R3D_FW1",                     # deepseek: the write-data fetch reads 4 bytes whatever len is
    T + "if (writeflag == MEM_WRITE)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, len);" + NL + NL
    + T + "if (relative_addr >= TIMER_1_LOAD",
    T + "if (writeflag == MEM_WRITE)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, 4);" + NL + NL
    + T + "if (relative_addr >= TIMER_1_LOAD")
put("R3D_LH1",                     # codex (dedicated): a latch that re-arms after four repeats -- disclosed, not rowed
    T * 2 + "else if (!d->warned_irq_status_w) {",
    T * 2 + "else if (!(d->warned_irq_status_w++ & 3)) {")
print("VARIANT FILES %d" % len([f for f in os.listdir(V) if f.endswith(".c") and f != "FIX.c"]))
