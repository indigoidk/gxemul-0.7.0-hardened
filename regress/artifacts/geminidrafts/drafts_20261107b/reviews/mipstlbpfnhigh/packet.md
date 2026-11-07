# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipstlbpfnhigh` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipstlbpfnhigh`, state `open`)

**title:** src/cpus/memory_mips_v2p.c:86,389-394 -- pmask is uint32_t, so ~pmask zero-extends and ((pfn << pfn_shift) & ~pmask) clears physical-address bits 32 and up on every R4000-style TLB translation, while EntryLo carries a 24-bit page frame number -- WRONG-RESULT

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/memory_mips_v2p.c:86

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_mips_v2p.c b/src/cpus/memory_mips_v2p.c
index 2746a81f..45f7a980 100644
--- a/src/cpus/memory_mips_v2p.c
+++ b/src/cpus/memory_mips_v2p.c
@@ -83,7 +83,7 @@ int TRANSLATE_ADDRESS(struct cpu *cpu, uint64_t vaddr,
 #endif
 	int x_64;	/*  non-zero for 64-bit address space accesses  */
 	int pageshift, n_tlbs;
-	uint32_t pmask;
+	uint64_t pmask;
 #ifdef V2P_MMU4100
 	const int pagemask_mask = PAGEMASK_MASK_R4100;
 	const int pagemask_shift = PAGEMASK_SHIFT_R4100;
```

## Every edited function, after the fix

### `src/cpus/memory_mips_v2p.c` -- post-edit lines 59-457 (`+` marks a line the diff added or the point of a deletion)

```c
   59|  {
   60|  	int writeflag = flags & FLAG_WRITEFLAG? MEM_WRITE : MEM_READ;
   61|  	int no_exceptions = flags & FLAG_NOEXCEPTIONS;
   62|  	int ksu, use_tlb, status, i;
   63|  	uint64_t vaddr_vpn2=0, vaddr_asid=0;
   64|  	int exccode, tlb_refill;
   65|  	struct mips_coproc *cp0;
   66|  
   67|  #ifdef V2P_MMU3K
   68|  	const int x_64 = 0;
   69|  	const int n_tlbs = 64;
   70|  	const uint32_t pmask = 0xfff;
   71|  	uint64_t xuseg_top;		/*  Well, useg actually.  */
   72|  #else
   73|  #ifdef V2P_MMU10K
   74|  	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK_R10K;
   75|  	uint64_t xuseg_top = ENTRYHI_VPN2_MASK_R10K | 0x1fffULL;
   76|  #else
   77|  #ifdef V2P_MMU4100
   78|  	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK | 0x1800;
   79|  #else
   80|  	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK;
   81|  #endif
   82|  	uint64_t xuseg_top = ENTRYHI_VPN2_MASK | 0x1fffULL;
   83|  #endif
   84|  	int x_64;	/*  non-zero for 64-bit address space accesses  */
   85|  	int pageshift, n_tlbs;
   86|+ 	uint64_t pmask;
   87|  #ifdef V2P_MMU4100
   88|  	const int pagemask_mask = PAGEMASK_MASK_R4100;
   89|  	const int pagemask_shift = PAGEMASK_SHIFT_R4100;
   90|  	const int pfn_shift = 10;
   91|  #else
   92|  	const int pagemask_mask = PAGEMASK_MASK;
   93|  	const int pagemask_shift = PAGEMASK_SHIFT;
   94|  	const int pfn_shift = 12;
   95|  #endif
   96|  #endif	/*  !V2P_MMU3K  */
   97|  
   98|  
   99|  	exccode = -1;
  100|  	tlb_refill = 1;
  101|  
  102|  	/*  Cached values:  */
  103|  	cp0 = cpu->cd.mips.coproc[0];
  104|  	status = cp0->reg[COP0_STATUS];
  105|  
  106|  	/*
  107|  	 *  MIPS R4000+ and MIPS64 Address Translation:
  108|  	 *
  109|  	 *  An address may be in one of the kernel segments, that are directly
  110|  	 *  mapped to physical addresses, or the address needs to be looked up
  111|  	 *  in the TLB entries.
  112|  	 *
  113|  	 *  KSU: EXL: ERL: X:  Name:   Range:
  114|  	 *  ---- ---- ---- --  -----   ------
  115|  	 *
  116|  	 *   10   0    0    0  useg    0 - 0x7fffffff    (2GB)  (via TLB)
  117|  	 *   10   0    0    1  xuseg   0 - 0xffffffffff  (1TB)  (via TLB)
  118|  	 *
  119|  	 *   01   0    0    0  suseg   0          - 0x7fffffff  (2GB via TLB)
  120|  	 *   01   0    0    0  ssseg   0xc0000000 - 0xdfffffff  (0.5 GB via TLB)
  121|  	 *   01   0    0    1  xsuseg  0 - 0xffffffffff         (1TB)  (via TLB)
  122|  	 *   01   0    0    1  xsseg   0x4000000000000000 - 0x400000ffffffffff
  123|  	 *					  (1TB)  (via TLB)
  124|  	 *   01   0    0    1  csseg   0xffffffffc0000000 - 0xffffffffdfffffff
  125|  	 *					  (0.5TB)  (via TLB)
  126|  	 *
  127|  	 *   00   x    x    0  kuseg   0 - 0x7fffffff  (2GB)  (via TLB)  (*)
  128|  	 *   00   x    x    0  kseg0   0x80000000 - 0x9fffffff (0.5GB)
  129|  	 *					  unmapped, cached
  130|  	 *   00   x    x    0  kseg1   0xa0000000 - 0xbfffffff (0.5GB)
  131|  	 *					  unmapped, uncached
  132|  	 *   00   x    x    0  ksseg   0xc0000000 - 0xdfffffff (0.5GB) (via TLB)
  133|  	 *   00   x    x    0  kseg3   0xe0000000 - 0xffffffff (0.5GB) (via TLB)
  134|  	 *   00   x    x    1  xksuseg 0 - 0xffffffffff (1TB) (via TLB) (*)
  135|  	 *   00   x    x    1  xksseg  0x4000000000000000 - 0x400000ffffffffff
  136|  	 *					  (1TB)  (via TLB)
  137|  	 *   00   x    x    1  xkphys  0x8000000000000000 - 0xbfffffffffffffff
  138|  	 *   00   x    x    1  xkseg   0xc000000000000000 - 0xc00000ff7fffffff
  139|  	 *   00   x    x    1  ckseg0  0xffffffff80000000 - 0xffffffff9fffffff
  140|  	 *   00   x    x    1  ckseg1  0xffffffffa0000000 - 0xffffffffbfffffff
  141|  	 *   00   x    x    1  cksseg  0xffffffffc0000000 - 0xffffffffdfffffff
  142|  	 *   00   x    x    1  ckseg3  0xffffffffe0000000 - 0xffffffffffffffff
  143|  	 *					  like 0x80000000 - 0xffffffff
  144|  	 *
  145|  	 *  (*) = if ERL=1 then kuseg is not via TLB, but unmapped,
  146|  	 *  uncached physical memory.
     | [... lines 147-427 not shown ...]
  428|  		tlb_refill = 0;
  429|  		if (writeflag == MEM_WRITE)
  430|  			exccode = EXCEPTION_ADES;
  431|  		else
  432|  			exccode = EXCEPTION_ADEL;
  433|  	}
  434|  
  435|  exception:
  436|  	if (no_exceptions)
  437|  		return 0;
  438|  
  439|  	/*  TLB Load or Store exception:  */
  440|  	if (exccode == -1) {
  441|  		if (writeflag == MEM_WRITE)
  442|  			exccode = EXCEPTION_TLBS;
  443|  		else
  444|  			exccode = EXCEPTION_TLBL;
  445|  	}
  446|  
  447|  #ifdef V2P_MMU3K
  448|  	vaddr_asid >>= R2K3K_ENTRYHI_ASID_SHIFT;
  449|  	vaddr_vpn2 >>= 12;
  450|  #endif
  451|  
  452|  	mips_cpu_exception(cpu, exccode, tlb_refill, vaddr,
  453|  	    0, vaddr_vpn2, vaddr_asid, x_64);
  454|  
  455|  	/*  Return failure:  */
  456|  	return 0;
  457|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSTLBPFNHIGH: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSTLBPFNHIGH: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_MIPSTLBPFNHIGH: UNSETTLED, 1 FINDINGS
1. UNSETTLED. The issue names sites 86 and 389-394. The diff edits line 86 to change the type of `pmask`. However, the usage site is not visible because lines 147-427 are not shown in the provided excerpt. It is impossible to verify if changing the declaration fully resolves the defect at 389-394 without seeing the exact expression used there. The file `src/cpus/memory_mips_v2p.c` would settle it.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exits that skip the common tail. 
3. RETURN VALUE: No return paths or returned values are changed by this diff.
4. ELSE: The diff changes nothing else beyond the type of `pmask` for non-MMU3K builds. 
5. House idioms: No new comments, messages, or long lines were added.
src/cpus/memory_mips_v2p.c:389: QUESTION - UNSETTLED: snippet excludes lines 147-427, missing `src/cpus/memory_mips_v2p.c` to check if usage is fixed.
```

(no definition of a name it used was found in HEAD's src/ -- the name may not exist in HEAD)
Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
