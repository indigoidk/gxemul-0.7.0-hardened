# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armstrexgranule` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armstrexgranule`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_arm_instr.c:2135-2139 -- a successful STREX clears other CPUs' reservations by comparing addr & 2047, the low bits, where the architecture's tag is the high bits (Memory_address[31:a]), so it clears unrelated reservations at the same offset and misses ones in the same block -- WRONG-RESULT (multi-CPU only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- requires correcting the mask to use high bits instead of low bits.

## The code at the cited lines

### `src/cpus/cpu_arm_instr.c` around the row's cited line 2135 (HEAD 2d25df65, lines 2090-2180)

```c
 2090| 	uint8_t word[sizeof(uint32_t)];
 2091| 	
 2092| 	/*  Synchronize the program counter:  */
 2093| 	low_pc = ((size_t)ic - (size_t)
 2094| 	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
 2095| 	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
 2096| 	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
 2097| 
 2098| 	if (addr & (sizeof(word)-1)) {
 2099| 		fatal("TODO: strex unaligned access: exception\n");
 2100| 		cpu->running = 0;
 2101| 		cpu->cd.arm.next_ic = &nothing_call;
 2102| 		return;
 2103| 	}
 2104| 
 2105| 	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
 2106| 		word[0]=r; word[1]=r>>8; word[2]=r>>16; word[3]=r>>24;
 2107| 	} else {
 2108| 		word[3]=r; word[2]=r>>8; word[1]=r>>16; word[0]=r>>24;
 2109| 	}
 2110| 
 2111| 	/*  If rmw is 0, then the store failed.  (This cache-line was written
 2112| 	    to by someone else.)  */
 2113| 	if (cpu->cd.arm.rmw == 0 || cpu->cd.arm.rmw_addr != addr
 2114| 	    || cpu->cd.arm.rmw_len != sizeof(word)) {
 2115| 		reg(ic->arg[0]) = 1;	// 1 = fail.
 2116| 		cpu->cd.arm.rmw = 0;
 2117| 		return;
 2118| 	}
 2119| 
 2120| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, word,
 2121| 	    sizeof(word), MEM_WRITE, CACHE_DATA)) {
 2122| 		/*  An exception occurred.  */
 2123| 		return;
 2124| 	}
 2125| 
 2126| 	/*  We succeeded. Let's invalidate everybody else's store to this
 2127| 	    cache line:  */
 2128| 	for (i=0; i<cpu->machine->ncpus; i++) {
 2129| 		if (cpu->machine->cpus[i]->cd.arm.rmw) {
 2130| 			uint64_t yaddr = addr, xaddr = cpu->machine->cpus[i]->
 2131| 			    cd.arm.rmw_addr;
 2132| 
 2133| 			/*  8-2048 bytes, implementation dependent :-(  */			
 2134| 			/*  https://stackoverflow.com/questions/11383125/do-the-arm-instructions-ldrex-strex-have-to-operate-on-cache-aligned-data  */
 2135| 			uint64_t mask = 2047;
 2136| 
 2137| 			xaddr &= mask;
 2138| 			yaddr &= mask;
 2139| 			if (xaddr == yaddr)
 2140| 				cpu->machine->cpus[i]->cd.arm.rmw = 0;
 2141| 		}
 2142| 	}
 2143| 
 2144| 	reg(ic->arg[0]) = 0;	// 0 = success
 2145| 	cpu->cd.arm.rmw = 0;
 2146| }
 2147| Y(strex)
 2148| 
 2149| 
 2150| /*  Various load/store multiple instructions:  */
 2151| extern uint32_t *multi_opcode[256];
 2152| extern void (**multi_opcode_f[256])(struct cpu *, struct arm_instr_call *);
 2153| X(multi_0x08b15018);
 2154| X(multi_0x08ac000c__ge);
 2155| X(multi_0x08a05018);
 2156| 
 2157| 
 2158| /*****************************************************************************/
 2159| 
 2160| 
 2161| /*
 2162|  *  netbsd_memset:
 2163|  *
 2164|  *  The core of a NetBSD/arm memset.
 2165|  *
 2166|  *  f01bc420:  e25XX080     subs    rX,rX,#0x80
 2167|  *  f01bc424:  a8ac000c     stmgeia ip!,{r2,r3}   (16 of these)
 2168|  *  ..
 2169|  *  f01bc464:  caffffed     bgt     0xf01bc420      <memset+0x38>
 2170|  */
 2171| X(netbsd_memset)
 2172| {
 2173| 	unsigned char *page;
 2174| 	uint32_t addr;
 2175| 
 2176| 	do {
 2177| 		addr = cpu->cd.arm.r[ARM_IP];
 2178| 
 2179| 		instr(subs)(cpu, ic);
 2180| 
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_ARMSTREXGRANULE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
