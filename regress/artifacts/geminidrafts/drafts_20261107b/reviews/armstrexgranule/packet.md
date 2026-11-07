# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armstrexgranule` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armstrexgranule`, state `open`)

**title:** src/cpus/cpu_arm_instr.c:2135-2139 -- a successful STREX clears other CPUs' reservations by comparing addr & 2047, the low bits, where the architecture's tag is the high bits (Memory_address[31:a]), so it clears unrelated reservations at the same offset and misses ones in the same block -- WRONG-RESULT (multi-CPU only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `uint64_t mask = 2047; xaddr &= mask; yaddr &= mask;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 5443a695..2d3af385 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -2132,7 +2132,8 @@ X(strex)
 
 			/*  8-2048 bytes, implementation dependent :-(  */			
 			/*  https://stackoverflow.com/questions/11383125/do-the-arm-instructions-ldrex-strex-have-to-operate-on-cache-aligned-data  */
-			uint64_t mask = 2047;
+			/* #armstrexgranule: match block tag (high bits), not offset */
+			uint64_t mask = ~2047ULL;
 
 			xaddr &= mask;
 			yaddr &= mask;
```

## Every edited function, after the fix

### `src/cpus/cpu_arm_instr.c` -- post-edit lines 2085-2147 (`+` marks a line the diff added or the point of a deletion)

```c
 2085|  X(strex)
 2086|  {
 2087|  	uint32_t addr = reg(ic->arg[1]);
 2088|  	uint64_t r = reg(ic->arg[2]);
 2089|  	int low_pc, i;
 2090|  	uint8_t word[sizeof(uint32_t)];
 2091|  	
 2092|  	/*  Synchronize the program counter:  */
 2093|  	low_pc = ((size_t)ic - (size_t)
 2094|  	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
 2095|  	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
 2096|  	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
 2097|  
 2098|  	if (addr & (sizeof(word)-1)) {
 2099|  		fatal("TODO: strex unaligned access: exception\n");
 2100|  		cpu->running = 0;
 2101|  		cpu->cd.arm.next_ic = &nothing_call;
 2102|  		return;
 2103|  	}
 2104|  
 2105|  	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
 2106|  		word[0]=r; word[1]=r>>8; word[2]=r>>16; word[3]=r>>24;
 2107|  	} else {
 2108|  		word[3]=r; word[2]=r>>8; word[1]=r>>16; word[0]=r>>24;
 2109|  	}
 2110|  
 2111|  	/*  If rmw is 0, then the store failed.  (This cache-line was written
 2112|  	    to by someone else.)  */
 2113|  	if (cpu->cd.arm.rmw == 0 || cpu->cd.arm.rmw_addr != addr
 2114|  	    || cpu->cd.arm.rmw_len != sizeof(word)) {
 2115|  		reg(ic->arg[0]) = 1;	// 1 = fail.
 2116|  		cpu->cd.arm.rmw = 0;
 2117|  		return;
 2118|  	}
 2119|  
 2120|  	if (!cpu->memory_rw(cpu, cpu->mem, addr, word,
 2121|  	    sizeof(word), MEM_WRITE, CACHE_DATA)) {
 2122|  		/*  An exception occurred.  */
 2123|  		return;
 2124|  	}
 2125|  
 2126|  	/*  We succeeded. Let's invalidate everybody else's store to this
 2127|  	    cache line:  */
 2128|  	for (i=0; i<cpu->machine->ncpus; i++) {
 2129|  		if (cpu->machine->cpus[i]->cd.arm.rmw) {
 2130|  			uint64_t yaddr = addr, xaddr = cpu->machine->cpus[i]->
 2131|  			    cd.arm.rmw_addr;
 2132|  
 2133|  			/*  8-2048 bytes, implementation dependent :-(  */			
 2134|  			/*  https://stackoverflow.com/questions/11383125/do-the-arm-instructions-ldrex-strex-have-to-operate-on-cache-aligned-data  */
 2135|+ 			/* #armstrexgranule: match block tag (high bits), not offset */
 2136|+ 			uint64_t mask = ~2047ULL;
 2137|  
 2138|  			xaddr &= mask;
 2139|  			yaddr &= mask;
 2140|  			if (xaddr == yaddr)
 2141|  				cpu->machine->cpus[i]->cd.arm.rmw = 0;
 2142|  		}
 2143|  	}
 2144|  
 2145|  	reg(ic->arg[0]) = 0;	// 0 = success
 2146|  	cpu->cd.arm.rmw = 0;
 2147|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMSTREXGRANULE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMSTREXGRANULE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
