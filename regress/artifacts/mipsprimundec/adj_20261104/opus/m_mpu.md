# m_mpu (agent add9f8383f95cb71a).  Final text 2026-11-04T08:18:05.513Z by claude-opus-5-5.

OPUS_SEAT_ALIVE_20261104_MMPU

VERDICT: INCONCLUSIVE. The draft is applied exactly and builds clean, but none of the per-word sessions ran. A safety classifier stopped my turn while I was reading the source to write the per-word driver. Following this project's recorded practice after a stop, I held the rest of the work and am filing it as owed. Nothing from the stopped turn ran.

**Measured (logs in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus_20261104\m_mpu\`)**

| item | result | artifact |
|---|---|---|
| Clone of `build/` | 15 MIPS-path files `cmp` equal to GXEMUL-SEC; no sentinel in `build/` | `s1.out` |
| Baseline rebuilt in the clone | make rc=0, binary newer than source; md5 `f4972320a381…` equals the copied `build/gxemul`, so `build/gxemul` rebuilds byte for byte from SEC's MIPS path | `s1.out`, `build_base.log` |
| Draft applied | 13 of 13 anchor lines matched. The packet's AFTER block matches 65 of 65 lines, with tabs expanded to 4 (the packet shows the file's tabs as 4 spaces). The diff's 42 +/- lines (+38/−4) match the packet's, in order. | `check2.out`, `draft.diff` |
| Draft build | make rc=0, no error or warning lines, `cpu_mips.o` recompiled, binary newer than source; md5 `2e4039a84b71…` | `s2.out`, `build_draft.log` |
| Cleanup | `/tmp/gxopus_mpu` removed (its sentinel was still in place) | `s9.out` |

`s2.out` ends with `APPLY_RESULT=NOT-EXACT`. That line is wrong: my checker had a bug (in Python `"" in "+-"` is True, so blank lines leaked in). `check2.out` is the corrected re-run and replaces it.

**Not measured, owed:**
- the repo probe on the draft binary;
- the word × CPU table (ExcCode/CE, EPC, PC) on the R4400, R3000 and 5KE;
- the PREF check on the 5KE;
- the delay-slot test on the R4400;
- the manual comparison.

I give no numbers for any of these, and none should be inferred from this answer.

**READ from source (GXEMUL-SEC):**
- **Base commit.** The packet names `87a73fdc`; HEAD is `ebe5af82`. `87a73fdc` is an ancestor of HEAD, and `git diff --stat` between them is empty over the nine MIPS-path files.
- **The second hunk is whitespace only.** It deletes the blank line after the SPECIAL3 `switch (s6) {` (old line 5600).
- **0x1e is left as it was.** The `HI6_LQ_MDMX` arm still goes to `bad`, as the packet says it intends, so the probe's `mdmx` rows must stay red on the draft. REASONED from the source, not measured.
- **LDC2/SDC2 are not ISA-gated.** The draft has no ISA test for them, while their sibling LDC1/SDC1 arm raises RI below ISA II (`cpu_mips_instr.c:5527-5531`) and `opcodes_mips.h:470,478` tags both as MIPS II. On the R3000 the draft should therefore raise CpU CE=2 where the sibling arm raises RI. REASONED; the MIPS I opcode table is unchecked.
- **The probe's parser cannot read a delay-slot row.** The debugger prints ` bd` between `(exccode N)` and ` ce=` (`cpu_mips.c:1634-1636`), and the probe's regex `\(exccode (\d+)\) ce=(\d+)` (`mips_primundec_probe.py:111`) will not match that line. A delay-slot row built on that parser would report exc = none.
- **Delay-slot mechanics.** `X(b)`/`X(b_samepage)` run the slot through `ic[1].f` under `TO_BE_DELAYED` (`cpu_mips_instr.c:359-401`). When `delay_slot` is set, `mips_cpu_exception` sets EPC = pc − 4 and BD (`cpu_mips.c:2138-2140`), and it skips EPC entirely if EXL is already set (`:2128`). So a word in the slot should give EPC = the branch with BD set. REASONED.
- **Cold R4400 Status.** The witness transcript `64_cpu2.txt` decodes it as `cu=3` (CU2 and CU3 clear), which is the precondition for CE=2/3.

**Manuals.** Sizes checked, all non-empty: `mips32_volII.txt` 775,072 bytes; `mips64_volII.txt` 500,193; `mips-iv.txt` 416,407; `mips_r4000.txt` 859,594; `idt_r30xx.txt` 1,071,238. The R4000 extract is not layout-preserving: its opcode table (`mips_r4000.txt:5823`) is one run-together line. The sequence `LWC1LWC2*SWC1SWC2*` suggests opcodes 0x33 and 0x3b are reserved (`*`) on the R4000, which would conflict with the draft's CE=3 on the R4400. The layout does not settle which cell is which, so this is UNSETTLED. I did not read the other four manuals.

**Seat ledger.** This is a partial seat: setup and build were completed, the measurement was not. Nothing was written to `build/`, `build-asan/`, `est/`, `GXEMUL-SEC/`, `/tmp/gx579` or `/tmp/gxsec-build`.
