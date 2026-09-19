# `alphavmkill` (#541) PASS 1 -- CONSOLIDATED FINDINGS for the fable5 seat (LAST; every other seat has answered)

**Tree:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` at HEAD `cdbe7d7`.  `memory_alpha.c` and `cpu_dyntrans.c` are
unmodified in the working tree.  **Use absolute paths.**  `C:\DocumentNoSnc\CC\GXEMUL\src\` is pristine 2021 upstream.
**The brief:** `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\panel_20260918_223507\brief_sent.md`.  **Every answer is in
that directory:**
- `codex.txt`, `kimi.txt` -- CLIs; the answer is the last `VERDICT:` block.
- `codex_adv541p1.txt` -- the dedicated job.
- `grok.txt`, `agy.txt`.
- `ollama_{glm,deepseek,minimax,kimi}.txt`.
- `opus5_p1.md`.

## VERDICTS (the member of the option set)

    3  DECLINE + LATCHED ANNOUNCE   agy, glm, kimi-k3, grok, codex (panel), codex_adv541p1, kimi CLI
    2  DECLINE silently             deepseek, minimax
    4  ACCEPT + latch               opus5 -- "the only member that fixes all three cells in-round"

## A MEASUREMENT, taken AFTER the seats answered, to settle the facts under the disagreement

**No build; the committed binary, at NEIGHBOUR addresses the trap does not cover.**  The Opus seat's proposal:
`regress/artifacts/alphavmkill/neighbours_20260918/RESULT.out`, with transcript and frozen instrument alongside.

    controls          live 0xaaaa0000aaaa, signature "HWRPB" (the base==0 arm's remap; also proves kernel mode, ptbr 0)
    LOAD  0xfffffffd80000008   dest 0x0 (identity -> past RAM -> zero-fill); the next instruction RAN (mark 0x1234)
    STORE 0xfffffffd80000008   dropped; the next instruction RAN (mark 0x5678)
    FETCH 0xfffffffd80002000   `[ Alpha PALcode 0x0 unimplemented! ]', `All machines stopped', pc = 0xfffffffd80002000,
                               the process ALIVE and it exits cleanly at `quit' (wait status 0)
    `non-existant' memory warnings: 4 (verbosity-gated)

**So member 4's behaviour, as Opus derived it, is what the neighbours ALREADY do on this build**:
- loads read 0;
- stores drop;
- a fetch halts that CPU through PAL 0, and the host survives.

**Members 2/3 fix LOAD and STORE, but leave FETCH dying.**  It dies at `cpu_dyntrans.c:729-733`, now WITNESSED at rung
3 as `alphaifetchkill`.  Session B of the same instrument: arm paging (swpctx to a zero L1[0]; the arming control keeps
its sentinel), then one JMP to a raw VA.  Result: two `wasn't found` lines for exactly that VA, then
`FATAL: could not find physical address of the exception handler?`, and wait status 256
(`regress/artifacts/alphaifetchkill/witness_HEAD_20260918/`).

## FINDINGS AND MY DISPOSITIONS

**H1. The deciding question is a DESIGN one, and the measurement sharpens it.**  Member 4 keeps the arm's own policy:
every other address in the `base == 0` window is identity-mapped, and this one address is the sole hole.  It fixes all
three cells in-round and gives loads a deterministic 0.  Members 2/3 "do not invent a translation", but:
- they leave loads with a STALE register: #215 abandons the access, and the witness's sentinel would survive;
- they leave STx_C's status register holding the data (Opus);
- they hand the fetch cell to `alphaifetchkill`.

**MY LEANING: 4 + latch** (keep the `fatal()`, latched once per CPU instance; drop `exit(1)`).  The majority is 3.
Count the arguments, not the seats.  **Rule on the argument.**

**H2. `0xfffffffd80000000` is NetBSD/alpha's page-table entry for `ALPHA_K1SEG_BASE`** (Opus's arithmetic, from a VPT
base of `0xfffffffc00000000`).  It is the one page this arm already remaps (`0xfffffe0000000000 -> 0x7efa000`), so the
trap is a deliberate "kernel VM wanted" tripwire.  **NOTED.**  It argues the announcement is true and worth keeping
(latched), which both 3 and 4 do.

**H3. `memory_alpha.c:194-196` says a failed walk returns 0 "so the caller raises the fault".  No Alpha caller does.**
Loads and stores abandon (#215) and fetches exit (:729-733).  **ACCEPT, as an L4 corrected in place in this round,
since the round touches the file.**

**H4. `:94`'s `fatal("AYONA3\n")` is its OWN row** (Opus, grok): a flood, on the walk path, unwitnessed.  **ACCEPT: FILE
LOW.**

**H5. The witness's DIED_ELSEWHERE path prints 0/0.**  The DETECTOR must use the three-way scorer (#540 F14), so that a
death under a mutant is a KILL.  **ACCEPT.**

**H6. codex_adv: "every I-fetch failure" is too strong.**  The single-step trace read handles its own failure by logging
(`cpu_dyntrans.c:287`, `:325`).  The COLD generic fetch is the path that dies.  **ACCEPT, as wording** in
`alphaifetchkill`.

**H7. The detector for 4 + latch** (Opus's list): LOAD dest == 0 + continued; STORE continued, then a load reads 0 (no
invented storage); FETCH -> PAL 0 halt, alive, NO kill text and NO `could not find physical`; LATCH exactly once across
two or more accesses; ANCHOR -- VMKILL+8 behaves like VMKILL.  **The mutants:** (b) re-add `exit(1)`; the latch never
set; the exit re-added under FLAG_INSTR only, writes only, or at VMKILL+8; and `return 0` in place of identity, which
the LOAD row's dest value catches.  **ACCEPT as the detector plan, if 4 is ruled.**  If 3 is ruled, the rows change:
dest == SENT, the FETCH cell DISCLOSED against `alphaifetchkill`, and no FETCH row.

**H8. alphaifetchkill's fix is NOT a one-liner (codex research job A).**  Replacing `exit(1)` with
`cpu->running = 0` falls through to `physaddr = paddr` with no paddr (`cpu_dyntrans.c:736`), and a bare `return`
leaves `next_ic` unset for the dispatch loop, which never checks `running`.  **NOTED for that row.**  Under member 4
this round does not depend on it.

**H9. The kimi CLI's case against 4, in its own words:** *"ACCEPT is a wrong translation that silently succeeds AND
floods warnings -- strictly worse than an honest decline on both axes ... the failure stays on the return-value
contract, which is exactly where a future member-5 fault delivery would hook."*  Three points need checking:
- the per-access `non-existant` WARNING (`core/memory.c:598-655`).  Opus says `-q` silences it; kimi calls it an
  unlatched flood.  My measurement counted 4 under `-V`.
- kimi reads `memory_alpha.c:194-196` (#194) as TRUTHFUL, against Opus's WRONG RECORD (H3).
- kimi calls VMKILL's VPT slot non-canonical; Opus sign-extends it to `ALPHA_K1SEG_BASE` (H2).  kimi found the guest
  header this rests on: `_guest-src-openbsd22/sys/arch/alpha/include/vmparam.h:154`, `VPTBASE 0xfffffffc00000000`.

**Settle these three by reading, not by vote.**

## QUESTIONS

**Q1 -- WHICH MEMBER?**  3 (the majority) or 4 + latch (Opus, and my leaning), given the measurement.  State the
discriminator, so the next "tripwire in an identity window" can reuse it.

**Q2 -- IF 3:** does `alphaifetchkill` (HIGH, now witnessed) go FIRST, or does this round ship with its fetch cell
disclosed?

**Q3 -- WHICH OF MY DISPOSITIONS IS WRONG?**  There are nine.  Be hardest on H1, where I lean against seven seats, and on H3 against H9.

**IDENTITY -- the first three lines of your answer:**

    FABLE_SEAT_ALIVE_20260918_541P1
    <your exact model id> | <the first line of C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md, verbatim>
    VERDICT: <member> -- <one line>

**READ-ONLY.**  Run no builds, no emulator and no panel scripts.  Write only `fable5_p1.md` in the panel directory
above.
