# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ioasicesar` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ioasicesar`, state `open`)

**title:** devices/dev_dec_ioasic.c -- station-address ROM reads return a synthetic pattern -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T66 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-27).  Source URLs: https://github.com/rpajarola/gxemul/commit/e108b546b2e6217ad30bb688b4cbb029755ce230.  Our site at de8c7547: src/devices/dev_dec_ioasic.c:415.  Portable fix: yes -- port rpajarola e108b54.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 415| 			odata = ((relative_addr - IOASIC_SYS_ETHER_ADDRESS(0)) / 4 + 1) * 0x10;

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_dec_ioasic.c b/src/devices/dev_dec_ioasic.c
index 6b2ed1f3..80cb31ae 100644
--- a/src/devices/dev_dec_ioasic.c
+++ b/src/devices/dev_dec_ioasic.c
@@ -412,7 +412,10 @@ DEVICE_ACCESS(dec_ioasic)
 			fatal("[ dec_ioasic: attempt to write to the station's"
 			    " ethernet address. ignored for now. ]\n");
 		} else {
-			odata = ((relative_addr - IOASIC_SYS_ETHER_ADDRESS(0)) / 4 + 1) * 0x10;
+			/* #001: Return a DEC OUI instead of synthetic pattern */
+			int offset = (relative_addr - IOASIC_SYS_ETHER_ADDRESS(0)) / 4;
+			static const uint8_t dec_mac[6] = { 0x08, 0x00, 0x2b, 0x11, 0x22, 0x33 };
+			odata = dec_mac[offset];
 		}
 		break;
```

## Every edited function, after the fix

### `src/devices/dev_dec_ioasic.c` -- post-edit lines 66-452 (`+` marks a line the diff added or the point of a deletion)

```c
   66|  DEVICE_ACCESS(dec_ioasic)
   67|  {
   68|  	struct dec_ioasic_data *d = (struct dec_ioasic_data *) extra;
   69|  	uint64_t idata = 0, odata = 0;
   70|  	// uint64_t curptr;
     | [... lines 71-304 not shown ...]
  305|  		if (writeflag == MEM_WRITE)
  306|  			d->isdn_r_data = idata;
  307|  		else
  308|  			odata = d->isdn_r_data;
  309|  
  310|  		debug("[ dec_ioasic: %s ISDN_R_DATA, data=0x%08" PRIx64 " ]\n",
  311|  			writeflag == MEM_WRITE ? "write to" : "read from",
  312|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  313|  		break;
  314|  
  315|  	case IOASIC_LANCE_DECODE:
  316|  		if (writeflag == MEM_WRITE)
  317|  			d->lance_decode = idata;
  318|  		else
  319|  			odata = d->lance_decode;
  320|  
  321|  		debug("[ dec_ioasic: %s LANCE_DECODE, data=0x%08" PRIx64 " ]\n",
  322|  			writeflag == MEM_WRITE ? "write to" : "read from",
  323|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  324|  		break;
  325|  
  326|  	case IOASIC_SCSI_DECODE:
  327|  		if (writeflag == MEM_WRITE)
  328|  			d->scsi_decode = idata;
  329|  		else
  330|  			odata = d->scsi_decode;
  331|  
  332|  		debug("[ dec_ioasic: %s SCSI_DECODE, data=0x%08" PRIx64 " ]\n",
  333|  			writeflag == MEM_WRITE ? "write to" : "read from",
  334|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  335|  		break;
  336|  
  337|  	case IOASIC_SCC0_DECODE:
  338|  		if (writeflag == MEM_WRITE)
  339|  			d->scc0_decode = idata;
  340|  		else
  341|  			odata = d->scc0_decode;
  342|  
  343|  		debug("[ dec_ioasic: %s SCC0_DECODE, data=0x%08" PRIx64 " ]\n",
  344|  			writeflag == MEM_WRITE ? "write to" : "read from",
  345|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  346|  		break;
  347|  
  348|  	case IOASIC_SCC1_DECODE:
  349|  		if (writeflag == MEM_WRITE)
  350|  			d->scc1_decode = idata;
  351|  		else
  352|  			odata = d->scc1_decode;
  353|  
  354|  		debug("[ dec_ioasic: %s SCC1_DECODE, data=0x%08" PRIx64 " ]\n",
  355|  			writeflag == MEM_WRITE ? "write to" : "read from",
  356|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  357|  		break;
  358|  
  359|  	case IOASIC_FLOPPY_DECODE:
  360|  		if (writeflag == MEM_WRITE)
  361|  			d->floppy_decode = idata;
  362|  		else
  363|  			odata = d->floppy_decode;
  364|  
  365|  		debug("[ dec_ioasic: %s FLOPPY_DECODE, data=0x%08" PRIx64 " ]\n",
  366|  			writeflag == MEM_WRITE ? "write to" : "read from",
  367|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  368|  		break;
  369|  
  370|  	case IOASIC_SCSI_SCR:
  371|  		if (writeflag == MEM_WRITE)
  372|  			d->scsi_scr = idata;
  373|  		else
  374|  			odata = d->scsi_scr;
  375|  
  376|  		debug("[ dec_ioasic: %s SCSI_SCR, data=0x%08" PRIx64 " ]\n",
  377|  			writeflag == MEM_WRITE ? "write to" : "read from",
  378|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  379|  		break;
  380|  
  381|  	case IOASIC_SCSI_SDR0:
  382|  		if (writeflag == MEM_WRITE)
  383|  			d->scsi_sdr0 = idata;
  384|  		else
  385|  			odata = d->scsi_sdr0;
  386|  
  387|  		debug("[ dec_ioasic: %s SCSI_SDR0, data=0x%08" PRIx64 " ]\n",
  388|  			writeflag == MEM_WRITE ? "write to" : "read from",
  389|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  390|  		break;
  391|  
  392|  	case IOASIC_SCSI_SDR1:
  393|  		if (writeflag == MEM_WRITE)
  394|  			d->scsi_sdr1 = idata;
  395|  		else
  396|  			odata = d->scsi_sdr1;
  397|  
  398|  		debug("[ dec_ioasic: %s SCSI_SDR1, data=0x%08" PRIx64 " ]\n",
  399|  			writeflag == MEM_WRITE ? "write to" : "read from",
  400|  			(uint64_t)(writeflag == MEM_WRITE ? idata : odata));
  401|  		break;
  402|  
  403|  
  404|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x00:
  405|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x04:
  406|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x08:
  407|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x0c:
  408|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x10:
  409|  	case IOASIC_SYS_ETHER_ADDRESS(0) + 0x14:
  410|  		/*  Station's ethernet address:  */
  411|  		if (writeflag == MEM_WRITE) {
  412|  			fatal("[ dec_ioasic: attempt to write to the station's"
  413|  			    " ethernet address. ignored for now. ]\n");
  414|  		} else {
  415|+ 			/* #001: Return a DEC OUI instead of synthetic pattern */
  416|+ 			int offset = (relative_addr - IOASIC_SYS_ETHER_ADDRESS(0)) / 4;
  417|+ 			static const uint8_t dec_mac[6] = { 0x08, 0x00, 0x2b, 0x11, 0x22, 0x33 };
  418|+ 			odata = dec_mac[offset];
  419|  		}
  420|  		break;
  421|  
  422|  	/*  The DECstation 5000/125's PROM uses these for cache testing. TODO.  */
  423|  	case 0x0f004:
  424|  	case 0x1f008:
  425|  	case 0x2f00c:
  426|  	case 0x3f010:
  427|  	case 0x4f014:
  428|  	case 0x5f018:
  429|  	case 0x6f01c:
  430|  	case 0x7f020:
  431|  	case 0x8f024:
  432|  	case 0x9f028:
  433|  	case 0xaf02c:
  434|  	case 0xbf030:
  435|  		break;
  436|  
  437|  	default:
  438|  		if (writeflag == MEM_WRITE)
  439|  			fatal("[ dec_ioasic: unimplemented write to address "
  440|  			    "0x%llx, data=0x%08llx ]\n",
  441|  			    (long long)relative_addr, (long long)idata);
  442|  		else
  443|  			fatal("[ dec_ioasic: unimplemented read from address "
  444|  			    "0x%llx ]\n", (long long)relative_addr);
  445|  		// exit(1);
  446|  	}
  447|  
  448|  	if (writeflag == MEM_READ)
  449|  		memory_writemax64(cpu, data, len, odata);
  450|  
  451|  	return 1;
  452|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_IOASICESAR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_IOASICESAR: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
