# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipssubpageram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipssubpageram`, state `open`)

**title:** cpus/memory_rw.c MIPS PROM-area fallthrough + devices/dev_mc146818.c init -- sub-page devices in the 0x1fc00000 window (KN02 RTC 0x100 bytes, DZ 0x80 bytes): one access past the registers maps the whole page as RAM and later accesses bypass the device -- WRONG-RESULT (device silently disconnected; NVRAM stores lost)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T37 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-66, A(c)#8).  Source URLs: https://github.com/rpajarola/gxemul/commit/e37235e61de104fc7402793e6bba9fdd7aeb2607.  Our site at de8c7547: src/cpus/memory_rw.c:662-667, :738-750; src/devices/dev_mc146818.c:671-682; src/include/devices.h:167.  Portable fix: yes -- port rpajarola e37235e (register the whole page) or fix the PROM-area fallthrough.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/cpus/memory_rw.c:686`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_rw.c b/src/cpus/memory_rw.c
index dd238d07..2e837527 100644
--- a/src/cpus/memory_rw.c
+++ b/src/cpus/memory_rw.c
@@ -683,6 +683,9 @@ not just the device in question.
 #ifdef MEM_MIPS
 		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
 			/*  Ok, this is PROM stuff  */
+			if (writeflag == MEM_READ)
+				memset(data, 0, len);
+			goto do_return_ok;
 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
 			/*  Sprite reads from this area of memory...  */
 			/*  TODO: is this still correct?  */
```

## Every edited function, after the fix

### `src/cpus/memory_rw.c` -- post-edit lines 232-808 (`+` marks a line the diff added or the point of a deletion)

```c
  232|  {
  233|  	const int offset_mask = MRW_OFFSET_MASK;
  234|  
  235|  	int ok = 2;
  236|  	uint64_t paddr;
     | [... lines 237-575 not shown ...]
  576|  					if (host_addr != NULL)
  577|  						cpu->update_translation_table(
  578|  						    cpu, vaddr & ~offset_mask,
  579|  						    host_addr, wf,
  580|  						    orig_paddr & ~offset_mask);
  581|  				}
  582|  
  583|  				res = 0;
  584|  				if (!no_exceptions || (mem->devices[i].flags &
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
  686|+ 			if (writeflag == MEM_READ)
  687|+ 				memset(data, 0, len);
  688|+ 			goto do_return_ok;
  689|  		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  690|  			/*  Sprite reads from this area of memory...  */
  691|  			/*  TODO: is this still correct?  */
  692|  			if (writeflag == MEM_READ)
  693|  				memset(data, 0, len);
  694|  			goto do_return_ok;
  695|  		} else
  696|  #endif /* MIPS */
  697|  		{
  698|  			if (paddr >= mem->physical_max && !no_exceptions)
  699|  				if (memory_warn_about_unimplemented_addr
  700|  				    (cpu, mem, writeflag, paddr, len))
  701|  					return MEMORY_ACCESS_FAILED;
  702|  
  703|  			if (writeflag == MEM_READ) {
  704|  				/*  Return all zeroes? (Or 0xff? TODO)  */
  705|  				memset(data, 0, len);
  706|  
  707|  #if 0
  708|  /*
  709|   *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  710|   *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  711|   *  the amount of RAM on some machine.
  712|   *
  713|   *  TODO: Figure out if it is not needed anymore, and remove it completely.
  714|   */
  715|  #ifdef MEM_MIPS
  716|  				/*
  717|  				 *  For real data/instruction accesses, cause
  718|  				 *  an exceptions on an illegal read:
  719|  				 */
  720|  				if (cache != CACHE_NONE && !no_exceptions &&
  721|  				    paddr >= mem->physical_max &&
  722|  				    paddr < mem->physical_max+1048576) {
  723|  					mips_cpu_exception(cpu,
  724|  					    EXCEPTION_DBE, 0, vaddr, 0,
  725|  					    0, 0, 0);
  726|  				}
  727|  #endif  /*  MEM_MIPS  */
  728|  #endif
  729|  			}
  730|  
  731|  			/*  Hm? Shouldn't there be a DBE exception for
  732|  			    invalid writes as well?  TODO  */
  733|  
  734|  			goto do_return_ok;
  735|  		}
  736|  	}
  737|  
  738|  
  739|  	/*
  740|  	 *  Uncached access:
  741|  	 *
  742|  	 *  1)  Translate the physical address to a host address.
  743|  	 *
  744|  	 *  2)  Insert this virtual->physical->host translation into the
  745|  	 *      fast translation arrays (using update_translation_table()).
  746|  	 *
  747|  	 *  3)  If this was a Write, then invalidate any code translations
  748|  	 *      in that page.
     | [... lines 749-778 not shown ...]
  779|  	if ((writeflag == MEM_WRITE
  780|  	    || (ok == 2 && cache == CACHE_DATA)
  781|  	    ) && cpu->invalidate_code_translation != NULL)
  782|  		cpu->invalidate_code_translation(cpu, paddr, INVALIDATE_PADDR);
  783|  
  784|  	if ((paddr&((1<<BITS_PER_MEMBLOCK)-1)) + len > (1<<BITS_PER_MEMBLOCK)) {
  785|  		/*  #165: (Codex/Fable) split accesses that cross a memblock
  786|  		    boundary (e.g. large DMA transfers) at the boundary,
  787|  		    instead of exiting the whole emulator.  */
  788|  		size_t len_head = (size_t) ((1<<BITS_PER_MEMBLOCK) -
  789|  		    (paddr & ((1<<BITS_PER_MEMBLOCK)-1)));
  790|  
  791|  		if (writeflag == MEM_WRITE)
  792|  			memcpy(memblock + offset, data, len_head);
  793|  		else
  794|  			memcpy(data, memblock + offset, len_head);
  795|  
  796|  		return MEMORY_RW(cpu, mem, vaddr + len_head, data + len_head,
  797|  		    len - len_head, writeflag, misc_flags);
  798|  	}
  799|  
  800|  	/*  And finally, read or write the data:  */
  801|  	if (writeflag == MEM_WRITE)
  802|  		memcpy(memblock + offset, data, len);
  803|  	else
  804|  		memcpy(data, memblock + offset, len);
  805|  
  806|  do_return_ok:
  807|  	return MEMORY_ACCESS_OK;
  808|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSSUBPAGERAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSSUBPAGERAM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_MIPSSUBPAGERAM: UNSETTLED, 1 FINDINGS
1. The diff successfully removes the defect by implementing the alternative fix option ("fix the PROM-area fallthrough"). However, it misses the other sites explicitly named in the issue: `src/devices/dev_mc146818.c` and `src/include/devices.h`.
2. CONTROL FLOW: Yes, the added `goto do_return_ok;` at `src/cpus/memory_rw.c:688` skips the block that maps uncached memory as RAM. It skips the common tail line: `804| memcpy(data, memblock + offset, len);`. It does not hand the guest an unwritten result because it explicitly zeroes `data` using `memset(data, 0, len);` before jumping.
3. RETURN VALUE: No, the path continues to return `MEMORY_ACCESS_OK` (via the `do_return_ok` label at line 806). This value implies the memory access was processed successfully and should not trigger a hardware exception.
4. What ELSE: Beyond preventing the erroneous RAM mapping, the diff alters the guest's view by explicitly feeding it zeroes for unmapped PROM addresses (instead of uninitialized or previously mapped RAM data). Additionally, writes to this region are now silently discarded.
5. House idioms: No style or idiom violations were found; the new code fits within 79 columns and doesn't introduce repeated diagnostics.
`src/devices/dev_mc146818.c:?` QUESTION UNSETTLED; missing file `src/devices/dev_mc146818.c` to definitively verify if device-level page registration changes are still needed despite the PROM fallthrough fix.
```

### `src/include/thirdparty/dec_prom.h` lines 154-170 (where HEAD defines `memcpy`)

```c
  154| 	void	(*_rex) __P((char cmd));				/* ac */
  155| 	/* b0 to d4 reserved */
  156| };
  157| 
  158| extern const struct callback *callv;
  159| extern const struct callback callvec;
  160| 
  161| #if defined(_STANDALONE) && !defined(_NO_PROM_DEFINES)
  162| #define memcpy (*callv -> _memcpy)
  163| #define memset (*callv -> _memset)
  164| #define strcat (*callv -> _strcat)
  165| #define strcmp (*callv -> _strcmp)
  166| #define strcpy (*callv -> _strcpy)
  167| #define strlen (*callv -> _strlen)
  168| #define strncat (*callv -> _strncat)
  169| #define strncpy (*callv -> _strncpy)
  170| #define strncmp (*callv -> _strncmp)
```

### `src/include/thirdparty/dec_prom.h` lines 155-171 (where HEAD defines `memset`)

```c
  155| 	/* b0 to d4 reserved */
  156| };
  157| 
  158| extern const struct callback *callv;
  159| extern const struct callback callvec;
  160| 
  161| #if defined(_STANDALONE) && !defined(_NO_PROM_DEFINES)
  162| #define memcpy (*callv -> _memcpy)
  163| #define memset (*callv -> _memset)
  164| #define strcat (*callv -> _strcat)
  165| #define strcmp (*callv -> _strcmp)
  166| #define strcpy (*callv -> _strcpy)
  167| #define strlen (*callv -> _strlen)
  168| #define strncat (*callv -> _strncat)
  169| #define strncpy (*callv -> _strncpy)
  170| #define strncmp (*callv -> _strncmp)
  171| #define getchar (*callv -> _getchar)
```

### `src/include/memory.h` lines 134-150 (where HEAD defines `MEMORY_ACCESS_OK`)

```c
  134| #define	DM_READS_HAVE_NO_SIDE_EFFECTS		4
  135| #define	DM_EMULATED_RAM				8
  136| 
  137| #define FLAG_WRITEFLAG          1
  138| #define FLAG_NOEXCEPTIONS       2
  139| #define FLAG_INSTR              4
  140| 
  141| #define	MEMORY_ACCESS_FAILED		0
  142| #define	MEMORY_ACCESS_OK		1
  143| #define	MEMORY_ACCESS_OK_WRITE		2
  144| #define	MEMORY_NOT_FULL_PAGE		256
  145| 
  146| void memory_device_dyntrans_access(struct cpu *, struct memory *mem,
  147| 	void *extra, uint64_t *low, uint64_t *high);
  148| 
  149| #define DEVICE_ACCESS(x)	int dev_ ## x ## _access(struct cpu *cpu, \
  150| 	struct memory *mem, uint64_t relative_addr, unsigned char *data,  \
```

Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
