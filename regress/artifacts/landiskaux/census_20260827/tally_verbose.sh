#!/bin/bash
f="$1"
echo "log bytes: $(wc -c < "$f")"
for pat in 'wdc: read from ALTSTATUS' 'wdc: write to ALT. CTRL' 'wdc: read from DATA' 'wdc: write to DATA' 'wdc: WARNING'; do
    printf '%-32s %s\n' "$pat" "$(grep -o "$pat" "$f" | wc -l)"
done
echo "2c writes: $(grep -o 'WRITE: to non-existant paddr=0x1400002c' "$f" | wc -l)"
echo "wd0 line : $(grep -c 'wd0: 128-sector PIO' "$f")"
