# `lcabadval` RESEARCH STAGE -- the six missing seats, by OWNER DECISION 2026-09-18 (a LATE research stage of a SHIPPED round)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
The code under review is `GXEMUL-SEC/src/devices/dev_lca.c` **AS COMMITTED AT HEAD** (the working copy carries another
round's uncommitted edits -- read `git show HEAD:src/devices/dev_lca.c`, not the file on disk).  Ignore any other `src/`.
Everything needed is inlined.  **VERDICT LINE FIRST** (RIGHT / RIGHT-WITH-GAPS / WRONG).  Check the premises.

## THE ROW AND WHAT SHIPPED
"dev_lca.c: SIX chipset registers in DEVICE_ACCESS(lca_ioc) kill the host on a value outside a small accepted set (CONF,
TB_ENA, W_BASE0/1, W_MASK0/1)."  The research stage ran with opus5, fable5 and codex.  The round shipped as `a616d20`
(#518): it WIDENED the whitelists to the values the Alpha 21066/21066A manual makes legal, rather than only changing what
happens on a bad value -- fable5's 2026-09-09 ruling that "the guards are WRONG, not harsh" (manual Table 6-6 lists
THIRTEEN legal W_MASK values where the fork accepted one; S6.4.14 REQUIRES SROM to write ZERO to W_BASE1).

## THE RESEARCH QUESTIONS THE STAGE WAS HELD ON (premises -- check them)
P1. The interrupt stubs `lca_interrupt_assert` / `lca_interrupt_deassert` are bare `fatal()+exit(1)` with the ISA PIC chain
    wired to them, so ANY interrupt ends the host with the same status as a value guard -- a CONFOUND: a probe must match
    each arm's fatal() TEXT, not the exit status.  Is that confound real at HEAD, and is text matching sound?
P2. The accept-row set is SIX (one per value-guarded arm: CONF, TB_ENA, W_BASE0, W_BASE1, W_MASK0, W_MASK1), not four.
P3. Member 5 of the option set (FAULT: deliver a bus error) is UNAVAILABLE on Alpha -- memory_rw.c delivers exceptions on a
    failed device access for MIPS and M88K only -- so widening (accept) or decline were the only honest members.
P4. The IOC_CONF arm's diagnostic could PRINT THE WRONG VALUE (row `lcaconfwidth`), which would corrupt a text oracle there.

## THE SHIPPED dev_lca.c CHANGE (git show --format= a616d20 -- src/devices/dev_lca.c)
```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index de9aa64..6873466 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -52,6 +52,12 @@
     `interrupt->extra' -- see the comment on lca_interrupt_assert().  */
 #define	LCA_W_IRQ_ASSERT	0	/*  #516  */
 #define	LCA_W_IRQ_DEASSERT	1	/*  #516  */
+#define	LCA_W_IOC_CONF_CFG1	2	/*  #518: IOC_CONF<1> set -- CFG AD<1:0> = 10/11, not a cycle type  */
+#define	LCA_W_IOC_WMASK0	3	/*  #518: unsupported W_MASK0 encoding declined  */
+#define	LCA_W_IOC_WMASK1	4	/*  #518: unsupported W_MASK1 encoding declined  */
+#define	LCA_W_IOC_WEN		5	/*  #518: a DMA window enabled -- translation not modelled  */
+#define	LCA_W_IOC_DEF_W	6	/*  #518: default-arm write declined  */
+#define	LCA_W_IOC_DEF_R	7	/*  #518: default-arm read answered with zero  */
 
 struct lca_data {
 	struct pci_data		*pci_data;
@@ -296,6 +302,27 @@ DEVICE_ACCESS(lca_isa)
 }
 
 
+/*
+ *  #518 (lcabadval): one bounded announce per (device instance, reason).  Six
+ *  IOC write arms used to end the host with fatal()+exit(1) on any value outside
+ *  a tiny accepted set -- and the sets were WRONG, not merely harsh: the 21066
+ *  HRM (Table 6-6) lists THIRTEEN legal W_MASK encodings where the model took
+ *  one, and S6.4.14 REQUIRES SROM to write ZERO to W_BASE1, which was fatal.
+ *  The arms below store the ARCHITECTED FIELDS, ignore reserved bits (type X),
+ *  validate W_MASK by its field rule, and decline what the model cannot honour
+ *  with this announce -- fatal() prints and returns (it cannot be silenced by
+ *  -q, which is why a latch and not a verbosity flag).
+ */
+static void lca_ioc_announce(struct lca_data *d, int bit, const char *what,
+	uint64_t v)
+{
+	if (d->warned & (1u << bit))
+		return;
+	d->warned |= 1u << bit;
+	fatal("[ lca_ioc: %s: 0x%" PRIx64 "  (once) ]\n", what, v);
+}
+
+
 DEVICE_ACCESS(lca_ioc)
 {
 	uint64_t idata = 0, odata = 0;
@@ -314,23 +341,21 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->ioc_conf;
 		} else {
-			d->ioc_conf = idata;
-			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
-			    bus non-0 selection bit.  */
-			if (idata & ~1) {
-				/*  #506: was `0x%x', (int)idata -- a 64-bit guarded value
-				    narrowed to 32 in the KILL diagnostic, so a write of
-				    0x100000000 trips `idata & ~1' and then reports "0x0",
-				    which is a value this same guard ACCEPTS.  The five
-				    sibling arms below already print the full width this
-				    way; this arm was the outlier among the VALUE-guard
-				    diagnostics.  (Not the file's only narrowing site --
-				    the default arm below has the same cast, and this
-				    round fixes it too.)  */
-				fatal("TODO: Write to unimplemented bit of"
-				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
-				exit(1);
-			}
+			/*  #518: was `if (idata & ~1) { fatal(); exit(1); }' with the
+			    store BEFORE the check (#506 had widened its diagnostic).
+			    HRM S6.2.9: IOC_CONF<1:0> is the CFG AD<1:0> field, and
+			    bit 0 selects the configuration cycle TYPE; everything
+			    above is reserved and is IGNORED, not fatal.  Bit 0
+			    selects type-1 cycles and is what lca_pci_conf
+			    reads (#515); bit 1 selects the CFG AD<1:0> encodings 10/11,
+			    which are not configuration-cycle types -- stored and
+			    announced once, not modelled.  (Pass 2: this comment first
+			    called bit 1 the type-1 select; grok read lca_pci_conf.)  */
+			d->ioc_conf = idata & 0x3ULL;
+			if (idata & 0x2ULL)
+				lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1, "IOC_CONF<1> set"
+				    " (CFG AD<1:0> = 10/11, not a configuration-cycle type):"
+				    " stored, not modelled", idata);
 		}
 		break;
 
@@ -343,14 +368,10 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->tlb_enable;
 		} else {
-			d->tlb_enable = idata;
-			/*  TODO: Actually implement this.  */
-			if (idata & ~IOC_TB_ENA_TEN) {
-				fatal("TODO: LCA_IOC_TB_ENA value "
-				    " (0x%" PRIx64") has unimplemented "
-				    "bits.\n", (uint64_t)idata);
-				exit(1);
-			}
+			/*  #518: TEN is the only architected bit (HRM Table 6-13);
+			    the rest are type X -- IGNORED on write, never fatal.  The
+			    old arm stored the whole value and then died on it.  */
+			d->tlb_enable = idata & IOC_TB_ENA_TEN;
 		}
 		break;
 
@@ -358,14 +379,16 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->window_base_0;
 		} else {
-			d->window_base_0 = idata;
-			/*  TODO: Actually implement this.  */
-			if (idata != 0ULL && idata != 0x300800000ULL) {
-				fatal("TODO: LCA_IOC_W_BASE0 value differs"
-				    " (0x%" PRIx64") from the only implemented"
-				    " values\n", (uint64_t)idata);
-				exit(1);
-			}
+			/*  #518: was a two-value whitelist + exit(1).  The HRM defines
+			    this register by FIELDS -- W_BASE<31:20>, SG<32>, WEN<33> --
+			    not by a list of numbers, and S6.4.14 REQUIRES SROM to write
+			    zero here.  Store the fields (reserved bits dropped); the
+			    window is not translated by this model, which is announced
+			    once when any window is ENABLED.  */
+			d->window_base_0 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);
+			if (idata & IOC_W_BASE_WEN)
+				lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"
+				    " enabled; window translation is not modelled", idata);
 		}
 		break;
 
@@ -373,13 +396,19 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->window_mask_0;
 		} else {
-			d->window_mask_0 = idata;
-			/*  TODO: Actually implement this.  */
-			if (idata != 0x700000ULL) {
-				fatal("TODO: LCA_IOC_W_MASK0 value differs"
-				    " (0x%" PRIx64") from the only implemented"
-				    " value\n", (uint64_t)idata);
-				exit(1);
+			/*  #518: was `!= 0x700000ULL' + exit(1): ONE accepted value where
+			    HRM Table 6-6 lists THIRTEEN (W_MASK<31:20> = 0, 1, 3, 7, ...
+			    0xfff: a contiguous low-ones field), and the old arm STORED
+			    before it checked.  Validate the field, store only when it is
+			    legal, decline once otherwise with the previous value kept.  */
+			{
+				uint64_t v = idata & 0xfff00000ULL, f = v >> 20;
+				if ((f & (f + 1)) == 0)
+					d->window_mask_0 = v;
+				else
+					lca_ioc_announce(d, LCA_W_IOC_WMASK0, "unsupported"
+					    " IOC_W_MASK0 encoding declined (HRM Table 6-6);"
+					    " previous value kept", idata);
 			}
 		}
 		break;
@@ -397,14 +426,13 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->window_base_1;
 		} else {
-			d->window_base_1 = idata;
-			/*  TODO: Actually implement this.  */
-			if (idata != 0x240000000ULL) {
-				fatal("TODO: LCA_IOC_W_BASE1 value differs"
-				    " (0x%" PRIx64") from the only implemented"
-				    " value\n", (uint64_t)idata);
-				exit(1);
-			}
+			/*  #518: was a ONE-value whitelist + exit(1) -- and the one value
+			    was not zero, which S6.4.14 item 3 requires SROM to write.
+			    Same disposition as W_BASE0 above.  */
+			d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);
+			if (idata & IOC_W_BASE_WEN)
+				lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"
+				    " enabled; window translation is not modelled", idata);
 		}
 		break;
 
@@ -412,13 +440,19 @@ DEVICE_ACCESS(lca_ioc)
 		if (writeflag == MEM_READ) {
 			odata = d->window_mask_1;
 		} else {
-			d->window_mask_1 = idata;
-			/*  TODO: Actually implement this.  */
-			if (idata != 0x3ff00000ULL) {
-				fatal("TODO: LCA_IOC_W_MASK1 value differs"
-				    " (0x%" PRIx64") from the only implemented"
-				    " value\n", (uint64_t)idata);
-				exit(1);
+			/*  #518: was `!= 0x3ff00000ULL' + exit(1): ONE accepted value where
+			    HRM Table 6-6 lists THIRTEEN (W_MASK<31:20> = 0, 1, 3, 7, ...
+			    0xfff: a contiguous low-ones field), and the old arm STORED
+			    before it checked.  Validate the field, store only when it is
+			    legal, decline once otherwise with the previous value kept.  */
+			{
+				uint64_t v = idata & 0xfff00000ULL, f = v >> 20;
+				if ((f & (f + 1)) == 0)
+					d->window_mask_1 = v;
+				else
+					lca_ioc_announce(d, LCA_W_IOC_WMASK1, "unsupported"
+					    " IOC_W_MASK1 encoding declined (HRM Table 6-6);"
+					    " previous value kept", idata);
 			}
 		}
 		break;
@@ -432,13 +466,35 @@ DEVICE_ACCESS(lca_ioc)
 		}
 		break;
 
-	default:fatal("[ lca_ioc: unimplemented %s to offset 0x%x",
-		    writeflag == MEM_WRITE? "write" : "read", (int)
-		    relative_addr);
-		if (writeflag == MEM_WRITE)
-			fatal(": 0x%" PRIx64, (uint64_t)idata);	/*  #506  */
-		fatal(" ]\n");
-		exit(1);
+	default:
+		/*  #518: was fatal()+exit(1) for ANY offset the switch does not
+		    list.  Decline the write (no IOC register changes; only the announce
+		    latch moves), answer a read with
+		    zero (odata is already 0), announce each direction once.  The
+		    value keeps #506's full width.  NOT all of these offsets are
+		    unimplemented HOLES: STAT0 (+0x040), STAT1 (+0x060), SFT_RST
+		    (+0x0c0) and PAR_DIS (+0x0e0) are DOCUMENTED registers this
+		    model has never had, and S6.4.14 items 1-2 require SROM to
+		    write SFT_RST and STAT0 -- those now survive as declined writes
+		    instead of ending the process, and are filed (lcaiocstat0) for
+		    an implementation, which this decline is not.  (grok, pass 2)  */
+		{
+			int bit = writeflag == MEM_WRITE ?
+			    LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_R;
+			if (!(d->warned & (1u << bit))) {
+				d->warned |= 1u << bit;
+				fatal("[ lca_ioc: unimplemented %s to offset 0x%x",
+				    writeflag == MEM_WRITE? "write" : "read", (int)
+				    relative_addr);
+				if (writeflag == MEM_WRITE)
+					fatal(": 0x%" PRIx64 " -- declined",
+					    (uint64_t)idata);	/*  #506  */
+				else
+					fatal(" -- answered with zero");
+				fatal("  (once per direction) ]\n");
+			}
+		}
+		break;
 	}
 
 	if (writeflag == MEM_READ)
```

## lca_interrupt_assert / lca_interrupt_deassert AT HEAD
```c
void lca_interrupt_assert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: this was `fatal(); exit(1)' with NO GUARD -- not a refused value,
	    an unimplemented path -- and DEVINIT below installs it as the ISA
	    interrupt callback that `bus_isa_init' wires to BUS_ISA_IDE0|IDE1.  So an
	    ordinary ISA interrupt ended the host, needing no unusual value anywhere.
	    MEASURED on two independent guest paths: one store to the 8042 command
	    port (regress/lca_irqstub_probe.py, 3/4) and three byte stores to the
	    ns16550 on IRQ 4 (regress/lca_irqstub_uart_probe.py, 2/4).

	    *** THE STUB IS NOT REPLACED BY A FORWARD, BECAUSE A FORWARD WOULD BE A
	    NO-OP.  ALPHA HAS NO INTERRUPT DELIVERY AT ALL. ***  `cd.alpha.irq_asserted'
	    is written by `cpu_alpha.c' and read NOWHERE.  `cpu_dyntrans.c' turns a
	    pending interrupt into a delivered one for FIVE architectures -- ARM and
	    M88K and PPC through their own `irq_asserted', MIPS through the COP0
	    exception model, and SH through `int_to_assert' -- and ALPHA IS ABSENT
	    FROM THAT LIST.  (An earlier draft of this comment said "ARM, M88K and
	    PPC only": that enumeration was made by grepping for `irq_asserted', which
	    is a CORRELATE of delivering rather than the property, and it missed the
	    two architectures that deliver by another mechanism.  The Alpha conclusion
	    is unchanged and is strengthened -- it is the outlier among five, not
	    three.)  Calling `cpu_interrupt()' here would set
	    a field nothing consumes.  Implementing delivery is a SUBSYSTEM -- the
	    dyntrans dispatch, the PALcode entry and the IPL check -- and is its own
	    round, not this one.

	    So the disposition is DECLINE plus a bounded announce, and what it buys is
	    stated narrowly on purpose: THE HOST STOPS DYING.  Interrupts do not start
	    working; they were never delivered on this architecture and still are not.

	    The latch is PER-INSTANCE (`interrupt->extra'), not function-static: a
	    function-static bit would let one guest access to one device instance
	    silence the diagnostic for every other instance, which is a class already
	    filed against this tree.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_ASSERT;
		fatal("[ lca: ISA interrupt assert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}
void lca_interrupt_deassert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: the sibling of lca_interrupt_assert() above, same reasoning.  A
	    SEPARATE latch bit, so the two are distinguishable: a driver normally
	    reaches both within one interrupt cycle, and one shared bit would report
	    whichever arrived first and hide the other entirely.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_DEASSERT;
		fatal("[ lca: ISA interrupt deassert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}
```

## QUESTIONS
Q1. P1-P4: confirm or refute from the code.
Q2. Is widening the whitelists (ACCEPT per the manual) the right disposition for every one of the six arms, or does any
    arm still need a decline for values the manual forbids?  What does the shipped fix do for an ILLEGAL value today?
Q3. What is still owed -- the interrupt stubs (member 7, IMPLEMENT), the default: arm's exit, anything else?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
