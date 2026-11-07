# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pckbcselftest` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pckbcselftest`, state `open`, severity `MED`)

**title:** devices/dev_pckbc.c controller 0xA9 / 0xAA and keyboard 0xFF -- 0xA9 queues no reply and self-test/reset do not flush the output queues -- WRONG-RESULT (guest polls to timeout)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T54 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-13).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9bda09a28df39f3208c0577c05723b8e254b7252, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/ca2377fa6c8c1c81eb0df9c578a9461ea08c0a2b, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/c861ff6d1909a97715eddf7d30b8d8cabd352519.  Our site at de8c7547: src/devices/dev_pckbc.c:1056-1061, :883-900.  Portable fix: yes -- port rs6000 9bda09a, rs6000 ca2377f, rs6000 c861ff6 (not the IBM-specific extra 0xB2).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 9bda09a, rs6000 ca2377f, rs6000 c861ff6 (not the IBM-specific extra 0xB2)

## The code at the cited lines

### `src/devices/dev_pckbc.c` around the row's cited line 1056 (HEAD d2a6f233, lines 1011-1101)

```c
 1011| 				dev_pckbc_command(d, port_nr);
 1012| 			}
 1013| 		}
 1014| 		break;
 1015| 	case 1:		/*  control  */
 1016| 		if (writeflag==MEM_READ) {
 1017| 			odata = 0;
 1018| 
 1019| 			/*  "Data in buffer" bit  */
 1020| 			if (d->head[0] != d->tail[0] ||
 1021| 			    d->state[port_nr] == STATE_RDCMDBYTE ||
 1022| 			    d->state[port_nr] == STATE_RDOUTPUT)
 1023| 				odata |= KBS_DIB;
 1024| 
 1025| 			if (d->state[port_nr] == STATE_RDCMDBYTE)
 1026| 				odata |= KBS_OCMD;
 1027| 
 1028| 			odata |= KBS_NOSEC;
 1029| 			/*  debug("[ pckbc: read from CTL status port: "
 1030| 			    "0x%02x ]\n", (int)odata);  */
 1031| 		} else {
 1032| 			debug("[ pckbc: write to CTL:");
 1033| 			for (i=0; i<len; i++)
 1034| 				debug(" %02x", data[i]);
 1035| 			debug(" ]\n");
 1036| 			d->reg[relative_addr] = idata;
 1037| 
 1038| 			switch (idata) {
 1039| 			case 0x10:
 1040| 			case 0x11:
 1041| 				/*  TODO: For now, don't print warnings about
 1042| 				    these. NetBSD sends these.  */
 1043| 				break;
 1044| 			case K_RDCMDBYTE:
 1045| 				d->state[port_nr] = STATE_RDCMDBYTE;
 1046| 				break;
 1047| 			case K_LDCMDBYTE:
 1048| 				d->state[port_nr] = STATE_LDCMDBYTE;
 1049| 				break;
 1050| 			case 0xa7:
 1051| 				d->cmdbyte |= KC8_MDISABLE;
 1052| 				break;
 1053| 			case 0xa8:
 1054| 				d->cmdbyte &= ~KC8_MDISABLE;
 1055| 				break;
 1056| 			case 0xa9:	/*  test auxiliary port  */
 1057| 				debug("[ pckbc: CONTROL 0xa9, TODO ]\n");
 1058| 				break;
 1059| 			case 0xaa:	/*  keyboard self-test  */
 1060| 				pckbc_add_code(d, 0x55, port_nr);
 1061| 				break;
 1062| 			case 0xab:	/*  keyboard interface self-test  */
 1063| 				pckbc_add_code(d, 0x00, port_nr);
 1064| 				break;
 1065| 			case 0xad:
 1066| 				d->cmdbyte |= KC8_KDISABLE;
 1067| 				break;
 1068| 			case 0xae:
 1069| 				d->cmdbyte &= ~KC8_KDISABLE;
 1070| 				break;
 1071| 			case 0xd0:
 1072| 				d->state[port_nr] = STATE_RDOUTPUT;
 1073| 				break;
 1074| 			case 0xd1:
 1075| 				d->state[port_nr] = STATE_LDOUTPUT;
 1076| 				break;
 1077| 			case 0xd3:	/*  write to auxiliary device
 1078| 					    output buffer  */
 1079| 				debug("[ pckbc: CONTROL 0xd3, TODO ]\n");
 1080| 				d->state[port_nr] = STATE_WAITING_FOR_AUX_OUT;
 1081| 				break;
 1082| 			case 0xd4:	/*  write to auxiliary port  */
 1083| 				debug("[ pckbc: CONTROL 0xd4, TODO ]\n");
 1084| 				d->state[port_nr] = STATE_WAITING_FOR_AUX;
 1085| 				break;
 1086| 			default:
 1087| 				fatal("[ pckbc: unknown CONTROL 0x%x ]\n",
 1088| 				    (int)idata);
 1089| 				d->state[port_nr] = STATE_NORMAL;
 1090| 			}
 1091| 		}
 1092| 		break;
 1093| 
 1094| 	/*
 1095| 	 *  8242 (PS2):
 1096| 	 */
 1097| 
 1098| 	case PS2 + PS2_TXBUF:
 1099| 		if (writeflag==MEM_READ) {
 1100| 			odata = random() & 0xff;
 1101| 			debug("[ pckbc: read from port %i, PS2_TXBUF: "
```

## The data structures those files define (every field that exists)

### `src/devices/dev_pckbc.c` -- `struct pckbc_data {` (HEAD lines 82-111)

```c
   82| struct pckbc_data {
   83| 	int		console_handle;
   84| 	int		in_use;
   85| 
   86| 	int		reg[DEV_PCKBC_LENGTH];
   87| 
   88| 	struct interrupt irq_keyboard;
   89| 	struct interrupt irq_mouse;
   90| 	int		currently_asserted[2];
   91| 	int		type;
   92| 	int		pc_style_flag;
   93| 
   94| 	/*  TODO: one of these for each port?  */
   95| 	int		clocksignal;
   96| 	int		rx_int_enable[2];
   97| 	int		tx_int_enable[2];
   98| 
   99| 	int		scanning_enabled[2];
  100| 	int		translation_table;
  101| 	int		state[2];
  102| 	int		cmdbyte;
  103| 	int		output_byte;
  104| 	int		last_scancode;
  105| 
  106| 	unsigned	key_queue[2][MAX_8042_QUEUELEN];
  107| 	int		head[2], tail[2];
  108| 	int		overrun_warned[2];	/*  #288  */
  109| 
  110| 	int		mouse_buttons;
  111| };
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

End with one line: `FIXDRAFT_PCKBCSELFTEST: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
