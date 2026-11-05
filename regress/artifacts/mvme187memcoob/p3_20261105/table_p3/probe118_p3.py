#!/usr/bin/env python3
"""mvme187memcoob -- DETECTOR (built on its rung-3 witness) for the MVME187 memory controller, dev_mvme187.c.

DEFECT (filed 2026-10-02).  DEVICE_ACCESS(mvme187_memc) ended the emulator (fatal() + exit(1)) on a store to memconf (+0x08) and on any
offset its switch did not name, and indexed the 124-byte register struct with the folded offset (0..0xff) before the switch -- an
out-of-bounds read in the C source for 0x7c..0xff whose value the exiting arms never used.

THE FIX (#NNN).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
folds onto the same image; a memconf store is not kept and is announced once per device; any other offset reads 0, a store there is
not kept, and the first such access is announced once per device with its direction, offset, controller and (for a store) value.  No
indexed read remains: the three served arms read their own fields and the default arm reads none.

WHAT THE ROWS MEASURE.  Cold `-E mvme88k -e mvme187 -M 64` debugger runs (UNMODIFIED in-tree) with r3 = 0xfff43000 (MVME187_MEM_CTLR).
The witness rows place one m88k ld.bu / st.b with `put w` and step it once.  The controls read chipid, chiprev, memconf and controller
1's chipid: their session and pc rows, with `neg apparatus`, are the nine APPARATUS PINS (the CONTROL rows), and their r2 rows pin the
per-field reads.  The four sessions the old code ended (loads of the unserved offsets +0x0c, +0x7c and +0xff, and a memconf store) must
survive to the prompt.  The latch rows need several accesses in ONE emulator lifetime, so msession() places each word at the next word
from 0x10000, steps each once, sends each load to its own register (r2, r4-r15, each seeded with 0x55555555 so a load that does not
retire cannot read as a green 0) and reads them all at the end.  R3: a memconf store of 0xff, the memconf load (3: no bit kept), a
load at +0x7c (0), a controller-1 memconf store; exactly two announce lines, one per category, none naming the second store.  R4: the
chipid and chiprev loads, then four unserved-offset loads, the last through controller 1; the served loads read their fields, the
rest read 0, pc advances, one announce naming offset 0xc.  R5: a default-arm store, the load back (0), an aliased store; one announce
carrying the value.  R6: the six served reads through both controllers; no announce.  R7: through controller 1, a default load, a
memconf load (3) and a memconf store; two announces, both naming controller 1.  R8: a memconf store and a default load set both
latches, then the twelve bytes +0x7c..+0x87 are read one by one; every one reads 0.  Every notice fragment a row matches runs to the
notice's closing " (once) ]".  Row names are at most 16 characters (the gate's two-space anchor).  The multi-access sessions are six:
R3, R4, R5, R6, R7 and R8.

CLAUSE (e) -- catches (test-variant table 3, artifacts/mvme187memcoob/r3_20261105/table3/SCORES.txt, PRETABLE_3.out written before
it; all 63 of 63 variants red on this probe as predicted: 28 on exactly their predicted rows, and 35 predicted 'at least' -- table
2's 29 at their table-2 rows, six of the new ones at the rows named -- each on a superset).
Table 3 adds the class closure of the repair-3 ruling (artifacts/mvme187memcoob/p2r_20261105/ADJ_MYTHOS.md): either latch's test
or set conditioned on the controller (N1, N2, N3); the fold clear widened by any one of bits 0-7 (FCL_b0..FCL_b6, N4) and the fold
test widened by bit 7 (N5); the selector dropping any one of its eight bits (SEL_b0..SEL_b7) or made word-granular (N21); a memconf
store keeping bit 0, bit 1 or both (N6), kept only through controller 1 (N7) or only once the latch is set (N19); a default store
kept only through controller 1 (N8); a memconf store written into chiprev or chipid and a default store into memconf or chipid
(N9a-N9d); the store's read length or the read's write-back length hard-coded to 1 (RLEN1, WLEN1); the memconf latch gated on a
nonzero value (IDATA_GATE).  Table 2's 29, re-run here: each removed defect reinstated verbatim -- the memconf store's exit (B1),
the default arm's exit (B2), the indexed read before the switch (B3: R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4); the memconf
store kept, whole
(ACCEPT) or above the size code (T2_keepstore); the default arm failing the access (FAULT); either latch's test inverted or its
set dropped; one latch shared by both categories; either latch made per-controller (D6, T2_mlatch_perctl) or the memconf latch
qualified by controller (T2_mlatch_ctl1); the memconf latch set on reads (T2_mlatch_hoist); a served read of chipid, chiprev or
memconf setting the default latch (T2_dlatch_rd00/04/08); the fold mask narrowed; the controller number never set, or replaced
by 0 in the memconf notice (T2_mnotice_ctl0); chiprev reading chipid and chipid reading chiprev (D9, T2_D9b); memconf losing its
field read; the memconf notice keyed on reads; a default-arm store kept and read back; the store notice losing its value, or the
read notice gaining one (T2_valprint); the notice's direction swapped.  Tables 1 and 2 (the then 56- and 74-row probes,
det_20261104/table1/ and table2/) caught all 19 and all 29 of theirs.  Stores to the served offsets +0x00 and +0x04 are dropped
silently (R12 00 r2, R12 04 r4: a byte store of 0 leaves chipid and chiprev reading 0x80 and 0x1); a served case that kept its
store would red them -- DERIVED, no variant of that shape ran.
  discloses, not claimed: multi-axis latch joints, among them a write notice whose first default access is through controller 1
(no single edit distinguishes it: the notice is one call); an OR-keep of memconf bits 0 and 1 (`memconf |= idata & 3`), which is
unobservable here because DEVINIT already sets both bits -- a limit of size code 3, not of the rows (a RAM size whose code has bit 0
or 1 clear would settle it); accesses wider than a byte, rowed only at +0x00 (a word load) and +0x08 (a word store, a halfword
load); +0x180 reaches the function only because DEVINIT registers a 0x200-byte window (read at memory_device_register); R8's catch of the reinstated indexed read (B3) holds while the two latches begin within
4 bytes after memcreg -- the struct comment pins that, and the gate's source check (no `memcreg)[` and no `[relative_addr]` in
dev_mvme187.c) covers latches moved before it; and the sanitizer legs (artifacts/mvme187memcoob/det_20261104/asan/, READING.md with
its errata).  Measured: with the indexed read reinstated (B3), the loads at +0x7c and +0xff produce 0 sanitizer reports on both
sanitizer builds.  At +0x7c..+0x83 the byte lies inside the 132-byte allocation, on the latches, so no sanitizer can report it.  At
+0xff the byte lies 123 bytes past the allocation; that it goes unreported is REASONED, not measured (it lands in a neighbouring heap
chunk whose poisoning depends on allocator state, and no shadow dump exists for that access).  R8's loads at +0x84..+0x87 lie in the
allocation's partial granule and are expected to report under ASan on the offline legs (REASONED).  On the plain build the catches
for B3 are R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4 (table 3).  MVME187_MEMC_ASAN=n counts one per "ERROR: AddressSanitizer"
or "runtime error:" line; it is informational, read by the offline legs, and no row.  On this 118-row probe the pre-fix build
scores 31 of the 118 rows with the symptom PRESENT (25 of the then 74-row probe, 27 of the 56-row one), and the three null media --
/bin/true, an absent binary, /bin/false -- each CONTROL=FAIL (r3_20261105/table3/SCORES.txt).

Sentinel: MVME187_MEMC_PROBE_DONE (plus MVME187_MEMC_RESULT=n/N, MVME187_MEMC_CONTROL=OK|FAIL, MVME187_MEMC_SYMPTOM=PRESENT|ABSENT,
MVME187_MEMC_RED=none|<names>, and the informational MVME187_MEMC_ASAN=n).  Session transcripts go to the optional [workdir].
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
FATAL = ("unimplemented read from offset", "unimplemented write to offset", "not yet implemented!")


def LD_BU(rd, rs1, imm):    # m88k ld.bu: op26 0x03, d16 offset (the encoding vme_default_probe.py uses)
    return (0x03 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def ST_B(rs, rs1, imm):     # m88k st.b: op26 0x0b
    return (0x0b << 26) | (rs << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_HU(rd, rs1, imm):    # m88k ld.hu: op26 0x02 (pcc2_width_probe.py's table)
    return (0x02 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_W(rd, rs1, imm):     # m88k ld (word): op26 0x05
    return (0x05 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def ST_W(rs, rs1, imm):     # m88k st (word): op26 0x09
    return (0x09 << 26) | (rs << 21) | (rs1 << 16) | (imm & 0xffff)


assert LD_BU(2, 3, 0x7c) == 0x0C43007C and ST_B(2, 3, 0x08) == 0x2C430008
assert LD_HU(7, 3, 0x08) == 0x08E30008 and LD_W(6, 3, 0) == 0x14C30000 and ST_W(5, 3, 0x08) == 0x24A30008

rows = []
controls = []
symptom_hits = 0
asan_hits = 0                # sanitizer REPORTS across every session (informational: MVME187_MEMC_ASAN, read by the offline legs)


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
    """One per report: an "ERROR: AddressSanitizer" line or a UBSan "runtime error:" line (a report's SUMMARY line repeats the
    AddressSanitizer token, so a substring count would score one report twice)."""
    global asan_hits
    asan_hits += sum(1 for line in t.split("\n") if "ERROR: AddressSanitizer" in line or "runtime error:" in line)


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
        for k in ("pc", "r2") + tuple("r%d" % i for i in range(4, 16)):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
            if m:
                regs[k] = int(m.group(1), 16)
    return regs, t, how, str(t.count("mvme187_memc:"))


def has(t, frag):
    return "yes" if frag in t else "no"


def prompt(t):
    return "yes" if ("GXemul> reg" in t and "cpu0:" in t[t.rfind("GXemul> reg"):]) else "no"


print("mvme187memcoob DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
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
    row("ctl %s r2" % nm, hx(r, "r2"), hex(want), note)
    row("ctl %s pc" % nm, hx(r, "pc"), hex(CODE + 4), "one instruction retired", control=True)

for nm, word, note in (("rd 0x0c", LD_BU(2, 3, 0x0c), "ld.bu +0x0c (first unimplemented offset)"),
                       ("rd 0x7c", LD_BU(2, 3, 0x7c), "ld.bu +0x7c (first byte past the struct)"),
                       ("rd 0xff", LD_BU(2, 3, 0xff), "ld.bu +0xff (the last offset)"),
                       ("wr cnf", ST_B(2, 3, 0x08), "st.b +0x08 (memconf write)")):
    r, T, how = session(nm, word, 0x7 if nm.startswith("wr") else SENT)
    row(nm + " session", how, "exit0", note + ": survives")
    row(nm + " prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ======================================================= MULTI-ACCESS ROWS (R3-R6) ==
#  R3: a memconf store of 0xff, the memconf load, a load at +0x7c, a controller-1 memconf store, the controller-1 memconf load, a second
#  controller-0 memconf store (0x00, from r0), and loads of memconf, chipid and chiprev -- two announce lines, one per category.  The
#  repair-3 additions (ADJ_MYTHOS.md, mvme187memcoob p2r): every bit of memconf written both set (0xff) and clear (0x00) and read back
#  (N6), a load after the controller-1 store (N7, N19), the served fields read after a memconf store (N9), a second controller-0 store
#  that must stay quiet (N1).
r, T, how, nl = msession("R3", [ST_B(5, 3, 0x08), LD_BU(2, 3, 0x08), LD_BU(4, 3, 0x7c), ST_B(6, 3, 0x108), LD_BU(9, 3, 0x108),
                                ST_B(0, 3, 0x08), LD_BU(11, 3, 0x08), LD_BU(12, 3, 0x00), LD_BU(13, 3, 0x04)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xff), ("r6", 0x05), ("r9", SENT), ("r11", SENT), ("r12", SENT),
                          ("r13", SENT)])
row("R3 session", how, "exit0", "nine accesses in one run: survives")
row("R3 cnf r2", hx(r, "r2"), hex(0x3), "memconf still reads 3: no bit of 0xff was kept")
row("R3 7c r4", hx(r, "r4"), hex(0), "the past-struct load reads 0")
row("R3 108 r9", hx(r, "r9"), hex(0x3), "memconf via controller 1 after its store: still 3")
row("R3 cnf0 r11", hx(r, "r11"), hex(0x3), "memconf after a 0x00 store: still 3")
row("R3 00 r12", hx(r, "r12"), hex(0x80), "chipid after the memconf stores")
row("R3 04 r13", hx(r, "r13"), hex(0x1), "chiprev after the memconf stores")
row("R3 pc", hx(r, "pc"), hex(CODE + 36), "nine instructions retired")
row("R3 lines", nl, "2", "one announce per category, each latched")
row("R3 cnf line", has(T, "memconf write 0xff (controller 0) ignored, not modelled (once) ]"), "yes",
    "the memconf store is announced")
row("R3 7c line", has(T, "unimplemented read from offset 0x7c (controller 0) (once) ]"), "yes", "the default-arm read is announced")
row("R3 no 0x5", has(T, "memconf write 0x5"), "no", "the controller-1 memconf store is latched quiet")
row("R3 no 0x0", has(T, "memconf write 0x0"), "no", "the second controller-0 store is latched quiet")
#  R4: the chipid and chiprev loads, then four unserved-offset loads, the last through controller 1 -- one announce, the served loads
#  read their fields and no served read sets the default latch (ADJ_MYTHOS.md M26/X1), the rest read 0, pc advances.
r, T, how, nl = msession("R4", [LD_BU(7, 3, 0x00), LD_BU(8, 3, 0x04), LD_BU(2, 3, 0x0c), LD_BU(4, 3, 0x7c), LD_BU(5, 3, 0xff),
                                LD_BU(6, 3, 0x10c)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT), ("r7", SENT), ("r8", SENT)])
row("R4 session", how, "exit0", "two served, four default-arm loads: survives")
row("R4 00 r7", hx(r, "r7"), hex(0x80), "chipid, read first")
row("R4 04 r8", hx(r, "r8"), hex(0x1), "chiprev, read second")
row("R4 0c", hx(r, "r2"), hex(0), "ld.bu +0x0c reads 0")
row("R4 7c", hx(r, "r4"), hex(0), "ld.bu +0x7c reads 0")
row("R4 ff", hx(r, "r5"), hex(0), "ld.bu +0xff reads 0")
row("R4 10c", hx(r, "r6"), hex(0), "ld.bu +0x10c (controller 1) reads 0")
row("R4 pc", hx(r, "pc"), hex(CODE + 24), "no fault: six instructions retired")
row("R4 lines", nl, "1", "one announce for the device, both controllers")
row("R4 line text", has(T, "unimplemented read from offset 0xc (controller 0) (once) ]"), "yes",
    "the first default offset is the one named")
#  R5: a default-arm store, the load back, an aliased store -- the store is not kept, the write is announced once with its value.
r, T, how, nl = msession("R5", [ST_B(5, 3, 0x18), LD_BU(2, 3, 0x18), ST_B(5, 3, 0x118)], [("r2", SENT), ("r5", 0x5a)])
row("R5 session", how, "exit0", "store, load back, aliased store: survives")
row("R5 r2", hx(r, "r2"), hex(0), "the default-arm store was not kept")
row("R5 pc", hx(r, "pc"), hex(CODE + 12), "three instructions retired")
row("R5 lines", nl, "1", "one announce for the device")
row("R5 line text", has(T, "unimplemented write to offset 0x18 (controller 0): 0x5a (once) ]"), "yes",
    "the write names its value")
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
#  R7: through controller 1, a default load, a memconf load and a memconf store -- both notices name controller 1 (the fix's comment
#  says the number is reported in the notices), and the memconf LOAD must not set the memconf latch (ADJ_MYTHOS.md M5, M25).
r, T, how, nl = msession("R7", [LD_BU(2, 3, 0x10c), LD_BU(4, 3, 0x108), ST_B(5, 3, 0x108)], [("r2", SENT), ("r4", SENT), ("r5", 0x07)])
row("R7 session", how, "exit0", "three controller-1 accesses: survives")
row("R7 r2", hx(r, "r2"), hex(0), "the default load reads 0")
row("R7 108 r4", hx(r, "r4"), hex(0x3), "the controller-1 memconf load reads 3")
row("R7 pc", hx(r, "pc"), hex(CODE + 12), "three instructions retired")
row("R7 lines", nl, "2", "two announces: default, then memconf")
row("R7 line text", has(T, "unimplemented read from offset 0xc (controller 1) (once) ]"), "yes", "the notice names controller 1")
row("R7 cnf line", has(T, "memconf write 0x7 (controller 1) ignored, not modelled (once) ]"), "yes",
    "the memconf notice names controller 1")
#  R8: the reinstated indexed read (B3) on either byte order (ADJ_MYTHOS.md M3, X5): both latches set, then the twelve bytes past
#  memcreg read one by one.  The fix's default arm forwards no image byte, so every one reads 0; the old read forwarded the latches.
#  r5 is the store's source (0x7) and also +0x7d's destination, so it starts non-zero too.
r, T, how, nl = msession("R8", [ST_B(5, 3, 0x08), LD_BU(2, 3, 0x0c)] + [LD_BU(4 + i, 3, 0x7c + i) for i in range(12)],
                         [("r2", SENT), ("r5", 0x07)] + [("r%d" % (4 + i), SENT) for i in range(12) if 4 + i != 5])
row("R8 session", how, "exit0", "both latches set, then twelve loads: survives")
for i in range(12):
    row("R8 %02x r%d" % (0x7c + i, 4 + i), hx(r, "r%d" % (4 + i)), hex(0), "+0x%x reads 0: no image byte forwarded" % (0x7c + i))
row("R8 pc", hx(r, "pc"), hex(CODE + 56), "fourteen instructions retired")
row("R8 lines", nl, "2", "one announce per category")
#  R9: controller 1 first, memconf: a 0x00 store, then a 0xff store, then memconf read through controller 1 and controller 0 -- the
#  latch is set by the FIRST store whatever its value (an idata-gated latch announces the second; ADJ_MYTHOS.md change 5), it is set
#  through controller 1 (N2), and no store is kept by either controller (N6, N7, N19).
r, T, how, nl = msession("R9", [ST_B(0, 3, 0x108), ST_B(5, 3, 0x108), LD_BU(2, 3, 0x108), LD_BU(4, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xff)])
row("R9 session", how, "exit0", "two controller-1 memconf stores: survives")
row("R9 108 r2", hx(r, "r2"), hex(0x3), "memconf via controller 1: still 3")
row("R9 08 r4", hx(r, "r4"), hex(0x3), "memconf via controller 0: still 3")
row("R9 lines", nl, "1", "one announce: the first store")
row("R9 no 0xff", has(T, "memconf write 0xff"), "no", "the second store is latched quiet")
row("R9 cnf line", has(T, "memconf write 0x0 (controller 1) ignored, not modelled (once) ]"), "yes",
    "the first store, value 0, is announced")
row("R9 pc", hx(r, "pc"), hex(CODE + 16), "four instructions retired")
#  R10: controller 1 first, default: two default loads, a default store through controller 1, then the stored offset read back through
#  both controllers, memconf, chipid and chiprev -- the default latch is set through controller 1 (N3), no default store is kept (N8),
#  and a default store reaches no served field (N9; change 3).
r, T, how, nl = msession("R10", [LD_BU(2, 3, 0x10c), LD_BU(4, 3, 0x110), ST_B(5, 3, 0x118), LD_BU(6, 3, 0x118), LD_BU(7, 3, 0x18),
                                 LD_BU(8, 3, 0x08), LD_BU(9, 3, 0x00), LD_BU(10, 3, 0x04)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x5a), ("r6", SENT), ("r7", SENT), ("r8", SENT), ("r9", SENT),
                          ("r10", SENT)])
row("R10 session", how, "exit0", "controller-1 default accesses first: survives")
row("R10 118 r6", hx(r, "r6"), hex(0), "the default store was not kept (ctl 1)")
row("R10 18 r7", hx(r, "r7"), hex(0), "nor seen through controller 0")
row("R10 08 r8", hx(r, "r8"), hex(0x3), "memconf after a default store")
row("R10 00 r9", hx(r, "r9"), hex(0x80), "chipid after a default store")
row("R10 04 r10", hx(r, "r10"), hex(0x1), "chiprev after a default store")
row("R10 lines", nl, "1", "one announce: the first default access")
row("R10 line text", has(T, "unimplemented read from offset 0xc (controller 1) (once) ]"), "yes",
    "the first default access names controller 1")
row("R10 pc", hx(r, "pc"), hex(CODE + 32), "eight instructions retired")
#  R11: the first default access is +0xff through controller 0 (a fold test widened by bit 7 would name controller 1: N5), then the
#  fold and selector edges -- +0x180 (a fold clear widened by bit 7 reads chipid: N4), the sub-word aliases +0x01 and +0x0a (N21), the
#  fold-clear bits 0, 1, 5, 6 (+0x101, +0x102, +0x120, +0x140: change 1) and the selector bits 5, 6 (+0x20, +0x40: change 2).  The
#  window is 0x200 bytes (DEVINIT), so +0x180 reaches the function.  Every one reads 0 on the fix.
r, T, how, nl = msession("R11", [LD_BU(2, 3, 0xff), LD_BU(4, 3, 0x180), LD_BU(5, 3, 0x01), LD_BU(6, 3, 0x0a), LD_BU(7, 3, 0x101),
                                 LD_BU(8, 3, 0x102), LD_BU(9, 3, 0x120), LD_BU(10, 3, 0x140), LD_BU(11, 3, 0x20),
                                 LD_BU(12, 3, 0x40)],
                         [("r%d" % i, SENT) for i in (2, 4, 5, 6, 7, 8, 9, 10, 11, 12)])
row("R11 session", how, "exit0", "ten default loads: survives")
row("R11 180 r4", hx(r, "r4"), hex(0), "+0x180 folds to 0x80: reads 0")
row("R11 01 r5", hx(r, "r5"), hex(0), "+0x01 is not chipid")
row("R11 0a r6", hx(r, "r6"), hex(0), "+0x0a is not memconf")
row("R11 101 r7", hx(r, "r7"), hex(0), "+0x101 folds to 0x01: reads 0")
row("R11 102 r8", hx(r, "r8"), hex(0), "+0x102 folds to 0x02: reads 0")
row("R11 120 r9", hx(r, "r9"), hex(0), "+0x120 folds to 0x20: reads 0")
row("R11 140 r10", hx(r, "r10"), hex(0), "+0x140 folds to 0x40: reads 0")
row("R11 20 r11", hx(r, "r11"), hex(0), "+0x20 is not chipid")
row("R11 40 r12", hx(r, "r12"), hex(0), "+0x40 is not chipid")
row("R11 line text", has(T, "unimplemented read from offset 0xff (controller 0) (once) ]"), "yes",
    "the first default access, +0xff, controller 0")
row("R11 lines", nl, "1", "one announce for the device")
row("R11 pc", hx(r, "pc"), hex(CODE + 40), "ten instructions retired")
#  R12: a WORD store of 0x000000ff to memconf first (the notice prints the whole value: a read length hard-coded to 1 prints 0x0 on this
#  big-endian CPU), byte stores of 0 to chipid and chiprev (dropped silently: change 4), then chipid and chiprev by byte, chipid by
#  WORD (a write-back length hard-coded to 1 returns the byte to the wrong lane), memconf by HALFWORD and by byte (N15 overturned).
r, T, how, nl = msession("R12", [ST_W(5, 3, 0x08), ST_B(0, 3, 0x00), ST_B(0, 3, 0x04), LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04),
                                 LD_W(6, 3, 0x00), LD_HU(7, 3, 0x08), LD_BU(8, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xff), ("r6", SENT), ("r7", SENT), ("r8", SENT)])
row("R12 session", how, "exit0", "word, halfword and served-offset accesses")
row("R12 cnf line", has(T, "memconf write 0xff (controller 0) ignored, not modelled (once) ]"), "yes",
    "the word store's whole value is announced")
row("R12 00 r2", hx(r, "r2"), hex(0x80), "chipid kept after a store to it")
row("R12 04 r4", hx(r, "r4"), hex(0x1), "chiprev kept after a store to it")
row("R12 w00 r6", hx(r, "r6"), hex(0x80), "chipid by word: 0x00000080")
row("R12 h08 r7", hx(r, "r7"), hex(0x3), "memconf by halfword: 0x0003")
row("R12 08 r8", hx(r, "r8"), hex(0x3), "memconf after the word store: still 3")
row("R12 lines", nl, "1", "one announce: the memconf word store")
row("R12 pc", hx(r, "pc"), hex(CODE + 32), "eight instructions retired")

n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("MVME187_MEMC_RESULT=%d/%d" % (n_ok, len(rows)))
print("MVME187_MEMC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("MVME187_MEMC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("MVME187_MEMC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("MVME187_MEMC_ASAN=%d" % asan_hits)
print("MVME187_MEMC_PROBE_DONE")
