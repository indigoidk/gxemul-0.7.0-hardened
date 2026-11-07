# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `gssiglblid` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `gssiglblid`, state `open`)

**title:** ps2_gs: N_GS_REGS excludes the file's own highest register, so SIGLBLID (0x1080) is refused -- writes dropped, reads 0

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): omised (dev_rtc.c:54-82, :158; doc/experiments.html:512). * `gssiglblid` MED -- ps2_gs: `N_GS_REGS 0x108` excludes the file's own highest register, so SIGLBLID (0x108) is refused (writes dropped, reads 0) by #99's guard (dev_ps2_gs.c:46, :77-81, :94-105). No GS manual on disk; ruled on the file's own table (the draft's DOUBTFUL overturned). * `mpstartupsp` MED -- dev_mp ST

**The drafter's own reading:** STILL PRESENT: YES -- dev_ps2_gs.c:46

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_ps2_gs.c b/src/devices/dev_ps2_gs.c
index 4b9933be..29fc5321 100644
--- a/src/devices/dev_ps2_gs.c
+++ b/src/devices/dev_ps2_gs.c
@@ -43,7 +43,7 @@
 /*  NOTE/TODO: This should be the same as in ps2_stuff:  */
 #define	DEV_PS2_GIF_FAKE_BASE		0x50000000
 
-#define	N_GS_REGS	0x108
+#define	N_GS_REGS	0x109
 
 struct gs_data {
 	uint64_t	reg[N_GS_REGS];		/*  GS registers  */
```

## Every edited function, after the fix

### `src/devices/dev_ps2_gs.c` -- post-edit lines 1-106 (`+` marks a line the diff added or the point of a deletion)

```c
    1|  /*
    2|   *  Copyright (C) 2003-2009  Anders Gavare.  All rights reserved.
    3|   *
    4|   *  Redistribution and use in source and binary forms, with or without
    5|   *  modification, are permitted provided that the following conditions are met:
    6|   *
    7|   *  1. Redistributions of source code must retain the above copyright
    8|   *     notice, this list of conditions and the following disclaimer.
    9|   *  2. Redistributions in binary form must reproduce the above copyright  
   10|   *     notice, this list of conditions and the following disclaimer in the 
   11|   *     documentation and/or other materials provided with the distribution.
   12|   *  3. The name of the author may not be used to endorse or promote products
   13|   *     derived from this software without specific prior written permission.
   14|   *
   15|   *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|   *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|   *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|   *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|   *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|   *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|   *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|   *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|   *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|   *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|   *  SUCH DAMAGE.
   26|   *   
   27|   *
   28|   *  COMMENT: PlayStation 2 graphics system
   29|   */
   30|  
   31|  #include <stdio.h>
   32|  #include <stdlib.h>
   33|  #include <string.h>
   34|  
   35|  #include "device.h"
   36|  #include "machine.h"
   37|  #include "memory.h"
   38|  #include "misc.h"
   39|  
   40|  
   41|  #define	DEV_PS2_GS_LENGTH		0x2000
   42|  
   43|  /*  NOTE/TODO: This should be the same as in ps2_stuff:  */
   44|  #define	DEV_PS2_GIF_FAKE_BASE		0x50000000
   45|  
   46|+ #define	N_GS_REGS	0x109
   47|  
   48|  struct gs_data {
   49|  	uint64_t	reg[N_GS_REGS];		/*  GS registers  */
   50|  };
   51|  
   52|  #define	GS_S_PMODE_REG		0x00
   53|  #define	GS_S_SMODE1_REG		0x01
   54|  #define	GS_S_SMODE2_REG		0x02
   55|  #define	GS_S_SRFSH_REG		0x03
   56|  #define	GS_S_SYNCH1_REG		0x04
   57|  #define	GS_S_SYNCH2_REG		0x05
   58|  #define	GS_S_SYNCV_REG		0x06
   59|  #define	GS_S_DISPFB1_REG	0x07
   60|  #define	GS_S_DISPLAY1_REG	0x08
   61|  #define	GS_S_DISPFB2_REG	0x09
   62|  #define	GS_S_DISPLAY2_REG	0x0a
   63|  #define	GS_S_EXTBUF_REG0	0x0b
   64|  #define	GS_S_EXTDATA_REG	0x0c
   65|  #define	GS_S_EXTWRITE_REG	0x0d
   66|  #define	GS_S_BGCOLOR_REG	0x0e
   67|  
   68|  //static const char *gs_reg_names[15] = {
   69|  //	"PMODE", "SMODE1", "SMODE2", "SRFSH",
   70|  //	"SYNCH1", "SYNCH2", "SYNCV", "DISPFB1",
   71|  //	"DISPLAY1", "DISPFB2", "DISPLAY2", "EXTBUF",
   72|  //	"EXTDATA", "EXTWRITE", "BGCOLOR"  };
   73|  
   74|  #define	GS_S_CSR_REG		0x100
   75|  #define	GS_S_IMR_REG		0x101
   76|  #define	GS_S_BUSDIR_REG		0x104
   77|  #define	GS_S_SIGLBLID_REG	0x108
   78|  
   79|  //static const char *gs_reg_high_names[4] = {
   80|  //	"CSR", "IMR", "BUSDIR", "SIGLBLID"
   81|  //	};
   82|  
   83|  
   84|  DEVICE_ACCESS(ps2_gs)
   85|  {
   86|  	struct gs_data *d = (struct gs_data *) extra;
   87|  	uint64_t idata = 0, odata = 0;
   88|  	size_t i;
   89|  	int regnr;
   90|  
   91|  	if (writeflag == MEM_WRITE)
   92|  		idata = memory_readmax64(cpu, data, len);
   93|  
   94|  	regnr = relative_addr / 16;
   95|  	if (regnr < 0 || regnr >= N_GS_REGS) {	/* #99: guest offset can exceed reg[] */
   96|  		static int warned = 0;	/* #119: loud-once (course-correction; was debug) */
   97|  		if (!warned) {
   98|  			fatal("[ gs: register access out of range (addr 0x%x); "
   99|  			    "ignored ]\n", (int)relative_addr);
  100|  			warned = 1;
  101|  		}
  102|  		if (writeflag == MEM_READ)
  103|  			memory_writemax64(cpu, data, len, 0);
  104|  		return 1;
  105|  	}
  106|  	if (relative_addr & 0xf) {
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_GSSIGLBLID: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_GSSIGLBLID: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
