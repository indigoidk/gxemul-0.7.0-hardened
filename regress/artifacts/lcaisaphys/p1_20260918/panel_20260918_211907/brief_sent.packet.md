# `#540` (lcaisaphys) PASS 1 -- the sparse ISA window forwards a PHYSICAL address without PHYSICAL

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` AT COMMIT `e0be9b2`** (`dev_lca.c` unchanged since `8bd97e4`).  Pristine-2021 copies elsewhere under the project
root are NOT this fork; if your line numbers disagree with mine by hundreds, you are reading one of them.
**If you cannot read files that is expected** -- every fact you need is inlined; name any premise you cannot settle.
**Where this brief states an arithmetic claim, enumerate it.**  **VERDICT LINE FIRST.**

**Seats that read files: read ONLY** `GXEMUL-SEC/src/devices/dev_lca.c`, `GXEMUL-SEC/src/cpus/memory_rw.c`,
`GXEMUL-SEC/src/cpus/memory_alpha.c`, `GXEMUL-SEC/regress/lca_isaphys_probe.py`.  Do not browse the rest of
`regress/`, `regress/artifacts/` or `tools/`.

    VERDICT: GO | GO-WITH-CHANGES | NO-GO -- <one line naming the deciding item>

## 1. HAS THIS ALREADY SHIPPED? (§C0, run at brief-writing time)

    git log -1 -- src/devices/dev_lca.c   ->  8bd97e4 #530 lcaisalane (a different row)
    grep lcaisaphys CHANGELOG.md          ->  (no match)
    ls regress/ | grep isaphys            ->  lca_isaphys_probe.py  (this round's new, uncommitted witness)

## 2. THE DEFECT, AND THE FUNCTION IT IS IN (committed, whole)

```c
DEVICE_ACCESS(lca_isa)
{
	unsigned int ofs, i;
	uint8_t byte;

	relative_addr >>= 5;
	/*  (a 13-line #530 comment elided here)  */
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

`lca_isa` is registered over the sparse window at `LCA_PCI_SIO = 0x1c0000000`; `LCA_ISA_BASE = LCA_PCI_SIO +
0x10000000 = 0x1d0000000` is where `bus_isa_init` registered the real ISA devices (ns16550, 8259, 8253, 8042,
pccmos).  **`LCA_ISA_BASE + port` is a PHYSICAL address.**  Both nested calls pass it with misc flags `CACHE_NONE`
and no `PHYSICAL`, so `memory_rw` hands it to the Alpha translator as a VIRTUAL address:

```c
	/* memory_rw.c */
	if (misc_flags & PHYSICAL || cpu->translate_v2p == NULL) {
		paddr = vaddr;
	} else {
		ok = cpu->translate_v2p(cpu, vaddr, &paddr, ...);
		if (!ok) { /* #244: zero a read buffer */ ...  return MEMORY_ACCESS_FAILED; }
	}
```

```c
	/* memory_alpha.c, alpha_translate_v2p() */
	if (!userMode && (vaddr >= ALPHA_K0SEG_BASE && vaddr <= ALPHA_K0SEG_END)) {   /* K0SEG: identity */
		*return_paddr = vaddr & 0x000003ffffffffffULL;  return 2;
	}
	if (!userMode && base == 0) {                          /* ptbr == 0: "UGLY hack", identity */
		*return_paddr = vaddr & 0x000003ffffffffffULL;  ...  return 2;
	}
	/* otherwise: a 3-level walk from ptbr; an invalid pte1 -> not_found: */
	fatal("[ alpha_translate_v2p: 0x%016" PRIx64" wasn't found ]\n", vaddr);
	return 0;
```

So the forward works ONLY while ptbr == 0.  Once a guest arms a page table (any Alpha OS does), the inner address
walks the GUEST's tables: a read answers a false zero with success, a write is silently abandoned, and each access
prints the `wasn't found` line -- an unlatched, guest-drivable message flood.  **Every existing LCA probe runs with
ptbr == 0, which is why nothing has ever seen it.**

## 3. THE WITNESS (rung 3) -- `regress/lca_isaphys_probe.py`, MEASURED on the committed build

One unmodified `-E alpha -e alphabook1` process.  Controls while ptbr == 0; then `CALL_PAL 0x30` (swpctx) with a PCB
whose ptbr names an all-zero L1 page (PFN `0x01050000 >> 13 = 0x828`, computed); then the defect accesses, each OUTER
access through K0SEG (identity) so the handler is entered, the INNER forward being the defect.  The pointer block is
re-based to K0SEG before the arm (a raw-VA pointer load would itself walk and miss after it).  If any arming control
is red the probe prints `LCAISAPHYS_CONTROL=DEAD`, `RESULT=0/0` and scores nothing.

    row          got              want            role
    alive        alive            alive           control
    live         0x55             0x55            LIVENESS through lca_isa (8042 self-test reply), ptbr == 0
    flat lsr     0x60             0x60            DEVICE SIGNATURE at the defect port, via the flat mapping
    ram plant    0xaaaa0000aaaa   0xaaaa0000aaaa  the arming VA is a real RAM cell under identity
    ptbr miss    present          present         PAGING IS ON: that VA now walks and misses
    ptbr sent    0xbad1d8a        0xbad1d8a       the walked load did not complete
    pte2 todo    absent           absent          the walk stopped at the zero L1 entry
    sp lsr ans   completed        completed       the sparse read returned
    sp lsr       0x0              0x60            DEFECT: sparse LSR after the arm   -- FAIL
    w lands      0x0              0x5a            DEFECT: sparse store after the arm -- FAIL
    r miss       present          absent          DEFECT: inner read miss at 0x1d00003fd -- FAIL
    w miss       present          absent          DEFECT: inner write miss at 0x1d00003ff -- FAIL
    row count    13               13              identity
    LCAISAPHYS_RESULT=9/13, no retry.  build/ == HEAD on every file of the path.

## 4. THE PROPOSED FIX -- two tokens

```c
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE | PHYSICAL);
	...
	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE | PHYSICAL);
```

**NOT `NO_EXCEPTIONS`**, which an earlier seat traced to a SECOND window-death: the device dispatch in `memory_rw.c`
is `if (!no_exceptions || (mem->devices[i].flags & DM_READS_HAVE_NO_SIDE_EFFECTS)) res = mem->devices[i].f(...);`,
and every ISA target here is registered `DM_DEFAULT` (0) -- so with `NO_EXCEPTIONS` the handler is NEVER CALLED, and
on the write arm the inner call would then report success for a store that never happened.

**Precedent census, DERIVED at brief-writing time** (every `memory_rw(...)` call in `src/devices/*.c`, comments
stripped, arguments joined across lines, classified by its misc-flags argument) -- stated in full because an earlier
note got it wrong.  **56 calls pass `PHYSICAL`:**

    38  NO_EXCEPTIONS | PHYSICAL   10 files: dev_dreamcast_maple.c 12, dev_dec21143.c 9, dev_pvr.c 3, dev_sgi_re.c 3,
                                   dev_jazz.c 2, dev_px.c 2, dev_scc.c 2, dev_sgi_gbe.c 2, dev_ssc.c 2, dev_luna88k.c 1
                                   (DMA to or from RAM, where the DM_DEFAULT skip does not arise)
    16  bare PHYSICAL              dev_sgi_mec.c 7, dev_pccmos.c 3, dev_sh4.c 2, dev_ps2_spd.c 2,
                                   dev_dreamcast_gdrom.c 1, dev_ram.c 1
     2  CACHE_NONE | PHYSICAL      dev_ps2_stuff.c 2

The row's research note called `CACHE_NONE | PHYSICAL` "already how dev_sh4.c, dev_pccmos.c and Maple forward a
known physical address" -- false for all three (bare, bare, and `NO_EXCEPTIONS | PHYSICAL`).  The proposal keeps the
EXISTING `CACHE_NONE` and adds one token, which is the smallest edit, not an appeal to a house idiom.

**Keeping `CACHE_NONE`:** in `memory_rw.c` the `cache` value is read by the translate call (skipped under `PHYSICAL`),
by three `#ifdef MEM_MIPS` / `MEM_M88K` blocks (not compiled into the Alpha unit), and by two RAM-path conditions.
My reading is that none of those is reached by a device address above `physical_max`, so `CACHE_NONE | PHYSICAL` and
bare `PHYSICAL` behave identically here -- **check that; I have not enumerated the RAM-path conditions.**

## 5. SETTLED PREMISES

* **The witness reproduces on the committed build**, per the table in §3 (measured today).
* **K0SEG is identity-mapped before any walk**, and **ptbr == 0 is identity** -- both read in `memory_alpha.c` above.
* **`LCA_ISA_BASE + port` is physical by construction**: it is the address `bus_isa_init` registered the devices at.

## 6. QUESTIONS

**Q1 -- PREMISE AUDIT, as questions.**  Is there ANY path on which the nested address is legitimately virtual -- a
guest mapping `0x1d0000000` on purpose?  Does any other device in the tree forward with a missing `PHYSICAL` in the
same way (a sibling of this defect)?  Is the severity MED, or is "the whole ISA window dies once paging is on, with an
unlatched flood" a HIGH for an Alpha machine whose every OS enables paging?

**Q2 -- CHECK THESE CANDIDATE WEAKENINGS** of the proposed fix.  For each, is it EQUIVALENT to the fix, or DIFFERENT --
and at which input do they first differ?  Which rows of §3 would each leave green?
  (a) `PHYSICAL` on the WRITE call only;  (b) on the READ call only;  (c) `NO_EXCEPTIONS | PHYSICAL` on both;
  (d) bare `PHYSICAL` (dropping `CACHE_NONE`) on both;  (e) `PHYSICAL` only when `relative_addr < 0x200`.

**Q3 -- OPTION-SET COMPLETENESS.**  Members I see: (1) the two `PHYSICAL` tokens; (2) translate nothing and call the
target device's handler directly; (3) register the ISA devices at the sparse window itself.  (2) and (3) are
restructurings, not fixes.  Is there a member I did not name, and is (1) the smallest correct one?

**Q4 -- THE WITNESS.**  Does each control prove what its note says?  Is the CONTROL=DEAD guard sufficient (rows 2-7)?
Could the defect rows be red for a reason other than the missing `PHYSICAL` -- e.g. the outer K0SEG access itself
failing after the arm?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
