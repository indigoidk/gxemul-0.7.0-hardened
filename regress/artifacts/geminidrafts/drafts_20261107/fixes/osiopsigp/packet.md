# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopsigp` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopsigp`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c -- an ISTAT SIGP write stops the script instead of waking WAIT RESELECT; CTEST2's SIGP mirror, the selection-timeout STO bit and SFBR are not modelled -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T84 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A7-40).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:1063-1083, :1043-1051, :693-700.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 1063 (HEAD d2a6f233, lines 1018-1108)

```c
 1018| 	case OSIOP_DSTAT:
 1019| 		/*  Cleared when read. Most likely not writable.  */
 1020| 		odata = d->reg[OSIOP_DSTAT];
 1021| 		d->reg[OSIOP_DSTAT] = OSIOP_DSTAT_DFE;
 1022| 		osiop_reassert_interrupts(d);
 1023| 		break;
 1024| 
 1025| 	case OSIOP_SSTAT0:
 1026| 		/*  Cleared when read. Most likely not writable.  */
 1027| 		odata = d->reg[OSIOP_SSTAT0];
 1028| 		d->reg[OSIOP_SSTAT0] = 0;
 1029| 		osiop_reassert_interrupts(d);
 1030| 		break;
 1031| 
 1032| 	case OSIOP_SSTAT1:
 1033| 	case OSIOP_SSTAT2:
 1034| 		break;
 1035| 		
 1036| 	case OSIOP_DSA:
 1037| 		if (writeflag == MEM_WRITE) {
 1038| 			if (osiop_debug)
 1039| 				debug("[ osiop: DSA set to 0x%x ]\n", (int) idata);
 1040| 		}
 1041| 		break;
 1042| 
 1043| 	case OSIOP_CTEST0:
 1044| 	case OSIOP_CTEST1:
 1045| 	case OSIOP_CTEST2:
 1046| 	case OSIOP_CTEST3:
 1047| 	case OSIOP_CTEST4:
 1048| 	case OSIOP_CTEST5:
 1049| 	case OSIOP_CTEST6:
 1050| 	case OSIOP_CTEST7:
 1051| 		break;
 1052| 
 1053| 	case OSIOP_TEMP:
 1054| 		if (writeflag == MEM_WRITE) {
 1055| 			if (osiop_debug)
 1056| 				debug("[ osiop: TEMP set to 0x%x ]\n", (int) idata);
 1057| 		}
 1058| 		break;
 1059| 
 1060| 	case OSIOP_DFIFO:
 1061| 		break;
 1062| 
 1063| 	case OSIOP_ISTAT:
 1064| 		if (writeflag == MEM_WRITE) {
 1065| 			if ((idata & 0x3f) != 0x00) {
 1066| 				/*  Unimplemented low ISTAT bits, reachable
 1067| 				    via an ordinary register write and
 1068| 				    recoverable: warn once, drop the
 1069| 				    unimplemented bits and stop the script
 1070| 				    engine (the #118 pattern) instead of
 1071| 				    exit(1).  */
 1072| 				static int warned = 0;
 1073| 				if (!warned) {
 1074| 					fatal("[ osiop: TODO: istat 0x%x; "
 1075| 					    "ignoring unimplemented low bits, "
 1076| 					    "stopping script ]\n", (int) idata);
 1077| 					warned = 1;
 1078| 				}
 1079| 				d->scripts_running = 0;
 1080| 				idata &= ~0x3f;
 1081| 			}
 1082| 
 1083| 			d->reg[relative_addr] = idata &
 1084| 			    ~(OSIOP_ISTAT_ABRT | OSIOP_ISTAT_RST);
 1085| 			osiop_reassert_interrupts(d);
 1086| 		}
 1087| 		break;
 1088| 
 1089| 	case OSIOP_CTEST8:
 1090| 		odata = (odata & 0xf) | (OSIOP_CHIP_REVISION << 4);
 1091| 		break;
 1092| 
 1093| 	case OSIOP_DBC:
 1094| 		break;
 1095| 
 1096| 	case OSIOP_DSP:
 1097| 		if (writeflag == MEM_WRITE) {
 1098| 			if (osiop_debug)
 1099| 				debug("[ osiop: DSP set to 0x%x ]\n", (int) idata);
 1100| 
 1101| 			d->scripts_running = 1;
 1102| 			osiop_execute_scripts(cpu, d);
 1103| 			osiop_reassert_interrupts(d);
 1104| 		}
 1105| 		break;
 1106| 
 1107| 	case OSIOP_DSPS:
 1108| 	case OSIOP_SCRATCH:
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

End with one line: `FIXDRAFT_OSIOPSIGP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
