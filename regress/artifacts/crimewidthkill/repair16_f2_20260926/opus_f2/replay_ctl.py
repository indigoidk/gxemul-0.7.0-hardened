#!/usr/bin/env python3
"""replay_ctl.py BIN SESSIONS.json ROW... -- replay the frozen 226-row probe's OWN sessions (command lists read from the
recorder's JSON, never re-typed) that feed each named row, on BIN, and print each session's CONTROL-arm texts: the
prefix count the probe's rows use, and the VALUES printed.  The probe's session() copied verbatim (no <RUN> is used by
these sessions)."""
import json, os, pty, re, select, signal, sys, time

BIN, SJ, WANT = sys.argv[1], sys.argv[2], sys.argv[3:]
S = json.load(open(SJ))["sessions"]
DUMMY = "/tmp/dummy_crimep.bin"


def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x80001000:" + DUMMY])
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
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
            ok = rd(spin if i == len(cmds) - 1 else 0.25)
        except OSError:
            break
        if not ok:
            break
    eof = True
    try:
        os.write(fd, b"quit\n")
        eof = not rd(10.0)
    except OSError:
        pass
    if not eof:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        how = ("sig%d" % os.WTERMSIG(stat)) if os.WIFSIGNALED(stat) else ("exit%d" % os.WEXITSTATUS(stat))
    except OSError:
        pass
    return buf.replace("\r", ""), (eof and how == "exit0")


print("REPLAY_CTL binary=%s" % BIN)
for w in WANT:
    s = [x for x in S if w in x["rows"]][0]
    t, clean = session(s["cmds"])
    vals = re.findall(r"CRIME_CONTROL: unimplemented control 0x([0-9a-f]+)", t)
    print("S%02d %-16s clean=%s prefix-count=%d values=%s count-of-0x1=%d" % (
        s["idx"], w, clean, t.count("CRIME_CONTROL: unimplemented"), ["0x%x" % int(v, 16) for v in vals],
        sum(1 for v in vals if int(v, 16) == 1)))
    sys.stdout.flush()
print("REPLAY_CTL_DONE")
