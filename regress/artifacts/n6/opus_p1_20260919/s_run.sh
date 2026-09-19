#!/bin/bash
# Run the n6 measuring probe in the scratch clone.
set -u
T=/tmp/gxopus539p1
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/n6/opus_p1_20260919
mkdir -p "$T/out"
python3 -c "import struct,sys; open(sys.argv[1],'wb').write(struct.pack('<I',0xe1a00000))" "$T/out/arm_stub.bin" || exit 9
ls -la "$T/out/arm_stub.bin"
cd "$T" || exit 9
python3 -u "$D/opus_m.py" "$T/gxemul" "$T/out/arm_stub.bin" > "$T/out/opus_m.raw" 2>&1
echo "PROBE_RC=$?"
echo "sentinel: $(tail -1 "$T/out/opus_m.raw")"
cp "$T/out/opus_m.raw" "$D/opus_m.raw"
wc -l "$T/out/opus_m.raw"
