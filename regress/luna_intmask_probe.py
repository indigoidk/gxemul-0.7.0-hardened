#!/usr/bin/env python3
"""MEASURE SEAT witness + detector for dev_luna88k.c:816 (INT_ST_MASK guarded low bits).

ONE cold-debugger session, real m88k guest instructions, real address decode, real
memory_rw, COMMITTED UNMODIFIED machine description (-e luna-88k + the committed rig
image; no device_add, no new machine, nothing introduced in order to reach the site).
Witness-ladder rung 3.

WHY THE OBVIOUS PROBE VALUE IS WRONG.  The read path is
    odata = interrupt_enable[cpunr] >> 8 ;  odata |= (highestCurrentStatus << 29)
so a write of 0x00000001 is INVISIBLE -- bits 7..0 shift out entirely and store-as-is,
store-masked and not-storing-at-all all read back identically.  Every value row below
therefore uses a bit in 25..8 and TWO DIFFERENT architected prefixes, so that the three
candidate shapes produce three DIFFERENT numbers rather than one shared one.

Bits 31..29 of odata are the pending-level field and are not under the probe's control on
a live machine (a timer tick can set one), so every value assertion is on (r4 & 0xffffff).

Encodings (cpu_m88k.c:991-1019, same source as regress/m8820x_sites_probe.py):
    ld rD,rS1,IMM16  op26=0x05 ;  st rD,rS1,IMM16  op26=0x09
EVERY PLANTED WORD IS DISASSEMBLED AND ITS TEXT CHECKED BEFORE IT IS STEPPED -- this
project has a recorded incident where a wrong register field made a gate row measure the
wrong thing for months.

usage: luna_intmask_probe.py <gxemul-binary> <images-dir>
"""
import os, pty, re, select, sys, time

BIN     = sys.argv[1]
IMAGES  = sys.argv[2]
IMG     = IMAGES + "/liveimage-luna88k-raw-20250518.img"
CODE    = 0x00010000
SCRATCH = 0x00020000
DEV     = 0x65000000        # INT_ST_MASK0 -- the LITERAL, deliberately not the #define


def enc(is_store, d, s1, imm16):
    return ((0x09 if is_store else 0x05) << 26) | (d << 21) | (s1 << 16) | imm16


SLOTS = [(CODE + 0x00, enc(True,  4, 5, 0), "st\tr4,r5,0x0"),
         (CODE + 0x04, enc(False, 4, 5, 0), "ld\tr4,r5,0x0"),
         (CODE + 0x08, enc(True,  4, 6, 0), "st\tr4,r6,0x0"),
         (CODE + 0x0c, enc(False, 4, 6, 0), "ld\tr4,r6,0x0")]
A_WDEV, A_RDEV, A_WRAM, A_RRAM = [s[0] for s in SLOTS]

pid, fd = pty.fork()
if pid == 0:
    os.chdir(IMAGES)
    os.execvp(BIN, [BIN, "-V", "-e", "luna-88k", "-d", "R:" + IMG, "boot"])
    os._exit(127)

buf = ""
dead = [False]


def rd(t=0.4):
    global buf
    r, _, _ = select.select([fd], [], [], t)
    if fd not in r:
        return True
    try:
        d = os.read(fd, 65536)
    except OSError:
        dead[0] = True
        return False
    if not d:
        dead[0] = True
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


def send(x, timeout=60):
    b = (x + "\n").encode("latin1")
    _mark = len(buf)
    n = 0
    try:
        while n < len(b):
            n += os.write(fd, b[n:])
    except OSError:
        dead[0] = True
        return False
    return wait(mark=_mark, echo=x if x else None)


#  Loose on wording, tight on the register name: the row must survive a reworded message
#  but must not count some other luna88k diagnostic.  The second alternative is the
#  PRE-FIX text, so the same script counts on both sides of the edit.
DIAG_NEW = re.compile(r"luna88k[^\r\n]{0,80}INT_ST_MASK")
DIAG_OLD = re.compile(r"TODO: luna88k interrupts")


def ndiag():
    return len(DIAG_NEW.findall(buf)) + len(DIAG_OLD.findall(buf))


def r4():
    global buf
    mark = len(buf)
    if not send("reg", timeout=30):
        return None
    m = re.search(r"r4\s*=\s*0x([0-9a-fA-F]+)", buf[mark:])
    return int(m.group(1), 16) if m else None


fails = []


def check_ge(label, got, want):
    ok = got is not None and got >= want
    print("  %-62s got=%s want>=%d %s" % (label, got, want, "OK" if ok else "*** MISMATCH ***"))
    if not ok:
        fails.append(label)
    return ok


def check(label, got, want, mask=0xffffffff):
    ok = got is not None and (got & mask) == want
    print("  %-62s got=%s want=0x%08x %s"
          % (label, ("0x%08x" % got) if got is not None else "DEAD/NONE", want,
             "OK" if ok else "*** MISMATCH ***"))
    if not ok:
        fails.append(label)
    return ok


def step_at(addr):
    """Point pc at a planted slot and execute exactly it.  False => the host died."""
    if dead[0]:
        return False
    if not send("pc=0x%08x" % addr):
        return False
    ok = send("step 1", timeout=30)
    return ok and not dead[0]


def bail(msg, verdict, code=1):
    print("  " + msg)
    print("LUNA_INTMASK_WITNESS=%s" % verdict)
    print("PROBE_WALL=%.1fs" % (time.time() - t0))
    sys.exit(code)


print("BINARY=%s" % BIN)
t0 = time.time()
if not wait(timeout=180):
    print("NO-PROMPT")
    sys.exit(2)

for addr, word, _ in SLOTS:
    send("put w 0x%08x, 0x%08x" % (addr, word))
print("PLANTED -- each slot disassembled and checked against the emulator's own spelling:")
dis_ok = True
for addr, word, want in SLOTS:
    mark = len(buf)
    send("unassemble 0x%08x" % addr)
    m = re.search(r"((?:ld|st)[\w.]*\s+r\d+,r\d+,0x[0-9a-f]+)", buf[mark:])
    got = m.group(1) if m else "(none)"
    good = re.sub(r"\s+", " ", got) == re.sub(r"\s+", " ", want)
    print("  0x%08x word=0x%08x dis=%-20r %s" % (addr, word, got, "OK" if good else "*** WRONG ENCODING ***"))
    dis_ok = dis_ok and good
if not dis_ok:
    print("LUNA_INTMASK_WITNESS=FAIL (encoding)")
    sys.exit(2)

send("r5=0x%08x" % DEV)
send("r6=0x%08x" % SCRATCH)

print("C1 LIVENESS -- plain RAM through the same decode:")
send("r4=0x12345678")
step_at(A_WRAM)
send("r4=0x00000000")
step_at(A_RRAM)
check("C1 RAM readback", r4(), 0x12345678)

print("C2 DEVICE SIGNATURE -- the handler's own >>8; RAM cannot produce this:")
send("r4=0xfc000000")
step_at(A_WDEV)
send("r4=0x00000000")
if not step_at(A_RDEV):
    bail("host died on a LEGAL read -- the probe itself is broken", "FAIL (probe)", 2)
g = r4()
check("C2 read INT_ST_MASK0 after legal write of 0xfc000000", g, 0x00fc0000, 0x00ffffff)
if g is not None and g == 0xfc000000:
    print("  *** 0xfc000000 verbatim is RAM/absorbed-store behaviour, NOT this device ***")

print("D1 GUARDED WRITE #1 -- 0x84000100 (INT_SLAVE_MASK prefix + bit 8):")
send("r4=0x84000100")
if not step_at(A_WDEV):
    hits = DIAG_OLD.findall(buf) or DIAG_NEW.findall(buf)
    m = re.findall(r"\[[^\r\n]*luna88k[^\r\n]*\]", buf)
    print("  HOST DIED.  emulator said: %s" % (m[-1] if m else "(no diagnostic captured)"))
    print("SYMPTOM=EXIT_ON_GUARDED_WRITE")
    bail("this is the PRE-FIX symptom, on a committed unmodified machine description.",
         "PRE_FIX_SYMPTOM")
send("r4=0x00000000")
step_at(A_RDEV)
check("D1 readback  as-is=0x00840001 masked=0x00840000 nostore=0x00fc0000", r4(), 0x00840001, 0x00ffffff)
check_ge("E1 a diagnostic was emitted at all -- 0 means the guard was deleted outright", ndiag(), 1)

print("D2 GUARDED WRITE #2 -- 0xe4000200; kills latch-once-then-exit-on-the-next:")
send("r4=0xe4000200")
if not step_at(A_WDEV):
    bail("HOST DIED ON THE SECOND GUARDED WRITE -- a latch that still exits later.",
         "FAIL (died on hit 2)")
send("r4=0x00000000")
step_at(A_RDEV)
check("D2 readback  as-is=0x00e40002 masked=0x00e40000 nostore=0x00840001", r4(), 0x00e40002, 0x00ffffff)

print("D3 GUARDED WRITE #3 -- 0xc4000041, low bits ONLY in 7..0; kills a narrowed guard:")
send("r4=0xc4000041")
if not step_at(A_WDEV):
    bail("HOST DIED on a write whose only low bits are 7..0 -- the guard is still lethal there.",
         "FAIL (died on hit 3)")
send("r4=0x00000000")
step_at(A_RDEV)
check("D3 readback -- bits 7..0 are UNOBSERVABLE, >>8 eats them", r4(), 0x00c40000, 0x00ffffff)

print("D4 A SECOND CASE LABEL -- INT_ST_MASK1 at 0x65000004; the site has FOUR:")
send("r5=0x%08x" % (DEV + 4))
send("r4=0x84000100")
if not step_at(A_WDEV):
    bail("HOST DIED on INT_ST_MASK1 -- the fix did not cover every case label.",
         "FAIL (died on cpunr 1)")
send("r4=0x00000000")
step_at(A_RDEV)
check("D4 readback from INT_ST_MASK1 -- independent of MASK0", r4(), 0x00840001, 0x00ffffff)
send("r5=0x%08x" % DEV)

print("C3 LIVENESS AGAIN -- the machine still executes after three guarded writes:")
send("r4=0x0badf00d")
step_at(A_WRAM)
send("r4=0x00000000")
step_at(A_RRAM)
check("C3 RAM readback", r4(), 0x0badf00d)

#  LATCH -- and this row is TEXT-COUPLED ON PURPOSE, with its weakness stated.
#  MEASURED: debugmsg_va() short-circuits on `!single_step` (debugmsg.c:181-183) and
#  debug() adds +1 to v when single-stepping (debugmsg.c:368-374), so IN A COLD DEBUGGER
#  EVERY DIAGNOSTIC PRINTS whatever its level.  A latched and an unlatched implementation
#  therefore emit the SAME NUMBER of lines here and no count can separate them.  The only
#  separator left is the first-hit marker in the message text, which a mutant restores in
#  one edit.  The real bound is a free-running property and belongs in a different
#  instrument; this row is a hint, not a proof.
#  THE CONSTANT ENCODES THE LATCH GRANULARITY THE ROUND SHIPS, and nothing else can:
#     per-DEVICE-INSTANCE latch (V1)  -> 1  (the D4 write to MASK1 is demoted)
#     per-CPU latch          (V1c)    -> 2  (MASK0 and MASK1 each report once)
#  MEASURED both ways.  Update it if the shipped granularity changes.
LATCH_FIRST_HITS = 2
once = len(re.findall(r"reported once", buf))
check("E2 LATCH (text-coupled, see comment) -- first-hit markers across 4 hits/2 regs",
      once, LATCH_FIRST_HITS)
print("DIAG_LINES_SEEN=%d" % ndiag())
for m in re.findall(r"\[[^\r\n]*luna88k[^\r\n]*INT_ST_MASK[^\r\n]*\]", buf):
    print("  emulator said: %s" % m)
try:
    os.write(fd, b"quit\n")
    time.sleep(0.3)
    os.kill(pid, 9)
    os.waitpid(pid, 0)
except Exception:
    pass
print("LUNA_INTMASK_WITNESS=%s" % ("PASS" if not fails else ("FAIL " + "; ".join(fails))))
print("PROBE_WALL=%.1fs" % (time.time() - t0))
sys.exit(0 if not fails else 1)
