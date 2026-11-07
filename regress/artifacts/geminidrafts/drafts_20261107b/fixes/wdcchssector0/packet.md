# GXemul hardened fork -- DRAFT A FIX for one filed issue, `wdcchssector0` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `wdcchssector0`, state `open`, severity `LOW`)

**title:** src/devices/dev_wdc.c:469-471,560-562 -- in CHS mode a sector register of 0 is used as sector - 1, so (c, h, 0) addresses the previous track's last sector instead of being rejected (CHS sectors number from 1) -- WRONG-RESULT (CHS mode)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- add 0-check for CHS sector

## The code at the cited lines

### `src/devices/dev_wdc.c` around the row's cited line 469 (HEAD 8d9df658, lines 349-589)

```c
  349| 	/*  10-19: Serial number  */
  350| 	memcpy(&d->identify_struct[2 * 10], "#0                  ", 20);
  351| 
  352| 	/*  23-26: Firmware version  */
  353| 	memcpy(&d->identify_struct[2 * 23], "1.0     ", 8);
  354| 
  355| 	/*  27-46: Model number  */
  356| 	if (diskimage_getname(cpu->machine, d->drive + d->base_drive,
  357| 	    DISKIMAGE_IDE, namebuf, sizeof(namebuf))) {
  358| 		size_t i;
  359| 		for (i=0; i<sizeof(namebuf); i++)
  360| 			if (namebuf[i] == 0) {
  361| 				for (; i<sizeof(namebuf); i++)
  362| 					namebuf[i] = ' ';
  363| 				break;
  364| 			}
  365| 		memcpy(&d->identify_struct[2 * 27], namebuf, 40);
  366| 	} else
  367| 		memcpy(&d->identify_struct[2 * 27],
  368| 		    "Fake GXemul IDE disk                    ", 40);
  369| 
  370| 	/*  47: max sectors per multitransfer  */
  371| 	d->identify_struct[2 * 47 + 0] = 0x80;
  372| 	d->identify_struct[2 * 47 + 1] = 128;
  373| 
  374| 	/*  49: capabilities: (0x200 = LBA, 0x100 = DMA support.)  #572
  375| 	    honours LBA28 commands (the LBA bit of the select byte) but does
  376| 	    NOT advertise LBA here: the advertisement is a separate, measured
  377| 	    decision (see the wdclbaadvertise row); words 60-61 already carry
  378| 	    the capacity.  */
  379| 	d->identify_struct[2 * 49 + 0] = 0;
  380| 	d->identify_struct[2 * 49 + 1] = 0;
  381| 
  382| 	/*  51: PIO timing mode.  */
  383| 	d->identify_struct[2 * 51 + 0] = 0x00;	/*  ?  */
  384| 	d->identify_struct[2 * 51 + 1] = 0x00;
  385| 
  386| 	/*  53: 0x02 = fields 64-70 valid, 0x01 = fields 54-58 valid  */
  387| 	d->identify_struct[2 * 53 + 0] = 0x00;
  388| 	d->identify_struct[2 * 53 + 1] = 0x02;
  389| 
  390| 	/*
  391| 	 *  #405: `% 255` where `& 255` is meant, on six of these eight lines.
  392| 	 *
  393| 	 *  The two that were already right are the ones whose operand is small:
  394| 	 *  `(sectors) & 255` cannot exceed a byte anyway. Every other line shifts
  395| 	 *  first and does NOT pre-mask, so its operand is a multi-byte quantity and
  396| 	 *  `% 255` is not byte extraction that occasionally coincides -- it is a
  397| 	 *  base-256 digit sum. Measured in closed form, 0 counterexamples over 2^26:
  398| 	 *      x % 255 == ((x >> 8) + (x & 255)) % 255
  399| 	 *
  400| 	 *  So this is not a rare corner. Above the threshold it is wrong 100.0000%
  401| 	 *  of the time; the 0.39% of sizes where the >>8 byte is accidentally right
  402| 	 *  are exactly the ones where >>16 is wrong. The announced capacity lands
  403| 	 *  either side of the truth, worst case reporting ZERO SECTORS.
  404| 	 *
  405| 	 *  Smallest size at which any byte diverges is 65,280 sectors -- but
  406| 	 *  diskimage_recalc_size()'s closing whole-cylinder round-up (the shared
  407| 	 *  bytespercyl block, hoisted there by #414) rounds every image up to
  408| 	 *  whole cylinders, so that exact count is unreachable. The smallest
  409| 	 *  REACHABLE divergence is 33,546,240 bytes (65 cylinders), where a 32 MB
  410| 	 *  disk announces itself as 120 KB.
  411| 	 *
  412| 	 *  The byte order is NOT a second defect and was deliberately left alone.
  413| 	 *  The convention is stated at the top of this function ("Offsets are in
  414| 	 *  16-bit WORDS!  High byte, then low"), the geometry words follow it, the
  415| 	 *  transmit loop in wdc_command()'s WDCC_IDENTIFY case pushes [i+1] before
  416| 	 *  [i+0], and dev_wdc_access()'s wd_data read reassembles (high << 8) | low.
  417| 	 *  Two panel seats called it a defect from the snippet alone; two that read
  418| 	 *  the file found it consistent, and a later pass CONFIRMED it by executing
  419| 	 *  the whole guest path: both the LE and BE branches, plus memory_writemax64,
  420| 	 *  land the SAME two bytes in guest memory, so the device layer is
  421| 	 *  byte-stream-preserving. The 57-vs-58 WORD order is not establishable from
  422| 	 *  this tree at all -- there is no ATA specification here -- so a mask-only
  423| 	 *  correction is exactly as much as the source can justify.
  424| 	 *
  425| 	 *  #408: THE CITATIONS ABOVE NAME CONSTRUCTS, NOT LINE NUMBERS, AND THAT IS
  426| 	 *  DELIBERATE.  #405 cited lines that its own inserted comment had shifted by
  427| 	 *  +31.  #407 wrote a correction saying "re-read every line reference AFTER
  428| 	 *  the edit is in place" -- and then made the identical error, because that
  429| 	 *  correction was itself +9 lines and every number it "fixed" was re-read from
  430| 	 *  the pre-edit file.  Two rounds, same mechanism, and the second one had the
  431| 	 *  lesson written down in front of it.  A line number inside a file the same
  432| 	 *  commit edits is measured against the file it was written in, not the one
  433| 	 *  that ships; naming the construct survives every future edit instead.
  434| 	 */
  435| 	/*  57-58: current capacity in sectors  */
  436| 	d->identify_struct[2 * 58 + 0] = ((total_size / 512) >> 24) & 255;
  437| 	d->identify_struct[2 * 58 + 1] = ((total_size / 512) >> 16) & 255;
  438| 	d->identify_struct[2 * 57 + 0] = ((total_size / 512) >> 8) & 255;
  439| 	d->identify_struct[2 * 57 + 1] = (total_size / 512) & 255;
  440| 
  441| 	/*  60-61: total nr of addressable sectors  */
  442| 	d->identify_struct[2 * 61 + 0] = ((total_size / 512) >> 24) & 255;
  443| 	d->identify_struct[2 * 61 + 1] = ((total_size / 512) >> 16) & 255;
  444| 	d->identify_struct[2 * 60 + 0] = ((total_size / 512) >> 8) & 255;
  445| 	d->identify_struct[2 * 60 + 1] = (total_size / 512) & 255;
  446| 
  447| 	/*  64: Advanced PIO mode support. 0x02 = mode4, 0x01 = mode3  */
  448| 	d->identify_struct[2 * 64 + 0] = 0x00;
  449| 	d->identify_struct[2 * 64 + 1] = 0x03;
  450| 
  451| 	/*  67, 68: PIO timing  */
  452| 	d->identify_struct[2 * 67 + 0] = 0;
  453| 	d->identify_struct[2 * 67 + 1] = 120;
  454| 	d->identify_struct[2 * 68 + 0] = 0;
  455| 	d->identify_struct[2 * 68 + 1] = 120;
  456| }
  457| 
  458| 
  459| /*
  460|  *  wdc__read():
  461|  */
  462| void wdc__read(struct cpu *cpu, struct wdc_data *d)
  463| {
  464| #define MAX_SECTORS_PER_CHUNK	64
  465| 	const int max_sectors_per_chunk = MAX_SECTORS_PER_CHUNK;
  466| 	unsigned char buf[512 * MAX_SECTORS_PER_CHUNK];
  467| 	int i, cyl = d->cyl_hi * 256+ d->cyl_lo;
  468| 	int count = d->seccnt? d->seccnt : 256;
  469| 	uint64_t offset = 512 * (d->sector - 1
  470| 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
  471| 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
  472| 
  473| 	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
  474| 	    (it overflows int for any head != 0).  */
  475| 	if (d->lba)
  476| 		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
  477| 		    (cyl << 8) + d->sector);
  478| 
  479| 	while (count > 0) {
  480| 		int to_read = count > max_sectors_per_chunk?
  481| 		    max_sectors_per_chunk : count;
  482| 
  483| 		/*  TODO: result code from the read?  */
  484| 
  485| 		/*  #484: AN OCCUPANCY BOUND.  The test below is a BUFFER bound -- does
  486| 		    the linear write fit inside the allocation -- and it is NOT an
  487| 		    occupancy bound: this arm bypasses wdc_addtoinbuf() entirely and
  488| 		    compares the two pointers nowhere, so it can step head past tail and
  489| 		    overwrite unread bytes in silence.
  490| 
  491| 		    MEASURED, AND THE QUALIFIER IS PART OF THE MEASUREMENT: driving the
  492| 		    FUNCTION with a prefilled ring gives occupancy 262156 -> 1548, a
  493| 		    plausible-looking number, with 1548 bytes of unread data replaced by
  494| 		    disk contents.
  495| 
  496| 		    *** BUT 'REACHABLE' IS THE WRONG WORD AND THE READING SEATS WERE RIGHT
  497| 		    ABOUT THE PRODUCT. ***  `wdc__read()` has exactly ONE caller and it sits
  498| 		    AFTER `wdc_new_command_reset()`, so the ring is EMPTY on every real
  499| 		    invocation.  The prefilled state the rows build is a FUNCTION state, not
  500| 		    a guest route.  The arm is occupancy-blind AS CODE; this guard is
  501| 		    DEFENSIVE, and it is licensed by the caller invariant being unwritten
  502| 		    anywhere else -- not by a live defect.  A second seat then MEASURED
  503| 		    that too: 512 READ/READMULTI commands driven only through the guest
  504| 		    register interface, ring pre-stuffed each time, reached this guard
  505| 		    1280 times and FIRED IT ZERO TIMES.
  506| 		
  507| 		    The `- 1` is the sacrificed slot and is load-bearing: without it this
  508| 		    guard admits a refill of exactly room+1 bytes, which is the ONLY input
  509| 		    that distinguishes the two forms (measured 15/16, one row).
  510| 		
  511| 		    It is the SAME admission predicate as the producer's, and that is the
  512| 		    reason both hunks are one round: split them and the two arms disagree
  513| 		    about what "full" means, which is an incoherence the split itself
  514| 		    creates.  */
  515| 		if (512 * to_read > (d->inbuf_tail - d->inbuf_head - 1 +
  516| 		    WDC_INBUF_SIZE) % WDC_INBUF_SIZE) {
  517| 			if (!d->warned_inbuf_overrun) {
  518| 				d->warned_inbuf_overrun = 1;
  519| 				/*  #484: names THIS function, not the producer.  The
  520| 				    shared latch already removes the only other way to
  521| 				    tell the two sites apart, so a message pointing at
  522| 				    a guard that did not fire is a wrong record in
  523| 				    product output.  */
  524| 				fatal("[ wdc__read(): WARNING! wdc inbuf would"
  525| 				    " overrun; refill refused. Increase"
  526| 				    " WDC_MAX_SECTORS. ]\n");
  527| 			}
  528| 			break;
  529| 		}
  530| 
  531| 		if (d->inbuf_head + 512 * to_read <= WDC_INBUF_SIZE) {
  532| 			diskimage_access(cpu->machine, d->drive + d->base_drive,
  533| 			    DISKIMAGE_IDE, 0, offset,
  534| 			    d->inbuf + d->inbuf_head, 512 * to_read);
  535| 			d->inbuf_head += 512 * to_read;
  536| 			if (d->inbuf_head == WDC_INBUF_SIZE)
  537| 				d->inbuf_head = 0;
  538| 		} else {
  539| 			diskimage_access(cpu->machine, d->drive + d->base_drive,
  540| 			    DISKIMAGE_IDE, 0, offset, buf, 512 * to_read);
  541| 			for (i=0; i<512 * to_read; i++)
  542| 				wdc_addtoinbuf(d, buf[i]);
  543| 		}
  544| 
  545| 		offset += 512 * to_read;
  546| 		count -= to_read;
  547| 	}
  548| 
  549| 	d->int_assert = 1;
  550| }
  551| 
  552| 
  553| /*
  554|  *  wdc__write():
  555|  */
  556| void wdc__write(struct cpu *cpu, struct wdc_data *d)
  557| {
  558| 	int cyl = d->cyl_hi * 256+ d->cyl_lo;
  559| 	int count = d->seccnt? d->seccnt : 256;
  560| 	uint64_t offset = 512 * (d->sector - 1
  561| 	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
  562| 	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
  563| 	/*  #572: LBA28 -- head[3:0] is LBA[27:24]; the product is 64-bit
  564| 	    (it overflows int for any head != 0).  */
  565| 	if (d->lba)
  566| 		offset = 512 * (int64_t)(((d->head & 0xf) << 24) +
  567| 		    (cyl << 8) + d->sector);
  568| 
  569| 	d->write_in_progress = d->cur_command;
  570| 	d->write_count = count;
  571| 	d->write_offset = offset;
  572| 
  573| 	/*  TODO: result code?  */
  574| }
  575| 
  576| 
  577| /*
  578|  *  status_byte():
  579|  *
  580|  *  Return a reasonable status byte corresponding to the controller's current
  581|  *  state.
  582|  */
  583| static int status_byte(struct wdc_data *d, struct cpu *cpu)
  584| {
  585| 	int odata = 0;
  586| 	if (diskimage_exist(cpu->machine, d->drive + d->base_drive,
  587| 	    DISKIMAGE_IDE))
  588| 		odata |= WDCS_DRDY | WDCS_DSC;
  589| 	if (d->inbuf_head != d->inbuf_tail)
```

## The data structures those files define (every field that exists)

### `src/devices/dev_wdc.c` -- `struct wdc_data {` (HEAD lines 54-134)

```c
   54| struct wdc_data {
   55| 	struct interrupt irq;
   56| 	int		addr_mult;
   57| 	int		base_drive;
   58| 	int		data_debug;
   59| 	int		io_enabled;
   60| 
   61| 	/*  Cached values:  */
   62| 	int		cyls[2];
   63| 	int		heads[2];
   64| 	int		sectors_per_track[2];
   65| 
   66| 	unsigned char	*inbuf;
   67| 	int		inbuf_head;
   68| 	int		inbuf_tail;
   69| 
   70| 	int		int_assert;
   71| 
   72| 	/*  #337: latch each replaced exit(1) so a guest that retries in a
   73| 	    loop cannot flood the host log -- the same flood #265 caused and
   74| 	    #269 had to undo.  */
   75| 	int		warned_badlen;
   76| 	int		warned_empty_drain;
   77| 	int		warned_atapi_err;
   78| 	int		warned_null_xfer;
   79| 	int		warned_atapi_dataout;
   80| 
   81| 	/*  #464 (wdcflood): the SIX fatal() this file still emitted without bound.
   82| 	    #337 latched "each replaced exit(1)"; these were always fatal()
   83| 	    and never exit(1), so they fell outside that round's enumeration.
   84| 	    Measured: 20 stores -> 20 host lines with AND without -q, and the
   85| 	    OVER-READ site at 500 iterations produced 2000 lines / 158,449
   86| 	    bytes.  Artifacts: regress/artifacts/wdcflood/witness_20260825/
   87| 	    {fr_no__q,fr_with__q,n3}.out.  (An earlier wording said "the read
   88| 	    path", which points a reader at the non-8-bit READ guard instead;
   89| 	    n3.out is 2000x "reading too much", i.e. the ring over-read.)
   90| 	    fatal() has no early-out (core/debugmsg.c:384-390, against
   91| 	    debug()'s at core/debugmsg.c:375), so -q cannot silence it.
   92| 
   93| 	    SIX FLAGS, NOT FOUR.  Pairing the ring halves or the two width
   94| 	    checks was proposed and is wrong: #337's own shared warned_badlen
   95| 	    spans the two arms of ONE ENDIANNESS BRANCH (the
   96| 	    `cpu->byte_order == EMUL_LITTLE_ENDIAN` test in the wd_data write
   97| 	    arm below, and its else),
   98| 	    which are mutually exclusive at runtime, so sharing there loses
   99| 	    nothing.  These six can all fire in one session.  Measured
  100| 	    corroboration: in the session that produced the over-read, no
  101| 	    PRODUCER operation ran at all, so no overrun could have preceded
  102| 	    it -- the ring halves are causally independent.
  103| 
  104| 	    (An earlier draft warranted that with "it fires with NO DISK
  105| 	    ATTACHED", which is a NON-SEQUITUR: wdc_addtoinbuf is reachable
  106| 	    from the guest DATA-WRITE path below, so a diskless guest can
  107| 	    fill the ring perfectly well.  The conclusion holds; the reason
  108| 	    given for it did not, and a wrong reason gets reused.)
  109| 
  110| 	    fatal() is KEPT rather than downgraded, on this fork's own
  111| 	    recorded warrant at dev_asc.c:248-257: under -q verbosity settles
  112| 	    at VERBOSITY_ERROR, so a WARNING-level debugmsg would be INVISIBLE
  113| 	    to the boot-log hygiene grep and an ERROR-level one would trip
  114| 	    #261's break-on-ERROR.  */
  115| 	int		warned_inbuf_overrun;
  116| 	int		warned_inbuf_overread;
  117| 	int		warned_unimpl_cmd;
  118| 	int		warned_nonbyte_write;
  119| 	int		warned_nonbyte_read;
  120| 	int		warned_data_unexpected;
  121| 
  122| 	int		write_in_progress;
  123| 	int		write_count;
  124| 	int64_t		write_offset;
  125| 
  126| 	int		error;
  127| 	int		precomp;
  128| 	int		seccnt;
  129| 	int		sector;
  130| 	int		cyl_lo;
  131| 	int		cyl_hi;
  132| 	int		sdh_resv;
  133| 	int		lba;
  134| 	int		drive;
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

End with one line: `FIXDRAFT_WDCCHSSECTOR0: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
