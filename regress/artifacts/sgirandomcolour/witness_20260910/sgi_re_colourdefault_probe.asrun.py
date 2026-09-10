#!/usr/bin/env python3
#
#  sgirandomcolour -- RUNG-3 WITNESS for dev_sgi_re.c horrible_getputpixel() colour-mode default.
#
#  THE DEFECT.  horrible_getputpixel() extracts `color_mode = mode & DE_MODE_TYPE_MASK' (mask 0xf0)
#  and switches on it during a PUT.  Four cases are implemented:
#    case DE_MODE_TYPE_CI:   buf[0] = *color;
#    case DE_MODE_TYPE_RGB:  buf[0] = *color >> 24; buf[1] = *color >> 16; buf[2] = *color >> 8; buf[3] = 0;
#    case DE_MODE_TYPE_RGBA: buf[0] = *color >> 24; buf[1] = *color >> 16; buf[2] = *color >> 8; buf[3] = *color;
#    case DE_MODE_TYPE_ABGR: buf[0] = *color; buf[1] = *color >> 8; buf[2] = *color >> 16; buf[3] = *color >> 24;
#  The `default:' arm executes:
#    buf[0] = random(); buf[1] = random(); buf[2] = random(); buf[3] = random();
#    fatal("[ put: color mode = 0x%x ]\n", color_mode);
#  and then allows the common tail to execute:
#    cpu->memory_rw(cpu, cpu->mem, tileptr + ofs, buf, bufdepth, MEM_WRITE, NO_EXCEPTIONS | PHYSICAL);
#  which writes the four host-PRNG bytes to guest memory.  fatal() does not exit.
#
#  REACHABILITY: 12 of the 16 nibbles reach default:, including the documented DE_MODE_TYPE_YCRCB
#  (0x000000f0 per crmfbreg.h) and reserved encodings such as 0x50.
#
#  POST-FIX BEHAVIOUR: an unhandled / unimplemented colour mode during a PUT declines and skips
#  writing to memory, leaving the destination pre-paint intact.
#
#  CONTRACT (vacuity-floor clause (e)) -- what this witness catches and what it does NOT:
#    CATCHES   the default arm assigning random() and storing it: `ycrcb put' and `reserved put'
#              expect the destination to remain unchanged (post-fix honest decline); on HEAD they
#              fail because host random() bytes overwrite the pre-painted sentinel.
#    DOES NOT  implement YCRCB colour space conversion or other colour modes; it witnesses the defect
#              on unhandled modes under ordinary bounds-correctness engineering.
#
#  usage: sgi_re_colourdefault_probe.py <gxemul-binary> [label]
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy_sgirand.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE      = 0x80001000
SCRATCH   = 0xa0001800
LIVE_VAL  = 0x5a5a5a5a

RE_LINEAR_A   = 0xb5001700
DE_MODE_SRC   = 0xb5002000
DE_MODE_DST   = 0xb5002008
DE_DRAWMODE   = 0xb5002018
DE_XVERTEX_0  = 0xb5002070
DE_XVERTEX_1  = 0xb5002074
DE_XFER_ADDR  = 0xb50020a0
DE_FG         = 0xb50020d0
DE_XFER_STEPX = 0xb50020a8
DE_PRIM_START = 0xb5002860

MODE_RGBA     = 0x1220        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RGBA  0x20
MODE_YCRCB    = 0x12f0        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_YCRCB 0xf0
MODE_RESERVED = 0x1250        # LIN_A 0x1000 | BUFDEPTH_32 0x200 | TYPE_RESV  0x50
DRAWMODE_SOLID = 0x000000f8   # PLANEMASK 0x80 | BYTEMASK 0x78 (solid fill, no XFER/ROP/STIP)
PRIM_RECT     = 0x03020000    # DE_PRIM_RECTANGLE 0x03000000 | DE_PRIM_TB 0x00020000

TILE_PHYS     = 0x10000       # re_linear_a[0] = 0x10 -> physical 0x10000
DST_KSEG1     = 0xa0000000 + TILE_PHYS
FG_VAL        = 0xaabbccdd    # distinctive foreground colour
DST_PAINT     = 0x11223344    # sentinel pattern: distinct from FG_VAL and random values

OP_NOP        = 0x00000000
OP_B_SELF     = 0x1000ffff
OP_SW_T0_A3   = 0xace80000    # sw $t0, 0($a3)
OP_SD_T0_A3   = 0xfce80000    # sd $t0, 0($a3)
OP_LW_V0_AT   = 0x8c220000    # lw $v0, 0($at)

rows = []
def row(name, got, want, note="", negate=False):
    ok = (got != want) if negate else (got == want)
    rows.append((name, ok))
    shown = ("NOT " + str(want)) if negate else str(want)
    print("%-16s %-14s %-16s %-52s %s" % (name, str(got), shown, note, "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.6):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x80001000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.22):
            alive = False
            break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%08x" % (int(m.group(1), 16) & 0xffffffff)

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, val, op=OP_SW_T0_A3):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([op], A.take(1))

SENTINEL = 0xdeadbeef
def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1))

def setup_put(A, dst_mode, fg=FG_VAL, paint=DST_PAINT):
    """Program the engine, paint destination with sentinel, then fire one pixel PUT."""
    c  = store(A, RE_LINEAR_A, 0x0000001000000000, op=OP_SD_T0_A3)  # re_linear_a[0] = 0x10 -> phys 0x10000
    c += store(A, DST_KSEG1, paint)
    c += store(A, DE_MODE_DST, dst_mode)
    c += store(A, DE_DRAWMODE, DRAWMODE_SOLID)
    c += store(A, DE_FG, fg)
    c += store(A, DE_XVERTEX_0, 0x00000000)
    c += store(A, DE_XVERTEX_1, 0x00000000)
    c += store(A, DE_PRIM_START, PRIM_RECT)
    return c

print("sgirandomcolour RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-16s %-52s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- row 1: live
A = Addr(CODE)
t_live, alive_live = session(setup_put(A, MODE_RGBA) + load(A, DST_KSEG1) + ["print v0"])
got_live = printed(t_live, "v0") if alive_live else "died"
row("live", got_live, "0x%08x" % FG_VAL,
    "LIVENESS: supported RGBA DE PUT lands known colour in destination")

# ---------------------------------------------------------------- row 2: ycrcb put
A = Addr(CODE)
t_ycrcb1, alive_ycrcb1 = session(setup_put(A, MODE_YCRCB) + load(A, DST_KSEG1) + ["print v0"])
got_ycrcb1 = printed(t_ycrcb1, "v0") if alive_ycrcb1 else "died"
want_sentinel = "0x%08x" % DST_PAINT
row("ycrcb put", got_ycrcb1, want_sentinel,
    "DEFECT: YCRCB (0xf0) PUT must leave sentinel unchanged; on HEAD clobbered")

# ---------------------------------------------------------------- row 3: ycrcb attrib
diag_ycrcb = "[ put: color mode = 0xf0 ]" in t_ycrcb1
row("ycrcb attrib", "yes" if diag_ycrcb else "no", "yes",
    "ATTRIBUTION: transcript carries `[ put: color mode = 0xf0 ]`")

# ---------------------------------------------------------------- row 4: reserved put
A = Addr(CODE)
t_resv, alive_resv = session(setup_put(A, MODE_RESERVED) + load(A, DST_KSEG1) + ["print v0"])
got_resv = printed(t_resv, "v0") if alive_resv else "died"
row("reserved put", got_resv, want_sentinel,
    "RESERVED: unsupported 0x50 PUT must leave sentinel unchanged; on HEAD clobbered")

# ---------------------------------------------------------------- row 5: determinism
A = Addr(CODE)
t_ycrcb2, alive_ycrcb2 = session(setup_put(A, MODE_YCRCB) + load(A, DST_KSEG1) + ["print v0"])
got_ycrcb2 = printed(t_ycrcb2, "v0") if alive_ycrcb2 else "died"
identical = (got_ycrcb1 == got_ycrcb2 and got_ycrcb1 != "died")
got_det = "identical" if identical else "differ"
row("determinism", got_det, "identical",
    "DETERMINISM: repeat YCRCB put; post-fix identical (sentinel), pre-fix differs across runs")

ok = sum(1 for _, o in rows if o)
print()
print("SGICOLOUR_RESULT=%d/%d" % (ok, len(rows)))
print("SGICOLOUR_DONE")
sys.exit(0 if ok == len(rows) else 1)
