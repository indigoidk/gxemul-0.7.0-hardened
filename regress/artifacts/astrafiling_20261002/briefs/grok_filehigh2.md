SEVEN MORE HIGH ROWS -- the same first-hand re-read, for the rows added after your first pass

FIRST line of your answer: `VERDICT: <t> of 7 HIGH rows true as titled, <c> true only under a condition the title omits, <f> not HIGH or not true`.
SECOND line: the token `GROK_FILEHIGH2_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  You re-read the 57 HIGH rows of the Astra review campaign's filing table against the committed source
(`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\grok\grok_filehigh.txt`).  The check of
that table then found rows the derivation had MISSED, and seven of the rows it added are graded HIGH.  They were never
in your population, so they have had no independent first-hand reading.  A row graded HIGH gets a correction round; a
HIGH that is false, or true only under a condition its title does not state, misdirects real work.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`.  Read committed files
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`); if that command is refused to you, read the file
from disk and SAY SO for each file -- the working tree carries uncommitted edits to `src/devices/dev_lca.c`,
`dev_pcc2.c`, `dev_sh4.c` and `src/cpus/cpu_alpha_palcode.c`, none of them a file these rows name.  Never read any other
`src/` under the project root; never `git status` or `git diff`.  Write nothing.

**Severity, as the campaign applied it:** HIGH -- guest-controlled input ends the emulator process, makes one of its
memory accesses leave a buffer's bounds, or stops it making progress.

**The seven rows** (each row's title and governing text are in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\FILING_OVERLAY.tsv`, the `ADD` lines; the
rulings they come from are in `...\regress\artifacts\astraretro_20260926\DISPOSITIONS.md`):
1. `armcp15cp14exits` -- three sibling exits of `src/cpus/cpu_arm_coproc.c`: `:62` CP15 with Rd == PC, `:264` CP15 PID,
   `:528` CP14 unknown.
2. `m88kpsrbokill` -- m88k: a supervisor `stcr` or `rte` that writes PSR with the BO bit flipped against the machine's
   byte order stops the CPU (`src/cpus/cpu_m88k.c:522-532`; `src/cpus/cpu_m88k_instr.c:843-847`).
3. `osiopselectzero` -- a site of the existing class row `exitunowned76` in `src/devices/dev_osiop.c` (DISPOSITIONS.md
   line 681 names the finding, `devosiop:F1`).
4. `osiopregexit` -- another site of that class in `dev_osiop.c` (DISPOSITIONS.md line 683, `devosiop:F3`).
5. `osiopdnadexit` -- `dev_osiop.c:942`, `:946` whitelist OSIOP_DNAD (0x28) and OSIOP_ADDER (0x3c) for 32-bit width, the
   register switch has no case for either, and one aligned access reaches `exit(1)` at `:1152`.
6. `pvrrenderexit` -- `src/devices/dev_pvr.c`'s render and texture loops still call `exit(1)` (the queue's prose at
   `OUTSTANDING_BUGS.md:2721-2723` graded it "med DoS").
7. `ofpeerexit` -- OpenFirmware `peer()`: `src/promemul/of.c:394` calls `exit(1)` when the handle is not the root and
   the lookup misses.

**For each, one line:**
`<id> | TRUE / CONDITIONAL: <the condition> / NOT HIGH: <why> / NOT TRUE: <what the source shows> | <the lines you read, path:line>`
For each say also WHO reaches it: a guest instruction or device access on an in-tree machine (name one machine that
registers the device or runs that CPU), or only something the guest cannot do.
Then: **(a)** a row whose defect `OUTSTANDING_BUGS.md` already files under another id (name the id and line);
**(b)** `DENOMINATOR: <s> rows read in the source, <t> ruled from the table's text alone, of 7`.
