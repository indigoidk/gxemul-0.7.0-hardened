# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armmmufaultlog` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armmmufaultlog`, state `open`, severity `LOW`)

**title:** cpus/memory_arm.c:arm_translate_v2p_mmu -- two `fatal()` lines per guest page fault unless -q -- HYGIENE (guest-drivable host log flood)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T139 (class HYGIENE; reach U, user mode; effort: one-line; report rows: A1-41, C U20).  Source URLs: https://github.com/retroprom/gxemul/commit/bc914bbe, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/memory_arm.c:261-266.  Portable fix: yes -- port upstream bc914bbe (SVN r6575).  Filing check (TRIAGE.md): mentioned only as the symptom in `armvecrecurse`'s witness.  Not a duplicate of `armvecrecurse` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- one-line log flood fix port.

## The code at the cited lines

### `src/cpus/memory_arm.c` around the row's cited line 261 (HEAD 2d25df65, lines 216-279)

```c
  216| 			switch (vaddr & 0x00000c00) {
  217| 			case 0x000: ap = ap0; break;
  218| 			case 0x400: ap = ap1; break;
  219| 			case 0x800: ap = ap2; break;
  220| 			default:    ap = ap3;
  221| 			}
  222| 			/*  NOTE: Ugly hack for XScale:  */
  223| 			if ((d2 & 3) == 3) {
  224| 				/*  Treated as 4KB page:  */
  225| 				ap = ap0;
  226| 			} else {
  227| 				if (ap0 != ap1 || ap0 != ap2 || ap0 != ap3)
  228| 					subpage = 1;
  229| 			}
  230| 			*return_paddr = (d2 & 0xfffff000)|(vaddr & 0x00000fff);
  231| 			break;
  232| 		}
  233| 		access = arm_check_access(cpu, ap, dav, user);
  234| 		if (access > writeflag)
  235| 			return access | (subpage? MEMORY_NOT_FULL_PAGE : 0);
  236| 		fs = FAULT_PERM_P;
  237| 		goto exception_return;
  238| 
  239| 	case 2:	/*  Section descriptor:  */
  240| 		if (dav == 0) {
  241| 			fs = FAULT_DOMAIN_S;
  242| 			goto exception_return;
  243| 		}
  244| 		*return_paddr = (d & 0xfff00000) | (vaddr & 0x000fffff);
  245| 		ap = (d >> 10) & 3;
  246| 		access = arm_check_access(cpu, ap, dav, user);
  247| 		if (access > writeflag)
  248| 			return access;
  249| 		fs = FAULT_PERM_S;
  250| 		goto exception_return;
  251| 
  252| 	default:fatal("TODO: descriptor for vaddr 0x%08x: 0x%08x ("
  253| 		    "unimplemented type %i)\n", vaddr, d, d&3);
  254| 		exit(1);
  255| 	}
  256| 
  257| exception_return:
  258| 	if (no_exceptions)
  259| 		return 0;
  260| 
  261| 	if (!quiet_mode) {
  262| 		fatal("{ arm memory fault: vaddr=0x%08x domain=%i dav=%i ap=%i "
  263| 		    "access=%i user=%i", (int)vaddr, domain, dav, ap,
  264| 		    access, user);
  265| 		fatal(" d=0x%08x d2=0x%08x pc=0x%08x }\n", d, d2, (int)cpu->pc);
  266| 	}
  267| 
  268| 	if (instr)
  269| 		arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
  270| 	else {
  271| 		cpu->cd.arm.far = vaddr;
  272| 		cpu->cd.arm.fsr = (domain << 4) | fs;
  273| 		arm_exception(cpu, ARM_EXCEPTION_DATA_ABT);
  274| 	}
  275| 
  276| 	return 0;
  277| }
  278| 
  279| 
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

End with one line: `FIXDRAFT_ARMMMUFAULTLOG: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
