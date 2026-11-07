# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mb89352psns` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mb89352psns`, state `open`, severity `MED`)

**title:** devices/dev_mb89352.c -- PSNS writes are stored instead of going to SDGC, and BUS_REL does not clear PSNS -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T91 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A1-27, C U9(c)).  Source URLs: https://github.com/retroprom/gxemul/commit/a1cafe7c.  Our site at de8c7547: src/devices/dev_mb89352.c:562-569.  Portable fix: yes -- port upstream a1cafe7c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port upstream a1cafe7c.

## The code at the cited lines

### `src/devices/dev_mb89352.c` around the row's cited line 562 (HEAD 8d9df658, lines 442-682)

```c
  442| 						    disk layer's only guard is exactly that
  443| 						    field (diskimage_scsicmd.c:778 compares
  444| 						    data_out_offset against the CDB size and
  445| 						    otherwise writes data_out straight to the
  446| 						    image at :788).  A guest that sets up a
  447| 						    DATA_OUT phase, writes NO data bytes, and
  448| 						    then issues a WRITE therefore committed
  449| 						    whatever the freed heap block last held --
  450| 						    and scsi_transfer_alloc() keeps a freelist
  451| 						    for the transfer structs while the buffers
  452| 						    themselves are free()d, so a same-size
  453| 						    malloc very often returns the PREVIOUS
  454| 						    command's sector data.  #263 measured that
  455| 						    exact consequence on the ASC: 384 bytes of
  456| 						    the previous command's buffer written onto
  457| 						    the disk image.
  458| 
  459| 						    This is NOT #263's short-transfer shape --
  460| 						    mb89352_dreg_write() only issues the
  461| 						    command at exact fill, so the natural PIO
  462| 						    path always supplies every byte.  The
  463| 						    defect is the premature offset, and the
  464| 						    honest repair (offset 0, advanced as bytes
  465| 						    arrive) is DEFERRED on purpose: the disk
  466| 						    layer would then return 2 and this model
  467| 						    discards that return, so the guest would
  468| 						    be told a WRITE completed that never
  469| 						    reached the disk -- exactly the defect
  470| 						    #283 fixed in the ASC, re-created on the
  471| 						    luna88k write path.  That needs its own
  472| 						    round and its own probe.  Zeroing removes
  473| 						    the disclosure now and cannot regress a
  474| 						    correct guest, which overwrites every one
  475| 						    of these bytes before use.  */
  476| 						scsi_transfer_allocbuf(&d->xferp->data_out_len,
  477| 						    &d->xferp->data_out, d->transfer_count, 1);
  478| 						/*  #338: was `= d->transfer_count`,
  479| 						    i.e. "all the data has arrived"
  480| 						    declared at ALLOCATION time, before
  481| 						    a single byte had. diskimage_scsicmd
  482| 						    gates a WRITE on
  483| 						    `data_out_offset != size` and on
  484| 						    nothing else, so that satisfied the
  485| 						    guard immediately: a guest could
  486| 						    SELECT, XFR a DATAOUT phase sized to
  487| 						    the write, switch to PH_CMD, send a
  488| 						    WRITE(6) CDB, and have the buffer
  489| 						    committed to the disk image without
  490| 						    ever entering a data phase. #295
  491| 						    zeroed the buffer, so what remained
  492| 						    was silent corruption rather than
  493| 						    heap disclosure -- the offset is now
  494| 						    truthful instead, and starts empty.  */
  495| 						d->xferp->data_out_offset = 0;
  496| 						break;
  497| 					case PH_DATAIN:
  498| 						break;
  499| 					case PH_CMD:
  500| 						scsi_transfer_allocbuf(&d->xferp->cmd_len,
  501| 						    &d->xferp->cmd, d->transfer_count, 0);
  502| 						break;
  503| 					case PH_STAT:
  504| 						break;
  505| 					case PH_MSGIN:
  506| 						break;
  507| 					default:
  508| 						debugmsg_cpu(cpu, d->subsys, "",
  509| 						    VERBOSITY_ERROR,
  510| 					    	    "Transfer command: unimplemented phase %i",
  511| 					    	    d->phase);
  512| 						/*  #186: (Codex/Fable) guest-selectable PCTL phase via
  513| 						    a valid SCMD_XFR; log and break, don't exit(1).  */
  514| 						break;
  515| 					}
  516| 
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
  608| 			d->reg[regnr] = idata;
  609| 			debugmsg_cpu(cpu, d->subsys, "",
  610| 			    VERBOSITY_WARNING,
  611| 		    	    "unimplemented write to SERR: 0x%x",
  612| 			    (int) idata);
  613| 		}
  614| 		break;
  615| 
  616| 	case PCTL:
  617| 		if (writeflag == MEM_WRITE) {
  618| 			d->reg[regnr] = idata;
  619| 			if (idata & 0x78)
  620| 				debugmsg_cpu(cpu, d->subsys, "",
  621| 				    VERBOSITY_WARNING,
  622| 			    	    "write to read-only bits of PCTL ignored: 0x%x",
  623| 				    (int) idata);
  624| 			d->reg[regnr] &= 0x87;
  625| 		}
  626| 		break;
  627| 
  628| 	case MBC:
  629| 		if (writeflag == MEM_WRITE) {
  630| 			debugmsg_cpu(cpu, d->subsys, "",
  631| 			    VERBOSITY_WARNING,
  632| 		    	    "write to read-only MBC ignored: 0x%x",
  633| 			    (int) idata);
  634| 		}
  635| 		break;
  636| 
  637| 	case DREG:
  638| 		if (d->transfer_count == 0) {
  639| 			debugmsg_cpu(cpu, d->subsys, "",
  640| 			    VERBOSITY_WARNING,
  641| 		    	    "DREG %s, but transfer count = 0!",
  642| 		    	    writeflag == MEM_WRITE ? "WRITE" : "READ");
  643| 		} else {
  644| 			d->transfer_count --;
  645| 
  646| 			if (writeflag == MEM_WRITE)
  647| 				mb89352_dreg_write(cpu, d, writeflag, idata);
  648| 			else
  649| 				odata = mb89352_dreg_read(cpu, d, writeflag);
  650| 		}
  651| 		break;
  652| 
  653| 	case TEMP:
  654| 		if (writeflag == MEM_WRITE)
  655| 			d->reg[regnr] = idata;
  656| 		break;
  657| 
  658| 	case TCH:
  659| 	case TCM:
  660| 	case TCL:
  661| 		if (writeflag == MEM_WRITE) {
  662| 			d->reg[regnr] = idata;
  663| 
  664| 			// Update d->transfer_count to be in sync with the registers.
  665| 			d->transfer_count = (d->reg[TCH] << 16) + (d->reg[TCM] << 8) + d->reg[TCL];
  666| 		} else {
  667| 			d->reg[TCH] = d->transfer_count >> 16;
  668| 			d->reg[TCM] = d->transfer_count >> 8;
  669| 			d->reg[TCL] = d->transfer_count;
  670| 			odata = d->reg[regnr];
  671| 		}
  672| 		break;
  673| 
  674| 	default:
  675| 		if (writeflag == MEM_WRITE)
  676| 			debugmsg_cpu(cpu, d->subsys, "",
  677| 			    mb89352_abort_on_unimplemented_stuff ? VERBOSITY_ERROR : VERBOSITY_WARNING,
  678| 		    	    "unimplemented %zu-bit WRITE to address 0x%x: 0x%x",
  679| 		    	    len * 8,
  680| 			    (int) relative_addr,
  681| 			    (int) idata);
  682| 		else
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

## YOUR PREVIOUS DRAFT SAID `STILL PRESENT: UNSETTLED` -- here is what it said was missing

```text
STILL PRESENT: UNSETTLED -- `d->reg[regnr] = idata;` at 564 stores to PSNS, but the macros for `SDGC` and `SCMD_BUS_REL` (or `BUS_REL`) are not shown in this packet.
```json
[]
```
The fix cannot be drafted because `SDGC` and `SCMD_BUS_REL` are not present in the text, and using them would violate the rule to use ONLY fields, functions, and macros that appear in the packet.
FIXDRAFT_MB89352PSNS: UNSETTLED PRESENT, 0 EDITS
```

## What you said was missing, from HEAD

### `src/cpus/tmp_alpha_tail.c` lines 45-61 (where HEAD defines `reg`)

```c
   45| #define DYNTRANS_PC_TO_POINTERS_GENERIC alpha_pc_to_pointers_generic
   46| #include "cpu_dyntrans.c"
   47| #undef DYNTRANS_PC_TO_POINTERS_FUNC
   48| 
   49| #undef DYNTRANS_PC_TO_POINTERS_GENERIC
   50| 
   51| #define COMBINE_INSTRUCTIONS alpha_combine_instructions
   52| #ifndef DYNTRANS_32
   53| #define reg(x) (*((uint64_t *)(x)))
   54| #define MODE_uint_t uint64_t
   55| #define MODE_int_t int64_t
   56| #else
   57| #define reg(x) (*((uint32_t *)(x)))
   58| #define MODE_uint_t uint32_t
   59| #define MODE_int_t int32_t
   60| #endif
   61| #define COMBINE(n) alpha_combine_ ## n
```

### `src/cpus/tmp_alpha_tail.c` lines 49-65 (where HEAD defines `reg`)

```c
   49| #undef DYNTRANS_PC_TO_POINTERS_GENERIC
   50| 
   51| #define COMBINE_INSTRUCTIONS alpha_combine_instructions
   52| #ifndef DYNTRANS_32
   53| #define reg(x) (*((uint64_t *)(x)))
   54| #define MODE_uint_t uint64_t
   55| #define MODE_int_t int64_t
   56| #else
   57| #define reg(x) (*((uint32_t *)(x)))
   58| #define MODE_uint_t uint32_t
   59| #define MODE_int_t int32_t
   60| #endif
   61| #define COMBINE(n) alpha_combine_ ## n
   62| #include "quick_pc_to_pointers.h"
   63| #include "cpu_alpha_instr.c"
   64| 
   65| #define DYNTRANS_RUN_INSTR_DEF alpha_run_instr
```

### `src/include/thirdparty/mb89352reg.h` lines 130-146 (where HEAD defines `SCMD_BUS_REL`)

```c
  130| 
  131| /* SCSI_SCMD */
  132| #define SCMD_RST	0x10
  133| #define SCMD_ICPT_XFR	0x08
  134| #define SCMD_PROG_XFR	0x04
  135| #define SCMD_PAD	0x01	/* if initiator */
  136| #define SCMD_PERR_STOP	0x01	/* if target */
  137| 	/* command codes */
  138| #define SCMD_BUS_REL	0x00
  139| #define SCMD_SELECT	0x20
  140| #define SCMD_RST_ATN	0x40
  141| #define SCMD_SET_ATN	0x60
  142| #define SCMD_XFR	0x80
  143| #define SCMD_XFR_PAUSE	0xa0
  144| #define SCMD_RST_ACK	0xc0
  145| #define SCMD_SET_ACK	0xe0
  146| 
```


Now draft the fix, or -- if it still cannot be written from what is shown -- say `STILL PRESENT: UNSETTLED` and name the
exact definition or function still missing.  A name that appears in no section of this packet does not exist in HEAD; do
not use it.  Do not return an empty edit list, and do not return edits that change only comments.

## YOUR PREVIOUS DRAFT FAILED TO BUILD -- correct it

It applied cleanly and the compiler rejected it:

```text
dev_mb89352.c:522:25: error: duplicate case value
```

That means a `case` label your edit adds is already handled by another `case` in the same switch -- look for the existing
label in the code shown and extend THAT arm instead of adding a second one.

The previous edits:

```json
[
  {
    "file": "src/devices/dev_mb89352.c",
    "old": "\t\t\tcase SCMD_RST_ACK:\n\t\t\t\td->reg[SSTS] &= ~(SSTS_INITIATOR | SSTS_TARGET);\n\t\t\t\td->reg[PSNS] &= ~PSNS_REQ;\n\t\t\t\tbreak;\n\n\t\t\tdefault:",
    "new": "\t\t\tcase SCMD_BUS_REL:\n\t\t\t\td->reg[PSNS] = 0;\n\t\t\t\tbreak;\n\n\t\t\tcase SCMD_RST_ACK:\n\t\t\t\td->reg[SSTS] &= ~(SSTS_INITIATOR | SSTS_TARGET);\n\t\t\t\td->reg[PSNS] &= ~PSNS_REQ;\n\t\t\t\tbreak;\n\n\t\t\tdefault:",
    "why": "Clear PSNS on BUS_REL."
  },
  {
    "file": "src/devices/dev_mb89352.c",
    "old": "\tcase PSNS:\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->reg[regnr] = idata;\n\t\t\tdebugmsg_cpu(cpu, d->subsys, \"\",\n\t\t\t    VERBOSITY_WARNING,\n\t\t    \t    \"unimplemented write to PSNS/SDGC: 0x%x\",\n\t\t\t    (int) idata);\n\t\t}",
    "new": "\tcase PSNS:\n\t\tif (writeflag == MEM_WRITE) {\n\t\t\tdebugmsg_cpu(cpu, d->subsys, \"\",\n\t\t\t    VERBOSITY_WARNING,\n\t\t    \t    \"unimplemented write to PSNS/SDGC: 0x%x\",\n\t\t\t    (int) idata);\n\t\t}",
    "why": "Prevent writes to SDGC from corrupting the read-only PSNS register."
  }
]
```

Return a CORRECTED complete edit list in the same form, or `STILL PRESENT: UNSETTLED` naming what is missing.
