# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `wdcatadocstale` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `wdcatadocstale`, state `open`)

**title:** src/devices/dev_wdc.c:421-423,1080-1081 + regress/diff_wdc_identify.c:25-26 + regress/gate_offline.sh:1525 -- four comments say no ATA document exists here while dev_wdc.c:637-639 cites _scratchpad/ata2_x3t10_948d.txt -- RECORD

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 421| 	 *  this tree at all -- there is no ATA specification here -- so a mask-only

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index e369ebc0..ed7c208a 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -419,7 +419,7 @@ static void wdc_initialize_identify_struct(struct cpu *cpu, struct wdc_data *d)
 	 *  the whole guest path: both the LE and BE branches, plus memory_writemax64,
 	 *  land the SAME two bytes in guest memory, so the device layer is
 	 *  byte-stream-preserving. The 57-vs-58 WORD order is not establishable from
-	 *  this tree at all -- there is no ATA specification here -- so a mask-only
+	 *  this tree at all, so a mask-only
 	 *  correction is exactly as much as the source can justify.
 	 *
 	 *  #408: THE CITATIONS ABOVE NAME CONSTRUCTS, NOT LINE NUMBERS, AND THAT IS
```

## Every edited function, after the fix

### `src/devices/dev_wdc.c` -- post-edit lines 314-456 (`+` marks a line the diff added or the point of a deletion)

```c
  314|  static void wdc_initialize_identify_struct(struct cpu *cpu, struct wdc_data *d)
  315|  {
  316|  	uint64_t total_size;
  317|  	int flags, cdrom = 0;
  318|  	char namebuf[40];
  319|  
  320|  	total_size = diskimage_getsize(cpu->machine, d->drive + d->base_drive,
  321|  	    DISKIMAGE_IDE);
  322|  	if (diskimage_is_a_cdrom(cpu->machine, d->drive + d->base_drive,
  323|  	    DISKIMAGE_IDE))
  324|  		cdrom = 1;
  325|  
  326|  	memset(d->identify_struct, 0, sizeof(d->identify_struct));
  327|  
  328|  	/*  Offsets are in 16-bit WORDS!  High byte, then low.  */
  329|  
  330|  	/*  0: general flags  */
  331|  	flags = 1 << 6;	/*  Fixed  */
  332|  	if (cdrom)
  333|  		flags = 0x8580;		/*  ATAPI, CDROM, removable  */
  334|  	d->identify_struct[2 * 0 + 0] = flags >> 8;
  335|  	d->identify_struct[2 * 0 + 1] = flags;
  336|  
  337|  	/*  1: nr of cylinders  */
  338|  	d->identify_struct[2 * 1 + 0] = d->cyls[d->drive] >> 8;
  339|  	d->identify_struct[2 * 1 + 1] = d->cyls[d->drive];
  340|  
  341|  	/*  3: nr of heads  */
  342|  	d->identify_struct[2 * 3 + 0] = d->heads[d->drive] >> 8;
  343|  	d->identify_struct[2 * 3 + 1] = d->heads[d->drive];
  344|  
  345|  	/*  6: sectors per track  */
  346|  	d->identify_struct[2 * 6 + 0] = d->sectors_per_track[d->drive] >> 8;
  347|  	d->identify_struct[2 * 6 + 1] = d->sectors_per_track[d->drive];
  348|  
  349|  	/*  10-19: Serial number  */
  350|  	memcpy(&d->identify_struct[2 * 10], "#0                  ", 20);
  351|  
  352|  	/*  23-26: Firmware version  */
  353|  	memcpy(&d->identify_struct[2 * 23], "1.0     ", 8);
  354|  
  355|  	/*  27-46: Model number  */
  356|  	if (diskimage_getname(cpu->machine, d->drive + d->base_drive,
  357|  	    DISKIMAGE_IDE, namebuf, sizeof(namebuf))) {
  358|  		size_t i;
  359|  		for (i=0; i<sizeof(namebuf); i++)
  360|  			if (namebuf[i] == 0) {
  361|  				for (; i<sizeof(namebuf); i++)
  362|  					namebuf[i] = ' ';
  363|  				break;
  364|  			}
  365|  		memcpy(&d->identify_struct[2 * 27], namebuf, 40);
  366|  	} else
  367|  		memcpy(&d->identify_struct[2 * 27],
  368|  		    "Fake GXemul IDE disk                    ", 40);
  369|  
  370|  	/*  47: max sectors per multitransfer  */
  371|  	d->identify_struct[2 * 47 + 0] = 0x80;
  372|  	d->identify_struct[2 * 47 + 1] = 128;
  373|  
  374|  	/*  49: capabilities: (0x200 = LBA, 0x100 = DMA support.)  #572
  375|  	    honours LBA28 commands (the LBA bit of the select byte) but does
  376|  	    NOT advertise LBA here: the advertisement is a separate, measured
  377|  	    decision (see the wdclbaadvertise row); words 60-61 already carry
  378|  	    the capacity.  */
  379|  	d->identify_struct[2 * 49 + 0] = 0;
  380|  	d->identify_struct[2 * 49 + 1] = 0;
  381|  
  382|  	/*  51: PIO timing mode.  */
  383|  	d->identify_struct[2 * 51 + 0] = 0x00;	/*  ?  */
  384|  	d->identify_struct[2 * 51 + 1] = 0x00;
  385|  
  386|  	/*  53: 0x02 = fields 64-70 valid, 0x01 = fields 54-58 valid  */
  387|  	d->identify_struct[2 * 53 + 0] = 0x00;
  388|  	d->identify_struct[2 * 53 + 1] = 0x02;
  389|  
  390|  	/*
  391|  	 *  #405: `% 255` where `& 255` is meant, on six of these eight lines.
  392|  	 *
  393|  	 *  The two that were already right are the ones whose operand is small:
  394|  	 *  `(sectors) & 255` cannot exceed a byte anyway. Every other line shifts
  395|  	 *  first and does NOT pre-mask, so its operand is a multi-byte quantity and
  396|  	 *  `% 255` is not byte extraction that occasionally coincides -- it is a
  397|  	 *  base-256 digit sum. Measured in closed form, 0 counterexamples over 2^26:
  398|  	 *      x % 255 == ((x >> 8) + (x & 255)) % 255
  399|  	 *
  400|  	 *  So this is not a rare corner. Above the threshold it is wrong 100.0000%
  401|  	 *  of the time; the 0.39% of sizes where the >>8 byte is accidentally right
  402|  	 *  are exactly the ones where >>16 is wrong. The announced capacity lands
  403|  	 *  either side of the truth, worst case reporting ZERO SECTORS.
  404|  	 *
  405|  	 *  Smallest size at which any byte diverges is 65,280 sectors -- but
  406|  	 *  diskimage_recalc_size()'s closing whole-cylinder round-up (the shared
  407|  	 *  bytespercyl block, hoisted there by #414) rounds every image up to
  408|  	 *  whole cylinders, so that exact count is unreachable. The smallest
  409|  	 *  REACHABLE divergence is 33,546,240 bytes (65 cylinders), where a 32 MB
  410|  	 *  disk announces itself as 120 KB.
  411|  	 *
  412|  	 *  The byte order is NOT a second defect and was deliberately left alone.
  413|  	 *  The convention is stated at the top of this function ("Offsets are in
  414|  	 *  16-bit WORDS!  High byte, then low"), the geometry words follow it, the
  415|  	 *  transmit loop in wdc_command()'s WDCC_IDENTIFY case pushes [i+1] before
  416|  	 *  [i+0], and dev_wdc_access()'s wd_data read reassembles (high << 8) | low.
  417|  	 *  Two panel seats called it a defect from the snippet alone; two that read
  418|  	 *  the file found it consistent, and a later pass CONFIRMED it by executing
  419|  	 *  the whole guest path: both the LE and BE branches, plus memory_writemax64,
  420|  	 *  land the SAME two bytes in guest memory, so the device layer is
  421|  	 *  byte-stream-preserving. The 57-vs-58 WORD order is not establishable from
  422|+ 	 *  this tree at all, so a mask-only
  423|  	 *  correction is exactly as much as the source can justify.
  424|  	 *
  425|  	 *  #408: THE CITATIONS ABOVE NAME CONSTRUCTS, NOT LINE NUMBERS, AND THAT IS
  426|  	 *  DELIBERATE.  #405 cited lines that its own inserted comment had shifted by
  427|  	 *  +31.  #407 wrote a correction saying "re-read every line reference AFTER
  428|  	 *  the edit is in place" -- and then made the identical error, because that
  429|  	 *  correction was itself +9 lines and every number it "fixed" was re-read from
  430|  	 *  the pre-edit file.  Two rounds, same mechanism, and the second one had the
  431|  	 *  lesson written down in front of it.  A line number inside a file the same
  432|  	 *  commit edits is measured against the file it was written in, not the one
  433|  	 *  that ships; naming the construct survives every future edit instead.
  434|  	 */
  435|  	/*  57-58: current capacity in sectors  */
  436|  	d->identify_struct[2 * 58 + 0] = ((total_size / 512) >> 24) & 255;
  437|  	d->identify_struct[2 * 58 + 1] = ((total_size / 512) >> 16) & 255;
  438|  	d->identify_struct[2 * 57 + 0] = ((total_size / 512) >> 8) & 255;
  439|  	d->identify_struct[2 * 57 + 1] = (total_size / 512) & 255;
  440|  
  441|  	/*  60-61: total nr of addressable sectors  */
  442|  	d->identify_struct[2 * 61 + 0] = ((total_size / 512) >> 24) & 255;
  443|  	d->identify_struct[2 * 61 + 1] = ((total_size / 512) >> 16) & 255;
  444|  	d->identify_struct[2 * 60 + 0] = ((total_size / 512) >> 8) & 255;
  445|  	d->identify_struct[2 * 60 + 1] = (total_size / 512) & 255;
  446|  
  447|  	/*  64: Advanced PIO mode support. 0x02 = mode4, 0x01 = mode3  */
  448|  	d->identify_struct[2 * 64 + 0] = 0x00;
  449|  	d->identify_struct[2 * 64 + 1] = 0x03;
  450|  
  451|  	/*  67, 68: PIO timing  */
  452|  	d->identify_struct[2 * 67 + 0] = 0;
  453|  	d->identify_struct[2 * 67 + 1] = 120;
  454|  	d->identify_struct[2 * 68 + 0] = 0;
  455|  	d->identify_struct[2 * 68 + 1] = 120;
  456|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_WDCATADOCSTALE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_WDCATADOCSTALE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
