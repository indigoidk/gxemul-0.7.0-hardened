# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipsllzero` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipsllzero`, state `open`, severity `MED`)

**title:** src/cpus/cpu_mips_instr.c:5486-5490 -- a load-linked (LL or LLD) into $zero prints `HM... unusual load linked` and reaches goto bad, though the encoding is legal -- CPU-STOP (any privilege, ISA II and later)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- remove the goto bad and treat load-linked to $zero as a valid operation

## The code at the cited lines

### `src/cpus/cpu_mips_instr.c` around the row's cited line 5486 (HEAD 8d9df658, lines 5366-5606)

```c
 5366| 					warning = 1;
 5367| 				}
 5368| 				ic->f = instr(reserved);
 5369| 			}
 5370| 			break;
 5371| 
 5372| 		default:/*
 5373| 			 *  #309: an unimplemented REGIMM sub-opcode is a
 5374| 			 *  RESERVED INSTRUCTION, not a reason to stop the
 5375| 			 *  machine.  `goto bad` reaches the shared label in
 5376| 			 *  cpu_dyntrans.c, which sets cpu->running = 0 -- so
 5377| 			 *  before this, a guest executing any rt outside the
 5378| 			 *  implemented set (4-7, 0xd, 0xf, 0x14-0x17,
 5379| 			 *  0x1a-0x1e) halted the emulator instead of taking
 5380| 			 *  the exception real silicon takes.  Reproduced on
 5381| 			 *  both rigs with rt=0x15; the same encoding now
 5382| 			 *  raises RI and the guest kernel decides what to do.
 5383| 			 *
 5384| 			 *  The shape is the tree's own, two arms above: the
 5385| 			 *  trap opcodes on a pre-MIPS32 CPU already resolve to
 5386| 			 *  instr(reserved) behind a latched warning.  Upstream
 5387| 			 *  reached the same conclusion independently in the
 5388| 			 *  0.7.1 line it never released.
 5389| 			 *
 5390| 			 *  The warning is latched rather than verbosity-gated
 5391| 			 *  because it reports a DEFICIENCY of the emulator
 5392| 			 *  (an opcode nobody implemented), which #279 argues
 5393| 			 *  should survive into a quiet run exactly once --
 5394| 			 *  unlike #276's guest-answered diagnostics, which are
 5395| 			 *  gated.  translation_readahead still takes the old
 5396| 			 *  path: speculative decoding must not warn at all.
 5397| 			 */
 5398| 			if (cpu->translation_readahead)
 5399| 				goto bad;
 5400| 			else {
 5401| 				static int warned_regimm = 0;
 5402| 				if (!warned_regimm) {
 5403| 					warned_regimm = 1;
 5404| 					debugmsg_cpu(cpu, SUBSYS_CPU, "opcode",
 5405| 					    VERBOSITY_WARNING,
 5406| 					    "unimplemented REGIMM rt=%i -- "
 5407| 					    "raising Reserved Instruction. "
 5408| 					    "Only printing this once.", rt);
 5409| 				}
 5410| 				ic->f = instr(reserved);
 5411| 			}
 5412| 			break;
 5413| 		}
 5414| 		break;
 5415| 
 5416| 	case HI6_LB:
 5417| 	case HI6_LBU:
 5418| 	case HI6_SB:
 5419| 	case HI6_LH:
 5420| 	case HI6_LHU:
 5421| 	case HI6_SH:
 5422| 	case HI6_LW:
 5423| 	case HI6_LWU:
 5424| 	case HI6_SW:
 5425| 	case HI6_LD:
 5426| 	case HI6_SD:
 5427| 		/*  TODO: LWU should probably also be x64=1?  */
 5428| 		size = 2; signedness = 0; store = 0;
 5429| 		switch (main_opcode) {
 5430| 		case HI6_LB:  size = 0; signedness = 1; break;
 5431| 		case HI6_LBU: size = 0; break;
 5432| 		case HI6_LH:  size = 1; signedness = 1; break;
 5433| 		case HI6_LHU: size = 1; break;
 5434| 		case HI6_LW:  signedness = 1; break;
 5435| 		case HI6_LWU: break;
 5436| 		case HI6_LD:  size = 3; x64 = 1; break;
 5437| 		case HI6_SB:  store = 1; size = 0; break;
 5438| 		case HI6_SH:  store = 1; size = 1; break;
 5439| 		case HI6_SW:  store = 1; break;
 5440| 		case HI6_SD:  store = 1; size = 3; x64 = 1; break;
 5441| 		}
 5442| 
 5443| 		ic->f =
 5444| #ifdef MODE32
 5445| 		    mips32_loadstore
 5446| #else
 5447| 		    mips_loadstore
 5448| #endif
 5449| 		    [ (cpu->byte_order == EMUL_LITTLE_ENDIAN? 0 : 16)
 5450| 		    + store * 8 + size * 2 + signedness];
 5451| 		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5452| 		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5453| 		ic->arg[2] = (int32_t)imm;
 5454| 
 5455| 		/*  Load into the dummy scratch register, if rt = zero  */
 5456| 		if (!store && rt == MIPS_GPR_ZERO)
 5457| 			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 5458| 
 5459| 		if (main_opcode == HI6_LW)
 5460| 			cpu->cd.mips.combination_check = COMBINE(lw);
 5461| 		if (main_opcode == HI6_SW)
 5462| 			cpu->cd.mips.combination_check = COMBINE(sw);
 5463| 		break;
 5464| 
 5465| 	case HI6_LL:
 5466| 	case HI6_LLD:
 5467| 	case HI6_SC:
 5468| 	case HI6_SCD:
 5469| 		/*  32-bit load-linked/store-condition for ISA II and up:  */
 5470| 		/*  (64-bit load-linked/store-condition for ISA III...)  */
 5471| 		if (cpu->cd.mips.cpu_type.isa_level < 2) {
 5472| 			ic->f = instr(reserved);
 5473| 			break;
 5474| 		}
 5475| 
 5476| 		store = 0;
 5477| 		switch (main_opcode) {
 5478| 		case HI6_LL:  ic->f = instr(ll); break;
 5479| 		case HI6_LLD: ic->f = instr(lld); x64 = 1; break;
 5480| 		case HI6_SC:  ic->f = instr(sc); store = 1; break;
 5481| 		case HI6_SCD: ic->f = instr(scd); store = 1; x64 = 1; break;
 5482| 		}
 5483| 		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5484| 		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5485| 		ic->arg[2] = (int32_t)imm;
 5486| 		if (!store && rt == MIPS_GPR_ZERO) {
 5487| 			if (!cpu->translation_readahead)
 5488| 				fatal("HM... unusual load linked\n");
 5489| 			goto bad;
 5490| 		}
 5491| 		break;
 5492| 
 5493| 	case HI6_LWL:
 5494| 	case HI6_LWR:
 5495| 	case HI6_LDL:
 5496| 	case HI6_LDR:
 5497| 	case HI6_SWL:
 5498| 	case HI6_SWR:
 5499| 	case HI6_SDL:
 5500| 	case HI6_SDR:
 5501| 		/*  TODO: replace these with faster versions...  */
 5502| 		store = 0;
 5503| 		switch (main_opcode) {
 5504| 		case HI6_LWL: ic->f = instr(lwl); break;
 5505| 		case HI6_LWR: ic->f = instr(lwr); break;
 5506| 		case HI6_LDL: ic->f = instr(ldl); x64 = 1; break;
 5507| 		case HI6_LDR: ic->f = instr(ldr); x64 = 1; break;
 5508| 		case HI6_SWL: ic->f = instr(swl); store = 1; break;
 5509| 		case HI6_SWR: ic->f = instr(swr); store = 1; break;
 5510| 		case HI6_SDL: ic->f = instr(sdl); store = 1; x64 = 1; break;
 5511| 		case HI6_SDR: ic->f = instr(sdr); store = 1; x64 = 1; break;
 5512| 		}
 5513| 		ic->arg[0] = (size_t)&cpu->cd.mips.gpr[rt];
 5514| 		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5515| 		ic->arg[2] = (int32_t)imm;
 5516| 
 5517| 		/*  Load into the dummy scratch register, if rt = zero  */
 5518| 		if (!store && rt == MIPS_GPR_ZERO)
 5519| 			ic->arg[0] = (size_t)&cpu->cd.mips.scratch;
 5520| 		break;
 5521| 
 5522| 	case HI6_LWC1:
 5523| 	case HI6_SWC1:
 5524| 	case HI6_LDC1:
 5525| 	case HI6_SDC1:
 5526| 		/*  64-bit floating-point load/store for ISA II and up...  */
 5527| 		if ((main_opcode == HI6_LDC1 || main_opcode == HI6_SDC1)
 5528| 		    && cpu->cd.mips.cpu_type.isa_level < 2) {
 5529| 			ic->f = instr(reserved);
 5530| 			break;
 5531| 		}
 5532| 
 5533| 		ic->arg[0] = (size_t)&cpu->cd.mips.coproc[1]->reg[rt];
 5534| 		ic->arg[1] = (size_t)&cpu->cd.mips.gpr[rs];
 5535| 		ic->arg[2] = (int32_t)imm;
 5536| 		switch (main_opcode) {
 5537| 		case HI6_LWC1: ic->f = instr(lwc1); break;
 5538| 		case HI6_LDC1: ic->f = instr(ldc1); break;
 5539| 		case HI6_SWC1: ic->f = instr(swc1); break;
 5540| 		case HI6_SDC1: ic->f = instr(sdc1); break;
 5541| 		}
 5542| 
 5543| 		/*  Cause a coprocessor unusable exception if
 5544| 		    there is no floating point coprocessor:  */
 5545| 		if (cpu->cd.mips.cpu_type.flags & NOFPU ||
 5546| 		    cpu->cd.mips.coproc[1] == NULL) {
 5547| 			ic->f = instr(cpu);
 5548| 			ic->arg[0] = 1;
 5549| 		}
 5550| 		break;
 5551| 
 5552| 	case HI6_LWC2:
 5553| 	case HI6_SWC2:
 5554| 		/*  #580: coprocessor-2 word load and store.  Nothing in this
 5555| 		    tree creates a coprocessor-2 object and no coprocessor-2
 5556| 		    load or store is implemented, so the arm raises Coprocessor
 5557| 		    Unusable with Cause.CE = 2 whatever Status.CU2 holds, as the
 5558| 		    HI6_COP2 arm does.  With CU2 clear that is the architectural
 5559| 		    result at every ISA level; with CU2 set and no coprocessor,
 5560| 		    MIPS I-IV leave it undefined and MIPS32/64 Vol. II say
 5561| 		    Reserved Instruction, a distinction this arm does not make.
 5562| 		    Before this the words fell to default: goto bad, which
 5563| 		    stopped the emulated CPU from any privilege level.  */
 5564| 		ic->f = instr(cpu);
 5565| 		ic->arg[0] = 2;
 5566| 		break;
 5567| 
 5568| 	case HI6_LDC2:
 5569| 	case HI6_SDC2:
 5570| 		/*  #580: the doubleword forms are MIPS II; below that the
 5571| 		    encoding is reserved, as LDC1/SDC1 already are (above).
 5572| 		    From MIPS II on: Coprocessor Unusable, CE = 2, with the
 5573| 		    Status.CU2 note under HI6_LWC2 applying.  */
 5574| 		if (cpu->cd.mips.cpu_type.isa_level < 2) {
 5575| 			ic->f = instr(reserved);
 5576| 		} else {
 5577| 			ic->f = instr(cpu);
 5578| 			ic->arg[0] = 2;
 5579| 		}
 5580| 		break;
 5581| 
 5582| 	case HI6_SWC3:
 5583| 		/*  #580: through MIPS II, SWC3 is a coprocessor-3 store; no
 5584| 		    coprocessor-3 load or store is implemented, so it raises
 5585| 		    Coprocessor Unusable with CE = 3 whatever Status.CU3 holds.
 5586| 		    MIPS III removed the coprocessor-3 loads and stores and later
 5587| 		    levels through Release 5 keep the encoding reserved (Release
 5588| 		    6 reassigns it to PCREL; no Release 6 CPU is modelled), so
 5589| 		    from ISA III on it is a Reserved Instruction here (MIPS IV
 5590| 		    Instruction Set rev 3.2, Table A-39; R4000 User's Manual,
 5591| 		    Figure A-2).  Neither stops the CPU.  */
 5592| 		if (cpu->cd.mips.cpu_type.isa_level >= 3) {
 5593| 			ic->f = instr(reserved);
 5594| 		} else {
 5595| 			ic->f = instr(cpu);
 5596| 			ic->arg[0] = 3;
 5597| 		}
 5598| 		break;
 5599| 
 5600| 	case 0x1d:
 5601| 		/*  #580: JALX exists only with the MIPS16 ASE (MIPS16e
 5602| 		    included) or microMIPS.  This tree models neither -- the
 5603| 		    Config registers report no MIPS16 -- and without them the
 5604| 		    encoding is reserved through Release 5: it is a Reserved
 5605| 		    Instruction here (#309's REGIMM precedent), not a stopped
 5606| 		    CPU.  */
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

End with one line: `FIXDRAFT_MIPSLLZERO: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
