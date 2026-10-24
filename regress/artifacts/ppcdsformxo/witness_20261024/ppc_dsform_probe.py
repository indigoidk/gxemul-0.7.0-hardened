#!/usr/bin/env python3
"""ppcdsformxo -- RUNG-3 WITNESS for the 64-bit DS-form LOADS ld, ldu, lwa (primary opcode 58).

usage: ppc_dsform_probe.py <gxemul> [label] [workdir]
       workdir (default /tmp) receives the 4-byte dummy boot file and the two session
       transcripts, RAW_<label>_main.txt and RAW_<label>_neg.txt.

ARCHITECTURE, read locally -- PowerPC Book I v2.01, _scratchpad/ppc_uisa_book1_v201.txt:
  :777-787    Figure 7, the DS instruction format:
              OPCD 0:5 | RT 6:10 | RA 11:15 | DS 16:29 | XO 30:31   (IBM big-endian bit numbers)
  :1047       XO, the extended-opcode field; 30:31 is among its listed positions
  :951-955    DS (16:29) is "a 14-bit signed two's complement integer which is concatenated on
              the right with 0b00 and sign-extended to 64 bits"
  :1221-1227  "With DS-form instructions, the 14-bit DS field is concatenated on the right with
              0b00 and sign-extended to form a 64-bit address component", added to (RA|0)
  :2350-2367  ld   RT,DS(RA)  XO 0   EA <- b + EXTS(DS || 0b00)     RT <- MEM(EA, 8)
  :2372-2395  ldu  RT,DS(RA)  XO 1   EA <- (RA) + EXTS(DS || 0b00)  RT <- MEM(EA, 8)   RA <- EA
                                     "If RA = 0 or RA=RT, the instruction form is invalid."
  :2297-2317  lwa  RT,DS(RA)  XO 2   EA <- b + EXTS(DS || 0b00)     RT <- EXTS(MEM(EA, 4))
  :2244       lwz  RT,D(RA)   primary opcode 32, the D-form control (RTL :2254-2259):
                                     EA <- b + EXTS(D)               RT <- 32 zero bits || MEM(EA, 4)
So the two low bits of an opcode-58 word select the form and are never part of the displacement.
The five VALUE wants (ld, ldu, lwa, lwz, and ldu's RA) are computed from these lines and the data
pattern, never from the tree.  `live' wants the guest's own immediate; the census wants the tree's
disassembler text (its convention, not architecture); `neg apparatus' wants the tree's exit status.

THE COMMITTED DECODE, as read from source (the run measures it): src/cpus/cpu_ppc_instr.c's
D/DS-form load/store arm lists `case PPC_HI6_LD:' among its D-form cases, takes
`imm = (int16_t)iword;' -- the whole low halfword, XO bits included -- and decodes
`case PPC_HI6_LD:   load=1; size=3; break;' without looking at XO.  Read that way, every
opcode-58 word is a doubleword load from RA + (DS || XO): ldu reads at EA + 1 and leaves RA
alone, and lwa reads a DOUBLEWORD at EA + 2.  The disassembler (src/cpus/cpu_ppc.c,
`case PPC_HI6_LD:  load=1; wlen = 8; mnem = "ld"; break;' under its
`imm = (int16_t)(iword & 0xffff);') folds XO into the displacement the same way.

RUNG 3.  Instruction words built by encode() from their fields are placed by the debugger's
`put w', fetched, decoded by the real decoder and executed by the real handler on the UNMODIFIED
in-tree `-E bareppc' (MACHINE_DEFAULT_CPU PPC970, a 64-bit CPU; MSR 0 at reset, so every address
here is physical -- the msr readback is printed).  No machine description edited, no device_add,
no CPU override.  One session, stepped exactly once per placed word, then `reg':

    lis + ori, four times   r20, r21, r22, r23 <- DATA + 0x80   (the guest sets every base)
    ld   r4,-0x70(r20)      XO 0     EA = DATA + 0x10
    ldu  r5,-0x60(r21)      XO 1     EA = DATA + 0x20, and r21 <- EA
    lwa  r6,+0x08(r22)      XO 2     EA = DATA + 0x88
    lwz  r7,+0x08(r23)      D-form   EA = DATA + 0x88, the word lwa reads
    li   r9,0x1234          liveness, LAST: a green `live' means every placed word ran

DATA (0x20000) is filled by the debugger's `put b' with a COUNTING BYTE PATTERN -- byte DATA + k
is k, for k below 0x100 -- so a doubleword loaded from DATA + k reads 0x(k)(k+1)..(k+7) and
NAMES k; names() inverts a loaded value back to the offset it came from.  ld and ldu carry
NEGATIVE displacements, so the DS sign extension is exercised; ld is the XO-0 control for the same
decode, so a red ldu beside a green ld points at the XO bits rather than at the sign extension.
The word at DATA + 0x88 has its sign bit set, so lwa's sign extension and lwz's zero extension of
that one word differ only in the high half.  Every destination and base is seeded with a sentinel
first, so a register no instruction wrote reads back as the sentinel, not as zero.

ROWS -- 8, the row denominator:
    ld value       XO 0 control: MEM(EA, 8), EA = DATA + 0x10
    ldu value      MEM(EA, 8), EA = DATA + 0x20
    ldu RA after   r21 = EA = DATA + 0x20
    lwa value      EXTS(MEM(EA, 4)), EA = DATA + 0x88
    lwz value      D-form control: MEM(EA, 4) zero-extended, EA = DATA + 0x88
    live           li r9,0x1234 round-trips through the guest and the `reg' readback
    unasm census   every placed word's `unassemble' line (address, word, mnemonic, RT, RA, raw low
                   halfword) equals the text derived from the encoder's fields, and the line count
                   is part of the equality.  For opcode 58 the expected text is the disassembler's
                   OWN convention, `ld' with displacement (DS || XO): an OBSERVATION about the
                   tree's disassembler that confirms opcode, RT, RA and the raw low halfword of
                   each placed word -- not a check of architecture
    neg apparatus  the same command stream against a bogus machine TYPE exits 1 with no register
                   dump, so every register oracle above can go red (a bogus SUBTYPE is not
                   rejected, which is why the TYPE is the one made bogus)

SUMMARY LINES: PPC_DSFORM_RESULT=<ok>/8; PPC_DSFORM_CONTROL=OK|FAIL over ld value, lwz value,
live, unasm census and neg apparatus; PPC_DSFORM_SYMPTOM over ldu value, ldu RA after and lwa
value -- PRESENT n/m when every one of them is red, ABSENT when none is, MIXED otherwise, and
attributable to the decode only when CONTROL=OK; PPC_DSFORM_RED=<names>; then the sentinel
PPC_DSFORM_PROBE_DONE.  Exit status 1 on any red row, so a run on a build that carries the
defect exits 1 by design.

CONTRACT (clause (e)).
  OBSERVED: for the DS-form loads ld, ldu and lwa and the D-form lwz control, the effective
    address each one reads (named by the loaded value), the width and extension of what it
    loads, and ldu's write of EA into RA.  The other three bases are read back and printed as
    observations (architecturally unchanged); they are not rows.
  NOT CLAIMED:
    * the store forms std and stdu (primary opcode 62) -- a later step; this probe places no
      store instruction in the guest;
    * the illegal XO values (opcode 58 with XO 3; opcode 62 with XO 2 or 3);
    * the invalid update forms, ldu with RA = 0 or RA = RT;
    * 32-bit CPUs;
    * translation on (MSR IR or DR set) -- every access here is physical;
    * 64-bit mode (MSR SF set), an EA with a non-zero high half, displacements and bases other
      than the ones above, an EA that crosses a page, and the indexed forms ldx, ldux, lwax and
      lwaux.

Sentinel: PPC_DSFORM_PROBE_DONE
"""

import hashlib
import os
import re
import subprocess
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_dsform_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else "/tmp"
DUMMY = os.path.join(WORK, "ppc_dsform_dummy.bin")
with open(DUMMY, "wb") as _fh:
    _fh.write(b"\x00\x00\x00\x00")

CODE = 0x10000             # the guest program
DATA = 0x20000             # the counting byte pattern
PATLEN = 0x100             # byte DATA + k is k, for k in [0, PATLEN)
BASE = DATA + 0x80         # every base register's value, computed by the guest
M64 = (1 << 64) - 1
SENT = 0x5A5A5A5A5A5A5A5A  # seeded into every destination and base before the program runs
LIVE = 0x1234
LIVEREG = 9
SPARE = 30                 # seeded, never written: shows the seeding itself took

OP_ADDI = 14               # li  RT,SI  is  addi RT,0,SI
OP_ADDIS = 15              # lis RT,SI  is  addis RT,0,SI
OP_ORI = 24                # ori RA,RS,UI   (RS sits in bits 6:10, RA in 11:15)
OP_LWZ = 32                # lwz RT,D(RA)   :2244
OP_DSLOAD = 58             # ld / ldu / lwa :2350, :2372, :2297
XO_LD = 0
XO_LDU = 1
XO_LWA = 2

rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-20s %-20s %-52s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


def obs(text):
    print("OBS " + text)


# ----------------------------------------------------------------- architecture
def sext(v, bits):
    """The two's-complement value of the low `bits' bits of v."""
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def exts64(v, bits):
    """EXTS to 64 bits, as the unsigned image a 64-bit register holds."""
    return sext(v, bits) & M64


def pat(k):
    """The counting byte pattern: byte DATA + k is k."""
    assert 0 <= k < PATLEN
    return k


def mem(k, n):
    """MEM(DATA + k, n) over the pattern, big-endian (the machine's byte order)."""
    v = 0
    for i in range(n):
        v = (v << 8) | pat(k + i)
    return v


def ea_ds(ra_val, ds):
    """EA = (RA) + EXTS(DS || 0b00) -- :2362, :2385, :2309."""
    return (ra_val + exts64((ds & 0x3FFF) << 2, 16)) & M64


def ea_d(ra_val, d):
    """EA = (RA) + EXTS(D) -- lwz, :2258."""
    return (ra_val + exts64(d, 16)) & M64


# -------------------------------------------------------------------- encoding
def encode(opcd, rt, ra, ds, xo):
    """THE encoder: every placed word comes from here.  Figure 7 (:777-787):
         OPCD 0:5 | RT 6:10 | RA 11:15 | DS 16:29 | XO 30:31   (big-endian bit numbers)
       DS is the 14-bit field (a signed count of words) and XO the 2-bit field.  A D-form
       word has the same layout, its D field (16:31) occupying DS and XO side by side --
       d_fields() splits a D value into those two positions."""
    assert 0 <= opcd < 64 and 0 <= rt < 32 and 0 <= ra < 32
    assert -0x2000 <= ds < 0x2000 and 0 <= xo < 4
    return ((opcd << 26) | (rt << 21) | (ra << 16) | ((ds & 0x3FFF) << 2)
            | xo) & 0xFFFFFFFF


def d_fields(d):
    """A D-form field D (16:31) as the (DS, XO) pair encode() takes."""
    assert -0x8000 <= d <= 0xFFFF
    return sext(d >> 2, 14), d & 3


def low_half(ds, xo):
    """The raw low halfword (bits 16:31) of a word built by encode()."""
    return ((ds & 0x3FFF) << 2) | xo

# ----------------------------------------------------------------- the program
PROG = []    # (label, opcd, rt, ra, ds, xo): the encoder's fields, kept for the census


def place(label, opcd, rt, ra, ds, xo):
    PROG.append((label, opcd, rt, ra, ds, xo))


BASEREG = {"ld": 20, "ldu": 21, "lwa": 22, "lwz": 23}
DEST = {"ld": 4, "ldu": 5, "lwa": 6, "lwz": 7}
DISP = {"ld": -0x70, "ldu": -0x60, "lwa": 0x08, "lwz": 0x08}   # byte displacements

for _nm in ("ld", "ldu", "lwa", "lwz"):
    _b = BASEREG[_nm]
    place("lis", OP_ADDIS, _b, 0, *d_fields(BASE >> 16))       # lis b,BASE@h
    place("ori", OP_ORI, _b, _b, *d_fields(BASE & 0xFFFF))      # ori b,b,BASE@l
for _nm, _xo in (("ld", XO_LD), ("ldu", XO_LDU), ("lwa", XO_LWA)):
    assert DISP[_nm] % 4 == 0 and DEST[_nm] != BASEREG[_nm] and BASEREG[_nm] != 0
    place(_nm, OP_DSLOAD, DEST[_nm], BASEREG[_nm], DISP[_nm] >> 2, _xo)
place("lwz", OP_LWZ, DEST["lwz"], BASEREG["lwz"], *d_fields(DISP["lwz"]))
place("li", OP_ADDI, LIVEREG, 0, *d_fields(LIVE))

WORDS = [encode(o, t, a, s, x) for _, o, t, a, s, x in PROG]
N = len(WORDS)


def fields(label):
    hits = [f for f in PROG if f[0] == label]
    assert len(hits) == 1, label
    return hits[0]


# ------------------------------------------- wants, from the ENCODED fields and the RTL
EA = {}
for _nm in ("ld", "ldu", "lwa"):
    EA[_nm] = ea_ds(BASE, fields(_nm)[4])
EA["lwz"] = ea_d(BASE, low_half(fields("lwz")[4], fields("lwz")[5]))
OFF = dict((_nm, EA[_nm] - DATA) for _nm in EA)
for _nm in OFF:
    assert 0 <= OFF[_nm] and OFF[_nm] + 8 <= PATLEN, (_nm, OFF[_nm])

WANT = {
    "ld": mem(OFF["ld"], 8),                   # RT <- MEM(EA, 8)                :2363
    "ldu": mem(OFF["ldu"], 8),                 # RT <- MEM(EA, 8)                :2386
    "lwa": exts64(mem(OFF["lwa"], 4), 32),     # RT <- EXTS(MEM(EA, 4))          :2310
    "lwz": mem(OFF["lwz"], 4),                 # RT <- 32 zero bits || MEM(EA, 4) :2259
}
WANT_LDU_RA = EA["ldu"]                        # RA <- EA                        :2387

#  NOT a want: what the committed decode computes as read from source -- RA plus the RAW
#  low halfword, XO folded in.  Printed as an observation beside each load, never graded.
FOLD = {}
for _nm in ("ld", "ldu", "lwa", "lwz"):
    _f = fields(_nm)
    FOLD[_nm] = (BASE + exts64(low_half(_f[4], _f[5]), 16)) & M64


def names(v):
    """Every pattern location a loaded value can only have come from: (kind, offset)."""
    out = []
    if v is None or v < 0:
        return out
    for k in range(PATLEN - 7):
        if v == mem(k, 8):
            out.append(("doubleword", k))
    for k in range(PATLEN - 3):
        w = mem(k, 4)
        if w & 0x80000000:
            if v == w:
                out.append(("zero-extended word", k))
            if v == exts64(w, 32):
                out.append(("sign-extended word", k))
        elif v == w:
            out.append(("word (sign bit clear)", k))
    return out


def names_text(v):
    if v is None or v < 0:
        return "no readback"
    if v == SENT:
        return "unwritten (still the seeded sentinel)"
    hits = names(v)
    if not hits:
        return "not a value of the pattern"
    return "; ".join("%s at DATA+0x%02x" % (kind, k) for kind, k in hits)


# --------------------------------------------------------------------- sessions
def commands():
    seeded = sorted(set(DEST.values()) | set(BASEREG.values()) | {LIVEREG, SPARE})
    cmds = ["r%d=0x%x" % (r, SENT) for r in seeded]
    for k in range(PATLEN):
        cmds.append("put b 0x%x, 0x%02x" % (DATA + k, pat(k)))
    cmds.append("dump 0x%x 0x%x" % (DATA, DATA + PATLEN))
    for i, w in enumerate(WORDS):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds.append("unassemble 0x%x 0x%x" % (CODE, CODE + 4 * N))
    cmds.append("pc=0x%x" % CODE)
    cmds.append("step %d" % N)
    cmds.append("reg")
    return cmds


def session(cmds, machine="bareppc", timeout=120):
    """The piped cold-debugger session -- regress/ppc_rldicl_probe.py's idiom.
       Returns (regs, pc, msr, unassemble lines, transcript, how, argv, CRs removed)."""
    argv = [BIN, "-V", "-x", "-E", machine, "-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        raw = p.stdout.decode("latin-1", "replace")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        raw = (e.output or b"").decode("latin-1", "replace")
        how = "TIMEOUT"
    ncr = raw.count("\r")
    t = raw.replace("\r", "")
    regs, pc, msr = {}, None, None
    idx = t.rfind("GXemul> reg")
    if idx >= 0:
        seg = t[idx:]
        for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", seg):
            regs[int(m.group(1))] = int(m.group(2), 16)
        m = re.search(r"\bpc  = (0x[0-9a-fA-F]+)", seg)
        pc = int(m.group(1), 16) if m else None
        m = re.search(r"\bmsr = (0x[0-9a-fA-F]+)", seg)
        msr = int(m.group(1), 16) if m else None
    dis = []
    di = t.find("GXemul> unassemble")
    if di >= 0:
        de = t.find("GXemul> pc=", di)
        seg = t[di:de if de > 0 else len(t)]
        for m in re.finditer(r"^([0-9a-f]{16}): ([0-9a-f]{8})\s*(?:<- )?(\S+)"
                             r"(?:\t(\S+))?", seg, re.M):
            dis.append((int(m.group(1), 16), int(m.group(2), 16), m.group(3),
                        m.group(4) or ""))
    return regs, pc, msr, dis, t, how, argv, ncr


def save_transcript(name, t, how, argv, ncr):
    with open(os.path.join(WORK, name), "w", encoding="latin-1", newline="\n") as fh:
        fh.write("ARGV: %s\nHOW: %s\nCR_REMOVED: %d (otherwise verbatim)\n\n"
                 % (" ".join(argv), how, ncr))
        fh.write(t)


def expect_unasm(opcd, rt, ra, ds, xo):
    """The disassembler's own text for the five opcodes placed (src/cpus/cpu_ppc.c), derived
       from the encoder's fields: the tree's convention, not architecture.  For opcode 58 it
       prints `ld' whatever XO is, with the RAW low halfword as the signed displacement --
       (DS || XO), the fold -- so the line still confirms opcode, RT, RA and that halfword."""
    lh = low_half(ds, xo)
    if opcd == OP_DSLOAD:
        return "ld", "r%d,%d(r%d)" % (rt, sext(lh, 16), ra)
    if opcd == OP_LWZ:
        return "lwz", "r%d,%d(r%d)" % (rt, sext(lh, 16), ra)
    if opcd == OP_ADDIS and ra == 0:
        return "lis", "r%d,%d" % (rt, sext(lh, 16))
    if opcd == OP_ADDI and ra == 0:
        return "li", "r%d,%d" % (rt, sext(lh, 16))
    if opcd == OP_ORI:
        return "ori", "r%d,r%d,0x%04x" % (ra, rt, lh)    # it prints RA, then RS (6:10)
    raise AssertionError("no expected text for opcode %d" % opcd)

# ========================================================================= RUN ==
print("ppcdsformxo RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
try:
    with open(BIN, "rb") as _fh:
        print("binary md5=%s" % hashlib.md5(_fh.read()).hexdigest())
except OSError as _e:
    print("binary md5=UNREADABLE (%s)" % _e)
print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970, 64-bit)")
print("value wants: _scratchpad/ppc_uisa_book1_v201.txt :2350-2367 (ld) :2372-2395 (ldu)"
      " :2297-2317 (lwa) :2244 (lwz); DS || 0b00 sign-extended :951-955 :1221-1227")
print("CODE=0x%x DATA=0x%x (byte DATA+k = k, k < 0x%x) BASE=0x%x placed words=%d"
      % (CODE, DATA, PATLEN, BASE, N))
print("%-16s %-20s %-20s %-52s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

CMDS = commands()
regs, pc, msr, dis, T, how, argv, ncr = session(CMDS)
save_transcript("RAW_%s_main.txt" % LABEL, T, how, argv, ncr)


def g(r):
    return regs.get(r, -1)


# ------------------------------------------------------------ the load rows ----
row("ld value", hex(g(DEST["ld"])), hex(WANT["ld"]),
    "XO 0 control: MEM(EA,8), EA = DATA+0x%02x" % OFF["ld"])
row("ldu value", hex(g(DEST["ldu"])), hex(WANT["ldu"]),
    "XO 1: MEM(EA,8), EA = DATA+0x%02x" % OFF["ldu"])
row("ldu RA after", hex(g(BASEREG["ldu"])), hex(WANT_LDU_RA),
    "XO 1: RA <- EA (r%d)" % BASEREG["ldu"])
row("lwa value", hex(g(DEST["lwa"])), hex(WANT["lwa"]),
    "XO 2: EXTS(MEM(EA,4)), EA = DATA+0x%02x" % OFF["lwa"])
row("lwz value", hex(g(DEST["lwz"])), hex(WANT["lwz"]),
    "D-form control: zero-extended MEM(EA,4), EA = DATA+0x%02x" % OFF["lwz"])
row("live", hex(g(LIVEREG)), hex(LIVE),
    "li r%d,0x%x is the LAST word: the guest ran every word" % (LIVEREG, LIVE))

# ------------------------------------------------------- the unassemble census --
matched = 0
for i, (lab, o, t, a, s, x) in enumerate(PROG):
    em, eo = expect_unasm(o, t, a, s, x)
    if i < len(dis):
        d_addr, d_word, d_mn, d_ops = dis[i]
        same = (d_addr == CODE + 4 * i and d_word == WORDS[i]
                and d_mn == em and d_ops == eo)
        got_txt = "%x: %08x %s %s" % (d_addr, d_word, d_mn, d_ops)
    else:
        same = False
        got_txt = "(no line)"
    matched += 1 if same else 0
    extra = ""
    if o == OP_DSLOAD:
        extra = ("  [placed as %s: opcode %d RT %d RA %d DS %d XO %d; raw low half 0x%04x]"
                 % (lab, o, t, a, s, x, low_half(s, x)))
    obs("unasm %-3s %s | want %s %s | %s%s"
        % (lab, got_txt, em, eo, "same" if same else "DIFFERS", extra))
row("unasm census", "%d/%d" % (matched, len(dis)), "%d/%d" % (N, N),
    "every placed word's unassemble line, pinned by equality")

# ------------------------------------------- per-instruction observations (no rows) --
for _nm in ("ld", "ldu", "lwa", "lwz"):
    v = regs.get(DEST[_nm])
    obs("%-3s r%d = %s  names: %s  | arch EA = DATA+0x%02x | RA + raw low half = DATA+0x%02x"
        % (_nm, DEST[_nm], hex(v) if v is not None else "none", names_text(v),
           OFF[_nm], FOLD[_nm] - DATA))
for _nm in ("ld", "ldu", "lwa", "lwz"):
    v = regs.get(BASEREG[_nm])
    obs("%-3s base r%d after = %s  (architectural: %s, %s)"
        % (_nm, BASEREG[_nm], hex(v) if v is not None else "none",
           hex(WANT_LDU_RA if _nm == "ldu" else BASE),
           "RA <- EA" if _nm == "ldu" else "unchanged"))
obs("r%d (seeded with the sentinel, never written) = %s" % (SPARE, hex(g(SPARE))))
obs("pc after `step %d' = %s  (CODE + 4 x %d = %s)"
    % (N, hex(pc) if pc is not None else "none", N, hex(CODE + 4 * N)))
obs("msr = %s" % (hex(msr) if msr is not None else "none"))
obs("main session how=%s, %d commands, transcript RAW_%s_main.txt" % (how, len(CMDS) + 1, LABEL))

# ================================================== NEGATIVE APPARATUS CONTROL ==
# The SAME command stream against a bogus machine TYPE: no guest is built, so no register
# dump exists and every register oracle above would read -0x1.  Without this, `live' and
# the value rows would be checks that cannot be shown to fail.
nregs, _npc, _nmsr, _ndis, nT, nhow, nargv, nncr = session(CMDS, machine="nosuchmachine",
                                                           timeout=60)
save_transcript("RAW_%s_neg.txt" % LABEL, nT, nhow, nargv, nncr)
row("neg apparatus", "%s/%s" % (nhow, hex(nregs.get(LIVEREG, -1))), "exit1/-0x1",
    "same commands, bogus machine TYPE: exit 1, no register dump")

# ================================================================ SUMMARY + DONE
CONTROL = ("ld value", "lwz value", "live", "unasm census", "neg apparatus")
SYMPTOM = ("ldu value", "ldu RA after", "lwa value")
okmap = dict(rows)
assert len(rows) == 8 and set(CONTROL) | set(SYMPTOM) == set(okmap) \
    and not set(CONTROL) & set(SYMPTOM), "row set drifted from the docstring"
npass = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
nsym = sum(1 for n in SYMPTOM if not okmap[n])
if nsym == len(SYMPTOM):
    sym = "PRESENT %d/%d" % (nsym, len(SYMPTOM))
elif nsym == 0:
    sym = "ABSENT"
else:
    sym = "MIXED"
print("")
print("elapsed=%.1fs binary=%s label=%s" % (time.time() - t0, BIN, LABEL))
print("PPC_DSFORM_RESULT=%d/%d" % (npass, len(rows)))
print("PPC_DSFORM_CONTROL=%s" % ("OK" if all(okmap[n] for n in CONTROL) else "FAIL"))
print("PPC_DSFORM_SYMPTOM=%s" % sym)
print("PPC_DSFORM_RED=%s" % (",".join(red) if red else "none"))
print("PPC_DSFORM_PROBE_DONE")
sys.stdout.flush()
sys.exit(1 if red else 0)
