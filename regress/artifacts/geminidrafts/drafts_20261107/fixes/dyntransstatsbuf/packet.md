# GXemul hardened fork -- DRAFT A FIX for one filed issue, `dyntransstatsbuf` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 521d136a).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `dyntransstatsbuf`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_dyntrans.c:44,63-98 -- gather_statistics() appends with snprintf(buf + strlen(buf), sizeof(buf), ...), so the size passed never shrinks and a long -s field list writes past the 60-byte stack buffer -- OOB-WRITE (host -s option only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- snprintf size parameter must be the remaining buffer size, not the total size.

## The code at the cited lines

### `src/cpus/cpu_dyntrans.c` around the row's cited line 44 (HEAD 521d136a, lines 1-89)

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
```

### `src/machines/machine.c` around the row's cited line 398 (HEAD 521d136a, lines 353-443)

```c
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
APPLY FAILED: FAIL  edit 2 src/cpus/cpu_dyntrans.c: old occurs 2 times
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
    "old": "\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "new": "\t\t\ta += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;\n\t\t\tif (cpu->is_32bit)\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%08\" PRIx32, (uint32_t)a);\n\t\t\telse\n\t\t\t\tsnprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),\n\t\t\t\t    \"0x%016\" PRIx64, (uint64_t)a);\n\t\t\tbreak;",
    "why": "Buffer limit must be remaining size, ensuring a unique old block."
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
