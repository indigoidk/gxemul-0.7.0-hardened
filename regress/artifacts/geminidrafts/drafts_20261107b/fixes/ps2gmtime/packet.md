# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ps2gmtime` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ps2gmtime`, state `open`, severity `LOW`)

**title:** src/machines/machine_playstation2.c:141-145 -- the gmtime() result is used without a NULL test (the argument is time(NULL) + 9*3600) -- NULL (host only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- add NULL check for tm_ptr before accessing its members

## The code at the cited lines

### `src/machines/machine_playstation2.c` around the row's cited line 141 (HEAD 8d9df658, lines 21-186)

```c
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: Sony PlayStation 2
   29|  */
   30| 
   31| #include <stdio.h>
   32| #include <stdlib.h>
   33| #include <string.h>
   34| #include <time.h>
   35| 
   36| #include "cpu.h"
   37| #include "device.h"
   38| #include "devices.h"
   39| #include "diskimage.h"
   40| #include "machine.h"
   41| #include "memory.h"
   42| #include "misc.h"
   43| 
   44| #define PLAYSTATION2_BDA        0xffffffffa0001000ULL
   45| #define PLAYSTATION2_OPTARGS    0xffffffff81fff100ULL
   46| #define PLAYSTATION2_SIFBIOS    0xffffffffbfc10000ULL
   47| 
   48| 
   49| static int int_to_bcd(int i)
   50| {
   51| 	return (i/10) * 16 + (i % 10);
   52| }
   53| 
   54| 
   55| MACHINE_SETUP(playstation2)
   56| {
   57| 	char tmpstr[200];
   58| 	int tmplen;
   59| 	char *tmp;
   60| 	time_t timet;
   61| 	struct tm *tm_ptr;
   62| 
   63| 	machine->machine_name = strdup("Playstation 2");
   64| 	cpu->byte_order = EMUL_LITTLE_ENDIAN;
   65| 
   66| 	if (machine->physical_ram_in_mb != 32)
   67| 		fprintf(stderr, "WARNING! Playstation 2 machines are supposed "
   68| 		    "to have exactly 32 MB RAM. Continuing anyway.\n");
   69| 	if (!machine->x11_md.in_use)
   70| 		fprintf(stderr, "WARNING! Playstation 2 without -X is pretty "
   71| 		    "meaningless. Continuing anyway.\n");
   72| 
   73| 	/*
   74| 	 *  According to NetBSD:
   75| 	 *
   76| 	 *	Hardware irq 0 is timer/interrupt controller
   77| 	 *	Hardware irq 1 is dma controller
   78| 	 *
   79| 	 *  Some things are not yet emulated (at all), and hence are detected
   80| 	 *  incorrectly:
   81| 	 *
   82| 	 *	sbus0 at mainbus0: controller type 2
   83| 	 *	ohci0 at sbus0		(at 0x1f801600, according to linux)
   84| 	 *	ohci0: OHCI version 1.0
   85| 	 */
   86| 
   87| 	device_add(machine, "ps2 addr=0x10000000");
   88| 	device_add(machine, "ps2_gs addr=0x12000000");
   89| 	device_add(machine, "ps2_ether addr=0x14001000");
   90| 
   91| 	/*  TODO: how much?  */
   92| 	dev_ram_init(machine, 0x1c000000, 4 * 1048576, DEV_RAM_RAM, 0, NULL);
   93| 
   94| 	/*  OHCI at SBUS irq 1:  */
   95| 	snprintf(tmpstr, sizeof(tmpstr), "ohci addr=0x1f801600 irq="
   96| 	    "%s.cpu[%i].ps2_sbus.1", machine->path, machine->bootstrap_cpu);
   97| 	device_add(machine, tmpstr);
   98| 
   99| 	/*  Set the Harddisk controller present flag, if either
  100| 	    disk 0 or 1 is present:  */
  101| 	if (diskimage_exist(machine, 0, DISKIMAGE_IDE) ||
  102| 	    diskimage_exist(machine, 1, DISKIMAGE_IDE)) {
  103| 		if (machine->prom_emulation)
  104| 			store_32bit_word(cpu, 0xa0000000 + machine->
  105| 			    physical_ram_in_mb*1048576 - 0x1000 + 0x0, 0x100);
  106| 		device_add(machine, "ps2_spd addr=0x14000000");
  107| 	}
  108| 
  109| 	if (!machine->prom_emulation)
  110| 		return;
  111| 
  112| 
  113| 	tmplen = 1000;
  114| 	CHECK_ALLOCATION(tmp = (char *) malloc(tmplen));
  115| 
  116| 	add_symbol_name(&machine->symbol_context,
  117| 	    PLAYSTATION2_SIFBIOS, 0x10000, "[SIFBIOS entry]", 0, 0);
  118| 	store_32bit_word(cpu, PLAYSTATION2_BDA + 0,
  119| 	    PLAYSTATION2_SIFBIOS);
  120| 	store_buf(cpu, PLAYSTATION2_BDA + 4, "PS2b", 4);
  121| 
  122| 	/*  "Magic trap" instruction for software PROM emulation:  */
  123| 	store_32bit_word(cpu, PLAYSTATION2_SIFBIOS, 0x00c0de0c);
  124| 
  125| 	store_32bit_word(cpu, 0xa0000000 + machine->physical_ram_in_mb
  126| 	    * 1048576 - 0x1000 + 0x4, PLAYSTATION2_OPTARGS);
  127| 
  128| 	strlcpy(tmp, "root=/dev/hda1 crtmode=vesa0,60", tmplen);
  129| 
  130| 	if (machine->boot_string_argument[0])
  131| 		snprintf(tmp+strlen(tmp), tmplen-strlen(tmp),
  132| 		    " %s", machine->boot_string_argument);
  133| 	tmp[tmplen-1] = '\0';
  134| 
  135| 	machine->bootstr = tmp;
  136| 	store_string(cpu, PLAYSTATION2_OPTARGS, machine->bootstr);
  137| 
  138| 	/*  TODO:  netbsd's bootinfo.h, for symbolic names  */
  139| 
  140| 	/*  RTC data given by the BIOS:  */
  141| 	timet = time(NULL) + 9*3600;	/*  PS2 uses Japanese time  */
  142| 	tm_ptr = gmtime(&timet);
  143| 	/*  TODO:  are these 0- or 1-based?  */
  144| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  145| 	    * 1048576 - 0x1000 + 0x10 + 1, int_to_bcd(tm_ptr->tm_sec));
  146| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  147| 	    * 1048576 - 0x1000 + 0x10 + 2, int_to_bcd(tm_ptr->tm_min));
  148| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  149| 	    * 1048576 - 0x1000 + 0x10 + 3, int_to_bcd(tm_ptr->tm_hour));
  150| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  151| 	    * 1048576 - 0x1000 + 0x10 + 5, int_to_bcd(tm_ptr->tm_mday));
  152| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  153| 	    * 1048576 - 0x1000 + 0x10 + 6, int_to_bcd(tm_ptr->tm_mon+1));
  154| 	store_byte(cpu, 0xa0000000 + machine->physical_ram_in_mb
  155| 	    * 1048576 - 0x1000 + 0x10 + 7, int_to_bcd(tm_ptr->tm_year-100));
  156| 
  157| 	/*  "BOOTINFO_PCMCIA_TYPE" in NetBSD's bootinfo.h. This
  158| 	    contains the sbus controller type.  */
  159| 	store_32bit_word(cpu, 0xa0000000 + machine->physical_ram_in_mb
  160| 	    * 1048576 - 0x1000 + 0x1c, 2);
  161| }
  162| 
  163| 
  164| MACHINE_DEFAULT_CPU(playstation2)
  165| {
  166| 	machine->cpu_name = strdup("R5900");
  167| }
  168| 
  169| 
  170| MACHINE_DEFAULT_RAM(playstation2)
  171| {
  172| 	machine->physical_ram_in_mb = 32;
  173| }
  174| 
  175| 
  176| MACHINE_REGISTER(playstation2)
  177| {
  178| 	MR_DEFAULT(playstation2, "Playstation 2", MACHINE_PS2);
  179| 
  180| 	machine_entry_add_alias(me, "playstation2");
  181| 	machine_entry_add_alias(me, "ps2");
  182| 
  183| 	me->set_default_ram = machine_default_ram_playstation2;
  184| }
  185| 
  186| 
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

End with one line: `FIXDRAFT_PS2GMTIME: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
