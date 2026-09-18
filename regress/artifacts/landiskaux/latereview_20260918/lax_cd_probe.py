#!/usr/bin/env python3
"""lax_cd_probe.py <gxemul> -- the CD-ROM cell the census left NOT SETTLED.

COMMAND_RESET is SET at exactly one site (dev_wdc.c's altstatus RST arm) and READ
at exactly two (the cyl_lo / cyl_hi read arms, both gated on
diskimage_is_a_cdrom()).  So on landisk, where no guest store reaches the
altstatus window today, the ATAPI signature 0x14/0xEB is UNREACHABLE; after the
fix it is posted after the guest's SRST.  Same machine (-E landisk, unmodified),
the scratch image attached as an IDE CD-ROM (`icR:`), same guest-instruction
plumbing as lax_probe.py (whose session()/prog() are imported, not copied)."""
import os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], sys.argv[1]]
BIN = sys.argv[1]
src = open(os.path.join(HERE, "lax_probe.py")).read()
#  Re-use the helpers WITHOUT running lax_probe's rows: cut at the first row.
helpers = src.split("#  ------------------------------------------------------------ S0: the map")[0]
g = {"__name__": "lax_helpers"}
exec(compile(helpers, "lax_probe_helpers", "exec"), g)
g["DISK_ARG"] = "icR:" + g["DISK"]

def session_cd(label, cmds, settle=8.0, spin=2.0):
    import pty, select, time
    argv = [BIN, "-V", "-E", "landisk", "-M", "64", "-d", g["DISK_ARG"], g["KERNEL"]]
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, argv); os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        os.write(fd, (c + "\n").encode()); rd(spin if i == len(cmds) - 1 else 0.35)
    os.write(fd, b"quit\n"); rd(0.6)
    try:
        os.close(fd); os.waitpid(pid, 0)
    except OSError:
        pass
    return buf, alive

W = g["WDC"]
rows = []
def row(name, got, want, note):
    ok = got == want
    rows.append(ok)
    print("%-12s %-12s %-12s %-52s %s" % (name, got, want, note, "ok" if ok else "FAIL"))

def srst_then_sig(label, target):
    cmds = ["r4=0x%x" % target, "r5=0x0c", "r6=0x%x" % (W + 0x08), "r7=0x%x" % (W + 0x0a),
            "r2=0", "r3=0"]
    ops = [g["MOVB_ST"](5, 4),   # SRST|4BIT to the window under test
           g["MOVB_LD"](6, 2),   # r2 = cyl_lo
           g["MOVB_LD"](7, 3)]   # r3 = cyl_hi
    t, alive = session_cd(label, cmds + g["prog"](ops) + ["print r2", "print r3"])
    cd = "cdrom" if "CD-ROM" in t or "cdrom" in t.lower() else "NO-CDROM-IN-BANNER"
    return g["b8"](g["printed"](t, "r2")), g["b8"](g["printed"](t, "r3")), cd

lo, hi, cd = srst_then_sig("cd_new", g["AUX_NEW"])
row("cd banner", cd, "cdrom", "the attached image is an IDE CD-ROM")
row("cd new sig", "%s/%s" % (lo, hi), "0x14/0xeb", "SRST @0x1400002c -> ATAPI signature posted")
lo, hi, cd = srst_then_sig("cd_old", g["AUX_OLD"])
row("cd old sig", "%s/%s" % (lo, hi), "0x00/0x00", "SRST @0x14000206 -> no signature (unmapped)")
print("LAX_CD_RESULT=%d/%d" % (sum(rows), len(rows)))
print("LAX_CD_DONE")
