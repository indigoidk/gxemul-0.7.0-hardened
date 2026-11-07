# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `devstrnamequote` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `devstrnamequote`, state `open`)

**title:** src/devices/device.c:342-357 -- a name2= value that is a lone quote makes len2 - 2 wrap to SIZE_MAX, so snprintf() is given size 0 and the new name buffer is left unterminated -- WRAP (host device strings only)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/device.c:355-356`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/device.c b/src/devices/device.c
index da0e78dd..e4f0ba37 100644
--- a/src/devices/device.c
+++ b/src/devices/device.c
@@ -352,8 +352,10 @@ void *device_add(struct machine *machine, const char *name_and_params)
 			}
 			CHECK_ALLOCATION(devinit.name2 = (char *) malloc(len2 + 1));
 			h = s2 + 6;
-			if (*h == '\'')
-				len2 -= 2, h++;
+			if (*h == '\'') {
+				len2 = len2 >= 2 ? len2 - 2 : 0;
+				h++;
+			}
 			snprintf(devinit.name2, len2 + 1, "%s", h);
 		} else {
 			fatal("unknown param: %s\n", s2);
```

## Every edited function, after the fix

### `src/devices/device.c` -- post-edit lines 252-401 (`+` marks a line the diff added or the point of a deletion)

```c
  252|  void *device_add(struct machine *machine, const char *name_and_params)
  253|  {
  254|  	struct device_entry *p;
  255|  	struct devinit devinit;
  256|  	const char *s2;
  257|  	const char *s3;
  258|  	size_t len, interrupt_path_len = strlen(machine->path) + 100;
  259|  	int quoted;
  260|  
  261|  	memset(&devinit, 0, sizeof(struct devinit));
  262|  	devinit.machine = machine;
  263|  
  264|  	/*  Default values:  */
  265|  	devinit.addr_mult = 1;
  266|  	devinit.in_use = 1;
  267|  
  268|  	/*  Get the device name first:  */
  269|  	s2 = name_and_params;
  270|  	while (s2[0] != ',' && s2[0] != ' ' && s2[0] != '\0')
  271|  		s2 ++;
  272|  
  273|  	len = (size_t)s2 - (size_t)name_and_params;
  274|  	CHECK_ALLOCATION(devinit.name = (char *) malloc(len + 1));
  275|  	memcpy(devinit.name, name_and_params, len);
  276|  	devinit.name[len] = '\0';
  277|  
  278|  	/*  Allocate space for the default interrupt name:  */
  279|  	CHECK_ALLOCATION(devinit.interrupt_path = (char *)
  280|  	    malloc(interrupt_path_len + 1));
  281|  	snprintf(devinit.interrupt_path, interrupt_path_len,
  282|  	    "%s.cpu[%i]", machine->path, machine->bootstrap_cpu);
  283|  
  284|  	p = device_lookup(devinit.name);
  285|  	if (p == NULL) {
  286|  		fatal("no such device (\"%s\")\n", devinit.name);
  287|  		if (device_exit_on_error)
  288|  			exit(1);
  289|  		else
  290|  			goto return_fail;
  291|  	}
  292|  
  293|  	/*  Get params from name_and_params:  */
  294|  	while (*s2 != '\0') {
  295|  		/*  Skip spaces, commas, and semicolons:  */
  296|  		while (*s2 == ' ' || *s2 == ',' || *s2 == ';')
  297|  			s2 ++;
  298|  
  299|  		if (*s2 == '\0')
  300|  			break;
  301|  
  302|  		/*  s2 now points to the next param. eg "addr=1234"  */
  303|  
  304|  		/*  Get a word (until there is a '=' sign):  */
  305|  		s3 = s2;
  306|  		while (*s3 != '=' && *s3 != '\0')
  307|  			s3 ++;
  308|  		if (s3 == s2) {
  309|  			fatal("weird param: %s\n", s2);
  310|  			if (device_exit_on_error)
  311|  				exit(1);
  312|  			else
  313|  				goto return_fail;
  314|  		}
  315|  		s3 ++;
  316|  		/*  s3 now points to the parameter value ("1234")  */
  317|  
  318|  		if (strncmp(s2, "addr=", 5) == 0) {
  319|  			devinit.addr = mystrtoull(s3, NULL, 0);
  320|  		} else if (strncmp(s2, "addr2=", 6) == 0) {
  321|  			devinit.addr2 = mystrtoull(s3, NULL, 0);
  322|  		} else if (strncmp(s2, "len=", 4) == 0) {
  323|  			devinit.len = mystrtoull(s3, NULL, 0);
  324|  		} else if (strncmp(s2, "addr_mult=", 10) == 0) {
  325|  			devinit.addr_mult = mystrtoull(s3, NULL, 0);
  326|  		} else if (strncmp(s2, "pci_little_endian=", 18) == 0) {
  327|  			devinit.pci_little_endian = mystrtoull(s3, NULL, 0);
  328|  			switch (devinit.pci_little_endian) {
  329|  			case 0:	break;
  330|  			case 1:	devinit.pci_little_endian =
  331|  				    MEM_PCI_LITTLE_ENDIAN;
  332|  				break;
  333|  			default:fatal("Bad pci_little_endian value.\n");
  334|  				exit(1);
  335|  			}
  336|  		} else if (strncmp(s2, "irq=", 4) == 0) {
  337|  			snprintf(devinit.interrupt_path, interrupt_path_len, "%s", s3);
  338|  			if (strchr(devinit.interrupt_path, ' ') != NULL)
  339|  				*strchr(devinit.interrupt_path, ' ') = '\0';
  340|  		} else if (strncmp(s2, "in_use=", 7) == 0) {
  341|  			devinit.in_use = mystrtoull(s3, NULL, 0);
  342|  		} else if (strncmp(s2, "name2=", 6) == 0) {
  343|  			const char *h = s2 + 6;
  344|  			size_t len2 = 0;
  345|  			quoted = 0;
  346|  			while (*h) {
  347|  				if (*h == '\'')
  348|  					quoted = !quoted;
  349|  				h++, len2++;
  350|  				if (!quoted && *h == ' ')
  351|  					break;
  352|  			}
  353|  			CHECK_ALLOCATION(devinit.name2 = (char *) malloc(len2 + 1));
  354|  			h = s2 + 6;
  355|+ 			if (*h == '\'') {
  356|+ 				len2 = len2 >= 2 ? len2 - 2 : 0;
  357|+ 				h++;
  358|+ 			}
  359|  			snprintf(devinit.name2, len2 + 1, "%s", h);
  360|  		} else {
  361|  			fatal("unknown param: %s\n", s2);
  362|  			if (device_exit_on_error)
  363|  				exit(1);
  364|  			else
  365|  				goto return_fail;
  366|  		}
  367|  
  368|  		/*  skip to the next param:  */
  369|  		s2 = s3;
  370|  		quoted = 0;
  371|  		while (*s2 != '\0' && (*s2 != ' ' || quoted) &&
  372|  		    *s2 != ',' && *s2 != ';') {
  373|  			if (*s2 == '\'')
  374|  				quoted = !quoted;
  375|  			s2 ++;
  376|  		}
  377|  	}
  378|  
  379|  
  380|  	/*
  381|  	 *  Call the init function for this device:
  382|  	 */
  383|  
  384|  	devinit.return_ptr = NULL;
  385|  
  386|  	if (!p->initf(&devinit)) {
  387|  		fatal("error adding device (\"%s\")\n", name_and_params);
  388|  		if (device_exit_on_error)
  389|  			exit(1);
  390|  		else
  391|  			goto return_fail;
  392|  	}
  393|  
  394|  	free(devinit.interrupt_path);
  395|  	free(devinit.name);
  396|  	return devinit.return_ptr;
  397|  
  398|  return_fail:
  399|  	free(devinit.name);
  400|  	return NULL;
  401|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_DEVSTRNAMEQUOTE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_DEVSTRNAMEQUOTE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
