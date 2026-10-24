# F3 -- the ADJUDICATION of round `#569`'s PASS 3 (the scoped repair-diff pass), for GPT-6 Astra (adjudicator; owner roster 2026-10-23)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

You adjudicated pass 2 (`pass2_20261023/f2/codex_t1f2.txt`: SHIP WITH THE NAMED REPAIRS) and the repairs were made and
measured (`repair1_20261023/`), then reviewed by the seats in section 1 on the pass-3 brief (`pass3_20261023/packet.md`:
the repair diff inlined, the receipts, the composite floor question).  **Rule whether the repair chain CLOSES** -- a
valid pass with zero breaches, its denominator stated -- or owes another repair.  You may open every file under
`regress/artifacts/m88kscaledbyte/` and the source under `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/` (the working tree
carries the uncommitted round files; `repair1_20261023/staged/gate_offline.sh` is the gate as it will be committed).  Do
not build or run anything.  VERDICT LINE FIRST: `VERDICT: <CLOSE | REPAIR AGAIN | DO NOT SHIP> -- <one sentence>`, then
one line per numbered item (`G1 UPHOLD` / `G3 AMEND: ...`), then your reasoning with file:line citations.

## 1. The seats

| seat | answer | verdict line |
|---|---|---|
| Grok 4.7 (xhigh, plan mode; file-reading) | `grok_t1p3.txt` (8,817 b) | CLOSE -- "the repair diff is the commanded comment, fallback, move, and index formula, and no edit inside the 54 contracted indices keeps all 123 rows green" (the producers' image re-derived from the source: 12 + 4 + 8) |
| GLM 5.3 (packet-fed) | `ollama_glm_t1p3.txt` (8,368 b) | CLOSE -- zero breaches over the fully enumerated contract; three record nits (G4-G6) |
| DeepSeek v4-pro (packet-fed) | `ollama_deepseek_t1p3.txt` (2,208 b) | CLOSE -- "the repair diff matches the ruling and the composite floor shows no in-contract edit that keeps all 123 rows green; inspected all 123 driver identities and 126 gate checks" |
| Fable 5.1 | `fable5.HELD.txt` | DELIBERATELY NOT FIRED (owner hold; question carried) |
| Gemini 4 Argon | `argon.NOT_FIRED.txt` | NOT FIRED (four failed controls today; a seat-failure class) |

Not on the owner's roster: agy, kimi, minimax, Opus-as-seat (the builder).

## 2. Findings and the main loop's dispositions

| # | finding (seat : line) | disposition |
|---|---|---|
| G1 | DeepSeek `:1-4`: CLOSE; the repair diff is exactly R1-R5 + F25; R3's 12 + 4 + 8 enumerated by `R3_SOURCE_READING.out`; the 123 identities and 126 gate checks unchanged by the move; placement trade-off right. | UPHOLD. |
| G2 | DeepSeek `:7`, `:16` NOT CHECKABLE from the packet: (i) `.gitignore:33`; (ii) the 359 baseline at `1329d894`; (iii) the staged driver's mode. | CLOSED by the main loop: (i) HEAD's `.gitignore` line 33 is `regress/diff_*` (read 2026-10-23); (ii) `_scratchpad/nightly/verdict_20261004_180001.txt` records `HEAD=1329d894`, `TREE_DIRTY=YES` (its dirty list names neither `gate_offline.sh` nor `diff_wdc_identify.c` -- the pass-2 drafter's reading, `pass2_20261023/drafter_NOTES.md` #1) and gate 2 PASS, the 359 count in that battery's log (`battery_20261004_180001.log:2325`); `1329d894` is the last commit touching either gate file (`git log`, 0 later commits); (iii) the mode is a LANDING attestation: `git ls-files -s` after the commit must show `100755`, recorded in the follow-up records commit. |
| G3 | GLM `:1-11` (8,368 b): CLOSE, with the denominator enumerated (the 54 cells per artifact, the 5 structural shapes per side, cmp, the 4 status rows, the sentinel, 123/126); R3's 12/4/8 re-derived over the producers' domains (`:19`); R4's sum form reproduces every roster index (`:21`); the diff decomposes to exactly R1-R5 + F25 (`:23`). | UPHOLD. |
| G4 | GLM `:11` (1): the pass-3 brief's S5 said "every line after it moved by +4" -- false for the working tree: HEAD -> pass 2 was +4, R3 added +2, so +6. | RECORD (a brief premise, not a product record): noted here; no file changes. |
| G5 | GLM `:9`, `:11` (2): Q4's premise that "the CHANGELOG `#569` block already names ..." is contradicted by S0 (no such block in HEAD or the working tree). | RECORD: the sentence meant the landing DRAFT (`t1/landing/changelog_569.md`, which carries those items); the block lands with the commit.  GLM is right that it is an obligation, not a fact. |
| G6 | GLM `:11` (3): `REPAIR_REPORT.md` section 1 lists M1 at 11:48 while `M1.out` / `M1_cc_cases.out` are stamped 12:02:54 -- "an unrecorded re-run or a timeline error". | CHECKED by the main loop (file stamps and the report's timeline, below); disposition in G6a. |
| G6a | The main loop's check: `M1.out`, `fixed_r1.out`, `M1_cc_cases.out` are stamped 12:02:54-56 (after M4's 11:58-12:02 rebuilds); the report's row says 11:48. The content is the repaired driver's (md5 `7c888857...`), ROWS=123 FAIL=0, byte-identical to pass 2's `fixed.out`. | RECORD, corrected in place: a "Timeline correction" paragraph appended to `REPAIR_REPORT.md` (either a re-run after M4 overwrote the 11:48 files, or the row is a timeline error; the receipts are the 12:02 ones; the measurement stands).  Not a repair. |
| G7 | GLM `:19`: the decoder's twelve rest on the branch that makes byte LOADS unsigned-or-signed at `cpu_m88k_instr.c:~3585-3597` (not inlined; "NOT CHECKABLE" for a packet-fed seat; carried by the pass-2 settled premise S4). | SETTLED: `cpu_m88k_instr.c:3592-3600` (read 2026-10-23) -- the `(iword & 0xf800) == 0x800` arm clears signedness for the unsigned byte/half forms, the `else` arm keeps it for `ld.b` (`if (opsize >= 2 \|\| op == 1) signedness = 0;`), so the register-form decoder reaches signed and unsigned byte loads and the byte store: 3 kinds x 2 (.usr) x 2 (endian) = 12, as your F2 Q4 already established ("twelve sync decoder consumers"). |

| G8 | Grok `:1-7`, `:11-35`: CLOSE; R3's twelve/four/eight walked from the decoder's own branches (`cpu_m88k_instr.c:3592-3600`, the `.wt` rejection `:3606-3614`, the immediate form's forced `scaled = 0`/`user = 0` `:2368-2372`) and both endiannesses shown to be in the producers' image (`emul_parse.c:493-499`, `emul.c:737-743`, `file_elf.c:693-694`); R1 at `gate_offline.sh:187-232` between `:185` and `:234`; 126 `ok   m88k loadstore generator:` lines in the committed-form receipt. | UPHOLD. |
| G9 | Grok `:39`: `GATE2_committedform_tail.out`'s note says the run used the staged gate `faebdd85` while its inventory line shows the restored working-tree hash `2af22d40` -- "the report says the same thing: not a clean tree". | RECORD: the inventory line was taken after the restore; the receipt's own note names the staged md5 that ran.  The landing text names both: the staged gate `faebdd85...` ran; the working tree was restored to `2af22d40...`. |
| G10 | Grok `:49`: the carried claim that `MANIFEST.md5:5` still records `0735ace9...` no longer matches -- it now reads `1e3b3b30...` (refreshed by the main loop before this pass). | CLOSED: F15's manifest refresh is done; Grok could not recompute (shell denied) -- the main loop recomputed it at the refresh (27 entries). |
| G11 | Grok `:43`, `:47`: landing attestations -- `git ls-files -s` must show `100755` (WSL's `ls` mode is not that proof); the CHANGELOG block names M2's 485 on the dirty tree with staged gate `faebdd85`, M3's 502 on the working-tree gate `2af22d40`, `(c): measured at`, the four filed rows; commit the staged gate, not the working-tree gate. | ADOPTED in the landing (the mode proof lands in the follow-up records commit that names the landing commit). |

## 3. Questions
Q1. VERDICT, then per item: UPHOLD / AMEND / OVERTURN.
Q2. Does the chain CLOSE under the repair-chain rule (one valid pass, zero breaches, denominator stated), or is a further
    repair owed -- and if so, which L1-L4 licence?
Q3. The landing attestations: the driver added with `-f` at mode 100755; `regress/gate_offline.sh` committed as HEAD +
    the one hunk (`repair1_20261023/staged/gate_offline.sh`, md5 to be recorded); the peer's backup moved out of the
    artifacts; the row `held` with its question; the four filed rows; the two gate runs named with their trees.  Anything
    missing?
Q4. Anything else, with the file:line that settles it.
