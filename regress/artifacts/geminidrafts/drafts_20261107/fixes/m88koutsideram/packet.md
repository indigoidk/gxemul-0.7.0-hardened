# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88koutsideram` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88koutsideram`, state `open`, severity `MED`)

**title:** cpus/memory_rw.c non-MIPS path beyond RAM -- an 88K access with no RAM or device behind it reads zeros or drops the write instead of raising a bus error -- WRONG-RESULT (SVR4 memory sizing never terminates)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T38 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-33, A1-25).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415, https://github.com/retroprom/gxemul/commit/4e3e72b1.  Our site at de8c7547: src/cpus/memory_rw.c:663-713; src/core/memory.c:598-656.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 02 / upstream 4e3e72b1 outside-RAM part; luna88k/OpenBSD boots must be re-checked.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 02 / upstream 4e3e72b1

## The code at the cited lines

### `src/cpus/memory_rw.c` around the row's cited line 663 (HEAD d2a6f233, lines 618-708)

```c
  618| 					    orig_paddr, the PHYSICAL address saved before paddr
  619| 					    was made device-relative.  cmmu[0] is the instruction
  620| 					    CMMU, cmmu[1] the data CMMU (memory_m88k.c's index);
  621| 					    the other CMMU is not written.  For a CPU without a
  622| 					    CMMU, this arm makes no register write; the exception
  623| 					    call is unchanged.  `null route` scores data-access
  624| 					    delivery; instruction-access delivery is unscored
  625| 					    (`null surv` scores survival only).  NO_EXCEPTIONS
  626| 					    callers (e.g. the debugger's dump) never get here:
  627| 					    the test above keeps them out.  */
  628| 					{
  629| 						struct m8820x_cmmu *cmmu =
  630| 						    cpu->cd.m88k.cmmu[cache ==
  631| 						    CACHE_INSTRUCTION ? 0 : 1];
  632| 						if (cmmu != NULL) {
  633| 							cmmu->reg[CMMU_PFSR] =
  634| 							    CMMU_PFSR_BERROR << 16;
  635| 							cmmu->reg[CMMU_PFAR] =
  636| 							    (uint32_t) orig_paddr;
  637| 						}
  638| 					}
  639| 					m88k_exception(cpu, cache == CACHE_INSTRUCTION
  640| 					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
  641| 					    : M88K_EXCEPTION_DATA_ACCESS, 0);
  642| #endif
  643| 					return MEMORY_ACCESS_FAILED;
  644| 				}
  645| 				goto do_return_ok;
  646| 			}
  647| 
  648| 			if (paddr < mem->devices[i].baseaddr)
  649| 				end = i - 1;
  650| 			if (paddr >= mem->devices[i].endaddr)
  651| 				start = i + 1;
  652| 			i = (start + end) >> 1;
  653| 		} while (start <= end);
  654| 	}
  655| 
  656| 
  657| #ifdef MEM_MIPS
  658| 	/*
  659| 	 *  Data and instruction cache emulation:
  660| 	 */
  661| 
  662| 	switch (cpu->cd.mips.cpu_type.mmu_model) {
  663| 	case MMU3K:
  664| 		/*  if not uncached addess  (TODO: generalize this)  */
  665| 		if (!(misc_flags & PHYSICAL) && cache != CACHE_NONE &&
  666| 		    !((vaddr & 0xffffffffULL) >= 0xa0000000ULL &&
  667| 		      (vaddr & 0xffffffffULL) <= 0xbfffffffULL)) {
  668| 			if (memory_cache_R3000(cpu, cache, paddr,
  669| 			    writeflag, len, data))
  670| 				goto do_return_ok;
  671| 		}
  672| 		break;
  673| 	default:
  674| 		/*  R4000 etc  */
  675| 		/*  TODO  */
  676| 		;
  677| 	}
  678| #endif	/*  MEM_MIPS  */
  679| 
  680| 
  681| 	/*  Outside of physical RAM?  */
  682| 	if (paddr >= mem->physical_max) {
  683| #ifdef MEM_MIPS
  684| 		if ((paddr & 0xffffc00000ULL) == 0x1fc00000) {
  685| 			/*  Ok, this is PROM stuff  */
  686| 		} else if ((paddr & 0xfffff00000ULL) == 0x1ff00000) {
  687| 			/*  Sprite reads from this area of memory...  */
  688| 			/*  TODO: is this still correct?  */
  689| 			if (writeflag == MEM_READ)
  690| 				memset(data, 0, len);
  691| 			goto do_return_ok;
  692| 		} else
  693| #endif /* MIPS */
  694| 		{
  695| 			if (paddr >= mem->physical_max && !no_exceptions)
  696| 				if (memory_warn_about_unimplemented_addr
  697| 				    (cpu, mem, writeflag, paddr, len))
  698| 					return MEMORY_ACCESS_FAILED;
  699| 
  700| 			if (writeflag == MEM_READ) {
  701| 				/*  Return all zeroes? (Or 0xff? TODO)  */
  702| 				memset(data, 0, len);
  703| 
  704| #if 0
  705| /*
  706|  *  NOTE: This code prevents a PROM image from a real 5000/200 from booting.
  707|  *  I think I introduced it because it was how some guest OS (NetBSD?) detected
  708|  *  the amount of RAM on some machine.
```

### `src/core/memory.c` around the row's cited line 598 (HEAD d2a6f233, lines 553-643)

```c
  553| 
  554| 	if (table[entry] == NULL) {
  555| 		size_t alloclen;
  556| 
  557| 		/*
  558| 		 *  Special case:  reading from a nonexistant memblock
  559| 		 *  returns all zeroes, and doesn't allocate anything.
  560| 		 *  (If any intermediate pagetable is nonexistant, then
  561| 		 *  the same thing happens):
  562| 		 */
  563| 		if (writeflag == MEM_READ)
  564| 			return NULL;
  565| 
  566| 		/*  Allocate a memblock:  */
  567| 		alloclen = 1 << BITS_PER_MEMBLOCK;
  568| 
  569| 		/*  printf("  allocating for entry %i, len=%i\n",
  570| 		    entry, alloclen);  */
  571| 
  572| 		/*  Anonymous mmap() should return zero-filled memory,
  573| 		    try malloc + memset if mmap failed.  */
  574| 		table[entry] = (void *) mmap(NULL, alloclen,
  575| 		    PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
  576| 		/*  #175: (Codex/Fable) mmap failure is MAP_FAILED, not NULL  */
  577| 		if (table[entry] == MAP_FAILED) {
  578| 			CHECK_ALLOCATION(table[entry] = malloc(alloclen));
  579| 			memset(table[entry], 0, alloclen);
  580| 		}
  581| 	}
  582| 
  583| 	hostptr = (unsigned char *) table[entry];
  584| 
  585| 	if (hostptr != NULL)
  586| 		hostptr += (paddr & ((1 << BITS_PER_MEMBLOCK) - 1));
  587| 
  588| 	return hostptr;
  589| }
  590| 
  591| 
  592| /*
  593|  *  memory_warn_about_unimplemented_addr():
  594|  *
  595|  *  Called from memory_rw whenever memory outside of the physical address space
  596|  *  is accessed.
  597|  */
  598| bool memory_warn_about_unimplemented_addr(struct cpu *cpu, struct memory *mem,
  599| 	int writeflag, uint64_t paddr, size_t len)
  600| {
  601| 	/*
  602| 	 *  HACK: This allows guest OS kernels to probe memory a few KBs past
  603| 	 *  the end of memory, without giving too many warnings.
  604| 	 */
  605| 	if (paddr < mem->physical_max + 0x40000)
  606| 		return false;
  607| 
  608| 	int verbosity = VERBOSITY_WARNING;
  609| 	if (cpu->machine->halt_on_nonexistant_memaccess)
  610| 		verbosity = VERBOSITY_ERROR;
  611| 
  612| 	// ERROR is always "enough", so we will print in that case.
  613| 	if (!ENOUGH_VERBOSITY(SUBSYS_MEMORY, verbosity))
  614| 		return false;
  615| 
  616| 	uint64_t offset;
  617| 	char* symbol = get_symbol_name(&cpu->machine->symbol_context, cpu->pc, &offset);
  618| 
  619| 	// Not the prettiest, but should work fine.
  620| 	if (cpu->is_32bit)
  621| 		debugmsg_cpu(cpu, SUBSYS_MEMORY,
  622| 		    writeflag ? "WRITE" : "READ",
  623| 		    verbosity, "%s non-existant "
  624| 			"paddr=0x%08" PRIx32 " len=%zu pc=0x%08" PRIx32 "%s%s%s",
  625| 		    writeflag ? "to" : "from",
  626| 		    (uint32_t) paddr,
  627| 		    len,
  628| 		    (uint32_t) cpu->pc,
  629| 		    symbol ? " <" : "",
  630| 		    symbol ? symbol : "",
  631| 		    symbol ? ">" : "");
  632| 	else
  633| 		debugmsg_cpu(cpu, SUBSYS_MEMORY,
  634| 		    writeflag ? "WRITE" : "READ",
  635| 		    verbosity, "%s non-existant "
  636| 			"paddr=0x%016" PRIx64 " len=%zu pc=0x%016" PRIx64 "%s%s%s",
  637| 		    writeflag ? "to" : "from",
  638| 		    (uint64_t) paddr,
  639| 		    len,
  640| 		    (uint64_t) cpu->pc,
  641| 		    symbol ? " <" : "",
  642| 		    symbol ? symbol : "",
  643| 		    symbol ? ">" : "");
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

End with one line: `FIXDRAFT_M88KOUTSIDERAM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
