#!/bin/bash
#  Run the #485 rung-3 witness against BOTH builds with the SAME script, then run the
#  no-disk NEGATIVE CONTROL against the pre-fix build.
#
#  Test-first, restated per-probe: the identical file must show the symptom on the
#  PRE-FIX build and go green on the POST-FIX one.  Nothing here edits GXEMUL-SEC, and
#  neither build tree is the live C:\...\GXEMUL\build\ tree.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/witness485
IMG=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images
KERNEL=$IMG/openbsd76-landisk-bsd.rd
DISK=/tmp/wdc485scratch.img

#  Local copy: the gxemul process reads this for the whole run, and /mnt/c is slow.
[ -f "$DISK" ] || cp "$IMG/wdc-scratch-64m.img" "$DISK"

for lab in pre post; do
    BIN=/tmp/gxw485$lab/gxemul
    echo "==================================================================== $lab"
    echo "binary  $BIN"
    md5sum "$BIN"
    echo -n "int_assert = 1; sites in its dev_wdc.c: "
    grep -c 'int_assert = 1;' /tmp/gxw485$lab/src/devices/dev_wdc.c
    python3 -u "$W/wdcnoirq_rung3_probe.py" "$BIN" "$KERNEL" "$DISK" "$lab" \
        2>&1 | tee "$W/rows_$lab.out"
done

echo "==================================================================== pre, NO DISK"
echo "NEGATIVE CONTROL: wdc_command()'s no-disk early return asserts for EVERY opcode,"
echo "so the two defect rows go GREEN on the unfixed binary.  This is why the witness"
echo "attaches an image, and it is a measurement rather than a caution."
WDCNOIRQ_NODISK=1 python3 -u "$W/wdcnoirq_rung3_probe.py" \
    /tmp/gxw485pre/gxemul "$KERNEL" "$DISK" "pre_nodisk" \
    2>&1 | tee "$W/rows_pre_nodisk.out"
