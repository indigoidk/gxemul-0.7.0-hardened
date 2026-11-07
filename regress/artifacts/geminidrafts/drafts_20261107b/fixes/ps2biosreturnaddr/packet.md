# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ps2biosreturnaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ps2biosreturnaddr`, state `open`, severity `LOW`)

**title:** src/promemul/ps2_bios.c:179,190,209-216 -- the iop-heap allocator's static return_addr grows by the guest-supplied size with no bound and wraps, and the static is shared by every machine in the process -- WRAP (guest firmware call; the wrapped address is only handed back to the guest)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- move return_addr to machine-specific state and add bounds check

## The code at the cited lines

### `src/promemul/ps2_bios.c` around the row's cited line 179 (HEAD 8d9df658, lines 59-236)

```c
   59| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0x200;		/*  TODO  */
   60| 		break;
   61| 	case 1:			/*  halt(int mode)  */
   62| 		debug("[ SIFBIOS halt(0x%" PRIx64") ]\n",
   63| 		    (uint64_t) cpu->cd.mips.gpr[MIPS_GPR_A1]);
   64| 		cpu->running = 0;
   65| 		break;
   66| 	case 2:			/*  setdve(int mode)  */
   67| 		debug("[ SIFBIOS setdve(0x%" PRIx64") ]\n",
   68| 		    (uint64_t) cpu->cd.mips.gpr[MIPS_GPR_A1]);
   69| 		break;
   70| 	case 3:			/*  putchar(int ch)  */
   71| 		/*  debug("[ SIFBIOS putchar(0x%x) ]\n",
   72| 		    (char)cpu->cd.mips.gpr[MIPS_GPR_A1]);  */
   73| 		console_putchar(cpu->machine->main_console_handle,
   74| 		    cpu->cd.mips.gpr[MIPS_GPR_A1]);
   75| 		break;
   76| 	case 4:			/*  getchar()  */
   77| 		/*  This is untested. TODO  */
   78| 		/*  debug("[ SIFBIOS getchar() ]\n";  */
   79| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
   80| 		if (console_charavail(cpu->machine->main_console_handle))
   81| 			cpu->cd.mips.gpr[MIPS_GPR_V0] = console_readchar(
   82| 			    cpu->machine->main_console_handle);
   83| 		break;
   84| 	case 16:		/*  dma_init()  */
   85| 		debug("[ SIFBIOS dma_init() ]\n");
   86| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;		/*  TODO  */
   87| 		break;
   88| 	case 17:		/*  dma_exit()  */
   89| 		debug("[ SIFBIOS dma_exit() ]\n");
   90| 		break;
   91| 	case 32:		/*  cmd_init()  */
   92| 		debug("[ SIFBIOS cmd_init() ]\n");
   93| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;		/*  TODO  */
   94| 		break;
   95| 	case 33:		/*  cmd_exit()  */
   96| 		debug("[ SIFBIOS cmd_exit() ]\n");
   97| 		break;
   98| 	case 48:
   99| 		debug("[ SIFBIOS rpc_init(): TODO ]\n");
  100| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;		/*  TODO  */
  101| 		break;
  102| 	case 49:
  103| 		debug("[ SIFBIOS rpc_exit(): TODO ]\n");
  104| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;		/*  TODO  */
  105| 		break;
  106| 	case 51:
  107| 		debug("[ SIFBIOS rpc_bind(): TODO ]\n");
  108| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 1;		/*  TODO  */
  109| 		break;
  110| 	case 64:
  111| 		fatal("[ SIFBIOS SBR_IOPH_INIT(0x%" PRIx32",0x%" PRIx32",0x%"
  112| 		    PRIx32"): TODO ]\n",
  113| 		    (uint32_t) cpu->cd.mips.gpr[MIPS_GPR_A1],
  114| 		    (uint32_t) cpu->cd.mips.gpr[MIPS_GPR_A2],
  115| 		    (uint32_t) cpu->cd.mips.gpr[MIPS_GPR_A3]);
  116| 
  117| 		/*
  118| 		 *  This is really really ugly:   TODO
  119| 		 *
  120| 		 *  Linux and NetBSD seem to work, but it's an ugly hack.
  121| 		 *  This should really be a callback thingy...
  122| 		 *
  123| 		 *  NetBSD has a done-word which should be set to 1.
  124| 		 *  Linux has one done-word which should be set to 1, and
  125| 		 *  one which should be set to 0.
  126| 		 *
  127| 		 *  The code as it is right now probably overwrites stuff in
  128| 		 *  memory that shouldn't be touched. Not good.
  129| 		 *
  130| 		 *  Linux: err = sbios_rpc(SBR_IOPH_INIT, NULL, &result);
  131| 		 *         err should be 0 (just as NetBSD),
  132| 		 *         and result should be set to 0 as well.
  133| 		 */
  134| 		{
  135| 			uint32_t tmpaddr;
  136| 
  137| 			tmpaddr = load_32bit_word(cpu,
  138| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 0);
  139| 			fatal("  +0: %08x\n", tmpaddr);
  140| 			tmpaddr = load_32bit_word(cpu,
  141| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 4);
  142| 			fatal("  +4: %08x\n", tmpaddr);
  143| 			tmpaddr = load_32bit_word(cpu,
  144| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 8);
  145| 			fatal("  +8: %08x\n", tmpaddr);
  146| 			tmpaddr = load_32bit_word(cpu,
  147| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 12);
  148| 			fatal(" +12: %08x\n", tmpaddr);
  149| 
  150| 			/*  TODO: This is probably netbsd specific  */
  151| 			tmpaddr = load_32bit_word(cpu,
  152| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 12);
  153| 			fatal("tmpaddr 1 = 0x%08x\n", tmpaddr);
  154| 
  155| 			/*  "done" word for NetBSD:  */
  156| 			store_32bit_word(cpu, tmpaddr, 1);
  157| 			/*  "done" word A for Linux:  */
  158| 			store_32bit_word(cpu, tmpaddr + 4, 1);
  159| 			/*  "done" word B for Linux:  */
  160| 			store_32bit_word(cpu,
  161| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 0, 0);
  162| 		}
  163| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  164| 		break;
  165| 	case 65:
  166| 		fatal("[ SIFBIOS alloc iop heap(0x%" PRIx32") ]\n",
  167| 		    (uint32_t)cpu->cd.mips.gpr[MIPS_GPR_A1]);
  168| 
  169| 		/*
  170| 		 *  Linux uses this to allocate "heap" for the OHCI USB
  171| 		 *  controller.
  172| 		 *
  173| 		 *  TODO:  This naïve implementation does not allow for a
  174| 		 *  "free iop heap" function: :-/
  175| 		 */
  176| 
  177| 		{
  178| 			uint32_t tmpaddr;
  179| 			static uint32_t return_addr = 0x1000;
  180| 				/*  0xbc000000;  */
  181| 			uint32_t size;
  182| 
  183| 			tmpaddr = load_32bit_word(cpu,
  184| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 0);
  185| 			fatal("  +0: %08x (result should be placed here)\n",
  186| 			    tmpaddr);
  187| 			tmpaddr = load_32bit_word(cpu,
  188| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 4);
  189| 			fatal("  +4: %08x (*arg)\n", tmpaddr);
  190| 			size = load_32bit_word(cpu, tmpaddr + 0);
  191| 			fatal("      size = %08x\n", size);
  192| 			tmpaddr = load_32bit_word(cpu,
  193| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 8);
  194| 			fatal("  +8: %08x (*func (void *, int))\n", tmpaddr);
  195| 			tmpaddr = load_32bit_word(cpu,
  196| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 12);
  197| 			fatal(" +12: %08x (*para)\n", tmpaddr);
  198| 
  199| 			/*  TODO: This is probably netbsd specific  */
  200| 			tmpaddr = load_32bit_word(cpu,
  201| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 12);
  202| 			fatal("tmpaddr 1 = 0x%08x\n", tmpaddr);
  203| 
  204| 			/*  "done" word for NetBSD:  */
  205| 			store_32bit_word(cpu, tmpaddr, 1);
  206| 			/*  "done" word A for Linux:  */
  207| 			store_32bit_word(cpu, tmpaddr + 4, 1);
  208| 
  209| 			/*  Result:  */
  210| 			store_32bit_word(cpu,
  211| 			    cpu->cd.mips.gpr[MIPS_GPR_A1] + 0, return_addr);
  212| 
  213| 			return_addr += size;
  214| 			/*  Round up to next page:  */
  215| 			return_addr += 4095;
  216| 			return_addr &= ~4095;
  217| 		}
  218| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  219| 		break;
  220| 	case 66:
  221| 		debug("[ SIFBIOS iopmem_free(): TODO ]\n");
  222| 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;		/*  TODO  */
  223| 		break;
  224| 	default:
  225| 		quiet_mode = 0;
  226| 		cpu_register_dump(cpu->machine, cpu, 1, 0x1);
  227| 		printf("\n");
  228| 		fatal("Playstation 2 SIFBIOS emulation: "
  229| 		    "unimplemented call nr 0x%x\n", callnr);
  230| 		cpu->running = 0;
  231| 	}
  232| 
  233| 	return 1;
  234| }
  235| 
  236| 
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

End with one line: `FIXDRAFT_PS2BIOSRETURNADDR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_ps2biosreturnaddr//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
