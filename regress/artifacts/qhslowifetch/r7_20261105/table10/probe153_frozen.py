#!/usr/bin/env python3
"""qhslowifetch -- DETECTOR (built on its rung-3 witness) for the PowerPC slow-path instruction fetch in X(to_be_translated).

DEFECT (filed 2026-10-02).  src/cpus/cpu_ppc_instr.c, X(to_be_translated): when the instruction word is not in a host
page, the translator reads it with cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION); if that read FAILED it printed
"PPC to_be_translated(): read failed: TODO" and called exit(1) -- the emulator process ended.

THE FIX (#NNN).  The read-failure arm has four exits and a fallback: (a) read-ahead returns untouched; (b) a fetch whose
translation already delivered an exception (pc, its low two bits cleared, != addr) refreshes next_ic and returns; (c) a -T halt
(memory.c cleared running) parks the CPU on nothing_call at the fetch's pc (its low two bits kept; the halt report names the
aligned address); (d) a device declining an instruction-width read while running delivers a machine check (vector 0x200) when
MSR[ME] is set, and a checkstop (text, running = 0, park) when it is clear.

WHICH FETCHES REACH IT (measured 2026-11-04).  An IR-on fetch from an unmapped address SURVIVES on the pre-fix build: the ISI
is delivered by the dispatch PC lookup before the translator runs (the `isi` rows).  What reaches the arm is a fetch that
translates and then fails as a PHYSICAL read: with `-T` (halt on a non-existent memory access) a real-mode fetch past the end
of RAM.  Without `-T` the same fetch reads zeros and the CPU stops on the zero word (the `noT` rows).

WHAT THE ROWS MEASURE.  Cold `-E pmppc` debugger runs (an UNMODIFIED in-tree machine: Artesyn PM/PPC, PPC750, 32 MB) with a
four-byte `ori r0,r0,0` loaded raw at 0x2000 and SRR0 seeded with a sentinel only an exception entry overwrites.  CONTROLS: the
loaded word executes (`ctl`); a bogus machine runs nothing (`neg`); the ISI route survives and delivers the exception (`isi`);
the no-`-T` route stops on the zero word (`noT`).  `noT unimpl` (the zero word reported UNIMPLEMENTED, because the read
succeeded) and `noT chkstop` (no checkstop text) are NOT controls: they catch D15 and V7, which send a successful read into the
failure block.  The -T SESSIONS at 0x02040000 are `T step` (one step), `T cont` (continue), `again` (step, step, continue,
continue) and `T me` (one step with MSR[ME] set).  `T step`, `T cont` and `again` each pin: exit 0 with the prompt back and no
`read failed: TODO`; pc parked at the fetch address; SRR0 unchanged; the exact count of -T halt reports; no UNIMPLEMENTED, no `[
PPC Exception`, no checkstop text.  `T me` pins exit 0, pc, SRR0, the halt count, no `read failed: TODO`, no `[ PPC Exception`,
no UNIMPLEMENTED (`T me unimpl`, added by the adjudication of repair pass 2, Q4: an arm (c) that sends an ME-set -T halt to bad:
changes no other `T me` channel) and no checkstop text (`T me chkstop`, V11); its prompt channel is left to the other three
sessions.  Every -T session also pins the final MSR (the `msr` rows: 0 where ME is clear, 0x1000 where it is set; the
adjudication of repair pass 3, F1) -- true from repair 7, which added `T ra odd msr`: repair 6's `T ra odd` carried no msr row, so
while it stood this sentence was FALSE (codex pass 6, R1).  The halt counts ("non-existant"): two for a step -- the single-step
read's report, its "could not read the instruction" line, then the translator's report -- one for a continue, and two for the whole
`again` session, because a -T halt leaves running at 0 (memory.c), so the run loop does not enter the CPU again and a further step
or continue runs nothing (measured, and the reverse of the reconciliation's provisional want; see
artifacts/qhslowifetch/det_20261104/FINDING_D8.md).  `isi1` steps into the ISI as `isi` continues into it; both pin the vector,
SRR0 and no halt report.  `T ra` continues under -T from 0xfec00004, the last word of cpc700_pci's 8-byte window, which reads
0x23120e00 (subfic r24,r18,0xe00) in its reset state: translating it reads ahead into 0xfec00008, past the window, so the -T
halt fires DURING read-ahead and arm (a) returns; the subfic runs; the real fetch of 0xfec00008 halts again and arm (c) parks.
It pins exit 0, pc 0xfec00008, two halt reports both naming 0xfec00008, and the stop (the window sweep found it,
det_20261104/window_sweep.out; FINAL_FABLE.md F4 owed it).  `T ra me` is `T ra` with MSR[ME] set (msr=0x1000; the adjudication
of repair pass 2, Q1): it pins exit 0, pc 0xfec00008 and the two reports, so arm (a)'s guard is seen with ME both clear and set.
`T ra` also pins no checkstop text (`T ra chkstop`, F2: the parity of `T ra me chkstop`).  `T ra me` also pins the halted
address and the stop (`T ra me addr`, `T ra me stopped`, repair 7b); until then it carried neither, and this text disclosed "an
edit that moves the halt address or the stop only when ME is set" as not claimed.  `T ra srr0` and `T ra me srr0` pin SRR0
unchanged on the read-ahead route (the repair-pass-4 ruling, R6).  `T blr` (repair 5, the repair-pass-4
ruling) continues under -T into a GUEST-MADE unaligned pc: `mtlr r3; blr` with r3 = 0x02040007, bits 0-2 set (repair 6), so the
prologue gives addr 0x02040004.  This fork's mtlr and its unconditional blr (X(bclr_20)) copy LR unmasked and the prologue
aligns addr but not pc, so the failure block sees pc != addr; before repair 5 arm (b) took it and re-ran the slot -- 8278 halt
reports (p4_20261105/BLR_NOTE.md) -- and with the aligned compare it parks in arm (c).  It pins exit 0, pc 0x02040007, one halt
report, SRR0 and MSR unchanged, no checkstop or UNIMPLEMENTED text, and LR holding the stored value.  `T ra odd` (repair 6) is
`T ra` entered at the UNALIGNED pc 0xfec00005: the read-ahead fetch reaches the failure block with pc != addr, arm (a) returns
and the real fetch halts again; it pins exit 0, pc 0xfec00009, two reports and MSR 0 (`T ra odd msr`, repair 7), so arm (a)'s
guard is seen with an unaligned pc (p5_20261105/TRAODD_NOTE.md).  `T ra o1m`, `T ra o2`, `T ra o2m`, `T ra o3` and `T ra o3m`
(repair 7, the CLASS CLOSURE: passes 5 and 6 both found unrowed arm (a) x alignment cells, r7_20261105/B123_NOTE.md) complete the
grid of pc's low two bits {00, 01, 10, 11} x MSR[ME] {clear, set} on that route: each is `T ra` entered at 0xfec00004 | low bits
(the digit; `m` = MSR[ME] set, written msr=0x1000 before pc) and pins exit 0, pc 0xfec00008 | low bits, two reports and MSR as
entered.  REPAIR 7B gave the six unaligned sessions the four channels their aligned siblings pinned and they did not -- the
halted address, the stop, the checkstop text and SRR0 (`addr`, `stopped`, `chkstop`, `srr0`) -- and `T ra me` the first two, so
all eight cells (with `T ra`, `T ra me` and `T ra odd`) pin the same eight channels: session, pc, nonex, addr, stopped, msr,
chkstop and srr0.  Before it an SRR0 write and a checkstop print in arm (a), each gated on pc != addr, passed all 103 rows
(r7_20261105/B123_NOTE.md, repair 7b).  Repair 8 added a ninth channel to all eight read-ahead sessions: no UNIMPLEMENTED text
(`unimpl`).  This text argued that none was needed: "the real fetch of each reaches the block in a state the 0x02040000 sessions
and `T blr` already pin -- not read-ahead, running 0, ME clear or set, pc aligned or not -- so an edit gated on anything the block
tests that prints `read failed: TODO`, `[ PPC Exception` or UNIMPLEMENTED there prints it on one of those sessions too".  That was
FALSE: those sessions hold ME and alignment one at a time and never the unaligned ME-set joint state, and a `goto bad` gated on
`(msr & ME) && pc != addr` in arm (c) printed UNIMPLEMENTED on `T ra o1m`, `T ra o2m` and `T ra o3m` with all 129 rows green (codex
pass 7, F1 and R1; MEASURED, r7_20261105/B123_NOTE.md, repair 8).  No read-ahead session carries a `text`, `exc` or `prompt` row,
and the reason is now given per channel, from the block's own arms: `[ PPC Exception` is printed only by ppc_exception, which
always moves pc to the vector and writes SRR0, both rowed on every read-ahead session; `read failed: TODO` is the removed exit's
text, which the composite SYMPTOM key scans every session for and whose exit ends the session; the prompt is implied by the
register rows, which read `none` without it.  Their wants are derived from the code -- the read-ahead fetch reaches the failure
block at pc 0xfec00008 | low bits, arm (a) returns, the subfic runs, the real fetch halts again and arm (c) parks at that pc -- and
the eight-cell table measured them before the rows existed; a guard refusing a cell parks it at read-ahead time instead (one
report).

WHY THE CHECKSTOP AND ME-SET ROWS EXIST.  MSR is 0 on `T step`, `T cont` and `again`; `T me` sets MSR[ME] (0x1000).  On the
first three, arm (c) deleted or inverted falls to the checkstop fallback, which parks identically -- same pc, SRR0 and
next_ic -- and differs only by its text (the `chkstop` rows).  And arm (c) ordered below arm (d), or conditioned on ME clear,
differs only when ME is set (the `T me` session, which drives arm (d)'s tested bit at the -T halt).  Both were added by the
pre-table check, before the test-variant table ran.  Arm (a)'s guard conjoined with an ME-clear test differs only on a
read-ahead with ME set (`T ra me` and the three unaligned `m` sessions), and conjoined with an ME-set test only on one with ME
clear (`T ra`, `T ra odd`, `T ra o2`, `T ra o3`); an arm (c) that sends an ME-set halt to bad: only by its UNIMPLEMENTED text (`T
me unimpl`, and from repair 8 the unimpl rows of the four ME-set read-ahead sessions).  An arm (c) that sends an ME-set halt to the
checkstop fallback differs only by the checkstop line, so `T me` and `T ra me` carry a chkstop row (`T me chkstop`, `T ra me
chkstop`; the shape-grid check before table 3 found that composition, all three cloud seats).

CLAUSE (e) -- catches (test-variant table 9, artifacts/qhslowifetch/r7_20261105/table9/SCORES.txt, PRETABLE_9.out written before
it; 69 variants on this 137-row probe: 54 red, every one on this probe; 14 green, the predicted fourteen; V12 NOT PREDICTED): the
removed exit reinstated verbatim (B1); a bare return at the arm head (W2) or on every non-read-ahead fetch (D5); goto bad (W3); an
ISI invented in arm (c) (W4); the arm emptied, or skipped by conditioning the read's failure test on running, so the uninitialised
word decodes (W5, D7); arm (c) inverted or deleted (D1, D2: the chkstop rows of the ME-clear -T sessions -- `T cont`, `T step`,
`again`, `T blr` and the four ME-clear read-ahead sessions -- and, where ME is set and the missing park falls to the machine check,
`T me exc` and the pc and srr0 rows of `T me`, `T ra me` and the three unaligned ME-set read-ahead sessions; `T me chkstop` and the
four ME-set read-ahead chkstop rows stay green under both -- this clause said "D1, D2: the chkstop rows", which
LATE_REPLICATIONS_20261105.md row 13 found too broad); arm (c) without its park (D3); arm (b) inverted (D4: `T cont nonex`, `T ra
nonex`, `T ra me nonex`); arm (c) below arm (d), or conditioned on ME clear or on ME set (D8, D13, D14); the read's failure test
made always true (D15: the noT rows and the read-ahead sessions) or inverted (V7: the same rows plus `T cont unimpl` and the pc,
srr0 and exc rows of `T step`, `T me` and `again` -- this clause said "D15, V7: the noT rows and the read-ahead sessions", which
omitted those, LATE_REPLICATIONS_20261105.md row 12; V7 is build-dependent, so these are its table-8 rows); arm (a)'s guard deleted
(W7), and the slow path skipped during read-ahead (D12), by the read-ahead rows; arm (a)'s guard conjoined with ME clear (V8: the
nonex rows of the four ME-set read-ahead sessions) or with ME set (V9: those of the four ME-clear ones); an ME-set halt sent to
bad: (V10: the unimpl rows of `T me` and the four ME-set read-ahead sessions) or to the checkstop fallback (V11: the chkstop rows
of `T me` and the four ME-set read-ahead sessions); MSR[ME] cleared in arm (c) (B1a: `T me msr` and the msr rows of the four ME-set
read-ahead sessions) or in arm (a) (B1b: those four), or set in arm (c) (B1c: the msr rows of `T cont`, `T step`, `again`, `T blr`
and the four ME-clear read-ahead sessions); the checkstop line printed on an ME-clear read-ahead failure while arm (a) still
returns (B2: the chkstop rows of the four ME-clear read-ahead sessions); arm (b)'s aligned compare reverted to `pc != addr`
(R5_revert: `T blr nonex` and the nonex rows of the six unaligned read-ahead sessions), or its mask narrowed to either low bit
(R5_mask1, R5_mask2: `T blr nonex` and the nonex rows of the four read-ahead sessions whose pc carries the other bit); SRR0 written
in arm (a) (R5_srr0_a: the srr0 rows of all eight read-ahead sessions); the aligned compare's mask widened to bit 2 (R6_mask7: `T
blr nonex`) or to bits 2-3 (R6_mask15: `T blr nonex` and the nonex rows of all eight read-ahead sessions); arm (a)'s guard
conjoined with an alignment test, `cpu->pc == addr` or `!(cpu->pc & 3)` (R6_a_pceq, R6_a_align: the nonex rows of the six unaligned
read-ahead sessions), with a test of pc's bit 1 (R7_a_bit1, codex pass 6's B1: the nonex rows of `T ra o2`, `T ra o2m`, `T ra o3`,
`T ra o3m`) or of bit 0 (R7_a_bit0: those of `T ra odd`, `T ra o1m`, `T ra o3`, `T ra o3m`), with a test refusing an unaligned
read-ahead when ME is set (R7_a_meun, codex's B2, and its De Morgan form R7_x_unme: the nonex rows of `T ra o1m`, `T ra o2m`, `T ra
o3m`) or clear (R7_a_clun and R7_x_uncl: those of `T ra odd`, `T ra o2`, `T ra o3`), or refusing an aligned one when ME is clear
(R7_x_alcl: `T ra nonex`) or set (R7_x_alme: `T ra me nonex`) -- each cell of the grid excluded alone reds exactly its own
sessions; MSR[ME] set or cleared in arm (a) when pc != addr (R7_a_msrset, codex's B3: the msr rows of `T ra odd`, `T ra o2`, `T ra
o3`; R7_a_msrclr: those of `T ra o1m`, `T ra o2m`, `T ra o3m`); SRR0 written, or the checkstop line printed, in arm (a) when pc !=
addr (R7b_a_srr0un, R7b_a_chkun: the six unaligned srr0 or chkstop rows -- each passed all 103 rows before repair 7b), or pc
aligned there (R7b_a_pcalign: their pc rows); the read's failure test disjoined with `cpu->pc != addr` (R7_fail_unal: the pc, nonex
and addr rows of the six unaligned read-ahead sessions, with the chkstop rows of the ME-clear three and the srr0 rows of the ME-set
three -- their first fetch reads successfully at pc != addr, so the block checkstops at the entry pc (ME clear) or takes a machine
check to 0x200 (ME set), with no halt report either way; this clause listed that widening as FILED -- "no row drives" an unaligned
fetch -- until codex pass 6, R3, pointed at `T ra odd`), or conjoined with MSR[ME], with its complement, with
`translation_readahead` or with `cpu->pc != addr` (R7b_f_me, R7b_f_meclr, R7b_f_ra, R7b_f_unal; never built before table 8 --
LATE_REPLICATIONS_20261105.md rows 33 and 41): a failure the conjunct refuses skips the block and decodes the uninitialised ib, so
which rows red is stack-decided, as for W5 and D7, and each reddened only sessions whose failing fetch it refuses, as PRETABLE_8
and PRETABLE_9 predicted; and a halt sent from arm (c) to bad: at pc != addr with ME set (R8_c_meun_bad, codex pass 7's F1: the
unimpl rows of `T ra o1m`, `T ra o2m` and `T ra o3m` -- it passed all 129 rows before repair 8) or with ME clear (R8_c_clun_bad:
those of `T ra odd`, `T ra o2` and `T ra o3`, and `T blr unimpl`, which alone caught it before).  W5, D7, V7 and D12 ride on the
uninitialised or stale instruction word: which rows red is BUILD-DEPENDENT -- D12 reddened a different set in each of tables 2, 3
and 4, with `T ra nonex` in all three (table4/VERDICT.md), table 5 reddened table 4's set plus `T ra srr0`, table 6 moved D12's,
W5's and D7's sets again within the read-ahead rows (r6_20261105/table6/VERDICT.md), table 7 moved them once more -- W5 lost `T ra
me srr0`, D7 gained it, D12 traded `T ra odd pc` for `T ra me pc` and `T ra srr0` (r7_20261105/table7/VERDICT.md) -- and table 8
again on the same 103 rows: W5 regained `T ra me srr0`, and D12 dropped `T ra pc`, `T ra addr`, `T ra srr0`, `T ra o1m pc` and `T
ra o3 pc` and gained `T ra o2m pc` (r7_20261105/table8/VERDICT.md) -- and table 9 again (r7_20261105/table9/VERDICT.md) -- and the
claim is that some row reds.  V12 IS NOT PREDICTED: its outcome depends on the uninitialised fetch buffer ib -- the stale stack
word is decoded on the variant's path, and whether a row reds depends on whether that word decodes as an implemented instruction.
In table 3 it did on the `T ra` leg and a row reddened, while on the `T ra me` leg every row stayed green -- read as the word
decoding to bad:, which returns quietly during read-ahead, an INFERENCE from the all-green leg and not a measurement (this sentence
stated the decode as fact: LATE_REPLICATIONS_20261105.md row 34); table 4, on the same fix, reddened `T ra me` and left `T ra`
green; table 5 reddened both legs; table 6 the `T ra` and `T ra odd` legs; table 7 every read-ahead leg except `T ra me` and `T ra
o3m`; table 8 every one except `T ra` and `T ra o2`; table 9 every one.  A red that the stack's contents decide is counted in
neither tally.  Zero-initialising ib (filed) would make the variant deterministically green.  Green, fourteen: arm (d) or the
checkstop fallback edited (D6, D9, D10, V4, V5, V6, and R7_G2_d_msr -- the Gemini seat's pass-6 G2, arm (d)'s test made `if
(cpu->cd.ppc.msr)`) -- MEASURED unreached on pmppc (the window sweep below); arm (b) edited (D11, V2, and R7_G1_b_lt -- the Gemini
seat's G1, the aligned compare made `cpu->pc < addr`) -- with the aligned compare arm (b) is taken only when the translation moved
pc to an exception vector, which no measured session produces; arm (c)'s guard forced true (V3), and the park tested before arm (b)
as well (R5_cb) -- equivalent on every reachable entry, since running is 0 at each; arm (a) restoring running before its return
(R5_arun, and R7b_a_runun, the same write gated on pc != addr) -- disclosed below.  The shape-grid check before table 3
(r3_20261105/GRID_*.md) and the repair-pass-3 findings, each measured before its adjudication (p3_20261105/table_p3, DHALT_NOTE.md;
the ruling p3_20261105/ADJ_MYTHOS.md), placed the msr rows and `T ra chkstop`; the eight-cell table before repair 7
(r7_20261105/B123_NOTE.md) placed `T ra odd msr` and the five sessions `T ra o1m` .. `T ra o3m`; repair 7b's measurement (the same
note) placed their addr, stopped, chkstop and srr0 rows and `T ra me`'s addr and stopped, and repair 8's (the same note) the eight
unimpl rows; the other shapes are disclosed below.
  discloses, not claimed: arm (a)'s guard and its exit are claimed only at read-ahead depth 1, the only depth measured -- a
weakening of the guard, or a substitution of its exit (arm (b)'s refresh-and-return in place of the bare return), that differs
from the fix only at a deeper read-ahead is green on every row and is not claimed, and neither is arm (a) on a read-ahead fetch
whose own translation raises an exception (an ISI or 603 IMISS from memory_rw during read-ahead): read-ahead stays inside the page
the dispatch lookup has just translated, so no session produces it (this clause named deeper read-ahead only:
LATE_REPLICATIONS_20261105.md row 35); MSR is rowed on every -T session (from
repair 7: before it `T ra odd` had no msr row and this clause was false -- codex pass 6, R1), and a write to a CPU field this block
neither reads nor writes -- one that changes none of pc, SRR0, MSR or the reports -- is not claimed, nor is a write to SRR1 (only
arm (d)'s machine check writes it here, unreached on pmppc, and no session rows it), and neither is a write to running in arm (a)
(R5_arun, MEASURED green in tables 5, 6 and 7; the repair-pass-4 review): the real fetch's second halt masks it on every read-ahead
session, a window whose last word branches away would see it, and none is measured on pmppc; a mask on the aligned compare that
also clears bits above bit 3 is caught where a cleared bit is one the rowed failing fetch addresses carry -- 0x02040000 bits 18 and
25, 0x02040004 bits 2, 18 and 25, 0xfec00008 bits 3, 22-23 and 25-31 -- because arm (b) then takes that fetch (MEASURED for bits 2
and 3, R6_mask7 and R6_mask15; DERIVED, not measured, for the others: `~0x40003` against `T blr`, codex pass 6); one whose extra
cleared bits are all absent from those addresses -- bits 4-17, 19-21, 24 or above 31 (`~0x13`, for example) -- changes no rowed
fetch's arm (b) test and is not claimed (this clause said "no rowed failing fetch carries such a bit" of every bit above bit 3,
which those addresses refute: codex pass 6, R2); the read's failure test disjoined with `translation_readahead` (glm, pass 5) is
not claimed: a successful read-ahead fetch then returns through arm (a) untranslated, which costs translation throughput and
changes no guest-visible state; arm (b)'s refresh (D11, V2): repair 5 compares pc with its low two bits cleared, because an
unaligned pc keeps them through the translator's prologue (cpu->pc is assigned before addr is aligned) -- from the debugger, and
from guest code, since this fork's mtlr and its unconditional blr (X(bclr_20)) copy LR without masking them (architecturally a
branch ignores them: filed separately) -- and the bare compare sent such a pc into arm (b), which re-ran the slot (`T blr` rows it
now); arm (b) itself is reached only when the translation moved pc to an exception vector, on no measured session -- so its compare
made `cpu->pc < addr` (R7_G1_b_lt, the Gemini seat's pass 6; MEASURED green, r7_20261105/B123_NOTE.md) is not claimed: wherever the
fix skips arm (b) the aligned pc equals addr and pc is not below it, and the taken side has no producer, because cpu_dyntrans.c's
lookup re-translates every page without host memory and delivers the exception itself before the translator runs -- also when
MSR[IP] puts the vector above the fetch (r7_20261105/g12_table/explore); WITHOUT -T the guest-made unaligned fetch reads zeros and
stops on the zero word, so no arm of the block runs (MEASURED, p4_20261105/AC_NOTE.md) and no no-T `blr` session is rowed; arm (d)
and the checkstop fallback (D6, D9, D10, and R7_G2_d_msr -- arm (d)'s test made `if (cpu->cd.ppc.msr)`, the Gemini seat's pass 6,
MEASURED green; with V4 and V5 green no predicate in that position is observable): no fetch on pmppc reaches them -- MEASURED by a
fetch at every 4-byte offset of every window `device list` names, MSR 0 and MSR[ME], each offset with evidence the word was fetched
(det_20261104/window_sweep.out), and in the slack above RAM (slack_sweep.out); their producer is a device declining an instruction
fetch while running, which needs another machine (the reconciliation's ROW 5, FILED pending X11), and it is the only producer of a
read-ahead fetch that fails with running still 1 -- every rowed read-ahead failure is a -T halt, which clears running before the
read returns -- so arm (a)'s guard conjoined with `!cpu->running` (the Gemini seat's pass-6 replication, G3; not built) is
equivalent on pmppc and not claimed; 64-bit CPUs; PPC603-class CPUs (their miss vector is 0x10); IR-on fetches whose translation
succeeds onto non-existent memory; a successful slow-path fetch with running already 0 (glm's `|| !running` widening of the failure
test) -- no measured single-CPU shape produces one: a -T data halt ends the run at the faulting load or store
(p3_20261105/DHALT_NOTE.md), and the one producer that measurement cannot see is another CPU mid-batch after memory.c's -T halt
cleared every CPU's running (#PPP).  THE READ-AHEAD CELLS are measured on cpc700_pci (the eight sessions `T ra`, `T ra me`, `T ra
odd`, `T ra o1m`, `T ra o2`, `T ra o2m`, `T ra o3`, `T ra o3m`: pc's low two bits x MSR[ME]); at the other seven windows' last
words the word a guest load records before the continue is 0x00000000, which decodes as unimplemented, so no read-ahead past the
window is issued (part 2: no halt report) -- MEASURED at that word, DERIVED for other values of those registers: a window end
inside a page puts the failing word in reach of read-ahead, and whether read-ahead happens depends on the decoded word (cpc700_pci
shows a valid non-branch word reaches it).  Read-ahead runs only on a free-running continue: single-step disables it (measured,
artifacts/qhslowifetch/p2r_20261105/extra_sessions.out), and so do instruction trace and any set breakpoint (cpu_dyntrans.c's
read-ahead condition, by code reading).  The RTC window ran twice and read 0 at +0xfc both times.
  RE-ENTRY -- every exit returns before the slot's function pointer is replaced, so the slot stays untranslated.  Re-entry after
arm (a)'s exit is measured by `T ra`: the slot stays untranslated and the real fetch re-enters the arm in the same batch (the
second report).  Re-entry after arm (c)'s exit is untestable here: the park ends the batch and running is clear, so nothing
fetches the slot again; the `again` session therefore measures nothing about re-entry after a park and stands as the control
that the debugger survives step and continue on a halted CPU, its halt-count row the control that a -T halt is terminal for the
session.  W5's catch rides on the uninitialised instruction word: which rows red under W5 depends on the garbage decoded, though
some row must (a decoded word moves pc, traps or prints UNIMPLEMENTED; one that branches back to its own slot changes nothing on
that session -- `T blr` stays green under R7b_f_me and R7b_f_ra -- so the claim rests on the other sessions).  -T imprecision: a -T
data halt earlier in the same batch followed by a declined fetch takes arm (c), with no machine check (cosmetic; the debugger is
entered either way). The reconciliation's W7 (the read-ahead guard missing) is rowed by `T ra`; its W8 (the running-1 arm missing)
and W9 (a wrong machine check) have no row on pmppc: they need its ROW 5 (FILED pending X11).  On this 137-row probe the pre-fix
build scores 61/137 (76 rows red) with PPC_IFETCH_SYMPTOM=PRESENT, and the three null media -- /bin/true 55/137, an absent binary
38/137, /bin/false 39/137 -- each CONTROL=FAIL (r7_20261105/table9/SCORES.txt).

Sentinel: PPC_IFETCH_PROBE_DONE (plus PPC_IFETCH_RESULT=n/N, PPC_IFETCH_CONTROL=OK|FAIL, PPC_IFETCH_SYMPTOM=PRESENT|ABSENT,
PPC_IFETCH_RED=none|<names>).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_ifetch_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="ppc_ifetch_")
NOP = os.path.join(_TMPDIR, "nop.bin")
open(NOP, "wb").write(bytes([0x60, 0x00, 0x00, 0x00]))      # ori r0,r0,0 (big-endian)

ENTRY = 0x2000
SENT = 0x11111111            # the SRR0 sentinel; only an exception entry overwrites it in these runs
ISI_PC = 0x20000000          # a reset-BAT gap on the PPC750: no IBAT covers it, SDR1 = 0, so translation misses
MSR_IR = 0x20
MSR_ME = 0x1000              # PPC_MSR_ME, cpu_ppc.h: arm (d)'s test
NOMEM = 0x02040000           # past 32 MB of RAM and the 256 KB SILENT slack above it (core/memory.c:605), so `-T` fails the read
FATAL = "read failed: TODO"  # the translator's text at the exit
AGAIN_NONEX = 2             # ROW 3: frozen from the first run on the fixed build.  A -T halt leaves running at 0, so a second step
                             # or continue runs nothing (D3 and D4: the same count without the park; FINDING_D8.md's correction)

rows = []
controls = []
symptom_hits = 0


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def session(name, cmds, flags=(), machine="pmppc", timeout=60):
    """One cold debugger run: `cmds` then `reg` and `quit`.  Returns (regs, text, how)."""
    global symptom_hits
    allc = list(cmds) + ["reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine] + list(flags) + ["0x%x:%s" % (ENTRY, NOP)]
    inp = ("\n".join(allc) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every session row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(allc) + "\n--- transcript (%s) ---\n" % how + t)
    if FATAL in t:
        symptom_hits += 1
    regs = {}
    idx = t.rfind("GXemul> reg")
    if idx >= 0:
        seg = t[idx:]
        for key in ("pc", "srr0", "srr1", "msr", "lr"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % key, seg)
            if m:
                regs[key] = int(m.group(1), 16)
    return regs, t, how


def hexr(regs, k):
    return hex(regs[k]) if k in regs else "none"


def text(t):
    return "present" if FATAL in t else "absent"


def prompt(t):
    return "yes" if ("GXemul> reg" in t and "cpu0: pc" in t) else "no"


def nonex(t):
    """How many `-T` halt reports the run printed (memory_rw's "non-existant" line)."""
    return str(t.count("non-existant"))


def halts(t):
    """The distinct addresses the -T halt reports name, sorted ("none" when there is no report)."""
    return ",".join(sorted(set(re.findall(r"non-existant paddr=(0x[0-9a-fA-F]+)", t)))) or "none"


def stopped(t):
    """Whether the run printed the emulator's stop line (every CPU's running cleared)."""
    return "yes" if "All machines stopped" in t else "no"


def unimpl(t):
    return "present" if "UNIMPLEMENTED" in t else "absent"


def exc(t):
    return "present" if "[ PPC Exception" in t else "absent"


def chk(t):
    """The (d) arm's checkstop text.  MSR[ME] is clear on T step, T cont and again (msr = 0; T me sets it), so on those an arm (c)
    that is deleted or inverted falls to the checkstop fallback -- same pc, SRR0 and park -- and this text is the one channel that
    differs."""
    return "present" if "checkstop" in t else "absent"


print("qhslowifetch DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E pmppc (UNMODIFIED in-tree; Artesyn PM/PPC, PPC750, 32 MB); `ori r0,r0,0` loaded raw at 0x%x" % ENTRY)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

# ============================================================ CONTROL SESSIONS ==
regs, T, how = session("ctl", ["srr0=0x%x" % SENT, "step 1"])
row("ctl session", how, "exit0", "the control session's exit status", control=True)
row("ctl live", hexr(regs, "pc"), hex(ENTRY + 4), "the loaded word executed (one step)", control=True)
row("ctl srr0 kept", hexr(regs, "srr0"), hex(SENT), "a good fetch delivers no exception", control=True)
nregs, _, nhow = session("neg", ["step 1"], machine="nosuchmachine", timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hexr(nregs, "pc")), "exit1/none", "a bogus machine runs no guest", control=True)
regs, T, how = session("isi", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_IR, "pc=0x%x" % ISI_PC, "continue"])
row("isi session", how, "exit0", "IR on, fetch in a BAT gap: survives", control=True)
row("isi srr0", hexr(regs, "srr0"), hex(ISI_PC), "the ISI was delivered (SRR0 = fault PC)", control=True)
row("isi pc", hexr(regs, "pc"), hex(0x400), "resumed at the ISI vector (zero word stops)", control=True)
row("isi text", text(T), "absent", "the translator's exit is not on this route", control=True)
row("isi nonex", nonex(T), "0", "premise: no -T report on the ISI route (W6)", control=True)
regs, T, how = session("isi1", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_IR, "pc=0x%x" % ISI_PC, "step 1"])
row("isi1 session", how, "exit0", "IR on, one step into the BAT gap: survives", control=True)
row("isi1 srr0", hexr(regs, "srr0"), hex(ISI_PC), "premise: the lookup delivers the ISI (W6)", control=True)
row("isi1 pc", hexr(regs, "pc"), hex(0x400), "premise: the step lands on the ISI vector", control=True)
row("isi1 nonex", nonex(T), "0", "premise: no -T report on the ISI step", control=True)
regs, T, how = session("noT", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"])
row("noT session", how, "exit0", "no -T: the read past RAM zero-fills", control=True)
row("noT pc", hexr(regs, "pc"), hex(NOMEM), "the CPU stopped on the zero word", control=True)
row("noT srr0 kept", hexr(regs, "srr0"), hex(SENT), "no exception on that route", control=True)
row("noT unimpl", unimpl(T), "present", "the zero word is reported unimplemented (the read succeeded)")
row("noT chkstop", chk(T), "absent", "a successful read never enters the failure arm")

# ========================================================= THE WITNESS ROWS (-T) ==
regs, T, how = session("T cont", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "continue"], flags=["-T"])
row("T cont session", how, "exit0", "-T fetch past RAM, continue: survives")
row("T cont text", text(T), "absent", "no `read failed: TODO` exit")
row("T cont prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")
row("T cont pc", hexr(regs, "pc"), hex(NOMEM), "parked at the fetch address (W2, W5)")
row("T cont srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on the -T route (W4)")
row("T cont nonex", nonex(T), "1", "exactly one halt report: the loop stopped (W2)")
row("T cont unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented (W3)")
row("T cont exc", exc(T), "absent", "no exception entry on the -T route (W4)")
row("T cont chkstop", chk(T), "absent", "arm (c) parked it; the checkstop arm did not run")
row("T cont msr", hexr(regs, "msr"), hex(0), "the park leaves MSR as it was (B1c)")
regs, T, how = session("T step", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1"], flags=["-T"])
row("T step session", how, "exit0", "-T fetch past RAM, step: survives")
row("T step text", text(T), "absent", "no `read failed: TODO` exit")
row("T step prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")
row("T step pc", hexr(regs, "pc"), hex(NOMEM), "parked at the fetch address (W2: a bare return moves it)")
row("T step srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on the -T route (W4)")
row("T step nonex", nonex(T), "2", "premise: single-step read + translator read", control=True)
row("T step unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented (W3)")
row("T step exc", exc(T), "absent", "no exception entry on the -T route (W4)")
row("T step chkstop", chk(T), "absent", "arm (c) parked it; the checkstop arm did not run")
row("T step msr", hexr(regs, "msr"), hex(0), "the park leaves MSR as it was (B1c)")
# The floor cell the merged rows left empty (the pre-table check, 2026-11-04): arm (d) TESTS MSR[ME], and MSR is 0 on every -T
# session above, so the -T halt with ME SET is driven here -- arm (c) must still park it, not deliver a machine check.
regs, T, how = session("T me", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_ME, "pc=0x%x" % NOMEM, "step 1"], flags=["-T"])
row("T me session", how, "exit0", "-T halt with MSR[ME] set: survives")
row("T me pc", hexr(regs, "pc"), hex(NOMEM), "parked, not at the 0x200 machine-check vector")
row("T me srr0", hexr(regs, "srr0"), hex(SENT), "no machine check delivered on the -T route")
row("T me nonex", nonex(T), "2", "premise: the same two reports with ME set", control=True)
row("T me text", text(T), "absent", "no `read failed: TODO` exit")
row("T me exc", exc(T), "absent", "no `[ PPC Exception 0x2` on the -T route")
row("T me unimpl", unimpl(T), "absent", "an ME-set halt is not sent to bad: (V10)")
row("T me chkstop", chk(T), "absent", "an ME-set halt does not take the checkstop (V11)")
row("T me msr", hexr(regs, "msr"), hex(MSR_ME), "the park leaves MSR[ME] set (B1a)")
regs, T, how = session("again", ["srr0=0x%x" % SENT, "pc=0x%x" % NOMEM, "step 1", "step 1", "continue", "continue"], flags=["-T"])
print("again: measured non-existant count = %s" % nonex(T))
row("again session", how, "exit0", "a second step and a second continue after the halt survive")
row("again pc", hexr(regs, "pc"), hex(NOMEM), "still parked: no translated zero slot ran (W5)")
row("again srr0", hexr(regs, "srr0"), hex(SENT), "still no exception entry (W4)")
row("again nonex", nonex(T), str(AGAIN_NONEX), "premise: a -T halt is terminal (repeats run nothing)", control=True)
row("again text", text(T), "absent", "no `read failed: TODO` exit on the repeats")
row("again unimpl", unimpl(T), "absent", "a translated zero slot would print UNIMPLEMENTED (W5)")
row("again exc", exc(T), "absent", "no exception entry on the repeats (W4)")
row("again chkstop", chk(T), "absent", "arm (c), not the checkstop arm, on every repeat")
row("again prompt", prompt(T), "yes", "the debugger ran `reg` after the repeats")
row("again msr", hexr(regs, "msr"), hex(0), "the repeats leave MSR as it was (B1c)")

# The read-ahead cell (FINAL_FABLE.md F4; found by det_20261104/window_sweep.out): cpc700_pci's last word, 0xfec00004, reads
# 0x23120e00 in its reset state -- subfic r24,r18,0xe00 -- so translating it reads ahead into 0xfec00008, past the 8-byte window.
# The -T halt fires DURING read-ahead and arm (a) returns; the subfic runs; the real fetch of 0xfec00008 halts again and arm (c)
# parks.  Two halt reports, both naming 0xfec00008.
RA_LAST = 0xfec00004         # cpc700_pci's data word: the window's last word
RA_NEXT = 0xfec00008         # past the window: no device answers it
regs, T, how = session("T ra", ["srr0=0x%x" % SENT, "pc=0x%x" % RA_LAST, "continue"], flags=["-T"])
row("T ra session", how, "exit0", "-T read-ahead past cpc700_pci: survives")
row("T ra pc", hexr(regs, "pc"), hex(RA_NEXT), "parked at the word past the window")
row("T ra nonex", nonex(T), "2", "the read-ahead's halt, then the real fetch's (W7)")
row("T ra addr", halts(T), hex(RA_NEXT), "every halt names the word past the window")
row("T ra stopped", stopped(T), "yes", "the -T halt stopped the machine (running 0)")
row("T ra msr", hexr(regs, "msr"), hex(0), "the read-ahead route leaves MSR as it was (B1c)")
row("T ra chkstop", chk(T), "absent", "no checkstop line on the read-ahead route (B2)")
row("T ra srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on the read-ahead route")
row("T ra unimpl", unimpl(T), "absent", "the real fetch is not sent to bad: (W3)")
# Arm (a)'s guard with MSR[ME] SET (the adjudication of repair pass 2, Q1: GLM's floor gap).  `T ra` runs with MSR 0, so a guard
# conjoined with an ME-clear test is invisible there; with ME set that conjunct sends the read-ahead failure past arm (a) to
# arm (c)'s park -- one report where the fix gives two (the base side: artifacts/qhslowifetch/p2r_20261105/tra_me_base.out).
regs, T, how = session("T ra me", ["srr0=0x%x" % SENT, "msr=0x%x" % MSR_ME, "pc=0x%x" % RA_LAST, "continue"], flags=["-T"])
row("T ra me session", how, "exit0", "-T read-ahead with MSR[ME] set: survives")
row("T ra me pc", hexr(regs, "pc"), hex(RA_NEXT), "parked at the word past the window")
row("T ra me nonex", nonex(T), "2", "arm (a) returns on read-ahead with ME set (V8)")
row("T ra me addr", halts(T), hex(RA_NEXT), "every halt names the word past the window (W2, D3)")
row("T ra me stopped", stopped(T), "yes", "the -T halt stopped the machine (B1)")
row("T ra me chkstop", chk(T), "absent", "the real fetch parks, not a checkstop (V11)")
row("T ra me msr", hexr(regs, "msr"), hex(MSR_ME), "MSR[ME] stays set through read-ahead and park (B1a, B1b)")
row("T ra me srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented with ME set")
row("T ra me unimpl", unimpl(T), "absent", "the real fetch is not sent to bad: (W3, V10)")
# `T ra` entered at the UNALIGNED pc 0xfec00005 (repair 6; Mythos pass-5 breach 2, p5_20261105/TRAODD_NOTE.md): the prologue
# keeps pc's low two bits, so the read-ahead fetch reaches the failure block with pc != addr.  The fix's arm (a) returns and the
# real fetch halts again: two reports, the park at 0xfec00009.  A guard conjoined with an alignment test sends the read-ahead
# failure on to arm (c), which parks it at read-ahead time: one report.  No breakpoint, so read-ahead runs.
RA_ODD = 0xfec00005
regs, T, how = session("T ra odd", ["srr0=0x%x" % SENT, "pc=0x%x" % RA_ODD, "continue"], flags=["-T"])
row("T ra odd session", how, "exit0", "-T read-ahead from an unaligned pc: survives")
row("T ra odd pc", hexr(regs, "pc"), hex(RA_NEXT | 1), "parked past the window, the low bit kept")
row("T ra odd nonex", nonex(T), "2", "the read-ahead halt, then the real fetch (arm (a) at pc != addr)")
row("T ra odd addr", halts(T), hex(RA_NEXT), "every halt names the word past the window (W2, D3)")
row("T ra odd stopped", stopped(T), "yes", "the -T halt stopped the machine (B1)")
row("T ra odd msr", hexr(regs, "msr"), hex(0), "MSR as entered: arm (a) writes no MSR (R7_a_msrset)")
row("T ra odd chkstop", chk(T), "absent", "no checkstop line on this route (R7b_a_chkun)")
row("T ra odd srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on this route (R7b_a_srr0un)")
row("T ra odd unimpl", unimpl(T), "absent", "the real fetch is not sent to bad: (W3, R8_c_clun_bad)")
# THE ARM (a) CLASS CLOSURE (repair 7; codex pass 6, r7_20261105/B123_NOTE.md).  Passes 5 and 6 both found arm (a) x alignment cells
# unrowed, so the read-ahead route is crossed over pc's low two bits {00, 01, 10, 11} x MSR[ME] {clear, set}: `T ra`, `T ra me` and
# `T ra odd` hold three cells and these five sessions the rest -- `T ra` entered at 0xfec00004 | low bits, MSR written only when ME
# is set (`m`).  The prologue keeps pc's low bits, so the read-ahead fetch reaches the failure block at pc 0xfec00008 | low bits; arm
# (a) returns, the subfic runs, the real fetch halts again and arm (c) parks at that pc: exit 0, that pc, two reports naming
# 0xfec00008, the stop, MSR as entered, no checkstop line, SRR0 untouched and no UNIMPLEMENTED text -- `T ra`'s nine channels
# (repair 7b; `unimpl`, repair 8).  A guard that refuses a cell parks it at read-ahead time instead (one report); an MSR or SRR0
# write, a checkstop print, or a transfer to bad: from the real fetch (where bad: prints UNIMPLEMENTED and changes nothing else; a
# read-ahead transfer returns silently -- this comment said "a transfer to bad: (which prints UNIMPLEMENTED ...)", codex pass 8, R1)
# shows in its own row.
for tag, low, msr, kills in (("o1m", 1, MSR_ME, "R7_a_meun"), ("o2", 2, 0, "R7_a_bit1, R7_a_clun"),
                             ("o2m", 2, MSR_ME, "R7_a_bit1, R7_a_meun"), ("o3", 3, 0, "R7_a_bit1, R7_a_bit0, R7_a_clun"),
                             ("o3m", 3, MSR_ME, "R7_a_bit1, R7_a_bit0, R7_a_meun")):
    nm = "T ra " + tag
    regs, T, how = session(nm, ["srr0=0x%x" % SENT] + (["msr=0x%x" % msr] if msr else []) + ["pc=0x%x" % (RA_LAST | low), "continue"],
                           flags=["-T"])
    row(nm + " session", how, "exit0", "-T read-ahead, pc&3 = %d, ME %s: survives" % (low, "set" if msr else "clear"))
    row(nm + " pc", hexr(regs, "pc"), hex(RA_NEXT | low), "parked past the window, low bits kept (R7_fail_unal)")
    row(nm + " nonex", nonex(T), "2", "arm (a) returns at this cell (%s)" % kills)
    row(nm + " addr", halts(T), hex(RA_NEXT), "every halt names the word past the window (W2, D3)")
    row(nm + " stopped", stopped(T), "yes", "the -T halt stopped the machine (B1)")
    row(nm + " msr", hexr(regs, "msr"), hex(msr), "MSR as entered (%s)" % ("R7_a_msrclr" if msr else "R7_a_msrset"))
    row(nm + " chkstop", chk(T), "absent", "no checkstop line on this route (R7b_a_chkun)")
    row(nm + " srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented on this route (R7b_a_srr0un)")
    row(nm + " unimpl", unimpl(T), "absent",
        "the real fetch is not sent to bad: (%s)" % ("W3, V10, R8_c_meun_bad" if msr else "W3, R8_c_clun_bad"))
# Arm (b) with a guest-made UNALIGNED pc (repair pass 4; p4_20261105/BLR_NOTE.md, ADJ_MYTHOS.md): this fork's mtlr and its
# unconditional blr (X(bclr_20)) copy LR unmasked and the translator's prologue aligns addr but not pc, so `mtlr r3; blr` reaches the
# failure block with pc != addr.  Before repair 5 arm (b) took it, refreshed and re-ran the slot: 8278 halt reports under -T.  With
# the aligned compare the fetch parks in arm (c).  r3 = 0x02040007 has bits 0-2 set (repair 6; p5_20261105/MASK7_NOTE.md): the
# prologue gives addr 0x02040004, so a mask narrowed to either low bit (`& ~1`, `& ~2`) or widened to bit 2 (`& ~7`) still floods.
# The program is written with `put b` (byte stores do not warm translations); a far breakpoint disables read-ahead.
BLR_PC = 0x02040007
cmds = ["srr0=0x%x" % SENT, "r3=0x%x" % BLR_PC]
for i, w in enumerate((0x7C6803A6, 0x4E800020)):          # mtlr r3 ; blr
    for j in range(4):
        cmds.append("put b 0x%x,0x%02x" % (ENTRY + 4 * i + j, (w >> (24 - 8 * j)) & 0xff))
regs, T, how = session("T blr", cmds + ["breakpoint add 0x3000", "continue"], flags=["-T"])
row("T blr session", how, "exit0", "-T fetch at a guest-made unaligned pc: survives")
row("T blr pc", hexr(regs, "pc"), hex(BLR_PC), "parked at the unaligned pc (arm (c))")
row("T blr nonex", nonex(T), "1", "one halt report: the slot is not re-run (repair 5)")
row("T blr srr0", hexr(regs, "srr0"), hex(SENT), "no exception invented")
row("T blr msr", hexr(regs, "msr"), hex(0), "MSR unchanged")
row("T blr chkstop", chk(T), "absent", "arm (c) parked it; no checkstop")
row("T blr unimpl", unimpl(T), "absent", "the halt is not reported as unimplemented")
row("T blr lr", hexr(regs, "lr"), hex(BLR_PC), "LR holds the stored value (mtlr writes all bits)")
# ONE-ENTRY FAILURES AT EVERY UNALIGNED PATTERN (repair 9; codex pass 8, B1; r7_20261105/B123_NOTE.md).  Every read-ahead session
# enters the failure block TWICE -- the read-ahead failure, then the real fetch -- so a change the block makes on pc's low bits and
# makes again on the second entry (a toggle) cancels before the final state is read.  A one-entry failure sees it once: `T cont`,
# `T step`, `T me` and `again` hold low bits 00, `T blr` holds 11, and these two hold 01 and 10 -- `T blr` with r3 = 0x02040005 /
# 0x02040006; the breakpoint keeps read-ahead off, so the failing fetch enters the block once and arm (c) parks it.
BLR_PUTS = cmds[2:]
for tag, target, bits, togs, floods in (("o1", 0x02040005, "01", "R9_tog_me1", "R5_mask2"),
                                        ("o2", 0x02040006, "10", "R9_tog_me2", "R5_mask1")):
    nm = "T blr " + tag
    regs, T, how = session(nm, ["srr0=0x%x" % SENT, "r3=0x%x" % target] + BLR_PUTS + ["breakpoint add 0x3000", "continue"],
                           flags=["-T"])
    row(nm + " session", how, "exit0", "-T fetch at a guest-made pc, low bits %s: survives" % bits)
    row(nm + " pc", hexr(regs, "pc"), hex(target), "parked at the unaligned pc (arm (c))")
    row(nm + " nonex", nonex(T), "1", "one halt report: one entry, the slot not re-run (%s)" % floods)
    row(nm + " srr0", hexr(regs, "srr0"), hex(SENT), "SRR0 as entered: one entry, no toggle cancels (R9_tog_srr0_1)")
    row(nm + " msr", hexr(regs, "msr"), hex(0), "MSR as entered: one entry, no toggle cancels (%s)" % togs)
    row(nm + " chkstop", chk(T), "absent", "arm (c) parked it; no checkstop")
    row(nm + " unimpl", unimpl(T), "absent", "the halt is not sent to bad:")
    row(nm + " lr", hexr(regs, "lr"), hex(target), "LR holds the stored value")

# ===================================================================== RESULT ==
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_IFETCH_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_IFETCH_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("PPC_IFETCH_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("PPC_IFETCH_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("PPC_IFETCH_PROBE_DONE")
