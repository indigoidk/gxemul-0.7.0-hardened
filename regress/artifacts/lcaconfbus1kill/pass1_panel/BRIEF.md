# DESIGN BRIEF — `lcaconfbus1kill` pass 1: what should `lca_pci_conf` do for a non-zero bus?

**VERDICT LINE FIRST**, then the body.

Tree under review: **`GXEMUL-SEC/src/`**. Ignore any other `src/` under the project root — three
pristine 2021 upstream copies live there and give line numbers off by hundreds.

## PLEASE DO NOT SIMPLY RATIFY

A recent panel here had seven of nine seats confirm a premise the brief stated wrongly. **Check the
premises, not just the derivations.** I have already had to withdraw one characterisation of this
very fix (see "A correction of mine" below), so treat my proposal as a sketch, not a design.

---

# SETTLED PREMISES (inlined; you need not read files)

**1. The defect is MEASURED, rung 3.** `regress/lca_confbus_probe.py` on unmodified `alphabook1`:
a guest `stq` of `0x1` to `LCA_IOC_CONF` is **accepted** (`idata & ~1` is 0), and the *next* guest
`ldq` into the PCI config window ends the host.

    bus ctl      yes                    yes                    control read at ioc_conf==0 survived   ok
    bus ctlsig   0xffffffffffffffff     0xffffffffffffffff     empty-slot ID probe signature          ok
    bus kill     dead                   alive                  <- THE DEFECT                          FAIL
    bus attrib   yes                    yes                    EVIDENCE: TODO. Non-zero bus.          ok

**2. The code.** `DEVICE_ACCESS(lca_pci_conf)`, verbatim, after `#511`:

```c
	reg = (relative_addr >> 5) & 0xfc;
	tag = (relative_addr >> 5) & ~0xff;

	bus = d->ioc_conf & 1;

	if (bus == 0) {
		for (dev=0; dev<21; dev++)
			if (tag & (0x800U << dev))	/*  #511  */
				break;
		if (dev >= 21) {
			/*  fatal("[ LCA: No bus 0 device? TODO ]\n");
			exit(1);  */
			dev = 0;
		}
	} else {
		fatal("TODO. Non-zero bus.\n");
		exit(1);
	}

	func = (tag >> 8) & 7;
	/*  Pass PCI accesses onto bus_pci:  */
	bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
	bus_pci_data_access(cpu, d->pci_data, ...);
```

**3. The file's own comment on tag layout**, quoted verbatim:

```
	 *  According to NetBSD's lca_pci.c, the address is composed like this:
	 *	addr = tag << 5 | (regoffset & ~0x03) << 5 | 0x3 << 3
	 *
	 *  On the primary bus (nr 0):
	 *	tag = (1 << (device + 11)) | (function << 8);
	 *  and on other busses, the tag is a normal:
	 *	tag = (bus << 16) | (device << 11) | (function << 8)
```

**4. `bus_pci` is bus-agnostic**, verified: `cur_bus` is a plain `int` (`bus_pci.h:84`), devices are
a **linked list** (`first_device`), and lookup is `dev->bus == pci_data->cur_bus` (`bus_pci.c:102`).
Nothing is sized for one bus and nothing asserts. An empty-slot **read** returns
`0xffffffffffffffff` — which the probe's `bus ctlsig` row has MEASURED on bus 0.

**5. `fatal()` does not terminate**; only the explicit `exit(1)` does.

---

# A CORRECTION OF MINE, MADE BEFORE WRITING THIS

I earlier recorded that the fix is **"a DELETION — stop special-casing `bus != 0` and let the
existing path serve the cycle."** *** THAT IS WRONG AND I WITHDRAW IT. *** The `bus == 0` branch does
not merely guard — it **computes `dev`** from the IDSEL bit. Deleting the `else` would leave `dev`
**uninitialised** on the non-zero-bus path and pass garbage to `bus_pci_setaddr`.

So this is option-set **member 7 (IMPLEMENT)**, not a deletion. That changes what the round owes.

# THE SKETCH I WANT ATTACKED

Per premise 3, a non-zero-bus tag is `(bus << 16) | (device << 11) | (function << 8)`, so:

```c
	} else {
		dev = (tag >> 11) & 0x1f;	/*  type-1: device is bits 15..11  */
	}
```

leaving `func` and `reg` as they already are, and letting `bus_pci_setaddr(bus, dev, func, reg)`
serve the cycle — an absent device on an absent bus then answers all-ones by itself.

## Questions

1. **Is `dev = (tag >> 11) & 0x1f` right?** The comment says device occupies bits 15..11 of the tag
   for type-1. **But `tag` here is `(relative_addr >> 5) & ~0xff`, which has already been shifted** —
   so is the comment describing the same `tag` this code computes, or the pre-shift value? **This is
   the premise I am least sure of and it is the whole fix.**

2. **Where does `bus` come from architecturally?** The code takes it from `ioc_conf & 1` — a
   *register bit* — while the type-1 tag layout says the bus number is in **bits 23..16 of the tag**.
   Those are two different sources. **Which one does real LCA hardware use, and does the model's
   choice make the type-1 decode incoherent?** If `bus` should come from the tag, the fix is
   different and larger.

3. **Is IMPLEMENT even the right member here?** The alternatives: DECLINE the cycle silently;
   DECLINE with a latched announce; or return all-ones explicitly without touching `bus_pci`. Note
   that on real hardware a config read of an absent device returns all-ones, so declining and
   implementing may be **observationally identical for an empty bus** — and differ only if a device
   is ever placed on bus 1, which nothing in this tree does.

4. *** THE DISCRIMINATING ROW. *** The existing witness only checks that the host survives, and
   "survives" is true for a silent return, a latched announce, and a working implementation alike.
   I propose adding the mirror of `bus ctlsig` on the armed side: **the armed read must return
   `0xffffffffffffffff`**, which separates "serviced an empty bus" from "returned without
   servicing" (`0x0`, indistinguishable from unmapped). **Is that sufficient, or does it still
   conflate members?**

5. **What does this NOT close?** The `default:` arm of `lca_ioc` still exits for reads and writes,
   and `lca_interrupt_assert`/`_deassert` are still bare kills (filed as `lcairqstubkill`, witnessed).

6. If, while checking this, you found something ELSE — say so.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* Give the denominator: how many callers/consumers of `bus_pci_setaddr` you examined.
* A clean "your Q1 shift is wrong because X" is the most useful answer you can give.
