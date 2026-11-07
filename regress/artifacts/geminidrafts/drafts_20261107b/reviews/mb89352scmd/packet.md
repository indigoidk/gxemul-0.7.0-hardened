# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mb89352scmd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mb89352scmd`, state `open`)

**title:** devices/dev_mb89352.c SCMD decode -- the command is matched on the whole byte instead of bits 7:5 (no RST_ATN/SET_ATN) and transfers are accepted only with PROG_XFR -- WRONG-RESULT (variants reach the halting default arm)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T89 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-24, A1-27, C U9(b)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c, https://github.com/retroprom/gxemul/commit/922fc86b, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/devices/dev_mb89352.c:364, :409-410, :527-535.  Portable fix: yes -- port the decode part of upstream a1cafe7c + upstream 922fc86b (SVN r6544/r6546/r6550).  Filing check (TRIAGE.md): `qhmbunimplstops` covers only the resulting halt.  Not a duplicate of `qhmbunimplstops` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 364

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mb89352.c b/src/devices/dev_mb89352.c
index 179a47a2..63befc61 100644
--- a/src/devices/dev_mb89352.c
+++ b/src/devices/dev_mb89352.c
@@ -361,7 +361,7 @@ DEVICE_ACCESS(mb89352)
 			if (idata & SCMD_RST)
 				idata = SCMD_BUS_REL;
 			
-			switch (idata) {
+			switch (idata & 0x1f) {
 
 			case SCMD_BUS_REL:	// 0x00
 				d->reg[SSTS] &= ~(SSTS_TARGET | SSTS_INITIATOR | SSTS_XFR);
@@ -406,6 +406,7 @@ DEVICE_ACCESS(mb89352)
 				}
 				break;
 
+			case SCMD_XFR:
 			case SCMD_XFR | SCMD_PROG_XFR:
 			case SCMD_XFR | SCMD_PROG_XFR | SCMD_ICPT_XFR:
 				{
```

## Every edited function, after the fix

### `src/devices/dev_mb89352.c` -- post-edit lines 299-702 (`+` marks a line the diff added or the point of a deletion)

```c
  299|  DEVICE_ACCESS(mb89352)
  300|  {
  301|  	struct mb89352_data *d = (struct mb89352_data *) extra;
  302|  	uint64_t idata = 0, odata = 0;
  303|  
  304|  	if (len != 1) {
  305|  		debugmsg_cpu(cpu, d->subsys, "",
  306|  		    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  307|  	    	    "unimplemented LEN: %zu-bit access, address 0x%x",
  308|  	    	    len * 8,
  309|  	    	    (int) relative_addr);
  310|  
  311|  		if (mb89352_abort_on_unimplemented_stuff) {
  312|  			cpu->running = 0;
  313|  			return 0;
  314|  		}
  315|  	}
  316|  
  317|  	int regnr = (relative_addr >> 2) & (MB89352_NREGS - 1);
  318|  
  319|  	if (writeflag == MEM_WRITE)
  320|  		idata = memory_readmax64(cpu, data, len);
  321|  	else
  322|  		odata = d->reg[regnr];
  323|  
  324|  	reg_debug(cpu, d, writeflag, regnr, idata);
  325|  
  326|  	switch (regnr) {
  327|  
  328|  	case BDID:
  329|  		if (writeflag == MEM_WRITE) {
  330|  			d->reg[BDID] = idata;
  331|  			if (idata != 7)
  332|  				debugmsg_cpu(cpu, d->subsys, "",
  333|  				    VERBOSITY_INFO, "unimplemented BDID value: 0x%x",
  334|  			    	    (int) idata);
  335|  		} else {
  336|  			odata = (1 << d->reg[BDID]);
  337|  		}
  338|  		break;
  339|  
  340|  	case SCTL:
  341|  		if (writeflag == MEM_WRITE) {
  342|  			d->reg[SCTL] = idata;
  343|  
  344|  			if (idata & SCTL_DIAG)
  345|  				debugmsg_cpu(cpu, d->subsys, "",
  346|  				    VERBOSITY_ERROR,
  347|  			    	    "Diagnostics mode NOT IMPLEMENTED");
  348|  
  349|  			if (idata & SCTL_CTRLRST) {
  350|  				debugmsg(d->subsys, "", VERBOSITY_INFO, "resetting controller");
  351|  				reset_controller(d);
  352|  			}
  353|  		}
  354|  		break;
  355|  
  356|  	case SCMD:
  357|  		if (writeflag == MEM_WRITE) {
  358|  			d->reg[SCMD] = idata;
  359|  			
  360|  			// RST = Reset ?
  361|  			if (idata & SCMD_RST)
  362|  				idata = SCMD_BUS_REL;
  363|  			
  364|+ 			switch (idata & 0x1f) {
  365|  
  366|  			case SCMD_BUS_REL:	// 0x00
  367|  				d->reg[SSTS] &= ~(SSTS_TARGET | SSTS_INITIATOR | SSTS_XFR);
  368|  				d->phase = PH_BUS_FREE;
  369|  				// TODO: BUS FREE interrupt enable: PCTL_BFINT_ENAB?
  370|  				break;
  371|  
  372|  			case SCMD_SELECT:
  373|  				// Select target in the temp register.
  374|  				{
  375|  					int target = 0;
  376|  					while (target < 8) {
  377|  						int m = 1 << target;
  378|  						if (d->reg[TEMP] & ~(1 << 7) & m)
  379|  							break;
  380|  						target ++;
  381|  					}
  382|  
  383|  					if (target < 8)
  384|  						debugmsg_cpu(cpu, d->subsys, "",
  385|  						    VERBOSITY_DEBUG,
  386|  					    	    "selecting target %i", target);
  387|  					else
  388|  						debugmsg_cpu(cpu, d->subsys, "",
  389|  						    VERBOSITY_WARNING,
  390|  					    	    "SCMD_SELECT with no target?");
  391|  
  392|  					d->target = target;
  393|  					d->reg[INTS] |= INTS_CMD_DONE;
  394|  					d->reg[PSNS] &= ~7;
  395|  					d->phase = PH_CMD;
  396|  					d->reg[PSNS] |= PSNS_REQ;
  397|  
  398|  					if (d->xferp != NULL)
  399|  						scsi_transfer_free(d->xferp);
  400|  
  401|  					d->xferp = scsi_transfer_alloc();
  402|  					d->transfer_bufpos = 0;
  403|  
  404|  					d->reg[SSTS] &= ~SSTS_TARGET;
  405|  					d->reg[SSTS] |= SSTS_BUSY;
  406|  				}
  407|  				break;
  408|  
  409|+ 			case SCMD_XFR:
  410|  			case SCMD_XFR | SCMD_PROG_XFR:
  411|  			case SCMD_XFR | SCMD_PROG_XFR | SCMD_ICPT_XFR:
  412|  				{
  413|  					/*  #167: (Codex/Fable)
  414|  					    a transfer command issued before any
  415|  					    SCMD_SELECT leaves d->xferp NULL; treat
  416|  					    it as an illegal command instead of
  417|  					    dereferencing NULL below.  */
  418|  					if (d->xferp == NULL) {
  419|  						debugmsg_cpu(cpu, d->subsys, "",
  420|  						    VERBOSITY_WARNING,
  421|  						    "Transfer command with no"
  422|  						    " selected target; ignored");
  423|  						d->reg[INTS] |= INTS_CMD_DONE;
  424|  						break;
  425|  					}
  426|  
  427|  					d->reg[SSTS] |= SSTS_XFR;
  428|  					d->phase = d->reg[PCTL] & 7;
  429|  
  430|  					d->transfer_bufpos = 0;
  431|  
  432|  					debugmsg_cpu(cpu, d->subsys, "",
  433|  					    VERBOSITY_DEBUG,
  434|  				    	    "Transfer command: phase %i, len %zu",
  435|  				    	    d->phase, d->transfer_count);
  436|  
  437|  					switch (d->phase) {
  438|  					case PH_DATAOUT:
  439|  						/*  #295: zero the buffer (clearflag 1).
  440|  						    The line below declares it FULL --
  441|  						    data_out_offset = transfer_count -- before
  442|  						    a single guest byte has arrived, and the
  443|  						    disk layer's only guard is exactly that
  444|  						    field (diskimage_scsicmd.c:778 compares
  445|  						    data_out_offset against the CDB size and
  446|  						    otherwise writes data_out straight to the
  447|  						    image at :788).  A guest that sets up a
  448|  						    DATA_OUT phase, writes NO data bytes, and
  449|  						    then issues a WRITE therefore committed
  450|  						    whatever the freed heap block last held --
  451|  						    and scsi_transfer_alloc() keeps a freelist
  452|  						    for the transfer structs while the buffers
  453|  						    themselves are free()d, so a same-size
  454|  						    malloc very often returns the PREVIOUS
  455|  						    command's sector data.  #263 measured that
  456|  						    exact consequence on the ASC: 384 bytes of
  457|  						    the previous command's buffer written onto
  458|  						    the disk image.
  459|  
  460|  						    This is NOT #263's short-transfer shape --
  461|  						    mb89352_dreg_write() only issues the
  462|  						    command at exact fill, so the natural PIO
  463|  						    path always supplies every byte.  The
  464|  						    defect is the premature offset, and the
  465|  						    honest repair (offset 0, advanced as bytes
  466|  						    arrive) is DEFERRED on purpose: the disk
  467|  						    layer would then return 2 and this model
  468|  						    discards that return, so the guest would
  469|  						    be told a WRITE completed that never
     | [... lines 470-672 not shown ...]
  673|  		break;
  674|  
  675|  	default:
  676|  		if (writeflag == MEM_WRITE)
  677|  			debugmsg_cpu(cpu, d->subsys, "",
  678|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  679|  		    	    "unimplemented %zu-bit WRITE to address 0x%x: 0x%x",
  680|  		    	    len * 8,
  681|  			    (int) relative_addr,
  682|  			    (int) idata);
  683|  		else
  684|  			debugmsg_cpu(cpu, d->subsys, "",
  685|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  686|  		    	    "unimplemented %zu-bit READ from address 0x%x",
  687|  		    	    len * 8,
  688|  			    (int) relative_addr);
  689|  
  690|  		if (mb89352_abort_on_unimplemented_stuff) {
  691|  			cpu->running = 0;
  692|  			return 0;
  693|  		}
  694|  	}
  695|  
  696|  	reassert_interrupts(d);
  697|  
  698|  	if (writeflag == MEM_READ)
  699|  		memory_writemax64(cpu, data, len, odata);
  700|  
  701|  	return 1;
  702|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MB89352SCMD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MB89352SCMD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
