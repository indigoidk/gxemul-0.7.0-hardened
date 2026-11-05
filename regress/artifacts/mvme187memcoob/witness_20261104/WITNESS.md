# mvme187memcoob -- the rung-3 witness, measured 2026-11-04 01:22 (before any edit)

No fix exists: the design ruling (the bound first, then the exits' disposition) is Fable's and is HELD (owner 2026-11-04 ~00:4x
"hold fable"; ~01:0x "keep going ... on the 5 oldest bugs").  Measured by the main loop (Opus 5.5).

**Instrument.**  `regress/mvme187_memc_probe.py`, run as the frozen copy `probe_frozen.py` (md5 69b4d98bfccb, equal to the source at
run time; `RUN.log` 01:22:32).  Machine: `-E mvme88k -e mvme187 -M 64`, UNMODIFIED in-tree; each access is one real m88k `ld.bu` or
`st.b` (r3 = 0xfff43000, MVME187_MEM_CTLR) placed with `put w` and stepped once.

| run | binary | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|---|
| `prefix_head.out` | the scratch clone /tmp/gx579 rebuilt with HEAD `ebe5af82`'s `dev_pcc2.c`, `mvme_pcctworeg.h` and `cpu_ppc_instr.c`; `dev_mvme187.c`, `machine_mvme88k.c`, `memory_rw.c` checked `== HEAD` (`RUN.log`) | 13/21 | OK | PRESENT | the eight witness rows |
| `prefix_build.out` | `build/gxemul` (its `dev_pcc2.c` and `mvme_pcctworeg.h` are the tree's UNCOMMITTED copies, not this round's; the memc files are HEAD's) | 13/21 | OK | PRESENT | the eight witness rows |
| `null.out` | `/bin/true` | 8/21 | FAIL | ABSENT | -- |
| `nobin.out` | a missing path | 0/21 | FAIL | ABSENT | -- |

Controls: `ld.bu` at +0x00 reads 0x80 (MEMC_CHIPID), +0x04 reads 0x1, +0x08 reads 0x3 (memconf for 64 MB), and the controller-1 alias
+0x100 reads 0x80 -- values only the device supplies (a read at 0xfff43000 with no device there would be zero-filled by memory_rw.c:700-702).  Witness: `ld.bu` at +0x0c, +0x7c and +0xff each end the
process with `[ mvme187_memc: unimplemented read from offset 0x.. ]`, and `st.b` to +0x08 with `mvme187_memc: Write to relative_addr 8
(controller 0) not yet implemented!` (exit status 1; `prefix_head_sessions/`).

**Measured facts the ruling should weigh:**

1. **The host out-of-bounds read is LATENT, not live.**  On the ASAN build (`build-asan/`, `-O3 -fsanitize=address,undefined`) the loads
   at +0x7c and +0xff produced NO AddressSanitizer report: the default arm's `exit(1)` came first, and (REASONED from the missing report, not observed) the compiled handler does not perform that read on the exiting path (BANKED 02:5x at `asan_head/` -- `ld_bu_7c.txt`, `ld_bu_ff.txt`, `RUN.txt`: exit status 1, zero
   AddressSanitizer reports, the handler's text present; this sentence first cited the 01:1x smoke runs, which were never preserved --
   a wrong record an Opus reading seat caught, corrected here).  So removing the exit
   without bounding the index would make it live -- the bound must land with or before any change to the exits, and the detector owes an
   ASAN leg on the fix.
2. **An apparatus fact, found by the first run (try1_negdefect/):** `-E nosuchmachine -e mvme187` CONSTRUCTS the mvme187 (exit status 0,
   chipid read back) -- the subtype name selects the machine -- so the negative control must not pass `-e`.  Fixed before this run.

**Owed when the design is ruled:** the value a declined read returns and whether a once-latched announce prints; widths other than a
byte; stores other than to memconf; controller 1 beyond chipid; the ASAN leg; the gate wiring and the kill table.
