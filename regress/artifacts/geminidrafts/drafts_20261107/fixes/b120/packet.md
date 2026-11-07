# GXemul hardened fork -- DRAFT A FIX for one filed issue, `b120` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `b120`, state `held`, severity `-`)

**title:** b120u  SCSI: an unknown command is reported to the guest as success

**state_note (head):**

[2026-10-22] CARRIES the external-fixes research's T9 (regress/artifacts/research_20261022/TRIAGE.md T9; regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B: not re-filed): WRITE AND VERIFY(10) falls into this row's default arm, so where a controller reports GOOD its data is never written; VERIFY(10) and RESERVE/RELEASE(6/10) are GOOD by accident (report rows A5-20, A5-21, A5-42; rs6000 75010de, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/75010dedf93747f1c6391430688971a922400418; NetBSD PR pkg/54114, https://gnats.netbsd.org/54114, quotes the SPC answer: CHECK CONDITION, ILLEGAL REQUEST, ASC 0x20).  The per-controller outcomes are this row's own record.  ||  *** L4 WRONG RECORD, CORRECTED IN PLACE 2026-08-27. An adversarial opus pass REFUTED THE MECHANISM THIS ROW STATED BELOW. The defect is real; my explanation of it was false, and the true picture is four different wrong outcomes rather than one. ***

**WHAT I GOT WRONG.** I wrote that `scsi_transfer_alloc()`'s `memset(p, 0, ...)` leaves a status BYTE of 0x00, which the guest reads as GOOD. **`status` is `unsigned char *` (`diskimage.h:196-197`)** -- so the memset leaves `status == NULL` and `status_len == 0`. **There is no zeroed status byte anywhere.** Nothing reads a 0x00 out of that struct. The conclusion happened to hold for one controller, for an entirely different reason.

**WHAT SURVIVES, and it is the structural half:** the `default:` arm is the **only one of 25** that never calls `diskimage__return_default_status_and_message()` or `diskimage__return_check_condition()` -- verified by grepping every case/helper pair -- and it falls through to `return 1`, which the function's own header (`:263-266`) documents as the success token (`2` = expects DATA_OUT, `1` = otherwise ok, `0` = error).

*** THE HONEST STATEMENT: ONE OMISSION, FOUR DIFFERENT WRONG OUTCOMES. ***
  * **`dev_asc.c` -- guest IS told GOOD**, but via an explicit `else fifo_write(0x00)` fallback at `:1284-1292`, which `git log -S` places in the unmodified upstream 0.7.0 import, NOT a fork change. Right conclusion, wrong reason.
  * **`dev_mb89352.c` -- REFUTES the 'told success' claim outright.** `data_in == NULL` sets `phase = PH_STAT` (`:284`); the guest's PH_STAT read takes `p = status (NULL), len = 0`, trips the `read longer than buffer?` arm (`:173`) and **sets `cpu->running = 0`**. The guest is not told anything -- the emulated CPU is STOPPED. **Filed separately as [[mb89352halt]].**
  * **`dev_osiop.c:573-582`** -- `while (... && i < status_len)` with `status_len == 0` writes **no status byte at all**; the guest's destination memory keeps its prior contents.
  * **`dev_wdc.c` (ATAPI)** -- `atapi_st->status` is read nowhere in the file; `res == 1` with `data_in == NULL` gives `PHASE_COMPLETED` with `WDCS_ERR` unset: a successful packet command.

> **That is a BETTER case than the row originally made, not a weaker one** -- a single omitted completion step producing four distinct wrong behaviours across four controllers. But it is not the claim as written, and the claim as written was the one being ranked.

**A SECOND CONSEQUENCE THE ORIGINAL RECORD MISSED:** the helper also RETIRES LATCHED SENSE (the `#417` fix, `:187-188`). The `default:` arm skips that too -- so an unimplemented command following a failed one leaves `sense_key/asc/ascq` latched, and a follow-up REQUEST SENSE attributes the OLD failure to the command that just ran. That is exactly the regression `#417` was written to [... 2640 more characters not shown]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- requires explicit check condition return for unknown SCSI commands.

## The code at the cited lines

### `src/disk/diskimage_scsicmd.c` around the row's cited line 1380 (HEAD 2d25df65, lines 1335-1391)

```c
 1335| 				fatal(" %02x", xferp->data_out[j]);
 1336| 			fatal(" ]");
 1337| 		}
 1338| 
 1339| 		debug(" ]\n");
 1340| 		diskimage__return_default_status_and_message(xferp, d);
 1341| 		break;
 1342| 
 1343| 	case SCSICMD_PREVENT_ALLOW_REMOVE:
 1344| 		debug("[ SCSI 0x%02x Prevent/allow medium removal: "
 1345| 		    "TODO ]\n", xferp->cmd[0]);
 1346| 
 1347| 		diskimage__return_default_status_and_message(xferp, d);
 1348| 		break;
 1349| 
 1350| 	case 0xbd:
 1351| 		fatal("[ SCSI 0x%02x (len %zu), TODO: ", xferp->cmd[0],
 1352| 		    xferp->cmd_len);
 1353| 		for (i=0; i<(ssize_t)xferp->cmd_len; i++)
 1354| 			fatal(" %02x", xferp->cmd[i]);
 1355| 		fatal(" ]\n");
 1356| 
 1357| 		/*
 1358| 		 *  Used by Windows NT?
 1359| 		 *
 1360| 		 *  Not documented in http://www.danbbs.dk/~dino/
 1361| 		 *		SCSI/SCSI2-D.html.
 1362| 		 *  Google gave the answer "MECHANISM_STATUS" for ATAPI. Hm.
 1363| 		 */
 1364| 
 1365| 		if (xferp->cmd_len < 12) {
 1366| 			fatal("WEIRD LEN?\n");
 1367| 			retlen = 8;
 1368| 		} else {
 1369| 			retlen = xferp->cmd[8] * 256 + xferp->cmd[9];
 1370| 		}
 1371| 
 1372| 		/*  Return data:  */
 1373| 		scsi_transfer_allocbuf(&xferp->data_in_len,
 1374| 		    &xferp->data_in, retlen, 1);
 1375| 
 1376| 		diskimage__return_default_status_and_message(xferp, d);
 1377| 
 1378| 		break;
 1379| 
 1380| 	default:
 1381| 		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
 1382| 		    xferp->cmd[0], id);
 1383| 		// exit(1);
 1384| 	}
 1385| 
 1386| 	debug(" ]\n");
 1387| 
 1388| 	return 1;
 1389| }
 1390| 
 1391| 
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

End with one line: `FIXDRAFT_B120: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
