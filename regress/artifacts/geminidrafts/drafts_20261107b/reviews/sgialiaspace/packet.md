# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `sgialiaspace` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `sgialiaspace`, state `open`)

**title:** alias extractor misses aliases that contain a space

**state_note (head):** GOVERNING TEXT (from the dispositions file, cut at 400 characters): regress24:F3 | draft said NEW MED `sgialiaspace` | should be NEW HIGH `sgialiaspace` | The omitted subtype aliases are registered at `src/machines/machine_sgi.c:740`. Removing them leaves the extractor unchanged (`regress/gate_ab.sh:322-336`), but selecting the formerly supported subtype reaches `exit(1)` at `src/machines/machine.c:190-212`. The supplied rule includes process termination at...

**The drafter's own reading:** STILL PRESENT: YES -- `src/machines/machine.c:212`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/machines/machine.c b/src/machines/machine.c
index d3d57160..3d05d64f 100644
--- a/src/machines/machine.c
+++ b/src/machines/machine.c
@@ -209,7 +209,8 @@ int machine_name_to_type(char *stype, char *ssubtype,
 				fatal("\nUse an alias when selecting a "
 				    "subtype, e.g.:  -e %s\n",
 				    me->subtype[0]->aliases[0]);
-				exit(1);
+				*type = MACHINE_NONE;
+				return 0;
 			}
 
 		me = me->next;
```

## Every edited function, after the fix

### `src/machines/machine.c` -- post-edit lines 160-260 (`+` marks a line the diff added or the point of a deletion)

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
  212|+ 				*type = MACHINE_NONE;
  213|+ 				return 0;
  214|  			}
  215|  
  216|  		me = me->next;
  217|  	}
  218|  
  219|  	/*  Not found? Then just check ssubtype:  */
  220|  	me = first_machine_entry;
  221|  	while (me != NULL) {
  222|  		if (me->n_subtypes == 0) {
  223|  			me = me->next;
  224|  			continue;
  225|  		}
  226|  
  227|  		/*  Check for subtype:  */
  228|  		for (j=0; j<me->n_subtypes; j++)
  229|  			for (k=0; k<me->subtype[j]->n_aliases; k++)
  230|  				if (strcasecmp(ssubtype, me->subtype[j]->
  231|  				    aliases[k]) == 0) {
  232|  					*type = me->machine_type;
  233|  					*subtype = me->subtype[j]->machine_subtype;
  234|  					nmatches ++;
  235|  				}
  236|  
  237|  		me = me->next;
  238|  	}
  239|  
  240|  	switch (nmatches) {
  241|  	case 0:	fatal("\nSorry, emulation \"%s\"", stype);
  242|  		if (ssubtype != NULL && ssubtype[0] != '\0')
  243|  			fatal(" (subtype \"%s\")", ssubtype);
  244|  		fatal(" is unknown.\n");
  245|  		break;
  246|  	case 1:	return 1;
  247|  	default:fatal("\nSorry, multiple matches for \"%s\"", stype);
  248|  		if (ssubtype != NULL && ssubtype[0] != '\0')
  249|  			fatal(" (subtype \"%s\")", ssubtype);
  250|  		fatal(".\n");
  251|  	}
  252|  
  253|  	*type = MACHINE_NONE;
  254|  	*subtype = 0;
  255|  
  256|  	fatal("Use the -H command line option to get a list of "
  257|  	    "available types and subtypes.\n\n");
  258|  
  259|  	return 0;
  260|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_SGIALIASPACE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_SGIALIASPACE: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
