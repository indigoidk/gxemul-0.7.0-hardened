#!/usr/bin/env python3
"""#457: a guest UTLB associative write matching two entries ended the host.

Prints one line per row:  <name> <got> <want> ok|FAIL
then SH_TLBMULTI_CONTROL=OK|DEAD and SH_TLBMULTI_RESULT=<passed>/<total>.
gate_sh_rounding.sh does the asserting.

What this protects
------------------
`dev_sh4.c` raises `sh_exception(cpu, EXPEVT_RESET_TLB_MULTI_HIT, 0, 0)` when an
ASSOCIATIVE write to the UTLB address array matches more than one entry.
`sh_exception()` had no case for `0x140`, so it fell to the `default:` arm and ran
`exit(1)`.  Three ordinary privileged guest stores ended the host process.

Measured on the committed build, `-E landisk`, unmodified, under `step 3`:

    8c010000:  2102  mov.l r0,@r1 ; r1 = 0xf6000000     <- entry 0, indexed
    8c010002:  2542  mov.l r4,@r5 ; r5 = 0xf6000100     <- entry 1, indexed
    8c010004:  2762  mov.l r6,@r7 ; r7 = 0xf6000080     <- ASSOCIATIVE
    [ exception 0x140, pc=0x8c010004 vaddr=0x00000000 ]
    sh_exception(): exception 0x140 is not yet implemented.
      -> host process gone

*** SURVIVAL IS NOT ENOUGH, AND NEITHER IS EXPEVT PLUS PC.  Six mutants were BUILT
and measured against this row set. ***

    mutA  detection deleted                passes alive
    mutB  own arm -> general vector        passes alive
    mutC  own arm, pc + vbr only           passes alive, expevt, pc AND vbr
    mutD  n_hits > 2                       passes alive
    mutE  device raises RESET_MANUAL       passes alive, pc, vbr
    mutF  n_hits >= 1                      passes EVERY row on the trigger

`expevt == 0x140 && pc == 0xa0000000` kills mutA, mutB, mutD and mutE, and is passed
by mutC and mutF.  Two rows exist solely to kill those two:

  * `sr under FD` -- pre-sets SR to 0x40008000 (MD|FD, IMASK=0) before the trigger,
    so the reset transition's THIRD statement becomes observable.  From the
    reset-default SR that statement is a NO-OP (IMASK already 0xf, FD already clear),
    which is exactly why mutC -- an arm that sets pc and vbr and forgets it -- is
    invisible to every other row.  Figure 5.2 (`sh7750_hardware.txt:12228`) specifies
    SR.{MD,RB,BL,FD,IMASK} <- 11101111 for this transition.
  * `single hit` -- the identical program with entry 1 given a DIFFERENT VPN.  Nothing
    should fire.  It is the only row that sees mutF, which fires on one match.

*** THE RIG IS LANDISK, NOT TESTSH, AND THAT IS FORCED. ***  landisk's PROM leaves
`vbr = 0x8c000000` (`promemul/sh_ipl_g.c:55`), so `vbr == 0` after the fault is a REAL
transition and mutB's `vbr + 0x100` is distinguishable.  Measured cold-start `vbr` on
testsh is already `0x00000000`, which would make that row vacuous there.

Two further facts worth carrying, both measured rather than assumed:

  * The exception flips `SR.RB`, so `r0-r7` are the other bank afterwards.  Anything
    read back across the fault uses `r8-r15`, which are unbanked.
  * `cpu_sh.c` USED TO rewrite ANY expevt to `EXPEVT_RESET_POWER` when `SR.BL` is set
    (a BL-set guest silently latched `0x000`, the multiple hit included).  #577 makes it
    `EXPEVT_RESET_MANUAL` with the multiple-hit code exempt; the BL rows at the end of
    this file pin both halves.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c010000
UTLB_AA = 0xf6000000           # SH4_UTLB_AA, 16 MB window
ENTRY0 = UTLB_AA + 0x000
ENTRY1 = UTLB_AA + 0x100
ASSOC = UTLB_AA + 0x080        # SH4_UTLB_A, the associative form
VPN_A = 0x12345100             # VPN 0x12345000, ASID 0, V=1
VPN_B = 0x22345100             # a DIFFERENT VPN -- the single-hit control

MOV_L_R0_AT_R1 = 0x2102        # mov.l r0,@r1
MOV_L_R4_AT_R5 = 0x2542        # mov.l r4,@r5
MOV_L_R6_AT_R7 = 0x2762        # mov.l r6,@r7

rows = []


def row(name, got, want):
    ok = (got == want)
    rows.append(ok)
    print("%-14s %-24s %-24s %-10s %s"
          % (name, got, want, "#457", "ok" if ok else "FAIL"))


def session(pre=(), entry1_vpn=VPN_A, settle=8.0, trigger=True, program=None, steps=None):
    """Install two UTLB entries then do the associative write. Returns (regs, died).

    `pre` runs before the trigger -- used to pre-set SR so the reset transition's
    SR update is observable.
    #577: `program` (a list of 16-bit words placed at CODE) and `steps` replace the
    three-store multiple-hit program for the BL rows; the default is that program.
    """
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    alive = rd(settle)
    #  *** THE CONTROL MUST NOT RUN THE TRIGGER. ***  The first draft ran the three
    #  stores unconditionally, so the "does the session come up" control EXERCISED the
    #  defect and reported DEAD on the committed build -- a control failing for the
    #  very reason it exists to rule out.  Rule 4: did it fail for the reason under
    #  test?  It did not.
    if program is None:
        trig = ["r0=0x%08x" % VPN_A, "r1=0x%x" % ENTRY0,
                "r4=0x%08x" % entry1_vpn, "r5=0x%x" % ENTRY1,
                "r6=0x%08x" % VPN_A, "r7=0x%x" % ASSOC,
                "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),
                "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R4_AT_R5),
                "put h 0x%x, 0x%04x" % (CODE + 4, MOV_L_R6_AT_R7),
                "pc=0x%x" % CODE, "step 3"]
    else:   # #577: an arbitrary short program; the caller seeds registers through `pre`
        trig = ["put h 0x%x, 0x%04x" % (CODE + 2 * i, w) for i, w in enumerate(program)]
        trig += ["pc=0x%x" % CODE, "step %d" % (steps if steps is not None else len(program))]
    cmds = list(pre) + ([] if not trigger else trig) + [
        #  `registers` does not exist as a command, and a bare dump would not show
        #  these anyway: cpu_sh.c prints expevt/vbr only under `coprocs & 2`.
        #  `print <name>` reads them through CPU_SETTINGS_ADD_REGISTER32.  Established
        #  by trying the candidates against a live session, not assumed.
        "print expevt", "print pc", "print vbr", "print sr"]
    for c in cmds:
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(1.2):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.2)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, not alive


def reg(t, name):
    """Read back one `print <name>`: the debugger echoes the command, then the value.

    Anchored to the ECHO rather than scanning for a bare hex word, because the
    transcript is full of addresses and the wrong one would be indistinguishable from
    the right one -- the same reason this project's verdict extractor anchors instead
    of grepping.
    """
    m = re.search(r"print\s+%s\s*\r?\n\s*0x([0-9a-f]+)" % re.escape(name), t)
    return ("0x%08x" % int(m.group(1), 16)) if m else "absent"


#  ---- control: the session comes up at all ------------------------------------
ctl, ctl_died = session(trigger=False)
print("SH_TLBMULTI_CONTROL=%s" % ("DEAD" if ctl_died else "OK"))
if ctl_died:
    print("SH_TLBMULTI_RESULT=0/0")
    sys.exit(0)

#  ---- the trigger, at reset-default SR ----------------------------------------
t, died = session()
row("tlbm alive", "died" if died else "alive", "alive")
row("tlbm expevt", reg(t, "expevt") if not died else "died", "0x00000140")
row("tlbm pc", reg(t, "pc") if not died else "died", "0xa0000000")
row("tlbm vbr", reg(t, "vbr") if not died else "died", "0x00000000")

#  ---- the SR row: the ONLY row that sees a pc+vbr-only arm --------------------
t2, died2 = session(pre=["sr=0x40008000"])
row("tlbm sr", reg(t2, "sr") if not died2 else "died", "0x700000f0")

#  ---- the single-hit control: the ONLY row that sees `n_hits >= 1` ------------
#  A LIVENESS control too: it proves the three stores execute and the session
#  survives them, so "died" on the rows above is the SECOND match and not the
#  program.
t3, died3 = session(entry1_vpn=VPN_B)
row("tlbm single", "died" if died3 else reg(t3, "expevt"), "0x00000000")


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

print("SH_TLBMULTI_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
