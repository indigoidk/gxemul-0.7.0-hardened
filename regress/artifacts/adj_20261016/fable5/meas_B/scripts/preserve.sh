#!/bin/bash
# fable5 adj B -- assemble the durable measurement directory meas_B from the scratch clone.
set -u
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/adjB
W=/tmp/gxfable_adjB
M=$W/meas_B; rm -rf "$M"; mkdir -p "$M/out" "$M/diffs" "$M/rowlogs_sel" "$M/latent" "$M/scripts" "$M/variants" "$M/media"
cp "$W/RESULTS.txt" "$W/RESULTS_shape.txt" "$W/MEDIA.tsv" "$W/JOBS.txt" "$M/"
cp "$P/MATRIX.out" "$P/SHAPE.out" "$P/LATENT.out" "$M/"
cp "$W"/out/*.out "$M/out/"
cp "$W"/pinned_cases.diff "$W"/pinned_driver.diff "$W"/preflight_driver.diff "$W"/shape_cases.diff "$W"/shape_driver.diff "$M/diffs/"
for t in pinned/BASE pinned/cand_buf4 pinned/ptr4 pinned/ptr8 pinned/cast_uc pinned/cast_u8 pinned/plus0 pinned/u64obj pinned/static8 pinned/cand_buf16 pinned/sz8 pinned/cand_rwlen_hex pinned/T54_MEM_WRITE_2 \
         pinned@noasan/BASE sizeof_both/ptr4 sizeof_both/ptr8 sizeof_both/cand_buf4 pinned_mw2/BASE pinned_mw2/T54_MEM_WRITE_2 \
         pinned_shape/BASE pinned_shape/A_enoparen pinned_shape/B_enoparen pinned_sample/e1noparen pinned_sample/e2noparen; do
  mkdir -p "$M/rowlogs_sel/$t"
  for f in PROD_ID.run PROD_TVAL.run PROD_ID.err PROD_TVAL.err; do [ -f "$W/rowlogs/$t/$f" ] && cp "$W/rowlogs/$t/$f" "$M/rowlogs_sel/$t/"; done
done
#  the sweeps' first wrongly accepted/refused line, from the kept sweep logs, for the four shape media (the full .err is MBs)
for t in pinned_sample/e1noparen pinned_sample/e2noparen pinned_shape/A_enoparen pinned_shape/B_enoparen; do
  for f in PROD_SWEEP.err PROD_TSWEEP.err; do
    [ -f "$W/rowlogs/$t/$f" ] && { echo "== $t/$f: $(wc -l < $W/rowlogs/$t/$f) lines, first 3 error lines:"; grep -m3 ': error: ' "$W/rowlogs/$t/$f"; } >> "$M/rowlogs_sel/sweep_heads.txt"
  done
done
cp "$W"/latent/*.c "$W"/latent/*.err "$M/latent/" 2>/dev/null
for m in BASE A_enoparen B_enoparen e1noparen e2noparen; do [ -x "$W/latent/indomain_$m" ] && "$W/latent/indomain_$m" > "$M/latent/indomain_$m.out"; done
cp "$P"/gen_media.py "$P"/mk_variants.py "$P"/mk_variant2.py "$P"/mk_indomain.py "$P"/cc_noasan.sh "$P"/setup.sh "$P"/run_matrix.sh "$P"/run_shape.sh "$P"/latent.sh "$P"/wsl_check.sh "$P"/preserve.sh "$M/scripts/"
for v in orig pinned pinned_sample pinned_preflight sizeof_both pinned_mw2 pinned_shape; do mkdir -p "$M/variants/$v"; cp "$W/variants/$v/"* "$M/variants/$v/"; done
for m in $(ls "$W/media"); do mkdir -p "$M/media/$m"; cp "$W/media/$m/thirdparty/dreamcast_sysasicvar.h" "$M/media/$m/"; done
cp "$W/comp/dreamcast_sysasicvar.h" "$M/media/COMPOSITE_header_6b5cc648.h"
cp "$W/memory.h" "$M/media/memory.h_HEAD"
cat > "$M/README.txt" <<'EOF'
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
EOF
( cd "$M" && find . -type f ! -name MANIFEST.md5 -print0 | sort -z | xargs -0 md5sum > MANIFEST.md5 )
echo "meas_B files: $(find $M -type f | wc -l); bytes: $(du -sb $M | cut -f1)"
rm -rf "$P/meas_B"; cp -r "$M" "$P/meas_B"
echo "copied to scratchpad: $(find $P/meas_B -type f | wc -l) files"
echo PRESERVE_DONE
