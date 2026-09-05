set -e
rm -rf /tmp/gxopus_p8
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build /tmp/gxopus_p8
mkdir -p /tmp/gxopus_p8/p8
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cp "$SEC/src/devices/dev_pcc2.c" /tmp/gxopus_p8/src/devices/dev_pcc2.c
cp "$SEC/regress/pcc2_width_probe.py" /tmp/gxopus_p8/p8/frozen_probe.py
chmod -w /tmp/gxopus_p8/p8/frozen_probe.py || true
echo "--- cmp dev_pcc2.c clone vs SEC ---"
cmp /tmp/gxopus_p8/src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" && echo "CMP CLEAN"
md5sum /tmp/gxopus_p8/src/devices/dev_pcc2.c "$SEC/src/devices/dev_pcc2.c" /tmp/gxopus_p8/p8/frozen_probe.py "$SEC/regress/pcc2_width_probe.py"
echo "--- baseline build ---"
cd /tmp/gxopus_p8
rm -f src/devices/dev_pcc2.o gxemul
make 2>&1 | tail -4
ls -la gxemul
if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo "FRESH_OK"; else echo "STALE_FAIL"; fi
