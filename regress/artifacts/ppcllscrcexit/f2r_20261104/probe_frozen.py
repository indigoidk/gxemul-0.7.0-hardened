#!/usr/bin/env python3
"""ppcllscrcexit -- RUNG-3 WITNESS and DETECTOR for the PowerPC load-reserve / store-conditional handler X(llsc).

DEFECT (#579).  src/cpus/cpu_ppc_instr.c, X(llsc): the opcode-31 decoder keys on the ten-bit extended opcode alone
(`xo = (iword >> 1) & 1023`), so every word with XO 20 (lwarx), 84 (ldarx), 150 (stwcx.) or 214 (stdcx.) reaches the
handler whatever bit 31 holds.  The handler then ended the emulator process -- `fatal()` + `exit(1)` -- on the four
bit-31 forms it did not expect: lwarx/ldarx with bit 31 set, stwcx./stdcx. with bit 31 clear.  One guest instruction,
any privilege level, every modelled CPU.

ARCHITECTURE (the local extracts; cite nothing not read there):
  * lwarx/ldarx: bit 31 is a RESERVED field ("/" in the layout, Book II v2.01 ppc_vea_book2_v201.txt:1264), and
    "Reserved fields in instructions are ignored by the processor" (Book I v2.01 ppc_uisa_book1_v201.txt:432-433).
    The bit-31-set words are VALID forms: they run the one body the instruction has, and CR is not written.
  * stwcx./stdcx.: bit 31 is "1" in the layout (ppc_vea_book2_v201.txt:1305, :1307); the bit-clear words are INVALID
    forms (Book I :1122-1128 names the Store Conditional instructions), whose permitted outcomes are the illegal-
    instruction handler or boundedly undefined results (Book I :1116-1120).  This core takes the latter and performs
    the defined store-conditional, CR0 = 0b00 || EQ || XER[SO] (Book II :1323, :1337) included.

WHAT THE ROWS MEASURE.  Each session is one cold `-E bareppc -M 64` debugger run (an UNMODIFIED in-tree machine;
PPC970 at 64 bits, and `-C PPC603` for the 32-bit leg) that places one to three guest words at CODE (`stw chain`
and `stw twice` place three), seeds the registers, steps them, and reads the registers back (`reg`) and the data
bytes (`dump`).  The CONTROL rows run the four valid forms and prove the apparatus: the load brings a non-palindromic pattern into r3 (a 4-byte load and an
8-byte load assemble different values), the store-conditional after a load writes its bytes and sets CR to
0x2fffffff from a seed of 0xffffffff, a store with no reservation leaves memory alone and clears CR0, and XER[SO]
reaches CR0 bit 3.  The FIXED rows run the four bit-31 forms with the same seeds and want the SAME observables as
their valid twins; on the pre-fix build those sessions end at the step with the handler's fatal text, which is the
witness symptom (PPC_LLSC_SYMPTOM=PRESENT).  A row that wanted only survival would pass a handler that returned
without doing the load or the store, so every fixed form's row group demands the value, the bytes or the CR; its
`session`, `pc` and `seed` rows carry the exit status, the program counter and the seed.

CLAUSE (e) -- what this instrument catches and what it discloses:
  catches: either guard reinstated verbatim (the six bit-31 `session` rows die -- four on the 64-bit CPU, two on the
    32-bit one); a bare `return` or any other no-op at either guard site (the value/bytes/CR rows); `load` inverted or
    forced (a load word takes the store path and vice versa); `len = 8` dropped on ldarx/stdcx. or added on
    lwarx/stwcx. (the 4-byte and 8-byte patterns differ in value; they share their first four bytes); the CR0 success
    constant or the XER[SO] copy dropped; the reservation test nulled (`stw noresv`, `stw mismatch`); the failure-path
    `ll_bit` clear dropped (`stw chain`); the success-path all-CPU reservation clear dropped (`stw twice`); the RA base
    dropped, or the RT or RB field mask narrowed to four bits (`lw ra`: RA = 6, RT = 17, RB = 20); a bit-31-set lwarx
    that loads but does not reserve (`rc1 resv`); the reservation-failure path's XER[SO] copy dropped (`stw nso`); a
    bit-clear stwcx. that skips the reservation test (`rc0 noresv`).
  discloses, not claimed: ldarx/stdcx. on the 32-bit CPUs (illegal opcodes there for BOTH bit-31 values; the 32-bit
    leg runs the word forms only, as #571 left primary opcodes 58 and 62); the XOs 532 and 596 (20 and 84 with XO bit
    9 set: unassigned in Book I v2.01, and this decoder sends them to `goto bad` -- they are not this handler's words;
    the later architecture's hint is bit 31 of XO 20/84, which `lw rc1` / `ld rc1` already run); the #216 DSI returns
    (deleting one, test variant M20, scores 83/83: this instrument verifies nothing about them) and the stale-SRR0 row
    `ppcllscsrr0`; unaligned EAs; little-endian guests (the PPC core is big-endian); ncpus > 1 (the all-CPU clear is
    observed on ONE CPU only); the sampling -- RA is 0 in every session but `lw ra`, RT is 3 but for `lw ra`, two of
    eleven CPU models, one privilege level, one CR seed, two XER seeds (SO clear, SO set) -- so narrowing only the RA
    field's mask (RA never exceeds 15 in any session) is not detected; the disassembler, which prints `lwarx`/`stwcx.`
    for both bit-31 values (so `unasm census` checks the placed WORDS, never the mnemonics); the `session` rows are
    exit-status oracles, so a NON-emulator binary passes the 14 exit-status rows and an absent binary passes none --
    the instrument fails both through RESULT (pinned by equality), CONTROL=FAIL and the census (which counts the words
    PLACED, `neg` excluded, so it reads 0/35 there), never through those rows.

Sentinel: PPC_LLSC_PROBE_DONE (plus PPC_LLSC_RESULT=n/N, PPC_LLSC_CONTROL=OK|FAIL, PPC_LLSC_SYMPTOM=PRESENT|ABSENT,
PPC_LLSC_RED=none|<names>).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_llsc_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="ppc_llsc_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x10000
DATA = 0x20000           # 16-byte aligned, a different dyntrans page from CODE
DATA2 = 0x20100          # the mismatch / chain rows' second address
SENT = 0x5A5A5A5A5A5A5A5A
SEED_R3 = 0x1111111111111111
CR_SEED = 0xFFFFFFFF
PAT_HI, PAT_LO = 0xA5C3E719, 0x5A3CE817      # the data pattern: a5 c3 e7 19 5a 3c e8 17 (no byte repeats)
STW_VAL = 0xC0FFEE01                          # c0 ff ee 01
STW_VAL2 = 0x0BAD0F55                         # the second store-conditional's value, which must never land
STD_VAL = 0x0102030405060708
XER_SO = 0x80000000

rows = []
controls = []
symptom_hits = 0
census_ok = census_all = 0


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


# -------------------------------------------------------------------- encodings
XO_LWARX, XO_LDARX, XO_STWCX, XO_STDCX = 20, 84, 150, 214


def X31(xo, rt, ra, rb, bit31):
    """Opcode-31 X-form word (Book II layouts, ppc_vea_book2_v201.txt:1264 and :1305-1307)."""
    assert 0 <= rt <= 31 and 0 <= ra <= 31 and 0 <= rb <= 31 and bit31 in (0, 1)
    return ((31 << 26) | (rt << 21) | (ra << 16) | (rb << 11) | (xo << 1) | bit31) & 0xFFFFFFFF


def LI(rd, simm):
    return ((14 << 26) | (rd << 21) | (simm & 0xFFFF)) & 0xFFFFFFFF


assert X31(XO_LWARX, 3, 0, 4, 0) == 0x7C602028 and X31(XO_STWCX, 3, 0, 4, 1) == 0x7C60212D   # the smoke words

# ---------------------------------------------------------------------- sessions
DUMP_RE = re.compile(r"^0x([0-9a-f]{8,16})  ([0-9a-f]{8}) ([0-9a-f]{8}) ([0-9a-f]{8}) ([0-9a-f]{8}) ", re.M)   # 8 digits on a 32-bit CPU
UNASM_RE = re.compile(r"^[0-9a-f]{8,16}: ([0-9a-f]{8})\s", re.M)


def parse_dump(text):
    m = {}
    for mm in DUMP_RE.finditer(text):
        a = int(mm.group(1), 16)
        hx = "".join(mm.group(i) for i in range(2, 6))
        for k in range(16):
            m[a + k] = int(hx[2 * k:2 * k + 2], 16)
    return m


def session(name, steps, pre=(), machine="bareppc", cpu=None, timeout=120):
    """`pre' = debugger commands before anything else (seeds, data); `steps' = a list of (word, [commands before
    this step]) -- each word is placed at CODE + 4*i and stepped once.  Returns (regs, mem, text, how)."""
    global symptom_hits, census_ok, census_all
    cmds = ["r30=0x%x" % SENT] + list(pre)
    for i, (w, _) in enumerate(steps):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds.append("unassemble 0x%x 0x%x" % (CODE, CODE + 4 * len(steps)))
    cmds.append("pc=0x%x" % CODE)
    for i, (w, before) in enumerate(steps):
        cmds += list(before)
        cmds.append("step 1")
    cmds += ["reg", "dump 0x%x 0x%x" % (DATA, DATA + 16), "dump 0x%x 0x%x" % (DATA2, DATA2 + 16), "quit"]
    argv = [BIN, "-V", "-x", "-E", machine, "-M", "64"]
    if cpu:
        argv += ["-C", cpu]
    argv += ["0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium too: every row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if "rc-bit" in t:               # the handler's fatal text: "ll: rc-bit set?" / "sc: rc-bit not set?"
        symptom_hits += 1
    regs = {}
    idx = t.rfind("GXemul> reg")
    if idx >= 0:
        seg = t[idx:]
        for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", seg):
            regs[int(m.group(1))] = int(m.group(2), 16)
        for key in ("cr", "pc", "xer"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % key, seg)
            if m:
                regs[key] = int(m.group(1), 16)
    census_all += 0 if name == "neg" else len(steps)    # the words PLACED, known before the run (neg runs no machine)
    di = t.find("GXemul> unassemble")
    if di >= 0:
        end = t.find("GXemul> pc=", di)
        seen = [int(x, 16) for x in UNASM_RE.findall(t[di:end if end > 0 else len(t)])]
        for i, (w, _) in enumerate(steps):
            if i < len(seen) and seen[i] == w:
                census_ok += 1
    return regs, parse_dump(t), t, how


def hexr(regs, k):
    return hex(regs[k]) if k in regs else "none"


def mem(m, a, n):
    if all(a + k in m for k in range(n)):
        return "".join("%02x" % m[a + k] for k in range(n))
    return "none"


PAT8 = "%08x%08x" % (PAT_HI, PAT_LO)
SEEDS = ["r4=0x%x" % DATA, "r5=0x%x" % DATA2, "r3=0x%x" % SEED_R3, "cr=0x%x" % CR_SEED, "xer=0",
         "put w 0x%x, 0x%08x" % (DATA, PAT_HI), "put w 0x%x, 0x%08x" % (DATA + 4, PAT_LO),
         "put w 0x%x, 0x%08x" % (DATA2, PAT_HI), "put w 0x%x, 0x%08x" % (DATA2 + 4, PAT_LO)]


def load_rows(tag, xo, bit31, want, cpu=None, control=False):
    regs, m, T, how = session(tag, [(X31(xo, 3, 0, 4, bit31), [])], SEEDS, cpu=cpu)
    row(tag + " session", how, "exit0", "the session's exit status was 0 (`exit0` proves the status, not that `quit` ran)", control=control)
    row(tag + " value", hexr(regs, 3), hex(want), "r3 = the %d-byte pattern" % (8 if xo == XO_LDARX else 4), control=control)
    row(tag + " cr", hexr(regs, "cr"), hex(CR_SEED), "a load-reserve writes no CR bit", control=control)
    row(tag + " pc", hexr(regs, "pc"), hex(CODE + 4), "one instruction retired", control=control)
    row(tag + " seed", hexr(regs, 30), hex(SENT & (0xFFFFFFFF if cpu else 0xFFFFFFFFFFFFFFFF)),
        "r30 seeded, never written (32-bit GPRs on the -C leg)", control=control)


def store_rows(tag, xo_ld, xo_st, bit31, cpu=None, control=False):
    """load-reserve (valid form) at CODE, then the store-conditional under test at CODE+4 with r3 reloaded."""
    val = STD_VAL if xo_st == XO_STDCX else STW_VAL
    n = 8 if xo_st == XO_STDCX else 4
    steps = [(X31(xo_ld, 3, 0, 4, 0), []),
             (X31(xo_st, 3, 0, 4, bit31), ["r3=0x%x" % val, "cr=0x%x" % CR_SEED])]
    regs, m, T, how = session(tag, steps, SEEDS, cpu=cpu)
    row(tag + " session", how, "exit0", "the session's exit status was 0 (`exit0` proves the status, not that `quit` ran)", control=control)
    row(tag + " bytes", mem(m, DATA, n), "%0*x" % (2 * n, val), "the %d bytes stored" % n, control=control)
    if n == 4:
        row(tag + " tail", mem(m, DATA + 4, 4), "%08x" % PAT_LO, "the next word untouched", control=control)
    row(tag + " cr", hexr(regs, "cr"), hex(0x2FFFFFFF), "CR0 = 0b001 (EQ), SO clear, fields 1-7 kept", control=control)
    row(tag + " pc", hexr(regs, "pc"), hex(CODE + 8), "two instructions retired", control=control)


print("ppcllscrcexit RUNG-3 WITNESS/DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; PPC970 64-bit, and -C PPC603 32-bit for the word forms)")
print("wants from PowerPC Book I v2.01 :432-433, :1109-1128 and Book II v2.01 :1264, :1305-1307, :1323, :1337")
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

# ============================================================ CONTROL SESSION ==
regs, m, T, how = session("ctl", [(LI(9, 0x1234), [])], SEEDS)
row("ctl session", how, "exit0", "the control session's exit status was 0 (`exit0` proves the status, not that `quit` ran)", control=True)
row("ctl live", hexr(regs, 9), hex(0x1234), "li r9 -- the guest executes", control=True)
row("ctl seed holds", hexr(regs, 30), hex(SENT), "r30 seeded, never written", control=True)
row("ctl data", mem(m, DATA, 8), PAT8, "the data pattern is in place", control=True)
nregs, _, _, nhow = session("neg", [(LI(9, 0x1234), [])], SEEDS, machine="nosuchmachine", timeout=60)
row("neg apparatus", "%s/%s" % (nhow, hexr(nregs, 9)), "exit1/none", "a bogus machine runs no guest", control=True)

# ============================================= THE FOUR VALID FORMS (controls) ==
load_rows("lw ok", XO_LWARX, 0, PAT_HI, control=True)
load_rows("ld ok", XO_LDARX, 0, (PAT_HI << 32) | PAT_LO, control=True)
store_rows("stw ok", XO_LWARX, XO_STWCX, 1, control=True)
store_rows("std ok", XO_LDARX, XO_STDCX, 1, control=True)

# ============================================ RESERVATION AND XER[SO] (controls) ==
regs, m, T, how = session("stw noresv", [(X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL])], SEEDS)
row("noresv session", how, "exit0", "", control=True)
row("noresv bytes", mem(m, DATA, 8), PAT8, "no reservation: nothing stored", control=True)
row("noresv cr", hexr(regs, "cr"), hex(0x0FFFFFFF), "CR0 = 0b000, SO clear", control=True)
steps = [(X31(XO_LWARX, 3, 0, 4, 0), []), (X31(XO_STWCX, 3, 0, 5, 1), ["r3=0x%x" % STW_VAL, "cr=0x%x" % CR_SEED])]
regs, m, T, how = session("stw mismatch", steps, SEEDS)
row("mismatch bytes", mem(m, DATA2, 8), PAT8, "reserved DATA, stored to DATA2: refused", control=True)
row("mismatch cr", hexr(regs, "cr"), hex(0x0FFFFFFF), "CR0 = 0b000", control=True)
steps = [(X31(XO_LWARX, 3, 0, 4, 0), []), (X31(XO_STWCX, 3, 0, 5, 1), ["r3=0x%x" % STW_VAL]),
         (X31(XO_STWCX, 3, 0, 4, 1), ["cr=0x%x" % CR_SEED])]
regs, m, T, how = session("stw chain", steps, SEEDS)
row("chain bytes", mem(m, DATA, 8), PAT8, "a failed stwcx. clears the reservation", control=True)
row("chain cr", hexr(regs, "cr"), hex(0x0FFFFFFF), "the third word fails too", control=True)
steps = [(X31(XO_LWARX, 3, 0, 4, 0), []), (X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL, "cr=0x%x" % CR_SEED, "xer=0x%x" % XER_SO])]
regs, m, T, how = session("stw so", steps, SEEDS)
row("so bytes", mem(m, DATA, 4), "%08x" % STW_VAL, "stored", control=True)
row("so cr", hexr(regs, "cr"), hex(0x3FFFFFFF), "CR0 = 0b001 || XER[SO]=1", control=True)
#  (pass 2, GLM) a successful store-conditional consumes the reservation: a second stwcx. with no new lwarx must be refused
steps = [(X31(XO_LWARX, 3, 0, 4, 0), []), (X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL]),
         (X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL2, "cr=0x%x" % CR_SEED])]
regs, m, T, how = session("stw twice", steps, SEEDS)
row("twice bytes", mem(m, DATA, 4), "%08x" % STW_VAL, "the second stwcx. stored nothing", control=True)
row("twice cr", hexr(regs, "cr"), hex(0x0FFFFFFF), "CR0 = 0b000: the reservation was consumed", control=True)
#  (pass 2, GLM) every other row has RA = 0 and low register numbers: one row with a base register and fields above 15
regs, m, T, how = session("lw ra", [(X31(XO_LWARX, 17, 6, 20, 0), [])], SEEDS + ["r6=0x%x" % (DATA - 0x40), "r20=0x40", "r17=0x%x" % SEED_R3])
row("ra value", hexr(regs, 17), hex(PAT_HI), "lwarx r17,r6,r20: EA = r6 + r20", control=True)
row("ra r3 kept", hexr(regs, 3), hex(SEED_R3), "r3 untouched (rt decoded as 17, not 1 or 3)", control=True)
#  (F2 table 3) the reservation-FAILURE path's XER[SO] copy: a stwcx. with no reservation and SO set -> CR0 = 0b000 || SO
regs, m, T, how = session("stw nso", [(X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL, "xer=0x%x" % XER_SO])], SEEDS)
row("nso bytes", mem(m, DATA, 8), PAT8, "no reservation: nothing stored", control=True)
row("nso cr", hexr(regs, "cr"), hex(0x1FFFFFFF), "CR0 = 0b000 || XER[SO]=1", control=True)

# ======================================= THE FOUR BIT-31 FORMS (the fixed rows) ==
load_rows("lw rc1", XO_LWARX, 1, PAT_HI)
load_rows("ld rc1", XO_LDARX, 1, (PAT_HI << 32) | PAT_LO)
store_rows("stw rc0", XO_LWARX, XO_STWCX, 0)
store_rows("std rc0", XO_LDARX, XO_STDCX, 0)
#  (F2 table 3) the reservation a BIT-31-SET lwarx creates must be the one a store-conditional consumes
steps = [(X31(XO_LWARX, 3, 0, 4, 1), []), (X31(XO_STWCX, 3, 0, 4, 1), ["r3=0x%x" % STW_VAL, "cr=0x%x" % CR_SEED])]
regs, m, T, how = session("rc1 resv", steps, SEEDS)
row("rc1 resv bytes", mem(m, DATA, 4), "%08x" % STW_VAL, "lwarx (bit 31 set) reserved; stwcx. stored")
row("rc1 resv cr", hexr(regs, "cr"), hex(0x2FFFFFFF), "CR0 = 0b001: the reservation held")
#  (F2) a bit-clear store-conditional with NO reservation is refused like the valid form
regs, m, T, how = session("rc0 noresv", [(X31(XO_STWCX, 3, 0, 4, 0), ["r3=0x%x" % STW_VAL])], SEEDS)
row("rc0 nr bytes", mem(m, DATA, 8), PAT8, "bit-clear stwcx., no reservation: nothing stored")
row("rc0 nr cr", hexr(regs, "cr"), hex(0x0FFFFFFF), "CR0 = 0b000")

# ================================================== THE 32-BIT LEG (word forms) ==
load_rows("lw32 ok", XO_LWARX, 0, PAT_HI, cpu="PPC603", control=True)
store_rows("sw32 ok", XO_LWARX, XO_STWCX, 1, cpu="PPC603", control=True)
load_rows("lw32 rc1", XO_LWARX, 1, PAT_HI, cpu="PPC603")
store_rows("sw32 rc0", XO_LWARX, XO_STWCX, 0, cpu="PPC603")

# ===================================================================== RESULT ==
row("unasm census", "%d/%d" % (census_ok, census_all), "%d/%d" % (census_all, census_all),
    "every placed word read back by `unassemble'", control=True)
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_LLSC_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_LLSC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PPC_LLSC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PPC_LLSC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PPC_LLSC_PROBE_DONE")
