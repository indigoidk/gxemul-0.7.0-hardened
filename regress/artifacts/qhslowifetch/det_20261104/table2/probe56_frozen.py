#!/usr/bin/env python3
"""qhslowifetch -- DETECTOR (built on its rung-3 witness) for the PowerPC slow-path instruction fetch in X(to_be_translated).

DEFECT (filed 2026-10-02).  src/cpus/cpu_ppc_instr.c, X(to_be_translated): when the instruction word is not in a host
page, the translator reads it with cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION); if that read FAILED it printed
"PPC to_be_translated(): read failed: TODO" and called exit(1) -- the emulator process ended.

THE FIX (#NNN).  The read-failure arm has four exits and a fallback: (a) read-ahead returns untouched; (b) a fetch whose
translation already delivered an exception (pc != addr) refreshes next_ic and returns; (c) a -T halt (memory.c cleared
running) parks the CPU on nothing_call at the failing address; (d) a device declining an instruction-width read while running
delivers a machine check (vector 0x200) when MSR[ME] is set, and a checkstop (text, running = 0, park) when it is clear.

WHICH FETCHES REACH IT (measured 2026-11-04).  An IR-on fetch from an unmapped address SURVIVES on the pre-fix build: the ISI
is delivered by the dispatch PC lookup before the translator runs (the `isi` rows).  What reaches the arm is a fetch that
translates and then fails as a PHYSICAL read: with `-T` (halt on a non-existent memory access) a real-mode fetch past the end
of RAM.  Without `-T` the same fetch reads zeros and the CPU stops on the zero word (the `noT` rows).

WHAT THE ROWS MEASURE.  Cold `-E pmppc` debugger runs (an UNMODIFIED in-tree machine: Artesyn PM/PPC, PPC750, 32 MB) with a
four-byte `ori r0,r0,0` loaded raw at 0x2000 and SRR0 seeded with a sentinel only an exception entry overwrites.  CONTROLS:
the loaded word executes (`ctl`); a bogus machine runs nothing (`neg`); the ISI route survives and delivers the exception
(`isi`); the no-`-T` route stops on the zero word (`noT`), reports it as UNIMPLEMENTED because the read succeeded, and never
prints the checkstop text.  The -T SESSIONS at 0x02040000 are `T step` (one step), `T cont` (continue), `again` (step, step,
continue, continue) and `T me` (one step with MSR[ME] set).  `T step`, `T cont` and `again` each pin: exit 0 with the prompt
back and no `read failed: TODO`; pc parked at the fetch address; SRR0 unchanged; the exact count of -T halt reports; no
UNIMPLEMENTED, no `[ PPC Exception`, no checkstop text.  `T me` pins exit 0, pc, SRR0, the halt count, no `read failed: TODO`
and no `[ PPC Exception`; its prompt, UNIMPLEMENTED and checkstop channels are left to the other three sessions, since no
single edit inside the arm reds one of them on `T me` without redding another session's row.  The halt counts
("non-existant"): two for a step -- the single-step read's report, its "could not read the instruction" line, then the
translator's report -- one for a continue, and two for the whole `again` session, because a -T halt leaves running at 0
(memory.c), so the run loop does not enter the CPU again and a further step or continue runs nothing (measured, and the
reverse of the reconciliation's provisional want; see artifacts/qhslowifetch/det_20261104/FINDING_D8.md).  `isi1` steps into
the ISI as `isi` continues into it; both pin the vector, SRR0 and no halt report.  `T ra` continues under -T from 0xfec00004, the
last word of cpc700_pci's 8-byte window, which reads 0x23120e00 (subfic r24,r18,0xe00) in its reset state: translating it reads
ahead into 0xfec00008, past the window, so the -T halt fires DURING read-ahead and arm (a) returns; the subfic runs; the real fetch
of 0xfec00008 halts again and arm (c) parks.  It pins exit 0, pc 0xfec00008, two halt reports both naming 0xfec00008, and the
stop (the window sweep found it, det_20261104/window_sweep.out; FINAL_FABLE.md F4 owed it).

WHY THE CHECKSTOP AND ME-SET ROWS EXIST.  MSR is 0 on `T step`, `T cont` and `again`; `T me` sets MSR[ME] (0x1000).  On the
first three, arm (c) deleted or inverted falls to the checkstop fallback, which parks identically -- same pc, SRR0 and
next_ic -- and differs only by its text (the `chkstop` rows).  And arm (c) ordered below arm (d), or conditioned on ME clear,
differs only when ME is set (the `T me` session, which drives arm (d)'s tested bit at the -T halt).  Both were added by the
pre-table check, before the test-variant table ran.

CLAUSE (e) -- catches (test-variant table 1, artifacts/qhslowifetch/det_20261104/table1/SCORES.txt, PRETABLE.out written
before it; 13 of 18 variants red): the removed exit reinstated verbatim (B1); a bare return at the arm head (W2) or on every
non-read-ahead fetch (D5); goto bad (W3); an ISI invented in arm (c) (W4); the arm emptied, or skipped by conditioning the
read's failure test on running, so the uninitialised word decodes (W5, D7); arm (c) inverted or deleted (D1, D2: the chkstop
rows, and the T me rows); arm (c) without its park (D3); arm (b) inverted (D4: the free-running continue re-fetches the
refreshed slot thousands of times -- `T cont nonex`); arm (c) below arm (d) or conditioned on ME clear (D8, D13: the T me rows).
  discloses, not claimed: arm (b)'s refresh, reached on no measured session (D11); arm (d) and the checkstop fallback (D6,
D9, D10): no fetch on pmppc reaches them -- MEASURED by a fetch at every 4-byte offset of every window `device list` names, MSR 0
and MSR[ME], each offset with evidence the word was fetched (det_20261104/window_sweep.out), and in the slack above RAM
(slack_sweep.out); their producer is a device declining an instruction fetch while running, which needs another machine (the
reconciliation's ROW 5, FILED pending X11); 64-bit CPUs; PPC603-class CPUs (their miss vector is 0x10); IR-on fetches whose
translation succeeds onto non-existent memory.  THE READ-AHEAD CELL is measured on cpc700_pci (`T ra`); at the other seven
windows' last words the word a guest load records before the continue is 0x00000000, which decodes as unimplemented and reads
ahead into nothing -- MEASURED at that word, DERIVED for other values of those registers: a window end inside a page puts the
failing word in reach of read-ahead, and whether read-ahead happens depends on the decoded word (cpc700_pci shows a valid
non-branch word reaches it).  The RTC window ran twice and read 0 at +0xfc both times.
  Also not claimed: RE-ENTRY -- every exit returns before the slot's function
pointer is replaced, so the slot stays untranslated and a fetch that later reaches it re-enters the arm, but nothing restores
running after a -T halt on this harness, so no row can test it (a code-reading claim); the `again` session therefore measures
nothing about re-entry and stands as the control that the debugger survives step and continue on a halted CPU, its halt-count
row the control that a -T halt is terminal for the session.  W5's catch rides on the uninitialised instruction word: which rows
red under W5 depends on the garbage decoded, though some row must (a decoded word moves pc, traps, prints UNIMPLEMENTED or
loops).  -T imprecision: a -T data halt earlier in the same batch followed by a declined fetch takes arm (c), with no machine
check (cosmetic; the debugger is entered either way).  The reconciliation's W7 (the read-ahead guard missing) is rowed by
`T ra`; its W8 (the running-1 arm missing) and W9 (a wrong machine check) have no row on pmppc: they need its ROW 5 (FILED pending
X11).  Scores on this probe are regenerated from table 2 (the 50-row table 1 scored the pre-fix build
31 of 50 rows with the symptom PRESENT, and the three null media -- /bin/true, an absent binary, /bin/false -- each
CONTROL=FAIL).

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
MSR_ME = 0x1000              # PPC_MSR_ME, cpu_ppc.h: arm (d)'s test
NOMEM = 0x02040000           # past 32 MB of RAM and the 256 KB SILENT slack above it (core/memory.c:605), so `-T` fails the read
FATAL = "read failed: TODO"  # the translator's text at the exit
AGAIN_NONEX = 2             # ROW 3: frozen from the first run on the fixed build.  A -T halt leaves running at 0, so a second step
                             # or continue runs nothing (D3 and D4: the same count without the park; FINDING_D8.md's correction)

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
    """The (d) arm's checkstop text.  MSR[ME] is clear on T step, T cont and again (msr = 0; T me sets it), so on those an arm (c)
    that is deleted or inverted falls to the checkstop fallback -- same pc, SRR0 and park -- and this text is the one channel that
    differs."""
    return "present" if "checkstop" in t else "absent"


print("qhslowifetch DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
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
row("isi nonex", nonex(T), "0", "premise: no -T report on the ISI route (W6)", control=True)
regs, T, how = session("isi1", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_IR, "pc=0x%x" % ISI_PC, "step 1"])
row("isi1 session", how, "exit0", "IR on, one step into the BAT gap: survives", control=True)
row("isi1 srr0", hexr(regs, "srr0"), hex(ISI_PC), "premise: the lookup delivers the ISI (W6)", control=True)
row("isi1 pc", hexr(regs, "pc"), hex(0x400), "premise: the step lands on the ISI vector", control=True)
row("isi1 nonex", nonex(T), "0", "premise: no -T report on the ISI step", control=True)
regs, T, how = session("noT", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"])
row("noT session", how, "exit0", "no -T: the read past RAM zero-fills", control=True)
row("noT pc", hexr(regs, "pc"), hex(NOMEM), "the CPU stopped on the zero word", control=True)
row("noT srr0 kept", hexr(regs, "srr0"), hex(SENT), "no exception on that route", control=True)
row("noT unimpl", unimpl(T), "present", "the zero word is reported unimplemented (the read succeeded)")
row("noT chkstop", chk(T), "absent", "a successful read never enters the failure arm")

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
row("T step nonex", nonex(T), "2", "premise: single-step read + translator read", control=True)
row("T step unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented (W3)")
row("T step exc", exc(T), "absent", "no exception entry on the -T route (W4)")
row("T step chkstop", chk(T), "absent", "arm (c) parked it; the checkstop arm did not run")
# The floor cell the merged rows left empty (the pre-table check, 2026-11-04): arm (d) TESTS MSR[ME], and MSR is 0 on every -T
# session above, so the -T halt with ME SET is driven here -- arm (c) must still park it, not deliver a machine check.
regs, T, how = session("T me", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_ME, "pc=0x%x" % NOMEM, "step 1"], flags=["-T"])
row("T me session", how, "exit0", "-T halt with MSR[ME] set: survives")
row("T me pc", hexr(regs, "pc"), hex(NOMEM), "parked, not at the 0x200 machine-check vector")
row("T me srr0", hexr(regs, "srr0"), hex(SENT), "no machine check delivered on the -T route")
row("T me nonex", nonex(T), "2", "premise: the same two reports with ME set", control=True)
row("T me text", text(T), "absent", "no `read failed: TODO` exit")
row("T me exc", exc(T), "absent", "no `[ PPC Exception 0x2` on the -T route")
regs, T, how = session("again", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1", "step 1", "continue", "continue"], flags=["-T"])
print("again: measured non-existant count = %s" % nonex(T))
row("again session", how, "exit0", "a second step and a second continue after the halt survive")
row("again pc", hexr(regs, "pc"), hex(NOMEM), "still parked: no translated zero slot ran (W5)")
row("again srr0", hexr(regs, "srr0"), hex(SENT), "still no exception entry (W4)")
row("again nonex", nonex(T), str(AGAIN_NONEX), "premise: a -T halt is terminal (repeats run nothing)", control=True)
row("again text", text(T), "absent", "no `read failed: TODO` exit on the repeats")
row("again unimpl", unimpl(T), "absent", "a translated zero slot would print UNIMPLEMENTED (W5)")
row("again exc", exc(T), "absent", "no exception entry on the repeats (W4)")
row("again chkstop", chk(T), "absent", "arm (c), not the checkstop arm, on every repeat")
row("again prompt", prompt(T), "yes", "the debugger ran `reg` after the repeats")

# The read-ahead cell (FINAL_FABLE.md F4; found by det_20261104/window_sweep.out): cpc700_pci's last word, 0xfec00004, reads
# 0x23120e00 in its reset state -- subfic r24,r18,0xe00 -- so translating it reads ahead into 0xfec00008, past the 8-byte window.
# The -T halt fires DURING read-ahead and arm (a) returns; the subfic runs; the real fetch of 0xfec00008 halts again and arm (c)
# parks.  Two halt reports, both naming 0xfec00008.
RA_LAST = 0xfec00004         # cpc700_pci's data word: the window's last word
RA_NEXT = 0xfec00008         # past the window: no device answers it
regs, T, how = session("T ra", ["srr0=0x%x" % SENT, "pc=0x%x" % RA_LAST, "continue"], flags=["-T"])
row("T ra session", how, "exit0", "-T read-ahead past cpc700_pci: survives")
row("T ra pc", hexr(regs, "pc"), hex(RA_NEXT), "parked at the word past the window")
row("T ra nonex", nonex(T), "2", "the read-ahead's halt, then the real fetch's (W7)")
row("T ra addr", ",".join(sorted(set(re.findall(r"non-existant paddr=(0x[0-9a-fA-F]+)", T)))) or "none", hex(RA_NEXT),
    "every halt names the word past the window")
row("T ra stopped", "yes" if "All machines stopped" in T else "no", "yes", "the -T halt stopped the machine (running 0)")

# ===================================================================== RESULT ==
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_IFETCH_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_IFETCH_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PPC_IFETCH_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PPC_IFETCH_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PPC_IFETCH_PROBE_DONE")
