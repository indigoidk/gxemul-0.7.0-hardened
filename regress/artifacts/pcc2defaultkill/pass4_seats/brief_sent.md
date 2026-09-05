# #501 pcc2defaultkill -- PASS 4: the pass on the PASS-3 REPAIR DIFF.  Pass 3 measured six clean sweeps of the 36-row detector (one the mirror of the cell pass 2 had closed) and derived four more; the repair appends ten rows to existing sessions and this pass reviews THAT diff.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A repair made in response to a pass owes its own pass, scoped to the repair diff -- **but the FLOOR QUESTION is asked of
the shipped COMPOSITE**: does a clause-(d) mutant exist that sweeps the 46-row detector clean?  Two passes running, seats
that READ said close and a seat that BUILT found sweeps.  Build (or derive with the row list in hand), do not vote.  The
pass-3 repair closed the announce's VALUE channel on the arm the pass-2 mutant had NOT used -- the `#499` shape -- so ask
first: **what is the mirror of each new row?**  Be harder on the accepted dispositions; a seat whose escape was adopted
scrutinises its own repair row MORE (does the row kill the mutant for the reason claimed, or by accident?).  **VERDICT
LINE FIRST.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of `7076134`.**  Three
pristine-2021 copies of `src/` under the project root are NOT this fork; if your line numbers disagree by hundreds you are
reading one -- say so.  The pass-3 product state is preserved verbatim as
`regress/artifacts/pcc2defaultkill/killtable3_20260905/dev_pcc2.pass3.c` and the pass-3 instrument as
`killtable3_20260905/frozen_probe.py` (md5 10737375): the diffs below are against THOSE.

## PREMISES ALREADY SETTLED, RE-INLINED (each is a QUESTION if you can check it)

1. **The fix** (unchanged in substance since pass 1; unchanged in CODE since pass 2): the `default:` arm no longer calls
   `exit(1)`; a READ keeps the byte the memcpy served and is announced `served 0x%02x` from `data[0]` with its length;
   a WRITE is DECLINED (member 3) and announced with its length and value; one latched `fatal()` per offset per instance
   (`uint64_t warned_unimpl`, bit `relative_addr`, folded `%= PCC2_SIZE` (0x40) first so the shift is 0..63).  43 of the
   0x40 offsets reach the arm (18 named-unimplemented, 12 counter interiors, 13 the fork header leaves unnamed).
2. **The pass-3 repair to the product is TWO COMMENT SENTENCES** (the tick reason narrowed to the two COUNT words while a
   counter runs, with the end-span reason added; "a counter interior" -> "inside a running COUNT word").  No code line.
3. **The pass-3 escapes and the row that now kills each** (all ten rows APPENDED to existing sessions, zero new sessions):
     Opus M_WRVAL0 / M_WRDATA0  write announce value -> 0 / -> data[0] (MEASURED 36/36)  -> `wr val text', `wide wr val'
     Opus M_LASTBYTE            read announce data[len-1] (MEASURED 36/36)             -> `srvd half text' (0x56 of 0x5678)
     Opus M_RELOAD              read announce reloads the array (MEASURED 36/36)       -> DISCLOSED: no deterministic row
     Opus M_BACKEDLOW           member 6 for relative_addr < 0x14 (MEASURED 36/36)     -> `inword rdawr', `half wr rdawr'
     Opus M_LATCHOFF            latch SET only at IEICR/IEERR (MEASURED 36/36)          -> `inword msg', `unnamed msg'
     grok/Fable  `if (len == 2) exit(1);'                                               -> the srvd session (len-2 read+write)
     codex M_LATCH_RD_ZERO      latched-path READ response zeroed (derived)             -> `srvd rd latch', `srvd wr latch'
     codex len -> 4 on either arm (derived)                                             -> `srvd val text' (`(len 1)'), `wr val text'
   In table 4 each of the ten is scored by BOTH instruments: the pass-3 one (36/36 = the breach, measured -- M_RELOAD's
   46/46 on the new one is the DISCLOSED expectation) and the repaired one (red).  BASE is measured full on both.
4. **The offset axis is NOT floor** (the arm has no `if' on `relative_addr'; the switch tests cased vs uncased only) --
   pass 3 closed it per CLASS (named / in-word / unnamed: one count and one read-back each) and DISCLOSES single-offset
   scoping.  `len' is not tested by the arm either: width rows are CLAIM rows; len 1, 2 and 4 are now rowed both ways,
   len 8 (the m88k core issues ld.d/st.d) stays disclosed.
5. **The witness** (rung 3, unchanged): 7/13 on the committed build, 13/13 on the fix (`witness_20260905/`).
6. **The roster**: nine seats; agy DELIBERATELY NOT FIRED (measurement reserve).  Pass 3's glm burned twice (recorded as a
   seat failure); kimi paged the pointer form but exited without a verdict line while it waited on a scratch build.
   **This packet is therefore SHORT on purpose, and its questions are CLOSED where they can be.**

## THE MEASUREMENTS (every number names its log)

Table 4 (`killtable4_20260905/driver.log`; frozen repaired instrument md5 b9b2fadc, live b9b2fadc; the pass-3
instrument `old36/` 10737375; scratch clone of build/, BASE rebuilt in the clone, each mutant compile-checked before the
table (22/22) and proven by a diff count).  `.old36` rows are the pass-3 instrument on the same binary:
    BASE               46/46    -
    BASE.old36         36/36    -
    M_WRVAL0           44/46    wr val text,wide wr val
    M_WRVAL0.old36     36/36    -
    M_WRDATA0          45/46    wide wr val
    M_WRDATA0.old36    36/36    -
    M_LASTBYTE         45/46    srvd half text
    M_LASTBYTE.old36   36/36    -
    M_RELOAD           46/46    -
    M_RELOAD.old36     36/36    -
    M_BACKEDLOW        43/46    inword rdawr,half wr rdawr,srvd wr latch
    M_BACKEDLOW.old36  36/36    -
    M_LATCHOFF         42/46    inword msg,unnamed msg,srvd val text,srvd half text
    M_LATCHOFF.old36   36/36    -
    M_HALFKILL         40/46    srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch
    M_HALFKILL.old36   36/36    -
    M_LATCHRD0         43/46    half wr rdawr,srvd rd latch,srvd wr latch
    M_LATCHRD0.old36   36/36    -
    M_LEN4R            44/46    srvd val text,srvd half text
    M_LEN4R.old36      36/36    -
    M_LEN4W            45/46    wr val text
    M_LEN4W.old36      36/36    -
    M_EXIT             7/46     named wr,named wr msg,named rd,named rd msg,named rd srvd,inword wr,inword msg,inword rdawr,inword rd,unnamed wr,unnamed msg,unnamed rdawr,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch twooff,latch rw one,latch rd rd,latch rd wr,latch aba,alias 0x6a,alias msg,dir wr text,wr declined,wr val text,dir rd text,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_UNLATCH          36/46    inword msg,unnamed msg,latch sameoff,latch rw one,latch rd rd,latch rd wr,latch aba,srvd val text,srvd half text,wide wr msg
    M_ONELATCH         38/46    named wr msg,named rd msg,named rd srvd,inword msg,unnamed msg,latch twooff,latch aba,srvd half text
    M_BACKED           38/46    inword rdawr,unnamed rdawr,ieicr rdawr,ieerr rdawr,sameoff val,half wr rdawr,srvd wr latch,wide wr
    M_RDKILL           16/46    named rd,named rd msg,named rd srvd,inword wr,inword msg,inword rdawr,inword rd,unnamed wr,unnamed msg,unnamed rdawr,unnamed rd,ieicr rdawr,ieerr rdawr,latch sameoff,sameoff val,latch rw one,latch rd rd,latch rd wr,dir rd text,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_DIRSWAP          37/46    named rd srvd,dir wr text,wr declined,wr val text,dir rd text,srvd val text,srvd half text,wide wr val,wide rd srvd
    M_WRLATCH          43/46    latch rd rd,latch rd wr,srvd val text
    M_WIDEKILL         35/46    srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch,wide wr,wide wr msg,wide wr val,wide rd,wide rd srvd
    M_OFFKILL          36/46    inword wr,inword msg,inword rdawr,inword rd,srvd val,srvd val text,srvd half text,half wr rdawr,srvd rd latch,srvd wr latch
    M_SRVD0            44/46    srvd val text,srvd half text
    M_BACKED2          42/46    inword rdawr,unnamed rdawr,sameoff val,half wr rdawr
    M_ABA              42/46    inword msg,unnamed msg,latch aba,srvd val text

PREDICTIONS written BEFORE the table (`PRETABLE_501c.out`, VERBATIM):
```
PRE-TABLE BLOCK, #501 pcc2defaultkill PASS-3 REPAIR (table 4) -- written BEFORE the table (mtime against
killtable4_20260905/driver.log).  Repair from the nine-seat pass 3 (_scratchpad/panel_20260905_081718): the Opus seat
MEASURED six clean sweeps of the 36-row instrument in its own clone -- M_WRVAL0 / M_WRDATA0 (the WRITE announce's value:
the mirror of pass 2's M_O1, which the pass-2 repair pinned on the READ arm only -- the #499 shape inside the repair),
M_LASTBYTE (data[len-1]: `wide rd srvd' reads four zero bytes, so its channel could not vary -- the CHANNEL check's own
failure mode), M_RELOAD (disclosed: a race no deterministic row can pin), M_BACKEDLOW / M_LATCHOFF (member 6 and the
latch SET conditioned on OFFSET CLASS -- kimi derived the same store); grok and Fable named the len-2-only re-kill;
codex DERIVED three more: a latched-path READ whose response is zeroed (the mirror of M_O2 on the read channel -- every
rowed read after a preceding access expected 0), and the width label made constant on either arm (no byte row required
`(len 1)').  Class closure #2 in ONE diff: TEN rows, EVERY ONE APPENDED TO AN EXISTING SESSION (zero new sessions).

  - SIBLING PARITY -- the announce has five channels (fate, count, direction, width, value) x two arms (writeflag).  At
    pass 3 nine of the ten cells were rowed; the WRITE arm's VALUE was not.  Now: `wr val text' (len 1) and `wide wr val'
    (len 4) -- the latter also separates idata from data[0] (a byte write cannot).  The RESPONSE channel on the latched
    path: pass 2 rowed the write side (`sameoff val'); now the read side too (`srvd rd latch', `srvd wr latch': a
    nonzero byte re-read after its bit was set by a read and by a write).
  - CLAIM -> ROW -- the contract claimed "a wrong OR CONSTANT byte -> srvd val text" while disclaiming the first-byte
    label: M_LASTBYTE showed the claim false for the wide row (all four bytes zero).  Now `srvd half text' serves a
    len-2 read whose two bytes DIFFER (0x56 0x78), so a byte-selection mutant reds; the claim is reworded to the rows.
    The width LABEL is now load-bearing at len 1 (`srvd val text', `wr val text') and len 2 (`srvd half text'), not only
    at len 4.  The len-2 disclosure is CLOSED by the same session (`half wr rdawr': a len-2 write declined); len 8 stays
    disclosed.  M_RELOAD is DISCLOSED as unrowable and listed under the denominator's exclusions, with its reason.
  - GUARD FIELD vs BODY FIELD -- guard: warned_unimpl bit relative_addr.  Body: writeflag, idata, len, data[0].  The
    OFFSET axis is not body-tested (no `if' on relative_addr in the arm; the switch tests cased vs uncased only), so
    per-offset cells are NOT floor -- but pass 3 measured member 6 and the latch SET conditioned on offset CLASS
    passing 36 rows, so one read-back and one count per CLASS are appended (in-word: 0x06; unnamed: 0x21; the named
    class already had ieicr/ieerr rdawr and latch sameoff).  A single-offset scoping beyond those stays disclosed.
  - CHANNEL -- per new row: wr val text / wide wr val: announce TEXT under DKV/DKD/DKT; srvd val text (reworded): TEXT
    under DKZ/DKY; srvd half text: TEXT under DKL/DKY and FATE under DKH; half wr rdawr: VALUE under DKG/DKB/DK2/DKX and
    FATE under DKH; srvd rd latch / srvd wr latch: VALUE under DKX (and DKG/DKB for the write-set one); inword msg /
    unnamed msg: COUNT under DKC (and DKU/DK1/DKE); inword rdawr / unnamed rdawr: VALUE under DKG/DKB/DK2.

PREDICTIONS (46-row instrument; the ten pass-3 mutants ALSO on the 36-row pass-3 instrument, where 36/36 is the
measured breach -- except M_RELOAD, whose 46/46 is the disclosed expectation; MINIMUM red set per mutant):
    BASE        46/46  and 36/36 on the pass-3 instrument
    M_WRVAL0    44/46  wr val text 0, wide wr val 0                                  old36: 36/36 (Opus measured)
    M_WRDATA0   45/46  wide wr val 0 (wr val text stays: byte write, idata == data[0]) old36: 36/36 (Opus measured)
    M_LASTBYTE  45/46  srvd half text 0                                             old36: 36/36 (Opus measured)
    M_RELOAD    46/46  DISCLOSED ESCAPE (expected)                                  old36: 36/36 (Opus measured)
    M_BACKEDLOW 43/46  inword rdawr 0x5a, half wr rdawr 0xbb78, srvd wr latch 0xbb  old36: 36/36 (Opus measured)
    M_LATCHOFF  43/46  inword msg 14, unnamed msg 15, srvd half text 2              old36: 36/36 (Opus measured)
    M_HALFKILL  40/46  the six srvd-session rows (srvd val, srvd val text, srvd half text, half wr rdawr, srvd rd
                       latch, srvd wr latch): the session dies at its ld.hu       old36: 36/36 (no len-2 access there)
    M_LATCHRD0  43/46  srvd rd latch 0x0, srvd wr latch 0x0, half wr rdawr 0x78    old36: 36/36 (codex derived)
    M_LEN4R     44/46  srvd val text 0, srvd half text 0 (wide rd srvd stays: it IS len 4)   old36: 36/36 (codex)
    M_LEN4W     45/46  wr val text 0 (wide wr msg / wide wr val stay: len 4)       old36: 36/36 (codex)
    M_EXIT       7/46  the 29 of table 3 + all ten new rows
    M_UNLATCH   37/46  the six of table 3 (latch sameoff now 3) + inword msg 14, unnamed msg 15, srvd half text 2
    M_ONELATCH  38/46  the five of table 3 + inword msg 1, unnamed msg 1, srvd half text 0
    M_BACKED    38/46  the four of table 3 + inword rdawr 0x5a, unnamed rdawr 0x5a, half wr rdawr 0xaabb, srvd wr latch 0xbb
    M_RDKILL    18/46  the 19 of table 3 + inword msg, inword rdawr, unnamed msg, unnamed rdawr, srvd half text,
                       half wr rdawr, srvd rd latch, srvd wr latch, wide wr val (its session reads)
    M_DIRSWAP   37/46  the six of table 3 + wr val text, wide wr val, srvd half text
    M_WRLATCH   44/46  latch rd rd 2, latch rd wr 2 (unchanged)
    M_WIDEKILL  35/46  the four of table 3 + wide wr val + the six srvd-session rows
    M_OFFKILL   36/46  the two of table 3 + inword msg, inword rdawr + the six srvd-session rows
    M_SRVD0     44/46  srvd val text 0, srvd half text 0
    M_BACKED2   42/46  sameoff val, inword rdawr, unnamed rdawr 0x5a; half wr rdawr 0xbb78 (the st.b at 0x07 is a FIRST
                       write there: declined, so srvd wr latch stays 0x78)
    M_ABA       43/46  latch aba 3, inword msg 13, unnamed msg 14
  A miss in the SAFE direction is recorded (with its value, not just its colour -- table 3's `latch sameoff 3' was
  recorded late); one in the UNSAFE direction stops the round.  A pass-3 mutant NOT at 36/36 on the old instrument is a
  wrong breach claim and is recorded as such.  Written 2026-09-05 09:08:39.
```

Gate 14 (`killtable4_20260905/gate14_501c.log`, run alone): pcc2 default rows emitted 46, green 46; pcc2 width
rows emitted 251, green 251; the gate's own line `PASS (867 checks)`; GATE_RC=0.

## SECTION F2 -- THE PASS-3 DISPOSITIONS, numbered (the adjudication the panel shares)

ACCEPTED, REPAIRED IN-ROUND (L1: the detector is uncommitted; the class closure per the repair-chain amendment)
 1. (opus5, MEASURED) M_WRVAL0 / M_WRDATA0 -- the write announce's value: `wr val text', `wide wr val'.
 2. (opus5, MEASURED) M_LASTBYTE -- `srvd half text' serves two bytes that differ (0x56 0x78).  L4 on the contract's
    "wrong or constant byte" claim: reworded to the rows.
 3. (opus5, MEASURED) M_BACKEDLOW, M_LATCHOFF -- one read-back and one count per offset class (`inword msg/rdawr',
    `unnamed msg/rdawr').  NOT 43 value rows (the #392 shape); single-offset scoping DISCLOSED.
 4. (codex, derived) M_LATCH_RD_ZERO -- `srvd rd latch' (bit set by a read), `srvd wr latch' (bit set by a write).
 5. (codex, derived) `len' -> `4' -- `srvd val text' reworded to `0x5 (len 1) -- served 0x34'; `wr val text' carries `(len 1)'.
 6. (grok, fable5) `len == 2' re-kill -- the srvd session's ld.hu/st.h/ld.hu (`srvd half text', `half wr rdawr'): the
    pass-2 len-2 disclosure is CLOSED; len 8 stays disclosed.
 7. (opus5, MEASURED) M_RELOAD -- DISCLOSED as unrowable (a race in the COUNT words under the signal-driven tick, or the
    end-span path where every reachable start byte is 0); `data[0]' stays the operand, with the end-span reason in the
    comment (fable5) -- Fable's "ticks run between instructions" premise REFUTED by reading timer.c (the SIGALRM handler
    calls the callbacks directly); grok's narrowing (COUNT words only, CEN off at init) adopted; codex's "twelve
    interiors" -> six.
 8. L4s corrected IN PLACE: "875 checks" -> the gate's own 857 (grok, Opus, codex); the headline and the detector heading
    "23 rows" (grok, Fable, Opus); the four pass-1 sentences the pass-2 section had corrected only in a later paragraph
    (codex); the unrecorded `latch sameoff 3' safe miss (Opus, codex); the CHANGELOG denominator list vs the probe's
    DISCLOSED list (Opus); SEATS.txt's "kimi MISSING" reconciled in the record (codex).
 9. (kimi, grok) the write-value and offset-class residuals filed as `pcc2dispall' at pass 3 -> WITHDRAWN as a filing:
    both are rows now.

REJECTED / NOT CREDITED
10. (grok, deepseek, minimax; fable5 GO-WITH-CHANGES) close on the 36-row instrument -- overtaken by six measured sweeps.
    Readings, recorded by name; not seat failures.
11. (fable5) R2 as stated -- the premise was wrong (timer.c), the second reason right and adopted.
12. (opus5) "eight of the twelve interiors are tick-written" -- six (the two COUNT words' interiors).
13. (glm) SEAT FAILURE, thinking burn x2 -- not agreement.

## QUESTIONS

1. **IS THE REPAIR RIGHT?**  Ten rows, two encoders (`LD_HU' 0x02, `ST_H' 0x0a -- check them against `cpu_m88k_instr.c'
   or the width probe), the srvd session's register plan (r4 0x34, r6 0x5678, r8 0x34, r9 0x78; r7 = 0xaabb), the
   alignment of every new access (0x06 halfword, 0x07 byte, 0x21 byte).  Does any new row's text anchor collide with
   another announce in its session (e.g. `0x6 (len 2)' vs a write text)?  Is `srvd wr latch' 0x78 -- i.e. does the
   declined st.b at 0x07 leave the array byte the cased word store put there?
2. **DOES EACH OF THE TWENTY-TWO MUTANTS DIE FOR THE REASON CLAIMED?**  Table 4 and its predictions are inlined; the ten
   pass-3 mutants carry a second score on the pass-3 instrument (36/36 owed = the breach; M_RELOAD 46/46 on the new one
   is disclosed).  A prediction that missed is the interesting case; a mutant killed by a row OTHER than the one built
   for it is a row killing by accident.
3. **THE MIRRORS.**  For each of the ten new rows name its mirror cell (the other arm, the other setter direction, the
   other width, the other offset class) and say whether that cell is rowed, disclosed, or NEITHER.  Neither is the
   finding.
4. **THE SMALLEST EDIT THAT BREAKS THE PROPERTY AND PASSES 46 ROWS.**  Name the row you expect to stay green and why.
   Measured beats derived (Opus built six last pass; derived escapes have been right three times and wrong zero -- but
   they are predictions until measured).
5. **IS THE RECORD HONEST?**  The CHANGELOG block (pass 2, pass 3, table 4, gate sections inlined), the contract
   (docstring, v3), the pass-4 PRETABLE.  Name any sentence a measurement refutes, any count without a deriver, any
   correction that landed only in a later paragraph while the original sentence stands.
6. **CLOSE?**  A closing zero must be VALID: the diff delivered (inlined), the roster complete or misses named, the zero
   carried WITH its denominator -- which mutant shapes (twenty-two, named), which cells -- and its EXCLUSIONS (M_RELOAD,
   len 8, end-span reads, single-offset scoping, per-instance latch scope, the `debug()'-for-`fatal()' probe-shape
   limit).  If you say close, say what the denominator excludes; if you say not close, name the cell and the edit.

If, while verifying a claim, you found something ELSE -- say so.

## THE PRODUCT DIFF OF THIS REPAIR (pass-3 state -> now, VERBATIM -- two comment sentences)

```diff
--- GXEMUL-SEC/regress/artifacts/pcc2defaultkill/killtable3_20260905/dev_pcc2.pass3.c	2026-09-05 09:09:41.252010700 -0500
+++ GXEMUL-SEC/src/devices/dev_pcc2.c	2026-09-05 09:08:20.247168000 -0500
@@ -670,8 +670,8 @@
 		    ones -- READS included, though the memcpy above the switch had
 		    already served them.  A guest ld.bu or st.b at any of them was a host
 		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
-		    current byte, said so -- for a counter interior that is the tick's
-		    value, not a default); a WRITE is DECLINED.  Not a
+		    current byte, said so -- inside a running COUNT word that is the
+		    tick's value, not a default); a WRITE is DECLINED.  Not a
 		    backed store: the cased siblings contradict one (SCCERR clears on
 		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
 		    read-only), no inspected OpenBSD driver path reaches them (if_ie never
@@ -692,8 +692,10 @@
 				    (int) relative_addr, (int) len, (int) idata);
 			else
 				/*  data[0] is the byte actually SERVED; a reload of the
-				    array here could differ (the tick rewrites the
-				    counter interiors), and a wide read is labelled.  */
+				    array could differ: on the end-span path (zero-filled,
+				    the array byte kept) and inside a running COUNT word,
+				    whose SIGALRM-driven tick (timer.c) can land between
+				    the copy and this line.  A wide read is labelled.  */
 				fatal("[ pcc2: unimplemented read from offset "
 				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
 				    (int) relative_addr, (int) len, data[0]);

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
		    current byte, said so -- inside a running COUNT word that is the
		    tick's value, not a default); a WRITE is DECLINED.  Not a
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
				    array could differ: on the end-span path (zero-filled,
				    the array byte kept) and inside a running COUNT word,
				    whose SIGALRM-driven tick (timer.c) can land between
				    the copy and this line.  A wide read is labelled.  */
				fatal("[ pcc2: unimplemented read from offset "
				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
				    (int) relative_addr, (int) len, data[0]);
		}
		break;
	}

	return 1;
```

## THE DETECTOR DIFF OF THIS REPAIR (pass-3 instrument -> now, VERBATIM)

```diff
--- GXEMUL-SEC/regress/artifacts/pcc2defaultkill/killtable3_20260905/frozen_probe.py	2026-09-05 07:26:32.872418000 -0500
+++ GXEMUL-SEC/regress/pcc2_default_probe.py	2026-09-05 09:08:20.245585100 -0500
@@ -10,53 +10,79 @@
 (rung-3 witness, 7/13 on the committed build: regress/artifacts/pcc2defaultkill/witness_20260905/).
 
 THE FIX (pass-1 panel of 2026-09-05, nine seats, converged): READ side -- keep the byte the memcpy
-already served (the register array's CURRENT byte -- the tick's, for a counter interior: the announce says so);
+already served (the register array's CURRENT byte -- the tick's, inside a running COUNT word: the announce says so);
 WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
 accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
 mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
 reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
 one arm reached by 43 offsets adds a bounded-write surface the decline does not have.
 
-CONTRACT -- what this detector is built to catch, by row (36 rows; the 13 added by the pass-2 repair are marked +):
+CONTRACT -- what this detector is built to catch, by row (46 rows: 23 at pass 2, +13 by the pass-2 repair, +10 by the
+pass-3 repair; every pass-3 row was APPENDED to an existing session):
+  member 6 on the READ side of the latched path -- a read whose bit is already set gets its RESPONSE zeroed (codex
+      M_LATCH_RD_ZERO: every rowed read after a preceding access expected 0 anyway)
+                                                    -> `srvd rd latch' (0x34 after a read set the bit), `srvd wr latch'
+                                                       (0x78 after a write set it)
+  the announce's width label constant (`(int) len' -> `4', codex: no byte row required `(len 1)')
+                                                    -> `srvd val text' (`0x5 (len 1) -- served 0x34'), `wr val text'
+                                                       (`0x30 (len 1): 0x5a'), `srvd half text' (`(len 2)')
   (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
   (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
   (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
-  (d) the latch SET conditioned on writes (grok A)  -> + `latch rd rd' (2, not 1), + `latch rd wr' (2, not 1): with
+  (d) the latch SET conditioned on writes (grok A)  -> `latch rd rd' (2, not 1), `latch rd wr' (2, not 1): with
       `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
-  (d) `|=' -> `=' at the latch update (codex)       -> + `latch aba' (3, not 2): bits already set survive a new offset
+  (d) the latch SET conditioned on OFFSET CLASS (Opus M_LATCHOFF, MEASURED 36/36)
+                                                    -> `inword msg' (12), `unnamed msg' (13): a second write to one
+                                                       offset of each class is silent; the named class is `latch sameoff'
+  (d) `|=' -> `=' at the latch update (codex)       -> `latch aba' (3, not 2): bits already set survive a new offset
   (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
-  (d) a `len != 1' re-kill -- the removed kill was width-agnostic, so this is a partial reinstatement (grok B)
-                                                    -> + `wide wr' / + `wide rd' (host exit)
-  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' now drive all 12 / all 13, and
-                                                       + `inword rd' / + `unnamed rd' read them: every one of the 43
-                                                       uncased offsets is written once and read once
-  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / + `wr declined'
+  (d) a width re-kill -- the removed kill was width-agnostic, so `len != 1' (grok B) or `len == 2' (grok, Fable) is a
+      partial reinstatement                         -> `wide wr' / `wide rd' (len 4, host exit); `srvd half text' /
+                                                       `half wr rdawr' (len 2, host exit)
+  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' drive all 12 / all 13, and `inword rd'
+                                                       / `unnamed rd' read them: every one of the 43 uncased offsets is
+                                                       written once and read once
+  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / `wr declined'
   member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
       instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
       control that reads 0x0 under either and makes the delta attributable
-  member 6 on the LATCHED path only (Opus M_O2: a store exempting the first write per offset -- MEASURED 23/23 on
-      the 23-row instrument)                        -> + `sameoff val' (0x5a, not 0x0)
-  the read announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23: `named rd srvd' counts the
-      phrase, not the value)                        -> + `srvd val text' (`served 0x34' absent); + `srvd val' pins
-      the served byte itself as one the GUEST wrote (through the cased T1CMP word arm), not a default
-  the announce omitting the access width            -> + `wide wr msg' / + `wide rd srvd' (`(len 4)')
+  member 6 on the LATCHED path only (Opus M_O2, MEASURED 23/23)   -> `sameoff val' (0x5a, not 0x0)
+  member 6 scoped to an OFFSET CLASS (Opus M_BACKEDLOW `relative_addr < 0x14', MEASURED 36/36; kimi M_STORE1)
+                                                    -> `inword rdawr' (0x5a), `unnamed rdawr' (0x5a), `half wr rdawr'
+                                                       (0xbb78): one read-back per class -- named (ieicr/ieerr rdawr),
+                                                       in-word, unnamed, and the len-2 write
+  the READ announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23)
+                                                    -> `srvd val text' (`served 0x34' absent) -- the served byte itself
+                                                       is one the GUEST wrote (`srvd val'), not a default
+  the READ announce printing the wrong byte of a wide read (Opus M_LASTBYTE `data[len-1]', MEASURED 36/36: `wide rd
+      srvd' reads four ZERO bytes, so its channel could not vary)   -> `srvd half text' (0x56 of 0x5678, not 0x78)
+  the WRITE announce printing a wrong or constant value (Opus M_WRVAL0 `0' and M_WRDATA0 `data[0]', MEASURED 36/36 --
+      the mirror of M_O1, unrowed by the pass-2 repair)  -> `wr val text' (0x5a at len 1), `wide wr val' (0x5a5a5a5a at
+                                                       len 4, where data[0] says 0x5a)
+  the announce omitting the access width            -> `wide wr msg' / `wide rd srvd' / `srvd half text' (`(len N)')
   the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
   the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
-DISCLOSED, not caught: half-word (len 2) default accesses (the mutant that kills len 4 also kills len 2; one that
-kills ONLY len 2 is not rowed); an END-SPANNING wide read (0x3d + 4 > 0x40) takes the zero-fill path and is announced
-`served 0x00' truthfully (data[0] is what was served) but no row drives it; the announce names the FIRST served byte
-of a wide read, labelled with the width; the in-word bytes are the interior of IMPLEMENTED counters, declined here
-as a width/alignment matter (pcc2widecompose's business) -- and their served byte is the tick's, not a default,
-which is why the announce prints data[0] rather than reloading the array; the fold of 0x40..0xfff onto 0x00..0x3f
-IS the real part's: Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated'
-(_scratchpad/vmesbcp2.txt:4629; two seats had rightly called it unestablished before the manual was on disk); the
-fork's PCC2_SIZE (0x40) and the guest header's (0x1000) name different things; the IACK offsets 0x23/0x25 are
-declined like the rest -- modelling them (on the SCCRXIACK shape) would open two new entries into the C040 path, so
-pcc2c040kill goes first; `named wr'/`named rd' touch all eighteen offsets in ONE session each (valid because the
-fix has no per-offset branch; the count rows are AGGREGATES, so a per-offset failure is located by reading the
-log, not by a row) -- if a later round branches per offset this compression is invalid; "unnamed" means the FORK
-HEADER has no label, not that the part is undocumented (0x39 is SPEED's second byte, 0x3b PRTDATA's low byte);
-per-instance latch scope is not provable by fresh sessions (each is a new process; `pcc2latchinst').
+DISCLOSED, not caught: the read announce printing a RELOAD of the array instead of data[0] (Opus M_RELOAD, MEASURED
+44/44 -- expected: the two differ only on the end-span zero-fill path, where every reachable start offset's array
+byte is 0, and inside a running COUNT word, where the SIGALRM-driven tick (timer.c calls the callback from the
+handler) can land between the copy and the announce -- a race no deterministic row can pin; data[0] is what was
+served and stays the operand); len-8 default accesses (ld.d/st.d exist in cpu_m88k_instr.c; a re-kill of ONLY len 8
+passes -- outside the contract, not a breach of it); an END-SPANNING wide read (0x3d + 4 > 0x40) is announced `served
+0x00' truthfully but no row drives it; the in-word bytes are the interior of IMPLEMENTED counters, declined here as a
+width/alignment matter (pcc2widecompose's business), and inside the two COUNT words the served byte is the tick's
+while a counter runs; the disposition is value-pinned at ONE offset per class (IEICR/IEERR, 0x06, 0x21, plus 0x28 at
+len 4 and 0x06 at len 2), valid because the arm has no per-offset branch -- a member 6 scoped to a single OTHER
+offset passes (the `#392' shape if rowed per offset); the announce COUNT likewise (a silent skip of one unsampled
+offset passes, the kill form does not); the fold of 0x40..0xfff onto 0x00..0x3f IS the real part's: Motorola VMESBCP2
+Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated' (_scratchpad/vmesbcp2.txt:4629; two seats had
+rightly called it unestablished before the manual was on disk); the fork's PCC2_SIZE (0x40) and the guest header's
+(0x1000) name different things; the IACK offsets 0x23/0x25 are declined like the rest -- modelling them (on the
+SCCRXIACK shape) would open two new entries into the C040 path, so pcc2c040kill goes first; `named wr'/`named rd'
+touch all eighteen offsets in ONE session each (valid because the fix has no per-offset branch; the count rows are
+AGGREGATES, so a per-offset failure is located by reading the log, not by a row) -- if a later round branches per
+offset this compression is invalid; "unnamed" means the FORK HEADER has no label, not that the part is undocumented
+(0x39 is SPEED's second byte, 0x3b PRTDATA's low byte); per-instance latch scope is not provable by fresh sessions
+(each is a new process; `pcc2latchinst').
 The debugger's `put b' never reaches a DM_DEFAULT arm (measured): `put b ctl' is a control, not a witness.
 
 Usage: python3 pcc2_default_probe.py <gxemul> <label>      Sentinel: PCC2D_PROBE_DONE
@@ -86,6 +112,8 @@
 def LD_W(rd, off): return enc(0x05, rd, 2, off)
 def ST_B(rs, off): return enc(0x0b, rs, 2, off)
 def ST_W(rs, off): return enc(0x09, rs, 2, off)
+def LD_HU(rd, off): return enc(0x02, rd, 2, off)   # pass 3: a len-2 default read
+def ST_H(rs, off): return enc(0x0a, rs, 2, off)    # pass 3: a len-2 default write
 I_ST_SCR = enc(0x09, 5, 3, 0); I_LD_SCR = enc(0x05, 4, 3, 0); I_BR_SELF = 0xc0000000
 def program(insns, at=CODE):
     words = list(insns) + [I_BR_SELF, 0]
@@ -119,12 +147,16 @@
 row("named rd", fate(alive, how), "survived", "guest ld.bu at all 18 in one session: the READ side of the defect; a writeflag guard that re-kills reads dies here")
 row("named rd msg", t.count(MSG) if alive else "n/a", 18, "the read announce fires once per offset too")
 row("named rd srvd", t.count("served 0x") if alive else "n/a", 18, "the read announce says what happened -- SERVED, never 'ignored' (the VALUE is pinned by `srvd val text')")
-t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD]))
+t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD] + [ST_B(5, 0x06), LD_BU(4, 0x06)]) + ["print r4"])
 row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
+row("inword msg", t.count(MSG) if alive else "n/a", 12, "...twelve announces for twelve offsets; the SECOND write to 0x06 and the read-back are silent: the latch is per offset in THIS class too (Opus M_LATCHOFF)")
+row("inword rdawr", val(t, alive, how), "0x0", "...and 0x06 reads back 0x0 after two writes: DECLINED in this class too -- a member 6 scoped to the low offsets reads 0x5a (Opus M_BACKEDLOW)")
 t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
 row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
-t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED]))
+t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED] + [ST_B(5, 0x21), LD_BU(4, 0x21)]) + ["print r4"])
 row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
+row("unnamed msg", t.count(MSG) if alive else "n/a", 13, "...thirteen announces; the second write to 0x21 and its read-back are silent (per-offset latch, unnamed class)")
+row("unnamed rdawr", val(t, alive, how), "0x0", "...and 0x21 reads back 0x0: declined in the unnamed class too (a member 6 scoped by offset class reads 0x5a)")
 t, alive, how = session(setup() + program([LD_BU(4, o) for o in UNNAMED]))
 row("unnamed rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the thirteen: with named rd + inword rd every one of the 43 is read once")
 # -- the disposition-pinning rows: read-after-write in ONE session
@@ -155,16 +187,22 @@
 t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, PRTICR)]))
 row("dir wr text", t.count("unimplemented write to") if alive else "n/a", 1, "the announce says WRITE for a store (an inverted writeflag test in the text says read)")
 row("wr declined", t.count("declined") if alive else "n/a", 1, "...and the word is DECLINED (no other row counts it: `ignored' would pass every count row)")
+row("wr val text", t.count("0x30 (len 1): 0x5a -- declined") if alive else "n/a", 1, "...and the announced VALUE is the byte written: the mirror of `srvd val text' on the write arm -- `idata -> 0' printed 0x0 and passed 36 rows (Opus M_WRVAL0, MEASURED)")
 t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
 row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
 # -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
-t, alive, how = session(setup(r5="0x12345678") + program([ST_W(5, T1CMP), LD_BU(4, 0x05)]) + ["print r4"])
+t, alive, how = session(setup(r5="0x12345678") + ["r7=0xaabb"] + program([ST_W(5, T1CMP), LD_BU(4, 0x05), LD_HU(6, 0x06), ST_H(7, 0x06), LD_HU(6, 0x06), LD_BU(8, 0x05), ST_B(7, 0x07), LD_BU(9, 0x07)]) + ["print r4", "print r6", "print r8", "print r9"])
 row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
-row("srvd val text", t.count("served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served): `served 0x%02x' of 0 passes `named rd srvd' (Opus M_O1, MEASURED)")
+row("srvd val text", t.count("0x5 (len 1) -- served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served) WITH its width: `served 0x%02x' of 0 passed 23 rows (Opus M_O1, MEASURED); `(len 1)' -> `(len 4)' passed 36 (codex)")
+row("srvd half text", t.count("0x6 (len 2) -- served 0x56") if alive else "n/a", 1, "a len-2 default read at 0x06 is announced from its FIRST byte (0x56 of 0x5678): data[len-1] says 0x78 (Opus M_LASTBYTE, MEASURED 36/36); a len-2 re-kill dies here")
+row("half wr rdawr", (printed(t, "r6") if alive else fate(alive, how)), "0x5678", "...then st.h 0xaabb at 0x06 is DECLINED (silent: the bit is set) and ld.hu reads 0x5678 back: len-2 disposition; a byte-truncated backed store reads 0xbb78")
+row("srvd rd latch", (printed(t, "r8") if alive else fate(alive, how)), "0x34", "a SECOND read at 0x05 -- its bit set by the FIRST READ -- still receives 0x34: a latched-path read whose response is zeroed passes count rows (codex M_LATCH_RD_ZERO)")
+row("srvd wr latch", (printed(t, "r9") if alive else fate(alive, how)), "0x78", "st.b 0xbb at 0x07 (declined, announced) then ld.bu at 0x07 -- its bit set by a WRITE -- receives 0x78: the response is preserved on the latched path whichever direction set the bit")
 # -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
 t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
 row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
 row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
+row("wide wr val", t.count("(len 4): 0x5a5a5a5a -- declined") if alive else "n/a", 1, "...and the announced value is the WHOLE word: printing data[0] instead of idata says 0x5a (Opus M_WRDATA0, MEASURED 36/36)")
 t, alive, how = session(setup() + program([LD_W(4, PRTICR)]) + ["print r4"])
 row("wide rd", val(t, alive, how), "0x0", "a guest ld.w at PRTICR (0x30..0x33, all uncased) survives and is served the four zero bytes")
 row("wide rd srvd", t.count("(len 4) -- served 0x00") if alive else "n/a", 1, "...and the announce names the width and the first served byte")

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
already served (the register array's CURRENT byte -- the tick's, inside a running COUNT word: the announce says so);
WRITE side -- DECLINE + a per-offset latched `fatal()' ("(once)", the house idiom), NOT a backed
accept: the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear, the ICRs
mask and reassert, PSCALECNT/SPEED/the IACKs are read-only), the addition licence is unmet (no guest
reaches these offsets on this model's inspected driver paths -- if_ie never attaches), and a store into pcctwo_reg[] from the
one arm reached by 43 offsets adds a bounded-write surface the decline does not have.

CONTRACT -- what this detector is built to catch, by row (46 rows: 23 at pass 2, +13 by the pass-2 repair, +10 by the
pass-3 repair; every pass-3 row was APPENDED to an existing session):
  member 6 on the READ side of the latched path -- a read whose bit is already set gets its RESPONSE zeroed (codex
      M_LATCH_RD_ZERO: every rowed read after a preceding access expected 0 anyway)
                                                    -> `srvd rd latch' (0x34 after a read set the bit), `srvd wr latch'
                                                       (0x78 after a write set it)
  the announce's width label constant (`(int) len' -> `4', codex: no byte row required `(len 1)')
                                                    -> `srvd val text' (`0x5 (len 1) -- served 0x34'), `wr val text'
                                                       (`0x30 (len 1): 0x5a'), `srvd half text' (`(len 2)')
  (b) the verbatim `exit(1)' reinstated             -> every survival row (named/inword/unnamed wr AND rd, alias, wide)
  (d) the announce unlatched                        -> `latch sameoff' (2 lines, not 1)
  (d) one whole-arm latch bit instead of per-offset -> `latch twooff' (1 line, not 2), `named wr msg' (1, not 18)
  (d) the latch SET conditioned on writes (grok A)  -> `latch rd rd' (2, not 1), `latch rd wr' (2, not 1): with
      `latch sameoff' (W,W) and `latch rw one' (W,R) these are ALL FOUR setter x tester direction cells
  (d) the latch SET conditioned on OFFSET CLASS (Opus M_LATCHOFF, MEASURED 36/36)
                                                    -> `inword msg' (12), `unnamed msg' (13): a second write to one
                                                       offset of each class is silent; the named class is `latch sameoff'
  (d) `|=' -> `=' at the latch update (codex)       -> `latch aba' (3, not 2): bits already set survive a new offset
  (d) a writeflag guard that re-kills READS         -> `named rd' (host exit)
  (d) a width re-kill -- the removed kill was width-agnostic, so `len != 1' (grok B) or `len == 2' (grok, Fable) is a
      partial reinstatement                         -> `wide wr' / `wide rd' (len 4, host exit); `srvd half text' /
                                                       `half wr rdawr' (len 2, host exit)
  (d) a re-kill at ONE unsampled offset (Fable)     -> `inword wr' / `unnamed wr' drive all 12 / all 13, and `inword rd'
                                                       / `unnamed rd' read them: every one of the 43 uncased offsets is
                                                       written once and read once
  (d) the direction test inverted in the text       -> `dir wr text' / `dir rd text' / `wr declined'
  member 6 (BACKED ACCEPT) substituted for member 3 -> `ieicr rdawr' / `ieerr rdawr' read back the stored byte (0x5a)
      instead of 0x0 -- the DISPOSITION-pinning rows; `sccerr rdawr' (a CASED, write-to-clear sibling) is the
      control that reads 0x0 under either and makes the delta attributable
  member 6 on the LATCHED path only (Opus M_O2, MEASURED 23/23)   -> `sameoff val' (0x5a, not 0x0)
  member 6 scoped to an OFFSET CLASS (Opus M_BACKEDLOW `relative_addr < 0x14', MEASURED 36/36; kimi M_STORE1)
                                                    -> `inword rdawr' (0x5a), `unnamed rdawr' (0x5a), `half wr rdawr'
                                                       (0xbb78): one read-back per class -- named (ieicr/ieerr rdawr),
                                                       in-word, unnamed, and the len-2 write
  the READ announce printing a wrong or constant byte (Opus M_O1, MEASURED 23/23)
                                                    -> `srvd val text' (`served 0x34' absent) -- the served byte itself
                                                       is one the GUEST wrote (`srvd val'), not a default
  the READ announce printing the wrong byte of a wide read (Opus M_LASTBYTE `data[len-1]', MEASURED 36/36: `wide rd
      srvd' reads four ZERO bytes, so its channel could not vary)   -> `srvd half text' (0x56 of 0x5678, not 0x78)
  the WRITE announce printing a wrong or constant value (Opus M_WRVAL0 `0' and M_WRDATA0 `data[0]', MEASURED 36/36 --
      the mirror of M_O1, unrowed by the pass-2 repair)  -> `wr val text' (0x5a at len 1), `wide wr val' (0x5a5a5a5a at
                                                       len 4, where data[0] says 0x5a)
  the announce omitting the access width            -> `wide wr msg' / `wide rd srvd' / `srvd half text' (`(len N)')
  the `relative_addr %= PCC2_SIZE' fold changed      -> `alias msg' (the announce names offset 0x2a, not 0x6a)
  the fix perturbing a cased arm                    -> `genctl rt', `t1cmp word rt'
DISCLOSED, not caught: the read announce printing a RELOAD of the array instead of data[0] (Opus M_RELOAD, MEASURED
44/44 -- expected: the two differ only on the end-span zero-fill path, where every reachable start offset's array
byte is 0, and inside a running COUNT word, where the SIGALRM-driven tick (timer.c calls the callback from the
handler) can land between the copy and the announce -- a race no deterministic row can pin; data[0] is what was
served and stays the operand); len-8 default accesses (ld.d/st.d exist in cpu_m88k_instr.c; a re-kill of ONLY len 8
passes -- outside the contract, not a breach of it); an END-SPANNING wide read (0x3d + 4 > 0x40) is announced `served
0x00' truthfully but no row drives it; the in-word bytes are the interior of IMPLEMENTED counters, declined here as a
width/alignment matter (pcc2widecompose's business), and inside the two COUNT words the served byte is the tick's
while a counter runs; the disposition is value-pinned at ONE offset per class (IEICR/IEERR, 0x06, 0x21, plus 0x28 at
len 4 and 0x06 at len 2), valid because the arm has no per-offset branch -- a member 6 scoped to a single OTHER
offset passes (the `#392' shape if rowed per offset); the announce COUNT likewise (a silent skip of one unsampled
offset passes, the kill form does not); the fold of 0x40..0xfff onto 0x00..0x3f IS the real part's: Motorola VMESBCP2
Table 6-1 lists $FFF42040-$FFF42FFF as 'PCCchip2 Registers  Repeated' (_scratchpad/vmesbcp2.txt:4629; two seats had
rightly called it unestablished before the manual was on disk); the fork's PCC2_SIZE (0x40) and the guest header's
(0x1000) name different things; the IACK offsets 0x23/0x25 are declined like the rest -- modelling them (on the
SCCRXIACK shape) would open two new entries into the C040 path, so pcc2c040kill goes first; `named wr'/`named rd'
touch all eighteen offsets in ONE session each (valid because the fix has no per-offset branch; the count rows are
AGGREGATES, so a per-offset failure is located by reading the log, not by a row) -- if a later round branches per
offset this compression is invalid; "unnamed" means the FORK HEADER has no label, not that the part is undocumented
(0x39 is SPEED's second byte, 0x3b PRTDATA's low byte); per-instance latch scope is not provable by fresh sessions
(each is a new process; `pcc2latchinst').
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
def LD_HU(rd, off): return enc(0x02, rd, 2, off)   # pass 3: a len-2 default read
def ST_H(rs, off): return enc(0x0a, rs, 2, off)    # pass 3: a len-2 default write
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
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in INWORD] + [ST_B(5, 0x06), LD_BU(4, 0x06)]) + ["print r4"])
row("inword wr", fate(alive, how), "survived", "ALL twelve bytes inside the four 32-bit counter/compare words: no case -> default: (a re-kill at any one dies)")
row("inword msg", t.count(MSG) if alive else "n/a", 12, "...twelve announces for twelve offsets; the SECOND write to 0x06 and the read-back are silent: the latch is per offset in THIS class too (Opus M_LATCHOFF)")
row("inword rdawr", val(t, alive, how), "0x0", "...and 0x06 reads back 0x0 after two writes: DECLINED in this class too -- a member 6 scoped to the low offsets reads 0x5a (Opus M_BACKEDLOW)")
t, alive, how = session(setup() + program([LD_BU(4, o) for o in INWORD]))
row("inword rd", fate(alive, how), "survived", "...and a guest ld.bu at each of the twelve (reads drove 18/43 offsets before this row -- codex, Fable)")
t, alive, how = session(setup(r5="0x5a") + program([ST_B(5, o) for o in UNNAMED] + [ST_B(5, 0x21), LD_BU(4, 0x21)]) + ["print r4"])
row("unnamed wr", fate(alive, how), "survived", "ALL thirteen offsets the fork header does not name (the manual names some: 0x39 is SPEED's 2nd byte, 0x3b PRTDATA's)")
row("unnamed msg", t.count(MSG) if alive else "n/a", 13, "...thirteen announces; the second write to 0x21 and its read-back are silent (per-offset latch, unnamed class)")
row("unnamed rdawr", val(t, alive, how), "0x0", "...and 0x21 reads back 0x0: declined in the unnamed class too (a member 6 scoped by offset class reads 0x5a)")
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
row("wr val text", t.count("0x30 (len 1): 0x5a -- declined") if alive else "n/a", 1, "...and the announced VALUE is the byte written: the mirror of `srvd val text' on the write arm -- `idata -> 0' printed 0x0 and passed 36 rows (Opus M_WRVAL0, MEASURED)")
t, alive, how = session(setup() + program([LD_BU(4, PRTICR)]))
row("dir rd text", t.count("unimplemented read from") if alive else "n/a", 1, "...and READ for a load")
# -- the served VALUE: a guest word store to the CASED T1CMP puts 0x34 in its interior byte 0x05, then an uncased ld.bu there
t, alive, how = session(setup(r5="0x12345678") + ["r7=0xaabb"] + program([ST_W(5, T1CMP), LD_BU(4, 0x05), LD_HU(6, 0x06), ST_H(7, 0x06), LD_HU(6, 0x06), LD_BU(8, 0x05), ST_B(7, 0x07), LD_BU(9, 0x07)]) + ["print r4", "print r6", "print r8", "print r9"])
row("srvd val", val(t, alive, how), "0x34", "the served byte is the array's CURRENT byte, here one the guest wrote through the cased word arm -- not a default")
row("srvd val text", t.count("0x5 (len 1) -- served 0x34") if alive else "n/a", 1, "...and the announce prints THAT byte (data[0], what was served) WITH its width: `served 0x%02x' of 0 passed 23 rows (Opus M_O1, MEASURED); `(len 1)' -> `(len 4)' passed 36 (codex)")
row("srvd half text", t.count("0x6 (len 2) -- served 0x56") if alive else "n/a", 1, "a len-2 default read at 0x06 is announced from its FIRST byte (0x56 of 0x5678): data[len-1] says 0x78 (Opus M_LASTBYTE, MEASURED 36/36); a len-2 re-kill dies here")
row("half wr rdawr", (printed(t, "r6") if alive else fate(alive, how)), "0x5678", "...then st.h 0xaabb at 0x06 is DECLINED (silent: the bit is set) and ld.hu reads 0x5678 back: len-2 disposition; a byte-truncated backed store reads 0xbb78")
row("srvd rd latch", (printed(t, "r8") if alive else fate(alive, how)), "0x34", "a SECOND read at 0x05 -- its bit set by the FIRST READ -- still receives 0x34: a latched-path read whose response is zeroed passes count rows (codex M_LATCH_RD_ZERO)")
row("srvd wr latch", (printed(t, "r9") if alive else fate(alive, how)), "0x78", "st.b 0xbb at 0x07 (declined, announced) then ld.bu at 0x07 -- its bit set by a WRITE -- receives 0x78: the response is preserved on the latched path whichever direction set the bit")
# -- wide accesses at default offsets: the old kill was width-agnostic, so a `len != 1' re-kill is a partial reinstatement (grok B)
t, alive, how = session(setup(r5="0x5a5a5a5a") + program([ST_W(5, IEERR), LD_W(4, IEERR)]) + ["print r4"])
row("wide wr", val(t, alive, how), "0x0", "a guest st.w at IEERR (0x28..0x2b, all uncased) survives and is declined: reads back 0x0 (a memcpy-backed store reads 0x5a5a5a5a)")
row("wide wr msg", t.count("offset 0x28 (len 4)") if alive else "n/a", 1, "...announced once, with the width; the ld.w at the same offset is silenced by the per-offset bit")
row("wide wr val", t.count("(len 4): 0x5a5a5a5a -- declined") if alive else "n/a", 1, "...and the announced value is the WHOLE word: printing data[0] instead of idata says 0x5a (Opus M_WRDATA0, MEASURED 36/36)")
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
index 65930c2..9e9409d 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1303,6 +1303,33 @@ else
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
+        "named rd srvd" "inword wr" "inword msg" "inword rdawr" "inword rd" "unnamed wr" \
+        "unnamed msg" "unnamed rdawr" "unnamed rd" "ieicr rdawr" "ieerr rdawr" "sccerr rdawr" \
+        "latch sameoff" "sameoff val" "latch twooff" "latch rw one" "latch rd rd" "latch rd wr" \
+        "latch aba" "alias 0x6a" "alias msg" "dir wr text" "wr declined" "wr val text" \
+        "dir rd text" "srvd val" "srvd val text" "srvd half text" "half wr rdawr" "srvd rd latch" \
+        "srvd wr latch" "wide wr" "wide wr msg" "wide wr val" "wide rd" "wide rd srvd" \
+        "genctl rt" "t1cmp word rt" "put b ctl" "put b ctl msg"; do
+        check "pcc2 default row: $v" "$(count "$PCC2DLOG" "^$v  .*ok$")" "1"
+    done
+    check "pcc2 default rows emitted" "$(( $(count "$PCC2DLOG" " ok$") + $(count "$PCC2DLOG" " FAIL$") ))" "46"
+    check "pcc2 default rows green"   "$(count "$PCC2DLOG" " ok$")"   "46"
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
`regress/pcc2_default_probe.py`, 46 rows (23 at pass 2; +13 by the pass-2 repair, +10 by the pass-3 repair, below), run by gate 14.  Witness: rung 3, measured before the edit.**

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

READ: keep the byte the memcpy served and SAY it is served -- it is the register array's CURRENT byte (inside a running
COUNT word, the tick's; the pass-1 design said "default, not a computed value", corrected at pass 2), so this is not
the option set's member 4 and a bounded announce about it is not a wrong record.  WRITE:
member 3, DECLINE + latched announce -- NOT member 6 (backed accept), on three warrants the seats measured or read:
the file's own cased siblings contradict a blanket store (SCCERR is write-to-clear -- the board manual's SCLR bits
read as zero; the ICRs mask and reassert; PSCALECNT/SPEED/the IACKs are read-only); the addition licence is unmet
(no inspected OpenBSD driver path reaches these offsets on this model -- the rung-3 witness is itself a guest, so the
pass-1 wording "no guest reaches" was too wide: codex, pass 2); a store from the one arm 43 offsets reach adds a bounded-write
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

## The detector as it shipped at PASS 2 (`regress/pcc2_default_probe.py`, 23 rows then; 46 now -- see the pass-2 and pass-3 sections; gate 14 pins all 46)

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
prediction ENUMERATED sixteen red rows -- the measured set exactly -- and CALLED them fifteen, so its derived score was
8/23 against a measured 7/23 (the first draft of this sentence said "listed fifteen"; the set was right and only the
numeral and the derived score were wrong -- Opus, codex, kimi, pass 2) -- an arithmetic slip in the
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
the gate cannot count is a detector whose OWN summary reads green while the gate counts nothing of it -- and the
gate is the check that saw it, FAIL 25/844 (the first draft said "would have shipped green", which overstated: it
could not have shipped past that gate -- codex, pass 2), which is what a gate is for.*

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
the SIGALRM tick writes back the two COUNT words (`dev_pcc2.c` `write32(&d->pcctwo_reg[PCCTWO_T1COUNT]..` and T2COUNT)
-- so for the six bytes inside those two words the announced byte could differ from the served one while a counter
runs.  `"the array's default, NOT a computed value"` was therefore also wrong for those six.  **Pass 3 narrowed and
settled this in three readings.**  grok: the tick only READS the compare words and CEN is off at init, so under this
instrument -- `srvd val` lives in T1CMP's interior -- `data[0]` and a reload are the same byte, and `srvd val text` pins
the constant-0 mutant, NOT the reload (Opus then MEASURED the reload mutant at a clean sweep; disclosed in the contract).
Fable: the mid-handler race is unreachable because ticks run between guest instructions -- REFUTED by reading
`src/core/timer.c`: `timer_tick(int signal_nr)` IS the SIGALRM handler and calls `timer->timer_tick(timer, timer->extra)`
directly, and `dev_pcc2.c` registers `pcc_timer_tick` with `timer_add`, so the pcc2 tick is signal-driven and can land
anywhere, the copy-to-announce gap included.  Fable's SECOND reason needs no timing and is added to the comment: on the
#119 END-SPAN path the read is zero-filled while the array byte is kept, so a reload would announce a value the guest
did not receive (Opus adds a third backstop: `memory_rw.c` `#95` pre-zeroes the buffer before device dispatch).
`data[0]` is definitionally what was served -- the right operand under every reading.

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

**Every one of the twelve predictions was EXACT in score and red set -- with one VALUE miss in the safe direction that
the first draft of this section did not record (Opus, pass 3): `PRETABLE_501b.out` predicts `latch sameoff 2` under
M_UNLATCH and the row measured `got=3`, because the repair had appended a read-back to that session (three accesses,
three announces unlatched); the row is red either way -- and every one of the six pass-2 escapes is
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

`pcc2 default rows emitted 36 / green 36 / red 0`; `pcc2 width rows emitted 251 / green 251 / red 0`; **857 checks** (the gate's own `PASS (857 checks)` line; 844 at pass 2 + 13 new default rows = 857 -- an earlier draft said 875 from `grep -c ' ok '`, which counts 18 non-check lines too: the grok and Opus seats caught it against the log the sentence named), 0 FAIL, `GATE_RC=0`.
The gate's name list for the default section is DERIVED from the probe's `row("...")` calls by the repair script (36
names, none longer than 14 characters -- the gate's `%-16s` + two-space anchor would silently stop counting a longer
one), so the list and the probe cannot disagree by transcription.

## Pass 3 (nine seats on the pass-2 repair diff, `_scratchpad/panel_20260905_081718`): the repair had reproduced the breach it closed, on the other arm

**Roster.**  codex (GPT-6 Astra, max; a reconnect storm mid-run, then a 9 KB final answer), grok, kimi (the 81 KB pointer
form paged fine this time -- 124 KB of derivation -- but the CLI EXITED while it slept on its own scratch build in `~/p3m`,
so there is NO VERDICT LINE; its derivations are used and it is recorded as a reading, not a seat failure and not
agreement), deepseek and minimax (answered the 19 KB packet), **glm SEAT FAILURE** (thinking-burned on the 19 KB packet
AND on a 2 KB one-question mini packet -- both burns kept as `ollama_glm.burn*.txt`; the mini's open-ended "name the
smallest edit" is the likely trigger, since pass 2's closed-question mini had landed), Opus 5 and Fable 5 (Agent seats,
preserved as `opus5.txt` / `fable5.txt`).  agy DELIBERATELY NOT FIRED.  Three seats said close (grok, deepseek, minimax),
Fable GO-WITH-CHANGES after two L4s, codex NO-GO, Opus NOT CLOSE -- **and Opus MEASURED.**

**Six clean sweeps of the 36-row instrument, measured by the Opus seat in its own scratch clone** (BASE reproduced at
36/36; instrument md5 verified equal to the frozen table-3 pair; every mutant two diff lines, rebuilt from a removed
`.o`, probed with the unedited instrument; sentinel discipline and a `RESTORE_CMP_CLEAN_VS_SEC` line; nothing written to
any project tree):

| mutant | edit | why 36 rows could not see it |
|---|---|---|
| M_WRVAL0 | the WRITE announce's `(int) idata` -> `0` | **the mirror of pass 2's M_O1**: the value channel was pinned on the READ arm only (`srvd val text`); every write-side row counts a phrase -- `#499` reproduced inside its own repair |
| M_WRDATA0 | `(int) idata` -> `data[0]` | same cell; the edit the new symmetric-looking comment invites -- prints `0x5a` for a `0x5a5a5a5a` word write |
| M_LASTBYTE | the READ announce's `data[0]` -> `data[len-1]` | `wide rd srvd` reads PRTICR, whose four bytes are all zero and unreachable by a guest write -- its channel CANNOT VARY under a byte-selection mutant: the pre-table CHANNEL check's own failure mode, and the contract had claimed "a wrong or constant byte -> `srvd val text`" |
| M_RELOAD | `data[0]` -> `d->pcctwo_reg[relative_addr]` (reverts the pass-2 product repair) | the two differ only in a race (the COUNT words, while a counter runs, under the SIGALRM-driven tick) or on the end-span path, where every reachable start offset's array byte is 0 -- **no deterministic row can pin it**: DISCLOSED |
| M_BACKEDLOW | `if (writeflag == MEM_WRITE && relative_addr < 0x14) pcctwo_reg[ra] = idata;` | member 6 conditioned off the two offsets that read back: the FATE axis was closed at 43 offsets, the DISPOSITION axis at two (kimi derived the same store, M_STORE1) |
| M_LATCHOFF | the latch SET restricted to IEICR/IEERR | the same class on the latch axis: every count row lives at the named offsets |

codex, reading, DERIVED three more that pass 36 rows: **M_LATCH_RD_ZERO** -- `else if (writeflag == MEM_READ) data[0] =
0;` on the latched path, the mirror of M_O2 on the READ response channel (every rowed read after a preceding access
expected 0 anyway; `srvd val` read its nonzero byte with the latch clear); and the width label made constant on either
arm (`(int) len` -> `4`: no byte row required `(len 1)`).  grok and Fable named `if (len == 2) exit(1);` -- the len-2
re-kill the pass-2 contract had DISCLOSED.  kimi named the write-value hole independently (M_WVAL0).

**Adjudication (count the arguments).**  The three close verdicts and Fable's had not built the edits; Opus had.  The
write-announce value is the cell the pass-2 repair should have closed with its mirror: two consecutive passes found the
value channel unpinned, one arm each -- the repair-chain amendment's trigger -- so the class is closed in one diff here:
**ten rows, every one APPENDED to an existing session** (zero new sessions): `wr val text` and `wide wr val` (the write
value at len 1 and len 4; the wide one separates `idata` from `data[0]`); `srvd half text` and `half wr rdawr` (a len-2
read served and announced from its FIRST byte, 0x56 of 0x5678 -- two bytes that differ, so a byte-selection mutant
reds -- and a len-2 write declined: the len-2 disclosure CLOSED); `srvd rd latch` and `srvd wr latch` (a nonzero byte
re-read after its bit was set by a read and by a write); `inword msg`/`inword rdawr` and `unnamed msg`/`unnamed rdawr`
(one announce count and one read-back per remaining offset CLASS, the named class already having `latch sameoff` and
the `rdawr` rows); and `srvd val text` reworded to count `0x5 (len 1) -- served 0x34` so the width label is
load-bearing at len 1.  Two encoders (`LD_HU`, `ST_H`) borrowed from the width probe.  The product is untouched except
two comment sentences.  46 rows; every name still under 14 characters.

**Dispositions the pass changed or narrowed.**  F2 #7 (codex's tick reason for `data[0]`): grok narrowed it -- the tick
writes back only T1COUNT/T2COUNT and only while a counter runs, so under this instrument `data[0]` and a reload are the
same byte and `srvd val text` pins the constant-0 mutant, not the reload; Fable REFUTED it -- "ticks run between guest
instructions, not inside `memory_rw`" -- and that refutation is itself refuted by reading `src/core/timer.c`:
`timer_tick(int signal_nr)` is the SIGALRM handler and calls `timer->timer_tick(timer, timer->extra)` directly, while
`dev_pcc2.c` registers `pcc_timer_tick` with `timer_add`, so the pcc2 tick is signal-driven and can land in the
copy-to-announce gap.  Fable's second reason needs no timing and is added to the comment: on the `#119` end-span path
the read is zero-filled while the array byte is kept.  Opus adds a third backstop, `memory_rw.c` `#95` pre-zeroing the
buffer before dispatch.  `data[0]` -- what was served -- is the right operand under every reading; M_RELOAD is disclosed
as unrowable, with that reason.  The kimi/grok/Opus offset-class residual is closed per CLASS and disclosed per single
offset (`#392` if rowed per offset); the write-announce value is closed; len 8 (`ld.d`/`st.d` exist in the m88k core)
stays disclosed beside end-span reads and per-instance latch scope; the "F2 #10 safety sentence" is narrowed (codex): it
says only that no previously successful trace entered the arm, not that the surviving arm is boot-validated.  Rejected:
minimax's and deepseek's close verdicts were readings of the packet and are overtaken by the measurements.  The pass-2
`pcc2dispall` filing is WITHDRAWN as filed -- its two items are now rows.

**Records defects found by the pass, corrected in place** (codex, grok, Opus, Fable): the gate paragraph's "875 checks"
-- the gate's own line says `PASS (857 checks)` and `grep -c ' ok '` had counted 18 nested probe lines; the opening
summary and the detector heading still said 23 rows (now 46, with the history); the four pass-1 sentences the pass-2
section had corrected only in a LATER paragraph -- "the array's default", "no guest reaches", "listed fifteen", "would
have shipped green" -- are now corrected in their own sentences with the first wording quoted; the table-3 section did
not record the `latch sameoff` value miss (predicted 2 under M_UNLATCH, measured 3 -- the appended read-back announces
too; red either way); the "twelve interiors" tick rationale (six); the pass-3 `SEATS.txt` says kimi MISSING because it
was written before the kimi answer landed (the file stands; this sentence is the reconciliation).

## Table 4 (`killtable4_20260905/driver.log`; predictions in `PRETABLE_501c.out`, mtime 09:08:39, table launched 09:09; frozen repaired instrument md5 `b9b2fadc` == live; the pass-3 instrument `old36/` md5 `10737375`; scratch clone of build/, BASE rebuilt in the clone, twenty-two mutants each compile-checked before the table and proven by a diff count; driver parse-checked before exec)

**Every one of the ten pass-3 escapes is MEASURED on the same binary by both instruments: 36/36 on the instrument that
shipped at pass 3, red on the repaired one on exactly the rows built for it -- and the disclosed exception, M_RELOAD,
measured 46/46 on the repaired instrument as the contract predicts.**  Seventeen of twenty-two predictions were EXACT in
score and red set; five missed in the SAFE direction only (extra reds, no predicted red went green), all of one class,
named below with their values.

| mutant | shape | repaired instrument (46 rows) | red rows | pass-3 instrument (36) |
|---|---|---|---|---|
| BASE | the repaired working set | **46/46** | -- | **36/36** (control) |
| M_WRVAL0 | write announce value `-> 0` (Opus) | 44/46 | wr val text, wide wr val | **36/36** -- the breach |
| M_WRDATA0 | write announce value `-> data[0]` (Opus) | 45/46 | wide wr val (a byte write's idata IS data[0], so `wr val text` stays -- as predicted) | **36/36** |
| M_LASTBYTE | read announce `data[len-1]` (Opus) | 45/46 | srvd half text (says `served 0x78`) | **36/36** |
| M_RELOAD | read announce reloads the array (Opus) | **46/46 -- DISCLOSED ESCAPE, as predicted** | none: no deterministic row can pin it (a race in the COUNT words under the signal-driven tick, or the end-span path where every reachable start byte is 0) | **36/36** |
| M_BACKEDLOW | member 6 for `relative_addr < 0x14` (Opus) | 43/46 | inword rdawr (0x5a), half wr rdawr (0xbb78), srvd wr latch (0xbb) | **36/36** |
| M_LATCHOFF | latch SET only at IEICR/IEERR (Opus) | 42/46 (pred 43) | inword msg 14, unnamed msg 15, srvd half text 2, **+ srvd val text 2** (safe miss, see below) | **36/36** |
| M_HALFKILL | `if (len == 2) exit(1);` (grok, Fable) | 40/46 | the six srvd-session rows (the session dies at its `ld.hu`) | **36/36** (no len-2 access there) |
| M_LATCHRD0 | `else if (writeflag == MEM_READ) data[0] = 0;` (codex, derived) | 43/46 | srvd rd latch (0x0), srvd wr latch (0x0), half wr rdawr (0x78) | **36/36** |
| M_LEN4R | read announce `(int) len -> 4` (codex, derived) | 44/46 | srvd val text, srvd half text | **36/36** |
| M_LEN4W | write announce `(int) len -> 4` (codex, derived) | 45/46 | wr val text | **36/36** |
| M_EXIT | (b) the verbatim `exit(1)` arm | 7/46 | the 29 of table 3 + all ten new rows | (table 3: 7/36) |
| M_UNLATCH | (d) announce unlatched | 36/46 (pred 37) | the six of table 3 (latch sameoff 3) + inword msg 14, unnamed msg 15, srvd half text 2, **+ srvd val text 2** | (30/36) |
| M_ONELATCH | (d) one whole-arm bit | 38/46 | the five of table 3 + inword msg 1, unnamed msg 1, srvd half text 0 | (31/36) |
| M_BACKED | member 6, every write | 38/46 | the four of table 3 + inword rdawr, unnamed rdawr (0x5a), half wr rdawr (0xaabb), srvd wr latch (0xbb) | (32/36) |
| M_RDKILL | (d) reads re-killed | 16/46 (pred 18) | the 19 of table 3 + the nine predicted + **inword wr, unnamed wr** (their sessions now END in a read the mutant kills) | (17/36) |
| M_DIRSWAP | (d) direction test inverted | 37/46 | the six of table 3 + wr val text, wide wr val, srvd half text | (30/36) |
| M_WRLATCH | latch SET only on writes (grok A) | 43/46 (pred 44) | latch rd rd, latch rd wr, **+ srvd val text 2** | (34/36) |
| M_WIDEKILL | `if (len != 1) exit(1);` (grok B) | 35/46 | the four of table 3 + wide wr val + the six srvd-session rows | (32/36) |
| M_OFFKILL | `if (relative_addr == 0x06) exit(1);` (Fable) | 36/46 | the two of table 3 + inword msg, inword rdawr + the six srvd-session rows | (34/36) |
| M_SRVD0 | read announce value `-> 0` (Opus, pass 2) | 44/46 | srvd val text, srvd half text | (35/36) |
| M_BACKED2 | member 6 on the latched path (Opus, pass 2) | 42/46 | sameoff val, inword rdawr, unnamed rdawr (0x5a), half wr rdawr (0xbb78) -- `srvd wr latch` stays 0x78: the st.b at 0x07 is a FIRST write there, declined | (35/36) |
| M_ABA | `\|=` `->` `=` (codex, pass 2) | 42/46 (pred 43) | latch aba 3, inword msg 13, unnamed msg 14, **+ srvd val text 2** | (35/36) |

**The five safe misses are ONE class, recorded with their values:** the repair appended a re-read of 0x05 to the served-value
session (`LD_BU(8, 0x05)`, the `srvd rd latch` row), so under any mutant that leaves 0x05 UNLATCHED at that point -- the
latch disabled (M_UNLATCH), scoped to IEICR/IEERR (M_LATCHOFF), set only on writes (M_WRLATCH), or forgotten by `=`
(M_ABA) -- the re-read announces a second `0x5 (len 1) -- served 0x34` and `srvd val text` counts 2 against a want of 1.
The prediction listed `srvd half text 2` for the same reason and missed its neighbour.  M_RDKILL's two extra reds are the
in-word and unnamed WRITE rows, whose sessions now end in the read-back the mutant kills.  Every predicted red went red;
no predicted red stayed green.  The table-3 section's late-recorded `latch sameoff 3` was the same family.

Denominator of this zero: twenty-two mutant shapes, named above; the cells closed are the announce's five channels (fate,
count, direction, width, value) on BOTH arms; the setter x tester direction product (four); accumulation across offsets;
the disposition AND the read response on the latched path; served value at len 1 and len 2; widths 1, 2 and 4 in both
directions; every one of the 43 uncased offsets driven once in each direction, with one announce count and one
read-back per offset CLASS.  EXCLUDED, disclosed in the contract: the reload of the array (M_RELOAD, measured 46/46 --
outside the contract by construction); len 8; an end-spanning wide read; a member 6 or a latch scoped to a SINGLE
unsampled offset; per-instance latch scope; `debug()` for `fatal()` (the probe steps, so both print).

One run.  The clone's source was `cmp`-clean against SEC after the restore rebuild and its sentinel cleared.

## Gate 14 on the pass-3 instrument (`killtable4_20260905/gate14_501c.log`; the live probes -- default md5 `b9b2fadc` == the table-4 frozen instrument, width `a080e2bc`; run alone 10:46-11:23 on a build/ that had passed the two-part clearance in the same chained job, after `propagate3.sh` rebuilt build/, build-asan/ and the arc rig and est/ was copied by hand)

`pcc2 default rows emitted 46 / green 46 / red 0`; `pcc2 width rows emitted 251 / green 251 / red 0`; the gate's own line `PASS (867 checks)` (857 at pass 3 + 10 new default rows = 867), 0 FAIL, `GATE_RC=0`.  The name list is derived from the probe's `row("...")` calls by the repair script (46 names, longest 14 characters).

<<PANEL501P4_OWED>>

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
362	0	CHANGELOG.md
27	0	regress/gate_arm.sh
20	6	regress/sgi_de_primop_probe.py
43	7	src/devices/dev_pcc2.c
199	1	tools/pipeline/ledger.json
?? regress/artifacts/pcc2defaultkill/killtable3_20260905/
?? regress/artifacts/pcc2defaultkill/killtable4_20260905/
?? regress/artifacts/pcc2defaultkill/killtable_20260905/
?? regress/artifacts/pcc2defaultkill/pass2_seats/
?? regress/artifacts/pcc2defaultkill/pass3_seats/
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
