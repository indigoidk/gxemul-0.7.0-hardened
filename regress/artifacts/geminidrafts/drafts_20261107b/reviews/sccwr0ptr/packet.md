# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `sccwr0ptr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `sccwr0ptr`, state `open`)

**title:** devices/dev_scc.c:DEVICE_ACCESS(scc) -- the WR0 register pointer is the whole byte & 15 and WR0 commands are not decoded -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T68 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-29).  Source URLs: https://github.com/rpajarola/gxemul/commit/2dfd6ec32be07d7dd38a707f66742de3e2023ed3.  Our site at de8c7547: src/devices/dev_scc.c:402-405.  Portable fix: yes -- port rpajarola 2dfd6ec.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/devices/dev_scc.c:402

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_scc.c b/src/devices/dev_scc.c
index 0b1ad2c0..a202bed2 100644
--- a/src/devices/dev_scc.c
+++ b/src/devices/dev_scc.c
@@ -400,9 +400,11 @@ DEVICE_ACCESS(scc)
 			/*  If no register is selected, then select one.
 			    Otherwise, write to the selected register.  */
 			if (d->register_select_in_progress[port] == 0) {
-				d->register_select_in_progress[port] = 1;
-				d->register_selected[port] = idata;
+				/* #sccwr0ptr: extract register pointer, cmds not decoded yet */
+				d->register_selected[port] = idata & 0x0f;
 				d->register_selected[port] &= (N_SCC_REGS-1);
+				d->register_select_in_progress[port] =
+				    (d->register_selected[port] != 0);
 			} else {
 				d->scc_register_w[port * N_SCC_REGS +
 				    d->register_selected[port]] = idata;
```

## Every edited function, after the fix

### `src/devices/dev_scc.c` -- post-edit lines 319-489 (`+` marks a line the diff added or the point of a deletion)

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
  403|+ 				/* #sccwr0ptr: extract register pointer, cmds not decoded yet */
  404|+ 				d->register_selected[port] = idata & 0x0f;
  405|  				d->register_selected[port] &= (N_SCC_REGS-1);
  406|+ 				d->register_select_in_progress[port] =
  407|+ 				    (d->register_selected[port] != 0);
  408|  			} else {
  409|  				d->scc_register_w[port * N_SCC_REGS +
  410|  				    d->register_selected[port]] = idata;
  411|  #ifdef SCC_DEBUG
  412|  				fatal("[ scc: port %i, register %i, write "
  413|  				    "value 0x%02x ]\n", port,
  414|  				    d->register_selected[port], idata);
  415|  #endif
  416|  
  417|  				d->scc_register_r[port * N_SCC_REGS +
  418|  				    SCC_RR12] = d->scc_register_w[port *
  419|  				    N_SCC_REGS + SCC_WR12];
  420|  				d->scc_register_r[port * N_SCC_REGS +
  421|  				    SCC_RR13] = d->scc_register_w[port *
  422|  				    N_SCC_REGS + SCC_WR13];
  423|  
  424|  				d->register_select_in_progress[port] = 0;
  425|  				d->register_selected[port] = 0;
  426|  			}
  427|  		}
  428|  		break;
  429|  	case 5:		/*  data  */
  430|  		if (writeflag==MEM_READ) {
  431|  			if (rx_avail(d, port))
  432|  				odata = rx_nextchar(d, port);
  433|  
  434|  			/*  TODO:  perhaps only clear the RX part of RR3?  */
  435|  			d->scc_register_r[N_SCC_REGS + SCC_RR3] = 0;
  436|  
  437|  			INTERRUPT_DEASSERT(d->irq);
  438|  
  439|  //			debug("[ scc: (port %i) read from 0x%08lx: 0x%02x ]\n",
  440|  //			    port, (long)relative_addr, (int)odata);
  441|  		} else {
  442|  			/*  debug("[ scc: (port %i) write to  0x%08lx: "
  443|  			    "0x%08x ]\n", port, (long)relative_addr,
  444|  			    (int)idata);  */
  445|  
  446|  			/*  Send the character:  */
  447|  			lk201_tx_data(&d->lk201, d->scc_nr * 2 + port, idata);
  448|  
  449|  			/*  Loopback:  */
  450|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR14]
  451|  			    & SCC_WR14_LOCAL_LOOPB)
  452|  				dev_scc_add_to_rx_queue(d, idata, d->scc_nr
  453|  				    * 2 + port);
  454|  
  455|  			/*  TX interrupt:  */
  456|  			if (d->scc_register_w[port * N_SCC_REGS + SCC_WR9] &
  457|  			    SCC_WR9_MASTER_IE &&
  458|  			    d->scc_register_w[port * N_SCC_REGS + SCC_WR1] &
  459|  			    SCC_WR1_TX_IE) {
  460|  				if (port == SCC_CHANNEL_A)
  461|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  462|  					    |= SCC_RR3_TX_IP_A;
  463|  				else
  464|  					d->scc_register_r[N_SCC_REGS + SCC_RR3]
  465|  					    |= SCC_RR3_TX_IP_B;
  466|  			}
  467|  
  468|  			dev_scc_tick(cpu, extra);
  469|  		}
  470|  		break;
  471|  	default:
  472|  		if (writeflag==MEM_READ) {
  473|  			debug("[ scc: (port %i) read from 0x%08lx ]\n",
  474|  			    port, (long)relative_addr);
  475|  		} else {
  476|  			debug("[ scc: (port %i) write to  0x%08lx: 0x%08x ]\n",
  477|  			    port, (long)relative_addr, (int)idata);
  478|  		}
  479|  	}
  480|  
  481|  	if (ultrix_mode && writeflag == MEM_READ) {
  482|  		odata <<= 8;
  483|  	}
  484|  
  485|  	if (writeflag == MEM_READ)
  486|  		memory_writemax64(cpu, data, len, odata);
  487|  
  488|  	return 1;
  489|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SCCWR0PTR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SCCWR0PTR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
