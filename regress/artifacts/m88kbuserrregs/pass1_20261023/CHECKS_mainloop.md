# T36 pass 1 -- the main loop's own checks (reads of HEAD 7fca7187, 2026-10-23 ~21:45), each with what would refute it

1. `grep -n 'm8820x' src/cpus/cpu_m88k.c` -> only `:53 #include "thirdparty/m8820x_pte.h"`; `src/cpus/memory_m88k.c:46`
   includes `thirdparty/m8820x.h` and is its own object.  => A6 (the include is owed in `cpu_m88k.c`).  Refuted if a
   header already reached by `cpu_m88k.c` defines `CMMU_PFSR`: `git grep -n 'define CMMU_PFSR' HEAD -- src` must show
   only `src/include/thirdparty/m8820x.h`.
2. `src/debugger/debugger_cmds.c:1302`: `m->cpus[cpuid]->running = !m->cpus[cpuid]->running;` (the `pause` command).
   => B5c reachability.  Refuted if the main loop refuses to run a cpu that `pause` turned on -- the builder's first
   two-cpu session settles it (if cpu 1 never executes, the HANDLED/FELL markers both stay clear and the session is
   NOT BUILDABLE; say so).
3. `src/devices/dev_mvme187.c:136-137, 148-149`: CMMUs attached to `cpus[bootstrap_cpu]` only; `:141, :155` register
   `addr2=0` / `addr2=1`; `src/devices/dev_m8820x.c:542-543`: `cmmu_nr = addr2 & 1; cpu_nr = addr2 >> 1`.  => C4.
4. `src/devices/dev_m8820x.c:108` uses `cpu->cd.m88k.cmmu[d->cmmu_nr]->reg` (the ACCESSING cpu); `:250-252` use
   `cpus[d->cpu_nr]`.  => C5 and the B5c constraint.  NOT CHECKED here: which function `:108` is in and which guest
   accesses reach it -- the builder reads it before designing cpu 1's path.
5. `src/cpus/memory_m88k.c:130-132`: NULL CMMU -> `*return_paddr = vaddr; return 2`.  => B5c (cpu 1 addresses the
   `unreadable` window directly).
6. `src/core/emul.c:510-513, 742-748`: bootstrap cpu random only with the option; the other cpus get the bootstrap's
   pc; only the bootstrap cpu is started.  => A3's licence upgrade and B5c's dispatcher.
7. `ls regress/artifacts/m88kbuserrregs/witness_20261023/` -> one `.py` (`m88k_buserr_probe.py`); helpers are
   `*.py.txt` / `*.sh.txt`.  => B11 (two MANIFEST lines, no more).
8. `WITNESS_headbin.out:28`: `INFO ifetch ... path=v2 SXIP=0xfff46013 iPFSR=0x2468ace0 iPFAR=0xbadf00d dPFSR=0x5a5a5a5a
   dPFAR=0x13572468 pre-read-msg=1 halt-msg=0` -- the stepped instruction cell is reached on HEAD and keeps its seeds.
   => B5a's wants (RED on HEAD for `ifetch pfsr`/`ifetch pfar`).
9. All six seat files read whole; verdict lines agree with their bodies (no seat's body contradicts its verdict).
   The one body-vs-verdict tension: GLM-Q34:2 says Q4 "finds two real defects in sections 5-7" -- both are RECORDS
   corrections (B9), not product defects; carried as such.
10. NOT CHECKED (owed to the builder): compile of the four-file repair; the exact `pause`-session mechanics; the gate-14
    skip chain; whether any committed probe touches `0x3ffffff0`.
