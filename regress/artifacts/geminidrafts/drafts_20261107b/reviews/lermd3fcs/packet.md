# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `lermd3fcs` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `lermd3fcs`, state `open`)

**title:** devices/dev_le.c:le_rx -- RMD3 counts len+4 but only len bytes are copied, so the last 4 bytes of the guest buffer are stale -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T59 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A2-10).  Source URLs: https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556.  Our site at de8c7547: src/devices/dev_le.c:598.  Portable fix: yes -- port rpajarola d1f0720.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 598| rx_descr[3] |= d->rx_packet_len + 4;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_le.c b/src/devices/dev_le.c
index 922bc9b5..5ba1b0ab 100644
--- a/src/devices/dev_le.c
+++ b/src/devices/dev_le.c
@@ -571,17 +571,18 @@ static int le_rx(struct net *net, struct le_data *d)
 
 		/*  Copy data from the packet into SRAM:  */
 		for (i=0; i<buflen; i++) {
-			if (d->rx_packet_offset+(ssize_t)i >= d->rx_packet_len)
+			if (d->rx_packet_offset+(ssize_t)i >= d->rx_packet_len + 4)
 				break;
 			d->sram[(bufaddr + i) & (SRAM_SIZE-1)] =
-			    d->rx_packet[d->rx_packet_offset + i];
+			    (d->rx_packet_offset + i < d->rx_packet_len) ?
+			    d->rx_packet[d->rx_packet_offset + i] : 0;
 		}
 
 		/*  Here, i is the number of bytes copied.  */
 		d->rx_packet_offset += i;
 
 		/*  Set the ENP bit if this was the end of a packet:  */
-		if (d->rx_packet_offset >= d->rx_packet_len) {
+		if (d->rx_packet_offset >= d->rx_packet_len + 4) {
 			rx_descr[1] |= LE_ENP;
 
 			/*
```

## Every edited function, after the fix

### `src/devices/dev_le.c` -- post-edit lines 514-669 (`+` marks a line the diff added or the point of a deletion)

```c
  514|  static int le_rx(struct net *net, struct le_data *d)
  515|  {
  516|  	int start_rxp = d->rxp, rx_exhausted = 0;
  517|  	size_t i;
  518|  	uint16_t rx_descr[4];
  519|  	uint32_t bufaddr, buflen;
  520|  
  521|  	do {
  522|  		if (d->rx_packet == NULL)
  523|  			return 0;
  524|  
  525|  		/*  Load the 8 descriptor bytes:  */
  526|  		rx_descr[0] = le_read_16bit(d, d->rdra + d->rxp*8 + 0);
  527|  		rx_descr[1] = le_read_16bit(d, d->rdra + d->rxp*8 + 2);
  528|  		rx_descr[2] = le_read_16bit(d, d->rdra + d->rxp*8 + 4);
  529|  		rx_descr[3] = le_read_16bit(d, d->rdra + d->rxp*8 + 6);
  530|  
  531|  		bufaddr = rx_descr[0] + ((rx_descr[1] & 0xff) << 16);
  532|  		buflen = 4096 - (rx_descr[2] & 0xfff);
  533|  
  534|  		/*
  535|  		 *  Check the OWN bit. If it is zero, then this buffer is
  536|  		 *  not ready to receive data yet.
  537|  		 */
  538|  		if (!(rx_descr[1] & LE_OWN)) {
  539|  			/*  #262: No chip-owned descriptor is available to
  540|  			    start this frame.  Drop it and report MISS.  A
  541|  			    chained-buffer shortage is detected below, before
  542|  			    ownership of the current descriptor is released.  */
  543|  			le_rx_miss(d);
  544|  			return 1;
  545|  		}
  546|  
  547|  		/*
  548|  		 *  #274: The descriptor is owned by the chip, but it is not
  549|  		 *  usable.  The lookahead below only lets a frame continue
  550|  		 *  into a descriptor that this very test accepts, so this can
  551|  		 *  only be the FIRST buffer of a frame: nothing has been
  552|  		 *  filled in, and the descriptor is deliberately NOT written
  553|  		 *  back.  Drop the frame just like the exhaustion case above.
  554|  		 *  (The manual gives no status for a descriptor violating the
  555|  		 *  '1111' rule; reporting it as a missed packet is emulator
  556|  		 *  policy, not documented Am7990 behaviour.)
  557|  		 */
  558|  		if (!le_rx_descr_ok(rx_descr[2])) {
  559|  			debugmsg(d->subsys, "rx", VERBOSITY_WARNING,
  560|  			    "descr %i unusable (0x%04x, buflen = %i)",
  561|  			    d->rxp, rx_descr[2], buflen);
  562|  			le_rx_miss(d);
  563|  			return 1;
  564|  		}
  565|  
  566|  		debugmsg(d->subsys, "rx", VERBOSITY_DEBUG,
  567|  		    "descr %3i DUMP: 0x%04x 0x%04x 0x%04x 0x%04x "
  568|  		    "=> addr=0x%06x, len=%i bytes", d->rxp,
  569|  		    rx_descr[0], rx_descr[1], rx_descr[2], rx_descr[3],
  570|  		    bufaddr, buflen);
  571|  
  572|  		/*  Copy data from the packet into SRAM:  */
  573|  		for (i=0; i<buflen; i++) {
  574|+ 			if (d->rx_packet_offset+(ssize_t)i >= d->rx_packet_len + 4)
  575|  				break;
  576|  			d->sram[(bufaddr + i) & (SRAM_SIZE-1)] =
  577|+ 			    (d->rx_packet_offset + i < d->rx_packet_len) ?
  578|+ 			    d->rx_packet[d->rx_packet_offset + i] : 0;
  579|  		}
  580|  
  581|  		/*  Here, i is the number of bytes copied.  */
  582|  		d->rx_packet_offset += i;
  583|  
  584|  		/*  Set the ENP bit if this was the end of a packet:  */
  585|+ 		if (d->rx_packet_offset >= d->rx_packet_len + 4) {
  586|  			rx_descr[1] |= LE_ENP;
  587|  
  588|  			/*
  589|  			 *  NOTE:  The Lance documentation that I have read
  590|  			 *  says _NOTHING_ about the length being 4 more than
  591|  			 *  the length of the data.  You can guess how
  592|  			 *  surprised I was when I saw the following in
  593|  			 *  NetBSD (dev/ic/am7990.c):
  594|  			 *
  595|  			 *	lance_read(sc, LE_RBUFADDR(sc, bix),
  596|  			 *		(int)rmd.rmd3 - 4);
  597|  			 */
  598|  			rx_descr[3] &= ~0xfff;
  599|  			rx_descr[3] |= d->rx_packet_len + 4;
  600|  
  601|  			free(d->rx_packet);
  602|  			d->rx_packet = NULL;
  603|  			d->rx_packet_len = 0;
  604|  			d->rx_packet_offset = 0;
  605|  			d->rx_middle_bit = 0;
  606|  
  607|  			d->reg[0] |= LE_RINT;
  608|  		}
  609|  
  610|  		/*  Set the STP bit if this was the start of a packet:  */
  611|  		if (!d->rx_middle_bit) {
  612|  			rx_descr[1] |= LE_STP;
  613|  
  614|  			/*  Are we continuing on this packet?  */
  615|  			if (d->rx_packet != NULL)
  616|  				d->rx_middle_bit = 1;
  617|  		}
  618|  
  619|  		/*
  620|  		 *  #262: If this frame continues, look ahead while the current
  621|  		 *  descriptor is still chip-owned.  If the next descriptor is
  622|  		 *  unavailable, terminate this descriptor with ERR|BUFF and
  623|  		 *  no ENP.
  624|  		 */
  625|  		if (d->rx_packet != NULL) {
  626|  			int next_rxp = d->rxp + 1;
  627|  
  628|  			if (next_rxp >= d->rlen)
  629|  				next_rxp = 0;
  630|  			/*  #274: the next descriptor has to be usable, not
  631|  			    just chip-owned; a descriptor with a bad mark or
  632|  			    byte count cannot hold the rest of this frame.  */
  633|  			if (next_rxp == d->rxp ||
  634|  			    !(le_read_16bit(d,
  635|  			    d->rdra + next_rxp*8 + 2) & LE_OWN) ||
  636|  			    !le_rx_descr_ok(le_read_16bit(d,
  637|  			    d->rdra + next_rxp*8 + 4))) {
  638|  				rx_descr[1] |= LE_ERR | LE_RBUFF;
  639|  				free(d->rx_packet);
  640|  				d->rx_packet = NULL;
  641|  				d->rx_packet_len = 0;
  642|  				d->rx_packet_offset = 0;
  643|  				d->rx_middle_bit = 0;
  644|  				d->reg[0] |= LE_RINT;
  645|  				rx_exhausted = 1;
  646|  			}
  647|  		}
  648|  
  649|  		/*  Clear the OWN bit:  */
  650|  		rx_descr[1] &= ~LE_OWN;
  651|  
  652|  		/*  Write back the descriptor to SRAM:  */
  653|  		le_write_16bit(d, d->rdra + d->rxp*8 + 2, rx_descr[1]);
  654|  		le_write_16bit(d, d->rdra + d->rxp*8 + 4, rx_descr[2]);
  655|  		le_write_16bit(d, d->rdra + d->rxp*8 + 6, rx_descr[3]);
  656|  
  657|  		/*  Go to the next descriptor:  */
  658|  		d->rxp ++;
  659|  		if (d->rxp >= d->rlen)
  660|  			d->rxp = 0;
  661|  
  662|  		if (rx_exhausted)
  663|  			return 1;
  664|  	} while (d->rxp != start_rxp);
  665|  
  666|  	/*  We are here if all descriptors were taken care of.  */
  667|  	debugmsg(d->subsys, "rx", VERBOSITY_WARNING, "all descriptors used up?");
  668|  	return 0;
  669|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_LERMD3FCS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_LERMD3FCS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
