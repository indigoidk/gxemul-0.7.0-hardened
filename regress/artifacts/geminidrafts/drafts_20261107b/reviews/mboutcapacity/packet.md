# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mboutcapacity` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mboutcapacity`, state `open`)

**title:** MB89352: the WRITE path re-sizes data_out_len without reallocating, and DREG writes bound on that length

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): `mboutcapacity` HIGH -- MB89352: the WRITE path re-sizes `data_out_len` without reallocating, and DREG writes bound on that length -- a store through a NULL `data_out` after the CDB returns 2, or past a 16-byte block allocated by an earlier small XFR DATAOUT (dev_mb89352.c:225-246, :268-280, :476-495; diskimage_scsicmd

**The drafter's own reading:** STILL PRESENT: YES -- 246| p[d->transfer_bufpos ++] = idata;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mb89352.c b/src/devices/dev_mb89352.c
index 179a47a2..71950b31 100644
--- a/src/devices/dev_mb89352.c
+++ b/src/devices/dev_mb89352.c
@@ -236,9 +236,9 @@ void mb89352_dreg_write(struct cpu* cpu, struct mb89352_data *d, int writeflag,
 	    	return;
 	}
 
-	if (d->transfer_bufpos >= len) {
+	if (p == NULL || d->transfer_bufpos >= len) {
 		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
-	    	    "DREG: write longer than buffer?");
+	    	    "DREG: write longer than buffer or null?");
 	    	cpu->running = 0;
 	    	return;
 	}
```

## Every edited function, after the fix

### `src/devices/dev_mb89352.c` -- post-edit lines 211-296 (`+` marks a line the diff added or the point of a deletion)

```c
  211|  void mb89352_dreg_write(struct cpu* cpu, struct mb89352_data *d, int writeflag, int idata)
  212|  {
  213|  	if (d->xferp == NULL) {
  214|  		debugmsg_cpu(cpu, d->subsys, "",
  215|  		    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  216|  	    	    "DREG: no ongoing transfer to write to?");
  217|  	    	return;
  218|  	}
  219|  	
  220|  	uint8_t *p = d->xferp->data_in;
  221|  	size_t len = d->xferp->data_in_len;
  222|  	
  223|  	switch (d->phase) {
  224|  	case PH_DATAOUT:
  225|  		p = d->xferp->data_out;
  226|  		len = d->xferp->data_out_len;
  227|  		break;
  228|  	case PH_CMD:
  229|  		p = d->xferp->cmd;
  230|  		len = d->xferp->cmd_len;
  231|  		break;
  232|  	default:
  233|  		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  234|  	    	    "DREG: write in unimplemented phase %i", d->phase);
  235|  	    	cpu->running = 0;
  236|  	    	return;
  237|  	}
  238|  
  239|+ 	if (p == NULL || d->transfer_bufpos >= len) {
  240|  		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  241|+ 	    	    "DREG: write longer than buffer or null?");
  242|  	    	cpu->running = 0;
  243|  	    	return;
  244|  	}
  245|  
  246|  	p[d->transfer_bufpos ++] = idata;
  247|  
  248|  	if (d->transfer_bufpos < len)
  249|  		return;
  250|  
  251|  	debugmsg_cpu(cpu, d->subsys, "",
  252|  	    VERBOSITY_DEBUG,
  253|      	    "%zu bytes written", d->transfer_bufpos);
  254|  
  255|  	int res;
  256|  
  257|  	switch (d->phase) {
  258|  
  259|  	case PH_DATAOUT:
  260|  		/*  #338: publish how many bytes ACTUALLY arrived. This is the
  261|  		    only place that knows -- transfer_bufpos counted them one
  262|  		    at a time above -- and it is reached exactly when the
  263|  		    buffer has filled, so the command now becomes eligible
  264|  		    because the data is present rather than because it was
  265|  		    promised.  */
  266|  		d->xferp->data_out_offset = d->transfer_bufpos;
  267|  
  268|  		res = diskimage_scsicommand(cpu,
  269|  	    	    d->target, DISKIMAGE_SCSI, d->xferp);
  270|  
  271|  		// TODO: How about failure results?
  272|  		d->phase = PH_STAT;
  273|  		break;
  274|  
  275|  	case PH_CMD:
  276|  		res = diskimage_scsicommand(cpu,
  277|  	    	    d->target, DISKIMAGE_SCSI, d->xferp);
  278|  
  279|  		if (res == 2)
  280|  			d->phase = PH_DATAOUT;
  281|  		else if (d->xferp->data_in != NULL)
  282|  			d->phase = PH_DATAIN;
  283|  		else
  284|  			d->phase = PH_STAT;
  285|  		break;
  286|  
  287|  	default:
  288|  		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  289|  	    	    "DREG write: UNIMPLEMENTED PHASE %i", d->phase);
  290|  	    	cpu->running = 0;
  291|  	}
  292|  	
  293|  	d->reg[PSNS] |= PSNS_REQ;
  294|  	d->reg[SSTS] &= ~SSTS_XFR;
  295|  	d->reg[INTS] |= INTS_CMD_DONE;
  296|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MBOUTCAPACITY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MBOUTCAPACITY: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
