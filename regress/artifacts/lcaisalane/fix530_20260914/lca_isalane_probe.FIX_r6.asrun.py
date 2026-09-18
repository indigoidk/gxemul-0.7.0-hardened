#!/usr/bin/env python3
#
#  lcaisalane -- RUNG-3 WITNESS: the LCA sparse-I/O byte-lane handler ends the host process on an
#  ordinary byte access to a documented ISA register, and SILENTLY ANSWERS ZERO on another.
#
#  THE DEFECT, quoted from `DEVICE_ACCESS(lca_isa)' in src/devices/dev_lca.c:
#
#      relative_addr >>= 5;
#
#      ofs = relative_addr & 3;
#      if (ofs > len) {
#              fatal("[ ofs=%i len=%i in lca_isa access function. "
#                  "aborting ]\n", ofs, len);
#              exit(1);
#      }
#
#      if (writeflag == MEM_WRITE) {
#              byte = data[ofs % len];
#              return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
#                  relative_addr, &byte, 1, writeflag, CACHE_NONE);
#      }
#
#      cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
#          &byte, 1, MEM_READ, CACHE_NONE);
#
#      for (i=0; i<len; i++)
#              data[i] = i == ofs? byte : 0x00;
#
#  *** THE LANE IS NOT AN INDEPENDENT FIELD.  IT IS THE LOW TWO BITS OF THE ISA PORT NUMBER. ***
#  The shift comes FIRST, so `ofs' is bits 6:5 of the incoming relative address -- which are bits
#  1:0 of the derived port -- and the forwarded access goes to `LCA_ISA_BASE + (r >> 5)', i.e. to
#  that same port INCLUDING those two bits.  So there is no way to address ONE port through two
#  different lanes: the lane is a FUNCTION of the port.  The defect therefore partitions the whole
#  64 K ISA port space by `port & 3', and for a BYTE (len == 1) access it reads:
#
#      port & 3 == 0   ->  ofs 0.  data[0] = byte.                        CORRECT
#      port & 3 == 1   ->  ofs 1.  1 > 1 is FALSE, so ACCEPTED -- and the packing loop runs
#                          `for (i = 0; i < 1; i++) data[i] = (i == 1)? byte : 0', which is
#                          never true, so THE DEVICE BYTE IS DISCARDED AND THE GUEST IS HANDED
#                          ZERO with a success return.  A false success, not a decline.
#      port & 3 == 2   ->  ofs 2.  2 > 1  ->  fatal() + exit(1).          HOST DEATH
#      port & 3 == 3   ->  ofs 3.  3 > 1  ->  fatal() + exit(1).          HOST DEATH
#
#  For len == 2 the same arithmetic gives ofs 2 a zero answer and ofs 3 a death; for len 4 and 8
#  `ofs > len' is never true and the packing index is always in range, so those widths are clean.
#  The guard's `>' (rather than `>=') is what admits the zero-answering case: `ofs == len' passes
#  the guard and then indexes nothing.
#
#  WHAT THAT COSTS AT A REAL DEVICE, and it is why the ns16550 is the right subject.  The console
#  UART sits at ISA 0x3f8..0x3ff, so its eight registers fall into all four classes:
#
#      0x3f8 data     ofs 0   ok        0x3fc mcr       ofs 0   ok
#      0x3f9 ier      ofs 1   ZERO      0x3fd lsr       ofs 1   ZERO
#      0x3fa iir      ofs 2   DEATH     0x3fe msr       ofs 2   DEATH
#      0x3fb lctl     ofs 3   DEATH     0x3ff scratch   ofs 3   DEATH
#
#  A byte read of the LINE STATUS REGISTER -- the register a polling console driver reads before
#  every character -- returns zero, and a byte read of the MODEM STATUS or LINE CONTROL register
#  ends the emulator.  No unusual value, no driver setup, four guest instructions.
#
#  ---------------------------------------------------------------------------------------------
#  *** #530: IT IS NOW THE WITNESS AND THE DETECTOR.  Sessions 1-3 are the witness below, unchanged but
#  for the sentinel; the #530 sessions at the end are the detector for the fix. ***
#
#  THE FIX (disposition B, regress/artifacts/lcaisalane/FABLE_F2_RULING_20260914.md): the byte for port
#  P sits at buffer position (P & 3) % len on BOTH arms; `len == 0' is refused first; no latch, no
#  announce (there is no event -- member 4, ACCEPT).  Table 1 (37 rows): HEAD 19/37, fix 37/37
#  (regress/artifacts/lcaisalane/fix530_20260914/HEAD_det.out, FIX_det.out); after the pass-2 repair
#  (51 rows) see that dir's table 2; after closing pass 1's class closure (77 rows) its table 3; after
#  closing pass 2's tail cells and phantom-read rows (93 rows) its table 4; after closing pass 3's
#  fallthrough rows (111 rows) its table 5; after closing pass 4's forward-count CLASS CLOSURE (185 rows) its table 6.
#
#  THE CELL SPACE, rowed WHOLE since closing pass 2 (the direct and head cells since closing pass 1, the
#  tail cells since closing pass 2; pass 2 and closing pass 1 found the same class --
#  a (len, lane, direction) cell of the position rule with no row -- one cell over each time, so the
#  repair rows the cross rather than the next cell): direct widths len 1, 2, 4, 8 x lane 0-3 x R/W,
#  every cell rowed (the read side of len 4 at lanes 2/3 FULL-register, not only a single-lane mask);
#  split HEADS len 1-7 at lane 3 x R/W (a head ends at a port 0x1f mod 0x20; this probe's is 0x3ff);
#  split TAILS len 1-7 at lane 0 x R/W (a tail starts at the next port, 0 mod 0x20) -- tails of len 1,
#  2 and 4 are the direct lane-0 cells, and tails of len 3, 5, 6 and 7 are rowed at the 8042 DATA port
#  0x60 (sessions 4f `tailr' / `tailw', since closing pass 2).  *** THIS SAID "split TAILS start at port
#  0x400, where nothing is mapped, so a tail cell shows only as a whole-access failure ... not rowed per
#  length" UNTIL CLOSING PASS 2, AND IT WAS MEASURED FALSE: tails start at EVERY port 0 mod 0x20 (the
#  8259 at 0x20/0xa0, the 8253 at 0x40, the 8042 at 0x60), and the Opus seat's tail mis-placement
#  mutant scored 77/77 because the split rows' tails at the unmapped 0x400 can show a decline but never
#  a position. ***
#
#  CONTRACT (clause e) -- the detector is DESIGNED to catch, on EITHER arm, at every cell of that space:
#  a byte placed at any position other than (P & 3) % len (a single-cell mis-decode included -- the
#  Opus closing seat's c1_w2, c1_w1w, c1_r4 each scored 51/51 before this repair); and, by name: the
#  removed exit reinstated at any of the six cells that ended the host (reads AND
#  writes at (1,2) (1,3) (2,3)); a decline beyond the width or at-and-beyond it, or of any lane-0 wide
#  access (a store dropped, a load's register kept); a store arm narrowed to len <= 2 or its stores
#  dropped or forwarded to another port; one arm folding and the other not; the byte placed at position 0
#  instead of (P & 3) % len (the clamp, anchored on (2,1) == (2,3)); a lane decode that drops bit 1 or
#  the `& 3', on the read arm or the write arm; `& (len - 1)' for `% len' (the len-3/5 split heads); a
#  byte replicated into every position, at len 2, 4 or 8; the read arm's success return turned into a
#  failure; the write arm's `return' removed, so a store falls into the read arm and makes a phantom
#  read of the stored port (x_wfallthru), and the read arm's forward DUPLICATED (RD2, a second read) -- together THE
#  FORWARD-COUNT CLASS, CLOSED BY ENUMERATION SINCE REPAIR 5 (flagship ruling, regress/artifacts/lcaisalane/
#  FABLE_C4_RULING_20260915.md, part B), in either form, unconditioned or gated on the width, the lane or the data:
#    DIRECT cells, 4 lanes x widths 1/2/4/8 x both arms -- every one rowed.  Lane 0: stores 4k `kbcq' (the 8042 data
#      port, one reply queued), loads 4l `rdq' (two replies queued).  Lane 1: both arms 4m `cmos' (CMOS REG C, whose
#      read clears it).  Lane 2: stores 4h `iir' / 4i `iirw', loads 4j `iirr' (len 1) and 4n `iirr2' (len 2/4/8) (IIR
#      0x3fa with TXRDY armed).  Lane 3: 4o `stub3' ALONE -- the 8042 PC-style stub at 0x63, an emulator-model oracle
#      (below).  4o `stub0'/`stub1'/`stub2' carry lanes 0-2 again as a strengthening, never as the sole carrier.
#    TAIL cells, widths 3/5/6/7 at lane 0 x both arms -- rowed at the 8042 data port 0x60 with the queue: 4p
#      `tailq_w' (one reply queued) and 4q `tailq_r' (two).  Tails of 1/2/4 are the direct lane-0 cells.
#    HEAD cells, widths 1-7 at lane 3 -- EQUIVALENT: the only mapped ports 0x1f mod 0x20 on this machine are 0x3ff and
#      0x2ff (ns16550 SCR, whose read returns d->reg[] with no side effect); 0x60-0x6f holds no 0x1f-mod-0x20 port.
#    DATA: every fallthrough row before repair 5 stored 0; the stub rows store 0x5a at every position and 4m stores 0x0f,
#      so the zero/nonzero partition is rowed on both sides (a strengthening, not floor -- the write body tests no bit
#      of the value); a fallthrough keyed on an EXACT value is disclosed by class.
#  SCOPE of that enumeration, stated because each is a premise: the machine AS PROBED (alphabook1, no IDE image so no
#  wdc at 0x1f0-0x1f7, no VGA without X11; the lpt read arm has no side effect -- checked by the flagship seat); the
#  width set is the memory_rw widths 1/2/4/8 plus the 1 KB split's heads (always lane 3) and tails (always lane 0);
#  `len == 0' is refused and DISCLOSED (no producer); a DIRECTION swap (a store forwarded as a read, or the reverse) is a
#  different class, caught by the value rows.  *** THE CHANNEL AT LANE 3 IS AN EMULATOR TODO: dev_pckbc.c's PC-style
#  branch answers 0x61-0x6f (but 0x64) from `static int x; x++;', bit 0x10 its parity.  If that port is ever implemented
#  the stub rows go green whatever the access count -- which is why every stub session opens with a LIVENESS row (two
#  flat reads must flip bit 0x10) that reds when the oracle disappears. ***
#  *** HISTORY, because each step was a wrong record in its turn: repair 4 SCOPED this entry to lane 2 and lane 0 at the
#  direct widths and DISCLOSED lane 1 and lane-3 direct; its lane-3 warrant ("no read-side-effect port is present on
#  this probe's machine") was MEASURED FALSE by the Opus closing-pass-4 seat (L3gate, the stub at 0x63), its RD2
#  sentence was unscoped while its one row was (1,2) (R2w escaped at len 2/4/8, 111/111), and it gave the tail cells no
#  disposition at all (WT6/WTsplit 111/111) -- grok had corrected the lane-1 and wdc halves hours earlier.  Before that,
#  "the write arm's `return' removed" stood here UNSCOPED while its rows sat at (1,2) and (4,2) only (W4, 93/93). ***
#  *** TABLE 1'S CONTRACT CLAIMED MOST OF THIS AT 37 ROWS AND WAS MEASURED FALSE: the Opus
#  pass-2 seat built ten mutants that scored 37/37, nine changing a guest outcome -- no row stored at len
#  4/8 -- and measured that the split heads it DISCLOSED as needing a translated access split on K0SEG. ***
#  DISCLOSED, not caught: the len-0 refusal (no producer); the zero-fill of the positions other than
#  `ofs' (p_nozero -- EQUIVALENT: memory_rw's #95 pre-zero already clears the buffer); an address-decode
#  edit above port 0x3ff (p_port10 -- not an edit of the fix; measured 51/51 by the Opus closing seat.
#  This said "every probed port is below 0x400", and the split TAILS reach port 0x400 -- grok and the
#  Opus seat, closing pass 1 -- so the premise was wrong and the scoping reason is the one that stands);
#  the DISCARDED sparse byte offset a<4:0> -- the size field a<4:3> included (lcaisasize) -- which the
#  handler shifts away, so an edit keyed on it (the Opus closing-pass-3 seat's H1b, keyed on a<4:0> =
#  0x1c: the 4-byte split head, 93/93; this said "a<4:2> = 0x1c", impossible for a 3-bit slice -- agy,
#  closing pass 4) is not seen [widened from "the size field a<4:3>" by the flagship
#  ruling, closing pass 3]; the hardware QUADWORD ENCODING's route (lcaisaqword: on the
#  21066 a<6:5> = 11 with a<4:3> = 11 is a quadword at port P, which the model forwards to P|3 -- NOT the
#  len-8 lane this probe rows, which follows the same (P & 3) % len rule as every other width); the
#  missing PHYSICAL (lcaisaphys); the end-of-window clamp at port 0xffff (nothing is mapped there).
#  Disclosed BY CLASS (closing pass 2; each measured 77/77 by the Opus seat, regress/artifacts/lcaisalane/
#  opus_c2_20260914/): a decline or mis-decode keyed on an EXACT PORT VALUE (kimi-k3's `relative_addr ==
#  0x400 && len == 4' -- the p_port10 class: the body never tests the port against a constant); a
#  mis-decode keyed on the DATA (codex's `ofs == 2 && !data[2]', generally `data[ofs] ? data[ofs] :
#  data[0]' -- every VALUE store row carries a NONZERO correct byte and the `iir', `iirw' and `kbcq' rows
#  store all-zero words, so no row distinguishes a zero correct byte from a nonzero byte beside it [the
#  `iirw'/`kbcq' zero stores added to this list 2026-09-15 from closing pass 4 (codex, kimi CLI); a sentence
#  "'the correct byte is 0' is unrowed" stood here and was dropped as imprecise by the flagship ruling]).  [Corrected 2026-09-14 from closing pass 3 (codex, grok, kimi-k3): this said
#  "every store row carries a NONZERO correct byte", false since session 4h stores zero.]  EQUIVALENT on alphabook1, named: the inner forward's return value honoured on the
#  read arm, or forced to success on the write arm -- no ISA device there fails an access, and an
#  unmapped forward returns success with a zero fill.
#  EQUIVALENT by construction, named so no table is spent on them (kimi-k3, pass 2): restoring the dead
#  `% len' on the write arm's index (`ofs' is already reduced), and reinstating `if (ofs > len) exit(1)'
#  AFTER the fold (unsatisfiable once ofs < len) -- the reinstated exit that matters is on the UNFOLDED
#  lane, which the table's m_exit builds.
#
#  *** WHAT THE WITNESS (sessions 1-3) IS AND IS NOT.  IT IS A WITNESS, NOT A DETECTOR. ***
#
#  It establishes, on unmodified `alphabook1' with no disk image and no OS: that the sparse window
#  IS live and does reach ISA devices (`live', 0x55 from the 8042 through the same handler); that a
#  BYTE read of a device register whose port is 1 mod 4 completes successfully and hands the guest
#  zero while the device's own byte is demonstrably present (`ofs1 devsig' + `ofs1 wide'); and that
#  a byte read of a register whose port is 2 or 3 mod 4 ends the host with the arm's own diagnostic.
#
#  It is NOT a detector of any repair.  `alive' greens equally for a decline, for a latched
#  announce, for a fault and for a full implementation, and `ofs1 zero' greens for any fix that
#  hands the byte back.  A fix round owes rows that discriminate those -- at minimum, per the codex
#  design reading (regress/artifacts/lcaisalane/codex_design_20260910.err): a REFUSED access must
#  leave the destination register holding its previous value (the `answer' channel this probe
#  already reads), the refusal must repeat without re-announcing, and a supported lane must still
#  deliver the correctly packed byte at every width.
#
#  ---------------------------------------------------------------------------------------------
#  SHAPE, and every element of it is answering a specific objection:
#
#    1.  ONE PROCESS PER OUTCOME, CONTROL FIRST.  A death ends the process, so the two killing
#        lanes get their own runs -- but inside each run the DEVICE SIGNATURE and the WIDE control
#        are taken BEFORE the killing access, so between the access that lives and the access that
#        dies only the WIDTH differs: same address, same window, same process, same instant.
#    2.  ZERO READBACK ALONE PROVES NOTHING, and the design seat said so in those words.  Unmapped
#        space, a missed device and a zero-filled failure buffer all read 0 (`memory_rw.c''s #95
#        pre-zero).  So `ofs1 zero' is never asserted on its own: `ofs1 devsig' reads the SAME
#        register through the flat ISA mapping and gets a nonzero value the device alone produces,
#        and `ofs1 wide' reads it through THIS handler at len 4 and finds the byte sitting in lane
#        1 -- so the byte reaches the packing loop and the loop is what drops it.
#    3.  THE DESTINATION REGISTER IS PRE-SEEDED WITH A SENTINEL before every load.  A load that
#        FAULTS leaves the register untouched (cpu_alpha_instr_loadstore.c returns before
#        writeback when memory_rw fails), so `ofs1 answer' distinguishes "the model answered zero"
#        from "the access failed and the guest kept its old value".  On HEAD it is the former: a
#        FALSE SUCCESS.  This is the discriminator the design seat asked for, taken pre-fix.
#    4.  ATTRIBUTION IS BY THE ARM'S OWN TEXT, NEVER BY EXIT STATUS.  `in lca_isa access function'
#        appears exactly once in src/.  A death for any other reason -- a bad encoding, a different
#        arm -- reds the attrib row instead of passing as a reproduction.
#    5.  EVERY ACCESS IS A GUEST INSTRUCTION.  `lca_isa' is registered DM_DEFAULT, so debugger
#        `dump' would skip the handler entirely and read the pre-zero.  Every `put d' below targets
#        SCRATCH, which is RAM.
#    6.  STAY ON `step'.  Nothing here needs a host timer: the 8042 reply and the UART register
#        file are synchronous with the guest access.
#
#  THE NEGATIVE CONTROL IS ISA PORT 0x300 (`ctl'), which is 0 mod 4 and has NO device behind it.
#  It survives and answers zero.  That is what attributes the two deaths to the LANE rather than to
#  the sparse window, to the byte width, to K0SEG, or to hitting empty ISA space -- and note the
#  two killing ports DO have a device behind them, so the pair brackets the question from both
#  sides.
#
#  Usage:  lca_isalane_probe.py <gxemul-binary> [label]
#          LCAISALANE_RAW=<dir>   -- optional: dump each session's raw pty transcript there
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY
RAW   = os.environ.get("LCAISALANE_RAW", "")

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7
#  T6 is the highest used.  A probe reaching for an undefined register name dies with a NameError
#  rather than emitting a bad encoding, which is the safe direction (#516 found this the hard way).

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)   # BWX byte load  -> memory_rw len 1
def LDL (ra, disp, rb):      return mem(0x28, ra, rb, disp)   # longword load  -> memory_rw len 4
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)   # quadword load  -> memory_rw len 8
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)   # BWX byte store -> memory_rw len 1
def LDWU(ra, disp, rb):      return mem(0x0c, ra, rb, disp)   # BWX word load  -> memory_rw len 2  (#530)
def STW (ra, disp, rb):      return mem(0x0d, ra, rb, disp)   # BWX word store -> memory_rw len 2  (#530)
def STL (ra, disp, rb):      return mem(0x2c, ra, rb, disp)   # longword store -> memory_rw len 4  (#530 pass 2)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)   # quadword store -> memory_rw len 8  (#530 pass 2)
#  LDBU/STB are opcodes 0x0a/0x0e and are decoded with `loadstore_type = 0' in
#  cpu_alpha_instr.c, which selects the 1-byte template in cpu_alpha_instr_loadstore.c -- so the
#  handler under test really does see len == 1.  Not a new capability: lca_irqstub_probe.py already
#  drives STB on this machine, and there is no BWX gate in this tree.

def load_const(reg, val):
    #  32-bit only, and deliberately so: this builds SCRATCH pointers and sentinels, never a
    #  64-bit operand.  Every 64-bit address this probe drives arrives via `put d' + LDQ.
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

SENT = 0x0bad1d8a         #  the pre-seed.  A load that FAULTS leaves this in the register.
#  #530: was 0x0bad1dea, whose low byte 0xea has bits 5-6 SET -- so `ofs1 zero', masked to
#  LSR_FIXED (0x60), read a declined load (sentinel kept) as the LSR byte and went GREEN under a
#  decline (measured on the F2 A variant, regress/artifacts/lcaisalane/opus_f2_20260913/).  0x8a
#  has bits 5-6 CLEAR.  Re-pinned FIRST, HEAD re-run 13/16 with the same three reds, THEN the fix
#  (the oracle-correction order; FABLE_F2_RULING_20260914.md R3).
def sent(reg): return load_const(reg, SENT)

# ---------------------------------------------------------------- addresses
K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p

LCA_PCI_SIO  = 0x1c0000000               # alpha_lcareg.h; DEVINIT maps 0x10000<<5 bytes here as
                                         # "lca_isa" -- THE HANDLER UNDER TEST
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000  # dev_lca.c:47.  bus_isa_init put the real devices here,
                                         # and this is where the handler FORWARDS to.
def SP(port):   return LCA_PCI_SIO  + (port << 5)   # the guest-visible sparse address
def FLAT(port): return LCA_ISA_BASE + port          # the internal flat mapping

#  ---- the ports, and why each one ----------------------------------------------------------
KBC_CMD, KBC_DAT = 0x64, 0x60      # 8042: both 0 mod 4.  0xAA is the standard self-test command
KBC_SELFTEST, KBC_REPLY = 0xAA, 0x55
UART_LSR   = 0x3fd                 # 1 mod 4 -> ofs 1.  DEVICE_ACCESS(ns16550) sets
LSR_FIXED  = 0x60                  #   `d->reg[com_lsr] |= LSR_TXRDY | LSR_TSRE' at the TOP of
                                   #   every access, so 0x20|0x40 is there by construction, with
                                   #   no setup.  Masked to those two bits because LSR_RXRDY (0x01)
                                   #   tracks console input and is the one bit a stray keystroke
                                   #   could flip -- a witness must not have a race in its oracle.
UART_MSR   = 0x3fe                 # 2 mod 4 -> ofs 2.  Same handler unconditionally sets
MSR_FIXED  = 0xb0                  #   MSR_DCD|MSR_DSR|MSR_CTS = 0x80|0x20|0x10, and nothing else
                                   #   ever sets an MSR bit, so this is exact.
UART_SCR   = 0x3ff                 # 3 mod 4 -> ofs 3.  reg 7 falls to the ns16550 `default:' arm,
SCR_VALUE  = 0x5a                  #   which stores and returns the byte -- a plain scratchpad.
NODEV_PORT = 0x300                 # 0 mod 4, and bus_isa_init registers nothing at 0x300.

SCRATCH      = 0x01020000
CODE         = 0x01040000
assert max(SCRATCH, CODE) < 64 * 1024 * 1024, "scratch/code must be inside RAM"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.45):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.5)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)

def build(consts, phases):
    """consts -> SCRATCH slots 0,8,16,...   phases = list of (ops, printreg|None).
    Returns the debugger command list."""
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ops, _ in phases:
        prog += ops
        lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None:
            cmds.append("print %s" % pr)
    return cmds

def run(tag, consts, phases, want_regs, settle=3.0, spin=4.0):
    """want_regs: registers whose `print' MUST be present for the run to be READY.  A run that is
    not ready timed out rather than measured, and is retried ONCE with tripled patience -- the
    machine may be loaded.  Returns (txt, alive, retried)."""
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    retried = False
    if not all(printed(txt, r) is not None for r in want_regs):
        retried = True
        txt, alive = session(cmds, settle * 3, spin * 3)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    return txt, alive, retried

def evidence(txt, tag):
    for _l in txt.split(chr(10)):
        if ("lca_isa access function" in _l or "lca:" in _l or "pckbc:" in _l
                or "non-existant" in _l):
            print("  EVIDENCE[%s]: %s" % (tag, _l.strip()))

def hx(v):
    return "absent" if v is None else "0x%x" % v

ATTRIB = "in lca_isa access function"     # unique in src/; the arm's own diagnostic

print("lca_isalane_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("  sparse LCA_PCI_SIO=0x%x  flat LCA_ISA_BASE=0x%x  ofs = (r>>5) & 3 = port & 3"
      % (LCA_PCI_SIO, LCA_ISA_BASE))
print("%-14s %-24s %-24s %-56s %s" % ("row", "got", "want", "note", ""))

# ================================================================ SESSION 1: the surviving rows
#  [A] STB 0xAA -> sparse(0x64)      8042 command, ofs 0
#  [B] LDBU     <- sparse(0x60)      8042 data,    ofs 0   -> 0x55            `live'
#  [C] LDBU     <- flat(0x3fd)       LSR via the internal mapping             `ofs1 devsig'
#  [D] LDBU     <- sparse(0x3fd)     LSR, len 1, ofs 1 -> 0 on HEAD           `ofs1 zero'
#  [E] LDL      <- sparse(0x3fd)     LSR, len 4, ofs 1 -> byte in lane 1      `ofs1 wide'
#  [F] LDBU     <- sparse(0x300)     no device, ofs 0                         `ctl'
C1 = [k0(SP(KBC_CMD)), KBC_SELFTEST, k0(SP(KBC_DAT)), k0(FLAT(UART_LSR)),
      k0(SP(UART_LSR)), k0(SP(NODEV_PORT))]
P1 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
        LDQ(T1, 16, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
      ([LDQ(T1, 24, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
      ([LDQ(T1, 32, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),
      ([LDQ(T1, 32, T0)] + sent(T6) + [LDL (T6, 0, T1)], "t6"),
      ([LDQ(T1, 40, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2")]
t1x, a1, r1 = run("base", C1, P1, ["t3", "t4", "t5", "t6", "t2"])
b_live, b_flat, b_byte, b_wide, b_ctl = (printed(t1x, r) for r in ("t3", "t4", "t5", "t6", "t2"))
print("  RAW[base]: live=%s flatLSR=%s sparseLSR=%s wideLSR=%s nodev=%s alive=%s retried=%s"
      % (hx(b_live), hx(b_flat), hx(b_byte), hx(b_wide), hx(b_ctl), a1, r1))

row("base alive", "alive" if a1 else "dead", "alive",
    "CONTROL: nothing in this session may end the host")

#  ---- LIVENESS + DEVICE SIGNATURE, through the handler under test ---------------------------
#  Only the 8042 answers 0x55 to a load from ISA 0x60 after 0xAA reached ISA 0x64.  RAM and
#  unmapped space cannot, and this proves the SPARSE window reaches devices at all.
row("live", hx(b_live), hx(KBC_REPLY),
    "LIVENESS+DEVSIG: 8042 self-test reply, THROUGH lca_isa at ofs 0")

#  ---- the device byte exists, taken through the OTHER mapping --------------------------------
row("ofs1 devsig", hx(None if b_flat is None else b_flat & LSR_FIXED), hx(LSR_FIXED),
    "DEVSIG: TXRDY|TSRE are set by the ns16550 handler on every access")

#  ---- THE DEFECT ROW -------------------------------------------------------------------------
#  ORACLE POLARITY is the witness ladder's: assert the CORRECT behaviour, so this is RED pre-fix
#  and GREEN post-fix with the SAME script.  WANT = THE DEVICE BYTE.  For len == 1 the caller's
#  buffer has exactly one lane and it is data[0]; `i == ofs' with ofs 1 selects nothing, so the
#  byte is dropped.  (A DECLINE is the other defensible disposition and would also red this row --
#  which is correct: a decline must not be reported as a successful read of zero.  What a fix may
#  NOT do is keep answering a false zero.)
row("ofs1 zero", hx(None if b_byte is None else b_byte & LSR_FIXED),
    hx(None if b_flat is None else b_flat & LSR_FIXED),
    "*** DEFECT: byte read of ISA 0x3fd (LSR) -- port 1 mod 4 -> ofs 1 ***")

#  ---- the zero is an ANSWER, not a fault -----------------------------------------------------
#  A load whose memory_rw fails returns before writeback (cpu_alpha_instr_loadstore.c), leaving
#  the sentinel.  This row says which of the two happened, and on HEAD it is a FALSE SUCCESS.
row("ofs1 answer", "completed" if (b_byte is not None and b_byte != SENT) else "faulted/absent",
    "completed",
    "the handler returned 1: the guest was ANSWERED zero, not refused")

#  ---- the byte DOES reach the packing loop ---------------------------------------------------
#  Same address, same process, len 4 instead of 1: ofs 1 <= 4, so the loop writes data[1] and the
#  guest sees the byte shifted into lane 1.  This is what makes `ofs1 zero' a lane-packing finding
#  rather than "the sparse window does not reach the UART".
row("ofs1 wide", hx(None if b_wide is None else (b_wide >> 8) & LSR_FIXED), hx(LSR_FIXED),
    "SAME ADDRESS at len 4: the device byte lands in lane 1 -- so it arrived")

#  ---- the negative control for the window ----------------------------------------------------
row("ctl", "alive" if a1 else "dead", "alive",
    "CONTROL: byte access to an ISA port with NO device, ofs 0, survives")
row("ctl zero", hx(b_ctl), hx(0),
    "CONTROL: and it answers zero -- so zero alone proves nothing (see ofs1 devsig)")
evidence(t1x, "base")
print("")

# ================================================================ SESSION 2: ofs 2 ends the host
#  [A] LDBU <- flat(0x3fe)     MSR through the internal mapping   -> 0xb0
#  [B] LDL  <- sparse(0x3fe)   MSR, len 4, ofs 2 -> byte in lane 2, SURVIVES
#  [C] LDBU <- sparse(0x3fe)   MSR, len 1, ofs 2 -> 2 > 1 -> exit(1)
C2 = [k0(FLAT(UART_MSR)), k0(SP(UART_MSR))]
P2 = [([LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
      ([LDQ(T1, 8, T0)] + sent(T3) + [LDL (T3, 0, T1)], "t3"),
      ([LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], None)]
t2x, a2, r2 = run("ofs2", C2, P2, ["t2", "t3"])
m_flat, m_wide = printed(t2x, "t2"), printed(t2x, "t3")
print("  RAW[ofs2]: flatMSR=%s wideMSR=%s alive=%s retried=%s" % (hx(m_flat), hx(m_wide), a2, r2))

row("ofs2 devsig", hx(m_flat), hx(MSR_FIXED),
    "DEVSIG: DCD|DSR|CTS are set by the ns16550 handler on every access")
row("ofs2 wide", hx(None if m_wide is None else (m_wide >> 16) & 0xff), hx(MSR_FIXED),
    "CONTROL: the SAME sparse address at len 4 survives and packs lane 2")
row("ofs2 exit", "alive" if a2 else "dead", "alive",
    "*** DEFECT: byte read of ISA 0x3fe (MSR) -- port 2 mod 4 -> ofs 2 ***")
row("ofs2 attrib", "yes" if (a2 or ATTRIB in t2x) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry the arm's own diagnostic")
evidence(t2x, "ofs2")
print("")

# ================================================================ SESSION 3: ofs 3 ends the host
#  [A] STB 0x5a -> flat(0x3ff);  LDBU <- flat(0x3ff)   scratch register, through the flat mapping
#  [B] LDL  <- sparse(0x3ff)     len 4, ofs 3 -> byte in lane 3, SURVIVES
#  [C] LDBU <- sparse(0x3ff)     len 1, ofs 3 -> 3 > 1 -> exit(1)
C3 = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))]
P3 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
      ([LDQ(T1, 16, T0)] + sent(T4) + [LDL (T4, 0, T1)], "t4"),
      ([LDQ(T1, 16, T0)] + sent(T5) + [LDBU(T5, 0, T1)], None)]
t3x, a3, r3 = run("ofs3", C3, P3, ["t3", "t4"])
s_flat, s_wide = printed(t3x, "t3"), printed(t3x, "t4")
print("  RAW[ofs3]: flatSCR=%s wideSCR=%s alive=%s retried=%s" % (hx(s_flat), hx(s_wide), a3, r3))

row("ofs3 devsig", hx(s_flat), hx(SCR_VALUE),
    "DEVSIG: the ns16550 scratchpad returns the byte just written to it")
row("ofs3 wide", hx(None if s_wide is None else (s_wide >> 24) & 0xff), hx(SCR_VALUE),
    "CONTROL: the SAME sparse address at len 4 survives and packs lane 3")
row("ofs3 exit", "alive" if a3 else "dead", "alive",
    "*** DEFECT: byte read of ISA 0x3ff (scratch) -- port 3 mod 4 -> ofs 3 ***")
row("ofs3 attrib", "yes" if (a3 or ATTRIB in t3x) else "died-elsewhere", "yes",
    "ATTRIBUTION: a death here must carry the arm's own diagnostic")
evidence(t3x, "ofs3")
print("")

# ================================================================ #530: THE DETECTOR SESSIONS
#  Everything above is the rung-3 WITNESS, unchanged except for the sentinel.  Everything below is
#  the DETECTOR for the #530 fix (disposition B, FABLE_F2_RULING_20260914.md): the byte for port P
#  sits at buffer position `(P & 3) % len' on BOTH arms -- the rule HEAD already ran at every served
#  cell -- so no access ends the host and none is answered with a discarded byte.  Each row names
#  the enumerated mutant it kills (R3's table) and the channel: a FULL-REGISTER read (so a declined
#  load, which keeps the sentinel, and a replicated or mis-laned byte all differ from the want), or
#  a store read back through the FLAT mapping, which is a plain forward independent of the handler.
#
#  Ports: LSR 0x3fd (1 mod 4; TXRDY|TSRE forced), MSR 0x3fe (2 mod 4; reads reg|0xb0), IER 0x3f9
#  (1 mod 4; stores and returns the byte), SCR 0x3ff (3 mod 4; scratch).
UART_IER = 0x3f9
UART_MCR = 0x3fc              # 0 mod 4: modem control, stores and returns its low bits (pass 2)
DRETRIED = []

def prints_in_order(txt):
    #  The detector sessions reuse register names, so values are taken IN PRINT ORDER rather than
    #  by name (printed() returns the FIRST match, which would read an earlier phase's value).
    return [int(v, 16) for _, v in re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", txt)]

def dsession(tag, consts, phases, names, settle=3.0, spin=4.0):
    """Returns (alive, {name: value|None}).  A run that did not produce every print is retried ONCE
    with tripled patience -- the load-tolerance rule the witness sessions already follow."""
    need = sum(1 for _, pr in phases if pr is not None)
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    if len(prints_in_order(txt)) < need and alive:
        #  recorded since pass 2 (Opus): before it, this retry was SILENT and LCAISALANE_RETRIED reported
        #  only the three witness sessions
        DRETRIED.append(tag)
        txt, alive = session(cmds, settle * 3, spin * 3)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    vals = prints_in_order(txt)
    got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
    print("  RAW[%s]: alive=%s %s" % (tag, alive, " ".join("%s=%s" % (n, hx(got[n])) for n in names)))
    evidence(txt, tag)
    return alive, got

#  ---- SESSION 4: the cells that never ended the host (no mutant in the table can kill them) --
#  slots: 0 SP(LSR) 1 FLAT(LSR) 2 SP(MSR) 3 FLAT(MSR) 4 SP(IER) 5 FLAT(IER)
C4 = [k0(SP(UART_LSR)), k0(FLAT(UART_LSR)), k0(SP(UART_MSR)), k0(FLAT(UART_MSR)),
      k0(SP(UART_IER)), k0(FLAT(UART_IER))]
P4 = [([LDQ(T1, 8, T0)]  + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                 # lsr  (flat)
      ([LDQ(T1, 0, T0)]  + sent(T3) + [LDBU(T3, 0, T1)], "t3"),                 # r11  len 1 ofs 1
      ([LDQ(T1, 0, T0)]  + sent(T4) + [LDWU(T4, 0, T1)], "t4"),                 # r21  len 2 ofs 1
      ([LDQ(T1, 0, T0)]  + sent(T5) + [LDQ (T5, 0, T1)], "t5"),                 # r81  len 8, P%8 == 5
      ([LDQ(T1, 24, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                 # msr  (flat)
      ([LDQ(T1, 16, T0)] + sent(T2) + [LDWU(T2, 0, T1)], "t2"),                 # r22  len 2 ofs 2
      (load_const(T3, 0x3a) + [LDQ(T1, 32, T0), STB(T3, 0, T1),
       LDQ(T1, 40, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                  # w11  STB -> IER
      (load_const(T3, 0x5a00) + [LDQ(T1, 32, T0), STW(T3, 0, T1),
       LDQ(T1, 40, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),                  # w21  STW -> IER
      (load_const(T3, 0x0040) + [LDQ(T1, 16, T0), STW(T3, 0, T1),
       LDQ(T1, 24, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6")]                  # w22  STW -> MSR
a4, g4 = dsession("fold", C4, P4, ["lsr", "r11", "r21", "r81", "msr", "r22", "w11", "w21", "w22"])
lsr = g4["lsr"]
row("fold alive", "alive" if a4 else "dead", "alive",
    "CONTROL: none of these cells ever ended the host")
row("r11 byte", hx(g4["r11"]), hx(lsr),
    "(1,1) LDBU LSR, FULL register == the flat LSR: kills the A decline (sentinel) + C/HEAD (0)")
row("r21 anchor", hx(g4["r21"]), hx(None if lsr is None else lsr << 8),
    "(2,1) LDWU LSR: position 1 on HEAD and after -- the P mod len ANCHOR; kills replicate/lane edits")
row("r81 lane", hx(g4["r81"]), hx(None if lsr is None else lsr << 8),
    "(8,1) LDQ LSR, port 5 mod 8: lane 1, not 5 -- kills dropping the `& 3' (m_nomask)")
row("r22 byte", hx(g4["r22"]), hx(g4["msr"]),
    "(2,2) LDWU MSR == flat MSR at position 0: kills the A decline and HEAD's discarded byte")
row("w11 lands", hx(g4["w11"]), hx(0x3a),
    "(1,1) STB 0x3a -> IER, flat readback: lands on HEAD -- kills the A decline (F3)")
row("w21 lane", hx(g4["w21"]), hx(0x5a),
    "(2,1) STW 0x5a00 -> IER forwards position 1 on HEAD and after")
row("w22 lands", hx(g4["w22"]), hx(0x40 | MSR_FIXED),
    "(2,2) STW 0x0040 -> MSR, flat readback reg|0xb0: lands on HEAD -- kills the A decline")
print("")

#  ---- SESSION 4b (#530 pass 2): len 4 and 8 STORES, a wide access at a 0-mod-4 port, full-width reads ----
#  The Opus pass-2 seat BUILT ten mutants that scored 37/37 on the rows above, nine of them changing a guest
#  outcome (regress/artifacts/lcaisalane/opus_p2_20260914/): no row ever STORED at len 4 or 8 -- the canonical
#  real-OS `stl' outb -- no row made a wide access at a 0-mod-4 port, and no row read a whole len-4 value.  Every
#  cell here is served on HEAD and on the fix alike (none ends the host), so they share one process.
#  slots: 0 FLAT(SCR) 1 SP(SCR) 2 FLAT(MCR) 3 SP(MCR) 4 SP(LSR) 5 FLAT(LSR)
C4b = [k0(FLAT(UART_SCR)), k0(SP(UART_SCR)), k0(FLAT(UART_MCR)), k0(SP(UART_MCR)),
       k0(SP(UART_LSR)), k0(FLAT(UART_LSR))]
P4b = [(load_const(T3, 0x11) + [LDQ(T1, 0, T0), STB(T3, 0, T1)] + load_const(T3, 0x7e000000)
        + [LDQ(T1, 8, T0), STL(T3, 0, T1), LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),   # (4,3) W
       (load_const(T3, 0x6d000000) + [LDQ(T1, 8, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
        + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                                                      # (8,3) W
       (load_const(T3, 0x01) + [LDQ(T1, 16, T0), STB(T3, 0, T1)] + load_const(T3, 0x03)
        + [LDQ(T1, 24, T0), STL(T3, 0, T1), LDQ(T1, 16, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),  # (4,0) W
       ([LDQ(T1, 24, T0)] + sent(T6) + [LDL(T6, 0, T1)], "t6"),                                     # (4,0) R
       ([LDQ(T1, 32, T0)] + sent(T2) + [LDL(T2, 0, T1)], "t2"),                                     # (4,1) R full
       ([LDQ(T1, 8, T0)]  + sent(T3) + [LDQ(T3, 0, T1)], "t3"),                                     # (8,3) R
       ([LDQ(T1, 40, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                                    # lsr (flat)
a4b, g4b = dsession("wide", C4b, P4b, ["st4", "st8", "mcr4", "mcrrd", "ld4", "ld8", "lsr"])
lsrb = g4b["lsr"]
row("wide alive", "alive" if a4b else "dead", "alive",
    "CONTROL: every access in this session is served on HEAD and on the fix")
row("st4 lane3", hx(g4b["st4"]), hx(0x7e),
    "(4,3) STL 0x7e000000 -> SCR, flat readback: kills p_wbit1, p_wnarrow, p_wdrop4, p_waddr4 (opus p2)")
row("st8 lane3", hx(g4b["st8"]), hx(0x6d),
    "(8,3) STQ 0x6d000000 -> SCR, flat readback: kills p_q8lane and p_wbit1")
row("st4 lane0", hx(g4b["mcr4"]), hx(0x03),
    "(4,0) STL 3 -> MCR (0 mod 4), flat readback: kills p_lane0decl (the store dropped)")
row("ld4 lane0", hx(g4b["mcrrd"]), hx(0x03),
    "(4,0) LDL MCR, FULL register: kills p_lane0decl (the load declined, sentinel kept)")
row("ld4 full", hx(g4b["ld4"]), hx(None if lsrb is None else lsrb << 8),
    "(4,1) LDL LSR, FULL register == lsr << 8: kills p_rep4 (byte replicated at len 4)")
row("ld8 lane3", hx(g4b["ld8"]), hx(0x6d000000),
    "(8,3) LDQ SCR, FULL register: kills p_q8lane's read side")
print("")

#  ---- SESSION 4c (#530 pass 2): the 1 KB SPLIT heads -- MEASURABLE on K0SEG after all --------------
#  The table-1 contract disclosed the split heads as needing a TRANSLATED access.  FALSE (Opus pass 2, measured):
#  MEMORY_RW's split is keyed on `!(misc_flags & PHYSICAL) && cpu->translate_v2p != NULL', Alpha always sets
#  alpha_translate_v2p, and the load/store path passes only CACHE_DATA without an alignment check -- so an
#  unaligned LDQ/LDL on K0SEG splits at port 0x3ff/0x400.  SP(SCR) + 0x1d is 3 bytes below the 1 KB line: an LDQ
#  there hands the handler a len-3 head at ofs 3 -- the (3,3) cell the fix CHANGED (HEAD discarded the byte).
#  The tail goes to flat port 0x400, where nothing is mapped (one `non-existant' line per access, expected).
#  slots: 0 FLAT(SCR) 1 0x5a 2 SP(SCR)+0x1d 3 SP(SCR)+0x1b 4 SP(SCR)
C4c = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR) + 0x1d), k0(SP(UART_SCR) + 0x1b), k0(SP(UART_SCR))]
P4c = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),   # scr (flat)
       ([LDQ(T1, 16, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),                                  # LDQ head len 3
       ([LDQ(T1, 16, T0)] + sent(T5) + [LDL(T5, 0, T1)], "t5"),                                  # LDL head len 3
       ([LDQ(T1, 24, T0)] + sent(T6) + [LDQ(T6, 0, T1)], "t6"),                                  # LDQ head len 5
       ([LDQ(T1, 32, T0)] + sent(T2) + [LDQ(T2, 0, T1)], "t2"),                                  # aligned control
       (load_const(T3, 0x00c3007e) + [LDQ(T1, 16, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
        + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                                                   # STQ head len 3
a4c, g4c = dsession("split", C4c, P4c, ["scr", "q3", "l3", "q5", "qal", "w3"])
row("split alive", "alive" if a4c else "dead", "alive",
    "CONTROL: no split head here ends the host on HEAD or on the fix")
row("split devsig", hx(g4c["scr"]), hx(SCR_VALUE),
    "DEVSIG: the scratchpad holds 0x5a through the flat mapping")
row("h3 ldq", hx(g4c["q3"]), hx(SCR_VALUE),
    "(3,3) LDQ head: position 3 % 3 = 0 -- RED ON HEAD (discarded byte); kills & (len-1) (0x5a0000)")
row("h3 ldl", hx(g4c["l3"]), hx(SCR_VALUE),
    "(3,3) LDL head: the no-BWX route to the fix-changed cell -- RED ON HEAD; kills & (len-1)")
row("h5 ldq", hx(g4c["q5"]), hx(SCR_VALUE << 24),
    "(5,3) LDQ head: position 3 % 5 = 3; kills & (len-1) (position 3 & 4 = 0)")
row("split al", hx(g4c["qal"]), hx(SCR_VALUE << 24),
    "CONTROL: the aligned LDQ at the same port packs lane 3")
row("h3 stq", hx(g4c["w3"]), hx(0x7e),
    "(3,3) STQ 0x00c3007e head: position 0 forwards 0x7e; kills & (len-1) (position 2 = 0xc3)")
print("")

#  ---- SESSION 4d (#530 closing pass 1): THE WHOLE len x lane x direction CROSS for the direct widths ------------
#  Closing pass 1 found the same class as pass 2 one cell over -- codex an LDQ at lane 0, grok (2,0) and (8,0), minimax a
#  wide STORE at lane 1, glm one at lane 2 -- and the PRETABLE's sibling-parity line had checked WIDTHS per arm and said
#  nothing about LANES per width, which is how it passed.  Two passes, one class: this repair rows the whole cross.  The
#  direct widths are 1, 2, 4, 8 and the lane is P & 3; every (len, lane, dir) cell is now rowed somewhere -- the ones
#  below are the nine no earlier session reached, plus FULL-register len-4 reads at lanes 2 and 3 (the Opus
#  closing seat, measured: `ofs2/ofs3 wide' mask one lane, so a mis-fill of the OTHER positions scored 51/51).  Lane 0 = MCR 0x3fc, lane 1 = IER 0x3f9, lane 2 = MSR 0x3fe (a store
#  is kept; a read returns reg | 0xb0), lane 3 = SCR 0x3ff.  None of these cells ever ended the host.
#  slots: 0 FLAT(MCR) 1 SP(MCR) 2 FLAT(IER) 3 SP(IER) 4 FLAT(MSR) 5 SP(MSR) 6 FLAT(SCR) 7 0x5a 8 SP(SCR)
C4d = [k0(FLAT(UART_MCR)), k0(SP(UART_MCR)), k0(FLAT(UART_IER)), k0(SP(UART_IER)),
       k0(FLAT(UART_MSR)), k0(SP(UART_MSR)), k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))]
P4d = [(load_const(T3, 0x03) + [LDQ(T1, 0, T0), STB(T3, 0, T1),                                  # MCR = 3 (flat)
        LDQ(T1, 8, T0)] + sent(T2) + [LDWU(T2, 0, T1)], "t2"),                                    # R(2,0)
       ([LDQ(T1, 8, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),                                     # R(8,0)
       ([LDQ(T1, 40, T0)] + sent(T5) + [LDQ(T5, 0, T1)], "t5"),                                    # R(8,2)
       ([LDQ(T1, 32, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                                   # msr (flat)
       ([LDQ(T1, 40, T0)] + sent(T2) + [LDL(T2, 0, T1)], "t2"),                                    # R(4,2) FULL
       ([LDQ(T1, 48, T0), LDQ(T2, 56, T0), STB(T2, 0, T1),
         LDQ(T1, 64, T0)] + sent(T3) + [LDL(T3, 0, T1)], "t3"),                                   # R(4,3) FULL
       (load_const(T3, 0x0002) + [LDQ(T1, 8, T0), STW(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                                     # W(2,0) -> MCR
       (load_const(T3, 0x01) + [LDQ(T1, 8, T0), STQ(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                                     # W(8,0) -> MCR
       (load_const(T3, 0x4d00) + [LDQ(T1, 24, T0), STL(T3, 0, T1),
        LDQ(T1, 16, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),                                    # W(4,1) -> IER
       (load_const(T3, 0x5c00) + [LDQ(T1, 24, T0), STQ(T3, 0, T1),
        LDQ(T1, 16, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                                    # W(8,1) -> IER
       (load_const(T3, 0x00400000) + [LDQ(T1, 40, T0), STQ(T3, 0, T1),
        LDQ(T1, 32, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                                    # W(8,2) -> MSR
       ([LDQ(T1, 32, T0), STB(ZERO, 0, T1)]                                                        # MSR = 0 (flat)
        + load_const(T3, 0x00040000) + [LDQ(T1, 40, T0), STL(T3, 0, T1),
        LDQ(T1, 32, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                                    # W(4,2) -> MSR
a4d, g4d = dsession("cross", C4d, P4d, ["r20", "r80", "r82", "msr", "r42", "r43", "w20", "w80", "w41", "w81", "w82",
                                          "w42"])
row("cross alive", "alive" if a4d else "dead", "alive", "CONTROL: none of these cells ever ended the host")
row("r20 byte", hx(g4d["r20"]), hx(0x03), "(2,0) LDWU MCR: position 0")
row("r80 byte", hx(g4d["r80"]), hx(0x03), "(8,0) LDQ MCR: position 0 -- codex's `return len != 8 || ofs'")
row("r82 lane", hx(g4d["r82"]), hx(None if g4d["msr"] is None else g4d["msr"] << 16), "(8,2) LDQ MSR: position 2")
row("r42 full", hx(g4d["r42"]), hx(None if g4d["msr"] is None else g4d["msr"] << 16),
    "(4,2) LDL MSR, FULL register: position 2 and the other positions 0 (Opus c1_r4)")
row("r43 full", hx(g4d["r43"]), hx(SCR_VALUE << 24), "(4,3) LDL SCR, FULL register: position 3, the rest 0")
row("w20 lands", hx(g4d["w20"]), hx(0x02), "(2,0) STW 0x0002 -> MCR, flat readback")
row("w80 lands", hx(g4d["w80"]), hx(0x01), "(8,0) STQ 0x01 -> MCR, flat readback")
row("w41 lane", hx(g4d["w41"]), hx(0x4d), "(4,1) STL 0x4d00 -> IER: position 1 (minimax)")
row("w81 lane", hx(g4d["w81"]), hx(0x5c), "(8,1) STQ 0x5c00 -> IER: position 1")
row("w82 lane", hx(g4d["w82"]), hx(0x40 | MSR_FIXED), "(8,2) STQ 0x400000 -> MSR: position 2 (glm's store side)")
row("w42 lane", hx(g4d["w42"]), hx(0x04 | MSR_FIXED), "(4,2) STL 0x40000 -> MSR: position 2")
print("")

#  ---- SESSIONS 4e (#530 closing pass 1): the SPLIT heads at every length 1..7, both arms --------------------------
#  A split head always ends at a port 0x1f mod 0x20 (lane 3 -- the lane is the invariant; this probe's boundary is port
#  0x3ff), so its cells are (len, 3) for len 1..7.  4c rowed len 3 (R, W) and
#  5 (R); deepseek found `len == 6' free.  Heads of len 6 and 7 (R) and 5-7 (W) never ended the host and share one
#  process; heads of len 1 and 2 DID (they are the (1,3) / (2,3) cells reached WITHOUT BWX -- `lcaisaunaligned'), so each
#  gets its own process with an `alive' row, like sessions 5-10.
#  STQ value 0xc3a5967e: position 0 = 0x7e, 1 = 0x96, 3 = 0xc3.
SPLITV = 0xc3a5967e
C4e = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR) + 0x1a), k0(SP(UART_SCR) + 0x19), k0(SP(UART_SCR) + 0x1b)]
P4e = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),  # scr = 0x5a (flat)
       ([LDQ(T1, 16, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),                                  # R head 6
       ([LDQ(T1, 24, T0)] + sent(T5) + [LDQ(T5, 0, T1)], "t5"),                                  # R head 7
       (load_const(T3, SPLITV) + [LDQ(T1, 32, T0), STQ(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                                   # W head 5 -> SCR
       ([LDQ(T1, 0, T0), STB(ZERO, 0, T1)] + load_const(T3, SPLITV) + [LDQ(T1, 16, T0), STQ(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                                   # W head 6 -> SCR
       ([LDQ(T1, 0, T0), STB(ZERO, 0, T1)] + load_const(T3, SPLITV) + [LDQ(T1, 24, T0), STQ(T3, 0, T1),
        LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                                   # W head 7 -> SCR
a4e, g4e = dsession("split67", C4e, P4e, ["scr", "q6", "q7", "w5", "w6", "w7"])
row("split67 alive", "alive" if a4e else "dead", "alive", "CONTROL: heads of len 5-7 never ended the host")
row("h6 ldq", hx(g4e["q6"]), hx(SCR_VALUE << 24), "(6,3) LDQ head: position 3 -- deepseek's `len == 6'")
row("h7 ldq", hx(g4e["q7"]), hx(SCR_VALUE << 24), "(7,3) LDQ head: position 3")
row("h5 stq", hx(g4e["w5"]), hx(0xc3), "(5,3) STQ head: position 3 forwards 0xc3")
row("h6 stq", hx(g4e["w6"]), hx(0xc3), "(6,3) STQ head: position 3")
row("h7 stq", hx(g4e["w7"]), hx(0xc3), "(7,3) STQ head: position 3")
print("")

for tag, off, store, wantf, note in (
        ("h1 ldq", 0x1f, False, lambda: SCR_VALUE, "(1,3) LDQ head: was a host death on HEAD (no BWX)"),
        ("h2 ldq", 0x1e, False, lambda: SCR_VALUE << 8, "(2,3) LDQ head: position 1; was a host death on HEAD"),
        ("h1 stq", 0x1f, True, lambda: 0x7e, "(1,3) STQ head: position 0; was a host death on HEAD"),
        ("h2 stq", 0x1e, True, lambda: 0x96, "(2,3) STQ head: position 1; was a host death on HEAD")):
    C = [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR) + off)]
    if store:
        P = [(load_const(T3, SPLITV) + [LDQ(T1, 16, T0), STQ(T3, 0, T1),
              LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
    else:
        P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
               LDQ(T1, 16, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4")]
    ah, gh = dsession(tag.replace(" ", "_"), C, P, ["v"])
    row("%s alive" % tag, "alive" if ah else "dead", "alive", note)
    row(tag, hx(gh["v"]), hx(wantf()), note.split(":")[0] + " value")
print("")

#  ---- SESSIONS 4f (#530 closing pass 2): the split TAIL cells, at a MAPPED port ------------------------------------
#  A 1 KB split (MRW_SPLIT_MASK 0x3ff on the VIRTUAL address = 32 sparse ports) puts its head at a port 0x1f mod 0x20
#  (lane 3) and its TAIL at the next port, 0 mod 0x20 (lane 0), of length 8 - h (LDQ/STQ) or 4 - h (LDL/STL).  Tails of
#  length 1, 2 and 4 are handler-identical to the direct lane-0 cells; tails of length 3, 5, 6 and 7 exist ONLY as tails.
#  The split rows above put their tails on port 0x400, where nothing is mapped: a tail read there is zero-filled and a
#  tail write goes nowhere, so they see a tail DECLINE and never a tail MIS-PLACEMENT (principle 2 -- zero readback alone
#  proves nothing -- applied to the probe's own tails).  The Opus closing-pass-2 seat MEASURED
#  `if ((relative_addr & 3) == 0 && len > 2 && (len & 3)) ofs = 1;' at 77/77 (regress/artifacts/lcaisalane/
#  opus_c2_20260914/).  These two sessions are its discriminator, ported: an unaligned LDQ/STQ at SP(0x5f) + 0x1f / 0x1e
#  / 0x1d / 0x1b is a head of 1 / 2 / 3 / 5 at port 0x5f (unmapped) and a tail of 7 / 6 / 5 / 3 at port 0x60, the 8042
#  DATA port.  Read channel: the self-test reply 0x55 lands at register byte h.  Write channel: the 8042 command byte
#  (0x60 to the command port, then the tail's forwarded byte; read back with 0x20 through the FLAT mapping).  The 1- and
#  2-byte heads at 0x5f are (1,3) and (2,3) cells, so on HEAD each session ends the host at its first split.
TAILHEADS = ((1, 0x1f), (2, 0x1e), (3, 0x1d), (5, 0x1b))   # (head length h, byte offset) -> tail 8 - h at port 0x60
C4f = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(SP(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
def kbc_selftest(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
P4f = [(kbc_selftest() + [LDQ(T1, 16, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3")]                  # control: (8,0)
for i in range(len(TAILHEADS)):
    P4f.append((kbc_selftest() + [LDQ(T1, 24 + 8 * i, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"))
a4f, g4f = dsession("tailr", C4f, P4f, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
row("tailr alive", "alive" if a4f else "dead", "alive", "CONTROL (1/2-byte heads at 0x5f were host deaths on HEAD)")
row("tailr ctl", hx(g4f["ctl"]), hx(KBC_REPLY), "CONTROL: aligned LDQ at SP(0x60), the (8,0) cell, reads 0x55")
for h, _ in TAILHEADS:
    row("tailr t%d" % (8 - h), hx(g4f["t%d" % (8 - h)]), hx(KBC_REPLY << (8 * h)),
        "(%d,0) LDQ TAIL at port 0x60: position 0 -> register byte %d" % (8 - h, h))
print("")

def tailv(h): return (0x44 << (8 * h)) | (0x21 << (8 * (h + 1)))   # tail position 0 = 0x44, position 1 = 0x21
C4g = ([k0(FLAT(KBC_CMD)), 0x60, 0x20, k0(FLAT(KBC_DAT))] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
       + [tailv(h) for h, _ in TAILHEADS])
def kbc_ldcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]
def kbc_rdcmd(): return [LDQ(T1, 0, T0), LDQ(T2, 16, T0), STB(T2, 0, T1), LDQ(T1, 24, T0)]
def kbc_reset(): return kbc_ldcmd() + load_const(T3, 0x04) + [LDQ(T1, 24, T0), STB(T3, 0, T1)]   # cmdbyte = 0x04 (flat)
P4g = [(kbc_reset() + kbc_rdcmd() + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                          # control: flat
#  Each tail phase RESETS the command byte to 0x04 first: without it a DECLINED tail store would read back the previous
#  phase's 0x44 and pass (the order is t7, t6, t5, t3), so these rows would see a mis-placement and never a decline.
for i in range(len(TAILHEADS)):
    P4g.append((kbc_reset() + kbc_ldcmd() + [LDQ(T3, 64 + 8 * i, T0), LDQ(T1, 32 + 8 * i, T0), STQ(T3, 0, T1)]
                + kbc_rdcmd() + sent(T5) + [LDBU(T5, 0, T1)], "t5"))
a4g, g4g = dsession("tailw", C4g, P4g, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
row("tailw alive", "alive" if a4g else "dead", "alive", "CONTROL (1/2-byte heads at 0x5f were host deaths on HEAD)")
row("tailw ctl", hx(g4g["ctl"]), hx(0x04), "CONTROL: flat command-byte round trip")
for h, _ in TAILHEADS:
    row("tailw t%d" % (8 - h), hx(g4g["t%d" % (8 - h)]), hx(0x44),
        "(%d,0) STQ TAIL at port 0x60 forwards position 0 (0x44), not 1 (0x21)" % (8 - h))
print("")

#  ---- SESSION 4h (#530 closing pass 2): a store to a port whose READ has a side effect ---------------------------
#  Every port the 77-row instrument stored to read back without a side effect, so deleting the write arm's `return' -- the
#  store then FALLS INTO the read arm, a phantom 1-byte read of the same port -- scored 77/77 (x_wfallthru, table 3 and
#  the Opus closing-pass-2 seat).  It is not equivalent for a guest: dev_ns16550.c's com_iir READ arm clears IIR_TXRDY
#  (and com_data's calls console_readchar, so every THR store would eat a pending input character).  Channel: arm
#  TXRDY (IER 0 -> ETXRDY), store 0 through lca_isa to ISA 0x3fa (FCR on a write, IIR on a read), flat IIR & 3.
UART_IIR = 0x3fa                    # 2 mod 4 -> lane 2
def iir_arm(): return load_const(T3, 0x02) + [LDQ(T1, 0, T0), STB(ZERO, 0, T1), STB(T3, 0, T1)]
C4h = [k0(FLAT(UART_IER)), k0(FLAT(UART_IIR)), k0(SP(UART_IIR))]
P4h = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                     # control, no lca store
       (iir_arm() + [LDQ(T1, 16, T0), STB(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),  # (1,2)
       (iir_arm() + [LDQ(T1, 16, T0), STL(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]  # (4,2)
a4h, g4h = dsession("iir", C4h, P4h, ["ctl", "stb", "stl"])
iir3 = lambda v: None if v is None else v & 0x03
row("iir alive", "alive" if a4h else "dead", "alive", "CONTROL")
row("iir ctl", hx(iir3(g4h["ctl"])), hx(0x02), "CONTROL: IER 0 -> ETXRDY sets IIR_TXRDY; flat IIR & 3 = TXRDY")
row("iir stb", hx(iir3(g4h["stb"])), hx(0x02), "(1,2) STB 0 -> SP(0x3fa): TXRDY survives the store (x_wfallthru)")
row("iir stl", hx(iir3(g4h["stl"])), hx(0x02), "(4,2) STL 0 -> SP(0x3fa): TXRDY survives the store (x_wfallthru)")
print("")

#  ---- SESSIONS 4i-4k (#530 closing pass 3, REPAIR 4 -- the flagship ruling, option (c)) -------------------------
#  Closing pass 3 measured the same channel escaping GATED: `return' removed only for len 8 (W1) or len 2 (W2), for
#  every width but the two 4h stores at (W4), or only off lane 2 (W3) -- all 93/93 and guest-visible (the Opus seat,
#  regress/artifacts/lcaisalane/opus_c3_20260914/) -- and its read-arm mirror RD2 (the forward DUPLICATED) likewise.
#  The flagship ruled the contract's unscoped x_wfallthru entry a wrong record to be fixed in-round by rowing every
#  OBSERVABLE cell of the class (regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md).  A phantom read shows only
#  where the forwarded-to port's READ has a side effect that is ARMED: lane 2 -> IIR 0x3fa (TXRDY armed, as 4h); lane 0
#  -> the 8042 data port 0x60 with a reply QUEUED (a self-test's 0x55, then 0xd1 so the store lands in output_byte, not
#  in the keyboard; a phantom read pops the 0x55 and the flat status's DIB bit drops).  The 8042 queue is a FIFO, so
#  each lane-0 width gets its own process (one queued reply each).  New sessions only: no earlier session changes.
P4i = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                     # control, no lca store
       (iir_arm() + [LDQ(T1, 16, T0), STW(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),  # (2,2)
       (iir_arm() + [LDQ(T1, 16, T0), STQ(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]  # (8,2)
a4i, g4i = dsession("iirw", C4h, P4i, ["ctl", "stw", "stq"])
row("iirw alive", "alive" if a4i else "dead", "alive", "CONTROL")
row("iirw ctl", hx(iir3(g4i["ctl"])), hx(0x02), "CONTROL: IER 0 -> ETXRDY sets IIR_TXRDY")
row("iir stw", hx(iir3(g4i["stw"])), hx(0x02), "(2,2) STW 0 -> SP(0x3fa): TXRDY survives (W1/W2/W4: gated fallthrough)")
row("iir stq", hx(iir3(g4i["stq"])), hx(0x02), "(8,2) STQ 0 -> SP(0x3fa): TXRDY survives (W1/W4)")
print("")

C4j = [k0(FLAT(UART_IER)), k0(SP(UART_IIR))]
P4j = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]                     # (1,2) READ via lca
a4j, g4j = dsession("iirr", C4j, P4j, ["rd"])
row("iirr alive", "alive" if a4j else "dead", "alive", "CONTROL ((1,2) read -- a host death on HEAD)")
row("iir lca rd", hx(iir3(g4j["rd"])), hx(0x02), "(1,2) LDBU SP(0x3fa) after arming: TXRDY read ONCE (RD2: forwarded twice)")
print("")

KBC_WROUTPORT = 0xd1                # the next data-port write goes to output_byte, not to the keyboard
for w, stop in (("b", STB), ("w", STW), ("l", STL), ("q", STQ)):
    C = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, KBC_WROUTPORT, k0(SP(KBC_DAT))]
    P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T2, 16, T0), STB(T2, 0, T1)]
          + sent(T3) + [LDBU(T3, 0, T1)], "t3"),                                                # flat status, reply queued
         ([LDQ(T1, 24, T0), stop(ZERO, 0, T1), LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]  # lca store, status
    ak, gk = dsession("kbcq_" + w, C, P, ["pre", "post"])
    dib = lambda v: None if v is None else v & 0x01
    lenw = {"b": 1, "w": 2, "l": 4, "q": 8}[w]
    row("kbcq %s alive" % w, "alive" if ak else "dead", "alive", "CONTROL")
    row("kbcq %s pre" % w, hx(dib(gk["pre"])), hx(0x01), "CONTROL: the self-test reply is queued (status DIB)")
    row("kbcq %s dib" % w, hx(dib(gk["post"])), hx(0x01),
        "(%d,0) ST 0 -> SP(0x60): the queued reply survives the store (W3: lane-gated fallthrough)" % lenw)
print("")

#  ---- SESSIONS 4l-4q (#530 closing pass 4, REPAIR 5 -- the forward-count CLASS CLOSURE) --------------------------
#  Closing pass 4 found the class a THIRD consecutive time, each escape guest-visible at 111/111 (the Opus seat,
#  regress/artifacts/lcaisalane/opus_c4_20260914/): RD2 gated on the width (only (1,2) was rowed), the split-TAIL cells,
#  lane-0 reads, lane-3 direct.  The flagship ruling (regress/artifacts/lcaisalane/FABLE_C4_RULING_20260915.md, part B)
#  owes the enumeration DERIVED FROM THE HANDLER in one diff: its two arms (a store's phantom read after the forward; a
#  load's forward duplicated) x every width kind x every lane.  Each observable cell below has a row, on an ARCHITECTURAL
#  channel at lanes 0-2 and on the 8042 stub counter at lane 3 (the only lane-3 port with an access side effect on this
#  machine); the stub also carries lanes 0-2 as a strengthening, never as the sole carrier.  Heads are EQUIVALENT (below).
#
#  4l `rdq': LANE-0 READS, direct widths 1/2/4/8.  Two self-test replies queued, one lca load of SP(0x60), then the flat
#  status: DIB must still be 1 (a duplicated read pops both).  Each phase drains the survivor with a flat data read.  The
#  control shows the channel counts pops: after two replies and ONE flat pop DIB is 1, after a second pop it is 0.
def selftest(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]             # queue one 0x55 (slot 0 = cmd port)
def kstatus(reg): return [LDQ(T1, 0, T0)] + sent(reg) + [LDBU(reg, 0, T1)]           # flat status (DIB = bit 0)
def kpop(): return [LDQ(T1, 16, T0), LDBU(T5, 0, T1)]                                # flat data read (slot 2) pops one
C4l = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(FLAT(KBC_DAT)), k0(SP(KBC_DAT))]
P4l = [(selftest() + selftest() + kpop() + kstatus(T4), "t4"),                        # control: one of two left
       (kpop() + kstatus(T4), "t4")]                                                  # control: none left
for w, n, ld, _ in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
    P4l.append((selftest() + selftest() + [LDQ(T1, 24, T0)] + sent(T3) + [ld(T3, 0, T1)] + kstatus(T4) + kpop(), "t4"))
a4l, g4l = dsession("rdq", C4l, P4l, ["ctl1", "ctl0", "r1", "r2", "r4", "r8"])
dibv = lambda v: None if v is None else v & 0x01
row("rdq alive", "alive" if a4l else "dead", "alive", "CONTROL")
row("rdq ctl1", hx(dibv(g4l["ctl1"])), hx(0x01), "CONTROL: two replies queued, one flat pop -> one left (DIB 1)")
row("rdq ctl0", hx(dibv(g4l["ctl0"])), hx(0x00), "CONTROL: a second flat pop empties it (DIB 0): the channel counts pops")
for n in (1, 2, 4, 8):
    row("rdq r%d" % n, hx(dibv(g4l["r%d" % n])), hx(0x01),
        "(%d,0) LOAD SP(0x60) pops ONE of two replies (RD2: the read forward duplicated)" % n)
print("")

#  4m `cmos': LANE 1, both arms, direct widths 1/2/4/8, on CMOS register C through the pccmos index/data pair (select
#  0x0c at 0x70; 0x71 forwards to dev_mc146818.c, whose REG C read returns the register and then ZEROES it, and whose
#  store sets it).  The stored value is 0x0f and every compare masks 0x0f: the mc146818 access path ORs UF/AF/PF/IRQF
#  (0xf0) into REG C from the HOST CLOCK, so only the low nibble is deterministic.  Store rows: an lca store of 0x0f
#  must still read back 0x0f (a phantom read after the store clears it).  Load rows: after a flat store of 0x0f the lca
#  load must deliver 0x0f at lane position (1 % len) (a duplicated forward delivers the second, cleared, read).
CMOS_VAL = 0x0f0f0f0f0f0f0f0f
def csel(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]                   # select REG C (flat 0x70)
def cset(): return csel() + [LDQ(T1, 24, T0), LDQ(T3, 32, T0), STB(T3, 0, T1)]        # flat store 0x0f -> REG C
def cget(reg): return csel() + [LDQ(T1, 24, T0)] + sent(reg) + [LDBU(reg, 0, T1)]     # flat read REG C (clears it)
C4m = [k0(FLAT(0x70)), 0x0c, k0(SP(0x71)), k0(FLAT(0x71)), CMOS_VAL]
P4m = [(cset() + cget(T4), "t4"), (cget(T4), "t4")]                                   # controls: set, then cleared
for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
    P4m.append((csel() + [LDQ(T1, 16, T0), LDQ(T3, 32, T0), st(T3, 0, T1)] + cget(T4), "t4"))       # lca STORE
for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
    P4m.append((cset() + csel() + [LDQ(T1, 16, T0)] + sent(T4) + [ld(T4, 0, T1)], "t4"))           # lca LOAD
a4m, g4m = dsession("cmos", C4m, P4m, ["set", "clr", "w1", "w2", "w4", "w8", "r1", "r2", "r4", "r8"])
nib = lambda v, sh=0: None if v is None else (v >> sh) & 0x0f
row("cmos alive", "alive" if a4m else "dead", "alive", "CONTROL")
row("cmos set", hx(nib(g4m["set"])), hx(0x0f), "CONTROL: a flat store of 0x0f to REG C reads back 0x0f")
row("cmos clr", hx(nib(g4m["clr"])), hx(0x00), "CONTROL: that read cleared it -- the channel sees ONE extra read")
for n in (1, 2, 4, 8):
    row("cmos w%d" % n, hx(nib(g4m["w%d" % n])), hx(0x0f),
        "(%d,1) STORE 0x0f.. -> SP(0x71): REG C keeps it (x_wfallthru: a phantom read clears it)" % n)
for n in (1, 2, 4, 8):
    row("cmos r%d" % n, hx(nib(g4m["r%d" % n], 8 * (1 % n))), hx(0x0f),
        "(%d,1) LOAD SP(0x71) delivers REG C = 0x0f at position %d (RD2: the second read is cleared)" % (n, 1 % n))
print("")

#  4n `iirr2': LANE-2 READS at widths 2/4/8 -- a NEW session, `iirr' (the (1,2) read) is left as it was.  Re-arm TXRDY
#  before each load; the lane-2 byte of the loaded value must be IIR & 3 = TXRDY (a duplicated read clears it first).
C4n = [k0(FLAT(UART_IER)), k0(SP(UART_IIR))]
P4n = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T4) + [ld(T4, 0, T1)], "t4") for ld in (LDWU, LDL, LDQ)]
a4n, g4n = dsession("iirr2", C4n, P4n, ["r2", "r4", "r8"])
row("iirr2 alive", "alive" if a4n else "dead", "alive", "CONTROL")
for n, sh in ((2, 0), (4, 16), (8, 16)):
    v = g4n["r%d" % n]
    row("iir lca rd%d" % n, hx(None if v is None else (v >> sh) & 0x03), hx(0x02),
        "(%d,2) LOAD SP(0x3fa) after arming: TXRDY at position %d, read ONCE (R2w: RD2 gated on len)" % (n, 2 % n))
print("")

#  4o `stub0'-`stub3': the 8042 PC-style STUB.  dev_pckbc.c answers every port of 0x61-0x6f except 0x64 from a
#  FUNCTION-STATIC counter (`static int x; x++;') bumped on EVERY access, read or write, with bit 0x10 its parity -- a
#  "TODO (port 0x61)", an EMULATOR-MODEL oracle, not an architectural register (like the 0xffffffff absent-device
#  signature).  Flat read, ONE lca access, flat read: the two flat answers agree in bit 0x10; an extra access flips it.
#  The flats are chained, so each row brackets exactly one lca access.  Stores carry 0x5a at every byte position, so
#  the data-keyed fallthrough (dataA: the fallthrough only on a NONZERO byte) is inside the rows.  Lane 3 (0x63) is the
#  SOLE carrier of its cells; lanes 0-2 (0x68, 0x61, 0x62) are a strengthening beside 4k/4l/4m/4h-4j/4n.
#  *** LIVENESS, and it is MANDATORY: if port 0x61 is ever implemented every stub row goes green whatever the access
#  count.  Each session opens with two flat reads and NO lca access between them, which MUST flip bit 0x10. ***
STUB_DATA = 0x5a5a5a5a5a5a5a5a
for lane, port in ((3, 0x63), (0, 0x68), (1, 0x61), (2, 0x62)):
    C = [k0(FLAT(port)), k0(SP(port)), STUB_DATA]
    def sflat(): return [LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)]
    P = [(sflat(), "t2"), (sflat(), "t2")]
    names = ["f0", "f1"]
    for w, n, ld, st in (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ)):
        P.append(([LDQ(T1, 8, T0)] + sent(T3) + [ld(T3, 0, T1)] + sflat(), "t2"))
        names.append("r%d" % n)
        P.append(([LDQ(T1, 8, T0), LDQ(T3, 16, T0), st(T3, 0, T1)] + sflat(), "t2"))
        names.append("w%d" % n)
    a, g = dsession("stub%d" % lane, C, P, names)
    flip = lambda x, y: None if x is None or y is None else (x ^ y) & 0x10
    row("stub%d alive" % lane, "alive" if a else "dead", "alive", "CONTROL")
    row("stub%d live" % lane, hx(flip(g["f0"], g["f1"])), hx(0x10),
        "LIVENESS: two flat reads of 0x%x flip bit 4 -- the stub's access counter is present" % port)
    prev = "f1"
    for nm in names[2:]:
        n = int(nm[1:])
        row("stub%d %s" % (lane, nm), hx(flip(g[prev], g[nm])), hx(0x00),
            "(%d,%d) %s SP(0x%x): ONE access reaches the port (%s)"
            % (n, lane, "LOAD" if nm[0] == "r" else "STORE 0x5a..", port,
               "RD2" if nm[0] == "r" else "x_wfallthru, nonzero byte"))
        prev = nm
    print("")

#  4p `tailq_w' / 4q `tailq_r': the split-TAIL cells, widths 3/5/6/7 at LANE 0 (a tail always starts at a port 0 mod
#  0x20; here the 8042 data port 0x60).  `tailw' (4f) stores into an EMPTY queue, so a phantom read there changes nothing
#  -- WT6/WTsplit scored 111/111.  WRITE tails: one reply queued, 0xd1 (the next data write goes to output_byte), the
#  split STQ's tail forwards 0, and the flat status DIB must still be 1.  READ tails: two replies queued, the split LDQ's
#  tail pops ONE, DIB must still be 1.  Each phase drains the survivor with a flat data read.
C4p = [k0(FLAT(KBC_CMD)), KBC_SELFTEST, k0(FLAT(KBC_DAT)), KBC_WROUTPORT] + [k0(SP(0x5f) + o) for _, o in TAILHEADS]
def wrout(): return [LDQ(T1, 0, T0), LDQ(T2, 24, T0), STB(T2, 0, T1)]                # 0xd1 -> the command port
P4p = [(selftest() + kstatus(T4) + kpop(), "t4")]                                     # control: one reply queued
for i in range(len(TAILHEADS)):
    P4p.append((selftest() + wrout() + [LDQ(T1, 32 + 8 * i, T0), STQ(ZERO, 0, T1)] + kstatus(T4) + kpop(), "t4"))
a4p, g4p = dsession("tailq_w", C4p, P4p, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
row("tailq w alive", "alive" if a4p else "dead", "alive", "CONTROL")
row("tailq w ctl", hx(dibv(g4p["ctl"])), hx(0x01), "CONTROL: a queued reply sets DIB")
for h, _ in TAILHEADS:
    row("tailq w t%d" % (8 - h), hx(dibv(g4p["t%d" % (8 - h)])), hx(0x01),
        "(%d,0) STQ TAIL at 0x60: the queued reply survives the store (x_wfallthru at a tail width)" % (8 - h))
P4q = [(selftest() + selftest() + kpop() + kstatus(T4) + kpop(), "t4")]               # control: one of two left
for i in range(len(TAILHEADS)):
    P4q.append((selftest() + selftest() + [LDQ(T1, 32 + 8 * i, T0)] + sent(T3) + [LDQ(T3, 0, T1)]
                + kstatus(T4) + kpop(), "t4"))
a4q, g4q = dsession("tailq_r", C4p, P4q, ["ctl"] + ["t%d" % (8 - h) for h, _ in TAILHEADS])
row("tailq r alive", "alive" if a4q else "dead", "alive", "CONTROL")
row("tailq r ctl", hx(dibv(g4q["ctl"])), hx(0x01), "CONTROL: two replies queued, one flat pop -> one left")
for h, _ in TAILHEADS:
    row("tailq r t%d" % (8 - h), hx(dibv(g4q["t%d" % (8 - h)])), hx(0x01),
        "(%d,0) LDQ TAIL at 0x60 pops ONE of two replies (RD2 at a tail width pops both)" % (8 - h))
print("")

#  ---- SESSIONS 5-10: the six cells that ENDED THE HOST on HEAD, one process each -------------
#  Each cell gets its own process and its own `alive' row, so a reinstated exit is attributed to its
#  cell -- with ONE overlap (codex, pass 2): w13's round trip ALSO reads (1,3), so an exit keyed on the
#  (1,3) read alone ends both r13 and w13.  And a value row, because `alive' greens equally for a
#  decline (the C and A mutants), so the value is what separates the fix from them.
EXITS = [
  #  tag   consts                                              phases                                      names            rows (name, key, want-fn, note)
  ("r12", [k0(FLAT(UART_MSR)), k0(SP(UART_MSR))],
          [([LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
           ([LDQ(T1, 8, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3")],
          ["msr", "r12"],
          [("r12 byte", "r12", lambda g: g["msr"],
            "(1,2) LDBU MSR == flat MSR: was host death; kills C/A (sentinel)")]),
  ("r13", [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))],
          [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
             LDQ(T1, 16, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3")],
          ["r13"],
          [("r13 byte", "r13", lambda g: SCR_VALUE,
            "(1,3) LDBU SCR after a flat store of 0x5a: was host death; kills C/A")]),
  ("r23", [k0(FLAT(UART_SCR)), SCR_VALUE, k0(SP(UART_SCR))],
          [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1),
             LDQ(T1, 16, T0)] + sent(T3) + [LDWU(T3, 0, T1)], "t3")],
          ["r23"],
          [("r23 lane", "r23", lambda g: SCR_VALUE << 8,
            "(2,3) LDWU SCR -> position 1, paired with `r21 anchor': kills the clamp (position 0)")]),
  ("w12", [k0(SP(UART_MSR)), k0(FLAT(UART_MSR))],
          [(load_const(T3, 0x40) + [LDQ(T1, 0, T0), STB(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")],
          ["w12"],
          [("w12 lands", "w12", lambda g: 0x40 | MSR_FIXED,
            "(1,2) STB 0x40 -> MSR, flat readback: was host death; kills C/A (store dropped)")]),
  ("w13", [k0(SP(UART_SCR)), k0(FLAT(UART_SCR))],
          [(load_const(T3, 0x3c) + [LDQ(T1, 0, T0), STB(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
           ([LDQ(T1, 0, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")],
          ["w13", "w13rt"],
          [("w13 lands", "w13", lambda g: 0x3c,
            "(1,3) STB 0x3c -> SCR, flat readback: was host death; kills C/A and the unfolded write"),
           ("w13 roundtrip", "w13rt", lambda g: 0x3c,
            "SELF-COHERENCE: stb then ldbu at ONE sparse address returns what was stored")]),
  ("w23", [k0(SP(UART_SCR)), k0(FLAT(UART_SCR))],
          [(load_const(T3, 0x7e00) + [LDQ(T1, 0, T0), STW(T3, 0, T1),
            LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")],
          ["w23"],
          [("w23 lane", "w23", lambda g: 0x7e,
            "(2,3) STW 0x7e00 -> SCR forwards position 1 (as `w21 lane'): kills the clamp")]),
]
for tag, consts, phases, names, rws in EXITS:
    ax, gx = dsession(tag, consts, phases, names)
    row("%s alive" % tag, "alive" if ax else "dead", "alive",
        "was a host death on HEAD (`ofs > len'); kills the reinstated exit")
    for nm, key, wantf, note in rws:
        w = wantf(gx)
        row(nm, hx(gx[key]), hx(w), note)
    print("")

# ---------------------------------------------------------------- summary
#  Computed adjacent to the print on purpose: #516 shipped a probe whose numerator was counted
#  over an older row set while the denominator was evaluated at print time, and every row said
#  `ok' beside a summary that did not.
ok = sum(1 for _, o in rows if o)
retr = ",".join([t for t, r in (("base", r1), ("ofs2", r2), ("ofs3", r3)) if r] + DRETRIED)
print("")
print("LCAISALANE_RETRIED=%s" % (retr if retr else "none"))
print("LCAISALANE_RESULT=%d/%d" % (ok, len(rows)))
print("LCAISALANE_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCAISALANE_DONE")
sys.exit(0 if ok == len(rows) else 1)
