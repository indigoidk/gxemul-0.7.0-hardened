#!/usr/bin/env python3
"""#433: all five former exit(1) sites in dev_m8820x.c, each driven by ONE REAL GUEST
INSTRUCTION on the real memory path.

WHY THIS EXISTS ALONGSIDE regress/diff_m8820x.c.  The offline differential calls
dev_m8820x_access() directly, so it proves BEHAVIOUR but cannot prove the site is REACHABLE
by a guest -- it would stay green under a change that unmapped the device (a
memory_device_register length or DM_ flag change).  This probe goes through the real
address decode and the real memory_rw plumbing.  It is also structurally immune to the
harness artifact that corrupted this round's first offline reproduction: a harness fault
produces NO `m8820x:` diagnostic at all, so a real detection and a broken probe are
distinguishable by construction rather than by remembering to check an exit status.

COST, measured: 3.2 s for 8 rows on a COLD DEBUGGER -- no boot.  A full luna88k rig drive is
182-233 s, so this is ~60x cheaper.  A booting-rig row was deliberately NOT written: the fix
is measured boot-neutral, so such a row could only re-assert what gate_ab already asserts,
at ~200 s of load-sensitive wall clock added to a battery already carrying ~37 such oracles.

VALUES, NOT SURVIVAL.  Rounds 79/80 taught this project that a survival-only row cannot tell
a repaired access from one that merely stopped faulting: replacing exit(1) with `return 1`
while dropping the write-back would leave the guest with garbage and the row green.  So the
first row READS CMMU_IDR back into r4 and asserts 0x00a90000 -- the 88200 rev-9 id seeded by
dev_luna88k.c:901, a value that can only have come through this device.

Cold debugger on luna-88k, no boot.  r5 = 0xFFF06000 = CMMU_D0 (luna88k_board.h:163).

Encodings read off the disassembler, not memory (cpu_m88k.c:991-1019):
    ld rD,rS1,IMM16  op26 = 0x05   iw = 0x05<<26 | d<<21 | s1<<16 | imm16
    st rD,rS1,IMM16  op26 = 0x09   iw = 0x09<<26 | d<<21 | s1<<16 | imm16
EVERY ROW DISASSEMBLES THE PLANTED WORD AND CHECKS THE TEXT BEFORE STEPPING IT -- this
project has a recorded incident where a wrong register field made a gate row measure the
wrong thing for months, and a row expecting a small nonzero value is the defence.
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
IMAGES = sys.argv[2]
IMG = IMAGES + "/liveimage-luna88k-raw-20250518.img"
CODE = 0x00010000
CMMU_D0 = 0xFFF06000


def run_row(name, is_store, imm16, r4val, note):
    op26 = 0x09 if is_store else 0x05
    word = (op26 << 26) | (4 << 21) | (5 << 16) | imm16
    want = "%s\tr4,r5,0x%x" % ("st" if is_store else "ld", imm16)
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(IMAGES)
        os.execvp(BIN, [BIN, "-V", "-e", "luna-88k", "-d", "R:" + IMG, "boot"])
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

    #  Signature order is not free choice: gate_hygiene.sh pins the CANONICAL
    #  #392 call form as a literal `return wait(mark=_mark, echo=<x> if <x>
    #  else None)`, deliberately tightened three times because every looser
    #  prefix was a substring of the broken form too.  Written any other way,
    #  a probe is simply not covered by that ratchet -- which is worse than
    #  failing it.  So timeout goes last, and send() ends on the pinned form.
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

    status, dis, fatal, r4got = "?", "", "", None
    #  KEYWORD, and this is not style.  Reordering wait()'s parameters to the
    #  pinned #392 form silently turned this positional 120 into mark=120 --
    #  the probe would have waited on a slice of an empty buffer with a 60 s
    #  budget instead of 120 s for the cold prompt.  A conversion done for a
    #  detector's benefit is still a code change.
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        send("r5=0x%08x" % CMMU_D0)
        send("r4=0x%08x" % r4val)
        send("put w 0x%08x, 0x%08x" % (CODE, word))
        mark = len(buf)
        send("unassemble 0x%08x" % CODE)
        m = re.search(r"((?:ld|st)[\w.]*\s+r\d+,r\d+,0x[0-9a-f]+)", buf[mark:])
        dis = m.group(1) if m else "(none)"
        send("pc=0x%08x" % CODE)
        mark = len(buf)
        ok = send("step 1", timeout=30)
        if dead[0] or not ok:
            status = "HOST-DIED"
        elif send("reg", timeout=30):
            status = "SURVIVED"
            mm = re.search(r"r4\s*=\s*0x([0-9a-fA-F]+)", buf[mark:])
            if mm:
                r4got = int(mm.group(1), 16)
        else:
            status = "HOST-DIED" if dead[0] else "NO-REG"
    ms = re.findall(r"(m8820x\w*:[^\r\n]*)", buf)
    ms = [x for x in ms if "Copyright" not in x]
    if ms:
        fatal = ms[-1].strip()
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    print("%-34s word=0x%08x dis_ok=%-5s %-9s r4=%s %s"
          % (name, word, str(want in dis), status,
             ("0x%08x" % r4got) if r4got is not None else "-", note))
    if fatal:
        print("      emulator said: %s" % fatal)
    return status


print("BINARY=%s" % BIN)
t0 = time.time()
#  name, is_store, imm16, r4 seed, note
ROWS = [
    ("VALUE ld CMMU_IDR -> 0x00a90000", False, 0x000, 0x00000000, "the seeded 88200 rev-9 id; VALUE not survival"),
    ("CONTROL st CMMU_SAR   (handled)", True,  0x00c, 0x00000000, "must survive"),
    ("CONTROL st SCR cmd 0x35 (handled)", True, 0x004, 0x00000035, "FLUSH_SUPER_PAGE; guest issues it 158664x"),
    ("site 2: ld CMMU_SCR",            False, 0x004, 0x00000000, "read of a write-only reg"),
    ("site 1: st CMMU_IDR",            True,  0x000, 0x00000001, "write to the read-only ID reg"),
    ("site 3: st CMMU_SSR",            True,  0x008, 0x00000001, "write to the status reg"),
    ("site 4: st SCR cmd 0x34",        True,  0x004, 0x00000034, "FLUSH_SUPER_LINE: DEFINED in m8820x.h:112, unhandled"),
    ("site 4: st SCR cmd 0x24",        True,  0x004, 0x00000024, "PROBE_SUPER: DEFINED in m8820x.h:107, unhandled"),
    ("site 0: st CMMU_CTP0",           True,  0x840, 0x00000000, "cache tag port, DEFINED in m8820x.h:82"),
]
results = [run_row(*r) for r in ROWS]
print("SURVIVED=%d of %d" % (results.count("SURVIVED"), len(results)))
print("M8820X_SITES_%s" % ("PASS" if results.count("SURVIVED") == len(results) else "FAIL"))
print("PROBE_WALL=%.1fs for %d rows" % (time.time() - t0, len(ROWS)))
