# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipsdivwrap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipsdivwrap`, state `open`, severity `MED`)

**title:** cpus/cpu_mips_instr.c:X(div)/X(ddiv) -- INT_MIN / -1 returns LO=0 (and ddiv HI = dividend) where the manuals give the wrapped quotient with HI=0 -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T21 (class WRONG-RESULT; reach U, user mode; effort: one-line each; report rows: A6-5, A issues (CHERI PR#1)).  Source URLs: https://github.com/CTSRD-CHERI/gxemul/commit/1236c18954d858650dcc6267ede063fad1e6df6b, https://github.com/CTSRD-CHERI/gxemul/pull/1.  Our site at de8c7547: src/cpus/cpu_mips_instr.c:1839-1840, :1863-1867.  Portable fix: yes -- port CHERI 1236c18 / CHERI PR#1 (result value only; the host-trap guard is already present).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port CHERI 1236c18 result value only

## The code at the cited lines

### `src/cpus/cpu_mips_instr.c` around the row's cited line 1839 (HEAD d2a6f233, lines 1794-1884)

```c
 1794| 	reg(ic->arg[1]) = x;
 1795| }
 1796| X(dshd)
 1797| {
 1798| 	uint64_t x = reg(ic->arg[0]);
 1799| 	x = ((x & 0x000000000000ffffULL) << 48)
 1800| 	  | ((x & 0x00000000ffff0000ULL) << 16)
 1801| 	  | ((x & 0x0000ffff00000000ULL) >> 16)
 1802| 	  | ((x & 0xffff000000000000ULL) >> 48);
 1803| 	reg(ic->arg[1]) = x;
 1804| }
 1805| X(wsbh)
 1806| {
 1807| 	uint32_t x = reg(ic->arg[0]);
 1808| 	x = ((x & 0x00ff00ff) << 8) | ((x & 0xff00ff00) >> 8);
 1809| 	reg(ic->arg[1]) = (int32_t) x;
 1810| }
 1811| X(seb) { reg(ic->arg[1]) = (int8_t)reg(ic->arg[0]); }
 1812| X(seh) { reg(ic->arg[1]) = (int16_t)reg(ic->arg[0]); }
 1813| 
 1814| 
 1815| /*
 1816|  *  2-register + immediate:
 1817|  *
 1818|  *  arg[0] = pointer to rs
 1819|  *  arg[1] = pointer to rt
 1820|  *  arg[2] = uint32_t immediate value
 1821|  */
 1822| X(andi) { reg(ic->arg[1]) = reg(ic->arg[0]) & (uint32_t)ic->arg[2]; }
 1823| X(ori)  { reg(ic->arg[1]) = reg(ic->arg[0]) | (uint32_t)ic->arg[2]; }
 1824| X(xori) { reg(ic->arg[1]) = reg(ic->arg[0]) ^ (uint32_t)ic->arg[2]; }
 1825| 
 1826| 
 1827| /*
 1828|  *  2-register:
 1829|  *
 1830|  *  arg[0] = ptr to rs
 1831|  *  arg[1] = ptr to rt
 1832|  */
 1833| X(div)
 1834| {
 1835| 	int32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1836| 	int32_t res, rem;
 1837| 	if (b == 0)
 1838| 		res = 0, rem = a;
 1839| 	else if (a == (int32_t)0x80000000U && b == -1)
 1840| 		res = 0, rem = 0;
 1841| 	else
 1842| 		res = a / b, rem = a - b*res;
 1843| 	cpu->cd.mips.lo = (int32_t)res;
 1844| 	cpu->cd.mips.hi = (int32_t)rem;
 1845| }
 1846| X(divu)
 1847| {
 1848| 	uint32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1849| 	uint32_t res, rem;
 1850| 	if (b == 0)
 1851| 		res = 0, rem = a;
 1852| 	else
 1853| 		res = a / b, rem = a - b*res;
 1854| 	cpu->cd.mips.lo = (int32_t)res;
 1855| 	cpu->cd.mips.hi = (int32_t)rem;
 1856| }
 1857| X(ddiv)
 1858| {
 1859| 	int64_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1860| 	int64_t res, rem;
 1861| 	if (b == 0)
 1862| 		res = 0;
 1863| 	else if (a == (int64_t)0x8000000000000000ULL && b == -1)
 1864| 		res = 0;
 1865| 	else
 1866| 		res = a / b;
 1867| 	rem = a - b*res;
 1868| 	cpu->cd.mips.lo = res;
 1869| 	cpu->cd.mips.hi = rem;
 1870| }
 1871| X(ddivu)
 1872| {
 1873| 	uint64_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
 1874| 	uint64_t res, rem;
 1875| 	if (b == 0)
 1876| 		res = 0;
 1877| 	else
 1878| 		res = a / b;
 1879| 	rem = a - b*res;
 1880| 	cpu->cd.mips.lo = res;
 1881| 	cpu->cd.mips.hi = rem;
 1882| }
 1883| X(mult)
 1884| {
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

End with one line: `FIXDRAFT_MIPSDIVWRAP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
