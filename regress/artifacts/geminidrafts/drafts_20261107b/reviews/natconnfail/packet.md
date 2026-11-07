# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `natconnfail` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `natconnfail`, state `open`)

**title:** net/net_ip.c:net_ip_tcp/net_tcp_rx_avail -- a failed outgoing NAT connect() is reported to the guest as connected and then closed -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T81 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-53, A(c)#12).  Source URLs: https://github.com/rpajarola/gxemul/commit/1c18c2b1ddb90a62cd27c4873b436511d730383d.  Our site at de8c7547: src/net/net_ip.c:594-601, :1520-1552.  Portable fix: yes -- port rpajarola 1c18c2b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/net/net_ip.c:597

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/net/net_ip.c b/src/net/net_ip.c
index 528d319d..dd5fd893 100644
--- a/src/net/net_ip.c
+++ b/src/net/net_ip.c
@@ -596,6 +596,12 @@ static void net_ip_tcp(struct net *net, struct nic_data *nic,
 
 		/*  connect can return -1, and errno = EINPROGRESS
 		    as we might not have connected right away.  */
+		if (res < 0 && errno != EINPROGRESS) {
+			/* #NNN: reject connection immediately if connect fails */
+			net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
+			tcp_closeconnection(net, con_id);
+			return;
+		}
 
 		net->tcp_connections[con_id].state =
 		    TCP_OUTSIDE_TRYINGTOCONNECT;
```

## Every edited function, after the fix

### `src/net/net_ip.c` -- post-edit lines 389-772 (`+` marks a line the diff added or the point of a deletion)

```c
  389|  {
  390|  	int con_id, free_con_id, i, res;
  391|  	int srcport, dstport, data_offset, window, checksum, urgptr;
  392|  	int syn, ack, psh, rst, urg, fin;
  393|  	uint32_t seqnr, acknr;
     | [... lines 394-488 not shown ...]
  489|  
  490|  	/*
  491|  	 *  Unknown connection, and not SYN? Then drop the packet.
  492|  	 *  TODO:  Send back RST?
  493|  	 */
  494|  	if (con_id < 0 && !syn) {
  495|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  496|  		    "dropping packet from unknown connection,"
  497|  		    " %i.%i.%i.%i:%i -> %i.%i.%i.%i:%i %s%s%s%s%s",
  498|  		    packet[26], packet[27], packet[28], packet[29], srcport,
  499|  		    packet[30], packet[31], packet[32], packet[33], dstport,
  500|  		    fin? "FIN ": "", syn? "SYN ": "", ack? "ACK ": "",
  501|  		    psh? "PSH ": "", rst? "RST ": "");
  502|  		return;
  503|  	}
  504|  
  505|  	/*  Known connection, and SYN? Then ignore the packet.  */
  506|  	if (con_id >= 0 && syn) {
  507|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  508|  		    "ignoring redundant SYN packet from known"
  509|  		    " connection, %i.%i.%i.%i:%i -> %i.%i.%i.%i:%i",
  510|  		    packet[26], packet[27], packet[28], packet[29], srcport,
  511|  		    packet[30], packet[31], packet[32], packet[33], dstport);
  512|  		return;
  513|  	}
  514|  
  515|  	/*
  516|  	 *  A new outgoing connection?
  517|  	 */
  518|  	if (con_id < 0 && syn) {
  519|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  520|  		    "new outgoing connection, %i.%i.%i.%i:%i"
  521|  		    " -> %i.%i.%i.%i:%i",
  522|  		    packet[26], packet[27], packet[28], packet[29], srcport,
  523|  		    packet[30], packet[31], packet[32], packet[33], dstport);
  524|  
  525|  		/*  Find a free connection id to use:  */
  526|  		if (free_con_id < 0) {
  527|  #if 1
  528|  			/*
  529|  			 *  TODO:  Reuse the oldest one currently in use, or
  530|  			 *  just drop the new connection attempt? Drop for now.
  531|  			 */
  532|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_WARNING,
  533|  			    "TOO MANY TCP CONNECTIONS IN USE! "
  534|  			    "Increase MAX_TCP_CONNECTIONS!");
  535|  			return;
  536|  #else
  537|  			int i;
  538|  			int64_t oldest = net->
  539|  			    tcp_connections[0].last_used_timestamp;
  540|  			free_con_id = 0;
  541|  
  542|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_WARNING,
  543|  			    "NO FREE TCP SLOTS, REUSING OLDEST ONE");
  544|  			for (i=0; i<MAX_TCP_CONNECTIONS; i++)
  545|  				if (net->tcp_connections[i].
  546|  				    last_used_timestamp < oldest) {
  547|  					oldest = net->tcp_connections[i].
  548|  					    last_used_timestamp;
  549|  					free_con_id = i;
  550|  				}
  551|  			tcp_closeconnection(net, free_con_id);
  552|  #endif
  553|  		}
  554|  
  555|  		con_id = free_con_id;
  556|  		memset(&net->tcp_connections[con_id], 0,
  557|  		    sizeof(struct tcp_connection));
  558|  
  559|  		memcpy(net->tcp_connections[con_id].ethernet_address,
  560|  		    packet + 6, 6);
  561|  		memcpy(net->tcp_connections[con_id].inside_ip_address,
  562|  		    packet + 26, 4);
  563|  		net->tcp_connections[con_id].inside_tcp_port = srcport;
  564|  		memcpy(net->tcp_connections[con_id].outside_ip_address,
  565|  		    packet + 30, 4);
  566|  		net->tcp_connections[con_id].outside_tcp_port = dstport;
  567|  
  568|  		net->tcp_connections[con_id].socket =
  569|  		    socket(AF_INET, SOCK_STREAM, 0);
  570|  		if (net->tcp_connections[con_id].socket < 0) {
  571|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_ERROR,
  572|  			    "socket() returned %i",
  573|  			    net->tcp_connections[con_id].socket);
  574|  			return;
  575|  		}
  576|  
  577|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  578|  		    "new tcp outgoing socket=%i",
  579|  		    net->tcp_connections[con_id].socket);
  580|  
  581|  		net->tcp_connections[con_id].in_use = 1;
  582|  
  583|  		/*  Set the socket to non-blocking:  */
  584|  		res = fcntl(net->tcp_connections[con_id].socket, F_GETFL);
  585|  		fcntl(net->tcp_connections[con_id].socket, F_SETFL,
  586|  		    res | O_NONBLOCK);
  587|  
  588|  		remote_ip.sin_family = AF_INET;
  589|  		memcpy((unsigned char *)&remote_ip.sin_addr,
  590|  		    net->tcp_connections[con_id].outside_ip_address, 4);
  591|  		remote_ip.sin_port = htons(
  592|  		    net->tcp_connections[con_id].outside_tcp_port);
  593|  
  594|  		res = connect(net->tcp_connections[con_id].socket,
  595|  		    (struct sockaddr *)&remote_ip, sizeof(remote_ip));
  596|  
  597|  		/*  connect can return -1, and errno = EINPROGRESS
  598|  		    as we might not have connected right away.  */
  599|+ 		if (res < 0 && errno != EINPROGRESS) {
  600|+ 			/* #NNN: reject connection immediately if connect fails */
  601|+ 			net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  602|+ 			tcp_closeconnection(net, con_id);
  603|+ 			return;
  604|+ 		}
  605|  
  606|  		net->tcp_connections[con_id].state =
  607|  		    TCP_OUTSIDE_TRYINGTOCONNECT;
  608|  
  609|  		net->tcp_connections[con_id].outside_acknr = 0;
  610|  		net->tcp_connections[con_id].outside_seqnr =
  611|  		    ((random() & 0xffff) << 16) + (random() & 0xffff);
  612|  	}
  613|  
  614|  	if (rst) {
  615|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  616|  		    "'rst': disconnecting TCP connection %i", con_id);
  617|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  618|  		tcp_closeconnection(net, con_id);
  619|  		return;
  620|  	}
  621|  
  622|  	if (ack && net->tcp_connections[con_id].state
  623|  	    == TCP_OUTSIDE_DISCONNECTED2) {
  624|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  625|  		    "'ack': guestOS's final termination of TCP "
  626|  		    "connection %i", con_id);
  627|  
  628|  		/*  Send an RST?  (TODO, this is wrong...)  */
  629|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  630|  
  631|  		/*  ... and forget about this connection:  */
  632|  		tcp_closeconnection(net, con_id);
  633|  		return;
  634|  	}
  635|  
  636|  	if (fin && net->tcp_connections[con_id].state
  637|  	    == TCP_OUTSIDE_DISCONNECTED) {
  638|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  639|  		    "'fin': response to outside's disconnection of "
  640|  		    "TCP connection %i", con_id);
  641|  
  642|  		/*  Send an ACK:  */
  643|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_CONNECTED;
  644|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  645|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_DISCONNECTED2;
  646|  		return;
  647|  	}
  648|  
  649|  	if (fin) {
  650|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  651|  		    "'fin': guestOS disconnecting TCP connection %i",
  652|  		    con_id);
  653|  
  654|  		/*  Send ACK:  */
  655|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  656|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_DISCONNECTED2;
  657|  
  658|  		/*  Return and send FIN:  */
  659|  		goto ret;
  660|  	}
  661|  
  662|  	if (ack) {
  663|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  664|  		    "ACK %i bytes, inside_acknr=%u outside_seqnr=%u",
     | [... lines 665-742 not shown ...]
  743|  			    TCP_OUTSIDE_DISCONNECTED;
  744|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  745|  			    "disconnect on select for writing");
  746|  			goto ret;
  747|  		}
  748|  
  749|  		res = write(net->tcp_connections[con_id].socket,
  750|  		    packet + send_ofs, len - send_ofs);
  751|  
  752|  		if (res > 0) {
  753|  			net->tcp_connections[con_id].outside_acknr += res;
  754|  		} else if (errno == EAGAIN) {
  755|  			/*  Just ignore this attempt.  */
  756|  			return;
  757|  		} else {
  758|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  759|  			    "error writing %i bytes to TCP connection %i:"
  760|  			    " errno = %i", len - send_ofs, con_id, errno);
  761|  			net->tcp_connections[con_id].state =
  762|  			    TCP_OUTSIDE_DISCONNECTED;
  763|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  764|  			    "disconnect on write()");
  765|  			goto ret;
  766|  		}
  767|  	}
  768|  
  769|  ret:
  770|  	/*  Send an ACK (or FIN) to the guest OS:  */
  771|  	net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  772|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_NATCONNFAIL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_NATCONNFAIL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
