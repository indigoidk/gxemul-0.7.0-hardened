#!/usr/bin/env python3
"""WITNESS (rung 3) for `lunaabsentcpu`: dev_luna88k.c reassert_interrupts() walks all MAX_CPUS
slots and calls INTERRUPT_ASSERT(d->cpu_irq[cpu]) -- a direct call through a function pointer
that DEVINIT connected only for configured CPUs (`if (devinit->machine->ncpus >= 2)` ...).  On
the default ONE-cpu luna-88k a guest word store to INT_ST_MASK1 (0x65000004) arms slot 1
(`d->interrupt_enable[cpunr] = idata` with no ncpus check), and a following store to SOFT_INT1
(0x69000004) sets that slot's bit 26 and calls reassert_interrupts() SYNCHRONOUSLY inside the
store -- so the NULL callback is reached while single-stepping, no host timer needed.

ONE cold-debugger session, real m88k guest instructions (st/ld through real address decode and
real memory_rw), COMMITTED UNMODIFIED machine description (-e luna-88k + the committed rig
image; no device_add, no new machine, nothing introduced in order to reach the site).

Attribution controls, in order:  C1 RAM liveness through the same decode;  C2 device signature
(the handler's own >>8 on MASK0);  A1 the SAME two-store sequence on the CONNECTED slot 0
(MASK0 bit 26 + SOFT_INT0) SURVIVES -- so a death on slot 1 is the absent slot, not the assert
path;  A2 the MASK1 store ALONE survives (no pending bit yet) -- so the death needs the
pending bit, which is what the reading predicts;  W1 THE WITNESS: SOFT_INT1 store with
MASK1 armed.  Pre-fix: the emulator process dies inside W1.  Post-fix: survives, and C3 RAM
liveness afterwards proves the machine still executes.

Machinery copied from regress/luna_intmask_probe.py (rung-3 exemplar for this device).
Encodings (cpu_m88k.c, same source as regress/m8820x_sites_probe.py):
    ld rD,rS1,IMM16  op26=0x05 ;  st rD,rS1,IMM16  op26=0x09
EVERY PLANTED WORD IS DISASSEMBLED AND ITS TEXT CHECKED BEFORE IT IS STEPPED.

usage: luna_absentcpu_probe.py <gxemul-binary> <images-dir>
"""
import os, pty, re, select, sys, time

BIN     = sys.argv[1]
IMAGES  = sys.argv[2]
IMG     = IMAGES + "/liveimage-luna88k-raw-20250518.img"
CODE    = 0x00010000
SCRATCH = 0x00020000
MASK0   = 0x65000000        # INT_ST_MASK0 -- the LITERAL, deliberately not the #define
SOFT0   = 0x69000000        # SOFT_INT0


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
    return wait(mark=_mark, echo=x if x else None, timeout=timeout)


def r4():
    global buf
    mark = len(buf)
    if not send("reg", timeout=30):
        return None
    m = re.search(r"r4\s*=\s*0x([0-9a-fA-F]+)", buf[mark:])
    return int(m.group(1), 16) if m else None


fails = []
rows = []


def row(label, result, note=""):
    rows.append((label, result))
    print("LUNAABS_ROW=%-10s RESULT=%-9s %s" % (label, result, note))


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


def host_status():
    """After a death: what did the child say / how did it exit."""
    try:
        _, st = os.waitpid(pid, os.WNOHANG)
        if os.WIFSIGNALED(st):
            return "signal %d" % os.WTERMSIG(st)
        if os.WIFEXITED(st):
            return "exit %d" % os.WEXITSTATUS(st)
    except Exception as e:
        return "unknown (%s)" % e
    return "still running?"


def finish(verdict, code):
    print("LUNA_ABSENTCPU_WITNESS=%s" % verdict)
    print("LUNAABS_RESULT=%d/%d" % (sum(1 for _, r in rows if r == "OK"), len(rows)))
    print("PROBE_WALL=%.1fs" % (time.time() - t0))
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
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
    finish("FAIL (encoding)", 2)

send("r6=0x%08x" % SCRATCH)

print("C1 LIVENESS -- plain RAM through the same decode:")
send("r4=0x12345678")
step_at(A_WRAM)
send("r4=0x00000000")
step_at(A_RRAM)
row("live", "OK" if check("C1 RAM readback", r4(), 0x12345678) else "BADREGS")

print("C2 DEVICE SIGNATURE -- MASK0: the handler's own >>8; RAM cannot produce this:")
send("r5=0x%08x" % MASK0)
send("r4=0xfc000000")
step_at(A_WDEV)
send("r4=0x00000000")
if not step_at(A_RDEV):
    row("devsig", "NOSTART", "host died on a LEGAL MASK0 read -- the probe itself is broken")
    finish("FAIL (probe)", 2)
g = r4()
row("devsig", "OK" if check("C2 read INT_ST_MASK0 after write 0xfc000000", g, 0x00fc0000, 0x00ffffff) else "BADREGS")

print("A1 ATTRIBUTION -- the SAME two-store sequence on the CONNECTED slot 0 must survive:")
print("   MASK0 already holds 0xfc000000 (bit 26 set); store 1 to SOFT_INT0 -> reassert -> slot 0 asserts")
send("r5=0x%08x" % SOFT0)
send("r4=0x00000001")
if not step_at(A_WDEV):
    row("slot0", "HALT", "host died asserting the CONNECTED cpu 0 -- attribution control FAILED (%s)" % host_status())
    finish("FAIL (control: connected slot died)", 2)
send("r4=0x00000000")
step_at(A_RDEV)                         # reading SOFT_INT0 clears it (and deasserts)
g = r4()
row("slot0", "OK" if check("A1 SOFT_INT0 readback (the stored 1; read clears it)", g, 0x00000001) else "BADREGS")

print("A2 THE MASK1 STORE ALONE -- arms the ABSENT slot 1; no pending bit yet, must survive:")
send("r5=0x%08x" % (MASK0 + 4))
send("r4=0xfc000000")
if not step_at(A_WDEV):
    row("mask1", "HALT", "host died on the MASK1 store alone (%s) -- a machine-wide status bit was already pending" % host_status())
    print("SYMPTOM=DEATH_ON_MASK1_STORE")
    finish("PRE_FIX_SYMPTOM (on the arming store)", 1)
send("r4=0x00000000")
step_at(A_RDEV)
g = r4()
row("mask1", "OK" if g is not None else "BADREGS", "MASK1 readback 0x%08x (as-is => 0x00fc0000 in 23..0; a decline => 0)" % (g if g is not None else 0))

print("W1 THE WITNESS -- SOFT_INT1 store: slot 1's bit 26 becomes pending, enable has it, irqActive clear")
print("   -> INTERRUPT_ASSERT(d->cpu_irq[1]) through a NULL interrupt_assert on a one-cpu machine")
send("r5=0x%08x" % (SOFT0 + 4))
send("r4=0x00000001")
if not step_at(A_WDEV):
    st = host_status()
    m = re.findall(r"\[[^\r\n]*luna88k[^\r\n]*\]", buf)
    row("soft1", "HALT", "HOST DIED (%s); last device line: %s" % (st, m[-1] if m else "(none)"))
    print("SYMPTOM=NULL_CALLBACK_ON_ABSENT_CPU")
    print("  this is the PRE-FIX symptom, on a committed unmodified one-cpu luna-88k, reached by two ordinary word stores.")
    finish("PRE_FIX_SYMPTOM", 1)
send("r4=0x00000000")
step_at(A_RDEV)
g = r4()
row("soft1", "OK", "survived; SOFT_INT1 readback 0x%08x" % (g if g is not None else 0))

print("C3 LIVENESS AGAIN -- the machine still executes:")
send("r4=0x0badf00d")
step_at(A_WRAM)
send("r4=0x00000000")
step_at(A_RRAM)
row("live2", "OK" if check("C3 RAM readback", r4(), 0x0badf00d) else "BADREGS")

for m in re.findall(r"\[[^\r\n]*luna88k[^\r\n]*\]", buf):
    print("  emulator said: %s" % m)
finish("PASS" if not fails else ("FAIL " + "; ".join(fails)), 0 if not fails else 1)
