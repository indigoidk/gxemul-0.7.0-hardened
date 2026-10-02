VERDICT: 10 confirmed-new, 5 confirmed-filed, 12 record-L4, 3 test-gap, 0 refuted, 0 unsettled, 4 duplicate, of 34 findings

FABLE_RETRO_2b_ALIVE_0926

CHECKPOINT.md first line, verbatim:
`# CHECKPOINT -- 2026-09-26 09:35 (087a90 sections rewritten; the peer's sections below are untouched)`

ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 2b. HEAD `8ea26abb` (verified: `git log -1`). Every
disposition below was checked against `git show HEAD:<path>` (extracted to a scratch dir, never the
working tree), the cited manuals under `_scratchpad/`, the cited probes at HEAD, and
`OUTSTANDING_BUGS.md` (OB) / `CHANGELOG.md` (CL) at HEAD. No build, no run: every CODE confirmation
is a static trace of the committed source, and every arithmetic claim Astra made was re-derived by
hand before being credited. Late-dissent rule applied: closure changes the licence, never the
truth-value. `OB:n` / `CL:n` are line numbers at HEAD.

Three findings recur across the three jobs because they live in ONE shared helper file; they are
ruled once under `floatemul` and marked DUPLICATE elsewhere:
  * finite / +-Inf under a directed mode ........ floatemul:F1 (cpushinstr:F2, cpumipscoproc:F1)
  * the 2^-969 accepted-nearest band ............. floatemul:F4 (cpushinstr:F7, cpumipscoproc:F7)

================================================================================
JOB floatemul (src/core/float_emul.c) -- 11 findings
================================================================================

floatemul:F1 | CONFIRMED-NEW MED divinfnan "finite / +-Inf under a directed mode, or via the round-to-odd divider in ANY mode, steps the signed zero into a NaN or +-2^-1074"
  Traced at float_emul.c:880-902. For a=-1.0, b=+Inf, rm=RZ: q=-0.0 is FINITE so the `!isfinite(q)`
  guard at :887 does not fire (it tests the quotient only; the operands are never tested);
  |a| >= OPTINY; `r = fma(-0.0, +Inf, 1.0)` = NaN; `NaN == 0.0` is false; overshoot =
  `(NaN > 0.0) == (a > 0.0)` = `false == false` = TRUE; ieee_dir_adjust(-0.0, 1, RZ) ->
  ieee_dir_step(-0.0, toward_zero) decrements 0x8000000000000000 to 0x7fffffffffffffff = NaN.
  The garbage overshoot flag is `(a <= 0)`, so the full table for finite a / +-Inf is: RZ: a<0 -> NaN;
  RP: (a>0,+Inf) -> +2^-1074 [step up from +0, owed +0], (a<0,+Inf) -> NaN; RM: (a>0,-Inf) -> -2^-1074,
  (a<0,-Inf) -> NaN. The other half of each mode's four sign cases is correct by accident.
  The sibling ieee_div_round_to_odd() at :987-1008 has the same hole and NO mode: a<0 -> NaN in every
  mode INCLUDING nearest, a>0 -> +-2^-1074 (masked by the S store except under RP/RM: 0x00000001 /
  0x80000001). Callers at HEAD: cpu_m88k_instr.c:1745/1775/1806 (fdiv_ss?/sd?, all modes -- OpenBSD
  userland runs RN, so `fdiv.sss -1.0, +Inf` stores 0x7fffffff where hardware stores 0x80000000: the
  most reachable member), :1398/1431/1465/1840 (fdiv .d?? directed), cpu_mips_coproc.c:1357 (div.d),
  cpu_ppc_instr.c:2239 (fdiv), cpu_sh_instr.c:3504 (PR=1 fdiv; the PR=0 arm at :3526 is plain C
  division and is correct). Manuals: sh4_programming.txt:11061-11069 (FDIV n / +-Inf: `zero(n, sign^sign)`
  unless n is DENORM/Inf), mips-iv.txt:1467 ("arithmetic on Inf is regarded as exact"),
  ppc_uisa_book1_v201.txt:5118. OB grep for div/infinity/finite-by-Inf: nothing. NEW.
  RECORD consequence, to land with the fix (the fix makes both sentences true again, so they are
  carried in the row rather than corrected twice): float_emul.c:802-803 "non-finite OPERANDS or results
  pass through UNTOUCHED ... every entry checks isfinite first" and CL:22350-22352 "Non-finite operands
  and results pass through untouched" are false at HEAD -- only the RESULT is tested, in all five
  helpers; mul/add/sqrt survive because an infinite operand gives an infinite result there, and only
  division can turn an infinite operand into a finite result.
  Astra's F1 gave the NaN shape; the +-2^-1074 shape and the nearest-mode m88k reach are additions of
  this check (see (b)).

floatemul:F2 | CONFIRMED-NEW MED sddexprange "m88k S-destination helpers lose the exponent range in their double intermediate: exact |result| >= 2^1024 stores Inf under RZ/RM+/RP-, and a product below 2^-1074 stores 0 under RP/RM-"
  ieee_mul_round_to_odd(DBL_MAX, 2.0): p=+Inf, `!isfinite(p)` -> return +Inf (:975-976); the S store's
  FP_INFINITE arm (:505-510) emits 0x7f800000 in every mode -- its mode-aware overflow arm (:614-635)
  is only reached from FP_NORMAL, i.e. when the double intermediate was still finite. MC88100
  (mc88100.txt:2541-2542): "the properly signed largest finite number or infinity, depending on the
  rounding mode"; :2387-2388 RZ performs no rounding -> 0x7f7fffff owed. Reachable: X(fmul_sdd)
  cpu_m88k_instr.c:1715, X(fdiv_sdd) :1806, X(fadd_sdd) :1596 take two full doubles. Underflow side:
  fmul.sdd(2^-1000, 2^-1000): p = 0.0 (host underflow), r = fma(a,b,-0) also underflows to 0 -> return
  +0 -> FP_ZERO -> +0 under RP, where 2^-2000 > 0 owes 0x00000001. Band is narrow (|exact| >= 2^1024
  or < 2^-1074) but the sdd/sds/ssd forms accept any double. OB grep sdd/DBL_MAX/"double
  intermediate": nothing. NEW.

floatemul:F3 | CONFIRMED-NEW MED oddoptinyband "the OPTINY guard copied into ieee_div_round_to_odd() suppresses the odd-force for normal operands below 2^-969 and breaks NEAREST single rounding on m88k fdiv.sdd"
  Re-derived Astra's witness. a=0x0170000020000000=(1+2^-23)*2^-1000, b=0x017000000ffffff0=
  (1+2^-24-2^-48)*2^-1000: (1+2^-24)*b = (1+2^-23-2^-72)*2^-1000, so a/b = (1+2^-24) + 2^-72/b', which
  the host rounds to EXACTLY 1+2^-24 (the S midpoint). Exact residual q*b-a = -2^-1072 -- REPRESENTABLE
  (>= 2^-1074), so the fma would resolve it and force q odd (0x3FF0000010000001), and the S store would
  then round UP to 0x3f800001 as owed. But `fabs(a) < IEEE_DIR_OPTINY` at :999 returns q unforced, the
  store sees an exact tie, ties-to-even gives 0x3f800000. Reachable via X(fdiv_sdd) cpu_m88k_instr.c:1806
  under RN (the default). This is the ORIGINAL #308 witness (float_emul.c:948-950,
  regress/m88k_rounding_probe.py:270-271) scaled by 2^-1000, and it is not covered by the OB:1971
  disclosure, which describes #300's DIRECTED-mode bands, not a nearest-mode consequence in #308's
  helper. mc88100.txt:4798-4800 (IEEE 754 division). NEW. See (b) for why the guard is never
  load-bearing.

floatemul:F4 | CONFIRMED-FILED optinyband (proposed name -- the entry exists at OB:1971-1973 as "#300's accepted-nearest bands", under "Known and deliberately not forced", and carries NO short id; assign one)
  float_emul.c:895-896 `if (fabs(a) < IEEE_DIR_OPTINY) return q;` with IEEE_DIR_OPTINY = 0x1p-969 (:824);
  siblings :1027 (mul, on the product) and :1045 (sqrt). 2^-1000/3 under RP: a < 2^-969 -> nearest
  returned; ppc_uisa_book1_v201.txt:5300-5304 requires Z1 (upward). OB:1971 files exactly this class
  ("real divergences from IEEE, pinned as named gate vectors ... Closing them needs scaled residuals").
  Exists at HEAD, id-less. Astra's "already filed, no separate ID" is correct.

floatemul:F5 | CONFIRMED-NEW MED addovftie "ieee_add_round_rm() returns the nearest sum when 2Sum's intermediate overflows: RZ at the overflow tie stores 0xffeffffffffffffe where 0xffeffffffffffffd is owed (single-point family, disclosed in code but not filed)"
  Re-derived: -DBL_MAX + 3*2^970 = -(2^54-5)*2^970 = -(2^53-2.5)*2^971, an exact tie; nearest-even =
  -(2^53-2)*2^971 = 0xffeffffffffffffe; RZ (smaller magnitude, ppc_uisa:5300-5301) = -(2^53-3)*2^971 =
  0xffeffffffffffffd. In the helper `bb = s - a` = -(2^53-0.5)*2^971 rounds to -2^1024 = -Inf, e = NaN,
  `!isfinite(e)` at :1068 returns s (nearest). The exclusion is disclosed at :1069-1077 and CL:22347-22348
  ("the single overflow-tie exclusion") and pinned by regress/diff_ieee_store.c:898-899 `D add ovf-tie RZ`
  want 0xffeffffffffffffe -- i.e. the gate row PINS THE DEVIATION and its comment (:887-889) says only
  that the family "anti-corrected under toward-minus-Inf before its guard existed"; the RM row (:896-897)
  happens to pin the architecturally correct answer because RM and nearest-even coincide there. OB grep
  ovf-tie/2Sum/3*2^970: nothing. NEW. When fixed, the RZ row flips: oracle-correction rule applies
  (re-pin first, measure the committed build red, then change the code).

floatemul:F6 | RECORD-L4 "W's upper bound is `nf >= 2147483648.0`, so the open interval (2147483647.0, 2^31) is NOT rejected: it reaches the cast, which truncates it to 0x7fffffff -- the same word the rejection arm returns. There is no slack and the two paths are indistinguishable unless FCSR Invalid signalling is ever added. (Under RN, #294 rounds values >= 2147483647.5 to 2^31 first, and those do take the rejection arm.)"
  CL:20471 says "W's *upper* bound has deliberate slack (it rejects the open interval between
  2147483647.0 and 2^31 ...)". float_emul.c:481-485: `nf >= 2147483648.0` -> 0x7fffffff, else
  `(int64_t) nf`; 2147483647.5 under RZ/LEGACY (ieee_round_to_integral is a no-op, :314-315) is cast to
  2147483647. Result correct, sentence false. Land as an appended dated correction to CL:20471 (the
  project corrects CHANGELOG by quoting what it refutes).

floatemul:F7 | RECORD-L4 "SH-4's FPSCR.DN (denormals-as-zero, set at reset) was NOT modelled when this was written. #334 added sh_dn() in cpu_sh_instr.c, applied to every FP RESULT store: DN=1 flushes a subnormal result to a signed zero, DN=0 passes the gradual-underflow result through -- which is what the manual specifies for results (sh4_programming.txt:5286-5289). The OPERAND side is still unmodelled: this decode always yields the true value, where silicon with DN=1 treats a denormalized input as zero (:999) and with DN=0 raises the FPU error (:5238) -- filed as `shdnoperand`."
  float_emul.c:217-225 says DN "stays NOT modelled" and "subnormal RESULTS still flush (#287/#292 store
  policy)". HEAD cpu_sh_instr.c:175-193 sh_dn() reads SH_FPSCR_DN_ZERO at :182 and flushes only when
  DN=1. Stale since #334 (CL:32604-32610). Replaces :217-225 from "SH-4's FPSCR.DN" to "so nobody fixes
  half of it."

floatemul:F8 | RECORD-L4 "\"SH FPSCR.DN flushes in hardware\" is true only for DN=1 -- with DN=0 the SH-4 DELIVERS the denormalized result (sh4_programming.txt:5286-5287); its FPU error is raised for a denormalized INPUT (:5238), never for a result -- and SH_FPSCR_DN_ZERO was never read by anything at all."
  float_emul.c:652-654 "(DN=0 raises an FPU error)". Manual :5285-5287: "Underflow (U): When FPSCR.DN =
  0, a denormalized number with the same sign as the unrounded value, or zero with the same sign as the
  unrounded value, is generated." :5238: "FPU error (E): When FPSCR.DN = 0 and a denormalized number is
  input". Already the carrier's own finding: OB:8153-8161 (`shsweep` item 4) names both this site and
  cpu_sh_instr.c:150-151 and rules "the code is right and the justification is wrong". Filed, not yet
  corrected in place; the L4 is owed regardless (rule 1 has no filed-exemption).

floatemul:F9 | RECORD-L4 ":789 'below 2^-1018' -> 'below 2^-969 (IEEE_DIR_OPTINY; the 2^-1018 figure was the first repair's TYPICAL-MAGNITUDE bound, corrected to the residual's QUANTUM bound by the second panel pass -- see the note below this contract)'; :1024-1026 'the accepted-nearest band for mul is the result below the same 2^-1018 threshold' -> 'the accepted-nearest band for mul is the product below the same 2^-969 threshold (IEEE_DIR_OPTINY)'"
  float_emul.c:789 and :1026 say 2^-1018; :824 `#define IEEE_DIR_OPTINY 0x1p-969`; :806-823 explains the
  correction. Two sentences in one file contradict the constant they describe; the third (:820-823) is
  right.

floatemul:F10 | RECORD-L4 "For finite s, s == 0 with e != 0 is impossible for ANY two doubles, not only for the single-derived operands the first callers passed: both operands are multiples of 2^-1074, so a sum whose magnitude is below 2^-1022 is exactly representable on the subnormal grid, and s rounds to zero only when the exact sum IS zero -- in which case e is zero too. (An earlier version of this note rested on a 2^-298 quantum floor for single-derived operands; the m88k .sdd forms -- fadd_sdd, fsub_sdd -- pass two arbitrary doubles here, so that floor does not hold and the argument above is the one that does.)"
  float_emul.c:1224-1228 claims "every operand is a single (or an exact 48-bit product, or sds's double)
  ... a seat proved the 2^-298 quantum floor". cpu_m88k_instr.c:1592-1597 X(fadd_sdd) and :1645
  X(fsub_sdd) interpret BOTH operands as IEEE_FMT_D and call ieee_sum_round_to_odd. Premise false,
  conclusion (s==0 => e==0) still holds by the subnormal-grid argument; Astra was right to say it
  establishes no wrong guest result. Replaces :1224-1228 from "For finite s from these call sites".

floatemul:F11 | TEST-GAP-FILE badfmtlatchrow
  #279's two one-shot latches (float_emul.c:69-70, :99-103, :442-446) have no committed row that fires
  them and counts exactly one line each. Checked at HEAD: regress/diff_ieee_store.c:82-85 stubs fatal()
  to nothing (deliberately, :78-81); `git grep` over regress/*.py|*.sh|*.c for badfmt/"unimplemented
  format"/add.ps/abs.ps finds only the gate-6 hygiene count in battery LOGS ("unimplemented format 0"),
  which asserts ABSENCE on a healthy boot and never exercises the latch; CL:20514's "Probe: 22/22" was a
  session probe, not a committed file (no regress script mentions #279). Gap confirmed.

================================================================================
JOB cpushinstr (src/cpus/cpu_sh_instr.c) -- 12 findings
================================================================================

cpushinstr:F1 | CONFIRMED-NEW LOW shoddprfield "PR=1 arithmetic/compare/conversion handlers accept an odd register field and read/write fr[n+1]; field 15 lands on xf[0] -- the #316 parity guard was applied to fneg/fabs only"
  Decoder :4954-4981 and :5029-5068 set arg[0]/arg[1] = &fr[r4]/&fr[r8] for ANY 0..15; the PR=1 arms
  read `reg(ic->arg[0] + sizeof(uint32_t))` (fadd :3376, fsub :3416, fmul :3452, fdiv :3490, fcmp/eq
  :3564, fcmp/gt, fsqrt :3254, fcnvds :3071, float :2929 (writes), fcnvsd :3062 (writes)) with no parity
  check; the only guards are fneg :3199-3200 and fabs :3227-3228 (#316) plus the FMOV pair redirects
  :1580-1582/:2902-2907 (which are ARCHITECTURAL XD semantics for FMOV, not a guard). cpu_sh.h:86,104-105:
  `fr[16]` is immediately followed by `xf[16]`, so fr[16] is xf[0] -- an out-of-ARRAY index that stays
  inside the cpu struct; no host-memory hazard (CL:19870's own words: "stays within the FP register
  union -- not a host OOB"). sh4_programming.txt:10424 gives the PR=1 encoding as `1111nnn0mmm00000`
  (even fields only); an odd field under PR=1 is a reserved combination whose hardware behaviour is
  "not guaranteed" (:4525-4526), so this is inconsistency with #316's chosen disposition, not a
  documented-behaviour divergence: LOW. OB:1778 files the ftrc member only, id-less ("SH `ftrc` with an
  odd m under PR=1 decodes as an odd `fr[]` pair"); CL:23399-23404 (#316) names no sibling. The new row
  absorbs OB:1778.

cpushinstr:F2 | DUPLICATE floatemul:F1
  cpu_sh_instr.c:3504 `ieee_div_round_rm(op2.f, op1.f, sh_fp_rm(cpu))` (op2 = FRn dividend, op1 = FRm
  divisor), PR=1 only; sh_fp_rm() yields RN or RZ, so on SH the reachable shape is RZ with a negative
  dividend -> NaN. Manual sh4_programming.txt:11069 confirmed (signed zero).

cpushinstr:F3 | CONFIRMED-NEW MED shnestedbranch "a delayed branch in another branch's delay slot is silently re-run as a plain branch; the manual makes it a Slot Illegal Instruction exception (EXPEVT H'1A0)"
  :2241-2248 (and 18 siblings, 19 in all -- `grep -c 'architecturally unpredictable on SH'` = 19,
  :2243..:2754): the inner branch sets EXCEPTION_IN_DELAY_SLOT and returns; the outer branch then skips
  `cpu->pc = target` (:2253-2258) and the inner branch executes again as an ordinary branch. No
  exception. sh4_programming.txt:4541-4549 lists "Decoding of a delayed branch instruction in a delay
  slot" as a Slot Illegal source, :4558-4560: SPC <- the preceding delayed branch's PC, EXPEVT <- H'1A0.
  The "architecturally unpredictable" premise in all 19 comments is false. CL:19869-19872 (#47's round)
  DEFERRED this knowingly ("raising the architectural slot-exception would be a guest-visible behaviour
  change across ~18 hot handlers") -- an honest record, but OB grep for slot illegal/0x1a0/SLOT_INST/
  nested branch finds NO queue row. NEW, MED (guest-visible, contrary to the manual). The fix owes the
  19 comments' correction (L4 folded into the row): "(a Slot Illegal Instruction exception on SH,
  EXPEVT H'1A0 -- sh4_programming.txt:4547; not raised here yet, see `shnestedbranch`)".

cpushinstr:F4 | CONFIRMED-NEW MED shslotres "X(reserved) raises EXPEVT_RES_INST (H'180) in a delay slot; the manual requires the Slot Illegal code H'1A0 for the designated undefined instruction H'FFFD there -- the split #316 already applies four lines away"
  :242-246 `sh_exception(cpu, EXPEVT_RES_INST, 0, 0)` unconditionally; cpu_sh.c:931-934 only sets
  EXCEPTION_IN_DELAY_SLOT and backs pc up, :949 stores the supplied expevt. H'FFFD decodes to
  `reserved`: decoder :5074-5099 -- 0xfffd matches neither FSCA (&0x01ff==0x00fd), FSCHG (0xf3fd), FRCHG
  (0xfbfd), FTRV (&0xf3ff==0xf1fd) nor FMAC (lo4==0xe), so it falls to :5099. Manual :4544-4546 (Slot
  Illegal sources: "Decoding of an undefined instruction in a delay slot ... Undefined instruction:
  H'FFFD"), :4561-4562 (only H'FFFD is guaranteed; other codes "not guaranteed"). #316's fneg/fabs/fsrra
  (:3209-3212, :3234-3237, :3291-3294) and trapa (:2852-2853) all do `delay_slot ? SLOT_INST : RES_INST`;
  CL:23403-23404 calls the distinction "architectural". OB grep: nothing. NEW. Also see (b): the
  upstream RES_INST_IF_NOT_MD macro (:50-55) has the same omission for privileged instructions.

cpushinstr:F5 | CONFIRMED-FILED sh4sqexpevt
  :3706-3716: SQMD check only inside `if (mmucr & AT)`, raises EXPEVT_RES_INST. sh7750_hardware.txt:
  11747-11748 (MMU on: "an address error will be flagged in user mode") and :11750-11755 (MMU off:
  "an address error will be flagged"). OB:7505-7531 `sh4sqexpevt` files the event-code half (exists at
  HEAD); the AT=0 gating is filed in the round-81 audit block at OB:1931-1936 and :1940-1944 ("is only
  consulted when AT=1, though the manual's SQMD rule is not AT-conditioned"), id-less. Both halves on
  record.

cpushinstr:F6 | CONFIRMED-FILED sh4sqwrite
  memory_sh.c:353-357: `vaddr in [0xe0000000,0xe4000000)` -> `*return_paddr = vaddr; return 2;` with
  the TODO "Take SH4_MMUCR_SQMD into account" -- guest stores into the queues take the identity map and
  skip UTLB judgment entirely; :3761 judges only the PREF side (read type, #454).
  sh7750_hardware.txt:11744-11746 ("Write type exception judgment is performed for writes to the SQs").
  OB:7951-7968 `sh4sqwrite` exists at HEAD and quotes the same sentence.

cpushinstr:F7 | DUPLICATE floatemul:F4
  :3460 `ieee_mul_round_rm(op2.f, op1.f, sh_fp_rm(cpu))`, PR=1. Astra's product re-derived: 1.5*2^-509 x
  (1+2^-52)*2^-510 = (1.5 + 2^-52 + 2^-53)*2^-1019; nearest-even carries the exact half-ulp tie up to
  1.5+2^-51 = 0x0048000000000002, RZ truncates to 0x0048000000000001; |p| ~ 2^-1018.4 < 2^-969 so :1027
  returns nearest. Both normal. Same filed band.

cpushinstr:F8 | RECORD-L4 "Double precision is NOT fixed by the store side and cannot be: the D format IS a host double, so the store is a pure re-encode with no narrowing step for a mode to control (see float_emul.c's own note that D has no remainder). #300 therefore corrects the ARITHMETIC instead: the PR=1 fadd/fsub/fmul/fdiv/fsqrt arms call the ieee_*_round_rm() helpers, which recover the directed-mode neighbour from an exact residual. Measured before #300: double 1.0/10.0 gave 0x...9999999a under both modes; the `Ddiv 1.0/10.0 low` row in regress/sh_rounding_probe.py now pins 9a under RN and 99 under RZ."
  :119-125 says "SuperH double arithmetic therefore still inherits the HOST's rounding mode. Measured:
  double 1.0/10.0 gives 0x...9999999a under both modes." HEAD :3504 uses ieee_div_round_rm; probe
  :113-117 expects {RN: 0x9999999a, RZ: 0x99999999}. Stale since #300. Replaces :119-125.

cpushinstr:F9 | RECORD-L4 ":150-151 -> 'With DN=1 the SH-4 writes a signed zero in place of a subnormal ARITHMETIC RESULT; with DN=0 it DELIVERS the gradual-underflow result -- sh4_programming.txt:5286-5287: \"When FPSCR.DN = 0, a denormalized number with the same sign as the unrounded value, or zero with the same sign as the unrounded value, is generated.\" The FPU error (E) is raised for a denormalized INPUT with DN=0 (:5238), never for a result.'  :159-164 -> 'DN=0 delivers the IEEE value here, which is what the manual specifies for results (above). What is NOT modelled is the operand side -- with DN=0 a denormalized INPUT raises the FPU error on silicon, with DN=1 it is treated as zero (:999) -- and this function touches results only; both operand behaviours are open (OUTSTANDING_BUGS `shdnoperand`; the exception model is its own queued round).'  CL:32605-32606 -> append '[Corrected 2026-09-26: the manual (sh4_programming.txt:5286-5289) says DN=1 writes a signed zero and DN=0 DELIVERS the denormalized result; the FPU error is for denormalized inputs (:5238). The DN=0 pass-through is the documented behaviour, not a divergence.]'"
  Three sites carry the false claim: cpu_sh_instr.c:150-151 and :159-164 ("a NAMED divergence"),
  float_emul.c:653 (floatemul:F8), CL:32605-32606. OB:8153-8161 (`shsweep` item 4) already refutes it
  and names the first two sites; the CHANGELOG site is an addition of this check. Filed, uncorrected;
  L4 owed.

cpushinstr:F10 | RECORD-L4 "Measured halting on this rig, among others: MAC.L, STC SGR, STC.L/LDC.L DBR, SYNCO, PREFI, ICBI, MOVLI.L and MOVCO.L. (SLEEP was reported halting by the first, marker-only classifier and is NOT: it has a decoder case and X(sleep) below -- regress/sh_halt_probe.py:33-38 records the retraction.)"
  :238-240 lists SLEEP; decoder :4129-4130 `/* SLEEP */ ic->f = instr(sleep)`; X(sleep) at :252;
  sh_halt_probe.py:36-37 "reported SLEEP as a halt, which is false -- SLEEP has a case and a handler".

cpushinstr:F11 | RECORD-L4 "The UNMASKED operand is what gets translated so that a fault carries the guest's actual address in TEA. The masking order does not otherwise matter: translate_via_mmu passes the in-page bits through (memory_sh.c: `(vaddr & ~mask) | (lo & mask & 0x1fffffff)`), so [9:5] survive whether the operand or the result is masked to the 32-byte block; the composition is translated bits above, the operand's own [9:5], [4:0] zero either way."
  :3726-3733 claims "Translating an already-aligned address instead would silently drop [9:5]". Masking
  to ~0x1f clears [4:0] only; memory_sh.c:165 passes `vaddr & ~mask` (the in-page bits, >= [9:0] for the
  1K minimum page) through untranslated, so [9:5] cannot be dropped. The TEA justification stands; the
  second is false. Replaces :3726-3733.

cpushinstr:F12 | TEST-GAP-FILE ftrvfourstores
  :3170-3173 are four independent `ieee_store_float_value_rm(..., sh_fp_rm(cpu))` stores; the only
  committed row, regress/sh_rounding_probe.py:94-98 `ftrv midpoint`, drives fr0=0x3f800001 and
  xf0=0x3fc00000 with every other xf zero, so frnp1..3 are exactly 0 (mode-insensitive) and only the fr0
  store is observed. A LEGACY revert of any of :3171-3173 alone passes the gate. Records note: CL:21920's
  "each named individually, so a single site reverting cannot hide behind an aggregate count" reads as
  "site = instruction" and is TRUE as written (an ftrv revert at :3170 reds the row); Astra's reading of
  it as "store site" overstates the claim, but the gap itself is real. FILE.

================================================================================
JOB cpumipscoproc (src/cpus/cpu_mips_coproc.c) -- 11 findings
================================================================================

cpumipscoproc:F1 | DUPLICATE floatemul:F1
  :1355-1358 `nf = ieee_div_round_rm(float_value[0].f, float_value[1].f, rm)` for D->D; +-Inf is not
  denormal so the #246 gate at :1293 lets it through; the NaN then reaches #255's canonicaliser and the
  guest reads a quiet NaN where mips-iv.txt:1467 owes -0 (RZ/RP/RM only; RN returns q at :885-886). Also
  CL:22350 wrong record, carried in floatemul:F1.

cpumipscoproc:F2 | CONFIRMED-NEW MED mipscmpdenorm "the #246 denormal-operand E trap fires for C.cond.fmt on R4000; the manual exempts Compare"
  :1293 `if (denormal && op != FPU_OP_MOV && fpu_unimpl_trap(cpu, cp)) return -1;` sits BEFORE the
  `switch (op)` so FPU_OP_C (:1053, called from :1733) is trapped; fpu_unimpl_trap() :1093-1101 returns 1
  on every exc_model but EXC3K, so on R4000 `c.eq.s` of 0x00000001 with itself raises E and leaves the
  condition bit untouched. mips_r4000.txt:1627: "Denormalized operand, except for Compare instruction ...
  NOTE: Denormalized and NaN operands are only trapped if the instruction is a convert or computational
  operation." OB grep c.eq/compare+denormal: nothing. NEW.

cpumipscoproc:F3 | CONFIRMED-FILED mipstiny
  OB:386-406 exists at HEAD, filed as "LOW, unresolved DISAGREEMENT" with an OWED item: "the manual
  sentence itself, quoted with its anchor, by a seat that has not already taken a side". This seat has
  not, and here it is -- mips_r4000.txt:1623: "Tininess can be detected by one of the following methods:
  after rounding (when a nonzero result, computed as though the exponent range were unbounded, would lie
  strictly between +-2^Emin) ... The MIPS architecture requires that tininess be detected after
  rounding." "Unbounded exponent range" is NOT the destination's subnormal grid, which is what
  fpu_subst_tiny() :1147 classifies on (`(mag >> n_frac) != 0`) and what its header :1113-1116 and
  CL:32598-32599 claim IS the MIPS test. Re-derived: 0x1.fffffep-127 = (2^24-1)*2^-150 has exactly 24
  significant bits, is exact at unbounded exponent, and is < 2^-126: TINY, so with FS=1/RN/U,I disabled
  Table 7-1 (:1603) owes +0; the encoder (:663-665, ieee_encode_subnormal) rounds it on the 23-bit
  subnormal grid -- 2^23-0.5 ties to even 2^23 -- to FLT_MIN, which :1147 then passes as normal. The
  discrepancy band under RN is [2^-126-2^-150, 2^-126-2^-151) (above 2^-126-2^-151 the unbounded-exponent
  rounding also gives FLT_MIN and the model is right). The disagreement resolves in the reviewer's
  favour: re-grade the row from "disagreement" to a defect (MED by the severity table; sliver-narrow;
  no OS in the tree sets FS, per the row's own note). Records owed with it -- L4, exact text: :1113-1116
  -> "Classification is done on the ENCODED word, i.e. after rounding onto the destination's SUBNORMAL
  grid. That is NOT the tininess MIPS specifies: mips_r4000.txt:1623 detects tininess after rounding
  'as though the exponent range were unbounded', i.e. to 24 (53) significant bits with no subnormal
  grid. The two differ on [2^-126-2^-150, 2^-126-2^-151) under nearest: 2^-126-2^-150 has exactly 24
  significant bits, is exact at unbounded exponent and is therefore TINY (owes the FS=1 substitution,
  +0 under nearest), while the subnormal encoding rounds it UP to FLT_MIN and this function then leaves
  it alone. Filed as `mipstiny`."; CL:32598-32599 -> append "[Corrected 2026-09-26: the encoded word is
  rounded on the subnormal grid; MIPS (mips_r4000.txt:1623) defines tininess after rounding at
  UNBOUNDED exponent, which differs on [2^-126-2^-150, 2^-126-2^-151). See `mipstiny`.]".

cpumipscoproc:F4 | CONFIRMED-NEW MED mipstinyenable "the #246 tiny-result guard tests FS alone; the R4000 raises E for a tiny result whenever Underflow OR Inexact is ENABLED, FS notwithstanding"
  :1173 `if (!(cp->fcr[MIPS_FPU_FCSR] & MIPS_FPU_FLUSH_BIT) && ...)` -- with FS=1 the whole predicate is
  false and the value is encoded and substituted (:1192-1197) whatever the enable bits say.
  mips_r4000.txt:1623 "Trap Enabled Results: If Underflow or Inexact traps are enabled, or if the FS bit
  is not set, then an Unimplemented exception (E) is generated, and the result register is not
  modified"; :1607 footnote and :1627 ("Denormalized result or Underflow, when either Underflow or
  Inexact Enable bits are set or the FS bit is not set") agree. cvt.s.d(2^-127), FS=1, U enabled: model
  writes +0 (RN), hardware traps E with fd preserved. OB grep FS=1/flush bit: nothing on this. NEW.

cpumipscoproc:F5 | CONFIRMED-FILED mipstinyprerm (proposed name -- the entry exists at OB:1650-1655 "The #246 trap predicate is pre-rounding", under round 72's still-open findings, id-less; assign one)
  :1175 `fabs(nf) < FLT_MIN` tests the unrounded host double; :1117-1121 admits the over-trap. Re-derived:
  2^-126-2^-152 = (2^26-1)*2^-152 rounds at unbounded exponent to 24 bits as 2^24*2^-150 = 2^-126,
  FLT_MIN, not tiny -> store FLT_MIN, no E; the model traps. Astra's boundary correction is right and is
  itself a RECORD-L4 on the filed entry: OB:1651 "(2^-126 - 2^-150, 2^-126)" -> "[2^-126 - 2^-151,
  2^-126) under nearest (the midpoint between the largest 24-bit value below FLT_MIN and FLT_MIN is
  2^-126 - 2^-151, and the tie goes to the even FLT_MIN; the band is mode-dependent -- (2^-126 - 2^-150,
  2^-126) under RP for positive values, empty under RZ)"; and OB:1653 "#332's substitution classifies on
  the encoded word and is correct" -> "#332's substitution classifies on the encoded word, which is NOT
  the manual's unbounded-exponent test -- see `mipstiny`, settled by mips_r4000.txt:1623". Note the two
  bands are complementary: with FS=0 the model is wrong on [2^-126-2^-151, 2^-126) (over-trap, this
  row) and right below it; with FS=1 it is wrong on [2^-126-2^-150, 2^-126-2^-151) (mipstiny) and right
  above it.

cpumipscoproc:F6 | CONFIRMED-NEW MED mipstinyhostzero "a D result the host already rounded to +-0 is classified FP_ZERO and escapes the #246 tiny trap; exact 2^-2044 from mul.d(2^-1022, 2^-1022) stores +0 where FS=0 owes E"
  :1174 `fpclassify(nf) == FP_SUBNORMAL` -- the host computes 2^-1022 * 2^-1022 = 2^-2044 < 2^-1075 and
  rounds it to +0.0, FP_ZERO; ieee_mul_round_rm (RN) returns p unchanged; the store writes +0.
  Table 7-2 footnote (:1607) and :1623: a tiny nonzero result with FS=0 sets E and leaves fd unmodified.
  Class-wide for every D op (add/sub/mul/div/sqrt/cvt) whose exact result is nonzero below the host's
  own underflow threshold; S ops are immune because their double intermediate cannot underflow. OB grep
  2^-2044/FP_ZERO/host-rounded-zero: nothing; distinct from the :1650 pre-rounding entry (which is about
  the S boundary). NEW; fold into one row with F5's entry when that entry gets its id.

cpumipscoproc:F7 | DUPLICATE floatemul:F4
  :1357 div.d, 2^-1000/3 under RP: :895 returns nearest 0x0155555555555555; mips_r4000.txt:6052 "rounded
  ... according to the current rounding mode". Same filed band.

cpumipscoproc:F8 | RECORD-L4 ":716-718 -> '#214: (Codex/Fable) reg 3 is undefined on R3000 but a guest can still mtc0 to it; warn instead of exit()ing the host. The value IS still stored -- this `break` leaves the switch and the common `cp->reg[reg_nr] = tmp` at the tail of this function runs -- but nothing on MMU3K consumes reg 3 (the R3000 TLB write path reads ENTRYLO0 only), so it is visible only to a later mfc0 of reg 3, which is undefined on the real R3000 as well.'  CL:20029 -> append '[Corrected 2026-09-26: warns and no longer exits; the write is still stored in the otherwise-unconsumed reg 3 -- see the source comment.]'"
  :713-721: `break` at :720; no `readonly = 1`, no `return`; :1011-1017 stores `cp->reg[reg_nr] = tmp`.
  MMU3K tlbwi (:2138-2143) reads COP0_ENTRYLO0 only; :2151 reads ENTRYLO1 in the R4000 branch. So the
  record ("warn and ignore") is false and the code is harmless: L4, not CODE. If the round's intent was
  a true ignore, a `readonly = 1` would make the comment true instead -- a code change this adjudication
  does not license.

cpumipscoproc:F9 | RECORD-L4 ":1185-1191 -> '#294: the W and L integer formats honour rm too -- ieee_round_to_integral() rounds the value to an integral under rm before #273's range guards -- and the SEPARATION lives in the decoder, which passes IEEE_RM_RZ for trunc.w/trunc.l (mode-independent by architecture, :1623/:1636) and FPU_RM_FROM_FCSR for cvt.w (:1794), so the two are distinguishable at this call. The D-format STORE cannot change anything: a host double already has exactly the 52 fraction bits D wants, so the remainder is always zero; D rounding is corrected in the arithmetic instead (#300).'"
  :1185-1189 says W/L "ignore the mode inside the store function on purpose -- cvt.w and trunc.w are
  indistinguishable at this call today". float_emul.c:465 `nf = ieee_round_to_integral(nf, rm)`;
  decoder :1623/:1636 pass IEEE_RM_RZ, :1794 FPU_RM_FROM_FCSR. OB:4648-4651 already folds this exact
  comment into "the existing comment-only docs task" (id-less); L4 owed regardless.

cpumipscoproc:F10 | RECORD-L4 ":1302-1303 'Double stays on the plain path: that is the next round's fma-residual work.' -> 'Double goes through ieee_add_round_rm() (#300, the 2Sum residual) in the branch below; only the mixed-format fallthrough stays on the plain path.'"
  :1307-1310 `else if (fmt == COP1_FMT_D && output_fmt == COP1_FMT_D) nf = ieee_add_round_rm(...)`.
  Stale since #300.

cpumipscoproc:F11 | TEST-GAP-FILE mipscvtsdlive
  CL:21404-21407 reports a live pmax+arc `ctc1 RM=0 -> cvt.s.d(1/3) = 0x3eaaaaab, RM=1 -> 0x3eaaaaaa`
  as "PROBE292_PASS". At HEAD no committed regress file drives it: mips_rounding_probe.py is gate 12
  (cvt.d.l / cvt.s.l, #301, rows :45-69); mips_fixedmode_probe.py encodes round/trunc/ceil/floor.w and
  cvt.w.d (:104-110), not cvt.s.d; mips_subnorm_probe.py is #331/#332; gate_mips.sh has no cvt row;
  `git grep 3eaaaaab|PROBE292` over regress/*.py|*.sh|*.c hits only diff_ieee_store.c:506-507 (the
  helper, host-side), m88k_rounding_probe.py and sh_rounding_probe.py:63 (other CPUs). The MIPS store-
  mode WIRING (#292's own "panel's bar") has no committed live observation. FILE.

================================================================================
(a) CODE findings NOT confirmed
================================================================================

None. All 19 CODE findings (7 SH, 7 MIPS, 5 float_emul) were confirmed by static trace of the
committed source, and every numeric witness Astra supplied (SH:F7's product, MIPS:F5's boundary,
float:F3's scaled operands, float:F5's overflow tie) was re-derived by hand and agreed. The
qualification that matters: "confirmed" here means traced at HEAD, not executed -- no binary was built
and no probe was run, per the brief. Four of the seven-plus-seven-plus-five are one defect each in a
shared helper and are ruled once (two DUPLICATE pairs). Severity is mine, not Astra's: SH:F1 is graded
LOW rather than by the letter of "outside a buffer", because the out-of-array index verifiably lands in
the adjacent `xf[0]` field of the same struct and the hardware behaviour for that reserved encoding is
undocumented.

================================================================================
(b) Findings Astra missed, noticed while checking -- MINE, unmeasured
================================================================================

b1. divinfnan is wider than Astra's NaN shape (folded into floatemul:F1's row): the garbage overshoot
    flag is `(a <= 0)`, so under RP a POSITIVE dividend / +Inf steps +0 up to +2^-1074 and under RM
    +finite / -Inf steps -0 to -2^-1074; and the round-to-odd divider has no mode, so on m88k
    fdiv.sss/ssd/sds a negative finite / +-Inf yields a NaN under NEAREST -- the mode OpenBSD/m88k
    userland runs. That member is ordinary-code reachable (`x / INFINITY` clamps) and is the one to row
    first.

b2. shdnoperand (proposed, MED, in scope -- #303 changed this guest-visible value): with FPSCR.DN=1 --
    the reset default, 0x40001 -- the SH-4 treats a denormalized OPERAND as zero
    (sh4_programming.txt:999 "DN = 1: A denormalized number is treated as zero", repeated per
    instruction at :10528, :10713, ...); the fork decodes every operand to its true value (#303) and
    sh_dn() touches RESULTS only (`SH_FPSCR_DN_ZERO` is read at cpu_sh_instr.c:182 and nowhere else).
    So `fmul` of a subnormal by 2^100 is a normal number on the fork and 0 on hardware, in the default
    configuration. float_emul.c:217-225 named the gap in 2026-07 ("one gap, named, so nobody fixes half
    of it"); #334 then fixed the result half, the comment went stale (floatemul:F7), and OB has no row
    for the operand half (grep DN + operand/input/treated: nothing; the #303 resolution at OB:1561-1573
    and `shsweep` are silent). The DN=0 operand side (FPU error on a denormalized input, :5238) is the
    exception model's business and stays with that queued round.

b3. Out of the retro's scope, one line: the upstream macro RES_INST_IF_NOT_MD (cpu_sh_instr.c:50-55,
    byte-identical in 39748e3c:50-55) raises EXPEVT_RES_INST with no delay-slot split, so a privileged
    instruction (LDC/STC/RTE/LDTLB/SLEEP) in user mode in a delay slot delivers H'180 where
    sh4_programming.txt:4550-4552 lists it as a Slot Illegal source (H'1A0). Same one-line fix as
    shslotres; carry it as a rider there rather than as a retro finding.

b4. Design note for optinyband and oddoptinyband, UNMEASURED and offered as a hypothesis for the fix
    round to test against the offline gate before anyone acts on it: the OPTINY guards (:895, :999,
    :1027, :1045) appear never to be load-bearing for correctness. fma() rounds the exact residual once
    and rounding is sign-preserving, so a residual below the subnormal quantum can only read as a FALSE
    ZERO -- which returns the nearest answer, exactly what the guard returns. The guard therefore cannot
    prevent any wrong step; it can only suppress correct steps where the residual IS representable
    (float:F3's 2^-1072, float:F4's 2^-1000/3). If that holds, the true accepted-nearest set is "residual
    rounds to zero", a strict subset of the guarded band, and OB:1971's "needs scaled residuals, not a
    threshold" overstates the cost of closing most of it. The 28+ named gate vectors that pin the band
    would flip.

b5. Out of scope (upstream, untouched), one line: mips_r4000.txt:1607 Table 7-2 and :1627 also make a
    QUIET-NaN operand an E-trap condition for computational ops on the R4000; the fork (and upstream)
    computes through it and #255 canonicalises the NaN result. The visible value after kernel
    completion is the same; the trap is not.

b6. Records, not a finding: Astra's cpushinstr:F12 reads CL:21920's "a single site reverting" as a
    STORE site; the sentence enumerates instructions and is true of them. Filed as a plain test gap.

================================================================================
(c) DENOMINATOR
================================================================================

34 of 34 findings checked against the committed source (`git show HEAD:` of cpu_sh_instr.c,
cpu_mips_coproc.c, float_emul.c, memory_sh.c, cpu_sh.c, cpu_m88k_instr.c, cpu_ppc_instr.c, cpu_sh.h,
OUTSTANDING_BUGS.md, CHANGELOG.md, and the five regress files cited); 0 ruled from Astra's text alone.
Manual lines read for the findings that rest on architecture: sh4_programming.txt:4518-4565, 5220-5245,
5278-5296, 10416-10432, 11040-11076, and :999/:10528 (DN=1); sh7750_hardware.txt:11738-11760;
mips_r4000.txt:1595-1635, 6046-6058; mips-iv.txt:1460-1472; mc88100.txt:2330-2340, 2378-2395,
2538-2546, 4795-4801; ppc_uisa_book1_v201.txt:5115-5120, 5155-5160, 5296-5306. Filed ids verified to
exist at HEAD: sh4sqexpevt (OB:7505), sh4sqwrite (OB:7951), mipstiny (OB:386), shsweep (OB:8078; item 4
at :8153). Proposed ids verified ABSENT from OB at HEAD: divinfnan, sddexprange, oddoptinyband,
optinyband, addovftie, badfmtlatchrow, shoddprfield, shnestedbranch, shslotres, ftrvfourstores,
mipscmpdenorm, mipstinyenable, mipstinyprerm, mipstinyhostzero, mipscvtsdlive, shdnoperand. Upstream
import 39748e3c consulted once (RES_INST_IF_NOT_MD provenance). Nothing built, nothing run, nothing
outside this file written.
