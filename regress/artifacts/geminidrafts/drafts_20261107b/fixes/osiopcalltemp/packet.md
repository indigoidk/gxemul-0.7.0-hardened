# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopcalltemp` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopcalltemp`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c JUMP/CALL -- CALL does not save the return address in TEMP while RETURN jumps to TEMP -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T83 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A7-39).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:859, :810.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 859 (HEAD 8d9df658, lines 739-979)

```c
  739| 					debug(" ATN");
  740| 				if (bit_ack)
  741| 					debug(" ACK");
  742| 				if (bit_target)
  743| 					debug(" TARGET");
  744| 				if (bit_carry)
  745| 					debug(" CARRY");
  746| 			}
  747| 					
  748| 			if (opcode == 3) {
  749| 				d->reg[OSIOP_SOCL] |= (bit_ack * OSIOP_ACK);
  750| 				d->reg[OSIOP_SOCL] |= (bit_atn * OSIOP_ATN);
  751| 				if (bit_carry)
  752| 					d->carry = 1;
  753| 				d->reg[OSIOP_SCNTL0] |=
  754| 				    (bit_target * OSIOP_SCNTL0_TRG);
  755| 			} else {
  756| 				d->reg[OSIOP_SOCL] &= ~(bit_ack * OSIOP_ACK);
  757| 				d->reg[OSIOP_SOCL] &= ~(bit_atn * OSIOP_ATN);
  758| 				if (bit_carry)
  759| 					d->carry = 0;
  760| 				d->reg[OSIOP_SCNTL0] &=
  761| 				    ~(bit_target * OSIOP_SCNTL0_TRG);
  762| 			}
  763| 		}
  764| 
  765| 		break;
  766| 
  767| 	case 0x80:
  768| 		/*  Transfer Control  */
  769| 		relative_addressing = (dbc >> 23) & 1;
  770| 		test_carry = (dbc >> 21) & 1;
  771| 		jump_if_true = (dbc >> 19) & 1;
  772| 		compare_data = (dbc >> 18) & 1;
  773| 		compare_phase = (dbc >> 17) & 1;
  774| 		wait_for_valid_phase = (dbc >> 16) & 1;
  775| 		
  776| 		switch (opcode) {
  777| 		case 0:	if (osiop_debug)
  778| 				debug(": JUMP");
  779| 			break;
  780| 		case 1:	if (osiop_debug)
  781| 				debug(": CALL");
  782| 			break;
  783| 		case 2:	if (osiop_debug)
  784| 				debug(": RETURN");
  785| 			break;
  786| 		case 3:	if (osiop_debug)
  787| 				debug(": INTERRUPT");
  788| 			break;
  789| 		default:fatal(": UNIMPLEMENTED dcmd=0x%02x opcode=%i\n",
  790| 			    dcmd, opcode);
  791| 			exit(1);
  792| 		}
  793| 
  794| 		if (opcode == 0 || opcode == 1) {
  795| 			if (relative_addressing) {
  796| 				/*  Note: Relative to _current_ DSP value,
  797| 				    not what it was when the current instruction
  798| 				    was read!  */
  799| 				target_addr = reladdr + *dspp;
  800| 				if (osiop_debug)
  801| 					debug(" REL(%i)", reladdr);
  802| 			} else {
  803| 				target_addr = instr2;
  804| 				if (osiop_debug)
  805| 					debug(" 0x%08x", instr2);
  806| 			}
  807| 		} else {
  808| 			if (opcode == 2) {
  809| 				/*  Return:  */
  810| 				target_addr = *tempp;
  811| 			} else {
  812| 				/*  Interrupt:  */
  813| 				interrupt_instead_of_branch = 1;
  814| 			}
  815| 		}
  816| 
  817| 		if (test_carry) {
  818| 			if (compare_data || compare_phase) {
  819| 				fatal("osiop: TODO: test_carry cannot be"
  820| 				    " combined with other tests!\n");
  821| 				exit(1);
  822| 			}
  823| 			
  824| 			fatal("osiop: TODO: test_carry\n");
  825| 			exit(1);
  826| 		}
  827| 
  828| 		if (compare_data) {
  829| 			fatal("osiop: TODO: compare_data\n");
  830| 			exit(1);
  831| 		}
  832| 
  833| 		if (compare_phase) {
  834| 			int cur_phase;
  835| 
  836| 			if (osiop_debug)
  837| 				debug(" %s %s%s",
  838| 				    wait_for_valid_phase ? "WHEN" : "IF",
  839| 				    jump_if_true? "" : "NOT ",
  840| 				    phases[phase]);
  841| 
  842| 			/*  TODO: wait for valid phase!  */
  843| 
  844| 			cur_phase = osiop_get_scsi_phase(d);
  845| 			
  846| 			comparison = (phase == cur_phase);
  847| 		}
  848| 
  849| 		if (!test_carry && !compare_data && !compare_phase)
  850| 			jump_if_true = comparison = 1;
  851| 
  852| 		if ((jump_if_true && comparison) ||
  853| 		    (!jump_if_true && !comparison)) {
  854| 			/*  Perform the branch or interrupt.  */
  855| 			if (interrupt_instead_of_branch) {
  856| 				d->scripts_running = 0;
  857| 				d->reg[OSIOP_DSTAT] |= OSIOP_DSTAT_SIR;
  858| 			} else {
  859| 				*dspp = target_addr;
  860| 			}
  861| 		}
  862| 
  863| 		break;
  864| 
  865| 	case 0xc0:
  866| 		if (osiop_debug)
  867| 			debug(": MEMORY MOVE");
  868| 		/*  TODO: third instruction word!  */
  869| 		fatal(": TODO\n");
  870| 		exit(1);
  871| 		break;
  872| 
  873| 	default:fatal(": UNIMPLEMENTED dcmd 0x%02x\n", dcmd);
  874| 		exit(1);
  875| 	}
  876| 
  877| 	if (osiop_debug)
  878| 		debug(" }\n");
  879| 
  880| 	return 1;
  881| }
  882| 
  883| 
  884| /*
  885|  *  osiop_execute_scripts():
  886|  *
  887|  *  Interprets SCRIPTS machine code by reading one instruction word at a time,
  888|  *  and executing it.
  889|  */
  890| void osiop_execute_scripts(struct cpu *cpu, struct osiop_data *d)
  891| {
  892| 	int n = 0;
  893| 
  894| 	if (osiop_debug)
  895| 		debug("{ SCRIPTS start }\n");
  896| 
  897| 	while (d->scripts_running && n < MAX_SCRIPTS_PER_CHUNK &&
  898| 	    osiop_execute_scripts_instr(cpu, d))
  899| 		n++;
  900| 
  901| 	if (osiop_debug)	
  902| 		debug("{ SCRIPTS end }\n");
  903| }
  904| 
  905| 
  906| DEVICE_TICK(osiop)
  907| {
  908| 	struct osiop_data *d = (struct osiop_data *) extra;
  909| 
  910| 	if (d->scripts_running)
  911| 		osiop_execute_scripts(cpu, d);
  912| 
  913| 	osiop_reassert_interrupts(d);
  914| }
  915| 
  916| 
  917| DEVICE_ACCESS(osiop)
  918| {
  919| 	uint64_t idata = 0, odata = 0;
  920| 	uint8_t oldreg = 0;
  921| 	struct osiop_data *d = (struct osiop_data *) extra;
  922| 	int origofs = relative_addr;
  923| 	int non1lenOk = 0;
  924| 
  925| 	idata = memory_readmax64(cpu, data, len);
  926| 
  927| 	/*  Make relative_addr suit addresses in osiopreg.h:  */
  928| 	if (cpu->byte_order == EMUL_BIG_ENDIAN) {
  929| 		relative_addr =
  930| 		    (relative_addr & ~3) |
  931| 		    (3 - (relative_addr & 3));
  932| 	}
  933| 
  934| 	if (len == sizeof(uint32_t)) {
  935| 		/*
  936| 		 *  NOTE: These are stored in HOST byte order!
  937| 		 */
  938| 		switch (origofs) {
  939| 		case OSIOP_DSA:
  940| 		case OSIOP_TEMP:
  941| 		case OSIOP_DBC:
  942| 		case OSIOP_DNAD:
  943| 		case OSIOP_DSP:
  944| 		case OSIOP_DSPS:
  945| 		case OSIOP_SCRATCH:
  946| 		case OSIOP_ADDER:
  947| 			relative_addr = origofs;
  948| 			non1lenOk = 1;
  949| 
  950| 			uint32_t *p = (uint32_t*) &d->reg[origofs];
  951| 
  952| 			if (writeflag == MEM_WRITE)
  953| 				*p = idata;
  954| 			else
  955| 				odata = *p;
  956| 			
  957| 			break;
  958| 		}
  959| 	} else {
  960| 		/*  Byte access:  */
  961| 		oldreg = d->reg[relative_addr];
  962| 
  963| 		if (writeflag == MEM_WRITE)
  964| 			d->reg[relative_addr] = idata;
  965| 		else
  966| 			odata = oldreg;
  967| 	}
  968| 
  969| 	switch (relative_addr) {
  970| 
  971| 	case OSIOP_SCNTL0:
  972| 	case OSIOP_SCNTL1:
  973| 		break;
  974| 
  975| 	case OSIOP_SIEN:
  976| 		/*  Used by OpenBSD/mvme88k during probing:  */
  977| 		if (len == 4)
  978| 			non1lenOk = 1;
  979| 		if (writeflag == MEM_WRITE)
```

## The data structures those files define (every field that exists)

### `src/devices/dev_osiop.c` -- `struct osiop_data {` (HEAD lines 75-99)

```c
   75| struct osiop_data {
   76| 	struct interrupt	irq;
   77| 	int			asserted;
   78| 	
   79| 	int			scripts_running;
   80| 
   81| 	/*  Current transfer:  */
   82| 	int			selected_id;
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			data_offset;
   85| 
   86| 	/*  Cached emulated physical RAM page lookup:  */
   87| 	uint32_t		last_phys_page;
   88| 	uint8_t			*last_host_page;
   89| 	int			hostpage_fault_warned;	/* #118: warn once */
   90| 
   91| 	/*  ALU:  */
   92| 	int			carry;
   93| 	
   94| 	/*
   95| 	 *  Most of these are byte-addressed, but some are not. (Note: For
   96| 	 *  convenience, 32-bit words are stored in host byte order!)
   97| 	 */
   98| 	uint8_t			reg[OSIOP_NREGS];
   99| };
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

End with one line: `FIXDRAFT_OSIOPCALLTEMP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
