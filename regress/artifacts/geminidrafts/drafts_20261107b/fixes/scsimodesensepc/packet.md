# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `scsimodesensepc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `scsimodesensepc`, state `open`)

**title:** disk/diskimage_scsicmd.c MODE SENSE -- page control PC=1/2/3 returns current values with an unlatched `fatal()` per command -- WRONG-RESULT (+ log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T78 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9ef1d3ea8ec6fb2a9e1621c6dfc8cb0fd065cb67, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:591-593.  Portable fix: yes -- port rs6000 9ef1d3e, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/disk/diskimage_scsicmd.c` -- AT HEAD, lines 270-1389 (`*` marks a line your previous draft changed)

```c
  270|  {
  271|  	char namebuf[16];
  272|  	int retlen, i, q;
  273|  	uint64_t size;
  274|  	int64_t ofs;
     | [... lines 275-480 not shown ...]
  481|  				    " set not yet implemented\n");
  482|  			}
  483|  		}
  484|  
  485|  		/*  Return data:  */
  486|  		scsi_transfer_allocbuf(&xferp->data_in_len, &xferp->data_in,
  487|  		    8, 1);
  488|  
  489|  		diskimage_recalc_size(d);
  490|  
  491|  		/*
  492|  		 *  #412: a zero-block disk must not announce a last block.
  493|  		 *
  494|  		 *  `size` is uint64_t and nr_of_logical_blocks is int64_t, so
  495|  		 *  0 - 1 underflows and the four bytes below then report
  496|  		 *  0xffffffff -- the guest is told the disk holds 4,294,967,296
  497|  		 *  blocks, i.e. 2 TiB at 512 bytes each, rather than that it is
  498|  		 *  empty.  MEASURED against this function: 0 blocks announced
  499|  		 *  last-LBA 0xffffffff.
  500|  		 *
  501|  		 *  This is not hypothetical.  A separate defect leaves every
  502|  		 *  `-d gH;S` disk with zero blocks, and such a disk KEEPS its
  503|  		 *  SCSI or IDE type -- so it reaches this handler and is told
  504|  		 *  it holds two terabytes.  Measured: a 10 MB image announced
  505|  		 *  as "SCSI DISK id 0, read/write, 0 MB (CHS=0,16,63)".  The
  506|  		 *  "0 MB" the operator sees on the console is only the
  507|  		 *  host-side banner; the GUEST is told 2 TiB.  That defect is
  508|  		 *  fixed separately -- this guard is what makes an empty disk
  509|  		 *  report itself as empty regardless of how it got that way,
  510|  		 *  and it stays correct after that fix lands.
  511|  		 *
  512|  		 *  #413 NARROWED THIS CLAIM.  #412 said "every floppy", which
  513|  		 *  is wrong: DISKIMAGE_FLOPPY is a WRITE-ONLY TYPE in this
  514|  		 *  codebase.  NO DEVICE REFERENCES IT.  Every controller
  515|  		 *  hard-codes its type argument (six diskimage_scsicommand()
  516|  		 *  sites pass DISKIMAGE_SCSI, the ATAPI one passes
  517|  		 *  DISKIMAGE_IDE) and both lookups match on d->type == type, so
  518|  		 *  a floppy-typed disk never reaches this function at all -- it
  519|  		 *  is invisible to every controller.  The gate row below is
  520|  		 *  unaffected: it uses a 0-byte image, which is a genuinely
  521|  		 *  reachable zero-block SCSI disk.
  522|  		 *
  523|  		 *  #418 STATED THE COUNT AND THE COUNT WAS THE BUG.  This
  524|  		 *  paragraph used to read "it occurs in exactly seven places,
  525|  		 *  all inside diskimage.c/diskimage.h" -- and it was wrong the
  526|  		 *  moment it was written, twice over: SPELLING THE IDENTIFIER
  527|  		 *  HERE MADE THE COUNT EIGHT, and "all inside
  528|  		 *  diskimage.c/diskimage.h" is falsified by the file this
  529|  		 *  sentence lives in.  The SAME sentence was duplicated in
  530|  		 *  CHANGELOG.md and is corrected there too -- found by a review
  531|  		 *  seat, not here, because this file's own census had silently
  532|  		 *  scoped itself to src/ (8 hits) when the tree carries 16.
  533|  		 *  That omitted scope is the very failure being corrected.  No
  534|  		 *  OTHER construct in the tree uses the pattern, so it is a
  535|  		 *  one-off rather than a class, but the cheap rule it earns is
  536|  		 *  worth keeping: A COMMENT MAY NOT STATE A COUNT OF AN
  537|  		 *  IDENTIFIER IT ALSO SPELLS.  State the structural property
  538|  		 *  instead -- it stays true across edits.
  539|  		 *
  540|  		 *  #418 also fixed HALF of the reachability defect: the
  541|  		 *  documented `d:` prefix now assigns the machine's default
  542|  		 *  disk type, so `-d d:floppy.img` gives a reachable disk.  A
  543|  		 *  BARE floppy-sized image is still typed FLOPPY and still
  544|  		 *  invisible; that half remains open.
  545|  		 *
  546|  		 *  0xffffffff is also the ATA/SCSI "capacity too large for this
  547|  		 *  command" sentinel, so reporting it for an EMPTY disk is the
  548|  		 *  worst available answer: it is not merely wrong, it is the
  549|  		 *  one value that means something else entirely.
  550|  		 */
  551|  		if (d->nr_of_logical_blocks < 1)
  552|  			size = 0;
  553|  		else
  554|  			size = d->nr_of_logical_blocks - 1;
  555|  
  556|  		xferp->data_in[0] = (size >> 24) & 255;
  557|  		xferp->data_in[1] = (size >> 16) & 255;
  558|  		xferp->data_in[2] = (size >> 8) & 255;
  559|  		xferp->data_in[3] = size & 255;
  560|  
  561|  		xferp->data_in[4] = (d->logical_block_size >> 24) & 255;
  562|  		xferp->data_in[5] = (d->logical_block_size >> 16) & 255;
  563|  		xferp->data_in[6] = (d->logical_block_size >> 8) & 255;
  564|  		xferp->data_in[7] = d->logical_block_size & 255;
  565|  
  566|  		diskimage__return_default_status_and_message(xferp, d);
  567|  		break;
  568|  
  569|  	case SCSICMD_MODE_SENSE:
  570|  	case SCSICMD_MODE_SENSE10:	
  571|  		debug("MODE_SENSE");
  572|  		q = 4; retlen = xferp->cmd[4];
  573|  		switch (xferp->cmd_len) {
  574|  		case 6:	break;
  575|  		case 10:q = 8;
  576|  			retlen = xferp->cmd[7] * 256 + xferp->cmd[8];
  577|  			break;
  578|  		default:fatal(" (unimplemented mode_sense len=%zu)",
  579|  			    xferp->cmd_len);
  580|  		}
  581|  
  582|  		/*
  583|  		 *  NOTE/TODO: This code doesn't handle too short retlens
  584|  		 *  very well. A quick hack around this is that I allocate
  585|  		 *  a bit too much memory, so that nothing is actually
  586|  		 *  written outside of xferp->data_in[].
  587|  		 */
  588|  
  589|  		retlen += 100;		/*  Should be enough. (Ugly.)  */
  590|  
  591|* 		if ((xferp->cmd[2] & 0xc0) != 0)
  592|* 			fatal("WARNING: mode sense, cmd[2] = 0x%02x\n",
  593|* 			    xferp->cmd[2]);
  594|  
  595|  		/*  Return data:  */
  596|  		scsi_transfer_allocbuf(&xferp->data_in_len,
  597|  		    &xferp->data_in, retlen, 1);
  598|  
  599|  		xferp->data_in_len -= 100;	/*  Restore size.  */
  600|  
  601|  		pagecode = xferp->cmd[2] & 0x3f;
  602|  
  603|  		debug("[ MODE SENSE id %i, pagecode=%i ]\n", id, pagecode);
  604|  
  605|  		/*  4 bytes of header for 6-byte command,
  606|  		    8 bytes of header for 10-byte command.  */
  607|  		xferp->data_in[0] = retlen;	/*  0: mode data length  */
  608|  		xferp->data_in[1] = d->is_a_cdrom? 0x05 : 0x00;
  609|  				/*  1: medium type  */
  610|  		xferp->data_in[2] = 0x00;	/*  device specific
  611|  						    parameter  */
  612|  		xferp->data_in[3] = 8 * 1;	/*  block descriptor
  613|  						    length: 1 page (?)  */
  614|  
  615|  		xferp->data_in[q+0] = 0x00;	/*  density code  */
  616|  		xferp->data_in[q+1] = 0;	/*  nr of blocks, high  */
  617|  		xferp->data_in[q+2] = 0;	/*  nr of blocks, mid  */
  618|  		xferp->data_in[q+3] = 0;	/*  nr of blocks, low */
  619|  		xferp->data_in[q+4] = 0x00;	/*  reserved  */
  620|  		xferp->data_in[q+5] = (d->logical_block_size >> 16) & 255;
  621|  		xferp->data_in[q+6] = (d->logical_block_size >> 8) & 255;
  622|  		xferp->data_in[q+7] = d->logical_block_size & 255;
  623|  		q += 8;
  624|  
  625|  		diskimage__return_default_status_and_message(xferp, d);
  626|  
  627|  		/*  descriptors, 8 bytes (each)  */
  628|  
  629|  		/*  page, n bytes (each)  */
  630|  		switch (pagecode) {
  631|  		case 0:
  632|  			/*  TODO: Nothing here?  */
  633|  			break;
  634|  		case 1:		/*  read-write error recovery page  */
  635|  			xferp->data_in[q + 0] = pagecode;
  636|  			xferp->data_in[q + 1] = 10;
  637|  			break;
  638|  		case 3:		/*  format device page  */
  639|  			xferp->data_in[q + 0] = pagecode;
  640|  			xferp->data_in[q + 1] = 22;
  641|  
  642|  			/*  10,11 = sectors per track  */
  643|  			xferp->data_in[q + 10] = 0;
  644|  			xferp->data_in[q + 11] = d->sectors_per_track;
  645|  
  646|  			/*  12,13 = physical sector size  */
  647|  			xferp->data_in[q + 12] =
  648|  			    (d->logical_block_size >> 8) & 255;
  649|  			xferp->data_in[q + 13] = d->logical_block_size & 255;
  650|  			break;
  651|  		case 4:		/*  rigid disk geometry page  */
  652|  			xferp->data_in[q + 0] = pagecode;
  653|  			xferp->data_in[q + 1] = 22;
     | [... lines 654-1359 not shown ...]
 1360|  		 *  Not documented in http://www.danbbs.dk/~dino/
 1361|  		 *		SCSI/SCSI2-D.html.
 1362|  		 *  Google gave the answer "MECHANISM_STATUS" for ATAPI. Hm.
 1363|  		 */
 1364|  
 1365|  		if (xferp->cmd_len < 12) {
 1366|  			fatal("WEIRD LEN?\n");
 1367|  			retlen = 8;
 1368|  		} else {
 1369|  			retlen = xferp->cmd[8] * 256 + xferp->cmd[9];
 1370|  		}
 1371|  
 1372|  		/*  Return data:  */
 1373|  		scsi_transfer_allocbuf(&xferp->data_in_len,
 1374|  		    &xferp->data_in, retlen, 1);
 1375|  
 1376|  		diskimage__return_default_status_and_message(xferp, d);
 1377|  
 1378|  		break;
 1379|  
 1380|  	default:
 1381|  		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
 1382|  		    xferp->cmd[0], id);
 1383|  		// exit(1);
 1384|  	}
 1385|  
 1386|  	debug(" ]\n");
 1387|  
 1388|  	return 1;
 1389|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/disk/diskimage_scsicmd.c",
    "old": "\t\tif ((xferp->cmd[2] & 0xc0) != 0)\n\t\t\tfatal(\"WARNING: mode sense, cmd[2] = 0x%02x\\n\",\n\t\t\t    xferp->cmd[2]);",
    "new": "\t\t/* #001: Demote unlatched fatal to debug */\n\t\tif ((xferp->cmd[2] & 0xc0) != 0)\n\t\t\tdebug(\"WARNING: mode sense, cmd[2] = 0x%02x\\n\",\n\t\t\t    xferp->cmd[2]);",
    "why": "Demote to debug to stop log flood while returning current values."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_SCSIMODESENSEPC: DEFECT, 1 FINDINGS
1. **Defect removal:** The diff only removes the log flood by changing `fatal` to `debug`. It fails to fix the `WRONG-RESULT` defect described in the issue (where PC=1/2/3 inappropriately returns the current values instead of changeable, default, or saved values). 
2. **CONTROL FLOW:** No added `return`, `goto`, `break`, or early exit. The control flow is unchanged.
3. **RETURN VALUE:** No return value is changed. The function still falls through to `return 1;` indicating the command was processed.
4. **ELSE:** It alters the logging severity from `fatal` (which may log heavily to the console) to `debug` (which is typically hidden unless debug logging is enabled).
5. **House idioms:** The comment `#001` is syntactically fine as a tag, but if the message were left as a warning that the user sees, it lacks a latch to prevent log floods. Since it's demoted to `debug`, the flood is hidden from normal operation, though it remains unlatched.
`src/disk/diskimage_scsicmd.c:592`: DEFECT: The fix fails to implement PC=1/2/3 behavior or return an error, leaving the `WRONG-RESULT` defect intact. Fix: Implement the PC behaviors or return a SCSI error condition.
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

End with two lines: `REVISION_SCSIMODESENSEPC: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_SCSIMODESENSEPC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
