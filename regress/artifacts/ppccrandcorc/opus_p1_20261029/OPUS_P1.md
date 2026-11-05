# opus575 pass-1 seat (agent a6a11d09f46e1e1df).  Final text 2026-10-30T04:52:56.854Z (2026-10-29 23:52 local) by claude-opus-5-5, the only model on every assistant turn; banked 2026-11-05 at the #575 landing from the subagent transcript (it was never saved to a file, and the pass-1 ruling, adj_p1_20261105/MYTHOS_local.md, names six seats -- codex, grok, GLM, kimi, deepseek, minimax -- and never this one).  The seat re-ran the frozen witness probe on /tmp/gx575/base/gxemul (_scratchpad/r575_ppccrandcorc/opus_pass1/opus575_check.out: 48/58, CONTROL=OK).  Its prompt pointed it at _scratchpad/r575_ppccrandcorc/pass1_brief.md (the brief the panel received) with the liveness token OPUS_SEAT_ALIVE_20261029_575.

OPUS_SEAT_ALIVE_20261029_575

`# CHECKPOINT -- 2026-10-07 11:3x RUNNING (087a90 sections rewritten; the peer's sections below are untouched)`

VERDICT: SHIP-WITH-CHANGES -- both proposed expressions match Book I (two manuals checked, tables walked, HEAD reproduced at 48/58); the detector needs aliased-destination rows, per-handler BT edges and a measured operand order before it ships, and the round should cite the already-filed `ppccrlogicshift`.

**Baseline, checked myself.** `GXEMUL-SEC/src/cpus/cpu_ppc_instr.c` has md5 `2015e243` and is clean in the working tree; its last commit is `cb21331c`. The handlers (`:2707-2769`) and the decode arm (`:4541-4558`) match the brief word for word. I re-ran the frozen probe (`35b9c248`) against `/tmp/gx575/base/gxemul`. That binary is dated 10-29 23:34 and its source 10-25, md5 `2015e243`. Result: **48/58, CONTROL=OK, sentinel present.** The 10 failing rows are exactly the brief's 10 DISC rows.

### Q1. Premise audit
- **P1: true, checked in two manuals.**
  - Book I `:1909` gives `CRBT ← CRBA & ¬CRBB` and `CRBT ← CRBA | ¬CRBB`. The prose at `:1911-1914` puts the complement on BB.
  - The 2001 PEM agrees on its own: crandc at `ppc_pem32_rev2_2001.txt:17439`/`:17447`, crorc at `:17738`/`:17746`.
  - I walked all 16 cells of the section-2 table and every one is right. Over (00, 01, 10, 11), `ba & !bb` gives 0,0,1,0 and `ba | !bb` gives 1,0,1,1, which is Book I exactly.
  - The xo values agree with both `opcodes_ppc.h:53-63` and Book I.
  - Minor wording point: section 2 is called "verbatim", but the extracted text has no arrow, and only the complement glyph is disclosed.
- **P2: true, checked.**
  - `instr(crandc)` and `instr(crorc)` occur only at `:4550`/`:4553`.
  - The translator has no instruction-combining path; "combin" appears only in comments (`:32`, `:91`).
  - `mode` is always set to `MODE_PPC` (`cpu_ppc.c:96`) and nothing sets `MODE_POWER`. The CR arm of the disassembler (`cpu_ppc.c:811-833`) ignores the `power` flag.
  - POWER would want the same function anyway. PEM Appendix B.7 (`:44601-44602`) says POWER runs these instructions "normally" and differs only when LK=1.
  - Book I §1.5.2 (`:432-433`) says reserved instruction fields are ignored, so the decoder dropping bit 0 is correct.
- **P3: nothing depends on the current behaviour, checked.**
  - Gate 13 states "There is no PowerPC OS rig" (`gate_ppc.sh:15`), and its NetBSD kernel is loaded but "never executed" (`:246`).
  - The two hpcmips probes' `mvmeppc` sessions abort while the machine is being built, so they run no guest code.
  - No regress script except the new probe names these instructions or builds an opcode-19 CR word. The `129`/`417` hits in the rlwimi and rounding probes are a row count and FP values.
- **P4: yes after the fix; on HEAD the PIN rows carry the proof.**
  - After the fix, every truth row passes only if the instruction actually wrote the bit, because each destination starts at the inverse of the Book I result.
  - On HEAD, a DISC row starts at exactly HEAD's wrong value, so it reads the same whether or not the handler wrote. What shows that HEAD computes NAND/NOR, rather than skipping the write, is the PIN rows, which do flip their starting values.
  - **Gap:** the probe's docstring says the five sibling instructions also check "the encoder". All five are symmetric in their two inputs, so they cannot detect BA and BB swapped by the encoder. The encoder is right by reading (Book I `:1905-1907`), but that is not measured.
  - Cheap fix: the probe already captures the disassembler's operand text (regex group 3), and `score_table` throws it away. Comparing it against the intended `BT,BA,BB` would measure operand order through the tree's own decode (`cpu_ppc.c:819-821`).

### Q2. Smallest breaking edit that still scores 58/58 (described as coverage gaps)
1. **Source-field width.** Every source the probe uses is CR bit 0-5. A one-character narrowing of the BA or BB field decode, to any width that still covers 0-5, leaves **all 58 rows green**. For example `64 crandc 10` reads bits 0-1 and cannot see it. Clause (e)(3) already discloses this, so it is coverage debt, not a breach.
2. **The BT edge rows are split between the handlers.** Bit 0 is tested only on crandc and bit 31 only on crorc. crandc's destinations are 0 and 8-11, so narrowing crandc's BT decode to anything that still covers 0-11 also scores 58/58.
   - Clause (e)(3) says the edge rows pin bits 0 and 31. That is true of the probe but not of either handler alone.
   - Fix: give each handler both edges, which is two rows in the existing edge session.
3. **The most consequential gap: reading the sources before clearing the destination.** No row has the destination bit equal to a source bit (destinations are 0, 8-27 and 31; sources are 0-5). So moving the clear above the two reads also scores 58/58. That is the kind of change a tidy-up or option (iii) would make.
   - Aliased forms are ordinary code: Book I's own `crclr`/`crset` write a bit that is also a source (`:1870`, `:1898`).
   - This gap is **not disclosed** in clause (e).
   - Row to add, one per handler: BT = BB, with the BB input set and the Book I result clear. That is crandc with a=1, b=1 and crorc with a=0, b=1.
   - On that row, a handler that skips the write and one that clears before reading both end up with a 1, so both fail the row.
   - The cell has to be picked this way because the destination is also an input, so the "start at the inverse" trick cannot be used.
   - Both rows give the same answer under HEAD's NAND/NOR, so they pass at HEAD.

### Q3. Option set
- **(i): keep it, with the logical `!`.** A bitwise complement of a 0/1 value is never zero, so in crorc it would make the condition true for every input.
- **(ii): out.** It is already filed as `ppccrnandundec` (`OUTSTANDING_BUGS.md:25582`). It needs a new decode case and a new expected-value function, so it fails the round-scope rule.
- **(iii): reject.** It rewrites five correct handlers with no measured benefit, and it is the change most likely to hit gap 3 in Q2.
- **(iv): out, and already filed** as `ppccrlogicshift` (`:23385`). The brief does not cite it.
  - The shift appears 14 times, exactly the clear and set lines of the seven handlers.
  - The fork's own precedent is the `(uint32_t)` cast in `mcrf` one function up (`:2697`, from commit `8dd86b5a`).
  - `build-asan` is built with `-fsanitize=address,undefined`, and this probe's `edge crandc bt0` row executes `1 << 31`. Running the probe on an ASAN build is therefore a likely witness for that row. This is a prediction; I did not run it.

### Q4. Floor plan
- **(a)** Reproduced above.
- **(b)** Right shape. I enumerated it: each reinstated handler scores 53/58, with exactly the 5 rows the brief names failing. The 32-bit table is required: the file is `#include`d twice (`tmp_ppc_tail.c:63`, `:118`), so each source line exists as two compiled copies.
- **(c)** Right form. Enumerated: an identity body scores 40/58, with the 16 truth rows and 2 edge rows failing.
  - Predicted from the source, not run: `/bin/true` scores 5/58 with CONTROL=FAIL.
  - A missing binary makes gate 13 SKIP via `need_exec` (`:103`). Record that as the gate's shared SKIP, as `:180-181` already does for rldicl.
- **(d)** No predicate dominates the edited `if`, and the guarded body reads only `bt`.
  - Because `ba` and `bb` are each 0 or 1, the expression is a function of two bits, and the truth rows cover its whole input range at both sites and both widths.
  - So any edit to the expression that changes the function fails a truth row, and any that does not is equivalent. Record it as "by construction", with the brief's two variants as measured instances.
  - Enumerated: each of those variants scores 54/58. The (0,1) and (1,0) rows fail at both widths, and the edge rows pass.
  - One edit form the rule names falls outside this argument: bringing `bt` into the condition. Give it a one-line disposition in `PRETABLE.out`.
  - Suggested clause (e) wording: (ba, bb) EXHAUSTED. BT SAMPLED: crandc 0 and 8-11, crorc 12-15 and 31. BA SAMPLED {0,1,2,4}. BB SAMPLED {0,1,2,3,5}. The LK=1 form has no row; its decode is correct per §1.5.2.

### Q5. Gate wiring
The rlwimi block shape (`:113-135`) with 58/58 pinned by equality and CONTROL=OK is enough for the totals. Three additions:
1. **Per-row named checks**, as the dsform block has (`:234`), at least for the 18 rows that carry the fix plus any rows added. A row that is renamed, or replaced by another passing row, leaves the totals unchanged.
2. **Place the block before the `need_file` at `:243`**, so a missing NetBSD image cannot turn a failing detector into a SKIP.
3. **Records:** disclose the `need_exec` SKIP, and add #575 to the gate's `gate_begin` title (`:98`).

### Something else
- **Seat ledger:** `panel_pass1.launch.log` gives agy's reason as the 2026-08-30 reservation, which CLAUDE.md marks as superseded; the live reason is the owner's 2026-10-26 hold. Its `kimi=` field is empty, so this pass's kimi seat is the packet-fed `kimi-k3:cloud` substitute.
- **Post-fix clone:** the working tree holds someone else's uncommitted `src/cpus/cpu_alpha_palcode.c`. Build the post-fix clone from the archive, as the HEAD clone was, so the two binaries differ only in `cpu_ppc_instr.c`.

I wrote only under `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\r575_ppccrandcorc\opus_pass1\`: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\r575_ppccrandcorc\opus_pass1\opus575_check.out` (my 48/58 run) and `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\r575_ppccrandcorc\opus_pass1\copy_out.sh`. Nothing under GXEMUL-SEC or any build tree was changed.

VERDICT: SHIP-WITH-CHANGES -- both proposed expressions match Book I (two manuals checked, tables walked, HEAD reproduced at 48/58); the detector needs aliased-destination rows, per-handler BT edges and a measured operand order before it ships, and the round should cite the already-filed `ppccrlogicshift`.
