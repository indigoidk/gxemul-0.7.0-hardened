#!/usr/bin/env python3
"""Gate 14's netbsd_memcpy instrument (#354), read-ahead install path.

Prints one line per row:  <name> <got> <want> ok|FAIL
then MEMCPY_CONTROL=OK|DEAD and MEMCPY_RESULT=<passed>/<total>.
gate_arm.sh does the asserting.

The defect (#354): X(netbsd_memcpy) folds the NetBSD/arm memcpy loop
(ldmia r1!,{r3,r4,ip,lr} / stmia r0!,{...} x2 / subs r2,#0x20 / bge). It did
memcpy(dst,src,32) per iteration and advanced r0/r1, but NEVER wrote
r3/r4/ip/lr -- which the architecture leaves holding the LAST 16 bytes loaded
(the final iteration's second ldmia). So after a memcpy the guest read four
stale registers. #354 publishes them from page_1+(addr_r1&0xffc)+16, before the
memcpy, direct read no byteswap (matching multi_0x08b15018).

Read-ahead ON (no breakpoint): COMBINE(netbsd_memcpy) installs the fold on the
first ldmia when the bge is translated ahead of execution, so one forward pass
reaches it (the fold is #ifdef HOST_LITTLE_ENDIAN -- active on x86).

Owed words are FULL-WIDTH and distinct per register (Opus's round-101 note): an
accidental byteswap or a wrong register index is then self-evident, not hidden
behind single-byte values.
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
SRC = 0x9100
DST = 0x9300            # clear of SRC+64


def prog(r2seed):
    return [
        0xE3A00C93,             # 0  mov r0,#0x9300   dst
        0xE3A01C91,             # 1  mov r1,#0x9100   src
        r2seed,                 # 2  mov r2,#imm      counter
        0xE3A03033,             # 3  mov r3,#0x33     stale sentinels
        0xE3A04044,             # 4  mov r4,#0x44
        0xE3A0C0CC,             # 5  mov ip,#0xcc
        0xE3A0E0EE,             # 6  mov lr,#0xee
        0xE8B15018,             # 7  L: ldmia r1!,{r3,r4,ip,lr}
        0xE8A05018,             # 8  stmia r0!,{r3,r4,ip,lr}
        0xE8B15018,             # 9  ldmia r1!,{r3,r4,ip,lr}
        0xE8A05018,             # 10 stmia r0!,{r3,r4,ip,lr}
        0xE2522020,             # 11 subs r2,r2,#0x20
        0xAAFFFFF9,             # 12 bge L (word 7)  -> arms the combiner
        0xE5873000,             # 13 ic[6]: str r3,[r7]
        0xE5874004,             # 14 str r4,[r7,#4]
        0xE587C008,             # 15 str ip,[r7,#8]
        0xE587E00C,             # 16 str lr,[r7,#12]
        0xE5870010,             # 17 str r0,[r7,#16]
        0xE5871014,             # 18 str r1,[r7,#20]
        0xEAFFFFFE,             # 19 b .   park
    ]


def session(r2seed, srcwords, extra):
    with open(STUB, "wb") as f:
        f.write((0xe1a00000).to_bytes(4, "little"))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-A"] + extra +
                  ["-E", "testarm", "-M", "64", "0x%x:%s" % (CODE, STUB)])
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

    def send(s):
        mark = len(buf)
        b = (s + "\n").encode("latin1")
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
    for i, w in enumerate(srcwords):
        send("put w 0x%x, 0x%08x" % (SRC + 4 * i, w))
    for i in range(6):
        send("put w 0x%x, 0xdeadbeef" % (DEST + 4 * i))
    #  #359: pre-fill the COPY DESTINATION with a sentinel unlike any source
    #  word, so a word the fold never wrote is unmistakable rather than
    #  indistinguishable from zeroed RAM. 16 words covers both the one- and
    #  two-iteration programs.
    for i in range(16):
        send("put w 0x%x, 0xbaadf00d" % (DST + 4 * i))
    send("r7=0x%x" % DEST)
    for i, iw in enumerate(prog(r2seed)):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < 2.0:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith(">")):
        os.write(fd, b"\x03")
        if not wait_from(cmark, 15):
            try:
                os.kill(pid, 9); os.waitpid(pid, 0)
            except Exception:
                pass
            return None
    flat = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 24))
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        flat = "".join(words).split()
        if len(flat) >= 6:
            break
        time.sleep(1.0); rd(1.0)
    #  NB the teardown that used to sit here moved BELOW the destination dump.
    #  Left in place it killed the emulator first, so the new dump read nothing
    #  and every destination row scored DEAD -- a probe defect that looks
    #  exactly like a dead fold.
    #  #359: read back the COPY DESTINATION itself. Everything above this point
    #  reads registers, and registers cannot see how many BYTES the fold moved:
    #  the handler publishes r3/r4/ip/lr from a direct page read that does not
    #  go through its memcpy call, and advances r0/r1 unconditionally. Measured
    #  consequence -- a build whose fold copies 16 of every 32 bytes passed this
    #  probe 12/12 and the whole of gate 14 at 243 checks. Sampling the
    #  destination is the only assertion in the suite that reads FAIL on it.
    dstw = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DST, DST + 64))
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        dstw = "".join(words).split()
        if len(dstw) >= 16:
            break
        time.sleep(1.0); rd(1.0)
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    if len(flat) < 6:
        return None
    regs = [int.from_bytes(bytes.fromhex(x), "little") for x in flat[:6]]
    dst = [int.from_bytes(bytes.fromhex(x), "little") for x in dstw[:16]]
    return regs + [dst]


rows = []


def row(name, kind, got, want):
    ok = (got == want)
    rows.append(ok)
    g = ("0x%08x" % got) if isinstance(got, int) else str(got)
    w = ("0x%08x" % want) if isinstance(want, int) else str(want)
    print("%-24s %-12s %-12s %s %s" % (name, g, w, kind, "ok" if ok else "FAIL"))


#  Source: 16 distinct full-width words (64 bytes) so both iteration rows read
#  distinct owed blocks and a byteswap/wrong-index is self-evident.
SRCW = [0x1A2A3A40 + i for i in range(16)]   # word k at SRC+4k

#  ---- control: -J (no combining) must fold NOTHING, so the guest runs the
#  genuine ldmia/stmia and r3/r4/ip/lr get the architectural values. If this
#  reference is wrong the probe measured nothing.
_c = session(0xE3A02000, SRCW, ["-J"])       # r2=0, one iteration
control = "OK" if (_c is not None and _c[0] == SRCW[4]) else "DEAD"
print("MEMCPY_CONTROL=%s" % control)
if control != "OK":
    print("MEMCPY_RESULT=0/0")
    sys.exit(0)

#  ---- row 1: r2=0 -> ONE iteration. Owed r3/r4/ip/lr = the 2nd ldmia's block
#  = SRC+16..+28 = words 4..7. r0/r1 advance by 0x20.
_1 = session(0xE3A02000, SRCW, [])
for nm, got, want, kind in (
        ("A memcpy 1it r3", _1[0] if _1 else None, SRCW[4], "DISC"),
        ("A memcpy 1it r4", _1[1] if _1 else None, SRCW[5], "DISC"),
        ("A memcpy 1it ip", _1[2] if _1 else None, SRCW[6], "DISC"),
        ("A memcpy 1it lr", _1[3] if _1 else None, SRCW[7], "DISC"),
        ("A memcpy 1it r0", _1[4] if _1 else None, DST + 0x20, "PIN"),
        ("A memcpy 1it r1", _1[5] if _1 else None, SRC + 0x20, "PIN")):
    row(nm, kind, got, want)

#  #359: the BYTES. Every row above reads registers, and registers cannot see
#  how much the fold actually copied -- r3/r4/ip/lr come from a direct page read
#  that bypasses the memcpy call, and r0/r1 advance unconditionally. A build
#  whose fold copied 16 of every 32 bytes was measured passing this probe 12/12
#  and gate 14 at all 243 checks. These are PIN, not DISC: the genuine
#  ldmia/stmia copies the same bytes, so the destination is identical folded or
#  not. What they discriminate is a BROKEN copy, which nothing else here can see.
#  The word at index 6 is the discriminator for a halved copy (it sits in the
#  second 16 bytes of the 32-byte iteration); the tail word catches the opposite
#  mistake, a fold that copies MORE than it was asked to.
_d1 = _1[6] if _1 else None
for nm, idx, want in (("A memcpy 1it dst w1", 1, SRCW[1]),
                      ("A memcpy 1it dst w6", 6, SRCW[6]),
                      ("A memcpy 1it dst tail", 8, 0xBAADF00D)):
    row(nm, "PIN", (_d1[idx] if _d1 and len(_d1) > idx else None), want)

#  ---- row 2: r2=0x20 -> TWO iterations (Opus: 0x40 is THREE, bge branches on
#  N==V regardless of Z). Owed = the final iteration's 2nd ldmia = SRC+48..+60
#  = words 12..15. r0/r1 advance by 0x40.
_2 = session(0xE3A02020, SRCW, [])
for nm, got, want, kind in (
        ("A memcpy 2it r3", _2[0] if _2 else None, SRCW[12], "DISC"),
        ("A memcpy 2it r4", _2[1] if _2 else None, SRCW[13], "DISC"),
        ("A memcpy 2it ip", _2[2] if _2 else None, SRCW[14], "DISC"),
        ("A memcpy 2it lr", _2[3] if _2 else None, SRCW[15], "DISC"),
        ("A memcpy 2it r0", _2[4] if _2 else None, DST + 0x40, "PIN"),
        ("A memcpy 2it r1", _2[5] if _2 else None, SRC + 0x40, "PIN")):
    row(nm, kind, got, want)

#  #359: bytes again, but deep in the SECOND iteration. A mutation that copies
#  the right amount on the first pass and less on later ones, or that mis-steps
#  the source pointer between iterations, shows up here and not above. Index 14
#  is in the final 16 bytes of the 64-byte copy, and no sentinel should survive.
_d2 = _2[6] if _2 else None
for nm, idx, want in (("A memcpy 2it dst w9", 9, SRCW[9]),
                      ("A memcpy 2it dst w14", 14, SRCW[14])):
    row(nm, "PIN", (_d2[idx] if _d2 and len(_d2) > idx else None), want)

print("MEMCPY_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
