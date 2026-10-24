## 5. QUESTIONS -- VERDICT LINE FIRST (format in section 0)

**Q1 THE REPAIR DIFF (section 2) -- is it exactly what the ruling commanded, and nothing else?**  (a) R1: the block now sits
between the gate's `CC=$(command -v cc || command -v gcc)` and its first `need_file`, invoked `GEN= TABLE= CC="$CC" ...`; HEAD ->
staged is ONE hunk (+48); the block's own comment gained only the placement sentence; its consumer sentence is unchanged
(the ruling: it does not over-state).  (b) R2: the driver's `CC` default is cc if present, else gcc, and the header note.
(c) R3: the generator comment's new sentence -- "the register-form ld/st decoder installs twelve of the slots as ic->f and
xmem_slow() calls four; the other eight have no caller today and are repaired with them" -- TRUE against the consumers
(`cpu_m88k_instr.c:2377`, `:2411`, `:3087`, `:3622`; the register-form decoder adds SCALEDNESS/USR, never NO_PC_SYNC;
`xmem_slow` adds NO_PC_SYNC, never SIGNEDNESS; bit 0x80 rejected as .wt at `:3606-3614`), with 12 + 4 + 8 = 24?  (d) R4: the
sum form of the index, consistent with the 54 hard-coded indices?  (e) F25: the NOT-OBSERVED line as measured in `F25.out`
(0/123 red when both artifacts swap; 1/123 when one does)?  (f) Anything in the diff beyond R1-R5 + F25?

**Q2 THE FLOOR QUESTION ON THE COMPOSITE** (the shipped generator + regenerated table + 123-row driver + the gate block as
it will be committed): name any edit INSIDE the detector's contract (the 24 repaired cells, the 9 accept cells, the 24
counterparts, the structural/status rows, the fresh-vs-committed equality, in either artifact) that keeps all 123 rows green
-- or state the cells/shapes you inspected and that none exists.  Does moving the block change any of the 123 identities or
the 126 gate checks?  Is the placement's trade-off right: a compiler-less host SKIPs gate 2 at its own `gate_skip` (as before
this round), a host WITH a compiler reds on a missing/non-compiling/non-running generator (B5)?

**Q3 THE MEASUREMENTS (section 3)** -- is each receipt what the report says: the committed-form GATE 2 run `PASS (485 checks)`
= the 2026-10-04 battery's 359 at `1329d894` + this block's 126 (the derived number OBSERVED; the run's tree described
honestly -- 21 of 702 tracked files differed from HEAD, the foreign `diff_wdc_identify.c` and the peer's five `src/` files
among them); the working-tree run 502 (= 485 + the foreign hunks' 17); the five compiler cases (three green with identical
output, two red at `gen_compiles`); the table unchanged; the clearance clean on all four trees with the binaries newer than
both sources; the driver output byte-identical to pass 2's `fixed.out`?  Is anything claimed that a receipt does not show?

**Q4 THE LANDING** -- the builder's D-5: `.gitignore:33` (`regress/diff_*`) IGNORES the new driver, so it must be added with
`git add -f` and mode 100755 (verified by `git ls-files -s` after the commit; the precedent `diff_autodev_gen.sh` is tracked
100755 under the same ignore rule).  D-6: `repair1_20261023/wt_gate_offline.sh.bak` holds ANOTHER SESSION's uncommitted gate
hunks -- the main loop will move it OUT of the artifacts dir before the commit (its md5 stays in the report) so no foreign
in-flight work lands under `#569`.  Right?  What else must the landing record for this repair (the CHANGELOG `#569` block
already names the move, the committed-form 485 and the working-tree 502 with their trees, `(c): measured at ...`, the four
filed rows)?

**Q5 ANYTHING ELSE**, with the file:line that settles it.  Roster for this pass: GLM 5.3, DeepSeek, Grok 4.7 (file-reading, the
same packet); GPT-6 Astra adjudicates; Fable 5.1 HELD by the owner; Gemini 4 Argon NOT FIRED (its transport failed four
controls today -- recorded as a seat failure, not agreement); agy/kimi/minimax/Opus-seat not on the owner's roster.
