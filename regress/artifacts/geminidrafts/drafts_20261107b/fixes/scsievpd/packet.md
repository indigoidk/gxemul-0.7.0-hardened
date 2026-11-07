# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `scsievpd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `scsievpd`, state `open`)

**title:** disk/diskimage_scsicmd.c INQUIRY -- EVPD requests get standard INQUIRY data instead of a VPD page -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T77 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-17).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/554e135a564bd029d4a6dc38341b82fd0879ea20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:363-367.  Portable fix: yes -- port rs6000 554e135, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/disk/diskimage_scsicmd.c` -- AT HEAD, lines 270-1389 (`*` marks a line your previous draft changed)

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
  367|* 		}
  368|  
  369|  		/*  Return values:  */
  370|  		retlen = xferp->cmd[4];
  371|  		if (retlen < 36) {
  372|  			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  373|  			    "WARNING: SCSI inquiry len=%i, <36!", retlen);
  374|  			retlen = 36;
  375|  		}
  376|  
  377|  		/*  Return data:  */
  378|  		scsi_transfer_allocbuf(&xferp->data_in_len, &xferp->data_in,
  379|  		    retlen, 1);
  380|  		xferp->data_in[0] = 0x00;  /*  0x00 = Direct-access disk  */
  381|  		xferp->data_in[1] = 0x00;  /*  0x00 = non-removable  */
  382|  		xferp->data_in[2] = 0x02;  /*  SCSI-2  */
  383|  #if 0
  384|  xferp->data_in[3] = 0x02;	/*  Response data format = SCSI-2  */
  385|  #endif
  386|  		xferp->data_in[4] = retlen - 4;	/*  Additional length  */
  387|  xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
  388|  		xferp->data_in[6] = 0x04;  /*  ACKREQQ  */
  389|  		xferp->data_in[7] = 0x60;  /*  WBus32, WBus16  */
  390|  
  391|  		/*  These are padded with spaces:  */
  392|  
  393|  		memcpy(xferp->data_in+8,  "GXemul  ", 8);
  394|  		if (diskimage_getname(cpu->machine, id,
  395|  		    type, namebuf, sizeof(namebuf))) {
  396|  			for (size_t j=0; j<sizeof(namebuf); j++) {
  397|  				if (namebuf[j] == 0) {
  398|  					for (; j<sizeof(namebuf); j++)
  399|  						namebuf[j] = ' ';
  400|  					break;
  401|  				}
  402|  			}
  403|  			
  404|  			memcpy(xferp->data_in+16, namebuf, 16);
  405|  		} else
  406|  			memcpy(xferp->data_in+16, "DISK            ", 16);
  407|  		memcpy(xferp->data_in+32, "0   ", 4);
  408|  
  409|  		/*
  410|  		 *  Some Ultrix kernels want specific responses from
  411|  		 *  the drives.
  412|  		 */
  413|  
  414|  		if (machine->machine_type == MACHINE_PMAX) {
  415|  			/*  DEC, RZ25 (rev 0900) = 832527 sectors  */
  416|  			/*  DEC, RZ58 (rev 2000) = 2698061 sectors  */
  417|  			memcpy(xferp->data_in+8,  "DEC     ", 8);
  418|  			memcpy(xferp->data_in+16, "RZ58     (C) DEC", 16);
  419|  			memcpy(xferp->data_in+32, "2000", 4);
  420|  		}
  421|  
  422|  		/*  Some data is different for CD-ROM drives:  */
  423|  		if (d->is_a_cdrom) {
  424|  			xferp->data_in[0] = 0x05;  /*  0x05 = CD-ROM  */
  425|  			xferp->data_in[1] = 0x80;  /*  0x80 = removable  */
  426|  			/*  memcpy(xferp->data_in+16, "CD-ROM          ", 16);*/
  427|  
     | [... lines 428-1359 not shown ...]
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
    "old": "\t\tif (xferp->cmd[1] != 0x00) {\n\t\t\tdebugmsg(SUBSYS_DISK, \"scsi\", VERBOSITY_WARNING,\n\t\t\t    \"WARNING: INQUIRY with cmd[1]=0x%02x not yet \"\n\t\t\t    \"implemented\", (int)xferp->cmd[1]);\n\t\t}",
    "new": "\t\tif (xferp->cmd[1] != 0x00) {\n\t\t\tdebugmsg(SUBSYS_DISK, \"scsi\", VERBOSITY_WARNING,\n\t\t\t    \"WARNING: INQUIRY with cmd[1]=0x%02x not yet \"\n\t\t\t    \"implemented\", (int)xferp->cmd[1]);\n\t\t\t/* #T77: Decline EVPD with Check Condition instead of standard data */\n\t\t\tdiskimage__return_default_status_and_message(xferp, d);\n\t\t\txferp->status[0] = 0x02;\n\t\t\treturn 0;\n\t\t}",
    "why": "Decline non-zero cmd[1] requests (like EVPD) with Check Condition to prevent returning standard INQUIRY data when VPD pages are requested."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_SCSIEVPD: DEFECT, 2 FINDINGS
1. **Defect removed:** Yes, the diff successfully intercepts EVPD requests (where `cmd[1] != 0x00`) and prevents the device from falling through to return standard INQUIRY data. It addresses the site named in the issue.
2. **CONTROL FLOW:** Yes, the added `return 0;` at line 370 skips the common tail of the function. Specifically, it skips line 1390 `debug(" ]\n");` and the standard successful exit line 1392 `return 1;`.
3. **RETURN VALUE:** Yes, the EVPD path now returns `0` instead of the original `1`. In this function, returning `1` implies the SCSI command was successfully processed by the emulator's device model (even if the SCSI status returned to the guest is a Check Condition error), whereas returning `0` implies a fatal emulator-level framework or dispatch failure (e.g., `cmd == NULL` or missing buffers).
4. **What ELSE changes:** The diff actively sets `xferp->status[0] = 0x02` (Check Condition) and invokes `diskimage__return_default_status_and_message(xferp, d)` to populate sense data before its early exit.
5. **House idioms:** The `debugmsg` block at line 364 (which the fix expands upon) logs a warning guest software can trigger repeatedly. It violates the house idiom by not employing a static latch or containing `(once)` in the message.
**Findings:**
- `src/disk/diskimage_scsicmd.c:370` DEFECT. The code improperly aborts emulator dispatch rather than concluding the SCSI command. Fix in one line: `break;`
- `src/disk/diskimage_scsicmd.c:364` STYLE. A guest can spam this warning. Fix in one line: Add a static latch and `(once)` to the log string.
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

End with two lines: `REVISION_SCSIEVPD: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_SCSIEVPD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
