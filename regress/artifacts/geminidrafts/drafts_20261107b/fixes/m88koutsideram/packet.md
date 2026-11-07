# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `m88koutsideram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `m88koutsideram`, state `open`)

**title:** cpus/memory_rw.c non-MIPS path beyond RAM -- an 88K access with no RAM or device behind it reads zeros or drops the write instead of raising a bus error -- WRONG-RESULT (SVR4 memory sizing never terminates)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T38 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-33, A1-25).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415, https://github.com/retroprom/gxemul/commit/4e3e72b1.  Our site at de8c7547: src/cpus/memory_rw.c:663-713; src/core/memory.c:598-656.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 02 / upstream 4e3e72b1 outside-RAM part; luna88k/OpenBSD boots must be re-checked.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/memory_rw.c` -- AT HEAD, lines 232-805 (`*` marks a line your previous draft changed)

```c
  232|  {
  233|  	const int offset_mask = MRW_OFFSET_MASK;
  234|  
  235|  	int ok = 2;
  236|  	uint64_t paddr;
     | [... lines 237-584 not shown ...]
  585|  				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
  586|  					bool running_before_device_access = cpu->running;
  587|  					res = mem->devices[i].f(cpu, mem, paddr,
  588|  					    data, len, writeflag,
  589|  					    mem->devices[i].extra);
  590|  
  591|  					if (running_before_device_access && !cpu->running)
  592|  						return MEMORY_ACCESS_FAILED;
  593|  				}
  594|  
  595|  				if (res == 0)
  596|  					res = -1;
  597|  
  598|  				/*
  599|  				 *  If accessing the memory mapped device
  600|  				 *  failed, then return with an exception.
  601|  				 *  (Architecture specific.)
  602|  				 */
  603|  				if (res <= 0 && !no_exceptions) {
  604|  					debug("[ %s device '%s' addr %08lx "
  605|  					    "failed ]\n", writeflag?
  606|  					    "writing to" : "reading from",
  607|  					    mem->devices[i].name, (long)paddr);
  608|  #ifdef MEM_MIPS
  609|  					mips_cpu_exception(cpu,
  610|  					    cache == CACHE_INSTRUCTION?
  611|  					    EXCEPTION_IBE : EXCEPTION_DBE,
  612|  					    0, vaddr, 0, 0, 0, 0);
  613|  #endif
  614|  #ifdef MEM_M88K
  615|  					/*  #570: record the bus error in the faulting side's
  616|  					    CMMU first: PFSR = BERROR << 16 (the field
  617|  					    OpenBSD/mvme88k's trap.c extracts) and PFAR =
  618|  					    orig_paddr, the PHYSICAL address saved before paddr
  619|  					    was made device-relative.  cmmu[0] is the instruction
  620|  					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621|  					    the other CMMU is not written.  For a CPU without a
  622|  					    CMMU, this arm makes no register write; the exception
  623|  					    call is unchanged.  `null route` scores data-access
  624|  					    delivery; instruction-access delivery is unscored
  625|  					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626|  					    callers (e.g. the debugger's dump) never get here:
  627|  					    the test above keeps them out.  */
  628|  					{
  629|  						struct m8820x_cmmu *cmmu =
  630|  						    cpu->cd.m88k.cmmu[cache ==
  631|  						    CACHE_INSTRUCTION ? 0 : 1];
  632|  						if (cmmu != NULL) {
  633|  							cmmu->reg[CMMU_PFSR] =
  634|  							    CMMU_PFSR_BERROR << 16;
  635|  							cmmu->reg[CMMU_PFAR] =
  636|  							    (uint32_t) orig_paddr;
  637|  						}
  638|  					}
  639|  					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640|  					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641|  					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642|  #endif
  643|  					return MEMORY_ACCESS_FAILED;
  644|  				}
  645|  				goto do_return_ok;
  646|  			}
  647|  
  648|  			if (paddr < mem->devices[i].baseaddr)
  649|  				end = i - 1;
  650|  			if (paddr >= mem->devices[i].endaddr)
  651|  				start = i + 1;
  652|  			i = (start + end) >> 1;
  653|  		} while (start <= end);
  654|  	}
  655|  
  656|  
  657|  #ifdef MEM_MIPS
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
  695|* 			if (paddr >= mem->physical_max && !no_exceptions)
  696|* 				if (memory_warn_about_unimplemented_addr
  697|  				    (cpu, mem, writeflag, paddr, len))
  698|  					return MEMORY_ACCESS_FAILED;
  699|* 
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
     | [... lines 760-775 not shown ...]
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
    "old": "\t\t\tif (paddr >= mem->physical_max && !no_exceptions)\n\t\t\t\tif (memory_warn_about_unimplemented_addr\n\t\t\t\t    (cpu, mem, writeflag, paddr, len))\n\t\t\t\t\treturn MEMORY_ACCESS_FAILED;",
    "new": "\t\t\tif (paddr >= mem->physical_max && !no_exceptions) {\n\t\t\t\tmemory_warn_about_unimplemented_addr\n\t\t\t\t    (cpu, mem, writeflag, paddr, len);\n\t\t\t\t/* #T38: decouple access failure from log verbosity to fix SVR4 memory sizing */\n\t\t\t\treturn MEMORY_ACCESS_FAILED;\n\t\t\t}",
    "why": "Unconditionally fail accesses outside RAM to ensure the CPU raises a bus error, rather than linking structural failure to log verbosity."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_M88KOUTSIDERAM: DEFECT, 3 FINDINGS
1. **Does the diff remove the defect at every site the issue names?**
   No. The issue explicitly names two sites: `src/cpus/memory_rw.c:663-713` and `src/core/memory.c:598-656`. The proposed diff only modifies `src/cpus/memory_rw.c` and completely misses the required fix in `src/core/memory.c`.
2. **CONTROL FLOW:**
   Yes, the added `return MEMORY_ACCESS_FAILED;` at `src/cpus/memory_rw.c:701` acts as an early exit. It skips the block that hands the guest an unwritten read result: `memset(data, 0, len);` and its corresponding `goto do_return_ok;`. It therefore skips the function's common tail at line 808-809: `do_return_ok: return MEMORY_ACCESS_OK;`.
3. **RETURN VALUE:**
   Yes, on the non-MIPS out-of-bounds RAM path, the function now returns `MEMORY_ACCESS_FAILED` instead of `MEMORY_ACCESS_OK`. Based on the context of the function (e.g., device access failure at line 643), returning this value implies the memory transaction was invalid, aborted, and cannot be fulfilled. 
4. **What ELSE does the diff change?**
   By returning early without manually raising the architecture-specific exception, the fix actually fails to generate the required 88K bus error state. Unlike the memory-mapped device failure path (which explicitly sets `CMMU_PFSR`, `CMMU_PFAR`, and calls `m88k_exception(...)` before returning `MEMORY_ACCESS_FAILED` at lines 614-644), this new early return silently drops the access. It leaves the guest without the bus error (or the CMMU fault registers) that the SVR4 memory sizing relies on.
5. **House idioms:**
   The new comment introduced in the diff at line 700 uses an invalid tag `/* #1: ... */`. House idioms dictate this should carry a `/* #NNN: ... */` tag corresponding to the issue, such as `/* #m88koutsideram: ... */`.
**Findings:**
`src/core/memory.c:UNSETTLED`, DEFECT, Apply the out-of-bounds memory fix to this missing file.
`src/cpus/memory_rw.c:701`, DEFECT, Explicitly call `m88k_exception` and set the CMMU fault registers before returning `MEMORY_ACCESS_FAILED`.
`src/cpus/memory_rw.c:700`, STYLE, Change `/* #1: non-MIPS memory sizing expects a bus error */` to use the correct issue identifier tag.
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

End with two lines: `REVISION_M88KOUTSIDERAM: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_M88KOUTSIDERAM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
