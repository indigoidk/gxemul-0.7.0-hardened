# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armbxalignstop` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armbxalignstop`, state `open`, severity `LOW`)

**title:** src/cpus/cpu_arm_instr.c:365-367,396-398,497-499 -- a BX or BLX target with bit 1 set and bit 0 clear prints ARM pc misaligned? and sets cpu->running = 0 in X(bx), X(bx_trace) and X(blx_reg), where the target is UNPREDICTABLE and the ARM ARM forbids a halt -- CPU-STOP

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- guest instruction can trigger forbidden CPU halt (guest DoS)

## The code at the cited lines

### `src/cpus/cpu_arm_instr.c` around the row's cited line 365 (HEAD 8d9df658, lines 245-485)

```c
  245|  */
  246| X(nop)
  247| {
  248| }
  249| 
  250| 
  251| /*
  252|  *  b:  Branch (to a different translated page)
  253|  *
  254|  *  arg[0] = relative offset from start of page
  255|  */
  256| X(b)
  257| {
  258| 	cpu->pc = (uint32_t)((cpu->pc & 0xfffff000) + (int32_t)ic->arg[0]);
  259| 
  260| 	/*  Find the new physical page and update the translation pointers:  */
  261| 	quick_pc_to_pointers_arm(cpu);
  262| }
  263| Y(b)
  264| 
  265| 
  266| /*
  267|  *  b_samepage:  Branch (to within the same translated page)
  268|  *
  269|  *  arg[0] = pointer to new arm_instr_call
  270|  *  arg[1] = pointer to the next instruction.
  271|  *
  272|  *  NOTE: This instruction is manually inlined.
  273|  */
  274| X(b_samepage) {
  275| 	cpu->cd.arm.next_ic = (struct arm_instr_call *) ic->arg[0];
  276| }
  277| X(b_samepage__eq) {
  278| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  279| 	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 0 : 1];
  280| }
  281| X(b_samepage__ne) {
  282| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  283| 	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 1 : 0];
  284| }
  285| X(b_samepage__cs) {
  286| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  287| 	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 0 : 1];
  288| }
  289| X(b_samepage__cc) {
  290| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  291| 	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 1 : 0];
  292| }
  293| X(b_samepage__mi) {
  294| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  295| 	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 0 : 1];
  296| }
  297| X(b_samepage__pl) {
  298| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  299| 	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 1 : 0];
  300| }
  301| X(b_samepage__vs) {
  302| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  303| 	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 0 : 1];
  304| }
  305| X(b_samepage__vc) {
  306| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  307| 	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 1 : 0];
  308| }
  309| X(b_samepage__hi) {
  310| 	cpu->cd.arm.next_ic = (condition_hi[cpu->cd.arm.flags])?
  311| 	    (struct arm_instr_call *) ic->arg[0] :
  312| 	    (struct arm_instr_call *) ic->arg[1];
  313| }
  314| X(b_samepage__ls) {
  315| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  316| 	    ic->arg[condition_hi[cpu->cd.arm.flags]];
  317| }
  318| X(b_samepage__ge) {
  319| 	cpu->cd.arm.next_ic = (condition_ge[cpu->cd.arm.flags])?
  320| 	    (struct arm_instr_call *) ic->arg[0] :
  321| 	    (struct arm_instr_call *) ic->arg[1];
  322| }
  323| X(b_samepage__lt) {
  324| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  325| 	    ic->arg[condition_ge[cpu->cd.arm.flags]];
  326| }
  327| X(b_samepage__gt) {
  328| 	cpu->cd.arm.next_ic = (condition_gt[cpu->cd.arm.flags])?
  329| 	    (struct arm_instr_call *) ic->arg[0] :
  330| 	    (struct arm_instr_call *) ic->arg[1];
  331| }
  332| X(b_samepage__le) {
  333| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  334| 	    ic->arg[condition_gt[cpu->cd.arm.flags]];
  335| }
  336| void (*arm_cond_instr_b_samepage[16])(struct cpu *,
  337| 	struct arm_instr_call *) = {
  338| 	arm_instr_b_samepage__eq, arm_instr_b_samepage__ne,
  339| 	arm_instr_b_samepage__cs, arm_instr_b_samepage__cc,
  340| 	arm_instr_b_samepage__mi, arm_instr_b_samepage__pl,
  341| 	arm_instr_b_samepage__vs, arm_instr_b_samepage__vc,
  342| 	arm_instr_b_samepage__hi, arm_instr_b_samepage__ls,
  343| 	arm_instr_b_samepage__ge, arm_instr_b_samepage__lt,
  344| 	arm_instr_b_samepage__gt, arm_instr_b_samepage__le,
  345| 	arm_instr_b_samepage, arm_instr_nop };
  346| 
  347| 
  348| /*
  349|  *  bx:  Branch, potentially exchanging Thumb/ARM encoding
  350|  *
  351|  *  arg[0] = ptr to rm
  352|  */
  353| X(bx)
  354| {
  355| 	uint32_t old_cpsr = cpu->cd.arm.cpsr;
  356| 	cpu->pc = reg(ic->arg[0]);
  357| 	if (cpu->pc & 1)
  358| 		cpu->cd.arm.cpsr |= ARM_FLAG_T;
  359| 	else
  360| 		cpu->cd.arm.cpsr &= ~ARM_FLAG_T;
  361| 
  362| 	if (cpu->cd.arm.cpsr != old_cpsr)
  363| 		cpu->cd.arm.next_ic = &nothing_call;
  364| 
  365| 	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
  366| 		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
  367| 		cpu->running = 0;
  368| 		cpu->n_translated_instrs --;
  369| 		cpu->cd.arm.next_ic = &nothing_call;
  370| 		return;
  371| 	}
  372| 
  373| 	/*  Find the new physical page and update the translation pointers:  */
  374| 	quick_pc_to_pointers_arm(cpu);
  375| }
  376| Y(bx)
  377| 
  378| 
  379| /*
  380|  *  bx_trace:  As bx, but with trace enabled, arg[0] = the link register.
  381|  *
  382|  *  arg[0] = ignored
  383|  */
  384| X(bx_trace)
  385| {
  386| 	uint32_t old_cpsr = cpu->cd.arm.cpsr;
  387| 	cpu->pc = cpu->cd.arm.r[ARM_LR];
  388| 	if (cpu->pc & 1)
  389| 		cpu->cd.arm.cpsr |= ARM_FLAG_T;
  390| 	else
  391| 		cpu->cd.arm.cpsr &= ~ARM_FLAG_T;
  392| 
  393| 	if (cpu->cd.arm.cpsr != old_cpsr)
  394| 		cpu->cd.arm.next_ic = &nothing_call;
  395| 
  396| 	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
  397| 		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
  398| 		cpu->running = 0;
  399| 		cpu->n_translated_instrs --;
  400| 		cpu->cd.arm.next_ic = &nothing_call;
  401| 		return;
  402| 	}
  403| 
  404| 	cpu_functioncall_trace_return(cpu);
  405| 
  406| 	/*  Find the new physical page and update the translation pointers:  */
  407| 	quick_pc_to_pointers_arm(cpu);
  408| }
  409| Y(bx_trace)
  410| 
  411| 
  412| /*
  413|  *  bl:  Branch and Link (to a different translated page)
  414|  *
  415|  *  arg[0] = relative address
  416|  *  arg[1] = offset within current page to the instruction
  417|  */
  418| X(bl)
  419| {
  420| 	uint32_t pc = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[1];
  421| 	cpu->cd.arm.r[ARM_LR] = pc + 4;
  422| 
  423| 	/*  Calculate new PC from this instruction + arg[0]  */
  424| 	cpu->pc = pc + (int32_t)ic->arg[0];
  425| 
  426| 	/*  Find the new physical page and update the translation pointers:  */
  427| 	quick_pc_to_pointers_arm(cpu);
  428| }
  429| Y(bl)
  430| 
  431| 
  432| /*
  433|  *  blx_imm:  Branch and Link, always switching to THUMB encoding
  434|  *
  435|  *  arg[0] = relative address
  436|  *  arg[1] = offset within current page to the current instruction
  437|  */
  438| X(blx_imm)
  439| {
  440| 	uint32_t pc = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[1];
  441| 	uint32_t old_cpsr = cpu->cd.arm.cpsr;
  442| 	cpu->cd.arm.r[ARM_LR] = pc + 4;
  443| 
  444| 	/*  Calculate new PC from this instruction + arg[0]  */
  445| 	cpu->pc = pc + (int32_t)ic->arg[0];
  446| 
  447| 	if (cpu->pc & 1)
  448| 		cpu->cd.arm.cpsr |= ARM_FLAG_T;
  449| 	else {
  450| 		fatal("[ blx_imm internal error. Should have switched to THUMB! 0x%08x ]\n", (int)cpu->pc);
  451| 		cpu->running = 0;
  452| 		cpu->n_translated_instrs --;
  453| 		cpu->cd.arm.next_ic = &nothing_call;
  454| 		return;
  455| 	}
  456| 
  457| 	if (cpu->cd.arm.cpsr != old_cpsr)
  458| 		cpu->cd.arm.next_ic = &nothing_call;
  459| 
  460| 	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
  461| 		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
  462| 		cpu->running = 0;
  463| 		cpu->n_translated_instrs --;
  464| 		cpu->cd.arm.next_ic = &nothing_call;
  465| 		return;
  466| 	}
  467| 
  468| 	if (cpu->machine->show_trace_tree)
  469| 		cpu_functioncall_trace(cpu, cpu->pc);
  470| 
  471| 	/*  Find the new physical page and update the translation pointers:  */
  472| 	quick_pc_to_pointers_arm(cpu);
  473| }
  474| 
  475| 
  476| /*
  477|  *  blx_reg:  Branch and Link, potentially exchanging Thumb/ARM encoding
  478|  *
  479|  *  arg[0] = ptr to rm
  480|  *  arg[2] = offset within current page to the instruction to return to
  481|  */
  482| X(blx_reg)
  483| {
  484| 	uint32_t lr = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
  485| 	cpu->cd.arm.r[ARM_LR] = lr;
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

End with one line: `FIXDRAFT_ARMBXALIGNSTOP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL  edit 1 src/cpus/cpu_arm_instr.c: old occurs 2 times
```

The previous edits:

```json
[
  {
    "file": "src/cpus/cpu_arm_instr.c",
    "old": "\tif (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {\n\t\tfatal(\"[ ARM pc misaligned? 0x%08x ]\\n\", (int)cpu->pc);\n\t\tcpu->running = 0;\n\t\tcpu->n_translated_instrs --;\n\t\tcpu->cd.arm.next_ic = &nothing_call;\n\t\treturn;\n\t}\n\n\t/*  Find the new physical page and update the translation pointers:  */",
    "new": "\tif (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {\n\t\t/* #001: ARM ARM forbids a halt on misaligned pc */\n\t\tfatal(\"[ ARM pc misaligned? 0x%08x ]\\n\", (int)cpu->pc);\n\t}\n\n\t/*  Find the new physical page and update the translation pointers:  */",
    "why": "Remove CPU halt on UNPREDICTABLE misaligned BX target"
  },
  {
    "file": "src/cpus/cpu_arm_instr.c",
    "old": "\tif (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {\n\t\tfatal(\"[ ARM pc misaligned? 0x%08x ]\\n\", (int)cpu->pc);\n\t\tcpu->running = 0;\n\t\tcpu->n_translated_instrs --;\n\t\tcpu->cd.arm.next_ic = &nothing_call;\n\t\treturn;\n\t}\n\n\tcpu_functioncall_trace_return(cpu);",
    "new": "\tif (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {\n\t\t/* #002: ARM ARM forbids a halt on misaligned pc */\n\t\tfatal(\"[ ARM pc misaligned? 0x%08x ]\\n\", (int)cpu->pc);\n\t}\n\n\tcpu_functioncall_trace_return(cpu);",
    "why": "Remove CPU halt on UNPREDICTABLE misaligned BX_trace target"
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
