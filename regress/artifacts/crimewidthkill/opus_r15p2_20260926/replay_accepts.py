#!/usr/bin/env python3
"""replay_accepts.py BIN sessions_f5e915f6.json -- replay the probe's OWN two ACCEPTS sessions (`rearm' and `latch x5',
command lists read from the recorder's JSON, not re-typed) on BIN and count, in each whole transcript, the CONTROL arm's
text and the decline notice.  This measures the channel an ALTERNATIVE member for entries 13/17 would use: a count row
on the existing sessions that already hold the 0x0200 writes (latch SET in `rearm', latch CLEAR in `latch x5')."""
import json, os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
S = json.load(open(sys.argv[2]))["sessions"]
DUMMY = "/tmp/dummy_crimep.bin"


def session(cmds, settle=1.5, spin=1.2):          # the probe's session(), verbatim minus the <RUN> branch (unused here)
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


for want in ("rearm once", "latch x5"):
    s = [x for x in S if want in x["rows"]][0]
    t, clean = session(s["cmds"])
    vals = re.findall(r"CRIME_CONTROL: unimplemented control (0x[0-9a-f]+)", t)
    print("S%02d (%s): clean=%s CONTROL texts=%d values=%s declined=%d" % (
        s["idx"], ",".join(s["rows"]), clean, len(vals), vals, t.count("-- declined.")))
    sys.stdout.flush()
print("REPLAY_DONE")
