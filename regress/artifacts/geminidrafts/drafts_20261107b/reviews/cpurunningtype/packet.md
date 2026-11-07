# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `cpurunningtype` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `cpurunningtype`, state `open`)

**title:** cpus/cpu.c:cpu_new -- `bool running` is registered as SETTINGS_TYPE_UINT8, so a debugger assignment can store a byte other than 0/1 -- HYGIENE (debugger-only UB)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T143 (class HYGIENE; reach C, configuration, debugger, host environment or a non-default build; effort: one-line; report rows: A1-17).  Source URLs: https://github.com/retroprom/gxemul/commit/6f477da8.  Our site at de8c7547: src/cpus/cpu.c:93; src/core/settings.c:223-224.  Portable fix: yes -- port upstream 6f477da8.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu.c:93

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/core/settings.c b/src/core/settings.c
index 3e3a0146..5b3a17b6 100644
--- a/src/core/settings.c
+++ b/src/core/settings.c
@@ -180,6 +180,9 @@ static int settings_read(struct settings *settings, int i, uint64_t *valuep)
 	case SETTINGS_TYPE_UINT:
 		*valuep = *((uint *) settings->ptr[i]);
 		break;
+	case SETTINGS_TYPE_BOOL:
+		*valuep = *((bool *) settings->ptr[i]);
+		break;
 	case SETTINGS_TYPE_UINT8:
 		*valuep = *((uint8_t *) settings->ptr[i]);
 		break;
@@ -219,6 +222,9 @@ static int settings_write(struct settings *settings, int i, uint64_t *valuep)
 	case SETTINGS_TYPE_UINT:
 		*((int *) settings->ptr[i]) = *valuep;
 		break;
+	case SETTINGS_TYPE_BOOL:
+		*((bool *) settings->ptr[i]) = (*valuep != 0);
+		break;
 	case SETTINGS_TYPE_INT8:
 	case SETTINGS_TYPE_UINT8:
 		*((int8_t *) settings->ptr[i]) = *valuep;
diff --git a/src/cpus/cpu.c b/src/cpus/cpu.c
index 2ce78e3b..6d5e9195 100644
--- a/src/cpus/cpu.c
+++ b/src/cpus/cpu.c
@@ -90,7 +90,7 @@ struct cpu *cpu_new(struct memory *mem, struct machine *machine,
 
 	settings_add(cpu->settings, "name", 0, SETTINGS_TYPE_STRING,
 	    SETTINGS_FORMAT_STRING, (void *) &cpu->name);
-	settings_add(cpu->settings, "running", 0, SETTINGS_TYPE_UINT8,
+	settings_add(cpu->settings, "running", 0, SETTINGS_TYPE_BOOL,
 	    SETTINGS_FORMAT_YESNO, (void *) &cpu->running);
 
 	cpu_create_or_reset_tc(cpu);
diff --git a/src/include/settings.h b/src/include/settings.h
index 1dc82994..1551b0e8 100644
--- a/src/include/settings.h
+++ b/src/include/settings.h
@@ -47,6 +47,7 @@ struct settings;
 #define	SETTINGS_TYPE_UINT16		10
 #define	SETTINGS_TYPE_UINT32		11
 #define	SETTINGS_TYPE_UINT64		12
+#define	SETTINGS_TYPE_BOOL		13
 
 /*  Presentation formats:  */
 #define	SETTINGS_FORMAT_DECIMAL		1	/*  -123  */
```

## Every edited function, after the fix

### `src/core/settings.c` -- post-edit lines 160-207 (`+` marks a line the diff added or the point of a deletion)

```c
  160|  static int settings_read(struct settings *settings, int i, uint64_t *valuep)
  161|  {
  162|  	*valuep = 0;
  163|  
  164|  	switch (settings->storage_type[i]) {
  165|  	case SETTINGS_TYPE_INT:
  166|  		*valuep = *((int *) settings->ptr[i]);
  167|  		break;
  168|  	case SETTINGS_TYPE_INT8:
  169|  		*valuep = *((int8_t *) settings->ptr[i]);
  170|  		break;
  171|  	case SETTINGS_TYPE_INT16:
  172|  		*valuep = *((int16_t *) settings->ptr[i]);
  173|  		break;
  174|  	case SETTINGS_TYPE_INT32:
  175|  		*valuep = *((int32_t *) settings->ptr[i]);
  176|  		break;
  177|  	case SETTINGS_TYPE_INT64:
  178|  		*valuep = *((int64_t *) settings->ptr[i]);
  179|  		break;
  180|  	case SETTINGS_TYPE_UINT:
  181|  		*valuep = *((uint *) settings->ptr[i]);
  182|  		break;
  183|+ 	case SETTINGS_TYPE_BOOL:
  184|+ 		*valuep = *((bool *) settings->ptr[i]);
  185|+ 		break;
  186|  	case SETTINGS_TYPE_UINT8:
  187|  		*valuep = *((uint8_t *) settings->ptr[i]);
  188|  		break;
  189|  	case SETTINGS_TYPE_UINT16:
  190|  		*valuep = *((uint16_t *) settings->ptr[i]);
  191|  		break;
  192|  	case SETTINGS_TYPE_UINT32:
  193|  		*valuep = *((uint32_t *) settings->ptr[i]);
  194|  		break;
  195|  	case SETTINGS_TYPE_UINT64:
  196|  		*valuep = *((uint64_t *) settings->ptr[i]);
  197|  		break;
  198|  	case SETTINGS_TYPE_STRING:
  199|  		/*  Note: Strings cannot be read like this.  */
  200|  		break;
  201|  	default:printf("settings_read(): FATAL ERROR! Unknown storage type"
  202|  		    ": %i\n", settings->storage_type[i]);
  203|  		exit(1);
  204|  	}
  205|  
  206|  	return SETTINGS_OK;
  207|  }
```

### `src/core/settings.c` -- post-edit lines 215-255 (`+` marks a line the diff added or the point of a deletion)

```c
  215|  static int settings_write(struct settings *settings, int i, uint64_t *valuep)
  216|  {
  217|  	if (!settings->writable[i])
  218|  		return SETTINGS_READONLY;
  219|  
  220|  	switch (settings->storage_type[i]) {
  221|  	case SETTINGS_TYPE_INT:
  222|  	case SETTINGS_TYPE_UINT:
  223|  		*((int *) settings->ptr[i]) = *valuep;
  224|  		break;
  225|+ 	case SETTINGS_TYPE_BOOL:
  226|+ 		*((bool *) settings->ptr[i]) = (*valuep != 0);
  227|+ 		break;
  228|  	case SETTINGS_TYPE_INT8:
  229|  	case SETTINGS_TYPE_UINT8:
  230|  		*((int8_t *) settings->ptr[i]) = *valuep;
  231|  		break;
  232|  	case SETTINGS_TYPE_INT16:
  233|  	case SETTINGS_TYPE_UINT16:
  234|  		*((int16_t *) settings->ptr[i]) = *valuep;
  235|  		break;
  236|  	case SETTINGS_TYPE_INT32:
  237|  	case SETTINGS_TYPE_UINT32:
  238|  		*((int32_t *) settings->ptr[i]) = *valuep;
  239|  		break;
  240|  	case SETTINGS_TYPE_INT64:
  241|  	case SETTINGS_TYPE_UINT64:
  242|  		*((int64_t *) settings->ptr[i]) = *valuep;
  243|  		break;
  244|  	case SETTINGS_TYPE_STRING:
  245|  		/*  Note: Strings cannot be read like this.  */
  246|  		printf("settings_write(): ERROR! Strings cannot be "
  247|  		    "written like this.\n");
  248|  		break;
  249|  	default:printf("settings_read(): FATAL ERROR! Unknown storage type"
  250|  		    ": %i\n", settings->storage_type[i]);
  251|  		exit(1);
  252|  	}
  253|  
  254|  	return SETTINGS_OK;
  255|  }
```

### `src/cpus/cpu.c` -- post-edit lines 60-152 (`+` marks a line the diff added or the point of a deletion)

```c
   60|  {
   61|  	char *cpu_type_name;
   62|  	char tmpstr[30];
   63|  
   64|  	if (name == NULL) {
   65|  		debugmsg(SUBSYS_CPU, "", VERBOSITY_ERROR, "cpu name = NULL?");
   66|  		return NULL;
   67|  	}
   68|  
   69|  	CHECK_ALLOCATION(cpu_type_name = strdup(name));
   70|  
   71|  	struct cpu *cpu = (struct cpu *) zeroed_alloc(sizeof(struct cpu));
   72|  
   73|  	CHECK_ALLOCATION(cpu->path = (char *) malloc(strlen(machine->path) + 15));
   74|  	snprintf(cpu->path, strlen(machine->path) + 15,
   75|  	    "%s.cpu[%i]", machine->path, cpu_id);
   76|  
   77|  	cpu->memory_rw  = NULL;
   78|  	cpu->name       = cpu_type_name;
   79|  	cpu->mem        = mem;
   80|  	cpu->machine    = machine;
   81|  	cpu->cpu_id     = cpu_id;
   82|  	cpu->byte_order = EMUL_UNDEFINED_ENDIAN;
   83|  	cpu->running    = 0;
   84|  
   85|  	/*  Create settings, and attach to the machine:  */
   86|  	cpu->settings = settings_new();
   87|  	snprintf(tmpstr, sizeof(tmpstr), "cpu[%i]", cpu_id);
   88|  	settings_add(machine->settings, tmpstr, 1,
   89|  	    SETTINGS_TYPE_SUBSETTINGS, 0, cpu->settings);
   90|  
   91|  	settings_add(cpu->settings, "name", 0, SETTINGS_TYPE_STRING,
   92|  	    SETTINGS_FORMAT_STRING, (void *) &cpu->name);
   93|+ 	settings_add(cpu->settings, "running", 0, SETTINGS_TYPE_BOOL,
   94|  	    SETTINGS_FORMAT_YESNO, (void *) &cpu->running);
   95|  
   96|  	cpu_create_or_reset_tc(cpu);
   97|  
   98|  	struct cpu_family *fp = first_cpu_family;
   99|  
  100|  	while (fp != NULL) {
  101|  		if (fp->cpu_new != NULL) {
  102|  			if (fp->cpu_new(cpu, mem, machine, cpu_id, cpu_type_name))
  103|  				break;
  104|  		}
  105|  
  106|  		fp = fp->next;
  107|  	}
  108|  
  109|  	if (fp == NULL) {
  110|  		debugmsg(SUBSYS_CPU, "", VERBOSITY_ERROR,
  111|  		    "unknown cpu type '%s'", cpu_type_name);
  112|  		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  113|  		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  114|  		munmap((void *)cpu, sizeof(struct cpu));
  115|  		return NULL;
  116|  	}
  117|  
  118|  	cpu->cpu_family = fp;
  119|  
  120|  	if (cpu->memory_rw == NULL) {
  121|  		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
  122|  		    "memory_rw == NULL");
  123|  		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  124|  		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  125|  		munmap((void *)cpu, sizeof(struct cpu));
  126|  		return NULL;
  127|  	}
  128|  
  129|  	fp->init_tables(cpu);
  130|  
  131|  	if (cpu->byte_order == EMUL_UNDEFINED_ENDIAN) {
  132|  		debugmsg_cpu(cpu, SUBSYS_CPU, "endianness", VERBOSITY_ERROR,
  133|  		    "Internal bug: Endianness not set!");
  134|  		/*  cpu was allocated with zeroed_alloc() (mmap), so it
  135|  		    must be munmap()ed, not free()d; cf. cpu_destroy().  */
  136|  		munmap((void *)cpu, sizeof(struct cpu));
  137|  		return NULL;
  138|  	}
  139|  	
  140|  	if (cpu->vaddr_mask == 0) {
  141|  		if (cpu->is_32bit)
  142|  			cpu->vaddr_mask = 0x00000000ffffffffULL;
  143|  		else
  144|  			cpu->vaddr_mask = (int64_t)-1;
  145|  
  146|  		debugmsg_cpu(cpu, SUBSYS_CPU, "vaddr_mask", VERBOSITY_DEBUG,
  147|  		    "Warning: vaddr_mask should be set in the CPU family's "
  148|  		    "cpu_new()! Assuming 0x%16llx", (long long)cpu->vaddr_mask);
  149|  	}
  150|  
  151|  	return cpu;
  152|  }
```

### `src/include/settings.h` -- post-edit lines 1-88 (`+` marks a line the diff added or the point of a deletion)

```c
    1|  #ifndef	SETTINGS_H
    2|  #define	SETTINGS_H
    3|  
    4|  /*
    5|   *  Copyright (C) 2006-2010  Anders Gavare.  All rights reserved.
    6|   *
    7|   *  Redistribution and use in source and binary forms, with or without
    8|   *  modification, are permitted provided that the following conditions are met:
    9|   *
   10|   *  1. Redistributions of source code must retain the above copyright
   11|   *     notice, this list of conditions and the following disclaimer.
   12|   *  2. Redistributions in binary form must reproduce the above copyright  
   13|   *     notice, this list of conditions and the following disclaimer in the 
   14|   *     documentation and/or other materials provided with the distribution.
   15|   *  3. The name of the author may not be used to endorse or promote products
   16|   *     derived from this software without specific prior written permission.
   17|   *
   18|   *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   19|   *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   20|   *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   21|   *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   22|   *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   23|   *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   24|   *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   25|   *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   26|   *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   27|   *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   28|   *  SUCH DAMAGE.
   29|   */
   30|  
   31|  #include <inttypes.h>
   32|  
   33|  #define	GLOBAL_SETTINGS_NAME	"settings"
   34|  
   35|  struct settings;
   36|  
   37|  /*  Storage types:  */
   38|  #define	SETTINGS_TYPE_SUBSETTINGS	1
   39|  #define	SETTINGS_TYPE_STRING		2
   40|  #define	SETTINGS_TYPE_INT		3
   41|  #define	SETTINGS_TYPE_INT8		4
   42|  #define	SETTINGS_TYPE_INT16		5
   43|  #define	SETTINGS_TYPE_INT32		6
   44|  #define	SETTINGS_TYPE_INT64		7
   45|  #define	SETTINGS_TYPE_UINT		8
   46|  #define	SETTINGS_TYPE_UINT8		9
   47|  #define	SETTINGS_TYPE_UINT16		10
   48|  #define	SETTINGS_TYPE_UINT32		11
   49|  #define	SETTINGS_TYPE_UINT64		12
   50|+ #define	SETTINGS_TYPE_BOOL		13
   51|  
   52|  /*  Presentation formats:  */
   53|  #define	SETTINGS_FORMAT_DECIMAL		1	/*  -123  */
   54|  #define	SETTINGS_FORMAT_HEX8		2	/*  0x12  */
   55|  #define	SETTINGS_FORMAT_HEX16		3	/*  0x1234  */
   56|  #define	SETTINGS_FORMAT_HEX32		4	/*  0x80000000  */
   57|  #define	SETTINGS_FORMAT_HEX64		5	/*  0xffffffff80000000  */
   58|  #define	SETTINGS_FORMAT_BOOL		6	/*  true, false  */
   59|  #define	SETTINGS_FORMAT_YESNO		7	/*  yes, no  */
   60|  #define	SETTINGS_FORMAT_STRING		8	/*  %s  */
   61|  
   62|  
   63|  /*
   64|   *  settings.c:
   65|   */
   66|  
   67|  struct settings *settings_new(void);
   68|  void settings_destroy(struct settings *settings);
   69|  
   70|  void settings_debugdump(struct settings *settings, const char *prefix,
   71|  	int recurse);
   72|  
   73|  void settings_add(struct settings *settings, const char *name, int writable,
   74|  	int type, int format, void *ptr);
   75|  void settings_remove(struct settings *settings, const char *name);
   76|  void settings_remove_all(struct settings *settings);
   77|  
   78|  int settings_access(struct settings *settings, const char *fullname,
   79|  	int writeflag, uint64_t *valuep);
   80|  
   81|  /*  Result codes from settings_access:  */
   82|  #define	SETTINGS_OK			1
   83|  #define	SETTINGS_NAME_NOT_FOUND		2
   84|  #define	SETTINGS_READONLY		3
   85|  
   86|  
   87|  #endif	/*  SETTINGS_H  */
   88|  
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_CPURUNNINGTYPE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_CPURUNNINGTYPE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
