# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopcalltemp` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopcalltemp`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c JUMP/CALL -- CALL does not save the return address in TEMP while RETURN jumps to TEMP -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T83 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A7-39).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:859, :810.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 859 (HEAD d2a6f233, lines 814-904)

```c
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
