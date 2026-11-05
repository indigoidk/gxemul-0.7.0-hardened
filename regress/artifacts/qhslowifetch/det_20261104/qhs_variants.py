#!/usr/bin/env python3
"""qhs_variants.py -- the test-variant set for the qhslowifetch fix's detector (legs50/probe50_frozen.py, 50 rows), 2026-11-04.
  qhs_variants.py list                     the variant names, in table order
  qhs_variants.py apply <name> <in> <out>  write <in> with variant <name> applied (each edit asserted to occur ONCE; exit 3 if not)
  qhs_variants.py pretable                 the PRETABLE record (written BEFORE table 1 runs; its mtime proves the order)
The set is clause (b) -- the removed exit reinstated VERBATIM at the fixed site (B1) -- the ruling's wrong edits that can be built in
this arm (W2-W5; W1 is B1, W6 is the ISI lookup outside this function, W7-W9 need ROW 5's machine), and clause (d) -- each predicate
the edited lines depend on, within X(to_be_translated), weakened to the least-restrictive form that still reads like the same check
(D*).  Exact-string edits on cpu_ppc_instr.c.fix only; every backslash is chr(92)."""
import io
import sys

T = chr(9)
NL = chr(10)
BS = chr(92)

OPEN = T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {" + NL
A = T * 3 + "if (cpu->translation_readahead)" + NL + T * 4 + "return;" + NL
B = T * 3 + "if (cpu->pc != addr) {" + NL
BREF = B + T * 4 + "quick_pc_to_pointers(cpu);" + NL
C = (T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 4 + "return;" + NL +
     T * 3 + "}" + NL)
CHEAD = T * 3 + "if (!cpu->running) {" + NL + T * 4 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL
DD = (T * 3 + "if (cpu->cd.ppc.msr & PPC_MSR_ME) {" + NL + T * 4 + "ppc_exception(cpu, PPC_EXCEPTION_MC);" + NL + T * 4 + "return;" +
      NL + T * 3 + "}" + NL)
CHK = (T * 3 + "cpu->running = 0;" + NL + T * 3 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 3 + "return;" + NL + T * 2 + "}" + NL)
ELSE = T + "} else {" + NL + T * 2 + '/*  fatal("TRANSLATION MISS!' + BS + 'n");  */' + NL
HEAD_EXIT = (T * 3 + 'fatal("PPC to_be_translated(): "' + NL + T * 3 + '    "read failed: TODO' + BS + 'n");' + NL + T * 3 + "exit(1);" + NL +
             T * 3 + "/*  goto bad;  */" + NL)


def w5(s):
    a = s.index(A)
    assert s.count(A) == 1 and s.count(CHK) == 1
    b = s.index(CHK, a) + len(CHK) - len(T * 2 + "}" + NL)
    return s[:a] + T * 3 + ";" + NL + s[b:]


def d8(s):
    assert s.count(C) == 1 and s.count(DD) == 1
    return s.replace(C, "", 1).replace(DD, DD + C, 1)


S_TS = "T step: session text prompt pc srr0"
S_TC = "T cont: session text prompt pc srr0"
S_AG = "again: session text prompt pc srr0"
S_ME = "T me: session text pc srr0"
V = [
    ("B1_exit_head", [(OPEN, OPEN + HEAD_EXIT)],
     "%s; %s; %s; %s (= the HEAD leg)" % (S_TS, S_TC, S_AG, S_ME), "(b) HEAD's fatal()+exit(1) reinstated verbatim at the arm head"),
    ("W2_bare_ret", [(OPEN, OPEN + T * 3 + "return;" + NL)],
     "T step pc (0x2040004), T cont nonex (the loop), T me pc, again pc", "W2: a bare return at the arm head, no park"),
    ("W3_goto_bad", [(OPEN, OPEN + T * 3 + "goto bad;" + NL)],
     "T step unimpl, T cont unimpl, again unimpl", "W3: goto bad (the stop names the halt unimplemented)"),
    ("W4_isi_inv", [(C, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "ppc_exception(cpu, PPC_EXCEPTION_ISI);" + NL + T * 4 + "return;" + NL +
                     T * 3 + "}" + NL)],
     "srr0 + exc + pc in T step, T cont, again and T me", "W4: arm (c) invents an ISI instead of parking"),
    ("W5_dec_tail", w5,
     "T step unimpl or pc (and the same in the other -T sessions)", "W5: the arm emptied, the zeroed/uninitialised ib decoded"),
    ("D1_c_inv", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (cpu->running)"))],
     "T step/T cont/again chkstop (ME clear: the checkstop arm); T me pc srr0 exc (ME set: the machine check)",
     "(d) arm (c)'s test inverted"),
    ("D2_c_del", [(C, "")],
     "as D1", "(d) arm (c) deleted"),
    ("D3_c_nopark", [(C, T * 3 + "if (!cpu->running) {" + NL + T * 4 + "return;" + NL + T * 3 + "}" + NL)],
     "T step pc (0x2040004: next_ic was already past the slot)", "(d) arm (c) keeps its test, drops the park"),
    ("D4_b_inv", [(B, T * 3 + "if (cpu->pc == addr) {" + NL)],
     "again nonex only (the repeats re-enter: 6, not 2)", "(d) arm (b)'s test inverted: the -T halt refreshes next_ic to the slot"),
    ("D5_a_inv", [(A, T * 3 + "if (!cpu->translation_readahead)" + NL + T * 4 + "return;" + NL)],
     "as W2", "(d) arm (a)'s test inverted: a bare return on every non-readahead fetch"),
    ("D6_d_inv", [(T * 3 + "if (cpu->cd.ppc.msr & PPC_MSR_ME) {", T * 3 + "if (!(cpu->cd.ppc.msr & PPC_MSR_ME)) {")],
     "NONE -- arm (c) returns first on every -T session (disclosed: arm (d) is ROW 5's, pending X11)", "(d) arm (d)'s test inverted"),
    ("D7_dom_run", [(OPEN, T * 2 + "    sizeof(ib), MEM_READ, CACHE_INSTRUCTION) && cpu->running) {" + NL)],
     "as W5 (memory_rw cleared running before returning, so the arm is skipped)",
     "(d) the read's failure test conditioned on running (the dominating predicate, X -> X && Y)"),
    ("D8_c_below_d", d8,
     "T me pc srr0 exc only (ME set: the machine check now precedes the park; ME clear is unchanged)", "(d) arm (c) moved below arm (d)"),
    ("D9_mc_vec", [("ppc_exception(cpu, PPC_EXCEPTION_MC);", "ppc_exception(cpu, PPC_EXCEPTION_DSI);")],
     "NONE (disclosed: arm (d) unreachable here)", "(d) arm (d) delivers the wrong exception"),
    ("D10_chk_run", [(CHK, T * 3 + "cpu->cd.ppc.next_ic = &nothing_call;" + NL + T * 3 + "return;" + NL + T * 2 + "}" + NL)],
     "NONE (disclosed: the checkstop fallback is unreachable here)", "(d) the checkstop fallback leaves running set"),
    ("D11_b_noref", [(BREF, B)],
     "NONE (disclosed: arm (b) is reached on no measured session)", "(d) arm (b) drops its next_ic refresh"),
    ("D12_else_ra", [(ELSE, T + "} else if (!cpu->translation_readahead) {" + NL + T * 2 + '/*  fatal("TRANSLATION MISS!' + BS + 'n");  */' + NL)],
     "NONE (disclosed: no read-ahead reaches a failing fetch on pmppc)",
     "(d) the slow path's else conditioned on not read-ahead (the dominating page != NULL test, else -> else if)"),
    ("D13_c_me", [(CHEAD, CHEAD.replace("if (!cpu->running)", "if (!cpu->running && !(cpu->cd.ppc.msr & PPC_MSR_ME))"))],
     "T me pc srr0 exc only (the joint cell: -T halt x ME set)", "(d) arm (c) conditioned on ME clear (keep the guard, null its repair)"),
]

PRETABLE = NL.join([
    "PRETABLE -- qhslowifetch detector, test-variant table 1.  Written BEFORE the table runs (this file's mtime precedes table1/'s).",
    "Instrument: legs50/probe50_frozen.py (50 rows; -E pmppc unmodified).  Baseline: the round's post-fix working set",
    "(legs50/cpu_ppc_instr.c.fix + cpu_ppc.h.fix).  Floor legs measured first (legs50/SCORES.txt).",
    "",
    "SIBLING PARITY -- the fix's four arms and the fallback, by observable channel on this machine:",
    "  (a) read-ahead: return, touch nothing.        Reached on no pmppc session (no read-ahead reaches a failing fetch). N/A, disclosed.",
    "  (b) pc != addr: refresh next_ic, return.      Reached on no measured session (its own comment says so). N/A, disclosed.",
    "  (c) !running (-T): park on nothing_call.      Every -T session: pc, SRR0, the halt-report count, the three texts.",
    "  (d) MSR[ME]: machine check, vector 0x200.     Unreachable while (c) returns first; ROW 5 (another machine) is FILED.",
    "  fallback: checkstop text, running = 0, park.  Unreachable likewise.",
    "  The asymmetry that matters: (c) and the fallback PARK IDENTICALLY (same pc, SRR0, next_ic) and differ only by the checkstop text,",
    "  and MSR = 0 on every -T session measured -- so the chkstop rows are the one channel that sees (c) deleted or inverted, and the",
    "  ME-SET -T session (T me) is the one cell that sees (c) ordered below (d) or conditioned on ME.  Both were added for this reason.",
    "",
    "CLAIM -> ROW (each comment sentence of the arm asserting an observable):",
    "  'none may run this slot'                      -> unimpl and pc rows (T step, T cont, again)",
    "  'the slot stays TO_BE_TRANSLATED, so a later fetch of this address re-enters this arm' -> again nonex = 2 MEASURES THE OPPOSITE",
    "      for a step or continue after the halt (FINDING_D8.md): the sentence is owed rewording with the pass-2 text changes",
    "  '(a) ... Touch nothing, as bad: does'         -> no row (unreachable here; disclosed)",
    "  '(b) ... Reached on no measured session'      -> no row (a statement of absence; nothing to observe)",
    "  '(c) memory.c cleared running and printed the non-existant line' -> T step nonex, T cont nonex, T me nonex",
    "  '(c) No PowerPC exception is involved'        -> srr0 and exc rows in all four -T sessions",
    "  '(c) Park at this pc ... so the debugger shows the failing fetch' -> pc rows in all four -T sessions",
    "  '(d) a machine check (vector 0x200) when MSR[ME] is set and a checkstop when it is clear' -> no row here: ROW 5, FILED",
    "  '(d) SRR1 status bits are not modelled'       -> no row (a disclosure)",
    "",
    "GUARD FIELD vs BODY FIELD (and the partition each body induces):",
    "  (a) guard translation_readahead {0, set}; body reads nothing.  Set cell unreachable on pmppc.",
    "  (b) guard pc, addr {pc == addr, pc != addr}; body calls quick_pc_to_pointers (callee not walked).  != cell unreached.",
    "  (c) guard running {0, nonzero}; body writes next_ic.  running is written by memory.c (-T), the debugger and the fallback.",
    "  (d) guard msr & ME {clear, set}; body calls ppc_exception.  Both cells are driven on the -T route (T step/T cont/again: clear;",
    "      T me: set) -- the generating set for the ME bit at the floor cell; (d) itself still never runs on pmppc.",
    "  Dominating: page != NULL (else = the slow read); !memory_rw(...) (the failure test).  No operand-swap variant: no guarded body",
    "  reads a field other than its own guard's.",
    "",
    "CHANNEL per row group (the variant each kills and the observable that differs under it):",
    "  session/text/prompt (T step, T cont, again, T me) -- B1/W1: exit status, the fatal text, the debugger prompt",
    "  pc (T step, T cont, again, T me)                  -- W2, D3, D5: 0x2040004; W4: 0x400; T me under D1/D2/D8/D13: 0x200",
    "  srr0 + exc                                        -- W4 (ISI), and T me under D1/D2/D8/D13 (the machine check)",
    "  unimpl                                            -- W3 (bad:), W5/D7 (a decoded zero or garbage word)",
    "  chkstop (T step, T cont, again, T me)             -- D1, D2 with ME clear: the checkstop arm's text",
    "  T step/T cont/T me nonex                          -- W2/D5 (the loop prints on), and the -T route's own two/one",
    "  again nonex                                       -- D4 (re-entering repeats print 6, not 2)",
    "  isi/isi1 rows, ctl, neg, noT                      -- controls: no variant in this arm can reach the ISI lookup or the no-T route",
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
            out += "   %-13s %-62s red: %s%s" % (n, what[:62], pred, NL)
        sys.stdout.write(out)
    elif len(a) == 4 and a[0] == "apply":
        name, src, dst = a[1:]
        s = io.open(src, encoding="latin-1", newline="").read()
        f = dict((n, e) for n, e, _, _ in V)[name]
        if callable(f):
            try:
                s = f(s)
            except (AssertionError, ValueError) as e:
                print("MUTANT-TEXT-NOT-FOUND", name, e)
                sys.exit(3)
        else:
            for old, new in f:
                if s.count(old) != 1:
                    print("MUTANT-TEXT-NOT-FOUND", name, repr(old[:60]), s.count(old))
                    sys.exit(3)
                s = s.replace(old, new)
        io.open(dst, "w", encoding="latin-1", newline="").write(s)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
