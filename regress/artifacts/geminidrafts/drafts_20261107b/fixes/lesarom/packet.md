# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `lesarom` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `lesarom`, state `open`)

**title:** devices/dev_le.c:DEVICE_ACCESS(le) -- the station-address ROM is not decoded at its slot+0x180000 alias and bytes 6-7 carry MAC copies instead of the ESAR checksum -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T58 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A2-8).  Source URLs: https://github.com/rpajarola/gxemul/commit/0c1e6d122a418955b36a2788a4dc9aaa5f4bbb2a.  Our site at de8c7547: src/devices/dev_le.c:955-956, :1027, :1086-1093 (lines of de8c7547; at 987cb596 the ROM read is :972-976 and the ROM fill :1103-1113, both 17 lines lower; :1027 moved the same way is :1044, the access switch's `default:` arm).  Portable fix: yes -- port rpajarola 0c1e6d1.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_le.c` -- AT HEAD, lines 953-1067 (`*` marks a line your previous draft changed)

```c
  953|  DEVICE_ACCESS(le)
  954|  {
  955|  	struct le_data *d = (struct le_data *) extra;
  956|  	uint64_t idata = 0, odata = 0;
  957|  	int retval = 1;
  958|  	size_t i;
  959|  
  960|  	if (writeflag == MEM_WRITE)
  961|  		idata = memory_readmax64(cpu, data, len);
  962|  
  963|  #ifdef LE_DEBUG
  964|  	if (writeflag == MEM_WRITE) {
  965|  		fatal("[ le: write to addr 0x%06x: ", (int)relative_addr);
  966|  		for (i=0; i<len; i++)
  967|  			fatal("%02x ", data[i]);
  968|  		fatal("]\n");
  969|  	}
  970|  #endif
  971|  
  972|  	/*  Read from station's ROM (ethernet address):  */
  973|* 	if (relative_addr >= 0xc0000 && relative_addr <= 0xfffff) {
  974|* 		uint32_t a;
  975|  		int j = (relative_addr & 0xff) / 4;
  976|  		a = d->rom[j & (ROM_SIZE-1)];
  977|  
  978|  		if (writeflag == MEM_READ) {
  979|  			odata = (a << 24) + (a << 16) + (a << 8) + a;
  980|  		} else {
  981|  			fatal("[ le: WRITE to ethernet addr (%08lx):",
  982|  			    (long)relative_addr);
  983|  			for (i=0; i<len; i++)
  984|  				fatal(" %02x", data[i]);
  985|  			fatal(" ]\n");
  986|  		}
  987|  
  988|  		retval = 13;	/*  13 cycles  */
  989|  		goto do_return;
  990|  	}
  991|  
  992|  
  993|  	switch (relative_addr) {
  994|  
  995|  	/*  Register read/write:  */
  996|  	case 0:
  997|  		if (writeflag==MEM_READ) {
  998|  			odata = d->reg[d->reg_select];
  999|  			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 1000|  			    "READ from register 0x%02x: 0x"
 1001|  			    "%02x", d->reg_select, (int)odata);
 1002|  
 1003|  			/*
 1004|  			 *  #573: CSR1..3 are accessible only while the STOP bit
 1005|  			 *  is SET (a read with STOP clear is "undefined" on the
 1006|  			 *  chip).  The old comment reported that Ultrix seems to
 1007|  			 *  read them with STOP set -- the in-spec case.  The model
 1008|  			 *  answers in either state; gating on STOP is filed, not
 1009|  			 *  implemented, and nothing is announced either way.
 1010|  			 */
 1011|  		} else {
 1012|  			debugmsg(d->subsys, "register", VERBOSITY_DEBUG,
 1013|  			    "WRITE to register 0x%02x: 0x%02x",
 1014|  			    d->reg_select, (int)idata);
 1015|  			/*
 1016|  			 *  #573: a write to CSR1..3 with STOP CLEAR is the one
 1017|  			 *  the chip ignores; writes with STOP set are the normal
 1018|  			 *  case (the old comment reported Ultrix writing them with
 1019|  			 *  STOP set).  The model accepts both -- gating on STOP is
 1020|  			 *  filed, not implemented.
 1021|  			 */
 1022|  			le_register_write(d, d->reg_select, idata);
 1023|  		}
 1024|  		break;
 1025|  
 1026|  	/*  Register select:  */
 1027|  	case 4:
 1028|  		if (writeflag==MEM_READ) {
 1029|  			odata = d->reg_select;
 1030|  			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
 1031|  			    "READ: 0x%02x", (int)odata);
 1032|  		} else {
 1033|  			debugmsg(d->subsys, "register select", VERBOSITY_DEBUG,
 1034|  			     "WRITE: 0x%02x", (int)idata);
 1035|  			d->reg_select = idata & (N_REGISTERS - 1);
 1036|  
 1037|  			if (idata >= N_REGISTERS)
 1038|  				debugmsg(d->subsys, "register select", VERBOSITY_WARNING,
 1039|  				    "WARNING! register %" PRIu64
 1040|  				    " (max is %i)", (uint64_t)idata,
 1041|  				    N_REGISTERS - 1);
 1042|  		}
 1043|  		break;
 1044|  
 1045|  	default:
 1046|  		if (writeflag==MEM_READ) {
 1047|  			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
 1048|  			    "read from UNIMPLEMENTED addr 0x%06x",
 1049|  			    (int)relative_addr);
 1050|  		} else {
 1051|  			debugmsg(d->subsys, "access", VERBOSITY_WARNING,
 1052|  			    "write to UNIMPLEMENTED addr 0x%06x: "
 1053|  			    "0x%08x", (int)relative_addr, (int)idata);
 1054|  		}
 1055|  	}
 1056|  
 1057|  do_return:
 1058|  	if (writeflag == MEM_READ) {
 1059|  		memory_writemax64(cpu, data, len, odata);
 1060|  		debugmsg(d->subsys, "access", VERBOSITY_DEBUG,
 1061|  		    "read from addr 0x%06" PRIx64 ": 0x%08" PRIx64, (uint64_t)relative_addr, (uint64_t)odata);
 1062|  	}
 1063|  
 1064|  	dev_le_tick(cpu, extra);
 1065|  
 1066|  	return retval;
 1067|  }
```

## The data structures those files define (every field that exists)

### `src/devices/dev_le.c` -- `struct le_data {` (HEAD lines 84-128)

```c
   84| struct le_data {
   85| 	struct nic_data	nic;
   86| 
   87| 	int		subsys;		/*  for debugmsg  */
   88| 
   89| 	struct interrupt irq;
   90| 	int		irq_asserted;
   91| 
   92| 	uint64_t	buf_start;
   93| 	uint64_t	buf_end;
   94| 	int		len;
   95| 
   96| 	uint8_t		rom[ROM_SIZE];
   97| 
   98| 	int		reg_select;
   99| 	uint16_t	reg[N_REGISTERS];
  100| 
  101| 	int		is_bigendian;
  102| 
  103| 	unsigned char	*sram;
  104| 
  105| 	/*  Initialization block:  */
  106| 	uint32_t	init_block_addr;
  107| 
  108| 	uint16_t	mode;
  109| 	uint16_t	ladrf[4];
  110| 	uint32_t	rdra;	/*  receive descriptor ring address  */
  111| 	int		rlen;	/*  nr of rx descriptors  */
  112| 	uint32_t	tdra;	/*  transmit descriptor ring address  */
  113| 	int		tlen;	/*  nr ot tx descriptors  */
  114| 
  115| 	int		allmulti;/* receive all multicast packets */
  116| 
  117| 	/*  Current rx and tx descriptor indices:  */
  118| 	int		rxp;
  119| 	int		txp;
  120| 
  121| 	unsigned char	*tx_packet;
  122| 	int		tx_packet_len;
  123| 
  124| 	unsigned char	*rx_packet;
  125| 	int		rx_packet_len;
  126| 	int		rx_packet_offset;
  127| 	int		rx_middle_bit;
  128| };
```


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_le.c",
    "old": "\t/*  Read from station's ROM (ethernet address):  */\n\tif (relative_addr >= 0xc0000 && relative_addr <= 0xfffff) {\n\t\tuint32_t a;\n\t\tint j = (relative_addr & 0xff) / 4;",
    "new": "\t/*  Read from station's ROM (ethernet address):  */\n\tif ((relative_addr >= 0xc0000 && relative_addr <= 0xfffff) ||\n\t    (relative_addr >= 0x180000 && relative_addr <= 0x1bffff)) {\n\t\tuint32_t a;\n\t\tint j = (relative_addr & 0xff) / 4;",
    "why": "Decode the station-address ROM at its 0x180000 alias as well"
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_LESAROM: DEFECT, 2 FINDINGS
1. No, the diff does not remove the defect at every site the issue names. It successfully addresses the decoding alias at `0x180000`, but completely misses the ESAR checksum bug. The issue states "bytes 6-7 carry MAC copies instead of the ESAR checksum" and notes the ROM fill occurs at lines 1103-1113. The diff leaves the ROM fill entirely untouched.
2. CONTROL FLOW: No added `return`, `goto`, or `break` skips code. The diff only expands the boolean expression in the `if` condition with an `||` operator. Execution correctly falls through to the existing `goto do_return;` at line 990, which accurately routes execution to the common tail (`do_return:` at line 1058).
3. RETURN VALUE: Yes. Accesses to the `0x180000`-`0x1bffff` range previously fell through to the `default:` switch case and returned `1`. Now, they enter the ROM block and return `13` (via `retval = 13;`). The shown code (`/*  13 cycles  */`) implies this value represents the number of clock/bus cycles the device takes to complete the read.
4. Beyond removing the read defect, routing the alias into this block means a guest write to the `0x180000` range now triggers a `fatal()` error at line 982 instead of safely warning about an UNIMPLEMENTED address. Because this is a hardened fork designed to remove crash-on-malformed-input defects, exposing a path where guest software can crash the host emulator on an alias write is a regression/defect.
5. House idioms: The diff introduces no new comments and stays within 79 columns. However, as noted above, keeping the `fatal()` on the write path violates the project's robustness goals (crash-on-malformed-input).
src/devices/dev_le.c:UNSETTLED (lines 1103-1113 missing from excerpt), severity DEFECT. Fix in ONE line: Update the ROM fill sequence to calculate and write the correct ESAR checksum to bytes 6 and 7 instead of copying the MAC.
src/devices/dev_le.c:982, severity DEFECT. Fix in ONE line: `debugmsg(d->subsys, "access", VERBOSITY_WARNING, "[ le: WRITE to ethernet addr (%08lx) ]\n", (long)relative_addr);`
FIXREVIEW_LESAROM: DEFECT, 2 FINDINGS
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

End with two lines: `REVISION_LESAROM: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_LESAROM: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
