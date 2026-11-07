# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `scsimodesensepc` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `scsimodesensepc`, state `open`)

**title:** disk/diskimage_scsicmd.c MODE SENSE -- page control PC=1/2/3 returns current values with an unlatched `fatal()` per command -- WRONG-RESULT (+ log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T78 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-19).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/9ef1d3ea8ec6fb2a9e1621c6dfc8cb0fd065cb67, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:591-593.  Portable fix: yes -- port rs6000 9ef1d3e, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/disk/diskimage_scsicmd.c:591-593

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/disk/diskimage_scsicmd.c b/src/disk/diskimage_scsicmd.c
index 5de21e05..394d55fd 100644
--- a/src/disk/diskimage_scsicmd.c
+++ b/src/disk/diskimage_scsicmd.c
@@ -588,9 +588,12 @@ xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
 
 		retlen += 100;		/*  Should be enough. (Ugly.)  */
 
-		if ((xferp->cmd[2] & 0xc0) != 0)
-			fatal("WARNING: mode sense, cmd[2] = 0x%02x\n",
+		/* #001: Return 0 on unsupported PC to prevent WRONG-RESULT */
+		if ((xferp->cmd[2] & 0xc0) != 0) {
+			debug("WARNING: mode sense, cmd[2] = 0x%02x\n",
 			    xferp->cmd[2]);
+			return 0;
+		}
 
 		/*  Return data:  */
 		scsi_transfer_allocbuf(&xferp->data_in_len,
```

## Every edited function, after the fix

### `src/disk/diskimage_scsicmd.c` -- post-edit lines 270-1392 (`+` marks a line the diff added or the point of a deletion)

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
  591|+ 		/* #001: Return 0 on unsupported PC to prevent WRONG-RESULT */
  592|+ 		if ((xferp->cmd[2] & 0xc0) != 0) {
  593|+ 			debug("WARNING: mode sense, cmd[2] = 0x%02x\n",
  594|  			    xferp->cmd[2]);
  595|+ 			return 0;
  596|+ 		}
  597|  
  598|  		/*  Return data:  */
  599|  		scsi_transfer_allocbuf(&xferp->data_in_len,
  600|  		    &xferp->data_in, retlen, 1);
  601|  
  602|  		xferp->data_in_len -= 100;	/*  Restore size.  */
  603|  
  604|  		pagecode = xferp->cmd[2] & 0x3f;
  605|  
  606|  		debug("[ MODE SENSE id %i, pagecode=%i ]\n", id, pagecode);
  607|  
  608|  		/*  4 bytes of header for 6-byte command,
  609|  		    8 bytes of header for 10-byte command.  */
  610|  		xferp->data_in[0] = retlen;	/*  0: mode data length  */
  611|  		xferp->data_in[1] = d->is_a_cdrom? 0x05 : 0x00;
  612|  				/*  1: medium type  */
  613|  		xferp->data_in[2] = 0x00;	/*  device specific
  614|  						    parameter  */
  615|  		xferp->data_in[3] = 8 * 1;	/*  block descriptor
  616|  						    length: 1 page (?)  */
  617|  
  618|  		xferp->data_in[q+0] = 0x00;	/*  density code  */
  619|  		xferp->data_in[q+1] = 0;	/*  nr of blocks, high  */
  620|  		xferp->data_in[q+2] = 0;	/*  nr of blocks, mid  */
  621|  		xferp->data_in[q+3] = 0;	/*  nr of blocks, low */
  622|  		xferp->data_in[q+4] = 0x00;	/*  reserved  */
  623|  		xferp->data_in[q+5] = (d->logical_block_size >> 16) & 255;
  624|  		xferp->data_in[q+6] = (d->logical_block_size >> 8) & 255;
  625|  		xferp->data_in[q+7] = d->logical_block_size & 255;
  626|  		q += 8;
  627|  
  628|  		diskimage__return_default_status_and_message(xferp, d);
  629|  
  630|  		/*  descriptors, 8 bytes (each)  */
  631|  
  632|  		/*  page, n bytes (each)  */
  633|  		switch (pagecode) {
  634|  		case 0:
  635|  			/*  TODO: Nothing here?  */
  636|  			break;
  637|  		case 1:		/*  read-write error recovery page  */
  638|  			xferp->data_in[q + 0] = pagecode;
  639|  			xferp->data_in[q + 1] = 10;
  640|  			break;
  641|  		case 3:		/*  format device page  */
  642|  			xferp->data_in[q + 0] = pagecode;
  643|  			xferp->data_in[q + 1] = 22;
  644|  
  645|  			/*  10,11 = sectors per track  */
  646|  			xferp->data_in[q + 10] = 0;
  647|  			xferp->data_in[q + 11] = d->sectors_per_track;
  648|  
  649|  			/*  12,13 = physical sector size  */
  650|  			xferp->data_in[q + 12] =
  651|  			    (d->logical_block_size >> 8) & 255;
  652|  			xferp->data_in[q + 13] = d->logical_block_size & 255;
  653|  			break;
  654|  		case 4:		/*  rigid disk geometry page  */
  655|  			xferp->data_in[q + 0] = pagecode;
  656|  			xferp->data_in[q + 1] = 22;
     | [... lines 657-1362 not shown ...]
 1363|  		 *  Not documented in http://www.danbbs.dk/~dino/
 1364|  		 *		SCSI/SCSI2-D.html.
 1365|  		 *  Google gave the answer "MECHANISM_STATUS" for ATAPI. Hm.
 1366|  		 */
 1367|  
 1368|  		if (xferp->cmd_len < 12) {
 1369|  			fatal("WEIRD LEN?\n");
 1370|  			retlen = 8;
 1371|  		} else {
 1372|  			retlen = xferp->cmd[8] * 256 + xferp->cmd[9];
 1373|  		}
 1374|  
 1375|  		/*  Return data:  */
 1376|  		scsi_transfer_allocbuf(&xferp->data_in_len,
 1377|  		    &xferp->data_in, retlen, 1);
 1378|  
 1379|  		diskimage__return_default_status_and_message(xferp, d);
 1380|  
 1381|  		break;
 1382|  
 1383|  	default:
 1384|  		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
 1385|  		    xferp->cmd[0], id);
 1386|  		// exit(1);
 1387|  	}
 1388|  
 1389|  	debug(" ]\n");
 1390|  
 1391|  	return 1;
 1392|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SCSIMODESENSEPC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SCSIMODESENSEPC: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
