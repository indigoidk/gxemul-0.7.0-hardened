# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `mb89352psns` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `mb89352psns`, state `open`)

**title:** devices/dev_mb89352.c -- PSNS writes are stored instead of going to SDGC, and BUS_REL does not clear PSNS -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T91 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-27, C U9(c)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c.  Our site at de8c7547: src/devices/dev_mb89352.c:562-569.  Portable fix: yes -- port upstream a1cafe7c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `d->reg[regnr] = idata;` at line 564 stores to PSNS, and BUS_REL is not processed there.

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_mb89352.c b/src/devices/dev_mb89352.c
index 179a47a2..7dc19913 100644
--- a/src/devices/dev_mb89352.c
+++ b/src/devices/dev_mb89352.c
@@ -561,11 +561,14 @@ DEVICE_ACCESS(mb89352)
 
 	case PSNS:
 		if (writeflag == MEM_WRITE) {
-			d->reg[regnr] = idata;
-			debugmsg_cpu(cpu, d->subsys, "",
-			    VERBOSITY_WARNING,
-		    	    "unimplemented write to PSNS/SDGC: 0x%x",
-			    (int) idata);
+			if (idata == SCMD_BUS_REL) {
+				d->reg[PSNS] = 0;
+			} else {
+				debugmsg_cpu(cpu, d->subsys, "",
+				    VERBOSITY_WARNING,
+			    	    "unimplemented write to PSNS/SDGC: 0x%x",
+				    (int) idata);
+			}
 		}
 
 		odata &= ~7;
```

## Every edited function, after the fix

### `src/devices/dev_mb89352.c` -- post-edit lines 299-704 (`+` marks a line the diff added or the point of a deletion)

```c
  299|  DEVICE_ACCESS(mb89352)
  300|  {
  301|  	struct mb89352_data *d = (struct mb89352_data *) extra;
  302|  	uint64_t idata = 0, odata = 0;
  303|  
     | [... lines 304-453 not shown ...]
  454|  						    command's sector data.  #263 measured that
  455|  						    exact consequence on the ASC: 384 bytes of
  456|  						    the previous command's buffer written onto
  457|  						    the disk image.
  458|  
  459|  						    This is NOT #263's short-transfer shape --
  460|  						    mb89352_dreg_write() only issues the
  461|  						    command at exact fill, so the natural PIO
  462|  						    path always supplies every byte.  The
  463|  						    defect is the premature offset, and the
  464|  						    honest repair (offset 0, advanced as bytes
  465|  						    arrive) is DEFERRED on purpose: the disk
  466|  						    layer would then return 2 and this model
  467|  						    discards that return, so the guest would
  468|  						    be told a WRITE completed that never
  469|  						    reached the disk -- exactly the defect
  470|  						    #283 fixed in the ASC, re-created on the
  471|  						    luna88k write path.  That needs its own
  472|  						    round and its own probe.  Zeroing removes
  473|  						    the disclosure now and cannot regress a
  474|  						    correct guest, which overwrites every one
  475|  						    of these bytes before use.  */
  476|  						scsi_transfer_allocbuf(&d->xferp->data_out_len,
  477|  						    &d->xferp->data_out, d->transfer_count, 1);
  478|  						/*  #338: was `= d->transfer_count`,
  479|  						    i.e. "all the data has arrived"
  480|  						    declared at ALLOCATION time, before
  481|  						    a single byte had. diskimage_scsicmd
  482|  						    gates a WRITE on
  483|  						    `data_out_offset != size` and on
  484|  						    nothing else, so that satisfied the
  485|  						    guard immediately: a guest could
  486|  						    SELECT, XFR a DATAOUT phase sized to
  487|  						    the write, switch to PH_CMD, send a
  488|  						    WRITE(6) CDB, and have the buffer
  489|  						    committed to the disk image without
  490|  						    ever entering a data phase. #295
  491|  						    zeroed the buffer, so what remained
  492|  						    was silent corruption rather than
  493|  						    heap disclosure -- the offset is now
  494|  						    truthful instead, and starts empty.  */
  495|  						d->xferp->data_out_offset = 0;
  496|  						break;
  497|  					case PH_DATAIN:
  498|  						break;
  499|  					case PH_CMD:
  500|  						scsi_transfer_allocbuf(&d->xferp->cmd_len,
  501|  						    &d->xferp->cmd, d->transfer_count, 0);
  502|  						break;
  503|  					case PH_STAT:
  504|  						break;
  505|  					case PH_MSGIN:
  506|  						break;
  507|  					default:
  508|  						debugmsg_cpu(cpu, d->subsys, "",
  509|  						    VERBOSITY_ERROR,
  510|  					    	    "Transfer command: unimplemented phase %i",
  511|  					    	    d->phase);
  512|  						/*  #186: (Codex/Fable) guest-selectable PCTL phase via
  513|  						    a valid SCMD_XFR; log and break, don't exit(1).  */
  514|  						break;
  515|  					}
  516|  
  517|  					if (!(d->phase & 1))
  518|  						d->reg[INTS] |= INTS_CMD_DONE;
  519|  				}
  520|  				break;
  521|  
  522|  			case SCMD_RST_ACK:
  523|  				d->reg[SSTS] &= ~(SSTS_INITIATOR | SSTS_TARGET);
  524|  				d->reg[PSNS] &= ~PSNS_REQ;
  525|  				break;
  526|  
  527|  			default:
  528|  				debugmsg_cpu(cpu, d->subsys, "",
  529|  				    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  530|  			    	    "unimplemented SCMD: 0x%x", (int) idata);
  531|  
  532|  				if (mb89352_abort_on_unimplemented_stuff) {
  533|  					cpu->running = 0;
  534|  					return 0;
  535|  				}
  536|  			}
  537|  		}
  538|  		break;
  539|  
  540|  	case TMOD:
  541|  		if (writeflag == MEM_WRITE) {
  542|  			d->reg[regnr] = idata;
  543|  			if (idata != 0)
  544|  				debugmsg_cpu(cpu, d->subsys, "",
  545|  				    VERBOSITY_WARNING,
  546|  				    "unimplemented write to TMOD: 0x%02x",
  547|  			    	    (int) idata);
  548|  		}
  549|  		break;	
  550|  
  551|  	case INTS:
  552|  		if (writeflag == MEM_WRITE) {
  553|  			int old = d->reg[INTS];
  554|  			d->reg[INTS] &= ~idata;
  555|  			if (old != d->reg[INTS])
  556|  				debugmsg_cpu(cpu, d->subsys, "",
  557|  				    VERBOSITY_INFO, "INTS: 0x%02x -> 0x%02x",
  558|  			    	    old, d->reg[INTS]);
  559|  		}
  560|  		break;	
  561|  
  562|  	case PSNS:
  563|  		if (writeflag == MEM_WRITE) {
  564|+ 			if (idata == SCMD_BUS_REL) {
  565|+ 				d->reg[PSNS] = 0;
  566|+ 			} else {
  567|+ 				debugmsg_cpu(cpu, d->subsys, "",
  568|+ 				    VERBOSITY_WARNING,
  569|+ 			    	    "unimplemented write to PSNS/SDGC: 0x%x",
  570|+ 				    (int) idata);
  571|+ 			}
  572|  		}
  573|  
  574|  		odata &= ~7;
  575|  		odata |= d->phase;
  576|  		break;
  577|  
  578|  	case SSTS:
  579|  		if (writeflag == MEM_WRITE) {
  580|  			d->reg[regnr] = idata;
  581|  			debugmsg_cpu(cpu, d->subsys, "",
  582|  			    VERBOSITY_WARNING,
  583|  		    	    "unimplemented write to SSTS: 0x%x",
  584|  			    (int) idata);
  585|  		}
  586|  
  587|  		if (d->transfer_count == 0)
  588|  			odata |= SSTS_TCZERO;
  589|  		else
  590|  			odata &= ~SSTS_TCZERO;
  591|  
  592|  		odata &= ~(SSTS_DREG_FULL | SSTS_DREG_EMPTY | SSTS_BUSY);
  593|  
  594|  		// Inbound phase, but no more data? Then the dreg is empty.
  595|  		if (d->phase & 1) {
  596|  			if (d->transfer_count == 0)
  597|  				odata |= SSTS_DREG_EMPTY;
  598|  		}
  599|  
  600|  		// Outbound phase, then the dreg is always empty.
  601|  		if (!(d->phase & 1)) {
  602|  			odata |= SSTS_DREG_EMPTY;
  603|  		}
  604|  
  605|  		if (d->phase & 1 && d->transfer_count > 0)
  606|  			odata |= SSTS_BUSY;
  607|  		break;
  608|  
  609|  	case SERR:
  610|  		if (writeflag == MEM_WRITE) {
  611|  			d->reg[regnr] = idata;
  612|  			debugmsg_cpu(cpu, d->subsys, "",
  613|  			    VERBOSITY_WARNING,
  614|  		    	    "unimplemented write to SERR: 0x%x",
  615|  			    (int) idata);
  616|  		}
  617|  		break;
  618|  
  619|  	case PCTL:
  620|  		if (writeflag == MEM_WRITE) {
  621|  			d->reg[regnr] = idata;
  622|  			if (idata & 0x78)
  623|  				debugmsg_cpu(cpu, d->subsys, "",
  624|  				    VERBOSITY_WARNING,
  625|  			    	    "write to read-only bits of PCTL ignored: 0x%x",
  626|  				    (int) idata);
  627|  			d->reg[regnr] &= 0x87;
  628|  		}
  629|  		break;
  630|  
  631|  	case MBC:
     | [... lines 632-674 not shown ...]
  675|  		break;
  676|  
  677|  	default:
  678|  		if (writeflag == MEM_WRITE)
  679|  			debugmsg_cpu(cpu, d->subsys, "",
  680|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  681|  		    	    "unimplemented %zu-bit WRITE to address 0x%x: 0x%x",
  682|  		    	    len * 8,
  683|  			    (int) relative_addr,
  684|  			    (int) idata);
  685|  		else
  686|  			debugmsg_cpu(cpu, d->subsys, "",
  687|  			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  688|  		    	    "unimplemented %zu-bit READ from address 0x%x",
  689|  		    	    len * 8,
  690|  			    (int) relative_addr);
  691|  
  692|  		if (mb89352_abort_on_unimplemented_stuff) {
  693|  			cpu->running = 0;
  694|  			return 0;
  695|  		}
  696|  	}
  697|  
  698|  	reassert_interrupts(d);
  699|  
  700|  	if (writeflag == MEM_READ)
  701|  		memory_writemax64(cpu, data, len, odata);
  702|  
  703|  	return 1;
  704|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_MB89352PSNS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_MB89352PSNS: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
