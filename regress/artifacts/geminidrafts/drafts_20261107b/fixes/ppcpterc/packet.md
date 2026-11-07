# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppcpterc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppcpterc`, state `open`)

**title:** cpus/memory_ppc.c:get_pte_low/ppc_vtp32 -- the hardware table walk never sets the PTE referenced/changed bits -- WRONG-RESULT (guest paging sees stale R/C)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T26 (class WRONG-RESULT; reach U, user mode; effort: medium; report rows: A4-20).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/4f9229ea7b224b4b7108d416d8b89bf12bc91022, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/daa612bde8d1a45d2108088df07f08ab5d4df925.  Our site at de8c7547: src/cpus/memory_ppc.c:131-232; src/cpus/memory_rw.c:745-749.  Portable fix: partial, or an idea only -- port with changes: rs6000 4f9229e, rs6000 daa612b (RW pages must stay read-only in the cache until the first store).  Filing check (TRIAGE.md): only a caution in `mrwstore2`.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/memory_rw.c` -- AT HEAD, lines 232-805 (`*` marks a line your previous draft changed)

```c
  232|  {
  233|  	const int offset_mask = MRW_OFFSET_MASK;
  234|  
  235|  	int ok = 2;
  236|  	uint64_t paddr;
     | [... lines 237-657 not shown ...]
  658|  	/*
  659|  	 *  Data and instruction cache emulation:
  660|  	 */
  661|  
  662|  	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663|  	case MMU3K:
  664|  		/*  if not uncached addess  (TODO: generalize this)  */
  665|  		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666|  		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667|  		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668|  			if (memory_cache_R3000(cpu, cache, paddr,
  669|  			    writeflag, len, data))
  670|  				goto do_return_ok;
  671|  		}
  672|  		break;
  673|  	default:
  674|  		/*  R4000 etc  */
  675|  		/*  TODO  */
  676|  		;
  677|  	}
  678|  #endif	/*  MEM_MIPS  */
  679|  
  680|  
  681|  	/*  Outside of physical RAM?  */
  682|  	if (paddr >= mem->physical_max) {
  683|  #ifdef MEM_MIPS
  684|  		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685|  			/*  Ok, this is PROM stuff  */
  686|  		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687|  			/*  Sprite reads from this area of memory...  */
  688|  			/*  TODO: is this still correct?  */
  689|  			if (writeflag == MEM_READ)
  690|  				memset(data, 0, len);
  691|  			goto do_return_ok;
  692|  		} else
  693|  #endif /* MIPS */
  694|  		{
  695|  			if (paddr >= mem->physical_max && !no_exceptions)
  696|  				if (memory_warn_about_unimplemented_addr
  697|  				    (cpu, mem, writeflag, paddr, len))
  698|  					return MEMORY_ACCESS_FAILED;
  699|  
  700|  			if (writeflag == MEM_READ) {
  701|  				/*  Return all zeroes? (Or 0xff? TODO)  */
  702|  				memset(data, 0, len);
  703|  
  704|  #if 0
  705|  /*
  706|   *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|   *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  708|   *  the amount of RAM on some machine.
  709|   *
  710|   *  TODO: Figure out if it is not needed anymore, and remove it completely.
  711|   */
  712|  #ifdef MEM_MIPS
  713|  				/*
  714|  				 *  For real data/instruction accesses, cause
  715|  				 *  an exceptions on an illegal read:
  716|  				 */
  717|  				if (cache != CACHE_NONE && !no_exceptions &&
  718|  				    paddr >= mem->physical_max &&
  719|  				    paddr < mem->physical_max+1048576) {
  720|  					mips_cpu_exception(cpu,
  721|  					    EXCEPTION_DBE, 0, vaddr, 0,
  722|  					    0, 0, 0);
  723|  				}
  724|  #endif  /*  MEM_MIPS  */
  725|  #endif
  726|  			}
  727|  
  728|  			/*  Hm? Shouldn't there be a DBE exception for
  729|  			    invalid writes as well?  TODO  */
  730|  
  731|  			goto do_return_ok;
  732|  		}
  733|  	}
  734|  
  735|  
  736|  	/*
  737|  	 *  Uncached access:
  738|  	 *
  739|  	 *  1)  Translate the physical address to a host address.
  740|  	 *
  741|  	 *  2)  Insert this virtual->physical->host translation into the
  742|  	 *      fast translation arrays (using update_translation_table()).
  743|  	 *
  744|  	 *  3)  If this was a Write, then invalidate any code translations
  745|  	 *      in that page.
  746|  	 */
  747|  	memblock = memory_paddr_to_hostaddr(mem, paddr & ~offset_mask,
  748|  	    writeflag);
  749|  	if (memblock == NULL) {
  750|  		if (writeflag == MEM_READ)
  751|  			memset(data, 0, len);
  752|  		goto do_return_ok;
  753|  	}
  754|  
  755|  	offset = paddr & offset_mask;
  756|  
  757|  	if (cpu->update_translation_table != NULL && !dyntrans_device_danger
  758|  #ifdef MEM_MIPS
  759|  	    /*  Ugly hack for R2000/R3000 caches:  */
  760|  	    && (cpu->cd.mips.cpu_type.mmu_model != MMU3K ||
  761|              !(cpu->cd.mips.coproc[0]->reg[COP0_STATUS] & MIPS1_ISOL_CACHES))
  762|  #endif
  763|  	    && !(ok & MEMORY_NOT_FULL_PAGE)
  764|  	    && !no_exceptions)
  765|  		cpu->update_translation_table(cpu, vaddr & ~offset_mask,
  766|  		    memblock, (misc_flags & MEMORY_USER_ACCESS) |
  767|  		    (cache == CACHE_INSTRUCTION?
  768|* 			(writeflag == MEM_WRITE? 1 : 0) : ok - 1),
  769|* 		    paddr & ~offset_mask);
  770|  
  771|  	/*
  772|  	 *  If writing, or if mapping a page where writing is ok later on,
  773|  	 *  then invalidate code translations for the (physical) page address:
  774|  	 */
  775|  
  776|  	if ((writeflag == MEM_WRITE
  777|  	    || (ok == 2 && cache == CACHE_DATA)
  778|  	    ) && cpu->invalidate_code_translation != NULL)
  779|  		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  780|  
  781|  	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  782|  		/*  #165: (Codex/Fable) split accesses that cross a memblock
  783|  		    boundary (e.g. large DMA transfers) at the boundary,
  784|  		    instead of exiting the whole emulator.  */
  785|  		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  786|  		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  787|  
  788|  		if (writeflag == MEM_WRITE)
  789|  			memcpy(memblock + offset, data, len_head);
  790|  		else
  791|  			memcpy(data, memblock + offset, len_head);
  792|  
  793|  		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
  794|  		    len - len_head, writeflag, misc_flags);
  795|  	}
  796|  
  797|  	/*  And finally, read or write the data:  */
  798|  	if (writeflag == MEM_WRITE)
  799|  		memcpy(memblock + offset, data, len);
  800|  	else
  801|  		memcpy(data, memblock + offset, len);
  802|  
  803|  do_return_ok:
  804|  	return MEMORY_ACCESS_OK;
  805|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/memory_rw.c",
    "old": "\t\t    (cache == CACHE_INSTRUCTION?\n\t\t\t(writeflag == MEM_WRITE? 1 : 0) : ok - 1),\n\t\t    paddr & ~offset_mask);",
    "new": "\t\t    (cache == CACHE_INSTRUCTION?\n\t\t\t(writeflag == MEM_WRITE? 1 : 0) : (writeflag == MEM_WRITE? ok - 1 : 0)),\n\t\t    paddr & ~offset_mask);",
    "why": "Keep RW pages read-only in the cache until the first actual store, forcing writes to trap so PTE Changed bits can be updated."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCPTERC: DEFECT, 2 FINDINGS
1. The diff does NOT remove the defect at every site named. The issue explicitly lists `src/cpus/memory_ppc.c:131-232` as a site needing a fix (for the hardware table walk), but the diff completely omits this file and only edits `src/cpus/memory_rw.c`.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit. The diff strictly changes an argument in a function call and does not skip the common tail.
3. RETURN VALUE: No path returns anything different. The return paths and values (`MEMORY_ACCESS_OK`, `MEMORY_RW(...)`) remain unchanged.
4. ELSE changed: By passing `0` instead of `ok - 1` when `writeflag != MEM_WRITE`, the cache mapping for reads will lack write permissions even if the page is writable. This forces subsequent writes to trap back into the core (which is the intended mechanism to allow updating the Changed/Referenced bits), but it restricts cache access.
5. House idioms: The newly modified line 768 exceeds the 79-column limit.
**Findings:**
`src/cpus/memory_ppc.c:131`: DEFECT - Site missed entirely. The hardware table walk R/C bit updates are not fixed. Fix: Implement the corresponding fix in `src/cpus/memory_ppc.c`.
`src/cpus/memory_rw.c:768`: STYLE - Line exceeds 79 columns. Fix: `(writeflag == MEM_WRITE ? 1 : 0) : \n (writeflag == MEM_WRITE ? ok - 1 : 0)),`
FIXREVIEW_PPCPTERC: DEFECT, 2 FINDINGS
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_PPCPTERC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCPTERC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
