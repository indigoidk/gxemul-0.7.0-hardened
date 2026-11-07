# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `pmaxsystype` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `pmaxsystype`, state `open`)

**title:** machines/machine_pmax.c environment + promemul/dec_prom.c:dec_jumptable_func -- no `systype` variable (Ultrix 3.1D panics) and the old jump table's close() at 0x50 returns -1 -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T74 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-65).  Source URLs: https://github.com/rpajarola/gxemul/commit/12306ee4747fd15a0c67cb2ecc3318ff2f7256d4.  Our site at de8c7547: src/machines/machine_pmax.c:935-940; src/promemul/dec_prom.c:186-195.  Portable fix: yes -- port rpajarola 12306ee.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/promemul/dec_prom.c` -- AT HEAD, lines 96-197 (`*` marks a line your previous draft changed)

```c
   96|  int dec_jumptable_func(struct cpu *cpu, int vector)
   97|  {
   98|  	static int file_opened = 0;
   99|  	static int current_file_offset = 0;
  100|  
  101|  	switch (vector) {
  102|  	case 0x0:	/*  reset()  */
  103|  		/*  TODO  */
  104|  		cpu->running = 0;
  105|  		break;
  106|  	case 0x10:	/*  restart()  */
  107|  		/*  TODO  */
  108|  		cpu->running = 0;
  109|  		break;
  110|  	case 0x18:	/*  reinit()  */
  111|  		/*  TODO  */
  112|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  113|  		break;
  114|  	case 0x30:	/*  open()  */
  115|  		/*
  116|  		 *  TODO: This is just a hack to allow Sprite/pmax' bootblock
  117|  		 *  code to load /vmsprite. The filename argument (in A0)
  118|  		 *  is ignored, and a file handle value of 1 is returned.
  119|  		 */
  120|  		if (file_opened) {
  121|  			/*  #241: Opening a second file is unsupported, but
  122|  			    return an error to the guest (V0 = -1) instead of
  123|  			    halting the host emulator.  */
  124|  			debugmsg_cpu(cpu, SUBSYS_PROMEMUL, "dec",
  125|  			    VERBOSITY_DEBUG,		/*  #245: gate  */
  126|  			    "open() of a second file is not supported");
  127|  			cpu->cd.mips.gpr[MIPS_GPR_V0] = (int32_t) -1;
  128|  			break;
  129|  		}
  130|  		file_opened = 1;
  131|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = 1;
  132|  		break;
  133|  	case 0x38:	/*  read(handle, ptr, length)  */
  134|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = (uint64_t) -1;
  135|  		/*  #191: (Codex/Fable) A2 is a guest-supplied length; cap it so a
  136|  		    huge value can't drive malloc()->CHECK_ALLOCATION->exit() (a
  137|  		    guest-reachable host DoS/OOM). 64 MB is far above any real
  138|  		    PROM disk read.  */
  139|  		if ((int32_t)cpu->cd.mips.gpr[MIPS_GPR_A2] > 0 &&
  140|  		    cpu->cd.mips.gpr[MIPS_GPR_A2] <= 64*1024*1024) {
  141|  			int disk_id = diskimage_bootdev(cpu->machine, NULL);
  142|  			int res;
  143|  			unsigned char *tmp_buf;
  144|  
  145|  			CHECK_ALLOCATION(tmp_buf = (unsigned char *)
  146|  			    malloc(cpu->cd.mips.gpr[MIPS_GPR_A2]));
  147|  
  148|  			res = diskimage_access(cpu->machine, disk_id,
  149|  			    DISKIMAGE_SCSI, 0, current_file_offset, tmp_buf,
  150|  			    cpu->cd.mips.gpr[MIPS_GPR_A2]);
  151|  
  152|  			/*  If the transfer was successful, transfer the data
  153|  			    to emulated memory:  */
  154|  			if (res) {
  155|  				uint64_t dst = cpu->cd.mips.gpr[MIPS_GPR_A1];
  156|  				store_buf(cpu, dst, (char *)tmp_buf,
  157|  				    cpu->cd.mips.gpr[MIPS_GPR_A2]);
  158|  				cpu->cd.mips.gpr[MIPS_GPR_V0] =
  159|  				    cpu->cd.mips.gpr[MIPS_GPR_A2];
  160|  				current_file_offset +=
  161|  				    cpu->cd.mips.gpr[MIPS_GPR_A2];
  162|  			}
  163|  
  164|  			free(tmp_buf);
  165|  		}
  166|  		break;
  167|* 	case 0x58:	/*  lseek(handle, offset[, whence])  */
  168|  		/*  TODO  */
  169|  		if (cpu->cd.mips.gpr[MIPS_GPR_A2] == 0)
  170|  			current_file_offset = cpu->cd.mips.gpr[MIPS_GPR_A1];
  171|  		else
  172|  			fatal("WARNING! Unimplemented whence in "
  173|  			    "dec_jumptable_func()\n");
  174|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  175|  		break;
  176|  	case 0x68:	/*  putchar()  */
  177|  		console_putchar(cpu->machine->main_console_handle,
  178|  		    cpu->cd.mips.gpr[MIPS_GPR_A0]);
  179|  		break;
  180|  	case 0x88:	/*  printf()  */
  181|  		return 0x30;
  182|  	case 0x108:	/*  getenv2()  */
  183|  		return 0x64;
  184|  	default:
  185|  		/*  #245: emit one verbosity-gated line instead of an
  186|  		    unconditional register dump + a0 string scan, so a guest
  187|  		    spamming bad jump-table vectors can't flood the host log
  188|  		    (raise promemul verbosity / `break promemul` for full state). */
  189|  		debugmsg_cpu(cpu, SUBSYS_PROMEMUL, "dec", VERBOSITY_DEBUG,
  190|  		    "unimplemented JUMP TABLE vector 0x%x (decimal function %i)",
  191|  		    vector, vector/8);
  192|  		/*  #241: return an error to the guest instead of halting.  */
  193|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = (int32_t) -1;
  194|  	}
  195|  
  196|  	return 0;
  197|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/promemul/dec_prom.c",
    "old": "\tcase 0x58:\t/*  lseek(handle, offset[, whence])  */",
    "new": "\tcase 0x50:\t/*  close()  */\n\t\tcpu->cd.mips.gpr[MIPS_GPR_V0] = 0;\n\t\tbreak;\n\tcase 0x58:\t/*  lseek(handle, offset[, whence])  */",
    "why": "Return success (0) instead of -1 for the old jump table's close() at 0x50 to prevent WRONG-RESULT errors."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PMAXSYSTYPE: DEFECT, 1 FINDINGS
1. No, the diff does not remove the defect at every site. It fixes `close()` at `0x50` in `src/promemul/dec_prom.c`, but misses the missing `systype` environment variable in `src/machines/machine_pmax.c` (referenced in the issue's drafter notes at lines 893-950).
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips any common tail code. The new `break` at `AFTER:169` merely exits the `switch` statement and proceeds to the common `return 0;` at `AFTER:199`, which perfectly matches the control flow of the previous `default` case.
3. RETURN VALUE: The function `dec_jumptable_func` still returns `0` at `AFTER:199`. However, the guest register `MIPS_GPR_V0` is now set to `0` at `AFTER:168` (previously it fell through to `default` and was set to `-1` at `AFTER:196`). This implies that the emulated `close()` call now reports success (0) instead of failure/error (-1) to the guest operating system.
4. ELSE: The diff changes nothing else. It strictly modifies the behavior of vector `0x50` and does not add any new side effects, messages, or uninitialized state.
5. House idioms: The diff introduces no new comments (except a standard case label comment), prints no new diagnostic messages, and stays within column limits, so no house idioms are violated.
`src/machines/machine_pmax.c:893`, severity DEFECT, Add the missing `systype` variable to the environment block for Ultrix 3.1D.
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

End with two lines: `REVISION_PMAXSYSTYPE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PMAXSYSTYPE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
