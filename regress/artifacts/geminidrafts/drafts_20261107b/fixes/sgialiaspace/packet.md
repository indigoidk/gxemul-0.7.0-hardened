# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `sgialiaspace` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `sgialiaspace`, state `open`)

**title:** alias extractor misses aliases that contain a space

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): regress24:F3 | draft said NEW MED `sgialiaspace` | should be NEW HIGH `sgialiaspace` | The omitted subtype aliases are registered at `src/machines/machine_sgi.c:740`. Removing them leaves the extractor unchanged (`regress/gate_ab.sh:322-336`), but selecting the formerly supported subtype reaches `exit(1)` at `src/machines/machine.c:190-212`. The supplied rule includes process termination at...

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/machines/machine.c` -- AT HEAD, lines 160-259 (`*` marks a line your previous draft changed)

```c
  160|  {
  161|  	struct machine_entry *me;
  162|  	int i, j, k, nmatches = 0;
  163|  
  164|  	*type = MACHINE_NONE;
  165|  	*subtype = 0;
  166|  
  167|  	/*  Check stype, and optionally ssubtype:  */
  168|  	me = first_machine_entry;
  169|  	while (me != NULL) {
  170|  		for (i=0; i<me->n_aliases; i++)
  171|  			if (strcasecmp(me->aliases[i], stype) == 0) {
  172|  				/*  Found a type:  */
  173|  				*type = me->machine_type;
  174|  
  175|  				if (me->n_subtypes == 0)
  176|  					return 1;
  177|  
  178|  				/*  Check for subtype:  */
  179|  				for (j=0; j<me->n_subtypes; j++)
  180|  					for (k=0; k<me->subtype[j]->n_aliases;
  181|  					    k++)
  182|  						if (strcasecmp(ssubtype,
  183|  						    me->subtype[j]->aliases[k]
  184|  						    ) == 0) {
  185|  							*subtype = me->subtype[
  186|  							    j]->machine_subtype;
  187|  							return 1;
  188|  						}
  189|  
  190|  				fatal("Unknown subtype '%s' for emulation"
  191|  				    " '%s'\n", ssubtype, stype);
  192|  				if (!ssubtype[0])
  193|  					fatal("(Maybe you forgot the -e"
  194|  					    " command line option?)\n");
  195|  
  196|  				/*  List the available subtypes, instead of
  197|  				    just complaining (see the TODO list):  */
  198|  				fatal("\nAvailable subtypes for '%s' are:\n",
  199|  				    stype);
  200|  				for (j=0; j<me->n_subtypes; j++) {
  201|  					struct machine_entry_subtype *mes =
  202|  					    me->subtype[j];
  203|  					fatal("  %s (", mes->name);
  204|  					for (k=0; k<mes->n_aliases; k++)
  205|  						fatal("%s\"%s\"", k? ", " : "",
  206|  						    mes->aliases[k]);
  207|  					fatal(")\n");
  208|  				}
  209|  				fatal("\nUse an alias when selecting a "
  210|  				    "subtype, e.g.:  -e %s\n",
  211|  				    me->subtype[0]->aliases[0]);
  212|* 				exit(1);
  213|* 			}
  214|  
  215|  		me = me->next;
  216|  	}
  217|  
  218|  	/*  Not found? Then just check ssubtype:  */
  219|  	me = first_machine_entry;
  220|  	while (me != NULL) {
  221|  		if (me->n_subtypes == 0) {
  222|  			me = me->next;
  223|  			continue;
  224|  		}
  225|  
  226|  		/*  Check for subtype:  */
  227|  		for (j=0; j<me->n_subtypes; j++)
  228|  			for (k=0; k<me->subtype[j]->n_aliases; k++)
  229|  				if (strcasecmp(ssubtype, me->subtype[j]->
  230|  				    aliases[k]) == 0) {
  231|  					*type = me->machine_type;
  232|  					*subtype = me->subtype[j]->machine_subtype;
  233|  					nmatches ++;
  234|  				}
  235|  
  236|  		me = me->next;
  237|  	}
  238|  
  239|  	switch (nmatches) {
  240|  	case 0:	fatal("\nSorry, emulation \"%s\"", stype);
  241|  		if (ssubtype != NULL && ssubtype[0] != '\0')
  242|  			fatal(" (subtype \"%s\")", ssubtype);
  243|  		fatal(" is unknown.\n");
  244|  		break;
  245|  	case 1:	return 1;
  246|  	default:fatal("\nSorry, multiple matches for \"%s\"", stype);
  247|  		if (ssubtype != NULL && ssubtype[0] != '\0')
  248|  			fatal(" (subtype \"%s\")", ssubtype);
  249|  		fatal(".\n");
  250|  	}
  251|  
  252|  	*type = MACHINE_NONE;
  253|  	*subtype = 0;
  254|  
  255|  	fatal("Use the -H command line option to get a list of "
  256|  	    "available types and subtypes.\n\n");
  257|  
  258|  	return 0;
  259|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/machines/machine.c",
    "old": "\t\t\t\tfatal(\"\\nUse an alias when selecting a \"\n\t\t\t\t    \"subtype, e.g.:  -e %s\\n\",\n\t\t\t\t    me->subtype[0]->aliases[0]);\n\t\t\t\texit(1);\n\t\t\t}",
    "new": "\t\t\t\tfatal(\"\\nUse an alias when selecting a \"\n\t\t\t\t    \"subtype, e.g.:  -e %s\\n\",\n\t\t\t\t    me->subtype[0]->aliases[0]);\n\t\t\t\treturn 0;\n\t\t\t}",
    "why": "Replace exit(1) with return 0 to prevent process termination on an unknown subtype, matching the documented return values."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_SGIALIASPACE: DEFECT, 2 FINDINGS
1. Does the diff remove the defect the issue describes, at every site the issue names? Name any site it misses.
No. While it replaces the `exit(1)` at `src/machines/machine.c:212`, it completely misses `src/machines/machine_sgi.c:740` and `regress/gate_ab.sh:322-336`, which the issue names as the sites of the omitted aliases and the alias extractor. The root defect ("alias extractor misses aliases that contain a space") is ignored.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above all its COMMON TAIL? Quote the tail line it skips.
Yes. The added `return 0;` at `src/machines/machine.c:212` skips the function's common failure cleanup tail. It skips:
`252| 	*type = MACHINE_NONE;`
`253| 	*subtype = 0;`
3. RETURN VALUE: does any path now return something different? Say what the shown code implies the value means.
Yes, the path previously aborted the process with `exit(1);`. It now returns `0`. As seen at lines 176, 187, and 245 (which `return 1;` on success), and line 258 (which returns `0` at the end of the failure path), returning `0` implies a failure to find a matching machine type and subtype.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that did not print one -- beyond removing the defect?
By skipping the common tail, the diff leaves the out-parameter `*type` modified. At `src/machines/machine.c:173`, `*type` is set to `me->machine_type`. Because the new `return 0;` does not clear it back to `MACHINE_NONE`, the caller receives a failure code but with a mutated `*type` state.
5. House idioms (low severity):
No new diagnostics or comments were added by this diff, so no house idioms (like `(once)` or `/* #NNN: ... */`) were violated. 
src/machines/machine_sgi.c:740: DEFECT: The diff misses the primary site where the omitted subtype aliases are registered, leaving the extractor defect unaddressed. Fix: Add the omitted aliases at this site or fix the extractor to support spaces.
src/machines/machine.c:212: DEFECT: The early return leaks the partially matched state in `*type`. Fix: `*type = MACHINE_NONE; return 0;`
FIXREVIEW_SGIALIASPACE: DEFECT, 2 FINDINGS
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_SGIALIASPACE: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_SGIALIASPACE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
