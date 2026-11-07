# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `ramallocnull` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `ramallocnull`, state `open`)

**title:** src/devices/dev_ram.c:155,182-185 -- the strdup() of the device name and the mirror-name malloc() are used without a NULL test -- NULL (host out-of-memory only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- lines 155 and 183

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_ram.c b/src/devices/dev_ram.c
index 40eae887..d8d318d9 100644
--- a/src/devices/dev_ram.c
+++ b/src/devices/dev_ram.c
@@ -152,7 +152,7 @@ void dev_ram_init(struct machine *machine, uint64_t baseaddr, uint64_t length,
 	CHECK_ALLOCATION(d = (struct ram_data *) malloc(sizeof(struct ram_data)));
 	memset(d, 0, sizeof(struct ram_data));
 
-	d->name = strdup((name == NULL) ? "ram" : name);
+	CHECK_ALLOCATION(d->name = strdup((name == NULL) ? "ram" : name));
 
 	if (mode & DEV_RAM_MIGHT_POINT_TO_DEVICES) {
 		mode &= ~DEV_RAM_MIGHT_POINT_TO_DEVICES;
@@ -180,7 +180,8 @@ void dev_ram_init(struct machine *machine, uint64_t baseaddr, uint64_t length,
 		
 		{
 			size_t mirrorNameAllocLen = strlen(d->name) + 15;
-			char *mirrorName = (char*) malloc(mirrorNameAllocLen);
+			char *mirrorName;
+			CHECK_ALLOCATION(mirrorName = (char*) malloc(mirrorNameAllocLen));
 			snprintf(mirrorName, mirrorNameAllocLen, "%s [mirror]", d->name);
 			d->name = mirrorName;
 		}
```

## Every edited function, after the fix

### `src/devices/dev_ram.c` -- post-edit lines 148-235 (`+` marks a line the diff added or the point of a deletion)

```c
  148|  {
  149|  	struct ram_data *d;
  150|  	int flags = DM_DEFAULT, points_to_ram = 1;
  151|  
  152|  	CHECK_ALLOCATION(d = (struct ram_data *) malloc(sizeof(struct ram_data)));
  153|  	memset(d, 0, sizeof(struct ram_data));
  154|  
  155|+ 	CHECK_ALLOCATION(d->name = strdup((name == NULL) ? "ram" : name));
  156|  
  157|  	if (mode & DEV_RAM_MIGHT_POINT_TO_DEVICES) {
  158|  		mode &= ~DEV_RAM_MIGHT_POINT_TO_DEVICES;
  159|  		points_to_ram = 0;
  160|  	}
  161|  
  162|  	if (mode & DEV_RAM_TRACE_ALL_ACCESSES) {
  163|  		mode &= ~DEV_RAM_TRACE_ALL_ACCESSES;
  164|  		d->trace = 1;
  165|  	}
  166|  
  167|  	d->mode         = mode;
  168|  	d->baseaddress  = baseaddr;
  169|  	d->otheraddress = otheraddress;
  170|  
  171|  	switch (d->mode) {
  172|  
  173|  	case DEV_RAM_MIRROR:
  174|  		/*
  175|  		 *  Calculate the amount that the mirror memory is offset from
  176|  		 *  the real (physical) memory. This is used in src/memory_rw.c
  177|  		 *  with dyntrans accesses if DM_EMULATED_RAM is set.
  178|  		 */
  179|  		d->offset = baseaddr - otheraddress;
  180|  		
  181|  		{
  182|  			size_t mirrorNameAllocLen = strlen(d->name) + 15;
  183|+ 			char *mirrorName;
  184|+ 			CHECK_ALLOCATION(mirrorName = (char*) malloc(mirrorNameAllocLen));
  185|  			snprintf(mirrorName, mirrorNameAllocLen, "%s [mirror]", d->name);
  186|  			d->name = mirrorName;
  187|  		}
  188|  
  189|  		/*  Aligned RAM? Then it works with dyntrans.  */
  190|  		if (points_to_ram &&
  191|  		    (baseaddr & (machine->arch_pagesize-1)) == 0 &&
  192|  		    (otheraddress & (machine->arch_pagesize - 1)) == 0 &&
  193|  		    (length & (machine->arch_pagesize - 1)) == 0 &&
  194|  		    !d->trace)
  195|  			flags |= DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK
  196|  			    | DM_EMULATED_RAM;
  197|  
  198|  		memory_device_register(machine->memory, d->name,
  199|  		    baseaddr, length, dev_ram_access, d, flags
  200|  		    | DM_READS_HAVE_NO_SIDE_EFFECTS, (unsigned char*) (void *) &d->offset);
  201|  		break;
  202|  
  203|  	case DEV_RAM_RAM:
  204|  		/*
  205|  		 *  Allocate zero-filled RAM using mmap(). If mmap() failed,
  206|  		 *  try malloc(), but then memset() must also be called, which
  207|  		 *  can be slow for large chunks of memory.
  208|  		 */
  209|  		d->length = length;
  210|  		d->data = (unsigned char *) mmap(NULL, length,
  211|  		    PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
  212|  		/*  #208: (Codex/Fable) mmap failure is MAP_FAILED, not NULL (the
  213|  		    #175 straggler); fall back to malloc instead of registering
  214|  		    RAM backed by (void*)-1.  */
  215|  		if (d->data == MAP_FAILED) {
  216|  			CHECK_ALLOCATION(d->data = (unsigned char *) malloc(length));
  217|  			memset(d->data, 0, length);
  218|  		}
  219|  
  220|  		/*  Aligned memory? Then it works with dyntrans.  */
  221|  		if ((baseaddr & (machine->arch_pagesize - 1)) == 0 &&
  222|  		    (length & (machine->arch_pagesize - 1)) == 0 &&
  223|  		    !d->trace)
  224|  			flags |= DM_DYNTRANS_OK | DM_DYNTRANS_WRITE_OK;
  225|  
  226|  		memory_device_register(machine->memory, d->name, baseaddr,
  227|  		    d->length, dev_ram_access, d, flags
  228|  		    | DM_READS_HAVE_NO_SIDE_EFFECTS, d->data);
  229|  		break;
  230|  
  231|  	default:
  232|  		fatal("dev_ram_access(): %s: unknown mode %i\n", d->name, d->mode);
  233|  		exit(1);
  234|  	}
  235|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_RAMALLOCNULL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_RAMALLOCNULL: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

## YOUR PREVIOUS REVIEW OF THIS DRAFT SAID UNSETTLED -- here is what it said, and the definitions it named

```text
FIXREVIEW_RAMALLOCNULL: UNSETTLED, 2 FINDINGS
1. **Defect removal**: The diff successfully wraps the `strdup` at line 155 and the `malloc` at line 184 with `CHECK_ALLOCATION`, covering all sites named in the issue. No missing sites.
2. **Control flow**: UNSETTLED. The diff uses the `CHECK_ALLOCATION()` macro, whose definition is not present in this file. Whether a failed allocation results in an early `return` (skipping the rest of the initialization), an `exit()`, or a `goto` cannot be determined without the header file that defines this macro.
3. **Return value**: The function `dev_ram_init` returns `void`. For the success path, the return behavior remains unchanged. On failure, it depends on the unsettled macro definition. 
4. **Other changes**: The diff splits the declaration and assignment of `mirrorName` into two separate lines (lines 183 and 184). No other guest-visible states or values are changed.
5. **House idioms**: The edit introduces a line that exceeds the 79-column limit. Assuming 8-space tabs, line 184 has 3 tabs (24 characters) plus 66 characters of code, totaling 90 columns.
**Findings:**
*   `src/devices/dev_ram.c:155,184`: UNSETTLED - The control flow behavior of `CHECK_ALLOCATION` on failure cannot be verified. We need the header file defining `CHECK_ALLOCATION` to settle this.
*   `src/devices/dev_ram.c:184`, STYLE, Smallest fix: Wrap the arguments inside the macro to stay under 79 columns, e.g., breaking after the equals sign or `malloc`.
```

### `src/include/misc.h` lines 182-198 (where HEAD defines `CHECK_ALLOCATION`)

```c
  182| 		char where_msg[400];					\
  183| 		snprintf(where_msg, sizeof(where_msg),			\
  184| 		    "%s, line %i, function %s().\n",			\
  185| 		    __FILE__, __LINE__, __func__);			\
  186|         	fprintf(stderr, "\n%s, in %s\n", error_msg, where_msg);	\
  187| 		exit(1);						\
  188| 	}
  189| 
  190| #define	CHECK_ALLOCATION(ptr)					{	\
  191| 		if ((ptr) == NULL)					\
  192| 			FAILURE("Out of memory");			\
  193| 	}
  194| 
  195| 
  196| /*
  197|  *  READ_WORD_LE / READ_WORD_BE:
  198|  *
```

### `src/devices/dev_ram.c` lines 138-154 (where HEAD defines `dev_ram_init`)

```c
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
```

### `src/include/devices.h` lines 368-384 (where HEAD defines `dev_ram_init`)

```c
  368| 
  369| /*  dev_ram.c:  */
  370| #define	DEV_RAM_RAM				0
  371| #define	DEV_RAM_MIRROR				1
  372| #define	DEV_RAM_MIGHT_POINT_TO_DEVICES		0x10
  373| #define	DEV_RAM_TRACE_ALL_ACCESSES		0x20
  374| int dev_ram_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
  375| 	unsigned char *data, size_t len, int writeflag, void *);
  376| void dev_ram_init(struct machine *machine, uint64_t baseaddr, uint64_t length,
  377| 	int mode, uint64_t otheraddr, const char* name);
  378| 
  379| /*  dev_scc.c:  */
  380| #define	DEV_SCC_LENGTH			0x1000
  381| int dev_scc_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
  382| 	unsigned char *data, size_t len, int writeflag, void *);
  383| int dev_scc_dma_func(struct cpu *cpu, void *extra, uint64_t addr,
  384| 	size_t dma_len, int tx);
```

Review the draft again with these in view.  If it still cannot be settled, say UNSETTLED and name the exact function or
definition still missing.
