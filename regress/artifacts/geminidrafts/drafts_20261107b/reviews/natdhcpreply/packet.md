# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `natdhcpreply` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `natdhcpreply`, state `open`)

**title:** net/net_ip.c:net_ip_broadcast_dhcp -- the reply lacks option 53 (message type) and puts the server address in giaddr instead of siaddr -- WRONG-RESULT (strict DHCP clients ignore it)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T82 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-38).  Source URLs: https://github.com/jroark/GXemul/commit/ba17c36283c56403734ba34fcdf3522c655c5335.  Our site at de8c7547: src/net/net_ip.c:1074, :1109-1110, :1123-1139.  Portable fix: yes -- port jroark ba17c36.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `HEAD:1109-1110` still writes to giaddr, and `HEAD:1074`/`HEAD:1139` lack Option 53.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/net/net_ip.c b/src/net/net_ip.c
index 528d319d..95d5e07d 100644
--- a/src/net/net_ip.c
+++ b/src/net/net_ip.c
@@ -1071,7 +1071,7 @@ static void net_ip_broadcast_dhcp(struct net *net, struct nic_data *nic,
 	 *         0000000000102030405060...0000...638253633501...000
 	 */
 
-        reply_len = 307;
+        reply_len = 310; /* #001: increase for option 53 */
         lp = net_allocate_ethernet_packet_link(net, nic, reply_len);
 
         /*  From old packet, copy everything before options field:  */
@@ -1106,8 +1106,8 @@ static void net_ip_broadcast_dhcp(struct net *net, struct nic_data *nic,
 	lp->data[60] = 0;
 	lp->data[61] = 1;	/*  TODO  */
 
-	/*  Server's IPv4 address:  (giaddr)  */
-	memcpy(lp->data + 66, &net->gateway_ipv4_addr[0], 4);
+	/*  Server's IPv4 address:  (siaddr)  */
+	memcpy(lp->data + 62, &net->gateway_ipv4_addr[0], 4);
 
 	/*  This is a Reply:  */
 	lp->data[42] = 0x02;
@@ -1136,7 +1136,11 @@ static void net_ip_broadcast_dhcp(struct net *net, struct nic_data *nic,
 	lp->data[300] = 54; /* server identifier */
 	lp->data[301] = 4;
 	memcpy(lp->data + 302, &net->gateway_ipv4_addr[0], 4);
-	lp->data[306] = 255; /* end */
+	/* #001: Add option 53 (DHCP Message Type = ACK) */
+	lp->data[306] = 53;
+	lp->data[307] = 1;
+	lp->data[308] = 5;
+	lp->data[309] = 255; /* end */
 
 	/*  Recalculate IP header checksum:  */
 	net_ip_checksum(lp->data + 14, 10, 20);
```

## Every edited function, after the fix

### `src/net/net_ip.c` -- post-edit lines 1023-1201 (`+` marks a line the diff added or the point of a deletion)

```c
 1023|  {
 1024|  	struct ethernet_packet_link *lp;
 1025|          int i, reply_len;
 1026|  
 1027|  	/*  #177: (Codex/Fable) the debug dumps assume DHCP fields at fixed
 1028|  	    offsets up to packet[85], but the caller's tail-cut can pass len
 1029|  	    as low as 14; drop short frames before the first such read
 1030|  	    (as #162).  */
 1031|  	if (len < 86) {
 1032|  		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_ERROR,
 1033|  		    "packet too short? len=%i", len);
 1034|  		return;
 1035|  	}
 1036|  
 1037|  	if (ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_DEBUG)) {
 1038|  		char s[4000];
 1039|  
 1040|  		snprintf(s, sizeof(s), "ver=%02x ", packet[14]);
 1041|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "tos=%02x ", packet[15]);
 1042|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "len=%02x%02x ", packet[16], packet[17]);
 1043|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "id=%02x%02x ",  packet[18], packet[19]);
 1044|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ofs=%02x%02x ", packet[20], packet[21]);
 1045|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ttl=%02x ", packet[22]);
 1046|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "p=%02x ", packet[23]);
 1047|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "sum=%02x%02x ", packet[24], packet[25]);
 1048|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "src=%02x%02x%02x%02x ",
 1049|  		    packet[26], packet[27], packet[28], packet[29]);
 1050|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "dst=%02x%02x%02x%02x ",
 1051|  		    packet[30], packet[31], packet[32], packet[33]);
 1052|  		for (i=34; i<len; i++) {
 1053|  			if (strlen(s) > sizeof(s) - 5)
 1054|  				break;
 1055|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1056|  		}
 1057|  
 1058|  		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_DEBUG, "%s", s);
 1059|  	}
 1060|  
 1061|  	if (len < 34 + 8 + 236) {
 1062|  		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_ERROR, "packet too short? len=%i", len);
 1063|  		return;
 1064|  	}
 1065|  
 1066|  	/*
 1067|  	 *  UDP data (at offset 34):
 1068|  	 *
 1069|  	 *  srcport=0044 dstport=0043 length=0134 chksum=a973
 1070|  	 *  data = 01010600d116d276000000000000000000000000000000
 1071|  	 *         0000000000102030405060...0000...638253633501...000
 1072|  	 */
 1073|  
 1074|+         reply_len = 310; /* #001: increase for option 53 */
 1075|          lp = net_allocate_ethernet_packet_link(net, nic, reply_len);
 1076|  
 1077|          /*  From old packet, copy everything before options field:  */
 1078|          memcpy(lp->data, packet, 278);
 1079|  
 1080|  	/*  We are sending to the client, from the gateway:  */
 1081|  	memcpy(lp->data + 0, packet + 6, 6);
 1082|  	memcpy(lp->data + 6, net->gateway_ethernet_addr, 6);
 1083|  
 1084|  	/*  Set IP length:  */
 1085|  	lp->data[16] = (reply_len - 14) >> 8;
 1086|  	lp->data[17] = (reply_len - 14) & 0xff;
 1087|  
 1088|          /*  Set IP addresses:  */
 1089|  	memcpy(lp->data + 26, &net->gateway_ipv4_addr[0], 4);
 1090|  	lp->data[30] = 0xff;
 1091|  	lp->data[31] = 0xff;
 1092|  	lp->data[32] = 0xff;
 1093|  	lp->data[33] = 0xff;
 1094|  
 1095|  	/*  Switch src and dst ports:  */
 1096|  	memcpy(lp->data + 34, packet + 36, 2);
 1097|  	memcpy(lp->data + 36, packet + 34, 2);
 1098|  
 1099|  	/*  Set UDP length:  */
 1100|  	lp->data[38] = (reply_len - 34) >> 8;
 1101|  	lp->data[39] = (reply_len - 34) & 0xff;
 1102|  
 1103|  	/*  Client's (yiaddr) IPv4 address:  */
 1104|  	lp->data[58] = 10;
 1105|  	lp->data[59] = 0;
 1106|  	lp->data[60] = 0;
 1107|  	lp->data[61] = 1;	/*  TODO  */
 1108|  
 1109|+ 	/*  Server's IPv4 address:  (siaddr)  */
 1110|+ 	memcpy(lp->data + 62, &net->gateway_ipv4_addr[0], 4);
 1111|  
 1112|  	/*  This is a Reply:  */
 1113|  	lp->data[42] = 0x02;
 1114|  
 1115|  	snprintf((char *)lp->data + 70+16+64, 8, "gxemul");
 1116|  
 1117|  	/*  Options field at offset 278:  */
 1118|  	lp->data[278] = 99;
 1119|  	lp->data[279] = 130;
 1120|  	lp->data[280] = 83;
 1121|  	lp->data[281] = 99;
 1122|  
 1123|  	/*  DHCP options, http://tools.ietf.org/html/rfc1533  */
 1124|  	lp->data[282] = 1; /* subnet mask */
 1125|  	lp->data[283] = 4;
 1126|  	lp->data[284] = 255;
 1127|  	lp->data[285] = 0;
 1128|  	lp->data[286] = 0;
 1129|  	lp->data[287] = 0;
 1130|  	lp->data[288] = 3; /* router */
 1131|  	lp->data[289] = 4;
 1132|  	memcpy(lp->data + 290, &net->gateway_ipv4_addr[0], 4);
 1133|  	lp->data[294] = 6; /* domain name server */
 1134|  	lp->data[295] = 4;
 1135|  	memcpy(lp->data + 296, &net->gateway_ipv4_addr[0], 4);
 1136|  	lp->data[300] = 54; /* server identifier */
 1137|  	lp->data[301] = 4;
 1138|  	memcpy(lp->data + 302, &net->gateway_ipv4_addr[0], 4);
 1139|+ 	/* #001: Add option 53 (DHCP Message Type = ACK) */
 1140|+ 	lp->data[306] = 53;
 1141|+ 	lp->data[307] = 1;
 1142|+ 	lp->data[308] = 5;
 1143|+ 	lp->data[309] = 255; /* end */
 1144|  
 1145|  	/*  Recalculate IP header checksum:  */
 1146|  	net_ip_checksum(lp->data + 14, 10, 20);
 1147|  
 1148|  	/*  ... and the UDP checksum:  */
 1149|          net_ip_tcp_checksum(lp->data + 34, 6, reply_len - 34,
 1150|  	    lp->data + 26, lp->data + 30, 1);
 1151|  
 1152|  	if (ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_DEBUG)) {
 1153|  		char s[4000];
 1154|  		s[0] = '\0';
 1155|  
 1156|  		packet = lp->data;
 1157|  
 1158|  		for (i=0; i<14; i++) {
 1159|  			if (strlen(s) > sizeof(s) - 5)
 1160|  				break;
 1161|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1162|  		}
 1163|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ver=%02x ", packet[14]);
 1164|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "tos=%02x ", packet[15]);
 1165|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "len=%02x%02x ", packet[16], packet[17]);
 1166|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "id=%02x%02x ",  packet[18], packet[19]);
 1167|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ofs=%02x%02x ", packet[20], packet[21]);
 1168|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ttl=%02x ", packet[22]);
 1169|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "p=%02x ", packet[23]);
 1170|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "sum=%02x%02x ", packet[24], packet[25]);
 1171|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "src=%02x%02x%02x%02x ",
 1172|  		    packet[26], packet[27], packet[28], packet[29]);
 1173|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "dst=%02x%02x%02x%02x ",
 1174|  		    packet[30], packet[31], packet[32], packet[33]);
 1175|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "op=%02x ", packet[42]);
 1176|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "htype=%02x ", packet[43]);
 1177|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "hlen=%02x ", packet[44]);
 1178|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "hops=%02x ", packet[45]);
 1179|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "xid=%02x%02x%02x%02x ",
 1180|  			packet[46], packet[47], packet[48], packet[49]);
 1181|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "secs=%02x%02x ", packet[50], packet[51]);
 1182|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "flags=%02x%02x ", packet[52], packet[53]);
 1183|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ciaddr=%02x%02x%02x%02x ",
 1184|  			packet[54], packet[55], packet[56], packet[57]);
 1185|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "yiaddr=%02x%02x%02x%02x ",
 1186|  			packet[58], packet[59], packet[60], packet[61]);
 1187|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "siaddr=%02x%02x%02x%02x ",
 1188|  			packet[62], packet[63], packet[64], packet[65]);
 1189|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "giaddr=%02x%02x%02x%02x ",
 1190|  			packet[66], packet[67], packet[68], packet[69]);
 1191|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "chaddr=");
 1192|  		for (i=70; i<70+16; i++) {
 1193|  			if (strlen(s) > sizeof(s) - 5)
 1194|  				break;
 1195|  
 1196|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1197|  		}
 1198|  
 1199|  		debugmsg(SUBSYS_NET, "IPv4 DHCP REPLY", VERBOSITY_DEBUG, "%s", s);
 1200|  	}
 1201|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_NATDHCPREPLY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_NATDHCPREPLY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
