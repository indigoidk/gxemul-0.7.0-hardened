# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppcbranch32width` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppcbranch32width`, state `open`, severity `MED`)

**title:** src/cpus/cpu_ppc_instr.c:349-359,516-518 -- the CTR branch condition uses all 64 bits in 32-bit mode and branch targets are sign-extended into the high half that 32-bit mode clears -- WRONG-RESULT (64-bit model at SF=0)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- mask bounds based on 32-bit mode

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 349 (HEAD 8d9df658, lines 229-469)

```c
  229| 
  230| /*
  231|  *  nop:  Do nothing.
  232|  */
  233| X(nop)
  234| {
  235| }
  236| 
  237| 
  238| /*
  239|  *  invalid:  To catch bugs.
  240|  */
  241| X(invalid)
  242| {
  243| 	fatal("PPC: invalid(): INTERNAL ERROR\n");
  244| 	exit(1);
  245| }
  246| 
  247| 
  248| /*
  249|  *  addi:  Add immediate.
  250|  *
  251|  *  arg[0] = pointer to source uint64_t
  252|  *  arg[1] = immediate value (int32_t or larger)
  253|  *  arg[2] = pointer to destination uint64_t
  254|  */
  255| X(addi)
  256| {
  257| 	reg(ic->arg[2]) = reg(ic->arg[0]) + (int32_t)ic->arg[1];
  258| }
  259| X(li)
  260| {
  261| 	reg(ic->arg[2]) = (int32_t)ic->arg[1];
  262| }
  263| X(li_0)
  264| {
  265| 	reg(ic->arg[2]) = 0;
  266| }
  267| 
  268| 
  269| /*
  270|  *  andi_dot:  AND immediate, update CR.
  271|  *
  272|  *  arg[0] = pointer to source uint64_t
  273|  *  arg[1] = immediate value (uint32_t)
  274|  *  arg[2] = pointer to destination uint64_t
  275|  */
  276| X(andi_dot)
  277| {
  278| 	MODE_uint_t tmp = reg(ic->arg[0]) & (uint32_t)ic->arg[1];
  279| 	reg(ic->arg[2]) = tmp;
  280| 	update_cr0(cpu, tmp);
  281| }
  282| 
  283| 
  284| /*
  285|  *  addic:  Add immediate, Carry.
  286|  *
  287|  *  arg[0] = pointer to source register
  288|  *  arg[1] = immediate value (int32_t or larger)
  289|  *  arg[2] = pointer to destination register
  290|  */
  291| X(addic)
  292| {
  293| 	/*  TODO/NOTE: Only for 32-bit mode, so far!  */
  294| 	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
  295| 	uint64_t tmp2 = tmp;
  296| 	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
  297| 	tmp2 += (uint32_t)ic->arg[1];
  298| 	if ((tmp2 >> 32) != (tmp >> 32))
  299| 		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
  300| 	reg(ic->arg[2]) = (uint32_t)tmp2;
  301| }
  302| 
  303| 
  304| /*
  305|  *  subfic:  Subtract from immediate, Carry.
  306|  *
  307|  *  arg[0] = pointer to source uint64_t
  308|  *  arg[1] = immediate value (int32_t or larger)
  309|  *  arg[2] = pointer to destination uint64_t
  310|  */
  311| X(subfic)
  312| {
  313| 	MODE_uint_t tmp = (int64_t)(int32_t)ic->arg[1];
  314| 	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
  315| 	if (tmp >= reg(ic->arg[0]))
  316| 		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
  317| 	reg(ic->arg[2]) = tmp - reg(ic->arg[0]);
  318| }
  319| 
  320| 
  321| /*
  322|  *  addic_dot:  Add immediate, Carry.
  323|  *
  324|  *  arg[0] = pointer to source uint64_t
  325|  *  arg[1] = immediate value (int32_t or larger)
  326|  *  arg[2] = pointer to destination uint64_t
  327|  */
  328| X(addic_dot)
  329| {
  330| 	/*  TODO/NOTE: Only for 32-bit mode, so far!  */
  331| 	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
  332| 	uint64_t tmp2 = tmp;
  333| 	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
  334| 	tmp2 += (uint32_t)ic->arg[1];
  335| 	if ((tmp2 >> 32) != (tmp >> 32))
  336| 		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
  337| 	reg(ic->arg[2]) = (uint32_t)tmp2;
  338| 	update_cr0(cpu, (uint32_t)tmp2);
  339| }
  340| 
  341| 
  342| /*
  343|  *  bclr:  Branch Conditional to Link Register
  344|  *
  345|  *  arg[0] = bo
  346|  *  arg[1] = 31 - bi
  347|  *  arg[2] = bh
  348|  */
  349| X(bclr)
  350| {
  351| 	unsigned int bo = ic->arg[0], bi31m = ic->arg[1];
  352| 	int ctr_ok, cond_ok;
  353| 	uint64_t old_pc = cpu->pc;
  354| 	MODE_uint_t tmp, addr = cpu->cd.ppc.spr[SPR_LR];
  355| 	if (!(bo & 4))
  356| 		cpu->cd.ppc.spr[SPR_CTR] --;
  357| 	ctr_ok = (bo >> 2) & 1;
  358| 	tmp = cpu->cd.ppc.spr[SPR_CTR];
  359| 	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
  360| 	cond_ok = (bo >> 4) & 1;
  361| 	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );
  362| 	if (ctr_ok && cond_ok) {
  363| 		uint64_t mask_within_page =
  364| 		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
  365| 		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  366| 		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  367| 		/*  TODO: trace in separate (duplicate) function?  */
  368| 		if (cpu->machine->show_trace_tree)
  369| 			cpu_functioncall_trace_return(cpu);
  370| 		if ((old_pc  & ~mask_within_page) ==
  371| 		    (cpu->pc & ~mask_within_page)) {
  372| 			cpu->cd.ppc.next_ic =
  373| 			    cpu->cd.ppc.cur_ic_page +
  374| 			    ((cpu->pc & mask_within_page) >>
  375| 			    PPC_INSTR_ALIGNMENT_SHIFT);
  376| 		} else {
  377| 			/*  Find the new physical page and update pointers:  */
  378| 			quick_pc_to_pointers(cpu);
  379| 		}
  380| 	}
  381| }
  382| X(bclr_20)
  383| {
  384| 	cpu->pc = cpu->cd.ppc.spr[SPR_LR];
  385| 	quick_pc_to_pointers(cpu);
  386| }
  387| X(bclr_l)
  388| {
  389| 	uint64_t low_pc, old_pc = cpu->pc;
  390| 	unsigned int bo = ic->arg[0], bi31m = ic->arg[1]  /* ,bh = ic->arg[2]*/;
  391| 	int ctr_ok, cond_ok;
  392| 	MODE_uint_t tmp, addr = cpu->cd.ppc.spr[SPR_LR];
  393| 	if (!(bo & 4))
  394| 		cpu->cd.ppc.spr[SPR_CTR] --;
  395| 	ctr_ok = (bo >> 2) & 1;
  396| 	tmp = cpu->cd.ppc.spr[SPR_CTR];
  397| 	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
  398| 	cond_ok = (bo >> 4) & 1;
  399| 	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );
  400| 
  401| 	/*  Calculate return PC:  */
  402| 	low_pc = ((size_t)ic - (size_t)
  403| 	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call) + 1;
  404| 	cpu->cd.ppc.spr[SPR_LR] = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
  405| 	    << PPC_INSTR_ALIGNMENT_SHIFT);
  406| 	cpu->cd.ppc.spr[SPR_LR] += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
  407| 
  408| 	if (ctr_ok && cond_ok) {
  409| 		uint64_t mask_within_page =
  410| 		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
  411| 		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  412| 		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  413| 		/*  TODO: trace in separate (duplicate) function?  */
  414| 		if (cpu->machine->show_trace_tree)
  415| 			cpu_functioncall_trace_return(cpu);
  416| 		if (cpu->machine->show_trace_tree)
  417| 			cpu_functioncall_trace(cpu, cpu->pc);
  418| 		if ((old_pc  & ~mask_within_page) ==
  419| 		    (cpu->pc & ~mask_within_page)) {
  420| 			cpu->cd.ppc.next_ic =
  421| 			    cpu->cd.ppc.cur_ic_page +
  422| 			    ((cpu->pc & mask_within_page) >>
  423| 			    PPC_INSTR_ALIGNMENT_SHIFT);
  424| 		} else {
  425| 			/*  Find the new physical page and update pointers:  */
  426| 			quick_pc_to_pointers(cpu);
  427| 		}
  428| 	}
  429| }
  430| 
  431| 
  432| /*
  433|  *  bcctr:  Branch Conditional to Count register
  434|  *
  435|  *  arg[0] = bo
  436|  *  arg[1] = 31 - bi
  437|  *  arg[2] = bh
  438|  */
  439| X(bcctr)
  440| {
  441| 	unsigned int bo = ic->arg[0], bi31m = ic->arg[1];
  442| 	uint64_t old_pc = cpu->pc;
  443| 	MODE_uint_t addr = cpu->cd.ppc.spr[SPR_CTR];
  444| 	int cond_ok = (bo >> 4) & 1;
  445| 	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );
  446| 	if (cond_ok) {
  447| 		uint64_t mask_within_page =
  448| 		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
  449| 		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  450| 		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
  451| 		/*  TODO: trace in separate (duplicate) function?  */
  452| 		if (cpu->machine->show_trace_tree)
  453| 			cpu_functioncall_trace_return(cpu);
  454| 		if ((old_pc  & ~mask_within_page) ==
  455| 		    (cpu->pc & ~mask_within_page)) {
  456| 			cpu->cd.ppc.next_ic =
  457| 			    cpu->cd.ppc.cur_ic_page +
  458| 			    ((cpu->pc & mask_within_page) >>
  459| 			    PPC_INSTR_ALIGNMENT_SHIFT);
  460| 		} else {
  461| 			/*  Find the new physical page and update pointers:  */
  462| 			quick_pc_to_pointers(cpu);
  463| 		}
  464| 	}
  465| }
  466| X(bcctr_l)
  467| {
  468| 	uint64_t low_pc, old_pc = cpu->pc;
  469| 	unsigned int bo = ic->arg[0], bi31m = ic->arg[1]  /*,bh = ic->arg[2] */;
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

End with one line: `FIXDRAFT_PPCBRANCH32WIDTH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
NO EDITS: the draft returned an EMPTY edit list, so nothing was changed and nothing was fixed.  If the defect is
present, write the executable change; if the code shown cannot settle it, say UNSETTLED and name exactly which
function or definition you would need to see.
```

The previous edits:

```json
[]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.

## YOUR PREVIOUS DRAFT FAILED -- correct it (the last retry)

```text
YOUR PREVIOUS REPLY SAID `STILL PRESENT: YES` BUT CONTAINED NO ```json EDIT BLOCK, so nothing could be applied.
Return the edit list in exactly one ```json block, or say UNSETTLED and name what is missing.
```

The previous edits:

```json
(none -- the reply had no edit block)
```

End with the line `FIXDRAFT_PPCBRANCH32WIDTH: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
