# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mboutcapacity` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mboutcapacity`, state `open`)

**title:** MB89352: the WRITE path re-sizes data_out_len without reallocating, and DREG writes bound on that length

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): `mboutcapacity` HIGH -- MB89352: the WRITE path re-sizes `data_out_len` without reallocating, and DREG writes bound on that length -- a store through a NULL `data_out` after the CDB returns 2, or past a 16-byte block allocated by an earlier small XFR DATAOUT (dev_mb89352.c:225-246, :268-280, :476-495; diskimage_scsicmd

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_mb89352.c` -- AT HEAD, lines 211-296 (`*` marks a line your previous draft changed)

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
  239|* 	if (d->transfer_bufpos >= len) {
  240|* 		debugmsg_cpu(cpu, d->subsys, "", VERBOSITY_ERROR,
  241|* 	    	    "DREG: write longer than buffer?");
  242|* 	    	cpu->running = 0;
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



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_mb89352.c",
    "old": "\tif (d->transfer_bufpos >= len) {\n\t\tdebugmsg_cpu(cpu, d->subsys, \"\", VERBOSITY_ERROR,\n\t    \t    \"DREG: write longer than buffer?\");\n\t    \tcpu->running = 0;\n\t    \treturn;\n\t}\n\n\tp[d->transfer_bufpos ++] = idata;",
    "new": "\tif (p == NULL || d->transfer_bufpos >= len) {\n\t\tdebugmsg_cpu(cpu, d->subsys, \"\", VERBOSITY_ERROR,\n\t    \t    \"DREG: write longer than buffer or null?\");\n\t    \tcpu->running = 0;\n\t    \treturn;\n\t}\n\n\tp[d->transfer_bufpos ++] = idata;",
    "why": "Prevent null pointer dereference if data_out is NULL but length allows writes"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MBOUTCAPACITY: DEFECT, 3 FINDINGS
1. The diff prevents the NULL dereference by adding `p == NULL`, but it completely fails to prevent writing past a 16-byte block because it still bounds on `len` (which the issue states is `data_out_len` that was resized without reallocating). It also entirely misses the other sites named in the issue: `dev_mb89352.c:476-495` and `diskimage_scsicmd`.
2. CONTROL FLOW: No newly added `return`, `goto`, or `break`. An existing early exit condition is expanded, skipping `p[d->transfer_bufpos ++] = idata;` and the common tail phase/register updates.
3. RETURN VALUE: The function is `void`; no return value changes occur. 
4. ELSE: The diff only updates the error string to include "or null?". 
5. HOUSE IDIOMS: The error at line 240 can be triggered repeatedly by the guest writing to the DREG, which violates the idiom to print ONCE per device instance.
`src/devices/dev_mb89352.c:239` DEFECT: Bounding on `len` still allows out-of-bounds writes because `data_out_len` is resized without reallocation. Fix: UNSETTLED (needs the actual allocation size from diskimage_scsicmd or lines 476-495).
`src/devices/dev_mb89352.c:476` DEFECT: The issue explicitly names lines 476-495 and diskimage_scsicmd, which this diff completely misses. Fix: UNSETTLED.
`src/devices/dev_mb89352.c:240` STYLE: The diagnostic can be triggered repeatedly by the guest and lacks a latch and `(once)` in the message. Fix: Add latch field check and include `(once)`.
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

End with two lines: `REVISION_MBOUTCAPACITY: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MBOUTCAPACITY: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
