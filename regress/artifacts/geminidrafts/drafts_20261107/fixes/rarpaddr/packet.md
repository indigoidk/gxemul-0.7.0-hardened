# GXemul hardened fork -- DRAFT A FIX for one filed issue, `rarpaddr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `rarpaddr`, state `open`, severity `MED`)

**title:** net/net.c:net_arp RARP arm -- the reply assigns 10.0.0.0 when MAC byte 5 is below 0x10 -- WRONG-RESULT (minor)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T104 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-59).  Source URLs: https://github.com/rpajarola/gxemul/commit/a4f5ea2dc20970c0da2935e466a2cdf43bc0885d.  Our site at de8c7547: src/net/net.c:250-254.  Portable fix: yes -- port rpajarola a4f5ea2 (embedded fix).  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola a4f5ea2

## The code at the cited lines

### `src/net/net.c` around the row's cited line 250 (HEAD 2d25df65, lines 205-295)

```c
  205| 
  206| 			/*  Address of the gateway:  */
  207| 			memcpy(lp->data +  8 + 14, net->gateway_ethernet_addr,
  208| 			    6);
  209| 			memcpy(lp->data + 14 + 14, net->gateway_ipv4_addr, 4);
  210| 
  211| 			/*  This is a Reply:  */
  212| 			lp->data[6 + 14] = 0x00; lp->data[7 + 14] = 0x02;
  213| 
  214| 			break;
  215| 		case 3:		/*  Reverse Request  */
  216| 			lp = net_allocate_ethernet_packet_link(
  217| 			    net, nic, 60 + 14);
  218| 
  219| 			/*  Copy the old packet first:  */
  220| 			memset(lp->data, 0, 60 + 14);
  221| 			if (len > 60) { static int w = 0; if (!w) { debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING, "oversized %i-byte ARP/RARP frame capped to 60", len); w = 1; } }	/* #119 */
  222| 			memcpy(lp->data + 14, packet, len < 0 ? 0 : (len > 60 ? 60 : len));	/* #102: lp->data is 74 B; cap copy to the 60-B body */
  223| 
  224| 			/*  Add ethernet RARP header:  */
  225| 			memcpy(lp->data + 0, packet + 8, 6);
  226| 			memcpy(lp->data + 6, net->gateway_ethernet_addr, 6);
  227| 			lp->data[12] = 0x80; lp->data[13] = 0x35;
  228| 
  229| 			/*  This is a RARP reply:  */
  230| 			lp->data[6 + 14] = 0x00; lp->data[7 + 14] = 0x04;
  231| 
  232| 			/*  Address of the gateway:  */
  233| 			memcpy(lp->data +  8 + 14, net->gateway_ethernet_addr,
  234| 			    6);
  235| 			memcpy(lp->data + 14 + 14, net->gateway_ipv4_addr, 4);
  236| 
  237| 			/*  MAC address of emulated machine:  */
  238| 			memcpy(lp->data + 18 + 14, packet + 8, 6);
  239| 
  240| 			/*
  241| 			 *  IP address of the emulated machine:  Automagically
  242| 			 *  generated from the MAC address. :-)
  243| 			 *
  244| 			 *  packet+8 points to the client's mac address,
  245| 			 *  for example 10:20:30:00:00:z0, where z is 0..15.
  246| 			 *  10:20:30:00:00:10 results in 10.0.0.1.
  247| 			 */
  248| 			/*  q = (packet[8 + 3]) >> 4;  */
  249| 			/*  q = q*15 + ((packet[8 + 4]) >> 4);  */
  250| 			q = (packet[8 + 5]) >> 4;
  251| 			lp->data[24 + 14] = 10;
  252| 			lp->data[25 + 14] =  0;
  253| 			lp->data[26 + 14] =  0;
  254| 			lp->data[27 + 14] =  q;
  255| 			break;
  256| 		case 2:		/*  Reply  */
  257| 		case 4:		/*  Reverse Reply  */
  258| 		default:
  259| 			debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING,
  260| 	    		    "UNIMPLEMENTED request type 0x%04x", r);
  261| 		}
  262| 	} else {
  263| 		if (len >= 6)
  264| 			debugmsg(SUBSYS_NET, "ARP", VERBOSITY_WARNING,
  265| 	   		    "UNIMPLEMENTED arp packet type: "
  266| 	   		    "0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x ...",
  267| 	   		    packet[0], packet[1], packet[2], packet[3],
  268| 	   		    packet[4], packet[5]);
  269| 	}
  270| }
  271| 
  272| 
  273| /*
  274|  *  net_ethernet_rx_avail():
  275|  *
  276|  *  Return 1 if there is a packet available for this nic, otherwise
  277|  *  return 0.
  278|  *
  279|  *  Appart from actually checking for incoming packets from the outside world,
  280|  *  this function basically works like net_ethernet_rx() but it only receives
  281|  *  a return value telling us whether there is a packet or not, we don't
  282|  *  actually get the packet.
  283|  */
  284| int net_ethernet_rx_avail(struct net *net, struct nic_data *nic)
  285| {
  286| 	if (net == NULL)
  287| 		return 0;
  288| 
  289| 	/*
  290| 	 *  If we're using a tap device, check in with that and
  291| 	 *  that's it.
  292| 	 */
  293| 	if (net->tapdev) {
  294| 		net_tap_rx_avail(net);
  295| 		return net_ethernet_rx(net, nic, NULL, NULL);
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_RARPADDR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
