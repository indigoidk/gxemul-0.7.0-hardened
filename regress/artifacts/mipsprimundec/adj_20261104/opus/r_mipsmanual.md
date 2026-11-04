# MIPS manual conformance per opcode (agent a5c2e80d36ef4b3b5).  Final text 2026-11-04T08:55:02.949Z by claude-opus-5-5.

OPUS_SEAT_ALIVE_20261104_MIPSMANUAL

VERDICT: CANDIDATE-DIFFERS (0x1e at every level; 0x36 and 0x3e at MIPS I; 0x33 and 0x3b at MIPS III/R4400) ; MANUALS-DO-NOT-SETTLE (0x3b at MIPS I; 0x3b at MIPS32 before Release 6; 0x32/0x36/0x3a/0x3e at MIPS32/64 when Status.CU2 = 1 and there is no coprocessor 2)

**Files checked; none are empty.**
- `idt_r30xx.txt`: 1,071,238 bytes, 22,370 lines.
- `mips_r4000.txt`: 859,594 bytes, 6,526 lines.
- `mips-iv.txt`: 416,407 bytes, 2,206 lines.
- `mips32_volII.txt`: 775,072 bytes, 1,872 lines. This is MD00086 **Rev 6.04 (Release 6)**; it shows the older encodings with "6R"/"6Rm" marks.
- `mips64_volII.txt`: 500,193 bytes, 2,099 lines. This is MD00087 **Rev 2.50**.

**What each mark means.**
- R4000: `*` = "cause reserved instruction exceptions in all current implementations" (`mips_r4000.txt:5834`). RI = undefined major opcode (`:1154`). CpU = coprocessor unit not marked usable (`:1158`). CE = coprocessor unit number referenced (`:1005`).
- MIPS IV (`mips-iv.txt:1447`): `*` = RI. π = coprocessor operation, CpU if access is not allowed. κ = removed in a later revision; RI when a MIPS III/IV CPU runs in MIPS II-only mode.
- MIPS32 Rev 6.04: `*` = RI (`:1775`). T = "RI (… coprocessor to which access is allowed) or CpU (… not allowed)" (`:1780`). H = extension; RI if not implemented (`:1780`). 6R/6Rm = RI on Release 6 (`:1782`).
- MIPS64 Rev 2.50: `*` = RI (`:2032`). θ = same RI/CpU rule as T (`:2039`). ε = extension; RI if not implemented (`:2039`).
- IDT: CE = the coprocessor number taken from the instruction (`idt_r30xx.txt:2462-2465`).

| op | level | instruction | required exception | read at | candidate agrees? |
|---|---|---|---|---|---|
| 0x1d | MIPS I | reserved `*` | RI | mips-iv.txt:1372 (MIPS I row 3: all 8 cells `*`). IDT has no opcode table and no JALX | yes |
| 0x1d | MIPS II | reserved | RI | mips-iv.txt:1380 | yes |
| 0x1d | MIPS III (R4000/R4400) | reserved | RI | mips_r4000.txt:5823 (`LDRe****`), PDF p.649 row 3 cols 4–7, :5834; mips-iv.txt:1388 | yes |
| 0x1d | MIPS IV | reserved | RI | mips-iv.txt:1396; :1404 (`*1` ×4 at 0x1c–0x1f) | yes |
| 0x1d | MIPS32 | JALX, "MIPS32 with (microMIPS or MIPS16e), removed in Release 6"; marks 6R, H | RI unless MIPS16e/microMIPS is implemented | mips32_volII.txt:690, :1782, :1780 | yes (the fork has no MIPS16: cpu_mips_coproc.c:61) |
| 0x1d | MIPS64 | JALX ε | RI unless MIPS16e is implemented | mips64_volII.txt:2046, :2039 | yes |
| 0x1e | MIPS I–IV | reserved | RI | mips-iv.txt:1372, :1380, :1388, :1396, :1404; R4000 p.649 | **no**: the candidate stops the CPU |
| 0x1e | MIPS32 | MSA (H, class); MDMX "not applicable" to MIPS32 | RI unless MSA is implemented | mips32_volII.txt:1782, :1780, :30 | **no** |
| 0x1e | MIPS64 | MDMX ε (class) | RI unless MDMX is implemented | mips64_volII.txt:2046, :2039 | **no** |
| 0x32 | MIPS I | LWC2 (π) | CpU CE=2 | mips-iv.txt:1372, :612, :616; idt_r30xx.txt:17158, :17148 | yes |
| 0x32 | MIPS II/III/IV | LWC2 | CpU CE=2 | mips-iv.txt:1380, :1388, :1396; mips_r4000.txt:5112, :5106 | yes |
| 0x32 | MIPS32/64 | LWC2 (T/θ) | CpU CE=2 if access is not allowed; RI if allowed and nothing is encoded | mips32_volII.txt:851, :1782; mips64_volII.txt:1055, :2048 | yes when CU2=0 |
| 0x33 | MIPS I | LWC3 (π, κ) | CpU CE=3 | mips-iv.txt:1372, :612, :616; idt_r30xx.txt:17162, :17148 | yes (see unsettled item 1) |
| 0x33 | MIPS II (a native MIPS II CPU) | LWC3 (π, κ) | CpU CE=3; RI in MIPS II-only mode of a MIPS III/IV CPU | mips-iv.txt:1380, :1365, :1369 | not stated in the brief |
| 0x33 | MIPS III | reserved `*` | **RI** | R4000 p.649 (row 6, col 3), mips_r4000.txt:5823, :5834, :5111-5112; mips-iv.txt:1388, :1426 ("*(was LWC3)"), :1365 | **no**: candidate gives CpU CE=3 |
| 0x33 | MIPS IV | PREF | executes; doing nothing is allowed. Its only listed exception, RI, applies when MIPS IV instructions are not enabled | mips-iv.txt:1396, :1404 ("PREF4"), :818, :824 | not stated (the committed arm already treats it as a no-op at isa_level ≥ 4: cpu_mips_instr.c:5552-5556) |
| 0x33 | MIPS32 | PREF (pre-R6) | executes; only Bus Error or Cache Error | mips32_volII.txt:1782, :1200, :1206 | not stated |
| 0x33 | MIPS64 | PREF | executes; only Bus Error or Cache Error | mips64_volII.txt:2048, :1357, :1368 | yes |
| 0x36 | MIPS I | reserved `*` | **RI** | mips-iv.txt:1372 (row 6: `* LWC1 LWC2 LWC3 * * * *`), :1415 (added in MIPS II), :395 | **no**: candidate gives CpU CE=2 |
| 0x36 | MIPS II/III/IV | LDC2 | CpU CE=2 | mips-iv.txt:1380, :1388, :1396, :399; mips_r4000.txt:4977, :4971 | yes |
| 0x36 | MIPS32/64 | LDC2 (T/θ) | same as 0x32 | mips32_volII.txt:735; mips64_volII.txt:838, :2048 | yes when CU2=0 |
| 0x3a | MIPS I | SWC2 (π) | CpU CE=2 | mips-iv.txt:1372, :1153, :1157; idt_r30xx.txt:18366, :18356 | yes |
| 0x3a | MIPS II/III/IV | SWC2 | CpU CE=2 | mips-iv.txt:1380, :1388, :1396; mips_r4000.txt:5596, :5592 | yes |
| 0x3a | MIPS32/64 | SWC2 (T/θ) | same as 0x32 | mips32_volII.txt:1461; mips64_volII.txt:1781, :2048 | yes when CU2=0 |
| 0x3b | MIPS I | SWC3 (π, κ) | CpU CE=3 per mips-iv.txt; **RI per IDT** | mips-iv.txt:1372; idt_r30xx.txt:18335-18336 | **unsettled** |
| 0x3b | MIPS II (native) | SWC3 (π, κ) | CpU CE=3; RI in MIPS II-only mode | mips-iv.txt:1380, :1365 | not stated |
| 0x3b | MIPS III | reserved `*` | **RI** | R4000 p.649 (row 7, col 3), :5834, :5595-5596; mips-iv.txt:1388, :1426 ("*(was SWC3)") | **no**: candidate gives CpU CE=3 |
| 0x3b | MIPS IV | reserved `*` | RI | mips-iv.txt:1396, :1404 ("∗3"), :1447 | not stated |
| 0x3b | MIPS32 | no pre-R6 mark; the cell shows only the Release 6 class PCREL | not settled by this file | mips32_volII.txt:1782, :1775 | not stated |
| 0x3b | MIPS64 | reserved `*` | RI | mips64_volII.txt:2048 | yes |
| 0x3e | MIPS I | reserved `*` | **RI** | mips-iv.txt:1372 (row 7), :1415, :865 | **no**: candidate gives CpU CE=2 |
| 0x3e | MIPS II/III/IV | SDC2 | CpU CE=2 | mips-iv.txt:1380, :1388, :1396, :869; mips_r4000.txt:5384, :5380 | yes |
| 0x3e | MIPS32/64 | SDC2 (T/θ) | same as 0x32 | mips32_volII.txt:1365; mips64_volII.txt:1477, :2048 | yes when CU2=0 |

**The R4000 question: 0x33 and 0x3b are reserved (`*`), so Reserved Instruction.** Four independent readings agree:
1. Rendering PDF page 649 (manual page A-181) with layout puts the `*` at character column 42, directly under the "3" column header, on the `6 LL LWC1 * LLD` and `7 SC SWC1 * SCD` lines.
2. In the run-together line 5823 each row comes out as a left-to-right group: "LWC1 LWC2 *", "SWC1 SWC2 *", "COP1 COP2 *". Every other cell of rows 6 and 7 is a named instruction elsewhere in that line, so column 3 is the only cell left for the `*`.
3. The instruction pages list only coprocessors 1 and 2: LWCz at :5111-5112, SWCz at :5595-5596, LDCz at :4976-4977, SDCz at :5383-5384. COPz lists COP0–COP2 (:4674-4678). The words LWC3, SWC3 and COP3 do not appear anywhere in the file.
4. The MIPS IV manual agrees: mips-iv.txt:1388 and :1426, and :1365 names "R4000 … R4400" as MIPS III parts on which the coprocessor 3 instructions "cause a Reserved Instruction exception".

No other mark (δ/φ/ξ/χ) sits on those cells.

**LDC2/SDC2 on MIPS I: yes, Reserved Instruction.** The MIPS I table (mips-iv.txt:1372) shows 0x36 and 0x3e as `*`. The IDT manual never mentions LDC2 or SDC2 (0 matches); it treats ldc1 on R30xx parts as an assembler macro (`idt_r30xx.txt:1648-1667`) and has no opcode table. The fork already makes LDC1/SDC1 and LL/SC Reserved Instruction below MIPS II (`cpu_mips_instr.c:5526-5531`, `:5471-5474`). LDC2/SDC2 should follow the same pattern.

**What the manuals do not settle**
1. **0x3b (SWC3) at MIPS I.**
   - IDT, on the SWCz page: "Execution of the instruction referencing coprocessor 3 causes a reserved instruction exception, not a coprocessor unusable exception" (`:18335-18336`). The same page's exception list names only "Coprocessor unusable" (`:18356`).
   - The MIPS IV manual's MIPS I table and π rule give CpU instead (`mips-iv.txt:1372`, `:1447`).
   - IDT contradicts itself elsewhere too: MFC3 is RI (`:17411`), but COP3, CFC3, MTC3 and LWC3 list only CpU (`:16568-16571`, `:16537`, `:17535`, `:17148`). So no line in either manual says LWC3 gives RI.
   - `mips-iv.txt:1369` says coprocessor 3 is "optional and implementation-specific in the MIPS I and MIPS II" levels, so both readings are allowed. No R2000/R3000 manual from MIPS itself is in the local set.
2. **0x33/0x3b at isa_level 2** (R6000, Allegrex). A native MIPS II CPU gets CpU CE=3, while MIPS II-only mode on a MIPS III/IV CPU gets RI (`:1365`). There is no local manual for either part.
3. **0x3b at MIPS32 before Release 6.** The Rev 6.04 table cell shows only PCREL (`:1782`). Its "no marking" rule says that before Release 6, RI "was not necessarily required" where no `*` is shown (`:1775`). MIPS64 Rev 2.50 marks the same cell `*` (`:2048`), which is the natural reading, but the MIPS32 file itself does not say it.
4. **Coprocessor 2 loads/stores with CU2 = 1 and no coprocessor 2.** MIPS I–IV say the result is undefined (`mips-iv.txt:612`). MIPS32/64 Volume II says RI (`mips32_volII.txt:1780`, `mips64_volII.txt:2039`). Whether CU2 can be set at all without a coprocessor 2 is a Volume III question, and no Volume III is in the local set. The fork's existing COP2 arm raises CpU without looking at CU2 (`cpu_mips_instr.c:5123-5130`).
5. **CE on MIPS32/64.** Volume II never defines Cause.CE. CE=2/3 rests on the R4000 definition (`:1005`) and the IDT one (`:2462-2465`).
6. **No local manual** covers the R5900 (where 0x1e is LQ), the VR41xx entries, or Allegrex.

**Adjacent, outside the eight opcodes.** Coprocessors 2 and 3 are never allocated (`cpu_mips.c:262-263`), so the committed COP3 arm gives CpU CE=3 for opcode 0x13 on every level (`cpu_mips_instr.c:5136-5142`). The manuals disagree with that:
- The R4000 table and the MIPS III table mark 0x13 `*` (Reserved Instruction): PDF p.649 row 2, and `mips-iv.txt:1426` ("*(was COP3)").
- MIPS IV and MIPS64 reuse 0x13 for COP1X, a floating-point instruction class (`mips-iv.txt:1396`, `mips64_volII.txt:2044`).

If the candidate's CE=3 arm for 0x33/0x3b was modelled on this one, it inherits the MIPS III error.

**Method.** I created, edited and deleted no files, and built nothing. Besides grep/awk/od on the text extracts, I read the PDFs directly in two ways:
- **Symbol glyphs.** The extracts render symbol-font glyphs as control bytes. I decoded them from each PDF's font table (its `/Differences` list, found with `grep -a`).
  - In `mips-iv.pdf`, byte 0x12 is an asterisk (`asteriskmath`), not the "cross" mark, which means an undefined result. So the 0x13/0x33/0x3b cells in the MIPS III and MIPS IV tables are true Reserved Instruction cells.
  - In `mips64_volII.pdf`, JALX and MDMX carry ε (code 16) and the four coprocessor 2 loads/stores carry θ (code 14).
- **Column positions.** I ran `pdftotext -layout` to stdout only, on R4000 page 649 and MIPS IV pages 193–197.

One asterisk in MIPS IV Table A-40 (cell 0x1c) is missing from both renderings. Table A-41 (`:1404`) shows all four cells 0x1c–0x1f as `*1`.
