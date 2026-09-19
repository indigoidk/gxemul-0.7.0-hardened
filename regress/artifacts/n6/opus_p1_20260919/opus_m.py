#!/usr/bin/env python3
"""n6 pass-1 MEASURING seat.  Same shape as regress/footbridge_sites_probe.py:
cold debugger, unmodified -E cats, MMU turned off by the guest, real guest words
stepped one at a time, registers read with `reg`.  No boot, no rig.

usage: opus_m.py <gxemul-binary> <four-byte-raw-stub>
"""
import os, pty, re, select, sys, time

BIN  = sys.argv[1]
STUB = sys.argv[2]
CODE = 0x00008000
DATA = 0x00009000
NOP  = 0xE1A00000

#  constants planted in RAM (the ARM immediate form cannot encode these)
CONSTS = {0x00: 0x11223344,   # liveness
          0x04: 0x12345678,
          0x08: 0x00002002,   # P  (brief: bits 1 and 13)
          0x0c: 0x60000000,   # Q  (brief: bits 29 and 30)
          0x10: 0x00ABCDEF}   # M3 width pattern

MMU_OFF = [(0x00, 0xEE110F10, "read CP15 c1"),
           (0x04, 0xE3C00001, "clear MMU enable bit"),
           (0x08, 0xEE010F10, "MMU OFF -> VA == PA")]

PRO = [(0x0c, 0xEE113F10, "C2: read CP15 c1 BACK"),
       (0x10, 0xE3A00442, "r0 = 0x42000000 footbridge base"),
       (0x14, 0xE3A04A09, "r4 = 0x9000 scratch RAM"),
       (0x18, 0xE5945000, "C1 liveness: ldr r5,[r4] -> 0x11223344"),
       (0x1c, 0xE5906000, "A1 devsig: ldr r6,[r0] VENDOR_ID -> 0x1011")]


def run(label, body):
    """body: list of (word, note) appended after the prologue at 0x20, 0x24, ..."""
    prog = [(o, w, c) for o, w, c in MMU_OFF + PRO]
    off = 0x20
    for w, c in body:
        prog.append((off, w, c))
        off += 4
    prog.append((off, NOP, "landing pad -- planted, never stepped"))

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
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

    status, regs, dis, stepped = "?", {}, [], 0
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        for o in sorted(CONSTS):
            send("put w 0x%08x, 0x%08x" % (DATA + o, CONSTS[o]))
        for o, w, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + o, w))
        send("pc=0x%08x" % CODE)
        status = "SURVIVED"
        for o, w, c in prog[:-1]:
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                dis.append("0x%02x 0x%08x  *** HOST DIED STEPPING THIS *** | %s"
                           % (o, w, c))
                break
            stepped += 1
            seg = buf[mark:]
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + o, w), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(NO STEP LINE)"
            dis.append("0x%02x 0x%08x  %-26s | %s" % (o, w, got, c))
        if status == "SURVIVED":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                for n in range(16):
                    mm = re.search(r"\br%d\s*=\s*0x([0-9a-fA-F]+)" % n, buf[mark:])
                    if mm:
                        regs[n] = int(mm.group(1), 16)
            else:
                status = "HOST-DIED" if dead[0] else "NO-REG"

    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        _, st = os.waitpid(pid, 0)
    except Exception:
        st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    sig  = os.WTERMSIG(st)    if st is not None and os.WIFSIGNALED(st) else None

    print("=" * 78)
    print("ARM %s" % label)
    print("  status=%s  exit=%s  signal=%s  stepped=%d" % (status, code, sig, stepped))
    print("  --- disassembly the emulator printed for each planted word ---")
    for d in dis:
        print("    " + d)
    if fatals:
        print("  --- footbridge diagnostics seen on the pty ---")
        for f in fatals:
            print("    " + f)
    else:
        print("  --- no footbridge diagnostic on the pty ---")
    if regs:
        print("  --- registers ---")
        print("    " + "  ".join("r%d=0x%08x" % (n, regs[n])
                                 for n in sorted(regs) if n <= 12))
    sys.stdout.flush()
    return {"status": status, "exit": code, "signal": sig, "regs": regs,
            "fatals": fatals, "dis": dis}


print("BINARY=%s" % BIN)
print("machine: -E cats (SA110), cold debugger, MMU disabled by the guest, no boot")
print("HEAD baseline: dev_footbridge.c == 408accf")
print()

OUT = {}

# ---------------- M1 -------------------------------------------------------
OUT["M1ctl"] = run("M1ctl  control: prologue only, nothing that can die",
                   [(NOP, "no device access after the prologue")])
OUT["M1_100"] = run("M1a    word read of +0x100 SDRAM_BA_MASK",
                    [(0xE5907100, "ldr r7,[r0,#256]  -- +0x100 SDRAM_BA_MASK"),
                     (NOP, "reached only if the read survives")])
OUT["M1_188"] = run("M1b    word read of +0x188 IRQ_ENABLE_SET (today)",
                    [(0xE5907188, "ldr r7,[r0,#392]  -- +0x188 IRQ_ENABLE_SET"),
                     (NOP, "reached only if the read survives")])
OUT["M1_18c"] = run("M1c    word read of +0x18c IRQ_ENABLE_CLEAR (sibling)",
                    [(0xE590718C, "ldr r7,[r0,#396]  -- +0x18c IRQ_ENABLE_CLEAR"),
                     (NOP, "reached only if the read survives")])

# ---------------- M2 -------------------------------------------------------
OUT["M2"] = run("M2     inertness of P and Q: raw status, write, status",
                [(0xE5901184, "ldr r1,[r0,#388]  IRQ_RAW_STATUS BEFORE  -> r1"),
                 (0xE5903180, "ldr r3,[r0,#384]  IRQ_STATUS BEFORE      -> r3"),
                 (0xE5942008, "ldr r2,[r4,#8]    r2 = P = 0x00002002"),
                 (0xE5802188, "str r2,[r0,#392]  IRQEnableSet <- P"),
                 (0xE5905180, "ldr r5,[r0,#384]  IRQ_STATUS after P     -> r5"),
                 (0xE5906184, "ldr r6,[r0,#388]  IRQ_RAW_STATUS after P -> r6"),
                 (0xE594200C, "ldr r2,[r4,#12]   r2 = Q = 0x60000000"),
                 (0xE5802188, "str r2,[r0,#392]  IRQEnableSet <- Q"),
                 (0xE5907180, "ldr r7,[r0,#384]  IRQ_STATUS after Q     -> r7"),
                 (0xE5908184, "ldr r8,[r0,#388]  IRQ_RAW_STATUS after Q -> r8"),
                 (NOP, "settling nop 1"), (NOP, "settling nop 2"),
                 (NOP, "settling nop 3"), (NOP, "settling nop 4"),
                 (0xE5909184, "ldr r9,[r0,#388]  IRQ_RAW_STATUS after 4 nops -> r9"),
                 (NOP, "")])

# ---------------- M3 -------------------------------------------------------
OUT["M3"] = run("M3     access width on a register that survives a read",
                [(0xE5942010, "ldr r2,[r4,#16]    r2 = 0x00ABCDEF"),
                 (0xE5802300, "str r2,[r0,#768]   TIMER_1_LOAD <- 0x00ABCDEF"),
                 (0xE5901300, "ldr r1,[r0,#768]   WORD read  +0x300 -> r1"),
                 (0xE5D03300, "ldrb r3,[r0,#768]  BYTE read  +0x300 -> r3"),
                 (0xE5D05301, "ldrb r5,[r0,#769]  BYTE read  +0x301 -> r5"),
                 (0xE5D06302, "ldrb r6,[r0,#770]  BYTE read  +0x302 -> r6"),
                 (0xE2808C03, "add r8,r0,#768     r8 = 0x42000300"),
                 (0xE1D890B0, "ldrh r9,[r8]       HALF read  +0x300 -> r9"),
                 (0xE1D8A0B2, "ldrh r10,[r8,#2]   HALF read  +0x302 -> r10"),
                 (NOP, "")])

print()
print("=" * 78)
print("RAW SUMMARY (values only; interpretation is in the report)")
for k in ("M1ctl", "M1_100", "M1_188", "M1_18c", "M2", "M3"):
    a = OUT[k]
    print("%-8s status=%-10s exit=%-5s signal=%-5s fatals=%s"
          % (k, a["status"], a["exit"], a["signal"], a["fatals"]))
for k in ("M2", "M3"):
    print("%s regs: %s" % (k, "  ".join("r%d=0x%08x" % (n, OUT[k]["regs"][n])
                                        for n in sorted(OUT[k]["regs"]) if n <= 12)))
print("OPUS_M_DONE")
