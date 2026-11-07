# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mb89352psns` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mb89352psns`, state `open`, severity `MED`)

**title:** devices/dev_mb89352.c -- PSNS writes are stored instead of going to SDGC, and BUS_REL does not clear PSNS -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T91 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-27, C U9(c)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c.  Our site at de8c7547: src/devices/dev_mb89352.c:562-569.  Portable fix: yes -- port upstream a1cafe7c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream a1cafe7c.

## The code at the cited lines

### `src/devices/dev_mb89352.c` around the row's cited line 562 (HEAD d2a6f233, lines 517-607)

```c
  517| 					if (!(d->phase & 1))
  518| 						d->reg[INTS] |= INTS_CMD_DONE;
  519| 				}
  520| 				break;
  521| 
  522| 			case SCMD_RST_ACK:
  523| 				d->reg[SSTS] &= ~(SSTS_INITIATOR | SSTS_TARGET);
  524| 				d->reg[PSNS] &= ~PSNS_REQ;
  525| 				break;
  526| 
  527| 			default:
  528| 				debugmsg_cpu(cpu, d->subsys, "",
  529| 				    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  530| 			    	    "unimplemented SCMD: 0x%x", (int) idata);
  531| 
  532| 				if (mb89352_abort_on_unimplemented_stuff) {
  533| 					cpu->running = 0;
  534| 					return 0;
  535| 				}
  536| 			}
  537| 		}
  538| 		break;
  539| 
  540| 	case TMOD:
  541| 		if (writeflag == MEM_WRITE) {
  542| 			d->reg[regnr] = idata;
  543| 			if (idata != 0)
  544| 				debugmsg_cpu(cpu, d->subsys, "",
  545| 				    VERBOSITY_WARNING,
  546| 				    "unimplemented write to TMOD: 0x%02x",
  547| 			    	    (int) idata);
  548| 		}
  549| 		break;	
  550| 
  551| 	case INTS:
  552| 		if (writeflag == MEM_WRITE) {
  553| 			int old = d->reg[INTS];
  554| 			d->reg[INTS] &= ~idata;
  555| 			if (old != d->reg[INTS])
  556| 				debugmsg_cpu(cpu, d->subsys, "",
  557| 				    VERBOSITY_INFO, "INTS: 0x%02x -> 0x%02x",
  558| 			    	    old, d->reg[INTS]);
  559| 		}
  560| 		break;	
  561| 
  562| 	case PSNS:
  563| 		if (writeflag == MEM_WRITE) {
  564| 			d->reg[regnr] = idata;
  565| 			debugmsg_cpu(cpu, d->subsys, "",
  566| 			    VERBOSITY_WARNING,
  567| 		    	    "unimplemented write to PSNS/SDGC: 0x%x",
  568| 			    (int) idata);
  569| 		}
  570| 
  571| 		odata &= ~7;
  572| 		odata |= d->phase;
  573| 		break;
  574| 
  575| 	case SSTS:
  576| 		if (writeflag == MEM_WRITE) {
  577| 			d->reg[regnr] = idata;
  578| 			debugmsg_cpu(cpu, d->subsys, "",
  579| 			    VERBOSITY_WARNING,
  580| 		    	    "unimplemented write to SSTS: 0x%x",
  581| 			    (int) idata);
  582| 		}
  583| 
  584| 		if (d->transfer_count == 0)
  585| 			odata |= SSTS_TCZERO;
  586| 		else
  587| 			odata &= ~SSTS_TCZERO;
  588| 
  589| 		odata &= ~(SSTS_DREG_FULL | SSTS_DREG_EMPTY | SSTS_BUSY);
  590| 
  591| 		// Inbound phase, but no more data? Then the dreg is empty.
  592| 		if (d->phase & 1) {
  593| 			if (d->transfer_count == 0)
  594| 				odata |= SSTS_DREG_EMPTY;
  595| 		}
  596| 
  597| 		// Outbound phase, then the dreg is always empty.
  598| 		if (!(d->phase & 1)) {
  599| 			odata |= SSTS_DREG_EMPTY;
  600| 		}
  601| 
  602| 		if (d->phase & 1 && d->transfer_count > 0)
  603| 			odata |= SSTS_BUSY;
  604| 		break;
  605| 
  606| 	case SERR:
  607| 		if (writeflag == MEM_WRITE) {
```

## The data structures those files define (every field that exists)

### `src/devices/dev_mb89352.c` -- `struct mb89352_data {` (HEAD lines 72-86)

```c
   72| struct mb89352_data {
   73| 	int			subsys;
   74| 
   75| 	struct interrupt	irq;
   76| 	bool			irq_asserted;
   77| 
   78| 	uint8_t			reg[MB89352_NREGS];
   79| 	
   80| 	int			target;		// target SCSI ID, e.g. 6
   81| 	int			phase;
   82| 
   83| 	struct scsi_transfer	*xferp;
   84| 	size_t			transfer_count;
   85| 	size_t			transfer_bufpos;
   86| };
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

End with one line: `FIXDRAFT_MB89352PSNS: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
