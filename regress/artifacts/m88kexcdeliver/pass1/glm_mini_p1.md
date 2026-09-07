# MINI PACKET for a packet-fed seat (you cannot read files; every fact is inlined). ONE question set; answer in under 600 words. VERDICT LINE FIRST.

An emulator (GXemul, MC88100 CPU model) has an exception function with TWO switches. Switch 1 marks four vectors `implemented = true`
(RESET, INTERRUPT, INSTRUCTION_ACCESS, DATA_ACCESS); seven other classes (MISALIGNED 4, UNIMPLEMENTED_OPCODE 5, PRIVILEGE 6,
BOUNDS_CHECK 7, ILLEGAL_INTEGER_DIVIDE 8, INTEGER_OVERFLOW 9, ERROR 10) print a message and leave it false. A fallback then stops
every guest CPU for any vector < 128 that is not implemented. After the fallback, a common path saves EPSR = PSR, sets PSR |=
SFRZ|IND|SFD1|MODE, sets SXIP = pc|V, SNIP = (pc+4)|V, SFIP = SNIP+4, pc = VBR + 8*vector, then a TAIL switch with arms for the four
implemented vectors and a `default:` that prints `internal error` and stops THIS cpu.

MEASURED FACTS (a compile-and-run seat, today): (1) naive fix = `implemented = true` only -> every fault stops at the tail default,
with pc/SXIP/PSR already correct. (2) full fix = implemented=true AND tail `case ... break` -> 3/3 rows DELIVER with pc=8*vector,
SXIP=fault_pc|2, SNIP=fault_pc+4|2, SFIP=+8|2, EPSR=0x80000002, PSR=0x8000000b, destination register unchanged. (3) supervisor
`tb1 0,r3,7` reaches BOUNDS_CHECK today (the trap instruction carries a 9-bit guest-chosen vector; no filter in supervisor mode).
(4) a second fault inside a handler (SFRZ already set) is re-routed to ERROR (vector 10) and dies at the tail default even with
the five-class fix. (5) The manual: rte resumes at SNIP, never SXIP; for all seven classes SXIP = the faulting instruction and the
destination is unchanged (6.6 for overflow: "destination register and carry bit are unchanged").

THE DESIGN: set `implemented = true` for the SEVEN classes, print them at VERBOSITY_INFO (like the four implemented ones), add the
seven as tail `case` labels with a bare `break`. Leave SFU1 (114/115) and vectors 11..113/116..127 at the fallback.

Q1 Is there any reason, from these facts, that a bare `break` in the tail is the WRONG return-address contract for any of the
   seven (e.g. one that should re-execute the faulting instruction, i.e. SNIP = pc)?
Q2 The detector asserts, per row: pc == 8*vector; SXIP; SNIP; SFIP; PSR == 0x8000000b; EPSR (0x80000002 supervisor rows,
   0x00000002 user-mode rows); destination unchanged; machine still running. Name the smallest edit to the fixed function
   that would pass ALL of those and still be wrong.
Q3 Name any option the design set {deliver seven / naive / decline (rejected) / make the tail default deliver everything} misses.
