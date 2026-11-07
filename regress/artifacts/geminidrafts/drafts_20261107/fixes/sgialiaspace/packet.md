# GXemul hardened fork -- DRAFT A FIX for one filed issue, `sgialiaspace` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `sgialiaspace`, state `open`, severity `HIGH`)

**title:** alias extractor misses aliases that contain a space

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): regress24:F3 | draft said NEW MED `sgialiaspace` | should be NEW HIGH `sgialiaspace` | The omitted subtype aliases are registered at `src/machines/machine_sgi.c:740`. Removing them leaves the extractor unchanged (`regress/gate_ab.sh:322-336`), but selecting the formerly supported subtype reaches `exit(1)` at `src/machines/machine.c:190-212`. The supplied rule includes process termination at...

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- exit(1) process termination perfectly matches the project mandate of fixing crash-on-malformed-input defects.

## The code at the cited lines

### `src/machines/machine_sgi.c` around the row's cited line 740 (HEAD d2a6f233, lines 695-751)

```c
  695| 	    machine->machine_subtype == 30 || machine->machine_subtype == 32))
  696| 	        machine->cpu_name = strdup("R10000");
  697| 	if (machine->cpu_name == NULL && (machine->machine_subtype == 21 ||
  698| 	    machine->machine_subtype == 26))
  699| 	        machine->cpu_name = strdup("R8000");
  700| 	if (machine->cpu_name == NULL && machine->machine_subtype == 24)
  701| 	        machine->cpu_name = strdup("R5000");
  702|                         
  703| 	/*  Other SGIs should probably work with
  704| 	    R4000, R4400 or R5000 or similar:  */
  705| 	if (machine->cpu_name == NULL)
  706| 	        machine->cpu_name = strdup("R4400");
  707| }
  708| 
  709| 
  710| MACHINE_DEFAULT_RAM(sgi)
  711| {
  712| 	// Self-compilation fails with OpenBSD/sgi 6.3 with as low as 128 MB
  713| 	// RAM, so 256 would be better. But my O2 has 128 MB, so this is kept
  714| 	// as 128 to simplify comparison between the real machine and the
  715| 	// emulator.
  716| 	machine->physical_ram_in_mb = 128;
  717| }
  718| 
  719| 
  720| MACHINE_REGISTER(sgi)
  721| {
  722| 	MR_DEFAULT(sgi, "SGI", MACHINE_SGI);
  723| 
  724| 	me->set_default_ram = machine_default_ram_sgi;
  725| 
  726| 	machine_entry_add_alias(me, "silicon graphics");
  727| 	machine_entry_add_alias(me, "sgi");
  728| 
  729| 	machine_entry_add_subtype(me, "IP12", 12, "ip12", NULL);
  730| 
  731| 	machine_entry_add_subtype(me, "IP19", 19, "ip19", NULL);
  732| 
  733| 	machine_entry_add_subtype(me, "IP20", 20, "ip20", NULL);
  734| 
  735| 	machine_entry_add_subtype(me, "IP22", 22, "ip22", "indy", NULL);
  736| 
  737| 	machine_entry_add_subtype(me, "IP24", 24, "ip24", NULL);
  738| 
  739| 	machine_entry_add_subtype(me, "IP27", 27,
  740| 	    "ip27", "origin 200", "origin 2000", NULL);
  741| 
  742| 	machine_entry_add_subtype(me, "IP28", 28, "ip28", NULL);
  743| 
  744| 	machine_entry_add_subtype(me, "IP30", 30, "ip30", "octane", NULL);
  745| 
  746| 	machine_entry_add_subtype(me, "IP32", 32, "ip32", "o2", NULL); 
  747| 
  748| 	machine_entry_add_subtype(me, "IP35", 35, "ip35", NULL); 
  749| }
  750| 
  751| 
```

### `src/machines/machine.c` around the row's cited line 190 (HEAD d2a6f233, lines 145-235)

```c
  145| 	free(machine);
  146| }
  147| 
  148| 
  149| /*
  150|  *  machine_name_to_type():
  151|  *
  152|  *  Take a type and a subtype as strings, and convert them into numeric
  153|  *  values used internally throughout the code.
  154|  *
  155|  *  Return value is 1 on success, 0 if there was no match.
  156|  *  Also, any errors/warnings are printed using fatal()/debug().
  157|  */
  158| int machine_name_to_type(char *stype, char *ssubtype,
  159| 	int *type, int *subtype)
  160| {
  161| 	struct machine_entry *me;
  162| 	int i, j, k, nmatches = 0;
  163| 
  164| 	*type = MACHINE_NONE;
  165| 	*subtype = 0;
  166| 
  167| 	/*  Check stype, and optionally ssubtype:  */
  168| 	me = first_machine_entry;
  169| 	while (me != NULL) {
  170| 		for (i=0; i<me->n_aliases; i++)
  171| 			if (strcasecmp(me->aliases[i], stype) == 0) {
  172| 				/*  Found a type:  */
  173| 				*type = me->machine_type;
  174| 
  175| 				if (me->n_subtypes == 0)
  176| 					return 1;
  177| 
  178| 				/*  Check for subtype:  */
  179| 				for (j=0; j<me->n_subtypes; j++)
  180| 					for (k=0; k<me->subtype[j]->n_aliases;
  181| 					    k++)
  182| 						if (strcasecmp(ssubtype,
  183| 						    me->subtype[j]->aliases[k]
  184| 						    ) == 0) {
  185| 							*subtype = me->subtype[
  186| 							    j]->machine_subtype;
  187| 							return 1;
  188| 						}
  189| 
  190| 				fatal("Unknown subtype '%s' for emulation"
  191| 				    " '%s'\n", ssubtype, stype);
  192| 				if (!ssubtype[0])
  193| 					fatal("(Maybe you forgot the -e"
  194| 					    " command line option?)\n");
  195| 
  196| 				/*  List the available subtypes, instead of
  197| 				    just complaining (see the TODO list):  */
  198| 				fatal("\nAvailable subtypes for '%s' are:\n",
  199| 				    stype);
  200| 				for (j=0; j<me->n_subtypes; j++) {
  201| 					struct machine_entry_subtype *mes =
  202| 					    me->subtype[j];
  203| 					fatal("  %s (", mes->name);
  204| 					for (k=0; k<mes->n_aliases; k++)
  205| 						fatal("%s\"%s\"", k? ", " : "",
  206| 						    mes->aliases[k]);
  207| 					fatal(")\n");
  208| 				}
  209| 				fatal("\nUse an alias when selecting a "
  210| 				    "subtype, e.g.:  -e %s\n",
  211| 				    me->subtype[0]->aliases[0]);
  212| 				exit(1);
  213| 			}
  214| 
  215| 		me = me->next;
  216| 	}
  217| 
  218| 	/*  Not found? Then just check ssubtype:  */
  219| 	me = first_machine_entry;
  220| 	while (me != NULL) {
  221| 		if (me->n_subtypes == 0) {
  222| 			me = me->next;
  223| 			continue;
  224| 		}
  225| 
  226| 		/*  Check for subtype:  */
  227| 		for (j=0; j<me->n_subtypes; j++)
  228| 			for (k=0; k<me->subtype[j]->n_aliases; k++)
  229| 				if (strcasecmp(ssubtype, me->subtype[j]->
  230| 				    aliases[k]) == 0) {
  231| 					*type = me->machine_type;
  232| 					*subtype = me->subtype[j]->machine_subtype;
  233| 					nmatches ++;
  234| 				}
  235| 
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

End with one line: `FIXDRAFT_SGIALIASPACE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
