#!/usr/bin/env python3
"""#447 DETECTOR: the four value guards in DEVICE_ACCESS(sh4) DIAGNOSE AND SURVIVE
instead of calling exit(1) -- and do not silently absorb the rejected value.

Rung 3.  Real SH-4 guest instructions through real address decode, real
`memory_rw` and real device dispatch, on an UNMODIFIED in-tree `-E landisk`.
No source is edited, no `device_add` of our own, no boot.

WHY THIS IS A SIBLING OF sh4_pcic_probe.py AND NOT MORE ROWS INSIDE IT.  That
file is #443's detector for `dev_sh4_pcic_access()`; this one is #447's for
`DEVICE_ACCESS(sh4)`.  Different function, different registers, different
address space, different latch array, different diagnostics.  gate_sh_rounding
grades sh4_pcic_probe's verdict under the name "sh4_pcic: no offset kills the
host", and folding #447 rows under that token would make the gate's own check
name untrue -- the wrong-record class this project treats as a defect.

IT IMPORTS ITS SESSION MACHINERY FROM sh4_pcic_probe RATHER THAN COPYING IT,
and that is deliberate in two directions.  It is the first probe in this tree to
import another, so it is worth stating why: gate_hygiene.sh counts the three
#392 readiness idioms across every regress/*.py and pins the total
(EXPECT_CONVERTED), so a COPY would silently need that pin bumped by three, and
a copy is also a second place for the predicate to rot.  Importing keeps all
three counts unchanged and keeps one correct predicate in the tree.  MEASURED:
with this file present the three counts are still 23/23/23 and bare/unknown/
whole_full are still 0/0/2.

WHAT THE FOUR SITES ARE, and they are NOT interchangeable:

  TCR0/1/2   0xffd80010/1c/28   idata & TCR_UNIMPLEMENTED (six bits)
  DMATCR0..7 0xffa00008 + ...   idata & ~0x00ffffff
  ICR        0xffd00000         idata & 0x80        (IRLM)
  RCR1       0xffc80038         idata & 0x18        (CIE|AIE -- TWO features)

*** THE ROW THAT MATTERS MOST IS V17, NOT THE SURVIVAL ROWS. ***  Deleting `exit(1)` and
nothing else does not fix RCR1 -- it makes it worse.  `d->rtc_rcr1 = idata;` ran
BEFORE the guard, so the rejected value had already landed and `exit(1)` was the
only thing stopping the guest reading it back.  V17 writes an accepted value,
then a rejected one, then READS THE REGISTER BACK through the guest.  The naive
fix turns a host kill into silent state corruption and V17 is the row that sees
it.  The other three sites do NOT have that shape -- checked per site, not
assumed from #443 -- and saying otherwise in a comment would have been wrong
three times out of four.

*** V19 IS THE VACUITY TRAP THIS FILE WAS BUILT AROUND. ***  A row that reads
state back through the same path that wrote it proves nothing if the read path
launders the value.  DMATCR's read arm masks with 0x00ffffff, so the rejected
top bits are invisible whether they were stored or not; the consumer that would
see them, sh4_dmac_transfer(), masks with 0x1fffffff -- FIVE BITS WIDER.  So V19
does not look for the top bits at all.  It writes an accepted 0x00000010, then a
rejected 0x01abcdef, and demands the LOW 24 bits still read 0x000010.

*** THE WIDTH AXIS IS PINNED, BECAUSE #443's CENSUS WAS ONE-DIMENSIONAL. ***
That file issued only len=4 and a mutant reading `if (len == 2) exit(1);` passed
29 of its 29 rows.  Three of this cluster's four registers are NOT 32-bit --
ICR and TCR are 16-bit and RCR1 is 8-bit -- so len=4 is the UNNATURAL width at
three of the four sites.  V5-V8 issue every reachable width at every site, in
both the tripping and the non-tripping direction, and V9's census pin fails if
the table ever shrinks.  len=8 is not covered because it is not reachable: every
memory_rw() call in cpu_sh_instr.c passes sizeof(data) with `data` declared
uint8_t, uint16_t or uint32_t -- there are no uint64_t declarations in that file
-- and SZ=1 register-pair fmov is implemented as two 32-bit accesses at addr and
addr+4 (cpu_sh_instr.c:797-798, :1459-1470).

V24-V28 pin the WHOLE diagnostic line, not one token.  #444 pinned a single
ARGUMENT and left the format free, and four seats independently found mutants in
other fields of the same string.  V28 additionally pins the TCR mask itself by
writing all six bits at once: drop any one of them from TCR_UNIMPLEMENTED and
the printed value changes.

V13-V15 are about the LATCH KEY, which is (class, instance, offending bit):
  V11/V12  a key WITHOUT the instance reports timer 0 and silences timers 1
           and 2, and reports DMA channel 0 and silences the other seven --
           #443's measured half-fix, one level down.
  V13/V14  a key without the BIT reports the first feature a guest asks for and
           swallows every other one AT THE SAME REGISTER.  RCR1's one guard
           covers two independent features and TCR's covers six.
  V15      the key is the MASKED bits, not the written value.  Keying on the
           value would make 0x0004 and 0x0104 two complaints when they are one,
           and hand a looping guest an unbounded host-CPU burn -- the exact
           thing the latch exists to prevent.  fatal() has no quiet_mode
           early-out, so -q could not silence it.

V10 is the direction axis: all four guards sit on the WRITE path, so a read at
any of the four addresses must survive AND diagnose nothing.

Under a cold debugger `single_step` is true, so `debug()`'s quiet_mode early-out
never fires and a STEPPED row cannot distinguish `fatal()` from `debug()` by
presence.  Every latch row therefore counts the LATCHED SUFFIX, never a register
name.

*** BUT THAT LIMIT IS ESCAPABLE, AND V32 ESCAPES IT. ***  The standing rule in
this project is stated unconditionally -- "a probe cannot tell fatal() from
debug()" -- and it is only true WHILE SINGLE-STEPPING.  debugmsg.c:367-373
computes `ss = single_step || about_to_enter_single_step` and then
`if (emul_executing) v--; if (ss) v++;`, so stepping pushes debug() ABOVE the
threshold and free-running pushes it below.  Run the same store under
`continue` with a breakpoint after it and debug() goes silent while fatal()
does not -- with no -q needed.  MEASURED both ways on two builds; a mutant with
all four fatal() calls swapped for debug() scored 32/32 against this file
before V32 existed, and V32 is the only row that fails it.

NO SH-4 MANUAL IS CITED ANYWHERE IN THIS FILE.  There is none in this tree
(`_scratchpad/sh4_manual.txt` is one byte).  Every constant below is read out of
a header in this repository, with the file and line named, or measured.

usage:  sh4_val_probe.py <gxemul-binary> <landisk-kernel>

    *** KEEP THE "./" ON THE BINARY. ***  `os.execvp` on a bare name searches
    PATH; when it misses, EVERY arm silently reports alive=False and a probe
    written the naive way "passes" having measured nothing.  V0 catches that,
    and the existence check in main() catches it sooner.
"""
import argparse
import os
import re
import sys
import time

#  Python puts this script's own directory on sys.path[0], so the import below
#  finds the sibling however the gate spells its cwd.
import sh4_pcic_probe as P

# ----------------------------------------------------------------- constants
#  All READ from this tree.  Every one was opened.
SH4_TCR0 = 0xffd80010           # thirdparty/sh4_tmureg.h:54
SH4_TCR1 = 0xffd8001c           # :57
SH4_TCR2 = 0xffd80028           # :60
SH4_DMATCR0 = 0xffa00008        # sh4_dmacreg.h:39
SH4_DMATCR1 = 0xffa00018        # :44   -- the stride is 0x10 up to channel 3
SH4_DMATCR7 = 0xffa00088        # :84   -- the far end of the fall-through chain
SH4_ICR = 0xffd00000            # thirdparty/sh4_intcreg.h:79   ("16bit")
SH4_RCR1 = 0xffc80038           # thirdparty/sh4_rtcreg.h:68
SH4_PVR_ADDR = 0xff000030       # thirdparty/sh4_cpu.h:187
SH4_PRR_ADDR = 0xff000044       # :189
SH4_PVR_SH7751 = 0x04110000     # :196   -- what SH7751R's pvr field holds
SH4_PRR_7751R = 0x00000110      # :200
UNCLAIMED = 0xff00fffc          # no `case` in DEVICE_ACCESS(sh4); reaches `default:`

#  The six TCR bits DEVICE_ACCESS(sh4) does not model.  thirdparty/sh4_tmureg.h
#  :75-82.  TCR_UNF (0x0100) is deliberately NOT here -- it IS modelled, and V15
#  uses that fact.
TCR_ICPF, TCR_ICPE1, TCR_ICPE0 = 0x0200, 0x0080, 0x0040
TCR_CKEG1, TCR_CKEG0, TCR_TPSC2 = 0x0010, 0x0008, 0x0004
TCR_UNF = 0x0100
TCR_UNIMPLEMENTED = (TCR_ICPF | TCR_ICPE1 | TCR_ICPE0 |
                     TCR_CKEG1 | TCR_CKEG0 | TCR_TPSC2)      # 0x02dc
TCR_REJECT = TCR_ICPF | TCR_TPSC2                            # 0x0204, V21's

#  *** THE BITS AT THE SAME REGISTER THAT ARE MODELLED. ***  A mask pinned only
#  from BELOW -- every bit in it is rejected -- cannot see a guard that GREW, and
#  a guard that grew takes a working feature away from the guest for good.  These
#  three are the ones widening TCR_UNIMPLEMENTED would swallow, and all three are
#  live: TCR_UNIE is consumed at dev_sh4.c:313 (`if (d->tcr[i] & TCR_UNIE)`), so
#  adding it to the mask means the guest can never enable the timer interrupt;
#  TCR_TPSC0 and TCR_TPSC1 are the prescaler switch's own two bits, so adding
#  either makes two of the four TPSC codes unusable.  thirdparty/sh4_tmureg.h:79,
#  :83-84.
TCR_UNIE = 0x0020
TCR_TPSC1, TCR_TPSC0 = 0x0002, 0x0001

#  The eight-bit window the TCR singleton sweep walks, low bit first -- one
#  `shll` apart, so ONE session and ONE register cover it.  Six are rejected and
#  the two modelled ones SITTING BETWEEN THEM are accepted, which is why a sweep
#  says more than either half alone: bits 0x0020 and 0x0100 are not at the end of
#  the range where an off-by-one mask would put them, they are in the middle.
TCR_SWEEP = [TCR_TPSC2, TCR_CKEG0, TCR_CKEG1, TCR_UNIE,
             TCR_ICPE0, TCR_ICPE1, TCR_UNF, TCR_ICPF]

#  thirdparty/sh4_rtcreg.h:72-73.  TWO independent features, one guard.
SH_RCR1_CIE, SH_RCR1_AIE = 0x10, 0x08
#  :71 and :74.  The two nearest bits the guard must NOT take, and they bracket
#  it: CF is above CIE and AF is below AIE.  `odata = d->rtc_rcr1` is unmasked
#  (dev_sh4.c:2256), so unlike DMATCR a plain read-back sees these exactly.
SH_RCR1_CF, SH_RCR1_AF = 0x80, 0x01

#  machine_landisk.c:81.  P64 -> 33333333/64 = 520833.328125, P4 -> 8333333.25.
#  The naive fix (guard left below the prescaler switch) installs P4 for a
#  rejected write, because 0x0204 & 3 == 0.  V22 is the row that sees it.
PCLOCK = 33333333
HZ_P64 = "520833"
HZ_P4 = "8333333"
#  The other two prescaler codes.  *** THESE THREE CONSTANTS ARE UNUSED TODAY AND ARE KEPT
#  DELIBERATELY, which is a claim that needs saying rather than leaving to be discovered. ***
#  They are residue of an aborted 33->43 row edit that a transient API failure killed
#  mid-write, and the comment here originally described row V34 IN THE PRESENT TENSE as
#  though it existed.  It does not; nor do V33, V37 or V39.  Those rows are PLANNED, in
#  `sh4valrows`, and the constants are left in place because that round needs them.
#
#  *** THE RESTORE THAT FOLLOWED THAT ABORT WAS CALLED "VERIFIED 33/33" AND THE PHANTOM
#  REFERENCES SURVIVED IT. ***  They survived because the identity rows -- V30 on planted
#  opcodes, V31 on the row count -- are the two things that caught the half-edit, and
#  NEITHER CAN SEE A COMMENT OR AN UNUSED CONSTANT.  A flagship-seat read found them.  The
#  lesson is not that the identity discipline failed; it is that "verified" means verified
#  BY SOMETHING, and naming what that something cannot see is part of the claim.
#
#  No two of the four strings are a prefix of another, so `startswith` discriminates all
#  four when the rows do land.
HZ_P16 = "2083333"
HZ_P256 = "130208"
HZ_TPSC = (HZ_P4, HZ_P16, HZ_P64, HZ_P256)      # indexed by `idata & 3`

#  Every #447 diagnostic ends this way.  Counted, never matched by register name
#  -- see the cold-debugger note in the docstring.
LATCHED = "-- write ignored.  (once per bit) ]"
VAL_RE = re.compile(r"\[ sh4: [^\n]*" + re.escape(LATCHED))

#  The four diagnostics this round REPLACED.  None of them may come back.
PREFIX_MSGS = ["Unimplemented SH4 timer control",
               "Attempt to set top 8 ",
               "IRLM not yet ",
               "TODO: RTC interrupt enable"]

#  Guest scratch, shared with sh4_pcic_probe: landisk RAM is 64 MB at 0x0c000000
#  (machine_landisk.c:84) and 0x8c010000 is its P1 alias, past the 0x8c002000
#  entry point and inside the loaded image.
CODE, DEST, RAMSRC = P.CODE, P.DEST, P.RAMSRC
POISON = P.POISON

#  Instruction halfwords.  EVERY ONE is checked against the emulator's own
#  disassembler in a session that executed it -- row V30.  A wrong register
#  field is silent: it yields 0, which a zero-valued oracle accepts by accident.
OPS = {
    0x0009: "nop",
    0x2100: "mov.b r0,@r1",
    0x2101: "mov.w r0,@r1",
    0x2102: "mov.l r0,@r1",
    0x2140: "mov.b r4,@r1",
    0x2141: "mov.w r4,@r1",
    0x2142: "mov.l r4,@r1",
    0x2162: "mov.l r6,@r1",
    0x2322: "mov.l r2,@r3",
    0x2560: "mov.b r6,@r5",
    0x2781: "mov.w r8,@r7",
    0x29a2: "mov.l r10,@r9",
    0x29b2: "mov.l r11,@r9",
    0x6212: "mov.l @r1,r2",
    0x6252: "mov.l @r5,r2",
    0x6272: "mov.l @r7,r2",
    0x6292: "mov.l @r9,r2",
    0x710c: "add #12,r1",
    0x7110: "add #16,r1",
    0x7120: "add #32,r1",
}

#  Store opcode by access width, `mov.X r0,@r1`.  The device sees len == the key.
ST = {1: 0x2100, 2: 0x2101, 4: 0x2102}

#  ------------------------------------------------------------- WIDTH CENSUS
#  (site, address, len, value, does it trip the guard?).  Pinned by V9.
#
#  Two cells are STRUCTURALLY unreachable rather than skipped, and the table says
#  so by carrying them as non-tripping: DMATCR at len 1 and 2 cannot satisfy
#  `idata & ~0x00ffffff`, because idata is at most 0xffff.  TCR at len=1 reaches
#  five of its six bits but not TCR_ICPF (0x0200); len 2 and 4 reach all six.
CENSUS = [
    ("TCR0", SH4_TCR0, 1, TCR_CKEG0, True),
    ("TCR0", SH4_TCR0, 2, TCR_ICPF | TCR_TPSC2, True),
    ("TCR0", SH4_TCR0, 4, TCR_ICPF | TCR_TPSC2, True),
    ("TCR0", SH4_TCR0, 1, 0x02, False),
    ("TCR0", SH4_TCR0, 2, 0x0002, False),
    ("TCR0", SH4_TCR0, 4, 0x00000002, False),

    ("DMATCR0", SH4_DMATCR0, 1, 0x10, False),
    ("DMATCR0", SH4_DMATCR0, 2, 0x0010, False),
    ("DMATCR0", SH4_DMATCR0, 4, 0x01000000, True),
    ("DMATCR0", SH4_DMATCR0, 4, 0x00ffffff, False),

    ("ICR", SH4_ICR, 1, 0x80, True),
    ("ICR", SH4_ICR, 2, 0x0080, True),
    ("ICR", SH4_ICR, 4, 0x00000080, True),
    ("ICR", SH4_ICR, 1, 0x7f, False),
    ("ICR", SH4_ICR, 2, 0x007f, False),
    ("ICR", SH4_ICR, 4, 0x0000007f, False),

    ("RCR1", SH4_RCR1, 1, SH_RCR1_CIE | SH_RCR1_AIE, True),
    ("RCR1", SH4_RCR1, 2, SH_RCR1_CIE | SH_RCR1_AIE, True),
    ("RCR1", SH4_RCR1, 4, SH_RCR1_CIE | SH_RCR1_AIE, True),
    ("RCR1", SH4_RCR1, 1, 0x01, False),
    ("RCR1", SH4_RCR1, 2, 0x0001, False),
    ("RCR1", SH4_RCR1, 4, 0x00000001, False),
]
#  IDENTITY constants.  A file copied into a tree where it no longer runs all of
#  its rows -- or all of its census cells -- must not report a green verdict.
EXPECT_ROWS = 33
EXPECT_CENSUS = {1: 7, 2: 7, 4: 8}

DISASM = {}
rows = []
ALLTXT = []      # every session's output, so V29 can look at the WHOLE run


# ------------------------------------------------------------------- helpers
def run(pre, hws, nstep, label, kw, pre_run=None, go=None):
    """One session that plants `hws` at CODE and executes it.

    `go` swaps the cold-debugger `step` for a free-running command (V32 uses
    `continue`).  The disassembly census is skipped in that case, because
    session() sends it AFTER the commands and every opcode V32 plants is
    already covered by a stepped session.
    """
    cmds = pre + P.poke(hws) + (pre_run or []) + ["pc=0x%x" % CODE]
    buf, alive, st = P.session(cmds + ([go] if go else []), nstep, label,
                               disasm_upto=0 if go else 2 * len(hws), **kw)
    DISASM.update(P.DISASM)
    txt = (buf or "").replace("\r", "")
    ALLTXT.append(txt)
    return txt, alive, st


def store(addr, val, width, label, kw):
    """One guest STORE of `val` to `addr` at `width` bytes.  Nothing else."""
    return run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                "r0=0x%x" % val, "r1=0x%x" % addr],
               [ST[width], 0x0009], 1, label, kw)


def diags(txt):
    """Every #447 diagnostic line in a session's output, in order."""
    return VAL_RE.findall(txt)


def row(name, ok, got, want):
    rows.append((name, bool(ok), got, want))


def tcr_line(nr, bits):
    return ("[ sh4: timer %d: unimplemented TCR bits 0x%04x -- write ignored."
            "  (once per bit) ]" % (nr, bits))


def dma_line(ch, val):
    return ("[ sh4: DMA channel %d: transfer count 0x%08x exceeds 24 bits"
            " -- write ignored.  (once per bit) ]" % (ch, val))


def icr_line(bits):
    return ("[ sh4: INTC: ICR IRLM bit 0x%04x not implemented -- write ignored."
            "  (once per bit) ]" % bits)


CLK_RE = re.compile(r"\[ sh4 timer \d clock set to ([0-9.]+) Hz \]")


def clklines(txt):
    """Every accepted TCR write's debug() clock line, in order, any timer.

    An ACCEPTED control word prints exactly one of these and a REJECTED one
    prints none, so the count is a second, independent witness of the guard's
    disposition -- and the only witness of `timer_hz`, which is not a guest
    register.  V22 is the row that first needed it.

    V33/V34/V37/V39 are PLANNED, in `sh4valrows`, and DO NOT EXIST IN THIS FILE.
    An earlier draft of this sentence named them in the present tense; that was
    residue of an aborted edit and is corrected here rather than deleted, because
    the accept-side rows they stand for are the ones a flagship review called the
    in-round carve-out this round owes.
    """
    return CLK_RE.findall(txt)


def rcr1_line(bits):
    return ("[ sh4: RTC: RCR1 interrupt enable 0x%02x not implemented -- write"
            " ignored.  (once per bit) ]" % bits)


# =============================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    ap.add_argument("kernel")
    a = ap.parse_args()
    kw = dict(binary=a.binary, kernel=a.kernel)

    #  A missing binary or image is an OPERATIONAL failure, not a measurement.
    for p in (a.binary, a.kernel):
        if not os.path.exists(p):
            print("OPERATIONAL FAILURE: %s does not exist (cwd=%s)"
                  % (p, os.getcwd()))
            print("SH4_VAL_FAIL")
            return 2

    t_all = time.time()
    vals = []

    # ------------------------------------------------------------- V1-V4 controls
    #  If these are red, nothing else in the file means anything.
    txt, alive, st = run(["put w 0x%x, 0x5a5a1234" % RAMSRC,
                          "put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r1=0x%x" % RAMSRC, "r3=0x%x" % DEST],
                         [0x6212, 0x2322], 2, "V1", kw)
    v1 = P.dumped(txt)
    vals.append(v1)
    row("V1 LIVENESS: a known word returns through the same decode",
        st and alive and v1 == P.le(0x5a5a1234),
        "started=%s alive=%s val=%s" % (st, alive, v1),
        "val=%s" % P.le(0x5a5a1234))

    #  *** THE CONTROL THE FOOTBRIDGE PROBE LACKED. ***  That one returned 0x0
    #  everywhere WITH ITS RAM CONTROL GREEN, because 0 is what both a live
    #  device and a dead path answer.  These two answer values only this device
    #  synthesises -- and they are synthesised in DEVICE_ACCESS(sh4) itself, not
    #  in some other function of the same file, so they prove the switch under
    #  test was entered.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r1=0x%x" % SH4_PVR_ADDR, "r3=0x%x" % DEST],
                         [0x6212, 0x2322], 2, "V2", kw)
    v2 = P.dumped(txt)
    vals.append(v2)
    row("V2 DEVICE SIGNATURE: PVR reads 0x04110000 in DEVICE_ACCESS(sh4)",
        st and alive and v2 == P.le(SH4_PVR_SH7751),
        "started=%s alive=%s val=%s" % (st, alive, v2),
        "val=%s -- synthesised at the PVR case; RAM would answer %s"
        % (P.le(SH4_PVR_SH7751), P.le(0)))

    #  THE SMALL-NON-ZERO ROW.  0x00000110 accepts nothing but the right
    #  instruction at the right address.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r1=0x%x" % SH4_PRR_ADDR, "r3=0x%x" % DEST],
                         [0x6212, 0x2322], 2, "V3", kw)
    v3 = P.dumped(txt)
    vals.append(v3)
    row("V3 DEVICE SIGNATURE: PRR reads 0x00000110 (small non-zero)",
        st and alive and v3 == P.le(SH4_PRR_7751R),
        "started=%s alive=%s val=%s" % (st, alive, v3),
        "val=%s" % P.le(SH4_PRR_7751R))

    #  SCOPE, and it also pins a claim this round ASSESSED and deliberately did
    #  NOT change: DEVICE_ACCESS(sh4)'s own `default:` does not kill, because its
    #  exit(1) sits under `#ifdef SH4_DEBUG` and nothing in src/ defines that.
    #  The claim is one grep away from a reader; this row makes it fail loudly if
    #  anyone ever defines it.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r1=0x%x" % UNCLAIMED, "r3=0x%x" % DEST],
                         [0x6212, 0x2322], 2, "V4", kw)
    v4 = P.dumped(txt)
    vals.append(v4)
    row("V4 SCOPE: the `default:` arm answers 0, SURVIVES, and is not a #447 site",
        st and alive and v4 == P.le(0)
        and ("[ sh4: read from addr 0x%x ]" % UNCLAIMED) in txt
        and not diags(txt),
        "started=%s alive=%s val=%s default-said=%s val-diags=%d"
        % (st, alive, v4,
           ("[ sh4: read from addr 0x%x ]" % UNCLAIMED) in txt, len(diags(txt))),
        "alive=True, val=%s, the default diagnostic, and no #447 line" % P.le(0))

    # ------------------------------------------------- V5-V9  the width census
    #  #443's census issued ONE width and a `len == 2` kill passed 29/29.
    seen = {}
    per_site = {}
    for site, addr, width, val, trips in CENSUS:
        lab = "%s w=%d v=0x%x" % (site, width, val)
        txt, alive, st = store(addr, val, width, lab, kw)
        d = diags(txt)
        ok = st and alive and (bool(d) == trips)
        seen[width] = seen.get(width, 0) + 1
        per_site.setdefault(site, []).append((lab, ok, alive, len(d), trips))

    for site in ("TCR0", "DMATCR0", "ICR", "RCR1"):
        cells = per_site.get(site, [])
        bad = [c[0] for c in cells if not c[1]]
        widths = sorted({int(c[0].split("w=")[1].split(" ")[0]) for c in cells})
        row("V%d %s: every reachable width SURVIVES and diagnoses iff the value "
            "trips" % (5 + ("TCR0", "DMATCR0", "ICR", "RCR1").index(site), site),
            cells and not bad,
            "cells=%d widths=%s bad=%s" % (len(cells), widths, bad[:4]),
            "all cells alive, diagnostic present exactly on the tripping values")

    row("V9 WIDTH CENSUS PIN: the table itself, so a shrunken file cannot pass",
        seen == EXPECT_CENSUS and len(CENSUS) == sum(EXPECT_CENSUS.values()),
        "issued=%s total=%d" % (dict(sorted(seen.items())), len(CENSUS)),
        "issued=%s total=%d (len=8 is unreachable from SH-4 code -- see the "
        "docstring)" % (EXPECT_CENSUS, sum(EXPECT_CENSUS.values())))

    # ------------------------------------------------ V10  the direction axis
    #  All four guards sit on the WRITE path.  One session reads all four.
    txt, alive, st = run(
        ["put w 0x%x, 0x%08x" % (DEST, POISON),
         "r1=0x%x" % SH4_TCR0, "r5=0x%x" % SH4_DMATCR0,
         "r7=0x%x" % SH4_ICR, "r9=0x%x" % SH4_RCR1, "r3=0x%x" % DEST],
        [0x6212, 0x6252, 0x6272, 0x6292, 0x2322], 5, "V10", kw)
    v10 = P.dumped(txt)
    vals.append(v10)
    row("V10 DIRECTION: a READ of all four sites survives and diagnoses nothing",
        st and alive and v10 is not None and not diags(txt),
        "started=%s alive=%s last-val=%s diags=%d"
        % (st, alive, v10, len(diags(txt))),
        "alive=True and zero #447 lines -- every guard is write-only")

    # ------------------------------------------ V11/V12  the INSTANCE sub-key
    #  A latch keyed on the class alone reports timer 0 and silences 1 and 2.
    #  Three TCRs reach one `case` by fall-through; so do eight DMATCRs.
    txt, alive, st = run(["r0=0x%x" % TCR_TPSC2, "r1=0x%x" % SH4_TCR0],
                         [0x2101, 0x710c, 0x2101, 0x710c, 0x2101],
                         5, "V11", kw)
    want11 = [tcr_line(n, TCR_TPSC2) for n in (0, 1, 2)]
    got11 = diags(txt)
    row("V11 INSTANCE: TCR0, TCR1 and TCR2 each diagnose, in ONE process",
        st and alive and got11 == want11,
        "alive=%s lines=%d %s" % (alive, len(got11), got11[:4]),
        "exactly these three, in order: %s" % want11)

    txt, alive, st = run(["r0=0x01000000", "r1=0x%x" % SH4_DMATCR0],
                         [0x2102, 0x7110, 0x2102, 0x7110, 0x2102, 0x7110,
                          0x2102, 0x7120, 0x2102, 0x7110, 0x2102, 0x7110,
                          0x2102, 0x7110, 0x2102],
                         15, "V12", kw)
    want12 = [dma_line(c, 0x01000000) for c in range(8)]
    got12 = diags(txt)
    row("V12 INSTANCE: all EIGHT DMA channels diagnose, in ONE process",
        st and alive and got12 == want12,
        "alive=%s lines=%d %s" % (alive, len(got12), got12[:3]),
        "exactly eight, channels 0..7 in order")

    # ------------------------------------------ V13/V14  the BIT sub-key
    #  RCR1's one guard covers TWO independent features and TCR's covers SIX.
    #  A latch keyed on (class, instance) reports the first and swallows the rest.
    txt, alive, st = run(["r0=0x%x" % SH_RCR1_AIE, "r4=0x%x" % SH_RCR1_CIE,
                          "r1=0x%x" % SH4_RCR1],
                         [0x2100, 0x2140, 0x2100], 3, "V13", kw)
    want13 = [rcr1_line(SH_RCR1_AIE), rcr1_line(SH_RCR1_CIE)]
    got13 = diags(txt)
    row("V13 BIT: RCR1 AIE then CIE then AIE -> exactly TWO lines",
        st and alive and got13 == want13,
        "alive=%s lines=%d %s" % (alive, len(got13), got13),
        "exactly two (a per-register latch gives one, no latch gives three)")

    txt, alive, st = run(["r0=0x%x" % TCR_TPSC2, "r4=0x%x" % TCR_CKEG0,
                          "r1=0x%x" % SH4_TCR0],
                         [0x2101, 0x2141, 0x2101], 3, "V14", kw)
    want14 = [tcr_line(0, TCR_TPSC2), tcr_line(0, TCR_CKEG0)]
    got14 = diags(txt)
    row("V14 BIT: TCR0 TPSC2 then CKEG0 then TPSC2 -> exactly TWO lines",
        st and alive and got14 == want14,
        "alive=%s lines=%d %s" % (alive, len(got14), got14),
        "exactly two")

    # ------------------------------------------ V15  the key is the MASKED bits
    #  TCR_UNF (0x0100) IS modelled, so 0x0004 and 0x0104 are the SAME complaint.
    #  A latch keyed on the written value makes them two, and a guest looping over
    #  the unmasked bits then prints without bound -- fatal() has no -q early-out.
    txt, alive, st = run(["r0=0x%x" % TCR_TPSC2,
                          "r4=0x%x" % (TCR_UNF | TCR_TPSC2),
                          "r1=0x%x" % SH4_TCR0],
                         [0x2101, 0x2141], 2, "V15", kw)
    got15 = diags(txt)
    row("V15 KEY: TCR0 0x0004 then 0x0104 -> exactly ONE line (the key is the "
        "masked bits, not the value)",
        st and alive and got15 == [tcr_line(0, TCR_TPSC2)],
        "alive=%s lines=%d %s" % (alive, len(got15), got15),
        "exactly one: %s" % tcr_line(0, TCR_TPSC2))

    # ------------------------------------------------- V16  the CLASS sub-key
    #  A per-DEVICE latch -- the "1 of 4 kinds" hazard #438 recorded -- passes
    #  every row above and fails this one.
    #
    #  *** THE BIT-SETS OVERLAP ON PURPOSE, AND THE FIRST DRAFT OF THIS ROW DID
    #  NOT. ***  That draft hit all four sites in one process with DISJOINT
    #  offending bits, so a mutant collapsing every class into one still had
    #  room in the union for all four complaints and the row passed.  MEASURED:
    #  `cls = 0;` at the top of sh4_val_first() scored 32/32 against the whole
    #  file.  Six stores, arranged so that FIVE of the six class PAIRS share an
    #  offending bit value:
    #
    #    1 TCR0    TCR_ICPE1  0x0080 -> bit 0x80 at (TCRBITS, 0)
    #    2 ICR                0x0080 -> bit 0x80 at (ICRIRLM, 0)
    #    3 DMATCR0 0x80000000        -> bit 0x80 at (DMATCR,  0)
    #    4 RCR1    SH_RCR1_AIE 0x08  -> bit 0x08 at (RCR1INT, 0)
    #    5 TCR0    TCR_CKEG0  0x0008 -> bit 0x08 at (TCRBITS, 0)
    #    6 DMATCR0 0x08000000        -> bit 0x08 at (DMATCR,  0)
    #
    #  Collapse any of TCR/ICR/DMATCR into each other, or RCR1 into TCR or
    #  DMATCR, and a line goes missing.  The ONE pair this cannot reach is
    #  ICR<->RCR1: ICR's only offending bit is 0x80 and RCR1's are 0x08 and
    #  0x10, so their bit-sets are disjoint by construction and no value of the
    #  written word can make them collide.  Recorded, not papered over.
    txt, alive, st = run(
        ["r0=0x%x" % TCR_ICPE1, "r4=0x%x" % TCR_CKEG0, "r1=0x%x" % SH4_TCR0,
         "r6=0x%x" % SH_RCR1_AIE, "r5=0x%x" % SH4_RCR1,
         "r8=0x80", "r7=0x%x" % SH4_ICR,
         "r10=0x80000000", "r11=0x08000000", "r9=0x%x" % SH4_DMATCR0],
        [0x2101, 0x2781, 0x29a2, 0x2560, 0x2141, 0x29b2], 6, "V16", kw)
    want16 = [tcr_line(0, TCR_ICPE1),
              icr_line(0x80),
              dma_line(0, 0x80000000),
              rcr1_line(SH_RCR1_AIE),
              tcr_line(0, TCR_CKEG0),
              dma_line(0, 0x08000000)]
    got16 = diags(txt)
    row("V16 CLASS: six complaints across all four sites, with bit-sets that "
        "COLLIDE across classes",
        st and alive and got16 == want16,
        "alive=%s lines=%d %s" % (alive, len(got16), got16[:2]),
        "exactly six, in order -- a latch that merges any two classes except "
        "ICR<->RCR1 loses at least one")

    # ----------------------------------- V17/V18  RCR1: the store was UPSTREAM
    #  *** THE ROW THE NAIVE FIX FAILS. ***  Write an accepted value, then a
    #  rejected one, then read the register back THROUGH THE GUEST.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r0=0x01", "r4=0x%x" % (SH_RCR1_CIE | SH_RCR1_AIE),
                          "r1=0x%x" % SH4_RCR1, "r3=0x%x" % DEST],
                         [0x2100, 0x2140, 0x6212, 0x2322], 4, "V17", kw)
    v17 = P.dumped(txt)
    vals.append(v17)
    row("V17 RCR1 UPSTREAM STORE: a rejected value is NOT readable back",
        st and alive and v17 == P.le(0x01) and len(diags(txt)) == 1,
        "alive=%s val=%s diags=%d" % (alive, v17, len(diags(txt))),
        "val=%s -- the accepted 0x01, not the rejected 0x18 (DEST was poisoned "
        "%08x, so this is a real read)" % (P.le(0x01), POISON))

    #  SECOND OFFENCE.  #443 measured a brace slip that restored the first
    #  offence and corrupted every one after it, passing all 29 rows.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r0=0x01", "r4=0x%x" % (SH_RCR1_CIE | SH_RCR1_AIE),
                          "r1=0x%x" % SH4_RCR1, "r3=0x%x" % DEST],
                         [0x2100, 0x2140, 0x2140, 0x6212, 0x2322], 5, "V18", kw)
    v18 = P.dumped(txt)
    vals.append(v18)
    row("V18 RCR1 SECOND OFFENCE: still not readable back once the latch is set",
        st and alive and v18 == P.le(0x01) and len(diags(txt)) == 1,
        "alive=%s val=%s diags=%d" % (alive, v18, len(diags(txt))),
        "val=%s and exactly one diagnostic (the second write is latched, not "
        "accepted)" % P.le(0x01))

    # ------------------------------ V19/V20  DMATCR: the read path LAUNDERS
    #  The read arm masks with 0x00ffffff, so the top bits are invisible either
    #  way.  Discriminate on the LOW 24 bits instead.
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r0=0x10", "r4=0x01abcdef",
                          "r1=0x%x" % SH4_DMATCR0, "r3=0x%x" % DEST],
                         [0x2102, 0x2142, 0x6212, 0x2322], 4, "V19", kw)
    v19 = P.dumped(txt)
    vals.append(v19)
    row("V19 DMATCR LOW 24: a rejected count does not overwrite the accepted one",
        st and alive and v19 == P.le(0x10) and len(diags(txt)) == 1,
        "alive=%s val=%s diags=%d" % (alive, v19, len(diags(txt))),
        "val=%s, NOT %s -- the read arm masks the top byte, so only the low 24 "
        "bits can see this" % (P.le(0x10), P.le(0x00abcdef)))

    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r0=0x10", "r4=0x01abcdef", "r6=0x02123456",
                          "r1=0x%x" % SH4_DMATCR0, "r3=0x%x" % DEST],
                         [0x2102, 0x2142, 0x2162, 0x6212, 0x2322], 5, "V20", kw)
    v20 = P.dumped(txt)
    vals.append(v20)
    want20 = [dma_line(0, 0x01abcdef), dma_line(0, 0x02123456)]
    got20 = diags(txt)
    row("V20 DMATCR SECOND OFFENCE: two distinct top bits -> two lines, state kept",
        st and alive and v20 == P.le(0x10) and got20 == want20,
        "alive=%s val=%s lines=%s" % (alive, v20, got20),
        "val=%s and both lines (bit 24 and bit 25 are different features to the "
        "latch)" % P.le(0x10))

    # ------------------------------ V21/V22  TCR: timer_hz was set UPSTREAM
    txt, alive, st = run(["put w 0x%x, 0x%08x" % (DEST, POISON),
                          "r0=0x02", "r4=0x%x" % (TCR_ICPF | TCR_TPSC2),
                          "r1=0x%x" % SH4_TCR0, "r3=0x%x" % DEST],
                         [0x2101, 0x2141, 0x6212, 0x2322], 4, "V21", kw)
    v21 = P.dumped(txt)
    vals.append(v21)
    clocks = clklines(txt)
    row("V21 TCR REJECT: a rejected control word is NOT readable back",
        st and alive and v21 == P.le(0x02) and len(diags(txt)) == 1,
        "alive=%s val=%s diags=%d" % (alive, v21, len(diags(txt))),
        "val=%s -- the accepted TPSC_P64, not the rejected 0x0204" % P.le(0x02))

    #  *** THE ROW FOR THE STATE NO GUEST READ CAN SEE. ***  `timer_hz` is not a
    #  guest register.  Leave the guard where it was and drop exit(1) and the
    #  rejected write installs pclock/4, because 0x0204 & 3 == 0 -- a silent
    #  fault where the old one was loud.  The debug() line is its only witness.
    row("V22 TCR timer_hz: ONE clock line, and it is P64 -- never the P4 the "
        "naive fix installs",
        st and alive and len(clocks) == 1
        and clocks[0].startswith(HZ_P64) and HZ_P4 not in txt,
        "clock-lines=%d %s p4-seen=%s" % (len(clocks), clocks, HZ_P4 in txt),
        "exactly one, starting %s (%d/64); %s (%d/4) must never appear"
        % (HZ_P64, PCLOCK, HZ_P4, PCLOCK))

    # ------------------------------------------------------- V23  the boundary
    #  0x00ffffff is the largest count the register holds; 0x01000000 is the
    #  first that does not.  Pins the mask from both sides.
    lo = [c for c in per_site["DMATCR0"] if "0xffffff" in c[0]]
    hi = [c for c in per_site["DMATCR0"] if "0x1000000" in c[0]]
    row("V23 BOUNDARY: DMATCR accepts 0x00ffffff and rejects 0x01000000",
        len(lo) == 1 and len(hi) == 1 and lo[0][1] and hi[0][1]
        and lo[0][3] == 0 and hi[0][3] == 1,
        "accept-cell=%s reject-cell=%s" % (lo, hi),
        "the 24-bit boundary exactly: no diagnostic below it, one above")

    # ---------------------------------------------------- V24-V28  the FORMAT
    #  #444 pinned ONE argument and left the format free; four seats found
    #  mutants in other fields of the same string.  These pin whole lines, and
    #  each pins a field that VARIES, so a hardcoded literal cannot pass.
    row("V24 FORMAT: the whole TCR line, across three timers and two bit-sets",
        got11 == want11 and got14 == want14,
        "instances=%s bits=%s" % (got11 == want11, got14 == want14),
        "every field: site, timer number, offending bits, disposition, suffix")

    row("V25 FORMAT: the whole DMA line, across eight channels and two counts",
        got12 == want12 and got20 == want20,
        "channels=%s counts=%s" % (got12 == want12, got20 == want20),
        "every field: site, channel number, count, disposition, suffix")

    txt, alive, st = store(SH4_ICR, 0x80, 2, "V26", kw)
    got26 = diags(txt)
    row("V26 FORMAT: the whole ICR line",
        st and alive and got26 == [icr_line(0x80)],
        "alive=%s lines=%s" % (alive, got26),
        "exactly: %s" % icr_line(0x80))

    txt, alive, st = store(SH4_RCR1, SH_RCR1_CIE | SH_RCR1_AIE, 1, "V27", kw)
    got27 = diags(txt)
    row("V27 FORMAT: the whole RCR1 line, across three bit-sets",
        st and alive and got27 == [rcr1_line(SH_RCR1_CIE | SH_RCR1_AIE)]
        and got13 == want13,
        "alive=%s both=%s one=%s" % (alive, got13 == want13, got27),
        "exactly: %s, plus V13's two"
        % rcr1_line(SH_RCR1_CIE | SH_RCR1_AIE))

    #  ALL SIX BITS AT ONCE.  Drop any one of them from the guard's mask and the
    #  printed value changes, so this single line pins the whole mask.
    txt, alive, st = store(SH4_TCR0, TCR_UNIMPLEMENTED, 2, "V28", kw)
    got28 = diags(txt)
    row("V28 MASK: all six unimplemented TCR bits print as 0x%04x"
        % TCR_UNIMPLEMENTED,
        st and alive and got28 == [tcr_line(0, TCR_UNIMPLEMENTED)],
        "alive=%s lines=%s" % (alive, got28),
        "exactly: %s" % tcr_line(0, TCR_UNIMPLEMENTED))

    # ------------------------------- V32  fatal() is not debug(), MEASURED
    #  *** THE ONE ROW IN THIS TREE THAT CAN TELL THEM APART, AND IT EXISTS
    #  BECAUSE A MUTANT SCORED 32/32 WITHOUT IT. ***  Swapping all four fatal()
    #  calls for debug() is a real defect -- debug() has a quiet_mode early-out
    #  and fatal() does not, so under -q the operator loses every one of these
    #  complaints -- and every other row in this file is blind to it.  The
    #  standing project rule says a probe "cannot tell fatal() from debug() by
    #  presence", and that is true of a COLD debugger: src/core/debugmsg.c
    #  :367-373 reads
    #        bool ss = single_step || about_to_enter_single_step;
    #        int v = verbose;  if (emul_executing) v--;  if (ss) v++;
    #        if ((quiet_mode && !ss) || v < 0) return;
    #  so while single-stepping `ss` is true, `v` goes UP, and debug() prints
    #  exactly like fatal().  FREE-RUNNING inverts both terms: `ss` is false and
    #  `emul_executing` is true, so v < 0 and debug() returns.
    #
    #  MEASURED on two builds, one process each -- and note it needs no -q:
    #    fix (fatal)  step: printed    continue: printed
    #    M13 (debug)  step: printed    continue: ABSENT
    #
    #  The sentinel is the mechanism's own liveness control: if `continue` never
    #  ran the sequence, DEST still holds the poison and this row fails as a
    #  BROKEN MEASUREMENT rather than passing as an absent diagnostic.
    txt, alive, st = run(
        ["put w 0x%x, 0x%08x" % (DEST, POISON),
         "r0=0x%x" % (SH_RCR1_CIE | SH_RCR1_AIE), "r1=0x%x" % SH4_RCR1,
         "r2=0x5a5a1234", "r3=0x%x" % DEST],
        [0x2100, 0x2322, 0x0009], 0, "V32",
        dict(kw, timeout=40), pre_run=["breakpoint add 0x%x" % (CODE + 4)],
        go="continue")
    v32 = P.dumped(txt)
    vals.append(v32)
    row("V32 FREE-RUNNING: the diagnostic survives `continue`, so it is "
        "fatal() and not debug()",
        st and alive and v32 == P.le(0x5a5a1234)
        and diags(txt) == [rcr1_line(SH_RCR1_CIE | SH_RCR1_AIE)],
        "started=%s alive=%s sentinel=%s lines=%s"
        % (st, alive, v32, diags(txt)),
        "sentinel=%s (the sequence really ran free) AND the diagnostic present"
        % P.le(0x5a5a1234))

    # -------------------------------------------------- V29  the OLD wording
    #  A revert that keeps the survival but restores the old text -- or a
    #  half-revert of one arm -- shows up here and nowhere else.
    all_txt = "".join(ALLTXT)
    back = [m for m in PREFIX_MSGS if m in all_txt]
    row("V29 the four pre-fix diagnostics never come back, in ANY session",
        not back and len(ALLTXT) >= 30,
        "seen=%s sessions-scanned=%d" % (back, len(ALLTXT)),
        "none of: %s -- scanned over the WHOLE run, not one buffer"
        % PREFIX_MSGS)

    # ------------------------------------------------------- V30  disassembly
    #  EVERY hand-assembled halfword, checked against the emulator's OWN
    #  disassembler in a session that executed it.  A wrong register field is
    #  silent -- it produces a plausible address and a zero result.
    bad = {"%04x" % w: (DISASM.get(w), t) for w, t in OPS.items()
           if DISASM.get(w) != t}
    row("V30 every planted opcode matches the emulator's own disassembler",
        not bad, "mismatches=%s" % (bad or "none"),
        "all %d of: %s" % (len(OPS),
                           ", ".join("%04x" % w for w in sorted(OPS))))

    # ------------------------------------------------- V0, last: absent data
    n_ses = len(P.STARTS)
    n_ok = sum(1 for _, s in P.STARTS if s)
    row("V0 EVERY session reached the debugger prompt AND every arm produced data",
        n_ses > 0 and n_ok == n_ses and all(v is not None for v in vals),
        "sessions=%d started=%d failed=%s vals=%s"
        % (n_ses, n_ok, [l for l, s in P.STARTS if not s][:6], vals),
        "started == sessions > 0, and every value present")

    # ----------------------------------------------------------- V31 identity
    row("V31 IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, "rows=%d" % (len(rows) + 1),
        "rows=%d" % EXPECT_ROWS)

    print("=" * 78)
    print("#447  SH4 value guards in DEVICE_ACCESS(sh4) -- DETECTOR "
          "(-E landisk, unmodified)")
    print("  binary %s   kernel %s" % (a.binary, a.kernel))
    print("=" * 78)
    fails = 0
    for name, ok, got, want in rows:
        fails += 0 if ok else 1
        print("  %-4s %-70s" % ("ok" if ok else "FAIL", name))
        if not ok:
            print("       got  %s\n       want %s" % (got, want))
    print()
    print("  %d sessions, elapsed %.0f s" % (n_ses, time.time() - t_all))
    print("SH4_VAL_RESULT=%d/%d" % (len(rows) - fails, len(rows)))
    print("SH4_VAL_PASS" if fails == 0 else "SH4_VAL_FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
