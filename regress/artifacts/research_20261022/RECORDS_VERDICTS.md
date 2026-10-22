# External-fixes research, 2026-10-22 -- the coordinator's measured verdicts on TRIAGE.md's records section

TRIAGE.md section (c) records two disputes between the consolidation agent and the coordinator's first verdicts. Both
were settled by RE-MEASUREMENT on 2026-10-22, and **the agent was right on both.** The coordinator's first verdicts were
phantom absences from broken apparatus (the carrier's "a pattern that matched nothing reports zero for everything"
class): a `git diff --no-index` against a path that does not exist, with stderr suppressed, printed "0 files differ";
a grep for a CPU-control-register spelling (`M88K_CR_PFAR`) found nothing because the register is a CMMU register
spelled `CMMU_PFAR`.

## R1 -- the "unmodified upstream baseline" commit `39748e3c` is NOT pristine: CONFIRMED

Measured against the owner-archived pristine upstream `src` (`C:\DocumentNoSnc\CC\GXEMUL_upstream_2021\root_src`, the
April-2021 checkout per its README; 447 files) with `git -c core.safecrlf=false diff --no-index`:

* **1 file MODIFIED:** `src/cpus/generate_arm_r.c` -- `(int)(1 << (c-1))` -> `(int)(1U << (c-1))`. *This first said
  "at two sites"; the adjudication's frozen comparison (ADJ_RULINGS.md E) and the drafter's `R1_tree_diff_20261022.txt`
  both count THREE sites, lines 139, 200 and 279 -- the fork's `#13`.* A real edit (an undefined-signed-shift fix) in a
  commit whose message says "unmodified".
* **59 files only in the baseline:** *this first said "every one a generated `tmp_*.c`"; the same two comparisons
  correct it to* 50 `tmp_*.c` CPU-generator products plus 9 other generated files (`autodev.c`, `automachine.c`, six
  font files, `ppc_spr_strings.h`) -- none shipped by the tarball; versus the frozen upstream tarball the count is 61,
  the extra two being `grep.exe.stackdump` crash dumps (also present in `root_src`).
* `configure`: SETTLED by the drafter against the downloaded release tarball (`R1_tree_diff_20261022.txt`): the
  baseline carries the fork's `#9`, the GNU89-inline probe absent from upstream. *This first said "not settled
  locally" because the only local copy (the project-root `configure`, archived to
  `_archive/2026-10-22_root-cleanup/upstream-gxemul-0.7.0-dist/configure`) is dated 2026-06-28 and is not pristine.*

Consequence: `gate_ab` builds its "pristine" A tree from this commit, so that tree carries the `1U` edit and the
generated files. Behaviourally the `1U` change removes undefined behaviour and should be identical on this compiler, but
the RECORD (the commit message, and every A/B claim that calls the tree "pristine") is a wrong record -- L4, correct in
place; and the provenance note belongs in `gate_ab.sh`'s header.

## R2 -- the m88k PFAR note at `OUTSTANDING_BUGS.md:1896-1898`: FALSE in both reason and conclusion

The note says the defect is "REFUTED ... the register is not modelled at all. `PFAR` appears nowhere in `src/`."
Measured: `CMMU_PFAR` (`src/include/thirdparty/m8820x.h:66`, the CMMU P-bus fault address register) is WRITTEN at
`src/cpus/memory_m88k.c:399` (`= 0`) and `:405` (`= pfar`), and is guest-READABLE through `src/devices/dev_m8820x.c:438`.
The fork's own `vmedefaultkill` records read it. So the register IS modelled, and upstream's PFAR fix (TRIAGE.md R2)
targets a LIVE defect. Disposition: reopen the refuted item as a queue row; correct the note in place quoting what it
refutes.

## VR41xx 1 KB-page TLB write: CONFIRMED host exit, UNFILED

`src/cpus/cpu_mips_coproc.c:2040-2041`: `fatal("1KB pages don't work with dyntrans.\n"); exit(1);` on a guest TLB write.
HOST-STOP, guest-kernel-reachable on hpcmips. 0 matches in `OUTSTANDING_BUGS.md`. TRIAGE.md T11.

## Also verified by the coordinator against HEAD `de8c7547` (all unfiled, all in TRIAGE.md's first batch)

* **T1** `generate_m88k_loadstore.c:104-105` returns early for a scaled byte `xmem`, so its table slot is NULL and
  `cpu_m88k_instr.c:2377` consumes it unguarded -- a host crash from one user-mode instruction.
* **T4** `dev_wdc.c:470-476` and `:562-568` compile out the LBA offset (`#if 0`), and `:2015` reads the LBA flag from bit 5
  (ATA: bit 6). FreeBSD's patch alone would misroute NetBSD, whose CHS requests set bit 5 (`0xa0`).
* **88K bus-error registers** `memory_rw.c:614-623`: a refused device access raises the data-access exception with no
  fault status or address (upstream's own TODO stands); upstream fixed it in r6542/r6547.

## Cautions carried from the reports

* Do NOT copy trunk's removals of CPU stops as crash fixes: trunk now stops on every error-level message by default,
  the design this fork rejected in `#261`.
* Do NOT take T2 SDE's Linux tap patch (unbounded `strcpy` into a 16-byte field); the fork's `#253` is safer.
