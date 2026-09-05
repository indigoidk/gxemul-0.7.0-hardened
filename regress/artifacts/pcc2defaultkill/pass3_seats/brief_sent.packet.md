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

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot
settle from this packet rather than guessing at it.
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

## THE PRODUCT REPAIR DIFF (VERBATIM)

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

## THE THREE QUESTIONS

**1. Is the repair right -- is `data[0]` always the byte the guest received (memcpy path and end-span zero-fill path),
and which accepted disposition above is wrong, by number?**

**2. From table 3 and its predictions: does any mutant's result contradict its prediction; is any of the six pass-2
mutants NOT 23/23 on the pass-2 instrument (which would make the breach claim wrong); and is any cell of the closure
still open -- name the edit?**

**3. Should #501 close and commit?  Carry the denominator: which mutant shapes, which cells, what is excluded.**
Anything you cannot settle from this packet: one line.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
