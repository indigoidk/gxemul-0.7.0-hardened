# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `natconnfail` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `natconnfail`, state `open`)

**title:** net/net_ip.c:net_ip_tcp/net_tcp_rx_avail -- a failed outgoing NAT connect() is reported to the guest as connected and then closed -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T81 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-53, A(c)#12).  Source URLs: https://github.com/rpajarola/gxemul/commit/1c18c2b1ddb90a62cd27c4873b436511d730383d.  Our site at de8c7547: src/net/net_ip.c:594-601, :1520-1552.  Portable fix: yes -- port rpajarola 1c18c2b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/net/net_ip.c` -- AT HEAD, lines 389-766 (`*` marks a line your previous draft changed)

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
  599|* 
  600|  		net->tcp_connections[con_id].state =
  601|  		    TCP_OUTSIDE_TRYINGTOCONNECT;
  602|  
  603|  		net->tcp_connections[con_id].outside_acknr = 0;
  604|  		net->tcp_connections[con_id].outside_seqnr =
  605|  		    ((random() & 0xffff) << 16) + (random() & 0xffff);
  606|  	}
  607|  
  608|  	if (rst) {
  609|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  610|  		    "'rst': disconnecting TCP connection %i", con_id);
  611|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  612|  		tcp_closeconnection(net, con_id);
  613|  		return;
  614|  	}
  615|  
  616|  	if (ack && net->tcp_connections[con_id].state
  617|  	    == TCP_OUTSIDE_DISCONNECTED2) {
  618|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  619|  		    "'ack': guestOS's final termination of TCP "
  620|  		    "connection %i", con_id);
  621|  
  622|  		/*  Send an RST?  (TODO, this is wrong...)  */
  623|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  624|  
  625|  		/*  ... and forget about this connection:  */
  626|  		tcp_closeconnection(net, con_id);
  627|  		return;
  628|  	}
  629|  
  630|  	if (fin && net->tcp_connections[con_id].state
  631|  	    == TCP_OUTSIDE_DISCONNECTED) {
  632|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  633|  		    "'fin': response to outside's disconnection of "
  634|  		    "TCP connection %i", con_id);
  635|  
  636|  		/*  Send an ACK:  */
  637|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_CONNECTED;
  638|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  639|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_DISCONNECTED2;
  640|  		return;
  641|  	}
  642|  
  643|  	if (fin) {
  644|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  645|  		    "'fin': guestOS disconnecting TCP connection %i",
  646|  		    con_id);
  647|  
  648|  		/*  Send ACK:  */
  649|  		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  650|  		net->tcp_connections[con_id].state = TCP_OUTSIDE_DISCONNECTED2;
  651|  
  652|  		/*  Return and send FIN:  */
  653|  		goto ret;
  654|  	}
  655|  
  656|  	if (ack) {
  657|  		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  658|  		    "ACK %i bytes, inside_acknr=%u outside_seqnr=%u",
  659|  		    net->tcp_connections[con_id].incoming_buf_len,
     | [... lines 660-736 not shown ...]
  737|  			    TCP_OUTSIDE_DISCONNECTED;
  738|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  739|  			    "disconnect on select for writing");
  740|  			goto ret;
  741|  		}
  742|  
  743|  		res = write(net->tcp_connections[con_id].socket,
  744|  		    packet + send_ofs, len - send_ofs);
  745|  
  746|  		if (res > 0) {
  747|  			net->tcp_connections[con_id].outside_acknr += res;
  748|  		} else if (errno == EAGAIN) {
  749|  			/*  Just ignore this attempt.  */
  750|  			return;
  751|  		} else {
  752|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  753|  			    "error writing %i bytes to TCP connection %i:"
  754|  			    " errno = %i", len - send_ofs, con_id, errno);
  755|  			net->tcp_connections[con_id].state =
  756|  			    TCP_OUTSIDE_DISCONNECTED;
  757|  			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  758|  			    "disconnect on write()");
  759|  			goto ret;
  760|  		}
  761|  	}
  762|  
  763|  ret:
  764|  	/*  Send an ACK (or FIN) to the guest OS:  */
  765|  	net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  766|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/net/net_ip.c",
    "old": "\t\tres = connect(net->tcp_connections[con_id].socket,\n\t\t    (struct sockaddr *)&remote_ip, sizeof(remote_ip));\n\n\t\t/*  connect can return -1, and errno = EINPROGRESS\n\t\t    as we might not have connected right away.  */\n\n\t\tnet->tcp_connections[con_id].state =\n\t\t    TCP_OUTSIDE_TRYINGTOCONNECT;",
    "new": "\t\tres = connect(net->tcp_connections[con_id].socket,\n\t\t    (struct sockaddr *)&remote_ip, sizeof(remote_ip));\n\n\t\t/*  connect can return -1, and errno = EINPROGRESS\n\t\t    as we might not have connected right away.  */\n\t\tif (res < 0) {\n\t\t\t/* #NNN: immediate failure handled generically, skipping errno for now due to scope */\n\t\t\tnet_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);\n\t\t\ttcp_closeconnection(net, con_id);\n\t\t\treturn;\n\t\t}\n\n\t\tnet->tcp_connections[con_id].state =\n\t\t    TCP_OUTSIDE_TRYINGTOCONNECT;",
    "why": "Prevent failed connect() from advancing state, rejecting immediately if it returns an error."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_NATCONNFAIL: DEFECT, 3 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.
No. The diff only patches around line 596. It entirely misses the second site named in the issue description: `src/net/net_ip.c:1520-1552`.
Finding 1: `src/net/net_ip.c:1520-1552`, UNSETTLED, missing lines `1520-1552` to verify what was missed at the second site.
2. CONTROL FLOW: does any added return, goto, break or early exit skip code the function would otherwise run -- above all its COMMON TAIL? Quote the tail line it skips.
Yes, the early `return;` at line 603 skips the function's common tail, although it does manually write an RST result (`net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);`) before returning.
Finding 2: `src/net/net_ip.c:603`, QUESTION, skips tail line `771| 	net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);`.
3. RETURN VALUE: does any path now return something different? Say what the shown code implies the value means.
No. The signature for `net_ip_tcp` implies it returns `void` (deduced from the isolated `return;` statement). No path returns a different value.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one -- beyond removing the defect?
Because the socket is explicitly set to non-blocking (line 586), `connect()` will almost always return `-1` and set `errno = EINPROGRESS`. The diff's `if (res < 0)` blindly intercepts this normal asynchronous pending state and immediately aborts the connection. This breaks all legitimate asynchronous connections.
Finding 3: `src/net/net_ip.c:599`, DEFECT, fix: `if (res < 0 && errno != EINPROGRESS) {`
5. House idioms:
The code complies with house idioms. The comment correctly carries the `/* #NNN: ... */` tag, lines stay within 79 columns, and no latching diagnostics were added.
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

End with two lines: `REVISION_NATCONNFAIL: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_NATCONNFAIL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
