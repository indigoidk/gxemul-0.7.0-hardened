# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppctwundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppctwundec`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c:X(to_be_translated) -- twi (primary 3) and tw (31/4) are undecoded -- CPU-STOP (Linux/ppc MMIO accessors issue `twi`)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T122 (class CPU-STOP; reach U, user mode; effort: small-medium; report rows: A4-7, A(c)#4).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/02815906ef3d7a969aa5919885fa08e359a2b52c, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/6ac4dc4d64b06b80d6554dd9e8c725b04993decb, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/8bcf95a20ad8285503b81a2796f8430dd513cf10, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/ef62ef623c8c57b276f42e58c99dd9771063f5ec.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:5426, :5172; src/include/cpu_ppc.h:252-257.  Portable fix: yes -- port rs6000 0281590, rs6000 6ac4dc4, rs6000 8bcf95a, rs6000 ef62ef6 (also needs a program vector).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 0281590, 6ac4dc4, 8bcf95a, ef62ef6

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 5426 (HEAD 2d25df65, lines 5381-5471)

```c
 5381| 		case PPC_63_FNMSUB:	/*  #344  */
 5382| 		case PPC_63_FNMADD:	/*  #344  */
 5383| 			switch (xo & 31) {
 5384| 			case PPC_63_FMSUB: ic->f = instr(fmsub); rc_f = instr(fmsub_dot); break;
 5385| 			case PPC_63_FMADD: ic->f = instr(fmadd); rc_f = instr(fmadd_dot); break;
 5386| 			case PPC_63_FNMSUB: ic->f = instr(fnmsub); rc_f = instr(fnmsub_dot); break;
 5387| 			case PPC_63_FNMADD: ic->f = instr(fnmadd); rc_f = instr(fnmadd_dot); break;
 5388| 			}
 5389| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5390| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5391| 			ic->arg[2] = iword;
 5392| 			break;
 5393| 		case PPC_63_FSEL:	/*  #326  */
 5394| 			ic->f = instr(fsel); rc_f = instr(fsel_dot);
 5395| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5396| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5397| 			ic->arg[2] = iword;
 5398| 			break;
 5399| 		default:/*  Use all 10 bits of xo:  */
 5400| 			switch (xo) {
 5401| 			case PPC_63_FCMPU:
 5402| 				ic->f = instr(fcmpu);
 5403| 				ic->arg[0] = 28 - 4*(rt >> 2);
 5404| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
 5405| 				ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rb]);
 5406| 				break;
 5407| 			case PPC_63_FRSP:
 5408| 			case PPC_63_FCTIW:	/*  #326  */
 5409| 			case PPC_63_FCTIWZ:
 5410| 			case PPC_63_FNEG:
 5411| 			case PPC_63_FABS:
 5412| 			case PPC_63_FNABS:	/*  #326  */
 5413| 			case PPC_63_FMR:
 5414| 				switch (xo) {
 5415| 				case PPC_63_FRSP:   ic->f = instr(frsp); rc_f = instr(frsp_dot); break;
 5416| 				case PPC_63_FCTIW:  ic->f = instr(fctiw); rc_f = instr(fctiw_dot); break;
 5417| 				case PPC_63_FCTIWZ: ic->f = instr(fctiwz); rc_f = instr(fctiwz_dot);break;
 5418| 				case PPC_63_FNEG:   ic->f = instr(fneg); rc_f = instr(fneg_dot); break;
 5419| 				case PPC_63_FABS:   ic->f = instr(fabs); rc_f = instr(fabs_dot); break;
 5420| 				case PPC_63_FNABS:  ic->f = instr(fnabs); rc_f = instr(fnabs_dot); break;
 5421| 				case PPC_63_FMR:    ic->f = instr(fmr); rc_f = instr(fmr_dot); break;
 5422| 				}
 5423| 				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rb]);
 5424| 				ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rt]);
 5425| 				break;
 5426| 
 5427| 			/*
 5428| 			 *  #326: the FPSCR control group. BT is the five-bit
 5429| 			 *  rt field; BF and BFA are three bits each, sitting
 5430| 			 *  at the TOP of the rt and ra fields, hence the >> 2
 5431| 			 *  -- the same shape the fcmpu case above uses.
 5432| 			 */
 5433| 			case PPC_63_MTFSB0:
 5434| 			case PPC_63_MTFSB1:
 5435| 				if (xo == PPC_63_MTFSB0) {
 5436| 					ic->f = instr(mtfsb0);
 5437| 					rc_f  = instr(mtfsb0_dot);
 5438| 				} else {
 5439| 					ic->f = instr(mtfsb1);
 5440| 					rc_f  = instr(mtfsb1_dot);
 5441| 				}
 5442| 				ic->arg[0] = rt;
 5443| 				break;
 5444| 			case PPC_63_MTFSFI:
 5445| 				ic->f = instr(mtfsfi); rc_f = instr(mtfsfi_dot);
 5446| 				ic->arg[0] = 28 - 4*(rt >> 2);
 5447| 				/*  U is the four bits at ISA 16:19, which is
 5448| 				    the top of the rb field.  */
 5449| 				ic->arg[1] = (iword >> 12) & 0xf;
 5450| 				break;
 5451| 			case PPC_63_MCRFS:
 5452| 				ic->f = instr(mcrfs);
 5453| 				ic->arg[0] = 28 - 4*(rt >> 2);
 5454| 				ic->arg[1] = 28 - 4*(ra >> 2);
 5455| 				/*
 5456| 				 *  Book I lists, per BFA, exactly which of the
 5457| 				 *  copied bits are cleared. Four of the eight
 5458| 				 *  fields clear NOTHING -- and those are the
 5459| 				 *  ones that would hurt: field 4 is the FPCC,
 5460| 				 *  6 the exception enables, 7 the rounding
 5461| 				 *  mode. Computed here so the handler stays a
 5462| 				 *  mask-and-go.
 5463| 				 */
 5464| 				switch (ra >> 2) {
 5465| 				case 0:	/*  FX and OX; not FEX/VX  */
 5466| 					ic->arg[2] = 0x90000000; break;
 5467| 				case 1:	/*  UX ZX XX VXSNAN  */
 5468| 					ic->arg[2] = 0x0f000000; break;
 5469| 				case 2:	/*  VXISI VXIDI VXZDZ VXIMZ  */
 5470| 					ic->arg[2] = 0x00f00000; break;
 5471| 				case 3:	/*  VXVC only; NOT FR/FI/C  */
```

### `src/include/cpu_ppc.h` around the row's cited line 252 (HEAD 2d25df65, lines 207-288)

```c
  207| #define	PPC_FPSCR_VXCVI	(1 << 8)	/*  Invalid: integer convert  */
  208| #define	PPC_FPSCR_VE	(1 << 7)	/*  Invalid enable  */
  209| #define	PPC_FPSCR_OE	(1 << 6)	/*  Overflow enable  */
  210| #define	PPC_FPSCR_UE	(1 << 5)	/*  Underflow enable  */
  211| #define	PPC_FPSCR_ZE	(1 << 4)	/*  Zero divide enable  */
  212| #define	PPC_FPSCR_XE	(1 << 3)	/*  Inexact enable  */
  213| #define	PPC_FPSCR_NI	(1 << 2)	/*  Non-IEEE mode  */
  214| 
  215| /*
  216|  *  The nine Invalid Operation causes. VX is defined by Book I as the OR of
  217|  *  exactly these -- it is derived, not stored, and no instruction may write
  218|  *  it directly.
  219|  */
  220| #define	PPC_FPSCR_VX_CAUSES	(PPC_FPSCR_VXNAN | PPC_FPSCR_VXISI | \
  221| 				 PPC_FPSCR_VXIDI | PPC_FPSCR_VXZDZ | \
  222| 				 PPC_FPSCR_VXIMZ | PPC_FPSCR_VXVC | \
  223| 				 PPC_FPSCR_VXSOFT | PPC_FPSCR_VXSQRT | \
  224| 				 PPC_FPSCR_VXCVI)
  225| 
  226| /*
  227|  *  #330: every STICKY exception bit -- ISA 3:12 and 21:23. Moved here from
  228|  *  cpu_ppc_instr.c, which is compiled twice, so that ppc_fpscr_raise() in
  229|  *  cpu_ppc.c can see it too. The run stops at ISA 12 and resumes at 21
  230|  *  because bit 20 is reserved.
  231|  */
  232| #define	PPC_FPSCR_EXC_BITS	(PPC_FPSCR_OX | PPC_FPSCR_UX | \
  233| 				 PPC_FPSCR_ZX | PPC_FPSCR_XX | \
  234| 				 PPC_FPSCR_VX_CAUSES)
  235| 
  236| #define	PPC_FPSCR_FPCC	0x0000f000
  237| #define	PPC_FPSCR_FPCC_SHIFT	12
  238| #define	PPC_FPSCR_FL	(1 << 15)	/*  Less than  */
  239| #define	PPC_FPSCR_FG	(1 << 14)	/*  Greater than  */
  240| #define	PPC_FPSCR_FE	(1 << 13)	/*  Equal or Zero  */
  241| #define	PPC_FPSCR_FU	(1 << 12)	/*  Unordered or NaN  */
  242| /*  #304: the rounding-control field, FPSCR[30:31] in IBM numbering -- the two
  243|     LOWEST bits of the register.  The encoding (0 nearest, 1 toward zero,
  244|     2 toward +Inf, 3 toward -Inf) is numerically identical to this project's
  245|     IEEE_RM_* values, so `fpscr & PPC_FPSCR_RN_MASK` may be passed straight to
  246|     float_emul's mode-aware entry points.  The register was guest-writable and
  247|     decoded NOWHERE before #304: `frsp` narrowed with a host cast, which always
  248|     rounds to nearest, so three of the four architected modes were unreachable.  */
  249| #define	PPC_FPSCR_RN_MASK	0x3
  250| 
  251| /*  Exceptions:  */
  252| #define	PPC_EXCEPTION_MC	0x2	/*  Machine check, vector 0x200  */
  253| #define	PPC_EXCEPTION_DSI	0x3	/*  Data Storage Interrupt  */
  254| #define	PPC_EXCEPTION_ISI	0x4	/*  Instruction Storage Interrupt  */
  255| #define	PPC_EXCEPTION_EI	0x5	/*  External interrupt  */
  256| #define	PPC_EXCEPTION_FPU	0x8	/*  Floating-Point unavailable  */
  257| #define	PPC_EXCEPTION_DEC	0x9	/*  Decrementer  */
  258| #define	PPC_EXCEPTION_SC	0xc	/*  Syscall  */
  259| 
  260| /*  XER bits:  */
  261| #define	PPC_XER_SO	(1UL << 31)	/*  Summary Overflow  */
  262| #define	PPC_XER_OV	(1 << 30)	/*  Overflow  */
  263| #define	PPC_XER_CA	(1 << 29)	/*  Carry  */
  264| 
  265| 
  266| /*  cpu_ppc.c:  */
  267| int ppc_run_instr(struct cpu *cpu);
  268| int ppc32_run_instr(struct cpu *cpu);
  269| void ppc_exception(struct cpu *cpu, int exception_nr);
  270| void ppc_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
  271| 	unsigned char *host_page, int writeflag, uint64_t paddr_page);
  272| void ppc32_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
  273| 	unsigned char *host_page, int writeflag, uint64_t paddr_page);
  274| void ppc_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
  275| void ppc32_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
  276| void ppc_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
  277| void ppc32_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
  278| void ppc_init_64bit_dummy_tables(struct cpu *cpu);
  279| int ppc_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
  280| 	unsigned char *data, size_t len, int writeflag, int cache_flags);
  281| void ppc_cpu_family_init(struct cpu_family *);
  282| 
  283| /*  memory_ppc.c:  */
  284| int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
  285| 	uint64_t *return_addr, int flags);
  286| 
  287| #endif	/*  CPU_PPC_H  */
  288| 
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

End with one line: `FIXDRAFT_PPCTWUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
