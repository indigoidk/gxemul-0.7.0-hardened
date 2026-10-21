VERDICT: WITNESSED -- HEAD 5dbc000e: one guest ld/st to any of 7 uncased VME2 offsets exits the emulator (status 1); free-running at default verbosity it is silent.

(Measured by an Opus 5.5 sub-agent seat, 2026-10-20 ~19:1x-19:3x; this file is its final report, saved by the main loop
because the sub-agent harness refused to write a report .md.  Raw outputs beside it.)

HEAD 5dbc000e85d0e310305d876bb6ccc847ae571091 | dev_vme.c md5 2516a82bc777fe780f2dc6ccc00fd6c3 (only commit 39748e3c, upstream import)
Binary /tmp/gxvme_head_20261020/gxemul md5 7da30adb66fbee980b2e981b70d1ba56; -nt dev_vme.c: yes (weak: git archive sets
sources to commit time; fresh empty dir + make.log compiles are the evidence)
Probe: committed vme_sites_probe.py.txt, unmodified (md5 d4e86d3cdbd34798e37c6112fea87c87), label HEAD_5dbc000e

Site Reg        Off  Type  Result     Default-arm text (stepped transcript)
A1   MASTERCTL  0x28 read  NO (rc=1)  [ vme: unimplemented READ from offset 0x28 ]
A2   MASTER3    0x1c write NO (rc=1)  [ vme: unimplemented WRITE to offset 0x1c: 0x5a5a1234 ]
A3   MASTER4    0x20 write NO (rc=1)  [ vme: unimplemented WRITE to offset 0x20: 0x5a5a1234 ]
A4   MASTER4MOD 0x24 write NO (rc=1)  [ vme: unimplemented WRITE to offset 0x24: 0x5a5a1234 ]
A5   MASTERCTL  0x28 write NO (rc=1)  [ vme: unimplemented WRITE to offset 0x28: 0x5a5a1234 ]
H1   IRQSTAT    0x68 read  NO (rc=1)  [ vme: unimplemented READ from offset 0x68 ]
H2   IRQCLR     0x74 write NO (rc=1)  [ vme: unimplemented WRITE to offset 0x74: 0x5a5a1234 ]
Controls: (a) PASS (T1CMP 0x12345678 round trip, r4 0x1234, pc 0x1000c); (c) PASS; (b) constant print, NOT measured --
the 2026-10-09 probe prints control (b) as a fixed string (a check that cannot fail); on HEAD no site session reaches
its liveness `or`.
Identical to 2026-10-09 run_HEAD.out after masking binary path/label (diff_runHEAD_20261009_vs_20261020.txt).

Free-running (argv -V -x -E mvme88k -e mvme187 -M 64 0x10000:/tmp/vme_probe_dummy.bin; ld / or / c0000000 br-self
verified by unassemble; breakpoint 0x10008; continue; reg):
  KILL  r3=0xfff40028 x2: rc 1, "[ vme: unimplemented" absent, breakpoint not reached, output ends at "GXemul> continue"
  CTRL  r3=0xfff40050 x2: rc 0, BREAKPOINT pc=0x10008, r4 0x00001234, r2 0x00000000
  extra: KILL with -v -> rc 1 + "[ vme: unimplemented READ from offset 0x28 ]"; TCR (cased, debug()-only) free-running
  -> rc 0, no text; TCR stepped -> text present.  So debug() output is hidden whenever the emulator free-runs at default
  verbosity while exit(1) still runs.
Other-reason failures: none (no timeouts, no build failures, disassembly checked in every session).  The 2026-10-09
binary /tmp/gxppcwit/gxemul (md5 656c8bd5...) has no recorded build commit; md5s are not comparable across build dirs
(the banner embeds the build directory name).
Cleanup: /tmp/gxvme_head_20261020 removed after all outputs were saved.  No project tree written; every git command
read-only with --no-optional-locks.
Completion markers present: VME_SITES_DONE (run_HEAD_5dbc000e.out), VME_FREERUN_DONE (run_FREERUN_HEAD_5dbc000e.out).
