#!/usr/bin/env python3
"""qhslowifetch -- RUNG-3 WITNESS for the PowerPC slow-path instruction fetch in X(to_be_translated).

DEFECT (filed 2026-10-02).  src/cpus/cpu_ppc_instr.c, X(to_be_translated): when the instruction word is not in a host
page, the translator reads it with cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION); if that read FAILS it prints
"PPC to_be_translated(): read failed: TODO" and calls exit(1) -- the emulator process ends.

WHICH FETCHES REACH IT (2026-11-04).  MEASURED: an IR-on fetch from an unmapped address (the `isi` rows) SURVIVES on the
pre-fix build -- the ISI is delivered (SRR0 = the fault address, PC = 0x400).  READ, not measured: that this holds for
any fetch that does not TRANSLATE, since the dyntrans PC lookup translates with FLAG_INSTR first (cpu_dyntrans.c:670-680).
What reaches the exit is a fetch that translates and then fails as a PHYSICAL read (MEASURED, the `-T` rows): with `-T`
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
NOMEM = 0x02040000           # past 32 MB of RAM and the 256 KB SILENT slack above it (core/memory.c:605), so `-T` fails the read
FATAL = "read failed: TODO"  # the translator's text at the exit
AGAIN_NONEX = None             # ROW 3: frozen from the first run on the fixed build (RECON_FABLE.md D8); None = not yet frozen

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


def nonex(t):
    """How many `-T` halt reports the run printed (memory_rw's "non-existant" line)."""
    return str(t.count("non-existant"))


def unimpl(t):
    return "present" if "UNIMPLEMENTED" in t else "absent"


def exc(t):
    return "present" if "[ PPC Exception" in t else "absent"


def chk(t):
    """The (d) arm's checkstop text.  MSR[ME] is clear on every -T session here (msr = 0, measured), so an arm (c) that is
    deleted or inverted falls to the checkstop fallback -- same pc, SRR0 and park -- and this text is the one channel that differs."""
    return "present" if "checkstop" in t else "absent"


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
row("isi nonex", nonex(T), "0", "no -T halt report on the ISI route (W6)")
regs, T, how = session("isi1", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_IR, "pc=0x%x" % ISI_PC, "step 1"])
row("isi1 session", how, "exit0", "IR on, one step into the BAT gap: survives")
row("isi1 srr0", hexr(regs, "srr0"), hex(ISI_PC), "the ISI was delivered on the step (W6)")
row("isi1 pc", hexr(regs, "pc"), hex(0x400), "the step lands on the ISI vector (W6)")
row("isi1 nonex", nonex(T), "0", "no -T halt report on the ISI step (W6)")
regs, T, how = session("noT", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"])
row("noT session", how, "exit0", "no -T: the read past RAM zero-fills", control=True)
row("noT pc", hexr(regs, "pc"), hex(NOMEM), "the CPU stopped on the zero word", control=True)
row("noT srr0 kept", hexr(regs, "srr0"), hex(SENT), "no exception on that route", control=True)

# ========================================================= THE WITNESS ROWS (-T) ==
regs, T, how = session("T cont", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"], flags=["-T"])
row("T cont session", how, "exit0", "-T fetch past RAM, continue: survives")
row("T cont text", text(T), "absent", "no `read failed: TODO` exit")
row("T cont prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")
row("T cont pc", hexr(regs, "pc"), hex(NOMEM), "parked at the fetch address (W2, W5)")
row("T cont srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on the -T route (W4)")
row("T cont nonex", nonex(T), "1", "exactly one halt report: the loop stopped (W2)")
row("T cont unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented (W3)")
row("T cont exc", exc(T), "absent", "no exception entry on the -T route (W4)")
row("T cont chkstop", chk(T), "absent", "arm (c) parked it; the checkstop arm did not run")
regs, T, how = session("T step", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1"], flags=["-T"])
row("T step session", how, "exit0", "-T fetch past RAM, step: survives")
row("T step text", text(T), "absent", "no `read failed: TODO` exit")
row("T step prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")
row("T step pc", hexr(regs, "pc"), hex(NOMEM), "parked at the fetch address (W2: a bare return moves it)")
row("T step srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on the -T route (W4)")
row("T step nonex", nonex(T), "2", "exactly two halt reports on one step (W2, W5)")
row("T step unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented (W3)")
row("T step exc", exc(T), "absent", "no exception entry on the -T route (W4)")
row("T step chkstop", chk(T), "absent", "arm (c) parked it; the checkstop arm did not run")
regs, T, how = session("again", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1", "step 1", "continue", "continue"], flags=["-T"])
print("again: measured non-existant count = %s" % nonex(T))
row("again session", how, "exit0", "a second step and a second continue after the halt survive")
row("again pc", hexr(regs, "pc"), hex(NOMEM), "still parked: no translated zero slot ran (W5)")
row("again srr0", hexr(regs, "srr0"), hex(SENT), "still no exception entry (W4)")
row("again nonex", nonex(T), str(AGAIN_NONEX), "the count frozen from the first run (D8)")
row("again text", text(T), "absent", "no `read failed: TODO` exit on the repeats")
row("again unimpl", unimpl(T), "absent", "a translated zero slot would print UNIMPLEMENTED (W5)")
row("again exc", exc(T), "absent", "no exception entry on the repeats (W4)")
row("again chkstop", chk(T), "absent", "arm (c), not the checkstop arm, on every repeat")
row("again prompt", prompt(T), "yes", "the debugger ran `reg` after the repeats")

# ===================================================================== RESULT ==
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_IFETCH_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_IFETCH_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PPC_IFETCH_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PPC_IFETCH_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PPC_IFETCH_PROBE_DONE")
