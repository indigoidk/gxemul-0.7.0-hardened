# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `dyntransstatsbuf` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `dyntransstatsbuf`, state `open`)

**title:** src/cpus/cpu_dyntrans.c:44,63-98 -- gather_statistics() appends with snprintf(buf + strlen(buf), sizeof(buf), ...), so the size passed never shrinks and a long -s field list writes past the 60-byte stack buffer -- OOB-WRITE (host -s option only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_dyntrans.c:69

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_dyntrans.c b/src/cpus/cpu_dyntrans.c
index 05a941db..62092254 100644
--- a/src/cpus/cpu_dyntrans.c
+++ b/src/cpus/cpu_dyntrans.c
@@ -66,7 +66,7 @@ static void gather_statistics(struct cpu *cpu)
 
 		switch (ch) {
 		case 'i':
-			snprintf(buf + strlen(buf), sizeof(buf),
+			snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
 			    "%p", (void *)ic->f);
 			break;
 		case 'p':
@@ -78,10 +78,10 @@ static void gather_statistics(struct cpu *cpu)
 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
 			if (cpu->is_32bit)
-				snprintf(buf + strlen(buf), sizeof(buf),
+				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
 				    "0x%08" PRIx32, (uint32_t)a);
 			else
-				snprintf(buf + strlen(buf), sizeof(buf),
+				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
 				    "0x%016" PRIx64, (uint64_t)a);
 			break;
 		case 'v':
@@ -91,10 +91,10 @@ static void gather_statistics(struct cpu *cpu)
 			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
 			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
 			if (cpu->is_32bit)
-				snprintf(buf + strlen(buf), sizeof(buf),
+				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
 				    "0x%08" PRIx32, (uint32_t)a);
 			else
-				snprintf(buf + strlen(buf), sizeof(buf),
+				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
 				    "0x%016" PRIx64, (uint64_t)a);
 			break;
 		}
```

## Every edited function, after the fix

### `src/cpus/cpu_dyntrans.c` -- post-edit lines 42-105 (`+` marks a line the diff added or the point of a deletion)

```c
   42|  static void gather_statistics(struct cpu *cpu)
   43|  {
   44|  	char ch, buf[60];
   45|  	struct DYNTRANS_IC *ic = cpu->cd.DYNTRANS_ARCH.next_ic;
   46|  	int i = 0;
   47|  	uint64_t a;
   48|  	int low_pc = ((size_t)cpu->cd.DYNTRANS_ARCH.next_ic - (size_t)
   49|  	    cpu->cd.DYNTRANS_ARCH.cur_ic_page) / sizeof(struct DYNTRANS_IC);
   50|  
   51|  	if (cpu->machine->statistics.file == NULL) {
   52|  		fatal("statistics gathering with no filename set is"
   53|  		    " meaningless\n");
   54|  		return;
   55|  	}
   56|  
   57|  	/*  low_pc must be within the page!  */
   58|  	if (low_pc < 0 || low_pc > DYNTRANS_IC_ENTRIES_PER_PAGE)
   59|  		return;
   60|  
   61|  	buf[0] = '\0';
   62|  
   63|  	while ((ch = cpu->machine->statistics.fields[i]) != '\0') {
   64|  		if (i != 0)
   65|  			strlcat(buf, " ", sizeof(buf));
   66|  
   67|  		switch (ch) {
   68|  		case 'i':
   69|+ 			snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
   70|  			    "%p", (void *)ic->f);
   71|  			break;
   72|  		case 'p':
   73|  			/*  Physical program counter address:  */
   74|  			cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
   75|  			    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
   76|  			a = cpu->cd.DYNTRANS_ARCH.cur_physpage->physaddr;
   77|  			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   78|  			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   79|  			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   80|  			if (cpu->is_32bit)
   81|+ 				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
   82|  				    "0x%08" PRIx32, (uint32_t)a);
   83|  			else
   84|+ 				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
   85|  				    "0x%016" PRIx64, (uint64_t)a);
   86|  			break;
   87|  		case 'v':
   88|  			/*  Virtual program counter address:  */
   89|  			a = cpu->pc;
   90|  			a &= ~((DYNTRANS_IC_ENTRIES_PER_PAGE-1) <<
   91|  			    DYNTRANS_INSTR_ALIGNMENT_SHIFT);
   92|  			a += low_pc << DYNTRANS_INSTR_ALIGNMENT_SHIFT;
   93|  			if (cpu->is_32bit)
   94|+ 				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
   95|  				    "0x%08" PRIx32, (uint32_t)a);
   96|  			else
   97|+ 				snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf),
   98|  				    "0x%016" PRIx64, (uint64_t)a);
   99|  			break;
  100|  		}
  101|  		i++;
  102|  	}
  103|  
  104|  	fprintf(cpu->machine->statistics.file, "%s\n", buf);
  105|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_DYNTRANSSTATSBUF: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_DYNTRANSSTATSBUF: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
