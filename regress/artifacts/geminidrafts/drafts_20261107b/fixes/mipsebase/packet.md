# GXemul hardened fork -- DRAFT A FIX for one filed issue, `mipsebase` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `mipsebase`, state `open`, severity `MED`)

**title:** cpus/cpu_mips_coproc.c / cpu_mips.c:mips_cpu_exception -- EBase (CP0 15 sel 1) is not modelled for the Release-2 cores (4KEc, 5KE, 24KEc): mtc0 is dropped with an unlatched fatal(), mfc0 returns PRId, the vector base is hard-wired -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T47 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A7-2).  Source URLs: https://github.com/klx3300/gxemul-hos/commit/8f94a57900ee6385d6fb6fcd09f9320af12a95c2.  Our site at de8c7547: src/cpus/cpu_mips_coproc.c:892-894, :1011-1014, :601, :647; src/cpus/cpu_mips.c:2165-2168.  Portable fix: yes -- port klx3300 8f94a57.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port klx3300 8f94a57

## The code at the cited lines

### `src/cpus/cpu_mips_coproc.c` around the row's cited line 892 (HEAD d2a6f233, lines 847-937)

```c
  847| 				if ((cp->reg[COP0_ENTRYHI] &
  848| 				    R2K3K_ENTRYHI_ASID_MASK) !=
  849| 				    (tmp & R2K3K_ENTRYHI_ASID_MASK))
  850| 					inval = 1;
  851| 				break;
  852| 			default:
  853| 				old_asid = cp->reg[COP0_ENTRYHI] & ENTRYHI_ASID;
  854| 				if ((cp->reg[COP0_ENTRYHI] & ENTRYHI_ASID) !=
  855| 				    (tmp & ENTRYHI_ASID))
  856| 					inval = 1;
  857| 				break;
  858| 			}
  859| 
  860| 			if (inval)
  861| 				invalidate_asid(cpu, old_asid);
  862| 
  863| 			unimpl = 0;
  864| 			if (cpu->cd.mips.cpu_type.mmu_model == MMU3K &&
  865| 			    (tmp & 0x3f)!=0) {
  866| 				/* char *symbol;
  867| 				   uint64_t offset;
  868| 				   symbol = get_symbol_name(cpu->pc,
  869| 				    &offset);
  870| 				   fatal("YO! pc = 0x%08llx <%s> "
  871| 				    "hi=%016llx\n", (long long)cpu->pc,
  872| 				    symbol? symbol :
  873| 				    "no symbol", (long long)tmp);  */
  874| 				tmp &= ~0x3f;
  875| 			}
  876| 			if (cpu->cd.mips.cpu_type.mmu_model == MMU3K)
  877| 				tmp &= (R2K3K_ENTRYHI_VPN_MASK |
  878| 				    R2K3K_ENTRYHI_ASID_MASK);
  879| 			else if (cpu->cd.mips.cpu_type.mmu_model == MMU10K)
  880| 				tmp &= (ENTRYHI_R_MASK |
  881| 				    ENTRYHI_VPN2_MASK_R10K | ENTRYHI_ASID);
  882| 			else if (cpu->cd.mips.cpu_type.rev == MIPS_R4100)
  883| 				tmp &= (ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK |
  884| 				    0x1800 | ENTRYHI_ASID);
  885| 			else
  886| 				tmp &= (ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK |
  887| 				    ENTRYHI_ASID);
  888| 			break;
  889| 		case COP0_EPC:
  890| 			unimpl = 0;
  891| 			break;
  892| 		case COP0_PRID:
  893| 			readonly = 1;
  894| 			break;
  895| 		case COP0_CONFIG:
  896| 			if (select > 0) {
  897| 				switch (select) {
  898| 				case 1:	cpu->cd.mips.cop0_config_select1 = tmp;
  899| 					break;
  900| 				default:fatal("[ coproc_register_write(): unimpl"
  901| 					    "emented config register select "
  902| 					    "%i ]\n", select);
  903| 					/*  #213: (Codex/Fable) guest-reachable via mtc0
  904| 					    Config2..7; ignore the write, don't exit().  */
  905| 					break;
  906| 				}
  907| 				return;
  908| 			}
  909| 
  910| 			/*  fatal("COP0_CONFIG: modifying K0 bits: "
  911| 			    "0x%08x => ", cp->reg[reg_nr]);  */
  912| 			tmp = *ptr;
  913| 			tmp &= 0x3;	/*  only bits 2..0 can be written  */
  914| 			cp->reg[reg_nr] &= ~(0x3);  cp->reg[reg_nr] |= tmp;
  915| 			/*  fatal("0x%08x\n", cp->reg[reg_nr]);  */
  916| 			return;
  917| 		case COP0_STATUS:
  918| 			oldmode = cp->reg[COP0_STATUS];
  919| 			tmp &= ~(1 << 21);	/*  bit 21 is read-only  */
  920| 
  921| 			/*
  922| 			 *  When switching between 32-bit and 64-bit address
  923| 			 *  spaces, invalidate all translations.
  924| 			 */
  925| 			if (!cpu->is_32bit &&
  926| 			    (oldmode & (STATUS_KX | STATUS_SX | STATUS_UX)) !=
  927| 			    (tmp & (STATUS_KX | STATUS_SX | STATUS_UX)))
  928| 				cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
  929| 
  930| 			/*
  931| 			 *  When isolating caches, invalidate all translations.
  932| 			 *  During the isolation, a special hack in memory_rw.c
  933| 			 *  prevents translation tables from being updated, so
  934| 			 *  the translation caches don't have to be invalidated
  935| 			 *  when switching back to normal mode.
  936| 			 */
  937| 			if (cpu->cd.mips.cpu_type.mmu_model == MMU3K &&
```

### `src/cpus/cpu_mips.c` around the row's cited line 2165 (HEAD d2a6f233, lines 2120-2210)

```c
 2120| 				if (cpu->cd.mips.cpu_type.mmu_model == MMU10K)
 2121| 					reg[COP0_ENTRYHI] = (vaddr & (ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK_R10K)) | vaddr_asid;
 2122| 				else
 2123| 					reg[COP0_ENTRYHI] = (vaddr & (ENTRYHI_R_MASK | ENTRYHI_VPN2_MASK)) | vaddr_asid;
 2124| 			}
 2125| 		}
 2126| 	}
 2127| 
 2128| 	if (exc_model != EXC3K && reg[COP0_STATUS] & STATUS_EXL) {
 2129| 		/*
 2130| 		 *  Don't set EPC if STATUS_EXL is set, for R4000 and up.
 2131| 		 *  This actually happens when running IRIX and Ultrix, when
 2132| 		 *  they handle interrupts and/or tlb updates, I think, so
 2133| 		 *  printing this with debug() looks better than with fatal().
 2134| 		 */
 2135| 		/*  debug("[ warning: cpu%i exception while EXL is set,"
 2136| 		    " not setting EPC ]\n", cpu->cpu_id);  */
 2137| 	} else {
 2138| 		if (cpu->delay_slot) {
 2139| 			reg[COP0_EPC] = cpu->pc - 4;
 2140| 			reg[COP0_CAUSE] |= CAUSE_BD;
 2141| 		} else {
 2142| 			reg[COP0_EPC] = cpu->pc;
 2143| 			reg[COP0_CAUSE] &= ~CAUSE_BD;
 2144| 		}
 2145| 	}
 2146| 
 2147| 	if (cpu->delay_slot)
 2148| 		cpu->delay_slot = EXCEPTION_IN_DELAY_SLOT;
 2149| 	else
 2150| 		cpu->delay_slot = NOT_DELAYED;
 2151| 
 2152| 	/*  #210: (Codex/Fable) emit the exception on the trappable
 2153| 	    SUBSYS_EXCEPTION channel (MIPS was the only major CPU not doing so)
 2154| 	    with the fault signature now fully set -- lets `break exception`
 2155| 	    stop inside the TLB-miss path that the -p PC breakpoint cannot
 2156| 	    reach. Cheap: debugmsg early-returns when nothing is armed.  */
 2157| 	debugmsg_cpu(cpu, SUBSYS_EXCEPTION, exception_names[exccode],
 2158| 	    (exccode == EXCEPTION_ADEL || exccode == EXCEPTION_ADES ||
 2159| 	     exccode == EXCEPTION_RI || exccode == EXCEPTION_CPU)?
 2160| 	    VERBOSITY_WARNING : VERBOSITY_DEBUG,
 2161| 	    "epc=0x%" PRIx64 " vaddr=0x%" PRIx64 " cause=0x%" PRIx64,
 2162| 	    (uint64_t)reg[COP0_EPC], (uint64_t)vaddr, (uint64_t)reg[COP0_CAUSE]);
 2163| 
 2164| 	/*  TODO: This is true for MIPS64, but how about others?  */
 2165| 	if (reg[COP0_STATUS] & STATUS_BEV)
 2166| 		base = 0xffffffffbfc00200ULL;
 2167| 	else
 2168| 		base = 0xffffffff80000000ULL;
 2169| 
 2170| 	switch (exc_model) {
 2171| 	case EXC3K:
 2172| 		/*  Userspace tlb, vs others:  */
 2173| 		if (tlb && !(vaddr & 0x80000000ULL) &&
 2174| 		    (exccode == EXCEPTION_TLBL || exccode == EXCEPTION_TLBS) )
 2175| 			cpu->pc = base + 0x000;
 2176| 		else
 2177| 			cpu->pc = base + 0x080;
 2178| 		break;
 2179| 	default:
 2180| 		/*
 2181| 		 *  These offsets are according to the MIPS64 manual, but
 2182| 		 *  should work with R4000 and the rest too (I hope).
 2183| 		 *
 2184| 		 *  0x000  TLB refill, if EXL=0
 2185| 		 *  0x080  64-bit XTLB refill, if EXL=0
 2186| 		 *  0x100  cache error  (not implemented yet)
 2187| 		 *  0x180  general exception
 2188| 		 *  0x200  interrupt (if CAUSE_IV is set)
 2189| 		 */
 2190| 		if (tlb && (exccode == EXCEPTION_TLBL ||
 2191| 		    exccode == EXCEPTION_TLBS) &&
 2192| 		    !(reg[COP0_STATUS] & STATUS_EXL)) {
 2193| 			if (x_64)
 2194| 				cpu->pc = base + 0x080;
 2195| 			else
 2196| 				cpu->pc = base + 0x000;
 2197| 		} else {
 2198| 			if (exccode == EXCEPTION_INT &&
 2199| 			    (reg[COP0_CAUSE] & CAUSE_IV))
 2200| 				cpu->pc = base + 0x200;
 2201| 			else
 2202| 				cpu->pc = base + 0x180;
 2203| 		}
 2204| 	}
 2205| 
 2206| 	if (exc_model == EXC3K) {
 2207| 		/*  R{2,3}000:  Shift the lowest 6 bits to the left two steps:*/
 2208| 		reg[COP0_STATUS] = (reg[COP0_STATUS] & ~0x3f) +
 2209| 		    ((reg[COP0_STATUS] & 0xf) << 2);
 2210| 	} else {
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

End with one line: `FIXDRAFT_MIPSEBASE: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
