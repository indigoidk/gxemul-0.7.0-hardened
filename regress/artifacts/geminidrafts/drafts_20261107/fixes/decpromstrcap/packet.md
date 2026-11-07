# GXemul hardened fork -- DRAFT A FIX for one filed issue, `decpromstrcap` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `decpromstrcap`, state `open`, severity `LOW`)

**title:** src/promemul/dec_prom.c:66-71,247-266,323-327,336-343,393-405,615-618 -- the PROM strcmp, strlen, puts, printf (format and %s) and execute_cmd services scan guest memory one byte at a time with no maximum length, stopping only at the first zero byte -- WRONG-RESULT (guest firmware call)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Unbounded memory reads allow guest to force host into infinite loops or excessive work.

## The code at the cited lines

### `src/promemul/dec_prom.c` around the row's cited line 66 (HEAD 2d25df65, lines 21-111)

```c
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *
   27|  *
   28|  *  COMMENT: DECstation PROM emulation
   29|  *
   30|  *  Implementation note: Remember that only the lowest 32 bits of GPRs are
   31|  *  actually valid when using dyntrans with e.g. R3000 CPUs.
   32|  */
   33| 
   34| #include <stdio.h>
   35| #include <stdlib.h>
   36| #include <string.h>
   37| #include <sys/types.h>
   38| #include <sys/time.h>
   39| #include <sys/resource.h>
   40| 
   41| #include "console.h"
   42| #include "cpu.h"
   43| #include "cpu_mips.h"
   44| #include "diskimage.h"
   45| #include "machine.h"
   46| #include "machine_pmax.h"
   47| #include "memory.h"
   48| #include "misc.h"
   49| 
   50| #include "thirdparty/dec_prom.h"
   51| #include "thirdparty/dec_5100.h"
   52| #include "thirdparty/dec_kn01.h"
   53| #include "thirdparty/dec_kn02.h"
   54| #include "thirdparty/dec_kn03.h"
   55| 
   56| 
   57| extern int quiet_mode;
   58| 
   59| 
   60| /*
   61|  *  mem_readchar():
   62|  *
   63|  *  Reads a byte from emulated RAM, using a MIPS register as a base address.
   64|  *  (Helper function.)
   65|  */
   66| static unsigned char mem_readchar(struct cpu *cpu, int regbase, int offset)
   67| {
   68| 	unsigned char ch;
   69| 	cpu->memory_rw(cpu, cpu->mem, (int32_t)cpu->cd.mips.gpr[regbase] +
   70| 	    offset, &ch, sizeof(ch), MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
   71| 	return ch;
   72| }
   73| 
   74| 
   75| /*
   76|  *  dec_jumptable_func():
   77|  *
   78|  *  The jumptable is located at the beginning of the PROM, at 0xbfc00000 + i*8,
   79|  *  where i is the decimal function number. Many of these can be converted to
   80|  *  an identical callback function.
   81|  *
   82|  *  Return value is non-zero if the vector number was converted into a callback
   83|  *  function number, otherwise 0.
   84|  *
   85|  *	Vector	(dec)	Function
   86|  *	0x0	0	reset()
   87|  *	0x10	2	restart()
   88|  *	0x18	3	reinit()
   89|  *	0x30	6	open()
   90|  *	0x38	7	read()
   91|  *	0x58	11	lseek()
   92|  *	0x68	13	putchar()
   93|  *	0x88	17	printf()
   94|  *	0x108	33	getenv2()
   95|  */
   96| int dec_jumptable_func(struct cpu *cpu, int vector)
   97| {
   98| 	static int file_opened = 0;
   99| 	static int current_file_offset = 0;
  100| 
  101| 	switch (vector) {
  102| 	case 0x0:	/*  reset()  */
  103| 		/*  TODO  */
  104| 		cpu->running = 0;
  105| 		break;
  106| 	case 0x10:	/*  restart()  */
  107| 		/*  TODO  */
  108| 		cpu->running = 0;
  109| 		break;
  110| 	case 0x18:	/*  reinit()  */
  111| 		/*  TODO  */
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

End with one line: `FIXDRAFT_DECPROMSTRCAP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
