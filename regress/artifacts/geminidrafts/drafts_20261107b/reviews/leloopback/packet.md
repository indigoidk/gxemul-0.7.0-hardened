# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `leloopback` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `leloopback`, state `open`)

**title:** devices/dev_le.c:le_tx -- loopback mode (LOOP/INTL) is not modelled, so self-test frames go out to the network or tap -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T60 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-11).  Source URLs: https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556.  Our site at de8c7547: src/devices/dev_le.c:438, :74.  Portable fix: yes -- port rpajarola d1f0720.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 438| 			net_ethernet_tx(net, &d->nic, d->tx_packet,

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_le.c b/src/devices/dev_le.c
index 922bc9b5..17fd82b8 100644
--- a/src/devices/dev_le.c
+++ b/src/devices/dev_le.c
@@ -435,8 +435,10 @@ static void le_tx(struct net *net, struct le_data *d)
 		 *  the packet.
 		 */
 		if (enp) {
-			net_ethernet_tx(net, &d->nic, d->tx_packet,
-			    d->tx_packet_len);
+			/* #T60: do not send out self-test frames */
+			if (!(d->mode & LE_MODE_LOOP))
+				net_ethernet_tx(net, &d->nic, d->tx_packet,
+				    d->tx_packet_len);
 
 			free(d->tx_packet);
 			d->tx_packet = NULL;
```

## Every edited function, after the fix

### `src/devices/dev_le.c` -- post-edit lines 319-466 (`+` marks a line the diff added or the point of a deletion)

```c
  319|  static void le_tx(struct net *net, struct le_data *d)
  320|  {
  321|  	int start_txp = d->txp;
  322|  	uint16_t tx_descr[4];
  323|  	int stp, enp, cur_packet_offset;
  324|  	size_t i;
  325|  	uint32_t bufaddr, buflen;
  326|  
  327|  	/*  TODO: This is just a guess:  */
  328|  	d->reg[0] &= ~LE_TDMD;
  329|  
  330|  	do {
  331|  		/*  Load the 8 descriptor bytes:  */
  332|  		tx_descr[0] = le_read_16bit(d, d->tdra + d->txp*8 + 0);
  333|  		tx_descr[1] = le_read_16bit(d, d->tdra + d->txp*8 + 2);
  334|  		tx_descr[2] = le_read_16bit(d, d->tdra + d->txp*8 + 4);
  335|  		tx_descr[3] = le_read_16bit(d, d->tdra + d->txp*8 + 6);
  336|  
  337|  		bufaddr = tx_descr[0] + ((tx_descr[1] & 0xff) << 16);
  338|  		stp = tx_descr[1] & LE_STP? 1 : 0;
  339|  		enp = tx_descr[1] & LE_ENP? 1 : 0;
  340|  		buflen = 4096 - (tx_descr[2] & 0xfff);
  341|  
  342|  		/*
  343|  		 *  Check the OWN bit. If it is zero, then this buffer is
  344|  		 *  not ready to be transmitted yet.
  345|  		 */
  346|  		if (!(tx_descr[1] & LE_OWN))
  347|  			return;
  348|  
  349|  		/*
  350|  		 *  #275: The chip owns this buffer, but it is not the start of
  351|  		 *  a packet and no packet is in progress.  The Am7990 manual
  352|  		 *  (1986) section 4.5.2 says that the chip then "will simply
  353|  		 *  turn the ownership back over to the host", generate TINT,
  354|  		 *  and go on to the next buffer, without any error indication.
  355|  		 *
  356|  		 *  This has to be decided BEFORE the tmd2 checks below: while
  357|  		 *  polling, the chip reads the status word (tmd1) only, and
  358|  		 *  does not fetch the byte count from tmd2 until it has found
  359|  		 *  both OWN and STP set.
  360|  		 */
  361|  		if (d->tx_packet == NULL && !stp) {
  362|  			debugmsg(d->subsys, "tx", VERBOSITY_DEBUG,
  363|  			    "descr %3i skipped: !stp but tx_packet == NULL",
  364|  			    d->txp);
  365|  			tx_descr[1] &= ~LE_OWN;
  366|  			le_write_16bit(d, d->tdra + d->txp*8 + 2, tx_descr[1]);
  367|  			d->reg[0] |= LE_TINT;
  368|  			d->txp ++;
  369|  			if (d->txp >= d->tlen)
  370|  				d->txp = 0;
  371|  			continue;
  372|  		}
  373|  
  374|  		/*
  375|  		 *  Check the '1111' mark, and make sure that byte-count is
  376|  		 *  reasonable.  #275: a descriptor that fails these tests is
  377|  		 *  returned to the host with an error, instead of being kept
  378|  		 *  chip-owned forever with the guest waiting for it.
  379|  		 */
  380|  		if ((tx_descr[2] & 0xf000) != 0xf000) {
  381|  			le_tx_abort(d, tx_descr);
  382|  			return;
  383|  		}
  384|  		if (buflen < 12 || buflen > 1900) {
  385|  			debugmsg(d->subsys, "tx", VERBOSITY_WARNING, "buflen = %i", buflen);
  386|  			le_tx_abort(d, tx_descr);
  387|  			return;
  388|  		}
  389|  
  390|  		debugmsg(d->subsys, "tx", VERBOSITY_DEBUG,
  391|  		    "descr %3i DUMP: 0x%04x 0x%04x 0x%04x 0x%04x "
  392|  		    "=> addr=0x%06x, len=%i bytes, STP=%i ENP=%i", d->txp,
  393|  		    tx_descr[0], tx_descr[1], tx_descr[2], tx_descr[3],
  394|  		    bufaddr, buflen, stp, enp);
  395|  
  396|  		if (d->tx_packet != NULL && stp) {
  397|  			debugmsg(d->subsys, "tx", VERBOSITY_WARNING,
  398|  			    "stp but tx_packet != NULL");
  399|  			free(d->tx_packet);
  400|  			d->tx_packet = NULL;
  401|  			d->tx_packet_len = 0;
  402|  		}
  403|  
  404|  		/*  Where to write to in the tx_packet:  */
  405|  		cur_packet_offset = d->tx_packet_len;
  406|  
  407|  		/*  Start of a new packet:  */
  408|  		if (stp) {
  409|  			d->tx_packet_len = buflen;
  410|  			CHECK_ALLOCATION(d->tx_packet = (unsigned char *) malloc(buflen));
  411|  		} else {
  412|  			/*  #199: (Codex/Fable) cap the aggregate multi-fragment TX
  413|  			    packet so a guest rearming a non-ENP descriptor can't grow
  414|  			    host memory without bound.  #275: report the aborted frame
  415|  			    to the guest instead of holding the descriptor forever.  */
  416|  			if ((size_t)d->tx_packet_len + buflen > 65536) {
  417|  				le_tx_abort(d, tx_descr);
  418|  				return;
  419|  			}
  420|  			d->tx_packet_len += buflen;
  421|  			CHECK_ALLOCATION(d->tx_packet = (unsigned char *)
  422|  			    realloc(d->tx_packet, d->tx_packet_len));
  423|  		}
  424|  
  425|  		/*  Copy data from SRAM into the tx packet:  */
  426|  		for (i=0; i<buflen; i++) {
  427|  			unsigned char ch;
  428|  			ch = d->sram[(bufaddr + i) & (SRAM_SIZE-1)];
  429|  			d->tx_packet[cur_packet_offset + i] = ch;
  430|  		}
  431|  
  432|  		/*
  433|  		 *  Is this the last buffer in a packet? Then transmit
  434|  		 *  it, cause an interrupt, and free the memory used by
  435|  		 *  the packet.
  436|  		 */
  437|  		if (enp) {
  438|+ 			/* #T60: do not send out self-test frames */
  439|+ 			if (!(d->mode & LE_MODE_LOOP))
  440|+ 				net_ethernet_tx(net, &d->nic, d->tx_packet,
  441|+ 				    d->tx_packet_len);
  442|  
  443|  			free(d->tx_packet);
  444|  			d->tx_packet = NULL;
  445|  			d->tx_packet_len = 0;
  446|  
  447|  			d->reg[0] |= LE_TINT;
  448|  		}
  449|  
  450|  		/*  Clear the OWN bit:  */
  451|  		tx_descr[1] &= ~LE_OWN;
  452|  
  453|  		/*  Write back the descriptor to SRAM:  */
  454|  		le_write_16bit(d, d->tdra + d->txp*8 + 2, tx_descr[1]);
  455|  		le_write_16bit(d, d->tdra + d->txp*8 + 4, tx_descr[2]);
  456|  		le_write_16bit(d, d->tdra + d->txp*8 + 6, tx_descr[3]);
  457|  
  458|  		/*  Go to the next descriptor:  */
  459|  		d->txp ++;
  460|  		if (d->txp >= d->tlen)
  461|  			d->txp = 0;
  462|  	} while (d->txp != start_txp);
  463|  
  464|  	/*  We are here if all descriptors were taken care of.  */
  465|  	debugmsg(d->subsys, "tx", VERBOSITY_WARNING, "all descriptors used up?");
  466|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_LELOOPBACK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_LELOOPBACK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
