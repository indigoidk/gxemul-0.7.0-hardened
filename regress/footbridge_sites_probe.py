#!/usr/bin/env python3
"""#432: the DC21285 "footbridge" driven by REAL GUEST INSTRUCTIONS, with no rig.

WHY THIS EXISTS ALONGSIDE regress/diff_footbridge.c.  The offline differential calls
footbridge_effective_cycles() and dev_footbridge_access() directly, so it proves BEHAVIOUR
but cannot prove the device is REACHABLE by a guest -- it would stay green under a change
that unmapped it (a memory_device_register length, a DM_ flag, or machine_cats.c's
`addr=0x42000000` line).  Until this probe, R6 was THE ONLY CODE ROUND IN THIS TREE WITH NO
REACHABILITY WITNESS OF ANY KIND: no rig boots a footbridge and there is no m8online analog.
This is that analog.  It goes through the real address decode and the real memory_rw
plumbing, on a COLD DEBUGGER -- no boot, no disk image, no guest OS.

*** THE TRAP THIS PROBE EXISTS TO SURVIVE, and it is the whole reason for arm T. ***
machine_cats.c:131 calls arm_setup_initial_translation_table(), which (cpu_arm.c:239-255)
writes a section descriptor for i in 0..255 at VA (j<<28)+(i<<20) -> PA i<<20 -- i.e. the
TOP NIBBLE OF THE VA IS IGNORED and only the low 256 MB of physical space is mapped
anywhere.  The footbridge sits at PA 0x42000000, outside that window, so under the boot-time
MMU it is UNREACHABLE: VA 0x42000000 aliases to PA 0x02000000 and a load returns 0.

That is not a hypothetical.  The first version of this probe returned 0x0 on every device
row WITH ITS RAM CONTROL STILL GREEN, and 0x0 is exactly what "the device is not there"
looks like -- so a survival-shaped or absence-shaped assertion would have CONFIRMED THE
OPPOSITE CONCLUSION.  A RAM liveness row cannot see it, because VA 0x9000 maps to PA 0x9000
identically with the MMU on or off.

So the guard is not a comment, it is arm T: THE SAME PROGRAM WITH THE THREE MMU-DISABLE
INSTRUCTIONS REPLACED BY NOPS MUST NOT PRODUCE THE DEVICE'S ANSWER.  If arm T ever reads
0x1011, the discriminator is dead and every other row here is meaningless -- and it goes RED
rather than silently green.  Arm L additionally reads CP15 c1 BACK after the mcr and asserts
bit 0 is clear, so the precondition is MEASURED rather than inferred from the store having
been issued.  Three separate statements, deliberately: the guest turned the MMU off, the two
arms really differ in MMU state, and only the MMU-off arm can see the device.

VALUES, NOT SURVIVAL (rounds 79/80, and m8820x_sites_probe.py's header says the same).
A row that only asks "did the host stay up" cannot tell a reachable device from an absent
one -- an unmapped read survives too, it just returns 0.  So the two device rows assert
values that ONLY dev_footbridge.c can produce:
  * A1 reads VENDOR_ID and requires 0x1011 (dev_footbridge.c:423, DC21285_VENDOR_ID).
    Nonzero and specific: the hand-assembled-encoding trap this project has been bitten by
    yields 0 from a wrong register field, and 0 is the one answer this row rejects.
  * A2 writes 0x12345678 to TIMER_1_LOAD and reads back 0x00345678.  THE VANISHING TOP BYTE
    IS THE HANDLER'S OWN SIGNATURE: dev_footbridge.c:548 stores `idata & TIMER_MAX_VAL`
    (0x00FFFFFF, dc21285reg.h:371).  RAM, or any decode that merely absorbed the store,
    would return 0x12345678 unchanged.  This row therefore distinguishes "the device
    handled it" from "the write landed somewhere", which A1 alone cannot.

THE KILL PAIR, which is this probe's own failability control.  Arms L and K differ by
EXACTLY ONE INSTRUCTION.  Arm K adds a guest read of IRQ_ENABLE_SET (base+0x188), which
dev_footbridge.c:495-497 answers with fatal() then exit(1) -- an UNFIXED site, used here
rather than repaired, because a probe that reports SURVIVED for every row is vacuous unless
something in it can still die.  Arm L must live; arm K must exit 1 and say so.  If both
survived, the guest instructions are not reaching the device at all and every SURVIVED
verdict above is worthless; if both died, the probe is killing the host for its own reasons.
The one-instruction delta is the entire argument.

EVERY PLANTED WORD IS CHECKED AGAINST THE DISASSEMBLY THE EMULATOR PRINTS AS IT STEPS IT --
not against a separate `unassemble`, because the step line is the instruction that actually
executed.  This project has a recorded incident where a wrong register field made a gate row
measure the wrong thing for months.

COST, measured: see PROBE_WALL below -- 3 cold-debugger launches, no boot.  A booting-rig row
was deliberately NOT written: no rig in this tree boots a footbridge machine at all, which is
the gap this probe closes, and adding one would put a load-sensitive wall-clock oracle into a
battery already carrying ~37.

usage: footbridge_sites_probe.py <gxemul-binary> <four-byte-raw-stub>
The stub is the same scaffolding gate_arm.sh writes for testarm: `cats` needs a file
argument to construct, and every word of it is overwritten before anything executes.
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
STUB = sys.argv[2]
CODE = 0x00008000
DATA = 0x00009000
NOP = 0xE1A00000
NOPTXT = "mov r0,r0"      #  the EMULATOR's spelling of 0xe1a00000; it does not print "nop"

#  (offset, word, expected disassembly text, comment)
#  Spellings are the EMULATOR's own, not a manual's: "mrc 15,0,r0,cr1,cr0,0" and decimal
#  ldr/str offsets ("[r0,#768]" for 0x300) are what this disassembler prints.
MMU_OFF = [
    (0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"),
    (0x04, 0xE3C00001, "bic r0,r0,#1",          "clear the MMU enable bit"),
    (0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"),
]
MMU_NOP = [
    (0x00, NOP, NOPTXT, "arm T: MMU LEFT ON -- the negative control"),
    (0x04, NOP, NOPTXT, ""),
    (0x08, NOP, NOPTXT, ""),
]
BODY = [
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: read CP15 c1 BACK -- measures the state"),
    (0x10, 0xE3A00442, "mov r0,#0x42000000",    "footbridge base (machine_cats.c:64)"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness: plain RAM, 0x11223344"),
    (0x1c, 0xE5906000, "ldr r6,[r0]",           "A1: VENDOR_ID"),
    (0x20, 0xE5942004, "ldr r2,[r4,#4]",        "load 0x12345678 from RAM"),
    (0x24, 0xE5802300, "str r2,[r0,#768]",      "A2: TIMER_1_LOAD <- 0x12345678"),
    (0x28, 0xE5901300, "ldr r1,[r0,#768]",      "A2: read it back"),
]
KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site")
KILL_LOAD = (0x2c, 0xE5907188, "ldr r7,[r0,#392]", "arm K: read IRQ_ENABLE_SET (0x188)")
TAIL = [(0x30, NOP, NOPTXT, "landing pad -- planted, never stepped")]


def run_arm(label, prog):
    """Plant `prog`, step it one instruction at a time, report registers and liveness."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    dead = [False]

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

    #  Signature order is not free choice: gate_hygiene.sh pins the CANONICAL #392 call form
    #  as a literal `return wait(mark=_mark, echo=<x> if <x> else None)`, tightened three
    #  times because every looser prefix was a substring of the broken form too.  Written any
    #  other way, a probe is simply not covered by that ratchet -- which is worse than failing
    #  it.  So timeout goes last, and send() ends on the pinned form.
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
        return wait(mark=_mark, echo=x if x else None)

    status, regs, badis = "?", {}, []
    #  KEYWORD, and this is not style.  A positional wait(120) silently becomes mark=120 under
    #  the pinned parameter order -- a real behaviour change, and the exact mistake the
    #  m8820x probe's conversion had to fix in the same commit.
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
        send("put w 0x%08x, 0x%08x" % (DATA + 4, 0x12345678))
        for off, word, _t, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + off, word))
        send("pc=0x%08x" % CODE)
        status = "SURVIVED"
        for off, word, text, _c in prog[:-1]:      # the landing pad is never stepped
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                break
            seg = buf[mark:]
            #  Match the emulator's own step line for THIS address and compare the mnemonic
            #  it printed against what this table says was planted.
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + off, word), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
            if got != text:
                badis.append("0x%02x planted 0x%08x -> %r, expected %r"
                             % (off, word, got, text))
        if status == "SURVIVED":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                for n in (0, 1, 2, 3, 5, 6, 7):
                    mm = re.search(r"\br%d\s*=\s*0x([0-9a-fA-F]+)" % n, buf[mark:])
                    if mm:
                        regs[n] = int(mm.group(1), 16)
            else:
                status = "HOST-DIED" if dead[0] else "NO-REG"
    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.3)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        _, st = os.waitpid(pid, 0)
    except Exception:
        st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
    print("  arm %-36s %-9s exit=%-5s signal=%s" % (label, status, code, sig))
    for b in badis:
        print("      DISASSEMBLY MISMATCH: %s" % b)
    return {"status": status, "regs": regs, "exit": code, "signal": sig,
            "fatals": fatals, "badis": badis}


def hexs(v):
    return "-" if v is None else "0x%08x" % v


def row(tag, note, got, want):
    ok = got == want
    print("%-4s %-40s got=%-12s want=%-12s %s"
          % (tag, note, hexs(got), hexs(want), "ok" if ok else "FAIL"))
    return ok


print("BINARY=%s" % BIN)
print("machine: cats/SA110, cold debugger, MMU disabled by the guest, no boot")
t0 = time.time()

L = run_arm("L  live      (MMU off)",      MMU_OFF + BODY + [KILL_NOP] + TAIL)
T = run_arm("T  trap ctrl (MMU LEFT ON)",  MMU_NOP + BODY + [KILL_NOP] + TAIL)
K = run_arm("K  kill      (MMU off,+188)", MMU_OFF + BODY + [KILL_LOAD] + TAIL)
print()

results = []
#  ---- controls.  A probe whose control row failed has measured NOTHING. ----
c1 = row("C1", "liveness: guest ran, plain RAM readback",
         L["regs"].get(5), 0x11223344)
c2 = row("C2", "MMU really OFF in arm L (CP15 c1 bit 0)",
         (L["regs"][3] & 1) if 3 in L["regs"] else None, 0)
c3 = row("C3", "MMU really ON in arm T (the arms differ)",
         (T["regs"][3] & 1) if 3 in T["regs"] else None, 1)
results += [c1, c2, c3]
#  *** C4 IS THE TRAP GUARD.  Stated as an INEQUALITY on purpose: arm T may read 0, or -T may
#  halt it on the non-existent alias at PA 0x02000000, and both are acceptable outcomes.  What
#  is never acceptable is arm T producing the device's answer, because then arm L's 0x1011 is
#  not evidence of anything.  ***
t_vendor = T["regs"].get(6)
c4 = t_vendor != 0x1011
print("%-4s %-40s got=%-12s want=%-12s %s"
      % ("C4", "MMU-on arm CANNOT see the device", hexs(t_vendor), "!= 0x1011",
         "ok" if c4 else "FAIL"))
if not c4:
    print("      *** THE DISCRIMINATOR IS DEAD: the device answered with the boot-time MMU")
    print("      *** still enabled, so arm L proves nothing about turning it off.  Either the")
    print("      *** cats translation table changed (machine_cats.c:131, cpu_arm.c:239-255)")
    print("      *** or the device moved into the low 256 MB.  Re-derive before believing A1/A2.")
results.append(c4)

#  ---- the reachability rows.  VALUES, not survival. ----
a1 = row("A1", "VENDOR_ID through a real guest ldr", L["regs"].get(6), 0x1011)
a2 = row("A2", "TIMER_1_LOAD masked to 24 bits by :548", L["regs"].get(1), 0x00345678)
results.append(a1)
results.append(a2)
#  *** NAME THE RIGHT CAUSE, and this branch is here because the first draft named the WRONG
#  one.  A red A1 has two utterly different causes that look identical -- r6 == 0 -- and the
#  earlier version printed "this is NOT the MMU trap" unconditionally, so on the very run
#  where the MMU trap WAS the cause it pointed the reader at the device.  Measured: the
#  negative-control run (arm L with the three mcr/bic words replaced by nops) printed exactly
#  that misdiagnosis.  A diagnostic that fires on the wrong branch is worse than none.  ***
if not a1:
    if not c2:
        print("      *** THE MMU TRAP, and A1/A2 are NOT evidence about the device: arm L's")
        print("      *** CP15 c1 bit 0 is still SET, so VA 0x42000000 aliased to PA 0x02000000")
        print("      *** (machine_cats.c:131 -> cpu_arm.c:239-255 maps only the low 256 MB) and")
        print("      *** nothing ever addressed the footbridge.  Fix the MMU-off sequence first.")
    elif L["regs"].get(6) == 0:
        print("      NOTE: r6 == 0 with C2 and C4 GREEN is not the MMU trap -- the guest really")
        print("      NOTE: did address PA 0x42000000, so the device is absent or has stopped")
        print("      NOTE: decoding there (memory_device_register / DM_ flags / machine_cats.c:64).")
results.append(row("A2b", "the value the guest actually stored",
                   L["regs"].get(2), 0x12345678))

#  ---- the kill pair: this probe's own failability control. ----
l_ok = L["status"] == "SURVIVED" and L["exit"] == 0 and not L["fatals"]
k_ok = any("ENABLE SET" in f for f in K["fatals"]) and K["exit"] == 1
print("%-4s %-40s %-30s %s"
      % ("I1", "isolation arm SURVIVES untouched",
         "status=%s exit=%s" % (L["status"], L["exit"]), "ok" if l_ok else "FAIL"))
print("%-4s %-40s %-30s %s"
      % ("K1", "kill arm dies at 0x188, exit 1",
         "exit=%s" % K["exit"], "ok" if k_ok else "FAIL"))
print("      kill arm said: %s" % ((K["fatals"] or ["(nothing)"])[-1]))
results.append(l_ok)
results.append(k_ok)

nbad = sum(len(a["badis"]) for a in (L, T, K))
print("%-4s %-40s %-30s %s"
      % ("D1", "every planted word disassembled as meant",
         "%d mismatches" % nbad, "ok" if nbad == 0 else "FAIL"))
results.append(nbad == 0)

#  Named, not indexed.  The first version wrote `results[0] and results[1] ...`, which silently
#  re-points at different rows the moment a row is inserted above -- the same class as pinning a
#  row by an id that names a family.
ctrl_ok = c1 and c2 and c3 and c4
print()
print("ROWS=%d of %d" % (sum(1 for r in results if r), len(results)))
print("FOOTBRIDGE_SITES_CONTROL=%s" % ("OK" if ctrl_ok else "BAD"))
print("FOOTBRIDGE_SITES_%s" % ("PASS" if all(results) else "FAIL"))
print("PROBE_WALL=%.1fs for 3 cold-debugger arms" % (time.time() - t0))
