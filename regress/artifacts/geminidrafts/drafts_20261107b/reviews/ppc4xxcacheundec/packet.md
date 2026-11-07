# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ppc4xxcacheundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ppc4xxcacheundec`, state `open`)

**title:** src/cpus/cpu_ppc_instr.c:5201 -- dccci and iccci (defined in opcodes_ppc.h, no case) reach the opcode-31 default `goto bad` on the PPC405GP model -- CPU-STOP (PPC405GP only via -C)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_ppc_instr.c:5290

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 508e9181..4151d131 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -5287,6 +5287,10 @@ X(to_be_translated)
 			ic->f = load? instr(lvx) : instr(stvx);
 			break;
 
+		case PPC_31_DCCCI:
+		case PPC_31_ICCCI:
+			ic->f = instr(nop);
+			break;
 		default:goto bad;
 		}
 		break;
```

## Every edited function, after the fix

### `src/cpus/cpu_ppc_instr.c` -- post-edit lines 4084-5555 (`+` marks a line the diff added or the point of a deletion)

```c
 4084|  X(to_be_translated)
 4085|  {
 4086|  	uint64_t addr, low_pc, tmp_addr;
 4087|  	uint32_t iword, mask;
 4088|  	unsigned char *page;
     | [... lines 4089-5179 not shown ...]
 5180|  		case PPC_31_MULLW:
 5181|  		case PPC_31_MULHW:
 5182|  		case PPC_31_MULHWU:
 5183|  		case PPC_31_DIVW:
 5184|  		case PPC_31_DIVWU:
 5185|  		case PPC_31_ADD:
 5186|  		case PPC_31_ADDC:
 5187|  		case PPC_31_ADDE:
 5188|  		case PPC_31_ADDME:
 5189|  		case PPC_31_ADDZE:
 5190|  		case PPC_31_SUBF:
 5191|  		case PPC_31_SUBFC:
 5192|  		case PPC_31_SUBFE:
 5193|  		case PPC_31_SUBFME:
 5194|  		case PPC_31_SUBFZE:
 5195|  			rt = (iword >> 21) & 31;
 5196|  			ra = (iword >> 16) & 31;
 5197|  			rb = (iword >> 11) & 31;
 5198|  			oe_bit = (iword >> 10) & 1;
 5199|  			rc = iword & 1;
 5200|  			if (oe_bit) {
 5201|  				if (!cpu->translation_readahead)
 5202|  					fatal("oe_bit not yet implemented\n");
 5203|  				goto bad;
 5204|  			}
 5205|  			switch (xo) {
 5206|  			case PPC_31_MULLW:  ic->f = instr(mullw); break;
 5207|  			case PPC_31_MULHW:  ic->f = instr(mulhw); break;
 5208|  			case PPC_31_MULHWU: ic->f = instr(mulhwu); break;
 5209|  			case PPC_31_DIVW:   ic->f = instr(divw); n64=1; break;
 5210|  			case PPC_31_DIVWU:  ic->f = instr(divwu); n64=1; break;
 5211|  			case PPC_31_ADD:    ic->f = instr(add); break;
 5212|  			case PPC_31_ADDC:   ic->f = instr(addc); n64=1; break;
 5213|  			case PPC_31_ADDE:   ic->f = instr(adde); n64=1; break;
 5214|  			case PPC_31_ADDME:  ic->f = instr(addme); n64=1; break;
 5215|  			case PPC_31_ADDZE:  ic->f = instr(addze); n64=1; break;
 5216|  			case PPC_31_SUBF:   ic->f = instr(subf); break;
 5217|  			case PPC_31_SUBFC:  ic->f = instr(subfc); break;
 5218|  			case PPC_31_SUBFE:  ic->f = instr(subfe); n64=1; break;
 5219|  			case PPC_31_SUBFME: ic->f = instr(subfme); n64=1; break;
 5220|  			case PPC_31_SUBFZE: ic->f = instr(subfze); n64=1;break;
 5221|  			}
 5222|  			if (rc) {
 5223|  				switch (xo) {
 5224|  				case PPC_31_ADD:
 5225|  					ic->f = instr(add_dot); break;
 5226|  				case PPC_31_ADDE:
 5227|  					ic->f = instr(adde_dot); break;
 5228|  				case PPC_31_ADDME:
 5229|  					ic->f = instr(addme_dot); break;
 5230|  				case PPC_31_ADDZE:
 5231|  					ic->f = instr(addze_dot); break;
 5232|  				case PPC_31_DIVW:
 5233|  					ic->f = instr(divw_dot); break;
 5234|  				case PPC_31_DIVWU:
 5235|  					ic->f = instr(divwu_dot); break;
 5236|  				case PPC_31_MULLW:
 5237|  					ic->f = instr(mullw_dot); break;
 5238|  				case PPC_31_MULHW:
 5239|  					ic->f = instr(mulhw_dot); break;
 5240|  				case PPC_31_MULHWU:
 5241|  					ic->f = instr(mulhwu_dot); break;
 5242|  				case PPC_31_SUBF:
 5243|  					ic->f = instr(subf_dot); break;
 5244|  				case PPC_31_SUBFC:
 5245|  					ic->f = instr(subfc_dot); break;
 5246|  				case PPC_31_SUBFE:
 5247|  					ic->f = instr(subfe_dot); break;
 5248|  				case PPC_31_SUBFME:
 5249|  					ic->f = instr(subfme_dot); break;
 5250|  				case PPC_31_SUBFZE:
 5251|  					ic->f = instr(subfze_dot); break;
 5252|  				default:if (!cpu->translation_readahead)
 5253|  						fatal("RC bit not yet "
 5254|  						    "implemented\n");
 5255|  					goto bad;
 5256|  				}
 5257|  			}
 5258|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5259|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5260|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
 5261|  			if (cpu->cd.ppc.bits == 64 && n64) {
 5262|  				if (!cpu->translation_readahead)
 5263|  					fatal("Not yet for 64-bit mode\n");
 5264|  				goto bad;
 5265|  			}
 5266|  			break;
 5267|  
 5268|  		case PPC_31_LVX:
 5269|  		case PPC_31_LVXL:
 5270|  		case PPC_31_STVX:
 5271|  		case PPC_31_STVXL:
 5272|  			load = 0;
 5273|  			switch (xo) {
 5274|  			case PPC_31_LVX:
 5275|  			case PPC_31_LVXL:
 5276|  				load = 1; break;
 5277|  			}
 5278|  			rs = (iword >> 21) & 31;
 5279|  			ra = (iword >> 16) & 31;
 5280|  			rb = (iword >> 11) & 31;
 5281|  			ic->arg[0] = rs;
 5282|  			if (ra == 0)
 5283|  				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
 5284|  			else
 5285|  				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 5286|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
 5287|  			ic->f = load? instr(lvx) : instr(stvx);
 5288|  			break;
 5289|  
 5290|+ 		case PPC_31_DCCCI:
 5291|+ 		case PPC_31_ICCCI:
 5292|+ 			ic->f = instr(nop);
 5293|+ 			break;
 5294|  		default:goto bad;
 5295|  		}
 5296|  		break;
 5297|  
 5298|  	case PPC_HI6_59:
 5299|  		xo = (iword >>  1) & 1023;
 5300|  		rt = (iword >> 21) & 31;
 5301|  		ra = (iword >> 16) & 31;
 5302|  		rb = (iword >> 11) & 31;
 5303|  		rs = (iword >>  6) & 31;	/*  actually frc  */
 5304|  		rc = iword & 1;
 5305|  
 5306|  		/*
 5307|  		 *  #326: Rc=1 no longer stops the emulator. Each case below
 5308|  		 *  sets rc_f to its record-form twin, and the substitution is
 5309|  		 *  applied once, after the switch. A case that forgets to set
 5310|  		 *  rc_f leaves it NULL and still reaches `goto bad` -- so a
 5311|  		 *  missed record form stays a loud halt rather than becoming a
 5312|  		 *  silent no-op that executes but never writes CR1. (The
 5313|  		 *  integer block uses the same rc_f shape with no such guard.)
 5314|  		 */
 5315|  		rc_f = NULL;
 5316|  
 5317|  		/*  NOTE: Some floating-point instructions are selected
 5318|  		    using only the lowest 5 bits, not all 10!  */
 5319|  		switch (xo & 31) {
 5320|  		case PPC_59_FDIVS:
 5321|  		case PPC_59_FSUBS:
 5322|  		case PPC_59_FADDS:
 5323|  			switch (xo & 31) {
 5324|  			case PPC_59_FDIVS: ic->f = instr(fdivs); rc_f = instr(fdivs_dot); break;
 5325|  			case PPC_59_FSUBS: ic->f = instr(fsubs); rc_f = instr(fsubs_dot); break;
 5326|  			case PPC_59_FADDS: ic->f = instr(fadds); rc_f = instr(fadds_dot); break;
 5327|  			}
 5328|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5329|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rb]);
 5330|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5331|  			break;
 5332|  		case PPC_59_FMULS:
 5333|  			ic->f = instr(fmuls); rc_f = instr(fmuls_dot);
 5334|  			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5335|  			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5336|  			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rs]); /* frc */
 5337|  			break;
 5338|  		default:/*  Use all 10 bits of xo:  */
 5339|  			switch (xo) {
 5340|  			default:goto bad;
 5341|  			}
 5342|  		}
 5343|  		/*  #326: apply the record form, guarded.  */
 5344|  		if (rc) {
 5345|  			if (rc_f == NULL)
 5346|  				goto bad;
 5347|  			ic->f = rc_f;
 5348|  		}
 5349|  		break;
 5350|  
 5351|  	case PPC_HI6_63:
 5352|  		xo = (iword >>  1) & 1023;
 5353|  		rt = (iword >> 21) & 31;
     | [... lines 5354-5525 not shown ...]
 5526|  				 *  source and nowhere else; masking it would
 5527|  				 *  break a legitimate write.
 5528|  				 */
 5529|  				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
 5530|  				    PPC_FPSCR_VX);
 5531|  				break;
 5532|  			default:goto bad;
 5533|  			}
 5534|  		}
 5535|  		/*
 5536|  		 *  #326: apply the record form. The NULL guard keeps the
 5537|  		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
 5538|  		 *  rejected when their low bit is set, because that is a
 5539|  		 *  reserved encoding and not a record form.
 5540|  		 */
 5541|  		if (rc) {
 5542|  			if (rc_f == NULL)
 5543|  				goto bad;
 5544|  			ic->f = rc_f;
 5545|  		}
 5546|  		break;
 5547|  
 5548|  	default:goto bad;
 5549|  	}
 5550|  
 5551|  
 5552|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5553|  #include "cpu_dyntrans.c"
 5554|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5555|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PPC4XXCACHEUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PPC4XXCACHEUNDEC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
