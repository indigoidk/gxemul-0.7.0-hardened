#!/usr/bin/env python3
# Minimal pexpect-style PTY driver for GXemul guests.
# Usage:  drive.py <logfile> <total_timeout_s> <cmd...>   (expect/send script on stdin)
# stdin script lines:
#   E:<regex>        wait (within total timeout) until <regex> appears in new output
#   S:<text>         send <text> to the guest (supports \n \r \t \xNN escapes)
#   W:<seconds>      passive wait (just capture) for N seconds
# Everything the guest prints is mirrored to <logfile> (and stdout markers for steps).
import os, pty, select, sys, time, re

logpath = sys.argv[1]
total   = float(sys.argv[2])
cmd     = sys.argv[3:]

steps = []
for line in sys.stdin:
    line = line.rstrip("\n")
    if line.startswith("E:"): steps.append(("E", line[2:]))
    elif line.startswith("S:"): steps.append(("S", line[2:].encode().decode("unicode_escape")))
    elif line.startswith("W:"): steps.append(("W", float(line[2:])))

pid, fd = pty.fork()
if pid == 0:
    os.execvp(cmd[0], cmd)
    os._exit(127)

log = open(logpath, "wb")
buf = ""
i = 0
start = time.time()
wait_until = 0.0

def left(): return total - (time.time() - start)

while left() > 0 and i < len(steps):
    # fire any pending SEND / W steps that don't need to wait for output
    while i < len(steps) and steps[i][0] in ("S", "W"):
        kind, val = steps[i]
        if kind == "S":
            os.write(fd, val.encode("latin1"))
            log.write(("\n[SENT %r]\n" % val).encode()); log.flush()
            i += 1
        else:  # W
            wait_until = time.time() + val
            log.write(("\n[WAIT %.1fs]\n" % val).encode()); log.flush()
            i += 1
            # passive wait
            t = time.time()
            while time.time() < wait_until and left() > 0:
                r,_,_ = select.select([fd], [], [], 0.3)
                if fd in r:
                    try: d = os.read(fd, 65536)
                    except OSError: d = b""
                    if not d: break
                    log.write(d); log.flush()
                    buf += d.decode("latin1", "replace")
    r,_,_ = select.select([fd], [], [], 0.5)
    if fd in r:
        try: data = os.read(fd, 65536)
        except OSError: break
        if not data: break
        log.write(data); log.flush()
        buf += data.decode("latin1", "replace")
        if i < len(steps) and steps[i][0] == "E":
            # match against both raw and high-bit-stripped buf (the pmax console
            # getty/login prompt arrives with the 8th bit set on every char)
            stripped = "".join(chr(ord(c) & 0x7f) for c in buf)
            if re.search(steps[i][1], buf) or re.search(steps[i][1], stripped):
                log.write(("\n[MATCHED %r]\n" % steps[i][1]).encode()); log.flush()
                buf = ""
                i += 1

# Clean shutdown: GXemul buffers disk writes via stdio (fwrite) and only flushes
# on a clean exit() / fclose. A SIGKILL would lose unflushed FFS metadata
# (inodes/dirs written during umount), leaving the image's data blocks present
# but the directory tree empty. So drop into the GXemul debugger (Ctrl-C) and
# 'quit', which exits via exit() and fcloses the disk images.
try:
    os.write(fd, b"\x03"); time.sleep(1.5)
    os.write(fd, b"quit\n")
    t = time.time()
    while time.time() - t < 12:
        r,_,_ = select.select([fd], [], [], 0.5)
        if fd in r:
            try: d = os.read(fd, 65536)
            except OSError: d = b""
            if not d: break
            log.write(d); log.flush()
        try:
            wpid,_ = os.waitpid(pid, os.WNOHANG)
            if wpid == pid: break
        except Exception: break
except Exception: pass
try: os.kill(pid, 9)
except Exception: pass
try: os.waitpid(pid, 0)
except Exception: pass
log.close()
print("drive.py: completed %d/%d steps in %.1fs (timeout=%.0fs)" % (i, len(steps), time.time()-start, total))
