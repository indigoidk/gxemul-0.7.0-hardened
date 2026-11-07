# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `natdhcpreply` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `natdhcpreply`, state `open`)

**title:** net/net_ip.c:net_ip_broadcast_dhcp -- the reply lacks option 53 (message type) and puts the server address in giaddr instead of siaddr -- WRONG-RESULT (strict DHCP clients ignore it)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T82 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-38).  Source URLs: https://github.com/jroark/GXemul/commit/ba17c36283c56403734ba34fcdf3522c655c5335.  Our site at de8c7547: src/net/net_ip.c:1074, :1109-1110, :1123-1139.  Portable fix: yes -- port jroark ba17c36.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/net/net_ip.c` -- AT HEAD, lines 1023-1197 (`*` marks a line your previous draft changed)

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
 1074|          reply_len = 307;
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
 1109|* 	/*  Server's IPv4 address:  (giaddr)  */
 1110|* 	memcpy(lp->data + 66, &net->gateway_ipv4_addr[0], 4);
 1111|* 
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
 1139|  	lp->data[306] = 255; /* end */
 1140|  
 1141|  	/*  Recalculate IP header checksum:  */
 1142|  	net_ip_checksum(lp->data + 14, 10, 20);
 1143|  
 1144|  	/*  ... and the UDP checksum:  */
 1145|          net_ip_tcp_checksum(lp->data + 34, 6, reply_len - 34,
 1146|  	    lp->data + 26, lp->data + 30, 1);
 1147|  
 1148|  	if (ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_DEBUG)) {
 1149|  		char s[4000];
 1150|  		s[0] = '\0';
 1151|  
 1152|  		packet = lp->data;
 1153|  
 1154|  		for (i=0; i<14; i++) {
 1155|  			if (strlen(s) > sizeof(s) - 5)
 1156|  				break;
 1157|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1158|  		}
 1159|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ver=%02x ", packet[14]);
 1160|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "tos=%02x ", packet[15]);
 1161|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "len=%02x%02x ", packet[16], packet[17]);
 1162|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "id=%02x%02x ",  packet[18], packet[19]);
 1163|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ofs=%02x%02x ", packet[20], packet[21]);
 1164|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ttl=%02x ", packet[22]);
 1165|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "p=%02x ", packet[23]);
 1166|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "sum=%02x%02x ", packet[24], packet[25]);
 1167|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "src=%02x%02x%02x%02x ",
 1168|  		    packet[26], packet[27], packet[28], packet[29]);
 1169|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "dst=%02x%02x%02x%02x ",
 1170|  		    packet[30], packet[31], packet[32], packet[33]);
 1171|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "op=%02x ", packet[42]);
 1172|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "htype=%02x ", packet[43]);
 1173|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "hlen=%02x ", packet[44]);
 1174|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "hops=%02x ", packet[45]);
 1175|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "xid=%02x%02x%02x%02x ",
 1176|  			packet[46], packet[47], packet[48], packet[49]);
 1177|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "secs=%02x%02x ", packet[50], packet[51]);
 1178|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "flags=%02x%02x ", packet[52], packet[53]);
 1179|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ciaddr=%02x%02x%02x%02x ",
 1180|  			packet[54], packet[55], packet[56], packet[57]);
 1181|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "yiaddr=%02x%02x%02x%02x ",
 1182|  			packet[58], packet[59], packet[60], packet[61]);
 1183|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "siaddr=%02x%02x%02x%02x ",
 1184|  			packet[62], packet[63], packet[64], packet[65]);
 1185|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "giaddr=%02x%02x%02x%02x ",
 1186|  			packet[66], packet[67], packet[68], packet[69]);
 1187|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), "chaddr=");
 1188|  		for (i=70; i<70+16; i++) {
 1189|  			if (strlen(s) > sizeof(s) - 5)
 1190|  				break;
 1191|  
 1192|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1193|  		}
 1194|  
 1195|  		debugmsg(SUBSYS_NET, "IPv4 DHCP REPLY", VERBOSITY_DEBUG, "%s", s);
 1196|  	}
 1197|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/net/net_ip.c",
    "old": "\t/*  Server's IPv4 address:  (giaddr)  */\n\tmemcpy(lp->data + 66, &net->gateway_ipv4_addr[0], 4);",
    "new": "\t/*  Server's IPv4 address:  (siaddr)  */\n\tmemcpy(lp->data + 62, &net->gateway_ipv4_addr[0], 4);\n\n\t/* #001: Add option 53 (DHCP Message Type = ACK) */\n\tlp->data[282] = 53;\n\tlp->data[283] = 1;\n\tlp->data[284] = 5;\n\tlp->data[285] = 255;",
    "why": "Move server IP from giaddr (offset 66) to siaddr (offset 62) and append DHCP Message Type option 53 with ACK (5) and End (255)."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_NATDHCPREPLY: DEFECT, 1 FINDINGS
1. The diff does NOT successfully add option 53. It moves the server address from `giaddr` (66) to `siaddr` (62) correctly, but the added Option 53 assignments at `src/net/net_ip.c:1113-1116` to offsets 282-285 are unconditionally overwritten by the subnet mask option at `src/net/net_ip.c:1130-1133` which writes to the exact same offsets.
2. No added `return`, `goto`, `break`, or early exit skips any code.
3. No return values are changed.
4. The diff changes nothing else beyond the failed defect removal.
5. The comment tag `#001:` follows the required house idiom.
src/net/net_ip.c:1113, DEFECT, shift Option 53 to append at 306, move the 255 end marker to 309, and increase reply_len to 310.
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

End with two lines: `REVISION_NATDHCPREPLY: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_NATDHCPREPLY: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
