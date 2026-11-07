# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `wdcatadocstale` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `wdcatadocstale`, state `open`)

**title:** src/devices/dev_wdc.c:421-423,1080-1081 + regress/diff_wdc_identify.c:25-26 + regress/gate_offline.sh:1525 -- four comments say no ATA document exists here while dev_wdc.c:637-639 cites _scratchpad/ata2_x3t10_948d.txt -- RECORD

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_wdc.c` -- AT HEAD, lines 314-456 (`*` marks a line your previous draft changed)

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
  422|* 	 *  this tree at all -- there is no ATA specification here -- so a mask-only
  423|* 	 *  correction is exactly as much as the source can justify.
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


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_wdc.c",
    "old": "\t *  this tree at all -- there is no ATA specification here -- so a mask-only\n\t *  correction is exactly as much as the source can justify.",
    "new": "\t *  this tree at all, so a mask-only\n\t *  correction is exactly as much as the source can justify.",
    "why": "Remove the stale claim that no ATA specification exists here."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_WDCATADOCSTALE: DEFECT, 1 FINDINGS
1. The diff does NOT remove the defect at every site the issue names. It edits `dev_wdc.c` around line 421, but completely misses the other three sites named in the issue: `dev_wdc.c:1080-1081`, `regress/diff_wdc_identify.c:25-26`, and `regress/gate_offline.sh:1525`. 
2. CONTROL FLOW: No added `return`, `goto`, `break`, or early exit. The edit strictly changes text within a block comment.
3. RETURN VALUE: No path returns anything different. The edit is entirely contained within a C comment.
4. What ELSE does the diff change: Nothing. The diff only deletes the text `-- there is no ATA specification here --` from one block comment.
5. House idioms: The modified comment line (421) stays within the 79-column limit.
Finding 1: 
`src/devices/dev_wdc.c:421`, DEFECT, Fix misses `dev_wdc.c:1080-1081`, `regress/diff_wdc_identify.c:25-26`, and `regress/gate_offline.sh:1525`.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_WDCATADOCSTALE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_WDCATADOCSTALE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
