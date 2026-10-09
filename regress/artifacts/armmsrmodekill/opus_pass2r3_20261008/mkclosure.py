#!/usr/bin/env python3
"""mkclosure.py <frozen probe> <out> -- build the Opus CLASS-CLOSURE variant of the 40-row probe:
  src rows: accept SPSR 0xffffffdf (every bit but T), and before EACH decline `msr cpsr_fsx,#0' +
            re-entry, so the old CPSR differs from the declined SPSR (0xffffffcf) at bits 31:6.
  tbit row: T-set accept through pop, DPI and msr_imm (0x3f), T-set decline through msr_imm, pop,
            DPI (0x34), each read by the debugger's `print cpsr'.
Every edit is presence-pinned (count == 1)."""
import io
import sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, newline="").read()


def sub(a, b):
    global s
    n = s.count(a)
    if n != 1:
        raise SystemExit("PIN FAIL count=%d: %r" % (n, a[:60]))
    s = s.replace(a, b)


sub('WORDS["str_r3_14"] = 0xE5843014              # str  r3, [r4,#20]\n',
    'WORDS["str_r3_14"] = 0xE5843014              # str  r3, [r4,#20]\n'
    '#  OPUS CLOSURE words\n'
    'WORDS["sf_ff"] = 0xE368F4FF                  # msr spsr_f, #0xff000000\n'
    'WORDS["ss_ff"] = 0xE364F8FF                  # msr spsr_s, #0x00ff0000\n'
    'WORDS["sx_ff"] = 0xE362FCFF                  # msr spsr_x, #0x0000ff00\n'
    'WORDS["cf_0"] = 0xE32EF000                   # msr cpsr_fsx, #0\n'
    'for m in (0x3F, 0x34):\n'
    '    WORDS["c_%02x" % m] = 0xE321F000 | m\n'
    '    WORDS["s_%02x" % m] = 0xE361F000 | m\n')

# DPI src session
sub('                [ck, "sf_c0", "s_df", "movs_pc_r5"],\n'
    '                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", "add_r5_40", cc, "s_cf", "movs_pc_r5"]),\n'
    '                        (BLK[1], ["mrs_r3", "str_r3_8", "add_r5_40", "movs_pc_r5"]),\n',
    '                [ck, "sf_ff", "ss_ff", "sx_ff", "s_df", "movs_pc_r5"],\n'
    '                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", "add_r5_40", "cf_0", cc, "s_cf",\n'
    '                                  "movs_pc_r5"]),\n'
    '                        (BLK[1], ["mrs_r3", "str_r3_8", "add_r5_40", "cf_0", cc, "movs_pc_r5"]),\n')
sub('                segments=(((), 21),), late_end=DEST + 0x14)\n',
    '                segments=(((), 26),), late_end=DEST + 0x14)\n')
# POP src session
sub('                [ck, "sf_c0", "s_df", "ldm_r6w_pc_s"],\n'
    '                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", cc, "s_cf", "ldm_r6w_pc_s"]),\n'
    '                        (BLK[1], ["mrs_r3", "str_r3_8", "ldm_r6w_pc_s"]),\n',
    '                [ck, "sf_ff", "ss_ff", "sx_ff", "s_df", "ldm_r6w_pc_s"],\n'
    '                blocks=[(BLK[0], ["mrs_r3", "str_r3_4", "cf_0", cc, "s_cf", "ldm_r6w_pc_s"]),\n'
    '                        (BLK[1], ["mrs_r3", "str_r3_8", "cf_0", cc, "ldm_r6w_pc_s"]),\n')
sub('                segments=(((), 18),), late_end=DEST + 0x14)\n',
    '                segments=(((), 23),), late_end=DEST + 0x14)\n')
sub('        acc, dec = NZ | 0xDF, NZ | 0xC0 | mode\n',
    '        acc, dec = 0xFFFFFFDF, 0xFFFFFFC0 | mode\n')

# tbit row, before the identity row
sub('row("row count", len(rows) + 1, 40,',
    'T2, T3, T4, T5 = 0x8200, 0x8300, 0x8340, 0x8380\n'
    'T6 = 0x83C0\n'
    'early, late, alive, marked, full = prog_session(\n'
    '    ["s_3f", "ldm_r5_pc_s"],\n'
    '    blocks=[(TGT, []), (T2, ["s_3f", "movs_pc_lr"]), (T3, ["c_3f"]), (T4, ["c_34"]),\n'
    '            (T5, ["s_34", "ldm_r5_pc_s"]), (T6, ["s_34", "movs_pc_lr"])],\n'
    '    data={LDMW: TGT}, regs=["r5=0x%x" % LDMW, "lr=0x%x" % TGT],\n'
    '    segments=(((), 2), (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T2, "lr=0x%x" % TGT], 2),\n'
    '              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T3], 1),\n'
    '              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T4], 1),\n'
    '              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T5], 2),\n'
    '              (["print cpsr", "cpsr=0xd3", "pc=0x%x" % T6, "lr=0x%x" % TGT], 2),\n'
    '              (["print cpsr"], 0)))\n'
    'if not marked or not arming(early, full):\n'
    '    got = "unarmed"\n'
    'elif not alive:\n'
    '    got = "dead"\n'
    'else:\n'
    '    vals = re.findall(r"print\\s+cpsr\\s*\\n\\s*(0x[0-9a-f]+)", late)\n'
    '    t = early + late\n'
    '    got = " ".join("%02x" % (int(v, 16) & 0xff) for v in vals) + " n=%d" % (\n'
    '        announces(t, "msr_imm") + announces(t, "arm_pop") + announces(t, "dpi S-to-pc"))\n'
    'row("tbit", got, "3f 3f 3f 33 33 33 n=3",\n'
    '    "T-set accept via pop/DPI/msr (0x3f), T-set decline via msr/pop/DPI (0x34): T from the operand.")\n'
    'row("row count", len(rows) + 1, 41,')
io.open(out, "w", newline="").write(s)
print("CLOSURE PROBE WRITTEN", out)
