# GXemul hardened fork -- DRAFT A FIX for one filed issue, `strtoullbase` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `strtoullbase`, state `open`, severity `LOW`)

**title:** src/core/misc.c:175-191 -- mystrtoull() accepts a digit at or above the base (for example 9 in an octal number) and wraps silently on long input -- WRONG-RESULT (host command line and configuration file)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- add base and overflow tests to mystrtoull

## The code at the cited lines

### `src/core/misc.c` around the row's cited line 175 (HEAD 8d9df658, lines 55-295)

```c
   55| 	}
   56| 
   57| 	return r && enable_colorized_output;
   58| }
   59| 
   60| 
   61| void color_prompt()
   62| {
   63| 	if (use_colorized_output())
   64| 		printf("\e[34;1m");
   65| }
   66| 
   67| 
   68| void color_normal()
   69| {
   70| 	if (use_colorized_output())
   71| 		printf("%s", color_normal_ptr());
   72| }
   73| 
   74| void color_error(bool bold)
   75| {
   76| 	if (!use_colorized_output())
   77| 		return;
   78| 
   79| 	if (bold)
   80| 		printf("\e[31;1m");
   81| 	else
   82| 		printf("\e[31m");
   83| }
   84| 
   85| 
   86| void color_debugmsg_subsystem()
   87| {
   88| 	if (use_colorized_output())
   89| 		printf("\e[33m");
   90| }
   91| 
   92| 
   93| void color_debugmsg_name()
   94| {
   95| 	if (use_colorized_output())
   96| 		printf("\e[34;1m");
   97| }
   98| 
   99| 
  100| void color_banner()
  101| {
  102| 	if (use_colorized_output())
  103| 		printf("\e[1m");
  104| }
  105| 
  106| 
  107| void color_pc_indicator()
  108| {
  109| 	if (!use_colorized_output())
  110| 		return;
  111| 
  112| 	printf("\e[31m");
  113| }
  114| 
  115| 
  116| const char* color_symbol_ptr()
  117| {
  118| 	if (use_colorized_output())
  119| 		return "\e[35m";
  120| 	else
  121| 		return "";
  122| }
  123| 
  124| 
  125| const char* color_normal_ptr()
  126| {
  127| 	if (use_colorized_output())
  128| 		return "\e[0m";
  129| 	else
  130| 		return "";
  131| }
  132| 
  133| 
  134| /*
  135|  *  mystrtoull():
  136|  *
  137|  *  This function is used on OSes that don't have strtoull() in libc.
  138|  */
  139| unsigned long long mystrtoull(const char *s, char **endp, int base)
  140| {
  141| 	unsigned long long res = 0;
  142| 	int minus_sign = 0;
  143| 
  144| 	if (s == NULL)
  145| 		return 0;
  146| 
  147| 	/*  TODO: Implement endp?  */
  148| 	if (endp != NULL) {
  149| 		fprintf(stderr, "mystrtoull(): endp isn't implemented\n");
  150| 		exit(1);
  151| 	}
  152| 
  153| 	if (s[0] == '-') {
  154| 		minus_sign = 1;
  155| 		s++;
  156| 	}
  157| 
  158| 	/*  Guess base:  */
  159| 	if (base == 0) {
  160| 		if (s[0] == '0') {
  161| 			/*  Just "0"? :-)  */
  162| 			if (!s[1])
  163| 				return 0;
  164| 			if (s[1] == 'x' || s[1] == 'X') {
  165| 				base = 16;
  166| 				s += 2;
  167| 			} else {
  168| 				base = 8;
  169| 				s ++;
  170| 			}
  171| 		} else if (s[0] >= '1' && s[0] <= '9')
  172| 			base = 10;
  173| 	}
  174| 
  175| 	while (s[0]) {
  176| 		int c = s[0];
  177| 		if (c >= '0' && c <= '9')
  178| 			c -= '0';
  179| 		else if (c >= 'a' && c <= 'f')
  180| 			c = c - 'a' + 10;
  181| 		else if (c >= 'A' && c <= 'F')
  182| 			c = c - 'A' + 10;
  183| 		else
  184| 			break;
  185| 		switch (base) {
  186| 		case 8:	res = (res << 3) | c;
  187| 			break;
  188| 		case 16:res = (res << 4) | c;
  189| 			break;
  190| 		default:res = (res * base) + c;
  191| 		}
  192| 		s++;
  193| 	}
  194| 
  195| 	if (minus_sign)
  196| 		res = (uint64_t) -(int64_t)res;
  197| 	return res;
  198| }
  199| 
  200| 
  201| /*
  202|  *  mymkstemp():
  203|  *
  204|  *  mkstemp() replacement for systems that lack that function. The trailing run
  205|  *  of 'X' characters in the template is filled with random alphanumeric
  206|  *  characters, and the file is created with O_CREAT | O_EXCL so an existing
  207|  *  file is never clobbered (defeating the classic symlink race). On collision
  208|  *  the substitution is retried with fresh characters. Returns an open fd, or
  209|  *  -1 on error (with errno set).
  210|  */
  211| int mymkstemp(char *templ)
  212| {
  213| 	static const char chars[] =
  214| 	    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  215| 	size_t len = strlen(templ);
  216| 	size_t start = len;
  217| 	int attempt;
  218| 	int urandom_fd;
  219| 
  220| 	/*  Locate the trailing run of 'X' characters to substitute.  */
  221| 	while (start > 0 && templ[start - 1] == 'X')
  222| 		start--;
  223| 
  224| 	/*  Draw the random suffix from the kernel CSPRNG so the names are not
  225| 	    predictable (random() may be unseeded). Fall back to random() per
  226| 	    byte only if /dev/urandom cannot be opened/read.  */
  227| 	urandom_fd = open("/dev/urandom", O_RDONLY);
  228| 
  229| 	for (attempt = 0; attempt < 256; attempt++) {
  230| 		size_t i;
  231| 		int h;
  232| 
  233| 		for (i = start; i < len; i++) {
  234| 			unsigned char rb;
  235| 			if (urandom_fd < 0 || read(urandom_fd, &rb, 1) != 1)
  236| 				rb = (unsigned char) random();
  237| 			templ[i] = chars[rb % (sizeof(chars) - 1)];
  238| 		}
  239| 
  240| 		h = open(templ, O_RDWR | O_CREAT | O_EXCL, 0600);
  241| 		if (h >= 0) {
  242| 			if (urandom_fd >= 0)
  243| 				close(urandom_fd);
  244| 			return h;
  245| 		}
  246| 		if (errno != EEXIST) {
  247| 			if (urandom_fd >= 0)
  248| 				close(urandom_fd);
  249| 			return -1;
  250| 		}
  251| 	}
  252| 
  253| 	if (urandom_fd >= 0)
  254| 		close(urandom_fd);
  255| 	return -1;
  256| }
  257| 
  258| 
  259| #ifdef USE_STRLCPY_REPLACEMENTS
  260| /*
  261|  *  mystrlcpy():
  262|  *
  263|  *  strlcpy() replacement for systems that lack that function. Copies at most
  264|  *  size-1 bytes from src to dst and always NUL-terminates dst (when size > 0).
  265|  *  Returns strlen(src), i.e. the length of the string it tried to create, so
  266|  *  that truncation can be detected (retval >= size). Uses only strlen()/memcpy()
  267|  *  so it has no dependency on other possibly-missing libc functions.
  268|  */
  269| size_t mystrlcpy(char *dst, const char *src, size_t size)
  270| {
  271| 	size_t src_len = strlen(src);
  272| 
  273| 	if (size != 0) {
  274| 		size_t copy_len = (src_len >= size) ? size - 1 : src_len;
  275| 		memcpy(dst, src, copy_len);
  276| 		dst[copy_len] = '\0';
  277| 	}
  278| 
  279| 	return src_len;
  280| }
  281| 
  282| 
  283| /*
  284|  *  mystrlcat():
  285|  *
  286|  *  strlcat() replacement for systems that lack that function. Appends src to
  287|  *  dst, writing at most size-1 bytes total and always NUL-terminating (when
  288|  *  there is room). Returns the length of the string it tried to create, i.e.
  289|  *  the initial length of dst plus strlen(src). The length of dst is measured
  290|  *  with a bounded scan so that an unterminated buffer is never over-read.
  291|  */
  292| size_t mystrlcat(char *dst, const char *src, size_t size)
  293| {
  294| 	size_t dst_len = 0;
  295| 	size_t src_len = strlen(src);
```

### `src/devices/device.c` around the row's cited line 319 (HEAD 8d9df658, lines 199-439)

```c
  199| 	return NULL;
  200| }
  201| 
  202| 
  203| /*
  204|  *  device_unregister():
  205|  *
  206|  *  Unregisters a device.
  207|  *
  208|  *  Return value is 1 if a device was unregistered, 0 otherwise.
  209|  */
  210| int device_unregister(char *name)
  211| {
  212| 	ssize_t i;
  213| 	struct device_entry *p = device_lookup(name);
  214| 
  215| 	if (p == NULL) {
  216| 		fatal("device_unregister(): no such device (\"%s\")\n", name);
  217| 		return 0;
  218| 	}
  219| 
  220| 	i = (size_t)p - (size_t)device_entries;
  221| 	i /= sizeof(struct device_entry);
  222| 
  223| 	free(device_entries[i].name);
  224| 	device_entries[i].name = NULL;
  225| 
  226| 	if (i == n_device_entries-1) {
  227| 		/*  Do nothing if we're removing the last array element.  */
  228| 	} else {
  229| 		/*  Remove array element i by copying the last element
  230| 		    to i's position:  */
  231| 		device_entries[i] = device_entries[n_device_entries-1];
  232| 
  233| 		/*  The array is not sorted anymore:  */
  234| 		device_entries_sorted = 0;
  235| 	}
  236| 
  237| 	n_device_entries --;
  238| 
  239| 	/*  TODO: realloc?  */
  240| 	return 1;
  241| }
  242| 
  243| 
  244| /*
  245|  *  device_add():
  246|  *
  247|  *  Add a device to a machine. For example: "kn210 addr=0x12340000" adds a
  248|  *  device called "kn210" at a specific address.
  249|  *
  250|  *  TODO: This function is quite ugly, and should be cleaned up.
  251|  */
  252| void *device_add(struct machine *machine, const char *name_and_params)
  253| {
  254| 	struct device_entry *p;
  255| 	struct devinit devinit;
  256| 	const char *s2;
  257| 	const char *s3;
  258| 	size_t len, interrupt_path_len = strlen(machine->path) + 100;
  259| 	int quoted;
  260| 
  261| 	memset(&devinit, 0, sizeof(struct devinit));
  262| 	devinit.machine = machine;
  263| 
  264| 	/*  Default values:  */
  265| 	devinit.addr_mult = 1;
  266| 	devinit.in_use = 1;
  267| 
  268| 	/*  Get the device name first:  */
  269| 	s2 = name_and_params;
  270| 	while (s2[0] != ',' && s2[0] != ' ' && s2[0] != '\0')
  271| 		s2 ++;
  272| 
  273| 	len = (size_t)s2 - (size_t)name_and_params;
  274| 	CHECK_ALLOCATION(devinit.name = (char *) malloc(len + 1));
  275| 	memcpy(devinit.name, name_and_params, len);
  276| 	devinit.name[len] = '\0';
  277| 
  278| 	/*  Allocate space for the default interrupt name:  */
  279| 	CHECK_ALLOCATION(devinit.interrupt_path = (char *)
  280| 	    malloc(interrupt_path_len + 1));
  281| 	snprintf(devinit.interrupt_path, interrupt_path_len,
  282| 	    "%s.cpu[%i]", machine->path, machine->bootstrap_cpu);
  283| 
  284| 	p = device_lookup(devinit.name);
  285| 	if (p == NULL) {
  286| 		fatal("no such device (\"%s\")\n", devinit.name);
  287| 		if (device_exit_on_error)
  288| 			exit(1);
  289| 		else
  290| 			goto return_fail;
  291| 	}
  292| 
  293| 	/*  Get params from name_and_params:  */
  294| 	while (*s2 != '\0') {
  295| 		/*  Skip spaces, commas, and semicolons:  */
  296| 		while (*s2 == ' ' || *s2 == ',' || *s2 == ';')
  297| 			s2 ++;
  298| 
  299| 		if (*s2 == '\0')
  300| 			break;
  301| 
  302| 		/*  s2 now points to the next param. eg "addr=1234"  */
  303| 
  304| 		/*  Get a word (until there is a '=' sign):  */
  305| 		s3 = s2;
  306| 		while (*s3 != '=' && *s3 != '\0')
  307| 			s3 ++;
  308| 		if (s3 == s2) {
  309| 			fatal("weird param: %s\n", s2);
  310| 			if (device_exit_on_error)
  311| 				exit(1);
  312| 			else
  313| 				goto return_fail;
  314| 		}
  315| 		s3 ++;
  316| 		/*  s3 now points to the parameter value ("1234")  */
  317| 
  318| 		if (strncmp(s2, "addr=", 5) == 0) {
  319| 			devinit.addr = mystrtoull(s3, NULL, 0);
  320| 		} else if (strncmp(s2, "addr2=", 6) == 0) {
  321| 			devinit.addr2 = mystrtoull(s3, NULL, 0);
  322| 		} else if (strncmp(s2, "len=", 4) == 0) {
  323| 			devinit.len = mystrtoull(s3, NULL, 0);
  324| 		} else if (strncmp(s2, "addr_mult=", 10) == 0) {
  325| 			devinit.addr_mult = mystrtoull(s3, NULL, 0);
  326| 		} else if (strncmp(s2, "pci_little_endian=", 18) == 0) {
  327| 			devinit.pci_little_endian = mystrtoull(s3, NULL, 0);
  328| 			switch (devinit.pci_little_endian) {
  329| 			case 0:	break;
  330| 			case 1:	devinit.pci_little_endian =
  331| 				    MEM_PCI_LITTLE_ENDIAN;
  332| 				break;
  333| 			default:fatal("Bad pci_little_endian value.\n");
  334| 				exit(1);
  335| 			}
  336| 		} else if (strncmp(s2, "irq=", 4) == 0) {
  337| 			snprintf(devinit.interrupt_path, interrupt_path_len, "%s", s3);
  338| 			if (strchr(devinit.interrupt_path, ' ') != NULL)
  339| 				*strchr(devinit.interrupt_path, ' ') = '\0';
  340| 		} else if (strncmp(s2, "in_use=", 7) == 0) {
  341| 			devinit.in_use = mystrtoull(s3, NULL, 0);
  342| 		} else if (strncmp(s2, "name2=", 6) == 0) {
  343| 			const char *h = s2 + 6;
  344| 			size_t len2 = 0;
  345| 			quoted = 0;
  346| 			while (*h) {
  347| 				if (*h == '\'')
  348| 					quoted = !quoted;
  349| 				h++, len2++;
  350| 				if (!quoted && *h == ' ')
  351| 					break;
  352| 			}
  353| 			CHECK_ALLOCATION(devinit.name2 = (char *) malloc(len2 + 1));
  354| 			h = s2 + 6;
  355| 			if (*h == '\'')
  356| 				len2 -= 2, h++;
  357| 			snprintf(devinit.name2, len2 + 1, "%s", h);
  358| 		} else {
  359| 			fatal("unknown param: %s\n", s2);
  360| 			if (device_exit_on_error)
  361| 				exit(1);
  362| 			else
  363| 				goto return_fail;
  364| 		}
  365| 
  366| 		/*  skip to the next param:  */
  367| 		s2 = s3;
  368| 		quoted = 0;
  369| 		while (*s2 != '\0' && (*s2 != ' ' || quoted) &&
  370| 		    *s2 != ',' && *s2 != ';') {
  371| 			if (*s2 == '\'')
  372| 				quoted = !quoted;
  373| 			s2 ++;
  374| 		}
  375| 	}
  376| 
  377| 
  378| 	/*
  379| 	 *  Call the init function for this device:
  380| 	 */
  381| 
  382| 	devinit.return_ptr = NULL;
  383| 
  384| 	if (!p->initf(&devinit)) {
  385| 		fatal("error adding device (\"%s\")\n", name_and_params);
  386| 		if (device_exit_on_error)
  387| 			exit(1);
  388| 		else
  389| 			goto return_fail;
  390| 	}
  391| 
  392| 	free(devinit.interrupt_path);
  393| 	free(devinit.name);
  394| 	return devinit.return_ptr;
  395| 
  396| return_fail:
  397| 	free(devinit.name);
  398| 	return NULL;
  399| }
  400| 
  401| 
  402| /*
  403|  *  device_dumplist():
  404|  *
  405|  *  Dump a list of all registered devices.  (If the list is not sorted when
  406|  *  this function is called, it is implicitly sorted.)
  407|  */
  408| void device_dumplist(void)
  409| {
  410| 	int i;
  411| 
  412| 	if (!device_entries_sorted)
  413| 		sort_entries();
  414| 
  415| 	for (i=0; i<n_device_entries; i++) {
  416| 		debug("  %s", device_entries[i].name);
  417| 
  418| 		/*  TODO: flags?  */
  419| 
  420| 		debug("\n");
  421| 	}
  422| }
  423| 
  424| 
  425| /*
  426|  *  device_set_exit_on_error():
  427|  *
  428|  *  This function selects the behaviour of the emulator when a device is not
  429|  *  found. During startup, it is nicest to abort the whole emulator session,
  430|  *  but if a device addition is attempted from within the debugger, then it is
  431|  *  nicer to just print a warning and continue.
  432|  */
  433| void device_set_exit_on_error(int exit_on_error)
  434| {
  435| 	device_exit_on_error = exit_on_error;
  436| }
  437| 
  438| 
  439| /*
```

### `src/core/emul_parse.c` around the row's cited line 532 (HEAD 8d9df658, lines 412-652)

```c
  412| 
  413| 		*parsestate = PARSESTATE_EMUL;
  414| 		return;
  415| 	}
  416| 
  417| 	WORD("tapdev", cur_net_tapdev);
  418| 	WORD("ipv4net", cur_net_ipv4net);
  419| 	WORD("ipv4len", cur_net_ipv4len);
  420| 	WORD("local_port", cur_net_local_port);
  421| 
  422| 	if (strcmp(word, "add_remote") == 0) {
  423| 		read_one_word(f, word, maxbuflen,
  424| 		    line, EXPECT_LEFT_PARENTHESIS);
  425| 		if (cur_net_n_remote >= MAX_N_REMOTE) {
  426| 			fprintf(stderr, "too many remote networks\n");
  427| 			exit(1);
  428| 		}
  429| 
  430| 		CHECK_ALLOCATION(cur_net_remote[cur_net_n_remote] =
  431| 		    (char *) malloc(MAX_REMOTE_LEN));
  432| 		read_one_word(f, cur_net_remote[cur_net_n_remote],
  433| 		    MAX_REMOTE_LEN, line, EXPECT_WORD);
  434| 		cur_net_n_remote ++;
  435| 		read_one_word(f, word, maxbuflen, line,
  436| 		    EXPECT_RIGHT_PARENTHESIS);
  437| 		return;
  438| 	}
  439| 
  440| 	fatal("line %i: not expecting '%s' in a 'net' section\n", *line, word);
  441| 	exit(1);
  442| }
  443| 
  444| 
  445| /*
  446|  *  parse__machine():
  447|  */
  448| static void parse__machine(struct emul *e, FILE *f, int *in_emul, int *line,
  449| 	int *parsestate, char *word, size_t maxbuflen)
  450| {
  451| 	int r, i;
  452| 
  453| 	if (word[0] == ')') {
  454| 		/*  Finished with the 'machine' section.  */
  455| 		struct machine *m;
  456| 
  457| 		if (!cur_machine_name[0])
  458| 			strlcpy(cur_machine_name, "no_name",
  459| 			    sizeof(cur_machine_name));
  460| 
  461| 		m = emul_add_machine(e, cur_machine_name);
  462| 
  463| 		r = machine_name_to_type(cur_machine_type, cur_machine_subtype,
  464| 		    &m->machine_type, &m->machine_subtype);
  465| 		if (!r)
  466| 			exit(1);
  467| 
  468| 		if (cur_machine_cpu[0])
  469| 			CHECK_ALLOCATION(m->cpu_name = strdup(cur_machine_cpu));
  470| 
  471| 		if (!cur_machine_use_x11[0])
  472| 			strlcpy(cur_machine_use_x11, "no",
  473| 			    sizeof(cur_machine_use_x11));
  474| 		m->x11_md.in_use = parse_on_off(cur_machine_use_x11);
  475| 
  476| 		if (!cur_machine_prom_emulation[0])
  477| 			strlcpy(cur_machine_prom_emulation, "yes",
  478| 			    sizeof(cur_machine_prom_emulation));
  479| 		m->prom_emulation = parse_on_off(cur_machine_prom_emulation);
  480| 
  481| 		if (!cur_machine_random_mem[0])
  482| 			strlcpy(cur_machine_random_mem, "no",
  483| 			    sizeof(cur_machine_random_mem));
  484| 		m->random_mem_contents =
  485| 		    parse_on_off(cur_machine_random_mem);
  486| 
  487| 		if (!cur_machine_random_cpu[0])
  488| 			strlcpy(cur_machine_random_cpu, "no",
  489| 			    sizeof(cur_machine_random_cpu));
  490| 		m->use_random_bootstrap_cpu =
  491| 		    parse_on_off(cur_machine_random_cpu);
  492| 
  493| 		m->byte_order_override = NO_BYTE_ORDER_OVERRIDE;
  494| 		if (cur_machine_byte_order[0]) {
  495| 			if (strncasecmp(cur_machine_byte_order, "big", 3) == 0)
  496| 				m->byte_order_override = EMUL_BIG_ENDIAN;
  497| 			else if (strncasecmp(cur_machine_byte_order, "little",
  498| 			    6) == 0)
  499| 				m->byte_order_override = EMUL_LITTLE_ENDIAN;
  500| 			else {
  501| 				fatal("Byte order must be big-endian or"
  502| 				    " little-endian\n");
  503| 				exit(1);
  504| 			}
  505| 		}
  506| 
  507| 		if (!cur_machine_force_netboot[0])
  508| 			strlcpy(cur_machine_force_netboot, "no",
  509| 			    sizeof(cur_machine_force_netboot));
  510| 		m->force_netboot = parse_on_off(cur_machine_force_netboot);
  511| 
  512| 		if (!cur_machine_start_paused[0])
  513| 			strlcpy(cur_machine_start_paused, "no",
  514| 			    sizeof(cur_machine_start_paused));
  515| 		m->start_paused = parse_on_off(cur_machine_start_paused) ? true : false;
  516| 
  517| 		/*  NOTE: Default nr of CPUs is 0:  */
  518| 		if (!cur_machine_ncpus[0])
  519| 			strlcpy(cur_machine_ncpus, "0",
  520| 			    sizeof(cur_machine_ncpus));
  521| 		m->ncpus = atoi(cur_machine_ncpus);
  522| 
  523| 		if (cur_machine_n_gfx_cards[0])
  524| 			m->n_gfx_cards = atoi(cur_machine_n_gfx_cards);
  525| 
  526| 		if (cur_machine_serial_nr[0]) {
  527| 			m->serial_nr = atoi(cur_machine_serial_nr);
  528| 			e->next_serial_nr = m->serial_nr+1;
  529| 		}
  530| 
  531| 		if (cur_machine_emulated_hz[0]) {
  532| 			m->emulated_hz = mystrtoull(cur_machine_emulated_hz,
  533| 			    NULL, 0);
  534| 		}
  535| 
  536| 		/*  NOTE: Default nr of CPUs is 0:  */
  537| 		if (!cur_machine_memory[0])
  538| 			strlcpy(cur_machine_memory, "0",
  539| 			    sizeof(cur_machine_memory));
  540| 		m->physical_ram_in_mb = atoi(cur_machine_memory);
  541| 
  542| 		if (!cur_machine_x11_scaledown[0])
  543| 			m->x11_md.scaledown = 1;
  544| 		else {
  545| 			m->x11_md.scaledown = atoi(cur_machine_x11_scaledown);
  546| 			if (m->x11_md.scaledown < 0) {
  547| 				m->x11_md.scaleup = 0 - m->x11_md.scaledown;
  548| 				m->x11_md.scaledown = 1;
  549| 			}
  550| 			if (m->x11_md.scaledown < 1) {
  551| 				fprintf(stderr, "Invalid scaledown value"
  552| 				    " (%i)\n", m->x11_md.scaledown);
  553| 				exit(1);
  554| 			}
  555| 		}
  556| 
  557| 		for (i=0; i<cur_machine_n_disk; i++) {
  558| 			if (diskimage_add(m, cur_machine_disk[i]) < 0) {
  559| 				debugmsg(SUBSYS_EMUL, "", VERBOSITY_ERROR,
  560| 				    "TODO");
  561| 				exit(1);
  562| 			}
  563| 
  564| 			free(cur_machine_disk[i]);
  565| 			cur_machine_disk[i] = NULL;
  566| 		}
  567| 
  568| 		m->boot_kernel_filename = strdup(cur_machine_bootname);
  569| 
  570| 		// HACK: This allows bootarg("") to be treated as
  571| 		// something that is explicitly set. Needed by e.g. Sprite.
  572| 		if (cur_machine_bootarg[0] != '\b')
  573| 			m->boot_string_argument = strdup(cur_machine_bootarg);
  574| 
  575| 		for (i=0; i<cur_machine_n_x11_disp; i++) {
  576| 			m->x11_md.n_display_names ++;
  577| 			CHECK_ALLOCATION(m->x11_md.display_names = (char **) realloc(
  578| 			    m->x11_md.display_names, m->x11_md.n_display_names
  579| 			    * sizeof(char *)));
  580| 			CHECK_ALLOCATION(m->x11_md.display_names[
  581| 			    m->x11_md.n_display_names-1] =
  582| 			    strdup(cur_machine_x11_disp[i]));
  583| 			free(cur_machine_x11_disp[i]);
  584| 			cur_machine_x11_disp[i] = NULL;
  585| 		}
  586| 
  587| 		emul_machine_setup(m,
  588| 		    cur_machine_n_load, cur_machine_load,
  589| 		    cur_machine_n_device, cur_machine_device);
  590| 
  591| 		for (i=0; i<cur_machine_n_device; i++) {
  592| 			free(cur_machine_device[i]);
  593| 			cur_machine_device[i] = NULL;
  594| 		}
  595| 
  596| 		for (i=0; i<cur_machine_n_load; i++) {
  597| 			free(cur_machine_load[i]);
  598| 			cur_machine_load[i] = NULL;
  599| 		}
  600| 
  601| 		*parsestate = PARSESTATE_EMUL;
  602| 		return;
  603| 	}
  604| 
  605| 	WORD("name", cur_machine_name);
  606| 	WORD("cpu", cur_machine_cpu);
  607| 	WORD("type", cur_machine_type);
  608| 	WORD("subtype", cur_machine_subtype);
  609| 	WORD("bootname", cur_machine_bootname);
  610| 	WORD("bootarg", cur_machine_bootarg);
  611| 	WORD("prom_emulation", cur_machine_prom_emulation);
  612| 	WORD("use_x11", cur_machine_use_x11);
  613| 	WORD("x11_scaledown", cur_machine_x11_scaledown);
  614| 	WORD("byte_order", cur_machine_byte_order);
  615| 	WORD("random_mem_contents", cur_machine_random_mem);
  616| 	WORD("use_random_bootstrap_cpu", cur_machine_random_cpu);
  617| 	WORD("force_netboot", cur_machine_force_netboot);
  618| 	WORD("ncpus", cur_machine_ncpus);
  619| 	WORD("serial_nr", cur_machine_serial_nr);
  620| 	WORD("n_gfx_cards", cur_machine_n_gfx_cards);
  621| 	WORD("emulated_hz", cur_machine_emulated_hz);
  622| 	WORD("memory", cur_machine_memory);
  623| 	WORD("start_paused", cur_machine_start_paused);
  624| 
  625| 	if (strcmp(word, "load") == 0) {
  626| 		read_one_word(f, word, maxbuflen,
  627| 		    line, EXPECT_LEFT_PARENTHESIS);
  628| 		if (cur_machine_n_load >= MAX_N_LOAD) {
  629| 			fprintf(stderr, "too many loads\n");
  630| 			exit(1);
  631| 		}
  632| 		CHECK_ALLOCATION(cur_machine_load[cur_machine_n_load] =
  633| 		    (char*) malloc(MAX_LOAD_LEN));
  634| 		read_one_word(f, cur_machine_load[cur_machine_n_load],
  635| 		    MAX_LOAD_LEN, line, EXPECT_WORD);
  636| 		cur_machine_n_load ++;
  637| 		read_one_word(f, word, maxbuflen,
  638| 		    line, EXPECT_RIGHT_PARENTHESIS);
  639| 		return;
  640| 	}
  641| 
  642| 	if (strcmp(word, "disk") == 0) {
  643| 		read_one_word(f, word, maxbuflen,
  644| 		    line, EXPECT_LEFT_PARENTHESIS);
  645| 		if (cur_machine_n_disk >= MAX_N_DISK) {
  646| 			fprintf(stderr, "too many disks\n");
  647| 			exit(1);
  648| 		}
  649| 		CHECK_ALLOCATION(cur_machine_disk[cur_machine_n_disk] =
  650| 		    (char*) malloc(MAX_DISK_LEN));
  651| 		read_one_word(f, cur_machine_disk[cur_machine_n_disk],
  652| 		    MAX_DISK_LEN, line, EXPECT_WORD);
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

End with one line: `FIXDRAFT_STRTOULLBASE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
