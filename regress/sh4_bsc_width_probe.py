#!/usr/bin/env python3
"""#441 DETECTOR: SH4_BCR2 / SH4_BCR3 service a non-16-bit guest access instead
of terminating the emulator.

Rung 3.  Real SH-4 guest instructions through real address decode, real
`memory_rw` and real device dispatch, on an UNMODIFIED in-tree `-E landisk`.
No source is edited, no `device_add` of our own, no boot.

WHAT THIS IS AND IS NOT.  The pre-fix WITNESS (`_scratchpad/_opusseat_sh4_bcr2_
probe.py`) asserted the SYMPTOM -- "a 4-byte store kills the host" -- and so it
goes red once the defect is gone, which is what a witness should do.  This file
is the DETECTOR: it asserts the FIXED behaviour, fails on the pre-fix build, and
is built specifically to fail on the mutants a pass-1 seat produced against the
fix.  Grading one by the other's clauses is a category error in either direction.

    D0  every arm produced data              (absent data must FAIL, not pass)
    D1  4-byte write reaches the register, masked
    D2  4-byte read returns it in its own lane
    D3  a 1-byte write is NOT promoted to 16 bits
    D4  BOTH sites carry the LATCHED form, in ONE process
    D5  a second non-16-bit access in one process survives
    D6  a 4-byte READ is diagnosed too, not only a write
    D8  BCR3's write path still reaches its register

(D7, the big-endian lane, needs a `byte_order(big)` config file and is left to
the round record rather than run here -- see the note at the foot of this file.)

*** D4's ORACLE IS NOT THE REGISTER NAME, AND THAT IS THE WHOLE POINT. ***  A
two-character mutant sharing one latch flag between the sites (`[site]` ->
`[0]`) passed a 13-row detector whose D4 asked "does the string BCR3 appear?",
because the DEMOTED `debug()` prints the same name.  Worse, under the cold
debugger `single_step` is true, so `debug()`'s `quiet_mode` early-out never
fires and a probe run this way CANNOT distinguish `fatal()` from `debug()` by
presence at all.  D4 counts the latched suffix instead.

usage: sh4_bsc_width_probe.py <gxemul-binary> <landisk-kernel>
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
DEST = 0x8c010100
BCR1 = 0xff800000
BCR2 = 0xff800004
#  #441: BCR3 is 0xff800050, NOT 0xff800006.  The pass-1 brief asserted the
#  latter without opening sh4_bscreg.h:70, and the three packet-fed seats -- which
#  by construction cannot check a fact the packet gets wrong -- built whole
#  designs on the imagined adjacency, while every seat that could open the header
#  caught it.  The two registers do not share an access window.
BCR3 = 0xff800050

MOV_L_R0_AT_R1 = 0x2102   # mov.l r0,@r1
MOV_L_R0_AT_R2 = 0x2202   # mov.l r0,@r2
MOV_W_R0_AT_R1 = 0x2101   # mov.w r0,@r1
MOV_B_R0_AT_R1 = 0x2100   # mov.b r0,@r1
MOV_B_AT_R1_R4 = 0x6410   # mov.b @r1,r4  (sign-extends)
MOV_L_AT_R1_R2 = 0x6212   # mov.l @r1,r2
MOV_W_AT_R1_R2 = 0x6211   # mov.w @r1,r2   (sign-extends)
MOV_L_R2_AT_R3 = 0x2322   # mov.l r2,@r3
LATCHED = "(reported once per register)"


#  #441 pass 2: the big-endian arm needs a CONFIG FILE, because byte_order() has no -E
#  equivalent.  emul.c applies the override AFTER the ELF's own byte order, so the
#  `cpu: SH7751R (Little-endian)` banner it prints is stale and must not be used as the
#  control -- BE0 below stores a known word and reads the BYTES back instead.
BE_CONF = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       ".sh4_bsc_be.conf.tmp")


def write_be_conf():
    with open(BE_CONF, "w") as f:
        f.write('machine(\n\tname("be-landisk")\n\ttype("landisk")\n'
                '\tbyte_order("big")\n\tmemory(64)\n\tload("%s")\n)\n'
                % os.path.abspath(KERNEL))
    return BE_CONF


def session(cmds, nstep, be=False):
    """One cold-debugger session.  Returns (buf, alive)."""
    pid, fd = pty.fork()
    if pid == 0:
        if be:
            os.execvp(BIN, [BIN, "-V", "@" + write_be_conf()])
        else:
            os.execvp(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""
    died = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            died[0] = True
            return False
        if not d:
            died[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(s):
        #  `_mark`, not `mark`: gate 6's fresh-mark census keys on that exact spelling
        #  (`return wait(mark=_mark, ...)`), and every other pty probe in the tree writes
        #  it that way.  Named `mark` at first, which left the guard PRESENT but INVISIBLE
        #  to the census -- the row went red while the two counts either side went green,
        #  a signature that reads like a defect and is not one.  Conforming to the house
        #  idiom is the fix; teaching the census a second spelling would only make it
        #  count substrings of the first.
        b = (s + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        while n < len(b):
            try:
                n += os.write(fd, b[n:])
            except OSError:
                died[0] = True
                return False
        return wait(mark=_mark, echo=s if s else None)

    if not wait(timeout=90):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None, False

    for c in cmds:
        send(c)
    if nstep:
        send("step %d" % nstep)

    #  Liveness of the SESSION after the step: a dump that answers proves the
    #  host is alive; no answer plus a closed pty proves it is not.
    alive = False
    for _ in range(3):
        mark = len(buf)
        if send("dump 0x%x 0x%x" % (DEST, DEST + 4)):
            if re.search(r"0x0*[0-9a-f]+\s+[0-9a-f]{8}", buf[mark:]):
                alive = True
                break
        if died[0]:
            break
        time.sleep(0.5)
        rd(0.5)
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t = time.time()
    while time.time() - t < 5 and rd(0.3):
        pass
    for fn in (lambda: os.kill(pid, 9), lambda: os.waitpid(pid, 0)):
        try:
            fn()
        except Exception:
            pass
    return buf, alive


def dumped(buf):
    m = re.findall(r"0x0*[0-9a-f]+\s+([0-9a-f]{8})", buf or "")
    return m[-1] if m else None


def poke(addr, halfwords):
    """Plant instruction halfwords at CODE and point pc at them."""
    return ["put h 0x%x, 0x%04x" % (CODE + 2 * i, hw)
            for i, hw in enumerate(halfwords)] + ["pc=0x%x" % CODE]


rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))


# ---------------------------------------------------------------- D1 / D2 / D6
#  Write 0x89ab3ffd as ONE 4-byte store, then read it back 16-bit.  On a
#  little-endian guest the register's own two bytes are idata[15:0], so the
#  device must hold 0x3ffd & 0x3ffd.  Pre-fix this arm KILLS THE HOST.
#  *** THE VALUE IS 0xc003 AND THAT IS THE WHOLE POINT OF THIS ROW. ***  It was 0x3ffd,
#  and 0x3ffd & 0x3ffd == 0x3ffd -- so a row NAMED "masked" could not see the mask, and
#  deleting `& 0x3ffd` passed 9/9.  0xc003 & 0x3ffd == 0x0001, so the masked and unmasked
#  results differ in every byte.  Pick oracle VALUES that the transform actually moves.
buf, alive = session(
    ["r0=0x89abc003", "r1=0x%x" % BCR2, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_L_R0_AT_R1, MOV_W_AT_R1_R2, MOV_L_R2_AT_R3]), 3)
d12 = dumped(buf)
row("D1 4-byte write reaches BCR2 AND IS MASKED; host survives",
    alive and d12 == "01000000", "alive=%s val=%s" % (alive, d12),
    "alive=True val=01000000 (0xc003 & 0x3ffd = 0x0001; unmasked would be 03c00000)")
#  Assert the MESSAGE, not merely that one was printed: swapping the
#  "Ignored"/"Servicing" ternary made the diagnostic state the opposite of what the code
#  did, and passed 9/9 against a presence-only oracle.  A 4-byte access IS serviced.
row("D6 the 4-byte access is diagnosed AND says it was serviced",
    bool(buf) and "BCR2" in buf and LATCHED in buf
    and "Servicing its own two bytes" in buf and "Ignored" not in buf,
    "latched=%s servicing=%s" % (bool(buf) and LATCHED in buf,
                                 bool(buf) and "Servicing its own two bytes" in buf),
    "both True, and the word 'Ignored' absent")

#  4-byte READ: same lane, and it must be diagnosed too -- a mutant that guards
#  only the write arm passes every write-side row.
buf, alive = session(
    ["r0=0x3ffd", "r1=0x%x" % BCR2, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_W_R0_AT_R1, MOV_L_AT_R1_R2, MOV_L_R2_AT_R3]), 3)
d2 = dumped(buf)
row("D2 4-byte read returns the register in its own lane",
    alive and d2 == "fd3f0000", "alive=%s val=%s" % (alive, d2),
    "alive=True val=fd3f0000")
row("D6b a 4-byte READ is diagnosed too, not only a write",
    bool(buf) and LATCHED in buf, "latched form present=%s" % (bool(buf) and LATCHED in buf),
    "True")

# ---------------------------------------------------------------- D3
#  A 1-byte write must NOT be promoted to a 16-bit one.  The reset value is
#  0x3ffc; a byte store of 0xa5 must leave it standing, not produce 0x00a5.
#  This row is also what makes the `len < 2` early-out visible: without it,
#  8 * (len - 2) on a size_t len==1 shifts by SIZE_MAX*8, which is UB.
buf, alive = session(
    ["r0=0xa5", "r1=0x%x" % BCR2, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_B_R0_AT_R1, MOV_W_AT_R1_R2, MOV_L_R2_AT_R3]), 3)
d3 = dumped(buf)
row("D3 a 1-byte write is not promoted to 16 bits",
    alive and d3 is not None and d3 not in ("a5000000", "00a50000")
    and "Ignored" in (buf or ""),
    "alive=%s val=%s said-Ignored=%s" % (alive, d3, "Ignored" in (buf or "")),
    "alive=True, val is not 0xa5, and the diagnostic says Ignored")


# ---------------------------------------------------------------- D9
#  *** A 1-BYTE READ.  THE HOLE THAT LET exit(1) BACK IN. ***  The reachable access
#  shapes are (read|write) x len(1|2|4) -- SIX -- and the first nine rows covered five.
#  A mutant adding `if (partial && writeflag == MEM_READ) exit(1);` therefore passed
#  every row while ending the host process on a guest-reachable path: the exact defect
#  this round exists to remove, reinstated under a fully green detector.
buf, alive = session(
    ["r1=0x%x" % BCR2, "r3=0x%x" % DEST, "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_B_AT_R1_R4]), 1)
row("D9 a 1-byte READ does not kill the host",
    alive, "alive=%s" % alive, "alive=True")

# ---------------------------------------------------------------- D4 / D5 / D8
#  BOTH sites, in ONE process.  D4 counts the LATCHED SUFFIX, never the register
#  name -- see the module docstring for why the name is not an oracle.
buf, alive = session(
    ["r0=0x89ab3ffd", "r1=0x%x" % BCR2, "r2=0x%x" % BCR3, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + ["put h 0x%x, 0x%04x" % (CODE + 0, MOV_L_R0_AT_R1),      # BCR2, 4-byte
       "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R0_AT_R1),      # BCR2 again
       "put h 0x%x, 0x%04x" % (CODE + 4, 0x6113),              # mov r1,r1 (nop-ish)
       "pc=0x%x" % CODE], 2)
n_latched = (buf or "").count(LATCHED)
row("D5 a second non-16-bit access in one process survives",
    alive and n_latched == 1, "alive=%s latched-lines=%d" % (alive, n_latched),
    "alive=True latched-lines=1 (the second is demoted, not repeated)")

#  Same constant, opposite direction: BCR3 is UNMASKED, so 0xc003 must arrive whole.
#  The old 0x1234 was mask-transparent (0x1234 & 0x3ffd == 0x1234), so ADDING a mask to
#  BCR3 -- silently dropping bits 15, 14 and 1 -- passed 9/9.
buf3, alive3 = session(
    ["r0=0x89abc003", "r1=0x%x" % BCR3, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_L_R0_AT_R1, MOV_W_AT_R1_R2, MOV_L_R2_AT_R3]), 3)
d8 = dumped(buf3)
row("D8 BCR3's write reaches its register UNMASKED",
    alive3 and d8 == "03c0ffff", "alive=%s val=%s" % (alive3, d8),
    "alive=True val=03c0ffff -- mov.w SIGN-EXTENDS and 0xc003 has bit 15 set, so r2 is "
    "0xffffc003; a stray & 0x3ffd would give 0x0001 and read back 01000000")

#  D4: BOTH SITES IN *ONE* PROCESS.  *** THE FIRST VERSION OF THIS ROW TOUCHED THE
#  TWO REGISTERS IN TWO SEPARATE SESSIONS AND THE SHARED-LATCH MUTANT PASSED 9/9.
#  ***  Each fresh process starts with every flag clear, so a shared flag latches
#  once per session and two sessions produce two latched lines -- indistinguishable
#  from per-site flags.  The requirement was written correctly in this file's
#  docstring ("in ONE process") and then implemented across two; the mutant run is
#  what caught it, which is the only reason it is right now.
#
#  With per-site flags this session prints TWO latched lines; with one shared flag
#  it prints ONE, because BCR3's FIRST report is demoted to debug().
buf4, alive4 = session(
    ["r0=0x89ab3ffd", "r1=0x%x" % BCR2, "r2=0x%x" % BCR3, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + ["put h 0x%x, 0x%04x" % (CODE + 0, MOV_L_R0_AT_R1),   # 4-byte store to BCR2
       "put h 0x%x, 0x%04x" % (CODE + 2, MOV_L_R0_AT_R2),   # 4-byte store to BCR3
       "pc=0x%x" % CODE], 2)
n4 = (buf4 or "").count(LATCHED)
row("D4 BOTH sites latch SEPARATELY, in one process (count the suffix, NOT the name)",
    alive4 and n4 == 2, "alive=%s latched-lines=%d" % (alive4, n4),
    "alive=True latched-lines=2 -- a SHARED latch demotes BCR3's first report to 1")

# ---------------------------------------------------------------- D10
#  *** A LEGAL 16-BIT ACCESS MUST NOT BE DIAGNOSED AT ALL, AND NOTHING ASSERTED THAT. ***
#  Found by a positive control that failed to be one: neutering the `len == sizeof(uint16_t)`
#  fast path (`if (0)`) passed 12/12.  That mutant is nearly behaviour-equivalent -- `partial`
#  is false for len == 2, so the access is still serviced with shift 0 -- and its ONLY effect
#  is to make every correct 16-bit driver access emit a "it is a 16-bit register" complaint.
#  On a real landisk boot, which touches BCR2 three times and BCR3 once, that is a flood of
#  wrong diagnostics about perfectly legal accesses, and `fatal()` cannot be silenced with -q.
#
#  The lesson is about CONTROLS, not about this mutant: a positive control that passes has
#  either a dead pipeline or a hole, and assuming the first would have hidden this.  The
#  pipeline was demonstrably alive -- five other mutants died in the same run.
buf10, alive10 = session(
    ["r0=0x1234", "r1=0x%x" % BCR2, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_W_R0_AT_R1, MOV_W_AT_R1_R2, MOV_L_R2_AT_R3]), 3)
quiet10 = bool(buf10) and "16-bit register" not in buf10 and LATCHED not in buf10
row("D10 a legal 16-bit access is NOT diagnosed",
    alive10 and quiet10, "alive=%s quiet=%s" % (alive10, quiet10),
    "alive=True quiet=True -- a correct driver access must produce no complaint")


# ---------------------------------------------------------------- D7
#  *** THE BIG-ENDIAN LANE, AND WITHOUT IT `return 0;` FOR THE SHIFT PASSES 9/9. ***  It
#  was left out of the first draft as "a second invocation shape"; that is exactly the
#  reasoning that leaves a mechanism uncovered, which this round has now paid for twice.
#
#  BE0 is the control and it does NOT trust the banner: emul.c applies byte_order() AFTER
#  the ELF's, so the printed "(Little-endian)" is stale.  Instead a guest 4-byte store of
#  0x12345678 must dump as 12345678 in address order rather than 78563412.
buf7, alive7 = session(
    ["r0=0x12345678", "r3=0x%x" % DEST, "put w 0x%x, 0x11111111" % DEST,
     "r1=0x%x" % DEST]
    + poke(CODE, [MOV_L_R0_AT_R1]), 1, be=True)
c7 = dumped(buf7)
row("D7a CONTROL: the CPU really is big-endian",
    alive7 and c7 == "12345678", "alive=%s val=%s" % (alive7, c7),
    "alive=True val=12345678 (little-endian would give 78563412)")

#  On BE the register's own two bytes are the TOP halfword of the access, so a 4-byte
#  store of 0xc0030000 must land 0xc003 & 0x3ffd = 0x0001 in BCR2.  A shift of 0 would
#  take the BOTTOM halfword -- 0x0000 -- instead.
#  BOTH halves of the input are non-zero and mask to DIFFERENT values, so the row
#  discriminates by more than one bit: top 0xc003 & 0x3ffd = 0x0001, bottom 0xa5a5 &
#  0x3ffd = 0x25a5.  The first draft used 0xc0030000, whose bottom half masks to 0x0000 --
#  a one-bit discriminator -- and carried an expected constant lifted from another probe
#  that had a different input entirely.  Recompute oracle values for YOUR input.
buf8, alive8 = session(
    ["r0=0xc003a5a5", "r1=0x%x" % BCR2, "r3=0x%x" % DEST,
     "put w 0x%x, 0x11111111" % DEST]
    + poke(CODE, [MOV_L_R0_AT_R1, MOV_W_AT_R1_R2, MOV_L_R2_AT_R3]), 3, be=True)
b7 = dumped(buf8)
row("D7b a 4-byte write takes the FIRST two bytes on big-endian",
    alive8 and b7 == "00000001", "alive=%s val=%s" % (alive8, b7),
    "alive=True val=00000001 (top half 0xc003 & 0x3ffd = 0x0001; a shift of 0 would take "
    "the BOTTOM half 0xa5a5 & 0x3ffd = 0x25a5 and give 000025a5)")

try:
    os.unlink(BE_CONF)
except OSError:
    pass

# ---------------------------------------------------------------- D0, last
#  ABSENT DATA MUST FAIL, NOT PASS.  Every value the rows above consult has to
#  have been present; a run that never started leaves defaults behind, and a
#  comparison of two defaults reports ok on a probe that measured nothing.
row("D0 every arm produced data",
    all(x is not None for x in (d12, d2, d3, d8, c7, b7))
    and n_latched >= 1 and n4 >= 1 and buf10 is not None,
    "d12=%s d2=%s d3=%s d8=%s latched=%d d4=%d be=%s/%s"
    % (d12, d2, d3, d8, n_latched, n4, c7, b7),
    "all present")

print("=" * 76)
print("#441  SH4 BSC non-16-bit access -- DETECTOR")
print("=" * 76)
fails = 0
for name, ok, got, want in rows:
    fails += 0 if ok else 1
    print("  %-4s %-58s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))
print()
print("SH4_BSC_WIDTH_RESULT=%d/%d" % (len(rows) - fails, len(rows)))
print("SH4_BSC_WIDTH_PASS" if fails == 0 else "SH4_BSC_WIDTH_FAIL")
sys.exit(1 if fails else 0)
