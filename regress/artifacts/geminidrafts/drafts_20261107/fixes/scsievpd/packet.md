# GXemul hardened fork -- DRAFT A FIX for one filed issue, `scsievpd` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `scsievpd`, state `open`, severity `MED`)

**title:** disk/diskimage_scsicmd.c INQUIRY -- EVPD requests get standard INQUIRY data instead of a VPD page -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T77 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-17).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/554e135a564bd029d4a6dc38341b82fd0879ea20, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/24cb943fd42dbb1fa6285d6a7e1dab89b8a1b6f8.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:363-367.  Portable fix: yes -- port rs6000 554e135, rs6000 24cb943.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 554e135, rs6000 24cb943

## The code at the cited lines

### `src/disk/diskimage_scsicmd.c` around the row's cited line 363 (HEAD 2d25df65, lines 318-408)

```c
  318| 
  319| 	if (d == NULL) {
  320| 		debugmsg_cpu(cpu, SUBSYS_DISK, "scsi",
  321| 		    VERBOSITY_INFO, "%s id %i not connected!",
  322| 		    diskimage_types[type], id);
  323| 
  324| 		// TODO: How to return suitable error?
  325| 		diskimage__return_default_status_and_message(xferp, d);
  326| 		xferp->status[0] = 0x02;	// ?
  327| 		return 0;
  328| 	}
  329| 
  330| 	// TODO: debugmsg:ify the rest of the debug messages...
  331| 	debug("[ diskimage_scsicommand(id=%i) cmd=0x%02x: ", id, xferp->cmd[0]);
  332| 
  333| #if 0
  334| 	fatal("[ diskimage_scsicommand(id=%i) cmd=0x%02x len=%i:",
  335| 	    id, xferp->cmd[0], xferp->cmd_len);
  336| 	for (i=0; i<xferp->cmd_len; i++)
  337| 		fatal(" %02x", xferp->cmd[i]);
  338| 	fatal("\n");
  339| if (xferp->cmd_len > 7 && xferp->cmd[5] == 0x11)
  340| 	single_step = true;
  341| #endif
  342| 
  343| 	switch (xferp->cmd[0]) {
  344| 
  345| 	case SCSICMD_TEST_UNIT_READY:
  346| 		debug("TEST_UNIT_READY");
  347| 		if (xferp->cmd_len != 6)
  348| 			debug(" (weird len=%zu)", xferp->cmd_len);
  349| 
  350| 		/*  TODO: bits 765 of buf[1] contains the LUN  */
  351| 		if (xferp->cmd[1] != 0x00)
  352| 			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  353| 			    "WARNING: TEST_UNIT_READY with cmd[1]=0x%02x"
  354| 			    " not yet implemented", (int)xferp->cmd[1]);
  355| 
  356| 		diskimage__return_default_status_and_message(xferp, d);
  357| 		break;
  358| 
  359| 	case SCSICMD_INQUIRY:
  360| 		debug("INQUIRY");
  361| 		if (xferp->cmd_len != 6)
  362| 			debug(" (weird len=%zu)", xferp->cmd_len);
  363| 		if (xferp->cmd[1] != 0x00) {
  364| 			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  365| 			    "WARNING: INQUIRY with cmd[1]=0x%02x not yet "
  366| 			    "implemented", (int)xferp->cmd[1]);
  367| 		}
  368| 
  369| 		/*  Return values:  */
  370| 		retlen = xferp->cmd[4];
  371| 		if (retlen < 36) {
  372| 			debugmsg(SUBSYS_DISK, "scsi", VERBOSITY_WARNING,
  373| 			    "WARNING: SCSI inquiry len=%i, <36!", retlen);
  374| 			retlen = 36;
  375| 		}
  376| 
  377| 		/*  Return data:  */
  378| 		scsi_transfer_allocbuf(&xferp->data_in_len, &xferp->data_in,
  379| 		    retlen, 1);
  380| 		xferp->data_in[0] = 0x00;  /*  0x00 = Direct-access disk  */
  381| 		xferp->data_in[1] = 0x00;  /*  0x00 = non-removable  */
  382| 		xferp->data_in[2] = 0x02;  /*  SCSI-2  */
  383| #if 0
  384| xferp->data_in[3] = 0x02;	/*  Response data format = SCSI-2  */
  385| #endif
  386| 		xferp->data_in[4] = retlen - 4;	/*  Additional length  */
  387| xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
  388| 		xferp->data_in[6] = 0x04;  /*  ACKREQQ  */
  389| 		xferp->data_in[7] = 0x60;  /*  WBus32, WBus16  */
  390| 
  391| 		/*  These are padded with spaces:  */
  392| 
  393| 		memcpy(xferp->data_in+8,  "GXemul  ", 8);
  394| 		if (diskimage_getname(cpu->machine, id,
  395| 		    type, namebuf, sizeof(namebuf))) {
  396| 			for (size_t j=0; j<sizeof(namebuf); j++) {
  397| 				if (namebuf[j] == 0) {
  398| 					for (; j<sizeof(namebuf); j++)
  399| 						namebuf[j] = ' ';
  400| 					break;
  401| 				}
  402| 			}
  403| 			
  404| 			memcpy(xferp->data_in+16, namebuf, 16);
  405| 		} else
  406| 			memcpy(xferp->data_in+16, "DISK            ", 16);
  407| 		memcpy(xferp->data_in+32, "0   ", 4);
  408| 
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

End with one line: `FIXDRAFT_SCSIEVPD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
