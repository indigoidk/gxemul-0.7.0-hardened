#!/usr/bin/env python3
"""Gate 14's measuring instrument: ARM subtract-carry flags and undefined routing.

Prints one line per row:  <name> <got> <want> ok|FAIL
then ARM_FLAGS_CONTROL=OK|DEAD and ARM_FLAGS_RESULT=<passed>/<total>.
gate_arm.sh does the asserting.

How it measures
---------------
Cold debugger on `testarm` (SA1110), RAM at 0. The machine needs A file to
construct -- it prints usage and exits without one -- so a four-byte raw stub is
loaded at the code address purely to satisfy that; it is overwritten by every
row before anything executes. LITTLE-endian, so `dump` renders bytes in memory
order and every word read here is byte-swapped back (the PowerPC rig is the
opposite case, and mixing the two up silently transposes every answer).

The flags are read by the guest's OWN `mrs r3,cpsr`, never by a debugger
register print: `mrs` is the architectural read, and it is the same path a real
kernel uses. The result register is stored alongside, because these two defects
are FLAG defects -- the computed value was already right -- and a row that
checked only the flag could not tell a fixed flag from a broken result.

The carry contract (ARM ARM, DDI 0100, subtract family)
-------------------------------------------------------
For SUB/CMP/RSB the carry-out is NOT-BORROW: set iff the 32-bit subtraction did
not borrow. For SBC/RSC the operation is `a - b - NOT(C)` and the carry-out must
account for that borrow-in term.

#311 computed the flag as `a >= b` for all five. That is correct for the three
that have no borrow-in, and WRONG for SBC/RSC exactly when `a == b` and the
carry-in is clear: `a - a - 1` borrows, so carry must be CLEAR, and `a >= b`
reports it SET. The fix computes the flag from the full 64-bit result that the
file already has in hand (`c32 == c64`), which is the same answer as `a >= b`
whenever there is no borrow-in -- hence the many PIN rows here, which exist to
prove the fix did NOT disturb the three instructions that were already right.

The carry-in for each row is established by a plain SUBS, never by a debugger
write to cpsr: a debugger write sets cpsr but not the separate `flags` field the
dyntrans handlers actually read, so it would preset nothing. SUBS is the correct
choice because it is the one member of the family whose carry both the committed
build and the fix compute identically -- the preset cannot itself be the bug.

The undefined contract
----------------------
#312: ARM's permanently-undefined space must raise the Undefined Instruction
exception. The committed build reached `goto bad`, which sets cpu->running = 0
(cpu_dyntrans.c:2014) -- a legal-to-attempt encoding stopping the whole
emulator, the same halt class as #264/#309/#310. GDB's breakpoint instruction
lives in this space, which is why the tree already contained an `und` routing
for it at cpu_arm_instr.c -- unreachable, because the block above it matches the
identical encodings first and breaks.

The witness is the HANDLER, not the absence of a message: code planted at the
UND vector (0x04) stores a marker, the mode, and the return address. A row that
merely checked "the emulator did not halt" would pass if the instruction were
silently treated as a nop.

Row classes
-----------
  PIN  -- correct today and must stay. Most of this table is pins, on purpose:
          the fix rewrites a line shared by five instructions and two of them
          are the ones that were already right.
  DISC -- discriminator: the committed byte is the measured defect, and the
          want flips when the fix lands.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
STUB = sys.argv[2]

CODE = 0x8000
DEST = 0x9000
VECT = 0x0004                   # ARM_EXCEPTION_UND * 4, low vectors
#  Last instruction slot of a 4KB ic page. Deliberately NOT the page holding
#  CODE: there, pc+4 would land exactly on DEST and the expected lr would be
#  numerically equal to the witness address, which reads as a coincidence
#  rather than a measurement.
PAGE_END = 0xAFFC

#  Instruction words. Rd=r0, Rn=r1, Rm=r2 throughout; r3 carries cpsr.
SUBS_R6_R6_R7 = 0xE0566007      # subs r6,r6,r7   -- the carry preset
MRS_R3_CPSR   = 0xE10F3000      # mrs  r3,cpsr
STR_R3_R4     = 0xE5843000      # str  r3,[r4]
STR_R0_R4     = 0xE5840000      # str  r0,[r4]
STR_R0_R5     = 0xE5850000      # str  r0,[r5]
STR_LR_R5     = 0xE585E000      # str  r14,[r5]
STR_R0_R6     = 0xE5860000      # str  r0,[r6]
MOV_R0_5A     = 0xE3A0005A      # mov  r0,#0x5a
NOP           = 0xE1A00000      # mov  r0,r0

SBCS = 0xE0D10002               # sbcs r0,r1,r2
RSCS = 0xE0F10002               # rscs r0,r1,r2   (rd = r2 - r1 - !C)
SUBS = 0xE0510002               # subs r0,r1,r2
RSBS = 0xE0710002               # rsbs r0,r1,r2   (rd = r2 - r1)
CMPS = 0xE1510002               # cmp  r1,r2
SUBS_PC_4 = 0xE25F0004          # subs r0,pc,#4   (the A__PC template variant)
ADDS = 0xE0910002               # adds r0,r1,r2
ADCS = 0xE0B10002               # adcs r0,r1,r2

UDF        = 0xE7F000F0         # permanently undefined (UDF #0)
UDF_GDB    = 0xE6000010         # the GDB-breakpoint form, same space
UDF_EQ     = 0x07F000F0         # the same encoding, condition EQ
ARM_MODE_UND32 = 0x1b


def session(cmds, nwords):
    """Run one cold-debugger session; return (words, transcript)."""
    #  -A disables colorized output. Under pty.fork() both isatty() checks
    #  pass, so a CLICOLOR in the caller's environment would otherwise put
    #  ANSI escapes between "cpu " and the debugmsg name and silently fail
    #  every marker grep -- an environment-dependent FAIL that looks like a
    #  real regression (a round-99 review seat's catch).
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A", "-E", "testarm", "-M", "64",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=45):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if buf.rstrip().endswith(">"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(60):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None, buf

    for c in cmds:
        send(c)

    #  Retry the READ, never the row: a dump can straggle past the prompt
    #  detector under host load, and the value cannot change between dumps.
    #  A row that lost this retry showed up as a spurious DEAD in the very
    #  first baseline sweep.
    flat = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 4 * nwords))
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})",
                           buf[mark:])
        flat = "".join(words).split()
        if len(flat) >= nwords:
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return (flat[:nwords] if len(flat) >= nwords else None), buf


def sw(h):
    """dump renders little-endian bytes; recover the stored value."""
    return int.from_bytes(bytes.fromhex(h), "little")


def run_flags(iw, rn, rm, cin):
    """Preset the carry, run one flag-setting instruction, publish cpsr and rd.

    Returns (cpsr, rd) or (None, None) if the session died."""
    r6, r7 = (1, 0) if cin else (0, 1)      # 1-0 => no borrow => C=1
    w, _ = session([
        "r1=0x%x" % rn, "r2=0x%x" % rm,
        "r6=0x%x" % r6, "r7=0x%x" % r7,
        "r4=0x%x" % DEST, "r5=0x%x" % (DEST + 4),
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE,      SUBS_R6_R6_R7),
        "put w 0x%x, 0x%08x" % (CODE + 4,  iw),
        "put w 0x%x, 0x%08x" % (CODE + 8,  MRS_R3_CPSR),
        "put w 0x%x, 0x%08x" % (CODE + 12, STR_R3_R4),
        "put w 0x%x, 0x%08x" % (CODE + 16, STR_R0_R5),
        "pc=0x%x" % CODE, "step 5"], 2)
    if w is None:
        return None, None
    return sw(w[0]), sw(w[1])


def teq_imm(rot, imm8):
    return 0xE3310000 | (rot << 8) | imm8


def tst_imm(rot, imm8):
    return 0xE3110000 | (rot << 8) | imm8


MOV_R8_1   = 0xE3A08001         # mov  r8,#1     -- the pass counter
SUBS_R8_R9 = 0xE0588009         # subs r8,r8,r9  -- r9 = 1
BEQ_FWD3   = 0x0A000003         # beq  +3 words (the not-taken branch under test)
BEQ_BACK8  = 0x0AFFFFF8         # beq  -8 words (back to the top of the loop)


def run_combined(iw, rn, cin):
    """FREE-RUNNING, TWO PASSES: the only way to reach a *_samepage handler.

    Two facts have to hold at once, and each defeated an earlier attempt:

      1. `step` cannot work. cpu_dyntrans.c:1888 disables combining whenever
         single_step is set, so a stepped probe exercises the STANDALONE
         handler while appearing to exercise the combined one.

      2. A single forward run cannot work either WHEN A BREAKPOINT IS SET.
         arm_combine_instructions rewrites ic[-1].f -- the PREVIOUS
         instruction -- while the BRANCH is translated, and by then the
         compare has already executed. The combined handler therefore exists
         only from the SECOND pass over that ic slot onward.

         CORRECTION (round 100): this is true only with a breakpoint. The
         guard above is NOT the whole story -- translation READ-AHEAD
         (cpu_dyntrans.c translates up to 128 following instructions ahead
         of execution and runs the combiner for each) is separately gated on
         `cpu->machine->breakpoints.n == 0` (:1939). Every probe in THIS file
         uses `breakpoint add`, which sets breakpoints.n and turns read-ahead
         OFF -- forcing the two-pass install. A real guest sets no breakpoint,
         so the fold installs AHEAD of execution and a single forward pass
         reaches it. The netbsd_idle rows live in arm_idle_probe.py precisely
         so they can exercise that path (its register-alias and forward-beq
         defects are invisible under a breakpoint, because the two-pass
         install pre-writes the register the fold would otherwise read stale).
         The two-pass driver below stays correct for the flag rows here; it
         is just not the only way a fold is reached, contrary to what this
         comment used to assert as a law.

    So the compare and its branch sit inside a loop that runs exactly twice,
    and the flags published are the second pass's. r8 counts: 1 -> 0 sets Z and
    branches back, 0 -> -1 clears Z and falls through. The carry preset uses
    r7 = 0, so `subs r6,r6,r7` re-establishes C=1 on BOTH passes without
    changing r6 -- a decrementing preset would silently differ between them.

    The breakpoint goes after the loop, never on the pair: single_step_breakpoint
    is in the same guard but is transient (set at :1802-1823 only when pc equals
    a breakpoint address, cleared at :1930). Instruction tracing must stay off
    for the same reason -- it is the third term of that guard."""
    r6, r7 = (1, 0) if cin else (0, 1)
    w, _ = session([
        "r1=0x%x" % rn, "r0=0x0",
        "r6=0x%x" % r6, "r7=0x%x" % r7, "r9=0x1",
        "r4=0x%x" % DEST,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE,      MOV_R8_1),
        # loop top
        "put w 0x%x, 0x%08x" % (CODE + 4,  SUBS_R6_R6_R7),
        "put w 0x%x, 0x%08x" % (CODE + 8,  iw),
        "put w 0x%x, 0x%08x" % (CODE + 12, BEQ_FWD3),
        "put w 0x%x, 0x%08x" % (CODE + 16, MRS_R3_CPSR),
        "put w 0x%x, 0x%08x" % (CODE + 20, STR_R3_R4),
        "put w 0x%x, 0x%08x" % (CODE + 24, SUBS_R8_R9),
        "put w 0x%x, 0x%08x" % (CODE + 28, BEQ_BACK8),
        # loop exit / breakpoint
        "put w 0x%x, 0x%08x" % (CODE + 32, NOP),
        "breakpoint add 0x%x" % (CODE + 32),
        "pc=0x%x" % CODE, "continue"], 2)
    if w is None or w[0] == "deadbeef":
        return None
    return sw(w[0])


#  eor Rd,Rn,Rm == 0xE0200000 | (Rn << 16) | (Rd << 12) | Rm.
#
#  The MATCHER's shape is `eor X,Y,X` -- Rm == Rd -- because eor_regshort's
#  arg[0] is Rn, arg[1] is Rm and arg[2] is Rd (cpu_arm_instr_dpi.c:72/110/252).
#  The first version of this control emitted `eor r0,r0,r1`, which is Rn == Rd,
#  so it never matched the combiner at all and was measuring three standalone
#  EORs while claiming to exercise the fold. A review seat caught it. The
#  same-register row is unaffected -- every operand collapses to one register,
#  so it matches under either reading -- which is why the DISC measurement below
#  stands and only the control had to be rebuilt.
EOR_R0_R0_R0 = 0xE0200000       # eor r0,r0,r0  -- zeroes r0, three times over
EOR_R0_R1_R0 = 0xE0210000       # eor r0,r1,r0  -- r0 ^= r1
EOR_R1_R0_R1 = 0xE0201001       # eor r1,r0,r1  -- r1 ^= r0
MOV_R1_A5    = 0xE3A010A5       # mov r1,#0xa5
STR_R1_R5    = 0xE5851000       # str r1,[r5]
BEQ_BACK10   = 0x0AFFFFF6       # beq -10 words, back to the loop top


def run_xchg(same_reg):
    """Two-pass free-running witness for the XOR-swap fold (see run_combined
    for why both properties are needed).

    The combiner folds `eor a,a,b / eor b,b,a / eor a,a,b` into X(xchg), which
    swaps the two registers -- but its match has NO a != b guard, so three
    `eor rX,rX,rX` also match. Standalone, each of those ZEROES rX; the folded
    swap exchanges rX with itself and leaves it alone.

    r0 is re-seeded to 0x5a at the TOP of the loop, which is what makes the two
    passes distinguishable: without it pass 1 would zero r0 and pass 2's
    "unchanged" would also read zero, and the row could not fail.

    A result of 0x5a is unambiguous -- three standalone EORs cannot leave a
    nonzero value, so only the folded handler can produce it, and it is both
    the defect and the proof that the fold occurred. A result of 0 is the
    correct answer but does NOT by itself prove the fold happened, so it is
    never read as evidence of a fix on its own."""
    seq = ([EOR_R0_R0_R0] * 3 if same_reg
           else [EOR_R0_R1_R0, EOR_R1_R0_R1, EOR_R0_R1_R0])
    w, _ = session([
        "r0=0x0", "r1=0x0", "r9=0x1",
        "r4=0x%x" % DEST, "r5=0x%x" % (DEST + 4),
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE,      MOV_R8_1),
        #  BOTH registers are re-seeded at the loop top, and to DISTINCT
        #  values. Seeding r1 once outside the loop was the second half of the
        #  same review finding: pass 1 would leave r1 == r0, so on pass 2 a
        #  correct swap and a no-op would both answer 0x5a and the control
        #  could not fail.
        "put w 0x%x, 0x%08x" % (CODE + 4,  MOV_R0_5A),   # loop top
        "put w 0x%x, 0x%08x" % (CODE + 8,  MOV_R1_A5),
        "put w 0x%x, 0x%08x" % (CODE + 12, seq[0]),
        "put w 0x%x, 0x%08x" % (CODE + 16, seq[1]),
        "put w 0x%x, 0x%08x" % (CODE + 20, seq[2]),
        "put w 0x%x, 0x%08x" % (CODE + 24, STR_R0_R4),
        "put w 0x%x, 0x%08x" % (CODE + 28, STR_R1_R5),
        "put w 0x%x, 0x%08x" % (CODE + 32, SUBS_R8_R9),
        "put w 0x%x, 0x%08x" % (CODE + 36, BEQ_BACK10),
        "put w 0x%x, 0x%08x" % (CODE + 40, NOP),
        "breakpoint add 0x%x" % (CODE + 40),
        "pc=0x%x" % CODE, "continue"], 2)
    if w is None or w[0] == "deadbeef":
        return None
    return sw(w[0]), sw(w[1])


#  #345/#346: NetBSD cache-clean fold. The matcher (COMBINE(netbsd_cacheclean)
#  in cpu_arm_instr.c; numeric line cites here went stale twice in two rounds,
#  so this one is by symbol) tested
#  only the SHAPE of the loop -- a post-indexed word load, `subs rX,rX,#32`, a
#  branch back to the load -- while X(netbsd_cacheclean) hardcodes
#  `r[0] += r[1]; r[1] = 0`. #345 pinned the two registers the handler WRITES;
#  #346 pins the load's own remaining two operands, because that closed form is
#  arithmetic that only holds for a 32-BYTE STRIDE.
#
#  The genuine sequence, from the comment above X(netbsd_cacheclean):
#
#      ldr  r2,[r0],#32        subs r1,r1,#0x20        bne back        mcr ...
#
#  All four loops below are built from that with exactly ONE field wrong, so
#  each row attributes its answer to one guard.
SUBS_R6_32   = 0xE2566020       # subs r6,r6,#32
SUBS_R1_32   = 0xE2511020       # subs r1,r1,#32
BNE_BACK4    = 0x1AFFFFFC       # bne  -4 words, back to the load
MCR_CLEAN    = 0xEE070F9A       # the iword that arms the combination check
MOV_R6_32    = 0xE3A06020       # mov  r6,#32  -> one subs reaches zero
MOV_R1_32    = 0xE3A01020       # mov  r1,#32
MOV_R0_11    = 0xE3A00011       # mov  r0,#0x11 -- sentinel the loop never uses
MOV_R1_22    = 0xE3A01022       # mov  r1,#0x22
MOV_R5_9100  = 0xE3A05C91       # mov  r5,#0x9100  (safe RAM as the load base)
MOV_R0_9100  = 0xE3A00C91       # mov  r0,#0x9100
MOV_R2_77    = 0xE3A02077       # mov  r2,#0x77 -- the load's destination seed
MOV_R6_66    = 0xE3A06066       # mov  r6,#0x66 -- ditto for the wrong-Rd loop
STR_R0_R7    = 0xE5870000
STR_R1_R7_4  = 0xE5871004
STR_R2_R7_8  = 0xE5872008
STR_R6_R7_12 = 0xE587600C

#  Round 99: the outer back-branch is COMPUTED from the program layout
#  (outer_beq below). Its predecessor BEQ_BACK16 was a hand-encoded offset
#  that was correct only for the 17-word #345/#346 program; adding the flag
#  seed and the cpsr publish would have silently retargeted it mid-program,
#  skipped the counter seeds on pass 2, and let `fold r0` and `still folds`
#  keep passing while measuring a different program -- the hand-assembled-
#  encoding trap this harness has recorded twice already.
MOV_R1_48    = 0xE3A01030       # mov  r1,#0x30 -- borrow-exit counter
MOV_R1_0     = 0xE3A01000       # mov  r1,#0    -- the #347 r1==0 disjunct
MOV_R1_33    = 0xE3A01021       # mov  r1,#0x21 -- non-multiple counter
MOV_R10_20   = 0xE3A0A020       # mov  r10,#0x20 -- zero-n pass-1 counter
MOV_R10_0    = 0xE3A0A000       # mov  r10,#0    -- zero-n pass-2 counter
MOV_R1_R10   = 0xE1A0100A       # mov  r1,r10   -- per-pass counter seed
CMP_R9_HI    = 0xE3590208       # cmp  r9,#0x80000000 (0x08 ror 4; r9=1 ->
                                #   N1 Z0 C0 V1 = 0x9: every NZCV bit must
                                #   move to reach the 0x6 answer. 0xE3590102
                                #   encodes the same value; this one is the
                                #   form the round-99 repro measured live)
CMP_R9_1     = 0xE3590001       # cmp  r9,#1 (r9=1 -> 0 -> Z1 C1 = 0x6)

CC_BASE = 0x9100                # safe RAM, clear of DEST..DEST+19
CC_MEM  = 0xA5A5A5A5            # the word the load must fetch from CC_BASE

#  #349's fold-fired markers, anchored to the debugmsg line shape. On this
#  1-machine 1-cpu rig the line is `[ cpu <name>: combined N iterations ]`
#  -- there is NO "cpu0:" prefix (debugmsg.c:213-232 prints it only for
#  multiple machines/cpus). Anchoring on `cpu <name>: combined` survives
#  both the name-prefix collision (cacheclean vs cacheclean2) and pty ECHO
#  of the probe's own typed commands, which lands in the same transcript.
MARK1 = re.compile(r"cpu netbsd_cacheclean: combined")
MARK2 = re.compile(r"cpu netbsd_cacheclean2: combined")


def outer_beq(branch_idx, target_idx=1):
    """Backward BEQ from program word branch_idx to word target_idx
    (ARM B offset: target = branch + 8 + imm24*4)."""
    return 0x0A000000 | ((target_idx - branch_idx - 2) & 0xFFFFFF)


def verb_cmds():
    """Raise the cpu subsystem to DEBUG and echo the setting back. The
    echo line ("3: DEBUG") is each fires-session's own positive control
    that the level took -- an absence row under a verbosity that silently
    failed to rise would pass for the wrong reason."""
    return ["verbosity cpu 3", "verbosity cpu"]


def marker_count(buf, mark):
    return len(mark.findall(buf)) if buf else 0


def verb_took(buf):
    return "3: DEBUG" in (buf or "")


def ldr_post(rn, rd, imm):
    """LDR Rd,[Rn],#imm -- post-indexed, immediate, U=1 W=0 (add, no writeback
    bit; post-index always writes back). arg[0]=&r[Rn], arg[1]=imm,
    arg[2]=&r[Rd] (the load/store decode in cpu_arm_instr.c's main-opcode-4
    case, and cpu_arm_instr_loadstore.c:118)."""
    return 0xE4900000 | (rn << 16) | (rd << 12) | imm


def run_cacheclean(variant, seed=NOP, verbose=False):
    """Two-pass witness for the cache-clean fold's operand checks.

    The inner `bne` never has to be TAKEN -- the matcher inspects the branch's
    target at translation time, not its outcome -- so the counter is seeded to
    32 and one `subs` reaches zero, except in "genuine40", whose TWO
    iterations are load-bearing for #348: with a 0x20 counter, a broken fix
    that skipped the `r[1] = 0x20` preload and delegated the subs on the LIVE
    counter would produce bit-identical registers AND flags, and no row could
    see it (a round-99 review seat's finding). At 0x40 the two diverge:
    correct code answers r1 = 0 with flags Z|C; a missing preload answers
    r1 = 0x20 with C alone. What must happen twice is entry to the whole
    block, because the combiner rewrites ic[-3] while the MCR is translated,
    so the folded handler only exists from the second pass (see run_combined).

    `seed` is one extra instruction word run LAST among the seeds on every
    pass -- the flag preset for the #348 rows, a NOP elsewhere -- so the
    value the cpsr row reads cannot have been left by anything but the loop.
    `verbose=True` raises the cpu subsystem to DEBUG first and echoes the
    setting back (the #349 fires rows; the echo is the session's own proof
    the level took). Returns ((r0, r1, r2, r6, cpsr), transcript).

    Five program variants, one field each:

      "wrongregs" -- base r5, counter r6, stride 32. #345's guard. Folded it
          answers r0 = 0x11 + 0x22 = 0x33 and r1 = 0; architecturally r0 and r1
          are untouched. Its stride is 32 ON PURPOSE, so that #346's immediate
          check cannot block this fold and quietly stand in for #345's.

      "genuine"   -- the real sequence, counter 0x20, and a fold CONTROL: it
          must STILL fold, or the guards are over-tight and the optimisation
          is silently dead. r0 CANNOT discriminate here -- the closed form is
          exactly right for a 32-stride loop, and both answers are 0x9120
          (measured). What separates them is r2: the handler never performs
          the load, so folded r2 keeps its seed 0x77, while unfolded it holds
          CC_MEM. That stale destination is a real defect round 99 did NOT fix
          (see OUTSTANDING_BUGS); the row pins today's behaviour precisely
          because it is a fold detector independent of #349's marker.

      "genuine40" -- the real sequence, counter 0x40: carries the #348 flag
          and counter rows (see above).

      "imm4"      -- the same loop with `ldr r2,[r0],#4`. #346's discriminator:
          the fold advances r0 by 32 regardless, so it answered 0x9120 where the
          architecture returns 0x9104, and r2 was left at 0x77 instead of CC_MEM.

      "wrongdest" -- `ldr r6,[r0],#32`. Right stride, right base and counter,
          wrong destination: the fold fired and stranded r6 at 0x66 rather than
          CC_MEM.

    Every architectural answer above was taken from the identical program with
    the MCR replaced by a nop, so that nothing combines at all.
    """
    if variant == "wrongregs":
        seeds = [MOV_R6_32, MOV_R0_11, MOV_R1_22, MOV_R5_9100, MOV_R2_77]
        ldr, subs = ldr_post(5, 4, 0x20), SUBS_R6_32
    elif variant == "genuine":
        seeds = [MOV_R1_32, MOV_R0_9100, NOP, NOP, MOV_R2_77]
        ldr, subs = ldr_post(0, 2, 0x20), SUBS_R1_32
    elif variant == "genuine40":
        seeds = [MOV_R1_64, MOV_R0_9100, NOP, NOP, MOV_R2_77]
        ldr, subs = ldr_post(0, 2, 0x20), SUBS_R1_32
    elif variant == "imm4":
        seeds = [MOV_R1_32, MOV_R0_9100, NOP, NOP, MOV_R2_77]
        ldr, subs = ldr_post(0, 2, 0x04), SUBS_R1_32
    elif variant == "wrongdest":
        seeds = [MOV_R1_32, MOV_R0_9100, MOV_R6_66, NOP, MOV_R2_77]
        ldr, subs = ldr_post(0, 6, 0x20), SUBS_R1_32
    else:
        raise ValueError(variant)
    #  CODE+4 is the outer loop top: every seed re-runs on both passes, and
    #  the flag seed runs LAST.
    prog = [MOV_R8_1] + seeds + [seed] + [
        ldr,                    # ic[-3]
        subs,                   # ic[-2]
        BNE_BACK4,              # ic[-1]
        MCR_CLEAN,              # ic[0] -- arms the combination check
        MRS_R3_CPSR,
        STR_R0_R7, STR_R1_R7_4, STR_R2_R7_8, STR_R6_R7_12, STR_R3_R7_16,
        SUBS_R8_R9]
    prog += [outer_beq(len(prog)), NOP]
    cmds = ["r9=0x1", "r7=0x%x" % DEST,
            "put w 0x%x, 0x%08x" % (CC_BASE, CC_MEM)]
    cmds += ["put w 0x%x, 0xdeadbeef" % (DEST + 4 * i) for i in range(5)]
    cmds += ["put w 0x%x, 0x%08x" % (CODE + 4 * i, iw)
             for i, iw in enumerate(prog)]
    if verbose:
        cmds += verb_cmds()
    cmds += ["breakpoint add 0x%x" % (CODE + 4 * (len(prog) - 1)),
             "pc=0x%x" % CODE, "continue"]
    w, buf = session(cmds, 5)
    if w is None or w[0] == "deadbeef":
        return None, buf
    return tuple(sw(x) for x in w), buf


def run_cc_nonmult():
    """#350's witness: a counter that is not a multiple of 32 must NOT fold.

    Architecturally `subs r1,r1,#0x20` from 0x21 never reaches zero (the
    residue mod 32 is invariant), so the bne loop never exits; the unguarded
    fold terminated it. The program installs the fold with a genuine 0x20
    pass, then re-enters the SAME translated slot once with r1 = 0x21:

        word  0  mov r8,#1               outer-pass counter
              1  mov r1,#0x20            \\ phase-A seeds
              2  mov r0,#0x9100          /
              3  mov r2,#0x77
              4  ldr r2,[r0],#32         <- the fold slot
              5  subs r1,r1,#0x20
              6  bne -> 4
              7  mcr (arms; fold exit lands at word 8)
              8  mov r1,#0x21            phase-B counter
              9  subs r8,r9              1->0 Z=1 first time, 0->-1 Z=0 after
             10  beq -> 4                taken exactly once: re-enter the fold
             11  str r0,[r7]             publish
             12  nop                     breakpoint

    UNGUARDED: the fold consumes r1 = 0x21, r0 += 0x21 = 0x9141 (odd), falls
    out to words 8-12 and hits the breakpoint without help. GUARDED: the
    handler falls back to the real load every iteration and the loop runs
    forever, exactly as the architecture says; the session is forced back to
    the prompt with ^C and the verdict read from the REGISTERS. "live"
    demands THREE things, and the third is load-bearing (a review seat's
    catch): r1 mod 32 == 1 (the residue invariant), r0 a multiple of 0x20,
    AND r0 advanced past phase A's 0x9120 -- because a broken guard that
    returned WITHOUT calling the load would also loop forever with the
    residue invariant intact, but its r0 would be parked at 0x9120. Only
    the genuine fallback's post-index writeback moves r0.

    The first version of this witness planted a handler at the data-abort
    vector and expected the walking load to fault at the top of RAM. That
    was measured FALSE on this tree: a read of non-existent physical memory
    logs `memory READ: from non-existant paddr=...` per access and execution
    CONTINUES with the load returning junk -- r0 was observed 4 MB past the
    top of RAM, still walking (pc mid-loop, r1 invariant holding, which is
    also the live proof the guard's fallback path executes real loads). The
    same first version compared the dump string against "deadbeef" without
    byte-swapping -- the little-endian transposition this file's header
    warns about -- and so read its own sentinel's parity as a measurement.
    Both mistakes are recorded here so the next witness starts further on.

    A "live" verdict proves the guard HELD; it cannot by itself prove the
    fold was ever INSTALLED -- a broken matcher yields the same infinite
    loop. Words 4-7 here are iword-identical to the genuine session's
    program, whose still-folds and fires rows carry installation for this
    shape; the coverage is cross-row by design.

    Returns "fold" (the defect: fold consumed the counter), "live" (guard
    held; loop genuinely running), a state string for anything else, or
    None if the session died."""
    prog = [MOV_R8_1, MOV_R1_32, MOV_R0_9100, MOV_R2_77,
            ldr_post(0, 2, 0x20),   # word 4: the fold slot
            SUBS_R1_32,
            BNE_BACK4,              # -> word 4
            MCR_CLEAN,
            MOV_R1_33,
            SUBS_R8_R9,
            0x0AFFFFF8,             # beq -> word 4 (imm24 = 4 - 10 - 2 = -8)
            STR_R0_R7, NOP]
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A", "-E", "testarm", "-M", "64",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if buf.rstrip().endswith(">"):
                return True
        return False

    def send(s, tmo=30):
        b = (s + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait(tmo)

    if not wait(60):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None
    send("r9=0x1")
    send("r7=0x%x" % DEST)
    send("put w 0x%x, 0x%08x" % (CC_BASE, CC_MEM))
    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("breakpoint add 0x%x" % (CODE + 4 * (len(prog) - 1)))
    send("pc=0x%x" % CODE)
    #  Prompt detection anchored PAST the continue echo: whole-buffer
    #  endswith() could match the stale pre-continue prompt, or a flood
    #  line's trailing '>'. Either mis-detection fails toward "dead" (the
    #  reg parse then starves), never toward a false verdict, but the
    #  anchor removes the stall.
    mark0 = len(buf)
    os.write(fd, b"continue\n")

    def wait_past_mark(timeout):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark0 and buf[mark0:].rstrip().endswith(">"):
                return True
        return False

    hit_bp = wait_past_mark(2.5)
    if not hit_bp:
        os.write(fd, b"\x03")
        if not wait(15):
            try:
                os.kill(pid, 9)
                os.waitpid(pid, 0)
            except Exception:
                pass
            return None
    mark = len(buf)
    send("reg")
    seg = buf[mark:]
    regs = {}
    for r in ("r0", "r1"):
        m = re.search(r"\b%s\s*=\s*0x([0-9a-f]+)" % r, seg)
        if not m:
            try:
                os.write(fd, b"quit\n")
                time.sleep(0.3)
                os.kill(pid, 9)
                os.waitpid(pid, 0)
            except Exception:
                pass
            return None
        regs[r] = int(m.group(1), 16)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    if hit_bp:
        return "fold" if (regs["r0"] & 1) else "exit-%x" % regs["r0"]
    if ((regs["r1"] & 0x1f) == 1 and (regs["r0"] & 0x1f) == 0
            and regs["r0"] != 0x9120):
        return "live"
    return "state-%x-%x" % (regs["r0"], regs["r1"])


def run_cc_zero_n():
    """#350's r1 == 0 arm: gate the HONEST iteration count via the marker.

    For a zero counter the fold's registers and flags are identical whether
    n is 2^27 or a reverted `r1 >> 5` (= 0) -- only the marker text and the
    batch billing differ -- so the adopted formula was unassertable by any
    state row (a review seat's catch). The #349 marker carries the count,
    so this row reads it back.

    Installing the fold by genuinely executing a zero-counter loop is
    infeasible (pass 1 would run 2^27 real iterations, walking the load
    past the top of RAM through the log flood), so the counter is seeded
    THROUGH A REGISTER that changes between passes: pass 1 runs the loop
    with r1 = r10 = 0x20 (one iteration, installs the fold), r10 is then
    cleared, and pass 2 re-enters with r1 = r10 = 0 -- the fold computes
    n = 2^27 instantly and prints it.

        word  0  mov r8,#1
              1  mov r10,#0x20
              2  mov r1,r10          <- outer loop top, re-runs both passes
              3  mov r0,#0x9100
              4  mov r2,#0x77
              5  ldr r2,[r0],#32     <- the fold slot
              6  subs r1,r1,#0x20
              7  bne -> 5
              8  mcr (arms)
              9  mov r10,#0          the second pass's counter
             10  subs r8,r9
             11  beq -> 2
             12  nop                 breakpoint

    Returns the printed count as a string, "none" if the marker never
    fired, or None if the session died."""
    prog = [MOV_R8_1, MOV_R10_20,
            MOV_R1_R10,             # word 2: outer loop top
            MOV_R0_9100, MOV_R2_77,
            ldr_post(0, 2, 0x20),   # word 5: the fold slot
            SUBS_R1_32,
            BNE_BACK4,              # -> word 5
            MCR_CLEAN,
            MOV_R10_0,
            SUBS_R8_R9,
            0x0AFFFFF5,             # beq -> word 2 (imm24 = 2 - 11 - 2 = -11)
            NOP]
    cmds = ["r9=0x1",
            "put w 0x%x, 0x%08x" % (CC_BASE, CC_MEM)]
    cmds += ["put w 0x%x, 0x%08x" % (CODE + 4 * i, iw)
             for i, iw in enumerate(prog)]
    cmds += verb_cmds()
    cmds += ["breakpoint add 0x%x" % (CODE + 4 * (len(prog) - 1)),
             "pc=0x%x" % CODE, "continue"]
    w, buf = session(cmds, 0)
    if w is None:
        return None
    m = re.search(r"cpu netbsd_cacheclean: combined (\d+) iterations",
                  buf or "")
    return m.group(1) if m else "none"


#  #347: the SECOND cache-clean fold, and a worse case than the first. The
#  genuine NetBSD sequence (from the comment above X(netbsd_cacheclean2)) is
#
#      mcr 15,0,r0,cr7,cr10,1     mcr 15,0,r0,cr7,cr6,1
#      add r0,r0,#0x20            subs r1,r1,#0x20        bhi back
#
#  The two MCRs are pinned by exact iword, but the add and the subs were tested
#  only for `rn == rd` and an immediate of 32 -- ANY register -- while the
#  handler updated NO registers at all. Both halves are measured below.
#
#  The genuine counter is 0x40, two iterations, so the loop's last subs
#  reaches ZERO; the borrow (0x30) and zero (0) counters exercise the other
#  exit, where the subs BORROWS (see run_cc2).
MCR_CC2_A  = 0xEE070F3A         # mcr 15,0,r0,cr7,cr10,1  -- ic[-4]
MCR_CC2_B  = 0xEE070F36         # mcr 15,0,r0,cr7,cr6,1   -- ic[-3]
ADD_R0_32  = 0xE2800020         # add  r0,r0,#0x20
ADD_R5_32  = 0xE2855020         # add  r5,r5,#0x20
BHI_BACK6  = 0x8AFFFFFA         # bhi  -6 words; the iword that arms the check
CMP_R9_2   = 0xE3590002         # cmp  r9,#2  (r9 == 1) -> N=1 Z=0 C=0 V=0
MOV_R1_64  = 0xE3A01040         # mov  r1,#0x40  -- two iterations
MOV_R6_64  = 0xE3A06040         # mov  r6,#0x40
MOV_R5_55  = 0xE3A05055         # mov  r5,#0x55 -- sentinel
STR_R5_R7_8  = 0xE5875008
STR_R3_R7_16 = 0xE5873010


def run_cc2(variant, seed=CMP_R9_2, verbose=False):
    """Two-pass witness for the SECOND cache-clean fold. Returns
    ((r0, r1, r5, r6, cpsr), transcript).

    Unlike variant 1 the trigger is the BRANCH itself (the iword ==
    0x8afffffa arming in cpu_arm_instr.c's to_be_translated, case 0xa --
    cited by symbol; the numeric cite went stale twice), which sits at the
    bottom of the loop, so on pass 1 the combiner rewrites ic[-4] and the
    very next backward branch already lands on the folded handler. Pass 2 is still the
    one that matters: it re-seeds every register and enters the block with
    the fold already in place, which is the state a real guest reaches. The
    stores run on both passes and the second overwrites the first.

    `seed` is the flag preset, run LAST among the seeds on every pass so the
    value the cpsr rows read cannot have been left by anything but the loop.
    The #348 rows use `cmp r9,#0x80000000` (0x9 -- every NZCV bit must move
    to reach the zero-exit answer 0x6) and `cmp r9,#1` (0x6, against the
    borrow-exit answer 0x8). `verbose=True` raises the cpu subsystem to
    DEBUG and echoes the setting (the #349 fires rows).

    Five loops -- three matcher probes, each ONE field off the genuine
    sequence, and two more counters for the exit-flag family:

      "genuine"   -- the real thing, counter 0x40, zero exit. DISC on r0/r1
          (the #347 defect: stranded at 0x9100/0x40 where the loop owes
          0x9140/0) and on the exit flags (the #348 defect: seed survived
          where the loop owes Z|C = 0x6).

      "wrongbase" -- `add r5,r5,#32 / subs r1,r1,#32`. DISC on r5 and r1, which
          the fold stranded at 0x9100 and 0x40. r0 is seeded 0x11 and PINNED:
          it is what catches the OPPOSITE error, a handler that now writes r[0]
          and r[1] by name behind a matcher that still accepts any register.

      "wrongcnt"  -- `add r0,r0,#32 / subs r6,r6,#32`. DISC on r6 (0x40 where
          the loop owes 0); r1 is seeded 0x22 and pinned for the same reason.
          r0 is deliberately NOT a row here: the architecture leaves 0x9140 and
          an unguarded fold reading r1 = 0x22 computes 0x9140 too, so it cannot
          attribute anything.

      "borrow"    -- counter 0x30: the loop exits on the subs BORROWING, not
          reaching zero, and owes N alone (0x8) with r0 = 0x9140 and
          r1 = 0xfffffff0. The registers pin #347's closed form on the borrow
          path, which no other row covers; run with both flag seeds, 0x6 to
          discriminate N/Z/C and 0x9 to discriminate V.

      "zero"      -- counter 0: the one input where #347's `(r1 == 0 ||`
          disjunct is load-bearing (an alternative closed form like
          `(r1+31)>>5` fails exactly here). One iteration, borrow exit:
          owes r0 = 0x9120, r1 = 0xffffffe0, flags 0x8.

    The old cpsr CONTROL row (`A cclean2 still fold`) asserted the MISSING
    flags and died with the defect: once #348 lands, the genuine sequence is
    architecturally transparent folded or unfolded, and no register or flag
    can prove the fold still fires. #349's DEBUG-gated marker took over that
    duty -- see the fires/quiet rows.

    Architectural answers are measured, never derived: the identical program
    with the first MCR replaced by a nop, so nothing combines. cr7 is an
    unconditional no-op in this emulator (cpu_arm_coproc.c:209-215), so the
    substitution changes nothing else, and a second neutraliser that instead
    perturbs only the SECOND MCR's opcode2 (0xee070f56, still cr7) returned the
    same values for all three loops on both builds.
    """
    if variant == "genuine":
        seeds = [MOV_R1_64, MOV_R0_9100, MOV_R5_55, MOV_R6_66]
        add, subs = ADD_R0_32, SUBS_R1_32
    elif variant == "wrongbase":
        seeds = [MOV_R1_64, MOV_R5_9100, MOV_R0_11, MOV_R6_66]
        add, subs = ADD_R5_32, SUBS_R1_32
    elif variant == "wrongcnt":
        seeds = [MOV_R6_64, MOV_R0_9100, MOV_R1_22, MOV_R5_55]
        add, subs = ADD_R0_32, SUBS_R6_32
    elif variant == "borrow":
        seeds = [MOV_R1_48, MOV_R0_9100, MOV_R5_55, MOV_R6_66]
        add, subs = ADD_R0_32, SUBS_R1_32
    elif variant == "zero":
        seeds = [MOV_R1_0, MOV_R0_9100, MOV_R5_55, MOV_R6_66]
        add, subs = ADD_R0_32, SUBS_R1_32
    else:
        raise ValueError(variant)
    #  CODE+4 is the outer loop top; the flag seed is the LAST seed so that the
    #  value the flag rows read cannot have been left by anything but the loop.
    #  Program length is identical for every variant and seed (one-for-one
    #  substitutions), so the computed outer branch always resolves to the
    #  same word the old hand-encoded BEQ_BACK19 held.
    prog = [MOV_R8_1] + seeds + [seed] + [
        MCR_CC2_A,              # ic[-4] -- also the branch's target
        MCR_CC2_B,              # ic[-3]
        add,                    # ic[-2]
        subs,                   # ic[-1]
        BHI_BACK6,              # ic[ 0] -- arms the combination check
        MRS_R3_CPSR, STR_R0_R7, STR_R1_R7_4, STR_R5_R7_8, STR_R6_R7_12,
        STR_R3_R7_16, SUBS_R8_R9]
    prog += [outer_beq(len(prog)), NOP]
    cmds = ["r9=0x1", "r7=0x%x" % DEST]
    cmds += ["put w 0x%x, 0xdeadbeef" % (DEST + 4 * i) for i in range(5)]
    cmds += ["put w 0x%x, 0x%08x" % (CODE + 4 * i, iw)
             for i, iw in enumerate(prog)]
    if verbose:
        cmds += verb_cmds()
    cmds += ["breakpoint add 0x%x" % (CODE + 4 * (len(prog) - 1)),
             "pc=0x%x" % CODE, "continue"]
    w, buf = session(cmds, 5)
    if w is None or sw(w[0]) == 0xdeadbeef:
        return None, buf
    return tuple(sw(x) for x in w), buf


def run_und_condfailed(iw):
    """A conditional UDF whose condition is FALSE must do nothing at all.

    This is the strongest reachability witness in the table. The committed
    build's `goto bad` fires during DECODE, before any condition is evaluated,
    so the emulator stops even though the instruction would never have executed
    -- the guest does not have to semantically execute anything to stop the
    machine. Returns (fallthrough_marker, handler_marker): the first must be
    written and the second must NOT be, since no exception may be raised."""
    w, _ = session([
        "r6=5", "r7=3",                      # subs => Z=0, so EQ fails
        "r4=0x%x" % DEST, "r5=0x%x" % (DEST + 4),
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        #  handler at the vector: if it runs, the row fails
        "put w 0x%x, 0x%08x" % (VECT,     MOV_R0_5A),
        "put w 0x%x, 0x%08x" % (VECT + 4, STR_R0_R5),
        "put w 0x%x, 0x%08x" % (CODE,      SUBS_R6_R6_R7),
        "put w 0x%x, 0x%08x" % (CODE + 4,  iw),
        "put w 0x%x, 0x%08x" % (CODE + 8,  MOV_R0_5A),
        "put w 0x%x, 0x%08x" % (CODE + 12, STR_R0_R4),
        "pc=0x%x" % CODE, "step 6"], 2)
    if w is None:
        return None, None
    return sw(w[0]), sw(w[1])


def run_und(iw, at=CODE):
    """Plant a handler at the UND vector; report (mode, lr, marker).

    The marker is the row that proves the handler RAN; mode and lr prove it was
    entered as an exception rather than fallen into.

    `at` places the undefined word at a chosen address. X(und) reconstructs the
    faulting PC as `(pc & 0xfffff000) + arg[0]` with `arg[0] = addr & 0xfff`,
    both hard-coded to a 4KB instruction page. Offset 0 exercises none of that
    arithmetic -- the two halves are zero -- so a row at the LAST slot of a
    page is the one that can actually catch a wrong mask (a panel seat's
    finding)."""
    w, _ = session([
        "r4=0x%x" % DEST, "r5=0x%x" % (DEST + 4), "r6=0x%x" % (DEST + 8),
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0xdeadbeef" % (DEST + 8),
        "put w 0x%x, 0x%08x" % (VECT,      MRS_R3_CPSR),
        "put w 0x%x, 0x%08x" % (VECT + 4,  STR_R3_R4),
        "put w 0x%x, 0x%08x" % (VECT + 8,  STR_LR_R5),
        "put w 0x%x, 0x%08x" % (VECT + 12, MOV_R0_5A),
        "put w 0x%x, 0x%08x" % (VECT + 16, STR_R0_R6),
        "put w 0x%x, 0x%08x" % (at,        iw),
        "pc=0x%x" % at, "step 8"], 3)
    if w is None:
        return None, None, None
    return sw(w[0]), sw(w[1]), sw(w[2])


#  ---- round 78: rotations the decoder used to reject, and MVNS's carry ------
#  Three defects, all measured halting or answering wrongly on the committed
#  build. Each row asserts a VALUE, not survival: round 79's sweep showed that a
#  probe which only asks "did the emulator keep running" cannot tell a repaired
#  instruction from one that merely stopped faulting.
#
#  `uxtah ROR 24` is the discriminating row of the first group. A byte extract
#  gives the same answer under a rotate as under a shift at every encodable
#  amount, so the uxtab rows cannot distinguish the two; at ROR 24 the halfword
#  form wraps rm's low byte into bits 15:8, and copying the byte form's shift
#  would be silently wrong for exactly that one encoding.
#
#  The `movs r0,#0 ROR 4` row is the one that never halted: the old guard
#  exempted an imm8 of zero, so that case shipped with the wrong carry instead
#  of loudly stopping. It is the reason this group is a wrong-answer fix and not
#  only a halt fix.
#
#  The MVNS rows cover all four bands. The decoder rewrites `mvn #imm` into
#  `mov #~imm`, and with S set the template then read the carry off the
#  COMPLEMENT -- inverting the answer everywhere. Two rows would have passed by
#  coincidence, which is why all four bands are here.
STR_R0_R4 = 0xe5840000
MRS_R3_CPSR2 = 0xe10f3000
STR_R3_R4 = 0xe5843000
SUBS_PRESET = 0xe0566007

R78 = [
    #  (name, register presets, instruction, want, carry-in or None, read_flag)
    ("uxtab ROR 8",   ["r1=0", "r2=0x11223344"], 0xe6e10472, 0x33, None, False),
    ("uxtab ROR 16",  ["r1=0", "r2=0x11223344"], 0xe6e10872, 0x22, None, False),
    ("uxtab ROR 24",  ["r1=0", "r2=0x11223344"], 0xe6e10c72, 0x11, None, False),
    ("uxtah ROR 8",   ["r1=0", "r2=0x11223344"], 0xe6f10472, 0x2233, None, False),
    ("uxtah ROR 16",  ["r1=0", "r2=0x11223344"], 0xe6f10872, 0x1122, None, False),
    ("uxtah ROR 24",  ["r1=0", "r2=0x11223344"], 0xe6f10c72, 0x4411, None, False),
    ("uxtab ROR 0",   ["r1=0", "r2=0x11223344"], 0xe6e10072, 0x44, None, False),
    ("rotc movs val", [], 0xe3b00104, 1, None, False),
    ("rotc movs C",   [], 0xe3b00104, 0, 1, True),
    ("rotc zero C",   [], 0xe3b00200, 0, 1, True),
    ("rotc ands C",   ["r1=0xffffffff"], 0xe2110104, 0, 1, True),
    ("rotc orrs val", ["r1=0x10"], 0xe3910104, 0x11, None, False),
    ("rotc bics val", ["r1=0xff"], 0xe3d10104, 0xfe, None, False),
    ("rotc tst C",    ["r1=0xffffffff"], 0xe3110104, 0, 1, True),
    ("rot0 movs C",   [], 0xe3b00004, 1, 1, True),
    ("mvns rot0 C=0", [], 0xe3f00001, 0, 0, True),
    ("mvns rot0 C=1", [], 0xe3f00001, 1, 1, True),
    ("mvns b31=0 C",  [], 0xe3f00fff, 0, 1, True),
    ("mvns b31=1 C",  [], 0xe3f004ff, 1, 0, True),
    ("mvns value",    [], 0xe3f00001, 0xfffffffe, None, False),
    ("mvn S-clear",   [], 0xe3e00001, 0xfffffffe, None, False),
    #  #322: reading the PC as the source operand. Four of the five diff-review
    #  seats named this as the round's one remaining defect and one supplied the
    #  witness, which measured leaving the carry SET where the architecture
    #  clears it. The first fix excluded rn == PC from routing on the stated
    #  grounds that a cold handler could not reconstruct PC+8; that was simply
    #  wrong -- it needs ic, cur_ic_page and cpu->pc, all of which it has.
    #
    #  The rot-0 row is the pin that keeps the fix honest: with no rotation the
    #  carry must be left ALONE, so a handler that just cleared it always would
    #  pass the row above and fail this one.
    #
    #  `pc gt255` goes through the template rather than the new handler, and
    #  `bound 256` sits exactly one above the routing's `imm < 256` test -- a
    #  rotated operand of 0x100 must take the template's >255 arm and clear the
    #  carry from bit 31. Together they pin both sides of the boundary.
    ("rotc pc src C", [], 0xe31f0104, 0, 1, True),
    ("rot0 pc src C", [], 0xe31f0004, 1, 1, True),
    ("rotc pc gt255", [], 0xe31f0fff, 0, 1, True),
    ("rotc bound 256", [], 0xe3b00c01, 0, 1, True),
]


def run78(pre, iw, cin, read_flag):
    """Run one round-78 row; return the observed value, or None."""
    code = [iw, MRS_R3_CPSR2, STR_R3_R4] if read_flag else [iw, STR_R0_R4]
    cmds = list(pre)
    if cin is not None:
        #  Preset the carry with a plain SUBS, never a debugger cpsr write:
        #  the debugger sets cpsr but not the separate `flags` field the
        #  handlers actually read, so a written carry would preset nothing.
        r6, r7 = (1, 0) if cin else (0, 1)
        cmds = ["r6=%d" % r6, "r7=%d" % r7] + cmds
        code = [SUBS_PRESET] + code
    cmds += ["r4=0x%x" % DEST, "put w 0x%x, 0xdeadbeef" % DEST]
    for i, w in enumerate(code):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds += ["pc=0x%x" % CODE, "step %d" % len(code)]
    w, _ = session(cmds, 1)
    if w is None:
        return None
    v = sw(w[0])
    return ((v >> 29) & 1) if read_flag else v


rows = []


def row(name, kind, got, want):
    #  The name column is 30 wide, and that is load-bearing: gate_arm.sh
    #  matches each named row with TWO spaces after the name, to stop a name that
    #  is a prefix of a longer one from matching both. A name as long as the
    #  column gets NO padding and only the format's single separator space, so
    #  its check can never match anything -- the mirror image of the double-count
    #  trap, and it silently made two checks unsatisfiable until a diff-review
    #  seat found them. It was 26 through #347; round 99's review widened it to
    #  30 for headroom after a proposed name came out at exactly 26 characters.
    #  30 leaves >= 2 spaces for every name here; the longest is 24. Keep this
    #  wider than the longest row name plus two if any are added.
    ok = (got == want)
    rows.append(ok)
    print("%-30s %-12s %-12s %s %s"
          % (name,
             ("0x%08x" % got) if isinstance(got, int) else str(got),
             ("0x%08x" % want) if isinstance(want, int) else str(want),
             kind, "ok" if ok else "FAIL"))


def cflag(cpsr):
    return None if cpsr is None else (cpsr >> 29) & 1


def nzcv(cpsr):
    return None if cpsr is None else (cpsr >> 28) & 0xf


#  ---- control -------------------------------------------------------------
#  Nothing below may be believed unless the rig executes guest code at all.
#  This harness has been bitten by a probe that reported a defect off sentinel
#  reads while its guest code had never run.
cpsr, rd = run_flags(SUBS, 5, 3, 1)
control = "OK" if (cpsr is not None and rd == 2) else "DEAD"

print("ARM_FLAGS_CONTROL=%s" % control)
if control != "OK":
    print("ARM_FLAGS_RESULT=0/0")
    sys.exit(0)

#  ---- DISC: the SBC/RSC borrow-in defect ----------------------------------
#  Wrong exactly when a == b with carry-in clear, so all three equal-operand
#  rows below are the defect and the unequal ones are pins. Three different
#  equal values, because a fix that special-cased one constant would pass a
#  single row.
for nm, iw, a, b in [("sbcs eq C=0", SBCS, 5, 5),
                     ("sbcs eq0 C=0", SBCS, 0, 0),
                     ("sbcs eqmax C=0", SBCS, 0xffffffff, 0xffffffff),
                     ("rscs eq C=0", RSCS, 5, 5)]:
    cpsr, rd = run_flags(iw, a, b, 0)
    row(nm + " C", "DISC", cflag(cpsr), 0)
    #  The value was ALWAYS right; assert it so a "fix" that repaired the flag
    #  by breaking the arithmetic cannot pass.
    row(nm + " rd", "PIN", rd, 0xffffffff)

#  ---- PIN: the same two instructions where they were already correct ------
for nm, iw, a, b, cin, wc, wrd in [
        ("sbcs eq C=1",  SBCS, 5, 5, 1, 1, 0x00000000),
        ("sbcs gt C=0",  SBCS, 5, 4, 0, 1, 0x00000000),
        ("sbcs lt C=0",  SBCS, 4, 5, 0, 0, 0xfffffffe),
        ("sbcs lt C=1",  SBCS, 4, 5, 1, 0, 0xffffffff),
        ("rscs gt C=0",  RSCS, 4, 5, 0, 1, 0x00000000),
        ("rscs lt C=0",  RSCS, 5, 4, 0, 0, 0xfffffffe)]:
    cpsr, rd = run_flags(iw, a, b, cin)
    row(nm + " C", "PIN", cflag(cpsr), wc)
    row(nm + " rd", "PIN", rd, wrd)

#  ---- PIN: SUB/RSB/CMP, the three the fix must NOT disturb ----------------
#  These share the rewritten line. `a >= b` and `c32 == c64` agree for them,
#  which is exactly the claim these rows check rather than assume.
for nm, iw, a, b, wc, wrd in [
        ("subs eq", SUBS, 5, 5, 1, 0x00000000),
        ("subs lt", SUBS, 3, 5, 0, 0xfffffffe),
        ("subs gt", SUBS, 5, 3, 1, 0x00000002),
        ("subs zerominus", SUBS, 0, 1, 0, 0xffffffff),
        ("rsbs gt", RSBS, 3, 5, 1, 0x00000002),
        ("rsbs lt", RSBS, 5, 3, 0, 0xfffffffe)]:
    cpsr, rd = run_flags(iw, a, b, 1)
    row(nm + " C", "PIN", cflag(cpsr), wc)
    row(nm + " rd", "PIN", rd, wrd)

#  The A__PC template variant compiles its OWN copy of the changed line, and it
#  is the one operand path that is not plainly a 32-bit register read: when Rn
#  is PC the template recomputes the operand as page_base + slot*4 + 8 in 64-bit
#  arithmetic, which passes 2^32 for the last two instruction slots of the
#  address space. Three panel seats raised it and one classified it as a
#  regression this round would otherwise introduce, so #311 truncates that
#  operand back to 32 bits -- correct on its own terms, since ARM's PC is 32
#  bits and reading it must wrap.
#
#  These two rows CANNOT reach the top-of-space case: it needs RAM mapped at
#  0xfffff000 and this machine has not got any. What they do prove is that the
#  truncation left the reachable A__PC path alone, which is the part that is
#  measurable. The corner itself is reasoned, not measured, and the round notes
#  say so rather than implying the gate covers it.
#  The instruction sits at CODE+4, so ARM's PC reads CODE+12 and rd = CODE+8.
cpsr, rd = run_flags(SUBS_PC_4, 0, 0, 1)
row("subs rn=pc rd", "PIN", rd, CODE + 8)
row("subs rn=pc C", "PIN", cflag(cpsr), 1)

#  CMP writes no rd, so only its flags are meaningful. Full NZCV, because CMP
#  exists only for its flags and a carry-only check would miss a clobbered Z.
for nm, a, b, wnzcv in [("cmp eq", 5, 5, 0x6),        # Z=1 C=1
                        ("cmp lt", 3, 5, 0x8),        # N=1
                        ("cmp gt", 5, 3, 0x2)]:       # C=1
    cpsr, rd = run_flags(CMPS, a, b, 1)
    row(nm + " NZCV", "PIN", nzcv(cpsr), wnzcv)

#  ---- PIN: the ADD side of the same #if, which must stay on c32 != c64 ----
for nm, iw, a, b, cin, wc in [
        ("adds carry-out", ADDS, 0xffffffff, 1, 1, 1),
        ("adds no-carry",  ADDS, 1, 1, 1, 0),
        ("adcs carry-out", ADCS, 0xffffffff, 0, 1, 1),
        ("adcs no-carry",  ADCS, 1, 1, 0, 0)]:
    cpsr, rd = run_flags(iw, a, b, cin)
    row(nm + " C", "PIN", cflag(cpsr), wc)

#  ---- DISC: #313, ADC is the one opcode with no V formula -----------------
#  ADC appears in the OUTER #if that clears and recomputes V, but matches
#  neither inner arm (ADD||CMN, nor SUB||RSB||CMP||RSC||SBC), so `v` stays 0
#  and ADCS could only ever CLEAR V. Found by a panel seat reading the #if
#  nesting, then reproduced here. The paired ADDS rows are what make these
#  rows a statement about ADC specifically rather than about V in general:
#  the identical overflow through ADDS was already correct.
for nm, iw, a, b, cin, wv, kind in [
        ("adcs V pos-ovf",  ADCS, 0x7fffffff, 0, 1, 1, "DISC"),
        ("adcs V pos-ovf2", ADCS, 0x7ffffffe, 1, 1, 1, "DISC"),
        ("adcs V neg-ovf",  ADCS, 0x80000000, 0xffffffff, 0, 1, "DISC"),
        ("adcs V none",     ADCS, 1, 1, 1, 0, "PIN"),
        ("adds V pos-ovf",  ADDS, 0x7fffffff, 1, 1, 1, "PIN"),
        ("adds V none",     ADDS, 1, 1, 1, 0, "PIN"),
        ("sbcs V ovf",      SBCS, 0x80000000, 1, 0, 1, "PIN")]:
    cpsr, rd = run_flags(iw, a, b, cin)
    row(nm, kind, None if cpsr is None else (cpsr >> 28) & 1, wv)

#  ---- DISC: permanently-undefined routing ---------------------------------
#  Committed: the emulator STOPS, so every witness keeps its sentinel. The
#  marker proves the handler ran; the mode and lr prove it was reached as an
#  exception and not merely branched to.
for nm, iw, at in [("udf", UDF, CODE),
                   ("udf gdb-form", UDF_GDB, CODE),
                   ("udf page-end", UDF, PAGE_END)]:
    mode, lr, marker = run_und(iw, at)
    row(nm + " handler ran", "DISC", marker, 0x0000005a)
    row(nm + " UND32 mode", "DISC",
        None if mode is None else mode & 0x1f, ARM_MODE_UND32)
    row(nm + " lr=pc+4", "DISC", lr, at + 4)

#  A conditional UDF whose condition FAILS. The committed build fails this
#  because `goto bad` runs at DECODE time -- the guest never had to execute the
#  instruction for the emulator to stop, which is the strongest statement of
#  reachability in this table.
#
#  The two halves are ONE row on purpose. Asserting "the handler did not run"
#  separately would pass on the committed build for the wrong reason: nothing
#  ran at all there, so the sentinel survives and a dead emulator scores a
#  point. Only the conjunction -- execution continued AND no exception was
#  raised -- distinguishes correct silence from a stopped machine.
fall, handler = run_und_condfailed(UDF_EQ)
row("udf cond-failed nop", "DISC",
    "ran=0x%08x handler=0x%08x" % (fall, handler)
    if fall is not None else "dead",
    "ran=0x0000005a handler=0xdeadbeef")

for name, pre, iw, want, cin, rf in R78:
    got = run78(pre, iw, cin, rf)
    row(name, "PIN" if name in ("uxtab ROR 0", "rot0 movs C", "mvn S-clear",
                                "rot0 pc src C", "rotc pc gt255",
                                "rotc bound 256") else "DISC", got, want)


#  ---------------------------------------------------------------------------
#  #328: THUMB. Everything above drives ARM-mode encodings; the Thumb
#  interpreter is a completely separate implementation (cpu_arm.c,
#  arm_cpu_interpret_thumb_SLOW) and #311 never touched it.
#
#  Thumb is entered ARCHITECTURALLY: an ARM `bx` to an ODD address sets
#  ARM_FLAG_T and leaves the low bit in pc, and cpu_dyntrans.c dispatches to
#  the interpreter on the T bit.
#
#  An earlier draft of this comment gave the wrong reason for that choice,
#  claiming a debugger `cpsr=` write "would preset nothing" the way it does for
#  the NZCV carry-in above. That is FALSE and was corrected by a review seat:
#  cpu_dyntrans.c reads `cpu->cd.arm.cpsr & ARM_FLAG_T` directly, so a debugger
#  write does set T. The mirror problem is real but applies only to NZCV. The
#  actual reason to use `bx` is that the interpreter demands BOTH conditions --
#  `if (!(cpu->pc & 1) || !(cpsr & ARM_FLAG_T))` -- so setting T alone lands on
#  an even pc and refuses to run, and `bx` is the one operation that
#  establishes both together, exactly as a guest would.
#
#  `mrs` is ARM-only in Thumb-1, so each row returns to ARM with a second `bx`
#  before publishing; `bx` does not touch the flags, so the round trip is
#  transparent to what is being measured.
#
#  Four near-identical blocks each computed `old + b` in 64 bits -- with b
#  NEGATED first on the subtract arms -- and read every flag off that value.
#  Three of the four flags were wrong:
#    Z  from `result == 0` -- a subtract of equal NONZERO operands carries out
#       of bit 31, so Z stayed CLEAR while rd was 0, and `subs; bne` never
#       terminated. (0 - 0 was the one subtract that happened to work: nothing
#       carries out of it, so Z was set -- though C was still wrong there.) The
#       same line also missed Z for an ADD that wrapped to zero.
#    C  from bit 32 -- with b == 0 the addend is (uint32_t)(-0) == 0, nothing
#       carries out, so `cmp r0,#0` reported a borrow that never happened.
#    V  from the sign of the NEGATED subtrahend, which breaks at exactly
#       0x80000000 because that value is its own negation. Wrong in BOTH
#       directions, and x - x claimed overflow.
#  N was always right -- it cast to int32_t first, which is the shape the rest
#  should have had.
#
#  Every row publishes rd as well as the flags: these are FLAG defects, the
#  value was already correct, and a row checking only the flag could not tell a
#  fixed flag from a broken result.
THUMB_AT = 0x8100
THUMB_RET = 0x8200
BX_R6 = 0xE12FFF16              # arm:   bx r6
SUBS_R8_R8_R9 = 0xE0588009      # arm:   subs r8,r8,r9  (the carry preset)
T_BX_R7 = 0x4738                # thumb: bx r7


def t_reg(op, rd, rs, rn):      # ADDS/SUBS rd,rs,rn  (format 2)
    return op | ((rn & 7) << 6) | ((rs & 7) << 3) | (rd & 7)


def t_imm8(op, rd, imm):        # CMP/SUBS rd,#imm8   (format 3)
    return op | ((rd & 7) << 8) | (imm & 0xff)


def t_reg3(op, rd, rs, imm3):   # ADDS/SUBS rd,rs,#imm3 (format 2, I set)
    return op | ((imm3 & 7) << 6) | ((rs & 7) << 3) | (rd & 7)


def t_cmp_reg(rd, rs):          # CMP rd,rs           (format 4, op 1010)
    return 0x4280 | ((rs & 7) << 3) | (rd & 7)


def run_thumb(tiw, r0=0, r1=0, r2=0, r3=0, cin=None, pub=0):
    """One Thumb instruction, entered by bx; returns (cpsr, published reg).

    `cin` presets the CARRY, and it is not optional decoration. Without it the
    machine starts with C clear, which makes two whole contracts unmeasurable:
    "LSR #0 must CLEAR C for a positive operand" and "LSL #0 must LEAVE C
    alone" both pass vacuously against C=0. The preset is the same real SUBS
    gate 14 uses in ARM mode -- never a debugger cpsr write, which reaches
    cpsr but not the `flags` field the handlers read -- and it runs BEFORE the
    `bx`, which is safe because `bx` touches no flags.

    `pub` selects which register is published. Every row used to write and read
    r0, so a handler that read r0 instead of rd would have been invisible;
    that is the shadow of the very defect #329 fixes in the ASR block, where
    the flags came from a register chosen by the shift amount.
    """
    pre = []
    lead = 0
    if cin is not None:
        #  r8/r9 as the SUBS operands so r0-r3 stay free for the row.
        a, b = (1, 0) if cin else (0, 1)     # 1-0 => no borrow => C=1
        pre = ["r8=0x%x" % a, "r9=0x%x" % b,
               "put w 0x%x, 0x%08x" % (CODE, SUBS_R8_R8_R9)]
        lead = 1
    str_pub = STR_R0_R5 if pub == 0 else (STR_R0_R5 | (pub << 12))
    w, _ = session(pre + [
        "r0=0x%x" % r0, "r1=0x%x" % r1, "r2=0x%x" % r2, "r3=0x%x" % r3,
        "r4=0x%x" % DEST, "r5=0x%x" % (DEST + 4),
        "r6=0x%x" % (THUMB_AT | 1), "r7=0x%x" % THUMB_RET,
        "put w 0x%x, 0xdeadbeef" % DEST,
        "put w 0x%x, 0xdeadbeef" % (DEST + 4),
        "put w 0x%x, 0x%08x" % (CODE + 4 * lead, BX_R6),
        #  two Thumb halfwords per word, low halfword first
        "put w 0x%x, 0x%08x" % (THUMB_AT, (T_BX_R7 << 16) | tiw),
        "put w 0x%x, 0x%08x" % (THUMB_RET,     MRS_R3_CPSR),
        "put w 0x%x, 0x%08x" % (THUMB_RET + 4, STR_R3_R4),
        "put w 0x%x, 0x%08x" % (THUMB_RET + 8, str_pub),
        "pc=0x%x" % CODE, "step %d" % (6 + lead)], 2)
    if w is None:
        return None, None
    return sw(w[0]), sw(w[1])


def thumb_nzcv(cpsr):
    """Flags as a string. NOT named nzcv(): there is already an nzcv() above
    that returns an int, and defining a second one here SHADOWED it. Nothing
    broke only because this file executes top to bottom and the first one has
    finished being used by the time this line runs -- which is a latent trap,
    not a design. A review seat spotted it."""
    if cpsr is None:
        return None
    return "N%d Z%d C%d V%d" % ((cpsr >> 31) & 1, (cpsr >> 30) & 1,
                                (cpsr >> 29) & 1, (cpsr >> 28) & 1)


T_ADD, T_SUB = 0x1800, 0x1A00           # format 2, register operand
T_ADD3, T_SUB3 = 0x1C00, 0x1E00         # format 2, imm3 operand (I bit set)
T_CMPI, T_SUBI, T_ADDI = 0x2800, 0x3800, 0x3000     # format 3, imm8

#  name, word, r0, r1, r2, want rd, want NZCV, class
THUMB_ROWS = [
    #  controls -- if these fail the rig never reached Thumb and no other
    #  Thumb row here may be believed. The borrow control is the one that
    #  proves the rig can still tell a REAL borrow from the broken ones.
    ("T ctrl ADDS 2+3",    t_reg(T_ADD, 0, 1, 2), 0, 2, 3, 5,
     "N0 Z0 C0 V0", "PIN"),
    ("T ctrl SUBS 5-3",    t_reg(T_SUB, 0, 1, 2), 0, 5, 3, 2,
     "N0 Z0 C1 V0", "PIN"),
    ("T ctrl SUBS borrow", t_reg(T_SUB, 0, 1, 2), 0, 3, 5, 0xfffffffe,
     "N1 Z0 C0 V0", "PIN"),

    #  Z, all four blocks, plus the ADD that wraps to zero.
    ("T Z subs equal",     t_reg(T_SUB, 0, 1, 2), 0, 5, 5, 0,
     "N0 Z1 C1 V0", "DISC"),
    ("T Z cmp imm equal",  t_imm8(T_CMPI, 0, 5),  5, 0, 0, 5,
     "N0 Z1 C1 V0", "DISC"),
    ("T Z subs imm equal", t_imm8(T_SUBI, 0, 5),  5, 0, 0, 0,
     "N0 Z1 C1 V0", "DISC"),
    ("T Z cmp reg equal",  t_cmp_reg(0, 1),       5, 5, 0, 5,
     "N0 Z1 C1 V0", "DISC"),
    ("T Z adds wrap",      t_reg(T_ADD, 0, 1, 2), 0, 1, 0xffffffff, 0,
     "N0 Z1 C1 V0", "DISC"),

    #  C, all four blocks: a subtraction of ZERO does not borrow.
    ("T C subs zero",      t_reg(T_SUB, 0, 1, 2), 0, 5, 0, 5,
     "N0 Z0 C1 V0", "DISC"),
    ("T C cmp imm 0",      t_imm8(T_CMPI, 0, 0),  5, 0, 0, 5,
     "N0 Z0 C1 V0", "DISC"),
    ("T C subs imm 0",     t_imm8(T_SUBI, 0, 0),  5, 0, 0, 5,
     "N0 Z0 C1 V0", "DISC"),
    ("T C cmp reg zero",   t_cmp_reg(0, 1),       5, 0, 0, 5,
     "N0 Z0 C1 V0", "DISC"),

    #  V at the one subtrahend where negation cannot work. The middle row is
    #  the one that proves the defect ran in BOTH directions, and the third
    #  shows Z and V failing together on the same instruction.
    ("T V 0-INT_MIN",      t_cmp_reg(0, 1), 0, 0x80000000, 0, 0,
     "N1 Z0 C0 V1", "DISC"),
    ("T V -1-INT_MIN",     t_cmp_reg(0, 1), 0xffffffff, 0x80000000, 0,
     0xffffffff, "N0 Z0 C1 V0", "DISC"),
    ("T V INT_MIN-same",   t_cmp_reg(0, 1), 0x80000000, 0x80000000, 0,
     0x80000000, "N0 Z1 C1 V0", "DISC"),

    #  rd == rm, the aliasing case: the subtrahend must be captured BEFORE the
    #  result is stored, because `subs r0,r1,r0` overwrites it.
    #
    #  Read the operands here carefully, because the FIRST version of this row
    #  used 5 - 5 and a review seat showed it proved nothing about aliasing:
    #  for result = a - b, `a >= result` and `a >= b` have the SAME truth value
    #  at every operand, so no choice of values can catch a late re-read used
    #  by the CARRY formula. 0 - 1 is used instead because it catches a late
    #  re-read used by the OVERFLOW formula: with b captured (1) V is 0, while
    #  with b re-read after the store (0xffffffff) V comes out 1.
    ("T alias subs rd==rm", t_reg(T_SUB, 0, 1, 0), 1, 0, 0, 0xffffffff,
     "N1 Z0 C0 V0", "DISC"),

    #  The IMMEDIATE arms. Without these the `isImm3` operand selection and the
    #  ADD-side `isSub` polarity are unpinned: a regression that read the
    #  register instead of the imm3 field, or inverted isSub only where it
    #  shows on an ADD, would pass every row above. A review seat found the
    #  hole after the fix was already green.
    ("T Z adds imm8 wrap", t_imm8(T_ADDI, 0, 1), 0xffffffff, 0, 0, 0,
     "N0 Z1 C1 V0", "DISC"),
    ("T Z adds imm3 wrap", t_reg3(T_ADD3, 0, 1, 1), 0, 0xffffffff, 0, 0,
     "N0 Z1 C1 V0", "DISC"),
    ("T C subs imm3 zero", t_reg3(T_SUB3, 0, 1, 0), 0, 5, 0, 5,
     "N0 Z0 C1 V0", "DISC"),

    #  Four more the after-pass asked for, each closing a way a wrong
    #  implementation could still have passed everything above:
    #    - the V rows were all register CMP, so a SUBS with the same operand
    #      pins the OTHER register form,
    #    - no ADD row wanted V=1, so an add that always cleared V passed,
    #    - 0 - 0 is the one subtract that sets Z on the OLD code (nothing
    #      carries out), which makes it the case where C alone discriminates.
    ("T V subs INT_MIN",   t_reg(T_SUB, 0, 1, 2), 0, 0, 0x80000000,
     0x80000000, "N1 Z0 C0 V1", "DISC"),
    ("T V adds overflow",  t_reg(T_ADD, 0, 1, 2), 0, 0x7fffffff, 1,
     0x80000000, "N1 Z0 C0 V1", "PIN"),
    ("T C subs 0-0",       t_reg(T_SUB, 0, 1, 2), 0, 0, 0, 0,
     "N0 Z1 C1 V0", "DISC"),
    ("T V adds INT_MIN x2", t_reg(T_ADD, 0, 1, 2), 0, 0x80000000, 0x80000000,
     0, "N0 Z1 C1 V1", "DISC"),
]

for nm, tiw, a0, a1, a2, want_rd, want_f, cls in THUMB_ROWS:
    cpsr, rd = run_thumb(tiw, a0, a1, a2)
    row(nm, cls, thumb_nzcv(cpsr), want_f)
    row(nm + " rd", cls, rd, want_rd)


#  ---------------------------------------------------------------------------
#  #329: the THUMB SHIFT paths. Three more flag defects in the same function
#  #328 fixed, found by that round's completeness sweep.
#
#    1. ASR-immediate read Z and N from r[rd8] while writing r[rd]. In the
#       shift-immediate format (000 op imm5 Rs Rd) rd8 is bits 10:8 -- the top
#       three bits of imm5 -- so `asrs r0,r1,#12` took its flags from r3, a
#       register the instruction does not name. LSL and LSR never had this.
#       NOTE the witness needs imm5 >= 4: below that rd8 is 0, which for a row
#       writing r0 is accidentally the right register.
#    2. RORS ORed Z and N in without clearing first, so a stale Z survived a
#       nonzero rotate and a stale N survived a positive one.
#    3. LSR #0 and ASR #0 encode SHIFT BY 32, not shift by zero: LSR gives 0,
#       ASR gives a sign fill, and both write C from bit 31 of the operand.
#       They executed as no-ops with C untouched. LSL #0 IS a real no-op and
#       must stay one -- it is the control.
#
#  Half of contract 3 was unmeasurable until this round gave run_thumb a carry
#  preset: with C starting clear, "LSR #0 CLEARS C for a positive operand" and
#  "LSL #0 LEAVES C alone" both pass against a build that never touches C. The
#  rows below preset C=1 precisely so those two can fail.
T_LSL_I, T_LSR_I, T_ASR_I = 0x0000, 0x0800, 0x1000


def t_shift(op, rd, rs, imm5):
    return op | ((imm5 & 31) << 6) | ((rs & 7) << 3) | (rd & 7)


def t_ror(rd, rs):
    return 0x41C0 | ((rs & 7) << 3) | (rd & 7)


#  name, word, r0, r1, r2, r3, carry-in, publish, want reg, want NZCV, class
SHIFT_ROWS = [
    #  LSL #0 is the control in both directions: value through, C preserved.
    ("T LSL #0 keeps C1", t_shift(T_LSL_I, 0, 1, 0), 0, 0x80000000, 0, 0,
     1, 0, 0x80000000, "N1 Z0 C1 V0", "PIN"),
    ("T LSL #0 keeps C0", t_shift(T_LSL_I, 0, 1, 0), 0, 0x80000000, 0, 0,
     0, 0, 0x80000000, "N1 Z0 C0 V0", "PIN"),

    #  1. flags from the result, not from a register named by the shift count.
    ("T ASR #12 flags reg", t_shift(T_ASR_I, 0, 1, 12), 0, 0x80000000, 0, 0,
     0, 0, 0xfff80000, "N1 Z0 C0 V0", "DISC"),

    #  2. RORS must clear both. Z stale after an equal compare, N stale after
    #     a negative one -- the rotate results are nonzero and positive.
    ("T RORS clears Z", t_ror(0, 1), 0x12345678, 4, 0, 0,
     1, 0, 0x81234567, "N1 Z0 C1 V0", "DISC"),
    ("T RORS clears N", t_ror(0, 1), 0x00000010, 4, 0, 0,
     1, 0, 0x00000001, "N0 Z0 C0 V0", "DISC"),

    #  3. shift-by-32, both operand signs. The POSITIVE rows are the ones the
    #     carry preset made possible: C must be driven to 0, not left at 1.
    ("T LSR #0 neg", t_shift(T_LSR_I, 0, 1, 0), 0, 0x80000000, 0, 0,
     0, 0, 0x00000000, "N0 Z1 C1 V0", "DISC"),
    ("T LSR #0 pos", t_shift(T_LSR_I, 0, 1, 0), 0, 0x7fffffff, 0, 0,
     1, 0, 0x00000000, "N0 Z1 C0 V0", "DISC"),
    ("T ASR #0 neg", t_shift(T_ASR_I, 0, 1, 0), 0, 0x80000000, 0, 0,
     0, 0, 0xffffffff, "N1 Z0 C1 V0", "DISC"),
    ("T ASR #0 pos", t_shift(T_ASR_I, 0, 1, 0), 0, 0x7fffffff, 0, 0,
     1, 0, 0x00000000, "N0 Z1 C0 V0", "DISC"),

    #  A row whose destination is NOT r0, published from r1. Every other row
    #  here writes and reads r0, so a handler reading r0 instead of rd would
    #  be invisible -- which is the shadow of defect 1 itself.
    ("T LSR rd!=0", t_shift(T_LSR_I, 1, 2, 4), 0xdeadbeef, 0, 0x80000000, 0,
     0, 1, 0x08000000, "N0 Z0 C0 V0", "DISC"),
]

for nm, tiw, a0, a1, a2, a3, cin, pub, want_r, want_f, cls in SHIFT_ROWS:
    cpsr, rv = run_thumb(tiw, a0, a1, a2, a3, cin=cin, pub=pub)
    row(nm, cls, thumb_nzcv(cpsr), want_f)
    row(nm + " rd", cls, rv, want_r)


#  #340: the instruction COMBINER changes observable flags.
#
#  A data-processing immediate with S set updates C from the shifter carry-out;
#  this tree approximates that as "encoded immediate > 255 means it was rotated,
#  so C := its bit 31" (cpu_arm_instr_dpi.c:121-140). The standalone teqs/tsts
#  do it. The *_samepage handlers that a teq/tst-followed-by-branch folds into
#  do not touch C at all, and the teqs combiner has NO operand guard while the
#  tsts one guards only bit 31 -- which is about N (with the top bit clear,
#  a & b cannot be negative), not about C.
#
#  0x0000FF00 is `0xFF ror 24`: rotated, > 255, bit 31 CLEAR, so the owed answer
#  is C := 0. C is preset to 1 so "did nothing" is distinguishable from
#  "cleared correctly".
#
#  The STANDALONE rows are the control and are what attributes a difference to
#  the COMBINER rather than to the instruction: identical encoding, identical
#  operands, no following branch, and they must read C0 on both builds.
TEQ_ROT = teq_imm(12, 0xFF)     # teq r1, #0x0000FF00
TST_ROT = tst_imm(12, 0xFF)     # tst r1, #0x0000FF00

COMBINE_ROWS = [
    ("A teq rot C combined", run_combined(TEQ_ROT, 0x00000001, 1), 0, "DISC"),
    ("A tst rot C combined", run_combined(TST_ROT, 0x0000FF00, 1), 0, "DISC"),
    ("A teq rot C standalone", run_flags(TEQ_ROT, 0x00000001, 0, 1)[0], 0,
     "PIN"),
    ("A tst rot C standalone", run_flags(TST_ROT, 0x0000FF00, 0, 1)[0], 0,
     "PIN"),
    #  unrotated (<= 255): C is PRESERVED by the ISA on both paths. Catches a
    #  fix that starts clobbering C where it must be left alone.
    ("A teq flat C preserved", run_combined(teq_imm(0, 0x01), 0x00000010, 1),
     1, "PIN"),
]
for nm, cpsr, want_c, cls in COMBINE_ROWS:
    row(nm, cls, "C%d" % cflag(cpsr) if cpsr is not None else "dead",
        "C%d" % want_c)

#  #342: the XOR-swap fold had no a != b guard.
#
#  DISC: three  each ZERO r0; X(xchg) exchanges r0 with itself and
#  leaves it alone. 0x5a is the row own proof that the fold happened, since no
#  standalone EOR triplet can leave a nonzero value.
#
#  PIN: the distinct-register swap, in the shape the matcher actually accepts
#  (Rm == Rd). It exercises the FOLDED handler on pass 2 and pins that the swap
#  it performs is correct -- so a broken X(xchg) fails here -- but it cannot by
#  itself distinguish folded-and-correct from not-folded-and-correct, which is
#  exactly why it is a PIN and not a second discriminator.
XCHG_ROWS = []
_d = run_xchg(True)
XCHG_ROWS.append(("A xchg same-reg zeroes", _d[0] if _d else None,
                  0x00000000, "DISC"))
XCHG_ROWS.append(("A xchg same-reg r1 pin", _d[1] if _d else None,
                  0x000000a5, "PIN"))
_s = run_xchg(False)
XCHG_ROWS.append(("A xchg swap r0", _s[0] if _s else None, 0x000000a5, "PIN"))
XCHG_ROWS.append(("A xchg swap r1", _s[1] if _s else None, 0x0000005a, "PIN"))
for nm, got, want, cls in XCHG_ROWS:
    row(nm, cls, "%08x" % got if got is not None else "dead", "%08x" % want)

#  #345: the cache-clean fold clobbered r0/r1 for a loop that used neither.
#  #346: and it fired on any post-index immediate, so a 4-byte stride advanced
#  the base by 32. #348 made the fold write the loop's exit flags; #349 gave
#  it a DEBUG-gated fold-fired marker; #350 made a non-multiple counter fall
#  back to the real loop instead of terminating a loop that architecturally
#  never exits. See run_cacheclean / run_cc_nonmult for what each variant
#  isolates. "still folds" (stale r2) remains a fold detector independent of
#  the marker, because the skipped load is deliberately unfixed.
_cc, _ = run_cacheclean("wrongregs")
_cg, _ = run_cacheclean("genuine")
_ci, _ = run_cacheclean("imm4")
_cd, _ = run_cacheclean("wrongdest")
#  The #348 rows ride the 0x40 counter -- at 0x20 a fix that skipped the r1
#  preload would be invisible (see the docstring). The quiet row shares the
#  default-verbosity session: the marker must be absent from a plain run.
#  NB debugmsg's verbosity gate is bypassed under single_step, so the quiet
#  rows are valid only for breakpoint+continue sessions like these -- do not
#  rewrite them to drive the loop with `step`.
_cf, _cfbuf = run_cacheclean("genuine40", seed=CMP_R9_HI)
_, _cvbuf = run_cacheclean("genuine40", seed=CMP_R9_HI, verbose=True)
_, _cwbuf = run_cacheclean("wrongregs", verbose=True)
_cn = run_cc_nonmult()
for _nm, _got, _want, _cls in (
        ("A cacheclean r0 intact", _cc[0] if _cc else None, 0x11, "DISC"),
        ("A cacheclean r1 intact", _cc[1] if _cc else None, 0x22, "DISC"),
        ("A cacheclean still folds", _cg[2] if _cg else None, 0x77, "PIN"),
        ("A cacheclean fold r0", _cg[0] if _cg else None, 0x9120, "PIN"),
        ("A cacheclean imm4 r0", _ci[0] if _ci else None, 0x9104, "DISC"),
        ("A cacheclean imm4 r2", _ci[2] if _ci else None, CC_MEM, "DISC"),
        ("A cacheclean wrong Rd", _cd[3] if _cd else None, CC_MEM, "DISC"),
        ("A cacheclean flags", (_cf[4] & 0xf0000000) if _cf else None,
         0x60000000, "DISC"),
        ("A cacheclean fold r1", _cf[1] if _cf else None, 0x00000000, "PIN")):
    row(_nm, _cls, "%08x" % _got if _got is not None else "dead",
        "%08x" % _want)
#  The #350 verdict is a state word, not a register value: "fold" = the fold
#  consumed the 0x21 counter (prompt reached unaided, r0 odd), "live" = the
#  guard held and the architectural infinite loop was observed running
#  (^C-interrupted; r1 mod 32 == 1 and r0 even, the loop's two invariants).
row("A cacheclean nonmult", "DISC", _cn if _cn else "dead", "live")
#  Marker rows. The fires rows demand BOTH the marker and the echoed
#  "3: DEBUG" -- a session whose verbosity silently failed to rise reports
#  no-verb and fails, instead of passing an absence check for the wrong
#  reason. fires ctrl proves matcher selectivity under the SAME raised
#  verbosity whose effectiveness the fires row just proved.
_f1 = ("yes" if marker_count(_cvbuf, MARK1) >= 1 else "no") \
    if verb_took(_cvbuf) else "no-verb"
_x1 = ("absent" if marker_count(_cwbuf, MARK1) == 0 else "present") \
    if verb_took(_cwbuf) else "no-verb"
row("A cacheclean quiet", "PIN", "%d" % marker_count(_cfbuf, MARK1), "0")
row("A cacheclean fires", "DISC", _f1, "yes")
row("A cacheclean fires ctrl", "PIN", _x1, "absent")
#  #350's r1 == 0 arm: no register or flag can assert the honest n -- a
#  formula reverted to `r1 >> 5` reproduces every stored value -- so the
#  count is read off the #349 marker itself (see run_cc_zero_n).
_zn = run_cc_zero_n()
row("A cacheclean zero n", "DISC", _zn if _zn else "dead", "134217728")

#  #347: the SECOND cache-clean fold had BOTH halves wrong -- unguarded
#  registers AND no register update whatsoever. #348 added the exit flags by
#  delegating the final subs to the real dpi handler (zero exit owes Z|C,
#  borrow exit owes N; V is structurally 0, since before_last lies in
#  [0, 0x20] for every uint32 counter). The old `A cclean2 still fold`
#  control row ASSERTED the missing flags and died with the defect it was
#  built on -- #349's marker rows below are its replacement, decided and
#  re-authored in the same change, as the OUTSTANDING_BUGS entry required.
_g2, _g2buf = run_cc2("genuine", seed=CMP_R9_HI)
_b2, _ = run_cc2("wrongbase")
_n2, _ = run_cc2("wrongcnt")
_t2, _ = run_cc2("borrow", seed=CMP_R9_1)
_tv, _ = run_cc2("borrow", seed=CMP_R9_HI)
_z2, _ = run_cc2("zero", seed=CMP_R9_1)
_, _f2buf = run_cc2("genuine", seed=CMP_R9_HI, verbose=True)
_, _w2buf = run_cc2("wrongbase", verbose=True)
for _nm, _got, _want, _cls in (
        ("A cclean2 fold r0", _g2[0] if _g2 else None, 0x9140, "DISC"),
        ("A cclean2 fold r1", _g2[1] if _g2 else None, 0x00000000, "DISC"),
        ("A cclean2 flags", (_g2[4] & 0xf0000000) if _g2 else None,
         0x60000000, "DISC"),
        ("A cclean2 base r5", _b2[2] if _b2 else None, 0x9140, "DISC"),
        ("A cclean2 base r1", _b2[1] if _b2 else None, 0x00000000, "DISC"),
        ("A cclean2 base r0", _b2[0] if _b2 else None, 0x11, "PIN"),
        ("A cclean2 cnt r6", _n2[3] if _n2 else None, 0x00000000, "DISC"),
        ("A cclean2 cnt r1", _n2[1] if _n2 else None, 0x22, "PIN"),
        ("A cclean2 tail flags", (_t2[4] & 0xf0000000) if _t2 else None,
         0x80000000, "DISC"),
        ("A cclean2 tail r0", _t2[0] if _t2 else None, 0x9140, "PIN"),
        ("A cclean2 tail r1", _t2[1] if _t2 else None, 0xfffffff0, "PIN"),
        ("A cclean2 tail V", (_tv[4] & 0xf0000000) if _tv else None,
         0x80000000, "DISC"),
        ("A cclean2 zero flags", (_z2[4] & 0xf0000000) if _z2 else None,
         0x80000000, "DISC"),
        ("A cclean2 zero r0", _z2[0] if _z2 else None, 0x9120, "PIN"),
        ("A cclean2 zero r1", _z2[1] if _z2 else None, 0xffffffe0, "PIN")):
    row(_nm, _cls, "%08x" % _got if _got is not None else "dead",
        "%08x" % _want)
_f2y = ("yes" if marker_count(_f2buf, MARK2) >= 1 else "no") \
    if verb_took(_f2buf) else "no-verb"
_x2 = ("absent" if marker_count(_w2buf, MARK2) == 0 else "present") \
    if verb_took(_w2buf) else "no-verb"
row("A cclean2 quiet", "PIN", "%d" % marker_count(_g2buf, MARK2), "0")
row("A cclean2 fires", "DISC", _f2y, "yes")
row("A cclean2 fires ctrl", "PIN", _x2, "absent")

print("ARM_FLAGS_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
