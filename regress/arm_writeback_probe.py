#!/usr/bin/env python3
"""Round 104 gate candidate: the ARM load/store base writeback (#19).

The template `cpu_arm_instr_loadstore.c` computes one address, MASKS it for
alignment, and then writes the base register back from the masked value. ARM ARM
DDI 0100I computes the writeback from the UNMASKED Rn:

  A5.2.8 post-indexed:  address = Rn ;  Rn = Rn + offset_12
  A5.2.5 pre-indexed:   address = Rn + offset_12 ;  Rn = address
  A2-43: the truncation lives inside Memory[<address>,<size>], i.e. on the
         address sent to memory -- never on the register.

There are EXACTLY FOUR writeback sites in the single-register path, established
by enumeration: `reg(ic->arg[0]) =` at :213 and :216 (general path) and :338 and
:342 (fast path). `A__NAME_PC` and every conditional variant (`__eq`, `__ne`,
...) merely CALL `A__NAME`; two review seats suspected the PC special case was a
third copy and it is not. A review seat enumerated the instantiations from
generate_arm_loadstore.c -- 8 p/u/w files x (8 mode-2 + 12 mode-3) = 160 handler
families -- all funnelling through those four statements.

WHICH SITE EACH ROW REACHES, which is the point of the row set
--------------------------------------------------------------
The fast path only runs once the page is in the translation array, so a
SINGLE-execution row measures the GENERAL path and nothing else. That means the
obvious one-instruction rows leave two of the four sites uncovered. A review seat
caught this; the row set is built around it:

  :216 general post-index  -- rows B, F, G, and iteration 1 of A/A2/S/R
  :342 fast    post-index  -- iterations 2+ of A/A2/S/R
  :213 general pre-index   -- row C
  :338 fast    pre-index   -- row C2 ONLY (two passes, base re-seeded each pass
                              so the second execution is still unaligned)

Loads and stores are SEPARATE instantiations of this template, so a row set made
only of loads cannot see a store-side regression at all: row S is a store
livelock. Register-offset forms (`A__REG`) are a third family: row R.

THE HEADLINE IS A LOOP THAT CANNOT MAKE PROGRESS
------------------------------------------------
When the post-index offset is not a multiple of the access size the masked
writeback is a FIXED POINT. Word base 0x10001 with offset 1 masks to 0x10000,
adds 1, and writes back 0x10001 -- the value it started from. No amount of guest
patience recovers from that, which is why it is the headline rather than the
one-off wrong values. Progress is asserted as an exact architectural value after
an architecturally bounded iteration count, never as "how far did it get in T
seconds": the loop is counted in r3, which is independent of r0.

WHAT IS MANDATED VERSUS MERELY PERMITTED
----------------------------------------
A review seat supplied a precision worth keeping: the writeback is ARCHITECTURALLY
MANDATED for word accesses, whose unaligned behaviour is defined. Unaligned
halfword loads (A4.1.28) and doubleword accesses (A2.8) are UNPREDICTABLE prior
to ARMv6, so there an unmasked writeback is permitted-and-consistent rather than
required. Every row below except G is a word form, i.e. in mandated space. Row G
is labelled DISC-M ("model") for exactly that reason: it pins the pseudocode
model of A5.3.6, not a silicon mandate, and it asserts only the BASE -- an
unaligned halfword load's DATA is UNPREDICTABLE and must never be asserted.

NO LDRD/STRD ROW, overruling three review seats: A2.8 makes a doubleword access
UNPREDICTABLE prior to ARMv6 whenever the address is not doubleword-aligned, so
every base that would exercise the `~7` mask makes the instruction unspecified.
The general-path fix covers LDRD/STRD (the fast path chickens out to it at
:226-228, masking with `datalen - 1` == 7) but that coverage cannot honestly be
gated. #355 already taught this project not to assert on encodings the
architecture declines to define.

NO UNALIGNED-LOAD-DATA ROW. This template masks without ROTATING, where ARMv5
and below with CP15 A == 0 rotate the aligned word right by 8 * addr[1:0] (A2.8
p. A2-38, A4.1.23) -- 0x11223344 here where a rotating implementation returns
0x44112233. A PIN pinning the unrotated value would be inverted by the round
that fixes the rotation: the row would be rewritten by the change it exists to
guard. A review seat caught this. Row H asserts the loaded data at an ALIGNED
base instead, where no rotation applies in any architecture version, so the data
path is still guarded without pinning anything the rotation round will move.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
SRC = 0x10000

#  Encodings. Bits after the 010 class are P U B W L, verified against the
#  ldrt form 0xe4b0a004 (`ldrt sl,[r0],#4`) that netbsd_copyin matches; the
#  register-offset forms use class 011. The halfword layout is
#  cond 000 P U I W L Rn Rd immH 1SH1 immL, checked against `ldrh r1,[r0]` ==
#  0xe1d010b0. EVERY word below was confirmed through the emulator's own
#  `unassemble` before this probe was run -- this project has shipped a
#  mis-encoded row before, one of them a committed gate row that measured the
#  wrong register for months.
MOV_R0_10000 = 0xE3A00801   # mov  r0,#0x10000
MOV_R0_0     = 0xE3A00000   # mov  r0,#0
ADD_R0_1     = 0xE2800001   # add  r0,r0,#1
MOV_R2_1     = 0xE3A02001   # mov  r2,#1
MOV_R3_0     = 0xE3A03000   # mov  r3,#0
MOV_R3_1     = 0xE3A03001   # mov  r3,#1
LDR_P1       = 0xE4901001   # ldr  r1,[r0],#1     post-index, +1
LDR_P4       = 0xE4901004   # ldr  r1,[r0],#4     post-index, +4
LDR_PRE4W    = 0xE5B01004   # ldr  r1,[r0,#4]!    pre-index + writeback
LDR_PRE4     = 0xE5901004   # ldr  r1,[r0,#4]     pre-index, NO writeback
LDR_M4       = 0xE4101004   # ldr  r1,[r0],#-4    post-index, -4  (U == 0)
LDRB_P1      = 0xE4D01001   # ldrb r1,[r0],#1     byte: masks nothing
LDRH_P1      = 0xE0D010B1   # ldrh r1,[r0],#1     halfword: masks ~1
#  0xE480, not 0xE400: with L == 0 the U bit sits in the same nibble, so the
#  obvious guess 0xe4002001 disassembles as `str r2,[r0],#-1` -- a NEGATIVE
#  offset. Caught by `unassemble` before the sweep; it would have produced an
#  UNEXPECTED value and sent the round debugging the emulator.
STR_P1       = 0xE4802001   # str  r2,[r0],#1     STORE post-index, +1
LDR_POST_R2  = 0xE6901002   # ldr  r1,[r0],r2     post-index, REGISTER offset
ADD_R3_1     = 0xE2833001   # add  r3,r3,#1
SUBS_R3_1    = 0xE2533001   # subs r3,r3,#1
CMP_R3_10    = 0xE353000A   # cmp  r3,#10
SPIN         = 0xEAFFFFFE   # b .

UNAL = [MOV_R0_10000, ADD_R0_1]     # base 0x10001
ADD_R0_2     = 0xE2800002           # add  r0,r0,#2
ADD_R0_3     = 0xE2800003           # add  r0,r0,#3
LDR_OFF0     = 0xE5901000           # ldr  r1,[r0]   pre-index, offset 0, no wb
UNAL2 = [MOV_R0_10000, ADD_R0_2]    # base 0x10002
UNAL3 = [MOV_R0_10000, ADD_R0_3]    # base 0x10003
ALIGN = [MOV_R0_10000]              # base 0x10000
ZERO = [MOV_R0_0]                   # base 0


def _br(cond, frm, to):
    return cond | ((to - (frm + 2)) & 0xFFFFFF)


def once(setup, body):
    """One execution of `body`, then spin. Reaches the GENERAL path only."""
    return list(setup) + list(body) + [SPIN]


def loop10(setup, body):
    """`body` ten times, counted in r3 so the count cannot depend on r0.

    Iteration 1 takes the general path (page not yet in the translation array);
    iterations 2+ take the fast path. One row, both writeback sites.
    """
    prog = list(setup) + [MOV_R3_0]
    top = len(prog)
    prog += list(body) + [ADD_R3_1, CMP_R3_10]
    br = len(prog)
    prog += [_br(0x1A000000, br, top), SPIN]      # bne -> top
    return prog


def warmed(body):
    """Two passes, base RE-SEEDED each pass, so pass 2 is still unaligned.

    Without the re-seed the pre-index row self-heals: pass 1 leaves an ALIGNED
    base, and pass 2 then has nothing to discriminate. Pass 2 is the only
    execution in this whole set that reaches the fast pre-index site.
    """
    prog = [MOV_R3_1]
    top = len(prog)
    prog += UNAL + list(body) + [SUBS_R3_1]
    br = len(prog)
    prog += [_br(0x5A000000, br, top), SPIN]      # bpl -> top
    return prog


#  Names stay well inside the %-34s column they print into, so a gate check of
#  the form "<name>  *DISC" always sees at least two spaces. A name as long as
#  its column makes such a check UNSATISFIABLE -- shipped once before.
ROWS = [
    # name, kind, program, register, buggy, arch
    ("A wb word post1 unal x10", "DISC",
     loop10(UNAL, [LDR_P1]), "r0", 0x10001, 0x1000B),
    ("A wb word post1 algn x10", "DISC",
     loop10(ALIGN, [LDR_P1]), "r0", 0x10001, 0x1000A),
    ("A wb word post4 unal", "DISC",
     once(UNAL, [LDR_P4]), "r0", 0x10004, 0x10005),
    ("A wb word pre4 unal gen", "DISC",
     once(UNAL, [LDR_PRE4W]), "r0", 0x10004, 0x10005),
    ("A wb word pre4 unal fast", "DISC",
     warmed([LDR_PRE4W]), "r0", 0x10004, 0x10005),
    ("A wb word postneg4 unal", "DISC",
     once(UNAL, [LDR_M4]), "r0", 0x0000FFFC, 0x0000FFFD),
    ("A wb store post1 unal x10", "DISC",
     loop10(UNAL, [STR_P1]), "r0", 0x10001, 0x1000B),
    ("A wb regofs post1 unal x10", "DISC",
     loop10(UNAL + [MOV_R2_1], [LDR_POST_R2]), "r0", 0x10001, 0x1000B),
    ("A wb halfword post1 unal", "DISC-M",
     once(UNAL, [LDRH_P1]), "r0", 0x10001, 0x10002),
    ("A wb word post4 algn", "PIN",
     once(ALIGN, [LDR_P4]), "r0", 0x10004, 0x10004),
    ("A wb algn load data", "PIN",
     once(ALIGN, [LDR_P4]), "r1", 0x11223344, 0x11223344),
    ("A wb byte post1 unal", "PIN",
     once(UNAL, [LDRB_P1]), "r0", 0x10002, 0x10002),
    ("A wb word pre4 no wb", "PIN",
     once(ALIGN, [LDR_PRE4]), "r0", 0x10000, 0x10000),
    ("A wb wrap from zero", "PIN",
     once(ZERO, [LDR_M4]), "r0", 0xFFFFFFFC, 0xFFFFFFFC),

    #  #362: an unaligned word LOAD returns the aligned word ROTATED RIGHT by
    #  8 * addr[1:0] (DDI 0100I A2.8, A4.1.23). This template masked and never
    #  rotated. The word at 0x10000 is 0x11223344, so the three offsets owe
    #  0x44112233, 0x33441122 and 0x22334411, and the "buggy" column is the
    #  unrotated word -- which is what the pre-fix build returned in all three.
    #
    #  These rows IDENTIFY the model rather than merely failing an expectation:
    #  mask-only, rotate, and the ARMv6 U == 1 true-unaligned access are pairwise
    #  distinct at every nonzero offset, so a wrong answer says WHICH model is
    #  implemented. Measured MASK-only on all three pre-fix, ROTATE post-fix.
    #
    #  Offset 0 is deliberately absent: rotation by zero is the identity, so such
    #  a row could never fail, and the aligned case is already pinned elsewhere.
    ("A wb rot word unal plus1", "DISC",
     once(UNAL, [LDR_OFF0]), "r1", 0x11223344, 0x44112233),
    ("A wb rot word unal plus2", "DISC",
     once(UNAL2, [LDR_OFF0]), "r1", 0x11223344, 0x33441122),
    ("A wb rot word unal plus3", "DISC",
     once(UNAL3, [LDR_OFF0]), "r1", 0x11223344, 0x22334411),
]


def run(prog, regs):
    stub = "/tmp/r104c_stub.bin"
    with open(stub, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, "little"))
    pid, fd = pty.fork()
    if pid == 0:
        #  -T halts on a non-existent memory access rather than logging one
        #  host line per access: a run that goes wrong stops instead of
        #  flooding the pty and making the row host-speed dependent.
        os.execvp(BIN, [BIN, "-V", "-A", "-T", "-E", "testarm", "-M", "64",
                        "0x%x:%s" % (CODE, stub)])
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

    def wait_from(mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark and buf[mark:].rstrip().endswith(">"):
                return True
        return False

    def send(sx):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait_from(mark)

    if not wait_from(0, 60):
        os.kill(pid, 9)
        os.waitpid(pid, 0)
        return None

    #  Four distinct bytes per word, so a byte-order or rotation change would
    #  be unmistakable rather than a plausible-looking value.
    for i in range(8):
        send("put w 0x%x, 0x%08x" % (SRC + 4 * i, 0x11223344 + i))
    send("put w 0x0, 0x99887766")        # row K reads from address 0

    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)

    #  The programs finish in microseconds and then spin at `b .`, so the two
    #  second wait is ~six orders of magnitude of margin: the registers are
    #  settled long before the interrupt, and no row's value depends on how far
    #  execution got. The iteration count lives in r3, not in elapsed time.
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < 2.0:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith(">")):
        os.write(fd, b"\x03")
        wait_from(cmark, 15)

    out = {}
    for rn in regs:
        mark = len(buf)
        send("print %s" % rn)
        #  `print <reg>` answers with the bare value on its own line
        #  ("0x11223344"), NOT "r0 = 0x...". An earlier revision grepped for
        #  the "r0 = " form and scored every row DEAD -- a broken probe that
        #  looks exactly like a broken emulator.
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            out[rn] = int(m.group(1), 16)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.2)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return out


#  Gate-convention output: one "<name>  ... ok" / "... FAIL" line per row, a
#  RESULT= line, and a CONTROL= line proving the instrument is LIVE rather than
#  merely quiet. The control is the loaded-data row: r1 starts at 0, so a
#  distinctive NONZERO value proves the guest really executed and really loaded,
#  which is the check this project adds after a committed row was found to be
#  measuring the wrong register field -- a wrong field reads 0, and a row that
#  accepts 0 accepts that mistake by accident.
print("=== #19: ARM load/store base writeback (pre/post-index) ===")
print("    buggy = masked base + offset ; arch = unmasked (A5.2.5 / A5.2.8)")
print("    DISC-M pins the A5.3.6 pseudocode model, not a silicon mandate")

ngot = 0
control = "FAIL"
for name, kind, prog, reg, buggy, arch in ROWS:
    got = run(prog, [reg])
    if got is None or reg not in got:
        print("%-32s  %-6s DEAD  FAIL" % (name, kind))
        continue
    v = got[reg]
    ok = (v == arch)
    ngot += ok
    if name == "A wb algn load data" and v == 0x11223344:
        control = "OK"
    print("%-32s  %-6s %s=0x%08x want 0x%08x (buggy 0x%08x)  %s"
          % (name, kind, reg, v, arch, buggy, "ok" if ok else "FAIL"))

print("WRITEBACK_CONTROL=%s" % control)
print("WRITEBACK_RESULT=%d/%d" % (ngot, len(ROWS)))
