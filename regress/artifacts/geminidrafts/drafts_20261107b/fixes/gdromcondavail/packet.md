# GXemul hardened fork -- DRAFT A FIX for one filed issue, `gdromcondavail` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `gdromcondavail`, state `open`, severity `med`)

**title:** gdromcondavail  COND_DATA_AVAIL permanently lies after an overread -- the device advertises data while returning 0xffff (split out of gdromcondlies)

**state_note (head):**

*** THE ONE PRODUCT DEFECT OF THE NINE.  TRUE, with a qualification that narrows my title. ***
`dev_dreamcast_gdrom.c:1073`, anchors `cur_cnt >= d->cnt` and `GDROM_W_OVERREAD`: clearing
availability at exhaustion depends on the MUTABLE count, and the overread branch returns all-ones
without correcting availability.  Guest-reachable through Dreamcast MMIO -- the count can disagree
with the buffer extent.

**THE QUALIFICATION MY TITLE OVERSTATES:** *"ordinary exhaustion DOES clear availability; the
inconsistent state persists until another operation changes it."*  So 'permanently lies' is too
strong -- it lies until the next operation that touches the state.  The defect is real; its
permanence is not.

**The stimulus already exists and the ORACLE does not:** `regress/gdrom_data_probe.py:374`
(anchors `overread`, `overread x1`) drives exactly that disagreement but checks SURVIVAL and
DIAGNOSTICS, never the subsequent COND state.  *That is the channel-line failure -- a row whose
stimulus reaches the defect and whose oracle cannot see it.*

Falsifier offered and checked: *would be wrong if exhaustion independently cleared availability, or
the count could not diverge during a response.  Neither holds.*  `#496` fixed the separate
bad-value paths, not this.

*Evidence: codex evidence pass 2026-09-07, regress/artifacts/queueunrated/codex_bare2_20260907.txt.  Source-reading only -- no builds, gates or probes were run, so every
mutant outcome below is a static conclusion, not a fresh measurement.*

*** REACHABILITY ESTABLISHED FROM SOURCE, 2026-09-07 -- the row previously asserted it and now
has the mechanism. ***

**The guest writes `d->cnt` DIRECTLY, one byte at a time:**

    :1194   d->cnt = (d->cnt & 0xff00) | (idata & 0xff);
    :1202   d->cnt = (d->cnt & 0x00ff) | ((idata & 0xff) << 8);

**And availability is cleared only when the COUNT exhausts**, at `:1077 if (d->cur_cnt >= d->cnt)`
-> `:1078 if (d->cur_data_offset >= d->data_len)` -> `:1079 d->cond &= ~COND_DATA_AVAIL`.

> **So the path is: raise `cnt` after data is armed; `cur_cnt >= d->cnt` never becomes true; `:1079`
> never runs; the BUFFER still exhausts, and reads fall to the `:1087` else-arm, which returns
> `0xffff` and DOES NOT TOUCH `d->cond`.**  The guest then reads status, sees `COND_DATA_AVAIL`,
> reads data, gets `0xffff`, and repeats -- with the diagnostic LATCHED after the first occurrence,
> so the log says nothing after read one.

**Two things this changes about the row.**  Its title says availability *"permanently lies"*: it does
not -- ordinary exhaustion clears it and another command recovers the state, so the lie is confined
to repeated reads after entering the inconsistent state.  And the `:1087` arm is **deliberate**, not
an oversight: its comment records `#460` joining it to the `:1052` guard on the merits -- *"this and
the COND_DATA_AVAIL site above are ONE predicate family, 'read when there is nothing to give'"* --
so a repair there edits a decision a previous round argued explicitly.

**THE DESIGN QUESTION IS WHICH SITE OWNS THE BUG**, and it is out to the codex seat rather than
settled here: clear availability in the `:1087` over-read arm, or fix `:1077`, whose condition
couples a GUEST-WRITABLE count to a DEVICE-OWNED buffer extent -- the guard-field-versus-body-field
disagreement in its purest form.  *Brief: `regress/artifacts/gdromcondavail/DESIGN_brief.md`.*

*** CODEX DESIGN PASS 2026-09-07 (`regress/artifacts/gdromcondavail/codex_design_20260907.txt`).
 [... 13048 more characters not shown]

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Guest can manually manipulate count to cause overreads that return 0xffff without clearing availability.

## The code at the cited lines

### `src/devices/dev_dreamcast_gdrom.c` around the row's cited line 1032 (HEAD 8d9df658, lines 912-1152)

```c
  912| 		 *  completion event.  An early return skips that event and
  913| 		 *  leaves a guest waiting for a completion that never comes.
  914| 		 */
  915| 		if (!(d->warned & GDROM_W_CMD)) {
  916| 			d->warned |= GDROM_W_CMD;
  917| 			fatal("[ dreamcast_gdrom: handle_command:"
  918| 			    " unimplemented command 0x%02x -- declined."
  919| 			    "  (once) ]\n", d->cmd[0]);
  920| 		}
  921| 		break;
  922| 	}
  923| 
  924| 	// Any resulting data? Then set COND_DATA_AVAIL. Otherwise, clear
  925| 	// that bit, and set count to zero.
  926| 	if (d->data != NULL) {
  927| 		d->cond |= COND_DATA_AVAIL;
  928| 	} else {
  929| 		d->cnt = 0;
  930| 		d->cond &= ~COND_DATA_AVAIL;
  931| 	}
  932| 
  933| 	// NetBSD seems to sometimes request 32 sectors (2048 bytes each), i.e.
  934| 	// 65536 bytes. That is represented as count = 0x0000 (when NetBSD reads
  935| 	// from the CNTHI and CNTLO registers). That does not work very well.
  936| 	// This is a hack/workaround for that.
  937| 	if (d->cnt == 65536)
  938| 		d->cnt = 32768;
  939| 
  940| 	SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM);
  941| }
  942| 
  943| void dreamcast_gdrom_update_stat(struct cpu *cpu, struct dreamcast_gdrom_data *d)
  944| {
  945| 	// See NetBSD's gdrom.c.
  946| 	d->stat = 6;
  947| 
  948| 	if (diskimage_exist(cpu->machine, 0, DISKIMAGE_IDE)) {
  949| 		d->stat = 0;
  950| 	}
  951| }
  952| 
  953| 
  954| DEVICE_ACCESS(dreamcast_gdrom)
  955| {
  956| 	struct dreamcast_gdrom_data *d = (struct dreamcast_gdrom_data *) extra;
  957| 	uint64_t idata = 0, odata = 0;
  958| 
  959| 	if (writeflag == MEM_WRITE)
  960| 		idata = memory_readmax64(cpu, data, len);
  961| 
  962| 	switch (relative_addr) {
  963| 
  964| 	case GDROM_BUSY:
  965| 		if (writeflag == MEM_READ) {
  966| 			odata = d->busy;
  967| 		} else {
  968| 			// fatal("[ Write to GDROM_BUSY: 0x%08x ]\n", (int)idata);
  969| 			// I'm assuming that writing bits to BUSY clears them.
  970| 			d->busy &= ~idata;
  971| 		}
  972| 		break;
  973| 
  974| 	case GDROM_DATA:
  975| 		/*
  976| 		 *  #460: THIS SITE LOGS AND CONTINUES; the other three decline.
  977| 		 *  The difference is measured, not stylistic.
  978| 		 *
  979| 		 *  BEFORE THIS FIX, `len` appeared exactly once in the whole arm --
  980| 		 *  in the guard that was here -- and no index expression consulted
  981| 		 *  it.  (It appears three times now: this fix's own format string
  982| 		 *  and argument.  Stated in the past tense because the claim is
  983| 		 *  about the code the measurement was taken against, and a seat
  984| 		 *  caught the present tense going false the moment it shipped.)
  985| 		 *  Measured:
  986| 		 *  byte, word and longword reads all consume exactly two bytes
  987| 		 *  and return the same odata, and six BYTE stores assemble the
  988| 		 *  12-byte packet and DISPATCH the command, reaching handle_command
  989| 		 *  exactly as six word stores do.
  990| 		 *
  991| 		 *  *** BUT THE CONTINUATION IS NOT WIDTH-TRANSPARENT, and an earlier
  992| 		 *  draft said it was. ***  `idata >> 8` is zero for a byte store, so
  993| 		 *  EVERY ODD COMMAND BYTE IS FORGED TO ZERO.  That is harmless for
  994| 		 *  the TOC packet 0x14, whose odd bytes are already zero -- which is
  995| 		 *  exactly why the measurement that produced the earlier claim did
  996| 		 *  not see it.  Command 0x30 needs cmd[1] in {0x20,0x24} and a
  997| 		 *  byte-store packet can never satisfy it, so it reaches
  998| 		 *  handle_command's data-format arm.
  999| 		 *
 1000| 		 *  *** THIS SENTENCE READ "so it reaches handle_command's own
 1001| 		 *  exit(1).  MEASURED: this build dies there and a DECLINING
 1002| 		 *  build survives."  #490 MADE ITS OWN ANTECEDENT FALSE and the
 1003| 		 *  claim with it: there is no longer ANY exit(1) in
 1004| 		 *  handle_command, so a byte-store packet now reaches the
 1005| 		 *  LATCHED DECLINE and the build survives.  The comment even
 1006| 		 *  named the outcome -- "a DECLINING build survives" -- which is
 1007| 		 *  exactly what this build now is.  Caught by a pass-2 seat;
 1008| 		 *  corrected in-round because a WRONG RECORD is one of the two
 1009| 		 *  things the stopping rule fixes rather than files, and a claim
 1010| 		 *  labelled MEASURED is the worst kind to leave stale. ***
 1011| 		 *
 1012| 		 *  That is a RELOCATION, not a regression -- before this fix the
 1013| 		 *  same byte store died at the width guard, one step earlier -- but
 1014| 		 *  it means "dropping the guard changes NO BOUND" is the MEMORY
 1015| 		 *  safety argument and not the whole safety story.  Memory safety
 1016| 		 *  does hold: no index consults len, cur_data_offset advances by two
 1017| 		 *  regardless, and no mutant produced an out-of-bounds access.
 1018| 		 *
 1019| 		 *  Dropping the guard changes no bound -- which is
 1020| 		 *  precisely the warrant dev_pvr.c:1577-1581 (#187) states for
 1021| 		 *  the same class on this same machine.
 1022| 		 *
 1023| 		 *  *** DO NOT "EMULATE" NARROW ACCESS INSTEAD. ***  A pass-1
 1024| 		 *  panel split on that, and it was MEASURED ACTIVELY HARMFUL:
 1025| 		 *  letting cmd_count step by 1 makes eleven byte writes plus one
 1026| 		 *  word write go 11 -> 13, SKIPPING the `== 12` equality below,
 1027| 		 *  so busy&0x08 never clears and the next write reaches the
 1028| 		 *  "Too much GDROM_DATA" exit -- otherwise unreachable.  It also
 1029| 		 *  writes cmd[12], one past the array.  A fix that re-opens a
 1030| 		 *  dead site is worse than the defect, and only a build saw it.
 1031| 		 *
 1032| 		 *  DE-ESCALATION: this round removes FOUR host-fatal predicates and
 1033| 		 *  the detector carries accept rows for THREE.  *** THIS ONE IS
 1034| 		 *  EXEMPT, AND THE EXEMPTION IS STATED RATHER THAN LEFT AS A GAP. ***
 1035| 		 *  The clause's accept-row obligation applies to predicates a guest
 1036| 		 *  store can feed; this predicate tests the ACCESS WIDTH against a
 1037| 		 *  compile-time constant, and no guest store reaches its operand --
 1038| 		 *  the same failability carve-out the project already applies to
 1039| 		 *  read-only and never-set-by-device bits.  The other three (the two
 1040| 		 *  read predicates and the busy mask) DO carry rows.
 1041| 		 */
 1042| 		if (len != sizeof(uint16_t)) {
 1043| 			if (!(d->warned & GDROM_W_LEN)) {
 1044| 				d->warned |= GDROM_W_LEN;
 1045| 				fatal("[ dreamcast_gdrom: non-16bit"
 1046| 				    " GDROM_DATA access, len=%i -- handled"
 1047| 				    " as 16-bit.  (once) ]\n", (int) len);
 1048| 			}
 1049| 		}
 1050| 
 1051| 		if (writeflag == MEM_READ) {
 1052| 			if (!(d->cond & COND_DATA_AVAIL)) {
 1053| 				/*  #460: was exit(1).  `cond` is zero on a fresh
 1054| 				    device, so the FIRST guest load ended the host.  */
 1055| 				if (!(d->warned & GDROM_W_NODATA)) {
 1056| 					d->warned |= GDROM_W_NODATA;
 1057| 					fatal("[ dreamcast_gdrom: read from"
 1058| 					    " GDROM_DATA with no data"
 1059| 					    " available -- returning 0xffff."
 1060| 					    "  (once) ]\n");
 1061| 				}
 1062| 				/*  0xffff because a released ATA/ATAPI data bus
 1063| 				    reads as all-ones, which dev_wdc.c:155-167 also
 1064| 				    returns.  NOTE THE COLLISION: this device's TOC is
 1065| 				    memset(0xff), so 0xffff is LEGITIMATE PAYLOAD here
 1066| 				    and no returned value is self-identifying.  The
 1067| 				    DIAGNOSTIC is the truthfulness channel, not the
 1068| 				    value -- which is also why the latch is per-site.  */
 1069| 				odata = 0xffff;
 1070| 				break;
 1071| 			}
 1072| 
 1073| 			if (d->cur_data_offset < d->data_len) {
 1074| 				odata = d->data[d->cur_data_offset ++];
 1075| 				odata |= (d->data[d->cur_data_offset ++] << 8);
 1076| 				d->cur_cnt += sizeof(uint16_t);
 1077| 				if (d->cur_cnt >= d->cnt) {
 1078| 					if (d->cur_data_offset >= d->data_len) {
 1079| 						d->cond &= ~COND_DATA_AVAIL;
 1080| 					} else {
 1081| 						d->cnt = d->data_len - d->cur_data_offset;
 1082| 						d->cur_cnt = 0;
 1083| 					}
 1084| 
 1085| 					SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM);
 1086| 				}
 1087| 			} else {
 1088| 				/*  #460: joined on the merits -- this and the
 1089| 				    COND_DATA_AVAIL site above are ONE predicate
 1090| 				    family, "read when there is nothing to give".
 1091| 				    Fixing one and leaving the other fatal gives a
 1092| 				    device where a declined read is safe in one
 1093| 				    state and lethal in another.  */
 1094| 				if (!(d->warned & GDROM_W_OVERREAD)) {
 1095| 					d->warned |= GDROM_W_OVERREAD;
 1096| 					fatal("[ dreamcast_gdrom: read past"
 1097| 					    " the end of the GDROM_DATA"
 1098| 					    " buffer -- returning 0xffff."
 1099| 					    "  (once) ]\n");
 1100| 				}
 1101| 				odata = 0xffff;
 1102| 				break;
 1103| 			}
 1104| 		} else {
 1105| 			if (d->busy & 0x08) {
 1106| 				if (d->cmd_count >= 12) {
 1107| 					fatal("Too much GDROM_DATA?\n");
 1108| 					exit(1);
 1109| 				}
 1110| 				/*  Add data to cmd:  */
 1111| 				d->cmd[d->cmd_count++] = idata;
 1112| 				d->cmd[d->cmd_count++] = idata >> 8;
 1113| 				if (d->cmd_count == 12) {
 1114| 					d->busy &= ~0x08;
 1115| 					handle_command(cpu, d);
 1116| 				}
 1117| 			} else {
 1118| 				/*  #460: was exit(1).  `busy` is zero on a fresh
 1119| 				    device, so the FIRST guest store ended the host.  */
 1120| 				if (!(d->warned & GDROM_W_NOTWAIT)) {
 1121| 					d->warned |= GDROM_W_NOTWAIT;
 1122| 					fatal("[ dreamcast_gdrom: write to"
 1123| 					    " GDROM_DATA while not waiting"
 1124| 					    " for data -- ignored.  (once) ]\n");
 1125| 				}
 1126| 			}
 1127| 		}
 1128| 		break;
 1129| 
 1130| 	case GDROM_REGX:
 1131| 		if (writeflag == MEM_READ) {
 1132| 			debug("[ Read to GDROM_REGX? ]\n");
 1133| 		} else {
 1134| 			/*  NetBSD/dreamcast writes 0 here.  */
 1135| 			if (idata != 0)
 1136| 				debug("[ Write 0x%x to GDROM_REGX? ]\n", (int)idata);
 1137| 		}
 1138| 		break;
 1139| 
 1140| 	case GDROM_UNKNOWN_0x88:
 1141| 		if (writeflag == MEM_READ) {
 1142| 			fatal("Read from GDROM_UNKNOWN_0x88?\n");
 1143| 			// exit(1);
 1144| 		} else {
 1145| 			if (idata != 0xb) {
 1146| 				/*
 1147| 				 *  #496: a guest write of any value but
 1148| 				 *  0x0b ENDED THE HOST PROCESS here.  One
 1149| 				 *  store, from an ordinary driver, on an
 1150| 				 *  unmodified -E dreamcast.
 1151| 				 *
 1152| 				 *  The model implements NO behaviour for
```

## The data structures those files define (every field that exists)

### `src/devices/dev_dreamcast_gdrom.c` -- `struct dreamcast_gdrom_data {` (HEAD lines 129-177)

```c
  129| struct dreamcast_gdrom_data {
  130| 	// 0x005f7000: GDROM control registers
  131| 	uint8_t		busy;		/*  Busy status  */
  132| 	uint8_t		stat;		/*  Status  */
  133| 	int		cnt;		/*  Data length in bytes  */
  134| 	uint8_t		cond;
  135| 
  136| 	int		cmd_count;
  137| 	uint8_t		cmd[12];
  138| 
  139| 	uint8_t		*data;
  140| 	int		data_len;
  141| 	int		cur_data_offset;
  142| 	int		cur_cnt;
  143| 
  144| 	/*
  145| 	 *  #460: once-only diagnostic latch, ONE BIT PER SITE.
  146| 	 *
  147| 	 *  Modelled on dev_wdc.c's `warned_badlen` (#337) FOR THE MECHANISM ONLY
  148| 	 *  -- note that dev_wdc.c SHARES one flag between its two sites (:731
  149| 	 *  and :761), so the per-site decision below is this round's own measured
  150| 	 *  warrant and must not be attributed to that precedent.  Not on
  151| 	 *  sh4_val_first().  A review seat named the reason: dev_wdc.c is this
  152| 	 *  tree's OTHER ATA/ATAPI data port and fixed this exact class the same
  153| 	 *  way, while sh4_val_first() is an SH4 helper whose storage lives in
  154| 	 *  sh4_data -- and the GD-ROM is on the Holly/G1 bus, not the SH4.
  155| 	 *
  156| 	 *  Per-site and not one shared bit, MEASURED: a shared bit scores
  157| 	 *  identically on every row that drives ONE site per session -- which
  158| 	 *  was every row this detector had -- and diverges only when two sites
  159| 	 *  run in one session, where it loses the second diagnostic for good.
  160| 	 */
  161| 	uint32_t	warned;
  162| 
  163| 	/*
  164| 	 *  #461: one bit per (direction, word) for each window's default arm.
  165| 	 *  16 + 8 = 24 bytes.
  166| 	 *
  167| 	 *  KEPT SEPARATE FROM #460's `warned` ABOVE, deliberately: those four bits
  168| 	 *  key on a CONDITION at a single offset (0x80), so an offset key cannot
  169| 	 *  separate them.  #443 could unify its three classes only because all of
  170| 	 *  them key on the register offset.  A reviewer will ask; this is why.
  171| 	 */
  172| 	uint32_t	unimpl_reported[GDROM_NDIR][GDROM_BITWORDS(GDROM_NKEYS)];
  173| 	uint32_t	dma_unimpl_reported[GDROM_NDIR][GDROM_BITWORDS(GDROM_DMA_NKEYS)];
  174| 
  175| 	// 0x005f7400: GDROM DMA
  176| 	uint32_t	dma_reg[NREGS_GDROM_DMA];
  177| };
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

End with one line: `FIXDRAFT_GDROMCONDAVAIL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
