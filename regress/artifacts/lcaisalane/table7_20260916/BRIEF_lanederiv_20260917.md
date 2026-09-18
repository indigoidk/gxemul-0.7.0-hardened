# `#530` -- THE ONE THING THE FABLE ADJUDICATION LEFT UNSETTLED, AND IT DECIDES ROW-vs-PRODUCT

## VERDICT LINE FIRST.

**Fable's closing sentence, verbatim:** *"Not settled here, and I say so: whether the len-16 lane
derivation in D5 is right -- I derived it, nobody ran it."*

**You are being asked to settle it, or to say precisely what would.**  This is not a review of a
diff; it is one architectural question whose answer changes the disposition of an L2.

**TREE: `GXEMUL-SEC/`.**  Three pristine-2021 upstream copies sit under the PROJECT root; line
numbers off by hundreds mean you read one.  You can read files.  **PLEASE DO NOT RATIFY.**

## S1 -- THE STAKES, STATED PLAINLY

`#530` has a MEASURED L2 floor breach: the mutant `len == 0` -> `len == 0 || len > 8` scores
**352/352, a total escape** against the shipped detector.  The round's own pre-specified rule made
that L2 because `len > 8` is guest-reachable.

**The main loop then recorded "what is owed is a ROW, not a product change", on the reasoning that
the shipped code is CORRECT at wide widths.**  Fable accepted the L2 but flagged that clause as
CONDITIONAL and unestablished:

> *"The single fact that decides it: a 16-byte `memory_rw` at `lca_isa` is a `store_buf` artefact
> (split granule 1 KB), which on hardware would be TWO 8-byte transactions each forwarding its own
> lane byte -- while the shipped code forwards ONE byte for len 16.  If that derivation holds,
> `len > 8` is a LOST BYTE and a PRODUCT CHANGE, and the row's oracle must not pin one-byte as
> architecture."*

**If Fable is right, the fix is wrong and the row would PIN THE WRONG BEHAVIOUR AS ARCHITECTURE.**
That is the worst outcome available here: a detector certifying a defect.

## S2 -- THE CODE, INLINED EXACTLY

`src/devices/dev_lca.c`, the tail of the ISA-lane handler:

```c
	 *  One byte is forwarded whatever len is (the size field a<4:3> is
	 *  not decoded here).  len 0 has no producer; refuse it before the %.
	 */
	if (len == 0)
		return 0;
	ofs = (relative_addr & 3) % len;

	if (writeflag == MEM_WRITE) {
		byte = data[ofs];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);

	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;

	return 1;
}
```

`src/core/memory.c`, `store_buf()` -- the producer of wide `len`:

```c
void store_buf(struct cpu *cpu, uint64_t addr, const char *s, size_t len)
{
	size_t psize = 1024;	/*  1024 256 64 16 4 1  */

	while (len != 0) {
		if ((addr & (psize-1)) == 0) {
			while (len >= psize) {
				cpu->memory_rw(cpu, cpu->mem, addr,
				    (unsigned char *)s, psize, MEM_WRITE,
				    CACHE_DATA);
				addr += psize;  s += psize;  len -= psize;
			}
		}
		psize >>= 2;
	}
	while (len-- != 0)
		store_byte(cpu, addr++, *s++);
}
```

So for `len` 16 the handler is entered ONCE with `len == 16`, computes `ofs = (relative_addr & 3) %
16` which is in [0,3], forwards **ONE** byte, and on a read **zeroes the other fifteen**.

## S3 -- SETTLED PREMISES (read locally; do not re-derive)

* **The local manual is `_scratchpad/21066_66a_hrm.txt`** (Alpha 21066/21066A HRM, EC-QC4GB-TE).
* `:8840` (S6.2.6): CPU physical address bits <31:7> map to PCI address bits <26:2>.
* `:9216` (S6.2.9): PCI ad<1:0> come from IOC_CONF<1:0> -- **IOC_CONF selects the CYCLE TYPE and
  does NOT supply a bus number.**
* `:9486` (S6.2.18, PCI Master Abort): an unanswered read *"returns arbitrary data with error
  status to the CPU"* -- **absent-device reads on real LCA hardware are NOT all-ones**; the
  0xffffffff signature is an emulator-compatibility oracle, never a hardware contract.
* `len > 8` reachability is ESTABLISHED: PROM GETENV calls `store_buf(cpu, a2, s, len)` with a
  **guest-supplied `a2`** (`cpu_alpha_palcode.c`), and `len` is clamped to `strlen(s)+1`, so a boot
  kernel filename of >= 15 chars yields `len >= 16`.

## S4 -- THE QUESTIONS

1. **IS FABLE'S DERIVATION RIGHT?**  Does the ISA lane window's addressing mean a 16-byte access
   SHOULD forward more than one byte -- and if so, how many, and from which offsets?  **Answer from
   the manual and the code, not from plausibility.**  The comment claims `a<4:3>` is "not decoded
   here"; is that the reason one byte is right, or the reason the model is lossy?

2. **IS A WIDE `memory_rw` AT THIS WINDOW EVEN ARCHITECTURALLY MEANINGFUL?**  `store_buf` is an
   EMULATOR CONVENIENCE that splits a buffer into power-of-two granules. A 16-byte granule landing
   on an ISA byte-lane window may be an ARTEFACT OF THE EMULATOR'S OWN WRITER rather than anything
   a guest can express with an instruction (the widest Alpha store is STQ = 8 bytes).
   **If it is an artefact, "correct behaviour" may be undefined and the honest answer is to DECLINE
   rather than to pin either shape.**  Which is it?

3. **WHAT SHOULD THE ROW PIN?**  Three candidates, and I want the one you can defend:
   (a) one byte forwarded, fifteen zeroed -- today's behaviour, pinned as architecture;
   (b) multiple lane bytes forwarded -- Fable's reading, i.e. a PRODUCT CHANGE;
   (c) DECLINE `len > 8` -- i.e. the MUTANT is the correct behaviour and the fix is what is wrong.
   **Note (c) would invert the entire finding**, and I want to know if it is defensible.

4. **IF IT CANNOT BE SETTLED FROM THE MANUAL, NAME THE SINGLE MEASUREMENT THAT WOULD.**  An honest
   "not settleable, here is the experiment" is worth more than a confident guess.

**STANDING LICENSE: if while checking this you find something else, say so.**
