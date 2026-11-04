# mipsprimundec -- the v3 review, and a measured alternative for the disputed D1 cell (2026-11-04 04:44-05:0x)

Recorded by the main loop (Opus 5.5).  **No ruling here**: the design ruling is Fable's (`web/4_mipsprimundec.md`, waiting on Claude
Code Cloud); this file collects what the v3 review found, what the main loop CHECKED against primary sources, and one measured
alternative, so the ruling has them.

## 1. The seats (panel dir `_scratchpad/panel_20261104_044334_v3r_mipsprimundec/`)

| seat | answer | verdict | end line |
|---|---|---|---|
| Grok 4.7 xhigh (file-reading) | `grok.txt`, 11,676 b | V3-NEEDS-CHANGES | `GWEBV3RMPU: 4 FINDINGS 1 CHANGES-OWED 9 ROWS` |
| GLM 5.3 (packet-fed) | `ollama_glm.txt`, 11,658 b | V3-STANDS | `GWEBV3RMPU: 6 FINDINGS 3 CHANGES-OWED 11 ROWS` |
| Gemini Argon (packet-fed) | `gweb/jobs_20261103_adj/mipsprimundec_v3r/gemini_web.out`, 4,691 b (banked by the 04:5x cycle) | V3-STANDS | `GWEBV3RMPU: 6 ATTACKS 0 BROKEN 6 HOLDS 0 UNSETTLED DRAFTABLE:YES` (the gweb wrapper's own tag format) |
| GPT-6 Astra (file-reading) | -- | PENDING: walled until 08:24; a one-shot re-fire is set for 08:47 | -- |
| Opus 5.5 | -- | NOT FIRED: two Opus seats were stopped by a safety classifier on these bugs today | -- |

Both answering seats agree that V3-1 and V3-2 are implemented as the consensus stated, that the five measured cells are real, and that
the ISA II side of the new LDC2/SDC2 gate is unobservable (no ISA II CPU reaches translation).  They split on ONE cell pair:

* **Grok:** the LWC3 / SWC3 arms carried from the draft raise Coprocessor Unusable (CE = 3) on the R4400, but on MIPS III those
  encodings are Reserved Instruction -- "D1 should have been in v3".
* **GLM:** agrees with the architecture ("my own REASONED reading agrees (CP3 was withdrawn at MIPS III)") but keeps the cell out of v3
  on process grounds: "folding any into v3 would smuggle the ruling into the consensus carrier".
* **Argon:** the same split as GLM -- the R4400 `0x33`/`0x3b` cells are "architecturally incorrect" (`CPU/11/ce=3` where MIPS III requires Reserved Instruction), but they "correctly remain as originally drafted, because this is an intermediate consolidation step, not the final design ruling".

So all three answering seats read the architecture the same way; they differ only on whether the v3 or the ruling should carry it.

## 2. CHECKED by the main loop against local primary sources (a check, not a ruling)

* **MIPS IV Instruction Set, rev 3.2** (`_scratchpad/mips-iv.txt`): `:1366` -- the never-implemented Coprocessor 3 instructions "were
  removed or changed to another use starting in MIPSIII"; `:1372` (MIPS I map) and `:1380` (MIPS II map) list `LWC3` / `SWC3` in rows
  6 and 7; `:1388` (MIPS III map, Table A-39) reads `LL LWC1 LWC2 [empty] LLD LDC1 LDC2 LD` and `SC SWC1 SWC2 [empty] SCD SDC1 SDC2 SD`
  in this extraction; `:1447` (the key) -- kappa: "This opcode is removed in a later revision of the architecture.  If a MIPSIII or
  MIPSIV processor is operated in MIPSII-only mode this opcode will cause a Reserved Instruction exception."
* **R4000 User's Manual** (`_scratchpad/mips_r4000.txt`), the manual for the R4400's family: `:5823`, Figure A-2, the row fragment
  `LWC1 LWC2 * SWC1 SWC2 *`; `:5834`, its key: "Operation codes marked with an asterisk cause reserved instruction exceptions in all
  current implementations".
* So both local manuals read the R4400's `0x33` and `0x3b` as **Reserved Instruction**.  (The MIPS III table's empty cell carries no
  legible mark in this extraction; the R4000 map's `*` does.)
* **`machine_pmax.c:81` and `:170` allocate `coproc[3]`** (an R2020 / R3220 write-back memory unit), so the v3 (and draft) comment "no
  COP3 is modelled" is false as written.  What LWC3/SWC3 should do on pmax with Status.CU3 set is the disputed D2, unchanged.
* `v3.diff` is 53 added and 8 deleted lines; `MEASURED.md` said "56 changed lines" (the non-blank count) and is corrected in place.

## 3. v3b -- the D1 cell resolved as the manuals read, MEASURED (an alternative, not adopted)

`apply_v3b.py` (applied after `apply_v3.py`): SWC3 is Reserved Instruction from ISA III on (`isa_level >= 3`, was `>= 4`); LWC3 gains
an ISA III arm that is Reserved Instruction; through MIPS II both stay Coprocessor Unusable CE = 3.  Its comments are rewritten to be
true as written (no "no COP3 is modelled"; the CU3 simplification is stated).  `v3b.diff`: 64 added, 8 deleted.

`RUN_V3B.log` (`run_v3b.run-050000.sh`, own clone `/tmp/gxmain_mpu3b`, removed): make rc 0, 0 warnings, binary fresh.

| run | result |
|---|---|
| `probe_v3b.out` | 80/80, CONTROL OK, SYMPTOM ABSENT -- the probe's `exc` rows accept ExcCode 10 OR 11, so it cannot see the D1 difference |
| `table_v3b.out` vs `table_v3.out` | exactly TWO cells change: R4400 `lwc3` and `swc3`, `CPU/11/ce=3` -> `RI/10/ce=0`.  R3000, 5KE and 24KEc rows identical |
| R5000 (ISA IV), `table_head_5cpu.out` (HEAD) | every word STOPs the CPU except lwc3 (PREF) |
| R5000, `table_v3b.out` | jalx RI, mdmx RI, lwc2/ldc2/swc2/sdc2 CpU CE=2, lwc3 PREF, swc3 RI.  (v3 and v3b differ only at `isa_level == 3`, so v3 gives the same R5000 row -- READ, not measured) |

## 4. What the reviews say the detector will owe (for after the ruling)

* EXACT ExcCode and CE per cell -- the witness probe's `exc` rows accept 10 or 11 and so cannot see V3-1 (R3000 `ldc2`/`sdc2`) or D1
  (R4400 `lwc3`/`swc3`); grok and GLM both name this.
* R5000 `swc3` = RI catches a gate written `> 4` (GLM row 7); 24KEc `ldc2` = CpU CE=2 catches `x64` set on LDC2/SDC2 (grok); the
  R4400 D1 pair, whichever way it is ruled.
* Disclosed as unobservable: the ISA II cell (`< 2` vs `<= 2`), every R5900 row, CU2 = 1 / CU3 = 1 states, user mode, the pmax and arc
  rig machines.
* At implementation, whatever is ruled: **every product comment true as written** -- GLM F3 (the v3 comments state the contested ISA
  boundaries as fact) and grok's D2 note (the false "no COP3 is modelled").

## 5. For the adjudicator

Choose v3 (the draft's CpU CE = 3 on ISA III) or v3b (RI on ISA III, as both local manuals read) for D1; the rest of v3 is common to
both.  The UNSETTLED items in grok's consolidation (U1-U5) are unchanged.
