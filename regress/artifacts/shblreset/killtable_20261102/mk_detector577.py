#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mk_detector577.py -- build the #577 detector from HEAD's copies: regress/sh_tlbmulti_probe.py gains a `program`/`steps`
parameter on session() and four BL rows; regress/gate_sh_rounding.sh's `sh_tlbmulti rows run` pin moves 6 -> 10 and the four
names join the loop.  Writes w577/sh_tlbmulti_probe.NEW.py and w577/gate_sh_rounding.NEW.sh only (no project tree)."""
import io, os, re, subprocess
W = os.path.dirname(os.path.abspath(__file__))
SEC = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
BS = chr(92)
def head(p):
    return subprocess.run(["git", "-C", SEC, "show", "HEAD:" + p], capture_output=True).stdout.decode("utf-8")

# ---------------------------------------------------------------- probe
s = head("regress/sh_tlbmulti_probe.py")
old_sig = 'def session(pre=(), entry1_vpn=VPN_A, settle=8.0, trigger=True):\n'
new_sig = 'def session(pre=(), entry1_vpn=VPN_A, settle=8.0, trigger=True, program=None, steps=None):\n'
assert s.count(old_sig) == 1
s = s.replace(old_sig, new_sig)
old_doc = '    `pre` runs before the trigger -- used to pre-set SR so the reset transition\'s\n    SR update is observable.\n    """\n'
new_doc = ('    `pre` runs before the trigger -- used to pre-set SR so the reset transition\'s\n    SR update is observable.\n'
           '    #577: `program` (a list of 16-bit words placed at CODE) and `steps` replace the\n'
           '    three-store multiple-hit program for the BL rows; the default is that program.\n    """\n')
assert s.count(old_doc) == 1
s = s.replace(old_doc, new_doc)
old_cmds = ('    cmds = list(pre) + ([] if not trigger else [\n'
            '        "r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0,\n'
            '        "r4=0x%08x" % entry1_vpn, "r5=0x%x" % ENTRY1,\n'
            '        "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC,\n'
            '        "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),\n'
            '        "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R4_AT_R5),\n'
            '        "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R6_AT_R7),\n'
            '        "pc=0x%x" % CODE, "step 3"]) + [\n')
new_cmds = ('    if program is None:\n'
            '        trig = ["r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0,\n'
            '                "r4=0x%08x" % entry1_vpn, "r5=0x%x" % ENTRY1,\n'
            '                "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC,\n'
            '                "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),\n'
            '                "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R4_AT_R5),\n'
            '                "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R6_AT_R7),\n'
            '                "pc=0x%x" % CODE, "step 3"]\n'
            '    else:   # #577: an arbitrary short program; the caller seeds registers through `pre`\n'
            '        trig = ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(program)]\n'
            '        trig += ["pc=0x%x" % CODE, "step %d" % (steps if steps is not None else len(program))]\n'
            '    cmds = list(pre) + ([] if not trigger else trig) + [\n')
assert s.count(old_cmds) == 1, s.count(old_cmds)
s = s.replace(old_cmds, new_cmds)
old_tail = 'print("SH_TLBMULTI_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))\n'
assert s.count(old_tail) == 1
rows_block = '''
#  ---- #577: a general exception taken with SR.BL set is a MANUAL reset -----------
#  sh7750_hardware.txt 5.5.3 (:12302-12304): with BL set, a general exception other than a
#  user break performs a manual reset; EXPEVT is H'020 (:678-681).  Table 5.2 (:12006,
#  :12010) lists the two TLB multiple-hit exceptions as reset-category in their own right,
#  code H'140 (:12461), so the BL rule must not touch them.  HEAD's sh_exception() rewrote
#  EVERY code to EXPEVT_RESET_POWER (H'000) when BL was set; #577 makes it EXPEVT_RESET_MANUAL
#  with the multiple-hit code exempt.  Rows run under sr = MD|BL (0x500000f0, RB clear so the
#  bank-0 seeds are the ones the program uses); `tlbm trapa' is the BL-CLEAR control that pins
#  the general vector's own code.  Contract: TRAPA (H'160) and a misaligned load (H'0E0) are
#  the two general codes driven; a re-introduction of the rewrite keyed to a code this table
#  does not drive (a TLB miss, a reserved instruction) is clause-(e) disclosure.  The identity
#  medium for this predicate round is the BL block DELETED: `tlbm bl trapa' and `tlbm bl ldmis'
#  then read their own codes (red); `tlbm bl mhit' reads H'140 either way and cannot carry it.
#  Names stay at 13 characters or fewer: row() prints `%-14s' and the gate anchors `^$v  .*ok$'
#  with TWO spaces (Grok, pass 1 -- the padded-column trap).
SR_MD_BL = 0x500000f0
SR_MD = 0x400000f0
TRAPA_1 = 0xc301            # trapa #1  : 1100 0011 0000 0001
MOV_L_AT_R1_R2 = 0x6212     # mov.l @r1,r2 : 0110 0010 0001 0010
t5, died5 = session(pre=["sr=0x%08x" % SR_MD_BL], program=[TRAPA_1], steps=1)
row("tlbm bl trapa", "died" if died5 else reg(t5, "expevt"), "0x00000020")
t6, died6 = session(pre=["sr=0x%08x" % SR_MD_BL])
row("tlbm bl mhit", "died" if died6 else reg(t6, "expevt"), "0x00000140")
t7, died7 = session(pre=["sr=0x%08x" % SR_MD_BL, "r1=0x%08x" % (CODE + 1)], program=[MOV_L_AT_R1_R2], steps=1)
row("tlbm bl ldmis", "died" if died7 else reg(t7, "expevt"), "0x00000020")
t8, died8 = session(pre=["sr=0x%08x" % SR_MD], program=[TRAPA_1], steps=1)
row("tlbm trapa", "died" if died8 else reg(t8, "expevt"), "0x00000160")

'''
s = s.replace(old_tail, rows_block + old_tail)
# the docstring's stale note becomes history
old_note = ('  * `cpu_sh.c` rewrites ANY expevt to `EXPEVT_RESET_POWER` when `SR.BL` is set, before\n'
            '    the assignment.  This tree resets with BL clear, so the path is live -- but a\n'
            '    BL-set guest silently latches `0x000` instead.\n')
new_note = ('  * `cpu_sh.c` USED TO rewrite ANY expevt to `EXPEVT_RESET_POWER` when `SR.BL` is set\n'
            '    (a BL-set guest silently latched `0x000`, the multiple hit included).  #577 makes it\n'
            '    `EXPEVT_RESET_MANUAL` with the multiple-hit code exempt; the BL rows at the end of\n'
            '    this file pin both halves.\n')
assert s.count(old_note) == 1
s = s.replace(old_note, new_note)
io.open(os.path.join(W, "sh_tlbmulti_probe.NEW.py"), "w", encoding="utf-8", newline="\n").write(s)

# ---------------------------------------------------------------- gate
g = head("regress/gate_sh_rounding.sh")
old_pin = '    check "sh_tlbmulti rows run"     "${tmres#*/}" 6\n'
assert g.count(old_pin) == 1
g = g.replace(old_pin, '    #  #577: 6 -> 10 (three BL rows + the BL-clear TRAPA control; see the probe).  EQUALITY on purpose.\n'
                       '    check "sh_tlbmulti rows run"     "${tmres#*/}" 10\n')
old_loop = '    for v in "tlbm alive" "tlbm expevt" "tlbm pc" "tlbm vbr" "tlbm sr" "tlbm single"; do\n'
assert g.count(old_loop) == 1
g = g.replace(old_loop, '    for v in "tlbm alive" "tlbm expevt" "tlbm pc" "tlbm vbr" "tlbm sr" "tlbm single" ' + BS + '\n'
                        '             "tlbm bl trapa" "tlbm bl mhit" "tlbm bl ldmis" "tlbm trapa"; do\n')
io.open(os.path.join(W, "gate_sh_rounding.NEW.sh"), "w", encoding="utf-8", newline="\n").write(g)
print("probe NEW", len(s.encode()), "bytes; gate NEW", len(g.encode()), "bytes")
