#!/usr/bin/env python3
"""
#372: the general-path word STORE ignored cpu->byte_order.

The general path's word-store arm was UNCONDITIONALLY EMPTY -- its guard was
`!A__B && !A__H && HOST_LITTLE_ENDIAN` and its only body was `#ifdef A__STRD`,
but A__STRD implies A__H, which the guard excludes. So a plain word STR on an LE
host emitted no bytes and memory_rw copied the register's HOST bytes to guest
memory, never consulting byte order. The FAST path's word arm has always been
order-aware, so one STR wrote guest order to a WARM page and host order to a
COLD one -- the #342/#355 self-contradiction class -- and every `strt`, which is
general-path on its first access per page (#366), was reversed.

Measured before the fix on -E barearm: a cold store of 0x11223344 read back
0x44332211. After #372's fix: 0x11223344.

THIS PROBE RUNS BOTH BYTE ORDERS.
  * The BE rig is `-E barearm`, whose MACHINE_SETUP sets EMUL_BIG_ENDIAN outright
    (machine_test.c) -- no config file, no ELF, no stub-order wrinkle. Its rows
    are the DISCriminators.
  * The LE rig is plain `-E testarm`. On LE the broken code was ACCIDENTALLY
    RIGHT (host order == guest order), so the LE rows discriminate NOTHING about
    this fix: they are INVARIANCE CONTROLS, present to catch a fix that repairs
    BE by breaking LE (mutant M1 shows that is a live possibility -- see the
    round's mutation record).

The cold/warm pair is the whole argument: same instruction word, same value,
same addr[1:0], differing ONLY in the seeding of the target page -- which pins
the defect to A__NAME__general rather than to `str` in general. The four `ldrb`
witnesses are the purest form, because a byte load has no byte order (data[0] in
both branches), so they expose the raw memory layout with no dependence on the
word-load path; their `buggy` column is the exact reverse of `arch`, so the two
mirror-image groups cannot both be satisfied by a swapped expectation table.

r1 = 0x11223344 is built with immediates, never loaded -- a load would add its
own general-path access. COLD = 0x20000 is seeded with NOTHING (unseeded RAM is
zero and provably cold; stronger than `put b`, which carries a device-arm
warming caveat). WARM = 0x10000 is seeded with `put w`, which warms host_load
AND host_store (MMU off => ok-1==1 => writeflag set). Every encoding below was
verified through the emulator's own `unassemble`, the standing rule.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
CODE = 0x8000
WARM = 0x10000
COLD = 0x20000

#  Build r1 = 0x11223344 with immediates (mov + 3 orr), verified via unassemble.
BUILD_R1 = [0xE3A01411, 0xE3811822, 0xE3811C33, 0xE3811044]
MOV_R0_WARM = 0xE3A00801        # mov r0,#0x10000
MOV_R0_COLD = 0xE3A00802        # mov r0,#0x20000
STR_R1_R0 = 0xE5801000          # str  r1,[r0]
LDR_R2_R0 = 0xE5902000          # ldr  r2,[r0]
LDRB = (0xE5D03000, 0xE5D04001, 0xE5D05002, 0xE5D06003)  # ldrb r3..r6,[r0,#0..3]
SPIN = 0xEAFFFFFE               # b .


def store_prog(base_mov):
    return BUILD_R1 + [base_mov, STR_R1_R0, LDR_R2_R0] + list(LDRB) + [SPIN]


def run(machine, be_stub, prog, regs):
    #  A raw stub just makes the machine construct. barearm lays no LE halt stub
    #  of its own (unlike testarm), so nothing decodes as garbage post-flip.
    stub = "/tmp/gx_endian_%s.bin" % machine
    order = ">I" if machine == "barearm" else "<I"
    import struct
    with open(stub, "wb") as f:
        f.write(struct.pack(order, 0xE1A00000))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A", "-E", machine, "-M", "64",
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
            if len(buf) > mark and buf[mark:].rstrip().endswith("GXemul>"):
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
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    #  Seed the WARM page (put w warms it), leave COLD untouched.
    send("put w 0x%x, 0x00000000" % WARM)
    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)
    send("step %d" % (len(prog) - 1))    # straight-line, ends at the spin

    out = {}
    for rn in regs:
        mark = len(buf)
        send("print %s" % rn)
        m = re.search(r"(?m)^0x([0-9a-fA-F]+)\s*$", buf[mark:])
        if m:
            out[rn] = int(m.group(1), 16)
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    return out


#  (name, machine, base_mov, reg, arch, buggy)   buggy = the pre-#372 value.
#  On the LE machine arch == buggy by construction (host order == guest order):
#  those rows are INVARIANCE controls, not discriminators.
ROWS = [
    #  BE discriminators -----------------------------------------------------
    ("be warm word", "barearm", MOV_R0_WARM, "r2", 0x11223344, 0x11223344),
    ("be cold word", "barearm", MOV_R0_COLD, "r2", 0x11223344, 0x44332211),
    ("be cold byte0", "barearm", MOV_R0_COLD, "r3", 0x11, 0x44),
    ("be cold byte1", "barearm", MOV_R0_COLD, "r4", 0x22, 0x33),
    ("be cold byte2", "barearm", MOV_R0_COLD, "r5", 0x33, 0x22),
    ("be cold byte3", "barearm", MOV_R0_COLD, "r6", 0x44, 0x11),
    #  LE invariance controls ------------------------------------------------
    ("le warm word", "testarm", MOV_R0_WARM, "r2", 0x11223344, 0x11223344),
    ("le cold word", "testarm", MOV_R0_COLD, "r2", 0x11223344, 0x11223344),
    ("le cold byte0", "testarm", MOV_R0_COLD, "r3", 0x44, 0x44),
    ("le cold byte1", "testarm", MOV_R0_COLD, "r4", 0x33, 0x33),
    ("le cold byte2", "testarm", MOV_R0_COLD, "r5", 0x22, 0x22),
    ("le cold byte3", "testarm", MOV_R0_COLD, "r6", 0x11, 0x11),
]

print("=== #372: general-path word STORE must honour cpu->byte_order ===")
print("    BE rows DISCriminate; LE rows are INVARIANCE controls (host==guest)")

#  Control: the BE cold-word row must return a distinctive nonzero, proving the
#  barearm rig constructed, the program ran and the store+load happened, before
#  any DISC verdict is believed. A wrong register field reads 0.
control = "FAIL"
ngot = 0
for name, machine, base, reg, arch, buggy in ROWS:
    got = run(machine, machine == "barearm", store_prog(base), [reg])
    if got is None or reg not in got:
        print("%-20s DEAD  FAIL" % name)
        continue
    v = got[reg]
    ok = (v == arch)
    ngot += ok
    if name == "be warm word" and v == 0x11223344:
        control = "OK"
    #  Only the FIVE cold BE rows discriminate #372: they enter the general
    #  store path, which was the buggy one. `be warm word` is a BE row but takes
    #  the order-aware FAST path, so it is green on both the buggy and fixed
    #  builds -- it is the rig CONTROL, not a discriminator, and labelling it
    #  DISC was a precision slip. All six LE rows are invariance controls.
    kind = "DISC" if (machine == "barearm" and "cold" in name) else "CTRL"
    print("%-20s %-4s %s=0x%08x want 0x%08x (buggy 0x%08x)  %s"
          % (name, kind, reg, v, arch, buggy, "ok" if ok else "FAIL"))

print("ENDIAN_CONTROL=%s" % control)
print("ENDIAN_RESULT=%d/%d" % (ngot, len(ROWS)))
