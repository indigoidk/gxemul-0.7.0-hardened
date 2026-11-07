# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `leloopback` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `leloopback`, state `open`)

**title:** devices/dev_le.c:le_tx -- loopback mode (LOOP/INTL) is not modelled, so self-test frames go out to the network or tap -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T60 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-11).  Source URLs: https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556.  Our site at de8c7547: src/devices/dev_le.c:438, :74.  Portable fix: yes -- port rpajarola d1f0720.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_le.c` -- AT HEAD, lines 319-464 (`*` marks a line your previous draft changed)

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
  438|* 			net_ethernet_tx(net, &d->nic, d->tx_packet,
  439|* 			    d->tx_packet_len);
  440|* 
  441|  			free(d->tx_packet);
  442|  			d->tx_packet = NULL;
  443|  			d->tx_packet_len = 0;
  444|  
  445|  			d->reg[0] |= LE_TINT;
  446|  		}
  447|  
  448|  		/*  Clear the OWN bit:  */
  449|  		tx_descr[1] &= ~LE_OWN;
  450|  
  451|  		/*  Write back the descriptor to SRAM:  */
  452|  		le_write_16bit(d, d->tdra + d->txp*8 + 2, tx_descr[1]);
  453|  		le_write_16bit(d, d->tdra + d->txp*8 + 4, tx_descr[2]);
  454|  		le_write_16bit(d, d->tdra + d->txp*8 + 6, tx_descr[3]);
  455|  
  456|  		/*  Go to the next descriptor:  */
  457|  		d->txp ++;
  458|  		if (d->txp >= d->tlen)
  459|  			d->txp = 0;
  460|  	} while (d->txp != start_txp);
  461|  
  462|  	/*  We are here if all descriptors were taken care of.  */
  463|  	debugmsg(d->subsys, "tx", VERBOSITY_WARNING, "all descriptors used up?");
  464|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_le.c` -- `struct le_data {` (HEAD lines 84-128)

```c
   84| struct le_data {
   85| 	struct nic_data	nic;
   86| 
   87| 	int		subsys;		/*  for debugmsg  */
   88| 
   89| 	struct interrupt irq;
   90| 	int		irq_asserted;
   91| 
   92| 	uint64_t	buf_start;
   93| 	uint64_t	buf_end;
   94| 	int		len;
   95| 
   96| 	uint8_t		rom[ROM_SIZE];
   97| 
   98| 	int		reg_select;
   99| 	uint16_t	reg[N_REGISTERS];
  100| 
  101| 	int		is_bigendian;
  102| 
  103| 	unsigned char	*sram;
  104| 
  105| 	/*  Initialization block:  */
  106| 	uint32_t	init_block_addr;
  107| 
  108| 	uint16_t	mode;
  109| 	uint16_t	ladrf[4];
  110| 	uint32_t	rdra;	/*  receive descriptor ring address  */
  111| 	int		rlen;	/*  nr of rx descriptors  */
  112| 	uint32_t	tdra;	/*  transmit descriptor ring address  */
  113| 	int		tlen;	/*  nr ot tx descriptors  */
  114| 
  115| 	int		allmulti;/* receive all multicast packets */
  116| 
  117| 	/*  Current rx and tx descriptor indices:  */
  118| 	int		rxp;
  119| 	int		txp;
  120| 
  121| 	unsigned char	*tx_packet;
  122| 	int		tx_packet_len;
  123| 
  124| 	unsigned char	*rx_packet;
  125| 	int		rx_packet_len;
  126| 	int		rx_packet_offset;
  127| 	int		rx_middle_bit;
  128| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_le.c",
    "old": "\t\tif (enp) {\n\t\t\tnet_ethernet_tx(net, &d->nic, d->tx_packet,\n\t\t\t    d->tx_packet_len);\n\n\t\t\tfree(d->tx_packet);",
    "new": "\t\tif (enp) {\n\t\t\t/* #T60: do not send out self-test frames */\n\t\t\tif (!(d->mode & LE_MODE_LOOP))\n\t\t\t\tnet_ethernet_tx(net, &d->nic, d->tx_packet,\n\t\t\t\t    d->tx_packet_len);\n\n\t\t\tfree(d->tx_packet);",
    "why": "Prevent frames from leaking to the network or tap when the device is in loopback mode."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_LELOOPBACK: DEFECT, 1 FINDINGS
1. The diff removes the defect at `src/devices/dev_le.c:438` but misses the other site named in the issue: `src/devices/dev_le.c:74`.
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit skips any code. The function's common tail remains intact.
3. RETURN VALUE: No path returns anything different; the function `le_tx` returns `void` and no new return statements are added.
4. ELSE: The diff changes nothing else. The memory is still freed and the interrupt (LE_TINT) is still asserted. 
5. House idioms: The new comment carries the required tag (`/* #T60: ... */`) and lines stay within 79 columns.
src/devices/dev_le.c:74: DEFECT: Site named in the issue is missing from the patch. UNSETTLED: The file `src/devices/dev_le.c` (around line 74) is missing, so a fix cannot be proposed.
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

End with two lines: `REVISION_LELOOPBACK: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_LELOOPBACK: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
