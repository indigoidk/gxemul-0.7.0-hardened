# GXemul hardened fork -- DRAFT A FIX for one filed issue, `lermd3fcs` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `lermd3fcs`, state `open`, severity `MED`)

**title:** devices/dev_le.c:le_rx -- RMD3 counts len+4 but only len bytes are copied, so the last 4 bytes of the guest buffer are stale -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T59 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-10).  Source URLs: https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556.  Our site at de8c7547: src/devices/dev_le.c:598.  Portable fix: yes -- port rpajarola d1f0720.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola d1f0720

## The code at the cited lines

### `src/devices/dev_le.c` around the row's cited line 598 (HEAD 2d25df65, lines 553-643)

```c
  553| 		 *  back.  Drop the frame just like the exhaustion case above.
  554| 		 *  (The manual gives no status for a descriptor violating the
  555| 		 *  '1111' rule; reporting it as a missed packet is emulator
  556| 		 *  policy, not documented Am7990 behaviour.)
  557| 		 */
  558| 		if (!le_rx_descr_ok(rx_descr[2])) {
  559| 			debugmsg(d->subsys, "rx", VERBOSITY_WARNING,
  560| 			    "descr %i unusable (0x%04x, buflen = %i)",
  561| 			    d->rxp, rx_descr[2], buflen);
  562| 			le_rx_miss(d);
  563| 			return 1;
  564| 		}
  565| 
  566| 		debugmsg(d->subsys, "rx", VERBOSITY_DEBUG,
  567| 		    "descr %3i DUMP: 0x%04x 0x%04x 0x%04x 0x%04x "
  568| 		    "=> addr=0x%06x, len=%i bytes", d->rxp,
  569| 		    rx_descr[0], rx_descr[1], rx_descr[2], rx_descr[3],
  570| 		    bufaddr, buflen);
  571| 
  572| 		/*  Copy data from the packet into SRAM:  */
  573| 		for (i=0; i<buflen; i++) {
  574| 			if (d->rx_packet_offset+(ssize_t)i >= d->rx_packet_len)
  575| 				break;
  576| 			d->sram[(bufaddr + i) & (SRAM_SIZE-1)] =
  577| 			    d->rx_packet[d->rx_packet_offset + i];
  578| 		}
  579| 
  580| 		/*  Here, i is the number of bytes copied.  */
  581| 		d->rx_packet_offset += i;
  582| 
  583| 		/*  Set the ENP bit if this was the end of a packet:  */
  584| 		if (d->rx_packet_offset >= d->rx_packet_len) {
  585| 			rx_descr[1] |= LE_ENP;
  586| 
  587| 			/*
  588| 			 *  NOTE:  The Lance documentation that I have read
  589| 			 *  says _NOTHING_ about the length being 4 more than
  590| 			 *  the length of the data.  You can guess how
  591| 			 *  surprised I was when I saw the following in
  592| 			 *  NetBSD (dev/ic/am7990.c):
  593| 			 *
  594| 			 *	lance_read(sc, LE_RBUFADDR(sc, bix),
  595| 			 *		(int)rmd.rmd3 - 4);
  596| 			 */
  597| 			rx_descr[3] &= ~0xfff;
  598| 			rx_descr[3] |= d->rx_packet_len + 4;
  599| 
  600| 			free(d->rx_packet);
  601| 			d->rx_packet = NULL;
  602| 			d->rx_packet_len = 0;
  603| 			d->rx_packet_offset = 0;
  604| 			d->rx_middle_bit = 0;
  605| 
  606| 			d->reg[0] |= LE_RINT;
  607| 		}
  608| 
  609| 		/*  Set the STP bit if this was the start of a packet:  */
  610| 		if (!d->rx_middle_bit) {
  611| 			rx_descr[1] |= LE_STP;
  612| 
  613| 			/*  Are we continuing on this packet?  */
  614| 			if (d->rx_packet != NULL)
  615| 				d->rx_middle_bit = 1;
  616| 		}
  617| 
  618| 		/*
  619| 		 *  #262: If this frame continues, look ahead while the current
  620| 		 *  descriptor is still chip-owned.  If the next descriptor is
  621| 		 *  unavailable, terminate this descriptor with ERR|BUFF and
  622| 		 *  no ENP.
  623| 		 */
  624| 		if (d->rx_packet != NULL) {
  625| 			int next_rxp = d->rxp + 1;
  626| 
  627| 			if (next_rxp >= d->rlen)
  628| 				next_rxp = 0;
  629| 			/*  #274: the next descriptor has to be usable, not
  630| 			    just chip-owned; a descriptor with a bad mark or
  631| 			    byte count cannot hold the rest of this frame.  */
  632| 			if (next_rxp == d->rxp ||
  633| 			    !(le_read_16bit(d,
  634| 			    d->rdra + next_rxp*8 + 2) & LE_OWN) ||
  635| 			    !le_rx_descr_ok(le_read_16bit(d,
  636| 			    d->rdra + next_rxp*8 + 4))) {
  637| 				rx_descr[1] |= LE_ERR | LE_RBUFF;
  638| 				free(d->rx_packet);
  639| 				d->rx_packet = NULL;
  640| 				d->rx_packet_len = 0;
  641| 				d->rx_packet_offset = 0;
  642| 				d->rx_middle_bit = 0;
  643| 				d->reg[0] |= LE_RINT;
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

End with one line: `FIXDRAFT_LERMD3FCS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
