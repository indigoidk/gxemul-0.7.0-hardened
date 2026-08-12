#!/usr/bin/env python3
"""Gate 11 section 2's instrument: the m88k idle fold vs bcnd.n's delay slot.

#380: COMBINE(idle)'s arm 3 matched tb1/ld/bcnd.n but installed the handler
written for the PLAIN-bcnd sequence, so the bcnd.n delay slot -- which the
architecture executes once per branch, taken or not (MC88100 UM p. 1-4
sec 1.2.5, p. 3-26 sec 3.3.2, p. 3-35) -- ran ZERO times per taken iteration.
On loop exit it ran once, so every post-loop witness (boot markers, exit
registers) shows NO divergence; the witness must observe the delay slot's
side effect DURING the spin. This probe's guest program makes the slot a
store: `st r5,r7,0` -- the stored word IS the witness.

    0x10010  f020d8ff   tb1  1,r0,0xff      ; verbatim from the guest image
    0x10014  15a20000   ld   r13,r2,0x0     ; r2 = the spin word's address
    0x10018  ec4dfffe   bcnd.n eq0,r13,-8   ; verbatim from the guest image
    0x1001c  24a70000   st   r5,r7,0x0      ; DELAY SLOT = the witness store

Layout facts (each placement is load-bearing -- a pass-1 seat derived the
false-green routes):
* The machine is testm88k, free-running (`continue`), NO breakpoints, no -t,
  no -i: translation read-ahead then translates the whole loop while the
  tb1's own translation is still on the stack, the fold installs at the tb1,
  and the FIRST dispatched instruction is already the fold -- the real
  bcnd_n_eq0 never runs. With any breakpoint set there is no read-ahead, the
  first iteration runs the real branch handler, the slot executes once, and
  the taken row reads 0x11111111 on the BUGGY build -- an invisible
  non-reproduction. The MUTANT row is what proves install-beat-execution
  empirically (a fold that lost the race fails loudly there, never silently).
* The SPIN WORD lives in the CODE page (0x10100): pc_to_pointers populates
  host_load for the code page before the first dispatch, so the fold's fast
  path is live on its very first call (a spin word on a cold page would take
  the p==NULL fallback into the faithful sequence -- false green).
* DEST (r7 = 0x20000) is on a DIFFERENT page: a guest store to the code page
  would invalidate the loop's own translations at every idle break.
* All seeding happens BEFORE pc= and continue, so no translation exists yet
  for the seed writes to invalidate.

Rows (the gate asserts the fixed strings):
  taken    spin=0  committed=deadbeef (slot never ran)  fixed=11111111
  taken-J  spin=0  0x11111111 on EVERY build (-J disables combinations; this
                   is the route-3 reference proving program+store reachable)
  untaken  spin=1  0x11111111 on EVERY build (the loop exits through the
                   slot; execution then falls into 0x00000000 and the
                   emulator aborts to the prompt -- expected noise)
Counters (tlbdump; ABSENT output parses as DEAD, never as zero):
  committed build: DEAD (the counters do not exist pre-#380)
  fixed:  installs[2]>=1, n_taken_n>=1, slot_runs>=1
  mutant: installs[2]>=1, n_taken_plain>=1, n_taken_n==0 (the two taken
          counters are deliberately distinct so the mutant cannot blind its
          own diagnostics)

Output: M380_ROW=<name> RESULT=PASS|FAIL got=<hex> want=<hex>, then
M380_COUNTERS=<installs0/1/2,ntp,ntn,slot,ds | DEAD>, M380_RESULT=n/t.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else "all"   # taken|takenj|untaken|all

CODE = 0x10010
SPIN = 0x10100          # same 4 KB page as CODE -- load-bearing, see docstring
DEST = 0x20000          # different page -- load-bearing
PROG = (0xf020d8ff, 0x15a20000, 0xec4dfffe, 0x24a70000)


def run(spin_value, extra_argv, grace):
    #  A one-word raw stub so the machine constructs (m88k is big-endian).
    import struct
    stub = "/tmp/gx_m88k_idle_%d.bin" % os.getpid()
    with open(stub, "wb") as f:
        f.write(struct.pack(">I", 0xf4005800))      # or r0,r0,r0 (nop)
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V"] + extra_argv +
                  ["-E", "testm88k", "-M", "64", "0x10000:%s" % stub])
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
            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False

    def send(sx, timeout=30):
        mark = len(buf)
        b = (sx + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait_from(mark, timeout)
        return mark

    if not wait_from(0, 60):
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None, None

    for i, w in enumerate(PROG):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    send("put w 0x%x, 0x%08x" % (SPIN, spin_value))
    send("put w 0x%x, 0xdeadbeef" % DEST)
    send("r2=0x%x" % SPIN)
    send("r5=0x11111111")
    send("r7=0x%x" % DEST)
    send("pc=0x%x" % CODE)

    #  Free-run. The taken row idles (no prompt returns): grace, then ^C.
    #  The untaken row aborts to the prompt on its own (falls into zeroes).
    mark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        rd(0.3)
    if not buf[mark:].rstrip().endswith("GXemul>"):
        os.write(fd, b"\x03")
        wait_from(len(buf), 15)

    #  Read DEST back, parse bound to the 16-byte-aligned line address
    #  (width follows c->is_32bit -- 8 digits on this 32-bit CPU, but the
    #  0x[0-9a-f]* prefix tolerates either). m88k is BIG-endian: memory
    #  order == value spelling.
    addr_tail = "%x" % (DEST & ~0xf)
    val = None
    for _ in range(3):
        mark = send("dump 0x%x 0x%x" % (DEST, DEST + 8))
        for line in buf[mark:].splitlines():
            m = re.match(r"\s*0x[0-9a-f]*" + addr_tail +
                         r"\s+((?:[0-9a-f]{8}\s*)+)", line)
            if m:
                val = int.from_bytes(bytes.fromhex(m.group(1).split()[0]), "big")
                break
        if val is not None:
            break
        time.sleep(1.0)
        rd(1.0)

    #  Counters (absent on pre-#380 builds -> DEAD, never zero).
    mark = send("tlbdump")
    cm = re.search(r"idle_fold installs=(\d+)/(\d+)/(\d+) n_taken_plain=(\d+)"
                   r" n_taken_n=(\d+) slot_runs=(\d+) in_delayslot=(\d+)",
                   buf[mark:])
    counters = tuple(int(x) for x in cm.groups()) if cm else None

    try:
        os.write(fd, b"quit\n"); time.sleep(0.3)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return val, counters


#  name, spin value, extra argv, grace seconds, expected DEST (fixed build)
ROWS = [
    ("taken",   0, [],     4.0, 0x11111111),
    ("takenj",  0, ["-J"], 4.0, 0x11111111),
    ("untaken", 1, [],     4.0, 0x11111111),
]

passed = total = 0
last_counters = None
for name, spin, argv, grace, want in ROWS:
    if ONLY != "all" and ONLY != name:
        continue
    total += 1
    got, counters = run(spin, argv, grace)
    if name == "taken":
        last_counters = counters
    ok = (got == want)
    passed += ok
    print("M380_ROW=%s RESULT=%s got=%s want=%08x" % (
        name, "PASS" if ok else "FAIL",
        ("%08x" % got) if got is not None else "None", want))

if last_counters is None:
    print("M380_COUNTERS=DEAD")
else:
    print("M380_COUNTERS=installs:%d/%d/%d,ntp:%d,ntn:%d,slot:%d,ds:%d"
          % last_counters)
print("M380_RESULT=%d/%d" % (passed, total))
