#!/usr/bin/env python3
"""Gate 14's netbsd strlen-fold instrument (#355 alias guard, #356 budget bound).

Prints one line per row:  <name> <got> <want> ok|FAIL
then STRLEN_CONTROL=OK|DEAD and STRLEN_RESULT=<passed>/<total>.
gate_arm.sh does the asserting.

Two defects, both measured on the committed build before the fix:

  #355  COMBINE(strlen) pinned the load's destination to r3 and its immediate
        to 1 but never required base != dest. With `ldrb r3,[r3,#1]!` the
        genuine writeback overwrites the loaded byte, so `cmps r3,#0` compares
        an ADDRESS -- never zero -- and the loop runs on; the fold's condition
        tests the local byte and EXITS at the first NUL. The encoding is
        UNPREDICTABLE in the architecture, so neither answer is "wrong" --
        but this emulator was giving two different answers for one program,
        selected by whether the combination happened, and -J is gate 14's own
        architectural oracle. Pre-fix: folded exits (sentinel 0x55).

  #356  The walk had no budget bound: it ran to the end of the string inside
        ONE dispatch, so the host was unresponsive for the duration and
        n_translated_instrs (an int, reset per run_instr, and this walk is
        REPLAYABLE) was drivable into signed overflow with ~18-24 MB of
        non-NUL memory at the default -M 64.

HOW THE YIELD IS WITNESSED WITHOUT A CLOCK.  `testarm` carries the `mp` test
device; its NCYCLES register at 0x110000d0 returns cpu->ninstrs, and ninstrs is
committed only when run_instr RETURNS. So a guest that samples it either side of
a long walk reads ~0 if the whole walk stayed inside one dispatch, and a real
count if the fold yielded and the dispatcher went round again. Wall-clock timing
would not be acceptable in a gate; this is deterministic.

BANDS, NOT COUNTS -- and the real reason is staleness, not the constants.  The
numbers do depend on N_SAFE_DYNTRANS_LIMIT (8191) and the 120-dispatch group,
but the dominant imprecision is that ninstrs is committed only when run_instr
RETURNS, so the guest's second sample is stale by up to one batch. Measured on a
1 MB walk: folded 3,144,852 against an architectural 3n = 3,145,728 (0.99972),
-J genuine 3,138,120 (0.99758) -- deficits of 876 and 7608, both inside one
batch (69 x 120 = 8280). The mp register's own comment calls its value
"approximately the number of cycles" for the same reason.

CONSEQUENCE, stated so nobody over-reads these rows: this probe CANNOT verify
the 3n-1 billing constant to better than about 8K instructions. What these rows
prove is that the walk yields at all (0 vs not-0) and that the total is the
right order of magnitude. The exactness of 3n-1 rests on the source derivation
plus that 1 MB differential above, not on any row here.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]

CODE = 0x8000
DEST = 0x9000
STRBASE = 0x10000
STRLEN = 0x4000                 # 16 KB of non-NUL; NUL at STRBASE+STRLEN
ALIAS_STR = 0x9100              # short string for the #355 row

#  --- the #356 walk: base r4, dest r3 (distinct -- post-#355 the aliased form
#  --- is refused, so the yield row must use a genuine strlen shape).
PROG_WALK = [
    0xE3A07C90,   # 0  mov r7,#0x9000       publish base
    0xE3A08411,   # 1  mov r8,#0x11000000   mp device
    0xE28880D0,   # 2  add r8,r8,#0xd0      -> NCYCLES
    0xE5986000,   # 3  ldr r6,[r8]          D = ninstrs before
    0xE3A04801,   # 4  mov r4,#0x10000
    0xE2444001,   # 5  sub r4,r4,#1         first pre-indexed load hits 0x10000
    0xE5F43001,   # 6  S: ldrb r3,[r4,#1]!
    0xE3530000,   # 7  cmps r3,#0
    0x1AFFFFFC,   # 8  bne S                arms COMBINE(strlen)
    0xE5989000,   # 9  ldr r9,[r8]          E = ninstrs after
    0xE5876000,   # 10 str r6,[r7]
    0xE5879004,   # 11 str r9,[r7,#4]
    0xE5874008,   # 12 str r4,[r7,#8]       end address -- must be 0x14000
    0xEAFFFFFE,   # 13 b .
]

#  --- the #355 row: base == dest == r3. Publishes a sentinel ONLY if the loop
#  --- was exited, plus r3 itself so a program that never ran cannot pass by
#  --- looking like "still looping" (the forward-progress assertion).
PROG_ALIAS = [
    0xE3A07C90,   # 0 mov r7,#0x9000
    0xE3A03C91,   # 1 mov r3,#0x9100        base == dest
    0xE3A05055,   # 2 mov r5,#0x55          sentinel
    0xE5F33001,   # 3 S: ldrb r3,[r3,#1]!
    0xE3530000,   # 4 cmps r3,#0
    0x1AFFFFFC,   # 5 bne S
    0xE5875000,   # 6 str r5,[r7]           reached only if the loop EXITED
    0xE5873004,   # 7 str r3,[r7,#4]        r3 for the progress assertion
    0xEAFFFFFE,   # 8 b .
]


def session(prog, extra, nwords, grace, load_str, read_r3=False):
    """Run one read-ahead-ON session. Returns the published words, plus r3 read
    from the DEBUGGER when read_r3 is set.

    r3 must come from `reg`, not from a guest store: on the #355 row the loop
    never exits post-fix, so any store placed after the loop is unreachable and
    an assertion made through it could never pass. (That was the first version
    of the progress row here, and it failed for exactly that reason -- a row
    that cannot pass is the mirror of a row that cannot fail, and this harness
    retires both.)"""
    stub = "/tmp/gx_strlen_stub.bin"
    with open(stub, "wb") as f:
        f.write((0xe1a00000).to_bytes(4, "little"))
    args = [BIN, "-V", "-A"] + extra + ["-E", "testarm", "-M", "64",
                                        "0x%x:%s" % (CODE, stub)]
    if load_str:
        s = "/tmp/gx_strlen_str.bin"
        with open(s, "wb") as f:
            f.write(b"\xff" * STRLEN + b"\x00" * 4)
        args.append("0x%x:%s" % (STRBASE, s))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, args)
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

    def wait_from(mark, timeout=40):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if len(buf) > mark and buf[mark:].rstrip().endswith(">"):
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
    if not load_str:
        #  "AB\0" for the alias row.
        send("put w 0x%x, 0x00424101" % ALIAS_STR)
    for i in range(nwords):
        send("put w 0x%x, 0xdeadbeef" % (DEST + 4 * i))
    for i, iw in enumerate(prog):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, iw))
    send("pc=0x%x" % CODE)
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith(">")):
        os.write(fd, b"\x03")
        if not wait_from(cmark, 20):
            try:
                os.kill(pid, 9); os.waitpid(pid, 0)
            except Exception:
                pass
            return None
    flat = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 4 * nwords))
        w = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", buf[mark:])
        flat = "".join(w).split()
        if len(flat) >= nwords:
            break
        time.sleep(1.0); rd(1.0)
    r3 = None
    if read_r3:
        mark = len(buf)
        send("reg")
        m = re.search(r"\br3 = 0x([0-9a-f]+)", buf[mark:])
        if m:
            r3 = int(m.group(1), 16)
    try:
        os.write(fd, b"quit\n"); time.sleep(0.2)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    if len(flat) < nwords:
        return None
    vals = [int.from_bytes(bytes.fromhex(x), "little") for x in flat[:nwords]]
    return (vals, r3) if read_r3 else vals


rows = []


def row(name, kind, got, want):
    ok = (got == want)
    rows.append(ok)
    print("%-26s %-14s %-14s %s %s" % (name, got, want, kind,
                                       "ok" if ok else "FAIL"))


def band(v, lo, hi):
    return "in[%d,%d]" % (lo, hi) if (v is not None and lo <= v <= hi) \
        else ("%s" % v)


#  ---- control: -J must fold nothing, so the genuine walk yields a real
#  ---- NCYCLES delta and ends exactly at the NUL. Nothing below is believable
#  ---- if this reference is wrong.
_j = session(PROG_WALK, ["-J"], 3, 8.0, True)
#  The control deliberately does NOT test the end address: that is the
#  `-J end addr` row's job, and a control that already required it would make
#  the row unfailable -- the mirror of the rule this file commits to.
ctrl_ok = (_j is not None and (_j[1] - _j[0]) > 0)
print("STRLEN_CONTROL=%s" % ("OK" if ctrl_ok else "DEAD"))
if not ctrl_ok:
    print("STRLEN_RESULT=0/0")
    sys.exit(0)

#  These two restate what STRLEN_CONTROL already required, so whenever they
#  print they pass -- they are decorative in the pass direction and exist to put
#  the reference numbers in the log beside the folded ones. The real protection
#  is the control itself: if either condition fails, control goes DEAD, the
#  probe prints 0/0, and the gate fails loudly on both the control check and
#  `rows run`.
row("A strlen -J ref", "PIN", band(_j[1] - _j[0], 30000, 60000),
    "in[30000,60000]")
row("A strlen -J end addr", "PIN", "0x%05x" % _j[2],
    "0x%05x" % (STRBASE + STRLEN))

#  ---- #356: the folded walk must ALSO show a real delta -- i.e. it left the
#  ---- dispatch at least once. Pre-fix this read 0: the whole 16 KB walk
#  ---- happened inside one dispatch.
_f = session(PROG_WALK, [], 3, 8.0, True)
#  These two rows read ONE datum between them -- `yields` is its lower bound,
#  `bill band` its upper. The LOWER bound is what discriminates: pre-fix it read
#  0 (the walk never left the dispatch), and an add-clamp-only counterfeit --
#  one that trims the billing while the walk still completes in a single
#  dispatch -- also reads far below it. The UPPER bound only catches a fix that
#  bills wildly too much.
row("A strlen yields", "DISC",
    band((_f[1] - _f[0]) if _f else None, 30001, 10 ** 9), "in[30001,1000000000]")
row("A strlen bill band", "DISC",
    band((_f[1] - _f[0]) if _f else None, 30000, 90000), "in[30000,90000]")
#  ...and bounded above: an add-clamp-only "fix" (no loop bound) reads far
#  lower because the walk still completes in one dispatch and only the
#  BILLING is trimmed.
row("A strlen end addr", "PIN",
    ("0x%05x" % _f[2]) if _f else "dead", "0x%05x" % (STRBASE + STRLEN))

#  ---- #355: the aliased loop must NOT be folded, so it must not exit. The
#  ---- sentinel must be absent AND r3 must have moved off its seed -- the
#  ---- second half is the forward-progress assertion, so a program that never
#  ---- armed or never ran cannot masquerade as "still looping".
#  -T (halt on a non-existent memory access) is REQUIRED here, and #355 is what
#  made it so: post-fix the aliased loop no longer exits, so it marches off the
#  end of RAM and every subsequent byte logs a WARNING. Measured without it:
#  164,668 lines / 12.0 MB into the pty in ~0.94 s, accumulated in `buf` and
#  re-sliced on every poll, with r3 host-speed-dependent (console-throttled ~3x
#  slower than free-running). With -T: 1 warning, 132 bytes, r3 deterministic at
#  0x0403FFFF, and the discrimination is untouched -- pre-fix still exits with
#  the sentinel at 0x55 and r3 at 0x9103. (-q cannot be used: main.c ignores it
#  whenever -V is given.)
_ar = session(PROG_ALIAS, ["-T"], 2, 3.0, False, read_r3=True)
_a, _ar3 = _ar if _ar else (None, None)
row("A strlen alias exits", "DISC",
    ("0x%08x" % _a[0]) if _a else "dead", "0xdeadbeef")
#  DISC, not PIN: pre-fix the fold EXITED after three bytes, so r3 sat at
#  0x9103 and this reads "no". Post-fix the guest walks on for millions of
#  bytes. It doubles as the forward-progress guard -- a program that never
#  armed, or never ran at all, cannot masquerade as "still looping".
row("A strlen alias moved", "DISC",
    ("moved" if (_ar3 is not None and _ar3 > ALIAS_STR + 16) else "no"),
    "moved")

print("STRLEN_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
