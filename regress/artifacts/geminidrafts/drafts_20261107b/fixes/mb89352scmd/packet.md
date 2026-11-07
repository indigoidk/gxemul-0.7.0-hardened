# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `mb89352scmd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `mb89352scmd`, state `open`)

**title:** devices/dev_mb89352.c SCMD decode -- the command is matched on the whole byte instead of bits 7:5 (no RST_ATN/SET_ATN) and transfers are accepted only with PROG_XFR -- WRONG-RESULT (variants reach the halting default arm)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T89 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-24, A1-27, C U9(b)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c, https://github.com/retroprom/gxemul/commit/922fc86b, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/devices/dev_mb89352.c:364, :409-410, :527-535.  Portable fix: yes -- port the decode part of upstream a1cafe7c + upstream 922fc86b (SVN r6544/r6546/r6550).  Filing check (TRIAGE.md): `qhmbunimplstops` covers only the resulting halt.  Not a duplicate of `qhmbunimplstops` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_mb89352.c` -- AT HEAD, lines 299-701 (`*` marks a line your previous draft changed)

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
  364|* 			switch (idata) {
  365|* 
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
  409|* 			case SCMD_XFR | SCMD_PROG_XFR:
  410|  			case SCMD_XFR | SCMD_PROG_XFR | SCMD_ICPT_XFR:
  411|  				{
  412|  					/*  #167: (Codex/Fable)
  413|  					    a transfer command issued before any
  414|  					    SCMD_SELECT leaves d->xferp NULL; treat
  415|  					    it as an illegal command instead of
  416|  					    dereferencing NULL below.  */
  417|  					if (d->xferp == NULL) {
  418|  						debugmsg_cpu(cpu, d->subsys, "",
  419|  						    VERBOSITY_WARNING,
  420|  						    "Transfer command with no"
  421|  						    " selected target; ignored");
  422|  						d->reg[INTS] |= INTS_CMD_DONE;
  423|  						break;
  424|  					}
  425|  
  426|  					d->reg[SSTS] |= SSTS_XFR;
  427|  					d->phase = d->reg[PCTL] & 7;
  428|  
  429|  					d->transfer_bufpos = 0;
  430|  
  431|  					debugmsg_cpu(cpu, d->subsys, "",
  432|  					    VERBOSITY_DEBUG,
  433|  				    	    "Transfer command: phase %i, len %zu",
  434|  				    	    d->phase, d->transfer_count);
  435|  
  436|  					switch (d->phase) {
  437|  					case PH_DATAOUT:
  438|  						/*  #295: zero the buffer (clearflag 1).
  439|  						    The line below declares it FULL --
  440|  						    data_out_offset = transfer_count -- before
  441|  						    a single guest byte has arrived, and the
  442|  						    disk layer's only guard is exactly that
  443|  						    field (diskimage_scsicmd.c:778 compares
  444|  						    data_out_offset against the CDB size and
  445|  						    otherwise writes data_out straight to the
  446|  						    image at :788).  A guest that sets up a
  447|  						    DATA_OUT phase, writes NO data bytes, and
  448|  						    then issues a WRITE therefore committed
  449|  						    whatever the freed heap block last held --
  450|  						    and scsi_transfer_alloc() keeps a freelist
  451|  						    for the transfer structs while the buffers
  452|  						    themselves are free()d, so a same-size
  453|  						    malloc very often returns the PREVIOUS
  454|  						    command's sector data.  #263 measured that
  455|  						    exact consequence on the ASC: 384 bytes of
  456|  						    the previous command's buffer written onto
  457|  						    the disk image.
  458|  
  459|  						    This is NOT #263's short-transfer shape --
  460|  						    mb89352_dreg_write() only issues the
  461|  						    command at exact fill, so the natural PIO
  462|  						    path always supplies every byte.  The
  463|  						    defect is the premature offset, and the
  464|  						    honest repair (offset 0, advanced as bytes
  465|  						    arrive) is DEFERRED on purpose: the disk
  466|  						    layer would then return 2 and this model
  467|  						    discards that return, so the guest would
  468|  						    be told a WRITE completed that never
  469|  						    reached the disk -- exactly the defect
     | [... lines 470-671 not shown ...]
  672|  		break;
  673|  
  674|  	default:
  675|  		if (writeflag == MEM_WRITE)
  676|  			debugmsg_cpu(cpu, d->subsys, "",
  677|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  678|  		    	    "unimplemented %zu-bit WRITE to address 0x%x: 0x%x",
  679|  		    	    len * 8,
  680|  			    (int) relative_addr,
  681|  			    (int) idata);
  682|  		else
  683|  			debugmsg_cpu(cpu, d->subsys, "",
  684|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  685|  		    	    "unimplemented %zu-bit READ from address 0x%x",
  686|  		    	    len * 8,
  687|  			    (int) relative_addr);
  688|  
  689|  		if (mb89352_abort_on_unimplemented_stuff) {
  690|  			cpu->running = 0;
  691|  			return 0;
  692|  		}
  693|  	}
  694|  
  695|  	reassert_interrupts(d);
  696|  
  697|  	if (writeflag == MEM_READ)
  698|  		memory_writemax64(cpu, data, len, odata);
  699|  
  700|  	return 1;
  701|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mb89352.c` -- `struct mb89352_data {` (HEAD lines 72-86)

```c
   72| struct mb89352_data {
   73| 	int			subsys;
   74| 
   75| 	struct interrupt	irq;
   76| 	bool			irq_asserted;
   77| 
   78| 	uint8_t			reg[MB89352_NREGS];
   79| 	
   80| 	int			target;		// target SCSI ID, e.g. 6
   81| 	int			phase;
   82| 
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			transfer_count;
   85| 	size_t			transfer_bufpos;
   86| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_mb89352.c",
    "old": "\t\t\tswitch (idata) {",
    "new": "\t\t\tswitch (idata & 0x1f) {",
    "why": "Ignore bits 7:5 (RST_ATN, SET_ATN, etc.) when decoding SCMD commands."
  },
  {
    "file": "src/devices/dev_mb89352.c",
    "old": "\t\t\tcase SCMD_XFR | SCMD_PROG_XFR:",
    "new": "\t\t\tcase SCMD_XFR:\n\t\t\tcase SCMD_XFR | SCMD_PROG_XFR:",
    "why": "Accept SCMD_XFR command even without the PROG_XFR modifier."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_MB89352SCMD: DEFECT, 1 FINDINGS
1. The diff does not remove the defect at every site the issue names. It successfully addresses `src/devices/dev_mb89352.c:364` (the decode mask) and `:409` (accepting bare `SCMD_XFR`), but it entirely misses the third site at `:527-535`.
`src/devices/dev_mb89352.c:527`: DEFECT: Missed site from the issue report. Fix: UNSETTLED (lines 470-672 are omitted from the text, so the exact required fix cannot be provided).
2. CONTROL FLOW: No. The diff only modifies a switch expression and adds a case label that falls through to an existing block. No new `return`, `goto`, `break`, or early exit is introduced, so it does not skip the common tail (`reassert_interrupts(d);` and `return 1;`).
3. RETURN VALUE: Yes. By successfully matching the command (via the `0x1f` mask) and the `SCMD_XFR` case, the code now processes the command and reaches the common tail to `return 1;` (indicating success). Previously, these inputs would fall through to the `default:` arm at line 675, which returns `0` (halting the CPU) when `mb89352_abort_on_unimplemented_stuff` is true.
4. What ELSE does the diff change: Nothing. The diff strictly masks the command and adds the missing transfer case, with no other side effects, state changes, or prints.
5. House idioms: No new code or comments were added that violate house idioms (no new diagnostics or comments were introduced).
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

End with two lines: `REVISION_MB89352SCMD: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_MB89352SCMD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
