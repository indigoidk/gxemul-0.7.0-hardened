# pcc2widthkills -- PASS 3: the repair made in response to pass 2 owes its own pass.  Detector 60 -> 82 rows; product diff is COMMENTS + one typedef.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly,
and this round's own pass 2 refuted a reachability census the author had written into product
code (five even blocks; it is six).  **Check the premises, not just the derivations.**  Where I
state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of
`b78bb0f`.**  Three pristine-2021 copies under the project root are NOT this fork.  If your line
numbers disagree with mine by hundreds you are reading one of them -- say so.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- a lane value under a mask, a count of blocks,
a latch-bit cardinality -- ENUMERATE it rather than reasoning about it.**  Walk the values.
And ENUMERATE THE RIGHT DOMAIN: ask what the PRODUCER of these values can emit before you walk
them (the m88k core alignment-checks every non-byte access BEFORE memory_rw).

**VERDICT LINE FIRST**, so your answer survives truncation.

## WHY THIS PASS EXISTS (the repair chain, and what makes it terminate)

Pass 2 (commit `b78bb0f`, 60-row detector) was found by its measuring seat to have SIX clean
sweeps, the smallest a ONE-CHARACTER latch-bit alias.  A repair made in response to a pass 2
OWES ITS OWN PASS, scoped to the repair diff; the chain closes on the first VALID pass finding
zero floor breaches, with the denominator named.  **Review EFFORT is scoped to this diff.  The
FLOOR QUESTION -- does a clean-sweep mutant exist in the clause-(d) enumeration -- is asked of
the SHIPPED COMPOSITE (all 82 rows) on this pass.**  Two consecutive passes found breaches of
ONE class (uncovered cells of a 12-block x shape space), so this repair is a CLASS CLOSURE and
your job is to VERIFY THE ENUMERATION rather than hunt cells one at a time.

## N. PREMISES ALREADY SETTLED, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled by pass 1 / pass 2 / the pass-2 builder (panel_20260903_121558 and
`regress/artifacts/pcc2widthkills/opus_pass2_20260903/RESULTS.md`), warrants inline:

1. **The width is LEGAL** -- `mvme_pcctworeg.h`: the registers "can be accessed as bytes,
   two-bytes, or four-bytes".  Tree header, not a guess.
2. **`memory_readmax64` composes BIG-ENDIAN**, so `(uint8_t) idata` is the HIGHEST-address
   lane; a bare deletion of the guard stores the NEIGHBOUR's byte.  MEASURED: `M_DELETE` ->
   `rb genctl` reads 0xbb.
3. **Reachability, CORRECTED by pass 2:** every non-byte m88k access is alignment-checked
   before memory_rw and `relative_addr %= 0x40` keeps parity, so the SIX even-offset blocks
   (GENCTL 0x02, TxCTL 0x16, TxICR 0x1a, SCCERR 0x1c, SCCTX 0x1e, IPL 0x3e) are GUEST-reachable
   and the SIX odd ones (VECBASE, PSCALEADJ, SCCICR, SCCRX, SCSIICR, MASK) are OPERATOR-reachable.
   The old comment said five; IPL at 0x3e is even.
4. **The operator path reaches the SAME guard.** Debugger `put h` at an odd address warns, then
   calls `store_16bit_word` -> ONE `memory_rw(len 2)` -> the same `DEVICE_ACCESS` arm a guest
   would reach (verified by the builder from source, and MEASURED pre-fix: exit1).  Guest byte
   stores (`st.b`) at odd offsets are fine -- only non-byte accesses are alignment-checked.
5. **Arm bodies, read from the file (inlined below): SCCICR stores `idata & 0x1f`; SCCRX and
   SCSIICR store `idata & 0xdf`; each then calls `reassert_interrupts()`.  PSCALEADJ's write
   body STORES NOTHING -- it only prints "write to PSCALEADJ ignored (value ...)".**
   Seven of the twelve blocks call `reassert_interrupts()` (derived by awk over the arms; the
   earlier "six" was wrong and is corrected in the comment).
6. **`fatal()` returns** (`debugmsg.c`: no early-out, no exit).  The decline announces once per
   block per instance via `d->warned`, a 12-bit field written ONLY by `pcc2_width_decline()`.
7. **NOT fixed and cited:** `pcc2c040kill` (a legal byte write of 0x04 to GENCTL still ends the
   host in `reassert_interrupts`), `pcc2defaultkill`, `pcc2counter8`.  Every GENCTL lane value
   in the probe keeps bit 0x04 clear.
8. **The pass-2 ruling, adopted:** clause (d) is a FLOOR.  A guard kept with its decline nulled
   while the write lands (announce-then-land) at the four odd arms was "a sentence owed" in the
   repair's own PRETABLE Section 2; the builder asked whether a disclosure can discharge a floor
   clause.  It cannot.  Four rows were added instead (Section 5 of PRETABLE, inlined below).
9. **Pass-2 roster:** eight of nine answered (agy DELIBERATELY NOT FIRED, reserved for
   measurement); the Opus seat was the sole builder and then ran its own pass 3 unprompted.

## THE TABLES (every number below names its log; a zero without a denominator does not close)

Table 2 part 1 -- `killtable2_20260903/part1/driver.log`, 78-row instrument, scratch clone,
BASE rebuilt in the clone:
    BASE               78/78   -
    M_DELETE_MASK      75/78   latch all,op mask dcl,rb mask
    M_KILL_IPL         71/78   latch all,latch all lv,hrd ipl,hrd ipl lv,hwr ipl,hwr ipl lv,hwr ipl dcl
    M_KILL_MASK        73/78   latch all,latch all lv,op mask,op mask dcl,rb mask
    M_DELETE           72/78   rb genctl,rb genctl dcl,rb genctl lo,latch all,latch same,latch two
    M_DELETE_TXICR     74/78   rb t2icr,rb t2icr dcl,latch all,op t1icr dcl
    M_LENGT2_TXICR     74/78   rb t2icr,rb t2icr dcl,latch all,op t1icr dcl
    M_LENGT2_TXCTL     73/78   rb t2ctl,rb t2ctl dcl,latch all,latch two,op t1ctl dcl
    M_LENGT2_SCCTX     75/78   rb scctx,rb scctx dcl,latch all
    M_LENGT2_SCCERR    76/78   hwr sccerr dcl,latch all
  (the driver then died on the author's quoting at the 10th mutant; the 9 above stand.)

The builder's PASS 3 -- `opus_pass2_20260903/../pass3/kill3.log` (frozen 78-row instrument
md5 d9239db6, product 6fdb3880; its six pass-2 sweeps re-measured):
    BASE2              78/78   -
    M1                 77/78   latch all
    M2                 75/78   latch all,op mask dcl,rb mask
    M6                 77/78   rb mask
    M7                 71/78   latch all,latch all lv,hrd ipl,hrd ipl lv,hwr ipl,hwr ipl lv,hwr ipl dcl
    M8                 75/78   rb scctx,rb scctx dcl,latch all
    M9                 75/78   latch all,op mask dcl,rb mask

The builder's PASS 3b -- the four odd-arm FALL-THROUGHS vs the 78-row detector (the breach):
    M_FALL_SCCICR      78/78   -
    M_FALL_SCCRX       78/78   -
    M_FALL_SCSIICR     78/78   -
    M_FALL_PSCALEADJ   78/78   -

The builder's PASS 3c -- the same four vs the 82-row repair (frozen md5 cd22f951):
    BASE3              82/82   -
    M_FALL_SCCICR      81/82   rb sccicr
    M_FALL_SCCRX       81/82   rb sccrx
    M_FALL_SCSIICR     81/82   rb scsiicr
    M_FALL_PSCALEADJ   81/82   op pscale noig

Part 2 (mine) -- the pre-table block's own yield, `idata > 0xff` operand swap, vs 82 rows:
    BASE               82/82   -
    M_IDATA_GENCTL     80/82   rb genctl lo,latch all

## QUESTIONS

1. **THE PREMISE AUDIT, as questions.**  (a) Is the clause-(d) enumeration now CLOSED?  The
   inputs are `len`, `writeflag`, `relative_addr` (-> block), `idata`, `d->warned`.  The shapes
   measured are: guard deleted, `len != 1` -> `len > 2`, verbatim `exit(1)` reinstated, latch-bit
   ALIAS (one enum member for two blocks), announce-then-fall-through, and the operand swap
   `len != 1` -> `idata > 0xff`.  Enumerate 12 blocks x 6 shapes = 72 cells and say WHICH cells
   have a measured kill, which are argued equivalent, and which are UNMEASURED.  Do not accept
   "every block has a dcl row" as coverage of the fall-through shape -- pass 2 found that a
   `dcl` row cannot vary under a mutant that keeps announcing.
   (b) Is `latch all` a sound CARDINALITY row?  It writes one wide 0x0003 per BLOCK through the
   operator path and expects TWELVE announces.  Can any benign traffic in that session set a bit
   early so that an aliased pair still reads 12?  Can two blocks announce on one bit and still
   count 12 (e.g. because the session touches a block twice)?
   (c) Is `op pscale noig` a REAL channel -- does PSCALEADJ's "ignored" print reach the pty
   transcript the row counts, and is 0 the right expectation on the fix?
   (d) Are the three new readbacks (`rb sccicr/sccrx/scsiicr`: st.b 0x1f, put h 0xaab8, ld.bu ->
   0x1f) correct on the FIX?  Under a fall-through they land 0x18 (& 0x1f) or 0x98 (& 0xdf) and
   call `reassert_interrupts()` -- could that call END THE HOST (the pcc2c040kill class) and
   make the row "died" rather than a readback?  Either is red, but the record should say which.

2. **THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES 82 ROWS.**  Name the row you expect to
   stay green.  Shapes NOT in the tables above are the interesting ones.

3. **OPTION-SET COMPLETENESS: N/A this pass** -- no disposition is chosen here; the direction
   split (reads ACCEPT, writes DECLINE + latched announce) was settled in pass 1 and is not
   re-litigated.  Say so if you disagree that it is N/A.

4. **IS THE RECORD HONEST?**  The contract (probe header) and the PRETABLE sections are inlined.
   Name any sentence that a measurement above refutes, any count without a deriver, and any
   claim of coverage no row carries.  PRETABLE Section 2 still says four odd arms have no
   readback and Section 5 says three now do: is the composite document internally consistent?

If, while verifying a claim, you found something ELSE -- say so.

## THE ENCLOSING CODE (the helper and the four odd arms whose rows are new; whole arms, both
## exit paths, from the CURRENT file)

```c
static void pcc2_width_decline(struct pcc2_data *d, int bit, const char *name, int len)
{
	if (!(d->warned & (1u << bit))) {
		d->warned |= (1u << bit);
		fatal("[ pcc2: unimplemented len=%i write to %s -- declined."
		    "  (once) ]\n", len, name);
	}

	case PCCTWO_PSCALEADJ:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			fatal("[ pcc2: write to PSCALEADJ ignored (value "
			    "0x%02x) ]\n", (int)idata);
		}
		break;

	case PCCTWO_T2CTL:
	case PCCTWO_T1CTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			/*  PCC2_TCTL_CEN and PCC2_TCTL_COC:  */
			d->pcctwo_reg[relative_addr] &= 0xfc;
			d->pcctwo_reg[relative_addr] |= (idata & 3);

			if (idata & PCC2_TCTL_COVF)
				d->pcctwo_reg[relative_addr] &=
				    ~(PCC2_TCTL_OVF | PCC2_TCTL_COVF);

			if (idata & ~7)
				fatal("[ pcc2: HUH? write to PCCTWO_TxCTL"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_SCCICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCTX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCTX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCRX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRXIACK:
		/*  TODO. Hm. Is this enough?  */
		d->pcctwo_reg[PCCTWO_SCCRX] &= ~PCC2_IRQ_INT;
		reassert_interrupts(d);
		break;

	case PCCTWO_SCSIICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCSIICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_IPL:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above.  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			static int w = 0;	/* #119: was exit(1) (IPL is read-only) */
			if (!w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "
			    "ignored ]\n"); w = 1; }
		} else {
			if (d->pcctwo_reg[PCCTWO_IPL] == 0) {
				static int w = 0;	/* #119: was exit(1) */
				if (!w) { fatal("[ pcc2: IPL == 0 on read ]\n");
				    w = 1; }
			}
		}
		break;
```

## THE DETECTOR DIFF (`regress/pcc2_width_probe.py`, 60 -> 82 rows, INLINED IN FULL)

```diff
diff --git a/regress/pcc2_width_probe.py b/regress/pcc2_width_probe.py
index bed9732..3deaed9 100644
--- a/regress/pcc2_width_probe.py
+++ b/regress/pcc2_width_probe.py
@@ -16,9 +16,14 @@ four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:
 CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:
 
   CATCHES
-    * reinstatement of the kill at any of the five GUEST-reachable blocks (survival
+    * reinstatement of the kill at any of the SIX GUEST-reachable blocks (survival
       rows paired with a liveness observable, because exit status cannot tell
       "declined and quit" from "died with status 0");
+    * *** pass 2: the two FOLDED-IN arms, IPL and MASK, had NO ROW -- twelve blocks
+      converted, ten given rows, and the shipped contract did not say so.  A seat
+      found it by sibling parity: MASK is GENCTL's twin and had none of GENCTL's rows.
+      Repaired: IPL is EVEN and therefore the SIXTH guest-reachable block (survival +
+      message rows); MASK is odd (operator rows) and gets GENCTL's readback. ***
     * reinstatement at any of the seven OPERATOR-reachable blocks, through the
       debugger's `put h' at an odd address -- MEASURED to warn and store and kill
       (artifacts/pcc2widthkills/operator_reach_20260903.out);
@@ -64,6 +69,12 @@ PCC2 = 0xfff42000
 #  the five GUEST-reachable blocks (even offsets) and the seven OPERATOR-reachable ones
 GENCTL, T2CTL, T2ICR, SCCERR, SCCTX = 0x02, 0x16, 0x1a, 0x1c, 0x1e
 VECBASE, PSCALEADJ, T1CTL, T1ICR, SCCICR, SCCRX, SCSIICR = 0x03, 0x15, 0x17, 0x1b, 0x1d, 0x1f, 0x2f
+#  pcc2 pass 2: THE TWO FOLDED-IN ARMS HAD NO ROW AT ALL.  A seat found that the probe
+#  touched no offset at 0x3e or 0x3f -- twelve blocks converted, ten given rows.  MASK
+#  is GENCTL's byte-identical twin (store byte, reassert); GENCTL's null-repair was
+#  caught by `rb genctl', MASK's by nothing, a 60/60 sweep.  AND IPL IS EVEN: it is the
+#  SIXTH guest-reachable block, not a seventh operator one.
+IPL, MASK = 0x3e, 0x3f
 CHIPID = 0x00
 
 
@@ -164,6 +175,9 @@ def printed(t, reg):
 
 
 def program(insns, at=CODE):
+    #  `at' lets a session run TWO programs: a second sequence at the SAME address finds
+    #  pc already there and the assignment is skipped (the Addr hazard, designed out in
+    #  the sgi probes with Addr.take()).  Callers needing two pass at=CODE + 0x100.
     words = list(insns) + [I_BR_SELF, 0]
     cmds = ["put w 0x%x, 0x%08x" % (at + 4 * i, w) for i, w in enumerate(words)]
     return cmds + ["pc=0x%x" % at, "step %d" % len(insns)]
@@ -239,6 +253,56 @@ t, alive, how = session(setup(r5="0x50", r6="0xaabb")
 row("rb vecbase", printed(t, "r4") if alive else "died", "0x50",
     "VECBASE unchanged too -- the second lane of the declined halfword")
 
+# ---------------------------- per-arm channels (pass 2: sibling parity, arm by arm)
+#  A seat pointed out that only GENCTL had a readback: every other reachable arm's
+#  halfword-write row checked SURVIVAL alone, so a guard edited at ONE arm (`len > 2',
+#  or the guard deleted, at T2ICR only) left every row green.  Each arm now has its own
+#  channel, with a lane value its own mask turns into a different byte when it lands.
+for nm, off, pre, landed in (("t2ctl", T2CTL, "0x03", "0x3"), ("t2icr", T2ICR, "0x13", "0x13"),
+                             ("scctx", SCCTX, "0x1f", "0x1f")):
+    t, alive, how = session(setup(r5=pre, r6="0xaab8")
+                            + program([ST_B(5, off), ST_H(6, off), LD_BU(4, off)]) + ["print r4"])
+    row("rb " + nm, printed(t, "r4") if alive else "died", landed,
+        "%s unchanged after a declined st.h -- kills a guard edited at THIS arm" % nm.upper())
+    row("rb %s dcl" % nm, t.count("write to PCCTWO_%s " % ("TxCTL" if nm == "t2ctl" else "TxICR" if nm == "t2icr" else "SCCTX") + DECL), 1,
+        "...announced once at this arm")
+t, alive, how = session(setup(r6="0xaab8") + program([ST_H(6, SCCERR)]))
+row("hwr sccerr dcl", t.count("write to PCCTWO_SCCERR " + DECL), 1,
+    "halfword write to SCCERR declined once -- value-identical arm, message channel")
+
+#  PRE-TABLE BLOCK yield (section 1, guard field vs body field): the guard reads the access
+#  SHAPE (len) and the guarded body reads the VALUE (idata).  An operand swap to a value
+#  test -- `idata > 0xff', a plausible "does it fit a byte" reading -- accepts a halfword
+#  write whose value fits, and big-endian 0x0022 then stores 0x22, the NEIGHBOUR's lane,
+#  into GENCTL: the original defect, behind a guard that still reads like a width check.
+#  Every other wide-write row used a value above 0xff, so all 77 were green under it BY
+#  CONSTRUCTION.  Written before the repair table ran; the table says whether it kills.
+t, alive, how = session(setup(r5="0x11", r6="0x0022")
+                        + program([ST_B(5, GENCTL), ST_H(6, GENCTL), LD_BU(4, GENCTL)]) + ["print r4"])
+row("rb genctl lo", printed(t, "r4") if alive else "died", "0x11",
+    "st.h of a value that FITS a byte is still declined -- the guard is on len, not idata")
+
+# ------------------------- latch CARDINALITY (pass 2, the measuring seat's class closer)
+#  `latch same' and `latch two' pin ONE pair out of 66: every other session writes at most
+#  one BLOCK, so a bit shared by any other pair announces normally and no row moves.
+#  MEASURED by the builder: aliasing SCCTX onto SCCRX's bit -- a ONE-CHARACTER edit --
+#  left the 60-row detector at 60/60.  ONE OFFSET PER BLOCK: TxCTL serves T1CTL+T2CTL
+#  and TxICR serves T1ICR+T2ICR, so twelve LABELS would give only ten announces -- the
+#  same units slip that let "five even blocks + seven odd ones = twelve" read as all
+#  twelve blocks.  This row pins the CARDINALITY of the latch: any collision anywhere in
+#  the 12-bit space drops the count.  (Operator path for all twelve, so the odd ones are
+#  reachable; the guest-reachable halves have their own rows above.)
+BLOCKS12 = (("GENCTL", 0x02), ("VECBASE", 0x03), ("PSCALEADJ", 0x15), ("TxCTL", 0x16),
+            ("TxICR", 0x1a), ("SCCERR", 0x1c), ("SCCICR", 0x1d), ("SCCTX", 0x1e),
+            ("SCCRX", 0x1f), ("SCSIICR", 0x2f), ("IPL", 0x3e), ("MASK", 0x3f))
+#  VALUE 0x0003, not 0x0303: it fits a byte, so this row ALSO reds if any arm swaps its
+#  guard operand from len to a value test (see `rb genctl lo').  On the fix the value
+#  never lands, so the expectation is value-independent.
+t, alive, how = session(["put h 0x%x, 0x0003" % (PCC2 + o) for _, o in BLOCKS12])
+row("latch all", t.count(DECL), 12,
+    "one wide write per BLOCK -> TWELVE announces: bit CARDINALITY, not one pair")
+row("latch all lv", how, "exit0", "...and the host survived all twelve blocks")
+
 # ------------------------------------------------------------------ latch rows
 t, alive, how = session(setup(r6="0xaabb") + program([ST_H(6, GENCTL), ST_H(6, GENCTL)]))
 row("latch same", t.count("write to PCCTWO_GENCTL " + DECL), 1,
@@ -270,6 +334,53 @@ for nm, off in (("vecbase", VECBASE), ("pscale", PSCALEADJ), ("t1ctl", T1CTL),
     row("op " + nm, how, "exit0", "debugger put h at odd %s survives" % nm.upper())
     row("op %s dcl" % nm, t.count(DECL), 1, "...and was declined once")
 
+#  --------- the odd arms' FALL-THROUGH channel (pass 3, ruled a floor breach, not a disclosure)
+#  The block above proves each odd arm ANNOUNCES; it cannot see a guard that announces AND
+#  then lets the halfword land (the M_FALL shape -- decline nulled, guard kept: clause (d)).
+#  PRETABLE Section 2 had disclosed that as "a sentence owed".  The measuring seat asked
+#  whether a disclosure can discharge a floor clause; it cannot, or every breach becomes a
+#  sentence.  So each of the four arms gets the channel its body offers:
+#    SCCICR/SCCRX/SCSIICR store `idata & mask' then reassert_interrupts(): set 0x1f by
+#      byte (legal under both masks), decline a wide 0xaab8, read the byte back -- a landed
+#      write leaves 0x18 (& 0x1f) or 0x98 (& 0xdf) in an INTERRUPT CONTROL register.
+#    PSCALEADJ stores nothing; its write body only prints "ignored (value ...)".  A landed
+#      wide write therefore prints that line -- the message is the only channel, and the
+#      row counts it at ZERO.
+for nm, off in (("sccicr", SCCICR), ("sccrx", SCCRX), ("scsiicr", SCSIICR)):
+    t, alive, how = session(setup(r5="0x1f") + program([ST_B(5, off)])
+                            + ["put h 0x%x, 0xaab8" % (PCC2 + off)]
+                            + program([LD_BU(4, off)], at=CODE + 0x100) + ["print r4"])
+    row("rb " + nm, printed(t, "r4") if alive else "died", "0x1f",
+        "%s unchanged after a declined put h -- a fall-through lands 0x18/0x98 and reasserts" % nm.upper())
+t, alive, how = session(["put h 0x%x, 0x0303" % (PCC2 + PSCALEADJ)])
+row("op pscale noig", t.count("PSCALEADJ ignored"), 0,
+    "a declined wide write never reaches the 'ignored' print -- fall-through would")
+
+# --------------------------------- IPL (guest-reachable, EVEN) and MASK (operator, odd)
+#  IPL 0x3e: a halfword at 0x3e lands in the IPL arm.  Its write side is read-only (#119
+#  "ignored"), so a wide write is declined by the WIDTH latch first and a readback cannot
+#  tell the two refusals apart -- the channel is the message.
+t, alive, how = session(setup() + program([I_ST_SCR, LD_H(4, IPL), I_LD_SCR]) + ["print r4"])
+row("hrd ipl", how, "exit0", "ld.h IPL (EVEN, the SIXTH guest-reachable block) survives")
+row("hrd ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+t, alive, how = session(setup(r6="0x1234") + program([I_ST_SCR, ST_H(6, IPL), I_LD_SCR]) + ["print r4"])
+row("hwr ipl", how, "exit0", "st.h IPL survives")
+row("hwr ipl lv", printed(t, "r4") if alive else "died", "0x5a5a5a5a", "...and runs on")
+row("hwr ipl dcl", t.count("write to PCCTWO_IPL " + DECL), 1,
+    "...declined by the WIDTH latch (not the read-only one) -- the message is the channel")
+#  MASK 0x3f: odd, operator path.  It is GENCTL's twin, so it gets GENCTL's readback: set
+#  MASK to a known byte at the legal width, decline a wide write through the debugger,
+#  then read the byte back through a program at a SECOND address.  A deleted guard stores
+#  the wrong lane (0xbb); an accidental compose stores 0xaa.  reassert_interrupts on a
+#  MASK byte write is harmless here: GENCTL's C040 bit is clear and nothing is pending.
+t, alive, how = session(setup(r5="0x12") + program([ST_B(5, MASK)])
+                        + ["put h 0x%x, 0xaabb" % (PCC2 + MASK)]
+                        + program([LD_BU(4, MASK)], at=CODE + 0x100) + ["print r4"])
+row("op mask", how, "exit0", "debugger put h at odd MASK survives")
+row("op mask dcl", t.count("write to PCCTWO_MASK " + DECL), 1, "...and was declined once")
+row("rb mask", printed(t, "r4") if alive else "died", "0x12",
+    "MASK unchanged after the declined wide write -- GENCTL's twin gets GENCTL's readback")
+
 # ---------------------------------------------------------------------- summary
 print("NOROW  two device instances               -- mvme187 has ONE pcc2; per-instance latch state"
       " is by construction, not measured")

```

## THE GATE DIFF (`regress/gate_arm.sh`, INLINED IN FULL)

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index a8359d0..f5ee072 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1292,13 +1292,13 @@ if ! grep -q "PCC2W_PROBE_DONE" "$PCC2LOG"; then
     check "pcc2 width probe completed" "no" "yes"
 else
     check "pcc2 width probe completed" "yes" "yes"
-    for v in "live" "devsig" "byte rd" "byte rd liv" "hrd genctl" "hrd genctl lv" "hwr genctl" "hwr genctl lv" "hrd t2ctl" "hrd t2ctl lv" "hwr t2ctl" "hwr t2ctl lv" "hrd t2icr" "hrd t2icr lv" "hwr t2icr" "hwr t2icr lv" "hrd sccerr" "hrd sccerr lv" "hwr sccerr" "hwr sccerr lv" "hrd scctx" "hrd scctx lv" "hwr scctx" "hwr scctx lv" "wrd sccerr" "wrd sccerr lv" "wwr sccerr" "wwr sccerr lv" "wwr sccerr dcl" "val h genctl" "val w sccerr" "rb genctl" "rb genctl dcl" "rb vecbase" "latch same" "latch two" "acc genctl" "acc genctl nod" "acc t2ctl" "acc t2ctl nod" "acc t2icr" "acc t2icr nod" "acc scctx" "acc scctx nod" "acc sccerr" "acc sccerr nod" "op vecbase" "op vecbase dcl" "op pscale" "op pscale dcl" "op t1ctl" "op t1ctl dcl" "op t1icr" "op t1icr dcl" "op sccicr" "op sccicr dcl" "op sccrx" "op sccrx dcl" "op scsiicr" "op scsiicr dcl"; do
+    for v in "live" "devsig" "byte rd" "byte rd liv" "hrd genctl" "hrd genctl lv" "hwr genctl" "hwr genctl lv" "hrd t2ctl" "hrd t2ctl lv" "hwr t2ctl" "hwr t2ctl lv" "hrd t2icr" "hrd t2icr lv" "hwr t2icr" "hwr t2icr lv" "hrd sccerr" "hrd sccerr lv" "hwr sccerr" "hwr sccerr lv" "hrd scctx" "hrd scctx lv" "hwr scctx" "hwr scctx lv" "wrd sccerr" "wrd sccerr lv" "wwr sccerr" "wwr sccerr lv" "wwr sccerr dcl" "val h genctl" "val w sccerr" "rb genctl" "rb genctl dcl" "rb vecbase" "rb t2ctl" "rb t2ctl dcl" "rb t2icr" "rb t2icr dcl" "rb scctx" "rb scctx dcl" "hwr sccerr dcl" "rb genctl lo" "latch same" "latch two" "latch all" "latch all lv" "acc genctl" "acc genctl nod" "acc t2ctl" "acc t2ctl nod" "acc t2icr" "acc t2icr nod" "acc scctx" "acc scctx nod" "acc sccerr" "acc sccerr nod" "op vecbase" "op vecbase dcl" "op pscale" "op pscale dcl" "op t1ctl" "op t1ctl dcl" "op t1icr" "op t1icr dcl" "op sccicr" "op sccicr dcl" "op sccrx" "op sccrx dcl" "op scsiicr" "op scsiicr dcl" "rb sccicr" "rb sccrx" "rb scsiicr" "op pscale noig" "hrd ipl" "hrd ipl lv" "hwr ipl" "hwr ipl lv" "hwr ipl dcl" "op mask" "op mask dcl" "rb mask"; do
         check "pcc2 width row: $v" "$(count "$PCC2LOG" "^$v  .*ok$")" "1"
     done
 
     #  DENOMINATOR, SUMMED -- a lost row and a failing row need different responses.
-    check "pcc2 width rows emitted"           "$(( $(count "$PCC2LOG" " ok$") + $(count "$PCC2LOG" " FAIL$") ))" "60"
-    check "pcc2 width rows green" "$(count "$PCC2LOG" " ok$")"   "60"
+    check "pcc2 width rows emitted"           "$(( $(count "$PCC2LOG" " ok$") + $(count "$PCC2LOG" " FAIL$") ))" "82"
+    check "pcc2 width rows green" "$(count "$PCC2LOG" " ok$")"   "82"
     check "pcc2 width rows red"   "$(count "$PCC2LOG" " FAIL$")" "0"
 fi
 

```

## THE PRODUCT DIFF (`src/devices/dev_pcc2.c`: comments + a compile-time bound, INLINED IN FULL)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index e795fe9..b439b12 100644
--- a/src/devices/dev_pcc2.c
+++ b/src/devices/dev_pcc2.c
@@ -64,8 +64,9 @@
 
 // #define	debug fatal
 
-/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) ended the host
-    on a guest-chosen access width -- an ordinary aligned halfword load of a documented
+/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) -- TEN of them
+    `fatal(); exit(1)' kills that ended the host on a guest-chosen access width, and
+    two (IPL, MASK) #119 warn-once latches that declined it process-globally -- an ordinary aligned halfword load of a documented
     register.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).
 
     THE TREE ALREADY KNEW THE WIDTH IS LEGAL: mvme_pcctworeg.h says the PCCchip2
@@ -80,22 +81,29 @@
               byte" ONLY at len == 1: memory_readmax64 composes big-endian, so
               (uint8_t) idata is the HIGHEST-address lane.  Deleting the guard would
               store the neighbour's byte -- st.h 0xAABB to GENCTL would set GENCTL to
-              0xBB, VECBASE's lane.  And seven arms mask, read-modify-write or clear
-              on write, six of them calling reassert_interrupts().  Now: DECLINE +
+              0xBB, VECBASE's lane.  And eight arms mask, read-modify-write or clear
+              on write, and seven of the twelve blocks call reassert_interrupts()
+              (five of those eight; a seat measured the earlier "six" wrong).  Now: DECLINE +
               latched announce.  Per-lane composition through each arm (COMPOSE) is
               the faithful upgrade and is FILED as pcc2widecompose; not taken here
-              because the hardware's lane semantics are not on disk and no measured
-              driver wide-writes these registers.
+              because the hardware's lane semantics are not on disk and no driver
+              MEASUREMENT exists either way: the only consumer is mvme187, no mvme187
+              boot runs in this harness, and the one OS source in the tree (OpenBSD
+              2.2) declares these registers `volatile u_char' and byte-accesses them
+              -- a reading, not a measurement.
 
     ONE BIT PER BLOCK, twelve, per instance: a driver bringing up the chip touches
     several of these in one pass, and one latch would announce the first and silence
     the rest (#497's own reasoning).  Auto-incremented rather than `1 << N' literals,
-    which this fork records as collision-prone; PCC2_W_NBITS bounds it.
+    which this fork records as collision-prone; PCC2_W_NBITS names the count, and the
+    typedef after the enum makes the build fail if it ever exceeds the 32-bit field.
 
     REACHABILITY, verified: every non-byte m88k access is alignment-checked BEFORE
-    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the five
-    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX) are GUEST-reachable; the
-    seven odd ones are OPERATOR-reachable -- the debugger's `put h' warns on a
+    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the SIX
+    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX, IPL) are GUEST-reachable
+    (this said "five" until pass 2; IPL at 0x3e is even, and a seat counted); the
+    six odd ones -- VECBASE, PSCALEADJ, the T1 labels, SCCICR, SCCRX, SCSIICR, MASK
+    -- are OPERATOR-reachable -- the debugger's `put h' warns on a
     misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
     operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
     converted; the detector reaches the odd ones through that path.
@@ -118,6 +126,9 @@ enum {
 	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
 	PCC2_W_NBITS
 };
+/*  A seat pointed out that NBITS "bounded" nothing.  Now it does: negative array
+    size is a compile-time error, C99, no assert.h.  */
+typedef char pcc2_w_fits_in_warned[PCC2_W_NBITS <= 32 ? 1 : -1];
 
 struct pcc2_data {
 	struct interrupt	cpu_irq;

```

## PRETABLE.out (the pre-table block, written BEFORE table 2 part 1; Section 5 before part 2)

```
PRE-TABLE BLOCK -- pcc2widthkills pass-2 REPAIR table (killtable2_20260903), pcc2_width_probe.py
================================================================================

*** SECTION 0 -- THE HONEST PART: THIS ROUND'S TABLE 1 (killtable_20260903, 8 mutants, 60
*** rows) RAN WITH NO PRE-TABLE BLOCK.  The pass-2 measuring seat named the omission and
*** measured what the skipped SIBLING-PARITY check would have shown: GENCTL and MASK have
*** byte-identical write bodies, GENCTL carried five row mentions and MASK zero, and the
*** MASK null-repair was a 60/60 sweep.  The class -- aliasing a latch constant, one token,
*** clause (d) -- sat in sgideprimop's own PRETABLE.out 33 hours earlier, and this round
*** transferred that file's d->warned design without the check that qualified it.
--------------------------------------------------------------------------------
This block is written BEFORE table 2 runs; its mtime against the table-2 .out files
beside it proves the order for table 2 only.  Table 1 is recorded as HAVING HAD NO
PRE-TABLE BLOCK, not as having passed one.  (Third recorded skip of the mandate.)

SECTION 1 -- GUARD FIELD vs BODY FIELD
--------------------------------------------------------------------------------
GUARD reads (each of 12 blocks):  len, writeflag
DECLINE body reads:               d->warned (bit test), len (printed)     writes: d->warned |= bit
FALL-THROUGH body reads:          idata, relative_addr, d->pcctwo_reg[], pending_timer*_interrupts

Where they differ: the guard reads the ACCESS SHAPE, the body reads the VALUE.
Disagreeing states: (len==1, any idata)      -> acc rows: byte writes land
                    (len==2, idata > 0xff)   -> every hwr/rb/wwr/latch row
                    (len==2, idata <= 0xff)  -> NO ROW EXISTED.  All 77 wide-write rows used
                    values above 0xff, so a guard operand swap `len != 1' -> `idata > 0xff'
                    (a plausible "fits a byte" reading) was green by construction while a
                    big-endian st.h 0x0022 stored 0x22 -- the neighbour's lane -- into GENCTL.
  ==> ADDED before the table: `rb genctl lo' (st.b 0x11; st.h 0x0022; expect 0x11) and the
      `latch all' value changed 0x0303 -> 0x0003 so the cardinality row reds under the same
      swap at ANY arm.  Mutant M_IDATA_GENCTL built to measure it.  This is the block's own
      yield, found by asking the field question rather than the mutant question.

THE SHARED-BITFIELD QUESTION (who else writes d->warned, can they set my bit?):
    occurrences of 'warned |=' in dev_pcc2.c: 1      lines mentioning 'warned': 7
  One writer, pcc2_width_decline(), sets exactly the bit its caller names; nothing in
  DEVICE_ACCESS or a tick writes the field, so benign traffic cannot pre-set a bit.  What
  CAN collide is the ENUM: two callers naming one member.  That is the M_ALIAS_SCCTX shape,
  and `latch all' (12 announces, one per block) is the row that sees it -- `latch same' and
  `latch two' pin one pair of 66 and do not.

SECTION 2 -- SIBLING PARITY, ARM BY ARM (after the repair; every block owes a survival row,
a decline-announce row, and a readback where decline != accept)
--------------------------------------------------------------------------------
  block      even?  survival            announce                  readback (decline != accept?)
  GENCTL     even   hwr genctl(+lv)     rb genctl dcl             rb genctl, val h genctl, rb genctl lo, acc genctl
  VECBASE    odd    op vecbase          op vecbase dcl            rb vecbase
  PSCALEADJ  odd    op pscale           op pscale dcl             plain store, no mask: dcl is the channel
  TxCTL      even   hwr t2ctl(+lv)      rb t2ctl dcl              rb t2ctl (& 3), acc t2ctl, op t1ctl(+dcl)
  TxICR      even   hwr t2icr(+lv)      rb t2icr dcl              rb t2icr (& 0x17), acc t2icr, op t1icr(+dcl)
  SCCERR     even   hrd/hwr/wrd/wwr     hwr sccerr dcl, wwr dcl   VALUE-IDENTICAL (always 0): message only, disclosed
  SCCICR     odd    op sccicr           op sccicr dcl             dcl is the channel
  SCCTX      even   hwr scctx(+lv)      rb scctx dcl              rb scctx (& 0x1f), acc scctx
  SCCRX      odd    op sccrx            op sccrx dcl              dcl is the channel
  SCSIICR    odd    op scsiicr          op scsiicr dcl            dcl is the channel
  IPL        even   hrd/hwr ipl(+lv)    hwr ipl dcl               read-side IPL==0 diagnostic (width-independent)
  MASK       odd    op mask             op mask dcl               rb mask (GENCTL's twin: plain store + reassert)
  latch all  (all twelve, one offset per BLOCK -> 12 announces)
Asymmetry left, DISCLOSED: PSCALEADJ/SCCICR/SCCRX/SCSIICR have no readback row.  Their `dcl'
rows red under any guard edit that lets the halfword land silently (len > 2, delete, operand
swap) -- every shape in this table.  A guard edit that lands the write AND still announces
(the M_FALL_MASK shape) at one of those four would escape; that is the sentence owed, and
MASK's own fall-through is the measured instance of the shape.

SECTION 3 -- CLAIM -> ROW (added comment sentences asserting an observable)
--------------------------------------------------------------------------------
  "kills a guard edited at THIS arm"            -> rb t2ctl / rb t2icr / rb scctx   (M_LENGT2_TXCTL/TXICR/SCCTX)
  "TWELVE announces: bit CARDINALITY"           -> latch all                          (M_ALIAS_SCCTX)
  "0x3e is EVEN -- GUEST-reachable, survives"   -> hwr ipl, hwr ipl lv                (M_KILL_IPL)
  "value-identical arm, message channel"        -> hwr sccerr dcl                     (M_LENGT2_SCCERR)
  "guard is on len, not idata"                  -> rb genctl lo                       (M_IDATA_GENCTL)
  "six guest-reachable" (contract + comment)    -> hwr ipl                            (census row, not a kill)
  "seven of the twelve blocks call reassert"    -> DERIVED by awk over the arms; no row (not an observable of the fix)

SECTION 4 -- CHANNEL: mutant -> row -> observable that differs.  PREDICTIONS, written
before any table-2 cell landed.
--------------------------------------------------------------------------------
  M_DELETE_MASK    rb mask 0xbb (was 0x0), op mask dcl 0            MASK guard deleted: halfword lands the neighbour lane
  M_KILL_IPL       hwr ipl exit1, hwr ipl lv died                  verbatim kill at a GUEST-reachable arm
  M_KILL_MASK      op mask exit1                                    kill at the operator-reachable twin
  M_DELETE (ctl)   rb genctl 0xbb, rb genctl dcl 0                  the table-1 control still reds
  M_DELETE_TXICR   rb t2icr 0x10, rb t2icr dcl 0                    0xaab8 & 0x17 lands
  M_LENGT2_TXICR   same                                             per-arm `len > 2'
  M_LENGT2_TXCTL   rb t2ctl 0x0, rb t2ctl dcl 0                     0xaab8 & 3 lands
  M_LENGT2_SCCTX   rb scctx 0x18, rb scctx dcl 0                    0xaab8 & 0x1f lands
  M_LENGT2_SCCERR  hwr sccerr dcl 0                                 value-identical: the announce is the only channel
  M_ALIAS_SCCTX    latch all 11 (SCCTX announces on SCCRX's bit)    a collision drops the count; nothing else moves
  M_LENGT2_MASK    rb mask 0xbb, op mask dcl 0                      halfword lands at MASK
  M_FALL_MASK      rb mask 0xbb (op mask dcl stays 1)               announce-then-land: readback is the only channel
  M_IDATA_GENCTL   rb genctl lo 0x22, latch all 11                  operand swap to a value test: a small halfword lands
  BASE             78/78                                            the repair perturbed nothing
Every row above names a mutant under which its channel VARIES; no row is survival-only at a
refusal-effect site.  Rows whose channel cannot vary under any enumerated mutant: none added.


SECTION 5 -- AMENDMENT, written after table-2 PART 1 (9 mutants + BASE, all killed) and
BEFORE PART 2.  Section 2's "sentence owed" was RULED A FLOOR BREACH, not a disclosure.
--------------------------------------------------------------------------------
The measuring seat, running its own pass 3 against the 78-row detector, asked whether the
disclosed asymmetry (PSCALEADJ/SCCICR/SCCRX/SCSIICR: no readback, so a guard that ANNOUNCES
and then lets the halfword land is invisible) can be discharged by clause (e).  Ruling: NO.
Clause (d) is a FLOOR -- "the guard kept, its effect removed" -- and the fall-through shape at
those arms is exactly that.  Clause (e) governs claims ABOVE the floor; a disclosure cannot
place a detector below it, or every floor breach becomes dischargeable by a sentence.  The
CHANNEL rule in Section 4 already said as much: a `dcl' row cannot vary under a mutant that
keeps announcing, so at those four arms it was the WRONG channel for this shape.

Rows added (part 2 measures them):
  rb sccicr / rb sccrx / rb scsiicr   set 0x1f by byte, decline put h 0xaab8, read back 0x1f
                                      M_FALL_* lands 0x18 (& 0x1f) / 0x98 (& 0xdf) and REASSERTS
  op pscale noig                      PSCALEADJ's body stores nothing and only prints; count of
                                      "PSCALEADJ ignored" in the wide-write session == 0.
                                      M_FALL_PSCALEADJ prints it once.
Blast radius is NOT uniform across the four (the seat's point): three of them put the
neighbour's lane into an INTERRUPT CONTROL register and reassert; one prints.  One sentence
had covered all four, which was too coarse as well as below the floor.

```

## DISCLOSURE -- `git diff --numstat` for the round's files

```
93	0	CHANGELOG.md
50	0	OUTSTANDING_BUGS.md
3	3	regress/gate_arm.sh
112	1	regress/pcc2_width_probe.py
20	6	regress/sgi_de_primop_probe.py
21	10	src/devices/dev_pcc2.c
248	5	tools/pipeline/ledger.json
3	3	tools/pipeline/matrix.html

```
    regress/pcc2_width_probe.py   INLINED
    regress/gate_arm.sh           INLINED
    src/devices/dev_pcc2.c        INLINED
    regress/sgi_de_primop_probe.py  NOT SHOWN -- a different round (#500 pass 16, comment-only)
    OUTSTANDING_BUGS.md           NOT SHOWN -- filings (pcc2widecompose, sgideprimopstrengthen)
    tools/pipeline/ledger.json    NOT SHOWN -- seat records
    tools/pipeline/matrix.html    NOT SHOWN -- generated


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
