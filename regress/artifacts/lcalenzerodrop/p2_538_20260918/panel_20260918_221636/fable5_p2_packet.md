# `#538` PASS 2 -- CONSOLIDATED FINDINGS for the fable5 seat (LAST; every other seat has answered)

**Tree:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` at HEAD `cdbe7d7`, plus the working-tree diff to
`regress/lca_widewrite_probe.py` and `regress/lca_isalane_probe.py`.  The working-tree `dev_lca.c` ALSO carries the
unrelated, uncommitted #540 `| PHYSICAL` edit.  The #538 table ran on 8bd97e4's dev_lca.c (`logs/INSTRUMENT.md5`).
**Use absolute paths.**  `C:\DocumentNoSnc\CC\GXEMUL\src\` is pristine 2021 upstream.

**The brief:** `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\panel_20260918_221636\brief_sent.md`.
**Every answer is in that directory:**
- `codex.txt` -- the last `VERDICT:` block.
- `codex_adv538p2.txt` -- the dedicated job.  Its brief: `_scratchpad/cx538p2_adv_brief.md`.
- `kimi.txt` -- the CLI; the last `VERDICT:` block.
- `grok.txt`, `agy.txt`.
- `ollama_{glm,deepseek,minimax,kimi}.txt`.
- `opus5_p2.md`.  If it is not there, the Opus answer is quoted in F4-F9 below.

**The rule this pass is judged by** (your own #530 §F2 ruling, R6): the chain closes on the first VALID pass on
THIS diff that verifies the enumeration -- diff delivered, roster complete, zero WITH its denominator -- and
specifically kills the lane-1 escape with no lane cell open.

## VERDICTS

    CLOSES           agy, glm, deepseek, minimax, kimi-k3 (sub), kimi CLI, grok, codex (panel), opus5 -- each 0/4 open
    DOES NOT CLOSE   codex_adv538p2 -- ON EVIDENCE LIMITS ONLY (the file list I gave it); it proposed no surviving floor mutant

The roster is complete: eight scriptable seats, the dedicated job and Opus.  The diff was delivered: Opus md5-matched
the brief's fenced block against `git diff`, and it has 6 hunks.

## FINDINGS AND MY DISPOSITIONS

**F1. The closure itself.**  Nine seats found 0/4 open.  vc_ne0..3 each red exactly their own lane's row, and the lane-1
escape (vc_ne1) is 12/13, red at `low16`.
- codex_adv's unsettled premises are settled by evidence outside its permitted files:
  - **P1, whole-chunk delivery**: KILLLEN8's `transcript_KILLLEN8.wide:98` reads
    `[ writing to device 'lca_isa' addr 00005fe0 failed ]`, so the handler's `len > 8` refusal fired on the real
    binary (Opus found this).  M2_len8 and KILLLEN8 red at all four cells.
  - **P4, presets kept**: the per-leg `probe_*.raw` logs record 0x3, 0xff, 0xb0 and 0x5a under vc and M2_len8.
  - **P3**: #530 pass 2's measured legs.
- **DISPOSITION: CLOSES.**

**F2. THE HARNESS, and it is a genuine disagreement.**
- **codex (panel)** built an in-memory mock of the real `session()`.  It shows that a host death AFTER the final
  observation passes, and that a dead attempt with its last print missing qualifies for the retry, because
  `os.waitpid`'s status is DISCARDED.
- **grok**: "no path I can see ... the `quit` path swallows errors ... that is after the observations."
- **Opus**: "no path in these cells", but lists "record the waitpid status" as hardening (a) and names the residual:
  *"an intermittent death that went undetected and then passed on retry."*
- **MY DISPOSITION: FIX IN-ROUND (L1; the detector is unshipped).**  Patch (`_scratchpad/w538/waitstatus_patch.py`):
  after `quit`, DRAIN THE PTY TO EOF (bounded at 10 s), then close, reap, and require WIFEXITED with status 0.
  - Draining first matters: closing the master first sends the child SIGHUP, which would score as a death.
  - **Measured live, both directions:**
    - the #540 probe on the fixed build: 22/22, wait status 0, clean;
    - the alphavmkill witness on HEAD: died, wait status 256 (its `exit(1)`), not clean.
  - The same `session()` is copied into the unshipped #540 and alphavmkill probes; they get the same patch.
  - The committed parent (`lca_isalane_probe.py`) has it too.  **I would FILE that one** rather than widen this round.

**F3. RE-MEASUREMENT.**  F2, F4 and F5 change the instrument's code.  **MY DISPOSITION: re-run the FULL 17-leg
table with the final instrument**, so that the shipped probe IS the measured one (~26 min).  I am not arguing that a
stricter liveness check can only add kills: F4 changes a preset, and a comparison run owes one instrument.

**F4. `l2w16 live` is not a round-trip control (Opus).**  The MSR resets to 0 and ORs 0xb0 on every access, so preset
0x00 reads 0xb0 whether or not the write landed.  **ACCEPT: preset 0x01** (reads 0xb1, still != want 0xf3).  PRETABLE's
CHANNEL line and the row note are corrected in place.

**F5. The probe never creates `alpha_dummy.bin` (Opus).**  On a fresh clone that gives a phantom all-red.  **ACCEPT:**
copy the parent's three lines.

**F6. Contract wording, all ACCEPTED as comment-only L4s.**  None of them moves a cell into or out of the floor.
- **(ii)**: say port bits ABOVE the lane.  `P & 1` and `P & 3` are lane bits, inside the floor and caught.
- **(iv)**: disclose ANY stateful decline, not only chunk position.
- **(vii)**: equivalent/unreachable.  grok adds that a3=16 against a 16-byte string transfers no NUL at all, so "the
  terminator is at >= 15" is the wrong picture.
- **(viii)**: an added forward to the same port AFTER the lane byte IS visible.
- **Add (ix)**: lane 2 (the MSR) sees bits 0-3 and 6 only; a value edit confined to 0xb0 is invisible.
- **Add (x)**: the inner forward's WIDTH (codex_adv's (h)); widening the constant 1 is invisible where the register
  keeps the low byte, and it reads past `byte`.
- **Qualify "any variant"** to the body's inputs.
- **Label as derived, not measured**: `== L` for L != 3, and address misroutes.
- The PRETABLE's "first statement" for vg/vt1 means BEFORE `relative_addr >>= 5`, which `logs/vg.diff` confirms.

**F7. The parent header's `:164-169` and `:179` are stale present tense (Opus).**  **ACCEPT**, comment-only, as part of
the parent L4 edit.

**F8. The width pin replays the probe's OWN store_buf model (Opus).**  If `memory.c`'s ladder changed, the detector
would silently stop testing len > 8.  Opus proposes a source presence pin on `psize = 1024` / `psize >>= 2`.
**MY DISPOSITION: DISCLOSE it in the contract, as (xi), and FILE the presence pin as LOW hardening.**  A pin that reads
source is a rung-1 self-check, and making it a scored row raises a frozen-copy path question the round need not open.
**This is the one I am least sure of.**

**F9. Durable receipts (Opus).**  `logs/bins.md5` is now written: 18 hashes, and only `w_base` == `w_restored`
(== build/gxemul at HEAD).  `logs/BUILD_PHASE.out` carries ORDER_OK, BASELINE_CMP CLEAN, CLONE RESTORED cmp=clean and
restored == base.  **ACCEPT, DONE.**

**F10. Opus: #540 cannot move these 17 scores.**  Every session runs at ptbr == 0 in kernel mode, where identity equals
PHYSICAL.  **NOTED.**

## QUESTIONS

**Q1 -- CLOSES?**  By R6, with the denominator.

**Q2 -- THE HARNESS DISAGREEMENT (F2).**  Is a death after the final observation a real hole in a detector whose
purpose includes `alive`?  Is my fix right?  Is filing the committed parent's copy the right scope?

**Q3 -- F3 and F8.**  Is the full 17-leg re-run owed, or only the legs the edits could move?  Is the presence pin
owed, disclosed, or filed?

**Q4 -- WHICH OF MY DISPOSITIONS IS WRONG?**  There are ten.  Be hardest on F2 (I sided with one seat against two) and
F8 (I declined a seat's proposed guard).

**IDENTITY -- the first three lines of your answer:**

    FABLE_SEAT_ALIVE_20260918_538P2
    <your exact model id> | <the first line of C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md, verbatim>
    VERDICT: CLOSES | DOES NOT CLOSE -- <one line>

**READ-ONLY.**  A kill table is running on this machine.  Run no builds, no emulator and no panel scripts.  Write only
`fable5_p2.md` in the panel directory above.
