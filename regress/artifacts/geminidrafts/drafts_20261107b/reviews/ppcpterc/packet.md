# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppcpterc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppcpterc`, state `open`)

**title:** cpus/memory_ppc.c:get_pte_low/ppc_vtp32 -- the hardware table walk never sets the PTE referenced/changed bits -- WRONG-RESULT (guest paging sees stale R/C)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T26 (class WRONG-RESULT; reach U, user mode; effort: medium; report rows: A4-20).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/4f9229ea7b224b4b7108d416d8b89bf12bc91022, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/daa612bde8d1a45d2108088df07f08ab5d4df925.  Our site at de8c7547: src/cpus/memory_ppc.c:131-232; src/cpus/memory_rw.c:745-749.  Portable fix: partial, or an idea only -- port with changes: rs6000 4f9229e, rs6000 daa612b (RW pages must stay read-only in the cache until the first store).  Filing check (TRIAGE.md): only a caution in `mrwstore2`.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/memory_rw.c:768

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_rw.c b/src/cpus/memory_rw.c
index dd238d07..b34afd57 100644
--- a/src/cpus/memory_rw.c
+++ b/src/cpus/memory_rw.c
@@ -765,7 +765,8 @@ not just the device in question.
 		cpu->update_translation_table(cpu, vaddr & ~offset_mask,
 		    memblock, (misc_flags & MEMORY_USER_ACCESS) |
 		    (cache == CACHE_INSTRUCTION?
-			(writeflag == MEM_WRITE? 1 : 0) : ok - 1),
+			(writeflag == MEM_WRITE? 1 : 0) :
+			(writeflag == MEM_WRITE? ok - 1 : 0)),
 		    paddr & ~offset_mask);
 
 	/*
```

## Every edited function, after the fix

### `src/cpus/memory_rw.c` -- post-edit lines 232-806 (`+` marks a line the diff added or the point of a deletion)

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
  768|+ 			(writeflag == MEM_WRITE? 1 : 0) :
  769|+ 			(writeflag == MEM_WRITE? ok - 1 : 0)),
  770|  		    paddr & ~offset_mask);
  771|  
  772|  	/*
  773|  	 *  If writing, or if mapping a page where writing is ok later on,
  774|  	 *  then invalidate code translations for the (physical) page address:
  775|  	 */
  776|  
  777|  	if ((writeflag == MEM_WRITE
  778|  	    || (ok == 2 && cache == CACHE_DATA)
  779|  	    ) && cpu->invalidate_code_translation != NULL)
  780|  		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  781|  
  782|  	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  783|  		/*  #165: (Codex/Fable) split accesses that cross a memblock
  784|  		    boundary (e.g. large DMA transfers) at the boundary,
  785|  		    instead of exiting the whole emulator.  */
  786|  		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  787|  		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  788|  
  789|  		if (writeflag == MEM_WRITE)
  790|  			memcpy(memblock + offset, data, len_head);
  791|  		else
  792|  			memcpy(data, memblock + offset, len_head);
  793|  
  794|  		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
  795|  		    len - len_head, writeflag, misc_flags);
  796|  	}
  797|  
  798|  	/*  And finally, read or write the data:  */
  799|  	if (writeflag == MEM_WRITE)
  800|  		memcpy(memblock + offset, data, len);
  801|  	else
  802|  		memcpy(data, memblock + offset, len);
  803|  
  804|  do_return_ok:
  805|  	return MEMORY_ACCESS_OK;
  806|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCPTERC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_PPCPTERC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
