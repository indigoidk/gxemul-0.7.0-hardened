# PASS 9 -- Opus 5 seat, running notes (pcc2widthkills)

Tree: C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC, uncommitted on b78bb0f.
Probe md5 36aabf395e641430cd639425e0711c63 (== the md5 the CHANGELOG names for part 8). 1074 lines.
Scratch clone: /tmp/gxopus_p9 (cp -a of build/), dev_pcc2.c CMP_CLEAN against SEC at 10:5x.

## Line-number sanity (am I reading the fork?)
dev_pcc2.c is 749 lines; helper at :399-406; GENCTL guard :445; TxCTL :490; TxICR :511;
SCCERR :548; IPL :624; MASK :648; default: exit(1) :665.  Matches the brief's inlined text.
NOT one of the three pristine-2021 copies.

## Register facts re-derived from src/include/thirdparty/mvme_pcctworeg.h (NOT from the brief)
GENCTL 0x02 VECBASE 0x03 PSCALEADJ 0x15 T2CTL 0x16 T1CTL 0x17 T2ICR 0x1a T1ICR 0x1b
SCCERR 0x1c SCCICR 0x1d SCCTX 0x1e SCCRX 0x1f SCSIICR 0x2f IPL 0x3e MASK 0x3f
=> SIX EVEN: GENCTL, T2CTL, T2ICR, SCCERR, IPL, SCCTX.  CONFIRMS the contract's "six".
PCC2_C040 0x04, PCC2_MIEN 0x02, TCTL_CEN 0x01 COC 0x02 COVF 0x04 OVF 0xf0,
TTIRQ_IL 0x07 ICLR 0x08 IEN 0x10 INT 0x20.  SCCERR 0x1c is the only 4-aligned block. CONFIRMED.

## Verified so far
* `BREAKPOINT` appears in the whole of src/ at exactly TWO sites, both the hit site
  (src/cpus/cpu_dyntrans.c:1833 / :1837, `fatal("BREAKPOINT: pc = ...")`).  `breakpoint add`
  echoes lowercase and show_breakpoint prints no such token.  So session()'s `until` token
  cannot be satisfied by a stale echo -- the pass-7 inertness had a DIFFERENT cause and the
  pass-8 fix is not defeated by a token collision.  (This was the cheapest way the repair
  could still have been inert; it is not.)

## Q1 -- the value-domain statement, VERIFIED by re-deriving the writer census from source

I enumerated each guarded WRITE body's read-set myself (dev_pcc2.c:444-656), not from the brief:
  GENCTL/MASK      idata, relative_addr            (+ reassert_interrupts -- CALLEE, non-transitive)
  VECBASE          idata, relative_addr
  PSCALEADJ        idata
  TxCTL            reg[relative_addr] (RMW), idata, relative_addr
  TxICR            reg[relative_addr], idata, relative_addr, pending_timer1, pending_timer2
  SCCERR           relative_addr only
  SCCICR/TX/RX/SCSIICR  idata, relative_addr       (+ reassert -- callee)
  IPL              the WRITE branch's function-static `w'
  helper           d->warned, bit, name, len
=> the contract's list is COMPLETE.  No lvalue is missing.

Values HELD at a wide write (derived from the probe's own sessions):
  len              2, 4, 8   (+1 on the accept side)          -- extremes held
  writeflag        WRITE, and READ at 6 even blocks + SCCERR word
  idata            0, 1, 3, 0x22, 0x303, 0x1234, 0xaab8, 0xaabb, 0xaab8ccd9, 0xaab8ccdd,
                   0x...40, 0x...44, 0x00000003, 0x...0003
  reg[TxCTL]       0x00, 0x03, 0x11, 0x81, 0xfc      -> EVERY bit 0..7 held SET and CLEAR
  reg[TxICR]       0x00, 0x13, 0x17, 0x31            -> every LIVE bit (0,1,2,4,5) held both ways
  pending1/2       0, 1, ~10^4 (each SEPARATELY)
  relative_addr    0x16/0x17 and 0x1a/0x1b
  IPL write static 0, 1
  d->warned        0, own bit set, foreign bits both orders

SINGLE-OPERAND CLOSURE SWEPT BY HAND (16 single-bit predicates on the two registers, both
polarities; 6 shapes on the counts; 7 on idata; 4 widths; both writeflag forms):
  * every predicate on a LIVE bit of reg[TxCTL] or reg[TxICR] is killed -- because
    `rb t2ctl b27' holds 0xfc (bits 2-7) and `latch all' holds 0x00;
  * TxICR bits 3, 6, 7 and TxCTL bits 2-3 (absent the memcpy) are genuinely DEAD.  I
    re-derived the writer census independently: the TxICR body's `&= ~0x17' / `|= idata&0x17'
    cannot set 3/6/7; reassert only sets 0x20; and the counter arm's memcpy spans
    0x10..0x17 at most (case labels 0x04/0x08/0x0c/0x10 only), so it cannot reach 0x1a/0x1b.
    THE `E' WARRANT HOLDS.
  * the remaining escapes are arbitrary integer constants (`idata != 2'), which the
    contract DISCLOSES with a stop condition.
So the answer to Q1 is: no held value is wrongly claimed, and the per-lvalue extremes are held.

### THE ONE GAP I FOUND IN Q1: the JOINT pending state is unheld and undisclosed
The TxICR body reads BOTH counts, so both are rule-(2) operands.  Every session arms exactly
ONE timer, so the joint domain is {(0,0),(1,0),(0,1),(N,0),(0,N)} -- (nonzero, nonzero) is
REACHABLE (both CTL CEN + both ICR IEN) and held by NO row.  Measured below.

## Q3 -- the eight measurements re-checked against their predictions
part8/driver.log is genuine and detailed: each mutant is proven by a DIFF COUNT vs SEC with
its first added line quoted, and each carries binary/source timestamps.  I re-derived every
red set from the arm bodies and the mask constants; all eight match.
  * M_TXCTL_OVFHI 184 vs predicted 186: the pre-table wrote `0xfc & 0xe0 != 0 -> the guard
    declines them'.  !(0xfc & 0xe0) is FALSE, so the guard does NOT decline -- the polarity
    was backwards and the CHANGELOG's correction is right.  184 = 190 - 6 CONFIRMED.
  * M_IDATA_NE0_QUAL 170 vs predicted 186: I enumerated the value-0 wide writes independently
    -- r9=0x0 in PEND_REGS/OVF_REGS/PENDN_REGS (8 rows), `put h ...,0x0000' at the T1 labels
    (8 rows), r6="0x0000" at IPL (ipl wset, ipl rset), r6="0x00000000" at SCCERR (wwr sccerr
    dcl), and `latch all zero'.  Exactly 20 rows.  170 CONFIRMED.
  Both explanations are CORRECT and both misses are in the SAFE direction.

## Premises I RE-DERIVED from source rather than accepting (all four HOLD)
1. `put b' cannot reach a DM_DEFAULT arm: debugger_cmds.c's put case 'b' calls
   `memory_rw(..., CACHE_NONE | NO_EXCEPTIONS)', and memory_rw.c:584-585 gates the device
   call on `!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS)'.  pcc2 registers
   DM_DEFAULT (dev_pcc2.c:736).  `put h/w/d' use store_16/32/64bit_word -> normal path. HOLDS.
2. The debugger drives only 2/4/8: `put q' prints "quad-words: TODO" and RETURNS without
   touching memory; 's'/'z' go through the NO_EXCEPTIONS byte path.  So the width set
   {1,2,4,8} is COMPLETE and `latch all' / `latch all w' / `latch all d' cover it. HOLDS.
3. Non-byte m88k accesses are alignment-checked before memory_rw:
   cpu_m88k_instr_loadstore.c:167-185, `#ifndef LS_1 ... if (addr & (LS_SIZE-1)) { exception;
   return; }' -- compiled for every size but the byte.  So byte accesses reach every offset
   and wide ones only aligned offsets. HOLDS.
4. `BREAKPOINT' is emitted ONLY by cpu_dyntrans.c:1833/:1837 on a hit. HOLDS (see above).
   (Also: the m88k guest DOES have 8-byte ld.d/st.d -- generate_m88k_loadstore.c:213 loops
   size 0..3 -- but NO guarded block sits at an 8-aligned offset, so no guest st.d can start
   at one.  The contract's "the guest drives 1, 2 and 4" is right about the guarded arms.)

## Q5 -- TWO WRONG RECORDS, both checkable, both in the shipped pass-8 material
* **`CHANGELOG.md:3` -- "Detector 171 -> 186 rows".**  MEASURED 190: part8/driver.log
  "BASE ... 190/190"; gate14_p9.log "pcc2 width rows emitted 190"; the gate's own name list
  has exactly 190 entries (I counted them: 190, zero duplicates); the brief's own headline
  says 171 -> 190.  The SAME CHANGELOG block says "the 190-row instrument" at :70 and prints
  190/190 at :77 -- **the block contradicts itself in its summary line.**  186 = 171 + 15,
  i.e. the addition list BEFORE `ipl rset', `latch all rev', `rb t2ctl b27', `rb t1ctl b27'
  were added; the gate section of the brief says "the nineteen names added" and 171+19 = 190.
  A count written before the thing it counts had finished -- the frozen-number class, and it
  is the ONE number in the block with no deriver.  L4.
* **`CHANGELOG.md:6` -- "## What pass 8 found (nine seats fired, agy deliberately not
  fired)"**, and the brief's premise 8 "nine of nine answered (...); agy DELIBERATELY NOT
  FIRED".  Both are self-contradictory and both over-count.  The panel dir
  `_scratchpad/panel_20260904_063019/` holds codex, grok, glm, deepseek, minimax and the
  kimi-k3:cloud substitute (`ollama_kimi.txt', 4729 b); `kimi.txt' is 350 b of
  `403 ... weekly (7-day) usage limit'; agy has no file at all.  With opus5 and fable5 that
  is EIGHT answering of a nine-seat roster, one seat deliberately not fired.  The block's own
  "Records corrected (L4)" section says pass 8 corrected exactly this in the pass-6 heading
  ("the pass-6 heading's 'nine of nine' -> eight answering seats of nine") -- **and then
  repeated it in its own heading.**  L4.
  (The pass-8 SEATS.txt additionally prints "this seat is LOST rather than covered" while
  ollama_kimi.txt sat beside it; that was already recorded as Opus F18 and `tools/panel.sh`
  now sets OLLAMA4="kimi-k3:cloud" -- fixed in the tool, so it will not recur.)

## MEASURED: BASE reproduced INDEPENDENTLY
/tmp/gxopus_p9 (cp -a of build/), dev_pcc2.c cmp-clean vs SEC, `rm src/devices/dev_pcc2.o`,
`make` (MAKE_RC=0), `[ gxemul -nt dev_pcc2.c ]` FRESH_OK.  Frozen probe md5 36aabf39.
  BASE  **190/190**, PCC2W_PROBE_DONE, no PCC2W_RED line.   log: BASE.out
NAME-SET CHECK the gate cannot do on its own: the probe emits 190 UNIQUELY named rows and
gate_arm.sh:1295's list holds exactly the same 190 names -- symmetric difference EMPTY, zero
duplicates on either side, longest name 15 chars (`brd pscale noig'), which is exactly what
keeps the gate's two-space `^$v  .*ok$' pattern satisfiable given `%-16s' + a literal space.
The `assert len(name) <= 15' in row() is load-bearing for the gate and nothing says so.

## Q1 -- the stop condition is HONEST but STATED WEAKER THAN WHAT WAS ACHIEVED
"the reachable extremes ... are held" is vague; what the rows actually achieve is stronger
and is checkable:
  reg[TxCTL] held {0x00, 0x03, 0x11, 0x81, 0xfc} -> **all EIGHT bits held both SET and CLEAR**
  reg[TxICR] held {0x00, 0x13, 0x17, 0x31}       -> **all FIVE live bits (0,1,2,4,5) held both
                                                     ways; bits 3,6,7 dead with a census**
That bit-coverage property is exactly why every single-bit predicate on either register dies,
and it is what a future round should be asked to preserve.  RECOMMEND replacing "the reachable
extremes are held" with the bit-coverage sentence -- it is falsifiable in one grep of the
presets, "extremes" is not.  (Note reg[TxCTL]'s bits 2,3,5,6 are held ONLY by `rb t*ctl b27',
i.e. only through the FILED pcc2counter8 path; the probe says so and the rows must be re-cut
when it is fixed.  That is disclosed correctly.)

## Q2 -- session(), traced against the LIVE file (pcc2_width_probe.py:375-479)
`("continue", 20.0, "BREAKPOINT")`:
  :409 isinstance tuple -> :410 `until = c[2] ...  # read the tuple BEFORE unpacking it`
  -> :411 `c, w = c[0], c[1]`.  The pass-7 order defect is GENUINELY fixed in the live file.
  :402 `return "timeout" if until is not None else True`; :419 `if r is False` uses IDENTITY,
  so the truthy string "timeout" cannot be mistaken for success and True cannot be mistaken
  for the string.  :423-424 on timeout -> `how = "no-breakpoint"; break`, so NOTHING further
  is written to a still-running guest.
  DOES THE WAIT STOP ON THE TOKEN?  YES, and it cannot fire early: `BREAKPOINT` occurs in the
  whole emulator source only at cpu_dyntrans.c:1833/:1837 (the hit).  `breakpoint add' echoes
  lowercase and show_breakpoint() prints no such token.
  KILLED GUEST KEEPS ITS LABEL: :440 `reaped` flag; :452 kill(9); :453 label guarded; :455-464
  bounded second reap; :469 `if stat is None or not reaped or how in (...)`: pass -- so
  WIFEXITED(0) can no longer overwrite "killed".  Pass-8 F2 is fixed.
  CAN THE GATE HANG?  NO.  Every wait is bounded: settle 1.5 s, per-command w (<= 20 s),
  0.4 s after quit, 3 s + 3 s reap.  The ONLY unbounded call left is `os.write(fd, ...)`,
  which can block if the pty input buffer fills while the guest is free-running; commands are
  tens of bytes against a kilobyte buffer, so it has never been hit.  Worth one sentence.

### FINDING 2A -- `cval()` covers HALF the apparatus, and the pass-8 record claims both halves
The eight `* decl` rows -- :790, :798, :814, :821, :842, :849, :859, :866 -- are
`cval(how, t.count(DECL))` with NO `alive' test.  Their eight companion `* rb' rows all carry
`... if alive and len(r4s) > 1 else "died"'.  So a session in which the emulator DIED (rather
than missed its breakpoint) grades the decl row as a BARE INTEGER with no apparatus note.
The pass-8 CHANGELOG says "a missed token now INVALIDATES the session and every companion row
reports the apparatus reason through `cval()'" -- true for the missed-token half, NOT for the
death half.  Not a coverage gap (the companion rows say "died", and a host-killing mutant reds
the decl row anyway) -- a LABELLING gap and an overclaimed sentence.  One-token fix:
`cval(how, t.count(DECL) if alive else "died")`.  L4 + a one-line instrument repair.

### FINDING 2B -- a row that can still red for a reason other than the one under test
`ovfhi2 arm/rb` and `ovfhi1 arm/rb` pin the EXACT value 0x81 (overflow count == 8 | CEN).  The
count advances by ONE per DELIVERED SIGALRM (pcc_timer_tick:240-244, `oc = 1 + (reg >> 4)`).
If the host deschedules the emulator across two callback periods inside the two-instruction
poll loop, the loop exits at count 9 and the rows report 0x91 -- and NEITHER armval() nor
cval() names that, because the BREAKPOINT was reached and the guest is alive.  The pend*/pendn*
rows have no such exposure (0x31 is stable once INT is set).  This is a NEW load sensitivity
introduced by pass 8's ovfhi rows; the contract's blanket "run the gate alone" is the only
mitigation recorded.  Cheap repair: accept `bit 7 set' rather than the exact 0x81, or say so.

### FINDING 2C -- dead code in the repair
:468 `if False:` disables the old blocking `os.waitpid(pid, 0)` instead of deleting it.
Harmless today; a future reader can re-enable the exact unbounded wait the repair removed.

## Q4 -- the smallest edit that breaks the property and passes 190 rows
**`&& idata != 2` at any one of the twelve guards.**  One added clause; the property broken is
the fix's own ("a wide WRITE never lands"): a guest `st.h 0x0002` to GENCTL then stores 0x02,
VECBASE's lane -- the ORIGINAL defect, for exactly that value, silently and unlatched.
ROWS I EXPECT TO STAY GREEN, and why: **all 190.**  I enumerated every wide-write value the
instrument drives: 0x0000, 0x0001, 0x0003, 0x0022, 0x0303, 0x1234, 0xaab8, 0xaabb,
0x00000003, 0xaab8ccd9, 0xaab8ccdd, 0x0000000000000003, 0xaab8ccdd00112240,
0xaab8ccdd00112244.  The value 2 is driven at NO arm at ANY width, so `latch all' (3),
`latch all one' (1) and `latch all zero' (0) -- the three cardinality rows that pin idata at
every arm -- all stay at 12, and every per-arm readback drives a value != 2.
THIS IS DISCLOSED: the contract says a value-test qualifier is caught only for 3, 1, 0 at
every arm and per-arm for that arm's own wide-write constants, "any other constant is not".
So it is OUTSIDE the contract, not a floor breach.  MEASURED below.
Runner-up, also disclosed: `&& d->pcctwo_reg[PCCTWO_IPL] == 0` at the IPL guard (out of
closure; consequence is one extra "write to read-only PCCTWO_IPL" line and no state change).

## MEASURED, interim: M_OPUS_PENDBOTH -- all 24 timer rows GREEN
At 135/190 rows the mutant `&& !(d->pending_timer1_interrupts &&
d->pending_timer2_interrupts)` at the TxICR guard (diff vs SEC: 3 lines; binary 11:15:00 >
source 11:14:54) has EVERY timer row green:
  pend2 arm/decl/rb, pend1 arm/decl/rb, ovf2 *, ovf1 *, ovfhi2 *, ovfhi1 *, pendn2 *,
  pendn1 *  -- 24 of 24, values 0x31 / 0x11 / 0x81 unchanged, DECL counts 1.
Exactly as predicted: no session arms BOTH timers, so the conjunct is TRUE in every row.

## The gate result is ATTRIBUTABLE (two-part clearance run, not asserted; read-only)
  cmp build/src/devices/dev_pcc2.c GXEMUL-SEC/src/devices/dev_pcc2.c  -> CLEAN
  build/gxemul 2026-09-04 04:13:30.629 > build/src/devices/dev_pcc2.c 04:13:21.357  -> FRESH
  gate_arm.sh:77 `PMAX=${PMAX:-$ROOT/build/gxemul}', gate_arm.sh:1287 runs the LIVE
  regress/pcc2_width_probe.py; gate14_p9.log mtime 10:42:52 > probe mtime 08:02:17, so the
  gate DID run against the shipped instrument (the pass-8 F7 defect is fixed).
  est/ is a SOURCE tree: part 2 N/A.  dev_pcc2.c is not on the est-divergence list.

## Order witnesses (mtimes, not memory)
  probe last edited        08:02:17
  PRETABLE_pass8.out       08:02:23   (6 s later, BEFORE the table)
  part8/driver.log         10:10:59
  gate14_p9.log            10:42:52
  my PREDICTIONS.md        11:06:00   (BEFORE my first mutant build at 11:14:54)

## READBACK VACUITY SWEEP (the part-6 0x33/0x44 trap), all clean
For every readback row I computed the value the fall-through/DELETE mutant would LAND and
compared it with the row's preset.  No collision anywhere:
  genctl  0x82 vs landed 0xbb (len2) / 0xd9 (len4) / 0x40 (len8) / 0xaa (compose) / 0x22 (lo)
  vecbase 0x50 vs 0xb0 / 0xd0 / 0x40           mask    0x12 vs 0xbb / 0xdd / 0x44
  t2ctl   0x03 vs 0x00 / 0x01 / 0x00           t1ctl   0x03 vs 0x00 / 0x01 / 0x00
  t2icr   0x13 vs 0x10 / 0x15 / 0x04           t1icr   0x13 vs 0x10 / 0x15 / 0x04
  sccicr  0x1f vs 0x18 / 0x1d / 0x04           scctx   0x1f vs 0x18 / 0x1d / 0x04
  sccrx   0x1f vs 0x98 / 0xdd / 0x44           scsiicr 0x1f vs 0x98 / 0xdd / 0x44
  t2ctl b27 0xfc vs 0xff                       t1ctl b27 0xfc vs 0xff
  ovf* 0x11 vs 0x10   ovfhi* 0x81 vs 0x80      pend*/pendn* 0x31 vs 0x20
  il4 0x17 vs 0x10
And the GENCTL lane values keep bit 0x04 clear (0xbb, 0xd9, 0x40, 0x22, 0x03, 0x01, 0x00),
which is what stops a landed write from killing the host in reassert_interrupts() and turning
a by-VALUE kill into a by-DEATH one.  c040ok() at :710-715 now asserts that at authoring time
-- correctly, on the LOW byte, which is the lane a truncating `= idata' store takes.

## OBSERVATION on what M_IDATA_NE0_QUAL's 170 actually measures (not a defect)
All EIGHT free-running sessions wide-write the value ZERO -- `r9=0x0' in PEND_REGS, OVF_REGS
and PENDN_REGS for the T2 labels, and a literal `put h ..., 0x0000' for the T1 labels.  So 16
of that mutant's 20 red rows are the free-running sessions, and only 4 (`latch all zero',
`wwr sccerr dcl', and pend1's decl/rb pair as the pre-table named them) are rows built for the
value-0 cell.  The pre-table's 186 was an under-count for exactly that reason and the
CHANGELOG says so correctly.  The consequence worth knowing: the free-running sessions
contribute NOTHING to the `idata' dimension beyond the value 0 -- they exist to hold the
REGISTER and COUNT state -- so a future round that changes `r9' would move that mutant's score
without changing coverage.  Leave it: 0 is also the value whose landed result differs most
from each preset (0x31 -> 0x20, 0x11 -> 0x10, 0x81 -> 0x80).

## *** MEASURED RESULT 1: M_OPUS_PENDBOTH = 190/190, A TOTAL ESCAPE ***
    mutant  `if (len != 1 && writeflag == MEM_WRITE
                && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts)) {'
            at the TxICR guard ONLY.  diff vs SEC: 3 lines.  binary 11:15:00 > source 11:14:54.
    log     M_OPUS_PENDBOTH.out, PCC2W_PROBE_DONE, no PCC2W_RED line.
    PREDICTED 190/190 in PREDICTIONS.md at 11:06:00, before the build.
Every one of the 24 timer rows stayed green with its exact value (0x31 / 0x11 / 0x81) and its
DECL count of 1.  Both counts are body-read fields at TxICR, so both are inside the clause-(d)
rule-(2) operand set -- but the instrument holds them only ONE AT A TIME, and (nonzero,
nonzero) is REACHABLE (both TxCTL CEN, both TxICR IEN, both compares low).
DISPOSITION -- and I argue AGAINST calling this a floor breach, so the round can adjudicate:
  * the (d) rule's own test is "could a PLAUSIBLE future edit produce it"; `&& !(p1 && p2)' is
    not an edit anyone writes.  Every SINGLE-operand form is killed: `== 0' and `!x' by pend*,
    `< 2' by pendn*, `> 0' by `latch all' (pending is 0 there), and the T1/T2 cross forms by
    the opposite label's rows.
  * admitting arbitrary BOOLEAN COMBINATIONS of the read-set makes the (d) space exponential
    in the number of body-read fields, which is exactly what the DEPENDS-ON bound
    ("finite, derivable from the diff by reading") exists to prevent.  Read as single-operand,
    the closure is complete; read as multi-operand, it is #392.
  * row demand is PER ENUMERATED MUTANT, never per reachable state, so NO ROW IS OWED.
  => **L4: one sentence in the enumeration** -- "pending_timer1/2 are held SEPARATELY; no
     session arms both timers, so a predicate over the PAIR is outside the sample" -- and no
     new row.  Adding a both-timers session would add a ninth free-running row-group and make
     gate 14 more load-sensitive for a cell no plausible mutant reaches.

## WHAT I SWEPT (the denominator behind my zero)
1. **Lvalue completeness**: read-set of all 12 guarded write bodies + the helper, re-derived
   from dev_pcc2.c:444-656 and :399-406.  SEVEN distinct lvalues.  Contract's list == mine.
   **0 missing.**
2. **48 single-operand clause-(d) predicates walked by hand** at the values the 190 rows hold:
   reg[TxCTL] 8 bits x 2 polarities (16), reg[TxICR] 8 x 2 (16), the two pending counts
   (`==0', `!x', `<2', `>0' = 4), idata (`!=0', `!=1', `!=3', `>0xff', `<=0xffff',
   `(idata&0xff)!=0', `(idata>>8)!=0' = 7), relative_addr at the two shared blocks (3),
   the two IPL statics (2).  **45 killed, 3 equivalent-by-dead-bit (TxICR bits 3/6/7, always-
   true polarity only; writer census re-derived), 0 escaping.**
3. **d->warned**: own bit at 12 blocks (11 rowed by `rb2 *' / `pscale noig2' / `ipl noig2';
   SCCERR genuinely E -- its second wide write stores 0 either way) and all **132 ordered
   foreign pairs** (`latch all' covers B-before-A, `latch all rev' the rest; I checked the
   derivation both directions).
4. **96 width x arm x direction cells** (12 blocks x {1,2,4,8} x {R,W}): every cell has a row,
   an E warrant, or an unreachability warrant.  Width set independently confirmed to be exactly
   {1,2,4,8} (`put q' touches no memory; `put b/s/z' use NO_EXCEPTIONS and cannot reach a
   DM_DEFAULT arm; the m88k alignment check fires for every non-byte size).
5. **Every readback row** checked for the part-6 preset-collision trap: **0 vacuous.**
6. **Instrument/gate agreement**: 190 probe rows == 190 gate names, symmetric difference EMPTY,
   0 duplicates, longest name 15 (which is what keeps the gate's two-space pattern satisfiable).
7. **All eight part-8 red-sets re-derived by hand** from the arm bodies and the mask constants;
   all eight reproduce, and both prediction misses are explained correctly and in the SAFE
   direction.
8. **BASE 190/190 reproduced in my own clone**, plus TWO mutants built and measured.
NOT swept (say so rather than leave a blank): floor clause (a) -- I did not rebuild a pre-fix
binary; that was established in earlier parts (witness_20260903_PREFIX.out) and is not this
pass's material.  Multi-operand boolean combinations beyond the one I measured.  The 4-/8-byte
repeats of the latch-set shape, which the contract already FILES as coverage debt.

## FOUND OUTSIDE THE QUESTIONS
* **A stale `panel.sh` sits at the PROJECT ROOT** -- `C:\DocumentNoSnc\CC\GXEMUL\panel.sh`,
  dated 2026-08-17 (the migration day), 22,668 bytes against `GXEMUL-SEC/tools/panel.sh`'s
  49,489, 453 differing lines, and it has NO `OLLAMA4' at all.  A session that types
  `./panel.sh' from the project root fires the PRE-MIGRATION roster: no kimi substitute, no
  argv-cap pointer form, no Ollama daemon pre-flight -- and it would look like a completed
  panel.  The carrier already says to always use the `GXEMUL-SEC/tools/' path, but for a
  DIFFERENT reason (cwd drift makes `./panel.sh' fail loudly); this one fails QUIETLY, which
  is worse.  Delete it or make it an `exec' shim.  (Out of this pass's scope; reported because
  it is one `rm' and the failure mode is silent.)
* `row()`'s `assert len(name) <= 15` (pcc2_width_probe.py:367) is LOAD-BEARING FOR THE GATE and
  nothing says so: `"%-16s "` gives a 15-char name two trailing spaces and a 16-char name one,
  and gate_arm.sh:1296 greps `"^$v  .*ok$"` -- two spaces.  A 16-char row name would make its
  gate check UNSATISFIABLE (the padded-column trap) while the probe still printed the row.
  One comment on the assert.

## STRENGTHENING (not owed, cheap, and it makes a vague claim checkable)
Replace the contract's "the reachable extremes ... are held" with what the rows actually
achieve: **"every LIVE bit of each in-closure register is held both SET and CLEAR at a wide
write -- reg[TxCTL] by {0x00,0x03,0x11,0x81,0xfc}, reg[TxICR] by {0x00,0x13,0x17,0x31}; TxICR
bits 3,6,7 are dead with a writer census."**  That is falsifiable by one grep of the presets;
"extremes" is not, and it is the property that actually kills every single-bit predicate.

## *** MEASURED RESULT 2: M_OPUS_IDATA2 = 190/190, A TOTAL ESCAPE (DISCLOSED) ***
    mutant  `&& idata != 2' at ALL TWELVE guards.  diff vs SEC: 24 lines (12 guards).
            binary 11:29:08 > source 11:29:06.  log M_OPUS_IDATA2.out, PCC2W_PROBE_DONE,
            no PCC2W_RED line.  PREDICTED 190/190 at 11:06:00, before the build.
This is the contract's OWN disclosure measured rather than reasoned: a value-test qualifier
on any guard escapes for every constant the rows do not drive.  Consequence: a guest
`st.h 0x0002' to GENCTL then stores 0x02 -- VECBASE's lane -- silently and unlatched, i.e.
the round's original defect for exactly that value.  OUTSIDE THE CONTRACT, not a breach.

## TABLE (every number names its log; all in this directory)
    BASE                190/190   BASE.out              (clone rebuilt first, FRESH_OK)
    M_OPUS_PENDBOTH     190/190   M_OPUS_PENDBOTH.out   TOTAL ESCAPE, predicted
    M_OPUS_IDATA2       190/190   M_OPUS_IDATA2.out     TOTAL ESCAPE, predicted, DISCLOSED
    driver              DRIVER.log   predictions PREDICTIONS.md (11:06:00, before mutant 1)

## HYGIENE (run, not asserted)
  clone /tmp/gxopus_p9 only; NOTHING written to GXEMUL-SEC, build/, est/ or build-asan.
  Verified after the run: `git -C GXEMUL-SEC status --porcelain' identical to the pre-run
  listing (same 9 modified files, same untracked dirs); build/gxemul and
  build/src/devices/dev_pcc2.c still 04:13:30.629 / 04:13:21.357; no `.MUTANT' anywhere;
  GXEMUL-SEC probe md5 still 36aabf39.  Clone restored FROM SEC, cmp CLEAN, REBUILT
  (binary 11:43:14 > source 11:43:13), sentinel cleared.
