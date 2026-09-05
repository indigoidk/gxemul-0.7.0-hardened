# pcc2widthkills PASS 6 -- Fable 5 measuring seat

## Headline
The 118-row detector closes every class the prior passes named (latch-SET state via rb2*,
FAULT member at operator blocks via `latch all fail`, wide-READ fall-through via hrd*rb/noro,
typedef bound). All verified against source + the part3/4/5 driver logs.

BUT the domain is NOT fully closed. A guard qualified by device RUNTIME state that no row
holds in a non-initial value escapes all 118 rows:
  - d->pending_timer1_interrupts, d->pending_timer2_interrupts  (0 in every session)
  - d->cur_int_vec[8]                                           (all-zero in every session)
  - the reassert_interrupts()-recomputed PCCTWO_IPL register byte (0 in every session)

## The measured mutant
  case PCCTWO_T2ICR/T1ICR:
    if (len != 1 && writeflag == MEM_WRITE && !d->pending_timer2_interrupts) {
Analytic certainty: no probe row enables timer2 (CEN) with a nonzero compare and drives a
tick, so pending_timer2_interrupts is 0 in all 118 sessions -> the added conjunct is always
true -> byte-identical behavior to the fix on all 118 rows -> 118/118 escape.
Property break: a guest with an armed/fired timer2 interrupt (pending>0) that wide-writes
T2ICR is NOT declined -> the RMW body runs on the big-endian idata -> neighbour lane into an
interrupt-control register (and can wrong-decrement pending via the ICLR/IEN lanes).

## Disposition (the judgment call, both sides)
At TxICR the body READS pending_timer1/2_interrupts (the `> 0` tests at the RMW arm), so by the
clause-(d) DEPENDS-ON closure (2) -- "swaps drawn ONLY from fields the guarded BODY reads" --
this conjunct is IN closure -> floor-eligible (L2), same standard that made pass-5's `warned`
qualifier an L2. AGAINST: a (d) mutant must "read like the same check"; `&& !pending_timer2`
does not read like a width check, and it is out-of-closure for 11 of 12 arms (reassert is a
callee). Lean: BELOW the floor as an implausible width-check edit => FILE as coverage debt,
but the contract MUST gain a one-line DOES NOT CATCH disclosure, and the pre-table
guard-field/body-field walk for TxICR should have listed pending_timer* (it lists only len/idata).

## Everything else verified honest
- gate: emitted 118 / green 118 / red 0 (gate_arm.sh:1300-1302).
- offsets even/odd split exact (mvme_pcctworeg.h): 6 even guest-reachable, 6 odd operator + T1CTL/T1ICR labels.
- d->warned written only at dev_pcc2.c:402 (helper); the `static int warned` at :423 is a different symbol.
- GENCTL/MASK bodies byte-identical (store idata; reassert). SCCERR only ever 0 (E-warrant true).
- reassert called by exactly 7 of 12 width blocks; 8 arms mask/RMW/clear; 5 of those 8 reassert -- comment correct.
- typedef pcc2_w_fits_in_warned tests the field via sizeof(member); PCC2_W_NBITS=12 <= 32 -> ok; narrowing warned -> compile error.
- part5/part5b logs match the brief tables (BASE 118; M_RET0_VECBASE 116; M_TEST_EQ 117; M_QUAL_GENCTL 117; M_QUAL_ALL 107; M_NOWRITECHK_GENCTL 117), clean restore + sentinel cleared.

## Retraction (my own error, recorded)
Earlier I reported build/ lacked the fix -- FALSE. It was a cwd artifact: build/ is at the
PROJECT ROOT, not under GXEMUL-SEC. The real build/ HAS the fix, == SEC, gxemul FRESH.
CHECKPOINT's "three trees CLEAN+FRESH" is correct.
