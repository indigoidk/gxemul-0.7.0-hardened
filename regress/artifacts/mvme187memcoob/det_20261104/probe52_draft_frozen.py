#!/usr/bin/env python3
"""mvme187memcoob -- RUNG-3 WITNESS for the MVME187 memory-controller model, DEVICE_ACCESS(mvme187_memc).

DEFECT (filed 2026-09-17).  src/devices/dev_mvme187.c: the device is registered at MVME187_MEM_CTLR (0xfff43000) for 0x200
bytes; bit 8 of the offset selects controller 1 and is then cleared, so relative_addr is 0..0xff.  The handler reads
`((uint8_t*)&d->memcreg)[relative_addr]` BEFORE its switch -- struct memcreg is 31 one-byte registers each padded to four
bytes, 124 bytes -- and then ends the emulator process: `exit(1)` on a write to memconf (+0x08) and in the default arm (any
offset other than chipid +0x00, chiprev +0x04, memconf +0x08).  One guest load or store, no privilege test.

WHAT IS MEASURED (2026-11-04, `-E mvme88k -e mvme187 -M 64`, an UNMODIFIED in-tree machine; one cold debugger session per
access: the word placed at CODE with `put w`, r3 = 0xfff43000, one `step`, then `reg`).  CONTROL rows: the three implemented
registers read back their DEVINIT values through a real `ld.bu` (chipid 0x80, chiprev 1, memconf 3 for 64 MB -- RAM would
read the zero dummy), the controller-1 alias at +0x100 reads chipid too, and a bogus machine runs nothing.  WITNESS rows: a
load at +0x0c (the first unimplemented offset), +0x7c (the first byte past the 124-byte struct) and +0xff (the last), and a
byte store to memconf, must each leave the process alive with the debugger prompt back.  On the pre-fix build all four end
the process with the handler's text (MVME187_MEMC_SYMPTOM=PRESENT).

THE HOST OUT-OF-BOUNDS READ IS NOT WITNESSED HERE.  MEASURED (artifacts/mvme187memcoob/witness_20261104/asan_head/): on the
ASAN build the loads at +0x7c and +0xff exit 1 with no ASAN report; REASONED from that, not observed: the handler skips the read.
It is LATENT: removing the exit with no bound exposes it once the value reaches the guest (MEASURED, draft_20261104/: an ASAN
READ at dev_mvme187.c:68), which is why the bound must land with (or before) any change to the exits.  The detector owes an ASAN leg on the fix.

NOT CLAIMED (owed when the design is ruled): the value a declined read returns, whether a once-latched announce prints, the
widths other than a byte, the stores other than to memconf, controller 1's offsets beyond chipid, and the ASAN leg.

Sentinel: MVME187_MEMC_PROBE_DONE (plus MVME187_MEMC_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT,
_RED=none|<names>).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: mvme187_memc_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="mvme187_memc_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))

CODE = 0x00010000
MEMC = 0xfff43000          # MVME187_MEM_CTLR (thirdparty/mvme187.h)
SENT = 0x55555555
FATAL = ("unimplemented read from offset", "not yet implemented!")


def LD_BU(rd, rs1, imm):    # m88k ld.bu: op26 0x03, d16 offset (the encoding vme_default_probe.py uses)
    return (0x03 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def ST_B(rs, rs1, imm):     # m88k st.b: op26 0x0b
    return (0x0b << 26) | (rs << 21) | (rs1 << 16) | (imm & 0xffff)


assert LD_BU(2, 3, 0x7c) == 0x0C43007C and ST_B(2, 3, 0x08) == 0x2C430008

rows = []
controls = []
symptom_hits = 0
asan_hits = 0                # AddressSanitizer / UBSan report lines across every session (R1, R2: the sanitizer builds)


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def session(name, word, r2, machine="mvme88k", sub="mvme187", timeout=60):
    """One cold run: r3 = MEMC, r2 = `r2`, `word` at CODE, one step, `reg`.  Returns (regs, text, how)."""
    global symptom_hits
    cmds = ["r3=0x%x" % MEMC, "r2=0x%x" % r2, "put w 0x%x, 0x%08x" % (CODE, word), "pc=0x%x" % CODE, "step 1", "reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine] + (["-e", sub] if sub else []) + ["-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and any(f in t for f in FATAL):
        symptom_hits += 1
    count_asan(t)
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        seg = t[i:]
        for k in ("pc", "r2"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
            if m:
                regs[k] = int(m.group(1), 16)
    return regs, t, how


def hx(regs, k):
    return hex(regs[k]) if k in regs else "none"


def count_asan(t):
    global asan_hits
    asan_hits += t.count("AddressSanitizer") + t.count("runtime error:")


def msession(name, words, init, timeout=60):
    """One cold run with SEVERAL accesses: r3 = MEMC and the `init` registers, then each word placed with `put w` at the next word
    from CODE and stepped once, then one `reg`.  Returns (regs, text, how, announce-line count)."""
    global symptom_hits
    cmds = (["r3=0x%x" % MEMC] + ["%s=0x%x" % (r, v) for r, v in init] +
            ["put w 0x%x, 0x%08x" % (CODE + 4 * i, w) for i, w in enumerate(words)] + ["pc=0x%x" % CODE] +
            ["step 1"] * len(words) + ["reg", "quit"])
    argv = [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and any(f in t for f in FATAL):
        symptom_hits += 1
    count_asan(t)
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        seg = t[i:]
        for k in ("pc", "r2", "r4", "r5", "r6", "r7", "r8"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
            if m:
                regs[k] = int(m.group(1), 16)
    return regs, t, how, str(t.count("mvme187_memc:"))


def has(t, frag):
    return "yes" if frag in t else "no"


def prompt(t):
    return "yes" if ("GXemul> reg" in t and "cpu0:" in t[t.rfind("GXemul> reg"):]) else "no"


print("mvme187memcoob RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E mvme88k -e mvme187 -M 64 (UNMODIFIED in-tree); MEMC at 0x%x" % MEMC)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

#  No `-e` here: measured 2026-11-04, `-E nosuchmachine -e mvme187` CONSTRUCTS the mvme187 (exit 0, chipid read back) --
#  the subtype name selects the machine -- so a negative control that keeps `-e` controls nothing.
nr, _, nhow = session("neg", LD_BU(2, 3, 0), SENT, machine="nosuchmachine", sub=None, timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hx(nr, "r2")), "exit1/none", "a bogus machine runs no guest", control=True)
for nm, off, want, note in (("chipid", 0x00, 0x80, "MEMC_CHIPID"), ("chiprev", 0x04, 0x1, "DEVINIT chiprev = 1"),
                            ("memconf", 0x08, 0x3, "DEVINIT memconf for 64 MB (RTOB(3) = 32 MB)"),
                            ("ctl1id", 0x100, 0x80, "controller 1 aliases chipid")):
    r, T, how = session("ctl " + nm, LD_BU(2, 3, off), SENT)
    row("ctl %s sess" % nm, how, "exit0", "ld.bu +0x%x: exit status" % off, control=True)
    row("ctl %s r2" % nm, hx(r, "r2"), hex(want), note, control=True)
    row("ctl %s pc" % nm, hx(r, "pc"), hex(CODE + 4), "one instruction retired", control=True)

for nm, word, note in (("rd 0x0c", LD_BU(2, 3, 0x0c), "ld.bu +0x0c (first unimplemented offset)"),
                       ("rd 0x7c", LD_BU(2, 3, 0x7c), "ld.bu +0x7c (first byte past the struct)"),
                       ("rd 0xff", LD_BU(2, 3, 0xff), "ld.bu +0xff (the last offset)"),
                       ("wr cnf", ST_B(2, 3, 0x08), "st.b +0x08 (memconf write)")):
    r, T, how = session(nm, word, 0x7 if nm.startswith("wr") else SENT)
    row(nm + " session", how, "exit0", note + ": survives")
    row(nm + " prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ======================================================= MULTI-ACCESS ROWS (R3-R6) ==
#  R3: a memconf store, the memconf load, a load past the struct, a second memconf store -- two announce lines, one per category.
r, T, how, nl = msession("R3", [ST_B(5, 3, 0x08), LD_BU(2, 3, 0x08), LD_BU(4, 3, 0x7c), ST_B(6, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x07), ("r6", 0x05)])
row("R3 session", how, "exit0", "four accesses in one run: survives")
row("R3 cnf r2", hx(r, "r2"), hex(0x3), "memconf still reads 3: the store was not kept")
row("R3 7c r4", hx(r, "r4"), hex(0), "the past-struct load reads 0")
row("R3 pc", hx(r, "pc"), hex(CODE + 16), "four instructions retired")
row("R3 lines", nl, "2", "one announce per category, each latched")
row("R3 cnf line", has(T, "memconf write 0x7 (controller 0) ignored"), "yes", "the memconf store is announced")
row("R3 7c line", has(T, "unimplemented read from offset 0x7c (controller 0)"), "yes", "the default-arm read is announced")
row("R3 no 0x5", has(T, "memconf write 0x5"), "no", "the second memconf store is latched quiet")
#  R4: four loads past the model, the last through controller 1 -- one announce, every load reads 0, pc advances.
r, T, how, nl = msession("R4", [LD_BU(2, 3, 0x0c), LD_BU(4, 3, 0x7c), LD_BU(5, 3, 0xff), LD_BU(6, 3, 0x10c)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT)])
row("R4 session", how, "exit0", "four default-arm loads: survives")
row("R4 0c", hx(r, "r2"), hex(0), "ld.bu +0x0c reads 0")
row("R4 7c", hx(r, "r4"), hex(0), "ld.bu +0x7c reads 0")
row("R4 ff", hx(r, "r5"), hex(0), "ld.bu +0xff reads 0")
row("R4 10c", hx(r, "r6"), hex(0), "ld.bu +0x10c (controller 1) reads 0")
row("R4 pc", hx(r, "pc"), hex(CODE + 16), "no fault: four instructions retired")
row("R4 lines", nl, "1", "one announce for the device, both controllers")
row("R4 line text", has(T, "unimplemented read from offset 0xc (controller 0)"), "yes", "the first offset is the one named")
#  R5: a default-arm store, the load back, an aliased store -- the store is not kept, the write is announced once with its value.
r, T, how, nl = msession("R5", [ST_B(5, 3, 0x18), LD_BU(2, 3, 0x18), ST_B(5, 3, 0x118)], [("r2", SENT), ("r5", 0x5a)])
row("R5 session", how, "exit0", "store, load back, aliased store: survives")
row("R5 r2", hx(r, "r2"), hex(0), "the default-arm store was not kept")
row("R5 pc", hx(r, "pc"), hex(CODE + 12), "three instructions retired")
row("R5 lines", nl, "1", "one announce for the device")
row("R5 line text", has(T, "unimplemented write to offset 0x18 (controller 0): 0x5a (once)"), "yes", "the write names its value")
#  R6: the six served reads through both controllers -- the fold, the per-field arms, and no announce on a served offset.
r, T, how, nl = msession("R6", [LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04), LD_BU(5, 3, 0x08), LD_BU(6, 3, 0x100), LD_BU(7, 3, 0x104),
                                LD_BU(8, 3, 0x108)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT), ("r7", SENT), ("r8", SENT)])
row("R6 session", how, "exit0", "six served loads: survives")
row("R6 00", hx(r, "r2"), hex(0x80), "chipid")
row("R6 04", hx(r, "r4"), hex(0x1), "chiprev")
row("R6 08", hx(r, "r5"), hex(0x3), "memconf")
row("R6 100", hx(r, "r6"), hex(0x80), "controller 1 chipid (the fold)")
row("R6 104", hx(r, "r7"), hex(0x1), "controller 1 chiprev")
row("R6 108", hx(r, "r8"), hex(0x3), "controller 1 memconf")
row("R6 pc", hx(r, "pc"), hex(CODE + 24), "six instructions retired")
row("R6 lines", nl, "0", "no announce on a served offset")
row("asan reports", str(asan_hits), "0", "no sanitizer report in any session (R1, R2)")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("MVME187_MEMC_RESULT=%d/%d" % (n_ok, len(rows)))
print("MVME187_MEMC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("MVME187_MEMC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("MVME187_MEMC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("MVME187_MEMC_PROBE_DONE")
