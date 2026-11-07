# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armmmufaultlog` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armmmufaultlog`, state `open`)

**title:** cpus/memory_arm.c:arm_translate_v2p_mmu -- two `fatal()` lines per guest page fault unless -q -- HYGIENE (guest-drivable host log flood)

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T139 (class HYGIENE; reach U, user mode; effort: one-line; report rows: A1-41, C U20).  Source URLs: https://github.com/retroprom/gxemul/commit/bc914bbe, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/memory_arm.c:261-266.  Portable fix: yes -- port upstream bc914bbe (SVN r6575).  Filing check (TRIAGE.md): mentioned only as the symptom in `armvecrecurse`'s witness.  Not a duplicate of `armvecrecurse` (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A: it exceeds the row it resembles).  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- 261| 	if (!quiet_mode) {

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/memory_arm.c b/src/cpus/memory_arm.c
index 679532ee..44049a77 100644
--- a/src/cpus/memory_arm.c
+++ b/src/cpus/memory_arm.c
@@ -258,12 +258,6 @@ exception_return:
 	if (no_exceptions)
 		return 0;
 
-	if (!quiet_mode) {
-		fatal("{ arm memory fault: vaddr=0x%08x domain=%i dav=%i ap=%i "
-		    "access=%i user=%i", (int)vaddr, domain, dav, ap,
-		    access, user);
-		fatal(" d=0x%08x d2=0x%08x pc=0x%08x }\n", d, d2, (int)cpu->pc);
-	}
 
 	if (instr)
 		arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
```

## Every edited function, after the fix

### `src/cpus/memory_arm.c` -- post-edit lines 116-271 (`+` marks a line the diff added or the point of a deletion)

```c
  116|  {
  117|  	unsigned char *q;
  118|  	uint32_t addr, d=0, d2 = (uint32_t)(int32_t)-1, ptba, vaddr = vaddr64;
  119|  	int instr = flags & FLAG_INSTR;
  120|  	int writeflag = (flags & FLAG_WRITEFLAG)? 1 : 0;
  121|  	int useraccess = flags & MEMORY_USER_ACCESS;
  122|  	int no_exceptions = flags & FLAG_NOEXCEPTIONS;
  123|  	int user = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32;
  124|  	int domain, dav, ap0,ap1,ap2,ap3, ap = 0, access = 0;
  125|  	int fs = 2;		/*  fault status (2 = terminal exception)  */
  126|  	int subpage = 0;
  127|  
  128|  	if (useraccess)
  129|  		user = 1;
  130|  
  131|  	addr = ((vaddr & 0xfff00000ULL) >> 18);
  132|  
  133|  	if (cpu->cd.arm.translation_table == NULL ||
  134|  	    cpu->cd.arm.ttb != cpu->cd.arm.last_ttb) {
  135|  		cpu->cd.arm.translation_table = memory_paddr_to_hostaddr(
  136|  		    cpu->mem, cpu->cd.arm.ttb & 0x0fffffff, 0);
  137|  		cpu->cd.arm.last_ttb = cpu->cd.arm.ttb;
  138|  	}
  139|  
  140|  	if (cpu->cd.arm.translation_table != NULL) {
  141|  		d = *(uint32_t *)(cpu->cd.arm.translation_table + addr);
  142|  #ifdef HOST_LITTLE_ENDIAN
  143|  		if (cpu->byte_order == EMUL_BIG_ENDIAN)
  144|  #else
  145|  		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  146|  #endif
  147|  			d = ((d & 0xff) << 24) | ((d & 0xff00) << 8) |
  148|  			    ((d & 0xff0000) >> 8) | ((d & 0xff000000) >> 24);
  149|  	}
  150|  
  151|  	/*  Get the domain from the descriptor, and the Domain Access Value:  */
  152|  	domain = (d >> 5) & 15;
  153|  	dav = (cpu->cd.arm.dacr >> (domain * 2)) & 3;
  154|  
  155|  	switch (d & 3) {
  156|  
  157|  	case 0:	domain = 0;
  158|  		fs = FAULT_TRANS_S;
  159|  		goto exception_return;
  160|  
  161|  	case 1:	/*  Course Pagetable:  */
  162|  		if (dav == 0) {
  163|  			fs = FAULT_DOMAIN_P;
  164|  			goto exception_return;
  165|  		}
  166|  		ptba = d & 0xfffffc00;
  167|  		addr = ptba + ((vaddr & 0x000ff000) >> 10);
  168|  
  169|  		q = memory_paddr_to_hostaddr(cpu->mem, addr & 0x0fffffff, 0);
  170|  		if (q == NULL) {
  171|  			/*  #193: (Codex/Fable) an L2 page-table page outside mapped
  172|  			    RAM must fault the guest, not exit() the host.  */
  173|  			fs = FAULT_TRANS_P;
  174|  			goto exception_return;
  175|  		}
  176|  		d2 = *(uint32_t *)(q);
  177|  #ifdef HOST_LITTLE_ENDIAN
  178|  		if (cpu->byte_order == EMUL_BIG_ENDIAN)
  179|  #else
  180|  		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
  181|  #endif
  182|  			d2 = ((d2 & 0xff) << 24) | ((d2 & 0xff00) << 8) |
  183|  			     ((d2 & 0xff0000) >> 8) | ((d2 & 0xff000000) >> 24);
  184|  
  185|  		switch (d2 & 3) {
  186|  		case 0:	fs = FAULT_TRANS_P;
  187|  			goto exception_return;
  188|  		case 1:	/*  16KB page:  */
  189|  			ap = (d2 >> 4) & 255;
  190|  			switch (vaddr & 0x0000c000) {
  191|  			case 0x4000:	ap >>= 2; break;
  192|  			case 0x8000:	ap >>= 4; break;
  193|  			case 0xc000:	ap >>= 6; break;
  194|  			}
  195|  			ap &= 3;
  196|  			*return_paddr = (d2 & 0xffff0000)|(vaddr & 0x0000ffff);
  197|  			break;
  198|  		case 3:	if (cpu->cd.arm.cpu_type.flags & ARM_XSCALE) {
  199|  				/*  4KB page (Xscale)  */
  200|  				subpage = 0;
  201|  			} else {
  202|  				/*  1KB page  */
  203|  				subpage = 1;
  204|  				ap = (d2 >> 4) & 3;
  205|  				*return_paddr = (d2 & 0xfffffc00) |
  206|  				    (vaddr & 0x000003ff);
  207|  				break;
  208|  			}
  209|  			/*  NOTE: Fall-through for XScale!  */
  210|  			// fall through
  211|  		case 2:	/*  4KB page:  */
  212|  			ap3 = (d2 >> 10) & 3;
  213|  			ap2 = (d2 >>  8) & 3;
  214|  			ap1 = (d2 >>  6) & 3;
  215|  			ap0 = (d2 >>  4) & 3;
  216|  			switch (vaddr & 0x00000c00) {
  217|  			case 0x000: ap = ap0; break;
  218|  			case 0x400: ap = ap1; break;
  219|  			case 0x800: ap = ap2; break;
  220|  			default:    ap = ap3;
  221|  			}
  222|  			/*  NOTE: Ugly hack for XScale:  */
  223|  			if ((d2 & 3) == 3) {
  224|  				/*  Treated as 4KB page:  */
  225|  				ap = ap0;
  226|  			} else {
  227|  				if (ap0 != ap1 || ap0 != ap2 || ap0 != ap3)
  228|  					subpage = 1;
  229|  			}
  230|  			*return_paddr = (d2 & 0xfffff000)|(vaddr & 0x00000fff);
  231|  			break;
  232|  		}
  233|  		access = arm_check_access(cpu, ap, dav, user);
  234|  		if (access > writeflag)
  235|  			return access | (subpage? MEMORY_NOT_FULL_PAGE : 0);
  236|  		fs = FAULT_PERM_P;
  237|  		goto exception_return;
  238|  
  239|  	case 2:	/*  Section descriptor:  */
  240|  		if (dav == 0) {
  241|  			fs = FAULT_DOMAIN_S;
  242|  			goto exception_return;
  243|  		}
  244|  		*return_paddr = (d & 0xfff00000) | (vaddr & 0x000fffff);
  245|  		ap = (d >> 10) & 3;
  246|  		access = arm_check_access(cpu, ap, dav, user);
  247|  		if (access > writeflag)
  248|  			return access;
  249|  		fs = FAULT_PERM_S;
  250|  		goto exception_return;
  251|  
  252|  	default:fatal("TODO: descriptor for vaddr 0x%08x: 0x%08x ("
  253|  		    "unimplemented type %i)\n", vaddr, d, d&3);
  254|  		exit(1);
  255|  	}
  256|  
  257|  exception_return:
  258|  	if (no_exceptions)
  259|  		return 0;
  260|  
  261|+ 
  262|  	if (instr)
  263|  		arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
  264|  	else {
  265|  		cpu->cd.arm.far = vaddr;
  266|  		cpu->cd.arm.fsr = (domain << 4) | fs;
  267|  		arm_exception(cpu, ARM_EXCEPTION_DATA_ABT);
  268|  	}
  269|  
  270|  	return 0;
  271|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMMMUFAULTLOG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMMMUFAULTLOG: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
