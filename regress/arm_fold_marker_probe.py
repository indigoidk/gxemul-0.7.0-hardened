#!/usr/bin/env python3
"""#358: fold-fired markers for netbsd_copyin / netbsd_copyout.

WHY THESE TWO FOLDS AND WHY NOW. Both replace six user-mode transfers with one C
function whose registers, read/written addresses and instruction billing are
IDENTICAL to the instructions they replace, so a row asserting their result
passes whether or not the fold ever fires. Until #357 there was exactly one
witness: the load/store template masked its base writeback while these folds did
not, so an unaligned base gave r0 = 0x10019 folded against 0x10018 genuine.
#357 corrected the template -- the folds were right all along -- and that
one-bit detector disappeared with it. These two folds also had NO harness rows of
any kind, so #358 adds the marker and this probe adds the first rows.

THE ROWS ARE FREE-RUNNING, AND THAT IS NOT A STYLE CHOICE. Three measured facts,
each of which independently breaks a plausible-looking row:

  - STEPPING UN-FOLDS THE SLOT. A `step` onto a fold slot re-translates it
    UNCOMBINED, so the step executes a plain instruction and no marker appears.
    A row driven with `step` therefore measures the genuine sequence while
    believing it measured the fold. (This is also why an earlier pc-stride
    experiment here read pc + 4: not "a breakpoint suppresses the fold", which
    was the first guess, but stepping destroying the thing it would measure.)
  - A BREAKPOINT INSIDE THE LOOP GIVES ZERO FOLDS ON A HEALTHY BINARY. Measured
    over 8 passes: breakpoint after the sequence gives 1 matcher install and 7
    folds; breakpoint inside gives 8 installs and 0 folds, because the block is
    re-translated every pass. That row would read exactly like a dead fold, and
    the signature is invisible without instrumenting the matcher.
  - A BREAKPOINT ANYWHERE DISABLES READ-AHEAD, so the combiner installs only
    AFTER the entry slot has already dispatched once, making the fold count
    `passes - 1` rather than `passes`. Any row's expected count must be a number
    derived from that rule, never "greater than zero".

A breakpoint ON the entry slot is worse still: that path re-marks its own slot
for retranslation and the matchers test ic[i].f, so a fold can never install
there at all.

TWO PASSES ARE REQUIRED. The folds gate on is_userpage, which only an access
carrying the user-access flag sets -- and that access is the general handler the
fold's own bail-out delegates to. So pass 1 always runs genuinely and sets the
bit; only pass 2 and later can fold.

PAGE LAYOUT IS LOAD-BEARING. The user page must differ from the code page,
because instruction translation updates the code page's entry WITHOUT the user
flag and the translation layer clears the bit before re-setting it. Code 0x8000,
user data 0x10000 (loads) / 0x11000 (stores), and nothing is published to memory.
Measured deterministic: 5 consecutive runs gave identical results.

EACH FOLD GETS A PAIR, so neither row can be vacuous in either direction:
  fires (DISC) -- combining on, marker present, AND the verbosity echo present.
                  The echo matters: a session whose verbosity raise silently
                  failed would report zero markers and look exactly like a dead
                  fold, so a row that only counted markers could pass for the
                  wrong reason. It also asserts the six transferred values, so
                  the row proves the work happened, not merely that a line was
                  printed.
  quiet (PIN)  -- default verbosity, zero markers. Must use continue/free-run,
                  NEVER `step`: single-step BYPASSES the verbosity gate, so a
                  stepped session prints markers at default verbosity and this
                  row would fail for a reason that has nothing to do with the
                  fold.

Proven non-vacuous before shipping, on a scratch tree built from this exact
source with ONLY this fold's arming line removed and combining otherwise
enabled: markers 0 with the arming gone, 1 with it present, verbosity confirmed
raised in both. That isolates the fold's own arming rather than all combining,
which `-J` alone would not.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
LOADSRC = 0x10000          # user page read by copyin
STOREDST = 0x11000         # user page written by copyout

#  Every encoding below was confirmed through the emulator's own `unassemble`
#  before use. The six-transfer register ORDER is fixed by the matchers, which
#  pin each transfer's register, and by the arming iword of the sixth.
#    copyin : ldrt sl,fp,r6,r7,r8,r9 from [r0],#4   arming 0xe4b09004
#    copyout: strt r8,r9,sl,fp,r6,r7 to  [r1],#4    arming 0xe4a17004
COPYIN = [
    0xE3A03001,   # mov  r3,#1            two passes
    0xE3A00801,   # L: mov r0,#0x10000    user page, distinct from code
    0xE4B0A004,   # ldrt sl,[r0],#4       <- fold entry slot
    0xE4B0B004,   # ldrt fp,[r0],#4
    0xE4B06004,   # ldrt r6,[r0],#4
    0xE4B07004,   # ldrt r7,[r0],#4
    0xE4B08004,   # ldrt r8,[r0],#4
    0xE4B09004,   # ldrt r9,[r0],#4       arms COMBINE(netbsd_copyin)
    0xE2533001,   # subs r3,r3,#1
    0x5AFFFFF6,   # bpl -> word 1
    0xEAFFFFFE,   # b .
]

COPYOUT = [
    0xE3A03001,   # mov  r3,#1
    0xE3A01A11,   # L: mov r1,#0x11000    user page for the stores
    0xE4A18004,   # strt r8,[r1],#4       <- fold entry slot
    0xE4A19004,   # strt r9,[r1],#4
    0xE4A1A004,   # strt sl,[r1],#4
    0xE4A1B004,   # strt fp,[r1],#4
    0xE4A16004,   # strt r6,[r1],#4
    0xE4A17004,   # strt r7,[r1],#4       arms COMBINE(netbsd_copyout)
    0xE2533001,   # subs r3,r3,#1
    0x5AFFFFF6,   # bpl -> word 1
    0xEAFFFFFE,   # b .
]


def session(prog, verbose, seed_regs=None, extra=None):
    """Free-running two-pass session. Returns (marker_count, verb_took, regs)."""
    stub = "/tmp/r104f_stub.bin"
    with open(stub, "wb") as f:
        f.write((0xE1A00000).to_bytes(4, "little"))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A"] + (extra or []) +
                  ["-E", "testarm", "-M", "64", "0x%x:%s" % (CODE, stub)])
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

    def send(sx, timeout=30):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait_from(mark, timeout)
        return buf[mark:]

    if not wait_from(0, 60):
        os.kill(pid, 9); os.waitpid(pid, 0)
        return None

    for i in range(8):
        send("put w 0x%x, 0x%08x" % (LOADSRC + 4 * i, 0x11223344 + i))
    for r, v in (seed_regs or {}).items():
        send("%s=0x%x" % (r, v))
    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)
    if verbose:
        send("verbosity cpu 3")

    #  The program parks in `b .`, so `continue` never returns a prompt on its
    #  own and every later command would sit out its own timeout -- the first
    #  revision of this probe took minutes per session and had to be killed.
    #  Let it free-run briefly (both passes finish in microseconds; the fold
    #  needs pass 2, so this must NOT be a breakpoint stop), then interrupt.
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < 2.0:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith(">")):
        os.write(fd, b"\x03")
        wait_from(cmark, 15)

    regs = {}
    for rn in ("sl", "fp", "r6", "r7", "r8", "r9", "r0", "r1"):
        mark = len(buf)
        send("print %s" % rn)
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            regs[rn] = int(m.group(1), 16)
    mem = []
    if prog is COPYOUT:
        mark = len(buf)
        send("dump 0x%x 0x%x" % (STOREDST, STOREDST + 24))
        w = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        mem = [int.from_bytes(bytes.fromhex(x), "little")
               for x in "".join(w).split()][:6]
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, regs, mem


def count(buf, name):
    return len([l for l in buf.splitlines() if "%s: combined" % name in l])


print("=== #358: fold-fired markers, netbsd_copyin / netbsd_copyout ===")
rows = []

#  ---- copyin ----------------------------------------------------------------
r = session(COPYIN, True)
if r is None:
    rows.append(("A fold copyin fires", "DISC", "DEAD", False))
else:
    buf, regs, _ = r
    n = count(buf, "netbsd_copyin")
    verb = "3: DEBUG" in buf
    #  The six loaded words prove the work happened; they hold folded or not,
    #  which is why they are part of the row rather than a row of their own.
    vals_ok = (regs.get("sl") == 0x11223344 and regs.get("fp") == 0x11223345
               and regs.get("r6") == 0x11223346 and regs.get("r9") == 0x11223349)
    rows.append(("A fold copyin fires", "DISC",
                 "markers=%d verb=%s vals=%s" % (n, verb, vals_ok),
                 n >= 1 and verb and vals_ok))

r = session(COPYIN, False)
if r is None:
    rows.append(("A fold copyin quiet", "PIN", "DEAD", False))
else:
    buf, _, _ = r
    n = count(buf, "netbsd_copyin")
    rows.append(("A fold copyin quiet", "PIN", "markers=%d" % n, n == 0))

#  ---- copyout ---------------------------------------------------------------
SEED = {"r6": 0x66660001, "r7": 0x77770002, "r8": 0x88880003,
        "r9": 0x99990004, "sl": 0xAAAA0005, "fp": 0xBBBB0006}
r = session(COPYOUT, True, seed_regs=SEED)
if r is None:
    rows.append(("A fold copyout fires", "DISC", "DEAD", False))
else:
    buf, regs, mem = r
    n = count(buf, "netbsd_copyout")
    verb = "3: DEBUG" in buf
    #  Store order is r8,r9,sl,fp,r6,r7 -- pinned by the matcher. Asserting the
    #  MEMORY makes a future permutation regression visible, which a
    #  register-only row could not see.
    want = [SEED["r8"], SEED["r9"], SEED["sl"],
            SEED["fp"], SEED["r6"], SEED["r7"]]
    mem_ok = (mem == want)
    rows.append(("A fold copyout fires", "DISC",
                 "markers=%d verb=%s mem=%s" % (n, verb, mem_ok),
                 n >= 1 and verb and mem_ok))

r = session(COPYOUT, False, seed_regs=SEED)
if r is None:
    rows.append(("A fold copyout quiet", "PIN", "DEAD", False))
else:
    buf, _, _ = r
    n = count(buf, "netbsd_copyout")
    rows.append(("A fold copyout quiet", "PIN", "markers=%d" % n, n == 0))

ngot = 0
for name, kind, detail, ok in rows:
    ngot += ok
    print("%-28s  %-4s %-40s %s" % (name, kind, detail, "ok" if ok else "FAIL"))
print("FOLDMARK_RESULT=%d/%d" % (ngot, len(rows)))
