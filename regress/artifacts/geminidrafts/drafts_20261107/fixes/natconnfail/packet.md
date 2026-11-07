# GXemul hardened fork -- DRAFT A FIX for one filed issue, `natconnfail` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `natconnfail`, state `open`, severity `MED`)

**title:** net/net_ip.c:net_ip_tcp/net_tcp_rx_avail -- a failed outgoing NAT connect() is reported to the guest as connected and then closed -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T81 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-53, A(c)#12).  Source URLs: https://github.com/rpajarola/gxemul/commit/1c18c2b1ddb90a62cd27c4873b436511d730383d.  Our site at de8c7547: src/net/net_ip.c:594-601, :1520-1552.  Portable fix: yes -- port rpajarola 1c18c2b.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola 1c18c2b

## The code at the cited lines

### `src/net/net_ip.c` around the row's cited line 594 (HEAD d2a6f233, lines 549-639)

```c
  549| 					free_con_id = i;
  550| 				}
  551| 			tcp_closeconnection(net, free_con_id);
  552| #endif
  553| 		}
  554| 
  555| 		con_id = free_con_id;
  556| 		memset(&net->tcp_connections[con_id], 0,
  557| 		    sizeof(struct tcp_connection));
  558| 
  559| 		memcpy(net->tcp_connections[con_id].ethernet_address,
  560| 		    packet + 6, 6);
  561| 		memcpy(net->tcp_connections[con_id].inside_ip_address,
  562| 		    packet + 26, 4);
  563| 		net->tcp_connections[con_id].inside_tcp_port = srcport;
  564| 		memcpy(net->tcp_connections[con_id].outside_ip_address,
  565| 		    packet + 30, 4);
  566| 		net->tcp_connections[con_id].outside_tcp_port = dstport;
  567| 
  568| 		net->tcp_connections[con_id].socket =
  569| 		    socket(AF_INET, SOCK_STREAM, 0);
  570| 		if (net->tcp_connections[con_id].socket < 0) {
  571| 			debugmsg(SUBSYS_NET, "TCP", VERBOSITY_ERROR,
  572| 			    "socket() returned %i",
  573| 			    net->tcp_connections[con_id].socket);
  574| 			return;
  575| 		}
  576| 
  577| 		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  578| 		    "new tcp outgoing socket=%i",
  579| 		    net->tcp_connections[con_id].socket);
  580| 
  581| 		net->tcp_connections[con_id].in_use = 1;
  582| 
  583| 		/*  Set the socket to non-blocking:  */
  584| 		res = fcntl(net->tcp_connections[con_id].socket, F_GETFL);
  585| 		fcntl(net->tcp_connections[con_id].socket, F_SETFL,
  586| 		    res | O_NONBLOCK);
  587| 
  588| 		remote_ip.sin_family = AF_INET;
  589| 		memcpy((unsigned char *)&remote_ip.sin_addr,
  590| 		    net->tcp_connections[con_id].outside_ip_address, 4);
  591| 		remote_ip.sin_port = htons(
  592| 		    net->tcp_connections[con_id].outside_tcp_port);
  593| 
  594| 		res = connect(net->tcp_connections[con_id].socket,
  595| 		    (struct sockaddr *)&remote_ip, sizeof(remote_ip));
  596| 
  597| 		/*  connect can return -1, and errno = EINPROGRESS
  598| 		    as we might not have connected right away.  */
  599| 
  600| 		net->tcp_connections[con_id].state =
  601| 		    TCP_OUTSIDE_TRYINGTOCONNECT;
  602| 
  603| 		net->tcp_connections[con_id].outside_acknr = 0;
  604| 		net->tcp_connections[con_id].outside_seqnr =
  605| 		    ((random() & 0xffff) << 16) + (random() & 0xffff);
  606| 	}
  607| 
  608| 	if (rst) {
  609| 		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  610| 		    "'rst': disconnecting TCP connection %i", con_id);
  611| 		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  612| 		tcp_closeconnection(net, con_id);
  613| 		return;
  614| 	}
  615| 
  616| 	if (ack && net->tcp_connections[con_id].state
  617| 	    == TCP_OUTSIDE_DISCONNECTED2) {
  618| 		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  619| 		    "'ack': guestOS's final termination of TCP "
  620| 		    "connection %i", con_id);
  621| 
  622| 		/*  Send an RST?  (TODO, this is wrong...)  */
  623| 		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 1);
  624| 
  625| 		/*  ... and forget about this connection:  */
  626| 		tcp_closeconnection(net, con_id);
  627| 		return;
  628| 	}
  629| 
  630| 	if (fin && net->tcp_connections[con_id].state
  631| 	    == TCP_OUTSIDE_DISCONNECTED) {
  632| 		debugmsg(SUBSYS_NET, "TCP", VERBOSITY_DEBUG,
  633| 		    "'fin': response to outside's disconnection of "
  634| 		    "TCP connection %i", con_id);
  635| 
  636| 		/*  Send an ACK:  */
  637| 		net->tcp_connections[con_id].state = TCP_OUTSIDE_CONNECTED;
  638| 		net_ip_tcp_connectionreply(net, nic, con_id, 0, NULL, 0, 0);
  639| 		net->tcp_connections[con_id].state = TCP_OUTSIDE_DISCONNECTED2;
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

End with one line: `FIXDRAFT_NATCONNFAIL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
