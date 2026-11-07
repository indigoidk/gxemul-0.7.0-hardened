# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `ppccrnandundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `ppccrnandundec`, state `open`)

**title:** cpus/cpu_ppc_instr.c XL decode -- crnand (19/225) is defined but missing from the CR case list -- CPU-STOP

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T124 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A4-9).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/2ec64fdde77aa73187fd80592679ea3f44e46fa2.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:4512-4531 (lines of de8c7547; at 987cb596 :4541-4560).  Portable fix: yes -- port rs6000 2ec64fd.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.  | 2026-11-05 (#575): X(crandc) now computes `ba & !bb` (Book I).  #575's pass-1 ruling notes for this round (adj_p1_20261105/MYTHOS_local.md, section 4): the draft here sketches `!(ba & bb)` as the crnand body -- the OLD crandc -- so crnand needs its own handler and must not alias `instr(crandc)`.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_ppc_instr.c` -- AT HEAD, lines 4084-5551 (`*` marks a line your previous draft changed)

```c
 4084|  X(to_be_translated)
 4085|  {
 4086|  	uint64_t addr, low_pc, tmp_addr;
 4087|  	uint32_t iword, mask;
 4088|  	unsigned char *page;
     | [... lines 4089-4521 not shown ...]
 4522|  			ic->f = instr(sc);
 4523|  		break;
 4524|  
 4525|  	case PPC_HI6_B:
 4526|  		aa_bit = (iword & 2) >> 1;
 4527|  		lk_bit = iword & 1;
 4528|  		tmp_addr = (int64_t)(int32_t)((iword & 0x03fffffc) << 6);
 4529|  		tmp_addr = (int64_t)tmp_addr >> 6;
 4530|  		if (lk_bit) {
 4531|  			if (cpu->machine->show_trace_tree) {
 4532|  				ic->f = instr(bl_trace);
 4533|  				samepage_function = instr(bl_samepage_trace);
 4534|  			} else {
 4535|  				ic->f = instr(bl);
 4536|  				samepage_function = instr(bl_samepage);
 4537|  			}
 4538|  		} else {
 4539|  			ic->f = instr(b);
 4540|  			samepage_function = instr(b_samepage);
 4541|  		}
 4542|  		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
 4543|  		ic->arg[1] = (addr & 0xffc) + 4;
 4544|  		/*  Branches are calculated as cur PC + offset.  */
 4545|  		/*  Special case: branch within the same page:  */
 4546|  		{
 4547|  			uint64_t mask_within_page =
 4548|  			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
 4549|  			uint64_t old_pc = addr;
 4550|  			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
 4551|  			if ((old_pc & ~mask_within_page) ==
 4552|  			    (new_pc & ~mask_within_page)) {
 4553|  				ic->f = samepage_function;
 4554|  				ic->arg[0] = (size_t) (
 4555|  				    cpu->cd.ppc.cur_ic_page +
 4556|  				    ((new_pc & mask_within_page) >> 2));
 4557|  			}
 4558|  		}
 4559|  		if (aa_bit) {
 4560|  			if (lk_bit) {
 4561|  				if (cpu->machine->show_trace_tree) {
 4562|  					ic->f = instr(bla_trace);
 4563|  				} else {
 4564|  					ic->f = instr(bla);
 4565|  				}
 4566|  			} else {
 4567|  				ic->f = instr(ba);
 4568|  			}
 4569|  			ic->arg[0] = (ssize_t)tmp_addr;
 4570|  		}
 4571|  		break;
 4572|  
 4573|  	case PPC_HI6_19:
 4574|  		xo = (iword >> 1) & 1023;
 4575|  		switch (xo) {
 4576|  
 4577|  		case PPC_19_BCLR:
 4578|  		case PPC_19_BCCTR:
 4579|  			bo = (iword >> 21) & 31;
 4580|  			bi = (iword >> 16) & 31;
 4581|  			bh = (iword >> 11) & 3;
 4582|  			lk_bit = iword & 1;
 4583|  			if (xo == PPC_19_BCLR) {
 4584|  				if (lk_bit)
 4585|  					ic->f = instr(bclr_l);
 4586|  				else {
 4587|  					ic->f = instr(bclr);
 4588|  					if (!cpu->machine->show_trace_tree &&
 4589|  					    (bo & 0x14) == 0x14)
 4590|  						ic->f = instr(bclr_20);
 4591|  				}
 4592|  			} else {
 4593|  				if (!(bo & 4)) {
 4594|  					if (!cpu->translation_readahead)
 4595|  						fatal("TODO: bclr/bcctr "
 4596|  						    "bo bit 2 clear!\n");
 4597|  					goto bad;
 4598|  				}
 4599|  				if (lk_bit)
 4600|  					ic->f = instr(bcctr_l);
 4601|  				else
 4602|  					ic->f = instr(bcctr);
 4603|  			}
 4604|  			ic->arg[0] = bo;
 4605|  			ic->arg[1] = 31 - bi;
 4606|  			ic->arg[2] = bh;
 4607|  			break;
 4608|  
 4609|  		case PPC_19_ISYNC:
 4610|  			/*  TODO  */
 4611|  			ic->f = instr(nop);
 4612|  			break;
 4613|  
 4614|  		case PPC_19_RFI:
 4615|  			ic->f = instr(rfi);
 4616|  			break;
 4617|  
 4618|  		case PPC_19_RFID:
 4619|  			ic->f = instr(rfid);
 4620|  			break;
 4621|  
 4622|  		case PPC_19_MCRF:
 4623|  			bf = (iword >> 23) & 7;
 4624|  			bfa = (iword >> 18) & 7;
 4625|  			ic->arg[0] = 28 - 4*bf;
 4626|  			ic->arg[1] = 28 - 4*bfa;
 4627|  			ic->f = instr(mcrf);
 4628|  			break;
 4629|  
 4630|  		case PPC_19_CRAND:
 4631|  		case PPC_19_CRANDC:
 4632|* 		case PPC_19_CREQV:
 4633|  		case PPC_19_CROR:
 4634|  		case PPC_19_CRORC:
 4635|  		case PPC_19_CRNOR:
 4636|  		case PPC_19_CRXOR:
 4637|  			switch (xo) {
 4638|  			case PPC_19_CRAND:  ic->f = instr(crand); break;
 4639|  			case PPC_19_CRANDC: ic->f = instr(crandc); break;
 4640|  			case PPC_19_CREQV:  ic->f = instr(creqv); break;
 4641|  			case PPC_19_CROR:   ic->f = instr(cror); break;
 4642|  			case PPC_19_CRORC:  ic->f = instr(crorc); break;
 4643|  			case PPC_19_CRNOR:  ic->f = instr(crnor); break;
 4644|  			case PPC_19_CRXOR:  ic->f = instr(crxor); break;
 4645|  			}
 4646|  			ic->arg[0] = iword;
 4647|  			break;
 4648|  
 4649|  		default:goto bad;
 4650|  		}
 4651|  		break;
 4652|  
 4653|  	case PPC_HI6_RLWNM:
 4654|  	case PPC_HI6_RLWINM:
 4655|  		ra = (iword >> 16) & 31;
 4656|  		mb = (iword >> 6) & 31;
 4657|  		me = (iword >> 1) & 31;   
 4658|  		rc = iword & 1;
 4659|  		mask = 0;
 4660|  		for (;;) {
 4661|  			mask |= ((uint32_t)0x80000000 >> mb);
 4662|  			if (mb == me)
 4663|  				break;
 4664|  			mb ++; mb &= 31;
 4665|  		}
 4666|  		switch (main_opcode) {
 4667|  		case PPC_HI6_RLWNM:
 4668|  			ic->f = rc? instr(rlwnm_dot) : instr(rlwnm); break;
 4669|  		case PPC_HI6_RLWINM:
 4670|  			ic->f = rc? instr(rlwinm_dot) : instr(rlwinm); break;
 4671|  		}
 4672|  		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4673|  		ic->arg[1] = mask;
 4674|  		ic->arg[2] = (uint32_t)iword;
 4675|  		break;
 4676|  
 4677|  	case PPC_HI6_RLWIMI:
 4678|  		rs = (iword >> 21) & 31;
 4679|  		ra = (iword >> 16) & 31;
 4680|  		ic->f = instr(rlwimi);
 4681|  		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4682|  		ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4683|  		ic->arg[2] = (uint32_t)iword;
 4684|  		break;
 4685|  
 4686|  	case PPC_HI6_LMW:
 4687|  	case PPC_HI6_STMW:
 4688|  		/*  NOTE: Loads use rt, not rs.  */
 4689|  		rs = (iword >> 21) & 31;
 4690|  		ra = (iword >> 16) & 31;
 4691|  		ic->arg[0] = rs;
 4692|  		if (ra == 0)
     | [... lines 4693-5521 not shown ...]
 5522|  				 *  source and nowhere else; masking it would
 5523|  				 *  break a legitimate write.
 5524|  				 */
 5525|  				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
 5526|  				    PPC_FPSCR_VX);
 5527|  				break;
 5528|  			default:goto bad;
 5529|  			}
 5530|  		}
 5531|  		/*
 5532|  		 *  #326: apply the record form. The NULL guard keeps the
 5533|  		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
 5534|  		 *  rejected when their low bit is set, because that is a
 5535|  		 *  reserved encoding and not a record form.
 5536|  		 */
 5537|  		if (rc) {
 5538|  			if (rc_f == NULL)
 5539|  				goto bad;
 5540|  			ic->f = rc_f;
 5541|  		}
 5542|  		break;
 5543|  
 5544|  	default:goto bad;
 5545|  	}
 5546|  
 5547|  
 5548|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5549|  #include "cpu_dyntrans.c"
 5550|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5551|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "\t\tcase PPC_19_CRAND:\n\t\tcase PPC_19_CRANDC:\n\t\tcase PPC_19_CREQV:",
    "new": "\t\tcase PPC_19_CRAND:\n\t\tcase PPC_19_CRANDC:\n\t\tcase PPC_19_CRNAND:\n\t\tcase PPC_19_CREQV:",
    "why": "Add crnand to the CR case list"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PPCCRNANDUNDEC: DEFECT, 1 FINDINGS
1. **Does the diff remove the defect the issue describes, at every site the issue names?** No. While it adds `PPC_19_CRNAND` to the outer case list, it fails to add it to the inner `switch (xo)` at `src/cpus/cpu_ppc_instr.c:4638`. Because of this omission, `ic->f` is never assigned a handler for `crnand`, leaving it uninitialized or preserving its previous value, which violates the issue note that "crnand needs its own handler".
2. **CONTROL FLOW:** No. The diff only adds a `case` label (line 4632) and falls through to the inner switch block; it does not add any `return`, `goto`, `break`, or early exit that skips the common tail. 
3. **RETURN VALUE:** No. The return values/types are unchanged by this diff.
4. **What ELSE does the diff change:** Nothing else directly, but due to the incomplete implementation, it leaves `ic->f` unset for `PPC_19_CRNAND`, which will execute whatever handler was left in the instruction context (or a null pointer), leading to undefined behavior or a crash upon execution.
5. **House idioms:** No house idioms are violated.
**Findings:**
`src/cpus/cpu_ppc_instr.c:4646`, DEFECT, `case PPC_19_CRNAND: ic->f = instr(crnand); break;`
FIXREVIEW_PPCCRNANDUNDEC: DEFECT, 1 FINDINGS
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_PPCCRNANDUNDEC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PPCCRNANDUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR REVISED DRAFT FAILED TO BUILD -- correct it (a build repair, not another review)

```text
tmp_ppc_head.c:42:18: error: 'ppc_instr_crnand' undeclared (first use in this function); did you mean 'ppc_instr_crand'?
tmp_ppc_tail.c:77:18: error: 'ppc32_instr_crnand' undeclared (first use in this function); did you mean 'ppc32_instr_crand'?
```

The build generates `ppc_instr_<name>` and `ppc32_instr_<name>` from each `X(<name>) { ... }` handler in
`src/cpus/cpu_ppc_instr.c`.  Referencing `crnand` therefore needs an `X(crnand) { ... }` handler defined in that file,
in the style of its siblings, shown here from HEAD:

### `src/cpus/cpu_ppc_instr.c` lines 2715-2774 (HEAD)

```c
 2715| /*
 2716|  *  crand, crxor etc:  Condition Register operations
 2717|  *
 2718|  *  arg[0] = copy of the instruction word
 2719|  */
 2720| X(crand) {
 2721| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2722| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2723| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2724| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2725| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2726| 	if (ba & bb)
 2727| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2728| }
 2729| X(crandc) {
 2730| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2731| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2732| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2733| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2734| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2735| 	if (ba & !bb)	/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
 2736| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2737| }
 2738| X(creqv) {
 2739| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2740| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2741| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2742| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2743| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2744| 	if (!(ba ^ bb))
 2745| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2746| }
 2747| X(cror) {
 2748| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2749| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2750| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2751| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2752| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2753| 	if (ba | bb)
 2754| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2755| }
 2756| X(crorc) {
 2757| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2758| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2759| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2760| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2761| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2762| 	if (ba | !bb)	/*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */
 2763| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2764| }
 2765| X(crnor) {
 2766| 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2767| 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2768| 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2769| 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2770| 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2771| 	if (!(ba | bb))
 2772| 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2773| }
 2774| X(crxor) {
```

Your revised edits:

```json
[
  {
    "file": "src/cpus/cpu_ppc_instr.c",
    "old": "\t\tcase PPC_19_CRAND:\n\t\tcase PPC_19_CRANDC:\n\t\tcase PPC_19_CREQV:\n\t\tcase PPC_19_CROR:\n\t\tcase PPC_19_CRORC:\n\t\tcase PPC_19_CRNOR:\n\t\tcase PPC_19_CRXOR:\n\t\t\tswitch (xo) {\n\t\t\tcase PPC_19_CRAND:  ic->f = instr(crand); break;\n\t\t\tcase PPC_19_CRANDC: ic->f = instr(crandc); break;\n\t\t\tcase PPC_19_CREQV:  ic->f = instr(creqv); break;\n\t\t\tcase PPC_19_CROR:   ic->f = instr(cror); break;\n\t\t\tcase PPC_19_CRORC:  ic->f = instr(crorc); break;\n\t\t\tcase PPC_19_CRNOR:  ic->f = instr(crnor); break;\n\t\t\tcase PPC_19_CRXOR:  ic->f = instr(crxor); break;\n\t\t\t}",
    "new": "\t\tcase PPC_19_CRAND:\n\t\tcase PPC_19_CRANDC:\n\t\tcase PPC_19_CREQV:\n\t\tcase PPC_19_CROR:\n\t\tcase PPC_19_CRORC:\n\t\tcase PPC_19_CRNOR:\n\t\tcase PPC_19_CRNAND:\n\t\tcase PPC_19_CRXOR:\n\t\t\tswitch (xo) {\n\t\t\tcase PPC_19_CRAND:  ic->f = instr(crand); break;\n\t\t\tcase PPC_19_CRANDC: ic->f = instr(crandc); break;\n\t\t\tcase PPC_19_CREQV:  ic->f = instr(creqv); break;\n\t\t\tcase PPC_19_CROR:   ic->f = instr(cror); break;\n\t\t\tcase PPC_19_CRORC:  ic->f = instr(crorc); break;\n\t\t\tcase PPC_19_CRNOR:  ic->f = instr(crnor); break;\n\t\t\tcase PPC_19_CRNAND: ic->f = instr(crnand); break;\n\t\t\tcase PPC_19_CRXOR:  ic->f = instr(crxor); break;\n\t\t\t}",
    "why": "Add crnand to both the outer CR instruction switch block and the inner handler assignment switch"
  }
]
```

Return the COMPLETE corrected edit list (it must define every handler it references), then end with the line
`FIXDRAFT_PPCCRNANDUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
