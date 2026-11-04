# r_mpu (agent a7e40a27c08bffd9b).  Final text 2026-11-04T08:38:35.800Z by claude-opus-5-5; banked 2026-11-04 from the subagent transcript (it was summarised in BATCH.md at 02:3x but never saved).

OPUS_SEAT_ALIVE_20261104_MPU
# mipsprimundec -- what is in this directory, and what is MISSING

VERDICT: NO-GO

The disposition is right: raise the architectural exception instead of stopping the CPU, through `X(cpu)` and `X(reserved)`. The draft as written still fails in four ways:

1. **LWC3 (0x33) and SWC3 (0x3b) on ISA III.** The draft raises Coprocessor Unusable (CpU) with CE=3. The local MIPS IV and R4000 manuals say MIPS III removed coprocessor 3, so these words take Reserved Instruction (RI). This hits the arc rig (R4000/R4400) and the witness's own 64-bit CPU. The fork filed the same fact for opcode 0x13 on 2026-11-02 (`mipscop3isa3`).
2. **LDC2/SDC2 (0x36/0x3e) on ISA I.** The draft raises CpU CE=2. These encodings do not exist before MIPS II, so RI is owed. This hits the pmax rig.
3. **0x1e off the R5900 is left on `goto bad`.** The 8 `mdmx` witness rows stay red: I predict 72/80. 0x1e is a reserved cell on every non-R5900 CPU in the tree, so by the draft's own rule ("convert only encodings that ARE reserved") it should be RI.
4. **Four comment sentences are wrong records**, and an unrelated blank-line hunk rides along.

Five bounded changes make it a GO; the shape is at the end of Q3.

**Abbreviations** (all under `C:\DocumentNoSnc\cc\GXEMUL\`):
- `I` = `GXEMUL-SEC\src\cpus\cpu_mips_instr.c`, `D` = `...\cpu_dyntrans.c`, `M` = `...\cpu_mips.c`, `CO` = `...\cpu_mips_coproc.c`
- `T` = `GXEMUL-SEC\src\include\mips_cpu_types.h`, `OP` = `...\include\opcodes_mips.h`
- Manual extracts: `M4` = `_scratchpad\mips-iv.txt`, `R4K` = `mips_r4000.txt`, `IDT` = `idt_r30xx.txt`, `M64` = `mips64_volII.txt`, `M32` = `mips32_volII.txt`. All are non-empty (416 KB to 1.07 MB).
- `W` = `GXEMUL-SEC\regress\artifacts\mipsprimundec\witness_20261104\`

HEAD is `ebe5af82`. `git diff` from `de8c7547` and from `50f9c601` to HEAD is empty for I, D, M, CO, OP, T, `machine_pmax.c` and `machine_test.c`, and `git status` shows them clean. So every line number in both briefs is still exact. Argon-BR's "slight drift" is wrong. CHECKED.

Seat abbreviations: BR = bug-review answer, FD = fix-draft answer.

## Q1. Premises the witness refutes or narrows

**1. "The eight words reach `default: goto bad`" — narrowed.**
- Six words fall to `I:5708 default:goto bad;`. 0x1e and 0x33 reach `bad` through their own arms: `I:5571-5574 fatal("TODO: MDMX\n"); goto bad;` and `I:5558-5560`.
- The transcripts show this: `32_mdmx.txt` prints `TODO: MDMX` and `64_lwc3.txt` prints `TODO: lwc3 not implemented yet`, each before `UNIMPLEMENTED instruction`. CHECKED.
- Said so: GLM-BR, Grok-BR, Astra-BR, Grok-FD, Astra-FD.
- Said the opposite: Argon-BR, which marks the default-path claim HOLDS and would also convert the R5900 arms at `I:5568` and `:5581`.

**2. "0x1e is R5900-only" and "MDMX is a real instruction this tree does not implement" — refuted.**
- The measured 0x78000000 sessions on the R4400 and R3000 run the non-R5900 MDMX arm and stop.
- On both CPUs 0x1e is a reserved cell (`M4:1372`, `:1388`).
- Said so: GLM-BR/FD, Astra-BR/FD, Grok-FD.
- Argon-FD left it UNSETTLED ("no proof 0x1e corresponds to HI6_LQ_MDMX"); `OP:429 #define HI6_LQ_MDMX 0x1e` settles it. CHECKED.

**3. "Every MIPS machine" — narrowed for 0x33.**
- In the witness's first run, the testmips default CPU (5KE, MIPS64 release 2: `machine_test.c:406`, `:412`, `T:104`) executed 0xcc000000 as PREF. That is the existing `I:5554-5556 isa_level >= 4` nop arm, matching the row's own "LWC3 below ISA IV".
- Every seat that addressed it keeps that nop (GLM-BR, Grok-BR, Astra-BR); none disagreed. (The transcript of that run did not survive; see Q5.)

**4. "The PC handling in X(cpu)/X(reserved) is right for a 64-bit kernel" — supported for the non-delay case.**
- The `64 cpu2` row reads EPC `0xffffffff80020000` and PC `0xffffffff80000180` through `X(cpu)` on the 64-bit translator (`W\prefix_build.out`). CHECKED.
- Said so: GLM-FD, Grok-FD, Astra-FD.
- Said the opposite: Argon-FD ("zero-extend ... clearing the upper 32 bits ... BROKEN"). That is refuted by the row and by C: `~((1024-1) << 2)` is a negative int, which converts to `uint64_t` as `0xfffffffffffff003` (`cpu.h:409`, `uint64_t pc`).
- The delay-slot case is unmeasured and owed.

**5. "Cause.CE carries the coprocessor number" — confirmed on the R3000.**
- `32_cpu2.txt` reads `cause=2000002c` with `ce=2`, matching `IDT:2462-2465`. CHECKED.
- Grok-BR and Astra-BR gave CE values for the R3000. GLM-BR said the opposite ("R3000 Cause has no CE field").

**6. "The COP2/COP3 forms owe CpU (the #236/#309 idiom)" — the label is wrong.**
- The witness controls do prove the two idioms the fix needs: the COP2 arm (`I:5123-5130`) gives CpU CE=2 on both translators, and the ISA-I LDC1 gate (`I:5527-5531`) gives RI on the R3000.
- But #236 and #309 are both RI fixes, not CpU precedents: `I:4933-4937` is a COP0 function raising `instr(reserved)` (confirmed by `CHANGELOG.md:24220-24221`), and `I:5372-5411` is the REGIMM default. CHECKED.
- Grok-BR said so and named the right CpU precedents. GLM-FD ("same shape as the shipped COP1 arm") and Argon-BR ("mimicking #309") did not flag it.

**7. "witness: none" — superseded** by `W`: a rung-3 witness on unmodified testmips, symptom present pre-fix, controls OK, null media rejected (`RUN.log` 01:14:58). CHECKED.

**8. Still REASONED, not measured:** "any privilege" (only kernel mode was run), the pmax and arc rigs (only testmips), and a word in a delay slot. The arms have no privilege test (`I:5552-5708` read). User reach needs a mapped, executable user page. Grok-BR and Astra-BR said so; Argon-BR's "READ/HOLDS" for any privilege overstates.

**What the witness cannot settle:** which exception each word owes. Its `exc` rows accept 10 or 11 (`probe_frozen.py:126-129`, `:159`).

## Q2. Required exception per word and ISA level

"CpU n" means Coprocessor Unusable with CE=n, owed while Status.CUn is clear. CUn is clear at cold start on every machine: `CO:374-380` sets CU0|CU1 only, and the transcripts show `status=30000000` and `0x34000000`. In-tree ISA levels are only 1, 2, 3, 4, 32 and 64 (`T:68-113`).

| word | ISA I (R2000, R3000, TX3920) | ISA II (R6000, Allegrex) | ISA III (R4000, R4400, VR41xx, R5900) | ISA IV (R5000, R10000, RM5200) | MIPS32/64 | draft gives |
|---|---|---|---|---|---|---|
| 0x1d JALX `74000000` | RI | RI | RI | RI | RI (valid only with MIPS16e or microMIPS) | RI, correct |
| 0x1e `78000000` | RI | RI | RI (R5900: LQ) | RI | RI (ASE not modelled) | **CPU-STOP** |
| 0x32 LWC2 `c8000000` | CpU 2 | CpU 2 | CpU 2 | CpU 2 | CpU 2 | correct |
| 0x33 LWC3 `cc000000` | CpU 3 | CpU 3 | **RI** | PREF | PREF | **CpU 3 at III** |
| 0x36 LDC2 `d8000000` | **RI** | CpU 2 | CpU 2 | CpU 2 | CpU 2 | **CpU 2 at I** |
| 0x3a SWC2 `e8000000` | CpU 2 | CpU 2 | CpU 2 | CpU 2 | CpU 2 | correct |
| 0x3b SWC3 `ec000000` | CpU 3 | CpU 3 | **RI** | RI | RI | **CpU 3 at III** |
| 0x3e SDC2 `f8000000` | **RI** | CpU 2 | CpU 2 | CpU 2 | CpU 2 | **CpU 2 at I** |

**Evidence by column** (all CHECKED, quoted as extracted):
- **ISA I:** `M4:1372` (Table A-37): row 3 is all `*`; row 6 reads `*LWC1LWC2LWC3****`; row 7 reads `*SWC1SWC2SWC3****`. `M4:612` and `:1153` list LWC3/SWC3 as "MIPS I". `M4:395` says LDC2 is "MIPS II".
- **ISA II:** `M4:1380` (Table A-38) shows `LLLWC1LWC2LWC3*LDC1LDC2LDC3`. `M4:1415` (Table A-42) lists LDC2/SDC2 as added in MIPS II.
- **ISA III:**
  - `M4:1426` (Table A-43) reads `*(wasCOP3)`, `*(was LWC3)`, `*(was SWC3)`.
  - The key at `M4:1447`: `*(asterisk)This opcode is reserved for future use. An attempt to execute itcauses a Reserved Instruction exception.`
  - `M4:1365` names the R4000, R4200, R4300, R4400 and R4600; `:1366` and `:1369` say CP3 "was removed from MIPS III and later architecture levels".
  - `R4K:5823` shows `LWC1LWC2*SWC1SWC2*`, `COP1COP2*`, `LDRe****`. The key at `R4K:5834`: "cause reserved instruction exceptions in all current implementations". `R4K:18` says the manual covers "the MIPS R4000 and R4400 family". The LWCz/LDCz/SWCz encoding pages list units 1 and 2 only (`R4K:5111-5112`, `:4976-4977`, `:5595-5596`).
- **ISA IV:** `M4:1396` (Table A-40) shows `LLLWC1LWC2PREF`. `M4:1404` shows `*1*1*1*1` at 0x1c-0x1f. `M4:1439` (Table A-44) adds only COP1X, PREF, MOVCI and MOVZ/MOVN, so 0x3b stays reserved.
- **MIPS32/64:**
  - `M64:2039-2048` (Table A-2): row 3 `... SPECIAL2 JALX MDMX SPECIAL3`, row 6 `LL LWC1 LWC2 PREF`, row 7 `SWC2*SCD`; `M64:2032` defines `*` as RI.
  - `M64:41`: MIPS16e and MDMX are ASE volumes IV-a and IV-b. `M64:838` and `:1055`: LDC2 and LWC2 are "MIPS32", listing CpU and RI.
  - `M32:690`: JALX is "MIPS32 with (microMIPS or MIPS16e)". `M32:1782`: `JALX6R H`, `LWC26Rm T`. `M32:1780`: H means an unimplemented Module/ASE must raise RI; T means CpU when access is not allowed, RI when it is allowed.
- **The emulator's own configuration:** `CO:61` `const int m16 = 0;`. `CO:104` sets Config1 MIPS16 to 0, and `CO:102-106` set no COP2 or MDMX bit. `CO:176` sets the VR41xx M16 bit to 0. `coproc[2]` is never assigned anywhere in `src/` (grep).

**Where these words are valid instructions:**
- PREF at 0x33 from ISA IV, MIPS32 and MIPS64 (`M4:1396`, `M64:1357`).
- JALX on MIPS32/64 cores with MIPS16e or microMIPS (`M32:690`), and, REASONED with no local manual, on the original-MIPS16 NEC VR41xx. The emulated VR41xx advertise no MIPS16 (`CO:176`).
- MDMX at 0x1e on MIPS64 cores with that ASE; none is modelled.
- LQ at 0x1e on the R5900 (`OP:429`).

**What the manuals do not settle (UNSETTLED):**
- **R5900 (Emotion Engine)** meanings of 0x32/0x33/0x36/0x3a/0x3b/0x3e. Grok-FD cites PCSX2 for PREF, LQC2, SQC2 and empty slots; no local manual settles it. The EE Core Instruction Set Manual would.
- **Allegrex** VFPU use of the COP2 slots, and **VR5432** vendor extensions. No local manual.
- **pmax with CU3 set.** pmax installs a real CP3 object (`machine_pmax.c:81`, `:170`). For an unimplemented coprocessor `M4:236` and `:612` call the result undefined, but the R2020/R3220's behaviour is not in any local file. `mipscop3pmaxstop` already records it as "not established".
- **ISA-I CP3 cells by implementation.** The generic MIPS I text says CpU 3 (`M4:612`, `:1153`; `IDT:17142-17162` lists LWC3 with CpU). But IDT's own R30xx parts raise RI for SWC3 (`IDT:18335-18336`: "causes a reserved instruction exception, not a coprocessor unusable exception") and for MFC3 (`IDT:17411`). `M4:1369` calls CP3 "implementation-specific" in MIPS I and II. The tree's R2000/R3000 are the DECstation parts, so CpU 3 is a defensible choice, but it is a choice and the comment should say so.
- **Smaller gaps:** the glyph on M64's JALX/MDMX cells did not extract (every candidate glyph gives RI without the ASE); the `M32` extract is the Release 6 edition and does not show the pre-Release-5 MIPS32 meaning of 0x1e (RI either way).

## Q3. The draft against the real control flow in both translators

**Same body in both translators.** `generate_tail.c:141-154` includes the file a second time under MODE32, so `instr(cpu)` and `instr(reserved)` resolve to the mode's own copy. The new arms contain no `#ifdef MODE32`. CHECKED.

**Paths to `bad:` for the eight words.**
- Pre-fix: `I:5708` (six words), `I:5560` (0x33 below ISA IV), `I:5568` and `:5574` (0x1e).
- After the draft, only `I:5568` and `:5574` remain; 0x1e still stops.
- `bad:` returns without stopping during read-ahead (`D:1990-1991`) and clears `cpu->running` on execution (`D:2014`).
- The other ways into `bad:` cannot be reached from the new arms: the MODE32 tail (`I:5713-5725`) needs `x64`, which stays 0, and `D:1902-1909` fires only if `ic->f` is unset.

**Sketch rule.** Every new arm ends in a `break` of the primary switch, not of an inner one. Control reaches the `x64` block and the shared tail (`D:1857-1980`), so nothing is skipped. CHECKED.

**What `ic` and the PC hold.**
- On entry, `low_pc` comes from `ic`, and `I:4292-4295` forces `cpu->pc` to that slot's address.
- When single-stepping, the new arm executes in the same call (`D:1938`, `:1978`).
- When free-running, read-ahead translates later slots and moves `cpu->pc` each time (`I:4295`). That is why `X(cpu)` and `X(reserved)` rebuild the PC from `ic` (`I:134-138`, `:151-155`).
- Delay slot: `X(beq)` sets `TO_BE_DELAYED` and calls `ic[1]` (`I:191-192`). `mips_cpu_exception` then sets EPC to pc-4 with BD set (`M:2138-2144`), and the branch skips its own jump on `EXCEPTION_IN_DELAY_SLOT` (`I:194-205`).
- Cross-page delay slot: `X(end_of_page)` moves `cur_ic_page` and calls `to_be_translated` directly (`I:3747`, `:3768`), so the rebuild yields the slot-0 address and EPC becomes the branch.
- Afterwards: CE is always written (`M:2049-2051`); the vector is base+0x080 on EXC3K and base+0x180 otherwise (`M:2170-2203`); `pc_to_pointers` runs (`M:2219-2224`).
- Status: CHECKED, plus REASONED for the delay-slot result, which is unmeasured.

**Is it the same idiom?** Partly.
- It matches the absent-coprocessor shape: COP1 (`I:5034-5039`, `:5545-5549`) and COP2 (`I:5126-5130`) choose `instr(cpu)` at translation time without reading Status, and the cached handler is safe because nothing it depends on changes.
- It drops COP2's `coproc[2] == NULL` test. Behaviour is the same today, since nothing assigns `coproc[2]`, but no row could see the difference, so keep the test for parity or say why not.
- It diverges from COP3 (`I:5139-5153`), which raises CpU only when `coproc[3] == NULL`. On pmax the draft's unconditional CpU 3 is right while CU3 is clear; that is a design choice, not a copy of the COP3 arm.
- It omits the tree's own ISA gate for doubleword transfers, the LDC1/SDC1 gate at `I:5527-5531`.
- It is not the `#309` shape. `#309` declines translation during read-ahead and raises RI at execution behind a latched warning, because it reports an emulator gap (`I:5390-5411`). For architectural exceptions, a silent, cached handler is the right shape.
- If a CU-dependent policy is ever chosen (pmax CU3, or RI for MIPS32 when CU2 is set), it must be checked at execution time, like `COPROC_AVAILABILITY_CHECK` (`I:43-56`), because the translation is cached.

**`x64` stays 0 in every new arm.** That is correct: LDC2 is valid on 32-bit CPUs ("MIPS32", `M64:838`; "MIPS II", `M4:395`). Setting it would turn LDC2/SDC2 into RI on MODE32 CPUs at ISA II and 32.

**The outer default becomes unreachable.** The primary switch has 58 one-tab case labels (`I:4370-5703`); adding six makes all 64 opcode values. CHECKED. Keeping `default:` is harmless, but the packet's reason for it is false: R5900 LQ/SQ and MDMX never reach it.

**Corrected shape** (REASONED; tabs in the file):
```c
case HI6_LWC2: case HI6_SWC2: case HI6_LDC2: case HI6_SDC2:
    if ((main_opcode == HI6_LDC2 || main_opcode == HI6_SDC2) &&
        cpu->cd.mips.cpu_type.isa_level < 2) {   /* MIPS II, mips-iv.txt:395 */
        ic->f = instr(reserved); break;
    }
    ic->f = instr(cpu); ic->arg[0] = 2; break;   /* as HI6_COP2; coproc[2] never set */
case HI6_SWC3:
    if (cpu->cd.mips.cpu_type.isa_level >= 3) {  /* CP3 removed in MIPS III, :1426 */
        ic->f = instr(reserved); break;
    }
    ic->f = instr(cpu); ic->arg[0] = 3; break;
case 0x1d:  /* JALX: MIPS16(e)/microMIPS only; m16 = 0 */
    ic->f = instr(reserved); break;
/* HI6_LWC3:  >= 4 nop (unchanged);  >= 3 instr(reserved);  else instr(cpu), arg 3 */
/* HI6_LQ_MDMX: R5900 arm unchanged; else  ic->f = instr(reserved); break;  */
```

**The `break` after the new 0x1e RI is load-bearing.** The current arm ends in `goto bad;` followed by a commented-out `/*  break  */` (`I:5574-5575`), directly above `case HI6_SQ_SPECIAL3:`. Without the `break`, 0x78000000 falls through. On release-2 CPUs (5KE, 24KEc, 4KEc) it then decodes as SPECIAL3 EXT with rt=0, i.e. `instr(nop)` (`I:5584-5611`, `OP:432`). On older CPUs it becomes RI with a misleading "SPECIAL3 opcode used" warning. REASONED from source; it needs a row on the 5KE.

Also drop the blank-line hunk inside SPECIAL3 (`I:5599-5600`).

## Q4. Where the seats disagree

| # | Position A | Position B | Settled by |
|---|---|---|---|
| 1 | LWC3/SWC3 on ISA III raise CpU 3 (draft; Grok-BR; Grok-FD; GLM-BR) | Possibly RI: Astra-BR ("the MIPS-III reserved slot"); GLM-FD ("if COP3 died at MIPS III the gate is off by one", UNSETTLED) | `M4:1426` with key `:1447`, `M4:1365-1369`, `R4K:5823`/`:5834`: **RI** |
| 2 | SWC3 becomes RI from ISA IV (draft, GLM-BR, Grok-FD) | from MIPS32 (Grok-BR) | Same tables: **from ISA III**; both proposals are wrong |
| 3 | LDC2/SDC2 at ISA I raise CpU 2 (draft) | RI (GLM-FD, Grok-BR/FD, Astra-FD, Argon-FD) | `M4:1372` (cells `*`), `:395`, `I:5527-5531`; the `32 ri` control measures that gate |
| 4 | pmax LWC3/SWC3: CpU 3 always (draft) | CU3 checked at run time, CpU when clear and RI when set (Grok-BR); keep `goto bad` (Grok-FD); undecided (Astra-FD, GLM-FD) | CU3 clear means CpU 3 (`M4:612`, `:1153`). CU3 set: no local file; it needs a ruling and a pmax-rig check of whether any guest issues these words. Keeping `goto bad` breaks the fork's never-stop rule |
| 5 | 0x1e off the R5900 stays at `bad` (draft) | RI (GLM-BR, Grok-BR, Astra-BR, Argon-BR) | `M4:1372`/`:1388`/`:1396` row 3; `M64:2039` and `:2046`; `CO:102-106`; measured stop in the `mdmx` rows |
| 6 | Convert the R5900 LQ/SQ arms too (Argon-BR) | Leave them (GLM, Grok, Astra) | `OP:429` (LQ is a real instruction); no local EE manual, so leave and disclose |
| 7 | The 64-bit PC rebuild is correct (GLM-FD, Grok-FD, Astra-FD) | It zero-extends (Argon-FD) | The `64 cpu2` row: EPC `0xffffffff80020000` |
| 8 | The R3000 has a CE field (Grok-BR, Astra-BR) | It does not (GLM-BR) | `IDT:2434-2465`; `32 cpu2` reads `ce=2` |
| 9 | The outer default becomes dead (Grok-FD, Astra-FD) | It still catches LQ/SQ/MDMX (fix-draft packet; GLM-FD unsure) | The 58-label enumeration plus 6 = 64 |
| 10 | R5900 slots are PREF/LQC2/SQC2/empty (Grok-FD, citing PCSX2) | The others are silent | UNSETTLED; the EE Core manual settles it |
| 11 | No warning, because the exception is architectural (Grok-BR, draft) | Follow `#309`'s pattern (Argon-BR) | `I:5390-5396`: `#309` latches because it reports an emulator gap |
| 12 | With CU2 set, raise CpU anyway (draft, the COP2 arm) | RI on MIPS32/64 (Grok's manual-brief answer) | MIPS I-IV: undefined (`M4:236`, `:612`), so CpU is acceptable. MIPS32: the T key prescribes RI (`M32:1780`). Disclose; the existing COP2 arm has the same corner |

Grok contradicts itself on rows 1-2: its own manual-brief answer (`22_answer_manual_grok.txt:3`, `:27`, `:63`) reached RI at ISA III. That is the position the local extracts confirm.

## Q5. Other findings

1. **The manual packet inlined page headers instead of rules.** `_scratchpad\gweb\mk_extra_packets.py:41` reads with `io.open(...).read().split("\n")` in default newline mode. A lone CR at `M4:303` therefore shifts every later label by one. As a result `M4KEY:1447`, `M4LWCZ:612`, `M4SWCZ:1153`, `M4LDCZ:395` and `M4SDCZ:865` carried the headers at 1446, 611, 1152, 394 and 864. Line 236, before the CR, came out correctly.
   - CHECKED: the line comparison, the CR's position, and line 41. REASONED: the mechanism.
   - That is why packet-fed seats could not settle the ISA III cells. `M32` has 231 CRs and `M64` has 133, so packets citing them carry the same risk. Fix: read with `newline=""`.
2. **The PREF-on-5KE result has no preserved transcript.** That run's outputs were overwritten; only the `RUN.log` 01:14:10 line ("17/80") remains. The owed PREF row would restore the evidence.
3. **The witness's EPC rows cannot see the PC rebuild.** A cold single-step sets `cpu->pc` (`I:4295`) before the handler runs, and PLANT sits at IC-page slot 0. A free-running or delay-slot row at a non-zero page offset is needed.
4. **The probe has no 64-bit RI control.** RI on the 64-bit translator is exercised only by `#309`'s `arc regimm rt=0x15` row (`mips_subnorm_probe.py:357`), which I read but did not run.
5. **Detector rows must pin (ExcCode, CE) per word per CPU.** As written, the probe would pass the draft's four wrong-exception sessions (`32 ldc2`, `32 sdc2`, `64 lwc3`, `64 swc3`).
   - The `x64` mutant needs a MODE32 CPU at ISA II or 32 (for example `-C 4KEc`); the R3000 and R4400 cannot see it.
   - The fall-through mutant needs the 5KE.
6. **Records state.** The witness directory and `regress/mips_primundec_probe.py` are untracked at HEAD (`git status`: `??`).
7. **Siblings.**
   - `mipscop3isa3`, `mipscop1xcpu` and `mipscop3pmaxstop` already exist; keep the LWC3/SWC3 predicate consistent with `mipscop3isa3`.
   - New candidate filing: MIPS II defines LDC3/SDC3 at 0x37/0x3f (`M4:1380`, `:1415`), but the tree decodes them as LD/SD and, via `x64`, raises RI on ISA II CPUs (`I:5425-5440`, `:5712-5725`).
   - The emulator lets a guest set CU2/CU3 (`CO:917-919` masks only bit 21).
8. **Comment corrections.** Cite `HI6_COP2` and the LDC1 gate, not `#236`. Write "ISA I-II", not "I-III". Drop "no COP3 is modelled" (pmax models one). Write "MIPS16(e) or microMIPS", not "only MIPS16e".