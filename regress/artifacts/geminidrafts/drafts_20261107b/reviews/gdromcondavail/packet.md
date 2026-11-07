# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `gdromcondavail` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `gdromcondavail`, state `open`)

**title:** gdromcondavail  COND_DATA_AVAIL permanently lies after an overread -- the device advertises data while returning 0xffff (split out of gdromcondlies)

**state_note (head):** *** THE ONE PRODUCT DEFECT OF THE NINE.  TRUE, with a qualification that narrows my title. ***
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

**Two things this changes about the row.**  Its title says  [... 14048 more characters not shown]

**The drafter's own reading:** STILL PRESENT: YES -- 1087

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_dreamcast_gdrom.c b/src/devices/dev_dreamcast_gdrom.c
index 82aea52e..a89bb946 100644
--- a/src/devices/dev_dreamcast_gdrom.c
+++ b/src/devices/dev_dreamcast_gdrom.c
@@ -1098,6 +1098,7 @@ DEVICE_ACCESS(dreamcast_gdrom)
 					    " buffer -- returning 0xffff."
 					    "  (once) ]\n");
 				}
+				d->cond &= ~COND_DATA_AVAIL;
 				odata = 0xffff;
 				break;
 			}
```

## Every edited function, after the fix

### `src/devices/dev_dreamcast_gdrom.c` -- post-edit lines 954-1365 (`+` marks a line the diff added or the point of a deletion)

```c
  954|  DEVICE_ACCESS(dreamcast_gdrom)
  955|  {
  956|  	struct dreamcast_gdrom_data *d = (struct dreamcast_gdrom_data *) extra;
  957|  	uint64_t idata = 0, odata = 0;
  958|  
     | [... lines 959-990 not shown ...]
  991|  		 *  *** BUT THE CONTINUATION IS NOT WIDTH-TRANSPARENT, and an earlier
  992|  		 *  draft said it was. ***  `idata >> 8` is zero for a byte store, so
  993|  		 *  EVERY ODD COMMAND BYTE IS FORGED TO ZERO.  That is harmless for
  994|  		 *  the TOC packet 0x14, whose odd bytes are already zero -- which is
  995|  		 *  exactly why the measurement that produced the earlier claim did
  996|  		 *  not see it.  Command 0x30 needs cmd[1] in {0x20,0x24} and a
  997|  		 *  byte-store packet can never satisfy it, so it reaches
  998|  		 *  handle_command's data-format arm.
  999|  		 *
 1000|  		 *  *** THIS SENTENCE READ "so it reaches handle_command's own
 1001|  		 *  exit(1).  MEASURED: this build dies there and a DECLINING
 1002|  		 *  build survives."  #490 MADE ITS OWN ANTECEDENT FALSE and the
 1003|  		 *  claim with it: there is no longer ANY exit(1) in
 1004|  		 *  handle_command, so a byte-store packet now reaches the
 1005|  		 *  LATCHED DECLINE and the build survives.  The comment even
 1006|  		 *  named the outcome -- "a DECLINING build survives" -- which is
 1007|  		 *  exactly what this build now is.  Caught by a pass-2 seat;
 1008|  		 *  corrected in-round because a WRONG RECORD is one of the two
 1009|  		 *  things the stopping rule fixes rather than files, and a claim
 1010|  		 *  labelled MEASURED is the worst kind to leave stale. ***
 1011|  		 *
 1012|  		 *  That is a RELOCATION, not a regression -- before this fix the
 1013|  		 *  same byte store died at the width guard, one step earlier -- but
 1014|  		 *  it means "dropping the guard changes NO BOUND" is the MEMORY
 1015|  		 *  safety argument and not the whole safety story.  Memory safety
 1016|  		 *  does hold: no index consults len, cur_data_offset advances by two
 1017|  		 *  regardless, and no mutant produced an out-of-bounds access.
 1018|  		 *
 1019|  		 *  Dropping the guard changes no bound -- which is
 1020|  		 *  precisely the warrant dev_pvr.c:1577-1581 (#187) states for
 1021|  		 *  the same class on this same machine.
 1022|  		 *
 1023|  		 *  *** DO NOT "EMULATE" NARROW ACCESS INSTEAD. ***  A pass-1
 1024|  		 *  panel split on that, and it was MEASURED ACTIVELY HARMFUL:
 1025|  		 *  letting cmd_count step by 1 makes eleven byte writes plus one
 1026|  		 *  word write go 11 -> 13, SKIPPING the `== 12` equality below,
 1027|  		 *  so busy&0x08 never clears and the next write reaches the
 1028|  		 *  "Too much GDROM_DATA" exit -- otherwise unreachable.  It also
 1029|  		 *  writes cmd[12], one past the array.  A fix that re-opens a
 1030|  		 *  dead site is worse than the defect, and only a build saw it.
 1031|  		 *
 1032|  		 *  DE-ESCALATION: this round removes FOUR host-fatal predicates and
 1033|  		 *  the detector carries accept rows for THREE.  *** THIS ONE IS
 1034|  		 *  EXEMPT, AND THE EXEMPTION IS STATED RATHER THAN LEFT AS A GAP. ***
 1035|  		 *  The clause's accept-row obligation applies to predicates a guest
 1036|  		 *  store can feed; this predicate tests the ACCESS WIDTH against a
 1037|  		 *  compile-time constant, and no guest store reaches its operand --
 1038|  		 *  the same failability carve-out the project already applies to
 1039|  		 *  read-only and never-set-by-device bits.  The other three (the two
 1040|  		 *  read predicates and the busy mask) DO carry rows.
 1041|  		 */
 1042|  		if (len != sizeof(uint16_t)) {
 1043|  			if (!(d->warned & GDROM_W_LEN)) {
 1044|  				d->warned |= GDROM_W_LEN;
 1045|  				fatal("[ dreamcast_gdrom: non-16bit"
 1046|  				    " GDROM_DATA access, len=%i -- handled"
 1047|  				    " as 16-bit.  (once) ]\n", (int) len);
 1048|  			}
 1049|  		}
 1050|  
 1051|  		if (writeflag == MEM_READ) {
 1052|  			if (!(d->cond & COND_DATA_AVAIL)) {
 1053|  				/*  #460: was exit(1).  `cond` is zero on a fresh
 1054|  				    device, so the FIRST guest load ended the host.  */
 1055|  				if (!(d->warned & GDROM_W_NODATA)) {
 1056|  					d->warned |= GDROM_W_NODATA;
 1057|  					fatal("[ dreamcast_gdrom: read from"
 1058|  					    " GDROM_DATA with no data"
 1059|  					    " available -- returning 0xffff."
 1060|  					    "  (once) ]\n");
 1061|  				}
 1062|  				/*  0xffff because a released ATA/ATAPI data bus
 1063|  				    reads as all-ones, which dev_wdc.c:155-167 also
 1064|  				    returns.  NOTE THE COLLISION: this device's TOC is
 1065|  				    memset(0xff), so 0xffff is LEGITIMATE PAYLOAD here
 1066|  				    and no returned value is self-identifying.  The
 1067|  				    DIAGNOSTIC is the truthfulness channel, not the
 1068|  				    value -- which is also why the latch is per-site.  */
 1069|  				odata = 0xffff;
 1070|  				break;
 1071|  			}
 1072|  
 1073|  			if (d->cur_data_offset < d->data_len) {
 1074|  				odata = d->data[d->cur_data_offset ++];
 1075|  				odata |= (d->data[d->cur_data_offset ++] << 8);
 1076|  				d->cur_cnt += sizeof(uint16_t);
 1077|  				if (d->cur_cnt >= d->cnt) {
 1078|  					if (d->cur_data_offset >= d->data_len) {
 1079|  						d->cond &= ~COND_DATA_AVAIL;
 1080|  					} else {
 1081|  						d->cnt = d->data_len - d->cur_data_offset;
 1082|  						d->cur_cnt = 0;
 1083|  					}
 1084|  
 1085|  					SYSASIC_TRIGGER_EVENT(SYSASIC_EVENT_GDROM);
 1086|  				}
 1087|  			} else {
 1088|  				/*  #460: joined on the merits -- this and the
 1089|  				    COND_DATA_AVAIL site above are ONE predicate
 1090|  				    family, "read when there is nothing to give".
 1091|  				    Fixing one and leaving the other fatal gives a
 1092|  				    device where a declined read is safe in one
 1093|  				    state and lethal in another.  */
 1094|  				if (!(d->warned & GDROM_W_OVERREAD)) {
 1095|  					d->warned |= GDROM_W_OVERREAD;
 1096|  					fatal("[ dreamcast_gdrom: read past"
 1097|  					    " the end of the GDROM_DATA"
 1098|  					    " buffer -- returning 0xffff."
 1099|  					    "  (once) ]\n");
 1100|  				}
 1101|+ 				d->cond &= ~COND_DATA_AVAIL;
 1102|  				odata = 0xffff;
 1103|  				break;
 1104|  			}
 1105|  		} else {
 1106|  			if (d->busy & 0x08) {
 1107|  				if (d->cmd_count >= 12) {
 1108|  					fatal("Too much GDROM_DATA?\n");
 1109|  					exit(1);
 1110|  				}
 1111|  				/*  Add data to cmd:  */
 1112|  				d->cmd[d->cmd_count++] = idata;
 1113|  				d->cmd[d->cmd_count++] = idata >> 8;
 1114|  				if (d->cmd_count == 12) {
 1115|  					d->busy &= ~0x08;
 1116|  					handle_command(cpu, d);
 1117|  				}
 1118|  			} else {
 1119|  				/*  #460: was exit(1).  `busy` is zero on a fresh
 1120|  				    device, so the FIRST guest store ended the host.  */
 1121|  				if (!(d->warned & GDROM_W_NOTWAIT)) {
 1122|  					d->warned |= GDROM_W_NOTWAIT;
 1123|  					fatal("[ dreamcast_gdrom: write to"
 1124|  					    " GDROM_DATA while not waiting"
 1125|  					    " for data -- ignored.  (once) ]\n");
 1126|  				}
 1127|  			}
 1128|  		}
 1129|  		break;
 1130|  
 1131|  	case GDROM_REGX:
 1132|  		if (writeflag == MEM_READ) {
 1133|  			debug("[ Read to GDROM_REGX? ]\n");
 1134|  		} else {
 1135|  			/*  NetBSD/dreamcast writes 0 here.  */
 1136|  			if (idata != 0)
 1137|  				debug("[ Write 0x%x to GDROM_REGX? ]\n", (int)idata);
 1138|  		}
 1139|  		break;
 1140|  
 1141|  	case GDROM_UNKNOWN_0x88:
 1142|  		if (writeflag == MEM_READ) {
 1143|  			fatal("Read from GDROM_UNKNOWN_0x88?\n");
 1144|  			// exit(1);
 1145|  		} else {
 1146|  			if (idata != 0xb) {
 1147|  				/*
 1148|  				 *  #496: a guest write of any value but
 1149|  				 *  0x0b ENDED THE HOST PROCESS here.  One
 1150|  				 *  store, from an ordinary driver, on an
 1151|  				 *  unmodified -E dreamcast.
 1152|  				 *
 1153|  				 *  The model implements NO behaviour for
 1154|  				 *  this register: 0x0b is accepted and is
 1155|  				 *  a no-op, touching no device state.  So
 1156|  				 *  an unmodelled value is declined, not
 1157|  				 *  fatal.  The announce is kept because
 1158|  				 *  the accepted set is what ONE boot ROM
 1159|  				 *  happens to write, not a documented
 1160|  				 *  register contract -- so an unmodelled
 1161|  				 *  value is a fact about the guest worth
     | [... lines 1162-1335 not shown ...]
 1336|  	 *  *** THE INVARIANT IS THE THING TO WATCH: if a store tail is ever added
 1337|  	 *  to this arm, the injectivity argument at the DMA site must be re-derived
 1338|  	 *  HERE and a guard added with it. ***  Written down because the safety is
 1339|  	 *  structural rather than guarded, and structure is what a later edit
 1340|  	 *  silently changes.
 1341|  	 */
 1342|  	default:if (GDROM_UNIMPL_FIRST(d->unimpl_reported[
 1343|  		    writeflag == MEM_READ ? GDROM_RD : GDROM_WR],
 1344|  		    relative_addr)) {
 1345|  			if (writeflag == MEM_READ)
 1346|  				fatal("[ dreamcast_gdrom: read from addr"
 1347|  				    " 0x%x -- unimplemented, returning 0."
 1348|  				    "  (once per offset per direction) ]\n",
 1349|  				    (int)relative_addr);
 1350|  			else
 1351|  				fatal("[ dreamcast_gdrom: write to addr"
 1352|  				    " 0x%x: 0x%x -- unimplemented, ignored."
 1353|  				    "  (once per offset per direction) ]\n",
 1354|  				    (int)relative_addr, (int)idata);
 1355|  		}
 1356|  
 1357|  		odata = 0;
 1358|  		break;
 1359|  	}
 1360|  
 1361|  	if (writeflag == MEM_READ)
 1362|  		memory_writemax64(cpu, data, len, odata);
 1363|  
 1364|  	return 1;
 1365|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_GDROMCONDAVAIL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_GDROMCONDAVAIL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
