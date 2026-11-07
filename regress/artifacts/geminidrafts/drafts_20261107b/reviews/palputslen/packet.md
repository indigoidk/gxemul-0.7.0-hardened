# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `palputslen` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `palputslen`, state `open`)

**title:** src/cpus/cpu_alpha_palcode.c:110-119 -- PROM_R_PUTS loops addr < a2 + a3 over guest-supplied a2 and a3 with no length cap, so a huge a3 runs that many single-byte reads and console writes, and a wrapped sum prints nothing while still returning a3 -- WRONG-RESULT (guest firmware call)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `for (addr = a2; addr < a2 + a3; addr ++)` and `cpu->cd.alpha.r[ALPHA_V0] = a3;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_alpha_palcode.c b/src/cpus/cpu_alpha_palcode.c
index 39ae212f..9cbf195f 100644
--- a/src/cpus/cpu_alpha_palcode.c
+++ b/src/cpus/cpu_alpha_palcode.c
@@ -109,13 +109,18 @@ void alpha_prom_call(struct cpu *cpu)
 
 	case PROM_R_PUTS:
 		/*  a1 = channel, a2 = ptr to buf, a3 = len  */
-		for (addr = a2; addr < a2 + a3; addr ++) {
+		len = a3;
+		if (len > 65536)
+			len = 65536; /* #palputslen: length cap */
+		if (a2 + len < a2)
+			len = -a2;
+		cpu->cd.alpha.r[ALPHA_V0] = len;
+		for (addr = a2; len > 0; len--, addr++) {
 			unsigned char ch;
 			cpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),
 			    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
 			console_putchar(cpu->machine->main_console_handle, ch);
 		}
-		cpu->cd.alpha.r[ALPHA_V0] = a3;
 		break;
 
 	case PROM_R_GETENV:
```

## Every edited function, after the fix

### `src/cpus/cpu_alpha_palcode.c` -- post-edit lines 101-159 (`+` marks a line the diff added or the point of a deletion)

```c
  101|  void alpha_prom_call(struct cpu *cpu)
  102|  {
  103|  	uint64_t addr, a1 = cpu->cd.alpha.r[ALPHA_A1];
  104|  	uint64_t a2 = cpu->cd.alpha.r[ALPHA_A2], a3 = cpu->cd.alpha.r[ALPHA_A3];
  105|  	uint64_t len;
  106|  	const char *s = "";
  107|  
  108|  	switch (cpu->cd.alpha.r[ALPHA_A0]) {
  109|  
  110|  	case PROM_R_PUTS:
  111|  		/*  a1 = channel, a2 = ptr to buf, a3 = len  */
  112|+ 		len = a3;
  113|+ 		if (len > 65536)
  114|+ 			len = 65536; /* #palputslen: length cap */
  115|+ 		if (a2 + len < a2)
  116|+ 			len = -a2;
  117|+ 		cpu->cd.alpha.r[ALPHA_V0] = len;
  118|+ 		for (addr = a2; len > 0; len--, addr++) {
  119|  			unsigned char ch;
  120|  			cpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),
  121|  			    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
  122|  			console_putchar(cpu->machine->main_console_handle, ch);
  123|  		}
  124|+ 		break;
  125|  
  126|  	case PROM_R_GETENV:
  127|  		/*  a1 = variable id, a2 = char *buf, a3 = bufsize  */
  128|  		switch (a1) {
  129|  		case PROM_E_BOOTED_DEV:
  130|  			s = "";		/*  TODO  */
  131|  			break;
  132|  		case PROM_E_BOOTED_FILE:
  133|  			s = cpu->machine->boot_kernel_filename;
  134|  			break;
  135|  		case PROM_E_BOOTED_OSFLAGS:
  136|  			s = cpu->machine->boot_string_argument;
  137|  			break;
  138|  		case PROM_E_TTY_DEV:
  139|  			s = "";		/*  TODO  */
  140|  			break;
  141|  		default:fatal("[ Alpha PALcode: GXemul PROM getenv %" PRIi64 ": TODO "
  142|  			    "]\n", (int64_t)cpu->cd.alpha.r[ALPHA_A1]);
  143|  			cpu->running = 0;
  144|  		}
  145|  		/*  Copy at most a3 bytes.  */
  146|  		len = a3;
  147|  		if (strlen(s) < len)
  148|  			len = strlen(s) + 1;
  149|  		store_buf(cpu, a2, s, len);
  150|  		break;
  151|  
  152|  	default:fatal("[ Alpha PALcode: GXemul PROM call, a0=0x%" PRIx64" ]\n",
  153|  		    (uint64_t) cpu->cd.alpha.r[ALPHA_A0]);
  154|  		cpu->running = 0;
  155|  	}
  156|  
  157|  	/*  Return from the PROM call.  */
  158|  	cpu->pc = cpu->cd.alpha.r[ALPHA_RA];
  159|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PALPUTSLEN: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PALPUTSLEN: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
