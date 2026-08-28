#!/bin/bash
#  Occurrence counts, not line counts: the warning interleaves with the guest
#  console stream, so a `grep -c` under-counts (measured 10 lines vs 12 hits).
for f in "$@"; do
    [ -f "$f" ] || { echo "$f MISSING"; continue; }
    w=$(grep -o 'WRITE: to non-existant paddr=0x1400002c' "$f" | wc -l)
    r=$(grep -o 'READ: from non-existant paddr=0x1400002c' "$f" | wc -l)
    lines=$(grep -c 'non-existant paddr=0x1400002c' "$f")
    other=$(grep -o 'non-existant paddr=0x140000[0-9a-f][0-9a-f]' "$f" | grep -v '0x1400002c' | wc -l)
    wd=$(grep -c 'wd0: 128-sector PIO' "$f")
    echo "$(basename $f): 2c_writes=$w 2c_reads=$r (naive grep -c lines=$lines) other_0x140000xx=$other wd0_line=$wd"
done
