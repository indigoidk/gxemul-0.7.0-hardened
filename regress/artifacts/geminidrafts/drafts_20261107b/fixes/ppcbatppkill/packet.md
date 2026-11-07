# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcbatppkill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcbatppkill`, state `open`, severity `HIGH`)

**title:** PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches fatal()+exit(1) instead of a DSI/ISI

**state_note (head):**

[2026-10-22] RE-FOUND by the external-fixes adjudication as N5 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md C; Grok 4.7, adj_20261022/grok_adj.txt): memory_ppc.c:69-73 (the BAT block returns 0 for PP=none, or for a write to a read-only BAT) and the caller's exit at :273-276 are this row's defect, so no second row is filed -- the seat searched for the message text 'TODO: BAT exception', which this row does not quote.  `qhslowifetch`'s fix (return into an ISI already raised) is not this row's fix (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B, T6).  ||  GOVERNING TEXT (from the dispositions file, cut at 400 characters): `ppcbatppkill` HIGH -- PPC: a BAT hit with PP=00, or a store through a read-only BAT, reaches `fatal()` + `exit(1)` (memory_ppc.c `ppc_bat_block` -> `:273-276`) instead of a DSI/ISI (ppc_pem32_rev2_2001.txt:13503-13519). Also precedes the FLAG_NOEXCEPTIONS test, so a debugger `dump` of such a block ends the process

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Replace fatal()+exit(1) with proper DSI/ISI exception generation

## The code at the cited lines

### `src/cpus/memory_ppc.c` around line 43 -- LOCATED BY THE COORDINATOR from the name `ppc_bat_block` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1-163)

```c
    1| /*
    2|  *  Copyright (C) 2005-2009  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *
   27|  *
   28|  *  Included from cpu_ppc.c.
   29|  */
   30| 
   31| 
   32| /*
   33|  *  ppc_bat():
   34|  *
   35|  *  BAT translation. Returns -1 if there was no BAT hit, >= 0 for a hit.
   36|  *  (0 for access denied, 1 for read-only, and 2 for read-write access allowed.)
   37|  */
   38| /*  #116: MPC7445/7455 HID0[HIGH_BAT_EN] (MSB-0 bit 8) enables IBAT4-7/DBAT4-7.  */
   39| #define	HID0_HIGH_BAT_EN	0x00800000
   40| 
   41| /*  #116: scan one 4-pair BAT block (base_spr = SPR_IBAT0U or SPR_IBAT4U).
   42|     The body is the original ppc_bat() loop, unchanged.  */
   43| static int ppc_bat_block(struct cpu *cpu, uint64_t vaddr, uint64_t *return_paddr,
   44| 	int flags, int user, int istart, int iend, int base_spr)
   45| {
   46| 	int i, pp;
   47| 
   48| 	for (i=istart; i<iend; i++) {
   49| 		int regnr = base_spr + i * 2;
   50| 		uint32_t upper = cpu->cd.ppc.spr[regnr];
   51| 		uint32_t lower = cpu->cd.ppc.spr[regnr + 1];
   52| 		uint32_t phys = lower & BAT_RPN, ebs = upper & BAT_EPI;
   53| 		uint32_t mask = ((upper & BAT_BL) << 15) | 0x1ffff;
   54| 
   55| 		/*  Not valid in either supervisor or user mode?  */
   56| 		if (user && !(upper & BAT_Vu))
   57| 			continue;
   58| 		if (!user && !(upper & BAT_Vs))
   59| 			continue;
   60| 
   61| 		/*  Virtual address mismatch? Then skip.  */
   62| 		if ((vaddr & ~mask) != (ebs & ~mask))
   63| 			continue;
   64| 
   65| 		*return_paddr = (vaddr & mask) | (phys & ~mask);
   66| 
   67| 		pp = lower & BAT_PP;
   68| 		switch (pp) {
   69| 		case BAT_PP_NONE:
   70| 			return 0;
   71| 		case BAT_PP_RO_S:
   72| 		case BAT_PP_RO:
   73| 			return (flags & FLAG_WRITEFLAG)? 0 : 1;
   74| 		default:/*  BAT_PP_RW:  */
   75| 			return 2;
   76| 		}
   77| 	}
   78| 
   79| 	return -1;
   80| }
   81| 
   82| int ppc_bat(struct cpu *cpu, uint64_t vaddr, uint64_t *return_paddr, int flags,
   83| 	int user)
   84| {
   85| 	int istart = 0, iend = 8, r;
   86| 
   87| 	if (flags & FLAG_INSTR)
   88| 		iend = 4;
   89| 	else
   90| 		istart = 4;
   91| 
   92| 	if (cpu->cd.ppc.bits != 32) {
   93| 		fatal("TODO: ppc_bat() for non-32-bit\n");
   94| 		exit(1);
   95| 	}
   96| 	if (cpu->cd.ppc.cpu_type.flags & PPC_601) {
   97| 		fatal("TODO: ppc_bat() for PPC 601\n");
   98| 		exit(1);
   99| 	}
  100| 
  101| 	/*  Base BATs 0-3 (the 4 instruction or the 4 data BATs):  */
  102| 	r = ppc_bat_block(cpu, vaddr, return_paddr, flags, user,
  103| 	    istart, iend, SPR_IBAT0U);
  104| 	if (r != -1)
  105| 		return r;
  106| 
  107| 	/*  #116: extended BATs 4-7 (MPC7445/7455), identical layout at 0x230,
  108| 	    but ONLY when the guest has enabled them via HID0[HIGH_BAT_EN].  This
  109| 	    keeps the aliased DC_ADR/DC_DAT/DC_CST (0x231/0x232/0x238) cache-debug
  110| 	    SPRs from spoofing a BAT on a non-745x guest (Codex+agy consensus).  */
  111| 	/*  #174: (Codex/Fable) also require the modeled CPU to actually
  112| 	    have the extended BATs (PPC_HIGH_BAT capability), so that e.g.
  113| 	    a 603/7400 guest cannot enable them via HID0.  */
  114| 	if ((cpu->cd.ppc.cpu_type.flags & PPC_HIGH_BAT) &&
  115| 	    (cpu->cd.ppc.spr[SPR_HID0] & HID0_HIGH_BAT_EN))
  116| 		return ppc_bat_block(cpu, vaddr, return_paddr, flags, user,
  117| 		    istart, iend, SPR_IBAT4U);
  118| 
  119| 	return -1;
  120| }
  121| 
  122| 
  123| /*
  124|  *  get_pte_low():
  125|  *
  126|  *  Scan a PTE group for a cmp (compare) value.
  127|  *
  128|  *  Returns 1 if the value was found, and *lowp is set to the low PTE word.
  129|  *  Returns 0 if no match was found.
  130|  */
  131| static int get_pte_low(struct cpu *cpu, uint64_t pteg_select,
  132| 	uint32_t *lowp, uint32_t cmp)
  133| {
  134| 	unsigned char *d = memory_paddr_to_hostaddr(cpu->mem, pteg_select, 1);
  135| 	int i;
  136| 
  137| 	for (i=0; i<8; i++) {
  138| 		uint32_t *ep = (uint32_t *) (d + (i << 3)), upper;
  139| 		upper = *ep;
  140| 		upper = BE32_TO_HOST(upper);
  141| 
  142| 		/*  Valid PTE, and correct api and vsid?  */
  143| 		if (upper == cmp) {
  144| 			uint32_t lo = ep[1];
  145| 			lo = BE32_TO_HOST(lo);
  146| 			*lowp = lo;
  147| 			return 1;
  148| 		}
  149| 	}
  150| 
  151| 	return 0;
  152| }
  153| 
  154| 
  155| /*
  156|  *  ppc_vtp32():
  157|  *
  158|  *  Virtual to physical address translation (32-bit mode).
  159|  *
  160|  *  Returns 1 if a translation was found, 0 if none was found. However, finding
  161|  *  a translation does not mean that it should be returned; there can be
  162|  *  a permission violation. *resp is set to 0 for no access, 1 for read-only
  163|  *  access, or 2 for read/write access.
```

### `src/cpus/memory_ppc.c` around line 299 -- LOCATED BY THE COORDINATOR from the name `FLAG_NOEXCEPTIONS` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 179-329)

```c
  179| 	tmp = (hash1 >> 10) & (sdr1 & 0x1ff);
  180| 	pteg_select = htaborg & 0xfe000000;
  181| 	pteg_select |= ((hash1 & 0x3ff) << 6);
  182| 	pteg_select |= (htaborg & 0x01ff0000) | (tmp << 16);
  183| 	cpu->cd.ppc.spr[SPR_HASH1] = pteg_select;
  184| 	cmp = cpu->cd.ppc.spr[instr? SPR_ICMP : SPR_DCMP] =
  185| 	    PTE_VALID | api | (vsid << PTE_VSID_SHFT);
  186| 	match = get_pte_low(cpu, pteg_select, &lower_pte, cmp);
  187| 
  188| 	/*  Secondary hash:  */
  189| 	hash2 = hash1 ^ 0x7ffff;
  190| 	tmp = (hash2 >> 10) & (sdr1 & 0x1ff);
  191| 	pteg_select = htaborg & 0xfe000000;
  192| 	pteg_select |= ((hash2 & 0x3ff) << 6);
  193| 	pteg_select |= (htaborg & 0x01ff0000) | (tmp << 16);
  194| 	cpu->cd.ppc.spr[SPR_HASH2] = pteg_select;
  195| 	if (!match) {
  196| 		cmp |= PTE_HID;
  197| 		match = get_pte_low(cpu, pteg_select, &lower_pte, cmp);
  198| 	}
  199| 
  200| 	*resp = 0;
  201| 
  202| 	if (!match)
  203| 		return 0;
  204| 
  205| 	/*  Non-executable, or Guarded page?  */
  206| 	if (instr && cpu->cd.ppc.sr[srn] & SR_NOEXEC)
  207| 		return 1;
  208| 	if (instr && lower_pte & PTE_G)
  209| 		return 1;
  210| 
  211| 	access = lower_pte & PTE_PP;
  212| 	*return_paddr = (lower_pte & PTE_RPGN) | (vaddr & ~PTE_RPGN);
  213| 
  214| 	key = (cpu->cd.ppc.sr[srn] & SR_PRKEY && msr & PPC_MSR_PR) ||
  215| 	    (cpu->cd.ppc.sr[srn] & SR_SUKEY && !(msr & PPC_MSR_PR));
  216| 
  217| 	if (key) {
  218| 		switch (access) {
  219| 		case 1:
  220| 		case 3:	*resp = writeflag? 0 : 1;
  221| 			break;
  222| 		case 2:	*resp = 2;
  223| 			break;
  224| 		}
  225| 	} else {
  226| 		switch (access) {
  227| 		case 3:	*resp = writeflag? 0 : 1;
  228| 			break;
  229| 		default:*resp = 2;
  230| 		}
  231| 	}
  232| 
  233| 	return 1;
  234| }
  235| 
  236| 
  237| /*
  238|  *  ppc_translate_v2p():
  239|  *
  240|  *  Return values:
  241|  *	0  Failure
  242|  *	1  Success, the page is readable only
  243|  *	2  Success, the page is read/write
  244|  */
  245| int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
  246| 	uint64_t *return_paddr, int flags)
  247| {
  248| 	int instr = flags & FLAG_INSTR, res = 0, match, user;
  249| 	int writeflag = flags & FLAG_WRITEFLAG? 1 : 0;
  250| 	uint64_t msr;
  251| 
  252| 	reg_access_msr(cpu, &msr, 0, 0);
  253| 	user = msr & PPC_MSR_PR? 1 : 0;
  254| 
  255| 	if (cpu->cd.ppc.bits == 32)
  256| 		vaddr &= 0xffffffff;
  257| 
  258| 	if ((instr && !(msr & PPC_MSR_IR)) || (!instr && !(msr & PPC_MSR_DR))) {
  259| 		*return_paddr = vaddr;
  260| 		return 2;
  261| 	}
  262| 
  263| 	if (cpu->cd.ppc.cpu_type.flags & PPC_601) {
  264| 		fatal("ppc_translate_v2p(): TODO: 601\n");
  265| 		exit(1);
  266| 	}
  267| 
  268| 	/*  Try the BATs first:  */
  269| 	if (cpu->cd.ppc.bits == 32) {
  270| 		res = ppc_bat(cpu, vaddr, return_paddr, flags, user);
  271| 		if (res > 0)
  272| 			return res;
  273| 		if (res == 0) {
  274| 			fatal("[ TODO: BAT exception ]\n");
  275| 			exit(1);
  276| 		}
  277| 	}
  278| 
  279| 	/*  Virtual to physical translation:  */
  280| 	if (cpu->cd.ppc.bits == 32) {
  281| 		match = ppc_vtp32(cpu, vaddr, return_paddr, &res, msr,
  282| 		    writeflag, instr);
  283| 		if (match && res > 0)
  284| 			return res;
  285| 	} else {
  286| 		/*  htaborg = sdr1 & 0xfffffffffffc0000ULL;  */
  287| 		fatal("TODO: ppc 64-bit translation\n");
  288| 		exit(1);
  289| 	}
  290| 
  291| 
  292| 	/*
  293| 	 *  No match? Then cause an exception.
  294| 	 *
  295| 	 *  PPC603: cause a software TLB reload exception.
  296| 	 *  All others: cause a DSI or ISI.
  297| 	 */
  298| 
  299| 	if (flags & FLAG_NOEXCEPTIONS)
  300| 		return 0;
  301| 
  302| 	if (!quiet_mode)
  303| 		fatal("[ memory_ppc: exception! vaddr=0x%" PRIx64" pc=0x%" PRIx64
  304| 		    " instr=%i user=%i wf=%i ]\n", (uint64_t) vaddr,
  305| 		    (uint64_t) cpu->pc, instr, user, writeflag);
  306| 
  307| 	if (cpu->cd.ppc.cpu_type.flags & PPC_603) {
  308| 		cpu->cd.ppc.spr[instr? SPR_IMISS : SPR_DMISS] = vaddr;
  309| 
  310| 		msr |= PPC_MSR_TGPR;
  311| 		reg_access_msr(cpu, &msr, 1, 0);
  312| 
  313| 		ppc_exception(cpu, instr? 0x10 : (writeflag? 0x12 : 0x11));
  314| 	} else {
  315| 		if (!instr) {
  316| 			cpu->cd.ppc.spr[SPR_DAR] = vaddr;
  317| 			cpu->cd.ppc.spr[SPR_DSISR] = match?
  318| 			    DSISR_PROTECT : DSISR_NOTFOUND;
  319| 			if (writeflag)
  320| 				cpu->cd.ppc.spr[SPR_DSISR] |= DSISR_STORE;
  321| 		}
  322| 		ppc_exception(cpu, instr?
  323| 		    PPC_EXCEPTION_ISI : PPC_EXCEPTION_DSI);
  324| 	}
  325| 
  326| 	return 0;
  327| }
  328| 
  329| 
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

End with one line: `FIXDRAFT_PPCBATPPKILL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
