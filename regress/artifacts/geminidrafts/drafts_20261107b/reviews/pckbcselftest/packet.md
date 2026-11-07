# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `pckbcselftest` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `pckbcselftest`, state `open`)

**title:** devices/dev_pckbc.c controller 0xA9 / 0xAA and keyboard 0xFF -- 0xA9 queues no reply and self-test/reset do not flush the output queues -- WRONG-RESULT (guest polls to timeout)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T54 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-13).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9bda09a28df39f3208c0577c05723b8e254b7252, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/ca2377fa6c8c1c81eb0df9c578a9461ea08c0a2b, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/c861ff6d1909a97715eddf7d30b8d8cabd352519.  Our site at de8c7547: src/devices/dev_pckbc.c:1056-1061, :883-900.  Portable fix: yes -- port rs6000 9bda09a, rs6000 ca2377f, rs6000 c861ff6 (not the IBM-specific extra 0xB2).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_pckbc.c:1056-1061

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_pckbc.c b/src/devices/dev_pckbc.c
index fd2cde1a..542076d0 100644
--- a/src/devices/dev_pckbc.c
+++ b/src/devices/dev_pckbc.c
@@ -1054,9 +1054,14 @@ if (x&1)
 				d->cmdbyte &= ~KC8_MDISABLE;
 				break;
 			case 0xa9:	/*  test auxiliary port  */
-				debug("[ pckbc: CONTROL 0xa9, TODO ]\n");
+				/* #T54: flush aux queue, return success 0x00 */
+				d->head[1] = d->tail[1] = 0;
+				pckbc_add_code(d, 0x00, port_nr);
 				break;
 			case 0xaa:	/*  keyboard self-test  */
+				/* #T54: flush all output queues */
+				d->head[0] = d->tail[0] = 0;
+				d->head[1] = d->tail[1] = 0;
 				pckbc_add_code(d, 0x55, port_nr);
 				break;
 			case 0xab:	/*  keyboard interface self-test  */
```

## Every edited function, after the fix

### `src/devices/dev_pckbc.c` -- post-edit lines 946-1199 (`+` marks a line the diff added or the point of a deletion)

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
 1057|+ 				/* #T54: flush aux queue, return success 0x00 */
 1058|+ 				d->head[1] = d->tail[1] = 0;
 1059|+ 				pckbc_add_code(d, 0x00, port_nr);
 1060|  				break;
 1061|  			case 0xaa:	/*  keyboard self-test  */
 1062|+ 				/* #T54: flush all output queues */
 1063|+ 				d->head[0] = d->tail[0] = 0;
 1064|+ 				d->head[1] = d->tail[1] = 0;
 1065|  				pckbc_add_code(d, 0x55, port_nr);
 1066|  				break;
 1067|  			case 0xab:	/*  keyboard interface self-test  */
 1068|  				pckbc_add_code(d, 0x00, port_nr);
 1069|  				break;
 1070|  			case 0xad:
 1071|  				d->cmdbyte |= KC8_KDISABLE;
 1072|  				break;
 1073|  			case 0xae:
 1074|  				d->cmdbyte &= ~KC8_KDISABLE;
 1075|  				break;
 1076|  			case 0xd0:
 1077|  				d->state[port_nr] = STATE_RDOUTPUT;
 1078|  				break;
 1079|  			case 0xd1:
 1080|  				d->state[port_nr] = STATE_LDOUTPUT;
 1081|  				break;
 1082|  			case 0xd3:	/*  write to auxiliary device
 1083|  					    output buffer  */
 1084|  				debug("[ pckbc: CONTROL 0xd3, TODO ]\n");
 1085|  				d->state[port_nr] = STATE_WAITING_FOR_AUX_OUT;
 1086|  				break;
 1087|  			case 0xd4:	/*  write to auxiliary port  */
 1088|  				debug("[ pckbc: CONTROL 0xd4, TODO ]\n");
 1089|  				d->state[port_nr] = STATE_WAITING_FOR_AUX;
 1090|  				break;
 1091|  			default:
 1092|  				fatal("[ pckbc: unknown CONTROL 0x%x ]\n",
 1093|  				    (int)idata);
 1094|  				d->state[port_nr] = STATE_NORMAL;
 1095|  			}
 1096|  		}
 1097|  		break;
 1098|  
 1099|  	/*
 1100|  	 *  8242 (PS2):
 1101|  	 */
 1102|  
 1103|  	case PS2 + PS2_TXBUF:
 1104|  		if (writeflag==MEM_READ) {
 1105|  			odata = random() & 0xff;
 1106|  			debug("[ pckbc: read from port %i, PS2_TXBUF: "
 1107|  			    "0x%x ]\n", port_nr, (int)odata);
 1108|  		} else {
 1109|  			debug("[ pckbc: write to port %i, PS2_TXBUF: "
 1110|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1111|  
 1112|  			/*  Handle keyboard commands:  */
 1113|  			d->reg[PS2_TXBUF] = idata;
 1114|  			dev_pckbc_command(d, port_nr);
 1115|  		}
 1116|  		break;
 1117|  
 1118|  	case PS2 + PS2_RXBUF:
 1119|  		if (writeflag==MEM_READ) {
 1120|  			/*  TODO: What should be returned if no data 
 1121|  			    is available?  */
 1122|  			odata = 0;
 1123|  			if (d->head[port_nr] != d->tail[port_nr])
 1124|  				odata = pckbc_get_code(d, port_nr);
 1125|  			debug("[ pckbc: read from port %i, PS2_RXBUF: "
 1126|  			    "0x%02x ]\n", port_nr, (int)odata);
 1127|  		} else {
 1128|  			debug("[ pckbc: write to port %i, PS2_RXBUF: "
 1129|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1130|  		}
 1131|  		break;
 1132|  
 1133|  	case PS2 + PS2_CONTROL:
 1134|  		if (writeflag==MEM_READ) {
 1135|  			debug("[ pckbc: read from port %i, PS2_CONTROL"
 1136|  			    " ]\n", port_nr);
 1137|  		} else {
 1138|  			debug("[ pckbc: write to port %i, PS2_CONTROL:"
 1139|  			    " 0x%llx ]\n", port_nr, (long long)idata);
 1140|  			d->clocksignal = (idata & 0x10) ? 1 : 0;
 1141|  			d->rx_int_enable[port_nr] = (idata & PS2_CONTROL_RXINTEN) ? 1 : 0;
 1142|  			d->tx_int_enable[port_nr] = (idata & PS2_CONTROL_TXINTEN) ? 1 : 0;
 1143|  
 1144|  			// HACK/TODO: NetBSD/sgimips' X11 seems to work when
 1145|  			// interrupts are enabled, but it seems to not turn
 1146|  			// them on. Having this here makes it work, but it not
 1147|  			// the correct solution.
 1148|  			if (port_nr == 1) {
 1149|  				d->rx_int_enable[port_nr] = 1;
 1150|  			}
 1151|  		}
 1152|  		break;
 1153|  
 1154|  	case PS2 + PS2_STATUS:
 1155|  		if (writeflag==MEM_READ) {
 1156|  			odata = d->clocksignal + PS2_STATUS_TXEMPTY;
 1157|  
 1158|  			if (d->head[port_nr] != d->tail[port_nr]) {
 1159|  				/*  receiced data available  */
 1160|  				odata |= PS2_STATUS_RXFULL;
 1161|  			}
 1162|  
 1163|  			//debug("[ pckbc: read from port %i, PS2_STATUS: "
 1164|  			//    "0x%llx ]\n", port_nr, (long long)odata);
 1165|  		} else {
 1166|  			debug("[ pckbc: write to port %i, PS2_STATUS: "
 1167|  			    "0x%llx ]\n", port_nr, (long long)idata);
 1168|  		}
 1169|  		break;
 1170|  
 1171|  	default:
 1172|  		if (writeflag==MEM_READ) {
 1173|  			debug("[ pckbc: read from unimplemented reg %i ]\n",
 1174|  			    (int)relative_addr);
 1175|  			odata = d->reg[relative_addr % DEV_PCKBC_LENGTH];
 1176|  		} else {
 1177|  			debug("[ pckbc: write to unimplemented reg %i:",
 1178|  			    (int)relative_addr);
 1179|  			for (i=0; i<len; i++)
 1180|  				debug(" %02x", data[i]);
 1181|  			debug(" ]\n");
 1182|  			d->reg[relative_addr % DEV_PCKBC_LENGTH] = idata;
 1183|  		}
 1184|  	}
 1185|  
 1186|  	/*  SGI? TODO: fix  */
 1187|  #if 0
 1188|  	if (len == 8)
 1189|  		odata |= (odata << 8) | (odata << 16) | (odata << 24) |
 1190|  		    (odata << 32) | (odata << 40) | (odata << 48) |
 1191|  		    (odata << 56);
 1192|  #endif
 1193|  	if (writeflag == MEM_READ)
 1194|  		memory_writemax64(cpu, data, len, odata);
 1195|  
 1196|  	pckbc_reassert_interrupts(d);
 1197|  
 1198|  	return 1;
 1199|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_PCKBCSELFTEST: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_PCKBCSELFTEST: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
