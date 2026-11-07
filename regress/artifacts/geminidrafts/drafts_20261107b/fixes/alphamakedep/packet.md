# GXemul hardened fork -- DRAFT A FIX for one filed issue, `alphamakedep` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `alphamakedep`, state `open`, severity `LOW`)

**title:** cpus/Makefile.skel -- cpu_alpha.o lacks a dependency on the generated tmp_alpha_misc.c -- HYGIENE/BUILD

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T146 (class HYGIENE/BUILD; reach B, build only; effort: one-line; report rows: A1-6, C U18).  Source URLs: https://github.com/retroprom/gxemul/commit/587f438a, https://sourceforge.net/p/gxemul/code2/HEAD/log/.  Our site at de8c7547: src/cpus/Makefile.skel:24-25; src/cpus/cpu_alpha_instr.c:742.  Portable fix: yes -- port upstream 587f438a (SVN r6531).  Filing check (TRIAGE.md): bears on `depsrm`.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- one-line build dependency port.

## The code at the cited lines

### `src/cpus/cpu_alpha_instr.c` around the row's cited line 742 (HEAD 8d9df658, lines 622-862)

```c
  622|  *  arg[2] = pointer to source uint64_t or immediate
  623|  */
  624| X(mull)
  625| {
  626| 	int32_t a = reg(ic->arg[1]);
  627| 	int32_t b = reg(ic->arg[2]);
  628| 	reg(ic->arg[0]) = (int64_t)(int32_t)(a * b);
  629| }
  630| X(mull_imm)
  631| {
  632| 	int32_t a = reg(ic->arg[1]);
  633| 	int32_t b = ic->arg[2];
  634| 	reg(ic->arg[0]) = (int64_t)(int32_t)(a * b);
  635| }
  636| 
  637| 
  638| /*
  639|  *  mulq, mulq_imm:  Unsigned Multiply 64x64 => 64.
  640|  *
  641|  *  arg[0] = pointer to destination uint64_t
  642|  *  arg[1] = pointer to source uint64_t
  643|  *  arg[2] = pointer to source uint64_t or immediate
  644|  */
  645| X(mulq)
  646| {
  647| 	reg(ic->arg[0]) = reg(ic->arg[1]) * reg(ic->arg[2]);
  648| }
  649| X(mulq_imm)
  650| {
  651| 	reg(ic->arg[0]) = reg(ic->arg[1]) * ic->arg[2];
  652| }
  653| 
  654| 
  655| /*
  656|  *  umulh:  Unsigned Multiply 64x64 => 128. Store high part in dest reg.
  657|  *
  658|  *  arg[0] = pointer to destination uint64_t
  659|  *  arg[1] = pointer to source uint64_t
  660|  *  arg[2] = pointer to source uint64_t
  661|  */
  662| X(umulh)
  663| {
  664| 	uint64_t reshi = 0, reslo = 0;
  665| 	uint64_t s1 = reg(ic->arg[1]), s2 = reg(ic->arg[2]);
  666| 	int i, bit;
  667| 
  668| 	for (i=0; i<64; i++) {
  669| 		bit = (s1 & 0x8000000000000000ULL)? 1 : 0;
  670| 		s1 <<= 1;
  671| 
  672| 		/*  If bit in s1 set, then add s2 to reshi/lo:  */
  673| 		if (bit) {
  674| 			uint64_t old_reslo = reslo;
  675| 			reslo += s2;
  676| 			if (reslo < old_reslo)
  677| 				reshi ++;
  678| 		}
  679| 
  680| 		if (i != 63) {
  681| 			reshi <<= 1;
  682| 			reshi += (reslo & 0x8000000000000000ULL? 1 : 0);
  683| 			reslo <<= 1;
  684| 		}
  685| 	}
  686| 
  687| 	reg(ic->arg[0]) = reshi;
  688| }
  689| 
  690| 
  691| /*
  692|  *  lda:  Load address.
  693|  *
  694|  *  arg[0] = pointer to destination uint64_t
  695|  *  arg[1] = pointer to source uint64_t
  696|  *  arg[2] = offset (possibly as an int32_t)
  697|  */
  698| X(lda)
  699| {
  700| 	reg(ic->arg[0]) = reg(ic->arg[1]) + (int64_t)(int32_t)ic->arg[2];
  701| }
  702| 
  703| 
  704| /*
  705|  *  lda_0:  Load address compared to the zero register.
  706|  *
  707|  *  arg[0] = pointer to destination uint64_t
  708|  *  arg[1] = ignored
  709|  *  arg[2] = offset (possibly as an int32_t)
  710|  */
  711| X(lda_0)
  712| {
  713| 	reg(ic->arg[0]) = (int64_t)(int32_t)ic->arg[2];
  714| }
  715| 
  716| 
  717| /*
  718|  *  clear:  Clear a 64-bit register.
  719|  *
  720|  *  arg[0] = pointer to destination uint64_t
  721|  */
  722| X(clear)
  723| {
  724| 	reg(ic->arg[0]) = 0;
  725| }
  726| 
  727| 
  728| /*
  729|  *  rdcc:  Read the Cycle Counter into a 64-bit register.
  730|  *
  731|  *  arg[0] = pointer to destination uint64_t
  732|  */
  733| X(rdcc)
  734| {
  735| 	reg(ic->arg[0]) = cpu->cd.alpha.pcc;
  736| 
  737| 	/*  TODO: actually keep the pcc updated!  */
  738| 	cpu->cd.alpha.pcc += 20;
  739| }
  740| 
  741| 
  742| #include "tmp_alpha_misc.c"
  743| 
  744| 
  745| /*****************************************************************************/
  746| 
  747| 
  748| X(end_of_page)
  749| {
  750| 	/*  Update the PC:  (offset 0, but on the next page)  */
  751| 	cpu->pc &= ~((ALPHA_IC_ENTRIES_PER_PAGE-1)
  752| 	    << ALPHA_INSTR_ALIGNMENT_SHIFT);
  753| 	cpu->pc += (ALPHA_IC_ENTRIES_PER_PAGE
  754| 	    << ALPHA_INSTR_ALIGNMENT_SHIFT);
  755| 
  756| 	/*  Find the new physical page and update the translation pointers:  */
  757| 	alpha_pc_to_pointers(cpu);
  758| 
  759| 	/*  end_of_page doesn't count as an executed instruction:  */
  760| 	cpu->n_translated_instrs --;
  761| }
  762| 
  763| 
  764| /*****************************************************************************/
  765| 
  766| 
  767| /*
  768|  *  alpha_instr_to_be_translated():
  769|  *
  770|  *  Translate an instruction word into an alpha_instr_call. ic is filled in with
  771|  *  valid data for the translated instruction, or a "nothing" instruction if
  772|  *  there was a translation failure. The newly translated instruction is then
  773|  *  executed.
  774|  */
  775| X(to_be_translated)
  776| {
  777| 	uint64_t addr, low_pc;
  778| 	uint32_t iword;
  779| 	unsigned char *page;
  780| 	unsigned char ib[4];
  781| 	void (*samepage_function)(struct cpu *, struct alpha_instr_call *);
  782| 	int opcode, ra, rb, func, rc, imm, load, loadstore_type, fp, llsc;
  783| 
  784| 	/*  Figure out the (virtual) address of the instruction:  */
  785| 	low_pc = ((size_t)ic - (size_t)cpu->cd.alpha.cur_ic_page)
  786| 	    / sizeof(struct alpha_instr_call);
  787| 	addr = cpu->pc & ~((ALPHA_IC_ENTRIES_PER_PAGE-1) <<
  788| 	    ALPHA_INSTR_ALIGNMENT_SHIFT);
  789| 	addr += (low_pc << ALPHA_INSTR_ALIGNMENT_SHIFT);
  790| 	addr &= ~((1 << ALPHA_INSTR_ALIGNMENT_SHIFT) - 1);
  791| 	cpu->pc = addr;
  792| 
  793| 	/*  Read the instruction word from memory:  */
  794| 	{
  795| 		const uint32_t mask1 = (1 << DYNTRANS_L1N) - 1;
  796| 		const uint32_t mask2 = (1 << DYNTRANS_L2N) - 1;
  797| 		const uint32_t mask3 = (1 << DYNTRANS_L3N) - 1;
  798| 		uint32_t x1 = (addr >> (64-DYNTRANS_L1N)) & mask1;
  799| 		uint32_t x2 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N)) & mask2;
  800| 		uint32_t x3 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N-
  801| 		    DYNTRANS_L3N)) & mask3;
  802| 		struct DYNTRANS_L2_64_TABLE *l2 = cpu->cd.alpha.l1_64[x1];
  803| 		struct DYNTRANS_L3_64_TABLE *l3 = l2->l3[x2];
  804| 		page = l3->host_load[x3];
  805| 	}
  806| 
  807| 	if (page != NULL) {
  808| 		/*  fatal("TRANSLATION HIT!\n");  */
  809| 		memcpy(ib, page + (addr & 8191), sizeof(ib));
  810| 	} else {
  811| 		/*  fatal("TRANSLATION MISS!\n");  */
  812| 		if (!cpu->memory_rw(cpu, cpu->mem, addr, &ib[0],
  813| 		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
  814| 			fatal("to_be_translated(): read failed: TODO\n");
  815| 			goto bad;
  816| 		}
  817| 	}
  818| 
  819| 	/*  Alpha instruction words are always little-endian. Convert
  820| 	    to host order:  */
  821| 	{
  822| 		uint32_t *p = (uint32_t *) ib;
  823| 		iword = LE32_TO_HOST( *p );
  824| 	}
  825| 
  826| #define DYNTRANS_TO_BE_TRANSLATED_HEAD
  827| #include "cpu_dyntrans.c"
  828| #undef	DYNTRANS_TO_BE_TRANSLATED_HEAD
  829| 
  830| 
  831| 	opcode = (iword >> 26) & 63;
  832| 	ra = (iword >> 21) & 31;
  833| 	rb = (iword >> 16) & 31;
  834| 	func = (iword >> 5) & 0x7ff;
  835| 	rc = iword & 31;
  836| 	imm = iword & 0xffff;
  837| 
  838| 	switch (opcode) {
  839| 	case 0x00:						/*  CALL_PAL  */
  840| 		ic->f = instr(call_pal);
  841| 		ic->arg[0] = (size_t) (iword & 0x3ffffff);
  842| 		break;
  843| 	case 0x08:						/*  LDA  */
  844| 	case 0x09:						/*  LDAH  */
  845| 		if (ra == ALPHA_ZERO) {
  846| 			ic->f = instr(nop);
  847| 			break;
  848| 		}
  849| 		/*  TODO: A special case which is common is to add or subtract
  850| 		    a small offset from sp.  */
  851| 		ic->f = instr(lda);
  852| 		ic->arg[0] = (size_t) &cpu->cd.alpha.r[ra];
  853| 		ic->arg[1] = (size_t) &cpu->cd.alpha.r[rb];
  854| 		if (rb == ALPHA_ZERO)
  855| 			ic->f = instr(lda_0);
  856| 		ic->arg[2] = (ssize_t)(int16_t)imm;
  857| 		if (opcode == 0x09)
  858| 			ic->arg[2] <<= 16;
  859| 		break;
  860| 	case 0x0b:						/*  LDQ_U  */
  861| 	case 0x0f:						/*  STQ_U  */
  862| 		if (ra == ALPHA_ZERO && opcode == 0x0b) {
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

End with one line: `FIXDRAFT_ALPHAMAKEDEP: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
