# PASS-2 DIFF REVIEW -- round #571, ledger row `ppcdsformxo` (research item T2) -- GXemul hardened fork

**Brief v1, PACKET-FED form -- for the seats that cannot read files (GLM 5.3, DeepSeek).  It stands alone.  The FULL form
is the AUTHORITY; sections 6, 7 and 11 here are byte-identical to it, and every other section is cut or condensed and says
so.**  Drafted 2026-10-24 09:47 -0500.  Tree under review: `GXEMUL-SEC/` at HEAD `add098b9` plus this round's uncommitted edits.

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

**This is the packet-fed form; the FULL form is the authority.**  You cannot read files, and that is expected: every fact a
question depends on is inlined below.  Where you need a fact this packet does not carry, write NOT CHECKABLE rather than
guessing.

**The project.**  GXemul is a computer-architecture emulator; this fork does ordinary software-correctness work on its C code
and keeps each correction fixed with regression tests.  *Guest* = the program inside the emulator; *host* = the emulator
process; a *leg* = a deliberately altered copy of the code, built only to measure whether a test notices (mutation testing).
Quoted records say a row "kills" a leg when it turns red under it (detects it); the "kill table" is the table of legs.

**The defect and the fix.**  On the 64-bit PowerPC CPU this tree models (PPC970) the decoder treated primary opcode 58 as
ONE instruction (`ld`, 8-byte load) and 62 as ONE instruction (`std`), taking the displacement from the word's whole low
halfword.  These are DS-form opcodes: the two lowest bits are an extended opcode (XO) selecting `ld`/`ldu`/`lwa` (58) or
`std`/`stdu` (62), and the displacement is DS || 0b00.  So `ldu` loaded from EA+1 and left RA alone, `lwa` loaded a
doubleword from EA+2, `stdu` stored at EA+1 and left RA alone, and the reserved encodings executed -- all MEASURED red on
the committed decode (section 4).  The fix re-decodes the two case bodies (section 1); it ends no emulator process.

**This pass.**  PASS 2 reviews the SHIPPED material -- the product diff, the detector, the table of variant legs, the gate block, the
records -- against pass 1's rulings.  Everything is built and MEASURED (section 4); nothing is committed (section 5).
Section 6 re-inlines the settled rulings; section 7 lists discrepancies the drafter found, AS QUESTIONS; section 11 asks
Q1-Q4.  READ-ONLY review: nobody is asked for code, a diff, a variant or a guest program.

**Roster:** GPT-6 Astra and Grok 4.7 (FULL form) and Gemini 4 Argon (COMPACT form) read files; GLM 5.3 and DeepSeek (this
form, two firings: Q1+Q2, then Q3+Q4) do not.  Fable 5.1 HELD; kimi, minimax and Opus-as-seat NOT FIRED (Opus 5.5 wrote the
detector and drafted this brief).  **The answer format is at the head of section 11.**

---

## 1. The product change -- `src/cpus/cpu_ppc_instr.c`, the only product file (+31 -2; GNU `diff` against the HEAD blob)

### 1.1 The diff, VERBATIM

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

### 1.2 The arm AFTER the edit -- :4293-4381 (working tree), VERBATIM.  CUT: :4269-4292 are the arm's 24 `case` labels -- LBZ, LBZU, LHZ, LHZU, LHA, LHAU, LWZ, LWZU, LD, LFD, LFDU, LFS, LFSU, STB, STBU, STH, STHU, STW, STWU, STD, STFD, STFDU, STFS, STFSU -- falling into :4293.

~~~~
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

A `break` falls into the function's tail (`cpu_dyntrans.c`, #included at the end of `X(to_be_translated)`): the
instruction is marked translated and executed.  A `goto bad` -- the arm's guard, the new `default:` arms, and every other
`goto bad` in the function -- lands at that tail's `bad:`, `src/cpus/cpu_dyntrans.c` :1983-2014, VERBATIM:

~~~~
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
~~~~

The table slots and the `X(invalid)` handler are S7 and A1.

---

## 2. The detector -- `regress/ppc_dsform_probe.py` (NEW; 40,883 bytes, 836 lines by `wc -l`, md5 `0266228894811ba6c51cff82585753c9`)

### 2.1 The docstring's SESSIONS (stop sessions, negative control, global rows) and CONTRACT -- :25-26, :36-86, VERBATIM (CUT: usage and architecture :1-24 and the loads/stores session text :27-35, which 2.3's table carries; FULL 2.1)

~~~~
25| SESSIONS -- eight; each guest session has its own liveness row (li r9,0x1234, the last word
26| before any stop word):
...
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
~~~~

### 2.2 The row tables -- ROW_NAMES, CONTROL, SYMPTOM and their asserts, :127-156, and `row()`, :161-169, VERBATIM

~~~~
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
...
161| def row(name, got, want, note=""):
162|     assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
163|     #  14, not 15: gate 13 pins each row as `^name  ' (two spaces) inside this %-16s column.
164|     assert len(name) <= 14, name
165|     ok = (got == want)
166|     rows.append((name, ok))
167|     print("%-16s %-20s %-20s %-52s %s" % (name, str(got), str(want), note,
168|                                           "ok" if ok else "FAIL"))
169|     return ok
~~~~

### 2.3 The session programs -- every DS-form and D-form word placed, CONDENSED into a table read from the probe's own program objects (the code is :334-402, VERBATIM in the FULL form)

`arch EA` = Book I's address; the last column = what the committed decode used (RA + the raw low halfword).  Seeded bytes:
0x20000+k = k, 0x7000+k = 0x80+2k (loads); 0x21000+k = k, 0x70f0+k = 0x10+k (stores); 0x0+k = 0x60+k (the RA = 0 stops).
Store sources are eight distinct bytes absent from the pattern (r4 = 0xc0c1c2c3c4c5c6c7, ...).

~~~~
tag         word     op/XO  RT/S  RA = base     disp     arch EA  RA + raw low halfword (the committed decode)
-- session loads (27 words: setup, these, then li r9,0x1234 LAST)
ld          e894ff90 58/0   4     r20=0x20080   -0x70    0x20010  0x20010
ldu         e8b5ffa1 58/1   5     r21=0x20080   -0x60    0x20020  0x20021
lwa         e8d6000a 58/2   6     r22=0x20080   +0x8     0x20088  0x2008a
lwz         80f70008 32 D   7     r23=0x20080   +0x8     0x20088  0x20088
ld ds0      e97a0000 58/0   11    r26=0x20040   0        0x20040  0x20040
ldu ds0     e9180001 58/1   8     r24=0x20030   0        0x20030  0x20031
lwa ds0     e9590002 58/2   10    r25=0x20090   0        0x20090  0x20092
lwz odd     81db0006 32 D   14    r27=0x20000   +0x6     0x20006  0x20006
lwa ra0     e9a07006 58/2   13    0             +0x7004  0x7004   0x7006
ld ra0      e9807000 58/0   12    0             +0x7000  0x7000   0x7000
-- session stores (50 words: setup, these, then li r9,0x1234 LAST)
std         f894ffd0 62/0   4     r20=0x21040   -0x30    0x21010  0x21010
std ds0     f9190000 62/0   8     r25=0x210b0   0        0x210b0  0x210b0
stdu        f8b5ffd1 62/1   5     r21=0x21060   -0x30    0x21030  0x21031
stdu ds0    f8d60001 62/1   6     r22=0x21050   0        0x21050  0x21051
stdu alias  faf7fff1 62/1   23    r23=0x21080   -0x10    0x21070  0x21071
stw odd     90f80006 36 D   7     r24=0x2108a   +0x6     0x21090  0x21090
std ra0     f9407100 62/0   10    0             +0x7100  0x7100   0x7100
-- session xo58_3 (4 words: setup, li r9,0x1234, then this stop word LAST)
xo58_3      e894fff3 58/3   4     r20=0x20020   -0x10    illegal  0x20013
-- session xo62_2 (9 words: setup, li r9,0x1234, then this stop word LAST)
xo62_2      f894ffd2 62/2   4     r20=0x21040   -0x30    illegal  0x21012
-- session xo62_3 (9 words: setup, li r9,0x1234, then this stop word LAST)
xo62_3      f894ffd3 62/3   4     r20=0x21040   -0x30    illegal  0x21013
-- session ldu ra0 (2 words: setup, li r9,0x1234, then this stop word LAST)
ldu ra0     e8800011 58/1   4     0             +0x10    invalid  0x11
-- session stdu ra0 (7 words: setup, li r9,0x1234, then this stop word LAST)
stdu ra0    f8800011 62/1   4     0             +0x10    invalid  0x11
~~~~

---

## 3. The gate block, the MANIFEST keys, the coverage pin

### 3.1 `regress/gate_ppc.sh` (gate 13) -- the diff, VERBATIM

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

Earlier in the same gate (`gate_ppc.sh` :103): `need_exec "$PMAX"`, which is (`regress/lib.sh` :153-157)
`[ -x "$f" ] || gate_skip "missing or non-executable binary: $f"` -- an absent binary SKIPs the whole gate (K3).  `count`
(`lib.sh` :326-331) is `grep -ac -- "$2" "$1"` (0 for a missing file).

### 3.2 The MANIFEST keys -- the insertion into the HEAD-blob copy of `tools/pipeline/check_probe_wiring.py` (`staged/INSERTIONS.txt` :72-75), VERBATIM

~~~~
-- diff HEAD-blob staged/check_probe_wiring.py.txt (after):
3221a3222,3223
>     "ppc_dsform_probe.py": (CLASS_DETECTOR, "#571 ppcdsformxo: the 64-bit DS-form loads and stores (opcodes 58 and 62: ld, ldu, lwa, std, stdu, the reserved XO encodings, and ldu/stdu with RA = 0) -- 39 rows on unmodified -E bareppc -M 64; gated in gate_ppc.sh (gate 13) under the stem ppc_dsform, pinned at 39; kill table artifacts/ppcdsformxo/table1_20261024/ (SCORES.txt)"),
>     "artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py": (CLASS_WITNESS, "#571 ppcdsformxo: the rung-3 pre-fix witness of the LOADS (8 rows, md5 5e96b69d) -- 5/8 on HEAD (witness_20261024/WITNESS_headbin.out); its post-fix run is table1_20261024/fixed_witness8.out, and the stores' pre-fix artifact is table1_20261024/prefix_BASE.out"),
~~~~

The same two lines go into the working-tree file, whose 15 OTHER uncommitted lines are a peer's.  `check_probe_wiring.py`
reports both keys GHOST until the two probe files are staged (its domain reads `git ls-files`); `check_score_claims.py`:
`SCORE_CLAIMS_PASS, SCORE_CLAIMS_PINNED=39 (was 38)` (`INSERTIONS.txt` section 4).

### 3.3 `tools/precommit_check.sh` -- the diff, VERBATIM

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

## 4. The measurements (`regress/artifacts/ppcdsformxo/table1_20261024/`)

**Order (mtimes):** `PRETABLE.out` 07:56:54 -> the detector 08:26:52 -> its freeze 08:27:36 / 08:29:04 -> `prefix_BASE.out`
08:29:05 -> the fix built and measured 08:30:55-08:32:06 -> `PREDICTIONS.txt` 08:32:01 -> sixteen legs and L5b
08:34:28-08:54:13 -> `SCORES.txt` 08:55:33 -> clearance 09:03:35 -> gate 13 09:03:54-09:05:23.

### 4.1 Pre-fix -- `prefix_BASE.out`, the BASE binary (built from HEAD's `src/`): the 39 rows, CONDENSED to name / got / want / status (the FULL form carries each line VERBATIM with its note), then the summary lines VERBATIM

The STORE half's clause-(a) artifact (B1).  Post-fix (`fixed.out`): `PPC_DSFORM_RESULT=39/39`, `CONTROL=OK`,
`SYMPTOM=ABSENT`, `RED=none`; the frozen 8-row witness on the fixed binary: 8/8, ABSENT.

~~~~
row             got                  want                 
ld value        0x1011121314151617   0x1011121314151617   ok
ld RA after     0x20080              0x20080              ok
ld ds0 value    0x4041424344454647   0x4041424344454647   ok
ld ra0 value    0x80828486888a8c8e   0x80828486888a8c8e   ok
ldu value       0x2122232425262728   0x2021222324252627   FAIL
ldu RA after    0x20080              0x20020              FAIL
ldu ds0 value   0x3132333435363738   0x3031323334353637   FAIL
lwa value       0x8a8b8c8d8e8f9091   0xffffffff88898a8b   FAIL
lwa RA after    0x20080              0x20080              ok
lwa ds0 value   0x9293949596979899   0xffffffff90919293   FAIL
lwa ra0 value   0x8c8e90929496989a   0xffffffff888a8c8e   FAIL
lwz value       0x88898a8b           0x88898a8b           ok
lwz odd         0x6070809            0x6070809            ok
live            0x1234               0x1234               ok
std value       0xc0c1c2c3c4c5c6c7   0xc0c1c2c3c4c5c6c7   ok
std RA after    0x21040              0x21040              ok
std ds0 value   0xe0e1e2e3e4e5e6e7   0xe0e1e2e3e4e5e6e7   ok
std ra0 value   0xe8e9eaebecedeeef   0xe8e9eaebecedeeef   ok
stdu value      0x30c8c9cacbcccdce   0xc8c9cacbcccdcecf   FAIL
stdu neigh      0x2f|0xcf393a3b      0x2f|0x38393a3b      FAIL
stdu RA after   0x21060              0x21030              FAIL
stdu ds0 value  0x50d0d1d2d3d4d5d6   0xd0d1d2d3d4d5d6d7   FAIL
stdu alias val  0x7000000000000210   0x0000000000021080   FAIL
stdu alias RA   0x21080              0x21070              FAIL
stw odd         0xdcdddedf           0xdcdddedf           ok
st live         0x1234               0x1234               ok
xo58_3 live     0x1234               0x1234               ok
xo58_3 bad      nostop,rt=0x131415161718191a,ra=kept stop,rt=sent,ra=kept FAIL
xo62_2 live     0x1234               0x1234               ok
xo62_2 bad      nostop,win=changed,ra=kept stop,win=kept,ra=kept FAIL
xo62_3 live     0x1234               0x1234               ok
xo62_3 bad      nostop,win=changed,ra=kept stop,win=kept,ra=kept FAIL
ldu ra0 live    0x1234               0x1234               ok
ldu ra0 bad     nostop,rt=0x7172737475767778,ra=kept stop,rt=sent,ra=kept FAIL
stdu ra0 live   0x1234               0x1234               ok
stdu ra0 bad    nostop,win=changed,ra=kept stop,win=kept,ra=kept FAIL
unasm census    108/108              108/108              ok
word pins       e894ff90,e8b5ffa1,e8d6000a e894ff90,e8b5ffa1,e8d6000a ok
neg apparatus   exit1/-0x1           exit1/-0x1           ok

PPC_DSFORM_RESULT=22/39
PPC_DSFORM_CONTROL=OK
PPC_DSFORM_SYMPTOM=PRESENT 17/17
PPC_DSFORM_RED=ldu value,ldu RA after,ldu ds0 value,lwa value,lwa ds0 value,lwa ra0 value,stdu value,stdu neigh,stdu RA after,stdu ds0 value,stdu alias val,stdu alias RA,xo58_3 bad,xo62_2 bad,xo62_3 bad,ldu ra0 bad,stdu ra0 bad
PPC_DSFORM_PROBE_DONE
~~~~

### 4.2 `SCORES.txt`, VERBATIM (whole; its "predicted" column is PREDICTIONS.txt's, which the FULL form carries VERBATIM)

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

Where the L9a and L10 loads and stores sessions stopped -- their `OBS session` lines, VERBATIM (on the fixed binary they end
at pc 0x1006c and 0x100c8, after their last word, the `li`; every stop session of both legs ends as on the fixed binary):

~~~~
L9a_xo0asxo1.out: OBS session loads    how=exit0 words=27 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10064 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_loads.txt
L9a_xo0asxo1.out: OBS session stores   how=exit0 words=50 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x100c0 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L9a_xo0asxo1_stores.txt
L10_updall.out: OBS session loads    how=exit0 words=27 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x10060 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_loads.txt
L10_updall.out: OBS session stores   how=exit0 words=50 unimplemented=1 todo_ra0=1 internal_error=0 pc=0x100c0 msr=0x0 r30=0x5a5a5a5a5a5a5a5a seeded_readback=same transcript=RAW_L10_updall_stores.txt
~~~~

L3 (both case bodies reinstated verbatim) rebuilt the BASE binary bit for bit (`s6_all.out`: leg binary md5 `3cd0501c...`,
leg source md5 `87a766e0...` = the HEAD blob).

### 4.3 `PRETABLE.out` section 4 -- the CHANNEL per row, written before the detector existed, VERBATIM

~~~~
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
~~~~

### 4.4 Clearance and gate 13 (summary)

`CLEARANCE.out` (re-checked at drafting): `src/cpus/cpu_ppc_instr.c` md5 `2015e243...` in GXEMUL-SEC, est/ and the three
build trees, every build binary FRESH, no `.MUTANT` sentinel.  Gate 13 alone on build/gxemul: `PASS (193 checks)`,
`REGRESS_PASS`, `RUN_RC=0`; the `#571` block's 53 checks all `ok` (completed; sentinel last; the four keys once in any form
and once accepted; 39 rows by name; census 108/108; rows run / green / red 39 / 39 / 0); the siblings unchanged (rlwimi
28/28, rldimi 29/29, rldicl 24/24); the image-gated rounding probe green (138 rows).

---

## 5. C0 -- NOT SHIPPED.  At HEAD no CHANGELOG line, commit message or `pass2_ledger.tsv` line names the row or `#571`; the detector and every `ppcdsformxo` artifact are untracked; the ledger row is `state=open witness=none commits=''`; the four filing ids have zero rows; no commit between `c8fcb5ff` and HEAD touches `src/`.

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

## 8. SOURCE context -- CUT (FULL section 8: the dispatch table, the generic handler, the two decoders, Book I's RTL, the disassembler arm).  S2-S9 and M2 in section 6 carry what the questions take from them.

---

## 9. The records under review -- what the landing will say (DRAFTS; FULL 9.1-9.5 carry them VERBATIM)

### 9.1 The CHANGELOG draft's numbers against the artifacts

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


### 9.2 The ledger witness term -- the draft, VERBATIM

~~~~
probe:regress/artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py -- rung 3 on the UNMODIFIED in-tree bareppc -M 64 (PPC970) through the cold debugger, the LOADS only: RED on HEAD 5/8 with the three symptom rows red for the reason under test (ldu loads EA+1 and leaves RA; lwa loads a doubleword at EA+2) and five controls green (WITNESS_headbin.out); the same frozen script 8/8 SYMPTOM=ABSENT on the fixed binary (table1_20261024/fixed_witness8.out).  The STORE half's clause-(a) artifact is the shipped detector's own pre-fix run, table1_20261024/prefix_BASE.out (22/39, SYMPTOM=PRESENT 17/17: stdu stores at EA+1 with no update; 62/XO 2-3 store instead of stopping).  The shipped detector regress/ppc_dsform_probe.py (39 rows, 8 sessions, gate 13, pinned at 39) is fixed 39/39; floor (b) L3/L4b/L4c, (c) measured L5 17/39 CONTROL=FAIL and L5b no sentinel, (d) L6a-L8c, growth L9a-L12b -- 16 of 16 legs red, 14 at their written prediction (SCORES.txt).  Not covered: ldu with RA = RT, 32-bit CPUs, the DS = 0 x RA = 0 joints, a positive-word lwa, translation on, the indexed forms, the disassembler's text.
~~~~

### 9.3 The four filings as drafted -- the OUTSTANDING_BUGS draft gives `ppcdisasmxo` LOW (cpu_ppc.c :1495-1517; witness: the frozen census lines, e.g. `ld r5,-95(r21)` for `ldu r5,-96(r21)`), `ppcdisasmfpupd` LOW (:1468-1489; source-derived), `ppcldxabsent` MED (no `PPC_31_*` define for `ldx`/`ldux`/`lwax`/`lwaux`; source-derived; rung-3 shape one stepped `ldx` word), `ppc64on32gate` "LOW, open, design" (K12).

---

## 10. The project rules the questions apply (CONDENSED; FULL section 10 quotes each VERBATIM from the carrier with line numbers)

* **R1** -- a detector is VACUOUS (replace it in-round) unless it fails (a) on the pre-fix build, (b) on a VERBATIM
  reinstatement of the removed defect at EVERY fixed site, and (c) on a NULL MEDIUM.
* **R2** -- for an instruction-handler round the null medium is an IDENTITY BODY (decode and retire, write nothing); for a
  runtime probe also an ABSENT binary.  The pre-fix build is clause (a)'s medium, never clause (c)'s.  Record (c) as
  `(c): measured at <artifact>` or `(c): by construction via <row/pin>, leg not run`.
* **R3** -- (d): the detector must also fail when the fix is present but its repair is NULLED.
* **R5** -- DEPENDS ON enumerates the predicates dominating the edited lines (enclosing function only).
* **R7** -- the FLOOR (cells a row is owed for) = the guard's dominating predicates x the state the fix's own repair path
  reads, jointly reachable; joint cells outside it are clause-(e) debt, subject to the one ask-again; a filter may reject a
  cell but may demand a row only for a floor cell.
* **R7b** -- a derived input gets the partition the body induces on IT, never its data flow.  EXHAUSTED = every cell of the
  body-tested partition rowed; SAMPLED = driven at two or more values; disclosure vocabulary never demands a row.
* **R9** -- CHANNEL: for each row, the variant leg it detects and the observable that differs; a row whose channel cannot vary
  under its named leg is VACUOUS BY CONSTRUCTION.
* **R10** -- (e): the probe header names the edits the detector is designed to catch.
* **R15** -- ONE ask-again per detector per round; everything it returns is disposed of under L1-L4 and the floor, and a
  floor breach among its findings is L2, repaired in-round.
* **R-L** -- in-round fixes only for L1 (pre-ship construction), L2 (floor breach), L3 (undischarged obligation), L4 (wrong
  record); everything else is FILED.
* **R-STOP** -- a pass closes the chain only if VALID (the diff delivered, the roster complete or its misses named, the
  zero carried with its denominator); the floor question is asked of the SHIPPED COMPOSITE.
* **R-SCORE** -- a preserved log is verified by its completion sentinel; a score claim names its artifact.

---

**THIS FIRING ANSWERS Q3 AND Q4 ONLY.**  Q1 and Q2 went to a separate firing of this same packet; treat the settled design as given here and do not answer them.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

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

## 12. Paths -- every repository path cited exists (checked by `[ -e ]` at drafting); the FULL form lists them one per line.
