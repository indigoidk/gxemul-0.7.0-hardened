# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `rarpaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `rarpaddr`, state `open`)

**title:** net/net.c:net_arp RARP arm -- the reply assigns 10.0.0.0 when MAC byte 5 is below 0x10 -- WRONG-RESULT (minor)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T104 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-59).  Source URLs: https://github.com/rpajarola/gxemul/commit/a4f5ea2dc20970c0da2935e466a2cdf43bc0885d.  Our site at de8c7547: src/net/net.c:250-254.  Portable fix: yes -- port rpajarola a4f5ea2 (embedded fix).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 250| 			q = (packet[8 + 5]) >> 4;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/net/net.c b/src/net/net.c
index 337d752d..83e21cce 100644
--- a/src/net/net.c
+++ b/src/net/net.c
@@ -248,6 +248,7 @@ static void net_arp(struct net *net, struct nic_data *nic,
 			/*  q = (packet[8 + 3]) >> 4;  */
 			/*  q = q*15 + ((packet[8 + 4]) >> 4);  */
 			q = (packet[8 + 5]) >> 4;
+			if (q == 0) q = packet[8 + 5] ? packet[8 + 5] : 1;	/* #105: avoid 10.0.0.0 network address */
 			lp->data[24 + 14] = 10;
 			lp->data[25 + 14] =  0;
 			lp->data[26 + 14] =  0;
```

## Every edited function, after the fix

### `src/net/net.c` -- post-edit lines 136-271 (`+` marks a line the diff added or the point of a deletion)

```c
  136|  {
  137|  	int q;
  138|  	int i;
  139|  
  140|  	/*  #132: a full ARP/RARP body is 28 bytes, and everything below
  141|  	    (including the debug dump) reads up to packet[27], but the
  142|  	    caller only guarantees len >= 20. Reject shorter frames.  */
  143|  	if (len < 28) {
  144|  		debugmsg(SUBSYS_NET, reverse? "RARP" : "ARP",
  145|  		    VERBOSITY_WARNING,
  146|  		    "too short %i-byte ARP/RARP frame ignored", len);
  147|  		return;
  148|  	}
  149|  
  150|  	/*  TODO: This debug dump assumes ethernet->IPv4 translation:  */
  151|  	if (ENOUGH_VERBOSITY(SUBSYS_NET, VERBOSITY_DEBUG)) {
  152|  		char s[300];
  153|  		s[0] = '\0';
  154|  
  155|  		for (i=0; i<2; i++)
  156|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x",
  157|  			    packet[i]);
  158|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), " ");
  159|  		for (i=2; i<4; i++)
  160|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x",
  161|  			    packet[i]);
  162|  		snprintf(s+strlen(s), sizeof(s)-strlen(s),
  163|  		    " %02x %02x req=%02x%02x from=",
  164|  		    packet[4], packet[5], packet[6], packet[7]);
  165|  		for (i=8; i<18; i++)
  166|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x",
  167|  			    packet[i]);
  168|  		snprintf(s+strlen(s), sizeof(s)-strlen(s), " to=");
  169|  		for (i=18; i<28; i++)
  170|  			snprintf(s+strlen(s), sizeof(s)-strlen(s), "%02x",
  171|  			    packet[i]);
  172|  
  173|  		debugmsg(SUBSYS_NET, reverse? "RARP" : "ARP",
  174|  		    VERBOSITY_DEBUG, "%s", s);
  175|  	}
  176|  
  177|  	if (packet[0] == 0x00 && packet[1] == 0x01 &&
  178|  	    packet[2] == 0x08 && packet[3] == 0x00 &&
  179|  	    packet[4] == 0x06 && packet[5] == 0x04) {
  180|  		int r = (packet[6] << 8) + packet[7];
  181|  		struct ethernet_packet_link *lp;
  182|  
  183|  		switch (r) {
  184|  		case 1:		/*  Request  */
  185|  			/*  Only create a reply if this was meant for the
  186|  			    gateway:  */
  187|  			if (memcmp(packet+24, net->gateway_ipv4_addr, 4) != 0)
  188|  				break;
  189|  
  190|  			lp = net_allocate_ethernet_packet_link(
  191|  			    net, nic, 60 + 14);
  192|  
  193|  			/*  Copy the old packet first:  */
  194|  			memset(lp->data, 0, 60 + 14);
  195|  			if (len > 60) { static int w = 0; if (!w) { debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING, "oversized %i-byte ARP/RARP frame capped to 60", len); w = 1; } }	/* #119 */
  196|  			memcpy(lp->data + 14, packet, len < 0 ? 0 : (len > 60 ? 60 : len));	/* #102: lp->data is 74 B; cap copy to the 60-B body */
  197|  
  198|  			/*  Add ethernet ARP header:  */
  199|  			memcpy(lp->data + 0, lp->data + 8 + 14, 6);
  200|  			memcpy(lp->data + 6, net->gateway_ethernet_addr, 6);
  201|  			lp->data[12] = 0x08; lp->data[13] = 0x06;
  202|  
  203|  			/*  Address of the emulated machine:  */
  204|  			memcpy(lp->data + 18 + 14, lp->data + 8 + 14, 10);
  205|  
  206|  			/*  Address of the gateway:  */
  207|  			memcpy(lp->data +  8 + 14, net->gateway_ethernet_addr,
  208|  			    6);
  209|  			memcpy(lp->data + 14 + 14, net->gateway_ipv4_addr, 4);
  210|  
  211|  			/*  This is a Reply:  */
  212|  			lp->data[6 + 14] = 0x00; lp->data[7 + 14] = 0x02;
  213|  
  214|  			break;
  215|  		case 3:		/*  Reverse Request  */
  216|  			lp = net_allocate_ethernet_packet_link(
  217|  			    net, nic, 60 + 14);
  218|  
  219|  			/*  Copy the old packet first:  */
  220|  			memset(lp->data, 0, 60 + 14);
  221|  			if (len > 60) { static int w = 0; if (!w) { debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING, "oversized %i-byte ARP/RARP frame capped to 60", len); w = 1; } }	/* #119 */
  222|  			memcpy(lp->data + 14, packet, len < 0 ? 0 : (len > 60 ? 60 : len));	/* #102: lp->data is 74 B; cap copy to the 60-B body */
  223|  
  224|  			/*  Add ethernet RARP header:  */
  225|  			memcpy(lp->data + 0, packet + 8, 6);
  226|  			memcpy(lp->data + 6, net->gateway_ethernet_addr, 6);
  227|  			lp->data[12] = 0x80; lp->data[13] = 0x35;
  228|  
  229|  			/*  This is a RARP reply:  */
  230|  			lp->data[6 + 14] = 0x00; lp->data[7 + 14] = 0x04;
  231|  
  232|  			/*  Address of the gateway:  */
  233|  			memcpy(lp->data +  8 + 14, net->gateway_ethernet_addr,
  234|  			    6);
  235|  			memcpy(lp->data + 14 + 14, net->gateway_ipv4_addr, 4);
  236|  
  237|  			/*  MAC address of emulated machine:  */
  238|  			memcpy(lp->data + 18 + 14, packet + 8, 6);
  239|  
  240|  			/*
  241|  			 *  IP address of the emulated machine:  Automagically
  242|  			 *  generated from the MAC address. :-)
  243|  			 *
  244|  			 *  packet+8 points to the client's mac address,
  245|  			 *  for example 10:20:30:00:00:z0, where z is 0..15.
  246|  			 *  10:20:30:00:00:10 results in 10.0.0.1.
  247|  			 */
  248|  			/*  q = (packet[8 + 3]) >> 4;  */
  249|  			/*  q = q*15 + ((packet[8 + 4]) >> 4);  */
  250|  			q = (packet[8 + 5]) >> 4;
  251|+ 			if (q == 0) q = packet[8 + 5] ? packet[8 + 5] : 1;	/* #105: avoid 10.0.0.0 network address */
  252|  			lp->data[24 + 14] = 10;
  253|  			lp->data[25 + 14] =  0;
  254|  			lp->data[26 + 14] =  0;
  255|  			lp->data[27 + 14] =  q;
  256|  			break;
  257|  		case 2:		/*  Reply  */
  258|  		case 4:		/*  Reverse Reply  */
  259|  		default:
  260|  			debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING,
  261|  	    		    "UNIMPLEMENTED request type 0x%04x", r);
  262|  		}
  263|  	} else {
  264|  		if (len >= 6)
  265|  			debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING,
  266|  	   		    "UNIMPLEMENTED arp packet type: "
  267|  	   		    "0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x ...",
  268|  	   		    packet[0], packet[1], packet[2], packet[3],
  269|  	   		    packet[4], packet[5]);
  270|  	}
  271|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_RARPADDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_RARPADDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
