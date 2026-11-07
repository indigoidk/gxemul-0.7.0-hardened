# GXemul hardened fork -- DRAFT A FIX for one filed issue, `cpurunningtype` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `cpurunningtype`, state `open`, severity `LOW`)

**title:** cpus/cpu.c:cpu_new -- `bool running` is registered as SETTINGS_TYPE_UINT8, so a debugger assignment can store a byte other than 0/1 -- HYGIENE (debugger-only UB)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T143 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A1-17).  Source URLs: https://github.com/retroprom/gxemul/commit/6f477da8.  Our site at de8c7547: src/cpus/cpu.c:93; src/core/settings.c:223-224.  Portable fix: yes -- port upstream 6f477da8.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Portable fix available upstream.

## The code at the cited lines

### `src/cpus/cpu.c` around the row's cited line 93 (HEAD d2a6f233, lines 48-138)

```c
   48| 
   49| /*
   50|  *  cpu_new():
   51|  *
   52|  *  Create a new cpu object.  Each family is tried in sequence until a
   53|  *  CPU family recognizes the cpu_type_name.
   54|  *
   55|  *  If there was no match, NULL is returned. Otherwise, a pointer to an
   56|  *  initialized cpu struct is returned.
   57|  */
   58| struct cpu *cpu_new(struct memory *mem, struct machine *machine,
   59|         int cpu_id, char *name)
   60| {
   61| 	char *cpu_type_name;
   62| 	char tmpstr[30];
   63| 
   64| 	if (name == NULL) {
   65| 		debugmsg(SUBSYS_CPU, "", VERBOSITY_ERROR, "cpu name = NULL?");
   66| 		return NULL;
   67| 	}
   68| 
   69| 	CHECK_ALLOCATION(cpu_type_name = strdup(name));
   70| 
   71| 	struct cpu *cpu = (struct cpu *) zeroed_alloc(sizeof(struct cpu));
   72| 
   73| 	CHECK_ALLOCATION(cpu->path = (char *) malloc(strlen(machine->path) + 15));
   74| 	snprintf(cpu->path, strlen(machine->path) + 15,
   75| 	    "%s.cpu[%i]", machine->path, cpu_id);
   76| 
   77| 	cpu->memory_rw  = NULL;
   78| 	cpu->name       = cpu_type_name;
   79| 	cpu->mem        = mem;
   80| 	cpu->machine    = machine;
   81| 	cpu->cpu_id     = cpu_id;
   82| 	cpu->byte_order = EMUL_UNDEFINED_ENDIAN;
   83| 	cpu->running    = 0;
   84| 
   85| 	/*  Create settings, and attach to the machine:  */
   86| 	cpu->settings = settings_new();
   87| 	snprintf(tmpstr, sizeof(tmpstr), "cpu[%i]", cpu_id);
   88| 	settings_add(machine->settings, tmpstr, 1,
   89| 	    SETTINGS_TYPE_SUBSETTINGS, 0, cpu->settings);
   90| 
   91| 	settings_add(cpu->settings, "name", 0, SETTINGS_TYPE_STRING,
   92| 	    SETTINGS_FORMAT_STRING, (void *) &cpu->name);
   93| 	settings_add(cpu->settings, "running", 0, SETTINGS_TYPE_UINT8,
   94| 	    SETTINGS_FORMAT_YESNO, (void *) &cpu->running);
   95| 
   96| 	cpu_create_or_reset_tc(cpu);
   97| 
   98| 	struct cpu_family *fp = first_cpu_family;
   99| 
  100| 	while (fp != NULL) {
  101| 		if (fp->cpu_new != NULL) {
  102| 			if (fp->cpu_new(cpu, mem, machine, cpu_id, cpu_type_name))
  103| 				break;
  104| 		}
  105| 
  106| 		fp = fp->next;
  107| 	}
  108| 
  109| 	if (fp == NULL) {
  110| 		debugmsg(SUBSYS_CPU, "", VERBOSITY_ERROR,
  111| 		    "unknown cpu type '%s'", cpu_type_name);
  112| 		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  113| 		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  114| 		munmap((void *)cpu, sizeof(struct cpu));
  115| 		return NULL;
  116| 	}
  117| 
  118| 	cpu->cpu_family = fp;
  119| 
  120| 	if (cpu->memory_rw == NULL) {
  121| 		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
  122| 		    "memory_rw == NULL");
  123| 		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  124| 		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  125| 		munmap((void *)cpu, sizeof(struct cpu));
  126| 		return NULL;
  127| 	}
  128| 
  129| 	fp->init_tables(cpu);
  130| 
  131| 	if (cpu->byte_order == EMUL_UNDEFINED_ENDIAN) {
  132| 		debugmsg_cpu(cpu, SUBSYS_CPU, "endianness", VERBOSITY_ERROR,
  133| 		    "Internal bug: Endianness not set!");
  134| 		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  135| 		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  136| 		munmap((void *)cpu, sizeof(struct cpu));
  137| 		return NULL;
  138| 	}
```

### `src/core/settings.c` around the row's cited line 223 (HEAD d2a6f233, lines 178-268)

```c
  178| 		*valuep = *((int64_t *) settings->ptr[i]);
  179| 		break;
  180| 	case SETTINGS_TYPE_UINT:
  181| 		*valuep = *((uint *) settings->ptr[i]);
  182| 		break;
  183| 	case SETTINGS_TYPE_UINT8:
  184| 		*valuep = *((uint8_t *) settings->ptr[i]);
  185| 		break;
  186| 	case SETTINGS_TYPE_UINT16:
  187| 		*valuep = *((uint16_t *) settings->ptr[i]);
  188| 		break;
  189| 	case SETTINGS_TYPE_UINT32:
  190| 		*valuep = *((uint32_t *) settings->ptr[i]);
  191| 		break;
  192| 	case SETTINGS_TYPE_UINT64:
  193| 		*valuep = *((uint64_t *) settings->ptr[i]);
  194| 		break;
  195| 	case SETTINGS_TYPE_STRING:
  196| 		/*  Note: Strings cannot be read like this.  */
  197| 		break;
  198| 	default:printf("settings_read(): FATAL ERROR! Unknown storage type"
  199| 		    ": %i\n", settings->storage_type[i]);
  200| 		exit(1);
  201| 	}
  202| 
  203| 	return SETTINGS_OK;
  204| }
  205| 
  206| 
  207| /*
  208|  *  settings_write():
  209|  *
  210|  *  Used internally by settings_access().
  211|  */
  212| static int settings_write(struct settings *settings, int i, uint64_t *valuep)
  213| {
  214| 	if (!settings->writable[i])
  215| 		return SETTINGS_READONLY;
  216| 
  217| 	switch (settings->storage_type[i]) {
  218| 	case SETTINGS_TYPE_INT:
  219| 	case SETTINGS_TYPE_UINT:
  220| 		*((int *) settings->ptr[i]) = *valuep;
  221| 		break;
  222| 	case SETTINGS_TYPE_INT8:
  223| 	case SETTINGS_TYPE_UINT8:
  224| 		*((int8_t *) settings->ptr[i]) = *valuep;
  225| 		break;
  226| 	case SETTINGS_TYPE_INT16:
  227| 	case SETTINGS_TYPE_UINT16:
  228| 		*((int16_t *) settings->ptr[i]) = *valuep;
  229| 		break;
  230| 	case SETTINGS_TYPE_INT32:
  231| 	case SETTINGS_TYPE_UINT32:
  232| 		*((int32_t *) settings->ptr[i]) = *valuep;
  233| 		break;
  234| 	case SETTINGS_TYPE_INT64:
  235| 	case SETTINGS_TYPE_UINT64:
  236| 		*((int64_t *) settings->ptr[i]) = *valuep;
  237| 		break;
  238| 	case SETTINGS_TYPE_STRING:
  239| 		/*  Note: Strings cannot be read like this.  */
  240| 		printf("settings_write(): ERROR! Strings cannot be "
  241| 		    "written like this.\n");
  242| 		break;
  243| 	default:printf("settings_read(): FATAL ERROR! Unknown storage type"
  244| 		    ": %i\n", settings->storage_type[i]);
  245| 		exit(1);
  246| 	}
  247| 
  248| 	return SETTINGS_OK;
  249| }
  250| 
  251| 
  252| /*
  253|  *  settings_debugdump():
  254|  *
  255|  *  Dump settings in a settings object to stdout.
  256|  *  If recurse is non-zero, all subsetting objects are also dumped.
  257|  */
  258| void settings_debugdump(struct settings *settings, const char *prefix,
  259| 	int recurse)
  260| {
  261| 	size_t name_buflen = strlen(prefix) + 100;
  262| 	char *name;
  263| 	int i;
  264| 	uint64_t value = 0;
  265| 
  266| 	CHECK_ALLOCATION(name = (char *) malloc(name_buflen));
  267| 
  268| 	for (i=0; i<settings->n_settings; i++) {
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

End with one line: `FIXDRAFT_CPURUNNINGTYPE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
BUILD FAILED (make rc=2 errors=3 warnings_in_edited=0):
cpu.c:93:51: error: 'SETTINGS_TYPE_BOOL' undeclared (first use in this function); did you mean 'SETTINGS_TYPE_UINT'?
settings.c:183:14: error: 'SETTINGS_TYPE_BOOL' undeclared (first use in this function); did you mean 'SETTINGS_TYPE_UINT'?
settings.c:225:14: error: 'SETTINGS_TYPE_BOOL' undeclared (first use in this function); did you mean 'SETTINGS_TYPE_UINT'?
```

The previous edits:

```json
[
  {
    "file": "src/cpus/cpu.c",
    "old": "\tsettings_add(cpu->settings, \"running\", 0, SETTINGS_TYPE_UINT8,\n\t    SETTINGS_FORMAT_YESNO, (void *) &cpu->running);",
    "new": "\tsettings_add(cpu->settings, \"running\", 0, SETTINGS_TYPE_BOOL,\n\t    SETTINGS_FORMAT_YESNO, (void *) &cpu->running);",
    "why": "Register the bool field with its actual type to prevent out-of-bounds byte values."
  },
  {
    "file": "src/core/settings.c",
    "old": "\tcase SETTINGS_TYPE_UINT8:\n\t\t*valuep = *((uint8_t *) settings->ptr[i]);\n\t\tbreak;",
    "new": "\tcase SETTINGS_TYPE_BOOL:\n\t\t*valuep = *((bool *) settings->ptr[i]);\n\t\tbreak;\n\tcase SETTINGS_TYPE_UINT8:\n\t\t*valuep = *((uint8_t *) settings->ptr[i]);\n\t\tbreak;",
    "why": "Add read support for SETTINGS_TYPE_BOOL."
  },
  {
    "file": "src/core/settings.c",
    "old": "\tcase SETTINGS_TYPE_INT8:\n\tcase SETTINGS_TYPE_UINT8:\n\t\t*((int8_t *) settings->ptr[i]) = *valuep;\n\t\tbreak;",
    "new": "\tcase SETTINGS_TYPE_BOOL:\n\t\t*((bool *) settings->ptr[i]) = (*valuep != 0);\n\t\tbreak;\n\tcase SETTINGS_TYPE_INT8:\n\tcase SETTINGS_TYPE_UINT8:\n\t\t*((int8_t *) settings->ptr[i]) = *valuep;\n\t\tbreak;",
    "why": "Add write support for SETTINGS_TYPE_BOOL, ensuring the value is clamped to a valid 0 or 1."
  }
]
```

### `src/include/settings.h` lines 33-57 (where HEAD defines `SETTINGS_TYPE_UINT`)

```c
   33| #define	GLOBAL_SETTINGS_NAME	"settings"
   34| 
   35| struct settings;
   36| 
   37| /*  Storage types:  */
   38| #define	SETTINGS_TYPE_SUBSETTINGS	1
   39| #define	SETTINGS_TYPE_STRING		2
   40| #define	SETTINGS_TYPE_INT		3
   41| #define	SETTINGS_TYPE_INT8		4
   42| #define	SETTINGS_TYPE_INT16		5
   43| #define	SETTINGS_TYPE_INT32		6
   44| #define	SETTINGS_TYPE_INT64		7
   45| #define	SETTINGS_TYPE_UINT		8
   46| #define	SETTINGS_TYPE_UINT8		9
   47| #define	SETTINGS_TYPE_UINT16		10
   48| #define	SETTINGS_TYPE_UINT32		11
   49| #define	SETTINGS_TYPE_UINT64		12
   50| 
   51| /*  Presentation formats:  */
   52| #define	SETTINGS_FORMAT_DECIMAL		1	/*  -123  */
   53| #define	SETTINGS_FORMAT_HEX8		2	/*  0x12  */
   54| #define	SETTINGS_FORMAT_HEX16		3	/*  0x1234  */
   55| #define	SETTINGS_FORMAT_HEX32		4	/*  0x80000000  */
   56| #define	SETTINGS_FORMAT_HEX64		5	/*  0xffffffff80000000  */
   57| #define	SETTINGS_FORMAT_BOOL		6	/*  true, false  */
```

Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
