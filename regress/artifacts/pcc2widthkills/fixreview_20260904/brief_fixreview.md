# pcc2widthkills -- FIX REVIEW AND ADJUDICATION (owner directive 2026-09-04: "review any previous fixes and adjudicate").  Two seats: the codex seat on its new model at xhigh, and the Fable 5 seat.  You are asked to review the PRODUCT FIX first, then every repair made since, then to produce an ORDERED disposition of the filed queue.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Eleven review passes have run on this round's detector and none on its FIX alone since the commit that
shipped it.  A reading seat can be wrong about a fix that passes every table -- the tables measure the
detector.  Review the fix as if the tables did not exist, THEN use them.  Where you can settle a
premise from the tree, do; where you cannot, say so in one line.  **VERDICT LINE FIRST.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/`, UNCOMMITTED on top of
`b78bb0f`.**  Three pristine-2021 copies under the project root are NOT this fork.  If your line
numbers disagree with mine by hundreds you are reading one of them -- say so.

## WHAT WAS FIXED (the product change, committed in b78bb0f)

`dev_pcc2.c` (m88k mvme187 PCC2 chip) had TWELVE register blocks whose handler ended the host with
`exit(1)` when a guest issued a 2-, 4- or 8-byte access -- `#119` had already fixed two of them in the
same file with a warn-once + continue.  The fix is a DIRECTION SPLIT at every block: wide READS are
accepted (the top-of-function memcpy has already served them from the register array, which is what
the pristine model did before the kill), wide WRITES are DECLINED -- a per-instance latched announce
(`pcc2_width_decline`, one bit per block in `d->warned`, `(once)` in the text) and `break`, so the
write does not land in a register whose byte-lane composition the model does not define.  Six of the
twelve blocks sit at even offsets and are guest-reachable at len 2; the other six are operator-only
for wide writes (the m88k alignment check).  The detector that ships with it (`regress/pcc2_width_probe.py`,
now 242 rows, gate 14 pins the count) was built and rebuilt across eleven passes, each finding a cell
of state no row held; the fix itself has not changed since the commit except for comments and a
compile-time typedef.

## QUESTIONS

1. **IS THE FIX RIGHT?**  For each of the twelve blocks: is DECLINE the right disposition for a wide
   WRITE, or should any block ACCEPT (the model already computes the right value), FAULT (return 0, the
   bus-error disposition `dev_unreadable.c` embodies), or compose per lane (`pcc2widecompose`, filed)?
   Is ACCEPT right for every wide READ -- is there a block whose read has a side effect the memcpy
   skips (SCCRXIACK's body runs on reads; the IACK path)?  Is the latch per-instance and per-block as
   claimed, and is one announce per block per instance the right granularity?  Does the `break` skip
   any common tail the arm relied on (the sketch rule: read the enclosing function's exits)?  What
   does a REAL guest (OpenBSD/mvme88k, whose headers are in the tree) do that this fix would now
   silently refuse?
2. **IS ANY PREVIOUS REPAIR IN THE CHAIN WRONG?**  Passes 5-11 repaired the DETECTOR and the RECORD --
   the free-running rows and their masks, the cval() labels, the generating sets for the idata bits at
   pending cells, the enumeration across the arms, and four carrier amendments (clause (d) joint cells,
   its bound, two corrections).  Name any repair that made something worse, any row that is vacuous as
   built, any sentence a measurement refutes.  Each pass's CHANGELOG title is listed below and the
   newest block is inlined in full.
3. **ADJUDICATE THE FILED QUEUE.**  Nine pcc2 items were filed by this chain and none has a round yet
   (inlined below).  Give an ORDERED list: which to fix next and why, which to fold into another, which
   to file-and-leave, which to drop -- with the measurable consequence each one names, and the cheapest
   witness you can think of for each.  `pcc2c040kill` is the only HIGH; say whether you agree it is.
4. **THE ONE RULE SPLIT STILL OPEN.**  The floor of clause (d) at a joint cell: Fable's bound (the
   device-STATE lvalues the fix's data flow makes jointly reachable; idata bits are marginals) versus
   the Opus seat's (DECISIVE axes -- if-tested or index -- x a covering array of STRENGTH t, disclosed
   by strength).  Both are in the rule text below.  Which would you adopt as the floor, in one sentence,
   and what would it have demanded at TxCTL and TxICR that the tree does not now hold?
5. **THE CLOSING QUESTION.**  With part 12 measured (its predictions are in `PRETABLE_pass11b.out`),
   should the chain CLOSE at pass 12 and commit?  A closing zero must be VALID: the diff delivered, the
   roster complete or its misses named, the zero carried with its denominator.

**The Fable seat adjudicates: it produces the disposition list; the codex seat's list is one input to
it.  Where the two seats disagree, say so in their own words and settle by what can be checked.**

## THE COMMITTED FIX (`git show --format= b78bb0f -- src/devices/dev_pcc2.c`, VERBATIM)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index c4e850e..e795fe9 100644
--- a/src/devices/dev_pcc2.c
+++ b/src/devices/dev_pcc2.c
@@ -64,11 +64,70 @@
 
 // #define	debug fatal
 
+/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) ended the host
+    on a guest-chosen access width -- an ordinary aligned halfword load of a documented
+    register.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).
+
+    THE TREE ALREADY KNEW THE WIDTH IS LEGAL: mvme_pcctworeg.h says the PCCchip2
+    registers "can be accessed as bytes (8 bits), two-bytes (16 bits), or four-bytes
+    (32 bits)".  So this is not a fault to model; it is an access the model declines
+    to IMPLEMENT on one side and already implements on the other:
+
+      READS   are served BEFORE the switch by memcpy(data, pcctwo_reg + addr, len),
+              raw bytes in address order -- width-correct by construction.  The old
+              guard discarded a correct answer.  Now: ACCEPT (fall through).
+      WRITES  every arm uses `idata', the composed value, which is "the addressed
+              byte" ONLY at len == 1: memory_readmax64 composes big-endian, so
+              (uint8_t) idata is the HIGHEST-address lane.  Deleting the guard would
+              store the neighbour's byte -- st.h 0xAABB to GENCTL would set GENCTL to
+              0xBB, VECBASE's lane.  And seven arms mask, read-modify-write or clear
+              on write, six of them calling reassert_interrupts().  Now: DECLINE +
+              latched announce.  Per-lane composition through each arm (COMPOSE) is
+              the faithful upgrade and is FILED as pcc2widecompose; not taken here
+              because the hardware's lane semantics are not on disk and no measured
+              driver wide-writes these registers.
+
+    ONE BIT PER BLOCK, twelve, per instance: a driver bringing up the chip touches
+    several of these in one pass, and one latch would announce the first and silence
+    the rest (#497's own reasoning).  Auto-incremented rather than `1 << N' literals,
+    which this fork records as collision-prone; PCC2_W_NBITS bounds it.
+
+    REACHABILITY, verified: every non-byte m88k access is alignment-checked BEFORE
+    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the five
+    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX) are GUEST-reachable; the
+    seven odd ones are OPERATOR-reachable -- the debugger's `put h' warns on a
+    misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
+    operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
+    converted; the detector reaches the odd ones through that path.
+
+    NOT FIXED HERE, cited so "twelve kills removed" is not read as "file clean":
+    pcc2c040kill (a LEGAL byte write of 0x04 to GENCTL still ends the host in
+    reassert_interrupts) and pcc2defaultkill (an unlisted offset still ends it).  */
+enum {
+	PCC2_W_GENCTL_LEN,
+	PCC2_W_VECBASE_LEN,
+	PCC2_W_PSCALEADJ_LEN,
+	PCC2_W_TXCTL_LEN,	/*  one block serves T1CTL and T2CTL  */
+	PCC2_W_TXICR_LEN,	/*  one block serves T1ICR and T2ICR  */
+	PCC2_W_SCCERR_LEN,
+	PCC2_W_SCCICR_LEN,
+	PCC2_W_SCCTX_LEN,
+	PCC2_W_SCCRX_LEN,
+	PCC2_W_SCSIICR_LEN,
+	PCC2_W_IPL_LEN,		/*  was a #119 function-static: process-global  */
+	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
+	PCC2_W_NBITS
+};
+
 struct pcc2_data {
 	struct interrupt	cpu_irq;
 
 	uint8_t			pcctwo_reg[PCC2_SIZE];
 
+	/*  pcc2widthkills: one bit per width-guard block, see the enum.  Zeroed by
+	    the init memset, so every instance starts with every announce armed.  */
+	uint32_t		warned;
+
 	uint8_t			cur_int_vec[8];
 
 	/*  Timers:  */
@@ -319,6 +378,18 @@ DEVICE_TICK(pcc2)
 }
 
 
+/*  pcc2widthkills: decline a wide WRITE to a byte register, announcing once per
+    block per instance.  The caller `break's after this; the read side of the same
+    block never reaches here.  */
+static void pcc2_width_decline(struct pcc2_data *d, int bit, const char *name, int len)
+{
+	if (!(d->warned & (1u << bit))) {
+		d->warned |= (1u << bit);
+		fatal("[ pcc2: unimplemented len=%i write to %s -- declined."
+		    "  (once) ]\n", len, name);
+	}
+}
+
 DEVICE_ACCESS(pcc2)
 {
 	uint64_t idata = 0;
@@ -356,10 +427,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_GENCTL:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_GENCTL\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata;
@@ -368,10 +438,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_VECBASE:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_VECBASE\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata & 0xf0;
@@ -391,10 +460,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_PSCALEADJ:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_PSCALEADJ\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			fatal("[ pcc2: write to PSCALEADJ ignored (value "
@@ -404,10 +472,9 @@ DEVICE_ACCESS(pcc2)
 
 	case PCCTWO_T2CTL:
 	case PCCTWO_T1CTL:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_TxCTL\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			/*  PCC2_TCTL_CEN and PCC2_TCTL_COC:  */
@@ -426,10 +493,9 @@ DEVICE_ACCESS(pcc2)
 
 	case PCCTWO_T2ICR:
 	case PCCTWO_T1ICR:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_TxICR\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] &= ~0x17;
@@ -464,20 +530,18 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_SCCERR:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_SCCERR\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_SCCERR_LEN, "PCCTWO_SCCERR", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE)
 			d->pcctwo_reg[relative_addr] = 0;	/*  clear  */
 		break;
 
 	case PCCTWO_SCCICR:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_SCCICR\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata & 0x1f;
@@ -489,10 +553,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_SCCTX:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_SCCTX\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata & 0x1f;
@@ -504,10 +567,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_SCCRX:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_SCCRX\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata & 0xdf;
@@ -525,10 +587,9 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_SCSIICR:
-		if (len != 1) {
-			fatal("TODO: pcc2: non-byte reads and writes of "
-			    "PCCTWO_SCSIICR\n");
-			exit(1);
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);
+			break;
 		}
 		if (writeflag == MEM_WRITE) {
 			d->pcctwo_reg[relative_addr] = idata & 0xdf;
@@ -540,10 +601,11 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_IPL:
-		if (len != 1) {
-			static int w = 0;	/* #119: was exit(1) -> warn-once + continue */
-			if (!w) { fatal("[ pcc2: non-byte access to PCCTWO_IPL; "
-			    "ignored ]\n"); w = 1; }
+		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
+		    said "ignored" about a READ the memcpy above had already served.
+		    Now per-instance, write-only, like the ten blocks above.  */
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
 			break;
 		}
 		if (writeflag == MEM_WRITE) {
@@ -560,10 +622,11 @@ DEVICE_ACCESS(pcc2)
 		break;
 
 	case PCCTWO_MASK:
-		if (len != 1) {
-			static int w = 0;	/* #119: was exit(1) -> warn-once + continue */
-			if (!w) { fatal("[ pcc2: non-byte access to PCCTWO_MASK; "
-			    "ignored ]\n"); w = 1; }
+		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
+		    said "ignored" about a READ the memcpy above had already served.
+		    Now per-instance, write-only, like the ten blocks above.  */
+		if (len != 1 && writeflag == MEM_WRITE) {
+			pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);
 			break;
 		}
 		if (writeflag == MEM_WRITE) {

```

## THE WORKING-TREE CHANGE TO THE SAME FILE SINCE THE COMMIT (comments and a compile-time typedef; VERBATIM)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index e795fe9..4a975f5 100644
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
@@ -80,22 +81,30 @@
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
+    eight odd OFFSETS -- the six odd-only blocks VECBASE, PSCALEADJ, SCCICR, SCCRX,
+    SCSIICR, MASK, plus the T1CTL/T1ICR labels of the shared TxCTL/TxICR blocks --
+    are OPERATOR-reachable -- the debugger's `put h' warns on a
     misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
     operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
     converted; the detector reaches the odd ones through that path.
@@ -135,6 +144,12 @@ struct pcc2_data {
 	int			pending_timer1_interrupts;
 	int			pending_timer2_interrupts;
 };
+/*  pcc2widthkills: the enum must fit the field.  A seat pointed out that a bare
+    `<= 32' tested a literal, not the field, so narrowing `warned' would compile
+    silently; this is dev_dreamcast_gdrom.c's own form.  Negative array size is a
+    compile-time error, C99, no assert.h.  */
+typedef char pcc2_w_fits_in_warned[(PCC2_W_NBITS <= 8 * sizeof(((struct pcc2_data *)0)->warned)
+    && PCC2_W_NBITS <= 8 * sizeof(1u)) ? 1 : -1];
 
 
 static uint32_t read32(unsigned char *p)
@@ -603,7 +618,9 @@ DEVICE_ACCESS(pcc2)
 	case PCCTWO_IPL:
 		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
 		    said "ignored" about a READ the memcpy above had already served.
-		    Now per-instance, write-only, like the ten blocks above.  */
+		    Now per-instance, write-only, like the ten blocks above -- that is
+		    the WIDTH latch; the body's own #119 `static int w' below stays
+		    process-global (pcc2pscaleflood's family; not this round's).  */
 		if (len != 1 && writeflag == MEM_WRITE) {
 			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
 			break;
@@ -624,7 +641,10 @@ DEVICE_ACCESS(pcc2)
 	case PCCTWO_MASK:
 		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
 		    said "ignored" about a READ the memcpy above had already served.
-		    Now per-instance, write-only, like the ten blocks above.  */
+		    Now per-instance, write-only, like the ten blocks above -- that is
+		    the WIDTH latch.  (pcc2widthkills pass 7: this comment once claimed a
+		    #119 static of MASK's own "below" -- there is none; the body stores
+		    the byte and reasserts.  The static belongs to IPL's arm above.)  */
 		if (len != 1 && writeflag == MEM_WRITE) {
 			pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);
 			break;

```

## THE HANDLER AS IT NOW STANDS (the helper and the whole DEVICE_ACCESS, VERBATIM)

```c
static void pcc2_width_decline(struct pcc2_data *d, int bit, const char *name, int len)
{
	if (!(d->warned & (1u << bit))) {
		d->warned |= (1u << bit);
		fatal("[ pcc2: unimplemented len=%i write to %s -- declined."
		    "  (once) ]\n", len, name);
	}
}

DEVICE_ACCESS(pcc2) -- TEN of them
    `fatal(); exit(1)' kills that ended the host on a guest-chosen access width, and
    two (IPL, MASK) #119 warn-once latches that declined it process-globally -- an ordinary aligned halfword load of a documented
    register.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).

    THE TREE ALREADY KNEW THE WIDTH IS LEGAL: mvme_pcctworeg.h says the PCCchip2
    registers "can be accessed as bytes (8 bits), two-bytes (16 bits), or four-bytes
    (32 bits)".  So this is not a fault to model; it is an access the model declines
    to IMPLEMENT on one side and already implements on the other:

      READS   are served BEFORE the switch by memcpy(data, pcctwo_reg + addr, len),
              raw bytes in address order -- width-correct by construction.  The old
              guard discarded a correct answer.  Now: ACCEPT (fall through).
      WRITES  every arm uses `idata', the composed value, which is "the addressed
              byte" ONLY at len == 1: memory_readmax64 composes big-endian, so
              (uint8_t) idata is the HIGHEST-address lane.  Deleting the guard would
              store the neighbour's byte -- st.h 0xAABB to GENCTL would set GENCTL to
              0xBB, VECBASE's lane.  And eight arms mask, read-modify-write or clear
              on write, and seven of the twelve blocks call reassert_interrupts()
              (five of those eight; a seat measured the earlier "six" wrong).  Now: DECLINE +
              latched announce.  Per-lane composition through each arm (COMPOSE) is
              the faithful upgrade and is FILED as pcc2widecompose; not taken here
              because the hardware's lane semantics are not on disk and no driver
              MEASUREMENT exists either way: the only consumer is mvme187, no mvme187
              boot runs in this harness, and the one OS source in the tree (OpenBSD
              2.2) declares these registers `volatile u_char' and byte-accesses them
              -- a reading, not a measurement.

    ONE BIT PER BLOCK, twelve, per instance: a driver bringing up the chip touches
    several of these in one pass, and one latch would announce the first and silence
    the rest (#497's own reasoning).  Auto-incremented rather than `1 << N' literals,
    which this fork records as collision-prone; PCC2_W_NBITS names the count, and the
    typedef after the enum makes the build fail if it ever exceeds the 32-bit field.

    REACHABILITY, verified: every non-byte m88k access is alignment-checked BEFORE
    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the SIX
    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX, IPL) are GUEST-reachable
    (this said "five" until pass 2; IPL at 0x3e is even, and a seat counted); the
    eight odd OFFSETS -- the six odd-only blocks VECBASE, PSCALEADJ, SCCICR, SCCRX,
    SCSIICR, MASK, plus the T1CTL/T1ICR labels of the shared TxCTL/TxICR blocks --
    are OPERATOR-reachable -- the debugger's `put h' warns on a
    misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
    operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
    converted; the detector reaches the odd ones through that path.

    NOT FIXED HERE, cited so "twelve kills removed" is not read as "file clean":
    pcc2c040kill (a LEGAL byte write of 0x04 to GENCTL still ends the host in
    reassert_interrupts) and pcc2defaultkill (an unlisted offset still ends it).  */
enum {
	PCC2_W_GENCTL_LEN,
	PCC2_W_VECBASE_LEN,
	PCC2_W_PSCALEADJ_LEN,
	PCC2_W_TXCTL_LEN,	/*  one block serves T1CTL and T2CTL  */
	PCC2_W_TXICR_LEN,	/*  one block serves T1ICR and T2ICR  */
	PCC2_W_SCCERR_LEN,
	PCC2_W_SCCICR_LEN,
	PCC2_W_SCCTX_LEN,
	PCC2_W_SCCRX_LEN,
	PCC2_W_SCSIICR_LEN,
	PCC2_W_IPL_LEN,		/*  was a #119 function-static: process-global  */
	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
	PCC2_W_NBITS
};

struct pcc2_data {
	struct interrupt	cpu_irq;

	uint8_t			pcctwo_reg[PCC2_SIZE];

	/*  pcc2widthkills: one bit per width-guard block, see the enum.  Zeroed by
	    the init memset, so every instance starts with every announce armed.  */
	uint32_t		warned;

	uint8_t			cur_int_vec[8];

	/*  Timers:  */
	struct timer		*timer;
	int			pending_timer1_interrupts;
	int			pending_timer2_interrupts;
};
/*  pcc2widthkills: the enum must fit the field.  A seat pointed out that a bare
    `<= 32' tested a literal, not the field, so narrowing `warned' would compile
    silently; this is dev_dreamcast_gdrom.c's own form.  Negative array size is a
    compile-time error, C99, no assert.h.  */
typedef char pcc2_w_fits_in_warned[(PCC2_W_NBITS <= 8 * sizeof(((struct pcc2_data *)0)->warned)
    && PCC2_W_NBITS <= 8 * sizeof(1u)) ? 1 : -1];


static uint32_t read32(unsigned char *p)
{
	uint32_t x = 0;
	size_t i;

	for (i=0; i<sizeof(x); i++) {
		x <<= 8;
		x |= p[i];
	}

	return x;
}


static void write32(unsigned char *p, uint32_t x)
{
	size_t i;

	for (i=0; i<sizeof(x); i++) {
		p[sizeof(x) - 1 - i] = x;
		x >>= 8;
	}
}


static void pcc_timer_tick(struct timer *t, void *extra)
{
	struct pcc2_data *d = (struct pcc2_data *) extra;

	/*  The PCC2 timers run at 1 MHz.  */
	int steps = (int) (1000000.0 / PCC_TIMER_TICK_HZ);

	uint32_t count1, count2, compare1, compare2;
	int interrupt1 = 0, interrupt2 = 0;

	/*  Read values:  */
	count1 = read32(&d->pcctwo_reg[PCCTWO_T1COUNT]);
	count2 = read32(&d->pcctwo_reg[PCCTWO_T2COUNT]);
	compare1 = read32(&d->pcctwo_reg[PCCTWO_T1CMP]);
	compare2 = read32(&d->pcctwo_reg[PCCTWO_T2CMP]);

	/*  Timer enabled? Then count...  */
	if (d->pcctwo_reg[PCCTWO_T1CTL] & PCC2_TCTL_CEN) {
		uint32_t old_count1 = count1;
		count1 += steps;

		/*  Did we pass the compare value?  */
		if ((old_count1 < compare1 && count1 >= compare1) ||
		    (old_count1 < compare1 && count1 < old_count1)) {
			interrupt1 = 1;

			if (d->pcctwo_reg[PCCTWO_T1CTL] & PCC2_TCTL_COC) {
				while (count1 >= compare1) {
					count1 -= compare1;
					interrupt1 ++;
				}
				interrupt1 --;
			}
		}

		/*  Overflow?  */
		if ((int32_t) old_count1 >= 0 && (int32_t) count1 < 0) {
			int oc = 1 + (d->pcctwo_reg[PCCTWO_T1CTL] >> 4);
			d->pcctwo_reg[PCCTWO_T1CTL] &= ~PCC2_TCTL_OVF;
			d->pcctwo_reg[PCCTWO_T1CTL] |= (oc << 4);
		}
	}

	/*  ... and the same for timer 2:  */
	if (d->pcctwo_reg[PCCTWO_T2CTL] & PCC2_TCTL_CEN) {
		uint32_t old_count2 = count2;
		count2 += steps;

		if ((old_count2 < compare2 && count2 >= compare2) ||
		    (old_count2 < compare2 && count2 < old_count2)) {
			interrupt2 = 1;
			if (d->pcctwo_reg[PCCTWO_T2CTL] & PCC2_TCTL_COC) {
				while (count2 >= compare2) {
					count2 -= compare2;
					interrupt2 ++;
				}
				interrupt2 --;
			}
		}

		if ((int32_t) old_count2 >= 0 && (int32_t) count2 < 0) {
			int oc = 1 + (d->pcctwo_reg[PCCTWO_T2CTL] >> 4);
			d->pcctwo_reg[PCCTWO_T2CTL] &= ~PCC2_TCTL_OVF;
			d->pcctwo_reg[PCCTWO_T2CTL] |= (oc << 4);
		}
	}

	/*  Should we cause interrupts?  */
	if (interrupt1 && d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pending_timer1_interrupts += interrupt1;
	if (interrupt2 && d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pending_timer2_interrupts += interrupt2;

	/*  Write back values:  */
	write32(&d->pcctwo_reg[PCCTWO_T1COUNT], count1);
	write32(&d->pcctwo_reg[PCCTWO_T2COUNT], count2);
}


static void reassert_interrupts(struct pcc2_data *d)
{
	int assert = 0;

	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		/*  The M68000 interrupt mechanism involves outputting
		    interrupt level on pins EIPL<2..0>. Not implemented
		    yet.  */
		fatal("pcc2: C040 interrupt assertions... TODO\n");
		exit(1);
	}

	/*
	 *  Recalculate current interrupt level:
	 */
	d->pcctwo_reg[PCCTWO_IPL] = 0;

	/*  Timer interrupts?  */
	if (d->pending_timer1_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T1ICR] |= PCC2_TTIRQ_INT;
	if (d->pending_timer2_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T2ICR] |= PCC2_TTIRQ_INT;

	if (d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER1;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}
	if (d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER2;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_TX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_RX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCSI;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	/*  TODO: Other interrupt sources.  */

	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
		assert = 1;

	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
		assert ? "ASSERT" : "no assert");

	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
		assert = 0;

	if (assert)
		INTERRUPT_ASSERT(d->cpu_irq);
	else
		INTERRUPT_DEASSERT(d->cpu_irq);
}


void pcctwo_interrupt_common(struct interrupt *interrupt, int assert)
{
	struct pcc2_data *d = (struct pcc2_data *) interrupt->extra;

	switch (interrupt->line) {

	case PCC2V_SCSI:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCSIICR] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCSIICR] &= ~PCC2_IRQ_INT;
		break;

	case PCC2V_SCC_TX:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCCTX] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCCTX] &= ~PCC2_IRQ_INT;
		break;

	case PCC2V_SCC_RX:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCCRX] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCCRX] &= ~PCC2_IRQ_INT;
		break;

	default:fatal("[ pcctwo_interrupt_common: TODO: line = %i ]\n",
		    interrupt->line);
		exit(1);
	}

	reassert_interrupts(d);
}


static void pcctwo_interrupt_assert(struct interrupt *interrupt)
{
	pcctwo_interrupt_common(interrupt, 1);
}
static void pcctwo_interrupt_deassert(struct interrupt *interrupt)
{
	pcctwo_interrupt_common(interrupt, 0);
}



static void reassert_interrupts(struct pcc2_data *d)
{
	int assert = 0;

	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		/*  The M68000 interrupt mechanism involves outputting
		    interrupt level on pins EIPL<2..0>. Not implemented
		    yet.  */
		fatal("pcc2: C040 interrupt assertions... TODO\n");
		exit(1);
	}

	/*
	 *  Recalculate current interrupt level:
	 */
	d->pcctwo_reg[PCCTWO_IPL] = 0;

	/*  Timer interrupts?  */
	if (d->pending_timer1_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T1ICR] |= PCC2_TTIRQ_INT;
	if (d->pending_timer2_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T2ICR] |= PCC2_TTIRQ_INT;

	if (d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER1;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}
	if (d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER2;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_TX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_RX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCSI;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	/*  TODO: Other interrupt sources.  */

	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
		assert = 1;

	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
		assert ? "ASSERT" : "no assert");

	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
		assert = 0;

	if (assert)
		INTERRUPT_ASSERT(d->cpu_irq);
	else
		INTERRUPT_DEASSERT(d->cpu_irq);
}
```

## THE DETECTOR'S CONTRACT (the probe's docstring, VERBATIM)

```
pcc2widthkills DETECTOR -- the twelve width-guard blocks in DEVICE_ACCESS(pcc2).

WHAT THE FIX DID.  Twelve `if (len != 1)' blocks -- TEN `fatal(); exit(1)' kills that ended the host on
a guest-chosen access width, and two #119 warn-once latches that refused it with a
process-global static.  The
tree's own header says PCC2 registers "can be accessed as bytes, two-bytes, or
four-bytes", so the width is LEGAL.  The fix is a DIRECTION SPLIT:

    READS   ACCEPT -- the memcpy above the switch already served them, raw bytes in
            address order, width-correct by construction.  The guard discarded a
            correct answer.
    WRITES  DECLINE + per-instance latched announce -- every STORING write arm uses `idata'
            (SCCERR stores a constant 0; PSCALEADJ and IPL store nothing and print),
            the big-endian-composed value, which is "the addressed byte" ONLY at
            len==1.  Deleting the guard would store the NEIGHBOUR's lane.

CONTRACT (vacuity-floor clause (e)) -- what this detector is designed to catch:

  CATCHES
    * reinstatement of the kill at any of the SIX GUEST-reachable blocks (survival
      rows paired with a liveness observable, because exit status cannot tell
      "declined and quit" from "died with status 0");
    * *** pass 2: the two FOLDED-IN arms, IPL and MASK, had NO ROW -- twelve blocks
      converted, ten given rows, and the shipped contract did not say so.  A seat
      found it by sibling parity: MASK is GENCTL's twin and had none of GENCTL's rows.
      Repaired: IPL is EVEN and therefore the SIXTH guest-reachable block (survival +
      message rows); MASK is odd (operator rows) and gets GENCTL's readback. ***
    * reinstatement at any of the six OPERATOR-only blocks (VECBASE, PSCALEADJ, SCCICR,
      SCCRX, SCSIICR, MASK; the T1CTL/T1ICR labels are odd too but share TxCTL/TxICR's
      blocks), through the debugger's `put h' at an odd address -- MEASURED to warn
      and store and kill
      (artifacts/pcc2widthkills/operator_reach_20260903.out);
    * *** DELETE instead of decline on the write side -- the lane hazard.  `st.h
      0xAABB' to GENCTL must leave GENCTL unchanged; a bare deletion stores 0xBB,
      VECBASE's lane, because (uint8_t) idata is the HIGHEST-address byte ***;
    * an accidental per-lane compose (GENCTL would read 0xAA);
    * the value a wide READ composes -- lane order and width -- not merely survival;
    * loss of the latch in either direction: dropped `|=' floods (same site twice
      must announce ONCE), and one bit shared across blocks silences (two sites must
      announce TWICE);
    * the de-escalation clause: at the five even blocks with `acc' rows a legal byte write
      lands and reads back through the arm's own mask with NO decline message; at all
      twelve, `acc all' pins NO decline and survival (a guard grown to refuse bytes); at
      the two print-only arms the body's own print is the proof (`acc pscale ign',
      `acc ipl ro').  SCCERR's byte side is value-identical (always 0) and is disclosed,
      not claimed.

  THE ENUMERATION (pass 3 class closure, pass 4 domain repair).  Twelve blocks x NINE
  clause-(d) shapes, the helper's own two operations, and four access widths.  Two
  consecutive passes found breaches of ONE class -- a block with no channel for the
  ANNOUNCE-THEN-FALL-THROUGH shape (guard kept, announce kept, `break' removed, the
  halfword LANDS) -- at MASK, then at four odd arms, then (pass 3, MEASURED 82/82 by a
  seat) at VECBASE, whose `rb vecbase' row is GENCTL's neighbour-lane check and never
  writes wide to VECBASE's own arm.  So the space is written down, cell by cell.
  M = measured kill (log named in CHANGELOG/PRETABLE); S = same channel as a measured
  shape at that arm (the mutant lands the write exactly as the measured one does);
  E = equivalent by construction, with its warrant.  Shapes: DEL guard deleted; LEN
  `len != 1' -> `len > 2' (halfword lands, word declined); LEN2 its MIRROR, `len != 1' ->
  `len == 2' (halfword declined, WORD lands -- named by the codex seat on pass 3); KILL
  verbatim exit(1) reinstated; ALIAS one enum member for two blocks; FALL announce-then-
  fall-through; SWAP guard operand `len' -> `idata > 0xff'; GROW the guard widened to
  decline the LEGAL byte width too (`len != 1' -> `len != 0'), the de-escalation clause.

      block      DEL   LEN   LEN2  KILL  ALIAS FALL  SWAP  GROW   FALL channel
      GENCTL     M     S     W     S     C     M     M     A/C    rb genctl (table 1 M_NOBREAK)
      VECBASE    S     S     W     M     C     M     C     C      rb vecbase own  (pass-3 repair)
      PSCALEADJ  S     S     W     S     C     M     C     A/C    op pscale noig  (message; acc pscale ign)
      TxCTL      S     M     W     S     C     M     C     A/C    rb t2ctl (FALL: part 3b, t2 and t1)
      TxICR      M     M     W     S     C     S     C     A/C    rb t2icr
      SCCERR     S     M     S     S     C     E     C     A/C    E: the arm stores 0 and nothing in
                                                                  the model ever stores a nonzero
                                                                  SCCERR (deriver: every writer of
                                                                  pcctwo_reg[], grep -F 'pcctwo_reg[';
                                                                  the counter memcpy's 8-byte span
                                                                  is pcc2counter8, disclosed)
      SCCICR     S     S     W     S     C     M     C     C      rb sccicr
      SCCTX      M     M     W     S     C     S     C     A/C    rb scctx
      SCCRX      S     S     W     S     C     M     C     C      rb sccrx
      SCSIICR    S     S     W     S     C     M     C     C      rb scsiicr
      IPL        S     S     W     M     C     M     C     A/C    hwr ipl noig    (pass-3 repair; acc ipl ro;
                                                                  the write body prints once)
      MASK       M     M     W     M     C     M     C     C      rb mask
      C  = the cardinality row `latch all' (twelve wide writes, twelve announces): ALIAS,
           any collision drops the count; SWAP: the bare swap drops the length test and every byte preset
           kills it (part 7, 95/171); a value-test QUALIFIER on the guard is caught only
           for the VALUES rows drive AT EVERY ARM -- 3 (`latch all'), 1 (`latch all
           one') and 0 (`latch all zero') -- and, per arm, for whatever that arm's own
           wide-write rows drive (0xaabb, 0xaab8, 0x0022 ...); any other constant is not
           (passes 7-8; Opus F13).
      W  = `latch all w' (twelve WORD writes via put w, twelve announces): a `len == 2'
           guard at ANY arm lets the word land silently and drops the count.  SCCERR's
           own word rows (wrd/wwr sccerr) are its S.
      A/C = the arm's own `acc' row, AND `acc all' (twelve legal GUEST byte stores, ZERO
           declines): a guard grown to refuse bytes at ANY arm announces and reds it.
           Blocks marked C alone have no per-arm acc row; `acc all' is their channel.
           NOT the debugger's `put b': it calls memory_rw with NO_EXCEPTIONS, which does not
           dispatch to a DM_DEFAULT device, so a `put b' row could not see the grown guard
           (MEASURED: 95/96 in part 3 and 96/96 in part 3b, the mutation proven in the binary).  `put h/w/d' go
           through the store_Nbit_word helpers and do reach the arms.
      DEL/LEN/KILL cells marked S land the write, or die, exactly as the measured shape at
      that arm does, and the arm's own dcl / survival
      / readback rows are the channel.  KILL cells' channel is the survival PAIR (exit
      status plus the liveness observable), which varies under a reinstated kill by
      construction; the CHANNEL rule's 'survival-only' names a survival oracle at a
      REFUSAL-effect site, which a kill is not.  `d->warned' is a 32-bit field with twelve bits assigned.

      A NINTH SHAPE, on the input the six-shape list named and never walked: RDDECL, the
      direction split's own conjunct nulled, `writeflag == MEM_WRITE' -> `<= MEM_WRITE'
      (ONE character; MEM_READ is 0).  The Opus seat MEASURED it 82/82 on pass 3: wide
      READS were declined, announced as writes, skipped the arm's read body and consumed
      the block's latch bit -- and no session holding a wide read carried a decline-count
      row.  Closed by `hrd <block> nod' / `wrd sccerr nod' on the SEVEN wide-read sessions
      that already existed (six even blocks by ld.h, SCCERR by ld): a declined read is a
      DECL where zero is expected.  The six ODD blocks' WIDE-read cells are UNREACHABLE by
      construction -- a guest wide read at an odd offset alignment-faults before memory_rw
      (BYTE reads do reach them; see THE SECOND PREDICATE),
      and a debugger read does not dispatch to a DM_DEFAULT device -- and are disclosed,
      not rowed.  One cosmetic gap, disclosed: the seven `op * dcl' rows count the GENERIC
      decline text, and for FIVE arms (VECBASE, PSCALEADJ, SCCICR, SCCRX, SCSIICR) no other
      row pins the name string, so a change of the NAME alone there is invisible; the
      T1 labels share TxCTL/TxICR's fatal() with the named `rb t2ctl dcl' / `rb t2icr dcl'
      rows, and `latch all' pins cardinality.

      THE SHARED BLOCKS.  TxCTL serves T1CTL (0x17, odd) and T2CTL (0x16, even); TxICR
      serves T1ICR (0x1b) and T2ICR (0x1a).  The blocks' readbacks above are at the T2
      offsets; a seat noted that a fall-through reaching only the T1 labels (the block
      split in two) would leave `op t1ctl dcl' at 1 with nothing reading T1CTL back.  So
      the T1 labels carry their own operator-path readbacks, `rb t1ctl' and `rb t1icr'.
      THE THIRTEENTH ARM.  SCCRXIACK has NO width guard and never had one: its body
      ignores `idata' (it clears a bit in SCCRX and reasserts), so its effect is
      width-invariant by construction and it is not a member of the twelve.  It is named
      here so the census is not read as an omission.
      SESSIONS.  Every session() is a fresh pty.fork/execv of the emulator, so no latch
      state survives from one row to the next; `latch all' counts one process.
      THE HELPER'S OWN OPERATIONS (pass 4).  pcc2_width_decline() has two lines that
      every block depends on: the TEST `!(d->warned & (1u << bit))' and the SET
      `d->warned |= (1u << bit)'.  One-token edits to the SET line escaped every row:
      `|=' -> `=' (assign: A, B clears A -- `latch aba' A,B,A = 2) and `(1u << bit)' ->
      `1' (bit 0 always: every other block announces every time -- `latch same2', MASK
      twice = 1).  The TEST line's operand swap (`&' -> `==') is caught by `latch all':
      with the field accumulating, equality fails from the second block on and it
      announces 12 either way; `latch aba' DOES distinguish it (A=1, then the field is 3,
      and 3 == 1 is false, so A re-announces -- MEASURED 100/101 by a pass-5 seat).  An
      earlier version of this sentence called it indistinguishable; the instrument was
      stronger than its contract said.  `|=' -> `^=' or `+=' in the SET line is
      EQUIVALENT: the SET runs only under the TEST, i.e. only when the bit is clear.
      WIDTHS.  The debugger drives len 2 (`put h'), 4 (`put w') and 8 (`put d'); the
      guest drives 1, 2 and 4.  `latch all', `latch all w' and `latch all d' pin the
      ANNOUNCE at every block for each non-byte width, so a guard true on a subset of
      {2,4,8} drops one of the three counts; the REFUSAL per width is `rb *', `rb4 *'
      and `rb8 *' (see THE LANDING CHANNEL AT EVERY WIDTH).
      BIT IDENTITY.  `latch all' and `latch all w' are cardinality rows: they assert
      twelve announces, never WHICH bit.  A translation of the bit index
      (`1u << bit' -> `1u << (bit + 1)') is EQUIVALENT by construction -- no code
      outside pcc2_width_decline() reads d->warned's bits -- and was MEASURED 96/96 by a
      pass-4 seat as the clause-(f) control.  That warrant expires the day anything
      indexes or reports those bits.
      ANNOUNCE SEVERITY.  Every row counts TEXT on a pty run under -V; `fatal(' ->
      `debug(' in the helper changes no text these rows read.  NOT CAUGHT, disclosed;
      the fork's recorded warrant for fatal() over debug() is dev_asc.c's (-q makes a
      debug()-level line invisible to the boot-log hygiene grep).
      THE FAULT MEMBER.  `break' -> `return 0' at a guard turns the decline into a bus
      error.  At the six GUEST-reachable blocks the guest's store faults and the program
      never prints, so the block's `lv' row reds while its `hwr' row stays green -- the
      HOST survives (M_RET0_GENCTL, part 4: `hwr genctl lv' died, `hwr genctl' exit0; an
      earlier version of this sentence and PRETABLE_pass4 said the pair).  At
      the six OPERATOR-only blocks NOTHING above sees it -- MEASURED 101/101 at VECBASE
      by a pass-5 seat -- so `latch all fail' counts memory_rw's "failed ]" line at zero
      over the twelve-block session (M_RET0_VECBASE, part 5).
      THE FIX'S OWN STATE AS A GUARD INPUT (pass 5, MEASURED 101/101 at one arm and at all
      twelve by the Opus seat).  A guard qualified by its own latch bit -- `&& !(d->warned &
      (1u << bit))', the canonical clause-(d) conjunct -- declines and announces the FIRST
      wide write exactly as the fix does and lands the SECOND.  Every row above observed
      the device only while its latch was still armed.  Closed at every block by `rb2 *'
      (set, two wide writes, read back), `pscale noig2' and `ipl noig2' (the body's print,
      counted at zero after two writes); SCCERR is value-identical there too (E).
      THE SECOND PREDICATE.  Each arm's `if (writeflag == MEM_WRITE)' is now load-bearing
      for reads that fall through to it: WIDE reads at the even blocks since the split
      (the pre-fix guard killed them first), and BYTE reads at EVERY block, always (a byte
      access skips the alignment check and passes `len != 1').  Deleting it stores
      idata == 0 on a read while the readback in the same stream -- served by the memcpy
      before the switch -- still prints the old value; only a second read sees it.
      Pinned by `hrd * rb' (wide, four even storing blocks), `hrd ipl noro', and by
      `brd2 *' (byte, read twice, all nine storing blocks) with `brd pscale noig' /
      `brd ipl noro'; SCCERR is E.  It does not dominate the edited lines, so it sits
      outside the clause-(d) closure and is carried here as construction, not as a breach.
      THE LANDING CHANNEL AT EVERY WIDTH (pass 6, Opus seat, measured).  `latch all',
      `latch all w' and `latch all d' pin the ANNOUNCE at all twelve for len 2, 4, 8 --
      not the refusal: `break;' -> `if (len < 4) break;' at all twelve announced and
      LANDED every 4- and 8-byte write and scored 118/118.  The REFUSAL is pinned per
      width by `rb *' (len 2), `rb4 *' and `rb8 *' (nine storing blocks each, and the T1CTL /
      T1ICR labels), by
      `pscale noig4|8' / `ipl noig4|8' (the print-only bodies), and announce-once per
      width by `latch same' / `latch samew' / `latch samed'; SCCERR is E at every width.
      Landed lanes under a fall-through, len 4 / len 8: MASK 0xdd/0x44, VECBASE
      0xd0/0x40, TxCTL 0x01/0x00, TxICR 0x15/0x04, SCCICR and SCCTX (`& 0x1f') 0x1d/0x04,
      SCCRX and SCSIICR (`& 0xdf') 0xdd/0x44; GENCTL's own lanes 0xd9/0x40 -- none equals
      its preset, and none carries PCC2_C040 at GENCTL.
      The 8-byte pattern's low lane is 0x44 because 0x33 EQUALLED the TxCTL and TxICR
      presets through `& 3' and `& 0x17' -- measured in part 6, where `rb8 t2ctl' and
      `rb8 t2icr' stayed green under the fall-through; a readback row must choose a
      value whose landed lane differs from the preset under THAT arm's mask.
      The 4- and 8-byte rows are OPERATOR rows (`put w' / `put d'): only SCCERR is
      4-aligned, so a guest word store reaches no other block.
      THE GUARD'S OPERAND SPACE, CLOSED AS A CLASS (pass 6; RESTATED pass 7 after the same
      class was found a third time).  Clause (d) rule (2) draws a guard's extra operand from
      the LVALUES THE GUARDED BODY READS, walked to the enclosing function only -- never into
      callees -- so the closure is NON-TRANSITIVE BY DEFINITION.  Enumerated per arm, each
      lvalue with the bits a row CAN hold (dead bits -- set by no writer -- are named as
      such) and the row holding it non-initial at a wide write:
        TxCTL   reads d->pcctwo_reg[relative_addr] (RMW): bits 0-1 by the byte presets
                (`rb/rb4/rb8 t2ctl', `rb/rb4/rb8 t1ctl'); bits 4-7, the overflow count that
                ONLY pcc_timer_tick sets, held at 1 by `ovf1 *' / `ovf2 *' and at >= 8 (bit 7;
                the rows mask to bits 7 and 0, so 9-15 under host load read the same)
                by `ovfhi1 *' / `ovfhi2 *' (free-running, the count re-armed each iteration);
                a predicate true of 0, 1 and 8 alike is disclosed, not owed -- NAMED: the
                count at 2-7 and 9-15, bits 0-1 = 2 (COC alone), the byte 0xff; bits 2-3
                are set by NO model writer (the body stores `idata & 3', COVF only clears,
                the tick writes bits 4-7) except the counter arm's raw memcpy -- the filed
                pcc2counter8 path, which a guest `st.d' at the 8-aligned T2COUNT reaches --
                so they are held, all at once with bits 5-7, by `rb t2ctl b27' / `rb t1ctl
                b27' (measured: `&& !(reg & COVF)' 188/190).  Those two rows REST ON A FILED
                DEFECT and must be re-cut when it is fixed (bits 4-7 via overflows; bits 2-3
                then have no writer and become dead).  Pass 9 corrected the earlier sentence
                here that called the path operator-only and the bits E with no row.
        TxICR   reads the register (bits 0, 1 and 4 by the 0x13 presets, bit 2 by the 0x17
                presets; the combination 0x37 -- IL bit 2 with INT -- is held by no row and a
                guard exempting exactly it is a disclosed escape by name; continuing:
                presets of `rb t2icr il4' / `rb t1icr il4'; bit 5 INT, set ONLY by
                reassert_interrupts under a pending count, by `pend*'),
                d->pending_timer1/2_interrupts, held at 1 by `pend1 *' / `pend2 *' and at
                thousands by `pendn1 *' / `pendn2 *' (COC with compare 1; a predicate true of
                1 and ~9999 alike, `< 10000' say, is disclosed by name), and JOINTLY with
                each other, with the label and with the tested bits of idata (JOINT CELLS below), and relative_addr
                (the T1/T2 label: `rb t1icr', `op t1icr dcl', `pend1 *' hold the T1 value,
                every T2 row the other).
                TxCTL reads relative_addr too, as its RMW index: the same T1/T2 rows.
                BIT COVERAGE, the checkable form of the above (pass 9, Opus seat): reg[TxCTL]
                is held at {0x00, 0x03, 0x11, 0x81 (masked to bit 7 and CEN: the masked rows' KILL channel
                is CEN alone -- a landed write drives idata 0 and clears it -- bit 7 is arming, and
                bits 1-6 of that state are pinned only by `ovf*' at the exact 0x11, so the ovfhi wide
                writes must keep bit 0 clear; Opus, pass 10), 0xfc} -- all eight bits held SET and CLEAR;
                reg[TxICR] at {0x00, 0x13, 0x17, 0x31} -- every live bit (0, 1, 2, 4, 5) both
                ways, bits 3, 6, 7 dead by census.  That is why every single-bit predicate on
                either register is killed, and it is what a future edit must preserve; the
                pending counts are held at 0, 1 and thousands.
                JOINT CELLS.  The rule (pass 10, the flagship seat; BOUNDED on pass 11 by the same
                seat against its own letter; CLAUDE.md clause (d)): a joint cell is ENUMERATED when
                the guarded body's own code distinguishes it, and the FLOOR -- the cells a row is
                OWED for -- is the cross-product of the guard's dominating predicates with the
                device-STATE lvalues the fix's own repair path reads that are jointly reachable
                through its own data flow.  Here that is {T2, T1} x {p1 = 0, > 0} x {p2 = 0, > 0}:
                one pcc_timer_tick callback increments both counts and reassert_interrupts reads
                both, so (p1, p2) is a joint input of the model.  EIGHT floor cells, every one held
                at a wide write: (T2, 0, 0) by `latch all' (0x0003) and `rb t2icr' (0xaab8), (T1, 0, 0) by `op t1icr dcl' (0x0303) and `rb t1icr' -- NOT `latch all', which iterates BLOCKS12 at 0x1a and never writes T1ICR (Opus, pass 11); (T1, >0, 0) `pend1 rb'; (T2, >0,
                0) `pend1 rb2'; (T2, 0, >0) `pend2 rb'; (T1, 0, >0) `pend2 rb1'; (T2, >0, >0)
                `pendboth rb'; (T1, >0, >0) `pendboth rb1'.  BEYOND THE FLOOR, HELD AS A GENERATING
                SET (grok, pass 11): the bits of the written idata that the body tests -- IEN (0x10),
                ICLR (0x08, a write strobe), the HUH? bits 0xe0 -- are single-operand MARGINALS of
                the value, not floor; yet at EVERY pending cell each is written both clear and set
                (0x0000; 0x0013; 0x0018; 0x0020 -- the `*i', `*c', `*h' readbacks, with a `huh' row
                per session as the HUH? print channel), so any single-axis extra conjunct on one of
                them at a pending cell lands a write and reds a readback (M_P2IEN, M_ICLR, M_HI,
                M_P1IEN).  The idle rows drive 0xaab8 (IEN|ICLR|INT|0x80) at both labels and 0x0003 / 0x0303, so the same
                holds at the (0, 0) cells.  DISCLOSED, with the derivation: multi-axis idata joints at
                a pending cell (`!(p2 && (idata & ICLR) && (idata & 0xe0))' and the like -- every held
                write sets at most one of the three); INT clear with a count pending -- UNREACHABLE on
                the model (the tick increments only under IEN and reassert sets INT before any guard
                runs; grok); pending counts >= 2 at once (the body tests `> 0' only; grok read OpenBSD's
                clock.c as arming COC on both timers -- not in this tree, NOT independently verified;
                the in-tree warrant is the model's joint handling); `idata == k' for any k no row
                drives; TxICR 0x37; TxCTL 0xff; the overflow count at 2-7 and 9-15.  Pass 9 held one
                floor cell; pass 10 the label mirror and its neighbours (Opus, codex); pass 11 found
                the ICLR x pending cell open (three seats, the Opus seat measured it) and the rule's
                letter over-demanding (its own author).  The De Morgan form of the original gap (kimi
                substitute): `!(p1 && p2)' is `p1 == 0 || p2 == 0' -- neither disjunct true of all its
                lvalue's held values, the disjunction true in every row, so a per-lvalue disclosure
                test could never fire on it.
                THE ENUMERATION ACROSS THE ARMS (pass 11 batch two; the class-closure amendment: three
                passes found one class -- an unvaried axis crossed with a varied one -- so the repair
                owes the enumeration, not another cell).  Read off each guarded write body, the axes its
                code makes DECISIVE (tested in an `if', or used as an index), and what the rows hold:
                  GENCTL, VECBASE, SCCICR, SCCTX, SCCRX, SCSIICR, SCCERR, PSCALEADJ, MASK -- stores,
                     masks or a print with NO `if' on state or idata: no axis beyond the label; the
                     plain rows hold every label.  (Their callee reassert_interrupts tests C040/MIEN --
                     out of the closure: non-transitive.)
                  IPL -- one function-static latch `w': held clear (`ipl noig2') and set (`ipl wset').
                  TxCTL -- the label (an RMW index), the register's overflow-count class {0, 1, >= 8,
                     0xfc-via-memcpy} and two tested idata bits, COVF (`if (idata & PCC2_TCTL_COVF)')
                     and the HUH? bits (`if (idata & ~7)').  Generating set: in the four overflow
                     sessions COVF-set (0x0004) and HUH?-bit-set (0x0008) writes at the ARMED label,
                     then the IDLE label preset to 0x02 (COC without CEN) with 0x0000 / 0x0004 /
                     0x0008 -- the `ovf* rbv/rbx/rb1/rb1v/rb1x' and `ovf1/ovfhi1 rb2*' readbacks and an
                     `ovf* huh' row per session.  Landed values never equal a preset: count 1 -> 0x00
                     (COVF clears the count and itself) / 0x10 (+ HUH?); count >= 8 -> 0x00 / 0x80
                     masked; idle 0x02 -> 0x00.  Disclosed: COVF at the 0xfc cell (rests on the filed
                     pcc2counter8 path) and at the plain 0x03 cell (a preset of 0x03 would start the
                     idle timer); the HUH? bits are held at the plain cell by 0xaab8 (lane 0xb8).
                  TxICR -- passes 9 to 11 above.
                A future arm added to the guard set owes this paragraph one line before its rows.
                Bit 3 (ICLR, 0x08) is a WRITE STROBE: the body TESTS it (`idata & PCC2_TTIRQ_ICLR') and
                never stores it -- the store mask 0x17 is bits 0, 1, 2, 4 -- so the register bit is set by
                no writer (pass 10 accepted a sentence calling the mask a writer of it; pass 11 reverted
                that: 0x17 & 0x08 == 0).  Bits 6-7 of the TxICR byte are set by no writer at all (body `idata & 0x17',
                reassert bit 5, the counter memcpy cannot reach 0x1a): E, same warrant.
        IPL     reads the function-static `w' of its WRITE branch (its #119 print latch):
                `ipl wset'.  The READ branch has a second static of the same name; it is
                outside the closure (not the guarded write body) and `ipl rset' holds it
                set anyway.
        helper  reads d->warned: `rb2 *' holds each arm's OWN bit set; a guard naming
                ANOTHER arm's bit (the sibling round's foreign-bit cell, sgi_de pass 16,
                filed there as derived-not-measured) is held by `latch all' + `latch all
                rev' -- every ordered pair of blocks, measured in part 8.
        GENCTL, VECBASE, SCCICR, SCCTX, SCCRX, SCSIICR, MASK: pure stores (`= idata & m'),
                reading no PRIOR device state -- `idata' (the value under test, read by ten
                of the twelve bodies) is held by every wide-write row and pinned per arm by
                `latch all' / `latch all one' / `latch all zero'.  SCCERR: constant store.
                PSCALEADJ: reads only idata (print).  So a guard conditioned on those registers' bits
                (the SCC* INT bits included) is OUTSIDE the closure; the byte presets still
                pin their landing.
      OUT OF CLOSURE, disclosed not owed: d->pcctwo_reg[PCCTWO_IPL] is read by the IPL arm's
      READ branch and by the callee reassert_interrupts(), not by IPL's guarded write body --
      `&& reg[IPL] == 0' at the IPL guard escapes with a one-message consequence, and at any
      arm no row wide-writes with an interrupt pending; at TxICR the pend rows DO (reassert
      has raised IPL to the pending level), so the all-twelve form is killed there: MEASURED
      by the pass-7 Opus seat, 155/159, red pend1/pend2 decl+rb (pass7_seats_20260904/opus/).
      Likewise `&& pending_timer2 == 0' at all twelve: 157/159,
      the TxICR-only signature -- the conjunct is invisible at the other eleven arms, which
      is what the non-transitive closure predicts and discloses;
      cur_int_vec[] is WRITTEN by reassert_interrupts() and read only by the IACK handler.
      GATE 14 IS LOAD-SENSITIVE since pass 6: the pend*/ovf* rows need the host's 100 Hz
      SIGALRM to fire during a `continue' (20 s ceiling -- inert until pass 8: the tuple's
      third element was read after unpacking, so the wait returned at once), so a starved
      host reds them for a
      reason the row names (`no-breakpoint') -- run the gate alone.  Their poll loops also
      rely on GENCTL.MIEN being clear at init, so the guest never takes the interrupt.
      At GENCTL the 4-/8-byte lanes are 0xd9 / 0x40: 0xdd and 0x44 carry PCC2_C040 and a
      LANDED write there ends the host (pcc2c040kill) -- the row would still kill, by death
      instead of by value, and the NOROW line below would be false (pass 7, measured).
      reassert_interrupts() (a callee of seven bodies) reads GENCTL, the pending counts, the
      TxICR / SCC* IEN, INT and IL bits, MASK and IPL.  `latch all fail' rests on memory_rw's
      debug() line, which prints because this probe single-steps.
      pending_timer1/2_interrupts are INCREMENTED only by pcc_timer_tick (a SIGALRM callback
      that debugger.c stops during `step'); the TxICR body clears and decrements them.
      NOT PINNED, disclosed: the announce's `len=%i' value -- no row reads it (cosmetic,
      the NAME gap's sibling).  And the generic-DECL counts are over the WHOLE pty
      transcript: three other devices emit the same suffix, none instantiated on mvme187.
      OTHER DEVICE STATE AS A GUARD OPERAND (pass 6).  A guard conditioned on
      d->pcctwo_reg[], pending_timer*, the TxICR INT bit or reg[IPL] being NONZERO
      declines nothing in the init-state sessions (of the twelve guarded registers only
      VECBASE 0x0f and PSCALEADJ 0xdf are non-zero at init; CHIPID 0x20 is, and is not one
      of them), so `latch all' reads 0 -- killed.  One conditioned on them
      being ZERO is the shipped behaviour in every row that holds the field at its init
      value; MEASURED by both Agent seats at TxICR (`&& !d->pending_timer2_interrupts',
      `&& d->pending_timer1_interrupts == 0': 118/118 each) and closed as a class -- see
      THE GUARD'S OPERAND SPACE below.  The latch-set check (`rb2 *') is at width 2 only;
      the qualified-guard shape is width-agnostic, so its 4- and 8-byte repeats are
      coverage debt, FILED, not a floor cell.
      THE ODD BLOCKS FIRST.  Every guest-side channel at an odd block is absent by
      construction, and three consecutive passes found a shape with no channel there
      (fall-through x4, then at VECBASE and IPL, then FAULT x6).  A new shape is checked
      against the six operator-only blocks before anything else.
      INSTRUMENTS.  Parts 3, 3b and 3c ran three frozen copies (md5 3dcf73de, 280d9ab3,
      72759b4f); the last is the shipped probe.  3 -> 3b changed only `rb t1ctl' /
      `rb t1icr's expected string, 3b -> 3c only `acc all's session; row-name sets are
      identical and no killing row was touched, so the part-3 kills TRANSFER.  `acc all'
      was REWRITTEN, not added: its warrant is that the session is self-contained and
      part 3c measured the rewrite (95/96, `acc all' alone).

  DOES NOT CATCH, stated so an escape is outside the contract rather than an argument
    * per-instance vs process-global latch state: mvme187 instantiates ONE pcc2, so no
      session can hold two instances.  The bitfield is per-instance by construction;
      nothing here measures it;
    * pcc2c040kill -- a LEGAL byte write of 0x04 to GENCTL still ends the host in
      reassert_interrupts().  Every GENCTL lane value here keeps bit 0x04 CLEAR so no
      row dies for that reason;
    * pcc2defaultkill -- an unlisted offset (0x06, 0x14, 0x18, 0x2c ...) still ends the
      host in `default:';
    * pcc2counter8 -- the counter arm's raw memcpy of an 8-byte write;
    * what real hardware does with the LANES of a wide write (not on disk);
    * the SCCERR word-write's stored value: the arm always stores 0, so a decline and
      an accept are value-identical there and the row's channel is the message.

Sentinel: PCC2W_PROBE_DONE

```

## THE RULE AS IT STANDS IN CLAUDE.md CLAUSE (d) (VERBATIM)

```
> #### *** JOINT CELLS -- adjudicated 2026-09-04 on `pcc2widthkills` pass 10 by the flagship seat, after
> #### a measuring seat's CONJUNCTION of two body-read counts escaped 190/190 AND THE SAME SEAT ARGUED IT
> #### WAS NOT A BREACH.  Both proposed bounds were rejected; the one adopted came from neither. ***
>
> > **DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues EXACTLY
> > WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM.**  For each lvalue take the PARTITION the
> > body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives
> > {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary
> > boolean functions of the read-set.  A mutant exempting a single cell whose reachability is
> > MEASURED is a floor breach; close the whole cross-product in ONE diff and write into the
> > contract which cells are rowed.  A value or combination the body never tests as a case
> > (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`)
> > is DISCLOSED under clause (e).
>
> **Why this form and not the two that were argued.**  The dissent's discriminator -- *a plausible
> future edit* -- failed three ways: plausibility is not derivable by reading; the mutant was written
> and measured, so it is an edit someone writes; and "single-operand is complete" is measurably
> false, since `&& idata != 2` is single-operand and escapes.  The main loop's own bound -- *pairs of
> body-read lvalues over a finite reachable space* -- was rejected as SELF-REFUTING: the counts' raw
> value space is 2^32 apiece, so "finite" does no bounding work on its motivating case (a C `int` is
> finite -- the first wording here said it was not; codex and glm caught it on pass 11); "reachable
> guest state" would force rowing
> `idata == 2` that the same record discloses; and a PAIRS cap misses `#499`'s four axes.  The
> body-tested-partition form is finite (a product of small partition counts), derivable from the
> diff by reading the body's own `if`s, and it enumerates `#499`'s width x component x direction x
> position cells from `len`, `writeflag` and `relative_addr` -- which neither argued bound reached.
>
> **The measured case.**  The TxICR body tests both pending counts at `> 0` and the label at
> `== T1ICR` / `T2ICR`, so the closure is {T2, T1} x {p1 = 0, > 0} x {p2 = 0, > 0} -- eight cells.
> Pass 9 held one open cell (both counts, T2 label: a 190/190 escape, predicted by the Opus seat
> before its build); pass 10 found the MIRROR (both counts, T1 label) and the (p2 only, T1 label)
> cell open -- the `#499` shape reproduced inside the repair for it -- and the label x p1 x p2 x IEN
> product (sixteen cells) closed in one diff of nine readbacks in existing sessions; the ICLR, INT and
> 0xe0 partitions were disclosed by count, and pass 11 then found the ICLR x pending cell open and
> in-rule (this paragraph said "eight cells ... three readbacks" until pass 11).  **The De Morgan form of the gap**, from the kimi
> substitute: `!(p1 && p2)` is `p1 == 0 || p2 == 0`; neither disjunct is true of all its lvalue's
> held values, the disjunction is true in every row, so a per-lvalue disclosure test can never fire
> on it.  That is why the per-lvalue value-domain statement, correct as far as it went, could not
> see this class at all.
>
> **Two corollaries from the same pass, both measured.**  The PRE-TABLE CHECK's SIBLING PARITY row
> compares BLOCKS; at a block that serves TWO case labels the siblings are the LABELS, and a
> parity census over the row names is what would have shown `pendboth` as the only T2-only cell
> before its table ran (Opus, pass 10).  And the measuring seat's own bound -- the cross-product
> of the value-CLASSES the rows establish, with the dispatch axes as full axes, demand
> INCREMENTAL -- agrees with the body-tested form on every cell that mattered here and differs on
> where the classes come from (the rows, or the body's tests); that residual difference is
> carried to the next pass as a named question rather than settled by the author.
>
> #### *** THE LETTER OVER-DEMANDED, AND ITS OWN AUTHOR BOUNDED IT ONE PASS LATER (pass 11, 2026-09-04). ***
>
> Read literally, "the cross-product of the body-tested partitions" demanded ALL 128 cells at the TxICR
> arm -- the body also tests `idata & IEN`, `idata & ICLR`, the register's INT bit and `idata & 0xe0` --
> and it compounds as 2^k in the `if`-count across twelve arms: the `#392` shape wearing the rule's
> clothes.  Three seats said the letter demands the remainder; the flagship seat, asked to be harder on
> its own rule than on anyone, ruled AGAINST the letter:
>
> > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
> > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
> > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
> > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
> > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
> > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
>
> At TxICR the floor is {label} x {p1} x {p2}: one `pcc_timer_tick` callback increments both counts and
> `reassert_interrupts` reads both, so the pair is a joint input of the model.  Eight cells, all rowed.
>
> **What the debt costs when it has a measured warrant, and it is cheap:** the measuring seat built the
> disclosed `&& !(p2 && (idata & ICLR))` and it escaped the 203-row instrument, as three reading seats
> had predicted -- so the debt was taken as L1 construction in the GENERATING-SET form (grok): at every
> rowed pending cell, write each tested idata bit both clear and set, so any single-axis extra conjunct on
> one of them lands a write and reds a readback.  Twelve wide writes appended to three existing sessions;
> no new session, no new load sensitivity.  Multi-axis idata joints stay disclosed; INT-clear-with-a-count-
> pending is disclosed as UNREACHABLE with its derivation (the tick increments only under IEN and reassert
> sets INT before any guard runs), which is the honest form of a cell nobody rows.
>
> *Two records lessons from the same pass.  A CORRECTION IS NOT SAFER THAN THE THING IT CORRECTS: pass 10
> accepted "the store mask is a writer of ICLR" and made a true sentence false -- `0x17 & 0x08 == 0`, one
> AND that nobody ran.  And a PREDICTION COPIED INTO A MEASURED COLUMN is the frozen-number class in a new
> coat: a table said (0x13) where the log said 0x33; the score matched by coincidence and the value was a
> wrong record until a seat read the log.*
>
> *Count the arguments, not the seats: seven of eight landed seats put the pair inside the closure,
> and the one that did not (minimax) was reading the CONTRACT's per-lvalue wording rather than the
> clause -- the wording the discriminator sentence now replaces.*

> ### *** THE PRE-TABLE CHECK -- three greps, ~30 min, and it protects the ASK-AGAIN'S
> ### CAP rather than the clock. Adopted 2026-08-24; two seats derived it independently. ***
```

## THE CHAIN'S ROUND BLOCKS (titles; the newest block inlined)

    # Round pcc2widthkills, pass 10 -- the rule question adjudicated: a joint cell is in the closure when the guarded body's own code distinguishes it; two more cells measured open by the seat that predic
    # Round pcc2widthkills, pass 9 -- NOT the closing pass: the measuring seat's predicted mutant escaped 190 of 190 (both timers pending, a state no session held); the record corrected in place; the repa
    # Round pcc2widthkills, pass 8 -- not the closing pass: the pass-7 breakpoint wait was inert, and one non-initial value per lvalue is not a domain
    # Round pcc2widthkills, pass 7 -- not the closing pass: the same class a third time, and this time the enumeration is restated by the rule that bounds it
    # Round pcc2widthkills, pass 6 -- not the closing pass: three cells, two of them measured by the seats that then lost their transport, all three closed as classes
    # Round pcc2widthkills, pass 5 -- not the closing pass: the guard qualified by its own latch bit swept the shipped 101 rows, because every row watched the device only while its latch was still armed
    # Round pcc2widthkills, pass 4 -- the enumeration's derivations held, its domain was one function too small, and a one-character edit to the latch swept the shipped 96 rows
    # Round pcc2widthkills, pass 3 -- the same class a third time, three shapes the enumeration never named, and a closure written cell by cell into the contract
    # Round pcc2widthkills, passes 2 and 3 -- the 60-row detector had six clean sweeps, the smallest one character; the repair is 82 rows and every cell of it is measured

```
# Round pcc2widthkills, pass 11 -- the adjudication pass: one accepted disposition reversed (a correction had made a true sentence false), the rule's own author bounded its letter, and the disclosed ICLR cell was measured open -- taken as construction, twelve writes in existing sessions; the repair owes pass 12

**2026-09-04.  Detector 203 -> 218 rows (twelve readbacks and three HUH? rows appended to the three
timer sessions); clause (d) bounded in the carrier; the contract states its floor, what it holds beyond
it, and what it discloses with the derivation; product code unchanged.**

## The verdicts (the nine-seat roster: seven reading seats answering plus the measuring seat; agy deliberately not fired)

Pass 11 was the section-F2 adjudication pass -- every seat saw every other seat's pass-10 findings with
the main loop's disposition on each (sixteen accepted, three rejected, one held) -- and the pass on the
pass-10 repair.  Every landed seat answered question 1 by number.

**Which accepted disposition was wrong: #9, named by grok (its own pass-10 finding), codex and fable5,
and confirmed against the header.**  Pass 10 had accepted "the store mask IS a writer of ICLR" and
rewritten the contract to say so.  `PCC2_TTIRQ_ICLR` is 0x08; the store mask 0x17 is bits 0, 1, 2 and
4; `0x17 & 0x08 == 0`.  ICLR is a write STROBE the body tests and never stores -- which is exactly why
register bit 3 is dead, the same class as bits 6-7.  The original sentence had been right and the
accepted correction made it false: *a correction is not safer than the thing it corrects*, and one AND
would have kept it.  Reverted in the contract, the pass-10 block and the carrier.  The other fifteen
held (fable5: all defensible; grok: all check; codex: #2 carried a false premise -- a C `int` is finite
-- which the carrier now says differently; deepseek: #13's wording contradicted #5 -- the VALUE
both-thousands is unheld, the CELL is rowed -- taken as wording; minimax: F5 should name which table).
The packet-fed challenges to #1 (glm) and #12 (kimi substitute) were adjudicated against with the
reason in the ledger.  **The three rejections stood with every seat, grok recanting its own R1**: this
detector rows operator-only blocks throughout, so a guest-state clause would have to unrow `pend1`.

## H1 -- the rule's own author ruled against its letter

The held question: does the adopted rule -- the cross-product of the body-tested partitions -- demand
rows for the ICLR, INT and 0xe0 partitions the pass-10 repair disclosed by count (112 of 128 cells)?

* **Read literally, yes** (codex, glm, minimax, deepseek): "governs what a landed write DOES, not
  whether it lands" is no exclusion -- an extra conjunct on ICLR or 0xe0 at the GUARD changes whether
  the write lands exactly as IEN does, and IEN was rowed.  codex's constructive census: 96 reachable
  cells at guard entry (two labels, two opposite-timer states, eight idata classes, three stable target
  states), the 32 "count pending, INT clear" cells reachable only through an unmeasured interleaving.
* **The flagship seat, asked to be harder on its own rule than on anyone, bounded it:** the rule
  ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row is OWED for
  -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues the fix's
  own repair path reads that are jointly reachable through its own data flow.  The bits of the single
  value being written are single-operand MARGINALS, not floor.  At TxICR: {label} x {p1} x {p2}, eight
  cells, all rowed by pass 10; the idata joints are clause-(e) debt.  The letter, it said, is 2^k in the
  `if`-count and compounds across twelve arms -- `#392` in the rule's clothes.  Adopted, and written
  into the carrier as the correction of its own one-day-old paragraph.
* **grok's generating set is what the debt costs when it has a warrant:** per idata axis, a set/clear
  pair at every rowed pending cell, so any single-axis extra conjunct reds; unreachable partitions
  disclosed with the derivation (INT clear with a count pending: the tick increments only under IEN and
  `reassert_interrupts` sets INT before any guard runs).
* **The measuring seat's bound, put beside Fable's for pass 12 (the remaining split):** axes = the
  lvalues the body's code makes DECISIVE -- tested in an `if` OR used as an index or selector (which puts
  the T1/T2 axis in at TxCTL, where `relative_addr` is an RMW index no `if` tests); demand = a COVERING
  ARRAY of strength t, t = the longest conjunction the body itself writes (four here), cost O(2^t log k)
  rather than 2^k; disclose BY STRENGTH -- "kills every conjunction of at most t of the N axes" -- which is
  falsifiable and would have made the pass-11 escape unwritable; t and the axis list are read off the diff
  once and no pass may raise t.  It withdrew its own pass-10 "demand INCREMENTAL" as having no stopping
  rule.  Three consecutive passes found ONE class of breach -- an unvaried axis crossed with a varied one,
  190 -> 194 -> 203 -- so the class-closure amendment says the next repair owes THE ENUMERATION across the
  arms, not another cell; the seat derived (not measured) that at TxCTL the rule enumerates {COVF} x
  {idata & ~7} with two of four cells unheld.
* **The measuring seat built the disclosed cell:** `&& !(pending_timer2 && (idata & PCC2_TTIRQ_ICLR))` at the TxICR guard scored **203/203, a TOTAL
  ESCAPE**, on its own clone (`pass11_seats_20260904/opus/M_ICLR.out`; predicted at 16:56 before the
  16:59 mutate script), with a POSITIVE CONTROL proving the write LANDS rather than the mutant never
  reaching the binary -- mutant `CONTROL_RB=0x13, DECL=0` against baseline `0x31, DECL=1`: the store
  gives 0x33, the strobe clears INT and decrements the pending count to 0, reassert leaves INT clear.
  *Entering the cell corrupts the register and silently consumes a pending timer interrupt, with all
  203 rows green.*  A `BASE2` run on the post-edit instrument (md5 12c7a97b) also read 203/203, closing
  a one-instrument straddle the seat reported on itself: its runner re-copied the live probe between
  BASE and the mutant while the main loop applied docstring-only corrections at 17:12 -- seven text
  lines, 203 identical (name, want) pairs, but a class worth naming: **a driver that re-copies its
  instrument straddles any edit, and the main loop should not edit a probe while a seat measures it.**

**Disposition.**  The floor is Fable's; the generating set is cheap (twelve wide writes appended to
three existing sessions, no new session).  **The GRADING is the Opus seat's: L2, a floor breach repaired
in-round, not debt-with-a-warrant** -- by the round's own pass-3 sentence, written into the probe by that
seat, that *a disclosure cannot discharge a floor clause, or every breach becomes a sentence*, and
because the cell sits inside the closure on every bound anyone proposed (the adopted product, Fable's
data-flow floor once the ack path is read as state the fix's own repair touches, Opus's strength-4 or
strength-2 array).  The repair is identical under either grading; the record has to say which holds,
and it is the stricter one.  The contract now says, by name, what is floor, what is held beyond it,
and what is disclosed and why.  The pass-9 Opus dissent and minimax's R3 "correctly sensed
the exponentiality H1 had to fix" (fable5); the fix is the bound, not the dissent's arity cut.

## The repair

At every rowed pending cell -- `pend2` and `pend1` at both labels, `pendboth` at both -- the tested
bits of idata are now written both clear and set: IEN already (0x0000 / 0x0013), now ICLR (0x0018 =
IEN|ICLR: a landed write keeps IEN, and the strobe clears INT and decrements the count, so it reads
0x10) and the HUH? bits (0x0020: a landed write reads 0x20 at an armed ICR and 0x00 at an idle one,
zeroes the count, and PRINTS the HUH? line -- counted by a `huh` row per session as a second channel).
Twelve readbacks (`*c`, `*h` at each label) and three `huh` rows; the new writes are appended so the
existing readback indices do not move.  A landed 0x0020 reads the same 0x20 as a landed 0x0000 at an
armed ICR, which is why the `huh` rows exist: the readback alone would not separate `M_HI` from
`M_PENDBOTH`.  Under a count-conditioned mutant the order matters -- a landed 0x0018 decrements the count
and a landed 0x0000 or 0x0020 zeroes it, so the guard re-arms for the later writes -- and every
prediction in `PRETABLE_pass11.out` (Section 19, with the four mandated checks) derives the readbacks in
session order.  Rows with no mutant in the part-11 table are named there rather than left to be found.

## Part 11, measured (`killtable2_20260903/part11/driver.log`; predictions in `PRETABLE_pass11.out`, mtime 17:34:38; table launched 17:49:20 -- a first launch at 17:35 was REFUSED by the wrapper because the Opus seat's post-restore control was still running, which is the refusal working as designed)

| run | predicted | measured | red rows |
|---|---|---|---|
| BASE (clone of build/, rebuilt, CLEAN + FRESH) | 218/218 | **218/218** | -- |
| `M_ICLR` -- `&& !(p2 && (idata & PCC2_TTIRQ_ICLR))` at TxICR | 214/218 | **214/218** | `pend2 rbc` (0x10), `pend2 rbh` (0x10: declined after the strobe zeroed the count), `pendboth rbc` (0x10), `pendboth rbh` (0x10) |
| `M_HI` -- `&& !(p2 && (idata & 0xe0))` | 214/218 | **214/218** | `pend2 rbh` (0x20), `pend2 huh` (1), `pendboth rbh` (0x20), `pendboth huh` (1) |
| `M_P1IEN` -- `&& !(p1 && (idata & PCC2_TTIRQ_IEN))` | 206/218 | **206/218** | `pend1 rbi` (0x33), `rb2i` (0x13), `rbc` (0x10), `rbh` (0x10), `rb2c` (0x13), `rb2h` (0x13); `pendboth rbi` (0x33), `rb1i` (0x33), `rbc` (0x10), `rbh` (0x10), `rb1c` (0x10), `rb1h` (0x10) |

Frozen instrument md5 `f3cc2095` == the live probe at launch; each mutant string gcc-syntax-checked before
the table and proven by a two-line diff against SEC; the clone restored from SEC, rebuilt, cmp-clean,
sentinel cleared.  **All four predictions exact, red set and value** -- the first table in this chain
where every derivation held, and the derivations were all order-dependent: a landed 0x0018 decrements
the count and clears INT, so the write after it is declined and reads the same 0x10; a landed 0x0020
prints HUH? and zeroes the count; under `M_P1IEN` the landed 0x0013 raises T2ICR to 0x13 and the later
declined writes leave it there.  The cell the Opus seat measured open on the 203-row instrument
(`M_ICLR`, 203/203) is killed at four rows here; the previously unkilled `pend1 rbi` is killed by
`M_P1IEN`.

## Batch two -- the enumeration, not another cell

The class-closure amendment's own trigger fired: three consecutive passes found ONE class -- an unvaried
axis crossed with a varied one (190 -> 194 -> 203 -> 218) -- and the Opus seat said the next repair owes
the enumeration across the arms, deriving (not measuring) that TxCTL has two unheld cells of its own
{COVF} x {idata & ~7}.  Batch two, applied after part 11 and before the gate so the gate pins the final
probe: the contract now carries THE ENUMERATION -- per arm, the axes the body's code makes decisive (an
`if`, or an index) and what the rows hold: nine arms are stores, masks or a print with no `if` on state or
idata and are held by the plain rows; IPL has one static latch, held both ways; TxICR is passes 9 to 11;
TxCTL has the label as an RMW index, the count class, and two tested idata bits, COVF (0x04) and the
HUH? bits (`~7`), with COVF-set held at NO cell.  Its generating set: in the four overflow sessions
(count 1 and count >= 8, each timer) write 0x0004 and 0x0008 at the armed label, then preset the idle
label's CTL to 0x02 (COC without CEN -- CEN would start the idle timer) and write 0x0000 / 0x0004 /
0x0008 there; a `huh` row per session counts the TxCTL HUH? print.  Twenty-four rows -> 242.  Landed
values never equal a preset: count 1 (0x11): 0x0004 -> 0x00 (COVF clears the count and itself), 0x0008
-> 0x10 + HUH?; count >= 8 (0x81): 0x00 / 0x80 masked; idle 0x02: 0x00.  Also in the batch (Opus, pass
11): `cval()`'s value branch on a LIVE guest with a short transcript now says `short-transcript (FAILED
FOR SOME OTHER REASON)` instead of a bare `died`, and the (T1, 0, 0, IEN clear) cell is attributed to
`op t1icr dcl` (0x0303), not to `latch all`, which iterates BLOCKS12 at 0x1a and never writes T1ICR.
Predictions in `PRETABLE_pass11b.out` (Section 20, with the four mandated checks) before the table.

<<PART12_OWED>>

## Records corrected in place (L4), every one from a seat

* The #9 reversal above (grok, codex, fable5) -- contract, pass-10 block, carrier.
* The pass-10 table carried the PREDICTION's value in the measured column for one readback: `pendboth
  rb1i` under `M_P2IEN` read 0x33 in the log (T1ICR held 0x31 in that session), not the 0x13 written
  (opus5 by reading before its build; grok; fable5 confirmed from the log).  The score matched by
  coincidence.  Corrected in the pass-10 block with its provenance; the pre-table file keeps its
  misprediction, as pre-table files do.
* "The three decl rows expect 4" in the pass-10 block -- the rows want 1 (the announce is latched once
  per block on the first DECLINE), as the probe, the pre-table file and BASE all said (opus5, grok,
  codex, fable5).
* The landed-value account omitted 0x20 -- a landed 0x0000 at an armed ICR (codex).
* The carrier's JOINT CELLS paragraph said "the counts are `int`, so finite fails" -- a C `int` is
  finite; the raw value space does no bounding work (codex, glm).  And it said the measured case closed
  "eight cells in three readbacks" where the contract closed sixteen in nine (grok).
* "Predictions written at 13:14" -- the order witness is the PREDICTIONS.md mtime, 13:19:27, before the
  first mutant build at 13:24:15 (codex).
* The `pendboth arm1` note said the proof is `M_PENDBOTH` reddening "decl/rb"; on the 203-row
  instrument it reds `rb`/`rbi` and decl stays green (grok).
* The pass-10 brief's ENCLOSING CODE was empty (pass 10) and pass 11's builder ASSERTS a body -- the
  first form of that assertion stopped at the guard's own `}` and fired on the fix, which is what an
  assertion is for.
* The pass-11 packet did not flag the `M_PENDBOTH` misprediction as a finding and said "three existing
  sessions row all sixteen cells" without saying the (0, 0) cells are the plain rows (glm).  Both true
  of the block, not of the packet -- packet defects, recorded.

## Gate

<<GATE14_P12_OWED>>

## What stays open

Pass 12: the pass on this repair diff (the twelve writes, the `huh` rows, the contract's floor / held /
disclosed statement, the carrier's bound).  The chain closes on the first VALID pass that finds zero
floor breaches surviving adjudication, with the floor now bounded -- and the ask-again on the pass-10
table has been spent (this pass was it; what it found is rowed above).  Filed, not fixed: `pcc2c040kill`
(HIGH), `pcc2counter8`, `pcc2pscaleflood`, `pcc2huhflood` (the HUH? print this repair now counts is the
unlatched flood that item names), `pcc2widecompose`, `pcc2assertflood`, `pcc2iclrdec`,
`pcc2latchwidth48`, and the two rows that rest on `pcc2counter8`.

```

## THE FILED QUEUE (OUTSTANDING_BUGS.md, VERBATIM)

### `pcc2c040kill` (HIGH) -- a LEGAL byte write to GENCTL ends the host

**2026-09-03, surfaced by the `pcc2widthkills` pass-1 panel (fable5 and kimi, independently);
the panel found it while auditing the width fix and noted that "ten kills removed" would read as
"file clean" unless this one is cited.**

`dev_pcc2.c`, `reassert_interrupts()` (around `:189-195`): if GENCTL has bit `0x04` set
(C040), the function does `fatal("pcc2: C040 interrupt assertions... TODO"); exit(1);`.  GENCTL
is written by the guest through its own arm at the LEGAL width (`ld.b`/`st.b`), and that arm
calls `reassert_interrupts()` on every write.  So **a single byte store of `0x04` to
`0xfff42002` ends the host** -- no width trick, no misalignment, an ordinary register write.

It was mentioned once in prose under `widthkillclass` as "a BADVAL reachable by a byte write"
with no row id, which is the same gap `pcc2defaultkill` closed for the offset kill.  Filed now
with an id so the width round's contract can point at it.

**ROW-DESIGN TRAP for the width round, recorded here because it is where a reader looks:**
every GENCTL lane value in a width-round row must keep bit `0x04` CLEAR, or a DELETE /
fall-through mutant trips THIS kill and the row dies for a reason not under test.

Witness owed (rung 3, one session): `st.b 0x04` to `0xfff42002` on the committed build ->
`exit1`.  Not yet run; the width round's witness is the template.

### `pcc2counter8` (MED) -- the counter/compare arm accepts an 8-byte write and raw-copies through neighbours

**2026-09-03, found by the codex seat on the `pcc2widthkills` pass-1 panel.**

The `T1CMP / T2CMP / T1COUNT / T2COUNT` arm does `memcpy(d->pcctwo_reg + relative_addr, data,
len)` for any `len` within `PCC2_SIZE`.  The hardware guide lists 8/16/32-bit cycles only.  An
8-byte write at `T2COUNT (0x10)` raw-copies through `PSCALE (0x14)`, `PSCALEADJ (0x15)`,
`T2CTL (0x16)` and `T1CTL (0x17)` -- bypassing the per-register write semantics those arms
implement (masks, read-modify-write, COVF clear, `reassert_interrupts`).  A guest can set timer
control bits through a path that skips their arm.

Not a host kill; a semantic bypass.  Deliberately NOT folded into the width round -- it is a
different defect (accepts too much, rather than kills) in a different arm.  Reachability: `st.d`
to `0x10` is 8-aligned, so it is guest-reachable by construction.


*2026-09-04 (Opus seat, pcc2widthkills pass 8): the labels above were swapped (the header says 0x16 = T2CTL,
0x17 = T1CTL); corrected in place.  And the path is GUEST-reachable: 0xfff42010 is 8-aligned, so a
guest `st.d` lands raw bytes on both timer-control registers -- the width detector's `rb t*ctl b27'
rows now use exactly this path to hold TxCTL bits 2-7 set, and say so.*

### `pcc2huhflood` (MED, floodclass) -- eight unlatched, guest-drivable `fatal()` prints in the pcc2 arms, siblings of the one already filed

**Filed 2026-09-04 by the Opus seat on `pcc2widthkills` pass 8 (F14), from a census of every
print in `DEVICE_ACCESS(pcc2)`.**  `pcc2pscaleflood` filed ONE of nine: PSCALEADJ's "ignored"
print on every byte write.  The other eight are the same shape -- unlatched, reached by an
ordinary LEGAL byte write, and `fatal()` so `-q` cannot silence them: CHIPID/CHIPREV "IGNORING
write to read-only" (every write), and the `HUH?` prints at VECBASE (idata & ~0xf0), TxCTL
(& ~7), TxICR (& 0xe0), SCCICR and SCCTX (& ~0x1f), SCCRX and SCSIICR (& ~0xdf).  Seven of the
eight sit inside the twelve arms the width round rewrote.  The carrier's own rule -- grep for
the siblings before calling a claim fixed -- applies to a filing too.  The width probe itself
trips two of them (`acc all` stores 0x10 at every block, which is `& ~7` at TxCTL and `& ~0x1f`
at SCCICR/SCCTX), and its `devsig` oracle counts CHIPID's message at 1 after ONE byte write, so
latching each site per the house idiom (`(once)`, per instance) would not break the detector.
One round, one shape, nine sites; not the width round's business.

### `pcc2defaultkill` addendum (2026-09-04, Opus seat, pass 8)

`PCCTWO_SCCTXIACK` (0x25) has NO `case` in `DEVICE_ACCESS(pcc2)`, so any access to it reaches
`default:` and its `exit(1)` -- inside the filed family, named here so the census is complete.
`SCCRXIACK` (0x27) is the thirteenth arm (reads neither idata nor len; width-invariant) and runs
on READS as well as writes -- there is no writeflag test -- so a debugger-visible read clears
SCCRX's INT bit; true of upstream, not a width matter.

### `pcc2pscaleflood` (MED) -- PSCALEADJ's write-side `fatal()` is unlatched and guest-drivable

**Filed 2026-09-03 by the Opus seat on `pcc2widthkills` pass 3, while verifying something
else.**  `dev_pcc2.c`'s PSCALEADJ write arm prints `[ pcc2: write to PSCALEADJ ignored (value
0x..) ]` on EVERY byte write.  Byte accesses skip the m88k alignment check, so `st.b` to
`0xfff42015` in a loop floods the log at any verbosity -- `fatal()` has no early-out, so `-q`
cannot silence it.  The round converted IPL's and MASK's `#119` latches to per-instance and
left this one alone.  `floodclass` family; the house idiom is a per-instance latch with an
explicit `(once)` marker.  Not this diff's business; filed.

### `pcc2widecompose` (LOW) -- per-lane composition of a wide PCC2 write, the faithful upgrade to DECLINE

**Filed 2026-09-03 -- and the round's own record had said "FILED" for hours before it was.**
The codex seat on `pcc2widthkills` pass 2 found the claim in the code comment and the
CHANGELOG with no entry anywhere.  A "filed" that names no row is a wrong record.

`pcc2widthkills` shipped writes as DECLINE + latch because every write arm uses `idata`,
which is the addressed byte only at `len == 1`, and eight arms have per-register semantics
(masks, read-modify-write, clears; seven of the twelve blocks call `reassert_interrupts()`).  The faithful
alternative the pass-1 panel named is COMPOSE: decompose a wide write into `len` byte
accesses, each dispatched through its own arm with its own semantics and side effects.

**Warrant in the tree:** `mvme_pcctworeg.h` says the registers accept 8/16/32-bit cycles;
the read side already composes lanes in address order; the counter arms already accept wide
writes by memcpy.  **Warrant against, measured by a seat:** `_guest-src-openbsd22/sys/arch/
mvme88k/dev/pcctworeg.h:8` declares these registers `volatile u_char`, and the driver code
uses byte accesses -- one real OS shows NO demand for wide writes to the byte registers.

**Hazard, named by the seat that proposed it:** COMPOSE must live INSIDE the byte-register
arms.  Applied before the switch it would route bytes +1..+3 of a legal word write to a
counter register through `default:`, a NEW kill on a working path.

**Reopen condition:** a measured guest (a driver trace, a PROM disassembly) that wide-writes
one of the twelve byte registers.  Until then DECLINE is the honest model and this is the
recorded upgrade path, not a defect.

### `pcc2assertflood` (LOW, floodclass) -- the interrupt (de)assert trace prints on every tick while a pcc2 interrupt is pending

**Filed 2026-09-03 while hand-verifying the `pend2 *' row shape for `pcc2widthkills` pass 6.**
`reassert_interrupts()` in `dev_pcc2.c` prints `[ pcc2: IPL = 1, MASK = 0 => ASSERT ]` each time
it runs with an unmasked interrupt pending -- and it runs from `DEVICE_TICK(pcc2)` every 2^14
instructions plus on every qualifying register access.  A guest that arms timer 2 (compare 1,
count 0, IEN, CEN) and spins saw six of these lines in a two-second free-run at quit; a guest
that leaves an interrupt pending indefinitely floods the log for as long as it runs.  The line
is printed by `debug()` (`dev_pcc2.c`, the `=> %s` line in `reassert_interrupts()`): verbosity-gated at
default settings, so it floods under `-v` and while single-stepping, where `debug()` prints -- a
narrower exposure than a `fatal()` flood, which is why this is LOW.  `floodclass` family; the house idiom is a per-instance latch with an
explicit `(once)` marker, or printing only on a CHANGE of the asserted state (the ASSERT/DEASSERT
edge), which is what the message's own wording suggests it was meant to be.  Not the width
round's business; filed.  Witness available: the `pend2 *' session in `regress/pcc2_width_probe.py`
reaches the state on unmodified `mvme88k -e mvme187`.

### `pcc2latchwidth48` (LOW, coverage debt) -- the latch-SET decision is pinned at width 2 only

**Filed 2026-09-03 from `pcc2widthkills` pass 6 (codex, from the pass-5 record).**  `rb2 *' proves
that a wide write arriving with the block's latch already SET is still refused, but only at
`len == 2` (`st.h` / `put h`).  The qualified-guard shape `&& !(d->warned & bit)' is
width-agnostic, so the len-2 rows kill it and its 4- and 8-byte repeats are coverage debt rather
than a floor cell -- a guard that consulted the latch only for len 4 or 8 (`&& !(len > 2 &&
(d->warned & bit))') would escape.  Eighteen sessions if closed at every storing block; a
plausible future edit is doubtful, so filed below the live defects in the same file
(`pcc2c040kill`, `pcc2counter8`, `pcc2pscaleflood`).  The contract in the probe discloses it.

### `pcc2iclrdec` (LOW, coverage debt) -- the TxICR interrupt-clear decrement is exercised by no row in the tree

**Filed 2026-09-04 by the kimi-k3:cloud substitute seat on `pcc2widthkills` pass 7 (packet-fed,
reasoning from the inlined TxICR arm).**  The arm's clear branch, `if (ICLR && (reg & INT) &&
pending_timer2_interrupts > 0) pending_timer2_interrupts--;` (and the timer-1 twin), runs only for
a BYTE write carrying ICLR while an interrupt is pending -- and the width detector's `pend* *`
rows hold that state only at WIDE writes, which the guard declines before the body runs.  So `>
0` -> `>= 0`, or `--` -> `++`, inside either branch is unobserved by every row in the tree: the
count goes to -1 (or 2) while INT is cleared, and nothing reads it afterwards.  Outside the width
round's clause-(d) closure (the branch does not dominate the diff's edited lines; it is
pre-existing body logic), so filed rather than repaired there.  A row is cheap now that the
free-running shape exists: arm timer 2, poll to INT, `st.b` ICLR|IEN|IL1 (0x19) to T2ICR, then
observe that a second poll never sees INT again (pending consumed) -- and its twin with a
SECOND fired interrupt to distinguish `--` from `= 0`.  Belongs to a timer-semantics round, not
to this one.

## DISCLOSURE -- `git diff --numstat` for the working set

```
1273	0	CHANGELOG.md
132	1	OUTSTANDING_BUGS.md
4	4	regress/gate_arm.sh
1051	16	regress/pcc2_width_probe.py
20	6	regress/sgi_de_primop_probe.py
32	12	src/devices/dev_pcc2.c
86	0	tools/CLAUDE.md
3	1	tools/panel.sh
1366	106	tools/pipeline/ledger.json
5	5	tools/pipeline/matrix.html

```
