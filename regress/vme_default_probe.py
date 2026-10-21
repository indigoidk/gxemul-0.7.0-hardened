#!/usr/bin/env python3
"""vme_default_probe.py -- rung-3 DETECTOR for dev_vme.c's `default:' arm (vmedefaultkill, #568).

REVISION 3 (2026-10-21), 38 rows, against fix568b (dev_vme.c md5 beb120eae1be112b682bd528f103191c), #568's pass-2
repair of fix568: the typedef claims the field only, the guest-reach sentence says attach reaches FOUR registers,
`default:''s exception sentence is for a guest data load or store, and the read announce prints `0x%llx' of
`(unsigned long long) odata' (D1; every value this arm can serve prints the same digits either way).
REVISION 2 (the 34-row instrument, frozen md5 19de15b3ea69af28e437cdf92e22c97e) was MEASURED over fix568 (dev_vme.c
md5 4e3e7fc220062b429f7d9d6e140fec9e) by kill table 1 (regress/artifacts/vmedefaultkill/killtable1_20261020/
KILLTABLE1_VS_PRETABLE.out: 24 legs, 22 killed, survivors M_ODATA0 and M_SERVED0 -- equivalent today) and table 1b
(killtable1_20261020/table1b/KILLTABLE1B.out: 3 legs, all killed); the floor breach M_IDATA left all 34 rows green on
the 34-row instrument (killtable1_20261020/idata/KILLTABLE_IDATA.out), and this revision closes it.  Revision 3 is
measured by kill table 2 (regress/artifacts/vmedefaultkill/killtable2_20261021/, fix568b, frozen rev 3).  After table
2 the repair-diff pass and the records confirmation corrected this docstring and two comments -- no code line: the
file is AST-identical to the frozen copy with the module docstring removed -- and tables 2b, 2c and 2d (killtable2_20261021/table2b/, table2c/, table2d/) measured the seven legs
it raised.

WHAT REVISION 3 CHANGES (the four-seat F2 adjudication, vme/f2, and its amendments):
  * four NEW rows -- `p2 zero wr' (its own session), `p2 nw rd 2' and `p2 nw wr 2' (a second pass in the SAME process
    as the non-word session), `p1 quiet' (the free-running census AND widths runs);
  * `p1 widths' gains two LANE-0 accesses (ld.hu 0xb0, st.b 0xb4): eight faults where there were six;
  * the CONTROL split (CONTROL_ROWS below, with its definition) and cause-free wording wherever a row stops before its
    check: `dependent check not exercised: pass 1 did not complete', `pass 1 silent' (that IS the announce channel),
    `unexpected stop pc=... before the row's check', `nodev r30=...: device signature absent, check not made';
  * a TIMEOUT is named as one -- `timeout:no-breakpoint', `timeout:no-prompt' -- distinct from a process death
    (`died:exit1') and from an assertion mismatch, so a load-induced red is never read as a product kill;
  * the `unasm' literal re-derived by hand (1441: see the comment beside it).

DEFECT (HEAD 1a59a47e = 5dbc000e's src tree; dev_vme.c byte-identical to the 0.7.0 import).  DEVICE_ACCESS(vme)
names TEN offsets (0x00, GCSRCTL 0x2c, TCR 0x4c, T1CMP 0x50, T1COUNT 0x54, TCTL 0x60, IRQEN 0x6c, IRQL3 0x80,
IRQL4 0x84, VBR 0x88); every other offset reaches `default:', which prints with debug() and calls exit(1).

THE FIX (#568, fix568b):
  population 2 -- the 26 header-named register WORD STARTS with no case (the header's 36 contiguous words
      0x00..0x8c minus the ten): exact labels, DECLINE + ANNOUNCE ONCE.  A read is served d->reg[w] (0: nothing
      writes those words); a write is dropped; one latched fatal() per register per instance, the first access's
      direction deciding the wording:
        [ vme: unimplemented read from register 0x%x (len %d) -- served 0x%llx.  (once) ]
        [ vme: unimplemented write to register 0x%x (len %d): 0x%llx -- declined.  (once) ]
  population 1 -- every offset that is not one of the 36 exact labels (the 988 unnamed word starts 0x90..0xffc
      and every sub-word start): FAULT.  `default:' keeps its two debug() lines and returns 0; memory_rw.c raises
      the m88k data-access exception (vector 3; VBR 0 at reset -> PC 0x18) with DMT0/DMD0/DMA0 recorded.

RUNG 3: real MC88100 instructions through real address decode and real memory_rw on the UNMODIFIED in-tree
`-E mvme88k -e mvme187' (machine_mvme88k.c attaches "vme addr=0x%x", VME2_BASE = 0xfff40000), started with `-M 64'
and a 4-byte dummy image at 0x10000 (no PROM).  STEPPED sessions feed the debugger on stdin (mk48_nvram_probe.py's
shape); FREE-RUNNING sessions drive it through a pty one command at a time and send nothing while the guest runs --
the debugger reads MAIN_CONSOLE, which is also the guest console's input (pcc2_width_probe.py's shape).  Only a
free-running session can tell fatal() from debug(): stepping makes both print; `free neg ctl' proves each run really
was free.

MECHANICS (src/cpus/cpu_m88k.c, cpu_m88k_instr_loadstore.c):
  * a data-access exception sets PSR.SFRZ and a second one while it is set becomes ERROR, so every STEPPED fault
    row has a session of its own; the FREE-RUNNING fault rows install `addu r1,r1,1 ; rte' at the vector (rte
    restores PSR from EPSR and resumes at SNIP = fault + 4) and COUNT the faults;
  * a faulting load writes no register -- destinations are seeded with a sentinel that must survive;
  * every other session puts `br' to itself at the vector (a zero word there is `goto bad': "UNIMPLEMENTED
    instruction at 0x18", "All machines stopped" -- regress/artifacts/vmedefaultkill/probe_20261020/explore2_FIX.out
    section (a)), and free-running ones put a breakpoint on it, so a fault stops the run instead of hanging it;
  * a FREE-RUNNING fault prints NOTHING at default verbosity: probe_20261020/explore2_FIX.out section (b) took eight
    population-1 faults (r1 = 8) with 0 `[ vme:' lines, 0 memory_rw failure lines and 0 `exception DATA_ACCESS'
    lines in the continue text, while the stepped counterpart (b') printed eight of each (instrument preserved as
    explore2.py.txt beside it) -- the measured basis of `p1 quiet''s want of 0;
  * DMA0 is the WORD address (`dma[0] = addr & ~3'); DMT0 = VALID | DAS 0x4000 | byte enables << 2, plus
    DREG << 7 on a load or WRITE 0x2 on a store.  The eight DMT0 wants were PREDICTED from that code before the
    first run (probe_20261020/dmt0_predictions.txt) and that run (probe_20261020/trial2_FIX568.out) MEASURED all
    eight as predicted -- 0x4000 | (dreg << 7) | 0x3d for a word load (0x423d r4, 0x433d r6), 0x403f for a word
    store, 0x4211 for a byte at addr & 3 == 1, 0x420d for a halfword at addr & 2 == 2.

ENCODINGS are hand-assembled (decoder op26: ld.hu 0x02, ld.bu 0x03, ld.d 0x04, ld 0x05, st.d 0x08, st 0x09,
st.h 0x0a, st.b 0x0b, or 0x16, addu 0x18, br 0x30 with d26 = 0, rte 0xf400fc00).  EVERY placed word is re-read
with `unassemble' and compared word / mnemonic / operands against an independent expectation (row `unasm',
count pinned by a LITERAL).  Every session that touches the device reads VBR (0x88) and checks DEVINIT's seed
0x67000000: most open with `ld r30,r3,0x88' and their rows report `nodev r30=...: device signature absent, check
not made' otherwise; the control session reads VBR into r5 after an `or' (row `vbr reset'), and the cased census
reads it into r13.  A wrong base-register field would read RAM zeros, which the zero-expecting rows would otherwise
accept.

ROWS, each with the mutant it is DESIGNED to catch and the channel that differs under it.  The rev-2 descriptions
are DATED PREDICTIONS (2026-10-20); tables 1 and 1b measured them on the 34-row rev 2 and table 2 measures rev 3.
  CONTROL rows -- DEFINITION: a row whose role is a PREREQUISITE of the scored rows -- an apparatus, medium or
  device-signature proof.  It need not be product-independent: `vbr reset' and `free neg ctl' also depend on product
  behaviour (an edit to DEVINIT's VBR seed reds `vbr reset'), so CONTROL=FAIL means a prerequisite failed and claims
  NO cause.  (This said "a row a product edit can red is scored, never CONTROL", which those two rows contradict;
  corrected on the repair-diff pass.)
    neg apparatus  a bogus subtype: the liveness oracle MUST go red (it is failable)
    session / live the control session runs to `quit'; an or-immediate reads back
    vbr reset      DEVICE SIGNATURE: DEVINIT's VBR seed (RAM or a device-less build answers 0)
    free neg ctl   GCSRCTL's debug() line: PRESENT in the stepped cased census, ABSENT in the free run -- the
                   run was free at verbose 0, so the fatal-vs-debug channel of the announce rows can vary
    unasm          every placed word re-read by the disassembler
  cased rows (scored: product edits red them -- M_DROPTCTL, M_DROPIRQEN and M_T1CMPWRDROP in tables 1 and 1b)
    t1cmp rt       cased T1CMP stores and reads back (and is the null medium's second discriminator)
    cased census   one ld at each of the ten cased offsets, ONE session, sentinel-seeded, PC + liveness after:
                   a cased label dropped FAULTs that offset and every later load keeps its sentinel
    free ctl       FREE-RUNNING T1CMP round trip to a breakpoint
    free quiet     ...that run prints NO vme text at all (a cased access never announces)
    tctl rt        TCTL stores a word and reads it back
    vbr rt         VBR stores a word and reads it back, then is restored to the seed and read back again
    t1count inc    T1COUNT stores a word; two reads give it and it + 100 (the read arm's `+= 100')
    cased wr       a word store to each of the six NON-storing cased arms (0x00, GCSRCTL, TCR, IRQEN, IRQL3,
                   IRQL4): no fault, PC + liveness after
    (`tctl rt', `vbr rt' and `t1count inc' share ONE stepped session: a fault at its first store reds all three --
    table 1's M_DROPTCTL -- so two of those reds are DEPENDENT, not own-channel kills.)
  population 2 (decline)
    p2 rd census   26 ld: all 0, no fault, PC + liveness after; a label dropped FAULTs (HEAD: the host dies)
    p2 wr census   26 st of 0xa5a5a5a5, a liveness or (checked: a FAULTING store stops it), then the 26 ld:
                   all 0.  A decline that STORES reads back non-zero -- visible because the fix does NOT force
                   odata = 0; a decline conditioned on direction FAULTs
    p2 ld widths   ld.bu + ld.hu at 0x28, ld.d at 0x08 (BOTH r6 and r7): 0, no fault -- a decline conditioned
                   on len FAULTs one of them
    p2 st widths   st.b + st.h at 0x28, st.d at 0x08, a liveness or, then read 0x28, 0x08, 0x0c back: all 0
  announce (FREE-RUNNING; full tail literals; every offset exactly once)
    p2 ann rd      each of the 26 READ then immediately WRITTEN: exactly 26 read-form lines, 0 write-form
    p2 ann rd 2    the same pairs again in the same session: 0 lines, PC at the breakpoint, liveness proof
    p2 ann wr      each WRITTEN then immediately READ: exactly 26 write-form lines `(len 4): 0xa5a5a5a5'
    p2 ann wr 2    the same pairs again: 0 lines, PC at the breakpoint, liveness proof
                   -- together 26 labels x {read, write} x {latch clear, set}.  Rev 2's dated predictions, and what
                   table 1 MEASURED for each: read- or write-branch fatal -> debug (0 lines: M_RDEBUG, M_WDEBUG), a
                   shared latch (1 line: M_LATCHONE), a never-set latch (52 lines: M_LATCHNOSET), a latch cleared
                   by a write (pass 2 re-announces, 26 lines: M_LATCHCLRW and M_LATCHCLRW_POST), a dropped `(once)'
                   (no exact match: M_NOONCE).  NEVER BUILT: a per-direction latch (52), a latch set at one
                   constant bit (51).
    p2 nw rd       pass 1, FIRST access to three untouched registers by ld.bu / ld.hu / ld.d: `(len 1)',
                   `(len 2)', `(len 8) -- served 0x0.' -- an announce that fires only for 4-byte accesses gives 0
    p2 nw wr       pass 1, FIRST access by st.b / st.h / st.d: `(len 1): 0xd4', `(len 2): 0xc3d4',
                   `(len 8): 0x1122334455667788' -- a 32-bit truncation of the 64-bit value fails the match
    p2 nw rd 2     NEW.  Pass 2 IN THE SAME PROCESS (a new gxemul memsets the latch, so a separate process would be
                   green): the three non-word reads again -> 0 read-form lines.  Kills M_LATCHLEN4 (the latch SET
                   conditioned on len == 4: non-word accesses announce but never latch, so pass 2 re-announces 3).
                   A zero is accepted only from a pass that reached its breakpoint with its liveness proof, and only
                   when pass 1 announced reads at all (`pass 1 silent' otherwise)
    p2 nw wr 2     NEW.  The same for the three non-word stores -> 0 write-form lines (M_LATCHLEN4: 3)
    p2 zero wr     NEW.  Its OWN free-running session (inside the announce pair it would change a 26-count literal):
                   `st r0,r3,0x30' -- a ZERO-valued first store to an untouched register (DMACTL); nothing is
                   seeded into r0 (the m88k core stops the CPU when r0 holds a non-zero value).  Wants the exact
                   WRITE-FORM literal `(len 4): 0x0 -- declined.' and one `[ vme:' line.  Kills M_IDATA (the
                   direction test swapped for `if (idata)': a zero store takes the READ form).  A count of `[ vme:'
                   lines alone would accept the read-form line, so the literal is the oracle.  One width is enough:
                   the swapped test reads idata's zero-ness and the body tests nothing on len
  population 1 (fault)
    p1 fault lo / hi / mid   ld at 0x90 / 0xffc / 0x94: PC 0x18, DMA0, DMT0 (word load into r4), host alive;
                   `return 0' -> `break' serves the read (PC advances); exit(1) reinstated kills the host
    p1 fault wr    st at 0x90: PC 0x18, DMA0, DMT0 (the word-store form)
    p1 p2 edge     ld 0x8c declines (0), then ld 0x90 faults: the label set's last member dropped faults at
                   0x8c instead; a label added AT 0x90 declines it
    p1 census      FREE-RUNNING: all 988 population-1 word starts, faults counted: a label added at ANY of them
                   gives 987; `return 0' -> `break' gives 0
    p1 widths      FREE-RUNNING: ld.bu 0x93, ld.hu 0x96, ld.d 0x98, st.b 0x9d, st.h 0xa2, st.d 0xa8, and NEW the
                   two LANE-0 accesses ld.hu 0xb0 (into r8, sentinel-seeded) and st.b 0xb4 -- eight faults: a FAULT
                   narrowed to word accesses (or to one direction) declines some of them; `if (len == 2 &&
                   (relative_addr & 3) == 0) break;' (M_LANE0H) declines the ld.hu (seven faults, r8 loses its
                   sentinel) and its `len == 1' twin (M_LANE0B) the st.b (seven faults) -- two legs, two accesses
    p1 quiet       NEW.  `[ vme:' lines in the continue text of the free-running p1 census run AND the p1 widths
                   run, each wanting 0: `default:''s debug() is silent free-running and fatal() is not, so a
                   debug -> fatal PROMOTION prints -- read side (M_DFATAL) 988 census lines, write side
                   (M_DFATALW) four widths lines (the census stores nothing).  Free-running at verbose 0 is what
                   lets it vary: in a stepped session it would be red on the fix itself
  interims -- NAMED channels of `vmewidthlanes': that round reds these and re-derives them
    p3 interim     ld.bu 0x51 (inside cased T1CMP): fault, DMA0 0xfff40050 -- also `if (len != 4) break;' in
                   `default:' (Fable) declines it
    p2 int byte    ld.bu 0x29 (inside population-2 MASTERCTL): fault, DMA0 0xfff40028
    p2 int half    ld.hu 0x2a (inside MASTERCTL): fault, DMA0 0xfff40028

CONTRACT (clause e).  DESIGNED to catch: the mutants named above, by the channels named above; tables 1, 1b and 2
measure which.  PREMISE, stated because two designs rest on it: the decline-and-announce arm and `p1 quiet''s
channel need fatal() to PRINT AND RETURN -- it does not exit (src/core/debugmsg.c) -- and the green tables are that
premise's measurement.  NOT CLAIMED, so a later escape is outside the contract rather than an argument:
  * populations 3 and 4 and population-2 sub-word starts beyond the three interim pins (one byte at 0x51, one
    byte at 0x29, one halfword at 0x2a);
  * population 4 -- a cased base at len != 4 -- is SERVICED by its cased arm with the `vmewidthlanes' lane defect;
    it does NOT fault;
  * ld.d / st.d at the cased bases 0x00, 0x60 and 0x88, whose second word is a population-2 register (0x04,
    0x64, 0x8c): the device sees ONE access to the cased label;
  * cased-word ld.d / st.d lane placement (population 4: a 32-bit register served into, or stored from, the
    wrong half of an 8-byte access);
  * word-aligned narrow and double accesses at the population-2 registers no non-word row touches;
  * population-2 non-word offsets and cross-width latch reuse are SAMPLED, not exhausted -- the zero store is one
    width (len 4), the non-word rows one register per width;
  * store DATA is SAMPLED: the arm's body prints idata and tests no bit or value of it, so an exemption keyed on
    store data is clause (e).  The five population-2 store values are 0x0, 0xa5a5a5a5, 0xd4, 0xc3d4 and
    0x1122334455667788; the UNTESTED slice is the bits clear in all five -- 1, 11, 19, 20, 25, 27 of the low word and
    22 of the high (28 of 64) -- and `idata == k' for any unsampled k.  MEASURED for bit 1 on the direction test
    (`&& !(idata & 2)', 38/38: killtable2_20261021/table2b/); the other bits, the same exemptions on the latch test
    or set, and the unsampled values are DERIVED alike.  The SAMPLED zero pins the announce's FORM, not the latch
    SET: a set skipped for a zero store survives, MEASURED 38/38 (table2d/ M_ZEROSET; no session touches the
    zero-stored register twice).  NOT in the slice: `default:''s refusal conditioned on idata (both polarities
    killed, table2c/: 29/38 and 36/38); and an odata conjunct is EQUIVALENT, not sampled -- odata is 0 on every
    write and every population-2 word is 0: on the direction test the leg compiles to the fix's own binary
    (table2c/), on the latch set it scores 38/38 (table2d/ M_SETODATA);
  * EQUIVALENT by construction, not built: the latch literal `1ULL' -> `2ULL', the index `(relative_addr >> 2) ^ 1'
    in both the test and the set, and `|=' -> `^=' under the clear-bit guard -- each keeps one private bit per
    register;
  * the fault rows pin `return 0', DMA0 and DMT0, NOT the text of `default:''s two debug() lines;
  * DELETION of `default:''s two debug() calls: `p1 quiet' wants 0 lines and a deleted call also prints 0 -- the
    row sees a debug -> fatal promotion, never a deletion;
  * `default:''s write debug prints `(int)idata', a pre-existing truncation in host-debug text;
  * the typedef's compile-time guard: its negative control (the field narrowed) is a failed BUILD, recorded in the
    kill table -- a neutered typedef has no runtime row;
  * an unsampled population-1 interior added as a label (`case 0x91:');
  * NO_EXCEPTIONS callers -- the debugger's put/dump/unassemble never reach the handler (silent zero fill);
  * instruction fetch from the window (a population-1 fetch takes vector 2 and halts; a population-2 fetch
    declines);
  * xmem (declines twice at population 2 -- the store silently; its load faults at population 1);
  * per-instance latch isolation: mvme187 attaches ONE vme device per process;
  * the guest's abort-handler path (IRQSTAT, IRQCLR): vme2abort() is the ABORT-switch interrupt handler and this
    model raises no VME2 interrupt;
  * population-1 accesses other than the 988 word loads, the four stepped faults and the eight width faults -- so
    `default:''s refusal narrowed to exempt an undriven interior (`relative_addr != 0x91'; 0xffd..0xfff, MEASURED
    38/38 as table2d/ M_DFLTFFC) or an unrowed lane-0 cell (a len-1 load or a len-2 store at a word start) passes
    38/38;
  * a served value other than 0 in the read announce (no population-2 word is ever non-zero);
  * anything about the real VMEchip2 (its register chapter is not on disk).
DESIGN NOTE: a sub-word start inside a population-2 word maps onto that register's own latch bit (0x29 >> 2 == 10
== MASTERCTL's), so if `vmewidthlanes' later services such starts through the arm, one latch per register still
holds.
ORDER DEPENDENCE: a latch shift that loses its 64-bit literal (`1ULL' -> `1u') is undefined behaviour at MISC's bit
35, so what it does is the compiler's choice.  This paragraph said "on this x86-64 build it lands on bit 3,
SLAVELMOD2's (0x0c) ... so MISC's announce is silenced"; that was PRETABLE2's prediction, and kill table 2 measured
the alternative PRETABLE2 named instead: GCC 15.2.1 -O3 specialised the MISC case and folded the shift to 0, so
MISC never latches -- 27 lines in pass 1 and 2 in pass 2, red `p2 ann rd', `p2 ann wr' and both `2' rows
(killtable2_20261021/obj/M_ONENARROW_codegen.txt).  The masked-count shape was not built: there MISC and SLAVELMOD2
(0x0c) would share bit 3, so whichever of the two POP2 reaches second stays silent -- 25 lines in pass 1 in any
order; a reorder changes which register is silenced, not the kill.  No portable claim.

TEST-FIRST SHAPE: on the committed HEAD every session touching population 1 or 2 ends the host (exit 1); the
controls and the cased rows stay green.

Sentinel: VME_DEFAULT_PROBE_DONE (plus VME_DEFAULT_RESULT=n/N, VME_DEFAULT_CONTROL=OK|FAIL)
"""

import os
import pty
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: vme_default_probe.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
#  A private dummy file: a shared /tmp path once let two concurrent runs race on it.
_TMPDIR = tempfile.mkdtemp(prefix="vme_default_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
with open(DUMMY, "wb") as _f:
    _f.write(b"\x00\x00\x00\x00")

VME = 0xfff40000            # VME2_BASE (mvme88k_vme.h)
CODE = 0x00010000
CODE2 = 0x00010200          # the second pass of a two-pass free-running session
CENSUS = 0x00020000         # the population-1 census program
VEC_DACC = 0x18             # VBR 0 + 8 * M88K_EXCEPTION_DATA_ACCESS (3)
VEC_MISAL = 0x20            # VBR 0 + 8 * M88K_EXCEPTION_MISALIGNED_ACCESS (4)
SENT = 0xdeadbeef
WVAL = 0xa5a5a5a5
T1VAL = 0x12345678
TCTLVAL = 0x13572468
VBRVAL = 0x89abcdef
T1CVAL = 0x00001000
NARROW = 0xa1b2c3d4         # st.b / st.h source: distinct bytes, so a lane mix-up is visible
DHI, DLO = 0x11223344, 0x55667788   # st.d source pair: HIGH word != low word, so a 32-bit truncation shows
VBR_SEED = 0x67000000       # DEVINIT: VME2_SET_VBR0(6) + VME2_SET_VBR1(7) = 6 << 28 | 7 << 24
LIVE = 0x1234
LIVE2 = 0x5678              # the second-pass liveness proof
STLIVE = 0x5a5a             # the after-the-stores liveness proof
T1COUNT_STEP = 100          # the T1COUNT read arm's `+= 100' (after the preload has served)
ZERO_OFF = 0x30             # `p2 zero wr': DMACTL -- its own session; not MISC (0x8c) and not SLAVELMOD2 (0x0c),
                            # the pair a 32-bit latch shift could collide (undefined; see ORDER DEPENDENCE), and no
                            # non-census session touches it
LANE0_HU = 0xb0             # `p1 widths': a word-aligned (lane-0) halfword start no other access there uses
LANE0_B = 0xb4              # ...and a word-aligned byte start

CASED = (0x00, 0x2c, 0x4c, 0x50, 0x54, 0x60, 0x6c, 0x80, 0x84, 0x88)
POP2 = ((0x04, "SADDR2"), (0x08, "SLAVELMOD1"), (0x0c, "SLAVELMOD2"), (0x10, "SLAVECTL"),
        (0x14, "MASTER1"), (0x18, "MASTER2"), (0x1c, "MASTER3"), (0x20, "MASTER4"),
        (0x24, "MASTER4MOD"), (0x28, "MASTERCTL"), (0x30, "DMACTL"), (0x34, "DMAMODE"),
        (0x38, "DMALADDR"), (0x3c, "DMAVMEADDR"), (0x40, "DMACOUNT"), (0x44, "DMATABLE"),
        (0x48, "DMASTAT"), (0x58, "T2CMP"), (0x5c, "T2COUNT"), (0x64, "PRESCALE"),
        (0x68, "IRQSTAT"), (0x70, "SETSOFTIRQ"), (0x74, "IRQCLR"), (0x78, "IRQL1"),
        (0x7c, "IRQL2"), (0x8c, "MISC"))
POP2_OFFS = tuple(o for o, _ in POP2)
POP1 = tuple(range(0x90, 0x1000, 4))
#  The header's register block is 36 CONTIGUOUS words, 0x00..0x8c: cased + population 2 must tile it exactly.
assert len(CASED) == 10 and len(POP2) == 26 and len(POP1) == 988
assert sorted(CASED + POP2_OFFS) == list(range(0, 0x90, 4))

#  DMT0 PREDICTIONS (written before the first run, from cpu_m88k_instr_loadstore.c: VALID 0x1, DAS 0x4000,
#  byte enables << 2 -- word 0xf, byte 1 << (3 - (addr & 3)), half 3 << (2 - (addr & 2)) -- and DREG << 7 on a
#  load or WRITE 0x2 on a store).  The rows pin what the measurement says.
def dmt_load(dreg, en):
    return 0x1 | 0x4000 | (dreg << 7) | (en << 2)


DMT_ST_WORD = 0x1 | 0x2 | 0x4000 | (0xf << 2)          # 0x403f
DMT_LD_WORD_R4 = dmt_load(4, 0xf)                      # 0x423d
DMT_LD_WORD_R6 = dmt_load(6, 0xf)                      # 0x433d
DMT_LD_BYTE1_R4 = dmt_load(4, 1 << (3 - 1))            # 0x4211  (a byte at addr & 3 == 1)
DMT_LD_HALF2_R4 = dmt_load(4, 3 << (2 - 2))            # 0x420d  (a halfword at addr & 2 == 2)

PROMPT = "GXemul> "
RD_LINE = "[ vme: unimplemented read from register 0x%x (len %d) -- served 0x%x.  (once) ]"
WR_LINE = "[ vme: unimplemented write to register 0x%x (len %d): 0x%x -- declined.  (once) ]"
GCS_LINE = "[ vme: unimplemented GCSRCTL ]"
VMETXT = "[ vme:"


# ------------------------------------------------------------------- encodings
class Ins(object):
    __slots__ = ("word", "mnem", "ops")

    def __init__(self, word, mnem, ops):
        self.word, self.mnem, self.ops = word, mnem, ops


def enc(op26, rd, rs1, imm):
    assert 0 <= op26 < 64 and 0 <= rd < 32 and 0 <= rs1 < 32 and 0 <= imm <= 0xffff
    return (op26 << 26) | (rd << 21) | (rs1 << 16) | imm


def _mem(op26, mnem, rd, off, rs1=3):
    return Ins(enc(op26, rd, rs1, off), mnem, "r%d,r%d,0x%x" % (rd, rs1, off))


def LD(rd, off):
    return _mem(0x05, "ld", rd, off)


def LD_BU(rd, off):
    return _mem(0x03, "ld.bu", rd, off)


def LD_HU(rd, off):
    return _mem(0x02, "ld.hu", rd, off)


def LD_D(rd, off):
    assert rd != 31 and off % 8 == 0
    return _mem(0x04, "ld.d", rd, off)


def ST(rs, off):
    return _mem(0x09, "st", rs, off)


def ST_B(rs, off):
    return _mem(0x0b, "st.b", rs, off)


def ST_H(rs, off):
    assert off % 2 == 0
    return _mem(0x0a, "st.h", rs, off)


def ST_D(rs, off):
    assert rs != 31 and off % 8 == 0
    return _mem(0x08, "st.d", rs, off)


def OR_I(rd, rs1, imm):
    assert rd != 0
    return Ins(enc(0x16, rd, rs1, imm), "or", "r%d,r%d,0x%x" % (rd, rs1, imm))


def ADDU_I(rd, rs1, imm):
    #  the disassembler prints this immediate in DECIMAL (cpu_m88k.c: "%s\tr%i,r%i,%i")
    return Ins(enc(0x18, rd, rs1, imm), "addu", "r%d,r%d,%d" % (rd, rs1, imm))


def RTE():
    return Ins(0xf400fc00, "rte", "")


def BR_SELF():
    #  op26 0x30, d26 = 0: the target is the branch itself; the operand is filled in on placement
    return Ins(0xc0000000, "br", None)


def VSIG():
    return LD(30, 0x88)          # every device session's opening VBR read


GUARD = (VEC_DACC, [BR_SELF()])
HANDLER = (VEC_DACC, [ADDU_I(1, 1, 1), RTE()])


# ------------------------------------------------------------------- sessions
def hx(v):
    return "absent" if v is None else "0x%x" % v


def argv_for(subtype):
    return [BIN, "-V", "-x", "-E", "mvme88k", "-e", subtype, "-M", "64",
            "0x%x:%s" % (CODE, DUMMY)]


def seeds(pairs):
    return ["r%d=0x%x" % (r, v) for r, v in pairs]


def place(blocks):
    """blocks: [(addr, [Ins])] -> (debugger commands, [(addr, Ins)]).  Every block is re-read with
       `unassemble' (end-exclusive) right after it is written."""
    cmds, placed = [], []
    for at, insns in blocks:
        for i, ins in enumerate(insns):
            a = at + 4 * i
            if ins.ops is None:
                ins = Ins(ins.word, ins.mnem, "0x%08x" % a)
            cmds.append("put w 0x%x, 0x%08x" % (a, ins.word))
            placed.append((a, ins))
        cmds.append("unassemble 0x%x 0x%x" % (at, at + 4 * len(insns)))
    return cmds, placed


def run_piped(cmds, subtype="mvme187", timeout=90):
    inp = ("\n".join(list(cmds) + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv_for(subtype), input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return (e.output or b"").decode("latin-1", "replace").replace("\r", ""), "TIMEOUT"
    rc = p.returncode
    return (p.stdout.decode("latin-1", "replace").replace("\r", ""),
            ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc))


def run_pty(cmds, t_cmd=10.0, t_run=30.0):
    """One command at a time through a pty.  An ordinary command waits for the next prompt; `continue' waits
       for BREAKPOINT and then a prompt after it, and nothing is sent while the guest runs.  -> (transcript,
       how); how is exitN / sigN, or no-prompt / no-breakpoint (the child is then killed: a guest still running
       would never read `quit')."""
    pid, fd = pty.fork()
    if pid == 0:
        try:
            os.execv(BIN, argv_for("mvme187"))
        finally:
            os._exit(127)
    buf = [""]

    def pump(deadline, pred):
        while True:
            if pred():
                return "ok"
            left = deadline - time.time()
            if left <= 0:
                return "timeout"
            r, _, _ = select.select([fd], [], [], min(left, 0.05))
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return "eof"
            if not d:
                return "eof"
            buf[0] += d.decode("latin-1", "replace")

    state = pump(time.time() + 20.0, lambda: PROMPT in buf[0])
    failed = None if state == "ok" else ("no-prompt" if state == "timeout" else None)
    if state == "ok":
        for c in cmds:
            start = len(buf[0])
            try:
                os.write(fd, (c + "\n").encode("latin-1"))
            except OSError:
                state = "eof"
                break
            if c == "continue":
                def pred(start=start):
                    b = buf[0].find("BREAKPOINT", start)
                    return b >= 0 and buf[0].find(PROMPT, b) >= 0
                state = pump(time.time() + t_run, pred)
                if state == "timeout":
                    failed = "no-breakpoint"
            else:
                state = pump(time.time() + t_cmd,
                             lambda start=start: buf[0].find(PROMPT, start) >= 0)
                if state == "timeout":
                    failed = "no-prompt"
            if state != "ok":
                break
    if state == "ok":
        try:
            os.write(fd, b"quit\n")
        except OSError:
            pass
        pump(time.time() + 5.0, lambda: False)
    try:
        os.close(fd)
    except OSError:
        pass
    stat, reaped = None, False
    for attempt in range(2):
        for _ in range(40):
            try:
                p, s = os.waitpid(pid, os.WNOHANG)
            except OSError:
                p, s = pid, None
            if p:
                stat, reaped = s, True
                break
            time.sleep(0.05)
        if reaped:
            break
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        failed = failed or "killed"
    if failed:
        how = failed
    elif stat is None:
        how = "unreaped"
    elif os.WIFSIGNALED(stat):
        how = "sig%d" % os.WTERMSIG(stat)
    else:
        how = "exit%d" % os.WEXITSTATUS(stat)
    return buf[0].replace("\r", ""), how


DIS_RE = re.compile(r"^[su]([0-9a-f]{8}): ([0-9a-f]{8})\s+(?:<-\s+)?(\S+)(?:\t(\S+))?[ \t]*$", re.M)
GPR_RE = re.compile(r"\br(\d+)\s*=\s*(0x[0-9a-fA-F]+)")
PC_RE = re.compile(r"cpu\d+:\s+pc\s+=\s+(0x[0-9a-fA-F]+)")
CR_RE = re.compile(r"\b([A-Z][A-Z0-9]*)=(0x[0-9a-fA-F]+)")


class Res(object):
    pass


def analyse(text, how, placed):
    """Split the transcript at the prompts; parse every unassemble, every reg dump (in order), the last
       `reg 0,0', and the text of every `continue'."""
    r = Res()
    r.how, r.text, r.placed = how, text, placed
    r.dis, r.dumps, r.cr, r.conts = {}, [], None, []
    for part in text.split(PROMPT)[1:]:
        cmd, _, out = part.partition("\n")
        cmd = cmd.strip()
        if cmd.startswith("unassemble"):
            for m in DIS_RE.finditer(out):
                r.dis[int(m.group(1), 16)] = (int(m.group(2), 16), m.group(3), m.group(4) or "")
        elif cmd == "reg":
            m = PC_RE.search(out)
            if m:
                r.dumps.append(({int(g.group(1)): int(g.group(2), 16)
                                 for g in GPR_RE.finditer(out)}, int(m.group(1), 16)))
        elif cmd == "reg 0,0":
            cr = {g.group(1): int(g.group(2), 16) for g in CR_RE.finditer(out)}
            if cr:
                r.cr = cr
        elif cmd == "continue":
            r.conts.append(out)
    r.regs, r.pc = r.dumps[-1] if r.dumps else (None, None)
    return r


UNASM = {"ok": 0, "n": 0, "bad": []}


def check_unasm(r, scored=True):
    ok = n = 0
    for a, ins in r.placed:
        n += 1
        d = r.dis.get(a)
        if d is not None and d == (ins.word, ins.mnem, ins.ops):
            ok += 1
        elif scored:
            UNASM["bad"].append("0x%x:%08x %s %s -> %r" % (a, ins.word, ins.mnem, ins.ops, d))
    if scored:
        UNASM["ok"] += ok
        UNASM["n"] += n
    return ok, n


def stepped(blocks, regs, nsteps, cr=False, scored=True):
    cmds, placed = place(blocks)
    cmds = seeds([(3, VME)] + regs) + cmds + ["pc=0x%x" % CODE, "step %d" % nsteps, "reg"]
    if cr:
        cmds.append("reg 0,0")
    t, how = run_piped(cmds)
    r = analyse(t, how, placed)
    check_unasm(r, scored)
    return r


def freerun(blocks, regs, bps, runs):
    """runs: [start pc] -- each is `pc=<start>', `continue', `reg'.  All code, every unassemble and every
       breakpoint go in BEFORE the first `continue', so the disassembly cross-check never depends on surviving
       a run."""
    cmds, placed = place(blocks)
    cmds = seeds([(3, VME)] + regs) + cmds + ["breakpoint add 0x%x" % b for b in bps]
    for start in runs:
        cmds += ["pc=0x%x" % start, "continue", "reg"]
    t, how = run_pty(cmds)
    r = analyse(t, how, placed)
    check_unasm(r)
    return r


#  A TIMEOUT is named as one, distinctly from a process death (`died:exit1') and from an assertion mismatch, so a
#  load-induced red is never read as a product kill (rev 3; GLM, F2).  run_pty reports no-prompt / no-breakpoint,
#  run_piped TIMEOUT.
TIMEOUTS = ("no-prompt", "no-breakpoint", "TIMEOUT")


def died(r):
    return ("timeout:%s" if r.how in TIMEOUTS else "died:%s") % r.how


def reg(r, n):
    if r.regs is None:
        return died(r) if r.how != "exit0" else "absent"
    return hx(r.regs.get(n))


def devsig_bad(r):
    """None when the session's opening VBR read saw the device; else the reason."""
    if r.regs is None:
        return died(r)
    if r.regs.get(30) != VBR_SEED:
        return NODEV % hx(r.regs.get(30))
    return None


#  Cause-free stop wording (rev 3; AX's F9 text, refined per site by grok): each row stays RED, and none claims to
#  know whether the stop is the mutation under test.
NODEV = "nodev r30=%s: device signature absent, check not made"
STOPPED = "unexpected stop pc=%s before the row's check"
NOT_EXERCISED = "dependent check not exercised: pass 1 did not complete"
SILENT = "pass 1 silent"


def end_of(prog, at=CODE):
    return at + 4 * (len(prog) - 1)


def tail(r, pc_want, live_reg=31, live_want=LIVE):
    """'' when the stepped run ended at the program's br with its liveness register set; else a suffix."""
    s = ""
    if r.pc != pc_want:
        s += " pc=%s" % hx(r.pc)
    if r.regs.get(live_reg) != live_want:
        s += " r%d=%s" % (live_reg, hx(r.regs.get(live_reg)))
    return s


def lines(seg):
    return [ln.rstrip() for ln in seg.split("\n")]


rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 15, name     # `%-16s ' keeps a gate's `^$v  .*ok$' satisfiable
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-34s %-34s %-60s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    sys.stdout.flush()
    return ok


print("vmedefaultkill RUNG-3 DETECTOR (revision 3, fix568b) -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E mvme88k -e mvme187 -M 64 (UNMODIFIED); vme at 0x%08x" % VME)
t0 = time.time()

# ================================================================ INFO (unscored)
#  Measured so the panel has the number; NOT a row -- no want, no score, no pin.  (LD_D refuses a 4-mod-8
#  offset, so this one word is built by hand.)
cmds, placed = place([(VEC_MISAL, [BR_SELF()]), (CODE, [VSIG(), Ins(enc(0x04, 4, 3, 0x0c), "ld.d", "r4,r3,0xc"),
                                                        OR_I(6, 0, LIVE), BR_SELF()])])
t, how = run_piped(seeds([(3, VME), (4, SENT), (5, SENT), (6, SENT), (30, SENT)]) + cmds
                   + ["pc=0x%x" % CODE, "step 3", "reg"])
ri = analyse(t, how, placed)
print("INFO ld.d 4mod8  ld.d at 0x0c (4 mod 8): how=%s pc=%s r4=%s r5=%s r6=%s vme-text=%d unasm=%d/%d"
      % (ri.how, hx(ri.pc), reg(ri, 4), reg(ri, 5), reg(ri, 6), ri.text.count(VMETXT),
         *check_unasm(ri, scored=False)))

print("%-16s %-34s %-34s %-60s %s" % ("row", "got", "want", "note", ""))

# ================================================================ apparatus
#  APPARATUS NEGATIVE CONTROL: the liveness oracle must be able to go red.
cmds, _ = place([(CODE, [OR_I(4, 0, LIVE), BR_SELF()])])
t, how = run_piped(seeds([(4, SENT)]) + cmds + ["pc=0x%x" % CODE, "step 1", "reg"], subtype="187")
rn = analyse(t, how, [])
row("neg apparatus", "%s/%s" % (how, hx(rn.regs.get(4)) if rn.regs else "absent"), "exit1/absent",
    "bogus subtype `187' -> no machine -> `live' MUST fail")

prog = [OR_I(4, 0, LIVE), LD(5, 0x88), ST(2, 0x50), LD(6, 0x50), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(2, T1VAL), (4, SENT), (5, SENT), (6, SENT)], 4)
row("session", r.how, "exit0", "the control session ran to `quit'")
row("live", reg(r, 4), hx(LIVE), "or r4,r0,0x1234 -- the guest executes, readback works")
row("vbr reset", reg(r, 5), hx(VBR_SEED), "DEVICE SIGNATURE: DEVINIT's VBR seed; RAM or no device reads 0")
row("t1cmp rt", reg(r, 6), hx(T1VAL), "a word stored to CASED T1CMP reads back")

#  CASED CENSUS: one load per cased offset, ONE session, sentinel-seeded, then liveness.  Stepped, so the GCSRCTL
#  load's debug() line PRINTS here -- the positive half of `free neg ctl'.
CC = [(4, 0x00), (5, 0x2c), (6, 0x4c), (7, 0x50), (8, 0x54), (9, 0x60), (10, 0x6c), (11, 0x80), (12, 0x84),
      (13, 0x88)]
CC_WANT = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: VBR_SEED, 15: LIVE}
prog = [LD(rr, o) for rr, o in CC] + [OR_I(15, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(rr, SENT) for rr in CC_WANT], len(prog) - 1)
gcs_stepped = lines(r.text).count(GCS_LINE)
if r.regs is None:
    got = died(r)
else:
    got = "%d/%d" % (sum(1 for rr, v in CC_WANT.items() if r.regs.get(rr) == v), len(CC_WANT))
    if r.pc != end_of(prog):
        got += " pc=%s" % hx(r.pc)
row("cased census", got, "11/11", "ten cased offsets read (VBR 0x67000000, the rest 0) + liveness")

#  FREE-RUNNING SHAPE CONTROL: T1CMP round trip and a GCSRCTL read, to a breakpoint.
prog = [VSIG(), ST(2, 0x50), LD(5, 0x50), LD(8, 0x2c), OR_I(7, 0, LIVE), BR_SELF()]
bp = end_of(prog)
r = freerun([GUARD, (CODE, prog)], [(2, T1VAL), (5, SENT), (7, SENT), (8, SENT), (30, SENT)],
            [bp, VEC_DACC], [CODE])
if r.regs is None or not r.conts:
    got_c = got_q = got_n = died(r)
elif r.pc != bp:
    got_c = got_q = got_n = STOPPED % hx(r.pc)
else:
    got_c = "%s/%s/%s" % (hx(r.regs.get(5)), hx(r.regs.get(30)), hx(r.regs.get(7)))
    got_q = r.conts[0].count(VMETXT)
    got_n = "%d/%d" % (gcs_stepped, lines(r.conts[0]).count(GCS_LINE))
row("free ctl", got_c, "%s/%s/%s" % (hx(T1VAL), hx(VBR_SEED), hx(LIVE)),
    "FREE-RUNNING to a breakpoint: T1CMP round trip, VBR, liveness")
row("free quiet", got_q, 0, "...and that run prints NO vme text at all")
row("free neg ctl", got_n, "1/0", "GCSRCTL's debug() line: 1 stepped (cased census), 0 free-running")

# ================================================================ cased accept side (write paths)
prog = [VSIG(), ST(2, 0x60), LD(4, 0x60), ST(7, 0x88), LD(5, 0x88), ST(11, 0x88), LD(12, 0x88),
        ST(8, 0x54), LD(9, 0x54), LD(10, 0x54), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)],
            [(2, TCTLVAL), (7, VBRVAL), (8, T1CVAL), (11, VBR_SEED), (4, SENT), (5, SENT), (9, SENT),
             (10, SENT), (12, SENT), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
if bad:
    g_t = g_v = g_c = bad
else:
    sfx = tail(r, end_of(prog))
    g_t = hx(r.regs.get(4)) + sfx
    g_v = "%s/%s" % (hx(r.regs.get(5)), hx(r.regs.get(12))) + sfx
    g_c = "%s/%s" % (hx(r.regs.get(9)), hx(r.regs.get(10))) + sfx
row("tctl rt", g_t, hx(TCTLVAL), "TCTL stores a word and reads it back")
row("vbr rt", g_v, "%s/%s" % (hx(VBRVAL), hx(VBR_SEED)), "VBR stores, reads back; restored to the seed, reads back")
row("t1count inc", g_c, "%s/%s" % (hx(T1CVAL), hx(T1CVAL + T1COUNT_STEP)),
    "T1COUNT stores; two reads give it, then it + 100")

prog = [VSIG()] + [ST(2, o) for o in (0x00, 0x2c, 0x4c, 0x6c, 0x80, 0x84)] + [OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
row("cased wr", bad if bad else "%s/%s" % (hx(r.pc), hx(r.regs.get(31))),
    "%s/%s" % (hx(end_of(prog)), hx(LIVE)), "a word store to 0x00/GCSRCTL/TCR/IRQEN/IRQL3/IRQL4: no fault")

# ================================================================ population 2 (decline)
REGS26 = list(range(4, 30))
prog = [VSIG()] + [LD(rr, o) for rr, o in zip(REGS26, POP2_OFFS)] + [OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26], len(prog) - 1)
bad = devsig_bad(r)
row("p2 rd census", bad if bad else "%d/26" % sum(1 for rr in REGS26 if r.regs.get(rr) == 0) + tail(r, end_of(prog)),
    "26/26", "26 ld, one per population-2 register: all 0, no fault, runs on")

prog = ([VSIG()] + [ST(2, o) for o in POP2_OFFS] + [OR_I(1, 0, STLIVE)]
        + [LD(rr, o) for rr, o in zip(REGS26, POP2_OFFS)] + [OR_I(31, 0, LIVE), BR_SELF()])
r = stepped([GUARD, (CODE, prog)], [(2, WVAL), (1, SENT), (30, SENT), (31, SENT)] + [(rr, SENT) for rr in REGS26],
            len(prog) - 1)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    got = "%d/26" % sum(1 for rr in REGS26 if r.regs.get(rr) == 0) + tail(r, end_of(prog))
    if r.regs.get(1) != STLIVE:
        got += " after-st r1=%s" % hx(r.regs.get(1))
row("p2 wr census", got, "26/26", "26 st 0xa5a5a5a5, liveness AFTER the stores, 26 ld: all 0")

prog = [VSIG(), LD_BU(4, 0x28), LD_HU(5, 0x28), LD_D(6, 0x08), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (7, SENT), (30, SENT), (31, SENT)],
            len(prog) - 1)
bad = devsig_bad(r)
row("p2 ld widths", bad if bad else "%d/4" % sum(1 for rr in (4, 5, 6, 7) if r.regs.get(rr) == 0)
    + tail(r, end_of(prog)), "4/4", "ld.bu + ld.hu at 0x28, ld.d at 0x08 (r6 AND r7): 0, no fault")

prog = [VSIG(), ST_B(12, 0x28), ST_H(12, 0x28), ST_D(10, 0x08), OR_I(1, 0, STLIVE),
        LD(4, 0x28), LD(5, 0x08), LD(6, 0x0c), OR_I(31, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(12, NARROW), (10, DHI), (11, DLO), (1, SENT), (4, SENT), (5, SENT),
                                    (6, SENT), (30, SENT), (31, SENT)], len(prog) - 1)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    got = "%d/3" % sum(1 for rr in (4, 5, 6) if r.regs.get(rr) == 0) + tail(r, end_of(prog))
    if r.regs.get(1) != STLIVE:
        got += " after-st r1=%s" % hx(r.regs.get(1))
row("p2 st widths", got, "3/3", "st.b + st.h at 0x28, st.d at 0x08: no fault; 0x28/0x08/0x0c read back 0")


# ================================================================ announce (free-running)
def announce_pair(rows_names, first, second, want_line, want_form):
    """Two passes in ONE free-running session.  Pass 1 and pass 2 each access every population-2 register twice
       in a row, `first' then `second'.  Pass 1 must print exactly the 26 `want_line' lines (one per offset, full
       literal) and no other vme text; pass 2 must print nothing, end at its breakpoint, and set its liveness."""
    def pairs():
        out = []
        for o in POP2_OFFS:
            out += [first(o), second(o)]
        return out
    pass1 = [VSIG()] + pairs() + [BR_SELF()]
    pass2 = pairs() + [OR_I(31, 0, LIVE2), BR_SELF()]
    bp1, bp2 = end_of(pass1), end_of(pass2, CODE2)
    r = freerun([GUARD, (CODE, pass1), (CODE2, pass2)], [(2, WVAL), (4, SENT), (30, SENT), (31, SENT)],
                [bp1, bp2, VEC_DACC], [CODE, CODE2])
    pcs = [pc for _, pc in r.dumps]
    n1, n2 = rows_names
    note1 = "pass 1: vme lines / exact %s lines / offsets exactly once" % want_form
    note2 = "pass 2, same pairs again: no vme text; breakpoint + r31=0x5678"
    if not pcs or not r.conts:
        row(n1, died(r), "26/26/26", note1)
        row(n2, NOT_EXERCISED, 0, note2)
        return
    bad = None
    if r.dumps[0][0].get(30) != VBR_SEED:
        bad = NODEV % hx(r.dumps[0][0].get(30))
    l1 = lines(r.conts[0])
    exact = [o for o in POP2_OFFS if l1.count(want_line(o)) == 1]
    nvme = r.conts[0].count(VMETXT)
    g1 = bad if bad else "%d/%d/%d" % (nvme, sum(l1.count(want_line(o)) for o in POP2_OFFS), len(exact))
    if pcs[0] != bp1 and not bad:
        g1 += " stopped pc=%s" % hx(pcs[0])
    row(n1, g1, "26/26/26", note1)
    #  pass 2's zero is accepted only from a pass that ran to its breakpoint with its liveness proof (Astra, F2),
    #  and only after pass 1 announced at all -- a silent pass 1 is reported as such (it IS the announce channel)
    if bad or pcs[0] != bp1:
        g2 = NOT_EXERCISED
    elif nvme == 0:
        g2 = SILENT
    elif len(pcs) < 2 or len(r.conts) < 2:
        g2 = "pass 2 %s" % died(r)
    elif pcs[1] != bp2 or r.dumps[1][0].get(31) != LIVE2:
        g2 = "%d stopped pc=%s r31=%s" % (r.conts[1].count(VMETXT), hx(pcs[1]), hx(r.dumps[1][0].get(31)))
    else:
        g2 = r.conts[1].count(VMETXT)
    row(n2, g2, 0, note2)


announce_pair(("p2 ann rd", "p2 ann rd 2"), lambda o: LD(4, o), lambda o: ST(2, o),
              lambda o: RD_LINE % (o, 4, 0), "read-form")
announce_pair(("p2 ann wr", "p2 ann wr 2"), lambda o: ST(2, o), lambda o: LD(4, o),
              lambda o: WR_LINE % (o, 4, WVAL), "write-form")

#  NON-WORD ACCESSES, free-running, TWO passes in ONE process (rev 3).  Pass 1 reaches each of six untouched registers
#  FIRST at its own width; pass 2 (CODE2, own breakpoint, LIVE2) repeats the same six accesses and must print nothing.
#  The second pass MUST share the process: a new gxemul memsets the latch, so a separate process would be green under
#  a latch SET conditioned on len == 4 (M_LATCHLEN4; grok, F2).
NW_RD = [(LD_BU(4, 0x04), RD_LINE % (0x04, 1, 0)), (LD_HU(5, 0x0c), RD_LINE % (0x0c, 2, 0)),
         (LD_D(6, 0x10), RD_LINE % (0x10, 8, 0))]
NW_WR = [(ST_B(12, 0x14), WR_LINE % (0x14, 1, NARROW & 0xff)),
         (ST_H(12, 0x1c), WR_LINE % (0x1c, 2, NARROW & 0xffff)),
         (ST_D(10, 0x20), WR_LINE % (0x20, 8, (DHI << 32) | DLO))]
RD_HEAD = "[ vme: unimplemented read from register"
WR_HEAD = "[ vme: unimplemented write to register"
nw1 = [VSIG()] + [i for i, _ in NW_RD + NW_WR] + [OR_I(31, 0, LIVE), BR_SELF()]
nw2 = [i for i, _ in NW_RD + NW_WR] + [OR_I(31, 0, LIVE2), BR_SELF()]
bp1, bp2 = end_of(nw1), end_of(nw2, CODE2)
r = freerun([GUARD, (CODE, nw1), (CODE2, nw2)], [(12, NARROW), (10, DHI), (11, DLO), (4, SENT), (5, SENT), (6, SENT),
                                                 (7, SENT), (30, SENT), (31, SENT)], [bp1, bp2, VEC_DACC], [CODE, CODE2])
pcs = [pc for _, pc in r.dumps]
if not pcs or not r.conts:
    bad = died(r)
elif r.dumps[0][0].get(30) != VBR_SEED:
    bad = NODEV % hx(r.dumps[0][0].get(30))
elif pcs[0] != bp1:
    bad = STOPPED % hx(pcs[0])
else:
    bad = None
if bad:
    g_r = g_w = bad
    g_r2 = g_w2 = NOT_EXERCISED
else:
    l = lines(r.conts[0])
    nrd = sum(1 for x in l if x.startswith(RD_HEAD))
    nwr = sum(1 for x in l if x.startswith(WR_HEAD))
    g_r = "%d/%d" % (sum(1 for _, w in NW_RD if l.count(w) == 1), nrd)
    g_w = "%d/%d" % (sum(1 for _, w in NW_WR if l.count(w) == 1), nwr)
    if r.dumps[0][0].get(31) != LIVE:
        g_r += " r31=%s" % hx(r.dumps[0][0].get(31))
        g_w += " r31=%s" % hx(r.dumps[0][0].get(31))
    #  pass 2: a zero is accepted only from a pass that ran to its breakpoint with its liveness proof (Astra, F2),
    #  and only when pass 1 announced that direction at all (`pass 1 silent' otherwise: it IS the channel)
    if len(pcs) < 2 or len(r.conts) < 2:
        g_r2 = g_w2 = "pass 2 %s" % died(r)
    elif pcs[1] != bp2 or r.dumps[1][0].get(31) != LIVE2:
        l2 = lines(r.conts[1])
        tail2 = " stopped pc=%s r31=%s" % (hx(pcs[1]), hx(r.dumps[1][0].get(31)))
        g_r2 = "%d%s" % (sum(1 for x in l2 if x.startswith(RD_HEAD)), tail2)
        g_w2 = "%d%s" % (sum(1 for x in l2 if x.startswith(WR_HEAD)), tail2)
    else:
        l2 = lines(r.conts[1])
        g_r2 = SILENT if nrd == 0 else sum(1 for x in l2 if x.startswith(RD_HEAD))
        g_w2 = SILENT if nwr == 0 else sum(1 for x in l2 if x.startswith(WR_HEAD))
row("p2 nw rd", g_r, "3/3", "FREE: first ld.bu/ld.hu/ld.d -> (len 1)/(len 2)/(len 8) served 0x0")
row("p2 nw wr", g_w, "3/3", "FREE: first st.b/st.h/st.d -> 0xd4/0xc3d4/0x1122334455667788")
row("p2 nw rd 2", g_r2, 0, "pass 2, SAME process: the three non-word reads again -> 0 read-form lines")
row("p2 nw wr 2", g_w2, 0, "pass 2, SAME process: the three non-word stores again -> 0 write-form lines")

#  ZERO-VALUED FIRST STORE, free-running, its OWN session (rev 3; inside announce_pair it would change a 26-count
#  literal).  `st r0' stores the hardwired zero register: NOTHING is seeded into r0 (the m88k core stops the CPU when
#  r0 holds a non-zero value).  The oracle is the exact WRITE-FORM literal, never a count of `[ vme:' lines -- the
#  read form that M_IDATA (`if (writeflag == MEM_WRITE)' -> `if (idata)') prints for a zero store would satisfy a
#  count (grok, F2).
prog = [VSIG(), ST(0, ZERO_OFF), OR_I(31, 0, LIVE), BR_SELF()]
bp = end_of(prog)
r = freerun([GUARD, (CODE, prog)], [(30, SENT), (31, SENT)], [bp, VEC_DACC], [CODE])
bad = devsig_bad(r)
if not bad and (r.pc != bp or not r.conts):
    bad = STOPPED % hx(r.pc)
if bad:
    got = bad
else:
    got = "%d/%d" % (lines(r.conts[0]).count(WR_LINE % (ZERO_OFF, 4, 0)), r.conts[0].count(VMETXT))
    if r.regs.get(31) != LIVE:
        got += " r31=%s" % hx(r.regs.get(31))
row("p2 zero wr", got, "1/1", "FREE: first st r0 at 0x30 -> the write form `(len 4): 0x0 -- declined', one line")


# ================================================================ population 1 (fault) + interims
def fault_row(name, access, extra_seeds, dma_want, dmt_want, note):
    """Stepped, ONE fault per session: VSIG, the access, an or, br; three steps put PC on the vector's br."""
    prog = [VSIG(), access, OR_I(5, 0, LIVE), BR_SELF()]
    r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (30, SENT)] + extra_seeds, 3, cr=True)
    bad = devsig_bad(r)
    if bad:
        got = bad
    else:
        cr = r.cr or {}
        got = "%s/%s/%s/%s" % (r.how, hx(r.pc), hx(cr.get("DMA0")), hx(cr.get("DMT0")))
        for rr in (4, 5):        # a faulting load writes no register; the instruction after it never runs
            if r.regs.get(rr) != SENT:
                got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
    row(name, got, "exit0/0x18/%s/%s" % (hx(VME + dma_want), hx(dmt_want)), note)


fault_row("p1 fault lo", LD(4, 0x90), [], 0x90, DMT_LD_WORD_R4, "ld r4 at 0x90: PC 0x18, DMA0, DMT0, host alive")
fault_row("p1 fault hi", LD(4, 0xffc), [], 0xffc, DMT_LD_WORD_R4, "ld r4 at 0xffc (the last word)")
fault_row("p1 fault mid", LD(4, 0x94), [], 0x94, DMT_LD_WORD_R4, "ld r4 at 0x94 (an interior sample)")
fault_row("p1 fault wr", ST(2, 0x90), [(2, WVAL)], 0x90, DMT_ST_WORD, "st at 0x90: the word-store DMT0")

prog = [VSIG(), LD(4, 0x8c), LD(6, 0x90), OR_I(5, 0, LIVE), BR_SELF()]
r = stepped([GUARD, (CODE, prog)], [(4, SENT), (5, SENT), (6, SENT), (30, SENT)], 4, cr=True)
bad = devsig_bad(r)
if bad:
    got = bad
else:
    cr = r.cr or {}
    got = "%s/%s/%s/%s" % (hx(r.regs.get(4)), hx(r.pc), hx(cr.get("DMA0")), hx(cr.get("DMT0")))
    for rr in (5, 6):
        if r.regs.get(rr) != SENT:
            got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
row("p1 p2 edge", got, "0x0/0x18/%s/%s" % (hx(VME + 0x90), hx(DMT_LD_WORD_R6)),
    "ld 0x8c declines (0), then ld r6 at 0x90 faults")

fault_row("p3 interim", LD_BU(4, 0x51), [], 0x50, DMT_LD_BYTE1_R4,
          "ld.bu 0x51 inside cased T1CMP faults; DMA0 = the WORD address")
fault_row("p2 int byte", LD_BU(4, 0x29), [], 0x28, DMT_LD_BYTE1_R4, "ld.bu 0x29 inside population-2 MASTERCTL faults")
fault_row("p2 int half", LD_HU(4, 0x2a), [], 0x28, DMT_LD_HALF2_R4, "ld.hu 0x2a inside MASTERCTL faults")

#  POPULATION-1 CENSUS: every word start 0x90..0xffc, free-running, each fault counted by the handler.
cprog = [VSIG()] + [LD(4, o) for o in POP1] + [BR_SELF()]
cbp = end_of(cprog, CENSUS)
r = freerun([HANDLER, (CENSUS, cprog)], [(1, 0), (4, SENT), (30, SENT)], [cbp], [CENSUS])
r_census = r
bad = devsig_bad(r)
if bad:
    got = bad
elif r.pc != cbp:
    got = STOPPED % hx(r.pc)
else:
    got = "%d/%d" % (r.regs.get(1, -1), len(POP1))
    if r.regs.get(4) != SENT:
        got += " r4=%s" % hx(r.regs.get(4))
row("p1 census", got, "988/988", "FREE-RUNNING: all 988 population-1 word starts fault")

#  POPULATION-1 WIDTHS: eight non-word accesses, free-running, faults counted; every load destination keeps its
#  sentinel and the closing or runs.  Rev 3 adds the two LANE-0 accesses (word-aligned starts): ld.hu at LANE0_HU
#  into r8 and st.b at LANE0_B -- a refusal narrowed to `len == 2 && (relative_addr & 3) == 0' (M_LANE0H) or its
#  `len == 1' twin (M_LANE0B) declines exactly one of them, which the existing ld.hu 0x96 / st.b 0x9d (lanes 2 and
#  1) cannot see.
prog = [VSIG(), LD_BU(4, 0x93), LD_HU(5, 0x96), LD_D(6, 0x98), ST_B(12, 0x9d), ST_H(12, 0xa2), ST_D(10, 0xa8),
        LD_HU(8, LANE0_HU), ST_B(12, LANE0_B), OR_I(31, 0, LIVE), BR_SELF()]
wbp = end_of(prog)
r = freerun([HANDLER, (CODE, prog)], [(1, 0), (12, NARROW), (10, DHI), (11, DLO), (4, SENT), (5, SENT), (6, SENT),
                                      (7, SENT), (8, SENT), (30, SENT), (31, SENT)], [wbp], [CODE])
r_widths = r
bad = devsig_bad(r)
if bad:
    got = bad
elif r.pc != wbp:
    got = STOPPED % hx(r.pc)
else:
    got = "%d/8" % r.regs.get(1, -1)
    for rr in (4, 5, 6, 7, 8):
        if r.regs.get(rr) != SENT:
            got += " r%d=%s" % (rr, hx(r.regs.get(rr)))
    if r.regs.get(31) != LIVE:
        got += " r31=%s" % hx(r.regs.get(31))
row("p1 widths", got, "8/8", "FREE: ld.bu/ld.hu/ld.d/st.b/st.h/st.d + lane-0 ld.hu/st.b at population 1: 8 faults")


#  `[ vme:' lines in the continue text of the two free-running population-1 runs (rev 3).  Both runs are FREE at
#  verbose 0, so `default:''s debug() prints nothing and a fatal() would print: the census holds 988 READ faults
#  (read-side promotion, M_DFATAL), the widths run four reads and four STORES (write-side promotion, M_DFATALW --
#  the census stores nothing).  A DELETED debug() also prints 0, so deletion is NOT CLAIMED.  Never move this count
#  into a stepped session: stepping makes debug() print, and the row would be red on the fix itself.
def quiet_count(r, bp):
    bad = devsig_bad(r)
    if bad:
        return bad
    if r.pc != bp or not r.conts:
        return STOPPED % hx(r.pc)
    return r.conts[0].count(VMETXT)


q_c, q_w = quiet_count(r_census, cbp), quiet_count(r_widths, wbp)
if isinstance(q_c, int) and isinstance(q_w, int):
    got = "%d/%d" % (q_c, q_w)
else:
    got = "census %s; widths %s" % (q_c, q_w)
row("p1 quiet", got, "0/0", "FREE: no `[ vme:' text in the p1 census run, nor in the p1 widths run")

# ================================================================ disassembly cross-check
#  LITERAL want, derived by hand per session BEFORE the first run: ctl 6, cased 13, rt 13, cased wr 10, free ctl
#  7, p2 rd 30, p2 wr 57, p2 ld widths 7, p2 st widths 11, ann rd 109, ann wr 109, nonword 10, four p1 fault
#  rows 5 each, edge 6, three interim rows 5 each, census 992 (handler 2 + VSIG + 988 + br), p1 widths 11 = 1426
#  (rev 2).  REV 3, re-derived by hand the same way: nonword 18 (guard 1 + pass 1 nine: VSIG, six accesses, or, br
#  + pass 2 eight: six accesses, or, br) = +8; zero wr 5 (guard 1 + VSIG, st r0, or, br) = +5; p1 widths 13
#  (handler 2 + VSIG, eight accesses, or, br) = +2; p1 quiet places nothing.  1426 + 8 + 5 + 2 = 1441.
#  Computing it from the session lists would let a shrunk list pass its own count.
row("unasm", "%d/%d" % (UNASM["ok"], UNASM["n"]), "1441/1441", "every placed word re-read by the disassembler")
for b in UNASM["bad"][:8]:
    print("  unasm mismatch: %s" % b)

# ================================================================ score + done
npass = sum(1 for _, ok in rows if ok)
print("SCORE %d/%d" % (npass, len(rows)))
#  CONTROL rows (rev 3; F8 with GPT-6 Astra's amendment, and GLM's on `vbr reset').  DEFINITION: a row whose role is
#  a PREREQUISITE of the scored rows -- an apparatus, medium or device-signature proof -- and it need not be
#  product-independent: `vbr reset' (DEVINIT's VBR seed) and `free neg ctl' (GCSRCTL's debug() line) also depend on
#  product behaviour, and an edit to the DEVINIT seed reds `vbr reset'.  CONTROL=FAIL means a prerequisite failed and
#  claims NO cause.  `cased census', `t1cmp rt', `free ctl' and `free quiet' are prerequisites of nothing, so they are
#  scored.  (This comment said "a row a product edit can red is SCORED, never CONTROL", which `vbr reset' contradicts;
#  corrected at the records confirmation, as the header was on the repair-diff pass.)
CONTROL_ROWS = ("session", "live", "neg apparatus", "unasm", "vbr reset", "free neg ctl")
_status = dict(rows)
control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)    # a renamed control fails loudly
print("VME_DEFAULT_RESULT=%d/%d" % (npass, len(rows)))
print("VME_DEFAULT_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("VME_DEFAULT_LABEL=%s" % LABEL)
print("VME_DEFAULT_ELAPSED=%.1fs" % (time.time() - t0))
red = [n for n, ok in rows if not ok]
if red:
    print("VME_DEFAULT_RED=%s" % ",".join(red))
shutil.rmtree(_TMPDIR, ignore_errors=True)
print("VME_DEFAULT_PROBE_DONE")
sys.stdout.flush()
sys.exit(0 if control_ok and npass == len(rows) else 1)
