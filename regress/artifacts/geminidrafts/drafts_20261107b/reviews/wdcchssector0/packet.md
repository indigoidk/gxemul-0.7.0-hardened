# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `wdcchssector0` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `wdcchssector0`, state `open`)

**title:** src/devices/dev_wdc.c:469-471,560-562 -- in CHS mode a sector register of 0 is used as sector - 1, so (c, h, 0) addresses the previous track's last sector instead of being rejected (CHS sectors number from 1) -- WRONG-RESULT (CHS mode)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_wdc.c:469`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_wdc.c b/src/devices/dev_wdc.c
index e369ebc0..1d86f90d 100644
--- a/src/devices/dev_wdc.c
+++ b/src/devices/dev_wdc.c
@@ -466,7 +466,8 @@ void wdc__read(struct cpu *cpu, struct wdc_data *d)
 	unsigned char buf[512 * MAX_SECTORS_PER_CHUNK];
 	int i, cyl = d->cyl_hi * 256+ d->cyl_lo;
 	int count = d->seccnt? d->seccnt : 256;
-	uint64_t offset = 512 * (d->sector - 1
+	/* #NNN: clamp CHS sector 0 to 1 since CHS sectors start at 1 */
+	uint64_t offset = 512 * ((d->sector ? d->sector : 1) - 1
 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
 
@@ -557,7 +558,8 @@ void wdc__write(struct cpu *cpu, struct wdc_data *d)
 {
 	int cyl = d->cyl_hi * 256+ d->cyl_lo;
 	int count = d->seccnt? d->seccnt : 256;
-	uint64_t offset = 512 * (d->sector - 1
+	/* #NNN: clamp CHS sector 0 to 1 since CHS sectors start at 1 */
+	uint64_t offset = 512 * ((d->sector ? d->sector : 1) - 1
 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
 	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
```

## Every edited function, after the fix

### `src/devices/dev_wdc.c` -- post-edit lines 462-551 (`+` marks a line the diff added or the point of a deletion)

```c
  462|  void wdc__read(struct cpu *cpu, struct wdc_data *d)
  463|  {
  464|  #define MAX_SECTORS_PER_CHUNK	64
  465|  	const int max_sectors_per_chunk = MAX_SECTORS_PER_CHUNK;
  466|  	unsigned char buf[512 * MAX_SECTORS_PER_CHUNK];
  467|  	int i, cyl = d->cyl_hi * 256+ d->cyl_lo;
  468|  	int count = d->seccnt? d->seccnt : 256;
  469|+ 	/* #NNN: clamp CHS sector 0 to 1 since CHS sectors start at 1 */
  470|+ 	uint64_t offset = 512 * ((d->sector ? d->sector : 1) - 1
  471|  	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
  472|  	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
  473|  
  474|  	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
  475|  	    (it overflows int for any head != 0).  */
  476|  	if (d->lba)
  477|  		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
  478|  		    (cyl << 8) + d->sector);
  479|  
  480|  	while (count > 0) {
  481|  		int to_read = count > max_sectors_per_chunk?
  482|  		    max_sectors_per_chunk : count;
  483|  
  484|  		/*  TODO: result code from the read?  */
  485|  
  486|  		/*  #484: AN OCCUPANCY BOUND.  The test below is a BUFFER bound -- does
  487|  		    the linear write fit inside the allocation -- and it is NOT an
  488|  		    occupancy bound: this arm bypasses wdc_addtoinbuf() entirely and
  489|  		    compares the two pointers nowhere, so it can step head past tail and
  490|  		    overwrite unread bytes in silence.
  491|  
  492|  		    MEASURED, AND THE QUALIFIER IS PART OF THE MEASUREMENT: driving the
  493|  		    FUNCTION with a prefilled ring gives occupancy 262156 -> 1548, a
  494|  		    plausible-looking number, with 1548 bytes of unread data replaced by
  495|  		    disk contents.
  496|  
  497|  		    *** BUT 'REACHABLE' IS THE WRONG WORD AND THE READING SEATS WERE RIGHT
  498|  		    ABOUT THE PRODUCT. ***  `wdc__read()` has exactly ONE caller and it sits
  499|  		    AFTER `wdc_new_command_reset()`, so the ring is EMPTY on every real
  500|  		    invocation.  The prefilled state the rows build is a FUNCTION state, not
  501|  		    a guest route.  The arm is occupancy-blind AS CODE; this guard is
  502|  		    DEFENSIVE, and it is licensed by the caller invariant being unwritten
  503|  		    anywhere else -- not by a live defect.  A second seat then MEASURED
  504|  		    that too: 512 READ/READMULTI commands driven only through the guest
  505|  		    register interface, ring pre-stuffed each time, reached this guard
  506|  		    1280 times and FIRED IT ZERO TIMES.
  507|  		
  508|  		    The `- 1` is the sacrificed slot and is load-bearing: without it this
  509|  		    guard admits a refill of exactly room+1 bytes, which is the ONLY input
  510|  		    that distinguishes the two forms (measured 15/16, one row).
  511|  		
  512|  		    It is the SAME admission predicate as the producer's, and that is the
  513|  		    reason both hunks are one round: split them and the two arms disagree
  514|  		    about what "full" means, which is an incoherence the split itself
  515|  		    creates.  */
  516|  		if (512 * to_read > (d->inbuf_tail - d->inbuf_head - 1 +
  517|  		    WDC_INBUF_SIZE) % WDC_INBUF_SIZE) {
  518|  			if (!d->warned_inbuf_overrun) {
  519|  				d->warned_inbuf_overrun = 1;
  520|  				/*  #484: names THIS function, not the producer.  The
  521|  				    shared latch already removes the only other way to
  522|  				    tell the two sites apart, so a message pointing at
  523|  				    a guard that did not fire is a wrong record in
  524|  				    product output.  */
  525|  				fatal("[ wdc__read(): WARNING! wdc inbuf would"
  526|  				    " overrun; refill refused. Increase"
  527|  				    " WDC_MAX_SECTORS. ]\n");
  528|  			}
  529|  			break;
  530|  		}
  531|  
  532|  		if (d->inbuf_head + 512 * to_read <= WDC_INBUF_SIZE) {
  533|  			diskimage_access(cpu->machine, d->drive + d->base_drive,
  534|  			    DISKIMAGE_IDE, 0, offset,
  535|  			    d->inbuf + d->inbuf_head, 512 * to_read);
  536|  			d->inbuf_head += 512 * to_read;
  537|  			if (d->inbuf_head == WDC_INBUF_SIZE)
  538|  				d->inbuf_head = 0;
  539|  		} else {
  540|  			diskimage_access(cpu->machine, d->drive + d->base_drive,
  541|  			    DISKIMAGE_IDE, 0, offset, buf, 512 * to_read);
  542|  			for (i=0; i<512 * to_read; i++)
  543|  				wdc_addtoinbuf(d, buf[i]);
  544|  		}
  545|  
  546|  		offset += 512 * to_read;
  547|  		count -= to_read;
  548|  	}
  549|  
  550|  	d->int_assert = 1;
  551|  }
```

### `src/devices/dev_wdc.c` -- post-edit lines 557-576 (`+` marks a line the diff added or the point of a deletion)

```c
  557|  void wdc__write(struct cpu *cpu, struct wdc_data *d)
  558|  {
  559|  	int cyl = d->cyl_hi * 256+ d->cyl_lo;
  560|  	int count = d->seccnt? d->seccnt : 256;
  561|+ 	/* #NNN: clamp CHS sector 0 to 1 since CHS sectors start at 1 */
  562|+ 	uint64_t offset = 512 * ((d->sector ? d->sector : 1) - 1
  563|  	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
  564|  	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
  565|  	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
  566|  	    (it overflows int for any head != 0).  */
  567|  	if (d->lba)
  568|  		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
  569|  		    (cyl << 8) + d->sector);
  570|  
  571|  	d->write_in_progress = d->cur_command;
  572|  	d->write_count = count;
  573|  	d->write_offset = offset;
  574|  
  575|  	/*  TODO: result code?  */
  576|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_WDCCHSSECTOR0: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_WDCCHSSECTOR0: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
