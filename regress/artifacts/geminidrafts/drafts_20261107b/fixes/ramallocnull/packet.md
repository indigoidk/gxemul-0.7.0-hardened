# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ramallocnull` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ramallocnull`, state `open`, severity `LOW`)

**title:** src/devices/dev_ram.c:155,182-185 -- the strdup() of the device name and the mirror-name malloc() are used without a NULL test -- NULL (host out-of-memory only)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- wrap strdup and malloc calls with NULL checks

## The code at the cited lines

### `src/devices/dev_ram.c` around the row's cited line 155 (HEAD 8d9df658, lines 35-236)

```c
   35| #include <string.h>
   36| #include <sys/types.h>
   37| #include <sys/mman.h>
   38| 
   39| #include "cpu.h"
   40| #include "devices.h"
   41| #include "machine.h"
   42| #include "memory.h"
   43| #include "misc.h"
   44| 
   45| 
   46| struct ram_data {
   47| 	uint64_t	baseaddress;
   48| 	const char*	name;
   49| 
   50| 	int		trace;
   51| 	int		mode;
   52| 	uint64_t	otheraddress;
   53| 
   54| 	/*  If mode = DEV_RAM_MIRROR:  */
   55| 	uint64_t	offset;
   56| 
   57| 	/*  If mode = DEV_RAM_RAM:  */
   58| 	unsigned char	*data;
   59| 	uint64_t	length;
   60| };
   61| 
   62| 
   63| DEVICE_ACCESS(ram)
   64| {
   65| 	struct ram_data *d = (struct ram_data *) extra;
   66| 
   67| 	if (cpu->running && d->trace && writeflag == MEM_WRITE) {
   68| 		fatal("[ %s: write %i byte%s from 0x%x:",
   69| 		    d->name, (int)len, len==1? "":"s", (int)relative_addr);
   70| 		for (size_t i=0; i<len; i++)
   71| 			fatal(" %02x", data[i]);
   72| 		fatal(" ]\n");
   73| 	}
   74| 
   75| 	switch (d->mode) {
   76| 
   77| 	case DEV_RAM_MIRROR:
   78| 		/*  TODO:  how about caches?  */
   79| 		{
   80| 			int result = cpu->memory_rw(cpu, mem,
   81| 			    d->otheraddress + relative_addr, data, len,
   82| 			    writeflag, PHYSICAL);
   83| 			    
   84| 			/*  Invalidate any code translations in both the MIRRORED
   85| 			    and the MIRROR address ranges on a write:  */
   86| 			if (writeflag == MEM_WRITE &&
   87| 			    cpu->invalidate_code_translation != NULL) {
   88| 				cpu->invalidate_code_translation(
   89| 				    cpu, d->otheraddress + relative_addr,
   90| 				    INVALIDATE_PADDR);
   91| 				cpu->invalidate_code_translation(
   92| 				    cpu, d->baseaddress + relative_addr,
   93| 				    INVALIDATE_PADDR);
   94| 			}
   95| 
   96| 			if (cpu->running && d->trace && writeflag == MEM_READ) {
   97| 				fatal("[ %s: read %i byte%s from 0x%x:",
   98| 				    d->name, (int)len, len==1? "":"s", (int)relative_addr);
   99| 				for (size_t i=0; i<len; i++)
  100| 					fatal(" %02x", data[i]);
  101| 				fatal(" ]\n");
  102| 			}
  103| 
  104| 			return result;
  105| 		}
  106| 
  107| 	case DEV_RAM_RAM:
  108| 		if (writeflag == MEM_WRITE) {
  109| 			memcpy(&d->data[relative_addr], data, len);
  110| 
  111| 			/*  Invalidate any code translations on a write:  */
  112| 			if (cpu->invalidate_code_translation != NULL) {
  113| 				cpu->invalidate_code_translation(
  114| 				    cpu, d->baseaddress + relative_addr,
  115| 				    INVALIDATE_PADDR);
  116| 			}
  117| 		} else {
  118| 			memcpy(data, &d->data[relative_addr], len);
  119| 
  120| 			if (cpu->running && d->trace) {
  121| 				fatal("[ %s: read %i byte%s from 0x%x:",
  122| 				    d->name, (int)len, len==1? "":"s", (int)relative_addr);
  123| 				for (size_t i=0; i<len; i++)
  124| 					fatal(" %02x", data[i]);
  125| 				fatal(" ]\n");
  126| 			}
  127| 		}
  128| 		break;
  129| 
  130| 	default:
  131| 		fatal("dev_ram_access(): unknown mode %i\n", d->mode);
  132| 		exit(1);
  133| 	}
  134| 
  135| 	return 1;
  136| }
  137| 
  138| 
  139| /*
  140|  *  dev_ram_init():
  141|  *
  142|  *  Initializes a RAM or mirror device. Things get a bit complicated because
  143|  *  of dyntrans (i.e. mirrored memory ranges should be entered into the
  144|  *  translation arrays just as normal memory and other devices are).
  145|  */
  146| void dev_ram_init(struct machine *machine, uint64_t baseaddr, uint64_t length,
  147| 	int mode, uint64_t otheraddress, const char* name)
  148| {
  149| 	struct ram_data *d;
  150| 	int flags = DM_DEFAULT, points_to_ram = 1;
  151| 
  152| 	CHECK_ALLOCATION(d = (struct ram_data *) malloc(sizeof(struct ram_data)));
  153| 	memset(d, 0, sizeof(struct ram_data));
  154| 
  155| 	d->name = strdup((name == NULL) ? "ram" : name);
  156| 
  157| 	if (mode & DEV_RAM_MIGHT_POINT_TO_DEVICES) {
  158| 		mode &= ~DEV_RAM_MIGHT_POINT_TO_DEVICES;
  159| 		points_to_ram = 0;
  160| 	}
  161| 
  162| 	if (mode & DEV_RAM_TRACE_ALL_ACCESSES) {
  163| 		mode &= ~DEV_RAM_TRACE_ALL_ACCESSES;
  164| 		d->trace = 1;
  165| 	}
  166| 
  167| 	d->mode         = mode;
  168| 	d->baseaddress  = baseaddr;
  169| 	d->otheraddress = otheraddress;
  170| 
  171| 	switch (d->mode) {
  172| 
  173| 	case DEV_RAM_MIRROR:
  174| 		/*
  175| 		 *  Calculate the amount that the mirror memory is offset from
  176| 		 *  the real (physical) memory. This is used in src/memory_rw.c
  177| 		 *  with dyntrans accesses if DM_EMULATED_RAM is set.
  178| 		 */
  179| 		d->offset = baseaddr - otheraddress;
  180| 		
  181| 		{
  182| 			size_t mirrorNameAllocLen = strlen(d->name) + 15;
  183| 			char *mirrorName = (char*) malloc(mirrorNameAllocLen);
  184| 			snprintf(mirrorName, mirrorNameAllocLen, "%s [mirror]", d->name);
  185| 			d->name = mirrorName;
  186| 		}
  187| 
  188| 		/*  Aligned RAM? Then it works with dyntrans.  */
  189| 		if (points_to_ram &&
  190| 		    (baseaddr & (machine->arch_pagesize-1)) == 0 &&
  191| 		    (otheraddress & (machine->arch_pagesize - 1)) == 0 &&
  192| 		    (length & (machine->arch_pagesize - 1)) == 0 &&
  193| 		    !d->trace)
  194| 			flags |= DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK
  195| 			    | DM_EMULATED_RAM;
  196| 
  197| 		memory_device_register(machine->memory, d->name,
  198| 		    baseaddr, length, dev_ram_access, d, flags
  199| 		    | DM_READS_HAVE_NO_SIDE_EFFECTS, (unsigned char*) (void *) &d->offset);
  200| 		break;
  201| 
  202| 	case DEV_RAM_RAM:
  203| 		/*
  204| 		 *  Allocate zero-filled RAM using mmap(). If mmap() failed,
  205| 		 *  try malloc(), but then memset() must also be called, which
  206| 		 *  can be slow for large chunks of memory.
  207| 		 */
  208| 		d->length = length;
  209| 		d->data = (unsigned char *) mmap(NULL, length,
  210| 		    PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
  211| 		/*  #208: (Codex/Fable) mmap failure is MAP_FAILED, not NULL (the
  212| 		    #175 straggler); fall back to malloc instead of registering
  213| 		    RAM backed by (void*)-1.  */
  214| 		if (d->data == MAP_FAILED) {
  215| 			CHECK_ALLOCATION(d->data = (unsigned char *) malloc(length));
  216| 			memset(d->data, 0, length);
  217| 		}
  218| 
  219| 		/*  Aligned memory? Then it works with dyntrans.  */
  220| 		if ((baseaddr & (machine->arch_pagesize - 1)) == 0 &&
  221| 		    (length & (machine->arch_pagesize - 1)) == 0 &&
  222| 		    !d->trace)
  223| 			flags |= DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK;
  224| 
  225| 		memory_device_register(machine->memory, d->name, baseaddr,
  226| 		    d->length, dev_ram_access, d, flags
  227| 		    | DM_READS_HAVE_NO_SIDE_EFFECTS, d->data);
  228| 		break;
  229| 
  230| 	default:
  231| 		fatal("dev_ram_access(): %s: unknown mode %i\n", d->name, d->mode);
  232| 		exit(1);
  233| 	}
  234| }
  235| 
  236| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_ram.c` -- `struct ram_data {` (HEAD lines 46-60)

```c
   46| struct ram_data {
   47| 	uint64_t	baseaddress;
   48| 	const char*	name;
   49| 
   50| 	int		trace;
   51| 	int		mode;
   52| 	uint64_t	otheraddress;
   53| 
   54| 	/*  If mode = DEV_RAM_MIRROR:  */
   55| 	uint64_t	offset;
   56| 
   57| 	/*  If mode = DEV_RAM_RAM:  */
   58| 	unsigned char	*data;
   59| 	uint64_t	length;
   60| };
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

End with one line: `FIXDRAFT_RAMALLOCNULL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
