# PCI configuration-cycle address decode — correctness review of a one-function change

**Scope: this is an ordinary bounds-and-decode correctness review of an emulator device model, and
of the regression test shipped with it.** The subject is `DEVICE_ACCESS(lca_pci_conf)` in a
DEC 21066 (`LCA`) PCI host-bridge model: one local variable was being used for two distinct
quantities, so the handler could not reach its type-1 branch and instead hit an
`unimplemented; abort` stub. The change separates the two quantities and implements the branch.
Please review it as decode correctness and test adequacy.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.
**Check the premises, not just the derivations.** Where I state something as fact, ask whether it
is true. A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are THREE pristine-2021-upstream copies of
GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`). They are
NOT this fork. If your line numbers disagree with mine by hundreds you are reading one of them —
say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined. Name any premise
you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of reachable
addresses — ENUMERATE it rather than reasoning about it.** Walk the values. A derivation that skips
one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.** Ask what the PRODUCER of these
values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## §C0 — HAS THIS ROUND ALREADY SHIPPED?  Checked, both commands, before writing this.

```
git log -1 --oneline -- src/devices/dev_lca.c
  aedd072 #511 pass 2: the token is ratified, two claims are refused, ...

grep -n lcaconfbus1kill CHANGELOG.md
  520: (a #511 paragraph REFERRING to this row's probe -- not a shipped round for it)

highest round number in CHANGELOG.md:  514        ->  #515 is free
```

**The round has NOT shipped.** `#511` fixed a signed-overflow UB *inside* the `bus == 0` scan loop
of this same handler and cited this row's probe; it did not touch the guard under review.

---

## §C — SETTLED PREMISES (each VERIFIED LOCALLY for this brief, not carried from memory)

**P1 — `bus_pci_data_access`'s empty-slot contract.** Read from `src/devices/bus_pci.c`, the
`dev == NULL` arm, verbatim:

```c
	/*  No device? Then return emptiness.  */
	if (dev == NULL) {
		if (writeflag == MEM_READ) {
			if (pci_data->cur_reg == 0)
				*data = (uint64_t) -1;
			else
				*data = 0;
		} else {
			fatal("[ bus_pci_data_access(): write to non-existant"
			    " device, bus %i func %i device %i ]\n",
			    pci_data->cur_bus, pci_data->cur_func,
			    pci_data->cur_device);
		}
		return;
	}
```

So: **reads** return all-ones at register 0 and zero elsewhere; **writes** print a diagnostic
naming `cur_bus`, `cur_func`, `cur_device`. `fatal()` in this fork does NOT exit
(`src/core/debugmsg.c`, `fatal()` has no early-out and no `exit`), so that write path is a
diagnostic, not a detect.

**P2 — `bus_pci_setaddr` has no observable of its own.** Verbatim: it validates two pointers and
assigns `cur_bus`/`cur_device`/`cur_func`/`cur_reg`. Nothing is printed. **This is why the
discriminating oracle in the detector had to be a WRITE and not a read.**

**P3 — exactly one PCI device is registered on this machine.**
`bus_pci_add(devinit->machine, d->pci_data, devinit->machine->memory, 0, 7, 0, "i82378zb");`
— bus 0, device 7, function 0.

**P4 — the i82378zb's configuration header, DERIVED and then MEASURED, and the two agree.**
`PCIINIT(i82378zb)` sets `PCI_ID_REG = PCI_ID_CODE(PCI_VENDOR_INTEL, PCI_PRODUCT_INTEL_SIO)`.
An 8-byte guest `ldq` of registers 0..7 measured **`0x0000000304848086`** on the pre-fix build:
reg 0 = `0x04848086` (vendor 0x8086 Intel, product 0x0484 SIO), reg 4 = `0x00000003`
(command 0x0003, status 0x0000).

**P5 — the address decode, from the handler's own two lines.**
```c
	reg = (relative_addr >> 5) & 0xfc;
	tag = (relative_addr >> 5) & ~0xff;
```
**P6 — the 21066/21066A Hardware Reference Manual is LOCAL and was read for this claim**
(`_scratchpad/21066_66a_hrm.txt`, 13,876 lines). §6.2.9: *"PCI address bits ad<1:0> come directly
from configuration cycle type register (IOC_CONF, Section 6.4.2) bits <1:0>"* — so **IOC_CONF
selects the CYCLE TYPE and does not carry a bus number.** §6.2.6 gives the sparse-space mapping
`<31:7> -> <26:2>`, i.e. the shift of 5.
*Stated narrowly on purpose: the type-1 FIELD POSITIONS (bus 23..16, dev 15..11, fn 10..8,
reg 7..2) come from the PCI Local Bus specification, which §6.2.9 defers to explicitly — NOT from
this manual. A sibling row of mine over-read this same manual last week and a seat caught it.*

---

## §D — THE correctness error, AND THE WITNESS THAT ALREADY EXISTS

`DEVICE_ACCESS(lca_pci_conf)` used ONE variable, `bus`, for TWO different things: the cycle type
selected by `d->ioc_conf & 1`, and the destination bus. Pre-fix:

```c
	bus = d->ioc_conf & 1;

	if (bus == 0) {
		... IDSEL scan, already replace-the-abort-ined ...
	} else {
		fatal("TODO. Non-zero bus.\n");
		exit(1);
	}
```

The `lca_ioc` CONF guard is `if (idata & ~1) { fatal(...); exit(1); }` — so **`0x1` is ACCEPTED and
stored.** A guest then needs no unusual value anywhere: store 1 to IOC_CONF, then make any access
in the config window, and the host process ends.

**RUNG-3 WITNESS, MEASURED:** `regress/lca_confbus_probe.py` on unmodified `alphabook1`,
**3/4 pre-fix** (`artifacts/lcaconfbus1kill/witness_HEAD_20260907.raw`), with a liveness control
(the identical read at `ioc_conf == 0` completes) and a device-signature control (it returns the
empty-slot `0xffff...ffff`, where unmapped would read 0).

---

## §E — THE DIFF UNDER REVIEW (the real one, `git diff`, message suppressed)

```diff
diff --git a/src/devices/dev_lca.c b/src/devices/dev_lca.c
index d3c2488..97c2e6b 100644
--- a/src/devices/dev_lca.c
+++ b/src/devices/dev_lca.c
@@ -89,7 +89,7 @@ void lca_interrupt_deassert(struct interrupt *interrupt)
 DEVICE_ACCESS(lca_pci_conf)
 {
 	uint64_t idata = 0, odata = 0;
-	int tag, bus, dev, func, reg;
+	int tag, type1, bus, dev, func, reg;	/*  #515  */
 	struct lca_data *d = (struct lca_data *) extra;
 
 	if (writeflag == MEM_WRITE)
@@ -118,9 +118,25 @@ DEVICE_ACCESS(lca_pci_conf)
 	 *	tag = (bus << 16) | (device << 11) | (function << 8)
 	 */
 	/*  printf("tag = 0x%x\n", (int)tag);  */
-	bus = d->ioc_conf & 1;
 
-	if (bus == 0) {
+	/*  #515: `bus' used to be BOTH the configuration CYCLE TYPE and the
+	    DESTINATION BUS, and conflating them is the whole correctness error.  IOC_CONF bit 0
+	    selects the cycle type only -- 21066/21066A HRM S6.2.9: "PCI address bits
+	    ad<1:0> come directly from configuration cycle type register (IOC_CONF,
+	    Section 6.4.2) bits <1:0>" -- and it does NOT carry a bus number.  The
+	    destination bus of a type-1 cycle lives in the ADDRESS, per the PCI Local
+	    Bus specification's type-1 layout (bus 23..16, dev 15..11, fn 10..8,
+	    reg 7..2), which S6.2.9 defers to explicitly.
+
+	    Before this, a guest that merely SET bit 0 -- a value the CONF guard
+	    ACCEPTS -- made any subsequent access in this window reach
+	    `fatal("TODO. Non-zero bus."); exit(1)'.  MEASURED: two ordinary guest
+	    accesses, nothing refused anywhere on the path
+	    (regress/lca_confbus_probe.py, 3/4 pre-fix; artifacts/lcaconfbus1kill/).  */
+	type1 = d->ioc_conf & 1;	/*  #515  */
+	bus = 0;			/*  #515  */
+
+	if (!type1) {			/*  #515  */
 		/*  #511: was `0x800 << dev'.  `0x800' is a plain int (2^11) and `dev'
 		    reaches 20, so the last iteration evaluates 2^31 -- a SIGNED
 		    OVERFLOW, undefined by C99 6.5.7p4, not merely
@@ -163,17 +179,32 @@ DEVICE_ACCESS(lca_pci_conf)
 			dev = 0;
 		}
 	} else {
-		fatal("TODO. Non-zero bus.\n");
-		exit(1);
+		/*  #515: a type-1 cycle carries its destination in the address.  */
+		bus = (tag >> 16) & 0xff;	/*  #515  */
+		dev = (tag >> 11) & 0x1f;	/*  #515  */
 	}
 
 	func = (tag >> 8) & 7;
 	/*  printf("bus=%i dev=%i func=%i reg=%i\n", bus,dev,func,reg);  */
 
-	/*  Pass PCI accesses onto bus_pci:  */
-	bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
-	bus_pci_data_access(cpu, d->pci_data, writeflag == MEM_READ?
-	    &odata : &idata, len, writeflag);
+	/*  #515: a type-1 cycle whose bus field is zero selects NOTHING.  Type-1 is
+	    how a bridge is asked to reach a bus BEHIND it; the primary bus is reached
+	    with type-0 cycles, whose IDSEL encoding is decoded above.  Forwarding this
+	    case would set cur_bus = 0 and hand the access to whichever primary-bus
+	    device matched -- `i82378zb' is registered at 0:7:0 by DEVINIT below -- so
+	    simply decoding `bus' and stopping there would replace a unimplemented-path abort with a
+	    NEW MISROUTING.  Refuse it instead, matching `bus_pci_data_access''s own
+	    empty-slot contract (bus_pci.c, the `dev == NULL' arm: all-ones at register
+	    0, zero elsewhere) so the guest sees the ordinary "nothing there" answer.
+	    Writes are discarded, which leaves backend state untouched.  */
+	if (type1 && bus == 0) {		/*  #515  */
+		odata = reg == 0? (uint64_t) -1 : 0;
+	} else {
+		/*  Pass PCI accesses onto bus_pci:  */
+		bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
+		bus_pci_data_access(cpu, d->pci_data, writeflag == MEM_READ?
+		    &odata : &idata, len, writeflag);
+	}
 
 	if (writeflag == MEM_READ)
 		memory_writemax64(cpu, data, len, odata);
```

## §E2 — THE FULL ENCLOSING FUNCTION, POST-FIX

*Inlined because a brief that solicits or evaluates edits must show every exit path and the
common tail: four independent readers once proposed an early `return` into a function whose
last three lines they had not read.*

```c
DEVICE_ACCESS(lca_pci_conf)
{
	uint64_t idata = 0, odata = 0;
	int tag, type1, bus, dev, func, reg;	/*  #515  */
	struct lca_data *d = (struct lca_data *) extra;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	/*
	 *  1. Decompose the address into a tag.
	 *
	 *  According to NetBSD's lca_pci.c, the address is composed like this:
	 *
	 *	addr = tag << 5 | (regoffset & ~0x03) << 5 | 0x3 << 3
	 */
	reg = (relative_addr >> 5) & 0xfc;
	tag = (relative_addr >> 5) & ~0xff;

	/*
	 *  2. Decompose the tag into bus, dev, and func.
	 *
	 *  The tag can be constructed in one of two ways. On the primary
	 *  bus (nr 0):
	 *
	 *	tag = (1 << (device + 11)) | (function << 8);
	 *
	 *  and on other busses, the tag is a normal:
	 *
	 *	tag = (bus << 16) | (device << 11) | (function << 8)
	 */
	/*  printf("tag = 0x%x\n", (int)tag);  */

	/*  #515: `bus' used to be BOTH the configuration CYCLE TYPE and the
	    DESTINATION BUS, and conflating them is the whole correctness error.  IOC_CONF bit 0
	    selects the cycle type only -- 21066/21066A HRM S6.2.9: "PCI address bits
	    ad<1:0> come directly from configuration cycle type register (IOC_CONF,
	    Section 6.4.2) bits <1:0>" -- and it does NOT carry a bus number.  The
	    destination bus of a type-1 cycle lives in the ADDRESS, per the PCI Local
	    Bus specification's type-1 layout (bus 23..16, dev 15..11, fn 10..8,
	    reg 7..2), which S6.2.9 defers to explicitly.

	    Before this, a guest that merely SET bit 0 -- a value the CONF guard
	    ACCEPTS -- made any subsequent access in this window reach
	    `fatal("TODO. Non-zero bus."); exit(1)'.  MEASURED: two ordinary guest
	    accesses, nothing refused anywhere on the path
	    (regress/lca_confbus_probe.py, 3/4 pre-fix; artifacts/lcaconfbus1kill/).  */
	type1 = d->ioc_conf & 1;	/*  #515  */
	bus = 0;			/*  #515  */

	if (!type1) {			/*  #515  */
		/*  #511: was `0x800 << dev'.  `0x800' is a plain int (2^11) and `dev'
		    reaches 20, so the last iteration evaluates 2^31 -- a SIGNED
		    OVERFLOW, undefined by C99 6.5.7p4, not merely
		    implementation-defined.  MEASURED under UBSAN before the change:
		    "dev_lca.c:125:21: runtime error: left shift of 2048 by 20 places
		    cannot be represented in type 'int'", reached by an ordinary guest
		    ldq into the PCI config window (regress/lca_confbus_probe.py against
		    build-asan; artifacts/lcashiftub/ubsan_HEAD_20260907.raw).

		    `0x800U' makes the operand unsigned, so 2048U << 20 is 0x80000000U --
		    inside unsigned int -- and NOTHING ELSE MOVES.

		    *** THE REASON, CORRECTED: AN EARLIER DRAFT SAID `tag' IS "ALREADY A
		    WIDER UNSIGNED QUANTITY".  THAT IS FALSE -- `tag' is a plain signed
		    `int' (:92) -- AND FOUR PASS-2 SEATS CAUGHT IT.  Worse, the claim was
		    backwards: being WIDER is what would CREATE a difference, not remove
		    one.  Had `tag' been `uint64_t', the old `int' 0x80000000 is NEGATIVE
		    and would SIGN-EXTEND to 0xffffffff80000000 for the `&', while
		    `0x800U << 20' zero-extends to 0x0000000080000000 -- two different
		    masks.  The seats were right about the mechanism and it does not fire
		    here only because of the type.

		    WHAT ACTUALLY HOLDS: both operands are 32-bit, so the `&' is performed
		    at 32 bits either way -- `int & int' before, and after, `tag' converted
		    to `unsigned int' by the usual arithmetic conversions.  The RESULT'S
		    BIT PATTERN IS IDENTICAL; only its type changes, and it is consumed
		    solely as a truth test in `if (...)'.  So no guest-visible value moves,
		    and the repair is owed purely by the LANGUAGE. ***

		    *** THE LOOP THIS SITS IN IS THIS FILE'S OWN GRACEFUL-DEGRADATION
		    PRECEDENT -- the `dev >= 21' arm below has a commented-out
		    fatal()/exit(1) and substitutes `dev = 0' instead, and `lcabadval'
		    cites it as a transferable warrant.  The safe path contained the UB. ***  */
		for (dev=0; dev<21; dev++)
			if (tag & (0x800U << dev))	/*  #511  */
				break;
		if (dev >= 21) {
			/*  fatal("[ LCA: No bus 0 device? TODO ]\n");
			exit(1);  */
			dev = 0;
		}
	} else {
		/*  #515: a type-1 cycle carries its destination in the address.  */
		bus = (tag >> 16) & 0xff;	/*  #515  */
		dev = (tag >> 11) & 0x1f;	/*  #515  */
	}

	func = (tag >> 8) & 7;
	/*  printf("bus=%i dev=%i func=%i reg=%i\n", bus,dev,func,reg);  */

	/*  #515: a type-1 cycle whose bus field is zero selects NOTHING.  Type-1 is
	    how a bridge is asked to reach a bus BEHIND it; the primary bus is reached
	    with type-0 cycles, whose IDSEL encoding is decoded above.  Forwarding this
	    case would set cur_bus = 0 and hand the access to whichever primary-bus
	    device matched -- `i82378zb' is registered at 0:7:0 by DEVINIT below -- so
	    simply decoding `bus' and stopping there would replace a unimplemented-path abort with a
	    NEW MISROUTING.  Refuse it instead, matching `bus_pci_data_access''s own
	    empty-slot contract (bus_pci.c, the `dev == NULL' arm: all-ones at register
	    0, zero elsewhere) so the guest sees the ordinary "nothing there" answer.
	    Writes are discarded, which leaves backend state untouched.  */
	if (type1 && bus == 0) {		/*  #515  */
		odata = reg == 0? (uint64_t) -1 : 0;
	} else {
		/*  Pass PCI accesses onto bus_pci:  */
		bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
		bus_pci_data_access(cpu, d->pci_data, writeflag == MEM_READ?
		    &odata : &idata, len, writeflag);
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

---

## §F — THE MEASUREMENT (both runs preserved; each verified by its completion sentinel)

Scratch clone `/tmp/gxlca`, a relocatable `cp -a` of `build/`, baseline named as git HEAD `5d3f82c`;
`dev_lca.c` `cmp`-clean against the baseline before variant 1; the baseline binary REBUILT in the
clone with `[ binary -nt source ]` checked. `build/`, `est/`, `build-asan/` and the WSL tree were
NOT touched.

```
PRE-FIX   LCACONFBUS_RESULT=6/10     (artifacts/lcaconfbus1kill/pass2_20260908/lca_pre.raw)
POST-FIX  LCACONFBUS_RESULT=10/10    (.../lca_post.raw)
```

| row | pre | post | what it is |
|---|---|---|---|
| `bus ctl` | ok | ok | LIVENESS: the identical read at `ioc_conf == 0` completes |
| `bus ctlsig` | ok | ok | DEVICE SIGNATURE: empty-slot `0xffff…ffff`; unmapped would read 0 |
| `bus detect` | **FAIL** | ok | the correctness error row: an accepted `stq 1` then an ordinary `ldq` must not reach the abort |
| `bus attrib` | ok | ok | ATTRIBUTION: a the abort here must carry this arm's unique diagnostic |
| `t1 alive` | **FAIL** | ok | a type-1 write to a NON-zero bus must not reach the abort |
| `t1 anchor` | **FAIL** | ok | **ANCHOR**: forwarding happened AND landed at bus 1 dev 3 func 2 |
| `t1 alias` | **FAIL** | ok | type-1 with bus 0 must NOT be forwarded onto the primary bus |
| `t0 alive` | ok | ok | ACCEPT: the type-0 path still reaches a registered device |
| `t0 real` | ok | ok | ACCEPT: dev 7 is neither empty-slot nor unmapped |
| `t0 accept` | **FAIL** | ok | ACCEPT: the exact pre-fix value `0x304848086` is unchanged |

The anchor's evidence line, echoed into the log by the probe itself:

```
  EVIDENCE(S2): [ bus_pci_data_access(): write to non-existant device, bus 1 func 2 device 3 ]
```

**Addresses derived from the handler's own two lines, then confirmed by that printed tuple:**
`bus 1 dev 3 func 2 reg 0` -> `tag = 0x11a00` -> `relative_addr = 0x234000`; the alias ->
`relative_addr = 0`; type-0 dev 7 -> `tag = 0x40000` -> `relative_addr = 0x800000`. The three
fields are deliberately DISTINCT and non-zero so a swapped field cannot pass by coincidence.

**A correctness error I FOUND IN MY OWN ROW AND FIXED BEFORE THIS BRIEF — please check the repair, not just
the confession.** `t1 alias` first read `refused if ALIAS not in txt2`, and scored **GREEN on the
pre-fix build** — where the host had already aborted at the previous access and the alias write NEVER
EXECUTED. An absence-of-text oracle cannot distinguish "ran and was refused" from "never ran". It
is now bound to `alive2` and renders `aborted-before-E`. **Is that binding sufficient, or can the row
still pass without the access having been serviced?**

---

## §G — THE QUESTIONS

**Q1 — THE VACUITY FLOOR, CLAUSE (d): what is the DEPENDS-ON closure of this diff, and is any cell
unrowed?** The diff adds two predicates — `!type1` (replacing `bus == 0`) and `type1 && bus == 0`.
The guarded body reads `bus`, `dev`, `func`, `reg`, `type1`, `d->pci_data`, `writeflag` and `len`.
The body's own tests induce the partitions {type-0, type-1} × {bus == 0, bus != 0} ×
{read, write}. **Enumerate the cross-product and say which cells the ten rows hold and which they
do not.** I believe the unrowed cells are (type-1, bus != 0, read) and (type-1, bus == 0, read) —
both of which return the same all-ones value as the control, so a read oracle cannot see them.
**Am I right that they are indistinguishable, or is there a channel I have missed?**

**Q2 — IS THE REFUSAL THE RIGHT DISPOSITION, and does it need an announce?** The option set has
seven members (DELETE / DECLINE / DECLINE+LATCHED ANNOUNCE / ACCEPT / FAULT / BACKED ACCEPT /
IMPLEMENT). This diff is member 2 for the alias and member 7 for the type-1 decode. **Three
sub-questions.** (a) Should the alias arm carry the house `(once)` latched announce, or is silence
right given a guest may legitimately probe type-1 space? (b) The refusal DISCARDS writes silently,
whereas forwarding an empty slot PRINTS a diagnostic — so the fix makes one case quieter than the
neighbouring one. Is that asymmetry defensible or is it a sibling-parity breach? (c) **FAULT is
member 5 and is NOT available here** — `memory_rw.c` dispatches a bus error for MIPS and M88K and
there is no Alpha equivalent — but the 21066 manual §6.2.18 says real hardware returns *"arbitrary
data with error status to the CPU, which causes an instruction exception"* on a master abort.
**Should the round disclose that the model's all-ones answer is an emulator-compatibility
convention rather than the hardware contract?**

**Q3 — THE DE-ESCALATION CLAUSE: are the accept rows complete?** This diff DELETES `exit(` from a
device, so every predicate that used to gate the abort owes an accept row proving legal traffic still
lands. I have shipped `t0 accept` (a registered device on the type-0 path still returns its exact
pre-fix config data) and `t1 anchor` (type-1 to a real bus still forwards, to the right tuple).
**Is a third row owed for the type-1 path reaching a REGISTERED device?** No device exists on any
bus but 0, so I cannot build that state without adding one — and adding a device to reach a site is
the laundering the witness ladder forbids. **Is "no such state is constructible on this machine" an
acceptable disclosure, or does it mean the forwarding path is untested where it matters most?**

**Q4 — THE ANCHOR ROW'S OWN FRAGILITY.** `t1 anchor` matches the literal
`bus 1 func 2 device 3` in `bus_pci_data_access`'s diagnostic. That string is a `fatal()` in a file
this round does not touch. **If someone reworded that diagnostic, my anchor row goes silently
green-to-red — or worse, a reworded-but-still-printed message could make it red while nothing is
wrong. Is that an acceptable coupling for the only absolute-position oracle in this detector, and
is there a better channel I have not found?** (I checked: `bus_pci_setaddr` prints nothing, so I
believe this is the only one. Please refute that if you can.)
