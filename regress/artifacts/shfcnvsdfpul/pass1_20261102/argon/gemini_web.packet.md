# Reading task: pass 1: shfcnvsdfpul (Argon) (Gemini web; 2026-11-02)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBP1SHFCNVSD-67f7` on a line of its own.

# PANEL PASS 1 -- `shfcnvsdfpul`: the SuperH FCNVSD handler overwrites FPUL, a register the instruction only reads

PASS 1, fired 2026-11-02 17:0x.  HEAD at drafting (2026-10-30) and today: `987cb596`, unchanged.  Round number #576.
Roster for this fix (owner ruling 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3, Argon (Gemini web), Grok 4.7.  Packet-fed seats
(glm, Argon): every fact you need is inlined; the artifact paths below are for the file-reading seats and are quoted where they matter.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`, and the older warning about this has changed.**
The pristine-2021 copies this project's template warns about (`./src/` and two under
`_archive/audit-results-*/builds/`) are GONE: `find` for `cpu_sh_instr.c` under the project
root returned none of them today.  **Stray copies do exist, and one is the worse kind:**

    d4512a77 5117  GXEMUL-SEC/src/cpus/cpu_sh_instr.c      <- THE TREE UNDER REVIEW
    d4512a77 5117  est/  build/  build-asan/               the fork's other trees, same bytes
    d4512a77 5117  _scratchpad/diagdiv_20261030/headtree/  same bytes, a scratch copy
    d4512a77 5117  GXEMUL-SEC/regress/artifacts/stateaudit_20260923/.../head_tree/   same bytes
    3f27aefa 5026  GXEMUL-SEC/.claude/worktrees/agent-ae870115d0e5f6f85/   OLDER FORK COPY, 91 lines short

The last one is a nearly-right copy, so a line-number difference from it would be in the tens,
not the hundreds.  Do not read under `.claude/worktrees/`.  If your line numbers disagree with
mine, say so rather than reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**
Walk the values.  A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

**You are a packet-fed seat: everything you need is quoted in this message.**  This round asks for reading only.

## 1. The defect as filed, and the proposed fix

FCNVSD converts the single-precision value in FPUL to double precision and stores it in a
register pair DRn.  This handler also stores a truncated integer back into FPUL.  Any guest
code that uses FPUL after an FCNVSD sees the wrong value, and for NaN, infinity and
out-of-range values the store comes from a C cast whose result is undefined.

**Proposed fix: delete the one line** `cpu->cd.sh.fpul = (int32_t) op1.f;` from
`X(fcnvsd_fpul_drn)`.  Nothing else in product code changes.

Severity filed: MED.  Harm is wrong guest data, not an emulator failure: the handler has no
terminating call and no memory access beyond the FP registers.

**Reproduction: MEASURED 2026-11-02 16:5x, rung 3, on a clone of HEAD `987cb596` built fresh in WSL (`/tmp/gxdivw/gxemul`, binary
newer than its source), machine `-E landisk -M 64` UNMODIFIED, the rig kernel loaded for construction only.**  Script and output are
preserved at `GXEMUL-SEC/regress/artifacts/shfcnvsdfpul/witness_20261102/` (`sh_fcnvsd_witness.py`, `witness_head.out`, `RECEIPT.txt`);
the output, verbatim:

```
row          got        want       role      verdict
fpul 1.5     0x00000001 0x3fc00000 DEFECT    FAILED-FOR-THE-REASON-UNDER-TEST (FPUL holds the truncated integer the handler stores)
fpul -1.5    0xffffffff 0xbfc00000 DEFECT    FAILED-FOR-THE-REASON-UNDER-TEST (FPUL holds the truncated integer the handler stores)
fpul 0.1     0x00000000 0x3dcccccd DEFECT    FAILED-FOR-THE-REASON-UNDER-TEST (FPUL holds the truncated integer the handler stores)
dr hi 1.5    0x3ff80000 0x3ff80000 LIVENESS  ok
dr lo 0.1    0xa0000000 0xa0000000 LIVENESS  ok
fcnvds ctl   0x3fc00000 0x3fc00000 CONTROL   ok
RESULT=3/6
```

Shape: the cold debugger seeds `fpscr` (DN|PR|RN), `fpul`, and the DR2 pair with the sentinel `0xdeadbeef`; the guest executes `fcnvsd
fpul,dr2` (0xf2ad) followed by `sts fpul,r2` (0x025a) and `mov.l r2,@r1` (0x2122) -- or `fmov.s fr2,@r1` / `fmov.s fr3,@r1` for the DRn
halves -- into a sentinel word at 0x8c010100, read back with `dump`.  The three FPUL rows are red with EXACTLY the value section 6
predicts for HEAD (the truncation), so the failure is for the reason under test; the two DRn rows show the conversion itself lands
correctly on HEAD (liveness), and the FCNVDS row shows the FPUL write channel is live where the manual says write (control).  The
same script must read 6/6 on the fixed build; that is clause (i) of the witness rule and is owed before the edit ships.

## 2. PREMISES (C0 OUTPUT AND WHAT IS SETTLED)

C0, run 2026-10-30 at `987cb596` and re-checked 2026-11-02 (HEAD unchanged, `grep -c shfcnvsdfpul CHANGELOG.md` still 0):

    $ git log -1 --format='%h %ad %s' --date=short -- <file>
    src/cpus/cpu_sh_instr.c      3ff21380 2026-08-22 #454 the store-queue PREF transfer is judged READ type, and a gate row pinned the opposite
    src/core/float_emul.c        064caaf6 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it
    regress/sh_rounding_probe.py 1329d894 2026-10-02 #556 hrecord: 154 record corrections placed as 155 notes in the regression harness's comments and do
    regress/gate_sh_rounding.sh  0901b388 2026-10-25 #572 wdclbaaddr: the IDE model decoded the select byte's LBA flag from bit 5 and left both LBA28 add

    $ grep -c shfcnvsdfpul CHANGELOG.md
    0

    $ grep -n shfcnvsdfpul OUTSTANDING_BUGS.md
    24069:#### `shfcnvsdfpul` (MED, an id for an entry this file already carries in prose) -- FCNVSD writes FPUL, which the instruction only reads

    $ ls regress/sh_*
    sh_halt_probe.py  sh_intprio_probe.py  sh_iprbcd_probe.py  sh_pclock_probe.py  sh_rounding_probe.py  sh_tlbmulti_probe.py

**So the round has NOT shipped**: the CHANGELOG does not name the row.  No new tool is proposed.

Settled, each re-read in this function or file today:

* **The line is upstream residue.**  `git log -L3049,3063:src/cpus/cpu_sh_instr.c` returns one commit:
  `39748e3c Import GXemul 0.7.0 (unmodified upstream baseline)`.  The fork never touched the handler.
* **`fatal()` is not involved anywhere in this handler**, and neither is `exit`.
* **`cd.sh.fpul` is `uint32_t`, `fr[]` is `uint32_t[]`** (`src/include/cpu_sh.h`:
  `uint32_t	fpul;		/*  Floating-point Communication Reg  */`).
* **`op1.f` is a `double`** (`struct ieee_float_value { double f; int nan; };`, `float_emul.h`).
* **The deleted line does not feed the DRn result.**  `op1.f` is not assigned between the line and
  the store, so deleting it cannot change the value written to DRn.  Check this by reading section 4.
* **FPSCR resets to DN=1** (the comment above `sh_dn()` says "FPSCR RESETS TO 0x40001").
* **The tree's FP exception model is absent by standing decision.**  `sh_dn()`'s comment calls this
  "a NAMED divergence ... the exception model is its own queued round", and `float_emul.c`'s `#303`
  comment says "SH-4's FPSCR.DN ... stays NOT modelled".  So the manual's `set_E()` and `invalid()`
  branches in section 5 are out of scope here.

**Stated as questions, because I am less sure of them:**

* **The scoping note and the bug file both say the cast is the one `#297` "removed from FTRC".  I do not
  think that is what happened.**  `X(ftrc_frm_fpul)` at HEAD still has `cpu->cd.sh.fpul = (int32_t) op1.f;`
  on both arms.  What `#297` added is a ladder of range checks ahead of each cast, so that the cast is
  only reached with an in-range value.  **Is "guarded" the right word, and does the row's wording owe a
  correction?**
* **Is FPUL really never written by the real instruction?**  The manual's pseudocode in section 5 assigns
  only `DR[n>>1]`, and FCNVSD's `*FPUL` argument is read by `fpul_type` and the assignment.  Read it and
  say whether you agree.
* **Does any guest code depend on the current behaviour?**  I have read no guest source.  A guest reading
  FPUL after an FCNVSD on HEAD gets the truncated integer.  I expect none depends on that, and I have no
  evidence either way.

## 3. THE DECODER, VERBATIM

`GXEMUL-SEC/src/cpus/cpu_sh_instr.c`, anchor `grep -n 'FCNVSD FPUL,DRn' <file>` (`:5061-5068` at HEAD):

```c
		} else if ((iword & 0x01ff) == 0x00ad) {
			/*  FCNVSD FPUL,DRn  */
			ic->f = instr(fcnvsd_fpul_drn);
			ic->arg[0] = (size_t)&cpu->cd.sh.fr[r8];
		} else if ((iword & 0x01ff) == 0x00bd) {
			/*  FCNVDS DRm,FPUL  */
			ic->f = instr(fcnvds_drm_fpul);
			ic->arg[0] = (size_t)&cpu->cd.sh.fr[r8];
```

Bit 8 is required clear, so `r8` is even and the pair `fr[r8]`, `fr[r8+1]` stays in the array.  The
filed row `shoddprfield` records the same: "FCNVSD/FCNVDS are NOT affected."  The decoder does not test
FPSCR.PR.

## 4. THE FULL HANDLER AND ITS SIBLING, VERBATIM

Same file, anchor `grep -n '^X(fcnvsd_fpul_drn)' <file>` (`:3043-3076` at HEAD).  This is both
functions whole, including their header comment.  Neither has a common tail beyond what is shown.

```c
/*
 *  fcnvsd_fpul_drn:  Convert single-precision to double-precision.
 *  fcnvds_drm_fpul:  Convert double-precision to single-precision.
 *
 *  arg[0] = ptr to destination (double- or single-precision float)
 */
X(fcnvsd_fpul_drn)
{
	struct ieee_float_value op1;
	int64_t ieee;

	FLOATING_POINT_AVAILABLE_CHECK;

	ieee_interpret_float_value(cpu->cd.sh.fpul, &op1, IEEE_FMT_S);
	cpu->cd.sh.fpul = (int32_t) op1.f;

	/*  Store double-precision result:  */
	ieee = ieee_store_float_value(op1.f, IEEE_FMT_D);
	reg(ic->arg[0]) = (uint32_t) (ieee >> 32);
	reg(ic->arg[0] + sizeof(uint32_t)) = (uint32_t) ieee;
}
X(fcnvds_drm_fpul)
{
	struct ieee_float_value op1;
	int64_t r1;

	FLOATING_POINT_AVAILABLE_CHECK;

	r1 = reg(ic->arg[0] + sizeof(uint32_t)) +
	    ((uint64_t)reg(ic->arg[0]) << 32);
	ieee_interpret_float_value(r1, &op1, IEEE_FMT_D);

	cpu->cd.sh.fpul = ieee_store_float_value_rm(op1.f, IEEE_FMT_S, sh_fp_rm(cpu));
}
```

The check macro, verbatim, with the only exit path the handler has before the conversion:

```c
#define	FLOATING_POINT_AVAILABLE_CHECK					\
	if (cpu->cd.sh.sr & SH_SR_FD) {					\
		/*  FPU disabled: Cause exception.  */			\
		SYNCH_PC;						\
		if (cpu->delay_slot)					\
			sh_exception(cpu, EXPEVT_FPU_SLOT_DISABLE, 0, 0);\
		else							\
			sh_exception(cpu, EXPEVT_FPU_DISABLE, 0, 0);	\
		return;							\
	}
```

In this file `ieee_store_float_value(v, fmt)` is a macro, `sh_dn(cpu, (ieee_store_float_value)((v),
(fmt)), (fmt))`.  `sh_dn()` flushes only a value that is subnormal IN THE DESTINATION format.  Every
single-precision value, subnormal ones included, is normal as a double.  **So `sh_dn()` never changes an
FCNVSD result** (enumerate this: the smallest single subnormal is 2^-149, and the smallest normal double
is 2^-1022).

What `ieee_interpret_float_value` (`src/core/float_emul.c`) gives for `IEEE_FMT_S`, condensed from my
reading, not verbatim:

* infinity: `f = INFINITY`, then the sign is applied;
* any other all-ones exponent: `f = NAN`, `nan = 1`, and the sign step is JUMPED OVER (`goto
  no_reasonable_result`);
* `x == 0` or `x == 0x80000000`: `f = 0.0`, then the sign is applied, so `-0.0` is produced for `0x80000000`;
* biased exponent 0 with nonzero mantissa: the true subnormal value (`#303`);
* otherwise the normal value.

`ieee_store_float_value_rm` for `IEEE_FMT_D`, verbatim in the two arms that matter, with the sign bit
set first from `signbit(nf)`:

```c
		case FP_INFINITE:
			if (fmt == IEEE_FMT_D)
				r |= 0x7ff0000000000000ULL;
```
```c
		case FP_NAN:
			if (fmt == IEEE_FMT_D)
				r |= 0x7fffffffffffffffULL;
```

**So every NaN FPUL produces one DRn value, with the payload lost.**  I did not read the `FP_ZERO` arm, so
the `-0` DRn prediction in section 6 is a prediction.

## 5. THE MANUALS, VERBATIM

`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\sh4_programming.txt`, Rev. 5.0, section 9.29.  Line numbers from
`awk NR`.  The extraction drops the arrow character in the summary lines.

```
10861: PR Format             Summary of Operation Instruction Code    Execution
10864: 0--                   --                       --              --  --
10866: 1 FCNVSD FPUL, DRn (double) FPUL  DRn 1111nnn010101101 2           --
10870: When FPSCR.PR = 1: This instruction converts the single-precision floating-point number in
10871: FPUL to a double-precision floating-point number, and stores the result in DRn.
10881:      case((FPSCR_PR){
10883:              0: undefined_operation(); /* reserved */
10885:              1: fcnvsd (n, *FPUL); break; /* FCNVSD */
10891: void fcnvsd(int n, float *FPUL)
10895:      case(fpul_type(FPUL)){
10897:              PZERO :
10899:              NZERO :
10901:              PINF :
10903:              NINF :               DR[n>>1] = *FPUL;    break;
10905:              DENORM : set_E();                 break;
10907:              qNaN :               qnan(n);     break;
10909:              sNaN :               invalid(n);          break;
10926:           if((FPSCR_DN == 1) || (abs == 0x00000000)){
10934:           else                   return(DENORM);
10948:    else if(abs < 0x7fc00000) return(qNaN);
10950:    else                       return(sNaN);
10958: FCNVSD(FPUL FRn) +NORM -NORM +0 -0 +INF -INF qNaN Invalid
10960: Note: When DN = 1, the value of a denormalized number is treated as 0.
```

(Line 10958's minus signs are a replacement character in the extraction, shown here as `-`.  That one
substitution aside, these lines are verbatim; blank lines and unquoted lines between them are omitted.)

**Two things a careful reader will notice.**  The `case` list at 10897-10909 has no `NORM` label, while
`fpul_type` returns NORM and the table at 10958 gives `+NORM`.  I read that as a manual omission; it does
not change the point about FPUL.  And the pseudocode at 10948 classes the lower NaNs as qNaN and the upper
as sNaN.

The sibling, section 9.28, for contrast:

```
10754: 1 FCNVDS DRm,FPUL (float)DRm  FPUL  1111mmm010111101 2  --
10758: When FPSCR.PR = 1: This instruction converts the double-precision floating-point number in
10759: DRm to a single-precision floating-point number, and stores the result in FPUL.
10763: an exception has occurred. When an exception occurs, correct exception information is reflected in
10764: FPSCR.cause and FPSCR.flag, and FPUL is not updated. Appropriate processing should therefore
```

An unstaggered table line, `:16935`:
`FCNVSD FPUL,DRn        float_to_ double [FPUL]  DRn 1111nnn010101101 --     --`.
The table at `:6300-6301` is staggered (it prints the FCNVDS operation beside the FCNVSD name), so do not
cite it.

`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\sh7750_hardware.txt` has **no prose description of FCNVSD**.  A grep for
`FCNVSD` gives only instruction lists and timing tables (`:15226`, `:15828`, `:16022`, `:17062`, `:18211`),
and `:15226` has the same stagger.  So this round rests on the programming manual alone.

**A correction to my scoping note:** it quoted `:10870-10871` starting at "This instruction converts",
dropping "When FPSCR.PR = 1:".  The qualifier matters for Q4.

## 6. WHAT HEAD DOES, PER INPUT CLASS (rows 1.5, -1.5 and ~0.1 MEASURED above and matching this table exactly; the rest READ, not run)

| FPUL in | value | FPUL after, HEAD | FPUL after, fixed | DRn (hi lo), both |
|---|---|---|---|---|
| `0x3f800000` | 1.0 | `0x00000001` | unchanged | `3ff00000 00000000` |
| `0x3fc00000` | 1.5 | `0x00000001` | unchanged | `3ff80000 00000000` |
| `0xbfc00000` | -1.5 | `0xffffffff` | unchanged | `bff80000 00000000` |
| `0x3dcccccd` | ~0.1 | `0x00000000` | unchanged | `3fb99999 a0000000` |
| `0x80000000` | -0 | `0x00000000` | unchanged | `80000000 00000000` (prediction) |
| `0x4f000000` | 2^31 | C cast undefined | unchanged | `41e00000 00000000` |
| `0x7f800000` | +Inf | C cast undefined | unchanged | `7ff00000 00000000` |
| `0x7fc00000` | NaN | C cast undefined | unchanged | `7fffffff ffffffff` (a model policy, see below) |
| `0x00000001` | smallest subnormal | `0x00000000` | unchanged | a normal double, see below |
| `0x00000000` | +0 | `0x00000000` | unchanged | `00000000 00000000` |

Arithmetic worth enumerating: `0x3dcccccd` has mantissa `0x4ccccd`.  Shifted left 29 into a 52-bit
fraction with exponent `0x3fb`, that gives `3fb99999 a0000000`, by my hand derivation.  It is the only row
above with a nonzero low word.

**Three things the table implies, each a premise to check:**

1. **+0 is the one input I believe HEAD leaves unchanged, so it cannot show the defect.**  I checked the
   other in-range candidates by hand: solving `(int32_t)value(b) == b` over the exponent ranges where value
   and bit pattern are of similar size gave no integer solution.  That is a hand derivation, not a run.
   **Enumerate it if you can.**
2. **The DRn NaN value is a model policy and I am not claiming it is correct.**  The manual routes qNaN to
   `qnan(n)`, whose body I did not read.  This round fixes FPUL only.  A DRn row at NaN would pin the policy
   rather than the architecture, so I propose none.
3. **The subnormal DRn value disagrees with the manual's note at DN=1 and this round leaves that alone.**
   10960 says a denormal is treated as 0 when DN = 1.  HEAD converts it to its true value, and `sh_dn()`
   does not flush it (section 4).  That is the named "operands decode per DN=0" gap in `#303`'s comment.

## 7. THE PROPOSED DETECTOR

**Vehicle: extend `VECTORS` in `regress/sh_rounding_probe.py`.**  Facts about it, read today:

* It runs real guest code on an unmodified `-E landisk`, through the cold debugger, one fresh session per
  row per mode.  A row seeds registers through debugger assignments, including `fpul`, writes up to two
  32-bit instruction words, single-steps, and reads back **one** 32-bit word from memory.
* Its `ftrcS-*` rows already read FPUL back by the guest's own `sts` and store, and its `ftrcD-*` rows
  already run with PR set.  So the row shapes needed already exist in the table.  DRn is read a half at a
  time with `fmov.s`, as the `Ddiv 1.0/10.0 low` row reads one half under PR.  No new probe is proposed.
* One readback per session means each input needs up to three sessions per mode: FPUL, high half, low half.

**Gate wiring, from `git show HEAD:regress/gate_sh_rounding.sh`** (the working copy of this file holds
another session's uncommitted edits, at old lines 530, 590 and 822, so I cite only HEAD):

```sh
check     "vector-mode pairs run"                  "$want" 36
check     "vector-mode pairs correct"              "$got"  "$want"
check     "vectors that discriminate the two modes" "$disc" 9
for v in "fdiv" "float" "fadd " "fmac " "fmactie" "fipr" "ftrv" "fmul" \
         "fsub band" "faddinf" "Ddiv" "ftrcS-inf" "ftrcS-ovf" "ftrcS-nan" "ftrcS-edge" \
         "ftrcD-2p31" "ftrcD-neghalf"; do
    n=$(grep -c "^$v.*ok$" "$LOG")
    check "  $v: both modes correct" "$n" 2
done
```

So the row total is pinned by EQUALITY and moves with every added row.  Each row name goes in the list and
must not be a prefix of another row's name, because `grep -c "^$v.*ok$"` matches by prefix.  The probe
prints names in a `%-28s` column, so names must also stay short of 28 characters.  **The discriminating
count stays 9 by my reading**: the conversion to double does not use RM, the new rows' two modes want the
same value, and `discriminating` is computed from the table's own dictionaries.

**Proposed rows** (values from section 6, each run under both modes; the DN=0 leg is a Q3 question):

| row | input | reads | channel: what differs under HEAD or a weakened fix |
|---|---|---|---|
| `fcnvsd fpul 1.5` | 1.5 | FPUL | truncates to 1; a value above 1 in size |
| `fcnvsd fpul -1.5` | -1.5 | FPUL | truncates to `0xffffffff`; the sign path |
| `fcnvsd fpul 0.1` | ~0.1 | FPUL | truncates to 0; a value below 1 in size |
| `fcnvsd fpul -0` | -0 | FPUL | `0x80000000` becomes 0 |
| `fcnvsd fpul inf` | +Inf | FPUL | an undefined cast; the specials |
| `fcnvsd fpul nan` | NaN | FPUL | an undefined cast; the specials |
| `fcnvsd dr hi` | ~0.1 | FR(n) | high half written and in the right register |
| `fcnvsd dr lo` | ~0.1 | FR(n+1) | low half nonzero, so an unwritten register cannot pass |

**Accept side:** these are not a removed guard, so the de-escalation clause does not apply.  The DRn rows are
what show the instruction still does its work.

**Floor (the project's minimum for shipping a detector).**
* (a) red on the pre-fix build: the FPUL rows, once the owed measurement confirms it.
* (b) red on the removed line reinstated verbatim: the same FPUL rows.
* (d) a pure deletion owes the removed behaviour re-introduced under a DIFFERENT predicate.  The handler's
  only dominating predicate is the FD check in the macro, and the body tests nothing.  Candidates are in Q3.
* (e) the probe header names what the detector is designed to catch, and what it does not.

**Clause (c), a null medium, a product carrying none of the behaviour under test.**  This is an
instruction-handler round, so the medium is an IDENTITY BODY: the handler decodes and retires and writes
nothing.  **On that medium every FPUL row goes GREEN by construction, because leaving FPUL alone is what they
test.  Only the two DRn rows can go red**, which is why they are in the table.  The seeded DRn must also differ
from the expected value.  Proposed record, in the required form:

    (c): measured at regress/artifacts/shfcnvsdfpul/<dated dir>/RECEIPT.txt  -- NOT YET RUN, owed before ship

The other permitted form, `(c): by construction via <row/pin>, leg not run`, would rest on the gate's
equality pin and the sentinel `0xdeadbeef` in the readback word.  I do not propose it, because a dead run
is a different medium from an identity body.

**The expected witness rung is 3** (real guest instruction on an unmodified machine description).  Clause (ii)'s
liveness and device-signature controls are written for device accesses; this is a CPU register, and the
`0xdeadbeef` sentinel plus rows whose values could not arise by chance are what I would offer instead.
**Is that adequate, or is a control owed?**

## 8. QUESTIONS

**Q1, premise audit.**  Which premise in sections 2, 4, 6 and 7 is false?  In particular:
(a) does the deleted line's removal leave DRn byte-identical for every FPUL value;
(b) does anything else in the tree rely on FCNVSD having changed FPUL;
(c) is `#297` "removed" or "guarded";
(d) is +0 the only in-range unchanged input;
(e) do the cold-debugger seeds really reach `cd.sh.fpul`, and is FPUL's truncation visible through the guest's
`sts` under the step count the probe uses for a three-instruction row?

**Q2, the partition.**  Which FPUL inputs does the fix change the answer for, and which does it leave alone?
Enumerate the partition, and say whether the row table in section 7 has a member in each part.

**Q3, candidate weakenings.**  Here are candidate forms of the fixed handler.  For each, say whether it is
EQUIVALENT to the fixed form or gives a different result, at which input the two first differ, and which
proposed row, if any, turns red.  Then say which, if any, is inside the project's floor rather than disclosed
coverage debt.  The rule: the floor enumerates the predicates dominating the edit, up to the function boundary,
and partitions the body itself tests; this body tests nothing.  A value class no code tests is clause (e)
disclosure.

    (a) cpu->cd.sh.fpul = (int32_t) op1.f;                        the removed line, verbatim
    (b) if (op1.f >= 1.0 || op1.f <= -1.0) <that line>            only when size is at least 1
    (c) if (op1.f > -1.0 && op1.f < 1.0) cpu->cd.sh.fpul = 0;     only when size is below 1
    (d) if (op1.nan || isinf(op1.f)) cpu->cd.sh.fpul = 0x80000000;  only the specials
    (e) if (sh_fp_rm(cpu) == IEEE_RM_RZ) <that line>              only under one rounding mode
    (f) if (!(cpu->cd.sh.fpscr & SH_FPSCR_DN_ZERO)) <that line>   only with DN clear
    (g) if (ic->arg[0] != (size_t)&cpu->cd.sh.fr[0]) <that line>  only for a destination other than DR0
    (h) after the store: cpu->cd.sh.fpul = (uint32_t) ieee;       the low half of the result
    (i) the two reg() stores exchanged                            high and low halves swapped

Form (f) is why I raise a DN=0 leg: the probe ORs DN into every row except those marked `NODN`, so the table
as proposed never runs with DN clear.  Form (g) asks the same about using only one destination register.
**Is either owed a row, or is each a disclosure?**  Please do not invent further forms unless you can name the
input at which it first differs.

**Q4, option-set completeness.**  The disposition is to delete.  Is there a member this brief did not name?
Say, from the two handlers quoted in section 4, whether the sibling convert uses the same idiom.  The neighbouring questions, each of which I propose to FILE
rather than ride here, under the one-site rule:

* **PR = 0.**  The manual marks FCNVSD reserved at PR=0 (10864, 10883), and the handler converts anyway.  So does
  FCNVDS.  Does this differ from sibling PR=1-only instructions in the tree?  I have not checked whether a row
  already holds this.
* **FCNVDS has no row at all either.**  A grep of `regress/*.py` and `regress/*.sh` for `cnvsd` and `fcnvds`
  matched nothing, case-insensitively.  Should one row of it ride here as a same-file control, or is that scope
  growth?
* **The DN=1 subnormal input** (section 6, item 3).  It is already a named gap.  Does it want its own row, or
  does `#303`'s comment cover it?

**Q5, the vehicle.**  Extending `VECTORS` moves the equality pin at `gate_sh_rounding.sh:64` and the name list at
`:78`.  Re-checked 2026-11-02 by `git diff HEAD -- regress/gate_sh_rounding.sh`: the working copy holds THREE uncommitted hunks of
this session's own earlier (09-17) work, none near those lines -- the `gdrom_default rows run` pin 60 -> 62 with its comment (old
`:530`), a whitespace-only change in a `for v in` list (old `:590`), and `sh4_chcr: rows actually run` 27 -> 29 (old `:822`); each is
paired with an uncommitted probe (`sh4_chcr_probe.py`) and must NOT ride with this round.  So this round's hunks are staged from a
HEAD-based copy of the gate file carrying only its own changes (the project's #548 recipe: back up the working file, commit the
HEAD-based copy, restore and md5-check), not by `git add` of the working file.  `sh_rounding_probe.py` itself is clean.
Eight rows at two modes is sixteen
more sessions.  **Is the row count proportionate to a one-line deletion?**  Name any row you would drop, and say
what then stops turning red.

**If, while verifying a claim, you found something ELSE -- say so.**

**Please end with:** `VERDICT: PROCEED / PROCEED WITH CHANGES / DO NOT PROCEED`, repeated from your first line,
and for any premise you could not settle from this packet, name it.

## 9. VERDICT FORMAT FOR THIS PANEL

First line and last line: `VERDICT: PROCEED / PROCEED WITH CHANGES (<n>) / DO NOT PROCEED`.  Then Q1-Q5 in order, each
answer opening with the question number.  Name every premise you could not settle from this packet.  Packet-fed seats: do not plan
to read files; everything is inlined above.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBP1SHFCNVSD: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
