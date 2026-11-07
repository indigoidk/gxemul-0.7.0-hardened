# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mk48gmtime` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mk48gmtime`, state `open`, severity `LOW`)

**title:** src/devices/dev_mk48txx.c:63-66 -- the gmtime() result is used without a NULL test (the argument is time(NULL)) -- NULL (host only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Critical but simple host-side NULL dereference.

## The code at the cited lines

### `src/devices/dev_mk48txx.c` around the row's cited line 63 (HEAD 2d25df65, lines 18-108)

```c
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *
   27|  *
   28|  *  COMMENT: Mostek MK48Txx Real Time Clock
   29|  *
   30|  *  TODO:
   31|  *	Only the MK48T08 is implemented so far.
   32|  */
   33| 
   34| #include <stdio.h>
   35| #include <stdlib.h>
   36| #include <string.h>
   37| #include <time.h>
   38| 
   39| #include "cpu.h"
   40| #include "device.h"
   41| #include "emul.h"
   42| #include "machine.h"
   43| #include "memory.h"
   44| #include "misc.h"
   45| 
   46| #include "thirdparty/mk48txxreg.h"
   47| 
   48| 
   49| #define	MK48TXX_LEN		MK48T08_CLKSZ
   50| 
   51| #define	BCD(x)	((((x) / 10) << 4) + ((x) % 10))
   52| 
   53| struct mk48txx_data {
   54| 	uint8_t		reg[MK48TXX_LEN];
   55| };
   56| 
   57| 
   58| void mk48txx_update_regs(struct mk48txx_data *d)
   59| {
   60| 	struct tm *tmp;
   61| 	time_t timet;
   62| 
   63| 	timet = time(NULL);
   64| 	tmp = gmtime(&timet);
   65| 
   66| 	d->reg[MK48T08_CLKOFF + MK48TXX_ISEC] = BCD(tmp->tm_sec);
   67| 	d->reg[MK48T08_CLKOFF + MK48TXX_IMIN] = BCD(tmp->tm_min);
   68| 	d->reg[MK48T08_CLKOFF + MK48TXX_IHOUR] = BCD(tmp->tm_hour);
   69| 	d->reg[MK48T08_CLKOFF + MK48TXX_IWDAY] = tmp->tm_wday + 1;
   70| 	d->reg[MK48T08_CLKOFF + MK48TXX_IDAY] = BCD(tmp->tm_mday);
   71| 	d->reg[MK48T08_CLKOFF + MK48TXX_IMON] = BCD(tmp->tm_mon + 1);
   72| 	d->reg[MK48T08_CLKOFF + MK48TXX_IYEAR] = BCD(tmp->tm_year % 100);
   73| }
   74| 
   75| 
   76| DEVICE_ACCESS(mk48txx)
   77| {
   78| 	struct mk48txx_data *d = (struct mk48txx_data *) extra;
   79| 	uint64_t idata = 0, odata = 0;
   80| 
   81| 	if (writeflag == MEM_WRITE)
   82| 		idata = memory_readmax64(cpu, data, len);
   83| 
   84| 	if (writeflag == MEM_READ)
   85| 		odata = d->reg[relative_addr];
   86| 
   87| 	/*  #521 (mk48nvramkill): the lower bound was MK48T08_CLKOFF, i.e. 0x1ff0,
   88| 	    and it was missing its `+ MK48TXX_ICSR'.  The switch below holds exactly
   89| 	    ONE case, MK48T08_CLKOFF + MK48TXX_ICSR (0x1ff8), so the eight offsets
   90| 	    0x1ff0..0x1ff7 fell through it to a `default:' that calls exit(1) --
   91| 	    EIGHT bytes inside the device's own 8192-byte registration ending the
   92| 	    emulator process on an ordinary access.  MEASURED at rung 3 BEFORE this
   93| 	    edit, on unmodified `-E mvme88k -e mvme187':
   94| 	        artifacts/mk48nvramkill/opus_mk48_nvram_witness_20260910.py
   95| 	        artifacts/mk48nvramkill/opus_witness_run_20260910.txt  -- 15/47,
   96| 	            all 15 controls green and all 32 kill rows red.
   97| 	    THE POPULATION IS SIXTEEN CELLS, NOT EIGHT: every offset kills in BOTH
   98| 	    directions, ld.bu and st.b alike, and all sixteen were driven.  The kill
   99| 	    is WIDTH-INDEPENDENT -- `len' never enters the guard, so ld / ld.h /
  100| 	    ld.bu all die at the same start offset and there is no width axis here.
  101| 
  102| 	    THOSE EIGHT ARE ORDINARY NVRAM ON THIS PART, which is what licenses
  103| 	    accepting them rather than declining.  mk48txxreg.h says the first bank
  104| 	    of eight registers at (nvramsz - 16) -- exactly 0x1ff0 -- is "available
  105| 	    only on more recent MK48Txx models", and names them IFLAGS, IASEC,
  106| 	    IAMIN, IAHOUR, IADAY, IINTR, IWDOG.  They are the MK48T59's alarm and
  107| 	    watchdog bank; this file implements the MK48T08 alone, where the region
  108| 	    is plain non-volatile RAM.  Storage already existed -- `reg' is
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_MK48GMTIME: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
