# GXemul hardened fork -- DRAFT A FIX for one filed issue, `dyntransstatsbuf` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `dyntransstatsbuf`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_dyntrans.c:44,63-98 -- gather_statistics() appends with snprintf(buf + strlen(buf), sizeof(buf), ...), so the size passed never shrinks and a long -s field list writes past the 60-byte stack buffer -- OOB-WRITE (host -s option only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- snprintf size parameter must be the remaining buffer size, not the total size.

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 44 (HEAD 8d9df658, lines 1-164)

```c
    1| /*
    2|  *  Copyright (C) 2005-2021  Anders Gavare.  All rights reserved.
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
   28|  *  Common dyntrans routines. Included from cpu_*.c.
   29|  *
   30|  *  Note: This might be a bit hard to follow, if you are reading this source
   31|  *  code for the first time. It is basically a hack to implement "templates"
   32|  *  with normal C code, by using suitable defines/macros, and then including
   33|  *  this file.
   34|  */
   35| 
   36| 
   37| #ifndef STATIC_STUFF
   38| #define	STATIC_STUFF
   39| /*
   40|  *  gather_statistics():
   41|  */
   42| static void gather_statistics(struct cpu *cpu)
   43| {
   44| 	char ch, buf[60];
   45| 	struct DYNTRANS_IC *ic = cpu->cd.DYNTRANS_ARCH.next_ic;
   46| 	int i = 0;
   47| 	uint64_t a;
   48| 	int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - (size_t)
   49| 	    cpu->cd.DYNTRANS_ARCH.cur_ic_page) / sizeof(struct DYNTRANS_IC);
   50| 
   51| 	if (cpu->machine->statistics.file == NULL) {
   52| 		fatal("statistics gathering with no filename set is"
   53| 		    " meaningless\n");
   54| 		return;
   55| 	}
   56| 
   57| 	/*  low_pc must be within the page!  */
   58| 	if (low_pc < 0 || low_pc > DYNTRANS_IC_ENTRIES_PER_PAGE)
   59| 		return;
   60| 
   61| 	buf[0] = '\0';
   62| 
   63| 	while ((ch = cpu->machine->statistics.fields[i]) != '\0') {
   64| 		if (i != 0)
   65| 			strlcat(buf, " ", sizeof(buf));
   66| 
   67| 		switch (ch) {
   68| 		case 'i':
   69| 			snprintf(buf + strlen(buf), sizeof(buf),
   70| 			    "%p", (void *)ic->f);
   71| 			break;
   72| 		case 'p':
   73| 			/*  Physical program counter address:  */
   74| 			cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
   75| 			    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
   76| 			a = cpu->cd.DYNTRANS_ARCH.cur_physpage->physaddr;
   77| 			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   78| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   79| 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   80| 			if (cpu->is_32bit)
   81| 				snprintf(buf + strlen(buf), sizeof(buf),
   82| 				    "0x%08" PRIx32, (uint32_t)a);
   83| 			else
   84| 				snprintf(buf + strlen(buf), sizeof(buf),
   85| 				    "0x%016" PRIx64, (uint64_t)a);
   86| 			break;
   87| 		case 'v':
   88| 			/*  Virtual program counter address:  */
   89| 			a = cpu->pc;
   90| 			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   91| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   92| 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   93| 			if (cpu->is_32bit)
   94| 				snprintf(buf + strlen(buf), sizeof(buf),
   95| 				    "0x%08" PRIx32, (uint32_t)a);
   96| 			else
   97| 				snprintf(buf + strlen(buf), sizeof(buf),
   98| 				    "0x%016" PRIx64, (uint64_t)a);
   99| 			break;
  100| 		}
  101| 		i++;
  102| 	}
  103| 
  104| 	fprintf(cpu->machine->statistics.file, "%s\n", buf);
  105| }
  106| 
  107| 
  108| #define S		gather_statistics(cpu)
  109| 
  110| 
  111| #if 1
  112| 
  113| /*  The normal instruction execution core:  */
  114| #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; ic->f(cpu, ic);
  115| 
  116| #else
  117| 
  118| /*  For heavy debugging:  */
  119| #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++;	\
  120| 		{	\
  121| 			int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - \
  122| 			    (size_t)cpu->cd.DYNTRANS_ARCH.cur_ic_page) / \
  123| 			    sizeof(struct DYNTRANS_IC);			\
  124| 			printf("cur_ic_page=%p ic=%p (low_pc=0x%x)\n",	\
  125| 			    cpu->cd.DYNTRANS_ARCH.cur_ic_page,		\
  126| 			    ic, low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT); \
  127| 		} \
  128| 		ic->f(cpu, ic);
  129| 
  130| #endif
  131| 
  132| /*  static long long nr_of_I_calls = 0;  */
  133| 
  134| /*  Temporary hack for finding NULL bugs:  */
  135| /*  #define I	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; 			\
  136| 		nr_of_I_calls ++;					\
  137| 		if (ic->f == NULL) {					\
  138| 			int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - \
  139| 			    (size_t)cpu->cd.DYNTRANS_ARCH.cur_ic_page) / \
  140| 			    sizeof(struct DYNTRANS_IC);			\
  141| 			cpu->pc &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) << \
  142| 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);		\
  143| 			cpu->pc += (low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT);\
  144| 			printf("Crash at %016" PRIx64"\n", cpu->pc);	\
  145| 			printf("nr of I calls: %lli\n", nr_of_I_calls);	\
  146| 			printf("Next ic = %p\n", cpu->cd.		\
  147| 				DYNTRANS_ARCH.next_ic);			\
  148| 			printf("cur ic page = %p\n", cpu->cd.		\
  149| 				DYNTRANS_ARCH.cur_ic_page);		\
  150| 			cpu->running = 0;				\
  151| 			return 0;					\
  152| 		}							\
  153| 		ic->f(cpu, ic);  */
  154| 
  155| /*  Temporary hack for MIPS, to hunt for 32-bit/64-bit sign-extension bugs:  */
  156| /*  #define I		{ int k; for (k=1; k<=31; k++)	\
  157| 	cpu->cd.mips.gpr[k] = (int32_t)cpu->cd.mips.gpr[k];\
  158| 	if (cpu->cd.mips.gpr[0] != 0) {			\
  159| 		fatal("NOOOOOO\n"); exit(1);		\
  160| 	}						\
  161| 	ic = cpu->cd.DYNTRANS_ARCH.next_ic ++; ic->f(cpu, ic); }
  162| */
  163| #endif	/*  STATIC STUFF  */
  164| 
```

### `src/machines/machine.c` around the row's cited line 398 (HEAD 8d9df658, lines 278-518)

```c
  278| 	    realloc(machine->breakpoints.hitcount, n * sizeof(uint64_t)));
  279| 	CHECK_ALLOCATION(machine->breakpoints.ignore_left = (int64_t *)
  280| 	    realloc(machine->breakpoints.ignore_left, n * sizeof(int64_t)));
  281| 	CHECK_ALLOCATION(machine->breakpoints.string[machine->breakpoints.n] =
  282| 	    strdup(optarg));
  283| 
  284| 	machine->breakpoints.addr[machine->breakpoints.n] = 0;
  285| 	machine->breakpoints.hitcount[machine->breakpoints.n] = 0;
  286| 	machine->breakpoints.ignore_left[machine->breakpoints.n] = 0;
  287| 	machine->breakpoints.n ++;
  288| }
  289| 
  290| 
  291| /*
  292|  *  machine_watchpoint_match():
  293|  *
  294|  *  #250: return (index + 1) of the first data write-watchpoint whose physical
  295|  *  range [addr, addr+len) overlaps the accessed range, or 0 for no match.
  296|  *  Callers guard with watchpoints.n != 0, so this is never called on the hot
  297|  *  paths unless the user has actually set a watchpoint.
  298|  */
  299| int machine_watchpoint_match(struct machine *machine, uint64_t addr,
  300| 	uint64_t len)
  301| {
  302| 	int i;
  303| 
  304| 	for (i = 0; i < machine->watchpoints.n; i++) {
  305| 		uint64_t wa = machine->watchpoints.addr[i];
  306| 		uint64_t wl = machine->watchpoints.len[i];
  307| 
  308| 		if (addr < wa + wl && wa < addr + len)
  309| 			return i + 1;
  310| 	}
  311| 
  312| 	return 0;
  313| }
  314| 
  315| 
  316| /*
  317|  *  machine_add_tickfunction():
  318|  *
  319|  *  Adds a tick function (a function called every now and then, depending on
  320|  *  clock cycle count) to a machine.
  321|  *
  322|  *  If tickshift is non-zero, a tick will occur every (1 << tickshift) cycles.
  323|  *  This is used for the normal (fast dyntrans) emulation modes.
  324|  *
  325|  *  If tickshift is zero, then this is a cycle-accurate tick function.
  326|  *  The hz value is used in this case.
  327|  */
  328| void machine_add_tickfunction(struct machine *machine, void (*func)
  329| 	(struct cpu *, void *), void *extra, int tickshift)
  330| {
  331| 	int n = machine->tick_functions.n_entries;
  332| 
  333| 	CHECK_ALLOCATION(machine->tick_functions.ticks_till_next = (int *) realloc(
  334| 	    machine->tick_functions.ticks_till_next, (n+1) * sizeof(int)));
  335| 	CHECK_ALLOCATION(machine->tick_functions.ticks_reset_value = (int *) realloc(
  336| 	    machine->tick_functions.ticks_reset_value, (n+1) * sizeof(int)));
  337| 	CHECK_ALLOCATION(machine->tick_functions.f = (void (**)(struct cpu*,void*)) realloc(
  338| 	    machine->tick_functions.f, (n+1) * sizeof(void *)));
  339| 	CHECK_ALLOCATION(machine->tick_functions.extra = (void **) realloc(
  340| 	    machine->tick_functions.extra, (n+1) * sizeof(void *)));
  341| 
  342| 	/*
  343| 	 *  The dyntrans subsystem wants to run code in relatively
  344| 	 *  large chunks without checking for external interrupts;
  345| 	 *  too low tickshifts are not allowed.
  346| 	 */
  347| 	if (tickshift < N_SAFE_DYNTRANS_LIMIT_SHIFT) {
  348| 		fatal("ERROR! tickshift = %i, less than "
  349| 		    "N_SAFE_DYNTRANS_LIMIT_SHIFT (%i)\n",
  350| 		    tickshift, N_SAFE_DYNTRANS_LIMIT_SHIFT);
  351| 		exit(1);
  352| 	}
  353| 
  354| 	machine->tick_functions.ticks_till_next[n]   = 0;
  355| 	machine->tick_functions.ticks_reset_value[n] = 1 << tickshift;
  356| 	machine->tick_functions.f[n]                 = func;
  357| 	machine->tick_functions.extra[n]             = extra;
  358| 
  359| 	machine->tick_functions.n_entries = n + 1;
  360| }
  361| 
  362| 
  363| /*
  364|  *  machine_statistics_init():
  365|  *
  366|  *  Initialize the parts of a machine struct that deal with instruction
  367|  *  statistics gathering.
  368|  *
  369|  *  Note: The fname argument contains "flags:filename".
  370|  */
  371| void machine_statistics_init(struct machine *machine, char *fname)
  372| {
  373| 	int n_fields = 0;
  374| 	char *pcolon = fname;
  375| 	const char *mode = "a";	/*  Append by default  */
  376| 
  377| 	machine->allow_instruction_combinations = 0;
  378| 
  379| 	if (machine->statistics.fields != NULL) {
  380| 		fprintf(stderr, "Only one -s option is allowed.\n");
  381| 		exit(1);
  382| 	}
  383| 
  384| 	machine->statistics.enabled = 1;
  385| 	CHECK_ALLOCATION(machine->statistics.fields = (char *) malloc(1));
  386| 	machine->statistics.fields[0] = '\0';
  387| 
  388| 	while (*pcolon && *pcolon != ':')
  389| 		pcolon ++;
  390| 
  391| 	if (*pcolon != ':') {
  392| 		fprintf(stderr, "The syntax for the -s option is:    "
  393| 		    "-s flags:filename\nYou omitted the flags. Run g"
  394| 		    "xemul -h for a list of available flags.\n");
  395| 		exit(1);
  396| 	}
  397| 
  398| 	while (*fname != ':') {
  399| 		switch (*fname) {
  400| 
  401| 		/*  Type flags:  */
  402| 		case 'v':
  403| 		case 'i':
  404| 		case 'p':
  405| 			CHECK_ALLOCATION(machine->statistics.fields = (char *) realloc(
  406| 			    machine->statistics.fields, strlen(
  407| 			    machine->statistics.fields) + 2));
  408| 			machine->statistics.fields[n_fields ++] = *fname;
  409| 			machine->statistics.fields[n_fields] = '\0';
  410| 			break;
  411| 
  412| 		/*  Optional flags:  */
  413| 		case 'o':
  414| 			mode = "w";
  415| 			break;
  416| 		case 'd':
  417| 			machine->statistics.enabled = 0;
  418| 			break;
  419| 
  420| 		default:fprintf(stderr, "Unknown flag '%c' used with the"
  421| 			    " -s option. Aborting.\n", *fname);
  422| 			exit(1);
  423| 		}
  424| 		fname ++;
  425| 	}
  426| 
  427| 	fname ++;	/*  point to the filename after the colon  */
  428| 
  429| 	CHECK_ALLOCATION(machine->statistics.filename = strdup(fname));
  430| 	machine->statistics.file = fopen(machine->statistics.filename, mode);
  431| }
  432| 
  433| 
  434| /*
  435|  *  machine_dumpinfo():
  436|  *
  437|  *  Dumps info about a machine in some kind of readable format. (Used by
  438|  *  the 'machine' debugger command.)
  439|  */
  440| void machine_dumpinfo(struct machine *m)
  441| {
  442| 	int i;
  443| 
  444| 	debug("serial nr: %i", m->serial_nr);
  445| 	if (m->nr_of_nics > 0)
  446| 		debug("  (nr of NICs: %i)", m->nr_of_nics);
  447| 	debug("\n");
  448| 
  449| 	char meminfo[2000];
  450| 	snprintf(meminfo, sizeof(meminfo), "%i MB", m->physical_ram_in_mb);
  451| 
  452| 	if (m->memory_offset_in_mb != 0)
  453| 		snprintf(meminfo + strlen(meminfo), sizeof(meminfo) - strlen(meminfo),
  454| 		    " (offset by %i MB)", m->memory_offset_in_mb);
  455| 	if (m->random_mem_contents)
  456| 		snprintf(meminfo + strlen(meminfo), sizeof(meminfo) - strlen(meminfo),
  457| 		    ", randomized content");
  458| 
  459| 	debugmsg(SUBSYS_MACHINE, "memory", VERBOSITY_INFO, "%s", meminfo);
  460| 
  461| 	if (!m->prom_emulation)
  462| 		debug("PROM emulation disabled\n");
  463| 
  464| 	for (i=0; i<m->ncpus; i++)
  465| 		cpu_dumpinfo(m, m->cpus[i], true);
  466| 
  467| 	if (m->ncpus > 1)
  468| 		debug("Bootstrap cpu is nr %i\n", m->bootstrap_cpu);
  469| 
  470| 	if (m->x11_md.in_use) {
  471| 		debug("Using X11");
  472| 		if (m->x11_md.scaledown > 1)
  473| 			debug(", scaledown %i", m->x11_md.scaledown);
  474| 		if (m->x11_md.scaleup > 1)
  475| 			debug(", scaleup %i", m->x11_md.scaleup);
  476| 		if (m->x11_md.n_display_names > 0) {
  477| 			for (i=0; i<m->x11_md.n_display_names; i++) {
  478| 				debug(i? ", " : " (");
  479| 				debug("\"%s\"", m->x11_md.display_names[i]);
  480| 			}
  481| 			debug(")");
  482| 		}
  483| 		debug("\n");
  484| 	}
  485| 
  486| 	diskimage_dump_info(m);
  487| 
  488| 	if (m->force_netboot)
  489| 		debug("Forced netboot\n");
  490| }
  491| 
  492| 
  493| /*
  494|  *  machine_setup():
  495|  *
  496|  *  This function initializes memory, registers, and/or devices
  497|  *  required by specific machine emulations.
  498|  */
  499| void machine_setup(struct machine *machine)
  500| {
  501| 	struct machine_entry *me;
  502| 	struct cpu *cpu = machine->cpus[machine->bootstrap_cpu];
  503| 
  504| 	machine->bootdev_id = diskimage_bootdev(machine, &machine->bootdev_type);
  505| 	machine->machine_name = NULL;
  506| 
  507| 	/*  TODO: Move this somewhere else?  */
  508| 	if (machine->boot_string_argument == NULL) {
  509| 		switch (machine->machine_type) {
  510| 		case MACHINE_ARC:
  511| 			machine->boot_string_argument = strdup("-aN");
  512| 			break;
  513| 		case MACHINE_CATS:
  514| 			machine->boot_string_argument = strdup("-A");
  515| 			break;
  516| 		case MACHINE_PMAX:
  517| 			machine->boot_string_argument = strdup("-a");
  518| 			break;
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

End with one line: `FIXDRAFT_DYNTRANSSTATSBUF: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL  edit 3 src/cpus/cpu_dyntrans.c: old occurs 0 times
```

The previous edits:

```json
[
  {
    "file": "src/cpus/cpu_dyntrans.c",
    "old": "\t\tcase 'i':\n\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t    \"%p\", (void *)ic->f);\n\t\t\tbreak;",
    "new": "\t\tcase 'i':\n\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t    \"%p\", (void *)ic->f);\n\t\t\tbreak;",
    "why": "Buffer limit must be remaining size."
  },
  {
    "file": "src/cpus/cpu_dyntrans.c",
    "old": "\t\tcase 'p':\n\t\t\t/*  Physical program counter address:  */\n\t\t\tcpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)\n\t\t\t    cpu->cd.DYNTRANS_ARCH.cur_ic_page;\n\t\t\ta = cpu->cd.DYNTRANS_ARCH.cur_physpage->physaddr;\n\t\t\ta &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<\n\t\t\t    DYNTRANS_INSTR_ALIGNMENT_SHIFT);\n\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "new": "\t\tcase 'p':\n\t\t\t/*  Physical program counter address:  */\n\t\t\tcpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)\n\t\t\t    cpu->cd.DYNTRANS_ARCH.cur_ic_page;\n\t\t\ta = cpu->cd.DYNTRANS_ARCH.cur_physpage->physaddr;\n\t\t\ta &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<\n\t\t\t    DYNTRANS_INSTR_ALIGNMENT_SHIFT);\n\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "why": "Buffer limit must be remaining size. Expanding the block guarantees a unique old string match for case p."
  },
  {
    "file": "src/cpus/cpu_dyntrans.c",
    "old": "\t\tcase 'v':\n\t\t\t/*  Virtual program counter address:  */\n\t\t\ta = cpu->pc;\n\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "new": "\t\tcase 'v':\n\t\t\t/*  Virtual program counter address:  */\n\t\t\ta = cpu->pc;\n\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "why": "Buffer limit must be remaining size. Expanding the block guarantees a unique old string match for case v."
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
