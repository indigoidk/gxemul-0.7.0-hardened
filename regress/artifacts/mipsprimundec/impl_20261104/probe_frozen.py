#!/usr/bin/env python3
"""mipsprimundec -- RUNG-3 WITNESS for MIPS primary opcodes the translator has no working arm for.

DEFECT (filed 2026-10-22).  src/cpus/cpu_mips_instr.c, X(to_be_translated): the primary-opcode switch has no case for
0x1d (JALX), 0x32 (LWC2), 0x36 (LDC2), 0x3a (SWC2), 0x3b (SWC3) and 0x3e (SDC2), so they fall to `default: goto bad`;
the 0x1e (MDMX, off the R5900) and 0x33 (LWC3) cases print a TODO and also go to `bad`.  `bad:` stops the emulated
CPU ("UNIMPLEMENTED instruction", "All machines stopped") -- one guest word, no privilege test, no exception delivered.

WHAT THE ROWS MEASURE (each session is one cold `-E testmips` debugger run on an UNMODIFIED in-tree machine: `-C R4400`
(ISA III, the 64-bit translator) and `-C R3000` (ISA I, the 32-bit one) -- cpu_mips_instr.c is compiled twice, once under
MODE32.  Not the default testmips CPU: that is the MIPS64 5KE, where 0xcc000000 is PREF, a legal prefetch (`pref 0x0,0(zr)`,
PC +4, no exception: artifacts/mipsprimundec/draft_20261104/table_head.out row "5KE lwc3"), so LWC3 is a defect only below ISA IV, as filed).  The word
under test is placed at PLANT with `put w`, the PC set there, one `step`, then `reg` and `reg ,0`.  CONTROL rows prove
the apparatus on each CPU: an ordinary `addiu` executes (`live`); the fork's own COP2 arm raises Coprocessor Unusable
with CE=2 (`cpu2`) and, on the R3000, LDC1 below ISA II raises Reserved Instruction (`ri`) -- so the probe sees an
architectural exception arrive (EPC = PLANT, ExcCode 10 or 11, PC = the general exception vector) whenever one is
raised.  WITNESS rows, for each of the eight words on each CPU: no "UNIMPLEMENTED instruction" text, EPC = PLANT, PC =
the general vector, ExcCode 10 (RI) or 11 (CpU).  On the pre-fix build every one of those sessions stops the CPU with
EPC and Cause untouched (MIPS_PRIMUNDEC_SYMPTOM=PRESENT).

NOT CLAIMED (the design ruling decides them; owed with the fix): WHICH exception each word takes (RI or CpU, and the CE
field) -- the `exc` rows accept either; the R5900's MDMX/LQ arm; LWC3/PREF at ISA IV and above; the pmax and arc rig
machines (testmips only here); user mode; a word in a branch delay slot (EPC = the branch, Cause.BD set).

Sentinel: MIPS_PRIMUNDEC_PROBE_DONE (plus MIPS_PRIMUNDEC_RESULT=n/N, _CONTROL=OK|FAIL, _SYMPTOM=PRESENT|ABSENT,
_RED=none|<names>).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: mips_primundec_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="mips_primundec_")
DUMMY = os.path.join(_TMPDIR, "zero.bin")
open(DUMMY, "wb").write(bytes(4))

PLANT64 = 0xffffffff80020000
CPUS = {   # tag: (extra argv, PLANT as the debugger prints it, the general exception vector with BEV clear)
    "64": (["-C", "R4400"], PLANT64, 0xffffffff80000180),
    "32": (["-C", "R3000"], 0x80020000, 0x80000080),
}
WORDS = [("jalx", 0x74000000), ("mdmx", 0x78000000), ("lwc2", 0xc8000000), ("lwc3", 0xcc000000),
         ("ldc2", 0xd8000000), ("swc2", 0xe8000000), ("swc3", 0xec000000), ("sdc2", 0xf8000000)]
STOP = "UNIMPLEMENTED instruction"

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


def session(name, word, extra, machine="testmips", timeout=60, count_symptom=False):
    """One cold run: place `word` at PLANT, step it once, read `reg` and `reg ,0`.  Returns (r, text, how)."""
    global symptom_hits
    cmds = ["put w 0x%x, 0x%08x" % (PLANT64, word), "pc=0x%x" % PLANT64, "step 1", "reg", "reg ,0", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine] + list(extra) + ["0x%x:%s" % (PLANT64, DUMMY)]
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
    if count_symptom and STOP in t:
        symptom_hits += 1
    r = {"how": how}
    i = t.rfind("GXemul> reg\n")
    j = t.rfind("GXemul> reg ,0")
    if 0 <= i < j:
        m = re.search(r"\bpc\s*=\s*(?:0x)?([0-9a-fA-F]+)", t[i:j])
        if m:
            r["pc"] = int(m.group(1), 16)
        m = re.search(r"\bv0\s*=\s*(?:0x)?([0-9a-fA-F]+)", t[i:j])
        if m:
            r["v0"] = int(m.group(1), 16)
    if j >= 0:
        seg = t[j:]
        m = re.search(r"\bepc\s*=\s*(?:0x)?([0-9a-fA-F]+)", seg)
        if m:
            r["epc"] = int(m.group(1), 16)
        m = re.search(r"cause:\s+\S+ \(exccode (\d+)\) ce=(\d+)", seg)
        if m:
            r["exc"] = (int(m.group(1)), int(m.group(2)))
    r["stopped"] = "present" if STOP in t else "absent"
    return r, t, how


def hx(r, k):
    return hex(r[k]) if k in r else "none"


def exc(r):
    return "%d/%d" % r["exc"] if "exc" in r else "none"


def trap(r):
    if "exc" not in r:
        return "none"
    return "trap" if r["exc"][0] in (10, 11) else "exccode%d" % r["exc"][0]


print("mipsprimundec RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E testmips (UNMODIFIED in-tree; -C R4400 for the 64-bit translator, -C R3000 for the MODE32 one)")
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

nr, _, nhow = session("neg", 0x24021234, [], machine="nosuchmachine", timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hx(nr, "pc")), "exit1/none", "a bogus machine runs no guest", control=True)

for tag, (extra, plant, vec) in sorted(CPUS.items(), reverse=True):
    # ---------------------------------------------------------------- controls
    r, T, how = session(tag + " live", 0x24021234, extra)            # addiu v0,zero,0x1234
    row(tag + " live v0", hx(r, "v0"), hex(0x1234), "addiu v0,zero,0x1234 executed", control=True)
    row(tag + " live pc", hx(r, "pc"), hex(plant + 4), "one instruction retired", control=True)
    row(tag + " live epc", hx(r, "epc"), hex(0), "no exception on an ordinary word", control=True)
    r, T, how = session(tag + " cpu2", 0x48000000, extra)            # COP2: the fork's own CpU arm
    row(tag + " cpu2 exc", exc(r), "11/2", "COP2: Coprocessor Unusable, CE=2", control=True)
    row(tag + " cpu2 epc", hx(r, "epc"), hex(plant), "EPC = the word's PC", control=True)
    row(tag + " cpu2 pc", hx(r, "pc"), hex(vec), "PC = the general exception vector", control=True)
    if tag == "32":
        r, T, how = session(tag + " ri", 0xd4000000, extra)          # LDC1 below ISA II: the fork's own RI arm
        row(tag + " ri exc", exc(r), "10/0", "LDC1 on ISA I: Reserved Instruction", control=True)
        row(tag + " ri epc", hx(r, "epc"), hex(plant), "EPC = the word's PC", control=True)
        row(tag + " ri pc", hx(r, "pc"), hex(vec), "PC = the general exception vector", control=True)
    # ----------------------------------------------------------- witness rows
    for nm, w in WORDS:
        r, T, how = session("%s %s" % (tag, nm), w, extra, count_symptom=True)
        row("%s %s stop" % (tag, nm), r["stopped"], "absent", "0x%08x: the CPU is not stopped" % w)
        row("%s %s exc" % (tag, nm), trap(r), "trap", "ExcCode 10 (RI) or 11 (CpU)")
        row("%s %s epc" % (tag, nm), hx(r, "epc"), hex(plant), "EPC = the word's PC")
        row("%s %s pc" % (tag, nm), hx(r, "pc"), hex(vec), "PC = the general exception vector")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("MIPS_PRIMUNDEC_RESULT=%d/%d" % (n_ok, len(rows)))
print("MIPS_PRIMUNDEC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("MIPS_PRIMUNDEC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("MIPS_PRIMUNDEC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("MIPS_PRIMUNDEC_PROBE_DONE")
