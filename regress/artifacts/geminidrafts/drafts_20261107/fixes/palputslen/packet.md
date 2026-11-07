# GXemul hardened fork -- DRAFT A FIX for one filed issue, `palputslen` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `palputslen`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_alpha_palcode.c:110-119 -- PROM_R_PUTS loops addr < a2 + a3 over guest-supplied a2 and a3 with no length cap, so a huge a3 runs that many single-byte reads and console writes, and a wrapped sum prints nothing while still returning a3 -- WRONG-RESULT (guest firmware call)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Unbounded iteration allowing trivial infinite looping or wrapping defects.

## The code at the cited lines

### `src/cpus/cpu_alpha_palcode.c` around the row's cited line 110 (HEAD d2a6f233, lines 65-155)

```c
   65| 	case 0x11: snprintf(buf, buflen, "PAL_OSF1_wrmces"); break;
   66| 	case 0x2b: snprintf(buf, buflen, "PAL_OSF1_wrfen"); break;
   67| 	case 0x2d: snprintf(buf, buflen, "PAL_OSF1_wrvptptr"); break;
   68| 	case 0x30: snprintf(buf, buflen, "PAL_OSF1_swpctx"); break;
   69| 	case 0x31: snprintf(buf, buflen, "PAL_OSF1_wrval"); break;
   70| 	case 0x32: snprintf(buf, buflen, "PAL_OSF1_rdval"); break;
   71| 	case 0x33: snprintf(buf, buflen, "PAL_OSF1_tbi"); break;
   72| 	case 0x34: snprintf(buf, buflen, "PAL_OSF1_wrent"); break;
   73| 	case 0x35: snprintf(buf, buflen, "PAL_OSF1_swpipl"); break;
   74| 	case 0x36: snprintf(buf, buflen, "PAL_rdps"); break;
   75| 	case 0x37: snprintf(buf, buflen, "PAL_OSF1_wrkgp"); break;
   76| 	case 0x38: snprintf(buf, buflen, "PAL_OSF1_wrusp"); break;
   77| 	case 0x39: snprintf(buf, buflen, "PAL_OSF1_wrperfmon"); break;
   78| 	case 0x3a: snprintf(buf, buflen, "PAL_OSF1_rdusp"); break;
   79| 	case 0x3c: snprintf(buf, buflen, "PAL_whami"); break;
   80| 	case 0x3d: snprintf(buf, buflen, "PAL_OSF1_retsys"); break;
   81| 	case 0x3e: snprintf(buf, buflen, "PAL_wtint"); break;
   82| 	case 0x3f: snprintf(buf, buflen, "PAL_OSF1_rti"); break;
   83| 	case 0x80: snprintf(buf, buflen, "PAL_bpt"); break;
   84| 	case 0x81: snprintf(buf, buflen, "PAL_bugchk"); break;
   85| 	case 0x83: snprintf(buf, buflen, "PAL_OSF1_callsys"); break;
   86| 	case 0x86: snprintf(buf, buflen, "PAL_imb"); break;
   87| 	case 0x92: snprintf(buf, buflen, "PAL_OSF1_urti"); break;
   88| 	case 0x9e: snprintf(buf, buflen, "PAL_rdunique"); break;
   89| 	case 0x9f: snprintf(buf, buflen, "PAL_wrunique"); break;
   90| 	case 0xaa: snprintf(buf, buflen, "PAL_gentrap"); break;
   91| 	case 0xae: snprintf(buf, buflen, "PAL_clrfen"); break;
   92| 	case 0x3fffffe: snprintf(buf, buflen, "GXemul_PROM"); break;
   93| 	default:snprintf(buf, buflen, "UNKNOWN 0x%" PRIx32, palcode);
   94| 	}
   95| }
   96| 
   97| 
   98| /*
   99|  *  alpha_prom_call():
  100|  */
  101| void alpha_prom_call(struct cpu *cpu)
  102| {
  103| 	uint64_t addr, a1 = cpu->cd.alpha.r[ALPHA_A1];
  104| 	uint64_t a2 = cpu->cd.alpha.r[ALPHA_A2], a3 = cpu->cd.alpha.r[ALPHA_A3];
  105| 	uint64_t len;
  106| 	const char *s = "";
  107| 
  108| 	switch (cpu->cd.alpha.r[ALPHA_A0]) {
  109| 
  110| 	case PROM_R_PUTS:
  111| 		/*  a1 = channel, a2 = ptr to buf, a3 = len  */
  112| 		for (addr = a2; addr < a2 + a3; addr ++) {
  113| 			unsigned char ch;
  114| 			cpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),
  115| 			    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
  116| 			console_putchar(cpu->machine->main_console_handle, ch);
  117| 		}
  118| 		cpu->cd.alpha.r[ALPHA_V0] = a3;
  119| 		break;
  120| 
  121| 	case PROM_R_GETENV:
  122| 		/*  a1 = variable id, a2 = char *buf, a3 = bufsize  */
  123| 		switch (a1) {
  124| 		case PROM_E_BOOTED_DEV:
  125| 			s = "";		/*  TODO  */
  126| 			break;
  127| 		case PROM_E_BOOTED_FILE:
  128| 			s = cpu->machine->boot_kernel_filename;
  129| 			break;
  130| 		case PROM_E_BOOTED_OSFLAGS:
  131| 			s = cpu->machine->boot_string_argument;
  132| 			break;
  133| 		case PROM_E_TTY_DEV:
  134| 			s = "";		/*  TODO  */
  135| 			break;
  136| 		default:fatal("[ Alpha PALcode: GXemul PROM getenv %" PRIi64 ": TODO "
  137| 			    "]\n", (int64_t)cpu->cd.alpha.r[ALPHA_A1]);
  138| 			cpu->running = 0;
  139| 		}
  140| 		/*  Copy at most a3 bytes.  */
  141| 		len = a3;
  142| 		if (strlen(s) < len)
  143| 			len = strlen(s) + 1;
  144| 		store_buf(cpu, a2, s, len);
  145| 		break;
  146| 
  147| 	default:fatal("[ Alpha PALcode: GXemul PROM call, a0=0x%" PRIx64" ]\n",
  148| 		    (uint64_t) cpu->cd.alpha.r[ALPHA_A0]);
  149| 		cpu->running = 0;
  150| 	}
  151| 
  152| 	/*  Return from the PROM call.  */
  153| 	cpu->pc = cpu->cd.alpha.r[ALPHA_RA];
  154| }
  155| 
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

End with one line: `FIXDRAFT_PALPUTSLEN: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
