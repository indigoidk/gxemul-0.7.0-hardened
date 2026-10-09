#!/usr/bin/env python3
"""mkclosure2.py <closure probe> <out> -- adds row `encl2': the enclosing-predicate and per-path cells
the closure probe still does not hold: S-DPI with Rn=PC/Rd!=PC (adds r0,pc,#0), S-LDM without pc
(ldmia r5,{r0}^), the DPI restore through a non-MOV opcode (subs pc,lr,#0), and an msr_imm decline
of a bit-4-clear value at a non-SVC label (msr cpsr_c,#0x03 from FIQ)."""
import io
import sys
src, out = sys.argv[1], sys.argv[2]
s = io.open(src, newline="").read()
def sub(a, b):
    global s
    if s.count(a) != 1:
        raise SystemExit("PIN FAIL %r" % a[:50])
    s = s.replace(a, b)
sub('#  OPUS CLOSURE words\n',
    '#  OPUS CLOSURE words\n'
    'WORDS["adds_r0_pc_0"] = 0xE29F0000           # adds r0, pc, #0\n'
    'WORDS["ldm_r5_r0_s"] = 0xE8D50001            # ldmia r5, {r0}^\n'
    'WORDS["subs_pc_lr_0"] = 0xE25EF000           # subs pc, lr, #0\n')
sub('row("row count", len(rows) + 1, 41,',
    'T7 = 0x8400\n'
    'early, late, alive, marked, full = prog_session(\n'
    '    ["s_1f", "adds_r0_pc_0", "mov_r0_2a", "mrs_r3", "str_r3_4", "ldm_r5_r0_s", "mrs_r3",\n'
    '     "str_r3_8", "s_14", "subs_pc_lr_0"],\n'
    '    blocks=[(T7, ["mrs_r3", "str_r3_c", "c_11", "c_03", "mrs_r3", "str_r3_10"])],\n'
    '    data={LDMW: 0x12345678}, regs=["r5=0x%x" % LDMW, "lr=0x%x" % T7],\n'
    '    segments=(((), 16),), late_end=DEST + 0x14)\n'
    'if not marked or not arming(early, full):\n'
    '    got = "unarmed"\n'
    'elif not alive:\n'
    '    got = "dead"\n'
    'else:\n'
    '    vals = [dumped(late, DEST + o) for o in (4, 8, 12, 16)]\n'
    '    got = " ".join("nofire" if v in (None, POISON) else "%02x" % (v & 0x1f) for v in vals)\n'
    'row("encl2", got, "13 13 13 11",\n'
    '    "adds r0,pc / ldm {r0}^ must not restore; subs pc,lr declines 0x14; msr #0x03 at FIQ declined.")\n'
    'row("row count", len(rows) + 1, 42,')
io.open(out, "w", newline="").write(s)
