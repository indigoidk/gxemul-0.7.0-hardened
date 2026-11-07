# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `osiopcalltemp` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `osiopcalltemp`, state `open`)

**title:** devices/dev_osiop.c JUMP/CALL -- CALL does not save the return address in TEMP while RETURN jumps to TEMP -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T83 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A7-39).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:859, :810.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_osiop.c:859 (`*dspp = target_addr;` handles CALL without saving to TEMP)

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_osiop.c b/src/devices/dev_osiop.c
index 87e9e955..a3713ff5 100644
--- a/src/devices/dev_osiop.c
+++ b/src/devices/dev_osiop.c
@@ -856,6 +856,9 @@ int osiop_execute_scripts_instr(struct cpu *cpu, struct osiop_data *d)
 				d->scripts_running = 0;
 				d->reg[OSIOP_DSTAT] |= OSIOP_DSTAT_SIR;
 			} else {
+				/* #T83: CALL must save return address to TEMP */
+				if (opcode == 1)
+					*tempp = *dspp;
 				*dspp = target_addr;
 			}
 		}
```

## Every edited function, after the fix

### `src/devices/dev_osiop.c` -- post-edit lines 330-884 (`+` marks a line the diff added or the point of a deletion)

```c
  330|  int osiop_execute_scripts_instr(struct cpu *cpu, struct osiop_data *d)
  331|  {
  332|  	uint32_t *dsap = (uint32_t*) &d->reg[OSIOP_DSA];
  333|  	uint32_t *dnadp = (uint32_t*) &d->reg[OSIOP_DNAD];
  334|  	uint32_t *dbcp = (uint32_t*) &d->reg[OSIOP_DBC];
     | [... lines 335-748 not shown ...]
  749|  				d->reg[OSIOP_SOCL] |= (bit_ack * OSIOP_ACK);
  750|  				d->reg[OSIOP_SOCL] |= (bit_atn * OSIOP_ATN);
  751|  				if (bit_carry)
  752|  					d->carry = 1;
  753|  				d->reg[OSIOP_SCNTL0] |=
  754|  				    (bit_target * OSIOP_SCNTL0_TRG);
  755|  			} else {
  756|  				d->reg[OSIOP_SOCL] &= ~(bit_ack * OSIOP_ACK);
  757|  				d->reg[OSIOP_SOCL] &= ~(bit_atn * OSIOP_ATN);
  758|  				if (bit_carry)
  759|  					d->carry = 0;
  760|  				d->reg[OSIOP_SCNTL0] &=
  761|  				    ~(bit_target * OSIOP_SCNTL0_TRG);
  762|  			}
  763|  		}
  764|  
  765|  		break;
  766|  
  767|  	case 0x80:
  768|  		/*  Transfer Control  */
  769|  		relative_addressing = (dbc >> 23) & 1;
  770|  		test_carry = (dbc >> 21) & 1;
  771|  		jump_if_true = (dbc >> 19) & 1;
  772|  		compare_data = (dbc >> 18) & 1;
  773|  		compare_phase = (dbc >> 17) & 1;
  774|  		wait_for_valid_phase = (dbc >> 16) & 1;
  775|  		
  776|  		switch (opcode) {
  777|  		case 0:	if (osiop_debug)
  778|  				debug(": JUMP");
  779|  			break;
  780|  		case 1:	if (osiop_debug)
  781|  				debug(": CALL");
  782|  			break;
  783|  		case 2:	if (osiop_debug)
  784|  				debug(": RETURN");
  785|  			break;
  786|  		case 3:	if (osiop_debug)
  787|  				debug(": INTERRUPT");
  788|  			break;
  789|  		default:fatal(": UNIMPLEMENTED dcmd=0x%02x opcode=%i\n",
  790|  			    dcmd, opcode);
  791|  			exit(1);
  792|  		}
  793|  
  794|  		if (opcode == 0 || opcode == 1) {
  795|  			if (relative_addressing) {
  796|  				/*  Note: Relative to _current_ DSP value,
  797|  				    not what it was when the current instruction
  798|  				    was read!  */
  799|  				target_addr = reladdr + *dspp;
  800|  				if (osiop_debug)
  801|  					debug(" REL(%i)", reladdr);
  802|  			} else {
  803|  				target_addr = instr2;
  804|  				if (osiop_debug)
  805|  					debug(" 0x%08x", instr2);
  806|  			}
  807|  		} else {
  808|  			if (opcode == 2) {
  809|  				/*  Return:  */
  810|  				target_addr = *tempp;
  811|  			} else {
  812|  				/*  Interrupt:  */
  813|  				interrupt_instead_of_branch = 1;
  814|  			}
  815|  		}
  816|  
  817|  		if (test_carry) {
  818|  			if (compare_data || compare_phase) {
  819|  				fatal("osiop: TODO: test_carry cannot be"
  820|  				    " combined with other tests!\n");
  821|  				exit(1);
  822|  			}
  823|  			
  824|  			fatal("osiop: TODO: test_carry\n");
  825|  			exit(1);
  826|  		}
  827|  
  828|  		if (compare_data) {
  829|  			fatal("osiop: TODO: compare_data\n");
  830|  			exit(1);
  831|  		}
  832|  
  833|  		if (compare_phase) {
  834|  			int cur_phase;
  835|  
  836|  			if (osiop_debug)
  837|  				debug(" %s %s%s",
  838|  				    wait_for_valid_phase ? "WHEN" : "IF",
  839|  				    jump_if_true? "" : "NOT ",
  840|  				    phases[phase]);
  841|  
  842|  			/*  TODO: wait for valid phase!  */
  843|  
  844|  			cur_phase = osiop_get_scsi_phase(d);
  845|  			
  846|  			comparison = (phase == cur_phase);
  847|  		}
  848|  
  849|  		if (!test_carry && !compare_data && !compare_phase)
  850|  			jump_if_true = comparison = 1;
  851|  
  852|  		if ((jump_if_true && comparison) ||
  853|  		    (!jump_if_true && !comparison)) {
  854|  			/*  Perform the branch or interrupt.  */
  855|  			if (interrupt_instead_of_branch) {
  856|  				d->scripts_running = 0;
  857|  				d->reg[OSIOP_DSTAT] |= OSIOP_DSTAT_SIR;
  858|  			} else {
  859|+ 				/* #T83: CALL must save return address to TEMP */
  860|+ 				if (opcode == 1)
  861|+ 					*tempp = *dspp;
  862|  				*dspp = target_addr;
  863|  			}
  864|  		}
  865|  
  866|  		break;
  867|  
  868|  	case 0xc0:
  869|  		if (osiop_debug)
  870|  			debug(": MEMORY MOVE");
  871|  		/*  TODO: third instruction word!  */
  872|  		fatal(": TODO\n");
  873|  		exit(1);
  874|  		break;
  875|  
  876|  	default:fatal(": UNIMPLEMENTED dcmd 0x%02x\n", dcmd);
  877|  		exit(1);
  878|  	}
  879|  
  880|  	if (osiop_debug)
  881|  		debug(" }\n");
  882|  
  883|  	return 1;
  884|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_OSIOPCALLTEMP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_OSIOPCALLTEMP: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
