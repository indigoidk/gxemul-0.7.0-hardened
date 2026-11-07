# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppctlbieseg` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppctlbieseg`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c:X(tlbie) -- invalidates only the exact EA, not the page index in every segment -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T41 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A4-21).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/59cc4103f41689f2d4b79626cfda6b9065e6595c, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/3dafe76542ea0ee67176456cfffbeeeaa98e983c.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:3930-3935.  Portable fix: yes -- port rs6000 59cc410 (branch-only working form; rs6000 3dafe76).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 59cc410 and 3dafe76

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 3930 (HEAD 2d25df65, lines 3885-3975)

```c
 3885| X(stvx)
 3886| {
 3887| 	uint8_t data[16];
 3888| 	MODE_uint_t addr = reg(ic->arg[1]) + reg(ic->arg[2]);
 3889| 	int rs = ic->arg[0];
 3890| 	uint64_t hi = cpu->cd.ppc.vr_hi[rs], lo = cpu->cd.ppc.vr_lo[rs];
 3891| 
 3892| 	data[0] = hi >> 56;
 3893| 	data[1] = hi >> 48;
 3894| 	data[2] = hi >> 40;
 3895| 	data[3] = hi >> 32;
 3896| 	data[4] = hi >> 24;
 3897| 	data[5] = hi >> 16;
 3898| 	data[6] = hi >> 8;
 3899| 	data[7] = hi;
 3900| 	data[8] = lo >> 56;
 3901| 	data[9] = lo >> 48;
 3902| 	data[10] = lo >> 40;
 3903| 	data[11] = lo >> 32;
 3904| 	data[12] = lo >> 24;
 3905| 	data[13] = lo >> 16;
 3906| 	data[14] = lo >> 8;
 3907| 	data[15] = lo;
 3908| 
 3909| 	cpu->memory_rw(cpu, cpu->mem, addr, data,
 3910| 	    sizeof(data), MEM_WRITE, CACHE_DATA);
 3911| }
 3912| 
 3913| 
 3914| /*
 3915|  *  vxor:  Vector (16-byte) XOR
 3916|  *
 3917|  *  arg[0] = v-register nr of source 1
 3918|  *  arg[1] = v-register nr of source 2
 3919|  *  arg[2] = v-register nr of destination
 3920|  */
 3921| X(vxor)
 3922| {
 3923| 	cpu->cd.ppc.vr_hi[ic->arg[2]] =
 3924| 	    cpu->cd.ppc.vr_hi[ic->arg[0]] ^ cpu->cd.ppc.vr_hi[ic->arg[1]];
 3925| 	cpu->cd.ppc.vr_lo[ic->arg[2]] =
 3926| 	    cpu->cd.ppc.vr_lo[ic->arg[0]] ^ cpu->cd.ppc.vr_lo[ic->arg[1]];
 3927| }
 3928| 
 3929| 
 3930| /*
 3931|  *  tlbia:  TLB invalidate all
 3932|  */
 3933| X(tlbia)
 3934| {
 3935| 	fatal("[ tlbia ]\n");
 3936| 	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
 3937| }
 3938| 
 3939| 
 3940| /*
 3941|  *  tlbie:  TLB invalidate
 3942|  */
 3943| X(tlbie)
 3944| {
 3945| 	/*  fatal("[ tlbie ]\n");  */
 3946| 	cpu->invalidate_translation_caches(cpu, reg(ic->arg[0]),
 3947| 	    INVALIDATE_VADDR);
 3948| }
 3949| 
 3950| 
 3951| /*
 3952|  *  sc: Syscall.
 3953|  */
 3954| X(sc)
 3955| {
 3956| 	/*  Synchronize the PC (pointing to _after_ this instruction)  */
 3957| 	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[1];
 3958| 
 3959| 	ppc_exception(cpu, PPC_EXCEPTION_SC);
 3960| 
 3961| 	/*  This caused an update to the PC register, so there is no need
 3962| 	    to worry about the next instruction being an end_of_page.  */
 3963| }
 3964| 
 3965| 
 3966| /*
 3967|  *  openfirmware:
 3968|  */
 3969| X(openfirmware)
 3970| {
 3971| 	of_emul(cpu);
 3972| 
 3973| 	cpu->pc = cpu->cd.ppc.spr[SPR_LR];
 3974| 	if (cpu->machine->show_trace_tree)
 3975| 		cpu_functioncall_trace_return(cpu);
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

End with one line: `FIXDRAFT_PPCTLBIESEG: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
