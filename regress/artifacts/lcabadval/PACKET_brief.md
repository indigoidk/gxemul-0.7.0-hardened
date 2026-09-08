# LCA window-mask registers: is my reading of the manual right, and what should the fix be?

**VERDICT LINE FIRST.**

You cannot open files, so **every fact you need is inlined below**. If a premise cannot be settled
from this packet, **say so plainly** — an honest "not checkable from here" is the answer I want.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
had stated wrongly. **Check the premises, not just the derivations** — and the load-bearing premise
here is my own arithmetic, done an hour ago.

## 1. THE CODE

`DEVICE_ACCESS(lca_ioc)` in this fork's `src/devices/dev_lca.c` handles writes to the LCA chipset's
I/O-controller registers. Six arms accept a narrow set of values and terminate the emulator process
on anything else:

```c
	case LCA_IOC_CONF:      if (idata & ~1)                              -> fatal + exit(1)
	case LCA_IOC_TB_ENA:    if (idata & ~IOC_TB_ENA_TEN)                 -> fatal + exit(1)
	case LCA_IOC_W_BASE0:   if (idata != 0 && idata != 0x300800000ULL)   -> fatal + exit(1)
	case LCA_IOC_W_MASK0:   if (idata != 0x700000ULL)                    -> fatal + exit(1)
	case LCA_IOC_W_BASE1:   if (idata != 0x240000000ULL)                 -> fatal + exit(1)
	case LCA_IOC_W_MASK1:   if (idata != 0x3ff00000ULL)                  -> fatal + exit(1)
```

`fatal()` here only prints — it has no early-out and returns normally. Only the explicit `exit(1)`
terminates the process. `idata` is the value the guest wrote.

## 2. THE MANUAL, QUOTED VERBATIM

From the Alpha 21066/21066A Hardware Reference Manual (EC-QC4GB-TE), which I have locally:

> *"The window mask register IOC_W_MASK provides a mask corresponding to bits <31:20> of an
> incoming PCI address. The size of each window is programmed to be from 1 MB to 4 GB by masking
> bits of the incoming PCI address with the IOC_W_MASK register. Table 6-6 shows the supported
> values of IOC_W_MASK register bits <31:20>; **other values are unsupported**."*

Table 6-6, all thirteen rows:

    IOC_W_MASK<31:20>   Window size        IOC_W_MASK<31:20>   Window size
    0000 0000 0000        1 MB             0000 1111 1111       256 MB
    0000 0000 0001        2 MB             0001 1111 1111       512 MB
    0000 0000 0011        4 MB             0011 1111 1111         1 GB
    0000 0000 0111        8 MB             0111 1111 1111         2 GB
    0000 0000 1111       16 MB             1111 1111 1111         4 GB
    0000 0001 1111       32 MB
    0000 0011 1111       64 MB
    0000 0111 1111      128 MB

And the matching rule: each incoming PCI address bit <31:20> is XORed with the corresponding window
base bit, and the result ANDed with the complement of the corresponding mask bit.

## 3. MY DERIVATION — this is what I want challenged

The register value is the `<31:20>` field shifted left by 20.

* `0x700000 >> 20 = 0x007` = `0000 0000 0111` = **8 MB**. Legal, one of thirteen.
* `0x3ff00000 >> 20 = 0x3ff` = `0011 1111 1111` = **1 GB**. Legal, one of thirteen.
* The legal set satisfies `(f & (f + 1)) == 0` — a contiguous run of low ones.

> **THEREFORE: the model terminates the host on TWELVE documented-legal values per mask register,
> 24 across the two. A guest programming any window size other than 8 MB / 1 GB is doing something
> the hardware manual explicitly supports.**

## 4. QUESTIONS

**Q1. Is that derivation right?** Check the shift, the two field values, the count of thirteen, and
the `(f & (f+1)) == 0` invariant. **If any step is wrong, the severity claim collapses — say so.**

**Q2. Is `(f & (f+1)) == 0` the right guard to ship**, or does it admit something Table 6-6
excludes / exclude something it admits? Give a counter-example if there is one.

**Q3. What should the six arms do instead?** The options are: delete the termination entirely;
decline the write silently; decline with a once-only announcement (this fork's house style, marked
`(once)`); accept and store the value; or accept with backing storage so reads return it. **Pick
one per arm and say why** — note that `W_MASK` and `W_BASE` have different characters, since the
manual enumerates legal values for one and not the other.

**Q4. Which is the more dangerous error direction here** — terminating on a legal value, or
silently accepting a value the model then does not honour in its address decode? The model's window
matching may not use these registers at all.

**Q5. What is the smallest plausible code change that would look like a correct fix and still leave
a legal value terminating the process?** Name it concretely.
