#!/usr/bin/env python3
"""m88kexcdeliver -- rung-3 witness AND detector: does the m88k exception core DELIVER a trap-like
exception (vector entry reached, shadow registers right, machine still running), or stop the machine?

`cpu_m88k.c`'s exception switch marks only RESET / INTERRUPT / INSTRUCTION_ACCESS / DATA_ACCESS
`implemented`; every other vector below M88K_EXCEPTION_USER_TRAPS_START falls to a fallback that
prints `unimplemented vector=0x%03x` and sets `running = false` on EVERY guest CPU.  The vector-
specific tail switch then has a `default:` that stops THIS cpu with `internal error` -- so a fix
needs BOTH `implemented = true` AND a tail arm (the naive one-site fix was MEASURED to halt, pass 1).
Real hardware delivers VBR + 8*vector (MC88100 UM Table 6-1, mc88100.txt:8524-8538) and the guest OS
turns it into a signal; rte resumes at SNIP (:8983-8985), the destination register is unchanged
(6.6 :9305-9308; 6.8.3 :10300-10305).

Cold-debugger probe on the COMMITTED `testm88k` machine (no machine or device edits).  Per row: a
guest program at 0x10000 planted with `put w` (liveness marker `addu r9,r0,r10` first), registers
seeded with `rN=`, a `br .` (c0000000) planted at every vector entry so a delivered exception spins
rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg` and `reg 0,0`.

  row        program (after the marker at 0x10000)                 raise                     entry
  div0       divu r2,r3,r0            f4436800                    ILLEGAL_INTEGER_DIVIDE 8  0x40
  ovf        add  r2,r3,r4 (7fffffff+1) f4437004                  INTEGER_OVERFLOW 9        0x48
  misalign   ld   r2,r3,0 (r3 odd)    14430000 (major opcode 5)   MISALIGNED_ACCESS 4       0x20
  bounds     tb1  0,r3,7 (r3=1)       f003d807  supervisor trap   BOUNDS_CHECK 7            0x38
  priv       stcr r3,cr1 (r3=0x2: MODE clear) 80038023; ldcr r2,cr1 80404020   PRIVILEGE 6  0x30
  privtb     stcr r3,cr1; tb1 0,r4,8 (f004d808) in user mode      PRIVILEGE 6               0x30
  unimpl     stcr r3,cr1; prom_call f400fc92 in user mode         UNIMPLEMENTED_OPCODE 5    0x28
  error      div0 whose handler at 0x40 is a misaligned ld: the 2nd fault with SFRZ set re-routes
             to ERROR 10                                                                    0x50
  dslot      br.n +16 (c4000004) with divu r2,r3,r0 in its delay slot -> the else-arm of the
             delay-slot branch (SNIP = pc+4 = 0x1000c, SFIP = delay_target = 0x10014 -- two
             DIFFERENT numbers; with br.n +8 both were 0x1000e and the SFIP channel was vacuous)  ILLEGAL_INTEGER_DIVIDE 0x40
             *** THIS ROW PINS THE ELSE-ARM AS IMPLEMENTED, NOT AS THE MANUAL'S CONTRACT.  Table 6-3 (shadows copy
             XIP/NIP/FIP: for a fault in the delay slot of a taken br.n, NIP = target, FIP = target+4) and X(rte)'s
             `fip != nip + 4' arm say the else-arm returns WRONG (codex, grok, pass 2: the fallthrough executes
             before the target).  Pre-existing, out of this diff's scope, filed as m88kdslotshadow; when that round
             lands this row is RE-PINNED FIRST (oracle-correction rule: re-pin, measure HEAD red, then fix). ***
  errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
             only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
             switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
  misaligntb/unimpltb/div0tb/ovftb   tb1 0,r3,{4,5,8,9} (f003d804/05/08/09), supervisor: the TRAP
             ROUTE into switch 1 for the four classes whose other rows arrive by instruction --
             `if (!is_trap) implemented = true' escapes those rows (grok, deepseek, pass 2)  0x20/0x28/0x40/0x48
  vbrtb      stcr r5,cr7 (800580e5, r5=0x2000) then tb1 0,r3,7: the vector table RELOCATED -> entry
             0x2038, not 0x38.  Every other row runs with VBR == 0, so `pc = 8*vector' (VBR dropped)
             was a 10/10 escape (Opus, pass 2).  The one ANCHORED row: it alone reds if the table moves.  0x2038
  trapfrozen div0 whose handler at 0x40 is tb1 0,r3,7 (r3=0x11): a TRAP with SFRZ already set is NOT
             re-routed to ERROR (UM :8633-8636, 6.10 :10613-10614) -- it delivers to 0x38 with the
             shadows still frozen.  `if (!is_trap)' -> `if (true)' was a 10/10 escape (Opus, pass 2)  0x38
  privsuptb  tb1 0,r3,6 (f003d806) in SUPERVISOR mode: the trap route into PRIVILEGE_VIOLATION.  privtb is
             NOT that route -- the user-mode filter in X(tb0) raises PRIVILEGE with is_trap == 0, so
             `implemented = !is_trap' on the PRIVILEGE arm left priv AND privtb green (codex, glm: pass 2)  0x30
  usertb     tb1 0,r3,128 (f003d880): the first USER trap vector, delivered by the pre-existing code to
             0x400.  Pins the tail switch's `< USER_TRAPS_START' guard: `<=' sends 128 into the tail
             default and stops the cpu (codex's one-character escape, pass 2)                       0x400
  resid50    tb1 0,r3,50 (f003d832): a residual vector.  EXPECTED RESULT = HALT (the fallback, by design).
             Negative control: the shipped form must NOT deliver it (rejected D4 would)             (0x190)
  sfu1h      div0 whose handler at 0x40 is a LEGAL divu r6,r5,r4: with SFD1 set the divide raises
             SFU1_PRECISE (114), which halts at the FALLBACK (it runs before the SFRZ re-route).  EXPECTED
             RESULT = HALT naming vector 0x072, with pc == 0x40 (the first delivery happened -- on HEAD the
             first divu halts on vector 0x008, not this row's 0x072, and it reads STOP).  With the fallback off (M_DELIVERALL) the
             nested SFU1 is RE-ROUTED TO ERROR (0x50), not delivered to 0x390: the row reds as STOP.  So it
             pins 'SFU1 inside a handler still halts', NOT 'SFU1 is not delivered to its vector' -- the
             first-exception SFU1 route is row m88kexcsfu1's (grok, kimi, pass 3)                    (0x390)
  udiv0      stcr r3,cr1 (r3=0x2: user mode) then divu r2,r3,r0: the fallback comment's own sentence,
             'one user-mode divu by zero ended the emulation', measured literally; also pins that user mode
             with SFD1 CLEAR yields vector 8, not SFU1 (the m88kexcsfu1 boundary)              ILLEGAL_INTEGER_DIVIDE 0x40
  indclr     stcr r5,cr1 (r5=0x80000000: MODE only, IND CLEAR) then add 7fffffff+1: the exception path must
             SET IND (PSR 0x8000000b from 0x80000000; EPSR 0x80000000).  Every other row's pre-fault PSR already
             has IND, so `| M88K_PSR_IND' was unobservable -- the carry shape again (grok, codex, pass 3)     0x48
  umisalign  stcr r5,cr1 (r5=0x2: user mode) then ld r2,r3,0 with r3 odd: MISALIGNED from USER mode
             (a MODE-conditioned `implemented' on that arm swept 23/23 -- Opus, pass 4)                    0x20
  uovf       stcr r5,cr1 (user mode) then add 7fffffff+1: OVERFLOW from USER mode -- the measured
             M_OVFSUPONLY escape (a user-mode overflow ended the emulation again, 23/23)               0x48
  errovf     div0 whose handler at 0x40 is add 7fffffff+1: a NON-TRAP fault of a SECOND class with
             SFRZ set -> re-routed to ERROR with frozen shadows (M_SFRZMIS -- `!is_trap && vector ==
             MISALIGNED' on the re-route -- swept 23/23 because `error' was that cell's only row)      0x50
  errdiv0    div0 whose handler is stcr r5,cr1 (r5=0x80000003: SFD1 CLEAR, SFRZ kept) then divu by zero:
             a frozen non-trap DIV0 -> ERROR (with SFD1 set the same divu raises SFU1 instead: sfu1h)     0x50
  errpriv    div0 whose handler is stcr r5,cr1 (r5=0x00000003: USER mode, SFRZ kept) then ldcr: a frozen
             non-trap PRIVILEGE -> ERROR (Fable, pass 4: the {SFRZ, !is_trap} x {class} closure)        0x50
  errunimpl  div0 whose handler is stcr r5,cr1 (user mode, SFRZ kept) then prom_call: a frozen non-trap
             UNIMPLEMENTED -> ERROR.  BOUNDS and ERROR have no non-trap route (trapfrozen covers the trap)  0x50
  ovfc       stcr r5,cr1 (80058025, r5=0x90000002: C set) then add 7fffffff+1: the carry bit must
             SURVIVE the exception path (UM 6.6) -> PSR 0x9000000b, EPSR 0x90000002.  Every other
             row's pre-fault C is 0, so PSR == 0x8000000b pinned 'C not set', never 'C unchanged'  0x48
  live       divu r2,r3,r4  (r3=0x60, r4=0x10) -> r2 = 6           none      LIVENESS control
  attrib     divu r2,r3,r4  (r3=0x10, r4=0x10) -> r2 = 1           none      ATTRIBUTION control
  selftest   no program: `reg 0,0` at reset must parse PSR == 0x80000002 (the CR parse works)

RESULT per fault row (the classifier tests the STOP channel before pc, deliberately: the naive fix
sets pc = entry and THEN stops, so pc alone cannot tell it from delivery):
  HALT       `unimplemented vector=` printed AND the machine stopped (both observed, pass 3); an
             expected-HALT row (resid50, sfu1h) must also see ITS vector named in the diagnostic
  TAILHALT   `internal error` printed and the machine stopped (the naive fix's shape)
  STOP       the machine stopped for another reason (e.g. a wrong vector base landed in zeros)
  BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed, or
             (bad=level) the transcript carried an `exception <CLASS>' line: the class printed at ERROR
             level, which the fork's default WARNING verbosity shows and INFO does not (kills M_LEVEL)
  (rows resid50 and sfu1h EXPECT HALT: the fallback stopping the machine is the correct answer there)
  DELIVER    entry breakpoint fired, machine running, and every assert holds:
             pc == entry, SXIP == fault_pc|V, SNIP, SFIP, PSR == 0x8000000b (SFRZ|IND|SFD1|MODE),
             EPSR == the pre-fault PSR (0x80000002 supervisor rows; 0x00000002 user-mode rows),
             r2 unchanged (0xdeadbeef)
  NOSTART    the liveness marker never ran
Controls print DONE (r2 == the expected quotient, machine running) or a failure word.

Output: one `M88KEXC_ROW=<name> RESULT=<word> ...` line per row, `M88KEXC_RESULT=<delivered>/<fault rows>`,
`M88KEXC_SELFTEST=OK|FAIL`, `M88KEXC_DONE`.  Set M88KEXC_VERBOSE=1 for transcripts.

CONTRACT (clause e): catches a class returned to the fallback (HALT) by either route (instruction rows
and the *tb trap rows); a class reaching the tail default (TAILHALT); a wrong vector SCALING (M_VEC4,
M_VEC7: STOP) and a DROPPED vector base (vbrtb: STOP); a stale SXIP/SNIP/SFIP; a wrong PSR, including a
cleared carry (ovfc); a dropped IND (indclr); the debugmsg LEVEL regression to ERROR/WARNING (bad=level on any
delivered row: those print at the post-startup WARNING floor, INFO and DEBUG do not -- so exact INFO is NOT pinned,
only 'not ERROR/WARNING' -- M_LEVEL; codex, pass 3); a skipped EPSR save; a skipped supervisor switch (the user-mode rows: EPSR MODE
clear vs PSR MODE set); a MODE-conditioned `implemented' on any class that user mode can raise ({class} x
{MODE} closure: DIV0 udiv0, PRIVILEGE priv/privtb, UNIMPLEMENTED unimpl, MISALIGNED umisalign, OVERFLOW uovf;
BOUNDS and ERROR have no user-mode route -- a user tb1 naming them raises PRIVILEGE, and every handler runs
supervisor); a class-conditioned SFRZ re-route ({SFRZ set, !is_trap} x {class}: MISALIGNED error, OVERFLOW errovf,
DIV0 errdiv0 -- the handler clears SFD1 first, with it set the divu raises SFU1 instead (sfu1h) --, PRIVILEGE errpriv
and UNIMPLEMENTED errunimpl -- the handler drops to user mode keeping SFRZ; BOUNDS and ERROR have no non-trap route,
the frozen TRAP is trapfrozen); a wrong return address; the delay-slot else-arm's SFIP source (dslot, +16
geometry); a trap re-routed to ERROR while frozen (trapfrozen); a written destination.  Does NOT catch:
fcr2/fcr4/fcr5; scoreboard (SSBR) bits; DMT contents; the post-delivery
`cpu->delay_slot' write on the NON-delay path (M_DELAYALWAYS: needs a second UNFROZEN exception -- filed);
vectors 0..3's tail arms (no row: M_TAILOFF -- filed); vectors 11..113 and 116..127 (fallback halts by
design); SFU1 (114/115, row m88kexcsfu1); `implemented = is_trap' on BOUNDS/ERROR (EQUIVALENT today: no
instruction raises 7 or 10 -- becomes live when tbnd lands, row m88ktbnd).
"""
import os, pty, re, select, struct, sys, time

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxsec-build/gxemul"
CODE = 0x10000
DATA = 0x20000
XIP_V = 0x2
PSR_RESET = 0x80000002          # MODE | IND (cpu_m88k.c: cr[PSR] = M88K_PSR_MODE | M88K_PSR_IND)
PSR_EXC = 0x8000000b            # MODE | SFD1 | IND | SFRZ after the common path
PSR_USER = 0x00000002           # IND only: what the user-mode rows write via stcr
PSR_FRZSUP = 0x80000003         # MODE | IND | SFRZ, SFD1 CLEAR: a frozen handler that wants its divu to raise DIV0, not SFU1
PSR_FRZUSER = 0x00000003        # IND | SFRZ, MODE CLEAR: a frozen handler dropping to user mode (PRIVILEGE / UNIMPLEMENTED routes)

def tri(sub, d, s1, s2):
    return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2

MARK = tri(0x60, 9, 0, 10)                       # addu r9,r0,r10  -> r9 = 0x12345678 (liveness)
SELF = 0xc0000000                                # br . (disp 0)
DIVU_R2_R3_R0 = tri(0x68, 2, 3, 0)               # f4436800
DIVU_R2_R3_R4 = tri(0x68, 2, 3, 4)               # f4436804
DIVU_R6_R5_R4 = tri(0x68, 6, 5, 4)               # f4c56804 -- a LEGAL divide inside a handler: SFD1 is set there, so X(divu) raises
                                                 #   SFU1_PRECISE (114) before it looks at the divisor -> the fallback must still HALT
ADD_R2_R3_R4 = tri(0x70, 2, 3, 4)                # f4437004
LD_R2_R3_0 = 0x14000000 | (2 << 21) | (3 << 16)  # 14430000 (major opcode 5, ld)
TB1_0_R3_7 = 0xf003d807                          # tb1 0,r3,7   (computed vector 7, supervisor)
TB1_0_R4_8 = 0xf004d808                          # tb1 0,r4,8
TB1_0_R3_10 = 0xf003d80a
TB1_0_R3_4 = 0xf003d804                          # tb1 0,r3,4   -- a supervisor trap naming MISALIGNED_ACCESS (4) directly
TB1_0_R3_5 = 0xf003d805                          # tb1 0,r3,5   -- naming UNIMPLEMENTED_OPCODE (5)
TB1_0_R3_8 = 0xf003d808                          # tb1 0,r3,8   -- naming ILLEGAL_INTEGER_DIVIDE (8)
TB1_0_R3_9 = 0xf003d809                          # tb1 0,r3,9   -- naming INTEGER_OVERFLOW (9)
TB1_0_R3_6 = 0xf003d806                          # tb1 0,r3,6   -- naming PRIVILEGE_VIOLATION (6): the user-mode tb1 filter raises
                                                 #   PRIVILEGE with is_trap == 0 (cpu_m88k_instr.c X(tb0)), so privtb is NOT the trap route
TB1_0_R3_128 = 0xf003d880                        # tb1 0,r3,128 -- the first USER trap vector: delivered by the pre-existing code (entry 0x400)
TB1_0_R3_50 = 0xf003d832                         # tb1 0,r3,50  -- a RESIDUAL vector (11..113): must still HALT (negative control vs D4)
#  The four *tb rows are the TRAP ROUTE into switch 1 for the classes whose other rows arrive by INSTRUCTION
#  (is_trap == 0).  Pass-2 seats (grok, deepseek, independently) predicted `if (!is_trap) implemented = true;'
#  escapes the instruction rows for MISALIGNED/UNIMPL/DIV0/OVF; these rows are the ones that redden it (M_ISTRAP).
                         # tb1 0,r3,10  (a supervisor trap naming vector 10 = ERROR directly)
STCR_R3_CR1 = 0x80038023                         # stcr r3,cr1 (PSR)
STCR_R5_CR1 = 0x80058025                         # stcr r5,cr1 (PSR)  -- same format: 0x80000000 | S1<<16 | 0x8000 | CR<<5 | S1
STCR_R5_CR7 = 0x800580e5                         # stcr r5,cr7 (VBR)
PSR_CARRY = 0x90000002                           # MODE | C | IND: the ovfc row's pre-fault PSR (C = bit 28, UM 6.6 'carry bit unchanged')
PSR_INDCLR = 0x80000000                          # MODE only, IND CLEAR: the indclr row's pre-fault PSR -- every other row starts with IND
                                                 #   already set, so `| M88K_PSR_IND' in the exception-path PSR write was unobservable (grok, codex, pass 3)
VBR_TEST = 0x2000                                # the vbrtb row relocates the vector table here (OpenBSD relocates its own)
LDCR_R2_CR1 = 0x80404020                         # ldcr r2,cr1
PROM_CALL = 0xf400fc92                           # M88K_PROM_INSTR
BR_N_PLUS8 = 0xc4000002
BR_N_PLUS16 = 0xc4000004                         # br.n +16: delay_target (slot+8) != slot_pc+4, so SNIP and SFIP are DIFFERENT numbers                          # br.n +2 words

V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR = 4, 5, 6, 7, 8, 9, 10
V_SFU1 = 114
V_USER0 = 128
V_RESID = 50
VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR, V_SFU1, V_USER0, V_RESID)

# name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
ROWS = [
    ("div0",     [DIVU_R2_R3_R0],               {"r3": 0x10},                    V_DIV0,     0x10004, PSR_RESET, None),
    ("ovf",      [ADD_R2_R3_R4],                {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10004, PSR_RESET, None),
    ("misalign", [LD_R2_R3_0],                  {"r3": DATA + 1},                V_MISALIGN, 0x10004, PSR_RESET, None),
    ("bounds",   [TB1_0_R3_7],                  {"r3": 1},                       V_BOUNDS,   0x10004, PSR_RESET, None),
    ("priv",     [STCR_R3_CR1, LDCR_R2_CR1],    {"r3": PSR_USER},                V_PRIV,     0x10008, PSR_USER,  None),
    ("privtb",   [STCR_R3_CR1, TB1_0_R4_8],     {"r3": PSR_USER, "r4": 1},       V_PRIV,     0x10008, PSR_USER,  None),
    ("unimpl",   [STCR_R3_CR1, PROM_CALL],      {"r3": PSR_USER},                V_UNIMPL,   0x10008, PSR_USER,  None),
    ("error",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": DATA + 1},    V_ERROR,    0x10004, PSR_RESET,
                 [0x14000000 | (6 << 21) | (5 << 16)]),       # handler at 0x40: ld r6,r5,0 with r5 odd -> 2nd fault
    ("dslot",    [BR_N_PLUS16, DIVU_R2_R3_R0],  {"r3": 0x10},                    V_DIV0,     0x10008, PSR_RESET, None),
    ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
    ("misaligntb", [TB1_0_R3_4],                {"r3": 1},                       V_MISALIGN, 0x10004, PSR_RESET, None),
    ("unimpltb", [TB1_0_R3_5],                  {"r3": 1},                       V_UNIMPL,   0x10004, PSR_RESET, None),
    ("div0tb",   [TB1_0_R3_8],                  {"r3": 1},                       V_DIV0,     0x10004, PSR_RESET, None),
    ("ovftb",    [TB1_0_R3_9],                  {"r3": 1},                       V_OVF,      0x10004, PSR_RESET, None),
    ("vbrtb",    [STCR_R5_CR7, TB1_0_R3_7],     {"r3": 1, "r5": VBR_TEST},       V_BOUNDS,   0x10008, PSR_RESET, None),
    ("trapfrozen", [DIVU_R2_R3_R0],             {"r3": 0x11},                    V_BOUNDS,   0x10004, PSR_RESET,
                 [TB1_0_R3_7]),                               # handler at 0x40: tb1 0,r3,7 with SFRZ set -> a TRAP is not re-routed to ERROR
    ("ovfc",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_CARRY}, V_OVF, 0x10008, PSR_CARRY, None),
    ("indclr",   [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_INDCLR}, V_OVF, 0x10008, PSR_INDCLR, None),
    ("umisalign", [STCR_R5_CR1, LD_R2_R3_0],    {"r3": DATA + 1, "r5": PSR_USER}, V_MISALIGN, 0x10008, PSR_USER,  None),
    ("uovf",     [STCR_R5_CR1, ADD_R2_R3_R4],   {"r3": 0x7fffffff, "r4": 1, "r5": PSR_USER}, V_OVF, 0x10008, PSR_USER,  None),
    ("errovf",   [DIVU_R2_R3_R0],               {"r3": 0x7fffffff, "r4": 1},     V_ERROR,    0x10004, PSR_RESET,
                 [ADD_R2_R3_R4]),                             # handler at 0x40: an OVERFLOW (non-trap) with SFRZ set -> re-routed to ERROR
    ("errdiv0",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZSUP},  V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, DIVU_R2_R3_R0]),               # handler: clear SFD1 (SFRZ kept), divu by zero -> DIV0 frozen -> ERROR
    ("errpriv",  [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, LDCR_R2_CR1]),                 # handler: drop to USER mode (SFRZ kept), ldcr -> PRIVILEGE frozen -> ERROR
    ("errunimpl", [DIVU_R2_R3_R0],              {"r3": 0x10, "r5": PSR_FRZUSER}, V_ERROR,    0x10004, PSR_RESET,
                 [STCR_R5_CR1, PROM_CALL]),                   # handler: drop to USER mode (SFRZ kept), prom_call -> UNIMPLEMENTED frozen -> ERROR
    ("privsuptb", [TB1_0_R3_6],                 {"r3": 1},                       V_PRIV,     0x10004, PSR_RESET, None),
    ("udiv0",    [STCR_R3_CR1, DIVU_R2_R3_R0],  {"r3": PSR_USER},                V_DIV0,     0x10008, PSR_USER,  None),
    ("usertb",   [TB1_0_R3_128],                {"r3": 1},                       V_USER0,    0x10004, PSR_RESET, None),
    ("resid50",  [TB1_0_R3_50],                 {"r3": 1},                       V_RESID,    0x10004, PSR_RESET, None),
    ("sfu1h",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": 0x60, "r4": 0x10}, V_SFU1, 0x10004, PSR_RESET,
                 [DIVU_R6_R5_R4]),                             # handler at 0x40: a legal divu with SFD1 set -> SFU1 (114) -> fallback HALT
    ("live",     [DIVU_R2_R3_R4],               {"r3": 0x60, "r4": 0x10},        None,       None,    None,      None),
    ("attrib",   [DIVU_R2_R3_R4],               {"r3": 0x10, "r4": 0x10},        None,       None,    None,      None),
]
EXPECT_R2 = {"live": 6, "attrib": 1}
VBR_OF = {"vbrtb": VBR_TEST}                     # rows that relocate the vector table; every other row runs with VBR == 0
#  NEGATIVE CONTROLS: rows whose CORRECT result is the fallback HALT.  They pin the boundary the diff keeps on purpose --
#  vectors 11..113/116..127 and SFU1 (114/115) still stop the machine -- and separate the shipped D1 form from the rejected
#  D4 (tail-default-delivers) and from delivering SFU1 (row m88kexcsfu1).  A mutant that delivers them turns these rows RED.
EXPECT_RESULT = {"resid50": "HALT", "sfu1h": "HALT"}
PSR_WANT = {"ovfc": 0x9000000b}                  # MODE | C | SFD1 | IND | SFRZ: carry PRESERVED through the exception path
#  indclr wants the default PSR_EXC (0x8000000b): IND was CLEAR before the fault and must be SET by the exception path;
#  EPSR keeps the pre-fault 0x80000000.  A write that drops `| M88K_PSR_IND' leaves 0x80000009 -> bad=psr.
EXPECT_VECTOR = {"resid50": 0x032, "sfu1h": 0x072}   # the vector the fallback diagnostic must NAME for an expected-HALT row

class Sess:
    def __init__(self):
        stub = "/tmp/gx_m88k_exc_%d.bin" % os.getpid()
        with open(stub, "wb") as f:
            f.write(struct.pack(">I", 0xf4005800))          # or r0,r0,r0 so the machine constructs
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(BIN, [BIN, "-V", "-E", "testm88k", "-M", "64", "0x10000:%s" % stub])
            os._exit(127)
        self.buf = ""
    def rd(self, t=0.4):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return True
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        self.buf += d.decode("latin1", "replace")
        return True
    def wait_prompt(self, mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False
    def send(self, sx, timeout=30):
        mark = len(self.buf)
        b = (sx + "\n").encode("latin1"); n = 0
        while n < len(b):
            n += os.write(self.fd, b[n:])
        self.wait_prompt(mark, timeout)
        return mark
    def cr(self, name):
        m = self.send("reg 0,0")
        mm = re.search(r"(?<![A-Z])%s=0x([0-9a-f]{8})" % name, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def gpr(self, n):
        m = self.send("reg")
        mm = re.search(r"r%-2d\s*=\s*0x([0-9a-f]{8})" % n, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def pc(self):
        m = self.send("reg")
        mm = re.search(r"pc\s*=\s*0x([0-9a-f]{8})", self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def close(self):
        try:
            os.write(self.fd, b"quit\n"); time.sleep(0.3); os.kill(self.pid, 9); os.waitpid(self.pid, 0)
        except Exception:
            pass

def fmt(v):
    return ("0x%08x" % v) if isinstance(v, int) else str(v)

def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0):
    s = Sess()
    if not s.wait_prompt(0, 60):
        s.close(); return dict(result="NOBOOT")
    vbr = VBR_OF.get(name, 0)
    entry = (vbr + 8 * vector) if vector is not None else None
    words = [MARK] + prog + [SELF]
    for i, w in enumerate(words):
        s.send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    for base in sorted({0, vbr}):                       # every entry spins unless a handler is planted (both tables if relocated)
        for v in VECTORS:
            s.send("put w 0x%x, 0x%08x" % (base + 8 * v, SELF))
    if entry is not None:
        s.send("put w 0x%x, 0x%08x" % (entry, SELF))
    if handler:
        for i, w in enumerate(handler):
            s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * i, w))
        s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * len(handler), SELF))
    s.send("put w 0x%x, 0x%08x" % (DATA, 0x0badf00d))
    for r, v in regs.items():
        s.send("%s=0x%x" % (r, v))
    s.send("r10=0x12345678"); s.send("r2=0xdeadbeef")
    if vector is not None:
        s.send("breakpoint add 0x%x" % entry)
    s.send("pc=0x%x" % CODE)
    mark = len(s.buf)
    os.write(s.fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        s.rd(0.3)
        if s.buf[mark:].rstrip().endswith("GXemul>"):
            break
    if not s.buf[mark:].rstrip().endswith("GXemul>"):
        os.write(s.fd, b"\x03"); s.wait_prompt(len(s.buf), 15)
    tr = s.buf[mark:]
    #  HALT is the fallback's diagnostic AND the machine-stopped observation (codex, pass 3: a mutant that keeps the
    #  message and drops the stop would otherwise classify as HALT); an expected-HALT row must also see ITS vector named.
    diag = re.search(r"unimplemented[^\r\n]*vector=0x([0-9a-f]+)", tr)
    stopped = "machines stopped" in tr           # emul.c's `All machines stopped.' -- the ONE stop observation (pass 4:
    halted = diag is not None and stopped        # an `or "stopped" in tr' disjunct had made the exact term dead code)
    if halted and name in EXPECT_VECTOR and int(diag.group(1), 16) != EXPECT_VECTOR[name]:
        halted = False                              # halted on some OTHER vector: not the row's answer
    #  LEVEL channel (Fable review seat, pass 2): main.c lowers every subsystem to WARNING after startup, so a
    #  free-running `continue' prints an ERROR-level `[ exception <CLASS>: ]' line and stays silent at INFO.  A
    #  delivered row that carries the line has the pre-fix level (M_LEVEL) -- #261's opt-in break-on-ERROR would
    #  then stop the emulator into the debugger on a user process's divide by zero.
    levelmsg = re.search(r"exception (MISALIGNED_ACCESS|UNIMPLEMENTED_OPCODE|PRIVILEGE_VIOLATION|"
                         r"BOUNDS_CHECK_VIOLATION|ILLEGAL_INTEGER_DIVIDE|INTEGER_OVERFLOW|ERROR)", tr) is not None
    tailhalt = "internal error" in tr
    pc = s.pc(); r2 = s.gpr(2); r9 = s.gpr(9)
    sxip, snip, sfip, psr, epsr = s.cr("SXIP"), s.cr("SNIP"), s.cr("SFIP"), s.cr("PSR"), s.cr("EPSR")
    s.close()
    started = (r9 == 0x12345678)
    res = dict(pc=pc, sxip=sxip, snip=snip, sfip=sfip, psr=psr, epsr=epsr, r2=r2, transcript=tr)
    if not started:
        res["result"] = "NOSTART"; return res
    if vector is None:
        ok = (not stopped) and r2 == EXPECT_R2[name]
        res["result"] = "DONE" if ok else ("STOP" if stopped else "BADREGS"); return res
    if halted:
        res["result"] = "HALT"
        if name == "sfu1h" and pc != 8 * V_DIV0:
            res["result"] = "BADREGS"; res["bad"] = ["stage1"]   # halted before the handler ran (the pre-fix shape)
    elif tailhalt:
        res["result"] = "TAILHALT"
    elif stopped:
        res["result"] = "STOP"
    elif pc != entry:
        res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
    else:
        want = dict(sxip=(fault_pc | XIP_V), psr=PSR_WANT.get(name, PSR_EXC), epsr=epsr_exp, r2=0xdeadbeef)
        if name in ("error", "trapfrozen", "errovf", "errdiv0", "errpriv", "errunimpl"):
            # the second fault runs with SFRZ set: the shadows stay FROZEN at the first fault's values.  For
            # `trapfrozen' the second fault is a TRAP, which the manual (:8633-8636, 6.10 :10613-10614) exempts from
            # the ERROR re-route: it must deliver to ITS OWN vector (0x38), shadows still frozen.  M_SFRZTRAP sends it to 0x50.
            want.update(sxip=(0x10004 | XIP_V), snip=(0x10008 | XIP_V), sfip=(0x1000c | XIP_V), epsr=PSR_RESET)
        elif name == "dslot":
            # the else-arm of the delay-slot branch: SNIP = (pc + 4) | V, SFIP = delay_target | V.  br.n +16 puts
            # delay_target at 0x10014 while slot_pc+4 is 0x1000c, so the two channels are DIFFERENT numbers (with
            # br.n +8 they were both 0x1000e and M_SFIPNOTGT / M_DSLOTSWAP escaped 10/10 -- Opus, pass 2).
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((CODE + 4 + 16) | XIP_V))
            assert want["snip"] != want["sfip"], "dslot geometry collapsed: SNIP and SFIP would be one number"
        else:
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc + 8) | XIP_V))
        bad = [k for k, v in want.items() if res.get(k) != v]
        if levelmsg:
            bad.append("level")
        res["result"] = "DELIVER" if not bad else "BADREGS"
        res["bad"] = bad
    return res

def selftest():
    s = Sess()
    ok = s.wait_prompt(0, 60)
    psr = s.cr("PSR") if ok else None
    s.close()
    return psr == PSR_RESET, psr

def main():
    ok, psr = selftest()
    print("M88KEXC_SELFTEST=%s psr_at_reset=%s (want 0x80000002)" % ("OK" if ok else "FAIL", fmt(psr)), flush=True)
    delivered = 0; total = 0; controls_bad = []
    for name, prog, regs, vector, fault_pc, epsr_exp, handler in ROWS:
        res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler)
        print("M88KEXC_ROW=%-9s RESULT=%-8s pc=%s sxip=%s snip=%s sfip=%s psr=%s epsr=%s r2=%s%s" % (
            name, res.get("result"), fmt(res.get("pc")), fmt(res.get("sxip")), fmt(res.get("snip")),
            fmt(res.get("sfip")), fmt(res.get("psr")), fmt(res.get("epsr")), fmt(res.get("r2")),
            (" bad=" + ",".join(res["bad"])) if res.get("bad") else ""), flush=True)
        if vector is not None:
            total += 1
            if res.get("result") == EXPECT_RESULT.get(name, "DELIVER"):
                delivered += 1
        elif res.get("result") != "DONE":
            controls_bad.append(name)
        if os.environ.get("M88KEXC_VERBOSE"):
            print("---- transcript ----"); print(res.get("transcript", "")[-1200:]); print("--------------------")
    print("M88KEXC_RESULT=%d/%d" % (delivered, total), flush=True)
    if controls_bad:
        print("M88KEXC_CONTROLS=BAD %s" % ",".join(controls_bad), flush=True)
    print("M88KEXC_DONE", flush=True)
    #  exit status: the gate can rely on it (a row printing a failure word while the process exits 0 was a pass-2 finding)
    sys.exit(0 if (ok and delivered == total and not controls_bad) else 1)

if __name__ == "__main__":
    main()
