# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `scsimodeselhdr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `scsimodeselhdr`, state `open`)

**title:** disk/diskimage_scsicmd.c MODE SELECT -- only NetBSD's exact header is accepted; anything else prints an unlatched `fatal()` hex dump -- WRONG-RESULT (+ log flood; OSF/1, Ultrix)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T76 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-61).  Source URLs: https://github.com/rpajarola/gxemul/commit/d685ed0fb10b82c22d1d5331e1f6e4cb46d64eba, https://github.com/rpajarola/gxemul/commit/39f3fbfac4e2fedca2b3688ceaad845466bdac54.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:1306-1337.  Portable fix: yes -- port rpajarola d685ed0, rpajarola 39f3fbf keeping #133's 256..8192 bound.  Filing check (TRIAGE.md): `stalelbsbound` is a different MODE SELECT defect.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 1308

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/disk/diskimage_scsicmd.c b/src/disk/diskimage_scsicmd.c
index 5de21e05..69bcfafd 100644
--- a/src/disk/diskimage_scsicmd.c
+++ b/src/disk/diskimage_scsicmd.c
@@ -1305,10 +1305,8 @@ xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
 
 		/*  Set sector size to 2048:  */
 		/*  00 05 00 08 00 03 ca 40 00 00 08 00  */
-		if (xferp->data_out[0] == 0x00 &&
-		    xferp->data_out[1] == 0x05 &&
-		    xferp->data_out[2] == 0x00 &&
-		    xferp->data_out[3] == 0x08) {
+		/* #NNN: Relax check to only require block descriptor length 0x08 */
+		if (xferp->data_out[3] == 0x08) {
 			/*  #133: guest-controlled; only accept a sane block
 			    size, since READ/WRITE transfer sizes are computed
 			    from it.  */
@@ -1327,13 +1325,13 @@ xferp->data_in[4] = 0x2c - 4;	/*  Additional length  */
 			}
 		} else {
 			int j;
-			fatal("[ unknown MODE_SELECT: cmd =");
+			debug("[ unknown MODE_SELECT: cmd =");
 			for (j=0; j<(ssize_t)xferp->cmd_len; j++)
-				fatal(" %02x", xferp->cmd[j]);
-			fatal(", data_out =");
+				debug(" %02x", xferp->cmd[j]);
+			debug(", data_out =");
 			for (j=0; j<(ssize_t)xferp->data_out_len; j++)
-				fatal(" %02x", xferp->data_out[j]);
-			fatal(" ]");
+				debug(" %02x", xferp->data_out[j]);
+			debug(" ]");
 		}
 
 		debug(" ]\n");
```

## Every edited function, after the fix

### `src/disk/diskimage_scsicmd.c` -- post-edit lines 270-1387 (`+` marks a line the diff added or the point of a deletion)

```c
  270|  {
  271|  	char namebuf[16];
  272|  	int retlen, i, q;
  273|  	uint64_t size;
  274|  	int64_t ofs;
     | [... lines 275-1197 not shown ...]
 1198|  		xferp->data_in[3] = 0;   /*  First track on disc  */
 1199|  		xferp->data_in[4] = 1;   /*  Number of sessions, lsb  */
 1200|  		xferp->data_in[5] = 0;   /*  first_track_last_session_lsb  */
 1201|  		xferp->data_in[6] = 0;   /*  last_track_last_session_lsb  */
 1202|  		xferp->data_in[7] = 0x20;/*  various flags  */
 1203|  		xferp->data_in[8] = 0;   /*  CD-ROM disc  */
 1204|  		xferp->data_in[9] = 1;   /*  num sessions, msb  */
 1205|  		xferp->data_in[10] = 0;  /*  first_track_last_session_msb  */
 1206|  		xferp->data_in[11] = 0;  /*  last_track_last_session_msb  */
 1207|  
 1208|  		/*  Lead-in data, for completed cd-rom:  */
 1209|  		for (size_t j=16; j<=23; j++)
 1210|  			xferp->data_in[j] = 0xff;
 1211|  
 1212|  		diskimage__return_default_status_and_message(xferp, d);
 1213|  		break;
 1214|  
 1215|  	case SCSICDROM_READ_TRACKINFO:
 1216|  		/*  (Patch from Haavard Eidnes.)  */
 1217|  		debug("CDROM_READ_TRACKINFO");
 1218|  		retlen = 36;
 1219|  		scsi_transfer_allocbuf(&xferp->data_in_len,
 1220|  		    &xferp->data_in, retlen, 1);
 1221|  
 1222|  		diskimage_recalc_size(d);
 1223|  
 1224|  		size = d->total_size / d->logical_block_size;
 1225|  		if (d->total_size & (d->logical_block_size-1))
 1226|  			size ++;
 1227|  
 1228|  		/*  TODO: Make more generic?  */
 1229|  		/*  TODO: Don't use magic values.  */
 1230|  		xferp->data_in[0] = retlen-2; /*  length of info, excl len  */
 1231|  		xferp->data_in[1] = 0;	      /*  length of info, msb  */
 1232|  		xferp->data_in[2] = 1;	      /*  track#, lsb  */
 1233|  		xferp->data_in[3] = 1;	      /*  session#, lsb  */
 1234|  		xferp->data_in[4] = 0;	      /*  reserved  */
 1235|  		xferp->data_in[5] = 0x6;      /*  trk mode: unintr. data,
 1236|  						  copyable  */
 1237|  		xferp->data_in[6] = 0x81;     /*  trk info: RT + trk mode  */
 1238|  		xferp->data_in[7] = 0x2;      /*  last rec=valid, next w=not
 1239|  						  valid */
 1240|  		/*
 1241|  		 *  track start, next writable, free blcks,
 1242|  		 *  blocking factor
 1243|  		 */
 1244|  		for(size_t j=8; j<=23; j++)
 1245|  			xferp->data_in[j] = 0;
 1246|  
 1247|  		/*  Track size:  */
 1248|  		xferp->data_in[24] = (size >> 24) & 0xff;
 1249|  		xferp->data_in[25] = (size >> 16) & 0xff;
 1250|  		xferp->data_in[26] = (size >> 8) & 0xff;
 1251|  		xferp->data_in[27] = size & 0xff;
 1252|  
 1253|  		/*  Last recorded address, only for dvd; zero out the rest:  */
 1254|  		for (size_t k=28; k<=35; k++)
 1255|  			xferp->data_in[k] = 0;
 1256|  
 1257|  		diskimage__return_default_status_and_message(xferp, d);
 1258|  		break;
 1259|  
 1260|  	case SCSICMD_MODE_SELECT:
 1261|  		debug("[ SCSI MODE_SELECT: ");
 1262|  
 1263|  		/*
 1264|  		 *  TODO:
 1265|  		 *
 1266|  		 *  This is super-hardcoded for NetBSD's usage of mode_select
 1267|  		 *  to set the size of CDROM sectors to 2048.
 1268|  		 */
 1269|  
 1270|  		/*  #285: ask for the 12-byte parameter list, and accept it only
 1271|  		    once all 12 bytes have arrived. The gate used to be
 1272|  		    `data_out_offset == 0`, i.e. it refused an EMPTY buffer but
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
 1308|+ 		/* #NNN: Relax check to only require block descriptor length 0x08 */
 1309|+ 		if (xferp->data_out[3] == 0x08) {
 1310|  			/*  #133: guest-controlled; only accept a sane block
 1311|  			    size, since READ/WRITE transfer sizes are computed
 1312|  			    from it.  */
 1313|  			int new_block_size =
 1314|  			    (xferp->data_out[9] << 16) +
 1315|  			    (xferp->data_out[10] << 8) +
 1316|  			    xferp->data_out[11];
 1317|  			if (new_block_size < 256 || new_block_size > 8192) {
 1318|  				fatal("[ MODE_SELECT: bogus logical_block_size"
 1319|  				    " %i ignored, keeping %i ]\n",
 1320|  				    new_block_size, d->logical_block_size);
 1321|  			} else {
 1322|  				d->logical_block_size = new_block_size;
 1323|  				debug("[ setting logical_block_size to %i ]\n",
 1324|  				    d->logical_block_size);
 1325|  			}
 1326|  		} else {
 1327|  			int j;
 1328|+ 			debug("[ unknown MODE_SELECT: cmd =");
 1329|  			for (j=0; j<(ssize_t)xferp->cmd_len; j++)
 1330|+ 				debug(" %02x", xferp->cmd[j]);
 1331|+ 			debug(", data_out =");
 1332|  			for (j=0; j<(ssize_t)xferp->data_out_len; j++)
 1333|+ 				debug(" %02x", xferp->data_out[j]);
 1334|+ 			debug(" ]");
 1335|  		}
 1336|  
 1337|  		debug(" ]\n");
 1338|  		diskimage__return_default_status_and_message(xferp, d);
 1339|  		break;
 1340|  
 1341|  	case SCSICMD_PREVENT_ALLOW_REMOVE:
 1342|  		debug("[ SCSI 0x%02x Prevent/allow medium removal: "
 1343|  		    "TODO ]\n", xferp->cmd[0]);
 1344|  
 1345|  		diskimage__return_default_status_and_message(xferp, d);
 1346|  		break;
 1347|  
 1348|  	case 0xbd:
 1349|  		fatal("[ SCSI 0x%02x (len %zu), TODO: ", xferp->cmd[0],
 1350|  		    xferp->cmd_len);
 1351|  		for (i=0; i<(ssize_t)xferp->cmd_len; i++)
 1352|  			fatal(" %02x", xferp->cmd[i]);
 1353|  		fatal(" ]\n");
 1354|  
 1355|  		/*
 1356|  		 *  Used by Windows NT?
 1357|  		 *
 1358|  		 *  Not documented in http://www.danbbs.dk/~dino/
 1359|  		 *		SCSI/SCSI2-D.html.
 1360|  		 *  Google gave the answer "MECHANISM_STATUS" for ATAPI. Hm.
 1361|  		 */
 1362|  
 1363|  		if (xferp->cmd_len < 12) {
 1364|  			fatal("WEIRD LEN?\n");
 1365|  			retlen = 8;
 1366|  		} else {
 1367|  			retlen = xferp->cmd[8] * 256 + xferp->cmd[9];
 1368|  		}
 1369|  
 1370|  		/*  Return data:  */
 1371|  		scsi_transfer_allocbuf(&xferp->data_in_len,
 1372|  		    &xferp->data_in, retlen, 1);
 1373|  
 1374|  		diskimage__return_default_status_and_message(xferp, d);
 1375|  
 1376|  		break;
 1377|  
 1378|  	default:
 1379|  		debug("[ UNIMPLEMENTED SCSI command 0x%02x, disk id=%i",
 1380|  		    xferp->cmd[0], id);
 1381|  		// exit(1);
 1382|  	}
 1383|  
 1384|  	debug(" ]\n");
 1385|  
 1386|  	return 1;
 1387|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SCSIMODESELHDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SCSIMODESELHDR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
