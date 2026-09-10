# `#518` lcabadval — PASS 2 ON THE REAL DIFF: six value-guarded IOC register arms that ended the emulator process on values the LCA manual makes legal

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like

## §C0 — HAS THIS ROUND SHIPPED?  NO.
HEAD is `e73623a`.  The diff below is the UNCOMMITTED working set of `GXEMUL-SEC/src/devices/dev_lca.c`
(`git diff -- src/devices/dev_lca.c`, 9 hunks) plus a NEW file `regress/lca_badval_probe.py` (untracked;
its detector block is inlined below and the whole file is on disk for seats that can read).  This is
ordinary value-acceptance correctness work on a chipset register model.  Use plain engineering language.

## §C — SETTLED PREMISES, RE-INLINED (check them; say which you cannot settle from this packet)
S1. THE DEFECT.  `DEVICE_ACCESS(lca_ioc)` had six write arms of the shape `d->x = idata; if (idata !=
    K) { fatal(...); exit(1); }` -- the value STORED, then the process ended.  Accepted sets, enumerated
    from the predicates: IOC_CONF {0,1}; IOC_TB_ENA {0,0x80}; W_BASE0 {0,0x300800000}; W_MASK0
    {0x700000}; W_BASE1 {0x240000000}; W_MASK1 {0x3ff00000}.  Plus a `default:` arm that ended the
    process on ANY unlisted offset, both directions.
S2. THE MANUAL (Alpha 21066/21066A HRM, local: `_scratchpad/21066_66a_hrm.txt`; every line read, not
    taken from a seat): Table 6-6 (:9586-9598) lists THIRTEEN legal W_MASK<31:20> encodings, the
    contiguous low-ones values 0x000..0xfff; S6.4.14 item 3 (:10791-10792) REQUIRES SROM to write ZERO
    to W_BASE0 and W_BASE1; Table 6-13 (:10443,:10453) makes TB_ENA bits other than TEN (0x80) RES
    type X, and the type legend (:985-988) says X bits are IGNORED ON WRITE; Table 6-10 (:10246-10254)
    makes IOC_CONF<1:0> a two-bit FIELD (all four encodings legal); Figure 6-9 (:10556-10560) gives
    W_BASE = <31:20> base, <32> SG, <33> WEN, agreeing with `alpha_lcareg.h`.  S6.4 (:10175): quadword
    access only.  So the guards were WRONG, not merely harsh (flagship ruling 2026-09-09).
S3. WITNESS (rung 3, `regress/lca_badval_probe.py`, unmodified `-E alpha -e alphabook1`, build/gxemul):
    on HEAD 74daefd the six `<arm> legal` rows are RED -- 14/20, each death carrying its own arm's
    diagnostic, the no-guard sibling W_T_BASE0 surviving the same value (HEAD_74daefd.out); on the fix,
    20/20 with the same script; the 20 detector rows added below score 40/40 on the fix
    (FIX518_detector_run1.out).  The #516 interrupt stubs no longer confound attribution.
S4. DESIGN (pass-1 panels 2026-09-06..08, fix design by the codex seat, flagship ruling 2026-09-09):
    WIDEN THE WHITELISTS to the manual's fields: store `IOC_CONF & 0x3`, `TB_ENA & TEN`, `W_BASE &
    (base|SG|WEN)`; validate W_MASK by `field = (idata & 0xfff00000) >> 20; (field & (field+1)) == 0`
    and store ONLY when valid, otherwise decline once keeping the previous value; the default arm
    declines writes and answers reads with zero, once per direction.  Member 3 (decline + bounded,
    latched announce); the latch is `d->warned` with six new bits; `fatal()` prints and RETURNS
    (`src/core/debugmsg.c`, no early-out, no exit), which is why a latch and not a verbosity flag.
S5. OUT OF SCOPE, deliberately: the `ofs > len` exit in `lca_isa` (row `lcaisalane`); W_T_BASE0/1
    (unchanged, no guard); the SG bit's effect (nothing consumes it); window TRANSLATION (announced
    once as not modelled when a window is enabled).
S6. The pre-table check is written and its mutant enumeration is inlined at the end
    (`regress/artifacts/lcabadval/killtable_20260910/PRETABLE.out`, mtime before any table).

## THE DIFF (src/devices/dev_lca.c, verbatim)
```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index de9aa64..57d61a8 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -52,6 +52,12 @@
     `interrupt->extra' -- see the comment on lca_interrupt_assert().  */
 #define	LCA_W_IRQ_ASSERT	0	/*  #516  */
 #define	LCA_W_IRQ_DEASSERT	1	/*  #516  */
+#define	LCA_W_IOC_CONF_CFG1	2	/*  #518: IOC_CONF<1> set -- type-1 cycles not modelled  */
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
@@ -314,23 +341,16 @@ DEVICE_ACCESS(lca_ioc)
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
+			    HRM S6.2.9: IOC_CONF<1:0> select the configuration cycle
+			    TYPE; everything above is reserved and is IGNORED, not
+			    fatal.  Bit 0 is what lca_pci_conf reads; bit 1 (type-1
+			    cycles) is stored and announced once, not modelled.  */
+			d->ioc_conf = idata & 0x3ULL;
+			if (idata & 0x2ULL)
+				lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1, "IOC_CONF<1> set"
+				    " (type-1 configuration cycles): stored, not modelled", idata);
 		}
 		break;
 
@@ -343,14 +363,10 @@ DEVICE_ACCESS(lca_ioc)
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
 
@@ -358,14 +374,16 @@ DEVICE_ACCESS(lca_ioc)
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
 
@@ -373,13 +391,19 @@ DEVICE_ACCESS(lca_ioc)
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
@@ -397,14 +421,13 @@ DEVICE_ACCESS(lca_ioc)
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
 
@@ -412,13 +435,19 @@ DEVICE_ACCESS(lca_ioc)
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
@@ -432,13 +461,28 @@ DEVICE_ACCESS(lca_ioc)
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
+		/*  #518: was fatal()+exit(1) for ANY unlisted offset.  Decline
+		    the write (no state changes), answer a read with zero (odata
+		    is already 0), announce each direction once.  The value keeps
+		    #506's full width.  */
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

## THE DETECTOR BLOCK ADDED TO regress/lca_badval_probe.py (verbatim; the 20 witness rows above it are unchanged)
```python
# ================================================================ #518 DETECTOR ROWS
#  The rows above are the WITNESS (RED on HEAD 74daefd at 14/20, GREEN on the fix with the same
#  script).  The rows below DEFEND the fix -- they are what a kill table is scored against -- and
#  each names the mutant it kills and the observable that differs (the CHANNEL line).
#
#  CONTRACT (clause (e)).  Designed to catch, per arm: (b) the verbatim kill reinstated (the
#  `stored' rows die); (d) the STORE MASK narrowed (CONF `& 0x3' -> `& 0x1' loses bit 1; TB_ENA
#  storing the raw value keeps 0x81; W_BASE dropping WEN/SG or truncating to 32 bits; W_MASK
#  `& 0xfff00000' widened or narrowed); (d) the W_MASK FIELD RULE weakened (`f != 0' accepts
#  0x500000; `f == 1' declines 0xfff00000) or the old STORE-BEFORE-CHECK order reinstated (the
#  declined value is kept instead of the previous one); (d) the latch bits COLLAPSED (the second
#  register's, or the second direction's, announce never prints) or the latch REMOVED (a second
#  identical write announces twice); (d) the default arm declining reads to nonzero or writing
#  state.  NOT rowed, disclosed: the SG bit's effect (nothing consumes it), the W_T_BASE arms
#  (unchanged, and the negative control already pins one), the reserved bits ABOVE bit 33 of
#  W_BASE (dropped by the same mask as the ones below it -- one row per mask, not per bit), and
#  the `ofs > len' exit in lca_isa, which belongs to lcaisalane.  Every value here is QUADWORD.
#
#  Session shape: T0 = SCRATCH base (live throughout), T1 = address, T2 = value, T3 = read-back;
#  each phase reloads T1/T2 from a `put d' slot, so eight registers are never a constraint.  A
#  phase is stepped as a block and its read-back printed while the host is certainly alive.

def seq(consts, phases, settle=1.6, spin=2.2):
    """consts: list of 64-bit values -> SCRATCH slots 0,8,16,...  phases: list of lists of
    (op, addr_slot, val_slot) with op in {'st', 'ld'}; each phase ends with `print t3'.
    Returns (txt, alive, [read-backs in phase order as strings])."""
    setup = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ph in phases:
        ops = []
        for op, a, v in ph:
            ops.append(LDQ(T1, 8 * a, T0))
            if op == "st":
                ops.append(LDQ(T2, 8 * v, T0))
                ops.append(STQ(T2, 0, T1))
            else:
                ops.append(LDQ(T3, 0, T1))
        prog += ops
        lens.append(len(ops))
    cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for n in lens[1:]:
        cmds += ["step %d" % n, "print t3"]
    txt, alive = session(cmds, settle, spin)
    vals = ["0x%x" % int(m, 16) for m in
            re.findall(r"print\s+t3\s*\n\s*(0x[0-9a-f]+)", txt)]
    return txt, alive, vals

def nth(vals, i):
    return vals[i] if i < len(vals) else "absent"

def announces(txt, needle):
    return txt.count(needle)

#  ---- D1: the STORED value per arm -- accepted, then manual-legal, then read back -------------
#  KILLS: (b) reinstated kill (dies); (d) mask narrowed / raw store / declined-not-stored (reads
#  the accepted value or the raw one).  The want is the NORMALIZED legal value: for TB_ENA 0x81
#  reads back 0x80, which is the reserved-bit rule in one row.
NORMAL = {"conf": 0x2, "tbena": 0x80, "wbase0": 0x280000000, "wmask0": 0x100000,
          "wbase1": 0x0, "wmask1": 0xfff00000}
for label, addr, accepted, legal, sig, why in ARMS:
    txt, alive, vals = seq([k0(addr), accepted, legal],
                           [[("st", 0, 1)], [("st", 0, 2), ("ld", 0, 0)]])
    row("%s stored" % label, nth(vals, 1) if alive else "dead", "0x%x" % NORMAL[label],
        "accepted then legal: reads back the NORMALIZED legal value (fields kept, RES dropped)")
    evidence(txt)

#  ---- D2: unsupported W_MASK encodings are DECLINED, the previous value KEPT, once per register --
#  KILLS: field rule weakened to `f != 0' (0x500000 stored); store-before-check reinstated (reads
#  0x500000); latch removed (two announces); MASK0/MASK1 latch bits collapsed (MASK1 never
#  announces after MASK0 did, in the SAME session).
DECL0, DECL1 = "IOC_W_MASK0 encoding declined", "IOC_W_MASK1 encoding declined"
txt, alive, vals = seq([k0(IOC_W_MASK0), 0x100000, 0x500000, 0x900000,
                        k0(IOC_W_MASK1), 0xfff00000],
                       [[("st", 0, 1), ("st", 0, 2), ("ld", 0, 0)],      # phase 0: legal, bad, read
                        [("st", 0, 3), ("ld", 0, 0)],                     # phase 1: second bad, read
                        [("st", 4, 5), ("st", 4, 2), ("ld", 4, 4)]])      # phase 2: MASK1 legal, bad, read
row("wmask0 declined", nth(vals, 0) if alive else "dead", "0x100000",
    "0x500000 (field 101b) declined: previous legal value KEPT, host alive")
row("wmask0 once", announces(txt, DECL0) if alive else "dead", 1,
    "TWO unsupported writes announce EXACTLY ONCE -- the (once) latch")
row("wmask0 kept2", nth(vals, 1) if alive else "dead", "0x100000",
    "the second unsupported write also leaves the previous value")
row("wmask1 declined", nth(vals, 2) if alive else "dead", "0xfff00000",
    "MASK1: 0x500000 declined after 0xfff00000 stored")
row("wmask1 indep", announces(txt, DECL1) if alive else "dead", 1,
    "MASK1 still announces after MASK0 did -- independent latch bits")
evidence(txt)

#  ---- D3: IOC_CONF reserved bits dropped, bit 1 kept and announced once ----------------------
#  KILLS: mask narrowed to bit 0 (reads 0x0 or 0x1); raw store (reads 0x100000002); latch removed.
CFG1 = "IOC_CONF<1> set"
txt, alive, vals = seq([k0(IOC_CONF), 0x1, 0x100000002, 0x2],
                       [[("st", 0, 1), ("st", 0, 2), ("ld", 0, 0)],
                        [("st", 0, 3), ("ld", 0, 0)]])
row("conf reserved", nth(vals, 0) if alive else "dead", "0x2",
    "0x100000002: reserved bit 32 DROPPED, CFG<1> kept")
row("conf once", announces(txt, CFG1) if alive else "dead", 1,
    "two writes with CFG<1> set announce EXACTLY ONCE")
evidence(txt)

#  ---- D4: enabling a window announces ONCE across both registers; BASE0 accepts SROM's zero ---
#  KILLS: WEN latch removed (two announces); per-register WEN latches (also two); BASE0 zero
#  refused.  0x240000000 has bit 33 (WEN) set, so the accepted W_BASE1 value enables a window.
WEN = "a DMA window was enabled"
txt, alive, vals = seq([k0(IOC_W_BASE0), 0x280000000, k0(IOC_W_BASE1), 0x240000000, 0x0],
                       [[("st", 0, 1), ("st", 2, 3), ("ld", 2, 2)],
                        [("st", 0, 4), ("ld", 0, 0)]])
row("wen once", announces(txt, WEN) if alive else "dead", 1,
    "BASE0 then BASE1 both with WEN: the not-modelled announce prints ONCE")
row("wbase1 wen", nth(vals, 0) if alive else "dead", "0x240000000",
    "BASE1's accepted value round-trips with WEN (bit 33) intact")
row("wbase0 zero", nth(vals, 1) if alive else "dead", "0x0",
    "SROM's required zero lands at BASE0 too (S6.4.14 item 3)")
evidence(txt)

#  ---- D5: the default arm -- write declined, read answers zero, each direction latched -------
#  KILLS: reinstated kill; a default arm that stores or returns nonzero; the two direction
#  latches collapsed (the read never announces after the write did); latch removed (two writes
#  announce twice).  +0x1e0 is inside DEVINIT's window and names no register in alpha_lcareg.h.
UNL = LCA_IOC_BASE + 0x1e0
DEFW, DEFR = "unimplemented write to offset 0x1e0", "unimplemented read to offset 0x1e0"
txt, alive, vals = seq([k0(UNL), 0x5a5a5a5a],
                       [[("st", 0, 1), ("st", 0, 1)],
                        [("ld", 0, 0)]])
row("def alive", "alive" if alive else "dead", "alive",
    "two writes to an unlisted IOC offset survive")
row("def w once", announces(txt, DEFW) if alive else "dead", 1,
    "the declined write announces EXACTLY ONCE for two writes")
row("def read0", nth(vals, 0) if alive else "dead", "0x0",
    "a read of the unlisted offset answers ZERO, not the written value")
row("def r once", announces(txt, DEFR) if alive else "dead", 1,
    "the read direction announces on its OWN latch bit after the write did")
evidence(txt)

```

## THE PRE-TABLE CHECK (verbatim)
```
#518 lcabadval -- PRE-TABLE CHECK, written 2026-09-10 ~00:1x BEFORE table 1 runs (mtime is the proof).
Instrument: regress/lca_badval_probe.py, 40 rows (20 witness + 20 detector), 40/40 on the fixed
build/gxemul (FIX518_detector_run1.out); 14/20 on HEAD 74daefd with the 20-row witness form
(HEAD_74daefd.out).  Diff under review: src/devices/dev_lca.c (scratchpad/patch_lcabadval.py, 166
changed lines), lca_ioc_announce() helper + six arms + the default arm + six latch bits.

1. SIBLING PARITY
   The six de-fatalised arms sit in one switch beside FOUR untouched siblings: BASE (ignored),
   TBIA (ignored), W_T_BASE0, W_T_BASE1 (store + echo, no guard).  Channels per de-fatalised arm:
   survival, read-back of the normalized value, announce text, announce count.  The siblings
   have: survival + read-back (W_T_BASE0 is the negative control, `ctl noguard'/`ctl echo').
   ASYMMETRY 1: the six arms now DROP reserved bits; the W_T_BASE arms store raw.  Deliberate --
   the manual's T_BASE layout was not audited this round; SENTENCE OWED (in the probe contract),
   no row.
   ASYMMETRY 2: W_BASE0/1 share ONE WEN latch (`wen once' rows it); W_MASK0/1 have SEPARATE
   latches (`wmask1 indep' rows it).  Both directions of the default arm have separate latches
   (`def r once' rows it).  Each asymmetry has a row.
   ASYMMETRY 3: CONF announces on bit 1; TB_ENA announces on nothing (reserved bits silently
   dropped).  A TB_ENA announce would be per the manual's "ignored on write" -- nothing to
   announce.  SENTENCE, no row.

2. CLAIM -> ROW (every added comment sentence asserting an observable consequence)
   "IOC_CONF<1:0> select the cycle TYPE; everything above is reserved and is IGNORED"  -> conf reserved
   "bit 1 is stored and announced once"                                                -> conf stored, conf once
   "TEN is the only architected bit; the rest are type X -- IGNORED on write"          -> tbena stored (0x81 -> 0x80)
   "Store the fields (reserved bits dropped)" (W_BASE)                                 -> wbase0 stored, wbase1 wen
   "announced once when any window is ENABLED"                                          -> wen once
   "S6.4.14 REQUIRES SROM to write zero"                                                -> wbase1 legal/stored, wbase0 zero
   "Validate the field, store only when legal, decline once, previous value kept"       -> wmask{0,1} declined/once/kept2/indep
   "Decline the write (no state changes), answer a read with zero, announce each
    direction once"                                                                     -> def alive, def w once, def read0, def r once
   "The value keeps #506's full width" (default-arm diagnostic)                        -> no row: a diagnostic FORMAT claim;
                                                                                          checked by reading the EVIDENCE line
                                                                                          (0x5a5a5a5a printed in full).  SENTENCE.
   "fatal() prints and returns" (helper comment)                                       -> every `stored' row is alive after an
                                                                                          announce: rowed by construction.

3. GUARD FIELD vs BODY FIELD
   Guards read: idata (all arms), the field f (masks).  Bodies read/write: d->ioc_conf,
   d->tlb_enable, d->window_base_{0,1}, d->window_mask_{0,1}, d->warned.  The shared field is
   d->warned: now EIGHT bits, six of them set inside DEVICE_ACCESS(lca_ioc) by ordinary guest
   writes.  "Who else writes this field, and can they set my bit?" -- #516's two IRQ bits are set
   by the interrupt stubs; the six new bits by this handler; no site writes the whole word.  A
   collision (two reasons on one bit) is what the `indep' rows and `def r once' pin.  The
   DISAGREEING state the rule asks for: a latch bit set by a DIFFERENT reason before this one
   fires -- built in-session by `wmask1 indep' (MASK0's bit set first) and `def r once' (the
   write bit set first).  W_MASK: guard reads f, body writes v -- same derivation from idata,
   no disagreeing state possible.

4. CHANNEL -- per row, the mutant it kills and the observable that differs.  (b) = verbatim
   reinstatement of the kill at that arm; (d) = DEPENDS-ON weakening; each (d) mutant is one edit.
   row              kills                                        observable
   <arm> legal      (b) at that arm                              alive vs dead
   <arm> stored     (b); M_conf_mask (`& 0x3' -> `& 0x1');       read-back value
                    M_tbena_raw (`& TEN' removed); M_base_mask
                    (WEN or SG dropped from the mask, or `& 0xffffffff');
                    M_mask_field (`& 0xfff00000' -> `& 0xfff' etc.)
   wmask0 declined  M_rule_weak (`(f & (f+1)) == 0' -> `f != 0');  read-back 0x500000 vs 0x100000
                    M_store_first (store v before the test)
   wmask0 once      M_nolatch_mask0 (guard on the bit removed)     announce count 2 vs 1
   wmask0 kept2     M_store_first                                  read-back
   wmask1 declined  M_rule_weak at MASK1; M_store_first at MASK1   read-back
   wmask1 indep     M_shared_masklatch (MASK1 uses MASK0's bit)    MASK1 announce count 0 vs 1
   conf reserved    M_conf_mask; M_conf_raw (`& 0x3' removed)      read-back 0x0/0x1/0x100000002 vs 0x2
   conf once        M_nolatch_conf                                 count 2 vs 1
   wen once         M_wen_perreg (two latch bits) / M_nolatch_wen  count 2 vs 1
   wbase1 wen       M_base_mask (WEN dropped)                      read-back 0x40000000 vs 0x240000000
   wbase0 zero      (b) at BASE0 would NOT kill zero (accepted there): this row pins the SROM
                    value at BASE0 for the record; its mutant is M_base0_nonzero (a `!= 0'
                    decline) -- read-back 0x280000000 vs 0x0
   def alive        (b) at default                                alive vs dead
   def w once       M_nolatch_defw                                 count 2 vs 1
   def read0        M_def_echo (default reads return idata/last)  0x5a5a5a5a vs 0x0
   def r once       M_shared_deflatch (one bit for both)          read count 0 vs 1
   ctl noguard/echo (control) no mutant; reddens only if the window or width breaks.
   VACUOUS-BY-CONSTRUCTION CHECK: no row's channel is fixed under its named mutant.  The one
   row whose value is 0 on both a correct build and a store-skipping mutant is `wbase1 stored'
   AFTER the accepted write -- which is why every `stored' session writes the accepted value
   FIRST, so a skipped store reads 0x240000000, not 0.

5. THE (d) ENUMERATION FOR TABLE 1 (DEPENDS-ON, bounded to the diff's own hunks):
   predicates dominating the edited lines: writeflag == MEM_WRITE (unchanged; not mutated),
   the switch label (each arm its own case, no fall-through group -- the 7g-1 discriminator
   does not fire), the mask/field tests introduced by the fix.  Cells: per arm {mask kept,
   mask narrowed, mask dropped} x {store, no store}; masks {rule kept, weakened, strengthened}
   x {store order}; latches {kept, removed, shared}.  Planned mutants (one edit each):
   M1_conf_kill (b)   M2_tbena_kill (b)   M3_base0_kill (b)   M4_mask0_kill (b)
   M5_base1_kill (b)  M6_mask1_kill (b)   M7_def_kill (b)     M8_conf_mask1 (& 0x1)
   M9_conf_raw        M10_tbena_raw       M11_base_nowen (mask drops WEN)
   M12_base_32 (& 0xffffffff)             M13_rule_weak (f != 0)   M14_rule_strong (f == 1)
   M15_store_first (mask0)                M16_nolatch_mask0        M17_shared_masklatch
   M18_nolatch_conf   M19_nolatch_wen     M20_def_echo (read returns idata-ish)
   M21_shared_deflatch                    M22_null (a 217-byte comment-only dev_lca.c is not
   buildable; the null medium here is the PRE-FIX file, i.e. all seven kills at once = HEAD)
   ACCEPT rows (de-escalation): the `live' rows (6) plus `wbase0 zero', `wbase1 wen'.  Their
   growth mutant: M23_accept_narrow (W_BASE0 rejecting 0x300800000, i.e. the old whitelist
   re-added under the new mask) -- reddens `wbase0 live' -- built as the failability check.
```

## THE QUESTIONS — VERDICT LINE FIRST, then answer extensionally
Q1. THE PREMISE AUDIT, as questions.  (a) Is `(f & (f + 1)) == 0` over the 12-bit field EXACTLY the
    thirteen Table 6-6 encodings and nothing else?  Enumerate the 4096 values.  (b) Does dropping
    reserved bits at IOC_CONF (`& 0x3`) change what `lca_pci_conf` reads (it reads bit 0)?  (c) Is
    `0x240000000` really WEN-set (bit 33) so that `wbase1 wen` and `wen once` test what they claim?
    (d) Is +0x1e0 inside DEVINIT's mapped window and absent from `alpha_lcareg.h`, so the default arm
    is what answers it?  (e) Is anything in the diff a behaviour change for an ACCEPTED value that
    the old code took (a regression for a working guest)?
Q2. THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES ALL 40 ROWS.  Name the row you expect to stay
    green.  The enumeration in PRETABLE §5 is the author's; find the cell it does not contain.
Q3. OPTION-SET COMPLETENESS at the default arm and at W_MASK: is there a member the design did not
    name?  Grep the fork for the idiom (dev_gt.c's stored-but-unused address-decode registers and
    dev_footbridge.c's SDRAM_BA_MASK were the precedents named on pass 1).
Q4. THE FLOOR: for each of the six arms, the DEPENDS-ON cells are {mask kept / narrowed / dropped} x
    {store / no store}, and for W_MASK additionally {rule kept / weakened / strengthened} x {store
    before / after the test}, and for the latches {kept / removed / shared}.  Which cell has NO row
    whose channel varies under it?  Say "none" with the denominator if that is the answer.
Q5. ACCEPT-ROW FAILABILITY: for each `live` row and for `wbase0 zero` / `wbase1 wen`, name the growth
    mutant that reddens it (the old whitelist re-added under the new mask is the author's candidate).
Q6. CLAIM -> ROW: quote any added comment sentence asserting an observable consequence that has no
    row and no sentence in PRETABLE §2.
If, while verifying a claim, you found something ELSE — say so.  State what you read versus what you
took from this packet.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
