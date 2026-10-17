fable5 adjudication B (asiceventaddr, 2026-10-16) -- MEASUREMENTS, all in a scratch clone /tmp/gxfable_adjB (WSL2 Gentoo,
gcc 15.2.1 20260214, LP64); no project tree was read for compiling and none was written.  Inputs: the HEAD header and
memory.h via `git archive e483d931' (md5 daccce33a5df9e7c3093c310153ce92e / c6df57c550707a6415a5f6cfefdceb8a), the composite
header = HEAD + deliver/dreamcast_sysasicvar.h.diff (md5 6b5cc64842911e4566ffff6d400a82c1, the build's own number), the frozen
instrument deliver/sysasic_range_check.py (78b7fa63a2c563d924355aee4f6a0433) and sysasic_range_cases.c
(68ae679e01f4a6bf882ed1127a7703b5).  Header media by exact replacement (MEDIA.tsv; the md5s of cand_buf4, cand_buf16,
cand_rwlen_hex, static8, e1noparen, e2noparen, A_enoparen, B_enoparen equal the measuring seat's).
  RESULTS.txt        the 57-job matrix: driver variant x header medium (orig; pinned = PIN's A+B+C; pinned_sample = + the
                     SWEEP/TSWEEP sample `1 ? 200 : 5'; pinned_preflight = + an ASAN preflight; sizeof_both = opus5's
                     sizeof-capture stub; pinned_mw2 = the stub's MEM_WRITE drifted to 2; @noasan = a compiler wrapper
                     that fails every -fsanitize=address link the way ld does).  Every run: 30 rows (28 + ID/TVAL).
  RESULTS_shape.txt  pinned_shape = pinned_sample + the in-domain sample `1 ? 33 : 0' + two TX raises in TVAL.
  MATRIX.out / SHAPE.out / LATENT.out   the three drivers' full stdout (LATENT: the oracle-shaped compile of
                     `SYSASIC_TRIGGER_EVENT(1 ? 200 : 5)' and the in-domain run program).
  out/               every run's driver output (row lines, counts, verdict token).
  rowlogs_sel/       the ID/TVAL compile and run logs for the extent, length, writeflag and shape media (ASAN reports
                     inside the .run files); sweep_heads.txt = the first error lines of the sweeps on the shape media.
  diffs/             the pinned stub/driver against the frozen deliverables; the preflight; the shape additions.
  variants/ media/ scripts/   everything needed to re-run: setup.sh then run_matrix.sh, latent.sh, run_shape.sh.
