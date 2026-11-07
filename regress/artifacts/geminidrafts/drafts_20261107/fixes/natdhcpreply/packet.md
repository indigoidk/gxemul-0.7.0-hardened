# GXemul hardened fork -- DRAFT A FIX for one filed issue, `natdhcpreply` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `natdhcpreply`, state `open`, severity `MED`)

**title:** net/net_ip.c:net_ip_broadcast_dhcp -- the reply lacks option 53 (message type) and puts the server address in giaddr instead of siaddr -- WRONG-RESULT (strict DHCP clients ignore it)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T82 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-38).  Source URLs: https://github.com/jroark/GXemul/commit/ba17c36283c56403734ba34fcdf3522c655c5335.  Our site at de8c7547: src/net/net_ip.c:1074, :1109-1110, :1123-1139.  Portable fix: yes -- port jroark ba17c36.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark ba17c36

## The code at the cited lines

### `src/net/net_ip.c` around the row's cited line 1074 (HEAD d2a6f233, lines 1029-1119)

```c
 1029| 	    as low as 14; drop short frames before the first such read
 1030| 	    (as #162).  */
 1031| 	if (len < 86) {
 1032| 		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_ERROR,
 1033| 		    "packet too short? len=%i", len);
 1034| 		return;
 1035| 	}
 1036| 
 1037| 	if (ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_DEBUG)) {
 1038| 		char s[4000];
 1039| 
 1040| 		snprintf(s, sizeof(s), "ver=%02x ", packet[14]);
 1041| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "tos=%02x ", packet[15]);
 1042| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "len=%02x%02x ", packet[16], packet[17]);
 1043| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "id=%02x%02x ",  packet[18], packet[19]);
 1044| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ofs=%02x%02x ", packet[20], packet[21]);
 1045| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "ttl=%02x ", packet[22]);
 1046| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "p=%02x ", packet[23]);
 1047| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "sum=%02x%02x ", packet[24], packet[25]);
 1048| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "src=%02x%02x%02x%02x ",
 1049| 		    packet[26], packet[27], packet[28], packet[29]);
 1050| 		snprintf(s+strlen(s), sizeof(s)-strlen(s), "dst=%02x%02x%02x%02x ",
 1051| 		    packet[30], packet[31], packet[32], packet[33]);
 1052| 		for (i=34; i<len; i++) {
 1053| 			if (strlen(s) > sizeof(s) - 5)
 1054| 				break;
 1055| 			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x", packet[i]);
 1056| 		}
 1057| 
 1058| 		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_DEBUG, "%s", s);
 1059| 	}
 1060| 
 1061| 	if (len < 34 + 8 + 236) {
 1062| 		debugmsg(SUBSYS_NET, "IPv4 DHCP", VERBOSITY_ERROR, "packet too short? len=%i", len);
 1063| 		return;
 1064| 	}
 1065| 
 1066| 	/*
 1067| 	 *  UDP data (at offset 34):
 1068| 	 *
 1069| 	 *  srcport=0044 dstport=0043 length=0134 chksum=a973
 1070| 	 *  data = 01010600d116d276000000000000000000000000000000
 1071| 	 *         0000000000102030405060...0000...638253633501...000
 1072| 	 */
 1073| 
 1074|         reply_len = 307;
 1075|         lp = net_allocate_ethernet_packet_link(net, nic, reply_len);
 1076| 
 1077|         /*  From old packet, copy everything before options field:  */
 1078|         memcpy(lp->data, packet, 278);
 1079| 
 1080| 	/*  We are sending to the client, from the gateway:  */
 1081| 	memcpy(lp->data + 0, packet + 6, 6);
 1082| 	memcpy(lp->data + 6, net->gateway_ethernet_addr, 6);
 1083| 
 1084| 	/*  Set IP length:  */
 1085| 	lp->data[16] = (reply_len - 14) >> 8;
 1086| 	lp->data[17] = (reply_len - 14) & 0xff;
 1087| 
 1088|         /*  Set IP addresses:  */
 1089| 	memcpy(lp->data + 26, &net->gateway_ipv4_addr[0], 4);
 1090| 	lp->data[30] = 0xff;
 1091| 	lp->data[31] = 0xff;
 1092| 	lp->data[32] = 0xff;
 1093| 	lp->data[33] = 0xff;
 1094| 
 1095| 	/*  Switch src and dst ports:  */
 1096| 	memcpy(lp->data + 34, packet + 36, 2);
 1097| 	memcpy(lp->data + 36, packet + 34, 2);
 1098| 
 1099| 	/*  Set UDP length:  */
 1100| 	lp->data[38] = (reply_len - 34) >> 8;
 1101| 	lp->data[39] = (reply_len - 34) & 0xff;
 1102| 
 1103| 	/*  Client's (yiaddr) IPv4 address:  */
 1104| 	lp->data[58] = 10;
 1105| 	lp->data[59] = 0;
 1106| 	lp->data[60] = 0;
 1107| 	lp->data[61] = 1;	/*  TODO  */
 1108| 
 1109| 	/*  Server's IPv4 address:  (giaddr)  */
 1110| 	memcpy(lp->data + 66, &net->gateway_ipv4_addr[0], 4);
 1111| 
 1112| 	/*  This is a Reply:  */
 1113| 	lp->data[42] = 0x02;
 1114| 
 1115| 	snprintf((char *)lp->data + 70+16+64, 8, "gxemul");
 1116| 
 1117| 	/*  Options field at offset 278:  */
 1118| 	lp->data[278] = 99;
 1119| 	lp->data[279] = 130;
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

End with one line: `FIXDRAFT_NATDHCPREPLY: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
