# ASSESS-STAGE BRIEF — `gdromwarnbits`: a pre-set trigger discharged, code SHIPPED, row NOT closed

## 0. THE HOLD QUESTION — this stage is held FOR this, answer it explicitly

> **Does discharging a PRE-SET TRIGGER require a full nine-seat panel, when the trigger
> already fixed every design choice and the change is measured behaviour-preserving?**

My lean is: *a panel only if the discharge makes a choice the trigger did not already fix.*
**That test is self-serving — the same loop wrote both the trigger and the discharge — and it
wants checking rather than accepting.** Whatever is ruled reads back onto `dev_sh4.c`, which
fired its own equivalent trigger the same way and is recorded as discharged.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise the brief stated wrongly, and a
round yesterday had FOUR load-bearing premises refuted by seats that opened a file the author
had not. **Check the premises, not just the derivations.** A seat that re-derives a fact from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`). They are NOT this fork. If your line numbers disagree
with mine by hundreds, you are reading one of them — say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined below. Name
any premise you cannot settle from this packet rather than guessing at it.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 1. WHAT SHIPPED (commit `84f6682`, already committed, tree clean)

`src/devices/dev_dreamcast_gdrom.c`, **35 insertions / 7 deletions**, no other product file.

### 1a. The field widened

```c
-	uint8_t		warned;
+	uint32_t	warned;
```

### 1b. The six masks became an enum of bit POSITIONS

BEFORE:

```c
#define	GDROM_W_LEN		0x01
#define	GDROM_W_NODATA	0x02
#define	GDROM_W_NOTWAIT	0x04
#define	GDROM_W_OVERREAD	0x08
#define	GDROM_W_DMANODATA	0x10
#define	GDROM_W_DMAARM		0x20
```

AFTER (the explanatory comment is elided here; its load-bearing claim is quoted in §4):

```c
enum {
	GDROM_W_LEN_B,		/*  was 0x01  */
	GDROM_W_NODATA_B,	/*  was 0x02  */
	GDROM_W_NOTWAIT_B,	/*  was 0x04  */
	GDROM_W_OVERREAD_B,	/*  was 0x08  */
	GDROM_W_DMANODATA_B,	/*  was 0x10  */
	GDROM_W_DMAARM_B,	/*  was 0x20  */
	GDROM_W_NBITS
};

#define	GDROM_W_LEN	(1u << GDROM_W_LEN_B)
#define	GDROM_W_NODATA	(1u << GDROM_W_NODATA_B)
#define	GDROM_W_NOTWAIT	(1u << GDROM_W_NOTWAIT_B)
#define	GDROM_W_OVERREAD	(1u << GDROM_W_OVERREAD_B)
#define	GDROM_W_DMANODATA	(1u << GDROM_W_DMANODATA_B)
#define	GDROM_W_DMAARM	(1u << GDROM_W_DMAARM_B)
```

### 1c. NO CALL SITE CHANGED

All six consumers still spell the MASK name. This is claimed to be the complete population —
every `GDROM_W_` use in the file outside the definition block:

```
 625:	if (!(d->warned & GDROM_W_LEN)) {
 626:		d->warned |= GDROM_W_LEN;
 637:		if (!(d->warned & GDROM_W_NODATA)) {
 638:			d->warned |= GDROM_W_NODATA;
 676:		if (!(d->warned & GDROM_W_OVERREAD)) {
 677:			d->warned |= GDROM_W_OVERREAD;
 702:		if (!(d->warned & GDROM_W_NOTWAIT)) {
 703:			d->warned |= GDROM_W_NOTWAIT;
 960:			if (!(d->warned & GDROM_W_DMANODATA)) {
 961:				d->warned |= GDROM_W_DMANODATA;
1016:		if (!(d->warned & GDROM_W_DMAARM)) {
1017:			d->warned |= GDROM_W_DMAARM;
```

**PREMISE TO CHECK, not to accept:** the claim is that these twelve lines are the entire
consumer set and that none of them changed. If you can read the tree, verify the population
is twelve, and verify that nothing stores or copies `warned` anywhere it is truncated back to
8 bits — a struct copy into a narrower field, a `%hhx` format specifier, an explicit cast, or
a serialised save-state that writes one byte.

## 2. WHY IT SHIPPED BEFORE ITS PANEL

The trigger was written into the file in `#460` and read: *"at the SEVENTH bit, widen
`warned` and convert these to an enum of bit POSITIONS ending in a GDROM_W_NBITS count."*

`gdromexitsix` Round 1 (the next round, in flight) adds **three** latches to the six in use.
The ninth would be `1u << 8`, which **truncates to zero in a uint8_t** — the latch never
sets, `!(warned & BIT)` stays true forever, and the diagnostic it guards FLOODS. No compile
error, no runtime complaint. **Two seats on that round's pass 1 reached this independently**
without being told the trigger existed.

So the code lands because Round 1 cannot proceed without it. **The ROW stays `in work` with
this stage HELD**, which is why you are reading this.

## 3. THE MEASUREMENT — behaviour-preservation, measured rather than asserted

Preserved at `regress/artifacts/gdromwarnbits/mask_equivalence_check.{c,out}`. Full source:

```c
#include <stdio.h>
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B,
       GDROM_W_OVERREAD_B, GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_NBITS };
#define GDROM_W_LEN       (1u << GDROM_W_LEN_B)
#define GDROM_W_NODATA    (1u << GDROM_W_NODATA_B)
#define GDROM_W_NOTWAIT   (1u << GDROM_W_NOTWAIT_B)
#define GDROM_W_OVERREAD  (1u << GDROM_W_OVERREAD_B)
#define GDROM_W_DMANODATA (1u << GDROM_W_DMANODATA_B)
#define GDROM_W_DMAARM    (1u << GDROM_W_DMAARM_B)
int main(void){
  unsigned want[6]={0x01,0x02,0x04,0x08,0x10,0x20};
  unsigned got[6]={GDROM_W_LEN,GDROM_W_NODATA,GDROM_W_NOTWAIT,
                   GDROM_W_OVERREAD,GDROM_W_DMANODATA,GDROM_W_DMAARM};
  int i,bad=0;
  for(i=0;i<6;i++){ if(got[i]!=want[i]){printf("  MISMATCH %d\n",i);bad=1;} }
  printf("  GDROM_W_NBITS = %d\n", GDROM_W_NBITS);
  printf(bad?"  MASKS DIFFER\n":"  ALL SIX BIT-IDENTICAL\n");
  return bad;
}
```

Its output, verbatim:

```
  GDROM_W_NBITS = 6, so 26 bits remain free in a uint32_t
  ALL SIX MASKS BIT-IDENTICAL to the hand-assigned originals
```

**PREMISE TO CHECK:** this check compiles the enum **in isolation**, not as it appears in
`dev_dreamcast_gdrom.c`. Does that weaken it? The argument for "no" is that the enum text is
copied verbatim and C's enum numbering is not context-dependent. But that is an assertion,
and it is exactly the "the verifier shares the defect of the thing it verifies" trap this
project has already been bitten by — a verification regex once matched the same wrong section
as the edit it was checking, and reported MATCH.

## 4. THE ONE KNOWN GAP, AND IT WANTS A RULING

`GDROM_W_NBITS` is described in the shipped comment as making the count *"correct BY
CONSTRUCTION rather than by maintenance"*. **But nothing in the product build enforces
`GDROM_W_NBITS <= 32`.** The bound is checked only by the offline program above, which
`make` does not compile.

The file's own comment near `:325` states why no assertion is present: `_Static_assert` is
C11 and this tree targets C99. `src/include/thirdparty/dreamcast_sysasicvar.h:77` records the
same decision for `#466` — shipped as a COMMENT ONLY, same rationale.

**So the honest reading is that this conversion moves the failure from SILENT (a truncating
`1u << 8`) to LOUD-ONLY-IF-SOMEONE-RUNS-AN-OFFLINE-CHECK — better, but not "by
construction".** Three questions:

* **(a)** Is the shipped comment's *"correct BY CONSTRUCTION"* an OVERCLAIM that should be
  corrected in place (this project's L4 — wrong record)? It looks at least loose: what is
  by-construction is the **uniqueness** of each bit, not the **bound** on their count.
* **(b)** Is there a C99-legal zero-cost bound assertion this tree would accept? The classic
  is a negative-array-size trick:
  `typedef char gdrom_w_fits[(GDROM_W_NBITS <= 32) ? 1 : -1];`
  — legal C99, no runtime cost. **Does this tree have precedent for that idiom, or a standing
  reason to refuse it?** Please grep rather than guess; the two in-tree comments above chose
  prose over C11 `_Static_assert`, and a C99 form may simply never have been considered. If
  you find the idiom in use anywhere in `src/`, say where.
* **(c)** If (b) is technically fine, does the ADDITION LICENCE bar it anyway? This project's
  rule is that additions to product code are licensed by MEASURED DELTAS or a TRANSFERRED
  WARRANT, never by "it cannot hurt". A bound assert that cannot fire at six bits has no
  measured delta. **Is a compile-time guard against a documented silent-failure mode a
  warrant, or is it exactly the "dead guards accrete" shape the licence exists to refuse?**

## 5. WHAT EACH SEAT IS ASKED FOR

1. **The HOLD QUESTION in §0** — a direct answer, with your reason.
2. **§1c's population claim** — is twelve the complete consumer set, and does anything
   truncate `warned` back to 8 bits (struct copy, format specifier, cast, save-state)?
3. **§4(a)/(b)/(c)** — the overclaim, the C99 idiom, the addition licence.
4. **The smallest edit that breaks this and still passes.** What change to this file would
   re-open the silent-truncation failure while leaving the equivalence check green?
5. **Anything the brief got wrong.** Premises before derivations.

Do not defer to seat authority; if you disagree, say so plainly and name the check that would
settle it.
