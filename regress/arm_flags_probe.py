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
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "testarm", "-M", "64",
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
    #  The name column is 26 wide, not 24, and that is load-bearing: gate_arm.sh
    #  matches each named row with TWO spaces after the name, to stop a name that
    #  is a prefix of a longer one from matching both. A name as long as the
    #  column gets NO padding and only the format's single separator space, so
    #  its check can never match anything -- the mirror image of the double-count
    #  trap, and it silently made two checks unsatisfiable until a diff-review
    #  seat found them. 26 leaves >= 2 spaces for every name here; the longest is
    #  24. Keep this wider than the longest row name if any are added.
    ok = (got == want)
    rows.append(ok)
    print("%-26s %-12s %-12s %s %s"
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
    row(name, "DISC" if name != "uxtab ROR 0" and name != "rot0 movs C"
        and name != "mvn S-clear" else "PIN", got, want)

print("ARM_FLAGS_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
