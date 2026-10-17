#!/bin/bash
set -u
echo "uname: $(uname -r)"
gcc --version | head -1
echo "int main(void){return 0;}" > /tmp/asan_probe_fable.c
if gcc -O3 -fomit-frame-pointer -fsanitize=address /tmp/asan_probe_fable.c -o /tmp/asan_probe_fable 2>/tmp/asan_probe_fable.err; then
  if /tmp/asan_probe_fable; then echo ASAN_LINK_RUN_OK; else echo "ASAN_RUN_FAILED rc=$?"; fi
else
  echo "ASAN_LINK_FAILED"; head -3 /tmp/asan_probe_fable.err
fi
echo "int main(void){char b[4]; volatile int i=5; b[i]=1; return b[0];}" > /tmp/asan_probe_fable2.c
gcc -O0 -fsanitize=address /tmp/asan_probe_fable2.c -o /tmp/asan_probe_fable2
/tmp/asan_probe_fable2 > /tmp/asan_probe_fable2.out 2>&1
echo "overflow probe rc=$? first line: $(grep -m1 -E 'ERROR|AddressSanitizer' /tmp/asan_probe_fable2.out)"
echo "gcc -m32 asan link:"; if gcc -m32 -fsanitize=address /tmp/asan_probe_fable.c -o /tmp/asan_probe_fable32 2>/tmp/asan32.err; then echo M32_ASAN_LINK_OK; else echo "M32_ASAN_LINK_FAILED: $(head -1 /tmp/asan32.err)"; fi
ls -d /tmp/gxopus_fp5 /tmp/gxopus_f2 /tmp/gxfable_adjB 2>&1
df -h /tmp | tail -1; nproc; which python3; python3 --version; which patch md5sum
