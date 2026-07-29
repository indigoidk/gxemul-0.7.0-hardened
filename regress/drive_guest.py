#!/usr/bin/env python3
"""Drive an emulated guest to a shell over a pty and check what it computes.

Why a pty rather than a pipe: on a pipe, both the emulator and the guest's libc switch to
block buffering, so a run cut short by a timeout loses its last partial block. An earlier
version of this harness compared byte counts across builds over pipes and "found" a
capability regression that was entirely a lost 4 KB buffer. A pty is line-buffered and is
also the only way to type at a login prompt.

Usage:  drive_guest.py <rig> <emulator-binary>
Exit:   0 all markers seen, 1 otherwise. Marker counts are printed as KEY=VALUE lines so
        the calling gate can parse them without guessing.
"""
import os
import pty
import re
import select
import sys
import time

IMAGES = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"

# Each rig: the emulator arguments, the conversation, and the markers that must appear.
# A rig proves something only if it CHECKS AN ANSWER -- "the guest survived" is not a
# result. The FP steps below compute values whose correct output is known, so a wrong
# float_emul.c arm shows up as a wrong number rather than as a still-running guest.
RIGS = {
    # m88k: cpu_m88k_instr.c stores IEEE_FMT_S, i.e. the exact arm #287 changed, and had
    # no execution coverage at all before this rig existed.
    "luna88k": {
        # "R:" opens the base image read-only and sends every guest write to a temporary
        # overlay that is thrown away at exit. Without it each run mutates the shared 2 GB
        # image and later runs inherit whatever filesystem state earlier ones left --
        # including an unclean unmount when a timeout kills a booted guest. That made
        # gate 7 fail non-deterministically; see the note in gate_ab.sh.
        "args": ["-e", "luna-88k", "-d",
                 "R:" + IMAGES + "/liveimage-luna88k-raw-20250518.img", "boot"],
        "boot_wait": 600,
        "boot_pat": r"login:",
        "tries": 4,
        # Markers split in the source so they can only come from guest OUTPUT, never from
        # the pty echoing what was typed.
        "steps": [
            ("root\n", 8),
            ("\n", 5),
            ("echo GX_SHELL''_OK; uname -m\n", 12, r"GX_SHELL_OK"),
            # 1.5/3.0 = 0.5 and sqrt(2) = 1.414214 -- the ANSWER is what is checked.
            ("awk 'BEGIN{printf \"GX_FP %.6f %.6f\\n\", 1.5/3.0, 2.0**0.5}'\n", 15,
             r"GX_FP [\d.]+ [\d.]+"),
            ("echo GX_DO''NE\n", 8, r"GX_DONE"),
        ],
        "markers": ["login:", "GX_SHELL_OK", "GX_DONE"],
        "expect_values": {r"GX_FP ([\d.]+) ([\d.]+)": ["0.500000", "1.414214"]},
    },
    # SuperH: cpu_sh_instr.c also stores IEEE_FMT_S. The 7.6 install kernel stops at an
    # installer menu offering (S)hell.
    #
    # NO IN-GUEST FP CHECK HERE, and that is a measured limitation rather than an
    # oversight: the OpenBSD install ramdisk was probed and has no awk, perl, bc, dc or
    # python, and its shell arithmetic is integer-only ($((3/2)) evaluates to 1). There is
    # nothing on the media that can compute a float. What this rig therefore proves is
    # that the SH4 core executes a complete kernel boot and an interactive shell -- real
    # instruction-level coverage of cpu_sh_instr.c, but not of its FP store path.
    #
    # That gap is narrower than it looks. #287 is in the SHARED float_emul.c, and the
    # luna88k rig above exercises that shared arm from a non-MIPS caller with a checked
    # answer. What remains unproven for SuperH is only its own caller glue.
    "landisk": {
        "args": ["-E", "landisk", "-M", "64",
                 IMAGES + "/openbsd76-landisk-bsd.rd"],
        "boot_wait": 420,
        "boot_pat": r"\(I\)nstall, \(U\)pgrade, \(A\)utoinstall or \(S\)hell\?",
        # This rig is INTERACTIVE again as of #293. It originally sent no input at all,
        # because typed lines vanished non-deterministically -- measured at 10 of 12
        # commands lost whole, no echo, no execution. The cause was never the SCIF: the
        # machine's main console handle was unclaimed on landisk, so handle 0 (polled
        # every tick for CTRL-C) raced the SCIF for the same host stdin and stole whole
        # lines. #293 makes the SCIF claim the main console, after which the same probe
        # measures 12 of 12 commands delivered. The confirm-and-retry machinery is kept
        # as a belt against future regressions -- a retry that never fires is free.
        #
        # Markers are split in the source (GX_SH''ELL_OK) so a pty echo of the typed
        # command cannot satisfy them; only guest output can.
        "tries": 3,
        "settle": 2,
        "steps": [
            ("S\n", 15),
            ("stty sane\n", 5),
            ("echo GX_SH''ELL_OK\n", 8, r"GX_SHELL_OK"),
            # The checked ANSWER: integer arithmetic computed by the guest shell. The
            # typed text is "$((6*7))", which does not contain "42", so the value can
            # only come from execution.
            ("echo GX_ANS $((6*7))\n", 8, r"GX_ANS 42"),
            ("echo GX_DO''NE\n", 8, r"GX_DONE"),
        ],
        "markers": ["OpenBSD 7.6", "root on rd0a", "GX_SHELL_OK", "GX_DONE"],
        # Both the boot-time hardware probe AND the interactive answer are asserted.
        # Anchored on the shpcic0 line: a bare "HITACHI (SH\w+)" matches the earlier
        # cpu0 line and returns "SH4".
        "expect_values": {
            r"shpcic0 at mainbus0: HITACHI (\w+)": ["SH7751R"],
            r"GX_ANS (\d+)": ["42"],
        },
    },
}


def drive(rig, binary):
    cfg = RIGS[rig]
    log_path = "/tmp/gxregress/drive_%s.log" % rig
    os.makedirs("/tmp/gxregress", exist_ok=True)
    os.chdir(IMAGES)
    log = open(log_path, "wb")

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(binary, [binary] + cfg["args"])
        os._exit(127)

    buf = ""

    def read_once(timeout):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], timeout)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        log.write(d)
        log.flush()
        buf += d.decode("latin1", "replace")
        return True

    def expect(pat, timeout):
        t = time.time()
        while time.time() - t < timeout:
            if not read_once(0.3):
                return False
            if re.search(pat, buf):
                return True
        return False

    def pump(secs):
        t = time.time()
        while time.time() - t < secs:
            if not read_once(0.3):
                return

    def send(s):
        b = s.encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])

    # SEND, THEN CONFIRM, THEN RETRY.
    #
    # The SuperH console drops guest input non-deterministically: a command vanishes
    # whole, with no echo and no output. Measured on one boot with ten commands of
    # increasing length, 15, 23 and 33 byte lines ran while 9, 17, 27 and 41 byte lines
    # were lost -- so it is neither a length limit nor a strict alternation, and adding
    # settle time before the write did not help. Roughly a third of writes get through.
    #
    # A rig cannot be built on "the send worked", so a step may carry a CONFIRM pattern
    # and is re-sent until that pattern appears. Steps without one are fire-and-forget.
    #
    # The confirm patterns match only what the command PRINTS, never what was typed --
    # a pty echoes the master's writes back, so a naive marker is satisfied by the echo
    # alone and proves nothing about execution.
    settle = cfg.get("settle", 0)
    tries = cfg.get("tries", 1)
    reached = expect(cfg["boot_pat"], cfg["boot_wait"])
    if reached:
        for step in cfg["steps"]:
            text, wait = step[0], step[1]
            confirm = step[2] if len(step) > 2 else None
            for attempt in range(tries if confirm else 1):
                if settle:
                    pump(settle)
                send(text)
                pump(wait)
                if confirm is None or re.search(confirm, buf):
                    break
                print("RETRY=%s attempt=%d" % (confirm, attempt + 1))

    try:
        os.write(fd, b"\x03")
        time.sleep(1.5)
        os.write(fd, b"quit\n")
        pump(5)
    except Exception:
        pass
    try:
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    log.close()

    txt = open(log_path, "rb").read().decode("latin1", "replace")
    ok = True

    print("RIG=%s" % rig)
    print("BINARY=%s" % binary)
    print("LOG=%s" % log_path)
    print("BYTES=%d" % len(txt))
    print("BOOT_REACHED=%d" % (1 if reached else 0))
    if not reached:
        ok = False

    for m in cfg["markers"]:
        c = txt.count(m)
        print("MARKER_%s=%d" % (re.sub(r"\W", "_", m), c))
        if c == 0:
            ok = False

    # A rig with no expected values proves nothing about what the guest COMPUTED, only
    # that it survived. Treat that as a failure rather than silently printing no VALUES
    # line: with the gate comparing VALUES against VALUES_WANT, both absent compared
    # equal and the answer check went green while checking nothing.
    expectations = cfg.get("expect_values", {})
    if not expectations:
        print("VALUES=(no expectation declared)")
        print("VALUES_WANT=(none)")
        print("ERROR=rig declares no expect_values; it cannot check an answer")
        ok = False

    for pat, want in expectations.items():
        found = re.search(pat, txt)
        got = list(found.groups()) if found else []
        print("VALUES=%s" % (",".join(got) if got else "(none)"))
        print("VALUES_WANT=%s" % ",".join(want))
        if got != want:
            ok = False

    print("VERDICT=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in RIGS:
        sys.stderr.write("usage: drive_guest.py <%s> <emulator>\n"
                         % "|".join(sorted(RIGS)))
        sys.exit(2)
    sys.exit(drive(sys.argv[1], sys.argv[2]))
