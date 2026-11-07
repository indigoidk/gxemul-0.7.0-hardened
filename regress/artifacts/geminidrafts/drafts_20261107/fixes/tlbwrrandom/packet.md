# GXemul hardened fork -- DRAFT A FIX for one filed issue, `tlbwrrandom` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `tlbwrrandom`, state `open`, severity `LOW`)

**title:** cpus/cpu_mips_coproc.c:coproc_tlbwri -- TLBWR takes its index from host random() -- HYGIENE (non-deterministic runs; OpenBSD linker warning)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T149 (class HYGIENE; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-35, C U25).  Source URLs: https://github.com/retroprom/gxemul/commit/90db505f, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/cpu_mips_coproc.c:1949.  Portable fix: yes -- port upstream 90db505f (SVN r6563) keeping #190's WIRED guard.  Filing check (TRIAGE.md): 0 hits.  Reach K, not build-only (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B): TLBWR selects its index at run time.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream 90db505f with WIRED guard

## The code at the cited lines

### `src/cpus/cpu_mips_coproc.c` around the row's cited line 1949 (HEAD d2a6f233, lines 1904-1994)

```c
 1904| 	if (found == -1)
 1905| 		cp->reg[COP0_INDEX] = INDEX_P;
 1906| 	else {
 1907| 		if (cpu->cd.mips.cpu_type.mmu_model == MMU3K)
 1908| 			cp->reg[COP0_INDEX] = found << R2K3K_INDEX_SHIFT;
 1909| 		else
 1910| 			cp->reg[COP0_INDEX] = found;
 1911| 	}
 1912| 
 1913| 	/*  Sign extend the index register:  */
 1914| 	if ((cp->reg[COP0_INDEX] >> 32) == 0 &&
 1915| 	    cp->reg[COP0_INDEX] & 0x80000000)
 1916| 		cp->reg[COP0_INDEX] |=
 1917| 		    0xffffffff00000000ULL;
 1918| }
 1919| 
 1920| 
 1921| /*
 1922|  *  coproc_tlbwri():
 1923|  *
 1924|  *  MIPS TLB write random (tlbwr) and write indexed (tlbwi) instructions.
 1925|  */
 1926| void coproc_tlbwri(struct cpu *cpu, int randomflag)
 1927| {
 1928| 	struct mips_coproc *cp = cpu->cd.mips.coproc[0];
 1929| 	int index, g_bit;
 1930| 	uint64_t oldvaddr;
 1931| 
 1932| 	if (randomflag) {
 1933| 		if (cpu->cd.mips.cpu_type.exc_model == EXC3K) {
 1934| 			index = ((cp->reg[COP0_RANDOM] & R2K3K_RANDOM_MASK)
 1935| 			    >> R2K3K_RANDOM_SHIFT) - 1;
 1936| 			/*  R3000 always has 8 wired entries:  */
 1937| 			if (index < 8)
 1938| 				index = cp->nr_of_tlbs - 1;
 1939| 			cp->reg[COP0_RANDOM] = index << R2K3K_RANDOM_SHIFT;
 1940| 		} else {
 1941| 			/*  #190: (Codex/Fable) COP0_WIRED is guest-writable; if it
 1942| 			    reaches or exceeds nr_of_tlbs the modulo below divides by
 1943| 			    zero (or the unsigned subtraction underflows) -> host SIGFPE.
 1944| 			    Pin Random at the top entry like hardware does on a bad
 1945| 			    WIRED instead of computing a random index.  */
 1946| 			if (cp->reg[COP0_WIRED] >= (uint64_t)cp->nr_of_tlbs)
 1947| 				cp->reg[COP0_RANDOM] = cp->nr_of_tlbs - 1;
 1948| 			else
 1949| 				cp->reg[COP0_RANDOM] = cp->reg[COP0_WIRED] + (random()
 1950| 				    % (cp->nr_of_tlbs - cp->reg[COP0_WIRED]));
 1951| 			index = cp->reg[COP0_RANDOM] & RANDOM_MASK;
 1952| 		}
 1953| 	} else {
 1954| 		if (cpu->cd.mips.cpu_type.mmu_model == MMU3K)
 1955| 			index = (cp->reg[COP0_INDEX] & R2K3K_INDEX_MASK)
 1956| 			    >> R2K3K_INDEX_SHIFT;
 1957| 		else
 1958| 			index = cp->reg[COP0_INDEX] & INDEX_MASK;
 1959| 	}
 1960| 
 1961| 	if (index >= cp->nr_of_tlbs) {
 1962| 		fatal("warning: tlb index %i too high (max is %i)\n",
 1963| 		    index, cp->nr_of_tlbs - 1);
 1964| 		/*  TODO:  cause an exception?  */
 1965| 		return;
 1966| 	}
 1967| 
 1968| 
 1969| #if 0
 1970| 	/*  Debug dump of the previous entry at that index:  */
 1971| 	fatal("{ old TLB entry at index %02x:", index);
 1972| 	if (cpu->cd.mips.cpu_type.mmu_model == MMU3K) {
 1973| 		fatal(" hi=%08" PRIx32, (uint32_t)cp->tlbs[index].hi);
 1974| 		fatal(" lo=%08" PRIx32, (uint32_t)cp->tlbs[index].lo0);
 1975| 	} else {
 1976| 		if (cpu->is_32bit) {
 1977| 			fatal(" mask=%08" PRIx32,(uint32_t)cp->tlbs[index].mask);
 1978| 			fatal(" hi=%08" PRIx32, (uint32_t)cp->tlbs[index].hi);
 1979| 			fatal(" lo0=%08" PRIx32, (uint32_t)cp->tlbs[index].lo0);
 1980| 			fatal(" lo1=%08" PRIx32, (uint32_t)cp->tlbs[index].lo1);
 1981| 		} else {
 1982| 			fatal(" mask=%016" PRIx64, cp->tlbs[index].mask);
 1983| 			fatal(" hi=%016" PRIx64, cp->tlbs[index].hi);
 1984| 			fatal(" lo0=%016" PRIx64, cp->tlbs[index].lo0);
 1985| 			fatal(" lo1=%016" PRIx64, cp->tlbs[index].lo1);
 1986| 		}
 1987| 	}
 1988| 	fatal(" }\n");
 1989| #endif
 1990| 
 1991| 	/*
 1992| 	 *  Any virtual address translation for the old TLB entry must be
 1993| 	 *  invalidated first:
 1994| 	 *
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

End with one line: `FIXDRAFT_TLBWRRANDOM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
