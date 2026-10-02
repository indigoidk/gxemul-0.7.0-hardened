THE ID-LESS TABLE -- three dispositions that name more than one outcome, and seven closing sentences to write out

FIRST line of your answer: `VERDICT: <a> of 3 compound dispositions settled, <b> of 7 sentences written, <d> amendments disputed`.
SECOND line: the token `GROK_ICOMPOUND_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  You ruled the id-less entries of this project's bug queue and GPT-6 Astra confirmed or amended each
ruling (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idless_20261002\IDLESS_DISPOSITIONS.md`).  A table of what the queue is owed was derived mechanically from those
lines.  The derivation reads ONE outcome per disposition, and it cannot turn an instruction into a sentence.  The ten
items below are where that fails.  The main loop must not settle them from a paraphrase; you ruled these entries, so
you write the result, and Astra checks it afterwards.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`; the queue line numbers are commit `db8b1a33`'s
(`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:OUTSTANDING_BUGS.md`; if `git show` is refused to you, say so and read
the file on disk by its text).  Never read any other `src/` under the project root; never `git status` or `git diff`.
Write nothing.

**Part A -- three compound dispositions.**  Astra's amendment splits each entry into a part that is ALREADY FILED
under an id and a part that needs a NEW row.  A filing unit prepared today (`#554`) adds rows of its own; they are
listed with their titles in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\draft\section554.draft.md`.
For each, ONE line per resulting row:
`<queue lines> | FILED <id> -- <where that row is: the queue line, or #554's draft> | covers: <which part of the entry>`
`<queue lines> | NEW <HIGH/MED/LOW> <id> | TITLE: <one sentence, at most 200 characters, no line numbers> | <the lines you read, path:line>`
* Read the source: a NEW row's title must be true at `7440e129` and must cover exactly the part the filed row does not.
* If the "NEW" part is in fact one of `#554`'s rows under another id, say `FILED <that id>` and give the line of the
  draft.  I believe -- check it -- that the third entry's `armcoprocstop` is `#554`'s `armcp15cp14exits`.
* If you dispute the split itself, say `DISPUTE: <what the amendment gets wrong, with path:line>`.

A1. queue lines 1705-1716 (slice 01)
   Astra's amendment: 1705–1716 | grok said NEW HIGH `qhppcdecode` covering ten pending encodings | should be FILED HIGH `ppcfmasingle` for `fmadds`/`fmsubs`, plus NEW HIGH `qhppcdecode` for the other eight; describe the failure as stopping emulation | `FILING.tsv:3` consolidates the single fused family; `DISPOSITIONS.md:24–27` explicitly forbids double filing. `regress/ppc_halt_probe.py:257–279` supplies the population; `src/cpus/cpu_dyntrans.c:2014` clears `cpu->running`. | confidence HIGH
   your ruling: 1705–1716 | ID-LESS: yes | OPEN: YES: regress/ppc_halt_probe.py:257–279 still marks `fctid`, `fctidz`, `fcfid`, `fcmpo`, `fmadds`, `fmsubs`, `fsqrt`, `fsqrts`, `fres`, and `frsqrte` PEND and :297 expects those rows to halt; src/cpus/cpu_ppc_instr.c:5218 and :5410 are `default: goto bad`, and src/cpus/cpu_dyntrans.c:2006–2014 prints UNIMPLEMENTED and sets `cpu->running = 0`. The word "twelve" is stale: `fnmadd` is FIXED at regress/ppc_halt_probe.py:273 | DISPOSITION: NEW HIGH qhppcdecode "ten PPC FP encodings still abort the emulator" | OUTSTANDING_BUGS.md:1705, regress/ppc_halt_probe.py:257–279, src/cpus/cpu_ppc_instr.c:5218, src/cpus/cpu_ppc_instr.c:5410, src/cpus/cpu_dyntrans.c:2006–2014
A2. queue lines 2616 (slice 02a)
   Astra's amendment: 2616 (CMMU/MB89352) | grok said NEW HIGH qhm88kstops for both | should be FILED m88kexit for CMMU; retain NEW HIGH qhm88kstops restricted to MB89352’s no-transfer DREG stop | `OUTSTANDING_BUGS.md:6868–6869` already owns the CMMU branch. Its exception predecessors assign non-SUCCESS statuses (`src/cpus/memory_m88k.c:172–341`), so the SUCCESS exit at `:394` is latent. The separate MB89352 stop remains at `src/devices/dev_mb89352.c:143–147`; `mb89352halt` concerns a different missing-status-buffer case. | confidence high
   your ruling: 2616 | ID-LESS: yes "" | OPEN: YES: MSR.IP takes the "Reboot hack for NetBSD/prep" path and sets cpu->running = 0 | DISPOSITION: NEW HIGH qhppciphack "MSR.IP stops the CPU instead of selecting the exception vector base" | src/cpus/cpu_ppc.c:288-291 at db8b1a33
A3. queue lines 16997-17000 (slice 07)
   Astra's amendment: 16997-17000 | grok said FILED `xscaleinten` HIGH | should be FILED `xscalecp6exits` HIGH for CP6, FILED `armendianexit` HIGH for endian switching, and NEW `armcoprocstop` HIGH for the remaining CP15/CP14 exits | The three named functions retain seven exits at `src/cpus/cpu_arm_coproc.c:62,177,264,322,331,417,528`. [DISPOSITIONS.md](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/astraretro_20260926/DISPOSITIONS.md:335):335-336 and `FILING.tsv:50` assign CP6’s three sites while expressly leaving `:62/:264/:528` owing an ID; `FILING.tsv:15` names the endian defect. Coalesce that unnamed remainder with `OUTSTANDING_BUGS.md:18721-18722`. `xscaleinten` shipped at `OUTSTANDING_BUGS.md:19488-19493`, and its repaired load at `src/cpus/cpu_arm_coproc.c:310-314` has no exit. Grok’s wholly-FILED disposition wrongly loses the remaining filing obligation. | HIGH confidence
   your ruling: 16997-17000 | ID-LESS: no "armbfxwidth32" | OPEN: YES: `exit(1)` is live at src/cpus/cpu_arm_coproc.c:62 (`arm_coproc_15`, `rd == ARM_PC`), :417 (`arm_coproc_i80321_6` unknown) and :528 (`arm_coproc_xscale_14` unknown). `X(mcr_mrc)` at src/cpus/cpu_arm_instr.c:948-953 passes the guest instruction word to `arm_mcr_mrc` (src/cpus/cpu_arm.c:2643-2655), which calls the installed handler. CP15 is installed at src/cpus/cpu_arm.c:175, CP14 at :179, CP6 at src/machines/machine_iq80321.c:57 and src/machines/machine_iyonix.c:64. A guest MCR/MRC on those paths ends the host process, which is HIGH. The same three kills are the CP15 `rd == ARM_PC`, CP6 `unknown` and CP14 `unknown` members of the sibling 

**Part B -- seven closing sentences.**  These entries are ruled CLOSE-RECORD: the queue's prose says something is
open, the source shows it is not, and ONE sentence will be added at the passage saying so.  For these seven the
governing line is Astra's amendment, and it gives a fragment, a correction to your sentence, or an instruction.  Write
the sentence that should stand, AS AMENDED.  ONE line each:
`<queue lines> | SENTENCE: <one or two sentences, true at 7440e129, naming the file and function or the round that settled it; no "as amended", no reference to this review> | AS AMENDED / DISPUTE: <why, with path:line> | <the lines you read>`

B1. queue lines 821-828 (slice 01)
   Astra's amendment: 821–828 | grok said CLOSE-RECORD, “five harness reds … were re-pinned” | should be CLOSE-RECORD with “resolved through corrected census scoping, guard checks and the specified re-pins” | `CHANGELOG.md:13385` says the whole-buffer pin never moved; `:13387` replaces WDC equality with three checks. The closure stands, but its replacement sentence is false. | confidence HIGH
   your ruling: 821–828 | ID-LESS: yes | OPEN: NO: CHANGELOG.md:13384–13388 records the shipped re-pins (promptless probes, whole-buffer full-prompt, class ratchet, wdcflood guards, asic_badaddr rows); regress/gate_hygiene.sh:712–722 is the whole-buffer allowlist | DISPOSITION: CLOSE-RECORD "The five harness reds named here were re-pinned in CHANGELOG.md:13384–13388 and do not go to another round." | OUTSTANDING_BUGS.md:821, CHANGELOG.md:13384–13388, regress/gate_hygiene.sh:712–722
B2. queue lines 1875-1885 (slice 01)
   Astra's amendment: 1875–1885 | grok said UNSETTLED | should be CLOSE-RECORD narrowly stating that default PROM bytes receive backing storage before machine setup and survive `baremips` setup; this establishes byte survival, not endian-correct reboot behavior | `src/core/emul.c:484,502,535` establishes creation order; `src/cpus/memory_rw.c:663–667,728–729` and `src/core/memory.c:554–579` back the write; `src/machines/machine_test.c:299–303` does not overwrite it. | confidence HIGH
   your ruling: 1875–1885 | ID-LESS: yes | UNSETTLED: src/cpus/cpu_mips.c:303 still stores `0x00c0de0d` at `0xffffffff9fc00000`; a pass over machine setup showing whether any machine leaves that word would settle the residual | DISPOSITION: UNSETTLED | OUTSTANDING_BUGS.md:1883, src/cpus/cpu_mips.c:303
B3. queue lines 4204-4225 (slice 02b)
   Astra's amendment: 4204–4225 | grok said CLOSE-RECORD, “the U=0 ignore-low-two-bits behaviour” | should remain **CLOSE-RECORD**, saying “U=0 with alignment checking disabled, A=0; alignment-fault enforcement remains armalignexc” | Access masking exists at `src/cpus/cpu_arm_instr.c:1716,1910`, with unmasked writeback at `:1777–1778,1925–1926`. The comment at `:1656–1666` explicitly requires the missing qualification. | HIGH; wording amendment
   your ruling: 4204–4225 | ID-LESS: yes | OPEN: NO: slow LDM and STM pass addr masked with 0xfffffffc, and the writeback stays unmasked | DISPOSITION: CLOSE-RECORD "The slow LDM and STM paths now pass addr & 0xfffffffc to memory_rw (cpu_arm_instr.c:1716 and :1910, #524) and keep the base writeback unmasked, which is the U=0 ignore-low-two-bits behaviour." | src/cpus/cpu_arm_instr.c:1716, :1910
B4. queue lines 4352-4354 (slice 02b)
   Astra's amendment: 4352–4354 | grok said NEW LOW qharmpromptnote | should be **CLOSE-RECORD**, stating that the probe comment documents full-prompt sufficiency and misleading earlier `>` sources | `regress/arm_idle_probe.py:156–185`, especially `:177–185`, explains that the true prompt follows the complete dump and identifies disassembly and dump-ASCII false sources. Grok’s literal phrase search missed the substantive explanation. Do not claim that a literal global enumeration was added. | MEDIUM-HIGH
   your ruling: 4352–4354 | ID-LESS: yes | OPEN: YES: the non-prompt-`>` sentence appears in the queue and in no probe comment | DISPOSITION: NEW LOW qharmpromptnote "the non-prompt greater-than safety argument lives only in the queue" | OUTSTANDING_BUGS.md:4352–4354
B5. queue lines 4741-4742 (slice 02b)
   Astra's amendment: 4741–4742 | grok said NEW LOW qhtstcarry, citing the immediate-S TODO | should be **CLOSE-RECORD**: “The combined TST/TEQ carry omission was measured and repaired by #340; the immediate-magnitude approximation is separate” | The referent is `OUTSTANDING_BUGS.md:1814–1842`. `src/cpus/cpu_arm_instr.c:3353–3360` implements carry propagation, called by all four handlers at `:3369,3391,3410,3434`. `CHANGELOG.md:32472–32475` distinguishes the repair from the unrelated approximation grok cited. | HIGH
   your ruling: 4741–4742 | ID-LESS: yes | OPEN: YES: the immediate S-bit carry TODO still covers TST and TEQ, and the entry says the defect is unmeasured | DISPOSITION: NEW LOW qhtstcarry "TST/TEQ immediate-S carry is still marked not exact and is unmeasured" | src/cpus/cpu_arm_instr_dpi.c:121–138; OUTSTANDING_BUGS.md:4741–4742
B6. queue lines 5383-5385 (slice 03)
   Astra's amendment: 5383–5385 | grok said UNSETTLED | should be CLOSE-RECORD: “The endpoints describe six observed idle boots, not population bounds; retain the subsequent lower sample as history” | `regress/drive_guest.py:130–135` and `CHANGELOG.md:26710–26713` explicitly identify the sampled population and reject deriving a ceiling from it. | confidence high
   your ruling: 5383–5385 | ID-LESS: yes | OPEN: UNSETTLED: whether sampled extremes are still printed as limits was not audited past this sentence | DISPOSITION: UNSETTLED | `OUTSTANDING_BUGS.md:5383-5385`
B7. queue lines 12520-12524 (slice 05)
   Astra's amendment: 12520–12524 | grok said CLOSE-RECORD “…live rows require… the guest’s own sector on disk…” | should be CLOSE-RECORD “row_residue_recovery was re-cut before shipping: its assertions require an empty ring after WDCC_WRITE and one recorded 512-byte write whose first byte is 0x55; the oracle-correction label was withdrawn because the original pin never shipped.” | `regress/diff_wdc_identify.c:3183,3204–3205` checks occupancy, write count, byte count and **only the first byte**. The stub at `:376–392` records these observations without writing a disk. `CHANGELOG.md:15394–15397` confirms the classification correction. Grok agrees with Astra’s scan here, but both overstate what the assertion verifies; the closure itself stands. | HIGH confidence
   your ruling: 12520–12524 | ID-LESS: yes | OPEN: NO: `row_residue_recovery` was re-cut. `regress/diff_wdc_identify.c:3140-3153` says the defect-shape pin never shipped and is replaced alongside nothing; the live checks fail when `occ != 0` (`:3183`) and when the sector is other than the guest's (`:3204-3205`). `CHANGELOG.md:15394-15397` withdraws the oracle-correction label: the old pin had never shipped, so the work was L1 pre-ship construction. | DISPOSITION: CLOSE-RECORD "`row_residue_recovery` was re-cut before it shipped: the live rows require an empty ring after the new command and the guest's own sec

End with `DENOMINATOR: <s> of 10 items read in the source`.
