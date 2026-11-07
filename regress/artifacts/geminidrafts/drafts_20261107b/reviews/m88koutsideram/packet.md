# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `m88koutsideram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `m88koutsideram`, state `open`)

**title:** cpus/memory_rw.c non-MIPS path beyond RAM -- an 88K access with no RAM or device behind it reads zeros or drops the write instead of raising a bus error -- WRONG-RESULT (SVR4 memory sizing never terminates)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T38 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-33, A1-25).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415, https://github.com/retroprom/gxemul/commit/4e3e72b1.  Our site at de8c7547: src/cpus/memory_rw.c:663-713; src/core/memory.c:598-656.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 02 / upstream 4e3e72b1 outside-RAM part; luna88k/OpenBSD boots must be re-checked.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/memory_rw.c:695-698` (the previous draft's unconditional `return MEMORY_ACCESS_FAILED;` drops the access without raising the required M88K exception).

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_rw.c b/src/cpus/memory_rw.c
index dd238d07..4ea5437d 100644
--- a/src/cpus/memory_rw.c
+++ b/src/cpus/memory_rw.c
@@ -692,10 +692,28 @@ not just the device in question.
 		} else
 #endif /* MIPS */
 		{
-			if (paddr >= mem->physical_max && !no_exceptions)
-				if (memory_warn_about_unimplemented_addr
-				    (cpu, mem, writeflag, paddr, len))
-					return MEMORY_ACCESS_FAILED;
+			if (paddr >= mem->physical_max && !no_exceptions) {
+				memory_warn_about_unimplemented_addr
+				    (cpu, mem, writeflag, paddr, len);
+#ifdef MEM_M88K
+				/* #m88koutsideram: 88K access beyond RAM must raise a bus error for SVR4 sizing */
+				{
+					struct m8820x_cmmu *cmmu =
+					    cpu->cd.m88k.cmmu[cache ==
+					    CACHE_INSTRUCTION ? 0 : 1];
+					if (cmmu != NULL) {
+						cmmu->reg[CMMU_PFSR] =
+						    CMMU_PFSR_BERROR << 16;
+						cmmu->reg[CMMU_PFAR] =
+						    (uint32_t) paddr;
+					}
+				}
+				m88k_exception(cpu, cache == CACHE_INSTRUCTION
+				    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
+				    : M88K_EXCEPTION_DATA_ACCESS, 0);
+#endif
+				return MEMORY_ACCESS_FAILED;
+			}
 
 			if (writeflag == MEM_READ) {
 				/*  Return all zeroes? (Or 0xff? TODO)  */
```

## Every edited function, after the fix

### `src/cpus/memory_rw.c` -- post-edit lines 232-823 (`+` marks a line the diff added or the point of a deletion)

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
  695|+ 			if (paddr >= mem->physical_max && !no_exceptions) {
  696|+ 				memory_warn_about_unimplemented_addr
  697|+ 				    (cpu, mem, writeflag, paddr, len);
  698|+ #ifdef MEM_M88K
  699|+ 				/* #m88koutsideram: 88K access beyond RAM must raise a bus error for SVR4 sizing */
  700|+ 				{
  701|+ 					struct m8820x_cmmu *cmmu =
  702|+ 					    cpu->cd.m88k.cmmu[cache ==
  703|+ 					    CACHE_INSTRUCTION ? 0 : 1];
  704|+ 					if (cmmu != NULL) {
  705|+ 						cmmu->reg[CMMU_PFSR] =
  706|+ 						    CMMU_PFSR_BERROR << 16;
  707|+ 						cmmu->reg[CMMU_PFAR] =
  708|+ 						    (uint32_t) paddr;
  709|+ 					}
  710|+ 				}
  711|+ 				m88k_exception(cpu, cache == CACHE_INSTRUCTION
  712|+ 				    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  713|+ 				    : M88K_EXCEPTION_DATA_ACCESS, 0);
  714|+ #endif
  715|+ 				return MEMORY_ACCESS_FAILED;
  716|+ 			}
  717|  
  718|  			if (writeflag == MEM_READ) {
  719|  				/*  Return all zeroes? (Or 0xff? TODO)  */
  720|  				memset(data, 0, len);
  721|  
  722|  #if 0
  723|  /*
  724|   *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  725|   *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  726|   *  the amount of RAM on some machine.
  727|   *
  728|   *  TODO: Figure out if it is not needed anymore, and remove it completely.
  729|   */
  730|  #ifdef MEM_MIPS
  731|  				/*
  732|  				 *  For real data/instruction accesses, cause
  733|  				 *  an exceptions on an illegal read:
  734|  				 */
  735|  				if (cache != CACHE_NONE && !no_exceptions &&
  736|  				    paddr >= mem->physical_max &&
  737|  				    paddr < mem->physical_max+1048576) {
  738|  					mips_cpu_exception(cpu,
  739|  					    EXCEPTION_DBE, 0, vaddr, 0,
  740|  					    0, 0, 0);
  741|  				}
  742|  #endif  /*  MEM_MIPS  */
  743|  #endif
  744|  			}
  745|  
  746|  			/*  Hm? Shouldn't there be a DBE exception for
  747|  			    invalid writes as well?  TODO  */
  748|  
  749|  			goto do_return_ok;
  750|  		}
  751|  	}
  752|  
  753|  
  754|  	/*
  755|  	 *  Uncached access:
  756|  	 *
  757|  	 *  1)  Translate the physical address to a host address.
  758|  	 *
  759|  	 *  2)  Insert this virtual->physical->host translation into the
  760|  	 *      fast translation arrays (using update_translation_table()).
  761|  	 *
  762|  	 *  3)  If this was a Write, then invalidate any code translations
  763|  	 *      in that page.
  764|  	 */
  765|  	memblock = memory_paddr_to_hostaddr(mem, paddr & ~offset_mask,
  766|  	    writeflag);
  767|  	if (memblock == NULL) {
  768|  		if (writeflag == MEM_READ)
  769|  			memset(data, 0, len);
  770|  		goto do_return_ok;
  771|  	}
  772|  
  773|  	offset = paddr & offset_mask;
  774|  
  775|  	if (cpu->update_translation_table != NULL && !dyntrans_device_danger
  776|  #ifdef MEM_MIPS
     | [... lines 777-793 not shown ...]
  794|  	if ((writeflag == MEM_WRITE
  795|  	    || (ok == 2 && cache == CACHE_DATA)
  796|  	    ) && cpu->invalidate_code_translation != NULL)
  797|  		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  798|  
  799|  	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  800|  		/*  #165: (Codex/Fable) split accesses that cross a memblock
  801|  		    boundary (e.g. large DMA transfers) at the boundary,
  802|  		    instead of exiting the whole emulator.  */
  803|  		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  804|  		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  805|  
  806|  		if (writeflag == MEM_WRITE)
  807|  			memcpy(memblock + offset, data, len_head);
  808|  		else
  809|  			memcpy(data, memblock + offset, len_head);
  810|  
  811|  		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
  812|  		    len - len_head, writeflag, misc_flags);
  813|  	}
  814|  
  815|  	/*  And finally, read or write the data:  */
  816|  	if (writeflag == MEM_WRITE)
  817|  		memcpy(memblock + offset, data, len);
  818|  	else
  819|  		memcpy(data, memblock + offset, len);
  820|  
  821|  do_return_ok:
  822|  	return MEMORY_ACCESS_OK;
  823|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_M88KOUTSIDERAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_M88KOUTSIDERAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
