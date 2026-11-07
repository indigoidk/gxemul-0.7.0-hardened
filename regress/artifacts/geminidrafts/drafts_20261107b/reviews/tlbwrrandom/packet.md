# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `tlbwrrandom` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `tlbwrrandom`, state `open`)

**title:** cpus/cpu_mips_coproc.c:coproc_tlbwri -- TLBWR takes its index from host random() -- HYGIENE (non-deterministic runs; OpenBSD linker warning)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T149 (class HYGIENE; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-35, C U25).  Source URLs: https://github.com/retroprom/gxemul/commit/90db505f, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/cpu_mips_coproc.c:1949.  Portable fix: yes -- port upstream 90db505f (SVN r6563) keeping #190's WIRED guard.  Filing check (TRIAGE.md): 0 hits.  Reach K, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): TLBWR selects its index at run time.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 1949| 				cp->reg[COP0_RANDOM] = cp->reg[COP0_WIRED] + (random()

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_coproc.c b/src/cpus/cpu_mips_coproc.c
index f6af6955..91c869f7 100644
--- a/src/cpus/cpu_mips_coproc.c
+++ b/src/cpus/cpu_mips_coproc.c
@@ -1945,9 +1945,12 @@ void coproc_tlbwri(struct cpu *cpu, int randomflag)
 			    WIRED instead of computing a random index.  */
 			if (cp->reg[COP0_WIRED] >= (uint64_t)cp->nr_of_tlbs)
 				cp->reg[COP0_RANDOM] = cp->nr_of_tlbs - 1;
-			else
-				cp->reg[COP0_RANDOM] = cp->reg[COP0_WIRED] + (random()
-				    % (cp->nr_of_tlbs - cp->reg[COP0_WIRED]));
+			else {
+				if (cp->reg[COP0_RANDOM] <= cp->reg[COP0_WIRED])
+					cp->reg[COP0_RANDOM] = cp->nr_of_tlbs - 1;
+				else
+					cp->reg[COP0_RANDOM]--;
+			}
 			index = cp->reg[COP0_RANDOM] & RANDOM_MASK;
 		}
 	} else {
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_coproc.c` -- post-edit lines 1926-2267 (`+` marks a line the diff added or the point of a deletion)

```c
 1926|  void coproc_tlbwri(struct cpu *cpu, int randomflag)
 1927|  {
 1928|  	struct mips_coproc *cp = cpu->cd.mips.coproc[0];
 1929|  	int index, g_bit;
 1930|  	uint64_t oldvaddr;
 1931|  
 1932|  	if (randomflag) {
 1933|  		if (cpu->cd.mips.cpu_type.exc_model == EXC3K) {
 1934|  			index = ((cp->reg[COP0_RANDOM] & R2K3K_RANDOM_MASK)
 1935|  			    >> R2K3K_RANDOM_SHIFT) - 1;
 1936|  			/*  R3000 always has 8 wired entries:  */
 1937|  			if (index < 8)
 1938|  				index = cp->nr_of_tlbs - 1;
 1939|  			cp->reg[COP0_RANDOM] = index << R2K3K_RANDOM_SHIFT;
 1940|  		} else {
 1941|  			/*  #190: (Codex/Fable) COP0_WIRED is guest-writable; if it
 1942|  			    reaches or exceeds nr_of_tlbs the modulo below divides by
 1943|  			    zero (or the unsigned subtraction underflows) -> host SIGFPE.
 1944|  			    Pin Random at the top entry like hardware does on a bad
 1945|  			    WIRED instead of computing a random index.  */
 1946|  			if (cp->reg[COP0_WIRED] >= (uint64_t)cp->nr_of_tlbs)
 1947|  				cp->reg[COP0_RANDOM] = cp->nr_of_tlbs - 1;
 1948|+ 			else {
 1949|+ 				if (cp->reg[COP0_RANDOM] <= cp->reg[COP0_WIRED])
 1950|+ 					cp->reg[COP0_RANDOM] = cp->nr_of_tlbs - 1;
 1951|+ 				else
 1952|+ 					cp->reg[COP0_RANDOM]--;
 1953|+ 			}
 1954|  			index = cp->reg[COP0_RANDOM] & RANDOM_MASK;
 1955|  		}
 1956|  	} else {
 1957|  		if (cpu->cd.mips.cpu_type.mmu_model == MMU3K)
 1958|  			index = (cp->reg[COP0_INDEX] & R2K3K_INDEX_MASK)
 1959|  			    >> R2K3K_INDEX_SHIFT;
 1960|  		else
 1961|  			index = cp->reg[COP0_INDEX] & INDEX_MASK;
 1962|  	}
 1963|  
 1964|  	if (index >= cp->nr_of_tlbs) {
 1965|  		fatal("warning: tlb index %i too high (max is %i)\n",
 1966|  		    index, cp->nr_of_tlbs - 1);
 1967|  		/*  TODO:  cause an exception?  */
 1968|  		return;
 1969|  	}
 1970|  
 1971|  
 1972|  #if 0
 1973|  	/*  Debug dump of the previous entry at that index:  */
 1974|  	fatal("{ old TLB entry at index %02x:", index);
 1975|  	if (cpu->cd.mips.cpu_type.mmu_model == MMU3K) {
 1976|  		fatal(" hi=%08" PRIx32, (uint32_t)cp->tlbs[index].hi);
 1977|  		fatal(" lo=%08" PRIx32, (uint32_t)cp->tlbs[index].lo0);
 1978|  	} else {
 1979|  		if (cpu->is_32bit) {
 1980|  			fatal(" mask=%08" PRIx32,(uint32_t)cp->tlbs[index].mask);
 1981|  			fatal(" hi=%08" PRIx32, (uint32_t)cp->tlbs[index].hi);
 1982|  			fatal(" lo0=%08" PRIx32, (uint32_t)cp->tlbs[index].lo0);
 1983|  			fatal(" lo1=%08" PRIx32, (uint32_t)cp->tlbs[index].lo1);
 1984|  		} else {
 1985|  			fatal(" mask=%016" PRIx64, cp->tlbs[index].mask);
 1986|  			fatal(" hi=%016" PRIx64, cp->tlbs[index].hi);
 1987|  			fatal(" lo0=%016" PRIx64, cp->tlbs[index].lo0);
 1988|  			fatal(" lo1=%016" PRIx64, cp->tlbs[index].lo1);
 1989|  		}
 1990|  	}
 1991|  	fatal(" }\n");
 1992|  #endif
 1993|  
 1994|  	/*
 1995|  	 *  Any virtual address translation for the old TLB entry must be
 1996|  	 *  invalidated first:
 1997|  	 *
 1998|  	 *  (Only Valid entries need to be invalidated, and only those that
 1999|  	 *  are either Global, or have the same ASID as the new entry will
 2000|  	 *  have. No other address translations should be active anyway.)
 2001|  	 */
 2002|  
 2003|  	switch (cpu->cd.mips.cpu_type.mmu_model) {
 2004|  
 2005|  	case MMU3K:
 2006|  		oldvaddr = cp->tlbs[index].hi & R2K3K_ENTRYHI_VPN_MASK;
 2007|  		oldvaddr = (int32_t) oldvaddr;
 2008|  
 2009|  		if (cp->tlbs[index].lo0 & R2K3K_ENTRYLO_V &&
 2010|  		    (cp->tlbs[index].lo0 & R2K3K_ENTRYLO_G ||
 2011|  		    (cp->tlbs[index].hi & R2K3K_ENTRYHI_ASID_MASK) ==
 2012|  		    (cp->reg[COP0_ENTRYHI] & R2K3K_ENTRYHI_ASID_MASK) ))
 2013|  			cpu->invalidate_translation_caches(cpu, oldvaddr,
     | [... lines 2014-2237 not shown ...]
 2238|  				    paddr1 + ptmp, INVALIDATE_PADDR);
 2239|  		}
 2240|  
 2241|  		/*
 2242|  		 *  If we have a memblock (host page) for the physical page,
 2243|  		 *  then add a translation for it immediately, to save some
 2244|  		 *  time. (It would otherwise be added later on anyway,
 2245|  		 *  because of a translation miss.)
 2246|  		 *
 2247|  		 *  NOTE/TODO: This is only for 4KB pages so far. It would
 2248|  		 *             be too expensive to add e.g. 16MB pages like
 2249|  		 *             this.
 2250|  		 */
 2251|  		if (psize == 0x1000) {
 2252|  			if (cp->reg[COP0_ENTRYLO0] & ENTRYLO_V) {
 2253|  				unsigned char *memblock = memory_paddr_to_hostaddr(cpu->mem, paddr0, 0);
 2254|  				if (memblock != NULL)
 2255|  					cpu->update_translation_table(cpu, vaddr0, memblock, wf0, paddr0);
 2256|  			}
 2257|  			if (cp->reg[COP0_ENTRYLO1] & ENTRYLO_V) {
 2258|  				unsigned char *memblock = memory_paddr_to_hostaddr(cpu->mem, paddr1, 0);
 2259|  				if (memblock != NULL)
 2260|  					cpu->update_translation_table(cpu, vaddr1, memblock, wf1, paddr1);
 2261|  			}
 2262|  		}
 2263|  
 2264|  		/*  Set new last_written_tlb_index hint:  */
 2265|  		cpu->cd.mips.last_written_tlb_index = index;
 2266|  	}
 2267|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_TLBWRRANDOM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_TLBWRRANDOM: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
