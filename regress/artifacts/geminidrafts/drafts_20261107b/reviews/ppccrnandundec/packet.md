# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppccrnandundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppccrnandundec`, state `open`)

**title:** cpus/cpu_ppc_instr.c XL decode -- crnand (19/225) is defined but missing from the CR case list -- CPU-STOP

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T124 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A4-9).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/2ec64fdde77aa73187fd80592679ea3f44e46fa2.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:4512-4531 (lines of de8c7547; at 987cb596 :4541-4560).  Portable fix: yes -- port rs6000 2ec64fd.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.  | 2026-11-05 (#575): X(crandc) now computes `ba & !bb` (Book I).  #575's pass-1 ruling notes for this round (adj_p1_20261105/MYTHOS_local.md, section 4): the draft here sketches `!(ba & bb)` as the crnand body -- the OLD crandc -- so crnand needs its own handler and must not alias `instr(crandc)`.

**The drafter's own reading:** STILL PRESENT: YES -- lines 4630-4645 do not include `PPC_19_CRNAND` in the inner or outer switch, and `X(crnand)` is undefined.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..559835f3 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -2735,6 +2735,16 @@ X(crandc) {
 	if (ba & !bb)	/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
 		cpu->cd.ppc.cr |= (1 << (31-bt));
 }
+
+X(crnand) {
+	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
+	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
+	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
+	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
+	cpu->cd.ppc.cr &= ~(1 << (31-bt));
+	if (!(ba & bb))
+		cpu->cd.ppc.cr |= (1 << (31-bt));
+}
 X(creqv) {
 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
@@ -4630,6 +4640,7 @@ X(to_be_translated)
 		case PPC_19_CRAND:
 		case PPC_19_CRANDC:
 		case PPC_19_CREQV:
+		case PPC_19_CRNAND:
 		case PPC_19_CROR:
 		case PPC_19_CRORC:
 		case PPC_19_CRNOR:
@@ -4638,6 +4649,7 @@ X(to_be_translated)
 			case PPC_19_CRAND:  ic->f = instr(crand); break;
 			case PPC_19_CRANDC: ic->f = instr(crandc); break;
 			case PPC_19_CREQV:  ic->f = instr(creqv); break;
+			case PPC_19_CRNAND: ic->f = instr(crnand); break;
 			case PPC_19_CROR:   ic->f = instr(cror); break;
 			case PPC_19_CRORC:  ic->f = instr(crorc); break;
 			case PPC_19_CRNOR:  ic->f = instr(crnor); break;
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 2706-2747 (`+` marks a line the diff added or the point of a deletion)

```c
 2706|  X(mcrf)
 2707|  {
 2708|  	int bf_shift = ic->arg[0], bfa_shift = ic->arg[1];
 2709|  	uint32_t tmp = (cpu->cd.ppc.cr >> bfa_shift) & 0xf;
 2710|  	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
 2711|  	cpu->cd.ppc.cr |= (tmp << bf_shift);
 2712|  }
 2713|  
 2714|  
 2715|  /*
 2716|   *  crand, crxor etc:  Condition Register operations
 2717|   *
 2718|   *  arg[0] = copy of the instruction word
 2719|   */
 2720|  X(crand) {
 2721|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2722|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2723|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2724|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2725|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2726|  	if (ba & bb)
 2727|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2728|  }
 2729|  X(crandc) {
 2730|  	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2731|  	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2732|  	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2733|  	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2734|  	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2735|  	if (ba & !bb)	/*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
 2736|  		cpu->cd.ppc.cr |= (1 << (31-bt));
 2737|  }
 2738|+ 
 2739|+ X(crnand) {
 2740|+ 	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
 2741|+ 	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
 2742|+ 	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
 2743|+ 	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
 2744|+ 	cpu->cd.ppc.cr &= ~(1 << (31-bt));
 2745|+ 	if (!(ba & bb))
 2746|+ 		cpu->cd.ppc.cr |= (1 << (31-bt));
 2747|+ }
```

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 4094-5563 (`+` marks a line the diff added or the point of a deletion)

```c
 4094|  X(to_be_translated)
 4095|  {
 4096|  	uint64_t addr, low_pc, tmp_addr;
 4097|  	uint32_t iword, mask;
 4098|  	unsigned char *page;
     | [... lines 4099-4532 not shown ...]
 4533|  		break;
 4534|  
 4535|  	case PPC_HI6_B:
 4536|  		aa_bit = (iword & 2) >> 1;
 4537|  		lk_bit = iword & 1;
 4538|  		tmp_addr = (int64_t)(int32_t)((iword & 0x03fffffc) << 6);
 4539|  		tmp_addr = (int64_t)tmp_addr >> 6;
 4540|  		if (lk_bit) {
 4541|  			if (cpu->machine->show_trace_tree) {
 4542|  				ic->f = instr(bl_trace);
 4543|  				samepage_function = instr(bl_samepage_trace);
 4544|  			} else {
 4545|  				ic->f = instr(bl);
 4546|  				samepage_function = instr(bl_samepage);
 4547|  			}
 4548|  		} else {
 4549|  			ic->f = instr(b);
 4550|  			samepage_function = instr(b_samepage);
 4551|  		}
 4552|  		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
 4553|  		ic->arg[1] = (addr & 0xffc) + 4;
 4554|  		/*  Branches are calculated as cur PC + offset.  */
 4555|  		/*  Special case: branch within the same page:  */
 4556|  		{
 4557|  			uint64_t mask_within_page =
 4558|  			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
 4559|  			uint64_t old_pc = addr;
 4560|  			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
 4561|  			if ((old_pc & ~mask_within_page) ==
 4562|  			    (new_pc & ~mask_within_page)) {
 4563|  				ic->f = samepage_function;
 4564|  				ic->arg[0] = (size_t) (
 4565|  				    cpu->cd.ppc.cur_ic_page +
 4566|  				    ((new_pc & mask_within_page) >> 2));
 4567|  			}
 4568|  		}
 4569|  		if (aa_bit) {
 4570|  			if (lk_bit) {
 4571|  				if (cpu->machine->show_trace_tree) {
 4572|  					ic->f = instr(bla_trace);
 4573|  				} else {
 4574|  					ic->f = instr(bla);
 4575|  				}
 4576|  			} else {
 4577|  				ic->f = instr(ba);
 4578|  			}
 4579|  			ic->arg[0] = (ssize_t)tmp_addr;
 4580|  		}
 4581|  		break;
 4582|  
 4583|  	case PPC_HI6_19:
 4584|  		xo = (iword >> 1) & 1023;
 4585|  		switch (xo) {
 4586|  
 4587|  		case PPC_19_BCLR:
 4588|  		case PPC_19_BCCTR:
 4589|  			bo = (iword >> 21) & 31;
 4590|  			bi = (iword >> 16) & 31;
 4591|  			bh = (iword >> 11) & 3;
 4592|  			lk_bit = iword & 1;
 4593|  			if (xo == PPC_19_BCLR) {
 4594|  				if (lk_bit)
 4595|  					ic->f = instr(bclr_l);
 4596|  				else {
 4597|  					ic->f = instr(bclr);
 4598|  					if (!cpu->machine->show_trace_tree &&
 4599|  					    (bo & 0x14) == 0x14)
 4600|  						ic->f = instr(bclr_20);
 4601|  				}
 4602|  			} else {
 4603|  				if (!(bo & 4)) {
 4604|  					if (!cpu->translation_readahead)
 4605|  						fatal("TODO: bclr/bcctr "
 4606|  						    "bo bit 2 clear!\n");
 4607|  					goto bad;
 4608|  				}
 4609|  				if (lk_bit)
 4610|  					ic->f = instr(bcctr_l);
 4611|  				else
 4612|  					ic->f = instr(bcctr);
 4613|  			}
 4614|  			ic->arg[0] = bo;
 4615|  			ic->arg[1] = 31 - bi;
 4616|  			ic->arg[2] = bh;
 4617|  			break;
 4618|  
 4619|  		case PPC_19_ISYNC:
 4620|  			/*  TODO  */
 4621|  			ic->f = instr(nop);
 4622|  			break;
 4623|  
 4624|  		case PPC_19_RFI:
 4625|  			ic->f = instr(rfi);
 4626|  			break;
 4627|  
 4628|  		case PPC_19_RFID:
 4629|  			ic->f = instr(rfid);
 4630|  			break;
 4631|  
 4632|  		case PPC_19_MCRF:
 4633|  			bf = (iword >> 23) & 7;
 4634|  			bfa = (iword >> 18) & 7;
 4635|  			ic->arg[0] = 28 - 4*bf;
 4636|  			ic->arg[1] = 28 - 4*bfa;
 4637|  			ic->f = instr(mcrf);
 4638|  			break;
 4639|  
 4640|  		case PPC_19_CRAND:
 4641|  		case PPC_19_CRANDC:
 4642|  		case PPC_19_CREQV:
 4643|+ 		case PPC_19_CRNAND:
 4644|  		case PPC_19_CROR:
 4645|  		case PPC_19_CRORC:
 4646|  		case PPC_19_CRNOR:
 4647|  		case PPC_19_CRXOR:
 4648|  			switch (xo) {
 4649|  			case PPC_19_CRAND:  ic->f = instr(crand); break;
 4650|  			case PPC_19_CRANDC: ic->f = instr(crandc); break;
 4651|  			case PPC_19_CREQV:  ic->f = instr(creqv); break;
 4652|+ 			case PPC_19_CRNAND: ic->f = instr(crnand); break;
 4653|  			case PPC_19_CROR:   ic->f = instr(cror); break;
 4654|  			case PPC_19_CRORC:  ic->f = instr(crorc); break;
 4655|  			case PPC_19_CRNOR:  ic->f = instr(crnor); break;
 4656|  			case PPC_19_CRXOR:  ic->f = instr(crxor); break;
 4657|  			}
 4658|  			ic->arg[0] = iword;
 4659|  			break;
 4660|  
 4661|  		default:goto bad;
 4662|  		}
 4663|  		break;
 4664|  
 4665|  	case PPC_HI6_RLWNM:
 4666|  	case PPC_HI6_RLWINM:
 4667|  		ra = (iword >> 16) & 31;
 4668|  		mb = (iword >> 6) & 31;
 4669|  		me = (iword >> 1) & 31;   
 4670|  		rc = iword & 1;
 4671|  		mask = 0;
 4672|  		for (;;) {
 4673|  			mask |= ((uint32_t)0x80000000 >> mb);
 4674|  			if (mb == me)
 4675|  				break;
 4676|  			mb ++; mb &= 31;
 4677|  		}
 4678|  		switch (main_opcode) {
 4679|  		case PPC_HI6_RLWNM:
 4680|  			ic->f = rc? instr(rlwnm_dot) : instr(rlwnm); break;
 4681|  		case PPC_HI6_RLWINM:
 4682|  			ic->f = rc? instr(rlwinm_dot) : instr(rlwinm); break;
 4683|  		}
 4684|  		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4685|  		ic->arg[1] = mask;
 4686|  		ic->arg[2] = (uint32_t)iword;
 4687|  		break;
 4688|  
 4689|  	case PPC_HI6_RLWIMI:
 4690|  		rs = (iword >> 21) & 31;
 4691|  		ra = (iword >> 16) & 31;
 4692|  		ic->f = instr(rlwimi);
 4693|  		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
 4694|  		ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4695|  		ic->arg[2] = (uint32_t)iword;
 4696|  		break;
 4697|  
 4698|  	case PPC_HI6_LMW:
 4699|  	case PPC_HI6_STMW:
 4700|  		/*  NOTE: Loads use rt, not rs.  */
 4701|  		rs = (iword >> 21) & 31;
 4702|  		ra = (iword >> 16) & 31;
 4703|  		ic->arg[0] = rs;
 4704|  		if (ra == 0)
 4705|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 4706|  		else
 4707|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4708|  		ic->arg[2] = (int32_t)(int16_t)iword;
 4709|  		switch (main_opcode) {
 4710|  		case PPC_HI6_LMW:
 4711|  			ic->f = instr(lmw);
 4712|  			break;
     | [... lines 4713-5533 not shown ...]
 5534|  				 *  source and nowhere else; masking it would
 5535|  				 *  break a legitimate write.
 5536|  				 */
 5537|  				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
 5538|  				    PPC_FPSCR_VX);
 5539|  				break;
 5540|  			default:goto bad;
 5541|  			}
 5542|  		}
 5543|  		/*
 5544|  		 *  #326: apply the record form. The NULL guard keeps the
 5545|  		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
 5546|  		 *  rejected when their low bit is set, because that is a
 5547|  		 *  reserved encoding and not a record form.
 5548|  		 */
 5549|  		if (rc) {
 5550|  			if (rc_f == NULL)
 5551|  				goto bad;
 5552|  			ic->f = rc_f;
 5553|  		}
 5554|  		break;
 5555|  
 5556|  	default:goto bad;
 5557|  	}
 5558|  
 5559|  
 5560|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5561|  #include "cpu_dyntrans.c"
 5562|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5563|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPCCRNANDUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPCCRNANDUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
