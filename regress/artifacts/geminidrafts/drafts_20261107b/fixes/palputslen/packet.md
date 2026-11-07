# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `palputslen` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `palputslen`, state `open`)

**title:** src/cpus/cpu_alpha_palcode.c:110-119 -- PROM_R_PUTS loops addr < a2 + a3 over guest-supplied a2 and a3 with no length cap, so a huge a3 runs that many single-byte reads and console writes, and a wrapped sum prints nothing while still returning a3 -- WRONG-RESULT (guest firmware call)

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/cpus/cpu_alpha_palcode.c` -- AT HEAD, lines 101-154 (`*` marks a line your previous draft changed)

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
  112|* 		for (addr = a2; addr < a2 + a3; addr ++) {
  113|* 			unsigned char ch;
  114|  			cpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),
  115|  			    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
  116|  			console_putchar(cpu->machine->main_console_handle, ch);
  117|  		}
  118|  		cpu->cd.alpha.r[ALPHA_V0] = a3;
  119|  		break;
  120|  
  121|  	case PROM_R_GETENV:
  122|  		/*  a1 = variable id, a2 = char *buf, a3 = bufsize  */
  123|  		switch (a1) {
  124|  		case PROM_E_BOOTED_DEV:
  125|  			s = "";		/*  TODO  */
  126|  			break;
  127|  		case PROM_E_BOOTED_FILE:
  128|  			s = cpu->machine->boot_kernel_filename;
  129|  			break;
  130|  		case PROM_E_BOOTED_OSFLAGS:
  131|  			s = cpu->machine->boot_string_argument;
  132|  			break;
  133|  		case PROM_E_TTY_DEV:
  134|  			s = "";		/*  TODO  */
  135|  			break;
  136|  		default:fatal("[ Alpha PALcode: GXemul PROM getenv %" PRIi64 ": TODO "
  137|  			    "]\n", (int64_t)cpu->cd.alpha.r[ALPHA_A1]);
  138|  			cpu->running = 0;
  139|  		}
  140|  		/*  Copy at most a3 bytes.  */
  141|  		len = a3;
  142|  		if (strlen(s) < len)
  143|  			len = strlen(s) + 1;
  144|  		store_buf(cpu, a2, s, len);
  145|  		break;
  146|  
  147|  	default:fatal("[ Alpha PALcode: GXemul PROM call, a0=0x%" PRIx64" ]\n",
  148|  		    (uint64_t) cpu->cd.alpha.r[ALPHA_A0]);
  149|  		cpu->running = 0;
  150|  	}
  151|  
  152|  	/*  Return from the PROM call.  */
  153|  	cpu->pc = cpu->cd.alpha.r[ALPHA_RA];
  154|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/cpus/cpu_alpha_palcode.c",
    "old": "\tcase PROM_R_PUTS:\n\t\t/*  a1 = channel, a2 = ptr to buf, a3 = len  */\n\t\tfor (addr = a2; addr < a2 + a3; addr ++) {\n\t\t\tunsigned char ch;\n\t\t\tcpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),\n\t\t\t    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);\n\t\t\tconsole_putchar(cpu->machine->main_console_handle, ch);\n\t\t}\n\t\tcpu->cd.alpha.r[ALPHA_V0] = a3;\n\t\tbreak;",
    "new": "\tcase PROM_R_PUTS:\n\t\t/*  a1 = channel, a2 = ptr to buf, a3 = len  */\n\t\tlen = a3;\n\t\tif (len > 65536)\n\t\t\tlen = 65536; /* #palputslen: length cap */\n\t\tif (a2 + len < a2)\n\t\t\tlen = -a2;\n\t\tfor (addr = a2; addr < a2 + len; addr ++) {\n\t\t\tunsigned char ch;\n\t\t\tcpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),\n\t\t\t    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);\n\t\t\tconsole_putchar(cpu->machine->main_console_handle, ch);\n\t\t}\n\t\tcpu->cd.alpha.r[ALPHA_V0] = a3;\n\t\tbreak;",
    "why": "Caps iteration length to 65536 bytes per call and prevents overflow of a2 + len, preventing infinite console writes or premature exit on wrapping sum, while still returning the original requested length."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PALPUTSLEN: DEFECT, 2 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names?
No. The diff attempts to handle wrapped sums by setting `len = -a2`, but `a2 + len` then evaluates to `0`. The loop condition `addr < a2 + len` becomes `addr < 0`, which is always false for unsigned integers, so the loop still executes zero times and prints nothing. It also fails to fix the "WRONG-RESULT" because it still unconditionally returns `a3` on line 123, even when the output is capped or wrapped.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run?
No. The diff only introduces variable assignments and conditional checks; it adds no jumps or early exits.
3. RETURN VALUE: does any path now return something different?
No. The function still places the original uncapped `a3` value into `ALPHA_V0` on line 123.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one -- beyond removing the defect?
It limits the actual memory reads and `console_putchar` calls to 65536 per invocation, reducing potential I/O hangs, but silently truncates the output since the guest still receives the full original length as the return value.
5. House idioms (low severity):
The new comment `/* #palputslen: length cap */` adheres to the required `/* #NNN: ... */` tagging idiom, and all modified lines stay well within the 79-column limit.
`src/cpus/cpu_alpha_palcode.c:117`
Severity: DEFECT
Description: When `len = -a2`, `a2 + len` overflows to `0`, making `addr < 0` false, so it still prints nothing on wrap.
Smallest fix: `for (addr = a2; len > 0; len--, addr++) {`
`src/cpus/cpu_alpha_palcode.c:123`
Severity: DEFECT
Description: The function continues to return the original guest-supplied `a3` length even if the operation was capped or wrapped, perpetuating the WRONG-RESULT.
Smallest fix: `cpu->cd.alpha.r[ALPHA_V0] = original_len_to_return;` (requires saving the executed `len` before the loop).
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_PALPUTSLEN: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PALPUTSLEN: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
