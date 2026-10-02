VERDICT: 8 confirmed-new, 7 confirmed-filed, 1 record-L4, 0 test-gap, 0 refuted, 0 unsettled, 9 duplicate, of 25 findings

FABLE_RETRO_3a_ALIVE_0928

CHECKPOINT.md first line, verbatim:
`# CHECKPOINT -- 2026-09-30 12:20 PAUSE POINT: no cron; r20 base leg, Fable 2e and two grok checks finishing on their own (087a90 sections rewritten; the peer's sections below are untouched)`

ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 3a (cpu_m88k.c, cpu_m88k_instr.c, generate_m88k_bcnd.c,
tmp_m88k_bcnd.c).  Adjudicated at `8ea26abb`; HEAD is `db8b1a33` and `git show --stat db8b1a33` touches no `src/`
file, so every `src/` and `regress/` line below is HEAD's too.  `CHANGELOG.md` and `OUTSTANDING_BUGS.md` are cited
at `8ea26abb` (the CHANGELOG is +84 lines at HEAD, verified three times: 8ea26abb:7782 = HEAD:7866, :22086 = :22170,
:23019 = :23103; the OUTSTANDING_BUGS.md lines cited here are identical at both commits, re-read at HEAD).  Ids were
checked for EXISTENCE at HEAD (`git show HEAD:OUTSTANDING_BUGS.md`) and in `DISPOSITIONS.md`.  Read only: `git show
8ea26abb:<path>` piped through `awk '{print NR": "$0}'`, `_scratchpad/mc88100.txt` at the cited lines, and the
upstream import `39748e3c` where provenance mattered; nothing built, run or edited except this file.  Model:
claude-fable-5-1, first-hand.

The codex draft (`codexpack_20260928/draft_3a/codex_draft_3a.txt`) and its check
(`grokjobs_20260930/draftcheck_3a/codex_draftcheck_3a.txt`) agree on all 25 lines, and both are the findings'
own model family, so their agreement was treated as a pointer to what to re-run, not as evidence.  Every lookup was
re-run.  The draft's dispositions CHANGE in these places: (1) tmpm88kbcnd:F1 is not a second row -- the generator's
recursion and the generated handler's dispatch walk have ONE root cause (no delayed branch checks whether it was
itself entered as a delay slot) and one fix, so it is DUPLICATE of generatem88kbcnd:F1 and the row `m88kbcndnest`
carries both consequences; (2) cpum88kinstr:F5's `m88kconvr0` (int/nint only) is replaced by `m88kfpr0stop` over all
EIGHT `d == 0 -> goto bad` sites, which the manual covers with one sentence; (3) cpum88kinstr:F7 is widened from
`fdiv.dds` to the SEVENTEEN double-destination writers and gains an L4 rider on cpu_m88k.h's "always zero" comment;
(4) cpum88kinstr:F4 gains `flt.ds`'s odd-DESTINATION rejection; (5) cpum88kinstr:F3 gains an L4 rider on the #195
comment whose premise the finding refutes; (6) cpum88kinstr:F2's rotate site is cross-referenced INTO the new row
rather than left under a shipped-round heading; (7) the PSR byte-order stop the check's section (b) raised is
verified and filed as `m88kpsrbokill` HIGH (the draft has no such line); (8) cpum88kinstr:F12's L4 text is rewritten
to name the mechanism and the id.  Everything else stands as the draft wrote it, re-verified.

Severity is graded by the brief's rule from the source, and four FILED rows carry a grade the queue does not:
`m88kexcsfu1` (queue MEDIUM) is HIGH -- a USER-mode `divu` with SFD1 set stops every CPU (probe row `usfu1`);
`m88kexctaildefault` (queue "LOW, design-option record") is HIGH by the rule's letter, supervisor-only;
`m88kexchwtraps` (queue LOW) is HIGH for its vector-0 half; `m88kexcfrozendmt` (queue LOW) is MED.  A `goto bad` /
`cpu->running = 0` is graded as the brief's "stops it making progress" (OUTSTANDING_BUGS.md:16993-16994 records that it
stops the virtual CPU and does not exit the host; batch 1b graded `ppcfmasingle` HIGH on the same shape).

---

cpum88k:F1 | CONFIRMED-FILED m88kexcsfu1
Checked: cpu_m88k.c:753-759 (SFU1_PRECISE/IMPRECISE leave `implemented` false) and :799-807 (every CPU's `running = false`); the residual-vector half (11..113, 116..127 via supervisor tb0/tb1/tcnd) is `m88kexctaildefault`, OUTSTANDING_BUGS.md:371-372, and the SFU1 half is :490-492; regress/m88k_exc_probe.py:452 pins `usfu1`/`sfu1h`/`resid11`/`resid50`/`resid127` as HALT on purpose; manual :9282-9285 (traps may name any vector), :10324-10327 (FPU-disabled exception).  Both ids exist at HEAD.  HIGH by the rule (user-mode reachable through SFU1).

cpum88k:F2 | CONFIRMED-FILED m88kdslotshadow
Checked: cpu_m88k.c:849-853 (`SNIP = pc + 4`, `SFIP = delay_target`), X(rte) at cpu_m88k_instr.c:2282-2319 (executes the SNIP instruction, then jumps to FIP when `fip != nip + 4`), manual :2093-2104 (NIP = next to execute, FIP = taken target while the branch executes) and :8898-8913, :8931-8935; OUTSTANDING_BUGS.md:356-362 records exactly this ("the guest executes the instruction the taken branch skipped") and the probe's `dslot` row (:29-37, :624-629) pins the arm AS IMPLEMENTED and says so.  MED.

cpum88k:F3 | CONFIRMED-FILED m88kexcfrozendmt
Checked: cpu_m88k.c:811-821 (`update_shadow_regs = false` under SFRZ for a trap) against :870-879 (DMT0..DMA2 zeroed unconditionally, outside that guard); manual :9290-9294 ("none of the exception-time or shadow registers are modified"); OUTSTANDING_BUGS.md:364-365 records it (LOW).  MED by the rule; the probe's `trapfrozen*` rows (:620-623) check SXIP/SNIP/SFIP/EPSR only, and :192 discloses "DMT contents" as uncovered.

cpum88k:F4 | CONFIRMED-NEW MED m88kdivcontext "Integer-divide (and precise FP) exception delivery writes no fcr2/fcr4/fcr5 and clears the destination scoreboard bit"
Checked: cpu_m88k.c:835 (`SSBR = 0` on every unfrozen delivery) and :958-960 (the fork's own comment: "Not modelled, disclosed: scoreboard capture ... and fcr2/fcr4/fcr5 for the divide"); the four raise sites cpu_m88k_instr.c:612, :624, :719, :731 write no fcr; manual :10302-10314 (SXIP, destination unchanged BUT its scoreboard bit SET, fcr2/fcr4 = operands, fcr5 = destination number) and :10319-10322 (every precise FP exception sets the destination scoreboard bits).  OUTSTANDING_BUGS.md greps for `fcr2|fcr5|scoreboard` find NOTHING; the disclosure lives only in the source comment, CHANGELOG.md:7782 and the probe header :192 -- a disclosure, not a filing.  Guest-visible: a handler reading fcr5 to clear the scoreboard bit reads a stale value.

cpum88k:F5 | CONFIRMED-FILED m88kidledup
Checked: cpu_m88k.c:343-352 (the counters), cpu_m88k_instr.c:2743-2744 (`slot_runs ++` beside `ic[3].f(...)`: a duplicated call without a duplicated increment is invisible), regress/gate_m88k_rounding.sh:212-214 (`slt -eq ntn`), regress/m88k_idle_probe.py:11, :68 (the witness is one idempotent store); OUTSTANDING_BUGS.md:494-495 and :15552-15554 ("cannot see a duplicated slot call whose counter is not duplicated"); DISPOSITIONS.md:39 confirmed it in batch 1b.  LOW.

cpum88kinstr:F1 | CONFIRMED-NEW MED m88kextcross "ext with offset+width > 32 no longer sign-extends from bit 31"
Checked: cpu_m88k_instr.c:459-470 -- `x = src >> o; x &= (1<<w)-1; if (x & signbit)`: for src 0x80000000, w = 2, o = 31 the shifted value is 1, the tested sign bit is bit 1 (clear), result 1; the upstream import 39748e3c:459-468 did `int32_t x >>= o` (arithmetic) then `<<= 32-w; >>= 32-w`, which yields 0xffffffff -- so the #46 rewrite that removed the signed-shift UB LOST this case (and only this case: the `w == 0` arm at :467-468 handles width 32 correctly).  Manual :4480-4481: "If the bit field extends beyond bit 31, then bit 31 is used as the sign bit".  `extu` is unaffected (no sign).  Unfiled (greps for `ext`, `bit 31`, `sign-extended` hit nothing m88k).

cpum88kinstr:F2 | CONFIRMED-NEW LOW m88ktrapmask "tb0/tb1 build their bit mask with a signed 1 << d (undefined at d = 31); m88k_rot's (1 << n) - 1 is the same class"
Checked: cpu_m88k_instr.c:3540 (`ic->arg[0] = 1 << d`) against the repaired sibling :3454 (`1U << d`); the consumers :2550 and :2563 AND a uint32_t register with the size_t arg, so on the common lowering (INT_MIN sign-extended into size_t) bit 31 still tests correctly -- no observable consequence established, hence LOW.  The rotate site :513 is recorded by prose at OUTSTANDING_BUGS.md:17085-17096 under the `armbfxwidth32` heading (:17038), which DISPOSITIONS.md:335-336 already ruled "names a SHIPPED round, not a live id"; it belongs in this row as its second site, both as children of `shiftubcensus` (batch 2a/2d precedent), not as a second id.

cpum88kinstr:F3 | CONFIRMED-NEW MED m88knegdiv "div completes negative-operand divisions that the MC88100 traps on; the #195 comment states a false premise"
Checked: cpu_m88k_instr.c:723-742 (X(div) traps only on a zero divisor; :732-737 completes INT_MIN/-1 as 0x80000000; :739-740 completes every other negative case) and :616-628 (div_imm: a negative rS1 completes); manual :4389-4390 ("If the divisor is zero or EITHER operand is negative, an integer divide exception is generated") and :10302-10305 (destination unchanged).  OUTSTANDING_BUGS.md:2700-2703 is the #188-#208 round record, not a filing; greps for `negative operand`, `INT_MIN` find nothing m88k.  Distinct from cpum88k:F4 (what the handler receives once an exception IS raised).  L4 RIDER on :734-736, whose "the m88k ALU yields the wrapped 2's-complement result 0x80000000" is false of the hardware -- replacement: "/*  #195: INT_MIN / -1 overflows and is C UB (host SIGFPE); complete it as the wrapped two's-complement 0x80000000 rather than crash.  The MC88100 never computes this case: `div` takes the integer-divide exception whenever EITHER operand is negative and leaves rD unchanged (UM 6.8.3), which this handler does not raise for any negative operand -- row m88knegdiv.  */".  Whether the guest kernel completes the trap identically is NOT established here (no OpenBSD source on disk); the guest-visible difference is the missing trap and the written destination.

cpum88kinstr:F4 | CONFIRMED-NEW HIGH m88kconvodd "int.sd/nint.sd/trnc.sd reject an odd source register, and flt.ds an odd destination, by stopping the CPU"
Checked: cpu_m88k_instr.c:3326-3329 (`if (s2 & 1) ... goto bad`, #302), :3346-3349 (trnc.sd, same), and :3235-3238 (flt.ds: `if (d & 1) goto bad` -- the check's (b), verified; same class, same row); cpu_dyntrans.c:1983-2014 (`bad:` reports "UNIMPLEMENTED instruction" and sets `cpu->running = 0`).  Manual :1630-1634: a double operand is rn/rn+1 with NO evenness requirement, and the pair may begin at r31 (r0 as the low word); :4948-4953 (flt's destination "can be single or double precision").  Unfiled (greps for `uneven`, `odd register`).  A legal encoding stops the machine: HIGH by the rule.

cpum88kinstr:F5 | CONFIRMED-NEW HIGH m88kfpr0stop "every FP arithmetic/convert decode with rD = r0 stops the CPU instead of raising the FP unimplemented-opcode exception"
Checked: the eight `if (d == 0) { fatal(...); goto bad; }` sites cpu_m88k_instr.c:3201-3205 (fmul), :3226-3230 (flt), :3245-3249 (fadd), :3270-3274 (fsub), :3295-3299 (fcmp), :3317-3320 (int/nint, #302 -- the finding's site), :3337-3341 (trnc), :3356-3360 (fdiv); cpu_dyntrans.c:2014.  Manual :3523-3525: "If general-purpose register r0 is specified as the destination register for ANY floating-point instruction except fstcr, fldcr, and fxcr, the MC88100 takes a floating-point unimplemented opcode exception"; :5189-5191 and :5676-5678 repeat it for int/nint.  The draft's `m88kconvr0` scoped two of eight sites; the check's (b) asked for the widening and the source supports it.  Delivering the exception depends on `m88kexcsfu1` (SFU1 delivery halts today), which the row must say.  Unfiled.

cpum88kinstr:F6 | CONFIRMED-FILED OUTSTANDING_BUGS.md:1549-1558 (prose, no id) -- proposed id m88kconvdelivery
Checked: cpu_m88k_instr.c:2063-2101 (`m88k_toint_result`: NaN -> 0x7fffffff at :2067-2068; |fl| >= 2^31 saturates at :2097-2100; everything else is stored directly) and the five stores :2118, :2134, :2161, :2177, :2191; manual :10335-10343 (exponent >= 30 -> conversion-overflow exception, handler completes) and :10319-10322 (nothing written to the GPRs).  The entry at :1549-1558 (identical at HEAD) says in its own words "the MC88100 traps on every special and writes nothing; the manual's trap window even catches in-range [2^30, 2^31)" -- a RESOLVED block that discloses the contract, which under the batch-2a rule is a filing without an id.  MED (guest handlers and FPECR/FIOV state never engage).

cpum88kinstr:F7 | CONFIRMED-NEW MED m88kpairpadding "a double result into rD = r31 writes r[32], which later double-source reads return as the pair's low word (hardware ignores the write and reads r0)"
Checked: cpu_m88k.h:253 (`r[N_M88K_REGS+1]`, i.e. r[0..32]) and :249-251 ("plus one which is always zero"); the SEVENTEEN writers `reg(ic->arg[0] + 4) = ...` at cpu_m88k_instr.c:983, :1009, :1035, :1062, :1136, :1162, :1188, :1215, :1261, :1287, :1313, :1340, :1401, :1434, :1468, :1843 (the finding's fdiv.dds) and :2002 -- the decoder rejects an odd rD only for flt.ds (:3235), so every other `.d`-destination arm reaches them with d = 31; the readers :1702-1703, :1726, :1756, :1786-1787, :1817 take `reg(arg + 4)` as the low word.  Manual :1632-1635: pair {r31, r0}, "writes to r0 are ignored".  Index 32 is INSIDE the declared array, so this is not the `shoddprfield` shape: MED, numerical.  Astra's 1.0/3.0 example is right by arithmetic (0x3fd5555555555555's low word), not run.  L4 RIDER cpu_m88k.h:246-252 -- replacement: "/*  General-Purpose Registers: 32 (N_M88K_REGS) registers plus one spare element, r[32].  The double-register result arms write it as the low word of a pair that starts at r31 (so the store stays inside the array; st.d with d = r31 reads it), and the double-source arms read it back as that pair's low word.  On the MC88100 the pair is {r31, r0}: the low-word write is ignored and the low word reads as zero -- row m88kpairpadding.  ld.d with d = r31 is converted to just ld.  TODO  */".  Unfiled (greps for `r[32]`, `always zero`, `r31`).

cpum88kinstr:F8 | DUPLICATE-OF-ROW oddoptinyband
Checked: cpu_m88k_instr.c:1806-1808 (fdiv.sdd stores through `ieee_div_round_to_odd`), float_emul.c:824 (`IEEE_DIR_OPTINY 0x1p-969`) and :999-1000 (`fabs(a) < OPTINY` returns the host nearest quotient unforced); the finding's operands carry exponent field 0x017, i.e. 2^-1000 < 2^-969, so the early return fires and the 24-bit midpoint double-rounds to 0x3f800000 where one rounding gives 0x3f800001 (manual :2367-2372).  DISPOSITIONS.md:203-205 is this exact defect ("the #308 witness scaled by 2^-1000"); the related directed-mode prose is OUTSTANDING_BUGS.md:1971-1973.  Adds nothing the row lacks.

cpum88kinstr:F9 | DUPLICATE-OF-ROW divbyinfnan
Checked: cpu_m88k_instr.c:1745-1747 and float_emul.c:987-1008 traced for {-1, +Inf}: q = -0 is finite, |a| = 1 >= 2^-969, r = fma(-0, +Inf, 1) is NaN, `(r > 0.0) == (a > 0.0)` is true, `ieee_force_odd` steps the even -0 pattern DOWN to 0x7fffffffffffffff (:842-849, :919-928), which :511-515 stores as 0x7fffffff.  DISPOSITIONS.md:27-30 and :231-234 already carry the defect, the |dividend| >= 2^-969 qualifier and the round-to-odd callers (fdiv.ssd/sds/sdd).  Adds nothing.

cpum88kinstr:F10 | DUPLICATE-OF-ROW m88ksddovf
Checked: cpu_m88k_instr.c:1715-1717 (fmul.sdd) with float_emul.c:972-976 (`!isfinite(p) -> return p`: the host product 2^1023 * 2 is already +Inf) and :505-510 (stored as 0x7f800000 in every mode); manual :2491-2497 (round-to-zero overflow owes the largest finite value), :2336-2342 (sticky).  DISPOSITIONS.md:31-33 and :235-238 carry both the overflow and the underflow sides with Astra's corrected boundaries.  Adds nothing.

cpum88kinstr:F11 | DUPLICATE cpum88k:F1
Checked: cpu_m88k_instr.c:2513-2529 (tcnd: a supervisor may name any vector; `m88k_exception(cpu, ic->arg[2], 1)`), :2550-2551 and :2563-2564 (tb0/tb1, same call), reaching cpu_m88k.c:799-807.  Same fallback, same two filed ids (`m88kexctaildefault`, `m88kexcsfu1`).  HIGH.

cpum88kinstr:F12 | CONFIRMED-FILED m88kexchwtraps
Checked: cpu_m88k.c:881-921 -- a software trap naming 0 reaches `case M88K_EXCEPTION_RESET` (:885-889, every CPU stopped; RESET is `implemented` at :698-700 so it passes the fallback), 1 rewinds SNIP/SFIP (:894-895), 2 clears them (:902-905) AND, the check's (b) verified, gets SXIP_E set at :859-860, 3 imports the DMT shadows (:910-918); the `is_trap` flag is never consulted in the tail; manual :9282-9288.  OUTSTANDING_BUGS.md:365-368 records it (LOW); HIGH for the vector-0 half by the rule, supervisor-only.  L4 RIDER, CHANGELOG.md:23018-23020 at 8ea26abb (= :23102-23104 at HEAD) -- "the trap was delivered correctly and the machine reset" is false of the code (no handler ran; the emulation stopped) -- replacement: "The vector is 128 or above on purpose.  The first version of the probe used vector 0, which `m88k_exception()`'s tail treats as the hardware RESET event and answers by stopping every CPU (`case M88K_EXCEPTION_RESET`); the MC88100 would run the handler at VBR+0 like any other software trap -- the `m88kexchwtraps` defect -- so the row read an emulator stop as a failure."

cpum88kinstr:F13 | DUPLICATE cpum88k:F3
Checked: cpu_m88k_instr.c:2529 enters cpu_m88k.c:811-821 with `is_trap`, and :870-879 zeroes DMT/DMD/DMA regardless.  Same defect, `m88kexcfrozendmt`.  MED.

cpum88kinstr:F14 | DUPLICATE cpum88k:F2
Checked: cpu_m88k_instr.c:2739-2752 -- the folded slot runs with `pc` at the bcnd and `delay_slot = TO_BE_DELAYED`, so a precise fault in ic[3] enters the same else-arm at cpu_m88k.c:849-853; the fold mirrors the generated protocol (tmp_m88k_bcnd.c:319-321), which settles equivalence with the generator, not with the manual.  Same defect, `m88kdslotshadow`.  MED.

cpum88kinstr:F15 | CONFIRMED-FILED OUTSTANDING_BUGS.md:4675-4682 (prose, no id) -- proposed id m88kidleslotsem
Checked: the matcher at cpu_m88k_instr.c:2926-2934 constrains ic[-2], ic[-1] and ic[0] and says nothing about the slot ic[1]; X(idle_with_tb1_n) reads `v` at :2726, runs the slot at :2744, then decides `wants_to_idle` from the PRE-slot `v` at :2755-2765; manual :4113-4114.  The entry at :4676-4680 says precisely this ("a polled-word-writing slot still arms one idle sleep decided from the PRE-slot value").  QUALIFIER (the check's, verified): "many iterations are credited" is wrong as INSTRUCTION accounting -- :2764 adds N_DYNTRANS_IDLE_BREAK and cpu_dyntrans.c:376-377 subtracts it; what the fold credits is TIME (one host sleep per fold entry, with pc left at the loop head via `next_ic = &nothing_call`, :2765), so an accumulating slot runs once per sleep instead of once per iteration, and progress is delayed by one sleep, not lost.  MED.

cpum88kinstr:F16 | DUPLICATE include2:F6 (batch 1b, RECORD-L4; DISPOSITIONS.md:54)
Checked: CHANGELOG.md:22086-22091 at 8ea26abb (= :22170-22175 at HEAD) still says "a decode that FORGETS the swap passes every sign-symmetric test"; regress/m88k_rounding_probe.py:68-69 are single-sign rows that already want opposite answers (0x3f800001 vs 0x3f800000), and the record's own mutant line :22121-22124 says the missing-swap mutant reds "the three direction-pinned symmetric rows".  The replacement text is already written at adjudication/fable_batch1b.md:74 and ratified; this finding adds nothing to it, and its "the source comment was corrected" is right (cpu_m88k_instr.c:899-904 states the two defences correctly).

cpum88kinstr:F17 | RECORD-L4 "HISTORICAL (#298), FIXED by #299: these arms once computed in host double before the store, so a residue finer than 2^-53 collapsed before a directed mode could see it -- hardware's sticky bit (MC88100UM: the OR of ALL infinitely-precise result bits) rounds 1.0 + 2^-60 UP under toward-+Inf, and this model stored 1.0.  fadd.sss, fsub.sss, fsub.sds and the mixed-width single-destination add/sub arms (#306) now route through ieee_sum_round_to_odd() before the modal single store (float_emul.c), and gate 11's `fadd band toward+Inf` row pins 0x3f800001.  fmul's product was always exact in double and a nonzero fdiv residue always survives; RN and RZ were never affected."
Checked: cpu_m88k_instr.c:906-914 (present tense: "where this model stores 1.0", "the remedy is ... the next round") against :951-956, :1082-1085, :1107-1110 and the five #306 sites at :1547-:1645 (all through `ieee_sum_round_to_odd`), float_emul.c:1209-1254, and regress/m88k_rounding_probe.py:101-106 (`fadd band toward+Inf` wants 0x3f800001 and says the band is "FIXED by #299").  LOW.  Replaces :906-914 whole.

cpum88kinstr:F18 | DUPLICATE cpum88k:F5
Checked: the same three artifacts (cpu_m88k_instr.c:2743-2744, regress/m88k_idle_probe.py:68, regress/gate_m88k_rounding.sh:212-214); `m88kidledup` exists at HEAD (OUTSTANDING_BUGS.md:15552-15554).  LOW.

generatem88kbcnd:F1 | CONFIRMED-NEW HIGH m88kbcndnest "a delayed branch entered as another delayed branch's delay slot: unbounded host recursion, and a dispatch pointer walked off its object"
Checked: generate_m88k_bcnd.c:164-179 emits `ic[1].f(cpu, ic+1)` BEFORE `n_translated_instrs ++` and before any check of `cpu->delay_slot` on entry (tmp_m88k_bcnd.c:319-330 is the emitted form); the decoder at cpu_m88k_instr.c:3467-3485 installs the handler with no nesting test; the hand-written br.n (:92-106), bsr.n (:115-130), jmp.n (:321-334) and the bb0/bb1 .n arms (:150, :198, :237) share the protocol, so the class is EVERY delayed branch, not only bcnd.n; end_of_page (:2794-2815) carries the chain onto the next page through `to_be_translated`; cpu_dyntrans.c:370-372 bounds only the outer unrolled loop.  Manual :4135-4137 calls the sequence an undetected programming error, which bounds nothing on the host.  BY READING: the host frame count per guest word is small and the guest can supply as many consecutive delayed-branch words as it has memory; the stack-exhaustion threshold was NOT measured.  Unfiled -- OUTSTANDING_BUGS.md:21950-21951 (`excvecrecurse`) is the untranslatable-vector re-entry, a different path; DISPOSITIONS.md's `shnestedbranch` (:208-210) is the SH sibling of the semantic half.  The row carries tmpm88kbcnd:F1's consequence and the two in (b) below.

tmpm88kbcnd:F1 | DUPLICATE generatem88kbcnd:F1
Checked (the mechanism is REAL and is this finding's contribution to `m88kbcndnest`): when the INNER delayed branch's slot fails to decode, cpu_dyntrans.c:2023-2034 sets `next_ic = &nothing_call + 1`, ORs EXCEPTION_IN_DELAY_SLOT (:2029-2030) and runs `nothing`, whose `next_ic --` (tmp_m88k_head.c:60-64) leaves `next_ic == &nothing_call` (the singleton, :66); the inner handler's else-arm (tmp_m88k_bcnd.c:329-330) then CLEARS the flag, so the OUTER handler takes its normal arm and, untaken, does `next_ic ++` (:328); the next `I` (cpu_dyntrans.c:114) dereferences `&nothing_call + 1` -- a read past a one-element static object and a call through whatever follows it.  Three guest words (two delayed branches and an undecodable word) reach it.  Same root cause as the recursion (no delayed branch knows it is a slot), one guard fixes both, so one row; HIGH stands.  Runtime manifestation NOT run.

---

(a) CODE findings I could NOT confirm: none refuted.  Qualifications that change wording, not disposition:
cpum88kinstr:F15's "many iterations are credited" is false as instruction accounting (the idle-break offset is added
at :2764 and subtracted at cpu_dyntrans.c:377) and true only as elapsed guest time; cpum88kinstr:F2 establishes no
observable consequence (LOW, not a defect with an effect); generatem88kbcnd:F1 and tmpm88kbcnd:F1 are confirmed by
reading only -- no reproducer was run and no stack threshold measured; cpum88kinstr:F7's 1/3 bit pattern was derived,
not run; cpum88kinstr:F3's claim about what the GUEST then sees (kernel completion or SIGFPE) is unestablished here.

(b) Findings Astra missed, noticed while checking (mine unless credited):
* `m88kpsrbokill` NEW HIGH (raised by the draft check's section (b); verified here, absent from the draft): a
  supervisor `stcr` (or `rte`) writing PSR with the BO bit flipped relative to the machine's byte order reaches
  cpu_m88k.c:522-532 (`cpu->running = false`), and X(stcr) at cpu_m88k_instr.c:843-847 aborts; manual :2001-2006
  (BO "is set by an stcr or xcr instruction").  OUTSTANDING_BUGS.md:374-375's `m88kmxmkill` names the MXM bit of the
  same function only; greps for `endianness`, `PSR_BO`, `byte order` + m88k find nothing.  Supervisor-only; batch 2a's
  `armendianexit` is the ARM precedent at HIGH.  Smallest witness: supervisor `stcr` of PSR with BO toggled on
  testm88k, cold.
* `m88kexchwtraps` rider (the check's, verified): a software trap naming vector 2 also sets SXIP_E at
  cpu_m88k.c:859-860, which the row's text does not list.
* `m88kbcndnest` riders, by reading, unmeasured: (i) with an inner delayed branch TAKEN and three or more untaken
  outer ones, each outer `next_ic ++` (tmp_m88k_bcnd.c:328) advances from the target page's entry past
  `ics[ENTRIES+1]` (cpu.h:81 declares `ics[ENTRIES+2]`) -- the same walk as tmpm88kbcnd:F1 on a different object;
  (ii) an exception raised IN the inner slot is abandoned: m88k_exception sets EXCEPTION_IN_DELAY_SLOT
  (cpu_m88k.c:865-866), the inner handler clears it (:329-330), and a TAKEN outer then overwrites pc with its own
  delay_target (:324-326), so the handler at VBR never runs.
* L4 riders already placed above: cpu_m88k_instr.c:734-736 (under `m88knegdiv`), cpu_m88k.h:246-252 (under
  `m88kpairpadding`), CHANGELOG.md:23018-23020 (under `m88kexchwtraps`).  One more, LOW, under the existing
  `divbyinfnan` (which already carries L4 riders): cpu_m88k_instr.c:1836-1838 says fdiv.dds's quotient is "rounded
  once, correctly"; through `ieee_div_round_rm` (float_emul.c:880-902) that holds for finite divisors with
  |dividend| >= 2^-969 and fails in the row's infinite-divisor shape under the directed modes.
* Scope widenings recorded in the lines above: `m88kfpr0stop` (8 sites), `m88kconvodd` (+ flt.ds :3235-3238),
  `m88kpairpadding` (17 writers), `m88ktrapmask` (+ the :513 rotate site).

(c) DENOMINATOR: 25 of 25 findings checked against the source at `8ea26abb` (every cited src/, regress/ and
CHANGELOG line opened; the manual opened at the cited lines for the 19 findings that rest on one; OUTSTANDING_BUGS.md
read at both commits for every id and every prose claim; DISPOSITIONS.md read whole); 0 ruled from Astra's text
alone.  Not run: anything -- generatem88kbcnd:F1, tmpm88kbcnd:F1 and the (b) riders are readings, and the two float
helper traces (F9, F10) and the 1/3 bit pattern (F7) are arithmetic, not measurements.  MC88110 behaviour not
considered (the manual on disk is the MC88100's).
