# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pckbcauxecho` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pckbcauxecho`, state `open`)

**title:** devices/dev_pckbc.c 0xD4/0xD3 -- a byte written to the aux device is echoed into the keyboard stream -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T55 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-15).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/d2ff00eb9d9dc8e8b660672c9a155a8131cb2b20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/94e3ed46472d2c17ffb5eaa2d58aa5ce7b1dae5a.  Our site at de8c7547: src/devices/dev_pckbc.c:1077-1085, :792-807.  Portable fix: yes -- port routing part of rs6000 d2ff00e, rs6000 94e3ed4.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 1010| default:d->reg[relative_addr] = idata; dev_pckbc_command(d, port_nr);

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pckbc.c b/src/devices/dev_pckbc.c
index fd2cde1a..4de2f1b9 100644
--- a/src/devices/dev_pckbc.c
+++ b/src/devices/dev_pckbc.c
@@ -1007,6 +1007,12 @@ if (x&1)
 				d->output_byte = idata;
 				d->state[port_nr] = STATE_NORMAL;
 				break;
+			case STATE_WAITING_FOR_AUX:
+			case STATE_WAITING_FOR_AUX_OUT:
+				d->reg[relative_addr] = idata;
+				dev_pckbc_command(d, 1);
+				d->state[port_nr] = STATE_NORMAL;
+				break;
 			default:d->reg[relative_addr] = idata;
 				dev_pckbc_command(d, port_nr);
 			}
```

## Every edited function, after the fix

### `src/devices/dev_pckbc.c` -- post-edit lines 946-1200 (`+` marks a line the diff added or the point of a deletion)

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
 1010|+ 			case STATE_WAITING_FOR_AUX:
 1011|+ 			case STATE_WAITING_FOR_AUX_OUT:
 1012|+ 				d->reg[relative_addr] = idata;
 1013|+ 				dev_pckbc_command(d, 1);
 1014|+ 				d->state[port_nr] = STATE_NORMAL;
 1015|+ 				break;
 1016|  			default:d->reg[relative_addr] = idata;
 1017|  				dev_pckbc_command(d, port_nr);
 1018|  			}
 1019|  		}
 1020|  		break;
 1021|  	case 1:		/*  control  */
 1022|  		if (writeflag==MEM_READ) {
 1023|  			odata = 0;
 1024|  
 1025|  			/*  "Data in buffer" bit  */
 1026|  			if (d->head[0] != d->tail[0] ||
 1027|  			    d->state[port_nr] == STATE_RDCMDBYTE ||
 1028|  			    d->state[port_nr] == STATE_RDOUTPUT)
 1029|  				odata |= KBS_DIB;
 1030|  
 1031|  			if (d->state[port_nr] == STATE_RDCMDBYTE)
 1032|  				odata |= KBS_OCMD;
 1033|  
 1034|  			odata |= KBS_NOSEC;
 1035|  			/*  debug("[ pckbc: read from CTL status port: "
 1036|  			    "0x%02x ]\n", (int)odata);  */
 1037|  		} else {
 1038|  			debug("[ pckbc: write to CTL:");
 1039|  			for (i=0; i<len; i++)
 1040|  				debug(" %02x", data[i]);
 1041|  			debug(" ]\n");
 1042|  			d->reg[relative_addr] = idata;
 1043|  
 1044|  			switch (idata) {
 1045|  			case 0x10:
 1046|  			case 0x11:
 1047|  				/*  TODO: For now, don't print warnings about
 1048|  				    these. NetBSD sends these.  */
 1049|  				break;
 1050|  			case K_RDCMDBYTE:
 1051|  				d->state[port_nr] = STATE_RDCMDBYTE;
 1052|  				break;
 1053|  			case K_LDCMDBYTE:
 1054|  				d->state[port_nr] = STATE_LDCMDBYTE;
 1055|  				break;
 1056|  			case 0xa7:
 1057|  				d->cmdbyte |= KC8_MDISABLE;
 1058|  				break;
 1059|  			case 0xa8:
 1060|  				d->cmdbyte &= ~KC8_MDISABLE;
 1061|  				break;
 1062|  			case 0xa9:	/*  test auxiliary port  */
 1063|  				debug("[ pckbc: CONTROL 0xa9, TODO ]\n");
 1064|  				break;
 1065|  			case 0xaa:	/*  keyboard self-test  */
 1066|  				pckbc_add_code(d, 0x55, port_nr);
 1067|  				break;
 1068|  			case 0xab:	/*  keyboard interface self-test  */
 1069|  				pckbc_add_code(d, 0x00, port_nr);
 1070|  				break;
 1071|  			case 0xad:
 1072|  				d->cmdbyte |= KC8_KDISABLE;
 1073|  				break;
 1074|  			case 0xae:
 1075|  				d->cmdbyte &= ~KC8_KDISABLE;
 1076|  				break;
 1077|  			case 0xd0:
 1078|  				d->state[port_nr] = STATE_RDOUTPUT;
 1079|  				break;
 1080|  			case 0xd1:
 1081|  				d->state[port_nr] = STATE_LDOUTPUT;
 1082|  				break;
 1083|  			case 0xd3:	/*  write to auxiliary device
 1084|  					    output buffer  */
 1085|  				debug("[ pckbc: CONTROL 0xd3, TODO ]\n");
 1086|  				d->state[port_nr] = STATE_WAITING_FOR_AUX_OUT;
 1087|  				break;
 1088|  			case 0xd4:	/*  write to auxiliary port  */
 1089|  				debug("[ pckbc: CONTROL 0xd4, TODO ]\n");
 1090|  				d->state[port_nr] = STATE_WAITING_FOR_AUX;
 1091|  				break;
 1092|  			default:
 1093|  				fatal("[ pckbc: unknown CONTROL 0x%x ]\n",
 1094|  				    (int)idata);
 1095|  				d->state[port_nr] = STATE_NORMAL;
 1096|  			}
 1097|  		}
 1098|  		break;
 1099|  
 1100|  	/*
 1101|  	 *  8242 (PS2):
 1102|  	 */
 1103|  
 1104|  	case PS2 + PS2_TXBUF:
 1105|  		if (writeflag==MEM_READ) {
 1106|  			odata = random() & 0xff;
 1107|  			debug("[ pckbc: read from port %i, PS2_TXBUF: "
 1108|  			    "0x%x ]\n", port_nr, (int)odata);
 1109|  		} else {
 1110|  			debug("[ pckbc: write to port %i, PS2_TXBUF: "
 1111|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1112|  
 1113|  			/*  Handle keyboard commands:  */
 1114|  			d->reg[PS2_TXBUF] = idata;
 1115|  			dev_pckbc_command(d, port_nr);
 1116|  		}
 1117|  		break;
 1118|  
 1119|  	case PS2 + PS2_RXBUF:
 1120|  		if (writeflag==MEM_READ) {
 1121|  			/*  TODO: What should be returned if no data 
 1122|  			    is available?  */
 1123|  			odata = 0;
 1124|  			if (d->head[port_nr] != d->tail[port_nr])
 1125|  				odata = pckbc_get_code(d, port_nr);
 1126|  			debug("[ pckbc: read from port %i, PS2_RXBUF: "
 1127|  			    "0x%02x ]\n", port_nr, (int)odata);
 1128|  		} else {
 1129|  			debug("[ pckbc: write to port %i, PS2_RXBUF: "
 1130|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1131|  		}
 1132|  		break;
 1133|  
 1134|  	case PS2 + PS2_CONTROL:
 1135|  		if (writeflag==MEM_READ) {
 1136|  			debug("[ pckbc: read from port %i, PS2_CONTROL"
 1137|  			    " ]\n", port_nr);
 1138|  		} else {
 1139|  			debug("[ pckbc: write to port %i, PS2_CONTROL:"
 1140|  			    " 0x%llx ]\n", port_nr, (long long)idata);
 1141|  			d->clocksignal = (idata & 0x10) ? 1 : 0;
 1142|  			d->rx_int_enable[port_nr] = (idata & PS2_CONTROL_RXINTEN) ? 1 : 0;
 1143|  			d->tx_int_enable[port_nr] = (idata & PS2_CONTROL_TXINTEN) ? 1 : 0;
 1144|  
 1145|  			// HACK/TODO: NetBSD/sgimips' X11 seems to work when
 1146|  			// interrupts are enabled, but it seems to not turn
 1147|  			// them on. Having this here makes it work, but it not
 1148|  			// the correct solution.
 1149|  			if (port_nr == 1) {
 1150|  				d->rx_int_enable[port_nr] = 1;
 1151|  			}
 1152|  		}
 1153|  		break;
 1154|  
 1155|  	case PS2 + PS2_STATUS:
 1156|  		if (writeflag==MEM_READ) {
 1157|  			odata = d->clocksignal + PS2_STATUS_TXEMPTY;
 1158|  
 1159|  			if (d->head[port_nr] != d->tail[port_nr]) {
 1160|  				/*  receiced data available  */
 1161|  				odata |= PS2_STATUS_RXFULL;
 1162|  			}
 1163|  
 1164|  			//debug("[ pckbc: read from port %i, PS2_STATUS: "
 1165|  			//    "0x%llx ]\n", port_nr, (long long)odata);
 1166|  		} else {
 1167|  			debug("[ pckbc: write to port %i, PS2_STATUS: "
 1168|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1169|  		}
 1170|  		break;
 1171|  
 1172|  	default:
 1173|  		if (writeflag==MEM_READ) {
 1174|  			debug("[ pckbc: read from unimplemented reg %i ]\n",
 1175|  			    (int)relative_addr);
 1176|  			odata = d->reg[relative_addr % DEV_PCKBC_LENGTH];
 1177|  		} else {
 1178|  			debug("[ pckbc: write to unimplemented reg %i:",
 1179|  			    (int)relative_addr);
 1180|  			for (i=0; i<len; i++)
 1181|  				debug(" %02x", data[i]);
 1182|  			debug(" ]\n");
 1183|  			d->reg[relative_addr % DEV_PCKBC_LENGTH] = idata;
 1184|  		}
 1185|  	}
 1186|  
 1187|  	/*  SGI? TODO: fix  */
 1188|  #if 0
 1189|  	if (len == 8)
 1190|  		odata |= (odata << 8) | (odata << 16) | (odata << 24) |
 1191|  		    (odata << 32) | (odata << 40) | (odata << 48) |
 1192|  		    (odata << 56);
 1193|  #endif
 1194|  	if (writeflag == MEM_READ)
 1195|  		memory_writemax64(cpu, data, len, odata);
 1196|  
 1197|  	pckbc_reassert_interrupts(d);
 1198|  
 1199|  	return 1;
 1200|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCKBCAUXECHO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PCKBCAUXECHO: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_PCKBCAUXECHO: UNSETTLED, 1 FINDINGS
1. Yes, the diff removes the defect. By intercepting `STATE_WAITING_FOR_AUX` and `STATE_WAITING_FOR_AUX_OUT` during a data write, it explicitly routes the byte to port 1 (the aux port) via `dev_pckbc_command(d, 1)` instead of allowing it to fall through to `dev_pckbc_command(d, port_nr)` (which echoes it to port 0, the keyboard).
2. CONTROL FLOW: No. The added `break;` correctly exits the inner `switch (d->state[port_nr])` block, allowing execution to naturally proceed to the common tail (starting at line 1194 with `if (writeflag == MEM_READ) memory_writemax64(...)` and line 1197 `pckbc_reassert_interrupts(d);`). It does not skip any required code.
3. RETURN VALUE: No. The patched code still completes the function and hits `return 1;` at line 1199, indicating a successfully handled memory access. 
4. What ELSE does the diff change: It explicitly resets the device state via `d->state[port_nr] = STATE_NORMAL;` (line 1014). The old code in the `default` case omitted this state reset, meaning a write in those states would have previously left the device permanently stuck waiting for aux data. 
5. House idioms: No style or idiom violations. The diff is concise and introduces no unformatted comments or excessively long lines.
FINDING 1: `src/devices/dev_pckbc.c:1013` - UNSETTLED - We cannot verify from this diff alone if `dev_pckbc_command(d, 1)` natively handles both `WAITING_FOR_AUX` (0xD4, a command *to* the mouse) and `WAITING_FOR_AUX_OUT` (0xD3, an injection directly into the host's receive buffer). We need to see the implementation of `dev_pckbc_command` to ensure 0xD3 does not erroneously get parsed as a mouse command.
```

### `src/devices/dev_pckbc.c` lines 111-127 (where HEAD defines `STATE_WAITING_FOR_AUX`)

```c
  111| };
  112| 
  113| #define	STATE_NORMAL			0
  114| #define	STATE_LDCMDBYTE			1
  115| #define	STATE_RDCMDBYTE			2
  116| #define	STATE_WAITING_FOR_TRANSLTABLE	3
  117| #define	STATE_WAITING_FOR_RATE		4
  118| #define	STATE_WAITING_FOR_ONEKEY_MB	5
  119| #define	STATE_WAITING_FOR_AUX		6
  120| #define	STATE_WAITING_FOR_AUX_OUT	7
  121| #define	STATE_LDOUTPUT			8
  122| #define	STATE_RDOUTPUT			9
  123| 
  124| 
  125| /*
  126|  *  pckbc_add_code():
  127|  *
```

### `src/devices/dev_pckbc.c` lines 112-128 (where HEAD defines `STATE_WAITING_FOR_AUX_OUT`)

```c
  112| 
  113| #define	STATE_NORMAL			0
  114| #define	STATE_LDCMDBYTE			1
  115| #define	STATE_RDCMDBYTE			2
  116| #define	STATE_WAITING_FOR_TRANSLTABLE	3
  117| #define	STATE_WAITING_FOR_RATE		4
  118| #define	STATE_WAITING_FOR_ONEKEY_MB	5
  119| #define	STATE_WAITING_FOR_AUX		6
  120| #define	STATE_WAITING_FOR_AUX_OUT	7
  121| #define	STATE_LDOUTPUT			8
  122| #define	STATE_RDOUTPUT			9
  123| 
  124| 
  125| /*
  126|  *  pckbc_add_code():
  127|  *
  128|  *  Adds a byte to the data queue.
```

### `src/devices/dev_pckbc.c` lines 727-743 (where HEAD defines `dev_pckbc_command`)

```c
  727| }
  728| 
  729| 
  730| /*
  731|  *  dev_pckbc_command():
  732|  *
  733|  *  Handle commands to the 8048 in the emulated keyboard.
  734|  */
  735| static void dev_pckbc_command(struct pckbc_data *d, int port_nr)
  736| {
  737| 	int cmd = d->type == PCKBC_8242 ? d->reg[PS2_TXBUF] : d->reg[PC_CMD];
  738| 
  739| #if 0
  740| 	// Mouse port debugging:
  741| 	if (port_nr == 1)
  742| 		fatal("[ pckbc: (port %i) command 0x%02x ]\n", port_nr, cmd);
  743| #endif
```

### `src/core/memory.c` lines 81-97 (where HEAD defines `memory_writemax64`)

```c
   81| /*
   82|  *  memory_writemax64():
   83|  *
   84|  *  Write at most 64 bits of data to a buffer.  Length is given by
   85|  *  len, and the byte order by cpu->byte_order.
   86|  *
   87|  *  This function should not be called with cpu == NULL.
   88|  */
   89| void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len,
   90| 	uint64_t data)
   91| {
   92| 	int i, byte_order = cpu->byte_order;
   93| 
   94| 	if (len & MEM_PCI_LITTLE_ENDIAN) {
   95| 		len &= ~MEM_PCI_LITTLE_ENDIAN;
   96| 		byte_order = EMUL_LITTLE_ENDIAN;
   97| 	}
```

### `src/include/memory.h` lines 92-108 (where HEAD defines `memory_writemax64`)

```c
   92| #define	BITS_PER_PAGETABLE	20
   93| #define	BITS_PER_MEMBLOCK	20
   94| #define	MAX_BITS		40
   95| 
   96| 
   97| /*  memory.c:  */
   98| #define	MEM_PCI_LITTLE_ENDIAN	128
   99| uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len);
  100| void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len,
  101| 	uint64_t data);
  102| 
  103| void *zeroed_alloc(size_t s);
  104| 
  105| struct memory *memory_new(uint64_t physical_max);
  106| 
  107| int memory_points_to_string(struct cpu *cpu, struct memory *mem,
  108| 	uint64_t addr, int min_string_length);
```

### `src/devices/dev_pckbc.c` lines 598-614 (where HEAD defines `pckbc_reassert_interrupts`)

```c
  598| 	}
  599| 	if (ctrl) {
  600| 		pckbc_add_code(d, 0xf0, p);
  601| 		pckbc_add_code(d, 0x11, p);
  602| 	}
  603| }
  604| 
  605| 
  606| void pckbc_reassert_interrupts(struct pckbc_data *d)
  607| {
  608| 	int ints_enabled = 1;
  609| 
  610| 	// if (d->cmdbyte & KC8_KDISABLE)
  611| 	//	ints_enabled = 0;
  612| 
  613| 	for (int port_nr = 0; port_nr < 2; port_nr++) {
  614| 		/*
```

### `src/devices/dev_pckbc.c` lines 105-121 (where HEAD defines `STATE_NORMAL`)

```c
  105| 
  106| 	unsigned	key_queue[2][MAX_8042_QUEUELEN];
  107| 	int		head[2], tail[2];
  108| 	int		overrun_warned[2];	/*  #288  */
  109| 
  110| 	int		mouse_buttons;
  111| };
  112| 
  113| #define	STATE_NORMAL			0
  114| #define	STATE_LDCMDBYTE			1
  115| #define	STATE_RDCMDBYTE			2
  116| #define	STATE_WAITING_FOR_TRANSLTABLE	3
  117| #define	STATE_WAITING_FOR_RATE		4
  118| #define	STATE_WAITING_FOR_ONEKEY_MB	5
  119| #define	STATE_WAITING_FOR_AUX		6
  120| #define	STATE_WAITING_FOR_AUX_OUT	7
  121| #define	STATE_LDOUTPUT			8
```

Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
