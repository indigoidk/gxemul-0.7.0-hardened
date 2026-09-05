# pcc2widthkills PASS 3 -- Fable 5 seat findings (2026-09-03)

VERDICT: DO NOT CLOSE. One clause-(d) FLOOR BREACH escapes all 82 rows:
  M_FALL_VECBASE (announce-then-fall-through at the VECBASE arm).

## The escape
VECBASE (0x03) is an ODD, operator-only, STATE-STORING arm: body = `d->pcctwo_reg[0x03] = idata & 0xf0`.
Under M_FALL_VECBASE (the VECBASE decline `break;` removed):
  - the announce STILL fires  -> op vecbase dcl == 1 (green), latch all == 12 (green)
  - the halfword LANDS          -> VECBASE 0x0f -> 0x00 (op vecbase / latch all sessions)
  - NO row reads VECBASE back after a WIDE write to VECBASE's own arm.
    `rb vecbase' writes wide to GENCTL and reads VECBASE (a compose/neighbour check); it
    never exercises the VECBASE arm wide, so it stays green.
=> 82/82, TOTAL ESCAPE. Same class the round set out to close; missed at the FIFTH odd arm.

## Why it was missed (records defect that hid it)
PRETABLE Section 2's parity table credits `rb vecbase' as VECBASE's readback. It is not --
it is GENCTL's neighbour-lane row. So VECBASE was left OUT of the "no readback" list
(PSCALEADJ/SCCICR/SCCRX/SCSIICR), and the builder's PREDICTIONS3B enumerated only those four.
The builder's OWN reasoning ("wide writes occur in exactly two sessions -- op X and latch all
-- no readback") applies verbatim to VECBASE.

## Enumeration (12 blocks x 6 shapes = 72 cells): 71 covered, 1 escape
S1 delete      : 12/12 (dcl rows drop to 0)               measured GENCTL,MASK,TxICR
S2 len>2       : 12/12 (halfword dcl/readback rows)       measured TxICR,TxCTL,SCCTX,SCCERR,MASK
S3 exit1       : 12/12 (survival rows)                    measured IPL,MASK
S4 alias       : cardinality, any collision -> latch all  measured SCCTX->SCCRX
S5 fall-through: 9 caught, 2 equiv (SCCERR stores0, IPL stores nothing), 1 ESCAPE = VECBASE
S6 operand-swap: 12/12 (latch all value 0x0003 <=0xff)    measured GENCTL

## Smallest edit that breaks and passes 82 (Q2)
Remove the `break;' after `pcc2_width_decline(d, PCC2_W_VECBASE_LEN, ...)'. One line.
Expected-green rows a naive reviewer trusts: op vecbase, op vecbase dcl, rb vecbase, latch all.

## Disposition
L2 floor breach -> repair IN-ROUND: add a VECBASE own-landing readback (rb vecbase2, the
rb mask pattern), and per the class-closure amendment enumerate ALL SIX operator-path arms
in the contract, stating readback (VECBASE/SCCICR/SCCRX/SCSIICR/MASK) vs message-only
(PSCALEADJ) vs value-identical (SCCERR) vs benign-noop (IPL).

## Q4 records
- Stale probe comment line 69: "five ... seven" contradicts the corrected six/six (docstring +6 lines below).
- PRETABLE Section 2 parity table misclassifies rb vecbase as VECBASE's readback (the defect that hid the escape).
- Contract DOES-NOT-CATCH does not exclude VECBASE fall-through -> it is a breach, not "outside the contract".
- "seven of the twelve blocks call reassert" -- VERIFIED correct (GENCTL,TxICR,SCCICR,SCCTX,SCCRX,SCSIICR,MASK).

## Confirmed sound
- 82 gate rows == 82 probe rows, set-equal, no dupes; denominator pinned 82 x3.
- m88k alignment premise: `#ifndef LS_1 ... if (addr & (LS_SIZE-1)) m88k_exception(MISALIGNED); return;` BEFORE memory_readmax64.
- six-even/six-odd parity from mvme_pcctworeg.h offsets.
- typedef NBITS(12)<=32 -> char[1], sound compile-time no-op.
- latch all is a sound cardinality row; op pscale noig / rb sccicr/sccrx/scsiicr correct on fix (pass3c 81/82 each).
