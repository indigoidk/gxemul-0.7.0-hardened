#!/usr/bin/env python3
"""pcc2widthkills -- RUNG-3 WITNESS for the access-width host kills in dev_pcc2.c.

DEFECT.  DEVICE_ACCESS(pcc2) has TEN register arms of the shape

    case PCCTWO_GENCTL:
            if (len != 1) {
                    fatal("TODO: pcc2: non-byte reads and writes of PCCTWO_GENCTL\\n");
                    exit(1);
            }

A guest choosing an access WIDTH ends the host process.  The killing widths are 2
and 4 -- ordinary, naturally alignable -- so a plain aligned halfword load of a
documented register is enough.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).

*** THE COUNT IS TEN, NOT TWELVE. ***  OUTSTANDING_BUGS.md's row says "twelve ... lines
359, 371, 394, 407, 429, 467, 477, 492, 507, 528, 543, 563".  Lines 543 and 563 are the
PCCTWO_IPL and PCCTWO_MASK arms, and both are ALREADY #119 warn-once latches, not kills.
The adjudication's "5 of the 10" is the right denominator.  Records defect, noted here so
the round's own record does not copy the twelve forward.

REACHABILITY, from OB:widthkillclass (2026-08-30), verified by reading
cpus/cpu_m88k_instr_loadstore.c: every NON-byte m88k access checks alignment BEFORE
memory_rw and raises MISALIGNED_ACCESS, and `relative_addr %= PCC2_SIZE' (0x40) keeps an
odd offset odd in all 64 aliases.  So only the EVEN-offset arms are guest-reachable:

    REACHABLE (5)     GENCTL 0x02   T2CTL 0x16   T2ICR 0x1a   SCCERR 0x1c   SCCTX 0x1e
    UNREACHABLE (7)   VECBASE 0x03  PSCALEADJ 0x15  T1CTL 0x17  T1ICR 0x1b  SCCICR 0x1d
                      SCCRX 0x1f  SCSIICR 0x2f    (odd -- a non-byte access cannot land)

    and of the five, only SCCERR 0x1c is 4-aligned, so a WORD access reaches one arm
    and a HALFWORD access reaches all five.

RUNG 3: real MC88100 instructions (ld.b / ld.h / ld / st.h / st.b) executed by the CPU
through real address decode and real memory_rw, on the UNMODIFIED in-tree
`-E mvme88k -e mvme187' (the only machine that instantiates pcc2, at PCC2_BASE 0xfff42000).
*** THE FIRST RUN PASSED `-e 187' AND EVERY ROW WENT RED, INCLUDING THE PURE-RAM CONTROL --
which is the control doing its job: "Unknown subtype '187'", exit 1, no session ever
started.  0/10 was the witness failing for the WRONG reason, and mechanical rule 4 says
do not claim it.  The subtype alias is `mvme187'. ***
No mvme88k rig exists here, so this is the strongest witness available; boot is not.

*** FIRST CORRECTED RUN: 3/10 -- controls green, three kills red FOR THE REASON UNDER
TEST, and one row red for MY reason: the liveness loads read a scratch word that no
instruction in THAT session had stored (each session is a fresh emulator), so they read
0 instead of 0x5a5a5a5a.  r4 was preset to a sentinel, so 0 vs sentinel vs absent were
still three distinguishable states -- but the row's note said "runs on to the RAM load"
and its want assumed a store the program did not contain.  Every kill session now
STORES the scratch word before the killing access. ***

TEST-FIRST SHAPE: every `want' below is the FIXED behaviour.  On the committed pre-fix
build the kill rows red (how == exit1); after the fix the same script goes green.

CONTROLS, clause (ii) of the witness ladder:
    live     a RAM word round-trips through the same decode
    devsig   a byte WRITE to CHIPID makes the DEVICE speak ("IGNORING write to read-only
             PCCTWO_CHIPID/CHIPREV") -- RAM emits no text, ever.  Independent of the
             width path, so it controls for "a device is there" without borrowing the
             channel under test.
    byte rd  the LEGAL width (ld.b) at the same register the kill row uses -- must be
             serviced on BOTH builds, so a fix that declines too much reds it.

ENCODING (immediate form): op26<<26 | rD<<21 | rS1<<16 | imm16.  Derived from the tree's
own constants -- m88k_idle_probe.py's `ld r13,r2,0' is 0x15a20000, i.e. op26 0x05, and
cpu_m88k_instr.c's dispatch gives ld.h 0x06, ld.b 0x07, st 0x09, st.h 0x0a, st.b 0x0b.

Sentinel: PCC2_WIDTH_WITNESS_DONE
"""

import os, pty, re, select, sys, time

if len(sys.argv) < 2:
    sys.stderr.write("usage: pcc2_width_witness.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"

DUMMY = "/tmp/pcc2_dummy.bin"
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x00010000            # guest code page
SCRATCH = 0x00020000         # RAM scratch, a DIFFERENT page from the code
PCC2 = 0xfff42000            # PCC2_BASE, mvme_pcctworeg.h
GENCTL, T2CTL, SCCERR, CHIPID = 0x02, 0x16, 0x1c, 0x00

#  r2 = PCC2 base, r3 = scratch, r4 = load target, r5 = store source.
def enc(op26, rd, rs1, imm):
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)

I_ST_W_R5_R3   = enc(0x09, 5, 3, 0)          # st   r5,r3,0      RAM
I_LD_W_R4_R3   = enc(0x05, 4, 3, 0)          # ld   r4,r3,0      RAM
I_ST_B_R5_R2_0 = enc(0x0b, 5, 2, CHIPID)     # st.b r5,r2,0x00   devsig (write-ignored msg)
I_LD_B_R4_R2_2 = enc(0x07, 4, 2, GENCTL)     # ld.b r4,r2,0x02   legal width, control
I_LD_H_R4_R2_2 = enc(0x06, 4, 2, GENCTL)     # ld.h r4,r2,0x02   *** KILL: halfword read
I_LD_W_R4_R2_1C = enc(0x05, 4, 2, SCCERR)    # ld   r4,r2,0x1c   *** KILL: word read
I_ST_H_R5_R2_16 = enc(0x0a, 5, 2, T2CTL)     # st.h r5,r2,0x16   *** KILL: halfword write
I_BR_SELF = 0xc0000000                       # br . (op26 0x30, disp 0)

SENTINEL = 0xdeadbeef
DEVSIG = "IGNORING write to read-only PCCTWO_CHIPID"
rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64",
                       "0x10000:" + DUMMY])
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
    return "0x%x" % int(m.group(1), 16) if m else "absent"


def program(insns, at=CODE):
    """put the instruction words + a self-loop, point pc at them, step past them."""
    words = list(insns) + [I_BR_SELF, 0]
    cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
    return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]


SETUP = ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=0x5a5a5a5a", "r4=0x%x" % SENTINEL]

print("pcc2widthkills RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- controls
t, alive, how = session(SETUP + program([I_ST_W_R5_R3, I_LD_W_R4_R3]) + ["print r4"])
row("live", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "RAM word round-trips through the same decode")

t, alive, how = session(SETUP + program([I_ST_B_R5_R2_0]))
row("devsig", t.count(DEVSIG), 1,
    "a byte write to CHIPID makes the DEVICE speak -- RAM emits no text")

t, alive, how = session(SETUP + program([I_ST_W_R5_R3, I_LD_B_R4_R2_2, I_LD_W_R4_R3]) + ["print r4"])
row("byte rd", how, "exit0",
    "ld.b of GENCTL is the LEGAL width -- serviced on both builds")
row("byte rd liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "...and the guest runs on to the RAM load")

# ---------------------------------------------------------------- the kills
#  Each kill row is PAIRED with a positive post-access observable, because exit
#  status alone cannot tell "declined and quit" from "died with status 0".
t, alive, how = session(SETUP + program([I_ST_W_R5_R3, I_LD_H_R4_R2_2, I_LD_W_R4_R3]) + ["print r4"])
row("half rd", how, "exit0",
    "ld.h of GENCTL (aligned halfword READ) must not end the host")
row("half rd liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "...and the guest runs on -- kills a death however it is spelled")

t, alive, how = session(SETUP + program([I_ST_W_R5_R3, I_LD_W_R4_R2_1C, I_LD_W_R4_R3]) + ["print r4"])
row("word rd", how, "exit0",
    "ld of SCCERR (the one 4-aligned arm) must not end the host")
row("word rd liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "...and the guest runs on")

t, alive, how = session(SETUP + program([I_ST_W_R5_R3, I_ST_H_R5_R2_16, I_LD_W_R4_R3]) + ["print r4"])
row("half wr", how, "exit0",
    "st.h to T2CTL (aligned halfword WRITE) must not end the host")
row("half wr liv", printed(t, "r4") if alive else "died", "0x5a5a5a5a",
    "...and the guest runs on")

bad = [n for n, ok in rows if not ok]
print("PCC2W_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
print("PCC2W_LABEL=%s" % LABEL)
if bad:
    print("PCC2W_RED=%s" % ",".join(bad))
print("PCC2_WIDTH_WITNESS_DONE")
