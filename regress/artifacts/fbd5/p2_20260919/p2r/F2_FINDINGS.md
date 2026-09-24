# #545 (fbdeclinefive) -- F2 adjudication-pass findings, consolidated

Written 2026-09-19 as a read-only records task. Nothing was built or run.
- Brief: `_scratchpad/fbd5/p2r/brief_fbd5_f2.md`, which describes the 149-row differential.
- Seat answers: `_scratchpad/panel_20260919_131006/`, plus the Opus seat at `_scratchpad/fbd5/opus_f2_20260919/OPUS_F2_ANSWER.md`.
- Closure is judged against the CURRENT tree: `GXEMUL-SEC/regress/diff_footbridge.c` has 327 rows, and its class-closure block X6/X7 starts at `:826`.
- The measurements are in `_scratchpad/fbd5/impl/table4/TABLE4.log`, with a durable copy in `regress/artifacts/fbd5/table4_20260919/`.
- "Checked" below means I read the current `GXEMUL-SEC/` tree or its artifacts.

## Seat table

| seat | verdict line (quoted) | kind |
|---|---|---|
| codex (GPT-6, block after last `codex`) | "NO-GO" | READING (it also ran an in-memory check of the gate predicates against `diff_FIX.log`; no builds) |
| agy (Gemini 3.8 flash high) | "**VERDICT: GO-WITH-CHANGES**" | READING |
| grok 4.6 | "VERDICT: DO NOT SHIP THE DETECTOR AS-IS. Product change still sound. Repair's own floor is not closed: X4's named `&& irq_enable` mutant is live on every write-decline, and X3's widened "legal writes re-arm no latch" row is CHANNEL-vacuous against `if (idata)`." | READING |
| kimi (CLI) | none. It hit `403 You've reached your 5-hour usage limit` mid-answer. Its body is partial reasoning; I read it and credit its findings below. | READING (partial) |
| ollama_glm | "VERDICT: UPHOLD THE PRODUCT CHANGE AND THE REPAIR'S SUBSTANCE, BUT THE COMPOSITE FLOOR IS LOWER THAN SECTION 2 CLAIMS ..." | READING (packet-fed) |
| ollama_deepseek | "VERDICT: UPHOLD with one concrete unbuilt floor escape (Q2) and one weak sub-check (Q3); no accepted disposition is demonstrably wrong from the packet ..." | READING (packet-fed) |
| ollama_minimax | "VERDICT (READ). Brief is internally consistent. ..." (no GO/NO-GO word) | READING (packet-fed) |
| ollama_kimi (kimi-k3:cloud) | "VERDICT: The repair cross-checks cleanly where the packet allows checking ... but the floor is NOT closed: ..." | READING (packet-fed) |
| Opus 5 (measuring seat) | "VERDICT: DO NOT CLOSE THE REPAIR CHAIN. 11 of 14 one-edit mutants of the FIXED dev_footbridge.c pass the SHIPPED composite (diff_footbridge.c 149/149 AND footbridge_sites_probe.py 37/37)." | MEASUREMENT (15 offline and 15 guest builds, scratch trees restored) |

Fable: not on this roster (held by the owner, per the brief).

**No seat found a defect in the product change.** Every blocking verdict is about the DETECTOR.

---

## Findings

### CLOSED-BY-X6X7

**G1. `&& irq_enable` / `&& fiq_enable` on a WRITE-decline guard escapes. X4 zeroes IRQEnable only at the read site.**
- Seats: codex, grok, agy, glm, deepseek, ollama_kimi, kimi CLI. Opus MEASURED it as F1b and F1c: 149/149 and 37/37.
- minimax's candidate-1 variant (`&& (irq_status & BIT)`, where BIT is set in the seeds) is the same class.
- It is also the challenge to disposition **F7/R1** ("X4 closed `&& irq_enable`"). grok and kimi said OVERTURN; codex and agy said REFINE. The challenge was correct against the pass-2 tree.
- Closed by X6's **all-zero state** cells at every write site, for the first access, at every width and both data values.
- Table 4: F1b red on `X6 write IRQ_STATUS ... all-zero` and `X7 IRQ Set write`. F1c red on `X6 write FIQ_STATUS` and `X7 FIQ Set write`.

**G2. A NONZERO legal enable write that re-arms a latch escapes. X3's widened writes all carry 0.**
- Seats: every seat. It is the brief's own candidate 3. Opus MEASURED F3 and F3b as escapes.
- It is also the challenge to disposition **F4** (codex OVERTURN; agy and grok REFINE).
- Closed by X7's `LW[]` cells, which write both 0 and 0x70 to IRQ/FIQ Set and Clear, from both states.
- Table 4: F3 red (`X7 IRQ Set write`); F3b red (`X7 IRQ Clear write`).

**G3. A legal read that re-arms a latch only when it reads ZERO escapes. The X3 reads were only at nonzero seeded values.**
- Seats: Opus measured F5 (escaped). F5b was killed only by guest N1.
- Closed by X7's all-zero-state legal-read cells at widths 1, 2 and 4.
- Table 4: F5 and F5b red on `X7 legal len 1/2/4 r...`.

**G4. A narrow or first decline that changes a register field escapes. X1 checked only the announce.**
- Seats: Opus (F4, F4b, F4c measured escapes), agy, glm, kimi CLI, ollama_kimi, codex.
- deepseek's variant belongs here too: X4 pre-zeroes irq_enable at the read site, so it cannot see a decline that CLEARS irq_enable.
- Closed by X6's `XSAME` (all four fields unchanged) in every cell. The seeded-state read cells cover deepseek's variant.
- Table 4: F4 red (`X6 write FIQ_STA`), F4b red (`X6 read IRQ_ENAB`), F4c red (`X6 write IRQ_RAW`).

**G5. A repeated or narrow decline that changes the interrupt output escapes. Only the first word decline counted asserts and deasserts.**
- Seats: Opus (F2, F2b measured escapes), agy (Q4.1), codex, glm, minimax (candidate 2), ollama_kimi. The brief's own candidate 2.
- Closed by X6's `irq_asserts == a0 && irq_deasserts == d0` in every cell, including the repeat.
- Table 4: F2 red (`X6 write IRQ_STA`, 12 failures); F2b red (`X6 write FIQ_RAW`).

**G6. The handler return code (rv) on narrow declines was unchecked.**
- Seats: agy (Q1 F6 REFINE; Q3), glm (Q4.2), codex (F6 REFINE).
- Closed by X6's `rv == 1` in every cell.
- **No table-4 mutant targets rv alone.** Closed by construction, NOT MEASURED.

**G7. A latched narrow +0x18c read returns `irq_enable`, i.e. the removed value.**
- Seats: Opus (F7b measured escape; F7 killed only by guest N3), codex (Q3.3).
- Closed by X6's read-site repeat cells, which `memset` 0xa5 and require 0 across the whole width.
- Table 4: F7 red and F7b red (`X6 read IRQ_ENAB`).

**G8. A latch assignment that does not latch on a zero or narrow first access (`d->warned_fiq_raw_w = idata;` or `= (len == 4);`), and no repeated narrow decline anywhere.**
- Seats: codex (its Q2 primary, one token, plus Q3.1), glm (Q4.3).
- Closed by construction by X6's **repeat** cells. They exist at data 0 and at len 1 and 2, and they require the announce delta to be 0 on the repeat. Under the mutant the repeat re-announces, so the cell goes red.
- **Neither mutant is in table 4.** Closed by construction, NOT MEASURED.

**G9. X1's narrow declined read was checked against a buffer that was not pre-poisoned. (minimax Q3)**
- X6 `memset`s 0xa5 and checks the full width.
- Table 4: A2 and Z8 red on X6.

### OPEN-DETECTOR-GAP

**G10. The offline gate pins count green LINES, not distinct row ids. This is the same class the round repaired in `gate_arm`.**
- Seats: codex, who DEMONSTRATED it in memory: with X5's preservation line replaced by a duplicate green X5 line, P stays 78, X stays 38 and PASS holds. grok, ollama_kimi and kimi CLI also raised it.
- **CHECKED-TRUE.** `gate_offline.sh:598-605` still uses `grep -cE '^  ok    P[0-9] '` = 78 and `X[1-7]` = 216. The new `X6` = 108 and `X7` = 70 pins are plain line counts too; none uses `sort -u`.
- Limit: a product mutant cannot duplicate a line, so this is a harness-edit hole only (kimi CLI's point).
- X6 and X7 row names are unique per cell, so a distinct-id pin is cheap.

**G11. The legal-read value WIDTH is unpinned: every seed fits in one byte.**
- Seats: codex (Q3.2: `d->irq_status & 0xff` in the IRQ_RAW_STATUS read passes everything), kimi CLI (X2's mask is vacuous), grok (says disclosed-class).
- **CHECKED-TRUE.** X2 and X6/X7 seed 0x18/0x30/0x60/0xc0, and X7 does not check read values.
- It is arguably outside the X6/X7 contract ("any other register's semantics"). But P0 and X2 claim to pin these read expressions, so either add a seed with a nonzero upper byte or disclose it.

**G12. The repaired `gate_arm` pins have never been run.**
- Seats: glm, ollama_kimi, codex (wants the run before sign-off). minimax and agy judged the pins sound BY READING only.
- **CHECKED-TRUE.** The only log is `regress/artifacts/fbd5/gate_20260919/gate_arm_545.log`, written at 11:57. `regress/gate_arm.sh` was modified at 12:46. That log has no `ROWS=37 of 37`, NO or C4 pin lines.
- The brief itself says "gate_arm ... NOT YET RUN".

### OPEN-WRONG-RECORD

**G13. The X4 header comment claims the `&& irq_enable` class. X3's widened row is named "legal writes ... re-arm NO latch" but drives only zero data.**
- Seats: grok (L4), Opus (Q3), agy.
- **CHECKED-TRUE.** `diff_footbridge.c:795-798` is unchanged. X4 still zeroes IRQEnable only at the read site.
- The class is now held by X6 and X7 (G1, G2), but neither the X4 comment nor the X3 row says so. Point both at X6/X7.

**G14. The sites probe still attributes width coverage to "P-rows", and still calls the N counts "ACCESS-LOCAL".**
- Seats: codex (Q4), grok (F20 REFINE).
- **CHECKED-TRUE.** `footbridge_sites_probe.py:104-107` says "rowed OFFLINE in regress/diff_footbridge.c (P-rows)". Widths are X1 and X6.
- `:259-260` says "ACCESS-LOCAL: each N row counts ITS text". The N rows count over the whole arm, as the header at `:101` now correctly says.

**G15. The #539 record correction promised under F34 is not in the tree.**
- Seat: codex.
- **CHECKED-TRUE.** `CHANGELOG.md` is unchanged versus HEAD. `git diff --stat HEAD -- CHANGELOG.md` is empty, and the tree has no `#545` block yet.
- Its text around `:227` still says #539's gate distinct-id check "now counts ids over the GREEN lines".
- This is owed in the #545 CHANGELOG block at commit time. It is not a false claim yet, but nothing is carrying it.

**G16. Table 3 had 35 mutants, not "34".**
- Seat: codex.
- **CHECKED-TRUE.** 35 distinct mutant ids besides FIX in the brief's `OFF` lines.
- **Addendum (mine, not a seat's):** `_scratchpad/CHECKPOINT.md:112` says table 4 had "all 50 mutants". `TABLE4.log` has **49** mutant `OFF` lines besides FIX: table 3's 35 plus Opus's 14. The same off-by-one, in the other direction.

**G17 (claim CHECKED-FALSE). glm: "the inlined diff has 21 hunks, not 22".**
- The brief carries 22 `@@` lines. Not a defect.

### DISPOSITION-CHALLENGE

**G18. R4 (row NO): REFINE.** Seats: codex (and its Q3.4), Opus (Q3, "disclose it").
- NO proves the ORDER of the texts, not which access emitted each one. A diagnostic emitted at a later access, but still in N1..N5 order, passes.
- **CHECKED-TRUE on the wording.** The header at `:101-103` and the comment at `:600-602` both say NO "binds each text to its own access". That overclaims.
- Remedy: disclose the limit in the contract, or attribute each text via the per-step segment, as codex suggests.
- agy, glm and ollama_kimi judged NO sound for text EXCHANGE. That is not in dispute: Z9 is red.

**G19. F40 (PRETABLE mtime correction): OVERTURN its remaining claim.** Seat: codex.
- `PRETABLE.out:119-120` says its mtime "proves the ORDER only for the text above the first `== TABLE 1` heading". The file was modified after table 1, so its mtime proves nothing about when any portion was written.
- **CHECKED-TRUE.** The line is still present (the file is 120 lines). It is a wrong record inside a correction.

**G20. F11 rationale ("their own verdict rows enforce them"): wrong as written.** Seat: glm.
- **CHECKED-TRUE.** No `gate_*.sh` or `run.sh` references `FBPENDING_VERDICT` or `FBDRAIN_VERDICT`, and the drain verdict is `REPORT-ONLY`.
- Restate F11 as "unenforced by design, disclosed". The disposition (disclose) stands.

**G21. F50 (DEVINIT memset "not rowed"): grok OVERTURNS; agy UPHOLDS.**
- grok's argument: arm S runs a real DEVINIT, so N1-N5 `count=1` pins the memset.
- **CHECKED:** DEVINIT is `malloc` plus `memset` (`dev_footbridge.c:791-792`), as grok says.
- **NOT CHECKED:** whether the guest actually reds with the memset removed. A freshly malloc'd block in a new process is usually zero, so the guest pin is at best probabilistic.
- I lean UPHOLD. It is not a reliable pin.

**G22 (CHECKED-FALSE). D2, glm: "the sites probe's H1 was left out of the no-prompt tightening".**
- `footbridge_sites_probe.py:546-547` requires `not H["prompt"]`, where `prompt = "GXemul>" in buf` (`:455`). That is no prompt anywhere in the buffer.

**G23 (CHECKED-FALSE). F8, glm: "M1's guest kill is unshown".**
- `killtable_20260919/TABLE2.log` has `SITES_M1 ROWS=21 of 36 ... FAIL`.

**G24 (CHECKED-FALSE). D6, ollama_kimi: "the SDRAM-pair mid-session death is unfiled".**
- It is filed as `fbsdrampair` (`ledger.json:46770`), and the probe names it at `:53`.

**G25 (CHECKED-FALSE as a challenge). F44, deepseek: "the product has no fiq_status writer" is suspicious.**
- There is no `fiq_status =` assignment in `dev_footbridge.c`. The premise holds.

**G26 (NOT CHECKED, minor). R2, minimax: `!idata` is killed by X1 (nonzero first write), not by X5.**
- So the disposition should read "X1 + X4" rather than "X4 + X5".

**G27 (claim CHECKED-FALSE). minimax, deepseek, ollama_kimi: "M9 was never measured on the guest".**
- `TABLE2.log` has `SITES_M9 ROWS=33 of 36 ... red: N1,N2,N0`. That run predates the NO row, and it has not been re-run on the current probe.

### OUT-OF-SCOPE / no action

**G28.** The `gate_arm.sh:1074` display grep omits `A2b`, because `A[0-9] ` cannot match `A2b `. (agy.)
- CHECKED-TRUE. Display only: `ROWS=37 of 37` still scores A2b.

**G29.** N and NO match the texts by substring, so an announce with extra text still passes. (kimi CLI.)
- ollama_kimi and minimax asked whether the TEXTS are pairwise substring-free. CHECKED-TRUE (`:261-265`), so NO fails closed on an ambiguous match.

**G30.** kimi CLI raised two pre-existing issues that #545 did not touch:
- A FIQ Set write that STORES instead of ORing is unobservable, because fiq_enable has no readback.
- `+0x288` (FIQ_ENABLE_SET) returns 0 silently on a read.

**G31.** glm: the differential reds a hardware-faithful `fiq_status == irq_status` implementation (7.3.30). This is intended and disclosed under F44; note it for any future conformance round.

**G32.** glm: NO reds on ANY unrelated fatal in arm S. That is brittle, but it fails closed.

**G33.** Opus F1 (`&& !timer_control[0]`) is outside the DEPENDS-ON bound. It is green offline (table 4 F1 is 327/327) and is killed only by guest N2, because arm S arms timer 1.
- The X6/X7 CONTRACT at `diff_footbridge.c:840-844` discloses exactly this.

---

## Counts

| class | findings |
|---|---|
| CLOSED-BY-X6X7 | 9 (G1-G9). G6 and G8 are closed by construction; no table-4 mutant targets them. |
| OPEN-DETECTOR-GAP | 3, all CHECKED-TRUE (G10-G12) |
| OPEN-WRONG-RECORD | 4 CHECKED-TRUE (G13-G16, plus the CHECKPOINT 49-vs-50 addendum), and 1 claim CHECKED-FALSE (G17) |
| DISPOSITION-CHALLENGE | 10 (G18-G27) |
| OUT-OF-SCOPE | 6 (G28-G33) |

The 10 disposition challenges break down as:
- **Stand, CHECKED-TRUE (3):** R4, F40, F11-rationale.
- **Contested (1):** F50, leaning uphold.
- **CHECKED-FALSE (5):** D2, F8, D6, F44, and M9-on-guest.
- **Minor, not checked (1):** R2.

The earlier challenges to **F4, F6 and F7/R1** were correct against the pass-2 tree. X6 and X7 now answer them (G1, G2, G6), and table 4 measured the kills for G1 and G2.
