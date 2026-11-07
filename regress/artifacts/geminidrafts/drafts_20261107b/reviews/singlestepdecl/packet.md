# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `singlestepdecl` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `singlestepdecl`, state `open`)

**title:** debugger/debugger.c vs cpus/generate_head.c -- single_step_breakpoint is defined `volatile int` and declared `extern int` in every generated head -- HYGIENE (latent cross-TU UB)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T148 (class HYGIENE; reach B, build only; effort: one-line; report rows: A1-11).  Source URLs: https://github.com/retroprom/gxemul/commit/6d2d8bf0.  Our site at de8c7547: src/debugger/debugger.c:73; src/cpus/generate_head.c:119.  Portable fix: yes -- port upstream 6d2d8bf0 (bool in both).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/debugger/debugger.c:73` and `src/cpus/generate_head.c:119`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/generate_head.c b/src/cpus/generate_head.c
index afd80e97..246c4223 100644
--- a/src/cpus/generate_head.c
+++ b/src/cpus/generate_head.c
@@ -116,7 +116,7 @@ int main(int argc, char *argv[])
 
 	printf("\nextern bool single_step;\n"
 	    "extern bool about_to_enter_single_step;\n"
-	    "extern int single_step_breakpoint;\n"
+	    "extern bool single_step_breakpoint;\n"
 	    "extern int old_quiet_mode;\n"
 	    "extern int quiet_mode;\n");
 
diff --git a/src/debugger/debugger.c b/src/debugger/debugger.c
index eb8e5d0e..b576ac9e 100644
--- a/src/debugger/debugger.c
+++ b/src/debugger/debugger.c
@@ -70,7 +70,7 @@ extern int verbose;
 bool single_step = false;
 bool about_to_enter_single_step = false;
 bool debugger_enter_at_end_of_run = false;
-volatile int single_step_breakpoint = 0;
+bool single_step_breakpoint = false;
 
 extern bool emul_shutdown;
```

## Every edited function, after the fix

### `src/cpus/generate_head.c` -- post-edit lines 54-155 (`+` marks a line the diff added or the point of a deletion)

```c
   54|  int main(int argc, char *argv[])
   55|  {
   56|  	char *a; //, *b;
   57|  
   58|  	if (argc != 3) {
   59|  		fprintf(stderr, "usage: %s arch Arch\n", argv[0]);
   60|  		fprintf(stderr, "Example: %s alpha Alpha\n", argv[0]);
   61|  		fprintf(stderr, "     or: %s arm ARM\n", argv[0]);
   62|  		exit(1);
   63|  	}
   64|  
   65|  	a = argv[1];
   66|  	// b = argv[2];
   67|  
   68|  
   69|  	printf("\n/*  AUTOMATICALLY GENERATED! Do not edit.  */\n\n");
   70|  
   71|  	printf("#include <assert.h>\n");
   72|  	printf("#include \"debugger.h\"\n");
   73|  
   74|  	printf("#define DYNTRANS_MAX_VPH_TLB_ENTRIES "
   75|  	    "%s_MAX_VPH_TLB_ENTRIES\n", uppercase(a));
   76|  	printf("#define DYNTRANS_ARCH %s\n", a);
   77|  	printf("#define DYNTRANS_%s\n", uppercase(a));
   78|  
   79|  	/*  For 64-bit platforms, arch_L2N, and arch_L3N must be defined.  */
   80|  	printf("#ifndef DYNTRANS_32\n");
   81|  	printf("#define DYNTRANS_L2N %s_L2N\n"
   82|  	    "#define DYNTRANS_L3N %s_L3N\n"
   83|  	    "#if !defined(%s_L2N) || !defined(%s_L3N)\n"
   84|  	    "#error arch_L2N, and arch_L3N must be defined for this arch!\n"
   85|  	    "#endif\n",
   86|  	    uppercase(a), uppercase(a), uppercase(a), uppercase(a));
   87|  	printf("#define DYNTRANS_L2_64_TABLE %s_l2_64_table\n"
   88|  	    "#define DYNTRANS_L3_64_TABLE %s_l3_64_table\n", a, a);
   89|  	printf("#endif\n");
   90|  
   91|  	/*  Default pagesize is 4KB.  */
   92|  	printf("#ifndef DYNTRANS_PAGESIZE\n"
   93|  	    "#define DYNTRANS_PAGESIZE 4096\n"
   94|  	    "#endif\n");
   95|  
   96|  	printf("#define DYNTRANS_IC %s_instr_call\n", a);
   97|  	printf("#define DYNTRANS_IC_ENTRIES_PER_PAGE "
   98|  	    "%s_IC_ENTRIES_PER_PAGE\n", uppercase(a));
   99|  	printf("#define DYNTRANS_INSTR_ALIGNMENT_SHIFT "
  100|  	    "%s_INSTR_ALIGNMENT_SHIFT\n", uppercase(a));
  101|  	printf("#define DYNTRANS_TC_PHYSPAGE %s_tc_physpage\n", a);
  102|  	printf("#define DYNTRANS_INVALIDATE_TLB_ENTRY "
  103|  	    "%s_invalidate_tlb_entry\n", a);
  104|  	printf("#define DYNTRANS_ADDR_TO_PAGENR %s_ADDR_TO_PAGENR\n",
  105|  	    uppercase(a));
  106|  	printf("#define DYNTRANS_PC_TO_IC_ENTRY %s_PC_TO_IC_ENTRY\n",
  107|  	    uppercase(a));
  108|  	printf("#define DYNTRANS_TC_ALLOCATE "
  109|  	    "%s_tc_allocate_default_page\n", a);
  110|  	printf("#define DYNTRANS_TC_PHYSPAGE %s_tc_physpage\n", a);
  111|  	printf("#define DYNTRANS_PC_TO_POINTERS %s_pc_to_pointers\n", a);
  112|  	printf("#define DYNTRANS_PC_TO_POINTERS_GENERIC "
  113|  	    "%s_pc_to_pointers_generic\n", a);
  114|  	printf("#define COMBINE_INSTRUCTIONS %s_combine_instructions\n", a);
  115|  	printf("#define DISASSEMBLE %s_cpu_disassemble_instr\n", a);
  116|  
  117|  	printf("\nextern bool single_step;\n"
  118|  	    "extern bool about_to_enter_single_step;\n"
  119|+ 	    "extern bool single_step_breakpoint;\n"
  120|  	    "extern int old_quiet_mode;\n"
  121|  	    "extern int quiet_mode;\n");
  122|  
  123|  	printf("\n/* instr uses the same names as in "
  124|  	    "cpu_%s_instr.c */\n#define instr(n) %s_instr_ ## n\n\n", a, a);
  125|  
  126|  	printf("#ifdef DYNTRANS_DUALMODE_32\n"
  127|  	    "#define instr32(n) %s32_instr_ ## n\n\n", a);
  128|  	printf("#endif\n\n");
  129|  
  130|  	printf("\n#define X(n) void %s_instr_ ## n(struct cpu *cpu, \\\n"
  131|  	    " struct %s_instr_call *ic)\n", a, a);
  132|  
  133|  	printf("\n/*\n *  nothing:  Do nothing.\n *\n"
  134|  	    " *  The difference between this function and a \"nop\" "
  135|  	    "instruction is that\n *  this function does not increase "
  136|  	    "the program counter.  It is used to \"get out\" of running in "
  137|  	    "translated\n *  mode.\n */\n");
  138|  	printf("X(nothing)\n{\n");
  139|  	printf("\tcpu->cd.%s.next_ic --;\n", a);
  140|  	printf("\tcpu->ninstrs --;\n");
  141|  	printf("}\n\n");
  142|  
  143|  	/*  Ugly special hacks for SH[34]:  */
  144|  	if (strcasecmp(argv[1], "sh") == 0) {
  145|  	        printf("static struct %s_instr_call nothing_call = { "
  146|  		    "instr(nothing), {0,0} };\n", a);
  147|  	} else {
  148|  	        printf("static struct %s_instr_call nothing_call = { "
  149|  		    "instr(nothing), {0,0,0} };\n", a);
  150|  	}
  151|  
  152|  	printf("\n");
  153|  
  154|  	return 0;
  155|  }
```

### `src/debugger/debugger.c` -- post-edit lines 13-133 (`+` marks a line the diff added or the point of a deletion)

```c
   13|   *     derived from this software without specific prior written permission.
   14|   *
   15|   *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|   *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|   *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|   *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|   *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|   *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|   *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|   *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|   *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|   *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|   *  SUCH DAMAGE.
   26|   *
   27|   *
   28|   *  Single-step debugger.
   29|   *
   30|   *
   31|   *  This entire module is very much non-reentrant. :-/  TODO: Fix.
   32|   */
   33|  
   34|  #include <ctype.h>
   35|  #include <signal.h>
   36|  #include <stdio.h>
   37|  #include <stdlib.h>
   38|  #include <string.h>
   39|  #include <unistd.h>
   40|  
   41|  #include "console.h"
   42|  #include "cpu.h"
   43|  #include "device.h"
   44|  #include "debugger.h"
   45|  #include "diskimage.h"
   46|  #include "emul.h"
   47|  #include "machine.h"
   48|  #include "memory.h"
   49|  #include "misc.h"
   50|  #include "net.h"
   51|  #include "settings.h"
   52|  #include "timer.h"
   53|  #include "x11.h"
   54|  
   55|  
   56|  extern int extra_argc;
   57|  extern char **extra_argv;
   58|  extern struct settings *global_settings;
   59|  
   60|  extern int quiet_mode;
   61|  extern int verbose;
   62|  
   63|  
   64|  /*
   65|   *  Global debugger variables:
   66|   *
   67|   *  TODO: Some of these should be moved to some other place!
   68|   */
   69|  
   70|  bool single_step = false;
   71|  bool about_to_enter_single_step = false;
   72|  bool debugger_enter_at_end_of_run = false;
   73|+ bool single_step_breakpoint = false;
   74|  
   75|  extern bool emul_shutdown;
   76|  
   77|  int old_quiet_mode = 0;
   78|  
   79|  static int debugger_n_steps_left_before_interaction = 0;
   80|  static volatile bool exit_debugger;
   81|  static volatile bool exit_debugger_to_continue_single_stepping;
   82|  
   83|  /*
   84|   *  State for the "step call" command: when non-zero, the debugger keeps
   85|   *  single-stepping without user interaction until one of the cpus in the
   86|   *  focused machine traces a function call or function return (see
   87|   *  cpu_functioncall_trace() and cpu_functioncall_trace_return() in
   88|   *  src/cpus/cpu.c), or until CTRL-C is pressed. show_trace_tree is
   89|   *  implicitly enabled while stepping, and restored afterwards.
   90|   */
   91|  static int debugger_stepping_until_function_transition = 0;
   92|  static int debugger_old_show_trace_tree = 0;
   93|  
   94|  
   95|  /*
   96|   *  Private (global) debugger variables:
   97|   */
   98|  
   99|  static volatile int ctrl_c;
  100|  
  101|  /*  Currently focused CPU, machine, and emulation:  */
  102|  int debugger_cur_cpu;
  103|  int debugger_cur_machine;
  104|  static struct machine *debugger_machine;
  105|  static struct emul *debugger_emul;
  106|  
  107|  #define	MAX_CMD_BUFLEN		72
  108|  #define	N_PREVIOUS_CMDS		150
  109|  static char *last_cmd[N_PREVIOUS_CMDS];
  110|  static int last_cmd_index;
  111|  
  112|  static char repeat_cmd[MAX_CMD_BUFLEN];
  113|  
  114|  #define	MAGIC_UNTOUCHED		0x98ca76c2ffcc0011ULL
  115|  
  116|  static uint64_t last_dump_addr = MAGIC_UNTOUCHED;
  117|  static uint64_t last_unasm_addr = MAGIC_UNTOUCHED;
  118|  
  119|  
  120|  /*
  121|   *  debugger_readchar():
  122|   */
  123|  char debugger_readchar(void)
  124|  {
  125|  	int ch;
  126|  
  127|  	while ((ch = console_readchar(MAIN_CONSOLE)) < 0 && !exit_debugger) {
  128|  		/*  Check for X11 events:  */
  129|  		x11_check_event(debugger_emul);
  130|  
  131|  		/*  Give up some CPU time:  */
  132|  		usleep(10000);
  133|  	}
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SINGLESTEPDECL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SINGLESTEPDECL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
