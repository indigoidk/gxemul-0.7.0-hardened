# GXemul hardened fork -- DRAFT A FIX for one filed issue, `scsimodesensepc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `scsimodesensepc`, state `open`, severity `MED`)

**title:** disk/diskimage_scsicmd.c MODE SENSE -- page control PC=1/2/3 returns current values with an unlatched `fatal()` per command -- WRONG-RESULT (+ log flood)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T78 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9ef1d3ea8ec6fb2a9e1621c6dfc8cb0fd065cb67, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:591-593.  Portable fix: yes -- port rs6000 9ef1d3e, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 9ef1d3e, rs6000 24cb943

## The code at the cited lines

### `src/disk/diskimage_scsicmd.c` around the row's cited line 591 (HEAD 2d25df65, lines 546-636)

```c
  546| 		 *  0xffffffff is also the ATA/SCSI "capacity too large for this
  547| 		 *  command" sentinel, so reporting it for an EMPTY disk is the
  548| 		 *  worst available answer: it is not merely wrong, it is the
  549| 		 *  one value that means something else entirely.
  550| 		 */
  551| 		if (d->nr_of_logical_blocks < 1)
  552| 			size = 0;
  553| 		else
  554| 			size = d->nr_of_logical_blocks - 1;
  555| 
  556| 		xferp->data_in[0] = (size >> 24) & 255;
  557| 		xferp->data_in[1] = (size >> 16) & 255;
  558| 		xferp->data_in[2] = (size >> 8) & 255;
  559| 		xferp->data_in[3] = size & 255;
  560| 
  561| 		xferp->data_in[4] = (d->logical_block_size >> 24) & 255;
  562| 		xferp->data_in[5] = (d->logical_block_size >> 16) & 255;
  563| 		xferp->data_in[6] = (d->logical_block_size >> 8) & 255;
  564| 		xferp->data_in[7] = d->logical_block_size & 255;
  565| 
  566| 		diskimage__return_default_status_and_message(xferp, d);
  567| 		break;
  568| 
  569| 	case SCSICMD_MODE_SENSE:
  570| 	case SCSICMD_MODE_SENSE10:	
  571| 		debug("MODE_SENSE");
  572| 		q = 4; retlen = xferp->cmd[4];
  573| 		switch (xferp->cmd_len) {
  574| 		case 6:	break;
  575| 		case 10:q = 8;
  576| 			retlen = xferp->cmd[7] * 256 + xferp->cmd[8];
  577| 			break;
  578| 		default:fatal(" (unimplemented mode_sense len=%zu)",
  579| 			    xferp->cmd_len);
  580| 		}
  581| 
  582| 		/*
  583| 		 *  NOTE/TODO: This code doesn't handle too short retlens
  584| 		 *  very well. A quick hack around this is that I allocate
  585| 		 *  a bit too much memory, so that nothing is actually
  586| 		 *  written outside of xferp->data_in[].
  587| 		 */
  588| 
  589| 		retlen += 100;		/*  Should be enough. (Ugly.)  */
  590| 
  591| 		if ((xferp->cmd[2] & 0xc0) != 0)
  592| 			fatal("WARNING: mode sense, cmd[2] = 0x%02x\n",
  593| 			    xferp->cmd[2]);
  594| 
  595| 		/*  Return data:  */
  596| 		scsi_transfer_allocbuf(&xferp->data_in_len,
  597| 		    &xferp->data_in, retlen, 1);
  598| 
  599| 		xferp->data_in_len -= 100;	/*  Restore size.  */
  600| 
  601| 		pagecode = xferp->cmd[2] & 0x3f;
  602| 
  603| 		debug("[ MODE SENSE id %i, pagecode=%i ]\n", id, pagecode);
  604| 
  605| 		/*  4 bytes of header for 6-byte command,
  606| 		    8 bytes of header for 10-byte command.  */
  607| 		xferp->data_in[0] = retlen;	/*  0: mode data length  */
  608| 		xferp->data_in[1] = d->is_a_cdrom? 0x05 : 0x00;
  609| 				/*  1: medium type  */
  610| 		xferp->data_in[2] = 0x00;	/*  device specific
  611| 						    parameter  */
  612| 		xferp->data_in[3] = 8 * 1;	/*  block descriptor
  613| 						    length: 1 page (?)  */
  614| 
  615| 		xferp->data_in[q+0] = 0x00;	/*  density code  */
  616| 		xferp->data_in[q+1] = 0;	/*  nr of blocks, high  */
  617| 		xferp->data_in[q+2] = 0;	/*  nr of blocks, mid  */
  618| 		xferp->data_in[q+3] = 0;	/*  nr of blocks, low */
  619| 		xferp->data_in[q+4] = 0x00;	/*  reserved  */
  620| 		xferp->data_in[q+5] = (d->logical_block_size >> 16) & 255;
  621| 		xferp->data_in[q+6] = (d->logical_block_size >> 8) & 255;
  622| 		xferp->data_in[q+7] = d->logical_block_size & 255;
  623| 		q += 8;
  624| 
  625| 		diskimage__return_default_status_and_message(xferp, d);
  626| 
  627| 		/*  descriptors, 8 bytes (each)  */
  628| 
  629| 		/*  page, n bytes (each)  */
  630| 		switch (pagecode) {
  631| 		case 0:
  632| 			/*  TODO: Nothing here?  */
  633| 			break;
  634| 		case 1:		/*  read-write error recovery page  */
  635| 			xferp->data_in[q + 0] = pagecode;
  636| 			xferp->data_in[q + 1] = 10;
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_SCSIMODESENSEPC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
