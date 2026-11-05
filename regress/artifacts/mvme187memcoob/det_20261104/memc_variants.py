#!/usr/bin/env python3
"""memc_variants.py -- the test-variant set for the mvme187memcoob fix's detector (legs56/probe56_frozen.py, 56 rows), 2026-11-04.
  memc_variants.py list                     the variant names, in table order
  memc_variants.py apply <name> <in> <out>  write <in> with variant <name> applied (each edit asserted to occur ONCE; exit 3 if not)
  memc_variants.py pretable                 the PRETABLE record (written BEFORE table 1 runs; its mtime proves the order)
The set is clause (b) -- each removed defect reinstated VERBATIM at its site (B1 the memconf-store exit, B2 the default-arm exit, B3 the
indexed read before the switch) -- the reconciliation's enumerated wrong edits that can be built in this function (ACCEPT, FAULT,
no latch, one shared latch, a default-arm store, a broken fold or mis-split field read, the value dropped from the write notice), and
clause (d) -- each predicate the edited lines depend on, weakened within DEVICE_ACCESS(mvme187_memc).  Exact-string edits on
dev_mvme187.c.fix only; every backslash is chr(92)."""
import io
import sys

T = chr(9)
NL = chr(10)
BS = chr(92)

FOLD = T * 2 + "relative_addr &= ~0x100;" + NL
CTRL = T * 2 + "controller = 1;" + NL
SWITCH = T + "switch (relative_addr) {" + NL
CHIPREV = T * 2 + "odata = d->memcreg.memc_chiprev;" + NL
CNF_RD = T * 2 + "odata = d->memcreg.memc_memconf;" + NL
CNF_W = T * 2 + "if (writeflag == MEM_WRITE) {" + NL
LATCH_M = T * 3 + "if (!d->warned_memconf) {" + NL
SET_M = T * 4 + "d->warned_memconf = 1;" + NL
LATCH_D = T * 2 + "if (!d->warned_default) {" + NL
SET_D = T * 3 + "d->warned_default = 1;" + NL
DVAL = T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + 'fatal(": 0x%x", (int)idata);' + NL
RW = '"write to" : "read from"'
HEAD_CNF = (T * 3 + 'fatal("mvme187_memc: Write to relative_addr %i (controller %i) not yet"' + NL +
            T * 3 + '    " implemented!' + BS + 'n", (int)relative_addr, controller);' + NL + T * 3 + "exit(1);" + NL)
HEAD_DEF = (T * 2 + 'fatal("[ mvme187_memc: unimplemented %s offset 0x%x",' + NL +
            T * 2 + '    writeflag == MEM_WRITE? "write to" : "read from",' + NL +
            T * 2 + '    (int) relative_addr);' + NL + T * 2 + "if (writeflag == MEM_WRITE)" + NL +
            T * 3 + 'fatal(": 0x%x", (int)idata);' + NL + T * 2 + 'fatal(" ]' + BS + 'n");' + NL + T * 2 + "exit(1);" + NL)
HEAD_IDX = T + "odata = ((uint8_t*)&d->memcreg)[relative_addr];" + NL + NL
DEF_STORE = (T * 2 + "if (relative_addr < sizeof(d->memcreg)) {" + NL +
             T * 3 + "if (writeflag == MEM_WRITE)" + NL + T * 4 + "((uint8_t*)&d->memcreg)[relative_addr] = idata;" + NL +
             T * 3 + "odata = ((uint8_t*)&d->memcreg)[relative_addr];" + NL + T * 2 + "}" + NL)

V = [
    ("B1_cnf_exit", [(LATCH_M, HEAD_CNF + LATCH_M)],
     "R3 session pc lines cnf r2 7c r4 cnf line 7c line; wr cnf session prompt", "(b) the memconf store's fatal()+exit(1), verbatim"),
    ("B2_def_exit", [(LATCH_D, HEAD_DEF + LATCH_D)],
     "rd 0x0c/0x7c/0xff session+prompt; R3-R5, R7 sessions and their later rows", "(b) the default arm's fatal()+exit(1), verbatim"),
    ("B3_idx_read", [(SWITCH, HEAD_IDX + SWITCH)],
     "R3 7c r4 (reads the memconf latch byte: 1); asan reports on the sanitizer build", "(b) the indexed read before the switch, verbatim"),
    ("A_cnf_accept", [(CNF_W, CNF_W + T * 3 + "d->memcreg.memc_memconf = idata;" + NL)],
     "R3 cnf r2 (0x7, not 0x3)", "ACCEPT: the memconf store is kept"),
    ("F_def_fault", [(LATCH_D, T * 2 + "return 0;" + NL + LATCH_D)],
     "R4 pc and every R4 load; R3/R5/R7 pc; rd 0x0c/0x7c/0xff (a bus error instead of a decline)", "FAULT: the default arm fails the access"),
    ("D1_mlatch_inv", [(LATCH_M, LATCH_M.replace("!d->warned_memconf", "d->warned_memconf"))],
     "R3 lines (1), R3 cnf line", "(d) the memconf latch test inverted"),
    ("D2_mlatch_noset", [(SET_M, "")],
     "R3 lines (3), R3 no 0x5", "(d) the memconf latch never set"),
    ("D3_shared_latch", [(LATCH_M, LATCH_M.replace("warned_memconf", "warned_default")), (SET_M, SET_M.replace("warned_memconf", "warned_default"))],
     "R3 lines (1), R3 7c line", "(d) one shared latch for both categories"),
    ("D4_dlatch_inv", [(LATCH_D, LATCH_D.replace("!d->warned_default", "d->warned_default"))],
     "R3/R4/R5/R7 lines and line texts", "(d) the default latch test inverted"),
    ("D5_dlatch_noset", [(SET_D, "")],
     "R4 lines (4), R5 lines, R3 lines", "(d) the default latch never set"),
    ("D6_dlatch_ctrl", [(LATCH_D, T * 2 + "if (!d->warned_default || controller) {" + NL)],
     "R4 lines (2), R5 lines (2)", "(d) the default latch made per-controller (controller 1 always announces)"),
    ("D7_fold", [(FOLD, FOLD.replace("~0x100", "~0x80"))],
     "R6 100/104/108, ctl ctl1id r2; R4 10c/R5/R7 line texts", "(d) the fold mask narrowed"),
    ("D8_ctrl_drop", [(CTRL, "")],
     "R7 line text only (controller 0 named for a controller-1 access)", "(d) the controller number never set"),
    ("D9_chiprev_swap", [(CHIPREV, CHIPREV.replace("memc_chiprev", "memc_chipid"))],
     "R6 04/104, ctl chiprev r2", "mis-split field read: chiprev returns chipid"),
    ("D10_cnf_noread", [(CNF_RD, "")],
     "R6 08/108, R3 cnf r2, ctl memconf r2", "memconf's read arm loses its field read"),
    ("D11_cnf_on_read", [(CNF_W, CNF_W.replace("MEM_WRITE", "MEM_READ"))],
     "R6 lines (1), R3 lines, R3 cnf line", "(d) the memconf announce keyed on reads, not writes"),
    ("D12_def_store", [(LATCH_D, DEF_STORE + LATCH_D)],
     "R5 r2 (0x5a, not 0)", "a default-arm store kept and read back (backed accept)"),
    ("D13_def_noval", [(DVAL, "")],
     "R5 line text", "the write notice drops its value"),
    ("D14_rw_swap", [(RW, '"read from" : "write to"')],
     "R4, R5, R7 line texts", "(d) the notice's direction swapped"),
]

PRETABLE = NL.join([
    "PRETABLE -- mvme187memcoob detector, test-variant table 1.  Written BEFORE the table runs (this file's mtime precedes table1/'s).",
    "Instrument: legs56/probe56_frozen.py (56 rows; -E mvme88k -e mvme187 -M 64 unmodified).  Baseline: the round's post-fix working set",
    "(legs56/dev_mvme187.c.fix).  Floor legs measured first (legs56/SCORES.txt).  R1/R2 (the sanitizer builds) are a separate leg set.",
    "",
    "SIBLING PARITY -- the fix's arms, by observable channel:",
    "  chipid / chiprev: each reads its own field (was: the indexed read, then break).  Channels: R6 00/04/100/104 values, the ctl rows.",
    "  memconf: reads its field; a store is not kept and announced once per device (was: exit).  Channels: R3 cnf r2, R3 lines/texts.",
    "  default: reads 0, a store is not kept, announced once per device with the direction and (for a store) the value (was: exit).",
    "      Channels: R4 values/pc/lines/text, R5 r2/lines/text, R7 text.",
    "  The asymmetry: the memconf notice and the default notice have SEPARATE latches -- R3 is the one session that drives both.",
    "",
    "CLAIM -> ROW (each comment sentence of the diff asserting an observable):",
    "  'DEVINIT memsets this struct, so they start at 0'          -> R3/R4/R5/R7 lines (each session's first access announces)",
    "  'Controller 1 ... presents the same register image'         -> R6 100/104/108, ctl ctl1id",
    "  'The number is reported in the notices below'               -> R7 line text (ADDED for this sentence: R3-R5 latch every controller-1",
    "                                                                  access silent, so no other row could see the number)",
    "  'No indexed read remains: each arm reads its own field'     -> R6 values; the asan reports row on the sanitizer builds (R1/R2)",
    "  'a store has nothing to change and is not kept'             -> R3 cnf r2 (3 after a store of 7)",
    "  'Announced once per device; it used to end the emulator'    -> R3 lines, R3 no 0x5; every session row's exit status",
    "  'A read returns 0'                                          -> R4 values, R7 r2",
    "  'a write is not kept'                                       -> R5 r2",
    "",
    "GUARD FIELD vs BODY FIELD (and the partition each body induces):",
    "  fold: relative_addr & 0x100 {clear, set}; body writes controller and relative_addr.  Both cells: R6 (0x0xx and 0x1xx), R4 10c, R7.",
    "  memconf store: writeflag {read, write}; body reads warned_memconf, idata.  Both: R3 (stores) and R6 08 (a read, no notice).",
    "  warned_memconf {0, 1}: both cells in R3 (the first and the second store).  warned_default {0, 1}: both cells in R4 (first, later).",
    "  default notice: writeflag {read, write} picks the direction text and the value print: R4/R7 (read), R5 (write).",
    "  controller {0, 1} at a notice: R3-R5 (0), R7 (1).",
    "",
    "CHANNEL per row group (the variant each kills and the observable that differs under it):",
    "  session/prompt rows and later rows of a session  -- B1, B2 (exit status; the rows after the exit read `none`)",
    "  R3 cnf r2                                        -- A_cnf_accept (7), D10 (0); B1",
    "  R3 7c r4                                         -- B3 (the over-read returns the memconf latch byte, 1)",
    "  R3/R4/R5/R7 lines and line texts                 -- D1-D6, D11, D13, D14, D8 (R7 only)",
    "  R4 values and pc                                 -- F_def_fault (a bus error: the load does not retire)",
    "  R5 r2                                            -- D12 (0x5a read back)",
    "  R6 values                                        -- D7, D9, D10",
    "  asan reports                                     -- B3 on the sanitizer builds only (a plain build reads garbage silently)",
    "",
    "VARIANTS (name, what, predicted red rows):",
    ""])


def main():
    a = sys.argv[1:]
    if a == ["list"]:
        print(" ".join(n for n, _, _, _ in V))
    elif a == ["pretable"]:
        out = PRETABLE
        for n, _, pred, what in V:
            out += "   %-15s %-60s red: %s%s" % (n, what[:60], pred, NL)
        sys.stdout.write(out)
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        for old, new in dict((n, e) for n, e, _, _ in V)[name]:
            if s.count(old) != 1:
                print("MUTANT-TEXT-NOT-FOUND", name, repr(old[:60]), s.count(old))
                sys.exit(3)
            s = s.replace(old, new)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
