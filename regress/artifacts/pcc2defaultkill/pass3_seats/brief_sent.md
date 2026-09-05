# #501 pcc2defaultkill -- PASS 3: the pass on the REPAIR DIFF.  Pass 2 found the 23-row detector below the floor six ways (two MEASURED clean sweeps, four predicted); the repair closes the class in one diff and this pass reviews THAT diff.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A repair made in response to a pass 2 owes its own pass, scoped to the repair diff -- **but the FLOOR QUESTION is
asked of the shipped COMPOSITE**: does a clause-(d) mutant exist that sweeps the 36-row detector clean?  Pass 2's
five PASS/GO seats had not tried the six edits three seats then named; **two of those were measured at 23/23 on the
instrument those seats had passed.**  So: build (or derive) the edit, do not vote.  Check the premises, not the
derivations; be harder on the ACCEPTED dispositions; a seat whose escape was adopted scrutinises its own repair row
MORE (does the row kill the mutant for the reason claimed, or by accident?).  **VERDICT LINE FIRST.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of `7076134`.**  Three
pristine-2021 copies of `src/` under the project root are NOT this fork; if your line numbers disagree by hundreds
you are reading one -- say so.  The pass-2 product state is preserved verbatim as
`regress/artifacts/pcc2defaultkill/killtable_20260905/dev_pcc2.pass2.c` and the pass-2 instrument as
`killtable_20260905/frozen_probe.py` (md5 a96b8bcf): the diffs below are against THOSE.

## PREMISES ALREADY SETTLED, RE-INLINED (each is a QUESTION if you can check it)

1. **The fix** (unchanged in substance since pass 1): the `default:` arm no longer calls `exit(1)`; a READ keeps the
   byte the memcpy served; a WRITE is DECLINED (member 3, not member 6 -- the cased siblings contradict a blanket
   store); one latched `fatal()` per offset per instance (`uint64_t warned_unimpl`, bit `relative_addr`, which is
   folded `%= PCC2_SIZE` (0x40) as the handler's first statement so the shift is 0..63 on a 64-bit type).  43 of the
   0x40 offsets reach the arm: 18 named-unimplemented, 12 counter interiors, 13 the fork header leaves unnamed (the
   MANUAL names some of those: 0x39 is SPEED's second byte, 0x3b PRTDATA's low byte).
2. **The repair to the product** is confined to the arm: both announces gain `(len %d)`; the read announce prints
   `data[0]` -- the byte actually SERVED -- instead of reloading `d->pcctwo_reg[relative_addr]`, because the SIGALRM
   tick rewrites the counter interiors between the memcpy and the announce (codex), and a wide read is labelled.
   `data` was filled by the memcpy above the switch (or zero-filled on the #119 end-span path, where `data[0]` is
   then truthfully 0x00).  Three comment sentences corrected ("no guest reaches" -> the inspected OpenBSD driver
   paths; "the array's default, not a computed value" -> the array's CURRENT byte, the tick's for an interior;
   "four arms up" -> above).
3. **The six escapes of the 23-row instrument** and the row that now kills each:
     Opus M_O1  read announce value -> 0 (MEASURED 23/23)              -> `srvd val text` (wants `served 0x34`)
     Opus M_O2  member 6 on the LATCHED path (MEASURED 23/23)          -> `sameoff val` (wants 0x0, reads 0x5a)
     grok A     latch SET only on writes                                -> `latch rd rd`, `latch rd wr` (want 1, print 2)
     grok B     `if (len != 1) exit(1);`                                -> `wide wr`, `wide rd` (host exit)
     codex      `|=` -> `=` at the latch update                          -> `latch aba` (wants 2, prints 3)
     Fable      `if (relative_addr == 0x06) exit(1);`                   -> `inword wr`/`inword rd` (all 12 interiors now)
   In table 3 each of those six is scored by BOTH instruments: the pass-2 one (23/23 = the breach, measured) and the
   repaired one (red).  BASE is measured full on both (the old anchors survive the `(len N)` text).
4. **The setter x tester product**: the body tests `writeflag` in the announce and the guard tests the latch bit;
   because the SET is unconditional, a mutant can condition it -- so the SETTER's direction is a real axis.  Rows:
   W,W `latch sameoff`; W,R `latch rw one`; R,R `latch rd rd`; R,W `latch rd wr`; accumulation `latch aba`.  `len` is
   NOT tested by the arm, so width cells are CLAIM rows (the pass-1 PRETABLE claimed "byte-and-wide"), not floor:
   one per direction at len 4; len 2 DISCLOSED.
5. **The witness** (rung 3, unchanged): 7/13 on the committed build, 13/13 on the fix (`witness_20260905/`).
6. **The roster**: nine seats; agy DELIBERATELY NOT FIRED (measurement reserve).  Pass 2's kimi CLI stalled on the
   pointer form and answered on a re-fire with the packet inline; glm/deepseek burned on the full packet and answered
   2 KB mini packets.  **This packet is therefore SHORT on purpose.**

## THE MEASUREMENTS (every number names its log)

Table 3 (`killtable3_20260905/driver.log`; frozen repaired instrument md5 10737375, live 10737375; the pass-2
instrument `old23/` a96b8bcf; scratch clone of build/, BASE rebuilt in the clone, each mutant compile-checked before the
table (12/12) and proven by a diff count).  `.old23` rows are the pass-2 instrument on the same binary:
    BASE               36/36    -
    BASE.old23         23/23    -
    M_WRLATCH          34/36    latch rd rd,latch rd wr
    M_WRLATCH.old23    23/23    -
    M_WIDEKILL         32/36    wide wr,wide wr msg,wide rd,wide rd srvd
    M_WIDEKILL.old23   23/23    -
    M_OFFKILL          34/36    inword wr,inword rd
    M_OFFKILL.old23    23/23    -
    M_SRVD0            35/36    srvd val text
    M_SRVD0.old23      23/23    -
    M_BACKED2          35/36    sameoff val
    M_BACKED2.old23    23/23    -
    M_ABA              35/36    latch aba
    M_ABA.old23        23/23    -
    M_EXIT             7/36     named wr,named wr msg,named rd,named rd msg,named rd srvd,inword wr,inword rd,unnamed wr,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch twooff,latch rw one,latch rd rd,latch rd wr,latch aba,alias 0x6a,alias msg,dir wr text,wr declined,dir rd text,srvd val,srvd val text,wide wr,wide wr msg,wide rd,wide rd srvd
    M_UNLATCH          30/36    latch sameoff,latch rw one,latch rd rd,latch rd wr,latch aba,wide wr msg
    M_ONELATCH         31/36    named wr msg,named rd msg,named rd srvd,latch twooff,latch aba
    M_BACKED           32/36    ieicr rdawr,ieerr rdawr,sameoff val,wide wr
    M_RDKILL           17/36    named rd,named rd msg,named rd srvd,inword rd,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch rw one,latch rd rd,latch rd wr,dir rd text,srvd val,srvd val text,wide wr,wide wr msg,wide rd,wide rd srvd
    M_DIRSWAP          30/36    named rd srvd,dir wr text,wr declined,dir rd text,srvd val text,wide rd srvd

PREDICTIONS written BEFORE the table (`PRETABLE_501b.out`, VERBATIM):
```
PRE-TABLE BLOCK, #501 pcc2defaultkill PASS-2 REPAIR (table 3) -- written BEFORE the table (mtime against
killtable3_20260905/driver.log).  Repair from the nine-seat pass 2 (_scratchpad/panel_20260905_055656): Opus MEASURED
two 23/23 escapes (M_O1 read-announce value, M_O2 member 6 on the latched path); grok predicted two (A latch SET only
on writes; B `len != 1' re-kill); codex predicted one (`|=' -> `='); Fable predicted one (re-kill at an unsampled offset).
Class closure in ONE diff rather than one cell per pass (the repair-chain amendment).

  - SIBLING PARITY -- the twelve cased byte arms decline WIDE writes with a latched announce that names the register
    and the width; the default arm's announce named neither the width nor (for a wide read) which byte.  Repaired:
    both announces carry `(len N)'; the read announce prints data[0] -- the byte SERVED -- not a reload of the array
    (codex: the SIGALRM tick rewrites the counter interiors between the memcpy and the announce).  Rows: wide wr msg,
    wide rd srvd, srvd val text.
  - CLAIM -> ROW -- every claim the pass-2 seats found rowless now has one: "per offset, not per direction" ->
    latch rd rd + latch rd wr (the two setter x tester cells rw one could not see); bits accumulate -> latch aba;
    "declined" on the latched path too -> sameoff val; "served" means THE byte -> srvd val + srvd val text;
    "byte-and-wide" (the pass-1 PRETABLE's own sentence, rowless) -> wide wr + wide rd; "43 offsets" -> every one
    now written and read (inword/unnamed wr at 12/13, + inword rd, unnamed rd).  The pass-1 PRETABLE's guard/body
    sentence -- "they disagree only in the latch's own state, which the sameoff/twooff/rw-one rows build" -- was the
    miss: the state was built and observed on the COUNT channel only; the VALUE channel on the latched path had no
    row (Opus).  Claim sentences in the product comment corrected: "no guest reaches" -> "no inspected OpenBSD
    driver path reaches"; "the array's default, not a computed value" -> "current byte (the tick's, for a counter
    interior)"; "four arms up" -> "above".
  - GUARD FIELD vs BODY FIELD -- guard: warned_unimpl bit relative_addr.  Body: writeflag, idata, len, data[0].
    Joint cells (body-tested writeflag x latch state, with the SETTER's direction as the third axis because the set
    is unconditional and a mutant can condition it): W,W (sameoff) W,R (rw one) R,R (rd rd) R,W (rd wr) -- all four
    rowed; accumulation across offsets (aba); disposition at latch-set (sameoff val).  len is NOT tested by the arm,
    so width cells are CLAIM rows, not floor -- one per direction at len 4; len 2 disclosed.
  - CHANNEL -- per new row: latch rd rd / rd wr / aba: announce COUNT under DKA/DKE; sameoff val: read-back VALUE
    under DK2 (and DKB); srvd val text: announce TEXT under DKZ (value 0x34 the guest wrote); wide wr / wide rd:
    FATE under DKW, VALUE under DKB; wide wr msg / wide rd srvd: TEXT `(len 4)'; inword rd / unnamed rd: FATE under
    DKF and DKO; wr declined: TEXT under DKS.  Each channel varies under its named mutant by construction.

PREDICTIONS (36-row instrument; the six pass-2 mutants ALSO on the 23-row pass-2 instrument, where 23/23 is the
measured breach; MINIMUM red set per mutant):
    BASE        36/36  and 23/23 on the pass-2 instrument (its anchors `offset 0x2a', `served 0x', the direction
                       phrases and MSG all survive the `(len N)' announce)
    M_WRLATCH   34/36  latch rd rd 2, latch rd wr 2                              old23: 23/23
    M_WIDEKILL  32/36  wide wr, wide wr msg n/a, wide rd, wide rd srvd n/a       old23: 23/23
    M_OFFKILL   34/36  inword wr, inword rd (host exit1 at 0x06)                 old23: 23/23
    M_SRVD0     35/36  srvd val text 0  (wide rd srvd stays: it IS 0x00 there)   old23: 23/23 (Opus measured)
    M_BACKED2   35/36  sameoff val 0x5a                                          old23: 23/23 (Opus measured)
    M_ABA       35/36  latch aba 3                                               old23: 23/23
    M_EXIT       7/36  the 16 of pass 2 + latch rd rd, latch rd wr, latch aba, sameoff val, srvd val, srvd val text,
                       wide wr, wide wr msg, wide rd, wide rd srvd, inword rd, unnamed rd, wr declined (29 red)
    M_UNLATCH   30/36  latch sameoff 2, latch rw one 2, latch rd rd 2, latch rd wr 2, latch aba 3, wide wr msg 2
    M_ONELATCH  31/36  named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1, latch aba 1
    M_BACKED    32/36  ieicr rdawr 0x5a, ieerr rdawr 0x5a, sameoff val 0x5a, wide wr 0x5a5a5a5a
    M_RDKILL    17/36  the seven of pass 2 (named rd, named rd msg, named rd srvd, dir rd text, latch rw one, ieicr
                       rdawr, ieerr rdawr) + latch sameoff (its session now ends in a read), sameoff val, latch rd rd,
                       latch rd wr, srvd val, srvd val text, wide wr, wide wr msg, wide rd, wide rd srvd, inword rd,
                       unnamed rd -- nineteen
    M_DIRSWAP   30/36  dir wr text 0, dir rd text 0, named rd srvd 0, srvd val text 0, wide rd srvd 0, wr declined 0
  A miss in the SAFE direction is recorded; one in the UNSAFE direction (a predicted red that stays green) stops the
  round.  A pass-2 mutant NOT at 23/23 on the old instrument is a wrong breach claim and is recorded as such.
  Written 2026-09-05 06:25:42.
```

Gate 14 (`killtable3_20260905/gate14_501b.log`, run alone): pcc2 default rows emitted 36, green 36; pcc2 width
rows emitted 251, green 251; GATE_RC=0.

## SECTION F2 -- THE PASS-2 DISPOSITIONS, numbered (the adjudication the panel shares)

ACCEPTED, REPAIRED IN-ROUND (L1: the detector was uncommitted)
 1. (opus5, MEASURED) M_O1 -- the announced value unpinned.  Row `srvd val text`; the product now prints data[0].
 2. (opus5, MEASURED) M_O2 -- the disposition on the latched path unpinned.  Row `sameoff val` (the existing session
    gains a read-back; zero new sessions).
 3. (grok) A -- latch SET conditioned on writes.  Rows `latch rd rd`, `latch rd wr` (the two setter x tester cells).
 4. (grok) B -- `len != 1` re-kill.  Rows `wide wr` (+msg), `wide rd` (+srvd).  The pass-1 PRETABLE's own
    "byte-and-wide" sentence had no row -- a CLAIM->ROW miss of the pre-table block itself.
 5. (codex) `|=` -> `=`.  Row `latch aba`.
 6. (fable5) a re-kill at an unsampled offset.  `inword`/`unnamed` rows now drive all 43 offsets both ways
    (2 new read rows).  Fable filed it as coverage debt; taking it in-round costs two sessions and closes the axis.
 7. (codex) the read announce RELOADS the array after the response was copied -- a PRODUCT defect for the twelve
    interiors the tick rewrites.  Fixed: data[0].  (Also makes "the array's default, not a computed value" false for
    those twelve -- corrected in comment and docstring.)
 8. (deepseek, grok, opus5, codex) the announce under-describes a wide access -> `(len %d)` in both announces;
    rows `wide wr msg`, `wide rd srvd` pin the label.
 9. L4s, corrected in place: kill-table header md5 (grok, codex, opus5); "three predictions exact" (fable5, codex,
    opus5); the M_EXIT diagnosis -- the 16-row SET was right, the numeral wrong (opus5, codex, kimi); "would have
    shipped green" -- the gate FAILED 25/844 and caught it (codex); `alias 0x6a` row vs docstring (grok); `unnamed wr`
    overrun note (grok); "four arms up" (grok); "no guest reaches" (codex); "unnamed" = the fork header (codex).
10. (opus5) "the arm can only add output where the old code called exit(1), so no boot that works today can
    regress" -- adopted as the safety sentence of the record.

REJECTED / NOT CREDITED
11. (minimax) the M_RDKILL prediction miss labelled "unsafe" -- a predicted-GREEN row that went RED is the SAFE
    direction by the round's own rule.
12. (kimi, glm, deepseek, minimax; fable5 GO-WITH-CHANGES) PASS on the 23-row instrument -- overtaken by the two
    MEASURED sweeps.  Not a seat failure: a reading that did not build the edit.  Recorded by name.
13. (grok, codex) a per-instance latch fixture -- `pcc2latchinst`, filed at pass 1, unchanged.
14. (opus5) there is no mvme88k boot rig, so gate 14's two probes are this device's entire coverage -- true, a
    queue fact, not this round's.

## QUESTIONS

1. **IS THE REPAIR RIGHT?**  The arm (inlined, every exit path): is `data[0]` always the byte the guest received --
   on the memcpy path AND the end-span zero-fill path; for a WRITE is `data` unused by the announce (it prints idata);
   does `(int) len` fit; does any row's text anchor break (`offset 0x2a`, `served 0x`, the direction phrases, MSG)?
2. **DOES EACH OF THE TWELVE MUTANTS DIE FOR THE REASON CLAIMED?**  Table 3 and its predictions are inlined; the six
   pass-2 mutants carry a second score on the pass-2 instrument (23/23 owed = the breach).  A prediction that missed
   is the interesting case; a mutant killed by a row OTHER than the one built for it is a row killing by accident.
3. **THE CLOSURE**: setter x tester (four cells), accumulation, latched-path disposition, served value, width both
   directions, every offset both directions.  Is any cell still open?  Name the mutant.  Is anything in the
   DISCLOSED list actually floor (a predicate the arm tests)?
4. **THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 36 ROWS.**  Name the row you expect to stay green and why.
   (Opus: the two pass-2 escapes were found by BUILDING; a derived escape is a prediction until measured.)
5. **IS THE RECORD HONEST?**  The CHANGELOG block (pass 2 + repair sections inlined), the contract (docstring), the
   pass-3 PRETABLE.  Name any sentence a measurement refutes, any count without a deriver.
6. **CLOSE?**  A closing zero must be VALID: the diff delivered (inlined), the roster complete or misses named, the
   zero carried WITH its denominator -- which mutant shapes (twelve, named), which cells.  If you say close, say
   what the denominator EXCLUDES.

If, while verifying a claim, you found something ELSE -- say so.

## THE PRODUCT REPAIR DIFF (pass-2 state -> now, VERBATIM)

```diff
--- GXEMUL-SEC/regress/artifacts/pcc2defaultkill/killtable_20260905/dev_pcc2.pass2.c	2026-09-05 06:27:41.062291000 -0500
+++ GXEMUL-SEC/src/devices/dev_pcc2.c	2026-09-05 06:25:42.901877900 -0500
@@ -670,14 +670,15 @@
 		    ones -- READS included, though the memcpy above the switch had
 		    already served them.  A guest ld.bu or st.b at any of them was a host
 		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
-		    default, said so -- not a computed value); a WRITE is DECLINED.  Not a
+		    current byte, said so -- for a counter interior that is the tick's
+		    value, not a default); a WRITE is DECLINED.  Not a
 		    backed store: the cased siblings contradict one (SCCERR clears on
 		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
-		    read-only), no guest reaches these offsets on this model (if_ie never
+		    read-only), no inspected OpenBSD driver path reaches them (if_ie never
 		    attaches: unreadable sits at its 82596 address), and a store from the
 		    one arm 43 offsets reach would add a bounded-write surface.  One
 		    latched fatal() per offset per instance, the house `(once)' shape --
-		    unlike PSCALEADJ's UNLATCHED print four arms up (pcc2pscaleflood).  The
+		    unlike PSCALEADJ's UNLATCHED print above (pcc2pscaleflood).  The
 		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
 		    the SCCRXIACK shape) would open two new entries into the C040 path,
 		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
@@ -687,13 +688,15 @@
 			d->warned_unimpl |= 1ULL << relative_addr;
 			if (writeflag == MEM_WRITE)
 				fatal("[ pcc2: unimplemented write to offset "
-				    "0x%x: 0x%x -- declined.  (once) ]\n",
-				    (int) relative_addr, (int) idata);
+				    "0x%x (len %d): 0x%x -- declined.  (once) ]\n",
+				    (int) relative_addr, (int) len, (int) idata);
 			else
+				/*  data[0] is the byte actually SERVED; a reload of the
+				    array here could differ (the tick rewrites the
+				    counter interiors), and a wide read is labelled.  */
 				fatal("[ pcc2: unimplemented read from offset "
-				    "0x%x -- served 0x%02x.  (once) ]\n",
-				    (int) relative_addr,
-				    d->pcctwo_reg[relative_addr]);
+				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
+				    (int) relative_addr, (int) len, data[0]);
 		}
 		break;
 	}

```

## THE ARM AS IT NOW STANDS (from `default:` to the handler's `return 1`, VERBATIM)

```c
	default:
		/*  #501 (pcc2defaultkill): this arm ended the host with exit(1) on ANY
		    access to an offset with no case -- 43 of the 0x40 byte offsets:
		    eighteen documented registers the model does not implement (IEICR,
		    IEERR, IEBERR, GPIO, SCSIERR, the printer block, SPEED, the *IACKs),
		    the bytes inside the four counter/compare words, and the unnamed
		    ones -- READS included, though the memcpy above the switch had
		    already served them.  A guest ld.bu or st.b at any of them was a host
		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
		    current byte, said so -- for a counter interior that is the tick's
		    value, not a default); a WRITE is DECLINED.  Not a
		    backed store: the cased siblings contradict one (SCCERR clears on
		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
		    read-only), no inspected OpenBSD driver path reaches them (if_ie never
		    attaches: unreadable sits at its 82596 address), and a store from the
		    one arm 43 offsets reach would add a bounded-write surface.  One
		    latched fatal() per offset per instance, the house `(once)' shape --
		    unlike PSCALEADJ's UNLATCHED print above (pcc2pscaleflood).  The
		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
		    the SCCRXIACK shape) would open two new entries into the C040 path,
		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
		    Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as repeated
		    PCCchip2 registers.  */
		if (!(d->warned_unimpl & (1ULL << relative_addr))) {
			d->warned_unimpl |= 1ULL << relative_addr;
			if (writeflag == MEM_WRITE)
				fatal("[ pcc2: unimplemented write to offset "
				    "0x%x (len %d): 0x%x -- declined.  (once) ]\n",
				    (int) relative_addr, (int) len, (int) idata);
			else
				/*  data[0] is the byte actually SERVED; a reload of the
				    array here could differ (the tick rewrites the
				    counter interiors), and a wide read is labelled.  */
				fatal("[ pcc2: unimplemented read from offset "
				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
				    (int) relative_addr, (int) len, data[0]);
		}
		break;
	}

	return 1;
```

## THE DETECTOR REPAIR DIFF (pass-2 instrument -> now, VERBATIM)

```diff
--- GXEMUL-SEC/regress/artifacts/pcc2defaultkill/killtable_20260905/frozen_probe.py	2026-09-05 05:18:54.696856900 -0500
+++ GXEMUL-SEC/regress/pcc2_default_probe.py	2026-09-05 06:25:42.903778500 -0500
@@ -10,34 +10,53 @@
 (rung-3 witness, 7/13 on the committed build: regress/artifacts/pcc2defaultkill/witness_20260905/).
 
 THE FIX (pass-1 panel of 2026-09-05, nine seats, converged): READ side -- keep the byte the memcpy
-already served (it is the register array's default, NOT a computed value: the announce says so);
+already served (the register array's CURRENT byte -- the tick's, for a counter interior: the announce says so);
 WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
 accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
 mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
-reaches these offsets on this model -- if_ie never attaches), and a store into pcctwo_reg[] from the
+reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
 one arm reached by 43 offsets adds a bounded-write surface the decline does not have.
 
-CONTRACT -- what this detector is built to catch, by row:
-  (b) the verbatim `exit(1)' reinstated             -> every survival row (named wr/rd, inword, unnamed, alias)
+CONTRACT -- what this detector is built to catch, by row (36 rows; the 13 added by the pass-2 repair are marked +):
+  (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
   (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
   (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
+  (d) the latch SET conditioned on writes (grok A)  -> + `latch rd rd' (2, not 1), + `latch rd wr' (2, not 1): with
+      `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
+  (d) `|=' -> `=' at the latch update (codex)       -> + `latch aba' (3, not 2): bits already set survive a new offset
   (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
-  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text'
-  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored
-      byte (0x5a) instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear
-      sibling) is the control that reads 0x0 under either and makes the delta attributable
+  (d) a `len != 1' re-kill -- the removed kill was width-agnostic, so this is a partial reinstatement (grok B)
+                                                    -> + `wide wr' / + `wide rd' (host exit)
+  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' now drive all 12 / all 13, and
+                                                       + `inword rd' / + `unnamed rd' read them: every one of the 43
+                                                       uncased offsets is written once and read once
+  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / + `wr declined'
+  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
+      instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
+      control that reads 0x0 under either and makes the delta attributable
+  member 6 on the LATCHED path only (Opus M_O2: a store exempting the first write per offset -- MEASURED 23/23 on
+      the 23-row instrument)                        -> + `sameoff val' (0x5a, not 0x0)
+  the read announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23: `named rd srvd' counts the
+      phrase, not the value)                        -> + `srvd val text' (`served 0x34' absent); + `srvd val' pins
+      the served byte itself as one the GUEST wrote (through the cased T1CMP word arm), not a default
+  the announce omitting the access width            -> + `wide wr msg' / + `wide rd srvd' (`(len 4)')
   the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
   the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
-DISCLOSED, not caught: the in-word bytes are the interior of IMPLEMENTED counters, declined here as a
-width/alignment matter (pcc2widecompose's business), not as unimplemented registers; the fold of
-0x40..0xfff onto 0x00..0x3f IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as
-'PCCchip2 Registers  Repeated' (_scratchpad/vmesbcp2.txt:4629, fetched at the codex seat's citation -- two
-seats had rightly called it unestablished before the manual was on disk), so `alias 0x6a' pins a documented
-behaviour; the fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things;
-the IACK offsets 0x23/0x25 are declined like the rest -- modelling them (on the SCCRXIACK shape) would
-open two new entries into the C040 path, so pcc2c040kill goes first; `named wr'/`named rd' touch all
-eighteen offsets in ONE session each (valid because the fix has no per-offset branch; `named wr msg'
-localises a failure) -- if a later round branches per offset this compression is invalid.
+DISCLOSED, not caught: half-word (len 2) default accesses (the mutant that kills len 4 also kills len 2; one that
+kills ONLY len 2 is not rowed); an END-SPANNING wide read (0x3d + 4 > 0x40) takes the zero-fill path and is announced
+`served 0x00' truthfully (data[0] is what was served) but no row drives it; the announce names the FIRST served byte
+of a wide read, labelled with the width; the in-word bytes are the interior of IMPLEMENTED counters, declined here
+as a width/alignment matter (pcc2widecompose's business) -- and their served byte is the tick's, not a default,
+which is why the announce prints data[0] rather than reloading the array; the fold of 0x40..0xfff onto 0x00..0x3f
+IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated'
+(_scratchpad/vmesbcp2.txt:4629; two seats had rightly called it unestablished before the manual was on disk); the
+fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things; the IACK offsets 0x23/0x25 are
+declined like the rest -- modelling them (on the SCCRXIACK shape) would open two new entries into the C040 path, so
+pcc2c040kill goes first; `named wr'/`named rd' touch all eighteen offsets in ONE session each (valid because the
+fix has no per-offset branch; the count rows are AGGREGATES, so a per-offset failure is located by reading the
+log, not by a row) -- if a later round branches per offset this compression is invalid; "unnamed" means the FORK
+HEADER has no label, not that the part is undocumented (0x39 is SPEED's second byte, 0x3b PRTDATA's low byte);
+per-instance latch scope is not provable by fresh sessions (each is a new process; `pcc2latchinst').
 The debugger's `put b' never reaches a DM_DEFAULT arm (measured): `put b ctl' is a control, not a witness.
 
 Usage: python3 pcc2_default_probe.py <gxemul> <label>      Sentinel: PCC2D_PROBE_DONE
@@ -58,8 +77,9 @@
 CHIPID, GENCTL, T1CMP, SCCERR = 0x00, 0x02, 0x04, 0x1c
 IEERR, IEICR, IEBERR, SCCTXIACK, PRTICR = 0x28, 0x2a, 0x2b, 0x25, 0x30
 NAMED18 = [0x14, 0x18, 0x19, 0x23, 0x25, 0x28, 0x2a, 0x2b, 0x2c, 0x30, 0x31, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x3a]
-INWORD = [0x05, 0x09, 0x0d, 0x11]
-UNNAMED = [0x20, 0x24, 0x29, 0x35, 0x3d]
+INWORD = [0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0d, 0x0e, 0x0f, 0x11, 0x12, 0x13]   # all 12 counter interiors
+UNNAMED = [0x20, 0x21, 0x22, 0x24, 0x26, 0x29, 0x2d, 0x2e, 0x35, 0x39, 0x3b, 0x3c, 0x3d]   # all 13 the fork header leaves unnamed
+assert len(NAMED18) + len(INWORD) + len(UNNAMED) == 43 and len(set(NAMED18 + INWORD + UNNAMED)) == 43
 MSG = "pcc2: unimplemented"
 def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
 def LD_BU(rd, off): return enc(0x03, rd, 2, off)
@@ -94,15 +114,19 @@
 # -- the eighteen named unimplemented registers, one session each direction
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in NAMED18]))
 row("named wr", fate(alive, how), "survived", "guest st.b at all 18 named unimplemented registers in ONE session: (b) reinstated exit(1) kills on the first")
-row("named wr msg", t.count(MSG) if alive else "n/a", 18, "one announce PER OFFSET: a whole-arm latch prints 1, an unlatched arm prints 18 too -- see `latch sameoff'")
+row("named wr msg", t.count(MSG) if alive else "n/a", 18, "one announce PER OFFSET: a whole-arm latch prints 1, an unlatched arm prints 18 too -- see `latch sameoff' (an aggregate count, not a locator)")
 t, alive, how = session(setup() + program([LD_BU(4, o) for o in NAMED18]))
 row("named rd", fate(alive, how), "survived", "guest ld.bu at all 18 in one session: the READ side of the defect; a writeflag guard that re-kills reads dies here")
 row("named rd msg", t.count(MSG) if alive else "n/a", 18, "the read announce fires once per offset too")
-row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED (the array's byte), never 'ignored'")
+row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED, never 'ignored' (the VALUE is pinned by `srvd val text')")
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD]))
-row("inword wr", fate(alive, how), "survived", "a byte inside each 32-bit counter/compare word (0x05, 0x09, 0x0d, 0x11): no case -> default:")
+row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
+t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
+row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED]))
-row("unnamed wr", fate(alive, how), "survived", "unnamed offsets 0x20, 0x24, 0x29, 0x35, 0x3d -- 0x3d is the one a backed store at len 4 would overrun")
+row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
+t, alive, how = session(setup() + program([LD_BU(4, o) for o in UNNAMED]))
+row("unnamed rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the thirteen: with named rd + inword rd every one of the 43 is read once")
 # -- the disposition-pinning rows: read-after-write in ONE session
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
 row("ieicr rdawr", val(t, alive, how), "0x0", "st.b 0x5a then ld.bu at IEICR in ONE session reads 0x0: the write was DECLINED (a backed accept reads 0x5a)")
@@ -111,20 +135,39 @@
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, SCCERR), LD_BU(4, SCCERR)]) + ["print r4"])
 row("sccerr rdawr", val(t, alive, how), "0x0", "CONTROL: the CASED write-to-clear sibling reads 0x0 under either disposition -- makes the two rows above attributable")
 # -- the latch: per offset, per instance
-t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEICR)]))
-row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 2")
+t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
+row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 2 (the read-back is silent: bit set)")
+row("sameoff val", val(t, alive, how), "0x0", "...and the SECOND write (latch already set) is declined too: a store exempting the first write reads 0x5a (Opus M_O2, MEASURED 23/23 escape)")
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR)]))
 row("latch twooff", t.count(MSG) if alive else "n/a", 2, "two offsets announce TWICE: a single whole-arm latch bit prints 1")
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]))
-row("latch rw one", t.count(MSG) if alive else "n/a", 1, "a write then a read at ONE offset announce once: the latch is per offset, not per direction")
+row("latch rw one", t.count(MSG) if alive else "n/a", 1, "a write then a read at ONE offset announce once: the WRITE sets the bit the READ tests")
+t, alive, how = session(setup() + program([LD_BU(4, IEICR), LD_BU(4, IEICR)]))
+row("latch rd rd", t.count(MSG) if alive else "n/a", 1, "two READS at one offset announce once: a latch SET only on writes prints 2 (grok A) -- the setter x tester cell rw one cannot see")
+t, alive, how = session(setup(r5="0x5a") + program([LD_BU(4, IEICR), ST_B(5, IEICR)]))
+row("latch rd wr", t.count(MSG) if alive else "n/a", 1, "a READ then a write at one offset announce once: the read's bit silences the write (the fourth setter x tester cell)")
+t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR), ST_B(5, IEICR)]))
+row("latch aba", t.count(MSG) if alive else "n/a", 2, "A,B,A announces TWICE: `|=' -> `=' forgets A when B announces and prints 3 (codex) -- earlier bits survive a new offset")
 # -- the fold and the text
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, 0x6a)]))
-row("alias 0x6a", fate(alive, how), "survived", "0x6a folds onto 0x2a (`relative_addr %= PCC2_SIZE'): the MODEL's fold, not proven of the real part")
+row("alias 0x6a", fate(alive, how), "survived", "0x6a folds onto 0x2a (`relative_addr %= PCC2_SIZE'): the real part's fold too (VMESBCP2 Table 6-1, `Repeated')")
 row("alias msg", t.count("offset 0x2a") if alive else "n/a", 1, "...and the announce names the FOLDED offset 0x2a: a changed fold names another")
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, PRTICR)]))
 row("dir wr text", t.count("unimplemented write to") if alive else "n/a", 1, "the announce says WRITE for a store (an inverted writeflag test in the text says read)")
+row("wr declined", t.count("declined") if alive else "n/a", 1, "...and the word is DECLINED (no other row counts it: `ignored' would pass every count row)")
 t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
 row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
+# -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
+t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_BU(4, 0x05)]) + ["print r4"])
+row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
+row("srvd val text", t.count("served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served): `served 0x%02x' of 0 passes `named rd srvd' (Opus M_O1, MEASURED)")
+# -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
+t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
+row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
+row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
+t, alive, how = session(setup() + program([LD_W(4, PRTICR)]) + ["print r4"])
+row("wide rd", val(t, alive, how), "0x0", "a guest ld.w at PRTICR (0x30..0x33, all uncased) survives and is served the four zero bytes")
+row("wide rd srvd", t.count("(len 4) -- served 0x00") if alive else "n/a", 1, "...and the announce names the width and the first served byte")
 # -- the cased arms are untouched
 t, alive, how = session(setup(r5="0x82") + program([ST_B(5, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
 row("genctl rt", val(t, alive, how), "0x82", "an IMPLEMENTED byte register still round-trips (no C040 bit in 0x82)")

```

## THE DETECTOR (`regress/pcc2_default_probe.py`, VERBATIM, contract included)

```python
#!/usr/bin/env python3
"""pcc2defaultkill DETECTOR (#501) -- the `default:' arm of DEVICE_ACCESS(pcc2) in dev_pcc2.c.

Before #501 that arm ended the emulator process (`exit(1)') on ANY access to an offset with no `case'
-- READS included, although the memcpy above the switch had already served them.  Forty-three of the
0x40 byte offsets reach it (derived from mvme_pcctworeg.h against the case list): eighteen NAMED
registers the model does not implement (PSCALECNT, GPIO_ICR/PCR, SCCMOIACK, SCCTXIACK, IEERR, IEICR,
IEBERR, SCSIERR, the printer block, SPEED, PRTDATA), the bytes INSIDE the four 32-bit counter/compare
words, and the unnamed offsets.  A single guest `st.b' or `ld.bu' at any of them was a host kill
(rung-3 witness, 7/13 on the committed build: regress/artifacts/pcc2defaultkill/witness_20260905/).

THE FIX (pass-1 panel of 2026-09-05, nine seats, converged): READ side -- keep the byte the memcpy
already served (the register array's CURRENT byte -- the tick's, for a counter interior: the announce says so);
WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
one arm reached by 43 offsets adds a bounded-write surface the decline does not have.

CONTRACT -- what this detector is built to catch, by row (36 rows; the 13 added by the pass-2 repair are marked +):
  (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
  (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
  (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
  (d) the latch SET conditioned on writes (grok A)  -> + `latch rd rd' (2, not 1), + `latch rd wr' (2, not 1): with
      `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
  (d) `|=' -> `=' at the latch update (codex)       -> + `latch aba' (3, not 2): bits already set survive a new offset
  (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
  (d) a `len != 1' re-kill -- the removed kill was width-agnostic, so this is a partial reinstatement (grok B)
                                                    -> + `wide wr' / + `wide rd' (host exit)
  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' now drive all 12 / all 13, and
                                                       + `inword rd' / + `unnamed rd' read them: every one of the 43
                                                       uncased offsets is written once and read once
  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / + `wr declined'
  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
      instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
      control that reads 0x0 under either and makes the delta attributable
  member 6 on the LATCHED path only (Opus M_O2: a store exempting the first write per offset -- MEASURED 23/23 on
      the 23-row instrument)                        -> + `sameoff val' (0x5a, not 0x0)
  the read announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23: `named rd srvd' counts the
      phrase, not the value)                        -> + `srvd val text' (`served 0x34' absent); + `srvd val' pins
      the served byte itself as one the GUEST wrote (through the cased T1CMP word arm), not a default
  the announce omitting the access width            -> + `wide wr msg' / + `wide rd srvd' (`(len 4)')
  the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
  the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
DISCLOSED, not caught: half-word (len 2) default accesses (the mutant that kills len 4 also kills len 2; one that
kills ONLY len 2 is not rowed); an END-SPANNING wide read (0x3d + 4 > 0x40) takes the zero-fill path and is announced
`served 0x00' truthfully (data[0] is what was served) but no row drives it; the announce names the FIRST served byte
of a wide read, labelled with the width; the in-word bytes are the interior of IMPLEMENTED counters, declined here
as a width/alignment matter (pcc2widecompose's business) -- and their served byte is the tick's, not a default,
which is why the announce prints data[0] rather than reloading the array; the fold of 0x40..0xfff onto 0x00..0x3f
IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated'
(_scratchpad/vmesbcp2.txt:4629; two seats had rightly called it unestablished before the manual was on disk); the
fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things; the IACK offsets 0x23/0x25 are
declined like the rest -- modelling them (on the SCCRXIACK shape) would open two new entries into the C040 path, so
pcc2c040kill goes first; `named wr'/`named rd' touch all eighteen offsets in ONE session each (valid because the
fix has no per-offset branch; the count rows are AGGREGATES, so a per-offset failure is located by reading the
log, not by a row) -- if a later round branches per offset this compression is invalid; "unnamed" means the FORK
HEADER has no label, not that the part is undocumented (0x39 is SPEED's second byte, 0x3b PRTDATA's low byte);
per-instance latch scope is not provable by fresh sessions (each is a new process; `pcc2latchinst').
The debugger's `put b' never reaches a DM_DEFAULT arm (measured): `put b ctl' is a control, not a witness.

Usage: python3 pcc2_default_probe.py <gxemul> <label>      Sentinel: PCC2D_PROBE_DONE
The pty session helper is the width probe's own (extracted at run time), never hand-rolled: a first
draft of the witness hand-rolled it and read every host kill as "survived".
"""
import io, os, pty, re, select, sys, time
BIN = sys.argv[1] if len(sys.argv) > 1 else "build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/pcc2_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 4096)
HERE = os.path.dirname(os.path.abspath(__file__))
_w = io.open(os.path.join(HERE, "pcc2_width_probe.py"), encoding="utf-8").read()
exec(_w[_w.index("def session("):_w.index("\ndef printed")])     # session(cmds) -> (transcript, alive, how)

CODE, SCRATCH, PCC2, SENTINEL = 0x00010000, 0x00020000, 0xfff42000, 0xdeadbeef
CHIPID, GENCTL, T1CMP, SCCERR = 0x00, 0x02, 0x04, 0x1c
IEERR, IEICR, IEBERR, SCCTXIACK, PRTICR = 0x28, 0x2a, 0x2b, 0x25, 0x30
NAMED18 = [0x14, 0x18, 0x19, 0x23, 0x25, 0x28, 0x2a, 0x2b, 0x2c, 0x30, 0x31, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x3a]
INWORD = [0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0d, 0x0e, 0x0f, 0x11, 0x12, 0x13]   # all 12 counter interiors
UNNAMED = [0x20, 0x21, 0x22, 0x24, 0x26, 0x29, 0x2d, 0x2e, 0x35, 0x39, 0x3b, 0x3c, 0x3d]   # all 13 the fork header leaves unnamed
assert len(NAMED18) + len(INWORD) + len(UNNAMED) == 43 and len(set(NAMED18 + INWORD + UNNAMED)) == 43
MSG = "pcc2: unimplemented"
def enc(op26, rd, rs1, imm): return (op26 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)
def LD_BU(rd, off): return enc(0x03, rd, 2, off)
def LD_W(rd, off): return enc(0x05, rd, 2, off)
def ST_B(rs, off): return enc(0x0b, rs, 2, off)
def ST_W(rs, off): return enc(0x09, rs, 2, off)
I_ST_SCR = enc(0x09, 5, 3, 0); I_LD_SCR = enc(0x05, 4, 3, 0); I_BR_SELF = 0xc0000000
def program(insns, at=CODE):
    words = list(insns) + [I_BR_SELF, 0]
    return ["put w 0x%x, 0x%08x" % (at + 4 * k, w) for k, w in enumerate(words)] + ["pc=0x%x" % at, "step %d" % len(insns)]
def setup(r5="0x5a5a5a5a"):
    return ["r2=0x%x" % PCC2, "r3=0x%x" % SCRATCH, "r5=%s" % r5, "r4=0x%x" % SENTINEL]
def printed(t, reg="r4"):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%x" % int(m.group(1), 16) if m else "absent"
def fate(alive, how): return "survived" if alive else "host " + how
def val(t, alive, how): return printed(t) if alive else fate(alive, how)
rows, bad = [], []
def row(name, got, want, why):
    ok = str(got) == str(want)
    rows.append(name); (None if ok else bad.append(name))
    #  STATUS LAST: gate 14 counts a row with `^<name>  .*ok$' / ` ok$' / ` FAIL$' -- a first draft printed the
    #  status before the note and the gate counted ZERO of 23 rows while the probe said DONE (caught by the gate, L1).
    print("%-16s %-14s %-14s %-60s %s" % (name, got, want, why[:60], "ok" if ok else "FAIL"), flush=True)
print("pcc2defaultkill DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-16s %-14s %-14s %-60s %s" % ("row", "got", "want", "note", ""))

t, alive, how = session(setup() + program([I_ST_SCR, I_LD_SCR]) + ["print r4"])
row("live", val(t, alive, how), "0x5a5a5a5a", "LIVENESS: scratch RAM st/ld round-trip")
t, alive, how = session(setup() + program([LD_BU(4, CHIPID)]) + ["print r4"])
row("devsig chipid", val(t, alive, how), "0x20", "DEVICE-SIGNATURE: CHIPID reads PCC2_ID through a guest ld.bu (RAM would read 0)")
# -- the eighteen named unimplemented registers, one session each direction
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in NAMED18]))
row("named wr", fate(alive, how), "survived", "guest st.b at all 18 named unimplemented registers in ONE session: (b) reinstated exit(1) kills on the first")
row("named wr msg", t.count(MSG) if alive else "n/a", 18, "one announce PER OFFSET: a whole-arm latch prints 1, an unlatched arm prints 18 too -- see `latch sameoff' (an aggregate count, not a locator)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in NAMED18]))
row("named rd", fate(alive, how), "survived", "guest ld.bu at all 18 in one session: the READ side of the defect; a writeflag guard that re-kills reads dies here")
row("named rd msg", t.count(MSG) if alive else "n/a", 18, "the read announce fires once per offset too")
row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED, never 'ignored' (the VALUE is pinned by `srvd val text')")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD]))
row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED]))
row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in UNNAMED]))
row("unnamed rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the thirteen: with named rd + inword rd every one of the 43 is read once")
# -- the disposition-pinning rows: read-after-write in ONE session
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
row("ieicr rdawr", val(t, alive, how), "0x0", "st.b 0x5a then ld.bu at IEICR in ONE session reads 0x0: the write was DECLINED (a backed accept reads 0x5a)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEERR), LD_BU(4, IEERR)]) + ["print r4"])
row("ieerr rdawr", val(t, alive, how), "0x0", "the same at IEERR (0x28), the write-to-clear class whose cased sibling SCCERR clears on write")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, SCCERR), LD_BU(4, SCCERR)]) + ["print r4"])
row("sccerr rdawr", val(t, alive, how), "0x0", "CONTROL: the CASED write-to-clear sibling reads 0x0 under either disposition -- makes the two rows above attributable")
# -- the latch: per offset, per instance
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEICR), LD_BU(4, IEICR)]) + ["print r4"])
row("latch sameoff", t.count(MSG) if alive else "n/a", 1, "two writes to one offset announce ONCE: an unlatched arm prints 2 (the read-back is silent: bit set)")
row("sameoff val", val(t, alive, how), "0x0", "...and the SECOND write (latch already set) is declined too: a store exempting the first write reads 0x5a (Opus M_O2, MEASURED 23/23 escape)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR)]))
row("latch twooff", t.count(MSG) if alive else "n/a", 2, "two offsets announce TWICE: a single whole-arm latch bit prints 1")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), LD_BU(4, IEICR)]))
row("latch rw one", t.count(MSG) if alive else "n/a", 1, "a write then a read at ONE offset announce once: the WRITE sets the bit the READ tests")
t, alive, how = session(setup() + program([LD_BU(4, IEICR), LD_BU(4, IEICR)]))
row("latch rd rd", t.count(MSG) if alive else "n/a", 1, "two READS at one offset announce once: a latch SET only on writes prints 2 (grok A) -- the setter x tester cell rw one cannot see")
t, alive, how = session(setup(r5="0x5a") + program([LD_BU(4, IEICR), ST_B(5, IEICR)]))
row("latch rd wr", t.count(MSG) if alive else "n/a", 1, "a READ then a write at one offset announce once: the read's bit silences the write (the fourth setter x tester cell)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, IEICR), ST_B(5, IEBERR), ST_B(5, IEICR)]))
row("latch aba", t.count(MSG) if alive else "n/a", 2, "A,B,A announces TWICE: `|=' -> `=' forgets A when B announces and prints 3 (codex) -- earlier bits survive a new offset")
# -- the fold and the text
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, 0x6a)]))
row("alias 0x6a", fate(alive, how), "survived", "0x6a folds onto 0x2a (`relative_addr %= PCC2_SIZE'): the real part's fold too (VMESBCP2 Table 6-1, `Repeated')")
row("alias msg", t.count("offset 0x2a") if alive else "n/a", 1, "...and the announce names the FOLDED offset 0x2a: a changed fold names another")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, PRTICR)]))
row("dir wr text", t.count("unimplemented write to") if alive else "n/a", 1, "the announce says WRITE for a store (an inverted writeflag test in the text says read)")
row("wr declined", t.count("declined") if alive else "n/a", 1, "...and the word is DECLINED (no other row counts it: `ignored' would pass every count row)")
t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
# -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_BU(4, 0x05)]) + ["print r4"])
row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
row("srvd val text", t.count("served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served): `served 0x%02x' of 0 passes `named rd srvd' (Opus M_O1, MEASURED)")
# -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
t, alive, how = session(setup() + program([LD_W(4, PRTICR)]) + ["print r4"])
row("wide rd", val(t, alive, how), "0x0", "a guest ld.w at PRTICR (0x30..0x33, all uncased) survives and is served the four zero bytes")
row("wide rd srvd", t.count("(len 4) -- served 0x00") if alive else "n/a", 1, "...and the announce names the width and the first served byte")
# -- the cased arms are untouched
t, alive, how = session(setup(r5="0x82") + program([ST_B(5, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
row("genctl rt", val(t, alive, how), "0x82", "an IMPLEMENTED byte register still round-trips (no C040 bit in 0x82)")
t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_W(4, T1CMP)]) + ["print r4"])
row("t1cmp word rt", val(t, alive, how), "0x12345678", "the cased 32-bit counter arm still round-trips a word: the fix swallowed no cased arm")
t, alive, how = session(["put b 0xfff4202a, 0x00"])
row("put b ctl", fate(alive, how), "survived", "CONTROL: the debugger's put b never reaches a DM_DEFAULT arm (measured before the fix too)")
row("put b ctl msg", t.count(MSG) if alive else "n/a", 0, "...so it prints nothing -- not a witness, a control")
print("PCC2D_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("PCC2D_RED=%s" % ",".join(bad))
print("PCC2D_PROBE_DONE")

```

## THE GATE SECTION (`git diff -- regress/gate_arm.sh`, VERBATIM; the whole #501 section is new against HEAD)

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index 65930c2..c542455 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1303,6 +1303,31 @@ else
 fi
 
 
+#  ------------------------------------------------------------ pcc2defaultkill (#501)
+#  The default: arm of DEVICE_ACCESS(pcc2) ended the host on any access to an uncased
+#  offset, reads included.  Now: reads keep the served byte, writes are declined, one
+#  latched announce per offset per instance.  The witness (regress/artifacts/pcc2defaultkill/
+#  witness_20260905/, 7/13 on the committed build) is NOT run here; this is its detector.
+PCC2DLOG=$LOGDIR/pcc2_default.log
+python3 -u pcc2_default_probe.py "$PMAX" gate > "$PCC2DLOG" 2>&1 || true
+if ! grep -q "PCC2D_PROBE_DONE" "$PCC2DLOG"; then
+    check "pcc2 default probe completed" "no" "yes"
+else
+    check "pcc2 default probe completed" "yes" "yes"
+    for v in "live" "devsig chipid" "named wr" "named wr msg" "named rd" "named rd msg" \
+        "named rd srvd" "inword wr" "inword rd" "unnamed wr" "unnamed rd" "ieicr rdawr" \
+        "ieerr rdawr" "sccerr rdawr" "latch sameoff" "sameoff val" "latch twooff" "latch rw one" \
+        "latch rd rd" "latch rd wr" "latch aba" "alias 0x6a" "alias msg" "dir wr text" \
+        "wr declined" "dir rd text" "srvd val" "srvd val text" "wide wr" "wide wr msg" \
+        "wide rd" "wide rd srvd" "genctl rt" "t1cmp word rt" "put b ctl" "put b ctl msg"; do
+        check "pcc2 default row: $v" "$(count "$PCC2DLOG" "^$v  .*ok$")" "1"
+    done
+    check "pcc2 default rows emitted" "$(( $(count "$PCC2DLOG" " ok$") + $(count "$PCC2DLOG" " FAIL$") ))" "36"
+    check "pcc2 default rows green"   "$(count "$PCC2DLOG" " ok$")"   "36"
+    check "pcc2 default rows red"     "$(count "$PCC2DLOG" " FAIL$")" "0"
+fi
+
+
 PITLOG=$LOGDIR/pit8253_latch.log
 python3 pit8253_latch_probe.py "$PMAX" "$STUB" > "$PITLOG" 2>&1 || true
 

```

## THE CHANGELOG BLOCK (as it stands)

```
# Round #501 pcc2defaultkill -- the `default:` arm of DEVICE_ACCESS(pcc2) ended the host on any access to an uncased offset, reads included; now reads keep the served byte and writes are declined, one latched announce per offset

**2026-09-05.  HIGH, ranked first by the 2026-09-04 fix-review adjudication.  Product change: `src/devices/dev_pcc2.c`
-- the `exit(1)` replaced by a per-offset latched `fatal()` (`uint64_t warned_unimpl`, one bit per byte offset) that
says DECLINED for a write and SERVED 0x%02x for a read, then `break` to the handler's single `return 1`.  Detector:
`regress/pcc2_default_probe.py`, 23 rows, run by gate 14.  Witness: rung 3, measured before the edit.**

## The defect and its witness

Forty-three of the 0x40 byte offsets have no `case` (derived from `mvme_pcctworeg.h` against the 21 labels; two seats
re-derived it): eighteen NAMED registers the model does not implement (PSCALECNT, GPIO_ICR/PCR, SCCMOIACK, SCCTXIACK,
IEERR, IEICR, IEBERR, SCSIERR, the printer block, SPEED, PRTDATA), the twelve bytes INSIDE the four 32-bit
counter/compare words, and thirteen unnamed offsets.  Any access to one of them -- a READ included, although the
memcpy above the switch had already served it -- reached `default:` and `exit(1)`.

**The witness (`regress/artifacts/pcc2defaultkill/witness_20260905/`), measured on the committed build BEFORE the
edit: 7/13.**  A guest `st.b` to IEICR (0x2a) ends the host with exit status 1, the arm's own `pcc2: unimplemented`
line printed first (the arm was reached); a guest `ld.bu` there likewise -- the READ side kills too; IEBERR and the
in-word byte 0x05 and the alias 0x6a kill the same way.  Liveness (the probe's scratch round-trip) and
device-signature (CHIPID reads PCC2_ID 0x20) controls pass.  **The debugger's `put b` does NOT reach the arm** -- it
survives and prints nothing -- which the filing had called the cheapest witness (measured false; corrected).  The
witness script is the width probe's own `session()` helper: a first draft hand-rolled the pty wait, accepted a
STALE prompt, and read every kill as "survived" -- the carrier's rule about hand-rolled pty plumbing, re-learned.
The combined IEBERR/IEERR row measures IEBERR only (the exiting build dies at the first); IEERR's kill follows from
source (codex).  **13/13 on the fixed build.**

## The design (pass 1: nine seats, `_scratchpad/panel_20260905_021751`, converged)

READ: keep the byte the memcpy served and SAY it is served -- it is the register array's default, not a computed
value, so this is not the option set's member 4 and a bounded announce about it is not a wrong record.  WRITE:
member 3, DECLINE + latched announce -- NOT member 6 (backed accept), on three warrants the seats measured or read:
the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear -- the board manual's SCLR bits
read as zero; the ICRs mask and reassert; PSCALECNT/SPEED/the IACKs are read-only); the addition licence is unmet
(no guest reaches these offsets on this model); a store from the one arm 43 offsets reach adds a bounded-write
surface into `pcctwo_reg[]` at 0x3d.  The Opus seat BUILT both candidates in a scratch clone and measured the
13-row witness at 13/13 under BOTH -- disposition-blind -- so the detector carries read-after-write rows in ONE
session (`ieicr rdawr`, `ieerr rdawr`: store 0x5a then load, want 0x0 -- a backed accept reads 0x5a) with the CASED
write-to-clear sibling `sccerr rdawr` as the control that reads 0x0 under either.

**Two premises of the pass-1 brief were wrong and are corrected here.**  The in-tree guest driver (`if_ie.c`) writes
three of these offsets, but NEVER RUNS on this model: `machine_mvme88k.c:106` installs `unreadable` at the 82596
address, `if_ie.c:407-409` fails its match on `badpaddr()` there, and `ie_setupram()` returns early at `:561-564`
before the PCC2 store at `:609` (Fable, Opus, grok, codex independently; verified).  `ie0` IS configured in
`conf/M187` and `conf/NFS` -- the brief's conf grep looked in the wrong files.  So the HIGH ranking rests on the
witness and severity, not on the driver.  And the alias the model implements (`relative_addr %= PCC2_SIZE`) is the
REAL part's: Motorola VMESBCP2 Table 6-1 lists `$FFF42040-$FFF42FFF  PCCchip2 Registers  Repeated` -- the codex seat
cited it, the manual was fetched into `_scratchpad/` and the line read (`vmesbcp2.txt:4629`).  Two seats had rightly
called the fold unestablished before the manual was on disk.

Recorded alternatives: the codex seat's ONE latch for the whole site, writes only (not adopted: a driver scanning
registers should see each distinct one announced; both forms are bounded).  Corrections to the option set from this
round: `return 0` denotes a FAILED TRANSACTION, not inherently unmapped hardware (an IACK cycle with no interrupt
pending times out on the real part).  Disclosed: the in-word bytes are the interior of IMPLEMENTED counters, declined
here as a width/alignment matter (`pcc2widecompose`), not claimed as unimplemented registers; the IACK offsets
0x23/0x25 are declined like the rest -- modelling them on the SCCRXIACK shape would open two new entries into the
C040 path, so `pcc2c040kill` goes first (filed as a cross-round obligation); per-instance latch scope is not
provable by two fresh sessions (each is a new process) -- a two-instance fixture is filed.

## The detector (`regress/pcc2_default_probe.py`, 23 rows; gate 14 pins them)

Controls: `live`, `devsig chipid`, `sccerr rdawr` (cased sibling), `genctl rt`, `t1cmp word rt` (the cased arms are
untouched), `put b ctl` + `put b ctl msg` (the debugger path never reaches the arm).  Survival: `named wr`, `named rd`
(all eighteen named offsets in ONE session per direction -- valid because the fix has no per-offset branch;
`named wr msg` localises), `inword wr`, `unnamed wr`, `alias 0x6a`.  Disposition: `ieicr rdawr`, `ieerr rdawr` (0x0,
not the stored byte), `named rd srvd` (the read announce says SERVED, never ignored).  Latch: `named wr msg` 18,
`named rd msg` 18, `latch sameoff` 1, `latch twooff` 2, `latch rw one` 1.  Text: `alias msg` (the announce names the
FOLDED offset), `dir wr text`, `dir rd text`.  The pty helper is the width probe's, extracted at run time -- the
frozen instrument is therefore a PAIR (both files copied beside the table).

## The kill table (`regress/artifacts/pcc2defaultkill/killtable_20260905/driver.log`; predictions in `PRETABLE_501.out`, mtime 04:12:20; run 1 launched 04:12:43, frozen default probe c76e053a; run 2 -- the table quoted -- frozen a96b8bcf, the status-last instrument gate 14 counts; width helper a080e2bc in both)

| run | predicted | measured | red rows |
|---|---|---|---|
| BASE (fresh clone of build/, rebuilt) | 23/23 | **23/23** | -- |
| `M_EXIT` -- the verbatim `exit(1)` body reinstated | 8/23 | **7/23** | named wr, named wr msg, named rd, named rd msg, named rd srvd, inword wr, unnamed wr, ieicr rdawr, ieerr rdawr, latch sameoff, latch twooff, latch rw one, alias 0x6a, alias msg, dir wr text, dir rd text -- sixteen (the prediction listed fifteen and miscounted its own green set) |
| `M_UNLATCH` -- `if (1)` for the latch test | 21/23 | **21/23** | latch sameoff 2, latch rw one 2 -- exact |
| `M_ONELATCH` -- one whole-arm bit (`1ULL`) | 19/23 | **19/23** | named wr msg 1, named rd msg 1, named rd srvd 1, latch twooff 1 -- exact |
| `M_BACKED` -- a store into `pcctwo_reg[]` added (member 6) | 21/23 | **21/23** | ieicr rdawr 0x5a, ieerr rdawr 0x5a -- exact; `sccerr rdawr` (the cased write-to-clear control) stayed 0x0 |
| `M_RDKILL` -- `if (writeflag == MEM_READ) exit(1);` | 18/23 | **16/23** | named rd, named rd msg, named rd srvd, dir rd text, latch rw one (the read in that session exits) -- as predicted -- plus ieicr rdawr and ieerr rdawr, whose store-then-LOAD sessions exit at the load |
| `M_DIRSWAP` -- the announce's direction test inverted | 20/23 | **20/23** | dir wr text 0, dir rd text 0, named rd srvd 0 -- exact |

Six of six killed; four predictions exact, two missed in the SAFE direction (more reds), each derived: M_EXIT's
prediction listed fifteen red rows against a green set of seven and so summed to 22 of 23 -- an arithmetic slip in the
pre-table, not a channel surprise; M_RDKILL's read-after-write rows contain a LOAD, so they die with the reads.  Every
mutant string was gcc-syntax-checked before the table (`mut_syntax2.py`, anchors from the driver's own `mut` lines) and
proven by a diff count against SEC; the clone restored from SEC, rebuilt, cmp-clean, sentinel cleared.  The
disposition-pinning rows did their one job: `M_BACKED` reads back the stored byte at both uncased offsets while the
cased sibling reads 0x0 -- the difference between member 6 and member 3, measured, with its control.

**Two runs, one prediction file.**  Run 1 (04:12-04:25, frozen default probe `c76e053a`) is the table above; its row
PRINT format put the status before the note, and gate 14 -- which counts rows by `^<name>  .*ok$` -- then counted
ZERO of 23 rows while the probe said DONE (`killtable_20260905/gate14_501_FAIL_rowformat.log`, 25 of 844 checks
red, the 251 width rows all green).  L1, fixed in-round: status last, as the width probe prints; the gate's own
patterns then count 23.  Run 2 (05:05-05:18, frozen `a96b8bcf`) re-measured the same six mutants on the fixed-format
instrument -- BASE 23, M_EXIT 7, M_UNLATCH 21, M_ONELATCH 19, M_BACKED 21, M_RDKILL 16, M_DIRSWAP 20 -- identical
to run 1 row for row; run 1 is kept as `run1_oldrowformat/`.  *A probe whose summary line is right and whose rows
the gate cannot count is a detector that would have shipped green and counted nothing; the gate is the check
that saw it, which is what a gate is for.*

## Gate 14 (`killtable_20260905/gate14_501.log`; the live probes -- default md5 a96b8bcf, width a080e2bc, both equal to the frozen run-2 pair; run alone 05:19-05:55)

`gate 14: ARM/Thumb flags: PASS (844 checks)`, `pcc2 default rows emitted 23`, `pcc2 default rows green 23`, `pcc2 width rows emitted 251`,
`pcc2 width rows green 251`, GATE_RC=0.  The previous run of this gate (04:26-05:00, `gate14_501_FAIL_rowformat.log`) had
counted ZERO default rows against a probe that said DONE -- the row-format defect described above -- and is kept.

## Pass 2 (nine seats on the real diff, `_scratchpad/panel_20260905_055656`): the 23-row detector was BELOW THE FLOOR, six ways

**Roster.**  codex (GPT-6 Astra, max), grok, kimi (the CLI stalled on the 54 KB pointer form -- 4.5 KB of paging
monologue, no answer, `kimi.stall_pointerform.txt` -- and was RE-FIRED ONCE with the 19 KB packet inline; it then
answered), glm and deepseek (thinking-burned on the full packet -- `ollama_*.burn.txt` -- and answered 2 KB
one-question mini packets), minimax, Opus 5 and Fable 5 (Agent seats; answers preserved as `opus5.txt`, `fable5.txt`).
agy DELIBERATELY NOT FIRED (measurement reserve).  Five seats said PASS or GO (kimi, minimax, glm, deepseek; Fable
GO-WITH-CHANGES, provisional); three said NOT CLOSE (codex, grok, Opus).  **Count the arguments: the three carried
measurements or predictions the five had not tested, and the Opus seat's two were MEASURED in its own scratch clone
against the frozen instrument pair (md5-verified equal to the live one).**  The fix itself every seat held right:
the fold bounds the shift (`uint64_t`, `%= 0x40`), `break` reaches the one `return 1`, the latch words are separate
fields both zeroed at DEVINIT, no cased arm is touched -- and, as Opus put it, the arm can only add output where the
old code called `exit(1)`, so no boot that works today can regress.

**The six escapes of the 23-row instrument** (every one a clause-(d)-shaped edit of the new arm; the first two
MEASURED at 23/23, the rest predicted from the row list and measured in table 3 below):

| seat | mutant | why 23 rows could not see it |
|---|---|---|
| Opus (MEASURED 23/23) | the read announce's value `-> 0` (one token) | `named rd srvd` counts the PHRASE `served 0x`, never the value; no row served a nonzero byte |
| Opus (MEASURED 23/23) | member 6 on the LATCHED path: `} else if (writeflag == MEM_WRITE) pcctwo_reg[ra] = idata;` | both `rdawr` rows store ONCE to a fresh offset in a fresh process; the latch state was built by `sameoff`/`twooff`/`rw one` and observed on the COUNT channel only |
| grok | the latch SET conditioned on writes | the bit-set cell was reached only through a WRITE (`rw one`); two reads at one offset had no row -- the setter's direction is a third axis the (writeflag x latch) 2x2 hides |
| grok | `if (len != 1) exit(1);` -- the removed kill was width-agnostic, so this is a PARTIAL reinstatement | every default-path row was `st.b`/`ld.bu`; the pass-1 PRETABLE's own SIBLING PARITY sentence said "byte-and-wide" and no row drove wide |
| codex | `|=` `->` `=` at the latch update (forgets earlier bits when a new offset announces) | A,A and A,B and W,R never REVISIT an offset after another has announced; A,B,A wants 2 and the mutant prints 3 |
| Fable | `if (relative_addr == 0x06) exit(1);` -- a re-kill at an offset the rows never drove | writes drove 27 of the 43 offsets and reads 18 (codex's count); the pass-1 contract had DISCLOSED the sampling |

**The diagnosis, from the pass-1 PRETABLE's own GUARD-FIELD line:** *"they disagree only in the latch's own state,
which the sameoff/twooff/rw-one rows build"* -- true, and the state was observed on one channel (the announce count)
while the mutant that matters (Opus M_O2) changes the OTHER channel (the read-back value) in exactly that state.  The
guard/body check found the cell and the row was written against the wrong observable.  And codex found a product
defect the rows could not: the read announce RELOADED `pcctwo_reg[relative_addr]` after the response was copied, and
the SIGALRM tick rewrites the counter interiors -- so for the twelve in-word offsets the announced byte could differ
from the served one.  `"the array's default, NOT a computed value"` was therefore also wrong for those twelve.

**The repair (one diff, class closure -- the repair-chain amendment: consecutive cells of one class are closed
together, not one per pass).**  PRODUCT: both announces carry `(len %d)`; the read announce prints `data[0]` -- the
byte actually SERVED -- with a comment saying why.  DETECTOR, 36 rows (+13): `latch rd rd` and `latch rd wr` complete
the setter x tester product (W,W `sameoff`; W,R `rw one`; R,R; R,W); `latch aba` pins accumulation across offsets;
`sameoff val` reads back after the SECOND write (the latched path's disposition); `srvd val` + `srvd val text` serve
a byte the GUEST wrote (a word store through the cased T1CMP arm puts 0x34 at 0x05) and pin the announced value;
`wide wr` (+`msg`) and `wide rd` (+`srvd`) drive `st.w`/`ld.w` at uncased word-aligned offsets and pin the width
text; `inword wr`/`unnamed wr` now drive all 12 / all 13, and `inword rd`/`unnamed rd` read them -- **every one of
the 43 uncased offsets is written once and read once**; `wr declined` pins the word.  Row names stay under 14
characters (the gate's `%-16s` anchor).  RECORDS (the L4s the seats named): the kill-table header's `c76e053a ==
live` (run 1's md5 against run 2's table; the live probe was `a96b8bcf`); "three predictions exact" (four); the
M_EXIT diagnosis (its 16-row red SET was right, only the numeral and the derived score were wrong); "would have
shipped green and counted nothing" (the gate FAILED 25/844 and caught it); the `alias 0x6a` row saying "not proven
of the real part" beside a docstring citing Table 6-1; `unnamed wr` describing an overrun M_BACKED's end-span guard
prevents; "four arms up" (ten case blocks); "no guest reaches these offsets" (the witness IS a guest -- limited to
the inspected OpenBSD driver paths); "unnamed" made explicit as "the fork header has no label" (the manual names
0x39 as SPEED's second byte and 0x3b as PRTDATA's low byte -- codex).  Pass-2 mini-packet findings adopted: the
announce under-described a wide read (deepseek, grok, Opus, codex all named it) -- fixed by the width label.
Rejected: minimax's "unsafe" label on the M_RDKILL prediction miss (a predicted-green row that went red is the
SAFE direction, by the round's own rule).  Recorded, not adopted: codex's per-instance latch point is `pcc2latchinst`
(filed); Opus noted there is NO mvme88k boot rig (`grep -l mvme regress/*.sh` is empty), so the two gate-14 probes are
this device's entire coverage -- a fact for the queue, not this round.

## Table 3 (`killtable3_20260905/driver.log`; predictions in `PRETABLE_501b.out`, mtime 06:25:42, written before either run; frozen repaired instrument md5 `10737375` == live; the pass-2 instrument `old23/` md5 `a96b8bcf`; scratch clone of build/, BASE rebuilt in the clone, twelve mutants each compile-checked before the table and proven by a diff count)

**Every one of the twelve predictions was EXACT -- score and red set -- and every one of the six pass-2 escapes is
MEASURED on the same binary by both instruments: 23/23 on the instrument that shipped at pass 2, red on the repaired
one, on exactly the row built for it.**

| mutant | shape | repaired instrument (36 rows) | red rows | pass-2 instrument (23 rows) |
|---|---|---|---|---|
| BASE | the repaired working set | **36/36** | -- | **23/23** (control: every old anchor survives the `(len N)` text) |
| M_WRLATCH | latch SET only on writes (grok A) | 34/36 | latch rd rd, latch rd wr | **23/23** -- the breach |
| M_WIDEKILL | `if (len != 1) exit(1);` (grok B) | 32/36 | wide wr, wide wr msg, wide rd, wide rd srvd | **23/23** |
| M_OFFKILL | `if (relative_addr == 0x06) exit(1);` (Fable) | 34/36 | inword wr, inword rd | **23/23** |
| M_SRVD0 | read announce prints 0 (Opus M_O1) | 35/36 | srvd val text | **23/23** (Opus had measured it) |
| M_BACKED2 | member 6 on the latched path (Opus M_O2) | 35/36 | sameoff val | **23/23** (Opus had measured it) |
| M_ABA | `\|=` `->` `=` at the latch update (codex) | 35/36 | latch aba | **23/23** |
| M_EXIT | (b) the verbatim `exit(1)` arm | 7/36 | the 16 of pass 2 + all 13 new rows (29) | (pass 2: 7/23) |
| M_UNLATCH | (d) announce unlatched | 30/36 | latch sameoff, latch rw one, latch rd rd, latch rd wr, latch aba, wide wr msg | (21/23) |
| M_ONELATCH | (d) one whole-arm latch bit | 31/36 | named wr msg, named rd msg, named rd srvd, latch twooff, latch aba | (19/23) |
| M_BACKED | member 6, every write (end-span guarded) | 32/36 | ieicr rdawr, ieerr rdawr, sameoff val, wide wr (0x5a5a5a5a) | (21/23) |
| M_RDKILL | (d) reads re-killed | 17/36 | the seven of pass 2 + latch sameoff (its session now reads), sameoff val, latch rd rd, latch rd wr, srvd val, srvd val text, wide wr, wide wr msg, wide rd, wide rd srvd, inword rd, unnamed rd | (16/23) |
| M_DIRSWAP | (d) the direction test inverted | 30/36 | dir wr text, dir rd text, named rd srvd, srvd val text, wide rd srvd, wr declined | (20/23) |

Denominator of the zero: twelve mutant shapes, named above; the cells they close are the setter x tester direction
product (four), accumulation across offsets, the disposition on the latched path, the served VALUE, wide (len 4)
default accesses in both directions, and every one of the 43 uncased offsets driven once in each direction.  NOT
closed, disclosed in the contract: len-2-only re-kills; an end-spanning wide read; per-instance latch scope.

**Two runs, one prediction file.**  Run 1 (06:26-06:35) measured BASE (36/36, 23/23) and M_WRLATCH (34/36, 23/23) --
identical to run 2 -- and then DIED at its second `mut` line: an apostrophe inside a single-quoted expect string
(`len != 1'`) ended the quote and bash aborted the script with a parse error, while the wrapper reported rc=0 (its
trailing echo).  `mut_syntax2.py` had checked all twelve mutants' C and could not see a shell-quoting defect in the
driver; `bash -n` had been run on the gate script and not on the driver.  The partial run is kept as
`run1_partial_quoting/`; the generator now refuses a quote in an expect string and the launcher runs `bash -n` on
the frozen driver before exec.  Run 2 (06:37-07:26) is the table above.  The clone's source was `cmp`-clean against
SEC and its sentinel cleared after the restore rebuild.

## Gate 14 on the repaired instrument (`killtable3_20260905/gate14_501b.log`; the live probes -- default md5 `10737375` == the table-3 frozen instrument, width `a080e2bc`; run alone 07:39-08:16 on a build/ that had passed the two-part clearance minutes earlier)

`pcc2 default rows emitted 36 / green 36 / red 0`; `pcc2 width rows emitted 251 / green 251 / red 0`; 875 checks ok, 0 FAIL, `GATE_RC=0`.
The gate's name list for the default section is DERIVED from the probe's `row("...")` calls by the repair script (36
names, none longer than 14 characters -- the gate's `%-16s` + two-space anchor would silently stop counting a longer
one), so the list and the probe cannot disagree by transcription.

<<PANEL501P3_OWED>>

## Records

OUTSTANDING_BUGS: `pcc2defaultkill` FIXED; filed from this round: `pcc2iackmodel` (SCCTXIACK/SCCMOIACK acknowledge
semantics on the SCCRXIACK shape, AFTER `pcc2c040kill`), `pcc2latchinst` (a two-instance fixture for per-instance
latch scope, a harness debt shared with the width latch).  `pcc2c040kill` gains the fact the design panel found: the
SCCRXIACK arm runs on READS (no writeflag test) and the console driver reads that offset, so the ENTRY into the C040
path is routine guest traffic -- only the arming (C040 set in GENCTL) is rare.  Ledger: witness
`probe:regress/artifacts/pcc2defaultkill/witness_20260905/defaultkill_witness.py`, detector
`regress/pcc2_default_probe.py`, every seat of both passes by name.  Carrier: the MVME187 manual added to the primary
sources; the member-5 wording.

```

## DISCLOSURE -- the working set (the `sgi_de_primop_probe.py` line is a pre-existing unrelated edit, not this round's)

```
218	0	CHANGELOG.md
25	0	regress/gate_arm.sh
20	6	regress/sgi_de_primop_probe.py
41	7	src/devices/dev_pcc2.c
100	1	tools/pipeline/ledger.json
?? regress/artifacts/pcc2defaultkill/killtable3_20260905/
?? regress/artifacts/pcc2defaultkill/killtable_20260905/
?? regress/artifacts/pcc2defaultkill/pass2_seats/
?? regress/artifacts/pcc2defaultkill/witness_20260905/detector_fixed_501.out
?? regress/artifacts/pcc2defaultkill/witness_20260905/witness_fixed_501.out
?? regress/pcc2_default_probe.py

```


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
