# GXemul hardened fork -- DRAFT A FIX for one filed issue, `osiopwidelanes` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `osiopwidelanes`, state `open`, severity `MED`)

**title:** devices/dev_osiop.c:dev_osiop_access -- a wide access to byte registers is not split into byte lanes (it now warns and stops the script) -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T85 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-41).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/devices/dev_osiop.c:1155-1167.  Portable fix: yes -- port ajfa mvme187 4a01173 patch 04.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port ajfa mvme187 4a01173 patch 04

## The code at the cited lines

### `src/devices/dev_osiop.c` around the row's cited line 1155 (HEAD d2a6f233, lines 1110-1200)

```c
 1110| 
 1111| 	case OSIOP_DMODE:
 1112| 		break;
 1113| 
 1114| 	case OSIOP_DIEN:
 1115| 		if (writeflag == MEM_WRITE)
 1116| 			osiop_reassert_interrupts(d);
 1117| 		break;
 1118| 
 1119| 	case OSIOP_DWT:
 1120| 		break;
 1121| 
 1122| 	case OSIOP_DCNTL:
 1123| 		if (writeflag == MEM_WRITE &&
 1124| 		    (idata & (OSIOP_DCNTL_SSM | OSIOP_DCNTL_LLM |
 1125| 		    OSIOP_DCNTL_STD))) {
 1126| 			/*  Unimplemented DCNTL modes (single-step, low-level,
 1127| 			    manual start-DMA), reachable via an ordinary
 1128| 			    register write and recoverable: warn once and stop
 1129| 			    the script engine (the #118 pattern) instead of
 1130| 			    exit(1). The message includes the value, so the
 1131| 			    specific bit (SSM/LLM/STD) is identifiable.  */
 1132| 			static int warned = 0;
 1133| 			if (!warned) {
 1134| 				fatal("[ osiop: TODO: DCNTL 0x%02x (SSM/LLM/"
 1135| 				    "STD unimplemented); stopping script ]\n",
 1136| 				    (int) idata);
 1137| 				warned = 1;
 1138| 			}
 1139| 			d->scripts_running = 0;
 1140| 		}
 1141| 		break;
 1142| 
 1143| 	default:
 1144| 		if (writeflag == MEM_READ) {
 1145| 			fatal("[ osiop: read from 0x%02lx ]\n",
 1146| 			    (long)relative_addr);
 1147| 		} else {
 1148| 			fatal("[ osiop: write to  0x%02lx: 0x%02x ]\n",
 1149| 			    (long)relative_addr, (int)idata);
 1150| 		}
 1151| 
 1152| 		exit(1);
 1153| 	}
 1154| 
 1155| 	if (len != 1 && !non1lenOk) {
 1156| 		/*  Unusual access width from the guest, on a register where
 1157| 		    only byte access is implemented: recoverable, so warn once
 1158| 		    and stop the script engine (the #118 pattern), completing
 1159| 		    the access instead of exit(1).  */
 1160| 		static int warned = 0;
 1161| 		if (!warned) {
 1162| 			fatal("[ osiop: TODO: len != 1, addr 0x%0x; "
 1163| 			    "stopping script ]\n", (int)relative_addr);
 1164| 			warned = 1;
 1165| 		}
 1166| 		d->scripts_running = 0;
 1167| 	}
 1168| 
 1169| 	if (writeflag == MEM_READ)
 1170| 		memory_writemax64(cpu, data, len, odata);
 1171| 
 1172| 	return 1;
 1173| }
 1174| 
 1175| 
 1176| DEVINIT(osiop)
 1177| {
 1178| 	struct osiop_data *d;
 1179| 
 1180| 	CHECK_ALLOCATION(d = (struct osiop_data *) malloc(sizeof(struct osiop_data)));
 1181| 	memset(d, 0, sizeof(struct osiop_data));
 1182| 
 1183| 	/*  Set up initial device register values:  */
 1184| 	d->reg[OSIOP_SCID] = OSIOP_SCID_VALUE(7);
 1185| 
 1186| 	/*  OpenBSD's osiop_checkintr needs this:  */
 1187| 	d->reg[OSIOP_CTEST1] = OSIOP_CTEST1_FMT;
 1188| 
 1189| 	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);
 1190| 
 1191| 	memory_device_register(devinit->machine->memory, "osiop",
 1192| 	    devinit->addr, DEV_OSIOP_LENGTH,
 1193| 	    dev_osiop_access, d, DM_DEFAULT, NULL);
 1194| 
 1195| 	machine_add_tickfunction(devinit->machine,
 1196| 	    dev_osiop_tick, d, OSIOP_TICK_SHIFT);
 1197| 
 1198| 	return 1;
 1199| }
 1200| 
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

End with one line: `FIXDRAFT_OSIOPWIDELANES: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
APPLY FAILED: FAIL /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/gweb/jobs_20261106_kits/fix_osiopwidelanes//reply.txt: 0 json blocks
```

The previous edits:

```json
(no edit block was returned)
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
