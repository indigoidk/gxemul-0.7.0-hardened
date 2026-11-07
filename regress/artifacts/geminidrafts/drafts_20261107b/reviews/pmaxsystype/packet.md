# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pmaxsystype` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pmaxsystype`, state `open`)

**title:** machines/machine_pmax.c environment + promemul/dec_prom.c:dec_jumptable_func -- no `systype` variable (Ultrix 3.1D panics) and the old jump table's close() at 0x50 returns -1 -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T74 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-65).  Source URLs: https://github.com/rpajarola/gxemul/commit/12306ee4747fd15a0c67cb2ecc3318ff2f7256d4.  Our site at de8c7547: src/machines/machine_pmax.c:935-940; src/promemul/dec_prom.c:186-195.  Portable fix: yes -- port rpajarola 12306ee.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `src/promemul/dec_prom.c` line 184 (default case handles 0x50 and returns -1) and `src/machines/machine_pmax.c` lines 893-950 (no `systype` environment variable is added).

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/promemul/dec_prom.c b/src/promemul/dec_prom.c
index e4a2a2bf..96d63ba1 100644
--- a/src/promemul/dec_prom.c
+++ b/src/promemul/dec_prom.c
@@ -164,6 +164,9 @@ int dec_jumptable_func(struct cpu *cpu, int vector)
 			free(tmp_buf);
 		}
 		break;
+	case 0x50:	/*  close()  */
+		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
+		break;
 	case 0x58:	/*  lseek(handle, offset[, whence])  */
 		/*  TODO  */
 		if (cpu->cd.mips.gpr[MIPS_GPR_A2] == 0)
```

## Every edited function, after the fix

### `src/promemul/dec_prom.c` -- post-edit lines 96-200 (`+` marks a line the diff added or the point of a deletion)

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
  167|+ 	case 0x50:	/*  close()  */
  168|+ 		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  169|+ 		break;
  170|  	case 0x58:	/*  lseek(handle, offset[, whence])  */
  171|  		/*  TODO  */
  172|  		if (cpu->cd.mips.gpr[MIPS_GPR_A2] == 0)
  173|  			current_file_offset = cpu->cd.mips.gpr[MIPS_GPR_A1];
  174|  		else
  175|  			fatal("WARNING! Unimplemented whence in "
  176|  			    "dec_jumptable_func()\n");
  177|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = 0;
  178|  		break;
  179|  	case 0x68:	/*  putchar()  */
  180|  		console_putchar(cpu->machine->main_console_handle,
  181|  		    cpu->cd.mips.gpr[MIPS_GPR_A0]);
  182|  		break;
  183|  	case 0x88:	/*  printf()  */
  184|  		return 0x30;
  185|  	case 0x108:	/*  getenv2()  */
  186|  		return 0x64;
  187|  	default:
  188|  		/*  #245: emit one verbosity-gated line instead of an
  189|  		    unconditional register dump + a0 string scan, so a guest
  190|  		    spamming bad jump-table vectors can't flood the host log
  191|  		    (raise promemul verbosity / `break promemul` for full state). */
  192|  		debugmsg_cpu(cpu, SUBSYS_PROMEMUL, "dec", VERBOSITY_DEBUG,
  193|  		    "unimplemented JUMP TABLE vector 0x%x (decimal function %i)",
  194|  		    vector, vector/8);
  195|  		/*  #241: return an error to the guest instead of halting.  */
  196|  		cpu->cd.mips.gpr[MIPS_GPR_V0] = (int32_t) -1;
  197|  	}
  198|  
  199|  	return 0;
  200|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PMAXSYSTYPE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PMAXSYSTYPE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
