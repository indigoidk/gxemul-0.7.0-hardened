# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mipsllzero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mipsllzero`, state `open`)

**title:** src/cpus/cpu_mips_instr.c:5486-5490 -- a load-linked (LL or LLD) into $zero prints `HM... unusual load linked` and reaches goto bad, though the encoding is legal -- CPU-STOP (any privilege, ISA II and later)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 5486

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_mips_instr.c b/src/cpus/cpu_mips_instr.c
index 0df67fd9..a0d7e16a 100644
--- a/src/cpus/cpu_mips_instr.c
+++ b/src/cpus/cpu_mips_instr.c
@@ -5483,11 +5483,9 @@ X(to_be_translated)
 		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 		ic->arg[2] = (int32_t)imm;
-		if (!store && rt == MIPS_GPR_ZERO) {
-			if (!cpu->translation_readahead)
-				fatal("HM... unusual load linked\n");
-			goto bad;
-		}
+		/*  Load into the dummy scratch register, if rt = zero  */
+		if (!store && rt == MIPS_GPR_ZERO)
+			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 		break;
 
 	case HI6_LWL:
```

## Every edited function, after the fix

### `src/cpus/cpu_mips_instr.c` -- post-edit lines 4270-5803 (`+` marks a line the diff added or the point of a deletion)

```c
 4270|  X(to_be_translated)
 4271|  {
 4272|  	uint64_t addr, low_pc;
 4273|  	uint32_t iword, imm;
 4274|  	unsigned char *page;
     | [... lines 4275-5375 not shown ...]
 5376|  			 *  cpu_dyntrans.c, which sets cpu->running = 0 -- so
 5377|  			 *  before this, a guest executing any rt outside the
 5378|  			 *  implemented set (4-7, 0xd, 0xf, 0x14-0x17,
 5379|  			 *  0x1a-0x1e) halted the emulator instead of taking
 5380|  			 *  the exception real silicon takes.  Reproduced on
 5381|  			 *  both rigs with rt=0x15; the same encoding now
 5382|  			 *  raises RI and the guest kernel decides what to do.
 5383|  			 *
 5384|  			 *  The shape is the tree's own, two arms above: the
 5385|  			 *  trap opcodes on a pre-MIPS32 CPU already resolve to
 5386|  			 *  instr(reserved) behind a latched warning.  Upstream
 5387|  			 *  reached the same conclusion independently in the
 5388|  			 *  0.7.1 line it never released.
 5389|  			 *
 5390|  			 *  The warning is latched rather than verbosity-gated
 5391|  			 *  because it reports a DEFICIENCY of the emulator
 5392|  			 *  (an opcode nobody implemented), which #279 argues
 5393|  			 *  should survive into a quiet run exactly once --
 5394|  			 *  unlike #276's guest-answered diagnostics, which are
 5395|  			 *  gated.  translation_readahead still takes the old
 5396|  			 *  path: speculative decoding must not warn at all.
 5397|  			 */
 5398|  			if (cpu->translation_readahead)
 5399|  				goto bad;
 5400|  			else {
 5401|  				static int warned_regimm = 0;
 5402|  				if (!warned_regimm) {
 5403|  					warned_regimm = 1;
 5404|  					debugmsg_cpu(cpu, SUBSYS_CPU, "opcode",
 5405|  					    VERBOSITY_WARNING,
 5406|  					    "unimplemented REGIMM rt=%i -- "
 5407|  					    "raising Reserved Instruction. "
 5408|  					    "Only printing this once.", rt);
 5409|  				}
 5410|  				ic->f = instr(reserved);
 5411|  			}
 5412|  			break;
 5413|  		}
 5414|  		break;
 5415|  
 5416|  	case HI6_LB:
 5417|  	case HI6_LBU:
 5418|  	case HI6_SB:
 5419|  	case HI6_LH:
 5420|  	case HI6_LHU:
 5421|  	case HI6_SH:
 5422|  	case HI6_LW:
 5423|  	case HI6_LWU:
 5424|  	case HI6_SW:
 5425|  	case HI6_LD:
 5426|  	case HI6_SD:
 5427|  		/*  TODO: LWU should probably also be x64=1?  */
 5428|  		size = 2; signedness = 0; store = 0;
 5429|  		switch (main_opcode) {
 5430|  		case HI6_LB:  size = 0; signedness = 1; break;
 5431|  		case HI6_LBU: size = 0; break;
 5432|  		case HI6_LH:  size = 1; signedness = 1; break;
 5433|  		case HI6_LHU: size = 1; break;
 5434|  		case HI6_LW:  signedness = 1; break;
 5435|  		case HI6_LWU: break;
 5436|  		case HI6_LD:  size = 3; x64 = 1; break;
 5437|  		case HI6_SB:  store = 1; size = 0; break;
 5438|  		case HI6_SH:  store = 1; size = 1; break;
 5439|  		case HI6_SW:  store = 1; break;
 5440|  		case HI6_SD:  store = 1; size = 3; x64 = 1; break;
 5441|  		}
 5442|  
 5443|  		ic->f =
 5444|  #ifdef MODE32
 5445|  		    mips32_loadstore
 5446|  #else
 5447|  		    mips_loadstore
 5448|  #endif
 5449|  		    [ (cpu->byte_order == EMUL_LITTLE_ENDIAN? 0 : 16)
 5450|  		    + store * 8 + size * 2 + signedness];
 5451|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5452|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5453|  		ic->arg[2] = (int32_t)imm;
 5454|  
 5455|  		/*  Load into the dummy scratch register, if rt = zero  */
 5456|  		if (!store && rt == MIPS_GPR_ZERO)
 5457|  			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 5458|  
 5459|  		if (main_opcode == HI6_LW)
 5460|  			cpu->cd.mips.combination_check = COMBINE(lw);
 5461|  		if (main_opcode == HI6_SW)
 5462|  			cpu->cd.mips.combination_check = COMBINE(sw);
 5463|  		break;
 5464|  
 5465|  	case HI6_LL:
 5466|  	case HI6_LLD:
 5467|  	case HI6_SC:
 5468|  	case HI6_SCD:
 5469|  		/*  32-bit load-linked/store-condition for ISA II and up:  */
 5470|  		/*  (64-bit load-linked/store-condition for ISA III...)  */
 5471|  		if (cpu->cd.mips.cpu_type.isa_level < 2) {
 5472|  			ic->f = instr(reserved);
 5473|  			break;
 5474|  		}
 5475|  
 5476|  		store = 0;
 5477|  		switch (main_opcode) {
 5478|  		case HI6_LL:  ic->f = instr(ll); break;
 5479|  		case HI6_LLD: ic->f = instr(lld); x64 = 1; break;
 5480|  		case HI6_SC:  ic->f = instr(sc); store = 1; break;
 5481|  		case HI6_SCD: ic->f = instr(scd); store = 1; x64 = 1; break;
 5482|  		}
 5483|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5484|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5485|  		ic->arg[2] = (int32_t)imm;
 5486|+ 		/*  Load into the dummy scratch register, if rt = zero  */
 5487|+ 		if (!store && rt == MIPS_GPR_ZERO)
 5488|+ 			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 5489|  		break;
 5490|  
 5491|  	case HI6_LWL:
 5492|  	case HI6_LWR:
 5493|  	case HI6_LDL:
 5494|  	case HI6_LDR:
 5495|  	case HI6_SWL:
 5496|  	case HI6_SWR:
 5497|  	case HI6_SDL:
 5498|  	case HI6_SDR:
 5499|  		/*  TODO: replace these with faster versions...  */
 5500|  		store = 0;
 5501|  		switch (main_opcode) {
 5502|  		case HI6_LWL: ic->f = instr(lwl); break;
 5503|  		case HI6_LWR: ic->f = instr(lwr); break;
 5504|  		case HI6_LDL: ic->f = instr(ldl); x64 = 1; break;
 5505|  		case HI6_LDR: ic->f = instr(ldr); x64 = 1; break;
 5506|  		case HI6_SWL: ic->f = instr(swl); store = 1; break;
 5507|  		case HI6_SWR: ic->f = instr(swr); store = 1; break;
 5508|  		case HI6_SDL: ic->f = instr(sdl); store = 1; x64 = 1; break;
 5509|  		case HI6_SDR: ic->f = instr(sdr); store = 1; x64 = 1; break;
 5510|  		}
 5511|  		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5512|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5513|  		ic->arg[2] = (int32_t)imm;
 5514|  
 5515|  		/*  Load into the dummy scratch register, if rt = zero  */
 5516|  		if (!store && rt == MIPS_GPR_ZERO)
 5517|  			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 5518|  		break;
 5519|  
 5520|  	case HI6_LWC1:
 5521|  	case HI6_SWC1:
 5522|  	case HI6_LDC1:
 5523|  	case HI6_SDC1:
 5524|  		/*  64-bit floating-point load/store for ISA II and up...  */
 5525|  		if ((main_opcode == HI6_LDC1 || main_opcode == HI6_SDC1)
 5526|  		    && cpu->cd.mips.cpu_type.isa_level < 2) {
 5527|  			ic->f = instr(reserved);
 5528|  			break;
 5529|  		}
 5530|  
 5531|  		ic->arg[0] = (size_t)&cpu->cd.mips.coproc[1]->reg[rt];
 5532|  		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5533|  		ic->arg[2] = (int32_t)imm;
 5534|  		switch (main_opcode) {
 5535|  		case HI6_LWC1: ic->f = instr(lwc1); break;
 5536|  		case HI6_LDC1: ic->f = instr(ldc1); break;
 5537|  		case HI6_SWC1: ic->f = instr(swc1); break;
 5538|  		case HI6_SDC1: ic->f = instr(sdc1); break;
 5539|  		}
 5540|  
 5541|  		/*  Cause a coprocessor unusable exception if
 5542|  		    there is no floating point coprocessor:  */
 5543|  		if (cpu->cd.mips.cpu_type.flags & NOFPU ||
 5544|  		    cpu->cd.mips.coproc[1] == NULL) {
 5545|  			ic->f = instr(cpu);
 5546|  			ic->arg[0] = 1;
 5547|  		}
 5548|  		break;
     | [... lines 5549-5773 not shown ...]
 5774|  		ic->f = instr(cache);
 5775|  		break;
 5776|  
 5777|  	default:goto bad;
 5778|  	}
 5779|  
 5780|  
 5781|  #ifdef MODE32
 5782|  	if (x64) {
 5783|  		static int has_warned = 0;
 5784|  		if (!has_warned && !cpu->translation_readahead) {
 5785|  			fatal("[ WARNING/NOTE: attempt to execute a 64-bit"
 5786|  			    " instruction on an emulated 32-bit processor; "
 5787|  			    "pc=0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 5788|  			has_warned = 1;
 5789|  		}
 5790|  		if (cpu->translation_readahead)
 5791|  			goto bad;
 5792|  		else
 5793|  			ic->f = instr(reserved);
 5794|  	}
 5795|  #else
 5796|  	(void)x64; // avoid compiler warning
 5797|  #endif
 5798|  
 5799|  
 5800|  #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5801|  #include "cpu_dyntrans.c" 
 5802|  #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
 5803|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MIPSLLZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MIPSLLZERO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
