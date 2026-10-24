# Proposed in-round repairs for `#569` (NOT applied; for the F2 adjudication)

Origin: the pass-2 drafter's NOTES #2 and #3 (`pass2_20261023/drafter_NOTES.md`), BUILD_REPORT D-9.  Both are L1/L4
in the carrier's taxonomy (the deliverable still being built; a wrong record in product code).  Each repair diff gets
its own scoped pass per the repair-chain rule, closing on the first pass that finds zero breaches.

## R1 -- the GATE 2 block moves BELOW the compiler detection and receives the gate's `$CC` (drafter #2 / D-9)

Facts (HEAD `regress/gate_offline.sh`): `:183-184` `command -v cc ... || command -v gcc ... || gate_skip "no C
compiler on PATH"`; `:185` `CC=$(command -v cc || command -v gcc)`; the `#406` autodev block (the other generator
block) is at `:1886-1928`, and `# ---- #412: SCSI READ CAPACITY` begins at `:1929`.  The working tree's foreign hunks
sit at HEAD `:1738`, `:1832-1834` (+50) and `:2273`/`:2277` -- an insertion at `:1928/1929` is 94 lines clear of the
nearest one, so `git merge-file` carries it onto the working tree without conflict.

* Move the whole `# ---- #569:` block (staged `gate_offline.sh:74-118`, 45 lines) from after the `#375` reader to
  immediately BEFORE `# ---- #412: SCSI READ CAPACITY on a zero-block disk` (HEAD `:1929`), i.e. right after the
  `#406` block's closing `fi` and blank line.  Content unchanged except the invocation line, which becomes:

      GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1

  so the driver compiles with the compiler the gate detected (cc or gcc).  A host with no compiler then SKIPS GATE 2 at
  `:184` as before this round, the way every other differential in the gate does; a host WITH a compiler still gets a
  RED row (never a skip) for a missing generator/table, a failed compile, a failed run (B5 unchanged).
* The block's comment gains one sentence: "Placed after the gate's compiler detection so the driver gets `$CC`;
  standalone it falls back to cc, then gcc."

## R2 -- the driver's standalone `CC` default (drafter #2)

`regress/diff_m88k_loadstore_gen.sh:92`:

      CC=${CC:-cc}
  ->
      CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}

(the gate passes `CC` explicitly; this only matters when the driver is run by hand on a gcc-only host).  The driver's
header comment line about `CC=<compiler>` (`:82`) is extended with "(default cc, else gcc)".

## R3 -- the `#569` comment in the generator says all 24 slots are consumed (drafter #3; L4)

`src/cpus/generate_m88k_loadstore.c:258-261` (working tree):

      They were NULL,
      and xmem_slow() calls them unguarded while the
      ld/st decoder installs them as ic->f (both in
      cpu_m88k_instr.c).  */
  ->
      They were NULL,
      and their consumers index the table unguarded --
      xmem_slow() calls the slot, the register-form
      ld/st decoder installs it as ic->f (both in
      cpu_m88k_instr.c) -- so none of the 24 may be
      NULL, whether or not an instruction reaches it
      today.  */

No row changes (the 24 pins already cover every slot); the regenerated table is unaffected (the comment is in the
generator source, not in its output).

## AMENDED after Grok's and DeepSeek's pass-2 answers (2026-10-23 ~11:30)
* **R1 placement:** Grok (`grok_t1p2.txt:79`) puts the block immediately AFTER the `CC=$(command -v cc || command -v gcc)`
  assignment (HEAD `gate_offline.sh:185`) and BEFORE the `need_file "$HERE/diff_ieee_store.c" ...` at `:186`.  That is
  better than "before `#412`": the driver needs a compiler but NOT a configured tree, and the `gate_skip "no configured
  tree"` at `:193` would otherwise skip it on a host that could run it.  HEAD `:185/:186` is 1,550 lines clear of the
  nearest foreign hunk.  ADOPTED.  Invocation: `GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1`.
* **R3 extends to the gate block's comment** (staged `gate_offline.sh:75-78`): DeepSeek (`ollama_deepseek_t1p2_A_Q12.txt:21`)
  and Grok (`:45`) both read "xmem_slow() calls the slot; the register-form ld/st decoder installs it as ic->f" as
  asserting a caller for every slot.  Reword to: "...which cpu_m88k_instr.c indexes with no NULL check: the register-form
  ld/st decoder installs twelve of the slots as ic->f and xmem_slow() calls four; the other eight have no caller today
  and are repaired with them."
* **R4 (Grok `:123`):** the driver's comment at `:119-120` ("256*no_pc_sync + ...", "the generator's loop variables")
  gains the clause "(the index is the SUM of the flag values the generator's loop variables already hold -- 256, 128,
  64, 32, 16, 8, 4 -- not a product with the 0/1 flags)".
* **R5 (Grok `:79`, `:87`; = F17):** after the move, GATE 2 is run ONCE with the STAGED (committed-form) gate in place
  of the working-tree file (swap in, run, swap back; both swaps recorded by md5), so the recorded check count is the
  committed file's (derived 485 = the 2026-10-04 battery's 359 at `1329d894` + this block's 126), and the CHANGELOG names
  both runs' trees.  GATE 11 is NOT re-run (the repair touches no product code); its earlier run is described as made on
  a `build/gxemul` rebuilt with the peer's uncommitted `cpu_alpha_palcode.c` present, and as not exercising the 24 slots.

## What the repairs do NOT change
The repair A1-A5, the table, the 123 rows, the legs' receipts.  After R1/R2 the committed driver's output is
byte-identical for the same inputs (only the compiler selection line changes), so `fixed.out` and the legs stand; R1
is re-measured by ONE GATE 2 run (the block's 126 checks green in the new position) and R3 by the gate's own
`#569`-comment-free rows (none observes the comment).
