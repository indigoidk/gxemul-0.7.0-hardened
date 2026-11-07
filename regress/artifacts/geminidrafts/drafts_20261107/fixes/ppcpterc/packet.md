# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcpterc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcpterc`, state `open`, severity `MED`)

**title:** cpus/memory_ppc.c:get_pte_low/ppc_vtp32 -- the hardware table walk never sets the PTE referenced/changed bits -- WRONG-RESULT (guest paging sees stale R/C)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T26 (class WRONG-RESULT; reach U, user mode; effort: medium; report rows: A4-20).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/4f9229ea7b224b4b7108d416d8b89bf12bc91022, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/daa612bde8d1a45d2108088df07f08ab5d4df925.  Our site at de8c7547: src/cpus/memory_ppc.c:131-232; src/cpus/memory_rw.c:745-749.  Portable fix: partial, or an idea only -- port with changes: rs6000 4f9229e, rs6000 daa612b (RW pages must stay read-only in the cache until the first store).  Filing check (TRIAGE.md): only a caution in `mrwstore2`.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port with changes to keep RW pages read-only until first store

## The code at the cited lines

### `src/cpus/memory_ppc.c` around the row's cited line 131 (HEAD 2d25df65, lines 86-176)

```c
   86| 
   87| 	if (flags & FLAG_INSTR)
   88| 		iend = 4;
   89| 	else
   90| 		istart = 4;
   91| 
   92| 	if (cpu->cd.ppc.bits != 32) {
   93| 		fatal("TODO: ppc_bat() for non-32-bit\n");
   94| 		exit(1);
   95| 	}
   96| 	if (cpu->cd.ppc.cpu_type.flags & PPC_601) {
   97| 		fatal("TODO: ppc_bat() for PPC 601\n");
   98| 		exit(1);
   99| 	}
  100| 
  101| 	/*  Base BATs 0-3 (the 4 instruction or the 4 data BATs):  */
  102| 	r = ppc_bat_block(cpu, vaddr, return_paddr, flags, user,
  103| 	    istart, iend, SPR_IBAT0U);
  104| 	if (r != -1)
  105| 		return r;
  106| 
  107| 	/*  #116: extended BATs 4-7 (MPC7445/7455), identical layout at 0x230,
  108| 	    but ONLY when the guest has enabled them via HID0[HIGH_BAT_EN].  This
  109| 	    keeps the aliased DC_ADR/DC_DAT/DC_CST (0x231/0x232/0x238) cache-debug
  110| 	    SPRs from spoofing a BAT on a non-745x guest (Codex+agy consensus).  */
  111| 	/*  #174: (Codex/Fable) also require the modeled CPU to actually
  112| 	    have the extended BATs (PPC_HIGH_BAT capability), so that e.g.
  113| 	    a 603/7400 guest cannot enable them via HID0.  */
  114| 	if ((cpu->cd.ppc.cpu_type.flags & PPC_HIGH_BAT) &&
  115| 	    (cpu->cd.ppc.spr[SPR_HID0] & HID0_HIGH_BAT_EN))
  116| 		return ppc_bat_block(cpu, vaddr, return_paddr, flags, user,
  117| 		    istart, iend, SPR_IBAT4U);
  118| 
  119| 	return -1;
  120| }
  121| 
  122| 
  123| /*
  124|  *  get_pte_low():
  125|  *
  126|  *  Scan a PTE group for a cmp (compare) value.
  127|  *
  128|  *  Returns 1 if the value was found, and *lowp is set to the low PTE word.
  129|  *  Returns 0 if no match was found.
  130|  */
  131| static int get_pte_low(struct cpu *cpu, uint64_t pteg_select,
  132| 	uint32_t *lowp, uint32_t cmp)
  133| {
  134| 	unsigned char *d = memory_paddr_to_hostaddr(cpu->mem, pteg_select, 1);
  135| 	int i;
  136| 
  137| 	for (i=0; i<8; i++) {
  138| 		uint32_t *ep = (uint32_t *) (d + (i << 3)), upper;
  139| 		upper = *ep;
  140| 		upper = BE32_TO_HOST(upper);
  141| 
  142| 		/*  Valid PTE, and correct api and vsid?  */
  143| 		if (upper == cmp) {
  144| 			uint32_t lo = ep[1];
  145| 			lo = BE32_TO_HOST(lo);
  146| 			*lowp = lo;
  147| 			return 1;
  148| 		}
  149| 	}
  150| 
  151| 	return 0;
  152| }
  153| 
  154| 
  155| /*
  156|  *  ppc_vtp32():
  157|  *
  158|  *  Virtual to physical address translation (32-bit mode).
  159|  *
  160|  *  Returns 1 if a translation was found, 0 if none was found. However, finding
  161|  *  a translation does not mean that it should be returned; there can be
  162|  *  a permission violation. *resp is set to 0 for no access, 1 for read-only
  163|  *  access, or 2 for read/write access.
  164|  */
  165| static int ppc_vtp32(struct cpu *cpu, uint32_t vaddr, uint64_t *return_paddr,
  166| 	int *resp, uint64_t msr, int writeflag, int instr)
  167| {
  168| 	int srn = (vaddr >> 28) & 15, api = (vaddr >> 22) & PTE_API;
  169| 	int access, key, match;
  170| 	uint32_t vsid = cpu->cd.ppc.sr[srn] & 0x00ffffff;
  171| 	uint64_t sdr1 = cpu->cd.ppc.spr[SPR_SDR1], htaborg;
  172| 	uint32_t hash1, hash2, pteg_select, tmp;
  173| 	uint32_t lower_pte = 0, cmp;
  174| 
  175| 	htaborg = sdr1 & 0xffff0000UL;
  176| 
```

### `src/cpus/memory_rw.c` around the row's cited line 745 (HEAD 2d25df65, lines 700-790)

```c
  700| 			if (writeflag == MEM_READ) {
  701| 				/*  Return all zeroes? (Or 0xff? TODO)  */
  702| 				memset(data, 0, len);
  703| 
  704| #if 0
  705| /*
  706|  *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|  *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  708|  *  the amount of RAM on some machine.
  709|  *
  710|  *  TODO: Figure out if it is not needed anymore, and remove it completely.
  711|  */
  712| #ifdef MEM_MIPS
  713| 				/*
  714| 				 *  For real data/instruction accesses, cause
  715| 				 *  an exceptions on an illegal read:
  716| 				 */
  717| 				if (cache != CACHE_NONE && !no_exceptions &&
  718| 				    paddr >= mem->physical_max &&
  719| 				    paddr < mem->physical_max+1048576) {
  720| 					mips_cpu_exception(cpu,
  721| 					    EXCEPTION_DBE, 0, vaddr, 0,
  722| 					    0, 0, 0);
  723| 				}
  724| #endif  /*  MEM_MIPS  */
  725| #endif
  726| 			}
  727| 
  728| 			/*  Hm? Shouldn't there be a DBE exception for
  729| 			    invalid writes as well?  TODO  */
  730| 
  731| 			goto do_return_ok;
  732| 		}
  733| 	}
  734| 
  735| 
  736| 	/*
  737| 	 *  Uncached access:
  738| 	 *
  739| 	 *  1)  Translate the physical address to a host address.
  740| 	 *
  741| 	 *  2)  Insert this virtual->physical->host translation into the
  742| 	 *      fast translation arrays (using update_translation_table()).
  743| 	 *
  744| 	 *  3)  If this was a Write, then invalidate any code translations
  745| 	 *      in that page.
  746| 	 */
  747| 	memblock = memory_paddr_to_hostaddr(mem, paddr & ~offset_mask,
  748| 	    writeflag);
  749| 	if (memblock == NULL) {
  750| 		if (writeflag == MEM_READ)
  751| 			memset(data, 0, len);
  752| 		goto do_return_ok;
  753| 	}
  754| 
  755| 	offset = paddr & offset_mask;
  756| 
  757| 	if (cpu->update_translation_table != NULL && !dyntrans_device_danger
  758| #ifdef MEM_MIPS
  759| 	    /*  Ugly hack for R2000/R3000 caches:  */
  760| 	    && (cpu->cd.mips.cpu_type.mmu_model != MMU3K ||
  761|             !(cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & MIPS1_ISOL_CACHES))
  762| #endif
  763| 	    && !(ok & MEMORY_NOT_FULL_PAGE)
  764| 	    && !no_exceptions)
  765| 		cpu->update_translation_table(cpu, vaddr & ~offset_mask,
  766| 		    memblock, (misc_flags & MEMORY_USER_ACCESS) |
  767| 		    (cache == CACHE_INSTRUCTION?
  768| 			(writeflag == MEM_WRITE? 1 : 0) : ok - 1),
  769| 		    paddr & ~offset_mask);
  770| 
  771| 	/*
  772| 	 *  If writing, or if mapping a page where writing is ok later on,
  773| 	 *  then invalidate code translations for the (physical) page address:
  774| 	 */
  775| 
  776| 	if ((writeflag == MEM_WRITE
  777| 	    || (ok == 2 && cache == CACHE_DATA)
  778| 	    ) && cpu->invalidate_code_translation != NULL)
  779| 		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  780| 
  781| 	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  782| 		/*  #165: (Codex/Fable) split accesses that cross a memblock
  783| 		    boundary (e.g. large DMA transfers) at the boundary,
  784| 		    instead of exiting the whole emulator.  */
  785| 		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  786| 		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  787| 
  788| 		if (writeflag == MEM_WRITE)
  789| 			memcpy(memblock + offset, data, len_head);
  790| 		else
```


RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_PPCPTERC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
