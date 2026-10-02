VERDICT: 9 confirmed-new, 9 confirmed-filed, 6 record-L4, 1 test-gap, 0 refuted, 0 unsettled, 0 duplicate, of 25 findings

FABLE_RETRO_3b_ALIVE_0928

Verbatim first line of `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`:
`# CHECKPOINT -- 2026-09-30 12:20 PAUSE POINT: no cron; r20 base leg, Fable 2e and two grok checks finishing on their own (087a90 sections rewritten; the peer's sections below are untouched)`

Adjudicator: the Fable seat (claude-fable-5-1), first-hand, 2026-10-01.  Every `src/` and `regress/` line below is at
`8ea26abb` (read with `git show 8ea26abb:<path>`; `src/` is byte-identical at HEAD `db8b1a33`).  `OUTSTANDING_BUGS.md`
lines are cited at `8ea26abb` AND hold at HEAD: `git diff 8ea26abb db8b1a33 -- OUTSTANDING_BUGS.md` has only two hunks,
at `:22514` and `:22611`, so every line below 22514 is identical in both (the three `#553` rows -- `wdcidresetcells`,
`analyze8robust`, `commitinflight` -- are appended at `:22619-22670` and none touches this batch).  `CHANGELOG.md` lines are
cited at `8ea26abb` with the HEAD line in brackets: the diff's hunks (`@@ -1,3 +1,81`, `-92,+170`, `-204,+284`,
`-280,+362`) add 84 lines before line 362 and nothing after, so HEAD = 8ea26abb + 84 for every line cited here.
Nothing was built, run or edited except this file.  The codex DRAFT (`codexpack_20260928/draft_3b/codex_draft_3b.txt`)
and the codex CHECK of it (`grokjobs_20260930/draftcheck_3b/codex_draftcheck_3b.txt`) were read AFTER my own pass over
each finding's source; where they disagree (cpumipsinstr:F1, cpumipsinstr:F2) and where the draft left a finding
unresolved (devsgiip30:F3) I ruled from the source first.  **I changed FOUR of the draft's dispositions** -- listed at
the end -- and qualified three severities.

---

## cpumips (2 findings)

**cpumips:F1 | CONFIRMED-NEW MED `mipsbadvpnscale` "R4000 Context/XContext BadVPN2 is scaled by the matched (or
last-scanned) TLB entry's page size instead of fixed VA bits 31:13 / 39:13"**
Checked: `memory_mips_v2p.c:286-287` (pmask == 0: `vaddr_vpn2 = (vaddr & vpn2_mask) >> pagemask_shift`, shift 13 from
`cop0.h:85` -- correct) versus `:313-314` (non-standard mask: `>> (pageshift + 1)`, pageshift 14 for a 16 KB pair from
`:295`) -> `cpu_mips.c:2096` and `:2100` insert it at `CONTEXT_BADVPN2_SHIFT`/`XCONTEXT_BADVPN2_SHIFT` = 4 (`cop0.h:80,150`);
the R4100 arm `:2081-2083,:2088` is a third site with the same input.  `mips_r4000.txt:957` ("bits 31:13 of the virtual
address ... For other page and PTE sizes, shifting and masking this value produces the appropriate address" -- i.e. the
OS shifts, the hardware field is fixed) and `:1032` (bits 39:13).  Astra's example holds: VA 0x4000 on a 16 KB pair gives
field 0 where 0x20 is owed.  **My extension (section b): the REFILL case is worse than Astra states** -- `vaddr_vpn2` is
reassigned for EVERY scanned entry (`:286-287`/`:313-314` precede the match test at `:341+`), so on a MISS the value
handed to `mips_cpu_exception` (`:452-453`) is the one computed with the LAST scanned entry's page mask, i.e. a refill's
Context pointer depends on the page size of an unrelated TLB entry.  Severity MED: a refill handler that indexes its PTE
table from Context loads the wrong PTE; the emulator does not terminate.  Not filed: `OUTSTANDING_BUGS.md` has no
BadVPN2/XContext mention (grep 0); `:2679-2680` records `#211`'s different AdEL/AdES correction.  Id absent from
`OUTSTANDING_BUGS.md` and `DISPOSITIONS.md`.  (Draft: same; kept.)

**cpumips:F2 | TEST-GAP-FILE `mipslowrefrow` (LOW)**
Checked: `cpu_mips.c:2003,2029-2037` is the `#278` site; `CHANGELOG.md:20502` [HEAD :20586] claims "Probe, 36/36 checks"
and itself says the only consumers of `LOW reference` were "the two TEST-FIRST probe rigs themselves and one read-only
marker counter" -- neither was committed.  `git grep -i 'LOW reference|lowref|low_ref' 8ea26abb -- regress/` outside
`regress/artifacts/` returns NOTHING; the only hits are quoted source in four archived seat answers.  Gap confirmed.
(Draft: same; kept.)

---

## cpumipsinstr (12 findings)

**cpumipsinstr:F1 | CONFIRMED-NEW HIGH `mipscop0tail` "Five COP0 decoder arms still `goto bad` (CPU stops) on
guest-executable encodings: EI/DI off-R5900, MFMCz non-ei/di, BC0x, unknown rs"**
Checked: `cpu_mips_instr.c:4922` (COP0_EI, `rev != R5900`), `:4928` (COP0_DI), `:5011` (MFMCz with `(iword & 0xffdf) !=
0x6000`), `:5021` (BCzc other than the DECstation `0x4100ffff`), `:5027` (rs not in {0,1,2,4,5,8,0xb,CO}) -> the shared
`bad:` at `cpu_dyntrans.c:2014` `cpu->running = 0` (`:1990-1991` exempts only speculative read-ahead); `emul.c:1052-1059`
then enters the debugger or ends the run.  **The halt happens at DECODE, before any privilege check**, so a user-mode
program's EI encoding stops the machine where silicon raises RI (`mips_r4000.txt:1154`) or CpU (`:1158`).  HIGH by the
rule's "stops it making progress" clause and by precedent (`ppcfmasingle` HIGH, batch 1b: `goto bad`).
**Draft CHANGED (FILED-BY-PROSE -> NEW):** `OUTSTANDING_BUGS.md:2668-2671` is the 2026-07-16 Codex round-19 BACKLOG line
("`cpu_mips_instr` `goto bad`/BREAK-reboot-sentinel/RDHWR/SUSPEND"); the twenty-third round at `:2601-2612` records it
CLEARED by `#234/#236/#237` and its "~5 remain" list at `:2612-2619` names RDHWR and not these arms.  A closed item is
not a filing for its residual (batch 2d: "a closed row is not a filing"; batch 2c: a shipped round is not a live id) --
the same rule Astra used to overturn batch 2a in the OTHER direction.  Grep for `COP0_EI|MFMCz|BCzc|ei_r5900|EI/DI` in
`OUTSTANDING_BUGS.md`: 0.  The check agreed; the draft did not.

**cpumipsinstr:F2 | CONFIRMED-NEW HIGH `mipsresetalias` "The reboot sentinel is gated on the VIRTUAL address's low 29
bits, so `break 0x30378` at any VA with low bits 0x1fc00000 stops the emulator (or raises CpU instead of BP)"**
Checked: `:4281-4296` derives `addr` from `cpu->pc` ("the (virtual) address"); `:4666-4667` tests `(addr & 0x1fffffff) ==
0x1fc00000`; `memory_mips_v2p.c:231-247` shows that masking is a physical identity only for kseg0/kseg1 -- VAs
0x1fc00000/0x3fc00000/0x5fc00000/0x7fc00000 (kuseg, TLB-mapped) and 0xdfc00000/0xffc00000 (kseg2/3) pass the test from
ordinary RAM.  `X(reboot)` at `:2612-2619` first runs `cop0_availability_check` and then `cpu->running = false`.  **So,
qualified as the draft says:** kernel mode (or user mode with CU0 set) -> the machine stops (HIGH); user mode with CU0
clear -> CpU where hardware owes BP (`mips_r4000.txt:1150`), a wrong exception (MED).  One row, HIGH.
**Draft CHANGED (FILED-BY-PROSE -> NEW):** `:2604-2605` records `#235` as DONE ("gated to the reset stub (phys
`0x1fc00000`), else real BP") -- a closed item with a FALSE description; `:2668` is the backlog line it closed.  Grep
`break 0x30378|reboot sentinel|0x1fc00000`: only those two lines.  L4 riders with the row: the `#235` comment at
`cpu_mips_instr.c:4660-4665` ("a guest that executes this encoding from ordinary RAM must get a real Breakpoint"),
`CHANGELOG.md:20152-20154` [HEAD :20236-20238] and `OUTSTANDING_BUGS.md:2604-2605` all say "phys" of a virtual test.

**cpumipsinstr:F3 | CONFIRMED-NEW LOW `mipsaddiuub` "ADDIU and seven fused-ADDIU handlers add two `int32_t` in signed
arithmetic (UB on the wrap ADDIU is defined to perform)"**
Checked: `:2363-2364` `(int32_t)reg + (int32_t)imm`, and `:245, :336, :1398, :3591, :3595, :3678, :3701`; `mips-iv.txt:129`
"No Integer Overflow exception occurs under any circumstances" (modulo arithmetic).  `configure` at `8ea26abb` sets no
`-fwrapv`/`-fno-strict-overflow` (grep: only `-O3`/`-O` at `:552,:555`; `Makefile.skel:5` passes `$(COPTIM)` through), so
the UB is real, not defined by flags.  Consequence under the rule: language-level, wraps in practice -> LOW, as batch 2a
graded `armuserpageshift`/`ppccrlogicshift`.  Distinct from `OB-24` (`:2916`, byte shifts) and `shiftubcensus` (`:16920`,
shifts).  (Draft: same; kept.)

**cpumipsinstr:F4 | CONFIRMED-NEW LOW `mipsjregionub` "MODE32 J/JAL/JAL_trace: `page_base + (int32_t)arg[1]` overflows
`int32_t` for a jump in the last two slots of page 0x7ffff000"**
Checked: `tmp_mips_tail.c:87` `MODE_int_t int32_t`; `:1542-1543, :1570-1571, :1598-1599`; decoder `:4834` `arg[1] = (addr &
0xffc) + 8` so arg[1] is 0x1000/0x1004 at offsets 0xff8/0xffc; `0x7ffff000 + 0x1000` exceeds INT32_MAX before the `- 4`.
With wrap the result (0x7ffffffc) and region are RIGHT, so this is pure UB -> LOW.  Flags checked as under F3.  (Draft:
same; kept.)

**cpumipsinstr:F5 | CONFIRMED-NEW MED `mipssubmin` "SUB/DSUB test overflow on the NEGATED subtrahend: MIN-MIN traps,
0-MIN does not"**
Checked: `:2094-2097` (`rt = -(uint32_t)rt`, then the ADD predicate on `rs`,`rt`,`rd`); `:2114-2117` for DSUB.  Worked:
rs=MIN, rt=MIN -> negated rt = MIN, rd = 0, predicate `rs<0 && rt<0 && rd>=0` TRUE -> spurious OV; rs=0, rt=MIN -> rd =
MIN, no term true -> missing OV where `mips_r4000.txt:5562`/`:4883` require a trap ("carries out of bits 30 and 31
differ").  MED (documented behaviour differs).  Not filed: `:2708-2710` describes the trap as ABSENT, not this predicate.
(Draft: same; kept.)

**cpumipsinstr:F6 | CONFIRMED-NEW MED `mipscachepriv` "The R3000 cache-invalidate fold mutates the loop register and
skips to the final MTC0 before any COP0 availability check runs"**
Checked: `:3384-3391` tests proposed IsC/alignment/budget only; the success path `:3394` writes `reg(ic[3].arg[0]) = ry` and
`:3398` jumps to `ic + 8` (the final mtc0, which DOES check at `:2457`); scalar `X(mtc0)` checks FIRST (`:2457-2458`); the
fold is installed only on EXC3K (`:4975-4978`, `:3995-4005`).  So a user-mode (CU0 clear) execution of the exact NetBSD
idiom gets CpU with EPC at the LAST mtc0 and rX already changed, where `mips-iv.txt:236` has the FIRST mtc0 trap with no
state change.  MED, **contrived** (the 9-instruction idiom, EXC3K, combinations enabled, user mode with CU0 clear) -- the
`mipssamepcstore` precedent.  Not the `#233 remainder` (`:2636-2638` names reads, the zero fold and the PC heuristic);
`:2666` is the generic predecessor `#233` closed.  (Draft: same; kept.)

**cpumipsinstr:F7 | CONFIRMED-FILED (by prose, no id) `OUTSTANDING_BUGS.md:2636-2638` -> propose id `mipsreadpriv`, MED**
Checked: `:2429-2437` mfc0, `:2439-2449` mfc0_select0, `:2491-2498` dmfc0, `:2500-2510` dmfc0_select0 -- no availability
check, three `TODO: cause exception if necessary`; decoder `:4965-4966` (and `:4950-4951` for CFC0) folds `rt == $zero` to
`instr(nop)`, which removes even the possibility.  `mips_r4000.txt:1158`: CpU for CP0 instructions in User/Supervisor mode.
The entry at `:2636-2638` ("the mfc0/dmfc0 READ-side availability check ... the `rt==$zero`->nop fold") is this defect,
deferred 2026-07-16.  The entry bundles three items; F7 is items 1-2 and F8 is item 3 -- two ids for one entry, as batch
2a did for `:1685-1687` (`ppcfprfclass`/`ppcveinhibit`).  Astra's "#233 remainder" is not an id.  (Draft: same; kept.)

**cpumipsinstr:F8 | CONFIRMED-FILED (by prose, no id) `OUTSTANDING_BUGS.md:2636-2638` -> propose id `mipsr3kpcpriv`, MED
(contrived)**
Checked: `cpu_mips_instr.c:83-84` `if (cpu->pc <= 0x7fffffff) in_usermode = 1;` with the file's own `TODO: if (... &
MIPS1_SR_KU_CUR)` at `:82`; `memory_mips_v2p.c:156-159` derives mode from Status.KU for the same CPU.  Wrong only for a
KERNEL (KUc=0) executing MTC0 from a mapped kuseg address with CU0 clear -> spurious CpU; user mode at kuseg and kernel at
kseg are classified right.  The entry names "the EXC3K user-mode-from-PC heuristic" explicitly.  **Astra's IDT citation
could not be checked locally: `_scratchpad/idt_r30xx.txt` is ZERO BYTES** (an empty extraction; the PDF is present at
1.2 MB and this environment cannot render it) -- the kernel-always-usable rule is taken from the architecture as stated
for the R4000 at `mips_r4000.txt:1158` (CpU "when the unit has not been marked usable and the process executes in either
User or Supervisor mode") and from the source's own TODO.  (Draft: same; kept.)

**cpumipsinstr:F9 | CONFIRMED-NEW MED `mipspsfault` "PS-format COP1 on an R3000/R4000-class FPU raises RI; the R4000
owes an FPU Unimplemented-Operation exception (Cause.E, FPE), and CpU when CU1 is clear"**
Checked: `:5084-5087` selects `instr(reserved)` for `isa_level != 5 && != 64`; `X(reserved)` (`:131-140`) raises RI with
no coprocessor-usable test; the bypassed `cop1_slow` checks `COPROC_AVAILABILITY_CHECK(1)` at `:2587`.
`mips_r4000.txt:1627`: "Any attempt to execute an instruction with an operation code or format code that has been
reserved for future definition sets the Unimplemented bit in the Cause field in the FPU Control/Status register and
traps"; `:1154` lists RI's causes and a reserved COP1 fmt is not among them; `:1158`/`:1162` CpU and FPE.  MED.  Scope:
isa_level 1-4 (the R3000A/R4000 audit targets); whether MIPS32 R1 wants RI is not decided here.  Not filed: the older
PS entry `:2257-2269` PRESCRIBES RI ("instead of raising Reserved Instruction", `:2260-2261`) -- it is the record side of
this defect, not a filing of it; `:1774-1777` is PS arithmetic.  L4 riders with the row: that `:2260-2261` prescription
and the `#290` comment at `cpu_mips_instr.c:5071-5074` ("the encoding is reserved, so raise RI").  (Draft: same; kept.)

**cpumipsinstr:F10 | CONFIRMED-NEW MED `mipssynci` "SYNCI has no REGIMM decoder case, so modelled Release-2 CPUs
(4KEc, 24KEc, 5KE) raise RI on a defined instruction"**
Checked: REGIMM switch `:5275-5414` -- cases 0-3, 0x10-0x13 (branches), 8-0xc, 0xe (traps); `default:` `:5410`
`instr(reserved)`.  `opcodes_mips.h:251` `REGIMM_SYNCI 0x1f`; `mips_cpu_types.h:102,104,105` isa 32/64 revision 2 models.
`mips32_volII.txt:1665` "MIPS32 Release 2"; the same page: "Reserved Instruction exception (Release 1 implementations
only)".  MED (documented behaviour differs); no rig boots an R2 core, so reachability is by `-C 4KEc` on a test machine.
Grep `SYNCI` in `OUTSTANDING_BUGS.md`: 0 relevant (two "syncing" hits).  (Draft: same; kept.)

**cpumipsinstr:F11 | RECORD-L4 `CHANGELOG.md:19998-20000` [HEAD :20082-20084]**
Checked: the sentence "the MIPS Integer-Overflow *trap* turned out to be **already correctly implemented** --
`add`/`addi`/`sub`/`dadd`/`daddi`/`dsub` raise `EXCEPTION_OV` on overflow" is false of `sub`/`dsub` per F5.  Replacement
for the first sentence (keep the UBSan explanation from "The audit's UBSan hit ..." unchanged):
"**#209 (`cpu_mips_instr.c`, MIPS integer add/sub -- audit follow-up):** the MIPS Integer-Overflow *trap* was already
present at all six sites -- `add`/`addi`/`dadd`/`daddi` raise `EXCEPTION_OV` correctly, while `sub`/`dsub` test overflow
on the NEGATED subtrahend and are wrong when it is the minimum signed value (MIN-MIN traps, 0-MIN does not; row
`mipssubmin`) -- and OpenBSD boots with it."
Rider (same L4): `OUTSTANDING_BUGS.md:2708-2710` says the opposite -- the trap "defined 2's-complement wrap in practice;
a real trap is the hottest instruction path + boot-regression risk, so left per OB-24" -- i.e. the queue records the trap
as ABSENT while the CHANGELOG records it PRESENT.  Replace with: "the MIPS `add/addi/sub` Integer-Overflow trap IS
implemented (see CHANGELOG #209); what remained was UB in the detection arithmetic (fixed by #209) and the `sub`/`dsub`
minimum-subtrahend predicate (`mipssubmin`)."  (Draft: same disposition; wording mine.)

**cpumipsinstr:F12 | RECORD-L4 `CHANGELOG.md:23042-23044` [HEAD :23126-23128] + source rider `cpu_mips_instr.c:5377-5379`**
Checked: "three CPU-specific ones" -- `grep -n 'MTSAB|MTSAH|SYNCI' cpu_mips_instr.c` at `8ea26abb`: ZERO hits; the three
have header definitions only (`opcodes_mips.h:249-251`) and reach the `default:` arm.  **And the in-source comment has the
same hole**: `:5377-5379` enumerates the unimplemented set as "(4-7, 0xd, 0xf, 0x14-0x17, 0x1a-0x1e)", which omits exactly
0x18, 0x19 and 0x1f -- the three the author believed implemented.  Replacement, CHANGELOG: "The implemented sub-opcodes
are the eight conditional branches and branch-and-links (rt 0-3, 0x10-0x13) and the six trap-immediates (rt 8-0xc, 0xe);
everything else -- rt 4-7, 0xd, 0xf, 0x14-0x1f, which includes MTSAB (0x18), MTSAH (0x19) and SYNCI (0x1f), none of which
has a decoder case -- stopped the machine."  Replacement, source: "(4-7, 0xd, 0xf, 0x14-0x1f)".  (Draft: CHANGELOG only;
the source rider is mine.)

---

## devsgiip30 (3 findings)

**devsgiip30:F1 | CONFIRMED-FILED `ip30setisrassign` (queue MED, kept)**
Checked: `dev_sgi_ip30.c:203` `d->isr = idata;` against the sibling `:251` `d->isr &= ~idata;` and the read at `:310`;
`OUTSTANDING_BUGS.md:21612-21623` records the identical defect with a MEASURED sequence (`0x00ff` then `0x5a00` -> `0x5a00`).
`heart.h` is NOT in the tree (`git grep heart.h 8ea26abb -- src/` hits only this file's comments), so the hardware
authority stays an inference from the set/clear PAIR plus Linux's per-bit IPI writes, as the draft said.  (Draft: same.)

**devsgiip30:F2 | RECORD-L4 `dev_sgi_ip30.c:50-52, :57-60` + rider `:216-218, :264-266`**
Checked: announce sites are the timer `:148` and the WRITE arms `:206`, `:254`, `:303` -- FOUR; the read arms `:210-243`
and `:258-287` contain comments only.  Replacement for `:50-52`: "FOUR announce paths share TWO bits, and that is
deliberate: IP30_W_ISR covers THREE (the 0x10020, 0x10028 and 0x10030 WRITES), which all print the SAME string byte for
byte; the 0x10020 and 0x10028 READS are silent declines and touch no latch."  Replacement for `:59` "five bits on the ISR
side" -> "three bits on the ISR side".  Rider: the two read-arm comments' "All five ISR sites print one byte-identical
string" (`:216-218`, `:264-266`) describe the pre-decline state in the present tense -> "All five ISR sites PRINTED (before
this decline was adopted)".  (Draft: same disposition; the read-arm rider is the check's, verified here.)

**devsgiip30:F3 | RECORD-L4 `CHANGELOG.md:2097` [HEAD :2181] + rider `regress/artifacts/ip30abortkill/ip30_abort_probe.py:187`**
**Draft CHANGED (DOUBTFUL -> RECORD-L4).**  The draft and the check both left this unchecked as "outside the permitted
artifact scope"; the probe is TRACKED at `8ea26abb` (`git ls-tree`: blob `a1259e35`), so it is a committed file and in
scope.  Checked: `:467` `t, alive = session(...)` scores BOTH `tick 50` (`:468`) and `tick 50 txt` (`:474`); `:553` one
session scores `xbit isr` (`:554`) and `xbit tick` (`:559`), deliberately ("it needs both announce classes in ONE
lifetime", `:557-558`).  The probe's own docstring at `:187` says "One fresh process per scored row." -- false of itself.
Replacement for the CHANGELOG: "one fresh process per SESSION -- most sessions score one row, but `tick 50`/`tick 50 txt`
and `xbit isr`/`xbit tick` each score two rows from one process, by design (the cross-bit mutant needs both announce
classes in one device lifetime)"; same correction to the docstring at `:187`.

---

## devsgire (8 findings)

**devsgire:F1 | CONFIRMED-FILED `sgirespanchk` -- with the row's open question ANSWERED and its grade re-opened:
RULE-QUESTION shoddprfield (consequence shown: MED; by the rule's letter: HIGH).  Rider to `sgilinearoob`.**
Checked, every link: ARC `GetFileInformation` (`arcbios.c:1137-1150`) calls `store_64bit_word` at a guest-supplied `A1`
(+0, +8, +16) -> `memory.c:763-783` -> `memory_rw(len 8, MEM_WRITE)`; ARC `Seek` (`:1905-1910`) reads 8 bytes from `A1`;
`MEMORY_RW` (`memory_rw.c:183-227`) has NO alignment test -- it only splits at a 1 KiB granule (`MRW_SPLIT_MASK 0x3ff`,
`:104`, `:187-223`) -- and the device dispatch at `:583-589` hands `paddr`/`len` to the handler unchanged.  The RE is
registered at `0x15000000 + 0x1000` (`machine_sgi.c:500`, `dev_sgi_re.c:850`) and adds 0x1000 back (`:435`), so with
`crmfbreg.h:230-237` TLB_A ends at phys `0x15001200`, TLB_C at `0x15001600`, LINEAR_A at `0x15001780` -- none a 1 KiB
boundary, so an 8-byte access at bank offset 0x1fe / 0x7c reaches the handler WHOLE -- while TLB_B (`0x15001400`) and
LINEAR_B (`0x15001800`) end ON one and the split declines both halves (`len != 8`).  Exactly Astra's bank list.  Then
`:499-504` (TLB_A write, tlbi 255 -> `re_tlb_a[255..258]`, i.e. `re_tlb_b[0..2]`), `:523-527` (read), `:562-566`/`:571-575`
(TLB_C -> `re_tex[0..2]`), `:705-707`/`:731-733` (LINEAR_A tlbi 31 -> `re_linear_a[32]` = `re_linear_b[0]`); TEX is safe
(`:586` `>> 3` caps tlbi at 31+3 < 112).  All inside the heap struct `sgi_re_data` (`:172-180`): a guest-controlled
firmware call clobbers up to three registers of ANOTHER bank, deterministically -- MED by consequence, intra-struct, no
host escape; the rule's letter says HIGH, which is the open `shoddprfield` question and is not settled here.
Why FILED and not NEW: `OUTSTANDING_BUGS.md:16292-16330` IS this defect ("the write SPAN is not [checked]") and its own
`:16327-16330` names the open question -- non-CPU callers "were not enumerated" -- which F1 answers: the ARC emulation
is one.  Riders (L4, with the row): `dev_sgi_re.c:645-654` ("ONE EXCEPTION, AND IT IS NOT A GUEST PATH: the host
debugger's `put d` ... NOT guest-reachable while this guard stands") is false -- ARC GetFileInformation/Seek are guest
paths that hand an unaligned `len == 8` to `memory_rw`; `:630-640` enumerates only CPU load/store paths as "the GUEST
paths"; `OUTSTANDING_BUGS.md:14754` ("unreachable today for exactly one reason: `len == 8` forces 8-byte alignment") is
false for the same reason, so `sgilinearoob`'s `[tlbi+1]` at 31 is ARC-reachable too; `:16318-16322`'s discharge was
scoped to "the normal SGI CPU access paths" and stands as scoped.  (Draft: FILED `sgirespanchk`, "HIGH for array-bound
violations"; disposition kept, grade re-marked as the rule question the brief names.)

**devsgire:F2 | CONFIRMED-FILED `sgirebufuninit` (queue HIGH "under active adjudication"; by this brief's rule MED)**
Checked: `:321` `uint8_t buf[8]` uninitialised; `:225` `bufdepth = 1 << ((mode >> 8) & 3)` independent of `color_mode`;
PUT arms assign `buf[0]` (CI, `:326`) or `buf[0..3]` (`:329-345`) while `:374-375` copies `bufdepth`; GET `:377-378` reads
`bufdepth` bytes and `:408-417` consume 3-4.  The 16-bit tiled MTE cell is already disclosed in `#509`'s comment
(`:1550-1553`).  `OUTSTANDING_BUGS.md:15810-15833` records both directions and says the grade is held for a roster.  Under
the brief's three clauses this is MED (in-bounds uninitialised bytes reach guest memory; no bound crossed, no stop); the
queue's HIGH rests on host-stack disclosure, which the rule does not enumerate -- carry both until that row's own
adjudication lands.  (Draft: same.)

**devsgire:F3 | CONFIRMED-FILED `sgirebufshiftub` (LOW)**
Checked: `:408, :411, :414, :417` `buf[i] << 24` on `uint8_t` -> `int`; `OUTSTANDING_BUGS.md:16377-16394` ("on all four GET
arms").  (Draft: same.)

**devsgire:F4 | CONFIRMED-FILED `sgiretlbshiftub` (queue "med"; by this brief's rule LOW)**
Checked: `:258, :260, :262` `uint16_t << 16` -> `int`, and `:312` accepts only pointers with bit 31 set, so every accepted
entry overflows; `OUTSTANDING_BUGS.md:18558-18570`.  Language-level, wraps in practice, no consequence beyond UBSan -> LOW,
as batch 2a graded the `1 << 31` forms; the queue's "med" warrant is ubiquity, not consequence.  (Draft: same.)

**devsgire:F5 | CONFIRMED-FILED `sgirandomskipput` (queue MED, kept), with the draft's ROP/stipple qualification**
Checked: `:1042` `color = fg`; `:1050-1051` the GET; an unsupported mode returns at `:308` leaving `*color`; `:1096-1097`
the dependent PUT.  Qualification confirmed from `:1053-1094`: `POLY_STIP` can skip the PUT (`draw = 0`, `:1058`) or
substitute bg; ROP XOR/COPY_INVERTED write a function of `oldcolor` -- "the destination receives foreground" holds for
ROP COPY without stipple.  `OUTSTANDING_BUGS.md:15761-15767`.  Wording rider (not L4): `dev_sgi_re.c:289-290` and
`:15762` say "fg" unconditionally.  (Draft: same.)

**devsgire:F6 | RECORD-L4 `dev_sgi_re.c:294-295`**
Checked: the comment says the COLOUR-mode switch "carries the same random() shape at its own default (row
sgirandomcolour)"; `#519` made it `ok = 0` (`:364`) + latched announce (`:365-370`) + `if (ok)` store (`:373-375`).  The
`sgirandomcolour` row stays open for its detector (`:19288-19301`), not for this code.  Replacement: "and the COLOUR-mode
switch below USED TO carry the same random() shape at its own default -- #519 (row sgirandomcolour) made it a latched
decline that clears `ok` and stores nothing".  (Draft: same disposition.)

**devsgire:F7 | RECORD-L4 `dev_sgi_re.c:465-469` -- discharges the owed sentence at `OUTSTANDING_BUGS.md:14775-14778`**
**Draft CHANGED (FILED-BY-PROSE + new id `sgirewidthrationale` -> RECORD-L4, no id).**  Checked: `:465-469` says a
narrower access "simply runs fewer iterations and stays in bounds -- there the guard is modelling fidelity only"; the
loop at `:500-501` (and `:563-564`, `:587-588`) reads `data[hwi]*256 + data[hwi+1]`, so `len == 1` would read `data[1]`,
one past the caller's `uint8_t data[LS_SIZE]` (`cpu_mips_instr_loadstore.c:46`); the `:491` guard is what prevents it;
`memory.c:55-77` adds no even-width filter.  The queue ALREADY records the correct reason at `:14770-14773` and says "The
round owes a sentence, not a row" -- so this is a false comment (the brief's rule 1, corrected in place), and giving it
an id would manufacture the row the queue declined.  Replacement for `:465-469`: "3. The guards are NOT redundant, and
for TLB_A/B/C and TEX they are not modelling fidelity only: the store loop consumes TWO bytes per iteration
(`data[hwi]*256 + data[hwi+1]`), so a len == 1 access would read `data[1]`, one byte past the caller's one-byte buffer
(cpu_mips_instr_loadstore.c `data[LS_SIZE]`) -- the width guard is a memory-safety check there too
(OUTSTANDING_BUGS.md:14770-14773).  For LINEAR_A and LINEAR_B the store is fixed-arity; see the note at those two sites."

**devsgire:F8 | CONFIRMED-FILED `sgidefatalstale` (LOW)**
Checked: `:487-488` "DEVICE_ACCESS(sgi_de)'s own width kill"; the arm at `:1181-1220` latches and `goto de_declined`
(`:1438-1444` answers and returns 1); accepted widths {4,8} at `:1169-1181`.  `OUTSTANDING_BUGS.md:18183-18191` records
the exact wording.  The draft's replacement ("own width decline, whose accepted widths are {4,8} rather than {8}
(sgidewidth)") is accurate and goes with that row.  (Draft: same.)

---

## (a) CODE findings I could NOT confirm, or confirm only as qualified

None was refuted.  Qualified: **cpumipsinstr:F2** -- the availability check precedes the stop, so user mode with CU0 clear
gets a WRONG EXCEPTION (CpU for BP), not a stop; the stop is kernel-mode (or CU0-set) reachable.  **cpumipsinstr:F4** --
UB only for a J/JAL in the last two slots of page 0x7ffff000, and the wrapped result is the correct address.
**cpumipsinstr:F6** -- reachability is contrived (the exact NetBSD idiom, EXC3K only, combinations on, user mode with CU0
clear).  **cpumipsinstr:F8** -- Astra's IDT-manual pages could not be checked: `_scratchpad/idt_r30xx.txt` is 0 bytes;
ruled on the source inconsistency and the R4000 manual's User/Supervisor-only CpU clause.  **devsgiip30:F1** -- `heart.h`
is not in the tree; MED rests on the set/clear-pair inference.  **devsgire:F5** -- "foreground" only under ROP COPY
without stipple.  **devsgire:F1** -- confirmed in full as a reachability finding; its SEVERITY is the open rule question.

## (b) What Astra missed, noticed while checking (mine unless credited)

1. **cpumips:F1's REFILL half (mine):** `vaddr_vpn2` is recomputed for every scanned entry before the match test
   (`memory_mips_v2p.c:286-287, :313-314`), so on a MISS the Context/XContext BadVPN2 handed to `mips_cpu_exception`
   (`:452-453`) carries the LAST scanned entry's page-size scaling -- a refill's PTE pointer depends on an unrelated TLB
   entry's PageMask.  Same row `mipsbadvpnscale`; it widens the reach from invalid/modified faults on large pages to every
   refill while a large-page entry sits at the scan's last index.
2. **`mipstrapgate` MED (candidate; the REGIMM half raised by the codex draft CHECK's section (b), verified here; the
   SPECIAL half is mine):** `cpu_mips_instr.c:5358-5369` replaces TGEI/TGEIU/TLTI/TLTIU/TEQI/TNEI with `instr(reserved)`
   when `isa_level < 32`, so the R4000 (isa 3, `mips_cpu_types.h:73`), R4400, R5000 and R10000 raise RI on instructions
   their manual defines (`mips_r4000.txt:1141` Trap exception "when a TGE, ..., TGEI, ..., or TNEI instruction results in a
   TRUE condition"; `:5683` TEQI) -- the gate should be `< 2` (MIPS II).  **The SPECIAL-form traps have the opposite
   defect:** `:4535-4540` decode TGE/TGEU/TLT/TLTU/TEQ/TNE with NO ISA gate, so an R3000 (MIPS I) executes them where RI
   is owed.  One row, both halves.  Not filed (`grep -i 'TGEI|TEQI|Trap opcode|trap-immediate'` in `OUTSTANDING_BUGS.md`:
   0; absent from `DISPOSITIONS.md`).  L4 riders: `CHANGELOG.md:23049-23051` [HEAD :23133-23135] and the comment at
   `cpu_mips_instr.c:5384-5386` cite that gate as "the tree's own shape" -- the shape is the defect.
3. **`_scratchpad/idt_r30xx.txt` is EMPTY (0 bytes, 2026-07-25)** while `CLAUDE.md` lists it among the extracted manual
   texts and the PDF (1.2 MB) is present.  Any past "checked against the IDT R3000 manual" claim that used the text file
   checked nothing.  Apparatus/records, LOW; one line in the carrier's manual list, not a queue row.
4. **cpumipsinstr:F7 scope note:** the `rt == $zero -> nop` fold also drops CFC0 (`:4950-4951`); include it in
   `mipsreadpriv`.
5. **cpumipsinstr:F9/F2 record riders** are listed under those findings (the `#290` RI prescription at `:5071-5074` and
   `OUTSTANDING_BUGS.md:2260-2261`; the `#235` "phys" wording at `:4660-4665`, `CHANGELOG.md:20152-20154` and
   `OUTSTANDING_BUGS.md:2604-2605`).

## Draft dispositions changed, and why

| finding | draft | ruling | why |
|---|---|---|---|
| cpumipsinstr:F1 | FILED-BY-PROSE :2668-2671 | CONFIRMED-NEW HIGH `mipscop0tail` | the backlog line is CLOSED by `#234/#236/#237` (:2601-2619); a closed item is not a filing for its residual; the five arms are named nowhere |
| cpumipsinstr:F2 | FILED-BY-PROSE :2668-2671 "reopen" | CONFIRMED-NEW HIGH `mipsresetalias` | `#235` is recorded DONE at :2604-2605 with a false description; same rule |
| devsgiip30:F3 | DOUBTFUL (probe "out of scope") | RECORD-L4 | the probe is a committed file at `8ea26abb`; read, and it scores two rows per session twice (:467-474, :553-559) |
| devsgire:F7 | FILED-BY-PROSE + new id `sgirewidthrationale` | RECORD-L4, no id | a false comment is corrected in place (rule 1); the queue paragraph it cites says "owes a sentence, not a row" |

Severities qualified against the draft: devsgire:F1 (draft HIGH -> RULE-QUESTION shoddprfield, MED by consequence);
devsgire:F2 (MED under the rule, the queue's HIGH left to its pending adjudication); the rest of the draft's grades kept.
Against the CHECK: it was right on F1/F2 (NEW) and left F3 (ip30) and F7 (re) where the draft had them; both changed here.

## (c) DENOMINATOR

**25 of 25 findings checked against the source at `8ea26abb`; 0 ruled from Astra's text alone.**  Every cited
`path:line` was opened; every `OUTSTANDING_BUGS.md` id or prose range was opened at HEAD and shown identical at
`8ea26abb` by the diff's hunk headers (both hunks >= :22514); every CHANGELOG passage was read at `8ea26abb` and its HEAD
line derived from the diff (+84).  Manuals opened at the cited lines: `mips_r4000.txt`, `mips-iv.txt`, `mips32_volII.txt`.
NOT checkable locally: the IDT R3000 pages (`idt_r30xx.txt` is empty; the PDF cannot be rendered here) and NetBSD's
`heart.h` (not in the tree) -- both stated at the finding.  Astra's clean-check inventories were not re-verified.
Nothing was built, run or edited; this file is the only write.
