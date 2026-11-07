# GXemul hardened fork -- DRAFT A FIX for one filed issue, `leloopback` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `leloopback`, state `open`, severity `MED`)

**title:** devices/dev_le.c:le_tx -- loopback mode (LOOP/INTL) is not modelled, so self-test frames go out to the network or tap -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T60 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A2-11).  Source URLs: https://github.com/rpajarola/gxemul/commit/d1f0720ac94c3a261bbecca8e870addc9c106556.  Our site at de8c7547: src/devices/dev_le.c:438, :74.  Portable fix: yes -- port rpajarola d1f0720.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola d1f0720

## The code at the cited lines

### `src/devices/dev_le.c` around the row's cited line 438 (HEAD d2a6f233, lines 393-483)

```c
  393| 		    tx_descr[0], tx_descr[1], tx_descr[2], tx_descr[3],
  394| 		    bufaddr, buflen, stp, enp);
  395| 
  396| 		if (d->tx_packet != NULL && stp) {
  397| 			debugmsg(d->subsys, "tx", VERBOSITY_WARNING,
  398| 			    "stp but tx_packet != NULL");
  399| 			free(d->tx_packet);
  400| 			d->tx_packet = NULL;
  401| 			d->tx_packet_len = 0;
  402| 		}
  403| 
  404| 		/*  Where to write to in the tx_packet:  */
  405| 		cur_packet_offset = d->tx_packet_len;
  406| 
  407| 		/*  Start of a new packet:  */
  408| 		if (stp) {
  409| 			d->tx_packet_len = buflen;
  410| 			CHECK_ALLOCATION(d->tx_packet = (unsigned char *) malloc(buflen));
  411| 		} else {
  412| 			/*  #199: (Codex/Fable) cap the aggregate multi-fragment TX
  413| 			    packet so a guest rearming a non-ENP descriptor can't grow
  414| 			    host memory without bound.  #275: report the aborted frame
  415| 			    to the guest instead of holding the descriptor forever.  */
  416| 			if ((size_t)d->tx_packet_len + buflen > 65536) {
  417| 				le_tx_abort(d, tx_descr);
  418| 				return;
  419| 			}
  420| 			d->tx_packet_len += buflen;
  421| 			CHECK_ALLOCATION(d->tx_packet = (unsigned char *)
  422| 			    realloc(d->tx_packet, d->tx_packet_len));
  423| 		}
  424| 
  425| 		/*  Copy data from SRAM into the tx packet:  */
  426| 		for (i=0; i<buflen; i++) {
  427| 			unsigned char ch;
  428| 			ch = d->sram[(bufaddr + i) & (SRAM_SIZE-1)];
  429| 			d->tx_packet[cur_packet_offset + i] = ch;
  430| 		}
  431| 
  432| 		/*
  433| 		 *  Is this the last buffer in a packet? Then transmit
  434| 		 *  it, cause an interrupt, and free the memory used by
  435| 		 *  the packet.
  436| 		 */
  437| 		if (enp) {
  438| 			net_ethernet_tx(net, &d->nic, d->tx_packet,
  439| 			    d->tx_packet_len);
  440| 
  441| 			free(d->tx_packet);
  442| 			d->tx_packet = NULL;
  443| 			d->tx_packet_len = 0;
  444| 
  445| 			d->reg[0] |= LE_TINT;
  446| 		}
  447| 
  448| 		/*  Clear the OWN bit:  */
  449| 		tx_descr[1] &= ~LE_OWN;
  450| 
  451| 		/*  Write back the descriptor to SRAM:  */
  452| 		le_write_16bit(d, d->tdra + d->txp*8 + 2, tx_descr[1]);
  453| 		le_write_16bit(d, d->tdra + d->txp*8 + 4, tx_descr[2]);
  454| 		le_write_16bit(d, d->tdra + d->txp*8 + 6, tx_descr[3]);
  455| 
  456| 		/*  Go to the next descriptor:  */
  457| 		d->txp ++;
  458| 		if (d->txp >= d->tlen)
  459| 			d->txp = 0;
  460| 	} while (d->txp != start_txp);
  461| 
  462| 	/*  We are here if all descriptors were taken care of.  */
  463| 	debugmsg(d->subsys, "tx", VERBOSITY_WARNING, "all descriptors used up?");
  464| }
  465| 
  466| 
  467| /*
  468|  *  le_rx_descr_ok():
  469|  *
  470|  *  #274: Can a receive descriptor be used?  It has to carry the '1111' mark,
  471|  *  and its byte count has to be reasonable.  The very same predicate is used
  472|  *  both for the descriptor that is about to be filled in and for the lookahead
  473|  *  at the next one, so that the two cannot drift apart.  (rx_descr2 is the
  474|  *  descriptor word at offset 4.)
  475|  */
  476| static int le_rx_descr_ok(uint16_t rx_descr2)
  477| {
  478| 	uint32_t buflen = 4096 - (rx_descr2 & 0xfff);
  479| 
  480| 	if ((rx_descr2 & 0xf000) != 0xf000)
  481| 		return 0;
  482| 	if (buflen < 12 || buflen > 1900)
  483| 		return 0;
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

End with one line: `FIXDRAFT_LELOOPBACK: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
