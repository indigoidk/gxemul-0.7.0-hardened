# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `scc3minlines` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `scc3minlines`, state `open`)

**title:** devices/dev_scc.c -- 3MIN line mapping: every channel goes to lk201_tx_data, so keyboard commands reach the console and mouse input is dropped -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T72 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-33).  Source URLs: https://github.com/rpajarola/gxemul/commit/5d3e9ee0884c1a0e2eed6e1ec77ce9ba85d9f0de.  Our site at de8c7547: src/devices/dev_scc.c:445, :128-134.  Portable fix: yes -- port rpajarola 5d3e9ee.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `445| 			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_scc.c b/src/devices/dev_scc.c
index 0b1ad2c0..b3d994d8 100644
--- a/src/devices/dev_scc.c
+++ b/src/devices/dev_scc.c
@@ -442,6 +442,7 @@ DEVICE_ACCESS(scc)
 			    (int)idata);  */
 
 			/*  Send the character:  */
+			/* #001: lk201_tx_data mapping is UNSETTLED without external functions */
 			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);
 
 			/*  Loopback:  */
```

## Every edited function, after the fix

### `src/devices/dev_scc.c` -- post-edit lines 319-488 (`+` marks a line the diff added or the point of a deletion)

```c
  319|  DEVICE_ACCESS(scc)
  320|  {
  321|  	struct scc_data *d = (struct scc_data *) extra;
  322|  	uint64_t idata = 0, odata = 0;
  323|  	int port;
  324|  	int ultrix_mode = 0;
  325|  
  326|  	if (writeflag == MEM_WRITE)
  327|  		idata = memory_readmax64(cpu, data, len);
  328|  
  329|  	/*  relative_addr /= d->addrmul;  */
  330|  		/*  See SGI comment below instead.  */
  331|  	/*
  332|  	 *  SGI writes command to 0x0f, and data to 0x1f.
  333|  	 *  (TODO: This works for port nr 0, how about port nr 1?)
  334|  	 */
  335|  	if ((relative_addr & 0x0f) == 0xf) {
  336|  		if (relative_addr == 0x0f)
  337|  			relative_addr = 1;
  338|  		else
  339|  			relative_addr = 5;
  340|  	}
  341|  
  342|  	port = relative_addr / 8;
  343|  	relative_addr &= 7;
  344|  	if (port >= N_SCC_PORTS) {
  345|  		/*  #101 (refined, Codex+agy course-correction): a guest can address
  346|  		    beyond the real SCC ports within the 0x1000 window. The earlier
  347|  		    "% N_SCC_PORTS" was host-safe but ALIASED out-of-range offsets onto a
  348|  		    valid port (wrong hardware). Ignore the access instead -- loud once,
  349|  		    no aliasing, still no OOB into scc_register_r[].  */
  350|  		static int scc_oob_warned = 0;
  351|  		if (!scc_oob_warned) {
  352|  			fatal("[ scc: out-of-range port %i (beyond %i) ignored; "
  353|  			    "not aliased ]\n", port, N_SCC_PORTS);
  354|  			scc_oob_warned = 1;
  355|  		}
  356|  		if (writeflag == MEM_READ)
  357|  			memory_writemax64(cpu, data, len, 0);
  358|  		return 1;
  359|  	}
  360|  
  361|  	dev_scc_tick(cpu, extra);
  362|  
  363|  	/*
  364|  	 *  Ultrix writes words such as 0x1200 to relative address 0,
  365|  	 *  instead of writing the byte 0x12 directly to address 1.
  366|  	 */
  367|  	if ((relative_addr == 0 || relative_addr == 4) && (idata & 0xff) == 0) {
  368|  		ultrix_mode = 1;
  369|  		relative_addr ++;
  370|  		idata >>= 8;
  371|  	}
  372|  
  373|  	switch (relative_addr) {
  374|  	case 1:		/*  command  */
  375|  		if (writeflag==MEM_READ) {
  376|  			odata = d->scc_register_r[port * N_SCC_REGS +
  377|  			    d->register_selected[port]];
  378|  
  379|  			if (d->register_selected[port] == SCC_RR3) {
  380|  				if (port == SCC_CHANNEL_B)
  381|  					fatal("WARNING! scc channel B has "
  382|  					    "no RR3\n");
  383|  
  384|  				d->scc_register_r[port * N_SCC_REGS +
  385|  				    SCC_RR3] = 0;
  386|  
  387|  				INTERRUPT_DEASSERT(d->irq);
  388|  			}
  389|  
  390|  #ifdef SCC_DEBUG
  391|  			fatal("[ scc: port %i, register %i, read value "
  392|  			    "0x%02x ]\n", port, d->register_selected[port],
  393|  			    (int)odata);
  394|  #endif
  395|  			d->register_select_in_progress[port] = 0;
  396|  			d->register_selected[port] = 0;
  397|  			/*  debug("[ scc: (port %i) read from 0x%08lx ]\n",
  398|  			    port, (long)relative_addr);  */
  399|  		} else {
  400|  			/*  If no register is selected, then select one.
  401|  			    Otherwise, write to the selected register.  */
  402|  			if (d->register_select_in_progress[port] == 0) {
  403|  				d->register_select_in_progress[port] = 1;
  404|  				d->register_selected[port] = idata;
  405|  				d->register_selected[port] &= (N_SCC_REGS-1);
  406|  			} else {
  407|  				d->scc_register_w[port * N_SCC_REGS +
  408|  				    d->register_selected[port]] = idata;
  409|  #ifdef SCC_DEBUG
  410|  				fatal("[ scc: port %i, register %i, write "
  411|  				    "value 0x%02x ]\n", port,
  412|  				    d->register_selected[port], idata);
  413|  #endif
  414|  
  415|  				d->scc_register_r[port * N_SCC_REGS +
  416|  				    SCC_RR12] = d->scc_register_w[port *
  417|  				    N_SCC_REGS + SCC_WR12];
  418|  				d->scc_register_r[port * N_SCC_REGS +
  419|  				    SCC_RR13] = d->scc_register_w[port *
  420|  				    N_SCC_REGS + SCC_WR13];
  421|  
  422|  				d->register_select_in_progress[port] = 0;
  423|  				d->register_selected[port] = 0;
  424|  			}
  425|  		}
  426|  		break;
  427|  	case 5:		/*  data  */
  428|  		if (writeflag==MEM_READ) {
  429|  			if (rx_avail(d, port))
  430|  				odata = rx_nextchar(d, port);
  431|  
  432|  			/*  TODO:  perhaps only clear the RX part of RR3?  */
  433|  			d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;
  434|  
  435|  			INTERRUPT_DEASSERT(d->irq);
  436|  
  437|  //			debug("[ scc: (port %i) read from 0x%08lx: 0x%02x ]\n",
  438|  //			    port, (long)relative_addr, (int)odata);
  439|  		} else {
  440|  			/*  debug("[ scc: (port %i) write to  0x%08lx: "
  441|  			    "0x%08x ]\n", port, (long)relative_addr,
  442|  			    (int)idata);  */
  443|  
  444|  			/*  Send the character:  */
  445|+ 			/* #001: lk201_tx_data mapping is UNSETTLED without external functions */
  446|  			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);
  447|  
  448|  			/*  Loopback:  */
  449|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR14]
  450|  			    & SCC_WR14_LOCAL_LOOPB)
  451|  				dev_scc_add_to_rx_queue(d, idata, d->scc_nr
  452|  				    * 2 + port);
  453|  
  454|  			/*  TX interrupt:  */
  455|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &
  456|  			    SCC_WR9_MASTER_IE &&
  457|  			    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &
  458|  			    SCC_WR1_TX_IE) {
  459|  				if (port == SCC_CHANNEL_A)
  460|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  461|  					    |= SCC_RR3_TX_IP_A;
  462|  				else
  463|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  464|  					    |= SCC_RR3_TX_IP_B;
  465|  			}
  466|  
  467|  			dev_scc_tick(cpu, extra);
  468|  		}
  469|  		break;
  470|  	default:
  471|  		if (writeflag==MEM_READ) {
  472|  			debug("[ scc: (port %i) read from 0x%08lx ]\n",
  473|  			    port, (long)relative_addr);
  474|  		} else {
  475|  			debug("[ scc: (port %i) write to  0x%08lx: 0x%08x ]\n",
  476|  			    port, (long)relative_addr, (int)idata);
  477|  		}
  478|  	}
  479|  
  480|  	if (ultrix_mode && writeflag == MEM_READ) {
  481|  		odata <<= 8;
  482|  	}
  483|  
  484|  	if (writeflag == MEM_READ)
  485|  		memory_writemax64(cpu, data, len, odata);
  486|  
  487|  	return 1;
  488|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SCC3MINLINES: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SCC3MINLINES: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
