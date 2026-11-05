# qhslowifetch repair pass 2 -- checks run by the main loop, 2026-11-05 02:0xZ

1. GLM item 3 (the gate runs the in-tree probe, the table ran probe56_frozen.py) -- regress/ppc_ifetch_probe.py (md5 0c2f8219d9b7) is NOT
   byte-identical to det_20261104/table2/probe56_frozen.py (0cae1c8e2884); they are AST-equal once the module docstring is removed (the
   clause (e) text regenerated from table 2 after it ran, apply_clause_e_tables2.py).  Gate 13 in situ ran the in-tree probe: RESULT
   56/56, RED=none (wiring_20261105/gate13_ppc_ifetch.log), gate PASS 359 checks, 0 fail.
2. Argon's floor gap ("quick_pc_to_pointers(cpu); deleted from arm (a)") -- REFUTED BY READING: arm (a) is `if (cpu->translation_readahead)
   return;` (cpu_ppc_instr.c:4144-4145); the quick_pc_to_pointers call is arm (b)'s (:4160-4163), whose deletion is D11 (a cell no
   measured session reaches).
3. GLM's floor gap (arm (a)'s guard conjoined with !(msr & ME)) -- BASE SIDE MEASURED: tra_me_base.out (this dir; build/gxemul md5
   ee2532155321): T ra with msr=0x1000 gives exit 0, pc 0xfec00008, 2 halt reports at 0xfec00008, machine stopped, srr0 unchanged, no
   checkstop or UNIMPLEMENTED.  The variant side is PREDICTED from W7's measured behaviour (arm (a) skipped during read-ahead -> pc == addr,
   so arm (b) is skipped and arm (c) parks: 1 report) and owes a build after gate 14.
4. D12's T ra outcome (Fable and grok disagreed with the errata's "presumably the garbage-decoded slot stopped the run") -- READ from
   table2/probe_D12_else_ra.out: T ra pc 0xfec00208, nonex 1, addr 0xfec00208, stopped yes.  One -T halt, at 0xfec00208 = 0xfec00008 +
   0x200: read-ahead translated 128 slots of garbage without a read, they ran, and the real fetch of 0xfec00208 halted.  grok's address is
   right; Fable's (0xfec0000c) and the errata's presumed cause are not.
5. Opus (c), "ppc_exception() leaves MSR[ME] set" unmeasured -- MEASURED TRUE (extra_sessions.out, session isi_me, build/gxemul md5
   ee2532155321): the probe's isi session with msr = IR|ME (0x1020) continues into the ISI: pc 0x400, SRR0 0x20000000, SRR1 0x1020, and
   MSR at the vector 0x1020 -- ME is still set.  ALSO MEASURED, and beyond this round: IR (0x20) is still set at the vector, where the
   architecture clears IR and DR on every exception (PEM Table 6-8) -- one more fact for the ppc_exception MSR-modelling filing (#QQQ's
   neighbour), no row here.
6. Fable item 5, single-step disables read-ahead -- MEASURED (extra_sessions.out): `T ra` with `step 1` instead of continue gives pc
   0xfec00008, 0 halt reports, not stopped (the subfic ran, no read-ahead); a second `step 1` gives 2 reports at 0xfec00008 and stops
   (the step-path read and the translator, as `T step`).  So the read-ahead cell is reached only by continue; the docstring's DERIVED
   clause should say so.
