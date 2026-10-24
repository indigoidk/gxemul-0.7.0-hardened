# PASS-1 DESIGN REVIEW -- round T1, ledger row `m88kscaledbyte` (GXemul hardened fork)
**Brief v1, COMPACT form (for a seat that cannot read files; it stands alone).**  Drafted 2026-10-22.
Tree under review: `GXEMUL-SEC/` at HEAD `cb2eba1e`.  Built from `GXEMUL-SEC/tools/BRIEF_TEMPLATE.md` (working tree).

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

**The project.**  GXemul is a computer-architecture emulator: a developer tool that runs legacy operating systems
inside a software sandbox.  This fork is a hardening effort -- ordinary software-correctness work on the emulator's
own C code: out-of-bounds accesses, missing checks, crash-on-unusual-input defects, and the regression tests that
keep them fixed.  The *guest* is a program or OS running INSIDE the emulator; the *host* is the emulator process on
the developer's own machine.  A *variant* below means a deliberately altered copy of the code, used to measure
whether a regression test notices the alteration (standard mutation testing).

**This pass.**  PASS 1: a design review BEFORE any edit.  The fix design for this round was adjudicated and AGREED
by two seats (section 3).  Your job is to check that design and the regression rows it owes.  The premises in
section 5 are settled -- re-open one only if you find it false, and then say so loudly.

**Hard limits.**  READ-ONLY.  Do not build, run, copy or modify anything in the repository.  No seat is asked to
design or run a guest-path reproduction for this round (section 2 says why).

**You cannot read files -- that is expected.**  Every fact you need is inlined.  Where a question needs a fact this
packet does not give you, write NOT CHECKABLE and name the fact; do not guess.  If your budget is short, answer Q1
and Q2 first; one paragraph per sub-question is enough.

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: READY | READY WITH CHANGES | NOT READY -- <one line>
Q1: <one line>   Q2: <one line>   Q3: <one line>   Q4: <one line>
~~~~
Then one section per question.  Mark each claim READ (you opened the source), DERIVED (from this packet) or NOT
CHECKABLE.

---

## 1. The defect -- as the ledger row and the queue describe it (VERBATIM)

Ledger row `m88kscaledbyte` at HEAD `cb2eba1e` (`tools/pipeline/ledger.json`), its fields rendered one per line, values
VERBATIM:
~~~~
id: m88kscaledbyte
sev: HIGH   state: open   opened: 2026-10-22   witness: none   commits: (empty)

title: cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP

state_note: QUEUE: external-research batch 1 of 10 (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md D).  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T1 (class HOST-STOP; reach U, user mode; effort: one-line + detector; report rows: A7-29, A7-30, A(c)#1).  Source URLs: https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415.  Our site at de8c7547: src/cpus/generate_m88k_loadstore.c:104-105, :254-257; src/cpus/cpu_m88k_instr.c:2357-2358, :2377-2395, :3608-3629; src/cpus/cpu_dyntrans.c:1906-1908.  Portable fix: yes -- port with a change: ajfa mvme187 4a01173 patch 01 makes scaled byte accesses unscaled but exempts xmem; which change closes the xmem slot is DISPUTED (below).  Filing check (TRIAGE.md): 0 hits for xmem / generate_m88k_loadstore / scaled-byte in OB or ledger; coordinator-confirmed.  Confirmed as classed by both adjudicating seats (regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md A).  Fix shape DISPUTED (D1): GPT-6 Astra -- xmem_slow rebuilds `scaled` from the instruction word, so dropping ajfa's `op != 3` exemption leaves the NULL call; repair the table by mapping the scaled-byte slots to the unscaled byte handlers, keeping the generation suppression; Grok 4.7 -- drop the exemption.  Pass 1 of the round settles it by reading cpu_m88k_instr.c:2357-2395 and generate_m88k_loadstore.c:254.  Do not port the exemption (F).  witness: none -- research finding, not yet reproduced here.
~~~~
**About that state_note:** it still says the fix shape is DISPUTED and that "pass 1 settles it".  The dispute was
SETTLED by the critical-items adjudication committed in the same HEAD (section 3).  This pass checks the settled
design; it does not re-run the dispute.  The `witness` field still reads `none`; section 2 records the attempt.

The queue, `OUTSTANDING_BUGS.md` at HEAD (VERBATIM) -- the row, and the sibling rows this round deliberately excludes:
~~~~
   28| > 1. `m88kscaledbyte` (HIGH, new) -- m88k scaled byte ld/st/xmem use NULL table slots; a user-mode xmem calls a NULL
   29| >    function in the host.  T1; the fix shape is disputed and pass 1 settles it.
  ...
25260| * **`m88kscaledbyte` (HIGH, open)** -- new.  cpus/generate_m88k_loadstore.c table + cpu_m88k_instr.c:X(xmem_slow) -- the
25261|   generator emits NULL for every scaled byte-size entry; scaled `xmem.bu rD,rS1[rS2]` calls that NULL pointer (host
25262|   SIGSEGV), scaled `ld.b/ld.bu/st.b` decode to `ic->f == NULL` (CPU stop) -- HOST-STOP.  TRIAGE.md T1; report rows
25263|   A7-29, A7-30, A(c)#1; port: yes (ajfa mvme187 4a01173).  Batch 1 of 10 (fix shape disputed; pass 1 settles it).
  ...
25557| * **`m88kxmemr0` (MED, open)** -- new.  cpus/cpu_m88k_instr.c:X(to_be_translated) xmem decode -- an xmem whose
25558|   destination is r0 is decoded as a NOP in both decoder forms, so the memory write half of the exchange and its access
25559|   semantics are dropped -- WRONG-RESULT.  ADJ_RULINGS.md C N1 (GPT-6 Astra); port: none found.
25560| * **`m88kxmemusr` (MED, open)** -- new.  cpus/cpu_m88k_instr.c:X(xmem_slow) -- the handler takes the .usr bit from 0x80
25561|   while the register-form decoder takes .usr from 0x100 and treats 0x80 as .wt, so an xmem's user/supervisor address
25562|   space follows the wrong bit -- WRONG-RESULT.  ADJ_RULINGS.md C N2 (GPT-6 Astra); port: none found.
  ...
25585| * **`m88kzeroword` (MED, open)** -- new.  cpus/cpu_m88k_instr.c -- instruction word 0x00000000 (`xmem.bu r0,r0,0`) is
25586|   sent to `goto bad` -- CPU-STOP (SVR4's IPL runs through zero padding).  TRIAGE.md T126; report rows A7-28; port: yes
25587|   (ajfa mvme187 4a01173).
25588| * **`m88kwtbit` (MED, open)** -- new.  cpus/cpu_m88k_instr.c ld/st register form -- the .wt bit (bit 7) halts ("wt bit
25589|   not yet implemented") -- CPU-STOP.  TRIAGE.md T127; report rows A7-31; port: UNVERIFIED (ajfa mvme187 4a01173).
~~~~

The external recipe the ledger names, as the research report describes it
(`regress/artifacts/research_20261022/A_github_forks.md`, VERBATIM):
~~~~
  153| **Source.** ajfa/mvme187-sysv88-gxemul, patch 01 of https://github.com/ajfa/mvme187-sysv88-gxemul/commit/4a01173afc4beafabbd61ca385bd158d07d4a415. It makes scaled byte ld/st unscaled, but exempts xmem (`op != 3`), so it leaves the crash in place. The xmem case was derived while reading that patch (part (b), A7 rows 29-30).
~~~~

**Evidence level.**  The defect is established by READING the source (both adjudicating seats, and this drafter
independently, section 5).  It has NOT been measured in this tree (section 2).

---

## 2. The witness disposition -- rung-3 attempt BLOCKED; detector-only by owner ruling (VERBATIM)

`regress/artifacts/m88kscaledbyte/witness_attempt_20261022/WITNESS_ATTEMPT.md`, inlined whole.  **It is UNTRACKED at
HEAD** (working tree only).
~~~~
    1| # m88kscaledbyte -- the rung-3 witness ATTEMPT, 2026-10-22: BLOCKED (recorded so `none` never means "did not think to")
    2| 
    3| Round T1 of the external-fixes batch (`regress/artifacts/research_20261022/`).  The carrier's lifecycle step 2 asks for
    4| a rung-3 witness attempt before the fix; the 2026-08-27 owner ruling asks one seat to try it; the 2026-08-27 `detector:`
    5| term requires the attempt to be RECORDED.
    6| 
    7| **What was attempted.**  A measuring seat was briefed (Agent tool, Opus) to make a cold-debugger probe through real
    8| instruction decode and real `memory_rw` on the unmodified in-tree `testm88k` machine, with the liveness and
    9| device-signature controls the witness ladder requires, built from HEAD 13233723 in a scratch clone -- the probe SHAPE both
   10| design seats specified in `research_20261022/crit_20261022/codex_rescrit.txt` and `grok_crit.txt` (their Q1 sections).
   11| The brief named no instruction words or decode paths; it pointed at the row id and those two answers.
   12| 
   13| **What happened.**  The coordinator's response was stopped by the harness safety classifier while the brief was being
   14| written (the seventh such stop that day; the class is recorded in the project memory `gxemul-panel-benign-framing`).
   15| The agent launched with a truncated brief and was killed at once; it had written nothing.  Per the standing rule for
   16| that class, the brief was not re-issued in any form.
   17| 
   18| **Owner ruling (2026-10-22, by question):** "Detector-only, attempt recorded" -- ship the agreed fix with an offline
   19| regression detector under the ledger's `detector:` witness term, record this attempt as BLOCKED, and leave a guest-path
   20| witness to the owner (or a session they drive) by another route if one is wanted.  The probe shape for that later run
   21| is the one the two seat answers specify; nothing here restates it.
   22| 
   23| **Status:** rung-3 attempt BLOCKED (classifier), not "not tried".  Witness term for the round: `detector:<path>`.
~~~~
**So, for this pass:** do NOT design, sketch or run a guest-path reproduction.  The round ships under the ledger's
`detector:<path>` witness term with an OFFLINE regression detector.  If an owed row could only be observed on a guest
path, NAME that row in Q3(d) and stop; the record will carry it to the owner.

---

## 3. The settled design (VERBATIM)

### 3.1 The merged ruling -- `regress/artifacts/research_20261022/crit_20261022/CRIT_RULINGS.md` (committed in `cb2eba1e`): header, the T1 row, the order paragraph
~~~~
    1| # Critical-items design adjudication -- merged rulings, 2026-10-22 (main loop; Fable 5.1 HELD by the owner)
    2| 
    3| Seats: GPT-6 Astra (ultra; `codex_rescrit.txt`) VERDICT OPEN -- "T1 repair correct; PPC fault-delivery dependencies and
    4| incomplete VR41xx subpage support prevent approving all six as ready fix rounds"; Grok 4.7 (xhigh; `grok_crit.txt`)
    5| VERDICT SETTLED.  Fable 5.1 DELIBERATELY NOT FIRED (`fable5.NOT_FIRED.txt`).  Both read source at HEAD de8c7547 and the
    6| local manuals; neither built or ran anything.  **On every design question the two seats agree**; the differences are
    7| scope labels (Astra's OPEN = N3/T11 are not plain fix rounds, which Grok also says).  This file carries DISPOSITIONS and
    8| POINTERS only; each round's owed rows, floor cells, accept controls and witness shape are specified in the two answers
    9| under the question named, and the round's pass-1 brief inlines them from there.
   10| 
   11| | item | ruling (both seats) | where the design is | status |
   12| |---|---|---|---|
   13| | **T1** m88k scaled-byte `xmem` NULL slot | The first adjudication's dispute is SETTLED for Astra: repair the TABLE (alias the scaled-byte slots to the existing unscaled byte handlers in `generate_m88k_loadstore.c:254-257`), keep the generation early-return (`:104-105`, else duplicate definitions), do NOT edit the decoder -- the `op != 3` exemption is not in this tree (it is the unported ajfa recipe) and changing a decoder-local `scaled` cannot reach `xmem_slow`'s own rebuild of it. Scaled `ld.b`/`st.b` share the slots (a CPU-stop, same change). N1/N2 stay separate rounds. | Astra Q1; Grok Q1 (24 repaired table entries; floor (a)-(d); accept rows; rung-3 on unmodified `testm88k`) | READY -- round 1 |
  ... (rows T36, T2, N5, N3, N4, T11, T4 omitted: other rounds)
   22| **Order (both seats):** T1, T36, T2, N5, T11, T4.  N3 feature; N4 unscheduled.  T1 is not merged with N1/N2; T2 not with
   23| N3; T36's generic path and LUNA case are ONE round; T11's two exits and the cache bit are ONE round; T4's advertisement,
   24| decode, arithmetic, readback and `#407` row are ONE round.
~~~~

### 3.2 GPT-6 Astra -- `codex_rescrit.txt` (same directory): the verdict line and the whole Q1 section
~~~~
    1| VERDICT: OPEN -- Astra’s T1 repair is correct; PPC fault-delivery dependencies and incomplete VR41xx subpage support prevent approving all six as ready fix rounds.
    3| Read the complete packet and checked the source at `de8c7547`, project rules, relevant manuals and preserved records. Nothing was built, executed or modified. The rows below are obligations, not measurements made today.
    5| **Q1 — T1: repair the table; both changes are not needed**
    6| 
    7| Astra is right. The decoder passes the original instruction word to `xmem_slow`, which independently reconstructs `scaled` and uses it for both load and store dispatch. Changing decoder-local `scaled` cannot repair those lookups. Also, the current decoder contains **no `op != 3` exemption**: that belongs to the proposed port. See [xmem_slow](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c:2348) and the [decoder](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c:3654).
    8| 
    9| Map valid scaled-byte table entries to their corresponding unscaled-byte handlers. Keep the function-generation suppression: the naming function deliberately omits `_scaled` for byte operations, so removing that suppression produces duplicate definitions. The separate table-generation rejection is the part to change. See [generator](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_loadstore.c:254).
   10| 
   11| The round owes:
   12| 
   13| - **Floor:** pre-fix red; verbatim restoration of the table defect; an identity `xmem` body that retires without exchanging anything; and repair-null variants that retain selection but omit the required mapping or effect. Observe both the returned byte and the memory write, including neighboring-byte preservation. Survival alone is insufficient.
   14| - **DEPENDS-ON:** byte/nonbyte × scaled/unscaled, preserving the dominating exclusions for signed stores, immediate `.usr`, and immediate scaled entries. There are **24 valid repaired entries**: `{unsigned load, signed load, store} × {LE, BE} × {ordinary, .usr} × {PC-sync, no-PC-sync}`, with byte/scaled/register-offset fixed. Check each against its corresponding unscaled entry. This finite table census does not require an arbitrary register/value cross-product.
   15| - **Accept controls:** unscaled bytes, scaled wider operations, and ordinary immediate forms remain correct.
   16| - **Cheapest rung-3 attempt:** an ordinary RAM exchange through real instruction decoding on an existing, unmodified 88K machine, checking register and memory effects and continuation. A boot is unnecessary.
   17| 
   18| N1 (`xmem` to r0 discarded) and N2 (`.usr` misdecoded inside the helper) remain separate defects. In particular, table coverage of `.usr` entries is not proof that decoder-driven `.usr xmem` reaches them correctly.
   19| 
   20| For **every round below**, the same applicable floor, bounded DEPENDS-ON enumeration, de-escalation accept rows, gate failure propagation, and documented rung-3 attempt remain owed. An offline fixture is a detector, not a guest-path witness.
~~~~

### 3.3 Grok 4.7 -- `grok_crit.txt` (same directory): the verdict and the whole Q1 section
~~~~
    1| [...] VERDICT: SETTLED -- Astra on T1 (the table alias, the generator suppression kept); T36 writes `BERROR<<16` and the saved physical address; N3 stays a feature and keeps its exit.
    3| No build was run. Every site below was read at HEAD `de8c7547`.
    5| ## Q1. T1 — Astra. The decoder exemption is not in this tree, and dropping it would not remove the call
    6| 
    7| `xmem_slow` (`cpu_m88k_instr.c:2357-2359`, call at `:2395`, store slot at `:2411-2426`) rebuilds `scaled` from bit `0x200` of the raw word the decoder stored in `ic->arg[0]` (`:3655-3656`). The decoder-local `scaled` at `:3608` is used by `ld`/`st` (`:3627`) and `lda` (`:3641`) only. There is no `op != 3` in this file. That exemption lives in the unported ajfa recipe. Clearing `scaled` in the decoder leaves the NULL call in place.
    8| 
    9| The repair is one change in the table printer. `generate_m88k_loadstore.c:254-257` emits `NULL` for `size == 0 && scaledness`. Delete that `continue` and let `:259-262` call `print_function_name`. `:80-81` already omits `_scaled` when `size == 0`, so the name is the existing unscaled byte function. Keep the generation early-return at `:104-105`. Removing it emits a second definition of that same name. Do not edit the decoder. Scale factor 1 makes the alias the architecture, not a decline.
   10| 
   11| The same arm also covers scaled `ld.b` / `ld.bu` / `st.b`. Those take a NULL `ic->f` and stop the CPU in the dyntrans NULL check, a different death from xmem's unguarded call, same slots, same change. N1 (`xmem` to r0 decoded as `nop` at `:3657-3658`) and N2 (handler reads `.usr` as `0x80` at `:2359`; the decoder's `.usr` is `0x100` at `:3604`, and `0x80` is `.wt`, which `goto bad`s at `:3611` before `xmem_slow`) are not this round. Scaled half and word keep scale 2 and 4.
   12| 
   13| The arm is reached only after `:249-252`, so `registeroffset` is already 1, and after `:239-242`, so `store && signedness` stays NULL. `cpu_m88k.c:130` forces big-endian, and xmem always adds `ENDIANNESS` (16). For `size == 0` the name printer emits `_le` for both endian values, so endianness is not a floor axis. Immediate xmem forces `scaled = 0` (`:2368-2370`).
   14| 
   15| Floor, channel is the exchanged byte:
   16| 
   17| - (a) Pre-fix: scaled `xmem.bu` rD≠0, rS2≠0, bit 9 set, bits 11:10 = 00, bit 7 clear, on unmodified `testm88k`. Host dies at the load call.
   18| - (b) Verbatim: put `NULL` back at that one arm. It covers the load index and the store index. A load-only alias moves the death to `:2426`, so the row must be the completed exchange.
   19| - (c) Identity body: decode, retire, write neither rD nor memory.
   20| - (d) Guard kept, name not emitted. The cells the arm distinguishes: `no_pc_sync` × {load, store} (xmem sets it, `ld`/`st` do not; `&& no_pc_sync` leaves scaled `ld.b` dead, `&& !no_pc_sync` leaves xmem dead); one signed scaled `ld.b` (xmem never sets `SIGNEDNESS`); one `.usr` scaled `ld.b` or `st.b` (a legal `xmem.usr` still indexes the non-usr slot, which is N2).
   21| 
   22| Accept, because a wrong alias is silent: the exchanged byte is exactly `rS1+rS2`, neighbours unchanged (kills a word or scale-4 alias); rD is the old byte zero-extended; an unscaled byte `xmem` still exchanges at `rS1+rS2`; a scaled word `xmem` still uses scale 4 where `rS2*4` differs from `rS2`. The growth mutant is widening `size == 0` so a scaled half or word slot is aliased to the byte function.
   23| 
   24| Rung-3: cold debugger, unmodified `testm88k`, real decode, real `memory_rw` into RAM. One scaled byte `xmem`, one unscaled byte `xmem`, one scaled word `xmem`. Liveness is the unscaled exchange of a known byte. Not a direct call of `xmem_slow`.
~~~~
*Condensed at line 1 only: the text before `VERDICT:` on that line is the seat's progress narration and is omitted
(`[...]`).  Lines 3 and 5-24 are verbatim.  Both seats read source at `de8c7547`; every source file they cite is
byte-identical at `cb2eba1e` (section 4, part 4), so their line numbers apply unchanged.*

*Astra's line 16 and Grok's line 24 specify the rung-3 witness attempt.  That attempt was made and is recorded
BLOCKED (section 2).  They are quoted because the task is to quote the Q1 sections whole -- not as work for this
pass.  Do not design or run them.*

**What "the repair" means in this brief**, in CRIT_RULINGS' words: alias the scaled-byte slots to the existing
unscaled byte handlers by removing the table printer's scaled-byte `NULL` arm in `generate_m88k_loadstore.c`
(lines 254-257); KEEP `loadstore()`'s matching early return (lines 104-105); do NOT edit the decoder.  P5 (section 6)
asks you to confirm the exact lines.

---

## 4. Section C0 -- has this round already shipped?  (commands run against HEAD; output CONDENSED -- the FULL brief carries it verbatim)

| part | command (against `cb2eba1e`) | result |
|---|---|---|
| 1 | `git log -1 -- src/cpus/generate_m88k_loadstore.c` | `39748e3c` 2026-06-28 "Import GXemul 0.7.0 (unmodified upstream baseline)" -- its ONLY commit |
| 1 | `git log -1 -- src/cpus/tmp_m88k_loadstore.c` | `39748e3c` 2026-06-28, the same import -- its ONLY commit |
| 1 | `git log -1` for `cpu_m88k_instr.c` / `cpu_m88k_instr_loadstore.c` / `cpu_dyntrans.c` | `ab9ae137` 2026-09-05 / `39748e3c` 2026-06-28 / `de1398e1` 2026-07-17 |
| 1 | `git log -1` for `regress/gate_offline.sh` / `gate_m88k_rounding.sh` / `m88k_exc_probe.py` / `diff_memory_rw.c` | `1329d894` 2026-10-02 / `01aef04f` 2026-10-16 / `01aef04f` 2026-10-16 / `abd7bad9` 2026-08-17 |
| 2 | `grep -n m88kscaledbyte CHANGELOG.md` (36,149 lines) | no match |
| 2 | `grep -n -i -E 'xmem\|generate_m88k_loadstore\|tmp_m88k_loadstore\|scaled.byte' CHANGELOG.md` | no match |
| 2 | `grep -n m88kscaledbyte OUTSTANDING_BUGS.md` | line 28 (OPEN LIST item 1) and line 25260 (the HIGH, open entry) -- section 1 |
| 2 | the ledger | the row is present; `state: open`; `commits` empty |
| 3 | `ls regress/diff_*.c regress/*m88k*`; `ls regress/*loadstore* regress/*xmem*` | 14 `diff_*.c` differentials, `gate_m88k_rounding.sh` and three `m88k_*_probe.py`; nothing named `*loadstore*` or `*xmem*` |
| 3 | `git ls-files regress tools \| grep -v '^regress/artifacts/' \| grep -iE 'loadstore\|xmem\|scaled'` | no match: no existing tool or detector for this class |
| 3 | `git ls-files regress/artifacts/m88kscaledbyte/` | empty: the directory is UNTRACKED; it holds only `WITNESS_ATTEMPT.md` (1,917 bytes, 2026-10-22 22:38) |
| 4 | md5 at `de8c7547` vs `cb2eba1e`: the generator, the table, `cpu_m88k_instr.c`, `cpu_dyntrans.c`, `cpu_m88k.c` | all SAME |
| 5 | md5 of the two repair files in `GXEMUL-SEC/`, `est/`, `build/`, `build-asan/` | all four identical (generator `bebaf439`, table `269e6e6f`); neither is in `tools/est_divergence.txt` |
**Result: NOT SHIPPED.**  No CHANGELOG hit for the row id or for the class; both files the repair edits are unchanged
since the upstream import `39748e3c`; no detector for the class exists.

---

## 5. SETTLED PREMISES -- re-inlined so nobody spends an answer re-deriving them

Settled by the critical-items adjudication (`crit_20261022`: GPT-6 Astra and Grok 4.7, source read at `de8c7547`,
neither built nor ran anything) and **RE-READ IN THIS SCOPE at HEAD `cb2eba1e`** by the drafter.  Each premise cites
the line re-read; the source is inlined in section 8.  Line numbers are as read at HEAD.

* **S1 -- the generator emits no handler for the scaled-byte class.**  `loadstore()` returns early on
  `if (size == 0 && scaledness)` (generate_m88k_loadstore.c:104-105).  The file's header comment says scaledness is
  "for halfword, word, and doublewords only" (:34-35).
* **S2 -- the table printer emits `NULL` for exactly those slots.**  In `main()`'s table loop:
  `if (size == 0 && scaledness) { printf("\tNULL"); continue; }` (:254-257), reached only after the three earlier NULL
  arms: `store && signedness` (:239-242), `!registeroffset && usr` (:244-247), `!registeroffset && scaledness`
  (:249-252).  MEASURED from the committed table (section 7): 296 of the 512 entries are `NULL` -- 128, 96 and 48 from
  those three arms, **24** from this one.
* **S3 -- the handler calls the slot unguarded.**  `X(xmem_slow)` sets `xmem_load = m88k_loadstore[...]`
  (cpu_m88k_instr.c:2377-2382) and calls `xmem_load(cpu, &call);` (:2395) with no NULL test; the store half the same
  (:2411-2417, call at :2426).  On a `NULL` slot that is a call through a NULL function pointer: the emulator process
  ends (the row's "host SIGSEGV").  *Read, not measured (section 2).*
* **S4 -- the decoder hands the raw instruction word to the slow handler, which rebuilds the scaling flag itself.**
  Both decode forms do `ic->f = instr(xmem_slow);` then `ic->arg[0] = iword;` (immediate form :3043-3044; register
  form :3655-3656).  The handler: `uint32_t iword = ic->arg[0];` (:2350), `int scaled = iword & 0x200;` (:2357),
  forced to 0 for the immediate form (:2368-2370).  The decoder's own `scaled` (declared :3566, set :3608-3609) is read
  only by the `ld`/`st` table index (:3627) and by `lda` (:3641).
* **S5 -- so the external recipe's decoder-side change cannot reach `xmem`.**  The recipe "makes scaled byte ld/st
  unscaled, but exempts xmem (`op != 3`)" (section 1).  Dropping that exemption changes only the decoder-local
  `scaled`, which `xmem_slow` never reads (S4).  This tree carries no such exemption at all:
  `git show cb2eba1e:src/cpus/cpu_m88k_instr.c | grep -c 'op != 3'` = **0** (also 0 for `op!=3`).
* **S6 -- scaled `ld.b` / `ld.bu` / `st.b` hit the same slots and STOP THE CPU (a controlled stop through the
  translator's error path -- no call through the NULL slot).**  The register-form `ld`/`st` index adds
  `+ (scaled? M88K_LOADSTORE_SCALEDNESS : 0)` (:3622-3629), so `ic->f` becomes NULL; the translator then runs
  `fatal("INTERNAL ERROR: ic->f == NULL!\n"); goto bad;` (cpu_dyntrans.c:1906-1909), and `bad:` sets
  `about_to_enter_single_step = true;` (:2002) and `cpu->running = 0;` (:2014).  Same slots, same repair.
* **S7 -- the architecture: a byte's scale factor is 1, and the result is identical.**  MC88100 User's Manual (local
  OCR text): "When the source 2 operand is scaled, it is shifted by 0, 1, 2, or 3 bits (multiplied by scale factor
  1, 2, 4, or 8) for byte, half-word, word, or double-word accesses, respectively. For byte accesses, the 5UBOPCODE
  [sic -- OCR for SUBOPCODE] field is distinctly different from the register indirect with index (unscaled) cases but
  the result is identical." (mc88100.txt:2961-2965).  `xmem` lists `xmem.bu rD,rS 1[rS2]` (OCR spacing) among its
  SCALED forms (:6421-6429), and "Operations that are byte and word in size define scale factors of one and four
  respectively" (:6459-6460).  The generated handlers compute `reg(ic->arg[1]) + LS_SIZE * reg(ic->arg[2])` under `LS_SCALED`
  (cpu_m88k_instr_loadstore.c:65-70 generic, :248-253 fast), so with `LS_SIZE` 1 a scaled and an unscaled byte
  handler compute the same address.
* **S8 -- the alias needs no new function, and this same table already aliases on another axis.**
  `print_function_name()` appends `_scaled` only `if (scaledness && size > 0)` (:80-81) and prints `_le` for every byte
  entry whatever its endianness (:74-75).  So with the arm at :254-257 gone, each scaled-byte slot prints its unscaled
  counterpart's existing name -- MEASURED: all 24 counterparts (index - 32) are existing non-NULL functions, **12
  distinct names** (section 7).  The table ALREADY maps two slots to one function on the endianness axis: `loadstore()`
  generates no big-endian byte function (:101-102), and every big-endian byte slot prints the `_le` name.
* **S9 -- the early return at :104-105 must stay.**  Without it `loadstore()` would emit a second `LS_N` /
  `LS_GENERIC_N` definition under the same unscaled byte name (S8): a duplicate definition, i.e. a compile failure,
  not a silent change.
* **S10 -- exactly four sites index the table** (`m88k_loadstore[` over `src/`, the generated file excluded): the
  `xmem_slow` load half (:2377) and store half (:2411); the immediate-form `ld`/`st` decoder (:3087 -- never adds
  SCALEDNESS, USR or REGISTEROFFSET); the register-form `ld`/`st` decoder (:3622 -- never adds NO_PC_SYNC).  The index
  constants are identical in the generator (:46-52) and the handler file (:298-304), and the table is printed in loop
  order with bit-weight increments, so array position == index (confirmed by the census: no non-NULL entry falls
  under any NULL arm).
* **S11 -- scope exclusions** (separate rows, section 1): `m88kxmemr0` (N1: `xmem` to r0 decoded as `nop`),
  `m88kxmemusr` (N2: the handler reads `.usr` from bit `0x80` while the decoder uses `0x100` and rejects `0x80` as
  `.wt`), `m88kzeroword`, `m88kwtbit`.  T1 is not merged with N1 or N2 (CRIT_RULINGS).
* **S12 -- the witness:** rung-3 attempt BLOCKED; owner ruling "Detector-only, attempt recorded"; witness term
  `detector:<path>`; the detector is an OFFLINE regression detector (section 2).
* **S13 -- section C0: not shipped** (section 4).
* **S14 -- the generated table is a TRACKED FILE, and neither seat mentions it.**  `src/cpus/tmp_m88k_loadstore.c` is
  in `git ls-files`, unchanged since the import `39748e3c`, and byte-identical in `GXEMUL-SEC/`, `est/`, `build/` and
  `build-asan/` (section 4, part 5; neither repair file is in `tools/est_divergence.txt`).  `src/cpus/Makefile.skel`
  lines 134-135 regenerate it from the generator binary at build time (section 8.7).  `build/`'s copy is byte-identical
  to the committed one and carries the same mtime minute as `build/`'s generator binary and source (2026-10-18 23:22)
  -- consistent with a rebuild; the byte identity is the measured part.  No section of `tools/precommit_check.sh`
  mentions `tmp_` or `generate_` (0 hits at HEAD).  *Its consequence is P4, a question.*

---

## 6. PREMISES STATED AS QUESTIONS -- check these; ratification is not wanted

* **P1 -- byte order (this challenges a seat's premise).**  Grok (line 13): "`cpu_m88k.c:130` forces big-endian, and
  xmem always adds `ENDIANNESS` (16). For `size == 0` the name printer emits `_le` for both endian values, so
  endianness is not a floor axis."  The constructor does set big-endian (cpu_m88k.c:130).
  But I read two LATER writers (section 8.8): machine setup applies the byte order the file loader reports
  (`cpu->byte_order = byte_order;`, emul.c:651-652; `file_elf.c:693-694` reports `EMUL_LITTLE_ENDIAN` for an
  `ELFDATA2LSB` file), and then a machine's `byte_order` setting from a configuration file (emul.c:737-738;
  `emul_parse.c:493-499` accepts "big" or "little").  **Is the little-endian half of the table (12 of the 24 slots)
  reachable on an m88k machine?**  If it is, does "endianness is not a floor axis" still hold -- note S8: the repair
  maps the LE and BE byte slots to the SAME names, so it is identical on both halves -- or does reachability change
  which rows are owed?
* **P2 -- `.usr` in the `xmem` half.**  `xmem_slow` takes `int user = iword & 0x80;` (:2359).  The register-form
  decoder treats bit 7 as `.wt` and sends it to `fatal(...); goto bad;` BEFORE `xmem_slow` (:3606-3614); the immediate
  form forces `user = 0` (:2372).  So I believe the `.usr` + no-PC-sync slots (496, 500; little-endian 480, 484) have
  **no producer today**, and would gain one if N2 (`m88kxmemusr`) is later fixed to read `0x100`.  Check.
* **P3 -- signed + no-PC-sync.**  `xmem_slow` never adds SIGNEDNESS; neither decoder adds NO_PC_SYNC.  So I believe
  slots 440 and 504 (little-endian 424, 488) have **no producer at all**.  Check.
* **P4 -- the tracked generated table (the question neither seat answered).**  Given S14: does the round's diff owe the
  committed `tmp_m88k_loadstore.c` regenerated in the same commit (24 lines change from `NULL` to a handler name)?  If
  yes, what verifies that the committed copy equals the generator's output?  If no, the committed copy disagrees with
  what every build compiles.  Which artifact the detector reads is Q3.
* **P5 -- the literal edit.**  Grok: "Delete that `continue` and let `:259-262` call `print_function_name`."  The arm
  is four lines, and `printf("\tNULL");` (:255) runs BEFORE the `continue` (:256).  Read against the loop, deleting
  only the `continue` prints `\tNULL` and then `\tm88k_instr_<name>` for the same entry -- two tokens with no comma in
  an initializer list, a compile failure in the generated file.  I read the intended repair as removing the whole arm
  (:254-257), which is CRIT_RULINGS' wording.  Confirm or correct.
* **P6 -- what the seats were told about clause (c).**  The packet the two seats answered stated the floor as quoted
  below (`crit_20261022/packet.md` lines 11-15, VERBATIM), and both seats then named an identity `xmem` body.  The
  owner's later ruling (section 2) makes this an OFFLINE detector, and the project's clause-(c) rule picks the null
  medium by INSTRUMENT KIND (section 10, R2).  Does the identity body still apply?  -> Q2(a), Q3(c).

~~~~
   11| `C:\DocumentNoSnc\CC\GXEMUL_upstream_2021\root_src\`. The project rules for a fix round are in the carrier
   12| `CLAUDE.md`: a detector ships WITH the fix and must pass the vacuity floor (fails on the pre-fix build; on a verbatim
   13| reinstatement of the defect; on a NULL MEDIUM -- for an instruction-handler round an IDENTITY BODY; and when the
   14| repair is nulled with its guard kept), with the de-escalation accept rows when a host exit is removed, and the
   15| DEPENDS-ON enumeration of the guard body-tested partitions. Every round owes a rung-3 witness ATTEMPT.
~~~~

---

## 7. The table census (MEASURED) and the producer enumeration (the drafter's -- CHECK IT)

**Deriver:** a read-only parse of the committed `src/cpus/tmp_m88k_loadstore.c` at HEAD -- the 512-entry
`m88k_loadstore[512]` initializer; nothing built or run.  It classifies each `NULL` by the first generator arm whose
predicate holds, in the table printer's order.  Output, VERBATIM:
~~~~
entries parsed: 512
NULL entries: 296
NULLs by arm: {'A store&&signedness': 128, 'C !regofs&&scaled': 48, 'B !regofs&&usr': 96, 'D size==0&&scaled': 24}
non-NULL entries with an arm (should be 0): 0
arm-D indices (24): [160, 164, 168, 176, 180, 184, 224, 228, 232, 240, 244, 248, 416, 420, 424, 432, 436, 440, 480, 484, 488, 496, 500, 504]

idx   kind   endian usr sync          | slot   | unscaled counterpart (index-32)
160   ld.bu  LE     -   sync          | NULL   | [128] m88k_instr_ld_u_1_le_regofs
164   st.b   LE     -   sync          | NULL   | [132] m88k_instr_st_1_le_regofs
168   ld.b   LE     -   sync          | NULL   | [136] m88k_instr_ld_1_le_regofs
176   ld.bu  BE     -   sync          | NULL   | [144] m88k_instr_ld_u_1_le_regofs
180   st.b   BE     -   sync          | NULL   | [148] m88k_instr_st_1_le_regofs
184   ld.b   BE     -   sync          | NULL   | [152] m88k_instr_ld_1_le_regofs
224   ld.bu  LE     usr sync          | NULL   | [192] m88k_instr_ld_u_1_le_usr_regofs
228   st.b   LE     usr sync          | NULL   | [196] m88k_instr_st_1_le_usr_regofs
232   ld.b   LE     usr sync          | NULL   | [200] m88k_instr_ld_1_le_usr_regofs
240   ld.bu  BE     usr sync          | NULL   | [208] m88k_instr_ld_u_1_le_usr_regofs
244   st.b   BE     usr sync          | NULL   | [212] m88k_instr_st_1_le_usr_regofs
248   ld.b   BE     usr sync          | NULL   | [216] m88k_instr_ld_1_le_usr_regofs
416   ld.bu  LE     -   nosync          | NULL   | [384] m88k_instr_ld_u_1_le_regofs_nopcsync
420   st.b   LE     -   nosync          | NULL   | [388] m88k_instr_st_1_le_regofs_nopcsync
424   ld.b   LE     -   nosync          | NULL   | [392] m88k_instr_ld_1_le_regofs_nopcsync
432   ld.bu  BE     -   nosync          | NULL   | [400] m88k_instr_ld_u_1_le_regofs_nopcsync
436   st.b   BE     -   nosync          | NULL   | [404] m88k_instr_st_1_le_regofs_nopcsync
440   ld.b   BE     -   nosync          | NULL   | [408] m88k_instr_ld_1_le_regofs_nopcsync
480   ld.bu  LE     usr nosync          | NULL   | [448] m88k_instr_ld_u_1_le_usr_regofs_nopcsync
484   st.b   LE     usr nosync          | NULL   | [452] m88k_instr_st_1_le_usr_regofs_nopcsync
488   ld.b   LE     usr nosync          | NULL   | [456] m88k_instr_ld_1_le_usr_regofs_nopcsync
496   ld.bu  BE     usr nosync          | NULL   | [464] m88k_instr_ld_u_1_le_usr_regofs_nopcsync
500   st.b   BE     usr nosync          | NULL   | [468] m88k_instr_st_1_le_usr_regofs_nopcsync
504   ld.b   BE     usr nosync          | NULL   | [472] m88k_instr_ld_1_le_usr_regofs_nopcsync
~~~~
`kind` is the table axis: `ld.bu` = unsigned load (the slot `xmem`'s load half uses), `ld.b` = signed load, `st.b` =
store.  The 12 distinct names are the right-hand column with the `[index]` dropped.

**Producer enumeration -- which of the 24 slots a guest instruction can reach today.**  This is the drafter's reading
of the four producers in S10.  ENUMERATE IT YOURSELF; do not ratify it.

| slot(s) | cell | producer at HEAD |
|---|---|---|
| 176, 184, 180 | `ld.bu` / `ld.b` / `st.b`; big-endian; plain; PC-sync | the register-form `ld`/`st` decoder with its `scaled` set (:3622-3629) -> `ic->f == NULL` -> CPU stop (S6) |
| 240, 248, 244 | the same with `.usr` (the decoder's `user`, from `0x100`) | the same decoder path with `user` also set -> CPU stop |
| 432, 436 | `ld.bu` / `st.b`; big-endian; plain; no-PC-sync | `xmem_slow`'s load half (:2377-2382), then its store half (:2411-2417), when the handler's own `scaled` is set and `size` is clear -> NULL call -> process ends (S3) |
| 440, 504 | `ld.b`; big-endian; no-PC-sync; plain / `.usr` | none (P3) |
| 496, 500 | `ld.bu` / `st.b`; big-endian; `.usr`; no-PC-sync | none today; `xmem` becomes their producer if N2 is fixed (P2) |
| 160, 168, 164, 224, 232, 228, 416, 420 | the little-endian twins of the eight reachable cells above | the same producers, only if the CPU's byte order is little-endian (P1) |
| 424, 488, 480, 484 | the little-endian twins of 440, 504, 496, 500 | none (P1 with P2/P3) |

Count check: 3 + 3 + 2 + 2 + 2 + 8 + 4 = **24**.  Reachable on a big-endian CPU today: **8** -- 176, 180, 184, 240,
244, 248, 432, 436.

---

## 8. SOURCE, INLINED -- the full enclosing functions (sketch rule); line numbers as read at HEAD `cb2eba1e`

### 8.1 `src/cpus/generate_m88k_loadstore.c` -- lines 27-112 and 191-271 (113-190, the rest of `loadstore()`'s `#define` printing, summarised in place)
`print_function_name()` is the naming block; `loadstore()` holds the generation early returns; `main()` holds the table
printer, where the edited arm is (254-257).  Anchor `if (size == 0 && scaledness) {` is unique (254); without the
brace it matches 104 and 254.
~~~~
   27|  *
   28|  *  Automatic generation of M88K loads and stores:
   29|  *
   30|  *	2 bits size (0=byte, 1=halfword, 2=word, 3=doubleword)
   31|  *	1 bit load/store
   32|  *	1 bit signedness (for byte and halfword loads only!)
   33|  *	1 bit endianness
   34|  *	1 bit scaledness (for halfword, word, and doublewords only,
   35|  *			  and only when using register offset)
   36|  *	1 bit ".usr" (only when using register offset)
   37|  *	1 bit registeroffset
   38|  *	1 bit indicating that Program Counter syncronization is skipped
   39|  *		(for using the load/store routine from another instruction)
   40|  */
   41| 
   42| #include <stdio.h>
   43| #include <string.h>
   44| 
   45| 
   46| #define	M88K_LOADSTORE_STORE		4
   47| #define	M88K_LOADSTORE_SIGNEDNESS	8
   48| #define	M88K_LOADSTORE_ENDIANNESS	16
   49| #define	M88K_LOADSTORE_SCALEDNESS	32
   50| #define	M88K_LOADSTORE_USR		64
   51| #define	M88K_LOADSTORE_REGISTEROFFSET	128
   52| #define	M88K_LOADSTORE_NO_PC_SYNC	256
   53| 
   54| 
   55| int generated_functions = 0;
   56| 
   57| 
   58| void print_function_name(int size, int store, int signedness,
   59| 	int endianness, int scaledness, int usr, int registeroffset,
   60| 	int no_pc_sync)
   61| {
   62| 	if (store)
   63| 		printf("st");
   64| 	else {
   65| 		printf("ld");
   66| 		if (!signedness)
   67| 			printf("_u");
   68| 	}
   69| 	printf("_%i", 1 << size);
   70| 
   71| 	if (endianness >= 0) {
   72| 		/*  Special case so that Byte loads/stores are only
   73| 		    included ones (for little endian):  */
   74| 		if (size == 0 && endianness)
   75| 			printf("_le");
   76| 		else
   77| 			printf(endianness? "_be" : "_le");
   78| 	}
   79| 
   80| 	if (scaledness && size > 0)
   81| 		printf("_scaled");
   82| 
   83| 	if (usr)
   84| 		printf("_usr");
   85| 
   86| 	if (registeroffset)
   87| 		printf("_regofs");
   88| 
   89| 	if (no_pc_sync)
   90| 		printf("_nopcsync");
   91| }
   92| 
   93| 
   94| void loadstore(int size, int store, int signedness,
   95| 	int endianness, int scaledness, int usr, int registeroffset,
   96| 	int no_pc_sync)
   97| {
   98| 	if (store && signedness)
   99| 		return;
  100| 
  101| 	if (size == 0 && endianness)
  102| 		return;
  103| 
  104| 	if (size == 0 && scaledness)
  105| 		return;
  106| 
  107| 	if (!registeroffset && usr)
  108| 		return;
  109| 
  110| 	if (!registeroffset && scaledness)
  111| 		return;
  112| 
  ... (lines 113-190, the rest of loadstore(): it prints the #define / #undef lines for LS_STORE/LS_LOAD, LS_N, LS_GENERIC_N, LS_<size>, LS_SIZE, LS_SIGNED, LS_BE/LS_LE, LS_INCLUDE_GENERIC, LS_SCALED, LS_USR, LS_REGOFS, LS_NO_PC_SYNC around #include "cpu_m88k_instr_loadstore.c" and counts generated_functions++; the FULL brief inlines them)
  191| 
  192| 
  193| int main(int argc, char *argv[])
  194| {
  195| 	int size, store, signedness, endianness, scaledness, usr,
  196| 	    registeroffset, no_pc_sync;
  197| 
  198| 	printf("\n/*  AUTOMATICALLY GENERATED! Do not edit.  */\n\n");
  199| 
  200| 	for (no_pc_sync=0; no_pc_sync<=M88K_LOADSTORE_NO_PC_SYNC;
  201| 		      no_pc_sync+=M88K_LOADSTORE_NO_PC_SYNC)
  202| 	 for (registeroffset=0; registeroffset<=M88K_LOADSTORE_REGISTEROFFSET;
  203| 		      registeroffset+=M88K_LOADSTORE_REGISTEROFFSET)
  204| 	  for (usr=0; usr<=M88K_LOADSTORE_USR; usr+=M88K_LOADSTORE_USR)
  205| 	   for (scaledness=0; scaledness<=M88K_LOADSTORE_SCALEDNESS;
  206| 			scaledness+=M88K_LOADSTORE_SCALEDNESS)
  207| 	    for (endianness=0; endianness<=M88K_LOADSTORE_ENDIANNESS;
  208| 			  endianness+=M88K_LOADSTORE_ENDIANNESS)
  209| 	      for (signedness=0; signedness<=M88K_LOADSTORE_SIGNEDNESS;
  210| 			    signedness+=M88K_LOADSTORE_SIGNEDNESS)
  211| 	        for (store=0; store<=M88K_LOADSTORE_STORE;
  212| 			      store+=M88K_LOADSTORE_STORE)
  213| 		  for (size=0; size<=3; size++)
  214| 			loadstore(size, store, signedness,
  215| 			    endianness, scaledness, usr, registeroffset,
  216| 			    no_pc_sync);
  217| 
  218| 	/*  Array of pointers to fast load/store functions:  */
  219| 	printf("\n\nvoid (*m88k_loadstore[512])(struct cpu *, struct "
  220| 	    "m88k_instr_call *) = {\n");
  221| 	for (no_pc_sync=0; no_pc_sync<=M88K_LOADSTORE_NO_PC_SYNC;
  222| 		      no_pc_sync+=M88K_LOADSTORE_NO_PC_SYNC)
  223| 	 for (registeroffset=0; registeroffset<=M88K_LOADSTORE_REGISTEROFFSET;
  224| 		      registeroffset+=M88K_LOADSTORE_REGISTEROFFSET)
  225| 	  for (usr=0; usr<=M88K_LOADSTORE_USR; usr+=M88K_LOADSTORE_USR)
  226| 	   for (scaledness=0; scaledness<=M88K_LOADSTORE_SCALEDNESS;
  227| 			scaledness+=M88K_LOADSTORE_SCALEDNESS)
  228| 	    for (endianness=0; endianness<=M88K_LOADSTORE_ENDIANNESS;
  229| 			  endianness+=M88K_LOADSTORE_ENDIANNESS)
  230| 	      for (signedness=0; signedness<=M88K_LOADSTORE_SIGNEDNESS;
  231| 			    signedness+=M88K_LOADSTORE_SIGNEDNESS)
  232| 	        for (store=0; store<=M88K_LOADSTORE_STORE;
  233| 			      store+=M88K_LOADSTORE_STORE)
  234| 		  for (size=0; size<=3; size++) {
  235| 			if (store || size || signedness || endianness
  236| 			    || scaledness || usr || registeroffset || no_pc_sync)
  237| 				printf(",\n");
  238| 
  239| 			if (store && signedness) {
  240| 				printf("\tNULL");
  241| 				continue;
  242| 			}
  243| 
  244| 			if (!registeroffset && usr) {
  245| 				printf("\tNULL");
  246| 				continue;
  247| 			}
  248| 
  249| 			if (!registeroffset && scaledness) {
  250| 				printf("\tNULL");
  251| 				continue;
  252| 			}
  253| 
  254| 			if (size == 0 && scaledness) {
  255| 				printf("\tNULL");
  256| 				continue;
  257| 			}
  258| 
  259| 			printf("\tm88k_instr_");
  260| 			print_function_name(size, store, signedness,
  261| 			    endianness, scaledness, usr, registeroffset,
  262| 			    no_pc_sync);
  263| 		}
  264| 	printf(" };\n");
  265| 
  266| 	fprintf(stderr, "%s: generated_functions = %i\n",
  267| 	    argv[0], generated_functions);
  268| 
  269| 	return 0;
  270| }
  271| 
~~~~

### 8.2 `src/cpus/cpu_m88k_instr.c` -- `X(xmem_slow)`, whole, with its header comment (lines 2337-2439; anchor `X(xmem_slow)`, unique)
Both indirect calls are unguarded.  Its exits: the `return;` after an exception in the load half, the `return;` after
an exception in the store half, and the fall-off at the closing brace.
~~~~
 2337| /*
 2338|  *  xmem_slow:  Unoptimized xmem (exchange register with memory)
 2339|  *
 2340|  *  arg[0] = copy of the instruction word
 2341|  *
 2342|  *  NOTE: The alternative would be to extend the load/store instructions
 2343|  *  to also include xmem, and thus implement a "fast" version (where
 2344|  *  the page is already accessible both readable and writable) and a
 2345|  *  generic version. (The generic implementation would then not need to
 2346|  *  have a NO_PC_SYNC flag, since they would always sync.)
 2347|  */
 2348| X(xmem_slow)
 2349| {
 2350| 	uint32_t iword = ic->arg[0];
 2351| 	uint32_t tmp;
 2352| 	int d      = (iword >> 21) & 0x1f;
 2353| 	int s1     = (iword >> 16) & 0x1f;
 2354| 	int s2     =  iword        & 0x1f;
 2355| 	int imm16  =  iword        & 0xffff;
 2356| 	int regofs = (iword & 0xf0000000) != 0;
 2357| 	int scaled = iword & 0x200;
 2358| 	int size   = iword & 0x400;
 2359| 	int user   = iword & 0x80;
 2360| 	uint32_t pc_before_memory_access;
 2361| 	void (*xmem_load)(struct cpu*, struct m88k_instr_call*);
 2362| 	void (*xmem_store)(struct cpu*, struct m88k_instr_call*);
 2363| 	struct m88k_instr_call call;
 2364| 
 2365| 	SYNCH_PC;
 2366| 	pc_before_memory_access = (uint32_t)cpu->pc;
 2367| 
 2368| 	if (!regofs) {
 2369| 		/*  immediate offset:  */
 2370| 		scaled = 0;
 2371| 		size = (iword >> 26) & 1;
 2372| 		user = 0;
 2373| 	}
 2374| 
 2375| 	tmp = cpu->cd.m88k.r[d];
 2376| 
 2377| 	xmem_load = m88k_loadstore[ (size? 2 : 0)
 2378| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
 2379| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 2380| 	    + (user? M88K_LOADSTORE_USR : 0)
 2381| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
 2382| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
 2383| 
 2384| 	call.f = xmem_load;
 2385| 	call.arg[0] = (size_t) &cpu->cd.m88k.r[d];
 2386| 	call.arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 2387| 	if (regofs)
 2388| 		call.arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 2389| 	else
 2390| 		call.arg[2] = imm16;
 2391| 
 2392| 	if (d == M88K_ZERO_REG)
 2393| 		call.arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
 2394| 
 2395| 	xmem_load(cpu, &call);
 2396| 
 2397| 	// If there was an exception in the load or store call, then the pc
 2398| 	// will have changed. Alternatively, one could check for changes in
 2399| 	// the transaction registers. (But handling the theoretical tiny risk
 2400| 	// that the pc was the same before and after, i.e. that the faulting
 2401| 	// instruction was the same as the exception handler, is not worth it.)
 2402| 	if ((uint32_t)cpu->pc != pc_before_memory_access) {
 2403| 		//printf("xmem_load exception, pc_before_memory_access = %08x\n", pc_before_memory_access);
 2404| 		cpu->cd.m88k.dmd[0] = tmp;
 2405| 		cpu->cd.m88k.dmt[0] |= DMT_LOCKBAR | DMT_WRITE;
 2406| 		cpu->cd.m88k.dmt[0] &= ~((0x1f) << DMT_DREGSHIFT);
 2407| 		cpu->cd.m88k.dmt[0] |= d << DMT_DREGSHIFT;
 2408| 		return;
 2409| 	}
 2410| 
 2411| 	xmem_store = m88k_loadstore[ (size? 2 : 0)
 2412| 	    + M88K_LOADSTORE_STORE
 2413| 	    + (cpu->byte_order == EMUL_BIG_ENDIAN? M88K_LOADSTORE_ENDIANNESS : 0)
 2414| 	    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 2415| 	    + (user? M88K_LOADSTORE_USR : 0)
 2416| 	    + (regofs? M88K_LOADSTORE_REGISTEROFFSET : 0)
 2417| 	    + M88K_LOADSTORE_NO_PC_SYNC ];
 2418| 
 2419| 	call.f = xmem_store;
 2420| 	call.arg[0] = (size_t) &tmp;
 2421| 	// arg[1] and arg[2] are already set up from xmem_load call.
 2422| 
 2423| 	if (d == M88K_ZERO_REG)
 2424| 		tmp = 0;
 2425| 
 2426| 	xmem_store(cpu, &call);
 2427| 
 2428| 	// If there was an exception in xmem_store(), then return the d register
 2429| 	// to what it was before the xmem_load().
 2430| 	if ((uint32_t)cpu->pc != pc_before_memory_access) {
 2431| 		//printf("xmem_store exception, pc_before_memory_access = %08x\n", pc_before_memory_access);
 2432| 		// cpu->cd.m88k.r[d] = tmp;
 2433| 		cpu->cd.m88k.dmd[0] = tmp;
 2434| 		cpu->cd.m88k.dmt[0] |= DMT_LOCKBAR | DMT_WRITE;
 2435| 		cpu->cd.m88k.dmt[0] &= ~((0x1f) << DMT_DREGSHIFT);
 2436| 		cpu->cd.m88k.dmt[0] |= d << DMT_DREGSHIFT;
 2437| 		return;
 2438| 	}
 2439| }
~~~~

### 8.3 `src/cpus/cpu_m88k_instr.c` -- the decoder's dispatch regions (EXCERPTS of `X(to_be_translated)`; the repair does NOT edit them)
Immediate form -- field extraction, then opcodes 0x00-0x0b (lines 3027-3096):
~~~~
 3027| 	op26   = (iword >> 26) & 0x3f;
 3028| 	op11   = (iword >> 11) & 0x1f;
 3029| 	op10   = (iword >> 10) & 0x3f;
 3030| 	d      = (iword >> 21) & 0x1f;
 3031| 	s1     = (iword >> 16) & 0x1f;
 3032| 	s2     =  iword        & 0x1f;
 3033| 	imm16  =  iword        & 0xffff;
 3034| 	// simm16 = (int16_t) (iword & 0xffff);
 3035| 	cr6    = (iword >>  5) & 0x3f;
 3036| 	d16    = ((int16_t) (iword & 0xffff)) * 4;
 3037| 	d26    = ((int32_t)((iword & 0x03ffffff) << 6)) >> 4;
 3038| 
 3039| 	switch (op26) {
 3040| 
 3041| 	case 0x00:
 3042| 	case 0x01:
 3043| 		ic->f = instr(xmem_slow);
 3044| 		ic->arg[0] = iword;
 3045| 		if (d == M88K_ZERO_REG)
 3046| 			ic->f = instr(nop);
 3047| 		if (iword == 0)
 3048| 			goto bad;
 3049| 		break;
 3050| 
 3051| 	case 0x02:	/*  ld.hu  */
 3052| 	case 0x03:	/*  ld.bu  */
 3053| 	case 0x04:	/*  ld.d   */
 3054| 	case 0x05:	/*  ld     */
 3055| 	case 0x06:	/*  ld.h   */
 3056| 	case 0x07:	/*  ld.b   */
 3057| 	case 0x08:	/*  st.d   */
 3058| 	case 0x09:	/*  st     */
 3059| 	case 0x0a:	/*  st.h   */
 3060| 	case 0x0b:	/*  st.b   */
 3061| 		{
 3062| 			int store = 0, signedness = 0, opsize = 0;
 3063| 
 3064| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3065| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3066| 			ic->arg[2] = imm16;
 3067| 
 3068| 			switch (op26) {
 3069| 			case 0x02: opsize = 1; break;
 3070| 			case 0x03: opsize = 0; break;
 3071| 			case 0x04: opsize = 3; break;
 3072| 			case 0x05: opsize = 2; break;
 3073| 			case 0x06: opsize = 1; signedness = 1; break;
 3074| 			case 0x07: opsize = 0; signedness = 1; break;
 3075| 			case 0x08: store = 1; opsize = 3; break;
 3076| 			case 0x09: store = 1; opsize = 2; break;
 3077| 			case 0x0a: store = 1; opsize = 1; break;
 3078| 			case 0x0b: store = 1; opsize = 0; break;
 3079| 			}
 3080| 
 3081| 			if (opsize == 3 && d == 31) {
 3082| 				fatal("m88k load/store of register pair r31/r0"
 3083| 				    " is not yet implemented\n");
 3084| 				goto bad;
 3085| 			}
 3086| 
 3087| 			ic->f = m88k_loadstore[ opsize
 3088| 			    + (store? M88K_LOADSTORE_STORE : 0)
 3089| 			    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3090| 			    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3091| 			       M88K_LOADSTORE_ENDIANNESS : 0) ];
 3092| 
 3093| 			if (!store && d == 0)
 3094| 				ic->arg[0] = (size_t) &cpu->cd.m88k.zero_scratch;
 3095| 		}
 3096| 		break;
~~~~
Register form -- the opcode-0x3d load / store / `xmem` / `lda` block (lines 3562-3660):
~~~~
 3562| 	case 0x3d:
 3563| 		if ((iword & 0xf000) <= 0x3fff ) {
 3564| 			/*  Load, Store, xmem, and lda:  */
 3565| 			int op = 0, opsize, user = 0, wt = 0;
 3566| 			int signedness = 1, scaled = 0;
 3567| 
 3568| 			switch (iword & 0xf000) {
 3569| 			case 0x2000: op = 1; /* st */  break;
 3570| 			case 0x3000: op = 2; /* lda */ break;
 3571| 			default:     if ((iword & 0xf800) >= 0x0800)
 3572| 					op = 0; /* ld */
 3573| 				     else
 3574| 					op = 3; /* xmem */
 3575| 			}
 3576| 
 3577| 			/*  for (most) ld, st, lda:  */
 3578| 			opsize = (iword >> 10) & 3;
 3579| 
 3580| 			/*  Turn opsize into x, where size = 1 << x:  */
 3581| 			opsize = 3 - opsize;
 3582| 
 3583| 			if (op == 3) {
 3584| 				/*  xmem:  */
 3585| 				switch ((iword >> 10) & 3) {
 3586| 				case 0: opsize = 0; break;
 3587| 				case 1: opsize = 2; break;
 3588| 				default:fatal("Weird xmem opsize/type?\n");
 3589| 					goto bad;
 3590| 				}
 3591| 			} else {
 3592| 				if ((iword & 0xf800) == 0x800) {
 3593| 					signedness = 0;
 3594| 					if ((iword & 0xf00) < 0xc00)
 3595| 						opsize = 1;
 3596| 					else
 3597| 						opsize = 0;
 3598| 				} else {
 3599| 					if (opsize >= 2 || op == 1)
 3600| 						signedness = 0;
 3601| 				}
 3602| 			}
 3603| 
 3604| 			if (iword & 0x100)
 3605| 				user = 1;
 3606| 			if (iword & 0x80)
 3607| 				wt = 1;
 3608| 			if (iword & 0x200)
 3609| 				scaled = 1;
 3610| 
 3611| 			if (wt) {
 3612| 				fatal("wt bit not yet implemented! TODO\n");
 3613| 				goto bad;
 3614| 			}
 3615| 
 3616| 			ic->arg[0] = (size_t) &cpu->cd.m88k.r[d];
 3617| 			ic->arg[1] = (size_t) &cpu->cd.m88k.r[s1];
 3618| 			ic->arg[2] = (size_t) &cpu->cd.m88k.r[s2];
 3619| 
 3620| 			if (op == 0 || op == 1) {
 3621| 				/*  ld or st:  */
 3622| 				ic->f = m88k_loadstore[ opsize
 3623| 				    + (op==1? M88K_LOADSTORE_STORE : 0)
 3624| 				    + (signedness? M88K_LOADSTORE_SIGNEDNESS:0)
 3625| 				    + (cpu->byte_order == EMUL_BIG_ENDIAN?
 3626| 				       M88K_LOADSTORE_ENDIANNESS : 0)
 3627| 				    + (scaled? M88K_LOADSTORE_SCALEDNESS : 0)
 3628| 				    + (user? M88K_LOADSTORE_USR : 0)
 3629| 				    + M88K_LOADSTORE_REGISTEROFFSET ];
 3630| 
 3631| 				if (d == M88K_ZERO_REG && op == 0)
 3632| 					ic->arg[0] = (size_t)&cpu->cd.m88k.zero_scratch;
 3633| 
 3634| 				if (opsize == 3 && d == 31) {
 3635| 					fatal("m88k load/store of register "
 3636| 					    "pair r31/r0: TODO\n");
 3637| 					goto bad;
 3638| 				}
 3639| 			} else if (op == 2) {
 3640| 				/*  lda:  */
 3641| 				if (scaled) {
 3642| 					switch (opsize) {
 3643| 					case 0: ic->f = instr(addu); break;
 3644| 					case 1: ic->f = instr(lda_reg_2); break;
 3645| 					case 2: ic->f = instr(lda_reg_4); break;
 3646| 					case 3: ic->f = instr(lda_reg_8); break;
 3647| 					}
 3648| 				} else {
 3649| 					ic->f = instr(addu);
 3650| 				}
 3651| 				if (d == M88K_ZERO_REG)
 3652| 					ic->f = instr(nop);
 3653| 			} else {
 3654| 				/*  xmem:  */
 3655| 				ic->f = instr(xmem_slow);
 3656| 				ic->arg[0] = iword;
 3657| 				if (d == M88K_ZERO_REG)
 3658| 					ic->f = instr(nop);
 3659| 			}
 3660| 		} else switch ((iword >> 8) & 0xff) {
~~~~

### 8.4 `src/cpus/cpu_m88k_instr.c` -- where the generated table enters the build, and this file's copy of the index constants (lines 292-304)
~~~~
  292| /*  Include all automatically generated bcnd and bcnd.n instructions:  */
  293| #include "tmp_m88k_bcnd.c"
  294| 
  295| 
  296| /*  Include all automatically generated load/store instructions:  */
  297| #include "tmp_m88k_loadstore.c"
  298| #define M88K_LOADSTORE_STORE            4
  299| #define M88K_LOADSTORE_SIGNEDNESS       8
  300| #define M88K_LOADSTORE_ENDIANNESS       16
  301| #define M88K_LOADSTORE_SCALEDNESS       32
  302| #define M88K_LOADSTORE_USR              64
  303| #define M88K_LOADSTORE_REGISTEROFFSET   128
  304| #define	M88K_LOADSTORE_NO_PC_SYNC	256
~~~~

### 8.5 `src/cpus/cpu_dyntrans.c` -- the NULL-`ic->f` check and the `bad:` path that stops the CPU (lines 1901-1909, 1983-2014; anchor `INTERNAL ERROR: ic->f == NULL!`, unique)
~~~~
 1901| 	/*  An additional check, to catch some bugs:  */
 1902| 	if (ic->f == TO_BE_TRANSLATED) {
 1903| 		fatal("INTERNAL ERROR: ic->f not set!\n");
 1904| 		goto bad;
 1905| 	}
 1906| 	if (ic->f == NULL) {
 1907| 		fatal("INTERNAL ERROR: ic->f == NULL!\n");
 1908| 		goto bad;
 1909| 	}
  ...
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

### 8.6 `src/cpus/cpu_m88k_instr_loadstore.c` -- the address computation (generic, then fast handler) and the byte load (lines 57-73, 246-256, 295-304; not edited by the repair)
~~~~
   57| #ifdef LS_INCLUDE_GENERIC
   58| void LS_GENERIC_N(struct cpu *cpu, struct m88k_instr_call *ic)
   59| {
   60| #ifdef LS_USR
   61| 	const int memory_rw_flags = CACHE_DATA | MEMORY_USER_ACCESS;
   62| #else
   63| 	const int memory_rw_flags = CACHE_DATA;
   64| #endif
   65| 	uint32_t addr = reg(ic->arg[1]) +
   66| #ifdef LS_REGOFS
   67| #ifdef LS_SCALED
   68| 	    LS_SIZE *
   69| #endif
   70| 	    reg(ic->arg[2]);
   71| #else
   72| 	    ic->arg[2];
   73| #endif
  ...
  246| void LS_N(struct cpu *cpu, struct m88k_instr_call *ic)
  247| {
  248| 	uint32_t addr = reg(ic->arg[1]) +
  249| #ifdef LS_REGOFS
  250| #ifdef LS_SCALED
  251| 	    LS_SIZE *
  252| #endif
  253| 	    reg(ic->arg[2]);
  254| #else
  255| 	    ic->arg[2];
  256| #endif
  ...
  295| #ifdef LS_LOAD
  296| 	/*  Load:  */
  297| 
  298| #ifdef LS_1
  299| 	reg(ic->arg[0]) =
  300| #ifdef LS_SIGNED
  301| 	    (int8_t)
  302| #endif
  303| 	    p[addr];
  304| #endif	/*  LS_1  */
~~~~

### 8.7 `src/cpus/Makefile.skel` -- how the table is built (lines 128-135)
~~~~
  128| cpu_m88k.o: cpu_m88k.c cpu_m88k_instr.c cpu_dyntrans.c memory_rw.c \
  129| 	tmp_m88k_loadstore.c tmp_m88k_head.c tmp_m88k_tail.c tmp_m88k_bcnd.c
  130| 
  131| tmp_m88k_bcnd.c: generate_m88k_bcnd
  132| 	./generate_m88k_bcnd > tmp_m88k_bcnd.c
  133| 
  134| tmp_m88k_loadstore.c: cpu_m88k_instr_loadstore.c generate_m88k_loadstore
  135| 	./generate_m88k_loadstore > tmp_m88k_loadstore.c
~~~~

### 8.8 Byte order -- the constructor and the two later writers (P1)
~~~~
src/cpus/cpu_m88k.c (the m88k CPU constructor):
  127| 	cpu->cd.m88k.cpu_type = cpu_type_defs[found];
  128| 	cpu->name            = strdup(cpu->cd.m88k.cpu_type.name);
  129| 	cpu->is_32bit        = 1;
  130| 	cpu->byte_order      = EMUL_BIG_ENDIAN;
  131| 

src/core/emul.c (machine setup, after the CPU is constructed):
  633| 		byte_order = NO_BYTE_ORDER_OVERRIDE;
  634| 
  635| 		/*
  636| 		 *  Load the file:  :-)
  637| 		 */
  638| 		file_load(m, m->memory, name_to_load, &entrypoint,
  639| 		    cpu->cpu_family->arch, &gp, &byte_order, &toc);
  ...
  651| 		if (byte_order != NO_BYTE_ORDER_OVERRIDE)
  652| 			cpu->byte_order = byte_order;
  ...
  737| 	if (m->byte_order_override != NO_BYTE_ORDER_OVERRIDE)
  738| 		cpu->byte_order = m->byte_order_override;
  739| 
  740| 	/*  Same byte order and entrypoint for all CPUs:  */
  741| 	for (i=0; i<m->ncpus; i++)
  742| 		if (i != m->bootstrap_cpu) {
  743| 			m->cpus[i]->byte_order = cpu->byte_order;
  744| 			m->cpus[i]->pc = cpu->pc;
  745| 		}

src/core/emul_parse.c (configuration-file machine settings):
  493| 		m->byte_order_override = NO_BYTE_ORDER_OVERRIDE;
  494| 		if (cur_machine_byte_order[0]) {
  495| 			if (strncasecmp(cur_machine_byte_order, "big", 3) == 0)
  496| 				m->byte_order_override = EMUL_BIG_ENDIAN;
  497| 			else if (strncasecmp(cur_machine_byte_order, "little",
  498| 			    6) == 0)
  499| 				m->byte_order_override = EMUL_LITTLE_ENDIAN;
  500| 			else {
  501| 				fatal("Byte order must be big-endian or"
  502| 				    " little-endian\n");
  503| 				exit(1);
  504| 			}
  505| 		}

src/file/file_elf.c (the ELF loader's reported byte order):
  693| 	if (encoding == ELFDATA2LSB)
  694| 		*byte_order = EMUL_LITTLE_ENDIAN;
  695| 	else
  696| 		*byte_order = EMUL_BIG_ENDIAN;
~~~~

### 8.9 MC88100 User's Manual -- `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\mc88100.txt` (OCR text; lines 2960-2965, 6421-6429, 6455-6460)
Anchors: `but the result is identical` (unique, 2965); `define scale factors of one and` (unique, 6459).
~~~~
 2960| 5UBOPCODE  This field identifies the particular instruction (ld, st, xmem, Ida), including
 2961|            the scaling factor for the memory data. When the source 2 operand is
 2962|            scaled, it is shifted by 0, 1, 2, or 3 bits (multiplied by scale factor 1, 2, 4,
 2963|            or 8) for byte, half-word, word, or double-word accesses, respectively. For
 2964|            byte accesses, the 5UBOPCODE field is distinctly different from the register
 2965|            indirect with index (unscaled) cases but the result is identical.
  ...
 6421|                        SCALED
 6422| 
 6423|              xmem.bu      rD,rS 1[rS2]
 6424| 
 6425|              xmem         rD,rS 1[rS2]
 6426| 
 6427|              xmem.bu.usr  rD,rS 1[rS2]
 6428| 
 6429|              xmem.usr     rD,rS 1[rS2]
  ...
 6455|       The xmem instruction with no options specifies a 32-bit operation. The .bu option
 6456|       specifies an unsigned byte (8 bits).
 6457| 
 6458|       For the scaled index modes, the scale factor is determined by the size option of the
 6459|       instruction. Operations that are byte and word in size define scale factors of one and
 6460|       four respectively, when the rS2 field is specified within square [ ].
~~~~

---

## 9. Detector-shape facts for Q3 (VERBATIM excerpts at HEAD)

### 9.1 The `#include` differential pattern -- exemplar `regress/diff_memory_rw.c` (header comment; the include, lines 133-135)
~~~~
    1| /*
    2|  *  Offline differential for the SHIPPED memory slow path -- src/cpus/memory_rw.c.
    3|  *
    4|  *  WHY THIS EXISTS.  #430 changed where memory_rw() translates, and the defect it fixes is
    5|  *  invisible to anything that only watches a guest boot: it needs two pages that are
    6|  *  adjacent VIRTUALLY and NOT adjacent physically, which no rig in this tree can be made to
    7|  *  produce on demand.  So the map is supplied by a stub and the whole thing runs offline.
    8|  *
    9|  *  IT IS THE REPOSITORY FILE.  memory_rw.c is never compiled on its own -- it is #included
   10|  *  by the per-CPU files with MEMORY_RW #defined to the flavour's name (see
   11|  *  tmp_ppc_tail.c:38).  This driver does exactly that, with NO family macro.
   12|  *
   13|  *  SAID CORRECTLY, because the first version of this comment gave a wrong reason: every
   14|  *  family DOES get a MEM_<FAMILY> macro (generate_tail.c:107 emits one, and
   15|  *  tmp_ppc_tail.c carries MEM_PPC).  What makes the no-macro build representative is
   16|  *  narrower, and it is the fact that actually matters -- memory_rw.c only ever TESTS
   17|  *  MEM_ALPHA, MEM_MIPS and MEM_M88K, so PPC/ARM/SH/RISC-V/i960 all compile the same
   18|  *  text this driver compiles.  Nothing is transcribed; there is nothing to keep in sync.
  ...
  133| #define	MEMORY_RW	test_memory_rw
  134| #include "../src/cpus/memory_rw.c"
  135| #undef MEMORY_RW
~~~~
How `regress/gate_offline.sh` (GATE 2, "offline-differential") compiles and pins it:
~~~~
  477| MRWBIN=$LOGDIR/diff_memory_rw
  478| MRWLOG=$LOGDIR/diff_memory_rw.log
  479| #  -fno-optimize-sibling-calls IS LOAD-BEARING, and only for the stack row.  gcc 15.2.1
  480| #  DOES eliminate the tail call at -O2, so a recursion mutant measured a 96-byte span and
  481| #  the "it is a loop" row passed under the very defect it exists to catch -- vacuous.
  482| #  With the flag: loop 0 bytes, recursion 1,572,768.  Measured both ways by a review seat.
  483| if ! $CC -O2 -fno-optimize-sibling-calls -std=c99 -D_POSIX_C_SOURCE=200809L \
  484|         -D_DEFAULT_SOURCE -I"$SEC/src" \
  485|         -o "$MRWBIN" "$HERE/diff_memory_rw.c" -lm > "$MRWLOG" 2>&1; then
  486|     note "memory_rw differential compile failed:"; sed 's/^/       /' "$MRWLOG" | head -12
  487|     check "memory_rw: compiles against the real memory_rw.c" "no" "yes"
  488| else
  489|     check "memory_rw: compiles against the real memory_rw.c" "yes" "yes"
  490|     "$MRWBIN" > "$MRWLOG" 2>&1
  491|     sed 's/^/       /' "$MRWLOG"
  492|     check     "memory_rw: row failures" \
  493|               "$(grep -oE '[0-9]+ failures' "$MRWLOG" | grep -oE '^[0-9]+')" "0"
  ... (lines 494-516: a comment on how the row-count floor once drifted)
  517|     check_min "memory_rw: rows actually run" \
  518|               "$(grep -oE '^[0-9]+ rows' "$MRWLOG" | grep -oE '^[0-9]+')" 23
  519|     check     "memory_rw: offline verdict" "$(grep -c 'DIFF_MEMORY_RW_PASS' "$MRWLOG")" "1"
  520|     #  Name each row that is the SOLE detector of something, so deleting one is a red row
  521|     #  rather than a quieter file.
  522|     check "memory_rw: the straddling-read row is present" \
  523|           "$(grep -c 'straddling read takes the VIRT-next page' "$MRWLOG")" "1"
  ...
  545|     check "memory_rw: the identity row is present" \
  546|           "$(grep -c 'IDENTITY row count' "$MRWLOG")" "1"
~~~~
And GATE 2's self-variant manifest, where each differential names the product file its self-test alters
(lines 982-986):
~~~~
  982| selfmutant_one diff_timer.c      src/core/timer.c            timer      "NaN"
  983| selfmutant_one diff_memory_rw.c  src/cpus/memory_rw.c        memory_rw  "G1 " "-fno-optimize-sibling-calls"
  984| selfmutant_one diff_footbridge.c src/devices/dev_footbridge.c footbridge "A1 "
  985| selfmutant_one diff_m8820x.c     src/devices/dev_m8820x.c    m8820x     "D3"
  986| selfmutant_one diff_m8invread.c  src/devices/dev_m8820x.c    m8invread  "F1 "
~~~~

### 9.2 The committed-generated-table idiom already in GATE 2 -- the `#375` block, which reads the COMMITTED MIPS table by index with no compiler
~~~~
   26| # #375: the mips*_loadstore[32] dispatch-table index is a SILENT CROSS-FILE
   27| # COUPLING. generate_mips_loadstore.c emits the table in the loop order
   28| # `endianness -> store -> size -> signedness`, so an entry's index is
   29| # endianness*16 + store*8 + size*2 + signedness. That arithmetic is then
   30| # hard-coded BY HAND, with no comment and no check, at a dozen sites: the
   31| # multi-transfer fold's bail (`mips32_loadstore[5]` = plain lw), the coproc
   32| # handlers (lwc1->5, swc1->12, ldc1->7, sdc1->14), the canonical decoder, and
   33| # the COMBINE(nop)/strlen/#169 matcher slots. Reorder that one generator loop
   34| # and every hand-coded index silently mis-resolves -- the fold bail dispatches
   35| # the wrong access SIZE, ldc1 becomes lw -- and NOTHING fails to compile. These
   36| # rows turn the coupling into a checked invariant, offline, needing no compiler
   37| # and no rig (only the committed generated table). Found by the #46 MIPS-combiner
   38| # audit; both boot rigs are LE, so the _be entries are dead code on the harness
   39| # but the coupling is real for any future BE MIPS work.
  ...
   47| MIPSLS=$SEC/src/cpus/tmp_mips_loadstore.c
   48| need_file "$MIPSLS"
   49| 
   50| #  ls_entry <array-name> <index> -> the function symbol at that index, read from
   51| #  the committed generated table (the [32] arrays, not the [16] generic ones).
   52| ls_entry() {
   53|     awk -v arr="$1" -v idx="$2" '
   54|         $0 ~ ("\\*" arr "\\[32\\]") { f = 1; n = 0; next }
   55|         f && /^};/ { f = 0 }
   56|         f { gsub(/[ \t,};]/, "");
   57|             if ($0 != "") { if (n == idx) { print $0; exit } n++ } }
   58|     ' "$MIPSLS"
   59| }
   60| 
   61| for arr in mips32_loadstore mips_loadstore; do
   62|     pfx=${arr%_loadstore}
   63|     check "  $arr[5]  = plain word-load LE"  "$(ls_entry $arr 5)"  "${pfx}_instr_l4_le"
   64|     check "  $arr[12] = plain word-store LE" "$(ls_entry $arr 12)" "${pfx}_instr_s4_le"
   65|     check "  $arr[21] = plain word-load BE"  "$(ls_entry $arr 21)" "${pfx}_instr_l4_be"
   66|     check "  $arr byte-load LE/BE share [1]==[17]" \
   67|         "$([ "$(ls_entry $arr 1)" = "$(ls_entry $arr 17)" ] && echo same || echo differ)" "same"
   68|     check "  $arr byte-store LE/BE share [8]==[24]" \
   69|         "$([ "$(ls_entry $arr 8)" = "$(ls_entry $arr 24)" ] && echo same || echo differ)" "same"
   70|     check "  $arr word-load LE != BE [5]!=[21]" \
   71|         "$([ "$(ls_entry $arr 5)" != "$(ls_entry $arr 21)" ] && echo differ || echo same)" "differ"
   72| done
~~~~

### 9.3 The m88k probe gate -- GATE 11, `regress/gate_m88k_rounding.sh`
Its `m88k_exc_probe.py` is a cold-debugger probe on the unmodified `testm88k` machine, pinned by a denominator
EQUALITY:
~~~~
  342| EXCLOG=$LOGDIR/m88k_exc.log
  343| python3 m88k_exc_probe.py "$PMAX" > "$EXCLOG" 2>&1 || true
  344| grep -E "^M88KEXC_(ROW|RESULT|SELFTEST|CONTROLS)" "$EXCLOG" | cut -c1-110 | sed 's/^/       /'
  345| 
  346| if ! grep -q "M88KEXC_DONE" "$EXCLOG"; then
  347|     note "m88k exception-delivery probe produced no completion sentinel; last lines follow"
  348|     tail -5 "$EXCLOG" | sed 's/^/       /'
  349|     check "m88k exc: probe completed" "no" "yes"
  350| else
  351|     check "m88k exc: CR parse self-test (PSR at reset == 0x80000002)" \
  352|           "$(grep -c 'M88KEXC_SELFTEST=OK' "$EXCLOG")" "1"
  353|     check "m88k exc: 84 fault rows, all as expected (the denominator is the pin)" \
  354|           "$(grep -c 'M88KEXC_RESULT=84/84' "$EXCLOG")" "1"
~~~~

---

## 10. The project rules the questions apply -- quoted with their bounds

**Provenance, plainly:** these are quoted from the WORKING-TREE carrier `GXEMUL-SEC/tools/CLAUDE.md` (byte-identical to
the root `CLAUDE.md` every session loads).  Several were adopted by owner ruling on 2026-10-09 and are **NOT
COMMITTED at HEAD `cb2eba1e`**: HEAD's carrier still states clause (c) as "fails on a null medium (a stale copy, a
comment-only file -- i.e. it carries identity rows)", and HEAD's `tools/BRIEF_TEMPLATE.md` (702 lines) has no section
on the null medium or on rule D2.  They are the rules this round is held to, and they travel here WITH their bounds:
a rule quoted without its bound is a different rule.

**R1 -- THE FLOOR** -- `tools/CLAUDE.md` (working tree) lines 1328-1333, VERBATIM:
~~~~
 1328| > **THE FLOOR.** A detector is VACUOUS — replace it IN-ROUND — unless it (a) fails on the
 1329| > pre-fix build, (b) fails on a **VERBATIM REINSTATEMENT of the removed defect at EVERY fixed
 1330| > site**, and (c) fails on a **NULL MEDIUM** -- a product medium carrying none of the behaviour under
 1331| > test (the clause-(c) block below says what that is per instrument kind). Below the floor, the
 1332| > round's own claim to have "shipped a detector with the fix" is a WRONG RECORD, which the
 1333| > stopping rule already fixes in-round.
~~~~

**R2 -- clause (c): the null medium by instrument kind, the pre-fix build, the two record forms** -- `tools/CLAUDE.md` (working tree) lines 1340-1367, VERBATIM:
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

**R3 -- clause (d)** -- `tools/CLAUDE.md` (working tree) lines 1376-1377, VERBATIM:
~~~~
 1376| > **(d) The detector must also fail when the fix is PRESENT but its REPAIR IS NULLED —
 1377| > the guard kept, its effect removed.**
~~~~

**R4 -- the two (d) shapes, including the pure-deletion form** -- `tools/CLAUDE.md` (working tree) lines 1428-1433, VERBATIM:
~~~~
 1428| > **The two shapes, once the enumeration is right:**
 1429| > * **fix ADDS a predicate** -> weaken the added one (unchanged; the original rule).
 1430| > * **fix adds none** -> the (d) mutant reroutes an EXISTING guard's repair. For a
 1431| >   de-fatalisation: **swap the guard's operand for a field the guarded BODY reads.**
 1432| >   For a pure deletion: **re-introduce the removed behaviour under a DIFFERENT predicate**
 1433| >   -- not the same one widened, which is (b) wearing (d)'s clothes.
~~~~

**R5 -- the DEPENDS-ON bound** -- `tools/CLAUDE.md` (working tree) lines 1448-1451, VERBATIM:
~~~~
 1448| > > **DEPENDS ON enumerates exactly two things: (1) the predicates DOMINATING the diff's
 1449| > > edited lines, walked up only to the ENCLOSING FUNCTION BOUNDARY -- never into callees
 1450| > > or callers; and (2) for operand-swap forms, swaps drawn ONLY from fields the guarded
 1451| > > BODY reads (the guard-field/body-field grep the pre-table check already mandates).**
~~~~

**R6 -- joint cells: the body-tested partition** -- `tools/CLAUDE.md` (working tree) lines 1464-1472, VERBATIM:
~~~~
 1464| > > **DEPENDS-ON enumerates JOINT cells over the guard's operands and the body-read lvalues EXACTLY
 1465| > > WHEN THE GUARDED BODY'S OWN CODE DISTINGUISHES THEM.**  For each lvalue take the PARTITION the
 1466| > > body's own tests induce (`pending > 0` gives {0, >0}; `relative_addr == PCCTWO_T1ICR` gives
 1467| > > {T1, T2}); the enumerated cells are the CROSS-PRODUCT of those partitions -- never arbitrary
 1468| > > boolean functions of the read-set.  A mutant exempting a single cell whose reachability is
 1469| > > MEASURED is a floor breach; close the whole cross-product in ONE diff and write into the
 1470| > > contract which cells are rowed.  A value or combination the body never tests as a case
 1471| > > (`idata == k`; a byte no conditional distinguishes; both counts >= 2 where the body tests `> 0`)
 1472| > > is DISCLOSED under clause (e).
~~~~

**R7 -- the floor (cells a row is OWED for) versus clause-(e) disclosure** -- `tools/CLAUDE.md` (working tree) lines 1517-1522, VERBATIM:
~~~~
 1517| > > **The rule ENUMERATES joint cells wherever the body distinguishes them; the FLOOR -- the cells a row
 1518| > > is OWED for -- is the cross-product of the guard's dominating predicates with the device-STATE lvalues
 1519| > > the fix's own repair path reads that are JOINTLY REACHABLE through its own data flow.**  The bits of
 1520| > > the single value being written are single-operand MARGINALS, not floor; joint cells outside the floor
 1521| > > are clause-(e) coverage debt, subject to the one ask-again.  A filter may reject or discharge a cell
 1522| > > but may demand a new row only for a floor cell -- so it cannot grow unbounded.
~~~~

**R8 -- rule D2: a relational compare is pinned at its edges** -- `tools/CLAUDE.md` (working tree) lines 1557-1566, VERBATIM:
~~~~
 1557| > > For a relational compare against a constant bound B that a fix DEPENDS ON (`X > B`, `e < 96`), each region of its
 1558| > > generating set is discharged by the row that varies under the LEAST-OBSERVABLE non-equivalent move of B: **X = B+1
 1559| > > for the region past the bound and X = B-1 for the region below it** (the "at" member is dead where the branch maps B
 1560| > > to itself).  **A far row proves the branch EXISTS and discharges the BRANCH partition; it never pins the BOUND.**
 1561| > > Measured on `#473`'s shipped WDC detector: its rows at 68928 and 4998 let `> 32769` and `> 32766` at each clamp --
 1562| > > one-token bound moves -- pass all 128 rows, while rows at 32769 and 32767 red each one
 1563| > > (`regress/artifacts/wdc473floor/pass1_20261009/fable5_meas/`).  **Bound: at most two rows per compare the fix
 1564| > > depends on -- the compare's own two edges.**  It adds no axis; it moves the rows a region already owes to where the
 1565| > > bound is observable, so it cannot become `#392`.  It is the accept-row finding -- *a single accept row pins exactly
 1566| > > ONE bound, the one it is near* -- stated for compares.
~~~~

**R9 -- the CHANNEL line (one row of the pre-table check's table)** -- `tools/CLAUDE.md` (working tree) lines 1741-1741, VERBATIM:
~~~~
 1741| > | **CHANNEL** | for each row, name **the mutant it kills** and **the observable that differs under that mutant**. A row whose named channel cannot vary under its named mutant is VACUOUS BY CONSTRUCTION, and that is knowable at writing time, before any table runs | a survival oracle at a REFUSAL-EFFECT site: guarded and unguarded code both survive |
~~~~

**R10 -- clause (e): the contract** -- `tools/CLAUDE.md` (working tree) lines 1801-1805, VERBATIM:
~~~~
 1801| > **(e) THE CONTRACT.** The probe header names which edits this detector is designed
 1802| > to catch. *A detector that says so is falsifiable; one claiming completeness is
 1803| > not* -- and a later escape becomes "outside the contract" or "a breach of it",
 1804| > which are different dispositions, rather than an argument about overclaiming.
 1805| > Two lines in a header.
~~~~

**R11 -- clause (f): the anchor rule** -- `tools/CLAUDE.md` (working tree) lines 1814-1817, VERBATIM:
~~~~
 1814| > **Rows that assert only PAIRWISE DISTINCTNESS, or a same-path round-trip, test the decode
 1815| > against ITSELF.** They are therefore invariant under any edit that re-maps addresses
 1816| > INJECTIVELY over the probed set -- translations first among them -- and they catch a re-map
 1817| > only where it COLLIDES on that set.
~~~~

**R12 -- the de-escalation clause** -- `tools/CLAUDE.md` (working tree) lines 2406-2415, VERBATIM:
~~~~
 2406| > **A fatal→survive fix DELETES THE ACCIDENTAL TRIPWIRE that made guard-mask growth
 2407| > self-announcing.** Before #447, adding `| TCR_UNIE` to a guard mask meant `exit(1)` on the
 2408| > first legal write — unmissable. After it, the same edit means a **silently refused write** and
 2409| > nothing anywhere notices.
 2410| >
 2411| > So: **when a fix removes a host-fatal guard, enumerate from the diff every predicate that used
 2412| > to gate death, and the detector shipping with that fix must pin the ACCEPT SIDE of each** — a
 2413| > row per adjacent modelled bit or value, proving legal writes still land. Those rows are part
 2414| > of the FIX'S COST, not future strengthening, because the fix itself destroyed the old
 2415| > (accidental) detector for that class.
~~~~

**R13 -- accept-row failability, by its discriminator** -- `tools/CLAUDE.md` (working tree) lines 2452-2458, VERBATIM:
~~~~
 2452| > **THE RULE, BY ITS DISCRIMINATOR:** the accept row must redden under the **least-observable
 2453| > growth form that is measured NON-EQUIVALENT at that site**. Find it by the reading the rule
 2454| > already mandates — read the latch/store arm and cite its line. Where the latch operand CAN
 2455| > mask the guard, guard-only is equivalent and JOINT is that form. Where the latch operand is a
 2456| > constant the guard cannot feed, guard-only is non-equivalent AND quieter, so it is that form.
 2457| > **"Build the form the latch operand does not mask"** is the generalisation, and it is not a
 2458| > new rule — it is this rule's own reason made explicit.
~~~~

---

## 11. QUESTIONS -- VERDICT LINE FIRST (format in section 0)
**THIS FIRING ANSWERS Q1 AND Q2 ONLY.**  Q3 and Q4 go to a separate firing of this same packet; do not answer them here.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

**Q1 -- the repair: complete and correct?**

(a) Is the agreed table-alias repair -- remove the arm at `generate_m88k_loadstore.c:254-257`, keep `loadstore()`'s
early return at :104-105, do not edit the decoder -- complete and correct for BOTH the `xmem` load slot (:2377-2395)
and the `xmem` store slot (:2411-2426), and for EVERY one of the 24 slots in section 7?  Per slot it is one comparison:
does the repaired entry name the handler the architecture requires (S7) for that (kind, `.usr`, PC-sync) cell?  Walk
the 24; do not reason about "all of them".  Say whether aliasing the slots with no producer today (P2, P3) is correct,
and whether it is needed.

(b) Does keeping the early return at :104-105 avoid the duplicate definitions (S9)?  Does removing the arm change any
OTHER generated output -- the separator logic (:235-237), the `generated_functions` count printed to stderr
(:266-267), the remaining 272 `NULL` entries?

(c) P5: name the exact lines the repair removes.

(d) P4: does the repair owe the committed `tmp_m88k_loadstore.c` regenerated in the same diff -- and `est/` and the
build trees updated (all four hold byte-identical copies today; neither file is in the declared divergence set)?

(e) The premise audit: answer P1, P2 and P3.  Say which of S1-S14 you re-derived from something this brief did NOT
give you -- that is the only kind of agreement that counts.

(f) Option-set completeness: is there a disposition for these 24 slots that this brief did not name?  The fork's own
idiom for "two table slots that must behave identically" is the endianness alias in this same table (S8).  Grep the
fork for others before answering.

(g) Is the CPU-stop half of the class (scaled `ld.b` / `ld.bu` / `st.b`, S6) fully closed by the same change?  After
N2's eventual fix (P2), are the slots that gain a producer already correct under this repair?

**Q2 -- the owed rows: complete, consistent with each other, bounded?**

The seats' row specifications are in section 3.2 ("The round owes:" -- floor, DEPENDS-ON, accept controls) and section
3.3 ("Floor, channel is the exchanged byte:" -- (a)-(d), accept, growth).  The rules are in section 10.

(a) **The floor, clause by clause.**  For each of (a) pre-fix red, (b) verbatim reinstatement "at EVERY fixed site",
(c) the null medium, (d) the nulled repair: which owed row carries it, and on which observable does it differ (R9,
the CHANNEL line)?  In particular:
  - (a): both seats state the pre-fix red as a guest-path exchange.  Under the owner's offline ruling, what is the
    pre-fix red?
  - (b): if P4's answer is "regenerate the committed table", is the committed table a second fixed site?
  - (c): both seats name an IDENTITY BODY ("an identity `xmem` body that retires without exchanging anything";
    "decode, retire, write neither rD nor memory"); P6 says why.  R2 picks the medium by instrument kind.  For the
    shape you choose in Q3, which medium applies, and in which of R2's TWO record forms?
  - (d): the repair is a PURE DELETION -- it removes an arm and adds no predicate.  R4: "For a pure deletion:
    re-introduce the removed behaviour under a DIFFERENT predicate -- not the same one widened, which is (b) wearing
    (d)'s clothes."

(b) **The candidate variants the two seats named.**  For EACH: is it a clause-(d) form or a partial clause (b)?  Is it
EQUIVALENT to the repaired generator, or does it produce a different table?  At which table index (section 7) do the
two first differ?  *(This replaces the template's "smallest edit" question with its standing substitute: the
candidates are supplied, and the question is equivalence and first difference.)*
  - **v1** Grok: "`&& no_pc_sync` leaves scaled `ld.b` dead"
  - **v2** Grok: "`&& !no_pc_sync` leaves xmem dead"
  - **v3** Grok: "one signed scaled `ld.b` (xmem never sets `SIGNEDNESS`)"
  - **v4** Grok: "one `.usr` scaled `ld.b` or `st.b` (a legal `xmem.usr` still indexes the non-usr slot, which is N2)"
  - **v5** Astra: "repair-null variants that retain selection but omit the required mapping or effect" -- say what
    concrete forms this denotes, and whether v1-v4 are instances of it
  - **v6** the growth variant, Grok: "widening `size == 0` so a scaled half or word slot is aliased to the byte
    function" -- after the repair the arm at :254 is gone; say which remaining `size` test it names:
    `print_function_name()` :74 (`size == 0 && endianness`) or :80 (`scaledness && size > 0`), or `loadstore()` :101
    or :104
  *Notation check before answering:* Grok's v1 and v2 attach the conjunct to the REPAIR ("`&& no_pc_sync` leaves
  scaled `ld.b` dead" reads as: the `NULL` arm survives on the complement).  Confirm that reading.

(c) **DEPENDS-ON.**  The edited lines (:254-257) sit in `main()`; inside `main()` the predicates dominating them are
the three earlier `NULL` arms (:239-252) and the loop bounds.  But the alias's correctness lives in a CALLEE,
`print_function_name()` (:74-75, :80-81), and R5 bounds the enumeration "only to the ENCLOSING FUNCTION BOUNDARY --
never into callees or callers".  Are :80's `scaledness && size > 0` and :74's `size == 0 && endianness` floor axes of
this round, or clause-(e) disclosures?  Then reconcile the two enumerations -- Astra: "There are **24 valid repaired
entries**: `{unsigned load, signed load, store} × {LE, BE} × {ordinary, .usr} × {PC-sync, no-PC-sync}`"; Grok:
"`no_pc_sync` × {load, store}", "one signed scaled `ld.b`", "one `.usr` scaled `ld.b` or `st.b`", "endianness is not
a floor axis".  Which set is the FLOOR (R7: the cells a row is OWED for) and which is clause-(e) disclosure?  Use
section 7's producer table and your answers to P1-P3.

(d) **Accept rows, the de-escalation clause, rule D2.**  The repair removes slots that ended the process or stopped
the CPU, so R12 owes accept rows for "every predicate that used to gate death" -- here `size == 0 && scaledness`.
Both seats' accept controls sit at scaled WORD (Grok: "a scaled word `xmem` still uses scale 4 where `rS2*4` differs
from `rS2`"; Astra: "scaled wider operations").  R8 (rule D2): a relational compare against a constant the fix
depends on is pinned at its edges B+1 and B-1.  :80's `size > 0` has B = 0, so its B+1 edge is size 1 (halfword,
scale 2) -- and `xmem` has no halfword form, so a halfword row exists only on the `ld`/`st` side.  Does R8, or R12's
"a row per adjacent modelled bit or value", owe a scaled-HALFWORD accept row?  Would v6, if it reaches halfword slots, pass a
word-only accept row?  (If your (c) answer puts :80 outside the floor, say how that changes this one.)

(e) **Anchoring.**  Astra: "Check each against its corresponding unscaled entry."  That compares slot i with slot
i - 32 -- a RELATIVE oracle.  R11 says relative rows "test the decode against ITSELF".  Is a relative comparison
satisfied by an edit that changes slot i and slot i - 32 together?  Does the census owe an absolute form (the expected
handler named per slot)?

(f) **Bounded?**  Is the resulting row set finite and closed over the diff (not the `#392` shape -- six follow-up
passes that never converged)?  Name the bound you rely on.

(g) For each row you keep: the variant it detects, and the observable that differs under it (R9).

**Q3 -- the detector's shape: which, and what does the gate row pin?**

Facts: section 9 and S14.  The owner ruling (section 2) is an OFFLINE regression detector under `detector:<path>`.

(a) Which shape carries the owed rows: an `#include` differential in the `regress/diff_*.c` pattern (exemplar
`regress/diff_memory_rw.c`, compiled and pinned by `regress/gate_offline.sh`, section 9.1); the committed-generated-
table reader of GATE 2's `#375` block (section 9.2); or both?  Weigh P4: the build regenerates the table from the
generator (S14), while the `#375` idiom reads the COMMITTED copy -- what does each shape see if only the generator is
reverted, or only the committed table?  Note that this round's product is a build-time program with its own
`main()` (section 8.1) plus its generated output (section 8.4), not a device file.

(b) What exactly does the gate row pin -- exact handler names at named indices?  the `NULL` count (272 after the
repair)?  slot-to-counterpart equality?  a compile row?  And in which form -- equality, `check_min`, presence?  (R2:
a by-construction clause-(c) claim fails its reading where the gate pins with `check_min` or not at all.)

(c) Clause (c) for the shape you choose: which null medium, and which record form (cross-reference Q2(a)).

(d) The probe-gate alternative (GATE 11, section 9.3) is listed because it exists.  For this round answer ONLY: is any
FLOOR cell observable ONLY on a guest path?  If so, name the cell and stop.  Do not design or sketch the guest program.

**Q4 -- the standing licence.**

If, while verifying a claim, you found something ELSE -- say so.

---

*Every path named in this brief was checked to exist at drafting time (none missing); the FULL form of this brief
carries the `ls` listing.*
