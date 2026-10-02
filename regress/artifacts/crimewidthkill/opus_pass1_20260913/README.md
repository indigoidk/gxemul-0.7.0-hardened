# crimewidthkill -- Opus seat, pass 1 (design), 2026-09-13

This is the compile-and-measure seat's evidence for the `DEVICE_ACCESS(crime)` width-guard design question.
Everything was built in a scratch clone (`/tmp/gxopuscrime`, a `cp -a` of `build/`). No project build tree was
touched, and nothing in GXEMUL-SEC was written except this directory.

## Baseline (named, then checked)
* Baseline = HEAD `9c91999`'s `src/devices/dev_sgi_ip32.c`. The clone's copy `cmp`s CLEAN against GXEMUL-SEC. So do
  the dispatch-path files (`memory_rw.c`, `cpu_mips*.c`, `machine_sgi.c`, `crimereg.h`, `dev_unreadable.c`); see
  `scripts/build_variants.out`.
* The baseline was rebuilt inside the clone (`rm dev_sgi_ip32.o && make -j4`; binary `-nt` source).
  The committed witness then gives **3/15, CONTROL=OK** (`out/witness_base.out`), matching `../witness_committed.out`.
* After the tables ran, the clone was restored from SEC and rebuilt. The restored binary is byte-identical to the
  base binary, the source `cmp`s clean, and the sentinel is cleared (`scripts/build_mutants.out`).

## Binaries (all built with `rc=0 fresh=yes`; every variant differs from base)
| label | shape | diff |
|---|---|---|
| base | committed code | -- |
| fault | member 5: `return 0;` in place of `fatal+exit(1)` | `diffs/fault.diff` |
| decline | member 3: per-instance `warned_len` latch, `(once)` text, **`goto crime_common_tail`**, which skips the switch | `diffs/decline.diff` |
| delete | member 1: the else-arm removed, so a narrow access falls into the switch with no store and no load | `diffs/delete.diff` |
| return1 | mutant of decline: `return 1;` instead of the goto (skips the common tail) | `diffs/return1.diff` |
| fallsw | mutant of decline: latch kept, goto deleted (falls into the switch) | `diffs/fallsw.diff` |
| nolatch | mutant of decline: latch never set | `diffs/nolatch.diff` |
| len1only | clause-(d) mutant: decline conditioned `else if (len == 1)` | `diffs/len1only.diff` |
| readonly | clause-(d) mutant: decline conditioned `else if (writeflag == MEM_READ)` | `diffs/readonly.diff` |

## Instruments
* `out/witness.FROZEN.py` is the committed witness, byte-identical (md5 `a2bb3f2d...`).
* `out/crime_opus_rows.FROZEN.py` is the observational probe (md5 `0f148fd8...`). It uses the same apparatus and
  prints what the guest sees rather than grading anything. `run1_base/` holds an earlier run on base only, made with
  the previous probe version (which lacked the `sw CTL+08` row).
* The probe was frozen by copy for the whole comparison run, so all nine binaries were measured by one instrument.
  Every preserved log ends in its completion sentinel (`CRIMEO_DONE` / `CRIMEW_DONE`).

## Results (MEASURED; the logs are in `out/`)
| cell | base | fault | decline | delete |
|---|---|---|---|---|
| committed witness | 3/15 | 15/15 | 15/15 | 15/15 |
| lb/lbu +7, lh/lhu +6: dest (seeded 0xdeadbeef) | host exit 1 | **0xdeadbeef** (untouched) | 0x0 | 0x0 |
| ... pc after / ExcCode / EPC | -- | **0xffffffff80000180 / 7 (DBE) / faulting pc** | pc+4 / -- / -- | pc+4 |
| sb +0x37, sh +0x36 over an accepted `sw 0x0badcafe` | host exit 1 | DBE, word unchanged | word unchanged | word unchanged |
| `sh 0x0800 -> +0x08` (CONTROL case label, BE lane of bits 63:48) | exit 1 | DBE, machine runs | machine runs | **"emul: All machines stopped."** |
| `sh 0x0800 -> +0x0e` (the BE lane that actually holds bit 11) | exit 1 | DBE | runs | runs, nothing happens |
| `sb 0x01 -> +0x08` | exit 1 | DBE | runs, silent | **`[ CRIME_CONTROL: unimplemented control 0x...01 ]`** |
| lb/lh at +0 from pc 0xbfc05180, ra=0x80004000 | exit 1 | DBE | pc=0xbfc05184 | **pc=0x80004000 (PROM-probe hack fired)** |
| 5 refused accesses, one session: host text | exit 1 at #1 | 5x `[ ... device 'crime' addr .. failed ]` (debug) | **1x `(once)`** | 5x `[ crime: read/write ... ]` (debug) |
| FREE-RUNNING (`breakpoint add` + `continue`), lb +7: host text | exit 1 | **NOTHING printed**; guest at vector 0x80000180, ExcCode 7 | `(once)` printed; host alive | nothing printed; host alive |
| accept cells: sd/ld, lw hi/lo, sw then ld, lw/ld REV | same | same | same | same |
| `sw 0x800 -> +0x08` (the existing 4-byte arm) | machine stopped | machine stopped | machine stopped | machine stopped |
| `sw 0x800 -> +0x0c` (the existing 4-byte arm, correct lane) | default arm, nothing | same | same | same |
| `-M 48`, then `lw +4` | exit 1 (RAM-size kill) | same | same | same |

Mutants of decline, diffed against decline's rows (`scripts/compare.out`):
* **return1: 0 differing lines in either direction.** It is EQUIVALENT on every channel here. For a refused access,
  memory_rw's `#95` pre-zero (`memset(data, 0, len)` above `paddr -= mem->devices[i].baseaddr;`) already zeroes the
  read buffer, and the tail's HARDINT/INTSTAT writes are no-ops. So a detector cannot tell whether the tail runs.
  Disclose this; do not row it.
* **fallsw:** value rows identical (v0 = 0; stores do not land). It differs on `sh CTL+08` (machine stopped),
  `sb CTL+08` (control text), revhack lb/lh (pc = ra) and the default-arm debug text.
* **nolatch:** differs only on the latch-count row (5 announcements, not 1).
* **len1only / readonly:** value rows identical to decline. The committed witness gives 15/15. They are seen only
  by (i) the announce text in a session whose one refused access is of the un-declined width or direction, and
  (ii) the switch side-effect rows (`sh CTL+08` halts; revhack lh redirects; `sb CTL+08` prints).

The committed witness scores **15/15 on all eight non-base binaries.** It is survival-only by design, and it cannot
tell the members apart.

## Apparatus notes
* The decline free-run row's breakpoint at the `b .` did not fire (`how=sig9`: the host was alive and the harness
  killed it). A breakpoint inside the same dyntrans run is not re-checked. So that row measures text and survival
  only. The fault free-run row's breakpoint at the exception vector did fire.
* git-bash environment variables do not reach `wsl ... bash`, so `WITNESS=0` in the first launch was a no-op. The
  first run therefore also ran the witness, which is harmless.
