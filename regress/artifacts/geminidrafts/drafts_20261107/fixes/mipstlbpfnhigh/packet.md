# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipstlbpfnhigh` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipstlbpfnhigh`, state `open`, severity `MED`)

**title:** src/cpus/memory_mips_v2p.c:86,389-394 -- pmask is uint32_t, so ~pmask zero-extends and ((pfn << pfn_shift) & ~pmask) clears physical-address bits 32 and up on every R4000-style TLB translation, while EntryLo carries a 24-bit page frame number -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- 32-bit bitwise NOT on pmask zero-extends to 64-bit, catastrophically clearing the high physical address bits.

## The code at the cited lines

### `src/cpus/memory_mips_v2p.c` around the row's cited line 86 (HEAD 2d25df65, lines 41-131)

```c
   41|  *                  R4000+/MIPS32/MIPS64 is presumed.
   42|  *  V2P_MMU10K      This enables the use of 44 userspace bits, instead of 40.
   43|  *  V2P_MMU4100     VR41xx processors support 1 KB pages, so their page mask
   44|  *                  is slightly different. (The emulator only supports 4 KB
   45|  *                  pages, though.)
   46|  *  V2P_MMU8K       Not yet. (TODO.)
   47|  *
   48|  *
   49|  *  Note:  Unfortunately, the variable name vpn2 is poorly choosen for R2K/R3K,
   50|  *         since it actual contains the vpn.
   51|  *
   52|  *  Return values:
   53|  *	0  Failure
   54|  *	1  Success, the page is readable only
   55|  *	2  Success, the page is read/write
   56|  */
   57| int TRANSLATE_ADDRESS(struct cpu *cpu, uint64_t vaddr,
   58| 	uint64_t *return_paddr, int flags)
   59| {
   60| 	int writeflag = flags & FLAG_WRITEFLAG? MEM_WRITE : MEM_READ;
   61| 	int no_exceptions = flags & FLAG_NOEXCEPTIONS;
   62| 	int ksu, use_tlb, status, i;
   63| 	uint64_t vaddr_vpn2=0, vaddr_asid=0;
   64| 	int exccode, tlb_refill;
   65| 	struct mips_coproc *cp0;
   66| 
   67| #ifdef V2P_MMU3K
   68| 	const int x_64 = 0;
   69| 	const int n_tlbs = 64;
   70| 	const uint32_t pmask = 0xfff;
   71| 	uint64_t xuseg_top;		/*  Well, useg actually.  */
   72| #else
   73| #ifdef V2P_MMU10K
   74| 	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK_R10K;
   75| 	uint64_t xuseg_top = ENTRYHI_VPN2_MASK_R10K | 0x1fffULL;
   76| #else
   77| #ifdef V2P_MMU4100
   78| 	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK | 0x1800;
   79| #else
   80| 	const uint64_t vpn2_mask = ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK;
   81| #endif
   82| 	uint64_t xuseg_top = ENTRYHI_VPN2_MASK | 0x1fffULL;
   83| #endif
   84| 	int x_64;	/*  non-zero for 64-bit address space accesses  */
   85| 	int pageshift, n_tlbs;
   86| 	uint32_t pmask;
   87| #ifdef V2P_MMU4100
   88| 	const int pagemask_mask = PAGEMASK_MASK_R4100;
   89| 	const int pagemask_shift = PAGEMASK_SHIFT_R4100;
   90| 	const int pfn_shift = 10;
   91| #else
   92| 	const int pagemask_mask = PAGEMASK_MASK;
   93| 	const int pagemask_shift = PAGEMASK_SHIFT;
   94| 	const int pfn_shift = 12;
   95| #endif
   96| #endif	/*  !V2P_MMU3K  */
   97| 
   98| 
   99| 	exccode = -1;
  100| 	tlb_refill = 1;
  101| 
  102| 	/*  Cached values:  */
  103| 	cp0 = cpu->cd.mips.coproc[0];
  104| 	status = cp0->reg[COP0_STATUS];
  105| 
  106| 	/*
  107| 	 *  MIPS R4000+ and MIPS64 Address Translation:
  108| 	 *
  109| 	 *  An address may be in one of the kernel segments, that are directly
  110| 	 *  mapped to physical addresses, or the address needs to be looked up
  111| 	 *  in the TLB entries.
  112| 	 *
  113| 	 *  KSU: EXL: ERL: X:  Name:   Range:
  114| 	 *  ---- ---- ---- --  -----   ------
  115| 	 *
  116| 	 *   10   0    0    0  useg    0 - 0x7fffffff    (2GB)  (via TLB)
  117| 	 *   10   0    0    1  xuseg   0 - 0xffffffffff  (1TB)  (via TLB)
  118| 	 *
  119| 	 *   01   0    0    0  suseg   0          - 0x7fffffff  (2GB via TLB)
  120| 	 *   01   0    0    0  ssseg   0xc0000000 - 0xdfffffff  (0.5 GB via TLB)
  121| 	 *   01   0    0    1  xsuseg  0 - 0xffffffffff         (1TB)  (via TLB)
  122| 	 *   01   0    0    1  xsseg   0x4000000000000000 - 0x400000ffffffffff
  123| 	 *					  (1TB)  (via TLB)
  124| 	 *   01   0    0    1  csseg   0xffffffffc0000000 - 0xffffffffdfffffff
  125| 	 *					  (0.5TB)  (via TLB)
  126| 	 *
  127| 	 *   00   x    x    0  kuseg   0 - 0x7fffffff  (2GB)  (via TLB)  (*)
  128| 	 *   00   x    x    0  kseg0   0x80000000 - 0x9fffffff (0.5GB)
  129| 	 *					  unmapped, cached
  130| 	 *   00   x    x    0  kseg1   0xa0000000 - 0xbfffffff (0.5GB)
  131| 	 *					  unmapped, uncached
```

### `src/include/cop0.h` around the row's cited line 63 (HEAD 2d25df65, lines 18-108)

```c
   18|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   19|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   20|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   21|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   22|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   23|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   24|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   25|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   26|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   27|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   28|  *  SUCH DAMAGE.
   29|  *
   30|  *
   31|  *  Misc. definitions for MIPS coprocessor 0.
   32|  */
   33| 
   34| 
   35| /*  TODO:  Coproc registers are actually CPU dependent, so an R4000
   36| 	has other bits/registers than an R3000...
   37|     TODO 2: CPUs like the R10000 are probably even a bit more different.  */
   38| 
   39| /*  Coprocessor 0's registers' names: (max 8 characters long)  */
   40| #define	COP0_NAMES	{ \
   41| 	"index", "random", "entrylo0", "entrylo1", \
   42| 	"context", "pagemask", "wired", "reserv7", \
   43| 	"badvaddr", "count", "entryhi", "compare", \
   44| 	"status", "cause", "epc", "prid", \
   45| 	"config", "lladdr", "watchlo", "watchhi", \
   46| 	"xcontext", "reserv21", "reserv22", "debug", \
   47| 	"depc", "perfcnt", "errctl", "cacheerr", \
   48| 	"tagdatlo", "tagdathi", "errorepc", "desave" }
   49| 
   50| #define	COP0_INDEX		0
   51| #define	   INDEX_P		    0x80000000UL	/*  Probe failure bit. Set by tlbp  */
   52| #define	   INDEX_MASK		    0x3f
   53| #define	   R2K3K_INDEX_P	    0x80000000UL
   54| #define	   R2K3K_INDEX_MASK	    0x3f00
   55| #define	   R2K3K_INDEX_SHIFT	    8
   56| #define	COP0_RANDOM		1
   57| #define	   RANDOM_MASK		    0x3f
   58| #define	   R2K3K_RANDOM_MASK	    0x3f00
   59| #define	   R2K3K_RANDOM_SHIFT	    8
   60| #define	COP0_ENTRYLO0		2
   61| #define	COP0_ENTRYLO1		3
   62| /*  R4000 ENTRYLO:  */
   63| #define	   ENTRYLO_PFN_MASK	    0x3fffffc0
   64| #define	   ENTRYLO_PFN_SHIFT	    6
   65| #define	   ENTRYLO_C_MASK	    0x00000038		/*  Coherency attribute  */
   66| #define	   ENTRYLO_C_SHIFT	    3
   67| #define	   ENTRYLO_D		    0x04		/*  Dirty bit  */
   68| #define	   ENTRYLO_V		    0x02		/*  Valid bit  */
   69| #define	   ENTRYLO_G		    0x01		/*  Global bit  */
   70| /*  R2000/R3000 ENTRYLO:  */
   71| #define	   R2K3K_ENTRYLO_PFN_MASK   0xfffff000UL
   72| #define	   R2K3K_ENTRYLO_PFN_SHIFT  12
   73| #define	   R2K3K_ENTRYLO_N	    0x800
   74| #define	   R2K3K_ENTRYLO_D	    0x400
   75| #define	   R2K3K_ENTRYLO_V	    0x200
   76| #define	   R2K3K_ENTRYLO_G	    0x100
   77| #define	COP0_CONTEXT		4
   78| #define	   CONTEXT_BADVPN2_MASK	    0x007ffff0
   79| #define	   CONTEXT_BADVPN2_MASK_R4100	    0x01fffff0
   80| #define	   CONTEXT_BADVPN2_SHIFT    4
   81| #define	   R2K3K_CONTEXT_BADVPN_MASK	 0x001ffffc
   82| #define	   R2K3K_CONTEXT_BADVPN_SHIFT    2
   83| #define	COP0_PAGEMASK		5
   84| #define	   PAGEMASK_MASK	    0x01ffe000
   85| #define	   PAGEMASK_SHIFT	    13
   86| #define	   PAGEMASK_MASK_R4100	    0x0007f800	/*  TODO: At least VR4131,  */
   87| 						/*  how about others?  */
   88| #define	   PAGEMASK_SHIFT_R4100	    11
   89| #define	COP0_WIRED		6
   90| #define	COP0_RESERV7		7
   91| #define	COP0_BADVADDR		8
   92| #define	COP0_COUNT		9
   93| #define	COP0_ENTRYHI		10
   94| /*  R4000 ENTRYHI:  */
   95| #define	   ENTRYHI_R_MASK	    0xc000000000000000ULL
   96| #define	   ENTRYHI_R_XKPHYS	    0x8000000000000000ULL
   97| #define	   ENTRYHI_R_SHIFT	    62
   98| #define	   ENTRYHI_VPN2_MASK_R10K   0x00000fffffffe000ULL
   99| #define	   ENTRYHI_VPN2_MASK	    0x000000ffffffe000ULL
  100| #define	   ENTRYHI_VPN2_SHIFT	    13
  101| #define	   ENTRYHI_ASID		    0xff
  102| #define	   TLB_G		    (1 << 12)
  103| /*  R2000/R3000 ENTRYHI:  */
  104| #define	   R2K3K_ENTRYHI_VPN_MASK   0xfffff000UL
  105| #define	   R2K3K_ENTRYHI_VPN_SHIFT  12
  106| #define	   R2K3K_ENTRYHI_ASID_MASK  0xfc0
  107| #define	   R2K3K_ENTRYHI_ASID_SHIFT 6
  108| #define	COP0_COMPARE		11
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

End with one line: `FIXDRAFT_MIPSTLBPFNHIGH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
