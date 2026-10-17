#!/bin/bash
# fable5 adj B -- scratch clone OUTSIDE every project tree: /tmp/gxfable_adjB
set -u
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/adjB
W=/tmp/gxfable_adjB
rm -rf "$W"; mkdir -p "$W/head" "$W/comp" "$W/frozen"
cp "$P/stage/head/src/include/thirdparty/dreamcast_sysasicvar.h" "$W/head/"
cp "$P/stage/head/src/include/memory.h" "$W/"
cp "$P/stage/frozen/sysasic_range_check.py" "$P/stage/frozen/sysasic_range_cases.c" "$W/frozen/"
cp "$P/stage/dreamcast_sysasicvar.h.diff" "$W/"
cp "$P/cc_noasan.sh" "$W/"; chmod +x "$W/cc_noasan.sh"
echo "head header md5: $(md5sum < $W/head/dreamcast_sysasicvar.h | cut -c1-32)   (want daccce33a5df9e7c3093c310153ce92e)"
cp "$W/head/dreamcast_sysasicvar.h" "$W/comp/dreamcast_sysasicvar.h"
( cd "$W/comp" && patch -p4 --no-backup-if-mismatch dreamcast_sysasicvar.h < "$W/dreamcast_sysasicvar.h.diff" )
echo "composite header md5: $(md5sum < $W/comp/dreamcast_sysasicvar.h | cut -c1-32)   (want 6b5cc64842911e4566ffff6d400a82c1)"
echo "memory.h md5: $(md5sum < $W/memory.h | cut -c1-32)"
echo "driver md5: $(md5sum < $W/frozen/sysasic_range_check.py | cut -c1-32)  cases md5: $(md5sum < $W/frozen/sysasic_range_cases.c | cut -c1-32)"
python3 -I "$P/gen_media.py" "$W" | tee "$W/MEDIA.tsv"
python3 -I "$P/mk_variants.py" "$W"
for v in orig pinned pinned_sample pinned_preflight sizeof_both pinned_mw2; do
  echo "  $v driver md5 $(md5sum < $W/variants/$v/sysasic_range_check.py | cut -c1-12) cases md5 $(md5sum < $W/variants/$v/sysasic_range_cases.c | cut -c1-12)"
done
diff "$W/variants/orig/sysasic_range_cases.c" "$W/variants/pinned/sysasic_range_cases.c" > "$W/pinned_cases.diff"
diff "$W/variants/orig/sysasic_range_check.py" "$W/variants/pinned/sysasic_range_check.py" > "$W/pinned_driver.diff"
diff "$W/variants/pinned/sysasic_range_check.py" "$W/variants/pinned_preflight/sysasic_range_check.py" > "$W/preflight_driver.diff"
echo "pinned cases diff lines: $(grep -c '^[<>]' $W/pinned_cases.diff); pinned driver diff lines: $(grep -c '^[<>]' $W/pinned_driver.diff); preflight diff lines: $(grep -c '^[<>]' $W/preflight_driver.diff)"
for v in orig pinned pinned_sample pinned_preflight sizeof_both pinned_mw2; do
  python3 -c "import ast; ast.parse(open('/tmp/gxfable_adjB/variants/$v/sysasic_range_check.py').read())" && echo "  $v driver parses"
done
echo SETUP_DONE
