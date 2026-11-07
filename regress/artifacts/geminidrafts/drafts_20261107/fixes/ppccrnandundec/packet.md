# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ppccrnandundec` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ppccrnandundec`, state `open`, severity `MED`)

**title:** cpus/cpu_ppc_instr.c XL decode -- crnand (19/225) is defined but missing from the CR case list -- CPU-STOP

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T124 (class CPU-STOP; reach U, user mode; effort: one-line; report rows: A4-9).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/2ec64fdde77aa73187fd80592679ea3f44e46fa2.  Our site at de8c7547: src/cpus/cpu_ppc_instr.c:4512-4531 (lines of de8c7547; at 987cb596 :4541-4560).  Portable fix: yes -- port rs6000 2ec64fd.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.  | 2026-11-05 (#575): X(crandc) now computes `ba & !bb` (Book I).  #575's pass-1 ruling notes for this round (adj_p1_20261105/MYTHOS_local.md, section 4): the draft here sketches `!(ba & bb)` as the crnand body -- the OLD crandc -- so crnand needs its own handler and must not alias `instr(crandc)`.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Port available from rs6000 2ec64fd

## The code at the cited lines

### `src/cpus/cpu_ppc_instr.c` around the row's cited line 4512 (HEAD d2a6f233, lines 4467-4557)

```c
 4467| 		else
 4468| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
 4469| 		ic->arg[2] = (ssize_t)imm;
 4470| 		break;
 4471| 
 4472| 	case PPC_HI6_BC:
 4473| 		aa_bit = (iword >> 1) & 1;
 4474| 		lk_bit = iword & 1;
 4475| 		bo = (iword >> 21) & 31;
 4476| 		bi = (iword >> 16) & 31;
 4477| 		tmp_addr = (int64_t)(int16_t)(iword & 0xfffc);
 4478| 		if (aa_bit) {
 4479| 			if (!cpu->translation_readahead)
 4480| 				fatal("aa_bit: NOT YET\n");
 4481| 			goto bad;
 4482| 		}
 4483| 		if (lk_bit) {
 4484| 			ic->f = instr(bcl);
 4485| 			samepage_function = instr(bcl_samepage);
 4486| 		} else {
 4487| 			ic->f = instr(bc);
 4488| 			if ((bo & 0x14) == 0x04) {
 4489| 				samepage_function = bo & 8?
 4490| 				    instr(bc_samepage_simple1) :
 4491| 				    instr(bc_samepage_simple0);
 4492| 			} else
 4493| 				samepage_function = instr(bc_samepage);
 4494| 		}
 4495| 		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
 4496| 		ic->arg[1] = bo;
 4497| 		ic->arg[2] = 31-bi;
 4498| 		/*  Branches are calculated as cur PC + offset.  */
 4499| 		/*  Special case: branch within the same page:  */
 4500| 		{
 4501| 			uint64_t mask_within_page =
 4502| 			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
 4503| 			uint64_t old_pc = addr;
 4504| 			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
 4505| 			if ((old_pc & ~mask_within_page) ==
 4506| 			    (new_pc & ~mask_within_page)) {
 4507| 				ic->f = samepage_function;
 4508| 				ic->arg[0] = (size_t) (
 4509| 				    cpu->cd.ppc.cur_ic_page +
 4510| 				    ((new_pc & mask_within_page) >> 2));
 4511| 			}
 4512| 		}
 4513| 		break;
 4514| 
 4515| 	case PPC_HI6_SC:
 4516| 		ic->arg[0] = (iword >> 5) & 0x7f;
 4517| 		ic->arg[1] = (addr & 0xfff) + 4;
 4518| 		if (iword == 0x44ee0002) {
 4519| 			/*  Special case/magic hack for OpenFirmware emul:  */
 4520| 			ic->f = instr(openfirmware);
 4521| 		} else
 4522| 			ic->f = instr(sc);
 4523| 		break;
 4524| 
 4525| 	case PPC_HI6_B:
 4526| 		aa_bit = (iword & 2) >> 1;
 4527| 		lk_bit = iword & 1;
 4528| 		tmp_addr = (int64_t)(int32_t)((iword & 0x03fffffc) << 6);
 4529| 		tmp_addr = (int64_t)tmp_addr >> 6;
 4530| 		if (lk_bit) {
 4531| 			if (cpu->machine->show_trace_tree) {
 4532| 				ic->f = instr(bl_trace);
 4533| 				samepage_function = instr(bl_samepage_trace);
 4534| 			} else {
 4535| 				ic->f = instr(bl);
 4536| 				samepage_function = instr(bl_samepage);
 4537| 			}
 4538| 		} else {
 4539| 			ic->f = instr(b);
 4540| 			samepage_function = instr(b_samepage);
 4541| 		}
 4542| 		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
 4543| 		ic->arg[1] = (addr & 0xffc) + 4;
 4544| 		/*  Branches are calculated as cur PC + offset.  */
 4545| 		/*  Special case: branch within the same page:  */
 4546| 		{
 4547| 			uint64_t mask_within_page =
 4548| 			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
 4549| 			uint64_t old_pc = addr;
 4550| 			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
 4551| 			if ((old_pc & ~mask_within_page) ==
 4552| 			    (new_pc & ~mask_within_page)) {
 4553| 				ic->f = samepage_function;
 4554| 				ic->arg[0] = (size_t) (
 4555| 				    cpu->cd.ppc.cur_ic_page +
 4556| 				    ((new_pc & mask_within_page) >> 2));
 4557| 			}
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

End with one line: `FIXDRAFT_PPCCRNANDUNDEC: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
