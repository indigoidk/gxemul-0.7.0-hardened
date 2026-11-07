# GXemul hardened fork -- DRAFT A FIX for one filed issue, `scsimodeselhdr` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `scsimodeselhdr`, state `open`, severity `MED`)

**title:** disk/diskimage_scsicmd.c MODE SELECT -- only NetBSD's exact header is accepted; anything else prints an unlatched `fatal()` hex dump -- WRONG-RESULT (+ log flood; OSF/1, Ultrix)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T76 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-61).  Source URLs: https://github.com/rpajarola/gxemul/commit/d685ed0fb10b82c22d1d5331e1f6e4cb46d64eba, https://github.com/rpajarola/gxemul/commit/39f3fbfac4e2fedca2b3688ceaad845466bdac54.  Our site at de8c7547: src/disk/diskimage_scsicmd.c:1306-1337.  Portable fix: yes -- port rpajarola d685ed0, rpajarola 39f3fbf keeping #133's 256..8192 bound.  Filing check (TRIAGE.md): `stalelbsbound` is a different MODE SELECT defect.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rpajarola d685ed0, rpajarola 39f3fbf keeping #133's 256..8192 bound

## The code at the cited lines

### `src/disk/diskimage_scsicmd.c` around the row's cited line 1306 (HEAD 8d9df658, lines 1186-1391)

```c
 1186| 
 1187| 	case SCSICDROM_READ_DISCINFO:
 1188| 		/*  (Patch from Haavard Eidnes.)  */
 1189| 		debug("CDROM_READ_DISCINFO, cmd[1]=0x%02x", xferp->cmd[1]);
 1190| 		retlen = 34;
 1191| 		scsi_transfer_allocbuf(&xferp->data_in_len,
 1192| 		    &xferp->data_in, retlen, 1);
 1193| 
 1194| 		/*  TODO: Make this more generic!  */
 1195| 		xferp->data_in[0] = retlen-2;	/*  length of info, excl len  */
 1196| 		xferp->data_in[1] = 0;	 /*  length of info-(len field), msb  */
 1197| 		xferp->data_in[2] = 0xE; /*  11=complete ses., 10=fin disc  */
 1198| 		xferp->data_in[3] = 0;   /*  First track on disc  */
 1199| 		xferp->data_in[4] = 1;   /*  Number of sessions, lsb  */
 1200| 		xferp->data_in[5] = 0;   /*  first_track_last_session_lsb  */
 1201| 		xferp->data_in[6] = 0;   /*  last_track_last_session_lsb  */
 1202| 		xferp->data_in[7] = 0x20;/*  various flags  */
 1203| 		xferp->data_in[8] = 0;   /*  CD-ROM disc  */
 1204| 		xferp->data_in[9] = 1;   /*  num sessions, msb  */
 1205| 		xferp->data_in[10] = 0;  /*  first_track_last_session_msb  */
 1206| 		xferp->data_in[11] = 0;  /*  last_track_last_session_msb  */
 1207| 
 1208| 		/*  Lead-in data, for completed cd-rom:  */
 1209| 		for (size_t j=16; j<=23; j++)
 1210| 			xferp->data_in[j] = 0xff;
 1211| 
 1212| 		diskimage__return_default_status_and_message(xferp, d);
 1213| 		break;
 1214| 
 1215| 	case SCSICDROM_READ_TRACKINFO:
 1216| 		/*  (Patch from Haavard Eidnes.)  */
 1217| 		debug("CDROM_READ_TRACKINFO");
 1218| 		retlen = 36;
 1219| 		scsi_transfer_allocbuf(&xferp->data_in_len,
 1220| 		    &xferp->data_in, retlen, 1);
 1221| 
 1222| 		diskimage_recalc_size(d);
 1223| 
 1224| 		size = d->total_size / d->logical_block_size;
 1225| 		if (d->total_size & (d->logical_block_size-1))
 1226| 			size ++;
 1227| 
 1228| 		/*  TODO: Make more generic?  */
 1229| 		/*  TODO: Don't use magic values.  */
 1230| 		xferp->data_in[0] = retlen-2; /*  length of info, excl len  */
 1231| 		xferp->data_in[1] = 0;	      /*  length of info, msb  */
 1232| 		xferp->data_in[2] = 1;	      /*  track#, lsb  */
 1233| 		xferp->data_in[3] = 1;	      /*  session#, lsb  */
 1234| 		xferp->data_in[4] = 0;	      /*  reserved  */
 1235| 		xferp->data_in[5] = 0x6;      /*  trk mode: unintr. data,
 1236| 						  copyable  */
 1237| 		xferp->data_in[6] = 0x81;     /*  trk info: RT + trk mode  */
 1238| 		xferp->data_in[7] = 0x2;      /*  last rec=valid, next w=not
 1239| 						  valid */
 1240| 		/*
 1241| 		 *  track start, next writable, free blcks,
 1242| 		 *  blocking factor
 1243| 		 */
 1244| 		for(size_t j=8; j<=23; j++)
 1245| 			xferp->data_in[j] = 0;
 1246| 
 1247| 		/*  Track size:  */
 1248| 		xferp->data_in[24] = (size >> 24) & 0xff;
 1249| 		xferp->data_in[25] = (size >> 16) & 0xff;
 1250| 		xferp->data_in[26] = (size >> 8) & 0xff;
 1251| 		xferp->data_in[27] = size & 0xff;
 1252| 
 1253| 		/*  Last recorded address, only for dvd; zero out the rest:  */
 1254| 		for (size_t k=28; k<=35; k++)
 1255| 			xferp->data_in[k] = 0;
 1256| 
 1257| 		diskimage__return_default_status_and_message(xferp, d);
 1258| 		break;
 1259| 
 1260| 	case SCSICMD_MODE_SELECT:
 1261| 		debug("[ SCSI MODE_SELECT: ");
 1262| 
 1263| 		/*
 1264| 		 *  TODO:
 1265| 		 *
 1266| 		 *  This is super-hardcoded for NetBSD's usage of mode_select
 1267| 		 *  to set the size of CDROM sectors to 2048.
 1268| 		 */
 1269| 
 1270| 		/*  #285: ask for the 12-byte parameter list, and accept it only
 1271| 		    once all 12 bytes have arrived. The gate used to be
 1272| 		    `data_out_offset == 0`, i.e. it refused an EMPTY buffer but
 1273| 		    accepted a PARTIAL one, and the parse below then read fixed
 1274| 		    offsets up to byte 11 out of a buffer whose tail the
 1275| 		    controller never supplied: a MODE SELECT(6) with 11 of 12
 1276| 		    bytes transferred committed a logical_block_size computed
 1277| 		    from a byte that was never sent. #205's guard does not fire
 1278| 		    on that, because data_out_len IS 12 on re-entry. This is the
 1279| 		    same contract the WRITE gate above already demands of every
 1280| 		    caller, and it is the only data_out gate in this file that
 1281| 		    was not `!= size`.
 1282| 
 1283| 		    The assignment stays BEFORE the test on purpose: data_out_len
 1284| 		    is 0 on first entry, so testing it before setting it would
 1285| 		    compare 0 against 0, never ask for the buffer at all, and
 1286| 		    turn every MODE SELECT into a silent no-op.  */
 1287| 		xferp->data_out_len = 12;	/*  TODO  */
 1288| 		if (xferp->data_out_offset != xferp->data_out_len) {
 1289| 			debug("data_out == NULL, wanting %i bytes ]\n",
 1290| 			    (int)xferp->data_out_len);
 1291| 			return 2;
 1292| 		}
 1293| 
 1294| 		/*  #205: (Codex/Fable) MODE SELECT reads fixed offsets up to byte 11;
 1295| 	    a controller can supply a shorter DATA OUT buffer, so verify it is
 1296| 	    present and >= 12 bytes before indexing it.  */
 1297| 	if (xferp->data_out == NULL || xferp->data_out_len < 12) {
 1298| 		diskimage__return_default_status_and_message(xferp, d);
 1299| 		break;
 1300| 	}
 1301| 
 1302| 	debug("data_out!=NULL (OK), ");
 1303| 
 1304| 		/*  TODO:  Care about cmd?  */
 1305| 
 1306| 		/*  Set sector size to 2048:  */
 1307| 		/*  00 05 00 08 00 03 ca 40 00 00 08 00  */
 1308| 		if (xferp->data_out[0] == 0x00 &&
 1309| 		    xferp->data_out[1] == 0x05 &&
 1310| 		    xferp->data_out[2] == 0x00 &&
 1311| 		    xferp->data_out[3] == 0x08) {
 1312| 			/*  #133: guest-controlled; only accept a sane block
 1313| 			    size, since READ/WRITE transfer sizes are computed
 1314| 			    from it.  */
 1315| 			int new_block_size =
 1316| 			    (xferp->data_out[9] << 16) +
 1317| 			    (xferp->data_out[10] << 8) +
 1318| 			    xferp->data_out[11];
 1319| 			if (new_block_size < 256 || new_block_size > 8192) {
 1320| 				fatal("[ MODE_SELECT: bogus logical_block_size"
 1321| 				    " %i ignored, keeping %i ]\n",
 1322| 				    new_block_size, d->logical_block_size);
 1323| 			} else {
 1324| 				d->logical_block_size = new_block_size;
 1325| 				debug("[ setting logical_block_size to %i ]\n",
 1326| 				    d->logical_block_size);
 1327| 			}
 1328| 		} else {
 1329| 			int j;
 1330| 			fatal("[ unknown MODE_SELECT: cmd =");
 1331| 			for (j=0; j<(ssize_t)xferp->cmd_len; j++)
 1332| 				fatal(" %02x", xferp->cmd[j]);
 1333| 			fatal(", data_out =");
 1334| 			for (j=0; j<(ssize_t)xferp->data_out_len; j++)
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


RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_SCSIMODESELHDR: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
