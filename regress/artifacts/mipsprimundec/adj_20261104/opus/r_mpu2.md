# r_mpu2 (agent aae2291178da9d80f).  Final text 2026-11-04T08:35:58.026Z by claude-opus-5-5; banked 2026-11-04 from the subagent transcript (it was summarised in BATCH.md at 02:3x but never saved).

OPUS_SEAT_ALIVE_20261104_MPU
# mipsprimundec -- what is in this directory, and what is MISSING

VERDICT: GO-WITH-CHANGES. The approach is right in both translators: new primary cases that install `X(cpu)` or `X(reserved)`, keep the common tail, and handle PC and EPC correctly. The draft must not land as written:
- four (word, ISA) cells take the wrong exception: LDC2 and SDC2 on ISA I, LWC3 and SWC3 on ISA III;
- one witnessed word, 0x1e off the R5900, still stops the CPU;
- five of the draft's comment claims are false or wrongly attributed;
- an unrelated hunk rides along.

Each correction is settled by a local manual line or by source. The corrected diff owes its own pass 2.

Basis. I read all 33 bundle files; the witness files (WITNESS.md, RUN.log, probe_frozen.py, prefix_build.out and the 22 session transcripts); and `GXEMUL-SEC/src` at HEAD ebe5af82. Running `git log 50f9c601..HEAD` and `de8c7547..HEAD` on cpu_mips_instr.c, cpu_dyntrans.c, cpu_mips.c, opcodes_mips.h, mips_cpu_types.h and cpu_mips_coproc.c returns nothing, so every packet line number and every filed line number is HEAD's, with no drift. [CHECKED]

Manual extract sizes (`wc -c`):

| file | bytes | note |
|---|---:|---|
| mips-iv.txt | 416,407 | |
| mips_r4000.txt | 859,594 | |
| idt_r30xx.txt | 1,071,238 | |
| mips32_volII.txt | 775,072 | Rev 6.04, a Release 6 manual |
| mips64_volII.txt | 500,193 | Rev 2.50 |

I created, edited, built and ran nothing.

## 1. Premises the witness refutes or narrows

| # | Premise (where stated) | What the witness shows | Seats that said so | Seats that said the opposite |
|---|---|---|---|---|
| P1 | "witness: none" (ledger row; bug-review §1) | Superseded. A rung-3 witness on `-E testmips` with R4400 (64-bit translator) and R3000 (MODE32): all 64 witness rows red, CONTROL=OK (prefix_build.out). [CHECKED] | All four seats agreed none existed. GLM (bug review) made a witness a precondition for landing. | none |
| P2 | `bad:` stops the CPU and delivers no exception; this is a CPU-STOP, not a host kill | Confirmed. Every session prints `UNIMPLEMENTED instruction` and `All machines stopped`, then still answers `reg`, `reg ,0` and `quit` (exit0). EPC is 0 and Cause is INT, exccode 0. 0x1e prints `TODO: MDMX` and 0x33 prints `TODO: lwc3 not implemented yet` first (64_mdmx.txt, 64_lwc3.txt). [CHECKED] | Grok and Astra (`fatal()` only prints) | GLM (witness) and Argon (witness adjudication draft) left "fatal() may exit(1)" open; this settles it. |
| P3 | "any privilege, every MIPS machine, including the pmax and arc rigs" | Narrowed. Only testmips was measured, in kernel mode (`status: ... ksu=kernel`); pmax, arc and user mode are listed as owed. On the default testmips CPU (the 5KE, machine_test.c:410-413), 0xcc000000 is PREF and executes (RUN.log 01:14:10, 17/80). [CHECKED] | Astra (0x33 stops at ISA 1/2/3 and is a nop at 4/32/64; user reach needs a real user mapping). Grok ("a user-mode fetch still has to survive the TLB"). | GLM ("every MIPS machine: REASONED") and Argon ("HOLDS"): not wrong, but unmeasured. |
| P4 | "0x1e is R5900-only" (bug-review §4; fix-draft packet) | Refuted. 0x78000000 stops both non-R5900 CPUs (`64 mdmx stop present`, `32 mdmx stop present`). [CHECKED] | GLM, Grok, Astra (every stage); Argon's adjudication draft | only the packets |
| P5 | Fix-draft packet: the outer `default` is kept because the R5900 LQ/SQ and MDMX words still reach it | Refuted. The transcripts show 0x1e and 0x33 stopping through their own arms (their TODO lines print), while the six default words print nothing. No R5900 or MDMX word reaches 5708, and after the draft no word does. [CHECKED] | Grok and Astra (full walk of all 64 values); GLM in part | Argon (left it UNSETTLED) |
| P6 | Argon (fix draft): the PC-sync mask "zero-extends" and corrupts a 64-bit PC | Refuted. The same `X(cpu)` vehicle on the 64-bit translator gave `64 cpu2 epc 0xffffffff80020000`. Source agrees: cpu.h:409 `uint64_t pc;` and cpu_mips.h:191/195 make `~((1024-1)<<2)` the int -4093, which converts to `0xfffffffffffff003`. [CHECKED] | GLM, Grok, Astra | Argon |
| P7 | GLM (bug review): "R3000 Cause has no CE field" | Refuted: `32 cpu2 exc 11/2` (R3000 cause = 0x2000002c). [CHECKED] | Grok, Astra (cpu_mips.c:2049-2051 writes CE for every model) | GLM (bug review) |
| P8 | The fork's ISA gate: "LDC1 below ISA II takes RI" | Measured: `32 ri exc 10/0`. This is exactly the idiom the draft's LDC2/SDC2 arm skips. [CHECKED] | Grok, Astra, GLM (fix draft), Argon (fix draft) all asked for the same gate | GLM's witness table (LDC2/SDC2 → CpU CE=2 on MIPS I); Argon's bug-review sketch (all four → CpU2) |
| P9 | Cold Status has CU2 and CU3 clear, so CpU is the required result in the measured state | Confirmed: status 0x34000000 (R4400) and 0x30000000 (R3000), "cu=3" meaning CU0 and CU1 (cpu_mips_coproc.c:374-380). The control readbacks match Astra's and Grok's predicted arithmetic: RI → 0x28, CpU2 → 0x2000002c, vectors 0xffffffff80000180 and 0x80000080. [CHECKED] | Grok, Astra | none |

What the witness does not settle: which exception each word should take. Its `exc` rows accept ExcCode 10 or 11 and never read CE (`trap()` in probe_frozen.py). [CHECKED] The RI-versus-CpU questions below are therefore settled from the manuals.

## 2. What the architecture requires, per word and ISA level

In-tree CPUs by ISA level (mips_cpu_types.h:68-113):

| ISA level | CPUs | translator |
|---|---|---|
| 1 | R2000, R2000A, R3000, R3000A, TX3920 | 32-bit |
| 2 | R6000, Allegrex | 32-bit |
| 3 | R4000, R4000PC, R4200, R4300, R4100, VR4102, VR4181, VR4121, VR4122, VR4131, R4400, R4600, R4700, R4650, R5900 (:92), TX7901 | 64-bit |
| 4 | R10000, R8000, R12000, R14000, R5000, VR5432, RM5200, RM7000, RM7900, RM9000 | 64-bit |
| 32 | RC32334, 4Kc, 4KEc, 24KEc, BCM4710, BCM4712, AU1000, AU1500, AU1100 | 32-bit |
| 64 | 5Kc, 5KE, SB1, SR7100 | 64-bit |

No CPU is ISA 5 and none is Release 6. ISA 1, 2 and 32 use the 32-bit translator (cpu_mips.c:116-118). [CHECKED]

Required result, with the coprocessor's usable bit clear:

| word | ISA I | ISA II | ISA III | ISA IV | MIPS32/64 (Release 1-2) | draft |
|---|---|---|---|---|---|---|
| 0x1d JALX | RI | RI | RI | RI | RI (extension absent) | RI: right |
| 0x1e | RI | RI | RI (R5900: LQ) | RI | RI (extension absent) | still stops: WRONG |
| 0x32 LWC2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | right |
| 0x33 | LWC3: CpU, CE=3 | LWC3: CpU, CE=3 | RI | PREF | PREF | CpU3 at III: WRONG |
| 0x36 LDC2 | RI | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU2 at I: WRONG |
| 0x3a SWC2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | right |
| 0x3b SWC3 | CpU, CE=3 | CpU, CE=3 | RI | RI | RI | CpU3 at III: WRONG |
| 0x3e SDC2 | RI | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU, CE=2 | CpU2 at I: WRONG |

Evidence for each word, all [CHECKED] unless marked:

- **The meaning of an asterisk.** mips-iv.txt:1447 reads "*(asterisk) This opcode is reserved for future use. An attempt to execute it causes a Reserved Instruction exception." The same key marks coprocessor operations as "pi": "If the processor state does not allow access to the specified coprocessor, the instruction causes a Coprocessor Unusable exception."
  - R4000: mips_r4000.txt:5834 reads "Operation codes marked with an asterisk cause reserved instruction exceptions in all current implementations."
  - MIPS64: mips64_volII.txt:2032 says asterisk means "must cause a Reserved Instruction Exception."
- **JALX and 0x1e on ISA I-IV.**
  - MIPS IV level table, mips-iv.txt:1404: `LDR3*1*1*1*1`, so 0x1c-0x1f are reserved from level 1.
  - R4000 map, mips_r4000.txt:5823: `LDRe****`.
- **JALX on MIPS32/64.**
  - mips32_volII.txt:690: "MIPS32 with (microMIPS or MIPS16e), removed in Release 6".
  - mips32_volII.txt:1782: `JALX6R H`; the H key at :1780 says "If the Module/ASE is not implemented, executing such an instruction must cause a Reserved Instruction exception."
  - MIPS64, mips64_volII.txt:2046: `JALXMDMX` (the symbol glyph is lost in extraction). mips64_volII.txt:41 names MIPS16e and MDMX as extensions; the extension symbol at :2039 means RI when absent. [REASONED for the MIPS64 glyph]
  - No in-tree CPU advertises MIPS16: cpu_mips_coproc.c:61 `const int m16 = 0;	/*  TODO: MIPS16 support  */`, used at :104 (Config1) and :176 (R4100 Config.M16).
- **0x1e on MIPS32/64.** No CPU advertises MDMX: Config1 is built at cpu_mips_coproc.c:94-107 with no MD bit.
- **LWC2 and SWC2.**
  - MIPS I onward: mips-iv.txt:612 and :1153.
  - Restriction text: "If the usable bit is not set, an attempt to execute the instruction will result in a Coprocessor Unusable exception."
  - R30xx: idt_r30xx.txt:17142-17158 and :18349-18366. R4000: mips_r4000.txt:5106 and :5111-5112, :5592 and :5595-5596.
  - The R4000 rule that CpU applies to CP1-3 in every mode is at mips_r4000.txt:1158; the CE field is defined at :1005.
- **LDC2 and SDC2.**
  - "MIPS II" (mips-iv.txt:395, :865). The MIPS I table has rows `*LWC1LWC2LWC3****` and `*SWC1SWC2SWC3****` (:1372). MIPS II adds LDC1-3 and SDC1-3 (Table A-42, :1415).
  - The R30xx manual has no LDCz or SDCz anywhere: grep count 0 over the whole 1,071,238-byte file.
- **LWC3 and SWC3.**
  - The MIPS I and II tables include COP3, LWC3 and SWC3 (:1372, :1380).
  - mips-iv.txt:1369: "Coprocessor 3 is optional and implementation-specific in the MIPS I and MIPS II architecture levels. It was removed from MIPS III and later architecture levels."
  - MIPS III change table (:1426): `*(wasCOP3)`, `*(was LWC3)`, `*(was SWC3)`. MIPS IV adds only COP1X and PREF at the primary level (:1439).
  - R4000 map (:5823): `LWC1LWC2*SWC1SWC2*` and `COP1COP2*`. Its LWCz and SWCz pages encode only coprocessors 1 and 2 (:5111-5112, :5595-5596).
  - MIPS64 row 7 is `SC SWC1 SWC2 * SCD...` (mips64_volII.txt:2048).
- **PREF.** mips-iv.txt:818: "An implementation may do nothing when executing a PREF instruction". The existing nop arm (cpu_mips_instr.c:5554-5556) is legal.

Where each word is a valid instruction:
- PREF at 0x33 on ISA IV, MIPS32 and MIPS64.
- JALX on MIPS32/64 with MIPS16e or microMIPS (none modelled here).
- LQ at 0x1e on the R5900.
- MDMX at 0x1e on MIPS64 with that extension (none modelled).
- LWC3 and SWC3 only on ISA I and II.

What the manuals leave unsettled:
- **(a) Usable bit set, no coprocessor.** On MIPS I-IV the result is undefined (mips-iv.txt:612: "An unimplemented coprocessor must never be enabled. The result ... when the usable bit is set, is undefined"), so raising CpU is an allowed fixed policy. MIPS32/64 require RI (the T symbol, mips32_volII.txt:1780; mips64_volII.txt:2039). CU2 and CU3 are guest-writable: cpu_mips_coproc.c:919 masks only bit 21 and :1017 stores the value. The draft copies this gap into four new arms; it is already filed as `mipscop2retrap`. [CHECKED]
- **(b) COP3 on ISA I depends on the part.** idt_r30xx.txt:18335-18336 says "Execution of the instruction referencing coprocessor 3 causes a reserved instruction exception, not a coprocessor unusable exception" (also :17411), but the same manual's LWCz page lists only CpU (:17142-17162). [UNSETTLED for the generic R2000/R3000 types]
- **(c)** What LWC3/SWC3 should do on a pmax with the R2020/R3220 present and CU3 set. [UNSETTLED; no local manual]
- **(d)** The R5900 cells (0x33 may be PREF, 0x36/0x3e may be LQC2/SQC2), the Allegrex VFPU loads and stores, and VR5432. `ls _scratchpad/*.pdf` shows no manual for any of them. [UNSETTLED]
- **(e)** mips32_volII.txt is Release 6.04. Its note at :1775 says that before Release 6 an empty slot did not necessarily signal RI, so the pre-Release-6 0x3b reading rests on the explicit asterisk in MIPS64 Rev 2.50. [CHECKED]

## 3. The draft against the enclosing function's real control flow

**Both translators.** cpu_mips_instr.c is compiled twice: tmp_mips_tail.c:63 for the 64-bit translator and :118 with MODE32 defined at :83. The draft touches no MODE32-only text, so both copies get identical arms. [CHECKED]

**Paths to `bad:` before the draft:**
- 0x1d, 0x32, 0x36, 0x3a, 0x3b and 0x3e reach `default:goto bad;` at :5708.
- 0x33 below ISA IV reaches :5558-5560.
- 0x1e reaches :5565-5568 on the R5900 and :5571-5574 elsewhere.
- `bad:` resets the translation (`ic->f = TO_BE_TRANSLATED`, cpu_dyntrans.c:1988), returns if this is read-ahead (:1990-1991), prints the message (:2004-2009), sets `cpu->running = 0` (:2014) and switches `next_ic` to the do-nothing entry (:2023).
- At that point the PC still holds the word's address, set at cpu_mips_instr.c:4295 `cpu->pc = (MODE_int_t)addr;`. That is why the witness reads pc = PLANT and EPC = 0. [CHECKED]

**After the draft:**
- Each new arm sets `ic->f` (and `arg[0]`) and leaves the switch by `break`.
- The MODE32 64-bit-instruction check (:5712-5725) is not taken: `x64` starts at 0 (:4276 `int main_opcode, rt, rs, rd, sa, s6, x64 = 0, s10;`) and the new arms never set it.
- The common tail then marks the page bitmap (cpu_dyntrans.c:1867-1876) and skips the combination check, which is NULL (:1888-1899). Its two `goto bad` checks cannot fire (:1902-1909).
- During read-ahead it returns before running the handler, so the handler is cached, not executed (:1917-1918). When single-stepping or in a cross-page delay slot it runs the handler once and discards it (:1925-1934); otherwise it executes it (:1978).
- No early return and no skipped tail.
- The six default words and the LWC3 else-path no longer reach `bad:`. 0x1e still does (:5568, :5574).
- The outer default at :5708 becomes unreachable: 58 existing top-level labels (:4370-:5703) plus the 6 new ones cover all 64 values of `iword >> 26`.
- One host-only change: read-ahead no longer stops at these words (:1959-1961).

[CHECKED]

**What `ic`, the PC and EPC hold.**
- At execution, `X(cpu)` and `X(reserved)` rebuild the PC from `ic - cur_ic_page` (:134-138, :151-155). This is needed because cached execution keeps `cpu->pc` accurate only to the page.
- `mips_cpu_exception`:
  - writes CE (cpu_mips.c:2049-2051);
  - writes EPC as the word's PC, or as PC - 4 with BD set when in a delay slot (:2138-2144; skipped when EXL is already set on non-EXC3K models, :2128);
  - sets `delay_slot = EXCEPTION_IN_DELAY_SLOT` (:2147-2148), so the branch does not apply its target (X(beq), cpu_mips_instr.c:194);
  - sign-extends EPC on 32-bit CPUs and repoints the translation pointers (:2219-2224).
- A cross-page delay slot goes through X(end_of_page) (:3734-3736 advance the page) and back into to_be_translated with `in_crosspage_delayslot` set (:4286-4290). EPC is then the page base minus 4, which is the branch.

[CHECKED, except the delay-slot case, which is REASONED and owed a measured row]

**Idioms compared:**
- **COP2 arm** (:5126-5130): `if (cpu->cd.mips.coproc[2] == NULL) { ic->f = instr(cpu); ic->arg[0] = 2; break; }`. The draft's COP2 arm is unconditional. There is no behavioural difference today: only `coproc[0]` and `[1]` (cpu_mips.c:262-263) and pmax's `[3]` are ever allocated. Either mirror the test or say why not. [CHECKED]
- **COP3 arm** (:5139-5143): the same pattern for coprocessor 3. pmax allocates it: machine_pmax.c:81 `cpu->cd.mips.coproc[3] = mips_coproc_new(cpu, 3);`, again at :170. With the draft, COP3 operations on pmax still stop (:5150-5152) while LWC3/SWC3 trap, and the draft's comment "no COP3 is modelled" is false. [CHECKED]
- **ISA gate** (:5527-5531): `if ((main_opcode == HI6_LDC1 || main_opcode == HI6_SDC1) && cpu->cd.mips.cpu_type.isa_level < 2) { ic->f = instr(reserved); break; }`, placed before the no-FPU CpU test. The draft omits it for LDC2/SDC2. The silent RI style itself matches the nearest siblings: LL/SC (:5471-5474), SPECIAL2 (:5224-5226) and ERET (:4869-4870). [CHECKED]
- **Gate threshold.** The draft reuses the PREF gate (:5554, `>= 4`) as the SWC3 boundary. COP3 ended at MIPS III, so the boundary is wrong by one level. [CHECKED]
- **Wrong tag in the comments.** The comments call this "the #236 idiom". #236 is the COP0-function RI fix (:4933-4937); the COP1 CpU arms (:5031-5039, :5543-5549) carry no tag. [CHECKED]

**Required changes:**
1. LDC2/SDC2: add `isa_level < 2` → `instr(reserved)` before the CpU(2) assignment, in the :5527-5531 shape. Do not set `x64`.
2. SWC3: RI for `isa_level >= 3` (numerically this also covers 4, 32 and 64). CpU(3) only on ISA I and II.
3. LWC3 else-arm: ISA III → `instr(reserved)`; ISA I and II → CpU(3). Keep the `>= 4` nop.
4. 0x1e off the R5900: replace `fatal("TODO: MDMX"); goto bad;` (:5571-5574) with `instr(reserved)`. Leave the R5900 arm to `mipsr5900lqsq`.
5. pmax needs an explicit ruling. Either:
   - unconditional CpU(3), with a comment saying the pmax coprocessor-3 object models only the BC3F poll (:5145-5148) and CU3 is not consulted; or
   - join `mipscop3pmaxstop`.
6. R5900: either exclude `rev == MIPS_R5900` from the 0x36/0x3e/0x33 conversions or disclose the choice. [UNSETTLED which is right]
7. Fix the comments:
   - drop "#236";
   - JALX: replace "exists only with MIPS16e" with "this model advertises no MIPS16 (cpu_mips_coproc.c:61)";
   - SWC3: "ISA I-III" becomes "ISA I-II";
   - qualify "No COP2 ... so the architectural result is CpU" as holding only while CU2 is clear;
   - mark the outer default as unreachable.
8. Drop hunk 2 (it deletes the blank line at :5600 after :5599 `switch (s6) {`). Regenerate the diff from a real edit: the packet contains no tab characters while the file is tab-indented (:5552 starts with a tab), and the hunk headers (-9,15 and -57,4) are relative to an excerpt. As written the diff cannot apply. [CHECKED]

**Effect on the detector.** These rows are not yet written. As it stands, the witness would pass the draft's wrong cells. My prediction, not a measurement: the draft as written scores 72/80 on this probe, because only the eight 0x1e rows stay red. Rows owed:

| CPU | 0x1d | 0x1e | 0x32 | 0x33 | 0x36 | 0x3a | 0x3b | 0x3e |
|---|---|---|---|---|---|---|---|---|
| R3000 (ISA I) | RI | RI | CpU2 | CpU3 | RI | CpU2 | CpU3 | RI |
| R4400 (ISA III) | RI | RI | CpU2 | RI | CpU2 | CpU2 | RI | CpU2 |

Also owed:
- an ISA IV or MIPS64 PREF accept row (PC + 4, Cause unchanged) and an SWC3 RI row;
- an ISA II row (`-C R6000`, if testmips constructs it) to pin `< 2` against `<= 2`;
- a delay-slot row (BD set, EPC = the branch);
- rows with CU2 or CU3 set that record the policy;
- a pmax row if pmax is ruled in.

## 4. Where the seats disagree

| # | Side A | Side B | What settles it |
|---|---|---|---|
| 1 | Argon: the PC mask zero-extends | GLM, Grok, Astra: it preserves the high bits | witness `64 cpu2 epc`; cpu.h:409, cpu_mips.h:191-195. Side B is right. |
| 2 | LWC3/SWC3 at ISA III → CpU3: the draft; Grok (bug review, fix draft, siblings, witness); GLM (bug review, witness; it flagged this as unsettled in its fix-draft answer) | → RI: Grok's manual answer; Astra (bug review: "MIPS-III reserved slot", unconfirmed) | mips-iv.txt:1426 with the key at :1447; mips_r4000.txt:5823/:5834. RI. |
| 3 | SWC3 at ISA IV is RI (draft, Grok fix draft, GLM) | Grok (bug review): MIPS IV still has SWC3; RI only from level 32 | mips-iv.txt:1439 (MIPS IV adds only COP1X and PREF) and :1369. RI already from III. |
| 4 | LDC2/SDC2 on ISA I → RI (Grok; fix-draft answers of Astra, GLM, Argon) | → CpU2 (the draft, Argon bug review, GLM witness); Astra (bug review): priority unsettled | mips-iv.txt:1372, :395, :865; R30xx has no LDCz; witness `32 ri`. RI. |
| 5 | 0x1e off the R5900: leave the stop (fix-draft packet) | RI (bug-review answers of all four seats) | mips-iv.txt:1404; mips_r4000.txt:5823; mips64_volII.txt:41/2039/2046; cpu_mips_coproc.c:94-107; witness mdmx rows. RI. |
| 6 | pmax LWC3/SWC3 → unconditional CpU3 (draft) | Grok (fix draft): CpU only when `coproc[3]` is NULL, else stop; Grok (bug review): a run-time CU3 check, RI when set; Astra: needs the R2020 specification | Presence: machine_pmax.c:81/170. CU3 clear means CpU3: mips-iv.txt:612/1153. CU3 set: UNSETTLED; the ruling seat (Fable) or the owner decides. |
| 7 | The outer default is unreachable after the draft (Grok, Astra) | It still catches R5900/MDMX words (packet); Argon UNSETTLED | the label walk :4370-:5703, plus the witness transcripts' TODO lines |
| 8 | Grok: R5900 0x36/0x3e are real LQC2/SQC2; 0x32/0x3a/0x3b → RI; 0x33 is PREF | The other seats are silent | only an R5900 (EE core) manual, which is not in `_scratchpad`. UNSETTLED. |
| 9 | JALX "only with MIPS16e" (draft, GLM, Grok) | Astra: the original MIPS16 also has it | mips32_volII.txt:690 refutes "only MIPS16e" (microMIPS also has it); original MIPS16 is UNSETTLED locally |
| 10 | Use the #309 shape: read-ahead `goto bad` plus a once-only notice (Astra, GLM and Argon, port answers) | No guest-visible difference; copy the COP2 arm (Grok fix draft Q3.7; GLM fix draft) | cpu_dyntrans.c:1917-1918 and :1938-1968: no guest-visible effect. A policy and record question. |
| 11 | R3000 has no CE field (GLM bug review) | CE is written (Grok, Astra) | witness `32 cpu2 exc 11/2` |
| 12 | Line drift (Argon bug review) | No drift (GLM, Grok, Astra) | `git log de8c7547..HEAD` is empty for those files |
| 13 | CU set: "CpU even if CU2 is set" (Grok bug review); "undefined, so CpU is policy" (Astra and GLM, manual answers) | MIPS32/64 require RI (Grok, manual answer) | mips-iv.txt:612 (undefined on I-IV) and mips32_volII.txt:1780 (RI on MIPS32/64). Both sides are right, for different ISA levels. |
| 14 | 0x1f off the R5900 is "simply reserved" (GLM fix draft) | It is SPECIAL3 on Release 2 (Grok, Astra) | cpu_mips_instr.c:5584-5699; mips64_volII.txt:2047 |
| 15 | `-e 5000` is a pmax rig (witness packet, GLM witness) | It is not an alias (Grok witness) | machine_pmax.c:989-1014, which lists `"3max", "5000/200"` and so on; the subtype lookup in machine.c uses exact `strcasecmp`. Grok is right. |

## 5. Anything else

- **The manual brief went out without its manual text.** 12_packet_manual.md labels its blocks with lines 1447, 612, 1153, 395 and 865 but prints the page-header lines 1446, 611, 1152, 394 and 864 instead. The key and the LWCz/SWCz/LDCz/SDCz rules never reached the seats; only COPz (:236) and JALX came through. Astra, Argon and GLM said so; Grok read the real file. Do not treat that stage as having checked the manual. [CHECKED]
- **The PREF-on-5KE transcript is gone.** WITNESS.md quotes `pref 0x0,0(zr)`, but that session was overwritten by the re-run; only the RUN.log score (17/80) survives. Source supports the claim (cpu_mips_instr.c:5554-5556; disassembler cpu_mips.c:1264-1265). The owed PREF accept row will measure it again. [CHECKED]
- **Seat factual slips** (count arguments, not seats):
  - Argon's bug-review sketch adds a top-level `case 0x1e:`, which duplicates `case HI6_LQ_MDMX:` (0x1e at opcodes_mips.h:429) and would not compile.
  - GLM's siblings answer puts LWC3 at "0x35" (it is 0x33, :467) and calls 0x3f unassigned (it is SD, :479).
  - GLM's witness answer says `HI6_LQ_MDMX` is 0x1d. [CHECKED]
- **A false fix-draft packet premise.** "#309's ruling converted only encodings that ARE reserved" is false. #309's default (cpu_mips_instr.c:5372-5411) also turns REGIMM 0x1f (SYNCI, filed as `mipssynci`) and 0x18/0x19 (MTSAB/MTSAH, opcodes_mips.h:74) into RI. [CHECKED]
- **Related filed rows:**
  - `mipscop3isa3` states the same MIPS III fact for 0x13; the draft's CpU3 at ISA III would contradict it.
  - `mipscop3pmaxstop` says "join mipsprimundec's round if witnessed".
  - `mipscop2retrap`: the draft copies this gap into four new arms.
  - `mipsr5900lqsq` and `mipscop1xcpu`: do not touch.
  - `mipsspecialrsvd` and `mipsmovciundec`: the same class in the SPECIAL default at :4679.
- **An `exit(1)` in the same file.** X(end_of_page2) still ends in `exit(1)` (cpu_mips_instr.c:3797-3798), while the m88k twin (cpu_m88k_instr.c:2827 onward) was changed to `debugmsg_cpu` plus `ABORT_EXECUTION`. No ledger, OUTSTANDING_BUGS or CHANGELOG entry names it (grep count 0). I did not trace whether a guest can reach it. Candidate for `cpusexitsweep`. [UNSETTLED]
- **Minor MIPS II sibling.** On ISA II, 0x37 and 0x3f are LDC3 and SDC3 (mips-iv.txt:1380). The fork decodes them as LD/SD with `x64 = 1`, which becomes RI through the MODE32 check (:5436, :5440, :5712-5725). Reachable only with `-C R6000`. [REASONED]
- **The once-only notice.** The port notes (FORKS:176) recommended the #309 print-once notice. The draft departs from that without saying so. No notice is right for architected exceptions, matching the COP1, COP2, COP3 and LDC1 arms, but the record should say why. [REASONED]