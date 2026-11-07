# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `pckbcselftest` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `pckbcselftest`, state `open`)

**title:** devices/dev_pckbc.c controller 0xA9 / 0xAA and keyboard 0xFF -- 0xA9 queues no reply and self-test/reset do not flush the output queues -- WRONG-RESULT (guest polls to timeout)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T54 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-13).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9bda09a28df39f3208c0577c05723b8e254b7252, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/ca2377fa6c8c1c81eb0df9c578a9461ea08c0a2b, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/c861ff6d1909a97715eddf7d30b8d8cabd352519.  Our site at de8c7547: src/devices/dev_pckbc.c:1056-1061, :883-900.  Portable fix: yes -- port rs6000 9bda09a, rs6000 ca2377f, rs6000 c861ff6 (not the IBM-specific extra 0xB2).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_pckbc.c` -- AT HEAD, lines 946-1194 (`*` marks a line your previous draft changed)

```c
  946|  {
  947|  static int x = 0;
  948|  x++;
  949|  if (x&1)
  950|  			odata ^= 0x10;
  951|  }
  952|  			if (writeflag == MEM_READ)
  953|  				memory_writemax64(cpu, data, len, odata);
  954|  			return 1;
  955|  		}
  956|  		if (relative_addr != 0)
  957|  			relative_addr = 1;
  958|  	} else {
  959|  		/*  Others... Non-Jazz ARC-based machines etc.  */
  960|  		if (relative_addr != 0)
  961|  			relative_addr = 1;
  962|  	}
  963|  
  964|  	switch (relative_addr) {
  965|  
  966|  	/*
  967|  	 *  8042 (PC):
  968|  	 */
  969|  
  970|  	case 0:		/*  data  */
  971|  		if (writeflag==MEM_READ) {
  972|  			switch (d->state[port_nr]) {
  973|  			case STATE_RDCMDBYTE:
  974|  				odata = d->cmdbyte;
  975|  				d->state[port_nr] = STATE_NORMAL;
  976|  				break;
  977|  			case STATE_RDOUTPUT:
  978|  				odata = d->output_byte;
  979|  				d->state[port_nr] = STATE_NORMAL;
  980|  				break;
  981|  			default:if (d->head[0] != d->tail[0]) {
  982|  					odata = pckbc_get_code(d, 0);
  983|  					d->last_scancode = odata;
  984|  				} else {
  985|  					odata = d->last_scancode;
  986|  					d->last_scancode |= 0x80;
  987|  				}
  988|  			}
  989|  			/*  debug("[ pckbc: read from DATA: 0x%02x ]\n",
  990|  			    (int)odata);  */
  991|  		} else {
  992|  			if (port_nr == 1) {
  993|  				fatal("[ pckbc: write to DATA:");
  994|  				for (i=0; i<len; i++)
  995|  					fatal(" %02x", data[i]);
  996|  				fatal(" ]\n");
  997|  			}
  998|  			
  999|  			switch (d->state[port_nr]) {
 1000|  			case STATE_LDCMDBYTE:
 1001|  				d->cmdbyte = idata;
 1002|  				d->rx_int_enable[port_nr] = d->cmdbyte &
 1003|  				    (KC8_KENABLE | KC8_MENABLE) ? 1 : 0;
 1004|  				d->state[port_nr] = STATE_NORMAL;
 1005|  				break;
 1006|  			case STATE_LDOUTPUT:
 1007|  				d->output_byte = idata;
 1008|  				d->state[port_nr] = STATE_NORMAL;
 1009|  				break;
 1010|  			default:d->reg[relative_addr] = idata;
 1011|  				dev_pckbc_command(d, port_nr);
 1012|  			}
 1013|  		}
 1014|  		break;
 1015|  	case 1:		/*  control  */
 1016|  		if (writeflag==MEM_READ) {
 1017|  			odata = 0;
 1018|  
 1019|  			/*  "Data in buffer" bit  */
 1020|  			if (d->head[0] != d->tail[0] ||
 1021|  			    d->state[port_nr] == STATE_RDCMDBYTE ||
 1022|  			    d->state[port_nr] == STATE_RDOUTPUT)
 1023|  				odata |= KBS_DIB;
 1024|  
 1025|  			if (d->state[port_nr] == STATE_RDCMDBYTE)
 1026|  				odata |= KBS_OCMD;
 1027|  
 1028|  			odata |= KBS_NOSEC;
 1029|  			/*  debug("[ pckbc: read from CTL status port: "
 1030|  			    "0x%02x ]\n", (int)odata);  */
 1031|  		} else {
 1032|  			debug("[ pckbc: write to CTL:");
 1033|  			for (i=0; i<len; i++)
 1034|  				debug(" %02x", data[i]);
 1035|  			debug(" ]\n");
 1036|  			d->reg[relative_addr] = idata;
 1037|  
 1038|  			switch (idata) {
 1039|  			case 0x10:
 1040|  			case 0x11:
 1041|  				/*  TODO: For now, don't print warnings about
 1042|  				    these. NetBSD sends these.  */
 1043|  				break;
 1044|  			case K_RDCMDBYTE:
 1045|  				d->state[port_nr] = STATE_RDCMDBYTE;
 1046|  				break;
 1047|  			case K_LDCMDBYTE:
 1048|  				d->state[port_nr] = STATE_LDCMDBYTE;
 1049|  				break;
 1050|  			case 0xa7:
 1051|  				d->cmdbyte |= KC8_MDISABLE;
 1052|  				break;
 1053|  			case 0xa8:
 1054|  				d->cmdbyte &= ~KC8_MDISABLE;
 1055|  				break;
 1056|  			case 0xa9:	/*  test auxiliary port  */
 1057|* 				debug("[ pckbc: CONTROL 0xa9, TODO ]\n");
 1058|* 				break;
 1059|  			case 0xaa:	/*  keyboard self-test  */
 1060|* 				pckbc_add_code(d, 0x55, port_nr);
 1061|  				break;
 1062|  			case 0xab:	/*  keyboard interface self-test  */
 1063|  				pckbc_add_code(d, 0x00, port_nr);
 1064|  				break;
 1065|  			case 0xad:
 1066|  				d->cmdbyte |= KC8_KDISABLE;
 1067|  				break;
 1068|  			case 0xae:
 1069|  				d->cmdbyte &= ~KC8_KDISABLE;
 1070|  				break;
 1071|  			case 0xd0:
 1072|  				d->state[port_nr] = STATE_RDOUTPUT;
 1073|  				break;
 1074|  			case 0xd1:
 1075|  				d->state[port_nr] = STATE_LDOUTPUT;
 1076|  				break;
 1077|  			case 0xd3:	/*  write to auxiliary device
 1078|  					    output buffer  */
 1079|  				debug("[ pckbc: CONTROL 0xd3, TODO ]\n");
 1080|  				d->state[port_nr] = STATE_WAITING_FOR_AUX_OUT;
 1081|  				break;
 1082|  			case 0xd4:	/*  write to auxiliary port  */
 1083|  				debug("[ pckbc: CONTROL 0xd4, TODO ]\n");
 1084|  				d->state[port_nr] = STATE_WAITING_FOR_AUX;
 1085|  				break;
 1086|  			default:
 1087|  				fatal("[ pckbc: unknown CONTROL 0x%x ]\n",
 1088|  				    (int)idata);
 1089|  				d->state[port_nr] = STATE_NORMAL;
 1090|  			}
 1091|  		}
 1092|  		break;
 1093|  
 1094|  	/*
 1095|  	 *  8242 (PS2):
 1096|  	 */
 1097|  
 1098|  	case PS2 + PS2_TXBUF:
 1099|  		if (writeflag==MEM_READ) {
 1100|  			odata = random() & 0xff;
 1101|  			debug("[ pckbc: read from port %i, PS2_TXBUF: "
 1102|  			    "0x%x ]\n", port_nr, (int)odata);
 1103|  		} else {
 1104|  			debug("[ pckbc: write to port %i, PS2_TXBUF: "
 1105|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1106|  
 1107|  			/*  Handle keyboard commands:  */
 1108|  			d->reg[PS2_TXBUF] = idata;
 1109|  			dev_pckbc_command(d, port_nr);
 1110|  		}
 1111|  		break;
 1112|  
 1113|  	case PS2 + PS2_RXBUF:
 1114|  		if (writeflag==MEM_READ) {
 1115|  			/*  TODO: What should be returned if no data 
 1116|  			    is available?  */
 1117|  			odata = 0;
 1118|  			if (d->head[port_nr] != d->tail[port_nr])
 1119|  				odata = pckbc_get_code(d, port_nr);
 1120|  			debug("[ pckbc: read from port %i, PS2_RXBUF: "
 1121|  			    "0x%02x ]\n", port_nr, (int)odata);
 1122|  		} else {
 1123|  			debug("[ pckbc: write to port %i, PS2_RXBUF: "
 1124|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1125|  		}
 1126|  		break;
 1127|  
 1128|  	case PS2 + PS2_CONTROL:
 1129|  		if (writeflag==MEM_READ) {
 1130|  			debug("[ pckbc: read from port %i, PS2_CONTROL"
 1131|  			    " ]\n", port_nr);
 1132|  		} else {
 1133|  			debug("[ pckbc: write to port %i, PS2_CONTROL:"
 1134|  			    " 0x%llx ]\n", port_nr, (long long)idata);
 1135|  			d->clocksignal = (idata & 0x10) ? 1 : 0;
 1136|  			d->rx_int_enable[port_nr] = (idata & PS2_CONTROL_RXINTEN) ? 1 : 0;
 1137|  			d->tx_int_enable[port_nr] = (idata & PS2_CONTROL_TXINTEN) ? 1 : 0;
 1138|  
 1139|  			// HACK/TODO: NetBSD/sgimips' X11 seems to work when
 1140|  			// interrupts are enabled, but it seems to not turn
 1141|  			// them on. Having this here makes it work, but it not
 1142|  			// the correct solution.
 1143|  			if (port_nr == 1) {
 1144|  				d->rx_int_enable[port_nr] = 1;
 1145|  			}
 1146|  		}
 1147|  		break;
 1148|  
 1149|  	case PS2 + PS2_STATUS:
 1150|  		if (writeflag==MEM_READ) {
 1151|  			odata = d->clocksignal + PS2_STATUS_TXEMPTY;
 1152|  
 1153|  			if (d->head[port_nr] != d->tail[port_nr]) {
 1154|  				/*  receiced data available  */
 1155|  				odata |= PS2_STATUS_RXFULL;
 1156|  			}
 1157|  
 1158|  			//debug("[ pckbc: read from port %i, PS2_STATUS: "
 1159|  			//    "0x%llx ]\n", port_nr, (long long)odata);
 1160|  		} else {
 1161|  			debug("[ pckbc: write to port %i, PS2_STATUS: "
 1162|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1163|  		}
 1164|  		break;
 1165|  
 1166|  	default:
 1167|  		if (writeflag==MEM_READ) {
 1168|  			debug("[ pckbc: read from unimplemented reg %i ]\n",
 1169|  			    (int)relative_addr);
 1170|  			odata = d->reg[relative_addr % DEV_PCKBC_LENGTH];
 1171|  		} else {
 1172|  			debug("[ pckbc: write to unimplemented reg %i:",
 1173|  			    (int)relative_addr);
 1174|  			for (i=0; i<len; i++)
 1175|  				debug(" %02x", data[i]);
 1176|  			debug(" ]\n");
 1177|  			d->reg[relative_addr % DEV_PCKBC_LENGTH] = idata;
 1178|  		}
 1179|  	}
 1180|  
 1181|  	/*  SGI? TODO: fix  */
 1182|  #if 0
 1183|  	if (len == 8)
 1184|  		odata |= (odata << 8) | (odata << 16) | (odata << 24) |
 1185|  		    (odata << 32) | (odata << 40) | (odata << 48) |
 1186|  		    (odata << 56);
 1187|  #endif
 1188|  	if (writeflag == MEM_READ)
 1189|  		memory_writemax64(cpu, data, len, odata);
 1190|  
 1191|  	pckbc_reassert_interrupts(d);
 1192|  
 1193|  	return 1;
 1194|  }
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


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_pckbc.c",
    "old": "\t\t\tcase 0xa9:\t/*  test auxiliary port  */\n\t\t\t\tdebug(\"[ pckbc: CONTROL 0xa9, TODO ]\\n\");\n\t\t\t\tbreak;\n\t\t\tcase 0xaa:\t/*  keyboard self-test  */\n\t\t\t\tpckbc_add_code(d, 0x55, port_nr);\n\t\t\t\tbreak;",
    "new": "\t\t\tcase 0xa9:\t/*  test auxiliary port  */\n\t\t\t\t/* #T54: flush aux queue, return success 0x00 */\n\t\t\t\td->head[1] = d->tail[1] = 0;\n\t\t\t\tpckbc_add_code(d, 0x00, port_nr);\n\t\t\t\tbreak;\n\t\t\tcase 0xaa:\t/*  keyboard self-test  */\n\t\t\t\t/* #T54: flush all output queues */\n\t\t\t\td->head[0] = d->tail[0] = 0;\n\t\t\t\td->head[1] = d->tail[1] = 0;\n\t\t\t\tpckbc_add_code(d, 0x55, port_nr);\n\t\t\t\tbreak;",
    "why": "0xA9 now flushes the auxiliary port output queue and queues a 0x00 success reply; 0xAA now flushes all output queues before queueing its 0x55 success reply."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_PCKBCSELFTEST: DEFECT, 2 FINDINGS
1. The diff removes the defect at `dev_pckbc.c:1056-1061` (for 0xA9 and 0xAA), but it misses the site `dev_pckbc.c:883-900` mentioned in the issue for the keyboard 0xFF self-test.
2. CONTROL FLOW: No added `return`, `goto`, or `break` skips the common tail. The added code falls through to the existing `break;` statements and proceeds to the function's tail (`pckbc_reassert_interrupts(d); return 1;`).
3. RETURN VALUE: No path returns something different. The function continues to return `1` on these paths, which indicates successful handling of the memory write.
4. What ELSE does the diff change: It removes the `debug("[ pckbc: CONTROL 0xa9, TODO ]\n");` log message that previously printed when 0xA9 was received. It now silently processes 0xA9.
5. House idioms: The new comments correctly use the `/* #T54: ... */` tag, and line lengths are within limits.
`src/devices/dev_pckbc.c:883`: DEFECT: The keyboard 0xFF self-test is missing from the diff; apply flush logic to that site as well.
`src/devices/dev_pckbc.c:1057`: QUESTION: The 0xA9 case removed the debug statement instead of preserving it; is it intentional to silence it completely?
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_PCKBCSELFTEST: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_PCKBCSELFTEST: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
