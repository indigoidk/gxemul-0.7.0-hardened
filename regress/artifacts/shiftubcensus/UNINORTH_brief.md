# CAN A GUEST ACCESS TO THE UNI-NORTH PCI ADDRESS REGISTER CARRY BITS 32..63?

**VERDICT LINE FIRST.** Scope to `GXEMUL-SEC/src/`; ignore any other `src/` under the project root.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.** Do not write a probe.

This is a **reachability and width question about one register**, not a design task. I want to know
what values a guest can actually place in one variable.

## The situation, verified by reading

`machine_macppc.c:68` instantiates `dev_uninorth_init(machine, machine->memory, 0xe2000000, ...)`,
and `dev_uninorth.c:141` registers `"uninorth_pci_addr"` at `addr + 0x800000`. The write path is:

```c
	if (writeflag == MEM_WRITE) {
		uint64_t idata = memory_readmax64(cpu, data, len
		    | MEM_PCI_LITTLE_ENDIAN);
		int bus, dev, func, reg;

		d->cur_addr = idata;
		if (idata == 0)
			return 0;

		if (idata & 1) {
			idata &= ~1;
			bus_pci_decompose_1(idata, &bus, &dev, &func, &reg);
		} else {
			bus = 0;
			for (dev=11; dev<32; dev++)
				if (idata & (1 << dev))
					break;
			...
		}
```

**`idata` is `uint64_t`.** `1 << dev` is an `int`, so at `dev == 31` it is `0x80000000`, which as a
signed `int` is NEGATIVE and **sign-extends to `0xffffffff80000000`** when converted for the `&`
against a `uint64_t`.

**So if `idata` can carry any bit in 32..63, the loop matches at `dev == 31` when it should not, and
the scan selects the wrong device.** If `idata` can never carry such a bit, the extra ones meet only
zeros and nothing observable happens.

## Questions

1. *** THE ONE THAT DECIDES IT. *** **What does `memory_readmax64(cpu, data, len)` return for each
   `len` this handler can be called with?** Specifically: can it return a value with any bit in
   32..63 set, and under what access width? Name the function and quote the relevant lines.

2. **What access widths actually reach this handler?** `memory_device_register` records a length for
   the region; the CPU's load/store path may split, clamp or reject widths. **On `macppc`
   specifically, can a guest issue an 8-byte store to `0xe2800000`?** PowerPC has 8-byte stores
   (`std` on 64-bit, `stfd`); whether one reaches a device handler intact is the question.

3. **Does `MEM_PCI_LITTLE_ENDIAN` change the width or only the byte order?** It is OR'd into the
   `len` argument, which looks like a flag sharing a parameter with a size — **I want to know whether
   that OR can perturb the length itself.** This is the premise I am least sure of.

4. **Is there any masking of `idata` before the loop that I have missed?** I see `idata &= ~1` only
   inside the `idata & 1` branch, which is the other arm. If something upstream truncates to 32 bits,
   say where.

5. **Same question for the sibling at `dev_v3.c:164`** — there `relative_addr` is `uint64_t` but is
   masked to 20 bits at `:161` and OR'd with a value that cannot exceed bit 31 at `:162`, so I
   believe its bits 32..63 are provably zero and the same shift is harmless. **Check that.**

6. If you found something else about this handler, say so.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* Give the denominator: how many call paths into this handler you examined.
* A clean "your premise in Q3 is wrong because X" is the most useful answer you can give.
