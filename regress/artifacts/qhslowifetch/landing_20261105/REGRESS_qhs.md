Begin your answer with the token MYTHOSREGQHS on its own line, then `model: <your model name>`, then your verdict line.  You may
open files under C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/ READ-ONLY to check a claim; write nothing, build nothing, run no git command
that writes.  The tree under review is GXEMUL-SEC/src/ and GXEMUL-SEC/regress/; ignore any other src/ you find (the project root
holds pristine 2021 upstream copies).  The probe, the gate block and the fix below are the STAGED copies the commit will carry; the
working tree's regress/gate_ppc.sh and src/cpus/cpu_ppc_instr.c also hold round #575's uncommitted change, so read them HERE.

# REGRESS REVIEW (the Fable-only stage) -- round #581 `qhslowifetch`: the detector as it will ship

**PROJECT FRAMING -- this is a defensive software-robustness project.**  GXemul is a computer-architecture emulator: a developer tool
that runs legacy operating systems in a software sandbox for research and preservation.  This fork is a HARDENING effort -- ordinary
software-correctness engineering on the emulator's own C code, each fix shipped with a regression test that keeps it fixed.  There is
no attack, no target system and no affected third party; the guest is a few instruction words under test INSIDE the emulator, and the
host is the emulator process on the developer's own machine.  This round removes a place where the emulator ENDED ITS OWN PROCESS
when an instruction fetch failed.  **Vocabulary**: a *test variant* is a deliberately broken copy of the fix used to measure whether
the regression test notices it; *red* = a row went red (detected); *green* (a variant) = every row passed; a *null medium* is a run
with no working emulator behind the probe (a non-emulator binary, a missing one); a *two-entry session* is one whose failing fetch
reaches the fix's code twice (first during translation read-ahead, then as the real fetch); a *one-entry session* reaches it once;
a *partner* is a one-entry session at the same full pc and MSR as a two-entry one.

**Your role: the flagship's REGRESS review**, the fable5 slot's step.  By standing owner directive only the flagship seat reviews
the `regress` stage.  THE ROUND: `src/cpus/cpu_ppc_instr.c`, X(to_be_translated) -- the PowerPC translator read the instruction
word with memory_rw and, when that read FAILED, printed `read failed: TODO` and called exit(1).  The fix (block G, one hunk; plus one
line in `src/include/cpu_ppc.h`, the PPC_EXCEPTION_MC define its machine-check arm uses) gives the failed read four exits and a
fallback: (a) read-ahead returns untouched; (b) a fetch whose translation already delivered an exception (pc, low two bits cleared,
!= addr) refreshes next_ic and returns; (c) a -T halt (memory.c cleared running) parks the CPU on nothing_call at the fetch's pc;
(d) a device declining an instruction-width read while running delivers a machine check when MSR[ME] is set; the fallback (ME
clear) prints a checkstop line, clears running and parks.  The rung-3 witness (block H2) measured the exit on the committed build
under `-E pmppc -T`.  The detector is regress/ppc_ifetch_probe.py (249 rows, 31 cold `-E pmppc` debugger sessions; block A, whose
header is the CONTRACT) in gate 13 (block B).  It grew through twelve numbered test-variant tables on probes of 50 to 249 rows (the
gate comment lists them); the repair chain ran passes 2r through 11 on the diff.  From pass 6 on, glm-5.3 and grok-4.7 were walled,
Gemini 4 Argon answered some passes late or in part, and passes 10 and 11 had ONE answering seat, GPT-6 Astra (the dispositions
name each seat: block F2 and p6..p10_20261105/DISPOSITION.md).  Passes 8, 9 and 10 each found a member of ONE family -- a state
change the fix's code makes and makes again on the second entry, so a two-entry session cancels it -- and repair 11 closed it
STRUCTURALLY with eight partners (block D).  Pass 11 found the family's first member whose marker is a bit the code never tests
(MSR[RI]); the ruling (block F1, local Claude Mythos 5.1) graded it clause-(e) DEBT, upheld two false records, and closed the
round after records corrections.  Those corrections were then read three times by GPT-6 Astra until a reading found nothing
(block F3: 2, 2, then 0 items to fix).  NO SEAT HAS REVIEWED THE DETECTOR AS IT WILL LAND as one object -- the 249-row probe after
the records chain, with two staged-only docstring edits, and the 249-row gate block -- and gate 13 last ran this block IN SITU
on the 56-row probe (block H2), so this review is also the first reading of the 249-row block's pins (block H1 replays them
over table 12's banked logs; the in-situ run is owed at landing).

Mark each claim CHECKED-IN-PACKET (block + line), CHECKED-IN-TREE (file:line you opened), REASONED, or UNSETTLED (name the one
measurement that settles it -- the main loop runs it).  A finding is fixed in this round only if it is a floor breach (L2), an
undischarged obligation (L3) or a wrong record (L4); everything else is FILED with its warrant.  Rows are owed per enumerated wrong
version of the fix inside the DEPENDS-ON bound (the predicates dominating the edited lines, walked to the enclosing function; operand
swaps only from fields the guarded body reads; joint cells only where the body's own tests distinguish them, and the FLOOR is the
guard's dominating predicates crossed with the state lvalues the repair path reads that are jointly reachable; at each floor cell
every bit the body TESTS -- masks or compares as a case -- is held both clear and set), never per possible state; a filter may
reject or repair a row, never demand one outside the bound.  Count the arguments, not the seats: an agreement that only restates a
packet's premise is no evidence.

**PREMISES PUT AS QUESTIONS -- please do not simply ratify; on this project seven of nine seats once confirmed a premise a brief
stated wrongly.  Check each against the tree:**
* P1. I believe the floor is: the read's failure test, then arm (a)'s `translation_readahead`, arm (b)'s `(pc & ~3) != addr`, arm
  (c)'s `!running` and arm (d)'s `msr & ME`, crossed with what is jointly reachable on pmppc -- pc's low two bits {00, 01, 10, 11} x
  MSR[ME] {clear, set} x {two-entry, one-entry}, every session pinning MSR and SRR0 -- the state the code writes -- among its
  channels (block A, THE GRID IS NOW HELD WHOLE), plus a partner per two-entry cell.  Is any dominating predicate or body-read
  lvalue missing (`page != NULL`, which selects this path; the prologue's `addr`; next_ic, written and never read)?
* P2. I believe arm (b)'s taken side, arm (d) and the checkstop fallback are DISCLOSED rather than floor: no fetch on pmppc reaches
  them (MEASURED by det_20261104/window_sweep.out and slack_sweep.out), and (d)'s producer needs another machine.  Table 12's
  fourteen green variants: seven in arm (d) or the fallback, three in arm (b)'s taken side, two (V3, R5_cb) equivalent wherever
  running is 0, and two (R5_arun, R7b_a_runun: arm (a) restoring running) masked by the real fetch's second halt on every rowed
  read-ahead session (block A's disclosures).  Is each correctly placed?  Does another machine in this tree reach (d) -- and if
  one does, is shipping two arms no row reaches still consistent with the floor?
* P3. I believe the pairing invariant (rec13's first-visit sentence) is true and, with the generating-set rows, catches every
  member of the toggle family whose marker is a TESTED bit -- the ruling DERIVED, did not measure, that a self-referential
  toggle on MSR[ME] or on pc's low bits reds -- leaving only untested markers (MSR[RI], PMM, LE, an SRR0 bit clear in the
  sentinel), graded clause-(e) debt.  Is a measurement of those two derived kills owed (L3), or is the derivation enough?
* P4. I believe clause (c) is `measured at` table12/probe_null_true.out, probe_null_absent.out, probe_null_false.out (94, 64 and 65
  of 249, CONTROL=FAIL on all three).  For a translator arm rather than an instruction handler, is the binary null medium the
  right object, or should the record also name W2 (the arm emptied to a bare return, 184/249) in the identity-body form?
* P5. I believe every one of the gate block's checks can fail (block H1 replays it over 93 banked and 13 synthetic logs).  Can
  any not?
* P6. I believe the four build-dependent variants (W5, D7, V7, D12), the four failure-test narrowings (R7b_f_*) and V12 (NOT
  PREDICTED, counted in neither tally) are correctly disclosed: each rides on the uninitialised `ib` buffer and the contract claims
  only that some row reds.  Does any floor cell rest on a stack-decided red?
* P7. The gate comment (block B) states the pairing guarantee a third time -- "a toggle that cancels over the two-entry
  session's two visits, under a condition on state the block reads that the toggle itself leaves unchanged, shows once on its
  partner".  rec11 accepted that comment; rec12 and rec13 then cut the docstring and the partner-loop comment down to the
  first-visit core, and rec13's denominator is "the two sites, their context" (block F3).  I believe the gate's sentence is
  true as written.  Is it, and is it consistent with rec13's sentence (whose condition reads only the pair's shared entry
  state, where this one's may read translation_readahead)?

**Write your answer in this order** (it is banked as regress/artifacts/qhslowifetch/regress_20261105/REG_MYTHOS_local.md):
1. Evidence basis (which blocks and which files you opened).
2. The vacuity floor, clause by clause, each with the artifact that discharges it or the breach: (a) the pre-fix build fails;
   (b) a verbatim reinstatement of the removed defect at every fixed site fails (B1_exit_head); (c) a null medium fails (P4); (d)
   null-repair over the DEPENDS-ON floor (P1, P2, P3); (e) the contract in the probe header: true as written, and complete for what
   table 12 measured -- the fourteen green, the build-dependent and NOT PREDICTED variants, the self-referential family, the
   read-ahead depth limit; (f) anchors -- which rows pin WHICH value (the park pc, SRR0's sentinel, the final MSR, the halted
   address) rather than only that something changed?  If the fix moved the park one word, which row reds?
3. Gate 13's qhs block (block B): does every pin red under (i) a dead probe, (ii) a probe that silently loses rows, (iii) a probe
   that adds a row, (iv) a probe whose sentinel prints but whose RESULT line is missing?  Name any pin that cannot fail.  Does
   block H1 show what it claims?  Is the block's comment true?
4. The tables (blocks C1, C2, D; PRETABLE_12.out and B123_NOTE.md by path): is any row VACUOUS by construction (its observable
   cannot vary under the variant it is meant to catch)?  Block H1 lists the rows no banked log ever reddened, null media
   included.  Is any detection credited to a different row than the record claims?
5. Records: wrong numbers or claims in the probe header (block A), the gate comment (block B), table 12's verdict (block C2), the
   ruling (block F1), the dispositions (block F2) and the records chain (block F3).  The probe's text says some items are
   "(filed)", "filed separately" or "FILED pending X11", and the fix's comments cite #MMM, #QQQ and #PPP: the landing files those
   rows and fills the placeholders, so read them as owed filings, and say whether any claim depends on one.  P7 is here too.
6. The main loop's dispositions: which accepted disposition is wrong?  Counted (block F2): pass 6 -- codex 3 breaches and 3 false
   records, Gemini G1-G3 (G1, G2 measured green and disclosed; G3 inside the stated non-coverage); passes 7 and 8 -- one breach and
   one false record each; passes 9 and 10 -- one breach and two false records each, one of the two in each a packet error of the
   main loop's; pass 11 -- one finding graded debt by the ruling and two false records upheld; the records chain rec11 (6 accepted,
   2 to fix), rec12 (0, 2), rec13 (2, 0).  Is the zero-floor disposition right, given that pass 11 rests on one answering seat?
7. Which of your own findings is weakest, and what would overturn it.
Final line: `MYTHOSREGQHS: <n> CHECKS <b> FLOOR-BREACHES <r> RECORD-FINDINGS VERDICT:<REGRESS-CLEAN|REGRESS-WITH-FINDINGS|REGRESS-BREACH>`

Files you may open (READ-ONLY), under regress/artifacts/qhslowifetch/: r7_20261105/PRETABLE_12.out (written before table 12), table12/SCORES.txt,
table12/COMPARE.out, ../compare12.py, ../qhs_variants_12.py, table12/PAIRS_base.out, ../pair_check.py, r7_20261105/B123_NOTE.md
(repairs 7-11 and the pass-11 records, each with the text it replaced), r7_20261105/ppc_ifetch_probe.py.{p11rec,rec11,rec12}.diff,
rec12_proof.out, LATE_REPLICATIONS_20261105.md, p11_20261105/codex_codex_qhs_p11.txt, det_20261104/window_sweep.out and
slack_sweep.out, adj_20261104/ (the design rulings); and the kit's STAGED_DIFFS_qhs.md, PROBE_IDENTITY_qhs.md, TREES_qhs.txt,
DRYRUN_qhs.out under C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/wqhs/landing/.

---

### A. the probe as it will ship (regress/ppc_ifetch_probe.py, the staged copy: the working copy with its docstring's `THE FIX (#NNN).` set to #581 and `PAIRS_OK=8/8` written `PAIRS_OK 8 of 8` -- section U reads every N/M in a gated probe's docstring as a score claim against the 249-row pin; landing_20261105/PROBE_IDENTITY_qhs.md proves the syntax tree minus the docstring, every string kept, equal to table 12's frozen instrument)

```
#!/usr/bin/env python3
"""qhslowifetch -- DETECTOR (built on its rung-3 witness) for the PowerPC slow-path instruction fetch in X(to_be_translated).

DEFECT (filed 2026-10-02).  src/cpus/cpu_ppc_instr.c, X(to_be_translated): when the instruction word is not in a host
page, the translator reads it with cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION); if that read FAILED it printed
"PPC to_be_translated(): read failed: TODO" and called exit(1) -- the emulator process ended.

THE FIX (#581).  The read-failure arm has four exits and a fallback: (a) read-ahead returns untouched; (b) a fetch whose
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
report, SRR0 and MSR unchanged, no checkstop or UNIMPLEMENTED text, and LR holding the stored value.  `T blr o1` and `T blr o2`
(repair 9; codex pass 8, B1) are `T blr` with r3 = 0x02040005 and 0x02040006, pinning the same eight channels.  They exist because
every read-ahead session enters the failure block TWICE -- the read-ahead failure, then the real fetch -- so a change the block
makes on pc's low bits and makes again on the second entry (a toggle) cancels before the final state is read; only a ONE-ENTRY
failure sees it.  With them the one-entry failures covered every low-bit pattern -- 00 by `T cont`, `T step`, `T me` and `again`
(each enters the block once at 0x02040000: the failing first fetch is not read-ahead and the -T halt is terminal), 11 by `T blr`,
01 and 10 by these two -- but with ME clear at 01, 10 and 11.  Before them an MSR[ME] toggle on low bits 01 or 10, and an SRR0
toggle on 01, passed all 137 rows (r7_20261105/B123_NOTE.md, repair 9).  `T blr m1`, `T blr m2` and `T blr m3` (repair 10; codex
pass 9, B1) are `T blr` with msr = 0x1000 and r3 = 0x02040005 / 0x02040006 / 0x02040007, pinning the same eight channels: a toggle
gated on BOTH pc's low bits and MSR[ME] runs on both visits of its cell's two-entry session and cancels, and no unaligned one-entry
failure was ME-set, so an SRR0 toggle gated on ME and pc != addr passed all 153 rows (r7_20261105/B123_NOTE.md, repair 10).  THE
GRID IS NOW HELD WHOLE: every (low bits, ME) cell has a two-entry and a one-entry failure session -- 00 clear `T ra` / `T cont`, `T
step`, `again`; 00 set `T ra me` / `T me`; 01 clear `T ra odd` / `T blr o1`; 01 set `T ra o1m` / `T blr m1`; 10 clear `T ra o2` /
`T blr o2`; 10 set `T ra o2m` / `T blr m2`; 11 clear `T ra o3` / `T blr`; 11 set `T ra o3m` / `T blr m3` -- and every one of them
pins MSR and SRR0, the state the block writes.  This text then said "so a toggle under any condition both visits share shows on the
one-entry session of its cell"; that was FALSE as a universal claim: those pairs matched low bits and ME but not the FULL pc, which
the block reads, and an SRR0 toggle gated on `(pc & ~0xb) != addr` cancelled on every read-ahead session (0xfec00008..b masks to
0xfec00000) and never fired on the one-entry sessions (0x02040000..7 masks to addr), passing all 177 rows (codex pass 10, B1 and
R1; MEASURED, r7_20261105/B123_NOTE.md, repair 11).  THE PAIRING INVARIANT (repair 11) replaces it.  Each read-ahead cell has a
one-entry PARTNER at the SAME full pc and MSR -- `T ra` / `T rp`, `T ra me` / `T rp me`, `T ra odd` / `T rp odd`, `T ra o1m` / `T
rp o1m`, `T ra o2` / `T rp o2`, `T ra o2m` / `T rp o2m`, `T ra o3` / `T rp o3`, `T ra o3m` / `T rp o3m` -- with pc set to
0xfec00008 | low bits directly, so its first fetch fails once (a failed fetch is never translated, so no read-ahead follows) and
arm (c) parks it; each partner pins its pair's nine channels.  A pair presents the failure block with the same pc, addr, MSR,
running (0) and instruction slot, and differs only in translation_readahead, nonzero on the two-entry session's first visit.  So a
toggle inserted before arm (a) whose condition reads only that shared state executes on the partner's one visit exactly when it
executes on the two-entry session's first visit, and so a toggle that executes on both visits and cancels there executes once on
the partner (DERIVED, not measured).  This says nothing about the second visit, which a toggle can remove or whose condition it can
change (codex rec11, rec12).  A condition on translation_readahead fires on one visit of the two-entry session and shows there.
THE SCOPE: the pairing guarantees equal INPUTS at entry; it says nothing about state the toggle writes on the first visit and tests
on the second.  A
SELF-REFERENTIAL toggle, `if (translation_readahead || (msr & BIT)) msr ^= BIT`, sets its marker on the read-ahead visit and clears
it on the real fetch, cancels on the two-entry side and never fires on the partner, which enters with the marker clear.  When the
marker is MSR[ME] or one of pc's low two bits, the generating-set rows catch it: the ME-set cells' msr rows and the pc rows of the
unaligned cells carrying it red because those bits are held both ways (DERIVED, not measured).  When the marker is MSR[RI] (codex
pass 11, B1; cpu_ppc.h:175; DERIVED, not measured), MSR[PMM], MSR[LE], or an SRR0 bit clear in the sentinel, no row distinguishes
it: this is a joint of translation_readahead x an untested bit x visit order, clause (e), NOT CLAIMED, and no row is owed for it
(tools/CLAUDE.md, the generating-set and 'tests means masks or compares' clauses).  An entry with that bit set would see any one
member and the next member moves the bit.  This text said "a toggle of pinned state under a condition on anything else the block
reads fires on both of the two-entry session's visits exactly when it fires on the partner's one"; that was FALSE for conditions on
state the toggle itself writes (codex pass 11, R1): the block reads MSR, B1's condition reads MSR, and the second visit's MSR is
not the entry MSR.  SHOWN TO SHARE, and how: pc and addr by the halt report memory_rw prints at each failing fetch
(`paddr=0xfec00008 len=4 pc=0xfec0000X`), textually identical on the partner's one report and both of its pair's
(r7_20261105/pair_check.py over the base run's transcripts, base249/PAIRS.out, PAIRS_OK 8 of 8; a mismatched pair fails it); MSR by
the same msr command before `continue` (none: the reset 0) and the same final MSR; running by memory.c, which clears it before
every -T read failure returns; the slot by the prologue, which derives pc and addr from the same pc's page bits and slot index
(both by code reading).  The bound: a condition on state the block does not READ: the GPRs the subfic changes (neither read nor
written here) and next_ic (written by arm (b)'s refresh, arm (c)'s park and the checkstop fallback, never read) is outside it.
This sentence called next_ic state the block "neither reads nor writes": FALSE (codex pass 11, R2).  The 0x0204000x and `T blr`
one-entry sessions stay; they carry other rows.  `T ra odd` (repair 6) is `T ra` entered at the UNALIGNED pc 0xfec00005: the
read-ahead fetch reaches the failure block with pc != addr, arm (a) returns and the real fetch halts again; it pins exit 0, pc
0xfec00009, two reports and MSR 0 (`T ra odd msr`, repair 7), so arm (a)'s guard is seen with an unaligned pc
(p5_20261105/TRAODD_NOTE.md).  `T ra o1m`, `T ra o2`, `T ra o2m`, `T ra o3` and `T ra o3m` (repair 7, the CLASS CLOSURE: passes 5
and 6 both found unrowed arm (a) x alignment cells, r7_20261105/B123_NOTE.md) complete the grid of pc's low two bits {00, 01, 10,
11} x MSR[ME] {clear, set} on that route: each is `T ra` entered at 0xfec00004 | low bits (the digit; `m` = MSR[ME] set, written
msr=0x1000 before pc) and pins exit 0, pc 0xfec00008 | low bits, two reports and MSR as entered.  REPAIR 7B gave the six unaligned
sessions the four channels their aligned siblings pinned and they did not -- the halted address, the stop, the checkstop text and
SRR0 (`addr`, `stopped`, `chkstop`, `srr0`) -- and `T ra me` the first two, so all eight cells (with `T ra`, `T ra me` and `T ra
odd`) pin the same eight channels: session, pc, nonex, addr, stopped, msr, chkstop and srr0.  Before it an SRR0 write and a
checkstop print in arm (a), each gated on pc != addr, passed all 103 rows (r7_20261105/B123_NOTE.md, repair 7b).  Repair 8 added a
ninth channel to all eight read-ahead sessions: no UNIMPLEMENTED text (`unimpl`).  This text argued that none was needed: "the real
fetch of each reaches the block in a state the 0x02040000 sessions and `T blr` already pin -- not read-ahead, running 0, ME clear
or set, pc aligned or not -- so an edit gated on anything the block tests that prints `read failed: TODO`, `[ PPC Exception` or
UNIMPLEMENTED there prints it on one of those sessions too".  That was FALSE: those sessions hold ME and alignment one at a time
and never the unaligned ME-set joint state, and a `goto bad` gated on `(msr & ME) && pc != addr` in arm (c) printed UNIMPLEMENTED
on `T ra o1m`, `T ra o2m` and `T ra o3m` with all 129 rows green (codex pass 7, F1 and R1; MEASURED, r7_20261105/B123_NOTE.md,
repair 8).  No read-ahead session carries a `text`, `exc` or `prompt` row, and the reason is now given per channel, from the
block's own arms: `[ PPC Exception` is printed only by ppc_exception, which always moves pc to the vector and writes SRR0, both
rowed on every read-ahead session; `read failed: TODO` is the removed exit's text, which the composite SYMPTOM key scans every
session for and whose exit ends the session; the prompt is implied by the register rows, which read `none` without it.  Their wants
are derived from the code -- the read-ahead fetch reaches the failure block at pc 0xfec00008 | low bits, arm (a) returns, the
subfic runs, the real fetch halts again and arm (c) parks at that pc -- and the eight-cell table measured them before the rows
existed; a guard refusing a cell parks it at read-ahead time instead (one report).

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

CLAUSE (e) -- catches (test-variant table 12, artifacts/qhslowifetch/r7_20261105/table12/SCORES.txt, PRETABLE_12.out written before
it; 88 variants on this 249-row probe: 73 red, every one on this probe; 14 green, the predicted fourteen; V12 NOT PREDICTED): the
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
those of `T ra odd`, `T ra o2` and `T ra o3`, and `T blr unimpl`, which alone caught it before); and a toggle at the top of the
failed-read block conditioned on pc's low bits -- MSR[ME] at 01, 10, 00 or 11 (R9_tog_me1, codex pass 8's B1, and R9_tog_me2: `T
blr o1 msr`, `T blr o2 msr`; R9_tog_me0: the msr rows of `T cont`, `T step`, `T me` and `again`; R9_tog_me3: `T blr msr`), or SRR0
at 01 (R9_tog_srr0_1: `T blr o1 srr0`) -- which the two-entry read-ahead sessions undo and the one-entry sessions see (R9_tog_me1,
R9_tog_me2 and R9_tog_srr0_1 passed all 137 rows before repair 9); and an SRR0 toggle there gated on MSR[ME] and pc != addr
(R10_tog_srr0_meun, codex pass 9's B1: the srr0 rows of `T blr m1`, `T blr m2` and `T blr m3`; its isolated members
R10_tog_srr0_me1, _me2 and _me3: one each -- all four passed all 153 rows before repair 10) or on low bits 10 alone
(R10_tog_srr0_2: `T blr o2 srr0` and `T blr m2 srr0`); and an SRR0 toggle there gated on the full pc against addr (R11_tog_full,
codex pass 10's B1: the srr0 rows of all eight partners `T rp` .. `T rp o3m`; its members R11_tog_full_<k><c|m>, gated also on low
bits k and ME: each its own cell's partner -- all nine passed all 177 rows before repair 11).  W5, D7, V7 and D12 ride on the
uninitialised or stale instruction word: which rows red is BUILD-DEPENDENT -- D12 reddened a different set in each of tables 2, 3
and 4, with `T ra nonex` in all three (table4/VERDICT.md), table 5 reddened table 4's set plus `T ra srr0`, table 6 moved D12's,
W5's and D7's sets again within the read-ahead rows (r6_20261105/table6/VERDICT.md), table 7 moved them once more -- W5 lost `T ra
me srr0`, D7 gained it, D12 traded `T ra odd pc` for `T ra me pc` and `T ra srr0` (r7_20261105/table7/VERDICT.md) -- and table 8
again on the same 103 rows: W5 regained `T ra me srr0`, and D12 dropped `T ra pc`, `T ra addr`, `T ra srr0`, `T ra o1m pc` and `T
ra o3 pc` and gained `T ra o2m pc` (r7_20261105/table8/VERDICT.md) -- and tables 9 to 12 again (r7_20261105/table9/VERDICT.md ..
table12/VERDICT.md) -- and the claim is that some row reds.  V12 IS NOT PREDICTED: its outcome depends on the uninitialised fetch
buffer ib -- the stale stack word is decoded on the variant's path, and whether a row reds depends on whether that word decodes as
an implemented instruction.  In table 3 it did on the `T ra` leg and a row reddened, while on the `T ra me` leg every row stayed
green -- read as the word decoding to bad:, which returns quietly during read-ahead, an INFERENCE from the all-green leg and not a
measurement (this sentence stated the decode as fact: LATE_REPLICATIONS_20261105.md row 34); table 4, on the same fix, reddened `T
ra me` and left `T ra` green; table 5 reddened both legs; table 6 the `T ra` and `T ra odd` legs; table 7 every read-ahead leg
except `T ra me` and `T ra o3m`; table 8 every one except `T ra` and `T ra o2`; table 9 every one; table 10 every one except `T
ra`, `T ra me` and `T ra o1m`; table 11 every one except `T ra o2`; table 12 every one except `T ra`.  A red that the stack's
contents decide is counted in neither tally.  Zero-initialising ib (filed) would make the variant deterministically green.  Green,
fourteen: arm (d) or the checkstop fallback edited (D6, D9, D10, V4, V5, V6, and R7_G2_d_msr -- the Gemini seat's pass-6 G2, arm
(d)'s test made `if (cpu->cd.ppc.msr)`) -- MEASURED unreached on pmppc (the window sweep below); arm (b) edited (D11, V2, and
R7_G1_b_lt -- the Gemini seat's G1, the aligned compare made `cpu->pc < addr`) -- with the aligned compare arm (b) is taken only
when the translation moved pc to an exception vector, which no measured session produces; arm (c)'s guard forced true (V3), and the
park tested before arm (b) as well (R5_cb) -- equivalent on every reachable entry, since running is 0 at each; arm (a) restoring
running before its return (R5_arun, and R7b_a_runun, the same write gated on pc != addr) -- disclosed below.  The shape-grid check
before table 3 (r3_20261105/GRID_*.md) and the repair-pass-3 findings, each measured before its adjudication (p3_20261105/table_p3,
DHALT_NOTE.md; the ruling p3_20261105/ADJ_MYTHOS.md), placed the msr rows and `T ra chkstop`; the eight-cell table before repair 7
(r7_20261105/B123_NOTE.md) placed `T ra odd msr` and the five sessions `T ra o1m` .. `T ra o3m`; repair 7b's measurement (the same
note) placed their addr, stopped, chkstop and srr0 rows and `T ra me`'s addr and stopped, repair 8's (the same note) the eight
unimpl rows, repair 9's `T blr o1` and `T blr o2`, repair 10's `T blr m1`, `T blr m2` and `T blr m3`, and repair 11's partners `T
rp` .. `T rp o3m`; the other shapes are disclosed below.
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
and W9 (a wrong machine check) have no row on pmppc: they need its ROW 5 (FILED pending X11).  On this 249-row probe the pre-fix
build scores 108/249 (141 rows red) with PPC_IFETCH_SYMPTOM=PRESENT, and the three null media -- /bin/true 94/249, an absent binary
64/249, /bin/false 65/249 -- each CONTROL=FAIL (r7_20261105/table12/SCORES.txt).

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
# THE ONE-ENTRY PARTNERS (repair 11; codex pass 10, B1; r7_20261105/B123_NOTE.md).  Each read-ahead session enters the failure block
# TWICE at one full pc -- the read-ahead visit, then the real fetch; its partner enters it ONCE at the SAME full pc and MSR: pc set to
# 0xfec00008 | low bits directly and continued under -T, so the first fetch fails (a failed fetch is never translated, so no
# read-ahead follows) and arm (c) parks it.  The pair then presents the block with the same pc, addr, MSR, running (0) and slot; only
# translation_readahead differs, nonzero on the two-entry session's first visit.  So a toggle inserted before arm (a) whose condition
# reads only those executes on the partner's one visit exactly when it executes on the two-entry session's first visit -- one that
# executes on both visits and cancels there executes once on the partner -- whatever the second visit does (the docstring; codex
# rec11, rec12); and a condition on translation_readahead fires on one visit only and shows on the two-entry side.
# A self-referential toggle is outside this: the docstring's SCOPE (codex pass 11, R1).
for tag, low, msr in (("", 0, 0), ("me", 0, MSR_ME), ("odd", 1, 0), ("o1m", 1, MSR_ME), ("o2", 2, 0), ("o2m", 2, MSR_ME),
                      ("o3", 3, 0), ("o3m", 3, MSR_ME)):
    nm, pair = ("T rp " + tag).rstrip(), ("T ra " + tag).rstrip()
    regs, T, how = session(nm, ["srr0=0x%x" % SENT] + (["msr=0x%x" % msr] if msr else []) + ["pc=0x%x" % (RA_NEXT | low), "continue"],
                           flags=["-T"])
    row(nm + " session", how, "exit0", "-T fetch at %s's full pc, one entry: survives" % pair)
    row(nm + " pc", hexr(regs, "pc"), hex(RA_NEXT | low), "parked at the same full pc as %s's real fetch" % pair)
    row(nm + " nonex", nonex(T), "1", "ONE halt report: one entry, where %s has two (R6_mask15)" % pair)
    row(nm + " addr", halts(T), hex(RA_NEXT), "the halt names the same word as %s's (W2, D3)" % pair)
    row(nm + " stopped", stopped(T), "yes", "the -T halt stopped the machine (B1)")
    row(nm + " msr", hexr(regs, "msr"), hex(msr), "MSR as entered: one entry, no toggle cancels (R9_tog_me%d)" % low)
    row(nm + " chkstop", chk(T), "absent", "arm (c) parked it; no checkstop (%s)" % ("V11" if msr else "D1, D2"))
    row(nm + " srr0", hexr(regs, "srr0"), hex(SENT),
        "SRR0 as entered: one entry, no toggle cancels (R11_tog_full, R11_tog_full_%d%s)" % (low, "m" if msr else "c"))
    row(nm + " unimpl", unimpl(T), "absent", "the halt is not sent to bad: (W3%s)" % (", V10" if msr else ""))
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
# ONE-ENTRY FAILURES (repairs 9 and 10; codex passes 8 and 9; r7_20261105/B123_NOTE.md).  Every read-ahead session enters the
# failure block TWICE -- the read-ahead failure, then the real fetch -- so a toggle the block makes under a condition both visits share
# (pc's low bits, MSR[ME]) cancels before the final state is read; only a ONE-ENTRY failure in the same (low bits, ME) cell sees it.
# The grid {00, 01, 10, 11} x {ME clear, set} x {two-entry, one-entry} is held whole: two-entry by the eight read-ahead sessions,
# one-entry by `T cont` / `T step` / `again` (00, clear), `T me` (00, set), `T blr` (11, clear) and these five -- `T blr` with r3 =
# 0x02040005 / 0x02040006 (o1, o2: ME clear; repair 9) and 0x02040005 / 0x02040006 / 0x02040007 with msr = 0x1000 (m1, m2, m3; repair
# 10).  The breakpoint keeps read-ahead off, so each failing fetch enters the block once and arm (c) parks it.  (Codex pass 9, R2: the
# srr0 note read "(R9_tog_srr0_1)" for o1 and o2 alike; o2 cannot see that toggle, so its note now names R10_tog_srr0_2.)
BLR_PUTS = cmds[2:]
for tag, target, msr, bits, togme, togsrr0, floods in (
        ("o1", 0x02040005, 0, "01", "R9_tog_me1", "R9_tog_srr0_1", "R5_mask2"),
        ("o2", 0x02040006, 0, "10", "R9_tog_me2", "R10_tog_srr0_2", "R5_mask1"),
        ("m1", 0x02040005, MSR_ME, "01", "R9_tog_me1", "R10_tog_srr0_me1", "R5_mask2"),
        ("m2", 0x02040006, MSR_ME, "10", "R9_tog_me2", "R10_tog_srr0_me2", "R5_mask1"),
        ("m3", 0x02040007, MSR_ME, "11", "R9_tog_me3", "R10_tog_srr0_me3", "R5_mask1, R5_mask2")):
    nm = "T blr " + tag
    regs, T, how = session(nm, ["srr0=0x%x" % SENT] + (["msr=0x%x" % msr] if msr else []) + ["r3=0x%x" % target] + BLR_PUTS +
                           ["breakpoint add 0x3000", "continue"], flags=["-T"])
    row(nm + " session", how, "exit0", "-T fetch at a guest-made pc, low bits %s, ME %s: survives" % (bits, "set" if msr else "clear"))
    row(nm + " pc", hexr(regs, "pc"), hex(target), "parked at the unaligned pc (arm (c))")
    row(nm + " nonex", nonex(T), "1", "one halt report: one entry, the slot not re-run (%s)" % floods)
    row(nm + " srr0", hexr(regs, "srr0"), hex(SENT), "SRR0 as entered: one entry, no toggle cancels (%s)" % togsrr0)
    row(nm + " msr", hexr(regs, "msr"), hex(msr), "MSR as entered: one entry, no toggle cancels (%s)" % togme)
    row(nm + " chkstop", chk(T), "absent", "arm (c) parked it; no checkstop")
    row(nm + " unimpl", unimpl(T), "absent", "the halt is not sent to bad: (%s)" % ("V10, R8_c_meun_bad" if msr else "R8_c_clun_bad"))
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
```

### B. gate 13's qhs block (the staged regress/gate_ppc.sh: HEAD's file plus exactly this block, directly below the #579 block, its header's #NNN set to #581; the gate_begin title gains ` + #581 ifetch`: `gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl + #571 DS-form + #579 llsc + #581 ifetch"`)

```
# ---- qhslowifetch (#581): a failed slow-path instruction fetch no longer ends the emulator process -- its 249-row detector ------
# X(to_be_translated) read the word with memory_rw and, on failure, printed `read failed: TODO' and called exit(1).  The arm now
# returns on read-ahead, refreshes next_ic when the translation already delivered an exception, PARKS the CPU on a -T halt, and
# delivers a machine check (MSR[ME] set) or a checkstop (clear) when a device declines the fetch while running.  `-E pmppc' with a
# raw four-byte word needs no image, so this block runs BEFORE the NetBSD prerequisite, like the #579 block above.  Thirty-one cold
# sessions: controls (a live word, a bogus machine, the ISI route by continue and by step, the no -T route), four -T sessions at
# 0x02040000 -- step, continue, step-step-continue-continue, and a step with MSR[ME] set -- each pinning the park (pc, SRR0), the
# exact halt-report count, the final MSR and the absence of the fatal, UNIMPLEMENTED, exception and checkstop text (the ME-set
# step pins the same), eight -T continues from cpc700_pci's last word whose read-ahead reaches arm (a) -- pc's low two bits {00,
# 01, 10, 11} x MSR[ME] {clear, set}, entered at 0xfec00004 | low bits, each pinning the same nine channels: survival, the park pc,
# the two halt reports, the halted address, the stop, the final MSR, no checkstop line, SRR0 untouched and no UNIMPLEMENTED text
# (repair 7 completed the grid, repairs 7b and 8 the channels; repair 6 added the first unaligned cell), eight one-entry PARTNERS
# at the same full pc and MSR as those eight (pc set to 0xfec00008 | low bits directly, so the first fetch fails once; repair 11):
# each pair presents the failure block with the same pc, addr, MSR, running and slot and differs only in translation_readahead, so a
# toggle that cancels over the two-entry session's two visits, under a condition on state the block reads that the toggle itself
# leaves unchanged, shows once on its partner (scope: the probe's docstring; codex pass 11, R1) -- and six -T continues
# into a guest-made unaligned pc (mtlr; blr), low bits 11, 01 and 10 with MSR[ME] clear and set, that arm (c) must park: one-entry
# failures, which see a change the block makes under pc's low bits and ME that the two-entry read-ahead sessions undo (repairs 5,
# 6, 9 and 10; with `T cont`, `T step`, `again` and `T me` they give every (low bits, ME) cell a one-entry session).
# The rung-3 witness is the 17-row probe frozen at regress/artifacts/qhslowifetch/witness_20261104/; the detector scores 108/249 (141
# rows red) on the pre-fix build and 249/249 on the fix (regress/artifacts/qhslowifetch/r7_20261105/table12/SCORES.txt).  Scored in the
# #579 shape: the completion sentinel once and last; each protocol key once in any form and once accepted; every row by name; the
# emitted, green and red row counts pinned to literals.  Names are at most 16 characters in an 18-wide column.  Test-variant tables:
# regress/artifacts/qhslowifetch/det_20261104/table1/ (the 50-row probe), table2/ (the 56-row probe), r3_20261105/table3/
# (the 62-row probe), r4_20261105/table4/ (the 69-row probe), r5_20261105/table5/ (the 79-row probe), r6_20261105/table6/ (the
# 82-row probe), r7_20261105/table7/ (the 103-row probe), r7_20261105/table8/ (the 129-row probe), r7_20261105/table9/ (the 137-row
# probe), r7_20261105/table10/ (the 153-row probe), r7_20261105/table11/ (the 177-row probe) and r7_20261105/table12/ (this probe,
# the record; its pairing check, table12/PAIRS_base.out).
IFLOG=$LOGDIR/ppc_ifetch.log
python3 -u ppc_ifetch_probe.py "$PMAX" gate "$LOGDIR/ppc_ifetch" > "$IFLOG" 2>&1 || true
if [ "$(grep -cx 'PPC_IFETCH_PROBE_DONE' "$IFLOG")" != 1 ]; then
    note "ppc_ifetch: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$IFLOG" | sed 's/^/       /'
    check "ppc_ifetch probe completed" "no" "yes"
else
    check "ppc_ifetch probe completed" "yes" "yes"
    check "ppc_ifetch sentinel is the last line" "$(tail -n 1 "$IFLOG")" "PPC_IFETCH_PROBE_DONE"
    for k in RESULT CONTROL SYMPTOM RED; do
        check "ppc_ifetch $k= lines" "$(grep -c "^PPC_IFETCH_$k=" "$IFLOG")" "1"
    done
    check "ppc_ifetch RESULT=249/249"  "$(grep -cx 'PPC_IFETCH_RESULT=249/249' "$IFLOG")" "1"
    check "ppc_ifetch CONTROL=OK"      "$(grep -cx 'PPC_IFETCH_CONTROL=OK' "$IFLOG")" "1"
    check "ppc_ifetch SYMPTOM=ABSENT"  "$(grep -cx 'PPC_IFETCH_SYMPTOM=ABSENT' "$IFLOG")" "1"
    check "ppc_ifetch RED=none"        "$(grep -cx 'PPC_IFETCH_RED=none' "$IFLOG")" "1"
    for v in "ctl session" "ctl live" "ctl srr0 kept" "neg apparatus" "isi session" "isi srr0" "isi pc" "isi text" "isi nonex" "isi1 session" "isi1 srr0" "isi1 pc" "isi1 nonex" "noT session" "noT pc" "noT srr0 kept" "noT unimpl" "noT chkstop" "T cont session" "T cont text" "T cont prompt" "T cont pc" "T cont srr0" "T cont nonex" "T cont unimpl" "T cont exc" "T cont chkstop" "T cont msr" "T step session" "T step text" "T step prompt" "T step pc" "T step srr0" "T step nonex" "T step unimpl" "T step exc" "T step chkstop" "T step msr" "T me session" "T me pc" "T me srr0" "T me nonex" "T me text" "T me exc" "T me unimpl" "T me chkstop" "T me msr" "again session" "again pc" "again srr0" "again nonex" "again text" "again unimpl" "again exc" "again chkstop" "again prompt" "again msr" "T ra session" "T ra pc" "T ra nonex" "T ra addr" "T ra stopped" "T ra msr" "T ra chkstop" "T ra srr0" "T ra unimpl" "T ra me session" "T ra me pc" "T ra me nonex" "T ra me addr" "T ra me stopped" "T ra me chkstop" "T ra me msr" "T ra me srr0" "T ra me unimpl" "T ra odd session" "T ra odd pc" "T ra odd nonex" "T ra odd addr" "T ra odd stopped" "T ra odd msr" "T ra odd chkstop" "T ra odd srr0" "T ra odd unimpl" "T ra o1m session" "T ra o1m pc" "T ra o1m nonex" "T ra o1m addr" "T ra o1m stopped" "T ra o1m msr" "T ra o1m chkstop" "T ra o1m srr0" "T ra o1m unimpl" "T ra o2 session" "T ra o2 pc" "T ra o2 nonex" "T ra o2 addr" "T ra o2 stopped" "T ra o2 msr" "T ra o2 chkstop" "T ra o2 srr0" "T ra o2 unimpl" "T ra o2m session" "T ra o2m pc" "T ra o2m nonex" "T ra o2m addr" "T ra o2m stopped" "T ra o2m msr" "T ra o2m chkstop" "T ra o2m srr0" "T ra o2m unimpl" "T ra o3 session" "T ra o3 pc" "T ra o3 nonex" "T ra o3 addr" "T ra o3 stopped" "T ra o3 msr" "T ra o3 chkstop" "T ra o3 srr0" "T ra o3 unimpl" "T ra o3m session" "T ra o3m pc" "T ra o3m nonex" "T ra o3m addr" "T ra o3m stopped" "T ra o3m msr" "T ra o3m chkstop" "T ra o3m srr0" "T ra o3m unimpl" "T rp session" "T rp pc" "T rp nonex" "T rp addr" "T rp stopped" "T rp msr" "T rp chkstop" "T rp srr0" "T rp unimpl" "T rp me session" "T rp me pc" "T rp me nonex" "T rp me addr" "T rp me stopped" "T rp me msr" "T rp me chkstop" "T rp me srr0" "T rp me unimpl" "T rp odd session" "T rp odd pc" "T rp odd nonex" "T rp odd addr" "T rp odd stopped" "T rp odd msr" "T rp odd chkstop" "T rp odd srr0" "T rp odd unimpl" "T rp o1m session" "T rp o1m pc" "T rp o1m nonex" "T rp o1m addr" "T rp o1m stopped" "T rp o1m msr" "T rp o1m chkstop" "T rp o1m srr0" "T rp o1m unimpl" "T rp o2 session" "T rp o2 pc" "T rp o2 nonex" "T rp o2 addr" "T rp o2 stopped" "T rp o2 msr" "T rp o2 chkstop" "T rp o2 srr0" "T rp o2 unimpl" "T rp o2m session" "T rp o2m pc" "T rp o2m nonex" "T rp o2m addr" "T rp o2m stopped" "T rp o2m msr" "T rp o2m chkstop" "T rp o2m srr0" "T rp o2m unimpl" "T rp o3 session" "T rp o3 pc" "T rp o3 nonex" "T rp o3 addr" "T rp o3 stopped" "T rp o3 msr" "T rp o3 chkstop" "T rp o3 srr0" "T rp o3 unimpl" "T rp o3m session" "T rp o3m pc" "T rp o3m nonex" "T rp o3m addr" "T rp o3m stopped" "T rp o3m msr" "T rp o3m chkstop" "T rp o3m srr0" "T rp o3m unimpl" "T blr session" "T blr pc" "T blr nonex" "T blr srr0" "T blr msr" "T blr chkstop" "T blr unimpl" "T blr lr" "T blr o1 session" "T blr o1 pc" "T blr o1 nonex" "T blr o1 srr0" "T blr o1 msr" "T blr o1 chkstop" "T blr o1 unimpl" "T blr o1 lr" "T blr o2 session" "T blr o2 pc" "T blr o2 nonex" "T blr o2 srr0" "T blr o2 msr" "T blr o2 chkstop" "T blr o2 unimpl" "T blr o2 lr" "T blr m1 session" "T blr m1 pc" "T blr m1 nonex" "T blr m1 srr0" "T blr m1 msr" "T blr m1 chkstop" "T blr m1 unimpl" "T blr m1 lr" "T blr m2 session" "T blr m2 pc" "T blr m2 nonex" "T blr m2 srr0" "T blr m2 msr" "T blr m2 chkstop" "T blr m2 unimpl" "T blr m2 lr" "T blr m3 session" "T blr m3 pc" "T blr m3 nonex" "T blr m3 srr0" "T blr m3 msr" "T blr m3 chkstop" "T blr m3 unimpl" "T blr m3 lr"; do
        check "ppc_ifetch row: $v" "$(count "$IFLOG" "^$v  .*ok$")" "1"
    done
    ifok=$(count "$IFLOG" " ok$"); ifbad=$(count "$IFLOG" " FAIL$"); ifrun=$((ifok + ifbad))
    check "ppc_ifetch rows run"   "$ifrun" 249
    check "ppc_ifetch rows green" "$ifok" 249
    check "ppc_ifetch rows red"   "$ifbad" 0
fi
```

### C1. table 12's legs (base, HEAD, the three null media, the verbatim reinstatement B1), the fourteen green variants, the tallies, and table 11's legs

```
(table 12, r7_20261105/table12/SCORES.txt, the record; RED lists replaced by their counts)
base [249 rows] 249/249 CONTROL=OK SYMPTOM=ABSENT PPC_IFETCH_PROBE_DONE RED=none
HEAD [249 rows] 108/249 CONTROL=OK SYMPTOM=PRESENT PPC_IFETCH_PROBE_DONE RED=<141 rows>
null_true [249 rows] 94/249 CONTROL=FAIL SYMPTOM=ABSENT PPC_IFETCH_PROBE_DONE RED=<155 rows>
null_absent [249 rows] 64/249 CONTROL=FAIL SYMPTOM=ABSENT PPC_IFETCH_PROBE_DONE RED=<185 rows>
null_false [249 rows] 65/249 CONTROL=FAIL SYMPTOM=ABSENT PPC_IFETCH_PROBE_DONE RED=<184 rows>
B1_exit_head [249 rows] 108/249 CONTROL=OK SYMPTOM=PRESENT PPC_IFETCH_PROBE_DONE RED=<141 rows>

the 14 variants scored 249/249 (green) are the TALLY's fourteen below

(table12/COMPARE.out, compare12.py against PRETABLE_12.out -- it counts V12_fail_ra among the red, where VERDICT.md counts it in neither tally)
TALLY: 88 variants; red 74, green 14 (D6_d_inv,D9_mc_vec,D10_chk_run,D11_b_noref,V2_b_del,V3_c_true,V4_d_false,V5_d_true,V6_chk_nopark,R5_cb,R5_arun,R7_G1_b_lt,R7_G2_d_msr,R7b_a_runun)
TALLY: exact 9/9, at-least held 56, predicted-green held 14, build-dependent red 4/4, red-within held 4/4, not predicted 1
COMPARE12_MISSES=0
COMPARE12_DONE

(tables 1-11: det_20261104/table1/, table2/, r3_20261105/table3/, r4_20261105/table4/, r5_20261105/table5/, r6_20261105/table6/, r7_20261105/table7/ .. table11/ -- tables 2-11 each with a VERDICT.md, table 1 with its SCORES.txt only; the gate comment lists them)
```

### C2. table 12's verdict (r7_20261105/table12/VERDICT.md, the verdict of record, unedited)

# qhslowifetch -- test-variant TABLE 12 (repair 11: 249 rows; no product change since repair 5), 2026-11-05 ~11:16-11:31Z

Driver `../table12_qhs.run.sh` (frozen copy of `../table12_qhs.sh`), in THREE phases (88 variants on a 31-session probe): phase a
(`../table12_run_a.log`) cloned build/ to /tmp/gxqhs18 under a clone-local .MUTANT sentinel, checked the clone's sources against the
baseline, ran the legs and variants 1-30 and put the baseline source back with the sentinel KEPT; phases b and c (`../table12_run_b.log`,
`../table12_run_c.log`) each refused unless the sentinel and the baseline source were still there, ran variants 31-60 and 61-88, and c
restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and only then cleared the sentinel.  Every build `fresh`.  Instrument
`probe249_frozen.py` == `../base249/probe249_run.py` (cmp-checked by the driver; 249/249 on build/ after both clearance checks,
`../CLEARANCE.txt`'s repair-11 section).  Baseline `../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_12.out` was written before
anything here.  Table 11 stays the record of the 177-row probe.  Scores: `SCORES.txt`; the mechanical comparison: `COMPARE.out`
(`../compare12.py`), **COMPARE12_MISSES=0**.

* **Legs, all exact.**  base 249/249, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 108/249 (141 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 11's + each partner's session, pc, stopped, msr and srr0 rows).  Null media: /bin/true 94/249, an
  absent binary 64/249, /bin/false 65/249 -- each the predicted score, CONTROL=FAIL on all three.
* **THE PAIRING INVARIANT, checked on this table's own base leg:** `../pair_check.py sessions_base` -> `PAIRS_base.out`, PAIRS_OK=8/8
  (as on build/, `../base249/PAIRS.out`): every partner prints ONE halt report, textually identical to each of its two-entry pair's
  two, with the same msr command and the same final pc, MSR and SRR0.
* **Repair 11's nine, predicted EXACTLY, every one matching:** R11_tog_full (pass 10's B1, an SRR0 toggle gated on `(pc & ~0xb) !=
  addr`) 241/249 -- the srr0 rows of all eight partners; R11_tog_full_<k><c|m> 248/249 each -- its own cell's partner only.  All nine
  were 177/177 on the 177-row probe (`../B123_NOTE.md`, repair 11): they cancel on the two-entry sessions and never fire on the
  0x0204000x one-entry sessions; a partner at the same full pc sees each once.
* **Table 11's 79.**  The 56 predicted AT LEAST their table-11 sets all held, and no deterministic variant's red set on the 177 old
  rows changed; the fourteen predicted GREEN stayed green; the four BUILD-DEPENDENT variants are red; the four failure-test
  narrowings stayed inside their sessions, now widened by the partners whose fetch each refuses (each also reddened partner rows:
  R7b_f_me the ME-clear partners, R7b_f_meclr the ME-set ones, R7b_f_ra all eight, R7b_f_unal the aligned two); V12_fail_ra, NOT
  PREDICTED, reddened 29 rows, every read-ahead leg except `T ra` and no partner row (its stale-buffer decode happens on the
  read-ahead visit, which a partner does not have) -- counted in neither tally.
* **Tallies for the probe's clause (e):** 88 variants on the 249-row probe; 73 red, every one on this probe; 14 green, the
  predicted fourteen; V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_12 did not name in advance, and no prediction missed.

### D. the measurement that made the partners (r7_20261105/B123_NOTE.md, its repair-11 section)

## Repair 11 (2026-11-05, ~11:1xZ) -- codex GPT-6 Astra's pass-10 B1 and R1 (p10_20261105/codex_codex_qhs_p10.txt, DISPOSITION.md)

**MEASURED first** -- `b11_table.run.sh` -> `b11_table/` (log `b11_table_run.log`): a fresh /tmp/gxqhs12, clone-local .MUTANT, both
sources cmp'd equal to GXEMUL-SEC and to fix7, the fix rebuilt fresh first, restored cmp-clean and rebuilt, sentinel cleared.
Variants: `b11_variant.py`, one conditional statement each at the top of the failed-read block.  Instrument: the 177-row probe.
R11_tog_full (B1: `if ((pc & ~(uint64_t)0xb) != addr) srr0 ^= 0x100;`) and its eight low-bit x ME members R11_tog_full_<k><c|m>
(the same, also gated on `(pc & 3) == k` and ME clear or set): **177/177 each -- all nine escape.**  The masked read-ahead pcs
0xfec00008..b all become 0xfec00000 != addr, so the toggle fires on both visits and cancels; the masked one-entry pcs 0x02040000..7
all equal addr, so it never fires there.  The repair-10 pairs matched low bits and ME and still differed in the FULL pc.

**THE STRUCTURAL FIX:** each read-ahead cell gets a ONE-ENTRY PARTNER at the SAME full pc and MSR -- pc set to 0xfec00008 | low bits
directly and continued under -T, so the first fetch fails; a failed fetch is never translated, so no read-ahead follows, and arm (c)
parks it.  PRE-CHECK on build/ (cell_witness.py, `b11_table/partners_precheck/`): at each of 0xfec00008..b with MSR 0 and 0x1000,
exit 0, park at that pc, ONE halt report reading `memory READ: from non-existant paddr=0xfec00008 len=4 pc=0xfec0000X` -- the line
its two-entry pair prints twice -- SRR0 and MSR as entered, no checkstop or UNIMPLEMENTED text.

Repair 11's rows: the eight one-entry partners `T rp` .. `T rp o3m` (9 rows each, the read-ahead cell's channels) -> 249 rows, 31
sessions; base 249/249 on build/ after both clearance checks (CLEARANCE.txt, repair-11 section).  THE PAIRING INVARIANT, checked by
`pair_check.py` on the base run (base249/PAIRS.out) and on table 12's base leg (table12/PAIRS_base.out): PAIRS_OK=8/8 both times --
each partner's one halt report textually equals each of its pair's two (same paddr 0xfec00008, same full pc), the same msr command
and the same final pc, MSR and SRR0; a mismatched pair (T ra odd vs T rp o2) gives two distinct lines, so the check can fail.  Table
12 (table12/VERDICT.md, PRETABLE_12.out first; COMPARE12_MISSES=0): R11_tog_full 241/249 (all eight partners' srr0 rows), each
member 248/249 (its own cell's partner).  R1 corrected in place, quoting it, in the probe's docstring.

### F1. the final ruling (adj_p11_20261105/ADJ_MYTHOS_local.md, whole)

MYTHOSADJP11QHS

VERDICT: B1 is clause-(e) DEBT, not floor; R1 and R2 are upheld as false records and are corrected in place; the pass is valid with its denominator and finds zero floor breaches surviving adjudication, so the round CLOSES after the records corrections. One part of the main loop's proposed disposition is wrong: the scope sentence it proposes for the pairing invariant. The invariant does not "cover" self-referential toggles on tested state, and the family is not split by "state the mutation creates" versus "state the block tests". It is split by whether the marker bit the mutation tests is a bit in the floor's generating set. The invariant must be scoped to conditions the toggle leaves unchanged, and the self-referential family must be disposed separately: caught by the generating-set rows when the marker is a tested bit, disclosed when it is not.

1. B1: DEBT. Derivation from the code and the rules.

What the block tests. The failed-read block (src/cpus/cpu_ppc_instr.c:4128-4209) tests exactly four things: translation_readahead at :4144, the aligned pc against addr at :4168, running at :4176, and MSR through `cpu->cd.ppc.msr & PPC_MSR_ME` at :4186. That is the only MSR test in the block. PPC_MSR_ME is bit 12 (src/include/cpu_ppc.h:166); PPC_MSR_RI is bit 1 (cpu_ppc.h:175). The block never masks or compares RI.

What the rules make of that. The floor is the cross-product of the guard's dominating predicates with the state lvalues the repair path reads, and "joint cells outside the floor are clause-(e) coverage debt" (tools/CLAUDE.md:1517-1522). The single-axis generating set is "every idata bit the guarded body TESTS ... written both clear and set", and "multi-axis idata joints stay clause-(e) debt" (CLAUDE.md:1531-1534). "TESTS" means masks or compares as a case, not depends-on, and "crossing a floor cell with a single bit of a compared value is the two-axis joint a probe's NOT CLAIMED (0) discloses" (CLAUDE.md:1541-1549). A derived input is graded by what the body tests on it, and "closable by a finite row set is NOT the discriminator" (CLAUDE.md:1614-1624).

Applying it. B1's condition is `translation_readahead || (msr & PPC_MSR_RI)` and its write is `msr ^= PPC_MSR_RI` (codex_codex_qhs_p11.txt:11-13). The member of this family that fires only on translation_readahead, `if (translation_readahead) msr ^= RI`, is caught: it leaves RI set at the end of every two-entry session and the eight `T ra* msr` rows red. B1's discriminator against that caught member is the `msr & RI` disjunct, which is a test of an untested bit of a field the block reads: exactly the `#549` latch x bit shape that CLAUDE.md:1547-1549 grades NOT CLAIMED. The round's own precedent agrees: G2, arm (d)'s test made `if (cpu->cd.ppc.msr)`, tests untested MSR bits and was graded disclosed, not rowed (P11_QHS_CODEX.md:596-602, 620-625).

The floor is doing its job, which is the decisive check. Put the same self-referential shape on a TESTED bit and the shipped detector catches it. `if (translation_readahead || (msr & ME)) msr ^= ME`: on `T ra me` the first visit clears ME, the second visit sees neither read-ahead nor ME and does nothing, arm (c) parks at :4176-4178 before arm (d), and the final MSR is 0 against the row's want of 0x1000, so `T ra me msr` reds; `T me msr` and `T rp me msr` red the same way. On `T ra` it cancels and on `T rp` it never fires, just like B1, but the ME-set cells exist because ME is a tested bit held both ways. Likewise a marker in pc's low bits (`if (translation_readahead || (pc & 1)) pc ^= 1`, the low bits surviving the prologue at :4102-4103) cancels on `T ra` but reds `T ra odd pc` and `T rp odd pc`. B1 escapes precisely and only because RI is outside the generating set. That is the definition of a joint cell outside the floor.

Codex's "in-bound" argument (codex_codex_qhs_p11.txt:33) conflates two bounds. "Fields the guarded body reads" bounds operand SWAPS; joint cells are admitted "only where the body's own tests distinguish them" (P11_QHS_CODEX.md:33-34). B1 is a joint of translation_readahead x RI x visit order that no test in the block distinguishes.

How a row could observe the intermediate state, and why none is owed. The shipped instrument reads only final state: halt lines, setup commands and final registers (P11_QHS_CODEX.md:797-800; codex line 56). The one way to see B1 with this machinery is a session entered with RI already set (msr=0x2): the partner then clears it once and its msr row reds, and the two-entry session clears it on the first visit and never re-sets it. That is a row on an untested bit, which "a filter ... may demand ... only for a floor cell" forbids (CLAUDE.md:1521-1522), and the next member moves the marker to PMM (0x4), LE (0x1), or an SRR0 bit clear in the sentinel (0x200 is clear in 0x11111111; 0x100 happens to be set, so that member is caught by luck). The family is open on every untested bit of every written field. Rowing it one bit at a time is the linear-in-cells convergence the stop rule names (CLAUDE.md:2701-2709). Do not row it. Disclose it.

2. The corrected pairing-invariant text (replacing the sentence at regress/ppc_ifetch_probe.py:73-77):

"A pair presents the failure block with the same pc, addr, MSR, running (0) and instruction slot, and differs only in translation_readahead, nonzero on the two-entry session's first visit. So a toggle of pinned state under a condition that the toggle itself leaves unchanged, on anything else the block reads, fires on both of the two-entry session's visits exactly when it fires on the partner's one; it cancels on one side and shows on the other. A condition on translation_readahead fires on one visit of the two-entry session and shows there. THE SCOPE: the pairing guarantees equal INPUTS at entry; it says nothing about state the toggle writes on the first visit and tests on the second. A SELF-REFERENTIAL toggle, `if (translation_readahead || (msr & BIT)) msr ^= BIT`, sets its marker on the read-ahead visit and clears it on the real fetch, cancels on the two-entry side and never fires on the partner, which enters with the marker clear. When the marker is a bit the block TESTS (MSR[ME], pc's low two bits) the generating-set rows catch it: the ME-set cells' msr rows and the unaligned cells' pc rows red because those bits are held both ways. When the marker is a bit the block does not test, MSR[RI] (codex pass 11, B1; cpu_ppc.h:175; DERIVED, not measured), MSR[PMM], MSR[LE], or an SRR0 bit clear in the sentinel, no row distinguishes it: this is a joint of translation_readahead x an untested bit x visit order, clause (e), NOT CLAIMED, and no row is owed for it (tools/CLAUDE.md, the generating-set and 'tests means masks or compares' clauses). An entry with that bit set would see any one member and the next member moves the bit."

3. Records.

R1: UPHELD. The sentence at ppc_ifetch_probe.py:74-77 is universal over "a condition on anything else the block reads" and is false for conditions on state the toggle itself writes (codex lines 54-56). The block reads MSR, B1's condition reads MSR, and the second visit's MSR is not the entry MSR. Corrected by the text in section 2, quoting the old sentence and marking it false, as the docstring did for its pass-10 predecessor (ppc_ifetch_probe.py:65-69). The main loop's proposed scope ("covers conditions on the state the block TESTS and the visit flag") is the part that is wrong: a self-referential toggle on tested state is also NOT covered by the invariant sentence, it is caught by other rows, and the contract must say which mechanism does the catching.

R2: UPHELD. ppc_ifetch_probe.py:82-83 says next_ic is state the block "neither reads nor writes". The block writes it at cpu_ppc_instr.c:4177 (arm (c)'s park) and :4207 (the checkstop fallback), and arm (b)'s refresh at :4169 writes it through the pc-to-pointers path (cpu_dyntrans.c:832). No line of :4128-4208 reads it. Correction: "a condition on state the block does not READ: the GPRs the subfic changes (neither read nor written here) and next_ic (written by arm (b)'s refresh, arm (c)'s park and the checkstop fallback, never read) is outside it, as the field-write disclosure says."

4. Closure. The floor question is asked of the shipped composite (CLAUDE.md:2686-2688) and this pass answers it with zero surviving breaches: B1 graded debt above. The pass is valid under CLAUDE.md:2670-2677: the diff was delivered in full (P11_QHS_CODEX.md section 2), the seat ledger names the misses (p11_20261105/DISPOSITION.md:3-5: Gemini down, glm and grok walled, one seat answered), and the zero carries its denominator (codex lines 42-44: 16 session-cells, nine channels each, the edit shapes swept including toggles whose condition inspects the toggled state). The records corrections are contract text, not floor-bound detector material: no row, no mutant, no score changes, so they owe no pass 12. The round closes after they land.

Disclosure for the lesson file, since this is the fourth consecutive pass on one family: passes 8, 9 and 10 found members whose discriminators were in the generating set (low bits, ME, full pc) and each was a true floor breach; pass 11 found the first member whose discriminator is outside it. The structural repair held the floor whole and the rules place the remainder, which is what closure looks like.

MYTHOSADJP11QHS: 0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS

### F2. the passes: every verdict line from pass 3 on, then pass 11's disposition whole (passes 6-10: p6_20261105/ .. p10_20261105/DISPOSITION.md; pass 10's B1 and the structural closure it ordered are block D)

```
(the verdict line of every pass and ruling from pass 3 on; passes 3-5 carry no DISPOSITION.md -- their dispositions are the rulings and notes in each directory)
p3 ruling    p3_20261105/ADJ_MYTHOS_r2.md             MYTHOSADJP3QHS: 7 RULINGS 6 ROWS OWED VERDICT:RECORDS-AND-ROWS
p4 ruling    p4_20261105/ADJ_MYTHOS_r2.md             MYTHOSADJP4QHS: 8 RULINGS 8 ROWS OWED VERDICT:REPAIR-5
p5 Mythos    p5_20261105/MYTHOS_r3.md                 MYTHOSP5QHS: 39 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
p6 codex     p6_20261105/DISPOSITION.md               CODEXP6QHS: 41 CELLS SWEPT 3 BREACHES 3 FALSE
RECORDS VERDICT:REPAIR
p7 codex     p7_20261105/DISPOSITION.md               CODEXP7QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS
VERDICT:REPAIR
p8 codex     p8_20261105/DISPOSITION.md               CODEXP8QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS
VERDICT:REPAIR
p9 codex     p9_20261105/DISPOSITION.md               CODEXP9QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR
p10 codex    p10_20261105/DISPOSITION.md              CODEXP10QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR
p11 codex    p11_20261105/DISPOSITION.md              CODEXP11QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR
p11 ruling   adj_p11_20261105/ADJ_MYTHOS_local.md     MYTHOSADJP11QHS: 0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS
rec11 codex  rec11_20261105/DISPOSITION.md            CODEXRECP11QHS: 6 ACCEPTED 2 TO FIX VERDICT:FIX
rec12 codex  rec12_20261105/DISPOSITION.md            CODEXREC12QHS: 0 ACCEPTED 2 TO FIX VERDICT:FIX
rec13 codex  rec13_20261105/DISPOSITION.md            CODEXREC13QHS: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT
```

# qhslowifetch PASS 11 -- disposition (main loop, 2026-11-05 ~13:1xZ)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p11.txt; `CODEXP11QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; source-derived).  Gemini 4 Argon: SEAT FAILURE -- the web route is down (control errors since ~11:07Z; bank_gweb.py
blocked the transport at 11:38Z).  glm-5.3 and grok-4.7: walled.

* B1: `if (translation_readahead || (msr & PPC_MSR_RI)) msr ^= PPC_MSR_RI;` -- the first visit sets RI, the second clears it, the
  partner does neither: a mutation that creates and consumes its own intermediate condition, which the pairing invariant's equal-
  baseline premise does not reach.  THE GRADING IS A RULE QUESTION: the block tests MSR only through `msr & ME`; MSR[RI] is a bit it
  never tests, and the condition reads the state the toggle writes.  PROPOSED (not ruled): clause-(e) DEBT, with the pairing invariant's
  scope stated honestly.  Sent to the ruler (local Mythos 5.1): prompt mythos_local/prompt_qhs_adj11.md -> ../adj_p11_20261105/.
* R1 (L4): the contract's universal pairing guarantee is false as stated.  R2 (L4): next_ic is WRITTEN by the block (:4177, :4207);
  the exclusion must say its value is not read.

## The ruling (2026-11-05 ~13:5xZ): ../adj_p11_20261105/ADJ_MYTHOS_local.md -- `0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`

The ruler (local Mythos 5.1) graded B1 clause-(e) DEBT.  Its discriminator against the caught read-ahead-only member is `msr & RI`, a
test of a bit the block never masks or compares (the `#549` latch x bit shape, NOT CLAIMED).  The same self-referential shape on a
TESTED bit (ME; pc's low bits) is caught by the generating-set rows; the ruler derived both from the code, not by measuring them.
It CORRECTED the main loop's proposal: the pairing invariant does not "cover" self-referential toggles on tested state.  Those are
caught by OTHER rows, and the contract must say which rows catch them; the family splits by whether the marker bit is in the
generating set.  R1 and R2 were upheld, with replacement text.  The records corrections are contract text, so no pass 12 is owed; a
second reading of the corrected text is still owed, because a correction is not safer than what it corrects.  Applied by the round's
implementer (Opus 5.5, resumed), who was told to verify each claim in the ruler's text before writing it.

### F3. the records chain after the ruling (rec11, rec12, rec13_20261105/DISPOSITION.md, whole)

# qhslowifetch -- second reading of the pass-11 records corrections (main loop, 2026-11-05 ~15:2xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_rec11.txt; `CODEXRECP11QHS: 6 ACCEPTED 2 TO FIX VERDICT:FIX`).
* ACCEPTED: R2, the gate comment, and ALL FOUR of the implementer's deviations from the ruler's wording.  On deviation 1 codex
  confirmed that the block does not test pc's low two bits (`(pc & ~3)` at :4168).  Low-bit self-referential toggles are caught by
  the marker-set cells and exact final-pc rows.  B1's DEBT grading stays consistent: the operational line is existing marker-set
  coverage, not which bits a block predicate tests.
* FIX: R1's sentence and the partner-loop comment still inferred two firings from an unchanged condition alone.  Codex's
  counterexample, derived from the source: `if (msr & ME) pc ^= 0xfec02000` keeps its condition but moves pc's page bits, so the next
  slot fetches RAM and the second failed visit never comes.  It is a records defect, not a detector escape.
Applied by the main loop as a PROVISO, with no new explanation: "provided both failed-fetch visits still happen and nothing between
them changes the toggled state", in the docstring (with codex's counterexample, marked DERIVED) and in the partner-loop comment
(r7_20261105/ppc_ifetch_probe.py.rec11.diff; copy .pre_rec11).  Text-only proof re-run: r7_20261105/rec11_proof.out, all six
EQUAL, negative control DIFFERENT, docstring max width 131.  A third reading, scoped to the proviso, is fired (rec12_20261105/).

# qhslowifetch -- third reading, the proviso (main loop, 2026-11-05 ~15:3xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_rec12.txt; `CODEXREC12QHS: 0 ACCEPTED 2 TO FIX VERDICT:FIX`).  The rec11
proviso still left a hole, and codex supplied a source-derived counterexample: `if (addr == 0xfec00008) pc ^= 0x1000`.  The second
visit happens and the toggled state is unchanged, but the prologue recomputes addr from the moved pc, so the condition is false the
second time; the toggle fires once and does not cancel.  It is a records defect, not a detector escape.

THE PATTERN IS memc's, and so is the remedy.  Two qualifications of one derived sentence, each defeated by a new counterexample:
the sentence made a claim about the SECOND visit, and every fix tried to bound what can happen there.  It is REPLACED by its
first-visit core, which says nothing about the second visit.  A toggle inserted before arm (a) whose condition reads only the
pair's shared entry state executes on the partner's one visit exactly when it executes on the two-entry session's first visit.
So one that executes on both visits and cancels there executes once on the partner (DERIVED).  "This says nothing about the
second visit, which a toggle can remove or whose condition it can change (codex rec11, rec12)."  The partner-loop comment is
changed the same way.  Diff: r7_20261105/ppc_ifetch_probe.py.rec12.diff (copy .pre_rec12).  Proof: r7_20261105/rec12_proof.out --
all six EQUAL, the negative control DIFFERENT, max width 131.  A fourth reading, scoped to the replacement, is fired
(rec13_20261105/).

# qhslowifetch -- fourth reading, the replaced sentence (main loop, 2026-11-05 ~15:5xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_rec13.txt; `CODEXREC13QHS: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT`).  The
first-visit replacement is TRUE at both sites: equal shared inputs at the compared first entries give the condition the same truth
value, and placement before arm (a) means both entries evaluate it.  The rec11 and rec12 counterexamples change only later execution.
The paragraph stays coherent with the translation_readahead sentence, THE SCOPE and the self-referential family.

THE PASS-11 RECORDS CHAIN CLOSES HERE, on a valid zero-finding reading with its denominator (the two sites, their context):
  rec11  6 accepted / 2 to fix  (R1 + the partner comment: two firings do not follow from an unchanged condition)
  rec12  0 / 2                  (the rec11 proviso defeated: addr recomputed from the moved pc)
  rec13  2 / 0                  (the sentence REPLACED by its first-visit core; no claim about the second visit)
The lesson matches memc's, reached independently on the same day.  A derived sentence that keeps failing a reading is cut down to
what it can prove, not qualified again; each qualification was a new claim about the part it could not prove.  qhs goes to landing
after #575.  Its REGRESS stage and landing kit are still owed.

### G. the fix: HEAD against the staged src/cpus/cpu_ppc_instr.c (this round's one hunk; the working copy also carries #575's two lines in X(crandc)/X(crorc), not carried -- STAGED_DIFFS_qhs.md), then src/include/cpu_ppc.h (staged = working copy).  The comments' #NNN, #MMM, #QQQ and #PPP are placeholders the landing fills

```
--- a/src/cpus/cpu_ppc_instr.c (HEAD cbd916d1)
+++ b/src/cpus/cpu_ppc_instr.c (staged, md5 ca49eca89e12)
@@ -4126,12 +4126,87 @@
     } else {
         /*  fatal("TRANSLATION MISS!\n");  */
         if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
             sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
-            fatal("PPC to_be_translated(): "
-                "read failed: TODO\n");
-            exit(1);
-            /*  goto bad;  */
+            /*  #NNN: the instruction fetch failed.  This
+                used to be fatal() + exit(1).  Four states
+                reach here; none may run this slot, and
+                the slot stays TO_BE_TRANSLATED, so a fetch
+                that later reaches it re-enters this arm.
+                (A -T halt is terminal whichever exit is
+                taken: memory.c cleared running, so the run
+                loop no longer enters this CPU and a further
+                step or continue runs nothing.  (c)'s park
+                only ends the current batch and keeps pc
+                here.)  */
+            /*  (a) Read-ahead: the guest has not reached
+                this address.  Touch nothing, as bad:
+                does.  */
+            if (cpu->translation_readahead)
+                return;
+            /*  (b) The translation in memory_rw raised an
+                ISI or 603 IMISS: ppc_exception() saved
+                SRR0/SRR1 and moved pc to the vector.
+                That route is reached on no measured
+                session (the dispatch pc lookup translates
+                this address first); kept so a delivered
+                exception is not doubled by (d).  Not
+                watertight: when the vector equals the
+                failing address, pc equals addr again, (b)
+                is skipped and (d) delivers a second
+                exception over SRR0/SRR1, or checkstops if
+                MSR[ME] is clear (#MMM; no producer on any
+                machine measured).  pc is compared ALIGNED:
+                the prologue aligns addr but not pc, and a
+                guest can make pc unaligned (mtlr and bclr
+                copy LR unmasked), so a bare pc != addr
+                took this arm for such a pc, re-ran the
+                slot and, under -T, printed thousands of
+                halt reports instead of parking in (c).
+                next_ic must follow pc; ppc_exception()
+                re-resolves it, and (d) relies on that.
+                The refresh here is redundant and harmless.  */
+            if ((cpu->pc & ~(uint64_t)3) != addr) {
+                quick_pc_to_pointers(cpu);
+                return;
+            }
+            /*  (c) -T: memory.c cleared running and printed
+                the non-existant line.  No PowerPC exception
+                is involved.  Park at this pc (set above) so
+                the debugger shows the failing fetch.  */
+            if (!cpu->running) {
+                cpu->cd.ppc.next_ic = &nothing_call;
+                return;
+            }
+            /*  (d) A device declined an instruction-width
+                read while running.  A fetch the bus
+                terminates with an error is a machine check
+                (vector 0x200) when MSR[ME] is set and a
+                checkstop when it is clear.  SRR1 status
+                bits are not modelled.  */
+            if (cpu->cd.ppc.msr & PPC_MSR_ME) {
+                /*  ppc_exception() leaves MSR[ME] set,
+                    where the architecture clears it on a
+                    machine check, so a further failing
+                    fetch here takes a second machine check
+                    instead of checkstopping (#QQQ).  */
+                ppc_exception(cpu, PPC_EXCEPTION_MC);
+                return;
+            }
+            /*  Clears only this CPU's running and parks
+                next_ic on nothing_call, which ends the
+                current batch.  memory.c's -T halt clears
+                every CPU's running; a checkstop is a
+                per-processor state.  pmppc has one CPU,
+                so what the other CPUs of a multiprocessor
+                do after this checkstop is not measured
+                (#PPP).  */
+            fatal("[ ppc: instruction fetch from 0x%" PRIx64
+                " declined with MSR[ME]=0: checkstop ]\n",
+                (uint64_t) addr);
+            cpu->running = 0;
+            cpu->cd.ppc.next_ic = &nothing_call;
+            return;
         }
     }
 
     {

--- a/src/include/cpu_ppc.h (HEAD)
+++ b/src/include/cpu_ppc.h (staged = working copy)
@@ -250,4 +250,5 @@
 
 /*  Exceptions:  */
+#define    PPC_EXCEPTION_MC    0x2    /*  Machine check, vector 0x200  */
 #define    PPC_EXCEPTION_DSI    0x3    /*  Data Storage Interrupt  */
 #define    PPC_EXCEPTION_ISI    0x4    /*  Instruction Storage Interrupt  */
```

### H1. gate 13's qhs block replayed over table 12's banked logs and synthetic logs (dryrun_qhs.py: the probe call replaced, marked, by a copy of each log; the real regress/lib.sh sourced)

```
Gate 13's qhslowifetch block, as staged, replayed over table 12's 93 banked logs and 13 synthetic logs, the probe call replaced by each log (`regress/artifacts/qhslowifetch/landing_20261105/DRYRUN_qhs.out`): base (the fix) green; HEAD red (146 of 262 checks); /bin/true red (160 of 262 checks); an absent binary red (190 of 262 checks); /bin/false red (189 of 262 checks); the 14 variants the probe scored green (D10_chk_run, D11_b_noref, D6_d_inv, D9_mc_vec, R5_arun, R5_cb, R7_G1_b_lt, R7_G2_d_msr, R7b_a_runun, V2_b_del, V3_c_true, V4_d_false, V5_d_true, V6_chk_nopark) green; the 74 it scored red, red; on every banked log the failing per-row pins are exactly the rows the log's PPC_IFETCH_RED names; the 13 synthetic logs (a dead probe; the sentinel missing, doubled or not last; protocol keys missing or doubled; a row lost, added, doubled or flipped; every row removed; a RESULT line that disagrees) each red on the pins they target; every one of the block's 262 checks failed on at least one leg.

--- base             249/249 CONTROL=OK SYMPTOM=ABSENT            want green got green; failing row pins == the log's RED list (0)
--- HEAD             108/249 CONTROL=OK SYMPTOM=PRESENT           want red   got red (146 of 262 checks); failing row pins == the log's RED list (141)
--- null_true        94/249 CONTROL=FAIL SYMPTOM=ABSENT           want red   got red (160 of 262 checks); failing row pins == the log's RED list (155)
--- null_absent      64/249 CONTROL=FAIL SYMPTOM=ABSENT           want red   got red (190 of 262 checks); failing row pins == the log's RED list (185)
--- null_false       65/249 CONTROL=FAIL SYMPTOM=ABSENT           want red   got red (189 of 262 checks); failing row pins == the log's RED list (184)
--- B1_exit_head     108/249 CONTROL=OK SYMPTOM=PRESENT           want red   got red (146 of 262 checks); failing row pins == the log's RED list (141)
--- X1 dead probe (empty log)                    got red (1 of 1 checks)
--- X2 sentinel missing                          got red (1 of 1 checks)
--- X3 sentinel duplicated                       got red (1 of 1 checks)
--- X4 a line after the sentinel                 got red (1 of 262 checks)
--- X5 RESULT line missing                       got red (2 of 262 checks)
--- X6 all four protocol keys missing            got red (8 of 262 checks)
--- X7 every protocol key printed twice          got red (8 of 262 checks)
--- X8 one row lost (T blr m3 lr)                got red (3 of 262 checks)
--- X9 one row added                             got red (2 of 262 checks)
--- X10 one row printed twice (T blr m3 lr)      got red (3 of 262 checks)
--- X11 one row FAIL, protocol unchanged (T blr m3 lr) got red (3 of 262 checks)
--- X12 every row line removed                   got red (251 of 262 checks)
--- X13 RESULT says 248/249                      got red (1 of 262 checks)

PIN COVERAGE (262 checks the base leg runs; legs on which each failed, over 93 banked + 13 synthetic legs):
    3  ppc_ifetch probe completed
    1  ppc_ifetch sentinel is the last line
    3  ppc_ifetch RESULT= lines
    2  ppc_ifetch CONTROL= lines
    2  ppc_ifetch SYMPTOM= lines
    2  ppc_ifetch RED= lines
   82  ppc_ifetch RESULT=249/249
    5  ppc_ifetch CONTROL=OK
    4  ppc_ifetch SYMPTOM=ABSENT
   80  ppc_ifetch RED=none
    4  ppc_ifetch rows run
   83  ppc_ifetch rows green
   79  ppc_ifetch rows red
  the 249 per-row pins: each failed on 1 to 30 legs; X12 (every row line removed) failed 249 of them
CHECKS THAT FAILED ON NO LEG: none
DRYRUN_QHS_OK

rows red on NO banked log, the three null media included (the union of table12/SCORES.txt's RED lists, which the replay shows equal to the failing per-row pins on every banked log): 3 -- isi text, isi nonex, isi1 nonex
(every leg's failing checks: landing_20261105/DRYRUN_qhs.out)
```

### H2. the rung-3 witness, and the last in-situ gate run

(witness_20261104/WITNESS.md, measured 2026-11-04 before any edit, the 17-row first probe frozen as witness_20261104/probe_frozen.py on UNMODIFIED -E pmppc; its narrative and the facts it lists are in the file)

| run | binary | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|---|
| `prefix_head.out` | the scratch clone /tmp/gx579 rebuilt with HEAD `ebe5af82`'s `cpu_ppc_instr.c`; `cpu_dyntrans.c`, `memory_rw.c`, `memory_ppc.c`, `core/memory.c`, `cpu_ppc.c`, `machine_pmppc.c` each checked `== HEAD` (`RUN.log`) | 11/17 | OK | PRESENT | the six `-T` rows |
| `prefix_build.out` | `build/gxemul` (HEAD plus the tree's six uncommitted product files; on this path only cpu_ppc_instr.c, whose diff is the three #579 X(llsc) hunks; part 1 (cpu_ppc_instr.c against SEC) CLEAN, part 2 FRESH) | 11/17 | OK | PRESENT | the six `-T` rows |
| `null.out` | `/bin/true` | 8/17 | FAIL | ABSENT | -- (the five exit-0 session rows and the three absent-text rows pass a non-emulator; neg apparatus fails) |
| `nobin.out` | a missing path | 3/17 | FAIL | ABSENT | -- |

The last IN-SITU run of gate 13 with this block: wiring_20261105/gate13.out (PASS, 359 checks) on the 56-row probe (wiring_20261105/gate13_ppc_ifetch.log: PPC_IFETCH_RESULT=56/56).  The 249-row block has never run in situ; block H1 replays it over table 12's logs, and the in-situ run is owed at landing.
