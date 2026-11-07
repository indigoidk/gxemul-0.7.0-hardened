# GXemul hardened fork -- DRAFT A FIX for one filed issue, `m88kexcdetectorl2` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
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

### `src/core/main.c` around the row's cited line 423 (HEAD 2d25df65, lines 378-468)

```c
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
```

### `src/core/emul.c` around the row's cited line 489 (HEAD 2d25df65, lines 444-534)

```c
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

End with one line: `FIXDRAFT_M88KEXCDETECTORL2: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
