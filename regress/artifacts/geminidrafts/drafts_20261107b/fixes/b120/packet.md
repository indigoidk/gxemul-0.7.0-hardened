# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `b120` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `b120`, state `held`)

**title:** b120u  SCSI: an unknown command is reported to the guest as success

**state_note (head):** [2026-10-22] CARRIES the external-fixes research's T9 (regress/artifacts/research_20261022/TRIAGE.md T9; regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md B: not re-filed): WRITE AND VERIFY(10) falls into this row's default arm, so where a controller reports GOOD its data is never written; VERIFY(10) and RESERVE/RELEASE(6/10) are GOOD by accident (report rows A5-20, A5-21, A5-42; rs6000 75010de, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/75010dedf93747f1c6391430688971a922400418; NetBSD PR pkg/54114, https://gnats.netbsd.org/54114, quotes the SPC answer: CHECK CONDITION, ILLEGAL REQUEST, ASC 0x20).  The per-controller outcomes are this row's own record.  ||  *** L4 WRONG RECORD, CORRECTED IN PLACE 2026-08-27. An adversarial opus pass REFUTED THE MECHANISM THIS ROW STATED BELOW. The defect is real; my explanation of it was false, and the true picture is four different wrong outcomes rather than one. ***

**WHAT I GOT WRONG.** I wrote that `scsi_transfer_alloc()`'s `memset(p, 0, ...)` leaves a status BYTE of 0x00, which the guest reads as GOOD. **`status` is `unsigned char *` (`diskimage.h:196-197`)** -- so the memset leaves `status == NULL` and `status_len == 0`. **There is no zeroed status byte anywhere.** Nothing reads a 0x00 out of that struct. The conclusion happened to hold for one controller, for an entirely different reason.

**WHAT SURVIVES, and it is the structural half:** the `default:` arm is the **only one of 25** that never calls `diskimage__return_default_status_and_message()` or `diskimage__return_check_condition()` -- verified by grepping every case/helper pair -- and it falls through to `return 1`, which the function's own header (`:263-266`) documents as the success token (`2` = expects DATA_OUT, `1` = otherwise ok, `0` = error).

*** THE HONEST STATEMENT: ONE OMISSION, FOUR DIFFERENT WRONG OUTCOMES. ***
  * **`dev_asc.c` -- guest IS told GOOD**, but via an explicit `else fifo_write(0x00)` fallback at `:1284-1292`, which `git log -S` places in the unmodified upstream 0.7.0 import, NOT a fork change. Right conclusion, wrong reason.
  * **`dev_mb89352.c` -- REFUTES the 'told success' claim outright.** `data_in == NULL` sets `phase = PH_STAT` (`:284`); the guest's PH_STAT read takes `p = status (NULL), len = 0`, trips the `read longer than buffer?` arm (`:173`) and **sets `cpu->running = 0`**. The guest is not told anything -- the emulated CPU is STOPPED. **Filed separately as [[mb89352halt]].**
  * **`dev_osiop.c: [... 3640 more characters not shown]

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/disk/diskimage_scsicmd.c` -- AT HEAD, lines 270-1389 (`*` marks a line your previous draft changed)

```c
  270|  {
  271|  	char namebuf[16];
  272|  	int retlen, i, q;
  273|  	uint64_t size;
  274|  	int64_t ofs;
     | [... lines 275-1272 not shown ...]
 1273|  		    accepted a PARTIAL one, and the parse below then read fixed
 1274|  		    offsets up to byte 11 out of a buffer whose tail the
 1275|  		    controller never supplied: a MODE SELECT(6) with 11 of 12
 1276|  		    bytes transferred committed a logical_block_size computed
 1277|  		    from a byte that was never sent. #205's guard does not fire
 1278|  		    on that, because data_out_len IS 12 on re-entry. This is the
 1279|  		    same contract the WRITE gate above already demands of every
 1280|  		    caller, and it is the only data_out gate in this file that
 1281|  		    was not `!= size`.
 1282|  
 1283|  		    The assignment stays BEFORE the test on purpose: data_out_len
 1284|  		    is 0 on first entry, so testing it before setting it would
 1285|  		    compare 0 against 0, never ask for the buffer at all, and
 1286|  		    turn every MODE SELECT into a silent no-op.  */
 1287|  		xferp->data_out_len = 12;	/*  TODO  */
 1288|  		if (xferp->data_out_offset != xferp->data_out_len) {
 1289|  			debug("data_out == NULL, wanting %i bytes ]\n",
 1290|  			    (int)xferp->data_out_len);
 1291|  			return 2;
 1292|  		}
 1293|  
 1294|  		/*  #205: (Codex/Fable) MODE SELECT reads fixed offsets up to byte 11;
 1295|  	    a controller can supply a shorter DATA OUT buffer, so verify it is
 1296|  	    present and >= 12 bytes before indexing it.  */
 1297|  	if (xferp->data_out == NULL || xferp->data_out_len < 12) {
 1298|  		diskimage__return_default_status_and_message(xferp, d);
 1299|  		break;
 1300|  	}
 1301|  
 1302|  	debug("data_out!=NULL (OK), ");
 1303|  
 1304|  		/*  TODO:  Care about cmd?  */
 1305|  
 1306|  		/*  Set sector size to 2048:  */
 1307|  		/*  00 05 00 08 00 03 ca 40 00 00 08 00  */
 1308|  		if (xferp->data_out[0] == 0x00 &&
 1309|  		    xferp->data_out[1] == 0x05 &&
 1310|  		    xferp->data_out[2] == 0x00 &&
 1311|  		    xferp->data_out[3] == 0x08) {
 1312|  			/*  #133: guest-controlled; only accept a sane block
 1313|  			    size, since READ/WRITE transfer sizes are computed
 1314|  			    from it.  */
 1315|  			int new_block_size =
 1316|  			    (xferp->data_out[9] << 16) +
 1317|  			    (xferp->data_out[10] << 8) +
 1318|  			    xferp->data_out[11];
 1319|  			if (new_block_size < 256 || new_block_size > 8192) {
 1320|  				fatal("[ MODE_SELECT: bogus logical_block_size"
 1321|  				    " %i ignored, keeping %i ]\n",
 1322|  				    new_block_size, d->logical_block_size);
 1323|  			} else {
 1324|  				d->logical_block_size = new_block_size;
 1325|  				debug("[ setting logical_block_size to %i ]\n",
 1326|  				    d->logical_block_size);
 1327|  			}
 1328|  		} else {
 1329|  			int j;
 1330|  			fatal("[ unknown MODE_SELECT: cmd =");
 1331|  			for (j=0; j<(ssize_t)xferp->cmd_len; j++)
 1332|  				fatal(" %02x", xferp->cmd[j]);
 1333|  			fatal(", data_out =");
 1334|  			for (j=0; j<(ssize_t)xferp->data_out_len; j++)
 1335|  				fatal(" %02x", xferp->data_out[j]);
 1336|  			fatal(" ]");
 1337|  		}
 1338|  
 1339|  		debug(" ]\n");
 1340|  		diskimage__return_default_status_and_message(xferp, d);
 1341|  		break;
 1342|  
 1343|  	case SCSICMD_PREVENT_ALLOW_REMOVE:
 1344|  		debug("[ SCSI 0x%02x Prevent/allow medium removal: "
 1345|  		    "TODO ]\n", xferp->cmd[0]);
 1346|  
 1347|  		diskimage__return_default_status_and_message(xferp, d);
 1348|  		break;
 1349|  
 1350|  	case 0xbd:
 1351|  		fatal("[ SCSI 0x%02x (len %zu), TODO: ", xferp->cmd[0],
 1352|  		    xferp->cmd_len);
 1353|  		for (i=0; i<(ssize_t)xferp->cmd_len; i++)
 1354|  			fatal(" %02x", xferp->cmd[i]);
 1355|  		fatal(" ]\n");
 1356|  
 1357|  		/*
 1358|  		 *  Used by Windows NT?
 1359|  		 *
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
 1383|* 		// exit(1);
 1384|* 	}
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
    "old": "\tdefault:\n\t\tdebug(\"[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i\",\n\t\t    xferp->cmd[0], id);\n\t\t// exit(1);\n\t}",
    "new": "\tdefault:\n\t\tdebug(\"[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i\",\n\t\t    xferp->cmd[0], id);\n\t\treturn 0;\n\t}",
    "why": "Return 0 (error) for unimplemented commands to avoid falling through to success (1)."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_B120: DEFECT, 3 FINDINGS
1. **Removes defect at every site?** UNSETTLED. The issue explicitly names `dev_asc.c`, `dev_mb89352.c`, and `dev_osiop.c` as having wrong outcomes. The provided text only shows the callee (`diskimage_scsicmd.c`). We cannot confirm if returning `0` causes these specific controller files to correctly report the failure to the guest.
2. **CONTROL FLOW:** DEFECT. The added `return 0;` early exit skips the function's common tail at `src/disk/diskimage_scsicmd.c:1386`: `debug(" ]\n");`. This leaves the `debug("[ UNIMPLEMENTED...` bracket from line 1381 unclosed.
3. **RETURN VALUE:** The path previously fell through to `return 1` (success token); it now returns `0`, which the issue text identifies as the error token. 
4. **What ELSE:** The diff breaks debug log formatting by skipping the closing bracket print.
5. **House idioms:** STYLE. The `UNIMPLEMENTED SCSI command` debug output at line 1381 can be triggered repeatedly by the guest but lacks a `(once)` latch field.
**Findings:**
`src/disk/diskimage_scsicmd.c:1383`, DEFECT, change to `debug(" ]\n"); return 0;`
`dev_asc.c:1`, UNSETTLED, missing `dev_asc.c`, `dev_mb89352.c`, and `dev_osiop.c` to verify caller handling of return 0.
`src/disk/diskimage_scsicmd.c:1381`, STYLE, add a latch to print this diagnostic only once per device.
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

End with two lines: `REVISION_B120: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_B120: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
