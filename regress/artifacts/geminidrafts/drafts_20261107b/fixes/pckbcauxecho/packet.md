# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pckbcauxecho` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pckbcauxecho`, state `open`, severity `MED`)

**title:** devices/dev_pckbc.c 0xD4/0xD3 -- a byte written to the aux device is echoed into the keyboard stream -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T55 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-15).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d2ff00eb9d9dc8e8b660672c9a155a8131cb2b20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/94e3ed46472d2c17ffb5eaa2d58aa5ce7b1dae5a.  Our site at de8c7547: src/devices/dev_pckbc.c:1077-1085, :792-807.  Portable fix: yes -- port routing part of rs6000 d2ff00e, rs6000 94e3ed4.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port routing part of rs6000 d2ff00e, rs6000 94e3ed4

## The code at the cited lines

### `src/devices/dev_pckbc.c` around the row's cited line 1077 (HEAD 8d9df658, lines 957-1197)

```c
  957| 			relative_addr = 1;
  958| 	} else {
  959| 		/*  Others... Non-Jazz ARC-based machines etc.  */
  960| 		if (relative_addr != 0)
  961| 			relative_addr = 1;
  962| 	}
  963| 
  964| 	switch (relative_addr) {
  965| 
  966| 	/*
  967| 	 *  8042 (PC):
  968| 	 */
  969| 
  970| 	case 0:		/*  data  */
  971| 		if (writeflag==MEM_READ) {
  972| 			switch (d->state[port_nr]) {
  973| 			case STATE_RDCMDBYTE:
  974| 				odata = d->cmdbyte;
  975| 				d->state[port_nr] = STATE_NORMAL;
  976| 				break;
  977| 			case STATE_RDOUTPUT:
  978| 				odata = d->output_byte;
  979| 				d->state[port_nr] = STATE_NORMAL;
  980| 				break;
  981| 			default:if (d->head[0] != d->tail[0]) {
  982| 					odata = pckbc_get_code(d, 0);
  983| 					d->last_scancode = odata;
  984| 				} else {
  985| 					odata = d->last_scancode;
  986| 					d->last_scancode |= 0x80;
  987| 				}
  988| 			}
  989| 			/*  debug("[ pckbc: read from DATA: 0x%02x ]\n",
  990| 			    (int)odata);  */
  991| 		} else {
  992| 			if (port_nr == 1) {
  993| 				fatal("[ pckbc: write to DATA:");
  994| 				for (i=0; i<len; i++)
  995| 					fatal(" %02x", data[i]);
  996| 				fatal(" ]\n");
  997| 			}
  998| 			
  999| 			switch (d->state[port_nr]) {
 1000| 			case STATE_LDCMDBYTE:
 1001| 				d->cmdbyte = idata;
 1002| 				d->rx_int_enable[port_nr] = d->cmdbyte &
 1003| 				    (KC8_KENABLE | KC8_MENABLE) ? 1 : 0;
 1004| 				d->state[port_nr] = STATE_NORMAL;
 1005| 				break;
 1006| 			case STATE_LDOUTPUT:
 1007| 				d->output_byte = idata;
 1008| 				d->state[port_nr] = STATE_NORMAL;
 1009| 				break;
 1010| 			default:d->reg[relative_addr] = idata;
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
 1102| 			    "0x%x ]\n", port_nr, (int)odata);
 1103| 		} else {
 1104| 			debug("[ pckbc: write to port %i, PS2_TXBUF: "
 1105| 			    "0x%llx ]\n", port_nr, (long long)idata);
 1106| 
 1107| 			/*  Handle keyboard commands:  */
 1108| 			d->reg[PS2_TXBUF] = idata;
 1109| 			dev_pckbc_command(d, port_nr);
 1110| 		}
 1111| 		break;
 1112| 
 1113| 	case PS2 + PS2_RXBUF:
 1114| 		if (writeflag==MEM_READ) {
 1115| 			/*  TODO: What should be returned if no data 
 1116| 			    is available?  */
 1117| 			odata = 0;
 1118| 			if (d->head[port_nr] != d->tail[port_nr])
 1119| 				odata = pckbc_get_code(d, port_nr);
 1120| 			debug("[ pckbc: read from port %i, PS2_RXBUF: "
 1121| 			    "0x%02x ]\n", port_nr, (int)odata);
 1122| 		} else {
 1123| 			debug("[ pckbc: write to port %i, PS2_RXBUF: "
 1124| 			    "0x%llx ]\n", port_nr, (long long)idata);
 1125| 		}
 1126| 		break;
 1127| 
 1128| 	case PS2 + PS2_CONTROL:
 1129| 		if (writeflag==MEM_READ) {
 1130| 			debug("[ pckbc: read from port %i, PS2_CONTROL"
 1131| 			    " ]\n", port_nr);
 1132| 		} else {
 1133| 			debug("[ pckbc: write to port %i, PS2_CONTROL:"
 1134| 			    " 0x%llx ]\n", port_nr, (long long)idata);
 1135| 			d->clocksignal = (idata & 0x10) ? 1 : 0;
 1136| 			d->rx_int_enable[port_nr] = (idata & PS2_CONTROL_RXINTEN) ? 1 : 0;
 1137| 			d->tx_int_enable[port_nr] = (idata & PS2_CONTROL_TXINTEN) ? 1 : 0;
 1138| 
 1139| 			// HACK/TODO: NetBSD/sgimips' X11 seems to work when
 1140| 			// interrupts are enabled, but it seems to not turn
 1141| 			// them on. Having this here makes it work, but it not
 1142| 			// the correct solution.
 1143| 			if (port_nr == 1) {
 1144| 				d->rx_int_enable[port_nr] = 1;
 1145| 			}
 1146| 		}
 1147| 		break;
 1148| 
 1149| 	case PS2 + PS2_STATUS:
 1150| 		if (writeflag==MEM_READ) {
 1151| 			odata = d->clocksignal + PS2_STATUS_TXEMPTY;
 1152| 
 1153| 			if (d->head[port_nr] != d->tail[port_nr]) {
 1154| 				/*  receiced data available  */
 1155| 				odata |= PS2_STATUS_RXFULL;
 1156| 			}
 1157| 
 1158| 			//debug("[ pckbc: read from port %i, PS2_STATUS: "
 1159| 			//    "0x%llx ]\n", port_nr, (long long)odata);
 1160| 		} else {
 1161| 			debug("[ pckbc: write to port %i, PS2_STATUS: "
 1162| 			    "0x%llx ]\n", port_nr, (long long)idata);
 1163| 		}
 1164| 		break;
 1165| 
 1166| 	default:
 1167| 		if (writeflag==MEM_READ) {
 1168| 			debug("[ pckbc: read from unimplemented reg %i ]\n",
 1169| 			    (int)relative_addr);
 1170| 			odata = d->reg[relative_addr % DEV_PCKBC_LENGTH];
 1171| 		} else {
 1172| 			debug("[ pckbc: write to unimplemented reg %i:",
 1173| 			    (int)relative_addr);
 1174| 			for (i=0; i<len; i++)
 1175| 				debug(" %02x", data[i]);
 1176| 			debug(" ]\n");
 1177| 			d->reg[relative_addr % DEV_PCKBC_LENGTH] = idata;
 1178| 		}
 1179| 	}
 1180| 
 1181| 	/*  SGI? TODO: fix  */
 1182| #if 0
 1183| 	if (len == 8)
 1184| 		odata |= (odata << 8) | (odata << 16) | (odata << 24) |
 1185| 		    (odata << 32) | (odata << 40) | (odata << 48) |
 1186| 		    (odata << 56);
 1187| #endif
 1188| 	if (writeflag == MEM_READ)
 1189| 		memory_writemax64(cpu, data, len, odata);
 1190| 
 1191| 	pckbc_reassert_interrupts(d);
 1192| 
 1193| 	return 1;
 1194| }
 1195| 
 1196| 
 1197| /*
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

End with one line: `FIXDRAFT_PCKBCAUXECHO: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
