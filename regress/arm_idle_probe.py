#!/usr/bin/env python3
"""Gate 14's netbsd_idle instrument (#351/#352/#353), read-ahead install path.

Prints one line per row:  <name> <got> <want> ok|FAIL
then IDLE_CONTROL=OK|DEAD and IDLE_RESULT=<passed>/<total>.
gate_arm.sh does the asserting.

Why this is a SEPARATE probe from arm_flags_probe.py
----------------------------------------------------
arm_flags_probe.py drives every combiner row with a debugger `breakpoint`, and
that is a blind spot a round-100 review seat found by compiling: translation
read-ahead is gated on `cpu->machine->breakpoints.n == 0` (cpu_dyntrans.c:1939),
so a breakpoint turns read-ahead OFF and the fold is only ever installed by the
two-pass EXECUTE path. Real guests set no breakpoint, so they take the
read-ahead path -- where COMBINE(beq_etc) installs netbsd_idle BEFORE the ldr
runs, and the very first fold execution reads a destination register the loop
has not yet written. netbsd_idle's register-alias defect (c) is invisible to a
breakpoint-driven probe because the two-pass install pre-writes that register.

So every row here runs with NO breakpoint (read-ahead ON) and one straight-line
pass. The architectural reference for the flag/dest rows is the SAME program run
with `-J` (instruction combining disabled), so nothing folds -- measured, not
derived.

The four netbsd_idle defects (all measured live on committed 704036e)
--------------------------------------------------------------------
  (a) the fold never wrote the load destination -> stale register.
  (b) the fold never wrote the flags -> stale N/Z though two teqs executed.
  (c) a loop whose second teqs ALIASES the load dest exited where the
      architecture idles (the matcher pins rZ != rY but not rZ != dest; the
      fold read the stale dest). #351 subsumes it by writing the dest before
      the teqs delegation reads it.
  (d) a FORWARD beq matched the loop and HUNG the guest (the matcher never
      pinned the branch target). #353 pins ic[0].arg[0] == &ic[-4].
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
MEM = 0x9100


def bcond(cond, frm, to):
    """B<cond> from program word `frm` to word `to` (target = frm+8+imm*4)."""
    return (cond << 28) | 0x0A000000 | ((to - frm - 2) & 0xFFFFFF)


#  ldr r2,[r0] / teqs / bne->X / teqs rZ / beq->L, then ic[5] and X.
def prog_exit(rz_reg, flag_seed):
    """rZ != 0 exit path (rz_reg seeded 0x80000000). Publishes dest (r2) and
    the post-loop cpsr, both via stores on the fold's exit path (ic[5..])."""
    return [
        0xE3A07C90,             # 0 mov r7,#0x9000
        0xE3A09001,             # 1 mov r9,#1
        0xE3A00C91,             # 2 mov r0,#0x9100     rY
        0xE3A02077,             # 3 mov r2,#0x77       dest seed
        0xE3A04102,             # 4 mov r4,#0x80000000 rZ seed (bit31)
        flag_seed,              # 5 cmp r9,#imm        flag preset
        0xE5902000,             # 6 L: ldr r2,[r0]
        0xE3320000,             # 7 teqs r2,#0
        bcond(1, 8, 14),        # 8 bne -> X
        0xE3300000 | (rz_reg << 16),   # 9 teqs rZ,#0
        bcond(0, 10, 6),        # 10 beq -> L
        0xE10F3000,             # 11 ic[5]: mrs r3,cpsr
        0xE5872000,             # 12 str r2,[r7]
        0xE5873004,             # 13 str r3,[r7,#4]
        0xEAFFFFFE,             # 14 X: b .
    ]


def prog_idle(flag_seed):
    """rZ == 0 idle path. The guest IDLES on both builds (rZ genuinely 0), so
    this row discriminates on the published dest and flags, not control flow.
    The flag seed is chosen with Z CLEAR so the owed Z=1 differs from it."""
    p = prog_exit(4, flag_seed)
    p[4] = 0xE3A04000           # mov r4,#0  -> rZ = 0 -> idle path
    return p


PROG_ALIAS = [                  # (c): second teqs tests r2, the load dest
    0xE3A07C90,   # 0 mov r7,#0x9000
    0xE3A00C91,   # 1 mov r0,#0x9100
    0xE3A02077,   # 2 mov r2,#0x77     dest == rZ, seeded nonzero
    0xE3A05055,   # 3 mov r5,#0x55     sentinel
    0xE5902000,   # 4 L: ldr r2,[r0]
    0xE3320000,   # 5 teqs r2,#0
    bcond(1, 6, 10),   # 6 bne -> X
    0xE3320000,   # 7 teqs r2,#0        rZ aliases the dest
    bcond(0, 8, 4),    # 8 beq -> L
    0xE5875000,   # 9 ic[5]: str r5,[r7]   <- fold's WRONG exit
    0xEAFFFFFE,   # 10 X: b .
]

PROG_TARGET = [                 # (d): the beq targets FORWARD, not the ldr
    0xE3A07C90,   # 0 mov r7,#0x9000
    0xE3A00C91,   # 1 mov r0,#0x9100
    0xE3A02077,   # 2 mov r2,#0x77
    0xE3A05055,   # 3 mov r5,#0x55
    0xE5902000,   # 4 L: ldr r2,[r0]
    0xE3320000,   # 5 teqs r2,#0
    bcond(1, 6, 10),   # 6 bne -> X
    0xE3340000,   # 7 teqs r4,#0        r4=0 -> beq taken
    bcond(0, 8, 11),   # 8 beq -> B (FORWARD, word 11) -- not a loop
    0xEAFFFFFE,   # 9 b .
    0xEAFFFFFE,   # 10 X: b .
    0xE5875000,   # 11 B: str r5,[r7]   arch reaches here
    0xEAFFFFFE,   # 12 b .
]


def session(prog, extra, verbose=False, grace=2.0):
    """One read-ahead-ON run; return (dumpwords, regtext, transcript)."""
    with open(STUB, "wb") as f:
        for w in prog:
            f.write(w.to_bytes(4, "little"))
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

    def kill():
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass

    #  Wait for a prompt AFTER a given buffer mark -- never the whole buffer.
    #  A stale prompt already in `buf` must not satisfy a later wait (Codex's
    #  round-100 finding); the round-99 nonmult witness learned the same.
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
        kill()
        return None, None, buf
    send("put w 0x%x, 0x0" % MEM)
    send("put w 0x%x, 0xdeadbeef" % DEST)
    send("put w 0x%x, 0xdeadbeef" % (DEST + 4))
    if verbose:
        send("verbosity cpu 3")
        send("verbosity cpu")
    send("pc=0x%x" % CODE)
    #  Free-run with NO breakpoint (read-ahead ON). The (d) row hangs by
    #  design, so continue may never return; grace-then-^C, and if the prompt
    #  does not come back, terminate rather than queue dump/reg into a live
    #  session (which would time out ~60 s each).
    cmark = len(buf)
    os.write(fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        rd(0.3)
    if not (len(buf) > cmark and buf[cmark:].rstrip().endswith(">")):
        os.write(fd, b"\x03")
        if not wait_from(cmark, 15):
            kill()
            return None, None, buf
    #  Retry the dump READ, never the row: a dump can straggle past the prompt
    #  detector under host load (arm_flags_probe.py documents this same race).
    flat = []
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (DEST, DEST + 8))
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})",
                           buf[mark:])
        flat = "".join(words).split()
        if len(flat) >= 2:
            break
        time.sleep(1.0)
        rd(1.0)
    mark = len(buf)
    send("reg")
    regtxt = buf[mark:]
    os.write(fd, b"quit\n")
    time.sleep(0.2)
    kill()
    return flat, regtxt, buf


def sw(h):
    return int.from_bytes(bytes.fromhex(h), "little")


def dumpw(flat, i):
    return sw(flat[i]) if flat and len(flat) > i else None


def nzcv_from_reg(regtxt):
    m = re.search(r"cpsr = ([NnZzCcVv]{4})", regtxt or "")
    if not m:
        return None
    f = m.group(1)
    return sum(1 << (3 - i) for i, ch in enumerate(f) if ch.isupper())


def reg(regtxt, rn):
    m = re.search(r"\b%s = 0x([0-9a-f]+)" % rn, regtxt or "")
    return int(m.group(1), 16) if m else None


MARK = re.compile(r"cpu netbsd_idle: combined")

rows = []


def row(name, kind, got, want):
    ok = (got == want)
    rows.append(ok)
    g = ("0x%08x" % got) if isinstance(got, int) else str(got)
    w = ("0x%08x" % want) if isinstance(want, int) else str(want)
    print("%-26s %-12s %-12s %s %s" % (name, g, w, kind, "ok" if ok else "FAIL"))


#  ---- control: the rig must execute guest code, and -J must fold nothing ----
#  If the -J architectural reference for the exit path is not dest=0/NZCV=0xA,
#  the probe has measured nothing and no row may be believed.
_flat, _reg, _ = session(prog_exit(4, 0xE3590001), ["-J"])
_ctrl_dest = dumpw(_flat, 0)
_ctrl_nzcv = (dumpw(_flat, 1) >> 28) & 0xF if dumpw(_flat, 1) is not None else None
control = "OK" if (_ctrl_dest == 0 and _ctrl_nzcv == 0xA) else "DEAD"
print("IDLE_CONTROL=%s" % control)
if control != "OK":
    print("IDLE_RESULT=0/0")
    sys.exit(0)

#  ---- (a)/(b) exit path: dest and flags, read-ahead ON ----------------------
#  flag seed cmp r9,#1 -> 0x6 (Z=1,C=1); owed after teqs(0x80000000) is
#  N=1 Z=0 C=1 V=0 = 0xA -- every N/Z bit moves off the seed.
_flat, _reg, _ = session(prog_exit(4, 0xE3590001), [])
row("A idle exit dest", "DISC", dumpw(_flat, 0), 0)
row("A idle exit flags", "DISC",
    (dumpw(_flat, 1) >> 28) & 0xF if dumpw(_flat, 1) is not None else None, 0xA)

#  ---- idle path: rZ = 0, distinct flag seed with Z CLEAR --------------------
#  cmp r9,#2 (r9=1) -> 1-2 = N=1 Z=0 C=0 V=0 = 0x8; owed idle flags are
#  Z=1 N=0 C=0 (C preserved from the seed) = 0x4. Guest idles on both builds.
_flat, _reg, _ = session(prog_idle(0xE3590002), [])
row("A idle path dest", "DISC", reg(_reg, "r2"), 0)
row("A idle path flags", "DISC", nzcv_from_reg(_reg), 0x4)

#  ---- (c) register-alias: fixed IDLES, buggy EXITS (sentinel 0x55) ----------
#  want == 0xdeadbeef is the DEST prefill, i.e. "the exit store never ran", not
#  a self-evidently-non-seed value -- so this row's anti-vacuity rests on the
#  IDLE_CONTROL bail and the `alias -J ref` PIN below (which fix the program's
#  architectural answer as idle). Pre-fix it measures 0x55; keep it beside those
#  two guards (Opus's round-100 note).
_flat, _reg, _ = session(PROG_ALIAS, [])
row("A idle alias exits", "DISC", dumpw(_flat, 0), 0xdeadbeef)   # deadbeef = idled

#  ---- (d) forward beq: fixed REACHES B (0x55), buggy HANGS (deadbeef) -------
_flat, _reg, _ = session(PROG_TARGET, [])
row("A idle target reached", "DISC", dumpw(_flat, 0), 0x55)

#  ---- #352 marker: fires on the exit path under verbosity, quiet by default -
_flat, _reg, vbuf = session(prog_exit(4, 0xE3590001), [], verbose=True)
fires = ("yes" if MARK.search(vbuf or "") else "no") \
    if "3: DEBUG" in (vbuf or "") else "no-verb"
row("A idle fires", "DISC", fires, "yes")
_flat, _reg, qbuf = session(prog_exit(4, 0xE3590001), [])
row("A idle quiet", "PIN", "%d" % (len(MARK.findall(qbuf or ""))), "0")

#  ---- architectural reference: the alias program under -J (combining OFF) must
#  idle, so the `alias exits` DISC above attributes its buggy 0x55 to the FOLD
#  and not to the program being wrong. This is a reference PIN, not a proof of
#  the read-ahead-install mechanism -- the straight-line `fires` row is that
#  proof (a marker on a single forward pass can only appear if the fold was
#  installed ahead of execution).  -----------------------------------------
_flat, _reg, _ = session(PROG_ALIAS, ["-J"])
row("A idle alias -J ref", "PIN", dumpw(_flat, 0), 0xdeadbeef)

print("IDLE_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
