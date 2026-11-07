# GXemul hardened fork -- DRAFT A FIX for one filed issue, `singlestepdecl` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `singlestepdecl`, state `open`, severity `LOW`)

**title:** debugger/debugger.c vs cpus/generate_head.c -- single_step_breakpoint is defined `volatile int` and declared `extern int` in every generated head -- HYGIENE (latent cross-TU UB)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T148 (class HYGIENE; reach B, build only; effort: one-line; report rows: A1-11).  Source URLs: https://github.com/retroprom/gxemul/commit/6d2d8bf0.  Our site at de8c7547: src/debugger/debugger.c:73; src/cpus/generate_head.c:119.  Portable fix: yes -- port upstream 6d2d8bf0 (bool in both).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream 6d2d8bf0

## The code at the cited lines

### `src/debugger/debugger.c` around the row's cited line 73 (HEAD 2d25df65, lines 28-118)

```c
   28|  *  Single-step debugger.
   29|  *
   30|  *
   31|  *  This entire module is very much non-reentrant. :-/  TODO: Fix.
   32|  */
   33| 
   34| #include <ctype.h>
   35| #include <signal.h>
   36| #include <stdio.h>
   37| #include <stdlib.h>
   38| #include <string.h>
   39| #include <unistd.h>
   40| 
   41| #include "console.h"
   42| #include "cpu.h"
   43| #include "device.h"
   44| #include "debugger.h"
   45| #include "diskimage.h"
   46| #include "emul.h"
   47| #include "machine.h"
   48| #include "memory.h"
   49| #include "misc.h"
   50| #include "net.h"
   51| #include "settings.h"
   52| #include "timer.h"
   53| #include "x11.h"
   54| 
   55| 
   56| extern int extra_argc;
   57| extern char **extra_argv;
   58| extern struct settings *global_settings;
   59| 
   60| extern int quiet_mode;
   61| extern int verbose;
   62| 
   63| 
   64| /*
   65|  *  Global debugger variables:
   66|  *
   67|  *  TODO: Some of these should be moved to some other place!
   68|  */
   69| 
   70| bool single_step = false;
   71| bool about_to_enter_single_step = false;
   72| bool debugger_enter_at_end_of_run = false;
   73| volatile int single_step_breakpoint = 0;
   74| 
   75| extern bool emul_shutdown;
   76| 
   77| int old_quiet_mode = 0;
   78| 
   79| static int debugger_n_steps_left_before_interaction = 0;
   80| static volatile bool exit_debugger;
   81| static volatile bool exit_debugger_to_continue_single_stepping;
   82| 
   83| /*
   84|  *  State for the "step call" command: when non-zero, the debugger keeps
   85|  *  single-stepping without user interaction until one of the cpus in the
   86|  *  focused machine traces a function call or function return (see
   87|  *  cpu_functioncall_trace() and cpu_functioncall_trace_return() in
   88|  *  src/cpus/cpu.c), or until CTRL-C is pressed. show_trace_tree is
   89|  *  implicitly enabled while stepping, and restored afterwards.
   90|  */
   91| static int debugger_stepping_until_function_transition = 0;
   92| static int debugger_old_show_trace_tree = 0;
   93| 
   94| 
   95| /*
   96|  *  Private (global) debugger variables:
   97|  */
   98| 
   99| static volatile int ctrl_c;
  100| 
  101| /*  Currently focused CPU, machine, and emulation:  */
  102| int debugger_cur_cpu;
  103| int debugger_cur_machine;
  104| static struct machine *debugger_machine;
  105| static struct emul *debugger_emul;
  106| 
  107| #define	MAX_CMD_BUFLEN		72
  108| #define	N_PREVIOUS_CMDS		150
  109| static char *last_cmd[N_PREVIOUS_CMDS];
  110| static int last_cmd_index;
  111| 
  112| static char repeat_cmd[MAX_CMD_BUFLEN];
  113| 
  114| #define	MAGIC_UNTOUCHED		0x98ca76c2ffcc0011ULL
  115| 
  116| static uint64_t last_dump_addr = MAGIC_UNTOUCHED;
  117| static uint64_t last_unasm_addr = MAGIC_UNTOUCHED;
  118| 
```

### `src/cpus/generate_head.c` around the row's cited line 119 (HEAD 2d25df65, lines 74-156)

```c
   74| 	printf("#define DYNTRANS_MAX_VPH_TLB_ENTRIES "
   75| 	    "%s_MAX_VPH_TLB_ENTRIES\n", uppercase(a));
   76| 	printf("#define DYNTRANS_ARCH %s\n", a);
   77| 	printf("#define DYNTRANS_%s\n", uppercase(a));
   78| 
   79| 	/*  For 64-bit platforms, arch_L2N, and arch_L3N must be defined.  */
   80| 	printf("#ifndef DYNTRANS_32\n");
   81| 	printf("#define DYNTRANS_L2N %s_L2N\n"
   82| 	    "#define DYNTRANS_L3N %s_L3N\n"
   83| 	    "#if !defined(%s_L2N) || !defined(%s_L3N)\n"
   84| 	    "#error arch_L2N, and arch_L3N must be defined for this arch!\n"
   85| 	    "#endif\n",
   86| 	    uppercase(a), uppercase(a), uppercase(a), uppercase(a));
   87| 	printf("#define DYNTRANS_L2_64_TABLE %s_l2_64_table\n"
   88| 	    "#define DYNTRANS_L3_64_TABLE %s_l3_64_table\n", a, a);
   89| 	printf("#endif\n");
   90| 
   91| 	/*  Default pagesize is 4KB.  */
   92| 	printf("#ifndef DYNTRANS_PAGESIZE\n"
   93| 	    "#define DYNTRANS_PAGESIZE 4096\n"
   94| 	    "#endif\n");
   95| 
   96| 	printf("#define DYNTRANS_IC %s_instr_call\n", a);
   97| 	printf("#define DYNTRANS_IC_ENTRIES_PER_PAGE "
   98| 	    "%s_IC_ENTRIES_PER_PAGE\n", uppercase(a));
   99| 	printf("#define DYNTRANS_INSTR_ALIGNMENT_SHIFT "
  100| 	    "%s_INSTR_ALIGNMENT_SHIFT\n", uppercase(a));
  101| 	printf("#define DYNTRANS_TC_PHYSPAGE %s_tc_physpage\n", a);
  102| 	printf("#define DYNTRANS_INVALIDATE_TLB_ENTRY "
  103| 	    "%s_invalidate_tlb_entry\n", a);
  104| 	printf("#define DYNTRANS_ADDR_TO_PAGENR %s_ADDR_TO_PAGENR\n",
  105| 	    uppercase(a));
  106| 	printf("#define DYNTRANS_PC_TO_IC_ENTRY %s_PC_TO_IC_ENTRY\n",
  107| 	    uppercase(a));
  108| 	printf("#define DYNTRANS_TC_ALLOCATE "
  109| 	    "%s_tc_allocate_default_page\n", a);
  110| 	printf("#define DYNTRANS_TC_PHYSPAGE %s_tc_physpage\n", a);
  111| 	printf("#define DYNTRANS_PC_TO_POINTERS %s_pc_to_pointers\n", a);
  112| 	printf("#define DYNTRANS_PC_TO_POINTERS_GENERIC "
  113| 	    "%s_pc_to_pointers_generic\n", a);
  114| 	printf("#define COMBINE_INSTRUCTIONS %s_combine_instructions\n", a);
  115| 	printf("#define DISASSEMBLE %s_cpu_disassemble_instr\n", a);
  116| 
  117| 	printf("\nextern bool single_step;\n"
  118| 	    "extern bool about_to_enter_single_step;\n"
  119| 	    "extern int single_step_breakpoint;\n"
  120| 	    "extern int old_quiet_mode;\n"
  121| 	    "extern int quiet_mode;\n");
  122| 
  123| 	printf("\n/* instr uses the same names as in "
  124| 	    "cpu_%s_instr.c */\n#define instr(n) %s_instr_ ## n\n\n", a, a);
  125| 
  126| 	printf("#ifdef DYNTRANS_DUALMODE_32\n"
  127| 	    "#define instr32(n) %s32_instr_ ## n\n\n", a);
  128| 	printf("#endif\n\n");
  129| 
  130| 	printf("\n#define X(n) void %s_instr_ ## n(struct cpu *cpu, \\\n"
  131| 	    " struct %s_instr_call *ic)\n", a, a);
  132| 
  133| 	printf("\n/*\n *  nothing:  Do nothing.\n *\n"
  134| 	    " *  The difference between this function and a \"nop\" "
  135| 	    "instruction is that\n *  this function does not increase "
  136| 	    "the program counter.  It is used to \"get out\" of running in "
  137| 	    "translated\n *  mode.\n */\n");
  138| 	printf("X(nothing)\n{\n");
  139| 	printf("\tcpu->cd.%s.next_ic --;\n", a);
  140| 	printf("\tcpu->ninstrs --;\n");
  141| 	printf("}\n\n");
  142| 
  143| 	/*  Ugly special hacks for SH[34]:  */
  144| 	if (strcasecmp(argv[1], "sh") == 0) {
  145| 	        printf("static struct %s_instr_call nothing_call = { "
  146| 		    "instr(nothing), {0,0} };\n", a);
  147| 	} else {
  148| 	        printf("static struct %s_instr_call nothing_call = { "
  149| 		    "instr(nothing), {0,0,0} };\n", a);
  150| 	}
  151| 
  152| 	printf("\n");
  153| 
  154| 	return 0;
  155| }
  156| 
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

End with one line: `FIXDRAFT_SINGLESTEPDECL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
