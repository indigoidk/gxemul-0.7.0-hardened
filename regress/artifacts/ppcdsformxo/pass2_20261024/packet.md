# PASS-2 DIFF REVIEW -- round #571, ledger row `ppcdsformxo` (research item T2) -- GXemul hardened fork

**Brief v1, FULL form -- for the seats that can read files (GPT-6 Astra, Grok 4.7); it is the AUTHORITY for the COMPACT and
PACKET forms.**  Drafted 2026-10-24 09:47 -0500 by an Opus 5.5 drafting sub-agent, read-only.  Tree under review: `GXEMUL-SEC/` at HEAD
`add098b9` (a RECORDS-ONLY commit on top of `c8fcb5ff`; no commit between them touches `src/` -- C0) PLUS this round's
uncommitted working-tree edits (section 0 names every dirty file).  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md`
(§A opener, §B anchors, §C0, §C settled premises, §C2-§C5, §C6 clause-(c) forms, §D enclosing code, §E questions, §F
pass-2 numstat).  Sections 6, 7 and 11 are byte-identical in all three forms.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

---

## 0. What this is, what this pass is for, and how to answer

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems inside a
software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's own C code and
the regression tests that keep each correction fixed.  The *guest* is a program running INSIDE the emulator; the *host* is
the emulator process.  A *leg* (or *variant*) is a deliberately altered copy of the code, built only to measure whether a
regression test notices the alteration (standard mutation testing).  The records quoted VERBATIM below use that
discipline's shorthand: a row that "kills" a leg is a row that turns red under it (it detects the alteration), and the
"kill table" is the table of legs.

**The defect and the fix, in one paragraph.**  On the 64-bit PowerPC CPU this tree models (PPC970, the default CPU of the
in-tree `bareppc`/`testppc` machines) the decoder treated primary opcode 58 as ONE instruction (`ld`, an 8-byte load) and 62
as ONE instruction (`std`), and took the displacement from the word's whole low halfword.  In the architecture these are
DS-form opcodes: the two lowest bits are an extended opcode (XO) selecting `ld`/`ldu`/`lwa` (58) or `std`/`stdu` (62), and
the displacement is DS || 0b00.  So `ldu` loaded from EA+1 and left RA alone, `lwa` loaded a doubleword from EA+2, `stdu`
stored at EA+1 and left RA alone, and the reserved encodings executed -- all MEASURED red on the committed decode (section
4).  The fix re-decodes the two case bodies (section 1).  Guest-visible wrong loads and misdirected stores; the product
change ends no emulator process anywhere.

**This pass.**  PASS 2 reviews the SHIPPED material -- the product diff, the detector, the table of variant legs, the gate block, the
records -- against pass 1's rulings.  The repair, the detector, the table, the two-part clearance and gate 13 are DONE and
MEASURED (section 4); nothing is committed (section 5).  Section 6 re-inlines the settled rulings.  Section 7 lists
discrepancies the drafter found while reading the records, AS QUESTIONS.  Section 11 asks Q1-Q4.

**Hard limits.**  READ-ONLY: do not build, run, copy or modify anything.  Nobody is asked for code, a diff, a variant or a
guest program.  Where a question concerns what the rows might not see, it asks which INPUT CELLS are observed and which are
not, and asks you to describe cells in words.

**Reading scope (seats that can read files).**  `GXEMUL-SEC/src/`; the top-level `GXEMUL-SEC/regress/*.py` and `*.sh`;
`GXEMUL-SEC/tools/precommit_check.sh` and `GXEMUL-SEC/tools/pipeline/check_score_claims.py`;
`GXEMUL-SEC/tools/pipeline/check_probe_wiring.py` AT HEAD (`git -C GXEMUL-SEC show HEAD:tools/pipeline/check_probe_wiring.py`)
plus its staged copy; and under `GXEMUL-SEC/regress/artifacts/ppcdsformxo/` ONLY the files section 12 lists (the frozen
witness, `PASS1_RULINGS.md`, `BUILD_SPEC.md`, and table1's measurement and record files).  **Do not open anything else
in `pass2_20261024/` (this brief aside: the other seats' answers to it land there), the pass-1 seat answer files and packets, table1's
per-leg variant files (`L*.diff`) or session transcripts (`RAW_*.txt`), or `tools/pipeline/ledger.json`.**  What a question
needs from them is inlined.  Outside the repository, by ABSOLUTE path:
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\ppc_uisa_book1_v201.txt` (PowerPC Book I v2.01) and
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\ppc_pem_32and64_2005.txt` (the 2005 Programming Environments Manual).

**The working tree is not clean -- these are the files, so a reader in plan mode can re-derive line numbers** (C0 part 5,
each `git ls-files -m` hit confirmed by `cmp` against `git show HEAD:<path>`):
* THIS ROUND's five, uncommitted -- line numbers in this brief are the WORKING TREE's for these:
  `src/cpus/cpu_ppc_instr.c` (+31 -2), `regress/ppc_dsform_probe.py` (NEW, untracked), `regress/gate_ppc.sh` (+39),
  `tools/pipeline/check_probe_wiring.py` (+2 MANIFEST keys; the working tree ALSO carries 15 uncommitted lines of a peer's --
  read it at HEAD plus the staged copy), `tools/precommit_check.sh` (+3 -1); and the untracked `regress/artifacts/ppcdsformxo/`.
* OTHER sessions' uncommitted edits, none on the PowerPC path: `regress/artifacts/recordfix_20261002/chk_hrec.py.txt`,
  `regress/diff_wdc_identify.c`, `regress/gate_offline.sh`, `regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`,
  `regress/sh4_chcr_probe.py`, `regress/wdc_addtoinbuf_probe.py`, `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`,
  `src/devices/dev_pcc2.c`, `src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`, `tools/BRIEF_TEMPLATE.md`,
  `tools/CLAUDE.md`, `tools/PIPELINE.md`, `tools/adjudicate.sh`, `tools/panel.sh`, `tools/pipeline/ledger.json`,
  `tools/pipeline/matrix.html` (and the 15 peer lines in `check_probe_wiring.py`).
* Every other file this brief cites is byte-identical at HEAD and in the working tree (`LS_PERMITTED.txt`, section 12).  If
  your line numbers disagree with this brief, say so rather than reconciling.

**The roster for this pass** (owner roster of 2026-10-23/24), so that a missing answer is read as what it is:

| seat | transport | class | packet |
|---|---|---|---|
| GPT-6 Astra | codex, pointer form | FILE-READING | FULL; reviews this pass, then ADJUDICATES the consolidated findings |
| Grok 4.7 (xhigh, plan mode) | `grok --prompt-file` | FILE-READING | FULL |
| Gemini 4 Argon (`gemini-4-argon-high`) | agy, `--add-dir GXEMUL-SEC` | FILE-READING | COMPACT (one Gemini-family lens) |
| GLM 5.3 (`glm-5.3:cloud`) | Ollama cloud | PACKET-FED | PACKET, two firings: Q1+Q2, then Q3+Q4 |
| DeepSeek (`deepseek-v4-pro:cloud`) | Ollama cloud | PACKET-FED | PACKET, two firings: Q1+Q2, then Q3+Q4 |
| Fable 5.1 | -- | HELD | the owner's Fable hold; its question is `pass2_20261024/fable5.HELD.txt` |
| kimi, minimax | -- | NOT FIRED | not on this roster |
| Opus 5.5 | -- | NOT FIRED as a review seat | this round's writing / measuring sub-agents (it wrote the detector), and this brief's drafter |

A seat that does not answer is a SEAT FAILURE; a seat deliberately not fired is neither a failure nor agreement.  **The
answer format is at the head of section 11.**

---

## 1. The product change -- the diff VERBATIM, the arm after the edit, and the code it falls into

### 1.1 The round's files (template §F: the `git diff --numstat` item, computed with GNU `diff` against `git show HEAD:<path>` -- no `git diff` was run, by the read-only rule)

| file | change | in this brief |
|---|---|---|
| `src/cpus/cpu_ppc_instr.c` | +31 -2, two hunks | INLINED: 1.2 (the diff), 1.3 (the arm after the edit) |
| `regress/ppc_dsform_probe.py` | +836, new, untracked | INLINED in part (section 2: the contract, the tables, `row()`, the session programs, the stop-row scoring, the summary); the helper functions SUMMARIZED -- the file is on the reading list |
| `regress/gate_ppc.sh` | +39 -0 | INLINED: 3.1 |
| `tools/pipeline/check_probe_wiring.py` | +2 -0 this round (the working tree also carries +15 peer lines that are NOT this round's) | INLINED: 3.2 (both insertions, into the HEAD-blob staged copy and into the working tree) |
| `tools/precommit_check.sh` | +3 -1 | INLINED: 3.3 |
| `regress/artifacts/ppcdsformxo/**` (witness_20261024/, pass1_20261024/, table1_20261024/, pass2_20261024/) | new, untracked | SUMMARIZED: section 4 inlines the measurements; the per-leg variant files (`L*.diff`) and the session transcripts (`RAW_*.txt`) are NOT SHOWN -- outside this review's reading scope |
| `CHANGELOG.md`, `OUTSTANDING_BUGS.md`, `tools/pipeline/ledger.json`, `regress/pass2_ledger.tsv` | not yet edited for `#571` | the landing commit's records: the CHANGELOG round-block DRAFT, the witness-term draft and the filing drafts are frozen into section 9 |

### 1.2 The product diff, VERBATIM (`diff_cpu_ppc_instr.patch`; applied by `patch` to the HEAD blob it reproduces the working-tree file byte for byte -- checked at drafting)

~~~~
diff --git a/src/cpus/cpu_ppc_instr.c b/src/cpus/cpu_ppc_instr.c
index 44565840..23b47a81 100644
--- a/src/cpus/cpu_ppc_instr.c
+++ b/src/cpus/cpu_ppc_instr.c
@@ -4304,7 +4304,26 @@ X(to_be_translated)
 		case PPC_HI6_LHZU: load=1; size=1; update=1; break;
 		case PPC_HI6_LWZ:  load=1; size=2; break;
 		case PPC_HI6_LWZU: load=1; size=2; update=1; break;
-		case PPC_HI6_LD:   load=1; size=3; break;
+		case PPC_HI6_LD:
+			/*  #571: DS form -- bits 30:31 are XO, the displacement is
+			    DS || 0b00.  The committed decode kept XO in the displacement
+			    and gave every XO the ld flags, so ldu/lwa ran as ld at
+			    EA+1/EA+2 with no update.  One masked imm feeds both the
+			    table index (imm==0) and ic->arg[2] below.  Reserved XO 3
+			    takes the arm's bare goto bad (the common tail announces it);
+			    ldu with RA=0 now reaches the existing ra==0 && update guard.
+			    Opcodes 58/62 are illegal on 32-bit implementations; the same
+			    source builds the MODE32 decoder and no width test is added
+			    here (disclosed).  The shared imm assignment above is unchanged.  */
+			imm = (int16_t)(iword & ~3);
+			load = 1; size = 3;
+			switch (iword & 3) {
+			case 0:	break;			/*  ld  */
+			case 1:	update = 1; break;	/*  ldu: RA <- EA  */
+			case 2:	size = 2; zero = 0; break;	/*  lwa: sign-extended word  */
+			default: goto bad;		/*  reserved encoding  */
+			}
+			break;
 		case PPC_HI6_LFD:  load=1; size=3; fp=1;ic->f=instr(lfd);break;
 		case PPC_HI6_LFDU: load=1; size=3; fp=1; update=1;
 				   ic->f=instr(lfdu); break;	/*  #310  */
@@ -4317,7 +4336,17 @@ X(to_be_translated)
 		case PPC_HI6_STHU: size=1; update=1; break;
 		case PPC_HI6_STW:  size=2; break;
 		case PPC_HI6_STWU: size=2; update=1; break;
-		case PPC_HI6_STD:  size=3; break;
+		case PPC_HI6_STD:
+			/*  #571: DS form, as for PPC_HI6_LD above: stdu ran as std at
+			    EA+1 with no update; XO 2 and 3 are reserved.  */
+			imm = (int16_t)(iword & ~3);
+			size = 3;
+			switch (iword & 3) {
+			case 0:	break;			/*  std  */
+			case 1:	update = 1; break;	/*  stdu: RA <- EA  */
+			default: goto bad;		/*  reserved encodings  */
+			}
+			break;
 		case PPC_HI6_STFD: size=3; fp=1; ic->f = instr(stfd); break;
 		case PPC_HI6_STFDU: size=3; fp=1; update=1;
 				   ic->f = instr(stfdu); break;	/*  #310  */
~~~~

### 1.3 The whole arm AFTER the edit -- `src/cpus/cpu_ppc_instr.c` :4269-4381 (working tree), VERBATIM

The 24 labels, the shared assignment, the inner switch with the two edited case bodies, and the common part every case
falls into: the table lookup, the `ra == 0 && update` guard, the argument assignments.

~~~~
4269| 	case PPC_HI6_LBZ:
4270| 	case PPC_HI6_LBZU:
4271| 	case PPC_HI6_LHZ:
4272| 	case PPC_HI6_LHZU:
4273| 	case PPC_HI6_LHA:
4274| 	case PPC_HI6_LHAU:
4275| 	case PPC_HI6_LWZ:
4276| 	case PPC_HI6_LWZU:
4277| 	case PPC_HI6_LD:
4278| 	case PPC_HI6_LFD:
4279| 	case PPC_HI6_LFDU:	/*  #310  */
4280| 	case PPC_HI6_LFS:
4281| 	case PPC_HI6_LFSU:	/*  #310  */
4282| 	case PPC_HI6_STB:
4283| 	case PPC_HI6_STBU:
4284| 	case PPC_HI6_STH:
4285| 	case PPC_HI6_STHU:
4286| 	case PPC_HI6_STW:
4287| 	case PPC_HI6_STWU:
4288| 	case PPC_HI6_STD:
4289| 	case PPC_HI6_STFD:
4290| 	case PPC_HI6_STFDU:	/*  #310  */
4291| 	case PPC_HI6_STFS:
4292| 	case PPC_HI6_STFSU:	/*  #310  */
4293| 		rs = (iword >> 21) & 31;
4294| 		ra = (iword >> 16) & 31;
4295| 		imm = (int16_t)iword;
4296| 		load = 0; zero = 1; size = 0; update = 0; fp = 0;
4297| 		ic->f = NULL;
4298| 		switch (main_opcode) {
4299| 		case PPC_HI6_LBZ:  load=1; break;
4300| 		case PPC_HI6_LBZU: load=1; update=1; break;
4301| 		case PPC_HI6_LHA:  load=1; size=1; zero=0; break;
4302| 		case PPC_HI6_LHAU: load=1; size=1; zero=0; update=1; break;
4303| 		case PPC_HI6_LHZ:  load=1; size=1; break;
4304| 		case PPC_HI6_LHZU: load=1; size=1; update=1; break;
4305| 		case PPC_HI6_LWZ:  load=1; size=2; break;
4306| 		case PPC_HI6_LWZU: load=1; size=2; update=1; break;
4307| 		case PPC_HI6_LD:
4308| 			/*  #571: DS form -- bits 30:31 are XO, the displacement is
4309| 			    DS || 0b00.  The committed decode kept XO in the displacement
4310| 			    and gave every XO the ld flags, so ldu/lwa ran as ld at
4311| 			    EA+1/EA+2 with no update.  One masked imm feeds both the
4312| 			    table index (imm==0) and ic->arg[2] below.  Reserved XO 3
4313| 			    takes the arm's bare goto bad (the common tail announces it);
4314| 			    ldu with RA=0 now reaches the existing ra==0 && update guard.
4315| 			    Opcodes 58/62 are illegal on 32-bit implementations; the same
4316| 			    source builds the MODE32 decoder and no width test is added
4317| 			    here (disclosed).  The shared imm assignment above is unchanged.  */
4318| 			imm = (int16_t)(iword & ~3);
4319| 			load = 1; size = 3;
4320| 			switch (iword & 3) {
4321| 			case 0:	break;			/*  ld  */
4322| 			case 1:	update = 1; break;	/*  ldu: RA <- EA  */
4323| 			case 2:	size = 2; zero = 0; break;	/*  lwa: sign-extended word  */
4324| 			default: goto bad;		/*  reserved encoding  */
4325| 			}
4326| 			break;
4327| 		case PPC_HI6_LFD:  load=1; size=3; fp=1;ic->f=instr(lfd);break;
4328| 		case PPC_HI6_LFDU: load=1; size=3; fp=1; update=1;
4329| 				   ic->f=instr(lfdu); break;	/*  #310  */
4330| 		case PPC_HI6_LFS:  load=1; size=2; fp=1;ic->f=instr(lfs);break;
4331| 		case PPC_HI6_LFSU: load=1; size=2; fp=1; update=1;
4332| 				   ic->f=instr(lfsu); break;	/*  #310  */
4333| 		case PPC_HI6_STB:  break;
4334| 		case PPC_HI6_STBU: update=1; break;
4335| 		case PPC_HI6_STH:  size=1; break;
4336| 		case PPC_HI6_STHU: size=1; update=1; break;
4337| 		case PPC_HI6_STW:  size=2; break;
4338| 		case PPC_HI6_STWU: size=2; update=1; break;
4339| 		case PPC_HI6_STD:
4340| 			/*  #571: DS form, as for PPC_HI6_LD above: stdu ran as std at
4341| 			    EA+1 with no update; XO 2 and 3 are reserved.  */
4342| 			imm = (int16_t)(iword & ~3);
4343| 			size = 3;
4344| 			switch (iword & 3) {
4345| 			case 0:	break;			/*  std  */
4346| 			case 1:	update = 1; break;	/*  stdu: RA <- EA  */
4347| 			default: goto bad;		/*  reserved encodings  */
4348| 			}
4349| 			break;
4350| 		case PPC_HI6_STFD: size=3; fp=1; ic->f = instr(stfd); break;
4351| 		case PPC_HI6_STFDU: size=3; fp=1; update=1;
4352| 				   ic->f = instr(stfdu); break;	/*  #310  */
4353| 		case PPC_HI6_STFS: size=2; fp=1; ic->f = instr(stfs); break;
4354| 		case PPC_HI6_STFSU: size=2; fp=1; update=1;
4355| 				   ic->f = instr(stfsu); break;	/*  #310  */
4356| 		}
4357| 		if (ic->f == NULL) {
4358| 			ic->f =
4359| #ifdef MODE32
4360| 			    ppc32_loadstore
4361| #else
4362| 			    ppc_loadstore
4363| #endif
4364| 			    [size + 4*zero + 8*load + (imm==0? 16 : 0)
4365| 			    + 32*update];
4366| 		}
4367| 		if (ra == 0 && update) {
4368| 			if (!cpu->translation_readahead)
4369| 				fatal("TODO: ra=0 && update?\n");
4370| 			goto bad;
4371| 		}
4372| 		if (fp)
4373| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rs]);
4374| 		else
4375| 			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
4376| 		if (ra == 0)
4377| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
4378| 		else
4379| 			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
4380| 		ic->arg[2] = (ssize_t)imm;
4381| 		break;
~~~~

### 1.4 Where the arm goes next -- the function's own head, its last `case`, and the tail it #includes

`X(to_be_translated)` declarations (`iword` is `uint32_t`, `imm` is `int`), :4071-4082, and how the word is read, :4124-4139:

~~~~
4071| X(to_be_translated)
4072| {
4073| 	uint64_t addr, low_pc, tmp_addr;
4074| 	uint32_t iword, mask;
4075| 	unsigned char *page;
4076| 	unsigned char ib[4];
4077| 	int main_opcode, rt, rs, ra, rb, rc, aa_bit, l_bit, lk_bit, spr, sh,
4078| 	    xo, imm, load, size, update, zero, bf, bo, bi, bh, oe_bit, n64=0,
4079| 	    bfa, fp, byterev, nb, mb, me;
4080| 	void (*samepage_function)(struct cpu *, struct ppc_instr_call *);
4081| 	void (*rc_f)(struct cpu *, struct ppc_instr_call *);
4082| 
4124| 	{
4125| 		uint32_t *p = (uint32_t *) ib;
4126| 		iword = *p;
4127| 		iword = BE32_TO_HOST(iword);
4128| 	}
4129| 
4130| #define DYNTRANS_TO_BE_TRANSLATED_HEAD
4131| #include "cpu_dyntrans.c"
4132| #undef  DYNTRANS_TO_BE_TRANSLATED_HEAD
4133| 
4134| 
4135| 	/*
4136| 	 *  Translate the instruction:
4137| 	 */
4138| 
4139| 	main_opcode = iword >> 26;
~~~~

The end of the function -- the outer switch's `default:goto bad;` and the tail #include, :5455-5462:

~~~~
5455| 	default:goto bad;
5456| 	}
5457| 
5458| 
5459| #define	DYNTRANS_TO_BE_TRANSLATED_TAIL
5460| #include "cpu_dyntrans.c"
5461| #undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
5462| }
~~~~

The tail itself -- `src/cpus/cpu_dyntrans.c` :1857-2036 (`DYNTRANS_TO_BE_TRANSLATED_TAIL`), VERBATIM: a `break` lands at its
top (mark the translation, then execute); a `goto bad` lands at `bad:` (:1983).

~~~~
1857| #ifdef DYNTRANS_TO_BE_TRANSLATED_TAIL
1858| 	/*
1859| 	 *  If we end up here, then an instruction was translated. Let's mark
1860| 	 *  the page as containing a translation at this part of the page.
1861| 	 */
1862| 
1863| 	/*  Make sure cur_physpage is in synch:  */
1864| 	cpu->cd.DYNTRANS_ARCH.cur_physpage = (struct DYNTRANS_TC_PHYSPAGE *)
1865| 	    cpu->cd.DYNTRANS_ARCH.cur_ic_page;
1866| 
1867| 	{
1868| 		int x = addr & (DYNTRANS_PAGESIZE - 1);
1869| 		int addr_per_translation_range = DYNTRANS_PAGESIZE / (8 *
1870| 		    sizeof(cpu->cd.DYNTRANS_ARCH.cur_physpage->
1871| 		    translations_bitmap));
1872| 		x /= addr_per_translation_range;
1873| 
1874| 		cpu->cd.DYNTRANS_ARCH.cur_physpage->
1875| 		    translations_bitmap |= ((uint32_t)1 << x);
1876| 	}
1877| 
1878| 
1879| 	/*
1880| 	 *  Now it is time to check for combinations of instructions that can
1881| 	 *  be converted into a single function call.
1882| 	 *
1883| 	 *  Note: Single-stepping or instruction tracing doesn't work with
1884| 	 *  instruction combinations. For architectures with delay slots,
1885| 	 *  we also ignore combinations if the delay slot is across a page
1886| 	 *  boundary.
1887| 	 */
1888| 	if (!single_step && !single_step_breakpoint
1889| 	    && !cpu->machine->instruction_trace
1890| #ifdef DYNTRANS_DELAYSLOT
1891| 	    && !in_crosspage_delayslot
1892| #endif
1893| 	    && cpu->cd.DYNTRANS_ARCH.combination_check != NULL
1894| 	    && cpu->machine->allow_instruction_combinations) {
1895| 		cpu->cd.DYNTRANS_ARCH.combination_check(cpu, ic,
1896| 		    addr & (DYNTRANS_PAGESIZE - 1));
1897| 	}
1898| 
1899| 	cpu->cd.DYNTRANS_ARCH.combination_check = NULL;
1900| 
1901| 	/*  An additional check, to catch some bugs:  */
1902| 	if (ic->f == TO_BE_TRANSLATED) {
1903| 		fatal("INTERNAL ERROR: ic->f not set!\n");
1904| 		goto bad;
1905| 	}
1906| 	if (ic->f == NULL) {
1907| 		fatal("INTERNAL ERROR: ic->f == NULL!\n");
1908| 		goto bad;
1909| 	}
1910| 
1911| 
1912| 	/*
1913| 	 *  ... and finally execute the translated instruction:
1914| 	 */
1915| 
1916| 	/*  (Except when doing read-ahead!)  */
1917| 	if (cpu->translation_readahead)
1918| 		return;
1919| 
1920| 	/*
1921| 	 *  Special case when single-stepping: Execute the translated
1922| 	 *  instruction, but then replace it with a "to be translated"
1923| 	 *  directly afterwards.
1924| 	 */
1925| 	if ((single_step_breakpoint && cpu->delay_slot == NOT_DELAYED)
1926| #ifdef DYNTRANS_DELAYSLOT
1927| 	    || in_crosspage_delayslot
1928| #endif
1929| 	    ) {
1930| 		single_step_breakpoint = 0;
1931| 		ic->f(cpu, ic);
1932| 		ic->f = TO_BE_TRANSLATED;
1933| 		return;
1934| 	}
1935| 
1936| 
1937| 	/*  Translation read-ahead:  */
1938| 	if (!single_step && !cpu->machine->instruction_trace &&
1939| 	    cpu->machine->breakpoints.n == 0) {
1940| 		uint64_t baseaddr = cpu->pc;
1941| 		uint64_t pagenr = DYNTRANS_ADDR_TO_PAGENR(baseaddr);
1942| 		int i = 1;
1943| 
1944| 		cpu->translation_readahead = MAX_DYNTRANS_READAHEAD;
1945| 
1946| 		while (DYNTRANS_ADDR_TO_PAGENR(baseaddr +
1947| 		    (i << DYNTRANS_INSTR_ALIGNMENT_SHIFT)) == pagenr &&
1948| 		    cpu->translation_readahead > 0) {
1949| 			void (*old_f)(struct cpu *,
1950| 			    struct DYNTRANS_IC *) = ic[i].f;
1951| 
1952| 			/*  Already translated? Then abort:  */
1953| 			if (old_f != TO_BE_TRANSLATED)
1954| 				break;
1955| 
1956| 			/*  Translate the instruction:  */
1957| 			ic[i].f(cpu, ic+i);
1958| 
1959| 			/*  Translation failed? Then abort.  */
1960| 			if (ic[i].f == old_f)
1961| 				break;
1962| 
1963| 			cpu->translation_readahead --;
1964| 			++i;
1965| 		}
1966| 
1967| 		cpu->translation_readahead = 0;
1968| 	}
1969| 
1970| 
1971| 	/*
1972| 	 *  Finally finally :-), execute the instruction.
1973| 	 *
1974| 	 *  Note: The instruction might have changed during read-ahead, if
1975| 	 *  instruction combinations are used.
1976| 	 */
1977| 
1978| 	ic->f(cpu, ic);
1979| 
1980| 	return;
1981| 
1982| 
1983| bad:	/*
1984| 	 *  Nothing was translated. (Unimplemented or illegal instruction.)
1985| 	 */
1986| 
1987| 	/*  Clear the translation, in case it was "half-way" done:  */
1988| 	ic->f = TO_BE_TRANSLATED;
1989| 
1990| 	if (cpu->translation_readahead)
1991| 		return;
1992| 
1993| 
1994| 	/*
1995| 	 *  Abort the emulation.  In principle, it may have been more accurate
1996| 	 *  to treat invalid/unimplemented instructions as something that
1997| 	 *  should cause e.g. an exception (depending on how the particular
1998| 	 *  CPU works), but chances are that this is an unimplemented
1999| 	 *  instruction that should be implemented for real.
2000| 	 */
2001| 
2002| 	about_to_enter_single_step = true;
2003| 
2004| 	if (cpu->is_32bit)
2005| 		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
2006| 		    "UNIMPLEMENTED instruction at 0x%" PRIx32, (uint32_t)cpu->pc);
2007| 	else
2008| 		debugmsg_cpu(cpu, SUBSYS_CPU, "", VERBOSITY_ERROR,
2009| 		    "UNIMPLEMENTED instruction at 0x%" PRIx64, (uint64_t)cpu->pc);
2010| 
2011| 	if (!(single_step || cpu->machine->instruction_trace))
2012| 		DISASSEMBLE(cpu, ib, 1, 0);
2013| 
2014| 	cpu->running = 0;
2015| 
2016| 	/*  Note: Single-stepping can jump here.  */
2017| stop_running_translated:
2018| 
2019| 	// This makes sure that we stop in the debugger, even if e.g.
2020| 	// "step 100" was executing and 50 steps remained.
2021| 	debugger_reset();
2022| 
2023| 	ic = cpu->cd.DYNTRANS_ARCH.next_ic = &nothing_call;
2024| 	cpu->cd.DYNTRANS_ARCH.next_ic ++;
2025| 
2026| #ifdef DYNTRANS_DELAYSLOT
2027| 	/*  Special hack: If the bad instruction was in a delay slot,
2028| 	    make sure that execution does not continue anyway:  */
2029| 	if (cpu->delay_slot)
2030| 		cpu->delay_slot |= EXCEPTION_IN_DELAY_SLOT;
2031| #endif
2032| 
2033| 	/*  Execute the "nothing" instruction:  */
2034| 	ic->f(cpu, ic);
2035| 
2036| #endif	/*  DYNTRANS_TO_BE_TRANSLATED_TAIL  */
~~~~

The table slot that ends the process (S7) -- `X(invalid)`, `src/cpus/cpu_ppc_instr.c` :238-245:

~~~~
238| /*
239|  *  invalid:  To catch bugs.
240|  */
241| X(invalid)
242| {
243| 	fatal("PPC: invalid(): INTERNAL ERROR\n");
244| 	exit(1);
245| }
~~~~

---

## 2. The detector -- `regress/ppc_dsform_probe.py` (NEW; 40,883 bytes, 836 lines by `wc -l`, LF only, md5 `0266228894811ba6c51cff82585753c9`, frozen at that md5 before its first run)

### 2.1 The docstring -- the CONTRACT, the sessions, the summary protocol -- :1-87, VERBATIM

~~~~
1| #!/usr/bin/env python3
2| """ppcdsformxo -- RUNG-3 DETECTOR for the 64-bit DS-form loads and stores (opcodes 58 and 62, #571).
3| 
4| usage: ppc_dsform_probe.py <gxemul> [label] [workdir]
5|        workdir, when given, receives one transcript per session, RAW_<label>_<session>.txt.
6|        The 4-byte dummy boot file is written to a private tempfile.mkdtemp directory, which is
7|        removed when the probe ends.
8| 
9| Promoted from the rung-3 witness of the loads, which stays byte-identical at
10| regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py.  Machine: the unmodified
11| in-tree -E bareppc -M 64 (PPC970, a 64-bit CPU; MSR 0, so every address here is physical).
12| Every placed word is built from its fields by encode() or encode_md().  Each session seeds
13| registers and memory with the debugger, places its words with `put w', unassembles them, steps
14| exactly once per word, then reads `reg' and `dump'.
15| 
16| ARCHITECTURE -- PowerPC Book I v2.01, _scratchpad/ppc_uisa_book1_v201.txt.  DS form: OPCD 0:5,
17| RT/RS 6:10, RA 11:15, DS 16:29, XO 30:31 (:777-787); EA = (RA|0) + EXTS(DS || 0b00)
18| (:951-955, :1221-1227).  Opcode 58: XO 0 ld, XO 1 ldu (RA <- EA), XO 2 lwa (the word,
19| sign-extended) (:2350-2367, :2372-2395, :2297-2317).  Opcode 62: XO 0 std, XO 1 stdu (RA <- EA)
20| (:2573-2593, :2595-2621).  Opcode 58 with XO 3 and opcode 62 with XO 2 or 3 are empty cells of
21| the opcode maps, so they are illegal instructions (:1040-1052, :10402-10435); ldu and stdu with
22| RA = 0 are invalid forms (:2395, :2618).  D-form controls: lwz (:2244) and stw (:2518-2541).
23| Every value, destination and RA want is computed from these lines and the seeded bytes.
24| 
25| SESSIONS -- eight; each guest session has its own liveness row (li r9,0x1234, the last word
26| before any stop word):
27|   loads     the witness's three words (ld, ldu, lwa at DS != 0); ld, ldu and lwa at DS = 0
28|             from second bases; ld and lwa with RA = 0 from a window at 0x7000 seeded with bytes
29|             that count by two; the D-form controls lwz +8 and lwz +6.  Data: a counting byte
30|             pattern at 0x20000.
31|   stores    std, stdu (RA != RS, and RA = RS), std and stdu at DS = 0, std with RA = 0 at 0x7100,
32|             and the D-form control stw +6.  Each destination window, EA-1 .. EA+11, is seeded
33|             with a counting pattern and read back by `dump'; each source other than the RA = RS
34|             store's (its own base) is eight distinct bytes absent from that pattern, built by
35|             the guest with lis, ori, sldi and oris.
36|   xo58_3, xo62_2, xo62_3, ldu ra0, stdu ra0
37|             one stop word each -- 58 with XO 3; 62 with XO 2; 62 with XO 3; ldu and stdu with
38|             RA = 0 at DS != 0 -- placed LAST.  Its `bad' row wants the `UNIMPLEMENTED instruction'
39|             line, RT still the sentinel (loads) or the destination window unchanged (stores), and
40|             RA unchanged.
41|   neg       the loads commands against a bogus machine TYPE: exit 1 and no register dump.
42| Global rows: `unasm census' (every placed word of the seven guest sessions, unassembled before
43| stepping) and `word pins' (the witness's three words read back as e894ff90, e8b5ffa1, e8d6000a).
44| 
45| CONTRACT (clause (e)).
46|   CLAIMED: for ld, ldu, lwa, std and stdu, the effective address (the XO bits are never part of
47|     the displacement), the width and extension of the transfer, and whether RA is written (ldu
48|     and stdu write EA; ld, lwa and std leave RA alone); the expected bytes at every store's
49|     destination, and for stdu the seeded bytes around it; the three reserved XO encodings stop
50|     the CPU and write nothing; ldu and stdu with RA = 0 (DS != 0) stop the CPU and write
51|     nothing; lwz +6 and stw +6 keep the low two bits of a D-form displacement.  The DS = 0 value
52|     rows pin the address each access reaches, not which half of the handler table was selected.
53|   NOT CLAIMED:
54|     * ldu with RA = RT (an invalid form; after the fix it leaves RT = EA; not checked);
55|     * 32-bit CPUs: opcodes 58 and 62 are illegal on 32-bit implementations; before and after
56|       this fix a 32-bit CPU decodes them through the same arm; the MODE32 table has real
57|       doubleword handlers (tmp_ppc_loadstore.c:1923+); after the fix the legal forms select
58|       those handlers and reserved XO / RA = 0 updates stop there too; no width test this
59|       round, and no 32-bit session is rowed;
60|     * the joints of DS = 0 with RA = 0: ldu and stdu (the only observer of an update
61|       conditioned on a non-zero displacement), ld and std, and lwa;
62|     * lwa of a word whose bit 31 is clear;
63|     * the D-form opcodes other than lwz and stw;
64|     * translation on (MSR IR or DR), MSR SF, an EA with a non-zero high half, an EA that
65|       crosses a page, and the indexed forms ldx, ldux, lwax, lwaux, stdx and stdux;
66|     * an access that fails: the translation-off failure path exists and is gated by -T
67|       (halt_on_nonexistant_memaccess), which this probe does not pass;
68|     * the disassembler's mnemonics.
69|   CENSUS: `unasm census' attests the opcode, RT/RS, RA and the raw low halfword of every placed
70|     word, never the instruction form: the tree's disassembler prints `ld' for every opcode-58
71|     word and `std' for every opcode-62 word, with the raw low halfword as the displacement.  Its
72|     expected text takes each DS-form word's opcode and XO from DSMAP, a table keyed by the
73|     word's label, never from the fields the word was encoded from.
74|   STOP WORDS: a word that stops the CPU ends its session's execution, so each one is the LAST
75|     word of its own session, after the liveness li.
76|   BEHAVIOUR CHANGES the fixed build shows: (1) opcode 58 with XO 3 and opcode 62 with XO 2 or 3
77|     stop the CPU, where the committed decode executed them as an 8-byte ld or std at EA + XO;
78|     (2) ldu and stdu with RA = 0 stop the CPU at the existing RA = 0 update guard, where the
79|     committed decode executed them as an absolute ld or std at EXTS(DS || XO) with no update.
80| 
81| SUMMARY LINES: PPC_DSFORM_RESULT=<ok>/<rows>; PPC_DSFORM_CONTROL=OK|FAIL over the CONTROL rows;
82| PPC_DSFORM_SYMPTOM over the SYMPTOM rows -- PRESENT n/m when every one of them is red, ABSENT
83| when none is, MIXED otherwise; PPC_DSFORM_RED=<names>|none; then the sentinel.  Exit status 1
84| on any red row.
85| 
86| Sentinel: PPC_DSFORM_PROBE_DONE
87| """
~~~~

### 2.2 The constants, DSMAP, ROW_NAMES, CONTROL, SYMPTOM and their asserts -- :98-156, VERBATIM

~~~~
98| CODE = 0x10000             # the guest program, in every session
99| DATA = 0x20000             # loads: byte DATA + k is k, k < 0x100
100| STORE = 0x21000            # stores: byte STORE + k is k, k < 0xc0
101| LOWLD = 0x7000             # loads with RA = 0: byte LOWLD + k is 0x80 + 2k, k < 0x10
102| LOWST = 0x7100             # std with RA = 0: byte LOWST - 0x10 + k is 0x10 + k, k < 0x30
103| M64 = (1 << 64) - 1
104| SENT = 0x5A5A5A5A5A5A5A5A  # seeded into every register no placed word may write
105| LIVE = 0x1234
106| LIVEREG = 9
107| SPARE = 30                 # seeded, never written: shows the seeding itself took
108| N_ROWS = 39
109| CENSUS_WORDS = 108         # words placed in the seven guest sessions: the census row's want
110| 
111| OP_ADDI = 14               # li  RT,SI   is addi RT,0,SI
112| OP_ADDIS = 15              # lis RT,SI   is addis RT,0,SI
113| OP_ORI = 24                # ori  RA,RS,UI  (RS sits in 6:10, RA in 11:15)
114| OP_ORIS = 25               # oris RA,RS,UI
115| OP_MD = 30                 # rldicr, the sldi encoding (MD form)
116| OP_LWZ = 32                # lwz RT,D(RA)   :2244
117| OP_STW = 36                # stw RS,D(RA)   :2518
118| OP_DSLOAD = 58             # ld / ldu / lwa :2350, :2372, :2297
119| OP_DSSTORE = 62            # std / stdu     :2573, :2595
120| XO_LD = 0
121| XO_LDU = 1
122| XO_LWA = 2
123| XO_STD = 0
124| XO_STDU = 1
125| XO_RLDICR = 1              # the MD-form XO field, 27:29
126| 
127| #  The census's expected (opcode, XO) for each DS-form label -- Table 16 and Table 19
128| #  (:10402-10435), written out here and never read from a placed word's fields.
129| DSMAP = {"ld": (58, 0), "ldu": (58, 1), "lwa": (58, 2), "xo58_3": (58, 3),
130|          "std": (62, 0), "stdu": (62, 1), "xo62_2": (62, 2), "xo62_3": (62, 3)}
131| 
132| ROW_NAMES = (
133|     "ld value", "ld RA after", "ld ds0 value", "ld ra0 value",
134|     "ldu value", "ldu RA after", "ldu ds0 value",
135|     "lwa value", "lwa RA after", "lwa ds0 value", "lwa ra0 value",
136|     "lwz value", "lwz odd", "live",
137|     "std value", "std RA after", "std ds0 value", "std ra0 value",
138|     "stdu value", "stdu neigh", "stdu RA after", "stdu ds0 value",
139|     "stdu alias val", "stdu alias RA", "stw odd", "st live",
140|     "xo58_3 live", "xo58_3 bad", "xo62_2 live", "xo62_2 bad", "xo62_3 live", "xo62_3 bad",
141|     "ldu ra0 live", "ldu ra0 bad", "stdu ra0 live", "stdu ra0 bad",
142|     "unasm census", "word pins", "neg apparatus")
143| #  CONTROL: green before and after the fix.  SYMPTOM: the rows the committed decode turns red.
144| CONTROL = ("ld value", "ld RA after", "ld ds0 value", "ld ra0 value", "lwa RA after",
145|            "lwz value", "lwz odd", "live",
146|            "std value", "std RA after", "std ds0 value", "std ra0 value", "stw odd", "st live",
147|            "xo58_3 live", "xo62_2 live", "xo62_3 live", "ldu ra0 live", "stdu ra0 live",
148|            "unasm census", "word pins", "neg apparatus")
149| SYMPTOM = ("ldu value", "ldu RA after", "ldu ds0 value",
150|            "lwa value", "lwa ds0 value", "lwa ra0 value",
151|            "stdu value", "stdu neigh", "stdu RA after", "stdu ds0 value",
152|            "stdu alias val", "stdu alias RA",
153|            "xo58_3 bad", "xo62_2 bad", "xo62_3 bad", "ldu ra0 bad", "stdu ra0 bad")
154| assert len(ROW_NAMES) == N_ROWS == len(set(ROW_NAMES))
155| assert set(CONTROL) | set(SYMPTOM) == set(ROW_NAMES) and not set(CONTROL) & set(SYMPTOM)
156| assert len(CONTROL) + len(SYMPTOM) == N_ROWS
~~~~

### 2.3 `row()` and `obs()` -- :158-176, VERBATIM (the 14-character assert and its comment: K1)

~~~~
158| rows = []
159| 
160| 
161| def row(name, got, want, note=""):
162|     assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
163|     #  14, not 15: gate 13 pins each row as `^name  ' (two spaces) inside this %-16s column.
164|     assert len(name) <= 14, name
165|     ok = (got == want)
166|     rows.append((name, ok))
167|     print("%-16s %-20s %-20s %-52s %s" % (name, str(got), str(want), note,
168|                                           "ok" if ok else "FAIL"))
169|     return ok
170| 
171| 
172| def obs(text):
173|     #  An observation never ends like a row: the gate counts lines ending ` ok' and ` FAIL'.
174|     if re.search(r"\s(ok|FAIL)$", text):
175|         text += " ."
176|     print("OBS " + text)
~~~~

### 2.4 The session programs -- every placed word, with its base, displacement and XO -- :334-402, VERBATIM

(`encode()` at :237-246 builds each word from its fields; `d_fields()` splits a D-form displacement into the DS and XO
positions; `set32`/`set64` are `lis`/`ori`/`sldi`/`oris` sequences, none of them opcode 58 or 62.)

~~~~
334| # loads -- the witness's bases r20..r23 first, then the second bases
335| LD_BASES = {20: DATA + 0x80, 21: DATA + 0x80, 22: DATA + 0x80, 23: DATA + 0x80,
336|             24: DATA + 0x30, 25: DATA + 0x90, 26: DATA + 0x40, 27: DATA}
337| LD = Prog("loads")
338| for _r in sorted(LD_BASES):
339|     LD.set32(_r, LD_BASES[_r])
340| LD.ds("ld", "ld", OP_DSLOAD, 4, 20, -0x70, XO_LD)            # the witness's e894ff90
341| LD.ds("ldu", "ldu", OP_DSLOAD, 5, 21, -0x60, XO_LDU)         # the witness's e8b5ffa1
342| LD.ds("lwa", "lwa", OP_DSLOAD, 6, 22, 0x08, XO_LWA)          # the witness's e8d6000a
343| LD.imm("lwz", OP_LWZ, 7, 23, 0x08, tag="lwz")
344| LD.ds("ld ds0", "ld", OP_DSLOAD, 11, 26, 0, XO_LD)
345| LD.ds("ldu ds0", "ldu", OP_DSLOAD, 8, 24, 0, XO_LDU)
346| LD.ds("lwa ds0", "lwa", OP_DSLOAD, 10, 25, 0, XO_LWA)
347| LD.imm("lwz", OP_LWZ, 14, 27, 6, tag="lwz odd")
348| #  The RA = 0 words go last before li: one that stops the CPU (under a variant that adds an update)
349| #  then leaves the fewest words unrun.
350| LD.ds("lwa ra0", "lwa", OP_DSLOAD, 13, 0, LOWLD + 4, XO_LWA)
351| LD.ds("ld ra0", "ld", OP_DSLOAD, 12, 0, LOWLD, XO_LD)
352| LD.li(LIVEREG, LIVE)
353| #  The 0x7000 window counts by two, so no value read from it is also a value of the DATA pattern.
354| LD_REGIONS = [(DATA, 0x100, 0x00, 1), (LOWLD, 0x10, 0x80, 2)]
355| LD_DUMPS = [(DATA, DATA + 0x100), (LOWLD, LOWLD + 0x10)]
356| LD_SEEDS = [0, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, LIVEREG, SPARE] + sorted(LD_BASES)
357| 
358| # stores -- one 0x20-byte slot per store in the STORE pattern, plus the RA = 0 window
359| ST_BASES = {20: STORE + 0x40, 21: STORE + 0x60, 22: STORE + 0x50, 23: STORE + 0x80,
360|             24: STORE + 0x8A, 25: STORE + 0xB0}
361| ST_SRC = {4: 0xC0C1C2C3C4C5C6C7, 5: 0xC8C9CACBCCCDCECF, 6: 0xD0D1D2D3D4D5D6D7,
362|           7: 0xD8D9DADBDCDDDEDF, 8: 0xE0E1E2E3E4E5E6E7, 10: 0xE8E9EAEBECEDEEEF}
363| ST = Prog("stores")
364| for _r in sorted(ST_BASES):
365|     ST.set32(_r, ST_BASES[_r])
366| for _r in sorted(ST_SRC):
367|     ST.set64(_r, ST_SRC[_r])
368| ST.ds("std", "std", OP_DSSTORE, 4, 20, -0x30, XO_STD)
369| ST.ds("std ds0", "std", OP_DSSTORE, 8, 25, 0, XO_STD)
370| ST.ds("stdu", "stdu", OP_DSSTORE, 5, 21, -0x30, XO_STDU)
371| ST.ds("stdu ds0", "stdu", OP_DSSTORE, 6, 22, 0, XO_STDU)
372| ST.ds("stdu alias", "stdu", OP_DSSTORE, 23, 23, -0x10, XO_STDU)   # RA = RS
373| ST.imm("stw", OP_STW, 7, 24, 6, tag="stw odd")
374| ST.ds("std ra0", "std", OP_DSSTORE, 10, 0, LOWST, XO_STD)      # RA = 0, last before li
375| ST.li(LIVEREG, LIVE)
376| ST_REGIONS = [(STORE, 0xC0, 0x00, 1), (LOWST - 0x10, 0x30, 0x10, 1)]
377| ST_DUMPS = [(STORE, STORE + 0xC0), (LOWST - 0x10, LOWST + 0x20)]
378| ST_SEEDS = [0, LIVEREG, SPARE] + sorted(ST_BASES) + sorted(ST_SRC)
379| ST_STORES = ("std", "std ds0", "stdu", "stdu ds0", "stdu alias", "stw odd", "std ra0")
380| 
381| # the five stop sessions: (name, label, opcode, XO, RA value or None for RA = 0, disp, store,
382| # seeded regions)
383| STOP_SRC = 0xF0F1F2F3F4F5F6F7
384| STOPS = (
385|     ("xo58_3", "xo58_3", OP_DSLOAD, 3, DATA + 0x20, -0x10, False, [(DATA, 0x40, 0x00, 1)]),
386|     ("xo62_2", "xo62_2", OP_DSSTORE, 2, STORE + 0x40, -0x30, True, [(STORE, 0x20, 0x00, 1)]),
387|     ("xo62_3", "xo62_3", OP_DSSTORE, 3, STORE + 0x40, -0x30, True, [(STORE, 0x20, 0x00, 1)]),
388|     ("ldu ra0", "ldu", OP_DSLOAD, XO_LDU, None, 0x10, False, [(0x0, 0x20, 0x60, 1)]),
389|     ("stdu ra0", "stdu", OP_DSSTORE, XO_STDU, None, 0x10, True, [(0x0, 0x20, 0x60, 1)]),
390| )
391| STOP_PROGS = {}
392| for _nm, _lb, _op, _xo, _ra, _disp, _st, _reg in STOPS:
393|     _p = Prog(_nm)
394|     if _ra is not None:
395|         _p.set32(20, _ra)
396|     if _st:
397|         _p.set64(4, STOP_SRC)
398|     _p.li(LIVEREG, LIVE)
399|     _p.ds(_nm, _lb, _op, 4, 20 if _ra is not None else 0, _disp, _xo)     # LAST
400|     STOP_PROGS[_nm] = _p
401| 
402| GUEST_PROGS = [LD, ST] + [STOP_PROGS[s[0]] for s in STOPS]
~~~~

### 2.5 The wants -- computed from the ENCODED fields and the RTL -- :405-447, VERBATIM

~~~~
405| # ------------------------------------------- wants, from the ENCODED fields and the RTL
406| LD_MODEL = seeded(LD_REGIONS)
407| LD_EA = dict((t, ea_of(LD.get(t), LD_BASES)) for t in
408|              ("ld", "ldu", "lwa", "lwz", "ld ds0", "ldu ds0", "lwa ds0", "ld ra0", "lwa ra0",
409|               "lwz odd"))
410| LD_WANT = {}
411| for _t in ("ld", "ldu", "ld ds0", "ldu ds0", "ld ra0"):
412|     LD_WANT[_t] = rd(LD_MODEL, LD_EA[_t], 8)                    # RT <- MEM(EA, 8)
413| for _t in ("lwa", "lwa ds0", "lwa ra0"):
414|     _w = rd(LD_MODEL, LD_EA[_t], 4)
415|     assert _w is not None and _w & 0x80000000, _t                 # bit 31 set: C8
416|     LD_WANT[_t] = exts64(_w, 32)                                  # RT <- EXTS(MEM(EA, 4))
417| for _t in ("lwz", "lwz odd"):
418|     LD_WANT[_t] = rd(LD_MODEL, LD_EA[_t], 4)                    # RT <- 32 zeros || MEM(EA, 4)
419| assert None not in LD_WANT.values()
420| assert low_half(LD.get("lwz odd")["ds"], LD.get("lwz odd")["xo"]) & 3 != 0
421| 
422| ST_MODEL0 = seeded(ST_REGIONS)
423| ST_MODEL = dict(ST_MODEL0)
424| ST_EA = {}
425| for _t in ST_STORES:
426|     _e = ST.get(_t)
427|     ST_EA[_t] = ea_of(_e, ST_BASES)
428|     _src = ST_BASES[23] if _t == "stdu alias" else ST_SRC[_e["rt"]]   # alias: the OLD RA
429|     _n = 4 if _t == "stw odd" else 8
430|     #  every destination window EA-1 .. EA+11 lies inside the seeded bytes, and windows
431|     #  do not overlap
432|     for _a in range(ST_EA[_t] - 1, ST_EA[_t] + 12):
433|         assert _a in ST_MODEL0, (_t, hex(_a))
434|     wr(ST_MODEL, ST_EA[_t], _src, _n)
435| for _i, _t in enumerate(ST_STORES):
436|     for _u in ST_STORES[_i + 1:]:
437|         assert abs(ST_EA[_t] - ST_EA[_u]) >= 13, (_t, _u)
438| for _v in ST_SRC.values():
439|     _b = [(_v >> (8 * _k)) & 0xFF for _k in range(8)]
440|     assert len(set(_b)) == 8 and not set(_b) & set(ST_MODEL0.values()), hex(_v)
441| assert low_half(ST.get("stw odd")["ds"], ST.get("stw odd")["xo"]) & 3 != 0
442| for _nm, _lb, _op, _xo, _ra, _disp, _st, _reg in STOPS:
443|     _b = [(STOP_SRC >> (8 * _k)) & 0xFF for _k in range(8)]
444|     assert len(set(_b)) == 8 and not set(_b) & set(seeded(_reg).values())
445|     _tgt = ea_ds(0 if _ra is None else _ra, STOP_PROGS[_nm].get(_nm)["ds"])
446|     for _a in range(_tgt - 1, _tgt + 12):
447|         assert _a in seeded(_reg), (_nm, hex(_a))
~~~~

### 2.6 One session -- the command stream and the transcript parse -- :514-593, VERBATIM

~~~~
514| def commands(prog, seeds, regions, dumps):
515|     cmds = ["r%d=0x%x" % (r, SENT) for r in sorted(set(seeds))]
516|     for start, n, v0, step in regions:
517|         for k in range(n):
518|             cmds.append("put b 0x%x, 0x%02x" % (start + k, v0 + step * k))
519|     for lo, hi in dumps:
520|         assert lo % 16 == 0 and hi % 16 == 0
521|         cmds.append("dump 0x%x 0x%x" % (lo, hi))
522|     for i, e in enumerate(prog.ent):
523|         cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, e["word"]))
524|     n = len(prog.ent)
525|     cmds.append("unassemble 0x%x 0x%x" % (CODE, CODE + 4 * n))
526|     cmds.append("pc=0x%x" % CODE)
527|     cmds.append("step %d" % n)
528|     cmds.append("reg")
529|     for lo, hi in dumps:
530|         cmds.append("dump 0x%x 0x%x" % (lo, hi))
531|     return cmds
532| 
533| 
534| def session(name, cmds, machine="bareppc", timeout=120):
535|     """The piped cold-debugger session -- regress/ppc_rldicl_probe.py's idiom.  An emulator
536|        that ends early still returns here; its missing readbacks read as absent."""
537|     argv = [BIN, "-V", "-x", "-E", machine, "-M", "64", "0x%x:%s" % (CODE, DUMMY)]
538|     inp = ("\n".join(cmds + ["quit"]) + "\n").encode("latin-1")
539|     try:
540|         p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE,
541|                            stderr=subprocess.STDOUT, timeout=timeout)
542|         raw = p.stdout.decode("latin-1", "replace")
543|         rc = p.returncode
544|         how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
545|     except subprocess.TimeoutExpired as ex:
546|         raw = (ex.output or b"").decode("latin-1", "replace")
547|         how = "TIMEOUT"
548|     ncr = raw.count("\r")
549|     t = raw.replace("\r", "")
550|     R = {"name": name, "how": how, "regs": {}, "pc": None, "msr": None, "dis": []}
551|     idx = t.rfind("GXemul> reg")
552|     if idx >= 0:
553|         seg = t[idx:]
554|         for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", seg):
555|             R["regs"][int(m.group(1))] = int(m.group(2), 16)
556|         m = re.search(r"\bpc  = (0x[0-9a-fA-F]+)", seg)
557|         R["pc"] = int(m.group(1), 16) if m else None
558|         m = re.search(r"\bmsr = (0x[0-9a-fA-F]+)", seg)
559|         R["msr"] = int(m.group(1), 16) if m else None
560|     di = t.find("GXemul> unassemble")
561|     if di >= 0:
562|         de = t.find("GXemul> pc=", di)
563|         for m in UNASM_RE.finditer(t[di:de if de > 0 else len(t)]):
564|             R["dis"].append((int(m.group(1), 16), int(m.group(2), 16), m.group(3),
565|                              m.group(4) or ""))
566|     si = t.find("GXemul> step")
567|     pre, post = (t[:si], t[si:]) if si >= 0 else (t, "")
568|     R["pre"] = parse_dump(pre)
569|     R["post"] = parse_dump(post)
570|     R["unimpl"] = post.count("UNIMPLEMENTED instruction at 0x")
571|     R["todo"] = post.count("TODO: ra=0 && update?")
572|     R["internal"] = post.count("PPC: invalid(): INTERNAL ERROR")
573|     fn = "RAW_%s_%s.txt" % (LABEL, name.replace(" ", "_"))
574|     with open(os.path.join(TDIR, fn), "w", encoding="latin-1", newline="\n") as fh:
575|         fh.write("ARGV: %s\nHOW: %s\nCR_REMOVED: %d (otherwise verbatim)\n\n"
576|                  % (" ".join(argv), how, ncr))
577|         fh.write(t)
578|     R["file"] = fn if KEEP else "(not kept)"
579|     return R
580| 
581| 
582| def g(R, r):
583|     return R["regs"].get(r, -1)
584| 
585| 
586| def obs_session(R, prog, seeded_model, dumps):
587|     seedok = all(R["pre"].get(a) == v for a, v in seeded_model.items()) if dumps else None
588|     obs("session %-8s how=%s words=%d unimplemented=%d todo_ra0=%d internal_error=%d pc=%s "
589|         "msr=%s r%d=%s seeded_readback=%s transcript=%s"
590|         % (R["name"], R["how"], len(prog.ent), R["unimpl"], R["todo"], R["internal"],
591|            hex(R["pc"]) if R["pc"] is not None else "none",
592|            hex(R["msr"]) if R["msr"] is not None else "none", SPARE, hex(g(R, SPARE)),
593|            {None: "not dumped", True: "same", False: "DIFFERS"}[seedok], R["file"]))
~~~~

### 2.7 The stop-session rows, the census, the word pins, the negative control and the summary -- :725-836, VERBATIM

~~~~
725|     # ------------------------------------------------------------ stop sessions ----
726|     for nm, _lb, _op, _xo, ra_val, _disp, store, regions in STOPS:
727|         prog = STOP_PROGS[nm]
728|         e = prog.get(nm)
729|         seeds = [0, 4, LIVEREG, SPARE] + ([20] if ra_val is not None else [])
730|         dumps = [(lo, lo + n) for lo, n, _v, _s in regions] if store else []
731|         R = session(nm, commands(prog, seeds, regions, dumps))
732|         results.append((R, prog))
733|         model = seeded(regions)
734|         ra_reg = 20 if ra_val is not None else 0
735|         ra_want = ra_val if ra_val is not None else SENT
736|         stop = "stop" if R["unimpl"] else "nostop"
737|         ra_txt = "kept" if g(R, ra_reg) == ra_want else hex(g(R, ra_reg))
738|         row("%s live" % nm, hex(g(R, LIVEREG)), hex(LIVE),
739|             "li r%d ran, the word before the stop word" % LIVEREG)
740|         if store:
741|             tgt = ea_ds(0 if ra_val is None else ra_val, e["ds"])
742|             win_got = hexbytes(R["post"], tgt - 1, 13)
743|             win_want = hexbytes(model, tgt - 1, 13)
744|             win = "none" if win_got is None else ("kept" if win_got == win_want else "changed")
745|             row("%s bad" % nm, "%s,win=%s,ra=%s" % (stop, win, ra_txt), "stop,win=kept,ra=kept",
746|                 "opcode %d XO %d, RA %s: CPU stops; window, RA unchanged"
747|                 % (DSMAP[e["label"]][0], e["xo"], "= 0" if ra_val is None else "!= 0"))
748|             obs("%-8s window 0x%x..0x%x got %s | seeded %s | RA + raw low half = 0x%x"
749|                 % (nm, tgt - 1, tgt + 11, win_got, win_want, fold_of(e, {20: ra_val})))
750|         else:
751|             rt_txt = "sent" if g(R, 4) == SENT else hex(g(R, 4))
752|             row("%s bad" % nm, "%s,rt=%s,ra=%s" % (stop, rt_txt, ra_txt), "stop,rt=sent,ra=kept",
753|                 "opcode %d XO %d, RA %s: CPU stops; RT, RA unchanged"
754|                 % (DSMAP[e["label"]][0], e["xo"], "= 0" if ra_val is None else "!= 0"))
755|             obs("%-8s r4 = %s  names: %s | RA + raw low half = 0x%x"
756|                 % (nm, hex(g(R, 4)), names_text(model, R["regs"].get(4)),
757|                    fold_of(e, {20: ra_val})))
758|         obs_session(R, prog, model, dumps)
759| 
760|     # ------------------------------------------------------- the unassemble census --
761|     matched = 0
762|     lines = 0
763|     for R, prog in results:
764|         dis = R["dis"]
765|         lines += len(dis)
766|         for i, e in enumerate(prog.ent):
767|             em, eo = expect_unasm(e)
768|             if i < len(dis):
769|                 d_addr, d_word, d_mn, d_ops = dis[i]
770|                 same = (d_addr == CODE + 4 * i and d_word == e["word"]
771|                         and d_mn == em and d_ops == eo)
772|                 got_txt = "%x: %08x %s %s" % (d_addr, d_word, d_mn, d_ops)
773|             else:
774|                 same = False
775|                 got_txt = "(no line)"
776|             matched += 1 if same else 0
777|             if e["kind"] == "ds" or not same:
778|                 extra = ""
779|                 if e["kind"] == "ds":
780|                     extra = ("  [placed as %s: opcode %d RT %d RA %d DS %d XO %d; raw low half"
781|                              " 0x%04x]" % (e["label"], e["word"] >> 26, e["rt"], e["ra"],
782|                                            e["ds"], e["xo"], low_half(e["ds"], e["xo"])))
783|                 obs("unasm %-8s %s | want %s %s | %s%s"
784|                     % (R["name"], got_txt, em, eo, "same" if same else "DIFFERS", extra))
785|     row("unasm census", "%d/%d" % (matched, lines), "%d/%d" % (CENSUS_WORDS, CENSUS_WORDS),
786|         "every placed word of the seven guest sessions")
787| 
788|     # ------------------------------------------------------------------ word pins --
789|     pins = []
790|     for t in ("ld", "ldu", "lwa"):
791|         i = LD.ent.index(LD.get(t))
792|         pins.append("%08x" % L["dis"][i][1] if i < len(L["dis"]) else "none")
793|     row("word pins", ",".join(pins), "e894ff90,e8b5ffa1,e8d6000a",
794|         "the witness's ld, ldu, lwa words, read back by unassemble")
795| 
796|     # ============================================== NEGATIVE APPARATUS CONTROL ==
797|     # The loads commands against a bogus machine TYPE: no guest is built, so no register
798|     # dump exists and every register oracle above would read -0x1.
799|     N = session("neg", LD_CMDS, machine="nosuchmachine", timeout=60)
800|     row("neg apparatus", "%s/%s" % (N["how"], hex(g(N, LIVEREG))), "exit1/-0x1",
801|         "loads commands, bogus machine TYPE: exit 1, no registers")
802|     obs("session neg      how=%s transcript=%s" % (N["how"], N["file"]))
803| 
804|     # ============================================================ SUMMARY + DONE
805|     assert [n for n, _ in rows] == list(ROW_NAMES), "row list drifted from ROW_NAMES"
806|     okmap = dict(rows)
807|     npass = sum(1 for _, ok in rows if ok)
808|     red = [n for n, ok in rows if not ok]
809|     nsym = sum(1 for n in SYMPTOM if not okmap[n])
810|     if nsym == len(SYMPTOM):
811|         sym = "PRESENT %d/%d" % (nsym, len(SYMPTOM))
812|     elif nsym == 0:
813|         sym = "ABSENT"
814|     else:
815|         sym = "MIXED"
816|     print("")
817|     print("elapsed=%.1fs binary=%s label=%s" % (time.time() - t0, BIN, LABEL))
818|     print("PPC_DSFORM_RESULT=%d/%d" % (npass, len(rows)))
819|     print("PPC_DSFORM_CONTROL=%s" % ("OK" if all(okmap[n] for n in CONTROL) else "FAIL"))
820|     print("PPC_DSFORM_SYMPTOM=%s" % sym)
821|     print("PPC_DSFORM_RED=%s" % (",".join(red) if red else "none"))
822|     print("PPC_DSFORM_PROBE_DONE")
823|     sys.stdout.flush()
824|     return 1 if red else 0
825| 
826| 
827| if __name__ == "__main__":
828|     if len(sys.argv) < 2:
829|         sys.stderr.write("usage: ppc_dsform_probe.py <gxemul> [label] [workdir]\n")
830|         sys.exit(2)
831|     _TMPDIR = tempfile.mkdtemp(prefix="ppc_dsform_")
832|     try:
833|         _RC = main(_TMPDIR)
834|     finally:
835|         shutil.rmtree(_TMPDIR, ignore_errors=True)
836|     sys.exit(_RC)
~~~~

### 2.8 `DETECTOR_FREEZE.txt` (table1, written 08:27:36 before the first run), VERBATIM

~~~~
DETECTOR_FREEZE -- regress/ppc_dsform_probe.py, round #571 (ppcdsformxo), written 2026-10-24

probe md5:   0266228894811ba6c51cff82585753c9
probe bytes: 40883
probe lines: 836  (LF only: 0 CR bytes)
ast check:   python -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" regress/ppc_dsform_probe.py
             exit status 0, output: (none)
witness:     regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py untouched, md5 5e96b69df49ac82e10b3118780899549; its MANIFEST.md5 verifies 6 of 6

N = 39

ROW NAMES, in emission order (the gate's name list is this list):
ld value
ld RA after
ld ds0 value
ld ra0 value
ldu value
ldu RA after
ldu ds0 value
lwa value
lwa RA after
lwa ds0 value
lwa ra0 value
lwz value
lwz odd
live
std value
std RA after
std ds0 value
std ra0 value
stdu value
stdu neigh
stdu RA after
stdu ds0 value
stdu alias val
stdu alias RA
stw odd
st live
xo58_3 live
xo58_3 bad
xo62_2 live
xo62_2 bad
xo62_3 live
xo62_3 bad
ldu ra0 live
ldu ra0 bad
stdu ra0 live
stdu ra0 bad
unasm census
word pins
neg apparatus

CONTROL (22 rows; green before and after the fix):
  ld value, ld RA after, ld ds0 value, ld ra0 value, lwa RA after, lwz value, lwz odd, live, std value, std RA after, std ds0 value, std ra0 value, stw odd, st live, xo58_3 live, xo62_2 live, xo62_3 live, ldu ra0 live, stdu ra0 live, unasm census, word pins, neg apparatus
SYMPTOM (17 rows; red under the committed decode):
  ldu value, ldu RA after, ldu ds0 value, lwa value, lwa ds0 value, lwa ra0 value, stdu value, stdu neigh, stdu RA after, stdu ds0 value, stdu alias val, stdu alias RA, xo58_3 bad, xo62_2 bad, xo62_3 bad, ldu ra0 bad, stdu ra0 bad

SESSIONS (eight), each `-E bareppc -M 64', debugger-stepped once per placed word:
  1. loads     27 words  regions 0x20000..0x200ff = 0x00 + 1*k; 0x7000..0x700f = 0x80 + 2*k; stop word none; li r9 last
  2. stores    50 words  regions 0x21000..0x210bf = 0x00 + 1*k; 0x70f0..0x711f = 0x10 + 1*k; stop word none; li r9 last
  3. xo58_3     4 words  regions 0x20000..0x2003f = 0x00 + 1*k; stop word LAST: e894fff3 (opcode 58, XO 3, RA r20 = 0x20020, disp -16)
  4. xo62_2     9 words  regions 0x21000..0x2101f = 0x00 + 1*k; stop word LAST: f894ffd2 (opcode 62, XO 2, RA r20 = 0x21040, disp -48), window dumped
  5. xo62_3     9 words  regions 0x21000..0x2101f = 0x00 + 1*k; stop word LAST: f894ffd3 (opcode 62, XO 3, RA r20 = 0x21040, disp -48), window dumped
  6. ldu ra0    2 words  regions 0x0..0x1f = 0x60 + 1*k; stop word LAST: e8800011 (opcode 58, XO 1, RA 0, disp 16)
  7. stdu ra0   7 words  regions 0x0..0x1f = 0x60 + 1*k; stop word LAST: f8800011 (opcode 62, XO 1, RA 0, disp 16), window dumped
  8. neg      the loads commands against -E nosuchmachine (row `neg apparatus', exit1/-0x1)
  placed words in the seven guest sessions: 108 (CENSUS_WORDS = 108; the census row's want is 108/108)
  word pins: the loads session's words for ld, ldu, lwa encode to e894ff90,e8b5ffa1,e8d6000a

NOTES (dispositions, no measurement of gxemul is claimed here):
  * `lwa ra0 value' is a SYMPTOM row, not a control.  It is opcode 58 with XO 2, so under the committed
    decode it loads the doubleword at 0x7006; BUILD_SPEC section 10 item 2's "gains nothing red from
    these eight (XO 0 is correct on BASE)" does not hold for it.  Section 4's 18 symptom rows were 11 plus
    seven stop rows; 10b leaves five stop rows, so 16, plus `lwa ra0 value' = 17.  Predicted from this
    source for the BASE binary: PPC_DSFORM_RESULT=22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17 (a
    prediction for prefix_BASE.out, not a measurement).
  * Row names: the loads and stores liveness rows keep section 3's names (`live', `st live'); the five
    stop sessions carry their session prefix (section 10 item 8).  Every name is at most 14 characters;
    the probe asserts it (`len(name) <= 14', commented with the gate pin).
  * The 0x7000 window counts by two, so no value read from it is also a value of the 0x20000 pattern.
  * Word order: in the loads and stores sessions the RA = 0 words are the last words before li (loads:
    lwa ra0, then ld ra0; stores: std ra0), so a variant that makes one of them a stopping word (L9a:
    ld ra0 and std ra0 reach the RA = 0 update guard; L10: lwa ra0 first) leaves the fewest words unrun.
  * PRETABLE.out section 4 names L5, L8a, L8b and L9b for `lwa ra0 value'.  Read from this source the row is
    also red on BASE and under L3, L4b and L7 (L3 and L4b leave it an 8-byte load from 0x7006, L7 a word load
    from 0x7006), and L9b (an extra +1 on the XO-0 forms) does not reach it (XO 2).
  * Store sources are built by the guest with lis, ori, sldi (rldicr r,r,32,31; opcode 30), oris and
    ori; none of those words is opcode 58 or 62, and the census covers them.
  * Interface: ppc_dsform_probe.py <gxemul> [label] [workdir].  workdir receives the transcripts
    RAW_<label>_<session>.txt; without it they go to the private tempfile.mkdtemp directory, removed in
    `finally:'.  Gate 13 passes "$LOGDIR/ppc_dsform".
  * A missing binary raises from subprocess (no sentinel), as the witness did: L5b's expectation.  An
    emulator that exits mid-session (L8c) returns normally; that session's rows read as absent (-0x1)
    and go red, CONTROL=FAIL, and the sentinel is printed.  Per session the probe prints
    how=, unimplemented=, todo_ra0= and internal_error= (the count of `PPC: invalid(): INTERNAL ERROR').
  * Logic check of the probe's Python only (not gxemul): a scratchpad stand-in that answers the
    debugger commands (fake_gxemul.py, in the session scratchpad t2/writer/) gave 39/39 with Book I
    semantics and 22/39 with exactly the 17 SYMPTOM rows red under committed-decode semantics, its
    three witness rows reproducing WITNESS_headbin.out's got values; gate 13's new block, run on those
    two outputs with stubbed check/count, scored 53 of 53 checks green and 31 of 53 respectively.
~~~~

---

## 3. The gate block, the MANIFEST keys, the coverage pin

### 3.1 `regress/gate_ppc.sh` (gate 13) -- the diff, VERBATIM (`diff_gate_ppc.patch`; reproduces the working tree; the staged copy `table1_20261024/staged/gate_ppc.sh.txt` is byte-identical, md5 `d361db09`)

~~~~
diff --git a/regress/gate_ppc.sh b/regress/gate_ppc.sh
index 7b65c5de..bf7e7541 100644
--- a/regress/gate_ppc.sh
+++ b/regress/gate_ppc.sh
@@ -200,6 +200,45 @@ else
     check "ppc_rldicl score 24/24"  "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
 fi
 
+# ---- ppcdsformxo (#571): the 64-bit DS-form loads and stores, opcodes 58 and 62 -- its 39-row detector ------
+# The decoder took the whole low halfword of an opcode-58 or opcode-62 word as the displacement and never read
+# the two-bit XO field: ldu, lwa and stdu executed as an 8-byte ld or std at EA + XO with no update, and the
+# reserved encodings (58 with XO 3, 62 with XO 2 or 3) executed as well.  BEFORE the NetBSD prerequisite for
+# the reason the rlwimi block gives: `-E bareppc -M 64' needs no image, so a red row is recorded first.  Eight
+# debugger-stepped sessions (loads, stores and five stop sessions, each stop word last) and one bogus-machine
+# session; the rung-3 witness of the loads (regress/artifacts/ppcdsformxo/witness_20261024/) is NOT run here.
+# Scored in the #565 shape: the completion sentinel exactly once and as the last line; each protocol key
+# exactly once in ANY form, then exactly once in its accepted form (the rldimi block's idiom); every row by
+# name; the census row at its frozen count of placed words; the emitted, green and red row counts -- each
+# pinned to a literal.  Names are at most 14 characters in a %-16s column, so `^name  ' cannot match a
+# neighbour (the padded-column trap).  Session transcripts go to $LOGDIR/ppc_dsform/.  Kill table:
+# regress/artifacts/ppcdsformxo/table1_20261024/.
+DSFLOG=$LOGDIR/ppc_dsform.log
+python3 -u ppc_dsform_probe.py "$PMAX" gate "$LOGDIR/ppc_dsform" > "$DSFLOG" 2>&1 || true
+if [ "$(grep -cx 'PPC_DSFORM_PROBE_DONE' "$DSFLOG")" != 1 ]; then
+    note "ppc_dsform: completion sentinel missing or duplicated; last lines follow"
+    tail -5 "$DSFLOG" | sed 's/^/       /'
+    check "ppc_dsform probe completed" "no" "yes"
+else
+    check "ppc_dsform probe completed" "yes" "yes"
+    check "ppc_dsform sentinel is the last line" "$(tail -n 1 "$DSFLOG")" "PPC_DSFORM_PROBE_DONE"
+    for k in RESULT CONTROL SYMPTOM RED; do
+        check "ppc_dsform $k= lines" "$(grep -c "^PPC_DSFORM_$k=" "$DSFLOG")" "1"
+    done
+    check "ppc_dsform RESULT=39/39"   "$(grep -cx 'PPC_DSFORM_RESULT=39/39' "$DSFLOG")" "1"
+    check "ppc_dsform CONTROL=OK"     "$(grep -cx 'PPC_DSFORM_CONTROL=OK' "$DSFLOG")" "1"
+    check "ppc_dsform SYMPTOM=ABSENT" "$(grep -cx 'PPC_DSFORM_SYMPTOM=ABSENT' "$DSFLOG")" "1"
+    check "ppc_dsform RED=none"       "$(grep -cx 'PPC_DSFORM_RED=none' "$DSFLOG")" "1"
+    for v in "ld value" "ld RA after" "ld ds0 value" "ld ra0 value" "ldu value" "ldu RA after" "ldu ds0 value" "lwa value" "lwa RA after" "lwa ds0 value" "lwa ra0 value" "lwz value" "lwz odd" "live" "std value" "std RA after" "std ds0 value" "std ra0 value" "stdu value" "stdu neigh" "stdu RA after" "stdu ds0 value" "stdu alias val" "stdu alias RA" "stw odd" "st live" "xo58_3 live" "xo58_3 bad" "xo62_2 live" "xo62_2 bad" "xo62_3 live" "xo62_3 bad" "ldu ra0 live" "ldu ra0 bad" "stdu ra0 live" "stdu ra0 bad" "unasm census" "word pins" "neg apparatus"; do
+        check "ppc_dsform row: $v" "$(count "$DSFLOG" "^$v  .*ok$")" "1"
+    done
+    check "ppc_dsform census, 108 placed words" "$(count "$DSFLOG" "^unasm census  *108/108  *108/108  .*ok$")" "1"
+    dsfok=$(count "$DSFLOG" " ok$"); dsfbad=$(count "$DSFLOG" " FAIL$"); dsfrun=$((dsfok + dsfbad))
+    check "ppc_dsform rows run"   "$dsfrun" 39
+    check "ppc_dsform rows green" "$dsfok" 39
+    check "ppc_dsform rows red"   "$dsfbad" 0
+fi
+
 need_file "$IMAGES/netbsd401-macppc-GENERIC"
 
 note "binary : $PMAX"
~~~~

What runs before it in the same gate, :94-104 (an absent binary is a SKIP of the whole gate -- K3), and the two idioms
B12 names -- the rldimi block's key-count (:137-160) and the `#565` block (:162-201), VERBATIM:

~~~~
94| set -u
95| cd "$(dirname "$0")"
96| . ./lib.sh
97| 
98| gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl"
99| 
100| PMAX=${PMAX:-$ROOT/build/gxemul}
101| LOG=$LOGDIR/gate_ppc.log
102| 
103| need_exec "$PMAX"
104| command -v python3 >/dev/null || gate_skip "python3 not available"
137| # ---- ppcrldimimask: X(rldimi) mask bounds + wrap (same shape, same reasons) ------------
138| RLDLOG=$LOGDIR/ppc_rldimi.log
139| python3 ppc_rldimi_probe.py "$PMAX" gate > "$RLDLOG" 2>&1 || true
140| #  Each KEY must occur exactly once in ANY form, and that one line must be well formed --
141| #  counting only well-formed lines let a malformed EXTRA `RESULT=' through (codex review).
142| rldres=$(grep -c '^PPC_RLDIMI_RESULT=' "$RLDLOG")
143| rldresok=$(grep -cE '^PPC_RLDIMI_RESULT=[0-9]+/[0-9]+$' "$RLDLOG")
144| rldctl=$(grep -c '^PPC_RLDIMI_CONTROL=' "$RLDLOG")
145| rldctlok=$(grep -cE '^PPC_RLDIMI_CONTROL=(OK|FAIL)$' "$RLDLOG")
146| rlddone=$(grep -c '^PPC_RLDIMI_PROBE_DONE' "$RLDLOG")
147| if [ "$rldres" = 1 ] && [ "$rldresok" = 1 ] && [ "$rldctl" = 1 ] && [ "$rldctlok" = 1 ] &&
148|    [ "$rlddone" = 1 ] && grep -qx 'PPC_RLDIMI_PROBE_DONE' "$RLDLOG"; then
149|     check "rldimi protocol parsed" "yes" "yes"
150|     grep -E " ok$| FAIL$" "$RLDLOG" | sed 's/^/       /'
151|     rld=$(grep '^PPC_RLDIMI_RESULT=' "$RLDLOG" | cut -d= -f2)
152|     check "rldimi controls prove the probe measures" \
153|           "$(grep '^PPC_RLDIMI_CONTROL=' "$RLDLOG" | cut -d= -f2)" "OK"
154|     check "rldimi rows run"     "${rld#*/}" 29
155|     check "rldimi rows correct" "${rld%/*}" 29
156| else
157|     note "rldimi: protocol lines missing or duplicated (result=$rldres control=$rldctl done=$rlddone)"
158|     tail -5 "$RLDLOG" | sed 's/^/       /'
159|     check "rldimi protocol parsed" "no" "yes"
160| fi
161| 
162| # ---- ppcrldiclzero (#522) + #565: X(rldicl) wrote ZERO on every execution -- its 24-row detector --------
163| # Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated three times by owner ruling (2026-09-18 with
164| # ten others, eec0f4a3; 2026-09-24 with nine others; 04f3e7c0 on 2026-10-09) because no block here
165| # scored it; #565 discharges that exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc -M 64`
166| # needs no image, so a red row is recorded first.  A stalled guest cannot hang the gate: the probe's
167| # own subprocess backstops (90 s; 60 s for the bogus-machine and 32-bit sessions) turn it into
168| # failing rows.  The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores
169| # mk48's: its completion sentinel, then EVERY row by name, then the run/green/red counts and its own
170| # SCORE line, each pinned to a literal so a shrunk or renamed table cannot pass -- 30 checks when
171| # green.  Names sit in a %-18s column and none is longer than 15, so `^name  ' cannot match a
172| # neighbour (the padded-column trap).  The rows-run line is in the form check_score_claims.py pins.
173| # CONTRACT: the block TRANSMITS the probe's verdicts and re-derives none -- each row's ok/FAIL and its
174| # SCORE come from one comparison in the probe's row(), so an edit there (Grok 4.7's `ok = True', GPT-6
175| # Astra's `>=', #565 pass 2) lets a mutant through, as it would through any block that scores only a
176| # probe's ok/FAIL tokens (some gate_arm.sh blocks also pin a got= value; this one, like mk48's, does not).
177| # The exit status is ignored on purpose: this probe exits 0 with failed rows (probeexitzero).
178| # Floor (c), measured (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/): an IDENTITY
179| # BODY for X(rldicl) -- decode and retire, write nothing -- reds 11 of the 30 (identity/), and
180| # /bin/true 22 of the 30.  An absent binary reds the sentinel check in this block's scoring text, but
181| # in gate 13 need_exec turns it into a SKIP before any check.
182| RLCLOG=$LOGDIR/ppc_rldicl.log
183| python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
184| if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
185|     note "ppc_rldicl: completion sentinel missing or duplicated; last lines follow"
186|     tail -5 "$RLCLOG" | sed 's/^/       /'
187|     check "ppc_rldicl probe completed" "no" "yes"
188| else
189|     check "ppc_rldicl probe completed" "yes" "yes"
190|     for v in "session" "live" "seed holds" "src intact" "disasm xcheck" "zx32 rldicl" "zx32 rldicr" "rot8 rldicl" "rot8 rldicr" "naive fix wrong" "neg apparatus" "bits32 live" "bits32 rld bad" "vacuous cell" "vac neighbour" "census run" "census wrong" "census zero" "disasm total" "cand session" "cr parsed" "sh63 rldicl" "sh32 rldicl" "rc cr0"; do
191|         check "ppc_rldicl row: $v" "$(count "$RLCLOG" "^$v  .*ok$")" "1"
192|     done
193|     rlcok=$(count "$RLCLOG" " ok$"); rlcbad=$(count "$RLCLOG" " FAIL$"); rlcrun=$((rlcok + rlcbad))
194|     check "ppc_rldicl rows run"   "$rlcrun" 24
195|     check "ppc_rldicl rows green" "$rlcok" 24
196|     check "ppc_rldicl rows red"   "$rlcbad" 0
197|     #  EVERY SCORE line is counted, then the one is read: counting only `SCORE 24/24' lines let an
198|     #  appended contradictory `SCORE 0/24' pass (GPT-6 Astra, pass 1).
199|     check "ppc_rldicl score lines"  "$(grep -c '^SCORE ' "$RLCLOG")" "1"
200|     check "ppc_rldicl score 24/24"  "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
201| fi
~~~~

`regress/lib.sh` -- `check` :80-88, `gate_skip` :137-145, `need_file` / `need_exec` :147-157, `count` :326-331, VERBATIM:

~~~~
80| check() {
81|     _checks=$((_checks+1))
82|     if [ "$2" = "$3" ]; then
83|         printf "  ${C_OK}ok${C_OFF}   %-52s %s\n" "$1" "$2"
84|     else
85|         printf "  ${C_BAD}FAIL${C_OFF} %-52s got=%s want=%s\n" "$1" "$2" "$3"
86|         _fails=$((_fails+1))
87|     fi
88| }
137| gate_skip() {
138|     echo
139|     if [ "${_fails:-0}" != 0 ]; then
140|         echo "${C_BAD}$GATE_NAME: FAIL${C_OFF} ($_fails of $_checks checks failed" \
141|              "before this section could not run: $*)"
142|         exit 1
143|     fi
144|     echo "${C_SKIP}$GATE_NAME: SKIP${C_OFF} -- $*"; exit $EXIT_SKIP
145| }
146| 
147| need_file() {
148|     for f in "$@"; do
149|         [ -e "$f" ] || gate_skip "missing required input: $f"
150|     done
151| }
152| 
153| need_exec() {
154|     for f in "$@"; do
155|         [ -x "$f" ] || gate_skip "missing or non-executable binary: $f"
156|     done
157| }
326| count() {
327|     [ -f "$1" ] || { echo 0; return; }
328|     local c
329|     c=$(grep -ac -- "$2" "$1" 2>/dev/null)
330|     echo "${c:-0}"
331| }
~~~~

### 3.2 The MANIFEST keys -- `table1_20261024/staged/INSERTIONS.txt`, VERBATIM (both insertions, the checks run, what the landing owes)

~~~~
INSERTIONS -- round #571 (ppcdsformxo): gate 13 block and the two MANIFEST keys, written 2026-10-24

N = 39    regress/ppc_dsform_probe.py md5 0266228894811ba6c51cff82585753c9 (40883 bytes)
The literal 39 in the gate pins (RESULT=39/39, rows run, rows green) and the census pin (108/108) come
from that file: ROW_NAMES has 39 entries and its seven guest sessions place 108 words (DETECTOR_FREEZE.txt).

== 1. regress/gate_ppc.sh
before the edit: 'git show HEAD:regress/gate_ppc.sh | cmp - regress/gate_ppc.sh' -> no output, status 0
(working tree == HEAD, md5 7a970b9a979dcd73da0f265abbecb847).
staged copy: staged/gate_ppc.sh.txt, made from 'git show HEAD:regress/gate_ppc.sh', the same insertion applied.
anchor: the #565 block's closing 'fi', then the blank line and need_file "$IMAGES/netbsd401-macppc-GENERIC"
(found once in each file); the block goes between them, so need_file stays the next statement after it.

-- diff HEAD-blob regress/gate_ppc.sh (working tree, after):
202a203,241
> # ---- ppcdsformxo (#571): the 64-bit DS-form loads and stores, opcodes 58 and 62 -- its 39-row detector ------
> # The decoder took the whole low halfword of an opcode-58 or opcode-62 word as the displacement and never read
> # the two-bit XO field: ldu, lwa and stdu executed as an 8-byte ld or std at EA + XO with no update, and the
> # reserved encodings (58 with XO 3, 62 with XO 2 or 3) executed as well.  BEFORE the NetBSD prerequisite for
> # the reason the rlwimi block gives: `-E bareppc -M 64' needs no image, so a red row is recorded first.  Eight
> # debugger-stepped sessions (loads, stores and five stop sessions, each stop word last) and one bogus-machine
> # session; the rung-3 witness of the loads (regress/artifacts/ppcdsformxo/witness_20261024/) is NOT run here.
> # Scored in the #565 shape: the completion sentinel exactly once and as the last line; each protocol key
> # exactly once in ANY form, then exactly once in its accepted form (the rldimi block's idiom); every row by
> # name; the census row at its frozen count of placed words; the emitted, green and red row counts -- each
> # pinned to a literal.  Names are at most 14 characters in a %-16s column, so `^name  ' cannot match a
> # neighbour (the padded-column trap).  Session transcripts go to $LOGDIR/ppc_dsform/.  Kill table:
> # regress/artifacts/ppcdsformxo/table1_20261024/.
> DSFLOG=$LOGDIR/ppc_dsform.log
> python3 -u ppc_dsform_probe.py "$PMAX" gate "$LOGDIR/ppc_dsform" > "$DSFLOG" 2>&1 || true
> if [ "$(grep -cx 'PPC_DSFORM_PROBE_DONE' "$DSFLOG")" != 1 ]; then
>     note "ppc_dsform: completion sentinel missing or duplicated; last lines follow"
>     tail -5 "$DSFLOG" | sed 's/^/       /'
>     check "ppc_dsform probe completed" "no" "yes"
> else
>     check "ppc_dsform probe completed" "yes" "yes"
>     check "ppc_dsform sentinel is the last line" "$(tail -n 1 "$DSFLOG")" "PPC_DSFORM_PROBE_DONE"
>     for k in RESULT CONTROL SYMPTOM RED; do
>         check "ppc_dsform $k= lines" "$(grep -c "^PPC_DSFORM_$k=" "$DSFLOG")" "1"
>     done
>     check "ppc_dsform RESULT=39/39"   "$(grep -cx 'PPC_DSFORM_RESULT=39/39' "$DSFLOG")" "1"
>     check "ppc_dsform CONTROL=OK"     "$(grep -cx 'PPC_DSFORM_CONTROL=OK' "$DSFLOG")" "1"
>     check "ppc_dsform SYMPTOM=ABSENT" "$(grep -cx 'PPC_DSFORM_SYMPTOM=ABSENT' "$DSFLOG")" "1"
>     check "ppc_dsform RED=none"       "$(grep -cx 'PPC_DSFORM_RED=none' "$DSFLOG")" "1"
>     for v in "ld value" "ld RA after" "ld ds0 value" "ld ra0 value" "ldu value" "ldu RA after" "ldu ds0 value" "lwa value" "lwa RA after" "lwa ds0 value" "lwa ra0 value" "lwz value" "lwz odd" "live" "std value" "std RA after" "std ds0 value" "std ra0 value" "stdu value" "stdu neigh" "stdu RA after" "stdu ds0 value" "stdu alias val" "stdu alias RA" "stw odd" "st live" "xo58_3 live" "xo58_3 bad" "xo62_2 live" "xo62_2 bad" "xo62_3 live" "xo62_3 bad" "ldu ra0 live" "ldu ra0 bad" "stdu ra0 live" "stdu ra0 bad" "unasm census" "word pins" "neg apparatus"; do
>         check "ppc_dsform row: $v" "$(count "$DSFLOG" "^$v  .*ok$")" "1"
>     done
>     check "ppc_dsform census, 108 placed words" "$(count "$DSFLOG" "^unasm census  *108/108  *108/108  .*ok$")" "1"
>     dsfok=$(count "$DSFLOG" " ok$"); dsfbad=$(count "$DSFLOG" " FAIL$"); dsfrun=$((dsfok + dsfbad))
>     check "ppc_dsform rows run"   "$dsfrun" 39
>     check "ppc_dsform rows green" "$dsfok" 39
>     check "ppc_dsform rows red"   "$dsfbad" 0
> fi
> 

-- diff HEAD-blob staged/gate_ppc.sh.txt: identical to the hunk above:
   'diff <that diff> <this diff>' -> no output, status 0 (the two insertions are identical)
   'cmp regress/gate_ppc.sh staged/gate_ppc.sh.txt' -> no output, status 0
   both pure insertions of 39 lines (no deleted lines); 'bash -n' clean on both.

== 2. tools/pipeline/check_probe_wiring.py (the MANIFEST)
working tree before the edit: md5 da65493d6248edf0bcdedeb63ae3022b (carries uncommitted peer edits; differs from HEAD).
HEAD blob: md5 2a98b470969f0d49d748c3b18790d71b; staged copy staged/check_probe_wiring.py.txt made from it.
anchor: the last line of the #570 witness entry ('...24/24 on the fixed build (table1_20261023/fixed_witness24.out)"),')
followed by the MANIFEST's closing '}' -- found once in each file; the two keys go between them.

-- diff working-tree-before tools/pipeline/check_probe_wiring.py (after):
3236a3237,3238
>     "ppc_dsform_probe.py": (CLASS_DETECTOR, "#571 ppcdsformxo: the 64-bit DS-form loads and stores (opcodes 58 and 62: ld, ldu, lwa, std, stdu, the reserved XO encodings, and ldu/stdu with RA = 0) -- 39 rows on unmodified -E bareppc -M 64; gated in gate_ppc.sh (gate 13) under the stem ppc_dsform, pinned at 39; kill table artifacts/ppcdsformxo/table1_20261024/ (SCORES.txt)"),
>     "artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py": (CLASS_WITNESS, "#571 ppcdsformxo: the rung-3 pre-fix witness of the LOADS (8 rows, md5 5e96b69d) -- 5/8 on HEAD (witness_20261024/WITNESS_headbin.out); its post-fix run is table1_20261024/fixed_witness8.out, and the stores' pre-fix artifact is table1_20261024/prefix_BASE.out"),

-- diff HEAD-blob staged/check_probe_wiring.py.txt (after):
3221a3222,3223
>     "ppc_dsform_probe.py": (CLASS_DETECTOR, "#571 ppcdsformxo: the 64-bit DS-form loads and stores (opcodes 58 and 62: ld, ldu, lwa, std, stdu, the reserved XO encodings, and ldu/stdu with RA = 0) -- 39 rows on unmodified -E bareppc -M 64; gated in gate_ppc.sh (gate 13) under the stem ppc_dsform, pinned at 39; kill table artifacts/ppcdsformxo/table1_20261024/ (SCORES.txt)"),
>     "artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py": (CLASS_WITNESS, "#571 ppcdsformxo: the rung-3 pre-fix witness of the LOADS (8 rows, md5 5e96b69d) -- 5/8 on HEAD (witness_20261024/WITNESS_headbin.out); its post-fix run is table1_20261024/fixed_witness8.out, and the stores' pre-fix artifact is table1_20261024/prefix_BASE.out"),

-- the two insertions compared with their hunk headers removed (line numbers differ: 3237-3238 in the
   working tree, 3222-3223 in the HEAD copy, because of the peer's edits above the anchor):
   no output, status 0 (identical)
   both pure insertions of 2 lines; no other line of either file changed.

== 3. md5 after the edits
0266228894811ba6c51cff82585753c9  regress/ppc_dsform_probe.py
d361db091a3d545b280acab979c5c241  regress/gate_ppc.sh
d361db091a3d545b280acab979c5c241  regress/artifacts/ppcdsformxo/table1_20261024/staged/gate_ppc.sh.txt
5e944fd659e697e75e842076dd4621e0  tools/pipeline/check_probe_wiring.py
4e237f85f75f317b44d5966fc07bb55e  regress/artifacts/ppcdsformxo/table1_20261024/staged/check_probe_wiring.py.txt
all four edited files are LF-only (0 CR bytes) and 'file -b' reports no CRLF.

== 4. checks run here (read-only, no build, no emulator)
  * 'python tools/pipeline/check_probe_wiring.py --selftest' (temp copies): PROBEWIRING_SELFTEST_PASS 22/22.
  * 'python tools/pipeline/check_probe_wiring.py': PROBEWIRING_FAIL 7 problems -- GHOST for both new keys
    (neither probe file is staged yet; domain() reads git ls-files) plus five GHOSTs already in the
    peer's working-tree MANIFEST (b115, fbclearread, wdcnullxfer x2, wdcrearmzero).  The two new GHOSTs
    clear when regress/ppc_dsform_probe.py and artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py
    are staged.
  * 'python tools/pipeline/check_score_claims.py': SCORE_CLAIMS_PASS, SCORE_CLAIMS_PINNED=39 (was 38): the
    new 'ppc_dsform rows run' pin is seen, and no comment line naming ppc_dsform nor the probe's docstring
    carries a stale score claim.

== 5. owed by the landing commit (not edited here: tools/ is outside this task except the two keys)
  * tools/precommit_check.sh: SCORE_CLAIMS_MANIFEST=38 must be raised to 39, deliberately, with its
    history line (one newly gated probe: ppc_dsform_probe.py, pinned UNQUOTED in gate_ppc.sh at 39 rows
    under the stem ppc_dsform; its docstring is checked).  Until then precommit section U reports
    'SCORE-CLAIM COVERAGE GREW: 39 probes pinned, manifest says 38'.
  * gate_ppc.sh's gate_begin title still names only 'rlwimi/rldimi/rldicl'; not changed (one insertion only).
  * gate 13's new block runs 53 checks when green (1 completed + 1 last line + 4 key counts + 4 accepted
    forms + 39 rows + 1 census + 3 counts).
~~~~

The anchor at HEAD -- `git show HEAD:tools/pipeline/check_probe_wiring.py`, lines 3214-3222 (the `#570` entries the keys follow):

~~~~
3214|                          "rev 2 (md5 d57c12ab), shipped as documentation revision 2c (md5 a49f417d, a docstring-only "
3215|                          "re-freeze: repair1_20261024/rev2c_equivalence.txt); kill table "
3216|                          "artifacts/m88kbuserrregs/table1_20261023/ (SCORES.txt): pre-fix HEAD 21/31, fixed 31/31, "
3217|                          "null medium 1/31 CONTROL=FAIL, all 20 variant legs red, 27 of 27 measurements as predicted "
3218|                          "(L22's prediction: BUILDER_QUESTIONS Q18 / BUILD_SPEC section 11 Q18)"),
3219|     "artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py":
3220|         (CLASS_WITNESS, "#570 m88kbuserrregs: the rung-3 pre-fix witness (rev 1, 24 rows, md5 d59798b0) -- 16/24 on HEAD "
3221|                         "(witness_20261023/WITNESS_headbin.out), 24/24 on the fixed build (table1_20261023/fixed_witness24.out)"),
3222| }
~~~~

### 3.3 `tools/precommit_check.sh` -- the diff, VERBATIM (`diff_precommit.patch`; reproduces the working tree)

~~~~
diff --git a/tools/precommit_check.sh b/tools/precommit_check.sh
index 23356b64..57afe9a7 100644
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -361,7 +361,9 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  RAISED 37 -> 38 ON 2026-10-24, DELIBERATELY.  One newly gated probe: m88k_buserr_probe.py
 	#  (#570, pinned UNQUOTED in gate_arm.sh at 31 rows under the stem m88k_buserr; the probe's own
 	#  docstring is checked -- its score-shaped strings were reworded in its documentation revision 2c).
-	SCORE_CLAIMS_MANIFEST=38
+	#  RAISED 38 -> 39 ON 2026-10-24, DELIBERATELY.  One newly gated probe: ppc_dsform_probe.py
+	#  (#571, pinned UNQUOTED in gate_ppc.sh at 39 rows under the stem ppc_dsform; its docstring is checked).
+	SCORE_CLAIMS_MANIFEST=39
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
~~~~

---

## 4. The measurements -- `regress/artifacts/ppcdsformxo/table1_20261024/`

### 4.1 Order (mtimes, read at drafting) -- each artifact precedes what it must precede

| time (2026-10-24) | artifact |
|---|---|
| 07:54:42 | `BASELINE.out` written (its last line appended 08:29:04) |
| 07:56:54 | `PRETABLE.out` |
| 08:26:52 | `regress/ppc_dsform_probe.py` (the detector) |
| 08:27:36 | `DETECTOR_FREEZE.txt` |
| 08:29:04-08:29:05 | the freeze line in `BASELINE.out`; `prefix_BASE.out` (the BASE binary) |
| 08:30:55-08:32:06 | the fix applied in the work clone, rebuilt, `fixed.out`, `fixed_witness8.out` (`s5_fix_build.out`) |
| 08:32:01 | `PREDICTIONS.txt` |
| 08:34:28-08:54:13 | the sixteen legs and L5b (`s6_all.out`); `SCORES.txt` 08:55:33 |
| 08:56:08-09:03:35 | propagation and the two-part clearance (`CLEARANCE.out`) |
| 09:03:54-09:05:23 | gate 13 alone (`gate13_20261024.out`) |
| 09:06:04 | `BUILD_REPORT.md` |

### 4.2 `BASELINE.out`, VERBATIM (indented two spaces, like `PRETABLE.out`, the gate-log excerpt, `C0_OUTPUT.txt`, the three drafts, `BUILD_REPORT.md` and `LS_PERMITTED.txt` below, so that their own `#` headings stay inside this brief's sections; nothing else is changed)

~~~~
  # BASELINE.out -- #571 (ppcdsformxo), written 2026-10-24 07:54:42 -0500 by the main loop (the S2 agent's responses were withheld twice; read-only commands only)
  HEAD: add098b9d94221c623e23fdd13fa26ec2793ab63 2026-10-24 05:24:44 -0500 records: `m88kbuserrregs` names its landing commit c8
  ## md5 of src/cpus/cpu_ppc_instr.c per tree (Windows side)
  C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC         87a766e0a8c1f8bbc41ebea8d9255d27
  C:/DocumentNoSnc/cc/GXEMUL/est                87a766e0a8c1f8bbc41ebea8d9255d27
  C:/DocumentNoSnc/cc/GXEMUL/build              87a766e0a8c1f8bbc41ebea8d9255d27
  C:/DocumentNoSnc/cc/GXEMUL/build-asan         87a766e0a8c1f8bbc41ebea8d9255d27
  ## HEAD blob md5: 87a766e0a8c1f8bbc41ebea8d9255d27
  ## binary freshness (Windows side): [ gxemul -nt src/cpus/cpu_ppc_instr.c ]
  C:/DocumentNoSnc/cc/GXEMUL/build: FRESH (binary 2026-10-24_04:07:57, source 2026-10-18_23:22:10)
  C:/DocumentNoSnc/cc/GXEMUL/build-asan: FRESH (binary 2026-10-24_04:10:05, source 2026-09-12_01:57:31)
  ## est/: source tree, part 2 N/A
  ## WSL side (script: scratchpad t2/build/baseline_wsl.sh)
  cc: cc (Gentoo 15.2.1_p20260214 p5) 15.2.1 20260214
  /tmp/gxsec-build     md5 87a766e0a8c1f8bbc41ebea8d9255d27  binary FRESH
  /tmp/gxt2/base       md5 87a766e0a8c1f8bbc41ebea8d9255d27  binary FRESH
  /tmp/gxt2/work       ABSENT
  base binary md5: 3cd0501cf7c854e0662797ccee1fce64  (witness recorded 3cd0501cf7c854e0662797ccee1fce64)
  no .MUTANT sentinel in /tmp/gxt2/base
  no legs dir yet
  DETECTOR FROZEN 2026-10-24 08:29:04: regress/ppc_dsform_probe.py md5 0266228894811ba6c51cff82585753c9, 40883 bytes (DETECTOR_FREEZE.txt; N = 39) -- frozen BEFORE prefix_BASE.out
~~~~

### 4.3 `PRETABLE.out` (written before the detector existed), VERBATIM

~~~~
  # PRETABLE.out -- #571 (ppcdsformxo), written 2026-10-24 ~08:0x by the main loop BEFORE table 1 (its mtime is the order proof)
  # Spec: BUILD_SPEC.md section 2 item 2, with sections 10 and 10b applied.  Rows are the amended list (8 sessions, N = 39);
  # legs are section 6 as amended (L4a == L7, one leg; L8c scored as emulator termination; L9 split into L9a/L9b).
  # Line numbers: HEAD add098b9, src/cpus/cpu_ppc_instr.c unless named.

  ## 1. SIBLING PARITY -- the five DS forms against each other, and against the arm's D-form siblings
  form   | opcode/XO | flags after the repair           | writes RA | extension        | rows (value / RA / DS=0 / RA=0)
  ld     | 58 / 0    | load=1 size=3 zero=1 update=0    | no        | n/a (8 bytes)    | ld value / ld RA after / ld ds0 value / ld ra0 value
  ldu    | 58 / 1    | load=1 size=3 zero=1 update=1    | YES       | n/a              | ldu value / ldu RA after / ldu ds0 value / ldu ra0 bad (refusal)
  lwa    | 58 / 2    | load=1 size=2 zero=0 update=0    | no        | sign (int32_t)   | lwa value / lwa RA after / lwa ds0 value / lwa ra0 value
  std    | 62 / 0    | load=0 size=3 zero=1 update=0    | no        | n/a              | std value / std RA after / std ds0 value / std ra0 value
  stdu   | 62 / 1    | load=0 size=3 zero=1 update=1    | YES       | n/a              | stdu value (+ stdu neigh) / stdu RA after / stdu ds0 value / stdu ra0 bad (refusal)
  58 / 3, 62 / 2, 62 / 3: reserved -> goto bad (rows xo58_3 bad, xo62_2 bad, xo62_3 bad, each own session).
  Parity holds: every legal form has a value row, an RA row (an ungraded RA observation where RA = 0 cannot carry one),
  a DS = 0 row and an RA = 0 row (a refusal row for the update forms).  The one asymmetric axis is the extension, which
  only lwa has (its sign is pinned by the bit-31-set word); std/stdu have no extension axis (N/A, not a missing row).
  D-form siblings reached by DIFFERENT case labels with the SAME flags: lwzu (size 2, zero 1, update 1) ~ ldu's shape;
  lha (size 1, zero 0) ~ lwa's shape; stwu ~ stdu's shape.  None of them checks RA = RT either (:4299-4326) -- the
  repair's D1 disclosure is sibling-consistent.  The D-form siblings are rowed only as SCOPE controls (lwz odd, stw odd):
  they must be UNCHANGED, which is what the shared assignment at :4295 being untouched means.

  ## 2. CLAIM -> ROW -- every sentence the #571 comment and the probe's contract will assert
  claim (the comment / contract sentence)                                           | row(s) that observe it           | leg that reds it
  the low two bits are XO; the displacement is EXTS(DS || 0b00)                      | ldu value, lwa value, stdu value, ldu/lwa/stdu ds0 value | L7, L3
  ldu and stdu write RA = EA                                                         | ldu RA after, stdu RA after, stdu alias RA | L6a, L6b, L3, L4b, L4c
  lwa is a sign-extending WORD load                                                   | lwa value, lwa ra0 value          | L8a (8 bytes), L8b (zero-ext), L3, L4b
  reserved XO 58/3, 62/2, 62/3 stop the cpu (bare goto bad; UNIMPLEMENTED line)        | xo58_3 bad, xo62_2 bad, xo62_3 bad | L12b, L12a, L3, L4b, L4c
  ldu/stdu with RA = 0 stop through the existing guard (:4338-4342)                  | ldu ra0 bad, stdu ra0 bad         | L6a, L6b, L3, L4b, L4c, L5
  ld/std and the other 22 opcodes of the arm are unchanged                           | ld value, std value, ld RA after, std RA after, lwz odd, stw odd | L9a, L9b, L10, L11
  no handler change (every form selects an existing slot)                           | NO ROW: a build fact (the slots named in the record; the table is generated) | --
  32-bit CPUs decode unchanged; no width test; MODE32 handlers are real             | NO ROW: disclosed in NOT CLAIMED (A6)  | --
  ldu RA = RT disclosed, not checked                                                 | NO ROW: disclosed (D1)                 | --
  the census attests opcode/RT/RA/raw halfword against the CURRENT disassembler text | unasm census, word pins (observations, apparatus) | an encoder error, not a product leg
  the store half's clause (a) is prefix_BASE.out                                      | every store symptom row            | the BASE run itself (L2)

  ## 3. GUARD FIELD vs BODY FIELD -- the predicates dominating the edited lines, the lvalues the body reads, the partition the body induces
  edited lines: the two case bodies inside `switch (main_opcode)` at :4298 (case PPC_HI6_LD :4307, case PPC_HI6_STD :4320).
  dominating predicates: the outer case labels :4269-4292 (24 opcodes), the inner `switch (main_opcode)`, the new `switch (iword & 3)`.
  body-read lvalues after the edit (the common tail :4328-4351):
    imm      tested `imm == 0` (:4335, table index)        partition {0, != 0}  -> EXHAUSTED per form (ds0 rows + DS != 0 rows); VALUES sampled (-112, -96, 8, 0, 0x7000, ...)
    ra       tested `ra == 0 && update` (:4338), `ra == 0` (:4347)   partition {0, != 0}  -> EXHAUSTED per form (ra0 rows: legal access for ld/lwa/std, refusal for ldu/stdu); the imm==0 x ra==0 JOINT cells are NOT rowed (disclosed: ldu/stdu ra0z, ld/std both, lwa ra0z)
    update   written by the repair (XO 1), read by :4338 and the table index       {0, 1} -> EXHAUSTED (both forms of each opcode)
    size/zero/load  written by the repair, read by the table index only           derived from (opcode, XO) -> EXHAUSTED through the five forms + the three reserved XOs
    fp       tested :4343; 0 for every 58/62 word (the FP labels set it)            {0} for this round -> N/A (a producer relationship, not an axis)
    ic->f    tested :4328 (NULL -> table); set by the FP cases only                 derived from the label -> N/A for 58/62
    rs/rt    arg[0]; never tested against ra                                       RA = RT (ldu) DISCLOSED; RA = RS (stdu, valid) rowed by choice (stdu alias val / RA)
    main_opcode  the label axis: 58 and 62 rowed exhaustively; two D-form labels (lwz, stw) rowed as scope controls; the other 20 labels SAMPLED by the rounding probe (FP D-forms, stw) and the NetBSD boot when the image is present -- they do not reach the edited lines (B7, F1)
  where guard and body fields DIFFER: the repair's guard is (main_opcode, iword & 3); the body additionally reads imm and ra.  Both are written/available at the same site (decode of one word), so no "disagreeing state" row is owed -- the partitions above are the rows.

  ## 4. CHANNEL per row -- the leg it kills and the observable that differs (names <= 14 chars; the stop rows' channel is the UNIMPLEMENTED line + sentinel/window + RA)
  session LOADS (bareppc -M 64; counting pattern at 0x20000..; seeded window at 0x7000.. for RA = 0; sentinel registers)
    ld value       kills L5 (RT keeps the sentinel), L9b (bytes at +1)                  obs: the 8 bytes at offset 0x10
    ld RA after    kills L9a, L10 (RA written)                                           obs: RA == base
    ld ds0 value   kills L5, L9b                                                         obs: the 8 bytes at RA (the address channel; NOT the table half -- F2)
    ld ra0 value   kills L5, L9b, L9a (at RA = 0 an added update becomes a refusal)      obs: the 8 bytes at the absolute address (the seeded window)
    ldu value      kills L3, L7 (EA + 1), L5                                             obs: the 8 bytes at offset 0x20 vs 0x21
    ldu RA after   kills L3, L4b, L6a, L5                                                obs: RA == EA
    ldu ds0 value  kills L7 (RA + 1), L3                                                 obs: the 8 bytes at RA
    lwa value      kills L3, L4b, L7 (EA + 2), L8a (8 bytes), L8b (zero-extended), L5    obs: 0xffffffff88898a8b (bit 31 set)
    lwa RA after   kills L10                                                             obs: RA == base
    lwa ds0 value  kills L7 (RA + 2), L3                                                 obs: the sign-extended word at RA
    lwa ra0 value  kills L5, L8a, L8b, L9b                                               obs: the sign-extended word at the absolute address
    lwz value      CONTROL (no product leg varies it): corroborates the pattern at lwa's word   obs: 0x88898a8b
    lwz odd        kills L11 (a mask on the shared assignment reads +4 for +6)           obs: 0x06070809
    live           kills L8c (the session's emulator terminates before the li) and any dead session   obs: the li value
  session STORES (seeded window at 0x21000.. and at 0x7100.. / 0x0.. for RA = 0 / DS = 0; sources = 8 distinct bytes; readback = debugger dump)
    std value      kills L5, L9b                                                         obs: the 8 bytes at EA
    std RA after   kills L9a, L10                                                        obs: RA == base
    std ds0 value  kills L5, L9b                                                         obs: the 8 bytes at RA
    std ra0 value  kills L5, L9b, L9a                                                    obs: the 8 bytes at the absolute address
    stdu value     kills L3, L4c, L7, L5                                                 obs: the 8 bytes at EA (not EA + 1)
    stdu neigh     kills L3, L4c, L7                                                     obs: flank bytes EA-1 and EA+8..EA+11 keep the seed
    stdu RA after  kills L3, L4c, L6b, L5                                                obs: RA == EA
    stdu ds0 value kills L7, L3                                                          obs: the 8 bytes at RA
    stdu alias val kills L3, L7, L5                                                      obs: the 8 bytes at EA equal the OLD base value (by-choice row, C18)
    stdu alias RA  kills L6b, L4c, L3                                                    obs: RA == EA
    stw odd        kills L11                                                             obs: the 4 bytes at +6
    st live        kills a dead stores session                                           obs: the li value
  sessions STOP (one word each, li before it; rows <name> live / <name> bad)
    xo58_3 bad     kills L3, L4b, L12b                                                   obs: UNIMPLEMENTED line present; RT == sentinel; RA == base
    xo62_2 bad     kills L3, L4c                                                         obs: UNIMPLEMENTED line; the window at EA-1..EA+11 keeps its seed; RA == base
    xo62_3 bad     kills L3, L4c, L12a                                                   obs: as xo62_2
    ldu ra0 bad    kills L3, L4b, L6a, L5                                                obs: UNIMPLEMENTED line; RT == sentinel
    stdu ra0 bad   kills L3, L4c, L6b, L5                                                obs: UNIMPLEMENTED line; the window at the absolute target keeps its seed
    <name> live    apparatus: the session reached the word (red only if the session died before it)
  global
    unasm census   apparatus (the hand-assembled-encoding guard; expected text = the tree's CURRENT disassembler); red under L5b (no output)
    word pins      apparatus: the three witness words equal their literals
    neg apparatus  apparatus: the bogus machine TYPE exits 1 with no registers
  Rows whose channel cannot vary under their named leg: NONE -- every product-leg assignment above names an observable that differs.
  Known non-assignments (so nobody reads them as kills): RA rows at DS = 0 (RA <- RA is invisible: no DS = 0 RA row exists);
  ds0 value rows vs the table half (unobservable on PPC970); `stdu neigh` under L5 (green: nothing is stored); `lwz value` under
  every product leg (green).

  ## 5. DIFF AGAINST THE BRIEF'S SECTION 7 (26 cells) AND RULINGS B4-B7 / F1 / F2
  Rowed: C1 (+RA row), C2 (ld ds0 -- added by F1, kept by F2 as a single-axis marginal), C3 (ld ra0 -- added by F1/F2),
  C4 (value + RA), C5, C6 (DS != 0 only), C8 (+RA row), C10, C11 (lwa ra0 -- added by F1/F2), C12, C13 (value + RA),
  C14 split into std ds0 and std ra0 (added by F1/F2), C15 (value + neigh + RA), C16, C17 (DS != 0 only), C18 (by choice:
  value + RA), C19, C20, C21, C22.  Disclosed, not rowed: C7 (RA = RT), C9 (positive-word lwa), C23 (FP / update D-forms
  beyond the two scope controls), C24 (32-bit), C25 (disassembler text), C26 (access failure; -T gated), and the three
  multi-axis joints F2 removed from F1's list (ld DS=0&RA=0, std DS=0&RA=0, lwa RA=0&DS=0) plus the two DS=0 RA=0 update
  refusals (ldu/stdu ra0z).  Changes from the brief: the brief's C14 lumped two cells (split); the brief's "lwa left at
  size 3 consumes the neighbour word" gloss is wrong (L8c is an emulator exit); the brief had no RA rows for the XO-0
  forms (B2 adds three); the brief's P2 sentence was inverted (M5).  Session count 8 (brief: unspecified; Codex 12; Grok 8).
~~~~

### 4.4 Pre-fix -- `prefix_BASE.out` on the BASE binary (md5 `3cd0501c`, built from HEAD's `src/`), every line but the `OBS` lines, VERBATIM

This is the STORE half's clause-(a) artifact (B1): 22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17.

~~~~
ppcdsformxo RUNG-3 DETECTOR for the 64-bit DS-form loads and stores (opcodes 58 and 62, #571) -- binary=/tmp/gxt2/base/gxemul label=prefix_BASE
binary md5=3cd0501cf7c854e0662797ccee1fce64
machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970, 64-bit)
wants: _scratchpad/ppc_uisa_book1_v201.txt :2350-2367 (ld) :2372-2395 (ldu) :2297-2317 (lwa) :2573-2593 (std) :2595-2621 (stdu) :2244 (lwz) :2518-2541 (stw); DS || 0b00 sign-extended :951-955 :1221-1227
CODE=0x10000 DATA=0x20000 STORE=0x21000 LOWLD=0x7000 LOWST=0x7100 placed words=108
row              got                  want                 note                                                 
ld value         0x1011121314151617   0x1011121314151617   XO 0 control: MEM(EA,8), EA = DATA+0x10              ok
ld RA after      0x20080              0x20080              XO 0, DS != 0: RA unchanged (r20)                    ok
ld ds0 value     0x4041424344454647   0x4041424344454647   XO 0, DS = 0: MEM(RA,8), RA = DATA+0x40              ok
ld ra0 value     0x80828486888a8c8e   0x80828486888a8c8e   XO 0, RA = 0: MEM(0x7000,8), absolute                ok
ldu value        0x2122232425262728   0x2021222324252627   XO 1: MEM(EA,8), EA = DATA+0x20                      FAIL
ldu RA after     0x20080              0x20020              XO 1, DS != 0: RA <- EA (r21)                        FAIL
ldu ds0 value    0x3132333435363738   0x3031323334353637   XO 1, DS = 0: MEM(RA,8), RA = DATA+0x30              FAIL
lwa value        0x8a8b8c8d8e8f9091   0xffffffff88898a8b   XO 2: EXTS(MEM(EA,4)), EA = DATA+0x88                FAIL
lwa RA after     0x20080              0x20080              XO 2, DS != 0: RA unchanged (r22)                    ok
lwa ds0 value    0x9293949596979899   0xffffffff90919293   XO 2, DS = 0: EXTS(MEM(RA,4)), RA = DATA+0x90        FAIL
lwa ra0 value    0x8c8e90929496989a   0xffffffff888a8c8e   XO 2, RA = 0: EXTS(MEM(0x7004,4)), absolute          FAIL
lwz value        0x88898a8b           0x88898a8b           D-form control: MEM(EA,4), EA = DATA+0x88            ok
lwz odd          0x6070809            0x6070809            D-form, D & 3 = 2: MEM(EA,4), EA = DATA+0x06         ok
live             0x1234               0x1234               li r9,0x1234 is the LAST word: every placed word ran ok
std value        0xc0c1c2c3c4c5c6c7   0xc0c1c2c3c4c5c6c7   XO 0 control: MEM(EA,8) <- RS, EA = 0x21010          ok
std RA after     0x21040              0x21040              XO 0, DS != 0: RA unchanged (r20)                    ok
std ds0 value    0xe0e1e2e3e4e5e6e7   0xe0e1e2e3e4e5e6e7   XO 0, DS = 0: MEM(RA,8) <- RS, RA = 0x210b0          ok
std ra0 value    0xe8e9eaebecedeeef   0xe8e9eaebecedeeef   XO 0, RA = 0: MEM(0x7100,8) <- RS, absolute          ok
stdu value       0x30c8c9cacbcccdce   0xc8c9cacbcccdcecf   XO 1: MEM(EA,8) <- RS, EA = 0x21030                  FAIL
stdu neigh       0x2f|0xcf393a3b      0x2f|0x38393a3b      XO 1: EA-1 and EA+8..EA+11 keep the seeded bytes     FAIL
stdu RA after    0x21060              0x21030              XO 1, DS != 0: RA <- EA (r21)                        FAIL
stdu ds0 value   0x50d0d1d2d3d4d5d6   0xd0d1d2d3d4d5d6d7   XO 1, DS = 0: MEM(RA,8) <- RS, RA = 0x21050          FAIL
stdu alias val   0x7000000000000210   0x0000000000021080   XO 1, RA = RS: MEM(EA,8) <- the old RA, EA = 0x21070 FAIL
stdu alias RA    0x21080              0x21070              XO 1, RA = RS, DS != 0: RA <- EA (r23)               FAIL
stw odd          0xdcdddedf           0xdcdddedf           D-form, D & 3 = 2: MEM(EA,4) <- RS low word, EA = 0x21090 ok
st live          0x1234               0x1234               li r9,0x1234 is the LAST word: every placed word ran ok
xo58_3 live      0x1234               0x1234               li r9 ran, the word before the stop word             ok
xo58_3 bad       nostop,rt=0x131415161718191a,ra=kept stop,rt=sent,ra=kept opcode 58 XO 3, RA != 0: CPU stops; RT, RA unchanged FAIL
xo62_2 live      0x1234               0x1234               li r9 ran, the word before the stop word             ok
xo62_2 bad       nostop,win=changed,ra=kept stop,win=kept,ra=kept opcode 62 XO 2, RA != 0: CPU stops; window, RA unchanged FAIL
xo62_3 live      0x1234               0x1234               li r9 ran, the word before the stop word             ok
xo62_3 bad       nostop,win=changed,ra=kept stop,win=kept,ra=kept opcode 62 XO 3, RA != 0: CPU stops; window, RA unchanged FAIL
ldu ra0 live     0x1234               0x1234               li r9 ran, the word before the stop word             ok
ldu ra0 bad      nostop,rt=0x7172737475767778,ra=kept stop,rt=sent,ra=kept opcode 58 XO 1, RA = 0: CPU stops; RT, RA unchanged  FAIL
stdu ra0 live    0x1234               0x1234               li r9 ran, the word before the stop word             ok
stdu ra0 bad     nostop,win=changed,ra=kept stop,win=kept,ra=kept opcode 62 XO 1, RA = 0: CPU stops; window, RA unchanged FAIL
unasm census     108/108              108/108              every placed word of the seven guest sessions        ok
word pins        e894ff90,e8b5ffa1,e8d6000a e894ff90,e8b5ffa1,e8d6000a the witness's ld, ldu, lwa words, read back by unassemble ok
neg apparatus    exit1/-0x1           exit1/-0x1           loads commands, bogus machine TYPE: exit 1, no registers ok

elapsed=0.2s binary=/tmp/gxt2/base/gxemul label=prefix_BASE
PPC_DSFORM_RESULT=22/39
PPC_DSFORM_CONTROL=OK
PPC_DSFORM_SYMPTOM=PRESENT 17/17
PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
PPC_DSFORM_PROBE_DONE
~~~~

### 4.5 Post-fix -- `s5_fix_build.out` (the work clone: patch, build, the detector and the frozen witness), VERBATIM

~~~~
=== 2026-10-24 08:30:55 work tree
cp -a base -> work
before patch: 87a766e0a8c1f8bbc41ebea8d9255d27  /tmp/gxt2/work/src/cpus/cpu_ppc_instr.c
=== 2026-10-24 08:30:55 patch
PATCHED: /tmp/gxt2/work/src/cpus/cpu_ppc_instr.c (+29 lines)
after patch:  2015e243f7af8e93fc2b5c283223bde5  /tmp/gxt2/work/src/cpus/cpu_ppc_instr.c
#571 tags in the file: 2
=== 2026-10-24 08:30:55 build (rm src/cpus/*.o; make)
MAKE_RC=0
warnings/errors in make_work.log: 0
=== 2026-10-24 08:32:06 freshness
-rwxr-xr-x 1 root root 6159736 2026-10-24 08:32:06.221855557 -0500 gxemul
-rwxrwxrwx 1 root root  152388 2026-10-24 08:30:55.522075618 -0500 src/cpus/cpu_ppc_instr.c
FRESH: gxemul -nt src/cpus/cpu_ppc_instr.c
904185b5223120c47129bce127a0d7dc  gxemul
2015e243f7af8e93fc2b5c283223bde5  src/cpus/cpu_ppc_instr.c
=== 2026-10-24 08:32:06 the frozen detector on the fixed binary -> fixed.out
0266228894811ba6c51cff82585753c9  /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/ppc_dsform_probe.py
DETECTOR_RC=0
elapsed=0.1s binary=/tmp/gxt2/work/gxemul label=fixed
PPC_DSFORM_RESULT=39/39
PPC_DSFORM_CONTROL=OK
PPC_DSFORM_SYMPTOM=ABSENT
PPC_DSFORM_RED=none
PPC_DSFORM_PROBE_DONE
=== 2026-10-24 08:32:06 the frozen witness on the fixed binary -> fixed_witness8.out
5e96b69df49ac82e10b3118780899549  /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py
WITNESS_RC=0
elapsed=0.0s binary=/tmp/gxt2/work/gxemul label=fixed8
PPC_DSFORM_RESULT=8/8
PPC_DSFORM_CONTROL=OK
PPC_DSFORM_SYMPTOM=ABSENT
PPC_DSFORM_RED=none
PPC_DSFORM_PROBE_DONE
=== 2026-10-24 08:32:06 files
-rwxrwxrwx 1 root root 19274 08:32:06 RAW_fixed8_main.txt
-rwxrwxrwx 1 root root   346 08:32:06 RAW_fixed8_neg.txt
-rwxrwxrwx 1 root root  4405 08:32:06 RAW_fixed_ldu_ra0.txt
-rwxrwxrwx 1 root root 24198 08:32:06 RAW_fixed_loads.txt
-rwxrwxrwx 1 root root   272 08:32:06 RAW_fixed_neg.txt
-rwxrwxrwx 1 root root  5530 08:32:06 RAW_fixed_stdu_ra0.txt
-rwxrwxrwx 1 root root 25511 08:32:06 RAW_fixed_stores.txt
-rwxrwxrwx 1 root root  6488 08:32:06 RAW_fixed_xo58_3.txt
-rwxrwxrwx 1 root root  5995 08:32:06 RAW_fixed_xo62_2.txt
-rwxrwxrwx 1 root root  5995 08:32:06 RAW_fixed_xo62_3.txt
-rwxrwxrwx 1 root root 13899 08:32:06 fixed.out
-rwxrwxrwx 1 root root  3795 08:32:06 fixed_witness8.out
FIX_BUILD_DONE
~~~~

### 4.6 `PREDICTIONS.txt` (written 08:32:01, before any leg), VERBATIM

~~~~
# PREDICTIONS.txt -- #571 (ppcdsformxo): per leg, the rows predicted RED, derived from the FROZEN detector source
# (regress/ppc_dsform_probe.py md5 0266228894811ba6c51cff82585753c9, N = 39, 17 SYMPTOM / 22 CONTROL rows) and
# PRETABLE.out's CHANNEL column, written 2026-10-24 08:3x BEFORE any leg runs (the mtime is the order proof).
# A leg's measured score lands in SCORES.txt beside these; every miss is named there.  The identity leg's number
# comes from THIS source, never from the witness's 4/8.

L1  frozen witness on the fixed binary                      8/8 green, SYMPTOM=ABSENT (clause (a), load half)
L2  the detector pre-fix (prefix_BASE.out, MEASURED 08:29)  22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17 (the 17 symptom rows); post-fix fixed.out 39/39
L3  both cases reinstated verbatim (HEAD's arm)             22/39: the 17 SYMPTOM rows red, every control green, CONTROL=OK -- identical to L2's pre-fix
L4b the opcode-58 case reinstated, 62 repaired              31/39: ldu value, ldu RA after, ldu ds0 value, lwa value, lwa ds0 value, lwa ra0 value, xo58_3 bad, ldu ra0 bad
L4c the opcode-62 case reinstated, 58 repaired              30/39: stdu value, stdu neigh, stdu RA after, stdu ds0 value, stdu alias val, stdu alias RA, xo62_2 bad, xo62_3 bad, stdu ra0 bad
L5  IDENTITY BODY for 58 and 62 (no-op handler, no stop)    17/39, CONTROL=FAIL: red = ld value, ld ds0 value, ld ra0 value, ldu value, ldu RA after, ldu ds0 value, lwa value, lwa ds0 value,
                                                            lwa ra0 value, std value, std ds0 value, std ra0 value, stdu value, stdu RA after, stdu ds0 value, stdu alias val, stdu alias RA,
                                                            xo58_3 bad, xo62_2 bad, xo62_3 bad, ldu ra0 bad, stdu ra0 bad (22); green = the RA-unchanged rows, stdu neigh, lwz/stw rows,
                                                            every live row, census, word pins, neg.  Record form: (c): measured at L5_identity.out
L5b the binary absent                                       no sentinel: the probe raises from subprocess (FileNotFoundError), as the witness did
L6a 58/1 update dropped (mask kept)                         37/39: ldu RA after, ldu ra0 bad (no refusal: the word executes at the absolute address)
L6b 62/1 update dropped (mask kept)                         36/39: stdu RA after, stdu alias RA, stdu ra0 bad
L7  raw imm in both cases, XO dispatch kept (= spec L4a)    27/39: ldu value, ldu RA after (EA is +1), ldu ds0 value, lwa value, lwa ds0 value, lwa ra0 value, stdu value, stdu neigh,
                                                            stdu RA after, stdu ds0 value, stdu alias val, stdu alias RA; XO-0 rows, D-form controls and all stop rows GREEN
L8a lwa branch reverted to the XO-0 flags (size 3, zero 1)  36/39: lwa value, lwa ds0 value, lwa ra0 value (8 bytes instead of the sign-extended word)
L8b lwa with zero left 1 (size 2)                            36/39: lwa value, lwa ds0 value, lwa ra0 value (zero-extended: high half 0)
L8c lwa size 3 with zero 0 (slot 11, the invalid handler)   EMULATOR EXIT in the loads session: its 14 rows red (controls among them -> CONTROL=FAIL), how=exit1 and
                                                            internal_error=1 on the loads session line, sentinel PRESENT; the other seven sessions unaffected -> 25/39
L9a XO 0 decoded as XO 1 (ld/std gain update)               35/39: ld RA after, std RA after, ld ra0 value, std ra0 value (RA = 0 + update = the existing refusal)
L9b EA + 1 on the XO-0 forms                                33/39: ld value, ld ds0 value, ld ra0 value, std value, std ds0 value, std ra0 value
L10 update = 1 for all five forms                           33/39: ld RA after, lwa RA after, std RA after, ld ra0 value, lwa ra0 value, std ra0 value
L11 the mask applied at the SHARED assignment (all 24 opcodes) 37/39: lwz odd, stw odd
L12a 62's reserved test narrowed to XO 2 (XO 3 stores)      38/39: xo62_3 bad
L12b 58's XO 3 not refused (executes as ld)                 38/39: xo58_3 bad
~~~~

### 4.7 `SCORES.txt`, VERBATIM (whole)

~~~~
# SCORES.txt -- #571 (ppcdsformxo) kill table, measured 2026-10-24 08:29-08:54 (console s6_all.out; drivers s6_leg.run-083332.sh +
# legs571.run-083332.py in the session scratchpad t2/build/, frozen copies; every leg a cp -a of /tmp/gxt2/work with a .MUTANT
# sentinel, built with rm src/cpus/*.o; make, measured by the FROZEN detector regress/ppc_dsform_probe.py md5
# 0266228894811ba6c51cff82585753c9 (N = 39), then DISCARDED -- /tmp/gxt2/legs is empty after TABLE_DONE).
# Columns: leg | predicted (PREDICTIONS.txt, written before any leg) | MEASURED | artifact | red rows | why the red is the reason under test.

L1  frozen witness post-fix        8/8 ABSENT            8/8 ABSENT            fixed_witness8.out   none                    clause (a) load half, same script as the witness
L2  detector pre-fix / post-fix    22/39 PRESENT 17/17   22/39 PRESENT 17/17   prefix_BASE.out      the 17 SYMPTOM rows     clause (a) both halves: every red names the misdirected address or the missing stop
                                   39/39 ABSENT          39/39 ABSENT          fixed.out            none
L3  both cases reinstated (HEAD)   22/39 CONTROL=OK      22/39 CONTROL=OK      L3_armHEAD.out       the 17 SYMPTOM rows     clause (b), full: identical row set to the pre-fix run
L4b 58 case reinstated             31/39                 31/39                 L4b_case58HEAD.out   ldu value, ldu RA after, ldu ds0 value, lwa value, lwa ds0 value, lwa ra0 value, xo58_3 bad, ldu ra0 bad   clause (b) per site: only opcode-58 rows red
L4c 62 case reinstated             30/39                 30/39                 L4c_case62HEAD.out   stdu value, stdu neigh, stdu RA after, stdu ds0 value, stdu alias val, stdu alias RA, xo62_2 bad, xo62_3 bad, stdu ra0 bad   clause (b) per site: only opcode-62 rows red
L5  IDENTITY BODY 58/62            17/39 CONTROL=FAIL    17/39 CONTROL=FAIL    L5_identity.out      22 rows: every 58/62 transfer and stop row; the RA-unchanged, lwz/stw, live, census, word-pin and neg rows green   clause (c): measured at L5_identity.out -- the no-op handler transfers nothing and stops nothing
L5b binary absent                  no sentinel           no sentinel (FileNotFoundError, rc 1)   L5b_absent.out   --                  the probe raises before any row; the gate's sentinel pin reds
L6a 58/1 update dropped            37/39                 37/39                 L6a_noupd58.out      ldu RA after, ldu ra0 bad   (d) null: RA not written; the RA = 0 word executes instead of stopping
L6b 62/1 update dropped            36/39                 36/39                 L6b_noupd62.out      stdu RA after, stdu alias RA, stdu ra0 bad   (d) null, store side
L7  raw imm, XO dispatch kept      27/39                 27/39                 L7_rawimm.out        the 12 address/RA rows of ldu, lwa, stdu (XO != 0 forms); XO-0 rows, D-form controls and every stop row green   (d) null of the mask: EA off by XO
L8a lwa -> XO-0 flags (8 bytes)    36/39                 36/39                 L8a_lwaxo0flags.out  lwa value, lwa ds0 value, lwa ra0 value   (d) null of the width: a doubleword where the sign-extended word was owed
L8b lwa zero left 1                36/39                 36/39                 L8b_lwazero1.out     lwa value, lwa ds0 value, lwa ra0 value   (d) null of the extension: high half 0
L8c lwa size 3 with zero 0         25/39 CONTROL=FAIL, emulator exit on the loads session, sentinel PRESENT   25/39 CONTROL=FAIL, loads session how=exit1 internal_error=1, sentinel PRESENT   L8c_lwasize3zero0.out   the 14 loads-session rows   the invalid handler (slot 11) ends the emulator; the probe records the exit and prints its sentinel -- scored as emulator termination, not as a wrong-width transfer
L9a XO 0 decoded as XO 1           35/39                 33/39 CONTROL=FAIL    L9a_xo0asxo1.out     ld RA after, ld ra0 value, live, std RA after, std ra0 value, st live   growth: RA written on the XO-0 forms; the RA = 0 words now REFUSE, which stops the loads and stores sessions before their liveness li -- *** PREDICTION MISS by 2 rows: the prediction named the refusal and did not carry it to the session's liveness row.  Detector redder than predicted; every red is the reason under test. ***
L9b EA + 1 on the XO-0 forms       33/39                 33/39 CONTROL=FAIL    L9b_xo0plus1.out     ld value, ld ds0 value, ld ra0 value, std value, std ds0 value, std ra0 value   growth: the XO-0 address off by one; RA rows green as predicted
L10 update = 1 for all five forms  33/39                 31/39 CONTROL=FAIL    L10_updall.out       ld RA after, ld ra0 value, lwa RA after, lwa ra0 value, live, std RA after, std ra0 value, st live   growth: RA written everywhere; the RA = 0 words refuse and stop both sessions before their li -- *** PREDICTION MISS by the same 2 liveness rows as L9a, same mechanism. ***
L11 mask on the SHARED assignment  37/39                 37/39 CONTROL=FAIL    L11_sharedmask.out   lwz odd, stw odd         the D-form scope controls: a mask reaching the other 22 opcodes reads +4 for +6
L12a 62 reserved test -> XO 2 only 38/39                 38/39                 L12a_xo623open.out   xo62_3 bad              XO 3 stores instead of stopping
L12b 58's XO 3 not refused         38/39                 38/39                 L12b_xo583open.out   xo58_3 bad              XO 3 loads instead of stopping

SUMMARY: 16 variant legs + L5b, all RED; 14 of 16 at the written prediction exactly; 2 (L9a, L10) redder than predicted by the two
session-liveness rows, one mechanism (an RA = 0 XO-0 word turned into a refusal stops its session), recorded as prediction misses --
no detector miss, no leg green, no leg red for a reason other than the one under test.  No leg left a tree mutated (each clone
discarded; /tmp/gxt2/legs empty at TABLE_DONE).  Clause (c) record: (c): measured at L5_identity.out.  Not built (clause (e),
disclosed in the probe's contract): RA = RT checks, a 32-bit width test, translation on, the indexed forms, the disassembler, the
DS = 0 x RA = 0 joints.  The ask-again (one, after this clean table) goes to pass 2's panel.
~~~~

### 4.8 The measured summary lines of every run, extracted from each `.out` (`PPC_DSFORM_RESULT=` / `CONTROL=` / `SYMPTOM=` / `RED=`), VERBATIM

~~~~
prefix_BASE.out          PPC_DSFORM_RESULT=22/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=PRESENT 17/17
                         PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
fixed.out                PPC_DSFORM_RESULT=39/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=ABSENT
                         PPC_DSFORM_RED=none
fixed_witness8.out       PPC_DSFORM_RESULT=8/8  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=ABSENT
                         PPC_DSFORM_RED=none
L3_armHEAD.out           PPC_DSFORM_RESULT=22/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=PRESENT 17/17
                         PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
L4b_case58HEAD.out       PPC_DSFORM_RESULT=31/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,xo58_3 bad,ldu ra0 bad
L4c_case62HEAD.out       PPC_DSFORM_RESULT=30/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo62_2 bad,xo62_3 bad,stdu ra0 bad
L5_identity.out          PPC_DSFORM_RESULT=17/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ld value,ld ds0 value,ld ra0 value,ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,std value,std ds0 value,std ra0 value,stdu value,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
L6a_noupd58.out          PPC_DSFORM_RESULT=37/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ldu RA after,ldu ra0 bad
L6b_noupd62.out          PPC_DSFORM_RESULT=36/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=stdu RA after,stdu alias RA,stdu ra0 bad
L7_rawimm.out            PPC_DSFORM_RESULT=27/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA
L8a_lwaxo0flags.out      PPC_DSFORM_RESULT=36/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=lwa value,lwa ds0 value,lwa ra0 value
L8b_lwazero1.out         PPC_DSFORM_RESULT=36/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=lwa value,lwa ds0 value,lwa ra0 value
L8c_lwasize3zero0.out    PPC_DSFORM_RESULT=25/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ld value,ld RA after,ld ds0 value,ld ra0 value,ldu value,ldu RA after,ldu ds0 value,lwa value,lwa RA after,lwa ds0 value,lwa ra0 value,lwz value,lwz odd,live
L9a_xo0asxo1.out         PPC_DSFORM_RESULT=33/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=ABSENT
                         PPC_DSFORM_RED=ld RA after,ld ra0 value,live,std RA after,std ra0 value,st live
L9b_xo0plus1.out         PPC_DSFORM_RESULT=33/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=ABSENT
                         PPC_DSFORM_RED=ld value,ld ds0 value,ld ra0 value,std value,std ds0 value,std ra0 value
L10_updall.out           PPC_DSFORM_RESULT=31/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=ld RA after,ld ra0 value,lwa RA after,lwa ra0 value,live,std RA after,std ra0 value,st live
L11_sharedmask.out       PPC_DSFORM_RESULT=37/39  PPC_DSFORM_CONTROL=FAIL  PPC_DSFORM_SYMPTOM=ABSENT
                         PPC_DSFORM_RED=lwz odd,stw odd
L12a_xo623open.out       PPC_DSFORM_RESULT=38/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=xo62_3 bad
L12b_xo583open.out       PPC_DSFORM_RESULT=38/39  PPC_DSFORM_CONTROL=OK  PPC_DSFORM_SYMPTOM=MIXED
                         PPC_DSFORM_RED=xo58_3 bad
L5b_absent.out           (no PPC_DSFORM_ lines; last line: FileNotFoundError: [Errno 2] No such file or directory: '/tmp/gxt2/NO_SUCH_BINARY/gxemul')
~~~~

The per-session observations of five runs -- where each session stopped (`pc=`), how it ended (`how=`), and what it printed
(`unimplemented=`, `todo_ra0=`, `internal_error=`) -- VERBATIM (`OBS session` lines):

~~~~
fixed.out: OBS session loads    how=exit0 words=27 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x1006c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_fixed_loads.txt
fixed.out: OBS session stores   how=exit0 words=50 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x100c8 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_fixed_stores.txt
fixed.out: OBS session xo58_3   how=exit0 words=4 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x1000c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_fixed_xo58_3.txt
fixed.out: OBS session xo62_2   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_fixed_xo62_2.txt
fixed.out: OBS session xo62_3   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_fixed_xo62_3.txt
fixed.out: OBS session ldu ra0  how=exit0 words=2 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10004 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_fixed_ldu_ra0.txt
fixed.out: OBS session stdu ra0 how=exit0 words=7 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10018 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_fixed_stdu_ra0.txt
fixed.out: OBS session neg      how=exit1 transcript=RAW_fixed_neg.txt
prefix_BASE.out: OBS session loads    how=exit0 words=27 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x1006c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_prefix_BASE_loads.txt
prefix_BASE.out: OBS session stores   how=exit0 words=50 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x100c8 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_prefix_BASE_stores.txt
prefix_BASE.out: OBS session xo58_3   how=exit0 words=4 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x10010 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_prefix_BASE_xo58_3.txt
prefix_BASE.out: OBS session xo62_2   how=exit0 words=9 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x10024 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_prefix_BASE_xo62_2.txt
prefix_BASE.out: OBS session xo62_3   how=exit0 words=9 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x10024 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_prefix_BASE_xo62_3.txt
prefix_BASE.out: OBS session ldu ra0  how=exit0 words=2 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x10008 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_prefix_BASE_ldu_ra0.txt
prefix_BASE.out: OBS session stdu ra0 how=exit0 words=7 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x1001c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_prefix_BASE_stdu_ra0.txt
prefix_BASE.out: OBS session neg      how=exit1 transcript=RAW_prefix_BASE_neg.txt
L8c_lwasize3zero0.out: OBS session loads    how=exit1 words=27 unimplemented=0 todo_ra0=0 internal_error=1 pc=none msr=none r30=-0x1 seeded_readback=same transcript=RAW_L8c_lwasize3zero0_loads.txt
L8c_lwasize3zero0.out: OBS session stores   how=exit0 words=50 unimplemented=0 todo_ra0=0 internal_error=0 pc=0x100c8 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L8c_lwasize3zero0_stores.txt
L8c_lwasize3zero0.out: OBS session xo58_3   how=exit0 words=4 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x1000c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L8c_lwasize3zero0_xo58_3.txt
L8c_lwasize3zero0.out: OBS session xo62_2   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L8c_lwasize3zero0_xo62_2.txt
L8c_lwasize3zero0.out: OBS session xo62_3   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L8c_lwasize3zero0_xo62_3.txt
L8c_lwasize3zero0.out: OBS session ldu ra0  how=exit0 words=2 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10004 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L8c_lwasize3zero0_ldu_ra0.txt
L8c_lwasize3zero0.out: OBS session stdu ra0 how=exit0 words=7 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10018 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L8c_lwasize3zero0_stdu_ra0.txt
L8c_lwasize3zero0.out: OBS session neg      how=exit1 transcript=RAW_L8c_lwasize3zero0_neg.txt
L9a_xo0asxo1.out: OBS session loads    how=exit0 words=27 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10064 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_loads.txt
L9a_xo0asxo1.out: OBS session stores   how=exit0 words=50 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x100c0 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_stores.txt
L9a_xo0asxo1.out: OBS session xo58_3   how=exit0 words=4 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x1000c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L9a_xo0asxo1_xo58_3.txt
L9a_xo0asxo1.out: OBS session xo62_2   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_xo62_2.txt
L9a_xo0asxo1.out: OBS session xo62_3   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_xo62_3.txt
L9a_xo0asxo1.out: OBS session ldu ra0  how=exit0 words=2 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10004 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L9a_xo0asxo1_ldu_ra0.txt
L9a_xo0asxo1.out: OBS session stdu ra0 how=exit0 words=7 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10018 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_stdu_ra0.txt
L9a_xo0asxo1.out: OBS session neg      how=exit1 transcript=RAW_L9a_xo0asxo1_neg.txt
L10_updall.out: OBS session loads    how=exit0 words=27 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10060 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_loads.txt
L10_updall.out: OBS session stores   how=exit0 words=50 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x100c0 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_stores.txt
L10_updall.out: OBS session xo58_3   how=exit0 words=4 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x1000c msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L10_updall_xo58_3.txt
L10_updall.out: OBS session xo62_2   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_xo62_2.txt
L10_updall.out: OBS session xo62_3   how=exit0 words=9 unimplemented=1 todo_ra0=0 internal_error=0 pc=0x10020 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_xo62_3.txt
L10_updall.out: OBS session ldu ra0  how=exit0 words=2 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10004 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=not dumped transcript=RAW_L10_updall_ldu_ra0.txt
L10_updall.out: OBS session stdu ra0 how=exit0 words=7 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10018 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_stdu_ra0.txt
L10_updall.out: OBS session neg      how=exit1 transcript=RAW_L10_updall_neg.txt
~~~~

The clause-(b) leg L3 (both case bodies reinstated verbatim) rebuilt the BASE binary bit for bit (leg binary md5 `3cd0501c...` = the BASE binary's; leg source md5 `87a766e0...` = the HEAD blob) -- `s6_all.out` lines 1-25, VERBATIM:

~~~~
=== 2026-10-24 08:34:28 S6 table: frozen driver copies s6_leg.run-083428.sh / legs571.run-083428.py
5371d36252290fa0133b034aba40adb3  /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/t2/build/legs571.run-083428.py
0266228894811ba6c51cff82585753c9  /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/ppc_dsform_probe.py
=== 2026-10-24 08:34:28 leg 3 (armHEAD): clone work -> /tmp/gxt2/legs/3
=== 2026-10-24 08:34:28 variant
VARIANT 3 applied to /tmp/gxt2/legs/3/src/cpus/cpu_ppc_instr.c
diff lines: 49
=== 2026-10-24 08:34:28 build
MAKE_RC=0  warnings/errors: 0
FRESH
3cd0501cf7c854e0662797ccee1fce64  gxemul
87a766e0a8c1f8bbc41ebea8d9255d27  src/cpus/cpu_ppc_instr.c
=== 2026-10-24 08:35:42 detector -> L3_armHEAD.out
0266228894811ba6c51cff82585753c9  /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/ppc_dsform_probe.py
DETECTOR_RC=1
OBS session neg      how=exit1 transcript=RAW_L3_armHEAD_neg.txt
PPC_DSFORM_RESULT=22/39
PPC_DSFORM_CONTROL=OK
PPC_DSFORM_SYMPTOM=PRESENT 17/17
PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
PPC_DSFORM_PROBE_DONE
=== 2026-10-24 08:35:42 discard the leg tree
leg tree removed (sentinel went with it)
LEG_DONE 3
--------------------------------------------------------------------------------
~~~~

### 4.9 The two-part clearance -- `CLEARANCE.out`, VERBATIM, and the drafter's re-check at drafting time

~~~~
# CLEARANCE.out -- #571, written 2026-10-24 08:56:08 -0500: propagation of src/cpus/cpu_ppc_instr.c and the two-part clearance per tree
SEC: 2015e243f7af8e93fc2b5c283223bde5   est/: 2015e243f7af8e93fc2b5c283223bde5  (est/: source tree, part 2 N/A)
=== 2026-10-24 08:56:08 /mnt/c/DocumentNoSnc/cc/GXEMUL/build
copied
MAKE_RC=0  warnings/errors: 0
PART 1 cmp vs SEC: CLEAN
PART 2 [ gxemul -nt src/cpus/cpu_ppc_instr.c ]: FRESH
    2026-10-24 08:57:31.037198600 /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
    2026-10-24 08:56:08.769808500 /mnt/c/DocumentNoSnc/cc/GXEMUL/build/src/cpus/cpu_ppc_instr.c
    binary md5 a142d92ae8508024f3a92455e6be86b3  /mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
=== 2026-10-24 08:57:31 /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan
copied
MAKE_RC=0  warnings/errors: 0
PART 1 cmp vs SEC: CLEAN
PART 2 [ gxemul -nt src/cpus/cpu_ppc_instr.c ]: FRESH
    2026-10-24 09:02:21.224648000 /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan/gxemul
    2026-10-24 08:57:31.217069800 /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan/src/cpus/cpu_ppc_instr.c
    binary md5 79d7544228f488cdc06263ceae6cd942  /mnt/c/DocumentNoSnc/cc/GXEMUL/build-asan/gxemul
=== 2026-10-24 09:02:21 /tmp/gxsec-build
copied
MAKE_RC=0  warnings/errors: 0
PART 1 cmp vs SEC: CLEAN
PART 2 [ gxemul -nt src/cpus/cpu_ppc_instr.c ]: FRESH
    2026-10-24 09:03:34.956928158 /tmp/gxsec-build/gxemul
    2026-10-24 09:02:21.965664501 /tmp/gxsec-build/src/cpus/cpu_ppc_instr.c
    binary md5 14ede3bd71dba2613509227b08661c73  /tmp/gxsec-build/gxemul
=== 2026-10-24 09:03:34 the peer's five dirty files in build/ (left exactly as they are)
   src/cpus/cpu_alpha_palcode.c: == SEC working tree
   src/devices/dev_lca.c: == SEC working tree
   src/devices/dev_pcc2.c: == SEC working tree
   src/devices/dev_sh4.c: == SEC working tree
   src/include/thirdparty/mvme_pcctworeg.h: == SEC working tree
CLEARANCE_DONE
~~~~

Re-checked read-only at drafting: `src/cpus/cpu_ppc_instr.c` md5 `2015e243f7af8e93fc2b5c283223bde5` in GXEMUL-SEC, est/,
build/, build-asan/ and WSL /tmp/gxsec-build; `[ gxemul -nt src/cpus/cpu_ppc_instr.c ]` FRESH in build/ (`a142d92a`),
build-asan/ (`79d75442`) and /tmp/gxsec-build (`14ede3bd`); no `.MUTANT` sentinel in any of the three; est/ is a source
tree (part 2 N/A).

### 4.10 Gate 13 alone -- `gate13_20261024.out`: its header, the `#571` block's 53 checks, and the summary, VERBATIM

~~~~
  === 2026-10-24 09:03:54 gate 13 via run.sh 13 (binary build/gxemul md5 a142d92ae8508024f3a92455e6be86b3)
  ############################################################
  ## GATE: gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl
  ############################################################
  ...
    ok   ppc_dsform probe completed                           yes
    ok   ppc_dsform sentinel is the last line                 PPC_DSFORM_PROBE_DONE
    ok   ppc_dsform RESULT= lines                             1
    ok   ppc_dsform CONTROL= lines                            1
    ok   ppc_dsform SYMPTOM= lines                            1
    ok   ppc_dsform RED= lines                                1
    ok   ppc_dsform RESULT=39/39                              1
    ok   ppc_dsform CONTROL=OK                                1
    ok   ppc_dsform SYMPTOM=ABSENT                            1
    ok   ppc_dsform RED=none                                  1
    ok   ppc_dsform row: ld value                             1
    ok   ppc_dsform row: ld RA after                          1
    ok   ppc_dsform row: ld ds0 value                         1
    ok   ppc_dsform row: ld ra0 value                         1
    ok   ppc_dsform row: ldu value                            1
    ok   ppc_dsform row: ldu RA after                         1
    ok   ppc_dsform row: ldu ds0 value                        1
    ok   ppc_dsform row: lwa value                            1
    ok   ppc_dsform row: lwa RA after                         1
    ok   ppc_dsform row: lwa ds0 value                        1
    ok   ppc_dsform row: lwa ra0 value                        1
    ok   ppc_dsform row: lwz value                            1
    ok   ppc_dsform row: lwz odd                              1
    ok   ppc_dsform row: live                                 1
    ok   ppc_dsform row: std value                            1
    ok   ppc_dsform row: std RA after                         1
    ok   ppc_dsform row: std ds0 value                        1
    ok   ppc_dsform row: std ra0 value                        1
    ok   ppc_dsform row: stdu value                           1
    ok   ppc_dsform row: stdu neigh                           1
    ok   ppc_dsform row: stdu RA after                        1
    ok   ppc_dsform row: stdu ds0 value                       1
    ok   ppc_dsform row: stdu alias val                       1
    ok   ppc_dsform row: stdu alias RA                        1
    ok   ppc_dsform row: stw odd                              1
    ok   ppc_dsform row: st live                              1
    ok   ppc_dsform row: xo58_3 live                          1
    ok   ppc_dsform row: xo58_3 bad                           1
    ok   ppc_dsform row: xo62_2 live                          1
    ok   ppc_dsform row: xo62_2 bad                           1
    ok   ppc_dsform row: xo62_3 live                          1
    ok   ppc_dsform row: xo62_3 bad                           1
    ok   ppc_dsform row: ldu ra0 live                         1
    ok   ppc_dsform row: ldu ra0 bad                          1
    ok   ppc_dsform row: stdu ra0 live                        1
    ok   ppc_dsform row: stdu ra0 bad                         1
    ok   ppc_dsform row: unasm census                         1
    ok   ppc_dsform row: word pins                            1
    ok   ppc_dsform row: neg apparatus                        1
    ok   ppc_dsform census, 108 placed words                  1
    ok   ppc_dsform rows run                                  39
    ok   ppc_dsform rows green                                39
    ok   ppc_dsform rows red                                  0
  ...
  gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl: PASS (193 checks)

  ############################################################
  ## SUMMARY
  ############################################################
    PASS 13. gate_ppc

    passed 1   failed 0   skipped 0
    GATE_COVERAGE=1/16 (SUBSET: 13)

  REGRESS_PASS
  RUN_RC=0
  === 2026-10-24 09:05:23 done
~~~~

The gate's detector log is preserved as `gate13_ppc_dsform.log` (ends with the sentinel); its 39 row lines equal
`fixed.out`'s (name, got, want -- compared at drafting).

---

## 5. C0 -- has this round already shipped?  NO.  (`C0_OUTPUT.txt`, run at drafting, VERBATIM)

~~~~
  # C0 -- has this round already shipped?  Run 2026-10-24 09:25:39 -0500 from GXEMUL-SEC/ against HEAD (pass-2 brief).
  # Read-only: git log / git show / git ls-files / grep / ls / md5sum / cmp only (no status, no diff, no add).

  $ git log -1 --format='%H %ad %s' --date=iso HEAD
  add098b9d94221c623e23fdd13fa26ec2793ab63 2026-10-24 05:24:44 -0500 records: `m88kbuserrregs` names its landing commit c8fcb5ff, and c8fcb5ff's committed-tree proofs and pass-2 receipt

  ## 1. git log -1 -- <each file the round touches>
  $ git log -1 --format='%h %ad %s' --date=short -- src/cpus/cpu_ppc_instr.c
  7e39a49e 2026-09-12 #527 (ppcrlwimiwidth, ppcrldimimask): rlwimi rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; rldimi's rotate loop consumed its shift count
  $ git log -1 --format='%h %ad %s' --date=short -- regress/ppc_dsform_probe.py
  (no commit touches this path -- it does not exist at HEAD)
  $ git log -1 --format='%h %ad %s' --date=short -- regress/gate_ppc.sh
  8d038908 2026-10-18 #565 (wiringcliff): ppc_rldicl_probe.py wired into gate 13 before its exemption refuses every commit -- 30 checks score all 24 rows; floor (c) measured with the identity body; the 
  $ git log -1 --format='%h %ad %s' --date=short -- tools/pipeline/check_probe_wiring.py
  c8fcb5ff 2026-10-24 #570 m88kbuserrregs: a refused m88k device access raised the access exception without recording the bus error in the CMMU -- PFSR/PFAR now written on the faulting side's CMMU, LUNA
  $ git log -1 --format='%h %ad %s' --date=short -- tools/precommit_check.sh
  c8fcb5ff 2026-10-24 #570 m88kbuserrregs: a refused m88k device access raised the access exception without recording the bus error in the CMMU -- PFSR/PFAR now written on the faulting side's CMMU, LUNA
  $ git log -1 --format='%h %ad %s' --date=short -- CHANGELOG.md
  add098b9 2026-10-24 records: `m88kbuserrregs` names its landing commit c8fcb5ff, and c8fcb5ff's committed-tree proofs and pass-2 receipt
  $ git log -1 --format='%h %ad %s' --date=short -- OUTSTANDING_BUGS.md
  c8fcb5ff 2026-10-24 #570 m88kbuserrregs: a refused m88k device access raised the access exception without recording the bus error in the CMMU -- PFSR/PFAR now written on the faulting side's CMMU, LUNA
  $ git log -1 --format='%h %ad %s' --date=short -- tools/pipeline/ledger.json
  add098b9 2026-10-24 records: `m88kbuserrregs` names its landing commit c8fcb5ff, and c8fcb5ff's committed-tree proofs and pass-2 receipt
  $ git log -1 --format='%h %ad %s' --date=short -- regress/pass2_ledger.tsv
  add098b9 2026-10-24 records: `m88kbuserrregs` names its landing commit c8fcb5ff, and c8fcb5ff's committed-tree proofs and pass-2 receipt
  $ git log --format='%h %ad %s' --date=short c8fcb5ff..HEAD -- src
  (no commit between c8fcb5ff -- the tree the witness and the BASE binary were built from -- and HEAD touches src/)
  $ git log --format='%h %s' c8fcb5ff..HEAD
  add098b9 records: `m88kbuserrregs` names its landing commit c8fcb5ff, and c8fcb5ff's committed-tree proofs and pass-2 receipt

  ## 2. grep <row id> and <round tag> in the HEAD blobs, and in every commit message
  $ git show HEAD:CHANGELOG.md | grep -n -e ppcdsformxo -e '#571'
  (grep rc=1)
  $ git show HEAD:regress/pass2_ledger.tsv | grep -n -e ppcdsformxo -e '#571'
  (grep rc=1)
  $ git show HEAD:OUTSTANDING_BUGS.md | grep -n ppcdsformxo | cut -c1-200
  33:> 4. `ppcdsformxo` (HIGH, new) -- DS-form XO bits: ldu/lwa/stdu run as ld/std at EA+1/+2.  T2; design owed.
  25264:* **`ppcdsformxo` (HIGH, open)** -- new.  cpu_ppc_instr.c:X(to_be_translated) D/DS-form arm -- primary opcodes 58/62
  $ git log --oneline --all -i --grep=ppcdsformxo
  (no commit message names the row)
  $ git log --oneline --all --grep='#571'
  (no commit message names #571)

  ## 3. ls <the directories a NEW TOOL of this round lives in>, and what is tracked there
  $ ls regress/ | grep -i -E 'ppc|dsform'
  gate_ppc.sh
  gate_ppc_halt.sh
  ppc_dsform_probe.py
  ppc_halt_probe.py
  ppc_rldicl_probe.py
  ppc_rldimi_probe.py
  ppc_rlwimi_probe.py
  ppc_rounding_probe.py
  $ git ls-files regress/ppc_dsform_probe.py regress/artifacts/ppcdsformxo
  (nothing tracked -- the detector and every ppcdsformxo artifact are untracked)
  $ ls regress/artifacts/ppcdsformxo/
  pass1_20261024
  pass2_20261024
  table1_20261024
  witness_20261024

  ## 4. the ledger at HEAD (git show HEAD:tools/pipeline/ledger.json, parsed): the row and the four filing ids
  rows at HEAD: 1079
  ppcdsformxo: state=open sev=HIGH opened=2026-10-22 witness=none commits='' stages=NoneType
  id ppcdisasmxo     rows with this id at HEAD: 0
  id ppcdisasmfpupd  rows with this id at HEAD: 0
  id ppcldxabsent    rows with this id at HEAD: 0
  id ppc64on32gate   rows with this id at HEAD: 0

  ## 5. working-tree files that differ from HEAD (git ls-files -m, each confirmed by cmp against git show HEAD:<path>)
    DIFFERS FROM HEAD     regress/artifacts/recordfix_20261002/chk_hrec.py.txt
    DIFFERS FROM HEAD     regress/diff_wdc_identify.c
    DIFFERS FROM HEAD     regress/gate_offline.sh
    DIFFERS FROM HEAD     regress/gate_ppc.sh
    DIFFERS FROM HEAD     regress/gate_sh_rounding.sh
    DIFFERS FROM HEAD     regress/gdrom_default_probe.py
    DIFFERS FROM HEAD     regress/sh4_chcr_probe.py
    DIFFERS FROM HEAD     regress/wdc_addtoinbuf_probe.py
    DIFFERS FROM HEAD     src/cpus/cpu_alpha_palcode.c
    DIFFERS FROM HEAD     src/cpus/cpu_ppc_instr.c
    DIFFERS FROM HEAD     src/devices/dev_lca.c
    DIFFERS FROM HEAD     src/devices/dev_pcc2.c
    DIFFERS FROM HEAD     src/devices/dev_sh4.c
    DIFFERS FROM HEAD     src/include/thirdparty/mvme_pcctworeg.h
    DIFFERS FROM HEAD     tools/BRIEF_TEMPLATE.md
    DIFFERS FROM HEAD     tools/CLAUDE.md
    DIFFERS FROM HEAD     tools/PIPELINE.md
    DIFFERS FROM HEAD     tools/adjudicate.sh
    DIFFERS FROM HEAD     tools/panel.sh
    DIFFERS FROM HEAD     tools/pipeline/check_probe_wiring.py
    DIFFERS FROM HEAD     tools/pipeline/ledger.json
    DIFFERS FROM HEAD     tools/pipeline/matrix.html
    DIFFERS FROM HEAD     tools/precommit_check.sh
    -- untracked, this round's:
    UNTRACKED             regress/ppc_dsform_probe.py
    UNTRACKED             regress/artifacts/ppcdsformxo
    -- this round's own files, md5 now:
    2015e243f7af8e93fc2b5c283223bde5 *src/cpus/cpu_ppc_instr.c
    0266228894811ba6c51cff82585753c9 *regress/ppc_dsform_probe.py
    d361db091a3d545b280acab979c5c241 *regress/gate_ppc.sh
    5e944fd659e697e75e842076dd4621e0 *tools/pipeline/check_probe_wiring.py
    cce34f8c80a933a170f912419b632d98 *tools/precommit_check.sh

  ## 6. the frozen witness and its receipts, re-verified
    RAW_headbin_main.txt: OK
    RAW_headbin_neg.txt: OK
    WITNESS_REPORT.md: OK
    WITNESS_headbin.out: OK
    ppc_dsform_dummy.bin: OK
    ppc_dsform_probe.py: OK
    receipts/baseline_build_vs_head.txt: OK
    receipts/baseline_scratch_vs_head.txt: OK
    receipts/build_base.out: OK
    receipts/cpu_ppc_instr.HEAD.c.md5: OK
    receipts/run_dsform_witness.out: OK
    receipts/run_dsform_witness.sh: OK

  C0_DONE
~~~~

---

## 6. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by pass 1 -- `pass1_20261024/PASS1_RULINGS.md`: checks M1-M5, rulings A1-A9, B1-B13, C1-C9, disputes D1-D8, and the
adjudications F1 (GPT-6 Astra, AMEND) and F2 (Grok 4.7, AMEND), handed to the builder as `BUILD_SPEC.md` sections 10 and
10b.  Code facts were RE-READ for this brief (working-tree line numbers; for every file but the round's five they equal
HEAD's).  Pass 2 asks whether the SHIPPED material carries these out; re-open one only if you find it false, and say so.

**The code (re-read here):**
* **S1** -- `PPC_HI6_LD` 0x3a = 58, `PPC_HI6_STD` 0x3e = 62 (`src/include/opcodes_ppc.h`).
* **S2** -- `X(to_be_translated)`'s D/DS-form arm is ONE `case` list of 24 primary opcodes (22 D-form + LD + STD;
  `cpu_ppc_instr.c` :4269-4292).  `imm = (int16_t)iword;` once for all 24 (:4295); an inner `switch (main_opcode)` sets
  `load`/`size`/`zero`/`update`/`fp`; the common part after it (:4357-4381) picks the handler from the generated table, runs
  the `ra == 0 && update` guard and sets `ic->arg[0..2]` (`arg[2] = imm`).  The arm leaves by `break` or `goto bad`.
* **S3 (Book I v2.01)** -- DS form: OPCD 0:5, RT/RS 6:10, RA 11:15, DS 16:29, XO 30:31; EA = (RA|0) + EXTS(DS || 0b00).
  58: XO 0 `ld` (8 bytes), XO 1 `ldu` (RA <- EA), XO 2 `lwa` (EXTS of a word); 62: XO 0 `std`, XO 1 `stdu` (RA <- EA).
  58/XO 3 and 62/XO 2-3 are empty opcode-map cells (illegal).  Invalid forms: `ldu` with RA = 0 or RA = RT, `stdu` with
  RA = 0 (RA = RS is valid).
* **S6 / M1** -- `bad:` (`cpu_dyntrans.c` :1983-2014, the tail #included at the end of `X(to_be_translated)`) clears the
  translation; in read-ahead it returns; otherwise it prints `UNIMPLEMENTED instruction at 0x...` (VERBOSITY_ERROR,
  unconditional, also under `step`), disassembles only when NOT stepping or tracing, and sets `cpu->running = 0`.
  Nothing is delivered to the guest and no process ends: the CPU stops.
* **S7** -- handler = `ppc_loadstore[size + 4*zero + 8*load + (imm==0? 16 : 0) + 32*update]` (`ppc32_loadstore` in the MODE32
  build).  Slots 11/27/43/59 (load, zero 0, size 3) are `ppc_instr_invalid`: `fatal("PPC: invalid(): INTERNAL
  ERROR\n"); exit(1);` (:241-245).
* **S8** -- the generic handler: EA = `reg(arg[1]) + (int32_t)arg[2]`; a load calls `memory_rw` then writes RT; a store
  copies RS then calls `memory_rw`; an update form then writes RA <- EA, only if the access succeeded.  On a 64-bit CPU every
  table handler delegates to it.
* **S9** -- `tmp_ppc_tail.c` #includes `cpu_ppc_instr.c` twice (:63; :118 under the MODE32 definitions; `cpu_ppc.c` :1842
  says so): an edit to the arm changes both decoders.
* **M2** -- the MODE32 table has real doubleword handlers (slots 7 std, 10 lwa, 11 invalid, 15 ld, 39 stdu, 47 ldu;
  `tmp_ppc_loadstore.c` :1923+): a 32-bit CPU executing 58/62 ends no process, before or after the fix.
* **M5** -- `arg[2]` matters for every XO != 0 word; the `imm == 0` table half is unobservable on PPC970 (both halves
  delegate to the generic handler).

**The repair (rulings as amended):**
* **A1** -- decode-only, five forms onto existing slots: `ld` 15/31, `ldu` 47/63, `lwa` 10/26 (`size` 2, `zero` 0), `std`
  7/23, `stdu` 39/55; none on 11/27/43/59; no handler edit.  `(int16_t)(iword & ~3)` == EXTS(DS || 0b00) in all twenty
  (DS, XO) cells walked.
* **A2 (+F2)** -- ONE masked `imm` must reach BOTH consumers (the table index and `arg[2]`); re-assigning it inside the two
  case bodies is sufficient, not the only shape; the record states the invariant, not the syntax.
* **A3 (+F1, F2)** -- reserved XO (58/3, 62/2, 62/3): bare `default: goto bad;`, no own message, no latch; the common tail's
  `UNIMPLEMENTED instruction` line is the diagnostic.  The comment must NOT say pre-`goto bad` `fatal()` sites mark only
  unimplemented features (the RA = 0 guard diagnoses an INVALID form); the `:4815`/`:4997` citations are withdrawn.
* **A4** -- `ldu`/`stdu` with RA = 0 reach the EXISTING `ra == 0 && update` guard once `update` is set: a BEHAVIOUR CHANGE
  (before: an absolute access at EXTS(DS || XO), no update; after: CPU stop), one of the TWO the record names (the other:
  reserved XO now stops).
* **A5** -- `ldu` RA = RT: disclosed, not checked (after the fix RT ends = EA).  `stdu` RA = RS is valid.
* **A6 (+F1)** -- 32-bit CPUs: option (i), DISCLOSE, no width test this round: 58/62 are illegal on 32-bit implementations;
  before and after the fix a 32-bit CPU decodes them through the same arm; the MODE32 table has real doubleword handlers;
  after the fix the legal forms select them and reserved XO / RA = 0 updates stop there too.
* **A7** -- no alignment assumption.  **A8** -- the disassembler is FILED (C1), not joined; the census keeps the CURRENT text
  and attests opcode, RT/RS, RA and the raw low halfword, never the form.
* **A9 (+F1)** -- records: a CHANGELOG round block naming the DS correction and the two behaviour changes; `/* #571: */`
  tags; the ledger witness term; the MODE32 twin stated beside the (e) disclosure.  F1: the edited sites are the TWO CASE
  BODIES, each with its own mask; there is no shared mask line.

**The detector (rulings as amended):**
* **B1** -- the store half's clause-(a) artifact is the grown detector on the BASE binary BEFORE the edit (`prefix_BASE.out`);
  the frozen 8-row witness is the load half's.  Store anchor: the debugger's `dump` over a seeded window EA-1 .. EA+11.
* **B2, B3** -- graded RA rows for the XO-0 forms and `lwa`; every RA row at DS != 0 (at DS = 0 the update is invisible).
* **B4 (+F2)** -- DS = 0 value rows ship for the ADDRESS channel; no record may say they prove which table half ran.
* **B5** -- C9 (a positive-word `lwa`) is clause (e), not rowed; C18 (`stdu` RA = RS) is (e), shipped BY CHOICE.
* **B6 as ruled in F2 (dispute D3, for Grok)** -- FIVE stop sessions, a liveness `li` then the word LAST: 58/XO 3, 62/XO 2,
  62/XO 3, `ldu` RA = 0, `stdu` RA = 0 (DS != 0).  The DS = 0 x RA = 0 cells are clause (e), DISCLOSED (the floor crosses
  the guard's dominating predicates with the state the repair path reads; the repair writes `imm` and `update` and reads
  no `ra`), with Astra's note: they are "the only observer of an update conditioned on a non-zero displacement".  F1's eight
  added legal-access cells become FIVE single-axis marginals: `ld ds0 value`, `ld ra0 value`, `lwa ra0 value`,
  `std ds0 value`, `std ra0 value`.
* **B7 (+F1)** -- one D-form load and one D-form store with non-zero low displacement bits (`lwz odd`, `stw odd`) are the
  scope controls; the other 22 labels owe no rows because they do not reach the edited case bodies.
* **B8** -- clause (c) = an IDENTITY BODY for 58/62 (decode, retire, no memory, no RT/RA write; reserved XO retired),
  MEASURED, recorded `(c): measured at <artifact>`, predicted from the detector's own frozen source.
* **B9 (+F1)** -- clause (b) = each case body reinstated verbatim and both together; "raw `imm` with the XO dispatch kept" is
  a SEMANTIC PARTIAL (L7).
* **B10 (+F1)** -- the `lwa` size-3 / zero-0 leg selects `ppc_instr_invalid` and ENDS THE EMULATOR: scored "emulator
  terminated; that session's rows red; CONTROL=FAIL; sentinel present".
* **B11** -- `unassemble` every placed word before stepping; expected text = the CURRENT disassembler, the expected XO from a
  label-keyed map; the three witness words pinned to `e894ff90` / `e8b5ffa1` / `e8d6000a`.  Contract: CLAIMED / NOT CLAIMED
  / the census sentence / the stop-word rule / the two behaviour changes.
* **B12 (+F1, F2)** -- gate 13, after the `#565` block, BEFORE the NetBSD `need_file`, on `-E bareppc -M 64`: each protocol key
  counted once in ANY form, then its accepted value once (the rldimi idiom); the sentinel once; every row by name once; rows
  emitted / green / red by literal.  Two MANIFEST keys (CLASS_DETECTOR, CLASS_WITNESS), needed at STAGING.  Names capped at
  14.  Witness term `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`, scoped to the LOADS, with
  `prefix_BASE.out` the store half's clause-(a) artifact.
* **B13** -- rule D2 N/A (equality and truth tests only); ONE ask-again after a clean table.  **F2:** EIGHT sessions (loads,
  stores, five stops, the negative apparatus); N "about 39", the literal following the frozen instrument.

**Filings (ids chosen at landing):** C1 `ppcdisasmxo` LOW, C2 `ppcdisasmfpupd` LOW, C3 `ppcldxabsent` MED, C4
`ppc64on32gate` (design).  F1 on C4: "at least FOURTEEN" ungated 64-bit-only forms; "decoder-ungated" is not "same runtime
behaviour" (`extsw` in MODE32 diagnoses and returns); the filing does not pre-authorise a uniform sweep.

---

## 7. THE DRAFTER'S CHECKS -- discrepancies found while reading the records, STATED AS QUESTIONS

Each says what the drafter read or ran (read-only) and asks whether it is right.  None is a product-code finding.  Check
them; do not ratify them.

* **K1 -- the names cap and the two-space pin.**  The probe's `row()` says "14, not 15: gate 13 pins each row as `^name  `
  (two spaces) inside this %-16s column"; F2 (B12) and BUILD_SPEC 10b item 3 rest on "a 15-character name passes the assert
  and MISSES the pin"; the CHANGELOG draft credits that catch.  The row format is `"%-16s %-20s ..."`: a 15-character name is
  padded to 16 and followed by the format's literal space -- two spaces.  Drafter's measurement: four lines in that format,
  scored with `lib.sh`'s own `count` (`grep -ac -- "^$v  .*ok$"`): names of 13, 14 and 15 characters count 1; 16 counts 0.
  So the cap is harmless and its stated reason looks false (the boundary is 15).  Right?  A wrong record (R-L L4)?
* **K2 -- the session count.**  The gate block's comment says "Eight debugger-stepped sessions (loads, stores and five stop
  sessions, ...) and one bogus-machine session": the parenthesis lists seven and the sentence reads as nine.  The probe's
  docstring says "SESSIONS -- eight", counting the bogus-machine one; the CHANGELOG draft says "EIGHT stepped sessions on
  `-E bareppc -M 64`" though the negative session runs `-E nosuchmachine`.  Seven guest sessions place the census's 108
  words; the eighth is the negative control.  Which records are wrong?
* **K3 -- L5b and gate 13.**  SCORES.txt (L5b): "the probe raises before any row; the gate's sentinel pin reds".  But
  `gate_ppc.sh` runs `need_exec "$PMAX"` before every block (`lib.sh`: `[ -x "$f" ] || gate_skip ...`): an absent binary SKIPs
  gate 13 before the `#571` block runs -- the `#565` block's comment says so for its probe.  L5b itself (no sentinel, rc 1)
  is measured.  Is the gate sentence a wrong record, and does it touch clause (c) (recorded on L5)?
* **K4 -- the driver names.**  SCORES.txt names `s6_leg.run-083332.sh` + `legs571.run-083332.py`; the console it cites
  (`s6_all.out` line 1) names `s6_leg.run-083428.sh` / `legs571.run-083428.py`; only the 083428 copies exist -- in the session
  scratchpad, not under `table1_20261024/`.
* **K5 -- the detector's size.**  `wc -l regress/ppc_dsform_probe.py` = 836 (40,883 bytes, LF, md5 0266228...);
  DETECTOR_FREEZE.txt says 836; BUILD_REPORT.md section 1 and the CHANGELOG draft say 834.
* **K6 -- PRETABLE's channel for `lwa ra0 value`.**  PRETABLE.out section 4 (07:56) says it "kills L5, L8a, L8b, L9b";
  DETECTOR_FREEZE.txt (08:27) notes L9b does not reach it (XO 2) and BASE, L3, L4b, L7 red it too.  Measured: L9b green; red
  under BASE, L3, L4b, L5, L7, L8a, L8b, L8c, L10.  PRETABLE may not be edited after the fact (its mtime is the order proof)
  -- is the correction carried where a reader of PRETABLE will meet it?
* **K7 -- the stores comment.**  The STD case says "as for PPC_HI6_LD above: stdu ran as std at EA+1 with no update; XO 2 and
  3 are reserved"; `stdu` with RA = 0 now stopping at the guard (A4) is named only by the LD comment's "ldu with RA=0"
  sentence.  Does "as for ... above" carry it?
* **K8 -- a line citation this commit moves.**  The CHANGELOG draft cites the guard as `:4338-4342` -- HEAD's numbering;
  after this commit it is `cpu_ppc_instr.c` :4367-4371 (29 lines are added above it).  `:4295` does not move.
* **K9 -- what ships.**  The CHANGELOG draft says "one product file ...; three harness files" (the probe, `gate_ppc.sh`,
  `check_probe_wiring.py`); the round also edits `tools/precommit_check.sh` (SCORE_CLAIMS_MANIFEST 38 -> 39).
* **K10 -- a stores list that reads as a disclosed joint.**  The CHANGELOG draft lists "`std` at DS = 0 and RA = 0"; the
  detector has two words (`std ds0`: DS = 0, RA != 0; `std ra0`: RA = 0, DS = 0x7100), and the JOINT cell is NOT CLAIMED.
* **K11 -- "eight amendments accepted".**  So says the CHANGELOG draft of Astra's adjudication; PASS1_RULINGS.md F1 lists
  eleven amended items (A3, A6, A9/B9, B2, B7, B10, B11/B13, B12, C4, Q3, Q5); BUILD_SPEC.md section 10 has eight numbered
  builder items.  Which members does the count mean?
* **K12 -- F1's C4 qualifications.**  BUILD_SPEC section 10 item 7 wanted the C4 census ("at least fourteen"; `extsw`'s MODE32
  handler diagnoses and returns) "in the report", and section 8 a "no boot A/B is owed" sentence; BUILD_REPORT.md carries
  neither.  The CHANGELOG draft has "at least fourteen" but no `extsw` note; the OUTSTANDING_BUGS draft gives C4 as "LOW,
  open, design" and says "the uniform `rld*`-idiom fix is its own round" -- against F1's "does not pre-authorise a uniform
  sweep"?
* **K13 -- times.**  PRETABLE.out's header says "written ~08:0x"; its mtime is 07:56:54 (BUILD_REPORT: 07:56).  BUILD_REPORT
  gives the gate run as "09:03:54-09:1x"; the log ends "09:05:23 done".  It gives PREDICTIONS.txt as "08:30"; the mtime is
  08:32:01.  Every order proof still holds.
* **K14 -- a window PRETABLE names and the detector lacks.**  PRETABLE section 4 gives the stores session's windows as
  "0x21000.. and at 0x7100.. / 0x0.. for RA = 0 / DS = 0"; the detector seeds 0x21000-0x210bf and 0x70f0-0x711f only
  (`ST_REGIONS`).  The 0x0 window belonged to a `std` row at DS = 0 and RA = 0 that F2 removed.  Does any row depend on it?

---

## 8. SOURCE context -- the table, the generic handler, the two decoders, the architecture, the disassembler

### 8.1 The 64-bit dispatch table -- `src/cpus/tmp_ppc_loadstore.c` :893-958 (generated, committed), VERBATIM

Index = `size + 4*zero + 8*load + (imm==0? 16 : 0) + 32*update`.  The MODE32 table at :1923+ has the same layout with
`ppc32_` names (M2).

~~~~
893| void (*ppc_loadstore[64])(struct cpu *, struct ppc_instr_call *) = {
894| 	ppc_instr_stb,
895| 	ppc_instr_sth,
896| 	ppc_instr_stw,
897| 	ppc_instr_std,
898| 	ppc_instr_stb,
899| 	ppc_instr_sth,
900| 	ppc_instr_stw,
901| 	ppc_instr_std,
902| 	ppc_instr_lba,
903| 	ppc_instr_lha,
904| 	ppc_instr_lwa,
905| 	ppc_instr_invalid,
906| 	ppc_instr_lbz,
907| 	ppc_instr_lhz,
908| 	ppc_instr_lwz,
909| 	ppc_instr_ld,
910| 	ppc_instr_stb_0,
911| 	ppc_instr_sth_0,
912| 	ppc_instr_stw_0,
913| 	ppc_instr_std_0,
914| 	ppc_instr_stb_0,
915| 	ppc_instr_sth_0,
916| 	ppc_instr_stw_0,
917| 	ppc_instr_std_0,
918| 	ppc_instr_lba_0,
919| 	ppc_instr_lha_0,
920| 	ppc_instr_lwa_0,
921| 	ppc_instr_invalid,
922| 	ppc_instr_lbz_0,
923| 	ppc_instr_lhz_0,
924| 	ppc_instr_lwz_0,
925| 	ppc_instr_ld_0,
926| 	ppc_instr_stbu,
927| 	ppc_instr_sthu,
928| 	ppc_instr_stwu,
929| 	ppc_instr_stdu,
930| 	ppc_instr_stbu,
931| 	ppc_instr_sthu,
932| 	ppc_instr_stwu,
933| 	ppc_instr_stdu,
934| 	ppc_instr_lbau,
935| 	ppc_instr_lhau,
936| 	ppc_instr_lwau,
937| 	ppc_instr_invalid,
938| 	ppc_instr_lbzu,
939| 	ppc_instr_lhzu,
940| 	ppc_instr_lwzu,
941| 	ppc_instr_ldu,
942| 	ppc_instr_stbu_0,
943| 	ppc_instr_sthu_0,
944| 	ppc_instr_stwu_0,
945| 	ppc_instr_stdu_0,
946| 	ppc_instr_stbu_0,
947| 	ppc_instr_sthu_0,
948| 	ppc_instr_stwu_0,
949| 	ppc_instr_stdu_0,
950| 	ppc_instr_lbau_0,
951| 	ppc_instr_lhau_0,
952| 	ppc_instr_lwau_0,
953| 	ppc_instr_invalid,
954| 	ppc_instr_lbzu_0,
955| 	ppc_instr_lhzu_0,
956| 	ppc_instr_lwzu_0,
957| 	ppc_instr_ldu_0
958| };
~~~~

### 8.2 The generic handler -- `src/cpus/cpu_ppc_instr_loadstore.c` :28-60, :84-137, :162-200, VERBATIM

~~~~
28|  *  POWER/PowerPC load/store instructions.
29|  *
30|  *
31|  *  Load/store instructions have the following arguments:
32|  *
33|  *  arg[0] = pointer to the register to load to or store from
34|  *  arg[1] = pointer to the base register
35|  *
36|  *  arg[2] = offset (as an int32_t)
37|  *	     (or, for Indexed load/stores: pointer to index register)
38|  */
39| 
40| 
41| #ifndef LS_IGNOREOFS
42| void LS_GENERIC_N(struct cpu *cpu, struct ppc_instr_call *ic)
43| {
44| #ifdef MODE32
45| 	uint32_t addr =
46| #else
47| 	uint64_t addr =
48| #endif
49| 	    reg(ic->arg[1]) +
50| #ifdef LS_INDEXED
51| 	    reg(ic->arg[2]);
52| #else
53| 	    (int32_t)ic->arg[2];
54| #endif
55| 	unsigned char data[LS_SIZE];
56| 
57| 	/*  Synchronize the PC:  */
58| 	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
59| 	    / sizeof(struct ppc_instr_call);
60| 	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
...
84| 	 *  there is no PowerPC manual in this project and none is reconstructed here.
85| 	 */
86| 
87| #ifdef LS_LOAD
88| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
89| 	    MEM_READ, CACHE_DATA)) {
90| 		/*  Exception.  */
91| 		if (!cpu->running)
92| 			cpu->cd.ppc.next_ic = &nothing_call;
93| 		return;
94| 	}
95| #ifdef LS_B
96| 	reg(ic->arg[0]) =
97| #ifndef LS_ZERO
98| 	    (int8_t)
99| #endif
100| 	    data[0];
101| #endif
102| #ifdef LS_H
103| 	reg(ic->arg[0]) =
104| #ifdef LS_BYTEREVERSE
105| 	    ((data[1] << 8) + data[0]);
106| #else
107| #ifndef LS_ZERO
108| 	    (int16_t)
109| #endif
110| 	    ((data[0] << 8) + data[1]);
111| #endif /*  !BYTEREVERSE  */
112| #endif
113| #ifdef LS_W
114| 	reg(ic->arg[0]) =
115| #ifdef LS_BYTEREVERSE
116| 	    ((data[3] << 24) + (data[2] << 16) +
117| 	    (data[1] << 8) + data[0]);
118| #else  /* !LS_BYTEREVERSE  */
119| #ifndef LS_ZERO
120| 	    (int32_t)
121| #else
122| 	    (uint32_t)
123| #endif
124| 	    ((data[0] << 24) + (data[1] << 16) +
125| 	    (data[2] << 8) + data[3]);
126| #endif /* !LS_BYTEREVERSE */
127| #endif
128| #ifdef LS_D
129| 	(*(uint64_t *)(ic->arg[0])) =
130| 	    ((uint64_t)data[0] << 56) + ((uint64_t)data[1] << 48) +
131| 	    ((uint64_t)data[2] << 40) + ((uint64_t)data[3] << 32) +
132| 	    ((uint64_t)data[4] << 24) + (data[5] << 16) +
133| 	    (data[6] << 8) + data[7];
134| #endif
135| 
136| #else	/*  store:  */
137| 
...
162| #endif
163| #ifdef LS_D
164| 	{ uint64_t x = *(uint64_t *)(ic->arg[0]);
165| 	data[0] = x >> 56;
166| 	data[1] = x >> 48;
167| 	data[2] = x >> 40;
168| 	data[3] = x >> 32;
169| 	data[4] = x >> 24;
170| 	data[5] = x >> 16;
171| 	data[6] = x >> 8;
172| 	data[7] = x; }
173| #endif
174| 	if (!cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
175| 	    MEM_WRITE, CACHE_DATA)) {
176| 		/*  Exception.  */
177| 		if (!cpu->running)
178| 			cpu->cd.ppc.next_ic = &nothing_call;
179| 		return;
180| 	}
181| #endif
182| 
183| #ifdef LS_UPDATE
184| 	reg(ic->arg[1]) = addr;
185| #endif
186| }
187| #endif
188| 
189| 
190| void LS_N(struct cpu *cpu, struct ppc_instr_call *ic)
191| {
192| #ifndef MODE32
193| 	/************************************************************/
194| 	/* For now, 64-bit access is done using the slow fallback.  */
195| 	if (!cpu->is_32bit) {
196| 		LS_GENERIC_N(cpu, ic);
197| 		return;
198| 	}
199| #endif
200| 
~~~~

### 8.3 One source, two decoders -- `src/cpus/tmp_ppc_tail.c` :55-63 and :115-118, and `src/cpus/cpu_ppc.c` :1841-1843, VERBATIM

~~~~
55| #define MODE_int_t int64_t
56| #else
57| #define reg(x) (*((uint32_t *)(x)))
58| #define MODE_uint_t uint32_t
59| #define MODE_int_t int32_t
60| #endif
61| #define COMBINE(n) ppc_combine_ ## n
62| #include "quick_pc_to_pointers.h"
63| #include "cpu_ppc_instr.c"
...
115| #undef COMBINE
116| #define COMBINE(n) ppc32_combine_ ## n
117| #include "quick_pc_to_pointers.h"
118| #include "cpu_ppc_instr.c"
1841|  *  This lives here, beside update_cr0, rather than as a static in
1842|  *  cpu_ppc_instr.c: that file is compiled twice (DYNTRANS_DUALMODE_32), so a
1843|  *  static helper there would be defined twice in one translation unit.
~~~~

### 8.4 The architecture -- Book I v2.01 (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\ppc_uisa_book1_v201.txt`), the RTL lines, VERBATIM (left column; the extraction drops the assignment arrow)

~~~~
2305| if RA = 0 then b  0
2306|                 b  (RA)
2307| else
2308| 
2309| EA  b + EXTS(DS || 0b00)
2310| RT  EXTS(MEM(EA, 4))
2311| 
2312| Let the effective address (EA) be the sum
2313| 
2314| (RA|0)+(DS||0b00). The word in storage addressed
2315| 
2316| by EA is loaded into RT32:63. RT0:31 are filled with a
2317| copy of bit 0 of the loaded word.
...
2358| if RA = 0 then b  0                                    i
2359|                 b  (RA)
2360| else                                                   e
2361| 
2362| EA  b + EXTS(DS || 0b00)                               E
2363| RT  MEM(EA, 8)                                         R
2364| 
2365| Let the effective address (EA) be the sum              L
2366| (RA|0)+(DS||0b00). The doubleword in storage           (
2367| addressed by EA is loaded into RT.                     b
...
2385| EA  (RA) + EXTS(DS || 0b00)                            E
2386| RT  MEM(EA, 8)                                         R
2387| RA  EA                                                 R
2388| 
2389| Let the effective address (EA) be the sum              L
2390| (RA)+(DS||0b00). The doubleword in storage             T
2391| addressed by EA is loaded into RT.                     i
2392| 
2393| EA is placed into register RA.                         E
2394| 
2395| If R A = 0 or RA=RT, the instruction form is invalid.  I
...
2581| if RA = 0 then b  0                                  if
2582|             b  (RA)
2583| else                                                 els
2584| 
2585| EA  b + EXTS(DS || 0b00)                             EA
2586| MEM(EA, 8)  (RS)                                     MEM
2587| 
2588| Let the effective address (EA) be the sum            Let
2589| (RA|0)+(DS||0b00). (RS) is stored into the           (RA
2590| doubleword in storage addressed by EA.               sto
...
2608| EA  (RA) + EXTS(DS || 0b00)                          EA
2609| MEM(EA, 8)  (RS)                                     MEM
2610| RA  EA                                               RA
2611| 
2612| Let the effective address (EA) be the sum            Let
2613| (RA)+(DS||0b00). (RS) is stored into the doubleword  (RS
2614| in storage addressed by EA.                          add
2615| 
2616| EA is placed into register RA.                       EA
2617| 
2618| If RA=0, the instruction form is invalid.            If
~~~~

and the 2005 PEM (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\ppc_pem_32and64_2005.txt`) :6253, VERBATIM:

~~~~
6253| The following primary opcodes are defined for 64-bit implementations only and are illegal on 32-bit implementations: 2, 30, 58, 62
~~~~

### 8.5 The disassembler arm the filings C1/C2 cite -- `src/cpus/cpu_ppc.c` :1468-1520, VERBATIM

~~~~
1468| 	case PPC_HI6_LD:
1469| 	case PPC_HI6_LWZ:
1470| 	case PPC_HI6_LWZU:
1471| 	case PPC_HI6_LHZ:
1472| 	case PPC_HI6_LHZU:
1473| 	case PPC_HI6_LHA:
1474| 	case PPC_HI6_LHAU:
1475| 	case PPC_HI6_LBZ:
1476| 	case PPC_HI6_LBZU:
1477| 	case PPC_HI6_LFD:
1478| 	case PPC_HI6_LFS:
1479| 	case PPC_HI6_LMW:
1480| 	case PPC_HI6_STD:
1481| 	case PPC_HI6_STW:
1482| 	case PPC_HI6_STWU:
1483| 	case PPC_HI6_STH:
1484| 	case PPC_HI6_STHU:
1485| 	case PPC_HI6_STB:
1486| 	case PPC_HI6_STBU:
1487| 	case PPC_HI6_STMW:
1488| 	case PPC_HI6_STFD:
1489| 	case PPC_HI6_STFS:
1490| 		/*  NOTE: Loads use rt, not rs, but are otherwise similar
1491| 		    to stores  */
1492| 		load = 0; wlen = 0;
1493| 		rs = (iword >> 21) & 31;
1494| 		ra = (iword >> 16) & 31;
1495| 		imm = (int16_t)(iword & 0xffff);
1496| 		fpreg = 0;
1497| 		switch (hi6) {
1498| 		case PPC_HI6_LD:  load=1; wlen = 8; mnem = "ld"; break;
1499| 		case PPC_HI6_LWZ:  load=1; wlen = 4;
1500| 			mnem = power? "l" : "lwz"; break;
1501| 		case PPC_HI6_LWZU: load=1; wlen = 4;
1502| 			mnem = power? "lu" : "lwzu"; break;
1503| 		case PPC_HI6_LHZ:  load=1; wlen = 2;
1504| 			mnem = "lhz"; break;
1505| 		case PPC_HI6_LHZU: load=1; wlen = 2;
1506| 			mnem = "lhzu"; break;
1507| 		case PPC_HI6_LHA:  load=2; wlen = 2;
1508| 			mnem = "lha"; break;
1509| 		case PPC_HI6_LHAU: load=2; wlen = 2;
1510| 			mnem = "lhau"; break;
1511| 		case PPC_HI6_LBZ:  load=1; wlen = 1;
1512| 			mnem = "lbz"; break;
1513| 		case PPC_HI6_LBZU: load=1; wlen = 1;
1514| 			mnem = "lbzu"; break;
1515| 		case PPC_HI6_LFD:  load=1; fpreg=1; wlen=8; mnem = "lfd"; break;
1516| 		case PPC_HI6_LFS:  load=1; fpreg=1; wlen=4; mnem = "lfs"; break;
1517| 		case PPC_HI6_STD:  wlen=8; mnem = "std"; break;
1518| 		case PPC_HI6_STW:  wlen=4; mnem = power? "st" : "stw"; break;
1519| 		case PPC_HI6_STWU: wlen=4; mnem = power? "stu" : "stwu"; break;
1520| 		case PPC_HI6_STH:  wlen=2; mnem = "sth"; break;
~~~~

---

## 9. The records under review -- what the landing will say

### 9.1 The CHANGELOG round block -- a DRAFT, frozen into this brief (main-loop scratchpad `t2/landing/changelog_571.draft.md`, 15,293 bytes, md5 `2f9af87160b8a888ef2a080f84258354`, mtime 09:07:42; do not open the scratchpad file -- it may have moved on).  Its `<<FILL>>` marks are the landing's to clear.  VERBATIM:

~~~~
  # `#571` (ppcdsformxo): the PowerPC decoder folded the DS-form XO bits into the displacement, so `ldu` and `lwa` ran as `ld` at EA+1 / EA+2 and `stdu` ran as `std` at EA+1 with no base update -- opcodes 58 and 62 now decode their five forms, reserved encodings and the RA = 0 update forms stop the cpu, and a 39-row rung-3 detector gates it in gate 13

  **The defect** (`ppcdsformxo`, HIGH; filed 2026-10-22 from the external-fixes research, T2 of its batch; class
  GUEST-CORRUPTION).  `src/cpus/cpu_ppc_instr.c`'s D/DS-form load/store arm takes the whole low halfword as the
  displacement (`imm = (int16_t)iword`) for all 24 of its primary opcodes and gives opcodes 58 (`PPC_HI6_LD`) and 62
  (`PPC_HI6_STD`) one fixed decode each -- an 8-byte load / store with no update -- although in the DS form the low two
  bits of the halfword are the XO field that selects `ld` / `ldu` / `lwa` (58) and `std` / `stdu` (62).  So on a 64-bit
  CPU every `ldu` loaded from EA+1 and left RA alone, every `lwa` loaded a DOUBLEWORD from EA+2 instead of a
  sign-extended word, and every `stdu` -- the instruction every PowerPC64 stack frame is pushed with -- stored its 8
  bytes at EA+1 and left the stack pointer alone.  The rung-3 witness (`regress/artifacts/ppcdsformxo/
  witness_20261024/`, cold debugger on UNMODIFIED `bareppc -M 64` = PPC970, HEAD `add098b9` = `c8fcb5ff` in source) is RED
  on HEAD: 5/8, three symptom rows red for the reason under test -- `ldu value` names offset 0x21 of a counting pattern
  whose architectural EA is offset 0x20, `ldu RA after` shows RA = 0x20080 where EA (0x20020) was owed, `lwa value` is
  the doubleword at offset 0x8a where the sign-extended word at 0x88 (`0xffffffff88898a8b`) was owed; the controls are
  green (`ld` at XO 0 with a negative DS reads the right doubleword, `lwz` on the same pattern reads the right word, a
  liveness `li`, a 13/13 disassembly census, a bogus-machine-TYPE negative control).  The store half is not in the witness
  (three store-bearing witness attempts were stopped before writing); it is measured RED on the base binary by the
  detector's own pre-fix run (`table1_20261024/prefix_BASE.out`, 17 of 39 red, below).

  **What ships** (one product file, byte-identical in `GXEMUL-SEC/` and `est/`; three harness files).
  * `src/cpus/cpu_ppc_instr.c` -- inside the arm's inner `switch (main_opcode)`, `case PPC_HI6_LD:` and
    `case PPC_HI6_STD:` become DS-form decodes: each re-assigns the shared `imm` to `(int16_t)(iword & ~3)` -- EXTS(DS ||
    0b00), enumerated equal for every DS and XO because the clear never reaches the halfword's sign bit -- so the table
    index (`imm == 0` selects the `_0` handler family) and `ic->arg[2]` both see the masked displacement, and dispatches on
    `iword & 3`: 58 -> `ld` (XO 0), `ldu` (XO 1, `update`), `lwa` (XO 2, `size` 2 and `zero` 0: the existing
    sign-extending word handler `ppc_instr_lwa`, slot 10 of the generated `ppc_loadstore[]`), reserved XO 3 -> the arm's
    bare `goto bad`; 62 -> `std` (XO 0), `stdu` (XO 1), reserved XO 2 and 3 -> `goto bad`.  No handler changes: every form
    selects a slot the generated table already holds (`ld` 15/31, `ldu` 47/63, `lwa` 10/26, `std` 7/23, `stdu` 39/55 --
    `tmp_ppc_loadstore.c:893-958`), and none reaches `ppc_instr_invalid` (slots 11/27/43/59, `load && !zero && size == 3`).
    TWO BEHAVIOUR CHANGES besides the displacement: a reserved XO, which executed as `ld`/`std` at EA+2 / EA+3, now stops
    the cpu through the common tail (`cpu_dyntrans.c:2004-2014`: `UNIMPLEMENTED instruction at 0x...`, printed under
    single-step too; nothing is delivered to the guest -- the tree has no Program interrupt), and `ldu`/`stdu` with RA = 0,
    which executed at the absolute address EXTS(DS || XO) with no update, now reach the arm's EXISTING `ra == 0 && update`
    guard (`:4338-4342`) and stop -- the disposition every other update form in the arm already takes.  `ldu` with RA = RT
    (an invalid form; Book I allows boundedly undefined results) is DISCLOSED, not checked -- the handler loads RT and then
    writes RA = RT with EA, as the sibling update loads do; `stdu` with RA = RS is VALID and stores the old RS before the
    update.  32-bit CPUs: opcodes 58 and 62 are illegal on 32-bit implementations (PEM :6253); before and after this fix a
    32-bit CPU decodes them through the same arm (one source builds both decoders); the MODE32 table holds real doubleword
    handlers (`tmp_ppc_loadstore.c:1923+`), so no host exit either way; after the fix the legal forms select those
    handlers and reserved XO / RA = 0 updates stop there too; no width test this round (filed, below).  The shared
    assignment at `:4295` and the other 22 opcodes of the arm are NOT touched.  Option set recorded in
    `pass1_20261024/PASS1_RULINGS.md` A3 / A6 / D1 / D2.
  * `regress/ppc_dsform_probe.py` (new; 834 lines, 40,883 bytes) -- the detector, the promoted copy of the witness probe (the
    witness file stays byte-identical under `witness_20261024/`, md5 `5e96b69df49ac82e10b3118780899549`; its build and run
    receipts are frozen in `witness_20261024/receipts/`).  Frozen before its first run at md5
    `0266228894811ba6c51cff82585753c9` (`table1_20261024/BASELINE.out`, `DETECTOR_FREEZE.txt`).  EIGHT stepped sessions on `-E bareppc -M 64`: loads (the five witness words plus
    `ld`/`ldu`/`lwa` at DS = 0, `ld`/`lwa` with RA = 0 from a seeded low-memory window, a `lwz` at +6 whose displacement
    has non-zero low bits -- the control that sees a mask applied to every opcode), stores (`std`, `stdu`, `stdu` at DS = 0,
    `stdu rA,DS(rA)`, `std` at DS = 0 and RA = 0, a `stw` at +6; every destination read back by the debugger's `dump` over a
    pre-seeded window EA-1 .. EA+11, each source eight distinct bytes), five stop sessions (58/XO 3, 62/XO 2, 62/XO 3,
    `ldu` RA = 0, `stdu` RA = 0 -- each a liveness `li` then the word LAST, since `bad:` clears `running`), and the
    negative apparatus.  Every word is produced by the probe's encoder; the disassembly census compares every placed word
    against the tree's CURRENT disassembler text (which folds XO -- see the filing) with the expected XO taken from a
    label-keyed map, and the three witness words are pinned to their literals.  Row names are capped at 14 characters so
    the gate's two-space pin cannot miss one (the `%-16s` column).  Protocol: `PPC_DSFORM_RESULT=ok/N`,
    `PPC_DSFORM_CONTROL=OK|FAIL`, `PPC_DSFORM_SYMPTOM=PRESENT n/m|ABSENT|MIXED`, `PPC_DSFORM_RED=<names>|none`,
    sentinel `PPC_DSFORM_PROBE_DONE`; non-zero exit on any red.
  * `regress/gate_ppc.sh` (gate 13) -- a `#571` block directly after the `#565` rldicl block and BEFORE the NetBSD image
    `need_file`, on the same machine as the register probes: the probe into `$LOGDIR` with `|| true`; every protocol key
    counted exactly once in any form and then its accepted value once (`RESULT=39/39`, `CONTROL=OK`,
    `SYMPTOM=ABSENT`, `RED=none`); the sentinel once; every one of the 39 row names once and green; rows emitted /
    green / red pinned by literal.
  * `tools/pipeline/check_probe_wiring.py` -- two MANIFEST keys: `ppc_dsform_probe.py` CLASS_DETECTOR (gate 13,
    39 rows, the table path) and `artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py` CLASS_WITNESS.

  **Measured** (`regress/artifacts/ppcdsformxo/table1_20261024/`; every score against its instrument revision and
  denominator; the instrument md5 in `BASELINE.out`; `PRETABLE.out` written before table 1, `PREDICTIONS.txt` per leg
  before each leg).
  * Pre-fix, the BASE binary (HEAD `c8fcb5ff`'s source, binary md5 `3cd0501c`): `prefix_BASE.out` **22/39, CONTROL=OK,
    SYMPTOM=PRESENT 17/17** -- the 17 symptom rows (`ldu value`, `ldu RA after`, `ldu ds0 value`, `lwa value`, `lwa ds0 value`,
    `lwa ra0 value`, `stdu value`, `stdu neigh`, `stdu RA after`, `stdu ds0 value`, `stdu alias val`, `stdu alias RA`,
    `xo58_3 bad`, `xo62_2 bad`, `xo62_3 bad`, `ldu ra0 bad`, `stdu ra0 bad`), each red by the misdirected address, the
    shifted destination window or the missing stop; every control green.  This is the STORE half's clause-(a) artifact.
  * Post-fix: `fixed.out` **39/39, ABSENT, RED=none**; the frozen 8-row witness `fixed_witness8.out` **8/8, ABSENT** (clause
    (a), same script as the witness).
  * The kill table (`SCORES.txt`; `PREDICTIONS.txt` written per leg before any leg ran; sixteen variant legs, each a
    discarded clone of the fixed tree with a `.MUTANT` sentinel): clause (b) `L3` both case bodies reinstated 22/39, `L4b`
    the 58 case alone 31/39, `L4c` the 62 case alone 30/39; clause (c) `L5` the identity body (the no-op handler for both
    opcodes) 17/39 CONTROL=FAIL -- **(c): measured at `L5_identity.out`**; `L5b` the binary absent: no sentinel; clause (d)
    `L6a`/`L6b` update dropped 37/39, 36/39; `L7` the raw displacement kept 27/39; `L8a`/`L8b` the `lwa` width and extension
    nulled 36/39 each; `L8c` `lwa` at size 3 with `zero` 0 selects the invalid handler and ENDS THE EMULATOR on the loads
    session -- 25/39, the exit recorded on the session line, the sentinel still printed (scored as emulator termination,
    never as a wrong-width transfer); growth `L9a` XO 0 as XO 1 33/39, `L9b` EA+1 on XO 0 33/39, `L10` update on every form
    31/39, `L11` the mask on the shared assignment 37/39 (the two D-form scope rows), `L12a`/`L12b` a reserved test opened
    38/39 each.  Fourteen legs at their written prediction exactly; `L9a` and `L10` two rows REDDER than predicted (the
    session-liveness rows: an RA = 0 XO-0 word turned into a refusal stops its session) -- prediction misses recorded in
    `SCORES.txt`, no detector miss, no leg green, no leg red for another reason.
  * Two-part clearance (`CLEARANCE.out`): build/ CLEAN + FRESH (gxemul `a142d92a`), build-asan/ CLEAN + FRESH (`79d75442`),
    /tmp/gxsec-build CLEAN + FRESH (`14ede3bd`); est/: source tree, part 2 N/A.
  * Gate 13 alone (`gate13_20261024.out`, `bash run.sh 13`, build/gxemul `a142d92a`): **PASS, 193 checks, REGRESS_PASS** --
    the `#571` block's 53 checks all ok (39 rows by name, census 108/108, rows run/green/red 39/39/0; the gate's detector
    log preserved as `gate13_ppc_dsform.log`); the siblings unchanged (rlwimi 28/28, rldimi 29/29, rldicl 24/24 with one
    SCORE line) and the image-gated rounding probe green -- the one other consumer of the edited arm (its FP D-forms and
    `stw`; its displacements are all multiples of 4, so it is collateral, not low-bit coverage).

  **Panel.**  Pass 1 (`pass1_20261024/`): GPT-6 Astra (ultra, file-reading, pointer form), Grok 4.7 (xhigh, plan mode),
  Gemini 4 Argon (file-reading through agy, `gemini-4-argon-high`; transport and reading-scope caveat in
  `argon_transport_20261024.txt`), GLM 5.3 and DeepSeek v4-pro (packet-fed, the 74,595-byte PACKET form split Q1-2 /
  Q3-4) -- seven answers: five READY WITH CHANGES, DeepSeek NOT READY twice (on a 32-bit width test, ruled (i) disclose,
  and on the store rows, specified in B1/B6).  Fable 5.1 HELD by the owner (hold question in `fable5.HELD.txt`); kimi,
  minimax and the Opus seat deliberately not fired by roster (`roster_NOT_FIRED.txt`).  The main loop's 31 dispositions
  and eight disputes are `PASS1_RULINGS.md` (A1-A9, B1-B13, C1-C9, D1-D8, with five measured main-loop checks M1-M5);
  ADJUDICATED by GPT-6 Astra (`adj/codex_t2p1adj.txt`, AMEND: eight amendments accepted, it withdrew its own (ii) and
  "all 22 labels" claims) and by Grok 4.7 (`adj/grok_t2p1adj.txt`, AMEND) -- the two adjudicators disagreed on ONE point
  (whether the DS = 0 x RA = 0 refusal cells are floor) and the main loop ruled for Grok on the carrier's pass-11 bound,
  trimming Astra's eight added legal-access cells to the five single-axis marginals (section F2).  Grok also caught the
  padded-column trap in the proposed names (a 15-character name passes the probe's assert and misses the gate's
  two-space pin) and a false citation in A3.  Pass 2 (`pass2_20261024/`): <<FILL>>.  F2 adjudication: <<FILL>>.

  **What the records claim, and do not.**  The detector claims the five legal DS forms at DS != 0, at DS = 0 and (the
  non-update forms) at RA = 0, the three reserved encodings, the two RA = 0 update stops, and the D-form scope controls
  (a load and a store whose displacement has non-zero low bits), on PPC970 with translation off.  NOT CLAIMED, disclosed
  in the probe's contract: `ldu` RA = RT (D1); 32-bit CPUs (illegal opcodes, decoded unchanged; the future fix is the
  `rld*` width idiom applied to the whole ungated set, filed); the DS = 0 x RA = 0 update cells (multi-axis joint, the only
  observer of an update conditioned on a non-zero displacement); a positive-word `lwa` (the sign is the callee's cast);
  translation on, MSR SF, page-crossing EAs, the indexed forms, an access that fails (the translation-off failure path
  exists but is gated by `-T`, which the probe does not pass); the disassembler's mnemonics (the census attests opcode,
  RT/RS, RA and the raw halfword against the CURRENT text, never the form).  Three premises of the pass-1 brief were
  corrected in the record rather than carried: "the two uses of `imm` matter only for DS = 0" (inverted: `arg[2]` matters
  for every XO != 0 word; the index use is unobservable on PPC970), "a base not a multiple of 8 gives an unaligned
  `ld`/`std`" (base residue 4 plus displacement residue 4 is aligned), and "`lwa` left at size 3 consumes the neighbour
  word" (with `zero` 0 it selects `ppc_instr_invalid` and exits the emulator -- the probe records the exit and still
  prints its sentinel).

  **Filed** (ledger rows, all source-derived unless stated): `ppcdisasmxo` (LOW -- `cpu_ppc.c:1495-1517` prints `ld`/`std`
  with the XO folded into the displacement for every opcode-58/62 word; guest-invisible; witness = the frozen census lines
  `ld r5,-95(r21)` / `ld r6,10(r22)`; its fix owes the oracle-correction order: re-pin the census first),
  `ppcdisasmfpupd` (LOW -- the disassembler has no case for `LFDU`/`LFSU`/`STFDU`/`STFSU`, which execute since `#310` and
  disassemble as an unimplemented primary opcode), `ppcldxabsent` (MED -- `ldx`/`ldux`/`lwax`/`lwaux` have no `PPC_31_*`
  define and reach opcode 31's `default: goto bad` on every CPU while `stdx`/`stdux` are implemented: a legal 64-bit
  guest load stops the cpu; witness shape: one stepped `ldx` word on HEAD PPC970), `ppc64on32gate` (design -- at least
  fourteen 64-bit-only forms decode ungated on 32-bit CPUs (`cmpd`, `cmpld`, `ld`, `std`, `rfid`, `mtmsrd`, `ldarx`,
  `stdcx.`, `stdx`, `stdux`, `extsw`, `sld`, ...), eleven more are absent on every width; the licensed fix is the `rld*`
  idiom (PEM :6253 + the opcode-30 precedent) applied to the ungated implemented set in its own round).
  <<FILL: confirm the four ids are unused in the ledger before landing (grep); M3 found 0 hits for the names.>>

  **Records.**  The ledger row's witness is `probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`
  (rung 3, the LOAD half; the store half's clause-(a) artifact is `table1_20261024/prefix_BASE.out`), state <<FILL>>,
  commits <<FILL>>.  The brief's own defects are recorded in `PASS1_RULINGS.md` C8 (the session list omitted the negative
  control; "every path exists at HEAD" was false for the untracked witness paths; P2 inverted; the `lwa size 3` gloss).
  CRIT's `testppc` is `bareppc` (both PPC970; `bareppc` has no devices).  Pass-2 receipt: `regress/pass2_ledger.tsv`
  <<FILL>>.
~~~~

### 9.2 The draft's numbers against the artifacts that carry them (the drafter's table -- check it)

Each claim of the frozen CHANGELOG draft that states a number or names an artifact, beside what that artifact says when
read (or what was run) at drafting.  "match" means the artifact says the same; every other verdict points to a K check.

| # | the draft says | the artifact | what it says | verdict |
|---|---|---|---|---|
| 1 | the witness is RED on HEAD, 5/8, three symptom rows | `witness_20261024/WITNESS_headbin.out` | `RESULT=5/8`, `SYMPTOM=PRESENT 3/3`, red `ldu value`, `ldu RA after`, `lwa value` | match |
| 2 | the detector is "834 lines, 40,883 bytes" | the file; `DETECTOR_FREEZE.txt` | `wc -l` 836, 40,883 bytes; the freeze says "probe lines: 836" | K5 |
| 3 | frozen at md5 `0266228...` before its first run | `BASELINE.out`, `DETECTOR_FREEZE.txt` | "DETECTOR FROZEN 2026-10-24 08:29:04 ... frozen BEFORE prefix_BASE.out" | match |
| 4 | "EIGHT stepped sessions on `-E bareppc -M 64`" incl. the negative apparatus | the probe | seven guest sessions on `bareppc`; the negative one runs `-E nosuchmachine` | K2 |
| 5 | stores include "`std` at DS = 0 and RA = 0" | the probe's stores program | two words (`std ds0`, `std ra0`); the joint cell is NOT CLAIMED | K10 |
| 6 | "one product file ...; three harness files" | `BUILD_REPORT.md` section 2; `diff_precommit.patch` | four harness files: `tools/precommit_check.sh` too | K9 |
| 7 | the guard "`:4338-4342`" | `cpu_ppc_instr.c` | HEAD :4338-4342; after this commit :4367-4371 | K8 |
| 8 | pre-fix 22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17, the 17 names | `prefix_BASE.out` | the same, the same 17 names | match |
| 9 | post-fix 39/39 ABSENT RED=none; the witness 8/8 ABSENT | `fixed.out`, `fixed_witness8.out` | the same | match |
| 10 | L3 22, L4b 31, L4c 30, L5 17 (CONTROL=FAIL), L5b no sentinel, L6a 37, L6b 36, L7 27, L8a 36, L8b 36, L8c 25, L9a 33, L9b 33, L10 31, L11 37, L12a 38, L12b 38 (of 39) | each `L*.out` | the same seventeen results | match |
| 11 | fourteen legs at their written prediction; L9a and L10 two rows redder | `SCORES.txt`, `PREDICTIONS.txt` | the same | match |
| 12 | clearance: build/ `a142d92a`, build-asan/ `79d75442`, /tmp/gxsec-build `14ede3bd`, est/ N/A | `CLEARANCE.out` | the same; re-checked at drafting | match |
| 13 | gate 13 PASS, 193 checks; the block's 53; census 108/108; rows 39/39/0; siblings 28/28, 29/29, 24/24 | `gate13_20261024.out` | the same | match |
| 14 | "a 15-character name passes the probe's assert and misses the gate's two-space pin" | K1's measurement | a 15-character name MATCHES the pin; 16 misses | K1 |
| 15 | Astra's adjudication: "eight amendments accepted" | `PASS1_RULINGS.md` F1; `BUILD_SPEC.md` section 10 | F1: eleven amended items; section 10: eight builder items | K11 |
| 16 | "31 dispositions and eight disputes" | `PASS1_RULINGS.md` | A1-A9 + B1-B13 + C1-C9 = 31; D1-D8 = 8 | match |
| 17 | the BASE binary is "HEAD `c8fcb5ff`'s source" | `BASELINE.out`; C0 part 1 | BASELINE names HEAD `add098b9`; no commit `c8fcb5ff..HEAD` touches `src/` | match |
| 18 | `ppcdisasmxo` cites `cpu_ppc.c:1495-1517`; the four ids are to be confirmed unused | `cpu_ppc.c`; C0 part 4 | :1495 the folded `imm`, :1498 `ld`, :1517 `std`; zero rows per id at HEAD | match |


### 9.3 The ledger witness term -- a DRAFT (`t2/landing/witness_term.txt`, md5 `3f755d68`), frozen, VERBATIM

~~~~
probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py -- rung 3 on the UNMODIFIED in-tree bareppc -M 64 (PPC970) through the cold debugger, the LOADS only: RED on HEAD 5/8 with the three symptom rows red for the reason under test (ldu loads EA+1 and leaves RA; lwa loads a doubleword at EA+2) and five controls green (WITNESS_headbin.out); the same frozen script 8/8 SYMPTOM=ABSENT on the fixed binary (table1_20261024/fixed_witness8.out).  The STORE half's clause-(a) artifact is the shipped detector's own pre-fix run, table1_20261024/prefix_BASE.out (22/39, SYMPTOM=PRESENT 17/17: stdu stores at EA+1 with no update; 62/XO 2-3 store instead of stopping).  The shipped detector regress/ppc_dsform_probe.py (39 rows, 8 sessions, gate 13, pinned at 39) is fixed 39/39; floor (b) L3/L4b/L4c, (c) measured L5 17/39 CONTROL=FAIL and L5b no sentinel, (d) L6a-L8c, growth L9a-L12b -- 16 of 16 legs red, 14 at their written prediction (SCORES.txt).  Not covered: ldu with RA = RT, 32-bit CPUs, the DS = 0 x RA = 0 joints, a positive-word lwa, translation on, the indexed forms, the disassembler's text.
~~~~

### 9.4 The OUTSTANDING_BUGS section and the four filings -- a DRAFT (`t2/landing/ob_571.md`, md5 `51b949ae`), frozen, VERBATIM

~~~~
  ### 2026-10-24 -- `ppcdsformxo` fixed by `#571` (held for Fable); `ppcdisasmxo`, `ppcdisasmfpupd`, `ppcldxabsent` and `ppc64on32gate` filed

  `#571` makes `src/cpus/cpu_ppc_instr.c`'s D/DS-form arm decode primary opcodes 58 and 62 as DS forms: the two case
  bodies re-assign the shared `imm` to `(int16_t)(iword & ~3)` -- EXTS(DS || 0b00), the XO bits no longer part of the
  displacement -- and dispatch on `iword & 3`: `ld` / `ldu` (RA <- EA) / `lwa` (the sign-extended word, the existing
  `ppc_instr_lwa` handler) and `std` / `stdu`, the reserved encodings (58 with XO 3, 62 with XO 2 or 3) taking the arm's
  bare `goto bad` (the common tail's `UNIMPLEMENTED instruction` stop) and `ldu`/`stdu` with RA = 0 reaching the arm's
  existing `ra == 0 && update` guard.  Before it every `ldu` loaded from EA+1 and left RA, every `lwa` loaded a DOUBLEWORD
  from EA+2, and every `stdu` -- the instruction every PowerPC64 stack frame is pushed with -- stored at EA+1 and left the
  stack pointer.  No handler changed (every form selects a slot the generated table already holds); the shared
  assignment and the other 22 opcodes of the arm are untouched; 32-bit CPUs are disclosed (illegal opcodes, decoded
  unchanged through the same source, no width test -- filed as `ppc64on32gate`).  It ships `regress/ppc_dsform_probe.py`,
  a 39-row rung-3 detector on the unmodified `bareppc -M 64` (eight debugger-stepped sessions: the loads, the stores with
  every destination read back by the debugger's dump, five stop sessions, the bogus-machine control; every word from the
  probe's own encoder; a census of all 108 placed words against the tree's current disassembler text), gated in gate 13
  with every row identity, the four protocol keys and the census pinned.  Measured in
  `regress/artifacts/ppcdsformxo/table1_20261024/` (pre-fix 22/39 with the 17 symptom rows red for the reason under test
  -- the store half's clause-(a) artifact; fixed 39/39; the frozen 8-row witness 8/8; 16 of 16 kill-table legs red, 14 at
  their written prediction, the identity body measured 17/39; clearance clean and fresh on every build tree; gate 13
  PASS with 193 checks, the `#571` block 53 of 53).  Panel: Astra, Grok, Argon (through agy), GLM 5.3 and DeepSeek on
  pass 1 (five READY WITH CHANGES, DeepSeek NOT READY twice on the 32-bit test and the store rows), adjudicated by Astra
  (AMEND) and by Grok (AMEND; the one adjudicator disagreement -- the DS = 0 x RA = 0 refusal cells -- ruled for Grok on
  the carrier's floor bound); PASS2_SUMMARY_GOES_HERE; Fable HELD with its question.  The row's witness is the frozen
  rung-3 probe (`witness_20261024/ppc_dsform_probe.py`, RED on HEAD 5/8, the loads); the store half's pre-fix red is the
  detector's own `prefix_BASE.out`.  Not claimed: `ldu` with RA = RT, 32-bit CPUs, the DS = 0 x RA = 0 joints, a
  positive-word `lwa`, translation on, the indexed forms, the disassembler's text.

  * **`ppcdisasmxo` (LOW, open)** -- new.  cpus/cpu_ppc.c:1495-1517: the disassembler folds the XO bits into the
    displacement and prints `ld`/`std` for every opcode-58/62 word (`ldu r5,-96(r21)` appears as `ld r5,-95(r21)`);
    guest-invisible.  Witnessed by the frozen witness's census lines.  Its fix owes the oracle-correction order: re-pin
    the detector's `unasm census` expectations first, measure HEAD red, then edit.
  * **`ppcdisasmfpupd` (LOW, open)** -- new.  cpus/cpu_ppc.c:1468-1489: no case for LFDU/LFSU/STFDU/STFSU, which execute
    since `#310` and disassemble as an unimplemented primary opcode.  Found by three seats independently; unfiled before
    this row.  Source-derived.
  * **`ppcldxabsent` (MED, open)** -- new.  include/opcodes_ppc.h + opcode 31's dispatch: `ldx`/`ldux`/`lwax`/`lwaux` have
    no `PPC_31_*` define and reach `default: goto bad` on every cpu while `stdx`/`stdux` are implemented -- a legal 64-bit
    guest's indexed doubleword load stops the cpu.  Unfiled before this row (the main loop's grep of the bug file and
    all 1,079 ledger rows).  Source-derived; the rung-3 witness shape is one stepped `ldx` word on HEAD PPC970.
  * **`ppc64on32gate` (LOW, open, design)** -- new.  At least fourteen 64-bit-only instructions decode with no width test
    on a 32-bit cpu (only `rld*` is gated) and eleven more are absent on every width; PEM :6253 makes opcodes 2, 30, 58
    and 62 illegal on 32-bit implementations.  `#571` discloses it; the uniform `rld*`-idiom fix is its own round, with a
    32-bit session row per gated label.
~~~~

### 9.5 `BUILD_REPORT.md` (table1, 09:06:04), VERBATIM

~~~~
  # T2 / round #571 (ppcdsformxo) -- BUILD_REPORT.md (the main loop as builder, with one Opus writing agent; 2026-10-24)

  ## 1. What was done, in order (BUILD_SPEC.md sections 2-9 under 10 and 10b)
  * 07:41-07:5x: the Opus BUILDER agent and then a records agent were each stopped by the harness's safety classifier before
    writing anything (checkpoint `## 087a90`); nothing on disk, no tree touched.  The build was split: an Opus WRITING agent
    (S3) produced the detector, the gate block and the MANIFEST keys (no runs); every run, build and record below was done by
    the main loop with scripts in the session scratchpad `t2/build/` (frozen copies for the long jobs).
  * 07:54 `BASELINE.out`: HEAD add098b9; `src/cpus/cpu_ppc_instr.c` at md5 87a766e0 in GXEMUL-SEC, est/, build/, build-asan/,
    /tmp/gxsec-build and /tmp/gxt2/base; every binary FRESH; the base binary's md5 equals the witness's (3cd0501c); no sentinel.
  * 07:56 `PRETABLE.out` (before any table): sibling parity, claim -> row, guard/body partitions with EXHAUSTED/SAMPLED, the
    CHANNEL per row with the leg it kills, the diff against the brief's 26 cells.
  * 08:26 S3 delivered `regress/ppc_dsform_probe.py` (40,883 b, md5 0266228894811ba6c51cff82585753c9, 834 lines, LF; N = 39,
    8 sessions, 108 census words, names <= 14 with the assert changed to 14 and a comment naming the gate pin), the gate-13
    block in `regress/gate_ppc.sh` (working tree == staged copy `staged/gate_ppc.sh.txt`, md5 d361db09), the two MANIFEST keys
    (working tree + `staged/check_probe_wiring.py.txt` from the HEAD blob; identical insertions), `DETECTOR_FREEZE.txt`,
    `staged/INSERTIONS.txt`.  Its logic check with a debugger stand-in (no emulator) predicted 22/39 on BASE and 39/39 fixed.
  * 08:29 the detector FROZEN (md5 appended to BASELINE.out), then `prefix_BASE.out` on /tmp/gxt2/base/gxemul:
    **22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17** -- every red row's got-value is the misdirected address, the shifted window
    or the missing stop (read row by row).
  * 08:30 `PREDICTIONS.txt` written per leg from the frozen source, before any leg.
  * 08:30-08:32 S5: /tmp/gxt2/work = cp -a of base; `patch571.py` applied (+29 lines, two `#571` tags); `rm src/cpus/*.o; make`
    rc 0, 0 warnings, FRESH; `fixed.out` **39/39 ABSENT RED=none**; `fixed_witness8.out` (the untouched witness) **8/8 ABSENT**.
    The same patch applied to GXEMUL-SEC and est/ (all three copies md5 2015e243f7af8e93fc2b5c283223bde5).
  * 08:33-08:54 S6: 16 variant legs (`legs571.py`, each a `cp -a` of work with a `.MUTANT` sentinel, rebuilt, measured by the
    frozen detector, then DISCARDED) + L5b; `SCORES.txt`; `/tmp/gxt2/legs` empty at TABLE_DONE.
  * 08:56-09:03 S7: the fixed file propagated to build/, build-asan/, /tmp/gxsec-build; each rebuilt; `CLEARANCE.out`.
  * 09:0x S8: gate 13 alone (`bash run.sh 13`); `gate13_20261024.out` -- see section 6.
  * tools/precommit_check.sh: SCORE_CLAIMS_MANIFEST 38 -> 39 with its dated line (`check_score_claims.py`: PASS, 39 pinned).

  ## 2. Diff stat (working tree vs HEAD add098b9)
  | file | change |
  |---|---|
  | `src/cpus/cpu_ppc_instr.c` | +31 / -2 (two hunks: the `case PPC_HI6_LD:` and `case PPC_HI6_STD:` bodies of the inner switch) -- byte-identical in GXEMUL-SEC, est/ and the three build trees |
  | `regress/ppc_dsform_probe.py` | NEW, 834 lines |
  | `regress/gate_ppc.sh` | +39 (the `#571` block after `#565`'s, before the NetBSD `need_file`) |
  | `tools/pipeline/check_probe_wiring.py` | +2 MANIFEST keys (staged copy from the HEAD blob at `staged/check_probe_wiring.py.txt`) |
  | `tools/precommit_check.sh` | +3 / -1 (the coverage pin and its history line) |
  | `regress/artifacts/ppcdsformxo/` | witness_20261024/ (+ receipts/), pass1_20261024/ (+ adj/), table1_20261024/, pass2_20261024/ |

  ## 3. N = 39, the rows
  `DETECTOR_FREEZE.txt` lists them in emission order; CONTROL 22, SYMPTOM 17.  Sessions: loads (14 rows), stores (12),
  five stop sessions (2 each), global 3 (`unasm census` 108/108, `word pins`, `neg apparatus`).

  ## 4. Every score, with its instrument and denominator (instrument = the frozen detector unless named)
  | run | artifact | score |
  |---|---|---|
  | pre-fix, BASE binary | `prefix_BASE.out` | 22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17 |
  | post-fix, work binary | `fixed.out` | 39/39, ABSENT, RED=none |
  | post-fix, the frozen 8-row witness | `fixed_witness8.out` | 8/8, ABSENT |
  | L3 both cases reinstated | `L3_armHEAD.out` | 22/39 (predicted 22/39) |
  | L4b / L4c one case reinstated | `L4b_case58HEAD.out` / `L4c_case62HEAD.out` | 31/39 / 30/39 (as predicted) |
  | L5 identity body | `L5_identity.out` | 17/39, CONTROL=FAIL (as predicted) -- `(c): measured at L5_identity.out` |
  | L5b absent binary | `L5b_absent.out` | no sentinel (FileNotFoundError), as predicted |
  | L6a / L6b update dropped | `L6a_noupd58.out` / `L6b_noupd62.out` | 37/39 / 36/39 (as predicted) |
  | L7 raw imm | `L7_rawimm.out` | 27/39 (as predicted) |
  | L8a / L8b / L8c lwa variants | `L8a_lwaxo0flags.out` / `L8b_lwazero1.out` / `L8c_lwasize3zero0.out` | 36/39 / 36/39 / 25/39 with the emulator exit on the loads session and the sentinel present (as predicted) |
  | L9a XO 0 as XO 1 | `L9a_xo0asxo1.out` | 33/39 (predicted 35/39: the two liveness rows also red -- the RA = 0 words refuse and stop their sessions) |
  | L9b EA + 1 on XO 0 | `L9b_xo0plus1.out` | 33/39 (as predicted) |
  | L10 update everywhere | `L10_updall.out` | 31/39 (predicted 33/39: the same two liveness rows) |
  | L11 shared-assignment mask | `L11_sharedmask.out` | 37/39 (as predicted) |
  | L12a / L12b reserved tests opened | `L12a_xo623open.out` / `L12b_xo583open.out` | 38/39 / 38/39 (as predicted) |
  Every leg red; no leg red for a reason other than the one under test (`SCORES.txt` names the reason per leg).

  ## 5. Two-part clearance (`CLEARANCE.out`, 09:03)
  build/: part 1 CLEAN, part 2 FRESH (gxemul a142d92a).  build-asan/: CLEAN, FRESH (79d75442).  /tmp/gxsec-build: CLEAN,
  FRESH (14ede3bd).  est/: source tree, part 2 N/A (md5 2015e243 = SEC).  The peer's five dirty files in build/ untouched.

  ## 6. Gate 13 alone
  `gate13_20261024.out` (09:03:54-09:1x, binary build/gxemul md5 a142d92a, `bash run.sh 13`): **PASS (193 checks),
  REGRESS_PASS, RUN_RC=0.**  The `#571` block: all 53 checks ok (completed; sentinel last; the four keys counted once each
  in any form and once in the accepted form; 39 rows by name; census 108/108; rows run / green / red 39 / 39 / 0).  The
  siblings unchanged: rlwimi 28/28, rldimi 29/29, `ppc_rldicl` 24/24 with its single SCORE line, and the image-gated
  rounding probe ran ("every rounding-mode write took" 0 misses).  The gate's detector log is preserved as
  `gate13_ppc_dsform.log` beside this report (the $LOGDIR copy, `/tmp/gxregress/ppc_dsform.log`).

  ## 7. Where this build disagreed with the spec or a ruling (by id)
  * BUILD_SPEC 10 item 2 said the five legal-access rows "gain nothing red": `lwa ra0 value` is opcode 58 with XO 2, so it is
    a SYMPTOM row (S3's correction; measured red on BASE).  SYMPTOM = 17 rows, not 18 (10b cut two stop sessions) and not 16.
  * PREDICTIONS L9a and L10 missed the session-liveness consequence of an RA = 0 word turning into a refusal (2 rows each);
    the detector is redder than predicted, for the reason under test.  Recorded in `SCORES.txt`.
  * The builder role was not held by one agent (two harness stops before any write); the measurements were run by the
    main loop from frozen scripts -- the receipts (`s5_fix_build.out`, `s6_all.out`, `CLEARANCE.out`) carry the commands.

  ## 8. Open items (for pass 2 and the main loop)
  * The one ask-again goes to pass 2's panel (the table is clean).
  * Landing: the ledger row (witness term scoped to the loads; `prefix_BASE.out` named for the store half; commits), the
    CHANGELOG round block (draft in scratchpad `t2/landing/changelog_571.draft.md`, `<<FILL>>` marks to clear), the four
    filings (C1-C4), OUTSTANDING_BUGS.md's dated section, the pass-2 receipt in `regress/pass2_ledger.tsv`, the MANIFEST
    keys landing with the files they name (the witness directory committed in the same unit).
~~~~

---

## 10. The project rules the questions apply -- quoted with their bounds

**Provenance:** the working-tree carrier `GXEMUL-SEC/tools/CLAUDE.md`, byte-identical to the root `CLAUDE.md` (4104 lines,
md5 `fbc0f91a`); line numbers are that file's.  Each rule travels WITH its bound: a rule quoted without its bound is a
different rule.

**R1 -- THE FLOOR** (:1328-1333):
~~~~
1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
1332| > round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
1333| > stopping rule already fixes in-round.
~~~~

**R2 -- clause (c): the null medium by instrument kind, the pre-fix build, the two record forms** (:1340-1367):
~~~~
1340| > **ONE criterion -- a product medium carrying none of the behaviour under test -- and its object
1341| > differs by instrument kind:**
1342| > * an offline differential that `#include`s the product: a COMMENT-ONLY product source, which must
1343| >   fail to COMPILE, with a gate that reds on the compile failure (measured for `#488`:
1344| >   `regress/artifacts/shortread/nullmedium_20261009/RECEIPT.txt`);
1345| > * a runtime probe: an ABSENT or NON-EMULATOR binary (every session dies), or a build WITHOUT the
1346| >   device for a device round;
1347| > * an instruction-handler round: an IDENTITY BODY (decode and retire, write nothing) -- the
1348| >   recommended default, two measured legs at `#527`.
1349| >
1350| > **THE PRE-FIX BUILD IS CLAUSE (a)'S MEDIUM AND NEVER CLAUSE (c)'S.**  It carries every behaviour of the
1351| > product, one of them wrong, so a detector can red on it and still pass a comment-only file -- `#446`,
1352| > the instance that created this clause.  A table that wrote "null medium" over a pre-fix leg carries a
1353| > WRONG RECORD (L4: correct it in place, quoting what it refutes, as
1354| > `ppcrldimimask/killtable_20260911/SCORES.txt` does), NOT a floor breach: clause (c) is then
1355| > UNMEASURED there.  **A breach is a genuine null medium coming back GREEN, and nothing else** -- "a
1356| > sharper medium was available" is not a floor criterion (at most clause-(e) debt).
1357| >
1358| > **RECORD CLAUSE (c) IN ONE OF EXACTLY TWO FORMS, never as a bare clause letter beside a row name:**
1359| > * `(c): measured at <artifact>` -- the leg was run and its receipt is durable;
1360| > * `(c): by construction via <row/pin>, leg not run` -- e.g. the gate pins the row count by EQUALITY
1361| >   and a named row reds on a dead run, or the differential `#include`s the product and its gate reds
1362| >   on a compile failure.  **A by-construction claim is checked by READING that shape; where the reading
1363| >   fails -- no runtime gate wiring, no pin, `check_min`, a control computed over the row list
1364| >   (`all([])` is True) -- the leg is OWED** (7n-1's two: the unwired `ppc_rldicl_probe.py` and
1365| >   `alpha_tbi_probe.py`).  Predict a dead run's score from the source, not from the row count (Astra
1366| >   measured luna's at 0/14 with four gate checks red, and SGI's at 6/46 because six rows test only
1367| >   exit status).
~~~~

**R3 -- clause (d)** (:1376-1377):
~~~~
1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
1377| > the guard kept, its effect removed.**
~~~~

**R5 -- the DEPENDS-ON bound** (:1448-1451):
~~~~
1448| > > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
1449| > > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
1450| > > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
1451| > > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
~~~~

**R7 -- the floor (cells a row is OWED for) versus clause-(e) disclosure** (:1517-1522):
~~~~
1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
1520| > > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
1521| > > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
1522| > > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~

**R7b -- a derived input is graded by what the body tests on it; EXHAUSTED / SAMPLED** (:1618-1630):
~~~~
1618| > A local computed from the function's inputs and feeding a body-read operand gets the partition the
1619| > body induces on IT: `#519`'s `tile_nr` -- tested `>= 256` on the tiled branch and `>= 32` on the
1620| > LIN_A branch, never for zero -- is clause (e), not floor, and so is its tile-index escape family.
1621| > Data flow alone is the transitive chasing the DEPENDS-ON bound forbids; a dispatch LABEL is a floor
1622| > axis only by the label clauses above.  **"Closable by a finite row set" is NOT the discriminator**: it
1623| > is the 09-04 finiteness bound under a new name, and every single slice is one-row closable while the
1624| > family never is -- so it separated nothing, and one species was graded two ways by it.
1625| >
1626| > **EXHAUSTED / SAMPLED is adopted as clause-(e) disclosure vocabulary**: EXHAUSTED = every cell of the
1627| > BODY-TESTED partition of that lvalue is rowed (never "every value in the domain"); SAMPLED = driven at
1628| > two or more values, with the untested slices and their derived or measured sweeps named.  A
1629| > disclosure vocabulary can never demand a row.  Its landing spot is the PRE-TABLE CHECK's GUARD FIELD
1630| > vs BODY FIELD row below, which now also records the partition the body induces on each lvalue.
~~~~

**R9 -- GUARD FIELD vs BODY FIELD, and the CHANNEL line** (:1740-1741):
~~~~
1740| > | **GUARD FIELD vs BODY FIELD** | list fields the PREDICATE reads and fields the guarded BODY reads; where they differ, grep whether they are written at the same sites. If not, the detector owes a state where they DISAGREE.  **Also record, per lvalue, the PARTITION THE BODY INDUCES on it** (its tested masks and compare regions) -- EXHAUSTED / SAMPLED is read off this column, never asserted (7n-5, 2026-10-09) | the guard's operand swapped for a field whose third state no row built |
1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~

**R10 -- clause (e): the contract** (:1801-1805):
~~~~
1801| > **(e) THE CONTRACT.** The probe header names which edits this detector is designed
1802| > to catch. *A detector that says so is falsifiable; one claiming completeness is
1803| > not* -- and a later escape becomes "outside the contract" or "a breach of it",
1804| > which are different dispositions, rather than an argument about overclaiming.
1805| > Two lines in a header.
~~~~

**R15 -- the ask-again cap, and what it counts** (:2471-2475, :2481-2483):
~~~~
2471| > **CAPPED AT ONE ASK-AGAIN PER DETECTOR PER ROUND.** This is not the #392 chain — #392 was
2472| > unbounded fix-of-fix passes with no stop condition; this is a single extra adversarial query
2473| > against a clean table with a measured stop: nothing found, done; something found, row added
2474| > under L1, done. **The cap IS the anti-#392 clause.** A second ask-again after an empty first
2475| > is exactly where the chain starts, and anything found past the cap is FILED, never fixed.
  ...
2481| > > Everything ONE ask returns is disposed of INDIVIDUALLY under L1–L4 and the floor — and **a
2482| > > floor breach among the findings is L2, repaired in-round however late it is found.** A
2483| > > second ASK is where the #392 chain starts; the number of rows one ask yields is not.
~~~~

**R-L -- the four reasons that license an in-round fix of detector material** (:2606-2618), **and the stopping rule** (:2645-2646):
~~~~
2606| > ### THE FOUR REASONS THAT LICENSE AN IN-ROUND FIX OF DETECTOR MATERIAL
2607| >
2608| > Everything else is FILED. Named so no round has to re-argue it:
2609| >
2610| > * **L1 — pre-ship construction.** The row is part of the deliverable still being built. A row
2611| >   measured vacuous before commit is unfinished, not a reopening. **The stopping rule governs
2612| >   findings against SHIPPED material only.**
2613| > * **L2 — floor breach.** The shipped detector fails vacuity-floor clause (a), (b) or (c) —
2614| >   replace in-round however late it is found.
2615| > * **L3 — undischarged obligation.** The row is the sole carrier of something the round OWES
2616| >   (a de-escalation accept row; the "shipped a detector" claim itself). A vacuous sole carrier
2617| >   makes the round's record false.
2618| > * **L4 — wrong record.** Prose or comments claiming coverage a measurement refutes.
  ...
2645| > A review finding gets FIXED IN THIS ROUND only if it is a MEASURED FALSE PASS or a WRONG
2646| > RECORD. Everything else gets FILED.
~~~~

**R-STOP -- a pass closes the chain only if it is VALID, and the floor question is asked of the shipped composite** (:2659-2661, :2670-2674, :2686-2688):
~~~~
2659| > **THE STOP CONDITION: one pass per floor-bound diff, closing on the FIRST PASS THAT FINDS
2660| > ZERO BREACHES** -- subject to the two corrections below, without which it closes early on a
2661| > live escape.
  ...
2670| > > **A closing pass must be a VALID pass: the diff actually delivered; the roster complete or
2671| > > its misses named per the seat ledger; and the zero carried WITH ITS DENOMINATOR -- which
2672| > > cells, which mutant shapes, were swept.** *"Zero found"* and *"zero looked for"* must not
2673| > > render the same, which is this project's oldest rule about blanks turned on its own stop
2674| > > condition.
  ...
2686| > > **Review EFFORT is scoped to the repair diff, so settled design is not re-litigated. The
2687| > > FLOOR QUESTION -- does a clean-sweep mutant exist in the (d) enumeration -- is asked of the
2688| > > SHIPPED COMPOSITE on every pass.**
~~~~

**R-SCORE -- a preserved log is verified by its sentinel; a score claim names its artifact** (:3507-3509, :3707):
~~~~
3507| > > **THE RULE, and it costs one line: A PRESERVED LOG IS VERIFIED BY ITS COMPLETION SENTINEL,
3508| > > NOT BY ITS EXISTENCE.** Every probe in this tree emits one (`TPROBE2_DONE`, `TARGETED_DONE`,
3509| > > `FREEZE_DONE`, `REGRESS_PASS`). `tail -1` before citing, and re-copy if it is absent.
  ...
3707| > **THE RULE: a score claim names its artifact — `8/32 pre-fix (kill461e.out)`.**
~~~~

*Not binding here, said so that nobody spends an answer on it: the de-escalation clause and accept-row failability bind a
diff that DELETES an `exit(` -- this diff deletes none; rule D2 (a relational compare pinned at its edges) is N/A (B13).*

---

## 11. QUESTIONS

Answer all four.  VERDICT LINE FIRST, in this vocabulary (this pass reviews material that is built and measured but not
yet committed):

~~~~
VERDICT: READY TO LAND | LAND WITH CHANGES | DO NOT LAND -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~

Then one section per question.  Mark each claim READ (you opened the file), DERIVED (from this packet) or NOT CHECKABLE.
For every finding, name its licence (R-L: L1-L4 = fix in this round; otherwise FILE) and the ids it rests on (S/M, the
A-F rulings, K checks, R rules).  Describe any construction in WORDS ONLY -- no code, no diff, no guest program.

**Q1 -- THE DIFF (section 1).**
(a) Is the repair exactly A1-A4 as amended: the mask inside BOTH case bodies (A9/B9 amended -- no shared mask line),
dispatch on `iword & 3`, the flags per form, `goto bad` for 58/XO 3 and 62/XO 2-3, and NOTHING ELSE moved (the shared
`imm = (int16_t)iword;`, the other 22 case bodies, the common part after the inner switch)?  ENUMERATE the table index (S7)
for the five forms at DS != 0 and at DS = 0 -- ten values -- against A1's slots; does any reach 11/27/43/59?
(b) Does a `goto bad` taken inside the nested `switch (iword & 3)` reach the function's `bad:` (S6) with the same effect as
the arm's other `goto bad` sites -- the `ra == 0 && update` guard, the opcode-31 `default:goto bad;`?  Name every
difference (the guard first prints `fatal("TODO: ra=0 && update?\n")` outside read-ahead), and say whether any state set
before the jump -- `load`, `size`, the re-assigned `imm`, `ic->f = NULL` -- outlives it.
(c) Is every sentence of the two `#571` comments accurate (against the code, section 4's measurements and K7), and is the
comment free of the withdrawn census (A3 as corrected by F1/F2)?
(d) The MODE32 twin (S9, M2): does the record state it as A6 (amended) and A9 require -- the comment's short sentence, the
contract's NOT CLAIMED bullet, the CHANGELOG draft -- and is the comment's short form enough beside the contract's long one?
(e) Anything the diff should carry and does not?  The `#571` tag count is 2 (one per case-body comment); A9 asked for a tag
"at each edited line (the mask line and the two case lines)" before F1 moved the mask into the case bodies.  Is two right?

**Q2 -- THE DETECTOR AND THE TABLE (sections 2 and 4).**
(a) Do the 39 rows discharge the floor as pass 1 enumerated it (B1-B13 as amended, F1, F2)?  Map every enumerated cell to
its row or to a NOT CLAIMED bullet of the contract; name any cell with neither.
(b) Compare every leg's measured red list with PREDICTIONS.txt.  Are the two misses -- L9a and L10, the liveness rows `live`
and `st live` -- correctly explained (under those legs the RA = 0 XO-0 words become refusals and stop their sessions
before the `li`; the OBS session lines show where each session stopped)?  Is any leg red for a reason OTHER than the one
under test?  Is L8c scored as B10 (amended) requires?
(c) Is any row VACUOUS -- its named channel cannot vary under its named leg (R9)?  Weigh the apparatus rows (the five
stop-session `live` rows, `unasm census`, `word pins`, `neg apparatus`), the control no leg reds (`lwz value`), and K6.  Is
each apparatus row labelled as apparatus?
(d) Clause (c): is `(c): measured at L5_identity.out` (the identity body) the right medium and record form (R2)?  K3: is
SCORES.txt's L5b sentence about gate 13 right?
(e) THE ASK-AGAIN -- the one capped ask (R15), after a clean table: can any change confined to the two case bodies leave
all 39 rows green?  Answer in the COVERAGE form, not as a construction.  Enumerate the inputs the case bodies see --
opcode 58/62 x XO 0-3 x DS (= 0 / != 0, and which signs the rows sample) x RA (= 0 / != 0; RA = RT for `ldu`; RA = RS for
`stdu`) x bit 31 of the word `lwa` loads x the CPU width -- and mark each cell OBSERVED (name the row) or UNOBSERVED.  For
each UNOBSERVED cell, state what the shipped decode produces there, which observable would show a different result, and
which NOT CLAIMED bullet of the contract discloses the cell -- or that none does, which makes it a floor question (R7;
licence L2).  Describe cells, not edits.

**Q3 -- THE GATE AND THE RECORDS (sections 3 and 9).**
(a) Gate 13's `#571` block (3.1): are its pins complete for B12 as amended -- each protocol key once in any form, then its
accepted value once; the literal 39 in `RESULT=39/39`, rows run and rows green; red 0; the census at 108/108; the sentinel
once and last; all 39 names by `^name  .*ok$`?  Can the block go green on a run that is not a green detector run?  K1 and
K2 -- right?  Should gate 13's title (still "... + rlwimi/rldimi/rldicl") name the block?
(b) The MANIFEST keys (3.2): classes right?  Both keys report GHOST until the two probe files are staged (the checker's
domain reads `git ls-files`).  The working-tree checker also carries a peer's 15 uncommitted lines: does any record say the
landing must carry the HEAD-based staged copy (HEAD plus the two keys), not the working-tree file?
(c) `SCORE_CLAIMS_MANIFEST` 38 -> 39 with its dated line (3.3): right?
(d) The contract's NOT CLAIMED list (2.1) against A5, A6 (amended), F2's joints, B5, B7, A8 and C5: complete and accurate?
(e) The CHANGELOG round block -- a DRAFT frozen into section 9, `<<FILL>>` marks and all: does every number it states match
the table1 artifact that carries it (section 9's table)?  K5, K8, K9, K10, K11, and K1's last clause -- right?
(f) The ledger witness term (B12): right, and is its scope (the LOADS; `prefix_BASE.out` for the stores) in the draft term?
(g) K4 and K13: wrong records to correct before landing?  Should the frozen drivers sit beside the table?

**Q4 -- THE STANDING LICENCE.**
If, while verifying a claim, you found something ELSE -- say so.  And the four filings (C1 `ppcdisasmxo` LOW, C2
`ppcdisasmfpupd` LOW, C3 `ppcldxabsent` MED, C4 `ppc64on32gate` design): are the ids right (all four unused at HEAD -- C0),
the severities (K12), the witnesses (C1 the frozen census lines; C2 and C3 source-derived, C3's rung-3 shape one stepped
`ldx` word) and the citations (`cpu_ppc.c` :1495-1517 for C1, :1468-1489 for C2)?  Do the drafted filing texts carry F1's
C4 qualifications (K12)?

---

## 12. Paths

**Permitted reading list for file-reading seats -- every path checked by `[ -e ]` at drafting, with HEAD equality
(`LS_PERMITTED.txt`, VERBATIM):**

~~~~
  # permitted-path check, 2026-10-24 09:26:11 -0500 -- [ -e ] on every path the pass-2 brief invites a seat to open (a MISSING line would name it);
  # for each tracked file, '= HEAD' means 'git show HEAD:<path> | cmp -s - <path>' succeeded; 'DIFFERS' marks this round's edit
  # (and, for check_probe_wiring.py, a peer's uncommitted lines too -- read it at HEAD + the staged copy); 'untracked' = new or frozen, not in git
  ok  DIFFERS      152388 b  GXEMUL-SEC/src/cpus/cpu_ppc_instr.c
  ok  = HEAD        58158 b  GXEMUL-SEC/src/cpus/cpu_dyntrans.c
  ok  = HEAD         8881 b  GXEMUL-SEC/src/cpus/cpu_ppc_instr_loadstore.c
  ok  = HEAD         8547 b  GXEMUL-SEC/src/cpus/generate_ppc_loadstore.c
  ok  = HEAD        41157 b  GXEMUL-SEC/src/cpus/tmp_ppc_loadstore.c
  ok  = HEAD         3589 b  GXEMUL-SEC/src/cpus/tmp_ppc_tail.c
  ok  = HEAD        54527 b  GXEMUL-SEC/src/cpus/cpu_ppc.c
  ok  = HEAD         8397 b  GXEMUL-SEC/src/include/opcodes_ppc.h
  ok  = HEAD        14971 b  GXEMUL-SEC/src/machines/machine_test.c
  ok  = HEAD        53550 b  GXEMUL-SEC/src/debugger/debugger_cmds.c
  ok  untracked     40883 b  GXEMUL-SEC/regress/ppc_dsform_probe.py
  ok  DIFFERS       22914 b  GXEMUL-SEC/regress/gate_ppc.sh
  ok  = HEAD        17714 b  GXEMUL-SEC/regress/lib.sh
  ok  = HEAD         6138 b  GXEMUL-SEC/regress/run.sh
  ok  = HEAD        38982 b  GXEMUL-SEC/regress/ppc_rldicl_probe.py
  ok  DIFFERS       80079 b  GXEMUL-SEC/tools/precommit_check.sh
  ok  = HEAD        12618 b  GXEMUL-SEC/tools/pipeline/check_score_claims.py
  ok  DIFFERS      371842 b  GXEMUL-SEC/tools/pipeline/check_probe_wiring.py
  ok  untracked     22953 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py
  ok  untracked      7513 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/WITNESS_REPORT.md
  ok  untracked      3829 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/WITNESS_headbin.out
  ok  untracked       324 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/MANIFEST.md5
  ok  untracked       345 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/receipts/MANIFEST.md5
  ok  untracked      3058 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024/receipts/build_base.out
  ok  untracked     34155 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/pass1_20261024/PASS1_RULINGS.md
  ok  untracked     26859 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/pass1_20261024/BUILD_SPEC.md
  ok  untracked      8055 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/BUILD_REPORT.md
  ok  untracked      1639 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/BASELINE.out
  ok  untracked     12615 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/PRETABLE.out
  ok  untracked      5899 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/DETECTOR_FREEZE.txt
  ok  untracked      4075 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/PREDICTIONS.txt
  ok  untracked      6102 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/SCORES.txt
  ok  untracked      1823 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/run_prefix_base.out
  ok  untracked     14196 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/prefix_BASE.out
  ok  untracked      2295 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/s5_fix_build.out
  ok  untracked     13899 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/fixed.out
  ok  untracked      3795 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/fixed_witness8.out
  ok  untracked     14190 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L3_armHEAD.out
  ok  untracked     14076 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L4b_case58HEAD.out
  ok  untracked     14137 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L4c_case62HEAD.out
  ok  untracked     14394 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L5_identity.out
  ok  untracked      2668 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L5b_absent.out
  ok  untracked     13985 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L6a_noupd58.out
  ok  untracked     14011 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L6b_noupd62.out
  ok  untracked     14116 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L7_rawimm.out
  ok  untracked     14019 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L8a_lwaxo0flags.out
  ok  untracked     13989 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L8b_lwazero1.out
  ok  untracked     13891 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L8c_lwasize3zero0.out
  ok  untracked     14066 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L9a_xo0asxo1.out
  ok  untracked     14057 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L9b_xo0plus1.out
  ok  untracked     14085 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L10_updall.out
  ok  untracked     14012 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L11_sharedmask.out
  ok  untracked     14009 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L12a_xo623open.out
  ok  untracked     14004 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/L12b_xo583open.out
  ok  untracked     16528 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/s6_all.out
  ok  untracked      1880 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/CLEARANCE.out
  ok  untracked     30946 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/gate13_20261024.out
  ok  untracked     13933 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/gate13_ppc_dsform.log
  ok  untracked      9265 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/staged/INSERTIONS.txt
  ok  untracked     22914 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/staged/gate_ppc.sh.txt
  ok  untracked    370614 b  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/staged/check_probe_wiring.py.txt
  ok  outside      783679 b  _scratchpad/ppc_uisa_book1_v201.txt
  ok  outside     1451137 b  _scratchpad/ppc_pem_32and64_2005.txt
  # GXEMUL-SEC/tools/pipeline/check_probe_wiring.py DIFFERS twice over (this round's 2 MANIFEST keys + a peer's 15 uncommitted lines):
  #   read it as  git -C GXEMUL-SEC show HEAD:tools/pipeline/check_probe_wiring.py  plus  GXEMUL-SEC/regress/artifacts/ppcdsformxo/table1_20261024/staged/check_probe_wiring.py.txt
  # the two _scratchpad manuals are outside the repository; cite them by ABSOLUTE path: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\<name>
  # NOT permitted (out of this review's scope): GXEMUL-SEC/regress/artifacts/ppcdsformxo/pass2_20261024/ (other seats' answers land there), the pass-1 seat answer files and packets
  #   in pass1_20261024/ (everything there except PASS1_RULINGS.md and BUILD_SPEC.md), table1_20261024/L*.diff and RAW_*.txt, tools/pipeline/ledger.json
  LS_DONE
~~~~

The pass-2 answers land in `GXEMUL-SEC/regress/artifacts/ppcdsformxo/pass2_20261024/` -- do not open it.  This brief's own
inputs (the three `.patch` files, `C0_OUTPUT.txt`, `LS_PERMITTED.txt`) are inlined above in full.
