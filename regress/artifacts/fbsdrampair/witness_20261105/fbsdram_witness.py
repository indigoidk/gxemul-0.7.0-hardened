#!/usr/bin/env python3
"""fbsdrampair -- a rung-3 WITNESS that a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_BA_OFFSET
(+0x104) on the DC21285 "footbridge" ends the emulator process.

THE DEFECT, quoted from GXEMUL-SEC/src/devices/dev_footbridge.c, DEVICE_ACCESS(footbridge):

	case SDRAM_BA_MASK:
		if (writeflag == MEM_READ) {
			fatal("[ footbridge read from sdram_ba_mask ]\\n");
			exit(1);
	...
	case SDRAM_BA_OFFSET:
		if (writeflag == MEM_READ) {
			fatal("[ footbridge read from sdram_ba_offset ]\\n");
			exit(1);

A WITNESS, NOT A DETECTOR: it exists BEFORE any fix and shows the symptom on the committed build.
Modelled on regress/footbridge_sites_probe.py (#432/#539/#545).  Its helpers are COPIED here, not
imported, because that file runs its six sessions at module level.

MACHINE AND ROUTE.  `-E cats` (unmodified, in-tree), cold debugger (-V), no boot, no disk image.
The footbridge CSRs sit at PA 0x42000000, which the boot-time MMU does not map (machine_cats.c calls
arm_setup_initial_translation_table(): the low 256 MB only, the top VA nibble ignored), so under the
boot MMU a VA 0x42000000 load aliases PA 0x02000000 and never reaches the device.  The guest
therefore turns the MMU off itself (mrc/bic/mcr) and reads CP15 c1 BACK, so the precondition is
MEASURED, not inferred from the store having been issued.

ONE SITE PER RUN.  On the defective build the process ends at the first SDRAM read, so a run that
read +0x100 first could never reach +0x104.
  W1  MMU off (proven), liveness + signature controls, then ONE word load from 0x42000100.
  W2  the same, then ONE word load from 0x42000104.
  W3  MMU LEFT ON (the three MMU words replaced by nops), the same prologue, then ONE word load from
      VA 0x42000100.  It aliases PA 0x02000100, inside memory_rw's `physical_max + 0x40000` slack
      (memory.c memory_warn_about_unimplemented_addr), so it reads zeros with no warning and no -T
      halt.  It must NOT reach the device: no fatal line, the process survives, `quit` exits 0.

CONTROLS, from a `reg` taken AFTER the prologue and BEFORE the site (on the defective build nothing
can be read after the site):
  C1   liveness   r5 = 0x11223344, loaded from plain RAM at 0x9000.
  C2   MMU OFF    r3 = CP15 c1 read back by the guest, bit 0 CLEAR (W1, W2).
  C3   MMU ON     the same read, bit 0 SET (W3) -- the runs really differ in MMU state.
  A1   signature  r6 = VENDOR_ID at +0x000, which only dev_footbridge.c answers 0x1011 (W1, W2).
  C4   trap guard r6 present and != 0x1011 in W3: the MMU-on run cannot see the device.  If it
                  could, nothing here would separate "reached the device" from "did not".
  CB   base       r0 = 0x42000000, so the site address is exactly 0x42000100 / 0x42000104.
  CS   sentinel   r7 = 0x5a5ac3c3 from RAM just before the site: the prologue ran to its end.
  D1   every stepped word disassembled as planted, INCLUDING the site load's own step line.
       cpu_dyntrans.c prints the step line before `I;` executes the instruction, so in W1/W2 that
       line precedes the fatal text (row ORD), which ties the death to this load and no other.

HOW A RUN ENDED comes from the reap (WIFEXITED / exit status / signal).  A kill fired by THIS
harness after a timeout is labelled HARNESS-KILL and is never passed off as a product death.

usage: fbsdram_witness.py <gxemul-binary> [tag]     (tag names the transcript files; default HEAD)
"""
import hashlib, os, pty, re, select, signal, struct, sys, time

BIN = sys.argv[1]
TAG = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
HERE = os.path.dirname(os.path.abspath(__file__))
STUB = os.path.join(HERE, "arm_stub.bin")
CODE = 0x00008000
DATA = 0x00009000
NOP = 0xE1A00000
NOPTXT = "mov r0,r0"      # the EMULATOR's spelling of 0xe1a00000; it does not print "nop"
LIVE = 0x11223344         # DATA+0: the C1 liveness word
SENT = 0x5A5AC3C3         # DATA+4: the r7 sentinel, loaded just before the site
BASE = 0x42000000
VENDOR = 0x1011
FATAL_MASK = "[ footbridge read from sdram_ba_mask ]"
FATAL_OFFSET = "[ footbridge read from sdram_ba_offset ]"

#  (offset, word, the emulator's own disassembly of it, comment) -- copied from
#  footbridge_sites_probe.py where the word is shared, so the spellings are already measured.
MMU_OFF = [
    (0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"),
    (0x04, 0xE3C00001, "bic r0,r0,#1",          "clear the MMU enable bit"),
    (0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"),
]
MMU_NOP = [
    (0x00, NOP, NOPTXT, "W3: MMU LEFT ON -- the negative control"),
    (0x04, NOP, NOPTXT, ""),
    (0x08, NOP, NOPTXT, ""),
]
PROLOGUE = [
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2/C3: read CP15 c1 BACK -- measures the state"),
    (0x10, 0xE3A00442, "mov r0,#0x42000000",    "CB: footbridge base (machine_cats.c addr=0x42000000)"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness: plain RAM, 0x11223344"),
    (0x1c, 0xE5906000, "ldr r6,[r0]",           "A1 / C4: VENDOR_ID at +0x000"),
    (0x20, 0xE5947004, "ldr r7,[r4,#4]",        "CS: r7 <- 0x5a5ac3c3 sentinel from RAM"),
]
SITE_100 = (0x24, 0xE5907100, "ldr r7,[r0,#256]", "THE SITE: one word load from base+0x100 (SDRAM_BA_MASK)")
SITE_104 = (0x24, 0xE5907104, "ldr r7,[r0,#260]", "THE SITE: one word load from base+0x104 (SDRAM_BA_OFFSET)")
PAD = (0x28, NOP, NOPTXT, "landing pad -- planted, never stepped")
REGNAME = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}   # the emulator's spellings
CAPTURE = (0, 3, 5, 6, 7)


def run(rid, label, prog, site):
    """Plant `prog`, step the prologue one instruction at a time, read the registers, then step the
    ONE site instruction and observe what happens.  Everything is observed BEFORE teardown."""
    site_off, site_word, site_text, _c = site
    argv = [BIN, "-V", "-T", "-E", "cats", "-M", "32", "0x%x:%s" % (CODE, STUB)]
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, argv)
        os._exit(127)
    buf = ""
    dead = [False]

    #  rd()/wait()/send() and the teardown below are COPIED from footbridge_sites_probe.py
    #  (#539/#545): rd() returns True on a select TIMEOUT and False only on EOF/EIO.
    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            dead[0] = True
            return False
        if not d:
            dead[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(fd, b[n:])
        except OSError:
            dead[0] = True
            return False
        return wait(mark=_mark, echo=x if x else None, timeout=timeout)

    def getregs(mark):
        regs = {}
        for n in CAPTURE:
            mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % REGNAME.get(n, "r%d" % n), buf[mark:])
            if mm:
                regs[n] = int(mm.group(1), 16)
        return regs

    def stepline(off, word, seg):
        m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + off, word), seg)
        return (re.sub(r"\s+", " ", m.group(1)).strip(), m.start()) if m else ("(no step line)", -1)

    status, before, after, badis = "?", {}, {}, []
    site_mark = None
    if not wait(timeout=120):        # KEYWORD: a positional wait(120) would become mark=120
        status = "NO-PROMPT"
    else:
        send("put w 0x%08x, 0x%08x" % (DATA, LIVE))
        send("put w 0x%08x, 0x%08x" % (DATA + 4, SENT))
        for off, word, _t, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + off, word))
        send("pc=0x%08x" % CODE)
        status = "PROLOGUE-OK"
        for off, word, text, _c in prog:
            if off == site_off:
                break
            mark = len(buf)
            rc = send("step 1", timeout=30)
            if not rc or dead[0]:
                status = ("DIED-IN-PROLOGUE@0x%02x" if dead[0] else "TIMEOUT-IN-PROLOGUE@0x%02x") % off
                break
            got, _p = stepline(off, word, buf[mark:])
            if got != text:
                badis.append("0x%02x planted 0x%08x -> %r, expected %r" % (off, word, got, text))
        if status == "PROLOGUE-OK":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                before = getregs(mark)
            else:
                status = "DIED-AT-REG-BEFORE-SITE" if dead[0] else "TIMEOUT-AT-REG-BEFORE-SITE"
        if status == "PROLOGUE-OK":
            site_mark = len(buf)
            rc = send("step 1", timeout=30)
            if dead[0]:
                status = "DIED-AT-SITE"
            elif not rc:
                status = "TIMEOUT-AT-SITE"
            else:
                status = "SURVIVED-SITE"
                mark = len(buf)
                if send("reg", timeout=30) and not dead[0]:
                    after = getregs(mark)
                else:
                    status = "DIED-AFTER-SITE" if dead[0] else "TIMEOUT-AFTER-SITE"
    #  Teardown, as in footbridge_sites_probe.py: quit, DRAIN to EOF (bounded), close the master,
    #  then a BOUNDED reap (poll 10 s, kill, wait).  Diagnostics are collected AFTER the drain.
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t1 = time.time()
    eof = False
    while time.time() - t1 < 20.0:
        if not rd(0.1):
            eof = True
            break
    try:
        os.close(fd)
    except OSError:
        pass
    rpid, st, gone = 0, None, False
    t1 = time.time()
    while rpid == 0 and time.time() - t1 < 10.0:
        try:
            rpid, st = os.waitpid(pid, os.WNOHANG)
        except OSError:
            gone = True      # ECHILD: already reaped elsewhere; its pid may be recycled -- never kill it
            break
        if rpid == 0:
            time.sleep(0.05)
    harness_killed = False
    if rpid == 0 and not gone:
        harness_killed = True
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            _, st = os.waitpid(pid, 0)
        except OSError:
            st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
    if harness_killed and sig == signal.SIGKILL:
        sig = "HARNESS-KILL(%s)" % sig
    elif not eof and sig is not None:
        sig = "HARNESS-CLOSE(%s)" % sig

    #  The site's own step line, searched in the FINAL buffer from the site mark (so bytes that
    #  arrived during the drain count), and its position for the ORD row.
    site_got, site_pos, site_seg = "(site never stepped)", -1, ""
    if site_mark is not None:
        site_seg = buf[site_mark:]
        site_got, p = stepline(site_off, site_word, site_seg)
        site_pos = site_mark + p if p >= 0 else -1
        if site_got != site_text:
            badis.append("SITE 0x%02x planted 0x%08x -> %r, expected %r"
                         % (site_off, site_word, site_got, site_text))
    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf)
    with open(os.path.join(HERE, "%s_%s.pty.txt" % (rid, TAG)), "w", encoding="latin1", newline="") as f:
        f.write(buf)
    print("  run %-3s %-40s %-16s exit=%-5s signal=%s" % (rid, label, status, code, sig))
    print("      argv: %s" % " ".join(argv))
    for b in badis:
        print("      DISASSEMBLY MISMATCH: %s" % b)
    return {"status": status, "before": before, "after": after, "exit": code, "signal": sig,
            "harness_killed": harness_killed, "eof": eof, "badis": badis, "fatals": fatals,
            "site_got": site_got, "site_pos": site_pos, "site_seg": site_seg, "buf": buf,
            "count": {FATAL_MASK: buf.count(FATAL_MASK), FATAL_OFFSET: buf.count(FATAL_OFFSET)},
            "pos": {FATAL_MASK: buf.find(FATAL_MASK), FATAL_OFFSET: buf.find(FATAL_OFFSET)}}


def hexs(v):
    return "-" if v is None else "0x%08x" % v


def row(tag, note, got, want):
    ok = got == want
    print("%-7s %-46s got=%-12s want=%-12s %s" % (tag, note, hexs(got), hexs(want), "ok" if ok else "FAIL"))
    return ok


def trow(tag, note, shown, ok):
    print("%-7s %-46s %-38s %s" % (tag, note, shown, "ok" if ok else "FAIL"))
    return ok


def printable(s):
    return "".join(ch if (" " <= ch <= "~") else "?" for ch in s)


def show_site(R, nlines=8):
    """Print the site segment verbatim (non-printables as '?'): the echoed command, the site's step
    line, and whatever the emulator printed after it, up to EOF or the prompt."""
    lines = [ln for ln in re.split(r"\r\n|\r|\n", R["site_seg"]) if ln.strip()]
    print("      site segment, verbatim (%d non-empty lines, first %d shown):" % (len(lines), min(nlines, len(lines))))
    for ln in lines[:nlines]:
        print("        | %s" % printable(ln))


def kill_run(rid, R, fatal_text, other_text):
    """W1/W2: the defect is SHOWN only when every control is green AND the process ended AT the site
    with exit status 1 AND the exact fatal text appeared once, after the site's step line."""
    b = R["before"]
    c1 = row(rid + ".C1", "liveness: plain RAM readback (r5)", b.get(5), LIVE)
    c2 = row(rid + ".C2", "MMU really OFF: CP15 c1 bit 0 (r3)", (b[3] & 1) if 3 in b else None, 0)
    a1 = row(rid + ".A1", "device signature: VENDOR_ID +0x000 (r6)", b.get(6), VENDOR)
    cb = row(rid + ".CB", "base register r0 (site = r0 + offset)", b.get(0), BASE)
    cs = row(rid + ".CS", "r7 sentinel loaded just before the site", b.get(7), SENT)
    d1 = trow(rid + ".D1", "every stepped word disassembled as planted",
              "%d mismatches; site: %s" % (len(R["badis"]), R["site_got"]), len(R["badis"]) == 0)
    ctrl = c1 and c2 and a1 and cb and cs and d1
    died = trow(rid + ".END", "process ended AT the site step (EOF)", "status=%s" % R["status"],
                R["status"] == "DIED-AT-SITE")
    ex1 = trow(rid + ".EXIT", "reaped: WIFEXITED, exit status 1, no signal",
               "exit=%s signal=%s harness_kill=%s" % (R["exit"], R["signal"], R["harness_killed"]),
               R["exit"] == 1 and R["signal"] is None and not R["harness_killed"])
    nf = R["count"][fatal_text]
    ft = trow(rid + ".FATAL", "exact text %s" % fatal_text[2:-2], "count=%d" % nf, nf == 1)
    order = R["site_pos"] >= 0 and R["pos"][fatal_text] > R["site_pos"]
    od = trow(rid + ".ORD", "fatal text printed AFTER the site's step line",
              "site@%d fatal@%d" % (R["site_pos"], R["pos"][fatal_text]), order)
    clean = R["count"][other_text] == 0 and R["fatals"] == [fatal_text]
    cl = trow(rid + ".ONLY", "no other footbridge diagnostic in the run",
              "fatals=%d other-site=%d" % (len(R["fatals"]), R["count"][other_text]), clean)
    seen = [printable(ln) for ln in re.split(r"\r\n|\r|\n", R["buf"]) if "footbridge read from" in ln]
    print("      fatal line(s) seen, verbatim: %s" % (" || ".join(repr(s) for s in seen) if seen else "(none)"))
    show_site(R)
    if R["status"] == "NO-PROMPT":
        v = "INVALID: no debugger prompt -- the session never started"
    elif R["harness_killed"] or "TIMEOUT" in R["status"]:
        v = "INVALID: timeout / harness kill (%s) -- not the defect" % R["status"]
    elif R["status"].startswith("DIED") and R["status"] != "DIED-AT-SITE":
        v = "INVALID: the process ended BEFORE the site (%s)" % R["status"]
    elif not ctrl:
        v = "INVALID: a control is red -- this run measured nothing"
    elif R["status"] == "SURVIVED-SITE":
        v = "DEFECT NOT SHOWN: the read was survived (r7 after = %s)" % hexs(R["after"].get(7))
    elif died and ex1 and ft and od and cl:
        v = "DEFECT SHOWN"
    else:
        v = "INCONCLUSIVE: died at the site, but " + ", ".join(
            n for n, ok in (("exit", ex1), ("fatal text", ft), ("order", od), ("only", cl)) if not ok)
    print("%-7s %s" % (rid + ".V", v))
    return v, ctrl


def ctrl_run(rid, R):
    """W3: MMU left on.  NOT REACHED requires every control green, survival of the site and of a
    `reg` after it, a quit that reaps exit 0, no footbridge diagnostic, and the load completed."""
    b, a = R["before"], R["after"]
    c1 = row(rid + ".C1", "liveness: plain RAM readback (r5)", b.get(5), LIVE)
    c3 = row(rid + ".C3", "MMU really ON: CP15 c1 bit 0 (r3)", (b[3] & 1) if 3 in b else None, 1)
    c4 = trow(rid + ".C4", "trap guard: +0x000 read is NOT the device's 0x1011",
              "r6=%s (want present, != 0x00001011)" % hexs(b.get(6)), 6 in b and b[6] != VENDOR)
    cb = row(rid + ".CB", "base register r0 (VA 0x42000100 = r0 + 0x100)", b.get(0), BASE)
    cs = row(rid + ".CS", "r7 sentinel loaded just before the site", b.get(7), SENT)
    d1 = trow(rid + ".D1", "every stepped word disassembled as planted",
              "%d mismatches; site: %s" % (len(R["badis"]), R["site_got"]), len(R["badis"]) == 0)
    ctrl = c1 and c3 and c4 and cb and cs and d1
    sv = trow(rid + ".END", "site stepped, process ALIVE, `reg` after it",
              "status=%s" % R["status"], R["status"] == "SURVIVED-SITE")
    ex0 = trow(rid + ".EXIT", "quit reaps WIFEXITED exit 0, no signal",
               "exit=%s signal=%s harness_kill=%s" % (R["exit"], R["signal"], R["harness_killed"]),
               R["exit"] == 0 and R["signal"] is None and not R["harness_killed"])
    nofatal = (R["count"][FATAL_MASK] == 0 and R["count"][FATAL_OFFSET] == 0 and R["fatals"] == [])
    nf = trow(rid + ".FATAL", "NO fatal text, no footbridge diagnostic at all",
              "mask=%d offset=%d fatals=%d" % (R["count"][FATAL_MASK], R["count"][FATAL_OFFSET],
                                               len(R["fatals"])), nofatal)
    v3 = row(rid + ".LOAD", "site load completed: r7 = RAM-window zero fill", a.get(7), 0)
    print("      'non-existant' memory warning in the run: %s"
          % ("YES" if "non-existant" in R["buf"] else "no"))
    show_site(R, 4)
    if R["status"] == "NO-PROMPT":
        v = "INVALID: no debugger prompt -- the session never started"
    elif R["harness_killed"] or "TIMEOUT" in R["status"]:
        v = "INVALID: timeout / harness kill (%s)" % R["status"]
    elif not ctrl:
        v = "INVALID: a control is red -- this run measured nothing"
    elif R["status"] == "DIED-AT-SITE":
        v = "REACHED: the MMU-on load ended the process -- the discriminator is DEAD"
    elif sv and ex0 and nf and v3:
        v = "NOT REACHED (as required): survived, exit 0, no fatal line"
    else:
        v = "INCONCLUSIVE: " + ", ".join(
            n for n, ok in (("survival", sv), ("exit 0", ex0), ("no fatal", nf), ("load", v3)) if not ok)
    print("%-7s %s" % (rid + ".V", v))
    return v, ctrl


def md5(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except OSError as e:
        return "(unreadable: %s)" % e


#  The four-byte raw stub gate_arm.sh writes for testarm: `cats` needs a file argument to construct,
#  and every word of it is overwritten before anything executes.  Scaffolding, not code under test.
with open(STUB, "wb") as f:
    f.write(struct.pack("<I", NOP))

SRC = os.path.join(os.path.dirname(os.path.abspath(BIN)), "src", "devices", "dev_footbridge.c")
print("BINARY=%s  md5=%s  mtime=%s" % (BIN, md5(BIN), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(BIN)))))
if os.path.exists(SRC):
    print("SOURCE=%s  md5=%s  binary-newer-than-source=%s"
          % (SRC, md5(SRC), os.path.getmtime(BIN) > os.path.getmtime(SRC)))
print("TAG=%s  STUB=%s" % (TAG, STUB))
print("machine: cats/SA110, cold debugger, no boot; ONE SDRAM site per run")
t0 = time.time()

R1 = run("W1", "MMU off, load 0x42000100", MMU_OFF + PROLOGUE + [SITE_100, PAD], SITE_100)
R2 = run("W2", "MMU off, load 0x42000104", MMU_OFF + PROLOGUE + [SITE_104, PAD], SITE_104)
R3 = run("W3", "MMU ON,  load VA 0x42000100", MMU_NOP + PROLOGUE + [SITE_100, PAD], SITE_100)
print()
print("---- W1: SDRAM_BA_MASK read (+0x100), MMU off ----")
v1, k1 = kill_run("W1", R1, FATAL_MASK, FATAL_OFFSET)
print()
print("---- W2: SDRAM_BA_OFFSET read (+0x104), MMU off ----")
v2, k2 = kill_run("W2", R2, FATAL_OFFSET, FATAL_MASK)
print()
print("---- W3: the same +0x100 load with the MMU LEFT ON (must not reach the device) ----")
v3, k3 = ctrl_run("W3", R3)
print()
shown = v1 == "DEFECT SHOWN" and v2 == "DEFECT SHOWN" and v3.startswith("NOT REACHED")
print("SUMMARY W1=[%s] W2=[%s] W3=[%s]" % (v1, v2, v3))
print("FBSDRAM_WITNESS_CONTROLS=%s" % ("OK" if (k1 and k2 and k3) else "BAD"))
print("FBSDRAM_WITNESS=%s" % ("SHOWN" if shown else "NOT-SHOWN"))
print("WITNESS_WALL=%.1fs for 3 cold-debugger runs" % (time.time() - t0))
print("FBSDRAM_WITNESS_DONE")
