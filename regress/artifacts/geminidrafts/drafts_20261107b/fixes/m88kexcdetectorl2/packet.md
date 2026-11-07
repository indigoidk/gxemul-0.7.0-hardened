# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kexcdetectorl2` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `m88kexcdetectorl2`, state `open`, severity `low`)

**title:** m88k_exc_probe.py: MEASURED clean sweep -- deleting `implemented = true' at DATA_ACCESS or RESET scores 59/59 with ZERO row diffs.  The COVERAGE GAP is measured; whether it grades as an L2 floor breach or clause-(e) debt is a RULE QUESTION for the 2026-09-09 adjudication

**state_note (head):**

FILED 2026-09-07 from the RETROSPECTIVE pass 2 on `79cd12e' -- the receipt that round never filed, which
`precommit_check.sh' section F refused the next commit over.  **This is the pass's one actionable finding.**

**THE PREDICTION, from the grok seat, verbatim:** *"The `#502` detector, asked of the shipped composite, has
one clause-(d) mutant I predict sweeps **59/59**: `implemented = true` -> `implemented =
(cpu->machine->ncpus < 2)' on the seven arms.  I could not build it (read-only seat; gates forbidden).  If
that score is real it is **L2 of the detector**, not of `cpu_m88k.c`."*

**IT IS THE CANONICAL CLAUSE-(d) SHAPE**: the guard is kept and its repair is CONDITIONED on a field the
guarded body reads -- `if (X)` -> `if (X && Y)` on the dominating predicate.  The floor says a clause-(d)
mutant that sweeps a detector clean is an **L2 breach, repaired in-round however late it is found**.

*** STATUS: PREDICTED, NOT MEASURED.  That distinction is the whole disposition. ***  The floor's L2 rule
fires on a MEASURED false pass; a prediction is a candidate.  grok said plainly it could not build the mutant
-- read-only seat, gates forbidden -- and did NOT dress the prediction as a score.  Recording it as owed rather
than acting on it is the honest reading, and recording it at all is what stops it becoming an unread review.

**WHY IT IS CREDIBLE ENOUGH TO MEASURE:** the same seat, in the same answer, correctly settled two other
premises by re-derivation -- that `machine->ncpus` has three assignment sites all preceding any device (so
`#503`'s DEVINIT snapshot is stable, which is what minimax had named as the settling fact and could not check
from the packet), and that `#502` delivers all seven classes at BOTH sites, i.e. it is NOT the `#499`
one-cell-repair shape that glm's arithmetic had suggested.  A seat that got two checkable things right in the
same answer has earned the build.

**TO MEASURE IT:** the mutant is one edit repeated on seven arms, scored against the shipped
`regress/m88k_exc_probe.py` (59 rows).  This is what the **agy measurement reserve exists for** -- it is the
only compile-and-measure seat not behind the Agent-tool transport, and Opus 5 / Fable 5 are held for the
2026-09-09 adjudication.  agy has no sandbox, so the brief must say: COPY the tree, build the COPY, never
write to GXEMUL-SEC, `rm src/cpus/*.o' first, and check `[ binary -nt source ]' because MAKE_RC has been
observed reporting 0 on a failed build.

**IF IT SWEEPS 59/59 it is L2 of the DETECTOR** -- `m88k_exc_probe.py`, not the product fix, which every seat
agrees is in the right place.  **If it does not sweep, the row closes as a measured non-finding** with the
score recorded, which is a result and not a waste.

*** SECOND, INDEPENDENT PREDICTION OF THE SAME HOLE -- FROM A DIFFERENT SEAT, ON A DIFFERENT MUTANT.
That is the one kind of agreement this project counts as evidence. ***

The `kimi-k3:cloud` substitute (the CLI being 403-walled) returned **NOT A CLEAN RATIFY** and predicted:

    *"a one-line deletion of `implemented = true;' on an unprobed exception class re-opens #502 exactly,
     and every probe row named in this packet stays green."*

**It is a DIFFERENT mutant from grok's** -- a bare DELETION on a class the probe never drives, where grok's is
a CONDITIONED repair (`implemented = (cpu->machine->ncpus < 2)`) on the seven arms.  Two seats, two shapes, one
conclusion: **the 59-row detector does not cover the `implemented' flag across the excepti [... 15106 more characters not shown]

**hold_question:** The L2 repair adds one row to a 59-row detector.  Does that oblige re-measuring every mutant already scored against those 59, or is a targeted table (baseline + the mutants whose kill sets could plausibly move) sufficient?  The cost difference is a full table versus a few runs.

**An earlier triage pass proposed:** FIX-NOW -- perform the full table measurement on agy as explicitly ruled by the adjudicator

## The code at the cited lines

### `src/core/main.c` around the row's cited line 423 (HEAD 8d9df658, lines 303-543)

```c
  303| 	int ch, res;
  304| 
  305| 	char *type = NULL, *subtype = NULL;
  306| 	struct machine *m = emul_add_machine(emul, NULL);
  307| 
  308| 	const char *opts =
  309| 	    "AC:c:Dd:E:e:fGHhI:iJj:k:KL:M:Nn:Oo:p:QqRrSs:TtVvW:"
  310| #ifdef WITH_X11
  311| 	    "XxY:"
  312| #endif
  313| 	    "Z:z:";
  314| 
  315| 	while ((ch = getopt(argc, argv, opts)) != -1) {
  316| 		switch (ch) {
  317| 		case 'A':
  318| 			enable_colorized_output = false;
  319| 			break;
  320| 		case 'C':
  321| 			CHECK_ALLOCATION(m->cpu_name = strdup(optarg));
  322| 			machine_specific_options_used = true;
  323| 			break;
  324| 		case 'c':
  325| 			emul->n_debugger_cmds ++;
  326| 			CHECK_ALLOCATION(emul->debugger_cmds = (char **)
  327| 			    realloc(emul->debugger_cmds,
  328| 			    emul->n_debugger_cmds * sizeof(char *)));
  329| 			CHECK_ALLOCATION(emul->debugger_cmds[emul->
  330| 			    n_debugger_cmds-1] = strdup(optarg));
  331| 			break;
  332| 		case 'D':
  333| 			skip_srandom_call = true;
  334| 			break;
  335| 		case 'd':
  336| 			/*  diskimage_add() is called further down  */
  337| 			(*n_diskimagesp) ++;
  338| 			CHECK_ALLOCATION( (*diskimagesp) = (char **)
  339| 			    realloc(*diskimagesp,
  340| 			    sizeof(char *) * (*n_diskimagesp)) );
  341| 			CHECK_ALLOCATION( (*diskimagesp)[(*n_diskimagesp) - 1] =
  342| 			    strdup(optarg) );
  343| 			using_switch_d = true;
  344| 			machine_specific_options_used = true;
  345| 			break;
  346| 		case 'E':
  347| 			if (using_switch_E ++ > 0) {
  348| 				fprintf(stderr, "-E already used.\n");
  349| 				exit(1);
  350| 			}
  351| 			type = optarg;
  352| 			machine_specific_options_used = true;
  353| 			break;
  354| 		case 'e':
  355| 			if (using_switch_e ++ > 0) {
  356| 				fprintf(stderr, "-e already used.\n");
  357| 				exit(1);
  358| 			}
  359| 			subtype = optarg;
  360| 			machine_specific_options_used = true;
  361| 			break;
  362| 		case 'f':
  363| 			/*  Force an fsync on every disk image write:  */
  364| 			do_fsync = 1;
  365| 			break;
  366| 		case 'G':
  367| 			enable_colorized_output = true;
  368| 			break;
  369| 		case 'H':
  370| 			machine_list_available_types_and_cpus();
  371| 			exit(1);
  372| 		case 'h':
  373| 			usage(true);
  374| 			exit(1);
  375| 		case 'I':
  376| 			m->emulated_hz = atoi(optarg);
  377| 			machine_specific_options_used = true;
  378| 			break;
  379| 		case 'i':
  380| 			m->instruction_trace = 1;
  381| 			machine_specific_options_used = true;
  382| 			break;
  383| 		case 'J':
  384| 			m->allow_instruction_combinations = 0;
  385| 			machine_specific_options_used = true;
  386| 			break;
  387| 		case 'j':
  388| 			CHECK_ALLOCATION(m->boot_kernel_filename = strdup(optarg));
  389| 			machine_specific_options_used = true;
  390| 			break;
  391| 		case 'k':
  392| 			{
  393| 				/*  atoi() overflowed int before the old
  394| 				    "< 1" check ran; the value is multiplied
  395| 				    by 1 MB, so bound it by what fits in a
  396| 				    size_t (and 1 TB as a sanity cap).  */
  397| 				long long max_mb =
  398| 				    (long long) (SIZE_MAX / 1048576);
  399| 				if (max_mb > 1048576)
  400| 					max_mb = 1048576;
  401| 				dyntrans_cache_size = (size_t)
  402| 				    parse_int_option('k', optarg, 1, max_mb)
  403| 				    * 1048576;
  404| 			}
  405| 			break;
  406| 		case 'K':
  407| 			debugger_enter_at_end_of_run = true;
  408| 			break;
  409| 		case 'L':
  410| 			CHECK_ALLOCATION(*tap_devname = strdup(optarg));
  411| 			break;
  412| 		case 'M':
  413| 			/*  atoi() let negative/overflowed values through
  414| 			    to the uint32_t field.  */
  415| 			m->physical_ram_in_mb = (uint32_t)
  416| 			    parse_int_option('M', optarg, 1, 1048576);
  417| 			machine_specific_options_used = true;
  418| 			break;
  419| 		case 'N':
  420| 			m->show_nr_of_instructions = 1;
  421| 			machine_specific_options_used = true;
  422| 			break;
  423| 		case 'n':
  424| 			/*  atoi() accepted negative counts, which later
  425| 			    feed malloc()/memset() size calculations.  */
  426| 			m->ncpus = (int)
  427| 			    parse_int_option('n', optarg, 1, 256);
  428| 			machine_specific_options_used = true;
  429| 			break;
  430| 		case 'O':
  431| 			m->force_netboot = 1;
  432| 			machine_specific_options_used = true;
  433| 			break;
  434| 		case 'o':
  435| 			CHECK_ALLOCATION(m->boot_string_argument = strdup(optarg));
  436| 			machine_specific_options_used = true;
  437| 			break;
  438| 		case 'p':
  439| 			machine_add_breakpoint_string(m, optarg);
  440| 			machine_specific_options_used = true;
  441| 			break;
  442| 		case 'Q':
  443| 			m->prom_emulation = 0;
  444| 			machine_specific_options_used = true;
  445| 			break;
  446| 		case 'q':
  447| 			quiet_mode = 1;
  448| 			break;
  449| 		case 'R':
  450| 			m->use_random_bootstrap_cpu = 1;
  451| 			machine_specific_options_used = true;
  452| 			break;
  453| 		case 'r':
  454| 			m->register_dump = 1;
  455| 			machine_specific_options_used = true;
  456| 			break;
  457| 		case 'S':
  458| 			m->random_mem_contents = 1;
  459| 			machine_specific_options_used = true;
  460| 			break;
  461| 		case 's':
  462| 			machine_statistics_init(m, optarg);
  463| 			machine_specific_options_used = true;
  464| 			break;
  465| 		case 'T':
  466| 			m->halt_on_nonexistant_memaccess = 1;
  467| 			machine_specific_options_used = true;
  468| 			break;
  469| 		case 't':
  470| 			m->show_trace_tree = 1;
  471| 			machine_specific_options_used = true;
  472| 			break;
  473| 		case 'V':
  474| 			single_step = true;
  475| 			debugger_enter_at_end_of_run = true;
  476| 			break;
  477| 		case 'v':
  478| 			verbose ++;
  479| 			break;
  480| 		case 'W':
  481| 			internal_w(optarg);
  482| 			exit(0);
  483| 		case 'X':
  484| 			m->x11_md.in_use = 1;
  485| 			machine_specific_options_used = true;
  486| 			/*  FALL-THROUGH  */
  487| 		case 'x':
  488| 			console_allow_slaves(1);
  489| 			break;
  490| 		case 'Y':
  491| 			m->x11_md.scaledown = atoi(optarg);
  492| 			if (m->x11_md.scaledown < -1) {
  493| 				m->x11_md.scaleup = - m->x11_md.scaledown;
  494| 				m->x11_md.scaledown = 1;
  495| 			}
  496| 			if (m->x11_md.scaledown < 1) {
  497| 				fprintf(stderr, "Invalid scaledown value.\n");
  498| 				exit(1);
  499| 			}
  500| 			machine_specific_options_used = true;
  501| 			break;
  502| 		case 'Z':
  503| 			m->n_gfx_cards = atoi(optarg);
  504| 			using_switch_Z = true;
  505| 			machine_specific_options_used = true;
  506| 			break;
  507| 		case 'z':
  508| 			m->x11_md.n_display_names ++;
  509| 			CHECK_ALLOCATION(m->x11_md.display_names = (char **) realloc(
  510| 			    m->x11_md.display_names,
  511| 			    m->x11_md.n_display_names * sizeof(char *)));
  512| 			CHECK_ALLOCATION(m->x11_md.display_names[
  513| 			    m->x11_md.n_display_names-1] = strdup(optarg));
  514| 			machine_specific_options_used = true;
  515| 			break;
  516| 		default:
  517| 			fprintf(stderr, "Run  %s -h  for help on command "
  518| 			    "line options.\n", progname);
  519| 			exit(1);
  520| 		}
  521| 	}
  522| 
  523| 	argc -= optind;
  524| 	argv += optind;
  525| 
  526| 	extra_argc = argc;
  527| 	extra_argv = argv;
  528| 
  529| 	// If -V is used, -q is ignored.
  530| 	if (single_step && quiet_mode) {
  531| 		fprintf(stderr, "ignoring -q, because -V is used\n");
  532| 		quiet_mode = 0;
  533| 	}
  534| 
  535| 	if (type != NULL || subtype != NULL) {
  536| 		if (type == NULL)
  537| 			type = strdup("");
  538| 		if (subtype == NULL)
  539| 			subtype = strdup("");
  540| 
  541| 		res = machine_name_to_type(type, subtype,
  542| 		    &m->machine_type, &m->machine_subtype);
  543| 		if (!res)
```

### `src/core/emul.c` around the row's cited line 489 (HEAD 8d9df658, lines 369-609)

```c
  369| 			scsidevice = arcbios_addchild_manual(cpu,
  370| 			    COMPONENT_CLASS_ControllerClass,
  371| 			    a, flags, 1, 2, d->id, 0xffffffff,
  372| 			    name, scsicontroller, NULL, 0);
  373| 
  374| 			scsidisk = arcbios_addchild_manual(cpu,
  375| 			    COMPONENT_CLASS_PeripheralClass,
  376| 			    b, flags, 1, 2, 0, 0xffffffff, NULL,
  377| 			    scsidevice, NULL, 0);
  378| 
  379| 			/*
  380| 			 *  Add device string to component address mappings:
  381| 			 *  "scsi(0)disk(0)rdisk(0)partition(0)"
  382| 			 */
  383| 
  384| 			if (d->is_a_cdrom) {
  385| 				snprintf(component_string,
  386| 				    sizeof(component_string),
  387| 				    "scsi(0)cdrom(%i)", d->id);
  388| 				arcbios_add_string_to_component(m,
  389| 				    component_string, scsidevice);
  390| 
  391| 				snprintf(component_string,
  392| 				    sizeof(component_string),
  393| 				    "scsi(0)cdrom(%i)fdisk(0)", d->id);
  394| 				arcbios_add_string_to_component(m,
  395| 				    component_string, scsidisk);
  396| 			} else {
  397| 				snprintf(component_string,
  398| 				    sizeof(component_string),
  399| 				    "scsi(0)disk(%i)", d->id);
  400| 				arcbios_add_string_to_component(m,
  401| 				    component_string, scsidevice);
  402| 
  403| 				snprintf(component_string,
  404| 				    sizeof(component_string),
  405| 				    "scsi(0)disk(%i)rdisk(0)", d->id);
  406| 				arcbios_add_string_to_component(m,
  407| 				    component_string, scsidisk);
  408| 			}
  409| 		}
  410| 
  411| 		d = d->next;
  412| 	}
  413| }
  414| 
  415| 
  416| /*
  417|  *  emul_machine_setup():
  418|  *
  419|  *	o)  Initialize the hardware (RAM, devices, CPUs, ...) which
  420|  *	    will be emulated in this machine.
  421|  *
  422|  *	o)  Load ROM code and/or other programs into emulated memory.
  423|  *
  424|  *	o)  Special hacks needed after programs have been loaded.
  425|  *
  426|  *  Returns true on success, false if the machine could not be set up.
  427|  */
  428| bool emul_machine_setup(struct machine *m, int n_load, char **load_names,
  429| 	int n_devices, char **device_names)
  430| {
  431| 	struct cpu *cpu;
  432| 	uint64_t memory_amount, entrypoint = 0, gp = 0, toc = 0;
  433| 	int i, byte_order;
  434| 
  435| 	if (m->name != NULL && m->name[0])
  436| 		debugmsg(SUBSYS_MACHINE, "", VERBOSITY_INFO, "%s", m->name);
  437| 	else
  438| 		debugmsg(SUBSYS_MACHINE, "", VERBOSITY_INFO, "%s", "");
  439| 
  440| 	debug_indentation(1);
  441| 
  442| 	if (m->machine_type == MACHINE_NONE) {
  443| 		fatal("No machine type specified?\n");
  444| 		return false;
  445| 	}
  446| 
  447| 	// Hack for Alpha.
  448| 	if (m->machine_type == MACHINE_ALPHA)
  449| 		m->arch_pagesize = 8192;
  450| 
  451| 	machine_memsize_fix(m);
  452| 
  453| 	/*
  454| 	 *  Create the system's base memory:
  455| 	 */
  456| 	char meminfo[2000];
  457| 	snprintf(meminfo, sizeof(meminfo), "%i MB", m->physical_ram_in_mb);
  458| 
  459| 	memory_amount = (uint64_t)m->physical_ram_in_mb * 1048576;
  460| 	if (m->memory_offset_in_mb > 0) {
  461| 		/*
  462| 		 *  A special hack is used for some SGI models,
  463| 		 *  where memory is offset by 128MB to leave room for
  464| 		 *  EISA space and other things.
  465| 		 */
  466| 		snprintf(meminfo + strlen(meminfo), sizeof(meminfo) - strlen(meminfo),
  467| 		    " (offset by %i MB)", m->memory_offset_in_mb);
  468| 
  469| 		memory_amount += 1048576 * m->memory_offset_in_mb;
  470| 	}
  471| 
  472| 	if (m->machine_type == MACHINE_SGI && m->machine_subtype == 32) {
  473| 		if (memory_amount > 0x10000000) {
  474| 			memory_amount = 0x10000000;
  475| 			snprintf(meminfo + strlen(meminfo), sizeof(meminfo) - strlen(meminfo),
  476| 			    " (SGI O2 hack: %i MB at offset 0)", 0x10000000 / 1048576);
  477| 		}
  478| 	}
  479| 
  480| 	if (m->random_mem_contents)
  481| 		snprintf(meminfo + strlen(meminfo), sizeof(meminfo) - strlen(meminfo),
  482| 		    ", randomized content");
  483| 
  484| 	m->memory = memory_new(memory_amount);
  485| 
  486| 	/*  Create CPUs:  */
  487| 	if (m->cpu_name == NULL)
  488| 		machine_default_cputype(m);
  489| 	if (m->ncpus == 0)
  490| 		m->ncpus = 1;
  491| 
  492| 	CHECK_ALLOCATION(m->cpus = (struct cpu **) malloc(sizeof(struct cpu *) * m->ncpus));
  493| 	memset(m->cpus, 0, sizeof(struct cpu *) * m->ncpus);
  494| 
  495| 	char cpuname[200];
  496| 	if (m->ncpus == 1)
  497| 		snprintf(cpuname, sizeof(cpuname), "cpu0");
  498| 	else
  499| 		snprintf(cpuname, sizeof(cpuname), "cpu0 .. cpu%i", m->ncpus - 1);
  500| 
  501| 	for (i=0; i<m->ncpus; i++) {
  502| 		m->cpus[i] = cpu_new(m->memory, m, i, m->cpu_name);
  503| 		if (m->cpus[i] == NULL) {
  504| 			fprintf(stderr, "Unable to create CPU object. "
  505| 			    "Aborting.");
  506| 			return false;
  507| 		}
  508| 	}
  509| 
  510| 	if (m->use_random_bootstrap_cpu)
  511| 		m->bootstrap_cpu = random() % m->ncpus;
  512| 	else
  513| 		m->bootstrap_cpu = 0;
  514| 
  515| 	cpu = m->cpus[m->bootstrap_cpu];
  516| 
  517| 	if (m->x11_md.in_use)
  518| 		x11_init(m);
  519| 
  520| 	/*  Fill the directly addressable memory with random bytes:  */
  521| 	if (m->random_mem_contents) {
  522| 		for (i=0; i<(int)memory_amount; i+=256) {
  523| 			unsigned char data[256];
  524| 			unsigned int j;
  525| 			for (j=0; j<sizeof(data); j++)
  526| 				data[j] = random() & 255;
  527| 			cpu->memory_rw(cpu, m->memory, i, data, sizeof(data),
  528| 			    MEM_WRITE, CACHE_NONE | NO_EXCEPTIONS | PHYSICAL);
  529| 		}
  530| 	}
  531| 
  532| 	for (i=0; i<n_devices; i++)
  533| 		device_add(m, device_names[i]);
  534| 
  535| 	machine_setup(m);
  536| 
  537| 	cpu_dumpinfo(m, cpu, false);
  538| 	debugmsg(SUBSYS_MACHINE, "memory", VERBOSITY_INFO, "%s", meminfo);
  539| 	diskimage_dump_info(m);
  540| 	console_debug_dump(m);
  541| 
  542| 	/*  Load files (ROM code, boot code, ...) into memory:  */
  543| 	if (n_load == 0) {
  544| 		if (m->first_diskimage != NULL) {
  545| 			if (!load_bootblock(m, cpu, &n_load, &load_names)) {
  546| 				fprintf(stderr, "\nNo executable files were"
  547| 				    " specified, and booting directly from disk"
  548| 				    " failed.\n");
  549| 				return false;
  550| 			}
  551| 		} else {
  552| 			fprintf(stderr, "No executable file(s) loaded, and "
  553| 			    "we are not booting directly from a disk image."
  554| 			    "\nAborting.\n");
  555| 			return false;
  556| 		}
  557| 	}
  558| 
  559| 	while (n_load > 0) {
  560| 		FILE *tmp_f;
  561| 		char *name_to_load = *load_names;
  562| 		int remove_after_load = 0;
  563| 		char *gunzip_temp_name = NULL;
  564| 
  565| 		/*  Special hack for removing temporary files:  */
  566| 		if (name_to_load[0] == 8) {
  567| 			name_to_load ++;
  568| 			remove_after_load = 1;
  569| 		}
  570| 
  571| 		/*
  572| 		 *  gzipped files are automagically gunzipped, by running
  573| 		 *  gunzip via fork()/exec() (never via a shell) into a fresh
  574| 		 *  temporary file.
  575| 		 */
  576| 		tmp_f = fopen(name_to_load, "r");
  577| 		if (tmp_f != NULL) {
  578| 			unsigned char buf[2];		/*  gzip header  */
  579| 			size_t res;
  580| 
  581| 			memset(buf, 0, sizeof(buf));
  582| 			res = fread(buf, 1, sizeof(buf), tmp_f);
  583| 
  584| 			if (res == sizeof(buf) &&
  585| 			    buf[0] == 0x1f && buf[1] == 0x8b) {
  586| 				int tmpfile_handle;
  587| 				char *new_temp_name;
  588| 				const char *tmpdir = getenv("TMPDIR");
  589| 
  590| 				if (tmpdir == NULL)
  591| 					tmpdir = DEFAULT_TMP_DIR;
  592| 
  593| 				debug("gunziping %s\n", name_to_load);
  594| 
  595| 				CHECK_ALLOCATION(new_temp_name =
  596| 				    (char*) malloc(300));
  597| 				snprintf(new_temp_name, 300,
  598| 				    "%s/gxemul.XXXXXXXXXXXX", tmpdir);
  599| 
  600| 				tmpfile_handle = mkstemp(new_temp_name);
  601| 				if (tmpfile_handle < 0) {
  602| 					perror(new_temp_name);
  603| 					exit(1);
  604| 				}
  605| 
  606| 				/*  Pass the open fd to the child (which dup2()s it
  607| 				    to stdout) instead of reopening new_temp_name by
  608| 				    name, closing the same-user temp race.  */
  609| 				if (decompress_gzip_to(name_to_load,
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

End with one line: `FIXDRAFT_M88KEXCDETECTORL2: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
