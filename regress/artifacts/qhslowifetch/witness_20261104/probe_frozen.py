#!/usr/bin/env python3
"""qhslowifetch -- RUNG-3 WITNESS for the PowerPC slow-path instruction fetch in X(to_be_translated).

DEFECT (filed 2026-10-02).  src/cpus/cpu_ppc_instr.c, X(to_be_translated): when the instruction word is not in a host
page, the translator reads it with cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION); if that read FAILS it prints
"PPC to_be_translated(): read failed: TODO" and calls exit(1) -- the emulator process ends.

WHICH FETCHES REACH IT (measured here, 2026-11-04, not reasoned).  An instruction fetch that does not TRANSLATE never
gets there: the dyntrans page lookup translates the PC with FLAG_INSTR first, the PowerPC translation raises the ISI
itself, and execution resumes at the vector -- so the `isi` rows below SURVIVE on the pre-fix build (SRR0 = the fault
address, PC = 0x400).  What reaches the exit is a fetch that translates and then fails as a PHYSICAL read: with `-T`
(halt on a non-existent memory access) a real-mode fetch past the end of RAM makes memory_rw return failure, and the
translator ends the process instead of letting the requested halt land.  Without `-T` the same fetch reads zeros and
the CPU stops on the zero word (the `noT` rows).  A device whose access function fails an instruction-width read is
a second producer; none is enumerated here.

WHAT THE ROWS MEASURE.  Each session is one cold `-E pmppc` debugger run (an UNMODIFIED in-tree machine: Artesyn PM/PPC,
PPC750, 32 MB) with a four-byte `ori r0,r0,0` loaded as a raw file at 0x2000.  SRR0 is seeded with a sentinel that
only an exception entry overwrites in these runs.  CONTROL rows: the loaded word executes (`ctl`); a bogus machine
runs nothing (`neg`); the ISI route survives and delivers the exception (`isi`); the no-`-T` route survives (`noT`).
WITNESS rows (`T cont`, `T step`): the `-T` fetch at 0x02040000, under `continue` and under `step`, must leave the
process alive with the debugger prompt back and no fatal text.  On the pre-fix build both sessions end with the fatal
text and exit status 1 (PPC_IFETCH_SYMPTOM=PRESENT).

NOT CLAIMED (owed when the fix design is ruled): the PC and SRR0 after the `-T` halt (a bare return and the commented
`goto bad` leave different PCs); 64-bit CPUs (bareppc/testppc PPC970); IR-on fetches whose translation succeeds onto
non-existent memory; device-produced read failures; PPC603-class CPUs (their miss vector is 0x10, not the ISI).  The
`session` rows are exit-status oracles, so a non-emulator binary passes the ones that want exit status 0 only if it
exits 0 -- RESULT (to be pinned by equality) and CONTROL=FAIL are what reject a null medium.

Sentinel: PPC_IFETCH_PROBE_DONE (plus PPC_IFETCH_RESULT=n/N, PPC_IFETCH_CONTROL=OK|FAIL, PPC_IFETCH_SYMPTOM=PRESENT|ABSENT,
PPC_IFETCH_RED=none|<names>).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_ifetch_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="ppc_ifetch_")
NOP = os.path.join(_TMPDIR, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))      # ori r0,r0,0 (big-endian)

ENTRY = 0x2000
SENT = 0x11111111            # the SRR0 sentinel; only an exception entry overwrites it in these runs
ISI_PC = 0x20000000          # a reset-BAT gap on the PPC750: no IBAT covers it, SDR1 = 0, so translation misses
MSR_IR = 0x20
NOMEM = 0x02040000           # past 32 MB of RAM and past the warn-only slack above it, so `-T` fails the read
FATAL = "read failed: TODO"  # the translator's text at the exit

rows = []
controls = []
symptom_hits = 0


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def session(name, cmds, flags=(), machine="pmppc", timeout=60):
    """One cold debugger run: `cmds` then `reg` and `quit`.  Returns (regs, text, how)."""
    global symptom_hits
    allc = list(cmds) + ["reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine] + list(flags) + ["0x%x:%s" % (ENTRY, NOP)]
    inp = ("\n".join(allc) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every session row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(allc) + "\n--- transcript (%s) ---\n" % how + t)
    if FATAL in t:
        symptom_hits += 1
    regs = {}
    idx = t.rfind("GXemul> reg")
    if idx >= 0:
        seg = t[idx:]
        for key in ("pc", "srr0", "srr1", "msr"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % key, seg)
            if m:
                regs[key] = int(m.group(1), 16)
    return regs, t, how


def hexr(regs, k):
    return hex(regs[k]) if k in regs else "none"


def text(t):
    return "present" if FATAL in t else "absent"


def prompt(t):
    return "yes" if ("GXemul> reg" in t and "cpu0: pc" in t) else "no"


print("qhslowifetch RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E pmppc (UNMODIFIED in-tree; Artesyn PM/PPC, PPC750, 32 MB); `ori r0,r0,0` loaded raw at 0x%x" % ENTRY)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

# ============================================================ CONTROL SESSIONS ==
regs, T, how = session("ctl", ["srr0=0x%x" % SENT, "step 1"])
row("ctl session", how, "exit0", "the control session's exit status", control=True)
row("ctl live", hexr(regs, "pc"), hex(ENTRY + 4), "the loaded word executed (one step)", control=True)
row("ctl srr0 kept", hexr(regs, "srr0"), hex(SENT), "a good fetch delivers no exception", control=True)
nregs, _, nhow = session("neg", ["step 1"], machine="nosuchmachine", timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hexr(nregs, "pc")), "exit1/none", "a bogus machine runs no guest", control=True)
regs, T, how = session("isi", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_IR, "pc=0x%x" % ISI_PC, "continue"])
row("isi session", how, "exit0", "IR on, fetch in a BAT gap: survives", control=True)
row("isi srr0", hexr(regs, "srr0"), hex(ISI_PC), "the ISI was delivered (SRR0 = fault PC)", control=True)
row("isi pc", hexr(regs, "pc"), hex(0x400), "resumed at the ISI vector (zero word stops)", control=True)
row("isi text", text(T), "absent", "the translator's exit is not on this route", control=True)
regs, T, how = session("noT", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"])
row("noT session", how, "exit0", "no -T: the read past RAM zero-fills", control=True)
row("noT pc", hexr(regs, "pc"), hex(NOMEM), "the CPU stopped on the zero word", control=True)
row("noT srr0 kept", hexr(regs, "srr0"), hex(SENT), "no exception on that route", control=True)

# ========================================================= THE WITNESS ROWS (-T) ==
regs, T, how = session("T cont", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"], flags=["-T"])
row("T cont session", how, "exit0", "-T fetch past RAM, continue: survives")
row("T cont text", text(T), "absent", "no `read failed: TODO` exit")
row("T cont prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")
regs, T, how = session("T step", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1"], flags=["-T"])
row("T step session", how, "exit0", "-T fetch past RAM, step: survives")
row("T step text", text(T), "absent", "no `read failed: TODO` exit")
row("T step prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ===================================================================== RESULT ==
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_IFETCH_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_IFETCH_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PPC_IFETCH_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PPC_IFETCH_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PPC_IFETCH_PROBE_DONE")
