#!/usr/bin/env python3
#
#  #498 sgidewidth -- the detector.
#
#  CONTRACT (vacuity-floor clause (e)) -- which edits this detector is designed
#  to catch, and which it is NOT:
#
#    CATCHES
#      * reinstatement of the width kill, in either direction (`lo_decl',
#        `lo_alive', and the read-side `hi_rd_*' rows);
#      * a decline that does not answer the read -- an early `return', or
#        `return 0' which cpus/memory_rw.c coerces to -1 and turns into a guest
#        EXCEPTION_DBE.  `lo_sent' and `hi_rd_sent' preset the destination
#        register to a SENTINEL, so "the tail ran and wrote odata (0)" and "the
#        load never completed" are distinguishable.  A survival-only oracle at
#        a refusal site is vacuous by construction;
#      * a decline that FALLS THROUGH to the tail, which would run
#        draw_primitive() for an access we just refused (`hi_draw',
#        `hi_rd_draw').  MEASURED: the naive splice scores 19/25 here;
#      * a decline that falls through to the register SWITCH, which then
#        announces a TODO about a write that never happened (`dec_switch').
#        MEASURED: the otherwise-plausible "clear startFlag and fall through"
#        shape scores 24/25 and this is the row it reds;
#      * a repair qualified to writes only -- the read-direction rows are not
#        redundant with the write ones (`hi_rd_*' kill that mutant at 21/25);
#      * a repair hoisted so it applies to EVERY access, which would silently
#        disable all drawing (`tail_acc' is the only row that catches it);
#      * reuse of #497's latch bit instead of a new one (`sharedlatch'):
#        the four handlers share one malloc'd struct, so sharing a bit lets an
#        sgi_re access silence sgi_de's decline entirely.  MEASURED 23/25;
#      * loss of the latch, so the decline floods (`lo_latch' COUNTS).
#
#    DOES NOT CATCH
#      * anything in the UPPER HALF that depends on the host surviving.  Every
#        access to +0x800..+0xfff already ends the host inside draw_primitive()
#        -- 254 of 256 drawing ops are unimplemented and the reset value is one
#        of them.  That is `sgideprimop', a separate row, and it is why the
#        accept rows below sit at +0x7fc/+0x7f8 rather than at the nominal last
#        slots.  A row that wanted survival up there would be testing the wrong
#        defect;
#      * an edit that changes only the message TEXT.  The rows count the
#        decline, they do not pin its wording beyond the `len=' prefix;
#      * anything in sgi_re, sgi_mte or sgi_de_status.
#
#  *** THE ROW SET IS NOT INVENTED HERE.  Each row below killed a specific
#  mutant in a nine-build, 25-row table measured before this file existed;
#  scores and variant sources are preserved under
#  regress/artifacts/sgidewidth/opus_witness_20260831/.  A row whose mutant is
#  named in its note is a row that has failed at least once. ***
#
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_kernel.bin")
if not os.path.exists(DUMMY):
    DUMMY = "/dev/null"

CODE = 0xffffffff80001000
SCRATCH_RAM = 0xffffffff80002000
DE = 0xffffffffb5002000              # sgi_de   @ phys 0x15002000
RE = 0xffffffffb5001000              # sgi_re   @ phys 0x15001000
DE_STATUS = 0xffffffffb5003000       # sgi_de_status, for the device signature

#  Hand-assembled, and every one is re-derived rather than copied: opcode(6)
#  rs(5) rt(5) imm(16).  Stores use a3 (reg 7) for the address and t0 (reg 8)
#  for the datum; loads use at (reg 1) and v0 (reg 2).
OP_NOP = 0x00000000
OP_B_SELF = 0x1000ffff
OP_SB_T0_A3 = 0xa0e80000             # sb   $t0, 0($a3)   101000 00111 01000
OP_SH_T0_A3 = 0xa4e80000             # sh   $t0, 0($a3)   101001 00111 01000
OP_SW_T0_A3 = 0xace80000             # sw   $t0, 0($a3)   101011 00111 01000
OP_SD_T0_A3 = 0xfce80000             # sd   $t0, 0($a3)   111111 00111 01000
OP_LBU_V0_AT = 0x90220000            # lbu  $v0, 0($at)   100100 00001 00010
OP_LW_V0_AT = 0x8c220000             # lw   $v0, 0($at)   100011 00001 00010
OP_LD_V0_AT = 0xdc220000             # ld   $v0, 0($at)   110111 00001 00010

DECL = "sgi_de: unimplemented len="          # the fix's decline announcement
KILL = "sgi_de: len = "                      # the pre-fix host kill
DRAW = "sgi_de: UNIMPLEMENTED drawing op"    # sgideprimop, the SECOND kill
SCIS = "sgi_de: TODO: non-zero CRIME_DE_SCISSOR"
RE_DECL = "sgi_re: unimplemented len=1 for CRIME_RE_TLB_A"

SENTINEL = 0xdeadbeef

rows = []


def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-14s %-14s %-44s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True

    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            alive = False
            break
    try:
        os.write(fd, b"quit\n")
        rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), alive, how


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    if not m:
        return "absent"
    return "0x%x" % int(m.group(1), 16)


def printed32(t, reg):
    """The low 32 bits of a register loaded by `lw`.

    *** lw SIGN-EXTENDS.  A 32-bit read of 0xcafebabe lands in the 64-bit
    register as 0xffffffffcafebabe, and a row comparing the raw string then
    FAILS on MIPS semantics rather than on device behaviour.  That bit this
    detector on its first run -- 21/22 with the device entirely correct --
    and the two neighbouring accept rows passed only because their fixtures
    happen to have bit 31 CLEAR. ***

    Masking rather than choosing a friendlier constant is deliberate: it
    makes the row correct BY CONSTRUCTION for any value, instead of correct
    by an accident of the fixture that the next person to edit it cannot
    see.  Nothing is lost -- for a `lw` the upper 32 bits carry no device
    data, only the sign extension.
    """
    v = printed(t, reg)
    if v == "absent":
        return v
    return "0x%x" % (int(v, 16) & 0xffffffff)


class Addr(object):
    def __init__(self, base):
        self.a = base

    def take(self, n):
        got = self.a
        self.a += 4 * (n + 2) + 0x20
        return got


def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def store(A, addr, op=OP_SW_T0_A3, val="0x12345678"):
    return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))


def load(A, addr, op=OP_LW_V0_AT):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))



LINB_DECL = "sgi_re: unimplemented len=1 for CRIME_RE_LINEAR_B"

print("#498 DISCRIMINATOR -- rows the shipped 25 do not have")
print("%-16s %-14s %-14s %-44s %s" % ("row", "got", "want", "note", ""))

A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM, val="0xcafe00d")
                        + load(A, SCRATCH_RAM) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0xcafe00d", "LIVENESS")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x048, val="0x12345678"))
row("devsig", t.count(SCIS + ": 0x0000000012345678"), 1, "DEVSIG")

#  --- against `bracegoto': TWO declined accesses in ONE session ---
A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + store(A, DE + 0x8d0, op=OP_SB_T0_A3, val="0x02"),
                        spin=1.6)
row("d2_hi_draw", t.count(DRAW), 0,
    "2nd DECLINED write must not reach draw_primitive")
row("d2_hi_alive", how, "exit0", "...and must not end the host")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + store(A, DE + 0x048, op=OP_SB_T0_A3, val="0x01"))
row("d2_switch", t.count(SCIS), 0,
    "2nd DECLINED write must not announce a TODO about it")

A = Addr(CODE)
t, alive, how = session(store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x01")
                        + load(A, DE + 0x8d0, op=OP_LBU_V0_AT) + ["print v0"],
                        spin=1.6)
row("d2_hi_rd", t.count(DRAW), 0, "2nd declined READ must not draw")

#  --- against `bit5collide': the OTHER four sibling bits ---
#  `sharedlatch' only pins TLB_A (1<<0).  LINEAR_B is 1<<5.
A = Addr(CODE)
t, alive, how = session(store(A, RE + 0x780, op=OP_SB_T0_A3, val="0x5a")
                        + store(A, DE + 0x0d0, op=OP_SB_T0_A3, val="0x5a"))
row("linb_first", t.count(LINB_DECL), 1, "#497's LINEAR_B latch fires first")
row("sharedlatch_b", t.count(DECL), 1,
    "sgi_de's bit must not collide with LINEAR_B's either")

n_ok = sum(1 for _, ok in rows if ok)
print("")
print("DISC_CONTROL=%s" % ("OK" if rows and rows[0][1] and rows[1][1] else "DEAD"))
print("DISC_RESULT=%d/%d" % (n_ok, len(rows)))
print("DISC_DONE")
