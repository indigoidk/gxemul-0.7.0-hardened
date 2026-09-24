#!/usr/bin/env python3
"""#545 r3c table: the Opus seat's 54 q2e variants (its own gen_q2e.py) and five shapes the repair-3 panel named, written
as mutated device files into argv[1].  Every anchor must match exactly once in the SEC device."""
import hashlib, io, os, sys

V = sys.argv[1]
OPUS = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/fbd5/q2e/opus"
SEC_DEV = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_footbridge.c"
sys.path.insert(0, OPUS)
import gen_q2e  # noqa: E402

T, NL = "\t", "\n"
EXTRA = [
    ("XA_xor", T + "d->irq_status |= interrupt->line;", T + "d->irq_status ^= interrupt->line;",
     "codex (panel): the assert producer's OR as XOR"),
    ("XC_dest", T * 3 + "d->irq_enable &= ~idata;" + NL + T * 3 + "if (d->irq_status & d->irq_enable)" + NL
     + T * 4 + "INTERRUPT_ASSERT(d->irq);",
     T * 3 + "d->irq_enable &= ~idata;" + NL + T * 3 + "if (d->irq_status & d->irq_enable)" + NL
     + T * 4 + "INTERRUPT_ASSERT(*(len < 4 ? &d->timer_irq[0] : &d->irq));",
     "codex (panel): a narrow Clear write asserts timer 1, not the CPU line"),
    ("XF_len8", T + "if (writeflag == MEM_WRITE)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, len);",
     T + "if (writeflag == MEM_WRITE && len != 8)" + NL + T * 2 + "idata = memory_readmax64(cpu, data, len);",
     "grok: the fetch skips an 8-byte write (an STRD at +0x188/+0x288)"),
    ("XZ_clr0", T * 2 + "if (writeflag == MEM_WRITE) {" + NL + T * 3 + "d->irq_enable &= ~idata;",
     T * 2 + "if (writeflag == MEM_WRITE && !(idata == 0 && d->warned_irq_clear_r)) {" + NL + T * 3 + "d->irq_enable &= ~idata;",
     "grok: a latched Clear of 0 is declined as a read"),
    ("XD_zero", T + "d->irq_status &= ~interrupt->line;", T + "d->irq_status = 0;",
     "deepseek: the deassert producer clears every line"),
]
fix = io.open(SEC_DEV, encoding="utf-8", newline="").read()
bad = 0
allv = [(v["vid"], v["old"], v["new"]) for v in gen_q2e.variants()] + [(a, b, c) for a, b, c, _ in EXTRA]
for vid, old, new in allv:
    if fix.count(old) != 1 or old == new:
        print("%s ANCHOR-ERROR (%d)" % (vid, fix.count(old)))
        bad += 1
        continue
    io.open(os.path.join(V, vid + ".c"), "w", encoding="utf-8", newline="").write(fix.replace(old, new))
print("Q2E+EXTRA VARIANTS: %d written, %d anchor errors (gen_q2e.py md5 %s)" % (
    len(allv) - bad, bad, hashlib.md5(open(OPUS + "/gen_q2e.py", "rb").read()).hexdigest()[:8]))
