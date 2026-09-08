# LCA IOC registers: check the fork's accepted value sets against the manual

**VERDICT LINE FIRST.**

**The tree under review is `GXEMUL-SEC/src/`** — ignore the pristine 2021 copy at the project root.
**The manual is `_scratchpad/21066_66a_hrm.txt`** (Alpha 21066/21066A HRM, EC-QC4GB-TE, 13,876
lines), local and readable.

**Please check the premises, not just the derivations.** Everything below marked MEASURED I derived
myself this morning and may have got wrong; everything marked QUOTED is verbatim from the local
manual text at the line given.

## 1. THE SITE

`DEVICE_ACCESS(lca_ioc)` in `src/devices/dev_lca.c` has SIX arms that accept a narrow set of
written values and call `exit(1)` on anything else, plus a `default:` arm that does the same for
unlisted offsets:

```c
	case LCA_IOC_CONF:      if (idata & ~1)                    -> fatal + exit(1)
	case LCA_IOC_TB_ENA:    if (idata & ~IOC_TB_ENA_TEN)       -> fatal + exit(1)
	case LCA_IOC_W_BASE0:   if (idata != 0 && idata != 0x300800000ULL) -> fatal + exit(1)
	case LCA_IOC_W_MASK0:   if (idata != 0x700000ULL)          -> fatal + exit(1)
	case LCA_IOC_W_BASE1:   if (idata != 0x240000000ULL)       -> fatal + exit(1)
	case LCA_IOC_W_MASK1:   if (idata != 0x3ff00000ULL)        -> fatal + exit(1)
	default:                                                    -> fatal + exit(1)
```

`fatal()` does not exit (`debugmsg.c:384` has no early-out and returns); only the explicit
`exit(1)` terminates.

## 2. WHAT I ESTABLISHED THIS MORNING — verify it, do not assume it

**QUOTED, `21066_66a_hrm.txt:9572-9578`:**

> *"The window mask register IOC_W_MASK provides a mask corresponding to bits <31:20> of an
> incoming PCI address. The size of each window is programmed to be from 1 MB to 4 GB by masking
> bits of the incoming PCI address with the IOC_W_MASK register. Table 6-6 shows the supported
> values of IOC_W_MASK register bits <31:20>; **other values are unsupported**."*

**QUOTED, Table 6-6 at `:9581-9598`** — thirteen rows, a doubling run:

    0000 0000 0000  1 MB      0000 0011 1111   64 MB     0011 1111 1111   1 GB
    0000 0000 0001  2 MB      0000 0111 1111  128 MB     0111 1111 1111   2 GB
    0000 0000 0011  4 MB      0000 1111 1111  256 MB     1111 1111 1111   4 GB
    0000 0000 0111  8 MB      0001 1111 1111  512 MB
    0000 0000 1111 16 MB

**MEASURED (my arithmetic — check it):** the register value is the field shifted left 20.
`0x700000 >> 20 = 0x007` = 8 MB; `0x3ff00000 >> 20 = 0x3ff` = 1 GB. **Both accepted values are
legal**, and each is **one of thirteen**. The legal set satisfies `(f & (f + 1)) == 0` — a
contiguous run of low ones.

> **THEREFORE (my conclusion, which is the thing I most want challenged): the model terminates the
> host on TWELVE documented-legal values per mask register — 24 across the two — and a guest that
> programs any window size other than 8 MB / 1 GB is not doing anything unsupported.**

**QUOTED, `:9600-9611`:** `IOC_W_BASE<31:20>` specifies the window start in PCI memory space;
matching is `((pci_addr<31:20> XOR base<31:20>) AND NOT mask<31:20>) == 0`. **I found no enumerated
legal set for W_BASE** — but I did not read §6.4.9 in full.

## 3. QUESTIONS

**Q1. Is my Table 6-6 reading right?** Watch for the extraction hazard this project has been bitten
by: `pdftotext -layout` staggers table cells, so names and values can land on different lines.
Calibrate on a row BELOW the one you cite, or on two rows straddling it — a single calibration
point is only valid for a uniform stagger and you cannot tell which kind you have from one point.
**Table 6-6 looked self-calibrating to me (a doubling bit-run beside a doubling size run), but say
if it is not.**

**Q2. The other four arms — what does the manual actually permit?** Read §6.4 for `IOC_CONF`,
`IOC_TB_ENA`, `IOC_W_BASE0` and `IOC_W_BASE1` and say, per register, what the legal value set is
and how many legal values the fork rejects. **Give a count with its denominator.** If the manual
does not constrain a register, say that plainly rather than inventing a bound.

**Q3. `0x300800000` and `0x240000000` are 34-bit values.** How wide are these registers, and what
do bits above 31 mean? Does the fork's accepted constant even correspond to a `<31:20>` field, or
is something else going on?

**Q4. What is the right disposition?** The refusal-decision menu here is: delete the termination;
decline silently; decline with a once-only announcement; accept and store; accept with backing
storage. **Which, and why?** Note the architectural-fault option is NOT available — `memory_rw.c`'s
device-failure path has `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` arms only, and `ALPHA_KENTRY_MM`
has zero consumers. **And grep the fork for an existing idiom before reasoning from first
principles — the tree's own precedents are part of the design space, and its house style for a
guest-drivable diagnostic is a once-only latch, `(once)` being the plurality marker.**

**Q5. Is a guest reproduction possible on unmodified `-E alpha -e alphabook1`?** Say what it would
look like, or say plainly that you could not find one.
