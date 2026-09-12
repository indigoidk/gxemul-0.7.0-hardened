# `ppcrlwimiwidth` + `ppcrldimimask` PASS 2 — review of two PowerPC fixes and their detectors before commit

VERDICT LINE FIRST, then the liveness token `PASS2_PPC_20260912`.

**ONE QUESTION: is there a clause-(d) mutant of either fix that stays GREEN on its detector?**
(Second, only if you read the source: is either fix itself wrong against Book I? — see the end.)

This is a mutation-testing review of an emulator detector.  **Please do not simply ratify** — a
recent panel had seven of nine seats confirm a premise a brief stated wrongly.  **Check the
premises, not just the derivations.**  If you find nothing, say WHAT YOU SWEPT (which predicates,
which operand swaps, which (SH, MB, ME) cells) — "zero found" and "zero looked for" must not read
the same.

## THE TREE

`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` and `...\GXEMUL-SEC\regress\`.  Ignore any other `src/`
under the project root (pristine 2021 copies; line numbers off by hundreds).

## ARCHITECTURE (PowerPC Book I v2.01, local copy `_scratchpad/ppc_uisa_book1_v201.txt`)

* rlwimi: `r <- ROTL32((RS)32:63, SH); m <- MASK(MB+32, ME+32); RA <- (r & m) | ((RA) & ~m)`.
  ROTL32 rotates the low word and DUPLICATES it into both halves.  MASK(x, y) is 1s from x through
  y, **wrapping if x > y** (:578).  So when MB > ME the mask covers the whole high word and RA's high
  word becomes the rotated word; when MB <= ME the high word is untouched.
* rldimi: `r <- ROTL64((RS), sh); m <- MASK(mb, 63-sh); RA <- (r & m) | ((RA) & ~m)` — the mask
  wraps when mb > 63-sh.

## THE FIXES (uncommitted), `src/cpus/cpu_ppc_instr.c`, both functions WHOLE, post-fix

```c
X(rldimi)
{
	uint32_t iw = ic->arg[0];
	int rs = (iw >> 21) & 31, ra = (iw >> 16) & 31;
	int sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
	int mb = ((iw >> 6) & 31) | (iw & 0x20);
	int rc = ic->arg[0] & 1;
	int m, n = sh;                                   /* FIX: was `int m;` */
	uint64_t tmp, s = cpu->cd.ppc.gpr[rs];
	while (n-- != 0) {                               /* FIX: was `sh--`, which left sh = -1 */
		int b = (s >> 63) & 1;
		s = (s << 1) | b;
	}
	m = mb; tmp = 0;
	do {
		tmp |= ((uint64_t)1 << (63-m));
		m = (m + 1) & 63;                        /* FIX: was `m ++;` */
	} while (m != ((64 - sh) & 63));                 /* FIX: was `m != 63 - sh` */
	cpu->cd.ppc.gpr[ra] &= ~tmp;
	cpu->cd.ppc.gpr[ra] |= (tmp & s);
	if (rc)
		update_cr0(cpu, cpu->cd.ppc.gpr[ra]);
}

X(rlwimi)
{
	uint32_t tmp = (uint32_t)reg(ic->arg[0]);        /* FIX: was MODE_uint_t tmp = reg(...) */
	MODE_uint_t ra = reg(ic->arg[1]);
	uint32_t iword = ic->arg[2];
	int sh = (iword >> 11) & 31;
	int mb = (iword >> 6) & 31;
	int me = (iword >> 1) & 31;
	int rc = iword & 1;

	tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

	/* (a 19-line comment: the wrapping mask selects the duplicated high word; a 32-bit
	   MODE_uint_t build keeps only the low word by unsigned-conversion semantics) */
	if (mb > me)                                     /* FIX: added, BEFORE the loop */
		ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);

	for (;;) {
		uint64_t mask;
		mask = (uint64_t)1 << (31-mb);
		ra &= ~mask;
		ra |= (tmp & mask);
		if (mb == me)
			break;
		mb ++;
		if (mb == 32)
			mb = 0;
	}
	reg(ic->arg[1]) = ra;
	if (rc)
		update_cr0(cpu, ra);
}
```

**The defects fixed.**  rlwimi: a 64-bit `tmp` rotated as if 32-bit contaminated the low word with
high-word bits (`(tmp << sh) | (tmp >> (32-sh))` on 64 bits), and a wrapping mask never wrote the
high word.  rldimi: the rotate loop consumed `sh` (leaving -1), so the mask end was computed from
-1; and the mask loop did not wrap past bit 63.

## SETTLED PREMISES (do not re-derive; challenge only with evidence)

* Both detectors drive real `rlwimi`/`rldimi` instructions on the unmodified in-tree machine
  `-E bareppc -M 64` (PPC970, 64-bit) through the debugger, one instruction per destination register.
* A 32-bit CPU build (PPC603) keeps only the low word; a 64-bit CPU in 32-bit MODE is disclosed, not
  covered (filed separately as `ppccr0modewidth`).

## THE DETECTORS

**`regress/ppc_rlwimi_probe.py` — 28 rows.**  Sources: RS_VAL = 0xDEADBEEFCAFEF00D (halves differ),
MUT_RS = 0xAAAAAAAA0000000F; destinations pre-seeded with SENT = 0x5A5A5A5A5A5A5A5A.
Rows: controls (`session`, `live`, `seed holds`, `src intact`, `disasm xcheck`, `ctl rlwinm`,
`neg apparatus`, `bits32 live`, `bits32 rlwimi`, `cr0 record form`, `disasm total` = 146/146,
`census run` = 129); non-wrapping into a zero dest (`nowrap sh0` [0,31], `nowrap sh8 mb0` [0,15],
`nowrap sh16 mb8` [8,23], `nowrap sh4 mb16` [16,31]); wrapping into SENT from MUT_RS (`wrap mutant`
sh0 [31,0], `wrap sh0 mb24` [24,8], `wrap sh8 mb20` [20,10], `wrap sh16 mb28` [28,4]); preservation
into SENT (`pres nowrap` sh8 [0,15], `pres wrap` sh0 [24,8], `wrap fullword` sh0 [1,0]); RA == RS
aliasing (`alias nowrap`, `alias wrap`, `alias both`); and a CENSUS: SH in {0,1,8,16,31} x
nonwrap {(0,31),(0,15),(8,23),(16,31),(10,20),(0,0),(31,31)} x wrap {(31,0),(24,8),(20,10),(28,4),
(1,0),(31,30),(16,8)}, plus the diagonals (k, k, 31-k) and (k, 31-k, k) for k = 0..31, deduplicated
to 129 cells, each into a SENT destination from RS_VAL, compared with Book I's RTL (`census wrong`
wants 0, `census zero` wants 0).

**`regress/ppc_rldimi_probe.py` — 27 rows.**  Controls (`session`, `live`, `seed holds`, `src intact`,
`disasm xcheck`, `ctl rldicl`, `ctl rldicr`, `neg apparatus`, `bits32 live`, `bits32 rld bad`,
`cr0 record form`, `disasm total` = 511/511, `census run` = 495); non-wrapping (`nowrap sh8 mb0`,
`nowrap sh32 mb0`, `nowrap sh0 mb0`, `nowrap sh16 mb16`, `nowrap single`); wrapping (`wrap sh40
mb40`, `wrap sh63 mb63`, `wrap full`, `wrap sh48 mb32`); preservation (`pres nowrap`, `pres wrap`,
`pres sh0`); and a 495-cell (SH, MB) census from an all-ones source, compared with Book I.  The
census does not test the rotate amount independently of the mask bounds — the pattern rows do.

## MEASURED — joint kill table 2 (one build per leg, BOTH probes against it), frozen instruments

| leg | edit | rlwimi /28 | rldimi /27 |
|---|---|---|---|
| BASE | the fix | 28 CONTROL=OK | 27 CONTROL=OK |
| HEAD | committed code | 14 | 17 |
| R_REV_COND | `if (mb > me)` -> `if (mb < me)` | 13 CONTROL=FAIL | 27 |
| R_ONLY_CAST | keep the uint32_t read, drop the high-word line | 19 | 27 |
| R_ONLY_HIGH | keep the high-word line, revert `tmp` to MODE_uint_t | 19 | 27 |
| R_POST_LOOP | move the `if (mb > me)` line AFTER the loop | 19 | 27 |
| R_ORIG | both rlwimi edits reverted | 14 | 27 |
| R_NULL | decode and retire, insert nothing | 12 CONTROL=FAIL | 27 |
| D_MUT63 | end test `(63 - sh) & 63` | 28 | 14 CONTROL=FAIL |
| D_NOCIRC | `m ++` without `& 63` | 28 | 20 CONTROL=FAIL |
| D_NOKEEP_SH | rotate loop consumes `sh` again | 28 | 16 CONTROL=FAIL |
| D_NOWRAP | `m ++; } while (m < 64 - sh)` | 28 | 21 CONTROL=OK |
| D_NO_MERGE | `gpr[ra] = (tmp & s)` (no preserve) | 28 | 24 CONTROL=FAIL |
| D_ORIG | all rldimi edits reverted | 28 | 17 |
| D_NULL | decode and retire, insert nothing | 28 | 13 CONTROL=FAIL |

Every rlwimi mutant left rldimi at 27/27 and vice versa.  14 of 15 legs were exactly as predicted in
writing before the table; D_NOCIRC was predicted 18 and measured 20 (its census completed this time;
in an earlier table it hit a 90 s session timeout at cell 182 — load decides, and it fails the gate
either way on `census wrong`).

## QUESTIONS

1. **(the one that matters)** Enumerate DEPENDS-ON for each diff: the predicates DOMINATING the edited
   lines up to the function boundary (rlwimi: `sh ?`, `mb > me`, the loop's `mb == me` and `mb == 32`;
   rldimi: `n-- != 0`, the mask loop's end test), and operand swaps drawn from fields the body reads
   (`tmp`, `ra`, `mb`, `me`, `sh`, `n`, `m`, `s`).  **Name any mutant that leaves its detector green**,
   and say which row or census cell you expected to catch it and why it cannot.  Candidates I have NOT
   built, to check or refute: rlwimi `mb > me` -> `mb >= me` (does a single-bit MB == ME cell with a
   SENT high word exist? the census has (0,0) and (31,31)); rlwimi `(uint64_t)tmp << 32` -> the
   UNROTATED source word; rldimi end test `m != 64 - sh` without `& 63` (sh = 0 only); rldimi rotate
   loop `n-- > 1`.
2. **Does any row's named channel fail to vary under its named mutant** (vacuous by construction)?
   Note the census source for rldimi is all-ones: which rotate defects is that blind to, and do the
   pattern rows actually cover them?
3. **`disasm total` and `census run` now want literals (146/129, 511/495).**  No leg in this table
   produced a short census, so those pins carry no measured kill.  Is that a floor gap or disclosure?
4. *(file-reading seats only)* Is either fix wrong against Book I for any (SH, MB, ME) the census does
   not reach?

Give a verdict line: `NO SURVIVING (d) MUTANT — swept: <list>` or `SURVIVOR: <exact edit>`.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
