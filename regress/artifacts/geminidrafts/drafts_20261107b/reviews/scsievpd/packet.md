# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `scsievpd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `scsievpd`, state `open`)

**title:** disk/diskimage_scsicmd.c INQUIRY -- EVPD requests get standard INQUIRY data instead of a VPD page -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T77 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-17).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/554e135a564bd029d4a6dc38341b82fd0879ea20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:363-367.  Portable fix: yes -- port rs6000 554e135, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 363

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/disk/diskimage_scsicmd.c b/src/disk/diskimage_scsicmd.c
index 5de21e05..55835879 100644
--- a/src/disk/diskimage_scsicmd.c
+++ b/src/disk/diskimage_scsicmd.c
@@ -364,6 +364,10 @@ if (xferp->cmd_len > 7 && xferp->cmd[5] == 0x11)
 			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
 			    "WARNING: INQUIRY with cmd[1]=0x%02x not yet "
 			    "implemented", (int)xferp->cmd[1]);
+			/* #T77: Decline EVPD with Check Condition instead of standard data */
+			diskimage__return_default_status_and_message(xferp, d);
+			xferp->status[0] = 0x02;
+			break;
 		}
 
 		/*  Return values:  */
```

## Every edited function, after the fix

### `src/disk/diskimage_scsicmd.c` -- post-edit lines 270-1393 (`+` marks a line the diff added or the point of a deletion)

```c
  270|  {
  271|  	char namebuf[16];
  272|  	int retlen, i, q;
  273|  	uint64_t size;
  274|  	int64_t ofs;
  275|  	int pagecode;
  276|  	struct machine *machine = cpu->machine;
  277|  	struct diskimage *d;
  278|  
  279|  	if (machine == NULL) {
  280|  		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  281|  		    VERBOSITY_ERROR, "machine == NULL");
  282|  		return 0;
  283|  	}
  284|  
  285|  	d = machine->first_diskimage;
  286|  	while (d != NULL) {
  287|  		if (d->type == type && d->id == id)
  288|  			break;
  289|  		d = d->next;
  290|  	}
  291|  
  292|  	if (xferp->cmd == NULL) {
  293|  		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  294|  		    VERBOSITY_ERROR, "cmd == NULL");
  295|  		return 0;
  296|  	}
  297|  
  298|  	if (xferp->cmd_len < 1) {
  299|  		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  300|  		    VERBOSITY_ERROR, "cmd_len = %zu",
  301|  		    xferp->cmd_len);
  302|  		return 0;
  303|  	}
  304|  
  305|  	{
  306|  		/*  #113: validate cmd_len against the CDB group length so the
  307|  		    per-opcode handlers below can't read past the controller-
  308|  		    sized cmd[] buffer on a short CDB.  */
  309|  		static const int cdb_group_len[8] = { 6,10,10,6,16,12,6,6 };
  310|  		int need = cdb_group_len[(xferp->cmd[0] >> 5) & 7];
  311|  		if (xferp->cmd_len < (size_t)need) {
  312|  			debugmsg_cpu(cpu, SUBSYS_DISK, "scsi", VERBOSITY_ERROR,
  313|  			    "short CDB: cmd_len %zu < %i (op 0x%02x)",
  314|  			    xferp->cmd_len, need, xferp->cmd[0]);
  315|  			return 0;
  316|  		}
  317|  	}
  318|  
  319|  	if (d == NULL) {
  320|  		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  321|  		    VERBOSITY_INFO, "%s id %i not connected!",
  322|  		    diskimage_types[type], id);
  323|  
  324|  		// TODO: How to return suitable error?
  325|  		diskimage__return_default_status_and_message(xferp, d);
  326|  		xferp->status[0] = 0x02;	// ?
  327|  		return 0;
  328|  	}
  329|  
  330|  	// TODO: debugmsg:ify the rest of the debug messages...
  331|  	debug("[ diskimage_scsicommand(id=%i) cmd=0x%02x: ", id, xferp->cmd[0]);
  332|  
  333|  #if 0
  334|  	fatal("[ diskimage_scsicommand(id=%i) cmd=0x%02x len=%i:",
  335|  	    id, xferp->cmd[0], xferp->cmd_len);
  336|  	for (i=0; i<xferp->cmd_len; i++)
  337|  		fatal(" %02x", xferp->cmd[i]);
  338|  	fatal("\n");
  339|  if (xferp->cmd_len > 7 && xferp->cmd[5] == 0x11)
  340|  	single_step = true;
  341|  #endif
  342|  
  343|  	switch (xferp->cmd[0]) {
  344|  
  345|  	case SCSICMD_TEST_UNIT_READY:
  346|  		debug("TEST_UNIT_READY");
  347|  		if (xferp->cmd_len != 6)
  348|  			debug(" (weird len=%zu)", xferp->cmd_len);
  349|  
  350|  		/*  TODO: bits 765 of buf[1] contains the LUN  */
  351|  		if (xferp->cmd[1] != 0x00)
  352|  			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  353|  			    "WARNING: TEST_UNIT_READY with cmd[1]=0x%02x"
  354|  			    " not yet implemented", (int)xferp->cmd[1]);
  355|  
  356|  		diskimage__return_default_status_and_message(xferp, d);
  357|  		break;
  358|  
  359|  	case SCSICMD_INQUIRY:
  360|  		debug("INQUIRY");
  361|  		if (xferp->cmd_len != 6)
  362|  			debug(" (weird len=%zu)", xferp->cmd_len);
  363|  		if (xferp->cmd[1] != 0x00) {
  364|  			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  365|  			    "WARNING: INQUIRY with cmd[1]=0x%02x not yet "
  366|  			    "implemented", (int)xferp->cmd[1]);
  367|+ 			/* #T77: Decline EVPD with Check Condition instead of standard data */
  368|+ 			diskimage__return_default_status_and_message(xferp, d);
  369|+ 			xferp->status[0] = 0x02;
  370|+ 			break;
  371|  		}
  372|  
  373|  		/*  Return values:  */
  374|  		retlen = xferp->cmd[4];
  375|  		if (retlen < 36) {
  376|  			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  377|  			    "WARNING: SCSI inquiry len=%i, <36!", retlen);
  378|  			retlen = 36;
  379|  		}
  380|  
  381|  		/*  Return data:  */
  382|  		scsi_transfer_allocbuf(&xferp->data_in_len, &xferp->data_in,
  383|  		    retlen, 1);
  384|  		xferp->data_in[0] = 0x00;  /*  0x00 = Direct-access disk  */
  385|  		xferp->data_in[1] = 0x00;  /*  0x00 = non-removable  */
  386|  		xferp->data_in[2] = 0x02;  /*  SCSI-2  */
  387|  #if 0
  388|  xferp->data_in[3] = 0x02;	/*  Response data format = SCSI-2  */
  389|  #endif
  390|  		xferp->data_in[4] = retlen - 4;	/*  Additional length  */
  391|  xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
  392|  		xferp->data_in[6] = 0x04;  /*  ACKREQQ  */
  393|  		xferp->data_in[7] = 0x60;  /*  WBus32, WBus16  */
  394|  
  395|  		/*  These are padded with spaces:  */
  396|  
  397|  		memcpy(xferp->data_in+8,  "GXemul  ", 8);
  398|  		if (diskimage_getname(cpu->machine, id,
  399|  		    type, namebuf, sizeof(namebuf))) {
  400|  			for (size_t j=0; j<sizeof(namebuf); j++) {
  401|  				if (namebuf[j] == 0) {
  402|  					for (; j<sizeof(namebuf); j++)
  403|  						namebuf[j] = ' ';
  404|  					break;
  405|  				}
  406|  			}
  407|  			
  408|  			memcpy(xferp->data_in+16, namebuf, 16);
  409|  		} else
  410|  			memcpy(xferp->data_in+16, "DISK            ", 16);
  411|  		memcpy(xferp->data_in+32, "0   ", 4);
  412|  
  413|  		/*
  414|  		 *  Some Ultrix kernels want specific responses from
  415|  		 *  the drives.
  416|  		 */
  417|  
  418|  		if (machine->machine_type == MACHINE_PMAX) {
  419|  			/*  DEC, RZ25 (rev 0900) = 832527 sectors  */
  420|  			/*  DEC, RZ58 (rev 2000) = 2698061 sectors  */
  421|  			memcpy(xferp->data_in+8,  "DEC     ", 8);
  422|  			memcpy(xferp->data_in+16, "RZ58     (C) DEC", 16);
  423|  			memcpy(xferp->data_in+32, "2000", 4);
  424|  		}
  425|  
  426|  		/*  Some data is different for CD-ROM drives:  */
  427|  		if (d->is_a_cdrom) {
  428|  			xferp->data_in[0] = 0x05;  /*  0x05 = CD-ROM  */
  429|  			xferp->data_in[1] = 0x80;  /*  0x80 = removable  */
  430|  			/*  memcpy(xferp->data_in+16, "CD-ROM          ", 16);*/
     | [... lines 431-1363 not shown ...]
 1364|  		 *  Not documented in http://www.danbbs.dk/~dino/
 1365|  		 *		SCSI/SCSI2-D.html.
 1366|  		 *  Google gave the answer "MECHANISM_STATUS" for ATAPI. Hm.
 1367|  		 */
 1368|  
 1369|  		if (xferp->cmd_len < 12) {
 1370|  			fatal("WEIRD LEN?\n");
 1371|  			retlen = 8;
 1372|  		} else {
 1373|  			retlen = xferp->cmd[8] * 256 + xferp->cmd[9];
 1374|  		}
 1375|  
 1376|  		/*  Return data:  */
 1377|  		scsi_transfer_allocbuf(&xferp->data_in_len,
 1378|  		    &xferp->data_in, retlen, 1);
 1379|  
 1380|  		diskimage__return_default_status_and_message(xferp, d);
 1381|  
 1382|  		break;
 1383|  
 1384|  	default:
 1385|  		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
 1386|  		    xferp->cmd[0], id);
 1387|  		// exit(1);
 1388|  	}
 1389|  
 1390|  	debug(" ]\n");
 1391|  
 1392|  	return 1;
 1393|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SCSIEVPD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SCSIEVPD: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
